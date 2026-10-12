# s-pick: corners of the subset-sum picture counted MODULO 2 (odd second differences only; a checkerboard window 10/01 gives +-2 and is free).
# Upper bounds from a small annealer over both orders (signs do not matter modulo 2).  Pure Python, whole numbers.
# Cost is a sum over neighbouring rows: w(S,S') = number of b with D[b] != D[b+1] modulo 2, D = row S xor row S' in the column order, D[N] = 0.
import random, itertools
def run(k, iters, seeds):
    N = 1 << k
    def pic(rows, cols): return [[1 if (r & c) == c else 0 for c in cols] + [0] for r in rows] + [[0] * (N + 1)]
    def M_of(rows, cols):
        A = pic(rows, cols); return [[A[a][b] - A[a + 1][b] - A[a][b + 1] + A[a + 1][b + 1] for b in range(N)] for a in range(N)]
    def odd(rows, cols): return sum(1 for r in M_of(rows, cols) for v in r if v & 1)
    best = None
    if k == 2:
        for rows in itertools.permutations(range(N)):
            for cols in itertools.permutations(range(N)):
                v = odd(rows, cols)
                if best is None or v < best[0]: best = (v, list(rows), list(cols))
    else:
        for seed in range(seeds):
            rnd = random.Random(seed); rows = rnd.sample(range(N), N); cols = rnd.sample(range(N), N); cur = odd(rows, cols)
            for it in range(iters):
                T = 1.0 * (1 - it / iters) + 0.05; arr = rows if rnd.random() < .5 else cols
                if rnd.random() < .5:
                    i, j = rnd.sample(range(N), 2); arr[i], arr[j] = arr[j], arr[i]; v = odd(rows, cols)
                    if v <= cur or rnd.random() < 2.718 ** ((cur - v) / T): cur = v
                    else: arr[i], arr[j] = arr[j], arr[i]
                else:
                    i, j = sorted(rnd.sample(range(N + 1), 2)); seg = arr[i:j]; arr[i:j] = seg[::-1]; v = odd(rows, cols)
                    if v <= cur or rnd.random() < 2.718 ** ((cur - v) / T): cur = v
                    else: arr[i:j] = seg
                if best is None or cur < best[0]: best = (cur, list(rows), list(cols))
    M = M_of(best[1], best[2]); A = pic(best[1], best[2])
    ok = all(sum(M[a2][b2] & 1 for a2 in range(a, N) for b2 in range(b, N)) % 2 == A[a][b] for a in range(N) for b in range(N))
    print(f"N={N}: odd corners {best[0]} (XOR gates {N - 2 + best[0]}; Yates {N // 2 * k}); whole-number corners of the same orders {sum(1 for r in M for v in r if v)}; entries +-2: {sum(1 for r in M for v in r if abs(v) == 2)}; picture rebuilt modulo 2: {ok}")
    print("   rows", best[1]); print("   cols", best[2], flush=True)
run(2, 0, 0); run(3, 40000, 3); run(4, 25000, 2)
