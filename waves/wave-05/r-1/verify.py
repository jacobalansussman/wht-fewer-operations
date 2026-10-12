# r-1: independent check of p-1's floor (one letter on dual chains). All arithmetic in whole numbers; costs in DOUBLED units
# (a node of two or more points costs 2, a single point costs 1), so t' = value / 2.
import itertools, random, sys
import numpy as np
random.seed(20261011)

# ---------- 1. tree sparsity by dynamic programme, any integer vector, balanced tree on positions lo..hi ----------
def tsp(f, wl=1, wi=2):
    vals = sorted(set(f) | {0}); memo = {}
    def g(lo, hi, off):
        key = (lo, hi, off)
        if key in memo: return memo[key]
        if hi - lo == 1: r = 0 if f[lo] == off else wl
        else:
            mid = (lo + hi) // 2
            r = min((0 if o == off else wi) + g(lo, mid, o) + g(mid, hi, o) for o in vals)
        memo[key] = r; return r
    return g(0, len(f), 0)

# ---------- 2. brute force, no dynamic programme: every subset S of tree nodes; f is a combination of the indicators of S
#               iff f = 0 outside the union of S and f is constant on every atom (node minus its S-descendants) ----------
def nodes(n):
    out = []; size = n
    while size >= 1:
        out += [(lo, lo + size) for lo in range(0, n, size)]; size //= 2
    return out
def brute(f, wl=1, wi=2):
    n = len(f); nd = nodes(n); best = None
    for mask in range(1 << len(nd)):
        S = [nd[i] for i in range(len(nd)) if mask >> i & 1]
        w = sum(wl if b - a == 1 else wi for a, b in S)
        if best is not None and w >= best: continue
        owner = [None] * n                      # smallest node of S containing each point
        for a, b in sorted(S, key=lambda t: t[0] - t[1]):   # large first, small overwrite
            for x in range(a, b): owner[x] = (a, b)
        ok = True; val = {}
        for x in range(n):
            if owner[x] is None:
                if f[x] != 0: ok = False; break
            elif val.setdefault(owner[x], f[x]) != f[x]: ok = False; break
        if ok: best = w
    return best
bad = 0; cnt = 0
for f in itertools.product([-2, -1, 0, 1, 2], repeat=4):
    cnt += 1; bad += tsp(f) != brute(f)
    bad += tsp(f, 2, 2) != brute(f, 2, 2)
for f in itertools.product([1, -1], repeat=8):
    if f[0] == 1: cnt += 1; bad += tsp(f) != brute(f)
for _ in range(25):
    f = tuple(random.choice([-3, -2, -1, 0, 0, 1, 2, 3]) for _ in range(8)); cnt += 1; bad += tsp(f) != brute(f)
print("1. dynamic programme against brute force over all subsets of nodes:", cnt, "vectors,", bad, "disagreements"); sys.stdout.flush()

# ---------- 3. t' for ALL sign vectors on n points at once (numpy, whole numbers); bit i of the index = 1 means f_i = -1 ----------
def T_all(n):
    idx = np.arange(1 << n)
    def rec(lo, hi):
        if hi - lo == 1:
            s = 1 - 2 * ((idx >> lo) & 1)
            return {o: (s != o).astype(np.int16) for o in (0, 1, -1)}
        mid = (lo + hi) // 2; A = rec(lo, mid); B = rec(mid, hi)
        S = {o: A[o] + B[o] for o in (0, 1, -1)}
        return {off: np.minimum.reduce([S[o] + (0 if o == off else 2) for o in (0, 1, -1)]) for off in (0, 1, -1)}
    return rec(0, n)[0]
def L2(n):          # 2 L(n) in whole numbers: min over the two halves c0, c1 of sum over characters of min(t'(c0 chi), t'(c1 chi)), doubled
    T = T_all(n); k = n.bit_length() - 1
    chim = np.array([sum(1 << x for x in range(n) if bin(a & x).count('1') & 1) for a in range(n)])
    cs = np.arange(1 << n)
    P = T[cs[:, None] ^ chim[None, :]]                    # profile of every sign vector c
    U = np.unique(P, axis=0)
    best = None
    for i in range(len(U)):
        s = np.minimum(U[i][None, :], U).sum(axis=1).min()
        if best is None or s < best: best = int(s)
    return best, len(U), int(P.sum(axis=1).min()), T
