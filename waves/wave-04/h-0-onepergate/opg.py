#!/usr/bin/env python3
"""h-0 onepergate / opg.py : the exchange-rate meter.  Count (G): a gate is any a*u + b*v, scalings free.  Exact Fractions.
For a circuit file: every gate wire's s (non-zeros in the inputs), s' (non-zeros in the outputs), entangled address bits,
fan-out, and the ledger  Q = gates + (over-limit gate wires) - N log2 N   (law L1 says Q >= 0).
Also the TRANSPOSED circuit (reverse every gate; same gate count) with every association order of its multi-term sums.
usage: opg.py meter <file> [verbose] | opg.py transpose <file>
"""
import sys, re, itertools
from fractions import Fraction as F
def wht(v):
    v = list(v); n = len(v); h = 1
    while h < n:
        for i in range(0, n, 2 * h):
            for j in range(i, i + h):
                a, b = v[j], v[j + h]; v[j], v[j + h] = a + b, a - b
        h *= 2
    return v
def nz(v): return sum(1 for z in v if z != 0)
def ent_bits(v, k):
    n = len(v); out = []
    for b in range(k):
        idx = [i for i in range(n) if not (i >> b) & 1]
        lo = [v[i] for i in idx]; hi = [v[i | (1 << b)] for i in idx]
        piv = next(j for j in range(len(lo)) if lo[j] != 0 or hi[j] != 0)
        if any(lo[piv] * hi[j] - hi[piv] * lo[j] != 0 for j in range(len(lo))): out.append(b)
    return out
def parse(path):
    """-> N, gates [(name, [(coef, src), (coef, src)])], alias {name: (coef, src)}"""
    gates = []; alias = {}; names = set()
    for line in open(path):
        line = line.split('#')[0].strip()
        if not line or '=' not in line or line.startswith(('output', 'N =')): continue
        parts = line.split('=')
        name = parts[0].strip(); rhs = parts[1].replace(' ', '')
        terms = re.findall(r'([+-]?)(?:\(?(-?\d+(?:/\d+)?)\)?\*)?([A-Za-z]\w*)', rhs)
        tt = []
        for sg, c, src in terms:
            c = F(c) if c else F(1)
            if sg == '-': c = -c
            tt.append((c, src))
        if len(tt) == 1: alias[name] = tt[0]
        else:
            assert len(tt) == 2, line
            gates.append((name, tt))
    return gates, alias
def evaluate(gates, alias, N):
    val = {}
    for p in 'xnw':
        for i in range(N): val['%s%d' % (p, i)] = tuple(F(int(i == j)) for j in range(N))
    for name, tt in gates:
        (a, u), (b, v) = tt
        u = alias.get(u, (1, u)); v = alias.get(v, (1, v))
        val[name] = tuple(a * u[0] * p + b * v[0] * q for p, q in zip(val[u[1]], val[v[1]]))
    return val
def rowid(v, N):
    """index j and scale c with v = c * (row j of H), else None"""
    piv = v[0]
    if piv == 0: return None
    for j in range(N):
        if all(v[x] == piv * (-1) ** bin(j & x).count('1') for x in range(N)): return j, piv
    return None
def describe(vecs, N, label):
    """vecs: list of (name, vector, [readers]) for gate wires, in order"""
    k = N.bit_length() - 1; T = V = 0; rows = []
    for name, v, rd in vecs:
        s = nz(v); s2 = nz(wht(v)); over = s * s2 != N
        if over: V += 1
        else: T += 1
        rows.append((name, s, s2, F(s * s2, N), ent_bits(v, k), rd, over, v))
    G = len(vecs); Q = G + V - N * k
    print('%s: N=%d gates=%d | tight gate wires T=%d, over-limit V=%d | saved=%d | Q = gates + V - N log2 N = %d  (L1: Q >= 0)%s'
          % (label, N, G, T, V, N * k - G, Q, '   <<<<< BREAKS L1' if Q < 0 else ''))
    return rows, Q
def meter(path, verbose=True):
    N = 8
    gates, alias = parse(path)
    if any(re.fullmatch(r'[xnw](\d+)', s) and int(s[1:]) >= 8 for _, tt in gates for _, s in tt) and len(gates) > 30: N = 16
    val = evaluate(gates, alias, N)
    readers = {}
    for name, tt in gates:
        for _, s in tt:
            s = alias.get(s, (1, s))[1]; readers.setdefault(s, []).append(name)
    outs = {}
    for name, _ in gates:
        r = rowid(val[name], N)
        if r and r[0] not in outs: outs[r[0]] = name
    assert len(outs) == N, 'outputs missing: %s' % sorted(outs)
    vecs = [(name, val[name], readers.get(name, [])) for name, _ in gates]
    rows, Q = describe(vecs, N, path.split('/')[-1])
    if verbose:
        for name, s, s2, r, eb, rd, over, v in rows:
            if over:
                kinds = []
                for g in rd:
                    vv = val[g]; kinds.append('%s(%d,%d)%s' % (g, nz(vv), nz(wht(vv)), '=OUT' if rowid(vv, N) else ''))
                print('   over-limit %-6s s=%d s\'=%d s*s\'/N=%s entangled bits %s read by %d: %s   %s' % (name, s, s2, r, eb, len(rd), ' '.join(kinds), [int(z) if z.denominator == 1 else str(z) for z in v]))
    return gates, alias, val, outs, N, Q
