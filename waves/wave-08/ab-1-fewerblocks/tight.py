#!/usr/bin/env python3
"""tight.py [ab-1-fewerblocks]  Exact.  Tight characters of the 'every direction once' pattern, sub-game, block size m,
W = 2^(m-2) arrays.  A quadratic form with exactly 2^(m-2) ones is the indicator of an affine subspace of codimension 2 that
misses 0; it is a constraint (<Q,I> = 1) when that subspace holds an odd number of the unit words e_i.
For such a Q exactly W moves are active and their product must be -1 on the live arrays.  With NO scratch arrays this forces
the W active moves to act through mutually annihilating rank-one projections [derived in the report].  So: if every two
directions lie together in one tight subspace, all 2^m - 1 projections annihilate each other, impossible in W dimensions."""
import itertools, sys
m = int(sys.argv[1]); N = 1 << m
par = lambda x: bin(x).count("1") & 1
units = [1 << i for i in range(m)]
tight = set()
# affine subspaces {z : l1.z = 1, l2.z = 0}, l1, l2 independent
for l1 in range(1, N):
    for l2 in range(1, N):
        if l2 == l1: continue
        A = frozenset(z for z in range(N) if par(z & l1) == 1 and par(z & l2) == 0)
        if sum(1 for e in units if e in A) & 1: tight.add(A)
pairs_ok = sum(1 for a, b in itertools.combinations(range(1, N), 2) if any(a in A and b in A for A in tight))
tot = (N - 1) * (N - 2) // 2
print("m = %d : %d tight characters (affine subspaces of %d words, missing 0, with an odd number of unit words); pairs of directions lying together in one: %d of %d"
      % (m, len(tight), N // 4, pairs_ok, tot))
# all tau-odd quadratic forms: least number of ones (check of the Reed-Muller count)
idx = [(i, j) for i in range(m) for j in range(i, m)]
if m <= 5:
    best = N
    for code in range(1, 1 << len(idx)):
        if sum(code >> t & 1 for t, (i, j) in enumerate(idx) if i == j) & 1:
            ones = sum(1 for z in range(1, N) if sum((code >> t & 1) & (z >> i & 1) & (z >> j & 1) for t, (i, j) in enumerate(idx)) & 1)
            best = min(best, ones)
    print("   least number of directions with Q(z) = 1 over all Q with <Q,I> = 1: %d  (so 'every direction once' serves W = %d arrays in the linear program)" % (best, best))
