#!/usr/bin/env python3
"""hubless.py (p-0-classtest): print the 7-gate circuits at 4 points that have NO helper of full support (they exist only for special tau).
usage: hubless.py p tau"""
import sys, subprocess, os, itertools
here = os.path.dirname(os.path.abspath(__file__)); p = int(sys.argv[1]); tau = int(sys.argv[2]) % p
rows = [tuple(pow(tau, bin(w & x).count('1'), p) for x in range(4)) for w in range(4)]
def canon(v):
    f = next(x for x in v if x); iv = pow(f, -1, p); return tuple(x * iv % p for x in v)
def comb(w, u, v):
    for a in range(p):
        for b in range(p):
            if (a or b) and canon(tuple((a * x + b * y) % p for x, y in zip(u, v))) == canon(w) if any((a * x + b * y) % p for x, y in zip(u, v)) else False:
                return a, b
    return None
inp = '\n'.join(' '.join(map(str, r)) for r in rows) + '\n'
res = subprocess.run([os.path.join(here, 'mincirc_sets'), str(p), '4', '3', '100000000'], input=inp, capture_output=True, text=True).stdout
sets = [[tuple(int(x) for x in s.split(',')) for s in line.split()[1:]] for line in res.splitlines() if line.startswith('SET')]
E = [tuple(int(i == j) for j in range(4)) for i in range(4)]
sgn = lambda x: x if x <= p // 2 else x - p
for S in sets:
    if any(all(h) for h in S): continue
    names = ['x%d' % i for i in range(4)] + ['h%d' % i for i in range(3)] + ['r%d%d' % (w >> 1, w & 1) for w in range(4)]
    pts = E + S + [canon(r) for r in rows]
    have = list(range(4)); todo = list(range(4, 11)); lines = []
    while todo:
        for n in todo:
            hit = next(((a, b) for a in have for b in have if a < b and comb(pts[n], pts[a], pts[b])), None)
            if hit:
                ca, cb = comb(pts[n], pts[hit[0]], pts[hit[1]])
                lines.append('%s%s = %d*%s + %d*%s' % (names[n], [sgn(x) for x in pts[n]], sgn(ca), names[hit[0]], sgn(cb), names[hit[1]])); have.append(n); todo.remove(n); break
        else: lines.append('STUCK'); break
    print(' ; '.join(lines))
