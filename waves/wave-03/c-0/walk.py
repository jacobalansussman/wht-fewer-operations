#!/usr/bin/env python3
"""c-0 walk.py: my own exact minimum of g-1's model "one merge tree plus flip walk" at 8 points, count (G).
Model (as g-1 states it): fix a sign vector F0 and a chain  pairs < fours < all  of cosets of subgroups of the addresses.
7 gates build F0 and leave the wires "F0 on A" for the 4 pairs and the 2 fours.  Then walk among full sign vectors (a wire
is a vector up to scale, so v and -v are one wire): a step flips one input, or flips a pair or a four on which the current
vector equals F0 up to sign.  One gate per new wire.  All 8 characters must be reached.
In the coordinates D = {places where the wire differs from F0}, D and its complement are the same wire.
gates = 7 + (edges of the smallest tree containing D = empty and the 8 characters) : a Steiner tree, solved exactly
by the Dreyfus-Wagner recursion (8 terminals, 128 vertices).  All chains are equivalent under the linear maps of the
addresses (they permute the characters), so one chain and all 128 sign vectors F0 (modulo sign) is the whole model."""
import heapq, sys
from collections import Counter

FULL = 255
def canon(D): return min(D, FULL ^ D)
PAIRS = [0b00000011, 0b00001100, 0b00110000, 0b11000000]      # cosets of {0,1}
FOURS = [0b00001111, 0b11110000]                              # cosets of {0,1,2,3}
NODES = PAIRS + FOURS
VERT = sorted({canon(D) for D in range(256)}); IDX = {D: i for i, D in enumerate(VERT)}
ADJ = []
for D in VERT:
    nb = set()
    for p in range(8): nb.add(IDX[canon(D ^ (1 << p))])
    for A in NODES:
        if (A & D) == A or (A & D) == 0: nb.add(IDX[canon(D ^ A)])
    nb.discard(IDX[D]); ADJ.append(sorted(nb))
NV = len(VERT)

def relax(d):
    """d: list of start costs; returns shortest-path closure (unit edges)"""
    d = d[:]; h = [(c, v) for v, c in enumerate(d) if c < 10 ** 9]; heapq.heapify(h)
    while h:
        c, v = heapq.heappop(h)
        if c > d[v]: continue
        for u in ADJ[v]:
            if c + 1 < d[u]: d[u] = c + 1; heapq.heappush(h, (c + 1, u))
    return d

def steiner(terms, root):
    T = len(terms); INF = 10 ** 9
    dp = [None] * (1 << T)
    for i, t in enumerate(terms):
        d = [INF] * NV; d[t] = 0; dp[1 << i] = relax(d)
    for S in range(1, 1 << T):
        if S & (S - 1) == 0: continue
        m = [INF] * NV
        low = S & -S; sub = (S - 1) & S
        while sub:
            if sub & low:                                  # each split once
                a, b = dp[sub], dp[S ^ sub]
                m = [x if x <= y + z else y + z for x, y, z in zip(m, a, b)]
            sub = (sub - 1) & S
        dp[S] = relax(m)
    return dp[(1 << T) - 1][root]

def chi(j, x): return 1 if bin(j & x).count("1") & 1 else 0
res = Counter(); best = []
for f in range(128):                                           # F0 as a 0/1 function, f(7)=0 fixes the sign
    terms = sorted({IDX[canon(sum(((chi(j, x) ^ ((f >> x) & 1)) << x) for x in range(8)))] for j in range(8)})
    e = steiner(terms, IDX[0])
    g = 7 + e; res[g] += 1
    if g <= 19: best.append(f)
print("one chain, all 128 centres modulo sign: exact minimum gate count -> number of centres:", sorted(res.items()))
print("minimum of the model:", min(res), "; centres reaching it (0/1 truth tables, bit x = value at address x):", [format(f, "08b") for f in best])
