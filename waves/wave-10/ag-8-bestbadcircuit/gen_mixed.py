#!/usr/bin/env python3
"""gen_mixed.py (ag-8): a textbook butterfly network for the N-point transform in which the inner 4-point blocks (the cosets of
the two lowest address bits) use DIFFERENT pairings of their four points.  N = 4 * B blocks; pairing code per block:
0 = pairs (0,1),(2,3)  1 = pairs (0,2),(1,3)  2 = pairs (0,3),(1,2).  The outer bits use the textbook order.  N log2 N gates.
usage: gen_mixed.py k code_string   e.g.  gen_mixed.py 4 0212   writes mixed_<k>_<codes>.txt"""
import sys
k = int(sys.argv[1]); codes = [int(c) for c in sys.argv[2]]; N = 1 << k; B = N // 4
assert len(codes) == B
PAIR = {0: ((0, 1), (2, 3)), 1: ((0, 2), (1, 3)), 2: ((0, 3), (1, 2))}
lines = []; cnt = [0]
def gate(u, su, v, sv):
    cnt[0] += 1; nm = 'g%d' % cnt[0]; lines.append('%s = %s%s %s %s' % (nm, '-' if su < 0 else '', u, '-' if sv < 0 else '+', v)); return nm
# inner blocks: wires for the four characters of the block, indexed by the character's sign vector on the block's points
blockw = []
for b in range(B):
    pts = [4 * b + i for i in range(4)]; (p, q), (r, s) = PAIR[codes[b]]
    s1 = gate('x%d' % pts[p], 1, 'x%d' % pts[q], 1); d1 = gate('x%d' % pts[p], 1, 'x%d' % pts[q], -1)
    s2 = gate('x%d' % pts[r], 1, 'x%d' % pts[s], 1); d2 = gate('x%d' % pts[r], 1, 'x%d' % pts[s], -1)
    W = {}
    for (u, eu, v, ev) in ((s1, (1, 1), s2, (1, 1)), (d1, (1, -1), d2, (1, -1))):
        for sg in (1, -1):
            vec = [0] * 4; vec[p], vec[q] = eu; vec[r], vec[s] = sg * ev[0], sg * ev[1]
            if vec[0] < 0: raise SystemExit('sign')
            W[tuple(vec)] = gate(u, 1, v, sg)
    blockw.append(W)
chars = [tuple((-1) ** bin(w & i).count('1') for i in range(4)) for w in range(4)]
for ch in chars:
    cur = [blockw[b].get(ch) or blockw[b][tuple(-x for x in ch)] for b in range(B)]
    sgn = [1 if ch in blockw[b] else -1 for b in range(B)]
    assert all(s == 1 for s in sgn)
    step = 1
    while step < B:
        new = list(cur)
        for b in range(0, B, 2 * step):
            for o in range(step):
                new[b + o] = gate(cur[b + o], 1, cur[b + o + step], 1); new[b + o + step] = gate(cur[b + o], 1, cur[b + o + step], -1)
        cur = new; step *= 2
open('mixed_%d_%s.txt' % (k, sys.argv[2]), 'w').write('# ag-8: mixed-pairing butterfly network, %d points, pairings %s, %d gates, count (G)\n' % (N, sys.argv[2], cnt[0]) + '\n'.join(lines) + '\n')
print('wrote', cnt[0], 'gates')
