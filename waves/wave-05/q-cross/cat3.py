# q-cross hybrid 1, part 2: anneal over BOTH orders and sign scalings for the caterpillar letter (exact integers via numpy).
# gates (G) = N - 2 + nnz(M), M = mixed second difference of r c H in the two orders. Upper bounds only.
import sys, random, numpy as np
k = int(sys.argv[1]); iters = int(sys.argv[2]); seeds = int(sys.argv[3]); N = 1 << k
H = np.array([[1 if (a & b) == b else 0 for b in range(N)] for a in range(N)], dtype=np.int64)  # Z: subset sums
def nnz(rows, cols, r, c):
    A = np.zeros((N + 1, N + 1), dtype=np.int64)
    A[:N, :N] = H[np.ix_(rows, cols)] * r[:, None] * c[None, :]
    M = A[:N, :N] - A[1:, :N] - A[:N, 1:] + A[1:, 1:]
    return int(np.count_nonzero(M)), M
best_all = None
for seed in range(seeds):
    rnd = random.Random(seed)
    rows = np.array(rnd.sample(range(N), N)); cols = np.array(rnd.sample(range(N), N))
    r = np.array([rnd.choice((-1, 1)) for _ in range(N)]); c = np.array([rnd.choice((-1, 1)) for _ in range(N)])
    cur, _ = nnz(rows, cols, r, c); best = cur; T0 = 1.2
    for it in range(iters):
        T = T0 * (1 - it / iters) + 0.05
        m = rnd.randrange(6)
        if m < 2:
            arr = rows if m == 0 else cols; i, j = rnd.sample(range(N), 2); arr[i], arr[j] = arr[j], arr[i]
            v, _ = nnz(rows, cols, r, c)
            if v <= cur or rnd.random() < 2.718 ** ((cur - v) / T): cur = v
            else: arr[i], arr[j] = arr[j], arr[i]
        elif m < 4:
            arr = rows if m == 2 else cols; i, j = sorted(rnd.sample(range(N + 1), 2)); seg = arr[i:j].copy(); arr[i:j] = seg[::-1]
            sg = r if m == 2 else c; sseg = sg[i:j].copy(); sg[i:j] = sseg[::-1]
            v, _ = nnz(rows, cols, r, c)
            if v <= cur or rnd.random() < 2.718 ** ((cur - v) / T): cur = v
            else: arr[i:j] = seg; sg[i:j] = sseg
        else:
            sg = r if m == 4 else c; i = rnd.randrange(N); sg[i] = -sg[i]
            v, _ = nnz(rows, cols, r, c)
            if v <= cur or rnd.random() < 2.718 ** ((cur - v) / T): cur = v
            else: sg[i] = -sg[i]
        if cur < best:
            best = cur; keep = (rows.copy(), cols.copy(), r.copy(), c.copy())
    print(f"N={N} seed={seed} best nnz={best} gates={N-2+best}", flush=True)
    if best_all is None or best < best_all[0]: best_all = (best, keep)
b, (rows, cols, r, c) = best_all
v, M = nnz(rows, cols, r, c)
vals, cnt = np.unique(M[M != 0], return_counts=True)
print("BEST", N, "nnz", v, "gates", N - 2 + v, "textbook", N * k, "values", dict(zip(vals.tolist(), cnt.tolist())))
print("rows", rows.tolist(), "r", r.tolist()); print("cols", cols.tolist(), "c", c.tolist())
# exact replay: L^T M L with the scalings undone must equal H in the two orders
L = np.tril(np.ones((N, N), dtype=np.int64))
R = L.T @ M @ L   # R[a][b] = sum_{a'>=a, b'>=b} M  -> with our convention use upper sums
A = H[np.ix_(rows, cols)] * r[:, None] * c[None, :]
U = np.triu(np.ones((N, N), dtype=np.int64))
print("replay exact:", bool(np.array_equal(U @ M @ U.T, A)))
