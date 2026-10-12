#!/usr/bin/env python3
"""i-backwards play 2: how sparse can an eigenbasis of the 16-point transform be?  Exact (Fraction).
For the plain Sylvester H16 and for the relabelled H16' = H4' (x) H4' (H4' = 2I - u u^T): for each eigenvalue and each
support size s, the dimension spanned by all eigenvectors supported inside some s-subset."""
from fractions import Fraction as F
from itertools import combinations
import sys, time
def pc(x): return bin(x).count("1")
H4 = [[(-1) ** pc(x & y) for x in range(4)] for y in range(4)]
P = [0, 2, 1, 3]
H4p = [[H4[y][P[x]] for x in range(4)] for y in range(4)]
def kron(A, B): return [[a * b for a in ra for b in rb] for ra in A for rb in B]
mats = {"plain H16": kron(H4, H4), "relabelled H16'": kron(H4p, H4p)}
def nullspace(M, cols):
    M = [[F(v) for v in r] for r in M]; rows = len(M); r = 0; piv = []
    for c in range(cols):
        p = next((i for i in range(r, rows) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]; pv = M[r][c]; M[r] = [v / pv for v in M[r]]
        for i in range(rows):
            if i != r and M[i][c] != 0:
                f = M[i][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        piv.append(c); r += 1
        if r == rows: break
    out = []
    for fc in (c for c in range(cols) if c not in piv):
        v = [F(0)] * cols; v[fc] = F(1)
        for i, c in enumerate(piv): v[c] = -M[i][fc]
        out.append(v)
    return out
class Span:
    def __init__(s): s.b = []
    def add(s, v):
        v = list(v)
        for lead, w in s.b:
            if v[lead] != 0:
                f = v[lead]; v = [a - f * c for a, c in zip(v, w)]
        lead = next((i for i, a in enumerate(v) if a != 0), None)
        if lead is None: return False
        v = [a / v[lead] for a in v]; s.b.append((lead, v)); return True
t0 = time.time()
for name, H in mats.items():
    for lam in (4, -4):
        A = [[H[i][j] - (lam if i == j else 0) for j in range(16)] for i in range(16)]
        mult = 16 - sum(1 for _ in [0])  # placeholder
        full = len(nullspace(A, 16))
        sp = Span(); line = []
        for sz in range(1, 9):
            for S in combinations(range(16), sz):
                if len(sp.b) == full: break
                for v in nullspace([[A[i][j] for j in S] for i in range(16)], sz):
                    w = [F(0)] * 16
                    for j, c in zip(S, v): w[j] = c
                    sp.add(w)
            line.append("<=%d:%d" % (sz, len(sp.b)))
            if len(sp.b) == full: break
        print("%-16s eigenvalue %+d (multiplicity %d): span of eigenvectors by support size  %s   [%.0fs]" % (name, lam, full, "  ".join(line), time.time() - t0))
        sys.stdout.flush()
