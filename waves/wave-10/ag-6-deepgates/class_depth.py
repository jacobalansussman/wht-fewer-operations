# class_depth.py : the 19-gate wiring for the third power of the kernel [[1,t],[t,1]] (k-cross/class19.txt gives it for t = 2, 3),
# rebuilt here for any whole number t from one formula, replayed in whole numbers, every gate reduced to primitive wires:
# g*w = a*u + b*v.  Prints the kinds, the 2-adic depth of each gate (largest power of 2 dividing a, b or g), the determinant of
# the outputs, and Morgenstern's count for circuits with coefficients 1 and 2 and no division (each gate multiplies the largest
# minor by at most 3).
import sys, math
from fractions import Fraction as F
def prim(v):
    g = 0
    for x in v: g = math.gcd(g, abs(x))
    s = next(x for x in v if x); s = 1 if s > 0 else -1
    return tuple(s * x // g for x in v)
def kind(u, v, w):
    n = len(u)
    for i in range(n):
        for j in range(i + 1, n):
            D = u[i] * v[j] - u[j] * v[i]
            if D:
                a = w[i] * v[j] - w[j] * v[i]; b = u[i] * w[j] - u[j] * w[i]
                assert all(D * w[l] == a * u[l] + b * v[l] for l in range(n)) and a and b
                g0 = math.gcd(math.gcd(abs(a), abs(b)), abs(D)); return (abs(a) // g0, abs(b) // g0, abs(D) // g0)
def v2(x):
    e = 0
    while x % 2 == 0: x //= 2; e += 1
    return e
def det(M):
    M = [[F(x) for x in r] for r in M]; n = len(M); d = F(1)
    for c in range(n):
        p = next((r for r in range(c, n) if M[r][c]), None)
        if p is None: return 0
        if p != c: M[c], M[p] = M[p], M[c]; d = -d
        d *= M[c][c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            for k in range(c, n): M[r][k] -= f * M[c][k]
    return d
def run(t, show):
    # wiring of k-cross/class19.txt; the coefficients below are those of the file for t = 2 and t = 3 written as functions of t
    colperm = [0, 1, 2, 3, 7, 6, 5, 4]; rowperm = [7, 2, 1, 4, 3, 6, 5, 0]; c = t * t - 1
    X = {('x%d' % i): tuple(1 if j == i else 0 for j in range(8)) for i in range(8)}
    prog = [('g1', t, 'x0', 1, 'x7'), ('g2', t * t, 'x1', t, 'x6'), ('g3', t * t, 'x2', t ** 3, 'x5'), ('g4', t, 'x3', t * t, 'x4'),
            ('g5', 1, 'g1', 1, 'g2'), ('g6', 1, 'g3', 1, 'g4'), ('g7', 1, 'g5', 1, 'g6'),
            ('g8', 1, 'g7', c, 'x7'), ('g9', 1, 'g7', -c * t, 'x5'), ('g10', 1, 'g8', c * t, 'x6'), ('g11', 1, 'g9', -c, 'x4'),
            ('y7', 1, 'g10', c, 'g4'), ('y1', 1, 'g10', F(-c, t * t), 'g3'), ('y6', 1, 'g11', F(-c, t * t), 'g2'), ('y0', 1, 'g11', c, 'g1'),
            ('y2', 1, 'g8', -c, 'x1'), ('y4', 1, 'y2', F(-c, t * t), 'g6'), ('y3', 1, 'g9', c * t, 'x3'), ('y5', 1, 'y3', c, 'g5')]
    kinds = {}; depth = 0; lines = []
    for name, a, p, b, q in prog:
        w = tuple(a * x + b * y for x, y in zip(X[p], X[q])); den = 1
        for x in w: den = den * F(x).denominator // math.gcd(den, F(x).denominator)
        w = tuple(int(x * den) for x in w); X[name] = w
        k = kind(prim(X[p]), prim(X[q]), prim(w)); kinds[k] = kinds.get(k, 0) + 1; d = max(v2(k[0]), v2(k[1]), v2(k[2])); depth += d
        lines.append('   %-4s = %s   kind (%d,%d)/%d  depth %d' % (name, prim(w), k[0], k[1], k[2], d))
    # check: output y_j is proportional to kernel row rowperm[j], inputs relabelled by colperm
    K = lambda r, cc: t ** bin(r ^ cc).count('1')
    rows = []
    for j in range(8):
        want = prim(tuple(K(rowperm[j], colperm[i]) for i in range(8))); assert prim(X['y%d' % j]) == want, (t, j); rows.append(want)
    D = abs(det(rows)); d2 = v2(int(D))
    print('t = %d: 19 gates replay OK; kinds %s; sum of gate depths %d; |det of the primitive outputs| = %s = 2^%d * %d; gates of depth >= 2: %d; Morgenstern for coefficients 1, 2 without division: at least %d gates' % (t, dict(sorted(kinds.items())), depth, D, d2, int(D) >> d2, sum(n for k, n in kinds.items() if max(v2(k[0]), v2(k[1]), v2(k[2])) >= 2), math.ceil(math.log(float(D)) / math.log(3) - 1e-9)))
    if show: print('\n'.join(lines))
for t in (2, 3, 5, 7, 9, 15, 17, 31, 63): run(t, t == 3)
