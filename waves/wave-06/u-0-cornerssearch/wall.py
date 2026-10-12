# u-0: the packing lower bound for the two-chain picture of subset sums, in whole numbers.
# Lemma: a step of cost <= c between outputs S, S' (S not inside S') forces a block of at least L = ceil(2^(|S|-1)/c)
# consecutive inputs all inside S.  Blocks of two outputs S1, S2 of one size j share at most 2^|S1 n S2| inputs.
# So: (number of outputs of size j owning such a block) <= P * V, P = floor((N-L)/(L-m)) + 1 with m = 2^(j-t) < L,
#     V = number of j-sets meeting a given j-set in more than j-t elements.  Each output is in at most 2 steps.
# corners >= max over c of (c+1) * (N - 2 * sum_j min(C(k,j), P*V)).
import sys
from math import comb
def good_bound(k, c):
    N = 1 << k; tot = 0
    for j in range(k + 1):
        L = -(-(1 << j) // (2 * c)) if j >= 1 else 1      # ceil(2^(j-1)/c)
        best = comb(k, j)
        for t in range(1, j + 1):
            m = 1 << (j - t)
            if m >= L: continue
            P = (N - L) // (L - m) + 1
            V = sum(comb(j, i) * comb(k - j, i) for i in range(t))
            if P * V < best: best = P * V
        tot += best
    return tot
if __name__ == '__main__':
    for k in [int(a) for a in sys.argv[1:]]:
        N = 1 << k; bestv = (N, 0)
        c = 1
        while True:
            g = good_bound(k, c)
            if 2 * g >= N: break
            v = (c + 1) * (N - 2 * g)
            if v > bestv[0]: bestv = (v, c)
            c = c + 1 if c < 64 else int(c * 1.25)
        num, den = bestv[0] * 1000 // N, 1000
        print(f"k={k}: corners >= {num/den:.3f} N (best c = {bestv[1]});  Yates per point = {k/2};  ratio to Yates {num/den/(k/2):.4f}", flush=True)
