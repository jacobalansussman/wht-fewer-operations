#!/usr/bin/env python3
"""refl.py m W seconds seed counts...  -- a first numerical probe: can reflections realise an allowed count vector?  [e2-2-ladder]
Old letters, the hidden-form picture of e2-2.md section 2, NO scratch arrays.
Unknowns: an order of the moves and one reflection R_i = 1 - 2 v_i w_i^T / (w_i.v_i) of R^W per move (move i has direction z_i).
Wanted: for every quadratic form q, the ordered product of the R_i with q(z_i) = 1 equals (-1)^q(I) times the identity.
Method: least squares (floating point) on a sample of forms (all products of two linear forms, all linear forms, random forms),
random orders, random starts.  A residual near 0 would be a CANDIDATE to be made exact and checked on all forms; a residual
that stays large in a few starts proves nothing.
counts: 'z:n' pairs as printed by milp.py (z in binary).
"""
import sys, time, itertools
import numpy as np
from scipy.optimize import least_squares
m = int(sys.argv[1]); W = int(sys.argv[2]); T = float(sys.argv[3]); seed = int(sys.argv[4])
moves = []
for tok in sys.argv[5:]:
    z, n = tok.strip(",").split(":")
    moves += [int(z, 2)] * int(n)
k = len(moves)
rng = np.random.default_rng(seed)
def dot(a, b): return bin(a & b).count("1") & 1
V = range(1, 1 << m)
forms = []          # each: (function z -> bit, q(I))
for a, b in itertools.combinations(V, 2):
    forms.append(([dot(a, z) & dot(b, z) for z in moves], dot(a, b)))
for a in V:
    forms.append(([dot(a, z) for z in moves], bin(a).count("1") & 1))
pairs = [(i, j) for i in range(m) for j in range(i, m)]
for _ in range(600):
    Q = rng.integers(0, 2, len(pairs))
    def q(z):
        s = 0
        for c, (i, j) in zip(Q, pairs):
            if c and z >> i & 1 and z >> j & 1: s ^= 1
        return s
    forms.append(([q(z) for z in moves], int(sum(Q[t] for t, (i, j) in enumerate(pairs) if i == j) & 1)))
SEL0 = np.array([f[0] for f in forms], dtype=float)          # forms x moves (in the listed order)
SGN = np.array([(-1.0) ** f[1] for f in forms])
nq = len(forms)
print("m = %d, W = %d, %d moves, %d forms in the sample (%d with q(I) = 1); fewest selected by a form with q(I)=1: %d"
      % (m, W, k, nq, int((SGN < 0).sum()), int(SEL0[SGN < 0].sum(axis=1).min())), flush=True)
I = np.eye(W)
def resid(x, SEL):
    v = x[:k * W].reshape(k, W); w = x[k * W:].reshape(k, W)
    P = np.broadcast_to(I, (nq, W, W)).copy()
    for i in range(k):
        d = v[i] @ w[i]
        Pv = P @ v[i]                                   # nq x W
        P = P - (2.0 / d) * SEL[:, i, None, None] * Pv[:, :, None] * w[i][None, None, :]
    return (P - SGN[:, None, None] * I).ravel()
t0 = time.time(); best = None; tries = 0
while time.time() - t0 < T:
    perm = rng.permutation(k)
    SEL = SEL0[:, perm]
    x0 = rng.normal(size=2 * k * W)
    # start near a frame-like configuration half of the time
    if tries % 2 == 0:
        v = np.zeros((k, W)); w = np.zeros((k, W))
        for i in range(k):
            j = i % W; v[i, j] = 1; w[i, j] = 1
        x0 = np.concatenate([v.ravel(), w.ravel()]) + 0.3 * rng.normal(size=2 * k * W)
    try:
        res = least_squares(resid, x0, args=(SEL,), method="trf", max_nfev=60, x_scale="jac")
    except Exception as e:
        print("  failed:", e, flush=True); tries += 1; continue
    r = float(np.sqrt(np.mean(res.fun ** 2)))
    tries += 1
    print("  try %d: order %s  rms residual %.4e  (start %.3e)" % (tries, [format(moves[p], "0%db" % m) for p in perm][:6], r, float(np.sqrt(np.mean(resid(x0, SEL) ** 2)))), flush=True)
    if best is None or r < best[0]:
        best = (r, perm.copy(), res.x.copy())
print("best rms residual over %d tries: %.4e" % (tries, best[0]))
print("for scale: the all-identity 'do nothing' has rms residual %.4e" % float(np.sqrt(np.mean((np.broadcast_to(I, (nq, W, W)) - SGN[:, None, None] * I) ** 2))))
if best[0] < 1e-6:
    np.save("refl_candidate_m%d_W%d_seed%d.npy" % (m, W, seed), np.concatenate([best[1].astype(float), best[2]]))
    print("CANDIDATE saved (floating point; not exact, not checked on all forms)")
