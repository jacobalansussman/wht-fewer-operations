#!/usr/bin/env python3
"""g-7-thirdturn / stats16.py -- exact.  (1) every one of the 16 sign changes T_a = (-1)^(Q0 + w(a,.)) times S is a signed
relabelling in ONE half-transform basis; its cycle type.  (2) random bases B made of five (4,4,4) cycles + a weight-4 fixed
vector: how many are invertible, how many mix several Lagrangian planes, and their pair-sharing counts (count (G), upper bound)."""
import random, sys
from fractions import Fraction as F
import search16 as s
n = 16; pc = s.pc
rows = [s.prim([((-1) ** pc(a & (y >> 2))) if (y & 3) == b else 0 for y in range(n)]) for a in range(4) for b in range(4)]
ridx = {r: i for i, r in enumerate(rows)}
out = {}
for a in range(n):
    Ta = [(-1) ** (s.Q0(x) ^ s.w(a, x)) for x in range(n)]
    perm = []; ok = True
    for r in rows:
        ft = [r[x] * Ta[x] for x in range(n)]
        g = s.prim([sum(ft[x] * s.S[x][y] for x in range(n) if ft[x]) for y in range(n)])
        if g not in ridx: ok = False; break
        perm.append(ridx[g])
    if not ok: out[a] = None; continue
    cyc = {}; seen = set()
    for i in range(n):
        if i in seen: continue
        L = 0; t = i
        while t not in seen: seen.add(t); t = perm[t]; L += 1
        cyc[L] = cyc.get(L, 0) + 1
    out[a] = tuple(sorted(cyc.items()))
print("(1) T_a S in the one half-transform basis, a = 0..15: relabelling for all a:", all(v is not None for v in out.values()))
print("    cycle types {length: count} -> number of a:", {k: sum(1 for v in out.values() if v == k) for k in set(out.values())})
st = s.stabs(); idx = {v: i for i, v in enumerate(st)}; nxt = [idx[s.Rmap(v)] for v in st]
wt = lambda i: sum(1 for x in st[i] if x)
trip = sorted({tuple(sorted((i, nxt[i], nxt[nxt[i]]))) for i in range(len(st)) if nxt[i] != i})
t444 = [t for t in trip if all(wt(i) == 4 for i in t)]
fix4 = [i for i in range(len(st)) if nxt[i] == i and wt(i) == 4]
def plane(i):
    sup = [x for x in range(n) if st[i][x]]; return frozenset(x ^ sup[0] for x in sup)
planes_of = lambda t: frozenset(plane(i) for i in t)
print("(2) (4,4,4) cycles: %d ; each lies on ONE plane: %s ; distinct planes: %d ; fixed vectors of weight 4: %d" % (
    len(t444), all(len(planes_of(t)) == 1 for t in t444), len({next(iter(planes_of(t))) for t in t444}), len(fix4)))
rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1); tot = 0; inv = 0; hist = {}; mixed = {}
N = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
for _ in range(N):
    tr = rng.sample(t444, 5); f0 = rng.choice(fix4); B = [st[i] for t in tr for i in t] + [st[f0]]; tot += 1
    if not s.full_rank(B): continue
    inv += 1; c = s.cse(B)[0]; npl = len({next(iter(planes_of(t))) for t in tr} | {plane(f0)})
    hist[(npl, c)] = hist.get((npl, c), 0) + 1
print("    %d random choices, %d invertible.  (number of different planes used, pair-sharing count) -> how many:" % (tot, inv))
for k in sorted(hist): print("      ", k, hist[k])
print("    least count seen:", min(c for (_, c) in hist), "; least count with more than one plane:", min([c for (p, c) in hist if p > 1] or [None]))
