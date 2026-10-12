#!/usr/bin/env python3
"""fam.py -- the family in hardware: the three designs at 16, 32, 64, 128 and 256 points.
Standard library only.  Run with  python3 -B fam.py <step>.

  circuits   write circuits/<N>_<design>.txt and check each with tools/circuits/slp.py
  paper      print the paper table (adders, depth, adder bits, register bits) and write paper.json
  rtl        write v/<N>_<design>_<c|p>_w<W>.v with ../rtl/gen_rtl.py, the null cores and the wrappers
  vectors N W   write the test vectors and the bench for one size and width (../rtl/sim/golden.py)

Designs:
  textbook   k layers of N/2 butterflies (a+b, a-b): N k adders.
  cfl1994    the 4-point circuit of 7 of Coppersmith, Feig and Linzer (1994) along each pair of
             address bits (lowest bits first); when k is odd, one textbook layer on the top bit, last.
             (7/8) N k adders, plus N/8 when k is odd.
  family     family(k, 'G') of tools/circuits/gen.py: (3/4) N k + N/4 adders.
"""
import json
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
REL = os.path.normpath(os.path.join(HERE, '..', '..'))      # tools/circuits of this repository: gen.py, slp.py
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'rtl'))         # gen_rtl.py
sys.path.insert(0, os.path.join(HERE, '..', 'rtl', 'sim'))  # golden.py
sys.path.insert(1, REL)
for _d in ('circuits', 'v'):                                 # the folders this program writes into
    os.makedirs(os.path.join(HERE, _d), exist_ok=True)

SIZES = [16, 32, 64, 128, 256]
DESIGNS = ['textbook', 'cfl1994', 'family']
WIDTHS = [9, 12]
VARIANTS = ['c', 'p']

CFL4 = """
z0 = x1 + x2
z1 = z0 + x3
z2 = x0 - z1
y0 = x0 + z1
y1 = z2 + 2*x2
y2 = z2 + 2*x1
y3 = z2 + 2*x3
"""


