# g-4-zetalead / more.py : three small exact checks behind statements in g-4.md.  Integers and exact rationals only.
#  1. "Two calls cannot give Z, even with arbitrary relabellings and arbitrary diagonals between and around the calls."
#     Proof in g-4.md reduces it to: the Walsh table W[x][w] = sum over y of (-1)^(x.pi(y) + w.y) of a permutation pi of the
#     addresses never has a row with exactly two non-zero entries (a^2 + b^2 = 4^k has no solution with a, b both non-zero).
#     Checked here for ALL permutations at 4 and 8 points, together with the row sums of squares (= N^2).
#  2. Z is a LIMIT of two-call kernels:  D(1/(2m), 1/2) H D(m+1, m-1) H D(1, 1/m) = [[1, 1/m^2], [1, 1]]  -> Z as m grows.
#  3. One integer three times: k 2^(k-1) = Yates's additions = log2 |det H_N| (Morgenstern's bound for the transform with
#     coefficients bounded by 1) = number of doublings needed to apply D(1,-2) to the k-th power with coefficients bounded by 1.
from fractions import Fraction as Fr
from itertools import permutations
import math

def dot(a, b): return bin(a & b).count("1") & 1

print("== 1. Walsh tables of all permutations ==")
for k in (1, 2, 3):
    N = 1 << k
    sgn = [[1 - 2 * dot(a, b) for b in range(N)] for a in range(N)]
    bad = 0; total = 0; hist = {}
    for pi in permutations(range(N)):
        total += 1
        for x in range(N):
            row = [sum(sgn[x][pi[y]] * sgn[w][y] for y in range(N)) for w in range(N)]
            assert sum(v * v for v in row) == N * N
            nz = sum(1 for v in row if v)
            hist[nz] = hist.get(nz, 0) + 1
            if nz == 2: bad += 1
    print("   N=%d: %6d permutations, rows with exactly two non-zeros: %d ; rows by number of non-zeros: %s" % (N, total, bad, dict(sorted(hist.items()))))
    assert bad == 0
print("   subset sums need k rows with exactly two non-zeros (the one-element sets), so no two-call form exists at these sizes;")
print("   for every k the same follows from a^2 + b^2 = 4^k having only the solutions with a = 0 or b = 0.")
for k in range(1, 13):
    n2 = 4 ** k
    sols = [(a, b) for a in range(1, 2 ** k) for b in [math.isqrt(n2 - a * a)] if b > 0 and a * a + b * b == n2]
    assert not sols
print("   a^2 + b^2 = 4^k with a, b > 0: no solution for k = 1..12 (by search; for all k by descent on the factor 4)")

print("== 2. Z as a limit of two calls ==")
def mm(A, B):
    return [[sum(A[i][t] * B[t][j] for t in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def kron(A, B): return [[a * b for a in ra for b in rb] for ra in A for rb in B]
def kpow(A, k):
    R = [[Fr(1)]]
    for _ in range(k): R = kron(R, A)
    return R
def dg(a, b): return [[Fr(a), Fr(0)], [Fr(0), Fr(b)]]
H = [[Fr(1), Fr(1)], [Fr(1), Fr(-1)]]; Z = [[Fr(1), Fr(0)], [Fr(1), Fr(1)]]
for m in (10, 1000, 10 ** 6):
    K = mm(mm(mm(mm(dg(Fr(1, 2 * m), Fr(1, 2)), H), dg(m + 1, m - 1)), H), dg(1, Fr(1, m)))
    assert K == [[Fr(1), Fr(1, m * m)], [Fr(1), Fr(1)]]
    for k in (1, 2, 3, 4):
        Kk = kpow(K, k); Zk = kpow(Z, k); N = 1 << k
        err = max(abs(Kk[i][j] - Zk[i][j]) for i in range(N) for j in range(N))
        if k == 4: print("   m = %-8d  two-call kernel = [[1, 1/m^2],[1,1]] exactly; k = 4: largest entry of (its 4th power - Z_16) = %s" % (m, err))
print("   so: two calls reach Z in the limit, three calls reach it exactly, and the limit cannot be attained (section 1 above).")

print("== 3. the integer k 2^(k-1) three times ==")
for k in range(1, 11):
    N = 1 << k
    yates = k * N // 2
    logdet = Fr(N * k, 2)                     # det H_N = +- N^(N/2), so log2 |det| = N k / 2
    doublings = sum(math.comb(k, w) * w for w in range(k + 1))   # entry (-2)^w at an address with w ones costs w doublings
    assert yates == logdet == doublings
print("   k = 1..10: Yates's additions = log2 |det H_N| = doublings in D(1,-2)^(tensor k) = k 2^(k-1): True")
print("done")
