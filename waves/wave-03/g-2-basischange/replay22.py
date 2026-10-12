# replay22.py: exact replay over the rationals of the 16-point analysis map B^-1 in 22 gates (count G) with ONE head basis for all layers:
#   g1 = x3 - x4, g2 = x2 - x4, g3 = x1 - x2 - x3 + x4.   Layers 1 and 3: 6 gates each.  Layer 2: 10 gates (lifted by hand from GF(5)).
from fractions import Fraction as Fr
import itertools
def prop(u, v): return any(u) and any(v) and all(u[i] * v[j] == u[j] * v[i] for i in range(len(u)) for j in range(len(u)))
def rank(rows):
    A = [[Fr(x) for x in r] for r in rows]; r = 0
    for c in range(len(A[0])):
        piv = next((i for i in range(r, len(A)) if A[i][c] != 0), None)
        if piv is None: continue
        A[r], A[piv] = A[piv], A[r]
        for i in range(len(A)):
            if i != r and A[i][c] != 0:
                f = A[i][c] / A[r][c]; A[i] = [x - f * y for x, y in zip(A[i], A[r])]
        r += 1
    return r
lin = lambda u, v, a, b: [a * x + b * y for x, y in zip(u, v)]
G1 = [(0, 0, 1, -1), (0, 1, 0, -1), (1, -1, -1, 1)]
# layer 1
x = [[int(i == j) for j in range(4)] for i in range(4)]
g1 = lin(x[2], x[3], 1, -1); g2 = lin(x[1], x[3], 1, -1); p = lin(x[0], x[3], 1, 1); q = lin(x[1], x[2], 1, 1); g3 = lin(p, q, 1, -1); s = lin(p, q, 1, 1)
ok1 = all(any(prop(list(t), o) for o in (g1, g2, g3)) for t in G1) and s == [1] * 4
print("layer 1: 6 gates (helpers x1+x4, x2+x3):", ok1)
# layer 2: wires x12, x13, x23, x14, x24, x34
pairs = [(0, 1), (0, 2), (1, 2), (0, 3), (1, 3), (2, 3)]
e = [[int(i == j) for j in range(6)] for i in range(6)]; x12, x13, x23, x14, x24, x34 = e
o1 = lin(x14, x23, 1, -1)          # 1  output: U g3 / 2
A = lin(x12, x34, 1, 1)            # 2  helper
h8 = lin(A, x24, 1, -1)            # 3  helper
o2 = lin(h8, x13, 1, -1)           # 4  output: head A - B
h10 = lin(A, o1, 1, 1)             # 5  helper (uses output 1)
o3 = lin(h10, x12, 1, -2)          # 6  output: -U g2
h12 = lin(h10, o2, 1, 1)           # 7  helper (uses output 4)
o4 = lin(h12, h8, 1, -2)           # 8  output: -U g1
o5 = lin(h12, x14, 1, -2)          # 9  output: head 2A - B - C
o6 = lin(o5, A, 1, -3)             # 10 output: minus the total (made from a head)
Ug = lambda g: [g[a] + g[b] for a, b in pairs]
Dn = lambda f: [sum(f[n] for n, P in enumerate(pairs) if i in P) for i in range(4)]
outs = [o1, o2, o3, o4, o5, o6]
ok2 = prop(o1, Ug(G1[2])) and prop(o3, Ug(G1[1])) and prop(o4, Ug(G1[0])) and prop(o6, [1] * 6) and not any(Dn(o2)) and not any(Dn(o5)) and rank(outs) == 6
print("layer 2: 10 gates:", ok2, " outputs:", outs)
print("total one way at 16 points with one common head basis: 6 + 10 + 6 = 22 gates:", ok1 and ok2)
# the dual basis (needed for the way out): rows of (G G^T)^-1 G
G = [[Fr(v) for v in g] for g in G1]; Gram = [[sum(a * b for a, b in zip(u, v)) for v in G] for u in G]
n = 3; M = [Gram[i] + [Fr(int(i == j)) for j in range(n)] for i in range(n)]
for c in range(n):
    piv = next(i for i in range(c, n) if M[i][c] != 0); M[c], M[piv] = M[piv], M[c]; M[c] = [v / M[c][c] for v in M[c]]
    for i in range(n):
        if i != c: M[i] = [a - M[i][c] * b for a, b in zip(M[i], M[c])]
inv = [r[n:] for r in M]; dual = [[sum(inv[i][j] * G[j][t] for j in range(n)) for t in range(4)] for i in range(n)]
print("dual head basis (way out):", [[str(v * 4) for v in d] for d in dual], "(times 4)")
