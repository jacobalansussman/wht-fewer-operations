#!/usr/bin/env python3
"""leakbound.py [ab-6-chainexchanges]  EXACT (whole numbers).  The numbers that enter the leak lemma of ab-6.md section 1.
Family: boxes P_g, g an address map (invertible bit matrix) on K = 2^k addresses.  R^K = 2 fixed numbers + V, dim V = K - 2.
The K x K table = (2 + V) x (2 + V) = 4 fixed + 4 V + V (x) V, and V (x) V = 1 + mV copies of V + Rest.
mV = <chi^3, 1> with chi = (fixed non-zero addresses) - 1, by a sum over the whole group.
Leak lemma: calls >= copies of V + ceil((Rest + d * ceil(Rest / d)) / d), d = K - 2."""
import itertools, sys
from fractions import Fraction as Fr
def group(k):
    n = 1 << k; out = []
    for cols in itertools.product(range(1, n), repeat=k):
        img = [0] * n; ok = True
        for x in range(1, n):
            v = 0
            for j in range(k):
                if x >> j & 1: v ^= cols[j]
            img[x] = v
        if len(set(img)) == n: out.append(img)
    return out
for k in (2, 3, 4):
    K = 1 << k; Gp = group(k); d = K - 2
    s1 = s2 = s3 = 0
    for img in Gp:
        chi = sum(1 for x in range(1, K) if img[x] == x) - 1
        s1 += chi; s2 += chi * chi; s3 += chi ** 3
    o = len(Gp); assert s1 == 0 and s2 == o and s3 % o == 0
    mV = s3 // o; rest = d * d - 1 - mV * d; copies = 4 + mV
    ceil = lambda a, b: -(-a // b)
    bound = copies + ceil(rest + d * ceil(rest, d), d)
    print("K = %2d: group order %5d, V irreducible (<chi,chi> = 1), copies of V in V x V: %d, copies of V in the table: %d, Rest: %d dimensions;"
          " leak bound %d calls; textbook %d; telescoping bound (x-3) %d" % (K, o, mV, copies, rest, bound, 2 * K, K + K // 2))
# parts of the table at K = 4 (x-3 section 4 found by float search: skew part 4 calls, symmetric part 3 calls)
print("K = 4, skew part: 2 copies of V, Rest 1 -> bound %d ; symmetric part: 3 copies of V, Rest 0 -> bound %d" % (2 + -(-(1 + 2) // 2), 3))
