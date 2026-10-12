#!/usr/bin/env python3
"""b-0: for the family's DAG at N = 2^k, the minimum number of scale gates (count (O)) over ALL ways of storing each node at a
power-of-two multiple of its true value, with a scaled copy of a node shared by all its users.  target t: outputs must be H / 2^t.
Integer program (HiGHS via scipy.optimize.milp); 'optimal' is HiGHS's proof, 'feasible' is only an upper bound.
usage: scale_ilp.py k tlimit"""
import sys, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
from fam import build
k = int(sys.argv[1]); tl = float(sys.argv[2])
N, gates, kind, outs = build(k)
S = list(range(-2, k // 2 + 3))
def solve(target):
    G = len(gates); zi = {}; mi = {}; nv = 0
    for i in range(G):
        for s in S: zi[(N + i, s)] = nv; nv += 1
    def m(u, d):
        nonlocal nv
        if (u, d) not in mi: mi[(u, d)] = nv; nv += 1
        return mi[(u, d)]
    rows = []   # each: list of (var, coef), ub
    for i in range(G): rows.append(([(zi[(N + i, s)], 1) for s in S], 1, 1))
    for i, (a, u, b, v) in enumerate(gates):
        t = N + i
        for (c, w) in ((a, u), (b, v)):
            al = abs(c).bit_length() - 1
            for st in S:
                if w < N:
                    d = al - st
                    if d: rows.append(([(zi[(t, st)], 1), (m(w, d), -1)], -np.inf, 0))
                else:
                    for sw in S:
                        d = al + sw - st
                        if d: rows.append(([(zi[(w, sw)], 1), (zi[(t, st)], 1), (m(w, d), -1)], -np.inf, 1))
    for o in outs:
        for so in S:
            d = so - target
            if d: rows.append(([(zi[(o, so)], 1), (m(o, d), -1)], -np.inf, 0))
    A = lil_matrix((len(rows), nv)); lo = np.empty(len(rows)); ub = np.empty(len(rows))
    for r, (terms, l, h) in enumerate(rows):
        for (j, cf) in terms: A[r, j] = cf
        lo[r] = l; ub[r] = h
    c = np.zeros(nv)
    for j in mi.values(): c[j] = 1
    res = milp(c, constraints=LinearConstraint(A.tocsr(), lo, ub), integrality=np.ones(nv), bounds=Bounds(0, 1), options={'time_limit': tl})
    return res
for target in sorted({0, k // 2, 1, (k + 1) // 2}):
    r = solve(target)
    G = len(gates)
    if r.x is None: print('N=%d target H/2^%d: no solution in time (%s)' % (N, target, r.message)); continue
    mm = int(round(r.fun))
    print('N=%d  outputs H/2^%d : min scale gates %s %d  -> total (O) = %d additions/subtractions + %d = %d ; textbook N k = %d ; status: %s ; dual bound %.2f'
          % (N, target, '=' if r.status == 0 else '<=', mm, G, mm, G + mm, N * k, 'optimal (proved by HiGHS)' if r.status == 0 else 'feasible only', getattr(r, 'mip_dual_bound', float('nan'))), flush=True)
