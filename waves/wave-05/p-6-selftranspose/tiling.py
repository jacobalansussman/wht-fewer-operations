#!/usr/bin/env python3
"""p-6-selftranspose / tiling.py   (count (G))

Model T ("one centre, one tree, a matching"):  G = J - 2E,  G a symmetric +-1 matrix with orthogonal rows (a Hadamard
matrix, so a signed relabelling of the transform at 4 and 8 points), E the 0/1 indicator of a union of pairwise DISJOINT
rectangles  A x B + B x A  (A, B two disjoint nodes of ONE merge tree, paired) or  A x A  (a node squared);
every node is used at most once; the root is used once as the square J.
Then x^T G x = (sum of all)^2 - 2 * sum of squares - 4 * sum of products of disjoint pairs of tree forms:
G = F^T M F with F the tree (N - 1 gates), N' = number of nodes used, cost N - 2 + N' gates.
Exhaustive over every tree shape with N leaves (leaves labelled 0..N-1 in tree order: G is then every symmetric
Hadamard matrix that fits, so no separate loop over relabellings is needed).
usage: tiling.py N [maxshapes] [maxNprime]
"""
import sys, itertools, time
N = int(sys.argv[1])
_main = __name__ == "__main__"
MAXSH = int(sys.argv[2]) if _main and len(sys.argv) > 2 else 10**9
MAXNP = int(sys.argv[3]) if _main and len(sys.argv) > 3 else 2 * N - 1
FULL = (1 << N) - 1

def shapes(n):
    """all rooted binary tree shapes with n leaves, as nested tuples; smaller-or-equal child first"""
    if n == 1:
        return [()]
    out = []
    for a in range(1, n // 2 + 1):
        b = n - a
        A = shapes_c(a); B = shapes_c(b)
        if a < b:
            for s in A:
                for t in B:
                    out.append((s, t))
        else:
            for i, s in enumerate(A):
                for t in A[i:]:
                    out.append((s, t))
    return out
_c = {}
def shapes_c(n):
    if n not in _c:
        _c[n] = shapes(n)
    return _c[n]

def nodes_of(shape):
    """returns list of leaf-set bitmasks of all nodes; leaves numbered in order"""
    out = []
    def rec(s, start):
        if s == ():
            out.append(1 << start)
            return 1 << start, start + 1
        m1, nxt = rec(s[0], start)
        m2, nxt = rec(s[1], nxt)
        out.append(m1 | m2)
        return m1 | m2, nxt
    rec(shape, 0)
    return out

def rect(a, b):
    """bitmask over N*N cells of rows a x columns b"""
    r = 0
    for x in range(N):
        if a >> x & 1:
            r |= b << (N * x)
    return r

def describe(shape):
    if shape == ():
        return "."
    return "(" + describe(shape[0]) + describe(shape[1]) + ")"

def search(shape, want_all=False):
    nodes = nodes_of(shape)
    nodes = [m for m in nodes if m != FULL]           # the root is the square J
    K = len(nodes)
    anc = [[i for i in range(K) if nodes[i] >> x & 1] for x in range(N)]   # non-root ancestors of leaf x (itself included)
    sol = []
    best = [MAXNP + 1]
    state = [None] * K                               # None unassigned, -1 unused, i itself (square), j partner
    rows = [None] * N
    cnt = [0]

    def rowmask(used, x):
        return (used >> (N * x)) & FULL

    def leaf(x, used, nused):
        if nused + 1 > best[0] and not want_all:
            return
        if x == N:
            cnt[0] += 1
            np_ = nused + 1
            if np_ < best[0]:
                best[0] = np_
                sol.clear()
            if np_ == best[0] or want_all:
                sol.append((np_, list(state)))
            return
        todo = [i for i in anc[x] if state[i] is None]
        assign(x, todo, 0, used, nused)

    def assign(x, todo, t, used, nused):
        if t == len(todo):
            r = rowmask(used, x)
            for y in range(x):
                if bin(r ^ rows[y]).count("1") != N // 2:
                    return
            rows[x] = r
            leaf(x + 1, used, nused)
            return
        i = todo[t]
        if state[i] is not None:
            assign(x, todo, t + 1, used, nused)
            return
        a = nodes[i]
        state[i] = -1
        assign(x, todo, t + 1, used, nused)
        sq = rect(a, a)
        if not (sq & used):
            state[i] = i
            assign(x, todo, t + 1, used | sq, nused + 1)
        for j in range(K):
            if state[j] is None and j != i and not (nodes[j] & a):
                b = nodes[j]
                # rows of leaves already finished must not change
                rr = rect(a, b) | rect(b, a)
                if rr & used:
                    continue
                # b x a adds cells in rows of b: forbidden if a leaf of b is already finished
                lowb = (b & -b).bit_length() - 1
                if lowb < x:
                    continue
                state[i] = j; state[j] = i
                assign(x, todo, t + 1, used | rr, nused + 2)
                state[j] = None
        state[i] = None

    leaf(0, 0, 0)
    return nodes, sol, cnt[0]

def show(nodes, st):
    def nm(m):
        return "{" + ",".join(str(x) for x in range(N) if m >> x & 1) + "}"
    parts = ["root^2"]
    for i, s in enumerate(st):
        if s == i:
            parts.append(nm(nodes[i]) + "^2")
        elif s is not None and s > i:
            parts.append(nm(nodes[i]) + "*" + nm(nodes[s]))
    return "  ".join(parts)

def matrix(nodes, st):
    used = 0
    for i, s in enumerate(st):
        if s == i:
            used |= rect(nodes[i], nodes[i])
        elif s is not None and s >= 0:
            used |= rect(nodes[i], nodes[s])
    return [[-1 if used >> (N * x + y) & 1 else 1 for y in range(N)] for x in range(N)]

if __name__ == "__main__":
    t0 = time.time()
    S = shapes_c(N)
    print("N =", N, " tree shapes:", len(S), " model T (root square, disjoint matched rectangles, coefficient -2)")
    tot = 0
    for k, sh in enumerate(S[:MAXSH]):
        nodes, sol, cnt = search(sh)
        tot += cnt
        if sol:
            np_ = sol[0][0]
            print("shape %3d %s : least N' = %d  (gates N-2+N' = %d), %d matchings at the least, %d visited"
                  % (k, describe(sh), np_, N - 2 + np_, len(sol), cnt))
            print("     e.g.", show(nodes, sol[0][1]))
            G = matrix(nodes, sol[0][1])
            ok = all(sum(G[x][z] * G[y][z] for z in range(N)) == (N if x == y else 0) for x in range(N) for y in range(N))
            sym = all(G[x][y] == G[y][x] for x in range(N) for y in range(N))
            print("     replay: rows orthogonal", ok, " symmetric", sym, " diagonal", [G[x][x] for x in range(N)])
        else:
            print("shape %3d %s : NONE with N' <= %d" % (k, describe(sh), MAXNP))
        sys.stdout.flush()
    print("seconds", round(time.time() - t0, 1))
