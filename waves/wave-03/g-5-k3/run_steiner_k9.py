#!/usr/bin/env python3
"""g-5-k3: j-machine/steiner.py (unchanged, imported) on the 9-point target K3 (x) K3, count (G).
Task 'K9': seeded with my 22-gate circuit (k9_22.json).  Task 'K9e': same target, no seed."""
import sys, json, numpy as np
sys.path.insert(0, '.')
import slp, steiner
K3 = np.array([[1, 1, 1], [2, 0, -2], [1, -1, 1.]])
_orig = slp.task
def task(name):
    if name in ('K9', 'K9e', 'K9n', 'H8n'):
        T = np.kron(K3, K3)
        if name == 'K9e': return T, [], []
        if name == 'H8n':
            H2 = np.array([[1, 1], [1, -1.]]); T = np.kron(np.kron(H2, H2), H2)
        d = json.load(open({'K9': 'k9_22.json', 'K9n': 'k9_new22.json', 'H8n': 'h8_pair22.json'}[name]))
        nin = d['n']
        # steiner.py normalises every gate to u + c*v, so node scales differ from mine: carry the scale along.
        from fractions import Fraction as Fr
        sc = [Fr(1)] * nin; g = []
        for (u, v, a, b) in d['gates']:
            a = Fr(a); b = Fr(b); c = b * sc[u] / (a * sc[v]); g.append((u, v, 1.0, float(c))); sc.append(sc[u] / a)
        return T, g, []
    return _orig(name)
slp.task = task
steiner.main()
