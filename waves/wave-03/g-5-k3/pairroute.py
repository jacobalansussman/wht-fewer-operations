#!/usr/bin/env python3
"""pairroute.py (g-5-k3): the 8^t-point Walsh-Hadamard transform built gate by gate, count (G), exact replay.
Each factor of 3 bits (x1, x2, x3): bits x1, x2 are a 'pair'.
  split : (x01, x10) -> (sum b, difference d) on every pair; over all t factors this is the transform on each swap orbit (7-gate bricks);
  middle: on a factor whose pair is symmetric (a = x00, b, c = x11) : the 12-gate brick for K3 (x) H2 (H2 on x3);
          on the antisymmetric lines: the transform on the x3 bits of those factors (7-gate bricks);
  merge : (K3 row 1 output, antisymmetric output) -> (F10, F01), again a transform on orbits (7-gate bricks).
usage: pairroute.py t"""
import sys, itertools
from fractions import Fraction as F
from k3 import hadamard, proportional
from brick12 import SC, brick12

def build(t):
    n = 8 ** t; c = SC(n)
    # label of a factor: ('raw', x1, x2, x3) -> ('p', letter in 'abcd', x3) -> ('m', r in 0..2 or 'd', u3) -> ('o', u1, u2, u3)
    raws = list(itertools.product(range(8), repeat=t))
    def raw_label(v): return ('raw', v >> 2 & 1, v >> 1 & 1, v & 1)
    cur = {tuple(raw_label(v) for v in p): i for i, p in enumerate(raws)}
    # ---- split
    new = {}; done = set()
    for key in list(cur):
        S = [i for i in range(t) if key[i][1] != key[i][2]]
        base = tuple(('raw', 0, 1, key[i][3]) if i in S else key[i] for i in range(t))
        if base in done: continue
        done.add(base); keys = []
        for idx in range(1 << len(S)):
            k = list(base)
            for b_, i in enumerate(S):
                if idx >> b_ & 1: k[i] = ('raw', 1, 0, base[i][3])
            keys.append(tuple(k))
        out = hadamard(c, [cur[k] for k in keys], True) if S else [cur[keys[0]]]
        for idx in range(1 << len(S)):
            lab = []
            for i in range(t):
                if i in S: lab.append(('p', 'd' if idx >> S.index(i) & 1 else 'b', base[i][3]))
                else: lab.append(('p', 'a' if base[i][1] == 0 else 'c', base[i][3]))
            new[tuple(lab)] = out[idx]
    cur = new; g_split = len(c.gates)
    # ---- middle, symmetric factors: brick12 along each factor in turn
    for i in range(t):
        new = dict(cur); done = set()
        for key in list(cur):
            if key[i][0] != 'p' or key[i][1] == 'd': continue
            rest = key[:i] + key[i + 1:]
            if rest in done: continue
            done.add(rest)
            def at(letter, x3): return cur[key[:i] + (('p', letter, x3),) + key[i + 1:]]
            o = brick12(c, at('a', 0), at('a', 1), at('b', 0), at('b', 1), at('c', 0), at('c', 1))
            for (r, j), node in o.items():
                del_key = None
                new[key[:i] + (('m', r, j),) + key[i + 1:]] = node
            for letter in 'abc':
                for x3 in (0, 1): new.pop(key[:i] + (('p', letter, x3),) + key[i + 1:], None)
        cur = new
    g_sym = len(c.gates) - g_split
    # ---- middle, antisymmetric lines: transform on the x3 bits of the antisymmetric factors
    new = {}; done = set()
    for key in list(cur):
        D = [i for i in range(t) if key[i][0] == 'p']            # still 'p' means letter d
        base = tuple(('p', 'd', 0) if i in D else key[i] for i in range(t))
        if base in done: continue
        done.add(base); keys = []
        for idx in range(1 << len(D)):
            k = list(base)
            for b_, i in enumerate(D):
                if idx >> b_ & 1: k[i] = ('p', 'd', 1)
            keys.append(tuple(k))
        out = hadamard(c, [cur[k] for k in keys], True) if D else [cur[keys[0]]]
        for idx in range(1 << len(D)):
            new[tuple(('m', 'd', idx >> D.index(i) & 1) if i in D else base[i] for i in range(t))] = out[idx]
    cur = new; g_anti = len(c.gates) - g_split - g_sym
    # ---- merge: (row 1, d) -> (F10 = P + D, F01 = P - D) on every factor
    new = {}; done = set()
    for key in list(cur):
        S = [i for i in range(t) if key[i][1] in (1, 'd')]
        base = tuple(('m', 1, key[i][2]) if i in S else key[i] for i in range(t))
        if base in done: continue
        done.add(base); keys = []
        for idx in range(1 << len(S)):
            k = list(base)
            for b_, i in enumerate(S):
                if idx >> b_ & 1: k[i] = ('m', 'd', base[i][2])
            keys.append(tuple(k))
        out = hadamard(c, [cur[k] for k in keys], True) if S else [cur[keys[0]]]
        for idx in range(1 << len(S)):
            lab = []
            for i in range(t):
                if i in S: lab.append(('o', 0, 1, base[i][2]) if idx >> S.index(i) & 1 else ('o', 1, 0, base[i][2]))
                else: lab.append(('o', 0, 0, base[i][2]) if base[i][1] == 0 else ('o', 1, 1, base[i][2]))
            new[tuple(lab)] = out[idx]
    cur = new; g_merge = len(c.gates) - g_split - g_sym - g_anti
    return c, cur, raws, (g_split, g_sym, g_anti, g_merge)

if __name__ == '__main__':
    t = int(sys.argv[1]); c, cur, raws, parts = build(t); n = 8 ** t; ok = len(cur) == n
    def bits(p): return [b for v in p for b in (v >> 2 & 1, v >> 1 & 1, v & 1)]
    xb = [bits(p) for p in raws]
    for key, node in cur.items():
        ub = [b for lab in key for b in lab[1:]]
        row = [F(-1 if sum(a * b for a, b in zip(ub, x)) & 1 else 1) for x in xb]
        if proportional(c.rows[node], row) is None: ok = False
    k = 3 * t; text = k * 2 ** k
    bk = (k // 2) * 7 * 2 ** (k - 2) + (k % 2) * 2 ** k
    mx = max(max(abs(a), abs(b)) for (_, _, a, b) in c.gates)
    print('t=%d: %d points: %d gates (split %d + bricks for K3(x)H2 %d + antisymmetric lines %d + merge %d); all %d outputs proportional to the rows of the transform: %s'
          % (t, n, len(c.gates), parts[0], parts[1], parts[2], parts[3], n, ok))
    print('      textbook %d ; product of 7-gate bricks %d ; ratio to textbook %.5f ; largest coefficient in a gate %s' % (text, bk, len(c.gates) / text, mx))
