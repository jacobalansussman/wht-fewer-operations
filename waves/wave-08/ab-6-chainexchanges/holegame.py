#!/usr/bin/env python3
"""holegame.py n S H mode targets nstarts seed   [ab-6-chainexchanges]  FLOATS (Levenberg-Marquardt); a hit is a candidate.
The "hole game" [derived in ab-6.md section 2]: n arrays, S stages.  In every stage each array climbs once and leaves one
port direction unmoved (a hole); shears go from arrays that have climbed to arrays that have not, each shear carrying ONE
hole move D_a (a = 1..H), D_a D_a = a free relabelling.  Free rational mixing between stages.  Over the characters
D_a -> eps_a = +-1 a word is right exactly when, for all 2^H sign patterns,
      C_S U_S(eps) C_(S-1) ... U_1(eps) C_0  =  diag_i( prod_{a in A_i} eps_a ),
U_k(eps) = unit lower triangular built from T_k(eps) = sum_a eps_a T_(k,a) (strictly lower triangular, rational):
  mode seq : sources in climbing order, each reads the values already written (the legal order inside a stage)
  mode sim : I + T_k (all shears read old values)
targets: the sets A_i, e.g. "12,12,12" (content i gets holes 1 and 2); "0" = the empty set."""
import sys, itertools, numpy as np
from scipy.optimize import least_squares
n, S, H = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); mode = sys.argv[4]
A = [set(int(c) for c in t if c != "0") for t in sys.argv[5].split(",")]; nst = int(sys.argv[6]); seed = int(sys.argv[7])
assert len(A) == n
eps_all = list(itertools.product((1, -1), repeat=H))
tgt = [np.diag([float(np.prod([e[a-1] for a in Ai])) if Ai else 1.0 for Ai in A]) for e in eps_all]
tril = np.tril_indices(n, -1); nt = len(tril[0])
nT = S*H*nt; nC = (S+1)*n*n
def build(v):
    T = np.zeros((S, H, n, n))
    T[:, :, tril[0], tril[1]] = v[:nT].reshape(S, H, nt)
    C = v[nT:].reshape(S+1, n, n); return T, C
def stage(Tk):
    if mode == "sim": return np.eye(n) + Tk
    M = np.eye(n)
    for i in range(n-1):
        E = np.eye(n); E[:, i] += Tk[:, i]; M = E @ M
    return M
def resid(v):
    T, C = build(v); out = []
    for e, D in zip(eps_all, tgt):
        P = C[0]
        for k in range(S):
            P = C[k+1] @ stage(sum(e[a]*T[k, a] for a in range(H))) @ P
        out.append((P - D).ravel())
    return np.concatenate(out)
npad = max(0, nT + nC - len(eps_all)*n*n)
def residp(v): return np.concatenate([resid(v), np.zeros(npad)])     # zero padding so that Levenberg-Marquardt accepts more unknowns than equations
rng = np.random.default_rng(seed); hits = 0; best = 9e9
for st in range(nst):
    v0 = rng.normal(size=nT+nC) * rng.choice([0.5, 1.0])
    sol = least_squares(residp, v0, method="lm", xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=4000)
    r = float(np.sqrt(2*sol.cost)); best = min(best, r)
    if r < 1e-9:
        hits += 1
        if hits == 1: np.save("hole_n%d_S%d_H%d_%s_%s.npy" % (n, S, H, mode, sys.argv[5].replace(",", "-")), sol.x)
print("n=%d S=%d H=%d mode=%s targets=%-22s starts %3d hits %3d best residual %.2e" % (n, S, H, mode, sys.argv[5], nst, hits, best), flush=True)
