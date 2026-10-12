#!/usr/bin/env python3
"""tables.py -- turn the output of "harness time" (style-generator variants) into tables.

    python3 -B tables.py RUNNAME=out/time-float-run1.txt,out/time-double-run1.txt [RUNNAME=...] > tables.md

For each run and each type:
  * the times: best (minimum) and median of the repeats, nanoseconds per point for one transform;
  * the change of each variant against FFHT as it is ("ffht"), in per cent, from the best times
    and (in brackets) from the medians.  "gT" is the same source as "ffht" compiled a second
    time and linked at another place: its column says how much two copies of the same code
    differ in that run, so a change of another variant that is not larger than that says nothing.
With two or more runs: a table of the changes of every run side by side.
A run can be several files (comma-separated): when a size occurs in more than one of them, the
occurrence whose hyper-thread sibling was least busy is used.

Nothing is rounded before a ratio is taken.  "!" marks a size whose hyper-thread sibling was
busy for more than 20 % of the time, or one of whose loops ran for less than 0.2 s.
"""
import re
import sys

ORDER = ['ffht', 'gT', 'g20x', 'g20s', 'g19f', 'g19r']
WHAT = {
    'ffht': 'FFHT as it is',
    'gT': 'the same source again',
    'g20x': '20 operations, exact',
    'g20s': '20 operations, up to scale',
    'g19f': '19 with multiply-add, constant in memory',
    'g19r': '19 with multiply-add, constant in a register',
}


def parse(paths):
    """{(type, k): record}.  A size can occur more than once (a later file that times some sizes
    again): the occurrence whose hyper-thread sibling was least busy is kept.  Inside one harness
    process a size that was timed again after a line D replaces its earlier attempt."""
    out = {}
    for path in paths:
        cur = None
        for line in open(path):
            line = line.rstrip('\n')
            if not line or line[0] not in 'BTEA' or line[1:2] != ' ':
                continue
            kv = dict(m.groups() for m in re.finditer(r'(\w+)=(\S+)', line))
            if line[0] == 'B':
                cur = {'T': {}, 'B': kv, 'file': path}
            elif cur is None:
                continue
            elif line[0] == 'T':
                cur['T'][kv['variant']] = kv
            elif line[0] == 'E':
                cur['E'] = kv
            else:
                cur['A'] = kv
                key = (kv['type'], int(kv['k']))
                old = out.get(key)
                if old is None or old['file'] == path or \
                        float(kv['sibling_busy_pct']) < float(old['A']['sibling_busy_pct']):
                    out[key] = cur
                cur = None
    return out


def pct(a, b):
    return 100.0 * (a - b) / b


def note_of(rec):
    note = ''
    if float(rec['A']['sibling_busy_pct']) > 20:
        note = '!'
    for t in rec['T'].values():
        if float(t['loop_s_min']) < 0.2:
            note = '!'
    return note


