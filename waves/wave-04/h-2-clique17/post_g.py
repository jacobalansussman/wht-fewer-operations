#!/usr/bin/env python3
"""post_g.py m W K leaves.txt  -- post2.py for any block size m <= 5 and any W: counting, clique lemma, zero-form lemma on
every count vector with at most K moves, up to the orthogonal group of the m-bit labels.   [h-2-clique17]   Exact integers."""
import sys, itertools
import numpy as np
m, W, K = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); NP = (1 << m) - 1
V = list(range(1, NP + 1))
def dot(a, b): return bin(a & b).count("1") & 1
pairs = [(i, j) for i in range(m) for j in range(i, m)]; npr = len(pairs)
mon = np.array([[(z >> i & 1) & (z >> j & 1) for z in V] for (i, j) in pairs], dtype=np.int64)
diag = [t for t, (i, j) in enumerate(pairs) if i == j]
Qs = np.arange(1, 1 << npr); bits = (Qs[:, None] >> np.arange(npr)[None, :]) & 1
lam = bits[:, diag].sum(axis=1) % 2
A1 = np.unique((bits[lam == 1] @ mon) % 2, axis=0); A0 = np.unique((bits[lam == 0] @ mon) % 2, axis=0)
def tv(a): return tuple((z ^ a) if dot(a, z) else z for z in V)
gens = [tv(a) for a in V if bin(a).count("1") % 2 == 0]
G = {tuple(V)}; frontier = [tuple(V)]
while frontier:
    new = []
    for g in frontier:
        for h in gens:
            c = tuple(h[g[i] - 1] for i in range(NP))
            if c not in G: G.add(c); new.append(c)
    frontier = new
P = np.array([[x - 1 for x in g] for g in G])
def canon(n):
    n = np.asarray(n, dtype=np.int64); T = np.zeros((len(P), NP), dtype=np.int64)
    np.put_along_axis(T, P, np.broadcast_to(n, (len(P), NP)), axis=1)
    return tuple(int(x) for x in T[np.lexsort(T.T[::-1])[0]])
def wclique(n, adj, cand):
    best = 0
    def bk(wR, Pm):
        nonlocal best
        if wR > best: best = wR
        if wR + sum(int(n[j]) for j in range(NP) if Pm >> j & 1) <= best: return
        while Pm:
            v = Pm & -Pm; i = v.bit_length() - 1
            bk(wR + int(n[i]), Pm & adj[i]); Pm &= ~v
    bk(0, cand); return best
def both(n):
    n = np.asarray(n, dtype=np.int64); cnt = A1 @ n
    assert cnt.min() >= W
    tight = np.unique(A1[cnt == W] * (n > 0), axis=0)
    adj = [0] * NP; intight = 0
    for row in tight:
        msk = sum(1 << i for i in range(NP) if row[i]); intight |= msk
        for i in range(NP):
            if row[i]: adj[i] |= msk & ~(1 << i)
    cl = wclique(n, adj, intight)
    if cl > W: return "clique", len(tight), cl
    c0 = A0 @ n
    for r in np.nonzero((c0 > 0) & (c0 <= 2 * W - 1))[0]:
        sel = sum(1 << i for i in range(NP) if A0[r][i] and n[i] > 0) & intight
        if 2 * wclique(n, adj, sel) > c0[r]: return "zero", len(tight), cl
    return "survives", len(tight), cl
def fmt(n): return " ".join("%s:%d" % (format(V[i], "0%db" % m), n[i]) for i in range(NP) if n[i])
classes = {}
for line in open(sys.argv[4]):
    p = line.split(); T = int(p[0]); fr = int(p[1]); n0 = list(map(int, p[2:]))
    free = [i for i in range(NP) if not fr >> i & 1]
    for e in range(0, K - T + 1):
        for comb in itertools.combinations_with_replacement(free, e):
            n = n0[:]
            for i in comb: n[i] += 1
            c = canon(n); classes.setdefault(sum(c), set()).add(c)
print("m = %d, W = %d (plain %d moves), up to %d moves; group of %d maps" % (m, W, m * W, K, len(P)))
if not classes: print("  no count vector with at most %d moves passes counting" % K)
for tot in sorted(classes):
    res = {"clique": 0, "zero": 0, "survives": 0}; lines = []
    for c in sorted(classes[tot]):
        kind, nt, cl = both(c); res[kind] += 1
        if kind == "survives": lines.append("     SURVIVES: %s  [tight selections %d, largest joined set %d]" % (fmt(c), nt, cl))
    print("  %d moves: %d count vectors pass counting; excluded by the clique lemma %d, by the zero-form lemma %d, SURVIVE %d"
          % (tot, len(classes[tot]), res["clique"], res["zero"], res["survives"]))
    for l in lines[:40]: print(l)
