# q-cross hybrid 2: tau is a cross-ratio.  Per address bit there are four points on the projective line of forms:
# the inputs e0 = (1,0), e1 = (0,1) and the outputs r0 = (1,1), r1 = (1,tau).  Exact fractions / Gaussian-free: tau rational here,
# the sixth roots are handled by the algebra in the report.
from fractions import Fraction as Fr
from itertools import permutations
def cr(p, q, r, s):   # cross-ratio of four points given as (a,b) ~ a/b on the line; det-based, exact
    d = lambda u, v: u[0] * v[1] - u[1] * v[0]
    return Fr(d(p, r) * d(q, s), d(p, s) * d(q, r))
def pts(tau): return {'e0': (Fr(1), Fr(0)), 'e1': (Fr(0), Fr(1)), 'r0': (Fr(1), Fr(1)), 'r1': (Fr(1), Fr(tau))}
def proj_map(P, src, dst):
    # the projective map sending src[i] -> dst[i] for i = 0, 1, 2 (points as 2-vectors), returned as a 2x2 matrix
    (a, b, c), (x, y, z) = src, dst
    def frame(a, b, c):
        # columns la*a, mu*b with la*a + mu*b = c
        det = a[0] * b[1] - a[1] * b[0]
        la = (c[0] * b[1] - c[1] * b[0]) / det; mu = (a[0] * c[1] - a[1] * c[0]) / det
        return [[la * a[0], mu * b[0]], [la * a[1], mu * b[1]]]
    F, G = frame(a, b, c), frame(x, y, z)
    det = F[0][0] * F[1][1] - F[0][1] * F[1][0]
    Fi = [[F[1][1] / det, -F[0][1] / det], [-F[1][0] / det, F[0][0] / det]]
    return [[sum(G[i][k] * Fi[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def same(u, v): return u[0] * v[1] == u[1] * v[0]
def app(M, u): return (M[0][0] * u[0] + M[0][1] * u[1], M[1][0] * u[0] + M[1][1] * u[1])
names = ['e0', 'e1', 'r0', 'r1']
print("cross-ratio (e0,e1;r0,r1) with this convention, and the symmetries of the four points:")
for tau in (Fr(-1), Fr(2), Fr(1, 2), Fr(3), Fr(-2), Fr(5, 7), Fr(1, 3)):
    P = pts(tau); syms = []; mixing = []
    for perm in permutations(range(4)):
        src = [P[names[i]] for i in range(3)]; dst = [P[names[perm[i]]] for i in range(3)]
        M = proj_map(P, src, dst)
        if M[0][0] * M[1][1] - M[0][1] * M[1][0] == 0: continue
        if same(app(M, P[names[3]]), P[names[perm[3]]]):
            syms.append(perm)
            img_inputs = {names[perm[0]], names[perm[1]]}
            if img_inputs not in ({'e0', 'e1'}, {'r0', 'r1'}): mixing.append((perm, M))
    print(f"tau={str(tau):5s} cross-ratio={str(cr(P['e0'], P['e1'], P['r0'], P['r1'])):5s} symmetries={len(syms):2d}  "
          f"of which neither keep nor swap inputs|outputs: {len(mixing)}")
    for perm, M in mixing[:2]:
        print("      ", {names[i]: names[perm[i]] for i in range(4)}, "matrix", [[str(v) for v in row] for row in M])
