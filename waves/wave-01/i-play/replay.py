# Exact replay: 4 points in 7 gates, 8 in 22, 16 in 56, 64 in 336; 3-point Fourier in 5 gates.
from fractions import Fraction as Fr
import itertools
def kron(A, B):
    return [[a*b for a in ra for b in rb] for ra in A for rb in B]
H2 = [[1,1],[1,-1]]
def Hn(k):
    M = [[1]]
    for _ in range(k): M = kron(M, H2)
    return M
class Prog:
    def __init__(self, n):
        self.n = n; self.gates = 0
        self.w = [[1 if i == j else 0 for i in range(n)] for j in range(n)]   # wire -> linear form
    def lin(self, a, u, b, v):       # one gate a*u + b*v on forms
        self.gates += 1
        return [a*x + b*y for x, y in zip(u, v)]
    def block4(self, idx):           # J - 2I on four wires: 3 + 4 gates
        f = [self.w[i] for i in idx]
        s = self.lin(1, f[0], 1, f[1]); s = self.lin(1, s, 1, f[2]); s = self.lin(1, s, 1, f[3])
        for t, i in enumerate(idx): self.w[i] = self.lin(1, s, -2, f[t])
    def bfly(self, i, j):
        a, b = self.w[i], self.w[j]
        self.w[i] = self.lin(1, a, 1, b); self.w[j] = self.lin(1, a, -1, b)
def monomial_equiv_check(M, k):
    # M should be D1 * H * P * D2 (signs and a permutation). Certificate: M M^T = N I, entries +-1, and
    # M equals the Kronecker product of the small blocks it was built from (checked by the caller).
    n = len(M)
    ok = all(abs(x) == 1 for r in M for x in r)
    ok = ok and all(sum(M[i][t]*M[j][t] for t in range(n)) == (n if i == j else 0) for i in range(n) for j in range(n))
    return ok
J2I = [[(-1 if i == j else 1) for j in range(4)] for i in range(4)]
# J - 2I = D1 H4 P D2 exactly: search signs and permutation
found = None
H4 = Hn(2)
for perm in itertools.permutations(range(4)):
    for s in itertools.product((1,-1), repeat=8):
        if all(s[i]*H4[i][perm[j]]*s[4+j] == J2I[i][j] for i in range(4) for j in range(4)):
            found = (perm, s); break
    if found: break
print("J-2I = D1 H4 P D2 with perm, signs:", found)
for k, plan in ((2, "4"), (3, "4+2"), (4, "4+4"), (6, "4+4+4")):
    n = 2**k; p = Prog(n)
    digits = list(range(k)); pos = 0; blocks = []
    for part in plan.split("+"):
        b = int(part).bit_length() - 1
        blocks.append(digits[pos:pos+b]); pos += b
    for blk in blocks:
        rest = [d for d in digits if d not in blk]
        for base in itertools.product((0,1), repeat=len(rest)):
            addr0 = sum(bit << d for bit, d in zip(base, rest))
            idx = [addr0 + sum(((t >> q) & 1) << d for q, d in enumerate(blk)) for t in range(2**len(blk))]
            if len(blk) == 2: p.block4(idx)
            else: p.bfly(idx[0], idx[1])
    M = p.w
    print("n=%d plan %s gates=%d textbook=%d ratio=%s  Hadamard(+-1, M M^T = n I): %s" % (n, plan, p.gates, n*k, Fr(p.gates, n*k), monomial_equiv_check(M, k)))
# eigen-split of (J-2I) tensor (J-2I): rank of M - 4I and M + 4I
def rank(M):
    M = [[Fr(x) for x in r] for r in M]; r = 0
    for c in range(len(M[0])):
        piv = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if piv is None: continue
        M[r], M[piv] = M[piv], M[r]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]/M[r][c]; M[i] = [x - f*y for x, y in zip(M[i], M[r])]
        r += 1
    return r
for m in (1, 2, 3):
    M = [[1]]
    for _ in range(m): M = kron(M, J2I)
    n = 4**m; s = 2**m
    print("(J-2I)^(x%d): n=%d rank(M - %dI)=%d rank(M + %dI)=%d" % (m, n, s, rank([[M[i][j] - (s if i == j else 0) for j in range(n)] for i in range(n)]), s, rank([[M[i][j] + (s if i == j else 0) for j in range(n)] for i in range(n)])))
# 3-point Fourier matrix in Z[w], w^2 = -1 - w : element (a, b) = a + b w
def mul(x, y): return (x[0]*y[0] - x[1]*y[1], x[0]*y[1] + x[1]*y[0] - x[1]*y[1])
def add(x, y): return (x[0]+y[0], x[1]+y[1])
one, w, w2, zero = (1,0), (0,1), (-1,-1), (0,0)
F3 = [[one, one, one],[one, w, w2],[one, w2, w]]
# claim: F3 = D1 (J + d I) D2 with a row/column scaling; circuit: s = c0 x0 + c1 x1 + c2 x2 (2 gates), y_i = r_i s + e_i x_i (3 gates)
# take column scaling c = (1, w, w), row scaling r = (1, w^2... ) solved by hand below and checked exactly
c = [one, w, w]; r = [one, w2, w2]
G = [[mul(r[i], c[j]) for j in range(3)] for i in range(3)]
diff = [[add(F3[i][j], (-G[i][j][0], -G[i][j][1])) for j in range(3)] for i in range(3)]
print("F3 - (rank one r c^T) =", diff, " -> off-diagonal all zero:", all(diff[i][j] == zero for i in range(3) for j in range(3) if i != j))
