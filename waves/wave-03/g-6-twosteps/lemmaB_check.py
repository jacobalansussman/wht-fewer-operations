#!/usr/bin/env python3
"""lemmaB_check.py: sanity check of the block law's algebra (g-6.md section 4, first display), on random data, modulo a prime.

Claim: M = A * P * B, two random tree steps (as in lemma_check.py).  For a node S of A's tree and a node U of B's tree let
u = the column direction of A[S, outside S'] and q = the row direction of B[outside U', U].  Then
    M[S, U] = (a matrix of rank <= |S' meet U'|) + (anything) x q + u x (anything),
i.e. after removing u on the left and q on the right the rank is at most |S' meet U'|.
Test: L = a basis of the row vectors killing u, Kq = a basis of the column vectors killed by q; rank(L M[S,U] Kq) <= |S' meet U'|.
"""
import random, sys
from lemma_check import P, rank_mod, random_tree, tree_step

def null_basis(v):
    """basis of {w : w . v = 0} modulo P, v not zero"""
    n = len(v)
    k = next(i for i in range(n) if v[i] % P)
    inv = pow(v[k], P - 2, P)
    out = []
    for i in range(n):
        if i == k:
            continue
        w = [0] * n
        w[i] = 1
        w[k] = (-v[i] * inv) % P
        out.append(w)
    return out

def main(N, trials, seed):
    rnd = random.Random(seed)
    tested = 0
    attained = 0
    for t in range(trials):
        n1 = random_tree(range(N), rnd)
        n2 = random_tree(range(N), rnd)
        A = tree_step(N, n1, rnd)
        B = tree_step(N, n2, rnd)
        perm = list(range(N)); rnd.shuffle(perm)
        inv = [0] * N
        for z in range(N):
            inv[perm[z]] = z
        M = [[sum(A[i][z] * B[perm[z]][j] for z in range(N)) % P for j in range(N)] for i in range(N)]
        for S in n1:
            if not (1 < len(S) < N):
                continue
            Sl = sorted(S)
            zout = next(z for z in range(N) if z not in S)
            u = [A[i][zout] for i in Sl]                      # column direction of A[S, outside S']
            Sp = {perm[z] for z in S}
            for U in n2:
                if not (1 < len(U) < N):
                    continue
                Ul = sorted(U)
                rout = next(r for r in range(N) if r not in U)
                q = [B[rout][j] for j in Ul]                  # row direction of B[outside U', U]
                L = null_basis(u)
                Kq = null_basis(q)
                blk = [[M[i][j] for j in Ul] for i in Sl]
                LM = [[sum(l[a] * blk[a][b] for a in range(len(Sl))) % P for b in range(len(Ul))] for l in L]
                LMK = [[sum(row[b] * kq[b] for b in range(len(Ul))) % P for kq in Kq] for row in LM]
                r = rank_mod(LMK) if LMK and LMK[0] else 0
                bound = len(Sp & U)
                tested += 1
                if r == bound:
                    attained += 1
                if r > bound:
                    print("VIOLATION", Sl, Ul, r, bound)
                    return
    print(f"N={N}: {trials} random pairs of tree steps, {tested} pairs of nodes: rank after removing u and q never above "
          f"|S' meet U'|; equal to it {attained} times")

if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