def circuit_text(N, design):
    import gen
    import slp
    k = N.bit_length() - 1
    B2 = gen.Template(slp.parse_text(gen.BUTTERFLY).lines, 'textbook step')
    C4 = gen.Template(slp.parse_text(CFL4).lines, 'CFL 1994, 4 points, 7 adders')
    if design == 'textbook':
        lines, fac = gen.layered(k, [B2] * k, False)
        head = '%d points, textbook: %d layers of %d butterflies, %d adders.' % (N, k, N // 2, N * k)
    elif design == 'cfl1994':
        plan = [C4] * (k // 2) + ([B2] if k % 2 else [])
        lines, fac = gen.layered(k, plan, False)
        head = ('%d points, Coppersmith-Feig-Linzer 1994: the 4-point circuit of 7 along %d pairs of address bits'
                % (N, k // 2)) + (', then one textbook layer on the top bit.' if k % 2 else '.')
    elif design == 'cfl1994b':            # the other order, for the paper table only
        plan = ([B2] if k % 2 else []) + [C4] * (k // 2)
        lines, fac = gen.layered(k, plan, False)
        head = '%d points, CFL 1994, textbook layer first.' % N
    elif design == 'family':
        lines, fac = gen.family(k, 'G')
        head = '%d points, the family: gen.family(%d, "G") of tools/circuits/gen.py, (3/4) N k + N/4 adders.' % (N, k)
    else:
        raise ValueError(design)
    assert fac == 1
    return gen.text(lines, head + '\nWritten by tools/circuits/fpga/family/fam.py; output yJ = row J of H.')


def step_circuits():
    import slp
    out = []
    for N in SIZES:
        for d in DESIGNS + ['cfl1994b']:
            if d == 'cfl1994b' and N.bit_length() % 2 == 1:
                continue                      # k even: same as cfl1994
            t = circuit_text(N, d)
            path = os.path.join(HERE, 'circuits', '%d_%s.txt' % (N, d))
            with open(path, 'w') as f:
                f.write(t)
            r = slp.verify(slp.parse_file(path), labelled=True)
            line = ('%s: N=%d adders(G)=%d [add %d, sub %d] factor %s labels_are_rows=%s checks: %s'
                    % (os.path.basename(path), r['N'], r['G'], r['add'], r['sub'], slp.fmt_fac(r['factors']),
                       r['labels_are_rows'], '; '.join(r['how'])))
            print(line, flush=True)
            out.append(line)
    with open(os.path.join(HERE, 'circuits', 'CHECKED.txt'), 'w') as f:
        f.write('\n'.join(out) + '\n')


def load(N, d):
    import gen_rtl
    path = os.path.join(HERE, 'circuits', '%d_%s.txt' % (N, d))
    with open(path) as f:
        lines, outs = gen_rtl.parse_text(f.read())
    return gen_rtl.Circuit(lines, outs, 'tools/circuits/fpga/family/circuits/%d_%s.txt' % (N, d))


def step_paper():
    rows = []
    for N in SIZES:
        for d in DESIGNS + ['cfl1994b']:
            if not os.path.exists(os.path.join(HERE, 'circuits', '%d_%s.txt' % (N, d))):
                continue
            c = load(N, d)
            sub = sum(1 for _, (sa, A, ka), (sb, B, kb) in c.adders if sa < 0 or sb < 0)
            shifted = sum(1 for _, (sa, A, ka), (sb, B, kb) in c.adders if ka or kb)
            for W in WIDTHS:
                m = c.metrics(W, 1)
                wd = c.widths(W)
                # bits of the operand that is subtracted (the iCE40 flow spends one LUT on each)
                subbits = 0
                for node, (sa, A, ka), (sb, B, kb) in c.adders:
                    if sa < 0 or sb < 0:
                        subbits += wd[node]
                m2 = c.metrics(W, 2)
                row = dict(N=N, design=d, W=W, adders=m['adders'], subtractors=sub, shifted=shifted,
                           depth=m['depth'], adder_bits=m['adder_bits'], chain_bits=m['chain_bits'],
                           sub_bits=subbits, reg_after_adders=m['reg_after_adders'], reg_delay=m['reg_delay'],
                           reg_data=m['reg_data'], reg_valid=m['reg_valid'], OW=m['OW'],
                           p2_reg_data=m2['reg_data'], p2_latency=m2['latency'])
                rows.append(row)
    with open(os.path.join(HERE, 'paper.json'), 'w') as f:
        json.dump(rows, f, indent=1)
    print('%-4s %-9s %2s %6s %5s %5s %10s %10s %8s | %9s %9s %8s | %8s'
          % ('N', 'design', 'W', 'adders', 'subs', 'depth', 'adder_bits', 'chain_bits', 'sub_bits',
             'p:adderFF', 'p:delayFF', 'p:total', 'p2:total'))
    for r in rows:
        print('%-4d %-9s %2d %6d %5d %5d %10d %10d %8d | %9d %9d %8d | %8d'
              % (r['N'], r['design'], r['W'], r['adders'], r['subtractors'], r['depth'], r['adder_bits'],
                 r['chain_bits'], r['sub_bits'], r['reg_after_adders'], r['reg_delay'], r['reg_data'],
                 r['p2_reg_data']))


def null_core(N, W, module):
    """A core that is wiring only: output j = input j, sign-extended.  For measuring the wrapper alone."""
    k = N.bit_length() - 1
    OW = W + k
    o = ['// Written by fam.py.  Null core: wiring only (output j = input j, sign-extended).',
         '`default_nettype none',
         'module %s (' % module,
         '    input  wire clk,',
         '    input  wire in_valid,',
         '    input  wire [%d:0] in_data,' % (N * W - 1),
         '    output wire out_valid,',
         '    output wire [%d:0] out_data' % (N * OW - 1),
         ');',
         '    genvar g;',
         '    generate for (g = 0; g < %d; g = g + 1) begin : e' % N,
         '        assign out_data[g*%d +: %d] = {{%d{in_data[g*%d + %d]}}, in_data[g*%d +: %d]};'
         % (OW, OW, k, W, W - 1, W, W),
         '    end endgenerate',
         '    assign out_valid = in_valid;',
         '    wire _unused_clk = clk;',
         'endmodule',
         '`default_nettype wire']
    return '\n'.join(o) + '\n'


def wrapper(N, W, core, module):
    """Four pins.  Serial in to a shift register that feeds the core; the core's outputs are loaded
    into a second shift register (a 2-to-1 choice in front of every flip-flop) and shifted out."""
    k = N.bit_length() - 1
    OW = W + k
    o = ['// Written by fam.py.  The same wrapper for every design: 4 pins (clk, sin, load, sout).',
         '// %d input flip-flops in a shift register; %d output flip-flops, each behind a 2-to-1 choice' % (N * W, N * OW),
         '// (load the core output, or shift).  The timed path is input register -> core -> output register.',
         '`default_nettype none',
         'module %s (input wire clk, input wire sin, input wire load, output wire sout);' % module,
         '    localparam IW = %d, OWT = %d;' % (N * W, N * OW),
         '    reg  [IW-1:0]  sr_in;',
         '    reg  [OWT-1:0] sr_out;',
         '    reg  load_r, valid_r, ov_r;',
         '    wire ov;',
         '    wire [OWT-1:0] y;',
         '    %s core (.clk(clk), .in_valid(valid_r), .in_data(sr_in), .out_valid(ov), .out_data(y));' % core,
         '    always @(posedge clk) begin',
         '        sr_in   <= {sr_in[IW-2:0], sin};',
         '        load_r  <= load;',
         '        valid_r <= load;',
         '        ov_r    <= ov;',
         '        if (load_r) sr_out <= y;',
         '        else        sr_out <= {sr_out[OWT-2:0], ov_r};',
         '    end',
         '    assign sout = sr_out[OWT-1];',
         'endmodule',
         '`default_nettype wire']
    return '\n'.join(o) + '\n'


def step_rtl():
    import gen_rtl
    man = []
    for N in SIZES:
        for d in DESIGNS:
            c = load(N, d)
            for W in WIDTHS:
                for v in VARIANTS:
                    bn = '%d_%s_%s_w%d' % (N, d, v, W)
                    with open(os.path.join(HERE, 'v', bn + '.v'), 'w') as f:
                        f.write(c.verilog(W, v, 'wht_' + bn, K=1))
                    with open(os.path.join(HERE, 'v', 'top_' + bn + '.v'), 'w') as f:
                        f.write(wrapper(N, W, 'wht_' + bn, 'top_' + bn))
                    man.append(dict(N=N, design=d, W=W, variant=v, file='v/%s.v' % bn, module='wht_' + bn,
                                    latency=0 if v == 'c' else c.depth))
        for W in WIDTHS:
            bn = '%d_null_c_w%d' % (N, W)
            with open(os.path.join(HERE, 'v', bn + '.v'), 'w') as f:
                f.write(null_core(N, W, 'wht_' + bn))
            with open(os.path.join(HERE, 'v', 'top_' + bn + '.v'), 'w') as f:
                f.write(wrapper(N, W, 'wht_' + bn, 'top_' + bn))
    with open(os.path.join(HERE, 'designs.json'), 'w') as f:
        json.dump(man, f, indent=1)
    print('wrote %d designs' % len(man))


def step_vectors(N, W):
    import golden
    golden.VEC = os.path.join(HERE, 'work', 'vec')
    golden.TB = os.path.join(HERE, 'work', 'tb')
    golden.NRANDOM = 20000
    golden.NMIX = 2000
    golden.NNAIVE = 100 if N >= 128 else 400
    os.makedirs(golden.VEC, exist_ok=True)
    os.makedirs(golden.TB, exist_ok=True)
    circ = [load(N, d) for d in DESIGNS]
    info = golden.write_vectors(N, W, circ)
    with open(os.path.join(HERE, 'designs.json')) as f:
        man = json.load(f)
    duts, files = [], []
    for r in man:
        if r['N'] == N and r['W'] == W:
            duts.append(('%d_%s_%s_w%d' % (N, r['design'], r['variant'], W), r['module'], r['latency']))
            files.append(r['file'])
    golden.write_tb(str(N), N, W, duts, info)
    with open(os.path.join(golden.TB, 'tb_%d_w%d.files' % (N, W)), 'w') as f:
        f.write('\n'.join(files) + '\n')
    print('N=%d W=%d: %d vectors (%d corner, of which %d from the adders of the designs and %d mixed; %d random); %d designs'
          % (N, W, info['vectors'], info['corner'], info['corner_structured'], info['corner_mixed'],
             info['random'], len(duts)))


if __name__ == '__main__':
    s = sys.argv[1]
    if s == 'circuits':
        step_circuits()
    elif s == 'paper':
        step_paper()
    elif s == 'rtl':
        step_rtl()
    elif s == 'vectors':
        step_vectors(int(sys.argv[2]), int(sys.argv[3]))
    else:
        raise SystemExit(__doc__)
