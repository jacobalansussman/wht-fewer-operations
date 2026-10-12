#!/usr/bin/env python3
"""lemma_check.py: sanity check of the rank inequality behind Lemma A of g-6.md, on random data (not on the transform).

A "tree step" here is the widest class I use: positions 0..N-1, a random binary tree on them, and
    A[i][j] = a_i * F(lowest common node of i and j, which side i is on) * b_j   (i != j),   A[i][i] = d_i,
so that for every node V of the tree the block A[V, not V] has rank <= 1 and so has A[not V, V].
M = A * P * B with P a random relabelling of the middle wires.  Claim: for every node S of A's tree (a set of rows of M)
and every node U of B's tree (a set of columns of M):   rank M[S, U] <= |S' meet U'| + 2,
where S' = S as a set of middle wires on A's side, U' = U carried back through P.
Arithmetic modulo the prime p = 2^31 - 1 with random entries: a rank modulo p is at most the rank of the same construction
over the rationals with those integer entries, so this is a test of the inequality, and "max slack 0" shows it is attained.
"""
import random, sys

P = (1 << 31) - 1

def rank_mod(M):
    M = [row[:] for row in M]
    r = 0
    n = len(M)
    m = len(M[0]) if n else 0
    for c in range(m):
        piv = next((i for i in range(r, n) if M[i][c] % P), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = pow(M[r][c], P - 2, P)
        for i in range(r + 1, n):
            f = M[i][c] * inv % P
            if f:
                M[i] = [(x - f * y) % P for x, y in zip(M[i], M[r])]
        r += 1
        if r == n:
            break
    return r

def random_tree(leaves, rnd):
    """returns list of nodes (frozensets), and a dict lca-key for pairs"""
    nodes = []
    def build(L):
        nodes.append(frozenset(L))
        if len(L) == 1:
            return
        k = rnd.randint(1, len(L) - 1)
        rnd.shuffle(L)
        build(L[:k]); build(L[k:])
    build(list(leaves))
    return nodes

def tree_step(N, nodes, rnd):
    a = [rnd.randrange(1, P) for _ in range(N)]
    b = [rnd.randrange(1, P) for _ in range(N)]
    d = [rnd.randrange(1, P) for _ in range(N)]
    # smallest node containing both i and j; side = whether i is in the first child found
    by_size = sorted(nodes, key=len)
    F = {}
    A = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if i == j:
                A[i][j] = d[i]
                continue
            v = next(nd for nd in by_size if i in nd and j in nd)
            # the child of v containing i: largest proper sub-node of v containing i
            ci = max((nd for nd in nodes if i in nd and nd < v), key=len)
            key = (v, ci)
            if key not in F:
                F[key] = rnd.randrange(1, P)
            A[i][j] = a[i] * F[key] % P * b[j] % P
    return A

def main(N, trials, seed):
    rnd = random.Random(seed)
    worst = None
    tested = 0
    attained = 0
    for t in range(trials):
        n1 = random_tree(range(N), rnd)
        n2 = random_tree(range(N), rnd)
        A = tree_step(N, n1, rnd)
        B = tree_step(N, n2, rnd)
        perm = list(range(N)); rnd.shuffle(perm)            # middle wire z of A is row perm[z] of B
        M = [[sum(A[i][z] * B[perm[z]][j] for z in range(N)) % P for j in range(N)] for i in range(N)]
        # check the tree steps themselves once
        for V in n1:
            if 0 < len(V) < N:
                blk = [[A[i][j] for j in range(N) if j not in V] for i in V]
                assert rank_mod(blk) <= 1
        for S in n1:
            if not (0 < len(S) < N):
                continue
            Sp = {perm[z] for z in S}                        # S' in B's row labels
            for U in n2:
                if not (0 < len(U) < N):
                    continue
                r = rank_mod([[M[i][j] for j in U] for i in S])
                bound = len(Sp & U) + 2
                slack = bound - r
                tested += 1
                if slack == 0:
                    attained += 1
                if worst is None or slack < worst:
                    worst = slack
                if slack < 0:
                    print("VIOLATION", sorted(S), sorted(U), r, bound)
                    return
    print(f"N={N}: {trials} random pairs of tree steps, {tested} pairs of nodes tested, smallest slack {worst}, "
          f"bound attained {attained} times")

if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
