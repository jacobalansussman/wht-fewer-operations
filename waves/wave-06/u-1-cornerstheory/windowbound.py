# u-1: the WINDOW BOUND, explicit.  Exact integers (math.comb), no search.
# Lemma used: a step between outputs S (the larger, "top", size s) and S' has R+ = {inputs T inside S, not inside S'}, |R+| >= 2^(s-1).
# If R+ is at most r runs of the input order, one run has length l >= ceil(2^(s-1)/r).  A window of L consecutive inputs inside it
# consists of L different subsets of S, so their union W has |W| >= lam = ceil(log2 L), and S contains W.
# For a fixed window at most comb(k-lam, s-lam) sets S of size s contain its union; each S is the top of at most 2 steps; there are N-L+1 windows.
# So  #(steps with top size s and at most r runs) * (l-L+1) <= 2 (N-L+1) comb(k-lam, s-lam).
from math import comb, ceil, log2
def few(k, s, r):
    N = 1 << k; l = -(-(1 << (s - 1)) // r); best = 2 * comb(k, s)
    L = 1
    while L <= l:
        lam = (L - 1).bit_length()
        if lam <= s:
            v = 2 * (N - L + 1) * comb(k - lam, s - lam) // (l - L + 1)
            best = min(best, v)
        L = L * 2 if L * 2 <= l else (l if L < l else l + 1)
    return best
def bound(k):
    N = 1 << k; best = (N, 0, 1)
    for s0 in range(1, k + 1):
        big = sum(comb(k, s) for s in range(s0, k + 1)); steps = (big + 1) // 2      # steps whose top has size >= s0
        r = 1
        while r <= N:
            cheap = sum(min(2 * comb(k, s), few(k, s, r)) for s in range(s0, k + 1))
            v = N + r * max(0, steps - cheap)       # every step has at least 1; the others at least r+1
            if v > best[0]: best = (v, s0, r)
            r *= 2
    return best
print(" k        N   corners >= (window bound)   per point   exponent log(bound)/log(N)   [top size from, runs r]   (N/2)log2 N + 1")
for k in list(range(3, 21)) + [24, 28, 32, 40, 48, 64, 96, 128]:
    v, s0, r = bound(k); N = 1 << k
    print(f"{k:3d} {N:>8.3g} {v:>14.6g} {v/N:12.3f} {log2(v)/k:10.4f}   [{s0}, {r}]   {N//2*k+1:.6g}")
