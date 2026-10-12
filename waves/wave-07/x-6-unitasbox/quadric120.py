#!/usr/bin/env python3
"""quadric120.py [x-6-unitasbox]  Exact whole numbers.  The 120 E8 ports against the quadric of s-cross hybrid 1 / u-7.
B[t][s] = (-1)^(number of common ones of port t and port s): the plain pattern of the transform on the 120 ports.
u-7's block satisfies M^2 + 8M - 128 = 0 with trace 120 (s-cross hybrid 1: -16 thirty-five times, +8 eighty-five times)."""
import sys, json, gzip, itertools
c = json.load(gzip.open(sys.argv[1])); P = c["ports"]; v = len(P)
wt = lambda x: bin(x).count("1")
allw = sorted(x for x in range(512) if wt(x) % 4 == 3)
print("the ports are exactly the 9-bit words of weight 3 modulo 4:", sorted(P) == allw, "(%d words); the other odd words: %d" % (len(allw), sum(1 for x in range(512) if wt(x) % 4 == 1)))
B = [[(-1) ** wt(a & b) for b in P] for a in P]
B2 = [[sum(B[i][k] * B[k][j] for k in range(v)) for j in range(v)] for i in range(v)]
for sg in (1, -1):
    ok = all(B2[i][j] + sg * 8 * B[i][j] - 128 * (i == j) == 0 for i in range(v) for j in range(v))
    print("B^2 %s 8B - 128 = 0: %s" % ("+" if sg == 1 else "-", ok))
tr = sum(B[i][i] for i in range(v))
print("trace of B:", tr, "; so if B^2 - 8B - 128 = 0 the eigenvalues are 16 (n times) and -8 (120 - n times) with 16n - 8(120 - n) = trace: n =", (tr + 960) / 24)
print("entries +1 off the diagonal per row (the pairs that know each other):", sorted({sum(1 for j in range(v) if j != i and B[i][j] == 1) for i in range(v)}))
