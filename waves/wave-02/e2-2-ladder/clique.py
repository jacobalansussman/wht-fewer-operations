#!/usr/bin/env python3
"""clique.py m W z:n ...  -- the clique lemma applied to a count vector.  Exact.  [e2-2-ladder]
Clique lemma (e2-2.md, section 2; old letters, ANY number of scratch arrays): call a form q with q(I) = 1 'tight' if it
selects exactly W moves.  A set of moves, any two of which are selected together by some tight form, has at most W members.
(For such a set the W-by-W products w_i.u_j form a triangular matrix with ones on the diagonal, of rank = its size, inside a
matrix of rank at most W.)
This program builds the graph 'selected together by a tight form' on the moves and finds its largest clique.
Two moves in the same direction are selected by the same forms, so they are joined whenever that direction is in a tight form.
"""
import sys, itertools
m = int(sys.argv[1]); W = int(sys.argv[2])
moves = []
for tok in sys.argv[3:]:
    z, n = tok.strip(",").split(":"); moves += [int(z, 2)] * int(n)
k = len(moves)
pairs = [(i, j) for i in range(m) for j in range(i, m)]
diagbits = [t for t, (i, j) in enumerate(pairs) if i == j]
monmask = [sum(((z >> i & 1) & (z >> j & 1)) << t for t, z in enumerate(moves)) for (i, j) in pairs]
seen = set(); adj = [0] * k; tight = 0; minsel = k; bad = 0
for Q in range(1, 1 << len(pairs)):
    if sum(Q >> t & 1 for t in diagbits) & 1 == 0: continue
    sel = 0
    for t in range(len(pairs)):
        if Q >> t & 1: sel ^= monmask[t]
    if sel in seen: continue
    seen.add(sel)
    c = bin(sel).count("1"); minsel = min(minsel, c)
    if c < W: bad += 1
    if c == W:
        tight += 1
        for i in range(k):
            if sel >> i & 1: adj[i] |= sel & ~(1 << i)
best = 0
def bk(R, P, X):
    global best
    if P == 0 and X == 0:
        best = max(best, bin(R).count("1")); return
    if bin(R).count("1") + bin(P).count("1") <= best: return
    pv = (P | X); u = pv.bit_length() - 1
    cand = P & ~adj[u]
    while cand:
        v = cand & -cand; i = v.bit_length() - 1
        bk(R | v, P & adj[i], X & adj[i])
        P &= ~v; X |= v; cand &= ~v
bk(0, (1 << k) - 1, 0)
edges = sum(bin(a).count("1") for a in adj) // 2
print("m = %d, W = %d, %d moves (plain %d): %s" % (m, W, k, m * W, " ".join(sys.argv[3:])))
print("  fewest moves selected by a form with q(I) = 1: %d (%s); tight selections: %d; pairs joined: %d of %d; largest clique: %d"
      % (minsel, "feasible for counting" if bad == 0 else "NOT feasible", tight, edges, k * (k - 1) // 2, best))
print("  -> %s" % ("EXCLUDED by the clique lemma (clique %d > W = %d), scratch arrays or not" % (best, W) if best > W else "not excluded by the clique lemma"))
