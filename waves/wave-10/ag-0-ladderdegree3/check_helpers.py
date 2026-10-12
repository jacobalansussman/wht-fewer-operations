#!/usr/bin/env python3
"""check_helpers.py [ag-0-ladderdegree3]  Tower design: are the helpers low-degree polynomials?
A(y) (P1 helper): degree in y.   B_a (P2 helper of colour a): on each piece 'lower bits = iota' (one atom active),
as a function of the free bits (everything except the lower bits and the active atom): degree.
Also the irregular Moore window for two partitions good for degree 3 (girth 16)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from designs import tower, pair_from_design, solve_U, degree_of_U

def moebius_deg(f, nb):
    f = list(f)
    for b in range(nb):
        bit = 1 << b
        for y in range(1 << nb):
            if y & bit: f[y] -= f[y ^ bit]
    return max([bin(y).count("1") for y in range(1 << nb) if f[y] != 0] or [0])

for (L, s) in ((2, 1), (2, 2), (3, 1)):
    m, acts = tower(L, s)
    k, t, l1, l2 = pair_from_design(m, acts)
    U, V, M = solve_U(k, 3, l1, l2); D = len(M)
    dA = degree_of_U(m, U, D)
    offs = []; mm = 0
    for j in range(L):
        offs.append(mm); mm += s * (1 if j == 0 else (1 << mm))
    worst = {}
    for a in range(L):
        off = offs[a]; sm = (1 << s) - 1
        for iota in range(1 << off if a else 1):
            pos = off + s * iota
            free = [b for b in range(off, m) if not (pos <= b < pos + s)]
            nb = len(free); dmax = 0
            for i in range(D):
                f = []
                for z in range(1 << nb):
                    y = iota
                    for j, b in enumerate(free):
                        if z >> j & 1: y |= 1 << b
                    f.append(V[(a, y)][i])
                dmax = max(dmax, moebius_deg(f, nb))
            worst[a] = max(worst.get(a, 0), dmax)
    print("tower L=%d s=%d k=%d : degree of A in y = %d ; degree of B_a on each piece, by colour: %s" % (L, s, k, dA, worst), flush=True)

print("irregular Moore window, girth 16 (n >= 2 * sum_{i<8} (d-1)^i, d = 2N/n; RECALLED theorem, as in ad-6):")
for kk in range(5, 17):
    N = 1 << kk
    n = 2
    while True:
        d = 2 * N / n
        if d <= 2 or n >= 2 * sum((d - 1) ** i for i in range(8)): break
        n += 1
    print("  k=%2d N=%6d  least classes allowed %6d = %.4f N" % (kk, N, n, n / N))
