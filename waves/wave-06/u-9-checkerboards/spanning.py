# u-9: test of the spanning theorem at 16, 32, 64 points.  For a merge tree T on the inputs and a direction d, c(d) = least number
# of nodes of T (the whole set free) whose exclusive-or is the set {x : d.x = 1} (Fitch's count on the tree).  The cheapest tree
# that joins the N rows of the parity matrix without junction points is a minimum spanning tree for the distance c(y + y').
# Claim [derived]: it is at least (N/2) log2 N for every T.  Random trees, the cube tree, chains.
import random, sys
def par(v): return bin(v).count("1") & 1
def fitch(children, leafof, N, d):
    nn = len(children); f = [None] * nn
    for v in range(nn):
        if v < N:
            lab = par(d & leafof[v]); f[v] = (0, 100) if lab == 0 else (100, 0)
        else:
            a, b = children[v]; f[v] = tuple(min(f[a][g], f[a][1 - g] + 1) + min(f[b][g], f[b][1 - g] + 1) for g in (0, 1))
    return min(f[nn - 1])
def mst(c, N):
    INF = 10 ** 9; d = [INF] * N; inn = [False] * N; inn[0] = True; tot = 0
    for i in range(1, N): d[i] = c[i]
    for _ in range(N - 1):
        b = min((i for i in range(N) if not inn[i]), key=lambda i: d[i]); tot += d[b]; inn[b] = True
        for i in range(N):
            if not inn[i] and c[b ^ i] < d[i]: d[i] = c[b ^ i]
    return tot
def randtree(N, rnd):
    leafof = rnd.sample(range(N), N); cl = list(range(N)); children = [None] * N
    while len(cl) > 1:
        a, b = rnd.sample(range(len(cl)), 2); children.append((cl[a], cl[b])); new = len(children) - 1
        cl = [c for i, c in enumerate(cl) if i not in (a, b)] + [new]
    return children, leafof
def cubetree(N):
    children = [None] * N; cur = list(range(N))
    while len(cur) > 1:
        nxt = []
        for i in range(0, len(cur), 2): children.append((cur[i], cur[i + 1])); nxt.append(len(children) - 1)
        cur = nxt
    return children, list(range(N))
def chain(N, order):
    children = [None] * N; cur = 0
    for i in range(1, N): children.append((cur, i)); cur = len(children) - 1
    return children, order
def balanced_random(N, rnd):   # cube-shaped tree with a random labelling of the leaves
    ch, _ = cubetree(N); return ch, rnd.sample(range(N), N)
for k, nt in ((4, 6000), (5, 2500), (6, 500)):
    N = 1 << k; rnd = random.Random(k); bound = k * N // 2; hist = {}; low = 10 ** 9
    named = [("cube tree", cubetree(N)), ("chain, address order", chain(N, list(range(N)))), ("chain, Gray order", chain(N, [i ^ (i >> 1) for i in range(N)]))]
    for name, (ch, lf) in named:
        c = [0] + [fitch(ch, lf, N, d) for d in range(1, N)]; print(f"N={N} {name}: spanning {mst(c, N)}  [(N/2) log2 N = {bound}]")
    for it in range(nt):
        ch, lf = randtree(N, rnd) if it % 2 else balanced_random(N, rnd)
        c = [0] + [fitch(ch, lf, N, d) for d in range(1, N)]; m = mst(c, N); low = min(low, m)
    print(f"N={N}: {nt} random trees (half random shapes, half cube shapes with random leaves): least spanning count {low}; never below {bound}: {low >= bound}", flush=True)
