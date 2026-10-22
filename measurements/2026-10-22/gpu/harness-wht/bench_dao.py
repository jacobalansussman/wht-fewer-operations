#!/usr/bin/env python3
"""bench_dao.py -- the strongest public CUDA WHT baselines, and the 5/6 / 3/4 steps patched INTO the strongest one.
22 Oct 2026.  UNTESTED on a GPU when written (no CUDA on the Mac).  Run by run.sh.

1. Dao-AILab fast-hadamard-transform (BSD-3), JIT-built twice from one source tree, two module names, one process:
     fht_tb  : as shipped (textbook butterflies in the per-thread register stage)
     fht_g   : the same tree with hadamard_mult_thread<3,...> -> the 19-line step (G19) and <4,...> -> the 52-line
               family step (G52)  (patch: patch_dao.py; fp16/bf16 hold 8 values per thread, fp32 holds 4, so fp32 rows
               only see the change through the chunk stage)
2. HadaCore (pytorch-labs/applied-ai, tensor-core WHT, fp16/bf16, sm_80+), if it builds.
3. torch reference: x @ H (fp32 matmul) for correctness only.
Every variant is checked against an fp64 reference first; any failure stops the script before timing (exit 3).
Timing: CUDA events around back-to-back calls, >= 0.2 s per repeat, 9 repeats, variants taking turns; GB/s counts
one read and one write of the tensor.  The GPU kernel is the thing timed (Python only launches; the batch is large
enough that launch overhead is < 1 %: checked by printing the time per call).
"""
import os, sys, time, importlib, math
import torch
from torch.utils.cpp_extension import load

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
SRC = os.environ.get('K0SRC', '/content/k0src')
dev = torch.device('cuda')
cap = torch.cuda.get_device_capability()
os.environ.setdefault('TORCH_CUDA_ARCH_LIST', f'{cap[0]}.{cap[1]}')
print('torch', torch.__version__, 'cuda', torch.version.cuda, 'gpu', torch.cuda.get_device_name(), 'cap', cap, flush=True)

NVCC = ['-O3', '-U__CUDA_NO_HALF_OPERATORS__', '-U__CUDA_NO_HALF_CONVERSIONS__', '-U__CUDA_NO_BFLOAT16_OPERATORS__',
        '-U__CUDA_NO_BFLOAT16_CONVERSIONS__', '-U__CUDA_NO_BFLOAT162_OPERATORS__', '-U__CUDA_NO_BFLOAT162_CONVERSIONS__',
        '--expt-relaxed-constexpr', '--expt-extended-lambda', '--use_fast_math', '-lineinfo']


def _bd(name):  # fix 22 Oct: torch's load() needs the build folder to exist
    d = os.path.join(os.environ.get('KBUILD', '/content/k0build'), name); os.makedirs(d, exist_ok=True); return d


def build(name, src, flags):
    t = time.time()
    m = load(name=name, sources=[os.path.join(src, 'csrc/fast_hadamard_transform.cpp'),
                                 os.path.join(src, 'csrc/fast_hadamard_transform_cuda.cu')],
             extra_cflags=['-O3'], extra_cuda_cflags=NVCC + flags, extra_include_paths=[src],
             build_directory=_bd(name), verbose=False)
    print(f'built {name} in {time.time() - t:.0f} s', flush=True)
    return m


def hadamard(n, dtype=torch.float64):
    H = torch.ones(1, 1, dtype=dtype)
    while H.shape[0] < n:
        H = torch.cat([torch.cat([H, H], 1), torch.cat([H, -H], 1)], 0)
    return H.to(dev)


