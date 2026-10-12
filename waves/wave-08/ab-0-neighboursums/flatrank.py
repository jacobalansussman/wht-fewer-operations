#!/usr/bin/env python3
"""flatrank.py -- exact, integers only.  'Signed flat' = a function on the k-bit addresses that is +1/-1 on an affine
subspace F (a coset of a subspace V) following a character (-1)^(a.z), and 0 elsewhere.  Convolution with it costs fewer
than N gates in count (G) whatever the dimension of F (one signed sum per coset of V).
Question: the least number r(k) of signed flats whose combination is the indicator of E = {e_1..e_k} (the k unit
addresses), i.e. neighbour sums as a sum of r coset sums.  E lies in the odd-weight hyperplane, an affine space of
dimension k-1 in which E is an affine basis; so we work in F_2^(k-1) with E = {0, e_1, .., e_(k-1)}.
This program decides r(k) <= 1 and r(k) <= 2 exhaustively.   usage: flatrank.py k
"""
import sys, itertools
from fractions import Fraction
k = int(sys.argv[1]); n = k - 1; P = 1 << n
E = [0] + [1 << j for j in range(n)]
Emask = sum(1 << z for z in E)

def span(basis):
    S = {0}
    for b in basis: S |= {s ^ b for s in S}
    return S

def subspaces():
    seen = set(); out = []
    def rec(basis, S, start):
        key = frozenset(S)
        if key in seen: return
        seen.add(key); out.append(sorted(S))
        for v in range(1, P):
            if v not in S: rec(basis + [v], S | {s ^ v for s in S}, v)
    rec([], {0}, 0)
    return out

subs = subspaces()
flats = []            # (support mask, list of (point, sign))
for V in subs:
    Vs = set(V); reps = []; cov = set()
    for z in range(P):
        if z not in cov: reps.append(z); cov |= {z ^ v for v in V}
    # characters on V up to those trivial on V: take a in a set of representatives giving distinct restrictions
    seenres = set()
    for a in range(P):
        res = tuple(bin(a & v).count('1') & 1 for v in V)
        if res in seenres: continue
        seenres.add(res)
        for b in reps:
            pts = [(b ^ v, -1 if bin(a & v).count('1') & 1 else 1) for v in V]
            flats.append((sum(1 << z for z, _ in pts), dict(pts)))
print('k', k, 'points', P, 'subspaces', len(subs), 'signed flats (up to overall sign)', len(flats))
r1 = [f for f in flats if f[0] == Emask]
print('r <= 1:', bool(r1))
hits = 0; cand = 0
for i in range(len(flats)):
    S1, f1 = flats[i]
    for j in range(i + 1, len(flats)):
        S2, f2 = flats[j]
        if (S1 ^ S2) & ~Emask or Emask & ~(S1 | S2): continue      # a point covered once must be in E; E must be covered
        cand += 1
        # solve c1 f1 + c2 f2 = 1_E exactly: use two points, then verify all
        pts = [z for z in range(P) if (S1 | S2) >> z & 1]
        sol = None
        for z1, z2 in itertools.combinations(pts, 2):
            a, b = f1.get(z1, 0), f2.get(z1, 0); c, d = f1.get(z2, 0), f2.get(z2, 0); det = a * d - b * c
            if det:
                t1 = 1 if z1 in E else 0; t2 = 1 if z2 in E else 0
                sol = (Fraction(t1 * d - b * t2, det), Fraction(a * t2 - t1 * c, det)); break
        if sol and all(sol[0] * f1.get(z, 0) + sol[1] * f2.get(z, 0) == (1 if z in E else 0) for z in range(P)):
            hits += 1
            if hits <= 3: print('  two flats:', sol, sorted(f1.items()), sorted(f2.items()))
print('r <= 2: support candidates', cand, 'exact solutions', hits)
