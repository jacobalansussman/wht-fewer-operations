# k-cross: build the explicit 19-gate circuit (count G: every line one gate a*u + b*v) for the third Kronecker power of
# other 2x2 kernels, and replay it exactly on the 8 basis vectors. Exact fractions.
from fractions import Fraction as Fr
import sys
sys.path.insert(0, '.')
exc = {2:{7,1}, 3:{5,3}, 7:{7,6,3,4}, 1:{7,6,2,5}, 4:{7,1,2,3,4,5}, 5:{5,3,0,1,6,7}, 6:{5,4,1,6}, 0:{5,4,0,7}}
terms = [((1,2,4,7),(7,)), ((0,3,5,6),(5,)), ((1,7),(6,)), ((0,6),(4,)), ((3,5),(3,)), ((2,4),(1,)),
         ((0,),(0,7)), ((6,),(1,6)), ((1,),(2,5)), ((7,),(3,4)), ((5,),(0,1,6,7)), ((4,),(2,3,4,5))]

def solve(vecs, target):
    n = len(vecs); rows = [[vecs[t][e] for t in range(n)] + [target[e]] for e in range(len(target))]
    r = 0; piv = []
    for c in range(n):
        p = next((i for i in range(r, len(rows)) if rows[i][c] != 0), None)
        if p is None: continue
        rows[r], rows[p] = rows[p], rows[r]
        rows[r] = [x / rows[r][c] for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] != 0:
                f = rows[i][c]; rows[i] = [x - f*y for x, y in zip(rows[i], rows[r])]
        piv.append(c); r += 1
    assert all(row[-1] == 0 for row in rows[r:]), "no solution"
    assert len(piv) == n, "constants not unique"
    return [rows[i][-1] for i in range(n)]

def build(name, K, sig, pi, fh):
    Kp = [[Fr(K[pi[j]][sig[i]]) for i in range(8)] for j in range(8)]
    c = [None]*8
    for i in range(8):
        if i not in (1, 7): c[i] = Kp[2][i]
    lam = Kp[2][0] / Kp[3][0]; c[1] = lam*Kp[3][1]; c[7] = lam*Kp[3][7]
    a = [next(iter({Kp[j][i] / c[i] for i in range(8) if i not in exc[j]})) for j in range(8)]
    R = [Kp[j][i] - a[j]*c[i] for j in range(8) for i in range(8)]
    vecs = [[(a[j]*c[i] if (j in nu and i in mu) else Fr(0)) for j in range(8) for i in range(8)] for (nu, mu) in terms]
    p = dict(zip(terms, solve(vecs, R)))
    P = lambda nu, mu: p[(tuple(nu), tuple(mu))]
    e = [[Fr(int(i == j)) for j in range(8)] for i in range(8)]
    W = {('x%d' % i): e[i] for i in range(8)}; lines = []
    def gate(nm, ca, u, cb, v):
        assert ca != 0 and cb != 0, "a zero coefficient: the shape degenerates here"
        W[nm] = [ca*x + cb*y for x, y in zip(W[u], W[v])]; lines.append("%-4s = %s * %s + %s * %s" % (nm, ca, u, cb, v))
    gate('g1', c[0], 'x0', c[7], 'x7'); gate('g2', c[1], 'x1', c[6], 'x6'); gate('g3', c[2], 'x2', c[5], 'x5'); gate('g4', c[3], 'x3', c[4], 'x4')
    gate('g5', 1, 'g1', 1, 'g2'); gate('g6', 1, 'g3', 1, 'g4'); gate('g7', 1, 'g5', 1, 'g6')
    gate('g8', 1, 'g7', P((1,2,4,7),(7,))*c[7], 'x7'); gate('g9', 1, 'g7', P((0,3,5,6),(5,))*c[5], 'x5')
    gate('g10', 1, 'g8', P((1,7),(6,))*c[6], 'x6'); gate('g11', 1, 'g9', P((0,6),(4,))*c[4], 'x4')
    gate('y7', 1, 'g10', P((7,),(3,4)), 'g4'); gate('y1', 1, 'g10', P((1,),(2,5)), 'g3')
    gate('y6', 1, 'g11', P((6,),(1,6)), 'g2'); gate('y0', 1, 'g11', P((0,),(0,7)), 'g1')
    gate('y2', 1, 'g8', P((2,4),(1,))*c[1], 'x1'); gate('y4', 1, 'y2', P((4,),(2,3,4,5)), 'g6')
    gate('y3', 1, 'g9', P((3,5),(3,))*c[3], 'x3'); gate('y5', 1, 'y3', P((5,),(0,1,6,7)), 'g5')
    ok = all([a[j]*x for x in W['y%d' % j]] == Kp[j] for j in range(8))
    big = max(max(abs(v.numerator), v.denominator) for v in list(p.values()) + c + a)
    print(name, ": gates", len(lines), "; every output y_j times the number a_j is exactly row pi(j) of the kernel power, columns in the order sig:", ok,
          "; all 12 constants non-zero:", all(v != 0 for v in p.values()), "; largest numerator or denominator", big)
    fh.write("# %s : 19 gates, count (G). Circuit input x_i is kernel column %s[i]; output y_j times a_j is kernel row %s[j].\n# a = %s\n" % (name, list(sig), [pi[j] for j in range(8)], [str(v) for v in a]))
    for l in lines: fh.write(l + "\n")
    fh.write("\n")

def kpow(k):
    return [[Fr(k[a >> 2 & 1][x >> 2 & 1]) * k[a >> 1 & 1][x >> 1 & 1] * k[a & 1][x & 1] for x in range(8)] for a in range(8)]
sig = (0, 1, 2, 3, 7, 6, 5, 4); pi = {2: 1, 3: 4, 7: 0, 1: 2, 6: 5, 0: 7, 4: 3, 5: 6}
with open('class19.txt', 'w') as fh:
    for nm, k in [("[[1,2],[2,1]]", [[1,2],[2,1]]), ("[[1,3],[3,1]]", [[1,3],[3,1]]), ("[[1,2],[3,4]]", [[1,2],[3,4]]), ("[[1,2],[2,3]]", [[1,2],[2,3]]),
                  ("[[2,7],[5,3]]", [[2,7],[5,3]]), ("[[1,1],[1,-1]] (the transform)", [[1,1],[1,-1]]), ("[[1,100],[1,1]] (near subset sums)", [[1,100],[1,1]])]:
        try: build("kernel " + nm + " cubed", kpow(k), sig, pi, fh)
        except AssertionError as ex: print("kernel", nm, ": this wiring fails:", ex)
