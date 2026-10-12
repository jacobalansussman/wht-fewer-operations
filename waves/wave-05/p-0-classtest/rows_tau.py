#!/usr/bin/env python3
"""rows_tau.py (p-0-classtest): target rows for mincirc: the k-th Kronecker power of K = [[1,1],[1,tau]] modulo p.
row w, column x: tau^(number of common 1-bits of w and x).  usage: rows_tau.py k p tau   (tau an integer modulo p)"""
import sys
k, p, tau = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]) % int(sys.argv[2])
N = 1 << k
for w in range(N): print(' '.join(str(pow(tau, bin(w & x).count('1'), p)) for x in range(N)))
