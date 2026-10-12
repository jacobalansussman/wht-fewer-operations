#!/usr/bin/env python3
"""unit_batch.py -- the published unit read as a batch.  [e2-2-ladder, 2026-10-10]  Reads the release tree, writes nothing there.
Block list of one unit exactly as tools/whatif_copies.py builds it (five invocations + idle blocks of the twins).
Rate condition of the engine (Work/Block/Engine.lean, allotB_bound):  sum over blocks (rank/m)^z < W.
Floating point (decimal, 60 digits) for the roots; counts are integers.
"""
import sys, json, gzip, math
from decimal import Decimal as Dc, getcontext
getcontext().prec = 60
R = "not-in-this-repository/wht-power-saving-r4-candidate/tools/certificate/"

def load(p):
    return json.load(gzip.open(p) if p.endswith(".gz") else open(p))

def unit_blocks(h, v, bl, classes="xysc"):
    B = {}
    per = {}
    for c in classes:
        for r, n in bl[c].items():
            B[int(r)] = B.get(int(r), 0) + 5 * n
            per[c] = per.get(c, 0) + 5 * n * int(r)
    idle = 0
    for r in (2 * (h - 1) + 4, 2 * (h - 1), h - 1, 4):
        B[r] = B.get(r, 0) + 2 * v
        idle += 2 * v * r
    per["idle"] = idle
    return B, per

def moment(B, m, W, z):
    lm = Dc(m).ln()
    return sum(Dc(n) * ((Dc(r).ln() - lm) * Dc(z)).exp() for r, n in B.items()) / Dc(W)

def root(B, m, W):
    lo, hi = Dc(0), Dc(1)
    if moment(B, m, W, 1) >= 1:
        return None
    for _ in range(120):
        mid = (lo + hi) / 2
        if moment(B, m, W, mid) < 1: hi = mid
        else: lo = mid
    return hi

for name in ("gcert1-e8-r783.json.gz", "gcert1-p11-pr193.json.gz", "c2-combine-best-h16.json"):
    d = load(R + name)
    h, v, Rr = d["h"], d["v"], d["R"]
    bl = d["blocks"]
    m, W = 5 * h, 4 * v + Rr
    B, per = unit_blocks(h, v, bl)
    nb = sum(B.values()); mv = sum(r * n for r, n in B.items())
    D = W * m - mv
    z = root(B, m, W)
    ent = sum(Dc(n) * Dc(r) / Dc(m) * (Dc(m) / Dc(r)).ln() for r, n in B.items()) / Dc(W)   # moves-weighted ln(m/r), per array
    print("== %s" % name)
    print("  batch: W = %d arrays (%d data = 4v, %d helpers), each of n = 2^(%d f) points, any f" % (W, 4 * v, Rr, m))
    print("  separately: W m = %d moves.  unit: %d moves in %d blocks (%.2f blocks per array, mean rank %.2f of %d)"
          % (W * m, mv, nb, nb / W, mv / nb, m))
    print("  moves by class (x, y: the two data arrays of a pair; s: helpers; c: scratch copies; idle: twins):", per)
    print("  D = %d moves saved; move ratio (batch / separate at z = 1) = 1 - %.6e" % (D, D / (W * m)))
    print("  saved moves per array: %.4f of %d;  per data array: %.4f" % (D / W, m, D / (4 * v)))
    print("  fragmentation F = sum (r/m) ln(m/r) / W = %s nats  (a whole transform cut into blocks of mean size m/e^F)" % str(ent)[:10])
    print("  exponent from the block list (no table-fill correction): z = %s, saving %s" % (str(z)[:14], str(1 - z)[:12]))
    print("  first-order check: (D / W m) / F = %s" % str(Dc(D) / Dc(W * m) / ent)[:12])
    print("  two-round rate theta = 2^z - 1 = %s" % str(Dc(2) ** z - 1)[:12])
    # what would have to change: delete a fraction of all moves uniformly (same shape), find the fraction that gives z = 0.9, 0.5
    for target in (Dc("0.99"), Dc("0.9"), Dc("0.5")):
        lo, hi = Dc(0), Dc(1)
        for _ in range(100):
            mid = (lo + hi) / 2
            # keep a fraction (1 - mid) of every block class
            if (1 - mid) * moment(B, m, 1, target) / Dc(W) < 1: hi = mid
            else: lo = mid
        print("    for z = %s with the same block shapes: %.4f of all blocks deleted, i.e. %.2f moves saved per array of %d (now %.4f)"
              % (target, hi, float(hi) * mv / W, m, D / W))
    # the other knob: same number of moves, but in blocks of one rank r for every array (r | not needed): moves per array needed
    for target in (Dc("0.9"), Dc("0.5")):
        out = []
        for r in (1, 2, 4, m // 5, m // 3, m // 2, m - 1):
            # k blocks of rank r per array:  k (r/m)^z < 1
            k = float(((Dc(m) / Dc(r)).ln() * target).exp())
            out.append("rank %d: fewer than %.2f blocks = %.1f moves per array" % (r, k, k * r))
        print("    for z = %s with blocks of one rank: " % target + "; ".join(out))
