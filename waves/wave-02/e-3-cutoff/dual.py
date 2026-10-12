#!/usr/bin/env python3
# e-3-cutoff, experiment 4: the leftover R = H - (cut-off form, centred window) is zero on the window pairs;
# claim [derived]: N * R^-1 = H + N*F with F nonzero only on pairs whose UNION has at most d elements (a tiny corner),
#   F[x,y] = (-1)^(|x|+|y|) * sum over S containing x|y, |S|<=d of ( 1/((-2)^|S| - c_|S|) - 1/(-2)^|S| ).
# Exact rationals.  k=6: R inverted outright by Gauss elimination over Q.  k=8: R*(H/N+F) = I checked on every row.
from fractions import Fraction as Fr
from math import comb
import sys
wt = lambda v: bin(v).count("1")
def gbin(n, r):
    num = 1
    for q in range(r): num *= (n - q)
    f = 1
    for q in range(2, r + 1): f *= q
    return num // f
def inv(M):
    n = len(M); A = [[Fr(x) for x in row] + [Fr(int(i == j)) for j in range(n)] for i, row in enumerate(M)]
    for c in range(n):
        p = next(i for i in range(c, n) if A[i][c] != 0); A[c], A[p] = A[p], A[c]
        iv = 1 / A[c][c]; A[c] = [x * iv for x in A[c]]
        for i in range(n):
            if i != c and A[i][c] != 0:
                f = A[i][c]; A[i] = [x - f * y for x, y in zip(A[i], A[c])]
    return [row[n:] for row in A]
for k, cases in ((6, ((1, 2), (1, 3), (2, 2))), (8, ((1, 2), (1, 3), (1, 4)))):
    N = 1 << k
    H = [[(-1) ** wt(x & y) for y in range(N)] for x in range(N)]
    for a, d in cases:
        c = [(-1) ** a * sum((-2) ** i * gbin(-a, i - j) for i in range(j, d + 1)) for j in range(d + 1)]
        pv = [sum(c[j] * comb(t, j) for j in range(d + 1)) for t in range(k + 1)]
        r = [(-1) ** t - pv[t] for t in range(k + 1)]
        R = [[r[wt(x & y)] for y in range(N)] for x in range(N)]
        zeros = sum(row.count(0) for row in R)
        sing = [j for j in range(d + 1) if c[j] == (-2) ** j]
        if sing:
            print('k=%d window [%d,%d]: level(s) %s have c_j = (-2)^j, so the leftover is singular (rank N - %d); skipped' % (k, a, a + d, sing, sum(comb(k, j) for j in sing))); continue
        dl = [Fr(1, (-2) ** j - c[j]) - Fr(1, (-2) ** j) for j in range(d + 1)]            # level j <= d
        fu = [sum(comb(k - u, j - u) * dl[j] for j in range(u, d + 1)) for u in range(d + 1)]   # as a function of the union size u
        Fm = {}
        for x in range(N):
            for y in range(N):
                u = wt(x | y)
                if u <= d and fu[u] != 0: Fm[(x, y)] = (-1) ** (wt(x) + wt(y)) * fu[u]
        if k == 6:
            Ri = inv(R)
            diff = {(x, y): Ri[x][y] - Fr(H[x][y], N) for x in range(N) for y in range(N) if Ri[x][y] != Fr(H[x][y], N)}
            ok = diff == Fm
        else:
            # R * (H/N + F) = I ; R*H is a function of ... just do it: R*H by integer products, R*F sparse
            ok = True
            cols = {}
            for (x, y), val in Fm.items(): cols.setdefault(y, []).append((x, val))
            for x in range(N):
                Rx = R[x]
                for y in range(N):
                    s = Fr(sum(p * q for p, q in zip(Rx, H[y])), N) + sum(Rx[z] * val for z, val in cols.get(y, ()))
                    if s != (1 if x == y else 0): ok = False; break
                if not ok: break
        print("k=%d window [%d,%d]: R has %d zero entries of %d (%.1f%%);  N*R^-1 = H + N*F with F on %d entries (pairs with union <= %d): %s ;  N*F as a function of union size: %s"
              % (k, a, a + d, zeros, N * N, 100 * zeros / N / N, len(Fm), d, ok, [str(N * z) for z in fu]))
        sys.stdout.flush()
