# p-1-letter16: the cost of one "twisted quarter".  n points, the chain tree in bit order (pairs along bit 0, fours along bits 0,1, ...).
# p(f) = fewest tree nodes that partition the points into pieces on which the sign vector f is constant.
# P(n) = min over sign vectors rho of  sum over the n characters chi of p(rho * chi).   Exact, exhaustive, whole numbers.
import itertools, sys
def pieces(f):
    n = len(f)
    if all(v == f[0] for v in f): return 1
    # children in the tree: fix the TOP bit (halves are cosets of the subgroup of the low bits)
    return pieces(f[:n // 2]) + pieces(f[n // 2:])
for k in range(1, 5):
    n = 1 << k; chars = [[(-1) ** bin(a & x).count('1') for x in range(n)] for a in range(n)]
    best = None; hist = {}
    for rho in itertools.product([1, -1], repeat=n - 1):
        rho = (1,) + rho
        s = sum(pieces([p * q for p, q in zip(rho, ch)]) for ch in chars)
        hist[s] = hist.get(s, 0) + 1
        if best is None or s < best[0]: best = (s, rho)
    print("n =", n, " P(n) =", best[0], " at rho =", best[1], " for a character: ", (2 * n * n + 1) // 3, "  n log2 n + 1 =", n * k + 1, " histogram:", sorted(hist.items())[:6])
    sys.stdout.flush()
