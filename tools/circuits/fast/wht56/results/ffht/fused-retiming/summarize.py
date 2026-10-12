# summarize.py -- read out/*.txt and print per-run and across-run figures
import re, sys, glob, statistics as st
def parse(path):
    runs = []; cur = None; hdr = {}
    for line in open(path):
        m = re.match(r'## (before|after): (\S+ \S+) UTC; load (\S+ \S+ \S+)', line)
        if m: hdr[m.group(1)] = (m.group(2), m.group(3))
        m = re.match(r'## waited (\d+) s', line)
        if m: hdr['waited'] = int(m.group(1))
        m = re.match(r'S k=(\d+) arrays=(\d+) bytes=\d+ G=(\d+) R=(\d+) cpu=(\d+) sibling=(\d+) sibling_busy=(-?\d+)%', line)
        if m:
            cur = {'k': int(m.group(1)), 'M': int(m.group(2)), 'cpu': int(m.group(5)), 'sib_busy': int(m.group(7)), 'V': {}, 'P': {}}
            runs.append(cur)
        m = re.match(r'V k=\d+ (\S+)\s+min=(\S+) med=(\S+) max=(\S+) ns/point\s+shortest_loop=(\S+)s', line)
        if m and cur is not None: cur['V'][m.group(1)] = (float(m.group(2)), float(m.group(3)), float(m.group(4)), float(m.group(5)))
        m = re.match(r'P k=\d+ (\S+) best/best=(\S+) med/med=(\S+)\s+repeat-by-repeat: min=(\S+) med=(\S+) max=(\S+)', line)
        if m and cur is not None: cur['P'][m.group(1)] = tuple(float(m.group(i)) for i in range(2, 7))
    return hdr, runs
files = sorted(glob.glob(sys.argv[1] + '/' + sys.argv[2] + '*.txt'))
acc = {}
for f in files:
    hdr, runs = parse(f)
    print('== %s  before %s  after %s  waited %s s' % (f.split('/')[-1], hdr.get('before'), hdr.get('after'), hdr.get('waited')))
    for r in runs:
        print('  k=%d arrays=%d cpu=%d sibling busy %d%%: ' % (r['k'], r['M'], r['cpu'], r['sib_busy']) + '  '.join('%s %.3f/%.3f(+%.0f%%)' % (n, v[0], v[1], 100 * (v[1] / v[0] - 1)) for n, v in r['V'].items()))
        for pn, p in r['P'].items():
            print('      %-14s best/best %.3f  med/med %.3f  repeat-by-repeat %.3f / %.3f / %.3f' % (pn, *p))
            acc.setdefault((r['k'], r['M'], pn), []).append((p[0], p[1], p[3], r['sib_busy'], r['cpu']))
        for n, v in r['V'].items(): acc.setdefault((r['k'], r['M'], 'ns:' + n), []).append((v[0], v[1], (v[1] / v[0] - 1) * 100, r['sib_busy'], r['cpu']))
print('\nACROSS RUNS')
for key in sorted(acc, key=lambda x: (x[1], x[0], x[2])):
    a = acc[key]
    if key[2].startswith('ns:'):
        print('k=%d arrays=%d %-12s n=%d  best: lowest %.3f median %.3f highest %.3f | median-of-9: lowest %.3f median %.3f highest %.3f | (med-best)/best %.0f..%.0f %%' % (key[0], key[1], key[2], len(a), min(x[0] for x in a), st.median(x[0] for x in a), max(x[0] for x in a), min(x[1] for x in a), st.median(x[1] for x in a), max(x[1] for x in a), min(x[2] for x in a), max(x[2] for x in a)))
    else:
        print('k=%d arrays=%d %-14s n=%d  best/best: %s -> lowest %.3f median %.3f highest %.3f | med/med: lowest %.3f median %.3f highest %.3f | paired median: lowest %.3f median %.3f highest %.3f | above 1 in %d of %d (best/best)' % (key[0], key[1], key[2], len(a), ' '.join('%.3f' % x[0] for x in a), min(x[0] for x in a), st.median(x[0] for x in a), max(x[0] for x in a), min(x[1] for x in a), st.median(x[1] for x in a), max(x[1] for x in a), min(x[2] for x in a), st.median(x[2] for x in a), max(x[2] for x in a), sum(1 for x in a if x[0] > 1), len(a)))
