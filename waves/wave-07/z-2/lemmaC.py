# z-2: own check of the "forced step" of x-4 lemma C, exhaustive over SIGN-valued p, q (the hand argument in z-2.md
# shows first that p and q must be sign-valued in the case e = +1 once N >= 32).
# Case e = +1: for all x, y with x + y outside {0, m1, m2, m1+m2}:  p(x) = chi(y)  or  q(y) = psi(x),
# chi(y) = (-1)^(m1.y), psi(x) = (-1)^(x.m2); p invariant under x -> x + m1, q under y -> y + m2.
# Count the solutions for EVERY pair m1, m2 (m1 = m2 included) with m1.m2 = 0, plain labelling (dot product).
import numpy as np, sys

def dot(x, y): return bin(x & y).count('1') & 1

def count(k, m1, m2, want_list=False):
    N = 1 << k
    # all m1-invariant sign functions p, as bit masks of {x : p(x) = -1}
    reps = [x for x in range(N) if x < (x ^ m1)]
    idx = np.arange(1 << len(reps), dtype=np.uint64)
    masks = np.zeros(1 << len(reps), dtype=np.uint64)
    for i, x in enumerate(reps):
        bit = np.uint64((1 << x) | (1 << (x ^ m1)))
        masks |= ((idx >> np.uint64(i)) & np.uint64(1)) * bit
    excl = {0, m1, m2, m1 ^ m2}
    ok = {}
    for y in range(N):
        chi_minus = dot(m1, y)            # chi(y) = -1 ?
        for s in (0, 1):                  # s = 1 means q(y) = -1
            # x off the diagonals with psi(x) != q(y) must have p(x) = chi(y)
            S = 0
            for x in range(N):
                if (x ^ y) in excl: continue
                if dot(x, m2) != s: S |= 1 << x
            S = np.uint64(S)
            target = S if chi_minus else np.uint64(0)
            ok[(y, s)] = (masks & S) == target
    total = np.ones(len(masks), dtype=np.int64)
    yreps = [y for y in range(N) if y < (y ^ m2)]
    for y in yreps:
        a = (ok[(y, 0)] & ok[(y ^ m2, 0)]).astype(np.int64) + (ok[(y, 1)] & ok[(y ^ m2, 1)]).astype(np.int64)
        total *= a
    n = int(total.sum())
    sols = []
    if want_list:
        for j in np.nonzero(total)[0]:
            sols.append(int(masks[j]))
    return n, sols

for k in (4, 5):
    N = 1 << k
    hist = {}
    npairs = 0
    bad = 0
    for m1 in range(1, N):
        for m2 in range(1, N):
            if dot(m1, m2): continue
            npairs += 1
            n, sols = count(k, m1, m2, want_list=True)
            key = (n, m1 == m2)
            hist[key] = hist.get(key, 0) + 1
            # are the solutions the two predicted ones p = eta psi ?
            psi_mask = sum(1 << x for x in range(N) if dot(x, m2))
            pred = {psi_mask, (N and ((1 << N) - 1)) ^ psi_mask}
            if k == 5 and set(sols) != pred: bad += 1
    print(f"N={N}: pairs m1, m2 with m1.m2 = 0: {npairs};  (number of solutions, m1 == m2) -> how many pairs: {sorted(hist.items())}"
          + (f";  pairs whose solution set is not exactly p = +-psi: {bad}" if k == 5 else ""))

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
