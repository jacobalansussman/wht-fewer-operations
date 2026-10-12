#!/usr/bin/env python3
"""p-6-selftranspose / general.py  (count (G))
Model C: G = J + sum over a partial matching of ONE merge tree of  c * (1_A 1_B^T + 1_B 1_A^T)  or  c * 1_A 1_A^T,
A != B ANY two nodes (nested or disjoint), c in COEF, each node used at most once, root = the square J (coefficient 1).
G must be a +-1 matrix with orthogonal rows.  Overlaps allowed.  Exhaustive DFS, integers only.
usage: general.py N coef,coef,... [first shape] [last shape]
"""
import sys, time
from tiling import shapes_c, nodes_of, describe
N = int(sys.argv[1]); COEF = [int(c) for c in sys.argv[2].split(",")]
lo = int(sys.argv[3]) if len(sys.argv) > 3 else 0
hi = int(sys.argv[4]) if len(sys.argv) > 4 else 10**9
FULL = (1 << N) - 1
def run(shape):
    nodes = [m for m in nodes_of(shape) if m != FULL]
    K = len(nodes)
    mem = [[x for x in range(N) if m >> x & 1] for m in nodes]
    anc = [[i for i in range(K) if nodes[i] >> x & 1] for x in range(N)]
    low = [m[0] for m in mem]
    V = [[1] * N for _ in range(N)]
    state = [None] * K
    best = [10**9]; sols = []; visited = [0]
    def add(i, j, c):
        if i == j:
            for x in mem[i]:
                r = V[x]
                for y in mem[i]: r[y] += c
        else:
            for x in mem[i]:
                r = V[x]
                for y in mem[j]: r[y] += c
            for x in mem[j]:
                r = V[x]
                for y in mem[i]: r[y] += c
    def leaf(x, nused):
        if x == N:
            visited[0] += 1
            if nused + 1 <= best[0]:
                if nused + 1 < best[0]: sols.clear()
                best[0] = nused + 1
                sols.append([(i, s, c) for i, (s, c) in enumerate(st2) if s is not None and s >= i])
            return
        todo = [i for i in anc[x] if state[i] is None]
        assign(x, todo, 0, nused)
    st2 = [(None, 0)] * K
    def assign(x, todo, t, nused):
        if t == len(todo):
            r = V[x]
            for v in r:
                if v != 1 and v != -1: return
            for y in range(x):
                q = V[y]
                if sum(a * b for a, b in zip(r, q)) != 0: return
            leaf(x + 1, nused); return
        i = todo[t]
        if state[i] is not None:
            assign(x, todo, t + 1, nused); return
        state[i] = -1
        assign(x, todo, t + 1, nused)
        for c in COEF:
            state[i] = i; st2[i] = (i, c); add(i, i, c)
            assign(x, todo, t + 1, nused + 1)
            add(i, i, -c); st2[i] = (None, 0)
        for j in range(K):
            if state[j] is None and j != i and low[j] >= x:
                for c in COEF:
                    state[i] = j; state[j] = i; st2[i] = (j, c); add(i, j, c)
                    assign(x, todo, t + 1, nused + 2)
                    add(i, j, -c); st2[i] = (None, 0); state[j] = None
        state[i] = None
    leaf(0, 0)
    return nodes, best[0], sols, visited[0]
def nm(m): return "{" + ",".join(str(x) for x in range(N) if m >> x & 1) + "}"
t0 = time.time()
S = shapes_c(N)
print("N =", N, "shapes", len(S), "coefficients", COEF, " model C (root square 1; any pairs, overlaps allowed)")
for k, sh in enumerate(S):
    if k < lo or k > hi: continue
    nodes, b, sols, vis = run(sh)
    if sols:
        print("shape %3d %s : least N' = %d (gates %d), %d at the least, %d Hadamard forms visited, %.0fs" % (k, describe(sh), b, N - 2 + b, len(sols), vis, time.time() - t0))
        for s in sols[:3]:
            print("     J " + " ".join(("%+d*%s^2" % (c, nm(nodes[i]))) if i == j else ("%+d*%s*%s" % (c, nm(nodes[i]), nm(nodes[j]))) for i, j, c in s))
    else:
        print("shape %3d %s : NONE   %.0fs" % (k, describe(sh), time.time() - t0))
    sys.stdout.flush()
