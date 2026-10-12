# ab-4-zcut/ztree.py : the crossing-helper inequality down a whole cube tree, on every optimal 12-gate circuit for Z at 8 points.
# Count (G). Exact.   For a node X of a cube tree (a block of addresses: some bits free, the others fixed), halves X0, X1:
#   n(X)  = number of distinct non-trivial classes among the circuit's wires cut down to X  (x-2's count; order-free)
#   Xh(X) = number of those classes that are non-zero on both halves of X and are NOT a row of subset sums on X
# Claim [derived, ab-4.md section 3]:  n(X) >= n(X0) + n(X1) + |X|/2 - Xh(X)  at every node, hence
#   gates >= (N/2) log2 N - (sum over the nodes of Xh).         Trees: the 6 orders of the 3 address bits.
import sys, re, itertools
exec(open('zmeter.py').read().split('def projections')[0])
def lift(d, p): return tuple((x if x <= p // 2 else x - p) for x in d)
def classes(wires, X):
    out = set()
    for w in wires:
        c = prim([w[i] for i in X])
        if c is not None and sum(1 for t in c if t) > 1: out.add(c)
    return out
def nodes(order):
    res = []
    def rec(X, d):
        if len(X) == 1: return
        b = order[d]; X0 = [x for x in X if not x >> b & 1]; X1 = [x for x in X if x >> b & 1]
        # reorder X so that X = X0 + X1 position-wise
        res.append((X0 + X1, X0, X1)); rec(X0, d + 1); rec(X1, d + 1)
    rec(list(range(N)), 0); return res
p = int(sys.argv[1]); tot = 0; hist = {}; best = {}; persize = {}
for line in open(sys.argv[2]):
    if 'example' not in line: continue
    hs = [lift([int(ch) for ch in h], p) for h in re.findall(r'\[(\d+)\]', line)]
    wires = list(hs) + list(targets)
    # replay check as in zmeter
    need = pairs_for(wires); made = 0; ch = True
    while ch:
        ch = False
        for g in range(12):
            if not made >> g & 1 and any(m & made == m for m in need[g]): made |= 1 << g; ch = True
    if made != 4095: continue
    tot += 1; sums = []
    for order in itertools.permutations(range(3)):
        s = 0
        for (X, X0, X1) in nodes(order):
            h = len(X0); cl = classes(wires, X); zr = {prim([r[i] for i in X]) for r in Zrows} - {None}
            xh = sum(1 for c in cl if any(c[:h]) and any(c[h:]) and c not in zr)
            n, n0, n1 = len(cl), len(classes(wires, X0)), len(classes(wires, X1))
            assert n >= n0 + n1 + h - xh, (hs, order, X, n, n0, n1, xh)
            s += xh; k = (len(X), xh, n - n0 - n1 - h + xh); persize[k] = persize.get(k, 0) + 1
        assert 12 >= 12 - s
        sums.append(s)
    hist[tuple(sorted(sums))] = hist.get(tuple(sorted(sums)), 0) + 1; best[min(sums)] = best.get(min(sums), 0) + 1
print('p=%d: %d circuits x 6 trees: the inequality n(X) >= n(X0) + n(X1) + |X|/2 - Xh(X) holds at every node' % (p, tot))
print('least over the 6 trees of (sum over nodes of Xh) : number of circuits   [0 = no crossing helper anywhere in some tree]')
for k in sorted(best): print('   %d : %d' % (k, best[k]))
print('(size of node, Xh, slack of the inequality) : count over circuits x trees x nodes')
for k in sorted(persize): print('   size %d Xh=%d slack=%d : %d' % (*k, persize[k]))
