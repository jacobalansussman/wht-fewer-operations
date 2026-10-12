# x-2-floorhatch/foreign.py : the floor's bookkeeping run on the night's circuits THROUGH A TREE THAT IS NOT THEIR OWN.  Count (G).
# For a circuit (ordered wires, exact replay by u-8's parser) and a cube tree given by an invertible bit matrix on the addresses:
# a gate is NEW AT a node X when its wire cut down to X is not zero, not one input, and not proportional to the cut of an
# earlier wire.  n(X) = gates new at X.  Halves X0, X1:  n(X) = n(X0) + n(X1) + E(X) - B(X)  [E: new at X and at neither half;
# B: new at both halves].  d(X) = E - B - |X|/2 - 1.  The excess  e = gates - (N - 1 + (N/2) log2 N) = sum of d over all nodes,
# for EVERY tree.  The floor theorem says d >= 0 at every node of the circuit's OWN tree.  Printed per level: sum of n, E, B, d,
# the least d, and the largest number of "leaf" nodes one gate has (nodes where it is new but new at neither half).
import sys, os, random
from math import gcd
os.chdir('waves/wave-06/u-8-compose'); exec(open('compose.py').read().split("if __name__ == '__main__':")[0])
def own_basis(vecs, N, k):
    sup = sorted({frozenset(i for i in range(N) if v[i] != 0) for v in vecs}, key=len); basis = []; span = {0}
    for s in sup:
        b = min(s)
        for x in s:
            if (x ^ b) not in span: basis.append(x ^ b); span = span | {y ^ x ^ b for y in span}
    assert len(basis) == k; return basis
def cut(v, X):
    c = [v[i] for i in X]; g = 0
    for t in c: g = gcd(g, t)
    if g == 0: return None
    s = next(t for t in c if t); s = g if s > 0 else -g
    return tuple(t // s for t in c)
def book(vecs, N, k, basis):
    # address with coordinates c (bit j of c multiplies basis[j]); node = top bits of c fixed
    addr = []
    for c in range(N):
        x = 0
        for j in range(k):
            if c >> j & 1: x ^= basis[j]
        addr.append(x)
    assert len(set(addr)) == N
    lev = {}; leaves = [0] * len(vecs)
    def rec(X):
        seen = set(); nx = set()
        for g, v in enumerate(vecs):
            c = cut(v, X)
            if c is None or sum(1 for t in c if t) < 2 or c in seen: continue
            seen.add(c); nx.add(g)
        s = len(X)
        if s == 1: return nx
        n0 = rec(X[:s // 2]); n1 = rec(X[s // 2:]); assert n0 <= nx and n1 <= nx
        E = nx - n0 - n1; B = n0 & n1
        for g in E: leaves[g] += 1
        t = lev.setdefault(s, [0, 0, 0, 0, 10 ** 9]); d = len(E) - len(B) - s // 2 - 1
        t[0] += len(nx); t[1] += len(E); t[2] += len(B); t[3] += d; t[4] = min(t[4], d)
        return nx
    rec(addr)
    return lev, max(leaves)
def run(label, path, maps):
    g = parse(path); N = npts(g); W = replay(g, N); k = N.bit_length() - 1
    vecs = []
    for (name, *_) in g:
        v = W[name]; assert all(t.denominator == 1 for t in v); vecs.append([int(t) for t in v])
    ob = own_basis(vecs, N, k); fl = N - 1 + (N // 2) * k
    for mname, mk in maps:
        basis = mk(ob, k); lev, ml = book(vecs, N, k, basis)
        tot = sum(lev[s][3] for s in lev)
        assert tot == len(vecs) - fl, (tot, len(vecs), fl)
        print('%-14s N=%2d gates=%3d e=%2d  tree %-9s | size: sum n, E, B, d, least d | %s | most leaves of one gate %d'
              % (label, N, len(vecs), len(vecs) - fl, mname, '  '.join('%d: %d %d %d %+d %+d' % (s, *lev[s]) for s in sorted(lev) if s > 2), ml))
def own(ob, k): return ob
def rev(ob, k): return ob[::-1]
def rot(ob, k): return ob[1:] + ob[:1]
def shear(ob, k): return [ob[j] ^ (ob[j + 1] if j + 1 < k else 0) for j in range(k)]
def mkrand(seed):
    def f(ob, k):
        r = random.Random(seed)
        while True:
            b = [r.randrange(1, 1 << k) for _ in range(k)]; span = {0}
            for x in b:
                if x in span: break
                span |= {y ^ x for y in span}
            else: return b
    return f
ID2 = ID
maps = [('own', own), ('reversed', rev), ('rotated', rot), ('sheared', shear), ('random1', mkrand(1)), ('random2', mkrand(2))]
for label, path in (('the 19', ID2 + 'g-1-tightwires/h8_19gates.txt'), ('staircase 8', ID2 + 'e2-0-pieces/slp_8.txt'), ('staircase 16', ID2 + 'e2-0-pieces/slp_16.txt'),
                    ('second 52', ID2 + 'h-1-staircase3/slp16_52_from54.txt'), ('staircase 32', ID2 + 'e2-0-pieces/slp_32.txt'), ('staircase 64', ID2 + 'e2-0-pieces/slp_64.txt')):
    run(label, path, maps if '64' not in label else maps[:4])
