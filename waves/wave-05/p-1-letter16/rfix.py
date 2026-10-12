# p-1-letter16: fewest tree rectangles for FIXED sign scalings r, c (float integer programme; candidates, replayed by replay.py).
# usage: rfix.py <design> <mode tile|gen> <time limit> <Mb> <tag> <r as comma list> <c as comma list>
import numpy as np, sys, time, json
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy import sparse as sp
from rf import D, par
def solve(name, mode, tl, Mb, tag, r_, c_, quiet=False):
    N, rown, coln, inv = D[name]
    H = np.array([[(-1) ** par(a & x) for x in range(N)] for a in range(N)], dtype=float)
    M = H * np.outer(r_, c_)
    rects = [(i, j) for i in range(len(rown)) for j in range(len(coln))]
    if mode == 'tile':   # only rectangles lying inside E = {M = -1}
        rects = [(i, j) for (i, j) in rects if all(M[y, x] < 0 for y in rown[i] for x in coln[j])]
    n = len(rects); NN = N * N; rr, cc = [], []
    for j, (a, b) in enumerate(rects):
        for y in rown[a]:
            for x in coln[b]: rr.append(y * N + x); cc.append(j)
    A = sp.csr_matrix((np.ones(len(rr)), (rr, cc)), shape=(NN, n)); t0 = time.time()
    if mode == 'tile':
        rhs = ((1 - M) / 2).ravel()
        res = milp(np.ones(n), constraints=[LinearConstraint(A, rhs, rhs)], integrality=np.ones(n), bounds=Bounds(np.zeros(n), np.ones(n)), options={'time_limit': tl})
        best = None if res.x is None else round(res.fun) + 1
        lst = None if res.x is None else [[list(range(N)), list(range(N)), 1.0]] + [[list(rown[rects[j][0]]), list(coln[rects[j][1]]), -2.0] for j in range(n) if res.x[j] > 0.5]
    else:
        I = sp.identity(n)
        cons = [LinearConstraint(sp.hstack([A, sp.csr_matrix((NN, n))]).tocsr(), M.ravel(), M.ravel()),
                LinearConstraint(sp.hstack([I, -Mb * I]).tocsr(), -np.inf, 0), LinearConstraint(sp.hstack([-I, -Mb * I]).tocsr(), -np.inf, 0)]
        res = milp(np.concatenate([np.zeros(n), np.ones(n)]), constraints=cons, integrality=np.concatenate([np.zeros(n), np.ones(n)]),
                   bounds=Bounds(np.concatenate([-Mb * np.ones(n), np.zeros(n)]), np.concatenate([Mb * np.ones(n), np.ones(n)])), options={'time_limit': tl})
        best = None if res.x is None else round(res.fun)
        lst = None if res.x is None else [[list(rown[rects[j][0]]), list(coln[rects[j][1]]), round(float(res.x[j]), 6)] for j in range(n) if abs(res.x[j]) > 1e-6]
    lbd = getattr(res, 'mip_dual_bound', None)
    if not quiet:
        print("design", name, tag, "mode", mode, "Mb", Mb, "status", res.status, " best tau:", best, " lower bound:", None if lbd is None else lbd + (1 if mode == 'tile' else 0), " (%.0f s)" % (time.time() - t0))
        if lst is not None:
            print("JSON", json.dumps({'design': name, 'tag': tag + ' ' + mode, 'N': N, 'r': [int(v) for v in r_], 'c': [int(v) for v in c_], 'rects': lst, 'rown': [list(s) for s in rown], 'coln': [list(s) for s in coln]}))
        sys.stdout.flush()
    return best, res.status, lst
if __name__ == '__main__':
    name, mode, tl, Mb, tag = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
    solve(name, mode, tl, Mb, tag, [int(t) for t in sys.argv[6].split(',')], [int(t) for t in sys.argv[7].split(',')])
