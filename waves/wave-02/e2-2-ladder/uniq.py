#!/usr/bin/env python3
"""uniq.py -- block size 4, old letters: is the even design the ONLY way to meet the counting bound?  [e2-2-ladder]
For W = 4 (15 moves) and W = 8 (30 moves): force one direction z to be used fewer times, or more times, than in the
even design (n_z = W/4) and ask the integer programme (covering condition only, no parity) for the fewest moves.
If every forced case needs more than the bound, the even design is the only count vector at the bound.
Then, by the frame argument of e2-2.md section 2, no unit WITHOUT scratch arrays has that many moves.
"""
import sys, math
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
m = 4
pairs = [(i, j) for i in range(m) for j in range(i, m)]
V = list(range(1, 1 << m))
def qval(Q, z):
    s = 0
    for k, (i, j) in enumerate(pairs):
        if Q >> k & 1 and z >> i & 1 and z >> j & 1: s ^= 1
    return s
diag = [k for k, (i, j) in enumerate(pairs) if i == j]
rows = set()
for Q in range(1, 1 << len(pairs)):
    if sum(Q >> k & 1 for k in diag) & 1:
        rows.add(tuple(qval(Q, z) for z in V))
A = np.array(sorted(rows), dtype=float)
nz = len(V)
for W in (4, 8, 12):
    base = W // 4
    bound = 15 * base
    worst = None
    for i in range(nz):
        for lab, lo, hi in (("fewer", 0, base - 1), ("more", base + 1, np.inf)):
            lb = np.zeros(nz); ub = np.full(nz, np.inf)
            lb[i], ub[i] = lo, hi
            res = milp(np.ones(nz), constraints=[LinearConstraint(A, W, np.inf)], integrality=np.ones(nz), bounds=Bounds(lb, ub), options={"time_limit": 20})
            k = None if res.x is None else int(round(res.fun))
            if worst is None or (k is not None and k < worst[0]): worst = (k, format(V[i], "04b"), lab, res.status)
    print("W = %d: even design has %d moves (plain %d). Fewest moves when one direction is forced off the even count: %s (direction %s used %s often; status %d)"
          % (W, bound, 4 * W, worst[0], worst[1], worst[2], worst[3]), flush=True)
    print("   -> the even design is %s count vector with %d moves" % ("the ONLY" if worst[0] > bound else "NOT the only", bound), flush=True)
