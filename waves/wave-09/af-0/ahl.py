#!/usr/bin/env python3
"""af-0/ahl.py  The stripped form of the class bound, in fractions.  A good pair on N points with C classes gives, after
stripping hanging edges, a graph with E <= N edges, all degrees >= 2, girth >= 8 and E - V >= N - C.
Alon-Hoory-Linial (2002): such a graph has V >= 2 (1 + (d-1) + (d-1)^2 + (d-1)^3), d = 2E/V.
For each N: the largest excess x = E - V that the theorem allows with E <= N; then classes >= N - x."""
from fractions import Fraction as F
def allowed(E, V):
    if V <= 0 or 2 * E < 2 * V: return V > 0 and E == V
    d = F(2 * E, V); return V >= 2 * (1 + (d - 1) + (d - 1) ** 2 + (d - 1) ** 3)
for k in range(3, 9):
    N = 1 << k
    best = max((E - V, E, V) for E in range(1, N + 1) for V in range(1, E + 1) if allowed(E, V))
    print("N=%4d: largest edges - vertices allowed with at most N edges: %d (at E=%d, V=%d)  => classes >= %d" % (N, best[0], best[1], best[2], N - best[0]))
print("cross-check with my exhaustive search (v4.out): excess 3 allowed at E=16? %s  E=17? %s  E=18? %s" % (allowed(16, 13), allowed(17, 14), allowed(18, 15)))
