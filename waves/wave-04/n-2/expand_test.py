#!/usr/bin/env python3
"""expand_test.py   (n-2; exact rationals)
1. The expansion behind both lemmas, as a pure matrix identity, on random words WITH mixing and scratch arrays:
      live( g_0 D_1 g_1 ... D_k g_k ) = live( g_0 ... g_k ) - 2 U_A (1 + 2 C_A)^(-1) W_A^T ,   D_i = 1 - 2 E_(l_i) for i in A.
2. A real unit with mixing (direction e_j on all W arrays, a random mixing of the arrays after each direction, the inverse
   at the end): the unit condition U_A N_A W_A^T = q(I) for every form, then the two lemmas' rank statements on it.
3. Sylvester: U N W^T = 0, N invertible  =>  rank U + rank W <= size of N  (random instances built to be extremal).
"""
import random, itertools
from fractions import Fraction as Fr
random.seed(20261011)
def mm(A, B): return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def ident(n): return [[Fr(int(i == j)) for j in range(n)] for i in range(n)]
def rnd(n, lo=-3, hi=3):
    while True:
        A = [[Fr(random.randint(lo, hi)) for _ in range(n)] for _ in range(n)]
        if rank(A) == n: return A
def rank(A):
    A = [r[:] for r in A]; r = 0
    for c in range(len(A[0]) if A else 0):
        p = next((i for i in range(r, len(A)) if A[i][c] != 0), None)
        if p is None: continue
        A[r], A[p] = A[p], A[r]
        for i in range(len(A)):
            if i != r and A[i][c] != 0:
                f = A[i][c] / A[r][c]; A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        r += 1
    return r
def inv(A):
    n = len(A); B = [A[i][:] + ident(n)[i] for i in range(n)]
    for c in range(n):
        p = next(i for i in range(c, n) if B[i][c] != 0); B[c], B[p] = B[p], B[c]
        d = B[c][c]; B[c] = [x / d for x in B[c]]
        for i in range(n):
            if i != c and B[i][c] != 0:
                f = B[i][c]; B[i] = [a - f * b for a, b in zip(B[i], B[c])]
    return [r[n:] for r in B]
def word_data(g, l, W):
    """g = [g_0..g_k], l = [l_1..l_k] (0-based arrays).  Returns u_i, w_i (lists of W numbers), c_ij."""
    k = len(l); n = len(g[0])
    pre = [g[0]]                                   # pre[i] = g_0 ... g_i
    for i in range(1, k + 1): pre.append(mm(pre[-1], g[i]))
    suf = [None] * (k + 1); suf[k] = g[k]          # suf[i] = g_i ... g_k
    for i in range(k - 1, -1, -1): suf[i] = mm(g[i], suf[i + 1])
    u = [[pre[i][r][l[i]] for r in range(W)] for i in range(k)]            # column l_i of g_0..g_(i-1) (move i+1 in 1-based)
    w = [[suf[i + 1][l[i]][c] for c in range(W)] for i in range(k)]         # row l_i of g_i..g_k
    c = [[Fr(0)] * k for _ in range(k)]
    for i in range(k):
        P = ident(n)
        for j in range(i + 1, k):
            P = mm(P, g[j]); c[i][j] = P[l[i]][l[j]]                         # entry (l_i, l_j) of g_i..g_(j-1)
    return u, w, c
def live_direct(g, l, A, W):
    n = len(g[0]); P = g[0]
    for i in range(len(l)):
        if i in A:
            D = ident(n); D[l[i]][l[i]] = Fr(-1); P = mm(P, D)
        P = mm(P, g[i + 1])
    return [r[:W] for r in P[:W]]
def formula(u, w, c, A, W, liveG):
    A = sorted(A)
    if not A: return liveG, None
    s = len(A)
    N = inv([[Fr(int(a == b)) + 2 * c[A[a]][A[b]] for b in range(s)] for a in range(s)])
    U = [[u[i][r] for i in A] for r in range(W)]                 # W x s
    Wt = [[w[i][r] for r in range(W)] for i in A]                # s x W
    X = mm(mm(U, N), Wt)
    return [[liveG[r][cc] - 2 * X[r][cc] for cc in range(W)] for r in range(W)], X
