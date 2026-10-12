#!/usr/bin/env python3
"""mkjobs.py -- write the job scripts into jobs/pending/.  The name gives the order (runq.py).
  sim     vectors (sim/golden.py) + Verilator build + run, one bench per size and width (6 designs)
  syn     yosys synth_<ice40|ecp5|xilinx> of the bare core, defaults; cell counts with "stat -json"
  wrap    yosys synth_<ice40|ecp5> -noflatten of core + wrapper, then flatten; JSON for nextpnr
  pnr     nextpnr-ice40 --hx8k --package ct256 / nextpnr-ecp5 --85k --package CABGA381, --freq 200
Usage: python3 -B mkjobs.py <group> ...   (groups below)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PEND = os.path.join(HERE, 'jobs', 'pending')
ENV = 'export PATH="${OSS_CAD_SUITE:-/opt/oss-cad-suite}/bin:$PATH"\n'
SIZES = [16, 32, 64, 128, 256]
DESIGNS = ['textbook', 'cfl1994', 'family']
SYN = {'ice40': 'synth_ice40', 'ecp5': 'synth_ecp5', 'xilinx': 'synth_xilinx'}


def put(name, body, timeout=600):
    done = os.path.join(HERE, 'jobs', 'done', name + '.sh')
    if os.path.exists(done) or os.path.exists(os.path.join(HERE, 'jobs', 'running', name + '.sh')):
        return
    with open(os.path.join(PEND, name + '.sh'), 'w') as f:
        f.write('# timeout=%d\n' % timeout + ENV + body + '\n')


def sim(pri, N, W):
    b = '%d_w%d' % (N, W)
    opt = '-O1' if N <= 64 else '-O0'
    put('%02d_sim_%03d_w%d' % (pri, N, W),
        'set -e\nmkdir -p work/vl\npython3 -B fam.py vectors %d %d\n' % (N, W) +
        'verilator --binary --timing -j 1 -Wno-fatal -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDSIGNAL '
        '-Wno-DECLFILENAME -CFLAGS %s --top-module tb --Mdir work/vl/tb_%s -o sim work/tb/tb_%s.v '
        '$(cat work/tb/tb_%s.files) > logs/verilator_build_%s.log 2>&1\n' % (opt, b, b, b, b) +
        '( cd work/vec && ../vl/tb_%s/sim ) > logs/sim_%s.log 2>&1\n' % (b, b) +
        'grep -E "^(BENCH|RESULT|MISMATCH)" logs/sim_%s.log\n' % b +
        'rm -rf work/vl/tb_%s work/vec/%s.in.hex work/vec/%s.out.hex\n' % (b, b, b), timeout=900)


def syn(pri, N, d, v, W, fam):
    bn = '%d_%s_%s_w%d' % (N, d, v, W)
    put('%02d_syn_%s_%03d_%s_%s_w%d' % (pri, fam, N, d, v, W),
        'yosys -q -l logs/syn_%s.%s.log -p "read_verilog v/%s.v; %s -top wht_%s; '
        'tee -q -o synth_out/%s.%s.json stat -json"' % (bn, fam, bn, SYN[fam], bn, bn, fam))


def wrap(pri, N, d, v, W, fam):
    bn = '%d_%s_%s_w%d' % (N, d, v, W)
    put('%02d_wrap_%s_%03d_%s_%s_w%d' % (pri, fam, N, d, v, W),
        'yosys -q -l logs/wrap_%s.%s.log -p "read_verilog v/%s.v v/top_%s.v; %s -top top_%s -noflatten; '
        'flatten; opt_clean; tee -q -o pnr/%s.%s.stat.json stat -json; write_json pnr/%s.%s.json"'
        % (bn, fam, bn, bn, SYN[fam], bn, bn, fam, bn, fam))


def pnr(pri, N, d, v, W, fam, seed):
    bn = '%d_%s_%s_w%d' % (N, d, v, W)
    if fam == 'ice40':
        cmd = ('nextpnr-ice40 --hx8k --package ct256 --json pnr/%s.ice40.json --pcf-allow-unconstrained '
               '--seed %d --freq 200 --timing-allow-fail -q -l pnr/%s.ice40.s%d.log' % (bn, seed, bn, seed))
    else:
        cmd = ('nextpnr-ecp5 --85k --package CABGA381 --json pnr/%s.ecp5.json --lpf-allow-unconstrained '
               '--seed %d --freq 200 --timing-allow-fail -q -l pnr/%s.ecp5.s%d.log' % (bn, seed, bn, seed))
    put('%02d_pnr_%s_%03d_%s_%s_w%d_s%d' % (pri, fam, N, d, v, W, seed), cmd)


def pack(pri, N, d, v, W, fam):
    bn = '%d_%s_%s_w%d' % (N, d, v, W)
    if fam == 'ice40':
        cmd = ('nextpnr-ice40 --hx8k --package ct256 --json pnr/%s.ice40.json --pcf-allow-unconstrained '
               '--pack-only -q -l pnr/%s.ice40.pack.log' % (bn, bn))
    else:
        cmd = ('nextpnr-ecp5 --85k --package CABGA381 --json pnr/%s.ecp5.json --lpf-allow-unconstrained '
               '--pack-only -q -l pnr/%s.ecp5.pack.log' % (bn, bn))
    put('%02d_pack_%s_%03d_%s_%s_w%d' % (pri, fam, N, d, v, W), cmd)


def packgroup(W, pw, pp):
    for fam in ('ice40', 'ecp5'):
        for N in SIZES:
            for v in ('c', 'p'):
                for d in ['null'] + DESIGNS:
                    if d == 'null' and v == 'p':
                        continue
                    j = os.path.join(HERE, 'pnr', '%d_%s_%s_w%d.%s.json' % (N, d, v, W, fam))
                    have = [n for n in os.listdir(PEND) + os.listdir(os.path.join(HERE, 'jobs', 'done')) +
                            os.listdir(os.path.join(HERE, 'jobs', 'running'))
                            if n.endswith('_wrap_%s_%03d_%s_%s_w%d.sh' % (fam, N, d, v, W))]
                    if not os.path.exists(j) and not [n for n in have if int(n[:2]) <= pw]:
                        wrap(pw, N, d, v, W, fam)
                    pack(pp, N, d, v, W, fam)


def main():
    for g in sys.argv[1:]:
        if g == 'sim9small':
            for N in (16, 32, 64):
                sim(10, N, 9)
        elif g == 'sim9big':
            for N in (128, 256):
                sim(25, N, 9)
        elif g == 'sim12':
            for N in SIZES:
                sim(60, N, 12)
        elif g == 'syn9c':
            for N in SIZES:
                for d in DESIGNS:
                    for fam in ('ice40', 'ecp5', 'xilinx'):
                        syn(20, N, d, 'c', 9, fam)
        elif g == 'syn9p_ice40':
            for N in SIZES:
                for d in DESIGNS:
                    syn(22, N, d, 'p', 9, 'ice40')
        elif g == 'syn9p_rest':
            for N in SIZES:
                for d in DESIGNS:
                    for fam in ('ecp5', 'xilinx'):
                        syn(28, N, d, 'p', 9, fam)
        elif g == 'pnr9_ice40':
            for N in (16, 32, 64):
                for v in ('c', 'p'):
                    for d in ['null'] + DESIGNS:
                        if d == 'null' and v == 'p':
                            continue
                        wrap(23, N, d, v, 9, 'ice40')
                        pnr(24, N, d, v, 9, 'ice40', 1)
        elif g == 'pnr9_ice40_seeds':
            for N in (16, 32, 64):
                for v in ('c', 'p'):
                    for d in ['null'] + DESIGNS:
                        if d == 'null' and v == 'p':
                            continue
                        for s in (2, 3):
                            pnr(30, N, d, v, 9, 'ice40', s)
        elif g == 'pnr9_ecp5_c':
            for N in (64, 128, 256):
                for d in ['null'] + DESIGNS:
                    wrap(25, N, d, 'c', 9, 'ecp5')
                    pnr(26, N, d, 'c', 9, 'ecp5', 1)
        elif g == 'pnr9_ecp5_p':
            for N in (64, 128, 256):
                for d in DESIGNS:
                    wrap(31, N, d, 'p', 9, 'ecp5')
                    pnr(32, N, d, 'p', 9, 'ecp5', 1)
        elif g == 'pnr9_ecp5_seeds':
            for N in (64, 128, 256):
                for d in ['null'] + DESIGNS:
                    for s in (2, 3):
                        pnr(34 if N == 64 else 50, N, d, 'c', 9, 'ecp5', s)
        elif g == 'syn12':
            for N in SIZES:
                for d in DESIGNS:
                    for fam in ('ice40', 'ecp5', 'xilinx'):
                        syn(40, N, d, 'c', 12, fam)
                    syn(41, N, d, 'p', 12, 'ice40')
        elif g == 'pack9':
            packgroup(9, 27, 29)
        elif g == 'pack12':
            packgroup(12, 61, 62)
        else:
            raise SystemExit('unknown group ' + g)


if __name__ == '__main__':
    main()
