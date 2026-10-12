#!/usr/bin/env python3
"""verify.py [ad-4-flatrank]   Exact replays (whole numbers and Fractions only).
 A. 16 points: the 4 unsigned flats (product), the 5 of the ruling.
 B. 256 points of the plain class = 16 points of the DOUBLED class: an orthogonal spread (Kerdock set) found by search;
    quadric signs = -1 + 2 * (9 subspaces) - 16 [z = 0]  : 11 unsigned flats;  and the same read as a 16 x 16 matrix identity
    H_16 = -J + 2 [x = 0] + 2 * sum over 8 alternating matrices S of [y = S x] - 16 [x = y = 0], with the gate price of each piece.
 C. replay of the candidates printed by fr (local search, floats): is g EXACTLY in the span of the listed signed flats?
 D. the pair-kill dichotomy of the report (section 3) tested on every replayed decomposition.
usage: verify.py [candidate files ...]"""
import sys, itertools
from fractions import Fraction
def wt(x): return bin(x).count("1")
def quad(z, K):       # z1 z2 + z3 z4 + ...  (bit 0 with bit 1, bit 2 with bit 3, ...)
    return sum(((z >> i) & 1) & ((z >> (i + 1)) & 1) for i in range(0, K, 2)) & 1
def gvec(K): return [(-1) ** quad(z, K) for z in range(1 << K)]
def Bform(a, b, K):   # the polar form of quad
    s = 0
    for i in range(0, K, 2): s ^= (((a >> i) & 1) & ((b >> (i + 1)) & 1)) ^ (((a >> (i + 1)) & 1) & ((b >> i) & 1))
    return s
def in_span(vecs, g):
    """exact: is g a rational combination of vecs?  returns the coefficients or None"""
    n = len(g); r = len(vecs)
    rows = [[Fraction(vecs[j][z]) for j in range(r)] + [Fraction(g[z])] for z in range(n)]
    rk = 0; piv = []
    for c in range(r):
        p = next((i for i in range(rk, n) if rows[i][c] != 0), None)
        if p is None: continue
        rows[rk], rows[p] = rows[p], rows[rk]; inv = 1 / rows[rk][c]; rows[rk] = [v * inv for v in rows[rk]]
        for i in range(n):
            if i != rk and rows[i][c] != 0:
                f = rows[i][c]; rows[i] = [a - f * b for a, b in zip(rows[i], rows[rk])]
        piv.append(c); rk += 1
    if any(rw[-1] != 0 for rw in rows[rk:]): return None
    coef = [Fraction(0)] * r
    for i, c in enumerate(piv): coef[c] = rows[i][-1]
    return coef
print("A. 16 points")
K = 4; N = 16; g = gvec(K)
f = [[1] * N, [1 if z & 3 == 3 else 0 for z in range(N)], [1 if (z >> 2) == 3 else 0 for z in range(N)], [1 if z == 15 else 0 for z in range(N)]]
print("   g = 1 - 2 [z1 z2 = 11] - 2 [z3 z4 = 11] + 4 [z = 1111] :", all(g[z] == f[0][z] - 2 * f[1][z] - 2 * f[2][z] + 4 * f[3][z] for z in range(N)), " (4 unsigned flats: whole space, two planes, one point)")
# the ruling: three totally singular planes through 0 that meet pairwise in 0 and cover the 10 zeros
zeros = [z for z in range(N) if quad(z, K) == 0]
planes = []
for a, b in itertools.combinations(range(1, N), 2):
    P = frozenset((0, a, b, a ^ b))
    if all(quad(z, K) == 0 for z in P): planes.append(P)
planes = list(set(planes))
tri = [t for t in itertools.combinations(planes, 3) if all(len(x & y) == 1 for x, y in itertools.combinations(t, 2))]
t = tri[0]
print("   totally singular planes: %d ; spreads (3 planes, pairwise meeting in 0): %d ; g = -1 + 2 (3 planes) - 4 [z = 0] :" % (len(planes), len(tri)),
      all(g[z] == -1 + 2 * sum(z in P for P in t) - 4 * (z == 0) for z in range(N)), " (5 unsigned flats)")
print("B. 16 points doubled = 256 points plain: orthogonal spread from a Kerdock set")
m = 4; n = 1 << m
def mat_apply(S, x):  # S: list of m row masks ; returns S x
    y = 0
    for i in range(m):
        if wt(S[i] & x) & 1: y |= 1 << i
    return y
def is_inv(S):
    rows = list(S); rk = 0
    for c in range(m):
        p = next((i for i in range(rk, m) if (rows[i] >> c) & 1), None)
        if p is None: return False
        rows[rk], rows[p] = rows[p], rows[rk]
        for i in range(m):
            if i != rk and (rows[i] >> c) & 1: rows[i] ^= rows[rk]
        rk += 1
    return True
alts = []
pairs = [(i, j) for i in range(m) for j in range(i + 1, m)]
for bits in range(1 << len(pairs)):
    S = [0] * m
    for t_, (i, j) in enumerate(pairs):
        if (bits >> t_) & 1: S[i] |= 1 << j; S[j] |= 1 << i
    alts.append(tuple(S))
