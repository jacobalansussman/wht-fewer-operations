# k-cross: FULL exact test: does the 13-rectangle shape of the 19-gate circuit exist for other kernels of the class?
# K'(j,i) = K(pi[j], sig[i]); need a, c and 12 constants with K' = a c^T + sum_t p_t (a on rows nu_t)(c on cols mu_t)^T.
from fractions import Fraction as Fr
from itertools import permutations
import sys, time

terms = [((1,2,4,7),(7,)), ((0,3,5,6),(5,)), ((1,7),(6,)), ((0,6),(4,)), ((3,5),(3,)), ((2,4),(1,)),
         ((0,),(0,7)), ((6,),(1,6)), ((1,),(2,5)), ((7,),(3,4)), ((5,),(0,1,6,7)), ((4,),(2,3,4,5))]
exc = {2:{7,1}, 3:{5,3}, 7:{7,6,3,4}, 1:{7,6,2,5}, 4:{7,1,2,3,4,5}, 5:{5,3,0,1,6,7}, 6:{5,4,1,6}, 0:{5,4,0,7}}
pairs = [(a, b) for a in range(8) for b in range(a+1, 8) if 8 - len(exc[a] | exc[b]) >= 2]
order = [2, 3, 7, 1, 6, 0, 4, 5]

def in_span(vecs, target):
    # exact: is target in the span of vecs (lists of Fractions)?
    M = [list(v) for v in vecs] + [list(target)]
    rows = [list(r) for r in zip(*M)]            # 64 x 13, last column the target
    r = 0; ncol = len(vecs)
    for c in range(ncol):
        p = next((i for i in range(r, len(rows)) if rows[i][c] != 0), None)
        if p is None: continue
        rows[r], rows[p] = rows[p], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i][c] != 0:
                f = rows[i][c] / rows[r][c]
                rows[i] = [x - f*y for x, y in zip(rows[i], rows[r])]
        r += 1
    return all(row[-1] == 0 for row in rows[r:])

def full(Kp):
    c = [None]*8
    for i in range(8):
        if i not in (1, 7): c[i] = Fr(Kp[2][i])
    lam = Fr(Kp[2][0]) / Kp[3][0]
    c[1] = lam * Kp[3][1]; c[7] = lam * Kp[3][7]
    if any(x == 0 for x in c): return False
    a = [None]*8
    for j in range(8):
        S = [i for i in range(8) if i not in exc[j]]
        rr = {Fr(Kp[j][i]) / c[i] for i in S}
        if len(rr) != 1: return False
        a[j] = rr.pop()
    R = [Fr(Kp[j][i]) - a[j]*c[i] for j in range(8) for i in range(8)]
    vecs = [[(a[j]*c[i] if (j in nu and i in mu) else Fr(0)) for j in range(8) for i in range(8)] for (nu, mu) in terms]
    return in_span(vecs, R)

def run(name, K):
    cache = {}
    def prop(r1, r2, mask):
        key = (r1, r2, mask)
        if key in cache: return cache[key]
        S = [s for s in range(8) if mask >> s & 1]; u, v = K[r1], K[r2]
        res = all(u[S[0]]*v[s] == u[s]*v[S[0]] for s in S[1:]); cache[key] = res; return res
    t0 = time.time(); cand = 0; okc = 0; first = None
    for sig in permutations(range(8)):
        masks = {}
        for (x, y) in pairs:
            un = {sig[i] for i in exc[x] | exc[y]}
            masks[(x, y)] = sum(1 << s for s in range(8) if s not in un)
        pi = {}
        def dfs(i):
            nonlocal cand, okc, first
            if i == 8:
                cand += 1
                Kp = [[K[pi[j]][sig[ii]] for ii in range(8)] for j in range(8)]
                if full(Kp):
                    okc += 1
                    if first is None: first = (sig, dict(pi))
                return
            j = order[i]
            for r in range(8):
                if r in pi.values(): continue
                good = True
                for jj in order[:i]:
                    x, y = (jj, j) if jj < j else (j, jj)
                    if (x, y) in masks:
                        ra, rb = (pi[jj], r) if jj < j else (r, pi[jj])
                        if not prop(ra, rb, masks[(x, y)]): good = False; break
                if good:
                    pi[j] = r; dfs(i + 1); del pi[j]
        dfs(0)
    print(name, ": candidates passing the necessary conditions", cand, "; passing the FULL exact test", okc, " (%.0f s)" % (time.time() - t0))
    if first: print("    first full solution: input wiring", first[0], " output labelling", first[1])
    sys.stdout.flush()

H8 = [[(-1)**bin(a & x).count('1') for x in range(8)] for a in range(8)]
run("the transform itself (control)", H8)
for t in (2, 3, Fr(1, 2), -2, 5):
    run("kernel t^(Hamming distance), t = %s" % t, [[Fr(t)**bin(a ^ x).count('1') for x in range(8)] for a in range(8)])
# a non-symmetric member and the subset-sum relative
def kpow(k):
    return [[k[a >> 2 & 1][x >> 2 & 1] * k[a >> 1 & 1][x >> 1 & 1] * k[a & 1][x & 1] for x in range(8)] for a in range(8)]
run("kernel [[1,2],[3,4]] cubed", kpow([[1,2],[3,4]]))
run("kernel [[1,2],[2,3]] cubed", kpow([[1,2],[2,3]]))
