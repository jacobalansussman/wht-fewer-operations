# aa-note/check.py: recompute the formulas quoted in WAVE8-NOTE.md ("mine").
# Exact fractions except the roots of the price law, which are floats (marked).
from fractions import Fraction as F
from math import log, ceil

print("1. adding-only law for neighbour sums, N (k - 1 - floor(k/2)/2); and modulo-2 composition N (23k/32 - 1)")
for k in range(2, 9):
    N = 2 ** k
    g = F(N) * (k - 1 - F(k // 2, 2))
    line = f"  k={k} N={N} gates={g} per point={float(g / N):.4f} (3/4)k-1={0.75 * k - 1:.4f}"
    if k % 4 == 0:
        line += f"  mod-2 composed={F(N) * (F(23 * k, 32) - 1)}"
    print(line)
# 64 points modulo 2: four bits by the 15-gate block (30 gates per 16-point slice) plus a pair; ac-0 reports 216
print("  transform route for comparison, 2 T + N with T = (3/4) N k staircase (7,20,52,128,304):")
for N, T in ((16, 52), (32, 128), (64, 304)):
    print(f"   N={N}: 2T+N = {2 * T + N}  against adding-only {F(N) * (len(bin(N)) - 3 - 1 - F((len(bin(N)) - 3) // 2, 2))}")

print("2. hybrid 3: moves per extra block needed for a saving e: m^e/(1-e) - 1  (floats)")
for e in (0.01, 0.1, 0.5):
    print("  e=%g: " % e + ", ".join(f"m={m}: {m ** e / (1 - e) - 1:.3f}" for m in (4, 9, 45, 110, 1000)))
print("  published unit as quoted: d=0.095 over 16.5 blocks ->", round(0.095 / 15.5, 4), "per extra block (15.5 extra),",
      round(0.095 / 16.5, 4), "per block")

print("3. equal-blocks law: saving = L/(ln k + L), L = ln(1/(1-rho))  (floats)")
for kk, rho in ((16.5, 0.0021), (2, 0.074), (2, 0.99)):
    L = log(1 / (1 - rho))
    print(f"  blocks={kk} rho={rho}: saving={L / (log(kk) + L):.5f}  z={1 - L / (log(kk) + L):.4f}")

print("4. order bound kappa <= 1 + (2^(h-r)-1)/(2^r-1)")
for h, r in ((4, 2), (5, 2), (6, 2), (6, 3), (7, 3), (8, 3), (9, 3), (9, 4), (9, 1), (55, 24), (23, 9)):
    b = 1 + F(2 ** (h - r) - 1, 2 ** r - 1)
    print(f"  (h,r)=({h},{r}): {float(b):.4g}   1+2^(h-2r)={1 + 2.0 ** (h - 2 * r):.4g}")

print("5. leak lemma: c + 2 ceil(Rest/d), d = K-2")
for K in (4, 8, 16, 32, 64):
    d = K - 2
    c, rest = (5, 1) if K == 4 else (6, d * (d - 2) - 1)
    print(f"  K={K}: bound={c + 2 * ceil(F(rest, d))}  textbook={2 * K}  2K-2={2 * K - 2}  1.5K={1.5 * K}")

print("6. ab-1 sub-game: z >= ln(moves per array)/ln m  (floats)")
for m, mv in ((3, 3), (4, 3.75), (5, 3.875), (6, 3.9375)):
    print(f"  m={m}: least moves {mv}: largest saving {1 - log(mv) / log(m):.4f}")
print("  tiny unit 3 arrays in 8 moves at m=3: saving", round(1 - log(8 / 3) / log(3), 4))

print("7. line sums of the plane: adding-only (N + sqrt N)(sqrt N - 1); recursion beta*log2 log2 N per point")
for k in (4, 6, 8):
    N, q = 2 ** k, 2 ** (k // 2)
    print(f"  N={N}: {(N + q) * (q - 1)} gates, rank mod 2 = 3^(k/2) = {3 ** (k // 2)}")

print("8. ab-4 by-product c(N) >= 2N - 2 - log2 N:", [2 * 2 ** k - 2 - k for k in (2, 3, 4)])
print("9. ab-0 flat-rank: ceil(k/2) for k=2..8:", [ceil(k / 2) for k in range(2, 9)])
