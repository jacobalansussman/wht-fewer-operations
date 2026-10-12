#!/usr/bin/env python3
"""play.py (g-5-k3): exact checks of the identities used in g-5.md.  Integers / Fractions / Gaussian integers (pairs)."""
from fractions import Fraction as F
import itertools
def mm(A, B): return [[sum(a * b for a, b in zip(r, c)) for c in zip(*B)] for r in A]
def kron(A, B): return [[a * b for a in ra for b in rb] for ra in A for rb in B]
def T(A): return [list(r) for r in zip(*A)]
K3 = [[1, 1, 1], [2, 0, -2], [1, -1, 1]]
I3 = [[int(i == j) for j in range(3)] for i in range(3)]
H2 = [[1, 1], [1, -1]]; H4 = kron(H2, H2)
print('1. K3^2 = 4 I:', mm(K3, K3) == [[4 * x for x in r] for r in I3])
u = [-1, 2, 1]; v = [1, -1, -1]
print('2. K3 = 2 I + u v^T with u = (-1,2,1), v = (1,-1,-1):', K3 == [[2 * I3[i][j] + u[i] * v[j] for j in range(3)] for i in range(3)],
      '; v K3 = -2 v:', mm([v], K3) == [[-2 * x for x in v]], '; (1,1,-1) K3 = 2 (1,1,-1):', mm([[1, 1, -1]], K3) == [[2, 2, -2]])
# 3. H4 = 2 SWAP + rank one
SW = [[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]
R = [[H4[i][j] - 2 * SW[i][j] for j in range(4)] for i in range(4)]
a = [-1, 1, 1, 1]; b = [1, -1, -1, -1]
print('3. H4 - 2 SWAP = (-1,1,1,1)^T (1,-1,-1,-1), rank one:', R == [[a[i] * b[j] for j in range(4)] for i in range(4)])
# 4. pair coordinates: (x00, x01+x10, x11, x01-x10).  B maps raw -> pair coordinates.
B = [[1, 0, 0, 0], [0, 1, 1, 0], [0, 0, 0, 1], [0, 1, -1, 0]]
Binv = [[F(1), 0, 0, 0], [0, F(1, 2), 0, F(1, 2)], [0, F(1, 2), 0, F(-1, 2)], [0, 0, F(1), 0]]
print('   B Binv = I:', mm(B, Binv) == [[F(int(i == j)) for j in range(4)] for i in range(4)])
M = mm(mm(B, H4), Binv)
print('4. H4 in pair coordinates = K3 (+) (-2):', M == [[1, 1, 1, 0], [2, 0, -2, 0], [1, -1, 1, 0], [0, 0, 0, -2]])
# 5. the 7-gate brick is K3's reflection form with the two pair butterflies absorbed
print('5. brick helper u = x00 - x01 - x10 - x11 in pair coordinates is v = (1,-1,-1) on (a, b, c) and 0 on the antisymmetric line:',
      mm([[1, -1, -1, -1]], Binv) == [[1, -1, -1, 0]])
# 6. the 4-point Fourier transform (group Z4) in the coordinates (f0, f1+f3, f2, f1-f3): Gaussian integers as (re, im)
def cmul(x, y): return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0])
def cadd(x, y): return (x[0] + y[0], x[1] + y[1])
w = [(1, 0), (0, 1), (-1, 0), (0, -1)]
F4 = [[w[(j * k) % 4] for k in range(4)] for j in range(4)]
Bz = [[1, 0, 0, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 1, 0, -1]]        # f -> (f0, f1+f3, f2, f1-f3)
Bzinv = [[F(1), 0, 0, 0], [0, F(1, 2), 0, F(1, 2)], [0, 0, F(1), 0], [0, F(1, 2), 0, F(-1, 2)]]
def cmm(A, Bm):
    out = []
    for r in A:
        row = []
        for c in zip(*Bm):
            s = (F(0), F(0))
            for x, y in zip(r, c): s = cadd(s, cmul(x, y))
            row.append(s)
        out.append(row)
    return out
c = lambda M_: [[(F(x), F(0)) if not isinstance(x, tuple) else (F(x[0]), F(x[1])) for x in r] for r in M_]
Mz = cmm(cmm(c(Bz), c(F4)), c(Bzinv))
target = [[(1, 0), (1, 0), (1, 0), (0, 0)], [(2, 0), (0, 0), (-2, 0), (0, 0)], [(1, 0), (-1, 0), (1, 0), (0, 0)], [(0, 0), (0, 0), (0, 0), (0, 2)]]
print('6. Fourier transform of Z4 in (f0, f1+f3, f2, f1-f3) -> same coordinates:', [[(int(x[0]), int(x[1])) for x in r] for r in Mz])
print('   = K3 (+) (a multiple of i) on the odd line:', all((Mz[i][j][0], Mz[i][j][1]) == (K3[i][j], 0) for i in range(3) for j in range(3))
      and all(Mz[i][3] == (0, 0) and Mz[3][i] == (0, 0) for i in range(3)), '; odd-line scalar =', (int(Mz[3][3][0]), int(Mz[3][3][1])))
