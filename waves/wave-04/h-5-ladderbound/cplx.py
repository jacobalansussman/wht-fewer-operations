#!/usr/bin/env python3
# h-5 / cplx.py : is a real wire the real part of ONE complex product wire c * (1, e_1) x (1, e_2) x ... with every e_b = +i or -i ?
# Exact Gaussian integers (pairs of ints).  Tested: the brick's hub at 4 points and the width-3 wires g7..g11 of g-1's 19-gate program.
import itertools
def mul(a, b): return (a[0]*b[0] - a[1]*b[1], a[0]*b[1] + a[1]*b[0])
def test(w, k):
    N = 1 << k; hits = []
    for eps in itertools.product((1, -1), repeat=k):
        for c in [(a, b) for a in range(-2, 3) for b in range(-2, 3) if (a, b) != (0, 0)]:
            ok = True
            for x in range(N):
                z = c
                for b in range(k):
                    if (x >> b) & 1: z = mul(z, (0, eps[b]))
                if z[0] != w[x]: ok = False; break
            if ok: hits.append((eps, c))
    return hits
W = {'hub (4 points)': ((1, 1, -1, 1), 2), 'g7 centre': ((1,-1,-1,-1,1,1,-1,1), 3), 'g8': ((1,-1,-1,-1,1,1,-1,-1), 3), 'g9': ((1,-1,-1,-1,1,-1,-1,1), 3),
     'g10': ((1,-1,-1,-1,1,1,1,-1), 3), 'g11': ((1,-1,-1,-1,-1,-1,-1,1), 3), 'hub11 of the 20': ((1,1,1,1,1,1,-1,-1), 3)}
for name, (w, k) in W.items():
    h = test(w, k)
    print('%-16s %s : %s' % (name, w, ('real part of c * product of (1, +-i): signs %s, c = %d%+di' % (h[0][0], h[0][1][0], h[0][1][1])) if h else 'not of that form'))
