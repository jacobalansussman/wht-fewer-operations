# u-4-zdz / ldl.py : "yes, and" number 1.  H = Z D Z^T is ONE triangular factorisation of the transform: the one you get by
# eliminating the addresses in an order compatible with inclusion.  Eliminate in ANY order p of the addresses:
#     (H in the order p) = L D L^T,  L lower triangular with ones on the diagonal, D diagonal   (unique when it exists).
# Then the transform costs at most 2 * cost(L) gates (G) (L, free scalings, L^T by the transposed circuit), and also at most
# 2 * cost(L^-1) because H^-1 = H / N.   Question: is subset sums the SPARSEST such L, or is there an order with fewer non-zeros?
# Exact fractions.  usage: ldl.py all K | ldl.py maps K | ldl.py anneal K steps seed
import sys, itertools, random
from fractions import Fraction as F
def pop(x): return bin(x).count('1')
def ldl(p):
    n = len(p); A = [[F((-1) ** pop(p[i] & p[j])) for j in range(n)] for i in range(n)]
    L = [[F(int(i == j)) for j in range(n)] for i in range(n)]; D = []
    for c in range(n):
        d = A[c][c]
        if d == 0: return None
        D.append(d)
        for i in range(c + 1, n):
            if A[i][c] != 0:
                f = A[i][c] / d; L[i][c] = f
                for j in range(c + 1, n): A[i][j] -= f * A[c][j]
    return L, D
def inv_unit_lower(L):
    n = len(L); X = [[F(int(i == j)) for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(i):
            X[i][j] = -sum(L[i][t] * X[t][j] for t in range(j, i))
    return X
def off(L): return sum(1 for i in range(len(L)) for j in range(i) if L[i][j] != 0)
def score(p):
    r = ldl(p)
    if r is None: return None
    L, D = r; return off(L), off(inv_unit_lower(L)), L, D
mode = sys.argv[1]; K = int(sys.argv[2]); N = 1 << K
zoff = 3 ** K - 2 ** K
print('N=%d  subset sums: off-diagonal non-zeros %d, Yates %d gates' % (N, zoff, N // 2 * K))
if mode == 'all':
    hist = {}; best = None; none = 0
    for p in itertools.permutations(range(N)):
        r = score(p)
        if r is None: none += 1; continue
        a, b = r[0], r[1]; m = min(a, b); hist[m] = hist.get(m, 0) + 1
        if best is None or m < best[0]: best = (m, p, a, b, r[2], r[3])
    print('orders with a zero pivot (no factorisation):', none)
    print('histogram of min(off-diagonal non-zeros of L, of L^-1):', sorted(hist.items()))
    m, p, a, b, L, D = best
    print('best: %d  order %s  off(L)=%d off(L^-1)=%d  D=%s' % (m, p, a, b, [str(d) for d in D]))
    for row in L: print('   ', ' '.join('%5s' % str(x) for x in row))
elif mode == 'maps':                      # orders p[i] = g(i), g an invertible K x K matrix of bits (an address map)
    hist = {}; best = None; none = 0; cnt = 0
    for cols in itertools.product(range(1, N), repeat=K):
        img = [0] * N; ok = True
        for i in range(N):
            v = 0
            for b in range(K):
                if i >> b & 1: v ^= cols[b]
            img[i] = v
        if len(set(img)) < N: continue
        cnt += 1; r = score(img)
        if r is None: none += 1; continue
        a, b = r[0], r[1]; m = min(a, b); hist[m] = hist.get(m, 0) + 1
        if best is None or m < best[0]: best = (m, img, a, b, r[2], r[3], cols)
    print('address maps:', cnt, ' with a zero pivot:', none)
    print('histogram of min(off(L), off(L^-1)):', sorted(hist.items()))
    m, p, a, b, L, D, cols = best
    print('best: %d  map columns %s  order %s  off(L)=%d off(L^-1)=%d  D=%s' % (m, cols, p, a, b, [str(d) for d in D]))
else:
    steps = int(sys.argv[3]); rnd = random.Random(int(sys.argv[4]))
    p = list(range(N)); rnd.shuffle(p)
    def val(p):
        r = score(p); return None if r is None else min(r[0], r[1])
    cur = val(p)
    while cur is None: rnd.shuffle(p); cur = val(p)
    best = (cur, list(p)); T = 3.0
    import math
    for s in range(steps):
        i, j = rnd.sample(range(N), 2); p[i], p[j] = p[j], p[i]; v = val(p)
        if v is not None and (v <= cur or rnd.random() < math.exp((cur - v) / T)): cur = v
        else: p[i], p[j] = p[j], p[i]
        if cur < best[0]: best = (cur, list(p))
        T = max(0.3, T * 0.9995)
    r = score(best[1])
    print('anneal seed %s steps %d: best min(off(L), off(L^-1)) = %d  off(L)=%d off(L^-1)=%d order %s' % (sys.argv[4], steps, best[0], r[0], r[1], best[1]))
    print('   D =', [str(d) for d in r[3]])
