#!/usr/bin/env python3
"""minj.py  (h-8-provethewrongthi, 2026-10-11)

Least number of gates, count (G), for the 8-point Walsh-Hadamard transform when every wire must come from a fixed
finite POOL and at most j of the wires may be over the limit (s*s' > N).  Integer programme (scipy.optimize.milp, HiGHS).
  variables: x_v = wire v is held;  y_e = gate e = (a, b -> c) is used (a, b, c three pool wires on one line);  pi_v = time stamp.
  minimise sum x_v;  outputs held;  a held wire needs one used gate;  a used gate needs both inputs held and earlier.
The UPPER bound (the circuit found) is replayed here in exact integers.  The LOWER bound is the solver's (floating point):
a solver statement, not a proof.

usage: minj.py pool j [timelimit]      pool in: tight | tight+hub04 | tight+hub84 | stab (the 240 stabiliser vectors) | stab+cubic (304)
"""
import sys, itertools, time, json
from math import gcd
from collections import defaultdict
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import coo_matrix

poolname = sys.argv[1]; J = int(sys.argv[2]); TL = float(sys.argv[3]) if len(sys.argv) > 3 else 600
k = 3; N = 8
pc = lambda x: bin(x).count("1")
def norm(v):
    g = 0
    for a in v: g = gcd(g, abs(a))
    if g == 0: return None
    v = [a // g for a in v]
    for a in v:
        if a != 0:
            if a < 0: v = [-b for b in v]
            break
    return tuple(v)
def had(v): return [sum(v[x] * (-1) ** pc(x & y) for x in range(N)) for y in range(N)]
def ss(v): return sum(1 for a in v if a), sum(1 for a in had(v) if a)

# coset sign vectors: (-1)^g on a coset, g a polynomial of degree <= deg in the coordinates of the coset
def subspaces():
    subs = set()
    for r in range(k + 1):
        for gens in itertools.combinations(range(1, N), r):
            S = {0}
            for g in gens: S |= {s ^ g for s in S}
            if len(S) == 1 << r: subs.add((gens, frozenset(S)))
    seen = {}
    for gens, S in subs: seen.setdefault(S, gens)
    return [(g, S) for S, g in seen.items()]
def coset_vectors(deg):
    res = set()
    for gens, V in subspaces():
        r = len(gens)
        # coordinates: element = xor of gens[i] for bits of m
        elems = []
        for m in range(1 << r):
            e = 0
            for i in range(r):
                if m >> i & 1: e ^= gens[i]
            elems.append(e)
        monos = [mm for mm in range(1 << r) if pc(mm) <= deg]
        reps = sorted({min(c ^ v for v in V) for c in range(N)})
        for coef in itertools.product((0, 1), repeat=len(monos)):
            vals = []
            for m in range(1 << r):
                b = 0
                for cf, mm in zip(coef, monos):
                    if cf and (m & mm) == mm: b ^= 1
                vals.append(b)
            for c in reps:
                vec = [0] * N
                for m in range(1 << r): vec[elems[m] ^ c] = (-1) ** vals[m]
                res.add(norm(vec))
    return res

tight = coset_vectors(1)
assert len(tight) == 128 and all(s * sp == N for s, sp in map(ss, tight))
if poolname == "tight": pool = set(tight)
elif poolname == "tight+hub04": pool = set(tight) | {(1, 1, 1, -1, 0, 0, 0, 0)}
elif poolname == "tight+hub84": pool = set(tight) | {(1, 1, 1, 1, 1, 1, -1, -1)}
elif poolname == "stab": pool = coset_vectors(2)
elif poolname == "stab+cubic": pool = coset_vectors(3)
else: raise SystemExit("pool?")
pool = sorted(pool); P = len(pool); idx = {v: i for i, v in enumerate(pool)}
over = [i for i, v in enumerate(pool) if v not in tight]
inputs = [idx[tuple(1 if x == i else 0 for x in range(N))] for i in range(N)]
outputs = [idx[norm([(-1) ** pc(x & y) for x in range(N)])] for y in range(N)]
print("pool", poolname, "wires", P, "over the limit", len(over), "j <=", J, flush=True)

# lines: group pairs by normalised Pluecker coordinates
lines = defaultdict(set)
pairs = list(itertools.combinations(range(N), 2))
for a in range(P):
    A = pool[a]
    for b in range(a + 1, P):
        B = pool[b]
        pl = norm([A[i] * B[j] - A[j] * B[i] for i, j in pairs])
        lines[pl].update((a, b))
gates = []      # (a, b, c)
for pl, S in lines.items():
    if len(S) < 3: continue
    S = sorted(S)
    for c in S:
        if c in inputs: continue
        for a, b in itertools.combinations([s for s in S if s != c], 2):
            gates.append((a, b, c))
print("lines with 3 or more pool wires:", sum(1 for S in lines.values() if len(S) >= 3), " directed gates:", len(gates), flush=True)

isin = set(inputs)
nonin = [v for v in range(P) if v not in isin]
xi = {v: i for i, v in enumerate(nonin)}; nx = len(nonin)
ny = len(gates); D = 12
nv = nx + ny + nx          # x, y, pi
c = np.zeros(nv); c[:nx] = 1
lb = np.zeros(nv); ub = np.ones(nv); ub[nx + ny:] = D
for o in outputs: lb[xi[o]] = 1
integrality = np.zeros(nv); integrality[:nx + ny] = 1
rows, cols, vals, lo, hi = [], [], [], [], []
r = 0
def add(entries, l, h):
    global r
    for cc, vv in entries: rows.append(r); cols.append(cc); vals.append(vv)
    lo.append(l); hi.append(h); r += 1
prod = defaultdict(list)
for e, (a, b, cw) in enumerate(gates):
    ye = nx + e
    prod[cw].append(ye)
    for inp in (a, b):
        if inp not in isin:
            add([(ye, 1), (xi[inp], -1)], -np.inf, 0)                                   # y <= x_in
            add([(nx + ny + xi[cw], 1), (nx + ny + xi[inp], -1), (ye, -(D + 1))], -D, np.inf)   # pi_c >= pi_in + 1 - (D+1)(1-y)
        else:
            add([(nx + ny + xi[cw], 1), (ye, -1)], 0, np.inf)                            # pi_c >= y
for v in nonin:
    add([(xi[v], 1)] + [(ye, -1) for ye in prod[v]], -np.inf, 0)                         # x_c <= sum y
add([(xi[v], 1) for v in over], -np.inf, J)
A = coo_matrix((vals, (rows, cols)), shape=(r, nv)).tocsr()
print("variables", nv, "constraints", r, flush=True)
t0 = time.time()
res = milp(c, constraints=LinearConstraint(A, np.array(lo), np.array(hi)), integrality=integrality, bounds=Bounds(lb, ub),
           options={"time_limit": TL, "disp": False})
print("solver status:", res.status, res.message, " seconds %.0f" % (time.time() - t0))
print("solver lower bound (floating point):", getattr(res, "mip_dual_bound", None), " gap:", getattr(res, "mip_gap", None))
if res.x is None: raise SystemExit("no circuit found")
held = [v for v in nonin if res.x[xi[v]] > 0.5]
# exact replay: derive the held wires in rounds using the pool's lines
have = set(inputs); order = []
bygate = defaultdict(list)
for a, b, cw in gates: bygate[cw].append((a, b))
changed = True
while changed:
    changed = False
    for v in held:
        if v in have: continue
        for a, b in bygate[v]:
            if a in have and b in have:
                have.add(v); order.append((v, a, b)); changed = True; break
ok = all(o in have for o in outputs) and all(v in have for v in held)
# exact check of each gate: rank 2 of the three integer vectors
def rank2(u, v, w):
    for i, j, l in itertools.combinations(range(N), 3):
        det = (u[i] * (v[j] * w[l] - v[l] * w[j]) - u[j] * (v[i] * w[l] - v[l] * w[i]) + u[l] * (v[i] * w[j] - v[j] * w[i]))
        if det: return False
    return True
ok = ok and all(rank2(pool[a], pool[b], pool[v]) for v, a, b in order)
nover = sum(1 for v in held if v in set(over))
print("RESULT pool=%s j<=%d : circuit with %d gates, %d over-limit wires, exact replay %s ; solver lower bound %s"
      % (poolname, J, len(held), nover, "PASS" if ok else "FAIL", getattr(res, "mip_dual_bound", None)))
for v, a, b in order:
    s, sp = ss(pool[v])
    print("   %-28s (s=%d,s'=%d)%s  from %s , %s" % (list(pool[v]), s, sp, " OVER" if s * sp > N else "", list(pool[a]), list(pool[b])))
