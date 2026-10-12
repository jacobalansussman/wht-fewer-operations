#!/usr/bin/env python3
"""batch.py -- run run.py over the whole matrix, two jobs at a time, and keep one JSON line per run
in results/<group>.jsonl.  A run already in the file is not repeated.

    python3 -B batch.py g8            8 points, every design, variant and width, 10 seeds
    python3 -B batch.py g16           16 points
    python3 -B batch.py g64 --seeds 5 64 points and the 8 x 8 block
    python3 -B batch.py g8 --list     print the job list only

A job = one design file with one flow; its seeds run one after the other (the first one also runs
yosys), so never more than two heavy processes run at a time.
"""
import argparse
import json
import os
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
FPGA = os.path.dirname(HERE)
RTLV = os.path.join(FPGA, 'rtl', 'v')
EXTRA = os.path.join(HERE, 'v_extra')
STD = os.path.join(FPGA, 'outside')        # the wrappers; the two outside cores are cloned into outside/cores/
RES = os.path.join(HERE, 'results')
LOCK = threading.Lock()

OWBITS = {'8': 3, '16': 4, '64': 6, '8x8': 6}
NPTS = {'8': 8, '16': 16, '64': 64, '8x8': 64}


def job(size, design, variant, W, path, flow='default', extra=None, incdir=None):
    tag = '%s_%s_%s_w%d' % (size, design, variant, W) + ('' if flow == 'default' else '_' + flow)
    return dict(tag=tag, size=size, design=design, variant=variant, W=W, flow=flow, path=path,
                extra=extra or [], incdir=incdir or [])


def stub(size, W):
    n = NPTS[size]
    nw, no = n * W, n * (W + OWBITS[size])
    return dict(tag='stub_%d_%d' % (nw, no), size=size, design='stub', variant='-', W=W, flow='default',
                path=None, nw=nw, no=no, extra=[], incdir=[])


