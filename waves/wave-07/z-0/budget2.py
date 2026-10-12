# z-0/budget2.py : skeptic's own check of x-0 lemma 2 (largest (|a|+|b|)/g of ONE gate g*w = a*u + b*v between primitive
# whole-number vectors with entries of size at most M).  Written without reading budget.py's method: here the value is taken
# as (|det(w,v)| + |det(u,w)|) / |det(u,v)| on a pivot pair of coordinates (Cramer), exact integers, numpy int64.
# usage: budget2.py <dimension> <M1> <M2> ...
import sys, itertools
import numpy as np
from math import gcd
from fractions import Fraction as F

def prims(M, n):
    out = []
    for t in itertools.product(range(-M, M + 1), repeat=n):
        g = 0
        for x in t: g = gcd(g, abs(x))
        if g != 1: continue
        if next(x for x in t if x) > 0: out.append(t)     # one of each +- pair
    return np.array(out, dtype=np.int64)

def run(M, n):
    P = prims(M, n); m = len(P)
    isform = (np.abs(P).max(axis=1) == 1)
    best = F(0); bestform = F(0); bestmerge = F(0); ex = exf = exm = None
    negbudget = None
    for iu in range(m):
        u = P[iu]
        for iv in range(iu + 1, m):
            v = P[iv]
            piv = None
            for i in range(n):
                for j in range(i + 1, n):
                    D = int(u[i] * v[j] - u[j] * v[i])
                    if D: piv = (i, j, D); break
                if piv: break
            if not piv: continue          # parallel: cannot happen for distinct primitive vectors up to sign
            i, j, D = piv
            A = P[:, i] * v[j] - P[:, j] * v[i]          # D*w = A*u + B*v
            B = u[i] * P[:, j] - u[j] * P[:, i]
            ok = (A != 0) & (B != 0)
            if n > 2:
                ok &= ((D * P) == (A[:, None] * u[None, :] + B[:, None] * v[None, :])).all(axis=1)
            if not ok.any(): continue
            S = np.abs(A) + np.abs(B)
            aD = abs(D)
            disjoint = not np.any((u != 0) & (v != 0))
            idx = np.nonzero(ok)[0]
            s = int(S[idx].max())
            if F(s, aD) > best:
                k = idx[np.argmax(S[idx])]; best = F(s, aD); ex = (tuple(u), tuple(v), tuple(P[k]), int(A[k]), int(B[k]), D)
            fidx = idx[isform[idx]]
            if len(fidx):
                s = int(S[fidx].max())
                if F(s, aD) > bestform:
                    k = fidx[np.argmax(S[fidx])]; bestform = F(s, aD); exf = (tuple(u), tuple(v), tuple(P[k]), int(A[k]), int(B[k]), D)
            if disjoint:
                s = int(S[idx].max())
                if F(s, aD) > bestmerge:
                    k = idx[np.argmax(S[idx])]; bestmerge = F(s, aD); exm = (tuple(u), tuple(v), tuple(P[k]), int(A[k]), int(B[k]), D)
            if negbudget is None:
                smin = int(S[idx].min())
                if smin < aD:
                    k = idx[np.argmin(S[idx])]; negbudget = (tuple(u), tuple(v), tuple(P[k]), int(A[k]), int(B[k]), D)
    print('M=%d dim=%d primitive vectors (up to sign)=%d  bound 4M^2=%d  formula 4M^2-6M+3=%d  4M-4=%d  2M-1=%d' % (M, n, m, 4*M*M, 4*M*M-6*M+3, 4*M-4, 2*M-1))
    print('   any gate : %s   D*w = A*u + B*v : u,v,w,A,B,D = %s' % (best, ex))
    print('   w a form : %s   %s' % (bestform, exf))
    print('   u,v disjoint: %s   %s' % (bestmerge, exm))
    print('   a gate with (|a|+|b|)/g < 1 (negative budget), first met: %s' % (negbudget,))
    sys.stdout.flush()

n = int(sys.argv[1])
for M in map(int, sys.argv[2:]): run(M, n)
