#!/usr/bin/env python3
"""g-7-thirdturn / inplace4b.py -- as inplace4.py, but (1) states are NOT reduced by row order (so a program can be read off),
(2) forward search over gate TOPOLOGIES with rational coefficients from a pool, exact Fractions: depth-first with a
meet-in-the-middle table of everything reachable from the targets in 3 backward gates.  Count (G), no extra wire.
usage: inplace4b.py <forward depth> <backward depth>
"""
import sys, itertools
from fractions import Fraction as F
n = 4; FD = int(sys.argv[1]); BD = int(sys.argv[2])
POOL = [F(1), F(-1), F(2), F(-2), F(1, 2), F(-1, 2)]
def canon(rows):
    out = []
    for r in rows:
        f = next(x for x in r if x != 0); out.append(tuple(x / f for x in r))
    return tuple(sorted(out))
def step(st, i, k, c):
    r = tuple(a + c * b for a, b in zip(st[i], st[k]))
    if not any(r): return None
    return st[:i] + (r,) + st[i + 1:]
I = tuple(tuple(F(int(a == b)) for b in range(n)) for a in range(n))
S = [[1, 1, 1, 1], [1, 1, -1, -1], [1, -1, 1, -1], [1, -1, -1, 1]]
OPS = [(i, k, c) for i in range(n) for k in range(n) if i != k for c in POOL]
# backward table: canonical states from which a target is reached in <= BD gates
back = {}
front = {}
for perm in itertools.permutations(range(n)):
    for d in itertools.product([F(1), F(-1), F(2), F(1, 2)], repeat=n):
        t = tuple(tuple(F(S[i][perm[k]]) * d[k] for k in range(n)) for i in range(n)); c = canon(t)
        if c not in back: back[c] = []; front[c] = t
print("targets (classes up to row scaling and order):", len(back), flush=True)
cur = dict(front)
for b in range(BD):
    nx = {}
    for c, st in cur.items():
        for (i, k, co) in OPS:
            # undo a gate: the state before a gate x_i <- x_i + co*x_k is obtained by x_i <- x_i - co*x_k
            s2 = step(st, i, k, -co)
            if s2 is None: continue
            c2 = canon(s2)
            if c2 not in back: back[c2] = back[c] + [(i, k, co)]; nx[c2] = s2
    cur = nx; print("backward depth %d: %d classes" % (b + 1, len(back)), flush=True)
# forward
seen = {canon(I): []}; cur = {canon(I): I}; hit = None
if canon(I) in back: hit = ([], back[canon(I)])
for f in range(FD):
    nx = {}
    for c, st in cur.items():
        for (i, k, co) in OPS:
            s2 = step(st, i, k, co)
            if s2 is None: continue
            c2 = canon(s2)
            if c2 in seen: continue
            seen[c2] = seen[c] + [(i, k, co)]; nx[c2] = s2
            if c2 in back and hit is None: hit = (seen[c2], back[c2], s2)
    cur = nx; print("forward depth %d: %d classes; meet: %s" % (f + 1, len(seen), hit is not None), flush=True)
    if hit: break
if hit:
    fwd, bwd, mid = hit
    print("in-place program found, %d + %d gates (forward part, then the backward part in the order it must be applied):" % (len(fwd), len(bwd)))
    print("  forward:", [(i, k, str(c)) for i, k, c in fwd]); print("  backward chain (as stored):", [(i, k, str(c)) for i, k, c in bwd])
    print("  middle state rows:", [[str(x) for x in r] for r in mid])
else:
    print("no in-place program with <= %d gates and coefficients in the pool" % (FD + BD))
