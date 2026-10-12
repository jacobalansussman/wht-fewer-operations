#!/usr/bin/env python3
"""stats.py -- the figures quoted in NOTES.md, from the harness output files.

    python3 stats.py out/time-float.txt out/time-double.txt out/time-int32.txt

Per number type: the range of each ratio over the sizes where the 8-register step is used, with the
sizes at the two ends; the sizes where the fused step is more than 4 % faster or slower than the
textbook step; the rows whose kept attempt had a busy sibling; and the cost of one later pass in
the cache, as the difference between two sizes that differ by exactly one such pass.
"""
import sys
from tables import parse

FIRST = {'float': 6, 'double': 5, 'int32': 6}          # smallest k at which the 8-register step is used
PASS = {'float': (9, 12, 64), 'double': (8, 11, 32), 'int32': (9, 12, 64)}   # k1, k2, numbers per step
GHZ = 2.63


def main():
    data, cond = parse(sys.argv[1:])
    for t in ('float', 'double', 'int32'):
        ks = sorted(k for (tt, k) in data if tt == t)
        if not ks:
            continue
        names = set()
        for k in ks:
            names |= set(data[(t, k)])
        ref = 'Tp'
        fused = 'G19p' if 'G19p' in names else 'G19sp'
        print(f'== {t}: sizes {ks[0]}..{ks[-1]} ({len(ks)} sizes)')
        busy = [(k, cond[(t, k)].get('sibling_busy_pct')) for k in ks if (t, k) in cond and float(cond[(t, k)].get('sibling_busy_pct', 0)) > 25]
        print('   rows with the sibling busy more than 25 %:', ', '.join(f'2^{k} ({b} %)' for k, b in busy) or 'none')
        for a, b in ((fused, ref), (fused, 'ffht'), ('G19ap', ref), (ref, 'ffht'), ('ffhtB', 'ffht'), ('Tfp', ref), ('sG19', 'sT'), ('sT', ref)):
            for which in ('min', 'med'):
                rs = []
                for k in ks:
                    d = data[(t, k)]
                    if k >= FIRST[t] and a in d and b in d:
                        rs.append((float(d[a][which]) / float(d[b][which]), k))
                if not rs:
                    continue
                lo, hi = min(rs), max(rs)
                good = [r for r in rs if not any(k == r[1] for k, _ in busy)]
                glo, ghi = (min(good), max(good)) if good else (lo, hi)
                print(f'   {a}/{b} ({which}): {lo[0]:.3f} (2^{lo[1]}) .. {hi[0]:.3f} (2^{hi[1]}); without the busy rows {glo[0]:.3f} (2^{glo[1]}) .. {ghi[0]:.3f} (2^{ghi[1]});'
                      f' below 0.96 at: {[k for r, k in rs if r < 0.96]}; above 1.04 at: {[k for r, k in rs if r > 1.04]}')
        k1, k2, pts = PASS[t]
        if (t, k1) in data and (t, k2) in data:
            for n in sorted(names - {'empty'}):
                if n in data[(t, k1)] and n in data[(t, k2)]:
                    d = float(data[(t, k2)][n]['min']) - float(data[(t, k1)][n]['min'])
                    print(f'   one later pass in the cache, {n}: 2^{k2} minus 2^{k1} = {d:.4f} ns per point = {d * pts:.2f} ns per step'
                          f' = {d * pts * GHZ:.1f} cycles per step at {GHZ} GHz')
        print('   key rows (min / med, ns per point):')
        for k in (6, 9, 12, 15, 18, 21, 24):
            if (t, k) in data:
                d = data[(t, k)]
                print(f'     2^{k}: ' + '; '.join(f"{n} {float(d[n]['min']):.3f} / {float(d[n]['med']):.3f}" for n in d if n != 'empty')
                      + f" | sibling busy {cond.get((t, k), {}).get('sibling_busy_pct', '?')} %")


if __name__ == '__main__':
    main()
