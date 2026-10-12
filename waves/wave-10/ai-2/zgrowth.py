# ai-2: growth of the rigorous bounds on log2(largest minor of Z) for large k, in closed form (floating point, lgamma).
#   lower(k) = max over r of [ sum of the r largest log2 sigma_i  -  log2 C(N, r) ]   (Cauchy-Binet, weaker form: e_r >= product of the r largest sigma^2)
#   upper(k) = sum of log2 sigma_i over sigma_i > 1 = log2(phi) * k * C(k-1, floor((k-1)/2))
# sigma_i = phi^(k-2j) with multiplicity C(k,j).   Morgenstern: a circuit for Z with coefficients of size at most 1 has at least lower(k) gates.
import math
lphi = math.log2((1 + 5 ** 0.5) / 2)
def lC(n, r): return (math.lgamma(n + 1) - math.lgamma(r + 1) - math.lgamma(n - r + 1)) / math.log(2)
print("   k        lower/N    upper/N    0.2770*sqrt(k)    (lower)/(N log2 N /2)   r/N at the best r")
for k in (8, 10, 11, 12, 14, 16, 20, 24, 32, 40, 52, 60, 80, 100, 200, 400, 1000):
    N = 2.0 ** k; best = (0.0, 0.0); s = 0.0; r = 0.0
    for j in range(k + 1):
        m = k - 2 * j
        if m <= 0: break
        s += math.comb(k, j) * m * lphi; r += math.comb(k, j)
        if k <= 1000:
            # log2 C(N, r) by entropy for huge N (exact enough: relative error far below the digits printed)
            p = r / N; ent = N * (-(p * math.log2(p) + (1 - p) * math.log2(1 - p))) if 0 < p < 1 else 0.0
            v = s - (lC(N, r) if k <= 40 else ent)
            if v > best[0]: best = (v, p)
    up = lphi * k * math.comb(k - 1, (k - 1) // 2)
    print(f"  {k:4d}   {best[0]/N:9.4f}  {up/N:9.4f}   {0.2770*k**0.5:9.4f}        {best[0]/(N*k/2):9.4f}            {best[1]:.3f}")
