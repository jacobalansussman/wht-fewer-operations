"""compare3.py ORIG_JSON OTHER_JSON... -- ay-h0: outputs equal to Dao's original (fp32, fixed input), and time ratios
other/orig per case.  Variants: cse (ax-h0's greedy circuit), grp (groups of 4, the published structured form),
mm (pow2 transform + K x K matmul, QuaRot style)."""
import json, sys
o = json.load(open(sys.argv[1])); others = [json.load(open(p)) for p in sys.argv[2:]]
print('GPU:', o['gpu'], '| torch', o['torch'])
for c in others:
    for k in o['outputs']:
        if k not in c['outputs']: print('check %-4s %-10s MISSING' % (c['tag'], k)); continue
        a, b = o['outputs'][k], c['outputs'][k]
        m = max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb)); s = max(abs(x) for ra in a for x in ra)
        print('check %-4s %-10s max |orig - %s| = %.3e (max |y| %.3e)  %s' % (c['tag'], k, c['tag'], m, s, 'PASS' if m <= 1e-5 * s else 'FAIL'))
idx = lambda r: (r['case'], r['d'], r['dtype'], r['B'])
print('| case | d | dtype | batch | orig us | ' + ' | '.join('%s us (x orig)' % c['tag'] for c in others) + ' | pow2 us (size) | copy us |')
print('|---|---|---|---|---|' + '---|' * len(others) + '---|---|')
maps = [{idx(r): r for r in c['rows']} for c in others]
for ro in o['rows']:
    cells = []
    for mp in maps:
        r = mp.get(idx(ro)); cells.append('%.2f (%.3f)' % (r['us'], r['us'] / ro['us']) if r else '-')
    print('| %s | %d | %s | %d | %.2f | %s | %.2f (%d) | %.2f |' % (ro['case'], ro['d'], ro['dtype'].replace('torch.', ''), ro['B'], ro['us'], ' | '.join(cells), ro['us_pow2'], ro['pow2'], ro['us_copy']))
