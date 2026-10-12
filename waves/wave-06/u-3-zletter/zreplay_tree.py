# u-3-zletter/zreplay_tree.py : exact replay (whole numbers) of a subset-sum letter on one input merge tree.
# Input: a file whose line 2 (or only line) holds the N-1 internal node masks of the input tree (output of zmst), N = 2^K.
# It recomputes, with whole numbers only: the distance of every two of {0} + rows of Z (least number of tree nodes whose
# signed sum is the difference, by dynamic programme with traceback), a minimum spanning tree, then WRITES THE CIRCUIT as gates
# and replays it on all N basis vectors.  Gate count (G): a gate is a*u + b*v.  Prints tau, gates, and the design in subsets.
# Usage: python3 -B zreplay_tree.py K file [gates_out.txt]
import sys
K = int(sys.argv[1]); N = 1 << K
lines = [l for l in open(sys.argv[2]).read().splitlines() if l.strip() and not l.startswith('K') and not l.startswith('row')]
masks = [int(x) for x in lines[0].split()]
assert len(masks) == N - 1
full = (1 << N) - 1
nodes = sorted(set(masks) | {1 << i for i in range(N)}, key=lambda m: bin(m).count('1'))
assert len(nodes) == 2 * N - 1 and nodes[-1] == full
# children
child = {}
for m in nodes:
    if m & (m - 1) == 0: continue
    subs = [s for s in nodes if s != m and s & m == s]
    # maximal proper subnodes
    mx = [s for s in subs if not any(t != s and t & s == s for t in subs)]
    assert len(mx) == 2 and mx[0] | mx[1] == m and mx[0] & mx[1] == 0, (m, mx)
    child[m] = mx
for a in nodes:
    for b in nodes:
        assert a & b in (0, a, b)
Z = [[1 if (t & s) == t else 0 for t in range(N)] for s in range(N)] + [[0] * N]
def rep(d):
    # least number of nodes with whole-number coefficients whose sum is d; returns list of (mask, coef)
    vals = (-1, 0, 1)
    cost = {}
    for m in nodes:   # ascending size
        if m & (m - 1) == 0:
            x = m.bit_length() - 1
            cost[m] = {a: (0 if d[x] == a else 1, d[x]) for a in vals}   # (cost given incoming a, value chosen)
        else:
            l, r = child[m]
            s = {b: cost[l][b][0] + cost[r][b][0] for b in vals}
            bb = min(vals, key=lambda b: s[b])
            cost[m] = {a: ((s[a], a) if s[a] <= s[bb] + 1 else (s[bb] + 1, bb)) for a in vals}
    out = []
    def walk(m, a):
        c, b = cost[m][a]
        if b != a: out.append((m, b - a))
        if m & (m - 1):
            for ch in child[m]: walk(ch, b)
    walk(full, 0)
    assert len(out) == cost[full][0][0]
    v = [0] * N
    for m, c in out:
        for x in range(N):
            if m >> x & 1: v[x] += c
    assert v == list(d)
    return out
M = N + 1
R = {}
for a in range(M):
    for b in range(a):
        R[(a, b)] = rep([Z[a][x] - Z[b][x] for x in range(N)])      # a = b + sum
import os
GATES = 'GATES' in os.environ      # GATES=1: choose the spanning tree that minimises gates (a first step from 0 is free)
def w0(a, b): return len(R[(max(a, b), min(a, b))])
def w(a, b): return w0(a, b) - (1 if GATES and N in (a, b) else 0)
inn = {N}; par = {}; tau = 0; order = []
key = {i: (w(i, N), N) for i in range(N)}
while len(inn) < M:
    u = min((i for i in range(M) if i not in inn), key=lambda i: key[i][0])
    inn.add(u); par[u] = key[u][1]; tau += w0(u, key[u][1]); order.append(u)
    for i in range(M):
        if i not in inn and w(u, i) < key[i][0]: key[i] = (w(u, i), u)
# circuit
def name(s): return ''.join(str(i + 1) for i in range(K) if s >> i & 1) or 'e'
def setname(m): return '{' + ','.join(name(t) for t in range(N) if m >> t & 1) + '}'
used = set()
gates = []          # (name, a, u, b, v)
wires = {}          # name -> vector
for x in range(N):
    e = [0] * N; e[x] = 1; wires['x%d' % x] = e
def fname(m): return 'x%d' % (m.bit_length() - 1) if m & (m - 1) == 0 else 'f%d' % m
needed = set()
steps = []
for u in order:
    p = par[u]
    lst = R[(u, p)] if u > p else [(m, -c) for m, c in R[(p, u)]]
    steps.append((u, p, lst))
    for m, c in lst:
        # mark m and everything below it as needed
        stack = [m]
        while stack:
            q = stack.pop()
            if q & (q - 1) and q not in needed:
                needed.add(q); stack.extend(child[q])
for m in sorted(needed, key=lambda m: bin(m).count('1')):
    l, r = child[m]
    gates.append((fname(m), 1, fname(l), 1, fname(r)))
    wires[fname(m)] = [a + b for a, b in zip(wires[fname(l)], wires[fname(r)])]
ng_tree = len(gates)
deg0 = 0
for u, p, lst in steps:
    if p == N:
        deg0 += 1
        (m0, c0), rest = lst[0], lst[1:]
        cur = (c0, fname(m0)); vec = [c0 * a for a in wires[fname(m0)]]
        if not rest:
            wires['y%d' % u] = vec; gates.append(('y%d' % u, c0, fname(m0), None, None)); continue
    else:
        cur = (1, 'y%d' % p); vec = wires['y%d' % p][:]; rest = lst
    for i, (m, c) in enumerate(rest):
        nm = 'y%d' % u if i == len(rest) - 1 else 'y%d_%d' % (u, i)
        gates.append((nm, cur[0], cur[1], c, fname(m)))
        vec = [a + c * b for a, b in zip(vec, wires[fname(m)])]
        wires[nm] = vec[:]; cur = (1, nm)
ok = all(wires['y%d' % s] == Z[s] for s in range(N))
real = [g for g in gates if g[3] is not None]
print('K', K, 'N', N, 'tau', tau, 'deg0', deg0, 'tree gates', ng_tree, 'step gates', len(real) - ng_tree, 'GATES (G)', len(real),
      'replay on all basis vectors:', 'PASS' if ok else 'FAIL')
print('Yates', N * K // 2, ' N-2+tau', N - 2 + tau)
hist = {}
for u, p, lst in steps: hist[len(lst)] = hist.get(len(lst), 0) + 1
print('steps by number of nodes:', sorted(hist.items()))
for u, p, lst in steps:
    print('  y[%s] = %s %s' % (name(u), '0' if p == N else 'y[%s]' % name(p), ' '.join(('+' if c > 0 else '-') + (str(abs(c)) if abs(c) != 1 else '') + setname(m) for m, c in lst)))
print('input tree nodes (internal), in subsets:')
for m in sorted(masks, key=lambda m: -bin(m).count('1')):
    print('  ', setname(m) if bin(m).count('1') <= 16 else '(%d inputs)' % bin(m).count('1'), '  USED' if any(m == mm for _, _, l in steps for mm, _ in l) else '')
if len(sys.argv) > 3:
    with open(sys.argv[3], 'w') as f:
        f.write('# subset sums at %d points, plain letter on one input tree; %d gates (G); replayed exactly: %s\n' % (N, len(real), 'PASS' if ok else 'FAIL'))
        for g in gates:
            if g[3] is None: f.write('%s = %d * %s\n' % (g[0], g[1], g[2]))
            else: f.write('%s = %d * %s + %d * %s\n' % g)
