#!/usr/bin/env python3
"""Smallest program inside a pool: integer program (HiGHS through scipy).  count (G): gate = any a*u+b*v.
x_p = 1 if pool point p is held; z_j = 1 if p is justified by the pair (q, r) on a common line;
t_p = step number (continuous) to forbid circular justification.  usage: milp.py pool.json seconds [T]"""
import sys, json, itertools, time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import coo_matrix
d = json.load(open(sys.argv[1])); tl = float(sys.argv[2]); T = int(sys.argv[3]) if len(sys.argv) > 3 else 14
P = d['P']; L = d['L']; ins = set(d['inputs']); outs = set(d['outputs']); n = len(P)
J = []
for l in L:
    for p in l:
        if p in ins: continue
        others = [q for q in l if q != p]
        for q, r in itertools.combinations(others, 2): J.append((p, q, r))
m = len(J); nv = 2 * n + m      # x: 0..n-1, t: n..2n-1, z: 2n..
print('points', n, 'justifications', m, flush=True)
rows = []; cols = []; vals = []; lo = []; hi = []
def add(coefs, l, h):
    i = len(lo)
    for c, v in coefs: rows.append(i); cols.append(c); vals.append(v)
    lo.append(l); hi.append(h)
M = T + 1
byp = {}
for j, (p, q, r) in enumerate(J):
    zj = 2 * n + j
    add([(zj, 1), (q, -1)], -np.inf, 0); add([(zj, 1), (r, -1)], -np.inf, 0)
    add([(n + p, 1), (n + q, -1), (zj, -M)], 1 - M, np.inf)     # t_p >= t_q + 1 - M(1-z)
    add([(n + p, 1), (n + r, -1), (zj, -M)], 1 - M, np.inf)
    byp.setdefault(p, []).append(zj)
for p in range(n):
    if p in ins: continue
    add([(p, 1)] + [(zj, -1) for zj in byp.get(p, [])], -np.inf, 0)   # x_p <= sum z
A = coo_matrix((vals, (rows, cols)), shape=(len(lo), nv)).tocsr()
c = np.zeros(nv); c[:n] = 1
lb = np.zeros(nv); ub = np.ones(nv); ub[n:2 * n] = T
for p in ins: lb[p] = 1; ub[n + p] = 0
for p in outs: lb[p] = 1
integ = np.ones(nv); integ[n:2 * n] = 0
t0 = time.time()
res = milp(c, constraints=LinearConstraint(A, lo, hi), integrality=integ, bounds=Bounds(lb, ub), options={'time_limit': tl, 'disp': True})
print('status', res.status, res.message, 'time', round(time.time() - t0, 1))
print('objective (points held incl. 8 inputs)', getattr(res, 'fun', None), 'dual bound', getattr(res, 'mip_dual_bound', None), 'gap', getattr(res, 'mip_gap', None))
if res.x is not None:
    held = [p for p in range(n) if res.x[p] > 0.5]
    order = sorted(held, key=lambda p: res.x[n + p])
    print('gates', len(held) - len(ins))
    json.dump({'held': [P[p] for p in order], 't': [res.x[n + p] for p in order]}, open(sys.argv[1].replace('.json', '') + '.milp.sol.json', 'w'))
    for p in order: print(round(res.x[n + p], 2), P[p], 'OUT' if p in outs else ('in' if p in ins else ''))
