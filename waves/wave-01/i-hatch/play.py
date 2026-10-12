# i-hatch play: small exact checks (Fractions), one float exploration (part D, marked).
import sys, math, random
from fractions import Fraction as F
from itertools import product
from math import comb

def kron(A, B):
    return [[a * b for a in ra for b in rb] for ra in A for rb in B]
def mul(A, B):
    Bt = list(zip(*B))
    return [[sum(x * y for x, y in zip(r, c)) for c in Bt] for r in A]
def tr(A): return [list(r) for r in zip(*A)]
def power(M, k):
    R = [[F(1)]]
    for _ in range(k): R = kron(R, M)
    return R
def diag(v): return [[v[i] if i == j else F(0) for j in range(len(v))] for i in range(len(v))]
def rank(A):
    A = [r[:] for r in A]; rk = 0; n = len(A); m = len(A[0])
    for c in range(m):
        p = next((i for i in range(rk, n) if A[i][c] != 0), None)
        if p is None: continue
        A[rk], A[p] = A[p], A[rk]
        for i in range(rk + 1, n):
            if A[i][c] != 0:
                f = A[i][c] / A[rk][c]
                A[i] = [a - f * b for a, b in zip(A[i], A[rk])]
        rk += 1
    return rk
H2 = [[F(1), F(1)], [F(1), F(-1)]]
Z2 = [[F(1), F(0)], [F(1), F(1)]]
pc = lambda x: bin(x).count("1")