# ---- 1. the identity on arbitrary words
bad = 0; tot = 0
for trial in range(60):
    W = random.randint(1, 3); s = random.randint(0, 3); n = W + s; k = random.randint(1, 7)
    g = [rnd(n) for _ in range(k + 1)]; l = [random.randrange(n) for _ in range(k)]
    u, w, c = word_data(g, l, W); liveG = live_direct(g, l, set(), W)
    for A in itertools.chain.from_iterable(itertools.combinations(range(k), r) for r in range(k + 1)):
        tot += 1
        if formula(u, w, c, set(A), W, liveG)[0] != live_direct(g, l, set(A), W): bad += 1
print("1. expansion identity on random words with mixing and scratch: %d selections tested, %d failures" % (tot, bad))
# ---- 2. a real unit with mixing; scratch arrays ride along (they get every direction too, so they cost moves; still a unit)
def unit_test(m, W, s):
    n = W + s; dirs = list(range(m))                                  # the coordinate frame
    g = [rnd(n)]; l = []
    prod = g[0]
    for d in dirs:
        for a in range(n):
            l.append(a)
            if a < n - 1: g.append(ident(n))
        mix = rnd(n) if d < m - 1 else inv(prod)
        g.append(mix); prod = mm(prod, mix)
    k = len(l); lab = [d for d in dirs for a in range(n)]             # move -> direction index
    u, w, c = word_data(g, l, W); liveG = live_direct(g, l, set(), W)
    assert liveG == ident(W)
    ok = True; tight = []; zero_ok = True; nzero = 0
    for bits in range(1, 1 << m):                                      # q restricted to the frame: values q(e_d); q(I) = parity
        A = {i for i in range(k) if bits >> lab[i] & 1}; qI = bin(bits).count("1") & 1
        _, X = formula(u, w, c, A, W, liveG)
        ok &= X == [[Fr(qI * int(r == cc)) for cc in range(W)] for r in range(W)]
        As = sorted(A)
        if qI and len(A) == W: tight.append(As)
        if not qI:
            nzero += 1
            rU = rank([[u[i][r] for i in As] for r in range(W)]); rW = rank([[w[i][r] for r in range(W)] for i in As])
            zero_ok &= rU + rW <= len(As)
    tri = True
    for As in tight:
        for a in As:
            for b in As:
                d = sum(x * y for x, y in zip(w[a], u[b]))
                if a == b: tri &= d == 1
                elif a > b: tri &= d == 0
    print("2. unit with random mixing, m=%d, W=%d live + %d scratch arrays, %d moves: unit condition for all selections %s; "
          "tight selections %d, triangular table on them %s; forms with q(I)=0: %d, rank U + rank W <= |A0| in all: %s"
          % (m, W, s, k, ok, len(tight), tri, nzero, zero_ok))
unit_test(3, 2, 0); unit_test(3, 2, 1); unit_test(4, 3, 0); unit_test(5, 4, 0); unit_test(5, 2, 2)
# ---- 3. the converse construction of h-2 section 1: any (u, w, c) is realised with one scratch array per move
badc = 0
for trial in range(20):
    W = random.randint(1, 3); k = random.randint(1, 5); n = W + k
    u = [[Fr(random.randint(-2, 2)) for _ in range(W)] for _ in range(k)]
    w = [[Fr(random.randint(-2, 2)) for _ in range(W)] for _ in range(k)]
    c = [[Fr(random.randint(-2, 2)) if j > i else Fr(0) for j in range(k)] for i in range(k)]
    # word of reflections R_i = 1 - 2 a_i b_i^T with a_i = (u_i ; e_i), b_i = (w_i ; b'_i), selected or not
    def refl(i):
        a = u[i] + [Fr(int(j == i)) for j in range(k)]
        bp = [Fr(0)] * k; bp[i] = 1 - sum(x * y for x, y in zip(w[i], u[i]))
        for j in range(i + 1, k): bp[j] = c[i][j] - sum(x * y for x, y in zip(w[i], u[j]))
        b = w[i] + bp
        return [[Fr(int(r == cc)) - 2 * a[r] * b[cc] for cc in range(n)] for r in range(n)]
    for A in itertools.chain.from_iterable(itertools.combinations(range(k), r) for r in range(k + 1)):
        P = ident(n)
        for i in A: P = mm(P, refl(i))
        live = [r[:W] for r in P[:W]]
        want, _ = formula(u, w, c, set(A), W, ident(W))
        if live != want: badc += 1
print("3. h-2's converse (any u, w, c realised by reflections with one scratch array per move): failures", badc)
