#!/usr/bin/env python3
"""g-7-thirdturn / search16b.py -- 16 points, exact Fractions.  The WHOLE freedom, not only stabilizer seeds:
state = 5 seed forms f_i (any rational vectors) and one fixed form f0; B = [f_i, f_i R, f_i R^2 ; f0].
Moves = elements of the centraliser of the relabelling: f_i += c * (f_k R^r), f_i += c * (f_i R^r), f_i += c * (a fixed form),
f0 += c * (f_i + f_i R + f_i R^2), f0 := a fixed stabilizer vector, f_i := a stabilizer vector.
Energy = pair-sharing count of B (mode B) or of B and B^-1 together (mode both).  Count (G), an upper bound; see search16.py.
usage: search16b.py <mode: B | both> <seconds> <rng seed> <start: L | chain | rand>
"""
import sys, time, random, json
from fractions import Fraction as F
from math import gcd
import search16 as s16
n = 16; T = s16.T; S = s16.S
def Rx(f):        # exact f R, R = T S / 4
    ft = [f[x] * T[x] for x in range(n)]
    return tuple(sum(ft[x] * S[x][y] for x in range(n) if ft[x]) / 4 for y in range(n))
def toint(f):
    den = 1
    for v in f: den = den * v.denominator // gcd(den, v.denominator)
    return s16.prim([int(v * den) for v in f])
def rows_of(state):
    seeds, f0 = state; rows = []
    for f in seeds:
        f1 = Rx(f); f2 = Rx(f1); rows += [f, f1, f2]
    rows.append(f0); return rows
mode, secs, seed, start = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
rng = random.Random(seed); t0 = time.time()
st = s16.stabs(); idx = {v: i for i, v in enumerate(st)}
fx = [tuple(F(x) for x in v) for v in st if s16.Rmap(v) == v]
assert all(Rx(u) == u for u in fx)
stF = [tuple(F(x) for x in v) for v in st if sum(1 for x in v if x) <= 4]
def energy(state):
    rows = rows_of(state); ir = [toint(r) for r in rows]
    if any(r is None for r in ir) or len(set(ir)) < 16: return None
    if max(abs(x) for r in ir for x in r) > 12: return None
    if not s16.full_rank(ir): return None
    cB = s16.cse(ir)[0]
    if mode == "B": return (cB, cB, None)
    Bi = s16.inv_int(ir)
    if max(abs(x) for r in Bi for x in r) > 60: return None
    cI = s16.cse(Bi)[0]; return (cB + cI, cB, cI)
pc = s16.pc
def start_state():
    if start == "L":
        rows = [tuple(F(x) for x in s16.prim([((-1) ** pc(a & (y >> 2))) if (y & 3) == b else 0 for y in range(n)])) for a in range(4) for b in range(4)]
        f0 = next(r for r in rows if Rx(r) == r); seeds = []; used = set()
        for r in rows:
            if r == f0 or toint(r) in used: continue
            r1 = Rx(r); r2 = Rx(r1); used |= {toint(r), toint(r1), toint(r2)}; seeds.append(r)
        assert len(seeds) == 5; return (seeds, f0)
    if start == "chain":      # the tensor square of the 4-point chain basis [x0; x0+x1; x0+x1+x2+x3; x0+x1+x2-x3]
        B4 = [[1, 0, 0, 0], [1, 1, 1, 1], [1, 1, 1, -1], [1, 1, 0, 0]]      # rows: seed e0, e0 R, e0 R^2, fixed
        # digits: address y -> digit i = (bit i of p1, bit i of p2) ; y = p1*4 + p2
        dig = lambda y: [(((y >> (2 + i)) & 1) << 1) | ((y >> i) & 1) for i in range(2)]
        rows = [tuple(F(B4[a][dig(y)[0]] * B4[b][dig(y)[1]]) for y in range(n)) for a in range(4) for b in range(4)]
        f0 = next(r for r in rows if Rx(r) == r); seeds = []; used = set()
        for r in rows:
            if r == f0 or toint(r) in used: continue
            r1 = Rx(r); r2 = Rx(r1); used |= {toint(r), toint(r1), toint(r2)}; seeds.append(r)
        assert len(seeds) == 5, len(seeds); return (seeds, f0)
    while True:
        s = ([rng.choice(stF) for _ in range(5)], rng.choice(fx))
        if energy(s) is not None: return s
