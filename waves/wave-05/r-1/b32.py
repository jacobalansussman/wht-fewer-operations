# r-1: p-1's design with B = 32 at 16 points, recomputed with my own t' (whole numbers, doubled units).
def tsp(f, wl=1, wi=2):
    vals = sorted(set(f) | {0}); memo = {}
    def g(lo, hi, off):
        key = (lo, hi, off)
        if key in memo: return memo[key]
        if hi - lo == 1: r = 0 if f[lo] == off else wl
        else:
            mid = (lo + hi) // 2
            r = min((0 if o == off else wi) + g(lo, mid, o) + g(mid, hi, o) for o in vals)
        memo[key] = r; return r
    return g(0, len(f), 0)
def rev(x, k): return int(format(x, '0%db' % k)[::-1], 2)
r = [1, -1, 1, -1, -1, 1, 1, -1, -1, -1, -1, -1, 1, 1, -1, -1]; c = [1, -1, 1, 1, 1, 1, -1, 1, 1, 1, 1, -1, 1, -1, -1, -1]
N = 16; M = [[r[y] * c[rev(x, 4)] * (-1) ** bin(y & rev(x, 4)).count('1') for x in range(N)] for y in range(N)]
rows = sum(tsp(tuple(M[p][x] - M[p + 1][x] for x in range(N))) for p in range(0, N, 2))
cols = sum(tsp(tuple(M[y][p] - M[y][p + 1] for y in range(N))) for p in range(0, N, 2))
print("p-1's design 'bound32': rows", rows / 2, " columns", cols / 2, " B =", (rows + cols) / 2)
