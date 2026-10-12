#!/usr/bin/env python3
"""eigdim.py [ab-8-reconcilecaps] FLOATS.  Multiplicities of the eigenvalues of the knows graph of one type (same graph as eig.py).
If E is the projection onto the eigenspace of the smallest eigenvalue lmin (multiplicity f), then  A - lmin*I  is positive
semidefinite of rank n - f, has diagonal |lmin| and is zero exactly where A is zero off the diagonal, so M = (A - lmin I)/|lmin|
is a symmetric positive scatter with kappa = n / (n - f)."""
import sys, numpy as np
sys.argv = sys.argv[:4]
import importlib.util, io, contextlib
src = open('eig.py').read().split("w = np.linalg.eigvalsh")[0]
exec(src)
w = np.linalg.eigvalsh(A.astype(np.float64)); r6 = np.round(w, 5)
vals, counts = np.unique(r6, return_counts=True)
print('class (%d,%d) type %s: n = %d, degree %d; eigenvalue: multiplicity  %s' % (h, r, want, n, d, ' ; '.join('%g: %d' % (float(a), int(b)) for a, b in zip(vals, counts))))
f = int(counts[0]); lmin = float(vals[0])
print('   M = (A + %g I)/%g is a symmetric positive scatter of rank n - f = %d : kappa = %.4f ; (three-stage gain needs > %.3f, five-stage > %.3f)' % (-lmin, -lmin, n - f, n / (n - f), 1.5 * h / r, 1.25 * h / r))
