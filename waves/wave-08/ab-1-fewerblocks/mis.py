#!/usr/bin/env python3
"""mis.py [ab-1-fewerblocks]  Largest set of ports no two of which know each other, exactly, by integer programming
(scipy.optimize.milp, HiGHS; the answer is a whole number certified by the solver's own bound, status printed).
Input: an edge list written by knows.py.  Done for every type of port separately and for all ports together."""
import sys, numpy as np, time
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import coo_matrix
f = open(sys.argv[1]); n, m = map(int, f.readline().split()); typ = [None] * n; E = []
for line in f:
    w = line.split()
    if w[0] == "t": typ[int(w[1])] = w[2]
    else: E.append((int(w[0]), int(w[1])))
tl = float(sys.argv[2]) if len(sys.argv) > 2 else 300
def solve(V, name):
    idx = {v: i for i, v in enumerate(V)}; Es = [(idx[a], idx[b]) for a, b in E if a in idx and b in idx]
    k = len(V)
    if not Es:
        print("   %-40s %5d ports, no two know each other: largest set %d, ceiling kappa <= 1" % (name, k, k)); return
    rows = np.repeat(np.arange(len(Es)), 2); cols = np.array(Es).ravel()
    A = coo_matrix((np.ones(len(rows)), (rows, cols)), shape=(len(Es), k)).tocsr()
    t0 = time.time()
    res = milp(c=-np.ones(k), constraints=LinearConstraint(A, -np.inf, 1), integrality=np.ones(k), bounds=Bounds(0, 1), options={"time_limit": tl})
    val = int(round(-res.fun)) if res.x is not None else None
    bound = getattr(res, "mip_dual_bound", None)
    print("   %-40s %5d ports, %6d edges: largest set no two knowing each other = %s (solver status %d, upper bound %s) -> ceiling kappa <= %.3f   [%.0f s]"
          % (name, k, len(Es), val, res.status, None if bound is None else round(-bound, 3), k / val, time.time() - t0), flush=True)
print("==", sys.argv[1])
for t in sorted(set(typ)): solve([v for v in range(n) if typ[v] == t], t)
solve(list(range(n)), "all types together")
