#!/usr/bin/env python3
"""c-0 walk2.py: one push beyond g-1's exact8: the same model "one merge tree plus flip walk" at 8 points, count (G), but the
merge tree is ANY balanced tree (any perfect matching of the 8 addresses into pairs, any grouping of the 4 pairs into two
fours): 105 * 3 = 315 trees, not only the 21 made of cosets of subgroups.  The set of 8 characters is invariant under the
1344 affine maps of the addresses (up to signs, which the model ignores), so one tree per orbit is enough.
Exact Steiner tree (Dreyfus-Wagner) for all 128 centres modulo sign, per orbit representative."""
import heapq, itertools
from collections import Counter

FULL = 255
def canon(D): return min(D, FULL ^ D)
VERT = sorted({canon(D) for D in range(256)}); IDX = {D: i for i, D in enumerate(VERT)}; NV = len(VERT)

def adjacency(nodes):
    ADJ = []
    for D in VERT:
        nb = set()
        for p in range(8): nb.add(IDX[canon(D ^ (1 << p))])
        for A in nodes:
            if (A & D) == A or (A & D) == 0: nb.add(IDX[canon(D ^ A)])
        nb.discard(IDX[D]); ADJ.append(sorted(nb))
    return ADJ

def relax(d, ADJ):
    d = d[:]; h = [(c, v) for v, c in enumerate(d) if c < 10 ** 9]; heapq.heapify(h)
    while h:
        c, v = heapq.heappop(h)
        if c > d[v]: continue
        for u in ADJ[v]:
            if c + 1 < d[u]: d[u] = c + 1; heapq.heappush(h, (c + 1, u))
    return d

def steiner(terms, root, ADJ):
    T = len(terms); INF = 10 ** 9; dp = [None] * (1 << T)
    for i, t in enumerate(terms):
        d = [INF] * NV; d[t] = 0; dp[1 << i] = relax(d, ADJ)
    for S in range(1, 1 << T):
        if S & (S - 1) == 0: continue
        m = [INF] * NV; low = S & -S; sub = (S - 1) & S
        while sub:
            if sub & low:
                a, b = dp[sub], dp[S ^ sub]
                m = [x if x <= y + z else y + z for x, y, z in zip(m, a, b)]
            sub = (sub - 1) & S
        dp[S] = relax(m, ADJ)
    return dp[(1 << T) - 1][root]

def chi(j, x): return bin(j & x).count("1") & 1

# the affine group of the addresses
def lin(cols, x):
    r = 0
    for b in range(3):
        if (x >> b) & 1: r ^= cols[b]
    return r
GROUP = []
for cols in itertools.product(range(1, 8), repeat=3):
    if len({lin(cols, x) for x in range(8)}) == 8:
        for t in range(8): GROUP.append([lin(cols, x) ^ t for x in range(8)])
assert len(GROUP) == 1344
def pm(perm, mask): return sum(1 << perm[x] for x in range(8) if (mask >> x) & 1)

def matchings(pts):
    if not pts: yield []; return
    a = pts[0]
    for b in pts[1:]:
        rest = [p for p in pts if p not in (a, b)]
        for m in matchings(rest): yield [(1 << a) | (1 << b)] + m
trees = []
for m in matchings(list(range(8))):
    for k in range(1, 4):
        f1 = m[0] | m[k]; trees.append((tuple(sorted(m)), tuple(sorted((f1, FULL ^ f1)))))
assert len(trees) == 315
def key(tr, g): return (tuple(sorted(pm(g, a) for a in tr[0])), tuple(sorted(pm(g, a) for a in tr[1])))
orbits = {}
for tr in trees:
    k = min(key(tr, g) for g in GROUP); orbits.setdefault(k, []).append(tr)
print("balanced merge trees: 315 ; orbits under the 1344 affine maps:", len(orbits), "; sizes", sorted(len(v) for v in orbits.values()), flush=True)
overall = Counter()
for k, members in sorted(orbits.items(), key=lambda kv: len(kv[1])):
    pairs, fours = k; ADJ = adjacency(list(pairs) + list(fours)); res = Counter()
    for f in range(128):
        terms = sorted({IDX[canon(sum(((chi(j, x) ^ ((f >> x) & 1)) << x) for x in range(8)))] for j in range(8)})
        res[7 + steiner(terms, IDX[0], ADJ)] += 1
    coset = all(len({a ^ b for a in range(8) for b in range(8) if a < b and P == (1 << a) | (1 << b)} ) == 1 for P in pairs) and len({[a ^ b for a in range(8) for b in range(8) if a < b and P == (1 << a) | (1 << b)][0] for P in pairs}) == 1
    print("orbit of %3d trees, pairs %s fours %s%s: exact minimum -> number of centres: %s" % (
        len(members), [format(p, "08b") for p in pairs], [format(p, "08b") for p in fours], " (pairs are cosets of one subgroup)" if coset else "", sorted(res.items())), flush=True)
    overall[min(res)] += len(members)
print("minimum over all 315 balanced trees and all centres:", min(overall), "; trees by their best count:", sorted(overall.items()))