def check(fn, name, dims, dtypes, supported):
    """numeric mismatch = failure; an exception (size or type the library does not take) = unsupported, skipped."""
    ok = True
    for n in dims:
        H = hadamard(n)
        for dt in dtypes:
            x = torch.randn(64, n, device=dev, dtype=torch.float32).to(dt)
            ref = (x.double() @ H)  # rows times H (H symmetric)
            try:
                y = fn(x).double()
                torch.cuda.synchronize()
            except Exception as e:  # noqa: BLE001
                print(f'CHECK {name:10s} n={n:6d} {str(dt):15s} UNSUPPORTED ({str(e)[:120]})', flush=True)
                continue
            sc = ((y * ref).sum() / (ref * ref).sum()).item()  # a library may normalise (e.g. 1/sqrt(n))
            # review fix 17: only the three usual scales are accepted (1, n^-1/2, n^-1); any other
            # fitted scale (a step computing c*H) is a FAIL, not a NOTE.
            allowed = [1.0, n ** -0.5, 1.0 / n]
            near = min(allowed, key=lambda a: abs(sc / a - 1))
            if abs(sc / near - 1) > 1e-2:
                print(f'CHECK {name:10s} n={n:6d} {str(dt):15s} output is {sc:.6g} x H: not 1, n^-1/2 or n^-1: FAIL', flush=True)
                ok = False
                continue
            if abs(sc - 1) > 1e-3:
                print(f'NOTE {name} n={n} {dt}: output is {sc:.6g} x H x (normalised); compared after dividing by {near:.6g}', flush=True)
                y = y / near
            err = ((y - ref).abs().max() / ref.abs().max()).item()
            tol = {torch.float32: 1e-5, torch.float16: 2e-2, torch.bfloat16: 5e-2}[dt]
            p = err < tol
            ok &= p
            if p:
                supported.add((name, n, dt))
            print(f'CHECK {name:10s} n={n:6d} {str(dt):15s} rel err {err:.3e} {"PASS" if p else "FAIL"}', flush=True)
    n = dims[0]; x = torch.randn(4, n, device=dev).to(dtypes[0]); ref = x.double() @ hadamard(n)
    y = fn(x).double(); y = y / ((y * ref).sum() / (ref * ref).sum()); y[0, n // 2 + 1] = -y[0, n // 2 + 1]
    caught = ((y - ref).abs().max() / ref.abs().max()).item() > 5e-2
    print(f'CHECK {name:10s} broken copy {"CAUGHT" if caught else "NOT CAUGHT"}', flush=True)
    return ok and caught


def time_turns(title, fns, x, out_bytes):
    """fns: list of (name, callable(x)).  Prints every repeat and RESULT lines."""
    ev0, ev1 = torch.cuda.Event(enable_timing=True), torch.cuda.Event(enable_timing=True)
    calls = []
    for nm, f in fns:
        c = 1
        while True:
            ev0.record()
            for _ in range(c):
                f(x)
            ev1.record(); ev1.synchronize()
            ms = ev0.elapsed_time(ev1)
            if ms >= 200:
                break
            c = c * 8 if ms < 12 else int(c * 220 / ms) + 1
        calls.append(c)
    reps = [[] for _ in fns]
    print(f'## {title} (9 repeats of >= 0.2 s, variants take turns)', flush=True)
    for r in range(9):
        for jj in range(len(fns)):
            k = (jj + r) % len(fns)
            nm, f = fns[k]
            ev0.record()
            for _ in range(calls[k]):
                f(x)
            ev1.record(); ev1.synchronize()
            us = ev0.elapsed_time(ev1) * 1e3 / calls[k]
            reps[k].append(us)
            print(f'rep {r} {nm:12s} {us:10.3f} us/call', flush=True)
    base = None
    for (nm, _), rr in zip(fns, reps):
        s = sorted(rr)
        med = s[4]
        base = base or med
        print(f'RESULT {title} {nm:12s} best {s[0]:.3f} median {med:.3f} us/call  {2 * out_bytes / (med * 1e3):.1f} GB/s  '
              f'ratio-vs-{fns[0][0]} {med / base:.4f}', flush=True)


def main():
    dao = os.path.join(SRC, 'fast-hadamard-transform')
    dao_g = os.path.join(SRC, 'fast-hadamard-transform-g')
    mods = {}
    mods['dao'] = build('fht_tb', dao, [])
    mods['dao_g'] = build('fht_g', dao_g, ['-DFHT_G19', '-DFHT_G52'])
    fns = {'dao': lambda x: mods['dao'].fast_hadamard_transform(x, 1.0),
           'dao+g19g52': lambda x: mods['dao_g'].fast_hadamard_transform(x, 1.0)}
    hcdir = os.path.join(SRC, 'applied-ai', 'kernels', 'cuda', 'inference', 'hadamard_transform')
    if cap[0] >= 8 and os.path.isdir(hcdir):
        try:
            t = time.time()
            hc = load(name='hadacore', sources=[os.path.join(hcdir, 'hadamard_transform.cpp'),
                                                os.path.join(hcdir, 'hadamard_transform_cuda.cu')],
                      extra_cflags=['-O3'], extra_cuda_cflags=['-O3', '-lineinfo'],
                      build_directory=_bd('hadacore'))
            print(f'built hadacore in {time.time() - t:.0f} s', flush=True)
            fns['hadacore'] = lambda x: hc.hadamard_transform(x, False)
        except Exception as e:  # noqa: BLE001
            print('HadaCore did not build:', repr(e)[:500], flush=True)
    else:
        print('HadaCore skipped (needs sm_80+ and the source)', flush=True)
    dims = [256, 512, 4096, 8192, 16384, 32768]
    ok, sup = True, set()
    for nm in list(fns):
        dts = [torch.float32, torch.float16, torch.bfloat16] if nm != 'hadacore' else [torch.float16, torch.bfloat16]
        try:
            ok &= check(fns[nm], nm, dims, dts, sup)
        except Exception as e:  # noqa: BLE001
            print(f'CHECK {nm} raised {e!r}'[:400], flush=True)
            if nm == 'hadacore':
                fns.pop('hadacore'); continue
            ok = False
    print('ALL', 'PASS' if ok else 'FAIL', flush=True)
    if not ok:
        sys.exit(3)
    for dt in (torch.float16, torch.bfloat16, torch.float32):
        for n in dims:
            vs = [(k, f) for k, f in fns.items() if (k, n, dt) in sup]
            if len(vs) < 2:
                continue
            rows = (64 << 20) // (n * torch.tensor([], dtype=dt).element_size())  # 64 MiB tensor (past L2 on T4/L4)
            x = torch.randn(rows, n, device=dev, dtype=torch.float32).to(dt)
            time_turns(f'{str(dt)[6:]} n={n} rows={rows}', vs, x, x.numel() * x.element_size())
            del x
    torch.cuda.empty_cache()


if __name__ == '__main__':
    main()
