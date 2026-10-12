#!/usr/bin/env python3
"""circuit2.py [ad-6-twohelpers]  A linear circuit, count (G), for: given the 1 + k + k(k-1)/2 coefficients of a
polynomial q of degree <= 2 in k bits, output q(x) at all N = 2^k cube points.  Built from the selector-and-atoms
family; every gate is u + v or u - v.  Replayed exactly: on every unit input (a linear circuit that is right on a
basis is right) for k <= kexact, and on random whole numbers above.  The gate count does not depend on the values.

q(a, y) = A(y) + B_a(y without atom a):
  A(y)   = the part of q in y alone, plus, for y_p in the atom with index b, the coefficient sum_i b_i Q[a_i, p];
           A is again a polynomial of degree <= 2 in y, so it is evaluated by the same program on m = k - t bits.
  B_a    = c(a) + sum over atoms b != a, p in atom b, of (sum_i (a_i - b_i) Q[a_i, p]) y_p : an AFFINE function of
           the bits outside atom a, evaluated on that smaller cube by halving (helper + helper).
  output = A + B_a : one gate per cube point.
"""
import sys, random
from itertools import combinations
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from verify import best_t
G = 0
def add(u, v, s=1):
    global G
    if v is None: return u
    if u is None: return v if s == 1 else -v          # a scaling, free in count (G)
    G += 1; return u + s * v
def eval1(c, lin):
    n = len(lin)
    if n == 0: return {0: c}
    if n == 1:
        p, l = lin[0]; return {0: c, 1 << p: add(c, l)}
    h = n // 2; A = eval1(c, lin[:h]); B = eval1(None, lin[h:])
    return {ma | mb: add(wa, wb) for ma, wa in A.items() for mb, wb in B.items()}
def eval2(c, lin, quad, P):
    k = len(P)
    qq = lambda p, q: quad[(p, q)] if p < q else quad[(q, p)]
    if k <= 2:
        out = {}
        for sub in range(1 << k):
            S = [P[i] for i in range(k) if sub >> i & 1]; w = c
            for p in S: w = add(w, lin[p])
            for p, q in combinations(S, 2): w = add(w, qq(p, q))
            out[sum(1 << p for p in S)] = w
        return out
    t = best_t(k); g = 1 << t; A_ = P[:t]; Y = P[t:]
    atoms = [[] for _ in range(g)]
    for j, p in enumerate(Y): atoms[j % g].append(p)
    atom_of = {p: b for b in range(g) for p in atoms[b]}
    linA = {}
    for p in Y:
        b = atom_of[p]; w = lin[p]
        for i in range(t):
            if b >> i & 1: w = add(w, qq(A_[i], p))
        linA[p] = w
    Aval = eval2(c, linA, {(p, q): qq(p, q) for p, q in combinations(sorted(Y), 2)}, Y)
    out = {}
    for a in range(g):
        S = [A_[i] for i in range(t) if a >> i & 1]; ca = None
        for p in S: ca = add(ca, lin[p])
        for p, q in combinations(S, 2): ca = add(ca, qq(p, q))
        lin_a = []
        for p in Y:
            b = atom_of[p]
            if b == a: continue
            w = None
            for i in range(t):
                ai = a >> i & 1; bi = b >> i & 1
                if ai != bi: w = add(w, qq(A_[i], p), 1 if ai else -1)
            lin_a.append((p, w))
        Bval = eval1(ca, lin_a)
        amask = sum(1 << p for p in S); keep = sum(1 << p for p in Y if atom_of[p] != a)
        for ym, wA in Aval.items(): out[amask | ym] = add(wA, Bval[ym & keep])
    return out
def run(k, c, lin, quad):
    global G
    G = 0; out = eval2(c, lin, quad, list(range(k))); g = G
    N = 1 << k; assert len(out) == N
    for x in range(N):
        S = [i for i in range(k) if x >> i & 1]
        if out[x] != c + sum(lin[p] for p in S) + sum(quad[(p, q)] for p, q in combinations(S, 2)): return g, False
    return g, True
if __name__ == "__main__":
    kmax = int(sys.argv[1]); kexact = int(sys.argv[2]); rnd = random.Random(6)
    print("k, N, t at the top level, gates (G), gates/N, (gates - N)/N, replay")
    for k in range(3, kmax + 1):
        pairs = list(combinations(range(k), 2)); D = 1 + k + len(pairs); ok = True; how = "random whole numbers, 3 draws"
        if k <= kexact:
            how = "every unit input (%d), exact" % D
            for j in range(D):
                c = 1 if j == 0 else 0; lin = {p: 1 if j == 1 + p else 0 for p in range(k)}
                quad = {pq: 1 if j == 1 + k + i else 0 for i, pq in enumerate(pairs)}
                g, o = run(k, c, lin, quad); ok = ok and o
        for _ in range(3):
            c = rnd.randrange(-10**9, 10**9); lin = {p: rnd.randrange(-10**9, 10**9) for p in range(k)}
            quad = {pq: rnd.randrange(-10**9, 10**9) for pq in pairs}
            g, o = run(k, c, lin, quad); ok = ok and o
        N = 1 << k
        print("k=%2d N=%6d t=%d gates %7d = %.4f N   excess %.4f N   replay %s [%s]" % (k, N, best_t(k), g, g / N, (g - N) / N, "PASS" if ok else "FAIL", how))
