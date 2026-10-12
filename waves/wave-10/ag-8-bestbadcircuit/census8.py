#!/usr/bin/env python3
"""census8.py (ag-8-bestbadcircuit): ALL circuits (count G) with 4 + m gates for the 4-point kernel square K (x) K, K = [[1,1],[1,tau]],
over GF(p), that are IRREDUNDANT (no helper can be left out), sorted by wiring SHAPE; then which shapes exist at tau = -1 and at no
generic tau (SPECIAL), and the reverse.
Input: files s<m>_<p>_<tau>.txt = output of p-0's mincirc_sets p 4 m (every set of m helper points after which all four rows are made).
A circuit = 4 inputs, m helpers, 4 targets (points up to scale); every non-input point lies on the line through two points made earlier.
WIRING = for each non-input point WHICH two points it reads (every acyclic choice is listed).  SHAPE = wiring with the names forgotten
(inputs, helpers, targets renamed within their kind).  Canonical form: least over the 4! x 4! renamings of inputs and targets of the
sorted list of gates, a helper being named by the expression of what it reads.
usage: census8.py p m tauH tau1 tau2 ..."""
import sys, itertools, os
p = int(sys.argv[1]); m = int(sys.argv[2]); taus = [int(t) for t in sys.argv[3:]]
NP = 4 + m + 4
def canon_pt(v):
    f = next(x for x in v if x); iv = pow(f, -1, p); return tuple(x * iv % p for x in v)
def rows(tau): return [tuple(pow(tau, bin(w & x).count('1'), p) for x in range(4)) for w in range(4)]
def coll(u, v, w):
    M = [list(u), list(v), list(w)]; r = 0
    for c in range(4):
        pv = next((i for i in range(r, 3) if M[i][c] % p), None)
        if pv is None: continue
        M[r], M[pv] = M[pv], M[r]; iv = pow(M[r][c], -1, p)
        for i in range(r + 1, 3):
            f = M[i][c] * iv % p
            if f: M[i] = [(a - f * b) % p for a, b in zip(M[i], M[r])]
        r += 1
    return r <= 2
E = [tuple(int(i == j) for j in range(4)) for i in range(4)]
PERMS = list(itertools.permutations(range(4)))
def load(m_, tau):
    fn = 's%d_%d_%d.txt' % (m_, p, tau)
    return [tuple(sorted(tuple(int(x) for x in s.split(',')) for s in line.split()[1:])) for line in open(fn) if line.startswith('SET')]
def options(pts):
    """for each non-input point the pairs it is collinear with."""
    n = len(pts); opts = {}
    for c in range(4, n):
        opts[c] = [(a, b) for a in range(n) for b in range(a + 1, n) if a != c and b != c and coll(pts[a], pts[b], pts[c])]
    return opts
def reach(opts, n, drop=None):
    """closure: which points can be made, when point `drop` is not allowed."""
    done = set(range(4)); ch = True
    while ch:
        ch = False
        for c in range(4, n):
            if c in done or c == drop: continue
            if any(a in done and b in done for a, b in opts[c]): done.add(c); ch = True
    return done
def wirings(opts, n):
    nodes = list(range(4, n)); out = []
    for choice in itertools.product(*[opts[c] for c in nodes]):
        w = dict(zip(nodes, choice)); done = set(range(4)); ch = True
        while ch:
            ch = False
            for c in nodes:
                if c not in done and w[c][0] in done and w[c][1] in done: done.add(c); ch = True
        if len(done) == n: out.append(w)
    return out
TWINS = [0]
def canon_shape(w):
    """nodes 0..3 inputs, 4..4+m-1 helpers, the last four targets.  Every node is named by the expression of what it reads, down to
    the inputs; the shape is the least, over the 4! renamings of the inputs, of the sorted list of (kind, expression).  Two nodes
    with the same expression (twins: two different points made from the same pair) are counted in TWINS."""
    best = None; T0 = 4 + m
    for pi in PERMS:
        lab = {i: 'abcd'[pi[i]] for i in range(4)}
        def ex(h):
            if h in lab: return lab[h]
            a, b = ex(w[h][0]), ex(w[h][1])
            lab[h] = '(' + (a + b if a < b else b + a) + ')'
            return lab[h]
        key = tuple(sorted(('T' if h >= T0 else 'h') + ex(h) for h in range(4, NP)))
        if best is None or key < best: best = key
    if len(set(best)) < len(best): TWINS[0] += 1
    return best
