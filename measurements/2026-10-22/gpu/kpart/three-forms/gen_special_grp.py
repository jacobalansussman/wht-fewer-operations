"""gen_special_grp.py CODE_GEN_PY OUT_H -- ay-h0: drop-in fast_hadamard_transform_special.h for Dao's
fast-hadamard-transform with hadamard_mult_thread_{12,20,28,40} as the KNOWN structured form (groups of 4 inputs:
all 8 signed sums per group, 12 adds; each output = +- one prepared sum per group), SAME matrices as Dao
(had_12_paley, had_20_will, had_28_will, had_40_tpal).  Proven on all unit vectors before writing."""
import re, sys
src = open(sys.argv[1]).read(); outp = sys.argv[2]
mats = {}
for name, body in re.findall(r'(had_\w+)\s*=\s*"""(.*?)"""', src, re.S):
    rows = [r.strip() for r in body.strip().splitlines() if r.strip()]
    mats[name] = [[1 if ch == '+' else -1 for ch in r] for r in rows]
nm = lambda e: 'p' if e > 0 else 'm'
hdr = ['', '#pragma once', '']
for name in ('had_12_paley', 'had_20_will', 'had_28_will', 'had_40_tpal'):
    M = mats[name]; K = len(M); G = K // 4
    terms = [[(M[i][4*g], g, M[i][4*g+1]*M[i][4*g], M[i][4*g+2]*M[i][4*g], M[i][4*g+3]*M[i][4*g]) for g in range(G)] for i in range(K)]
    for j in range(K):                                   # proof on unit vectors
        x = [1 if q == j else 0 for q in range(K)]
        for i in range(K):
            v = sum(s * (x[4*g] + e1*x[4*g+1] + e2*x[4*g+2] + e3*x[4*g+3]) for s, g, e1, e2, e3 in terms[i])
            assert v == M[i][j], (name, i, j)
    adds = G * 12 + K * (G - 1)
    print('%s: grouped(4) %d additions (dense %d), proof on unit vectors PASS' % (name, adds, K * (K - 1)))
    b = ['__device__ __forceinline__ void hadamard_mult_thread_%d(float x[%d]) {' % (K, K),
         '    /* %s: groups of 4, %d additions (dense: %d) */' % (name, adds, K * (K - 1)), '    float out[%d];' % K]
    for g in range(G):
        b.append('    float a%dp = x[%d] + x[%d], a%dm = x[%d] - x[%d], b%dp = x[%d] + x[%d], b%dm = x[%d] - x[%d];' % (
            g, 4*g, 4*g+1, g, 4*g, 4*g+1, g, 4*g+2, 4*g+3, g, 4*g+2, 4*g+3))
        for e1 in (1, -1):
            for e2 in (1, -1):
                for e3 in (1, -1):
                    b.append('    float s%d_%s%s%s = a%d%s %s b%d%s;' % (g, nm(e1), nm(e2), nm(e3), g, nm(e1), '+' if e2 > 0 else '-', g, nm(e2 * e3)))
    for i in range(K):
        e = ''
        for k, (s, g, e1, e2, e3) in enumerate(terms[i]):
            v = 's%d_%s%s%s' % (g, nm(e1), nm(e2), nm(e3))
            e += (('' if s > 0 else '-') if k == 0 else (' + ' if s > 0 else ' - ')) + v
        b.append('    out[%d] = %s;' % (i, e))
    b += ['    #pragma unroll', '    for (int i = 0; i < %d; i++) { x[i] = out[i]; }' % K, '}', '']
    hdr += b
open(outp, 'w').write('\n'.join(hdr) + '\n')
