# u-8-compose: (1) the tensor law on factors that are NOT on the floor; (2) joins J and shifts S of every composition:
#   e = (J - (N-1)) + (S - (N/2) log2 N)   (identity: gates = J + S when there are no Q or E gates).
# kinds as in m-cross: J = three different classes; S = result has the class of a parent; Q = parents share a class, result another.
import sys
exec(open('compose.py').read().split("if __name__ == '__main__':")[0])
def kinds(label, g, pred=None):
    N = npts(g); k = N.bit_length() - 1; out, W = outputs(g, N)
    ok = len(out) == N and all(f in (1, -1) for (_, f) in out.values())
    K = dict(J=0, S=0, Q=0, E=0)
    for (name, a, u, b, v) in g:
        cu, cv, cw = cls(W[u]), cls(W[v]), cls(W[name])
        K['E' if cu == cv == cw else 'Q' if cu == cv else 'S' if cw in (cu, cv) else 'J'] += 1
    G = len(g); e = G - (N - 1) - N * k // 2
    print('%-26s N=%3d gates=%4d exact_H=%s  J=%3d S=%3d Q=%d E=%d   duplicate joins D=J-(N-1)=%3d   S-(N/2)log2N=%3d   e=%3d%s'
          % (label, N, G, ok, K['J'], K['S'], K['Q'], K['E'], K['J'] - (N - 1), K['S'] - N * k // 2, e, '' if pred is None else '   law predicts %d: %s' % (pred, 'agrees' if pred == e else 'DISAGREES')))
    return e
brick = parse(ID + 'h-6-classhub/brick_m1.txt'); n19 = parse(ID + 'g-1-tightwires/h8_19gates.txt')
t2 = [('s', F(1), 'x0', F(1), 'x1'), ('d', F(1), 'x0', F(-1), 'x1')]
st = {N: parse(ID + 'e2-0-pieces/slp_%d.txt' % N) for N in (8, 16, 32, 64)}
t4 = tensor(t2, t2)
law = lambda m, eA, n, eB: n * eA + m * eB + (m - 1) * (n - 1)
print('--- the ways to put two bricks (or their relatives) on 16 points that I could build and replay')
kinds('textbook 16 = t2^4', tensor(t4, t4), law(4, 1, 4, 1))
kinds('brick x textbook4', tensor(brick, t4), law(4, 0, 4, 1))
kinds('textbook4 x brick', tensor(t4, brick), law(4, 1, 4, 0))
kinds('brick x brick (tensor)', tensor(brick, brick), law(4, 0, 4, 0))
kinds('staircase8 x t2', tensor(st[8], t2), law(8, 1, 2, 0))
kinds('t2 x staircase8', tensor(t2, st[8]), law(2, 0, 8, 1))
kinds('19 x t2', tensor(n19, t2), law(8, 0, 2, 0))
kinds('t2 x 19', tensor(t2, n19), law(2, 0, 8, 0))
kinds('staircase 16', st[16])
kinds('second 52 (h-1)', parse(ID + 'h-1-staircase3/slp16_52_from54.txt'))
print('--- smaller and larger')
kinds('brick', brick); kinds('the 19', n19); kinds('staircase 8', st[8]); kinds('staircase 32', st[32]); kinds('staircase 64', st[64])
kinds('brick x 19', tensor(brick, n19), law(4, 0, 8, 0)); kinds('19 x brick', tensor(n19, brick), law(8, 0, 4, 0))
kinds('brick x staircase8', tensor(brick, st[8]), law(4, 0, 8, 1)); kinds('staircase8 x brick', tensor(st[8], brick), law(8, 1, 4, 0))
kinds('19 x 19', tensor(n19, n19), law(8, 0, 8, 0)); kinds('staircase8 x staircase8', tensor(st[8], st[8]), law(8, 1, 8, 1))
kinds('brick x staircase16', tensor(brick, st[16]), law(4, 0, 16, 5)); kinds('staircase16 x brick', tensor(st[16], brick), law(16, 5, 4, 0))
