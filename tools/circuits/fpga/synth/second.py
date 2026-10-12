#!/usr/bin/env python3
"""second.py -- the second opinion: the same design files on other FPGA families.

    python3 -B second.py synth              yosys only, the design module alone (no harness):
                                            synth_ice40 (flat, as a cross-check of run.py),
                                            synth_ecp5, synth_xilinx -family xc7, synth_intel_alm
                                            -family cyclonev.  Cell counts as yosys prints them.
    python3 -B second.py ecp5 [--seeds 5]   place and route for a Lattice ECP5 (LFE5U-25F, package
                                            CABGA381, speed grade 6) with nextpnr-ecp5, in the same
                                            harness as run.py (shift register in, signature
                                            register out, design kept as its own module).

Results: results/second_synth.jsonl and results/second_ecp5.jsonl, one JSON line per run.
One process at a time.  Standard library only.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import run as R   # harness_src, stub_src, parse_design, yosys_stat

FPGA = os.path.dirname(HERE)
RTLV = os.path.join(FPGA, 'rtl', 'v')
EXTRA = os.path.join(HERE, 'v_extra')
RES = os.path.join(HERE, 'results')
WORK = os.path.join(HERE, 'work', 'second')
os.environ['PATH'] = R.BIN + ':' + os.environ.get('PATH', '')

FAMILIES = {
    'ice40': 'synth_ice40 -top {top}',
    'ecp5': 'synth_ecp5 -top {top}',
    'xc7': 'synth_xilinx -family xc7 -noclkbuf -top {top}',
    'cyclonev': 'synth_intel_alm -family cyclonev -noiopad -noclkbuf -top {top}',
}


def designs():
    L = []
    for W in (8, 12):
        for d in ('textbook', 'cfl1994', 'ar2023', 'ours'):
            for v in ('c', 'p', 'p2'):
                L.append(('8', d, v, W, os.path.join(RTLV, '8_%s_%s_w%d.v' % (d, v, W))))
            if d != 'textbook':
                L.append(('8', d, 'p3', W, os.path.join(EXTRA, '8_%s_p3_w%d.v' % (d, W))))
        for d in ('textbook', 'cfl1994', 'ours'):
            for v in ('c', 'p', 'p2'):
                L.append(('16', d, v, W, os.path.join(RTLV, '16_%s_%s_w%d.v' % (d, v, W))))
            if d != 'textbook':
                L.append(('16', d, 'p4', W, os.path.join(EXTRA, '16_%s_p4_w%d.v' % (d, W))))
    return L


def cells_of(stat_path, top):
    st = R.yosys_stat(stat_path)
    c = st.get(top) or st.get('top') or {}
    return {k: v for k, v in c.items() if k not in ('wires', 'ports', 'cells', 'submodules') and not k.startswith('$')}


def summarize(fam, c):
    s = {}
    if fam == 'ice40':
        s['lut'] = c.get('SB_LUT4', 0)
        s['carry'] = c.get('SB_CARRY', 0)
        s['ff'] = sum(v for k, v in c.items() if k.startswith('SB_DFF'))
    elif fam == 'ecp5':
        s['lut'] = c.get('LUT4', 0)
        s['carry'] = c.get('CCU2C', 0)                 # one CCU2C = two bits of carry chain = two LUT4 places
        s['lut_equiv'] = c.get('LUT4', 0) + 2 * c.get('CCU2C', 0)
        s['ff'] = c.get('TRELLIS_FF', 0)
        s['mux'] = c.get('PFUMX', 0) + c.get('L6MUX21', 0)
    elif fam == 'xc7':
        s['lut'] = sum(v for k, v in c.items() if re.match(r'LUT[1-6]$', k))
        s['carry'] = c.get('CARRY4', 0)                # one CARRY4 = four bits of carry chain
        s['ff'] = sum(v for k, v in c.items() if k.startswith('FD'))
        s['srl'] = sum(v for k, v in c.items() if k.startswith('SRL'))
        s['inv'] = c.get('INV', 0)
        s['lut_total'] = s['lut'] + s['srl']           # a shift-register LUT occupies a LUT
    elif fam == 'cyclonev':
        s['arith'] = c.get('MISTRAL_ALUT_ARITH', 0)    # one per adder bit (half an ALM)
        s['lut'] = sum(v for k, v in c.items() if re.match(r'MISTRAL_ALUT[2-6]$', k)) + c.get('MISTRAL_NOT', 0)
        s['ff'] = c.get('MISTRAL_FF', 0)
        s['lut_total'] = s['arith'] + s['lut']
    return s


def do_synth(a):
    os.makedirs(RES, exist_ok=True)
    out = os.path.join(RES, 'second_synth.jsonl')
    done = set()
    if os.path.exists(out):
        for l in open(out):
            r = json.loads(l)
            done.add((r['tag'], r['family']))
    for size, d, v, W, path in designs():
        mod, nw, no = R.parse_design(path)
        tag = mod[4:]
        for fam in a.families.split(','):
            if (tag, fam) in done:
                continue
            wd = os.path.join(WORK, 'synth', fam, tag)
            os.makedirs(wd, exist_ok=True)
            st = os.path.join(wd, 'stat.txt')
            ys = 'read_verilog %s\n%s\ntee -o %s stat\n' % (path, FAMILIES[fam].format(top=mod), st)
            open(os.path.join(wd, 'synth.ys'), 'w').write(ys)
            t0 = time.time()
            p = subprocess.run(['yosys', '-q', '-l', os.path.join(wd, 'yosys.log'), '-s', os.path.join(wd, 'synth.ys')],
                               capture_output=True, text=True)
            r = dict(tag=tag, family=fam, size=size, design_name=d, variant=v, W=W, seconds=round(time.time() - t0, 1))
            if p.returncode != 0:
                r['error'] = (p.stderr or p.stdout)[-300:]
            else:
                r['cells'] = cells_of(st, mod)
                r.update(summarize(fam, r['cells']))
            open(out, 'a').write(json.dumps(r) + '\n')
            print(tag, fam, {k: r[k] for k in r if k in ('lut', 'carry', 'ff', 'srl', 'arith', 'lut_total', 'lut_equiv', 'error')},
                  r['seconds'], flush=True)


def ecp5_one(tag, mod, design, nw, no, outreg, seeds, out, done, meta):
    wd = os.path.join(WORK, 'ecp5', tag)
    os.makedirs(wd, exist_ok=True)
    jsn = os.path.join(wd, 'top.json')
    if not os.path.exists(jsn):
        open(os.path.join(wd, 'harness.v'), 'w').write(R.harness_src(mod, nw, no, outreg))
        ys = ['read_verilog %s' % design, 'read_verilog %s' % os.path.join(wd, 'harness.v'),
              'synth_ecp5 -top top', 'tee -o %s stat' % os.path.join(wd, 'stat_hier.txt'),
              'setattr -mod -unset keep_hierarchy dut', 'flatten', 'clean', 'write_json %s' % jsn]
        open(os.path.join(wd, 'synth.ys'), 'w').write('\n'.join(ys) + '\n')
        p = subprocess.run(['yosys', '-q', '-l', os.path.join(wd, 'yosys.log'), '-s', os.path.join(wd, 'synth.ys')],
                           capture_output=True, text=True)
        if p.returncode != 0:
            open(out, 'a').write(json.dumps(dict(meta, tag=tag, error='yosys: ' + (p.stderr or p.stdout)[-300:])) + '\n')
            return
    st = R.yosys_stat(os.path.join(wd, 'stat_hier.txt'))
    dutc = {k: v for k, v in st.get('dut', {}).items() if k not in ('wires', 'ports', 'cells') and not k.startswith('$')}
    for s in seeds:
        if (tag, s) in done:
            continue
        base = os.path.join(wd, 's%d' % s)
        t0 = time.time()
        p = subprocess.run(['nextpnr-ecp5', '--25k', '--package', 'CABGA381', '--speed', '6', '--json', jsn,
                            '--seed', str(s), '--freq', '400', '--timing-allow-fail', '--report', base + '.report.json',
                            '--write', base + '.placed.json', '-q', '-l', base + '.nextpnr.log'], capture_output=True, text=True)
        r = dict(meta, tag=tag, seed=s, yosys_dut=dutc, nextpnr_seconds=round(time.time() - t0, 1))
        if p.returncode != 0:
            log = open(base + '.nextpnr.log').read() if os.path.exists(base + '.nextpnr.log') else ''
            m = re.search(r'ERROR:.*', log)
            r['error'] = m.group(0) if m else 'nextpnr-ecp5 failed'
        else:
            rep = json.load(open(base + '.report.json'))
            u = rep['utilization']
            r['util'] = {k: v['used'] for k, v in u.items() if v['used']}
            for k, v in rep.get('fmax', {}).items():
                r['fmax_nextpnr'] = round(v['achieved'], 2)
            # slices touched: a slice is one of SLICEA..D of a tile; it holds two LUT4 places and two flip-flops
            if os.path.exists(base + '.placed.json'):
                top = json.load(open(base + '.placed.json'))['modules']['top']
                sl = set()
                for n, x in top['cells'].items():
                    if x['type'] in ('TRELLIS_COMB', 'TRELLIS_FF'):
                        m = re.match(r'(X\d+/Y\d+)/(SLICE[A-D])', x['attributes'].get('NEXTPNR_BEL', ''))
                        if m:
                            sl.add(m.group(1) + m.group(2))
                r['slices'] = len(sl)
                os.remove(base + '.placed.json')
        open(out, 'a').write(json.dumps(r) + '\n')
        print(tag, s, r.get('util'), r.get('fmax_nextpnr'), r.get('error', ''), r['nextpnr_seconds'], flush=True)


def do_ecp5(a):
    os.makedirs(RES, exist_ok=True)
    out = os.path.join(RES, a.out)
    done = set()
    if os.path.exists(out):
        for l in open(out):
            r = json.loads(l)
            done.add((r['tag'], r.get('seed')))
    seeds = list(range(1, a.seeds + 1))
    seen = set()
    for size, d, v, W, path in designs():
        if v not in a.variants.split(','):
            continue
        mod, nw, no = R.parse_design(path)
        if (nw, no) not in seen:
            seen.add((nw, no))
            smod, ssrc = R.stub_src(nw, no)
            sd = os.path.join(WORK, 'ecp5', 'stub_%d_%d' % (nw, no))
            os.makedirs(sd, exist_ok=True)
            open(os.path.join(sd, 'stub.v'), 'w').write(ssrc)
            ecp5_one('stub_%d_%d' % (nw, no), smod, os.path.join(sd, 'stub.v'), nw, no, 0, [1], out, done,
                     dict(size=size, design_name='stub', variant='-', W=W, nw=nw, no=no))
        ecp5_one(mod[4:], mod, path, nw, no, 1 if v == 'c' else 0, seeds, out, done,
                 dict(size=size, design_name=d, variant=v, W=W, nw=nw, no=no))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('what', choices=['synth', 'ecp5'])
    ap.add_argument('--families', default='ice40,ecp5,xc7,cyclonev')
    ap.add_argument('--seeds', type=int, default=5)
    ap.add_argument('--variants', default='c,p')
    ap.add_argument('--out', default='second_ecp5.jsonl', help='results file name for ecp5')
    a = ap.parse_args()
    if a.what == 'synth':
        do_synth(a)
    else:
        do_ecp5(a)


if __name__ == '__main__':
    main()
