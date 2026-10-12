# u-4-zdz / refl.py : first look at NON-triangular answers.  B D B^T = H with B = Z Q, Q a reflection of the form D:
#     Q = I - 2 u (u^T D^-1) / (u^T D^-1 u),   Q D Q^T = D   (checked exactly for every u used).
# u runs over the vectors with at most S non-zeros, entries from VALS.  Reported: non-zeros of B (subset sums: 3^k), how many u
# give fewer, the sparsest B.  Exact fractions.   usage: refl.py K S
import sys, itertools
from fractions import Fraction as F
def pop(x): return bin(x).count('1')
K = int(sys.argv[1]); S = int(sys.argv[2]); N = 1 << K
VALS = [F(1), F(-1), F(2), F(-2), F(1, 2), F(-1, 2)]
Z = [[F(int(t & s == t)) for t in range(N)] for s in range(N)]
D = [F((-2) ** pop(j)) for j in range(N)]
H = [[F((-1) ** pop(s & t)) for t in range(N)] for s in range(N)]
def nnz(M): return sum(1 for r in M for x in r if x != 0)
hist = {}; best = None; tried = 0
for size in range(2, S + 1):
    for supp in itertools.combinations(range(N), size):
        for vals in itertools.product(VALS, repeat=size):
            if vals[0] not in (F(1), F(2), F(1, 2)): continue      # u and -u give the same Q
            u = [F(0)] * N
            for i, v in zip(supp, vals): u[i] = v
            w = [u[i] / D[i] for i in range(N)]; c = sum(u[i] * w[i] for i in range(N))
            if c == 0: continue
            tried += 1
            # B = Z - 2 (Z u) w^T / c
            zu = [sum(Z[s][i] * u[i] for i in supp) for s in range(N)]
            B = [[Z[s][t] - 2 * zu[s] * w[t] / c for t in range(N)] for s in range(N)]
            n = nnz(B); hist[n] = hist.get(n, 0) + 1
            if best is None or n < best[0]:
                ok = all(sum(B[s][j] * D[j] * B[t][j] for j in range(N)) == H[s][t] for s in range(N) for t in range(N))
                best = (n, u, B, ok)
print('N=%d: reflections tried %d (support <= %d, entries from 1, -1, 2, -2, 1/2, -1/2); non-zeros of subset sums: %d' % (N, tried, S, 3 ** K))
print('histogram of non-zeros of B = Z Q:', sorted(hist.items())[:12], '...')
n, u, B, ok = best
print('sparsest: %d non-zeros, u = %s, B D B^T = H exactly: %s' % (n, [str(x) for x in u], ok))
for r in B: print('    ', ' '.join('%5s' % str(x) for x in r))
