# 8 points.  Class: in-place programs made of butterflies (2 ops) and sum-reflections on q points with signs (2q ops).
# Count (O) below 24 means at most 11 "units" (a butterfly is 1 unit, a q-reflection q units).  By the entropy count (fresh rates,
# see bits.out) only the multisets {6,5} and {5,5,butterfly} can reach 24 bits within 11 units.  Here both are enumerated in full
# (every order, every support, every sign pattern; one reflection normalised by the symmetry of the gate set to rows 0..q-1, all +).
# Floating point with tolerance 1e-9; a hit would be a candidate to replay exactly.  Flat = all entries squared equal 1/8.
import itertools, math
N = 8
def refl(rows, signs):
    q = len(rows); M = [[1.0 if i == j else 0.0 for j in range(N)] for i in range(N)]
    for r, s in zip(rows, signs):
        for r2, s2 in zip(rows, signs): M[r][r2] -= 2.0 * s * s2 / q
    return M
def bfly(a, b):
    c = 1 / math.sqrt(2); M = [[1.0 if i == j else 0.0 for j in range(N)] for i in range(N)]
    M[a][a] = c; M[a][b] = c; M[b][a] = c; M[b][b] = -c
    return M
def mul(A, B): return [[sum(A[i][k] * B[k][j] for k in range(N)) for j in range(N)] for i in range(N)]
def flat(M): return all(abs(x * x - 1.0 / N) < 1e-9 for row in M for x in row)
def phi(M): return -sum(x * x * math.log2(x * x) for row in M for x in row if x * x > 1e-15)
def allrefl(q):
    for rows in itertools.combinations(range(N), q):
        for sg in itertools.product((1, -1), repeat=q - 1):
            yield refl(rows, (1,) + sg)
B = [bfly(a, b) for a, b in itertools.permutations(range(N), 2)]
R5 = list(allrefl(5)); R6 = list(allrefl(6))
n5 = refl((0, 1, 2, 3, 4), (1,) * 5); n6 = refl((0, 1, 2, 3, 4, 5), (1,) * 6)
hits = 0; tried = 0; best = 0.0
for X in R5:                      # {6,5}: two orders
    for P in (mul(n6, X), mul(X, n6)):
        tried += 1; best = max(best, phi(P)); hits += flat(P)
print("{6,5}: products tried %d, flat %d, best entropy %.4f of 24" % (tried, hits, best))
hits = 0; tried = 0; best = 0.0
for X in R5:                      # {5,5,butterfly}: three positions of the butterfly
    A = mul(n5, X); A2 = mul(X, n5)
    for b in B:
        for P in (mul(b, A), mul(A, b), mul(b, A2), mul(A2, b), mul(mul(n5, b), X), mul(mul(X, b), n5)):
            tried += 1; e = phi(P); best = max(best, e); hits += flat(P)
print("{5,5,butterfly}: products tried %d, flat %d, best entropy %.4f of 24" % (tried, hits, best))
