# z-2: own check of x-4 lemma D.  Exact: ranks over the rationals by fraction-free elimination on whole numbers
# (N <= 64), and ranks modulo a prime only where a LOWER bound on the rational rank is wanted (rank mod p <= rank over Q).
import random, sys, itertools
from fractions import Fraction
random.seed(20261011)
P = (1 << 61) - 1

def rank_mod(rows, p=P):
    rows = [[v % p for v in r] for r in rows]
    rk = 0; ncol = len(rows[0]) if rows else 0
    for c in range(ncol):
        piv = None
        for i in range(rk, len(rows)):
            if rows[i][c]:
                piv = i; break
        if piv is None: continue
        rows[rk], rows[piv] = rows[piv], rows[rk]
        inv = pow(rows[rk][c], p - 2, p)
        rr = rows[rk]
        for i in range(rk + 1, len(rows)):
            f = rows[i][c] * inv % p
            if f:
                ri = rows[i]
                rows[i] = [(a - f * b) % p for a, b in zip(ri, rr)]
        rk += 1
        if rk == len(rows): break
    return rk

def rank_exact(rows):
    rows = [[Fraction(v) for v in r] for r in rows]
    rk = 0; ncol = len(rows[0]) if rows else 0
    for c in range(ncol):
        piv = None
        for i in range(rk, len(rows)):
            if rows[i][c] != 0:
                piv = i; break
        if piv is None: continue
        rows[rk], rows[piv] = rows[piv], rows[rk]
        rr = rows[rk]
        for i in range(rk + 1, len(rows)):
            if rows[i][c] != 0:
                f = rows[i][c] / rr[c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rr)]
        rk += 1
        if rk == len(rows): break
    return rk

def dot(x, y): return bin(x & y).count('1') & 1

print("== (a) least rank of the block 'rows in a hyperplane, columns outside it' of H, all hyperplanes ==")
print("   (rank modulo 2^61-1: a lower bound for the rational rank; H has entries +-1)")
for k in range(3, 8):
    N = 1 << k
    H = [[1 - 2 * dot(x, y) for y in range(N)] for x in range(N)]
    seen = {}
    for a in range(1, N):
        rows = [x for x in range(N) if dot(a, x) == 0]
        cols = [y for y in range(N) if dot(a, y) == 1]
        r = rank_mod([[H[x][y] for y in cols] for x in rows])
        seen[r] = seen.get(r, 0) + 1
    print(f"k={k} N={N}: ranks found {sorted(seen.items())}  N/4={N//4} N/2={N//2}")

print("== (b) ANY N/2 x N/2 block of H (rows and columns chosen freely): rank >= N/4 by the singular-value count; samples ==")
for k in range(3, 8):
    N = 1 << k
    H = [[1 - 2 * dot(x, y) for y in range(N)] for x in range(N)]
    least = N
    trials = 300 if k <= 5 else 40
    for _ in range(trials):
        rows = random.sample(range(N), N // 2); cols = random.sample(range(N), N // 2)
        least = min(least, rank_mod([[H[x][y] for y in cols] for x in rows]))
    # structured adversary: rows a subgroup (hyperplane), columns a union of pairs {y, y+a} -> duplicate columns
    a = 1
    rows = [x for x in range(N) if dot(a, x) == 0]
    cols = []
    for y in range(N):
        if len(cols) >= N // 2: break
        if y not in cols and (y ^ a) not in cols: cols += [y, y ^ a]
    adv = rank_mod([[H[x][y] for y in cols] for x in rows])
    print(f"k={k} N={N}: least rank over {trials} random blocks {least}; adversarial block (duplicated columns) rank {adv}; N/4={N//4}")

def rand_flag(k):
    # a random flag = a random invertible bit matrix; M_j = span of its first j columns
    while True:
        b = [random.randrange(1, 1 << k) for _ in range(k)]
        span = {0}; ok = True
        for v in b:
            if v in span: ok = False; break
            span |= {s ^ v for s in span}
        if ok: return b

def span_of(vs):
    s = {0}
    for v in vs:
        if v not in s: s |= {t ^ v for t in s}
    return s

def flag_kernel(k, basis, c):
    N = 1 << k
    f = [0] * N
    lvl = [None] * N
    s = {0}; lvl[0] = 0
    for j, v in enumerate(basis, 1):
        new = {t ^ v for t in s} - s
        for u in new: lvl[u] = j
        s |= new
    for u in range(N):
        f[u] = sum(c[j] for j in range(lvl[u], k + 1))
    return [[f[x ^ y] for y in range(N)] for x in range(N)], lvl

def matmul(A, B):
    n = len(A); m = len(B[0]); Bt = list(zip(*B))
    return [[sum(a * b for a, b in zip(row, col)) for col in Bt] for row in A]

print("== (c) the count itself: random products D0 K1 D1 ... Kr Dr of flag kernels (random flags, weights, diagonals) ==")
print("   for every hyperplane containing W = M^1_t + ... + M^r_t: exact rank of the block against r N / 2^(t+1)")
for (k, r) in [(4, 1), (4, 2), (5, 2), (5, 3), (6, 2), (6, 3), (6, 4)]:
    N = 1 << k
    worst = None
    for trial in range(3):
        flags = [rand_flag(k) for _ in range(r)]
        Ks = []
        for b in flags:
            c = [random.randint(-5, 5) or 1 for _ in range(k + 1)]
            Ks.append(flag_kernel(k, b, c)[0])
        Ds = [[random.choice([-3, -2, -1, 1, 2, 3]) for _ in range(N)] for _ in range(r + 1)]
        M = [[Ds[0][x] if x == y else 0 for y in range(N)] for x in range(N)]
        for i in range(r):
            M = matmul(M, Ks[i])
            M = [[M[x][y] * Ds[i + 1][y] for y in range(N)] for x in range(N)]
        for t in range(0, k):
            if r * t >= k: break
            W = span_of([v for b in flags for v in b[:t]])
            # hyperplanes a^perp containing W
            for a in range(1, N):
                if any(dot(a, w) for w in W): continue
                rows = [x for x in range(N) if dot(a, x) == 0]
                cols = [y for y in range(N) if dot(a, y) == 1]
                blk = [[M[x][y] for y in cols] for x in rows]
                rk = rank_exact(blk) if N <= 32 else rank_mod(blk)
                bound = r * N // (1 << (t + 1))
                tight = N // (1 << (t + 1))
                rec = (rk, bound, t)
                if rk > bound:
                    print("VIOLATION", k, r, t, rk, bound); sys.exit(1)
                if worst is None or rk * worst[1] > worst[0] * bound: worst = rec
    print(f"k={k} r={r}: no violation; closest case rank {worst[0]} against bound {worst[1]} at t={worst[2]}"
          + ("  (exact fractions)" if N <= 32 else "  (rank modulo 2^61-1; whole-number entries, so this can only UNDER-count: a check, not a proof)"))

print("== (d) the bound as a table: least r with r >= 2^(ceil(k/r)-2) (lemma D alone), against k/2 and k/log2 k ==")
import math
def rmin(k):
    r = 1
    while True:
        t = -(-k // r) - 1          # largest t with r t < k
        if r >= 2 ** (t - 1): return r
        r += 1
for k in [4, 6, 8, 10, 12, 16, 24, 32, 64, 256, 1024, 4096, 65536, 1 << 20]:
    r = rmin(k)
    print(f"k={k}: r >= {r};  k/2 = {k//2};  k/log2 k = {k/math.log2(k):.1f};  ratio r log2(k)/k = {r*math.log2(k)/k:.3f}")
