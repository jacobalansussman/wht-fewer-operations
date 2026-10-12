# k-cross: four small exact checks. Exact integers / fractions throughout.
from fractions import Fraction as Fr
from itertools import permutations, product
import random, sys

def kron(A, B):
    return [[a*b for a in ra for b in rb] for ra in A for rb in B]
def matmul(A, B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def rank(M):
    M = [[Fr(v) for v in r] for r in M]; r = 0
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
def H(k):
    N = 1 << k
    return [[(-1)**bin(a & x).count('1') for x in range(N)] for a in range(N)]

print("== 1. two-tree rectangle form of the 19-gate circuit (g-1) ==")
# input-side forms of the merge tree
e = [[1 if i == j else 0 for j in range(8)] for i in range(8)]
def lin(*t):
    v = [0]*8
    for c, w in t: v = [a + c*b for a, b in zip(v, w)]
    return v
g1 = lin((1,e[0]),(1,e[7])); g2 = lin((1,e[1]),(1,e[6])); g3 = lin((1,e[2]),(-1,e[5])); g4 = lin((1,e[3]),(-1,e[4]))
g5 = lin((1,g1),(-1,g2)); g6 = lin((1,g3),(1,g4)); c = lin((1,g5),(-1,g6))
forms = {'c':c,'x7':e[7],'x5':e[5],'x6':e[6],'x4':e[4],'x3':e[3],'x1':e[1],'g1':g1,'g2':g2,'g3':g3,'g4':g4,'g5':g5,'g6':g6}
names = list(forms)
# the walk, with the 13 forms as independent symbols
def sym(n): return {n: 1}
def add(a, u, b, v):
    out = {}
    for k_, v_ in u.items(): out[k_] = out.get(k_, 0) + a*v_
    for k_, v_ in v.items(): out[k_] = out.get(k_, 0) + b*v_
    return out
G7 = sym('c'); G8 = add(1,G7,-2,sym('x7')); G9 = add(1,G7,-2,sym('x5')); G10 = add(1,G8,2,sym('x6')); G11 = add(1,G9,-2,sym('x4'))
Y = {}
Y[7] = add(1,G10,2,sym('g4')); Y[3] = add(1,G9,2,sym('x3')); Y[5] = add(-1,Y[3],2,sym('g5')); Y[1] = add(1,G10,2,sym('g3'))
Y[6] = add(1,G11,2,sym('g2')); Y[2] = add(1,G8,2,sym('x1')); Y[4] = add(1,Y[2],2,sym('g6')); Y[0] = add(-1,G11,2,sym('g1'))
W = [[Y[j].get(n, 0) for n in names] for j in range(8)]          # 8 x 13
F = [forms[n] for n in names]                                     # 13 x 8
print(" W*F == H_8:", matmul(W, F) == H(3))
astar = [W[j][0] for j in range(8)]
print(" output-side centre a* =", astar, "  input-side centre c =", c)
ok = True; sizes = []
for t, n in enumerate(names):
    col = [W[j][t] for j in range(8)]; sup = [j for j in range(8) if col[j] != 0]
    ratios = {Fr(col[j], astar[j]) for j in sup}
    fsup = [i for i in range(8) if forms[n][i] != 0]
    fr = {Fr(forms[n][i], c[i]) for i in fsup}
    ok &= (len(ratios) == 1 and len(fr) == 1)
    sizes.append((n, len(sup), len(fsup), sup, fsup))
print(" every term is (a* on a row set) x (c on a column set), one constant each:", ok)
for s in sizes: print("   term", s[0], " rows", s[3], " cols", s[4], " area", s[1]*s[2])
rows_sets = [frozenset(s[3]) for s in sizes]; col_sets = [frozenset(s[4]) for s in sizes]
lam = lambda S: all(a <= b or b <= a or not (a & b) for a in S for b in S)
print(" row sets nested-or-disjoint:", lam(rows_sets), "  column sets nested-or-disjoint:", lam(col_sets))
print(" terms tau =", len(names), "  N - 2 + tau =", 8 - 2 + len(names), "(the gate count 19)")
# brick and Potts in the same form
v = [1,1,1,-1]; H4 = H(2)
R = [[H4[i][j] - v[i]*v[j] for j in range(4)] for i in range(4)]
print(" 4 points: H_4 - v v^T has", sum(1 for r in R for x in r if x), "non-zeros, one per row and column:",
      all(sum(1 for x in r if x) == 1 for r in R), " -> tau = 5, N - 2 + tau = 7")

print("== 2. brick for every 2x2 kernel with b*c != 0 (not only symmetric) ==")
random.seed(1); allok = True
for _ in range(300):
    a, b, cc, d = [Fr(random.choice([-5,-4,-3,-2,-1,1,2,3,4,5]), random.choice([1,2,3])) for _ in range(4)]
    if a*d == b*cc: continue
    k = [[a,b],[cc,d]]; det = a*d - b*cc; K = kron(k, k)
    P = [[0]*4 for _ in range(4)]
    P[1][1] = det; P[2][2] = det; P[0][3] = -det*b/cc; P[3][0] = -det*cc/b
    D = [[K[i][j] - P[i][j] for j in range(4)] for i in range(4)]
    allok &= (rank(D) == 1)
print(" k(x)k - det*(scaled swap) has rank one for all 300 random rational kernels:", allok)

print("== 3. size of the mirror: reflection kernels against the rest ==")
def mirror_rank(k, m):
    a, b, cc, d = k[0][0], k[0][1], k[1][0], k[1][1]; det = a*d - b*cc
    P = [[0]*4 for _ in range(4)]
    P[1][1] = 1; P[2][2] = 1; P[0][3] = Fr(-b, cc); P[3][0] = Fr(-cc, b)   # k(x)k = rank one + det*P, P*P = I
    K2 = kron(k, k); KP = matmul(K2, P)          # = det*I + rank one
    M = KP
    for _ in range(m - 1): M = kron(M, KP)
    n = len(M)
    Mm = [[M[i][j] - (det**m if i == j else 0) for j in range(n)] for i in range(n)]
    zeros = sum(1 for r in Mm for x in r if x == 0)
    return rank(Mm), zeros, n
for name, k in [("transform [[1,1],[1,-1]]", [[1,1],[1,-1]]), ("[[1,2],[2,3]]", [[1,2],[2,3]]), ("[[1,2],[2,1]]", [[1,2],[2,1]]), ("[[2,1],[1,3]]", [[2,1],[1,3]])]:
    for m in (1, 2, 3):
        r, z, n = mirror_rank(k, m)
        print("  kernel", name, " N =", n, " rank of (kernel power * relabelling - scalar) =", r,
              "  (4^m-2^m)/2 =", (4**m - 2**m)//2, " 4^m-3^m =", 4**m - 3**m, "  zero entries:", z)
        sys.stdout.flush()

print("== 4. is the 19-gate shape a property of the class? necessary conditions, all 8! output labellings ==")
exc = {2:{7,1}, 3:{5,3}, 7:{7,6,3,4}, 1:{7,6,2,5}, 4:{7,1,2,3,4,5}, 5:{5,3,0,1,6,7}, 6:{5,4,1,6}, 0:{5,4,0,7}}
def rows_t(t):
    return [[t**bin(a ^ x).count('1') for x in range(8)] for a in range(8)]
def prop(u, v, S):
    S = sorted(S)
    return all(u[S[0]]*v[s] == u[s]*v[S[0]] for s in S[1:])
for t in (-1, 2, 3, Fr(1,2), -2):
    Rw = rows_t(t)
    okp = {}
    for j1 in range(8):
        for j2 in range(j1+1, 8):
            S = set(range(8)) - exc[j1] - exc[j2]
            if len(S) < 2: continue
            for r1 in range(8):
                for r2 in range(8):
                    if r1 != r2: okp[(j1,j2,r1,r2)] = prop(Rw[r1], Rw[r2], S)
    cnt = 0
    keys = sorted({(a,b) for (a,b,_,_) in okp})
    for pi in permutations(range(8)):
        if all(okp[(a,b,pi[a],pi[b])] for a,b in keys): cnt += 1
    print("  kernel entries t^(Hamming distance), t =", t, ": output labellings passing the necessary conditions:", cnt, "of 40320")
    sys.stdout.flush()
