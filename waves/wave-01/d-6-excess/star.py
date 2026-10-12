# d-6-excess: the star (one helper, every output one flip away): J - 2I on n points, 2n - 1 gates, excess 1.
# exact determinant, bits of volume per gate; and the same count for the Gray tree (excess 0) and for the textbook.
from fractions import Fraction
from math import log2
def det(M):
    M = [[Fraction(x) for x in r] for r in M]; n = len(M); d = Fraction(1)
    for c in range(n):
        p = next((r for r in range(c, n) if M[r][c] != 0), None)
        if p is None: return 0
        if p != c: M[c], M[p] = M[p], M[c]; d = -d
        d *= M[c][c]
        for r in range(c+1, n):
            f = M[r][c] / M[c][c]
            for k in range(c, n): M[r][k] -= f * M[c][k]
    return int(d)
print("n  |det(J-2I)|  2^(n-1)(n-2)  gates  bits  bits/gate   Hadamard bound n^(n/2) bits")
for n in range(3, 13):
    M = [[1 - 2*(i == j) for j in range(n)] for i in range(n)]
    d = abs(det(M))
    print("%2d %10d %10d %6d %7.3f %7.3f %12.3f" % (n, d, 2**(n-1)*(n-2), 2*n-1, log2(d), log2(d)/(2*n-1), n/2*log2(n)))
print("zero-excess (Gray) matrix: bits n-1 in 2n-2 gates: 0.5 bits per gate at any n")
print("textbook transform: (N/2) log2 N bits in N log2 N gates: 0.5;  7-gate brick: 4 bits in 7 gates: %.3f" % (4/7))
print("floor for words of sign-matrix layers made of stars of size b: (N/2) log2 N / max_b bits-per-gate")
best = max((log2(2**(b-1)*(b-2))/(2*b-1), b) for b in range(3, 40))
print("  best star size b = %d, %.4f bits per gate -> at least %.4f N log2 N gates (the 4-point star gives 7/8 = 0.875)" % (best[1], best[0], 0.5/best[0]))
