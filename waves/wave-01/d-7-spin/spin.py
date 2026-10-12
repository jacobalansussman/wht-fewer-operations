#!/usr/bin/env python3
"""d-7-spin: build the valence-bond (crystal) symmetry-adapted basis exactly and check what it does to the transform.
Exact integer arithmetic throughout (python integers)."""
import sys, itertools
from math import comb

def skeleton(x, k):
    """bracket matching: 1 opens, 0 closes the most recent open 1. returns (arcs, unmatched positions, t)."""
    stack, arcs, un0 = [], [], []
    for p in range(k):
        if (x >> (k - 1 - p)) & 1:
            stack.append(p)
        elif stack:
            arcs.append((stack.pop(), p))
        else:
            un0.append(p)
    return tuple(sorted(arcs)), tuple(un0 + stack), len(stack)

def addr(bits, k):
    v = 0
    for p in bits:
        v |= 1 << (k - 1 - p)
    return v

def vb_vector(arcs, U, t, k):
    """singlets on arcs (e[a=1,b=0] - e[a=0,b=1]) tensor unnormalised Dicke_t on U."""
    v = {}
    for signs in itertools.product((0, 1), repeat=len(arcs)):
        base, sg = [], 1
        for (a, b), s in zip(arcs, signs):
            if s == 0: base.append(a)
            else: base.append(b); sg = -sg
        for T in itertools.combinations(U, t):
            v[addr(list(base) + list(T), k)] = sg
    return v

def kraw(n, tp, t):
    return sum((-1) ** i * comb(tp, i) * comb(n - tp, t - i) for i in range(0, t + 1))

def wht(v):
    v = list(v); n = len(v); h = 1
    while h < n:
        for i in range(0, n, 2 * h):
            for j in range(i, i + h):
                a, b = v[j], v[j + h]; v[j], v[j + h] = a + b, a - b
        h *= 2
    return v

def run(k):
    N = 1 << k
    lab, colv = {}, {}
    for x in range(N):
        arcs, U, t = skeleton(x, k)
        lab[x] = (arcs, U, t)
        colv[x] = vb_vector(arcs, U, t, k)
    assert all(colv[x].get(x) in (1, -1) for x in range(N))
    col = {lab[x]: x for x in range(N)}
    assert len(col) == N
    ok = True; nnzM = 0
    for x in range(N):
        arcs, U, t = lab[x]; n = len(U)
        dense = [0] * N
        for y, c in colv[x].items(): dense[y] = c
        hs = wht(dense)                      # H is symmetric and (-1)^(a.b) in any bit order
        pred = [0] * N
        for tp in range(n + 1):
            m = (-2) ** len(arcs) * kraw(n, tp, t)
            if m:
                nnzM += 1
                for y, c in colv[col[(arcs, U, tp)]].items(): pred[y] += m * c
        ok &= (hs == pred)
    indeg = [0] * N
    for x in range(N):
        for y in colv[x]:
            if y != x: indeg[y] += 1
    queue = [y for y in range(N) if indeg[y] == 0]; seen = 0
    while queue:
        x = queue.pop(); seen += 1
        for y in colv[x]:
            if y != x:
                indeg[y] -= 1
                if indeg[y] == 0: queue.append(y)
    tri = (seen == N)
    nnzS = sum(len(colv[x]) for x in range(N))
    blocks = {}
    for x in range(N):
        arcs, U, t = lab[x]
        if t == 0: blocks[len(arcs)] = blocks.get(len(arcs), 0) + 1
    print("k=%d N=%d  H*S == S*M: %s   S entries in {0,+-1}: True by construction   S = relabelling x unitriangular: %s" % (k, N, ok, tri))
    print("   nnz(S)=%d (%.2f per entry)  nnz(M)=%d (%.3f per entry)  blocks {arcs j: multiplicity} = %s" % (nnzS, nnzS / N, nnzM, nnzM / N, dict(sorted(blocks.items()))))
    if k <= 7:
        p = 2147483629
        A = [[0] * N for _ in range(N)]
        for x in range(N):
            for y, c in colv[x].items(): A[y][x] = c % p
        det = 1
        for i in range(N):
            piv = next((r for r in range(i, N) if A[r][i]), None)
            if piv is None: det = 0; break
            if piv != i: A[i], A[piv] = A[piv], A[i]; det = -det
            det = det * A[i][i] % p
            inv = pow(A[i][i], p - 2, p); Ai = A[i]
            nzc = [c for c in range(i, N) if Ai[c]]
            for r in range(i + 1, N):
                if A[r][i]:
                    f = A[r][i] * inv % p; Ar = A[r]
                    for c in nzc: Ar[c] = (Ar[c] - f * Ai[c]) % p
        det %= p
        print("   det(S) mod %d = %s" % (p, "+1" if det == 1 else ("-1" if det == p - 1 else str(det))))
    return ok and tri

if __name__ == "__main__":
    ks = [int(a) for a in sys.argv[1:]] or [2, 3, 4, 5, 6, 8]
    allok = True
    for k in ks:
        allok &= run(k)
    print("ALL OK" if allok else "SOMETHING FAILED")
