# u-7-quotient, run F: the contrast.  Exact integers.
# F1. E8: 120 lines (one root per line, roots doubled to be integer vectors in 8 coordinates).  For pairs of lines: is r_i - r_j or
#     r_i + r_j again a root?  How many pairs give each line (how often one difference is repeated).
# F2. 256 points: Q(x) = x1x2 + x3x4 + x5x6 + x7x8 on the 8 address bits, B(x,y) = Q(x+y)+Q(x)+Q(y).  S = {Q = 1}.
#     |S|, neighbours inside S, and the 120 x 120 block (-1)^B(s,s') : rank of (block - c I) modulo the prime 1000003 for c in a few values
#     (a rank modulo a prime is a lower bound for nothing and an upper bound for nothing in general; here the exact spectrum is known
#      from the strongly regular graph, the run is a check of the multiplicities; the block^2 identity below is exact).
import itertools
roots = set()
for a, b in itertools.combinations(range(8), 2):
    for sa in (2, -2):
        for sb in (2, -2):
            v = [0] * 8; v[a] = sa; v[b] = sb; roots.add(tuple(v))
for s in itertools.product((1, -1), repeat=8):
    if sum(1 for t in s if t < 0) % 2 == 0: roots.add(tuple(s))
assert len(roots) == 240
def norm(v):
    l = next(t for t in v if t); return v if l > 0 else tuple(-t for t in v)
lines = sorted({norm(r) for r in roots}); assert len(lines) == 120
idx = {l: i for i, l in enumerate(lines)}
cnt = [0] * 120; pairs = 0; hit = 0
for i in range(120):
    for j in range(i):
        pairs += 1
        for sg in (1, -1):
            d = tuple(a - sg * b for a, b in zip(lines[i], lines[j]))
            if d in roots: hit += 1; cnt[idx[norm(d)]] += 1
print('F1. E8: pairs of lines %d ; pairs whose sum or difference is a root: %d ; times each line occurs as such a sum or difference: min %d max %d' % (pairs, hit, min(cnt), max(cnt)))
print('     so 120 wires in 8 dimensions: %d differences fall on 120 values; in the transform circuits every difference is distinct' % hit)
Qf = lambda x: (x & 1) * (x >> 1 & 1) ^ (x >> 2 & 1) * (x >> 3 & 1) ^ (x >> 4 & 1) * (x >> 5 & 1) ^ (x >> 6 & 1) * (x >> 7 & 1)
S = [x for x in range(256) if Qf(x)]
Bf = lambda x, y: Qf(x ^ y) ^ Qf(x) ^ Qf(y)
nb = {sum(1 for t in S if t != s and Bf(s, t)) for s in S}
print('F2. 256 points: |S| = %d = (256 - 16)/2 ; neighbours of each point inside S: %s' % (len(S), sorted(nb)))
M = [[(-1) ** Bf(s, t) for t in S] for s in S]
# exact: (M - 8 I)(M + 16 I) = 0 ?   and trace
n = 120
M2 = [[sum(M[i][t] * M[t][j] for t in range(n)) for j in range(n)] for i in range(n)]
ok = all(M2[i][j] + 8 * M[i][j] - 128 * (i == j) == 0 for i in range(n) for j in range(n))
print('     block M = ((-1)^B(s,t)) on S x S: M^2 + 8 M - 128 I = 0 exactly: %s ; trace %d  => eigenvalue 8 with multiplicity %d, -16 with multiplicity %d' % (
    ok, sum(M[i][i] for i in range(n)), (120 * 16 + 120) // 24, 120 - (120 * 16 + 120) // 24))
print('     so M = 8 I - 24 P with P a projection of rank 35: a 120 x 120 block of the 256-point transform is a diagonal plus rank 35')
