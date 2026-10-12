#!/usr/bin/env python3
"""post2.py K leaves.txt [design]  -- counting, the clique lemma AND the zero-form lemma on every count vector.  [h-2-clique17]
Zero-form lemma (h-2.md section 2): let q0 be a form with q0(I) = 0 that selects the set A0 of moves, and let T be a set of
moves inside A0 that are pairwise selected together by tight forms.  Then |A0| >= 2 |T|.
(U_A0 N W_A0^T = 0 with N invertible gives rank U_A0 + rank W_A0 <= |A0|; a pairwise joined set has a triangular table
w_i.u_j with ones on the diagonal, so both ranks are at least |T|.)
With 'design' as third argument the vectors are the odd-weight design plus up to K - 16 extra moves, instead of leaves.
"""
import sys, itertools
args = sys.argv[:]
sys.argv = [args[0], args[1]]
import post, numpy as np
K = int(args[1]); W = 4
V = post.V
bits = post.bits; diag = post.diag; mon = post.mon
keep0 = bits[:, diag].sum(axis=1) % 2 == 0
A0 = np.unique((bits[keep0] @ mon) % 2, axis=0)          # forms with q(I) = 0 (as functions on the 31 points)
def wclique(n, adj, cand):
    best = 0; bestset = 0
    def bk(R, wR, Pm):
        nonlocal best, bestset
        if wR > best: best = wR; bestset = R
        if wR + sum(int(n[j]) for j in range(31) if Pm >> j & 1) <= best: return
        while Pm:
            v = Pm & -Pm; i = v.bit_length() - 1
            bk(R | v, wR + int(n[i]), Pm & adj[i]); Pm &= ~v
    bk(0, 0, cand); return best, bestset
def both(n):
    n = np.asarray(n, dtype=np.int64); cnt = post.A @ n
    assert cnt.min() >= W
    tight = np.unique(post.A[cnt == W] * (n > 0), axis=0)
    adj = [0] * 31; intight = 0
    for row in tight:
        msk = sum(1 << i for i in range(31) if row[i]); intight |= msk
        for i in range(31):
            if row[i]: adj[i] |= msk & ~(1 << i)
    cl, clset = wclique(n, adj, intight)
    if cl > W: return ("clique", len(tight), cl, clset, None)
    c0 = A0 @ n
    worst = None
    for r in np.nonzero((c0 > 0) & (c0 <= 2 * W - 1))[0]:
        sel = sum(1 << i for i in range(31) if A0[r][i] and n[i] > 0) & intight
        t, ts = wclique(n, adj, sel)
        if 2 * t > c0[r]:
            return ("zero", len(tight), cl, ts, (int(c0[r]), t, [format(V[i], "05b") for i in range(31) if A0[r][i] and n[i] > 0]))
    return ("survives", len(tight), cl, clset, None)
if __name__ == "__main__":
    classes = {}
    if len(args) > 3 and args[3] == "design":
        odd = [1 if bin(z).count("1") & 1 else 0 for z in V]
        for e in range(0, K - 16 + 1):
            for comb in itertools.combinations_with_replacement(range(31), e):
                n = odd[:]
                for i in comb: n[i] += 1
                c = post.canon_fast(n); classes.setdefault(sum(c), set()).add(c)
    else:
        for line in open(args[2]):
            p = line.split(); T = int(p[0]); fr = int(p[1]); n0 = list(map(int, p[2:]))
            free = [i for i in range(31) if not fr >> i & 1]
            for e in range(0, K - T + 1):
                for comb in itertools.combinations_with_replacement(free, e):
                    n = n0[:]
                    for i in comb: n[i] += 1
                    c = post.canon_fast(n); classes.setdefault(sum(c), set()).add(c)
    for tot in sorted(classes):
        res = {"clique": 0, "zero": 0, "survives": 0}; lines = []
        for c in sorted(classes[tot]):
            kind, nt, cl, s, info = both(c); res[kind] += 1
            nodd = sum(1 for i in range(31) if c[i] and bin(V[i]).count("1") & 1)
            if kind != "clique":
                lines.append("     %s: %s   [tight selections %d, largest joined set %d, odd-weight directions used %d of 16]%s"
                             % (kind.upper(), post.fmt(c), nt, cl, nodd, "" if info is None else "  form with q(I)=0 selecting %d moves contains a joined set of %d: %s" % info))
        print("%d moves: %d count vectors pass counting (up to the 720 maps); excluded by the clique lemma %d, by the zero-form lemma %d, SURVIVE %d"
              % (tot, len(classes[tot]), res["clique"], res["zero"], res["survives"]))
        for l in lines: print(l)
