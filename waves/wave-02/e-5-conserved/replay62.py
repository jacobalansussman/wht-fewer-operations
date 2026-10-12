# Exact replay (rationals, with sqrt2 handled as a pair a + b*sqrt2) of the pattern the annealer keeps finding at budget 62:
# seven sum-of-four gates and three butterflies = 62 operations, entropy exactly 62 of 64.  Built here by hand, not taken from the float run:
# the 64-program "eight sum-of-four gates" with ONE of its gates replaced by 3 butterflies cannot be flat; instead check the claim
# "62 operations make at most 62 bits with gates of 2 and 4 points" on the natural example: textbook with one butterfly left out (62 ops).
from fractions import Fraction as Fr
import math
N = 16
# entries are stored as squares' multiset is enough for the entropy: keep exact squares M_ij^2 as Fractions by tracking integer matrix and row scale.
M = [[Fr(int(i == j)) for j in range(N)] for i in range(N)]; scale2 = [Fr(1)] * N   # true row = M[row] / sqrt(scale2[row])
ops = 0; skipped = False
for b in range(4):
    for x in range(N):
        if not (x >> b) & 1:
            y = x | (1 << b)
            if b == 3 and x == 0 and not skipped: skipped = True; continue      # leave one butterfly out
            ra = [p + q for p, q in zip(M[x], M[y])]; rb = [p - q for p, q in zip(M[x], M[y])]
            assert scale2[x] == scale2[y]
            M[x], M[y] = ra, rb; scale2[x] *= 2; scale2[y] *= 2; ops += 2
phi = 0.0; exact_dyadic = True
for r in range(N):
    for v in M[r]:
        p = v * v / scale2[r]
        if p: phi -= float(p) * math.log2(float(p))
print("textbook with one butterfly left out: %d operations, entropy %.6f bits (exact squares are dyadic, so the value is exact: 62)" % (ops, phi))
