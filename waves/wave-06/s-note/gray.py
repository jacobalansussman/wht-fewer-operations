import sys
sys.path.insert(0, 'waves/wave-06/s-note')
def corners(rows, cols):
    N = len(rows)
    M = [[1 if (t & s) == t else 0 for t in cols] + [0] for s in rows] + [[0] * (N + 1)]
    c = 0
    for i in range(N):
        d = [M[i][j] - M[i + 1][j] for j in range(N + 1)]
        c += sum(1 for j in range(N) if d[j] != d[j + 1])
    return c
for k in range(2, 8):
    N = 1 << k; g = [i ^ (i >> 1) for i in range(N)]
    print(N, 'rows fwd/cols fwd', corners(g, g), ' fwd/rev', corners(g, g[::-1]), ' rev/fwd', corners(g[::-1], g), ' rev/rev', corners(g[::-1], g[::-1]))
