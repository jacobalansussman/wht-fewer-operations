#!/usr/bin/env python3
"""compose.py [ad-3]  The first two exchanges of the 4-exchange path (k6_S2500_p1.out) go along the same u = 11.
Together they are ONE exchange on the symmetric difference of the two flats.  Is that set a union of 2 or 3 flats
(each unchanged by adding u)?  Exact, 64 points.  Then replay the path with the merged exchange."""
from itertools import combinations
u = 11; T1 = 0x1284482184122148; T2 = 0x6060606090909090
pts = lambda m: [y for y in range(64) if m >> y & 1]
def is_flat(S):
    S = sorted(S); n = len(S)
    if n == 0 or n & (n - 1): return False
    a = S[0]; st = set(S); return all((x ^ y ^ a) in st for x in S for y in S)
I = T1 & T2; X = T1 ^ T2
print("T1 and T2 share %d addresses; the merged set has %d addresses; unchanged by u: %s" % (len(pts(I)), len(pts(X)), all((y ^ u) in set(pts(X)) for y in pts(X))))
P = pts(X); st = set(P)
# all flats inside X that are unchanged by u: grow from pairs {y, y+u}
flats = set()
frontier = set(frozenset([y, y ^ u]) for y in P)
while frontier:
    flats |= frontier; nxt = set()
    for f in frontier:
        a = min(f)
        for y in P:
            if y in f: continue
            g = frozenset(list(f) + [x ^ a ^ y for x in f])
            if g <= st and is_flat(g): nxt.add(g)
    frontier = nxt - flats
flats = sorted(flats, key=len, reverse=True)
print("flats inside the merged set, unchanged by u: %d (sizes %s)" % (len(flats), sorted(set(len(f) for f in flats))))
best = None
for c in (1, 2, 3):
    for combo in combinations(flats, c):
        if frozenset().union(*combo) == st: best = (c, combo); break
    if best: break
print("least number of flats whose union is the merged set: %s" % (best[0] if best else "more than 3"))
if best: print("   " + " | ".join(str(sorted(f)) for f in best[1]))
def exch(A, u, T): return frozenset((y ^ u) if y in T else y for y in A)
A0 = frozenset(y for y in range(64) if y & 1 == 0 and y >= 8)
A = exch(A0, 11, st); A = exch(A, 15, set(pts(0x0000500a0000500a))); A = exch(A, 2, set(pts(0x0000a00500000000)))
end = set(pts(0x27b18d1b41d71482))
print("replay with the merged exchange (3 exchanges) ends in the 4-path's quadric: %s" % (A == end))
