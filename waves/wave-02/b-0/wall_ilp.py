#!/usr/bin/env python3
"""b-0: test of e2-0's wall lemma at the smallest size.  Class: points are (i) characters restricted to the aligned blocks
of sizes 1, 2, 4, 8 of ONE chain of halvings and (ii) hubs (character on the left half of a block) +- (a DIFFERENT character on
the right half).  Count (G): a gate is any a*u + b*v.  Question: fewest gates of a program for the 8-point transform whose every
point lies in this class.  Integer program (HiGHS): x_p = point p is computed, y_{p,(u,v)} = p is made from u and v, pos_p = time.
usage: wall_ilp.py tlimit [cap]"""
import sys, itertools, numpy as np
from fractions import Fraction as F
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
tl = float(sys.argv[1]); N = 8
def canon(v):
    for t in v:
        if t: return tuple(v) if t > 0 else tuple(-s for s in v)
def ch(w, m): return [(-1) ** bin(w & x).count('1') for x in range(m)]
def emb(lo, vals):
    v = [0] * N
    for i, t in enumerate(vals): v[lo + i] = t
    return v
inputs = [canon(emb(i, [1])) for i in range(N)]
pieces = {}; hubs = set()
for m in (2, 4, 8):
    for lo in range(0, N, m):
        for w in range(m): pieces[canon(emb(lo, ch(w, m)))] = m
        h = m // 2
        for a in range(h):
            for b in range(h):
                if a != b:
                    for c in (1, -1): hubs.add(canon(emb(lo, ch(a, h) + [c * t for t in ch(b, h)])))
outputs = [p for p, m in pieces.items() if m == N]
helpers = [p for p, m in pieces.items() if m < N] + sorted(hubs - set(pieces))
pts = inputs + helpers + outputs; idx = {p: i for i, p in enumerate(pts)}
assert len(set(pts)) == len(pts)
print('class pool at 8 points: inputs', len(inputs), 'helpers', len(helpers), '(pieces %d, hubs %d)' % (sum(1 for p in helpers if p in pieces), sum(1 for p in helpers if p not in pieces)), 'outputs', len(outputs), flush=True)
def dep(u, v, p):          # p = a*u + b*v with a, b both nonzero?
    for i in range(N):
        for j in range(i + 1, N):
            det = u[i] * v[j] - u[j] * v[i]
            if det:
                a = F(p[i] * v[j] - p[j] * v[i], det); b = F(u[i] * p[j] - u[j] * p[i], det)
                return a != 0 and b != 0 and all(a * u[t] + b * v[t] == p[t] for t in range(N))
    return False
der = []
for p in helpers + outputs:
    others = [q for q in pts if q != p]
    for u, v in itertools.combinations(others, 2):
        if dep(u, v, p): der.append((idx[p], idx[u], idx[v]))
print('one-gate derivations inside the class:', len(der), flush=True)
nI = len(inputs); nP = len(pts); T = 20
xv = {i: i - nI for i in range(nI, nP)}; nx = nP - nI
yv = {d: nx + j for j, d in enumerate(der)}; ny = len(der)
pv = {i: nx + ny + (i - nI) for i in range(nI, nP)}; nv = nx + ny + nx
rows = []
bypt = {}
for d in der: bypt.setdefault(d[0], []).append(d)
for i in range(nI, nP):
    rows.append(([(yv[d], 1) for d in bypt.get(i, [])] + [(xv[i], -1)], 0, 0))
for d in der:
    p, u, v = d
    for w in (u, v):
        if w >= nI:
            rows.append(([(yv[d], 1), (xv[w], -1)], -np.inf, 0))
            rows.append(([(pv[w], 1), (pv[p], -1), (yv[d], T + 1)], -np.inf, T))     # pos_p >= pos_w + 1 if y
cap = int(sys.argv[2]) if len(sys.argv) > 2 else None
if cap is not None: rows.append(([(xv[i], 1) for i in range(nI, nP)], -np.inf, cap))
A = lil_matrix((len(rows), nv)); lo = np.empty(len(rows)); ub = np.empty(len(rows))
for r, (terms, l, h) in enumerate(rows):
    for (j, cf) in terms: A[r, j] = cf
    lo[r] = l; ub[r] = h
c = np.zeros(nv); c[:nx] = 1
lb = np.zeros(nv); ubv = np.ones(nv)
for i in range(nI, nP): ubv[pv[i]] = T; lb[pv[i]] = 1
for o in outputs: lb[xv[idx[o]]] = 1
integ = np.ones(nv); integ[nx + ny:] = 0
res = milp(c, constraints=LinearConstraint(A.tocsr(), lo, ub), integrality=integ, bounds=Bounds(lb, ubv), options={'time_limit': tl})
print('status', res.status, res.message)
if res.x is not None:
    chosen = [pts[i] for i in range(nI, nP) if res.x[xv[i]] > 0.5]
    print('gates in the program found:', len(chosen), '| HiGHS lower bound on gates: %.2f' % res.mip_dual_bound, '| proved optimal:', res.status == 0)
    order = sorted(range(nI, nP), key=lambda i: res.x[pv[i]])
    for i in order:
        if res.x[xv[i]] > 0.5:
            d = [d for d in bypt[i] if res.x[yv[d]] > 0.5][0]
            print('  ', pts[i], '<-', pts[d[1]], ',', pts[d[2]], ' hub' if pts[i] in hubs and pts[i] not in pieces else '')
else:
    print('no program found; HiGHS lower bound', getattr(res, 'mip_dual_bound', None))
