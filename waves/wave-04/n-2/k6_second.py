#!/usr/bin/env python3
"""k6_second.py (n-2): the facts used in the hand argument that the complete-graph vector (15 moves, 3 arrays) is no unit."""
import sys, itertools
sys.argv = [sys.argv[0], "0"]
import mypost as P
frames = sorted({tuple(sorted(b)) for b in P.bases})
edge = {}                                           # direction -> the two frames through it
for z in P.V:
    if P.par(z) and z != 31: edge[z] = tuple(i for i, f in enumerate(frames) if z in f)
assert sorted(edge.values()) == sorted(itertools.combinations(range(6), 2))
used = sum(1 << (z - 1) for z in edge)
def edges(mk): return sorted(edge[z] for z in edge if mk >> (z - 1) & 1)
t1 = {f & used for f in P.F1}; t0 = {f & used for f in P.F0}
tight = [edges(s) for s in t1 if bin(s).count("1") == 3]
print("forms with q(I)=1 restricted to the 15 edges: %d patterns; smallest selects %d; patterns with exactly 3 edges: %d, all perfect matchings: %s"
      % (len(t1), min(bin(s).count("1") for s in t1), len(tight), all(len({v for e in t for v in e}) == 6 for t in tight)))
four = [edges(s) for s in t0 if bin(s).count("1") == 4]
def is4cycle(es):
    vs = {v for e in es for v in e}
    return len(vs) == 4 and all(sum(v in e for e in es) == 2 for v in vs)
print("forms with q(I)=0 restricted: %d patterns; with exactly 4 edges: %d, all 4-cycles: %s (K6 has 45 four-cycles)"
      % (len(t0), len(four), all(is4cycle(e) for e in four)))
print("every 4-cycle contains two disjoint edges (a joined pair), so it is an equality case of the zero-form lemma: 4 = 2*2")
