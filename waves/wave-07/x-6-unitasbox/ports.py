#!/usr/bin/env python3
"""ports.py [x-6-unitasbox]  Exact whole numbers.  How many PORTS does the h-th tensor power of a 2 x 2 kernel K have?
A port = a direction b (non-zero address word) together with a complementary hyperplane U' (the words a with l.a = 0, l.b = 1)
such that  K^(tensor h) = (something that maps each coset of U' to itself) x (ONE butterfly layer along b, any coefficients).
Test [derived in x-6.md]: that holds exactly when, for each coset C of U' and each pair of columns {x, x+b}, the |C| x 2
block of the matrix has rank at most 1.  The unit needs v pairs with ports; ports sharing nothing can help each other."""
import itertools
def tens(K, h):
    N = 1 << h
    M = [[1] * N for _ in range(N)]
    for a in range(N):
        for x in range(N):
            p = 1
            for j in range(h): p *= K[a >> j & 1][x >> j & 1]
            M[a][x] = p
    return M
par = lambda x: bin(x).count("1") & 1
def ports(M, h):
    N = 1 << h; out = []
    for b in range(1, N):
        for l in range(1, N):
            if par(l & b) != 1: continue
            ok = True
            for c in (0, 1):
                C = [a for a in range(N) if par(a & l) == c]
                for x in range(N):
                    if x > x ^ b: continue
                    rows = [(M[a][x], M[a][x ^ b]) for a in C]
                    piv = next((r for r in rows if r != (0, 0)), None)
                    if piv and any(r[0] * piv[1] != r[1] * piv[0] for r in rows): ok = False; break
                if not ok: break
            if ok: out.append((b, l))
    return out
kern = [("Hadamard [[1,1],[1,-1]] (cross-ratio -1)", [[1, 1], [1, -1]]), ("[[1,2],[3,-6]] (cross-ratio -1)", [[1, 2], [3, -6]]),
        ("[[1,2],[3,5]] (generic)", [[1, 2], [3, 5]]), ("[[2,1],[1,1]] (cross-ratio 2)", [[2, 1], [1, 1]]),
        ("[[1,1],[1,3]] (cross-ratio 3)", [[1, 1], [1, 3]]), ("subset sums [[1,0],[1,1]]", [[1, 0], [1, 1]]),
        ("a reflection [[3,4],[4,-3]] (cross-ratio -9/16)", [[3, 4], [4, -3]]), ("an involution [[1,3],[0,-1]]", [[1, 3], [0, -1]])]
for h in (2, 3, 4, 5):
    for name, K in kern:
        P = ports(tens(K, h), h)
        dirs = sorted({b for b, l in P}); wts = sorted({bin(b).count("1") for b in dirs})
        print("h=%d  %-42s ports (direction, hyperplane): %3d ; distinct directions %3d of %d ; their weights %s ; hyperplane = b-perp for all: %s"
              % (h, name, len(P), len(dirs), (1 << h) - 1, wts, all(b == l for b, l in P)))
