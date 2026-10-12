#!/usr/bin/env python3
"""run_formal3.py -- the equivalence proof in three steps, for the designs where
step A of run_formal.py (design = wide, in one go) does not finish.

The claim is the same: for ALL inputs, the combinational design D (the real file
in v/) gives the outputs of DEF, the transform written from its definition.

    WIDE = the same lines as D, every wire at the full output width, with one
           more output "fits": 1 when the value on every wire fits the exact
           width that D gives that wire.  (formal/helpers/<size>_<D>_widef_w<W>.v)

    step A1:  in WIDE, fits = 1 for all inputs.          z3 (word level: it brings
              every wire to a sum of inputs and then checks the range), with
              yices as a second opinion, limit 60 s
    step A2:  for all inputs with fits = 1,  D = WIDE.   bitwuzla (bit level)
    step B :  WIDE = DEF for all inputs.                 z3, yices as a second
              opinion (as in run_formal.py)

A1 and A2 give D = WIDE for all inputs; with B, D = DEF.  The two inferences
("if P always holds, and P implies Q, then Q always holds"; "equality is
transitive") are the only steps not done by a tool.

CONTROLS, per size: A1 on a helper that claims one wire is a bit narrower than
it is (must FAIL); A2 on a design with one wire one bit too narrow (must FAIL).

USE (from fpga/rtl):  python3 -B formal/run_formal3.py --sizes 64,8x8 --widths 8 [--timeout 300]
Results are appended to formal/RESULTS3.jsonl.
"""
import argparse
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.dont_write_bytecode = True
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)
import gen_rtl  # noqa: E402
import run_formal as rf  # noqa: E402


