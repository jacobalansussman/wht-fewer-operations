#!/usr/bin/env python3
"""g-1 exact8.py: EXACT minimum of the 'one merge tree + flip walk' model at 8 points (count (G)), pure Python integers.
Model (flipwalk.py): a sign vector F0, a chain of subgroups V1 < V2; tree nodes = the cosets of V1 (pairs) and of V2 (fours).
Vertices = difference sets D (D and its complement identified); a step toggles a point, or a tree node wholly inside or
wholly outside D.  Gates = 7 + (edges of the smallest tree containing the empty set and the 8 target sets).
Smallest tree: Dreyfus-Wagner dynamic programme (exact).  Symmetry used [derived]: all chains are equivalent under invertible
linear maps of the addresses (which permute the characters), and multiplying F0 by a character permutes the targets and leaves
the graph alone; so it is enough to take ONE chain and the 16 sign vectors (-1)^g, g a sum of the monomials x0x1, x0x2, x1x2,
x0x1x2.
"""
import itertools
N = 8; FULL = 255
def canon(D): return D ^ FULL if D & 1 else D
V1 = [0, 1]; V2 = [0, 1, 2, 3]
nodes = sorted({sum(1 << (x ^ c) for x in V) for V in (V1, V2) for c in range(N)})
verts = sorted({canon(D) for D in range(256)}); vid = {D: i for i, D in enumerate(verts)}; n = len(verts)
adj = [[] for _ in range(n)]
for D in verts:
    for p in range(N): adj[vid[D]].append(vid[canon(D ^ (1 << p))])
    for A in nodes:
        if D & A == 0 or D & A == A: adj[vid[D]].append(vid[canon(D ^ A)])
INF = 10 ** 9
dist = []
for s in range(n):
    d = [INF] * n; d[s] = 0; q = [s]
    for u in q:
        for v in adj[u]:
            if d[v] == INF: d[v] = d[u] + 1; q.append(v)
    dist.append(d)
def chi(j, x): return -1 if bin(j & x).count("1") & 1 else 1
results = {}
for co in itertools.product((0, 1), repeat=4):
    g = lambda x: (co[0] * (x & 1) * (x >> 1 & 1) + co[1] * (x & 1) * (x >> 2 & 1) + co[2] * (x >> 1 & 1) * (x >> 2 & 1) + co[3] * (x & 1) * (x >> 1 & 1) * (x >> 2 & 1)) & 1
    F0 = [(-1) ** g(x) for x in range(N)]
    terms = sorted({vid[canon(sum(1 << x for x in range(N) if chi(j, x) != F0[x]))] for j in range(N)} | {0})
    root = terms[0]; rest = terms[1:]; t = len(rest)
    dp = [None] * (1 << t)
    for i in range(t): dp[1 << i] = list(dist[rest[i]])
    for S in range(1, 1 << t):
        if S & (S - 1) == 0: continue
        best = [INF] * n
        sub = (S - 1) & S
        while sub:
            if sub < S ^ sub:
                a, b = dp[sub], dp[S ^ sub]
                for v in range(n):
                    c = a[v] + b[v]
                    if c < best[v]: best[v] = c
            sub = (sub - 1) & S
        # relax through the graph
        order = sorted(range(n), key=lambda v: best[v])
        out = [min(best[u] + dist[u][v] for u in order[:n]) for v in range(n)]
        dp[S] = out
    steps = dp[(1 << t) - 1][root]
    results[co] = (steps, len(terms)); print("F0 = %s (monomials x0x1,x0x2,x1x2,x0x1x2: %s): smallest tree has %d steps -> %d gates" % (F0, co, steps, 7 + steps), flush=True)
m = min(s for s, _ in results.values())
print("EXACT minimum of the one-tree flip-walk model at 8 points over all sign vectors and all chains of subgroups: %d gates (7 + %d)" % (7 + m, m))
