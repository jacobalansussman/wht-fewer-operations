# brick.py  (g-3-illconditioned): exact check, rationals, count (G).
# Identity [derived tonight]: for EVERY symmetric 2 x 2 matrix k = [[a, b], [b, d]]
#       k (x) k  =  v v^T  +  det(k) * P',     v = (a, b, b, d) = the kernel written as a vector,
#       P' = the signed relabelling with +1 at (01,01), (10,10) and -1 at (00,11), (11,00).
# Consequence: the 4-point Kronecker square of every 2 x 2 kernel with non-zero off-diagonal entries costs 7 gates
# (a kernel [[a,b],[c,d]] is a row scaling of the symmetric kernel [[a,b],[b,b*d/c]]): 3 gates for r = v.x, then
#       y00 = a*r - det*x11,  y01 = b*r + det*x01,  y10 = b*r + det*x10,  y11 = d*r - det*x00.
# For the Walsh-Hadamard kernel v = (1, 1, 1, -1): the known hub.
from fractions import Fraction as Fr
def kron(A, B): return [[x * y for x in ra for y in rb] for ra in A for rb in B]
P = [[0, 0, 0, -1], [0, 1, 0, 0], [0, 0, 1, 0], [-1, 0, 0, 0]]
def check(a, b, c, d):
    a, b, c, d = map(Fr, (a, b, c, d))
    lam = c / b; ds = d / lam                      # [[a,b],[c,d]] = diag(1, lam) * [[a,b],[b,ds]]
    det = a * ds - b * b; v = [a, b, b, ds]
    KK = kron([[a, b], [b, ds]], [[a, b], [b, ds]])
    ident = all(KK[i][j] == v[i] * v[j] + det * P[i][j] for i in range(4) for j in range(4))
    x = [[Fr(int(i == j)) for j in range(4)] for i in range(4)]
    g = lambda p, u, q, w: [p * s + q * t for s, t in zip(u, w)]
    r1 = g(a, x[0], b, x[1]); r2 = g(1, r1, b, x[2]); r = g(1, r2, ds, x[3])               # 3 gates
    ys = [g(a, r, -det, x[3]), g(b, r, det, x[1]), g(b, r, det, x[2]), g(ds, r, -det, x[0])]   # 4 gates
    target = kron([[a, b], [c, d]], [[a, b], [c, d]])
    scale = [Fr(1), lam, lam, lam * lam]            # row scalings are free in count (G)
    circ = all(ys[i][j] * scale[i] == target[i][j] for i in range(4) for j in range(4))
    print(f"kernel [[{a},{b}],[{c},{d}]]: identity exact: {ident}; 7-gate circuit gives the Kronecker square exactly (after free row scalings): {circ}; hub v = {[str(t) for t in v]}; det = {det}")
for k in [(1, 1, 1, -1), (1, 2, 2, 1), (1, Fr(1, 3), Fr(1, 3), 1), (1, Fr(-5, 7), Fr(-5, 7), 1), (2, 3, 3, 7), (1, 1, 1, 2), (1, 2, 3, 5), (0, 1, 1, 1), (3, 1, 4, 1)]:
    check(*k)
