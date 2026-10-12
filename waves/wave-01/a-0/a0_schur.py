# a-0, part (b): my own check that the bracket-matching (valence-bond) basis is at once a Jordan basis of the add-one-element
# operator U, turns Z into Pascal blocks and H into (-2)^pairs x Krawtchouk blocks.  Exact integers.  k = 2..KMAX.
# Written independently of schur.py: basis vectors are built from the ADDRESS (d-7's rule: a 1 opens, a 0 closes), the three
# operators are applied as sparse maps on dictionaries, and the claimed images are compared coefficient by coefficient.
# Rank: over Q, proved by a determinant modulo one prime (non-zero mod p implies non-zero over Q) up to RANKMAX.
import sys
from math import comb
KMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 10
RANKMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 9

def match(x, k):
    """pairs and free positions of address x: scanning positions 0..k-1, a 1 opens, a 0 closes the latest open 1."""
    st = []; pairs = []
    for pos in range(k):
        if (x >> pos) & 1: st.append(pos)
        elif st: pairs.append((st.pop(), pos))
    matched = set(p for pq in pairs for p in pq)
    free = [p for p in range(k) if p not in matched]
    ones = sum(1 for p in free if (x >> p) & 1)
    return tuple(sorted(pairs)), tuple(free), ones

def vec(pairs, free, t):
    """antisymmetric combination on every pair, sum of all placements of t ones on the free positions."""
    v = {0: 1}
    for (a, b) in pairs:
        w = {}
        for idx, c in v.items():
            w[idx | (1 << a)] = w.get(idx | (1 << a), 0) + c
            w[idx | (1 << b)] = w.get(idx | (1 << b), 0) - c
        v = w
    u = len(free); out = {}
    def rec(i, left, add):
        if left == 0:
            for idx, c in v.items(): out[idx | add] = out.get(idx | add, 0) + c
            return
        if u - i < left: return
        rec(i + 1, left - 1, add | (1 << free[i])); rec(i + 1, left, add)
    rec(0, t, 0)
    return out

def dense(d, N):
    v = [0] * N
    for i, c in d.items(): v[i] = c
    return v
def wht(v, k):
    v = v[:]
    for j in range(k):
        h = 1 << j
        for x in range(len(v)):
            if not x & h:
                a, b = v[x], v[x | h]; v[x], v[x | h] = a + b, a - b
    return v
def zeta(v, k):
    v = v[:]
    for j in range(k):
        h = 1 << j
        for x in range(len(v)):
            if x & h: v[x] += v[x ^ h]
    return v
def up(v, k):
    o = [0] * len(v)
    for T, c in enumerate(v):
        if c:
            for j in range(k):
                if not (T >> j) & 1: o[T | (1 << j)] += c
    return o
def down(v, k):
    o = [0] * len(v)
    for T, c in enumerate(v):
        if c:
            for j in range(k):
                if (T >> j) & 1: o[T ^ (1 << j)] += c
    return o
def kraw(u, j, i):   # coefficient of x^i in (1-x)^j (1+x)^(u-j)
    return sum((-1) ** l * comb(j, l) * comb(u - j, i - l) for l in range(0, i + 1) if l <= j and i - l <= u - j)
def lin(vs, terms, N):
    o = [0] * N
    for (key, c) in terms:
        if c:
            for i, a in vs[key].items(): o[i] += c * a
    return o

for k in range(2, KMAX + 1):
    N = 1 << k
    lab = {}                        # address -> (pairs, free, ones): d-7's relabelling
    for x in range(N): lab[x] = match(x, k)
    keys = set((p, f, t) for (p, f, t) in lab.values())
    assert len(keys) == N           # the relabelling is a bijection onto (matching, weight) labels
    # d-0's labelling is "one string per matching, u+1 vectors on it": same set?
    strings = set((p, f) for (p, f, t) in keys)
    assert all((p, f, t) in keys for (p, f) in strings for t in range(len(f) + 1)) and sum(len(f) + 1 for (p, f) in strings) == N
    vs = {key: vec(*key) for key in keys}
    okU = okZ = okH = okLow = True; nnz = 0
    for (p, f, t) in keys:
        u = len(f); v = dense(vs[(p, f, t)], N); nnz += len(vs[(p, f, t)])
        okU &= up(v, k) == lin(vs, [((p, f, t + 1), t + 1)] if t < u else [], N)
        okZ &= zeta(v, k) == lin(vs, [((p, f, j), comb(j, t)) for j in range(t, u + 1)], N)
        okH &= wht(v, k) == lin(vs, [((p, f, j), (-2) ** len(p) * kraw(u, j, t)) for j in range(u + 1)], N)
        if t == 0: okLow &= not any(down(v, k))          # string heads are killed by "remove one element": an sl2 basis
    rk = "-"
    if k <= RANKMAX:
        pr = 2147483629; order = sorted(keys)
        A = [[0] * N for _ in range(N)]
        for c, key in enumerate(order):
            for i, a in vs[key].items(): A[i][c] = a % pr
        r = 0
        for c in range(N):
            piv = next((i for i in range(r, N) if A[i][c]), None)
            if piv is None: continue
            A[r], A[piv] = A[piv], A[r]; inv = pow(A[r][c], pr - 2, pr); Ar = A[r]
            for i in range(r + 1, N):
                f0 = A[i][c]
                if f0:
                    f0 = f0 * inv % pr; A[i] = [(x - f0 * y) % pr for x, y in zip(A[i], Ar)]
            r += 1
        rk = str(r)
    print("k=%2d N=%4d strings=%3d rank mod p=%s  U shift:%s  Z Pascal:%s  H (-2)^pairs Krawtchouk:%s  heads killed by 'remove one':%s  non-zeros of B per column %.2f"
          % (k, N, len(strings), rk, okU, okZ, okH, okLow, nnz / N))
    sys.stdout.flush()