table = {}; reps = {}; stats = {}
for tau in taus:
    R = [canon_pt(r) for r in rows(tau)]
    sets = load(m, tau); sets = sorted(set(sets))
    small = set(load(m - 1, tau)) if os.path.exists('s%d_%d_%d.txt' % (m - 1, p, tau)) else set()
    irr = []; nred_quick = 0
    for S in sets:
        if any(tuple(x for j, x in enumerate(S) if j != i) in small for i in range(m)): nred_quick += 1; continue
        pts = E + list(S) + R
        if len(set(pts)) < NP: continue
        opts = options(pts)
        if any(len(reach(opts, NP, drop=h)) >= NP - 1 and all(t in reach(opts, NP, drop=h) for t in range(4 + m, NP)) for h in range(4, 4 + m)): continue
        irr.append((S, pts, opts))
    shapes = {}; nw = 0; cache = {}
    print('  tau=%d: %d sets, %d left after the quick filter, %d irredundant' % (tau, len(sets), len(sets) - nred_quick, len(irr)), flush=True)
    for S, pts, opts in irr:
        for w in wirings(opts, NP):
            nw += 1
            c = canon_shape(w)
            shapes[c] = shapes.get(c, 0) + 1
            reps.setdefault(c, {}).setdefault(tau, (pts, w))
    table[tau] = shapes; stats[tau] = (len(sets), len(irr), nw, len(shapes))
    print('p=%d tau=%d: %d helper sets, %d irredundant, %d wirings, %d shapes' % (p, tau, len(sets), len(irr), nw, len(shapes)), flush=True)
tH = taus[0]; gen = taus[1:]
allshapes = sorted(set().union(*[set(t) for t in table.values()]))
names = {c: 'S%03d' % i for i, c in enumerate(allshapes)}
special = [c for c in allshapes if c in table[tH] and all(c not in table[t] for t in gen)]
common = [c for c in allshapes if c in table[tH] and all(c in table[t] for t in gen)]
mixed = [c for c in allshapes if c in table[tH] and c not in special and c not in common]
rev = [c for c in allshapes if c not in table[tH]]
print('\nshapes at tau=%d (the transform): %d ; in every generic tau too: %d ; in some generic tau only: %d ; SPECIAL (no generic tau): %d' % (tH, len(table[tH]), len(common), len(mixed), len(special)))
print('shapes absent at the transform, present at a generic tau: %d' % len(rev), [(names[c], [t for t in gen if c in table[t]]) for c in rev][:40])
def show(c, tau):
    pts, w = reps[c][tau]
    return ' | '.join('%s%d=%s<-(%d,%d)' % ('h' if n < 4 + m else 'T', n, ','.join(map(str, pts[n])), w[n][0], w[n][1]) for n in sorted(w))
print('twin cases met:', TWINS[0])
print('\nSPECIAL shapes, one labelled specimen each (points modulo %d; nodes 0-3 inputs, then helpers h, then targets T = rows 00,01,10,11):' % p)
for c in special: print(names[c], 'wirings at tau=%d: %d' % (tH, table[tH][c]), '\n   ', show(c, tH), '\n    canon', c)
print('\nMIXED shapes (present at the transform and at some but not all generic tau):')
for c in mixed: print(names[c], {t: table[t].get(c, 0) for t in taus}, '\n   ', show(c, tH))
print('\nCOMMON shapes: number of wirings per tau')
for c in common: print(names[c], {t: table[t].get(c, 0) for t in taus})
print('\nshapes absent at the transform, specimens:')
for c in rev[:12]:
    t = next(t for t in gen if c in table[t]); print(names[c], 'tau', t, '\n   ', show(c, t))
