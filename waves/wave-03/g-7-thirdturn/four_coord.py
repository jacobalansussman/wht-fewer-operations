#!/usr/bin/env python3
"""g-7-thirdturn / four_coord.py -- 4 points, exact: coordinate seeds x0..x3 with EVERY fixed form a*(x0+x1) + b*(x0+x2),
(a : b) of height up to 12.  For each: can all non-coordinate rows of B, and of B^-1, be made with no helper?
(count (G); 'no helper' is tested exactly: a row is added when it lies on a line through two available points)."""
import itertools
from math import gcd
from fractions import Fraction as F
S = [[1, 1, 1, 1], [1, 1, -1, -1], [1, -1, 1, -1], [1, -1, -1, 1]]; T = [1, 1, 1, -1]
R = [[F(T[p] * S[p][y], 2) for y in range(4)] for p in range(4)]
mul = lambda f: [sum(f[x] * R[x][y] for x in range(4)) for y in range(4)]
def inv(M):
    n = 4; A = [[F(v) for v in r] + [F(int(i == j)) for j in range(n)] for i, r in enumerate(M)]
    for c in range(n):
        p = next((i for i in range(c, n) if A[i][c] != 0), None)
        if p is None: return None
        A[c], A[p] = A[p], A[c]; pv = A[c][c]; A[c] = [v / pv for v in A[c]]
        for i in range(n):
            if i != c and A[i][c] != 0:
                f = A[i][c]; A[i] = [x - f * y for x, y in zip(A[i], A[c])]
    return [r[n:] for r in A]
def prim(v):
    nz = next(x for x in v if x != 0); return tuple(F(x) / nz for x in v)
def rank3(u, v, t):
    M = [list(u), list(v), list(t)]; r = 0
    for c in range(4):
        p = next((i for i in range(r, 3) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        for i in range(3):
            if i != r and M[i][c] != 0:
                f = M[i][c] / M[r][c]; M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        r += 1
        if r == 3: break
    return r
def nohelper(rows):
    avail = {tuple(F(int(i == k)) for k in range(4)) for i in range(4)}
    todo = {prim(r) for r in rows} - avail; need = len(todo); ch = True
    while ch and todo:
        ch = False
        for t in list(todo):
            if any(rank3(u, v, t) == 2 for u, v in itertools.combinations(list(avail), 2)):
                avail.add(t); todo.discard(t); ch = True
    return need, not todo
res = {}; cnt = 0
for i in range(4):
    f = [F(int(k == i)) for k in range(4)]; f1 = mul(f); f2 = mul(f1)
    for a in range(-12, 13):
        for b in range(-12, 13):
            if (a, b) == (0, 0) or gcd(abs(a), abs(b)) != 1 or (a < 0 or (a == 0 and b < 0)): continue
            f0 = [F(a + b), F(a), F(b), F(0)]
            B = [f, f1, f2, f0]; Bi = inv(B)
            if Bi is None: continue
            cnt += 1
            n1, ok1 = nohelper(B); n2, ok2 = nohelper(Bi)
            lb = (n1 if ok1 else n1 + 1) + (n2 if ok2 else n2 + 1)
            res.setdefault((i, lb, ok1 and ok2), []).append((a, b))
print("coordinate seeds, %d bases.  (seed, lower bound on cost(B)+cost(B^-1), is the bound reached with no helper) -> number, examples" % cnt)
for k in sorted(res): print("  ", k, len(res[k]), res[k][:4])
print("least lower bound:", min(k[1] for k in res))
