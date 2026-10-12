# reflect.py (e-7-halftouch): exact check of the reading in section 2 of the report.
# After swapping columns 1 and 2, the 4-point transform is 2I - u u^T, u = (1,-1,-1,-1).  So with P the relabelling of
# N = 4^j points that does this swap in every base-4 digit, H_N * P = 2^j * (product of j commuting reflections), and
#     H_N = 2^j * P^T + (rest),   rest = 2^j * (R_1 ... R_j - I) * P^T.
# Printed: the rank of the rest, and, for the one-shot expansion into partial sums, how many terms each output needs
# (= entries per row of A) and how many numbers pass through the middle.
from fractions import Fraction as Fr
from itertools import product
def par(x): return bin(x).count("1") & 1
def Hm(n): return [[-1 if par(i & j) else 1 for j in range(n)] for i in range(n)]
def rank_mod(M, p=998244353):
    M = [[v % p for v in r] for r in M]; r = 0
    for c in range(len(M[0])):
        q = next((i for i in range(r, len(M)) if M[i][c]), None)
        if q is None: continue
        M[r], M[q] = M[q], M[r]; inv = pow(M[r][c], p - 2, p)
        for i in range(r + 1, len(M)):
            if M[i][c]:
                f = M[i][c] * inv % p; M[i] = [(a - f * b) % p for a, b in zip(M[i], M[r])]
        r += 1
    return r
sw = [0, 2, 1, 3]
for j in [1, 2, 3]:
    N = 4 ** j; H = Hm(N)
    def relabel(y):
        out = 0
        for d in range(j): out |= sw[(y >> (2 * d)) & 3] << (2 * d)
        return out
    # H' = H with columns relabelled; check H' = 2^j * tensor power of (I - u u^T / 2)
    u = [1, -1, -1, -1]
    R4 = [[(2 if a == b else 0) - u[a] * u[b] for b in range(4)] for a in range(4)]       # = 2I - u u^T
    ok = True
    for x in range(N):
        for y in range(N):
            v = 1
            for d in range(j): v *= R4[(x >> (2 * d)) & 3][(y >> (2 * d)) & 3]
            if H[x][relabel(y)] != v: ok = False
    S = [[(2 ** j) if relabel(y) == x else 0 for y in range(N)] for x in range(N)]   # 2^j * P^T in the original labels
    # H[x][relabel(y)] = 2^j at y = x on the diagonal of the product => S[x][relabel(x)] = 2^j
    S = [[0] * N for _ in range(N)]
    for x in range(N): S[x][relabel(x)] = 2 ** j
    rest = [[H[x][y] - S[x][y] for y in range(N)] for x in range(N)]
    print(f"N = {N}: relabelled transform is 2^{j} times a product of {j} reflections: {ok}; remainder has {N} entries of size {2**j};",
          f"rank of the rest (mod a prime; exact rank is at least this) = {rank_mod(rest)}, (N - sqrt N)/2 = {(N - 2**j)//2};",
          f"one-shot expansion: {2**j - 1} terms per output, {5**j - 4**j} numbers through the middle")
