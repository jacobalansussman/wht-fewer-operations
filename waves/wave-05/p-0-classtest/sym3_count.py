#!/usr/bin/env python3
"""sym3_count.py (p-0-classtest): is "5 gates for S_tau at every tau modulo p" ONE circuit that moves with tau, or a different accident
at each tau?  Count the helper sets: S_tau padded with a fourth input that no row uses (so that the even-size tool mincirc_sets applies),
2 helpers allowed (5 gates).  A generic circuit shows as the same count at almost every tau; accidents show as small erratic counts.
Also prints one helper set per tau so that the dependence on tau can be read.  usage: sym3_count.py p"""
import sys, subprocess, os
here = os.path.dirname(os.path.abspath(__file__)); p = int(sys.argv[1]); hist = {}
for t in range(2, p):
    S = [[1, 2, 1, 0], [1, 1 + t, t, 0], [1, 2 * t, t * t, 0]]
    inp = '\n'.join(' '.join(str(x % p) for x in r) for r in S) + '\n'
    res = subprocess.run([os.path.join(here, 'mincirc_sets'), str(p), '4', '2', '100000000'], input=inp, capture_output=True, text=True).stdout
    sets = [line.split()[1:] for line in res.splitlines() if line.startswith('SET')]
    sets3 = [s for s in sets if all(h.split(',')[3] == '0' for h in s)]
    hist.setdefault(len(sets3), []).append(t)
    print('p=%d tau=%d: %d helper sets give 5 gates (not using the dummy input); e.g. %s' % (p, t, len(sets3), sets3[:2]), flush=True)
print('number of helper sets -> how many tau:', sorted((k, len(v)) for k, v in hist.items()))
print('tau with the largest counts:', sorted(hist.items())[-3:])
