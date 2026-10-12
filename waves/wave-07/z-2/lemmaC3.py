# The case m1 = m2 = m with D1 odd under the shift (x-4 left it as a sketch): the algebra used in z-2.md, checked on random data.
import random
from fractions import Fraction
random.seed(7)
def flagf(k, basis, c):
    N = 1 << k
    lvl = [None] * N; s = {0}; lvl[0] = 0
    for j, v in enumerate(basis, 1):
        new = {t ^ v for t in s} - s
        for u in new: lvl[u] = j
        s |= new
    return [sum(c[j] for j in range(lvl[u], k + 1)) for u in range(N)]
def rand_flag_through(k, m):
    while True:
        b = [m] + [random.randrange(1, 1 << k) for _ in range(k - 1)]
        s = {0}; good = True
        for v in b:
            if v in s: good = False; break
            s |= {t ^ v for t in s}
        if good: return b
okall = True
for k in (3, 4, 5):
    N = 1 << k
    for trial in range(20):
        m = random.randrange(1, N)
        f1 = flagf(k, rand_flag_through(k, m), [random.randint(-4, 4) for _ in range(k + 1)])
        f2 = flagf(k, rand_flag_through(k, m), [random.randint(-4, 4) for _ in range(k + 1)])
        d = [0] * N
        for x in range(N):
            if x < (x ^ m):
                d[x] = random.choice([-3, -2, -1, 1, 2, 3]); d[x ^ m] = -d[x]
        a1 = f1[0] - f1[m]; a2 = f2[0] - f2[m]
        G1 = [f1[u] - (a1 if u == 0 else 0) for u in range(N)]
        G2 = [f2[u] - (a2 if u == 0 else 0) for u in range(N)]
        for x in range(N):
            for y in range(N):
                lhs = sum(f1[x ^ z] * d[z] * f2[z ^ y] for z in range(N))
                rhs = (a1 * a2 * d[x] if x == y else 0) + a1 * d[x] * G2[x ^ y] + a2 * G1[x ^ y] * d[y]
                if lhs != rhs: okall = False
print("m1 = m2, D1 odd under the shift: K1 D1 K2 = a1 a2 D1 + a1 D1 J2 + a2 J1 D1 on 60 random cases (8, 16, 32 points):", okall)
