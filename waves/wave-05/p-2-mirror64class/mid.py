#!/usr/bin/env python3
"""mid.py (p-2-mirror64class): the MIDDLE TABLE between the two type frames, exact integers.
Read frame: for every non-empty set S of digits, the start points of type3.py's scheme on the digits of S, e0 elsewhere
(3^n - 2^n points for |S| = n >= 2, one point for n = 1): 4^m - 3^m points in all.  Write frame: the image of the read frame
under tau (x) ... (x) tau, tau(x0,x1,x2,x3) = (-x3, x1, x2, -x0), which carries the read side to the write side.
Middle[b', b] = (write point b') . (read point b) / 2   (the mirror matrix M = I - R^m satisfies M M = 2 M).
Reports: size, rank, non-zeros, rows with one / two-or-more non-zeros, distinct heavy rows, and the cost bracket
  lower = distinct rows with >= 2 non-zeros,  upper = sum over those rows of (non-zeros - 1).
usage: mid.py mmax [variant]"""
import sys, itertools
from fractions import Fraction as Fr
mmax = int(sys.argv[1]); variant = sys.argv[2] if len(sys.argv) > 2 else "default"
e = [[1 if i == j else 0 for j in range(4)] for i in range(4)]
eps = {1: e[1], 2: e[2], 3: [0, 0, 0, -1]}; u = [1, 1, 1, 0]; w = [0, 1, 1, -1]
v = {j: [a - b for a, b in zip(eps[j], u)] for j in (1, 2, 3)}
def ten(*fs):
    out = [1]
    for f in fs: out = [a*b for a in out for b in f]
    return tuple(out)
def sub(a, b): return tuple(x - y for x, y in zip(a, b))
def q(J): return sub(ten(*[eps[j] for j in J]), ten(*[v[j] for j in J])) if len(J) > 1 else tuple(u)
base = 1 if variant == "default" else int(variant[-1])          # which digit value the slice uses
others = [a for a in (1, 2, 3) if a != base]
def d(a): return [x - y for x, y in zip(eps[base], eps[a])]
def start_points(n, prefix=()):
    P = lambda J: ten(*prefix, q(J)) if prefix else q(J)
    if n == 1: return [P((1,))]
    st = [P((base,) + Jp) for Jp in itertools.product((1, 2, 3), repeat=n-1)]
    for a in others: st += start_points(n-1, prefix + (d(a),))
    return st
def embed(vS, S, m):
    n = len(S); out = {}
    for idx, val in enumerate(vS):
        if val == 0: continue
        digs = [(idx // 4**(n-1-t)) % 4 for t in range(n)]; full = [0]*m
        for t, pos in enumerate(S): full[pos] = digs[t]
        I = 0
        for g in full: I = I*4 + g
        out[I] = val
    return out
def tau(vec, m):
    out = {}
    for I, val in vec.items():
        digs = [(I // 4**(m-1-t)) % 4 for t in range(m)]; sg = 1; nd = []
        for g in digs:
            if g == 0: nd.append(3); sg = -sg
            elif g == 3: nd.append(0); sg = -sg
            else: nd.append(g)
        J = 0
        for g in nd: J = J*4 + g
        out[J] = sg*val
    return out
def rank(rows):
    A = [[Fr(x) for x in r] for r in rows]; r = 0
    for c in range(len(A[0])):
        p = next((i for i in range(r, len(A)) if A[i][c] != 0), None)
        if p is None: continue
        A[r], A[p] = A[p], A[r]
        for i in range(r+1, len(A)):
            if A[i][c] != 0:
                f = A[i][c]/A[r][c]; A[i] = [x - f*y for x, y in zip(A[i], A[r])]
        r += 1
    return r
print("variant:", variant)
for m in range(2, mmax+1):
    N = 4**m; frame = []; typ = []
    for n in range(1, m+1):
        sp = start_points(n)
        for S in itertools.combinations(range(m), n):
            for vS in sp: frame.append(embed(vS, S, m)); typ.append(S)
    wframe = [tau(c, m) for c in frame]; rt = len(frame)
    Mid = [[sum(val*c.get(I, 0) for I, val in wv.items()) for c in frame] for wv in wframe]
    assert all(x % 2 == 0 for row in Mid for x in row); Mid = [[x//2 for x in row] for row in Mid]
    nnz = sum(1 for row in Mid for x in row if x)
    rows1 = sum(1 for row in Mid if sum(1 for x in row if x) == 1); rows0 = sum(1 for row in Mid if not any(row))
    seen = set(); lo = hi = 0
    for row in Mid:
        nzc = [x for x in row if x]
        if len(nzc) >= 2:
            f = nzc[0]; key = tuple(Fr(x, f) for x in row)
            if key not in seen: seen.add(key); lo += 1; hi += len(nzc) - 1
    rk = rank(Mid) if m <= 3 else "not run"
    blocks = {}
    for i in range(rt):
        for j in range(rt):
            if Mid[i][j]: blocks[(typ[i], typ[j])] = blocks.get((typ[i], typ[j]), 0) + 1
    outside = 5*(N - 3**m)
    print("m = %d  N = %d: frame size %d (4^m - 3^m = %d), middle rank %s (r = %d); non-zeros %d = %.2f per row; zero rows %d, rows with one non-zero %d; largest entry %d"
          % (m, N, rt, N - 3**m, rk, (N - 2**m)//2, nnz, nnz/rt, rows0, rows1, max(abs(x) for row in Mid for x in row)))
    print("      non-zero blocks (write type, read type): %d of %d ; every non-zero block has the two digit sets covering all digits: %s"
          % (len(blocks), (2**m - 1)**2, all(set(a) | set(b) == set(range(m)) for a, b in blocks)))
    print("      cost outside the middle 5(N - 3^m) = %d ; middle between %d and %d gates ; TOTAL between %d and %d ; Yates %d ; ratio of the upper total to Yates %.3f"
          % (outside, lo, hi, outside + lo, outside + hi, N*m, (outside + hi)/(N*m)))
    # greedy sharing of pairs (Paar's heuristic, exact fractions, no cancellation): an upper bound on the middle's gates
    rows = [{j: Fr(x) for j, x in enumerate(row) if x} for row in Mid]; nv = rt; pg = 0
    while True:
        freq = {}
        for row in rows:
            ks = sorted(row)
            if len(ks) < 2: continue
            for a_ in range(len(ks)):
                for b_ in range(a_+1, len(ks)):
                    key = (ks[a_], ks[b_], row[ks[b_]]/row[ks[a_]]); freq[key] = freq.get(key, 0) + 1
        if not freq: break
        (c1, c2, rho), _ = max(freq.items(), key=lambda kv: kv[1])
        for row in rows:
            if c1 in row and c2 in row and row[c2]/row[c1] == rho:
                cf = row.pop(c1); row.pop(c2); row[nv] = cf
        nv += 1; pg += 1
    print("      greedy pair sharing computes the middle in %d gates => TOTAL %d = %.3f x Yates  (m = %d)" % (pg, outside + pg, (outside + pg)/(N*m), m))
    if m == 2:
        print("      the 7 x 7 middle (rows = write frame, columns = read frame):")
        for row in Mid: print("        ", row)
    sys.stdout.flush()
