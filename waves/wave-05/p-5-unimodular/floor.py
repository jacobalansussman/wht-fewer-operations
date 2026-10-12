# floor.py: (b) the singular-value floor for the powers of K = [[1,1],[1,2]] and of Z, and three other meters. Floating point
# for logarithms only (the inequality is derived by hand; the numbers are for reading, 1e-9 accuracy is irrelevant).
from math import comb, log2, sqrt, lgamma, log
phi = (1 + sqrt(5)) / 2
def lg2comb(n, r): return (lgamma(n+1) - lgamma(r+1) - lgamma(n-r+1)) / log(2)
def floor(k, per):  # singular values 2^(per*(k-2j)), multiplicity C(k,j).  max over r of sum(top r logs) - log2 C(N,r)
    N = 2**k; best = 0.0; acc = 0.0; r = 0
    for j in range(k + 1):
        e = per * (k - 2*j)
        if e <= 0: break
        acc += comb(k, j) * e; r += comb(k, j)
        best = max(best, acc - lg2comb(N, r))
    return best
print("k  N  floorK/N  floorZ/N  0.5537*sqrt(k)  textbook/N=k  diagonal cost of Lambda /N   quasi-entropy |Phi|/N: K, H, Z")
for k in [1,2,3,4,5,6,8,10,12,16,20,24,32,48,64,128,256]:
    N = 2**k
    fK = floor(k, 2*log2(phi)) ; fZ = floor(k, log2(phi))
    diag = sum(comb(k, j) * abs(k - 2*j) for j in range(k + 1)) * 2 * log2(phi) / N
    print("%4d %8.3g  %7.3f  %7.3f  %7.3f  %5d  %8.3f   %d %d %d" % (k, N, fK / N, fZ / N, 2*log2(phi)*sqrt(2*k/3.14159265)/2, k, diag, 2*k, k, 0))
