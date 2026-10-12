# q-cross hybrid 1: the caterpillar letter. Rows in one order, columns in another, sign scalings r, c.
# A[a][b] = r[a] c[b] (-1)^(y_a . x_b);  M = mixed second difference (A padded with zeros);  H = L^T M L (L = prefix sums)
# gates (G) = N - 2 + nnz(M).   Exact integers.
import sys, random, itertools
def gray(k): return [i ^ (i >> 1) for i in range(1 << k)]
def bitrev(v, k): return int(format(v, '0%db' % k)[::-1], 2)
def dot(a, b): return bin(a & b).count('1') & 1
def nnzM(rows, cols, r, c):
    N = len(rows)
    A = [[r[a] * c[b] * (1 - 2 * dot(rows[a], cols[b])) for b in range(N)] + [0] for a in range(N)] + [[0] * (N + 1)]
    n = 0; kinds = {}
    for a in range(N):
        for b in range(N):
            m = A[a][b] - A[a + 1][b] - A[a][b + 1] + A[a + 1][b + 1]
            if m: n += 1; kinds[m] = kinds.get(m, 0) + 1
    return n, kinds
def anneal_signs(rows, cols, iters, seed):
    rnd = random.Random(seed); N = len(rows)
    # start: normalise last row and last column to +1
    r = [1 - 2 * dot(rows[a], cols[N - 1]) for a in range(N)]
    c = [(1 - 2 * dot(rows[N - 1], cols[b])) * r[N - 1] for b in range(N)]
    best, _ = nnzM(rows, cols, r, c); cur = best; br, bc = r[:], c[:]
    start = best
    for it in range(iters):
        i = rnd.randrange(2 * N)
        if i < N: r[i] = -r[i]
        else: c[i - N] = -c[i - N]
        v, _ = nnzM(rows, cols, r, c)
        if v <= cur or rnd.random() < 0.02: cur = v
        else:
            if i < N: r[i] = -r[i]
            else: c[i - N] = -c[i - N]
        if cur < best: best = cur; br, bc = r[:], c[:]
    return start, best, br, bc
for k in (2, 3, 4, 5, 6):
    N = 1 << k
    g = gray(k)
    designs = {'gray x gray': (g, g), 'gray x bit-reversed gray': (g, [bitrev(v, k) for v in g]),
               'binary x bit-reversed binary': (list(range(N)), [bitrev(v, k) for v in range(N)])}
    for name, (rows, cols) in designs.items():
        it = 4000 if k <= 4 else (1500 if k == 5 else 300)
        start, best, br, bc = anneal_signs(rows, cols, it, 1)
        n, kinds = nnzM(rows, cols, br, bc)
        print(f"N={N:3d} {name:30s} nnz(pivot signs)={start:5d} best signs={best:5d} gates={N-2+best:5d} "
              f"(N/2)log2N+1={N//2*k+1:4d} textbook={N*k:4d} values={sorted(kinds.items())}", flush=True)
