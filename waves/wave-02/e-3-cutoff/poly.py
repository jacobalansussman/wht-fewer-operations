#!/usr/bin/env python3
# e-3-cutoff, experiment 1: polynomials in the overlap t only.  Exact integers.
# p(t) = degree-d polynomial equal to (-1)^t on the window [a, a+d];  p(t) = sum_j c_j C(t,j).
# Newton form: p(t) = (-1)^a sum_{i<=d} (-2)^i C(t-a,i);  Vandermonde: C(t-a,i) = sum_j C(t,j) (-1)^(i-j) C(a+i-j-1,i-j).
from math import comb, isqrt, log2
from fractions import Fraction as F
def gbin(n, r):            # generalized binomial C(n, r) for any integer n, r >= 0
    num = 1
    for q in range(r): num *= (n - q)
    f = 1
    for q in range(2, r + 1): f *= q
    return num // f
def window99(k, target=F(99, 100)):
    p = [F(comb(k, t) * 3 ** (k - t), 4 ** k) for t in range(k + 1)]
    best = None; lo = 0; s = F(0)
    for hi in range(k + 1):
        s += p[hi]
        while s - p[lo] >= target: s -= p[lo]; lo += 1
        if s >= target and (best is None or hi - lo < best[1] - best[0]): best = (lo, hi, s)
    return best
print("gate count: none here (polynomials only)")
for k in (16, 64, 256):
    a, b, share = window99(k); d = b - a
    c = [(-1) ** a * sum((-2) ** i * gbin(-a, i - j) for i in range(j, d + 1)) for j in range(d + 1)]
    # for a = 0 the inner binomial C(i-j-1, i-j) is 0 unless i = j
    pv = lambda t: sum(c[j] * comb(t, j) for j in range(d + 1))
    assert all(pv(t) == (-1) ** t for t in range(a, b + 1))
    r = [(-1) ** t - pv(t) for t in range(k + 1)]
    assert all(r[t] == 0 for t in range(a, b + 1)) and all(r[t] != 0 for t in range(k + 1) if not a <= t <= b)
    # closed form of the leftover above the window: r(t) = (-1)^a sum_{i>d} (-2)^i C(t-a,i)
    assert all(r[t] == (-1) ** a * sum((-2) ** i * comb(t - a, i) for i in range(d + 1, t - a + 1)) for t in range(b + 1, k + 1))
    # below the window: r(t) = (-1)^t - (-1)^a sum_{i<=d} 2^i C(a-t+i-1,i)
    assert all(r[t] == (-1) ** t - (-1) ** a * sum(2 ** i * comb(a - t + i - 1, i) for i in range(d + 1)) for t in range(0, a))
    bits = lambda z: 0 if z == 0 else abs(z).bit_length()
    print("k=%d  window [%d,%d]  degree d=%d = %.2f sqrt(k)   share of pairs inside %.5f" % (k, a, b, d, d / k ** 0.5, float(share)))
    print("   bits of c_j, j=0..d: ", [bits(x) for x in c])
    print("   largest |c_j|: %d bits;  d*log2(k)=%.0f" % (max(bits(x) for x in c), d * log2(k)))
    print("   signs of c_j: ", "".join("+" if x > 0 else "-" if x < 0 else "0" for x in c))
    print("   bits of leftover r(t): t=0: %d   t=a-1: %d   t=b+1: %d   t=k/2: %d   t=k: %d" % (bits(r[0]), bits(r[a - 1]), bits(r[b + 1]), bits(r[k // 2]), bits(r[k])))
    print("   r(b+1) = %d = +-2^(d+1)? %s ;  r(a-1) = %d = +-(2^(d+1)... )" % (r[b + 1] if k < 100 else 0, abs(r[b + 1]) == 2 ** (d + 1), r[a - 1] if k < 100 else 0))
    # the same in the distance frame: delta = |x xor y| is k/2 +- 0.5 sqrt(k); (-1)^t = i^(|x|+|y|) (-i)^delta.
    # with weights' parities fixed delta moves in steps of 2, so a degree-d polynomial in delta fixes d+1 values of one parity
    pd = [F(comb(k, t), 2 ** k) for t in range(k + 1)]
    for dd in (d // 2, d):
        best = F(0)
        for lo in range(0, k + 1 - 2 * dd):
            # windows of dd+1 same-parity values lo, lo+2, ..., lo+2dd for one parity, and lo+1.. for the other
            s = sum(pd[lo + 2 * q] for q in range(dd + 1)) + sum(pd[lo + 1 + 2 * q] for q in range(dd + 1) if lo + 1 + 2 * q <= k)
            best = max(best, s)
        print("   distance frame, parity classes separate, degree %d: share of pairs exact %.5f" % (dd, float(best)))
