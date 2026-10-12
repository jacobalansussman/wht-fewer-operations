#!/usr/bin/env python3
"""Hub capacity at 8 points: hold inputs, first output, its 6 tree helpers (and the second output when the tree allows it);
add ONE more helper h = a*u + b*v (u, v held; ratio from a small set) and close under one-gate outputs.
How many outputs can one extra helper bring?  (2 more would fit the guess 'each extra helper enables at most two'.)"""
import sys, random
from itertools import combinations
sys.argv = [sys.argv[0], '3', '0']
exec(open('tree8.py').read().split("hist = {}")[0])   # reuse Y, on_line, random_tree
trials = int(sys.argv[2]) if False else 0
T = [(1, 1), (1, -1), (1, 2), (1, -2), (2, 1), (2, -1), (1, 3), (1, -3), (3, 1), (3, -1)]
rng = random.Random(11)
def sub(S):
    parts = [frozenset([x]) for x in S]; inner = []
    while len(parts) > 1:
        i, j = rng.sample(range(len(parts)), 2)
        m = parts[i] | parts[j]
        parts = [p for q, p in enumerate(parts) if q not in (i, j)] + [m]
        inner.append(m)
    return inner
def close(pts, got, newpts):
    # outputs on a line through a NEW point and any held point, repeated
    frontier = list(newpts)
    while frontier:
        nxt = []
        for w in range(1, N):
            if w in got: continue
            if any(on_line(Y[w], h, u) for h in frontier for u in pts if u != h):
                got.add(w); pts.append(Y[w]); nxt.append(Y[w])
        frontier = nxt
    return got
import time
t0 = time.time(); best = {}; examples = {}
ntree = 0
while time.time() - t0 < 85:
    ntree += 1
    w = rng.randrange(1, N)
    D = [x for x in range(N) if Y[w][x] == -1]; Dc = [x for x in range(N) if Y[w][x] == 1]
    sets = sub(D) + sub(Dc) if ntree % 3 else random_tree([[x] for x in range(N)])
    pts = [tuple(int(i == x) for i in range(N)) for x in range(N)]
    pts += [tuple(1 if i in S else 0 for i in range(N)) for S in sets]
    pts.append(Y[0])
    got = close(list(pts), {0}, []) if False else {0}
    base = list(pts)
    # base closure (all pairs)
    ch = True
    while ch:
        ch = False
        for ww in range(1, N):
            if ww in got: continue
            if any(on_line(Y[ww], u, v) for u, v in combinations(base, 2)):
                got.add(ww); base.append(Y[ww]); ch = True
    from math import gcd
    def pn(v):
        g = 0
        for x in v: g = gcd(g, abs(x))
        v = tuple(x // g for x in v)
        f = next(x for x in v if x)
        return v if f > 0 else tuple(-x for x in v)
    held = {pn(p) for p in base}
    for u, v in combinations(base, 2):
        for (a, b) in T:
            h = tuple(a * x + b * y for x, y in zip(u, v))
            if not any(h): continue
            h = pn(h)
            if h in held: continue   # proportional to a point already held: not a new helper
            g2 = close(base + [h], set(got), [h])
            gain = len(g2) - len(got)
            best[gain] = best.get(gain, 0) + 1
            if gain >= 2 and gain not in examples:
                examples[gain] = (sorted(map(sorted, sets)), h, (u, v), sorted(g2))
print("trees tried", ntree, " histogram of outputs gained by one extra helper:", sorted(best.items()))
for g, ex in sorted(examples.items()):
    print("gain", g, "example: tree sets", ex[0]); print("    helper", ex[1], "from", ex[2], "outputs held after", ex[3])
