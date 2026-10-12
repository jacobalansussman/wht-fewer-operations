# p-7-twoletters: (1) tensor cuts at 32 and 64 points as explicit gate lists, exact replay, letter count;
# (2) e2-0's 52 made into two letters by COPYING four middle wires pairs (free) and computing the four middle hubs twice.
import sys
from fractions import Fraction as Fr
import letters as L
I = 'waves/wave-05'
g19 = L.parse(I + '/g-1-tightwires/h8_19gates.txt')
def brick(pre, ins, outs_):
    x0, x1, x2, x3 = ins
    return [(pre + 'a', Fr(1), x0, Fr(1), x1), (pre + 'b', Fr(-1), x2, Fr(1), x3), (pre + 'h', Fr(1), pre + 'a', Fr(1), pre + 'b'),
            (outs_[0], Fr(1), pre + 'h', Fr(2), x2), (outs_[1], Fr(-1), pre + 'h', Fr(2), x0), (outs_[2], Fr(1), pre + 'h', Fr(-2), x3), (outs_[3], Fr(1), pre + 'h', Fr(-2), x1)]
def nineteen(pre, ins, outs_):
    ren = lambda t: ins[int(t[1:])] if t.startswith('x') else (outs_[int(t[1:])] if t.startswith('y') else pre + t)
    return [(ren(n), a, ren(u), b, ren(v)) for (n, a, u, b, v) in g19]
# 32 points: (I4 x H8)(H4 x I8)
g = []
for i in range(8): g += brick('B%d' % i, ['x%d' % ((t << 3) | i) for t in range(4)], ['m%d_%d' % (t, i) for t in range(4)])
for t in range(4): g += nineteen('N%d' % t, ['m%d_%d' % (t, i) for i in range(8)], ['o%d_%d' % (t, y) for y in range(8)])
L.report("32 points: eight bricks, then the 19 four times", 32, g)
# 64 points: (I8 x H8)(H8 x I8)
g = []
for i in range(8): g += nineteen('A%d' % i, ['x%d' % ((t << 3) | i) for t in range(8)], ['m%d_%d' % (t, i) for t in range(8)])
for t in range(8): g += nineteen('C%d' % t, ['m%d_%d' % (t, i) for i in range(8)], ['o%d_%d' % (t, y) for y in range(8)])
L.report("64 points: the 19 eight times, then eight times", 64, g)
