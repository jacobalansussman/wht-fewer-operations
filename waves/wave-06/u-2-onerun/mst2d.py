# u-2-onerun, hatch 1 ("the spreadsheet trick", q-cross experiment 8): the inputs in an a x b TABLE with the table of running
# totals P[i][j] = sum of the inputs in rows <= i and columns <= j  (2N - a - b gates).  A difference of two outputs is then
# sum of mixed[i][j] * P[i][j], mixed = the mixed second difference of (row S - row S') drawn in the table.  Cost of joining two
# outputs = non-zeros of mixed; outputs on the cheapest tree (minimum spanning tree, vertex "nothing" = zero table).
#   gates (G) = 2N - a - b + W - (outputs hung on nothing).          a = 1 is the one-chain case of mst.py (check: 41 at 16 points).
# usage: python3 mst2d.py <k> <a> <moves> <seed>      (numpy; whole numbers)
import sys, random
import numpy as np
def W_of(k, a, b, arr, hist=False):
    N = 1 << k
    cells = np.array(arr, dtype=np.int64).reshape(a, b)
    S = np.arange(N, dtype=np.int64)[:, None, None]
    G = ((cells[None, :, :] & S) == cells[None, :, :]).astype(np.int8)
    G = np.concatenate([G, np.zeros((1, a, b), np.int8)], axis=0)            # "nothing"
    Gp = np.zeros((N + 1, a + 1, b + 1), np.int8); Gp[:, :a, :b] = G
    MD = (Gp[:, :-1, :-1] - Gp[:, 1:, :-1] - Gp[:, :-1, 1:] + Gp[:, 1:, 1:]).reshape(N + 1, a * b)
    C = np.count_nonzero(MD[:, None, :] != MD[None, :, :], axis=2)
    n = N + 1; intree = np.zeros(n, bool); best = C[N].copy(); frm = np.full(n, N); intree[N] = True; W = 0; ws = []; degbot = 0
    for _ in range(N):
        cand = np.where(intree, 10 ** 9, best); v = int(cand.argmin()); W += int(best[v]); ws.append(int(best[v])); degbot += (frm[v] == N)
        intree[v] = True; upd = C[v] < best; frm[upd & ~intree] = v; best = np.minimum(best, C[v])
    if hist:
        h = {}
        for w in ws: h[w] = h.get(w, 0) + 1
        return W, sorted(h.items()), int(degbot)
    return W
def gray(m): return [i ^ (i >> 1) for i in range(1 << m)]
if __name__ == "__main__":
    k, a, moves, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]); N = 1 << k; b = N // a
    random.seed(seed); ka = a.bit_length() - 1; kb = k - ka
    prod_count = [(i << kb) | j for i in range(a) for j in range(b)]
    prod_gray = [(gi << kb) | gj for gi in gray(ka) for gj in gray(kb)]
    out = []
    for name, arr in (("product, counting order on each side", prod_count), ("product, Gray order on each side", prod_gray)):
        W, h, d = W_of(k, a, b, arr, True); out.append((W, arr))
        print(f"N={N} table {a}x{b}: {name}: W = {W}; edges by weight {h}; gates (G) = {2*N - a - b + W - d}; Yates = {N//2*k}", flush=True)
    cur = min(out)[1][:]; curW = min(out)[0]; bestW = curW; bestarr = cur[:]
    for t in range(moves):
        c = cur[:]; i, j = random.sample(range(N), 2); r = random.random()
        if r < 0.6: c[i], c[j] = c[j], c[i]
        else:
            i, j = sorted((i, j)); c[i:j + 1] = c[i:j + 1][::-1]
        W = W_of(k, a, b, c)
        if W <= curW or random.random() < 0.01: cur, curW = c, W
        if W < bestW: bestW, bestarr = W, c[:]
    W, h, d = W_of(k, a, b, bestarr, True)
    print(f"N={N} table {a}x{b}: best after {moves} moves: W = {W}; W/N = {W/N:.3f}; edges by weight {h}; hung on nothing {d}; gates (G) = {2*N - a - b + W - d}; Yates = {N//2*k}")
    print(f"   table, row by row: {bestarr}", flush=True)
