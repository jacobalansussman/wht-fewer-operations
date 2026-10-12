# k-cross: the 19-gate identity read in the exponent. Kernel entries t^(Hamming distance); exact (powers of t = 2 and t = 3).
from fractions import Fraction as Fr
exc = {2:{7,1}, 3:{5,3}, 7:{7,6,3,4}, 1:{7,6,2,5}, 4:{7,1,2,3,4,5}, 5:{5,3,0,1,6,7}, 6:{5,4,1,6}, 0:{5,4,0,7}}
sig = (0, 1, 2, 3, 7, 6, 5, 4); pi = {2: 1, 3: 4, 7: 0, 1: 2, 6: 5, 0: 7, 4: 3, 5: 6}
def lg(v, t):
    v = Fr(v); n = 0
    while v > 1: v /= t; n += 1
    while v < 1: v *= t; n -= 1
    assert v == 1; return n
res = []
for t in (2, 3):
    Kp = [[Fr(t)**bin(pi[j] ^ sig[i]).count('1') for i in range(8)] for j in range(8)]
    c = [None]*8
    for i in range(8):
        if i not in (1, 7): c[i] = Kp[2][i]
    lam = Kp[2][0] / Kp[3][0]; c[1] = lam*Kp[3][1]; c[7] = lam*Kp[3][7]
    a = [next(iter({Kp[j][i] / c[i] for i in range(8) if i not in exc[j]})) for j in range(8)]
    q = [lg(v, t) for v in c]; qa = [lg(v, t) for v in a]
    m = [[bin(pi[j] ^ sig[i]).count('1') - q[i] - qa[j] for i in range(8)] for j in range(8)]
    res.append((q, qa, m))
    print("t =", t, " centre = t^q, q over kernel columns 0..7:", [q[sig.index(x)] for x in range(8)], "  row scaling = t^q', q' over kernel rows 0..7:", [qa[[pi[j] for j in range(8)].index(y)] for y in range(8)])
print("same exponents for t = 2 and t = 3:", res[0] == res[1])
m = res[0][2]
from collections import Counter
print("values of  distance(x,y) - q(x) - q'(y)  over the 64 cells:", sorted(Counter(v for r in m for v in r).items()))
for r in m: print("   ", " ".join("%2d" % v for v in r))
print("cells with the value 2 modulo 4:", sum(1 for r in m for v in r if v % 4 == 2), " (the transform has 32 cells with -1)")
