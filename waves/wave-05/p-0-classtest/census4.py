#!/usr/bin/env python3
"""census4.py (p-0-classtest): ALL 7-gate circuits (count G) for the 4-point kernel power K (x) K, K = [[1,1],[1,tau]], over GF(p),
sorted by WIRING SHAPE, for every tau in GF(p) except 0 and 1.
Input: mincirc_sets (d-0-zeta's exhaustive search, printing every set of 3 helper points).
A circuit = 4 inputs e0..e3, 3 helpers, 4 targets (the rows, as points up to scale); each non-input point lies on the line through
two points made earlier.  WIRING = for each of the 7 non-input points, WHICH two points it reads.  SHAPE = the wiring with all
names forgotten (inputs, helpers, targets may be renamed within their kind): computed as a canonical form by brute force.
usage: census4.py p [taus...]      prints for each tau the multiset of shapes; then the table shape x tau."""
import sys, subprocess, itertools, os
here = os.path.dirname(os.path.abspath(__file__))
p = int(sys.argv[1]); taus = [int(t) % p for t in sys.argv[2:]] or [t for t in range(2, p)]
def canon_pt(v):
    f = next(x for x in v if x); iv = pow(f, -1, p); return tuple(x * iv % p for x in v)
def rows(tau): return [tuple(pow(tau, bin(w & x).count('1'), p) for x in range(4)) for w in range(4)]
def on_line(w, u, v):
    # is w in span(u, v)?  rank of 3 x 4 matrix <= 2 over GF(p)
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
PERM_I = list(itertools.permutations(range(4))); PERM_M = list(itertools.permutations(range(3)))
RELAB = [list(pi) + [4 + x for x in pm] + [7 + x for x in pt] for pi in PERM_I for pm in PERM_M for pt in PERM_I]
def canon_shape(w):
    """w: dict node -> (a, b) with nodes 0..3 inputs, 4..6 helpers, 7..10 targets.  EXACT canonical form: the least sorted
    gate list over all 4! * 3! * 4! renamings within kinds."""
    items = list(w.items()); best = None
    for m in RELAB:
        s = sorted((m[c], m[a], m[b]) if m[a] < m[b] else (m[c], m[b], m[a]) for c, (a, b) in items)
        if best is None or s < best: best = s
    return tuple(best)
def quick_inv(w):
    """cheap invariant used to avoid canonicalising the same wiring class many times (colour refinement, 4 rounds)."""
    kind = lambda n: 0 if n < 4 else 1 if n < 7 else 2
    col = {n: (kind(n),) for n in range(11)}
    for _ in range(4):
        new = {}
        for n in range(11):
            par = tuple(sorted(col[x] for x in w[n])) if n in w else ()
            ch = tuple(sorted(col[c] for c, ab in w.items() if n in ab))
            new[n] = (col[n], par, ch)
        ids = {v: i for i, v in enumerate(sorted(set(new.values()), key=repr))}
        col = {n: (kind(n), ids[new[n]]) for n in range(11)}
    return tuple(sorted(col.values()))
def wirings(pts):
    """all acyclic choices of a parent pair for each non-input point.  pts: list of 11 points."""
    opts = {}
    for n in range(4, 11):
        opts[n] = [(a, b) for a in range(11) for b in range(a + 1, 11) if a != n and b != n and on_line(pts[n], pts[a], pts[b])]
    out = []
    nodes = list(range(4, 11))
    for choice in itertools.product(*[opts[n] for n in nodes]):
        w = dict(zip(nodes, choice))
        # acyclic?
        done = set(range(4)); ch = True
        while ch:
            ch = False
            for n in nodes:
                if n not in done and w[n][0] in done and w[n][1] in done: done.add(n); ch = True
        if len(done) == 11: out.append(w)
    return out
table = {}; reps = {}; cache = {}
for tau in taus:
    R = [canon_pt(r) for r in rows(tau)]
    inp = '\n'.join(' '.join(map(str, r)) for r in rows(tau)) + '\n'
    res = subprocess.run([os.path.join(here, 'mincirc_sets'), str(p), '4', '3', '100000000'], input=inp, capture_output=True, text=True).stdout
    sets = [[tuple(int(x) for x in s.split(',')) for s in line.split()[1:]] for line in res.splitlines() if line.startswith('SET')]
    shapes = {}; nw = 0
    for S in sets:
        pts = E + S + R
        for w in wirings(pts):
            nw += 1
            q = tuple(sorted(w.items()))          # exact cache: the labelled wiring itself (colour refinement merged different shapes: first run, discarded)
            if q not in cache: cache[q] = canon_shape(w)
            c = cache[q]
            shapes[c] = shapes.get(c, 0) + 1
            reps.setdefault(c, {})[tau] = (pts, w)
    table[tau] = shapes
    print('p=%d tau=%d (1/tau=%d, order of tau %d): %d helper sets, %d wirings, %d shapes' % (p, tau, pow(tau, -1, p),
          next(e for e in range(1, p) if pow(tau, e, p) == 1), len(sets), nw, len(shapes)), flush=True)
allshapes = sorted(set().union(*[set(t) for t in table.values()]), key=lambda c: (-sum(c in table[t] for t in taus), c))
names = {c: 'S%02d' % i for i, c in enumerate(allshapes)}
print('\nshape x tau: number of wirings of that shape (0 = the shape does not exist for that tau over GF(%d))' % p)
print('shape  ' + ' '.join('%5d' % t for t in taus) + '   present for')
for c in allshapes:
    pres = [t for t in taus if c in table[t]]
    print(names[c] + '    ' + ' '.join('%5d' % table[t].get(c, 0) for t in taus) + '   ' + ('ALL tau' if len(pres) == len(taus) else 'tau in %s' % pres))
print('\nshapes written out (0-3 inputs, 4-6 helpers, 7-10 targets; child<-(a,b)):')
for c in allshapes: print(names[c], ' '.join('%d<-(%d,%d)' % t for t in c))
m1 = p - 1
if m1 in table:
    only = [c for c in allshapes if c in table[m1] and all(c not in table[t] for t in taus if t != m1)]
    print('\nshapes present at tau = -1 and at NO other tau over GF(%d): %s' % (p, [names[c] for c in only] or 'none'))
    notat = [c for c in allshapes if c not in table[m1]]
    print('shapes absent at tau = -1 but present at some other tau: %s' % ([(names[c], [t for t in taus if c in table[t]]) for c in notat] or 'none'))
