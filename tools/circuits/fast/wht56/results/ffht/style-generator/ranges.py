#!/usr/bin/env python3
"""ranges.py -- the smallest and the largest change of each variant against "ffht", over ranges
of sizes, from harness output (same arguments as tables.py: RUNNAME=file,file ...).

    python3 -B ranges.py final=out/time-float-run1.txt,out/time-double-run1.txt,out/time-redo-run1.txt

For each run, type and range of k: for every variant the smallest and the largest change of the
best time in per cent, the median over the sizes, and how many sizes are faster / slower than
FFHT by more than the largest difference that "gT" (the same code as ffht) shows in that range.
Sizes whose sibling was busy for more than 20 % of the time are left out and counted.
"""
import statistics
import sys

import tables

RANGES = [(3, 5), (6, 8), (9, 14), (15, 20), (21, 26), (6, 26)]


def main():
    for arg in sys.argv[1:]:
        name, paths = arg.split('=', 1)
        d = tables.parse(paths.split(','))
        for typ in ('float', 'double'):
            for lo, hi in RANGES:
                ks = [k for k in range(lo, hi + 1) if (typ, k) in d]
                clean = [k for k in ks if not tables.note_of(d[(typ, k)])]
                if not clean:
                    continue
                variants = [v for v in tables.ORDER if v != 'ffht' and all(v in d[(typ, k)]['T'] for k in clean)]
                ch = {}
                for v in variants:
                    ch[v] = [tables.pct(float(d[(typ, k)]['T'][v]['min']), float(d[(typ, k)]['T']['ffht']['min'])) for k in clean]
                floor = max(abs(x) for x in ch['gT']) if 'gT' in ch else 0.0
                parts = []
                for v in variants:
                    xs = ch[v]
                    parts.append('%s %+.1f .. %+.1f (median %+.1f; faster at %d, slower at %d of %d)' % (
                        v, min(xs), max(xs), statistics.median(xs),
                        sum(1 for x in xs if x < -floor), sum(1 for x in xs if x > floor), len(xs)))
                print('%s %s k=%d..%d (%d sizes, %d left out; same-code difference up to %.1f %%): %s'
                      % (name, typ, lo, hi, len(clean), len(ks) - len(clean), floor, '; '.join(parts)))
            print()


if __name__ == '__main__':
    main()
