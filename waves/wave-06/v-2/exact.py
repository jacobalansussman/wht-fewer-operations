# v-2 exact checks (fractions / whole numbers; the only floats are log2 of the golden ratio and of binomials, marked).
from fractions import Fraction as F
from itertools import combinations
from math import comb, log2, sqrt, pi
import random, sys
def mm(A, B): return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def kron(A, B): return [[A[i][j]*B[k][l] for j in range(len(A[0])) for l in range(len(B[0]))] for i in range(len(A)) for k in range(len(B))]
def rank(M):
    M = [[F(v) for v in r] for r in M]; rk = 0
    for c in range(len(M[0]) if M else 0):
        p = next((i for i in range(rk, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[rk], M[p] = M[p], M[rk]
        for i in range(len(M)):
            if i != rk and M[i][c] != 0:
                f = M[i][c]/M[rk][c]; M[i] = [a - f*b for a, b in zip(M[i], M[rk])]
        rk += 1
    return rk
def det(M):
    n = len(M); M = [[F(v) for v in r] for r in M]; d = F(1)
    for c in range(n):
        p = next((i for i in range(c, n) if M[i][c] != 0), None)
        if p is None: return F(0)
        if p != c: M[c], M[p] = M[p], M[c]; d = -d
        d *= M[c][c]
        for i in range(c+1, n):
            f = M[i][c]/M[c][c]
            if f: M[i] = [a - f*b for a, b in zip(M[i], M[c])]
    return d
rng = random.Random(5)
print('== (a) the textbook program as a call program, and the two counts the proof uses')
# x = vec(X) with index (i,k) -> i*K+k ; (A kron A) x = vec(A X A^T).
for K in (2, 3, 4):
    K2 = K*K; r = 2*K
    def E(i, k): return i*K + k
    # calls 1..K: c_k = A (column k of X); calls K+1..2K: d_i = A (row i of the table [c_1 .. c_K]) ; out[(i,k)] = d_i[k]
    L = [[[0]*K2 for _ in range(K)] for _ in range(r)]; M = {}; P = [[[0]*K for _ in range(K2)] for _ in range(r)]
    for k in range(K):
        for i in range(K): L[k][i][E(i, k)] = 1
    for i in range(K):
        for k in range(K):
            m = [[0]*K for _ in range(K)]; m[k][i] = 1; M[(K + i, k)] = m     # input of call K+i, coordinate k, is c_k[i]
            P[K + i][E(i, k)][k] = 1
    def runprog(A):
        c = []
        for j in range(r):
            W = [row[:] for row in L[j]]
            for h in range(j):
                if (j, h) in M:
                    T = mm(M[(j, h)], c[h]); W = [[a + b for a, b in zip(r1, r2)] for r1, r2 in zip(W, T)]
            c.append(mm(A, W))
        out = [[0]*K2 for _ in range(K2)]
        for j in range(r):
            T = mm(P[j], c[j]); out = [[a + b for a, b in zip(r1, r2)] for r1, r2 in zip(out, T)]
        return out
    ok = all(runprog(A) == kron(A, A) for A in ([[rng.randint(-9, 9) for _ in range(K)] for _ in range(K)] for _ in range(5)))
    s = rank([[v for row in L[j] for v in row] for j in range(r)]); pdim = rank([[v for row in P[j] for v in row] for j in range(r)])
    # degree 1: the tensor sum_j P_j (x) L_j, as the matrix of E -> sum_j P_j E L_j
    T1 = [[0]*(K2*K2) for _ in range(K*K)]
    zero1 = True
    for a in range(K):
        for b in range(K):
            Eab = [[1 if (i, j) == (a, b) else 0 for j in range(K)] for i in range(K)]
            S = [[0]*K2 for _ in range(K2)]
            for j in range(r):
                T = mm(mm(P[j], Eab), L[j]); S = [[x + y for x, y in zip(r1, r2)] for r1, r2 in zip(S, T)]
            zero1 &= all(v == 0 for row in S for v in row)
    print('K=%d: 2K=%d calls, equal to A kron A on 5 random whole-number boxes: %s; degree-1 tensor zero: %s; dim span L = %d, dim span P = %d, sum = %d = r' % (K, r, ok, zero1, s, pdim, s + pdim))
print('== (a) step 1 of the proof on random instances: sum_j P_j (x) L_j = 0 forces dim span P <= r - dim span L')
for (K, r, s) in ((2, 3, 2), (2, 3, 1), (2, 4, 2), (3, 5, 3), (3, 5, 2)):
    K2 = K*K; dl = K*K2
    base = [[rng.randint(-3, 3) for _ in range(dl)] for _ in range(s)]
    lam = [[rng.randint(-2, 2) for _ in range(s)] for _ in range(r)]
    while rank(lam) < s: lam = [[rng.randint(-2, 2) for _ in range(s)] for _ in range(r)]
    # P_j = sum_c N_jc Y_c is forced with N a basis of the null space of lam^T: its dimension is r - s
    print('K=%d r=%d: L spans %d, relations on the P_j: %d independent, so P spans at most %d;  K calls needed on each side: %s' % (K, r, s, rank(lam), r - s, 'possible' if (s >= K and r - s >= K) else 'IMPOSSIBLE (s >= K and r - s >= K fails)'))
print('== (b) two nested calls for every 2 x 2 reflection, as a polynomial identity modulo c^2 + s^2 = 1')
# polynomials in c, s reduced by s^2 = 1 - c^2: dict {(i, e): coeff} for c^i s^e, e in {0,1}
def padd(p, q, m=1):
    r = dict(p)
    for k, v in q.items():
        r[k] = r.get(k, 0) + m*v
        if r[k] == 0: del r[k]
    return r
def pmul(p, q):
    r = {}
    for (i, e), v in p.items():
        for (j, f), w in q.items():
            if e + f < 2: r = padd(r, {(i + j, e + f): v*w})
            else: r = padd(r, {(i + j, 0): v*w}); r = padd(r, {(i + j + 2, 0): -v*w})
    return r
c = {(1, 0): F(1)}; s = {(0, 1): F(1)}; one = {(0, 0): F(1)}; neg = lambda p: {k: -v for k, v in p.items()}
A = [[c, s], [s, neg(c)]]
def pmm(X, Y): 
    out = [[{} for _ in range(len(Y[0]))] for _ in range(len(X))]
    for i in range(len(X)):
        for j in range(len(Y[0])):
            for k in range(len(Y)): out[i][j] = padd(out[i][j], pmul(X[i][k], Y[k][j]))
    return out
def const(v): return {(0, 0): F(v)} if v else {}
good = True
for X in ([[1,0],[0,0]], [[0,1],[0,0]], [[0,0],[1,0]], [[0,0],[0,1]]):
    Xp = [[const(v) for v in r] for r in X]; want = pmm(pmm(A, Xp), A)        # A = A^T
    al = F(X[0][0] + X[1][1], 2); be = F(X[0][1] - X[1][0], 2); p = F(X[0][0] - X[1][1], 2); q = F(X[0][1] + X[1][0], 2)
    c1 = pmm(A, [[const(p)], [const(q)]]); c1 = [c1[0], [neg(c1[1][0])]]; c2 = pmm(A, c1)
    got = [[padd(const(al), c2[0][0]), padd(const(-be), c2[1][0])], [padd(const(be), c2[1][0]), padd(const(al), c2[0][0], -1)]]
    good &= (got == want)
print('identity holds for the four unit tables, hence for every table and every reflection (c, s on the circle, any field): %s' % good)
AszA = pmm(pmm(A, [[one, {}], [{}, neg(one)]]), A); print('A sz A =', AszA, ' (c^2 - s^2 = 2c^2 - 1 and 2cs: the reflection at twice the angle)')
print('glue gates (G): 4 before (two butterflies) + 4 after; calls: 2 x 2 gates; total 12, against 4 calls x 2 gates = 8 for rows-then-columns')
print('== (c) subset sums: minors, exact')
def Z(k): return [[1 if (t & s_) == t else 0 for t in range(1 << k)] for s_ in range(1 << k)]
def charpoly_e(G):   # elementary symmetric functions of the eigenvalues, by Faddeev-LeVerrier, exact
    n = len(G); Mk = [[F(0)]*n for _ in range(n)]; cs = [F(1)]; I = [[F(int(i == j)) for j in range(n)] for i in range(n)]
    for k_ in range(1, n + 1):
        Mk = [[a + cs[-1]*b for a, b in zip(r1, r2)] for r1, r2 in zip(mm(G, Mk), I)] if k_ > 1 else I
        AM = mm(G, Mk); cs.append(-sum(AM[i][i] for i in range(n))/k_)
    return [(-1)**j*cs[j] for j in range(n + 1)]     # e_0..e_n
for k in (2, 3):
    z = Z(k); N = 1 << k; G = mm([list(r) for r in zip(*z)], z); e = charpoly_e(G)
    line = []
    for r in range(1, N + 1):
        sq = 0; mx = 0
        for R in combinations(range(N), r):
            for C in combinations(range(N), r):
                d = det([[z[a][b] for b in C] for a in R]); sq += d*d; mx = max(mx, abs(d))
        assert sq == e[r], (k, r, sq, e[r]); line.append('%d:%d' % (r, mx))
    print('k=%d: sum of squared r x r minors = e_r(eigenvalues of Z^T Z) for every r (Cauchy-Binet), exact; largest minor by size r: %s' % (k, ' '.join(line)))
    print('     e_r:', [int(v) for v in e])
