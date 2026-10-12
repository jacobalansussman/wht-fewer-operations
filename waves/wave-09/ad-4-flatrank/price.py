#!/usr/bin/env python3
"""price.py [ad-4-flatrank]  The decompositions of g(z) = (-1)^(z1 z2 + z3 z4 + ...) read as N x N matrices: x = the odd-numbered bits of z,
y = the even-numbered ones, so g = (-1)^(x.y) = H(x, y), N = 2^(K/2).  A flat of the K-bit space is then a 0/+1/-1 matrix M with
p = log2(rows it touches), q = log2(columns it touches), t = log2(rank).  It is 'sum the inputs over 2^t classes of 2^(q-t) columns, hand each
sum to 2^(p-t) outputs'.  PRICE of a decomposition when every piece is computed by itself and added at the outputs, count (G):
   sum over pieces of (2^q - 2^t)  +  sum over pieces of 2^p  -  N       (the first piece to reach an output is free).
TOTAL RANK = sum of 2^t (at least N by the rank of H).   Whole numbers only."""
import sys
from collections import Counter
def split(z, K):
    x = y = 0
    for i in range(0, K, 2):
        x |= ((z >> i) & 1) << (i // 2); y |= ((z >> (i + 1)) & 1) << (i // 2)
    return x, y
def analyse(sups, K):
    N = 1 << (K // 2); out = []; price = -N; trank = 0
    for sup in sups:
        pts = [split(z, K) for z in range(1 << K) if (sup >> z) & 1]
        rows = {x for x, y in pts}; cols = {y for x, y in pts}
        p = len(rows).bit_length() - 1; q = len(cols).bit_length() - 1; d = len(pts).bit_length() - 1; t = p + q - d
        out.append((p, q, t)); price += (1 << q) - (1 << t) + (1 << p); trank += 1 << t
    return sorted(out, reverse=True), price, trank
best = {}
for fn in sys.argv[1:]:
    for line in open(fn):
        if not line.startswith("CANDIDATE"): continue
        head = line.split("(")[0].split(); r = int(head[1].split("=")[1]); K = int(head[2].split("=")[1])
        sups = [int(t.split(":")[0], 16) for t in line.split("):")[1].split()]
        pq, price, trank = analyse(sups, K); key = (K, r)
        best.setdefault(key, []).append((price, trank, pq))
for (K, r), lst in sorted(best.items()):
    lst.sort(); N = 1 << (K // 2)
    print("N=%d points (K=%d bits doubled), %d flats, %d decompositions from the search: price min %d, median %d, max %d (textbook %d); total rank min %d, max %d (floor N = %d)" % (
        N, K, r, len(lst), lst[0][0], lst[len(lst) // 2][0], lst[-1][0], N * (K // 2), min(x[1] for x in lst), max(x[1] for x in lst), N))
    print("    cheapest: (p,q,t) per flat", lst[0][2], " total rank", lst[0][1])
# the product decomposition H = Z D Z^T : one rectangle [x contains S][y contains S] per subset S
for k in (2, 3, 4):
    N = 1 << k; price = -N; tr = 0
    for S in range(N):
        s = bin(S).count("1"); p = q = k - s; t = 0; price += (1 << q) - (1 << t) + (1 << p); tr += 1
    print("product decomposition at N=%d: %d flats, all of rank 1 (total rank %d = N), price computed separately %d ; with the sums shared (Z, then Z transposed) %d ; textbook %d" % (N, N, tr, price, N * k, N * k))
