# ports6.py [z-1]: my own port test (x-6's definition: every block T[coset of L, coset of P] has rank <= 1, P and L complementary),
# pushed to h = 6, and the "knows" graphs of fat ports.  Exact whole numbers.
import itertools, random, sys, time
par = lambda x: bin(x).count("1") & 1
def span(vs):
    S = [0]
    for z in vs:
        if z in S: return None
        S = S + [s ^ z for s in S]
    return frozenset(S)
def subspaces(h, d):
    out = set()
    for vs in itertools.combinations(range(1, 1 << h), d):
        S = span(vs)
        if S is not None: out.add(S)
    return list(out)
def perp(P, h): return frozenset(a for a in range(1 << h) if all(par(a & p) == 0 for p in P))
def nondeg(P): return sum(1 for s in P if all(par(s & t) == 0 for t in P)) == 1
def tens(K, h):
    N = 1 << h
    T = [[1] * N for _ in range(N)]
    for a in range(N):
        for x in range(N):
            p = 1
            for j in range(h): p *= K[a >> j & 1][x >> j & 1]
            T[a][x] = p
    return T
def is_port(T, P, L):
    Pl, Ll = sorted(P), sorted(L)
    for p0 in Pl:                      # cosets of L have their representatives in P
        rows = [p0 ^ l for l in Ll]
        for l0 in Ll:                  # cosets of P have their representatives in L
            cols = [l0 ^ p for p in Pl]
            piv = None
            for a in rows:
                Ta = T[a]; r = [Ta[x] for x in cols]
                if piv is None:
                    if any(r): piv = r; j = next(i for i, t in enumerate(r) if t)
                    continue
                for i in range(len(r)):
                    if r[i] * piv[j] != r[j] * piv[i]: return False
    return True
t0 = time.time()
print("== A. ports by the rank test, all complementary pairs (P, L)")
for h, rs in ((4, (1, 2)), (5, (1, 2)), (6, (1, 2, 3))):
    subs = {d: subspaces(h, d) for d in set(rs) | {h - r for r in rs}}
    for name, K in (("transform", [[1, 1], [1, -1]]), ("generic [[1,2],[3,5]]", [[1, 2], [3, 5]]), ("subset sums", [[1, 0], [1, 1]])):
        T = tens(K, h)
        for r in rs:
            if r == 3 and name != "transform": continue
            found = []; pairs = 0
            for P in subs[r]:
                for L in subs[h - r]:
                    if len(P & L) != 1: continue
                    pairs += 1
                    if is_port(T, P, L): found.append((P, L))
            nd = sum(1 for P in subs[r] if nondeg(P))
            print("h=%d r=%d %-22s complementary pairs tested %7d ; ports %4d ; all have L = P-perp: %s ; set of P = set of subspaces meeting their perp in 0 (%d of %d): %s   [%.0fs]"
                  % (h, r, name, pairs, len(found), all(L == perp(P, h) for P, L in found), nd, len(subs[r]), {P for P, L in found} == {P for P in subs[r] if nondeg(P)}, time.time() - t0), flush=True)
print("== B. the knows graph of fat ports: vertices = ports of dimension r, edge = every word of one is orthogonal to every word of the other")
random.seed(1)
for h, r in ((4, 2), (5, 2), (6, 2), (6, 3), (7, 3)):
    V = [P for P in subspaces(h, r) if nondeg(P)]
    n = len(V); idx = {P: i for i, P in enumerate(V)}
    gens = []
    for P in V:
        g = []
        for s in sorted(P):
            if s and span(g + [s]) is not None and len(span(g + [s])) > len(span(g)) : g.append(s)
        gens.append(g)
    adj = [set() for _ in range(n)]
    for i in range(n):
        gi = gens[i]
        for j in range(i + 1, n):
            if all(par(a & b) == 0 for a in gi for b in gens[j]): adj[i].add(j); adj[j].add(i)
    degs = sorted({len(a) for a in adj})
    tri = sum(1 for i in range(n) for j in adj[i] if j > i for k in adj[i] & adj[j] if k > j)
    # bipartite? components
    col = [-1] * n; comps = 0; bip = True
    for s in range(n):
        if col[s] >= 0: continue
        comps += 1; col[s] = 0; st = [s]
        while st:
            u = st.pop()
            for w in adj[u]:
                if col[w] < 0: col[w] = 1 - col[u]; st.append(w)
                elif col[w] == col[u]: bip = False
    best = 0
    for _ in range(300 if n < 2000 else 20):
        order = list(range(n)); random.shuffle(order); order.sort(key=lambda u: len(adj[u]) + random.random())
        free = [True] * n; c = 0
        for u in order:
            if free[u]:
                c += 1; free[u] = False
                for w in adj[u]: free[w] = False
        best = max(best, c)
    print("h=%d r=%d : ports %5d ; degrees %s ; triangles %d ; components %d ; bipartite %s ; an independent set of size %d found, so rank(M) >= %d and kappa <= %.3f ; thresholds: five-stage 5h/4r = %.3f, three-stage 3h/2r = %.3f   [%.0fs]"
          % (h, r, n, degs, tri, comps, bip, best, best, n / best, 5 * h / (4 * r), 3 * h / (2 * r), time.time() - t0), flush=True)
