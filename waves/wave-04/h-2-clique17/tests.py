#!/usr/bin/env python3
"""tests.py  -- three exact checks around the clique lemma, block size 5, W = 4.   [h-2-clique17]
(1) Words that ARE right and are not the coordinate schedule: each array is transformed along its own orthonormal frame
    (5 directions z with z.z = 1, pairwise z.z' = 0; then sum z z^T = I).  There are 6 frames.  A real unit must pass the
    clique test, so this is a test of the lemma, not of the vectors.
(2) The odd-weight design plus 1, 2 or 3 extra moves anywhere: every such vector, clique test.
(3) Bookkeeping of the picture 'frames = 6 points, odd directions = pairs of frames'.
"""
import sys, itertools
sys.argv = [sys.argv[0], "19"]
import post
import numpy as np
V = post.V; dot = post.dot
odd = [z for z in V if bin(z).count("1") & 1]
# frames
frames = []
for F in itertools.combinations(odd, 5):
    if all(dot(a, b) == 0 for a, b in itertools.combinations(F, 2)): frames.append(F)
print("(3) orthonormal frames: %d; direction 11111 lies in %d of them; every other odd direction lies in %s; two frames share %s direction(s)"
      % (len(frames), sum(31 in F for F in frames), sorted(set(sum(z in F for F in frames) for z in odd if z != 31)),
         sorted(set(len(set(F) & set(G)) for F, G in itertools.combinations(frames, 2)))))
print("(1) four arrays, each along one of the 6 frames (20 moves; right words):")
seen = set(); worst = 0
for combo in itertools.combinations_with_replacement(range(6), 4):
    n = [0] * 31
    for f in combo:
        for z in frames[f]: n[z - 1] += 1
    c = post.canon_fast(n)
    if c in seen: continue
    seen.add(c)
    nt, best, bs = post.clique_test(c); worst = max(worst, best)
    print("     frames %s: tight selections %d, largest set joined pairwise %d  %s" % (combo, nt, best, "ok" if best <= 4 else "LEMMA CONTRADICTED"))
print("     -> %d classes; largest joined set over all: %d (the lemma allows at most 4)" % (len(seen), worst))
design = [1 if z in odd else 0 for z in V]
for e in (1, 2, 3):
    cls = set()
    for comb in itertools.combinations_with_replacement(range(31), e):
        n = design[:]
        for i in comb: n[i] += 1
        cls.add(post.canon_fast(n))
    hist = {}
    for c in cls:
        nt, best, bs = post.clique_test(c); hist[best] = hist.get(best, 0) + 1
    print("(2) design + %d extra move(s): %d vectors up to the 720 maps; largest joined set -> number of vectors: %s; not excluded: %d"
          % (e, len(cls), sorted(hist.items()), sum(v for k, v in hist.items() if k <= 4)))
