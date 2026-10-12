# g-4-zetalead / calls3.py : how many calls of H does a rational 2 x 2 kernel with invariant tau need?  Exact rationals.
# Two calls reach exactly the tau that are rational squares (a-0).  Three calls: the kernel of H D(a,b) H D(c,d) H is
#   [[pc+qd, pc-qd],[qc+pd, qc-pd]],  p = a+b, q = a-b,  with invariant  tau = (su+1)(u-s) / ((su-1)(u+s)),  s = p/q, u = c/d.
# For a given tau and s this is a quadratic in u:  s(1-tau) u^2 + (1-s^2)(1+tau) u - s(1-tau) = 0.
# Search s = m/n of small height for a rational root u, then CHECK the word as a product of 2 x 2 matrices.
from fractions import Fraction as Fr
from math import isqrt, gcd
import sys
def is_sq(x):
    if x < 0: return None
    n, d = x.numerator, x.denominator
    rn, rd = isqrt(n), isqrt(d)
    return Fr(rn, rd) if rn * rn == n and rd * rd == d else None
def mm(A, B): return [[sum(A[i][t] * B[t][j] for t in range(2)) for j in range(2)] for i in range(2)]
H = [[Fr(1), Fr(1)], [Fr(1), Fr(-1)]]
def dg(a, b): return [[Fr(a), Fr(0)], [Fr(0), Fr(b)]]
def tau(M): return M[0][0] * M[1][1] / (M[0][1] * M[1][0])
B = int(sys.argv[1]) if len(sys.argv) > 1 else 120
for t in [Fr(2), Fr(3), Fr(5), Fr(-2), Fr(-3), Fr(1, 2), Fr(7), Fr(-5), Fr(6), Fr(10), Fr(2, 3), Fr(-1, 2)]:
    found = None; tried = 0
    for n in range(1, B + 1):
        for m in range(-B, B + 1):
            if m == 0 or gcd(abs(m), n) != 1: continue
            s = Fr(m, n)
            if s * s == 1: continue
            tried += 1
            A2 = s * (1 - t); B1 = (1 - s * s) * (1 + t); C0 = -s * (1 - t)
            r = is_sq(B1 * B1 - 4 * A2 * C0)
            if r is None: continue
            for u in ((-B1 + r) / (2 * A2), (-B1 - r) / (2 * A2)):
                if u == 0 or u * u == s * s or s * u == 1 or s * u == -1: continue
                p, q, c, d = s, Fr(1), u, Fr(1)
                K = mm(mm(mm(mm(H, dg((p + q) / 2, (p - q) / 2)), H), dg(c, d)), H)
                if all(K[i][j] != 0 for i in range(2) for j in range(2)) and tau(K) == t:
                    found = (s, u, K); break
            if found: break
        if found: break
    if found:
        s, u, K = found
        print("tau = %-5s THREE calls: H D(%s,%s) H D(%s,1) H = %s  (invariant %s)" % (t, (s + 1) / 2, (s - 1) / 2, u, [[str(x) for x in r] for r in K], tau(K)))
    else:
        print("tau = %-5s no three-call word with s of height <= %d (%d values of s tried); is it a square: %s" % (t, B, tried, is_sq(t) is not None))
