# ag-4: gates (G) per point of the known generators of the half-rate space S_k (k odd), against the floors.
# space(r,k): split on one bit, f = (u, u + v) with u of degree <= r and v of degree <= r - 1 on k - 1 bits; one gate per point of
#   the half cube; ENDS FREE: degree 0 (all outputs are copies of one input) and degree >= k (every function: outputs = inputs).
#   Known exact ends used: degree 1 and degree k - 1 cost N - 2.
# mono(r,k): the same recursion for the MATRIX in the monomial basis (the full cube then costs (k/2) 2^k, Yates).
from functools import lru_cache
from math import comb, sqrt
import sys
sys.setrecursionlimit(10000)
@lru_cache(None)
def space(r, k):
    if r <= 0 or r >= k: return 0
    if r == 1 or r == k - 1: return (1 << k) - 2
    return space(r, k - 1) + space(r - 1, k - 1) + (1 << (k - 1))
@lru_cache(None)
def mono(r, k):
    if r <= 0 or k == 0: return 0
    return mono(min(r, k - 1), k - 1) + mono(r - 1, k - 1) + (1 << (k - 1))
print("  k        N  dim   space  /N     mono   /N    Yates/N  floor 3N/4   (k - space/N*2)/sqrt(k)")
for k in range(3, 42, 2):
    r = (k - 1) // 2; N = 1 << k
    s = space(r, k); m = mono(r, k)
    print(f"{k:3d} {N:>13d}  N/2 {s/N:8.4f}  {m/N:8.4f}  {k/2:5.1f}   0.75   c = {(k - 2*s/N)/sqrt(k):.4f}   c_mono = {(k - 2*m/N)/sqrt(k):.4f}"
          + (f"   exact: space {s}, mono {m}" if k <= 9 else ""))
print()
print("all degrees at 16 and 32 points: degree, dimension, space, mono, floor max(N - n, N - n/2 if dual distance >= 5)")
for k in (4, 5, 6):
    N = 1 << k
    for r in range(0, k + 1):
        n = sum(comb(k, j) for j in range(r + 1))
        dd = 2 ** (r + 1) if r < k else None
        fl = N - n if (dd is None or dd < 5) else -(-(2 * N - n) // 2)
        print(f"  k {k} degree {r} dim {n:3d} space {space(r,k):4d} mono {mono(r,k):4d} floor {fl:4d}  dual distance {dd}")
