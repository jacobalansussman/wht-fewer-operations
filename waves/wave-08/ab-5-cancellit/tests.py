# ab-5: exact tests (rational arithmetic).  Count (G): a gate is any a*u + b*v, scalings free.
from fractions import Fraction as F
from itertools import product
def kron(A, B): return [[a*b for a in ra for b in rb] for ra in A for rb in B]
def mat(A, B): return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def power(K, k):
    M = [[F(1)]]
    for _ in range(k): M = kron(M, K)
    return M
# --- T1. rank one plus sparse for the square of EVERY kernel [[1,1],[1,s]] ---
okall = True
for s in [F(-1), F(0), F(2), F(3), F(-5, 7), F(1, 2), F(7)]:
    K = [[F(1), F(1)], [F(1), s]]
    K2 = kron(K, K)
    b = [F(1), F(1), F(1), s]
    Pp = [[0,0,0,1],[0,-1,0,0],[0,0,-1,0],[1,0,0,0]]
    R = [[b[i]*b[j] + (1-s)*Pp[i][j] for j in range(4)] for i in range(4)]
    okall &= (R == K2)
    # the brick as a program: w = x0+x1+x2+s*x3 ; outputs w+(1-s)x3, w-(1-s)x1, w-(1-s)x2, s*w+(1-s)x0
    def brick(x):
        gates = 0
        w = x[0] + x[1]; gates += 1
        w = w + x[2]; gates += 1
        if s != 0: w = w + s*x[3]; gates += 1
        y0 = w + (1-s)*x[3]; gates += 1
        y1 = w - (1-s)*x[1]; gates += 1
        y2 = w - (1-s)*x[2]; gates += 1
        if s != 0: y3 = s*w + (1-s)*x[0]; gates += 1
        else: y3 = x[0]
        return [y0, y1, y2, y3], gates
    g = None
    for j in range(4):
        e = [F(int(i == j)) for i in range(4)]
        y, g = brick(e)
        okall &= all(y[i] == K2[i][j] for i in range(4))
    textbook = 4 if s == 0 else 8
    print('T1 s = %s: square of the kernel = b b^T + (1-s) P, b = (1,1,1,s): %s ; brick %d gates, textbook %d' % (s, R == K2, g, textbook))
print('T1 all exact:', okall)
# --- T2. three-call word at 16 points ---
k = 4; N = 16
H = power([[F(1), F(1)], [F(1), F(-1)]], k)
Z = power([[F(1), F(0)], [F(1), F(1)]], k)
def D(a, b): return [[(a**(k - bin(i).count('1')) * b**bin(i).count('1')) if i == j else F(0) for j in range(N)] for i in range(N)]
W = D(F(1), F(3, 5))
for d in [D(F(1), F(-1, 2)), D(F(1), F(1, 3)), D(F(1), F(5, 4))]:
    W = mat(mat(W, H), d)
print('T2 Z_16 = D(1,3/5) H D(1,-1/2) H D(1,1/3) H D(1,5/4) exactly:', W == Z)
print('T2 gates (G): 3 x 52 = 156 with the 52-gate 16-point transform of e2-0, 3 x 64 = 192 with the textbook; Yates 32')
# --- T3. the disjointness kernel R = [[1,1],[1,0]]: Z up to a relabelling, order 3 over the two-element field ---
R1 = [[1,1],[1,0]]
def kron_i(A, B): return [[a*b for a in ra for b in rb] for ra in A for rb in B]
for kk in [1, 2, 3, 4, 5]:
    M = [[1]]
    for _ in range(kk): M = kron_i(M, R1)
    n = len(M)
    M2 = [[sum(M[i][t]*M[t][j] for t in range(n)) % 2 for j in range(n)] for i in range(n)]
    M3 = [[sum(M2[i][t]*M[t][j] for t in range(n)) % 2 for j in range(n)] for i in range(n)]
    I = [[int(i == j) for j in range(n)] for i in range(n)]
    Zk = [[int((j & i) == j) for j in range(n)] for i in range(n)]
    relabel = [[Zk[i][(n-1) ^ j] for j in range(n)] for i in range(n)]   # Z with inputs complemented
    relabel2 = [[Zk[(n-1) ^ i][j] for j in range(n)] for i in range(n)]
    S = [[(I[i][j] + M[i][j] + M2[i][j]) % 2 for j in range(n)] for i in range(n)]
    # rank of S = I + M + M^2 over the two-element field (dimension of the part where M acts as the identity)
    rows = [sum(S[i][j] << j for j in range(n)) for i in range(n)]; rk = 0
    for bit in range(n):
        idx = next((t for t, r in enumerate(rows) if (r >> bit) & 1), None)
        if idx is None: continue
        piv = rows.pop(idx); rk += 1
        rows = [r ^ piv if (r >> bit) & 1 else r for r in rows]
    idem = all(sum(S[i][t]*S[t][j] for t in range(n)) % 2 == S[i][j] for i in range(n) for j in range(n))
    assert idem and rk == (n + 2*(-1)**kk)//3
    print('T3 k=%d: (R^k)^3 = 1 mod 2: %s ; R^k is Z with a relabelling of inputs or outputs: %s ; E = 1 + M + M^2 is an idempotent mod 2 of rank %d of %d = (N + 2(-1)^k)/3'
          % (kk, M3 == I, (M == relabel) or (M == relabel2), rk, n))
# --- T4. two levels of the s = 0 brick at 16 points ---
print('T4 two passes of the s = 0 brick at 16 points: 2 passes x 4 bricks x 5 gates = 40 gates (G); Yates 32; generic kernel 2 x 4 x 7 = 56 against 64')
