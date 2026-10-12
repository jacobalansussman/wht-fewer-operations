# d-2-letters: case generator for lm.c.  Prints cases on stdout.
# A flag is an ordered basis (b_1..b_k) of the address bits; the block of x at depth j is fixed by the first j coordinates of x
# in that basis.  Its many-scale (Haar) basis: the constant, and for each depth j and each block of depth j-1 the function
# +1 on one half, -1 on the other, normalised.  A letter is W diag(c) W^T: N free numbers, cost O(N) gates.
# Target: Hb[x][y] = (-1)^(x^T beta y), beta an invertible bit matrix (= the transform after a linear relabelling of one side).
import sys, itertools, random
pc = lambda v: bin(v).count("1")

def haar(basis, k):
    N = 1 << k
    pts = []                                   # pts[a] = point with coordinate word a (a_1 = top bit of a)
    for a in range(N):
        x = 0
        for j in range(k):
            if (a >> (k - 1 - j)) & 1: x ^= basis[j]
        pts.append(x)
    cols = [[1.0 / N ** 0.5] * N]
    for j in range(1, k + 1):
        size = 1 << (k - j + 1)                # block of depth j-1 has this many points
        for blk in range(1 << (j - 1)):
            col = [0.0] * N
            for t in range(size):
                a = blk * size + t
                col[pts[a]] = (1.0 if t < size // 2 else -1.0) / size ** 0.5
            cols.append(col)
    return [[cols[c][x] for c in range(N)] for x in range(N)]   # W[x][c]

def flagkey(basis, k):
    key = []
    for j in range(1, k):
        V = {0}
        for b in basis[j:]: V |= {v ^ b for v in V}
        key.append(frozenset(V))
    return tuple(key)

def all_flags(k):
    N = 1 << k; seen = {}
    def rec(basis, span):
        if len(basis) == k:
            b = basis[::-1]; seen.setdefault(flagkey(b, k), b); return
        for v in range(1, N):
            if v in span: continue
            rec(basis + [v], span | {s ^ v for s in span})
    rec([], {0})
    return list(seen.values())

def invertible(rows, k):
    r = list(rows); rank = 0
    for bit in range(k):
        p = next((i for i in range(rank, k) if (r[i] >> bit) & 1), None)
        if p is None: return False
        r[rank], r[p] = r[p], r[rank]
        for i in range(k):
            if i != rank and (r[i] >> bit) & 1: r[i] ^= r[rank]
        rank += 1
    return True

def target(beta, k):                           # beta: list of k row masks; x^T beta y = sum_i x_i * <beta_i, y>
    N = 1 << k; T = []
    for x in range(N):
        row = []
        for y in range(N):
            s = 0
            for i in range(k):
                if (x >> i) & 1: s ^= pc(beta[i] & y) & 1
            row.append(-1.0 if s else 1.0)
        T.append(row)
    return T

def emit(tag, k, Ws, T, restarts, seed):
    N = 1 << k
    out = ["%d %d %d %d %s" % (N, len(Ws), restarts, seed, tag)]
    for Wm in Ws:
        for row in Wm: out.append(" ".join("%.17g" % v for v in row))
    for row in T: out.append(" ".join("%g" % v for v in row))
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "k3all":                        # 8 points, two letters: first flag standard, second any of the 21, all 168 forms
        k = 3; FL = all_flags(k); std = [4, 2, 1]
        Wstd = haar(std, k)
        betas = [b for b in itertools.product(range(1, 8), repeat=3) if invertible(b, k)]
        for fi, fb in enumerate(FL):
            Wf = haar(fb, k)
            for b in betas:
                emit("F2=%s;beta=%s" % ("".join(map(str, fb)), "".join(map(str, b))), k, [Wstd, Wf], target(list(b), k), 6, fi * 1000 + b[0] * 64 + b[1] * 8 + b[2])
    elif mode == "k3one":                      # sanity: one letter at 4 points, one letter at 8 points
        for k in (2, 3):
            FL = all_flags(k)
            ident = [1 << i for i in range(k)]
            for fb in FL:
                emit("k=%d;one;F=%s" % (k, "".join(map(str, fb))), k, [haar(fb, k)], target(ident, k), 8, 7)
    elif mode == "sample":                     # sample: k, m letters, count, seed: random flags, random beta
        k, mm, cnt, seed = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
        restarts = int(sys.argv[6]) if len(sys.argv) > 6 else 5
        random.seed(seed); N = 1 << k
        def randbasis():
            while True:
                b = [random.randrange(1, N) for _ in range(k)]
                if invertible(b, k): return b
        for t in range(cnt):
            bs = [randbasis() for _ in range(mm)]
            beta = randbasis()
            emit("F=%s;beta=%s" % ("/".join(".".join(map(str, b)) for b in bs), ".".join(map(str, beta))), k, [haar(b, k) for b in bs], target(beta, k), restarts, seed * 100000 + t)
    elif mode == "perm":                       # k, m: all letters' flags are coordinate flags (bit orders), beta = identity or given
        k, mm = int(sys.argv[2]), int(sys.argv[3]); restarts = int(sys.argv[4]); which = sys.argv[5]
        ident = [1 << i for i in range(k)]
        std = [1 << (k - 1 - i) for i in range(k)]
        if which == "id": beta = ident
        elif which == "rev": beta = ident[::-1]
        else: beta = [int(v) for v in which.split(".")]
        perms = list(itertools.permutations(range(k)))
        if mm == 2: combos = [(tuple(range(k)), p) for p in perms]
        else:
            random.seed(5); combos = [(tuple(range(k)),) + tuple(random.choice(perms) for _ in range(mm - 1)) for _ in range(int(sys.argv[6]))]
        for cb in combos:
            bs = [[std[i] for i in p] for p in cb]
            emit("perm=%s;beta=%s" % ("/".join("".join(map(str, p)) for p in cb), which), k, [haar(b, k) for b in bs], target(beta, k), restarts, 17)
    elif mode == "k4nice":                     # 16 points: first flag = the tensor solution's flag, beta = identity, second flag: all 315
        k = 4; FL = all_flags(k); F1 = [4, 8, 1, 3]; ident = [1, 2, 4, 8]
        W1 = haar(F1, k)
        for fb in FL:
            emit("F1=4.8.1.3;F2=%s;beta=id" % ".".join(map(str, fb)), k, [W1, haar(fb, k)], target(ident, k), 4, 3)
    elif mode == "k5nice":                     # 32 points, two letters: first flag has the 4-point letter at the bottom; beta = identity; second flag sampled
        k = 5; ident = [1, 2, 4, 8, 16]; random.seed(int(sys.argv[2])); cnt = int(sys.argv[3]); N = 32
        firsts = [[16, 4, 8, 1, 3], [4, 8, 16, 1, 3], [16, 8, 4, 1, 3]]
        def randbasis():
            while True:
                b = [random.randrange(1, N) for _ in range(k)]
                if invertible(b, k): return b
        for t in range(cnt):
            F1 = firsts[t % 3]
            if t < 30: fb = [[1, 2, 16, 4, 12], [1, 2, 4, 16, 24], [1, 16, 2, 4, 12], [2, 1, 16, 12, 4], [1, 2, 4, 8, 24], [1, 2, 3, 16, 12], [1, 2, 16, 8, 12], [16, 1, 2, 4, 12], [1, 2, 4, 12, 16], [1, 2, 12, 4, 16]][t // 3]
            else: fb = randbasis()
            emit("F1=%s;F2=%s;beta=id" % (".".join(map(str, F1)), ".".join(map(str, fb))), k, [haar(F1, k), haar(fb, k)], target(ident, k), 3, t)
    elif mode == "k5three":                    # sanity at 32 points: three letters on the pair, pair, single flags (must be found)
        k = 5; ident = [1, 2, 4, 8, 16]
        Fs = [[16, 4, 8, 1, 3], [16, 1, 2, 4, 12], [1, 2, 4, 8, 16]]
        emit("three:pair,pair,single", k, [haar(b, k) for b in Fs], target(ident, k), 6, 9)
    elif mode == "k4two":                      # sanity at 16 points: the tensor solution's two flags
        k = 4; ident = [1, 2, 4, 8]
        emit("two:pair,pair", k, [haar([4, 8, 1, 3], k), haar([1, 2, 4, 12], k)], target(ident, k), 6, 9)
    elif mode == "onecall":                    # letter 1 = "anything on pair sums along v, diagonal on pair differences"; letter 2 = plain flag letter
        k = int(sys.argv[2]); N = 1 << k; what = sys.argv[3]; cnt = int(sys.argv[4]); random.seed(int(sys.argv[5])); restarts = int(sys.argv[6])
        v = 1; ident = [1 << i for i in range(k)]
        reps = [x for x in range(N) if x < x ^ v]
        W1 = [[0.0] * N for _ in range(N)]
        for a, x in enumerate(reps):
            W1[x][a] = W1[x ^ v][a] = 0.5 ** 0.5; W1[x][N // 2 + a] = 0.5 ** 0.5; W1[x ^ v][N // 2 + a] = -(0.5 ** 0.5)
        def randbasis():
            while True:
                b = [random.randrange(1, N) for _ in range(k)]
                if invertible(b, k): return b
        if what == "allF2":
            for fb in all_flags(k): emit("v=1;F2=%s;beta=id" % ".".join(map(str, fb)), k, [W1, haar(fb, k)], target(ident, k), restarts, 5)
        else:
            for t in range(cnt):
                fb = randbasis(); beta = randbasis()
                emit("v=1;F2=%s;beta=%s" % (".".join(map(str, fb)), ".".join(map(str, beta))), k, [W1, haar(fb, k)], target(beta, k), restarts, t)
