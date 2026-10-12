#!/usr/bin/env python3
"""shears.py [ad-0-rateperblock]  EXACT (Gaussian rationals, Fractions).  Why the word pays back all but one skipped move per array.
The move along one direction in the engine's phased form (read: x-6 section 1): D = a + b*shift, a = (1+i)/2, b = (1-i)/2, D^2 = shift.
On f digit columns the move is the f-th tensor power.  A SHEAR: target += c * D^(+-1) source.  Free: sums of whole arrays with scalar coefficients.
Checks: (1) the three-shear exchange for f = 1, 2, 3;  (2) a TWO-shear exchange with a free pre-mix exists for one column (f = 1) and
its last free step is impossible for f >= 2;  (3) the eigenvalues of D: {1, i} for f = 1, all four fourth roots of 1 from f = 3 (-1 from f = 2);
(4) in the sector D = -1 every shear is a transvection, and -1 is not a product of n transvections (brute force over the field of 3 and of 5
elements for n = 2; the three-line proof for all n is in the report)."""
from fractions import Fraction as F
import itertools
class G:
    __slots__ = ("r", "i")
    def __init__(s, r=0, i=0): s.r, s.i = F(r), F(i)
    def __add__(s, o): return G(s.r + o.r, s.i + o.i)
    def __sub__(s, o): return G(s.r - o.r, s.i - o.i)
    def __neg__(s): return G(-s.r, -s.i)
    def __mul__(s, o): return G(s.r * o.r - s.i * o.i, s.r * o.i + s.i * o.r)
    def inv(s):
        n = s.r * s.r + s.i * s.i; return G(s.r / n, -s.i / n)
    def __eq__(s, o): return s.r == o.r and s.i == o.i
    def iszero(s): return s.r == 0 and s.i == 0
    def __repr__(s): return "(%s%+si)" % (s.r, s.i)
