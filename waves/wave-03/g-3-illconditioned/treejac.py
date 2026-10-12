# treejac.py  (g-3-illconditioned)   FLOAT MEASUREMENT (singular values of a numerical Jacobian).
# At the exact two-letter tree words for 8 and 16 points (butterflies x bricks, bricks x bricks; treeexact.py), how many
# directions can the parameters move while the word stays "a +-1 orthogonal matrix after scaling rows and columns"?
# Parameters: outer diagonal r, then per letter: g (one number per internal tree node), h (diagonal), d (diagonal after it).
# Expected trivial directions: one overall scale per letter, absorbed by the neighbouring diagonal.
import numpy as np
def node_index(N, order):
    idx = np.zeros((N, N), dtype=int); dep = np.zeros((N, N), dtype=int)
    for x in range(N):
        for y in range(N):
            if x == y: continue
            pref = 0
            for j, b in enumerate(order):
                bx, by = x >> b & 1, y >> b & 1
                if bx != by: idx[x, y] = (1 << j) - 1 + pref; dep[x, y] = j; break
                pref = pref * 2 + bx
    return idx
def run(k, orders, gdepth, hs):
    N = 1 << k; m = len(orders); IDX = [node_index(N, o) for o in orders]; nB = 2 * N - 1
    def build(theta):
        K = None; pos = 0; r = theta[pos:pos + N]; pos += N
        for i in range(m):
            g = theta[pos:pos + N - 1]; h = theta[pos + N - 1:pos + nB]; pos += nB
            B = g[IDX[i]]; B[np.arange(N), np.arange(N)] = h
            d = theta[pos:pos + N]; pos += N
            K = (B * d) if K is None else (K @ B) * d
        return K * r[:, None]
    def resid(theta):
        K = build(theta); G = K @ K.T / N
        return np.concatenate([(K * K - 1).ravel(), G[np.triu_indices(N, 1)]])
    th = [np.ones(N)]
    for i in range(m):
        g = np.zeros(N - 1)
        for depth in range(k): g[(1 << depth) - 1:(1 << (depth + 1)) - 1] = gdepth[i][depth]
        th += [g, np.array([hs[i](x) for x in range(N)], dtype=float), np.ones(N)]
    th = np.concatenate(th); r0 = resid(th)
    J = np.zeros((len(r0), len(th))); e = 1e-6
    for j in range(len(th)):
        t1 = th.copy(); t1[j] += e; t2 = th.copy(); t2[j] -= e; J[:, j] = (resid(t1) - resid(t2)) / (2 * e)
    U, s, Vt = np.linalg.svd(J, full_matrices=True); null = int(np.sum(s < 1e-6 * s[0])) + max(0, len(th) - len(s))
    NS = Vt[len(th) - null:]                       # rows: a basis of the directions that keep the residual zero to first order
    zero_g = []; pos = N
    for i in range(m):
        zero_g += [pos + q for q in range(N - 1) if th[pos + q] == 0.0]; pos += nB + N
    sv = np.linalg.svd(NS[:, zero_g], compute_uv=False) if zero_g else np.array([])
    print(f"   couplings that are zero in the exact word (tree nodes above the bricks): {len(zero_g)}; "
          f"independent first-order ways to switch them on while staying a solution: {int(np.sum(sv > 1e-6))}  (singular values {sv.round(6)})")
    print(f"N={N} letters={m} orders={orders}: residual at the exact word {np.abs(r0).max():.1e}; parameters {len(th)}; "
          f"directions that keep the word a scaled +-1 orthogonal matrix to first order: {null}; of these trivial (letter scales): {m}; "
          f"smallest singular values {np.sort(s)[:6].round(8)}")
run(2, [(0, 1)], [(1, 1)], [lambda x: -1.0])
run(3, [(0, 1, 2), (2, 1, 0)], [(0, 0, 1), (0, 1, 1)], [lambda x: -1.0 if x >> 2 & 1 else 1.0, lambda x: -1.0])
run(4, [(0, 1, 2, 3), (2, 3, 0, 1)], [(0, 0, 1, 1), (0, 0, 1, 1)], [lambda x: -1.0, lambda x: -1.0])
