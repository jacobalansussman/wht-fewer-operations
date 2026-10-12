#!/usr/bin/env python3
"""h-1 anat.py: write a program's wires in the 'chain' language.  Exact integers.
Address bits are numbered 0 (pairs) upward.  A wire is factored as a tensor product over groups of address bits (finest partition
across which it is a product).  One-bit factors are printed as 0, 1 (the address bit is fixed: the wire lives on that half),
+ , - (a character on that bit), or (a,b).  A factor on two or three bits is printed as its sign pattern: these are the hubs.
usage: anat.py helpers.txt K [relabel-matrix rows as integers, lowest new bit first]"""
import sys, itertools
from fractions import Fraction as F
fn, K = sys.argv[1], int(sys.argv[2]); N = 1 << K
H = [tuple(int(t) for t in l.split()) for l in open(fn) if l.strip() and l[0] != '#']
rows = [tuple(-1 if bin(a & x).count('1') & 1 else 1 for x in range(N)) for a in range(N)]
A = [int(t) for t in sys.argv[3:3 + K]] if len(sys.argv) > 3 else [1 << i for i in range(K)]
def relabel(w):
    v = [0] * N
    for x in range(N):
        z = 0
        for i in range(K):
            if bin(A[i] & x).count('1') & 1: z |= 1 << i
        v[z] = w[x]
    return tuple(v)
def rank1(w, bits):
    """is w a product across (bits | rest)?  returns the factor on bits (normalised) or None"""
    rest = [b for b in range(K) if b not in bits]
    def idx(p, q):
        x = 0
        for i, b in enumerate(bits):
            if p >> i & 1: x |= 1 << b
        for i, b in enumerate(rest):
            if q >> i & 1: x |= 1 << b
        return x
    M = [[w[idx(p, q)] for q in range(1 << len(rest))] for p in range(1 << len(bits))]
    piv = None
    for q in range(1 << len(rest)):
        col = [M[p][q] for p in range(1 << len(bits))]
        if any(col): piv = col; break
    for q in range(1 << len(rest)):
        col = [M[p][q] for p in range(1 << len(bits))]
        # col must be a multiple of piv
        i0 = next(i for i, t in enumerate(piv) if t)
        r = F(col[i0], piv[i0])
        if any(F(c) != r * t for c, t in zip(col, piv)): return None
    return tuple(piv)
def factor(w):
    left = list(range(K)); parts = []
    while left:
        done = False
        for size in range(1, len(left) + 1):
            for bits in itertools.combinations(left, size):
                if bits[0] != left[0]: continue
                f = rank1(w, list(bits))
                if f is not None or size == len(left):
                    if f is None: f = w
                    parts.append((bits, f)); left = [b for b in left if b not in bits]; done = True; break
            if done: break
    return parts
def show(f):
    g = next(t for t in f if t); f = tuple(t // abs(g) * (1 if g > 0 else -1) if False else t for t in f)
    if len(f) == 2:
        return {(1, 0): '0', (0, 1): '1', (1, 1): '+', (1, -1): '-', (-1, 1): '-', (-1, -1): '+', (0, -1): '1', (-1, 0): '0'}.get(f, str(f))
    return '[' + ''.join('+' if t > 0 else '-' if t < 0 else '.' for t in f) + ']'
def wht(w):
    return [sum(a * b for a, b in zip(w, r)) for r in rows]
print('# %s, K=%d ; columns: s, s\', s*s\'/N, entangled groups of bits, factors (bits: factor)' % (fn, K))
tot = {}
for w0 in H:
    w = relabel(w0); parts = factor(w); s = sum(1 for t in w if t); sp = sum(1 for t in wht(w) if t)
    ent = [b for b, f in parts if len(b) > 1]
    desc = '  '.join('%s:%s' % (''.join(map(str, b)), show(f)) for b, f in parts)
    key = (s, sp, tuple(ent)); tot[key] = tot.get(key, 0) + 1
    print('s=%2d s\'=%2d ratio %2d  entangled %-10s  %s    %s' % (s, sp, s * sp // N, ','.join(''.join(map(str, b)) for b in ent) or '-', desc, ''.join('+' if t > 0 else '-' if t < 0 else '.' for t in w)))
print('# census (s, s\', entangled groups): count')
for k_, c in sorted(tot.items()): print('#  ', k_, c)
