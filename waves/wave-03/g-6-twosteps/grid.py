#!/usr/bin/env python3
"""grid.py: floating-point hunt for a product of TWO tree steps equal to the transform, in the "grid shape" of g-6.md.

A DISCOVERY INSTRUMENT (floats, real numbers, Levenberg-Marquardt from random starts).  "hit" = residual below 1e-16;
"no hit" is evidence, not a proof.  Nothing here is exact.

Shape (w, c), N = w*c:  outputs x = (xi, omega), inputs y = (eta, gamma), middle wires z = (xi, eta),
xi, gamma in c values, omega, eta in w values, H[x][y] = (-1)^(xi.gamma + omega.eta).
First step A (outputs x middle): tree whose blocks are the c sets {xi fixed} of w points, a tree inside each block,
a tree over the blocks; the rows of a block are matched to its columns by a relabelling (random or given).
Second step B (middle x inputs): tree whose blocks are the w sets {eta fixed} of c points, same freedom.
A step is the widest class: entry (i,j) = a_i * F(lowest common node, side) * b_j off the diagonal, d_i on it.

usage: grid.py <w> <c> <configs> <starts> <seed> [cat]      (cat: the tree inside each w-block is a caterpillar)
"""
import sys, random
import numpy as np
from scipy.optimize import least_squares

def popc(v):
    return bin(v).count("1")

def rand_tree(items, rnd, cat=False):
    items = list(items)
    if len(items) == 1:
        return items[0]
    if cat:
        return (items[0], rand_tree(items[1:], rnd, True))
    rnd.shuffle(items)
    k = rnd.randint(1, len(items) - 1)
    return (rand_tree(items[:k], rnd), rand_tree(items[k:], rnd))

def leaves(t):
    return [t] if not isinstance(t, tuple) else leaves(t[0]) + leaves(t[1])

def graft(top, sub):
    """replace leaf b of the tree top by the tree sub[b]"""
    return sub[top] if not isinstance(top, tuple) else (graft(top[0], sub), graft(top[1], sub))

def keys(tree, N):
    K = -np.ones((N, N), dtype=np.int64)
    cnt = [0]
    def rec(t):
        if not isinstance(t, tuple):
            return [t]
        L, R = rec(t[0]), rec(t[1])
        for i in L:
            for j in R:
                K[i, j] = cnt[0]
                K[j, i] = cnt[0] + 1
        cnt[0] += 2
        return L + R
    rec(tree)
    np.fill_diagonal(K, 0)
    return K, cnt[0]

class Step:
    def __init__(self, tree, N):
        self.N = N
        self.K, self.nF = keys(tree, N)
        self.n = 3 * N + self.nF
    def mat(self, p):
        N = self.N
        a, b, d, F = p[:N], p[N:2 * N], p[2 * N:3 * N], p[3 * N:]
        M = a[:, None] * F[self.K] * b[None, :]
        M[np.arange(N), np.arange(N)] = d
        return M

def config(w, c, rnd, cat):
    N = w * c
    H = np.array([[(-1) ** (popc((x // w) & (y % c)) + popc((x % w) & (y // c))) for y in range(N)] for x in range(N)], float)
    # step A: positions xi*w + i
    sub = {xi: rand_tree([xi * w + i for i in range(w)], rnd, cat) for xi in range(c)}
    t1 = graft(rand_tree(range(c), rnd), sub)
    perm = {xi: rnd.sample(range(w), w) for xi in range(c)}
    row1 = np.array([(x // w) * w + perm[x // w][x % w] for x in range(N)])          # x = xi*w + omega
    # middle wire z = xi*w + eta sits at position xi*w + eta of A's tree and eta*c + xi of B's tree
    row2 = np.array([(z % w) * c + (z // w) for z in range(N)])
    sub2 = {eta: rand_tree([eta * c + j for j in range(c)], rnd) for eta in range(w)}
    t2 = graft(rand_tree(range(w), rnd), sub2)
    perm2 = {eta: rnd.sample(range(c), c) for eta in range(w)}
    col2 = np.array([(y // c) * c + perm2[y // c][y % c] for y in range(N)])          # y = eta*c + gamma
    return H, Step(t1, N), row1, Step(t2, N), row2, col2, (t1, perm, t2, perm2)

def hunt(w, c, nconf, starts, seed, cat):
    rnd = random.Random(seed)
    rng = np.random.default_rng(seed)
    N = w * c
    best_all = []
    hits = 0
    for ci in range(nconf):
        H, A, row1, B, row2, col2, desc = config(w, c, rnd, cat)
        n_unk = A.n + B.n
        state = {"count": 0, "best": None}
        budget = 220 * (n_unk + 1)            # about 220 Levenberg-Marquardt iterations with a finite-difference Jacobian
        class Budget(Exception):
            pass
        def res(p):
            MA = A.mat(p[:A.n])[row1, :]
            MB = B.mat(p[A.n:])[np.ix_(row2, col2)]
            r = (MA @ MB - H).ravel()
            v = float(r @ r)
            if state["best"] is None or v < state["best"]:
                state["best"] = v
            state["count"] += 1
            if state["count"] > budget:
                raise Budget()
            pad = n_unk - r.size              # method lm needs at least as many residuals as unknowns
            return r if pad <= 0 else np.concatenate([r, np.zeros(pad)])
        best = None
        for s in range(starts):
            p0 = rng.normal(size=n_unk)
            state["count"] = 0
            state["best"] = None
            try:
                least_squares(res, p0, method="lm", xtol=1e-14, ftol=1e-14, gtol=1e-14, max_nfev=budget)
            except Budget:
                pass
            except Exception as e:
                print("solver error:", e, flush=True)
            r = state["best"]
            if r is not None and (best is None or r < best):
                best = r
            if best is not None and best < 1e-16:
                break
        best_all.append(best)
        if best is not None and best < 1e-16:
            hits += 1
            print(f"HIT config {ci}: squared residual {best:.2e}  trees/relabellings: {desc}", flush=True)
        else:
            print(f"config {ci}: best squared residual {best}", flush=True)
    vals = sorted(v for v in best_all if v is not None)
    print(f"shape ({w},{c}) N={N} caterpillar={cat}: {nconf} configurations x {starts} starts: {hits} hits; "
          f"smallest residuals {[round(v, 4) for v in vals[:8]]}")

if __name__ == "__main__":
    w, c, nconf, starts, seed = (int(v) for v in sys.argv[1:6])
    hunt(w, c, nconf, starts, seed, len(sys.argv) > 6 and sys.argv[6] == "cat")
