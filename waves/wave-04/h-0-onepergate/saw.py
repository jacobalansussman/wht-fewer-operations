#!/usr/bin/env python3
"""h-0 onepergate / saw.py : search for a better EXCHANGE RATE, not for fewer gates.  Count (G).  Exact (collinear triples of
integer vectors, as in g-1's sa8.py, whose pool and closure are reused).
Pool: the 304 coset sign vectors at 8 points (all vectors with entries 0, 1, -1 whose support is a coset of a subgroup:
the 128 tight wires, the 240 stabiliser vectors, all 128 full sign vectors, all sign patterns on the 14 half-cubes).
State = a set of helper wires.  cost = gates + (over-limit helpers) = 8 + |H| + V(H).  Law L1 says cost >= 24.
usage: saw.py anneal <seconds> <seed> <start: c19|c20|text|empty>      |     saw.py exchange <c19|c20|text>
"""
import sys, time, random, math, itertools
G1 = 'waves/wave-03/g-1-tightwires'
import os
if not os.path.isdir(G1): G1 = os.path.dirname(os.path.abspath(__file__)) + '/g1'
sys.path.insert(0, G1)
from pool import build_pool, lines
from ref import nz, wht, norm
pool = build_pool(3, 3); ws, trip = lines(pool); n = len(ws); idx = {w: i for i, w in enumerate(ws)}
just = [[] for _ in range(n)]
for (a, b, c) in trip:
    just[a].append((1 << b) | (1 << c)); just[b].append((1 << a) | (1 << c)); just[c].append((1 << a) | (1 << b))
S = [nz(w) for w in ws]; T = [nz(wht(w)) for w in ws]
inputs = [i for i in range(n) if S[i] == 1]; outs = [i for i in range(n) if S[i] == 8 and T[i] == 1]
over = [1 if S[i] * T[i] != 8 else 0 for i in range(n)]
cand = [i for i in range(n) if i not in inputs and i not in outs]
INMASK = 0
for i in inputs: INMASK |= 1 << i
def closure(H):
    avail = INMASK; todo = list(H) + [o for o in outs if o not in H]; ch = True
    while ch and todo:
        ch = False; rest = []
        for w in todo:
            if any((avail & m) == m for m in just[w]): avail |= 1 << w; ch = True
            else: rest.append(w)
        todo = rest
    return avail, len(todo)
def feasible(H): return closure(H)[1] == 0
def cost(H): return 8 + len(H) + sum(over[w] for w in H)
def vec(d):
    v = [0] * 8
    for p, c in d.items(): v[p] = c
    return idx[norm(v)]
def start(name):
    if name == 'empty': return []
    if name == 'text':
        H = []
        for q in range(4): H += [vec({2 * q: 1, 2 * q + 1: 1}), vec({2 * q: 1, 2 * q + 1: -1})]
        for b in (0, 4):
            for e in (1, -1):
                for f in (1, -1): H.append(vec({b: 1, b + 1: e, b + 2: f, b + 3: e * f}))
        return H
    if name == 'c19':
        g = [{0: 1, 7: 1}, {1: 1, 6: 1}, {2: 1, 5: -1}, {3: 1, 4: -1}, {0: 1, 7: 1, 1: -1, 6: -1}, {2: 1, 5: -1, 3: 1, 4: -1}]
        c = [1, -1, -1, -1, 1, 1, -1, 1]
        def fl(v, *ps):
            v = list(v)
            for p in ps: v[p] = -v[p]
            return v
        full = [c, fl(c, 7), fl(c, 5), fl(c, 7, 6), fl(c, 5, 4)]
        return [vec(d) for d in g] + [idx[norm(v)] for v in full]
    if name == 'c20':
        rows = ["1 1 0 0 0 0 0 0", "0 0 1 -1 0 0 0 0", "1 1 -1 1 0 0 0 0", "1 1 1 1 0 0 0 0", "1 -1 1 -1 0 0 0 0", "0 0 0 0 1 1 0 0", "0 0 0 0 0 0 1 -1",
                "0 0 0 0 1 1 1 -1", "0 0 0 0 1 1 -1 -1", "0 0 0 0 1 -1 -1 1", "1 1 1 1 1 1 -1 -1", "1 -1 1 -1 1 -1 -1 1"]
        return [idx[norm([int(z) for z in r.split()])] for r in rows]
