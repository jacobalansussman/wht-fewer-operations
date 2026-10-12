# u-2-onerun, mutation "outputs in a tree": for ONE order of the inputs, the cheapest way to make every output from another
# output (or from nothing) plus prefix sums is a minimum spanning tree of the outputs under the distance
#   w(S, S') = number of places where  row S - row S'  changes value along the input order (the right end counts)
# with one extra vertex "nothing" (the zero row).  Circuit: N - 1 running sums, then one gate per unit of tree weight, minus one
# for each output hung directly on "nothing":   gates (G) = N - 1 + W - deg(nothing).
# The path version (q-cross's corners) is the same with "shortest Hamiltonian path" in place of "minimum spanning tree", so
# W <= corners always.  This program: W for given orders, and a hill-climb over the input order alone.
# usage: python3 mst.py <k> <moves> <seed>
import sys, random, ast
def weight(k, cols, want_tree=False):
    N = 1 << k
    rowmask = []
    for S in range(N):
        m = 0
        for b in range(N):
            if cols[b] & S == cols[b]: m |= 1 << b
        rowmask.append(m)
    rowmask.append(0)                      # "nothing"
    def w(i, j):
        P = rowmask[i] & ~rowmask[j]; Q = rowmask[j] & ~rowmask[i]
        return bin((P ^ (P >> 1)) | (Q ^ (Q >> 1))).count('1')
    n = N + 1; INF = 10 ** 9
    best = [INF] * n; frm = [-1] * n; intree = [False] * n
    best[N] = 0; W = 0; edges = []
    for _ in range(n):
        v = min((x for x in range(n) if not intree[x]), key=lambda x: best[x])
        intree[v] = True; W += best[v]
        if frm[v] >= 0: edges.append((frm[v], v, best[v]))
        for u in range(n):
            if not intree[u]:
                d = w(v, u)
                if d < best[u]: best[u] = d; frm[u] = v
    return (W, edges) if want_tree else W
def gray(k): return [i ^ (i >> 1) for i in range(1 << k)]
if __name__ == "__main__":
    k = int(sys.argv[1]); moves = int(sys.argv[2]); seed = int(sys.argv[3]); N = 1 << k
    random.seed(seed)
    print(f"N={N}: Yates {N//2*k}; a tree of one-run steps would have weight at most 2N = {2*N}")
    print(f"  input order = counting order: W = {weight(k, list(range(N)))};  Gray order: W = {weight(k, gray(k))}")
    try:
        f = {2: 'cat3_4.out', 3: 'cat3_8.out', 4: 'cat3_16.out', 5: 'cat3_32.out', 6: 'cat3g_64.out'}[k]
        txt = open('waves/wave-05/q-cross/' + f).read().split('BEST')[-1]
        qc = ast.literal_eval(txt.split('cols ')[1].split(' c ')[0]); print(f"  input order of q-cross's best picture ({f}): W = {weight(k, qc)}")
    except Exception as ex: qc = None
    cur = qc[:] if qc else gray(k); curW = weight(k, cur); bestW = curW; bestc = cur[:]
    for t in range(moves):
        c = cur[:]; i, j = sorted(random.sample(range(N), 2)); r = random.random()
        if r < 0.4: c[i], c[j] = c[j], c[i]
        elif r < 0.8: c[i:j + 1] = c[i:j + 1][::-1]
        else: x = c.pop(i); c.insert(j, x)
        W = weight(k, c)
        if W <= curW or random.random() < 0.02: cur, curW = c, W
        if W < bestW: bestW, bestc = W, c[:]; print(f"    move {t}: W = {W}", flush=True)
    W, edges = weight(k, bestc, True)
    degbot = sum(1 for (a, b, d) in edges if a == N or b == N)
    hist = {}
    for (a, b, d) in edges: hist[d] = hist.get(d, 0) + 1
    print(f"  best after {moves} moves: W = {bestW}; W/N = {bestW/N:.3f}; edges by weight {sorted(hist.items())}; outputs hung on nothing {degbot}; gates (G) = {N - 1 + W - degbot}")
    print(f"  input order: {bestc}")
