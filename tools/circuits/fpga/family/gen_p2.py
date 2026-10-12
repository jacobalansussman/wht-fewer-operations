#!/usr/bin/env python3
"""gen_p2.py -- a second, small generator, written separately from gen_rtl.py: the same circuit
with a register after every STEP-th adder level (STEP = 2 gives the family k pipeline
stages, the number the textbook has with a register after every level).
Same ports as the main generator's modules, so the same wrapper is used.
Exact widths from recount.py's reader.  usage: gen_p2.py N design STEP W outdir"""
import os, sys, re
F = os.path.dirname(os.path.abspath(__file__))        # this folder; the circuits are in circuits/ (fam.py circuits)
sys.path.insert(0, F)
import recount
N, d, STEP, W, out = int(sys.argv[1]), sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
k = N.bit_length() - 1
lines = recount.read('%s/circuits/%d_%s.txt' % (F, N, d))
vec = {'x%d' % i: [1 if j == i else 0 for j in range(N)] for i in range(N)}
lev = {'x%d' % i: 0 for i in range(N)}
wid = {'x%d' % i: W for i in range(N)}
alias = {}; adders = []; outs = {}
for name, ts in lines:
    ts = [(c, alias.get(n, n)) for c, n in ts]
    v = [0]*N
    for c, n in ts: v = [a + c*b for a, b in zip(v, vec[n])]
    vec[name] = v
    if len(ts) == 2:
        lev[name] = 1 + max(lev[n] for _, n in ts); wid[name] = recount.width(v, W)
        adders.append((name, ts))
    else:
        assert ts[0][0] == 1, name
        alias[name] = ts[0][1]
        if re.fullmatch(r'y\d+', name): outs[int(name[1:])] = ts[0][1]
D = max(lev.values()); S = -(-D // STEP)
stage = {n: -(-L // STEP) for n, L in lev.items()}           # inputs: stage 0
last = {}                                                    # last boundary a value must be registered at
for name, ts in adders:
    for _, n in ts:
        if stage[n] < stage[name]: last[n] = max(last.get(n, 0), stage[name] - 1)
for J, n in outs.items(): last[n] = S
OW = W + k
mod = 'wht_%d_%s_p%d_w%d' % (N, d, STEP, W)
o = []
o.append('// Written by gen_p2.py.  %d-point Walsh-Hadamard transform, circuit %d_%s.txt.' % (N, N, d))
o.append('// A register after every %d adder levels: %d stages, latency %d.  Inputs %d bits signed, outputs %d bits.' % (STEP, S, S, W, OW))
o.append('`default_nettype none')
o.append('module %s (input wire clk, input wire in_valid, input wire [%d:0] in_data, output wire out_valid, output wire [%d:0] out_data);' % (mod, N*W-1, N*OW-1))
regs = []; nreg = 0
def use(n, t):          # name of value n as seen by an adder in stage t
    s = stage[n]
    if s == t or (s == 0 and t == 1): return n if s == 0 else 'n_' + n
    return '%s_r%d' % (n if s == 0 else 'n_' + n, t - 1)
def decl_regs(n):
    global nreg
    s = stage[n]; base = n if s == 0 else 'n_' + n
    first = max(s, 1)
    for j in range(first, last.get(n, 0) + 1):
        o.append('    reg signed [%d:0] %s_r%d;' % (wid[n]-1, base, j))
        regs.append('        %s_r%d <= %s;' % (base, j, base if j == first else '%s_r%d' % (base, j-1)))
        nreg += wid[n]
for i in range(N):
    o.append('    wire signed [%d:0] x%d = in_data[%d:%d];' % (W-1, i, W*i+W-1, W*i))
    decl_regs('x%d' % i)
def term(c, n, t):
    a = abs(c); sh = a.bit_length() - 1
    assert a == 1 << sh
    u = use(n, t)
    return u if sh == 0 else '(%s <<< %d)' % (u, sh)
for name, ts in adders:
    t = stage[name]
    (c1, n1), (c2, n2) = ts
    assert c1 > 0 or c2 > 0
    if c1 > 0 and c2 > 0: e = '%s + %s' % (term(c1, n1, t), term(c2, n2, t))
    elif c1 > 0: e = '%s - %s' % (term(c1, n1, t), term(c2, n2, t))
    else: e = '%s - %s' % (term(c2, n2, t), term(c1, n1, t))
    o.append('    wire signed [%d:0] n_%s = %s;   // level %d, stage %d' % (wid[name]-1, name, e, lev[name], t))
    decl_regs(name)
for J in range(N):
    n = outs[J]
    o.append('    assign out_data[%d:%d] = {{%d{n_%s_r%d[%d]}}, n_%s_r%d};' % (OW*J+OW-1, OW*J, OW - wid[n], n, S, wid[n]-1, n, S)
             if wid[n] < OW else '    assign out_data[%d:%d] = n_%s_r%d;' % (OW*J+OW-1, OW*J, n, S))
o.append('    reg [%d:0] vld = %d\'d0;' % (S-1, S))
o.append('    always @(posedge clk) begin')
o += regs
o.append('        vld <= {vld, in_valid};' if S > 1 else '        vld <= in_valid;')
o.append('    end')
o.append('    assign out_valid = vld[%d];' % (S-1))
o.append('endmodule')
o.append('`default_nettype wire')
open('%s/%d_%s_p%d_w%d.v' % (out, N, d, STEP, W), 'w').write('\n'.join(o) + '\n')
top = open('%s/v/top_%d_%s_p_w%d.v' % (F, N, d, W)).read().replace('%d_%s_p_w%d' % (N, d, W), '%d_%s_p%d_w%d' % (N, d, STEP, W))
open('%s/top_%d_%s_p%d_w%d.v' % (out, N, d, STEP, W), 'w').write(top)
print('%s: adders %d, levels %d, stages %d, register bits %d (+ %d valid)' % (mod, len(adders), D, S, nreg, S))
