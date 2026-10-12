#!/usr/bin/env python3
"""run_pl.py [ad-1-linesums]  adds the task PL16 (the 20 line sums of the plane of order 4, 16 inputs) to j-machine's
steiner.py annealer (auxiliary forms with coefficients from a pool that holds 8, 4, 3, 2, 3/2 and their inverses on purpose).
Energy = size of an honest circuit (count G).  Empty start = 60 = adding-only.  usage: run_pl.py PL16 <seconds> <seed> <outdir> [empty|seed] [temp]
seed mode starts from the 40 pair sums of the adding-only circuit (energy 60) and never restarts."""
import sys, numpy as np
sys.path.insert(0, '.')
import slp, steiner
def gmul(a, b):
    r = 0
    for i in range(2):
        if (b >> i) & 1: r ^= a << i
    if r & 4: r ^= 0b111
    return r
rows = []
for x in range(4):
    v = [0.] * 16
    for y in range(4): v[x | (y << 2)] = 1.
    rows.append(v)
for m in range(4):
    for c in range(4):
        v = [0.] * 16
        for x in range(4): v[x | ((gmul(m, x) ^ c) << 2)] = 1.
        rows.append(v)
T = np.array(rows)
orig = slp.task
def task(name):
    if name == 'PL16':
        known = []                                  # seed mode: the 40 pair sums of the adding-only circuit (then every line is one gate away)
        for r in rows:
            p = [i for i in range(16) if r[i]]
            known += [(p[0], p[1], 1., 1.), (p[2], p[3], 1., 1.)]
        return T, known, list(range(20))
    return orig(name)
slp.task = task
steiner.main()
