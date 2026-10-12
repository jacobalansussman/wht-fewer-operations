#!/usr/bin/env python3
"""u-4-zdz / zdz.py : the transform as (subset sums) x (free scalings) x (subset sums), H = Z D Z^T, written as a gate list,
replayed exactly on all basis vectors, and read with the meter modulo 2 (m-cross's definitions) and h-0's meter.
Count (G): a gate is any a*u + b*v, scalings free.  Whole numbers only (no division anywhere in these circuits).

usage: zdz.py <orders file or 'yates:K' or 'gray:K' or 'weight:K'> [assoc=seq|run] [p2=same|transpose] [write=<file>] [cap=<m>] [verbose]
  orders file : an output file of q-cross/cat3.py (BEST block: rows = order of the outputs, cols = order of the inputs)
  pass 1 : v = Z^T x, by the Z circuit with every address complemented;  then v_J scaled by (-2)^|J| (inside the gate coefficients);
  pass 2 : y = Z (scaled v).   p2=transpose uses the TRANSPOSED picture for pass 2 (rows' = complement of cols, cols' = complement
  of rows): same number of corners, other running sums.
"""
import sys, ast

def pop(x): return bin(x).count('1')

def load(spec):
    if spec.startswith('yates:'): return None, None, int(spec.split(':')[1])
    txt = open(spec).read().split('BEST')[-1]
    rows = ast.literal_eval(txt.split('rows ')[1].split(' r ')[0]); cols = ast.literal_eval(txt.split('cols ')[1].split(' c ')[0])
    return rows, cols, len(rows).bit_length() - 1

def secdiff(rows, cols):
    N = len(rows)
    A = [[1 if (rows[a] & cols[b]) == cols[b] else 0 for b in range(N)] + [0] for a in range(N)] + [[0] * (N + 1)]
    return [[A[a][b] - A[a + 1][b] - A[a][b + 1] + A[a + 1][b + 1] for b in range(N)] for a in range(N)]

def fold(terms, gates, names):
    """terms: list of (coef, wire); left fold; the i-th partial result is named by names(i, last?)"""
    cur = terms[0]
    for i, t in enumerate(terms[1:]):
        nm = names(i, i == len(terms) - 2)
        gates.append((nm, cur[0], cur[1], t[0], t[1])); cur = (1, nm)
    return cur

def zcircuit(rows, cols, inp, pre, outname, assoc, tag):
    """two-chain program for subset sums in the orders (rows, cols).  inp[address] = (coef, wire).  -> out[address] = (coef, wire)"""
    N = len(rows); M = secdiff(rows, cols); gates = []
    F = [inp[cols[0]]]
    for b in range(1, N):
        nm = '%sf%d' % (pre, b); c = inp[cols[b]]
        gates.append((nm, F[-1][0], F[-1][1], c[0], c[1], tag + 'F')); F.append((1, nm))
    out = {}; y = None
    for a in range(N - 1, -1, -1):
        terms = [(M[a][b] * F[b][0], F[b][1]) for b in range(N) if M[a][b]]
        g = []
        nmf = lambda i, last, a=a: (outname(rows[a]) if last else '%st%d_%d' % (pre, a, i))
        if y is None: y = fold(terms, g, nmf)
        elif assoc == 'seq': y = fold([y] + terms, g, nmf)
        else:
            r = fold(terms, g, lambda i, last, a=a: '%sr%d_%d' % (pre, a, i))
            y = fold([y, r], g, nmf)
        for i, t in enumerate(g): gates.append(t + (tag + ('Y' if i == len(g) - 1 else 'T'),))
        out[rows[a]] = y
    nz = sum(1 for a in range(N) for b in range(N) if M[a][b])
    return gates, out, nz

def yates(K, inp, pre, outname, up, tag):
    """up=True: v_J = sum of the inputs at T containing J (Z^T);  up=False: y_S = sum over J inside S (Z).  (N/2) K gates."""
    N = 1 << K; cur = dict(inp); gates = []
    for j in range(K):
        bit = 1 << j
        for s in range(N):
            if bool(s & bit) != up:
                o = s ^ bit; nm = (outname(s) if j == K - 1 else '%s%d_%d' % (pre, j, s))
                gates.append((nm, cur[s][0], cur[s][1], cur[o][0], cur[o][1], tag + 'Y')); cur[s] = (1, nm)
    return gates, cur

