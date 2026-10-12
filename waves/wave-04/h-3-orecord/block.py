#!/usr/bin/env python3
"""h-3-orecord / block.py.  Exact (Fractions).  A reflection through SEVERAL centres at once.
Centres c_a = (character a) * h, h = the 4-point hub pattern on two chosen address bits, a running over a set A of characters.
R = I - (2/N) * sum_a c_a c_a^T.   Reported: is R orthogonal; is it block diagonal on blocks of 4 points; how many rows of
H * R equal a row of H; supports of the rows of H * R."""
from fractions import Fraction as Fr
import itertools
def H(k):
    N = 1 << k; return [[(-1) ** bin(j & x).count('1') for x in range(N)] for j in range(N)]
def run(k, A, name):
    N = 1 << k; Hm = H(k)
    h = [(-1) ** (((x >> 0) & 1) * ((x >> 1) & 1)) for x in range(N)]            # sign pattern + + + - on bits 0,1
    C = [[Hm[a][x] * h[x] for x in range(N)] for a in A]
    for i, j in itertools.combinations(range(len(C)), 2): assert sum(p * q for p, q in zip(C[i], C[j])) == 0, 'centres not orthogonal'
    R = [[Fr(1 if i == j else 0) - Fr(2, N) * sum(c[i] * c[j] for c in C) for j in range(N)] for i in range(N)]
    RR = [[sum(R[i][t] * R[t][j] for t in range(N)) for j in range(N)] for i in range(N)]
    orth = RR == [[Fr(1 if i == j else 0) for j in range(N)] for i in range(N)]
    blocks = {}
    for i in range(N):
        blocks.setdefault(tuple(j for j in range(N) if R[i][j] != 0), []).append(i)
    width = sorted({len(b) for b in blocks})
    M = [[sum(Hm[i][t] * R[t][j] for t in range(N)) for j in range(N)] for i in range(N)]
    kept = sum(1 for i in range(N) if M[i] == [Fr(z) for z in Hm[i]]); sup = sorted({sum(1 for z in r if z) for r in M})
    ent = sorted({str(z) for r in R for z in r})
    print('%-46s N=%-3d centres=%-2d orthogonal=%s  non-zeros per row of R: %s  entries of R: %s  rows of H kept: %d  row supports of H*R: %s' % (name, N, len(A), orth, width, ent, kept, sup))
for k in (3, 4, 5):
    N = 1 << k
    run(k, [a for a in range(N) if a & 3 == 0], 'all characters trivial on bits 0,1 (N/4 centres)')
    run(k, [0], 'one centre')
    if k >= 4: run(k, [a for a in range(N) if a & 7 == 0], 'characters trivial on bits 0,1,2 (N/8 centres)')
