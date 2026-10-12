#!/usr/bin/env python3
"""g-1 fwq16.py: the one-tree flip-walk model at 16 points, ONE chain of subgroups (all chains are equivalent under linear maps
of the addresses) and ALL 64 quadratic forms without linear part as F0 = (-1)^g.  Heuristic tree (upper bounds), 8 random
tie-breaks per design; every best is replayed exactly.  Count (G).  usage: fwq16.py seconds"""
import sys, time, random, itertools
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from flipwalk import steiner, replay
k = 4; N = 16; rng = random.Random(5); t0 = time.time(); secs = float(sys.argv[1])
pairs = [(a, b) for a in range(k) for b in range(a + 1, k)]; res = {}; best = None
for co in itertools.product((0, 1), repeat=6):
    if time.time() - t0 > secs: break
    F0 = [(-1) ** (sum(c * (x >> a & 1) * (x >> b & 1) for c, (a, b) in zip(co, pairs)) & 1) for x in range(N)]
    edges, targets = steiner(k, F0, (1, 2, 4), rng, tries=8); g = N - 1 + len(edges); res[co] = g
    if best is None or g < best[0]:
        gates, ok = replay(k, F0, (1, 2, 4), edges); best = (g, co)
        print("t=%.0fs form %s (monomials %s): %d gates, replayed exactly: %d, all characters: %s" % (time.time() - t0, co, pairs, g, gates, ok), flush=True)
hist = {}
for g in res.values(): hist[g] = hist.get(g, 0) + 1
print("16 points, chain (1,2,4), %d of 64 quadratic forms done; gates (count: forms): %s; best %s" % (len(res), sorted(hist.items()), best))
