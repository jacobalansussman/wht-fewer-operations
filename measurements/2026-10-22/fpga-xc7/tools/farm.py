#!/usr/bin/env python3
"""farm.py (ax-k1, wave 16): a place-and-route farm for any design folder in our format.

    python3 -B tools/farm.py DESIGN_DIR [--seeds 5] [--slots N] [--mem-per-run GB] [--only TAG,...] [--out DIR]

DESIGN_DIR holds Verilog files and runs.txt.  Each non-empty, non-# line of runs.txt is ONE design measured on one or
more chips, written as fpga_measure.py arguments with a tag first:

    TAG: file1.v [file2.v ...] --chip ecp5-25k,nexus-lifcl40 [--top M] [--freq 250] [--param N=V] [--synth-opts "..."]

(paths relative to DESIGN_DIR; --seeds, --jobs, --work, --out and --tag are set by the farm).  Every line runs
through tools/fpga_farm.py (common/fpga_measure.py with the Colab changes: same harness, same counting, same JSON).
Concurrency: at most --slots tool runs at once (default: cores, but no more than RAM / --mem-per-run), split as
several lines at once x several seeds per line.  Output: OUT/farm.jsonl (every seed and every summary line),
OUT/farm_table.md (medians [lowest-highest] per tag and chip), OUT/logs/TAG.log.
"""
import argparse
import concurrent.futures as cf
import glob
import json
import os
import shlex
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))


def ram_gb():
    try:
        for line in open('/proc/meminfo'):
            if line.startswith('MemTotal:'):
                return int(line.split()[1]) / 1e6
    except OSError:
        pass
    return 16.0


def parse(design_dir, only):
    runs = []
    for i, line in enumerate(open(os.path.join(design_dir, 'runs.txt'))):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        tag, rest = line.split(':', 1)
        tag = tag.strip()
        if only and tag not in only:
            continue
        args = shlex.split(rest)
        out = []
        for j, x in enumerate(args):   # relative design files, folders and globs (xk265/fme/*.v) -> absolute paths
            pathy = j > 0 and args[j - 1] in ('--incdir', '--overwrite')
            if not x.startswith('-') and not os.path.isabs(x) and (pathy or '/' in x or x.endswith(('.v', '.sv'))):
                full = os.path.join(design_dir, x)
                hits = sorted(glob.glob(full)) if any(c in x for c in '*?[') else [full]
                if not hits or not all(os.path.exists(h) for h in hits):
                    raise SystemExit('runs.txt line %d: %s not found in %s' % (i + 1, x, design_dir))
                out += hits
                continue
            out.append(x)
        runs.append((tag, out))
    return runs


def table(rows):
    allk = {k for r in rows for k in r.get('stats', {})}
    keys_pref = [k for k in ['dut_lc', 'dut_comb', 'dut_lut', 'dut_lut_user', 'dut_lut_sites', 'dut_lut_srl_or_ram', 'dut_ff', 'dut_carry4',
                             'dut_carry', 'dut_dsp', 'dut_mult18', 'dut_bram', 'dut_slices_lower_bound', 'dut_slices_touched',
                             'fmax_mhz'] if k in allk]
    lines = ['| tag | chip | seeds ok / failed | ' + ' | '.join(k.replace('dut_', '') for k in keys_pref) + ' |',
             '|' + '---|' * (3 + len(keys_pref))]
    for r in rows:
        st = r.get('stats', {})
        cells = []
        for k in keys_pref:
            v = st.get(k)
            cells.append('-' if v is None else ('%g' % v['med'] if v['min'] == v['max'] else '%g [%g-%g]' % (v['med'], v['min'], v['max'])))
        lines.append('| %s | %s | %d / %d | %s |' % (r['tag'], r['chip'], len(r.get('seeds', [])), len(r.get('failed_seeds', [])),
                                                    ' | '.join(cells)))
    return '\n'.join(lines) + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('design_dir')
    ap.add_argument('--seeds', type=int, default=5)
    ap.add_argument('--slots', type=int, default=0)
    ap.add_argument('--mem-per-run', type=float, default=2.0, help='GB one nextpnr run may take (big designs: 4-8)')
    ap.add_argument('--only', default='')
    ap.add_argument('--out', default=None)
    ap.add_argument('--timeout', type=int, default=7200, help='seconds per tool run')
    ap.add_argument('--dry', action='store_true', help='print the runs and stop')
    a = ap.parse_args()
    dd = os.path.abspath(a.design_dir)
    out = os.path.abspath(a.out or os.path.join(os.getcwd(), 'out', os.path.basename(dd)))
    os.makedirs(os.path.join(out, 'logs'), exist_ok=True)
    slots = a.slots or max(1, min(os.cpu_count() or 2, int(ram_gb() / a.mem_per_run)))
    runs = parse(dd, set(t for t in a.only.split(',') if t))
    per_line = min(a.seeds, slots)
    lines_at_once = max(1, slots // per_line)
    env = dict(os.environ, FARM_SLOTS=str(slots))
    print('[farm] %d lines, %d seeds each, %d tool runs at once (%d lines x %d seeds); RAM %.0f GB; out %s'
          % (len(runs), a.seeds, slots, lines_at_once, per_line, ram_gb(), out), flush=True)
    jl = os.path.join(out, 'farm.jsonl')
    # the work folders hold the netlists (up to ~200 MB per design): outside the job folder when FARM_WORK is set,
    # so that fetching the results back does not copy them
    work = os.path.join(os.environ['FARM_WORK'], os.path.basename(dd)) if os.environ.get('FARM_WORK') else os.path.join(out, 'work')
    if a.dry:
        for tag, args in runs:
            print(tag, ' '.join(os.path.relpath(x, dd) if os.path.isabs(x) else x for x in args))
        return 0

    def one(tag, args):
        t0 = time.time()
        cmd = [sys.executable, '-B', os.path.join(HERE, 'fpga_farm.py')] + args + [
            '--seeds', str(a.seeds), '--jobs', str(per_line), '--tag', tag, '--work', work,
            '--out', jl, '--timeout', str(a.timeout)]
        with open(os.path.join(out, 'logs', tag + '.log'), 'w') as lf:
            rc = subprocess.run(cmd, stdout=lf, stderr=subprocess.STDOUT, env=env).returncode
        print('[farm] %-30s rc=%d  %.0f s' % (tag, rc, time.time() - t0), flush=True)
        return rc

    with cf.ThreadPoolExecutor(max_workers=lines_at_once) as ex:
        rcs = list(ex.map(lambda r: one(*r), runs))
    summ = []
    if os.path.exists(jl):
        for line in open(jl):
            d = json.loads(line)
            if d.get('summary') or d.get('synthesis_only'):
                summ.append(d)
    open(os.path.join(out, 'farm_table.md'), 'w').write(table([s for s in summ if s.get('summary')]))
    print(open(os.path.join(out, 'farm_table.md')).read())
    for s in summ:
        if s.get('synthesis_only'):
            print('[farm] synthesis only: %s %s %s' % (s['tag'], s['chip'], {k: v for k, v in s.items() if k.startswith('y_')}))
    print('FARM DONE: %d lines, %d failed' % (len(rcs), sum(1 for r in rcs if r)))
    return 0 if not any(rcs) else 1


if __name__ == '__main__':
    sys.exit(main())
