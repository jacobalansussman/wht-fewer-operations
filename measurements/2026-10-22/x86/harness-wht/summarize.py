#!/usr/bin/env python3
"""summarize.py OUTDIR -- one table from every RESULT line (x86-wht job). Standard library only.
For each test (one '## title' group) the BASELINE is the fastest by median of: the textbook (tb16 / tb8 / textbook),
the pipe-balanced textbook (tb16bal / tb8bal / textbook-bal) and FFHT (whole transforms).  Each circuit's figure is
its median divided by that baseline's median (below 1 = faster).  The bar: 0.90 or below (10 % less time)."""
import glob, os, re, sys
RX = re.compile(r'^RESULT (.*?)\s+(\S+)\s+best\s+([\d.]+)\s+median\s+([\d.]+)\s+ns/(\S+)')
BASE = ('tb16', 'tb8', 'tb16bal', 'tb8bal', 'textbook', 'textbook-bal', 'FFHT')
out = sys.argv[1] if len(sys.argv) > 1 else 'out'
groups = {}
for f in sorted(glob.glob(os.path.join(out, '*.txt'))):
    for line in open(f, errors='replace'):
        m = RX.match(line)
        if m:
            title, name, best, med, unit = m.groups()
            groups.setdefault((os.path.basename(f), title), []).append((name, float(best), float(med), unit))
print('# x86-wht summary\n')
print('Figure = circuit median / fastest baseline median (textbook, pipe-balanced textbook, FFHT); < 1 is faster.\n')
print('| test | baseline (ns/unit) | ' + 'circuit: ratio ... |')
print('|---|---|---|')
clears = []
for (f, title), rows in groups.items():
    base = [r for r in rows if r[0] in BASE]
    if not base:
        continue
    b = min(base, key=lambda r: r[2])
    cells = []
    for name, best, med, unit in rows:
        if name in BASE:
            continue
        q = med / b[2]
        cells.append(f'{name} {q:.3f}')
        if q <= 0.90:
            clears.append((f[:-4] + ': ' + title, name, q, b[0]))
    others = ', '.join(f'{r[0]} {r[2]/b[2]:.3f}' for r in base if r is not b)
    print(f'| {f[:-4]}: {title} | {b[0]} {b[2]:.4f} ({others}) | {"; ".join(cells)} |')
print()
print('## Port balancing alone (the textbook with half its adds as FMA by 1, against the plain textbook and FFHT)\n')
print('A second lead, independent of the circuits: if the balanced textbook is 10 % or more faster than both the plain')
print('textbook and FFHT in whole transforms, an x86 WHT library (FFHT, used by SpinQuant on x86) gains by balancing alone.\n')
for (f, title), rows in groups.items():
    d = {r[0]: r[2] for r in rows}
    bal = d.get('tb16bal') or d.get('tb8bal') or d.get('textbook-bal')
    plain = [d[k] for k in ('tb16', 'tb8', 'textbook', 'FFHT') if k in d]
    if bal and plain:
        print(f'- {f[:-4]}: {title}: balanced / best other textbook-or-FFHT = {bal / min(plain):.3f}'
              + (f' (FFHT {d["FFHT"]:.4f}, plain textbook {d.get("textbook", 0):.4f}, balanced {bal:.4f} ns)' if 'FFHT' in d else ''))
print()
if clears:
    print('## Cases at or below 0.90 of the fastest baseline (CHECK the whole-transform rows before believing a pass row)\n')
    for t, n, q, bn in clears:
        print(f'- {t}: {n} {q:.3f} (baseline {bn})')
else:
    print('## No circuit reaches 0.90 of the fastest baseline in any test.')
