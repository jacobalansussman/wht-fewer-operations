#!/usr/bin/env python3
"""g-7-thirdturn / turned16.py -- 16 points, exact.  The 'turned part' W = forms f with f + fR + fR^2 = 0 (at 4 points the
coordinate x3 is such a form and its identity is the 7-gate brick).  Sparsest forms of W at 16 points, and the number of
non-zeros of their images fR (the third member is -f - fR)."""
import itertools
from fractions import Fraction as F
import search16 as s
n = 16
R = [[F(s.T[p] * s.S[p][y], 4) for y in range(n)] for p in range(n)]
mul = lambda f: [sum(f[x] * R[x][y] for x in range(n) if f[x] != 0) for y in range(n)]
I = [[F(int(a == b)) for b in range(n)] for a in range(n)]
R2 = [mul(r) for r in R]
P = [[(I[a][b] + R[a][b] + R2[a][b]) / 3 for b in range(n)] for a in range(n)]      # row a = fixed part of e_a
def nullvec(rows):          # rows: list of vectors (the fixed parts of the chosen coordinates); find c with sum c_i rows_i = 0
    k = len(rows); M = [[rows[i][c] for i in range(k)] for c in range(n)]; piv = []; r = 0
    for c in range(k):
        p = next((i for i in range(r, n) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]; pv = M[r][c]; M[r] = [v / pv for v in M[r]]
        for i in range(n):
            if i != r and M[i][c] != 0:
                f = M[i][c]; M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        piv.append(c); r += 1
    free = [c for c in range(k) if c not in piv]
    if len(free) != 1: return None if not free else "many"
    fc = free[0]; x = [F(0)] * k; x[fc] = F(1)
    for i, c in enumerate(piv): x[c] = -M[i][fc]
    return x
for size in range(1, 7):
    found = {}
    for sup in itertools.combinations(range(n), size):
        x = nullvec([P[a] for a in sup])
        if x is None or x == "many" or any(v == 0 for v in x): continue
        f = [F(0)] * n
        for a, v in zip(sup, x): f[a] = v
        f1 = mul(f); w1 = sum(1 for v in f1 if v != 0); f2 = [-a - b for a, b in zip(f, f1)]; w2 = sum(1 for v in f2 if v != 0)
        key = (size,) + tuple(sorted((w1, w2))); found.setdefault(key, []).append((sup, [str(v) for v in x]))
    print("support size %d: forms in the turned part: %d ; (size, non-zeros of the other two members) -> count, example" % (size, sum(len(v) for v in found.values())))
    for k in sorted(found): print("    ", k, len(found[k]), found[k][0])
    if found and size >= 4: break