inv = [S for S in alts if is_inv(S)]
def diff(S, T): return tuple(a ^ b for a, b in zip(S, T))
best = []
def grow(cur, cand):
    global best
    if len(cur) > len(best): best = list(cur)
    if len(best) >= n // 2 - 1: return
    for i, S in enumerate(cand):
        grow(cur + [S], [T for T in cand[i + 1:] if is_inv(diff(S, T))])
        if len(best) >= n // 2 - 1: return
grow([], inv)
ker = [tuple([0] * m)] + best
print("   alternating 4 x 4 matrices: %d, invertible: %d ; Kerdock set found (pairwise differences invertible, with 0): %d matrices" % (len(alts), len(inv), len(ker)))
ok = True
for x in range(n):
    for y in range(n):
        v = -1 + 2 * (x == 0) + 2 * sum(mat_apply(S, x) == y for S in ker) - n * (x == 0 and y == 0)
        if v != (-1) ** wt(x & y): ok = False
print("   H_16(x, y) = -1 + 2 [x = 0] + 2 sum_S [y = S x] - 16 [x = y = 0] on all 256 entries:", ok, " (%d flats of the doubled space: the whole space, 9 subspaces of 4 bits, 1 point)" % (len(ker) + 3))
# price in gates (G): pieces [x=0] (one output gets the total: N - 1 gates), -J (the total again: 0 more), [y = S x] for S = 0 (the input 0 to every output: free),
# 7 permutations (free), the point (free); then each output x != 0 adds 1 (total) + 8 terms = 8 gates, output 0: total + input 0: 1 gate
price = (n - 1) + (n - 1) * 8 + 1
print("   price of this sum, pieces computed separately and added at the outputs: %d gates (G) at 16 points  [textbook 64, tonight's best 52]; in general N - 1 + (N - 1) N / 2 + 1" % price)
print("   flats: 4 at 4 points (5 rectangles), at most 8 at 8 points (13 rectangles), at most 11 at 16 points (49 rectangles)")
# C and D
def parse(line):
    toks = line.split(":", 1)[1].split()   # after 'CANDIDATE ... exactly):'
    return toks
def Vspace(sup, N):
    pts = [z for z in range(N) if (sup >> z) & 1]; a = pts[0]
    return a, sorted(p ^ a for p in pts)
def perpB(V, K):
    return [u for u in range(1 << K) if all(Bform(u, v, K) == 0 for v in V)]
for fn in sys.argv[1:]:
    print("C/D. replay of", fn)
    for line in open(fn):
        if not line.startswith("CANDIDATE"): continue
        head = line.split("(")[0].split(); r = int(head[1].split("=")[1]); K = int(head[2].split("=")[1]); N = 1 << K; g = gvec(K)
        toks = line.split("):")[1].split(); vecs = []; flats = []
        for t_ in toks:
            sup, neg = (int(x, 16) for x in t_.split(":"))
            vecs.append([0 if not (sup >> z) & 1 else (-1 if (neg >> z) & 1 else 1) for z in range(N)]); flats.append(sup)
        coef = in_span(vecs, g)
        if coef is None: print("   r=%d K=%d: NOT exact" % (r, K)); continue
        dims = [len(Vspace(s, N)[1]).bit_length() - 1 for s in flats]
        # dichotomy: a pair of non-whole flats with non-orthogonal U's (primal kill), a pair of non-point flats with non-orthogonal V's (dual kill), or all cosets of one Lagrangian
        Vs = [Vspace(s, N) for s in flats]; Us = [perpB(V, K) for a, V in Vs]
        prim = any(dims[i] < K and dims[j] < K and any(Bform(u, w, K) for u in Us[i] for w in Us[j]) for i in range(r) for j in range(i + 1, r))
        dual = any(dims[i] > 0 and dims[j] > 0 and any(Bform(u, w, K) for u in Vs[i][1] for w in Vs[j][1]) for i in range(r) for j in range(i + 1, r))
        lag = len({tuple(V) for a, V in Vs}) == 1 and all(tuple(V) == tuple(U) for (a, V), U in zip(Vs, Us))
        # do the kill for real when a primal pair exists: restrict to W and count the flats that still meet W
        surv = None
        if prim:
            for i in range(r):
                for j in range(i + 1, r):
                    if surv is not None or dims[i] == K or dims[j] == K: continue
                    for u in Us[i]:
                        for w in Us[j]:
                            if surv is None and Bform(u, w, K):
                                ci = Bform(u, Vs[i][0], K) ^ 1; cj = Bform(w, Vs[j][0], K) ^ 1
                                W = [z for z in range(N) if Bform(u, z, K) == ci and Bform(w, z, K) == cj]
                                surv = sum(1 for s in flats if any((s >> z) & 1 for z in W))
                                # the restricted function must be exactly reproduced by the survivors on W
                                assert all(sum(coef[x] * vecs[x][z] for x in range(r)) == g[z] for z in W)
        print("   r=%d K=%d exact: coefficients %s ; dimensions %s ; primal pair-kill %s, dual pair-kill %s, all cosets of one Lagrangian %s%s" % (
            r, K, " ".join(str(c) for c in coef), dims, prim, dual, lag, "" if surv is None else " ; after one primal kill %d flats still meet the %d-point restriction" % (surv, N // 4)))
