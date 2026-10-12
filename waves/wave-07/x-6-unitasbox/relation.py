#!/usr/bin/env python3
"""relation.py [x-6-unitasbox, 2026-10-11]  Exact (Gaussian rationals as pairs of fractions).  What relation between moves
does the published unit use?  Toy: h = 4, 16 addresses.
  move along z:  D_z = (1+i)/2 + (1-i)/2 * shift_z     (u-5 / h-7)      D_z^-1 = (1-i)/2 + (1+i)/2 * shift_z
  an ORTHONORMAL basis of the addresses: h words of odd weight, any two with an even number of common ones.
(1) the transform F = D_e1 D_e2 D_e3 D_e4 equals the product of moves along EVERY orthonormal basis
    (D_b if the weight of b is 1 modulo 4, D_b^-1 if it is 3 modulo 4);
(2) a general kernel a + b*shift does not have this property: the coordinate product for (a,b) against the product along the
    weight-3 basis for (b,a), (b,-a), ... ;
(3) the batch relation: sources X_t with different ports p_t; each makes the h-1 moves of an orthonormal basis of p_t-perp
    (moves it owes anyway); ONE inverse transform of the sum gives sum_t c_t D_(p_t)^(-+1) X_t: v different moves for h;
(4) the three-shear exchange as a call program: 3 calls, the sealed-box count for the same job is 2."""
from fractions import Fraction as Fr
import itertools, random
class G:
    __slots__ = ("a", "b")
    def __init__(s, a=0, b=0): s.a = Fr(a); s.b = Fr(b)
    def __add__(s, o): return G(s.a + o.a, s.b + o.b)
    def __sub__(s, o): return G(s.a - o.a, s.b - o.b)
    def __neg__(s): return G(-s.a, -s.b)
    def __mul__(s, o): return G(s.a * o.a - s.b * o.b, s.a * o.b + s.b * o.a)
    def __eq__(s, o): return s.a == o.a and s.b == o.b
    def __bool__(s): return bool(s.a) or bool(s.b)
    def __repr__(s): return "(%s + %s i)" % (s.a, s.b)
h = 4; N = 1 << h; Z = G()
ca, cb = G(Fr(1, 2), Fr(1, 2)), G(Fr(1, 2), Fr(-1, 2))
# everything here is a convolution operator: store it as its coefficient vector on the shifts (the group algebra); product = convolution
def conv(A, B):
    C = [G() for _ in range(N)]
    for i in range(N):
        if A[i]:
            for j in range(N):
                if B[j]: C[i ^ j] = C[i ^ j] + A[i] * B[j]
    return C
def ker(a, b, z):
    K = [G() for _ in range(N)]; K[0] = a; K[z] = b; return K
D = lambda z: ker(ca, cb, z); Di = lambda z: ker(cb, ca, z)
one = ker(G(1), G(), 1); one[1] = G()
def prod(L):
    P = list(one)
    for K in L: P = conv(P, K)
    return P
wt = lambda x: bin(x).count("1"); dot = lambda x, y: wt(x & y) & 1
F = prod([D(1 << j) for j in range(h)])
print("(0) coefficient of F on the shift by u is ((1+i)/2)^h (-i)^weight(u):", all(F[u] == prod([ker(ca, G(), 1)] * h)[0] * [G(1), G(0, -1), G(-1), G(0, 1)][wt(u) % 4] for u in range(N)))
odd = [z for z in range(1, N) if wt(z) & 1]
bases = [b for b in itertools.combinations(odd, h) if all(dot(x, y) == 0 for x, y in itertools.combinations(b, 2))]
mv = lambda z: D(z) if wt(z) % 4 == 1 else Di(z)
okb = [prod([mv(z) for z in b]) == F for b in bases]
print("(1) orthonormal bases of the %d-bit addresses: %d (coordinate basis included); product of their moves equals F for %d of them" % (h, len(bases), sum(okb)))
print("    the bases:", [tuple(format(z, "04b") for z in b) for b in bases])
allb = [b for b in itertools.combinations(range(1, N), h) if len({x for r in range(h + 1) for s in itertools.combinations(b, r) for x in [__import__('functools').reduce(lambda p, q: p ^ q, s, 0)]}) == N]
def anyprod(b):
    for signs in itertools.product((0, 1), repeat=h):
        if prod([(D(z) if s else Di(z)) for z, s in zip(b, signs)]) == F: return True
    return False
