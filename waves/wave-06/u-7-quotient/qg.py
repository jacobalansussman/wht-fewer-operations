# u-7-quotient, run G: the block of the transform on the addresses with Q = 1, Q = x1x2 + x3x4 + ... (k even), exact integers.
# claim: M = (sqrt N / 2) I - (3 sqrt N / 2) P, i.e. (M - c I)(M + 2c I) = 0 with c = sqrt(N)/2, rank(P) = n (sqrt N - 2) / (3 sqrt N).
for k in (2, 4, 6):
    N = 1 << k
    def Qf(x): return sum((x >> (2 * i) & 1) * (x >> (2 * i + 1) & 1) for i in range(k // 2)) % 2
    S = [x for x in range(N) if Qf(x)]; n = len(S)
    M = [[(-1) ** (Qf(s ^ t) ^ Qf(s) ^ Qf(t)) for t in S] for s in S]
    c = int(round(N ** 0.5)) // 2
    ok = all(sum(M[i][t] * M[t][j] for t in range(n)) + c * M[i][j] - 2 * c * c * (i == j) == 0 for i in range(n) for j in range(n))
    tr = sum(M[i][i] for i in range(n))
    # eigenvalues c (mult n - m) and -2c (mult m): tr = c (n - m) - 2 c m
    m = (c * n - tr) // (3 * c) if c else 0
    print('N=%d: n=%d = (N - sqrt N)/2 ; (M - c)(M + 2c) = 0 with c = %d: %s ; trace %d ; rank of P = %d ; formula n(sqrtN-2)/(3 sqrtN) = %s' % (
        N, n, c, ok, tr, m, n * (2 * c - 2) / (6 * c) if c else '-'))
