#!/usr/bin/env python3
"""g-7-thirdturn / equiang.py -- exact, N = 4, 16, 64.  P = (I + R + R^2)/3 is the projector onto the fixed space U of R.
Row x of P is the fixed part of the coordinate x.  Look at the Gram matrix of these fixed parts (it is P itself):
split the addresses by Q0 = 0 / Q0 = 1 and report rank, diagonal entry, off-diagonal entries and the cosine of the angle."""
from fractions import Fraction as F
pc = lambda x: bin(x).count("1")
def rank(M):
    M = [list(r) for r in M]; r = 0
    if not M: return 0
    for c in range(len(M[0])):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]; pv = M[r][c]; M[r] = [v / pv for v in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]; M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        r += 1
        if r == len(M): break
    return r
for j in (1, 2, 3):
    N = 1 << (2 * j); lo = (1 << j) - 1
    w = lambda p, y: (pc((p >> j) & (y & lo)) + pc((p & lo) & (y >> j))) & 1
    Q0 = lambda x: pc((x >> j) & (x & lo)) & 1
    R = [[F((-1) ** (Q0(p) ^ w(p, y)), 1 << j) for y in range(N)] for p in range(N)]
    R2 = [[sum(R[a][t] * R[t][b] for t in range(N)) for b in range(N)] for a in range(N)]
    P = [[(F(int(a == b)) + R[a][b] + R2[a][b]) / 3 for b in range(N)] for a in range(N)]
    for val in (0, 1):
        pts = [x for x in range(N) if Q0(x) == val]
        G = [[P[a][b] for b in pts] for a in pts]
        diag = sorted({G[i][i] for i in range(len(pts))}); off = sorted({abs(G[i][k]) for i in range(len(pts)) for k in range(len(pts)) if i != k})
        mixed = sorted({P[a][b] for a in pts for b in range(N) if Q0(b) != val})
        cos = [str(o / diag[0]) for o in off] if diag[0] != 0 else ["-"]
        print("N=%d, addresses with Q0 = %d: %d fixed parts spanning dimension %d; squared length %s; |inner products| %s; cosine %s; inner products with the other class: %s" % (
            N, val, len(pts), rank(G), [str(d) for d in diag], [str(o) for o in off], cos, [str(m) for m in mixed]), flush=True)
