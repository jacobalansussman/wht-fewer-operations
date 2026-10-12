#!/usr/bin/env python3
# h-5 / meters2.py : three meters on the 20-gate (e2-0) and 19-gate (g-1) programs at 8 points, exact integers/fractions.
#  s, s'                    non-zeros in the inputs / in the outputs
#  B(w)                     bits on which w is entangled (cut bit | rest has rank 2), coordinate bits
#  Bmin(w)                  least |B| over all 168 relabellings of the addresses by an invertible bit matrix
#  births of a gate         the pairs (bit i, sign t) such that the result lies in K(i,t) = {t on bit i, anything on the rest} and its parents do not
#  increments               births that raise dim span{wires in K(i,t)}   (they must total N log2 N = 24)
import sys, re, itertools
from fractions import Fraction
N = 8
class V(tuple):
    def __add__(s, o): return V(a + b for a, b in zip(s, o))
    def __sub__(s, o): return V(a - b for a, b in zip(s, o))
    def __neg__(s): return V(-a for a in s)
    def __rmul__(s, c): return V(c * a for a in s)
    def __mul__(s, c): return V(c * a for a in s)
def load(path):
    env = {'x%d' % i: V(int(i == j) for j in range(N)) for i in range(N)}
    gates = []
    for line in open(path):
        line = line.split('#')[0].strip()
        if '=' not in line: continue
        name, expr = [t.strip() for t in line.split('=')]
        par = [t for t in re.findall(r'[a-z]+\d+', expr)]
        env[name] = eval(expr, {}, env)
        gates.append((name, par, env[name]))
    return env, gates
def had(w): return tuple(sum((-1) ** bin(c & x).count('1') * w[x] for x in range(N)) for c in range(N))
def rank1(a, b):   # two 4-vectors proportional (or one zero)?
    return all(a[i] * b[j] == a[j] * b[i] for i in range(4) for j in range(i + 1, 4))
def B(w):
    out = []
    for i in range(3):
        lo = [w[x] for x in range(N) if not (x >> i) & 1]; hi = [w[x] for x in range(N) if (x >> i) & 1]
        if not rank1(lo, hi): out.append(i)
    return tuple(out)
def mats():
    for rows in itertools.product(range(1, 8), repeat=3):
        img = [sum(((bin(rows[i] & x).count('1') & 1) << i) for i in range(3)) for x in range(N)]
        if len(set(img)) == N: yield img
MATS = list(mats())
def Bmin(w): return min(len(B(tuple(w[m[x]] for x in range(N)))) for m in MATS)
def inK(w, i, t):  # w(x with bit i = 1) = t * w(x with bit i = 0)
    return all(w[x | (1 << i)] == t * w[x] for x in range(N) if not (x >> i) & 1)
def rank(rows):
    M = [[Fraction(a) for a in r] for r in rows]; r = 0
    for c in range(N):
        p = next((i for i in range(r, len(M)) if M[i][c]), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        for i in range(len(M)):
            if i != r and M[i][c]:
                f = M[i][c] / M[r][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
    return r
for path in sys.argv[1:]:
    env, gates = load(path)
    print('==', path, len(gates), 'gates')
    held = {(i, t): [] for i in range(3) for t in (1, -1)}
    tot = {0: 0, 1: 0, 2: 0, 3: 0}; totb = {0: 0, 1: 0, 2: 0, 3: 0}; ent = 0
    for name, par, w in gates:
        s = sum(1 for a in w if a); s2 = sum(1 for a in had(w) if a)
        births = [(i, t) for i in range(3) for t in (1, -1) if inK(w, i, t) and not any(inK(env[p], i, t) for p in par)]
        inc = []
        for (i, t) in births:
            if rank(held[(i, t)] + [w]) > len(held[(i, t)]): inc.append((i, t))
        for i in range(3):
            for t in (1, -1):
                if inK(w, i, t) and rank(held[(i, t)] + [w]) > rank(held[(i, t)]) if held[(i, t)] else inK(w, i, t): held[(i, t)].append(w)
        b = B(w); tot[len(inc)] += 1; totb[len(births)] += 1; ent += (len(b) > 0)
        print('  %-6s %-28s s=%d s\'=%d s*s\'/N=%-4s entangled on bits %-9s best basis: %d  parents widths %s births %d increments %d' % (
            name, ' '.join('%2d' % a for a in w), s, s2, Fraction(s * s2, N), b, Bmin(w), [len(B(env[p])) for p in par], len(births), len(inc)))
    G = len(gates)
    print('  gates %d ; by increments: double %d, single %d, zero %d ; sum of increments %d ; 24 - double + zero = %d ; entangled wires %d ; by births: %s'
          % (G, tot[2] + tot[3], tot[1], tot[0], tot[1] + 2 * tot[2] + 3 * tot[3], 24 - tot[2] - 2 * tot[3] + tot[0], ent, totb))
