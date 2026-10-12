#!/usr/bin/env python3
"""summary.py -- ratios of best times (and of medians) between variants, from "harness time" output.

    python3 summary.py --pairs N/T,Nc/T,T/ffht FILE [FILE ...]

For each number type and each pair a/b: the ratio of the best times at every size, the ratio of
the medians in brackets, and then, per band of sizes, the smallest and the largest ratio and how
many sizes have a ratio below 1 (a faster than b).  With several files each file is one run: the
ratios of every run are printed side by side, so that one sees what repeats and what does not.
"""
import sys
from tables import parse      # noqa: E402  (tables.py is beside this file)

BANDS = [(3, 8), (9, 14), (15, 20), (21, 26)]


def main():
    args = sys.argv[1:]
    i = args.index('--pairs')
    pairs = args[i + 1].split(',')
    del args[i:i + 2]
    runs = [parse(p) for p in args]
    for typ in ('float', 'double'):
        ks = sorted(set(k for d in runs for (t, k) in d if t == typ))
        if not ks:
            continue
        for pr in pairs:
            a, b = pr.split('/')
            print('\n%s  %s   (best/best, in brackets median/median; one column per run)' % (typ, pr))
            rows = {}
            for k in ks:
                cells = []
                for d in runs:
                    v = d.get((typ, k), {}).get('v', {})
                    if a in v and b in v:
                        cells.append((v[a][0] / v[b][0], v[a][1] / v[b][1]))
                    else:
                        cells.append(None)
                rows[k] = cells
                print('  k=%2d  ' % k + '   '.join('%.3f (%.3f)' % c if c else '      -      ' for c in cells))
            for lo, hi in BANDS:
                for ri in range(len(runs)):
                    r = [rows[k][ri][0] for k in ks if lo <= k <= hi and rows[k][ri]]
                    if r:
                        print('  2^%d..2^%d run %d: %.3f .. %.3f, median %.3f; %d of %d sizes below 1' %
                              (lo, hi, ri + 1, min(r), max(r), sorted(r)[len(r) // 2], sum(1 for x in r if x < 1), len(r)))


if __name__ == '__main__':
    main()
