#!/usr/bin/env python3
"""x-9-growinghubs/facts.py: exact checks of the hand-derived facts of x-9.md (Fractions; Gaussian rationals as pairs).
The 2-bit cell: 4 numbers on the four quarters (L1, L2, R1, R2), written as a 2x2 matrix [[L1, L2], [R1, R2]].
Product wire (x, y) = (1, x, y, x*y): slope x on the lower bit, y on the upper bit.  Rank 1 <=> det = 0."""
from fractions import Fraction as F
import itertools, random
random.seed(1)
def det(w): return w[0] * w[3] - w[1] * w[2]
def polar(u, w): return u[0] * w[3] + u[3] * w[0] - u[1] * w[2] - u[2] * w[1]      # det(u+w) - det(u) - det(w)
def reflect(M, W): return tuple(W[i] - polar(W, M) / det(M) * M[i] for i in range(4))   # W - B(W,M)/Q(M) * M
outs = {(a, b): (F(1), F(a), F(b), F(a * b)) for a in (1, -1) for b in (1, -1)}
# 1. starting fact: (1,1,1,1) - M_t = (0, 0, 1-t, 1+t)
for t in [F(2), F(-3), F(1, 2), F(5, 7), F(-9, 4)]:
    M = (F(1), F(1), t, -t)
    assert tuple(o - m for o, m in zip(outs[(1, 1)], M)) == (0, 0, 1 - t, 1 + t)
    s = (1 + t) / (1 - t)
    # all four outputs: witness = reflection of the output in M; it is rank 1; it lies in ONE half; its slope is s or 1/s
    wit = {}
    for key, O in outs.items():
        W = reflect(M, O)
        assert det(W) == 0 and W != O
        half = 'R' if W[0] == 0 and W[1] == 0 else 'L' if W[2] == 0 and W[3] == 0 else '?'
        sl = (W[3] / W[2]) if half == 'R' else (W[1] / W[0])
        wit[key] = (half, sl)
        # and the output really is one gate from M and the witness
        al = None
        for i, j in itertools.combinations(range(4), 2):
            d = M[i] * W[j] - M[j] * W[i]
            if d:
                al = (O[i] * W[j] - O[j] * W[i]) / d; be = (M[i] * O[j] - M[j] * O[i]) / d; break
        assert all(al * M[q] + be * W[q] == O[q] for q in range(4))
    assert wit[(1, 1)] == ('R', s) and wit[(1, -1)] == ('R', 1 / s) and wit[(-1, 1)] == ('L', s) and wit[(-1, -1)] == ('L', 1 / s), wit
print('1. [ok] hub M_t = (1,1,t,-t): the four outputs are one gate each; witnesses: slope s=(1+t)/(1-t) and 1/s on R (outputs a,+ and a,-), s and 1/s on L (outputs b,+ and b,-); witness = reflection of the output in M for the form det')
# 2. the reflection swaps the two rulings: general hub (1,p,t,tq)
for _ in range(200):
    p, q, t, s = [F(random.randint(-9, 9), random.randint(1, 9)) for _ in range(4)]
    if p == q or t == 0 or s == p: continue
    M = (F(1), p, t, t * q); W = (F(0), F(0), F(1), s)                # witness: slope s on R
    O = reflect(M, W); assert det(O) == 0 and O[0] != 0
    assert O[1] / O[0] == p and O[2] / O[0] == t * (q - s) / (p - s)  # output = (lower slope p, upper slope t(q-s)/(p-s))
    if s != q:
        W = (F(1), s, F(0), F(0)); O = reflect(M, W)                  # witness: slope s on L
        assert det(O) == 0
        if O[0] != 0: assert O[1] / O[0] == q and O[2] / O[0] == t * (s - q) / (s - p)
print('2. [ok] general hub (1,p,t,tq): witness of slope s on R -> product (p, t(q-s)/(p-s)); on L -> product (q, t(s-q)/(s-p))  (200 random rational cases)')
# 3. t = +-1: the four witnesses are the four corners (quarter pieces)
for t in (F(1), F(-1)):
    M = (F(1), F(1), t, -t); c = set()
    for O in outs.values():
        W = reflect(M, O); c.add(tuple(i for i in range(4) if W[i]))
    assert c == {(0,), (1,), (2,), (3,)}
print('3. [ok] t = +1 or -1: the witnesses of the four outputs are the four single quarters (M is the 2x2 transform written as 4 numbers)')
# 4. the orbit: Cayley map of order 4; fixed points +-i
def cay(t): return (1 + t) / (1 - t)
for t in [F(2), F(3), F(1, 3), F(-5, 2)]:
    o = [t]
    for _ in range(4): o.append(cay(o[-1]))
    assert o[4] == t and o[2] == -1 / t and o[3] == (t - 1) / (t + 1)
# Gaussian: (1+i)/(1-i) = i
num = complex(1, 1); den = complex(1, -1); assert num / den == complex(0, 1)
print('4. [ok] t -> (1+t)/(1-t) has order 4: t, s, -1/t, -1/s;  (1+i)/(1-i) = i (floating check of an exact identity: (1+i)^2 = 2i)')
print('   reading: -1/t is the hub with L and R exchanged, (y_b on R) - t (y_a on L); its witness slope is -1/s. The orbit of four = {hub, witness, mirror hub, mirror witness}.')
# 5. support lemma, exhaustive over a small field: for ANY M and two different rows O1, O2, the two witnesses O_i - a_i M (a_i != 0) have supports with union >= N/2
def rowsH(N): return [tuple(-1 if bin(w & x).count('1') & 1 else 1 for x in range(N)) for w in range(N)]
for N, p in ((4, 5), (4, 7), (8, 3), (8, 5)):
    R = rowsH(N); worst = N; cnt = 0
    for M in itertools.product(range(p), repeat=N):
        if not any(M): continue
        # for each row: the set of alphas and supports
        sup = []
        for O in R:
            best = []
            for al in range(1, p):
                best.append(frozenset(i for i in range(N) if (O[i] - al * M[i]) % p))
            sup.append(best)
        for i in range(N):
            for j in range(i + 1, N):
                for A in sup[i]:
                    for B in sup[j]:
                        u = len(A | B); cnt += 1
                        if u < worst: worst = u
    assert worst >= N // 2, (N, p, worst)
    print('5. [ok] support lemma, N=%d modulo %d: over all %d vectors M and all pairs of rows, least |supp(w1) u supp(w2)| = %d  (N/2 = %d); %d cases' % (N, p, p ** N - 1, worst, N // 2, cnt))
