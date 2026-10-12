# p-4-formula (c): fewest tree rectangles (overlaps allowed, any numbers up to a bound) for the RULE's design at 16 points,
# once for the transform (rho = -1) and once for generic members of the class (rho = 2, 3). FLOAT SOLVER (HiGHS): candidates only.
# Design: both trees split on bits 1,2,3,4 in order; centre exponents q = (1-X1)X4 + X2X3, q' = Y1Y4 + Y2Y3;
# F = X1Y4 + X2Y3 + X3Y2 + X4Y1. Target: rho^(F - q - q') = sum of numbers on rectangles (the root included). Count (G): gates = 14 + tau.
import numpy as np, sys, time
from itertools import product
from scipy.optimize import milp, LinearConstraint, Bounds
k = 4; P = list(product((0,1), repeat=k)); N = len(P); idx = {p: i for i, p in enumerate(P)}
def nodes(order):
    out = []
    for d in range(k+1):
        for vals in product((0,1), repeat=d):
            out.append(tuple(idx[p] for p in P if all(p[order[i]] == vals[i] for i in range(d))))
    return out
which = sys.argv[1]; tl = float(sys.argv[2])
inner = {'cells': (lambda X: X[1]*X[2], lambda Y: Y[1]*Y[2]), 'cyc': (lambda X: (1-X[1])*X[2], lambda Y: Y[1]*Y[2])}[sys.argv[3]]
q  = lambda X: (1-X[0])*X[3] + inner[0](X)
qp = lambda Y: Y[0]*Y[3] + inner[1](Y)
m = np.array([[sum(X[i]*Y[k-1-i] for i in range(k)) - q(X) - qp(Y) for X in P] for Y in P], dtype=float)
rown = nodes((0,1,2,3)); coln = nodes((0,1,2,3))
cols = []
for nu in rown:
    for mu in coln:
        M = np.zeros((N, N)); M[np.ix_(list(nu), list(mu))] = 1.0; cols.append(M.ravel())
A = np.array(cols).T; n = A.shape[1]; I = np.eye(n)
for rho in [float(eval(s)) for s in which.split(',')]:
    b = (rho ** m).ravel(); Mb = 64.0
    cons = [LinearConstraint(np.hstack([A, np.zeros_like(A)]), b, b),
            LinearConstraint(np.hstack([I, -Mb*I]), -np.inf, 0), LinearConstraint(np.hstack([-I, -Mb*I]), -np.inf, 0)]
    t0 = time.time()
    r = milp(np.concatenate([np.zeros(n), np.ones(n)]), constraints=cons, integrality=np.concatenate([np.zeros(n), np.ones(n)]),
             bounds=Bounds(np.concatenate([-Mb*np.ones(n), np.zeros(n)]), np.concatenate([Mb*np.ones(n), np.ones(n)])), options={'time_limit': tl})
    print("inner", sys.argv[3], "rho", rho, ": status", r.status, r.message, "| fewest rectangles found (root included):", None if r.x is None else round(r.fun),
          "| solver lower bound:", getattr(r, 'mip_dual_bound', None), "(%.0f s)" % (time.time() - t0))
    if r.x is not None:
        pp = r.x[:n]; nz = [(len(rown[i // len(coln)]), len(coln[i % len(coln)]), round(float(pp[i]), 6)) for i in range(n) if abs(pp[i]) > 1e-7]
        from collections import Counter
        print("   shapes (rows, columns, number): ", sorted(Counter(nz).items()))
    sys.stdout.flush()
