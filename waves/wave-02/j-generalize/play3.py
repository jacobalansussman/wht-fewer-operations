# j-generalize play 3 (pure Python, exact).
# A. The "relabel + phase + one-direction butterfly" class.  An element is a 2k x 2k matrix over GF(2)
#    (how it moves the shifts X and the sign patterns Z).  Free steps: linear relabellings of the address,
#    quadratic +-1/+-i phases.  Paid step: a butterfly layer on one address bit.  0-1 breadth-first search
#    over the whole group for k = 2, 3: least number of paid layers for every element, against the rank
#    of its upper-right k x k block.
# B. Ranks of the weight blocks of the transform (inputs of weight w -> outputs of weight v), exact.
import sys, time
from collections import deque
from fractions import Fraction
from math import comb

def rank2(rows):
    rows = list(rows); r = 0
    while rows:
        p = rows.pop()
        if p:
            r += 1; low = p & -p
            rows = [x ^ p if x & low else x for x in rows]
    return r

def clifford(k):
    n = 2 * k                                    # columns 0..k-1: x-part, k..2k-1: z-part; each column a 2k-bit int
    ident = tuple(1 << c for c in range(n))
    free, paid = [], []
    for i in range(k):
        free.append(("S", i, i))
        paid.append(i)
        for j in range(k):
            if i != j: free.append(("CN", i, j))
            if i < j: free.append(("CZ", i, j))
    def apply(st, g):
        s = list(st); t, i, j = g
        if t == "S": s[i] ^= s[k + i]
        elif t == "CZ": s[i] ^= s[k + j]; s[j] ^= s[k + i]
        else: s[j] ^= s[i]; s[k + i] ^= s[k + j]
        return tuple(s)
    dist = {ident: 0}; dq = deque([ident])
    while dq:
        st = dq.popleft(); d = dist[st]
        for g in free:
            nt = apply(st, g)
            if dist.get(nt, 99) > d:
                dist[nt] = d; dq.appendleft(nt)
        for i in paid:
            s = list(st); s[i], s[k + i] = s[k + i], s[i]; nt = tuple(s)
            if nt not in dist or dist[nt] > d + 1:
                dist[nt] = d + 1; dq.append(nt)
    # upper-right block B: rows 0..k-1 of columns k..2k-1
    mask = (1 << k) - 1
    table = {}
    for st, d in dist.items():
        rb = rank2([c & mask for c in st[k:]])
        table[(d, rb)] = table.get((d, rb), 0) + 1
    J = tuple(1 << ((c + k) % n) for c in range(n))
    return len(dist), table, dist[J]

for k in (2, 3):
    t0 = time.time()
    size, table, dj = clifford(k)
    print(f"A. k={k}: group size {size}; (least paid layers, rank of block): count ->", dict(sorted(table.items())),
          f"; the transform itself needs {dj}; {time.time() - t0:.0f}s", flush=True)

def rank_q(A):
    A = [[Fraction(v) for v in r] for r in A]; r = 0
    if not A: return 0
    for c in range(len(A[0])):
        p = next((i for i in range(r, len(A)) if A[i][c] != 0), None)
        if p is None: continue
        A[r], A[p] = A[p], A[r]
        for i in range(len(A)):
            if i != r and A[i][c] != 0:
                f = A[i][c] / A[r][c]
                A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        r += 1
    return r

popc = lambda a: bin(a).count("1")
for k in (4, 5, 6, 7):
    lv = [[a for a in range(1 << k) if popc(a) == w] for w in range(k + 1)]
    R = [[rank_q([[(-1) ** popc(y & x) for x in lv[w]] for y in lv[v]]) for w in range(k + 1)] for v in range(k + 1)]
    guess = [[comb(k, min(v, w, k - v, k - w)) for w in range(k + 1)] for v in range(k + 1)]
    print(f"B. k={k}: ranks of weight blocks:", R, " equals C(k, min(v,w,k-v,k-w)):", R == guess,
          f" sum of ranks {sum(map(sum, R))} against n = {1 << k}", flush=True)
