#!/usr/bin/env python3
"""shearrank.py [ad-5-whichbent]  Exact, exhaustive.  m = 3 (the half-address of 64 points), also m = 2.
A map s from m bits to m bits is written as a sum (bit by bit modulo 2) of ELEMENTARY terms v * [w in F], F a flat or the
complement of a flat, v a fixed vector: each term is one 'controlled shift' whose convolution costs about 2N gates (one
coset sum per column, one combination per point).  Constants are free (a relabelling).  FLAT-SHEAR RANK = least number of
terms.  Breadth-first over ALL 2^(m(2^m - 1)) maps with s(0) = 0."""
import itertools, sys
import numpy as np
from collections import Counter
def par(x): return bin(x).count("1") & 1
for m in (2, 3):
    q = 1 << m; pts = list(range(q))
    # all flats: solution sets of systems; enumerate as cosets of spans
    subs = {frozenset([0])}
    grow = True
    while grow:
        grow = False
        for S in list(subs):
            for v in pts:
                if v not in S:
                    T = frozenset(S | {x ^ v for x in S})
                    if T not in subs: subs.add(T); grow = True
    flats = {frozenset(x ^ a for x in S) for S in subs for a in pts}
    gens = set()
    for F in flats:
        for v in range(1, q):
            val = [v if w in F else 0 for w in pts]
            if val[0]: val = [x ^ v for x in val]          # normalise: value 0 at w = 0 (constants are free)
            code = 0
            for w in range(1, q): code |= val[w] << (m * (w - 1))
            if code: gens.add(code)
    gens = np.array(sorted(gens), dtype=np.int64)
    size = 1 << (m * (q - 1))
    dist = np.full(size, -1, dtype=np.int8); dist[0] = 0
    front = np.array([0], dtype=np.int64); d = 0
    while len(front):
        d += 1; new = []
        for t in gens:
            c = front ^ t; c = c[dist[c] < 0]
            if len(c): dist[c] = d; new.append(c)
        front = np.unique(np.concatenate(new)) if new else np.array([], dtype=np.int64)
    print("m=%d: %d flats, %d elementary terms (up to constants); all %d maps reached; rank histogram over all maps: %s"
          % (m, len(flats), len(gens), int((dist >= 0).sum()), dict(sorted(Counter(dist.tolist()).items()))), flush=True)
    hist = Counter()
    for p in itertools.permutations(range(1, q)):
        code = 0
        for w in range(1, q): code |= p[w - 1] << (m * (w - 1))
        s = (0,) + p
        # invariant of the class: number of non-zero c with c . s(w) of degree at most 1 (an affine function of w)
        aff = 0
        for c in range(1, q):
            f = [par(c & s[w]) for w in pts]
            if all(f[a ^ b ^ e] == f[a] ^ f[b] ^ f[e] for a in pts for b in pts for e in pts): aff += 1   # f affine with f(0)=0
        hist[(aff, int(dist[code]))] += 1
    print("   bijections fixing 0, by (number of affine combinations of the output bits, flat-shear rank): count")
    for key in sorted(hist, reverse=True): print("     affine combinations %d, rank %d: %d bijections" % (key[0], key[1], hist[key]))
    print("   least rank of a bijection: %d (lemma: at least m = %d)" % (min(r for (_, r) in hist), m))
