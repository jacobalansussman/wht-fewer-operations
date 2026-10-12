#!/usr/bin/env python3
"""mypost.py K leaves.txt [more leaves files]   (n-2; my own code, exact integers, no numpy)
Reads leaves (T, frozen mask, n_1..n_31) of mycover.c or of h-2's cover.c, expands "leaf + extras on free directions"
up to K moves, reduces by the orthogonal group of the 5-bit labels (built here by backtracking over orthonormal bases,
not by generators), and applies counting, the clique lemma and the zero-form lemma with my own implementation.
"""
import sys, itertools
import os
m = 5; W = int(os.environ.get("NW", "4"))
V = list(range(1, 32))
par = lambda x: bin(x).count("1") & 1
# ---- forms: (d, o) -> truth table as a 31-bit mask
pairs = [(i, j) for i in range(m) for j in range(i + 1, m)]
def table(d, o):
    mk = 0
    for z in V:
        s = par(d & z)
        for t, (i, j) in enumerate(pairs):
            if (o >> t & 1) and (z >> i & 1) and (z >> j & 1): s ^= 1
        if s: mk |= 1 << (z - 1)
    return mk
F1 = []; F0 = []
for d in range(32):
    for o in range(1024):
        (F1 if par(d) else F0).append(table(d, o))
assert len(set(F1)) == 16384 and len(set(F0)) == 16384
F0 = [f for f in F0 if f]
# ---- the group: matrices g with g^T g = 1, i.e. ordered orthonormal bases (columns)
odd = [z for z in V if par(z)]
bases = []
def ext(cols):
    if len(cols) == m: bases.append(tuple(cols)); return
    for c in odd:
        if all(par(c & x) == 0 for x in cols): ext(cols + [c])
ext([])
def image(cols, z):
    r = 0
    for i in range(m):
        if z >> i & 1: r ^= cols[i]
    return r
G = [tuple(image(b, z) for z in V) for b in bases]
G = [g for g in G if len(set(g)) == 31]
assert len(G) == 720, len(G)
# symmetry checks: the group permutes the set of forms with q(I) = 1, and is transitive on the 15 odd non-centre directions
F1set = set(F1)
def permmask(g, mk):
    r = 0
    for i in range(31):
        if mk >> i & 1: r |= 1 << (g[i] - 1)
    return r
if "--checkgroup" in sys.argv:
    for g in G:
        assert all(permmask(g, f) in F1set for f in F1[::37]), "group does not keep q(I)"
    gens_ok = all(permmask(g, f) in F1set for g in G[:40] for f in F1)
    orb = {g[0] for g in G}          # orbit of 00001
    print("group order", len(G), "; keeps the forms with q(I)=1 (all forms, 40 maps; every 37th form, all maps):", gens_ok,
          "; orbit of 00001:", len(orb), "directions, all odd non-centre:", orb == set(odd) - {31}, "; centre fixed:", all(g[30] == 31 for g in G))
    sys.argv.remove("--checkgroup")
from operator import itemgetter as _ig
_GET = []
for _g in G:
    _inv = [0] * 31
    for _i in range(31): _inv[_g[_i] - 1] = _i
    _GET.append(_ig(*_inv))
def canon(n):
    n = tuple(n)                                            # image vector t[j] = n[i] with g(i) = j; smallest over the 720 maps
    return min(get(n) for get in _GET)
def sel(mk, n): return sum(n[i] for i in range(31) if mk >> i & 1)
def wclique(n, adj, cand):
    best = [0, 0]
    def bk(R, wR, P):
        if wR > best[0]: best[0] = wR; best[1] = R
        if wR + sum(n[j] for j in range(31) if P >> j & 1) <= best[0]: return
        while P:
            v = P & -P; i = v.bit_length() - 1
            bk(R | v, wR + n[i], P & adj[i]); P &= ~v
    bk(0, 0, cand); return best
def names(mk): return [format(i + 1, "05b") for i in range(31) if mk >> i & 1]
def judge(n):
    used = sum(1 << i for i in range(31) if n[i])
    cnts = [sel(f, n) for f in F1]
    assert min(cnts) >= W, "does not pass counting"
    tight = {f & used for f, c in zip(F1, cnts) if c == W}
    adj = [0] * 31; intight = 0
    for t in tight:
        intight |= t
        for i in range(31):
            if t >> i & 1: adj[i] |= t & ~(1 << i)
    cl = wclique(n, adj, intight)
    if cl[0] > W: return "clique", len(tight), cl[0], None
    for f in F0:
        c = sel(f, n)
        if 0 < c <= 2 * W - 1:
            t = wclique(n, adj, f & used & intight)
            if 2 * t[0] > c: return "zero", len(tight), cl[0], (c, t[0], names(f & used), names(t[1]))
    return "survives", len(tight), cl[0], None
if __name__ == "__main__":
    K = int(sys.argv[1]); classes = {}; raw = 0
    for fn in sys.argv[2:]:
        for line in open(fn):
            p = line.split(); T = int(p[0]); fr = int(p[1]); n0 = list(map(int, p[2:]))
            free = [i for i in range(31) if not fr >> i & 1]
            for e in range(0, K - T + 1):
                for comb in itertools.combinations_with_replacement(free, e):
                    n = n0[:]
                    for i in comb: n[i] += 1
                    raw += 1; c = canon(n); classes.setdefault(sum(c), set()).add(c)
    print("K =", K, "; vectors before symmetry:", raw)
    for tot in sorted(classes):
        res = {"clique": 0, "zero": 0, "survives": 0}; notes = []; hist = {}
        for c in sorted(classes[tot]):
            kind, nt, cl, info = judge(list(c)); res[kind] += 1; hist[cl] = hist.get(cl, 0) + 1
            if kind != "clique":
                notes.append("    %s  %s  tight %d, largest joined set %d  %s" % (kind.upper(), " ".join("%s:%d" % (format(i + 1, "05b"), c[i]) for i in range(31) if c[i]), nt, cl, info))
        print("%d moves: %d classes; clique-excluded %d, zero-form-excluded %d, survive %d; largest joined set histogram %s" % (tot, len(classes[tot]), res["clique"], res["zero"], res["survives"], sorted(hist.items())))
        for l in notes: print(l)
    import pickle; pickle.dump(classes, open("classes_W%d_K%d.pkl" % (W, K), "wb"))
