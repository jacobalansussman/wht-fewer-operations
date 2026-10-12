#!/usr/bin/env python3
"""keynums.py -- the key numbers of the family's tables, from results.json (run collect.py first)."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, 'results.json')))
for W in (9, 12):
    print('W =', W)
    for N in (16, 32, 64, 128, 256):
        a = R.get('answer %d %d' % (N, W))
        if not a:
            continue
        T, C, F = a['textbook'], a['cfl1994'], a['family']
        for k in ('adders', 'bits', 'ice', 'ecp', 'xil', 'xc4', 'ice_pl', 'ecp_pl', 'ice_f', 'ecp_f', 'p_ice', 'p_ecp', 'p_xil'):
            t, c, f = T.get(k), C.get(k), F.get(k)
            if f is None:
                continue
            s = '  N=%-3d %-7s T=%-8s C=%-8s F=%-8s' % (N, k, t, c, f)
            if t:
                s += ' F/T=%.3f (%+.1f %%)' % (f / t, 100 * (f / t - 1))
            if c:
                s += ' F/C=%.3f (%+.1f %%)' % (f / c, 100 * (f / c - 1))
            print(s)
