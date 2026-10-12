# k-cross, second run. Exact integers / fractions / Gaussian integers.
from fractions import Fraction as Fr
from itertools import permutations
import sys, time

def rank(M):
    M = [[Fr(v) for v in r] for r in M]; r = 0
    if not M or not M[0]: return 0
    for c in range(len(M[0])):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]/M[r][c]
                M[i] = [a - f*b for a, b in zip(M[i], M[r])]
        r += 1
    return r
def kron(A, B): return [[a*b for a in ra for b in rb] for ra in A for rb in B]
def matmul(A, B): return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
H8 = [[(-1)**bin(a & x).count('1') for x in range(8)] for a in range(8)]

print("== A. rectangle lemma on the 13-term form: rank H[A,B] <= 2 + (terms strictly inside A x B) ==")
terms = [((0,1,2,3,4,5,6,7),(0,1,2,3,4,5,6,7)), ((1,2,4,7),(7,)), ((0,3,5,6),(5,)), ((1,7),(6,)), ((0,6),(4,)), ((3,5),(3,)), ((2,4),(1,)),
         ((0,),(0,7)), ((6,),(1,6)), ((1,),(2,5)), ((7,),(3,4)), ((5,),(0,1,6,7)), ((4,),(2,3,4,5))]
rownodes = [(0,1,2,3,4,5,6,7),(1,2,4,7),(0,3,5,6),(1,7),(2,4),(0,6),(3,5)]
colnodes = [(0,1,2,3,4,5,6,7),(0,1,6,7),(2,3,4,5),(0,7),(1,6),(2,5),(3,4)]
ok = True; tight = 0; tab = []
for A in rownodes:
    for B in colnodes:
        r = rank([[H8[y][x] for x in B] for y in A])
        n = sum(1 for (nu, mu) in terms if set(nu) < set(A) and set(mu) < set(B))
        ok &= (r <= 2 + n); tight += (r == 2 + n)
        tab.append((len(A), len(B), r, n, len(A)*len(B)//8 if len(A)*len(B) >= 8 else 0))
print(" holds on all", len(tab), "node pairs:", ok, "; met with equality on", tight)
print(" every block has the least rank |A||B|/N (or 1 when |A||B| < N):", all(t[2] == max(1, t[4]) for t in tab))

print("== B. every 2x2 kernel times a relabelling-with-scalings is traceless, so its square is a number ==")
import random; random.seed(2); good = True
for _ in range(200):
    a, b, c, d = [Fr(random.choice([-4,-3,-2,-1,1,2,3,4]), random.choice([1,2,3])) for _ in range(4)]
    if a*d == b*c: continue
    KM = matmul([[a,b],[c,d]], [[1,0],[0,-a/d]])          # trace a - a = 0
    S = matmul(KM, KM)
    good &= (S[0][1] == 0 and S[1][0] == 0 and S[0][0] == S[1][1])
print(" (K*diag(1,-a/d))^2 is a multiple of the identity for 200 random rational kernels:", good)

print("== C. the subset-sum kernel: mirror matrix has zero entries ==")
def mirror(k, m):
    a, b, c, d = k[0][0], k[0][1], k[1][0], k[1][1]; det = a*d - b*c
    P = [[0]*4 for _ in range(4)]; P[1][1] = 1; P[2][2] = 1; P[0][3] = Fr(-b, c); P[3][0] = Fr(-c, b)
    KP = matmul(kron(k, k), P); M = KP
    for _ in range(m - 1): M = kron(M, KP)
    n = len(M)
    return [[M[i][j] - (det**m if i == j else 0) for j in range(n)] for i in range(n)], n
for m in (1, 2, 3):
    Mm, n = mirror([[1,1],[1,0]], m)
    print("  kernel [[1,1],[1,0]] (subset sums up to relabelling)  N =", n, " rank", rank(Mm), " zero entries", sum(1 for r in Mm for x in r if x == 0), "of", n*n)
    sys.stdout.flush()

print("== D. the 19-gate shape for other kernels: all 8! input wirings x all output labellings, necessary conditions ==")
exc = {2:{7,1}, 3:{5,3}, 7:{7,6,3,4}, 1:{7,6,2,5}, 4:{7,1,2,3,4,5}, 5:{5,3,0,1,6,7}, 6:{5,4,1,6}, 0:{5,4,0,7}}
pairs = [(a, b) for a in range(8) for b in range(a+1, 8) if 8 - len(exc[a] | exc[b]) >= 2]
order = [2, 3, 7, 1, 6, 0, 4, 5]
def run(name, R, limit):
    # R: 8x8 matrix as rows; entries exact (ints or Gaussian pairs)
    def mul(u, v):
        if isinstance(u, tuple): return (u[0]*v[0]-u[1]*v[1], u[0]*v[1]+u[1]*v[0])
        return u*v
    cache = {}
    def prop(r1, r2, mask):
        key = (r1, r2, mask)
        if key in cache: return cache[key]
        S = [s for s in range(8) if mask >> s & 1]; u, v = R[r1], R[r2]
        res = all(mul(u[S[0]], v[s]) == mul(u[s], v[S[0]]) for s in S[1:])
        cache[key] = res; return res
    t0 = time.time(); total = 0; wir = 0; nsig = 0
    for sig in permutations(range(8)):
        if time.time() - t0 > limit: break
        nsig += 1
        masks = {}
        for (a, b) in pairs:
            un = {sig[i] for i in exc[a] | exc[b]}
            masks[(a, b)] = sum(1 << s for s in range(8) if s not in un)
        cnt = 0; pi = {}
        def dfs(i):
            nonlocal cnt
            if i == 8: cnt += 1; return
            j = order[i]
            for r in range(8):
                if r in pi.values(): continue
                okk = True
                for jj in order[:i]:
                    a, b = (jj, j) if jj < j else (j, jj)
                    if (a, b) in masks:
                        ra, rb = (pi[jj], r) if jj < j else (r, pi[jj])
                        if not prop(ra, rb, masks[(a, b)]): okk = False; break
                if okk:
                    pi[j] = r; dfs(i + 1); del pi[j]
        dfs(0)
        total += cnt; wir += (cnt > 0)
    print("  ", name, ": input wirings tried", nsig, "of 40320; wirings with at least one output labelling passing:", wir, "; passing pairs:", total, " (%.0f s)" % (time.time() - t0))
    sys.stdout.flush()
run("the transform itself (control)", H8, 100)
I4 = [(1,0), (0,1), (-1,0), (0,-1)]
run("t = i (control: the transform up to phases)", [[I4[bin(a ^ x).count('1') % 4] for x in range(8)] for a in range(8)], 100)
for t in (2, 3, -2, Fr(1, 2)):
    run("t = %s" % t, [[t**bin(a ^ x).count('1') for x in range(8)] for a in range(8)], 90)
