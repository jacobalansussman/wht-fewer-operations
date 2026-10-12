#!/usr/bin/env python3
"""d-4-codes play 3 (exact fractions): the 'one third is free' subspaces.
For each quadratic form Q_a = Q0 + w(a,.), T_a = diag((-1)^Q_a), g_a = T_a S / sqrt(N).
 1. g_a^3 = e_a I with e_a = +1 (hyperbolic) or -1 (elliptic)?
 2. U_a = {x : S x = e_a sqrt(N) T_a x}; projector P_a = (I + e_a g_a + g_a^2)/3; its rank = (N+2)/3 ?
 3. Is sum_a e_a T_a P_a a multiple of S/sqrt(N)?  (the transform as a sum of free sign changes on thirds of the space)
 4. At N=16: is U_0 spanned by indicators of totally singular lines (Q0 = 0 on the line) plus one vector on {Q0 = 1}?
"""
from fractions import Fraction as F
pc = lambda x: bin(x).count("1")
def rank(M):
    M = [[F(v) for v in r] for r in M]; r = 0
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
def run(j):
    k = 2 * j; N = 1 << k; r = 1 << j; lo = r - 1
    w = lambda p, y: (pc((p >> j) & (y & lo)) + pc((p & lo) & (y >> j))) & 1
    Q0 = lambda x: pc((x >> j) & (x & lo)) & 1
    S = [[F(-1 if w(p, y) else 1, r) for y in range(N)] for p in range(N)]      # S / sqrt(N), orthogonal
    I = [[F(int(p == y)) for y in range(N)] for p in range(N)]
    mm = lambda A, B: [[sum(A[i][t] * B[t][q] for t in range(N)) for q in range(N)] for i in range(N)]
    tot = [[F(0)] * N for _ in range(N)]; ranks = set(); eps = {}
    P0 = None
    for a in range(N):
        T = [(-1) ** (Q0(x) ^ w(a, x)) for x in range(N)]
        g = [[T[p] * S[p][y] for y in range(N)] for p in range(N)]
        g2 = mm(g, g); g3 = mm(g2, g)
        e = 1 if g3 == I else (-1 if g3 == [[-v for v in row] for row in I] else None)
        assert e is not None
        eps[a] = e
        P = [[(I[p][y] + e * g[p][y] + g2[p][y]) / 3 for y in range(N)] for p in range(N)]
        assert mm(P, P) == P
        ranks.add(sum(P[p][p] for p in range(N)))
        # S P == e T P
        SP = mm(S, P); assert SP == [[e * T[p] * P[p][y] for y in range(N)] for p in range(N)]
        for p in range(N):
            for y in range(N): tot[p][y] += e * T[p] * P[p][y]
        if a == 0: P0 = P
    ratio = {tot[p][y] / S[p][y] for p in range(N) for y in range(N)}
    print("N=%3d: g_a^3 = +I for %d forms, -I for %d;  e_a = +1 exactly for hyperbolic: %s; rank of every P_a: %s (N+2)/3 = %s;  S P_a = e_a T_a P_a: True" % (
        N, sum(1 for v in eps.values() if v == 1), sum(1 for v in eps.values() if v == -1),
        all((eps[a] == 1) == (Q0(a) == 0) for a in eps), sorted(ranks), F(N + 2, 3)))
    print("       sum_a e_a T_a P_a = c * S/sqrtN with c in", sorted(ratio), " (predicted (N+2)/3 = %s)" % F(N + 2, 3))
    if N == 16:
        sing = [x for x in range(N) if Q0(x) == 0]
        lines = []
        for x in sing:
            for y in sing:
                if 0 < x < y and Q0(x ^ y) == 0 and w(x, y) == 0:
                    L = tuple(sorted({0, x, y, x ^ y}))
                    if L not in lines: lines.append(L)
        ind = [[1 if x in L else 0 for x in range(N)] for L in lines]
        inU = all([sum(P0[p][y] * v[y] for y in range(N)) for p in range(N)] == v for v in ind)
        print("       totally singular lines:", len(lines), " their indicators lie in U_0:", inU, " rank:", rank(ind))
        # the part of U_0 supported on Q0 = 1
        ell = [x for x in range(N) if Q0(x) == 1]
        # vectors supported on ell fixed by P0: solve (P0 - I) restricted
        M = [[P0[p][y] - I[p][y] for y in ell] for p in range(N)]
        print("       points with Q0 = 1: %d ; dimension of U_0 inside the vectors supported there: %d" % (len(ell), len(ell) - rank(M)))
        print("       rank of P_0:", rank(P0), " P_0 distinct entries:", sorted({v for row in P0 for v in row}))
for j in (1, 2): run(j)
