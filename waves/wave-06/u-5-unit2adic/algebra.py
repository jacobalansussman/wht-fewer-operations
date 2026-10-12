# u-5: exact check (Gaussian rationals as pairs of fractions) of the algebra used in u-5.md, at h = 3 (8 addresses), port p = 111.
#   D_z = (1+i)/2 + (1-i)/2 * shift_z            (the engine's move along z, h-7 section 1)
# (a) D_z D_z = shift_z, so D_z^-1 = D_z shift_z (a move followed by a free relabelling);
# (b) supports: F_perp (product of D over a basis of p-perp) has rows of 2^(h-1) non-zeros, F_perp D_p^-1 has rows of 2^h;
# (c) the invocation as the certificate states it (x at label <p>, y at label 0  ->  x at the full label, y at label p-perp holding y + x)
#     is, on the ARRAYS: both arrays moved along p-perp only, and the shear  Y += D_p^-1 X;
# (d) three shears make the exchange: (X, Y) -> (-D Y, D^-1 X): both contents moved along p, no move along p made;
# (f) 2-adic depth adds under nesting: (2A + U) (x) (2a + u) is U (x) u modulo 2 and the wanted A (x) a enters only at the digit 4.
from fractions import Fraction as Fr
import random
class G:
    __slots__ = ("a", "b")
    def __init__(s, a=0, b=0): s.a = Fr(a); s.b = Fr(b)
    def __add__(s, o): return G(s.a + o.a, s.b + o.b)
    def __sub__(s, o): return G(s.a - o.a, s.b - o.b)
    def __neg__(s): return G(-s.a, -s.b)
    def __mul__(s, o): return G(s.a * o.a - s.b * o.b, s.a * o.b + s.b * o.a)
    def __eq__(s, o): return s.a == o.a and s.b == o.b
    def __repr__(s): return "(%s%+si)" % (s.a, s.b)
N = 8; ca, cb = G(Fr(1, 2), Fr(1, 2)), G(Fr(1, 2), Fr(-1, 2))
def mat(f): return [[f(y, x) for x in range(N)] for y in range(N)]
def mul(A, B): return [[sum((A[i][k] * B[k][j] for k in range(N)), G()) for j in range(N)] for i in range(N)]
def add(A, B, s=1): return [[A[i][j] + (B[i][j] if s == 1 else -B[i][j]) for j in range(N)] for i in range(N)]
I = mat(lambda y, x: G(int(x == y)))
def Sh(z): return mat(lambda y, x: G(int(x == y ^ z)))
def D(z): return mat(lambda y, x: (ca if x == y else G()) + (cb if x == y ^ z else G()))
def Dinv(z): return mat(lambda y, x: (cb if x == y else G()) + (ca if x == y ^ z else G()))
p = 0b111
print("(a) D_z D_z = shift_z for every z:", all(mul(D(z), D(z)) == Sh(z) for z in range(1, N)), "; D_z^-1 = D_z shift_z:", all(mul(D(z), Dinv(z)) == I and Dinv(z) == mul(D(z), Sh(z)) for z in range(1, N)))
F = mul(D(1), mul(D(2), D(4)))
Fperp = mul(D(0b011), D(0b110))                     # a basis of p-perp = the even-weight words
FpD = mul(Fperp, D(p))
nz = lambda A: sorted({sum(1 for t in r if not t == G()) for r in A})
mod2 = lambda A: sorted({t.a * t.a + t.b * t.b for r in A for t in r if not t == G()})
print("(b) non-zeros per row: F_perp %s (squared modulus %s); F_perp D_p^-1, what the y-array receives from the x-array, %s (squared modulus %s); the product of all three D %s"
      % (nz(Fperp), mod2(Fperp), nz(mul(Fperp, Dinv(p))), mod2(mul(Fperp, Dinv(p))), nz(F)))
print("    note: in this toy the frames are plain products of D, so D_1 D_2 D_4 and F_perp D_p are different operators; the engine makes")
print("    one operator per subspace with free address maps and phases (h-7 section 1). Statement (e) of an earlier draft (every D_z")
print("    diagonal at the full frame) was FALSE in this toy and is withdrawn: F commutes with D_z, so F D_z F^-1 = D_z.")
random.seed(5)
X = [G(random.randint(-9, 9)) for _ in range(N)]; Y = [G(random.randint(-9, 9)) for _ in range(N)]
ap = lambda A, v: [sum((A[i][k] * v[k] for k in range(N)), G()) for i in range(N)]
xi = ap(Dinv(p), X)                                  # the content the certificate calls x: X = frame_<p>(xi)
X1 = ap(FpD, xi); Y1 = ap(Fperp, [a + b for a, b in zip(Y, xi)])
print("(c) x-array after the invocation = F_perp(X raw):", X1 == ap(Fperp, X), "; y-array = F_perp(Y) + F_perp D_p^-1 X = F_perp(Y) + F_perp D_p (shift_p X):",
      Y1 == [a + b for a, b in zip(ap(Fperp, Y), ap(FpD, ap(Sh(p), X)))])
Dp, Di = D(p), Dinv(p)
Ya = [a + b for a, b in zip(Y, ap(Di, X))]          # Y += D^-1 X
Xb = [a - b for a, b in zip(X, ap(Dp, Ya))]         # X -= D Y
Yc = [a + b for a, b in zip(Ya, ap(Di, Xb))]        # Y += D^-1 X
print("(d) three shears: X ends as -D Y:", Xb == [-t for t in ap(Dp, Y)], "; Y ends as D^-1 X = D (shift X):", Yc == ap(Di, X) == ap(Dp, ap(Sh(p), X)))
A, U, a, u = 5, 3, 7, 9
w = (2 * A + U) * (2 * a + u)
print("(f) (2A+U)(2a+u) - U u = %d = 2 (A u + U a) + 4 A a: the wanted product A a carries the factor 4" % (w - U * u), (w - U * u) == 2 * (A * u + U * a) + 4 * A * a)
