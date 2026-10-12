#!/usr/bin/env python3
"""b-0: sanity for wall_dfs.py.  Is e2-0's 20-gate program (slp_8.txt) a legal leaf of that search: are all its 20 values points of
the class, and is every one of its gates in the table of one-gate derivations?  (Then the search at cap 20 would accept it.)"""
import re
src = open('wall_dfs.py').read().split("outs = [idx[o] for o in outputs]")[0].replace("CAP = int(sys.argv[1]); ", "CAP = 20; ")
exec(src)
from fractions import Fraction as Fr
val = {'x%d' % i: [Fr(int(i == j)) for j in range(N)] for i in range(N)}; ok = True; n = 0
for line in open('waves/wave-02/e2-0-pieces/slp_8.txt'):
    line = line.split('#')[0].strip()
    if not line: continue
    t, a, u, b, v = re.fullmatch(r'(\w+) = (\S+) \* (\w+) \+ (\S+) \* (\w+)', line).groups()
    val[t] = [Fr(a) * p + Fr(b) * q for p, q in zip(val[u], val[v])]; n += 1
    P, U, V = (canon(tuple(int(z) for z in val[w])) for w in (t, u, v))
    inpool = P in idx and idx[P] >= nI
    inder = inpool and ((idx[U], idx[V]) in ders[idx[P]] or (idx[V], idx[U]) in ders[idx[P]])
    ok = ok and inpool and inder
    if not (inpool and inder): print('NOT in class or table:', t, P)
print('gates', n, '| all values in the class and all gates in the derivation table:', ok)
