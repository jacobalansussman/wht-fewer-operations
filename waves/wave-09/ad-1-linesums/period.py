#!/usr/bin/env python3
"""period.py [ad-1-linesums]  One cyclic pass with a fixed number of gates per point whose 2-adic valuation grows with the
size of its coefficient, at selected primes only.
64 points: eta = t^9 + t^18 + t^36 (the three squares-orbit powers of a 7th root of unity) satisfies eta^2 + eta + 2 = 0.
           The pass  a + b * eta  with  a + b*eta = eta^L  (whole numbers a, b) costs 3 gates per point for every L.
256 points: rho = t^17 + t^34 + t^68 + t^136 (15th roots of unity) satisfies rho^2 - rho + 4 = 0 (d-1's quadratic number).
           The pass  a + b * rho = rho^L  costs 4 gates per point for every L.
Printed: the valuation of the pass at every prime of the top component (Galois ring Z/2^24[t]/(h), exact)."""
import math
def study(k, PRIM, expo, rel, name):
    N = 1 << k; n = N - 1; s = 24; MOD = 1 << s
    def mul(a, b):
        r = [0] * (2 * k - 1)
        for i in range(k):
            if a[i]:
                for l in range(k): r[i + l] += a[i] * b[l]
        for d in range(2 * k - 2, k - 1, -1):
            c = r[d]
            if c:
                r[d] = 0
                for i in range(k): r[d - k + i] -= c * PRIM[i]
        return [v % MOD for v in r[:k]]
    tau = [0, 1] + [0] * (k - 2)
    for _ in range(k * (s - 1)): tau = mul(tau, tau)
    pw = [[1] + [0] * (k - 1)]
    for i in range(1, n): pw.append(mul(pw[-1], tau))
    assert mul(pw[-1], tau) == pw[0]
    def val(x):
        v = s
        for c in x:
            c %= MOD
            if c: v = min(v, (c & -c).bit_length() - 1)
        return v
    seen = set(); top = []
    for a in range(1, n):
        if a in seen or math.gcd(a, n) != 1: continue
        b = a
        while b not in seen: seen.add(b); b = (2 * b) % n
        top.append(a)
    print("%d points: pass a + b * %s, %d gates per point; %d primes in the top component" % (N, name, len(expo), len(top)))
    a_, b_ = 0, 1                                   # the element a_ + b_ * x with x^2 = rel[0] * x + rel[1]
    for L in range(1, 13):
        if L > 1: a_, b_ = b_ * rel[1], a_ + b_ * rel[0]
        vals = []
        for a in top:
            x = [0] * k
            for e in expo:
                x = [u + v for u, v in zip(x, pw[(a * e) % n])]
            vals.append(val([a_ * (1 if i == 0 else 0) + b_ * x[i] for i in range(k)]))
        print("   L = %2d  a = %7d  b = %7d   largest |coefficient ratio| %.1f   valuations %s" % (L, a_, b_, max(abs(a_), abs(b_)) / max(1, min(abs(a_), abs(b_))), vals))
study(6, [1, 1, 0, 0, 0, 0], [9, 18, 36], (-1, -2), "(t^9 + t^18 + t^36)")
study(8, [1, 0, 1, 1, 1, 0, 0, 0], [17, 34, 68, 136], (1, -4), "(t^17 + t^34 + t^68 + t^136)")
