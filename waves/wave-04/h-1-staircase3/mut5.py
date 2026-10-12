#!/usr/bin/env python3
"""h-1 mut5.py: e2-0 mutation 5 on the 4-point brick, exact fractions.  Count (G).
Hub M_t = (1,1,0,0) + t*(0,0,1,-1) = (1,1,t,-t)  (piece of one character on the lower pair plus t times the piece of the other
character on the upper pair).  For each of the four outputs y of H_4, find every scalar s for which y - s*M_t has the fewest
non-zeros, and report that number: 1 means the partner is a single input (free), 2 means the partner is a two-term wire that
costs a gate of its own."""
from fractions import Fraction as F
H = [(1, 1, 1, 1), (1, -1, 1, -1), (1, 1, -1, -1), (1, -1, -1, 1)]
def best(M, y):
    cands = {F(y[i], M[i]) for i in range(4) if M[i] != 0}
    res = []
    for s in cands:
        r = [y[i] - s * M[i] for i in range(4)]; res.append((sum(1 for x in r if x), s, r))
    return min(res, key=lambda z: z[0])
for t in [F(1), F(-1), F(2), F(3), F(1, 2), F(-2), F(5, 3), F(7)]:
    row = []
    for form, M in (('(1,1,t,-t)', (F(1), F(1), t, -t)), ('(1,1,-t,t) ', (F(1), F(1), -t, t))):
        nz = [best(M, y)[0] for y in H]
        gates = 2 + 1 + sum(1 for n in nz if n == 2) + 4 if max(nz) <= 2 else None
        row.append('%s partners have %s non-zeros -> brick costs %s gates' % (form, nz, gates))
    print('t = %-4s  %s' % (t, ' ; '.join(row)))
print('t = +-1: every partner is a single input: 2 pieces + hub + 4 outputs = 7.  Any other t: every partner has two terms: 7 + 4 = 11 > 8.')
print('reason: y - M_t/s restricted to the pair where they differ is proportional to (1-t, 1+t) or (1+t, 1-t); one entry vanishes only if t*t = 1.')
