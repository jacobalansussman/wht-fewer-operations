#!/usr/bin/env python3
"""e-4-passes / four.py   exact (Fractions).  Is H_8 a product of FOUR passes in the word P B B P ?
E = D H' D^t (plain differences in a row order and a column order, all coefficients 1: a SAMPLE of the outer
passes, they are no longer forced when the middle is two letters).  Test: E = B2 * B3 with B2, B3 differences
(two non-zeros per row, supports on a path)  <=>  some running combination of the rows of E,
y_0 = e_r0, y_i = e_ri + c_i*y_(i-1), keeps at most 2 non-zeros in every y_i and the y's have path-shaped support.
Depth-first search over the row order r and the useful values of c_i: 0, the values that cancel an entry,
and (one step of lookahead) the values that make a two-entry y proportional to a later row on its two columns.
NOT complete: a free ratio carried over two or more steps is not followed."""
import sys, itertools
from fractions import Fraction as Fr
sys.path.insert(0, ".")
from pbp import had, emat, reduced_orders, path_ok
d = int(sys.argv[1]); cap = int(sys.argv[2])
H = had(d); ones = [1] * d
def factor(E):
    rows = [[Fr(v) for v in r] for r in E]
    sol = []
    def nz(v): return [k for k in range(d) if v[k] != 0]
    def dfs(used, y, ys, order, cs):
        if len(order) == d:
            if path_ok(ys): sol.append((order[:], cs[:], [r[:] for r in ys]))
            return
        for r in range(d):
            if sol: return
            if r in used: continue
            e = rows[r]; cands = [Fr(0)]
            for k in nz(y):
                if e[k] != 0: cands.append(-e[k] / y[k])
            # one-step lookahead for the free case: y has one non-zero (column k), e adds one other column l; then the
            # ratio of the two entries of e + c*y is free, and the useful values make it proportional to a later row
            ny = nz(y)
            if len(ny) == 1:
                k = ny[0]; S = set(nz(e)) | {k}
                if len(S) == 2:
                    l = [t for t in S if t != k][0]
                    for r2 in range(d):
                        if r2 != r and r2 not in used and rows[r2][k] != 0 and rows[r2][l] != 0:
                            cands.append((e[l] * rows[r2][k] / rows[r2][l] - e[k]) / y[k])
            for c in dict.fromkeys(cands):
                v = [e[k] + c * y[k] for k in range(d)]
                if 0 < len(nz(v)) <= 2:
                    dfs(used | {r}, v, ys + [v], order + [r], cs + [c])
    for r in range(d):
        if sol: break
        if len(nz(rows[r])) <= 2:
            dfs({r}, rows[r], [rows[r]], [r], [Fr(0)])
    return sol[0] if sol else None
tested = found = 0
for sig in reduced_orders(d):
    for rest in itertools.permutations(range(1, d)):
        pi = (0,) + rest
        E = emat(H, pi, sig, ones, ones)
        n = sum(1 for r in E for v in r if v)
        if n > cap: continue
        tested += 1
        s = factor(E)
        if s:
            found += 1
            if found == 1:
                print("FOUND  row order", pi, "column order", sig, "non-zeros of E", n)
                for r in E: print("   E ", r)
                print("   order of the running combination", s[0], "coefficients", [str(c) for c in s[1]])
                for r in s[2]: print("   B3", [str(v) for v in r])
print("d =", d, " arrangements with at most", cap, "non-zeros tested:", tested, "  factor as two differences:", found)
