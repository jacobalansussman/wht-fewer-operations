#!/usr/bin/env python3
"""r2_small.py (r-2): exact integer / fraction checks, no primes.
(1) tau = -1, 4 points: helper sets of 3 points with all coordinates in {0, 1, -1} (40 points of the rational projective space),
    decided by an exact fixpoint (integer 3 x 3 minors).  If the number is 228, every helper set found modulo p is the reduction
    of one of these rational sets.
(2) my own replay, with fractions, of p-0's three weight-only circuits and of the 5-gate circuit at several tau."""
import itertools
from fractions import Fraction as F
from math import comb
def col(a, b, c):
    for i, j, k in ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)):
        if a[i] * (b[j] * c[k] - b[k] * c[j]) - a[j] * (b[i] * c[k] - b[k] * c[i]) + a[k] * (b[i] * c[j] - b[j] * c[i]): return False
    return True
def norm(v):
    f = next(x for x in v if x); return tuple(x * f for x in v)          # entries 0, 1, -1: multiply by the sign of the first non-zero
pts = sorted(set(norm(v) for v in itertools.product((-1, 0, 1), repeat=4) if any(v)))
E = [tuple(int(i == j) for j in range(4)) for i in range(4)]
R = [norm(tuple((-1) ** bin(w & x).count('1') for x in range(4))) for w in range(4)]
cand = [q for q in pts if q not in E and q not in R]
def works(S):
    av = list(E); pend = list(S) + list(R); ch = True
    while pend and ch:
        ch = False
        for x in list(pend):
            if any(col(av[i], av[j], x) for i in range(len(av)) for j in range(i + 1, len(av))): av.append(x); pend.remove(x); ch = True
    return not pend
good = [S for S in itertools.combinations(cand, 3) if works(S)]
two = [S for S in itertools.combinations(cand, 2) if works(S)]
print('(1) tau = -1, exact over the rationals, points with coordinates 0, 1, -1: %d points, %d candidates' % (len(pts), len(cand)))
print('    sets of 2 helpers that work: %d;  sets of 3 helpers that work: %d;  of these with a helper of full support (a hub): %d' % (len(two), len(good), sum(1 for S in good if any(all(h) for h in S))))
def target(k, t): return [[sum(comb(i, m) * comb(k - i, j - m) * t ** m for m in range(0, min(i, j) + 1) if j - m <= k - i) for j in range(k + 1)] for i in range(k + 1)]
def replay(n, prog, T):
    val = {i: [F(int(i == j)) for j in range(n)] for i in range(n)}
    for name, a, u, b, v in prog: val[name] = [F(a) * x + F(b) * y for x, y in zip(val[u], val[v])]
    def prop(y, r): return any(y) and all(y[i] * r[j] == y[j] * r[i] for i in range(n) for j in range(n))
    return len(prog), all(prop(val['r%d' % i], T[i]) for i in range(n))
print('(2) weight-only circuits, my replay (gates, every output proportional to its row):')
for t in (F(3), F(2), F(1, 2), F(-2), F(5, 7), F(-1, 2), F(10), F(-1)):
    print('    k=2 tau=%s:' % t, replay(3, [('h1', 1, 0, 2, 1), ('h2', 1, 'h1', t, 2), ('r0', 1, 'h1', 1, 2), ('r1', 1, 'h2', t - 1, 1), ('r2', t, 'h2', 1 - t, 0)], target(2, t)))
print('    k=2 tau=-1, 4 gates:', replay(3, [('s', 1, 0, 1, 2), ('r1', 1, 0, -1, 2), ('r0', 1, 's', 2, 1), ('r2', 1, 's', -2, 1)], target(2, F(-1))))
print('    k=3 tau=-1, 7 gates:', replay(4, [('g4', 3, 1, 1, 3), ('g5', 1, 0, -1, 2), ('g6', 3, 'g5', -1, 'g4'), ('r0', 4, 0, -1, 'g6'), ('r2', 1, 'g6', 4, 3), ('r3', 1, 'r0', -2, 'g4'), ('r1', 1, 'r2', -6, 'g5')], target(3, F(-1))))
for k in (3, 4, 5):
    import itertools as it
    def minors2(T): return sum(1 for a, b in it.combinations(range(k + 1), 2) for c, d in it.combinations(range(k + 1), 2) if T[a][c] * T[b][d] == T[a][d] * T[b][c])
    print('    k=%d: zero entries and vanishing 2 x 2 minors of the block at tau = -1: %d, %d; at tau = 3: %d, %d; at tau = -2: %d, %d' % (k,
        sum(x == 0 for r in target(k, F(-1)) for x in r), minors2(target(k, F(-1))), sum(x == 0 for r in target(k, F(3)) for x in r), minors2(target(k, F(3))),
        sum(x == 0 for r in target(k, F(-2)) for x in r), minors2(target(k, F(-2)))))
