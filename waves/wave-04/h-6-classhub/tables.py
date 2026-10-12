#!/usr/bin/env python3
"""h-6-classhub / tables.py : read two exact programs written by solve19.py (same wiring, two values of tau) and decide whether every
wire is tau^(integer table) on its support up to one scalar; if so classify each gate as join / shift (as gatekinds.py).
usage: tables.py file_tauA tauA file_tauB tauB"""
import sys, re
from fractions import Fraction as F
def load(path, tau):
    tau = F(tau); wires = {}; gates = []
    for line in open(path):
        if line.startswith('#') or '=' not in line: continue
        m = re.match(r'^(\S+) = (\S+) \+ (\S+) \* (\S+)\s+# (.*)$', line.strip())
        nm, u, th, v, vals = m.groups(); vals = [F(t) for t in vals.split()]; u = u.split('*')[-1]
        lead = next(t for t in vals if t); e = []
        for t in vals:
            if t == 0: e.append(None); continue
            t = t / lead; a = 0; ok = True
            for _ in range(40):
                if t == 1: break
                if abs(t) > 1: t /= tau; a += 1
                else: t *= tau; a -= 1
            e.append(a if t == 1 else 'x')
        wires[nm] = e; gates.append((nm, u, v))
    return wires, gates
A, gates = load(sys.argv[1], sys.argv[2]); B, _ = load(sys.argv[3], sys.argv[4])
N = len(next(iter(A.values())))
for i in range(N): A['x%d' % i] = [0 if j == i else None for j in range(N)]
bad = [nm for nm in B if A[nm] != B[nm] or 'x' in A[nm]]
print('wires', len(B), '| wires that are NOT tau^(one integer table) at both tau:', len(bad), bad[:8])
kinds = {}
for nm, u, v in gates:
    if nm in bad or u in bad or v in bad: kinds['touches a non-table wire'] = kinds.get('touches a non-table wire', 0) + 1; continue
    eu, ev, ew = A[u], A[v], A[nm]
    su = {x for x in range(N) if eu[x] is not None}; sv = {x for x in range(N) if ev[x] is not None}
    if not su & sv: kind = 'join'
    else:
        big, small, eb = (su, sv, eu) if sv <= su else (sv, su, ev)
        if not small <= big: kind = 'other'
        else:
            off = {ew[x] - eb[x] for x in big - small}; on = {ew[x] - eb[x] for x in small} if all(ew[x] is not None for x in small) else {'cut'}
            if len(on) == 1 and len(off) == 1 and 'cut' not in on: kind = 'shift %+d' % (on.pop() - off.pop())
            elif on == {'cut'} and len(off) == 1: kind = 'cut'
            else: kind = 'other'
    kinds[kind] = kinds.get(kind, 0) + 1
print('kinds of gate:', dict(sorted(kinds.items())))
for nm in bad: print('  non-table wire', nm, 'entries at the first tau:', [l for l in open(sys.argv[1]) if l.startswith(nm + ' =')][0].strip())
