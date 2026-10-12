# r-0: independent check of "h-1's second 52-gate circuit is two letters".  Pure Python, exact fractions.  Count (G).
# Own parser, own replay, own search, and a certificate that does NOT trust the search: from an assignment it builds
# each letter as an explicit matrix  diag(row scale) x [sum of (row set) x (column set) x number] x diag(column scale),
# checks that row sets and column sets are nested-or-disjoint families, and that the product of the letters is H.
import sys, re
from fractions import Fraction as F
sys.setrecursionlimit(20000)
I = 'waves/wave-05'

def parse(path):
    gates = []
    term = re.compile(r'([+-]?)\s*(\d+(?:/\d+)?)?\s*\*?\s*([A-Za-z_]\w*)')
    for line in open(path):
        line = line.split('#')[0].strip()
        if '=' not in line: continue
        name, rhs = [t.strip() for t in line.split('=')]
        rhs = rhs.replace('+ -', '- ').replace('+-', '-')
        ts = term.findall(rhs)
        assert len(ts) == 2, line
        out = []
        for sg, co, w in ts:
            c = F(co) if co else F(1)
            out.append((-c if sg == '-' else c, w))
        gates.append((name, out[0][0], out[0][1], out[1][0], out[1][1]))
    return gates

def replay(N, gates):
    vec = {'x%d' % i: [F(int(i == j)) for j in range(N)] for i in range(N)}
    for (n, a, u, b, v) in gates:
        assert n not in vec, n
        vec[n] = [a * p + b * q for p, q in zip(vec[u], vec[v])]
    rows = {tuple(F((-1) ** bin(y & x).count('1')) for x in range(N)): y for y in range(N)}
    outs = {}
    for n in ['x%d' % i for i in range(N)] + [g[0] for g in gates]:
        t = tuple(vec[n])
        if t in rows: outs.setdefault(rows[t], n)
    return vec, outs

def assign(N, gates, Lmax, limit=3000000):
    let = {'x%d' % i: 0 for i in range(N)}; role = {'x%d' % i: 'in' for i in range(N)}; supp = {}
    fam = {l: [] for l in range(1, Lmax + 1)}; nodes = [0]; aborted = [False]
    def lam(l, S):
        for T in fam[l]:
            if T == S: return False
            J = T & S
            if J and J != T and J != S: return False
        return True
    def rec(i):
        nodes[0] += 1
        if nodes[0] > limit: aborted[0] = True; return False
        if i == len(gates): return True
        n, a, u, b, v = gates[i]
        for l in range(max(let[u], let[v], 1), Lmax + 1):
            parts = []; good = (u != v)
            for o in (u, v):
                if let[o] < l: parts.append(frozenset([o]))
                elif role[o] == 'up': parts.append(supp[o])
                else: good = False
            if good and not (parts[0] & parts[1]):
                S = parts[0] | parts[1]
                if lam(l, S):
                    let[n] = l; role[n] = 'up'; supp[n] = S; fam[l].append(S)
                    if rec(i + 1): return True
                    fam[l].pop(); del supp[n]; del let[n]; del role[n]
                    if aborted[0]: return False
            if sum(1 for o in (u, v) if let[o] == l and role[o] == 'down') <= 1 and u != v:
                let[n] = l; role[n] = 'down'
                if rec(i + 1): return True
                del let[n]; del role[n]
                if aborted[0]: return False
        return False
    ok = rec(0)
    return ok, nodes[0], aborted[0], ((dict(let), dict(role)) if ok else None)

def rank(M):
    M = [list(r) for r in M]; rk = 0
    for c in range(len(M[0]) if M else 0):
        p = next((r for r in range(rk, len(M)) if M[r][c] != 0), None)
        if p is None: continue
        M[rk], M[p] = M[p], M[rk]
        for r in range(rk + 1, len(M)):
            if M[r][c] != 0:
                f = M[r][c] / M[rk][c]; M[r] = [x - f * y for x, y in zip(M[r], M[rk])]
        rk += 1
    return rk

