#!/usr/bin/env python3
"""plain_test.py  (n-2): my judge on right 20-move words (must NOT be excluded), and the frame facts."""
import sys, itertools
sys.argv = [sys.argv[0], "0"]
import mypost as P
V = P.V; par = P.par
odd = [z for z in V if par(z)]
frames = sorted({tuple(sorted(b)) for b in P.bases})
print("orthonormal frames:", len(frames), [[format(z, "05b") for z in f] for f in frames])
# every odd non-centre direction lies in exactly two frames; two frames share exactly one direction
print("frames through each odd non-centre direction:", sorted({sum(z in f for f in frames) for z in odd if z != 31}),
      "; centre in", sum(31 in f for f in frames), "; common directions of two frames:", sorted({len(set(a) & set(b)) for a, b in itertools.combinations(frames, 2)}))
seen = {}
for combo in itertools.combinations_with_replacement(range(len(frames)), 4):
    n = [0] * 31
    for f in combo:
        for z in frames[f]: n[z - 1] += 1
    seen.setdefault(P.canon(n), combo)
print("count vectors of 'four arrays, each along its own frame' up to symmetry:", len(seen))
for c, combo in sorted(seen.items()):
    kind, nt, cl, info = P.judge(list(c))
    print("   frames %s: %s; tight selections %d; largest joined set %d" % (combo, kind, nt, cl))