AGREE = {}
for w in range(n):
    AGREE[w] = [max(sum(1 for x, y in zip(ws[w], ws[o]) if x != 0 and x == y), sum(1 for x, y in zip(ws[w], ws[o]) if x != 0 and x == -y)) for o in outs]
def energy(H, LAM=0.3):
    avail, _ = closure(H)
    missing = sum(1 for o in outs if not avail >> o & 1); dead = sum(1 for w in H if not avail >> w & 1)
    live = [w for w in H if avail >> w & 1]; gap = 0
    for t, o in enumerate(outs):
        if avail >> o & 1: continue
        gap += 8 - max([AGREE[w][t] for w in live] + [1])
    return cost(H) + 2.2 * missing + 2.5 * dead + LAM * gap, missing, dead
def show(H, tag):
    avail, _ = closure(H)
    print('%s: gates %d, over-limit helpers %d, cost = gates + over-limit = %d  (L1 says >= 24)' % (tag, 8 + len(H), sum(over[w] for w in H), cost(H)))
    for w in H: print('      (%d,%d)%s %s' % (S[w], T[w], ' OVER' if over[w] else '', list(ws[w])))
def anneal(secs, seed, st):
    rng = random.Random(seed); H = start(st); E, miss, dead = energy(H); best = (10 ** 9, None); t0 = time.time(); it = 0; hist = {}; seen = set()
    while time.time() - t0 < secs:
        it += 1; temp = 0.45 * (1 - 0.7 * (((time.time() - t0) % 60.0) / 60.0))
        H2 = list(H); m = rng.random()
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
                c = cost(H); key = (c, 8 + len(H)); hist[key] = hist.get(key, 0) + 1; seen.add(frozenset(H))
                if c < best[0]: best = (c, list(H)); print('   seed %d t=%.0fs: circuit with cost %d (gates %d + over-limit %d)' % (seed, time.time() - t0, c, 8 + len(H), c - 8 - len(H)), flush=True)
    print('seed %d start %s: %d moves; least cost %s; distinct circuits visited %d; visits by (cost, gates): %s' % (seed, st, it, best[0], len(seen), sorted(hist.items())))
    if best[1]: show(best[1], '   best')
def exchange(st):
    H = start(st); assert feasible(H); show(H, 'start ' + st); c0 = cost(H)
    tight_c = [w for w in cand if not over[w]]; over_c = [w for w in cand if over[w]]
    tested = hits = 0; found = []
    def adds(budget):
        """all sets of new helpers of total weight <= budget (tight = 1, over-limit = 2), at most 3 wires"""
        yield ()
        if budget >= 1:
            for w in tight_c: yield (w,)
        if budget >= 2:
            for w in over_c: yield (w,)
            for a in itertools.combinations(tight_c, 2): yield a
        if budget >= 3:
            for a in tight_c:
                for b in over_c: yield (a, b)
    for r in (1, 2, 3):
        for rem in itertools.combinations(range(len(H)), r):
            base = [h for i, h in enumerate(H) if i not in rem]; wr = sum(1 + over[H[i]] for i in rem)
            if r == 3 and wr - 1 > 2: bud = 2      # keep the largest neighbourhood affordable
            else: bud = wr - 1
            for A in adds(bud):
                if any(a in base for a in A): continue
                H2 = base + list(A); tested += 1
                if feasible(H2):
                    hits += 1
                    if len(found) < 5: found.append(H2)
    print('exchange around %s (cost %d): remove 1, 2 or 3 helpers and add helpers of smaller total weight: %d states tested, %d circuits with cost < %d' % (st, c0, tested, hits, c0))
    for H2 in found: show(H2, '   HIT')
if __name__ == '__main__':
    if sys.argv[1] == 'anneal': anneal(float(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
    else: exchange(sys.argv[2])
