#!/usr/bin/env python3
"""x-9-growinghubs/scan.py: run tgen.py over a grid of hub coefficients per level and tabulate the gate count.
Question: is there any (tau_2, ..., tau_k) other than +-1 for which a weighted witness coincides with a wire already held
(tgen.py deduplicates wires by vector, so a coincidence shows as a lower count)?   usage: scan.py k"""
import sys, subprocess, itertools, re, collections
k = int(sys.argv[1])
vals8 = ['1', '-1', 'i', '-i', '2', '-2', '1/2', '-1/2', '3', '-3', '1/3', '-1/3', '1+i', '1-i', '-1+i', '1/2+1/2i', '2i', '1/2i', '1+2i', '3/5+4/5i', '4', '5/3']
vals16 = ['1', '-1', 'i', '-i', '2', '1/2', '1+i', '3/5+4/5i', '3']
vals = vals8 if k == 3 else vals16
hist = collections.Counter(); best = {}
for combo in itertools.product(vals, repeat=k - 1):
    out = subprocess.run([sys.executable, '-B', 'tgen.py', str(k), ','.join(combo)], capture_output=True, text=True).stdout
    m = re.search(r'gates (\d+) .*exact: (\w+)', out)
    assert m and m.group(2) == 'True', (combo, out)
    g = int(m.group(1)); hist[g] += 1; best.setdefault(g, []).append(combo)
print('k', k, 'values per level', len(vals), 'runs', sum(hist.values()), 'every run replayed exactly as H')
for g in sorted(hist):
    ex = best[g][:6]
    print('  gates %d: %d schedules; e.g. %s' % (g, hist[g], '  '.join(','.join(c) for c in ex)))
low = sorted(hist)[0]
print('  ALL schedules with the least count %d:' % low, '  '.join(','.join(c) for c in best[low]))
