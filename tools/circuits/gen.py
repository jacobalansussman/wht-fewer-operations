#!/usr/bin/env python3
"""gen.py -- generators for the Walsh-Hadamard programs.  Standard library only.
Written from the recursions (stated below), not from the search programs.
Format and counts: see slp.py.

WORDS.  A block is a run of m = 2^j consecutive inputs starting at a multiple
of m.  Its halves are L (first m/2 inputs) and R (the rest); its quarters are
L0, L1, R0, R1 in order.  The "piece" (block, a), a in 0..m-1, is the linear
form  sum over t < m of (-1)^(common 1-bits of a and t) * x_(start+t):
row a of the m-point transform, on that block.  A single input is a piece of
size 1.  The whole transform is the N pieces of the block of size N.

THE FAMILY (construction 1; count (G) cost (3/4) N k + N/4 for N = 2^k, k >= 2).
  Task E(block of size m, sign s): make the m/2 pieces (block, a) with
  a < m/2 if s = +, with a >= m/2 if s = -.
    m = 2:  one gate, x + s*x'.
    m >= 4: do E(L, +) and E(R, -).  For every d < m/4 these give
            A = (L, d) and B = (R, d + m/4).  With q(X) = (X, d) on a quarter X:
            A = q(L0) + q(L1),  B = q(R0) - q(R1).
            hub     M  = A + c*B                                     1 gate
            piece   P1 = (L,d) + s*(R,d)           = M + (s-c) q(R0) + (s+c) q(R1)
            piece   P2 = (L,d+m/4) + s*(R,d+m/4)   = cs*M + (1-cs) q(L0) - (1+cs) q(L1)
            Take c = -s when d < m/8 (then P1 = M + 2s q(R0), P2 = -M + 2 q(L0)),
            and  c =  s when d >= m/8 (then P1 = M + 2s q(R1), P2 = M - 2 q(L1)).
            The quarter pieces used were made two levels down: E(L0,+) and
            E(R0,+) make exactly the pieces with d < m/8, E(L1,-) and E(R1,-)
            those with d >= m/8.  (For m = 4 the quarters are single inputs.)
            3 gates for each d:  E(m) = 2 E(m/2) + 3m/4,  E(2) = 1,
            so E(m) = m (3 log2 m - 1) / 4.
  Top, size N: E(L,+), E(R,-); for every d < N/4 one hub (c = +1), then
            two outputs as above (one P1 and one P2, the signs for which the
            quarter piece exists), and the other two by
            P1(-s) = 2A - P1(s)   and   P2(-s) = P2(s) - 2s B.
            5 gates for each d:  T(N) = 2 E(N/2) + 5N/4 = (3/4) N k + N/4.

THE SAME IN COUNT (O).  Keep a piece of size 2^j multiplied by 2^(-floor(j/2))
  and a hub at the scale of the two pieces it is made of.  Then at an even
  level j the hub is halved once (one multiplication, used by both P1 and P2)
  and at an odd level nothing is multiplied.  At the top, for odd k, A and B
  must be doubled (N/2 multiplications).  Outputs: H x / 2^floor(k/2).
  Cost: (7/8) N k + N/4 for even k,  (7/8) N k + (5/8) N for odd k.

THE 8-POINT UNIT (construction 2).  The 19-gate circuit found by the search
  (text below), and the same circuit with its centre g7 halved once: 19
  additions or subtractions and 1 multiplication, output H x / 2.

LAYERS.  If one program computes f*H on 2^a points and another g*H on 2^b
  points, applying the first along the low a address bits (to every block of
  2^a) and the second along the next b bits computes f*g*H on 2^(a+b) points.
  The cost per point adds up.  A final multiplication of every output by
  1/(f*g) gives H x exactly, N more operations in count (O).
"""
from fractions import Fraction as Fr
import slp

G8_19 = """
g1 = x0 + x7
g2 = x1 + x6
g3 = x2 - x5
g4 = x3 - x4
g5 = g1 - g2
g6 = g3 + g4
g7 = g5 - g6
g8 = g7 - 2*x7
g9 = g7 - 2*x5
g10 = g8 + 2*x6
g11 = g9 - 2*x4
y7 = g10 + 2*g4
y3 = g9 + 2*x3
y5 = -y3 + 2*g5
y1 = g10 + 2*g3
y6 = g11 + 2*g2
y2 = g8 + 2*x1
y4 = y2 + 2*g6
y0 = -g11 + 2*g1
"""
BUTTERFLY = "y0 = x0 + x1\ny1 = x0 - x1\n"


