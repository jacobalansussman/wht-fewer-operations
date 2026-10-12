# scd.py (d-0-zeta): symmetric chain decomposition (Greene-Kleitman bracket matching) of the k-cube,
# prefix sums along the chains, and what is left to reach the subset-sum matrix Z. Exact integers.
# Z[S][T] = 1 if T subset of S.  P = prefix sums along chains: P[S][T] = 1 if T below-or-equal S in the SAME chain.
# Input side:  Z = C * P   with C = Z * P^-1 ;  output side:  Z = P * C2  with C2 = P^-1 * Z.
import sys
def chains(k):
    # word b_1..b_k, bit i set = element i present. 1 = ')' , 0 = '(' ; match; unmatched look like 1..1 0..0
    N = 1 << k; succ = [None] * N; pred = [None] * N
    for S in range(N):
        stack = []; matched = [False] * k
        for i in range(k):
            if not (S >> i) & 1: stack.append(i)
            elif stack: j = stack.pop(); matched[i] = matched[j] = True
        un0 = [i for i in range(k) if not matched[i] and not (S >> i) & 1]
        un1 = [i for i in range(k) if not matched[i] and (S >> i) & 1]
        if un0: succ[S] = S | (1 << un0[0])       # leftmost unmatched 0 becomes 1
        if un1: pred[S] = S & ~(1 << un1[-1])      # rightmost unmatched 1 becomes 0
    for S in range(N):
        if succ[S] is not None: assert pred[succ[S]] == S
    return succ, pred
def mat_sub(k):
    N = 1 << k
    return [[1 if (T & S) == T else 0 for T in range(N)] for S in range(N)]
def rank_mod(M, p=1000003):
    M = [r[:] for r in M]; rk = 0; n = len(M[0])
    for c in range(n):
        piv = next((i for i in range(rk, len(M)) if M[i][c] % p), None)
        if piv is None: continue
        M[rk], M[piv] = M[piv], M[rk]; inv = pow(M[rk][c], p - 2, p)
        M[rk] = [x * inv % p for x in M[rk]]
        for i in range(len(M)):
            if i != rk and M[i][c] % p:
                f = M[i][c]; M[i] = [(x - f * y) % p for x, y in zip(M[i], M[rk])]
        rk += 1
    return rk
for k in (2, 3, 4, 5, 6, 8, 10):
    N = 1 << k; succ, pred = chains(k)
    nch = sum(1 for S in range(N) if pred[S] is None)
    lens = {}
    for S in range(N):
        if pred[S] is None:
            L = 1; T = S
            while succ[T] is not None: T = succ[T]; L += 1
            lens[L] = lens.get(L, 0) + 1
    # C2 rows: y_S - y_pred(S) = sum over T subset S containing b_S (the element removed going down), or all of [0,S] for a chain bottom
    # C columns: [T subset S] - [succ(T) subset S]
    nnzC2 = 0; nnzC = 0
    for S in range(N):
        nnzC2 += (1 << bin(S).count("1")) if pred[S] is None else (1 << (bin(S).count("1") - 1))
    for T in range(N):
        up = k - bin(T).count("1")
        nnzC += (1 << up) if succ[T] is None else (1 << (up - 1))
    line = "k=%2d N=%5d chains=%4d lengths=%s | pass cost N-chains=%5d | nnz Z=%7d  nnz(P^-1 Z)=%7d  nnz(Z P^-1)=%7d | textbook gates %6d" % (
        k, N, nch, sorted(lens.items()), N - nch, 3 ** k, nnzC2, nnzC, k * N // 2)
    if k <= 6:
        Z = mat_sub(k)
        C2 = [[Z[S][T] - (Z[pred[S]][T] if pred[S] is not None else 0) for T in range(N)] for S in range(N)]
        I = [[int(i == j) for j in range(N)] for i in range(N)]
        offdiag = sum(1 for S in range(N) for T in range(N) if S != T and C2[S][T])
        r = rank_mod([[C2[S][T] - I[S][T] for T in range(N)] for S in range(N)])
        rz = rank_mod([[Z[S][T] - I[S][T] for T in range(N)] for S in range(N)])
        # rows of C2 with a single non-zero off the diagonal cost one gate; rows equal to e_S cost nothing
        free = sum(1 for S in range(N) if sum(map(abs, C2[S])) == 1)
        line += " | off-diagonal entries left %d, rows already done %d, rank(P^-1 Z - I)=%d, rank(Z - I)=%d" % (offdiag, free, r, rz)
    print(line)
    if k == 4:
        print("   the 6 chains of the 4-cube and the rows of P^-1 Z (sets written as digit strings):")
        name = lambda S: "".join(str(i + 1) for i in range(k) if (S >> i) & 1) or "0"
        for S in range(N):
            if pred[S] is None:
                ch = [S]
                while succ[ch[-1]] is not None: ch.append(succ[ch[-1]])
                print("    chain:", " < ".join(name(x) for x in ch))
        for S in range(N):
            print("    y'_%-5s = sum of x_T over T in {%s}" % (name(S), ",".join(name(T) for T in range(N) if C2[S][T])))
