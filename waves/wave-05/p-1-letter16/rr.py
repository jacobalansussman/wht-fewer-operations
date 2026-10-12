# p-1-letter16: fewest tree rectangles when the column scaling c is FIXED and the row scalings r(y) are FREE REAL numbers
# (1 <= |r(y)| <= K), numbers on rectangles bounded by Mb.  sum_j v_j rect_j(y,x) = r(y) H(y,x) c(x) is linear in (v, r).
# Float integer programme: candidates only (replay.py replays exactly).   usage: rr.py <design> <centre name> <time limit> <Mb> <K>
import numpy as np, sys, time, json
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy import sparse as sp
from rf import D, par
def bit(x, i): return x >> i & 1
C = {
 'ones':   lambda x: 0,
 'bent':   lambda x: bit(x,0)&bit(x,1) ^ bit(x,2)&bit(x,3),
 'bentx':  lambda x: bit(x,0)&bit(x,3) ^ bit(x,1)&bit(x,2),
 'rank2a': lambda x: bit(x,0)&bit(x,1),
 'rank2b': lambda x: bit(x,0)&bit(x,3),
 'rank2c': lambda x: bit(x,2)&bit(x,3),
 'cubic':  lambda x: bit(x,0)&bit(x,1)&bit(x,2),
 'cubicb': lambda x: bit(x,1)&bit(x,2)&bit(x,3),
 'cubq':   lambda x: bit(x,0)&bit(x,1)&bit(x,2) ^ bit(x,0)&bit(x,3),
 'quart':  lambda x: bit(x,0)&bit(x,1)&bit(x,2)&bit(x,3),
 'c8':     lambda x: [0,0,0,1,0,1,0,0][x],
 'potts':  lambda x: 0,
}
if __name__ == '__main__':
    name, cn, tl, Mb, K = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
    N, rown, coln, inv = D[name]
    c = np.array([(-1.0) ** C[cn](x) for x in range(N)]) if not cn.startswith('v:') else np.array([float(t) for t in cn[2:].split(',')])
    H = np.array([[(-1) ** par(a & x) for x in range(N)] for a in range(N)], dtype=float)
    rects = [(i, j) for i in range(len(rown)) for j in range(len(coln))]; n = len(rects); NN = N * N
    rr_, cc_ = [], []
    for j, (a, b) in enumerate(rects):
        for y in rown[a]:
            for x in coln[b]: rr_.append(y * N + x); cc_.append(j)
    A = sp.csr_matrix((np.ones(len(rr_)), (rr_, cc_)), shape=(NN, n))
    # variables: v (n), z (n), r (N), s (N binary: 1 = positive)
    Rm = sp.csr_matrix(([-(H[y, x] * c[x]) for y in range(N) for x in range(N)], ([y * N + x for y in range(N) for x in range(N)], [y for y in range(N) for x in range(N)])), shape=(NN, N))
    Zs = sp.csr_matrix((NN, N)); I = sp.identity(n); Zr = sp.csr_matrix((n, 2 * N)); IN = sp.identity(N); ZN = sp.csr_matrix((N, 2 * n))
    cons = [LinearConstraint(sp.hstack([A, sp.csr_matrix((NN, n)), Rm, Zs]).tocsr(), 0, 0),
            LinearConstraint(sp.hstack([I, -Mb * I, Zr]).tocsr(), -np.inf, 0), LinearConstraint(sp.hstack([-I, -Mb * I, Zr]).tocsr(), -np.inf, 0),
            LinearConstraint(sp.hstack([ZN, IN, -(K + 1) * IN]).tocsr(), -K, np.inf),      # r >= 1 - (K+1)(1-s)  ->  r - (K+1)s >= -K
            LinearConstraint(sp.hstack([ZN, IN, -(K + 1) * IN]).tocsr(), -np.inf, -1)]     # r <= -1 + (K+1)s     ->  r - (K+1)s <= -1
    lb = np.concatenate([-Mb * np.ones(n), np.zeros(n), -K * np.ones(N), np.zeros(N)]); ub = np.concatenate([Mb * np.ones(n), np.ones(n), K * np.ones(N), np.ones(N)])
    lb[2 * n + N] = 1                                                                     # r(0) > 0: global sign
    integ = np.concatenate([np.zeros(n), np.ones(n), np.zeros(N), np.ones(N)]); cost = np.concatenate([np.zeros(n), np.ones(n), np.zeros(2 * N)])
    t0 = time.time()
    r = milp(cost, constraints=cons, integrality=integ, bounds=Bounds(lb, ub), options={'time_limit': tl, 'disp': False})
    print("design", name, "centre", cn, "Mb", Mb, "K", K, "N", N, "status", r.status, r.message, " best:", None if r.x is None else round(r.fun),
          " lower bound:", getattr(r, 'mip_dual_bound', None), " (%.0f s)" % (time.time() - t0))
    if r.x is not None:
        rs = [round(float(v), 6) for v in r.x[2 * n:2 * n + N]]
        lst = [[list(rown[rects[j][0]]), list(coln[rects[j][1]]), round(float(r.x[j]), 6)] for j in range(n) if abs(r.x[j]) > 1e-6]
        print("  tau", len(lst), " gates N - 2 + tau =", N - 2 + len(lst), " r =", rs)
        print("JSON", json.dumps({'design': name, 'tag': 'centre ' + cn + ' free real rows', 'N': N, 'r': rs, 'c': [float(t) for t in c], 'rects': lst, 'rown': [list(s) for s in rown], 'coln': [list(s) for s in coln]}))
    sys.stdout.flush()
