# p-1-letter16: the row-pair / column-pair lower bound of lb.py evaluated on actual sign designs at 16 points (standard dual chains).
#   B(r,c) = sum over row pairs of t'(difference of the two rows, along the column tree)
#          + sum over column pairs of t'(difference of the two columns, along the row tree)   <=  tau of any letter with these signs.
# Exact (fractions).  Column tree = cosets of <8> < <8,4> < <8,4,2>: aligned intervals after reversing the 4 bits of x.
import random, sys
from fractions import Fraction as F
from functools import lru_cache
N = 16
def par(a): return bin(a).count('1') & 1
rev = [int(format(x, '04b')[::-1], 2) for x in range(N)]
def tprime(f):
    f = tuple(f)
    @lru_cache(None)
    def g(lo, hi, off):
        if hi - lo == 1: return F(0) if f[lo] == off else F(1, 2)
        mid = (lo + hi) // 2
        return min((F(0) if o2 == off else F(1)) + g(lo, mid, o2) + g(mid, hi, o2) for o2 in (0, 2, -2))
    return g(0, N, 0)
cache = {}
def tp(f):
    f = tuple(f)
    if f not in cache: cache[f] = tprime(f)
    return cache[f]
def B(r, c):
    M = [[r[y] * c[x] * (-1) ** par(y & x) for x in range(N)] for y in range(N)]
    rows = sum(tp([M[y][rev[p]] - M[y ^ 1][rev[p]] for p in range(N)]) for y in range(0, N, 2))
    cols = sum(tp([M[y][x] - M[y][x ^ 8] for y in range(N)]) for x in range(8))
    return rows, cols
def q(f): return [(-1) ** f(x) for x in range(N)]
b = lambda x, i: x >> i & 1
named = {'45-design': (q(lambda y: b(y, 0) & (1 ^ b(y, 3))), q(lambda x: b(x, 0) & b(x, 3))),
         'bent x0x3+x1x2 both sides': (q(lambda x: b(x, 0) & b(x, 3) ^ b(x, 1) & b(x, 2)),) * 2,
         'bent x0x1+x2x3 both sides': (q(lambda x: b(x, 0) & b(x, 1) ^ b(x, 2) & b(x, 3)),) * 2,
         'all ones': ([1] * N, [1] * N)}
for nm, (r, c) in named.items():
    rw, cl = B(r, c); print(nm, ": rows", rw, " columns", cl, " bound on tau", rw + cl)
random.seed(11); best = None; hist = {}
def rq():
    mons = [m for m in range(1, N) if bin(m).count('1') <= 2]; ch = [m for m in mons if random.random() < 0.5]
    return [(-1) ** (sum(1 for m in ch if (x & m) == m) & 1) for x in range(N)]
import time; t0 = time.time(); cnt = 0
while time.time() - t0 < 150:
    r, c = (rq(), rq()) if cnt % 2 else ([random.choice([1, -1]) for _ in range(N)], [random.choice([1, -1]) for _ in range(N)])
    rw, cl = B(r, c); v = rw + cl; cnt += 1; hist[v] = hist.get(v, 0) + 1
    if best is None or v < best[0]: best = (v, r, c, rw, cl)
print("random designs (half quadratic, half arbitrary signs):", cnt, " smallest bound seen:", best[0], "(rows", best[3], "columns", best[4], ")  r", best[1], " c", best[2])
print("smallest values and counts:", sorted(hist.items())[:8])
