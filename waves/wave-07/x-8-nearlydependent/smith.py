# smith.py: exact checks for section 4 of x-8.md (whole numbers and fractions only).
#  1. H = Z D Z^T with Z = subset sums (determinant 1) and D = diagonal of (-2)^|S|  [g-4's identity]: so the invariant factors of H
#     (its Smith normal form) are 2^j with multiplicity C(k,j); H modulo 2 has rank 1, so the group Z^N / (rows of H) needs N-1 generators.
#  2. Rank distance to the nearest signed relabelling: with P4 the signed relabelling of the 4-point brick (H4 = v v^T - 2 P4),
#     rank( H_N * Mon^-1 - sqrt(N) * I ) = (N - sqrt N)/2 for Mon = (-P4)^(x k/2); the trace argument says no relabelling does better.
from fractions import Fraction as Fr
from math import comb
def kron(A, B): return [[x*y for x in ra for y in rb] for ra in A for rb in B]
def mul(A, B): return [[sum(a*b for a, b in zip(r, c)) for c in zip(*B)] for r in A]
def T(A): return [list(c) for c in zip(*A)]
def rank(M, p=None):
    A = [[(x % p if p else Fr(x)) for x in r] for r in M]; rk = 0; n = len(A); m = len(A[0])
    for c in range(m):
        pv = next((i for i in range(rk, n) if A[i][c] != 0), None)
        if pv is None: continue
        A[rk], A[pv] = A[pv], A[rk]
        iv = pow(A[rk][c], -1, p) if p else 1 / A[rk][c]
        A[rk] = [(x * iv) % p if p else x * iv for x in A[rk]]
        for i in range(n):
            if i != rk and A[i][c] != 0:
                f = A[i][c]; A[i] = [((x - f*y) % p if p else x - f*y) for x, y in zip(A[i], A[rk])]
        rk += 1
    return rk
H2 = [[1, 1], [1, -1]]; Z2 = [[1, 0], [1, 1]]; D2 = [[1, 0], [0, -2]]
H, Z, D = H2, Z2, D2
for k in range(1, 6):
    if k > 1: H, Z, D = kron(H, H2), kron(Z, Z2), kron(D, D2)
    N = 2**k; ok = mul(mul(Z, D), T(Z)) == H
    mult = {}
    for i in range(N): mult[abs(D[i][i])] = mult.get(abs(D[i][i]), 0) + 1
    print("N=%2d: H = Z D Z^T %s; |diagonal of D| multiplicities %s (binomials %s); rank of H modulo 2 = %d; sum of exponents = %d = (N/2) log2 N = %d"
          % (N, ok, sorted(mult.items()), [comb(k, j) for j in range(k+1)], rank(H, 2), sum(j*comb(k, j) for j in range(k+1)), N*k//2))
v = [1, 1, 1, -1]; P4 = [[0,0,0,-1],[0,1,0,0],[0,0,1,0],[-1,0,0,0]]; H4 = kron(H2, H2)
assert all(H4[i][j] == v[i]*v[j] - 2*P4[i][j] for i in range(4) for j in range(4)); print("brick: H4 = v v^T - 2 P4 exactly, v = (1,1,1,-1)")
Hn, Mon = H4, [[-x for x in r] for r in P4]; base = Mon
for k in (2, 4, 6):
    if k > 2: Hn, Mon = kron(Hn, H4), kron(Mon, base)
    N = 2**k; s = 2**(k//2); V = mul(Hn, T(Mon))  # Mon is a signed relabelling: its inverse is its transpose
    R = [[V[i][j] - s*int(i == j) for j in range(N)] for i in range(N)]
    print("N=%2d: rank(H Mon^-1 - sqrt(N) I) = %d ; (N - sqrt N)/2 = %d" % (N, rank(R), (N - s)//2))
