# g-4-zetalead / verify.py : exact checks for "the published exponent carries to the subset-sum (zeta) and Moebius transforms".
# Exact rationals (fractions.Fraction) everywhere.  Run:  python3 -B verify.py [kmax]
#
# Notation.  N = 2^k.  H = [[1,1],[1,-1]], Z = [[1,0],[1,1]] (subset sums), M = Z^-1 = [[1,0],[-1,1]] (Moebius),
# X = [[0,1],[1,0]] (complement of a bit), D(a,b) = diag(a,b); a letter with index k is the k-th Kronecker power.
#
# 1. the 2 x 2 identities (this is the whole proof: the rule (AB) kron (AB) = (A kron A)(B kron B) carries them to every k)
# 2. the same identities as full N x N matrix identities, k = 1..kmax (redundant with 1; done because the brief asks)
# 3. the one-parameter family of three-call words, and the member with no global factor
# 4. the same word run as a PROGRAM on vectors, with the operations counted in count (G) and count (O)
# 5. two calls cannot give Z, even with arbitrary (non-product) diagonals: checked by solving the equations at N = 2, 4
import sys
from fractions import Fraction as Fr
from itertools import product

kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 6

def mm(A, B):
    n, m, l = len(A), len(B), len(B[0])
    Bt = [[B[t][j] for t in range(m)] for j in range(l)]
    return [[sum(a * b for a, b in zip(row, col) if a and b) for col in Bt] for row in A]
def dg(*v): return [[Fr(v[i]) if i == j else Fr(0) for j in range(len(v))] for i in range(len(v))]
def kron(A, B): return [[a * b for a in ra for b in rb] for ra in A for rb in B]
def kpow(A, k):
    R = [[Fr(1)]]
    for _ in range(k): R = kron(R, A)
    return R
def word(*Ms):
    R = Ms[0]
    for Mx in Ms[1:]: R = mm(R, Mx)
    return R
def F(Mx): return [[Fr(x) for x in r] for r in Mx]
def T(A): return [list(r) for r in zip(*A)]

H = F([[1, 1], [1, -1]]); Z = F([[1, 0], [1, 1]]); Mo = F([[1, 0], [-1, 1]]); X = F([[0, 1], [1, 0]])

# the words.  Each is a list: diag, 'H', diag, 'H', ...
W_a0   = [(Fr(1, 4), Fr(1, 5)), (Fr(3, 2), Fr(-1, 2)), (2, 1), (1, Fr(5, 3))]          # a-0's word
W_unit = [(1, Fr(3, 5)), (1, Fr(-1, 2)), (1, Fr(1, 3)), (1, Fr(5, 4))]                  # mine: no global factor, every diagonal D(1, r)
W_moeb = [(1, Fr(-3, 5)), (1, Fr(-1, 2)), (1, Fr(1, 3)), (1, Fr(-5, 4))]                # Moebius = S Z S, S = D(1,-1) folded into the ends
W_zt   = [(1, Fr(5, 4)), (1, Fr(1, 3)), (1, Fr(-1, 2)), (1, Fr(3, 5))]                  # Z transpose (superset sums): the word reversed

def word3(ds, k):
    Hk = kpow(H, k)
    Ds = [kpow(dg(*d), k) for d in ds]
    return word(Ds[0], Hk, Ds[1], Hk, Ds[2], Hk, Ds[3])

print("== 1. 2 x 2 identities (exact) ==")
print("Z  = D(1/4,1/5) H D(3/2,-1/2) H D(2,1) H D(1,5/3)        :", word3(W_a0, 1) == Z)
print("Z  = D(1,3/5) H D(1,-1/2) H D(1,1/3) H D(1,5/4)           :", word3(W_unit, 1) == Z)
print("Z^-1 = D(1,-3/5) H D(1,-1/2) H D(1,1/3) H D(1,-5/4)       :", word3(W_moeb, 1) == Mo)
print("Z^T = D(1,5/4) H D(1,1/3) H D(1,-1/2) H D(1,3/5)          :", word3(W_zt, 1) == T(Z))
print("H  = Z D(1,-2) Z^T                                        :", word(Z, dg(1, -2), T(Z)) == H)
print("Z^T = X Z X                                               :", word(X, Z, X) == T(Z))
print("Z^-1 = D(1,-1) Z D(1,-1)                                  :", word(dg(1, -1), Z, dg(1, -1)) == Mo)
print("H  = Z^-1^T ... the Moebius form: H = D(1,-1) M D(1,2) M^T D(1,-1) :", word(dg(1, -1), Mo, dg(1, -2), T(Mo), dg(1, -1)) == H)

print("== 2. the same as N x N identities, k = 1..%d (exact) ==" % kmax)
for k in range(1, kmax + 1):
    N = 1 << k
    Hk, Zk, Xk = kpow(H, k), kpow(Z, k), kpow(X, k)
    ZTk = T(Zk)
    subset = all(Zk[S][Tt] == (1 if (Tt & S) == Tt else 0) for S in range(N) for Tt in range(N))
    moeb = [[(Fr(-1) ** bin(S ^ Tt).count("1") if (Tt & S) == Tt else Fr(0)) for Tt in range(N)] for S in range(N)]
    ident = [[Fr(int(i == j)) for j in range(N)] for i in range(N)]
    r = dict(
        Z_is_subset_sums=subset,
        moebius_is_inverse=(mm(Zk, moeb) == ident),
        a0_word=(word3(W_a0, k) == Zk),
        unit_word=(word3(W_unit, k) == Zk),
        moebius_word=(word3(W_moeb, k) == moeb),
        ZT_word=(word3(W_zt, k) == ZTk),
        H_from_Z=(word(Zk, kpow(dg(1, -2), k), ZTk) == Hk),
        ZT_is_XZX=(word(Xk, Zk, Xk) == ZTk),
    )
    print("k=%d N=%3d " % (k, N) + "  ".join("%s:%s" % kv for kv in r.items()))
    sys.stdout.flush()
    assert all(r.values())

