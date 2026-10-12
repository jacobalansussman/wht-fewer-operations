#!/usr/bin/env python3
"""bent3.py [ad-5-whichbent]  Whole numbers (numpy int64, entries far below 2^63).  Bent patterns at 64 and 256 points:
quadric, patterns x1 . p(x2) with p a permutation (MM), partial-spread patterns (PS).  For each: bent? degree, rank over the
two-element field of [f(x+y)], largest flat on which it is constant, membership in the completed MM class (Dillon's
test: a subspace V of k/2 bits with all second derivatives along V equal to 0), and the identities used for pricing."""
import sys, itertools, random
import numpy as np
POLY = {3: 0b1011, 4: 0b10011}
def gmul(a, b, j):
    r = 0
    for i in range(j):
        if (b >> i) & 1: r ^= a << i
    for i in range(2 * j - 2, j - 1, -1):
        if (r >> i) & 1: r ^= POLY[j] << (i - j)
    return r
def gpow(a, e, j):
    r = 1
    for _ in range(e): r = gmul(r, a, j)
    return r
def par(x): return bin(x).count("1") & 1
def rref_subspaces(k, d):
    """all subspaces of dimension d of k bits, as lists of d basis vectors (reduced echelon form)"""
    for piv in itertools.combinations(range(k), d):
        free = []
        for i, p in enumerate(piv):
            free.append([c for c in range(p + 1, k) if c not in piv])
        tot = [len(f) for f in free]
        for bits in itertools.product(*[range(1 << t) for t in tot]):
            basis = []
            for i, p in enumerate(piv):
                v = 1 << p
                for t, c in enumerate(free[i]):
                    if (bits[i] >> t) & 1: v |= 1 << c
                basis.append(v)
            yield basis
def rank2(rows):
    rows = list(rows); r = 0
    while rows:
        p = rows.pop()
        if p == 0: continue
        r += 1; low = p & -p
        rows = [x ^ p if x & low else x for x in rows]
    return r
