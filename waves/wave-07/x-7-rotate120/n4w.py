# x-7-rotate120 / n4.py : every pair of mirrors of the 4-point rotation R = D H / 2, over GF(p), priced with d-0-zeta/mincirc.
# usage: n4.py p [maxm]
# Definitions: H = 4-point transform with the two bits exchanged in the output address, D = diag((-1)^(x1 x2)), R = D H / 2.
# A "mirror" here is S with S^2 = 1 and S R S = R^-1.  The pair is (S, S R); the third mirror is S R^2.
# Count (G): cost(S) = least number of gates a*u+b*v that produce every row of S up to scale (mincirc, exhaustive over GF(p)).
import sys, itertools, subprocess, os, collections
p = int(sys.argv[1]); maxm = int(sys.argv[2]) if len(sys.argv) > 2 else 6
HERE = os.path.dirname(os.path.abspath(__file__))
MC = os.path.join(HERE, '..', 'd-0-zeta', 'mincirc')
N = 4
def pop(v): return bin(v).count('1')
def Q(x): return (x & 1) * ((x >> 1) & 1)
def sw(x): return ((x & 1) << 1) | ((x >> 1) & 1)
H = [[(-1) ** pop(x & sw(y)) for y in range(N)] for x in range(N)]
D = [(-1) ** Q(x) for x in range(N)]
inv2 = pow(2, p - 2, p)
def mul(A, B): return [[sum(A[i][t] * B[t][j] for t in range(N)) % p for j in range(N)] for i in range(N)]
I4 = [[int(i == j) for j in range(N)] for i in range(N)]
R = [[D[x] * H[x][y] * inv2 % p for y in range(N)] for x in range(N)]
R2 = mul(R, R); R3 = mul(R2, R)
assert R3 == I4, 'R^3 != 1'
Rinv = R2
# linear space L = {X : X R = R^-1 X}
rows = []
for i in range(N):
    for j in range(N):
        # (X R)[i][j] - (Rinv X)[i][j] = sum_t X[i][t] R[t][j] - sum_t Rinv[i][t] X[t][j]
        r = [0] * 16
        for t in range(N):
            r[i * 4 + t] = (r[i * 4 + t] + R[t][j]) % p
            r[t * 4 + j] = (r[t * 4 + j] - Rinv[i][t]) % p
        rows.append(r)
def nullspace(M, n):
    M = [r[:] for r in M]; piv = []; rr = 0
    for c in range(n):
        s = next((i for i in range(rr, len(M)) if M[i][c] % p), None)
        if s is None: continue
        M[rr], M[s] = M[s], M[rr]
        iv = pow(M[rr][c], p - 2, p); M[rr] = [x * iv % p for x in M[rr]]
        for i in range(len(M)):
            if i != rr and M[i][c]:
                f = M[i][c]; M[i] = [(a - f * b) % p for a, b in zip(M[i], M[rr])]
        piv.append(c); rr += 1
    free = [c for c in range(n) if c not in piv]
    basis = []
    for f in free:
        v = [0] * n; v[f] = 1
        for i, c in enumerate(piv): v[c] = (-M[i][f]) % p
        basis.append(v)
    return basis
B = nullspace(rows, 16)
print('p=%d: dimension of {X : X R = R^-1 X} = %d (expected 6 = 2^2 + 2*1^2)' % (p, len(B)))
# split: X = D (g0 + g1), g0 living on the fixed space of R, g1 on the rest; the two conditions decouple.
inv3 = pow(3, p - 2, p)
P0 = [[(I4[i][j] + R[i][j] + R2[i][j]) * inv3 % p for j in range(N)] for i in range(N)]
P1 = [[(I4[i][j] - P0[i][j]) % p for j in range(N)] for i in range(N)]
Dfull = [[(D[i] % p) if i == j else 0 for j in range(N)] for i in range(N)]
def comb(co, Bs):
    v = [sum(c * b[i] for c, b in zip(co, Bs)) % p for i in range(16)]
    return [v[0:4], v[4:8], v[8:12], v[12:16]]
