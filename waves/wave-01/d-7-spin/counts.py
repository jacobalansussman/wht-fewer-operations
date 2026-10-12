#!/usr/bin/env python3
"""d-7-spin: counts by exact formula (python integers / fractions)."""
from math import comb, sqrt, log2
from fractions import Fraction as Fr

def d(k, j): return comb(k, j) - (comb(k, j - 1) if j else 0)

print("A. where the determinant (Morgenstern's volume) of the transform sits in the valence-bond form")
print("   log2|det H| = k N / 2.  scalars (-2)^j give sum_j d_j * j * n_j ; Krawtchouk blocks give sum_j d_j * n_j (n_j - 1) / 2,  n_j = k - 2j + 1")
print("   %6s %14s %14s %10s %12s" % ("k", "scalars/N", "blocks/N", "check", "blocks/(N sqrt k)"))
for k in (2, 4, 8, 16, 32, 64, 128, 256, 1024):
    N = 1 << k
    sc = sum(d(k, j) * j * (k - 2 * j + 1) for j in range(k // 2 + 1))
    bl = sum(d(k, j) * (k - 2 * j + 1) * (k - 2 * j) // 2 for j in range(k // 2 + 1))
    print("   %6d %14.4f %14.4f %10s %12.4f" % (k, float(Fr(sc, N)), float(Fr(bl, N)), sc + bl == k * N // 2, float(Fr(bl, N)) / sqrt(k)))

print()
print("B. the pair scheme (adapt to swapping bits 2i-1, 2i only): in = Walsh transforms on the swap orbits, middle = spin-1 kernel powers")
print("   in(k) = sum_s C(k/2,s) 2^(k/2-s) * s 2^s ;  mid(k) = sum_r C(k/2,r) * 4 r 3^(r-1) ;  total = 2 in + mid  against  k N")
for k in (2, 4, 8, 16, 32):
    h = k // 2; N = 1 << k
    cin = sum(comb(h, s) * 2 ** (h - s) * s * 2 ** s for s in range(h + 1))
    mid = sum(comb(h, r) * 4 * r * 3 ** (r - 1) for r in range(1, h + 1))
    print("   k=%3d  in=%d  mid=%d  total=%d  kN=%d  tie=%s" % (k, cin, mid, 2 * cin + mid, k * N, 2 * cin + mid == k * N))

print()
print("C. the recursion  t(k) = 2 E[t(Bin(k/2,1/2))] + E[tau(Bin(k/2,3/4))]   (t = cost per entry of the 2^k-point transform,")
print("   tau(r) = cost per entry of the r-fold power of the spin-1 kernel [[1,1,1],[2,0,-2],[1,-1,1]]; textbook tau(r) = 4r/3)")
def solve(tau, K):
    t = {0: 0.0, 1: 1.0}
    # odd sizes: peel one bit at textbook price 1
    for k in range(2, K + 1):
        if k % 2: t[k] = t[k - 1] + 1.0; continue
        h = k // 2
        # t(k) appears on the right only through s = h = k/2 < k, fine
        a = sum(float(Fr(comb(h, s), 2 ** h)) * t[s] for s in range(h + 1))
        m = sum(float(Fr(comb(h, r) * 3 ** r, 4 ** h)) * tau(r) for r in range(h + 1))
        t[k] = min(2 * a + m, float(k))
    return t
K = 1024
for name, tau in (("textbook 4r/3", lambda r: 4 * r / 3), ("(4/3) r^0.9", lambda r: 4 / 3 * r ** 0.9), ("(4/3) r^0.5", lambda r: 4 / 3 * r ** 0.5), ("linear: 4/3 flat", lambda r: 4 / 3 if r else 0.0)):
    t = solve(tau, K)
    print("   tau = %-18s" % name + "  ".join("t(%d)=%.2f" % (k, t[k]) for k in (4, 16, 64, 256, 1024)) + "   t(1024)/t(256)=%.3f  log4 of it = %.3f" % (t[1024] / t[256], log2(t[1024] / t[256]) / 2))

print()
print("D. per-bit coupling (Clebsch-Gordan one bit at a time): cost in = sum_i 2^(k-i) sum_blocks 2 (n-1), against k N one way")
print("   %6s %12s %12s %14s %16s" % ("k", "in/N", "k - in/N", "(k-in/N)/sqrt k", "dense mid/N"))
for k in (2, 3, 4, 6, 8, 16, 32, 64, 128, 256):
    N = 1 << k
    cin = 0
    for i in range(2, k + 1):
        m = i - 1
        cin += 2 ** (k - i) * sum(d(m, j) * 2 * (m - 2 * j) for j in range(m // 2 + 1))
    mid = sum(d(k, j) * (k - 2 * j + 1) * (k - 2 * j) for j in range(k // 2 + 1))
    print("   %6d %12.4f %12.4f %14.4f %16.4f" % (k, float(Fr(cin, N)), k - float(Fr(cin, N)), (k - float(Fr(cin, N))) / sqrt(k), float(Fr(mid, N))))
print("   k=4: in = %d additions for 16 points by this build" % sum(2 ** (4 - i) * sum(d(i - 1, j) * 2 * (i - 1 - 2 * j) for j in range((i - 1) // 2 + 1)) for i in range(2, 5)))
