#!/usr/bin/env python3
"""h-0 onepergate / anyex.py : can ONE wire with ANY coefficients replace two or three wires of a record circuit?  Count (G).  Exact.
Around the 19-gate and the 20-gate circuit: remove 2 or 3 helpers (at least one of them over-limit), add ONE new wire w.
w is not taken from a pool: it ranges over EVERY point that lies on two different lines through pairs of the wires that remain
(inputs, remaining helpers, outputs).  A wire of a circuit must lie on such a pair of lines (one gate makes it, one reads it),
so this is every single wire, with any coefficients, that could do the job.  Feasibility: exact collinearity (integer Gram
determinants, entries small enough for 64-bit integers; asserted).
cost = gates + over-limit gate wires; both starts have cost 24; a hit is cost <= 23.
usage: anyex.py c19|c20
"""
import sys, itertools, math
import numpy as np
def wht(v):
    v = list(v); n = len(v); h = 1
    while h < n:
        for i in range(0, n, 2 * h):
            for j in range(i, i + h):
                a, b = v[j], v[j + h]; v[j], v[j + h] = a + b, a - b
        h *= 2
    return v
def nz(v): return sum(1 for x in v if x != 0)
def norm(v):
    g = 0
    for x in v: g = math.gcd(g, int(x))
    if g == 0: return None
    s = next(x for x in v if x != 0); s = g if s > 0 else -g
    return tuple(int(x) // s for x in v)
N = 8
ins = [tuple(int(i == j) for j in range(N)) for i in range(N)]
outs = [norm([(-1) ** bin(w & x).count('1') for x in range(N)]) for w in range(N)]
def start(name):
    if name == 'c19':
        g = [{0: 1, 7: 1}, {1: 1, 6: 1}, {2: 1, 5: -1}, {3: 1, 4: -1}, {0: 1, 7: 1, 1: -1, 6: -1}, {2: 1, 5: -1, 3: 1, 4: -1}]
        c = [1, -1, -1, -1, 1, 1, -1, 1]
        def fl(v, *ps):
            v = list(v)
            for p in ps: v[p] = -v[p]
            return v
        H = []
        for d in g:
            v = [0] * 8
            for p, x in d.items(): v[p] = x
            H.append(norm(v))
        return H + [norm(v) for v in (c, fl(c, 7), fl(c, 5), fl(c, 7, 6), fl(c, 5, 4))]
    rows = ["1 1 0 0 0 0 0 0", "0 0 1 -1 0 0 0 0", "1 1 -1 1 0 0 0 0", "1 1 1 1 0 0 0 0", "1 -1 1 -1 0 0 0 0", "0 0 0 0 1 1 0 0", "0 0 0 0 0 0 1 -1",
            "0 0 0 0 1 1 1 -1", "0 0 0 0 1 1 -1 -1", "0 0 0 0 1 -1 -1 1", "1 1 1 1 1 1 -1 -1", "1 -1 1 -1 1 -1 -1 1"]
    return [norm([int(z) for z in r.split()]) for r in rows]
def over(w): return nz(w) * nz(wht(w)) != N
def feasible(helpers):
    V = ins + list(helpers) + [o for o in outs if o not in helpers]; m = len(V)
    U = np.array(V, dtype=np.int64); assert np.abs(U).max() < 2000
    G = U @ U.T
    I, J, K = np.array(list(itertools.combinations(range(m), 3))).T
    det = (G[I, I] * (G[J, J] * G[K, K] - G[J, K] ** 2) - G[I, J] * (G[I, J] * G[K, K] - G[J, K] * G[I, K]) + G[I, K] * (G[I, J] * G[J, K] - G[J, J] * G[I, K]))
    col = np.nonzero(det == 0)[0]
    just = {}
    for t in col:
        a, b, c = int(I[t]), int(J[t]), int(K[t])
        just.setdefault(a, []).append((b, c)); just.setdefault(b, []).append((a, c)); just.setdefault(c, []).append((a, b))
    have = set(range(N)); todo = list(range(N, m)); ch = True
    while ch and todo:
        ch = False; rest = []
        for w in todo:
            if any(p in have and q in have for p, q in just.get(w, [])): have.add(w); ch = True
            else: rest.append(w)
        todo = rest
    return not todo
def normrows(P):
    g = np.gcd.reduce(np.abs(P), axis=1); g[g == 0] = 1; P = P // g[:, None]
    first = np.argmax(P != 0, axis=1); sgn = np.sign(P[np.arange(len(P)), first]); sgn[sgn == 0] = 1
    return P * sgn[:, None]
def candidates(base):
    """every point, not in base, on two different lines through pairs of base wires"""
    U = np.array(base, dtype=np.int64); n = len(base); Gm = U @ U.T; bs = set(base); out = set()
    for i in range(n):
        for j in range(i + 1, n):
            a, b, c = int(Gm[i, i]), int(Gm[i, j]), int(Gm[j, j]); det = a * c - b * b
            xi = U @ U[i]; xj = U @ U[j]
            P = det * U - np.outer(c * xi - b * xj, U[i]) - np.outer(a * xj - b * xi, U[j]); Pn = normrows(P)
            zero = ~np.any(Pn != 0, axis=1); groups = {}
            for t in range(n):
                if not zero[t]: groups.setdefault(Pn[t].tobytes(), []).append(t)
            for grp in groups.values():
                for p, q in itertools.combinations(grp, 2):
                    cidx = int(np.nonzero(P[q])[0][0]); num = int(P[p][cidx]); den = int(P[q][cidx])
                    w = norm([den * x - num * y for x, y in zip(base[p], base[q])])
                    if w is not None and w not in bs and max(abs(x) for x in w) < 1000: out.add(w)
    return out
name = sys.argv[1]; H = start(name); assert feasible(H)
c0 = 8 + len(H) + sum(map(over, H)); print('%s: %d gates, cost %d; start circuit replays: True' % (name, 8 + len(H), c0), flush=True)
tested = hits = ncand = 0; mags = {}; found = []
for r in (2, 3):
    for rem in itertools.combinations(range(len(H)), r):
        wr = sum(1 + over(H[i]) for i in rem)
        if wr < 3: continue
        keep = [h for i, h in enumerate(H) if i not in rem]
        cand = candidates(ins + keep + outs); ncand += len(cand)
        for w in cand:
            ww = 1 + over(w)
            if ww >= wr: continue                      # the new wire must be cheaper than what was removed
            tested += 1
            key = tuple(sorted({abs(x) for x in w if x})); mags[key] = mags.get(key, 0) + 1
            if feasible(keep + [w]):
                hits += 1
                if len(found) < 10: found.append((rem, w))
    print('   removals of %d helpers done: tested so far %d, hits %d' % (r, tested, hits), flush=True)
print('%s: remove 2 or 3 helpers (weight >= 3), add one wire with any coefficients: %d candidate points in all, %d tested, %d circuits with cost < %d' % (name, ncand, tested, hits, c0))
print('   sets of |entries| among the tested wires (the pool is not bounded in advance):', sorted(mags.items(), key=lambda z: -z[1])[:25])
for rem, w in found: print('   HIT: removed', [H[i] for i in rem], 'added', w, 'over-limit' if over(w) else 'tight')