def study(name, g, k, subs, H):
    N = 1 << k; q = 1 << (k // 2); xs = np.arange(N)
    spec = H @ g
    bent = bool(np.all(np.abs(spec) == q))
    f = ((1 - g) // 2).astype(np.int64)
    a = f.copy()                                   # Moebius transform modulo 2: algebraic degree
    for i in range(k):
        m = (xs >> i) & 1 == 1
        a[m] ^= a[xs[m] ^ (1 << i)]
    deg = max((bin(x).count("1") for x in range(N) if a[x]), default=0)
    r2 = rank2([int("".join(str(int(f[x ^ y])) for y in range(N)), 2) for x in range(N)])
    # largest flat of constancy
    D = 0
    for d in sorted(subs, reverse=True):
        found = False
        for basis in subs[d]:
            e = np.ones(N, dtype=bool)
            for b in basis: e &= (g == g[xs ^ b])
            for b in basis: e &= e[xs ^ b]
            if e.any(): found = True; break
        if found: D = d; break
    # Dillon's test for the completed MM class
    half = k // 2
    Z = np.zeros((N, N), dtype=bool)
    for a_ in range(N):
        da = f ^ f[xs ^ a_]
        for b_ in range(a_ + 1, N):
            if not np.any(da ^ da[xs ^ b_]): Z[a_, b_] = Z[b_, a_] = True
    mm = 0
    for basis in subs[half]:
        if all(Z[x, y] for x, y in itertools.combinations(basis, 2)): mm += 1
    print("%-34s N=%3d bent=%s degree=%d rank2[f(x+y)]=%3d largest constant flat D=%s (k/2=%d) subspaces passing Dillon's MM test=%d %s"
          % (name, N, bent, deg, r2, D if D else "<%d" % min(subs), half, mm, "-> in MM#" if mm else "-> NOT in MM#"), flush=True)
    return spec
def conv(g, N):
    xs = np.arange(N)
    return g[xs[:, None] ^ xs[None, :]]
for j in (3, 4):
    if len(sys.argv) > 1 and int(sys.argv[1]) != j: continue
    k = 2 * j; q = 1 << j; N = q * q; xs = np.arange(N)
    H = np.array([[1 - 2 * par(x & y) for y in range(N)] for x in range(N)], dtype=np.int64)
    Hq = np.array([[1 - 2 * par(x & y) for y in range(q)] for x in range(q)], dtype=np.int64)
    subs = {d: list(rref_subspaces(k, d)) for d in (j, j + 1)}
    print("k=%d: %d subspaces of dimension %d, %d of dimension %d" % (k, len(subs[j]), j, len(subs[j + 1]), j + 1), flush=True)
    lo = lambda x: x & (q - 1); hi = lambda x: x >> j
    inv = [0] + [gpow(y, q - 2, j) for y in range(1, q)]
    perms = {"quadric  x1.x2": list(range(q))}
    if j == 3: perms["MM  x1.p(x2), p=y^3"] = [gpow(y, 3, j) for y in range(q)]
    if j == 4:
        cube = [gpow(y, 3, j) for y in range(q)]
        print("   note: y^3 on the field with 16 elements takes %d values: not a permutation (3 divides 15); y^7 and 1/y are" % len(set(cube)))
        perms["MM  x1.p(x2), p=y^7"] = [gpow(y, 7, j) for y in range(q)]
    perms["MM  x1.p(x2), p=1/y"] = inv
    pats = {}
    for nm, p in perms.items():
        assert sorted(p) == list(range(q))
        pats[nm] = np.array([1 - 2 * par(lo(x) & p[hi(x)]) for x in range(N)], dtype=np.int64)
    # spread of the field plane: S_m = {(a, m a)}, S_inf = {(0, b)}
    spread = {m: [a | (gmul(m, a, j) << j) for a in range(q)] for m in range(q)}; spread["inf"] = [b << j for b in range(q)]
    assert sorted(x for S in spread.values() for x in S if x) == list(range(1, N))
    tr = lambda m: par(m ^ gmul(m, m, j) ^ gpow(m, 4, j) ^ (gpow(m, 8, j) if j == 4 else 0)) if False else None
    def trace(m):
        t = 0; y = m
        for _ in range(j): t ^= y; y = gmul(y, y, j)
        assert t in (0, 1); return t
    I_tr = [m for m in range(q) if trace(m) == 1]
    rnd = random.Random(5 + j)
    while True:
        I_rn = sorted(rnd.sample(range(1, q), q // 2))
        s = 0
        for m in I_rn: s ^= m
        # avoid the sets that are translates of an additive hyperplane (those are trace-like)
        if len({a ^ b for a in I_rn for b in I_rn}) > q // 2: break
    def psminus(I):
        g = np.ones(N, dtype=np.int64)
        for m in I:
            for x in spread[m]:
                if x: g[x] = -1
        return g
    def psplus(I):
        g = -np.ones(N, dtype=np.int64)
        for m in I:
            for x in spread[m]: g[x] = 1
        return g
    pats["PS-  slopes of trace 1"] = psminus(I_tr)
    pats["PS-  slopes %s" % I_rn] = psminus(I_rn)
    pats["PS+  slopes %s + inf" % I_rn] = psplus(I_rn + ["inf"])
    specs = {}
    for nm, g in pats.items(): specs[nm] = study(nm, g, k, subs, H)
    # identity 1: every MM convolution = (Hq x I) SHEAR (Hq x I) / q^2 ... address = x1 + q*x2, so 'Hq on x1' = I (x) Hq in numpy's kron order
    A = np.kron(np.eye(q, dtype=np.int64), Hq)          # transforms the low half x1 inside every block x2
    for nm, p in perms.items():
        C = conv(pats[nm], N)
        sig = [0] * q
        for y in range(q): sig[p[y]] = y                 # sigma = inverse of p
        Pi = np.zeros((N, N), dtype=np.int64)
        for w in range(q):
            for x2 in range(q): Pi[w | ((x2 ^ sig[w]) << j), w | (x2 << j)] = 1
        ok1 = np.array_equal(C, A @ Pi @ A)
        # identity 2 (shear calculus): the shear is the product of j one-bit shears 'add e_i to x2 where bit i of sigma(w) is 1'
        prod = np.eye(N, dtype=np.int64)
        for i in range(j):
            E1 = np.zeros((q, q), dtype=np.int64)        # q * (projector onto the characters w with bit i of sigma(w) = 1)
            for w in range(q):
                if (sig[w] >> i) & 1: E1 += np.outer(Hq[w], Hq[w])
            E0 = q * np.eye(q, dtype=np.int64) - E1
            P = np.zeros((q, q), dtype=np.int64)
            for x2 in range(q): P[x2 ^ (1 << i), x2] = 1
            step = np.kron(np.eye(q, dtype=np.int64), E0) + np.kron(P, E1)
            prod = prod @ step
        ok2 = np.array_equal(prod, q ** (j - 1) * C)
        # identity 3: conjugate to the quadric by Phi = I (x) (Hq P_sigma Hq / q)
        Ps = np.zeros((q, q), dtype=np.int64)
        for w in range(q): Ps[sig[w], w] = 1
        Phi = np.kron(np.eye(q, dtype=np.int64), Hq @ Ps @ Hq)
        Cq = conv(pats["quadric  x1.x2"], N)
        ok3 = np.array_equal(Phi.T @ Cq @ Phi, q * q * C)
        nzPhi = int(np.count_nonzero(Hq @ Ps @ Hq))
        print("   %-24s C = A SHEAR A (no factor): %s | C = product of %d one-bit shears: %s | C = Phi^T C_quadric Phi / q^2: %s (small Phi has %d of %d non-zero entries)"
              % (nm, ok1, j, ok2, ok3, nzPhi, q * q), flush=True)
    # identity 4: PS- convolution = J - 2 * sum of coset sums of the chosen spread members + q I ; and PS-(trace 1) = MM(1/y)?
    for nm, I in (("PS-  slopes of trace 1", I_tr), ("PS-  slopes %s" % I_rn, I_rn)):
        C = conv(pats[nm], N); S = np.zeros((N, N), dtype=np.int64)
        for m in I:
            ind = np.zeros(N, dtype=np.int64); ind[spread[m]] = 1; S += conv(ind, N)
        print("   %-34s C = J - 2 (sum of %d coset-sum matrices) + q I: %s" % (nm, len(I), np.array_equal(C, 1 - 2 * S + q * np.eye(N, dtype=np.int64))), flush=True)
    gtr = pats["PS-  slopes of trace 1"]
    # is PS-(trace 1) literally a pattern x . p(y) for the split (a, b)?  g(a, b) = (-1)^Tr(b / a)
    lit = np.array([1 - 2 * trace(gmul(hi(x), inv[lo(x)], j)) for x in range(N)], dtype=np.int64)
    print("   PS-(slopes of trace 1)(a, b) = (-1)^Tr(b / a) on all points:", np.array_equal(gtr, lit), flush=True)
    # how many -1 in each spectrum (the type of the reflection)
    for nm in pats: print("   %-34s spectrum: %d entries -q, %d entries +q" % (nm, int((specs[nm] < 0).sum()), int((specs[nm] > 0).sum())))
