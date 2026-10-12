# q-cross hybrid 1, part 3: the caterpillar letter with weights that are NOT signs.
# Row scalings r_a = +-3^i, column scalings c_b = +-2^j (i, j in -2..2), stored as integers after a common factor.
# An odd 2x2 block has second difference zero when (1 +- x)(1 +- y) = 2 for the ratios x, y of its two rows and two columns,
# e.g. x = 1/3, y = 1/2.  Question: does the best count fall below the best sign count?  Exact integers.  Annealing: upper bounds.
import sys, random
k = int(sys.argv[1]); iters = int(sys.argv[2]); seeds = int(sys.argv[3]); E = int(sys.argv[4]); N = 1 << k
Hs = [[1 - 2 * (bin(a & b).count('1') & 1) for b in range(N)] for a in range(N)]
P3 = [3 ** (e + E) for e in range(-E, E + 1)]; P2 = [2 ** (e + E) for e in range(-E, E + 1)]
def nnz(rows, cols, rs, re_, cs, ce):
    A = [[rs[a] * P3[re_[a]] * cs[b] * P2[ce[b]] * Hs[rows[a]][cols[b]] for b in range(N)] + [0] for a in range(N)] + [[0] * (N + 1)]
    n = 0
    for a in range(N):
        Aa, Ab = A[a], A[a + 1]
        for b in range(N):
            if Aa[b] - Ab[b] - Aa[b + 1] + Ab[b + 1]: n += 1
    return n
overall = None
for seed in range(seeds):
    rnd = random.Random(1000 + seed)
    rows = rnd.sample(range(N), N); cols = rnd.sample(range(N), N)
    rs = [rnd.choice((-1, 1)) for _ in range(N)]; cs = [rnd.choice((-1, 1)) for _ in range(N)]
    re_ = [E] * N; ce = [E] * N          # start from pure signs
    cur = nnz(rows, cols, rs, re_, cs, ce); best = cur; keep = None
    for it in range(iters):
        T = 1.0 * (1 - it / iters) + 0.05
        m = rnd.randrange(8); undo = None
        if m < 2:
            arr = rows if m == 0 else cols; i, j = rnd.sample(range(N), 2); arr[i], arr[j] = arr[j], arr[i]
            undo = lambda arr=arr, i=i, j=j: arr.__setitem__(slice(None), [arr[j] if t == i else arr[i] if t == j else arr[t] for t in range(N)])
        elif m < 4:
            sg = rs if m == 2 else cs; i = rnd.randrange(N); sg[i] = -sg[i]
            undo = lambda sg=sg, i=i: sg.__setitem__(i, -sg[i])
        elif E > 0:
            ex = re_ if m < 6 else ce; i = rnd.randrange(N); old = ex[i]; ex[i] = rnd.randrange(2 * E + 1)
            undo = lambda ex=ex, i=i, old=old: ex.__setitem__(i, old)
        else: continue
        v = nnz(rows, cols, rs, re_, cs, ce)
        if v <= cur or rnd.random() < 2.718 ** ((cur - v) / T): cur = v
        else: undo()
        if cur < best: best = cur; keep = (rows[:], cols[:], rs[:], [e - E for e in re_], cs[:], [e - E for e in ce])
    print(f"N={N} E={E} seed={seed} best nnz={best} gates={N-2+best}", flush=True)
    if overall is None or best < overall[0]: overall = (best, keep)
print("BEST", overall[0], "gates", N - 2 + overall[0]); print(overall[1])