def certificate(N, gates, let, role, vec, outs, verbose=True):
    L = max(let.values()); order = [g[0] for g in gates]; G = {g[0]: g for g in gates}
    usedby = {}
    for (n, a, u, b, v) in gates:
        for o in (u, v): usedby.setdefault(o, set()).add(let[n])
    xs = ['x%d' % i for i in range(N)]; final = [outs[y] for y in range(N)]
    W = [xs]
    for l in range(1, L):
        W.append([w for w in xs + order if let[w] <= l and ((w in final) or any(t > l for t in usedby.get(w, ())))])
    W.append(final)
    mats = []; info = []
    for l in range(1, L + 1):
        inp = W[l - 1]; inpset = set(inp); out = W[l]
        coef = {}
        for n in order:
            if let[n] == l and role[n] == 'up':
                _, a, u, b, v = G[n]; cs = []
                for o in (u, v):
                    if let[o] == l: assert role[o] == 'up'; cs.append(coef[o])
                    else: assert o in inpset, (n, o); cs.append({o: F(1)})
                assert not (set(cs[0]) & set(cs[1])), n
                coef[n] = {**{k: a * x for k, x in cs[0].items()}, **{k: b * x for k, x in cs[1].items()}}
        sets = {n: frozenset(c) for n, c in coef.items()}; names = list(sets)
        for p in range(len(names)):
            for q in range(p):
                A_, B_ = sets[names[p]], sets[names[q]]; J = A_ & B_
                assert A_ != B_ and (not J or J == A_ or J == B_), ('columns not nested', names[p], names[q])
        c = {}
        for i in inp:
            cont = [n for n in names if i in sets[n]]
            c[i] = coef[max(cont, key=lambda n: len(sets[n]))][i] if cont else F(1)
        gamma = {}
        for n in names:
            rs = {coef[n][i] / c[i] for i in sets[n]}
            assert len(rs) == 1, ('form not proportional to the column scaling', n)
            gamma[n] = rs.pop()
        def form(o):
            if let[o] == l: assert role[o] == 'up', o; return sets[o], gamma[o]
            assert o in inpset, o; return frozenset([o]), 1 / c[o]
        A = {}; parent = {}; raw = []
        for n in order:
            if let[n] == l and role[n] == 'down':
                _, a, u, b, v = G[n]
                st = [o for o in (u, v) if let[o] == l and role[o] == 'down']
                assert len(st) <= 1 and u != v, n
                if st: A[n] = (a if u == st[0] else b) * A[st[0]]; parent[n] = st[0]
                else: A[n] = F(1); parent[n] = None
                for cf, o in ((a, u), (b, v)):
                    if st and o == st[0]: continue
                    S, g = form(o); raw.append((n, S, cf * g / A[n]))
        def anc(w):
            r = []
            while w is not None: r.append(w); w = parent[w]
            return r
        ancs = {w: set(anc(w)) for w in A}
        rects = []; dead = 0
        for (n, S, num) in raw:
            R = frozenset(d for d in out if d in A and n in ancs[d])
            if R: rects.append((R, S, num, 'gate ' + n))
            else: dead += 1
        npass = 0
        for w in out:
            if let[w] < l: rects.append((frozenset([w]), frozenset([w]), 1 / c[w], 'pass ' + w)); npass += 1
            elif role[w] == 'up': rects.append((frozenset([w]), sets[w], gamma[w], 'upform ' + w)); npass += 1
        rowsets = sorted(set(r[0] for r in rects), key=len)
        for p in range(len(rowsets)):
            for q in range(p):
                J = rowsets[p] & rowsets[q]
                assert not J or J == rowsets[p] or J == rowsets[q], 'rows not nested'
        colsets = sorted(set(r[1] for r in rects), key=len)
        for p in range(len(colsets)):
            for q in range(p):
                J = colsets[p] & colsets[q]
                assert not J or J == colsets[p] or J == colsets[q], 'columns not nested'
        r = {w: (A[w] if w in A else F(1)) for w in out}
        S_ = {w: {i: F(0) for i in inp} for w in out}
        for (R, S, num, _) in rects:
            for w in R:
                for i in S: S_[w][i] += num
        M = [[r[w] * S_[w][i] * c[i] for i in inp] for w in out]
        # exact check against the replayed wires
        for wi, w in enumerate(out):
            got = [sum(M[wi][k] * vec[inp[k]][x] for k in range(len(inp))) for x in range(N)]
            assert got == vec[w], ('letter matrix disagrees with the replay', l, w)
        ng = sum(1 for n in order if let[n] == l); nu = sum(1 for n in order if let[n] == l and role[n] == 'up')
        mats.append(M)
        info.append(dict(l=l, inp=inp, out=out, rects=rects, sets=sets, S=S_, c=c, r=r, A=A, parent=parent, gates=ng, up=nu, dead=dead, npass=npass, rowsets=rowsets, colsets=colsets))
        if verbose:
            print("   letter %d: %d gates (%d up, %d down); matrix %d x %d; rectangles %d (of them %d free pass-throughs/up forms leaving); dead %d; row family %d sets, column family %d sets; nested: yes; matches replay: yes"
                  % (l, ng, nu, ng - nu, len(out), len(inp), len(rects), npass, dead, len(rowsets), len(colsets)))
    P = mats[0]
    for M in mats[1:]:
        P = [[sum(M[i][k] * P[k][j] for k in range(len(P))) for j in range(N)] for i in range(len(M))]
    H = [[F((-1) ** bin(y & x).count('1')) for x in range(N)] for y in range(N)]
    assert P == H
    if verbose: print("   product of the %d letter matrices = H_%d exactly: yes" % (L, N))
    return info

