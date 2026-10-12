#!/usr/bin/env python3
"""ports2.py [x-6-unitasbox]  Exact whole numbers.  PORTS OF DIMENSION 2: a 2-dimensional subspace P of the addresses and a
complement L such that  K^(tensor h) = (a map keeping every coset of L) x (a map keeping every coset of P).
Test [derived, as in ports.py]: every block T[rows in one coset of L, columns in one coset of P] has rank at most 1."""
import itertools
def tens(K, h):
    N = 1 << h; M = [[1] * N for _ in range(N)]
    for a in range(N):
        for x in range(N):
            p = 1
            for j in range(h): p *= K[a >> j & 1][x >> j & 1]
            M[a][x] = p
    return M
par = lambda x: bin(x).count("1") & 1
def span(vs):
    S = {0}
    for z in vs: S |= {s ^ z for s in S}
    return frozenset(S)
def subspaces(h, d):
    N = 1 << h; out = set()
    for vs in itertools.combinations(range(1, N), d):
        S = span(vs)
        if len(S) == 1 << d: out.add(S)
    return sorted(out, key=sorted)
def rank1(rows):
    piv = next((r for r in rows if any(r)), None)
    if piv is None: return True
    j = next(i for i, t in enumerate(piv) if t)
    return all(all(r[i] * piv[j] == r[j] * piv[i] for i in range(len(piv))) for r in rows)
def ports(M, h, r):
    N = 1 << h; out = []
    Ps = subspaces(h, r); Ls = subspaces(h, h - r)
    for P in Ps:
        for L in Ls:
            if len(P & L) != 1: continue
            cosL = {frozenset(a ^ l for l in L) for a in range(N)}; cosP = {frozenset(x ^ p for p in P) for x in range(N)}
            if all(rank1([[M[a][x] for x in sorted(Q)] for a in sorted(C)]) for C in cosL for Q in cosP): out.append((P, L))
    return out
for h in (4, 5):
    for name, K in (("transform [[1,1],[1,-1]]", [[1, 1], [1, -1]]), ("generic [[1,2],[3,5]]", [[1, 2], [3, 5]]), ("subset sums [[1,0],[1,1]]", [[1, 0], [1, 1]])):
        P2 = ports(tens(K, h), h, 2)
        perp = lambda P: frozenset(a for a in range(1 << h) if all(par(a & p) == 0 for p in P))
        kinds = {}
        for P, L in P2:
            odd = sum(1 for p in P if par(p & p)); kinds[odd] = kinds.get(odd, 0) + 1
        print("h=%d  %-28s ports of dimension 2: %3d ; complement = P-perp for all: %s ; by number of odd words in P: %s"
              % (h, name, len(P2), all(L == perp(P) for P, L in P2), kinds))
        if "transform" in name:
            Pl = [P for P, L in P2]
            deg = sorted({sum(1 for Q in Pl if Q != P and all(par(a & b) == 0 for a in P for b in Q)) for P in Pl})
            print("       each port of dimension 2 knows this many others (P_s inside P_t-perp):", deg, "; ports sharing a non-zero word with a given one (cannot know it): about",
                  sum(1 for Q in Pl if Q != Pl[0] and len(Q & Pl[0]) > 1))
