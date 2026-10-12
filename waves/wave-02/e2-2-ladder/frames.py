#!/usr/bin/env python3
"""frames.py m W z:n ...  -- does the frame argument exclude a count vector (old letters, NO scratch arrays)?  Exact.  [e2-2-ladder]
A form q with q(I) = 1 that selects exactly W moves forces those W reflections to commute pairwise (e2-2.md, section 2).
If the 'commute' relation so forced joins ALL moves, the unit is commuting, hence W separate schedules, hence needs m W moves.
Uses ALL quadratic forms with q(I) = 1 (not only the lightest).  Also reports whether the count vector is feasible at all.
"""
import sys, itertools
m = int(sys.argv[1]); W = int(sys.argv[2])
moves = []
for tok in sys.argv[3:]:
    z, n = tok.strip(",").split(":"); moves += [int(z, 2)] * int(n)
k = len(moves)
pairs = [(i, j) for i in range(m) for j in range(i, m)]
diagbits = [t for t, (i, j) in enumerate(pairs) if i == j]
# value of every monomial on every move
mon = [[(z >> i & 1) & (z >> j & 1) for z in moves] for (i, j) in pairs]
monmask = [sum(b << t for t, b in enumerate(row)) for row in mon]      # bitmask over moves
forced = set(); tight = 0; minsel = None; infeasible = 0; seen = set()
for Q in range(1, 1 << len(pairs)):
    if sum(Q >> t & 1 for t in diagbits) & 1 == 0: continue
    sel = 0
    for t in range(len(pairs)):
        if Q >> t & 1: sel ^= monmask[t]
    if sel in seen: continue
    seen.add(sel)
    c = bin(sel).count("1")
    minsel = c if minsel is None else min(minsel, c)
    if c < W: infeasible += 1
    if c == W:
        tight += 1
        idx = [i for i in range(k) if sel >> i & 1]
        for a, b in itertools.combinations(idx, 2): forced.add((a, b))
allpairs = k * (k - 1) // 2
print("m = %d, W = %d, %d moves (plain %d): %s" % (m, W, k, m * W, " ".join(sys.argv[3:])))
print("  distinct selections by forms with q(I) = 1: %d; fewest moves selected: %d; selections with fewer than W: %d; with exactly W (frames): %d"
      % (len(seen), minsel, infeasible, tight))
print("  pairs of moves forced to commute: %d of %d" % (len(forced), allpairs))
if infeasible: print("  -> NOT feasible for the counting condition")
elif len(forced) == allpairs and k > W: print("  -> every two moves must commute: EXCLUDED without scratch arrays (a commuting unit needs %d moves)" % (m * W))
else: print("  -> the frame argument does not exclude this count vector")
