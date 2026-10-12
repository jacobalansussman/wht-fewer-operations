# ab-5: for every non-zero form w over the two-element field on 8 points (not an input), the least number of
# gates for subset sums Z_8 when w is available at no cost.  Tool: mincirc_free (d-0's exhaustive search + free start forms).
# Known answer without w: 12 (checked first).  Output: saving(w) = 12 - gates(w).
import subprocess, sys, os, collections
here = os.path.dirname(os.path.abspath(__file__))
def run(m, free=None):
    args = [os.path.join(here, 'mincirc_free'), '2', '8', str(m), os.path.join(here, 'rows_zeta3.txt')]
    if free is not None:
        fn = os.path.join(here, 'free_tmp.txt')
        open(fn, 'w').write(' '.join(str((free >> i) & 1) for i in range(8)) + '\n')
        args.append(fn)
    out = subprocess.run(args, capture_output=True, text=True).stdout
    budget = int(out.split('gate budget')[1].split()[0])
    return ('YES' in out), budget
# check: no free form
assert run(4)[0] is False and run(5) == (True, 12)
print('check: Z_8 without free form: 12 gates, not 11 (two-element field)  OK')
names = lambda w: '+'.join('x%d' % i for i in range(8) if (w >> i) & 1)
zrows = {sum(1 << t for t in range(8) if (t & s) == t): s for s in range(8)}
res = {}
for w in range(1, 256):
    if bin(w).count('1') == 1: continue
    for m in range(0, 6):
        ok, budget = run(m, w)
        if ok: res[w] = budget; break
hist = collections.Counter(12 - g for g in res.values())
print('forms tried:', len(res))
print('saving -> number of forms:', dict(sorted(hist.items())))
for sv in sorted(hist, reverse=True):
    if sv >= 2:
        print('saving', sv, ':')
        for w, g in sorted(res.items()):
            if 12 - g == sv:
                tag = ' (output y_%s)' % format(zrows[w], '03b') if w in zrows else ''
                print('   gates %2d  w = %s%s' % (g, names(w), tag))
