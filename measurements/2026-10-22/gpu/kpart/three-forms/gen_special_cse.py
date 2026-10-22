"""gen_special_cse.py CODE_GEN_PY OUT_H -- write a drop-in fast_hadamard_transform_special.h for Dao's
fast-hadamard-transform in which hadamard_mult_thread_{12,20,28,40} use a greedy common-subexpression
circuit for the SAME matrices (had_12_paley, had_20_will, had_28_will, had_40_tpal) instead of dense
signed sums.  Checks each circuit exactly (random integer vectors) before writing.  ax-h0, wave 16."""
import sys, random
cg, outp = sys.argv[1], sys.argv[2]
src = open('cse.py').read().split('rng = random.Random(1)')[0]
ns = {}; sys_argv = sys.argv; sys.argv = ['cse.py', cg, '0']; exec(src, ns); sys.argv = sys_argv
mats, greedy, check = ns['mats'], ns['greedy'], ns['check']
rng = random.Random(7)
hdr = ['', '#pragma once', '']
for name in ('had_12_paley', 'had_20_will', 'had_28_will', 'had_40_tpal'):
    M = mats[name]; K = len(M)
    best = None
    for t in range(200):                       # tie-break tries only; the matrix itself is unchanged
        ops, defs, rows = greedy([r[:] for r in M], rng)
        if best is None or ops < best[0]: best = (ops, defs, rows)
    ops, defs, rows = best
    assert check(M, defs, rows, rng), name
    print('%s: %d additions (dense %d)' % (name, ops, K * (K - 1)))
    b = ['__device__ __forceinline__ void hadamard_mult_thread_%d(float x[%d]) {' % (K, K),
         '    /* %s: greedy-CSE circuit, %d additions (dense: %d) */' % (name, ops, K * (K - 1)),
         '    float out[%d];' % K]
    v = lambda w: 'x[%d]' % w if w < K else 't%d' % w
    for t, u, w, s in defs:
        b.append('    float t%d = %s %s %s;' % (t, v(u), '+' if s > 0 else '-', v(w)))
    for i in range(K):
        terms = sorted(rows[i].items())
        e = ''.join((' + ' if c > 0 else ' - ') + v(w) for w, c in terms).strip()
        if e.startswith('+ '): e = e[2:]
        b.append('    out[%d] = %s;' % (i, e))
    b += ['    #pragma unroll', '    for (int i = 0; i < %d; i++) { x[i] = out[i]; }' % K, '}', '']
    hdr += b
open(outp, 'w').write('\n'.join(hdr) + '\n')
