# x-2-floorhatch/dirtybook.py : the floor's bookkeeping on u-9's "dirty" circuit (3.2 N gates, outputs congruent to the transform
# modulo 4, NOT equal to it).  Count (G).  Exact whole numbers.  The circuit is rebuilt by u-9's own construction (dirty.py).
# Per level of the cube tree: n = gates new at the nodes, E = new at a node and at neither half, B = new at both halves.
# For the exact transform E >= s/2 + 1 at every node of size s (the outputs come in pairs with the same two halves).
# Question: which of the two numbers does the modulo-4 object change?
import sys
from math import gcd
def pc(v): return bin(v).count("1")
def build_all(k):
    N = 1 << k; wires = []
    def gate(a, u, b, v):
        w = [a * p + b * q for p, q in zip(u, v)]; wires.append(w); return w
    unit = [[1 if i == x else 0 for i in range(N)] for x in range(N)]; tsum = {}
    for x in range(N): tsum[(k, x)] = unit[x]
    for d in range(k - 1, -1, -1):
        for p in range(1 << d): tsum[(d, p)] = gate(1, tsum[(d + 1, 2 * p)], 1, tsum[(d + 1, 2 * p + 1)])
    def build(d, p, dirs):
        if not dirs: return {0: tsum[(d, p)]}
        if len(dirs) == 1 or d == k:
            out = {0: tsum[(d, p)]}; span = [0]
            for i in dirs: span = span + [u | (1 << i) for u in reversed(span)]
            for a in range(1, len(span)):
                i = (span[a] ^ span[a - 1]).bit_length() - 1; dd = k - i; w = out[span[a - 1]]
                for q in range(1 << dd):
                    if q & 1: w = gate(1, w, 2, tsum[(dd, q)])
                out[span[a]] = w
            return out
        h = len(dirs) // 2
        A = build(d + 1, 2 * p, dirs[:h]); B = build(d + 1, 2 * p + 1, dirs[h:])
        return {u1 | u2: gate(1, A[u1], 1, B[u2]) for u1 in A for u2 in B}
    out = build(0, 0, list(range(k)))
    assert all((out[y][x] - (-1) ** pc(y & x)) % 4 == 0 for y in range(N) for x in range(N))
    return wires, N, max(abs(t) for w in wires for t in w)
def cut(v, X):
    c = [v[i] for i in X]; g = 0
    for t in c: g = gcd(g, t)
    if g == 0: return None
    s = next(t for t in c if t); s = g if s > 0 else -g
    return tuple(t // s for t in c)
def book(vecs, N):
    lev = {}
    def rec(X):
        seen = set(); nx = set()
        for g, v in enumerate(vecs):
            c = cut(v, X)
            if c is None or sum(1 for t in c if t) < 2 or c in seen: continue
            seen.add(c); nx.add(g)
        s = len(X)
        if s == 1: return nx
        n0 = rec(X[:s // 2]); n1 = rec(X[s // 2:]); E = nx - n0 - n1; B = n0 & n1
        t = lev.setdefault(s, [0, 0, 0, 0]); t[0] += 1; t[1] += len(nx); t[2] += len(E); t[3] += len(B)
        return nx
    rec(list(range(N))); return lev
for k in range(2, 8):
    wires, N, mx = build_all(k); lev = book(wires, N)
    print('N=%3d gates=%3d (%.2f N) largest entry %d | size: nodes, sum n, E, B, and (s/2 + 1) x nodes | %s'
          % (N, len(wires), len(wires) / N, mx, '  '.join('%d: %d %d %d %d (%d)' % (s, lev[s][0], lev[s][1], lev[s][2], lev[s][3], lev[s][0] * (s // 2 + 1)) for s in sorted(lev) if s > 2)))
