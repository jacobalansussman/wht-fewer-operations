#!/usr/bin/env python3
"""h3_rate.py [aa-cross]  FLOATS, WHAT-IF.  The engine's price law, sum over the blocks of an array of (rank/m)^z = 1,
for the shape ab-1 found best: one big block of rank m - s - d and s blocks of rank 1 (d = moves saved per array)."""
import math
def need_d(m, s, e):
    z = 1 - e; t = 1 - s * m ** (-z)
    return None if t <= 0 else m - s - m * t ** (1 / z)
def saving(m, s, d):
    lo, hi = 0.0, 1.0
    f = lambda e: ((m - s - d) / m) ** (1 - e) + s * m ** (-(1 - e))
    if f(0.0) >= 1: return 0.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(mid) < 1: lo = mid
        else: hi = mid
    return lo
print("closed form to first order in s/m^z : d/s = m^e/(1-e) - 1   (e = saving, s = blocks of rank 1 per array, d = moves saved per array)")
for e in (0.01, 0.05, 0.1, 0.2, 0.5):
    print("  saving %.2f : moves to save per extra block, m = 4, 9, 45, 110, 1000 : " % e + "  ".join("%.3f" % (m ** e / (1 - e) - 1) for m in (4, 9, 45, 110, 1000)))
print("exact d needed for saving 0.1 at m = 45 with s single blocks:")
print("  " + "  ".join("s=%d: %.3f" % (s, need_d(45, s, 0.1)) for s in (1, 2, 3, 5, 8, 12, 15)))
print("ab-1's table (s = 1, saving 0.1): " + "  ".join("m=%d: %.3f" % (m, need_d(m, 1, 0.1)) for m in (4, 9, 45, 110)))
print("the published unit as ab-1 and x-6 quote it (d = 0.095 moves per array, 16.5 blocks per array, m = 45) IF its blocks were one big block and 15.5 singles:")
print("  d/s = %.4f ; saving by the law for that shape %.3e ; first-order formula d/(s (ln m + 1)) = %.3e ; published 8.7625e-4" % (0.095 / 15.5, saving(45, 15.5, 0.095), 0.095 / (15.5 * (math.log(45) + 1))))
print("the same d = 0.095 in fewer blocks: " + "  ".join("s=%g: %.4f" % (s, saving(45, s, 0.095)) for s in (1, 2, 4, 8, 15.5)))
print("linear size in this law: z -> 0 needs sum of (rank/m)^0 = number of blocks = 1, i.e. one block per array of rank < m; with 2 blocks z > 0 always:")
for rho in (0.5, 0.9, 0.99):
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if 2 * (1 - rho) ** mid > 1: lo = mid
        else: hi = mid
    print("  two equal blocks, share skipped %.2f : z = %.4f" % (rho, lo))
