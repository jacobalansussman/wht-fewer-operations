# delta.py : the one fact about the object M(d,k) that the private-wire lemma uses, checked from scratch.
#   M(d,k): one row for each address y (k bits), one column for each set S of at most d bits, entry 1 if S inside y.
#   A RELATION is a set of rows with non-zero coefficients adding to zero.  delta = fewest rows in a relation.
#   Claim (ag-7 section 4): delta = 2^(d+1) over every field (no relation at all when d >= k).
# Two-element field: exhaustive over the whole space of relations (2^(N-R) vectors), so the answer is exact.
# Rationals: every set of fewer than 2^(d+1) rows is tested for independence modulo the prime 1000003.
#   Independent modulo a prime implies independent over the rationals (a rational relation can be scaled to
#   whole numbers with no common factor, which is then a non-zero relation modulo the prime).  So "all sets
#   independent modulo p" proves delta >= 2^(d+1) over the rationals; the (d+1)-fold difference shows equality.
import sys
from itertools import combinations
P = 1000003

def rows(d, k):
    sets = [sum(1 << i for i in c) for j in range(d + 1) for c in combinations(range(k), j)]
    return [[1 if (s & y) == s else 0 for s in sets] for y in range(1 << k)], len(sets)

def delta_f2(d, k):
    M, R = rows(d, k)
    N = 1 << k
    # row y as a bitmask over columns, with an identity tag over rows to track combinations
    vecs = [(sum(b << j for j, b in enumerate(M[y])), 1 << y) for y in range(N)]
    basis = {}          # pivot bit -> (vector, tag)
    kernel = []
    for v, t in vecs:
        while v:
            p = v.bit_length() - 1
            if p in basis:
                bv, bt = basis[p]; v ^= bv; t ^= bt
            else:
                basis[p] = (v, t); break
        if v == 0:
            kernel.append(t)
    dim = len(kernel)
    if dim == 0:
        return None, 0
    if dim > 22:
        return 'skipped', dim
    best = N + 1
    # Gray-code walk over all non-zero kernel vectors
    cur = 0
    for g in range(1, 1 << dim):
        low = (g & -g).bit_length() - 1
        cur ^= kernel[low]
        w = bin(cur).count('1')
        if w < best: best = w
    return best, dim

def independent_mod_p(vectors):
    A = [list(v) for v in vectors]
    r = 0
    ncol = len(A[0])
    for c in range(ncol):
        piv = None
        for i in range(r, len(A)):
            if A[i][c] % P:
                piv = i; break
        if piv is None: continue
        A[r], A[piv] = A[piv], A[r]
        inv = pow(A[r][c], P - 2, P)
        for i in range(r + 1, len(A)):
            if A[i][c] % P:
                f = A[i][c] * inv % P
                A[i] = [(a - f * b) % P for a, b in zip(A[i], A[r])]
        r += 1
        if r == len(A): return True
    return r == len(A)

def delta_q_lower(d, k, limit):
    M, R = rows(d, k)
    N = 1 << k
    size = (1 << (d + 1)) - 1          # every set of this size independent  =>  delta >= 2^(d+1)
    if size > N: size = N
    count = 0
    for c in combinations(range(N), size):
        count += 1
        if count > limit: return 'stopped', count - 1
        if not independent_mod_p([M[y] for y in c]): return ('DEPENDENT', c), count
    return 'all independent', count

print("two-element field, exhaustive over all relations")
for k in range(2, 7):
    for d in range(1, k):
        b, dim = delta_f2(d, k)
        print(f"  k={k} d={d}: relations form a space of dimension {dim}; shortest = {b}; claim 2^(d+1) = {1 << (d + 1)}; {'OK' if b == (1 << (d + 1)) else ('skipped' if b == 'skipped' else 'MISMATCH')}", flush=True)
print("rationals (independence modulo 1000003 of every set of 2^(d+1) - 1 rows)")
for k, d in ((3, 1), (3, 2), (4, 1), (4, 2), (4, 3), (5, 1), (5, 2)):
    res, cnt = delta_q_lower(d, k, 4_000_000)
    print(f"  k={k} d={d}: {cnt} sets of {min((1 << (d + 1)) - 1, 1 << k)} rows: {res}", flush=True)