def trees(items):
    """all ways to add up a list of terms with two-input gates: yields nested tuples"""
    if len(items) == 1: yield items[0]; return
    first = items[0]; rest = items[1:]
    for r in range(len(rest) + 1):
        for comb in itertools.combinations(range(len(rest)), r):
            left = [first] + [rest[i] for i in comb]; right = [rest[i] for i in range(len(rest)) if i not in comb]
            if not right: continue
            for a in trees(left):
                for b in trees(right): yield (a, b)
def transpose(path):
    gates, alias, val, outs, N, Q0 = meter(path, verbose=False)
    k = N.bit_length() - 1
    # adjoint of node n = sum over readers g of coef(g, n) * adj(g)  +  (z_j if n is output j, scaled so that the map is H)
    incoming = {}   # node -> list of (coef, reader gate)
    for name, tt in gates:
        for c, s in tt:
            a = alias.get(s, (1, s)); incoming.setdefault(a[1], []).append((c * a[0], name))
    outname = {nm: j for j, nm in outs.items()}
    order = [name for name, _ in gates][::-1] + ['%s%d' % (p, i) for p in 'xnw' for i in range(N)]
    adj = {}; choice_nodes = []; base_terms = {}
    def unit(j, c): return tuple(F(c) if i == j else F(0) for i in range(N))
    # first pass with no intermediate wires: adjoint vectors do not depend on the association order
    for n in order:
        terms = []
        if n in outname:
            j = outname[n]; c = rowid(val[n], N)[1]; terms.append(unit(j, 1 / c))
        for c, g in incoming.get(n, []):
            terms.append(tuple(c * z for z in adj[g]))
        if not terms: continue
        adj[n] = tuple(sum(col) for col in zip(*terms)); base_terms[n] = terms
        if len(terms) >= 3: choice_nodes.append(n)
    # check: adjoints of the inputs are the rows of H
    pref = next(p for p in 'xnw' if ('%s0' % p) in adj)
    assert all(rowid(adj['%s%d' % (pref, i)], N) for i in range(N)), 'transposed circuit does not compute H'
    fixed = []   # gate wires that do not depend on choices: every node with >= 2 terms contributes its total
    for n in order:
        if n in base_terms and len(base_terms[n]) >= 2: fixed.append(('t(' + n + ')', adj[n]))
    def partials(tree, acc):
        if isinstance(tree[0], F): return tree     # a leaf vector
        a = partials(tree[0], acc); b = partials(tree[1], acc)
        v = tuple(p + q for p, q in zip(a, b)); acc.append(v); return v
    opts = []
    for n in choice_nodes:
        o = []
        for tr in trees(base_terms[n]):
            acc = []; partials(tr, acc); o.append(acc[:-1])       # the last one is the node's total (already in fixed)
        opts.append(o)
    ncomb = 1
    for o in opts: ncomb *= len(o)
    print('   transposed: %d gates (fixed wires %d, nodes with 3 or more terms: %s, association orders %d)' % (sum(len(t) - 1 for t in base_terms.values()), len(fixed), [(n, len(base_terms[n])) for n in choice_nodes], ncomb))
    def over(v): return nz(v) * nz(wht(v)) != N
    Vfix = sum(1 for _, v in fixed if over(v))
    # the best choice is independent per node: minimise over-limit partial sums node by node
    bestV = Vfix; extra = []
    for n, o in zip(choice_nodes, opts):
        b = min(o, key=lambda acc: sum(1 for v in acc if over(v))); bestV += sum(1 for v in b if over(v)); extra += [('t(%s)part' % n, v) for v in b]
    vecs = [(nm, v, []) for nm, v in fixed + extra]
    rows, Q = describe(vecs, N, '   TRANSPOSE of ' + path.split('/')[-1])
    for name, s, s2, r, eb, rd, ov, v in rows:
        if ov: print('      over-limit %-12s s=%d s\'=%d s*s\'/N=%s entangled bits %s  %s' % (name, s, s2, r, eb, [int(z) if z.denominator == 1 else str(z) for z in v]))
    return Q
if __name__ == '__main__':
    if sys.argv[1] == 'meter': meter(sys.argv[2])
    else: transpose(sys.argv[2])
