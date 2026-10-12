#!/usr/bin/env python3
"""run_seq.py -- formal proofs for the variants with registers (p, p2, r).

WHAT IS PROVED, for a variant V of a design at width W, with latency L:

    at every clock cycle from the L-th on, and for every sequence of inputs,
    out_data of V  =  out_data of the combinational variant c, L cycles earlier,
    and out_valid of V = in_valid, L cycles earlier (from the first cycle on).

Together with the proof that the combinational variant equals the definition
(run_formal.py) this says that the registered variant computes the transform.

HOW.  SymbiYosys, mode "prove" (bounded check from the start plus induction),
depth L + 1, engine smtbmc with bitwuzla.  The miter holds the two real files,
a shift register of L stages behind the combinational one, and the assertions.
No reset is assumed: data registers start with any value; the valid bits start
at 0, as the files declare.  Induction of depth L + 1 is complete here because
no register feeds back: every register value is fixed by the inputs of the last
L cycles.

CONTROL.  For every size the script also runs a damaged pipelined file (one
delay register skipped) and requires the result FAIL.

USE (from fpga/rtl):
    python3 -B formal/run_seq.py [--sizes 8,16] [--widths 8] [--timeout 300]
Results are appended to formal/RESULTS_SEQ.jsonl.
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
BIN = os.path.join(os.environ.get('OSS_CAD_SUITE', '/opt/oss-cad-suite'), 'bin')      # the unpacked oss-cad-suite
WORK = os.path.join(ROOT, 'work', 'formal_seq')
ENV = dict(os.environ, PATH=BIN + ':' + os.environ.get('PATH', ''))


def prove(tag, N, Wd, c_file, c_mod, v_file, v_mod, L, timeout):
    k = N.bit_length() - 1
    OWT = N * (Wd + k)
    d = os.path.join(WORK, tag)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'seqmiter.v'), 'w') as f:
        f.write('''module seqmiter (input wire clk, input wire in_valid, input wire [%(IW)d:0] in_data);
    wire [%(OM)d:0] a, b;
    wire va, vb;
    %(c_mod)s gc (.clk(clk), .in_valid(in_valid), .in_data(in_data), .out_valid(va), .out_data(a));
    %(v_mod)s gv (.clk(clk), .in_valid(in_valid), .in_data(in_data), .out_valid(vb), .out_data(b));
    reg [%(SH)d:0] sh;                 // the outputs of the combinational variant, delayed L cycles
    reg [%(L)d:0] dv = %(L1)d'd0;      // in_valid, delayed
    reg [7:0] cnt = 8'd0;              // cycles since the start, saturating at L
    always @(posedge clk) begin
        sh <= {sh, a};
        dv <= {dv, va};
        if (cnt < %(L)d) cnt <= cnt + 8'd1;
    end
    always @* begin
        assert (cnt <= %(L)d);
        if (cnt == %(L)d) assert (b == sh[%(SH)d:%(SL)d]);
        assert (vb == dv[%(Lm)d]);
    end
endmodule
''' % dict(IW=N * Wd - 1, OM=OWT - 1, c_mod=c_mod, v_mod=v_mod, SH=L * OWT - 1, SL=(L - 1) * OWT,
           L=L, L1=L + 1, Lm=L - 1))
    with open(os.path.join(d, 'p.sby'), 'w') as f:
        f.write('[options]\nmode prove\ndepth %d\ntimeout %d\n\n[engines]\nsmtbmc bitwuzla\n\n' % (L + 1, timeout))
        f.write('[script]\nread_verilog -formal seqmiter.v\nread_verilog %s\nread_verilog %s\n'
                % (os.path.basename(c_file), os.path.basename(v_file)))
        f.write('prep -top seqmiter\nflatten\n\n[files]\nseqmiter.v\n%s\n%s\n' % (c_file, v_file))
    t0 = time.time()
    p = subprocess.Popen([BIN + '/sby', '-f', 'p.sby'], cwd=d, env=ENV, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, start_new_session=True, universal_newlines=True)
    try:
        out, _ = p.communicate(timeout=timeout + 60)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        out, _ = p.communicate()
        out += '\nDONE (KILLED'
    with open(os.path.join(d, 'sby.out'), 'w') as f:
        f.write(out)
    m = re.findall(r'DONE \((\w+)', out)
    return (m[-1] if m else 'UNKNOWN'), time.time() - t0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sizes', default='8,16')
    ap.add_argument('--widths', default='8')
    ap.add_argument('--timeout', type=int, default=300)
    ap.add_argument('--variants', default='p,p2,r')
    ap.add_argument('--no-controls', action='store_true')
    a = ap.parse_args()
    with open(os.path.join(ROOT, 'designs.json')) as f:
        dj = json.load(f)
    os.makedirs(WORK, exist_ok=True)
    res = open(os.path.join(HERE, 'RESULTS_SEQ.jsonl'), 'a')

    def record(**kw):
        kw['when'] = time.strftime('%Y-%m-%d %H:%M:%S %Z')
        res.write(json.dumps(kw) + '\n')
        res.flush()
        print(' '.join('%s=%s' % (k, v) for k, v in kw.items() if k != 'when'), flush=True)

    for size in a.sizes.split(','):
        for Wd in [int(w) for w in a.widths.split(',')]:
            first = True
            for r in dj['designs']:
                if r['size'] != size or r['W'] != Wd:
                    continue
                c = r['files']['c']
                for vn in a.variants.split(','):
                    v = r['files'][vn]
                    tag = '%s_%s_%s_w%d' % (size, r['design'], vn, Wd)
                    verdict, t = prove(tag, r['N'], Wd, os.path.join(ROOT, c['file']), c['module'],
                                       os.path.join(ROOT, v['file']), v['module'], v['latency'], a.timeout)
                    record(size=size, design=r['design'], W=Wd, variant=vn, latency=v['latency'],
                           claim='variant = combinational variant delayed', engine='sby prove, smtbmc bitwuzla',
                           depth=v['latency'] + 1, verdict=verdict, seconds=round(t, 1))
                if first and not a.no_controls and r['reg_delay'] > 0:
                    first = False
                    v = r['files']['p']
                    txt = open(os.path.join(ROOT, v['file'])).read()
                    m = re.search(r'= (\w+_r(\d+)) [-+] \((\w+)_r(\d+) <<< 1\)', txt)
                    if m and int(m.group(4)) > 1:
                        bad = os.path.join(WORK, 'bad_%s_%s_p_w%d.v' % (size, r['design'], Wd))
                        s0 = '(%s_r%s <<< 1)' % (m.group(3), m.group(4))
                        s1 = '(%s_r%d <<< 1)' % (m.group(3), int(m.group(4)) - 1)
                        i = txt.index(s0, m.start())
                        with open(bad, 'w') as f:
                            f.write((txt[:i] + s1 + txt[i + len(s0):]).replace('module ' + v['module'], 'module bad_' + v['module']))
                        verdict, t = prove('ctl_%s_%s_p_w%d' % (size, r['design'], Wd), r['N'], Wd,
                                           os.path.join(ROOT, c['file']), c['module'], bad, 'bad_' + v['module'],
                                           v['latency'], a.timeout)
                        record(size=size, design=r['design'], W=Wd, variant='control-p', latency=v['latency'],
                               claim='p with %s taken one stage early = combinational delayed (must FAIL)' % m.group(3),
                               engine='sby prove, smtbmc bitwuzla', depth=v['latency'] + 1, verdict=verdict,
                               seconds=round(t, 1))


if __name__ == '__main__':
    main()
