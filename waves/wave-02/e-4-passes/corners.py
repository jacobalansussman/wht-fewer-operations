#!/usr/bin/env python3
"""e-4-passes / corners.py  exact integers.  Checks the 'corner' reading of the two-sided difference:
for a +-1 picture M (rows and columns of H in some order, with signs), E = D M D^T.  For an inner window
(rows i-1,i ; columns j-1,j):  E = 0  <=>  the two rows agree on the window or the two columns agree on it.
Vertex types: empty (window constant), straight (one wall passes through), corner (odd window), crossing
(checkerboard).  Claim: non-zero inner entries = corners + crossings, corners = #{(i,j): w_i . delta_j = 1}
(w_i = sum of consecutive row labels, delta_j = sum of consecutive column labels), and
crossings = empty + (d-1) - b/2 with b = number of wall segments that end on the border of the picture."""
import sys, ast
def had(d): return [[1 - 2 * (bin(a & x).count("1") & 1) for x in range(d)] for a in range(d)]
def check(name, pi, sig, sr, sc):
    d = len(pi); H = had(d)
    M = [[H[pi[i]][sig[j]] * sr[i] * sc[j] for j in range(d)] for i in range(d)]
    R = [M[0][:]] + [[M[i][j] - M[i-1][j] for j in range(d)] for i in range(1, d)]
    E = [[R[i][0]] + [R[i][j] - R[i][j-1] for j in range(1, d)] for i in range(d)]
    N = sum(1 for r in E for v in r if v)
    empty = straight = corner = cross = 0; okc = True; G = 0
    for i in range(1, d):
        for j in range(1, d):
            p, q, r, s = M[i-1][j-1], M[i-1][j], M[i][j-1], M[i][j]
            rows_eq = (p == r and q == s); cols_eq = (p == q and r == s)
            if (E[i][j] == 0) != (rows_eq or cols_eq): okc = False
            g = bin((pi[i] ^ pi[i-1]) & (sig[j] ^ sig[j-1])).count("1") & 1
            G += g
            if rows_eq and cols_eq: empty += 1
            elif rows_eq or cols_eq: straight += 1
            elif p * q * r * s == -1:
                corner += 1
                if not g: okc = False
            else: cross += 1
    b = sum(1 for i in range(1, d) for j in (0, d-1) if M[i][j] != M[i-1][j]) + sum(1 for j in range(1, d) for i in (0, d-1) if M[i][j] != M[i][j-1])
    edge = sum(1 for j in range(d) if E[0][j]) + sum(1 for i in range(1, d) if E[i][0])
    print(f"{name}: d={d} N={N} = border {edge} + corners {corner} + crossings {cross};  empty {empty} straight {straight};  G={G};"
          f" zero-criterion and corner=G hold: {okc and G == corner};  crossings - empty = {cross - empty}, (d-1) - b/2 = {(d-1) - b/2}")
if __name__ == "__main__":
    check("d=4 exhaustive minimum", (0,2,1,3), (0,1,2,3), [1]*4, [1]*4)
    check("d=8 exhaustive minimum", (0,6,2,4,7,3,5,1), tuple(range(8)), [1]*8, [1]*8)
    g = [i ^ (i >> 1) for i in range(16)]; rev = [int(format(i, "04b")[::-1], 2) for i in range(16)]
    check("d=16 plain / bit-reversed", list(range(16)), rev, [1]*16, [1]*16)
    check("d=16 Gray / bit-reversed Gray", g, [rev[v] for v in g], [1]*16, [1]*16)
    for fn in sys.argv[1:]:
        L = open(fn).read().split("\n")
        pi = ast.literal_eval(L[1].split("row order")[1].split("signs")[0].strip()); sr = ast.literal_eval(L[1].split("signs")[1].strip())
        sig = ast.literal_eval(L[2].split("col order")[1].split("signs")[0].strip()); sc = ast.literal_eval(L[2].split("signs")[1].strip())
        check(fn, pi, sig, sr, sc)
