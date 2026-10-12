#!/usr/bin/env python3
"""h1_seed13.py [aa-cross]  16 points, degree 2: is there a pair of partitions with 13 classes in all?  Seeded walk: start
from the 14-class family, merge two classes of one partition, then move single points between existing classes.
Rank modulo 1000003 as a filter; every hit is re-checked in Fractions.  A walk: silence is not a proof."""
import sys, time, random, itertools
sys.argv = sys.argv[:1]
import importlib.util
spec = importlib.util.spec_from_file_location("g", "h1_graph.py"); 
src = open("h1_graph.py").read().split('print("== theta family')[0]
g = {}; exec(src, g)
k = 4; N = 16; mon = g["monos"](k, 2); rnd = random.Random(13); secs = 100.0; t0 = time.time()
a0, b0 = g["theta"](k); ia = {c: i for i, c in enumerate(sorted(set(a0)))}; ib = {c: i for i, c in enumerate(sorted(set(b0), key=str))}
a0 = [ia[c] for c in a0]; b0 = [ib[c] for c in b0]
print("control: the family itself, classes %d, missing %d" % (len(set(a0)) + len(set(b0)), g["defect"](a0, b0, mon, g["rank_frac"])[0]))
seeds = [(0, p, q) for p, q in itertools.combinations(range(8), 2)] + [(1, p, q) for p, q in itertools.combinations(range(6), 2)]
best = 99; evals = 0; hits = []
while time.time() - t0 < secs and not hits:
    rnd.shuffle(seeds)
    for which, p, q in seeds:
        a = a0[:]; b = b0[:]; lab = a if which == 0 else b
        for x in range(N):
            if lab[x] == q: lab[x] = p
        cur = g["defect"](a, b, mon)[0]; stall = 0
        while cur and stall < 250 and time.time() - t0 < secs:
            w = rnd.random() < 0.5; L = a if w else b; x = rnd.randrange(N); old = L[x]; new = rnd.choice(sorted(set(L)))
            if new == old or L.count(old) == 1: continue          # keep the number of classes
            L[x] = new; d = g["defect"](a, b, mon)[0]; evals += 1
            if d <= cur: stall = 0 if d < cur else stall + 1; cur = d
            else: L[x] = old; stall += 1
        best = min(best, cur)
        if cur == 0:
            ex = g["defect"](a, b, mon, g["rank_frac"])
            if ex[0] == 0: hits.append((ex[1], a[:], b[:])); break
        if time.time() - t0 > secs: break
print("13 classes: least number of missing directions reached %d ; evaluations %d ; exact hits %d ; %.0f s" % (best, evals, len(hits), time.time() - t0))
for h in hits: print("   HIT classes %d P1=%s P2=%s" % h)
