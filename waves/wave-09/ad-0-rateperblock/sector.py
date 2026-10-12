#!/usr/bin/env python3
"""sector.py [ad-0-rateperblock]  MODULO A PRIME p = 1 mod 4 (so that i exists).  Mutation `sector-test`.
A two-shear exchange  X' = x + U y ; Y += D X' ; X' -= D^-1 Y ; Y += V X'   (U, V free) works exactly when   D + D U D = V.
With scalars only it needs 1 in span(D, D^-1): true on one column, false from two (shears.py).  Here the free steps are widened to
every MONOMIAL step that acts alike on all columns: an address map (any invertible affine map of the h address bits of a column;
with `all` any permutation of the 2^h addresses) times a sign pattern (a character), the same on each of the f columns.
Question: is D in  A + D A D , A = span of those steps?   D = (a + b*shift_p) on every column, a = (1+i)/2, b = (1-i)/2.
Why modulo p suffices for a NO: a solution over the Gaussian rationals reduces modulo every prime that divides none of its
denominators; so 'no solution modulo p' for two primes means a solution would need both primes in its denominators.  A YES would be
a candidate only and would have to be lifted."""
import sys, itertools
def run(h, f, p, port, group):
    n = 1 << h; N = n ** f
    im = next(x for x in range(2, p) if x * x % p == p - 1)
    inv2 = pow(2, p - 2, p); a = (1 + im) * inv2 % p; b = (1 - im) * inv2 % p
    idx = lambda xs: sum(x * n ** k for k, x in enumerate(xs))
    pts = [tuple((i // n ** k) % n for k in range(f)) for i in range(N)]      # position in the list = idx(point)
    assert all(idx(x) == i for i, x in enumerate(pts))
    # D as a dense N x N list of dicts (sparse rows): D = tensor of (a + b S)
    def Dmat(e=1):
        rows = []
        for xs in pts:
            row = {}
            for mask in range(1 << f):
                ys = tuple(x ^ port if mask >> k & 1 else x for k, x in enumerate(xs))
                c = 1
                for k in range(f): c = c * (b if mask >> k & 1 else a) % p
                row[idx(ys)] = (row.get(idx(ys), 0) + c) % p
            rows.append(row)
        return rows
    D = Dmat()
    # monomial steps on one column: x -> g(x) with sign chi_q(x)
    if group == "all": perms = list(itertools.permutations(range(n)))
    else:
        perms = set()
        for cols in itertools.product(range(1, n), repeat=h):
            img = []
            for x in range(n):
                y = 0
                for k in range(h):
                    if x >> k & 1: y ^= cols[k]
                img.append(y)
            if len(set(img)) == n:
                for t in range(n): perms.add(tuple(y ^ t for y in img))
        perms = sorted(perms)
    par = lambda x: bin(x).count("1") & 1
    vecs = {}
    def flat(rows):          # sparse operator -> tuple key of (position, value)
        return tuple(sorted((r * N + c, v) for r, row in enumerate(rows) for c, v in row.items() if v))
    def mul(A, B):
        out = []
        for row in A:
            acc = {}
            for k, v in row.items():
                for c, w in B[k].items():
                    acc[c] = (acc.get(c, 0) + v * w) % p
            out.append(acc)
        return out
    gens = []
    for g in perms:
        for q in range(n):
            rows = []
            for xs in pts:
                s = 1
                for x in xs:
                    if par(q & x): s = -s
                rows.append({idx(tuple(g[x] for x in xs)): s % p})
            gens.append(rows)
    A = {}
    for M in gens: A[flat(M)] = M
    cols = [dict(k) for k in A]                                   # A
    for M in A.values(): cols.append(dict(flat(mul(mul(D, M), D))))   # D A D
    target = dict(flat(D))
    # Gaussian elimination modulo p on sparse vectors (dict position -> value); keep pivots
    piv = {}
    def reduce(v):
        v = dict(v)
        while v:
            k = min(v)
            if k not in piv: return v
            c = v[k]; w = piv[k]
            for kk, vv in w.items():
                x = (v.get(kk, 0) - c * vv) % p
                if x: v[kk] = x
                else: v.pop(kk, None)
        return v
    rk = 0
    for c in cols:
        v = reduce(c)
        if v:
            k = min(v); iv = pow(v[k], p - 2, p)
            piv[k] = {kk: vv * iv % p for kk, vv in v.items()}; rk += 1
    res = reduce(target)
    # controls: is 1 + D^2-type things inside (sanity): D^2 = shift on all columns must be in A ; D itself in A?
    pivA = {}
    def redA(v):
        v = dict(v)
        while v:
            k = min(v)
            if k not in pivA: return v
            c = v[k]; w = pivA[k]
            for kk, vv in w.items():
                x = (v.get(kk, 0) - c * vv) % p
                if x: v[kk] = x
                else: v.pop(kk, None)
        return v
    ra = 0
    for kkey in A:
        v = redA(dict(kkey))
        if v:
            k = min(v); iv = pow(v[k], p - 2, p)
            pivA[k] = {kk: vv * iv % p for kk, vv in v.items()}; ra += 1
    d2 = redA(dict(flat(mul(D, D)))); d1 = redA(target)
    print("h=%d f=%d (%d points) port %s group %-6s p=%d : %d monomial steps, dim A = %d, dim (A + D A D) = %d ; control D^2 in A: %s ; D in A: %s ; D in A + D A D: %s"
          % (h, f, N, bin(port)[2:].zfill(h), group, p, len(A), ra, rk, not d2, not d1, "YES (candidate, to be lifted)" if not res else "NO"), flush=True)
jobs = sys.argv[1] if len(sys.argv) > 1 else "small"
if jobs == "small":
    for p in (10009, 1000033):
        assert p % 4 == 1
        run(2, 1, p, 1, "all")
        run(2, 2, p, 1, "all")
        run(2, 3, p, 1, "all")
else:
    run(3, 2, 10009, int(jobs, 2), "affine")
