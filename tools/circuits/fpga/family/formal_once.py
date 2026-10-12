#!/usr/bin/env python3
"""formal_once.py -- ONE try, 5 minutes in all, at an equivalence proof of the 16-point pair
(textbook and family, combinational, W = 9).  The method is that of ../rtl/formal/run_formal.py:
a direct miter of two different adder networks is a known hard case, so the proof goes through a
helper WIDE (the same lines, every wire at the full output width, doublings as repeated addition;
gen_rtl.py variant "wide"):
    A-family    family   = WIDE(family)        bitwuzla   (justifies the exact widths)
    A-textbook  textbook = WIDE(textbook)      bitwuzla
    B           WIDE(family) = WIDE(textbook)  z3         (sums modulo 2^13 only)
    control     family with one wire one bit too narrow = WIDE(family)   must FAIL
Each step: yosys write_smt2 of a miter with "assert (a == b)", then yosys-smtbmc -t 1.
Results: formal/RESULT.txt.
"""
import os
import re
import signal
import subprocess
import sys
import time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fam  # noqa: E402

BIN = os.path.join(os.environ.get('OSS_CAD_SUITE', '/opt/oss-cad-suite'), 'bin')      # the unpacked oss-cad-suite
ENV = dict(os.environ, PATH=BIN + ':' + os.environ.get('PATH', ''))
WORK = os.path.join(HERE, 'formal')
N, W = 16, 9
OW = W + 4
T0 = time.time()
LIMIT = 300


def run(cmd, cwd):
    left = LIMIT - (time.time() - T0)
    if left <= 1:
        return 'NO-TIME-LEFT', 0.0, ''
    t0 = time.time()
    p = subprocess.Popen(cmd, cwd=cwd, env=ENV, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         start_new_session=True, universal_newlines=True)
    try:
        out, _ = p.communicate(timeout=left)
        st = 'rc%d' % p.returncode
    except subprocess.TimeoutExpired:
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        out, _ = p.communicate()
        st = 'TIMEOUT'
    return st, time.time() - t0, out


def miter(tag, mod_a, mod_b, files, solver):
    d = os.path.join(WORK, tag)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'miter.v'), 'w') as f:
        f.write('module miter (input wire [%d:0] in_data);\n' % (N * W - 1))
        f.write('    wire [%d:0] a, b;\n    wire va, vb;\n' % (N * OW - 1))
        f.write('    %s ga (.clk(1\'b0), .in_valid(1\'b1), .in_data(in_data), .out_valid(va), .out_data(a));\n' % mod_a)
        f.write('    %s gb (.clk(1\'b0), .in_valid(1\'b1), .in_data(in_data), .out_valid(vb), .out_data(b));\n' % mod_b)
        f.write('    always @* assert (a == b);\nendmodule\n')
    with open(os.path.join(d, 'miter.ys'), 'w') as f:
        f.write('read_verilog -formal miter.v %s\n' % ' '.join(files))
        f.write('hierarchy -top miter\nproc\nflatten\nasync2sync\nopt_clean\nwrite_smt2 -wires miter.smt2\n')
    st, t1, out = run([BIN + '/yosys', '-q', '-l', 'yosys.log', 'miter.ys'], d)
    if st != 'rc0':
        return 'YOSYS-' + st, t1
    st, t2, out = run([BIN + '/yosys-smtbmc', '-s', solver, '-t', '1', '--noprogress', 'miter.smt2'], d)
    with open(os.path.join(d, 'smtbmc_%s.log' % solver), 'w') as f:
        f.write(out)
    if st in ('TIMEOUT', 'NO-TIME-LEFT'):
        return st, t2
    m = re.search(r'Status: (\w+)', out)
    return (m.group(1) if m else 'UNKNOWN-' + st), t2


def main():
    os.makedirs(WORK, exist_ok=True)
    res = []
    wide = {}
    for d in ('family', 'textbook'):
        c = fam.load(N, d)
        wide[d] = os.path.join(WORK, '16_%s_wide_w9.v' % d)
        with open(wide[d], 'w') as f:
            f.write(c.verilog(W, 'wide', 'wide_16_%s_w9' % d))
    real = dict((d, os.path.join(HERE, 'v', '16_%s_c_w9.v' % d)) for d in ('family', 'textbook'))
    for d in ('family', 'textbook'):
        v, t = miter('A_' + d, 'wht_16_%s_c_w9' % d, 'wide_16_%s_w9' % d, [real[d], wide[d]], 'bitwuzla')
        res.append('A-%-9s %s = WIDE(%s), bitwuzla: %s in %.1f s' % (d, d, d, v, t))
        print(res[-1], flush=True)
    v, t = miter('B', 'wide_16_family_w9', 'wide_16_textbook_w9', [wide['family'], wide['textbook']], 'z3')
    res.append('B           WIDE(family) = WIDE(textbook), z3: %s in %.1f s' % (v, t))
    print(res[-1], flush=True)
    # control: one adder of the family one bit too narrow
    c = fam.load(N, 'family')
    wd = c.widths(W)
    cands = [(wd[n], n) for n, _, _ in c.adders if wd[n] < OW]
    w0, node = cands[len(cands) // 2]
    txt = open(real['family']).read()
    pat = 'wire signed [%d:0] n_%s =' % (w0 - 1, node)
    assert pat in txt
    bad = os.path.join(WORK, '16_family_bad_w9.v')
    with open(bad, 'w') as f:
        f.write(txt.replace(pat, 'wire signed [%d:0] n_%s =' % (w0 - 2, node))
                .replace('module wht_16_family_c_w9', 'module bad_wht_16_family_c_w9'))
    v, t = miter('control', 'bad_wht_16_family_c_w9', 'wide_16_family_w9', [bad, wide['family']], 'bitwuzla')
    res.append('control     family with wire n_%s one bit too narrow = WIDE(family) (must be FAILED), bitwuzla: %s in %.1f s'
               % (node, v, t))
    print(res[-1], flush=True)
    res.append('total %.1f s of the %d s allowed; %s' % (time.time() - T0, LIMIT, time.strftime('%Y-%m-%d %H:%M:%S %Z')))
    with open(os.path.join(WORK, 'RESULT.txt'), 'w') as f:
        f.write('\n'.join(res) + '\n')


if __name__ == '__main__':
    main()
