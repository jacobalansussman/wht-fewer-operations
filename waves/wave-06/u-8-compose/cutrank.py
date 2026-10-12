# u-8-compose: cut-rank meter.  A wire is a vector over the N = 2^k addresses.  For a split of the address bits into a set S and the
# rest, lay the wire out as a 2^|S| x 2^(k-|S|) table and take its rank over the rationals (exact fractions).  A product wire has rank 1
# at every split.  maxrank(w) = the largest rank over all splits.  Also: the node excess  eps_t = (wires on support t) - 1 - |t|/2,
# whose sum over the supports is the excess e (identity, derived in u-8.md).
import sys, itertools
from fractions import Fraction as F
exec(open('compose.py').read().split("if __name__ == '__main__':")[0])
def rank(M):
    M = [list(r) for r in M]; r = 0
    for c in range(len(M[0])):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        for i in range(r + 1, len(M)):
            if M[i][c] != 0:
                f = M[i][c] / M[r][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
        if r == len(M): break
    return r
def splits(k):
    out = []
    for size in range(1, k // 2 + 1):
        for S in itertools.combinations(range(k), size):
            if 2 * size == k and 0 not in S: continue
            out.append(S)
    return out
def table(w, S, k):
    R = [b for b in range(k) if b not in S]
    rows = []
    for a in range(1 << len(S)):
        row = []
        for b in range(1 << len(R)):
            x = sum(((a >> i) & 1) << S[i] for i in range(len(S))) | sum(((b >> i) & 1) << R[i] for i in range(len(R)))
            row.append(w[x])
        rows.append(row)
    return rows
def run(label, g):
    N = npts(g); k = N.bit_length() - 1; out, W = outputs(g, N); sp = splits(k)
    hist = {}; tot = 0; H = [[(-1) ** bin(y & x).count('1') for x in range(N)] for y in range(N)]; V = 0
    supp = {}
    for (name, *_ ) in g:
        w = W[name]; mr = max(rank(table(w, S, k)) for S in sp)
        hist[mr] = hist.get(mr, 0) + 1; tot += mr - 1
        s = sum(1 for t in w if t != 0); s2 = sum(1 for y in range(N) if sum(H[y][x] * w[x] for x in range(N)) != 0)
        if s * s2 > N: V += 1
        c = cls(w); supp[c] = supp.get(c, 0) + 1
    G = len(g); eps = {}
    for c, a in supp.items():
        s = sum(c); eps.setdefault(s, []).append(a - 1 - s // 2)
    e = G - (N - 1) - N * k // 2
    print('%-22s N=%3d gates=%4d saved vs textbook=%3d  over-limit wires=%3d  sum(maxrank-1)=%3d  wires by maxrank %s' % (label, N, G, N * k - G, V, tot, sorted(hist.items())))
    print('      node excess by support size (sum over the nodes of that size): %s   total = %d  (e = %d)' % (', '.join('%d: %+d' % (s, sum(v)) for s, v in sorted(eps.items())), sum(sum(v) for v in eps.values()), e))
brick = parse(ID + 'h-6-classhub/brick_m1.txt'); n19 = parse(ID + 'g-1-tightwires/h8_19gates.txt')
run('brick', brick); run('the 19', n19)
for N in (8, 16, 32): run('staircase %d' % N, parse(ID + 'e2-0-pieces/slp_%d.txt' % N))
run('second 52 (h-1)', parse(ID + 'h-1-staircase3/slp16_52_from54.txt'))
run('brick x brick', parse('tensor_brick_x_brick.txt')); run('19 x t2', parse('tensor_19_x_t2.txt')); run('t2 x 19', parse('tensor_t2_x_19.txt'))
run('brick x 19', parse('tensor_brick_x_19.txt')); run('19 x brick', parse('tensor_19_x_brick.txt'))
