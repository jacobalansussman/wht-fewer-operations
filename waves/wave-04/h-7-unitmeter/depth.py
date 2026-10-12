#!/usr/bin/env python3
"""depth.py [h-7-unitmeter]  Where the guessed laws L1 and L2 must fail for the published program.  Floating point, rough.
Model [derived]: cost per point c(k) for arrays of 2^k points, c(k) = k (textbook) below k0, and one level of the unit
multiplies the rate rho = c(k)/k by (1 - delta) while k shrinks by e^-F  (delta = D/(W m), F = fragmentation, e2-2's law
saving = delta/F).  L1 needs  saved <= over-limit wires <= gates, so it fails at the latest when rho < 1/2.
L2: saved <= (1/2) sum over wires of log2(s s'/N); a wire inside d nested units has log2(s s'/N) <= sum over levels of
log2(t t'), so the budget per wire is at most d*B/2... (B = bits per level).  L2 fails when (1-delta)^-d - 1 > d*B/2."""
import math
D, W, m = 120, 1263, 45
delta = D / (W * m); F = 2.407; A = 19380
k0 = m * (A // D + 1)
print("delta = %.6e, F = %.3f, saving delta/F = %.4e, k0 = %d bits (first size where one level beats the textbook in count G)" % (delta, F, delta / F, k0))
d1 = math.log(2) / -math.log(1 - delta)
print("L1: rho < 1/2 after d = %.0f nested levels; log2 k = log2 k0 + d F / ln 2 = %.0f  (N = 2^k, k = 2^%.0f)" % (d1, math.log2(k0) + d1 * F / math.log(2), math.log2(k0) + d1 * F / math.log(2)))
for name, B in (("measured: 2 * mean log2 t = 2 * 78444/56715", 2 * 78444 / 56715), ("crude ceiling: 2 log2 W", 2 * math.log2(W))):
    d = 1
    while (1 - delta) ** (-d) - 1 <= d * B / 2:
        d += 1
    print("L2 with B = %.2f bits per level (%s): fails from d = %d levels; log2 k = %.0f" % (B, name, d, math.log2(k0) + d * F / math.log(2)))
# the exchange rate gamma = log2(1/rho) per mean bit of excess, for comparison
B = 2 * 78444 / 56715
print("published unit: log2(1/(1-delta)) / B = %.3e per bit of excess" % (-math.log2(1 - delta) / B))
for name, gates, k, N, ol_bits in (("brick, 4 points, 7 gates", 7, 2, 4, 2), ("staircase, 64 points, 304 gates", 304, 6, 64, 160)):
    rho = gates / (N * k)
    print("%s: rho = %.4f, mean excess = %.3f bits per wire, log2(1/rho)/mean = %.3f" % (name, rho, ol_bits / gates, -math.log2(rho) / (ol_bits / gates)))
