#!/usr/bin/env python3
"""tests2.py -- the zero-form lemma on words that are right (frame schedules): it must not exclude them.  [h-2-clique17]"""
import sys, itertools
sys.argv = [sys.argv[0], "20"]
import post, post2
V = post.V; dot = post.dot
odd = [z for z in V if bin(z).count("1") & 1]
frames = [F for F in itertools.combinations(odd, 5) if all(dot(a, b) == 0 for a, b in itertools.combinations(F, 2))]
seen = set()
for combo in itertools.combinations_with_replacement(range(6), 4):
    n = [0] * 31
    for f in combo:
        for z in frames[f]: n[z - 1] += 1
    c = post.canon_fast(n)
    if c in seen: continue
    seen.add(c)
    kind, nt, cl, s, info = post2.both(c)
    print("frames %s: %s (tight selections %d, largest joined set %d) %s" % (combo, kind, nt, cl, "" if info is None else info))