print("== 3. the family: for p, q with 2 p q (p^2+q^2)(q^2-p^2) invertible ==")
print("   Z = D(1/(2pq), 1/(p^2+q^2)) H D((p+q)/2, (p-q)/2) H D(q, p) H D(1, (p^2+q^2)/(q^2-p^2))")
ok = True; n = 0
for p, q in product([Fr(a, b) for a in range(-6, 7) for b in (1, 2, 3, 5)], repeat=2):
    if p == 0 or q == 0 or p * p == q * q: continue
    w = [(1 / (2 * p * q), 1 / (p * p + q * q)), ((p + q) / 2, (p - q) / 2), (q, p), (1, (p * p + q * q) / (q * q - p * p))]
    ok &= word3(w, 1) == Z; n += 1
print("   %d rational pairs (p, q) tried at k = 1, all equal to Z: %s" % (n, ok))
# global factor when all four diagonals are normalised to D(1, r): sigma = (p+q)/(4p); sigma = 1 iff q = 3p
print("   normalised to four diagonals D(1, r): global factor ((p+q)/(4p))^k ; it is 1 exactly when q = 3p, which gives")
print("   D(1,3/5) H D(1,-1/2) H D(1,1/3) H D(1,5/4), checked above for k = 1..%d" % kmax)

print("== 4. the word run as a program; operations counted ==")
# count (O): one unit per addition or subtraction of two data values, one unit per multiplication of a data value by a constant
#            other than 1 (a multiplication by -1 is charged).  Constants and index work are not counted here.
# count (G): one unit per gate a*u + b*v; scalings are free, so the four diagonals cost nothing.
def fwht(x, cnt):
    x = list(x); n = len(x); h = 1
    while h < n:
        for i in range(0, n, 2 * h):
            for j in range(i, i + h):
                u, v = x[j], x[j + h]
                x[j], x[j + h] = u + v, u - v
                cnt["add"] += 2
        h *= 2
    return x
def scale(x, r, cnt):
    out = []
    for i, v in enumerate(x):
        c = r ** bin(i).count("1")
        if c != 1: cnt["mul"] += 1
        out.append(c * v)
    return out
def zeta_by_word(x, ds, cnt):
    y = scale(x, ds[3][1], cnt)
    y = fwht(y, cnt); y = scale(y, ds[2][1], cnt)
    y = fwht(y, cnt); y = scale(y, ds[1][1], cnt)
    y = fwht(y, cnt); y = scale(y, ds[0][1], cnt)
    return y
def yates(x, cnt, sign=1):
    x = list(x); n = len(x); h = 1
    while h < n:
        for i in range(n):
            if i & h:
                x[i] = x[i] + sign * x[i ^ h]; cnt["add"] += 1
        h *= 2
    return x
import random
random.seed(4)
print("   k    N   Yates adds = k 2^(k-1)   word: adds   muls   total (O)   = 3 k N + 4 (N-1)   total (G) = 3 k N   ratio (O)/Yates   outputs equal")
for k in range(1, max(kmax, 10) + 1):
    N = 1 << k
    x = [Fr(random.randint(-9, 9), random.randint(1, 7)) for _ in range(N)]
    c1 = dict(add=0, mul=0); c2 = dict(add=0, mul=0); c3 = dict(add=0, mul=0); c4 = dict(add=0, mul=0)
    y1 = yates(x, c1); y2 = zeta_by_word(x, W_unit, c2)
    m1 = yates(x, c3, sign=-1); m2 = zeta_by_word(x, W_moeb, c4)
    tot = c2["add"] + c2["mul"]
    print("  %2d %5d %10d %22d %6d %9d %14d %19d %14.3f     zeta:%s moebius:%s" % (
        k, N, c1["add"], c2["add"], c2["mul"], tot, 3 * k * N + 4 * (N - 1), 3 * k * N, tot / c1["add"], y1 == y2, m1 == m2))
    assert y1 == y2 and m1 == m2 and tot == 3 * k * N + 4 * (N - 1) and c1["add"] == k * N // 2

print("== 5. two calls cannot give Z, even with arbitrary diagonals ==")
# D1 H_N D2 H_N D3 with D's ANY invertible diagonals: H D2 H has entry f(x xor y) with f = H d2.  Z[0][y] = 0 for y != 0 forces
# f(y) = 0 for all y != 0, so H D2 H is a multiple of the identity and the product is diagonal: never Z for N >= 2.  [derived]
# machine form of the same statement at N = 2 and 4: for the product to have Z's zero pattern, f must vanish on {x xor y : y not inside x}
for k in (1, 2, 3, 4):
    N = 1 << k
    must_vanish = {S ^ Tt for S in range(N) for Tt in range(N) if (Tt & S) != Tt}
    print("   k=%d: f must vanish on %d of the %d non-zero addresses -> H D2 H is a multiple of the identity: %s" % (
        k, len(must_vanish), N - 1, must_vanish == set(range(1, N))))
print("done")