def jobs_for(group):
    J = []
    if group == 'g8':
        for W in (8, 9, 12, 16):
            J.append(stub('8', W))
        xk = os.path.join(STD, 'cores', 'openasic-org_xk265', 'rtl')
        for W in (8, 12, 16):
            for d in ('textbook', 'cfl1994', 'ar2023', 'ours', 'cfl1994b', 'ar2023l'):
                for v in ('c', 'p', 'p2', 'r'):
                    J.append(job('8', d, v, W, os.path.join(RTLV, '8_%s_%s_w%d.v' % (d, v, W))))
            for d in ('textbook', 'cfl1994', 'ar2023', 'ours'):
                for fl in ('retime', 'dff'):
                    J.append(job('8', d, 'r', W, os.path.join(RTLV, '8_%s_r_w%d.v' % (d, W)), flow=fl))
            for d, Ks in (('cfl1994', (3, 4)), ('ar2023', (3, 4, 5)), ('ours', (3, 4, 5))):
                for K in Ks:
                    J.append(job('8', d, 'p%d' % K, W, os.path.join(EXTRA, '8_%s_p%d_w%d.v' % (d, K, W))))
        for W in (8, 9, 12, 16):
            for v in ('c', 'r'):
                J.append(job('8', 'xk265', v, W, os.path.join(STD, 'wrappers', '8_xk265_%s_w%d.v' % (v, W)),
                             extra=[os.path.join(xk, 'fme', 'fme_satd_8x8.v')], incdir=[xk]))
        for d in ('textbook', 'ours'):
            J.append(job('8', d, 'c', 9, os.path.join(STD, 'gen_w9', '8_%s_c_w9.v' % d)))
    elif group == 'g16':
        for W in (8, 9, 12, 16):
            J.append(stub('16', W))
        xk = os.path.join(STD, 'cores', 'openasic-org_xk264', 'rtl')
        for W in (8, 12, 16):
            for d in ('textbook', 'cfl1994', 'ours'):
                for v in ('c', 'p', 'p2', 'r'):
                    J.append(job('16', d, v, W, os.path.join(RTLV, '16_%s_%s_w%d.v' % (d, v, W))))
                for fl in ('retime', 'dff'):
                    J.append(job('16', d, 'r', W, os.path.join(RTLV, '16_%s_r_w%d.v' % (d, W)), flow=fl))
            for d, Ks in (('textbook', (3,)), ('cfl1994', (3, 4, 5, 6, 7)), ('ours', (3, 4, 5, 6, 7))):
                for K in Ks:
                    J.append(job('16', d, 'p%d' % K, W, os.path.join(EXTRA, '16_%s_p%d_w%d.v' % (d, K, W))))
        for v in ('c', 'r'):
            J.append(job('16', 'xk264', v, 9, os.path.join(STD, 'wrappers', '16_xk264_%s_w9.v' % v),
                         extra=[os.path.join(xk, 'intra', 'intra_hadamard4x4.v')], incdir=[xk]))
        for d in ('textbook', 'ours'):
            J.append(job('16', d, 'c', 9, os.path.join(STD, 'gen_w9', '16_%s_c_w9.v' % d)))
    elif group == 'g64':
        J.append(stub('64', 8))
        for size, designs in (('64', ('textbook', 'cfl1994', 'ours')), ('8x8', ('textbook', 'ours'))):
            for d in designs:
                for v in ('c', 'p2', 'p', 'r'):
                    J.append(job(size, d, v, 8, os.path.join(RTLV, '%s_%s_%s_w8.v' % (size, d, v))))
        for size, d, Ks in (('64', 'textbook', (3,)), ('64', 'cfl1994', (3, 4, 6)), ('64', 'ours', (3, 4, 6)),
                            ('8x8', 'ours', (3, 4, 6))):
            for K in Ks:
                J.append(job(size, d, 'p%d' % K, 8, os.path.join(EXTRA, '%s_%s_p%d_w8.v' % (size, d, K))))
    elif group == 'gnoreg':      # the combinational block alone: no output register in the design
        for size, designs in (('8', ('textbook', 'cfl1994', 'ar2023', 'ours', 'cfl1994b', 'ar2023l')),
                              ('16', ('textbook', 'cfl1994', 'ours'))):
            for W in (8, 12, 16):
                for d in designs:
                    J.append(job(size, d, 'c', W, os.path.join(RTLV, '%s_%s_c_w%d.v' % (size, d, W)), flow='noreg'))
    elif group == 'gS':          # the same circuits with other signs (resign.py)
        VR = os.path.join(HERE, 'v_resigned')
        # resign.py found other signs only for the 16-point circuit of this work; for every other
        # design the best choice of signs is the original file, so there is nothing new to measure.
        for size, designs, vs in (('16', ('ours',), ('c', 'p', 'p2', 'p4')),):
            for W in (8, 12, 16):
                for d in designs:
                    for v in vs:
                        f = os.path.join(VR, '%s_%sS_%s_w%d.v' % (size, d, v, W))
                        if os.path.exists(f):
                            J.append(job(size, d + 'S', v, W, f))
                    J.append(job(size, d + 'S', 'c', W, os.path.join(VR, '%s_%sS_c_w%d.v' % (size, d, W)), flow='noreg'))
    elif group == 'g64lean':     # 64 points with the lean harness (the standard one leaves too little room)
        st = stub('64', 8)
        st['tag'] += '_lean'
        st['flow'] = 'lean'
        J.append(st)
        order = [('64', 'textbook', 'c'), ('64', 'cfl1994', 'c'), ('64', 'ours', 'c'), ('8x8', 'ours', 'c'),
                 ('64', 'textbook', 'p3'), ('64', 'cfl1994', 'p6'), ('64', 'ours', 'p6'), ('8x8', 'ours', 'p6'),
                 ('64', 'cfl1994', 'p4'), ('64', 'textbook', 'p2'), ('64', 'textbook', 'p'), ('64', 'cfl1994', 'p3'),
                 ('8x8', 'ours', 'p4'), ('64', 'cfl1994', 'r'), ('64', 'ours', 'r'), ('8x8', 'ours', 'r')]
        for size, d, v in order:
            f = os.path.join(RTLV if v in ('c', 'p', 'p2', 'r') else EXTRA, '%s_%s_%s_w8.v' % (size, d, v))
            J.append(job(size, d, v, 8, f, flow='lean'))
    elif group == 'g64wide':     # synthesis only: the wider 64-point designs do not fit the chip
        for W in (12, 16):
            for size, designs in (('64', ('textbook', 'cfl1994', 'ours')), ('8x8', ('textbook', 'ours'))):
                for d in designs:
                    for v in ('c', 'p'):
                        J.append(job(size, d, v, W, os.path.join(RTLV, '%s_%s_%s_w%d.v' % (size, d, v, W))))
    else:
        raise SystemExit('unknown group ' + group)
    return J