def show(gates, let, role, info):
    for d in info:
        l = d['l']
        print("   --- letter %d ---" % l)
        print("   input wires (%d): %s" % (len(d['inp']), ' '.join(d['inp'])))
        print("   wires leaving (%d): %s" % (len(d['out']), ' '.join(d['out'])))
        for (n, a, u, b, v) in gates:
            if let[n] != l: continue
            extra = ''
            if role[n] == 'up': extra = 'set {%s}' % ','.join(sorted(d['sets'][n], key=lambda s: (len(s), s)))
            else: extra = 'stream: %s' % (d['parent'][n] or 'starts here')
            print("     %-4s = %s*%s + %s*%s   %-4s %s" % (n, a, u, b, v, role[n], extra))

def cells(N, info):
    d1, d2 = info
    mid = d1['out']; assert mid == d2['inp']
    xs = d1['inp']; ys = d2['out']
    H = {(y, x): F((-1) ** bin(yi & xi).count('1')) for yi, y in enumerate(ys) for xi, x in enumerate(xs)}
    Cs = [c_ for c_ in d2['rowsets'] if len(c_) > 1] + [frozenset(ys)]
    Bs = [b_ for b_ in d1['colsets'] if len(b_) > 1] + [frozenset(xs)]
    Cs = list(dict.fromkeys(Cs)); Bs = list(dict.fromkeys(Bs))
    actC = {C: set(j for j in mid if len(set(d2['S'][y][j] for y in C)) > 1) for C in Cs}
    actB = {B: set(j for j in mid if len(set(d1['S'][j][x] for x in B)) > 1) for B in Bs}
    bad = 0; table = {}
    for C in Cs:
        for B in Bs:
            rk = rank([[H[(y, x)] for x in sorted(B)] for y in sorted(C)])
            cell = actC[C] & actB[B]
            if rk > 2 + len(cell): bad += 1
            table.setdefault((len(C), len(B), rk), []).append(len(cell))
    print("   output nodes with more than one output: %d (sizes %s); input nodes with more than one input: %d (sizes %s)"
          % (len(Cs), sorted(len(c_) for c_ in Cs), len(Bs), sorted(len(b_) for b_ in Bs)))
    print("   p-7's Lemma 1 (rank of the block <= 2 + wires in the cell): violated on %d of %d pairs" % (bad, len(Cs) * len(Bs)))
    for k in sorted(table):
        v = table[k]
        print("     |C|=%2d |B|=%2d rank %d : %3d blocks, wires in the cell: %s" % (k[0], k[1], k[2], len(v), ' '.join('%dx%d' % (v.count(t), t) for t in sorted(set(v)))))
    return Cs, Bs, actC, actB

