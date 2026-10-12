# s-cross hybrid 2, exact check of the hand formula: for a 2 x 2 reflection A = [[c, s], [s, -c]] with c^2 + s^2 = 1 (rational points),
# A X A^T = alpha*I - beta*J + [[t, u], [u, -t]] with (t, u) = A sz A (p, q), sz = diag(1, -1): two calls of A, nested.
from fractions import Fraction as F
def mul(A, B): return [[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def app(A, v): return [A[0][0]*v[0] + A[0][1]*v[1], A[1][0]*v[0] + A[1][1]*v[1]]
ok = 0
for m in range(-6, 7):
    for X in ([[1,0],[0,0]], [[0,1],[0,0]], [[0,0],[1,0]], [[0,0],[0,1]], [[3,-5],[7,11]]):
        t0 = F(m, 5); c = (1 - t0*t0)/(1 + t0*t0); s = 2*t0/(1 + t0*t0); A = [[c, s], [s, -c]]
        X = [[F(v) for v in r] for r in X]
        want = mul(mul(A, X), [[A[0][0], A[1][0]], [A[0][1], A[1][1]]])
        al = (X[0][0] + X[1][1])/2; be = (X[0][1] - X[1][0])/2; p = (X[0][0] - X[1][1])/2; q = (X[0][1] + X[1][0])/2
        c1 = app(A, [p, q]); c2 = app(A, [c1[0], -c1[1]])      # call 1, then sz, then call 2
        got = [[al + c2[0], -be + c2[1]], [be + c2[1], al - c2[0]]]
        assert got == want; ok += 1
print('two nested calls give A X A^T for every 2 x 2 reflection tested: %d exact cases' % ok)
