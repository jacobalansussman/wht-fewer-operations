#!/usr/bin/env python3
"""postsim.py -- is the netlist that was placed and routed still the design?

For a job folder work/<group>/<tag>/ (written by run.py) this simulates two things side by side
with the same random serial input:
    A  the harness and the design as Verilog source (harness.v + the design file)
    B  the synthesised, flattened netlist that nextpnr received (top.json, read back by yosys and
       written as Verilog of SB_LUT4 / SB_CARRY / SB_DFF cells, simulated with yosys's cell models)
and compares the serial output bit `sout` on every clock after the registers have filled.
`sout` is the last bit of the signature register, so it depends on every output bit of the design.

    python3 -B postsim.py work/g8/8_ours_c_w8 work/g8/8_textbook_p_w8 ...
Prints one line per folder.  Uses yosys, iverilog, vvp; one process at a time.
"""
import os
import re
import subprocess
import sys

SUITE = os.environ.get('OSS_CAD_SUITE', '/opt/oss-cad-suite')      # the unpacked oss-cad-suite
BIN = os.path.join(SUITE, 'bin')
CELLS = os.path.join(SUITE, 'share', 'yosys', 'ice40', 'cells_sim.v')
HERE = os.path.dirname(os.path.abspath(__file__))
NCLK = 30000


def main():
    env = dict(os.environ, PATH=BIN + ':' + os.environ['PATH'])
    bad = 0
    for wd in sys.argv[1:]:
        wd = os.path.abspath(wd)
        tag = os.path.basename(wd)
        ys = open(os.path.join(wd, 'synth.ys')).read()
        srcs = re.findall(r'^read_verilog\s+(?:-I\S+\s+)*(\S+)\s*$', ys, re.M)
        incs = re.findall(r'-I(\S+)', ys)
        net = os.path.join(wd, 'post.v')
        p = subprocess.run(['yosys', '-q', '-p', 'read_json %s; rename top top_net; write_verilog -noattr %s' % (os.path.join(wd, 'top.json'), net)],
                           capture_output=True, text=True, env=env)
        if p.returncode != 0:
            print(tag, 'yosys failed', p.stderr[-200:])
            bad += 1
            continue
        hs = open(os.path.join(wd, 'harness.v')).read()
        nw = int(re.search(r'reg \[(\d+):0\] sr;', hs).group(1)) + 1
        no = int(re.search(r'reg \[(\d+):0\] acc;', hs).group(1))
        warm = nw + no + 40
        tb = os.path.join(wd, 'post_tb.v')
        open(tb, 'w').write('''`timescale 1ns/1ps
module tb;
  reg clk = 0, sin = 0, vin = 0; wire a, b;
  top A (.clk(clk), .sin(sin), .vin(vin), .sout(a));
  top_net B (.clk(clk), .sin(sin), .vin(vin), .sout(b));
  integer n = 0, errs = 0, xs = 0, seed = 7, ones = 0;
  always @(negedge clk) begin
    if (n > %d) begin
      if (a === 1'bx || b === 1'bx) xs = xs + 1;
      else if (a !== b) errs = errs + 1;
      if (a === 1'b1) ones = ones + 1;
    end
    sin <= $random(seed); vin <= ($random(seed) %% 8) != 0;
    n = n + 1;
    if (n == %d) begin $display("RESULT clocks=%%0d compared=%%0d mismatches=%%0d unknown=%%0d ones=%%0d", n, n - %d - 1, errs, xs, ones); $finish; end
  end
  always #5 clk = ~clk;
endmodule
''' % (warm, NCLK, warm))
        vvp = os.path.join(wd, 'post.vvp')
        cmd = ['iverilog', '-g2005', '-DNO_ICE40_DEFAULT_ASSIGNMENTS', '-o', vvp] + ['-I' + i for i in incs] + [tb, net, CELLS] + srcs
        c1 = subprocess.run(cmd, capture_output=True, text=True, env=env)
        if c1.returncode != 0:
            print(tag, 'iverilog failed', (c1.stderr + c1.stdout)[-400:])
            bad += 1
            continue
        c2 = subprocess.run(['vvp', '-n', vvp], capture_output=True, text=True, env=env)
        res = [l for l in c2.stdout.splitlines() if l.startswith('RESULT')]
        os.remove(vvp)
        os.remove(net)
        ok = bool(res) and ' mismatches=0 ' in res[0] and ' unknown=0 ' in res[0]
        if not ok:
            bad += 1
        print('%-28s %s  %s' % (tag, res[0] if res else 'NO RESULT ' + c2.stdout[-200:], 'ok' if ok else 'FAIL'), flush=True)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
