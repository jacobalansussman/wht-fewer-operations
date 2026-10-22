"""bench.py TAG OUT_JSON -- time Dao's hadamard_transform_{12,20,28,40}N against the power-of-two transform and
a plain copy (memory floor), on the GPU, for the build found on PYTHONPATH.  CUDA events, 20 warm-up + 200
timed calls per point, median of 7 rounds.  Also saves outputs on a fixed input for the cross-check."""
import sys, os, re, json, math, time, torch
import fast_hadamard_transform.fast_hadamard_transform_interface as F
tag, outp = sys.argv[1], sys.argv[2]
dev = 'cuda'
torch.manual_seed(0)
cases = [('12N', 12, 1024), ('20N', 20, 512), ('28N', 28, 512), ('28N', 28, 1024), ('40N', 40, 512)]
batches = [1, 16, 256, 4096]
dtypes = [torch.float16, torch.bfloat16, torch.float32]
mm = tag.startswith('mm')     # ay-h0: QuaRot-style rival: pow2 transform (orig build) + K x K matmul (tensor cores in fp16/bf16)
if mm:
    _src = open(os.environ['HAD_CODEGEN']).read(); _mats = {}
    for _n, _b in re.findall(r'(had_\w+)\s*=\s*"""(.*?)"""', _src, re.S):
        _mats[_n] = [[1.0 if ch == '+' else -1.0 for ch in r.strip()] for r in _b.strip().splitlines() if r.strip()]
    _use = {12: 'had_12_paley', 20: 'had_20_will', 28: 'had_28_will', 40: 'had_40_tpal'}
    HK = {K: torch.tensor(_mats[_use[K]], device=dev) for K in _use}
    def mmroute(z, K, P, scale, layout):
        B = z.shape[0]
        if layout == 'A':   # K is the slow index: x viewed as (B, K, P)
            y = F.hadamard_transform(z.reshape(B, K, P), scale)
            return torch.matmul(HK[K].to(z.dtype), y).reshape(B, K * P)
        y = F.hadamard_transform(z.reshape(B, P, K).transpose(1, 2).contiguous(), scale)
        return torch.matmul(HK[K].to(z.dtype), y).transpose(1, 2).contiguous().reshape(B, K * P)
fn = {'12N': F.hadamard_transform_12N, '20N': F.hadamard_transform_20N, '28N': F.hadamard_transform_28N, '40N': F.hadamard_transform_40N}
def t(f, x, reps=200):
    for _ in range(20): f(x)
    torch.cuda.synchronize()
    meds = []
    for _ in range(7):
        a, b = torch.cuda.Event(enable_timing=True), torch.cuda.Event(enable_timing=True)
        a.record()
        for _ in range(reps): f(x)
        b.record(); torch.cuda.synchronize()
        meds.append(a.elapsed_time(b) * 1e3 / reps)
    meds.sort(); return meds[3], meds[0]
res = {'tag': tag, 'gpu': torch.cuda.get_device_name(), 'torch': torch.__version__, 'rows': [], 'outputs': {}}
for name, K, P in cases:
  d = K * P
  try:
    if mm:                                    # pick the layout that equals Dao's own K-part (orig build on the path)
        xx = torch.randn(4, d, device=dev); ref = fn[name](xx, 1.0); lay = None
        for L in ('A', 'B'):
            if torch.allclose(mmroute(xx, K, P, 1.0, L), ref, rtol=1e-4, atol=1e-3 * ref.abs().max().item()): lay = L; break
        print('mm route layout for', name, d, ':', lay, flush=True)
        if lay is None: raise RuntimeError('mm route does not match Dao output in either layout')
        f_case = lambda z, sc: mmroute(z, K, P, sc, lay)
    else:
        f_case = lambda z, sc: fn[name](z, sc)
    for dt in ([] if os.environ.get('BENCH_CHECK_ONLY') else dtypes):   # check-only run = outputs, no timing
        for B in batches:
            x = torch.randn(B, d, device=dev, dtype=dt)
            med, best = t(lambda z: f_case(z, 1.0 / math.sqrt(d)), x)
            p2 = 1 << math.ceil(math.log2(d))
            y = torch.randn(B, p2, device=dev, dtype=dt)
            med2, _ = t(lambda z: F.hadamard_transform(z, 1.0 / math.sqrt(p2)), y)
            medc, _ = t(lambda z: z.clone(), x)
            gbs = 2 * x.numel() * x.element_size() / (med * 1e-6) / 1e9
            res['rows'].append(dict(case=name, K=K, d=d, dtype=str(dt), B=B, us=med, us_best=best, us_pow2=med2, pow2=p2, us_copy=medc, GBps=gbs))
            print('%s %-4s d=%6d %-15s B=%5d  %9.2f us (best %9.2f)  pow2 %d: %9.2f us  copy %9.2f us  %7.1f GB/s'
                  % (tag, name, d, dt, B, med, best, p2, med2, medc, gbs), flush=True)
    g = torch.Generator(device='cpu').manual_seed(1)
    x = torch.randn(8, d, generator=g, dtype=torch.float32).to(dev)
    res['outputs']['%s_%d' % (name, d)] = f_case(x, 1.0).cpu().tolist()
  except Exception as e:                      # e.g. a size the library does not support
    print('SKIP', name, d, repr(e)[:200], flush=True)
json.dump(res, open(outp, 'w'))