def query(tag, N, Wd, insts, body, files, solver, timeout):
    """insts: list of (module, instance, has_fits).  body: the assume/assert lines."""
    k = N.bit_length() - 1
    OW = Wd + k
    d = os.path.join(rf.WORK, tag)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'miter.v'), 'w') as f:
        f.write('module miter (input wire [%d:0] in_data);\n' % (N * Wd - 1))
        for n, (mod, has_fits) in enumerate(insts):
            f.write('    wire [%d:0] o%d; wire v%d; wire fits%d;\n' % (N * OW - 1, n, n, n))
            f.write('    %s g%d (.clk(1\'b0), .in_valid(1\'b1), .in_data(in_data), .out_valid(v%d), .out_data(o%d)%s);\n'
                    % (mod, n, n, n, ', .fits(fits%d)' % n if has_fits else ''))
        f.write('    always @* begin\n%s    end\nendmodule\n' % body)
    with open(os.path.join(d, 'miter.ys'), 'w') as f:
        f.write('read_verilog -formal miter.v %s\n' % ' '.join(files))
        f.write('hierarchy -top miter\nproc\nflatten\nasync2sync\nopt_clean\nwrite_smt2 -wires miter.smt2\n')
    st, t1, out = rf.run([rf.BIN + '/yosys', '-q', '-l', 'yosys.log', 'miter.ys'], 300, d)
    if st != 'rc0':
        return 'YOSYS-' + st, t1
    st, t2, out = rf.run([rf.BIN + '/yosys-smtbmc', '-s', solver, '-t', '1', '--noprogress', 'miter.smt2'], timeout, d)
    with open(os.path.join(d, 'smtbmc_%s.log' % solver), 'w') as f:
        f.write(out)
    if st == 'TIMEOUT':
        return 'TIMEOUT', t2
    m = re.search(r'Status: (\w+)', out)
    return (m.group(1) if m else 'UNKNOWN-' + st), t2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sizes', default='64,8x8')
    ap.add_argument('--widths', default='8')
    ap.add_argument('--timeout', type=int, default=300)
    ap.add_argument('--designs', default='')
    ap.add_argument('--no-controls', action='store_true')
    a = ap.parse_args()
    only = set(a.designs.split(',')) if a.designs else None
    os.makedirs(rf.WORK, exist_ok=True)
    os.makedirs(rf.HELP, exist_ok=True)
    res = open(os.path.join(HERE, 'RESULTS3.jsonl'), 'a')

    def record(**kw):
        kw['when'] = time.strftime('%Y-%m-%d %H:%M:%S %Z')
        res.write(json.dumps(kw) + '\n')
        res.flush()
        print(' '.join('%s=%s' % (k, v) for k, v in kw.items() if k != 'when'), flush=True)

    for size in a.sizes.split(','):
        for Wd in [int(w) for w in a.widths.split(',')]:
            first = True
            for d in gen_rtl.build_designs():
                if d['size'] != size or (only and d['design'] not in only):
                    continue
                lines, outs = gen_rtl.parse_text(d['text'])
                c = gen_rtl.Circuit(lines, outs, d['source'])
                N = c.N
                base = '%s_%s' % (size, d['design'])
                real = os.path.join(ROOT, 'v', '%s_c_w%d.v' % (base, Wd))
                real_mod = 'wht_%s_c_w%d' % (base, Wd)
                wide_mod = 'widef_%s_w%d' % (base, Wd)
                wide = os.path.join(rf.HELP, '%s_widef_w%d.v' % (base, Wd))
                with open(wide, 'w') as f:
                    f.write(c.verilog(Wd, 'wide', wide_mod, note=d['note'], fits=True))
                deff = os.path.join(ROOT, 'v', '%d_def_c_w%d.v' % (N, Wd))
                def_mod = 'wht_%d_def_c_w%d' % (N, Wd)
                common = dict(size=size, design=d['design'], W=Wd)
                v, t = query('%s_w%d_A1' % (base, Wd), N, Wd, [(wide_mod, True)],
                             '        assert (fits0);\n', [wide], 'z3', a.timeout)
                record(step='A1', claim='every wire of wide fits its exact width', solver='z3', verdict=v,
                       seconds=round(t, 2), **common)
                v, t = query('%s_w%d_A1' % (base, Wd), N, Wd, [(wide_mod, True)],
                             '        assert (fits0);\n', [wide], 'yices', min(a.timeout, 60))
                record(step='A1', claim='every wire of wide fits its exact width', solver='yices', verdict=v,
                       seconds=round(t, 2), **common)
                v, t = query('%s_w%d_A2' % (base, Wd), N, Wd, [(real_mod, False), (wide_mod, True)],
                             '        assume (fits1);\n        assert (o0 == o1);\n', [real, wide], 'bitwuzla', a.timeout)
                record(step='A2', claim='design = wide wherever every wire fits', solver='bitwuzla', verdict=v,
                       seconds=round(t, 2), **common)
                v, t = query('%s_w%d_B' % (base, Wd), N, Wd, [(wide_mod, True), (def_mod, False)],
                             '        assert (o0 == o1);\n', [wide, deff], 'z3', a.timeout)
                record(step='B', claim='wide = definition', solver='z3', verdict=v, seconds=round(t, 2), **common)
                v, t = query('%s_w%d_B' % (base, Wd), N, Wd, [(wide_mod, True), (def_mod, False)],
                             '        assert (o0 == o1);\n', [wide, deff], 'yices', min(a.timeout, 30))
                record(step='B', claim='wide = definition', solver='yices', verdict=v, seconds=round(t, 2), **common)
                if v != 'PASSED':
                    OW = Wd + c.k
                    npass, tsum, worst = 0, 0.0, 'PASSED'
                    for j in range(N):
                        hi, lo = j * OW + OW - 1, j * OW
                        v, t = query('%s_w%d_B1' % (base, Wd), N, Wd, [(wide_mod, True), (def_mod, False)],
                                     '        assert (o0[%d:%d] == o1[%d:%d]);\n' % (hi, lo, hi, lo),
                                     [wide, deff], 'yices', min(a.timeout, 30))
                        tsum += t
                        if v == 'PASSED':
                            npass += 1
                        else:
                            worst = v
                    record(step='B', claim='wide = definition, one output at a time', solver='yices-per-output',
                           verdict=worst, outputs_passed='%d of %d' % (npass, N), seconds=round(tsum, 2), **common)
                if first and not a.no_controls:
                    first = False
                    wdm = c.widths(Wd)
                    cands = [n for n, _, _ in c.adders if wdm[n] < Wd + c.k]
                    node = cands[len(cands) // 2]
                    w0 = wdm[node]
                    OW = Wd + c.k
                    # control A1: the helper claims that the wire fits one bit less
                    txt = open(wide).read()
                    pat = 'wire f_%s = (n_%s[%d:%d] == {%d{n_%s[%d]}});' % (node, node, OW - 1, w0 - 1, OW - w0 + 1, node, w0 - 1)
                    assert pat in txt, pat
                    bad = os.path.join(rf.WORK, '%s_w%d_ctlA1.v' % (base, Wd))
                    with open(bad, 'w') as f:
                        f.write(txt.replace(pat, 'wire f_%s = (n_%s[%d:%d] == {%d{n_%s[%d]}});'
                                            % (node, node, OW - 1, w0 - 2, OW - w0 + 2, node, w0 - 2))
                                .replace('module ' + wide_mod, 'module bad_' + wide_mod))
                    v, t = query('%s_w%d_ctlA1' % (base, Wd), N, Wd, [('bad_' + wide_mod, True)],
                                 '        assert (fits0);\n', [bad], 'z3', a.timeout)
                    record(step='control-A1', claim='wire n_%s fits %d bits, one fewer than it needs (must FAIL)' % (node, w0 - 1),
                           solver='z3', verdict=v, seconds=round(t, 2), **common)
                    # control A2: the design with that wire one bit too narrow
                    txt = open(real).read()
                    pat = 'wire signed [%d:0] n_%s =' % (w0 - 1, node)
                    assert pat in txt
                    bad = os.path.join(rf.WORK, '%s_w%d_ctlA2.v' % (base, Wd))
                    with open(bad, 'w') as f:
                        f.write(txt.replace(pat, 'wire signed [%d:0] n_%s =' % (w0 - 2, node))
                                .replace('module ' + real_mod, 'module bad_' + real_mod))
                    v, t = query('%s_w%d_ctlA2' % (base, Wd), N, Wd, [('bad_' + real_mod, False), (wide_mod, True)],
                                 '        assume (fits1);\n        assert (o0 == o1);\n', [bad, wide], 'bitwuzla', a.timeout)
                    record(step='control-A2', claim='design with wire n_%s one bit too narrow = wide wherever every wire fits (must FAIL)' % node,
                           solver='bitwuzla', verdict=v, seconds=round(t, 2), **common)


if __name__ == '__main__':
    main()