def run(label, N, gates, Lmax_try=(1, 2, 3, 4), limit=3000000, detail=False):
    vec, outs = replay(N, gates)
    print("%s: %d points, %d gates (G); exact replay, every row of the transform is a wire: %s" % (label, N, len(gates), len(outs) == N))
    if len(outs) != N: return None
    for Lm in Lmax_try:
        ok, nodes, ab, res = assign(N, gates, Lm, limit)
        if ok:
            print("   %d letter(s): assignment found (%d nodes)" % (Lm, nodes))
            let, role = res
            info = certificate(N, gates, let, role, vec, outs)
            if detail: show(gates, let, role, info)
            return Lm, let, role, info
        print("   %d letter(s): none; %s (%d nodes)" % (Lm, "stopped at the node limit, NOT a proof" if ab else "search exhaustive", nodes))
    return None

if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'main'
    g52b = parse(I + '/h-1-staircase3/slp16_52_from54.txt')
    if what == 'main':
        res = run("h-1 second 52", 16, g52b, detail=True)
        if res and res[0] == 2:
            print("   cells of the two-letter factorisation (p-7 section 4):")
            cells(16, res[3])
        print()
        run("g-1 19", 8, parse(I + '/g-1-tightwires/h8_19gates.txt'))
        run("e2-0 slp_8", 8, parse(I + '/e2-0-pieces/slp_8.txt'))
        run("h-8 three-hub 21", 8, parse(I + '/h-8-provethewrongthi/h8_21_three_hubs.txt'))
    if what == 'push':
        # 32 points from the second 52: (a) pairs first, then the 52 on the sums and on the differences; (b) the 52 on each half, pairs last
        ga = []
        for j in range(16): ga += [('s%d' % j, F(1), 'x%d' % (2 * j), F(1), 'x%d' % (2 * j + 1)), ('d%d' % j, F(1), 'x%d' % (2 * j), F(-1), 'x%d' % (2 * j + 1))]
        for fam in 'sd':
            ren = lambda t: (fam + t[1:]) if t.startswith('x') else (fam.upper() + t)
            ga += [(ren(n), a, ren(u), b, ren(v)) for (n, a, u, b, v) in g52b]
        run("pairs first, then the second 52 twice", 32, ga, Lmax_try=(2, 3), limit=int(sys.argv[2]) if len(sys.argv) > 2 else 1500000)
        gb = []
        vec, outs = replay(16, g52b)
        for h, pre in ((0, 'A'), (1, 'B')):
            ren = lambda t: ('x%d' % (int(t[1:]) + 16 * h)) if t.startswith('x') else (pre + t)
            gb += [(ren(n), a, ren(u), b, ren(v)) for (n, a, u, b, v) in g52b]
        for y in range(16):
            gb += [('P%d' % y, F(1), 'A' + outs[y], F(1), 'B' + outs[y]), ('Q%d' % y, F(1), 'A' + outs[y], F(-1), 'B' + outs[y])]
        run("the second 52 on each half, pairs last", 32, gb, Lmax_try=(2, 3), limit=int(sys.argv[2]) if len(sys.argv) > 2 else 1500000)
        for nm in ('slp_16', 'slp_32'):
            run("e2-0 " + nm, int(nm[4:]), parse(I + '/e2-0-pieces/%s.txt' % nm), Lmax_try=(2, 3, 4), limit=int(sys.argv[2]) if len(sys.argv) > 2 else 1500000)
