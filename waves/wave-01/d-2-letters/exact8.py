# d-2-letters: EXACT replay (Gaussian rationals: pairs of Fractions) of the non-commuting two-letter words.
# Claim A (8 points): H_8 = D0 * L1 * D1 * L2 * D2 with BOTH letters on the SAME tree (flag 2,6,1), middle diagonal not a scalar,
#   L1 = K (x) P+  +  C (x) P-,  L2 = K (x) P+  +  C' (x) P-,   D1 = A1 (x) Z,   K = 4-point letter, K[x][y] = (-i)^|x+y|.
#   A1 = any invertible diagonal (4 free numbers): C' = A1^-1, C = -i A1^-1.  The commuting class has no word on one flag at 8 points.
# Claim B (any size, here 16 and 32): for ANY matrix G of half size,
#   G (x) H_2 = (I (x) diag(1,-i)) * (2iG (x) P+ + I (x) P-) * (I (x) Z) * (2G (x) P+ + I (x) P-) * (I (x) diag(1/(1+i), 1/(1-i))).
#   So "two factors sharing their finest pairing" is the textbook recursion written serially: each factor carries one half-size call.
from fractions import Fraction as Fr
import random
class G:                                   # Gaussian rational
    __slots__ = ("a", "b")
    def __init__(s, a, b=0): s.a = Fr(a); s.b = Fr(b)
    def __add__(s, o): return G(s.a + o.a, s.b + o.b)
    def __sub__(s, o): return G(s.a - o.a, s.b - o.b)
    def __mul__(s, o): return G(s.a * o.a - s.b * o.b, s.a * o.b + s.b * o.a)
    def inv(s): n = s.a * s.a + s.b * s.b; return G(s.a / n, -s.b / n)
    def __eq__(s, o): return s.a == o.a and s.b == o.b
    def __repr__(s): return "%s%+si" % (s.a, s.b)
Z0, O, I_ = G(0), G(1), G(0, 1)
def mm(A, B): return [[sum((A[i][l] * B[l][j] for l in range(len(B))), Z0) for j in range(len(B[0]))] for i in range(len(A))]
def kron(A, B): return [[A[i][j] * B[p][q] for j in range(len(A[0])) for q in range(len(B[0]))] for i in range(len(A)) for p in range(len(B))]
def diag(v): return [[v[i] if i == j else Z0 for j in range(len(v))] for i in range(len(v))]
def eye(n): return diag([O] * n)
def add(A, B): return [[A[i][j] + B[i][j] for j in range(len(A))] for i in range(len(A))]
pc = lambda v: bin(v).count("1")
def had(k): return [[G(-1 if pc(x & y) & 1 else 1) for y in range(1 << k)] for x in range(1 << k)]
half = G(Fr(1, 2))
Pp = [[half, half], [half, half]]; Pm = [[half, Z0 - half], [Z0 - half, half]]; Zm = diag([O, G(-1)])
ipow = [O, I_, G(-1), G(0, -1)]
# --- the 4-point letter K and H_4 = D K D
K = [[ipow[(-pc(x ^ y)) % 4] for y in range(4)] for x in range(4)]
D4 = [ipow[pc(x) % 4] for x in range(4)]
assert mm(mm(diag(D4), K), diag(D4)) == had(2)
# K is diagonal in the many-scale basis of the tree {0,3} | {1,2}: check K h = c h for the four basis functions
for hvec, c in (([1, 1, 1, 1], G(0, -2)), ([1, -1, -1, 1], G(0, 2)), ([1, 0, 0, -1], G(2)), ([0, 1, -1, 0], G(2))):
    col = [[G(v)] for v in hvec]; assert mm(K, col) == [[c * G(v)] for v in hvec]
print("4 points: H_4 = D K D, K diagonal in the many-scale basis of the tree {0,3}|{1,2}, eigenvalues -2i, 2i, 2, 2   [exact]")
# --- Claim A
H8 = kron(had(2), had(1))                  # index = 2*x1 + x2 ; equals had(3) with bit 0 = x2
assert H8 == had(3)
for A1 in ([O, O, O, O], [G(1), G(2), G(3), G(5)], [G(1, 1), G(2, -3), G(Fr(1, 7)), G(0, 4)]):
    A1i = [a.inv() for a in A1]
    C = [G(0, -1) * a for a in A1i]; Cp = A1i
    L1 = add(kron(K, Pp), kron(diag(C), Pm)); L2 = add(kron(K, Pp), kron(diag(Cp), Pm))
    D1 = kron(diag(A1), Zm)
    d0 = [v for x1 in range(4) for v in (G(0, 2) * D4[x1], G(2) * D4[x1])]
    d2 = [v for y1 in range(4) for v in (D4[y1] * G(1, 1).inv(), D4[y1] * G(1, -1).inv())]
    W = mm(mm(mm(mm(diag(d0), L1), D1), L2), diag(d2))
    assert W == H8
    com = mm(L1, L2) == mm(L2, L1)
    print("8 points: H_8 = D0 L1 D1 L2 D2 exactly; same tree for both letters; middle diagonal =", [D1[z][z] for z in range(8)], "; L1 L2 = L2 L1:", com)
# each letter is diagonal in the many-scale basis of ONE tree on 8 points: top {x1 in {0,3}} | {x1 in {1,2}}, then x1, then x2
basis = []
for h4 in ([1, 1, 1, 1], [1, -1, -1, 1], [1, 0, 0, -1], [0, 1, -1, 0]): basis.append([v for a in h4 for v in (a, a)])
for x1 in range(4): basis.append([(1 if (z >> 1) == x1 else 0) * (1 if z % 2 == 0 else -1) for z in range(8)])
for L in (L1, L2):
    for hv in basis:
        col = [[G(v)] for v in hv]; out = mm(L, col); nz = next(i for i in range(8) if hv[i]); c = out[nz][0] * G(hv[nz]).inv()
        assert out == [[c * G(v)] for v in hv]
print("          both letters are diagonal in the many-scale basis of that one tree   [exact]")
# --- Claim B at 16 and 32 points, G = the half-size transform, and G = a random integer matrix
random.seed(4)
for k in (3, 4):
    n = 1 << k
    for name, Gm in (("the half-size transform", had(k)), ("a random integer matrix", [[G(random.randint(-9, 9)) for _ in range(n)] for _ in range(n)])):
        left = kron(eye(n), diag([O, G(0, -1)]))
        f1 = add(kron([[G(0, 2) * v for v in r] for r in Gm], Pp), kron(eye(n), Pm))
        f2 = add(kron([[G(2) * v for v in r] for r in Gm], Pp), kron(eye(n), Pm))
        right = kron(eye(n), diag([G(1, 1).inv(), G(1, -1).inv()]))
        W = mm(mm(mm(mm(left, f1), kron(eye(n), Zm)), f2), right)
        assert W == kron(Gm, had(1))
        print("%d points: G (x) H_2 = diag * (2iG (x) P+ + I (x) P-) * (I (x) Z) * (2G (x) P+ + I (x) P-) * diag, G = %s   [exact]" % (2 * n, name))