def run_tables(name, data, variants):
    L = []
    for typ in ('float', 'double'):
        ks = sorted(k for (t, k) in data if t == typ and 'A' in data[(t, k)])
        if not ks:
            continue
        L.append('### %s, %ss: the times\n' % (name, typ))
        L.append('Nanoseconds per point for one transform: best of the repeats (median).\n')
        hdr = ['k'] + variants + ['empty loop', 'repeats', 'largest spread: median / worst', 'sibling busy', 'processor', '']
        L.append('| ' + ' | '.join(hdr) + ' |')
        L.append('|' + '---|' * len(hdr))
        for k in ks:
            rec = data[(typ, k)]
            cells = [str(k)]
            sm = sx = 0.0
            for v in variants:
                t = rec['T'].get(v)
                if not t:
                    cells.append('-')
                    continue
                cells.append('%.3f (%.3f)' % (float(t['min']), float(t['med'])))
                sm = max(sm, float(t['spread_med_pct']))
                sx = max(sx, float(t['spread_max_pct']))
            cells += ['%.4f' % float(rec['E']['min']), rec['B']['repeats'], '%.1f %% / %.0f %%' % (sm, sx),
                      '%.0f %%' % float(rec['A']['sibling_busy_pct']), rec['A'].get('cpu', rec['B']['cpu']), note_of(rec)]
            L.append('| ' + ' | '.join(cells) + ' |')
        L.append('')
        L.append('### %s, %ss: the change against FFHT as it is\n' % (name, typ))
        L.append('Per cent, from the best times (from the medians). Negative = faster than FFHT.\n')
        hdr = ['k'] + [v for v in variants if v != 'ffht'] + ['']
        L.append('| ' + ' | '.join(hdr) + ' |')
        L.append('|' + '---|' * len(hdr))
        for k in ks:
            rec = data[(typ, k)]
            base = rec['T'].get('ffht')
            cells = [str(k)]
            for v in variants:
                if v == 'ffht':
                    continue
                t = rec['T'].get(v)
                if not t or not base:
                    cells.append('-')
                    continue
                cells.append('%+.1f (%+.1f)' % (pct(float(t['min']), float(base['min'])), pct(float(t['med']), float(base['med']))))
            cells.append(note_of(rec))
            L.append('| ' + ' | '.join(cells) + ' |')
        L.append('')
    return L


def side_by_side(runs, variants):
    L = []
    names = [n for n, _ in runs]
    for typ in ('float', 'double'):
        ks = sorted(set(k for _, d in runs for (t, k) in d if t == typ and 'A' in d[(t, k)]))
        if not ks:
            continue
        L.append('### All runs side by side, %ss: change against FFHT as it is, from the best times, per cent\n' % typ)
        L.append('In each cell: %s.\n' % ' / '.join(names))
        vs = [v for v in variants if v != 'ffht']
        L.append('| k | ' + ' | '.join(vs) + ' |')
        L.append('|---|' + '---|' * len(vs))
        for k in ks:
            cells = [str(k)]
            for v in vs:
                parts = []
                for _, d in runs:
                    rec = d.get((typ, k))
                    if not rec or v not in rec['T'] or 'ffht' not in rec['T']:
                        parts.append('-')
                    else:
                        parts.append('%+.1f%s' % (pct(float(rec['T'][v]['min']), float(rec['T']['ffht']['min'])), note_of(rec)))
                cells.append(' / '.join(parts))
            L.append('| ' + ' | '.join(cells) + ' |')
        L.append('')
        L.append('### All runs side by side, %ss: FFHT as it is, best time in each run (ns per point), and how far the runs are apart\n' % typ)
        L.append('| k | ' + ' | '.join(names) + ' | largest - smallest, per cent |')
        L.append('|---|' + '---|' * (len(names) + 1))
        for k in ks:
            vals = []
            for _, d in runs:
                rec = d.get((typ, k))
                vals.append(float(rec['T']['ffht']['min']) if rec and 'ffht' in rec['T'] else None)
            have = [x for x in vals if x is not None]
            L.append('| %d | %s | %.1f |' % (k, ' | '.join('-' if x is None else '%.3f' % x for x in vals),
                                             pct(max(have), min(have)) if len(have) > 1 else 0.0))
        L.append('')
    return L


def main():
    runs = []
    for arg in sys.argv[1:]:
        name, paths = arg.split('=', 1)
        runs.append((name, parse(paths.split(','))))
    present = set()
    for _, d in runs:
        for rec in d.values():
            present.update(rec['T'])
    variants = [v for v in ORDER if v in present]
    out = ['Variants: ' + '; '.join('`%s` = %s' % (v, WHAT[v]) for v in variants) + '.\n']
    for name, d in runs:
        out += run_tables(name, d, variants)
    if len(runs) > 1:
        out += side_by_side(runs, variants)
    print('\n'.join(out))


if __name__ == '__main__':
    main()
