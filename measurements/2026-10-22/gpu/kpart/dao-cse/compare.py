"""compare.py ORIG_JSON CSE_JSON -- outputs equal (fp32, fixed input) and the time ratios cse/orig."""
import json, sys
o, c = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
print('GPU:', o['gpu'], '| torch', o['torch'])
for k in o['outputs']:
    a, b = o['outputs'][k], c['outputs'][k]
    m = max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb))
    s = max(abs(x) for ra in a for x in ra)
    print('check %-10s max |orig - cse| = %.3e (max |y| %.3e)  %s' % (k, m, s, 'PASS' if m <= 1e-5 * s else 'FAIL'))
print('| case | d | dtype | batch | orig us | cse us | cse/orig | pow2 us (size) | copy us |')
print('|---|---|---|---|---|---|---|---|---|')
for ro, rc in zip(o['rows'], c['rows']):
    print('| %s | %d | %s | %d | %.2f | %.2f | %.3f | %.2f (%d) | %.2f |' % (ro['case'], ro['d'], ro['dtype'].replace('torch.', ''), ro['B'], ro['us'], rc['us'], rc['us'] / ro['us'], ro['us_pow2'], ro['pow2'], ro['us_copy']))
