#!/usr/bin/env python3
"""analyze.py (ag-8-bestbadcircuit): take the specimens printed by census8.py (labelled wirings found modulo p) and, for each,
 (1) solve the wiring EXACTLY at tau = -1 (fractions; wsolve.solve) and print the circuit with whole-number wires,
 (2) test the wiring against a general kernel in all 576 renamings of inputs and outputs (modulo 2^61-1 at a random tau),
 (3) report what it contains: supports, wires that are sums of few rows, eigenvectors of H, gates that read an output,
     coefficients (a halving shows as a denominator 2 between primitive wires).
usage: analyze.py census_file m [SPECIAL|MIXED|COMMON|ABSENT]"""
import sys, re, random, itertools
from fractions import Fraction as F
from math import gcd
import wsolve
from wsolve import solve, P, MODE
fn = sys.argv[1]; m = int(sys.argv[2]); which = sys.argv[3] if len(sys.argv) > 3 else 'SPECIAL'
random.seed(88)
txt = open(fn).read().split('\n')
specs = []; sect = None
for i, l in enumerate(txt):
    if l.startswith('SPECIAL shapes'): sect = 'SPECIAL'
    elif l.startswith('MIXED shapes'): sect = 'MIXED'
    elif l.startswith('COMMON shapes'): sect = 'COMMON'
    elif l.startswith('shapes absent at the transform, spec'): sect = 'ABSENT'
    elif l.startswith('COMMONSPEC'): sect = 'COMMON'
    if '<-(' in l and sect == which:
        name = txt[i - 1].split()[0] if i else '?'
        g = re.findall(r'([hT])(\d+)=([\d,]+)<-\((\d+),(\d+)\)', l)
        specs.append((name, [(int(n), int(a), int(b)) for k, n, pt, a, b in g]))
N = 4
H = [tuple((-1) ** bin(w & x).count('1') for x in range(4)) for w in range(4)]
def nm(n): return 'x%d' % n if n < 4 else ('h%d' % n if n < 4 + m else 'T%d' % n)
def prim(v):
    den = 1
    for x in v: den = den * F(x).denominator // gcd(den, F(x).denominator)
    w = [int(x * den) for x in v]; g = 0
    for x in w: g = gcd(g, abs(x))
    w = [x // g for x in w]
    if next(x for x in w if x) < 0: w = [-x for x in w]
    return tuple(w)
def topo(gl):
    done = set(range(4)); order = []; rest = list(gl)
    while rest:
        for g in rest:
            if g[1] in done and g[2] in done: order.append(g); done.add(g[0]); rest.remove(g); break
        else: raise SystemExit('cyclic')
    return order
PERMS = list(itertools.permutations(range(4)))
tally = {}
for name, gl in specs:
    gl = topo(gl); gates = [(nm(n), nm(a), nm(b)) for n, a, b in gl]; out = {nm(4 + m + w): w for w in range(4)}
    MODE['q'] = True
    try: r = solve(4, gates, out, F(-1))
    finally: MODE['q'] = False
    print('\n%s  gates=%d   exact solve at tau=-1: %s' % (name, len(gates), r[0]))
    yes = und = 0; t = random.randrange(2, P - 2)
    for s in PERMS:
        for rho in PERMS:
            q = solve(4, gates, out, t, list(s), list(rho))
            if q[0].startswith('YES'): yes += 1
            elif q[0] == 'UNDECIDED': und += 1
    print('   general kernel (random tau modulo 2^61-1), 576 renamings: YES %d, undecided %d  => %s' % (yes, und, 'OF THE CLASS' if yes else ('SPECIAL' if not und else 'special unless an undecided renaming works')))
    if not r[0].startswith('YES'): print('   (not solved by propagation: %s)' % (r[1],)); continue
    pts = {k: prim(v) for k, v in r[1]['pts'].items()}
    feats = []
    for g, u, v in gates:
        # coefficients g = a u + b v with primitive whole-number wires
        U, V, G = pts[u], pts[v], pts[g]; ab = None
        for i in range(4):
            for j in range(i + 1, 4):
                det = U[i] * V[j] - U[j] * V[i]
                if det: ab = (F(G[i] * V[j] - G[j] * V[i], det), F(U[i] * G[j] - U[j] * G[i], det)); break
            if ab: break
        # row content: g = sum c_w r_w / 4
        c = [sum(G[x] * H[w][x] for x in range(4)) for w in range(4)]
        eig = all(c[x] * G[0] == c[0] * G[x] for x in range(4)) if G[0] else all(c[x] * G[next(i for i in range(4) if G[i])] == c[next(i for i in range(4) if G[i])] * G[x] for x in range(4))
        sin = sum(1 for x in G if x); sout = sum(1 for x in c if x)
        note = []
        if ab[0].denominator > 1 or ab[1].denominator > 1: note.append('HALVING'); feats.append('halving')
        if eig: note.append('eigenvector of H'); feats.append('eigenvector')
        if g.startswith('h') and (u.startswith('T') or v.startswith('T')): note.append('helper reads an output'); feats.append('helper reads output')
        if g.startswith('h') and sin * sout > 4: note.append('over the limit (in %d x out %d)' % (sin, sout)); feats.append('over-limit')
        if max(abs(ab[0]), abs(ab[1])) > 2: feats.append('coefficient > 2')
        print('   %-3s = %5s * %-3s + %5s * %-3s   %-16s rows:%-18s %s' % (g, ab[0], u, ab[1], v, G, c, '; '.join(note)))
    hs = sorted(sum(1 for x in pts[g] if x) for g, u, v in gates if g.startswith('h'))
    key = (tuple(hs), tuple(sorted(set(feats))), 'class' if yes else 'special')
    tally[key] = tally.get(key, 0) + 1
print('\nTALLY (helper supports, features, verdict): count')
for k, v in sorted(tally.items(), key=repr): print('  ', k, v)
