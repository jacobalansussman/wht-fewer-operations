#!/usr/bin/env python3
"""d-4-codes play 1 (exact integers / Fractions).
A. N=16: the three self-dual codes of length 4, 48 atoms; transfer matrices; H as a signed permutation; hybrid bases.
B. Phase space of 4 bits: all 2295 Lagrangians; which are kept by the swap X<->Z (= bases on which H is monomial);
   how close such a basis can be to the standard basis.
C. Reflections: H4' = 2(I - u u^T/2); Householder x Householder as 8 reflections; the compact formula I - V S^-1 V^T.
"""
from fractions import Fraction as F
from itertools import combinations, product
pc = lambda x: bin(x).count("1")
N = 16
H = [[(-1) ** pc(x & y) for x in range(N)] for y in range(N)]
def span(gens):
    S = {0}
    for g in gens: S |= {s ^ g for s in S}
    return sorted(S)
def rank(M):
    M = [[F(v) for v in r] for r in M]; r = 0
    for c in range(len(M[0])):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]; pv = M[r][c]; M[r] = [v / pv for v in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
        if r == len(M): break
    return r
dot = lambda u, v: sum(a * b for a, b in zip(u, v))
def canon(v):
    f = next(c for c in v if c != 0)
    return tuple(c * (1 if f > 0 else -1) for c in v)

print("== A. N=16, three self-dual codes ==")
codes = {"12|34": [0b1100, 0b0011], "13|24": [0b1010, 0b0101], "14|23": [0b1001, 0b0110]}
atoms = {}                         # name -> list of canonical atoms
for name, gens in codes.items():
    C = span(gens); reps = []; seen = set()
    for a in range(16):
        if a not in seen: reps.append(a); seen |= {a ^ c for c in C}
    L = []
    for a in reps:
        for b in reps:
            L.append(canon([((-1) ** pc(b & x) if (x ^ a) in C else 0) for x in range(16)]))
    assert len(set(L)) == 16 and rank(L) == 16
    atoms[name] = L
allat = [g for L in atoms.values() for g in L]
print("atoms:", len(allat), "distinct:", len(set(allat)), " rank of all 48:", rank(allat))
idx = {g: i for i, g in enumerate(allat)}
# H as a signed permutation of the 48 atoms
fixed = 0; perm = {}
for g in allat:
    Hg = [dot(H[y], g) for y in range(16)]
    assert all(v % 4 == 0 for v in Hg)
    t = canon([v // 4 for v in Hg]); assert t in idx
    sgn = 1 if [v // 4 for v in Hg] == list(t) else -1
    perm[idx[g]] = (idx[t], sgn)
    fixed += (t == g)
print("H maps every atom to +-4 x an atom of the SAME code:", all(perm[i][0] // 16 == i // 16 for i in perm),
      " atoms fixed up to sign:", fixed, " transposed pairs:", (48 - fixed) // 2,
      " (+4 eigen-atoms: %d, -4: %d)" % (sum(1 for i in perm if perm[i] == (i, 1)), sum(1 for i in perm if perm[i] == (i, -1))))
# transfer matrices
names = list(codes)
for i, j in ((0, 1), (0, 2), (1, 2)):
    T = [[dot(g, h) for h in atoms[names[j]]] for g in atoms[names[i]]]   # <g,h>; coefficient is <g,h>/4
    nnz = sorted(set(sum(1 for v in r if v) for r in T)); vals = sorted(set(v for r in T for v in r))
    # block structure: connected components of the bipartite non-zero pattern
    comp = list(range(32))
    def find(a):
        while comp[a] != a: a = comp[a]
        return a
    for a in range(16):
        for b in range(16):
            if T[a][b]: comp[find(a)] = find(16 + b)
    blocks = {}
    for a in range(32): blocks.setdefault(find(a), []).append(a)
    print("transfer %s -> %s: non-zeros per row %s, inner products %s, blocks: %s" % (
        names[i], names[j], nnz, vals, sorted(len(v) // 2 for v in blocks.values())))
# orthogonality structure of the 48 atoms: components of the non-orthogonality graph
adj = [[dot(g, h) != 0 for h in allat] for g in allat]
comp = list(range(48))
def find(a):
    while comp[a] != a: a = comp[a]
    return a
for a in range(48):
    for b in range(48):
        if adj[a][b]: comp[find(a)] = find(b)
blk = {}
for a in range(48): blk.setdefault(find(a), []).append(a)
print("48 atoms split into mutually orthogonal families of sizes", sorted(len(v) for v in blk.values()),
      " ranks", sorted(rank([allat[i] for i in v]) for v in blk.values()))
for v in blk.values():
    G = sorted(set(abs(dot(allat[a], allat[b])) for a in v for b in v if a != b))
    hb = sorted(set(find(perm[a][0]) == find(a) for a in v))
    print("   family of %d atoms: |inner products| %s (norm 4), codes per family %s, H keeps the family: %s" % (
        len(v), G, sorted(set(a // 16 for a in v)), hb))
# orthogonal bases made of atoms (hybrid bases), and those closed under H
import sys
sys.setrecursionlimit(10000)
orth = [[dot(g, h) == 0 for h in allat] for g in allat]
count = [0, 0]
def rec(chosen, cand):
    if len(chosen) == 16:
        count[0] += 1
        S = set(chosen)
        if all(perm[i][0] in S for i in S): count[1] += 1
        return
    if len(chosen) + len(cand) < 16: return
    for t, c in enumerate(cand):
        rec(chosen + [c], [d for d in cand[t + 1:] if orth[c][d]])
rec([], list(range(48)))
print("orthogonal bases of 16 atoms taken from the 48: %d (pure: 3); closed under H: %d" % tuple(count))

print("== B. Lagrangians of the phase space of 4 bits ==")
k = 4
def apply(gen, v):               # v = (x<<k)|z
    x, z = v >> k, v & (N - 1)
    t, a, b = gen
    if t == "h":
        xa, za = (x >> a) & 1, (z >> a) & 1
        x = (x & ~(1 << a)) | (za << a); z = (z & ~(1 << a)) | (xa << a)
    elif t == "s":
        z ^= ((x >> a) & 1) << a
    else:                         # cnot a -> b
        x ^= ((x >> a) & 1) << b; z ^= ((z >> b) & 1) << a
    return (x << k) | z
gens = [("h", a, 0) for a in range(k)] + [("s", a, 0) for a in range(k)] + [("c", a, b) for a in range(k) for b in range(k) if a != b]
LZ = frozenset(range(N))
seen = {LZ}; front = [LZ]
while front:
    nf = []
    for L in front:
        for g in gens:
            M = frozenset(apply(g, v) for v in L)
            if M not in seen: seen.add(M); nf.append(M)
    front = nf
print("Lagrangians:", len(seen))
swap = lambda v: ((v & (N - 1)) << k) | (v >> k)
real = lambda L: all(pc((v >> k) & v) % 2 == 0 for v in L)
inv = [L for L in seen if frozenset(swap(v) for v in L) == L]
import math
hist = {}
for L in inv:
    d = int(math.log2(len(L & LZ)))
    css = len(L & LZ) * len(L & frozenset(v << k for v in range(N))) == N
    hist[(d, real(L), css)] = hist.get((d, real(L), css), 0) + 1
print("kept by the swap X<->Z (H is monomial in that basis):", len(inv), " of which real:", sum(1 for L in inv if real(L)),
      " (all real Lagrangians: %d)" % sum(1 for L in seen if real(L)))
for key in sorted(hist): print("   dim(L meet standard) = %d, real = %s, code-type (C+C) = %s : %d" % (key + (hist[key],)))
print("   => distance from the standard basis (4 - dim) of any basis in which H is monomial: min %d" % (4 - max(d for d, _, _ in hist)))

print("== C. reflections ==")
u = [1, 1, 1, -1]
H4p = [[(2 if i == j else 0) - u[i] * u[j] for j in range(4)] for i in range(4)]
print("H4' = 2I - u u^T rows:", H4p, " is Hadamard:", all(sum(H4p[i][t] * H4p[j][t] for t in range(4)) == (4 if i == j else 0) for i in range(4) for j in range(4)))
# 8 reflection vectors of Householder x Householder: e_i (x) u and u (x) e_j
V = []
for i in range(4): V.append([(u[q] if p == i else 0) for p in range(4) for q in range(4)])
for j in range(4): V.append([(u[p] if q == j else 0) for p in range(4) for q in range(4)])
I16 = [[F(int(i == j)) for j in range(16)] for i in range(16)]
def mm(A, B): return [[sum(A[i][t] * B[t][j] for t in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def refl(v):
    n2 = dot(v, v); return [[I16[i][j] - F(2 * v[i] * v[j], n2) for j in range(16)] for i in range(16)]
P = I16
for v in V: P = mm(P, refl(v))
tgt = [[F(H4p[p][pp] * H4p[q][qq], 4) for pp in range(4) for qq in range(4)] for p in range(4) for q in range(4)]
print("product of the 8 support-4 reflections == (H4' x H4')/4:", P == tgt, " rank of the 8 vectors:", rank(V),
      " rank(I - g):", rank([[I16[i][j] - tgt[i][j] for j in range(16)] for i in range(16)]))
# compact form: g = I - V S^-1 V^T, S = upper triangle of the Gram matrix with the diagonal halved
m = len(V); G = [[dot(V[a], V[b]) for b in range(m)] for a in range(m)]
S = [[F(G[a][b]) if a < b else (F(G[a][a], 2) if a == b else F(0)) for b in range(m)] for a in range(m)]
# invert upper-triangular S
Sinv = [[F(0)] * m for _ in range(m)]
for c in range(m):
    for r in range(c, -1, -1):
        rhs = F(int(r == c)) - sum(S[r][t] * Sinv[t][c] for t in range(r + 1, m))
        Sinv[r][c] = rhs / S[r][r]
Vt = [list(r) for r in zip(*V)]            # 16 x 8
W = mm(mm(Vt, Sinv), V)
print("g == I - V S^-1 V^T (S = half-Gram, upper triangular):", [[I16[i][j] - W[i][j] for j in range(16)] for i in range(16)] == tgt,
      " non-zeros: V %d, S %d" % (sum(1 for r in V for x in r if x), sum(1 for r in S for x in r if x)))
print("Gram of the 8 vectors, distinct off-diagonal values:", sorted(set(G[a][b] for a in range(m) for b in range(m) if a != b)))
