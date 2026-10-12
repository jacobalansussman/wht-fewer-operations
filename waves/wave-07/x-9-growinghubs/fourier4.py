#!/usr/bin/env python3
"""x-9-growinghubs/fourier4.py: the Fourier cell of x-9.md section 4, item 4, at its smallest size (4 points), exact.
Gaussian integers as Python complex numbers with small whole parts (exact in floating point at this size).
Coordinates (L1, L2, R1, R2) = (x0, x2, x1, x3): upper bit = parity of the index, lower bit = the other bit.
Row j of the 4-point Fourier transform is the product wire (lower slope p, upper slope r) = ((-1)^j, i^j)."""
i = 1j
rows = {j: (1, (-1) ** j, i ** j, (-1) ** j * i ** j) for j in range(4)}
for j in range(4):   # sanity: row j at index x = y0 + 2*y1 is i^(j x); coordinates are (x0, x2, x1, x3)
    assert rows[j] == tuple(i ** (j * x) for x in (0, 2, 1, 3))
def one_gate(M, O, cands):
    """witnesses w (from cands) with O = a*M + b*w"""
    res = []
    for name, w in cands.items():
        for p in range(4):
            for q in range(p + 1, 4):
                d = M[p] * w[q] - M[q] * w[p]
                if d != 0:
                    a = (O[p] * w[q] - O[q] * w[p]) / d; b = (M[p] * O[q] - M[q] * O[p]) / d
                    if a != 0 and b != 0 and all(abs(a * M[t] + b * w[t] - O[t]) < 1e-12 for t in range(4)): res.append(name)
                    break
            else: continue
            break
    return res
quarters = {'x0': (1, 0, 0, 0), 'x2': (0, 1, 0, 0), 'x1': (0, 0, 1, 0), 'x3': (0, 0, 0, 1)}
weighted = {'x0+(%s)x2' % s: (1, c, 0, 0) for s, c in (('i', i), ('-i', -i))}
weighted.update({'x1+(%s)x3' % s: (0, 0, 1, c) for s, c in (('i', i), ('-i', -i))})
for t, nm in ((1, 't = rho = 1'), (i, 't = i rho = i')):
    M = (1, 1, t, -t)
    print('hub (x0 + x2) + t (x1 - x3), %s:' % nm)
    for j in range(4):
        print('   row %d  slopes (%s, %s): single-input witnesses %s ; weighted-pair witnesses %s'
              % (j, rows[j][1], rows[j][2], one_gate(M, rows[j], quarters), one_gate(M, rows[j], weighted)))
