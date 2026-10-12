# v-2: the volume bound for subset sums as numbers. E = E|k - 2J| exact (J binomial(k, 1/2)); lphi = log2(golden ratio) FLOAT.
# per point (divide by N):  ceiling = lphi*E/2 (no minor of Z is larger: singular values of a submatrix are dominated)
#   minor floor  = max over cut j0 of [ lphi * sum_{j<=j0} C(k,j)(k-2j) - log2 C(N, r) ] / N      (g-4's count, r = sum_{j<=j0} C(k,j))
#   volume floor = the same with (1/2) log2 C(N, r)   (r wires against all N inputs; Raz / Buergisser-Lotz form)
from fractions import Fraction as F
from math import comb, log2, sqrt, pi, lgamma, log
lphi = log2((1 + sqrt(5))/2)
def l2comb(N, r):
    if N < 5000: return log2(comb(N, r))
    return (lgamma(N + 1) - lgamma(r + 1) - lgamma(N - r + 1))/log(2)
print('lphi = %.5f, lphi*sqrt(2/pi)/2 = %.5f' % (lphi, lphi*sqrt(2/pi)/2))
print('  k   E|k-2J|  E/sqrt(2k/pi)  ceiling   minor floor  volume floor  g-4 formula 0.277 sqrt(k) - 1   corners/pt >= (coef 1 | 2 | 4)')
first = {}
for k in list(range(2, 41)) + [52, 64, 82, 100, 117, 118, 128, 256, 512, 1000]:
    N = 1 << k; E = F(sum(comb(k, j)*abs(k - 2*j) for j in range(k + 1)), N)
    best_m = best_v = -9e9; acc = 0; r = 0
    for j0 in range(0, (k - 1)//2 + 1):
        acc += comb(k, j0)*(k - 2*j0); r += comb(k, j0)
        lc = l2comb(N, r) if k <= 40 else float(N)       # for k > 40 use log2 C(N, r) <= N
        best_m = max(best_m, (lphi*acc - lc)/N); best_v = max(best_v, (lphi*acc - lc/2)/N)
    ceil_ = lphi*float(E)/2; g4 = 0.277*sqrt(k) - 1
    for name, val in (('minor>0', best_m > 0), ('minor>1', best_m > 1), ('minor>2', best_m > 2), ('vol>0', best_v > 0), ('vol>1', best_v > 1), ('g4 formula above true minor floor', g4 > best_m + 1e-12)):
        if val and name not in first: first[name] = k
    if k <= 16 or k in (20, 30, 40, 52, 64, 82, 100, 117, 118, 128, 256, 512, 1000):
        print('%4d  %8.4f   %.5f     %7.4f   %8.4f     %8.4f      %8.4f            %7.3f | %7.3f | %7.3f' % (k, float(E), float(E)/sqrt(2*k/pi), ceil_, best_m, best_v, g4, best_m - 1, best_m/log2(3) - 1, best_m/log2(5) - 1))
print('first k in the list where each holds:', first)