def build(spec, assoc='seq', p2='same'):
    rows, cols, K = load(spec); N = 1 << K; full = N - 1
    inp1 = {c: (1, 'x%d' % (c ^ full)) for c in range(N)}
    if rows is None:
        g1, v = yates(K, {s: (1, 'x%d' % s) for s in range(N)}, 'a', lambda s: 'v%d' % s, True, '1')
        inp2 = {J: ((-2) ** pop(J) * v[J][0], v[J][1]) for J in range(N)}
        g2, y = yates(K, inp2, 'b', lambda s: 'y%d' % s, False, '2')
        return N, g1 + g2, y, None
    g1, o1, nz1 = zcircuit(rows, cols, inp1, 'a', lambda r: 'v%d' % (r ^ full), assoc, '1')
    v = {J: o1[J ^ full] for J in range(N)}
    inp2 = {J: ((-2) ** pop(J) * v[J][0], v[J][1]) for J in range(N)}
    if p2 == 'transpose': r2 = [c ^ full for c in cols]; c2 = [r ^ full for r in rows]
    else: r2, c2 = rows, cols
    g2, y, nz2 = zcircuit(r2, c2, inp2, 'b', lambda r: 'y%d' % r, assoc, '2')
    return N, g1 + g2, y, (nz1, nz2)

# ---------- exact replay and the meters (whole numbers) ----------
def wht(v):
    v = list(v); n = len(v); h = 1
    while h < n:
        for i in range(0, n, 2 * h):
            for j in range(i, i + h):
                a, b = v[j], v[j + h]; v[j], v[j + h] = a + b, a - b
        h *= 2
    return v
def val2(n):
    if n == 0: return 10 ** 9
    return (n & -n).bit_length() - 1
def prim(w):
    m = min(val2(a) for a in w); return [a >> m for a in w], m
def canon(pw, m):
    Mo = 1 << m; r = [a % Mo for a in pw]; lead = next(a for a in r if a & 1); inv = pow(lead, -1, Mo)
    return tuple((a * inv) % Mo for a in r)

