#!/usr/bin/env python3
"""place19.py (p-0-classtest): k-cross/hyb3.py (the 13-rectangle shape of g-1's 19-gate circuit; all 8! input wirings, all output
labellings; necessary conditions, then the full linear test) with ONE change: arithmetic modulo a large prime P = 1 (mod 12) instead
of fractions, so that tau may be a root of unity (i, a cube root, a sixth root) as well as a rational.
A count modulo one prime is a CANDIDATE count (an accidental zero has chance about 1/P per test); hyb3 is the exact reference
(288 for generic rational tau, 10,752 for the transform) and the generic control here must reproduce 288.
Kernel: K = [[1,1],[1,tau]] cubed, entry tau^(number of common 1-bits of row address and column address).
usage: place19.py name=value ...   value: an integer, a/b, 'i', 'w3', 'w6' (primitive roots of unity of order 4, 3, 6 modulo P)"""
import sys, time
from itertools import permutations
P = 1000000093
def is_prime(n):
    i = 2
    while i * i <= n:
        if n % i == 0: return False
        i += 1
    return True
while not (P % 12 == 1 and is_prime(P)): P += 1
inv = lambda x: pow(x, P - 2, P)
def root(order):
    g = 2
    while True:
        r = pow(g, (P - 1) // order, P)
        if all(pow(r, d, P) != 1 for d in range(1, order)): return r
        g += 1
def parse(s):
    if s == 'i': return root(4)
    if s == 'w3': return root(3)
    if s == 'w6': return root(6)
    if '/' in s: a, b = s.split('/'); return int(a) * inv(int(b) % P) % P
    return int(s) % P
terms = [((1,2,4,7),(7,)), ((0,3,5,6),(5,)), ((1,7),(6,)), ((0,6),(4,)), ((3,5),(3,)), ((2,4),(1,)),
         ((0,),(0,7)), ((6,),(1,6)), ((1,),(2,5)), ((7,),(3,4)), ((5,),(0,1,6,7)), ((4,),(2,3,4,5))]
exc = {2:{7,1}, 3:{5,3}, 7:{7,6,3,4}, 1:{7,6,2,5}, 4:{7,1,2,3,4,5}, 5:{5,3,0,1,6,7}, 6:{5,4,1,6}, 0:{5,4,0,7}}
pairs = [(a, b) for a in range(8) for b in range(a+1, 8) if 8 - len(exc[a] | exc[b]) >= 2]
order = [2, 3, 7, 1, 6, 0, 4, 5]
def in_span(vecs, target):
    rows = [list(r) for r in zip(*(vecs + [target]))]; r = 0; ncol = len(vecs)
    for c in range(ncol):
        pv = next((i for i in range(r, len(rows)) if rows[i][c]), None)
        if pv is None: continue
        rows[r], rows[pv] = rows[pv], rows[r]; iv = inv(rows[r][c])
        for i in range(len(rows)):
            if i != r and rows[i][c]:
                f = rows[i][c] * iv % P
                rows[i] = [(x - f * y) % P for x, y in zip(rows[i], rows[r])]
        r += 1
    return all(row[-1] == 0 for row in rows[r:])
def full(Kp):
    c = [None] * 8
    for i in range(8):
        if i not in (1, 7): c[i] = Kp[2][i]
    lam = Kp[2][0] * inv(Kp[3][0]) % P
    c[1] = lam * Kp[3][1] % P; c[7] = lam * Kp[3][7] % P
    if any(x == 0 for x in c): return False
    a = [None] * 8
    for j in range(8):
        S = [i for i in range(8) if i not in exc[j]]
        rr = {Kp[j][i] * inv(c[i]) % P for i in S}
        if len(rr) != 1: return False
        a[j] = rr.pop()
    R = [(Kp[j][i] - a[j] * c[i]) % P for j in range(8) for i in range(8)]
    vecs = [[(a[j] * c[i] % P if (j in nu and i in mu) else 0) for j in range(8) for i in range(8)] for (nu, mu) in terms]
    return in_span(vecs, R)
def run(name, K):
    cache = {}
    def prop(r1, r2, mask):
        key = (r1, r2, mask)
        if key in cache: return cache[key]
        S = [s for s in range(8) if mask >> s & 1]; u, v = K[r1], K[r2]
        res = all((u[S[0]] * v[s] - u[s] * v[S[0]]) % P == 0 for s in S[1:]); cache[key] = res; return res
    t0 = time.time(); cand = 0; okc = 0
    for sig in permutations(range(8)):
        masks = {}
        for (x, y) in pairs:
            un = {sig[i] for i in exc[x] | exc[y]}
            masks[(x, y)] = sum(1 << s for s in range(8) if s not in un)
        pi = {}
        def dfs(i):
            nonlocal cand, okc
            if i == 8:
                cand += 1
                if full([[K[pi[j]][sig[ii]] for ii in range(8)] for j in range(8)]): okc += 1
                return
            j = order[i]
            for r in range(8):
                if r in pi.values(): continue
                good = True
                for jj in order[:i]:
                    x, y = (jj, j) if jj < j else (j, jj)
                    if (x, y) in masks:
                        ra, rb = (pi[jj], r) if jj < j else (r, pi[jj])
                        if not prop(ra, rb, masks[(x, y)]): good = False; break
                if good: pi[j] = r; dfs(i + 1); del pi[j]
        dfs(0)
    print('tau = %-6s : placements passing the necessary conditions %6d ; passing the FULL test modulo P %6d   (%.0f s)' % (name, cand, okc, time.time() - t0), flush=True)
print('P =', P)
for spec in sys.argv[1:]:
    t = parse(spec)
    run(spec, [[pow(t, bin(a & x).count('1'), P) for x in range(8)] for a in range(8)])
