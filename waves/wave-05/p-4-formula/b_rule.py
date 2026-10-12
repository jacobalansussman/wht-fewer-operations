# p-4-formula (b),(c): the rule behind the 5 and the 13, pushed to k = 4, 5. Exact, whole-number exponents, so every
# identity below holds for EVERY kernel [[a,b],[c,d]] with no zero entry at once (rho = ad/(bc), K = scalings * rho^F).
# Bits X1..Xk (columns), Y1..Yk (rows); F(Y,X) = sum_i X_i * Y_(k+1-i)  (a relabelling of the usual x.y). Count (G).
from itertools import product, permutations
from fractions import Fraction as Fr
import sys

def F(Y, X): k = len(X); return sum(X[i]*Y[k-1-i] for i in range(k))
def pts(k): return list(product((0,1), repeat=k))

# --- the cyclic rule: outer pair (X1,Yk),(Xk,Y1); column half X1=a is matched to row half b*(a)=1-a, row half Y1=b to a*(b)=b
def q_rule(X, inner):      # centre exponent over columns
    k = len(X)
    if k == 0: return 0
    if k == 1: return 0
    return (1 - X[0])*X[-1] + inner[0](X[1:-1], X[0])
def qp_rule(Y, inner):
    k = len(Y)
    if k <= 1: return 0
    return Y[0]*Y[-1] + inner[1](Y[1:-1], Y[0])
def m_of(k, q, qp): return {(Y, X): F(Y, X) - q(X) - qp(Y) for Y in pts(k) for X in pts(k)}

def nodes(k, order):       # nodes of the merge tree that splits on the bits in this order: (set of points) for each prefix
    out = []
    for d in range(k+1):
        for vals in product((0,1), repeat=d):
            out.append(frozenset(P for P in pts(k) if all(P[order[i]] == vals[i] for i in range(d))))
    return out
def greedy(k, m, rorder, corder):
    R = sorted(nodes(k, rorder), key=len, reverse=True); C = sorted(nodes(k, corder), key=len, reverse=True)
    cand = sorted(((len(r)*len(c), r, c) for r in R for c in C), key=lambda t: -t[0])
    covered = set(); rects = []
    for area, r, c in cand:
        cells = [(y, x) for y in r for x in c]
        v = m[cells[0]]
        if v == 0 or any(m[z] != v for z in cells) or any(z in covered for z in cells): continue
        covered.update(cells); rects.append((r, c, v))
    assert all((m[z] != 0) == (z in covered) for z in m)
    return rects
def laminar(sets):
    s = list(set(sets))
    return all(a <= b or b <= a or not (a & b) for i, a in enumerate(s) for b in s[i+1:])

# ---------- k = 2 and k = 3: the rule reproduces 5 and 13
zero = (lambda Xi, a: 0, lambda Yi, b: 0)
m2 = m_of(2, lambda X: q_rule(X, zero), lambda Y: qp_rule(Y, zero))
r2 = greedy(2, m2, (0,1), (0,1))
print("k=2 cyclic rule: rectangles off the centre", len(r2), "-> tau", 1+len(r2), "gates", 4-2+1+len(r2), "| shapes", sorted((len(r),len(c),v) for r,c,v in r2))
inner13 = (lambda Xi, a: a*Xi[0], lambda Yi, b: 0)          # column half X1=1 uses the other centre of the 2-point kernel
m3 = m_of(3, lambda X: q_rule(X, inner13), lambda Y: qp_rule(Y, inner13))
r3 = greedy(3, m3, (0,1,2), (0,1,2))
print("k=3 cyclic rule: rectangles off the centre", len(r3), "-> tau", 1+len(r3), "gates", 8-2+1+len(r3), "| shapes", sorted((len(r),len(c),v) for r,c,v in r3))
# compare with k-cross's twelve rectangles, transported: kernel row y=(y3 y2 y1) -> Y=(y3,y1,y2); kernel column x -> X=(x2,x1,x3)
terms = [((1,2,4,7),(7,)), ((0,3,5,6),(5,)), ((1,7),(6,)), ((0,6),(4,)), ((3,5),(3,)), ((2,4),(1,)),
         ((0,),(0,7)), ((6,),(1,6)), ((1,),(2,5)), ((7,),(3,4)), ((5,),(0,1,6,7)), ((4,),(2,3,4,5))]
sig = (0, 1, 2, 3, 7, 6, 5, 4); pi = {2: 1, 3: 4, 7: 0, 1: 2, 6: 5, 0: 7, 4: 3, 5: 6}
ty = lambda y: (y>>2&1, y&1, y>>1&1); tx = lambda x: (x>>1&1, x&1, x>>2&1)
kc = {(frozenset(ty(pi[j]) for j in nu), frozenset(tx(sig[i]) for i in mu)) for nu, mu in terms}
print("   the twelve rectangles of the rule ARE k-cross's twelve (as sets of rows x sets of columns):", kc == {(r, c) for r, c, v in r3},
      "| values +1:", sum(v == 1 for *_, v in r3), " -1:", sum(v == -1 for *_, v in r3))
print("   formula checked on all 64 cells: m = X1Y3 + X2Y2 + X3Y1 - X3(1-X1) - X1X2 - Y1Y3 :",
      all(m3[(Y,X)] == X[0]*Y[2]+X[1]*Y[1]+X[2]*Y[0]-X[2]*(1-X[0])-X[0]*X[1]-Y[0]*Y[2] for Y in pts(3) for X in pts(3)))
