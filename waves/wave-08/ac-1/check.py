#!/usr/bin/env python3
"""check.py [ac-1]  EXACT (whole numbers and fractions).  Skeptic's own check of ab-6's leak lemma.
Part A: the numbers of the lemma for K = 4 .. 64 from orbit counts (no sum over the group), cross-checked by a sum over the
        group at K = 4, 8, 16.
Part B: K = 4, unreduced model (4-vectors, 16-entry table, permutation boxes):  B1 rank of the target differences;
        B2 the triangle; B3 a 7-call program of my own, replayed on all six maps; B4 step (2) of the lemma tested on that
        program (the rho-part of the calls' outputs for the sign datum is killed by the output map); B5 controls at 6 calls."""
import itertools, sys, random
from fractions import Fraction as Fr

def lin_maps(k):
    n = 1 << k; out = []
    for cols in itertools.product(range(1, n), repeat=k):
        img = [0] * n
        for x in range(n):
            v = 0
            for j in range(k):
                if x >> j & 1: v ^= cols[j]
            img[x] = v
        if len(set(img)) == n: out.append(tuple(img))
    return out

def orbits(k, m):
    """number of orbits of GL(k,2) on m-tuples of addresses; generators x_i ^= x_j (they generate GL(k,2))."""
    n = 1 << k
    gens = [[x ^ (((x >> j) & 1) << i) for x in range(n)] for i in range(k) for j in range(k) if i != j]
    N = n ** m; parent = list(range(N))
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]; a = parent[a]
        return a
    for idx in range(N):
        t = []; v = idx
        for _ in range(m): t.append(v % n); v //= n
        for img in gens:
            j = 0
            for c in reversed(t): j = j * n + img[c]
            ra, rb = find(idx), find(j)
            if ra != rb: parent[ra] = rb
    return sum(1 for a in range(N) if find(a) == a)

