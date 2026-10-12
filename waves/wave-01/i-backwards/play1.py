#!/usr/bin/env python3
"""i-backwards play 1: exact (integer / Fraction) facts about the 4- and 16-point Walsh-Hadamard matrix.
A. Householder form: a column-relabelled, re-signed H4 equals 2I - u u^T; 7 additions with free doubling.
B. LDU: H = Z D Z^T with Z the subset-sum (zeta) matrix and D = diag((-2)^|x|): all of Morgenstern's volume in one diagonal.
C. Minimal-support eigenvectors of H16 (support 4 = sqrt 16): enumerate every 4-subset exactly; span dimensions.
D. Zak basis of a self-dual code V: H g_{a,b} = +-4 g_{b,a} (H is a signed transposition in that basis).
E. Wire profile (support, co-support) of the textbook circuit and of the Householder circuit.
"""
from fractions import Fraction as F
from itertools import combinations, product
import sys

def pc(x): return bin(x).count("1")
def had(k):
    n = 1 << k
    return [[(-1) ** pc(x & y) for x in range(n)] for y in range(n)]
def matmul(A, B):
    return [[sum(A[i][t] * B[t][j] for t in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def rank(M):
    M = [[F(v) for v in r] for r in M]; r = 0
    rows, cols = len(M), len(M[0]) if M else 0
    for c in range(cols):
        p = next((i for i in range(r, rows) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        pv = M[r][c]
        M[r] = [v / pv for v in M[r]]
        for i in range(rows):
            if i != r and M[i][c] != 0:
                f = M[i][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
        if r == rows: break
    return r
def nullspace(M):
    M = [[F(v) for v in r] for r in M]; rows, cols = len(M), len(M[0]); r = 0; piv = []
    for c in range(cols):
        p = next((i for i in range(r, rows) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]; pv = M[r][c]; M[r] = [v / pv for v in M[r]]
        for i in range(rows):
            if i != r and M[i][c] != 0:
                f = M[i][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        piv.append(c); r += 1
        if r == rows: break
    free = [c for c in range(cols) if c not in piv]; out = []
    for fc in free:
        v = [F(0)] * cols; v[fc] = F(1)
        for i, c in enumerate(piv): v[c] = -M[i][fc]
        out.append(v)
    return out

print("== A. Householder form ==")
H4 = had(2)
# column relabelling/sign: search signed permutations W with H4 W symmetric, diagonal all +1
from itertools import permutations
best = None
for perm in permutations(range(4)):
    for sg in product([1, -1], repeat=4):
        M = [[H4[y][perm[x]] * sg[x] for x in range(4)] for y in range(4)]
        if all(M[i][i] == 1 for i in range(4)) and all(M[i][j] == M[j][i] for i in range(4) for j in range(4)):
            best = (perm, sg, M); break
    if best: break
perm, sg, M4 = best
print("signed column relabelling", perm, sg);
for r in M4: print("  ", r)
L4 = [[M4[i][j] - (2 if i == j else 0) for j in range(4)] for i in range(4)]
print("rank(H4' - 2I) =", rank(L4), " rows of H4'-2I:", L4[0], L4[1])
def kron(A, B):
    return [[a * b for a in ra for b in rb] for ra in A for rb in B]
M16 = kron(M4, M4); M64 = kron(M16, M4)
for nm, M, s in (("16", M16, 4), ("64", M64, 8)):
    n = len(M)
    print("N=%s: rank(H' - sqrtN I) = %d   (N/2 - sqrtN/2 = %d),  rank(H' + sqrtN I) = %d" % (
        nm, rank([[M[i][j] - (s if i == j else 0) for j in range(n)] for i in range(n)]), n // 2 - s // 2,
        rank([[M[i][j] + (s if i == j else 0) for j in range(n)] for i in range(n)])))
H16 = had(4)
print("plain Sylvester N=16: rank(H-4I) =", rank([[H16[i][j] - (4 if i == j else 0) for j in range(16)] for i in range(16)]))
# straight-line program, 4 points, free scaling: s = x0 - x1 - x2 + x3 (3 adds); y_i = 2 x_i -/+ s (4 adds)
u = [-L4[0][j] // (-L4[0][0]) * 1 for j in range(4)]
# recover u from L4 = -u u^T: u_j = L4[0][j] / -u_0 with u_0 = 1
u = [1] + [-L4[0][j] for j in range(1, 4)]
ok = all(L4[i][j] == -u[i] * u[j] for i in range(4) for j in range(4))
print("u =", u, " H4' = 2I - u u^T :", ok, "-> 3 additions for u.x, 4 for 2x_i - u_i (u.x): 7 additions (textbook 8); 16 points: 8 calls = 56 (textbook 64)")

print("== B. LDU: H = Z D Z^T ==")
for k in (2, 4):
    n = 1 << k
    Z = [[1 if (y & t) == t else 0 for t in range(n)] for y in range(n)]      # Z[y][T] = [T subset y]
    D = [[((-2) ** pc(t) if i == t else 0) for t in range(n)] for i in range(n)]
    ZT = [list(r) for r in zip(*Z)]
    print("k=%d: Z D Z^T == H :" % k, matmul(matmul(Z, D), ZT) == had(k), " nnz(Z) = %d = 3^k, sum of log2|D| = %d = (N/2) log2 N = %d" % (
        sum(map(sum, Z)), sum(pc(t) for t in range(n)), n // 2 * k))
# truncation: keep |T| <= d : exact wherever |x & y| <= d
k = 4; n = 16
for d in range(0, 5):
    Hd = [[sum((-2) ** j * (1 if j <= pc(x & y) else 0) * __import__("math").comb(pc(x & y), j) for j in range(d + 1)) for x in range(n)] for y in range(n)]
    diff = [[H16[y][x] - Hd[y][x] for x in range(n)] for y in range(n)]
    print("  k=4 keep |T|<=%d: rank(low part) = %2d, non-zeros of remainder = %3d, remainder lives on |x&y| > %d : %s" % (
        d, rank(Hd), sum(1 for r in diff for v in r if v), d, all((diff[y][x] == 0) or pc(x & y) > d for x in range(n) for y in range(n))))

print("== C. minimal-support eigenvectors of H16 ==")
I16 = [[1 if i == j else 0 for j in range(16)] for i in range(16)]
res = {}
for lam in (4, -4):
    A = [[H16[i][j] - (lam if i == j else 0) for j in range(16)] for i in range(16)]
    vecs = []
    for sz in (1, 2, 3, 4):
        cnt = 0
        for S in combinations(range(16), sz):
            sub = [[A[i][j] for j in S] for i in range(16)]
            ns = nullspace(sub)
            for v in ns:
                if all(c != 0 for c in v):
                    cnt += 1
                    full = [F(0)] * 16
                    for j, c in zip(S, v): full[j] = c
                    vecs.append((S, full))
        print("  eigenvalue %+d: eigenvectors with support exactly %d: %d" % (lam, sz, cnt))
    res[lam] = vecs
    print("  eigenvalue %+d: span of the support-4 eigenvectors has dimension %d (eigenspace: 8)" % (lam, rank([v for _, v in vecs]) if vecs else 0))
    supp_types = {}
    for S, v in vecs:
        x = 0
        for s in S: x ^= s
        aff = (S[0] ^ S[1] ^ S[2] ^ S[3]) == 0
        key = ("affine plane" if aff else "not affine", tuple(sorted(set(abs(c) for c in v))))
        supp_types[key] = supp_types.get(key, 0) + 1
    print("   support types:", supp_types)

print("== D. Zak basis of a self-dual code ==")
def span2(gens):
    S = {0}
    for g in gens: S |= {s ^ g for s in S}
    return sorted(S)
for name, gens in (("diagonal {(v,v)}", [0b0101, 0b1010]), ("{0000,1100,0011,1111}", [0b1100, 0b0011])):
    V = span2(gens)
    selfdual = all(pc(a & b) % 2 == 0 for a in V for b in V)
    reps = []; seen = set()
    for a in range(16):
        if a not in seen:
            reps.append(a); seen |= {a ^ v for v in V}
    # g_{a,b}(x) = (-1)^{b.x} 1_{V+a}(x), a,b coset representatives
    def g(a, b): return [((-1) ** pc(b & x) if (x ^ a) in V else 0) for x in range(16)]
    okall = True; signs = []
    for a in reps:
        for b in reps:
            Hg = [sum(H16[y][x] * gx for x, gx in enumerate(g(a, b))) for y in range(16)]
            t = g(b, a)
            sgn = None
            for s in (4, -4):
                if Hg == [s * v for v in t]: sgn = s
            if sgn is None: okall = False
            signs.append(sgn)
    B = [g(a, b) for a in reps for b in reps]
    print("  V = %s self-dual: %s; 16 functions g_{a,b}, rank %d; H g_{a,b} = +-4 g_{b,a} for all: %s; fixed (a=b) signs: %s" % (
        name, selfdual, rank(B), okall, [signs[i * 4 + i] for i in range(4)]))

print("== E. wire profiles (support, co-support) ==")
def cosupp(form):   # form as row vector l; l = mu H  => mu = l H / 16
    mu = [sum(form[x] * H16[x][y] for x in range(16)) for y in range(16)]
    return sum(1 for v in mu if v)
# textbook: after j butterfly levels, wire (x) holds sum over the subcube on bits < j
prof = {}
for j in range(5):
    for x in range(16):
        form = [0] * 16
        mask = (1 << j) - 1
        for z in range(16):
            if (z & ~mask) == (x & ~mask): form[z] = (-1) ** pc(z & x & mask)
        key = (sum(1 for v in form if v), cosupp(form)); prof[key] = prof.get(key, 0) + 1
print("  textbook wires (support, co-support): count ", sorted(prof.items()))
# Householder on the Kronecker-relabelled matrix M16 = M4 (x) M4: inner-product wires s = (u on digit 1) for each value of digit 2
def cosuppM(form, M):
    # form = mu M  => mu = form M^T / 16  (M orthogonal up to 16)
    mu = [sum(form[x] * M[y][x] for x in range(16)) for y in range(16)]
    return sum(1 for v in mu if v)
prof = {}
for b in range(4):
    form = [0] * 16
    for a in range(4): form[4 * a + b] = u[a]
    key = (4, cosuppM(form, M16)); prof[key] = prof.get(key, 0) + 1
print("  Householder inner-product wires u.x on one digit (support, co-support w.r.t. H16'):", sorted(prof.items()))
form = [u[a] * u[b] for a in range(4) for b in range(4)]
print("  wire u(x)u . x: support 16, co-support", cosuppM(form, M16))
