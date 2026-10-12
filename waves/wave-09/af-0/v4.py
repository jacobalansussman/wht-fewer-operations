#!/usr/bin/env python3
"""af-0/v4.py  Exhaustive check of the one graph fact behind V(4) >= 14, with no theorem recalled.
FACT: a graph (loops and repeated edges allowed, two-sidedness NOT assumed) in which every vertex has degree >= 2, no
cycle is shorter than 8, and edges - vertices >= 3, has at least 18 edges.
Reduction (by hand, in the report): one may assume edges - vertices = 3 exactly and no component that is a bare
cycle.  Erase the vertices of degree 2: what is left (the 'kernel') has every degree >= 3 and still edges - vertices
= 3, hence at most 6 vertices and at most 9 edges; the graph is the kernel with edge e replaced by a path of L[e] >= 1
edges, and a cycle of the graph is a cycle of the kernel with length = sum of L over it.
This program lists EVERY kernel on 1..6 labelled vertices (no reduction by symmetry, so nothing can be missed) and for
each finds by exhaustive search the least total sum(L) with every cycle >= GIRTH."""
import sys
from itertools import combinations
GIRTH = int(sys.argv[1]) if len(sys.argv) > 1 else 8
EXC = int(sys.argv[2]) if len(sys.argv) > 2 else 3
CAP = int(sys.argv[3]) if len(sys.argv) > 3 else 24
def kernels(n):
    E = n + EXC; slots = [(i, j) for i in range(n) for j in range(i, n)]; deg = [0] * n; cur = []
    def rec(si, left):
        if left == 0:
            if min(deg) >= 3: yield list(cur)
            return
        if si == len(slots): return
        # need: remaining slots can still raise every vertex < slots[si][0] ... simple prune: vertices below i are closed
        i, j = slots[si]
        if any(deg[v] < 3 for v in range(i)): return
        for mult in range(left + 1):
            for _ in range(mult): cur.append((i, j))
            deg[i] += mult; deg[j] += mult
            yield from rec(si + 1, left - mult)
            deg[i] -= mult; deg[j] -= mult
            for _ in range(mult): cur.pop()
    yield from rec(0, E)
def cycles(n, edges):
    cyc = set()
    for e, (i, j) in enumerate(edges):
        if i == j: cyc.add(frozenset([e]))
    adj = [[] for _ in range(n)]
    for e, (i, j) in enumerate(edges):
        if i != j: adj[i].append((j, e)); adj[j].append((i, e))
    def dfs(s, v, used_v, used_e):
        for (w, e) in adj[v]:
            if e in used_e: continue
            if w == s and len(used_e) >= 1: cyc.add(frozenset(used_e | {e})); continue
            if w > s and w not in used_v: dfs(s, w, used_v | {w}, used_e | {e})
    for s in range(n): dfs(s, s, {s}, frozenset())
    return [sorted(c) for c in cyc]
def feasible(m, cyc, budget):
    """is there L[0..m-1] >= 1 with sum <= budget and every cycle sum >= GIRTH ?  exhaustive with safe pruning."""
    L = [0] * m; incyc = [[c for c in range(len(cyc)) if e in cyc[c]] for e in range(m)]
    csum = [0] * len(cyc); cleft = [len(c) for c in cyc]
    def rec(e, tot):
        if e == m: return all(s >= GIRTH for s in csum)
        rest = m - e
        for c in range(len(cyc)):                      # most this cycle can still reach
            if csum[c] + (budget - tot - (rest - cleft[c])) < GIRTH: return False
        for v in range(1, budget - tot - (rest - 1) + 1):
            for c in incyc[e]: csum[c] += v; cleft[c] -= 1
            ok = rec(e + 1, tot + v)
            for c in incyc[e]: csum[c] -= v; cleft[c] += 1
            if ok: L[e] = v; return True
        return False
    return rec(0, 0)
best = None; total = 0; seen = {}
for n in range(1, 2 * EXC + 1):
    cnt = 0; nbest = None
    for edges in kernels(n):
        cnt += 1; cyc = cycles(n, edges); m = len(edges)
        lim = (best[0] - 1) if best else CAP
        lo = None
        b = m
        # smallest feasible budget not above the best so far (ties are not needed for the minimum)
        while b <= (best[0] if best else CAP):
            if feasible(m, cyc, b): lo = b; break
            b += 1
        if lo is not None:
            if nbest is None or lo < nbest[0]: nbest = (lo, edges)
            if best is None or lo < best[0]: best = (lo, edges, n)
    total += cnt
    print("kernels on %d labelled vertices with %d edges, all degrees >= 3: %d listed; least edges found among them: %s" % (n, n + EXC, cnt, nbest), flush=True)
print("girth >= %d, edges - vertices = %d: %d kernels in all; LEAST NUMBER OF EDGES = %s" % (GIRTH, EXC, total, best))
