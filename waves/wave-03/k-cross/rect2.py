# k-cross: fewest rectangles (float solver, HiGHS; candidates only) for two 16-point designs picked by the L1 sweep.
import numpy as np, sys, time
from scipy.optimize import milp, LinearConstraint, Bounds
N = 16
H = np.array([[(-1)**bin(a & x).count('1') for x in range(N)] for a in range(N)], dtype=float)
def perp(S): return {x for x in range(16) if all(bin(x & s).count('1') % 2 == 0 for s in S)}
def cosets(S):
    seen = set(); out = []
    for x in range(16):
        if x in seen: continue
        cs = tuple(sorted(x ^ s for s in S)); seen |= set(cs); out.append(cs)
    return out
designs = [([1,1,1,-1,1,1,-1,1,1,1,-1,1,-1,-1,-1,1], [[0,5],[0,2,5,7],[0,2,5,7,9,11,12,14]]),
           ([1,-1,1,-1,-1,-1,1,1,1,-1,-1,1,-1,-1,-1,-1], [[0,15],[0,2,13,15],[0,1,2,3,12,13,14,15]])]
for cc, fl in designs:
    cc = np.array(cc, dtype=float); a = H @ cc / 4.0
    V1, V2, V3 = [set(v) for v in fl]
    rown = [tuple(range(16))] + cosets(V3) + cosets(V2) + cosets(V1) + [(i,) for i in range(16)]
    coln = [tuple(range(16))] + cosets(perp(V3)) + cosets(perp(V2)) + cosets(perp(V1)) + [(i,) for i in range(16)]
    cols = []
    for nu in rown:
        for mu in coln:
            M = np.zeros((N, N)); M[np.ix_(list(nu), list(mu))] = 1.0; cols.append(M.ravel())
    A = np.array(cols).T; n = A.shape[1]; b = (H * np.outer(a, cc)).ravel(); Mb = 4.0; I = np.eye(n)
    cons = [LinearConstraint(np.hstack([A, np.zeros_like(A)]), b, b),
            LinearConstraint(np.hstack([I, -Mb*I]), -np.inf, 0), LinearConstraint(np.hstack([-I, -Mb*I]), -np.inf, 0)]
    t0 = time.time()
    r = milp(np.concatenate([np.zeros(n), np.ones(n)]), constraints=cons, integrality=np.concatenate([np.zeros(n), np.ones(n)]),
             bounds=Bounds(np.concatenate([-Mb*np.ones(n), np.zeros(n)]), np.concatenate([Mb*np.ones(n), np.ones(n)])), options={'time_limit': 270})
    print("design centre", cc.astype(int).tolist(), "flag", fl)
    print("  status", r.status, r.message, " best found:", None if r.x is None else round(r.fun), " solver lower bound:", getattr(r, 'mip_dual_bound', None), " (%.0f s)" % (time.time() - t0))
    if r.x is not None:
        pp = r.x[:n]; nz = [(rown[i // 31], coln[i % 31], round(float(pp[i]), 6)) for i in range(n) if abs(pp[i]) > 1e-7]
        print("  gates N - 2 + tau =", 14 + len(nz)); print("  ", nz)
    sys.stdout.flush()
