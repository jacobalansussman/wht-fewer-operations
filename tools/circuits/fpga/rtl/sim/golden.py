#!/usr/bin/env python3
"""golden.py -- test vectors and expected outputs for the Verilog designs, and
the test benches that apply them.  Standard library only.

THE GOLDEN MODEL is the definition of the transform and nothing else:
    y_J = sum over i of (-1)^popcount(J & i) * x_i .
It is computed twice: once for all vectors at a time with exact big integers
(every input column packed into one integer with 32-bit digits, the N^2 signed
sums done on those integers), and once more, entry by entry, on the first
vectors of every file; the two must agree.  No line of any circuit is used.

THE VECTORS for N points and W bits (the same file serves every design of that
size; the 8 x 8 block designs use the 64-point files, x_(8r+c) = X[r][c]):
  corner cases
    all zero, all largest (2^(W-1)-1), all smallest (-2^(W-1));
    one input at largest / smallest / +1 / -1 and the rest zero;
    for EVERY adder of EVERY design of that size: the input that makes that
      adder's value largest, and the one that makes it smallest (inputs that
      the adder does not depend on are 0 in one copy and at random extremes in
      another).  These are the vectors that would show a wire one bit too narrow;
    2,000 vectors with every entry drawn from {min, min+1, -1, 0, 1, max-1, max};
  100,000 vectors with every entry uniform over the whole signed range
    (Python's random.Random with seed 20261011*1000 + N*100 + W).

FILES (under ../work/vec/):  <N>_w<W>.in.hex and <N>_w<W>.out.hex, one vector
per line, the hexadecimal value of the bus (x_0 or y_0 in the low bits), and
<N>_w<W>.json with the counts.  The test benches go to ../work/tb/.

USE:  python3 -B sim/golden.py            (from fpga/rtl; writes everything)
"""
import array
import hashlib
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.dont_write_bytecode = True
sys.path.insert(0, ROOT)
import gen_rtl  # noqa: E402

VEC = os.path.join(ROOT, 'work', 'vec')
TB = os.path.join(ROOT, 'work', 'tb')
NRANDOM = 100000
NMIX = 2000
NNAIVE = 400


def H(j, i):
    return -1 if bin(i & j).count('1') % 2 else 1


def golden_packed(cols, N, Wd):
    """cols[i] = list of T values of x_i.  Returns rows[j] = list of T values of y_j."""
    T = len(cols[0])
    off = 1 << (Wd - 1)
    R = ((1 << (32 * T)) - 1) // ((1 << 32) - 1)          # 1 in every 32-bit digit
    V = []
    for i in range(N):
        a = array.array('I', [v + off for v in cols[i]])
        assert a.itemsize == 4
        if sys.byteorder != 'little':
            a.byteswap()
        V.append(int.from_bytes(a.tobytes(), 'little') - off * R)
    OFF2 = 1 << 31
    rows = []
    for j in range(N):
        Y = 0
        for i in range(N):
            Y = Y + V[i] if H(j, i) > 0 else Y - V[i]
        Y += OFF2 * R
        assert Y >= 0
        b = Y.to_bytes(4 * T, 'little')
        a = array.array('I')
        a.frombytes(b)
        if sys.byteorder != 'little':
            a.byteswap()
        rows.append([v - OFF2 for v in a])
    return rows


def corner_vectors(N, Wd, circuits, rnd):
    hi = (1 << (Wd - 1)) - 1
    lo = -(1 << (Wd - 1))
    seen, out = set(), []

    def put(v):
        t = tuple(v)
        if t not in seen:
            seen.add(t)
            out.append(list(v))

    put([0] * N)
    put([hi] * N)
    put([lo] * N)
    for i in range(N):
        for val in (hi, lo, 1, -1):
            v = [0] * N
            v[i] = val
            put(v)
    for c in circuits:
        for node, vec in c.coef.items():
            for sgn in (1, -1):
                put([(hi if sgn * cf > 0 else lo) if cf else 0 for cf in vec])
                put([(hi if sgn * cf > 0 else lo) if cf else rnd.choice((hi, lo)) for cf in vec])
    n_struct = len(out)
    pool = (lo, lo + 1, -1, 0, 1, hi - 1, hi)
    for _ in range(NMIX):
        out.append([rnd.choice(pool) for _ in range(N)])
    return out, n_struct