# 7. K3 transposed = cosine transform (type I) on 3 points = Fourier transform of Z4 on even functions
print('7. K3^T =', T(K3), ' = [cos(pi j k / 2) with end weights 1,2,1]:',
      T(K3) == [[[1, 0, -1, 0][(j * k) % 4] * (2 if k == 1 else 1) for k in range(3)] for j in range(3)])
# 8. the plethysm at 9 points: antisymmetric square of K3 = -2 K3^T ; symmetric square S6 has trace/determinant data
K9 = kron(K3, K3); idx = lambda i, j: 3 * i + j
ap = [(0, 1), (0, 2), (1, 2)]
A3 = [[K9[idx(a_, b_)][idx(c_, d_)] - K9[idx(a_, b_)][idx(d_, c_)] for (c_, d_) in ap] for (a_, b_) in ap]
print('8. antisymmetric square of K3 (basis 01, 02, 12) =', A3, '= -2 K3^T:', A3 == [[-2 * x for x in r] for r in T(K3)])
# 9. gates per bit
print('9. gates per bit of determinant: butterfly 2/1; K3 row-scaled 4/2; 7-gate brick 7/4; K9 best 22/12 = %.3f; K27 best 98/54 = %.3f; K81 best 388/216 = %.3f' % (22 / 12, 98 / 54, 388 / 216))
# 10. the mask form: K3^(x r) = (rows transformed, masked) after (columns transformed, masked) on arrays supported on disjoint pairs
def had(vec):
    n = len(vec); out = list(vec); h = 1
    while h < n:
        for i in range(0, n, 2 * h):
            for j in range(i, i + h): out[j], out[j + h] = out[j] + out[j + h], out[j] - out[j + h]
        h *= 2
    return out
import random
random.seed(5)
for r in (1, 2, 3, 4):
    n = 1 << r
    # letters: 0 -> (w,m) = (0,0); 1 -> the symmetric coordinate b ... we use the half-way picture directly:
    # input f lives on (x mod m, m): store it as X[x][m] for x disjoint from m (x subset of complement of m).
    X = [[random.randint(-9, 9) if (x & m) == 0 else 0 for m in range(n)] for x in range(n)]
    # step 1: transform every column m along x (full transform of the zero-extended column), then mask to w & m == 0
    Y = [[0] * n for _ in range(n)]
    for m in range(n):
        col = had([X[x][m] for x in range(n)])
        for w_ in range(n): Y[w_][m] = col[w_] if (w_ & m) == 0 else 0
    Z = [[0] * n for _ in range(n)]
    for w_ in range(n):
        row = had(Y[w_])
        for v_ in range(n): Z[w_][v_] = row[v_] if (w_ & v_) == 0 else 0
    # compare with K3^(x r) on the 3^r numbers: letter at position i from (x_i, m_i): (0,0)->0 ['a'], (0,1)->1 ['b'], (1,0)->2 ['c']
    # per position K3 in this picture: a = X[0][0], c = X[1][0], b = X[0][1]; outputs F(w=0,v=0) = a+b+c, F(w=0,v=1) = a - b + c, F(w=1,v=0) = a - c
    Kc = [[1, 1, 1], [1, 0, -1], [1, -1, 1]]             # row-scaled K3 (the factor 2 of the middle row is a free scaling)
    Kr = [[1]]
    for _ in range(r): Kr = kron(Kr, Kc)
    def letter_in(x, m): return 0 if (x, m) == (0, 0) else (1 if (x, m) == (0, 1) else 2)
    def letter_out(w_, v_): return 0 if (w_, v_) == (0, 0) else (2 if (w_, v_) == (0, 1) else 1)
    pts = list(itertools.product(range(3), repeat=r)); vec = [0] * len(pts); res = {}
    def code(letters): 
        s = 0
        for l in letters: s = 3 * s + l
        return s
    for x in range(n):
        for m in range(n):
            if x & m: continue
            vec[code([letter_in(x >> i & 1, m >> i & 1) for i in range(r)])] = X[x][m]
    out = [sum(a_ * b_ for a_, b_ in zip(row, vec)) for row in Kr]; ok = True
    for w_ in range(n):
        for v_ in range(n):
            if w_ & v_: continue
            if out[code([letter_out(w_ >> i & 1, v_ >> i & 1) for i in range(r)])] != Z[w_][v_]: ok = False
    print('10. r=%d: (transform columns, keep disjoint pairs, transform rows, keep disjoint pairs) = row-scaled K3^(x%d) on %d numbers: %s' % (r, r, 3 ** r, ok))
