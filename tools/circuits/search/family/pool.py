#!/usr/bin/env python3
"""e2-0-pieces: pools of 'piecewise characters' at 8 points and their lines.  Exact integer arithmetic.
Points are vectors up to scaling (primitive integer vector, first non-zero entry positive).
usage: pool.py stab|pm1|wide   -> prints sizes, writes <name>.json (points, maximal lines)"""
import sys, json, itertools
from math import gcd
from fractions import Fraction
N = 8; K = 3
def norm(v):
    g = 0
    for a in v: g = gcd(g, abs(a))
    if g == 0: return None
    v = tuple(a // g for a in v)
    for a in v:
        if a:
            return v if a > 0 else tuple(-b for b in v)
def dot(w, x): return bin(w & x).count('1') & 1
Y = [tuple((-1) ** dot(w, x) for x in range(N)) for w in range(N)]
E = [tuple(int(i == x) for i in range(N)) for x in range(N)]
def affine_subspaces():
    out = set()
    for d in range(K + 1):
        for basis in itertools.product(range(N), repeat=d):
            U = {0}
            for b in basis: U |= {u ^ b for u in U}
            if len(U) != 1 << d: continue
            for a in range(N): out.add(frozenset(a ^ u for u in U))
    return out
def stab_pool():
    P = set()
    quad = []
    for lin in range(N):
        for q in range(8):   # coefficients of x0x1, x0x2, x1x2
            def f(x, lin=lin, q=q):
                b = [(x >> i) & 1 for i in range(3)]
                return (dot(lin, x) + (q & 1) * b[0] * b[1] + ((q >> 1) & 1) * b[0] * b[2] + ((q >> 2) & 1) * b[1] * b[2]) & 1
            quad.append([f(x) for x in range(N)])
    for A in affine_subspaces():
        for f in quad:
            P.add(norm(tuple(((-1) ** f[x]) if x in A else 0 for x in range(N))))
    return P
def pm1_pool():
    P = set()
    for v in itertools.product((0, 1, -1), repeat=N):
        n = norm(v)
        if n: P.add(n)
    return P
def char_patterns(S):
    S = sorted(S); pats = set()
    for w in range(N):
        pats.add(tuple(Y[w][x] for x in S)); pats.add(tuple(-Y[w][x] for x in S))
    return S, pats
def wide_pool():
    """c1*y_w1 on S1 + c2*y_w2 on S2, S1,S2 disjoint, |S2|<=2 or S2 any?  Here: ratio 1 (all 0,+-1 vectors) plus
    ratio 2 with the '2' piece of size <= 2 or the '1' piece of size <= 2 (hub-like: an output with one or two entries changed)."""
    P = pm1_pool()
    subsets = [frozenset(x for x in range(N) if m >> x & 1) for m in range(1, 1 << N)]
    cp = {S: char_patterns(S) for S in subsets}
    for S1 in subsets:
        for S2 in subsets:
            if S1 & S2: continue
            if min(len(S1), len(S2)) > 2: continue
            l1, p1 = cp[S1]; l2, p2 = cp[S2]
            for a in p1:
                for b in p2:
                    v = [0] * N
                    for x, s in zip(l1, a): v[x] = s
                    for x, s in zip(l2, b): v[x] = 2 * s
                    P.add(norm(tuple(v)))
    return P
RAT = [(1, 1), (1, -1), (1, 2), (1, -2), (2, 1), (2, -1), (1, 3), (1, -3), (3, 1), (3, -1), (1, 4), (1, -4), (4, 1), (4, -1), (2, 3), (2, -3), (3, 2), (3, -2)]
def lines(P):
    P = sorted(P); idx = {p: i for i, p in enumerate(P)}
    L = set()
    for i, u in enumerate(P):
        for j in range(i + 1, len(P)):
            v = P[j]; on = {i, j}
            for a, b in RAT:
                w = norm(tuple(a * x + b * y for x, y in zip(u, v)))
                k = idx.get(w)
                if k is not None: on.add(k)
            if len(on) > 2: L.add(frozenset(on))
    # merge to maximal lines: two collinear sets sharing two points are the same line
    by_pair = {}
    Ls = sorted(L, key=len, reverse=True); maxl = []
    for l in Ls:
        l = set(l); key = None
        s = sorted(l)
        for a, b in itertools.combinations(s, 2):
            if (a, b) in by_pair: key = by_pair[(a, b)]; break
        if key is None:
            key = len(maxl); maxl.append(set())
        maxl[key] |= l
        s = sorted(maxl[key])
        for a, b in itertools.combinations(s, 2): by_pair[(a, b)] = key
    return P, [sorted(l) for l in maxl]
if __name__ == '__main__':
    name = sys.argv[1]
    P = {'stab': stab_pool, 'pm1': pm1_pool, 'wide': wide_pool}[name]()
    P |= set(E) | {norm(y) for y in Y}
    print(name, 'pool size', len(P), flush=True)
    from collections import Counter
    print(' support sizes', sorted(Counter(sum(1 for a in p if a) for p in P).items()))
    if name == 'stab' or len(sys.argv) > 2:
        P, L = lines(P)
        print(' maximal lines with >= 3 pool points:', len(L), ' by size', sorted(Counter(len(l) for l in L).items()))
        inc = Counter()
        for l in L:
            for p in l: inc[p] += 1
        print(' lines per point: min', min(inc.values()), 'max', max(inc.values()))
        json.dump({'P': P, 'L': L, 'inputs': [P.index(e) for e in E], 'outputs': [P.index(norm(y)) for y in Y]}, open(name + '.json', 'w'))
