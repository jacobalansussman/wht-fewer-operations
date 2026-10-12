# Hybrid 2: where the volume lives. Largest minor (sub-determinant) of the subset-sum matrix Z against the transform H.
import itertools, random
def bareiss(M):
    M = [r[:] for r in M]; n = len(M); sign = 1; prev = 1
    for i in range(n):
        p = next((r for r in range(i, n) if M[r][i]), None)
        if p is None: return 0
        if p != i: M[i], M[p] = M[p], M[i]; sign = -sign
        for r in range(i + 1, n):
            for c in range(i + 1, n):
                M[r][c] = (M[r][c] * M[i][i] - M[r][i] * M[i][c]) // prev
        prev = M[i][i]
    return sign * M[n - 1][n - 1]
def Z(k): return [[1 if (x & y) == x else 0 for x in range(1 << k)] for y in range(1 << k)]
def H(k): return [[(-1) ** bin(x & y).count('1') for x in range(1 << k)] for y in range(1 << k)]
def exhaustive(M):
    n = len(M); best = {}
    for m in range(1, n + 1):
        b = 0
        for R in itertools.combinations(range(n), m):
            sub = [M[r] for r in R]
            for C in itertools.combinations(range(n), m):
                d = abs(bareiss([[row[c] for c in C] for row in sub]))
                if d > b: b = d
        best[m] = b
    return best
for k in ():
    print(f"k={k} Z: largest |minor| by order, exhaustive:", exhaustive(Z(k)))
    print(f"k={k} H: largest |minor| by order, exhaustive:", exhaustive(H(k)))
# k = 4: hill climb for Z (a lower bound on the largest minor), exact determinants throughout
import sys; kk = int(sys.argv[1]); random.seed(7); M = Z(kk); n = 1 << kk; best = (0, None)
def val(R, C): return abs(bareiss([[M[r][c] for c in C] for r in R])) if R else 1
for restart in range(400):
    m = random.randint(4, n - 4)
    R = random.sample(range(n), m); C = random.sample(range(n), m); v = val(R, C)
    for step in range(int(sys.argv[2])):
        R2, C2 = R[:], C[:]; mv = random.random()
        if mv < 0.4:
            i = random.randrange(len(R2)); cand = [r for r in range(n) if r not in R2]
            if cand: R2[i] = random.choice(cand)
        elif mv < 0.8:
            i = random.randrange(len(C2)); cand = [c for c in range(n) if c not in C2]
            if cand: C2[i] = random.choice(cand)
        elif mv < 0.9 and len(R2) < n:
            R2.append(random.choice([r for r in range(n) if r not in R2])); C2.append(random.choice([c for c in range(n) if c not in C2]))
        elif len(R2) > 2:
            R2.pop(random.randrange(len(R2))); C2.pop(random.randrange(len(C2)))
        v2 = val(R2, C2)
        if v2 >= v: R, C, v = R2, C2, v2
    if v > best[0]: best = (v, (sorted(R), sorted(C)))
print("k=4 Z: largest |minor| found by hill climbing (lower bound only):", best[0], "order", len(best[1][0]), best[1])
print("k=4 H: determinant", 16 ** 8, "= 2^32; k=3 H: 8^4 = 4096")
