#!/usr/bin/env python3
# h-5 / classsa.py : annealer for 8-point circuits (count G) whose wires ALL lie in the pair class
# (product across at least one cut "one bit | the other two"), pool = every such wire with entries 0, +1, -1 (up to scale).
# Exact: a gate is a collinear triple of pool wires over the rationals (third points u+-v, u+-2v, 2u+-v; e2-0 derived that these are all).
# The annealing loop is g-1's sa8.py (energy = helpers + 8 + penalties, graded by agreement with the missing outputs).
# usage: classsa.py seconds seed [start: empty|stair]
import sys, time, random, math, itertools
from math import gcd
N = 8
def norm(v):
    g = 0
    for a in v: g = gcd(g, abs(a))
    if g == 0: return None
    v = tuple(a // g for a in v)
    for a in v:
        if a: return v if a > 0 else tuple(-b for b in v)
def cutrank1(w, i):
    lo = [w[x] for x in range(N) if not (x >> i) & 1]; hi = [w[x] for x in range(N) if (x >> i) & 1]
    return all(lo[a] * hi[b] == lo[b] * hi[a] for a in range(4) for b in range(a + 1, 4))
ws = sorted({norm(v) for v in itertools.product((-1, 0, 1), repeat=N) if any(v) and any(cutrank1(v, i) for i in range(3))})
idx = {w: i for i, w in enumerate(ws)}; n = len(ws)
RAT = [(1, 1), (1, -1), (1, 2), (1, -2), (2, 1), (2, -1)]
just = [set() for _ in range(n)]; ntr = 0
for i in range(n):
    for j in range(i + 1, n):
        for a, b in RAT:
            w = norm(tuple(a * x + b * y for x, y in zip(ws[i], ws[j])))
            if w in idx:
                k = idx[w]
                if k != i and k != j: just[k].add((1 << i) | (1 << j)); ntr += 1
just = [list(s) for s in just]
Y = [norm(tuple((-1) ** bin(c & x).count('1') for x in range(N))) for c in range(N)]
inputs = [idx[tuple(int(i == x) for x in range(N))] for i in range(N)]; outs = [idx[y] for y in Y]
cand = [i for i in range(n) if i not in inputs and i not in outs]
AGREE = {w: [max(sum(1 for x, y in zip(ws[w], ws[o]) if x != 0 and x == y), sum(1 for x, y in zip(ws[w], ws[o]) if x != 0 and x == -y)) for o in outs] for w in range(n)}
print('pair-class pool with entries 0,+-1: %d wires, %d candidate helpers, %d (wire, parent pair) gate records' % (n, len(cand), ntr), flush=True)
def closure(H):
    avail = 0
    for i in inputs: avail |= 1 << i
    todo = list(H) + [o for o in outs if o not in H]; order = []; ch = True
    while ch and todo:
        ch = False; rest = []
        for w in todo:
            if any((avail & m) == m for m in just[w]): avail |= 1 << w; order.append(w); ch = True
            else: rest.append(w)
        todo = rest
    return avail, order
LAM = 0.3; TEMP = 0.35
def energy(H, W=0.5):
    avail, order = closure(H)
    missing = sum(1 for o in outs if not avail >> o & 1); dead = sum(1 for w in H if not avail >> w & 1)
    live = [w for w in H if avail >> w & 1]; gap = 0
    for t, o in enumerate(outs):
        if avail >> o & 1: continue
        gap += 8 - max([AGREE[w][t] for w in live] + [1])
    return len(H) + 8 + W * missing + 1.0 * dead + LAM * gap, missing, dead
secs, seed = float(sys.argv[1]), int(sys.argv[2]); start = sys.argv[3] if len(sys.argv) > 3 else 'empty'; rng = random.Random(seed)
STAIR = [(1,1,0,0,0,0,0,0),(0,0,1,-1,0,0,0,0),(1,1,-1,1,0,0,0,0),(1,1,1,1,0,0,0,0),(1,-1,1,-1,0,0,0,0),(0,0,0,0,1,1,0,0),(0,0,0,0,0,0,1,-1),
         (0,0,0,0,1,1,1,-1),(0,0,0,0,1,1,-1,-1),(0,0,0,0,1,-1,-1,1),(1,1,1,1,1,1,-1,-1),(1,-1,1,-1,1,-1,-1,1)]
e, miss, dead = energy([idx[norm(h)] for h in STAIR]); print('staircase check: gates %d, outputs missing %d, dead helpers %d' % (len(STAIR) + 8, miss, dead), flush=True)
def anneal(H0, tmax, temp0=TEMP):
    H = list(H0); E, miss, dead = energy(H); best = (10 ** 9, None); t0 = time.time(); it = 0; hist = {}
    while time.time() - t0 < tmax:
        it += 1; temp = temp0 * (1 - 0.7 * ((time.time() - t0) / tmax)); H2 = list(H); m = rng.random()
        if m < 0.35 or not H2:
            avail, _ = closure(H2); w = rng.choice(cand)
            for _ in range(6):
                if w not in H2 and any((avail & mm) == mm for mm in just[w]): break
                w = rng.choice(cand)
            if w in H2: continue
            H2.append(w)
        elif m < 0.7: H2.pop(rng.randrange(len(H2)))
        else:
            H2.pop(rng.randrange(len(H2))); w = rng.choice(cand)
            if w in H2: continue
            H2.append(w)
        E2, miss2, dead2 = energy(H2)
        if E2 <= E or rng.random() < math.exp(-(E2 - E) / temp):
            H, E, miss, dead = H2, E2, miss2, dead2
            if miss == 0 and dead == 0:
                g = len(H) + 8; hist[g] = hist.get(g, 0) + 1
                if g < best[0]: best = (g, list(H)); print('   seed %d t=%.0fs: circuit with %d gates' % (seed, time.time() - t0, g), flush=True)
    return best, it, hist
H0 = [idx[norm(h)] for h in STAIR] if start == 'stair' else []
best = (10 ** 9, None); it = 0; hist = {}; t00 = time.time(); rounds = 0
while time.time() - t00 < secs:
    b2, it2, h2 = anneal(H0, min(60.0, secs - (time.time() - t00))); it += it2; rounds += 1
    for g, c in h2.items(): hist[g] = hist.get(g, 0) + c
    if b2[0] < best[0]: best = b2
print('restarts %d, seed %d start %s: %d moves; best circuit %s gates; feasible states visited by gate count: %s' % (rounds, seed, start, it, best[0], sorted(hist.items())))
if best[1]:
    H = best[1]; avail, order = closure(H)
    for w in order: print('   %s %s' % ('OUT ' if w in outs else 'help', list(ws[w])))
    better = 0; tested = 0
    for r in (1, 2):
        for rem in itertools.combinations(range(len(H)), r):
            base = [h for i, h in enumerate(H) if i not in rem]
            for add in ([None] if r == 1 else cand):
                if add is not None and add in base: continue
                H2 = base + ([add] if add is not None else []); tested += 1
                e, miss, dead = energy(H2)
                if miss == 0 and dead == 0: better += 1
    print('   exhaustive exchange around it (remove 1; remove 2 and add any 1 of %d): %d states tested, %d circuits with %d gates' % (len(cand), tested, better, best[0] - 1))
