#!/usr/bin/env python3
"""h-3-orecord / orec.py.  Count (O): every line  t = u + v | t = u - v | t = c * u  is ONE operation.
Builds explicit (O) programs for the Walsh-Hadamard transform on N = 2^k points from windows of address bits:
  window of 3 bits = g-1's 19-gate circuit with its centre halved once (20 operations, output H_8 x / 2),
  window of 1 bit  = a butterfly (2 operations).
Writes them to o_<N>.txt (scaled output) and ox_<N>.txt (exact H x: one more multiplication per output),
then REPLAYS each file from disk with a parser that shares nothing with the builder: exact integers, all N unit
vectors at once, every halving checked to be exact, output j compared with row j of H in Sylvester order.
Also re-reads e2-0's oslp_<N>.txt with the same parser."""
import sys, re, os
from fractions import Fraction
HERE = os.path.dirname(os.path.abspath(__file__))

U3 = """g1 = x0 + x7
g2 = x1 + x6
g3 = x2 - x5
g4 = x3 - x4
g5 = g1 - g2
g6 = g3 + g4
g7 = g5 - g6
h = 1/2 * g7
a8 = h - x7
a9 = h - x5
a10 = a8 + x6
a11 = a9 - x4
y7 = a10 + g4
y3 = a9 + x3
y5 = g5 - y3
y1 = a10 + g3
y6 = a11 + g2
y2 = a8 + x1
y4 = y2 + g6
y0 = g1 - a11"""
U1 = """y0 = x0 + x1
y1 = x0 - x1"""
UNIT = {3: U3, 1: U1}

def build(k, plan):
    """plan: list of tuples of bit positions.  Returns list of lines; outputs are named out<j>."""
    N = 1 << k; cur = ['x%d' % i for i in range(N)]; lines = []; ctr = [0]
    for W in plan:
        w = len(W); mask = sum(1 << b for b in W)
        def addr(base, t): return base | sum(((t >> i) & 1) << W[i] for i in range(w))
        for base in range(N):
            if base & mask: continue
            ctr[0] += 1; tag = 'u%d_' % ctr[0]; ren = {}
            for t in range(1 << w): ren['x%d' % t] = cur[addr(base, t)]
            new = {}
            for ln in UNIT[w].split('\n'):
                t, rhs = ln.split(' = ')
                toks = rhs.split(' ')
                nm = tag + t; ren[t] = nm
                toks = [ren.get(z, z) for z in toks]
                lines.append(nm + ' = ' + ' '.join(toks))
                if t[0] == 'y': new[int(t[1:])] = nm
            for j in range(1 << w): cur[addr(base, j)] = new[j]
    return lines, cur

def replay(path):
    """independent: parse file, run on scaled unit vectors with exact integers."""
    txt = [l.strip() for l in open(path) if l.strip() and l[0] != '#']
    names = set(); ops = {'+': 0, '-': 0, '*': 0}; halv = 0
    prog = []
    for l in txt:
        m = re.fullmatch(r'(\w+) = (\S+) ([+\-*]) (\S+)', l); assert m, l
        prog.append(m.groups())
    xs = sorted({z for (_, a, op, b) in prog for z in (a, b) if re.fullmatch(r'x\d+', z)}, key=lambda s: int(s[1:]))
    N = len(xs); assert xs == ['x%d' % i for i in range(N)]
    den = 1
    for (_, a, op, b) in prog:
        if op == '*': den *= Fraction(a).denominator
    S = den            # crude but safe common scale: every multiplication stays in the integers
    val = {'x%d' % i: [S if i == j else 0 for j in range(N)] for i in range(N)}
    for (t, a, op, b) in prog:
        assert t not in val, 'name reused ' + t
        if op == '*':
            c = Fraction(a); v = []
            for z in val[b]:
                q = z * c; assert q.denominator == 1; v.append(int(q))
            val[t] = v
        elif op == '+': val[t] = [p + q for p, q in zip(val[a], val[b])]
        else: val[t] = [p - q for p, q in zip(val[a], val[b])]
        ops[op] += 1
    return N, S, val, ops

def check_rows(N, S, val, outnames):
    """outnames[j] must be c * row j of H for one common c; returns c."""
    c = Fraction(val[outnames[0]][0], S)
    for j in range(N):
        v = val[outnames[j]]
        for x in range(N):
            want = c * S * (-1) ** bin(j & x).count('1')
            if v[x] != want: return None
    return c

def check_set(N, S, val, prefix='y'):
    outs = sorted(tuple(v) for t, v in val.items() if t.startswith(prefix))
    for d in (1, 2, 4, 8, 16, 32, 64):
        if S % d: continue
        rows = sorted(tuple((S // d) * (-1) ** bin(w & x).count('1') for x in range(N)) for w in range(N))
        if outs == rows: return Fraction(1, d)
    return None

if __name__ == '__main__':
    print('count (O): one operation per line (addition, subtraction, or multiplication by a constant)')
    print('k  N    plan            ops(scaled)  scale   textbook  ops(exact Hx)  per point per bit  bits/op   replay')
    for k in range(1, 10):
        N = 1 << k; a, b = divmod(k, 3)
        plan = [tuple(range(3 * i, 3 * i + 3)) for i in range(a)] + [(3 * a + i,) for i in range(b)]
        lines, cur = build(k, plan)
        p = os.path.join(HERE, 'o_%d.txt' % N)
        with open(p, 'w') as f:
            f.write('# count (O) program, %d operations, %d points; outputs out_j named in the last comment line\n' % (len(lines), N))
            f.write('\n'.join(lines) + '\n'); f.write('# OUT ' + ' '.join(cur) + '\n')
        outn = open(p).read().strip().split('\n')[-1].split()[2:]
        Nn, S, val, ops = replay(p); assert Nn == N
        c = check_rows(N, S, val, outn); ok1 = c is not None
        # exact version
        ex = list(lines); fin = []
        if a > 0:
            for j in range(N):
                ex.append('z%d = %d * %s' % (j, 2 ** a, cur[j])); fin.append('z%d' % j)
        else: fin = cur
        px = os.path.join(HERE, 'ox_%d.txt' % N)
        with open(px, 'w') as f:
            f.write('# count (O) program, %d operations, %d points, exact H x\n' % (len(ex), N)); f.write('\n'.join(ex) + '\n'); f.write('# OUT ' + ' '.join(fin) + '\n')
        outx = open(px).read().strip().split('\n')[-1].split()[2:]
        N2, S2, val2, ops2 = replay(px); c2 = check_rows(N, S2, val2, outx); ok2 = (c2 == 1)
        tb = N * k
        print('%d  %-4d %-15s %-12d %-7s %-9d %-14d %-18.4f %-8.4f %s' % (k, N, '3' * a + '1' * b, len(lines), str(c), tb, len(ex),
              len(lines) / (N * k), tb / len(lines), ('scaled OK ' if ok1 else 'scaled FAIL ') + ('exact OK' if ok2 else 'exact FAIL')), ops, flush=True)
    print()
    print("e2-0's programs, re-read with this parser (outputs = names starting with y, compared as a set):")
    E = os.path.join(HERE, '..', 'e2-0-pieces')
    for N in (4, 16, 64):
        Nn, S, val, ops = replay(os.path.join(E, 'oslp_%d.txt' % N))
        c = check_set(Nn, S, val)
        print('oslp_%d.txt  N %d  operations %d %s  outputs = rows of H times %s   textbook %d' % (N, Nn, sum(ops.values()), ops, c, N * (N.bit_length() - 1)))
