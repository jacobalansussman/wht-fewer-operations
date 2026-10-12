#!/usr/bin/env python3
# e-3-cutoff, experiment 5: the level picture.  Every function of the overlap is Z^T diag(D_j by level j=|S|) Z.
# leftover of window [a,a+d]: levels D'_j = (-2)^j - c_j (j<=d), (-2)^j (j>d).   Inverse: N*R^-1 = H + N*F, F a function of the union size u.
# Look at (i) the levels D'_j, (ii) N*F(u) against the lower-window leftover r_low,m(t) = sum_{i>m} (-2)^i C(t,i) for every m and shift.
from fractions import Fraction as Fr
from math import comb
def gbin(n, r):
    num = 1
    for q in range(r): num *= (n - q)
    f = 1
    for q in range(2, r + 1): f *= q
    return num // f
for k in (8, 10, 13):
    N = 1 << k
    for a in (1, 2, 3, 4, 5):
        for d in (2, 3, 4):
            if a + d > k: continue
            c = [(-1) ** a * sum((-2) ** i * gbin(-a, i - j) for i in range(j, d + 1)) for j in range(d + 1)]
            lev = [(-2) ** j - c[j] for j in range(d + 1)]
            if 0 in lev:
                print("k=%2d window [%d,%d]: levels %s  (singular)" % (k, a, a + d, lev)); continue
            dl = [Fr(1, lev[j]) - Fr(1, (-2) ** j) for j in range(d + 1)]
            NF = [N * sum(comb(k - u, j - u) * dl[j] for j in range(u, d + 1)) for u in range(d + 1)]
            hits = []
            for m in range(0, k):
                rl = lambda t: sum((-2) ** i * comb(t, i) for i in range(m + 1, t + 1)) if t >= 0 else None
                for sh in range(-3, 4):
                    for sg in (1, -1):
                        if all(k - u + sh >= 0 and NF[u] == sg * rl(k - u + sh) for u in range(d + 1)): hits.append((m, sh, sg))
            print("k=%2d window [%d,%d]: levels D'_j=%s   N*F(u)=%s   equals sign*r_low,m(k-u+shift) for (m,shift,sign) in %s" % (k, a, a + d, lev, [str(z) for z in NF], hits))
