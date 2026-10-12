#!/usr/bin/env python3
"""whatif.py [ab-1-fewerblocks]  FLOATS.  EVERY LINE HERE IS A WHAT-IF COUNT: a block list with no network behind it.
The engine's price law: z is the root of  sum over blocks of (rank/m)^z = W ; saving = 1 - z.  (root() copied from x-6's zlaw.py)"""
import math, itertools
def root(blocks, m, W):
    mom = lambda e: sum(n * (r / m) ** (1 - e) for r, n in blocks) / W
    if mom(0.0) >= 1: return 0.0
    lo, hi = 0.0, 1.0
    if mom(hi) < 1: return 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if mom(mid) < 1: lo = mid
        else: hi = mid
    return lo
print("== TABLE B.  Fat ports (h, r): ceiling on kappa from knows.py / mis.py, and what that ceiling is worth")
print("   three-stage word, m = 3h, per data array: blocks h-r, h-r, h-r, 2r ; totals: 1.5/kappa blocks of rank h per array; no helpers")
print("   merged: blocks h-r, h, h ; in place (a word nobody has): m = h, one block h-r per array, 1/kappa totals of rank h-1 and of rank 1")
rows = [(5, 2, 2.5, "exact"), (6, 2, 3.75, "between 3.48 and 3.75"), (7, 3, 2.647, "at most"), (8, 3, 4.364, "at most"), (9, 3, 4.636, "at most"), (9, 4, 2.55, "at most"),
        (8, 2, 8.0, "at most"), (9, 2, 8.5, "at most"), (9, 1, 16.0, "at most; the published E8 scatter has 15")]
for h, r, kap, st in rows:
    need = 1.5 * h / r
    a = root([(h - r, 3), (2 * r, 1), (h, 1.5 / kap)], 3 * h, 1)
    b = root([(h - r, 1), (h, 2), (h, 1.5 / kap)], 3 * h, 1)
    c = root([(h - r, 1), (h - 1, 1 / kap), (1, 1 / kap)], h, 1)
    a0 = root([(h - r, 3), (2 * r, 1)], 3 * h, 1); b0 = root([(h - r, 1), (h, 2)], 3 * h, 1); c0 = 1.0
    print("   (h,r) = (%d,%d): kappa <= %.3f (%s); gain needs kappa > %.2f : %s ; saving three-stage %.4f (free shears: %.4f) ; merged %.4f (free: %.4f) ; in place %.4f"
          % (h, r, kap, st, need, "PASSES" if kap > need else "fails", a, a0, b, b0, c))
print("== the club ceiling 2^(ceil((h+1)/2) - r) (rough; exact values above) against the threshold 3h/(2r), r = h/3")
for h in (9, 12, 15, 18, 24, 30, 45):
    r = h // 3; kap = 2.0 ** (math.ceil((h + 1) / 2) - r)
    print("   h = %2d, r = %2d : ceiling about %8.1f ; threshold %.2f ; three-stage saving AT the ceiling %.4f ; with free shears %.4f ; merged at the ceiling %.4f"
          % (h, r, kap, 1.5 * h / r, root([(h - r, 3), (2 * r, 1), (h, 1.5 / kap)], 3 * h, 1), root([(h - r, 3), (2 * r, 1)], 3 * h, 1), root([(h - r, 1), (h, 2), (h, 1.5 / kap)], 3 * h, 1)))
print("== TABLE C1.  One big block and one block of rank 1 per array: blocks (m-1-d, 1), d = moves saved per array")
for m in (4, 5, 9, 45, 110):
    out = []
    for d in (0.1, 0.25, 0.5, 1, 2):
        if m - 1 - d > 0: out.append("d=%.2f: %.4f (by moves alone %.4f)" % (d, root([(m - 1 - d, 1), (1, 1)], m, 1), 1 - math.log(m - d) / math.log(m)))
    lo, hi = 0.0, m - 1.5
    for _ in range(60):
        mid = (lo + hi) / 2
        if root([(m - 1 - mid, 1), (1, 1)], m, 1) < 0.1: lo = mid
        else: hi = mid
    print("   m = %3d : %s ; saving 0.1 needs d = %.3f moves per array = %.2f %% of the moves" % (m, " ; ".join(out), hi, 100 * hi / m))
print("== TABLE C2.  Tiny shapes scored by blocks.  'cut into single moves' = the score every search used; 'best grouping' = fewest/largest blocks")
print("   allowed by (full game) the floor theorem sum(1 - 2^-rank) >= W (1 - 2^-m), or (sub-game) at least 2W blocks [this report]")
def parts(k, mx):
    def rec(k, mx):
        if k == 0: yield (); return
        for p in range(min(k, mx), 0, -1):
            for rest in rec(k - p, p): yield (p,) + rest
    return rec(k, mx)
for m, W, k in ((3, 3, 8), (4, 3, 10), (4, 3, 11), (4, 4, 15), (5, 2, 9), (5, 4, 17), (5, 8, 31), (5, 8, 34), (6, 16, 63)):
    by_moves = 1 - math.log(k / W) / math.log(m)
    best = {"full": (0, None), "sub": (0, None)}
    if k <= 34:
        for p in parts(k, m - 1):
            bl = [(r, p.count(r)) for r in set(p)]
            e = root(bl, m, W)
            if sum(1 - 2.0 ** -r for r in p) >= W * (1 - 2.0 ** -m) - 1e-12 and e > best["full"][0]: best["full"] = (e, p)
            if len(p) >= 2 * W and e > best["sub"][0]: best["sub"] = (e, p)
    print("   m = %d, %2d arrays in %2d moves (%.3f per array): cut into single moves %.4f ; best grouping, full game %.4f %s ; sub-game %.4f %s"
          % (m, W, k, k / W, by_moves, best["full"][0], best["full"][1], best["sub"][0], best["sub"][1]))
print("== TABLE C3.  The character floor of the sub-game (lp.py, lp_sym.py): every direction once for 2^(m-2) arrays; saving if it existed")
for m in (4, 5, 6, 7, 8, 9, 16, 45, 110):
    a = 4 - 2.0 ** (2 - m)
    print("   m = %3d : %.4f moves per array against %d ; saving 1 - ln(%.4f)/ln(%d) = %.4f" % (m, a, m, a, m, 1 - math.log(a) / math.log(m)))
