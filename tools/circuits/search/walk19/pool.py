#!/usr/bin/env python3
"""g-1 pool.py: the pool of 'coset sign vectors' and its gates.  Count (G).  Exact integers.
A pool wire = a vector that is +-1 on a coset C of a subgroup of the addresses and 0 elsewhere, up to an overall sign.
Written (C, g): g a 0/1-valued function on C, the wire is (-1)^g on C.  g affine  <=> tight wire (coset character).
g quadratic <=> 'tight wire times a quadratic sign vector on a sub-cube' (the brief's pool).  maxdeg limits the degree of g.
usage: pool.py census k maxdeg      -> sizes, (s, s') histogram, number of collinear triples, hub capacities
"""
import sys, itertools, math
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from ref import wht, nz, norm, subspaces, RATIOS

def degree(vals, d):
    """algebraic degree of a function on a d-cube given by its 2^d values (0/1), via the Moebius transform"""
    a = list(vals); n = len(a); h = 1
    while h < n:
        for i in range(n):
            if i & h: a[i] ^= a[i ^ h]
        h *= 2
    return max((bin(i).count("1") for i in range(n) if a[i]), default=0)

def build_pool(k, maxdeg):
    N = 1 << k; pool = {}
    for V, d in subspaces(k).items():
        # a basis of V in echelon order, to index the coset as a d-cube
        basis = []; span = {0}
        for g in sorted(V):
            if g not in span: basis.append(g); span |= {x ^ g for x in span}
        reps = sorted({min(x ^ c for x in V) for c in range(N)})
        pts0 = []
        for t in range(1 << d):
            x = 0
            for i in range(d):
                if t >> i & 1: x ^= basis[i]
            pts0.append(x)
        for vals in itertools.product((0, 1), repeat=(1 << d) - 1):
            vals = (0,) + vals
            dg = degree(vals, d)
            if dg > maxdeg: continue
            for c in reps:
                v = [0] * N
                for t, x in enumerate(pts0): v[x ^ c] = -1 if vals[t] else 1
                pool[norm(v)] = (d, dg)
    return pool

def lines(pool):
    """all collinear triples (u, v, w) of pool wires, as index triples; each unordered triple once"""
    ws = sorted(pool); idx = {w: i for i, w in enumerate(ws)}; trip = set()
    for i in range(len(ws)):
        u = ws[i]
        for j in range(i):
            v = ws[j]
            for a, b in RATIOS:
                w = norm([a * x + b * y for x, y in zip(u, v)])
                if w is None or w == u or w == v: continue
                t = idx.get(w)
                if t is not None: trip.add(tuple(sorted((i, j, t))))
    return ws, sorted(trip)

if __name__ == "__main__":
    k, maxdeg = int(sys.argv[2]), int(sys.argv[3]); N = 1 << k
    pool = build_pool(k, maxdeg); ws, trip = lines(pool)
    S = [nz(w) for w in ws]; T = [nz(wht(w)) for w in ws]
    hist = {}
    for i, w in enumerate(ws):
        key = (S[i], T[i], pool[w][1]); hist[key] = hist.get(key, 0) + 1
    print("N = %d, functions of degree <= %d: %d pool wires, %d collinear triples (= possible gates, each usable three ways)" % (N, maxdeg, len(ws), len(trip)))
    print("   wires by (s, s', degree of g): %s" % sorted(hist.items()))
    # gate types by rise and drop
    types = {}
    for (a, b, c) in trip:
        for (u, v, w) in ((a, b, c), (a, c, b), (b, c, a)):
            lo, hi = sorted(((S[u], T[u]), (S[v], T[v])))
            r = max(0.0, math.log2(S[w] / min(S[u], S[v]))); d = max(0.0, math.log2(max(T[u], T[v]) / T[w]))
            key = (round(r + d, 2), round(r, 2), round(d, 2), lo, hi, (S[w], T[w])); types[key] = types.get(key, 0) + 1
    print("   gate types with the largest rise + drop (rise+drop, rise, drop, inputs (s,s'), output (s,s')): count")
    for key in sorted(types, reverse=True)[:14]: print("      %s : %d" % (key, types[key]))
    # hub capacity: for each wire, the number of OUTPUTS one gate away, and the partners' supports
    outs = [i for i, w in enumerate(ws) if S[i] == N and T[i] == 1]
    nb = {i: [] for i in range(len(ws))}
    for (a, b, c) in trip:
        for (u, v, w) in ((a, b, c), (a, c, b), (b, c, a)):
            if w in outs: nb[u].append((S[v], w)); nb[v].append((S[u], w))
    cap = {}
    for i in range(len(ws)):
        if i in outs: continue
        best = {}
        for sp, w in nb[i]: best[w] = min(best.get(w, 99), sp)
        key = (S[i], T[i], pool[ws[i]][1], tuple(sorted(best.values())))
        cap[key] = cap.get(key, 0) + 1
    print("   hubs: (s, s', degree) of a wire and the supports of the cheapest partners to each output it is one gate from: number of such wires")
    for key in sorted(cap):
        if key[3]: print("      %s : %d" % (key, cap[key]))
