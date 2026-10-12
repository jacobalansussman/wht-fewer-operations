#!/usr/bin/env python3
"""g-7-thirdturn / eval64.py -- 64 points, exact integers: the pair-sharing count (count (G), upper bound, no helper wires)
of two bases B of the brief's kind and of their inverses: (1) the half transform, (2) the tensor cube of the 4-point chain
basis (x0; x0+x1+x2+x3; x0+x1+x2-x3; x0+x1).  Also checks B R = (relabelling) B for both, exactly."""
import sys
from fractions import Fraction as F
from math import gcd
import search16 as s
pc = s.pc
def run(j):
    N = 1 << (2 * j); lo = (1 << j) - 1; r = 1 << j
    w = lambda p, y: (pc((p >> j) & (y & lo)) + pc((p & lo) & (y >> j))) & 1
    Q0 = lambda x: pc((x >> j) & (x & lo)) & 1
    S = [[-1 if w(p, y) else 1 for y in range(N)] for p in range(N)]; T = [(-1) ** Q0(x) for x in range(N)]
    def Rm(f):
        ft = [f[x] * T[x] for x in range(N)]
        return s.prim([sum(ft[x] * S[x][y] for x in range(N) if ft[x]) for y in range(N)])
    half = [s.prim([((-1) ** pc(a & (y >> j))) if (y & lo) == b else 0 for y in range(N)]) for a in range(r) for b in range(r)]
    B4 = [[1, 0, 0, 0], [1, 1, 1, 1], [1, 1, 1, -1], [1, 1, 0, 0]]
    dig = lambda y: [(((y >> (j + i)) & 1) << 1) | ((y >> i) & 1) for i in range(j)]
    import itertools
    chain = []
    for idx in itertools.product(range(4), repeat=j):
        row = []
        for y in range(N):
            v = 1
            for a, d in zip(idx, dig(y)): v *= B4[a][d]
            row.append(v)
        chain.append(s.prim(row))
    def inv(M):
        n = len(M); A = [[F(v) for v in r_] + [F(int(i == k)) for k in range(n)] for i, r_ in enumerate(M)]
        for c in range(n):
            p = next(i for i in range(c, n) if A[c if False else i][c] != 0)
            A[c], A[p] = A[p], A[c]; pv = A[c][c]; A[c] = [v / pv for v in A[c]]
            for i in range(n):
                if i != c and A[i][c] != 0:
                    f = A[i][c]; A[i] = [x - f * y for x, y in zip(A[i], A[c])]
        out = []
        for r_ in A:
            r_ = r_[n:]; den = 1
            for v in r_: den = den * v.denominator // gcd(den, v.denominator)
            out.append(s.prim([int(v * den) for v in r_]))
        return out
    for name, B in (("half transform", half), ("chain (tensor power of the 4-point chain)", chain)):
        st = set(B); closed = all(Rm(f) in st for f in B)
        nxt = {f: Rm(f) for f in B}; fixed = sum(1 for f in B if nxt[f] == f)
        cB = s.cse(B)[0]; Bi = inv(B); cI = s.cse(Bi)[0]
        print("N=%d %s: rows closed under R: %s (fixed %d, three-cycles %d); non-zeros of B %d, of B^-1 %d; pair-sharing count of B %d (per form %.2f), of B^-1 %d; sum %d; N log2 N = %d" % (
            N, name, closed, fixed, (N - fixed) // 3, sum(1 for r_ in B for x in r_ if x), sum(1 for r_ in Bi for x in r_ if x), cB, cB / N, cI, cB + cI, N * 2 * j), flush=True)
for j in (1, 2, 3): run(j)