ceil = lambda a, b: -(-a // b)
print("PART A.  pi = number of fixed addresses, chi = pi - 2 (character of V).  <pi^m, 1> = orbits on m-tuples.")
kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 5
for k in range(2, kmax + 1):
    K = 1 << k; d = K - 2
    o1, o2, o3 = orbits(k, 1), orbits(k, 2), orbits(k, 3)
    chichi = o2 - 4 * o1 + 4; mV = o3 - 6 * o2 + 12 * o1 - 8
    rest = d * d - 1 - mV * d; c = 4 + mV
    ab6 = c + ceil(rest + d * ceil(rest, d), d); mine = c + 2 * ceil(rest, d)
    line = "K = %2d: orbits on 1-, 2-, 3-tuples %d %d %d; <chi,chi> = %d; copies of V in V x V = %d; copies in the table c = %d; Rest = %d; " \
           "ab-6 formula %d; c + 2 ceil(Rest/d) = %d; 2K - 2 = %d; textbook %d; telescoping %d" % (K, o1, o2, o3, chichi, mV, c, rest, ab6, mine, 2 * K - 2, 2 * K, K + K // 2)
    if k <= 4:
        Gp = lin_maps(k); s2 = s3 = 0
        for img in Gp:
            ch = sum(1 for x in range(K) if img[x] == x) - 2; s2 += ch * ch; s3 += ch ** 3
        assert s2 == len(Gp) * chichi and s3 == len(Gp) * mV
        line += "; group sum over %d maps agrees" % len(Gp)
    print(line, flush=True)

# ---------------- exact linear algebra
def rref(M):
    M = [row[:] for row in M]; piv = []; r = 0
    ncol = len(M[0]) if M else 0
    for c in range(ncol):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]; inv = Fr(1) / M[r][c]; M[r] = [v * inv for v in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        piv.append(c); r += 1
        if r == len(M): break
    return M, piv
def rank(M): return len(rref([[Fr(v) for v in row] for row in M])[1])
def solve(A, B):
    """X with A X = B (free unknowns 0), or None.  A: m x n, B: m x q."""
    m, n, q = len(A), len(A[0]), len(B[0])
    M, piv = rref([[Fr(v) for v in A[i]] + [Fr(v) for v in B[i]] for i in range(m)])
    if any(p >= n for p in piv): return None
    X = [[Fr(0)] * q for _ in range(n)]
    for r, p in enumerate(piv): X[p] = M[r][n:]
    return X
def mm(A, B): return [[sum(a * b for a, b in zip(row, col)) for col in zip(*B)] for row in A]
def tr(A): return [list(r) for r in zip(*A)]

print("\nPART B.  K = 4, the six address maps, unreduced model.")
K = 4; Gp = lin_maps(2); assert len(Gp) == 6
def sgn(img):
    p = [img[1], img[2], img[3]]; s = 1
    for i in range(3):
        for j in range(i + 1, 3):
            if p[i] > p[j]: s = -s
    return s
def Pm(img): return [[1 if img[x] == y else 0 for x in range(K)] for y in range(K)]          # P e_x = e_{g x}
def Tm(img):
    T = [[0] * 16 for _ in range(16)]
    for x in range(4):
        for y in range(4): T[img[x] * 4 + img[y]][x * 4 + y] = 1
    return T
P = {g: Pm(g) for g in Gp}; T = {g: Tm(g) for g in Gp}
ident = tuple(range(4)); mul = lambda g, h: tuple(g[h[x]] for x in range(4)); inv = lambda g: tuple(g.index(x) for x in range(4))
# B1
rows = []
for g in Gp:
    for i in range(16): rows.append([T[g][i][j] - (1 if i == j else 0) for j in range(16)])
print("B1  rank of all (T(g) - 1), that is the number tau of output numbers that depend on g: %d (claimed 11 = 5 x 2 + 1)" % rank(rows))
# B2  V = sum-zero plane on addresses 1,2,3, basis e1 - e3, e2 - e3
def rho(g):
    cols = []
    for (i, j) in ((1, 3), (2, 3)):
        v = {g[i]: 1, g[j]: -1}; cols.append([v.get(1, 0), v.get(2, 0)])     # coordinates in the basis: coefficient of e1, e2
        assert v.get(3, 0) == -(v.get(1, 0) + v.get(2, 0))
    return tr(cols)
cyc = next(g for g in Gp if sgn(g) == 1 and g != ident); c2 = mul(cyc, cyc)
def tri(a):
    u = [sum(rho(cyc)[i][j] * a[j] for j in range(2)) - a[i] for i in range(2)]
    w = [sum(rho(c2)[i][j] * a[j] for j in range(2)) - a[i] for i in range(2)]
    return u[0] * w[1] - u[1] * w[0]
q11, q22, qs = tri([1, 0]), tri([0, 1]), tri([1, 1]); q12 = qs - q11 - q22
print("B2  det[(rho(c) - 1) a, (rho(c^2) - 1) a] = %d a1^2 + %d a1 a2 + %d a2^2 ; discriminant %d (negative = never 0 for a real a other than 0)"
      % (q11, q12, q22, q12 * q12 - 4 * q11 * q22))
assert tri([2, 5]) == q11 * 4 + q12 * 10 + q22 * 25
# B3 a 7-call program
rng = random.Random(20261011)
def equivariant():
    E0 = [[rng.randint(-3, 3) for _ in range(16)] for _ in range(4)]; E = [[0] * 16 for _ in range(4)]
    for g in Gp:
        X = mm(mm(P[inv(g)], E0), T[g]); E = [[a + b for a, b in zip(r1, r2)] for r1, r2 in zip(E, X)]
    for g in Gp: assert mm(E, T[g]) == mm(P[g], E)
    return E
tau = [0] * 16
for (x, y) in ((1, 2), (2, 3), (3, 1)): tau[x * 4 + y] = 1; tau[y * 4 + x] = -1
for g in Gp: assert mm([tau], T[g])[0] == [sgn(g) * v for v in tau]
def sign_pair(a, p2):
    """M (4x4), b, p1, q0 with  p2.P_g (M P_g a + b) + p1.P_g a + q0 = sign(g)  for all six g; linear in (M, b, p1, q0)."""
    A = []; B = []
    for g in Gp:
        gi = inv(g); row = [p2[g[u]] * a[gi[v]] for u in range(4) for v in range(4)] + [p2[g[u]] for u in range(4)] + [a[gi[w]] for w in range(4)] + [1]
        A.append(row); B.append([sgn(g)])
    X = solve(A, B)
    if X is None: return None
    X = [x[0] for x in X]
    return [X[4 * u:4 * u + 4] for u in range(4)], X[16:20], X[20:24], X[24]
def calls_matrix(prog, g):
    """prog: list of (L (4x16), {i: M_ji (4x4)}).  Returns the stacked 4r x 16 matrix of the calls' outputs as functions of x."""
    C = []
    for (L, Ms) in prog:
        W = [row[:] for row in L]
        for i, Mji in Ms.items():
            X = mm(Mji, C[i]); W = [[a + b for a, b in zip(r1, r2)] for r1, r2 in zip(W, X)]
        C.append(mm(P[g], W))
    return [row for blk in C for row in blk]
def glue_out(prog):
    """exact solve for the output glue [Pout Q]; returns (Pout, Q) or None."""
    r = len(prog); D = {g: calls_matrix(prog, g) for g in Gp}
    A = []; B = []
    for g in Gp:
        for col in range(16):
            A.append([D[g][i][col] for i in range(4 * r)] + [1 if j == col else 0 for j in range(16)])
            B.append([T[g][i][col] for i in range(16)])
    X = solve(A, B)
    if X is None: return None
    W = tr(X); return [row[:4 * r] for row in W], [row[4 * r:] for row in W], D
a = [0, 1, 2, 5]; p2 = [0, 3, -1, 1]
sp = sign_pair(a, p2); assert sp is not None, "sign pair not solvable with this a, p2"
Msg, b, p1, q0 = sp
for g in Gp:
    Pa = [a[inv(g)[w]] for w in range(4)]; inner = [sum(Msg[u][v] * Pa[v] for v in range(4)) + b[u] for u in range(4)]
    assert sum(p2[g[u]] * inner[u] for u in range(4)) + sum(p1[w] * Pa[w] for w in range(4)) + q0 == sgn(g)
print("B3  nested pair for the sign: p2.P_g (M P_g a + b) + p1.P_g a + q0 = sign(g) holds for all six maps (exact)")
prog = [(equivariant(), {}) for _ in range(5)]
prog.append(([[a[u] * tau[j] for j in range(16)] for u in range(4)], {}))
prog.append(([[b[u] * tau[j] for j in range(16)] for u in range(4)], {5: Msg}))
res = glue_out(prog); assert res is not None, "7-call program: no output glue"
Pout, Q, D = res; ok = 0
for g in Gp:
    out = [[x + y for x, y in zip(r1, r2)] for r1, r2 in zip(mm(Pout, D[g]), Q)]
    assert out == [[Fr(v) for v in row] for row in T[g]]; ok += 16
print("B3  my own 7-call program: output = P_g X P_g^T on all 6 maps x 16 unit tables = %d cases, exact.  r(4) <= 7." % ok)
# B4  step (2): the rho-part of the calls' outputs for the sign datum is in the kernel of the output map
chi = {g: sum(1 for x in range(4) if g[x] == x) - 2 for g in Gp}
tvec = [[Fr(v)] for v in tau]                                    # the datum t (the sign vector of the table), a 16 x 1 column
f = {g: [row[0] for row in mm(D[g], tvec)] for g in Gp}          # calls' outputs for t, a 28-vector for each g
kill = []
for g in Gp:
    e = [Fr(0)] * 28
    for h in Gp:
        fh = f[mul(g, h)]; e = [x + chi[h] * y for x, y in zip(e, fh)]
    kill.append([x * Fr(2, 6) for x in e])
pk = mm(Pout, tr(kill))
print("B4  rho-part of the calls' outputs for the sign datum, over the six maps: dimension %d (lemma: at least d x nu = 2); "
      "output map applied to it: %s" % (rank(kill), "all zero" if all(v == 0 for row in pk for v in row) else "NOT zero"))
rowsP = [r_ for r_ in Pout if any(v != 0 for v in r_)]
print("    rank of the output map on the 28 call outputs: %d" % rank(Pout))
# also the cruder fact used by the triangle: outputs for t at the three even maps
ev = [g for g in Gp if sgn(g) == 1]; diffs = [[x - y for x, y in zip(f[g], f[ident])] for g in ev if g != ident]
print("    7-call program: the differences of the calls' outputs for t between the even maps span %d dimensions, and the output map kills them: %s"
      % (rank(diffs), all(v == 0 for row in mm(Pout, tr(diffs)) for v in row)))
# B5 controls at 6 calls (these say only that THESE programs fail; the proof is B1 + B2)
fails = 0; trials = 0
for trial in range(12):
    pr = [(equivariant(), {}) for _ in range(5)]
    Ms = {i: [[rng.randint(-2, 2) for _ in range(4)] for _ in range(4)] for i in range(5)}
    pr.append(([[rng.randint(-2, 2) for _ in range(16)] for _ in range(4)], Ms)); trials += 1
    if glue_out(pr) is None: fails += 1
print("B5  control: 5 one-call triples + ONE more call with random whole-number glue: %d of %d have no output glue (expected: all)" % (fails, trials))
pr = prog[:6]; print("    control: my program without its 7th call: output glue exists: %s" % (glue_out(pr) is not None))
