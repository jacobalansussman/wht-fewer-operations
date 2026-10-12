#!/usr/bin/env python3
"""sixcall.py r nstarts seed [maxsec]   [ab-6-chainexchanges]   FLOATS: a hit is a candidate, "none" is not a proof.
x-3's family at K = 4: the box is the permutation matrix P_g of an address map g (the six permutations of the addresses
1, 2, 3; address 0 fixed).  Target: P_g X P_g^T for the 4 x 4 table X.  Textbook 8 calls, x-3's exact program 7, bound 6.
Reduction [derived, ab-6]: under the six maps a 4-vector is 2 fixed numbers + one 2-dimensional piece W (the plane sum = 0);
a call moves only the W-part of its input, by the 2 x 2 matrix rho(g).  The table is 5 fixed numbers + 5 copies of W + one
number t that is multiplied by sign(g).  Fixed numbers pass through a call unchanged, so a call program is, without loss,
    c_j = rho(g) (A_j z + sum_{i<j} m_ji c_i),   out = Q z + sum_j P_j c_j,      z = (s_1..s_5 in W^5, t) in R^11
and it must give out = (rho(g) s_1, ..., rho(g) s_5, sign(g) t) for all six g.  P and Q are found by exact linear least
squares for given A, m (variable projection); A, m by Levenberg-Marquardt from random starts."""
import sys, time, numpy as np
from scipy.optimize import least_squares
r = int(sys.argv[1]); nst = int(sys.argv[2]); seed = int(sys.argv[3]); maxsec = float(sys.argv[4]) if len(sys.argv) > 4 else 1e9
c, s = np.cos(2*np.pi/3), np.sin(2*np.pi/3)
R = np.array([[c, -s], [s, c]]); Fm = np.array([[1., 0.], [0., -1.]])
G = [(np.eye(2), 1), (R, 1), (R@R, 1), (Fm, -1), (Fm@R, -1), (Fm@R@R, -1)]
def target(rho, sg):
    T = np.zeros((11, 11))
    for a in range(5): T[2*a:2*a+2, 2*a:2*a+2] = rho
    T[10, 10] = sg; return T
TT = np.vstack([target(rho, sg).T for rho, sg in G])        # 66 x 11
nA = r*22; pairs = [(j, i) for j in range(r) for i in range(j)]
def unpack(v):
    A = v[:nA].reshape(r, 2, 11); m = {}
    for k, (j, i) in enumerate(pairs): m[(j, i)] = v[nA+4*k:nA+4*k+4].reshape(2, 2)
    return A, m
def Bmat(v):
    A, m = unpack(v); rows = []
    for rho, sg in G:
        C = []
        for j in range(r):
            w = A[j].copy()
            for i in range(j): w = w + m[(j, i)] @ C[i]
            C.append(rho @ w)
        rows.append(np.hstack([np.vstack(C).T, np.eye(11)]))   # 11 x (2r+11)
    return np.vstack(rows)                                     # 66 x (2r+11)
def resid(v):
    B = Bmat(v); X, *_ = np.linalg.lstsq(B, TT, rcond=None)
    return (B @ X - TT).ravel()
rng = np.random.default_rng(seed); t0 = time.time(); best = 9e9; hits = 0
for st in range(nst):
    if time.time() - t0 > maxsec: print("time up after %d starts" % st); break
    v0 = rng.normal(size=nA + 4*len(pairs)) * rng.choice([0.3, 1.0])
    sol = least_squares(resid, v0, method="lm", xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=4000)
    res = float(np.sqrt(2*sol.cost)); best = min(best, res)
    hit = res < 1e-9
    hits += hit
    print("r=%d start %3d residual %.3e %s  [%.0fs]" % (r, st, res, "HIT" if hit else "", time.time()-t0), flush=True)
    if hit: np.save("hit_r%d_s%d_%d.npy" % (r, seed, st), sol.x)
print("SUMMARY r=%d starts %d hits %d best residual %.3e" % (r, st+1, hits, best))
