#!/usr/bin/env python3
"""k3.py (g-5-k3, 2026-10-10): exact replay of circuits for the Kronecker powers of K3 = [[1,1,1],[2,0,-2],[1,-1,1]].
Count (G): a gate is a*u + b*v, scalings free; an output counts when a node is proportional to its row.
Count (O): additions/subtractions and scalar multiplications each cost 1; outputs must EQUAL the rows.
Everything in Fractions / integers.

The circuit: K3 = (butterfly on slots (s, b)) after (butterfly on letters (0, 2)), so
  K3^(x r) = B . A,   A = direct sum over M (positions holding letter 1) of the Walsh-Hadamard transform on {0,2}^(rest),
                      B = direct sum over W (positions holding the difference slot) of the transform on {sum slot, letter 1}^(rest).
'hadamard(wires, brick)' builds the transform on 2^s wires with plain butterflies or with the 7-gate 4-point brick.
"""
import sys, json, itertools
from fractions import Fraction as F
from math import comb

K3 = [[1, 1, 1], [2, 0, -2], [1, -1, 1]]

def kron(A, B):
    return [[a * b for a in ra for b in rb] for ra in A for rb in B]

def kpow(A, r):
    M = [[1]]
    for _ in range(r): M = kron(M, A)
    return M

class Circ:
    def __init__(self, n):
        self.n = n; self.rows = [[F(int(i == j)) for j in range(n)] for i in range(n)]; self.gates = []
    def gate(self, u, v, a, b):
        self.rows.append([a * x + b * y for x, y in zip(self.rows[u], self.rows[v])]); self.gates.append((u, v, a, b))
        return len(self.rows) - 1

def butterfly(c, x, y):
    return c.gate(x, y, 1, 1), c.gate(x, y, 1, -1)

def brick4(c, p, q, r, s):
    """4-point transform in 7 gates: helper u = p - q - r - s; outputs (++++), (++--), (+-+-), (+--+) in that order."""
    g1 = c.gate(p, q, 1, -1); g2 = c.gate(g1, r, 1, -1); u = c.gate(g2, s, 1, -1)
    return [c.gate(p, u, 2, -1), c.gate(u, q, 1, 2), c.gate(u, r, 1, 2), c.gate(u, s, 1, 2)]

def hadamard(c, wires, brick):
    """wires: list of 2^s node ids indexed by a bit string (bit i of the index = coordinate i).  Returns the list of
    output nodes, index bit i = 1 meaning 'difference along coordinate i'."""
    s = len(wires).bit_length() - 1; cur = list(wires); i = 0
    while i < s:
        if brick and i + 1 < s:
            done = set()
            for idx in range(len(cur)):
                base = idx & ~((1 << i) | (1 << (i + 1)))
                if base in done: continue
                done.add(base)
                p, q, r_, s_ = base, base | (1 << (i + 1)), base | (1 << i), base | (1 << i) | (1 << (i + 1))
                # brick outputs: (++++) -> 00, (++--) -> difference along the first listed pair split.
                o = brick4(c, cur[p], cur[q], cur[r_], cur[s_])
                # with inputs ordered (p, q, r, s) = (00, 01, 10, 11) in (bit i, bit i+1):
                # (++--) is the difference along bit i, (+-+-) the difference along bit i+1, (+--+) both.
                cur[p], cur[r_], cur[q], cur[s_] = o[0], o[1], o[2], o[3]
            i += 2
        else:
            for idx in range(len(cur)):
                if not idx >> i & 1:
                    j = idx | (1 << i); cur[idx], cur[j] = butterfly(c, cur[idx], cur[j])
            i += 1
    return cur

def k3power(r, brick):
    pts = list(itertools.product(range(3), repeat=r)); pos = {p: i for i, p in enumerate(pts)}
    c = Circ(3 ** r); cur = {p: pos[p] for p in pts}
    for (fixed_letter, lo, hi) in ((1, 0, 2), (2, 0, 1)):      # layer A: letters {0,2}, letter 1 fixed.  layer B: slots {0,1}, slot 2 fixed.
        for M in itertools.product((0, 1), repeat=r):          # M[i] = 1: position i holds the fixed letter
            free = [i for i in range(r) if not M[i]]
            if not free: continue
            wires = []; keys = []
            for idx in range(1 << len(free)):
                p = [fixed_letter] * r
                for b, i in enumerate(free): p[i] = hi if idx >> b & 1 else lo
                keys.append(tuple(p)); wires.append(cur[tuple(p)])
            out = hadamard(c, wires, brick)
            for kkey, o in zip(keys, out): cur[kkey] = o
    # after both layers: slot 0 = row 0 (s+b), slot 1 = row 2 (s-b), slot 2 = row 1 (d)
    rowmap = {0: 0, 1: 2, 2: 1}
    outs = {tuple(rowmap[x] for x in p): cur[p] for p in pts}
    return c, pts, pos, outs

