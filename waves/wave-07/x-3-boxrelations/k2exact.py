# x-3 boxrelations, exact replay at K = 2 (fractions). Table X = alpha*1 + beta*J + [[p, q], [q, -p]], J = [[0, -1], [1, 0]].
# (a) rotations A (A A^T = 1, det +1):  A X A^T = alpha*1 + beta*J + S(A(A(p, q)))            two nested calls, glue 1 between
# (b) reflections A (A A^T = 1, det -1): A X A^T = alpha*1 - beta*J + S(A(sz A(p, q))), sz = diag(1, -1)   two nested calls
# (c) the two programs differ (glue 1 against sz, sign of beta): each fails on the other component (checked).
# (d) first-order formula for the rotations' tangent line, so(2) = multiples of J: [J, X] = S(2 J (p, q)): ONE call.
# (e) so(3): [S, X] for a 3 x 3 table X with FOUR calls of S (three on the columns of the symmetric part, one on the vector of the skew part); textbook 6.
from fractions import Fraction as F
import random
random.seed(5)
def mm(A, B): return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def tr(A): return [list(r) for r in zip(*A)]
def app(A, v): return [sum(A[i][k]*v[k] for k in range(len(v))) for i in range(len(A))]
def S(v): return [[v[0], v[1]], [v[1], -v[0]]]
def circle():
    t = F(random.randint(-9, 9), random.randint(1, 9)); return (1 - t*t)/(1 + t*t), 2*t/(1 + t*t)
na = nb = nc = 0
for trial in range(200):
    c, s = circle(); X = [[F(random.randint(-9, 9)) for _ in range(2)] for _ in range(2)]
    al = (X[0][0] + X[1][1])/2; be = (X[1][0] - X[0][1])/2; p = (X[0][0] - X[1][1])/2; q = (X[0][1] + X[1][0])/2
    for det in (1, -1):
        A = [[c, -s], [s, c]] if det == 1 else [[c, s], [s, -c]]
        want = mm(mm(A, X), tr(A))
        c1 = app(A, [p, q])
        ga = S(app(A, c1)); gota = [[al + ga[0][0], -be + ga[0][1]], [be + ga[1][0], al + ga[1][1]]]
        gb = S(app(A, [c1[0], -c1[1]])); gotb = [[al + gb[0][0], be + gb[0][1]], [-be + gb[1][0], al + gb[1][1]]]
        if det == 1: assert gota == want; na += 1; nc += (gotb != want)
        else: assert gotb == want; nb += 1; nc += (gota != want)
print('(a) rotations, 2 nested calls: %d exact cases right; (b) reflections, 2 nested calls: %d exact cases right' % (na, nb))
print('(c) each program applied to the other component is wrong in %d of %d cases' % (nc, na + nb))
J = [[F(0), F(-1)], [F(1), F(0)]]; nd = 0
for trial in range(100):
    X = [[F(random.randint(-9, 9)) for _ in range(2)] for _ in range(2)]
    p = (X[0][0] - X[1][1])/2; q = (X[0][1] + X[1][0])/2
    JX = mm(J, X); XJ = mm(X, J); want = [[JX[i][j] - XJ[i][j] for j in range(2)] for i in range(2)]
    c1 = app(J, [2*p, 2*q]); assert S(c1) == want; nd += 1
print('(d) so(2): [J, X] by one call: %d exact cases right' % nd)
ne = 0
for trial in range(100):
    s = [F(random.randint(-9, 9)) for _ in range(3)]; Sm = [[0, -s[2], s[1]], [s[2], 0, -s[0]], [-s[1], s[0], 0]]
    X = [[F(random.randint(-9, 9)) for _ in range(3)] for _ in range(3)]
    Xs = [[(X[i][j] + X[j][i])/2 for j in range(3)] for i in range(3)]; Xa = [[(X[i][j] - X[j][i])/2 for j in range(3)] for i in range(3)]
    xi = [Xa[2][1], Xa[0][2], Xa[1][0]]                       # the vector of the skew part
    cols = [app(Sm, [Xs[i][j] for i in range(3)]) for j in range(3)]   # calls 1 to 3: S on the columns of the symmetric part
    v = app(Sm, xi)                                           # call 4: S on the vector of the skew part
    M = [[cols[j][i] for j in range(3)] for i in range(3)]    # M = S Xs
    got = [[M[i][j] + M[j][i] for j in range(3)] for i in range(3)]
    V = [[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]]
    got = [[got[i][j] + V[i][j] for j in range(3)] for i in range(3)]
    SX = mm(Sm, X); XS = mm(X, Sm); want = [[SX[i][j] - XS[i][j] for j in range(3)] for i in range(3)]
    assert got == want; ne += 1
print('(e) so(3): [S, X] by four calls: %d exact cases right' % ne)
