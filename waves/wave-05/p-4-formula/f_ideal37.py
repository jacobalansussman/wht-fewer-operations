# p-4-formula: the rule's IDEAL form at 16 points: 1 + 36 rectangles (overlaps allowed), exact, three kernels.
# It is a true identity for every kernel, but its row sets (and column sets) are NOT the nodes of one tree.
from fractions import Fraction as Fr
from itertools import product
P = list(product((0,1), repeat=4))
def F(Y, X): return sum(X[i]*Y[3-i] for i in range(4))
q  = lambda X: (1-X[0])*X[3] + X[1]*X[2]
qp = lambda Y: Y[0]*Y[3] + Y[1]*Y[2]
inner_m = lambda Yi, Xi: Xi[0]*Yi[1] + Xi[1]*Yi[0] - Xi[0]*Xi[1] - Yi[0]*Yi[1]          # the 4-point brick: four single cells, values +1, -1
cells = [(Yi, Xi, inner_m(Yi, Xi)) for Yi in product((0,1), repeat=2) for Xi in product((0,1), repeat=2) if inner_m(Yi, Xi) != 0]
assert len(cells) == 4
def build(rho):
    rects = []           # (row set, column set, number)
    for a in (0,1):
        for b in (0,1):
            xm = (a == b)                      # quadrants (0,0),(1,1): the mismatch sits on X4; (0,1),(1,0): on Y4
            s = -1 if a == 0 else 1            # its sign
            rowsQ = [Y for Y in P if Y[0] == b]; colsQ = [X for X in P if X[0] == a]
            if xm:
                rects.append((frozenset(rowsQ), frozenset(X for X in colsQ if X[3] == 1), rho**s - 1))
                for Yi, Xi, v in cells:
                    R = frozenset(Y for Y in rowsQ if Y[1:3] == Yi)
                    rects.append((R, frozenset([(a,)+Xi+(0,)]), rho**v - 1))
                    rects.append((R, frozenset([(a,)+Xi+(1,)]), rho**s*(rho**v - 1)))
            else:
                rects.append((frozenset(Y for Y in rowsQ if Y[3] == 1), frozenset(colsQ), rho**s - 1))
                for Yi, Xi, v in cells:
                    C = frozenset(X for X in colsQ if X[1:3] == Xi)
                    rects.append((frozenset([(b,)+Yi+(0,)]), C, rho**v - 1))
                    rects.append((frozenset([(b,)+Yi+(1,)]), C, rho**s*(rho**v - 1)))
    return rects
def laminar(sets):
    s = list(set(sets)); bad = [(a, b) for i, a in enumerate(s) for b in s[i+1:] if not (a <= b or b <= a or not (a & b))]
    return len(bad)
for nm, rho in (("[[1,2],[3,4]]", Fr(2,3)), ("[[2,7],[5,3]]", Fr(6,35)), ("the transform", Fr(-1)), ("[[1,1],[1,5]]", Fr(5))):
    rects = build(rho)
    ok = all(rho**(F(Y,X) - q(X) - qp(Y)) == 1 + sum(p for R, C, p in rects if Y in R and X in C) for Y in P for X in P)
    print(nm, "rho", rho, ": rectangles off the centre", len(rects), "| identity on all 256 cells:", ok, "| constants that are zero:", sum(p == 0 for *_, p in rects),
          "| crossing pairs among the row sets:", laminar([R for R, _, _ in rects]), ", among the column sets:", laminar([C for _, C, _ in rects]))
rects = build(Fr(2,3)); rs = set(R for R, _, _ in rects); cs = set(C for _, C, _ in rects)
from collections import Counter
print("row sets by size:", sorted(Counter(len(R) for R in rs).items()), " column sets by size:", sorted(Counter(len(C) for C in cs).items()))
