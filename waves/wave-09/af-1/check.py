#!/usr/bin/env python3
"""af-1/check.py  Skeptic's replay of ad-1's inequality  R(N) >= T(N) - (q+1) T(q).
Own code, whole numbers only (bit masks and Python integers), no floats.
Part A: the plane, the slice identity as an identity of matrices, and both compositions on an integer input,
        at N = 4, 16, 64, 256, 1024, 4096 (ad-1 and aa-cross stopped at 256).
Part B: what the two inequalities give in numbers with tonight's best known counts (G).
Usage: check.py <max j>"""
import sys, random
POLY = {1: 0b11, 2: 0b111, 3: 0b1011, 4: 0b10011, 5: 0b100101, 6: 0b1000011}
def mk_mul(j):
    p = POLY[j]
    def mul(a, b):
        r = 0
        while b:
            if b & 1: r ^= a
            a <<= 1
            if a >> j: a ^= p
            b >>= 1
        return r
    return mul
def par(x): return bin(x).count("1") & 1
def wht(v):
    v = list(v); n = len(v); h = 1
    while h < n:
        for s in range(0, n, 2 * h):
            for t in range(s, s + h):
                a, b = v[t], v[t + h]; v[t], v[t + h] = a + b, a - b
        h *= 2
    return v
def basis_of(S):
    B = []; span = {0}
    for s in S:
        if s not in span:
            B.append(s); span |= {t ^ s for t in span}
    return B
def run(j):
    q = 1 << j; N = q * q; k = 2 * j; mul = mk_mul(j)
    # field sanity: every non-zero element has an inverse
    assert all(any(mul(a, b) == 1 for b in range(1, q)) for a in range(1, q))
    spread = [[a | (mul(c, a) << j) for a in range(q)] for c in range(q)] + [[b << j for b in range(q)]]
    # spread: q + 1 subspaces, cover everything, meet pairwise in 0
    cover = set()
    for S in spread: cover |= set(S)
    assert len(cover) == N and sum(len(set(S)) for S in spread) == N + q          # N - 1 non-zero + (q+1) zeros
    M = [sum(1 << x for x in range(N) if (x >> t) & 1) for t in range(k)]          # M[t] = mask of addresses with bit t set
    full = (1 << N) - 1
    def rowmask(y):                                                                # addresses x with x.y odd
        r = 0
        for t in range(k):
            if (y >> t) & 1: r ^= M[t]
        return r
    lines = []; allmasks = set(); slice_ok = True
    for S in spread:
        B = basis_of(S); assert len(B) == j
        bm = [rowmask(s) for s in B]
        cos = []                                                                   # cos[sigma] = mask of the coset of V = perp(S) with syndrome sigma
        for sig in range(q):
            m = full
            for t in range(j): m &= bm[t] if (sig >> t) & 1 else (full ^ bm[t])
            cos.append(m)
        assert all(bin(m).count("1") == q for m in cos)
        allmasks |= set(cos); lines.append((B, cos))
        # slice identity, as an identity of rows of the matrix: for y = sum beta_t B_t in S,
        #   row y of H  =  sum over sigma of (-1)^(beta.sigma) * indicator(coset sigma)
        for beta in range(q):
            y = 0
            for t in range(j):
                if (beta >> t) & 1: y ^= B[t]
            neg = 0
            for sig in range(q):
                if par(beta & sig): neg |= cos[sig]
            slice_ok &= (neg == rowmask(y))
    assert len(allmasks) == N + q
    # affine plane: two lines of different classes meet in exactly one point (enough: the two zero cosets meet in 0 only)
    z = [c[1][0] for c in lines]
    plane_ok = all(bin(z[a] & z[b]).count("1") == 1 for a in range(q + 1) for b in range(a))
    # compositions on an integer input
    rnd = random.Random(1000 + j); x = [rnd.randrange(-10**6, 10**6) for _ in range(N)]
    Hx = wht(x)
    got = {}; back_ok = True
    for B, cos in lines:
        L = []
        for sig in range(q):
            m = cos[sig]; s = 0
            while m:
                low = m & -m; s += x[low.bit_length() - 1]; m ^= low
            L.append(s)
        W = wht(L)                                                                  # the q-point transform of this family
        ys = []
        for beta in range(q):
            y = 0
            for t in range(j):
                if (beta >> t) & 1: y ^= B[t]
            ys.append(y)
            if y in got: assert got[y] == W[beta]
            got[y] = W[beta]
        # converse: line sums = (1/q) * q-point transform of the transform's outputs on S
        back = wht([Hx[y] for y in ys])
        back_ok &= all(b == q * l for b, l in zip(back, L))
    fwd_ok = (len(got) == N) and all(got[y] == Hx[y] for y in range(N))
    print("N = %4d  q = %2d : spread and plane ok %s ; lines %d ; slice identity on all %d rows %s ; "
          "transform = small transforms of line sums %s ; line sums = small transforms of the transform / q %s"
          % (N, q, plane_ok, len(allmasks), (q + 1) * q, slice_ok, fwd_ok, back_ok))
    assert plane_ok and slice_ok and fwd_ok and back_ok
if __name__ == "__main__":
    jm = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    print("Part A")
    for j in range(1, jm + 1): run(j)
    print("Part B  count (G); T = best KNOWN upper bounds tonight (7, 19, 52, 304 built; 1600 and beyond = the formula (3/4) N k + N/4, not built)")
    Tk = {2: 7, 3: 19, 4: 52, 6: 304}
    def T(k): return Tk.get(k, (3 * (1 << k) * k + (1 << k)) // 4)
    print("   N      floor N+q   T(N)-(q+1)T(q)  per point   T(N)+(q+1)T(q)  per point   adding-only (N+q)(q-1)   (1/2)(3/4) k")
    for j in (2, 3, 4, 5, 6, 8, 16):
        k = 2 * j; q = 1 << j; N = q * q
        lo = T(k) - (q + 1) * T(j) if j >= 2 else None; hi = T(k) + (q + 1) * T(j)
        print("   2^%-3d %-10d  %-14d  %-10.3f  %-14d  %-10.3f  %-22d   %.3f" % (k, N + q, lo, lo / N, hi, hi / N, (N + q) * (q - 1), 0.375 * k))
    print("   The lower column is NOT a lower bound on R: it uses upper bounds on T(N). With a proved lower bound on T(N)")
    print("   (nothing above linear is known) the inequality gives nothing above the floor N + q.")
