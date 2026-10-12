# u-8-compose: build tensor compositions A x B from gate lists, replay exactly (Fractions), and meter them.
# count (G): one line = one gate a*u + b*v.  e = gates - (N-1) - (N/2) log2 N.
# class of a wire = primitive form modulo 2 (m-cross); survivors = gates with a new class.
import sys, re
from fractions import Fraction as F
ID = 'waves/wave-06/'
def coef(s):
    if s in ('', '+'): return F(1)
    if s == '-': return F(-1)
    return F(s)
def parse(path):
    gates = []
    for line in open(path, errors='replace'):
        line = line.split('#')[0].strip()
        if '=' not in line: continue
        name, rhs = line.split('=', 1); name = name.strip(); rhs = rhs.replace(' ', '')
        m = re.fullmatch(r'([+-]?[\d/]*)\*?([A-Za-z_]\w*)(\+-|\+|-)([\d/]*)\*?([A-Za-z_]\w*)', rhs)
        assert m, (path, line)
        a = coef(m.group(1)); b = coef(m.group(4)) * (-1 if '-' in m.group(3) else 1)
        gates.append((name, a, m.group(2), b, m.group(5)))
    return gates
def npts(g): return 1 + max(int(t[1:]) for (_, _, u, _, v) in g for t in (u, v) if re.fullmatch(r'x\d+', t))
def replay(g, N):
    W = {'x%d' % i: [F(int(i == j)) for j in range(N)] for i in range(N)}
    for (name, a, u, b, v) in g:
        assert name not in W, name
        W[name] = [a * p + b * q for p, q in zip(W[u], W[v])]
    return W
def outputs(g, N):
    """row index y -> (wire name, factor) with wire = factor * row y of H; exact."""
    W = replay(g, N); out = {}
    for (name, *_ ) in g:
        w = W[name]
        if any(t == 0 for t in w): continue
        for y in range(N):
            if all(w[x] == w[0] * (-1) ** bin(y & x).count('1') for x in range(N)): out[y] = (name, w[0])
    return out, W
def val2(q):
    n, d, v = q.numerator, q.denominator, 0
    while n % 2 == 0: n //= 2; v += 1
    while d % 2 == 0: d //= 2; v -= 1
    return v
def cls(w):
    m = min(val2(a) for a in w if a != 0)
    return tuple(int(((a / F(2) ** m).numerator) % 2) if a != 0 else 0 for a in w)
def meter(label, g):
    N = npts(g); k = N.bit_length() - 1
    out, W = outputs(g, N)
    ok = len(out) == N and all(f in (1, -1) for (_, f) in out.values())
    seen = {cls(W['x%d' % i]) for i in range(N)}; surv = 0; prof = {}
    for (name, *_ ) in g:
        c = cls(W[name]); s = sum(c)
        prof[s] = prof.get(s, 0) + 1
        if c not in seen: surv += 1; seen.add(c)
    cl = sorted(seen, key=sum); lam = all((not any(p and q for p, q in zip(a, b))) or all(p <= q for p, q in zip(a, b)) for i, a in enumerate(cl) for b in cl[i + 1:])
    G = len(g); e = G - (N - 1) - N * k // 2
    hubs = sum(1 for (name, *_ ) in g if all(t != 0 for t in W[name]) and name not in {v[0] for v in out.values()})
    print('%-34s N=%3d gates=%4d exact_H=%s survivors=%3d (N-1=%3d) dead=%4d e=%3d  classes=%d one_tree=%s  full non-outputs=%d  wires by support %s  rate=%.4f'
          % (label, N, G, ok, surv, N - 1, G - surv, e, len(seen), lam and len(seen) == 2 * N - 1, hubs, sorted(prof.items()), G / (N * k)))
    return e, G
def tensor(gA, gB):
    """A (m points) inside each of n blocks, then B across blocks on each of the m output coordinates. address = block*m + a."""
    m, n = npts(gA), npts(gB); oA, _ = outputs(gA, m); assert len(oA) == m
    g = []
    for j in range(n):
        ren = lambda t: 'x%d' % (j * m + int(t[1:])) if re.fullmatch(r'x\d+', t) else 'b%d_%s' % (j, t)
        for (name, a, u, b, v) in gA: g.append((ren(name), a, ren(u), b, ren(v)))
    for c in range(m):
        nm, f = oA[c]
        ren = lambda t: 'b%d_%s' % (int(t[1:]), nm) if re.fullmatch(r'x\d+', t) else 'c%d_%s' % (c, t)
        for (name, a, u, b, v) in gB: g.append((ren(name), a, ren(u), b, ren(v)))
    return g
def write(path, g, head):
    with open(path, 'w') as f:
        f.write('# ' + head + '\n')
        for (name, a, u, b, v) in g: f.write('%s = %s * %s + %s * %s\n' % (name, a, u, b, v))
if __name__ == '__main__':
    brick = parse(ID + 'h-6-classhub/brick_m1.txt'); n19 = parse(ID + 'g-1-tightwires/h8_19gates.txt')
    t2 = [('s', F(1), 'x0', F(1), 'x1'), ('d', F(1), 'x0', F(-1), 'x1')]
    E = {}
    for lab, g in (('textbook 2', t2), ('brick', brick), ('the 19', n19)): E[lab] = meter(lab, g)
    for N in (8, 16, 32, 64): E['staircase %d' % N] = meter('staircase %d' % N, parse(ID + 'e2-0-pieces/slp_%d.txt' % N))
    meter('second 52 (h-1)', parse(ID + 'h-1-staircase3/slp16_52_from54.txt'))
    meter('54 = 19 x textbook2 (h-0)', parse(ID + 'h-0-onepergate/h16_54gates_tensor.txt'))
    print('--- tensor products built here; law e(AxB) = n e(A) + m e(B) + (m-1)(n-1)')
    prods = [('t2 x t2', t2, t2), ('brick x t2', brick, t2), ('t2 x brick', t2, brick), ('brick x brick', brick, brick), ('19 x t2', n19, t2), ('t2 x 19', t2, n19),
             ('brick x 19', brick, n19), ('19 x brick', n19, brick), ('19 x 19', n19, n19)]
    base = {'t2': (2, 0), 'brick': (4, 0), '19': (8, 0)}
    for lab, A, B in prods:
        g = tensor(A, B); e, G = meter(lab, g)
        a, b = lab.split(' x '); (m, eA), (n, eB) = base[a], base[b]
        law = n * eA + m * eB + (m - 1) * (n - 1)
        print('      law predicts e = %d : %s' % (law, 'agrees' if law == e else 'DISAGREES'))
        write('tensor_%s_x_%s.txt' % (a, b), g, '%s : %d points, %d gates, count (G); A inside blocks then B across blocks' % (lab, npts(g), G))
    print('--- staircase as a composition: cross(m,n) = e(mn) - n e(m) - m e(n), against (3/4) m n - m - n + 1 and the tensor (m-1)(n-1)')
    es = {4: 0}
    for N in (8, 16, 32, 64): es[N] = E['staircase %d' % N][0]
    for N in (16, 32, 64):
        for m in (4, 8, 16):
            n = N // m
            if n in es and m in es and n >= 4:
                cr = es[N] - n * es[m] - m * es[n]
                print('   staircase %2d = %2d o %2d : cross = %3d   (3/4)mn-m-n+1 = %3d   tensor (m-1)(n-1) = %3d' % (N, m, n, cr, 3 * m * n // 4 - m - n + 1, (m - 1) * (n - 1)))
