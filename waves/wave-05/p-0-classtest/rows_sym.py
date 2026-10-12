#!/usr/bin/env python3
"""rows_sym.py (p-0-classtest): the class of g-5's K3.  K3 is the 4-point kernel power K (x) K acting on data that are symmetric
under the swap of the two address bits: with K = [[1,1],[1,tau]] it is S_tau = [[1,2,1],[1,1+tau,tau],[1,2tau,tau^2]]
(columns: x00, x01 = x10, x11; rows: w = 00, 01 = 10, 11).  At tau = -1 the middle entry 1 + tau is ZERO: that zero is what g-5 uses.
Prints the 6 rows of S_tau (x) K_sigma modulo p.  usage: rows_sym.py p tau [sigma]"""
import sys
p = int(sys.argv[1]); t = int(sys.argv[2]) % p; s = int(sys.argv[3]) % p if len(sys.argv) > 3 else t
S = [[1, 2, 1], [1, 1 + t, t], [1, 2 * t, t * t]]; K = [[1, 1], [1, s]]
for i in range(3):
    for j in range(2): print(' '.join(str(S[i][a] * K[j][b] % p) for a in range(3) for b in range(2)))
