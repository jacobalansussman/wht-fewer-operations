#!/usr/bin/env python3
"""zlaw.py [x-6-unitasbox]  The growth law of a unit in the engine's own accounting (R/tools/gen/foldlib.py, whole blocks):
a unit with W arrays, label dimension m and blocks of ranks r_1, r_2, ... gives O(n (log n)^z) for every z with
        sum over blocks of (r_i / m)^z  <  W          (fill parameter -> infinity; at fill 2^13 the tool's own formula).
FLOATS / decimals: this is a root of a transcendental equation, not an exact computation.  Saving = 1 - z.
Reads the published certificate's block list (read only).  Everything marked WHAT-IF is a block list nobody has a network for."""
import sys, json, gzip, math
from decimal import Decimal as Dc, getcontext
getcontext().prec = 50
def root(blocks, m, W, S=None):
    """largest saving e with moment < 1; blocks = list of (rank, count)"""
    def mom(e):
        z = 1 - e
        s = sum(n * (r / m) ** z for r, n in blocks) / W
        if S is None: return s
        f = 1 - 2.0 ** -S
        return f * s + (1 - f) * (((m - 1) / m) ** z + (1 / m) ** z)
    if mom(0.0) >= 1: return 0.0
    lo, hi = 0.0, 1.0
    if mom(hi) < 1: return 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if mom(mid) < 1: lo = mid
        else: hi = mid
    return lo
def show(name, blocks, m, W, S=None):
    mv = sum(r * n for r, n in blocks); nb = sum(n for r, n in blocks)
    e = root(blocks, m, W, S)
    print("%-78s W=%6d m=%3d blocks/array %6.2f moves/array a=%8.3f  saving %.4e%s" % (name, W, m, nb / W, mv / W, e, "" if S is None else "  (fill 2^%d)" % S))
    return e
for path in sys.argv[1:]:
    d = json.load(gzip.open(path)); h, v, R = d["h"], d["v"], d["R"]; bl = d["blocks"]; m = 5 * h
    idle = [(2 * (h - 1) + 4, 2 * v), (2 * (h - 1), 2 * v), (h - 1, 2 * v), (4, 2 * v)]
    def unit(classes):
        B = {}
        for c in classes:
            for r, n in bl[c].items(): B[int(r)] = B.get(int(r), 0) + 5 * n
        return sorted(B.items()) + idle
    print("== certificate h=%d v=%d R=%d : five-stage word, m = 5h" % (h, v, R))
    show("published unit (all blocks)", unit("xysc"), m, 4 * v + R, 13)
    show("published unit (all blocks), fill -> infinity", unit("xysc"), m, 4 * v + R)
    show("WHAT-IF no scratch copies", unit("xys"), m, 4 * v + R, 13)
    show("WHAT-IF no copies and no helpers, data blocks split as in the certificate", unit("xy"), m, 4 * v)
    show("WHAT-IF no copies, no helpers, every data array one whole block of rank h-1 per invocation", [(h - 1, 10 * v)] + idle, m, 4 * v)
    for r in range(1, h // 2 + 1):
        idr = [(2 * (h - r) + 4 * r, 2 * v), (2 * (h - r), 2 * v), (h - r, 2 * v), (4 * r, 2 * v)]
        show("WHAT-IF the same with ports of dimension r = %d (blocks h-r; catch-up 4r)" % r, [(h - r, 10 * v)] + idr, m, 4 * v)
print("== shapes that do not depend on h (rho = r/h, the share of a stage that the port covers); all WHAT-IF, shears and helpers free")
for rho in (0.02, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5):
    e5 = root([((1 - rho), 10), (2 * (1 - rho) + 4 * rho, 2), (2 * (1 - rho), 2), ((1 - rho), 2), (4 * rho, 2)], 5.0, 4)
    e3 = root([((1 - rho), 3), (2 * rho, 1)], 3.0, 1)
    e1 = root([((1 - rho), 1), (2 * rho / 3, 1)], 1.0, 1)        # every stage: one block 1-rho, and a catch-up of 2/3 of the port
    print("   rho = %.2f : five-stage bridged word %.4f ; three-stage word (3 blocks of h-r, one catch-up of 2r) %.4f" % (rho, e5, e3))
print("== k equal blocks per array, a share rho of the directions never moved along: saving = ln(1/(1-rho)) / (ln k + ln(1/(1-rho)))")
for k in (1, 2, 3, 6, 20):
    print("   k = %2d : " % k + " ; ".join("rho %.3f -> %.4f" % (rho, math.log(1 / (1 - rho)) / (math.log(k) + math.log(1 / (1 - rho)))) for rho in (1 / 45, 0.05, 0.1, 0.2, 0.5)))
print("   needed share rho for saving 0.1 :", " ; ".join("k = %d : %.3f" % (k, 1 - k ** (-1 / 9)) for k in (2, 3, 6, 20, 100)))
print("== three-stage word with the two paid port blocks merged into the next stage's climb (3 blocks per array: h-r, h, h); WHAT-IF, nobody has such a word")
for rho in (1 / 9, 0.2, 0.3, 1 / 3, 0.4, 0.5):
    print("   rho = %.3f : saving %.4f   (four blocks, unmerged: %.4f)" % (rho, root([((1 - rho), 1), (1.0, 2)], 3.0, 1), root([((1 - rho), 3), (2 * rho, 1)], 3.0, 1)))
print("== one-dimensional port, three merged blocks (h-1, h, h), by h:", " ; ".join("h=%d: %.4f" % (h, root([(h - 1, 1), (h, 2)], 3.0 * h, 1)) for h in (3, 5, 9, 16, 22)))
