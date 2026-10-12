#!/usr/bin/env python3
"""g-7-thirdturn / search64.py -- 64 points, exact Fractions: the centraliser walk of search16b.py at the next size.
state = 21 seeds f_i and one fixed form f0; B = [f_i, f_i R, f_i R^2 ; f0]; energy = pair-sharing count of B
(count (G), upper bound, no helper wires).  Moves: f_i += c * (f_k R^r), f_i += c * (f_i R^r), f_i += c * f0,
f0 += c * (f_i + f_i R + f_i R^2), f_i := f_i R^r.   usage: search64.py <seconds> <rng seed> <start: L | chain>"""
import sys, time, random, itertools
from fractions import Fraction as F
from math import gcd
import search16 as s
pc = s.pc; j = 3; n = 64; lo = 7; r = 8; m = 21
w = lambda p, y: (pc((p >> j) & (y & lo)) + pc((p & lo) & (y >> j))) & 1
Q0 = lambda x: pc((x >> j) & (x & lo)) & 1
S = [[-1 if w(p, y) else 1 for y in range(n)] for p in range(n)]; T = [(-1) ** Q0(x) for x in range(n)]
def Rx(f):
    ft = [f[x] * T[x] for x in range(n)]
    return tuple(sum(ft[x] * S[x][y] for x in range(n) if ft[x]) / 8 for y in range(n))
def toint(f):
    den = 1
    for v in f: den = den * v.denominator // gcd(den, v.denominator)
    return s.prim([int(v * den) for v in f])
PR = 1000003
def full_rank(M):
    A = [[v % PR for v in r_] for r_ in M]; rk = 0
    for c in range(n):
        p = next((i for i in range(rk, n) if A[i][c]), None)
        if p is None: return False
        A[rk], A[p] = A[p], A[rk]; iv = pow(A[rk][c], PR - 2, PR)
        for i in range(rk + 1, n):
            if A[i][c]:
                f = A[i][c] * iv % PR; A[i] = [(x - f * y) % PR for x, y in zip(A[i], A[rk])]
        rk += 1
    return True
secs, seed, start = float(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
rng = random.Random(seed); t0 = time.time()
if start == "L":
    rows = [tuple(F(x) for x in s.prim([((-1) ** pc(a & (y >> j))) if (y & lo) == b else 0 for y in range(n)])) for a in range(r) for b in range(r)]
else:
    B4 = [[1, 0, 0, 0], [1, 1, 1, 1], [1, 1, 1, -1], [1, 1, 0, 0]]
    dig = lambda y: [(((y >> (j + i)) & 1) << 1) | ((y >> i) & 1) for i in range(j)]
    rows = []
    for idx in itertools.product(range(4), repeat=j):
        row = []
        for y in range(n):
            v = 1
            for a, d in zip(idx, dig(y)): v *= B4[a][d]
            row.append(F(v))
        rows.append(tuple(row))
cyc = {}   # cache of cycles: seed -> (f, fR, fR2) as int rows
def cyc_rows(f):
    if f not in cyc:
        f1 = Rx(f); f2 = Rx(f1); cyc[f] = (toint(f), toint(f1), toint(f2), f1, f2)
        if len(cyc) > 20000: cyc.clear()
    return cyc[f]
f0 = next(q for q in rows if toint(Rx(q)) == toint(q)); seeds = []; used = set()
for q in rows:
    if q == f0 or toint(q) in used: continue
    c = cyc_rows(q); used |= set(c[:3]); seeds.append(q)
assert len(seeds) == m
def energy(seeds, f0):
    ir = []
    for f in seeds: ir += list(cyc_rows(f)[:3])
    ir.append(toint(f0))
    if any(q is None for q in ir) or len(set(ir)) < n: return None
    if max(abs(x) for q in ir for x in q) > 12: return None
    if not full_rank(ir): return None
    return s.cse(ir)[0]
E = energy(seeds, f0); best = E; hist = {}; nev = 0; temp = 0.7
print("start (%s): pair-sharing count of B = %d (per form %.3f)" % (start, E, E / n), flush=True)
add = lambda f, c, g: tuple(a + c * b for a, b in zip(f, g))
CO = [F(1), F(-1), F(2), F(-2), F(1, 2), F(-1, 2)]
while time.time() - t0 < secs:
    sd = list(seeds); g0 = f0; mv = rng.random(); i = rng.randrange(m); c = rng.choice(CO if rng.random() < 0.25 else CO[:2])
    if mv < 0.5:
        k = rng.choice([q for q in range(m) if q != i]); cr = cyc_rows(sd[k]); g = [sd[k], cr[3], cr[4]][rng.randrange(3)]
        sd[i] = add(sd[i], c, g)
    elif mv < 0.6:
        cr = cyc_rows(sd[i]); sd[i] = add(sd[i], c, cr[3 + rng.randrange(2)])
    elif mv < 0.72:
        sd[i] = add(sd[i], c, g0)
    elif mv < 0.84:
        cr = cyc_rows(sd[i]); g0 = add(g0, c, tuple(a + b + d for a, b, d in zip(sd[i], cr[3], cr[4])))
    else:
        cr = cyc_rows(sd[i]); sd[i] = cr[3 + rng.randrange(2)]
    E2 = energy(sd, g0)
    if E2 is None: continue
    nev += 1; hist[E2] = hist.get(E2, 0) + 1
    if E2 <= E or rng.random() < pow(2.718281828, -(E2 - E) / temp):
        seeds, f0, E = sd, g0, E2
        if E < best: best = E; print("  t=%.0f best %d after %d states" % (time.time() - t0, E, nev), flush=True)
print("DONE 64 points start=%s seed=%d states=%d best=%d (per form %.3f) histogram(lowest)=%s" % (start, seed, nev, best, best / n, {k: hist[k] for k in sorted(hist)[:8]}))