print("== A. all the volume in one diagonal: H = Z D Z^T ; H Z^T = Z^T (complement) 2^|S| ==")
for k in range(1, 7):
    n = 1 << k
    H, Z = power(H2, k), power(Z2, k)
    D = diag([F((-2) ** pc(t)) for t in range(n)])
    ok1 = mul(mul(Z, D), tr(Z)) == H
    Zt = tr(Z)
    M = [[F(0)] * n for _ in range(n)]
    for s in range(n): M[(n - 1) ^ s][s] = F(2 ** pc(s))      # column s -> 2^|s| * column (complement of s)
    ok2 = mul(H, Zt) == mul(Zt, M)
    print("k=%d  H==Z D Z^T: %s   H Z^T == Z^T * monomial: %s   det(D)=2^%d (= n^(n/2): %s)" % (
        k, ok1, ok2, sum(pc(t) for t in range(n)), sum(pc(t) for t in range(n)) == k * n // 2))
# zeta from three transforms and four diagonals (2x2, hence every k by tensoring)
a, b, c, e = diag([F(1, 4), F(1, 5)]), diag([F(3, 2), F(-1, 2)]), diag([F(2), F(1)]), diag([F(1), F(5, 3)])
print("Z2 == d1 H d2 H d3 H d4 :", mul(mul(mul(mul(mul(mul(a, H2), b), H2), c), H2), e) == Z2)
print("volume left in Z after the diagonal is removed (log2 of the product of its singular values above 1), per entry:")
phi = (1 + 5 ** 0.5) / 2
for k in (4, 16, 64, 256, 1024, 4096):
    per = float(F(sum(comb(k, j) * (k - 2 * j) for j in range(0, (k + 1) // 2)), 2 ** k)) * math.log2(phi)
    print("  k=%5d   Z: %.4f bits/entry = %.4f*sqrt(k)     H: %.1f bits/entry (k/2)" % (k, per, per / k ** 0.5, k / 2))

print("== B. H_4 = rank one + monomial (7 gates); how far can 'monomial + low rank' go ==")
H4 = power(H2, 2)
u = [1, 1, 1, -1]; v = [1, 1, 1, -1]
S = [[H4[i][j] - u[i] * v[j] for j in range(4)] for i in range(4)]
print("H4 - u v^T =", [[int(x) for x in r] for r in S], " non-zeros per row:", [sum(1 for x in r if x) for r in S])
def h4(x):                       # 3 gates for s, then one gate per output
    s = x[0] + x[1] + x[2] - x[3]
    return [s + 2 * x[3], s - 2 * x[1], s - 2 * x[2], -s + 2 * x[0]]
print("7-gate program equals H4 on the unit vectors:", all(h4([F(int(i == j)) for i in range(4)]) == [H4[r][j] for r in range(4)] for j in range(4)))
# rank(Q_N - M) for monomial M: trace bound says >= (N - sqrt N)/2
P4 = [[S[i][j] / 2 for j in range(4)] for i in range(4)]          # the monomial part of Q4 = H4/2
for j in (1, 2, 3):
    N = 4 ** j
    Q = [[x / 2 ** j for x in r] for r in power(H2, 2 * j)]
    M = power(P4, j) if j > 1 else P4
    if j > 1:
        M = [[F(1)]]
        for _ in range(j): M = kron(M, P4)
    R = [[Q[a_][b_] - M[a_][b_] for b_ in range(N)] for a_ in range(N)]
    print("  N=%3d  rank(H/sqrt(N) - tensor monomial) = %d   trace bound (N - sqrt N)/2 = %d   rank(H/sqrt(N) - I) = %d" % (
        N, rank(R), (N - 2 ** j) // 2, rank([[Q[a_][b_] - (a_ == b_) for b_ in range(N)] for a_ in range(N)])))

print("== C. Schur-Weyl: the transform is nearly free in the basis that splits by total spin ==")
print("   blocks of size d=k-2j+1 with multiplicity C(k,j)-C(k,j-1); dense cost sum(mult*d^2)/n, and the share where H is a scalar")
for k in (4, 16, 64, 256, 1024):
    tot = 0; scal = 0; dd = 0
    for j in range(0, k // 2 + 1):
        mlt = comb(k, j) - (comb(k, j - 1) if j else 0); d = k - 2 * j + 1
        tot += mlt * d * d; dd += mlt * d
        if d == 1: scal = mlt
    assert dd == 2 ** k
    print("  k=%5d  dense block cost per entry = %.3f = %.3f*sqrt(k)   (textbook: %d)   scalar share = %.2e" % (
        k, float(F(tot, 2 ** k)), float(F(tot, 2 ** k)) / k ** 0.5, k, float(F(scal, 2 ** k))))
# two bits: symmetric and antisymmetric parts
HH = power(H2, 2)
sym = [[1, 0, 0, 0], [0, 1, 1, 0], [0, 0, 0, 1]]; anti = [0, 1, -1, 0]
img = [[sum(HH[r][c] * w[c] for c in range(4)) for r in range(4)] for w in sym + [anti]]
print("  H(x)H on e00, e01+e10, e11, e01-e10 :", [[int(x) for x in r] for r in img], " (last one = -2 * itself: a scaling)")

print("== D. [float exploration] Ailon-style quasi-entropy: how many bits can ONE gate move when coefficients are large ==")
def qent(M, Mi):
    n = len(M); t = 0.0
    for i in range(n):
        for j in range(n):
            p = M[i][j] * Mi[j][i]
            if abs(p) > 1e-300: t -= p * math.log2(abs(p))
    return t
def run(n, gates):
    M = [[float(i == j) for j in range(n)] for i in range(n)]; Mi = [r[:] for r in M]
    for (i, j, c) in gates:
        M[i] = [x + c * y for x, y in zip(M[i], M[j])]          # row i += c row j
        for r in range(n): Mi[r][j] -= c * Mi[r][i]             # inverse: col j -= c col i
    return M, Mi
random.seed(7)
target = {2: 2.0, 3: 3 * math.log2(3), 4: 8.0}
for n in (2, 3, 4):
    pairs = [(i, j) for i in range(n) for j in range(n) if i != j]
    for g in (2, 3, 4, 6, 8):
        for big in (1.0, 8.0, 64.0):
            best = (-1e9, None)
            for _ in range(6000):
                gs = [(*random.choice(pairs), random.choice([-1, 1]) * big ** random.uniform(-1, 1)) for _ in range(g)]
                M, Mi = run(n, gs); q = qent(M, Mi)
                if q > best[0]: best = (q, gs)
            print("  wires=%d gates=%d coefficients up to %4.0f : best quasi-entropy %8.2f bits = %6.2f per gate   (orthogonal-gate rule: at most 2 per gate; H_%d itself: %.2f)" % (
                n, g, big, best[0], best[0] / g, n, target[n]))
