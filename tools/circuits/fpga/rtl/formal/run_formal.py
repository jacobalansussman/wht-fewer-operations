#!/usr/bin/env python3
"""run_formal.py -- formal equivalence proofs for the Verilog designs.

WHAT IS PROVED, for a design D at width W (D is the file v/<size>_<D>_c_w<W>.v,
the combinational variant, exactly as written by gen_rtl.py):

    for ALL values of the N*W input bits,  out_data of D  =  out_data of DEF,

where DEF is v/<N>_def_c_w<W>.v: the transform written from its definition,
one sum of N signed terms per output.  The textbook design is proved equal to
DEF in the same way, so every design is equal to the textbook on all inputs.

HOW.  A direct miter (design against textbook) was tried first and no engine
finished it, even at 8 points and 8 bits: yosys "sat" (MiniSat), ABC "cec",
and the SMT solvers bitwuzla, yices, boolector and z3 through SymbiYosys all
ran out of time (150 to 600 seconds).  Comparing two different networks of
adders bit by bit is a known hard case.  So each proof is made of two steps
that the solvers do finish, with a helper in between:

    WIDE = the same lines as D, in the same order, but every wire has the full
           output width (no truncation anywhere), and a doubling is written as
           two additions.  File formal/helpers/<size>_<D>_wide_w<W>.v, written
           by gen_rtl.py (variant "wide").

    step A:  D = WIDE     Same structure, different widths.  This step is where
                          the exact widths of D are justified: it fails if any
                          wire of D is too narrow for some input.
                          Solver: bitwuzla (bit level).
    step B:  WIDE = DEF   Sums modulo 2^(W + log2 N) only.
                          Solver: z3 (it brings both sides to the same
                          normal form); yices is run as a second opinion
                          with a limit of 30 seconds (it is a check of
                          z3, not a part of the proof; where it runs out
                          of time, yices is asked the same question
                          once per output, which it does finish).

D = DEF follows from A and B because both hold for all inputs.  That last
step (equality is transitive) is the only one not done by a tool.

Each step: yosys reads the real Verilog files and a three-line miter module
with "assert (a == b)", writes an SMT-LIB file (write_smt2), and yosys-smtbmc
asks the solver whether any input violates the assertion.  PASSED = none.

CONTROLS.  For every size the script also runs both steps on a deliberately
wrong design (one adder narrowed by one bit for step A; one sign changed for
step B) and requires the solver to report FAILED with a counterexample.

USE (from fpga/rtl):
    python3 -B formal/run_formal.py [--sizes 8,16] [--widths 8,12,16] [--timeout 300]
Results are appended to formal/RESULTS.jsonl; formal/summarize.py prints the table.
"""
import argparse
import json
import os
import re
import signal
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.dont_write_bytecode = True
sys.path.insert(0, ROOT)
import gen_rtl  # noqa: E402

BIN = os.path.join(os.environ.get('OSS_CAD_SUITE', '/opt/oss-cad-suite'), 'bin')      # the unpacked oss-cad-suite
WORK = os.path.join(ROOT, 'work', 'formal')
HELP = os.path.join(HERE, 'helpers')
ENV = dict(os.environ, PATH=BIN + ':' + os.environ.get('PATH', ''))


def run(cmd, timeout, cwd):
    """Run cmd; returns (status, seconds, output).  Kills the whole process group on timeout."""
    t0 = time.time()
    p = subprocess.Popen(cmd, cwd=cwd, env=ENV, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         start_new_session=True, universal_newlines=True)
    try:
        out, _ = p.communicate(timeout=timeout)
        st = 'rc%d' % p.returncode
    except subprocess.TimeoutExpired:
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        out, _ = p.communicate()
        st = 'TIMEOUT'
    return st, time.time() - t0, out


