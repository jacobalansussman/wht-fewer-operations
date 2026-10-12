#!/usr/bin/env python3
"""ruling256.py [ad-1-linesums]  The second relation of the brief, at 256 points (aa-cross ran it at 16 points only).
CLAIM: the zero set of the quadric Q = y1 y2 + y3 y4 + y5 y6 + y7 y8 (136 addresses) is the union of 9 subspaces of 4 bits
that meet pairwise only in 0, and then on all 256 addresses
    (-1)^Q(z) = -1 + 2 * (number of the 9 subspaces containing z) - 16 * [z = 0].
Exact, whole numbers.  Also: are the 9 subspaces part of a spread (17 subspaces covering everything), and is each one its own
perpendicular for the bit dot product after the relabelling that turns Q's pairing into the dot product."""
import itertools, sys
K = 8; N = 256
def Q(z): return ((z & 1) * ((z >> 1) & 1) + ((z >> 2) & 1) * ((z >> 3) & 1) + ((z >> 4) & 1) * ((z >> 5) & 1) + ((z >> 6) & 1) * ((z >> 7) & 1)) & 1
def B(u, v): return Q(u ^ v) ^ Q(u) ^ Q(v)
sing = [z for z in range(1, N) if Q(z) == 0]
print("singular non-zero addresses:", len(sing), " zeros of Q in all:", len(sing) + 1)
gens = set()
def span_add(S, v): return S | frozenset(s ^ v for s in S)
def grow(S, last, d):
    if d == 4: gens.add(S); return
    for v in sing:
        if v <= last or v in S: continue
        if all(B(v, s) == 0 for s in S):
            grow(span_add(S, v), v, d + 1)
grow(frozenset([0]), 0, 0)
gens = sorted(gens, key=sorted)
print("totally singular subspaces of 4 bits:", len(gens))
G = len(gens)
disj = [[len(gens[a] & gens[b]) == 1 for b in range(G)] for a in range(G)]
best = []
def clique(cur, cand):
    global best
    if len(cur) > len(best): best = cur[:]
    if len(best) >= 9: return
    if len(cur) + len(cand) <= len(best): return
    for i, c in enumerate(cand):
        clique(cur + [c], [d for d in cand[i + 1:] if disj[c][d]])
        if len(best) >= 9: return
clique([], list(range(G)))
print("largest family found of such subspaces meeting pairwise in 0:", len(best))
fam = [gens[i] for i in best]
cover = set().union(*fam)
print("their union is the zero set of Q:", cover == set(sing) | {0})
ok = all((-1) ** Q(z) == -1 + 2 * sum(z in S for S in fam) - 16 * (z == 0) for z in range(N))
print("identity (-1)^Q(z) = -1 + 2 * (number of subspaces containing z) - 16 * [z = 0] on all 256 addresses:", ok)
# perpendicular for the form B: each totally singular 4-space is its own B-perpendicular
selfperp = all(sorted(z for z in range(N) if all(B(z, s) == 0 for s in S)) == sorted(S) for S in fam)
print("each of the 9 is its own perpendicular for Q's pairing:", selfperp)
# can the 9 be completed to a spread (8 more subspaces of 4 bits covering the 120 remaining addresses, pairwise meeting in 0)?
rest = [z for z in range(1, N) if z not in cover]
print("addresses left over:", len(rest), "(a spread would need 8 more subspaces of 15 non-zero addresses each)")