for a in (0,1):
    for b in (0,1):
        vals = sorted({m3[(Y,X)] for Y in pts(3) for X in pts(3) if X[0]==a and Y[0]==b})
        n = sum(1 for r,c,v in r3 if all(x[0]==a for x in c) and all(y[0]==b for y in r))
        print("   quadrant X1=%d Y1=%d: values of m %s, rectangles inside %d" % (a, b, vals, n))

# ---------- k = 4, 5: push the rule once and twice; best greedy tiling over all bit orders of the two trees
def best(k, m, orders=None, cap=None):
    bestn = None; n = 0
    allo = list(permutations(range(k))) if orders is None else orders
    for ro in allo:
        for co in allo:
            if cap and n >= cap: break
            n += 1
            r = greedy(k, m, ro, co)
            if bestn is None or len(r) < bestn[0]: bestn = (len(r), ro, co, r)
    return bestn
brick_cells = (lambda Xi, a: Xi[0]*Xi[1], lambda Yi, b: Yi[0]*Yi[1])                     # inner 4-point brick, four single cells
brick_cyc   = (lambda Xi, a: (1-Xi[0])*Xi[1], lambda Yi, b: Yi[0]*Yi[1])                 # inner 4-point brick, cyclic form
for name, inner in (("inner brick = four single cells", brick_cells), ("inner brick = cyclic form", brick_cyc)):
    m4 = m_of(4, lambda X: q_rule(X, inner), lambda Y: qp_rule(Y, inner))
    vals = sorted(set(m4.values())); nz = sum(v != 0 for v in m4.values())
    n, ro, co, r = best(4, m4)
    print("k=4,", name, ": values of m", vals, "non-zero cells", nz, "| fewest tree rectangles found (greedy tiling, all 24x24 bit orders):", n,
          "-> tau", n+1, "gates", 16-2+n+1, "| row order", ro, "column order", co, "| laminar", laminar([x for x,_,_ in r]), laminar([x for _,x,_ in r]))
    sys.stdout.flush()
    if name.startswith("inner brick = four"):
        keep4 = (m4, r, lambda X: q_rule(X, brick_cells), lambda Y: qp_rule(Y, brick_cells))
# exact replay of the k = 4 tree form on three kernels: K = (row scaling)(column scaling) * [1 + sum (rho^v - 1) on rectangles]
m4, r4, q4, qp4 = keep4
for nm, ker in (("[[1,2],[3,4]]", [[1,2],[3,4]]), ("[[2,7],[5,3]]", [[2,7],[5,3]]), ("the transform [[1,1],[1,-1]]", [[1,1],[1,-1]])):
    a_, b_, c_, d_ = [Fr(v) for v in (ker[0][0], ker[0][1], ker[1][0], ker[1][1])]; rho = a_*d_/(b_*c_)
    ok = True
    for Y in pts(4):
        for X in pts(4):
            Yk = Y[::-1]                                     # kernel row index pairs X_i with Y_(5-i)
            true = Fr(1)
            for i in range(4): true *= Fr(ker[Yk[i]][X[i]])
            rs = Fr(1)
            for i in range(4): rs *= (a_ if (Yk[i], X[i]) == (0,0) else b_ if (Yk[i], X[i]) == (0,1) else c_ if (Yk[i], X[i]) == (1,0) else b_*c_/a_)
            # rs = the kernel power with d replaced by bc/a: a rank-one matrix (row scaling times column scaling)
            val = rs * rho**(q4(X) + qp4(Y)) * (1 + sum((rho**v - 1) for rr, cc, v in r4 if Y in rr and X in cc))
            ok &= (val == true)
    print("   k=4 replay,", nm, ": rho =", rho, "| all 256 entries equal:", ok, "| rectangles whose constant rho^v - 1 is zero:", sum(1 for *_, v in r4 if rho**v == 1))
# ideal (product) count of the rule at k = 4: outer 2-cell rectangles times inner cells, no trees asked
print("ideal count of the rule (no tree asked), T(k) = 8 T(k-2) - 3 :", "even k:", [1, 5, 37, 293, 2341], " odd k:", [2, 13, 101, 805], " | textbook tau: 2 6 18 50 130 322 770 1794")

# ---------- the conservation law of mismatch, by brute force: j outer bits per side
for j in (1, 2):
    P = pts(j); best_S = None; sums = set()
    maps = list(product(P, repeat=len(P)))
    for astar in maps:
        for bstar in maps:
            S = 0; D = 0
            for ia, a in enumerate(P):
                for ib, b in enumerate(P):
                    d = sum(u != v for u, v in zip(a, astar[ib])) + sum(u != v for u, v in zip(b, bstar[ia]))
                    S += 2**d; D += d
            sums.add(D)
            if best_S is None or S < best_S: best_S = S
    print("mismatch, j =", j, ": total mismatch over the", 4**j, "blocks, all", len(maps)**2, "choices of centre:", sorted(sums), "(always j*4^j =", j*4**j, ") | least sum of 2^mismatch:", best_S, "= 8^j:", best_S == 8**j, "| textbook choice gives", 9**j)