def proportional(a, b):
    k = None
    for x, y in zip(a, b):
        if (x == 0) != (y == 0): return None
        if y != 0:
            if k is None: k = x / y
            elif x != k * y: return None
    return k

def check(r, brick):
    c, pts, pos, outs = k3power(r, brick); T = kpow(K3, r); ok = True; scales = set()
    for p in pts:
        k = proportional(c.rows[outs[p]], [F(x) for x in T[pos[p]]])
        if k is None: ok = False
        else: scales.add(k)
    return c, outs, pts, pos, ok, scales

if __name__ == '__main__':
    print('== 1. exact replay, count (G) ==')
    for r in (1, 2, 3, 4):
        for brick in (False, True):
            c, outs, pts, pos, ok, scales = check(r, brick)
            print('K3^(x%d) on %d numbers: %s : %d gates, every output proportional to its row: %s ; textbook 4r3^(r-1) = %d ; volume bound (log2|det| of the row-scaled kernel) = %d'
                  % (r, 3 ** r, '7-gate bricks' if brick else 'plain butterflies', len(c.gates), ok, 4 * r * 3 ** (r - 1), 2 * r * 3 ** (r - 1)))
            if r == 2 and brick:
                json.dump({'n': 9, 'gates': [[u, v, str(a), str(b)] for (u, v, a, b) in c.gates],
                           'outs': [outs[p] for p in pts]}, open(sys.argv[1] if len(sys.argv) > 1 else 'k9_22.json', 'w'))
                for i, (u, v, a, b) in enumerate(c.gates):
                    print('    n%d = (%s)*n%d + (%s)*n%d   = %s' % (9 + i, a, u, b, v, [str(x) for x in c.rows[9 + i]]))
                print('    outputs (row index -> node):', {''.join(map(str, p)): outs[p] for p in pts})
    print()
    print('== 2. count (O): plain butterflies have coefficients +-1, so the nodes are the rows of the row-scaled kernel exactly;')
    print('      a row with j factors (2,0,-2) then needs one multiplication by 2^j ==')
    for r in (1, 2, 3, 4):
        c, outs, pts, pos, ok, scales = check(r, False)
        allpm = all(a in (1, -1) and b in (1, -1) for (_, _, a, b) in c.gates)
        T = kpow(K3, r); need = 0; exact = True
        for p in pts:
            k = proportional([F(x) for x in T[pos[p]]], c.rows[outs[p]])
            if k is None: exact = False
            elif k != 1: need += 1
            if k is not None and k != 2 ** sum(1 for x in p if x == 1): exact = False
        print('K3^(x%d): additions %d (all coefficients +-1: %s), multiplications by a power of 2: %d (= 3^r - 2^r = %d), count (O) total %d ; factors are 2^j exactly: %s'
              % (r, len(c.gates), allpm, need, 3 ** r - 2 ** r, len(c.gates) + need, exact))
    print()
    print('== 3. the two reductions as counts ==')
    def c3_from(T, r): return 2 * sum(comb(r, j) * T(r - j) for j in range(r + 1))
    def T_from(T, c3, k):
        h = k // 2
        return 2 * sum(comb(h, s) * 2 ** (h - s) * T(s) for s in range(h + 1)) + sum(comb(h, r) * c3(r) for r in range(h + 1))
    text = lambda s: s * 2 ** s
    best = {0: 0, 1: 2, 2: 7, 3: 22, 4: 56}
    def bk(s):                       # best known in count (G): 7-gate bricks
        return best[s] if s in best else (s // 2) * 7 * 2 ** (s - 2) + (s % 2) * 2 ** s
    for r in range(1, 9):
        a = c3_from(text, r); b = c3_from(bk, r)
        print('r=%d: K3 power from transforms: textbook prices %d (= 4r3^(r-1) = %d: %s), brick prices %d, ratio %.4f'
              % (r, a, 4 * r * 3 ** (r - 1), a == 4 * r * 3 ** (r - 1), b, b / a))
    for k in (2, 4, 6, 8, 16, 32):
        a = T_from(text, lambda r: c3_from(text, r), k); b = T_from(bk, lambda r: c3_from(bk, r), k)
        print('k=%d: transform from (orbit transforms, K3 powers from transforms): textbook prices %d (= k 2^k: %s), brick prices %d vs plain brick product %d'
              % (k, a, a == k * 2 ** k, b, bk(k)))