def meter(label, N, gates, y, cap=16, verbose=False):
    K = N.bit_length() - 1
    W = {'x%d' % i: [int(i == j) for j in range(N)] for i in range(N)}
    # exact replay
    for (nm, a, u, b, v, tag) in gates: W[nm] = [a * p + b * q for p, q in zip(W[u], W[v])]
    ok = all([y[s][0] * t for t in W[y[s][1]]] == [(-1) ** pop(s & x) for x in range(N)] for s in range(N))
    osets = [set() for _ in range(cap + 1)]; cls = {}; first = {}
    over = {}
    for i in range(N):
        nm = 'x%d' % i; pw, _ = prim(W[nm])
        for m in range(1, cap + 1): osets[m].add(canon(pw, m))
        c = canon(pw, 1); cls.setdefault(c, []).append(nm); over[nm] = False
    kinds = {}; surv = {}; dead = {}; hist = {}; V = 0; two_over = 0; qexp = {}; rec = []
    for (nm, a, u, b, v, tag) in gates:
        w = W[nm]; pw, mw = prim(w); pu, mu = prim(W[u]); pv, mv = prim(W[v])
        cu, cv, cw = canon(pu, 1), canon(pv, 1), canon(pw, 1)
        kd = 'E' if cu == cv == cw else 'Q' if cu == cv else 'S' if cw in (cu, cv) else 'J'
        p = tag[0]
        kinds[(p, kd)] = kinds.get((p, kd), 0) + 1
        o = 0
        for m in range(1, cap + 1):
            if canon(pw, m) in osets[m]: o = m
            else: break
        if o == 0: surv[p] = surv.get(p, 0) + 1
        else: dead[p] = dead.get(p, 0) + 1; hist[(p, o)] = hist.get((p, o), 0) + 1
        for m in range(1, cap + 1): osets[m].add(canon(pw, m))
        cls.setdefault(cw, []).append(nm)
        s = sum(1 for t in w if t); s2 = sum(1 for t in wht(w) if t)
        ov = s * s2 > N; over[nm] = ov
        if ov: V += 1
        if over[u] and over[v]: two_over += 1
        drop = mw - min(mu + val2(a), mv + val2(b))        # powers of 2 cancelled by the gate
        if kd in ('Q', 'E') or drop: qexp[(p, kd, drop)] = qexp.get((p, kd, drop), 0) + 1
        rec.append((nm, tag, kd, o, drop, s, s2, a, u, b, v))
    sets = []
    for c in cls: sets.append(sum(1 << i for i in range(N) if c[i]))
    ovl = 0
    for i in range(len(sets)):
        A = sets[i]
        for j in range(i):
            B = sets[j]; I = A & B
            if I and I != A and I != B: ovl += 1
    G = len(gates); nlogn = N * K
    print('== %s' % label)
    print('   N=%d  gates (G)=%d  [textbook N log2 N=%d, (3/4) N log2 N=%d]  exact replay as the transform on %d basis vectors: %s' % (N, G, nlogn, 3 * nlogn // 4, N, ok))
    print('   classes (inputs included)=%d  [2N-1=%d]   pairs of classes that overlap without nesting=%d of %d' % (len(cls), 2 * N - 1, ovl, len(sets) * (len(sets) - 1) // 2))
    for p in '12':
        print('   pass %s: gates=%d  J/S/Q/E=%d/%d/%d/%d  survivors=%d dead=%d  orders of dead gates=%s' % (p, sum(1 for g in gates if g[5][0] == p),
              kinds.get((p, 'J'), 0), kinds.get((p, 'S'), 0), kinds.get((p, 'Q'), 0), kinds.get((p, 'E'), 0), surv.get(p, 0), dead.get(p, 0),
              sorted((o, n) for (q, o), n in hist.items() if q == p)))
    ts = sum(surv.values()); td = sum(dead.values())
    print('   total: survivors=%d [one tree: N-1=%d]  dead=%d [(N/2) log2 N=%d; textbook N log2 N-N+1=%d]  dead-(N/2)log2N=%d' % (ts, N - 1, td, nlogn // 2, nlogn - N + 1, td - nlogn // 2))
    print('   highest order=%d  Q gates=%d  E gates=%d  gates that cancel powers of 2 (pass, kind, powers): %s' % (max([o for (_, o) in hist] or [0]),
              sum(n for (p, kd), n in kinds.items() if kd == 'Q'), sum(n for (p, kd), n in kinds.items() if kd == 'E'), sorted(qexp.items())))
    print('   over-limit gate wires V=%d of %d   h-0 sum: gates+V-N log2 N=%d   gates reading two over-limit wires=%d' % (V, G, G + V - nlogn, two_over))
    if verbose:
        for r in rec: print('      %-8s %-3s kind=%s order=%d cancel=%d s=%d s\'=%d   = %d * %s + %d * %s' % r)
    return dict(N=N, G=G, ok=ok, classes=len(cls), ovl=ovl, surv=ts, dead=td, rec=rec, W=W, cls=cls)

if __name__ == '__main__':
    spec = sys.argv[1]; opt = dict(a.split('=') for a in sys.argv[2:] if '=' in a)
    N, gates, y, nz = build(spec, opt.get('assoc', 'seq'), opt.get('p2', 'same'))
    if 'write' in opt:
        with open(opt['write'], 'w') as f:
            f.write('# u-4-zdz: H = Z D Z^T, %s assoc=%s p2=%s; %d gates (G); outputs: %s\n' % (spec.split('/')[-1], opt.get('assoc', 'seq'), opt.get('p2', 'same'), len(gates),
                    ' '.join('H%d=%d*%s' % (s, y[s][0], y[s][1]) for s in range(N))))
            for (nm, a, u, b, v, tag) in gates: f.write('%s = %d * %s + %d * %s\n' % (nm, a, u, b, v))
    label = '%s assoc=%s p2=%s corners=%s' % (spec.split('/')[-1], opt.get('assoc', 'seq'), opt.get('p2', 'same'), nz)
    meter(label, N, gates, y, int(opt.get('cap', 16)), 'verbose' in sys.argv)
