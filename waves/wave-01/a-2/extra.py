#!/usr/bin/env python3
"""a-2 extra: (1) s s' = N for every coset character at N = 16, 32 and a sample at 64; (2) the non-tight wires of the brick circuits."""
import random, sys
sys.path.insert(0, ".")
from tight import tight_wires, vec, wht, supp, bricks
rng = random.Random(3)
for k in (4, 5, 6):
    N = 1 << k
    tw = tight_wires(k)
    ws = list(tw) if k < 6 else rng.sample(list(tw), 20000)
    ok = all(supp(vec(w, N)) == 1 << tw[w] and supp(vec(w, N)) * supp(wht(vec(w, N))) == N for w in ws)
    print("N = %d: %d of %d coset characters checked, s = 2^level and s s' = N for each: %s" % (N, len(ws), len(tw), ok))
for k in (2, 4, 6, 8):
    N = 1 << k
    W, g = bricks(k)
    prods = {}
    for v in W[N:]:
        p = supp(v) * supp(wht(v))
        if p != N:
            prods[p // N] = prods.get(p // N, 0) + 1
    print("bricks, N = %d: %d gates, non-tight wires by s s'/N: %s" % (N, len(g), sorted(prods.items())))