CO = [F(1), F(-1), F(2), F(-2), F(1, 2), F(-1, 2), F(3), F(-3), F(1, 3), F(-1, 3)]
s = start_state(); E = energy(s); best = E; bests = [(E, s)]; hist = {}; nev = 0; temp = 0.7
print("start (%s): total %s  cost(B) %s  cost(B^-1) %s" % (start, E[0], E[1], E[2]), flush=True)
add = lambda f, c, g: tuple(a + c * b for a, b in zip(f, g))
while time.time() - t0 < secs:
    seeds, f0 = list(s[0]), s[1]; m = rng.random(); i = rng.randrange(5); c = rng.choice(CO if rng.random() < 0.3 else CO[:2])
    if m < 0.40:
        k = rng.choice([q for q in range(5) if q != i]); g = seeds[k]
        for _ in range(rng.randrange(3)): g = Rx(g)
        seeds[i] = add(seeds[i], c, g)
    elif m < 0.50:
        g = Rx(seeds[i])
        if rng.random() < 0.5: g = Rx(g)
        seeds[i] = add(seeds[i], c, g)
    elif m < 0.65:
        seeds[i] = add(seeds[i], c, f0 if rng.random() < 0.5 else rng.choice(fx))
    elif m < 0.75:
        f = seeds[i]; f1 = Rx(f); f2 = Rx(f1); f0 = add(f0, c, tuple(a + b + d for a, b, d in zip(f, f1, f2)))
    elif m < 0.82:
        f0 = rng.choice(fx)
    elif m < 0.92:
        seeds[i] = rng.choice(stF)
    else:
        g = seeds[i]
        for _ in range(1 + rng.randrange(2)): g = Rx(g)
        seeds[i] = g
    s2 = (seeds, f0); E2 = energy(s2)
    if E2 is None: continue
    nev += 1; hist[E2[0]] = hist.get(E2[0], 0) + 1
    if E2[0] <= E[0] or rng.random() < pow(2.718281828, -(E2[0] - E[0]) / temp):
        s, E = s2, E2
        if E[0] < best[0]:
            best = E; bests.append((E, s)); print("  t=%.0f best total %s  cost(B) %s  cost(B^-1) %s  after %d states" % (time.time() - t0, E[0], E[1], E[2], nev), flush=True)
print("DONE mode=%s seed=%d start=%s states=%d best=%s histogram(lowest)=%s" % (mode, seed, start, nev, best, {k: hist[k] for k in sorted(hist)[:8]}))
E, s = bests[-1]; rows = [toint(r) for r in rows_of(s)]
print("best B (rows in threes f, fR, fR^2; last row fixed), weights of rows:", [sum(1 for x in r if x) for r in rows])
for r in rows: print("   ", " ".join("%2d" % x for x in r))
c, prog, tg = s16.cse(rows); print("pair-sharing program for B: %d gates; nodes (new, u, v, p, q) meaning new = p*u + q*v:" % c, prog)
print("targets after sharing:", [sorted(d.items()) for d in tg])
Bi = s16.inv_int(rows); c2, prog2, tg2 = s16.cse(Bi)
print("B^-1 rows (scaled to integers), weights:", [sum(1 for x in r if x) for r in Bi])
for r in Bi: print("   ", " ".join("%3d" % x for x in r))
print("pair-sharing program for B^-1: %d gates" % c2)
json.dump({"E": E, "rows": [list(r) for r in rows]}, open("bestb_%s_%d_%s.json" % (mode, seed, start), "w"))