def miter(tag, N, Wd, mod_a, mod_b, files, solver, timeout, only_output=None):
    """Is out_data of mod_a equal to out_data of mod_b for all inputs?  Returns (verdict, seconds).
    With only_output = j the assertion is about output j alone."""
    k = N.bit_length() - 1
    OW = Wd + k
    d = os.path.join(WORK, tag)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'miter.v'), 'w') as f:
        f.write('module miter (input wire [%d:0] in_data);\n' % (N * Wd - 1))
        f.write('    wire [%d:0] a, b;\n    wire va, vb;\n' % (N * OW - 1))
        f.write('    %s ga (.clk(1\'b0), .in_valid(1\'b1), .in_data(in_data), .out_valid(va), .out_data(a));\n' % mod_a)
        f.write('    %s gb (.clk(1\'b0), .in_valid(1\'b1), .in_data(in_data), .out_valid(vb), .out_data(b));\n' % mod_b)
        if only_output is None:
            f.write('    always @* assert (a == b);\nendmodule\n')
        else:
            hi, lo = only_output * OW + OW - 1, only_output * OW
            f.write('    always @* assert (a[%d:%d] == b[%d:%d]);\nendmodule\n' % (hi, lo, hi, lo))
    with open(os.path.join(d, 'miter.ys'), 'w') as f:
        f.write('read_verilog -formal miter.v %s\n' % ' '.join(files))
        f.write('hierarchy -top miter\nproc\nflatten\nasync2sync\nopt_clean\nwrite_smt2 -wires miter.smt2\n')
    st, t1, out = run([BIN + '/yosys', '-q', '-l', 'yosys.log', 'miter.ys'], 300, d)
    if st != 'rc0':
        return 'YOSYS-' + st, t1
    st, t2, out = run([BIN + '/yosys-smtbmc', '-s', solver, '-t', '1', '--noprogress', 'miter.smt2'], timeout, d)
    with open(os.path.join(d, 'smtbmc_%s.log' % solver), 'w') as f:
        f.write(out)
    if st == 'TIMEOUT':
        return 'TIMEOUT', t2
    m = re.search(r'Status: (\w+)', out)
    return (m.group(1) if m else 'UNKNOWN-' + st), t2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sizes', default='8,16')
    ap.add_argument('--widths', default='8')
    ap.add_argument('--timeout', type=int, default=300)
    ap.add_argument('--designs', default='')
    ap.add_argument('--no-controls', action='store_true')
    ap.add_argument('--second-only', action='store_true', help='only the yices second opinion on step B')
    a = ap.parse_args()
    sizes = a.sizes.split(',')
    widths = [int(w) for w in a.widths.split(',')]
    only = set(a.designs.split(',')) if a.designs else None
    os.makedirs(WORK, exist_ok=True)
    os.makedirs(HELP, exist_ok=True)
    res = open(os.path.join(HERE, 'RESULTS.jsonl'), 'a')

    def record(**kw):
        kw['when'] = time.strftime('%Y-%m-%d %H:%M:%S %Z')
        res.write(json.dumps(kw) + '\n')
        res.flush()
        print(' '.join('%s=%s' % (k, v) for k, v in kw.items() if k != 'when'), flush=True)

    designs = gen_rtl.build_designs()
    for size in sizes:
        for Wd in widths:
            first = True
            for d in designs:
                if d['size'] != size or (only and d['design'] not in only):
                    continue
                lines, outs = gen_rtl.parse_text(d['text'])
                c = gen_rtl.Circuit(lines, outs, d['source'])
                N = c.N
                nsize = str(N)
                base = '%s_%s' % (size, d['design'])
                real = os.path.join(ROOT, 'v', '%s_c_w%d.v' % (base, Wd))
                real_mod = 'wht_%s_c_w%d' % (base, Wd)
                wide_mod = 'wide_%s_w%d' % (base, Wd)
                wide = os.path.join(HELP, '%s_wide_w%d.v' % (base, Wd))
                with open(wide, 'w') as f:
                    f.write(c.verilog(Wd, 'wide', wide_mod, note=d['note']))
                deff = os.path.join(ROOT, 'v', '%s_def_c_w%d.v' % (nsize, Wd))
                def_mod = 'wht_%s_def_c_w%d' % (nsize, Wd)
                if not a.second_only:
                    va, ta = miter('%s_w%d_A' % (base, Wd), N, Wd, real_mod, wide_mod, [real, wide], 'bitwuzla', a.timeout)
                    record(size=size, design=d['design'], W=Wd, step='A', claim='design = wide', solver='bitwuzla',
                           verdict=va, seconds=round(ta, 2))
                    vb, tb = miter('%s_w%d_B' % (base, Wd), N, Wd, wide_mod, def_mod, [wide, deff], 'z3', a.timeout)
                    record(size=size, design=d['design'], W=Wd, step='B', claim='wide = definition', solver='z3',
                           verdict=vb, seconds=round(tb, 2))
                vb2, tb2 = miter('%s_w%d_B' % (base, Wd), N, Wd, wide_mod, def_mod, [wide, deff], 'yices', min(a.timeout, 30))
                record(size=size, design=d['design'], W=Wd, step='B', claim='wide = definition', solver='yices',
                       verdict=vb2, seconds=round(tb2, 2))
                if vb2 != 'PASSED':
                    # the same question asked once per output; all N answers together are the same claim
                    npass, tsum, worst = 0, 0.0, 'PASSED'
                    for j in range(N):
                        v, t = miter('%s_w%d_B1' % (base, Wd), N, Wd, wide_mod, def_mod, [wide, deff], 'yices',
                                     min(a.timeout, 30), only_output=j)
                        tsum += t
                        if v == 'PASSED':
                            npass += 1
                        else:
                            worst = v
                    record(size=size, design=d['design'], W=Wd, step='B', claim='wide = definition, one output at a time',
                           solver='yices-per-output', verdict=worst, outputs_passed='%d of %d' % (npass, N),
                           seconds=round(tsum, 2))
                if first and not a.no_controls and not a.second_only:
                    first = False
                    # control for step A: the real file with one adder one bit too narrow
                    txt = open(real).read()
                    cands = [(c.widths(Wd)[n], n) for n, _, _ in c.adders if c.widths(Wd)[n] < Wd + c.k]
                    if not cands:
                        cands = [(c.widths(Wd)[n], n) for n, _, _ in c.adders]
                    w0, node = cands[len(cands) // 2]
                    pat = 'wire signed [%d:0] n_%s =' % (w0 - 1, node)
                    assert pat in txt
                    bad = os.path.join(WORK, '%s_w%d_ctlA.v' % (base, Wd))
                    with open(bad, 'w') as f:
                        f.write(txt.replace(pat, 'wire signed [%d:0] n_%s =' % (w0 - 2, node))
                                .replace('module ' + real_mod, 'module bad_' + real_mod))
                    v, t = miter('%s_w%d_ctlA' % (base, Wd), N, Wd, 'bad_' + real_mod, wide_mod, [bad, wide],
                                 'bitwuzla', a.timeout)
                    record(size=size, design=d['design'], W=Wd, step='control-A',
                           claim='design with wire n_%s one bit too narrow = wide (must FAIL)' % node,
                           solver='bitwuzla', verdict=v, seconds=round(t, 2))
                    # control for step B: the wide helper with one sign changed
                    txt = open(wide).read()
                    node = c.adders[len(c.adders) // 2][0]
                    m = re.search(r'(wire signed \[\d+:0\] n_%s = \S+ )([-+])' % re.escape(node), txt)
                    assert m
                    bad = os.path.join(WORK, '%s_w%d_ctlB.v' % (base, Wd))
                    with open(bad, 'w') as f:
                        f.write((txt[:m.start(2)] + ('-' if m.group(2) == '+' else '+') + txt[m.end(2):])
                                .replace('module ' + wide_mod, 'module bad_' + wide_mod))
                    v, t = miter('%s_w%d_ctlB' % (base, Wd), N, Wd, 'bad_' + wide_mod, def_mod, [bad, deff],
                                 'z3', a.timeout)
                    record(size=size, design=d['design'], W=Wd, step='control-B',
                           claim='wide with one sign changed at n_%s = definition (must FAIL)' % node,
                           solver='z3', verdict=v, seconds=round(t, 2))


if __name__ == '__main__':
    main()
