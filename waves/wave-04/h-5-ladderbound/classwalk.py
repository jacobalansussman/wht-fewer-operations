#!/usr/bin/env python3
# h-5 / classwalk.py : local walk at 8 points, count (G), INSIDE the class "every wire is a product across at least one cut
# (one bit | the other two)", i.e. entangled on at most two coordinate bits.  Exact integers.  Entries bounded by M (finite pool).
# Gates a*u + b*v with a, b in {+-1, +-2, +-3}.  Start: the 12 helpers of e2-0's 20-gate staircase (it lies in the class).
# Moves as in e2-0-pieces/walk.py: drop one helper; remove two and add one (improvement); swap one (plateau).
# usage: classwalk.py M seconds seed
import sys, time, random, itertools
from math import gcd
sys.path.insert(0, 'waves/wave-02/e2-0-pieces')
from pool import norm, Y, E, N
M, secs, seed = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]); rng = random.Random(seed)
RAT = [(a, b) for a in (1, 2, 3) for b in (-3, -2, -1, 1, 2, 3) if gcd(a, abs(b)) == 1]
def cutrank1(w, i):
    lo = [w[x] for x in range(N) if not (x >> i) & 1]; hi = [w[x] for x in range(N) if (x >> i) & 1]
    return all(lo[a] * hi[b] == lo[b] * hi[a] for a in range(4) for b in range(a + 1, 4))
def inpool(w): return max(map(abs, w)) <= M and any(cutrank1(w, i) for i in range(3))
OUT = [norm(y) for y in Y]; INS = set(E)
def third(u, v):
    for a, b in RAT:
        w = norm(tuple(a * x + b * y for x, y in zip(u, v)))
        if w is not None: yield w
def closure(points):
    D = set(INS); pend = [p for p in points if p not in D]; ch = True
    while ch and pend:
        ch = False; rest = []
        for p in pend:
            ok = False
            for q in D:
                for r in third(p, q):
                    if r in D and r != q and r != p: ok = True; break
                if ok: break
            if ok: D.add(p); ch = True
            else: rest.append(p)
        pend = rest
    return D, pend
def extend(D, pend, c):
    D = set(D); D.add(c); new = [c]; pend = list(pend)
    while new and pend:
        nxt = []; rest = []
        for p in pend:
            ok = False
            for n in new:
                for r in third(p, n):
                    if r in D and r != n and r != p: ok = True; break
                if ok: break
            (nxt if ok else rest).append(p)
        for p in nxt: D.add(p)
        new = nxt; pend = rest
    return D, pend
def candidates(D):
    C = set(); Dl = list(D)
    for i, q in enumerate(Dl):
        for r in Dl[i + 1:]:
            for w in third(q, r):
                if w not in D and inpool(w): C.add(w)
    return C
def valid(H):
    D, pend = closure(list(H) + OUT); return all(o in D for o in OUT), D
H0 = [(1,1,0,0,0,0,0,0),(0,0,1,-1,0,0,0,0),(1,1,-1,1,0,0,0,0),(1,1,1,1,0,0,0,0),(1,-1,1,-1,0,0,0,0),(0,0,0,0,1,1,0,0),(0,0,0,0,0,0,1,-1),
      (0,0,0,0,1,1,1,-1),(0,0,0,0,1,1,-1,-1),(0,0,0,0,1,-1,-1,1),(1,1,1,1,1,1,-1,-1),(1,-1,1,-1,1,-1,-1,1)]
H = set(norm(h) for h in H0); assert all(inpool(h) for h in H); ok, D = valid(H); assert ok
print('START gates', len(H) + 8, 'M', M, flush=True)
t0 = time.time(); seen = {frozenset(H)}; best = len(H); step = 0; tried = 0
while time.time() - t0 < secs:
    step += 1; Hl = sorted(H); done = False
    for h in Hl:
        if valid(H - {h})[0]: H = H - {h}; print('DROP ->', len(H) + 8, sorted(H), flush=True); done = True; break
    if done: best = min(best, len(H)); continue
    improved = False
    for h1, h2 in itertools.combinations(Hl, 2):
        rest = H - {h1, h2}; D, pend = closure(list(rest) + OUT)
        for c in candidates(D):
            tried += 1
            D2, pend2 = extend(D, pend, c)
            if all(o in D2 for o in OUT):
                H = set(p for p in rest if p in D2) | {c}; improved = True; break
        if improved or time.time() - t0 > secs: break
    if improved:
        print('IMPROVED ->', len(H) + 8, sorted(H), flush=True); best = min(best, len(H)); seen.add(frozenset(H)); continue
    nbrs = []; order = Hl[:]; rng.shuffle(order)
    for h in order[:5]:
        rest = H - {h}; D, pend = closure(list(rest) + OUT)
        for c in candidates(D):
            if c == h: continue
            D2, pend2 = extend(D, pend, c)
            if all(o in D2 for o in OUT) and all(p in D2 for p in rest):
                nb = frozenset(rest | {c})
                if nb not in seen: nbrs.append(nb)
    if not nbrs: print('no unseen neighbour at step', step, flush=True); break
    H = set(rng.choice(nbrs)); seen.add(frozenset(H))
    print('step', step, 'gates', len(H) + 8, 'neighbours', len(nbrs), 'remove-2-add-1 tries so far', tried, 'time', round(time.time() - t0), flush=True)
print('END best gates', best + 8, 'programs visited', len(seen), 'remove-2-add-1 tries', tried)
