# x-7-rotate120 / circle.py : exact.  A combination a*S + b*S R + c*S R^2 of the three mirrors of a triple is again a mirror
# when a + b + c = 1 and a^2 + b^2 + c^2 - ab - bc - ca = 1 (a rational circle through the three).  Checked at 4, 16, 64 points.
from fractions import Fraction as Fr
def pop(v): return bin(v).count('1')
def build(n):
    k = 2 * n; N = 1 << k
    Q = lambda x: sum(((x >> (2 * i)) & 1) * ((x >> (2 * i + 1)) & 1) for i in range(n)) & 1
    sw = lambda x: sum((((x >> (2 * i)) & 1) << (2 * i + 1)) | (((x >> (2 * i + 1)) & 1) << (2 * i)) for i in range(n))
    H = [[Fr((-1) ** pop(x & sw(y))) for y in range(N)] for x in range(N)]
    D = [[Fr((-1) ** Q(x)) if x == y else Fr(0) for y in range(N)] for x in range(N)]
    return N, H, D
def mul(A, B):
    Bt = list(zip(*B)); return [[sum(a * b for a, b in zip(r, c) if a and b) for c in Bt] for r in A]
for n in (1, 2, 3):
    N, H, D = build(n); I = [[Fr(int(i == j)) for j in range(N)] for i in range(N)]; s = Fr(1, 1 << n)
    R = [[x * s for x in r] for r in mul(D, H)]; R2 = mul(R, R)
    S0, S1, S2 = D, mul(D, R), mul(D, R2)
    for (a, b, c) in ((Fr(2, 3), Fr(2, 3), Fr(-1, 3)), (Fr(6, 7), Fr(3, 7), Fr(-2, 7)), (Fr(1, 2), Fr(1, 2), Fr(0))):
        ok_param = (a + b + c == 1) and (a * a + b * b + c * c - a * b - b * c - c * a == 1)
        S = [[a * S0[i][j] + b * S1[i][j] + c * S2[i][j] for j in range(N)] for i in range(N)]
        print('N=%d (a,b,c)=(%s,%s,%s) on the circle: %s ; S^2 = 1: %s ; S R S = R^-1: %s' % (N, a, b, c, ok_param, mul(S, S) == I, mul(mul(S, R), S) == R2))
