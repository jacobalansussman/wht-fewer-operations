# v-2: the same two nested calls work for every 2 x 2 ROTATION, with no sz in the middle: (t, u) = A A (p, q), and beta keeps its sign.
# Polynomial identity modulo c^2 + s^2 = 1 (exact). Also: what the reflection formula does on a scaled reflection t*A.
from fractions import Fraction as F
def padd(p, q, m=1):
    r = dict(p)
    for k, v in q.items():
        r[k] = r.get(k, 0) + m*v
        if r[k] == 0: del r[k]
    return r
def pmul(p, q):
    r = {}
    for (i, e), v in p.items():
        for (j, f), w in q.items():
            if e + f < 2: r = padd(r, {(i + j, e + f): v*w})
            else: r = padd(r, {(i + j, 0): v*w}); r = padd(r, {(i + j + 2, 0): -v*w})
    return r
def pmm(X, Y):
    out = [[{} for _ in range(len(Y[0]))] for _ in range(len(X))]
    for i in range(len(X)):
        for j in range(len(Y[0])):
            for k in range(len(Y)): out[i][j] = padd(out[i][j], pmul(X[i][k], Y[k][j]))
    return out
c = {(1, 0): F(1)}; s = {(0, 1): F(1)}; neg = lambda p: {k: -v for k, v in p.items()}
def const(v): return {(0, 0): F(v)} if v else {}
R = [[c, neg(s)], [s, c]]; RT = [[c, s], [neg(s), c]]; good = True
for X in ([[1,0],[0,0]], [[0,1],[0,0]], [[0,0],[1,0]], [[0,0],[0,1]]):
    Xp = [[const(v) for v in r] for r in X]; want = pmm(pmm(R, Xp), RT)
    al = F(X[0][0] + X[1][1], 2); be = F(X[0][1] - X[1][0], 2); p = F(X[0][0] - X[1][1], 2); q = F(X[0][1] + X[1][0], 2)
    c2 = pmm(R, pmm(R, [[const(p)], [const(q)]]))
    got = [[padd(const(al), c2[0][0]), padd(const(be), c2[1][0])], [padd(const(-be), c2[1][0]), padd(const(al), c2[0][0], -1)]]
    good &= (got == want)
print('rotations: R X R^T = alpha 1 + beta J + [[t,u],[u,-t]] with (t,u) = R R (p,q), two nested calls, for the four unit tables: %s' % good)
# one program for BOTH components of the orthogonal 2 x 2 matrices? the reflection program on a rotation and the other way round:
A = [[c, s], [s, neg(c)]]
c2 = pmm(R, [[c], [neg(s)]])      # reflection program (A sz A) run on a rotation, input (p,q) = (1,0): R sz R (1,0) = R (c, -s)
print('reflection program run on a rotation, (p,q) = (1,0): gives', c2, ' wanted R R (1,0) =', pmm(R, [[c], [s]]))
