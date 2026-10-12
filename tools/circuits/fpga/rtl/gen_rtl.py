#!/usr/bin/env python3
"""gen_rtl.py -- turn a circuit text file for the Walsh-Hadamard transform into
synthesizable Verilog.  Standard library only (Python 3.9).

THE CIRCUIT FORMAT is the one of tools/circuits/slp.py of this repository:
    name = term            a renaming or a scaling (no hardware)
    name = term + term     one adder
    name = term - term     one subtractor
  term = [-] [number *] name, number = a power of two (2, 4, 1/2, ...).
  Inputs x0 .. x(N-1); the output called yJ is row J of H,
  H[J][i] = (-1)^(number of 1-bits common to J and i).

WHAT IS BUILT.
  Inputs are signed, W bits (two's complement), range -2^(W-1) .. 2^(W-1)-1.
  Every line with two terms is ONE adder or subtractor,  a +- (b << k).
  A multiplication or a division by a power of two is wiring: every value is
  kept as (hardware wire) * 2^shift, and the shift is applied where the value
  is used.  So "1/2*g7" and "2*x3" cost nothing.
  Every adder output has the exact width its range needs: the range of a line
  is computed from its integer coefficients on the inputs (largest value = the
  positive coefficients times the largest input plus the negative ones times
  the smallest input).  No wire is wider than that.
  Outputs: full precision, W + log2 N bits each.
  The generator checks, from the coefficients, that output yJ is row J of H,
  and refuses to write a file otherwise.

PORTS (the same for every file).
    input  clk
    input  in_valid
    input  [N*W-1:0]   in_data      x_i = in_data[i*W +: W]
    output out_valid
    output [N*OW-1:0]  out_data     y_j = out_data[j*OW +: OW],  OW = W + log2 N
  out_valid is in_valid delayed by the latency of the variant.

VARIANTS.
  c    combinational.  Latency 0; clk is not used; out_valid = in_valid.
  p    pipelined: a register after every adder level.  The level of an adder is
       1 + the larger level of its two operands; inputs have level 0.  A value
       that is used more than one level after it was made, and an output made
       before the last level, is carried by delay registers.  Latency = depth.
  pK   (p2, p3, ...) the same with a register after every K-th adder level.
       Latency = ceil(depth / K).
  r    registers at the inputs and at the outputs only (for a tool to retime).
       Latency 2.  With --rstages S there are S register stages at the outputs.
  wide (not a design to measure; a helper for the proofs in formal/): the same
       lines in the same order, every wire at the full output width, a doubling
       written as two additions.  Optionally one more output "fits", which is 1
       when every wire holds a value that fits the exact width of variant c.
  No variant has a reset.  The valid bits start at 0; data registers start with
  any value.  The files v/<N>_def_c_w<W>.v are the transform written from its
  definition (one sum per output), the reference of the proofs.
  WARNING: --all rewrites every file in v/.  Do not run it while another job
  reads them.  MANIFEST.sha256 lists the files as checked.

NUMBERS REPORTED for a design at width W.
  adders        lines with two terms
  depth         the largest adder level
  adder bits    the sum of the widths of all adder outputs
  chain bits    the same, not counting the low k bits of an adder a +- (b << k)
                in which a enters with a plus sign: those bits are copies of
                the low bits of a and need no adder cell
  registers     for the pipelined variants: bits after adders, bits of delay
                registers, and the valid bits

USE.
    python3 -B gen_rtl.py --all              write every design in DESIGNS to v/
    python3 -B gen_rtl.py --table            print the table only
    python3 -B gen_rtl.py FILE.txt --variant p --width 8 --name foo -o foo.v
"""
import argparse
import json
import os
import re
import sys
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
RELEASE = os.path.normpath(os.path.join(HERE, '..', '..'))      # tools/circuits of this repository
PROG = os.path.join(RELEASE, 'programs')
CIRC = os.path.join(HERE, 'circuits')
VDIR = os.path.join(HERE, 'v')

# ----------------------------------------------------------------------------
# reading the text format
# ----------------------------------------------------------------------------
TOK = re.compile(r'\s*(?:(\d+(?:/\d+)?)|([A-Za-z_]\w*)|([-+*]))')


def parse_text(text):
    """Returns the list of lines (name, [(coef, operand)]) and the '# OUT' list or None."""
    lines, outs = [], None
    for raw in text.splitlines():
        if raw.startswith('# OUT '):
            outs = raw[6:].split()
        s = raw.split('#', 1)[0].strip()
        if not s:
            continue
        if '=' not in s:
            raise ValueError('no "=" in line: ' + raw)
        lhs, rhs = s.split('=', 1)
        toks, pos = [], 0
        rhs = rhs.strip()
        while pos < len(rhs):
            m = TOK.match(rhs, pos)
            if not m:
                raise ValueError('cannot read: ' + raw)
            toks.append(('n', m.group(1)) if m.group(1) else
                        ('w', m.group(2)) if m.group(2) else ('o', m.group(3)))
            pos = m.end()
        terms, i = [], 0
        while i < len(toks):
            sign = 1
            if terms and not (toks[i][0] == 'o' and toks[i][1] in '+-'):
                raise ValueError('expected + or -: ' + raw)
            while i < len(toks) and toks[i][0] == 'o' and toks[i][1] in '+-':
                if toks[i][1] == '-':
                    sign = -sign
                i += 1
            coef = Fr(1)
            if toks[i][0] == 'n':
                coef = Fr(toks[i][1])
                i += 1
                if toks[i] != ('o', '*'):
                    raise ValueError('expected *: ' + raw)
                i += 1
            if toks[i][0] != 'w':
                raise ValueError('expected a name: ' + raw)
            terms.append((sign * coef, toks[i][1]))
            i += 1
        lines.append((lhs.strip(), terms))
    return lines, outs


