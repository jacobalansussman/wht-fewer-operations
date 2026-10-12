#!/usr/bin/env python3
"""r2_shapes.py (r-2): my own census of 7-gate circuits at 4 points over GF(p): helper sets from r2_brute (independent of mincirc),
wirings and shapes by my own code.  Wiring = which two wires each of the 7 gates reads; shape = wiring up to renaming inputs,
helpers and outputs within their kind (least sorted gate list over the 4! * 3! * 4! renamings: the same DEFINITION as p-0, so that
the lists can be compared, other code).  usage: r2_shapes.py p B tau...   writes reps_p<p>.json (one named wiring per shape and tau)."""
import sys, subprocess, itertools, os, json, re
here = os.path.dirname(os.path.abspath(__file__))
p = int(sys.argv[1]); B = sys.argv[2]; taus = [int(t) for t in sys.argv[3:]]
def rows(t): return [[pow(t, bin(w & x).count('1'), p) for x in range(4)] for w in range(4)]
def canon(v):
    iv = pow(next(x for x in v if x), -1, p); return tuple(x * iv % p for x in v)
def collinear(a, b, c):
    # three distinct points of projective 3-space: all 3 x 3 minors of the 3 x 4 matrix vanish
    for i, j, k in ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)):
        d = (a[i] * (b[j] * c[k] - b[k] * c[j]) - a[j] * (b[i] * c[k] - b[k] * c[i]) + a[k] * (b[i] * c[j] - b[j] * c[i])) % p
        if d: return False
    return True
REL = [list(a) + [4 + x for x in b] + [7 + x for x in c] for a in itertools.permutations(range(4)) for b in itertools.permutations(range(3)) for c in itertools.permutations(range(4))]
cache = {}
def shape(w):
    key = tuple(sorted(w.items()))
    if key not in cache:
        best = None
        for m in REL:
            s = sorted((m[c], min(m[a], m[b]), max(m[a], m[b])) for c, (a, b) in key)
            if best is None or s < best: best = s
        cache[key] = tuple(best)
    return cache[key]
def acyclic(w):
    done = set(range(4)); ch = True
    while ch:
        ch = False
        for n, (a, b) in w.items():
            if n not in done and a in done and b in done: done.add(n); ch = True
    return len(done) == 11
E = [tuple(int(i == j) for j in range(4)) for i in range(4)]
table = {}; reps = {}
for t in taus:
    R = [canon(r) for r in rows(t)]
    inp = '\n'.join(' '.join(map(str, r)) for r in rows(t)) + '\n'
    out = subprocess.run([os.path.join(here, 'r2_brute'), str(p), '4', '3', B, '1'], input=inp, capture_output=True, text=True).stdout
    sets = [[tuple(int(x) for x in s.split(',')) for s in line.split()[1:]] for line in out.splitlines() if line.startswith('SET')]
    sh = {}; nw = 0; hubless = 0
    for S in sets:
        pts = E + S + R
        if all(sum(1 for x in h if x) < 4 for h in S): hubless += 1
        opts = [[(a, b) for a in range(11) for b in range(a + 1, 11) if a != n and b != n and collinear(pts[a], pts[b], pts[n])] for n in range(4, 11)]
        for ch in itertools.product(*opts):
            w = dict(zip(range(4, 11), ch))
            if not acyclic(w): continue
            nw += 1; c = shape(w); sh[c] = sh.get(c, 0) + 1
            reps.setdefault(' '.join('%d<-(%d,%d)' % g for g in c), {}).setdefault(str(t), [[list(x) for x in pts], sorted([n, a, b] for n, (a, b) in w.items())])
    table[t] = sh
    print('p=%d tau=%d: %d helper sets (%d without a hub), %d wirings, %d shapes' % (p, t, len(sets), hubless, nw, len(sh)), flush=True)
allsh = set().union(*[set(s) for s in table.values()])
names = {c: ' '.join('%d<-(%d,%d)' % g for g in c) for c in allsh}
print('shapes in all: %d' % len(allsh))
for c in sorted(allsh):
    pres = [t for t in taus if c in table[t]]
    if len(pres) < len(taus): print('  not at every tau tried:', names[c], ' present at tau =', pres, ' wirings', [table[t][c] for t in pres])
m1 = p - 1
if m1 in table:
    print('shapes at tau = -1 that are missing at some other tau tried:', [names[c] for c in table[m1] if any(c not in table[t] for t in taus)] or 'none')
    print('wirings per shape at tau = -1 divided by the same at tau = %d:' % taus[0], sorted(set((table[m1][c], table[taus[0]].get(c, 0)) for c in table[m1])))
# compare with p-0's printed list
f = os.path.join(here, '..', 'p-0-classtest', 'census4_p%d.out' % p)
if os.path.exists(f):
    theirs = set(re.sub(r'^S\d\d ', '', l.strip()) for l in open(f) if re.match(r'^S\d\d \d+<-', l))
    mine = set(names.values())
    print("p-0's list of shapes at this prime: %d; mine: %d; in both: %d; only theirs: %d; only mine: %d" % (len(theirs), len(mine), len(theirs & mine), len(theirs - mine), len(mine - theirs)))
json.dump({'p': p, 'taus': taus, 'reps': reps}, open(os.path.join(here, 'reps_p%d.json' % p), 'w'))
