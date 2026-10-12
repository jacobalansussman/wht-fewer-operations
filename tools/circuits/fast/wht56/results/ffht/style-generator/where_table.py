#!/usr/bin/env python3
"""where_table.py -- the table for the variants that use the new kernel only in some passes.

    python3 -B where_table.py out/time-float-where.txt out/time-double-where.txt

Per size: FFHT's best time (median), and for every variant the change against FFHT in per cent,
from the best times (from the medians), with the number of passes that have the new kernel in
that variant at that size (from out/scale/V.k8_scale.inc, written by the generator; p19f and
d19f have the new kernel in the same passes as p20s and d20s).
"""
import re
import sys

import tables

ORDER = ['g20s', 'p20s', 'p19f', 'd20s', 'd19f']
PASSES_FROM = {'g20s': 'g20s', 'p20s': 'p20s', 'p19f': 'p20s', 'd20s': 'd20s', 'd19f': 'd20s'}


def passes(v):
    out = {}
    for line in open('out/scale/%s.k8_scale.inc' % PASSES_FROM[v]):
        m = re.match(r'static const int k8_passes_(\w+)\[31\] = \{(.*)\};', line)
        if m:
            out[m.group(1)] = [int(x) for x in m.group(2).split(',')]
    return out


def main():
    d = tables.parse(sys.argv[1:])
    P = dict((v, passes(v)) for v in ORDER)
    for typ in ('float', 'double'):
        ks = sorted(k for (t, k) in d if t == typ)
        if not ks:
            continue
        print('**%ss**\n' % typ.capitalize())
        hdr = ['k', 'FFHT: ns per point, best (median)'] + ['`%s`' % v for v in ORDER] + ['spread: median / worst', 'sibling busy']
        print('| ' + ' | '.join(hdr) + ' |')
        print('|' + '---|' * len(hdr))
        for k in ks:
            r = d[(typ, k)]
            b = r['T']['ffht']
            cells = [str(k), '%.3f (%.3f)' % (float(b['min']), float(b['med']))]
            for v in ORDER:
                x = r['T'][v]
                n = P[v][typ][k]
                cells.append('%+.1f %% (%+.1f %%); %d' % (tables.pct(float(x['min']), float(b['min'])),
                                                        tables.pct(float(x['med']), float(b['med'])), n))
            sm = max(float(r['T'][v]['spread_med_pct']) for v in r['T'])
            sx = max(float(r['T'][v]['spread_max_pct']) for v in r['T'])
            cells += ['%.1f %% / %.0f %%' % (sm, sx), '%.0f %%%s' % (float(r['A']['sibling_busy_pct']), ' !' if tables.note_of(r) else '')]
            print('| ' + ' | '.join(cells) + ' |')
        print()


if __name__ == '__main__':
    main()
