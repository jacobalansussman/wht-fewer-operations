#!/usr/bin/env python3
"""h5_flatrank.py [aa-cross]  ab-0's flat rank against ab-3's level-set-flats count.  Exact (Fractions / whole numbers).
A kernel g on the cube (the convolution 'output(y) = sum of g(x + y) input(x)').  FLAT RANK r(g): the least number of
flats F_1..F_r (cosets of subspaces, any dimensions) with g = sum of c_j * indicator(F_j), any rational c_j.
D(g): the largest dimension of a flat on which the spectrum of g (its transform) is constant.
Claim [derived in aa-cross.md]: r(g) >= k - D(g).   Checked here by exhaustive search at k = 3 and (r <= 3) at k = 4."""
import sys, itertools, time
from fractions import Fraction
def flats(k):
    N = 1 << k; subs = {(0,)}
    # all subspaces by closure
    front = [(0,)]
    while front:
        new = []
        for S in front:
            for v in range(1, N):
                if v not in S:
                    T = tuple(sorted(set(S) | {s ^ v for s in S}))
                    if T not in subs: subs.add(T); new.append(T)
        front = new
    out = {}
    for S in subs:
        for a in range(N):
            m = 0
            for s in S: m |= 1 << (s ^ a)
            out[m] = len(S).bit_length() - 1
    return out            # bitmask -> dimension
def wt(x): return bin(x).count("1")
def spectrum(g, k):
    N = 1 << k; return [sum(g[x] * (-1) ** wt(x & y) for x in range(N)) for y in range(N)]
def Dval(sp, FL):
    best = 0
    for m, d in FL.items():
        vals = {sp[y] for y in range(len(sp)) if (m >> y) & 1}
        if len(vals) == 1 and d > best: best = d
    return best
def solvable(masks, g, N):
    # is g = sum c_j 1_{F_j}?  points with the same membership pattern must have the same g; then a tiny linear system
    sig = {}
    for x in range(N):
        s = tuple((m >> x) & 1 for m in masks)
        if s in sig:
            if sig[s] != g[x]: return False
        else: sig[s] = g[x]
    if any(v != 0 for s, v in sig.items() if not any(s)): return False
    rows = [[Fraction(v) for v in s] + [Fraction(val)] for s, val in sig.items() if any(s)]
    r = len(masks); rk = 0
    for c in range(r):
        piv = next((i for i in range(rk, len(rows)) if rows[i][c] != 0), None)
        if piv is None: continue
        rows[rk], rows[piv] = rows[piv], rows[rk]; inv = 1 / rows[rk][c]; rows[rk] = [v * inv for v in rows[rk]]
        for i in range(len(rows)):
            if i != rk and rows[i][c] != 0:
                f = rows[i][c]; rows[i] = [a - f * b for a, b in zip(rows[i], rows[rk])]
        rk += 1
    return all(rw[-1] == 0 for rw in rows[rk:])
def flatrank(g, k, FL, rmax, secs):
    N = 1 << k; supp = sum(1 << x for x in range(N) if g[x]); ms = list(FL); t0 = time.time()
    for r in range(1, rmax + 1):
        n = 0
        for comb in itertools.combinations(ms, r):
            u = 0
            for m in comb: u |= m
            if supp & ~u: continue
            n += 1
            if solvable(comb, g, N): return r, comb
            if time.time() - t0 > secs: return ">= %d (search for %d stopped by the clock)" % (r, r), None
    return "> %d" % rmax, None
for k, rmax, secs in ((3, 4, 60), (4, 3, float(sys.argv[1]) if len(sys.argv) > 1 else 120)):
    N = 1 << k; FL = flats(k)
    kern = {"neighbour sums (weight 1)": [1 if wt(x) == 1 else 0 for x in range(N)],
            "neighbour sums plus the point itself (weight <= 1)": [1 if wt(x) <= 1 else 0 for x in range(N)],
            "sphere of radius 2": [1 if wt(x) == 2 else 0 for x in range(N)],
            "quadric signs +,+,-,-,+ by weight (the transform's kernel for even k)": [1 if wt(x) % 4 in (0, 1) else -1 for x in range(N)]}
    print("k=%d : %d flats" % (k, len(FL)))
    for name, g in kern.items():
        sp = spectrum(g, k); D = Dval(sp, FL); r, comb = flatrank(g, k, FL, rmax, secs / len(kern))
        print("   %-70s D = %d, bound k - D = %d, flat rank found: %s%s" % (name, D, k - D, r, "" if comb is None else "  flats (bit masks) " + " ".join("%x" % m for m in comb)))
# the dimension D for neighbour sums at larger k: weight constant on a flat <=> its directions are pairwise orthogonal even words
for k in (5, 6):
    N = 1 << k; FL = flats(k); sp = [k - 2 * wt(y) for y in range(N)]
    q = [1 if wt(x) % 4 in (0, 1) else -1 for x in range(N)]
    print("k=%d : %d flats ; D(neighbour sums) = %d (floor(k/2) = %d) ; D(quadric signs' spectrum) = %d" % (k, len(FL), Dval(sp, FL), k // 2, Dval(spectrum(q, k), FL)))