good = [b for b in allb if anyprod(b)]
print("    all %d bases of the addresses, each move taken forwards or backwards: the product equals F for %d of them; all of those orthonormal: %s"
      % (len(allb), len(good), all(b in bases for b in good)))
# (2) a general kernel
w3 = [z for z in odd if wt(z) == 3]
for (a, b) in ((G(1), G(2)), (G(1), G(1, 1)), (G(1), G(0, -1))):
    P0 = prod([ker(a, b, 1 << j) for j in range(h)])
    hit = [(s1, s2) for s1 in (G(1), G(-1), G(0, 1), G(0, -1)) for s2 in (G(1), G(-1), G(0, 1), G(0, -1)) if prod([ker(s1 * b, s2 * a, z) for z in w3]) == P0]
    print("(2) kernel a + b*shift with (a, b) = (%s, %s): coordinate product = product along the weight-3 basis with kernel (unit*b, unit*a) for %d of 16 choices of units" % (a, b, len(hit)))
# (3) the batch relation
random.seed(7)
def perp_basis(p):
    c = [z for z in odd if dot(z, p) == 0]
    for b in itertools.combinations(c, h - 1):
        if all(dot(x, y) == 0 for x, y in itertools.combinations(b, 2)): return b
ok3 = True; rows = []
X = {p: [G(random.randint(-9, 9), random.randint(-9, 9)) for _ in range(N)] for p in odd}   # an array = a function on the addresses = an element of the same algebra
co = {p: G(random.randint(1, 5)) for p in odd}
Finv = prod([Di(1 << j) for j in range(h)])
assert conv(F, Finv) == one
T = [G() for _ in range(N)]; want = [G() for _ in range(N)]
for p in odd:
    b = perp_basis(p); Gp = prod([mv(z) for z in b])
    ok3 &= conv(mv(p), Gp) == F
    Yp = conv(Gp, X[p])                       # the source array after the h-1 moves it owes anyway
    T = [t + co[p] * y for t, y in zip(T, Yp)]
    inv_port = Di(p) if wt(p) % 4 == 1 else D(p)
    want = [w + co[p] * y for w, y in zip(want, conv(inv_port, X[p]))]
    rows.append((format(p, "04b"), tuple(format(z, "04b") for z in b)))
print("(3) ports = the %d odd words; for each an orthonormal basis of p-perp exists and F = (move along p) x (moves along that basis): %s" % (len(odd), ok3))
print("    F^-1 (sum_t c_t G_t X_t) = sum_t c_t (inverse move along p_t) X_t :", conv(Finv, T) == want, "   [%d different port moves delivered by %d moves on one array]" % (len(odd), h))
print("    ports and bases:", rows)
# (4) three shears as calls
p = 0b0111; Dp, Dq = D(p), Di(p)
Xa = X[1]; Ya = X[2]
c1 = conv(Dq, Xa); Y1 = [y + t for y, t in zip(Ya, c1)]
c2 = conv(Dp, Y1); X2 = [x - t for x, t in zip(Xa, c2)]
c3 = conv(Dq, X2); Y3 = [y + t for y, t in zip(Y1, c3)]
print("(4) three shears = 3 calls (D^-1, D, D^-1): X ends as -D Y: %s, Y ends as D^-1 X: %s ; the same job with sealed boxes: 2 calls (D on Y, D^-1 on X)"
      % (X2 == [-t for t in conv(Dp, Ya)], Y3 == conv(Dq, Xa)))
sh = ker(G(), G(1), p)
print("    D^-1 = D x shift_p (a free relabelling): %s ; D^2 = shift_p: %s" % (Dq == conv(Dp, sh), conv(Dp, Dp) == sh))
