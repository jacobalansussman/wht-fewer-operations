# a-1 extra: (1) the symmetric middle alone with the pair inputs scaled by 2 (free), (2) Krawtchouk blocks, (3) growth law.
import verify as V
from fractions import Fraction as Fr
# (1) sym middle alone: S coordinate of a pair = F[x][y] + F[y][x] = 2 * (off-diagonal entry); feed 2 * unit. Monkey-patch Circ.inp use:
def middle_sym(q, brick):
    H, pairs, symc, A2, S2 = V.squares(q)
    idx = {p: i for i, p in enumerate(symc)}; c = V.Circ(len(symc))
    sym0 = [c.inp(idx[(x, x)]) for x in range(q)]; sm = {}
    for m in range(1, q):
        p = V.low(m); sm[m] = []
        for e in range(q // 2):
            x = V.spread(e, p); y = x ^ m
            sm[m].append([2*t for t in c.inp(idx[(min(x, y), max(x, y))])])
    def half(s0, s):
        C = {}; t = V.wht(c, s0, brick)
        for w in range(q): C[(w, 0)] = t[w]
        for m in range(1, q):
            p = V.low(m); t = V.wht(c, s[m], brick)
            for e in range(q // 2):
                w = V.spread(e, p)
                if V.par(w & m): w |= 1 << p
                C[(w, m)] = t[e]
        return C
    C = half(sym0, sm)
    s0 = [C[(0, m)] for m in range(q)]; sw = {}
    for w in range(1, q):
        p = V.low(w); sw[w] = []
        for e in range(q // 2):
            m = V.spread(e, p)
            if V.par(m & w): m |= 1 << p
            sw[w].append(C[(w, m)])
    D = half(s0, sw)
    outs = list(D.values())
    def propto(o, r):
        k = [(x, y) for x, y in zip(o, r) if x or y]
        return bool(k) and all(x*k[0][1] == y*k[0][0] for x, y in k) and k[0][1] != 0 and k[0][0] != 0
    hit = [sum(1 for o in outs if propto(o, r)) for r in S2]
    return c.g, all(h == 1 for h in hit)
for q, brick in ((4, 0), (4, 1), (8, 0), (8, 1), (16, 0), (16, 1)):
    g, ok = middle_sym(q, brick); print("sym middle alone q=%d brick=%d: %d gates, every row of the symmetric square produced exactly once: %s" % (q, brick, g, ok))
# (2) Krawtchouk blocks of the antisymmetric square
H, pairs, symc, A2, S2 = V.squares(4); ip = {p: i for i, p in enumerate(pairs)}
newb = [{(0, 1): 1}, {(0, 3): 1, (1, 2): -1}, {(2, 3): 1}, {(0, 2): 1}, {(0, 3): 1, (1, 2): 1}, {(1, 3): 1}]
P = [[0]*6 for _ in range(6)]
for j, b in enumerate(newb):
    for pr, v in b.items(): P[ip[pr]][j] = v
def solve(P, B):
    n = len(P); M = [[Fr(x) for x in P[i]] + [Fr(x) for x in B[i]] for i in range(n)]
    for col in range(n):
        piv = next(r for r in range(col, n) if M[r][col] != 0); M[col], M[piv] = M[piv], M[col]
        M[col] = [x / M[col][col] for x in M[col]]
        for r in range(n):
            if r != col and M[r][col] != 0: M[r] = [x - M[r][col]*y for x, y in zip(M[r], M[col])]
    return [row[n:] for row in M]
X = solve(P, V.mm(A2, P))
print("antisymmetric square in the basis {01, 03-12, 23 | 02, 03+12, 13} (one butterfly away from the pair basis):")
for r in X: print("   ", [int(v) for v in r])
print("   block-diagonal:", all(X[i][j] == 0 for i in range(6) for j in range(6) if (i < 3) != (j < 3)))
K = [[1, 2, 1], [1, 0, -1], [1, -2, 1]]
print("   Krawtchouk matrix K = Sym^2 of [[1,1],[1,-1]] in the basis e0^2, e0e1, e1^2 :", K, " K^2 = 4I:", V.mm(K, K) == [[4*(i == j) for j in range(3)] for i in range(3)])
# (3) growth law. s(n) = textbook(n) - T(n). Route: s(q^2) = 2 s(q) + 4 (q-1) s(q/2). Tensor product: s(q^2) = 2 q s(q).
def lg(n): return n.bit_length() - 1
def best(n):      # 7-gate block on pairs of bits (count G), the best known to tonight's reports
    d = lg(n); return 7*d*n//8 if d % 2 == 0 else 7*(d-1)*n//8 + n
print("%8s %12s %12s %12s %10s %10s" % ("points", "textbook", "route", "7-gate blocks", "route/tb", "blocks/tb"))
for j in (1, 2, 3, 4, 5, 8, 16, 32, 64):
    q = 1 << j; n = q*q; tb = n*lg(n)
    route = 2*(q*q - q) + 2*best(q) + 4*(q - 1)*best(q // 2) if q > 1 else 0
    print("%8s %12d %12d %12d %10.5f %10.5f" % ("2^%d" % (2*j), tb, route, best(n), route/tb, best(n)/tb))
# identity: route - tensor = 2 (q-1) (s(q) - 2 s(q/2)) >= 0 for every price list with T(q) <= 2 T(q/2) + q
import random
random.seed(1); bad = 0
for trial in range(2000):
    T = {1: 0, 2: 2}
    for j in range(2, 12):
        q = 1 << j; T[q] = random.randint(q - 1, 2*T[q//2] + q)      # any price between the trivial floor and "one layer on top"
    for j in range(2, 12):
        q = 1 << j; route = 2*(q*q - q) + 2*T[q] + 4*(q - 1)*T[q//2]; tensor = 2*q*T[q]
        if route < tensor: bad += 1
        assert route - tensor == 2*(q - 1)*(2*T[q//2] + q - T[q])
print("random price lists with T(q) <= 2T(q/2) + q: cases where the route beats the plain product 2 q T(q):", bad, "of", 2000*10)
