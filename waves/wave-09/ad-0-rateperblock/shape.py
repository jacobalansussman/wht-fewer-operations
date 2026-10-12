#!/usr/bin/env python3
"""shape.py [ad-0-rateperblock]  FLOATS.  The price law read block by block.  No certificate is read; every line is a property of the law
    sum over blocks of (rank/m)^z = W      (z = 1 - e)
or a WHAT-IF block list.  Exact rewriting used throughout: give every block a share beta of its array's m moves (the moves it
STANDS FOR, its own plus the ones skipped on its account; the shares of an array add up to 1).  Then the law holds as soon as every block has
    rank <= m * beta^(1/z) ,  i.e. the block makes at most the fraction beta^(e/(1-e)) of the moves it stands for.
A block that meets this pays for itself; one that does not must be paid for by another."""
import math
def root(blocks, m, W):
    mom = lambda e: sum(n * (r / m) ** (1 - e) for r, n in blocks)
    if mom(0.0) >= W: return 0.0
    lo, hi = 0.0, 1.0
    if mom(hi) < W: return 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if mom(mid) < W: lo = mid
        else: hi = mid
    return lo
print("A. What ONE interruption costs, by where it falls [law only].  An array on the plain schedule (m-1, 1) is cut once more, t moves from one end:")
print("   blocks (t, m-1-t, 1); moves it must save elsewhere for the saving to stay at e = 0.1, i.e. m^e (t^(1-e) + (m-1-t)^(1-e) - (m-1)^(1-e)):")
for m in (9, 45, 110):
    ts = sorted({1, 2, 4, 8, m // 5, m // 3, (m - 1) // 2})
    print("   m = %3d : " % m + " ; ".join("t=%d: %.3f" % (t, m ** 0.1 * (t ** 0.9 + (m - 1 - t) ** 0.9 - (m - 1) ** 0.9)) for t in ts if 0 < t < m - 1)
          + "   (first-order bar of aa-cross for a single move: %.3f)" % (m ** 0.1 / 0.9 - 1))
print("B. The share of its own stage that a block must skip to pay for itself: 1 - beta^(e/(1-e)), beta = (moves it stands for) / m")
for e in (0.01, 0.05, 0.1, 0.2, 0.5):
    print("   saving %.2f : " % e + " ; ".join("beta 1/%d: %.4f" % (k, 1 - (1 / k) ** (e / (1 - e))) for k in (2, 3, 5, 9, 45, 110)) + " ; beta 44/45: %.5f" % (1 - (44 / 45) ** (e / (1 - e))))
print("   in moves, for a stage of h directions in a word of s stages (m = s h), saving 0.1: h (1 - s^(-1/9)):")
for s in (2, 3, 5):
    print("   s = %d : " % s + " ; ".join("h=%d: %.3f" % (h, h * (1 - s ** (-1 / 9))) for h in (3, 4, 6, 9, 13, 16, 22)))
print("C. A stage block that skips exactly ONE direction of its h (the published role climb, taken whole) pays for itself at saving")
print("   e_block = ln(h/(h-1)) / ln(m/(h-1))   [exact root of ((h-1)/m)^z = h/m]:")
for s in (2, 3, 5):
    print("   s = %d stages : " % s + " ; ".join("h=%d: %.4f" % (h, math.log(h / (h - 1)) / math.log(s * h / (h - 1))) for h in (3, 4, 6, 9, 13, 16, 22)))
print("D. The same block when the word pays back all but one skipped move per array (LEGAL shape of the published five-stage word, role climbs whole,")
print("   helpers and copies free: WHAT-IF), against the shape with nothing paid back (WHAT-IF, no word does this):")
for h in (3, 4, 6, 9, 16, 22):
    m = 5 * h
    idle = [(2 * h + 2, 2), (2 * h - 2, 2), (h - 1, 2), (4, 2)]
    print("   h = %2d : five-stage word %.4f ; nothing paid back %.4f ; ratio %.2f" % (h, root([(h - 1, 10)] + idle, m, 4), root([(h - 1, 20)], m, 4), root([(h - 1, 20)], m, 4) / root([(h - 1, 10)] + idle, m, 4)))
print("E. How many helper arrays a data array can afford [WHAT-IF].  Data arrays: 5 blocks of h-1, nothing paid back (the best line of D).")
print("   Helpers: g per data array, each one block of rank h per stage (their least), no copies.  Saving:")
for h in (3, 6, 9):
    print("   h = %d : " % h + " ; ".join("g=%.2f: %.4f" % (g, root([(h - 1, 5), (h, 5 * g)], 5 * h, 1 + g)) for g in (0, 0.25, 0.5, 1, 1.63, 3)))
print("   the same with helpers on the plain schedule (5h-1, 1) (a helper that is never interrupted; no network has one):")
for h in (3, 6, 9):
    print("   h = %d : " % h + " ; ".join("g=%.2f: %.4f" % (g, root([(h - 1, 5), (5 * h - 1, g), (1, g)], 5 * h, 1 + g)) for g in (0, 0.25, 0.5, 1, 1.63, 3)))
