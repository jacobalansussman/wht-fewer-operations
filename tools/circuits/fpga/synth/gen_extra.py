#!/usr/bin/env python3
"""gen_extra.py -- write the extra pipelined variants this measurement needs (a register after
every K-th adder level, K = 3 .. depth-1) with the generator of ../rtl, UNCHANGED
(../rtl/gen_rtl.py is only run, with its own option --variant pK), into ./v_extra/.
The files of ../rtl/v (c, p, p2, r) are not touched.

Then every new file is simulated against the combinational file of ../rtl/v, which is
checked and proved there: the pipelined output must equal the combinational output delayed by the
latency, on 4,000 random input vectors and 8 corner vectors, with out_valid checked too.

    python3 -B gen_extra.py            write and check everything
Results: v_extra/CHECK.txt (one line per file).  Standard library only; uses iverilog/vvp.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RTL = os.path.join(os.path.dirname(HERE), 'rtl')
REPO = os.path.normpath(os.path.join(HERE, '..', '..', '..', '..'))      # the top folder of the repository
BIN = os.path.join(os.environ.get('OSS_CAD_SUITE', '/opt/oss-cad-suite'), 'bin')      # the unpacked oss-cad-suite
OUT = os.path.join(HERE, 'v_extra')
TMP = os.path.join(HERE, 'work', 'sim_extra')

# size, design, widths, list of K
WANT = [
    ('8', 'cfl1994', (8, 12, 16), (3, 4)),
    ('8', 'ar2023', (8, 12, 16), (3, 4, 5)),
    ('8', 'ours', (8, 12, 16), (3, 4, 5)),
    ('16', 'textbook', (8, 12, 16), (3,)),
    ('16', 'cfl1994', (8, 12, 16), (3, 4, 5, 6, 7)),
    ('16', 'ours', (8, 12, 16), (3, 4, 5, 6, 7)),
    ('64', 'textbook', (8,), (3,)),
    ('64', 'cfl1994', (8,), (3, 4, 6)),
    ('64', 'ours', (8,), (3, 4, 6)),
    ('8x8', 'ours', (8,), (3, 4, 6)),
]


def src_path(s):
    return os.path.join(REPO, s)


def tb(modp, modc, nw, no, lat, nvec=4000):
    words = (nw + 31) // 32
    t = []
    t.append('`timescale 1ns/1ps')
    t.append('module tb;')
    t.append('  reg clk = 0; reg [%d:0] x = 0; reg iv = 0;' % (nw - 1))
    t.append('  wire [%d:0] yc, yp; wire vc, vp;' % (no - 1))
    t.append('  %s c (.clk(clk), .in_valid(iv), .in_data(x), .out_valid(vc), .out_data(yc));' % modc)
    t.append('  %s p (.clk(clk), .in_valid(iv), .in_data(x), .out_valid(vp), .out_data(yp));' % modp)
    t.append('  reg [%d:0] dl [0:%d]; reg dv [0:%d];' % (no - 1, lat, lat))
    t.append('  integer i, n = 0, errs = 0, seed = 20261011; reg [%d:0] r;' % (words * 32 - 1))
    t.append('  initial for (i = 0; i <= %d; i = i + 1) dv[i] = 0;' % lat)
    t.append('  always @(posedge clk) begin')
    t.append('    dl[0] <= yc; dv[0] <= vc;')
    t.append('    for (i = 1; i <= %d; i = i + 1) begin dl[i] <= dl[i-1]; dv[i] <= dv[i-1]; end' % lat)
    t.append('  end')
    t.append('  always @(negedge clk) begin')
    t.append('    if (n > %d) begin' % (lat + 2))
    t.append('      if (yp !== dl[%d] || vp !== dv[%d]) begin errs = errs + 1; if (errs < 4) $display("MISMATCH n=%%0d", n); end' % (lat - 1, lat - 1))
    t.append('    end')
    t.append('    for (i = 0; i < %d; i = i + 1) r[i*32 +: 32] = $random(seed);' % words)
    t.append('    case (n)')
    t.append('      10: x <= {%d{1\'b1}};' % nw)
    t.append('      11: x <= {%d{1\'b0}};' % nw)
    t.append('      12: x <= {%d{2\'b01}};' % (nw // 2))
    t.append('      13: x <= {%d{2\'b10}};' % (nw // 2))
    t.append('      default: x <= r[%d:0];' % (nw - 1))
    t.append('    endcase')
    t.append('    iv <= r[5];')
    t.append('    n = n + 1;')
    t.append('    if (n == %d) begin $display("RESULT vectors=%%0d errors=%%0d", n, errs); $finish; end' % (nvec + 8))
    t.append('  end')
    t.append('  always #5 clk = ~clk;')
    t.append('endmodule')
    return '\n'.join(t) + '\n'


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(TMP, exist_ok=True)
    env = dict(os.environ, PATH=BIN + ':' + os.environ['PATH'])
    d = json.load(open(os.path.join(RTL, 'designs.json')))
    rows = {(x['size'], x['design'], x['W']): x for x in d['designs']}
    lines = []
    bad = 0
    for size, design, widths, Ks in WANT:
        for W in widths:
            row = rows[(size, design, W)]
            depth = row['depth']
            for K in Ks:
                if K >= depth:
                    continue
                bn = '%s_%s_p%d_w%d' % (size, design, K, W)
                out = os.path.join(OUT, bn + '.v')
                p = subprocess.run([sys.executable, '-B', os.path.join(RTL, 'gen_rtl.py'), src_path(row['source']),
                                    '--variant', 'p%d' % K, '--width', str(W), '--name', 'wht_' + bn, '-o', out],
                                   capture_output=True, text=True, cwd=TMP)
                if p.returncode != 0:
                    lines.append('%s  GENERATOR FAILED: %s' % (bn, p.stderr.strip()[-200:]))
                    bad += 1
                    continue
                met = json.loads(p.stderr.strip().splitlines()[-1])
                lat = -(-depth // K)
                nw = row['N'] * W
                no = row['N'] * row['OW']
                cfile = os.path.join(RTL, row['files']['c']['file'])
                cmod = row['files']['c']['module']
                tbf = os.path.join(TMP, bn + '_tb.v')
                open(tbf, 'w').write(tb('wht_' + bn, cmod, nw, no, lat))
                vvp = os.path.join(TMP, bn + '.vvp')
                c1 = subprocess.run(['iverilog', '-g2005', '-o', vvp, tbf, out, cfile], capture_output=True, text=True, env=env)
                if c1.returncode != 0:
                    lines.append('%s  IVERILOG FAILED: %s' % (bn, (c1.stderr + c1.stdout).strip()[-300:]))
                    bad += 1
                    continue
                c2 = subprocess.run(['vvp', '-n', vvp], capture_output=True, text=True, env=env)
                res = [l for l in c2.stdout.splitlines() if l.startswith('RESULT')]
                ok = bool(res) and res[0].endswith('errors=0')
                if not ok:
                    bad += 1
                os.remove(vvp)
                lines.append('%-22s latency %d  reg bits: after adders %d + delay %d = %d   %s  %s' % (
                    bn, lat, met.get('reg_after_adders', -1), met.get('reg_delay', -1), met.get('reg_data', -1),
                    res[0] if res else 'NO RESULT', 'ok' if ok else 'FAIL'))
                print(lines[-1], flush=True)
    open(os.path.join(OUT, 'CHECK.txt'), 'w').write('\n'.join(lines) + '\n')
    print('files: %d, failures: %d' % (len(lines), bad))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
