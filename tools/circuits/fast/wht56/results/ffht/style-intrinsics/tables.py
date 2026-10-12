#!/usr/bin/env python3
"""tables.py -- make tables from the output of "harness time".

    python3 tables.py OUTFILE [OUTFILE ...] --cols ffht,T,Nc,N [--ratios Nc/T,N/T,T/ffht,Nc/ffht,N/ffht] [--type float]

Every figure is nanoseconds per point for one transform: the best of the repeats, and in brackets
the median.  With several files, a size that occurs in more than one is taken from the LAST file
that has it (so a re-run of some sizes replaces them), unless --each is given, which prints one
table per file.  A ratio a/b is best time of a over best time of b; below 1 means a is faster.
"spread" is the largest, over the columns shown, of (median - best) / best, and after the slash
of (worst - best) / best.  "sibling" is the share of the time in which the other hyper-thread of
the timed core was busy; "cpu" the processor the size was timed on.
"""
import re
import sys


def parse(path):
    data = {}        # (type, k) -> {'v': {name: (min, med, max, loop_s_min)}, 'sib': float, 'cpu': int, 'attempt': int, 'load': str}
    cur = None
    for line in open(path):
        f = dict(p.split('=', 1) for p in line.split()[1:] if '=' in p)
        tag = line[:2]
        if tag == 'B ':
            cur = {'v': {}, 'sib': None, 'cpu': int(f['cpu']), 'attempt': int(f['attempt']), 'loadB': f['load'], 'repeats': int(f['repeats']), 'R': f['R'], 'reset': f['reset']}
            data[(f['type'], int(f['k']))] = cur
        elif tag in ('T ', 'E ') and cur is not None:
            cur['v'][f['variant']] = (float(f['min']), float(f['med']), float(f['max']), float(f['loop_s_min']))
        elif tag == 'A ' and cur is not None:
            cur['sib'] = float(f['sibling_busy_pct'])
            cur['loadA'] = f['load']
            cur['steal'] = float(f['mycpu_steal_pct'])
    return data


def table(data, typ, cols, ratios, out):
    ks = sorted(k for (t, k) in data if t == typ)
    if not ks:
        return
    head = ['k'] + cols + ratios + ['spread: median / worst', 'sibling', 'cpu']
    out.append('| ' + ' | '.join(head) + ' |')
    out.append('|' + '---|' * len(head))
    for k in ks:
        d = data[(typ, k)]
        row = [str(k)]
        sm, sx = 0.0, 0.0
        for c in cols:
            if c in d['v']:
                mn, md, mx, _ = d['v'][c]
                row.append('%.3f (%.3f)' % (mn, md))
                sm = max(sm, (md - mn) / mn)
                sx = max(sx, (mx - mn) / mn)
            else:
                row.append('-')
        for r in ratios:
            a, b = r.split('/')
            row.append('%.3f' % (d['v'][a][0] / d['v'][b][0]) if a in d['v'] and b in d['v'] else '-')
        row.append('%.1f %% / %.0f %%' % (100 * sm, 100 * sx))
        row.append('%.0f %%' % d['sib'] if d['sib'] is not None else '?')
        row.append('%d%s' % (d['cpu'], '' if d['attempt'] == 1 else ' (attempt %d)' % d['attempt']))
        out.append('| ' + ' | '.join(row) + ' |')


def main():
    args = sys.argv[1:]

    def opt(name, default=None):
        if name in args:
            i = args.index(name)
            v = args[i + 1]
            del args[i:i + 2]
            return v
        return default
    cols = opt('--cols', 'ffht,T,N').split(',')
    ratios = [r for r in opt('--ratios', '').split(',') if r]
    types = [opt('--type')] if '--type' in args else ['float', 'double']
    each = '--each' in args
    if each:
        args.remove('--each')
    out = []
    if each:
        for p in args:
            d = parse(p)
            for t in types:
                out.append('')
                out.append('**%s, %s**' % (t, p))
                out.append('')
                table(d, t, cols, ratios, out)
    else:
        d = {}
        for p in args:
            d.update(parse(p))
        for t in types:
            out.append('')
            out.append('**%s**' % t)
            out.append('')
            table(d, t, cols, ratios, out)
    print('\n'.join(out))


if __name__ == '__main__':
    main()