def to_text(lines, header=''):
    out = ['# ' + h for h in header.split('\n') if h]
    for name, terms in lines:
        s = ''
        for i, (c, w) in enumerate(terms):
            a = abs(c)
            body = w if a == 1 else '%s*%s' % (a, w)
            s += (('-' if c < 0 else '') + body) if i == 0 else ((' - ' if c < 0 else ' + ') + body)
        out.append('%s = %s' % (name, s))
    return '\n'.join(out) + '\n'


def log2_exact(q):
    """q = 2^e for an integer e (q a positive Fraction); returns e."""
    if q.numerator == 1:
        d = q.denominator
        if d & (d - 1) == 0:
            return -(d.bit_length() - 1)
    if q.denominator == 1:
        n = q.numerator
        if n > 0 and n & (n - 1) == 0:
            return n.bit_length() - 1
    raise ValueError('coefficient %s is not a power of two' % q)


# ----------------------------------------------------------------------------
# the circuit as hardware: adders, shifts, coefficient vectors, levels
# ----------------------------------------------------------------------------
class Circuit:
    def __init__(self, lines, outs=None, source=''):
        self.source = source
        mx = -1
        for _, terms in lines:
            for _, u in terms:
                if re.fullmatch(r'x\d+', u):
                    mx = max(mx, int(u[1:]))
        self.N = N = mx + 1
        if N < 2 or N & (N - 1):
            raise ValueError('number of inputs is not a power of two: %d' % N)
        self.k = N.bit_length() - 1
        # W[name] = (hardware node, shift): value of name = node * 2^shift
        W = {}
        self.coef = {}            # node -> integer coefficient vector on the inputs
        self.level = {}
        self.adders = []          # (node, (sa, A, ka), (sb, B, kb)): node = sa*(A<<ka) + sb*(B<<kb)
        self.add_of = {}
        for i in range(N):
            x = 'x%d' % i
            W[x] = (x, 0)
            v = [0] * N
            v[i] = 1
            self.coef[x] = v
            self.level[x] = 0
        for name, terms in lines:
            if name in W:
                raise ValueError('name defined twice: ' + name)
            if len(terms) == 1:
                c, u = terms[0]
                if c < 0:
                    raise ValueError('a line "name = -term" would need a negation: ' + name)
                h, e = W[u]
                W[name] = (h, e + log2_exact(c))
                continue
            if len(terms) != 2:
                raise ValueError('a line has one or two terms: ' + name)
            (c1, u1), (c2, u2) = terms
            if c1 < 0 and c2 < 0:
                raise ValueError('both terms negative (needs a negation): ' + name)
            h1, e1 = W[u1]
            h2, e2 = W[u2]
            a = e1 + log2_exact(abs(c1))
            b = e2 + log2_exact(abs(c2))
            m = min(a, b)
            s1 = 1 if c1 > 0 else -1
            s2 = 1 if c2 > 0 else -1
            node = name
            self.coef[node] = [s1 * (p << (a - m)) + s2 * (q << (b - m))
                               for p, q in zip(self.coef[h1], self.coef[h2])]
            if not any(self.coef[node]):
                raise ValueError('line %s is identically zero' % name)
            self.level[node] = 1 + max(self.level[h1], self.level[h2])
            rec = (node, (s1, h1, a - m), (s2, h2, b - m))
            self.adders.append(rec)
            self.add_of[node] = rec
            W[name] = (node, m)
        if outs is None:
            outs = [name for name, _ in lines if name.startswith('y')]
        # outputs: yJ must be row J of H, exactly
        self.outs = [None] * N
        for o in outs:
            h, e = W[o]
            if e < 0:
                raise ValueError('output %s is not an integer combination' % o)
            vec = [c << e for c in self.coef[h]]
            f = vec[0]
            if abs(f) != 1:
                raise ValueError('output %s is not a row of H (coefficient %d at x0)' % (o, f))
            J = None
            for j in range(N):
                if all(vec[i] == (f if bin(i & j).count('1') % 2 == 0 else -f) for i in range(N)):
                    J = j
                    break
            if J is None or f != 1:
                raise ValueError('output %s is not a row of H' % o)
            if re.fullmatch(r'y\d+', o) and int(o[1:]) != J:
                raise ValueError('output %s is row %d' % (o, J))
            if self.outs[J] is not None:
                raise ValueError('row %d appears twice' % J)
            self.outs[J] = (h, e)
        if any(o is None for o in self.outs):
            raise ValueError('some row of H is missing from the outputs')
        # every adder must be used
        used = set(h for h, _ in self.outs)
        for node, (_, A, _), (_, B, _) in reversed(self.adders):
            if node in used:
                used.add(A)
                used.add(B)
        dead = [a[0] for a in self.adders if a[0] not in used]
        if dead:
            raise ValueError('lines not used by any output: ' + ' '.join(dead))
        self.depth = max(self.level[h] for h, _ in self.outs)

    # ---- widths ------------------------------------------------------------
    @staticmethod
    def range_of(vec, Wd):
        hi_in = (1 << (Wd - 1)) - 1
        lo_in = -(1 << (Wd - 1))
        pos = sum(c for c in vec if c > 0)
        neg = sum(-c for c in vec if c < 0)
        return pos * lo_in + neg * (-hi_in), pos * hi_in + neg * (-lo_in)

    @staticmethod
    def bits_for(lo, hi):
        w = 1
        while not (-(1 << (w - 1)) <= lo and hi <= (1 << (w - 1)) - 1):
            w += 1
        return w

    def widths(self, Wd):
        wd = {}
        for node, vec in self.coef.items():
            lo, hi = self.range_of(vec, Wd)
            wd[node] = self.bits_for(lo, hi)
        for i in range(self.N):
            assert wd['x%d' % i] == Wd
        return wd

    # ---- the numbers of the table -------------------------------------------
    def schedule(self, K):
        """Register plan with a register bank after every K-th adder level.
        Returns (seg, need, D): seg[node] = the segment in which node is computed
        (0 for inputs), need[node] = the last bank that must hold a copy of node,
        D = number of banks = latency."""
        seg = {}
        for node, lv in self.level.items():
            seg[node] = -(-lv // K)
        D = -(-self.depth // K)
        need = dict((node, 0) for node in seg)
        for node, (_, A, _), (_, B, _) in self.adders:
            s = seg[node]
            for u in (A, B):
                if seg[u] < s:
                    need[u] = max(need[u], s - 1)
        for h, _ in self.outs:
            need[h] = D
        return seg, need, D

    def copies(self, node, seg, need):
        """The banks that hold a copy of node."""
        first = max(seg[node], 1)
        return list(range(first, need[node] + 1))

    def metrics(self, Wd, K=1):
        wd = self.widths(Wd)
        OW = Wd + self.k
        assert max(wd[h] + e for h, e in self.outs) == OW, 'output width'
        adder_bits = sum(wd[a[0]] for a in self.adders)
        chain_bits = 0
        hist = {}
        for node, (sa, A, ka), (sb, B, kb) in self.adders:
            free = 0
            if ka == 0 and kb > 0 and sa > 0:
                free = kb
            elif kb == 0 and ka > 0 and sb > 0:
                free = ka
            chain_bits += max(wd[node] - free, 0)
            hist[wd[node]] = hist.get(wd[node], 0) + 1
        seg, need, D = self.schedule(K)
        reg_adder = reg_delay = 0
        for node in self.coef:
            cp = self.copies(node, seg, need)
            if not cp:
                continue
            if node in self.add_of:
                reg_adder += wd[node]
                reg_delay += wd[node] * (len(cp) - 1)
            else:
                reg_delay += wd[node] * len(cp)
        return dict(N=self.N, W=Wd, OW=OW, adders=len(self.adders), depth=self.depth,
                    adder_bits=adder_bits, chain_bits=chain_bits,
                    width_histogram=dict((str(k), v) for k, v in sorted(hist.items())),
                    every=K, latency=D, reg_after_adders=reg_adder, reg_delay=reg_delay,
                    reg_data=reg_adder + reg_delay, reg_valid=D,
                    r_reg_data=self.N * Wd + self.N * OW, r_reg_valid=2)

    # ---- Verilog ------------------------------------------------------------
    def verilog(self, Wd, variant, module, K=1, rstages=1, note='', fits=False):
        N, k = self.N, self.k
        OW = Wd + k
        wd = self.widths(Wd)
        m = self.metrics(Wd, K)
        o = []
        o.append('// Written by gen_rtl.py.  Do not edit by hand.')
        o.append('// %d-point Walsh-Hadamard transform, y_J = sum over i of (-1)^popcount(J & i) * x_i.' % N)
        o.append('// Source circuit: %s' % self.source)
        if note:
            for ln in note.split('\n'):
                o.append('// ' + ln)
        o.append('// Inputs: %d signed values of %d bits.  Outputs: %d signed values of %d bits.' % (N, Wd, N, OW))
        o.append('// Adders %d, depth %d adder levels, adder bits %d (chain bits %d).'
                 % (m['adders'], m['depth'], m['adder_bits'], m['chain_bits']))

        def sx(name):          # an operand name is already a signed wire or reg
            return name

        def expr(sa, A, ka, sb, B, kb):
            ta = A if ka == 0 else '(%s <<< %d)' % (A, ka)
            tb = B if kb == 0 else '(%s <<< %d)' % (B, kb)
            if sa > 0 and sb > 0:
                return '%s + %s' % (ta, tb)
            if sa > 0:
                return '%s - %s' % (ta, tb)
            return '%s - %s' % (tb, ta)

        def ports(extra=''):
            o.append('`default_nettype none')
            o.append('module %s (' % module)
            o.append('    input  wire                 clk,')
            o.append('    input  wire                 in_valid,')
            o.append('    input  wire [%d:0] in_data,' % (N * Wd - 1))
            o.append('    output wire                 out_valid,')
            o.append('    output wire [%d:0] out_data%s' % (N * OW - 1, ',' if extra else ''))
            if extra:
                o.append(extra)
            o.append(');')

        def outputs(ref, target='    assign out_data = {'):
            for j, (h, e) in enumerate(self.outs):
                r = ref(h)
                o.append('    wire signed [%d:0] o%d = %s;' % (OW - 1, j, r if e == 0 else '(%s <<< %d)' % (r, e)))
            names = ['o%d' % j for j in range(N - 1, -1, -1)]
            o.append(target)
            for i in range(0, N, 8):
                o.append('        ' + ', '.join(names[i:i + 8]) + (',' if i + 8 < N else ''))
            o.append('    };')

        nm = lambda node: node if node.startswith('x') and node[1:].isdigit() else 'n_' + node

        if variant == 'c':
            o.append('// Variant c: combinational.  Latency 0.  clk is not used.')
            ports()
            for i in range(N):
                o.append('    wire signed [%d:0] x%d = in_data[%d:%d];' % (Wd - 1, i, i * Wd + Wd - 1, i * Wd))
            for node, (sa, A, ka), (sb, B, kb) in self.adders:
                o.append('    wire signed [%d:0] %s = %s;   // level %d'
                         % (wd[node] - 1, nm(node), expr(sa, nm(A), ka, sb, nm(B), kb), self.level[node]))
            outputs(nm)
            o.append('    assign out_valid = in_valid;')
            o.append('    wire _unused_clk = clk;')
        elif variant == 'wide':
            # A helper for the equivalence proofs, not a design to be measured: the same adders
            # in the same order, but every wire has the full output width, and a doubling is
            # written as two additions so that a solver sees sums only.
            o.append('// Variant wide (proof helper): the same lines, every wire %d bits, doublings as repeated addition.' % OW)
            if fits:
                o.append('// Output "fits" is 1 when every wire holds a value that fits the exact width gen_rtl.py gives it.')
            ports('    output wire                 fits' if fits else '')
            for i in range(N):
                o.append('    wire signed [%d:0] x%d = $signed(in_data[%d:%d]);' % (OW - 1, i, i * Wd + Wd - 1, i * Wd))

            def rep(name, kk, sign):
                return ''.join((' %s %s' % ('+' if sign > 0 else '-', name)) for _ in range(1 << kk))

            for node, (sa, A, ka), (sb, B, kb) in self.adders:
                if sa > 0:
                    e_ = rep(nm(A), ka, 1)[3:] + rep(nm(B), kb, sb)
                else:
                    e_ = rep(nm(B), kb, 1)[3:] + rep(nm(A), ka, sa)
                o.append('    wire signed [%d:0] %s = %s;   // level %d, exact width %d'
                         % (OW - 1, nm(node), e_, self.level[node], wd[node]))
            for j, (h, e) in enumerate(self.outs):
                o.append('    wire signed [%d:0] o%d = %s;' % (OW - 1, j, rep(nm(h), e, 1)[3:]))
            names = ['o%d' % j for j in range(N - 1, -1, -1)]
            o.append('    assign out_data = {')
            for i in range(0, N, 8):
                o.append('        ' + ', '.join(names[i:i + 8]) + (',' if i + 8 < N else ''))
            o.append('    };')
            o.append('    assign out_valid = in_valid;')
            o.append('    wire _unused_clk = clk;')
            if fits:
                fl = []
                for node, _, _ in self.adders:
                    w = wd[node]
                    if w < OW:
                        # the bits from w-1 up are all equal: the value is the sign extension of its low w bits
                        o.append('    wire f_%s = (%s[%d:%d] == {%d{%s[%d]}});   // fits %d bits'
                                 % (node, nm(node), OW - 1, w - 1, OW - w + 1, nm(node), w - 1, w))
                        fl.append('f_' + node)
                    elif w > OW:
                        raise ValueError('wire %s needs more bits than the outputs' % node)
                o.append('    assign fits = %s;' % (' & '.join(fl) if fl else "1'b1"))
        elif variant == 'r':
            o.append('// Variant r: one register stage at the inputs, %d at the outputs, nothing between.  Latency %d.'
                     % (rstages, 1 + rstages))
            o.append('// Register bits: %d at the inputs, %d at the outputs, %d valid bits.'
                     % (N * Wd, rstages * N * OW, 1 + rstages))
            ports()
            for i in range(N):
                o.append('    reg  signed [%d:0] x%d;' % (Wd - 1, i))
            o.append('    always @(posedge clk) begin')
            for i in range(N):
                o.append('        x%d <= in_data[%d:%d];' % (i, i * Wd + Wd - 1, i * Wd))
            o.append('    end')
            for node, (sa, A, ka), (sb, B, kb) in self.adders:
                o.append('    wire signed [%d:0] %s = %s;   // level %d'
                         % (wd[node] - 1, nm(node), expr(sa, nm(A), ka, sb, nm(B), kb), self.level[node]))
            outputs(nm, '    wire [%d:0] out_comb = {' % (N * OW - 1))
            for s in range(1, rstages + 1):
                o.append('    reg  [%d:0] out_q%d;' % (N * OW - 1, s))
            o.append('    reg  [%d:0] vld = %d\'d0;' % (rstages, rstages + 1))
            o.append('    always @(posedge clk) begin')
            o.append('        out_q1 <= out_comb;')
            for s in range(2, rstages + 1):
                o.append('        out_q%d <= out_q%d;' % (s, s - 1))
            o.append('        vld <= {vld[%d:0], in_valid};' % (rstages - 1))
            o.append('    end')
            o.append('    assign out_data = out_q%d;' % rstages)
            o.append('    assign out_valid = vld[%d];' % rstages)
        elif variant == 'p':
            seg, need, D = self.schedule(K)
            o.append('// Variant p%s: a register after every %sadder level.  Latency %d.'
                     % ('' if K == 1 else str(K), '' if K == 1 else ('%d-th ' % K if K > 3 else {2: 'second ', 3: 'third '}[K]), D))
            o.append('// Register bits: %d after adders, %d in delay registers, %d valid bits.'
                     % (m['reg_after_adders'], m['reg_delay'], D))
            ports()

            def ref_at(node, s):
                """Name of node as seen by logic in segment s (s = D + 1 for the outputs)."""
                if seg[node] == s:
                    return nm(node)
                if s - 1 == 0:
                    assert seg[node] == 0
                    return nm(node)
                assert s - 1 in self.copies(node, seg, need), (node, s)
                return '%s_r%d' % (nm(node), s - 1)

            for i in range(N):
                o.append('    wire signed [%d:0] x%d = in_data[%d:%d];' % (Wd - 1, i, i * Wd + Wd - 1, i * Wd))
            regs = []
            for node in ['x%d' % i for i in range(N)] + [a[0] for a in self.adders]:
                if node in self.add_of:
                    _, (sa, A, ka), (sb, B, kb) = self.add_of[node]
                    s = seg[node]
                    o.append('    wire signed [%d:0] %s = %s;   // level %d, stage %d'
                             % (wd[node] - 1, nm(node),
                                expr(sa, ref_at(A, s), ka, sb, ref_at(B, s), kb), self.level[node], s))
                prev = nm(node)
                for t in self.copies(node, seg, need):
                    o.append('    reg  signed [%d:0] %s_r%d;' % (wd[node] - 1, nm(node), t))
                    regs.append('%s_r%d <= %s;' % (nm(node), t, prev))
                    prev = '%s_r%d' % (nm(node), t)
            outputs(lambda h: ref_at(h, D + 1))
            if D == 1:
                o.append('    reg  vld = 1\'b0;')
            else:
                o.append('    reg  [%d:0] vld = %d\'d0;' % (D - 1, D))
            o.append('    always @(posedge clk) begin')
            for r in regs:
                o.append('        ' + r)
            if D == 1:
                o.append('        vld <= in_valid;')
            else:
                o.append('        vld <= {vld[%d:0], in_valid};' % (D - 2))
            o.append('    end')
            o.append('    assign out_valid = %s;' % ('vld' if D == 1 else 'vld[%d]' % (D - 1)))
        else:
            raise ValueError('variant ' + variant)
        o.append('endmodule')
        o.append('`default_nettype wire')
        return '\n'.join(o) + '\n'


def definition_verilog(N, Wd, module):
    """The transform written from its definition: every output is one sum of N signed terms."""
    k = N.bit_length() - 1
    OW = Wd + k
    o = ['// Written by gen_rtl.py.  Do not edit by hand.',
         '// %d-point Walsh-Hadamard transform written from the definition:' % N,
         '// y_J = sum over i of (-1)^popcount(J & i) * x_i, one expression per output, %d bits.' % OW,
         '// A reference for the equivalence proofs; not a design to be measured.',
         '`default_nettype none',
         'module %s (' % module,
         '    input  wire                 clk,',
         '    input  wire                 in_valid,',
         '    input  wire [%d:0] in_data,' % (N * Wd - 1),
         '    output wire                 out_valid,',
         '    output wire [%d:0] out_data' % (N * OW - 1),
         ');']
    for i in range(N):
        o.append('    wire signed [%d:0] x%d = $signed(in_data[%d:%d]);' % (OW - 1, i, i * Wd + Wd - 1, i * Wd))
    for j in range(N):
        s = ''
        for i in range(N):
            neg = bin(i & j).count('1') % 2
            s += (' - ' if neg else ' + ') + 'x%d' % i if i else 'x0'
        o.append('    wire signed [%d:0] o%d = %s;' % (OW - 1, j, s))
    names = ['o%d' % j for j in range(N - 1, -1, -1)]
    o.append('    assign out_data = {')
    for i in range(0, N, 8):
        o.append('        ' + ', '.join(names[i:i + 8]) + (',' if i + 8 < N else ''))
    o.append('    };')
    o.append('    assign out_valid = in_valid;')
    o.append('    wire _unused_clk = clk;')
    o.append('endmodule')
    o.append('`default_nettype wire')
    return '\n'.join(o) + '\n'


# ----------------------------------------------------------------------------
# the designs
# ----------------------------------------------------------------------------
# The 4-point circuit of Coppersmith, Feig and Linzer (1994), page 969:
#   z0 = x1 + x2; z1 = z0 + x3; z2 = x0 - z1; y0 = x0 + z1;
#   y1 = z2 + 2 x2; y2 = z2 + 2 x1; y3 = z2 + 2 x3.
CFL4 = """
z0 = x1 + x2
z1 = z0 + x3
z2 = x0 - z1
y0 = x0 + z1
y1 = z2 + 2*x2
y2 = z2 + 2*x1
y3 = z2 + 2*x3
"""
BUTTERFLY = "y0 = x0 + x1\ny1 = x0 - x1\n"

# The 8-point step of Alman and Rao, arXiv:2211.06459v2, Algorithm 5, lines 12 to 28, at N = 8
# (so a = x0 and b..h = 2*x1 .. 2*x7, the scaled inputs of lines 4 to 11 with k = 0).
# Their lines, with their names; a name with a digit suffix (t1, t2, u1..u4) is mine, for the
# sums of three or four terms that they write on one line.  22 additions or subtractions,
# one halving, seven doublings of inputs.  Two ways to bracket the sums are given.
AR8_HEAD = """
a = x0
b = 2*x1
c = 2*x2
d = 2*x3
e = 2*x4
f = 2*x5
g = 2*x6
h = 2*x7
B1 = b + c
B2 = d + h
B3 = f + g
"""
AR8_BALANCED = AR8_HEAD + """
t1 = B1 + B2
t2 = B3 + e
totsum = t1 + t2
tot = 1/2*totsum
diff = a - tot
D = diff + d
E = diff + e
H = diff + h
y0 = a + tot
u1 = c + g
y1 = E + u1
u2 = b + f
y2 = E + u2
y3 = E + B2
y4 = D + B1
u3 = c + f
y5 = H + u3
u4 = b + g
y6 = H + u4
y7 = D + B3
"""
AR8_LEFT = AR8_HEAD + """
t1 = B1 + B2
t2 = t1 + B3
totsum = t2 + e
tot = 1/2*totsum
diff = a - tot
D = diff + d
E = diff + e
H = diff + h
y0 = a + tot
u1 = E + c
y1 = u1 + g
u2 = E + b
y2 = u2 + f
y3 = E + B2
y4 = D + B1
u3 = H + c
y5 = u3 + f
u4 = H + b
y6 = u4 + g
y7 = D + B3
"""


def unit(text):
    """A small circuit used as a building block: (lines, the name of the output for each row, bits)."""
    lines, _ = parse_text(text)
    c = Circuit(lines)
    outs = [None] * c.N
    for name, _ in lines:
        if re.fullmatch(r'y\d+', name):
            outs[int(name[1:])] = name
    return lines, outs, c.k


def layered(N, plan):
    """Apply the units of plan along successive groups of address bits, lowest bits first.
    The same construction as layered() in tools/circuits/gen.py."""
    k = N.bit_length() - 1
    assert sum(u[2] for u in plan) == k
    out, cnt = [], [0]
    wires = ['x%d' % i for i in range(N)]
    pos = 0
    for lines, uouts, bits in plan:
        n = 1 << bits
        new = wires[:]
        for base in range(N):
            if (base >> pos) & (n - 1):
                continue
            idx = [base + (u << pos) for u in range(n)]
            mp = dict(('x%d' % u, wires[idx[u]]) for u in range(n))
            for name, terms in lines:
                if len(terms) == 1 and terms[0][0] == 1:
                    mp[name] = mp[terms[0][1]]
                else:
                    cnt[0] += 1
                    t = 't%d' % cnt[0]
                    out.append((t, [(c, mp[u]) for c, u in terms]))
                    mp[name] = t
            for u in range(n):
                new[idx[u]] = mp[uouts[u]]
        wires = new
        pos += bits
    for j, w in enumerate(wires):
        out.append(('y%d' % j, [(Fr(1), w)]))
    return out


def read_release(rel):
    with open(os.path.join(PROG, rel)) as f:
        return f.read()


def build_designs():
    """Returns the list of designs: dict(size, design, primary, text, source, note)."""
    B2 = unit(BUTTERFLY)
    C4 = unit(CFL4)
    T8 = unit(read_release('generated/O_textbook_8.txt'))
    D = []

    def add(size, design, text, source, primary=True, note=''):
        D.append(dict(size=size, design=design, text=text, source=source, primary=primary, note=note))

    rel = 'tools/circuits/programs/'
    # 8 points
    add('8', 'textbook', read_release('generated/O_textbook_8.txt'), rel + 'generated/O_textbook_8.txt',
        note='The textbook: 3 layers of 4 butterflies (a+b, a-b).  24 adders.')
    add('8', 'cfl1994', to_text(layered(8, [C4, B2]),
        '8 points, 22 adders: the 4-point circuit of Coppersmith, Feig and Linzer (1994) on each half,\n'
        'then one plain layer of 4 butterflies.  Written by tools/circuits/fpga/rtl/gen_rtl.py; output yJ = row J of H.'),
        'tools/circuits/fpga/rtl/circuits/8_cfl1994.txt',
        note='Coppersmith, Feig, Linzer (1994): two 4-point circuits of 7, then one plain layer of 8.  22 adders.')
    add('8', 'cfl1994b', to_text(layered(8, [B2, C4]),
        '8 points, 22 adders: one plain layer of 4 butterflies, then the 4-point circuit of Coppersmith,\n'
        'Feig and Linzer (1994) twice.  Written by tools/circuits/fpga/rtl/gen_rtl.py; output yJ = row J of H.'),
        'tools/circuits/fpga/rtl/circuits/8_cfl1994b.txt', primary=False,
        note='Coppersmith, Feig, Linzer (1994), the other order: one plain layer of 8, then two 4-point circuits of 7.')
    add('8', 'ar2023', '# 8 points: the step of Alman and Rao, arXiv:2211.06459v2, Algorithm 5 (lines 12 to 28) at N = 8.\n'
        '# 22 additions or subtractions, one halving, seven doublings of inputs.  Sums of three or four terms\n'
        '# are bracketed in pairs (the paper writes them on one line).  Output yJ = row J of H.\n' + AR8_BALANCED,
        'tools/circuits/fpga/rtl/circuits/8_ar2023.txt',
        note='Alman and Rao (2023), Algorithm 5 at 8 points: 22 adders; the halving and the doublings are wiring.\n'
             'Their sums of three and four terms are bracketed in pairs.')
    add('8', 'ar2023l', '# 8 points: the step of Alman and Rao, arXiv:2211.06459v2, Algorithm 5 (lines 12 to 28) at N = 8.\n'
        '# 22 additions or subtractions, one halving, seven doublings of inputs.  Sums of three or four terms\n'
        '# are taken from left to right, as written.  Output yJ = row J of H.\n' + AR8_LEFT,
        'tools/circuits/fpga/rtl/circuits/8_ar2023l.txt', primary=False,
        note='Alman and Rao (2023), Algorithm 5 at 8 points, sums taken from left to right as written.  22 adders.')
    add('8', 'ours', read_release('h8_19gates.txt'), rel + 'h8_19gates.txt',
        note='This work: the 19-adder circuit.')
    # 16 points
    add('16', 'textbook', read_release('generated/O_textbook_16.txt'), rel + 'generated/O_textbook_16.txt',
        note='The textbook: 4 layers of 8 butterflies.  64 adders.')
    add('16', 'cfl1994', to_text(layered(16, [C4, C4]),
        '16 points, 56 adders: the 4-point circuit of Coppersmith, Feig and Linzer (1994) in two layers\n'
        '(eight 4-point circuits).  Written by tools/circuits/fpga/rtl/gen_rtl.py; output yJ = row J of H.'),
        'tools/circuits/fpga/rtl/circuits/16_cfl1994.txt',
        note='Coppersmith, Feig, Linzer (1994): eight 4-point circuits of 7 in two layers.  56 adders.')
    add('16', 'ours', read_release('h16_52gates.txt'), rel + 'h16_52gates.txt',
        note='This work: the 52-adder circuit (the family at 16 points).')
    # 64 points
    add('64', 'textbook', read_release('generated/O_textbook_64.txt'), rel + 'generated/O_textbook_64.txt',
        note='The textbook: 6 layers of 32 butterflies.  384 adders.')
    add('64', 'cfl1994', to_text(layered(64, [C4, C4, C4]),
        '64 points, 336 adders: the 4-point circuit of Coppersmith, Feig and Linzer (1994) in three layers.\n'
        'Written by tools/circuits/fpga/rtl/gen_rtl.py; output yJ = row J of H.'),
        'tools/circuits/fpga/rtl/circuits/64_cfl1994.txt',
        note='Coppersmith, Feig, Linzer (1994): 48 4-point circuits of 7 in three layers.  336 adders.')
    add('64', 'ours', read_release('generated/G_family_64.txt'), rel + 'generated/G_family_64.txt',
        note='This work: the family (3/4) N log2 N + N/4 at 64 points, written by tools/circuits/gen.py.  304 adders.')
    # the 8 x 8 block transform: Y = H8 X H8^T with X[r][c] = x_(8r+c); 16 one-dimensional transforms.
    # It is the same function as the 64-point transform.
    add('8x8', 'textbook', to_text(layered(64, [T8, T8]),
        '8 x 8 block, 384 adders: the textbook 8-point transform on the 8 rows, then on the 8 columns.\n'
        'Input x_(8r+c) = X[r][c]; output y_(8u+v) = Y[u][v].  Written by tools/circuits/fpga/rtl/gen_rtl.py.'),
        'tools/circuits/fpga/rtl/circuits/8x8_textbook.txt',
        note='2-D 8 x 8: the textbook 8-point transform on rows, then on columns (16 transforms, 384 adders).\n'
             'It is the same network of adders as 64_textbook, in another order of lines.')
    add('8x8', 'ours', read_release('generated/G_layers_64.txt'), rel + 'generated/G_layers_64.txt',
        note='2-D 8 x 8: the 19-adder circuit on rows, then on columns (16 transforms, 304 adders).')
    return D


VARIANTS = [('c', 'c', 1), ('p', 'p', 1), ('p2', 'p', 2), ('r', 'r', 1)]
WIDTHS = [8, 12, 16]


def base_name(size, design, vname, Wd):
    return '%s_%s_%s_w%d' % (size, design, vname, Wd)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('file', nargs='?')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--table', action='store_true')
    ap.add_argument('--variant', default='c', help='c, p, p2, p3, ..., r')
    ap.add_argument('--width', type=int, default=8)
    ap.add_argument('--rstages', type=int, default=1)
    ap.add_argument('--name', default=None)
    ap.add_argument('-o', '--out', default=None)
    a = ap.parse_args()

    if a.file:
        with open(a.file) as f:
            lines, outs = parse_text(f.read())
        c = Circuit(lines, outs, a.file)
        v = a.variant
        K = int(v[1:]) if v.startswith('p') and len(v) > 1 else 1
        kind = 'p' if v.startswith('p') else v
        name = a.name or 'wht_%d_custom_%s_w%d' % (c.N, v, a.width)
        txt = c.verilog(a.width, kind, name, K=K, rstages=a.rstages)
        if a.out:
            with open(a.out, 'w') as f:
                f.write(txt)
        else:
            sys.stdout.write(txt)
        sys.stderr.write(json.dumps(c.metrics(a.width, K)) + '\n')
        return

    designs = build_designs()
    rows = []
    if a.all:
        os.makedirs(CIRC, exist_ok=True)
        os.makedirs(VDIR, exist_ok=True)
    manifest = []
    for d in designs:
        lines, outs = parse_text(d['text'])
        src = d['source']
        if a.all and src.startswith('tools/circuits/fpga/rtl/circuits/'):
            with open(os.path.join(CIRC, os.path.basename(src)), 'w') as f:
                f.write(d['text'])
        c = Circuit(lines, outs, src)
        for Wd in WIDTHS:
            m1 = c.metrics(Wd, 1)
            m2 = c.metrics(Wd, 2)
            row = dict(size=d['size'], design=d['design'], primary=d['primary'], source=src, **m1)
            row['p2_latency'] = m2['latency']
            row['p2_reg_after_adders'] = m2['reg_after_adders']
            row['p2_reg_delay'] = m2['reg_delay']
            row['p2_reg_data'] = m2['reg_data']
            row['files'] = {}
            for vname, kind, K in VARIANTS:
                bn = base_name(d['size'], d['design'], vname, Wd)
                lat = {'c': 0, 'r': 2}.get(kind, -(-c.depth // K))
                row['files'][vname] = dict(file='v/%s.v' % bn, module='wht_' + bn, latency=lat)
                if a.all:
                    with open(os.path.join(VDIR, bn + '.v'), 'w') as f:
                        f.write(c.verilog(Wd, kind, 'wht_' + bn, K=K, note=d['note']))
            rows.append(row)
    # the definition, as a reference for proofs
    defs = []
    for size, N in (('8', 8), ('16', 16), ('64', 64)):
        for Wd in WIDTHS:
            bn = base_name(size, 'def', 'c', Wd)
            defs.append(dict(size=size, N=N, W=Wd, file='v/%s.v' % bn, module='wht_' + bn))
            if a.all:
                with open(os.path.join(VDIR, bn + '.v'), 'w') as f:
                    f.write(definition_verilog(N, Wd, 'wht_' + bn))
    if a.all:
        with open(os.path.join(HERE, 'designs.json'), 'w') as f:
            json.dump(dict(designs=rows, definitions=defs), f, indent=1)
    # the table
    print('%-4s %-9s %2s  %6s %5s  %10s %10s | %9s %9s %8s %5s | %9s %6s | %8s'
          % ('size', 'design', 'W', 'adders', 'depth', 'adder_bits', 'chain_bits',
             'p:adderFF', 'p:delayFF', 'p:total', 'p:lat', 'p2:total', 'p2:lat', 'r:total'))
    for r in rows:
        print('%-4s %-9s %2d  %6d %5d  %10d %10d | %9d %9d %8d %5d | %9d %6d | %8d'
              % (r['size'], r['design'], r['W'], r['adders'], r['depth'], r['adder_bits'], r['chain_bits'],
                 r['reg_after_adders'], r['reg_delay'], r['reg_data'], r['latency'],
                 r['p2_reg_data'], r['p2_latency'], r['r_reg_data']))


if __name__ == '__main__':
    main()
