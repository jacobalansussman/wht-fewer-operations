#!/usr/bin/env python3
"""lift16.py (p-2-mirror64class): 16 points, subset-sum kernel.  The three boxes with REDUNDANT coordinates:
read rt >= 6 numbers (start points need not be independent), middle rt' x rt, write from rt' numbers.
Start sets: rt points of targets + pool with at most 3 pool points, such that every target is reached by line gates inside
targets + start set.  read cost = (11 + h - rt) + 15 - rt, write cost = 11 + h' - rt', final additions 15,
middle: at least one gate per distinct row with two or more non-zeros, at most (non-zeros - 1) per such row.  Exact fractions."""
import sys, itertools, random
from fractions import Fraction as Fr
import mir
k = [[1, 1], [1, 0]]
M = mir.mirror(k, 2); n = 16; r = mir.rank(M)
cols = [[M[i][j] for i in range(n)] for j in range(n)]
cp, cm = mir.points(cols); rp, rm = mir.points(M)
_, _, Wr, _ = mir.reduced(cp, r, "read", maxx=-1); _, _, Ww, _ = mir.reduced(rp, r, "write", maxx=-1)
nT = 11
def feasible(W, rt, maxh=3):
    nW = len(W)
    trips = [sum(1 << i for i in c) for c in itertools.combinations(range(nW), 3) if mir.rank([W[i] for i in c]) == 2]
    fullT = (1 << nT) - 1; out = []
    for h in range(0, maxh+1):
        for X in itertools.combinations(range(nT, nW), h):
            xm = sum(1 << i for i in X); allowed = fullT | xm
            tm = [t for t in trips if t & allowed == t]
            for Bt in itertools.combinations(range(nT), rt - h):
                S = xm | sum(1 << i for i in Bt); ch = True
                while ch:
                    ch = False
                    for t in tm:
                        if t & S != t and bin(t & S).count('1') == 2: S |= t; ch = True
                if S & fullT == fullT: out.append((h, Bt + X))
    return out
def solve(A, v):
    nA = len(A); aug = [[Fr(x) for x in A[i]] + [Fr(v[i])] for i in range(nA)]; piv = []; rr = 0
    for cc in range(nA):
        p = next((i for i in range(rr, nA) if aug[i][cc] != 0), None)
        if p is None: continue
        aug[rr], aug[p] = aug[p], aug[rr]; f = aug[rr][cc]; aug[rr] = [x/f for x in aug[rr]]
        for i in range(nA):
            if i != rr and aug[i][cc] != 0:
                f = aug[i][cc]; aug[i] = [x - f*y for x, y in zip(aug[i], aug[rr])]
        piv.append(cc); rr += 1
    z = [Fr(0)]*nA
    for i, cc in enumerate(piv): z[cc] = aug[i][nA]
    return z
zr = [solve(M, v) for v in Wr]
val = [[sum(Fr(Ww[s][j])*zr[t][j] for j in range(n)) for t in range(len(Wr))] for s in range(len(Ww))]
random.seed(3)
for rt in (7, 8):
    FR = feasible(Wr, rt); FW = feasible(Ww, rt)
    hr = {}; 
    for h, _ in FR: hr[h] = hr.get(h, 0) + 1
    print("coordinates rt = %d: feasible read start sets by number of pool points in them: %s ; write: %d sets" % (rt, sorted(hr.items()), len(FW)))
    if not FR or not FW: continue
    hmin = min(h for h, _ in FR); hminw = min(h for h, _ in FW)
    A = [B for h, B in FR if h == hmin]; Bw = [B for h, B in FW if h == hminw]
    if len(A) > 1200: A = random.sample(A, 1200)
    if len(Bw) > 1200: Bw = random.sample(Bw, 1200)
    read_cost = (nT + hmin - rt) + 15 - rt; write_cost = nT + hminw - rt
    nzm = [sum(1 << t for t in range(len(Wr)) if val[s][t] != 0) for s in range(len(Ww))]
    Am = [sum(1 << t for t in B) for B in A]
    cands = []
    for Bp in Bw:
        rws = [nzm[s] for s in Bp]
        for bi, bm in enumerate(Am):
            heavy = 0; tot = 0
            for rw in rws:
                c_ = bin(rw & bm).count('1'); tot += c_; heavy += (c_ >= 2)
            cands.append((heavy, tot, bi, Bp))
            if len(cands) > 400000: cands.sort(); cands = cands[:300]
    cands.sort(); cands = cands[:300]
    best = None
    for heavy, tot, bi, Bp in cands:
        B = A[bi]; seen = set(); lo = 0; hi = 0
        for s in Bp:
            sub = [val[s][t] for t in B]; nzc = [x for x in sub if x != 0]
            if len(nzc) >= 2:
                f = nzc[0]; key = tuple(x/f for x in sub)
                if key not in seen: seen.add(key); lo += 1; hi += len(nzc) - 1
        if best is None or (lo, hi) < best[0]: best = ((lo, hi), B, Bp)
    (lo, hi), B, Bp = best
    print("   least pool points: read %d, write %d  => read cost %d, write cost %d ; best middle over %d x %d pairs: between %d and %d gates" % (hmin, hminw, read_cost, write_cost, len(A), len(Bw), lo, hi))
    print("   TOTAL at 16 points with %d coordinates: 15 + %d + %d + middle = between %d and %d   (Yates 32, product of 4-point routes 40, three boxes with 6 coordinates 41)" % (rt, read_cost, write_cost, 15 + read_cost + write_cost + lo, 15 + read_cost + write_cost + hi))
    print("   read start", [("c%d" % t if t < nT else Wr[t]) for t in B]); print("   write start", [("e%d" % s if s < nT else Ww[s]) for s in Bp])
    for s in Bp: print("     ", [str(val[s][t]) for t in B])
    sys.stdout.flush()
