# words.py: (c) exact 2x2 identities linking K = [[1,1],[1,2]], the transform H, subset sums Z.  Numbers a + b*sqrt(d), exact.
from fractions import Fraction as F
class Q:
    d = 2
    def __init__(s, a, b=0): s.a, s.b = F(a), F(b)
    def __add__(s, o): o = o if isinstance(o, Q) else Q(o); return Q(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __sub__(s, o): o = o if isinstance(o, Q) else Q(o); return Q(s.a - o.a, s.b - o.b)
    def __mul__(s, o): o = o if isinstance(o, Q) else Q(o); return Q(s.a*o.a + Q.d*s.b*o.b, s.a*o.b + s.b*o.a)
    __rmul__ = __mul__
    def inv(s): n = s.a*s.a - Q.d*s.b*s.b; return Q(s.a/n, -s.b/n)
    def __eq__(s, o): o = o if isinstance(o, Q) else Q(o); return s.a == o.a and s.b == o.b
    def __repr__(s): return "%s%+s*sqrt(%d)" % (s.a, s.b, Q.d) if s.b else str(s.a)
def mm(A, B): return [[sum((A[i][k]*B[k][j] for k in range(2)), Q(0)) for j in range(2)] for i in range(2)]
def dg(x, y): return [[x, Q(0)], [Q(0), y]]
def M(rows): return [[x if isinstance(x, Q) else Q(x) for x in r] for r in rows]
H = M([[1,1],[1,-1]]); K = M([[1,1],[1,2]]); Z = M([[1,0],[1,1]]); ZT = M([[1,1],[0,1]])
print("K = Z Z^T:", mm(Z, ZT) == K, "   H = Z diag(1,-2) Z^T:", mm(mm(Z, dg(Q(1), Q(-2))), ZT) == H)
L = M([[1,0],[3,-2]]); print("H = L K with L = [[1,0],[3,-2]] (triangular):", mm(L, K) == H)
Li = M([[1,0],[F(3,2),F(-1,2)]]); print("K = L^-1 H with L^-1 = [[1,0],[3/2,-1/2]]:", mm(Li, H) == K)
# two calls of the transform give K over Q(sqrt 2):  K = D1 H diag(a,b) H D1,  D1 = diag(1, sqrt2), a+b = 1, a-b = 1/sqrt2
Q.d = 2; s = Q(0, 1); a = (Q(1) + s.inv()) * Q(F(1,2)); b = (Q(1) - s.inv()) * Q(F(1,2)); D1 = dg(Q(1), s)
print("over Q(sqrt2): K = D1 H diag(a,b) H D1, D1 = diag(1,sqrt2), a =", a, " b =", b, ":", mm(mm(mm(mm(D1, H), dg(a, b)), H), D1) == K)
# two calls of K give H over Q(sqrt 17):  K diag(a,1) K = [[a+1, a+2],[a+2, a+4]];  need (a+1)(a+4) = -(a+2)^2 -> 2a^2 + 9a + 8 = 0
Q.d = 17; a = (Q(-9) + Q(0, 1)) * Q(F(1,4)); print("2a^2+9a+8 =", 2*a*a + 9*a + 8)
Mid = mm(mm(K, dg(a, Q(1))), K)   # [[p,q],[q,r]] with p r = -q^2 ; H = diag(1,x) Mid diag(1,x)/p with x = p/q
p, q, r = Mid[0][0], Mid[0][1], Mid[1][1]; x = p * q.inv(); D = dg(Q(1), x); S = mm(mm(D, Mid), D)
print("over Q(sqrt17): diag(1,x) K diag(a,1) K diag(1,x) = p * H:", S == [[p*h for h in row] for row in H], "  a =", a, " x =", x, " p =", p)
# quasi-probabilities p_ij = M_ij (M^-1)_ji  (rows sum to 1); their 'entropy' -sum p log2|p| is additive under Kronecker products
from math import log2
def qp(Mx):
    (a_, b_), (c_, d_) = Mx; det = a_*d_ - b_*c_; return [[a_*d_/det, -b_*c_/det], [-b_*c_/det, a_*d_/det]]
for nm, Mx in [("H", [[1,1],[1,-1]]), ("K", [[1,1],[1,2]]), ("Z", [[1,0],[1,1]]), ("[[2,1],[1,1]]", [[2,1],[1,1]]), ("[[1,2],[3,4]]", [[1,2],[3,4]]), ("[[1,1],[1,3]]", [[1,1],[1,3]])]:
    P = qp([[F(x) for x in r] for r in Mx]); ent = -sum(float(x)*log2(abs(x)) for r in P for x in r if x != 0)
    print("kernel %-14s quasi-probabilities %s  entropy per kernel %.4f (per row %.4f)  sum|p| per row %s" % (nm, [[str(x) for x in r] for r in P], ent, ent/2, abs(P[0][0]) + abs(P[0][1])))