def add(A, B_): return [[(A[i][j] + B_[i][j]) % p for j in range(N)] for i in range(N)]
part0 = []; part1 = []
for co in itertools.product(range(p), repeat=len(B)):
    pass_ = None
    break
# bases of the two parts of L: X P1 = 0 = P1 X (part 0), X P0 = 0 = P0 X (part 1)
def sub_basis(Pkill):
    out = []
    # X = sum c_i B_i ; require X Pkill = 0 and Pkill X = 0 : linear in c
    eqs = []
    mats = [comb([int(i == j) for j in range(len(B))], B) for i in range(len(B))]
    prods = [(mul(M, Pkill), mul(Pkill, M)) for M in mats]
    for a in range(N):
        for b in range(N):
            eqs.append([prods[i][0][a][b] for i in range(len(B))])
            eqs.append([prods[i][1][a][b] for i in range(len(B))])
    ns = nullspace(eqs, len(B))
    return [comb(c, B) for c in ns]
A0 = sub_basis(P1); A1 = sub_basis(P0)
print('part on the fixed space: dimension %d ; part on the rest: dimension %d' % (len(A0), len(A1)))
def lin(co, Ms):
    return [[sum(c * M[i][j] for c, M in zip(co, Ms)) % p for j in range(N)] for i in range(N)]
X0s = [X for X in (lin(co, A0) for co in itertools.product(range(p), repeat=len(A0))) if mul(X, X) == P0]
X1s = [X for X in (lin(co, A1) for co in itertools.product(range(p), repeat=len(A1))) if mul(X, X) == P1]
print('involutions on the fixed space: %d ; on the rest: %d' % (len(X0s), len(X1s)))
mirrors = [add(a, b) for a in X0s for b in X1s]
for X in mirrors[:50]: assert mul(X, X) == I4 and mul(X, R) == mul(Rinv, X)
print('mirrors (S^2 = 1, S R S = R^-1) over GF(%d): %d' % (p, len(mirrors)))

# x-7 / n4w.py : no pricing; row weights only.  For every mirror S: the product law and the non-zero counts.
import collections
def rw(X): return [sum(1 for x in r if x) for r in X]
def cw(X): return [sum(1 for r in X if r[j]) for j in range(N)]
def nnz(X): return sum(rw(X))
viol = 0; prod = collections.Counter(); best = None; shapes = collections.Counter()
for S in mirrors:
    S2 = mul(S, R)
    # law: every row x of S has at least N / (largest row weight of S R) non-zeros  [from R = S * (S R), R has no zero]
    if min(rw(S)) * max(rw(S2)) < N: viol += 1
    a, b = nnz(S), nnz(S2)
    prod[(a, b)] += 1
    shapes[(tuple(sorted(rw(S))), tuple(sorted(rw(S2))))] += 1
print('p=%d mirrors %d ; violations of (least row weight of S) x (largest row weight of S R) >= N : %d' % (p, len(mirrors), viol))
print('least nnz(S) * nnz(S R): %d (N^3 = 64) ; least nnz(S) + nnz(S R): %d (trivial pair 4 + 16 = 20)' % (min(a * b for a, b in prod), min(a + b for a, b in prod)))
print('pairs with product <= 100:', sorted((k, v) for k, v in prod.items() if k[0] * k[1] <= 100))
print('pairs in which both mirrors have every row of weight <= 2:', sum(v for (ra, rb), v in shapes.items() if max(ra) <= 2 and max(rb) <= 2))
print('pairs in which both mirrors have every row of weight <= 3:', sum(v for (ra, rb), v in shapes.items() if max(ra) <= 3 and max(rb) <= 3))
print('row-weight shapes of (S, S R) with the smallest total, top 8:')
for (ra, rb), v in sorted(shapes.items(), key=lambda kv: sum(kv[0][0]) + sum(kv[0][1]))[:8]: print('  ', ra, rb, v)
