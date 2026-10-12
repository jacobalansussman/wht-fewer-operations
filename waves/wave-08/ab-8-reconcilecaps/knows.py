#!/usr/bin/env python3
"""knows.py [ab-8-reconcilecaps]  EXACT whole-number counts.  The 'knows' graph on x-6's fat ports of class (h, r):
vertices = r-dimensional subspaces P of F_2^h that meet P-perp only in 0 (dot product x.y = parity of common ones);
P knows Q  <=>  Q inside P-perp  <=>  every word of P is orthogonal to every word of Q  (symmetric; then P, Q share only 0).
A set of ports no two of which know each other forces the scatter matrix to be the identity on it, so
     rank(M) >= that set,   kappa = v / rank(M) <= (size of the family) / (largest such subset).
Types (the orbits of the isometry group, [derived] in ab-8.md): 'alt' = every word of P even; 'one' = the all-ones word in P;
'gen' = neither.  Inside one type the graph is vertex-transitive, so kappa <= |type| / alpha(type) for EVERY sub-family of it,
and for mixed sub-families kappa <= sum over types of |type| / alpha(type).  Any explicit set gives a valid ceiling.
Explicit sets ('stars'): all ports containing a word of X, X a set of words any two of which overlap oddly."""
import sys, itertools, random, time
h, r = int(sys.argv[1]), int(sys.argv[2]); N = 1 << h; ALL = N - 1
PC = [bin(x).count('1') & 1 for x in range(N)]
dot = lambda a, b: PC[a & b]
def subspaces(h, r):
    for piv in itertools.combinations(range(h - 1, -1, -1), r):
        lists = []
        for p in piv:
            free = [b for b in range(p) if b not in piv]
            vals = []
            for mask in range(1 << len(free)):
                x = 1 << p
                for i, b in enumerate(free):
                    if mask >> i & 1: x |= 1 << b
                vals.append(x)
            lists.append(vals)
        yield from itertools.product(*lists)
def nondeg(B):
    rows = [sum(dot(a, b) << j for j, b in enumerate(B)) for a in B]
    rk = 0
    for c in range(len(B)):
        pv = next((i for i in range(rk, len(rows)) if rows[i] >> c & 1), None)
        if pv is None: return False
        rows[rk], rows[pv] = rows[pv], rows[rk]
        for i in range(len(rows)):
            if i != rk and rows[i] >> c & 1: rows[i] ^= rows[rk]
        rk += 1
    return True
def span(B):
    S = [0]
    for b in B: S += [s ^ b for s in S]
    return S
# star sets
u = 1; gens = [(1 << j) | (1 << (j + 1)) for j in range(1, h - 1, 2)]
Xodd = [u ^ s for s in span(gens)]
assert all(dot(a, b) == 1 for a in Xodd for b in Xodd)
Xev = [1 | (1 << j) for j in range(1, h)]
if h % 2 == 1: Xev.append(ALL ^ 1)
assert all(dot(a, b) == 1 for a in Xev for b in Xev if a != b)
inXodd = [0] * N; inXev = [0] * N
for x in Xodd: inXodd[x] = 1
for x in Xev: inXev[x] = 1
t0 = time.time(); tot = 0
cnt = {}; hit = {'odd': {}, 'ev': {}}; rep = {}; ports = []
keep = True
for B in subspaces(h, r):
    tot += 1
    if not nondeg(B): continue
    S = span(B)
    ty = 'alt' if not any(PC[b] for b in B) else ('one' if ALL in S else 'gen')
    cnt[ty] = cnt.get(ty, 0) + 1
    if any(inXodd[x] for x in S): hit['odd'][ty] = hit['odd'].get(ty, 0) + 1
    if any(inXev[x] for x in S): hit['ev'][ty] = hit['ev'].get(ty, 0) + 1
    rep.setdefault(ty, B)
    if keep:
        ports.append((B, ty))
        if len(ports) > 400000: keep = False; ports = None
print('class (%d,%d): %d subspaces of dimension %d, ports (meet their perpendicular only in 0): %d  by type %s   [%.0fs]' % (h, r, tot, r, sum(cnt.values()), dict(sorted(cnt.items())), time.time() - t0))
print('   star sets: X_odd = %d odd words pairwise overlapping oddly; X_even = %d even words pairwise overlapping oddly' % (len(Xodd), len(Xev)))
# degrees of one representative per type
if ports is not None:
    for ty, B in sorted(rep.items()):
        d = {}
        for C, t2 in ports:
            if all(dot(a, b) == 0 for a in B for b in C): d[t2] = d.get(t2, 0) + 1
        print('   a port of type %-3s knows: %s' % (ty, dict(sorted(d.items())) or 'nobody'))
