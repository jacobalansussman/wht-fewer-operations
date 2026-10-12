#!/usr/bin/env python3
"""uniq5.py -- block size 5, 4 arrays, old letters: is the odd-weight design the ONLY count vector with 16 moves?  [e2-2-ladder]
The odd-weight design: every direction with an odd number of ones, once (16 moves).  frames.py excludes it without scratch.
Here: force one direction off that design (odd-weight z: n_z = 0, or n_z >= 2; even-weight z: n_z >= 1) and minimise the
number of moves under the covering condition (no parity).  Coordinate permutations keep everything, so one direction of each
weight is enough.  If every forced case needs 17 or more (proved), the odd-weight design is the only 16-move count vector.
"""
import numpy as np, sys
from scipy.optimize import milp, LinearConstraint, Bounds
m, W = 5, 4
pairs = [(i, j) for i in range(m) for j in range(i, m)]
V = list(range(1, 1 << m))
mon = np.array([[(z >> i & 1) & (z >> j & 1) for z in V] for (i, j) in pairs], dtype=np.int64)
diag = [t for t, (i, j) in enumerate(pairs) if i == j]
Qs = np.arange(1, 1 << len(pairs))
bits = ((Qs[:, None] >> np.arange(len(pairs))[None, :]) & 1)
keep = (bits[:, diag].sum(axis=1) % 2) == 1
A = (bits[keep] @ mon) % 2
A = np.unique(A, axis=0).astype(float)
print("m = 5, W = 4: %d covering constraints" % len(A), flush=True)
nz = len(V)
cases = [("00001", 0, 0), ("00001", 2, np.inf), ("00111", 0, 0), ("00111", 2, np.inf), ("11111", 0, 0), ("11111", 2, np.inf),
         ("00011", 1, np.inf), ("01111", 1, np.inf)]
allok = True
for zs, lo, hi in cases:
    i = V.index(int(zs, 2))
    lb = np.zeros(nz); ub = np.full(nz, np.inf); lb[i], ub[i] = lo, hi
    res = milp(np.ones(nz), constraints=[LinearConstraint(A, W, np.inf)], integrality=np.ones(nz), bounds=Bounds(lb, ub), options={"time_limit": 50})
    k = None if res.x is None else int(round(res.fun))
    lbnd = getattr(res, "mip_dual_bound", None)
    print("  direction %s forced to be used %s times: fewest moves found %s, solver's lower bound %s, status %d (0 = proved optimal)"
          % (zs, "0" if hi == 0 else ">= %d" % lo, k, lbnd, res.status), flush=True)
    if lbnd is None or lbnd < 16.5: allok = False
    if k is not None and k <= 16:
        print("     another 16-move count vector: " + " ".join("%s:%d" % (format(V[t], "05b"), int(round(res.x[t]))) for t in range(nz) if round(res.x[t])), flush=True)
print("odd-weight design is the only 16-move count vector: %s" % ("YES (every forced case has lower bound above 16)" if allok else "NOT SHOWN"), flush=True)
