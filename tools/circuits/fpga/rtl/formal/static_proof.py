#!/usr/bin/env python3
"""static_proof.py -- a second proof, written separately from the generator, that a combinational design file computes the
Walsh-Hadamard transform for ALL inputs.  It does not use gen_rtl.py, the circuit text
files, or any solver.  It reads the Verilog text that was synthesised.

Method.  Every line of these files is   wire signed [h:0] NAME = T1 (+|-) T2;   or   = T1;
with T = NAME, (NAME <<< k), or an input slice.  All operands are declared signed, so Verilog
evaluates the right-hand side in two's complement at the width of the widest of {left side,
operands}, sign-extending each operand first, and then keeps the low h+1 bits.  Arithmetic
modulo 2^n followed by truncation gives the exact integer whenever the exact integer fits the
left side.  So the file is correct for all inputs if
  (1) for every wire, the exact integer value fits in its declared signed width, given that the
      wires it reads are exact (induction over the file order), and
  (2) output j has coefficient (-1)^popcount(j & i) on input i.
The exact value of each wire is an integer combination of the inputs; its largest and smallest
values over all inputs are  sum(pos)*max + sum(neg)*min  and  sum(pos)*min + sum(neg)*max.
The script refuses any line it does not fully understand."""
import re, sys

def prove(path):
    src = open(path).read()
    m = re.search(r'module\s+(\w+)\s*\((.*?)\);', src, re.S)
    name = m.group(1)
    NW = int(re.search(r'input\s+wire\s*\[(\d+):0\]\s*in_data', m.group(2)).group(1)) + 1
    NO = int(re.search(r'output\s+wire\s*\[(\d+):0\]\s*out_data', m.group(2)).group(1)) + 1
    body = src[m.end():src.index('endmodule')]
    body = re.sub(r'//[^\n]*', '', body)
    stmts = [s.strip() for s in body.split(';') if s.strip()]
    val = {}      # name -> (coef dict, width, signed)
    N = None; W = None
    nadd = 0
    outs = None
    def term(t):
        t = t.strip()
        mm = re.fullmatch(r'\(\s*(\w+)\s*<<<\s*(\d+)\s*\)', t)
        if mm:
            c, w, s = val[mm.group(1)]
            assert s, 'unsigned operand ' + t
            k = int(mm.group(2))
            return {i: v << k for i, v in c.items()}
        mm = re.fullmatch(r'\w+', t)
        if mm and t in val:
            c, w, s = val[t]
            assert s, 'unsigned operand ' + t
            return dict(c)
        raise SystemExit('%s: term not understood: %r' % (path, t))
    for s in stmts:
        mm = re.fullmatch(r'wire\s+signed\s*\[(\d+):0\]\s*(\w+)\s*=\s*(.+)', s, re.S)
        if mm:
            h, nm, rhs = int(mm.group(1)), mm.group(2), mm.group(3).strip()
            wd = h + 1
            mi = re.fullmatch(r'in_data\[(\d+):(\d+)\]', rhs)
            if mi:
                hi, lo = int(mi.group(1)), int(mi.group(2))
                assert hi - lo + 1 == wd, 'input slice width'
                if W is None: W = wd
                assert wd == W and lo % W == 0
                val[nm] = ({lo // W: 1}, wd, True)
                continue
            mb = re.fullmatch(r'(.+?)\s([+-])\s(.+)', rhs)
            if mb:
                a, op, b = term(mb.group(1)), mb.group(2), term(mb.group(3))
                c = dict(a)
                for i, v in b.items():
                    c[i] = c.get(i, 0) + (v if op == '+' else -v)
                nadd += 1
            else:
                c = term(rhs)
            c = {i: v for i, v in c.items() if v}
            lo_in, hi_in = -(1 << (W - 1)), (1 << (W - 1)) - 1
            pos = sum(v for v in c.values() if v > 0); neg = sum(v for v in c.values() if v < 0)
            vmax = pos * hi_in + neg * lo_in
            vmin = pos * lo_in + neg * hi_in
            if not (-(1 << h) <= vmin and vmax <= (1 << h) - 1):
                raise SystemExit('%s: wire %s [%d:0] cannot hold its range %d .. %d' % (path, nm, h, vmin, vmax))
            # is it the narrowest width that holds the range?  (style check, reported)
            tight = h == 0 or not (-(1 << (h - 1)) <= vmin and vmax <= (1 << (h - 1)) - 1)
            val[nm] = (c, wd, True)
            val[nm + '#tight'] = tight
            continue
        mm = re.fullmatch(r'assign\s+out_data\s*=\s*\{(.*)\}', s, re.S)
        if mm:
            outs = [t.strip() for t in mm.group(1).split(',')]
            continue
        if re.fullmatch(r'assign\s+out_valid\s*=\s*in_valid', s) or re.fullmatch(r'wire\s+_unused_clk\s*=\s*clk', s):
            continue
        raise SystemExit('%s: statement not understood: %r' % (path, s))
    N = NW // W
    OW = NO // N
    assert len(outs) == N
    outs = outs[::-1]                         # {o7,...,o0}: o0 is the low slice
    for j, o in enumerate(outs):
        c, wd, sg = val[o]
        assert wd == OW, 'output width'
        for i in range(N):
            want = -1 if bin(j & i).count('1') & 1 else 1
            if c.get(i, 0) != want:
                raise SystemExit('%s: output %d is not row %d of H' % (path, j, j))
    loose = [k[:-6] for k, v in val.items() if k.endswith('#tight') and not v and not k.startswith('o')]
    return name, N, W, nadd, loose

if __name__ == '__main__':
    for p in sys.argv[1:]:
        name, N, W, nadd, loose = prove(p)
        print('PROVED  %-28s N=%-3d W=%-2d adders=%-4d wires wider than their range needs: %d %s'
              % (name, N, W, nadd, len(loose), (','.join(loose[:6]) if loose else '')))
