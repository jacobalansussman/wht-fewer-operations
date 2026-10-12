# a-0, part (c): the middle and the phrase "any Jordan basis".  Exact rationals / integers.
# 1. Pascal block = diag(j!) * Toeplitz(1/(j-i)!) * diag(1/i!)   (a product with ONE FIXED polynomial, truncated): m = 1..40.
# 2. Krawtchouk block = Pascal-type * diagonal * Pascal-type, exactly: K_u = L diag((-2)^i) R with
#    L[j][i] = C(u-i, j-i) ... checked by brute force against the definition, u = 0..24.
# 3. "ANY Jordan basis of U" fails for H at 4 points: a Jordan basis of U in which H is not block diagonal.
#    And the repair: Z IS block diagonal (Toeplitz 1/(j-i)!) in any Jordan basis; H = Z D X Z X costs two passes.
# 4. The ledger of the middle with a real operation count instead of "m log2 m": dense, Karatsuba-free plain count, and an
#    FFT count (needs a root of unity of order 2^l >= 2m, NOT available to a rational program), k up to 2^16.
from fractions import Fraction as Fr
from math import comb, factorial, log2
def mm(A, B): return [[sum(A[i][t] * B[t][j] for t in range(len(B)) if A[i][t]) for j in range(len(B[0]))] for i in range(len(A))]

ok = True
for m in range(1, 41):
    P = [[Fr(comb(j, i)) for i in range(m)] for j in range(m)]
    T = [[Fr(1, factorial(j - i)) if j >= i else Fr(0) for i in range(m)] for j in range(m)]
    DL = [[Fr(factorial(j)) if i == j else Fr(0) for i in range(m)] for j in range(m)]
    DR = [[Fr(1, factorial(j)) if i == j else Fr(0) for i in range(m)] for j in range(m)]
    ok &= mm(mm(DL, T), DR) == P
print("1. Pascal(m) = diag(j!) Toeplitz(1/(j-i)!) diag(1/i!), m = 1..40:", ok)

def kraw(u, j, i): return sum((-1) ** l * comb(j, l) * comb(u - j, i - l) for l in range(0, i + 1) if l <= j and i - l <= u - j)
ok = True
for u in range(0, 25):
    m = u + 1
    K = [[kraw(u, j, i) for i in range(m)] for j in range(m)]           # K[j][i]: coefficient of E_j in H E_i (schur convention)
    # H = Z diag(1,-2) Z^T on one bit; on Sym^u in the basis E_i (sum of all i-subsets of u points):
    #   Z   : E_i -> sum_j C(j,i) E_j                (Pascal, lower)
    #   Z^T : E_i -> sum_j C(u-j, i-j) E_j           (superset counts, upper)
    #   D   : E_i -> (-2)^i E_i
    ZL = [[comb(j, i) for i in range(m)] for j in range(m)]
    ZU = [[comb(u - j, i - j) if i >= j else 0 for i in range(m)] for j in range(m)]
    D = [[(-2) ** i if i == j else 0 for i in range(m)] for j in range(m)]
    ok &= mm(mm(ZL, D), ZU) == K
print("2. Krawtchouk(u) = Pascal-lower * diag((-2)^i) * Pascal-upper, u = 0..24:", ok)

# 3. four points, coordinates indexed by subsets of {0,1}: 0 = {}, 1 = {0}, 2 = {1}, 3 = {0,1}
def up(v): return [0, v[0], v[0], v[1] + v[2]]
def wht(v): a, b, c, d = v; return [a + b + c + d, a - b + c - d, a + b - c - d, a - b - c + d]
def zeta(v): a, b, c, d = v; return [a, a + b, a + c, a + b + c + d]
def solve_in_span(vecs, w):
    # exact: is w in the span of vecs (rational)? Gaussian elimination on the augmented system
    rows = [[Fr(v[i]) for v in vecs] + [Fr(w[i])] for i in range(len(w))]
    n = len(vecs); r = 0
    for c in range(n):
        p = next((i for i in range(r, len(rows)) if rows[i][c] != 0), None)
        if p is None: continue
        rows[r], rows[p] = rows[p], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i][c] != 0:
                f = rows[i][c] / rows[r][c]; rows[i] = [x - f * y for x, y in zip(rows[i], rows[r])]
        r += 1
    return all(any(x != 0 for x in row[:n]) or row[n] == 0 for row in rows)
for c in (0, 1):
    head3 = [1, 0, 0, 0]; s3 = [head3, up(head3), [x // 2 for x in up(up(head3))]]        # e_{}, e_0 + e_1, e_{01}
    head1 = [0, 1, -1, c]                                                                # e_0 - e_1 + c e_{01}: U kills it for every c
    assert up(head1) == [0, 0, 0, 0] and up(s3[2]) == [0, 0, 0, 0]
    indep = not solve_in_span(s3, head1)
    print("3. c=%d: (e_0 - e_1 + c e_01) with the string of e_{} is a Jordan basis of U: %s ; H keeps the short string: %s ; Z keeps it: %s"
          % (c, indep, solve_in_span([head1], wht(head1)), solve_in_span([head1], zeta(head1))))
print("   so with c = 1 the transform is NOT block diagonal in a Jordan basis of U (smallest case: 4 points); Z always is.")

# 4. ledger of the middle, per entry.  multiplicity f = C(k,w) - C(k,w-1), block side m = k - 2w + 1.
#    dense Pascal (plain passes): m(m-1)/2 additions, twice, plus m scalings  -> about m^2
#    FFT with a root of unity of order L = least power of two >= 2m: one fixed-vector product = two transforms of length L,
#    (L/2) log2 L butterflies each at 3 operations, plus L pointwise scalings; a Krawtchouk block needs two products + 3m scalings.
def fftcost(m):
    if m == 1: return 0
    L = 1
    while L < 2 * m: L *= 2
    l = L.bit_length() - 1
    return 2 * 3 * (L // 2) * l + L
def best(m): return min(m * (m - 1) // 2, fftcost(m))
print("4. middle per entry for H (two fixed-vector products per block + 3 scalings per entry):")
print("      k      dense    m log2 m model    FFT count    best of dense/FFT    (1/2)log2 k    blocks where FFT wins hold this share of entries")
for e in range(2, 17, 2):
    k = 1 << e; N = 1 << k; dn = ft = bs = md = sh = 0; cur = 1; prev = 0      # cur = C(k,w), prev = C(k,w-1), exact integers
    for w in range(k // 2 + 1):
        f = cur - prev; m = k - 2 * w + 1
        dn += f * (m * (m - 1) + 3 * m); ft += f * (2 * fftcost(m) + 3 * m); bs += f * (2 * best(m) + 3 * m)
        if fftcost(m) < m * (m - 1) // 2: sh += f * m
        if m > 1: md += f * m * int(round(log2(m) * 10 ** 6))                 # log2 m to six decimals, summed exactly
        prev = cur; cur = cur * (k - w) // (w + 1)
    q = lambda a: float(Fr(a, N))
    print("  %7d  %9.2f  %9.2f  %12.2f  %12.2f  %14.1f   %.4f" % (k, q(dn), q(md) / 10 ** 6, q(ft), q(bs), e / 2, q(sh)))