def done_set(path):
    s = set()
    if os.path.exists(path):
        for line in open(path):
            try:
                r = json.loads(line)
            except ValueError:
                continue
            s.add((r['tag'], r.get('seed'), 'synth' if r.get('synth_only') else 'pack' if r.get('pack_only') else 'pnr'))
    return s


def run_job(j, seeds, out, done, work, synth_only, timeout, pack_only=False):
    mode = 'synth' if synth_only else 'pack' if pack_only else 'pnr'
    for s in seeds:
        if (j['tag'], s, mode) in done:
            continue
        cmd = [sys.executable, '-B', os.path.join(HERE, 'run.py'), '--seed', str(s), '--work', work, '--tag', j['tag'],
               '--pnr-timeout', str(timeout)]
        if j['design'] == 'stub':
            cmd += ['--stub', '--nw', str(j['nw']), '--no', str(j['no'])]
        else:
            cmd += [j['path']]
        if j['flow'] == 'retime':
            cmd += ['--retime']
        if j['flow'] == 'dff':
            cmd += ['--dff']
        if j['flow'] == 'noreg':
            cmd += ['--outreg', '0']
        if j['flow'] == 'lean':
            cmd += ['--lean']
        for e in j['extra']:
            cmd += ['--extra', e]
        for e in j['incdir']:
            cmd += ['--incdir', e]
        if synth_only:
            cmd += ['--no-pnr']
        if pack_only:
            cmd += ['--pack-only']
        t0 = time.time()
        p = subprocess.run(cmd, capture_output=True, text=True)
        try:
            r = json.loads(p.stdout.strip().splitlines()[-1])
        except (ValueError, IndexError):
            r = {'tag': j['tag'], 'seed': s, 'error': 'run.py gave no result: ' + (p.stderr or p.stdout)[-300:]}
        for k in ('size', 'design', 'variant', 'W', 'flow'):
            r[k if k != 'design' else 'design_name'] = j[k]
        r['synth_only'] = synth_only
        r['wall_seconds'] = round(time.time() - t0, 1)
        with LOCK:
            with open(out, 'a') as f:
                f.write(json.dumps(r) + '\n')
            print('%-28s seed %-2d lc_dut %-6s fmax %-7s icetime %-7s %5.1fs %s' % (
                j['tag'], s, r.get('lc_dut', '-'), r.get('fmax_nextpnr', '-'), r.get('fmax_icetime', '-'),
                r['wall_seconds'], r.get('error', '')), flush=True)
        if synth_only or pack_only or 'error' in r and 'yosys' in r['error']:
            break
        if r.get('error', '').startswith('nextpnr failed') or 'timed out' in r.get('error', ''):
            break      # it does not fit or does not finish: other seeds would say the same


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('group')
    ap.add_argument('--seeds', type=int, default=10)
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--synth-only', action='store_true')
    ap.add_argument('--pack-only', action='store_true')
    ap.add_argument('--max-lc', type=int, default=0, help='skip jobs whose packed image (results/<group>.jsonl, --pack-only) has more cells')
    ap.add_argument('--only', default=None, help='substring of the tag')
    ap.add_argument('--timeout', type=int, default=3600)
    ap.add_argument('--jobs', type=int, default=2)
    a = ap.parse_args()
    J = jobs_for(a.group)
    if a.only:
        J = [j for j in J if a.only in j['tag']]
    for j in J:
        if j['path'] and not os.path.exists(j['path']):
            raise SystemExit('missing file ' + j['path'])
    if a.list:
        for j in J:
            print(j['tag'], j['path'])
        print(len(J), 'jobs')
        return
    os.makedirs(RES, exist_ok=True)
    out = os.path.join(RES, a.group + '.jsonl')
    done = done_set(out)
    work = os.path.join(HERE, 'work', a.group)
    seeds = list(range(1, a.seeds + 1))
    if a.max_lc and os.path.exists(out):
        packed = {}
        for line in open(out):
            r = json.loads(line)
            if r.get('pack_only') and 'lc_total' in r:
                packed[r['tag']] = r['lc_total']
        J = [j for j in J if packed.get(j['tag'], 0) <= a.max_lc]
        print('jobs that fit %d cells: %d' % (a.max_lc, len(J)), flush=True)
    with ThreadPoolExecutor(max_workers=min(2, a.jobs)) as ex:
        futs = [ex.submit(run_job, j, seeds, out, done, work, a.synth_only, a.timeout, a.pack_only) for j in J]
        for f in futs:
            f.result()
    print('group', a.group, 'finished', time.strftime('%H:%M:%S'))


if __name__ == '__main__':
    main()
