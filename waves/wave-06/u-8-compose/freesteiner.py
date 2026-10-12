# u-8-compose: the root of a one-centre circuit WITHOUT the agreement rule.
# Vertices: sign vectors on N points up to a global sign.  One move: change the sign on one node of the bit-order merge tree
# (a single point, an aligned pair, an aligned block of 4, ...; not the whole set).  Terminals: the N rows of the transform.
# Exact least number of moves in a tree that joins all terminals, Steiner vertices free (Dreyfus-Wagner dynamic programme).
# A one-centre circuit on this tree has N - 1 joins and at least this many shifts, whatever its centre and whatever partners it holds.
import sys
from collections import deque
N = int(sys.argv[1]); k = N.bit_length() - 1
def norm(m): return m ^ ((1 << N) - 1) if m & 1 else m      # global sign: make point 0 positive
nodes = []
s = 1
while s < N:
    for a in range(0, N, s): nodes.append(sum(1 << x for x in range(a, a + s)))
    s *= 2
moves = sorted({m for m in nodes})
verts = sorted({norm(v) for v in range(1 << N)}) if N <= 8 else None
idx = {v: i for i, v in enumerate(verts)}; V = len(verts)
adj = [[idx[norm(v ^ m)] for m in moves] for v in verts]
def bfs(src):
    d = [-1] * V; d[src] = 0; q = deque([src])
    while q:
        u = q.popleft()
        for w in adj[u]:
            if d[w] < 0: d[w] = d[u] + 1; q.append(w)
    return d
rows = [norm(sum(1 << x for x in range(N) if bin(y & x).count('1') & 1)) for y in range(N)]
T = [idx[r] for r in rows]; assert len(set(T)) == N
dist = [bfs(u) for u in range(V)]
# minimum spanning tree of the terminals in this metric
import itertools
inT = {0}; mst = 0
while len(inT) < N:
    c, j = min((dist[T[i]][T[j]], j) for i in inT for j in range(N) if j not in inT); mst += c; inT.add(j)
full = (1 << N) - 1; INF = 10 ** 9
dp = [None] * (1 << N)
for i in range(N): dp[1 << i] = dist[T[i]][:]
for S in range(1, 1 << N):
    if S & (S - 1) == 0: continue
    best = [INF] * V
    low = S & -S; sub = (S - 1) & S
    while sub:
        if sub & low:
            a, b = dp[sub], dp[S ^ sub]
            for v in range(V):
                c = a[v] + b[v]
                if c < best[v]: best[v] = c
        sub = (sub - 1) & S
    # relax through the metric closure (Dijkstra-free: unit graph, use bucketed multi-source BFS)
    order = sorted(range(V), key=lambda v: best[v]); d = best[:]
    buckets = {}
    for v in range(V): buckets.setdefault(d[v], []).append(v)
    c = min(buckets)
    mx = max(buckets)
    while c <= mx + V:
        for u in buckets.get(c, []):
            if d[u] != c: continue
            for w in adj[u]:
                if d[w] > c + 1: d[w] = c + 1; buckets.setdefault(c + 1, []).append(w)
        c += 1
        if c > max(buckets): break
    dp[S] = d
print('N = %d  vertices %d  moves %d  spanning tree of the %d rows: %d moves   exact Steiner minimum: %d moves   (N/2) log2 N = %d'
      % (N, V, len(moves), N, mst, min(dp[full]), N * k // 2))
print('   so a one-centre circuit on the bit-order tree has at least %d gates, agreement rule or not; floor N - 1 + (N/2) log2 N = %d'
      % (N - 1 + min(dp[full]), N - 1 + N * k // 2))
