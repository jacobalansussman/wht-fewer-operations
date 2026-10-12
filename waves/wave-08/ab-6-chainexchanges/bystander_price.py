#!/usr/bin/env python3
"""bystander_price.py [ab-6-chainexchanges]  FLOATS.  The engine's price law (z = root of sum over blocks of (rank/m)^z = W)
on WHAT-IF block lists for the two-stage exchange with a bystander (ring.py (2)): 3 arrays, 2 stages of h directions,
m = 2h, port of dimension r.  Arrays 1 and 2 never move along the port; each array has one native hole of r directions per
stage; arrays 1, 2 catch up one hole, the bystander both.  NO NETWORK is behind any line: helpers free, unwanted terms
ignored, a batch for ports of dimension r assumed.  'kappa': each of the 4 shears pays h/kappa moves in blocks of rank h."""
def root(blocks, m, W):
    f = lambda e: sum(n * (r / m) ** (1 - e) for r, n in blocks) / W
    if f(0.0) >= 1: return 0.0
    lo, hi = 0.0, 1.0
    for _ in range(100):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if f(mid) < 1 else (lo, mid)
    return lo
print("%-7s %-46s %-9s %-9s %-9s %-9s" % ("r/h", "block list", "free", "kappa 60", "kappa 15", "kappa 5"))
for h, r in ((9, 3), (10, 2), (9, 1), (16, 1)):
    m = 2 * h
    lists = {
      "bystander, catch-up merged (2h-r | h-r, h | h-r, h+r)": [(2*h - r, 1), (h - r, 1), (h, 1), (h - r, 1), (h + r, 1)],
      "bystander, catch-up apart (2(h-r), r | ...)": [(2*(h - r), 1), (r, 1), (h - r, 2), (r, 1), (h - r, 2), (2*r, 1)],
    }
    for name, bl in lists.items():
        print("%-7.3f %-56s" % (r / h, name) + " ".join("%-9.4f" % root(bl + ([(h, 4.0 / k)] if k else []), m, 3) for k in (0, 60, 15, 5)))
    pe = [(h - r, 1), (2*(h - r), 1), (2*r, 1), (2*(h - r), 1), (h + r, 1)]
    print("%-7.3f %-56s" % (r / h, "plain exchange, merged (3 stages, 2 arrays)") + " ".join("%-9.4f" % root(pe + ([(h, 3.0 / k)] if k else []), 3 * h, 2) for k in (0, 60, 15, 5)))
print("moves per array, bystander word: (6h - 2r) / 3 against 2h ; skipped share on average r/(3h), the same as the plain exchange")
