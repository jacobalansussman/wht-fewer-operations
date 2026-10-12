# k-note: three small exact checks of objects quoted in WAVE3-NOTE.md. Exact fractions only.
from fractions import Fraction as F
from itertools import product, combinations
import random

def kron(A, B):
    return [[a*b for a in ra for b in rb] for ra in A for rb in B]
def mul(A, B):
    n, m, p = len(A), len(B), len(B[0])
    return [[sum(A[i][k]*B[k][j] for k in range(m)) for j in range(p)] for i in range(n)]
def power(K, k):
    M = [[F(1)]]
    for _ in range(k): M = kron(M, K)
    return M

# 1. g-1's 19-gate circuit for the 8-point transform, count (G), copied from the task text.
def c19(x):
    g1 = x[0]+x[7]; g2 = x[1]+x[6]; g3 = x[2]-x[5]; g4 = x[3]-x[4]
    g5 = g1-g2; g6 = g3+g4; g7 = g5-g6
    g8 = g7-2*x[7]; g9 = g7-2*x[5]; g10 = g8+2*x[6]; g11 = g9-2*x[4]
    y = [None]*8
    y[7] = g10+2*g4; y[1] = g10+2*g3; y[6] = g11+2*g2; y[0] = -g11+2*g1
    y[2] = g8+2*x[1]; y[3] = g9+2*x[3]; y[4] = y[2]+2*g6; y[5] = -y[3]+2*g5
    return y
H2 = [[F(1), F(1)], [F(1), F(-1)]]
H8 = power(H2, 3)
cols = [c19([F(1) if i == j else F(0) for i in range(8)]) for j in range(8)]
M = [[cols[j][i] for j in range(8)] for i in range(8)]
rows = {tuple(r) for r in H8}
ok_rows = all(tuple(r) in rows for r in M) and len({tuple(r) for r in M}) == 8
print("1. 19-gate circuit: gates counted = 19; outputs are the 8 rows of H_8 with factor 1 (in some order):", ok_rows)
print("   in the natural order:", M == H8)

# 2. g-4's word: Z = D(1,3/5) H D(1,-1/2) H D(1,1/3) H D(1,5/4), k = 1..6
def diag(a, b, k):
    d = power([[F(a), F(0)], [F(0), F(b)]], k)
    return d
Z2 = [[F(1), F(0)], [F(1), F(1)]]
for k in range(1, 7):
    Hk = power(H2, k)
    W = diag(1, F(3, 5), k)
    for d in (F(-1, 2), F(1, 3), F(5, 4)):
        W = mul(mul(W, Hk), diag(1, d, k))
    print("2. subset sums = three transforms and four diagonals, k =", k, ":", W == power(Z2, k))

# 3. brick identity for random kernels (g-3 symmetric; k-cross non-symmetric form): k (x) k - det*(scaled swap) has rank one
def rank(A):
    A = [r[:] for r in A]; r = 0
    for c in range(len(A[0])):
        p = next((i for i in range(r, len(A)) if A[i][c] != 0), None)
        if p is None: continue
        A[r], A[p] = A[p], A[r]
        for i in range(len(A)):
            if i != r and A[i][c] != 0:
                f = A[i][c]/A[r][c]
                A[i] = [x - f*y for x, y in zip(A[i], A[r])]
        r += 1
    return r
random.seed(39)
ok_sym = True; ok_gen = True
P = [[F(0)]*4 for _ in range(4)]
P[1][1] = P[2][2] = F(1); P[0][3] = P[3][0] = F(-1)
for _ in range(200):
    a, b, c, d = [F(random.choice([n for n in range(-9, 10) if n != 0])) for _ in range(4)]
    # symmetric kernel [[a,b],[b,d]]: k (x) k = v v^T + det*P', v = (a,b,b,d)   (g-3's statement)
    Ks = [[a, b], [b, d]]; dets = a*d - b*b
    v = [a, b, b, d]
    ok_sym &= (kron(Ks, Ks) == [[v[i]*v[j] + dets*P[i][j] for j in range(4)] for i in range(4)])
    # any kernel [[a,b],[c,d]] with no zero entry: K = diag(1, c/a) [[1,1],[1,tau]] diag(a, b), tau = ad/(bc);
    # then K (x) K minus (tau - 1) * (row scalings) P' (column scalings) must have rank one   (k-cross's statement)
    K = [[a, b], [c, d]]; tau = a*d/(b*c)
    r = [F(1), c/a]; col = [a, b]
    R = [r[i1]*r[i2] for i1 in range(2) for i2 in range(2)]
    C = [col[j1]*col[j2] for j1 in range(2) for j2 in range(2)]
    KK = kron(K, K)
    rest = [[KK[i][j] - (tau - 1)*R[i]*P[i][j]*C[j] for j in range(4)] for i in range(4)]
    ok_gen &= (rank(rest) == 1)
print("3a. brick identity, 200 random symmetric kernels, exact form k(x)k = v v^T + det*P':", ok_sym)
print("3b. 200 random kernels with four non-zero entries: k(x)k minus a relabelling-with-scalings has rank one:", ok_gen)

# 4. the mirror's 16 points: even sign vectors of length 6 up to sign; one common angle, cosine 1/3; differences are two-term vectors
pts = []
for s in product([1, -1], repeat=6):
    if s[0] == 1 and sum(1 for t in s if t == -1) % 2 == 0: pts.append(s)
ips = {abs(sum(p*q for p, q in zip(a, b))) for a, b in combinations(pts, 2)}
roots = set()
for a, b in combinations(pts, 2):
    for sg in (1, -1):
        w = tuple(p + sg*q for p, q in zip(a, b))
        if sum(1 for t in w if t != 0) == 2:
            w = tuple(t//2 for t in w)
            if next(t for t in w if t != 0) < 0: w = tuple(-t for t in w)
            roots.add(w)
print("4. mirror points at 16:", len(pts), "points; |inner products| =", ips, "of 6 (cosine 1/3); pairs =", len(list(combinations(pts, 2))), "; two-term vectors on lines through pairs:", len(roots))
