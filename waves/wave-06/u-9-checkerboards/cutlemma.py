# u-9: check of the cut-crossing lemma for B[y][x] = parity of common ones (H = J - 2B; odd corners of B = value-2 cells of H).
# Claim [derived]: for ANY two spanning trees on the addresses (chains are the special case), with row edges d = y+y' and column
# edges e = x+x', the number of pairs (row edge, column edge) with d.e = 1 (mod 2) is at least k 2^(k-1) = (N/2) log2 N.
# In a two-chain picture that number is the count of odd second differences away from the added zero row and column.
import itertools, sys
def par(v): return bin(v).count("1") & 1
def check(k):
    N = 1 << k
    G = [[par(d & e) for e in range(N)] for d in range(N)]
    # (a) all Hamiltonian paths (chains): distinct step-count vectors
    fs_path = set()
    if k <= 3:
        for p in itertools.permutations(range(N)):
            f = [0] * N
            for a in range(N - 1): f[p[a] ^ p[a + 1]] += 1
            fs_path.add(tuple(f))
    # (b) all spanning trees through Pruefer codes (N^(N-2) of them): distinct edge-count vectors
    fs_tree = set()
    if k <= 3:
        for code in itertools.product(range(N), repeat=N - 2):
            deg = [1] * N
            for c in code: deg[c] += 1
            f = [0] * N; deg = deg[:]
            for c in code:
                leaf = min(i for i in range(N) if deg[i] == 1)
                f[leaf ^ c] += 1; deg[leaf] -= 1; deg[c] -= 1
            u, v = [i for i in range(N) if deg[i] == 1]
            f[u ^ v] += 1
            fs_tree.add(tuple(f))
    def best(fs):
        fs = list(fs); gv = [[sum(G[d][e] * g[e] for e in range(N)) for d in range(N)] for g in fs]  # c(d) for each column tree
        m = None; arg = None
        for f in fs:
            for gi, cv in enumerate(gv):
                v = sum(f[d] * cv[d] for d in range(N) if f[d])
                if m is None or v < m: m = v; arg = (f, fs[gi])
        return m, arg
    mp, ap = best(fs_path); mt, at = best(fs_tree)
    print(f"N={N}: (N/2) log2 N = {k * N // 2}; least over ALL pairs of chains = {mp} ({len(fs_path)} step-count vectors); least over ALL pairs of spanning trees = {mt} ({len(fs_tree)} edge-count vectors)")
    print("   a best pair of chains, step counts by direction:", {d: c for d, c in enumerate(ap[0]) if c}, {d: c for d, c in enumerate(ap[1]) if c})
    print("   a best pair of trees, edge counts by direction:", {d: c for d, c in enumerate(at[0]) if c}, {d: c for d, c in enumerate(at[1]) if c}, flush=True)
check(2); check(3)
