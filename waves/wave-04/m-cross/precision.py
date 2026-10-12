# m-cross, the silly one: the transform to 2-adic precision.  H = sum_j (-2)^j B_j,  B_j(y,x) = C(|x and y|, j).   exact integers.
# (1) rank of B_j and of the truncation L_j = sum_{i<j} (-2)^i B_i, and H == L_j modulo 2^j.
# (2) an explicit circuit, count (G), for a matrix congruent to H modulo 4 (namely J - 2 * (y.x as a whole number)), replayed.
from fractions import Fraction as F
from math import comb
def rank(M):
    M = [[F(t) for t in r] for r in M]; rk = 0
    for c in range(len(M[0])):
        p = next((i for i in range(rk, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[rk], M[p] = M[p], M[rk]
        for i in range(rk + 1, len(M)):
            if M[i][c] != 0:
                f = M[i][c] / M[rk][c]; M[i] = [a - f * b for a, b in zip(M[i], M[rk])]
        rk += 1
    return rk
for k in (3, 4, 5):
    N = 2 ** k; ov = [[bin(x & y).count('1') for x in range(N)] for y in range(N)]
    H = [[(-1) ** ov[y][x] for x in range(N)] for y in range(N)]
    L = [[0] * N for _ in range(N)]; out = []
    for j in range(k + 1):
        B = [[comb(ov[y][x], j) for x in range(N)] for y in range(N)]
        cong = all((H[y][x] - L[y][x]) % 2 ** j == 0 for y in range(N) for x in range(N))
        out.append('j=%d: rank B_j=%d (C(k,j)=%d), rank of truncation before it=%d, H==truncation mod 2^j: %s' % (j, rank(B), comb(k, j), rank(L) if j else 0, cong))
        L = [[L[y][x] + (-2) ** j * B[y][x] for x in range(N)] for y in range(N)]
    print('N=%d' % N); print('   ' + '\n   '.join(out)); print('   full sum equals H:', L == H)
def circuit_mod4(k):
    N = 2 ** k; gates = 0
    vec = lambda i: [int(i == j) for j in range(N)]
    add = lambda u, v, a=1, b=1: [a * p + b * q for p, q in zip(u, v)]
    # half-cube sums s_i and the total S, by folding one bit at a time
    cur = [vec(x) for x in range(N)]; s = [None] * k
    for i in range(k):                       # fold away bit i (the lowest remaining)
        ones = [cur[t] for t in range(len(cur)) if t & 1]
        acc = ones[0]
        for w in ones[1:]: acc = add(acc, w); gates += 1
        s[i] = acc
        nxt = []
        for t in range(0, len(cur), 2): nxt.append(add(cur[t], cur[t + 1])); gates += 1
        cur = nxt
    S = cur[0]
    # all subset sums of s_0..s_{k-1}
    sub = {0: None}
    for y in range(1, N):
        low = y & -y; rest = y ^ low; i = low.bit_length() - 1
        if rest == 0: sub[y] = s[i]
        else: sub[y] = add(sub[rest], s[i]); gates += 1
    outs = [S] + [None] * (N - 1)
    for y in range(1, N): outs[y] = add(S, sub[y], 1, -2); gates += 1
    ok = all((outs[y][x] - (-1) ** bin(x & y).count('1')) % 4 == 0 for y in range(N) for x in range(N))
    return N, gates, ok
for k in (3, 4, 5, 6, 7, 8):
    N, g, ok = circuit_mod4(k); print('N=%3d: a matrix congruent to H modulo 4 in %4d gates (G) = %.2f N ; textbook for H %5d ; congruent: %s' % (N, g, g / N, N * k, ok))