class Builder:
    def __init__(self, mode):
        self.mode = mode          # 'G' or 'O'
        self.lines = []
        self.n = 0
        self.cache = {}

    def fresh(self, p='t'):
        self.n += 1
        return '%s%d' % (p, self.n)

    def emit(self, name, terms):
        self.lines.append((name, terms))
        return name

    def scaled(self, w, f):
        if (w, f) not in self.cache:
            self.cache[(w, f)] = self.emit(self.fresh('m'), [(f, w)])
        return self.cache[(w, f)]

    def lin(self, terms, tscale=Fr(1), p='t'):
        """terms = [(coef, (wire, scale))]: the wire holds scale * (its true value).
        Makes tscale * (sum of coef * true value).  One line in mode G; in mode O
        only u+v, u-v and c*u are written, and a scaled copy of a wire is made once."""
        if self.mode == 'G':
            return (self.emit(self.fresh(p), [(Fr(c), w) for c, (w, s) in terms]), Fr(1))
        ops = []
        for c, (w, s) in terms:
            e = tscale * c / s
            if abs(e) != 1:
                w = self.scaled(w, abs(e))
            ops.append((1 if e > 0 else -1, w))
        if ops[0][0] < 0 and ops[1][0] > 0:
            ops.reverse()
        if ops[0][0] < 0:
            t = self.emit(self.fresh('n'), [(Fr(1), ops[0][1]), (Fr(1), ops[1][1])])
            return (self.emit(self.fresh(p), [(Fr(-1), t)]), tscale)
        return (self.emit(self.fresh(p), [(Fr(s), w) for s, w in ops]), tscale)


def text(lines, header=''):
    out = ['# ' + h for h in header.split('\n') if h]
    for name, terms in lines:
        s = ''
        for i, (c, w) in enumerate(terms):
            a = abs(c)
            body = w if a == 1 else '%s*%s' % (a, w)
            if i == 0:
                s += ('-' if c < 0 else '') + body
            else:
                s += (' - ' if c < 0 else ' + ') + body
        out.append('%s = %s' % (name, s))
    return '\n'.join(out) + '\n'


def finish(b, outs, exact):
    """outs[j] = (wire, scale) for row j.  Name the outputs y0..y(N-1)."""
    for j, (w, s) in enumerate(outs):
        if exact and s != 1:
            b.emit('y%d' % j, [(1 / s, w)])       # one multiplication
        else:
            b.emit('y%d' % j, [(Fr(1), w)])       # a renaming, free
    return b.lines


