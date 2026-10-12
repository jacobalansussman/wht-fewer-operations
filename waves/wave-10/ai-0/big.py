#!/usr/bin/env python3
"""big.py [ai-0]  Count only (python whole numbers, nothing built): where does the tower first beat 2N?

Main terms of my builder (check.py), in closed form:
   outputs N ; helper A = one cubic on m bits ; helper B of a real colour c = 2^(start of level c) pieces, each one
   quadratic on m - start - s bits ; helper B of a colour that forgets nothing = one quadratic on m bits ;
   plus the forming of coefficients, bounded here by OVER (justified in ai-0.md section 4).
Inner evaluators, two versions:
   "textbook": f = g + x h, one gate per point with x = 1 (exact counts T2, T3 of check.py's recursion);
   "ad-6":     degree 2 by ad-6's count-only law E2 (ad-6-twohelpers/law.py, imported untouched; replayed by the
               critic af-0 up to k = 20, NOT replayed at these sizes), degree 3 by one more variable at a time:
               C3(j + 1) = C3(j) + E2(j) + 2^j.
"""
import sys, os, io, contextlib
from fractions import Fraction
sys.setrecursionlimit(100000)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ad-6-twohelpers"))
with contextlib.redirect_stdout(io.StringIO()):
    import law
KMAX = 2064
T2 = [0] * (KMAX + 1); T3 = [0] * (KMAX + 1); t1 = 0
for j in range(1, KMAX + 1):
    T3[j] = T3[j - 1] + T2[j - 1] + (1 << (j - 1)); T2[j] = T2[j - 1] + t1 + (1 << (j - 1)); t1 = t1 + (1 << (j - 1))
E2 = [0] * (KMAX + 1); C3 = [0] * (KMAX + 1)
for j in range(KMAX + 1): E2[j] = law.E2(j)[0]            # bottom-up, so the recursion stays shallow
for j in range(KMAX): C3[j + 1] = C3[j] + E2[j] + (1 << j)

def levels(Lr, s):
    offs = []; m = 0
    for j in range(Lr):
        offs.append(m); m += s * (1 if j == 0 else (1 << m))
    return offs, m

def count(Lr, s, t, extra, quad, cub):
    offs, mt = levels(Lr, s); m = mt + extra; k = m + t; N = 1 << k
    tot = N + cub[m]
    for c in range(1 << t):
        tot += (1 << offs[c]) * quad[m - offs[c] - s] if c < Lr else quad[m]
    over = 0                                            # forming coefficients: see ai-0.md section 4
    nq = 1 + m + m * (m - 1) // 2
    over += (1 << t) * 3 * nq + m * (2 * (offs[-1]) + 1) + (1 + m + m * (m - 1) // 2 + m * (m - 1) * (m - 2) // 6) + (1 << t) * nq
    for c in range(Lr):
        o = offs[c]; over += (1 << o) * (1 + m) * (1 + o + o * (o - 1) // 2)
    return k, N, tot, over

def show(x, N): return "%.6f" % float(Fraction(x, N))
print("sanity of the closed form against my built circuit (check.py, run3.out): 3 real colours of 4, s = 1, k = 13:")
k, N, tot, over = count(3, 1, 2, 0, T2, T3)
print("   main terms %d (built: outputs 8190 + A 6064 + B 5052 + B trivial 4083 = %d, two outputs need no gate) ; bound on coefficient gates %d (built: see run3.out)" % (tot, 8190 + 6064 + 5052 + 4083, over))
print()
print("degree-2 law of ad-6 at the sizes used: E2(j)/2^j =", ", ".join("%d: %s" % (j, show(E2[j], 1 << j)) for j in (400, 1024, 2046, 2058, 2060)))
print()
print("%-44s %6s %-22s %-22s %-22s" % ("design", "k", "tower, textbook inside", "tower, ad-6 inside", "best without tower"))
for name, (Lr, s, t, extra) in (("2 colours, s=2", (2, 2, 1, 0)), ("3 real colours of 4, s=1", (3, 1, 2, 0)), ("3 real colours of 4, s=1, +50 bits", (3, 1, 2, 50)),
                                ("3 real colours of 4, s=2", (3, 2, 2, 0)), ("3 real colours of 4, s=2, +4 bits", (3, 2, 2, 4)), ("4 colours, s=1", (4, 1, 2, 0)), ("4 colours, s=1, +3 bits", (4, 1, 2, 3))):
    k, N, a, ov = count(Lr, s, t, extra, T2, T3); _, _, b, _ = count(Lr, s, t, extra, E2, C3)
    print("%-44s %6d %-22s %-22s %-22s   coefficient gates at most %.3g = %.1e N" % (name, k, show(a + ov, N), show(b + ov, N), show(C3[k], N), ov, float(Fraction(ov, N))))
print()
print("in the limit (inner costs exactly 1 and 2 gates per point, coefficient gates dropped), gates/N of a tower with Lr real colours of 2^t and s-bit atoms:")
print("   1 + 2/2^t + (Lr/2^s + (2^t - Lr)) / 2^t")
for Lr, t, s in ((2, 1, 2), (3, 2, 1), (3, 2, 2), (3, 2, 3), (4, 2, 1), (4, 2, 2), (4, 2, 3), (8, 3, 3), (16, 4, 4)):
    v = 1 + Fraction(2, 1 << t) + Fraction(Lr, (1 << s) * (1 << t)) + Fraction((1 << t) - Lr, 1 << t)
    offs, m = levels(Lr, s) if Lr <= 3 or (Lr == 4 and s == 1) else (None, None)
    print("   Lr=%2d of %2d, s=%d : %s = %.4f   %s" % (Lr, 1 << t, s, v, float(v), ("needs k = %d" % (m + t)) if m else "needs a tower of bits"))
