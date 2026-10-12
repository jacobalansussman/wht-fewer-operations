#!/usr/bin/env python3
"""rescale.py [ad-4-flatrank]  Free sign changes of rows and columns (free in count (G)) change the flat rank in the doubled class.
Whole numbers.  (1) 4 points: with row signs a = (+,+,+,-) and column signs b = (+,+,+,-), a(x) H(x,y) b(y) = 1 - 2 [y = swap(x) + 11]:
the constant and ONE flat (a permutation matrix): 2 flats, total rank 1 + 4 = 5.  (2) 16 points: the tensor square: 4 flats, total rank 25.
(3) the rank of the quadratic form x.y + alpha(x) + beta(y) for all quadratic alpha, beta at k = 2, 3, 4 (least value)."""
import itertools
def wt(x): return bin(x).count("1")
k = 2; N = 4
a = [(-1) ** ((x & 1) & (x >> 1)) for x in range(N)]
M = [[a[x] * (-1) ** wt(x & y) * a[y] for y in range(N)] for x in range(N)]
def swap(x): return ((x & 1) << 1) | (x >> 1)
P = [[1 if y == (swap(x) ^ 3) else 0 for y in range(N)] for x in range(N)]
print("(1) 4 points: a H b = J - 2 P with P the permutation y = swap(x) + 11 :", all(M[x][y] == 1 - 2 * P[x][y] for x in range(N) for y in range(N)), "; rows of a H b:", M)
N2 = 16
a2 = [a[x & 3] * a[x >> 2] for x in range(N2)]
M2 = [[a2[x] * (-1) ** wt(x & y) * a2[y] for y in range(N2)] for x in range(N2)]
def p4(x, y): return P[x][y]
ok = all(M2[x][y] == 1 - 2 * p4(x & 3, y & 3) - 2 * p4(x >> 2, y >> 2) + 4 * p4(x & 3, y & 3) * p4(x >> 2, y >> 2) for x in range(N2) for y in range(N2))
print("(2) 16 points: a H b = J - 2 [low pair matched] - 2 [high pair matched] + 4 [both matched] :", ok, " : 4 flats of the doubled space (dimensions 8, 6, 6, 4; ranks 1, 4, 4, 16; total rank 25)")
# (3) least rank of the polar form [[A, I], [I, C]] over alternating A, C
def rank(rows, n):
    rows = list(rows); rk = 0
    for c in range(n):
        p = next((i for i in range(rk, len(rows)) if (rows[i] >> c) & 1), None)
        if p is None: continue
        rows[rk], rows[p] = rows[p], rows[rk]
        for i in range(len(rows)):
            if i != rk and (rows[i] >> c) & 1: rows[i] ^= rows[rk]
        rk += 1
    return rk
for k in (2, 3, 4):
    pairs = [(i, j) for i in range(k) for j in range(i + 1, k)]
    alts = []
    for bits in range(1 << len(pairs)):
        S = [0] * k
        for t, (i, j) in enumerate(pairs):
            if (bits >> t) & 1: S[i] |= 1 << j; S[j] |= 1 << i
        alts.append(S)
    best = 2 * k; cnt = {}
    for A in alts:
        for C in alts:
            rows = [A[i] | (1 << (k + i)) for i in range(k)] + [(1 << i) | (C[i] << k) for i in range(k)]
            r = rank(rows, 2 * k); cnt[r] = cnt.get(r, 0) + 1; best = min(best, r)
    print("(3) k=%d: rank of x.y + alpha(x) + beta(y) over all %d pairs of quadratic alpha, beta: %s ; least %d (plain transform: %d)" % (k, len(alts) ** 2, sorted(cnt.items()), best, 2 * k))