def family(k, mode, exact=False):
    """Construction 1.  Returns (lines, factor of the outputs)."""
    N = 1 << k
    b = Builder(mode)

    def sig(m):                   # scale at which a piece of size m is kept
        j = m.bit_length() - 1
        return Fr(1) if mode == 'G' else Fr(1, 1 << (j // 2))

    P = {}
    for i in range(N):
        P[(i, 1, 0)] = ('x%d' % i, Fr(1))

    def E(lo, m, s):
        if m == 2:
            P[(lo, 2, 0 if s > 0 else 1)] = b.lin([(1, P[(lo, 1, 0)]), (s, P[(lo + 1, 1, 0)])], sig(2), 'p')
            return
        h, q = m // 2, m // 4
        E(lo, h, 1)
        E(lo + h, h, -1)
        off = 0 if s > 0 else h
        for d in range(q):
            A = P[(lo, h, d)]
            B = P[(lo + h, h, d + q)]
            if q >= 2 and d >= q // 2:
                c = s
                M = b.lin([(1, A), (c, B)], sig(h), 'hub')
                P1 = b.lin([(1, M), (2 * s, P[(lo + h + q, q, d)])], sig(m), 'p')
                P2 = b.lin([(1, M), (-2, P[(lo + q, q, d)])], sig(m), 'p')
            else:
                c = -s
                M = b.lin([(1, A), (c, B)], sig(h), 'hub')
                P1 = b.lin([(1, M), (2 * s, P[(lo + h, q, d)])], sig(m), 'p')
                P2 = b.lin([(-1, M), (2, P[(lo, q, d)])], sig(m), 'p')
            P[(lo, m, d + off)] = P1
            P[(lo, m, d + q + off)] = P2

    outs = [None] * N
    if k == 1:
        outs[0] = b.lin([(1, P[(0, 1, 0)]), (1, P[(1, 1, 0)])], sig(2), 'p')
        outs[1] = b.lin([(1, P[(0, 1, 0)]), (-1, P[(1, 1, 0)])], sig(2), 'p')
    else:
        h, q = N // 2, N // 4
        E(0, h, 1)
        E(h, h, -1)
        for d in range(q):
            A = P[(0, h, d)]
            B = P[(h, h, d + q)]
            M = b.lin([(1, A), (1, B)], sig(h), 'hub')        # c = +1
            if q >= 2 and d >= q // 2:                        # quarter pieces on L1, R1: sign s = +
                P1 = b.lin([(1, M), (2, P[(h + q, q, d)])], sig(N), 'p')
                P2 = b.lin([(1, M), (-2, P[(q, q, d)])], sig(N), 'p')
                P1o = b.lin([(2, A), (-1, P1)], sig(N), 'p')      # sign -
                P2o = b.lin([(1, P2), (-2, B)], sig(N), 'p')      # sign -
                outs[d], outs[d + q], outs[d + h], outs[d + q + h] = P1, P2, P1o, P2o
            else:                                             # quarter pieces on L0, R0: sign s = -
                P1 = b.lin([(1, M), (-2, P[(h, q, d)])], sig(N), 'p')
                P2 = b.lin([(-1, M), (2, P[(0, q, d)])], sig(N), 'p')
                P1o = b.lin([(2, A), (-1, P1)], sig(N), 'p')      # sign +
                P2o = b.lin([(1, P2), (2, B)], sig(N), 'p')       # sign +
                outs[d + h], outs[d + q + h], outs[d], outs[d + q] = P1, P2, P1o, P2o
    fac = outs[0][1]
    return finish(b, outs, exact), (Fr(1) if exact else fac)


def rescale(src_text, scale_of):
    """Rewrite a count-(G) program as a strict count-(O) program in which the
    wire w holds scale_of(w) times its value in the original."""
    src = slp.parse_text(src_text)
    b = Builder('O')
    W = {'x%d' % i: ('x%d' % i, Fr(1)) for i in range(src.N)}
    for name, terms in src.lines:
        w, s = b.lin([(c, W[u]) for c, u in terms], scale_of(name), 'g')
        W[name] = (w, s)
    rows = src.packed_check()
    outs = [None] * src.N
    for o, j, f in rows:
        outs[j] = W[o]
    return finish(b, outs, False)


class Template:
    """A checked program used as a unit: lines, the output wire of each row, the factor."""
    def __init__(self, lines, name):
        prog = slp.Program(lines)
        rows = prog.packed_check()
        facs = set(f for _, _, f in rows)
        assert len(facs) == 1 and sorted(j for _, j, _ in rows) == list(range(prog.N))
        self.lines = lines
        self.outs = [None] * prog.N
        for o, j, f in rows:
            self.outs[j] = o
        self.factor = facs.pop()
        self.bits = prog.k
        self.name = name
        self.counts = prog.counts()


def layered(k, plan, exact):
    """plan: list of Templates, applied along successive groups of address bits
    (lowest bits first).  Returns (lines, factor)."""
    N = 1 << k
    assert sum(t.bits for t in plan) == k
    b = Builder('raw')
    wires = ['x%d' % i for i in range(N)]
    pos = 0
    fac = Fr(1)
    for t in plan:
        n = 1 << t.bits
        new = wires[:]
        for base in range(N):
            if (base >> pos) & (n - 1):
                continue
            idx = [base + (u << pos) for u in range(n)]
            mp = {'x%d' % u: wires[idx[u]] for u in range(n)}
            for name, terms in t.lines:
                if len(terms) == 1 and terms[0][0] == 1:
                    mp[name] = mp[terms[0][1]]            # a renaming: no line
                else:
                    mp[name] = b.emit(b.fresh('t'), [(c, mp[u]) for c, u in terms])
            for u in range(n):
                new[idx[u]] = mp[t.outs[u]]
        wires = new
        pos += t.bits
        fac *= t.factor
    lines = finish(b, [(w, fac) for w in wires], exact)
    return lines, (Fr(1) if exact else fac)


def units():
    """The small units, each checked on the spot."""
    u = {}
    u['B2'] = Template(slp.parse_text(BUTTERFLY).lines, 'textbook step (2 points)')
    u['G4'] = Template(family(2, 'G')[0], '7 gates, 4 points')
    u['G8'] = Template(slp.parse_text(G8_19).lines, '19 gates, 8 points')
    u['O4'] = Template(family(2, 'O')[0], '4 points, 7 additions and 1 halving, output H x / 2')
    u['O8'] = Template(rescale(G8_19, lambda w: Fr(1) if w in ('g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7') else Fr(1, 2)),
                       '8 points, 19 additions and 1 halving, output H x / 2')
    return u
