#!/usr/bin/env python3
"""blocks.py -- ab-3.  'Evaluate a polynomial of degree <= d at all N points of the cube' (the way back from the lightest
outputs) by the pigeonhole split: cut the k bits into d+1 blocks; every monomial of degree <= d misses a block, so the
polynomial is a sum of d+1 pieces, piece i not depending on block i.  Count (G), exact replay (whole numbers).
Inputs of the circuit: the V(d) coefficients.  Outputs: the N values.  By transposition [recalled rule] the way there
(N inputs -> V(d) lightest outputs) costs the same plus N - V(d)."""
import sys, itertools
from math import comb
from functools import lru_cache
sys.setrecursionlimit(10000)

class C:                                   # wires = dict coefficient-index -> int ; free scalings NOT needed here (all +-1)
    def __init__(self): self.g = 0; self.memo = {}
def monos(bits, d):
    return [frozenset(c) for r in range(d + 1) for c in itertools.combinations(bits, r)]

def build(bits, d, ms, cnt):
    """wires (as dict mono->+-1 coefficient vectors, i.e. python dicts) for the polynomial sum_{m in ms} c_m chi_m on `bits`,
    at all 2^len(bits) points; ms = list of monomials (subsets of bits, each of size <= d). returns list indexed by point."""
    j = len(bits)
    ms = [m for m in ms]
    if not ms: return [None] * (1 << j)
    if j == 0: return [{frozenset(): 1}]
    used = sorted(set().union(*ms)) if ms else []
    if len(used) < j:                      # the polynomial ignores some bits: build on the used ones and copy (no gates)
        sub = build(used, d, ms, cnt); pos = [bits.index(b) for b in used]
        return [sub[sum(((y >> pos[t]) & 1) << t for t in range(len(used)))] for y in range(1 << j)]
    dd = max(len(m) for m in ms)
    nb = min(dd + 1, j)                    # number of blocks
    size = [j // nb + (1 if t < j % nb else 0) for t in range(nb)]
    blocks = []; s = 0
    for t in range(nb): blocks.append(bits[s:s + size[t]]); s += size[t]
    if nb == j and dd >= j:                # full degree on single bits: plain butterfly on the last bit
        b = bits[-1]; rest = bits[:-1]
        g0 = build(rest, d, [m for m in ms if b not in m], cnt)
        g1 = build(rest, d, [m - {b} for m in ms if b in m], cnt)
        out = [None] * (1 << j)
        for y in range(1 << (j - 1)):
            for bit in (0, 1):
                out[y | (bit << (j - 1))] = comb2(g0[y], g1[y], -1 if bit else 1, b, cnt)
        return out
    # assign every monomial to the first block it misses
    pieces = [[] for _ in range(nb)]
    for m in ms:
        t = next(t for t in range(nb) if not (m & set(blocks[t])))
        pieces[t].append(m)
    out = [None] * (1 << j)
    for t in range(nb):
        if not pieces[t]: continue
        other = [b for b in bits if b not in blocks[t]]
        sub = build(other, d, pieces[t], cnt); pos = [bits.index(b) for b in other]
        for y in range(1 << j):
            v = sub[sum(((y >> pos[u]) & 1) << u for u in range(len(other)))]
            out[y] = v if out[y] is None else add(out[y], v, cnt)
    return out
def add(u, v, cnt):
    key = (id(u), id(v))
    if key in cnt.memo: return cnt.memo[key][2]
    w = dict(u)
    for m, c in v.items(): w[m] = w.get(m, 0) + c
    cnt.g += 1; cnt.memo[key] = (u, v, w); return w
def comb2(g0, g1, sign, b, cnt):
    if g1 is None: return g0
    v = {m | {b}: sign * c for m, c in g1.items()}
    if g0 is None:
        return v                                   # a scaling/relabelling of a wire: free
    key = (id(g0), id(g1), sign)
    if key in cnt.memo: return cnt.memo[key][2]
    w = dict(g0); w.update(v); cnt.g += 1; cnt.memo[key] = (g0, g1, w); return w

def check(bits, d, out):
    ms = monos(bits, d); j = len(bits)
    for y in range(1 << j):
        want = {m: (-1) ** sum((y >> bits.index(b)) & 1 for b in m) for m in ms}
        if out[y] != want: return False
    return True
def yates_cut(k, d):                       # the earlier recursion: N + S(k-1,d) + S(k-1,d-1), S(.,0)=0
    @lru_cache(None)
    def S(j, e):
        if j == 0 or e == 0: return 0
        return (1 << j) + S(j - 1, e) + S(j - 1, e - 1)
    return S(k, d)

if __name__ == "__main__":
    K = int(sys.argv[1])
    print("evaluate a polynomial of degree <= d at all N cube points: gates (G), pigeonhole split, replayed exactly;  in brackets gates/N; 'Y' = the cut-off Yates count for comparison")
    for d in (1, 2, 3, 4):
        line = []
        for k in range(d + 1, K + 1):
            if d >= 3 and k > K - 2: break
            cnt = C(); bits = list(range(k)); out = build(bits, d, monos(bits, d), cnt)
            ok = check(bits, d, out) if k <= 14 else None
            line.append(f"k={k}:{cnt.g}({cnt.g/(1<<k):.3f};Y {yates_cut(k,d)/(1<<k):.2f}){'ok' if ok else ('BAD' if ok is False else 'unchecked')}")
        print(f"d={d}: " + "  ".join(line), flush=True)
