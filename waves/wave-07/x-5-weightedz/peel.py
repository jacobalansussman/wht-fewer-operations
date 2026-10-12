# x-5-weightedz / peel.py : how many "lines" can be peeled off the quadratic form x^T H x by SPARSE vectors?
# A family v_1..v_m is acceptable when v_i^T H v_j = 0 for i != j and v_i^T H v_i != 0 (pairwise H-orthogonal, none isotropic).
# Vectors: entries 0, +1, -1, support at most smax (up to a global sign). Exact integers. Largest family = largest clique,
# found by Bron-Kerbosch with pivoting on bitsets; a time limit turns the answer into a lower bound (printed as such).
import sys, time
from itertools import combinations, product
pc = lambda x: bin(x).count("1")
def run(k, smax, limit):
    N = 1 << k
    Hm = [[(-1) ** pc(S & T) for T in range(N)] for S in range(N)]
    vecs = []
    for s in range(1, smax + 1):
        for supp in combinations(range(N), s):
            for signs in product((1, -1), repeat=s - 1):
                v = ((supp[0], 1),) + tuple(zip(supp[1:], signs))
                nrm = sum(a * b * Hm[S][T] for S, a in v for T, b in v)
                if nrm != 0: vecs.append(v)
    n = len(vecs)
    Hv = []
    for v in vecs:
        Hv.append([sum(a * Hm[S][T] for S, a in v) for T in range(N)])
    adj = [0] * n
    for i in range(n):
        hi = Hv[i]
        for j in range(i + 1, n):
            if sum(b * hi[T] for T, b in vecs[j]) == 0:
                adj[i] |= 1 << j; adj[j] |= 1 << i
    best = [0, None]; t0 = time.time(); out = [False]
    def bk(R, P, X, size):
        if time.time() - t0 > limit: out[0] = True; return
        if P == 0 and X == 0:
            if size > best[0]: best[0] = size; best[1] = R
            return
        if size + pc(P) <= best[0]: return
        # pivot: vertex of P|X with most neighbours in P
        PX = P | X; bu = -1; bc = -1; q = PX
        while q:
            u = (q & -q).bit_length() - 1; q &= q - 1
            c = pc(P & adj[u])
            if c > bc: bc = c; bu = u
        cand = P & ~adj[bu]
        while cand:
            v = (cand & -cand).bit_length() - 1; cand &= cand - 1
            bk(R | (1 << v), P & adj[v], X & adj[v], size + 1)
            P &= ~(1 << v); X |= 1 << v
            if out[0]: return
    sys.setrecursionlimit(10000)
    bk(0, (1 << n) - 1, 0, 0)
    fam = [vecs[i] for i in range(n) if best[1] is not None and (best[1] >> i) & 1]
    print("k=%d N=%d support<=%d: %d non-isotropic vectors; largest pairwise H-orthogonal family %s %d  (N/4 = %d, N/2 = %d, N = %d)  [%.0f s]" % (
        k, N, smax, n, ">=" if out[0] else "=", best[0], N // 4, N // 2, N, time.time() - t0))
    sizes = {}
    for v in fam: sizes[len(v)] = sizes.get(len(v), 0) + 1
    print("    supports in that family: %s ; covering sum of s(s-1)/2 = %d of the %d pairs" % (sorted(sizes.items()), sum(len(v) * (len(v) - 1) // 2 for v in fam), N * (N - 1) // 2))
    if N <= 16:
        for v in fam: print("     ", " ".join("%+d*e[%s]" % (a, format(S, "0%db" % k)) for S, a in v))
    sys.stdout.flush()
k = int(sys.argv[1]); smax = int(sys.argv[2]); limit = float(sys.argv[3])
run(k, smax, limit)
