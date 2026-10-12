# x-5-weightedz / ident.py : exact checks of the identities used in the report. Whole numbers and fractions only.
#  1. U = L - Z L Z^-1   (U = "add one element", L = diagonal of the set sizes, Z = subset sums).  Checked as U Z = L Z - Z L.
#  2. The cube's neighbour sum A = H L' H / N with L' = diagonal of k - 2|S|.
#  3. The potential: gates of ANY tree of couplings, each weight block of size m priced m(m-1), = sum over the final strings of
#     (d+1) d (d-1) / 3   (d + 1 = length of the string).  Checked for the tower (one coordinate at a time), the balanced tree and
#     a lopsided tree, from the multiplicities.
#  4. The volume budget of the tower (s-cross hybrid 3's ledger): per full 2 x 2 block [[1, 1], [j, -(d-j+1)]] the two gates are
#     u + v (budget 1) and (j u - (d-j+1) v)/g (budget log2((d+1)/g), g = gcd(j, d-j+1)).  Per point, against k.
#  5. H = N V^T D^-1 V for every V with V H V^T = D diagonal; and the covering count: sum over rows of s(s-1)/2 >= N(N-1)/2.
#     Checked on V = Moebius (inverse subset sums) and on V = the tower basis (rows = dual vectors are not needed: V rows = any
#     H-orthogonal basis; the tower strings are H-orthogonal only string against string, so they are first diagonalised inside
#     each string by the Pascal block).
import sys
from fractions import Fraction as Fr
from math import comb, log2, gcd
sys.path.insert(0, ".")

def zeta(v, k):
    v = v[:]
    for j in range(k):
        h = 1 << j
        for x in range(len(v)):
            if x & h: v[x] += v[x ^ h]
    return v
def wht(v, k):
    v = v[:]
    for j in range(k):
        h = 1 << j
        for x in range(len(v)):
            if not x & h: a, b = v[x], v[x | h]; v[x], v[x | h] = a + b, a - b
    return v
def up(v, k):
    o = [0] * len(v)
    for T, c in enumerate(v):
        if c:
            for j in range(k):
                if not (T >> j) & 1: o[T | (1 << j)] += c
    return o
pc = lambda x: bin(x).count("1")

print("== 1, 2: U Z = L Z - Z L and A = H L' H / N, on every basis vector ==")
for k in range(1, 9):
    N = 1 << k; ok1 = ok2 = True
    for T in range(N):
        e = [0] * N; e[T] = 1
        z = zeta(e, k)
        lhs = up(z, k)
        rhs = [pc(S) * z[S] - pc(T) * z[S] for S in range(N)]
        ok1 &= (lhs == rhs)
        h = wht(e, k); h = [(k - 2 * pc(S)) * h[S] for S in range(N)]; h = wht(h, k)
        nb = [0] * N
        for j in range(k): nb[T ^ (1 << j)] += 1
        ok2 &= (h == [N * x for x in nb])
    print("  k=%d  U Z = L Z - Z L: %s    H L' H = N * (neighbour sum): %s" % (k, ok1, ok2))

print("== 3: the potential (d+1) d (d-1)/3 ==")
def couple(ma, mb):
    c = 0; new = {}
    for a, x in ma.items():
        for b, y in mb.items():
            g = 0
            for w in range(a + b + 1):
                m = min(w, a, b, a + b - w) + 1
                g += m * (m - 1)
            c += x * y * g
            for d in range(abs(a - b), a + b + 1, 2): new[d] = new.get(d, 0) + x * y
    return c, new
def dim(m): return sum((d + 1) * x for d, x in m.items())
def tree(shape):
    # shape: 1 (a coordinate) or a pair of shapes. returns (gates, multiplicities)
    if shape == 1: return 0, {1: 1}
    ga, ma = tree(shape[0]); gb, mb = tree(shape[1])
    c, new = couple(ma, mb)
    return ga * dim(mb) + gb * dim(ma) + c, new
def tower_shape(k):
    s = 1
    for _ in range(k - 1): s = (s, 1)
    return s
def balanced(k):
    if k == 1: return 1
    return (balanced(k // 2), balanced(k - k // 2))
def lopsided(k):
    if k <= 2: return balanced(k)
    a = max(1, k // 3)
    return (lopsided(a), lopsided(k - a))
for k in (2, 3, 4, 5, 6, 7, 8, 12, 16, 24):
    N = 1 << k
    res = []
    for name, sh in (("tower", tower_shape(k)), ("balanced", balanced(k)), ("lopsided", lopsided(k))):
        g, m = tree(sh); res.append(g)
    pot = sum(x * (d + 1) * d * (d - 1) // 3 for d, x in m.items())
    avd = Fr(sum(x * (d + 1) * d for d, x in m.items()), N)
    print("  k=%2d  tower %d  balanced %d  lopsided %d  potential %d  all equal: %s   N (k - E[d]) = %s (E[d] = %.4f)" % (
        k, res[0], res[1], res[2], pot, len(set(res + [pot])) == 1, N * k - avd * N, float(avd)))

print("== 4: volume budget of the tower, per point ==")
mult = {1: 1}; tot = 0.0; gates = Fr(0); detlog = 0.0
for i in range(2, 257):
    b = 0.0; g = 0; dl = 0.0
    for d, x in mult.items():
        for j in range(1, d + 1):
            gg = gcd(j, d - j + 1)
            b += x * (1 + log2((d + 1) / gg)); g += 2 * x; dl += x * log2(d + 1)
    new = {}
    for d, x in mult.items():
        new[d + 1] = new.get(d + 1, 0) + x
        if d >= 1: new[d - 1] = new.get(d - 1, 0) + x
    mult = new
    tot += b / (1 << i); gates += Fr(g, 1 << i); detlog += dl / (1 << i)
    if i in (4, 8, 16, 32, 64, 128, 256):
        print("  k=%3d  gates/N %8.3f  budget/N %9.3f  budget per gate %.3f  log2|det of the integer basis|/N %9.3f  (the transform needs k/2 = %.1f;  (k/4) log2 k = %.1f)" % (
            i, float(gates), tot, tot / float(gates), detlog, i / 2, i / 4 * log2(i)))

print("== 5: H = N V^T D^-1 V for an H-orthogonal basis V, and the covering count ==")
for k in range(1, 7):
    N = 1 << k
    # V = Moebius: row S = sum over T inside S of (-1)^(|S|-|T|) e_T
    V = [[(-1) ** (pc(S) - pc(T)) if T & S == T else 0 for T in range(N)] for S in range(N)]
    HV = [wht(r, k) for r in V]                       # rows: H v_i
    G = [[sum(a * b for a, b in zip(HV[i], V[j])) for j in range(N)] for i in range(N)]
    diag = all(G[i][j] == 0 for i in range(N) for j in range(N) if i != j)
    d = [G[i][i] for i in range(N)]
    M = [[sum(Fr(V[i][S] * V[i][T], d[i]) for i in range(N)) * N for T in range(N)] for S in range(N)]
    okH = all(M[S][T] == (-1) ** pc(S & T) for S in range(N) for T in range(N))
    cover = sum(sum(1 for x in r if x) * (sum(1 for x in r if x) - 1) // 2 for r in V)
    print("  k=%d  Moebius rows: V H V^T diagonal %s, diagonal = (-2)^|S| %s, N V^T D^-1 V = H %s, covering %d >= %d" % (
        k, diag, all(d[S] == (-2) ** pc(S) for S in range(N)), okH, cover, N * (N - 1) // 2))
