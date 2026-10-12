# e-6-shifts: three identities met on the way, checked exactly in integers at N = 4, 8, 16 (all entries are small integers).
# A. shift array:  H * X * H = N * diag(Hx)  for X[a][b] = x[a xor b];   dual: H * diag(x) * H = the shift array of Hx.
# B. circ(x) + diag(Hx) commutes with H, circ(x) - diag(Hx) anticommutes  (so pinch(circ(x)) = (circ(x) + diag(Hx))/2).
# C. multiplication table: X[a][b] = x[a*b] (field with N elements, addresses paired by the trace form).  Then the
#    N^2-point transform of X is again a multiplication table: Y[u][v] = y[u*v] for (u,v) != (0,0), with
#    y[t] = sum_s Kl(s,t) x[s],  Kl(s,t) = sum over c != 0 of (-1)^Tr(c*s + t/c)   (a Kloosterman sum when s,t != 0),
#    and Y[0][0] = y[0] + N * (sum of x).
import sys
pc = lambda x: bin(x).count("1")
def mm(A, B): return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def gfmul(k, poly):
    n = 1 << k
    def mul(a, b):
        r = 0
        while b:
            if b & 1: r ^= a
            b >>= 1; a <<= 1
            if a & n: a ^= poly
        return r
    return mul
for k, poly in ((2, 0b111), (3, 0b1011), (4, 0b10011)):
    N = 1 << k
    H = [[1 - 2 * (pc(a & b) & 1) for b in range(N)] for a in range(N)]
    okA = okA2 = okB = True
    for s in range(N):     # linear in x: enough to check x = unit vector e_s
        X = [[1 if (a ^ b) == s else 0 for b in range(N)] for a in range(N)]
        Hx = [H[w][s] for w in range(N)]
        D = [[Hx[w] if w == v else 0 for v in range(N)] for w in range(N)]
        okA &= mm(mm(H, X), H) == [[N * D[i][j] for j in range(N)] for i in range(N)]
        E = [[1 if (a == s and b == s) else 0 for b in range(N)] for a in range(N)]
        okA2 &= mm(mm(H, E), H) == [[Hx[a ^ b] for b in range(N)] for a in range(N)]
        Cp = [[X[i][j] + D[i][j] for j in range(N)] for i in range(N)]; Cm = [[X[i][j] - D[i][j] for j in range(N)] for i in range(N)]
        okB &= mm(H, Cp) == mm(Cp, H) and mm(H, Cm) == [[-t for t in r] for r in mm(Cm, H)]
    mul = gfmul(k, poly)
    inv = {a: next(b for b in range(1, N) if mul(a, b) == 1) for a in range(1, N)}
    # trace form: Tr(a) = a + a^2 + ... ; pairing <u, a> = Tr(u*a)
    def tr(a):
        t = 0; y = a
        for _ in range(k): t ^= y; y = mul(y, y)
        assert t in (0, 1); return t
    chi = [[1 - 2 * tr(mul(u, a)) for a in range(N)] for u in range(N)]     # a Hadamard matrix: H with relabelled columns
    assert mm(chi, chi) == [[N if i == j else 0 for j in range(N)] for i in range(N)]
    Kl = [[sum(1 - 2 * (tr(mul(c, s)) ^ tr(mul(t, inv[c]))) for c in range(1, N)) for s in range(N)] for t in range(N)]
    okC = True
    for s in range(N):
        X = [[1 if mul(a, b) == s else 0 for b in range(N)] for a in range(N)]
        Y = mm(mm(chi, X), chi)
        for u in range(N):
            for v in range(N):
                want = Kl[mul(u, v)][s] + (N if (u == 0 and v == 0) else 0)
                okC &= (Y[u][v] == want)
    vals = sorted(set(Kl[t][s] for t in range(1, N) for s in range(1, N)))
    KK = mm(Kl, Kl)
    print("N=%2d  A: H X H = N diag(Hx): %s ; dual H diag(x) H = shifts of Hx: %s ;  B: circ+diag commutes, circ-diag anticommutes: %s ;  C: transform of a multiplication table is the multiplication table of the Kloosterman image: %s ; Kloosterman entries (s,t != 0): %s" % (N, okA, okA2, okB, okC, vals))