ceil = {}
for ty in sorted(cnt):
    best = max(hit['odd'].get(ty, 0), hit['ev'].get(ty, 0))
    print('   type %-3s : %7d ports ; star X_odd holds %7d, star X_even holds %7d  ->  kappa <= %s' % (ty, cnt[ty], hit['odd'].get(ty, 0), hit['ev'].get(ty, 0), ('%.3f' % (cnt[ty] / best)) if best else 'no bound'))
    ceil[ty] = [cnt[ty], best]
# small graphs: adjacency, greedy and exact independent sets per type
def mis_exact(adj, verts, limit=3_000_000):
    best = [0]; nodes = [0]
    order = sorted(verts, key=lambda x: -bin(adj[x]).count('1'))
    def rec(cand, size):
        nodes[0] += 1
        if nodes[0] > limit: raise TimeoutError
        if size + bin(cand).count('1') <= best[0]: return
        if cand == 0:
            best[0] = size; return
        # pick vertex of max degree inside cand
        bx, bd = None, -1
        c = cand
        while c:
            x = (c & -c).bit_length() - 1; c &= c - 1
            d = bin(adj[x] & cand).count('1')
            if d > bd: bx, bd = x, d
        if bd == 0:
            best[0] = max(best[0], size + bin(cand).count('1')); return
        if bd == 1:                                     # matching edges and isolated: take one endpoint of each edge
            s = size; c = cand
            while c:
                x = (c & -c).bit_length() - 1; c &= c - 1; s += 1; c &= ~adj[x]
            best[0] = max(best[0], s); return
        rec(cand & ~adj[bx] & ~(1 << bx), size + 1)
        rec(cand & ~(1 << bx), size)
    try:
        rec(sum(1 << x for x in verts), 0); return best[0], True
    except TimeoutError:
        return best[0], False
def greedy(adj, verts, trials=300, seed=1):
    rnd = random.Random(seed); best = 0; vs = list(verts)
    for _ in range(trials):
        rnd.shuffle(vs); cand = sum(1 << x for x in vs); s = 0
        while cand:
            # min degree vertex among a random sample
            pick = None; pd = 1 << 30
            c = cand; seen = 0
            for x in vs:
                if cand >> x & 1:
                    d = bin(adj[x] & cand).count('1')
                    if d < pd: pick, pd = x, d
                    seen += 1
                    if seen >= 12 or d == 0: break
            s += 1; cand &= ~adj[pick] & ~(1 << pick)
        best = max(best, s)
    return best
if ports is not None and len(ports) <= 2500:
    n = len(ports); adj = [0] * n
    for i in range(n):
        Bi = ports[i][0]
        for j in range(i + 1, n):
            if all(dot(a, b) == 0 for a in Bi for b in ports[j][0]): adj[i] |= 1 << j; adj[j] |= 1 << i
    print('   knows graph built: %d ports, degrees %s' % (n, sorted(set(bin(a).count('1') for a in adj))))
    groups = {ty: [i for i in range(n) if ports[i][1] == ty] for ty in cnt}
    groups['ALL'] = list(range(n))
    for ty, vs in sorted(groups.items()):
        g = greedy(adj, vs, 200 if n <= 500 else 20)
        ex, done = mis_exact(adj, vs, 400000) if len(vs) <= 400 else (0, False)
        a = max(g, ex)
        print('   %-3s: %5d ports; largest set with no two knowing each other: %s (greedy %d)  ->  size/alpha = %.3f' % (ty, len(vs), ('%d EXACT' % ex) if done else ('>= %d (search not finished)' % a), g, len(vs) / a))
        if ty in ceil and a > ceil[ty][1]: ceil[ty][1] = a
    # cliques: largest set of ports that all know each other, by greedy (lower bound) -> kappa of the block scatter
tot_k = 0.0; ok = True
for ty, (c, a) in sorted(ceil.items()):
    if a == 0: ok = False
    else: tot_k += c / a
    print('TYPE %d %d %s %s' % (h, r, ty, ('%.4f' % (c / a)) if a else 'none'))
if ok: print('CEIL %d %d %.4f   (every sub-family, types mixed: sum of the per-type ceilings)' % (h, r, tot_k))
print('   [%.0fs]' % (time.time() - t0))