for n in (2, 4, 8, 16):
    b, nu, one, T = L2(n)
    if n <= 8:      # spot check of the numpy table against the plain programme
        for m in range(1 << n): assert T[m] == tsp(tuple(1 - 2 * (m >> i & 1) for i in range(n)))
    print("2. N =", 2 * n, ": 2L(n) = floor for tau =", b, "  (L =", b / 2, ")  gates >=", 2 * n - 2 + b, "  distinct profiles", nu, "  one half only:", one / 2)
    sys.stdout.flush()

# ---------- 4. the inequality itself, on random sums of tree rectangles (NOT the transform): tau >= sum t'(row-pair differences) + sum t'(column-pair differences)
def Bfloor(M):      # doubled
    N = len(M); tot = 0
    for p in range(0, N, 2):
        tot += tsp(tuple(M[p][x] - M[p + 1][x] for x in range(N)))
        tot += tsp(tuple(M[y][p] - M[y][p + 1] for y in range(N)))
    return tot
viol = 0; tight = 0; trials = 0
for N, reps in ((4, 3000), (8, 3000), (16, 600)):
    nd = nodes(N); small = [t for t in nd if t[1] - t[0] == 1]
    for _ in range(reps):
        tau = random.randint(1, 3 * N); M = [[0] * N for _ in range(N)]; used = set()
        mode = random.random()
        while len(used) < tau:
            A = random.choice(small if random.random() < mode else nd); Bn = random.choice(small if random.random() < mode else nd)
            if (A, Bn) in used: continue
            used.add((A, Bn)); v = random.choice([-3, -2, -1, 1, 2, 3])
            for y in range(*A):
                for x in range(*Bn): M[y][x] += v
        b = Bfloor(M); trials += 1; viol += b > 2 * tau; tight += b == 2 * tau
print("4. inequality on random sums of tree rectangles:", trials, "trials,", viol, "violations,", tight, "cases of equality"); sys.stdout.flush()

# ---------- 5. the bound on actual designs. Standard dual chains: row nodes = blocks of consecutive addresses; column nodes = the same after reversing the bits of x
def rev(x, k): return int(format(x, '0%db' % k)[::-1], 2)
def design(k, r, c):
    N = 1 << k
    return [[r(y) * c(rev(x, k)) * (-1) ** bin(y & rev(x, k)).count('1') for x in range(N)] for y in range(N)]
b = lambda z, i: z >> i & 1
M45 = design(4, lambda y: (-1) ** (b(y, 0) * (1 + b(y, 3))), lambda x: (-1) ** (b(x, 0) * b(x, 3)))
print("5. the 45-rectangle design at 16 points: B =", Bfloor(M45) / 2, " (p-1 says 36)")
print("   all-ones scalings at 16 points: B =", Bfloor(design(4, lambda y: 1, lambda x: 1)) / 2, " (p-1 says 42)")
for k in (2, 3):
    N = 1 << k; best = None; hist = {}
    for rb in range(1 << (N - 1)):
        for cb in range(1 << (N - 1)):
            v = Bfloor(design(k, lambda y: 1 - 2 * (rb >> y & 1), lambda x: 1 - 2 * (cb >> x & 1)))
            hist[v] = hist.get(v, 0) + 1
    print("   N =", N, ": B(r,c) over ALL sign pairs (first signs fixed): least", min(hist) / 2, " census", {u / 2: hist[u] for u in sorted(hist)})
    sys.stdout.flush()
lo = None; cnt32 = 0; S = 20000
for _ in range(S):
    rb = random.getrandbits(16); cb = random.getrandbits(16)
    v = Bfloor(design(4, lambda y: 1 - 2 * (rb >> y & 1), lambda x: 1 - 2 * (cb >> x & 1)))
    lo = v if lo is None else min(lo, v); cnt32 += v == 64
print("   N = 16:", S, "random sign pairs: least B =", lo / 2, ";", cnt32, "of them have B = 32")
