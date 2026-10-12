# r-1: the two ingredients of p-8's lemma, checked exactly in whole numbers.
import itertools, sys
# (i) Parseval count. Cherries = the N/2 cosets of <d>; rows of one class differ by z in the subgroup perpendicular to d; on the
#     cherries these z act as the N/2 characters of the quotient group. For EVERY set W of wrong cherries with |W| >= N/4:
#     how many z have |sum over W of chi_z| > |W|/2 ?  The lemma says fewer than 8.
for N in (16, 32):
    m = N // 2; worst = 0; worst_any = 0; sets = 0
    chi = [[(-1) ** bin(z & j).count('1') for j in range(m)] for z in range(m)]
    for Wm in range(1, 1 << m):
        w = bin(Wm).count('1')
        js = [j for j in range(m) if Wm >> j & 1]
        cnt = sum(1 for z in range(m) if 2 * abs(sum(chi[z][j] for j in js)) > w)
        if 4 * w >= N: sets += 1; worst = max(worst, cnt)
    print("(i) N =", N, ":", sets, "sets W with |W| >= N/4; largest number of z with |sum| > |W|/2 :", worst, " (lemma: at most 7)")
    sys.stdout.flush()
# (ii) the cherry invariant on a real letter: the 45-rectangle design at 16 points (22 single-column rectangles).
#      phi_j(row) = M(y,a) - M(y,b) on column cherry {a,b}; rows consecutive around the row tree; each rectangle is passed twice.
def rev(x, k): return int(format(x, '0%db' % k)[::-1], 2)
b = lambda z, i: z >> i & 1
k = 4; N = 16
r = lambda y: (-1) ** (b(y, 0) * (1 + b(y, 3))); c = lambda x: (-1) ** (b(x, 0) * b(x, 3))
M = [[r(y) * c(rev(x, k)) * (-1) ** bin(y & rev(x, k)).count('1') for x in range(N)] for y in range(N)]
phi = [tuple(M[y][2 * j] - M[y][2 * j + 1] for j in range(N // 2)) for y in range(N)]
dist = [[sum(1 for j in range(N // 2) if phi[y][j] != phi[z][j]) for z in range(N)] for y in range(N)]
# best order of the leaves compatible with the row tree (swap children at will): dynamic programme on (first leaf, last leaf)
def best(lo, hi):
    if hi - lo == 1: return {(lo, lo): 0}
    mid = (lo + hi) // 2; A = best(lo, mid); B = best(mid, hi); out = {}
    for (a, a2), va in A.items():
        for (b2, bb), vb in B.items():
            v = va + dist[a2][b2] + vb
            for key in ((a, bb), (bb, a)):
                if out.get(key, -1) < v: out[key] = v
    return out
tour = max(v + dist[a][z] for (a, z), v in best(0, N).items())
nat = sum(dist[y][(y + 1) % N] for y in range(N))
print("(ii) 45-design: single-column rectangles >= (sum of phi-distances around the tree)/2 =", nat / 2, "in address order,", tour / 2, "in the best order; the design has 22")
