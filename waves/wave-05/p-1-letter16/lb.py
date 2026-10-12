# p-1-letter16: a lower bound for ONE letter on the dual chains with SIGN scalings (any numbers on the rectangles), exact arithmetic.
# Row pair {y, y+v}: the difference of its two rows of M is 0 on one half of the columns and 2 M(y,.) on the other half, and only
# rectangles whose row set is a single row of the pair can produce it.  So  #(single-row rectangles in that pair) >= sparsity of the
# sign vector  c * chi_y  on a half, written as a sum of column-tree nodes.  Single cells are shared with the column count: weight 1/2.
#   tau >= sum over row pairs of t'(c chi_y on its half) + sum over column pairs of t'(r chi_x on its half)  >=  2 L(n),  n = N/2.
# t'(f) = min over ways to write f as a sum of numbers on tree nodes of (#nodes of 2 or more points) + (1/2)(#single points).
# L(n) = min over the two halves c0, c1 of  sum over the n characters chi of min(t'(c0 chi), t'(c1 chi)).   Exhaustive.
import itertools, sys
from fractions import Fraction as F
from functools import lru_cache
def tprime(f):
    n = len(f)
    @lru_cache(None)
    def g(lo, hi, off):                 # cost to make f[lo:hi] given the ancestors already contribute 'off'
        if hi - lo == 1: return F(0) if f[lo] == off else F(1, 2)
        mid = (lo + hi) // 2; best = None
        for o2 in (0, 1, -1):           # optimal partial sums can be taken among the values of f and 0 (the zero outside)
            cst = (F(0) if o2 == off else F(1)) + g(lo, mid, o2) + g(mid, hi, o2)
            if best is None or cst < best: best = cst
        return best
    return g(0, n, 0)
for k in (1, 2, 3):
    n = 1 << k; chars = [tuple((-1) ** bin(a & x).count('1') for x in range(n)) for a in range(n)]
    tab = {}
    for f in itertools.product([1, -1], repeat=n): tab[f] = tprime(f)
    prof = {}
    for c in itertools.product([1, -1], repeat=n - 1):
        c = (1,) + c; prof[c] = tuple(tab[tuple(p * q for p, q in zip(c, ch))] for ch in chars)
    plist = sorted(set(prof.values()))
    best = None
    for p0 in plist:
        for p1 in plist:
            s = sum(min(a, b) for a, b in zip(p0, p1))
            if best is None or s < best[0]: best = (s, p0, p1)
    one = min(sum(p) for p in plist)
    print("half of n =", n, "points (N =", 2 * n, "):  L(n) =", best[0], "  so tau >= 2 L =", 2 * best[0], "  gates >= N - 2 + 2L =", 2 * n - 2 + 2 * best[0],
          "   [one half only, no choice: min sum =", one, "]", "  distinct profiles:", len(plist))
    print("     profiles at the minimum:", [str(v) for v in best[1]], [str(v) for v in best[2]])
    sys.stdout.flush()
