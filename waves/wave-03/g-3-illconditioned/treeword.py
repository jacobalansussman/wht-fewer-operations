# treeword.py  (g-3-illconditioned)   FLOATING POINT SEARCH: a hit is a candidate until rebuilt exactly.
# Question: is the N-point transform (up to scalings of rows and columns and any relabelling) a short word
#     K = B_1 D_1 B_2 D_2 ... B_m
# where D_i is any diagonal and B_i is a "tree matrix": B[x][y] = g(least common ancestor of x and y) for x != y, B[x][x] = h(x),
# for a binary tree over the N points given by an order of the address bits (first bit of the order = top split)?
# A tree matrix costs about 3N to 4N gates in count (G) (sums up the tree, then down), it is badly conditioned in general,
# and the Potts matrix t*I + (J - I) is the case g = 1, h = t.  The 4-point transform is ONE tree matrix (the 7-gate brick).
# Residual (zero exactly when K is a +-1 matrix with orthogonal rows after scaling rows and columns):
#   every entry of K squared minus 1 (K includes a diagonal on each side), and the off-diagonal part of K K^T / N.
# usage: treeword.py k m starts seed order1 order2 ...   (orders like 012, 210)
import sys, numpy as np
from scipy.optimize import least_squares
k = int(sys.argv[1]); m = int(sys.argv[2]); starts = int(sys.argv[3]); seed = int(sys.argv[4]); orders = [tuple(int(c) for c in o) for o in sys.argv[5:5 + m]]
N = 1 << k
def node_index(order):
    idx = np.zeros((N, N), dtype=int)
    for x in range(N):
        for y in range(N):
            if x == y: continue
            pref = 0
            for j, b in enumerate(order):
                bx, by = x >> b & 1, y >> b & 1
                if bx != by: idx[x, y] = (1 << j) - 1 + pref; break
                pref = pref * 2 + bx
    return idx
IDX = [node_index(o) for o in orders]
npar_B = (N - 1) + N
def build(theta):
    K = None; pos = 0
    r = theta[pos:pos + N]; pos += N
    for i in range(m):
        g = theta[pos:pos + N - 1]; h = theta[pos + N - 1:pos + npar_B]; pos += npar_B
        B = g[IDX[i]]; B[np.arange(N), np.arange(N)] = h
        d = theta[pos:pos + N]; pos += N
        K = (B * d) if K is None else (K @ B) * d
    return K * r[:, None]
npar = N + m * (npar_B + N)
def resid(theta):     # smooth: K (with its outer diagonals) should have every entry squared equal to 1 and orthogonal rows
    K = build(theta); G = K @ K.T / N
    return np.concatenate([(K * K - 1).ravel(), G[np.triu_indices(N, 1)]])
rng = np.random.default_rng(seed); best = 1e99; hist = []
for s in range(starts):
    th0 = rng.normal(size=npar) * rng.choice([0.5, 1.0, 2.0])
    try: r = least_squares(resid, th0, method="lm", max_nfev=4000, xtol=1e-15, ftol=1e-15, gtol=1e-15)
    except Exception as e: continue
    c = float(np.sum(r.fun ** 2)); hist.append(c)
    if len(hist) % 10 == 0: print(f'  progress: {len(hist)} starts, least squared residual so far {min(hist):.3e}', flush=True)
    if c < best:
        best = c; bt = r.x
hist.sort()
print(f"N={N} letters m={m} orders={orders} parameters={npar} conditions={N*N + N*(N-1)//2} starts={len(hist)}: least squared residual {best:.3e}; "
      f"five best {['%.2e' % h for h in hist[:5]]}; runs below 1e-18: {sum(h < 1e-18 for h in hist)}")
if best < 1e-18:
    S = build(bt)
    np.set_printoptions(precision=4, suppress=True, linewidth=200)
    print("candidate K after scaling (should be +-1):"); print(S)
    print("parameters:"); print(bt)
