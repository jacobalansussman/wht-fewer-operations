# 16 points, exact rationals.  Three programs written out gate by gate in count (O) (add, sub, scale: 1 each),
# each checked against its target matrix, then candidate "conserved" totals tabulated.
#  T : textbook, 4 butterfly layers, target H16 = H2^(x)4
#  G : Grover form in two passes, target ((J-2I)/2)^(x)2 * (output scales), which is H16 up to signed relabelling and scale
#  C : "4x - 2 rows - 2 cols + total" computed naively (the Clebsch reading), same target as G up to scale
from fractions import Fraction as Fr
import math
N = 16
def e(j): return tuple(Fr(int(i == j)) for i in range(N))
def add(u, v): return tuple(a + b for a, b in zip(u, v))
def sub(u, v): return tuple(a - b for a, b in zip(u, v))
def sc(c, u): return tuple(Fr(c) * a for a in u)
class Prog:
    def __init__(s): s.w = [e(j) for j in range(N)]; s.kind = ['in'] * N
    def A(s, i, j): s.w.append(add(s.w[i], s.w[j])); s.kind.append('add'); return len(s.w) - 1
    def S(s, i, j): s.w.append(sub(s.w[i], s.w[j])); s.kind.append('add'); return len(s.w) - 1
    def M(s, c, i): s.w.append(sc(c, s.w[i])); s.kind.append('scale'); return len(s.w) - 1
def textbook():
    p = Prog(); cur = list(range(N))
    for b in range(4):
        nxt = list(cur)
        for x in range(N):
            if not (x >> b) & 1:
                y = x | (1 << b)
                nxt[x] = p.A(cur[x], cur[y]); nxt[y] = p.S(cur[x], cur[y])
        cur = nxt
    return p, cur
def grover_pass(p, cur, axis):
    nxt = list(cur)
    for line in range(4):
        idx = [4 * line + k for k in range(4)] if axis == 0 else [4 * k + line for k in range(4)]
        s = p.A(cur[idx[0]], cur[idx[1]]); s = p.A(s, cur[idx[2]]); s = p.A(s, cur[idx[3]])
        h = p.M(Fr(1, 2), s)
        for t in idx: nxt[t] = p.S(h, cur[t])
    return nxt
def grover():
    p = Prog(); cur = list(range(N))
    cur = grover_pass(p, cur, 0); cur = grover_pass(p, cur, 1)
    return p, cur
H2 = [[1, 1], [1, -1]]
def kron(A, B): return [[a * b for a in ra for b in rb] for ra in A for rb in B]
H16 = kron(kron(H2, H2), kron(H2, H2))
J2I = [[Fr(1, 2) - (1 if i == j else 0) for j in range(4)] for i in range(4)]
G16 = kron(J2I, J2I)
def rowsof(p, outs): return [list(p.w[o]) for o in outs]
def supp(v): return sum(1 for a in v if a != 0)
def matvec_row(v, M): return [sum(v[k] * M[k][j] for k in range(N)) for j in range(N)]
def table(name, p, outs, target):
    M = rowsof(p, outs)
    ok = all(M[i][j] == target[i][j] for i in range(N) for j in range(N))
    # co-support of a wire w: the number of OUTPUTS needed to write w, i.e. support of w * target^{-1};
    # target is an involution up to scale here (target^2 = c I), so w * target has the same support.
    A = sum(1 for k in p.kind if k == 'add'); S = sum(1 for k in p.kind if k == 'scale')
    tot = 0.0; oncurve = 0; hist = {}
    for w, k in zip(p.w, p.kind):
        if k == 'in': continue
        s1 = supp(w); s2 = supp(matvec_row(w, target))
        tot += math.log2(s1 * s2); hist[(s1, s2)] = hist.get((s1, s2), 0) + 1
        if s1 * s2 == N: oncurve += 1
    gates_G = A
    print("%s: correct=%s  additions=%d scalings=%d  count(O)=%d  count(G)=%d  excess(G)=%d" % (name, ok, A, S, A + S, gates_G, gates_G - 16 - 16 + 2))
    print("   sum over made wires of log2(support*co-support) = %.3f ; wires on the curve support*co-support=16: %d of %d" % (tot, oncurve, A + S))
    print("   (support, co-support) histogram:", sorted(hist.items()))
p, o = textbook(); table("textbook", p, o, H16)
p, o = grover(); table("Grover two passes", p, o, G16)
# general size 4^k for the Grover two-pass form: additions 7*(N/4)*k, scalings (N/4)*k
for k in range(1, 7):
    n = 4 ** k
    print("N=4^%d=%d: additions %d + scalings %d = %d ; N log2 N = %d" % (k, n, 7 * (n // 4) * k, (n // 4) * k, 8 * (n // 4) * k, n * 2 * k))
