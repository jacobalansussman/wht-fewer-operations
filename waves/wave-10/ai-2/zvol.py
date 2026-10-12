# ai-2: how large are the minors of the subset-sum matrix Z (k address bits, N = 2^k)?  Exact whole numbers.
# (a) exhaustive largest minor at 4 and 8 points; (b) explicit minors: the "disjoint pairs" block (rows = complements of
# s-sets, columns = s-sets), determinant by exact elimination and by the eigenvalue formula; (c) two-sided bound from the
# singular values of Z: sum over all r x r minors of minor^2 = e_r (the r-th coefficient of det(1 + x Z^T Z)), so
#   largest minor^2 >= e_r / C(N,r)^2 ,   and   largest minor <= product of the singular values above 1.
import itertools, math, sys
from fractions import Fraction
def bareiss(M):
    M = [r[:] for r in M]; n = len(M); sign = 1; prev = 1
    for i in range(n):
        p = next((r for r in range(i, n) if M[r][i]), None)
        if p is None: return 0
        if p != i: M[i], M[p] = M[p], M[i]; sign = -sign
        for r in range(i + 1, n):
            for c in range(i + 1, n):
                M[r][c] = (M[r][c] * M[i][i] - M[r][i] * M[i][c]) // prev
        prev = M[i][i]
    return sign * M[n - 1][n - 1]
def Z(k): return [[1 if (x & y) == x else 0 for x in range(1 << k)] for y in range(1 << k)]
def lucas(m):
    a, b = 2, 1
    for _ in range(m): a, b = b, a + b
    return a
def e_poly(k):
    # coefficients of det(1 + x Z^T Z): singular values of the 2x2 block (1,0;1,1) are phi and 1/phi, so those of Z are
    # phi^(k-2j) with multiplicity C(k,j); a pair phi^(2m), phi^(-2m) gives the factor 1 + L_(2m) x + x^2 (L = Lucas numbers)
    N = 1 << k; P = [1]
    def mulq(P, L):   # times (1 + L x + x^2)
        Q = [0] * (len(P) + 2)
        for i, c in enumerate(P): Q[i] += c; Q[i + 1] += L * c; Q[i + 2] += c
        return Q
    def mull(P):      # times (1 + x)
        Q = [0] * (len(P) + 1)
        for i, c in enumerate(P): Q[i] += c; Q[i + 1] += c
        return Q
    for j in range(k + 1):
        m = k - 2 * j
        if m > 0:
            L = lucas(2 * m)
            for _ in range(math.comb(k, j)): P = mulq(P, L)
        elif m == 0:
            for _ in range(math.comb(k, j)): P = mull(P)
    assert len(P) == N + 1
    return P
print("(a) exhaustive, every minor of every order")
for k in (2, 3):
    M = Z(k); n = 1 << k; best = 0; sq = [0] * (n + 1)
    for m in range(1, n + 1):
        for R in itertools.combinations(range(n), m):
            for C in itertools.combinations(range(n), m):
                d = bareiss([[M[r][c] for c in C] for r in R]); sq[m] += d * d
                if abs(d) > best: best = abs(d)
    E = e_poly(k)
    print(f"  k={k}: largest |minor| of Z = {best}; sum of squared minors by order = {sq[1:]}; formula e_r = {E[1:]}; equal: {sq[1:] == E[1:]}")
print("(b) the disjoint-pairs block of Z: rows = complements of s-sets, columns = s-sets (order C(k,s))")
def kneser_formula(k, s):
    d = 1
    for j in range(s + 1):
        mult = math.comb(k, j) - (math.comb(k, j - 1) if j else 0)
        d *= math.comb(k - s - j, s - j) ** mult
    return d
for k in range(4, 10):
    M = Z(k) if k <= 8 else None; full = (1 << k) - 1; line = []
    for s in range(1, k // 2 + 1):
        if 2 * s > k: continue
        f = kneser_formula(k, s); order = math.comb(k, s)
        if M is not None and order <= 70:
            cols = [x for x in range(1 << k) if bin(x).count('1') == s]; rows = [full ^ x for x in cols]
            d = abs(bareiss([[M[r][c] for c in cols] for r in rows])); assert d == f, (k, s, d, f)
            line.append(f"s={s}: order {order}, |det| = {d} [elimination = formula]")
        else:
            line.append(f"s={s}: order {order}, |det| = 2^{math.log2(f):.1f} [formula]")
    print(f"  k={k} (N={1<<k}): " + "; ".join(line))
print("(c) bounds on log2(largest minor of Z) from the singular values; H needs (N/2) log2 N")
phi = (1 + 5 ** 0.5) / 2
kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 11
print("   k      N   explicit(b)   lower (Cauchy-Binet, best r)   upper = sum log2 sigma_i>1    upper/N   0.2770*sqrt(k)   (N/2)log2N")
for k in range(2, kmax + 1):
    N = 1 << k; E = e_poly(k); best = (-1e18, 0)
    for r in range(1, N + 1):
        v = 0.5 * (math.log2(E[r])) - math.log2(math.comb(N, r))
        if v > best[0]: best = (v, r)
    up = math.log2(phi) * sum(math.comb(k, j) * (k - 2 * j) for j in range(k + 1) if k > 2 * j)
    ex = max([math.log2(kneser_formula(k, s)) for s in range(1, k // 2 + 1) if 2 * s <= k] + [0])
    print(f"  {k:2d} {N:6d}   {ex:10.1f}   {max(best[0],0):12.1f} (r={best[1]})          {up:12.1f}             {up/N:6.3f}    {0.2770*k**0.5:6.3f}      {N*k//2}")
