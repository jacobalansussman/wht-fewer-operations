#!/usr/bin/env python3
"""milp.py m Wmax -- the ladder in W: fewest moves that counting and parity allow, old letters only.  [e2-2-ladder]
Necessary conditions for a word of mixing, shifts and directions serving W live arrays at block size m (e2-2.md, section 2):
  n_z = number of moves in direction z (z a non-zero bit vector of length m), integers >= 0;
  (cover)  for every quadratic form q with q(I) = 1:   sum over z with q(z) = 1 of n_z  >=  W        [rank argument]
  (parity) sum_z n_z z z^T = W I  modulo 2                                                           [determinant; no scratch]
Minimise the number of moves.  A value below m W would not be a unit; it says counting does not forbid one.
HiGHS integer programme on integer data; the optimum is reported with the solver's status.  'noparity' drops (parity),
which is the right relaxation when scratch arrays are allowed (the determinant argument needs a square system).
"""
import sys, math, itertools
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
m = int(sys.argv[1]); Wmax = int(sys.argv[2]); Wmin = int(sys.argv[3]) if len(sys.argv) > 3 else 1; TL = float(sys.argv[4]) if len(sys.argv) > 4 else 25
pairs = [(i, j) for i in range(m) for j in range(i, m)]
V = list(range(1, 1 << m))
def qval(Q, z):          # Q: dict pair -> bit
    s = 0
    for k, (i, j) in enumerate(pairs):
        if Q >> k & 1 and z >> i & 1 and z >> j & 1: s ^= 1
    return s
diag = [k for k, (i, j) in enumerate(pairs) if i == j]
rows = set()
for Q in range(1, 1 << len(pairs)):
    if sum(Q >> k & 1 for k in diag) & 1:
        rows.add(tuple(qval(Q, z) for z in V))
A = np.array(sorted(rows), dtype=float)
# drop dominated rows (a row whose 1-set contains another row's 1-set is implied)
keep = []
order = np.argsort(A.sum(axis=1), kind="stable")
for r in order:
    if not keep or not np.any(np.all(A[keep] <= A[r], axis=1)):
        keep.append(r)
A = A[keep]
print("m = %d: %d covering constraints after removing implied ones (lightest has %d ones, heaviest %d)"
      % (m, len(A), int(A.sum(axis=1).min()), int(A.sum(axis=1).max())), flush=True)
P = np.array([[ (z >> i & 1) * (z >> j & 1) for z in V] for (i, j) in pairs], dtype=float)   # (zz^T)_ij
nz, npar = len(V), len(pairs)
for W in range(Wmin, Wmax + 1):
    out = []
    for parity in (True, False):
        if parity:
            c = np.concatenate([np.ones(nz), np.zeros(npar)])
            Acov = np.hstack([A, np.zeros((len(A), npar))])
            Apar = np.hstack([P, -2 * np.eye(npar)])
            rhs = np.array([W % 2 if i == j else 0 for (i, j) in pairs], dtype=float)
            cons = [LinearConstraint(Acov, W, np.inf), LinearConstraint(Apar, rhs, rhs)]
            res = milp(c, constraints=cons, integrality=np.ones(nz + npar), bounds=Bounds(0, np.inf), options={"time_limit": TL})
        else:
            res = milp(np.ones(nz), constraints=[LinearConstraint(A, W, np.inf)], integrality=np.ones(nz), bounds=Bounds(0, np.inf), options={"time_limit": TL})
        if res.x is None:
            out.append((None, res.message)); continue
        k = int(round(res.fun)); n = np.round(res.x[:nz]).astype(int)
        out.append((k, res.status, n, getattr(res, 'mip_dual_bound', None)))
    s = "W = %d: plain %d moves; " % (W, m * W)
    for lab, o in zip(("with parity", "without parity"), out):
        if o[0] is None: s += "%s: no solution (%s); " % (lab, o[1])
        else:
            k = o[0]
            z = math.log(k / W) / math.log(m)
            s += "%s: %d moves (status %d: 0 = proved optimal, 1 = time limit, then only 'at most'; solver's lower bound %s), %.3f per array, z if realised with single moves %.4f; " % (lab, k, o[1], o[3], k / W, z)
    print(s, flush=True)
    if out[0][0] is not None and out[0][0] < m * W:
        n = out[0][2]
        print("      example of counts (direction: times): " + ", ".join("%s:%d" % (format(V[i], "0%db" % m), n[i]) for i in range(nz) if n[i]))
