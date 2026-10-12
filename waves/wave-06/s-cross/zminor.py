# s-cross hybrid 4: the volume budget of SUBSET SUMS. Z[S][T] = 1 if T inside S. det Z = 1, but its minors are not all 1.
# Morgenstern in the primitive scaling (pmeter.py) bounds EVERY minor of the output matrix, so a circuit for Z whose gates are
# all u + v or u - v has at least log2(largest minor of Z) gates. Exact whole numbers (fraction-free elimination).
import sys, itertools, random, math
def det(M):
    n = len(M); M = [r[:] for r in M]; prev = 1; sign = 1
    for i in range(n):
        if M[i][i] == 0:
            for r in range(i+1, n):
                if M[r][i]: M[i], M[r] = M[r], M[i]; sign = -sign; break
            else: return 0
        for r in range(i+1, n):
            for c in range(i+1, n): M[r][c] = (M[r][c]*M[i][i] - M[r][i]*M[i][c]) // prev
        prev = M[i][i]
    return sign*M[n-1][n-1] if n else 1
def Z(k): return [[1 if (t & s) == t else 0 for t in range(1 << k)] for s in range(1 << k)]
k = int(sys.argv[1]); N = 1 << k; z = Z(k)
if k <= 3:
    best = 0; arg = None
    for j in range(1, N+1):
        for R in itertools.combinations(range(N), j):
            for C in itertools.combinations(range(N), j):
                d = abs(det([[z[r][c] for c in C] for r in R]))
                if d > best: best = d; arg = (R, C)
    print('k=%d exhaustive: largest minor of Z = %d  (log2 = %.3f), rows %s cols %s' % (k, best, math.log2(best), arg[0], arg[1]))
else:
    rng = random.Random(int(sys.argv[2])); import time; t0 = time.time(); best = 0; arg = None
    # level blocks first: rows of size a, columns of size b (the incidence matrices between two levels), then hill-climb on unions
    pc = [bin(v).count('1') for v in range(N)]
    while time.time() - t0 < float(sys.argv[3]):
        j = rng.randint(2, N-1); R = rng.sample(range(N), j); C = rng.sample(range(N), j)
        d = abs(det([[z[r][c] for c in C] for r in R])); 
        for it in range(400):
            R2, C2 = R[:], C[:]
            if rng.random() < 0.5: 
                cand = [v for v in range(N) if v not in R2]; R2[rng.randrange(j)] = rng.choice(cand)
            else:
                cand = [v for v in range(N) if v not in C2]; C2[rng.randrange(j)] = rng.choice(cand)
            d2 = abs(det([[z[r][c] for c in C2] for r in R2]))
            if d2 >= d: R, C, d = R2, C2, d2
        if d > best: best = d; arg = (sorted(R), sorted(C)); print('k=%d search: minor %d (log2 %.3f) size %d rows %s cols %s' % (k, best, math.log2(best), j, arg[0], arg[1]), flush=True)
    print('k=%d search ended: largest minor found %d, log2 = %.3f  (a lower bound on the largest minor)' % (k, best, math.log2(best)))