Z, ONE, I = G(0), G(1), G(0, 1)
def mm(A, B): return [[sum((A[i][k] * B[k][j] for k in range(len(B))), Z) for j in range(len(B[0]))] for i in range(len(A))]
def madd(A, B, c=ONE): return [[A[i][j] + c * B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
def eye(n): return [[ONE if i == j else Z for j in range(n)] for i in range(n)]
def kron(A, B): return [[A[i][j] * B[k][l] for j in range(len(A)) for l in range(len(B))] for i in range(len(A)) for k in range(len(B))]
def scal(A, c): return [[c * x for x in r] for r in A]
def eq(A, B): return all(A[i][j] == B[i][j] for i in range(len(A)) for j in range(len(A[0])))
def rank(rows):
    M = [list(r) for r in rows]; rk = 0
    for c in range(len(M[0])):
        p = next((r for r in range(rk, len(M)) if not M[r][c].iszero()), None)
        if p is None: continue
        M[rk], M[p] = M[p], M[rk]; iv = M[rk][c].inv()
        M[rk] = [x * iv for x in M[rk]]
        for r in range(len(M)):
            if r != rk and not M[r][c].iszero():
                t = M[r][c]; M[r] = [x - t * y for x, y in zip(M[r], M[rk])]
        rk += 1
    return rk
a, b = G(F(1, 2), F(1, 2)), G(F(1, 2), F(-1, 2))
D1 = [[a, b], [b, a]]; S1 = [[Z, ONE], [ONE, Z]]
for f in (1, 2, 3):
    D, S = D1, S1
    for _ in range(f - 1): D, S = kron(D, D1), kron(S, S1)
    N = len(D); E = eye(N)
    assert eq(mm(D, D), S) and eq(mm(S, S), E)
    Di = mm(D, S)                                   # D^-1 = D * shift
    assert eq(mm(D, Di), E)
    # (1) three shears: Y1 = Y + D^-1 X ; X2 = X - D Y1 ; Y3 = Y1 + D^-1 X2  on blocks [X-part, Y-part] as 2N x 2N matrices over (x, y)
    X = [E, [[Z] * N for _ in range(N)]]; Y = [[[Z] * N for _ in range(N)], E]      # each array = (coefficient matrix of x, of y)
    lin = lambda P, M: [mm(M, P[0]), mm(M, P[1])]
    add = lambda P, Q, c=ONE: [madd(P[0], Q[0], c), madd(P[1], Q[1], c)]
    Y1 = add(Y, lin(X, Di)); X2 = add(X, lin(Y1, D), -ONE); Y3 = add(Y1, lin(X2, Di))
    ok3 = eq(X2[0], scal(E, Z)) and eq(X2[1], scal(D, -ONE)) and eq(Y3[0], Di) and eq(Y3[1], scal(E, Z))
    # (2) two shears with a pre-mix X = x + u y:  Y1 = Y + D X ; X2 = X - D^-1 Y1 = -D^-1 y ; then Y1 = D x + (1 + u D) y, clean iff (1 + u D) is a multiple of D^-1
    flat = lambda M: [x for r in M for x in r]
    r_all = rank([flat(E), flat(D), flat(Di)]); r_two = rank([flat(D), flat(Di)])
    two = (r_all == 2)            # then 1 lies in the span of D and D^-1 ... and 1 + uD = lam D^-1 is solvable
    # eigenvalues: which of 1, i, -1, -i occur = rank of the spectral projectors
    w = [ONE, I, -ONE, -I]; P2, P3 = mm(D, D), mm(mm(D, D), D)
    ev = []
    for k in range(4):
        wk = [ONE, w[(4 - k) % 4], w[(8 - 2 * k) % 4], w[(12 - 3 * k) % 4]]
        Pk = madd(madd(madd(scal(E, wk[0]), D, wk[1]), P2, wk[2]), P3, wk[3])
        ev.append(rank(Pk))
    print("f = %d columns (%d addresses): three-shear exchange gives X2 = -D y, Y3 = D^-1 x: %s ; rank of {1, D, D^-1} = %d (of {D, D^-1}: %d) -> two-shear exchange with a pre-mix: %s ; multiplicity of the eigenvalues 1, i, -1, -i of D: %s"
          % (f, N, ok3, r_all, r_two, "EXISTS (and is worth nothing: two calls for two moves, the plain count)" if two else "its last free step is IMPOSSIBLE", ev))
    if f == 1:
        u = G(F(-1, 2), F(1, 2))                    # u = (i - 1)/2 : 1 + u D = a D^-1
        lhs = madd(E, D, u); assert eq(lhs, scal(Di, a))
        Xm = add(X, Y, u); Y1 = add(Y, lin(Xm, D)); X2 = add(Xm, lin(Y1, Di), -ONE); Yc = add(Y1, X2, a)
        print("        f = 1, explicit: X = x + u y, u = (i-1)/2 ; Y1 = Y + D X ; X2 = X - D^-1 Y1 = -D^-1 y : %s ; Y1 + a X2 = D x : %s"
              % (eq(X2[0], scal(E, Z)) and eq(X2[1], scal(Di, -ONE)), eq(Yc[0], D) and eq(Yc[1], scal(E, Z))))
# (4) -1 as a product of transvections of 2 x 2 matrices over a small field (brute force), n = 2
for p in (3, 5):
    vecs = [(x, y) for x in range(p) for y in range(p) if (x, y) != (0, 0)]
    tv = set()
    for (a1, a2) in vecs:
        for (b1, b2) in vecs:
            if (a1 * b1 + a2 * b2) % p == 0:
                tv.add(((1 + a1 * b1) % p, (a1 * b2) % p, (a2 * b1) % p, (1 + a2 * b2) % p))
    mul = lambda A, B: ((A[0]*B[0] + A[1]*B[2]) % p, (A[0]*B[1] + A[1]*B[3]) % p, (A[2]*B[0] + A[3]*B[2]) % p, (A[2]*B[1] + A[3]*B[3]) % p)
    m1 = (p - 1, 0, 0, p - 1)
    two = any(mul(A, B) == m1 for A in tv for B in tv)
    pr2 = {mul(A, B) for A in tv for B in tv}
    three = any(mul(A, B) == m1 for A in pr2 for B in tv)
    print("field of %d elements, 2 x 2: %d transvections ; -1 a product of two: %s ; of three: %s" % (p, len(tv), two, three))
# n = 4 over the field of 3: -1 is not a product of 4 transvections (random search cannot prove it; the proof is in the report). Check 'five suffice' by one explicit product.
p = 3
import random
random.seed(1)
def tvn(n):
    while True:
        a = [random.randrange(p) for _ in range(n)]; bb = [random.randrange(p) for _ in range(n)]
        if any(a) and any(bb) and sum(x * y for x, y in zip(a, bb)) % p == 0:
            return [[(int(i == j) + a[i] * bb[j]) % p for j in range(n)] for i in range(n)]
def mulp(A, B): return [[sum(A[i][k] * B[k][j] for k in range(len(A))) % p for j in range(len(A))] for i in range(len(A))]
m4 = [[(p - 1) if i == j else 0 for j in range(4)] for i in range(4)]
# -1_4 = block diag(-1_2, -1_2), each a product of 3: six; find five by search: fix 3 random and meet in the middle over pairs
allt = {}
vs = [v for v in itertools.product(range(p), repeat=4) if any(v)]
T = []
for av in vs:
    for bv in vs:
        if sum(x * y for x, y in zip(av, bv)) % p == 0:
            M = tuple(tuple((int(i == j) + av[i] * bv[j]) % p for j in range(4)) for i in range(4))
            allt[M] = 1
T = [ [list(r) for r in M] for M in allt]
key = lambda M: tuple(map(tuple, M))
def inv_t(M):   # inverse of a transvection I + a b^T is I - a b^T = 2I - M
    return [[(2 * int(i == j) - M[i][j]) % p for j in range(4)] for i in range(4)]
pairs = {}
for A in T:
    for B in T:
        pairs.setdefault(key(mulp(A, B)), (A, B))
print("field of 3, 4 x 4: %d transvections, %d distinct products of two" % (len(T), len(pairs)))
four = any(key(mulp(m4, mulp(inv_t(B), inv_t(A)))) in pairs for A in T[:0] for B in T[:0])   # placeholder, replaced below
# -1 = t1 t2 t3 t4  <=>  t1 t2 = -1 * t4^-1 t3^-1 : both sides are products of two transvections (the inverse of a transvection is one)
neg = lambda M: tuple(tuple((-x) % p for x in r) for r in M)
four = any(neg(K) in pairs for K in pairs)
print("field of 3, 4 x 4: -1 a product of FOUR transvections: %s  (exhaustive over all products of two against all products of two)" % four)
# five: -1 = (t1 t2) (t3 t4) t5  <=>  (t1 t2) = -1 * t5^-1 * (t3 t4)^-1 ; (t3 t4)^-1 is again a product of two
five = False
for t5 in T:
    it5 = inv_t(t5)
    for K in itertools.islice(pairs, 0, None):
        L = key(mulp(mulp(m4, it5), [list(r) for r in K]))
        if L in pairs: five = True; break
    if five: break
print("field of 3, 4 x 4: -1 a product of FIVE transvections: %s" % five)
