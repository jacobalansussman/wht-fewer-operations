#!/usr/bin/env python3
"""deep.py: follow ONE configuration of grid.py for longer (floats).  usage: deep.py <w> <c> <seed> <config index> <start seeds...>
Prints the squared residual and the largest |unknown| after each leg, to tell "slow convergence to a word" from
"a limit that needs growing coefficients"."""
import sys, random
import numpy as np
from scipy.optimize import least_squares
import grid

w, c, seed, idx = (int(v) for v in sys.argv[1:5])
rnd = random.Random(seed)
for _ in range(idx + 1):
    H, A, row1, B, row2, col2, desc = grid.config(w, c, rnd, False)
n = A.n + B.n
def res(p):
    r = (A.mat(p[:A.n])[row1, :] @ B.mat(p[A.n:])[np.ix_(row2, col2)] - H).ravel()
    return r if n <= r.size else np.concatenate([r, np.zeros(n - r.size)])
print("configuration:", desc, flush=True)
for s in sys.argv[5:]:
    p = np.random.default_rng(int(s)).normal(size=n)
    for leg in range(6):
        sol = least_squares(res, p, method="lm", xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=400)
        p = sol.x
        v = float(sol.fun @ sol.fun)
        MA = A.mat(p[:A.n])[row1, :]
        MB = B.mat(p[A.n:])[np.ix_(row2, col2)]
        # size of the largest rank-one term A[:,z] B[z,:]: unchanged by rescaling the middle wires, so growth here is real
        term = float(np.max(np.linalg.norm(MA, axis=0) * np.linalg.norm(MB, axis=1)))
        print(f"start {s} leg {leg}: squared residual {v:.3e}  largest middle term {term:.3e}  largest |unknown| {np.max(np.abs(p)):.3e}", flush=True)
        if v < 1e-22:
            M = A.mat(p[:A.n])[row1, :] @ B.mat(p[A.n:])[np.ix_(row2, col2)]
            print("   max |A.B - H| =", float(np.max(np.abs(M - H))), flush=True)
            break
