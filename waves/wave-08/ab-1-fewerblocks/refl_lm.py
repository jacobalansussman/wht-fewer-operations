#!/usr/bin/env python3
"""refl_lm.py [ab-1-fewerblocks]  FLOATS.  The hunt of refl.py with a Levenberg-Marquardt loop written out in numpy.
Same equations: sub-game, single moves z_1..z_B, matrices P_j = u_j v_j^T / (v_j.u_j) on W + S arrays, and for every
character with values +1, -1 (quadratic forms Q):  prod_j (1 - 2 Q(z_j) P_j) maps (x,0) to ((-1)^<Q,I> x, anything).
These are NECESSARY conditions for a unit (the characters with values i, -i are left out), so a failure to solve them is
evidence against a unit and a solution is only a first step.
usage: refl_lm.py m W S seq tries seed [iters]     seq = all | plain | comma list of directions"""
import sys, itertools, numpy as np, time
m, W, S = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); seqs = sys.argv[4]; tries = int(sys.argv[5]); rng = np.random.default_rng(int(sys.argv[6]))
iters = int(sys.argv[7]) if len(sys.argv) > 7 else 80
D = W + S
idx = [(i, j) for i in range(m) for j in range(i, m)]
Qs = list(itertools.product(range(2), repeat=len(idx)))
def table(seq):
    act = np.zeros((len(Qs), len(seq))); tgt = np.zeros(len(Qs))
    for c, q in enumerate(Qs):
        tgt[c] = 1 - 2 * (sum(q[t] for t, (i, j) in enumerate(idx) if i == j) & 1)
        for j, z in enumerate(seq): act[c, j] = sum(q[t] & (z >> i & 1) & (z >> jj & 1) for t, (i, jj) in enumerate(idx)) & 1
    return act, tgt
def resid(par, act, tgt):
    B = act.shape[1]; U = par[:B * D].reshape(B, D); V = par[B * D:].reshape(B, D)
    M = np.broadcast_to(np.eye(D)[:, :W], (act.shape[0], D, W)).copy()
    for j in range(B):
        u = U[j] / (V[j] @ U[j])
        w = np.tensordot(M, V[j], axes=([1], [0]))            # (C, W)
        M -= (2 * act[:, j])[:, None, None] * u[None, :, None] * w[:, None, :]
    return (M[:, :W, :] - tgt[:, None, None] * np.eye(W)[None]).ravel()
def lm(x, act, tgt):
    lam = 1e-2; r = resid(x, act, tgt); c = r @ r
    for it in range(iters):
        J = np.empty((r.size, x.size)); h = 1e-6
        for k in range(x.size):
            xk = x.copy(); xk[k] += h; J[:, k] = (resid(xk, act, tgt) - r) / h
        A = J.T @ J; g = J.T @ r
        for _ in range(8):
            try: dx = np.linalg.solve(A + lam * np.diag(np.diag(A) + 1e-12), -g)
            except np.linalg.LinAlgError: lam *= 10; continue
            r2 = resid(x + dx, act, tgt); c2 = r2 @ r2
            if c2 < c: x, r, c = x + dx, r2, c2; lam = max(lam / 3, 1e-9); break
            lam *= 4
        else: break
        if c / r.size < 1e-24: break
    return x, float(np.sqrt(c / r.size))
t0 = time.time()
print("== m = %d, W = %d live, S = %d scratch, characters with values +-1 (%d), sequence %s" % (m, W, S, len(Qs), seqs), flush=True)
best = 9.0
for t in range(tries):
    if seqs == "plain": sq = [1 << i for i in range(m)] * W
    elif seqs == "all": sq = [int(s) for s in rng.permutation(np.arange(1, 1 << m))]
    else: sq = [int(s) for s in seqs.split(",")]
    act, tgt = table(sq)
    x, e = lm(rng.normal(size=2 * len(sq) * D), act, tgt); best = min(best, e)
    print("   try %d, order %s: root-mean-square error %.3e   [%.0f s]" % (t, ",".join(map(str, sq)), e, time.time() - t0), flush=True)
    if e < 1e-9: np.save("refl_lm_m%d_W%d_S%d_try%d.npy" % (m, W, S, t), np.concatenate([np.array(sq, float), x]))
print("   best root-mean-square error over %d tries: %.3e" % (tries, best))
