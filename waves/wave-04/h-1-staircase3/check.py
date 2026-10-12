#!/usr/bin/env python3
"""h-1 check.py: independent exact replay of a helper set.  Count (G).
Reads helper vectors (one per line), finds an order in which every helper and every output a*u + b*v (a, b rational, solved exactly)
of two wires derived before it, writes the program, replays it from the inputs with Fractions and requires every output to be
exactly its row of H.  Shares no code with sa.c.   usage: check.py helpers.txt K [slp_out.txt]"""
import sys
from fractions import Fraction as F
fn, K = sys.argv[1], int(sys.argv[2]); N = 1 << K
H = [tuple(int(t) for t in l.split()) for l in open(fn) if l.strip() and l[0] != '#']
rows = [tuple(-1 if bin(a & x).count('1') & 1 else 1 for x in range(N)) for a in range(N)]
def solve2(u, v, p):
    for i in range(N):
        for j in range(i + 1, N):
            det = u[i] * v[j] - u[j] * v[i]
            if det:
                a = F(p[i] * v[j] - p[j] * v[i], det); b = F(u[i] * p[j] - u[j] * p[i], det)
                return (a, b) if all(a * u[t] + b * v[t] == p[t] for t in range(N)) else None
    return None
have = [('x%d' % i, tuple(int(i == j) for j in range(N))) for i in range(N)]
todo = [('h', w) for w in dict.fromkeys(H)] + [('y%d' % a, rows[a]) for a in range(N)]
prog = []; cnt = 0; ch = True
while todo and ch:
    ch = False; rest = []
    for kind, w in todo:
        hit = None
        for i in range(len(have)):
            for j in range(i):
                s = solve2(have[i][1], have[j][1], w)
                if s and s[0] != 0 and s[1] != 0: hit = (s[0], have[i][0], s[1], have[j][0]); break
            if hit: break
        if hit:
            cnt += 1; nm = kind if kind[0] == 'y' else 'h%d' % cnt
            prog.append((nm, hit, w)); have.append((nm, w)); ch = True
        else: rest.append((kind, w))
    todo = rest
if todo: print('NOT a circuit: %d wires not derivable' % len(todo)); sys.exit(1)
val = {'x%d' % i: [F(int(i == j)) for j in range(N)] for i in range(N)}
for nm, (a, u, b, v), w in prog: val[nm] = [a * s + b * t for s, t in zip(val[u], val[v])]
ok = all(tuple(val['y%d' % a]) == rows[a] for a in range(N))
coef = sorted({abs(c) for _, (a, _, b, _), _ in prog for c in (a, b)})
print('K=%d N=%d gates(G)=%d helpers=%d  every output exactly its row of H: %s  |coefficients| %s  textbook %d' % (K, N, len(prog), len(prog) - N, ok, [str(c) for c in coef], N * K))
if len(sys.argv) > 3:
    with open(sys.argv[3], 'w') as f:
        f.write('# count (G) program, %d-point Walsh-Hadamard transform, %d gates; name = a*u + b*v ; exact replay by check.py: %s\n' % (N, len(prog), ok))
        for nm, (a, u, b, v), w in prog: f.write('%s = %s * %s + %s * %s    # %s\n' % (nm, a, u, b, v, ' '.join(map(str, w)) if N <= 16 else ''))