def write_vectors(N, Wd, circuits):
    k = N.bit_length() - 1
    OW = Wd + k
    rnd = random.Random(20261011 * 1000 + N * 100 + Wd)
    hi = (1 << (Wd - 1)) - 1
    lo = -(1 << (Wd - 1))
    corner, n_struct = corner_vectors(N, Wd, circuits, rnd)
    rand = [[rnd.randint(lo, hi) for _ in range(N)] for _ in range(NRANDOM)]
    vecs = corner + rand
    T = len(vecs)
    cols = [[v[i] for v in vecs] for i in range(N)]
    rows = golden_packed(cols, N, Wd)
    # second computation, entry by entry, on the first vectors and the last ones
    for t in list(range(min(NNAIVE, T))) + list(range(T - 50, T)):
        x = vecs[t]
        for j in range(N):
            assert rows[j][t] == sum(H(j, i) * x[i] for i in range(N)), (N, Wd, t, j)
    # every output must fit OW bits, and OW must be needed
    mx = max(max(r) for r in rows)
    mn = min(min(r) for r in rows)
    assert -(1 << (OW - 1)) <= mn and mx <= (1 << (OW - 1)) - 1
    assert mn == -(1 << (OW - 1)), 'the smallest output value was not reached'
    mi, mo = (1 << Wd) - 1, (1 << OW) - 1
    fi, fo = '%%0%dx\n' % ((N * Wd + 3) // 4), '%%0%dx\n' % ((N * OW + 3) // 4)
    base = os.path.join(VEC, '%d_w%d' % (N, Wd))
    hin, hout = hashlib.sha256(), hashlib.sha256()
    with open(base + '.in.hex', 'w') as f, open(base + '.out.hex', 'w') as g:
        for t in range(T):
            x = vecs[t]
            a = 0
            for i in range(N - 1, -1, -1):
                a = (a << Wd) | (x[i] & mi)
            b = 0
            for j in range(N - 1, -1, -1):
                b = (b << OW) | (rows[j][t] & mo)
            s1, s2 = fi % a, fo % b
            f.write(s1)
            g.write(s2)
            hin.update(s1.encode())
            hout.update(s2.encode())
    info = dict(N=N, W=Wd, OW=OW, vectors=T, corner=len(corner), corner_structured=n_struct,
                corner_mixed=NMIX, random=NRANDOM, seed=20261011 * 1000 + N * 100 + Wd,
                naive_recheck=min(NNAIVE, T) + 50,
                sha256_in=hin.hexdigest(), sha256_out=hout.hexdigest())
    with open(base + '.json', 'w') as f:
        json.dump(info, f, indent=1)
    return info


def write_tb(tag, N, Wd, duts, info):
    """duts: list of (label, module, latency).  One bench checks all of them on the same vectors."""
    k = N.bit_length() - 1
    OW = Wd + k
    maxlat = max(l for _, _, l in duts)
    o = []
    o.append('// Written by sim/golden.py.  Test bench: %d points, W = %d, %d designs, %d vectors.'
             % (N, Wd, len(duts), info['vectors']))
    o.append('`timescale 1ns/1ps')
    o.append('module tb;')
    o.append('    parameter NFILE = %d;          // vectors in the files' % info['vectors'])
    o.append('    parameter NRUN  = %d;          // vectors applied (first NRUN of the file)' % info['vectors'])
    o.append('    localparam IW = %d, OWT = %d, MAXLAT = %d;' % (N * Wd, N * OW, maxlat))
    o.append('    reg clk = 1\'b0;')
    o.append('    always #5 clk = ~clk;')
    o.append('    reg in_valid = 1\'b0;')
    o.append('    reg [IW-1:0] in_data = {IW{1\'b0}};')
    o.append('    reg [IW-1:0]  invec [0:NFILE-1];')
    o.append('    reg [OWT-1:0] expv  [0:NFILE-1];')
    o.append('    reg           vbit  [0:NFILE+MAXLAT+3];')
    for n, (label, module, lat) in enumerate(duts):
        o.append('    wire v%d; wire [OWT-1:0] o%d; integer err%d = 0; integer chk%d = 0;' % (n, n, n, n))
        o.append('    %s u%d (.clk(clk), .in_valid(in_valid), .in_data(in_data), .out_valid(v%d), .out_data(o%d));'
                 % (module, n, n, n))
    o.append('    integer i; integer total;')
    o.append('    initial begin')
    o.append('        $readmemh("%s_w%d.in.hex", invec);' % (N, Wd))
    o.append('        $readmemh("%s_w%d.out.hex", expv);' % (N, Wd))
    o.append('        repeat (4) @(negedge clk);')
    o.append('        for (i = 0; i < NRUN + MAXLAT + 2; i = i + 1) begin')
    o.append('            if (i < NRUN) begin')
    o.append('                in_data = invec[i];')
    o.append('                in_valid = (i % 61) != 7;     // a gap in in_valid now and then; the data still flow')
    o.append('            end else begin')
    o.append('                in_data = {IW{1\'b0}};')
    o.append('                in_valid = 1\'b0;')
    o.append('            end')
    o.append('            vbit[i] = in_valid;')
    o.append('            #1;')
    for n, (label, module, lat) in enumerate(duts):
        o.append('            if (i >= %d && i - %d < NRUN) begin' % (lat, lat))
        o.append('                chk%d = chk%d + 1;' % (n, n))
        o.append('                if (o%d !== expv[i - %d] || v%d !== vbit[i - %d]) begin' % (n, lat, n, lat))
        o.append('                    err%d = err%d + 1;' % (n, n))
        o.append('                    if (err%d <= 3) $display("MISMATCH %s vector %%0d: got %%h valid %%b, want %%h valid %%b", i - %d, o%d, v%d, expv[i - %d], vbit[i - %d]);'
                 % (n, label, lat, n, n, lat, lat))
        o.append('                end')
        o.append('            end else if (v%d !== 1\'b0) begin' % n)
        o.append('                err%d = err%d + 1;' % (n, n))
        o.append('                if (err%d <= 3) $display("MISMATCH %s: out_valid is %%b outside the run, step %%0d", v%d, i);' % (n, label, n))
        o.append('            end')
    o.append('            @(negedge clk);')
    o.append('        end')
    o.append('        total = 0;')
    for n, (label, module, lat) in enumerate(duts):
        o.append('        $display("RESULT %s latency %d checked %%0d errors %%0d", chk%d, err%d); total = total + err%d;'
                 % (label, lat, n, n, n))
    o.append('        $display("BENCH %s_w%d designs %d vectors %%0d total_errors %%0d", NRUN, total);' % (tag, Wd, len(duts)))
    o.append('        $finish;')
    o.append('    end')
    o.append('endmodule')
    path = os.path.join(TB, 'tb_%s_w%d.v' % (tag, Wd))
    with open(path, 'w') as f:
        f.write('\n'.join(o) + '\n')
    return path


def main():
    os.makedirs(VEC, exist_ok=True)
    os.makedirs(TB, exist_ok=True)
    with open(os.path.join(ROOT, 'designs.json')) as f:
        dj = json.load(f)
    designs = gen_rtl.build_designs()
    circ = {}
    for d in designs:
        lines, outs = gen_rtl.parse_text(d['text'])
        c = gen_rtl.Circuit(lines, outs, d['source'])
        circ.setdefault(c.N, []).append(c)
    summary = []
    for tag, N in (('8', 8), ('16', 16), ('64', 64)):
        for Wd in gen_rtl.WIDTHS:
            info = write_vectors(N, Wd, circ[N])
            duts, files = [], []
            for r in dj['designs']:
                if r['N'] == N and r['W'] == Wd:
                    for vname in ('c', 'p', 'p2', 'r'):
                        e = r['files'][vname]
                        duts.append(('%s_%s_%s_w%d' % (r['size'], r['design'], vname, Wd), e['module'], e['latency']))
                        files.append(e['file'])
            for e in dj['definitions']:
                if e['N'] == N and e['W'] == Wd:
                    duts.append(('%s_def_c_w%d' % (e['size'], Wd), e['module'], 0))
                    files.append(e['file'])
            tb = write_tb(tag, N, Wd, duts, info)
            with open(os.path.join(TB, 'tb_%s_w%d.files' % (tag, Wd)), 'w') as f:
                f.write('\n'.join(files) + '\n')
            info['bench'] = os.path.relpath(tb, ROOT)
            info['designs_in_bench'] = len(duts)
            summary.append(info)
            print('N=%d W=%d: %d vectors (%d corner of which %d from the adders of the designs and %d mixed; %d random); bench with %d designs'
                  % (N, Wd, info['vectors'], info['corner'], info['corner_structured'], info['corner_mixed'],
                     info['random'], len(duts)), flush=True)
    with open(os.path.join(ROOT, 'work', 'vec', 'SUMMARY.json'), 'w') as f:
        json.dump(summary, f, indent=1)


if __name__ == '__main__':
    main()
