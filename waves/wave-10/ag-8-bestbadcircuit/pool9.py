#!/usr/bin/env python3
"""pool9.py (ag-8-bestbadcircuit): 4-point transform, circuits with 4 + m gates (count G) whose m helpers are taken from a POOL:
all wires with entries 0, +1, -1 (up to sign; 40 points, minus the 4 inputs and the 4 rows = 32).  NOT exhaustive over all circuits:
exhaustive over this pool only.  For every irredundant helper set: all wirings, shape, and the verdict of wsolve (general kernel,
random tau modulo 2^61-1, the 576 renamings of inputs and outputs, stop at the first YES).
A helper set is SPECIAL if none of its wirings is of the class.
usage: pool9.py m seconds [seed]"""
import sys, itertools, random, time
import wsolve
from wsolve import solve, solve_branch
m = int(sys.argv[1]); budget = float(sys.argv[2]); random.seed(int(sys.argv[3]) if len(sys.argv) > 3 else 5)
NP = 4 + m + 4; T0 = 4 + m
def norm(v):
    f = next(x for x in v if x); return tuple(x * f for x in v)
E = [tuple(int(i == j) for j in range(4)) for i in range(4)]
R = [tuple((-1) ** bin(w & x).count('1') for x in range(4)) for w in range(4)]
pool = sorted(set(norm(v) for v in itertools.product((0, 1, -1), repeat=4) if any(v)) - set(E) - set(R))
ALL = E + pool + R                    # indices: 0-3 inputs, 4..4+len(pool)-1 pool, last four rows
nA = len(ALL)
def coll3(u, v, w):
    for i, j, k in ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)):
        if u[i] * (v[j] * w[k] - v[k] * w[j]) - u[j] * (v[i] * w[k] - v[k] * w[i]) + u[k] * (v[i] * w[j] - v[j] * w[i]): return False
    return True
COL = {}
for a in range(nA):
    for b in range(a + 1, nA):
        for c in range(4, nA):
            if c != a and c != b and coll3(ALL[a], ALL[b], ALL[c]): COL.setdefault(c, []).append((a, b))
COLS = {c: set(v) for c, v in COL.items()}
RI = list(range(nA - 4, nA)); PI = list(range(4, nA - 4))
PERMS = list(itertools.permutations(range(4)))
def canon_shape(w, nodes):
    best = None
    for pi in PERMS:
        lab = {i: 'abcd'[pi[i]] for i in range(4)}
        def ex(h):
            if h in lab: return lab[h]
            a, b = ex(w[h][0]), ex(w[h][1])
            lab[h] = '(' + (a + b if a < b else b + a) + ')'
            return lab[h]
        key = tuple(sorted(('T' if h in RI else 'h') + ex(h) for h in nodes))
        if best is None or key < best: best = key
    return best
FR = [(list(s), list(r)) for s in PERMS for r in PERMS]
verdict = {}
def is_class(w, nodes):
    # topological order
    done = set(range(4)); order = []; rest = list(nodes)
    while rest:
        for c in rest:
            if w[c][0] in done and w[c][1] in done: order.append(c); done.add(c); rest.remove(c); break
    nm = lambda n: 'x%d' % n if n < 4 else ('T%d' % n if n in RI else 'h%d' % n)
    gates = [(nm(c), nm(w[c][0]), nm(w[c][1])) for c in order]; out = {nm(RI[i]): i for i in range(4)}
    fr = FR[:]; random.shuffle(fr); res = []
    for prime, tau in ((31, 3), (37, 5)):
        wsolve.P = prime; und = 0; got = 'special'
        if (prime, tau) == (31, 3) and solve_branch(4, gates, out, prime - 1) != 'YES': return 'CONTROL-FAILED', 0
        for s, r in fr:
            q = solve_branch(4, gates, out, tau, s, r)
            if q == 'YES': got = 'class'; break
            if q == 'UNDECIDED': und += 1
        if got == 'special' and und: got = 'undecided'
        res.append(got)
    return (res[0] if res[0] == res[1] else 'undecided'), res
t0 = time.time(); nsets = nirr = 0; stats = {'class': 0, 'special': 0, 'undecided': 0, 'CONTROL-FAILED': 0}; SPEC = {}; shapes = set(); tested = 0
subsets = list(itertools.combinations(PI, m)); random.shuffle(subsets)
for S in subsets:
    if time.time() - t0 > budget: break
    nsets += 1; pts = list(range(4)) + list(S) + RI; pset = set(pts)
    opts = {c: [ab for ab in COL.get(c, ()) if ab[0] in pset and ab[1] in pset] for c in pts[4:]}
    def reach(drop=None):
        done = set(range(4)); ch = True
        while ch:
            ch = False
            for c in pts[4:]:
                if c in done or c == drop: continue
                for a, b in opts[c]:
                    if a in done and b in done: done.add(c); ch = True; break
        return done
    if len(reach()) < NP: continue
    if any(all(t in reach(h) for t in RI) for h in S): continue
    nirr += 1
    nodes = pts[4:]; ws = []
    for choice in itertools.product(*[opts[c] for c in nodes]):
        w = dict(zip(nodes, choice)); done = set(range(4)); ch = True
        while ch:
            ch = False
            for c in nodes:
                if c not in done and w[c][0] in done and w[c][1] in done: done.add(c); ch = True
        if len(done) == NP: ws.append(w)
        if len(ws) >= 300: break
    res = 'special'; cs = []
    for w in ws:
        c = canon_shape(w, nodes); cs.append(c); shapes.add(c)
        if c not in verdict: verdict[c] = is_class(w, nodes)[0]; tested += 1
        if verdict[c] == 'class': res = 'class'; break
        if verdict[c] in ('undecided', 'CONTROL-FAILED') and res == 'special': res = 'undecided'
    stats[res] += 1
    if res != 'class':
        k = min(cs); SPEC.setdefault((res, k), [0, S, ws[cs.index(k)]]); SPEC[(res, k)][0] += 1
print('pool of %d wires with entries 0, +1, -1; m=%d helpers (%d gates): %d of %d helper sets examined in %.0f s; %d irredundant: %d of the class, %d SPECIAL, %d undecided; shapes met %d, shapes tested with wsolve %d'
      % (len(pool), m, 4 + m, nsets, len(subsets), time.time() - t0, nirr, stats['class'], stats['special'], stats['undecided'], len(shapes), tested), flush=True)
print('verdicts by shape:', {v: sum(1 for x in verdict.values() if x == v) for v in ('class', 'special', 'undecided', 'CONTROL-FAILED')})
for i, ((res, k), (n, S, w)) in enumerate(sorted(SPEC.items(), key=lambda kv: -kv[1][0])[:40]):
    print('%s kind %d: %d sets; specimen helpers %s' % (res.upper(), i, n, [ALL[h] for h in S]))
    print('    ' + ' | '.join('%s%s<-(%s,%s)' % ('T' if c in RI else 'h', ALL[c], ALL[w[c][0]], ALL[w[c][1]]) for c in sorted(w)))
