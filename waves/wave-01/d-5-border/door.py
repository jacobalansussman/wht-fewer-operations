# The door example, exact rational arithmetic.
# Border program on n wires, 2n-1 gates: chain 1 adds the inputs in the order 1..n, chain 2 in the order n..1,
# every coefficient is 1 + (integer)*e; last gate w = (u - v)/e, where u and v are the two chain ends (same limit: all-ones).
# Limits: prefix sums, suffix sums, all-ones (twice), and w = u_1 - v_1.
# Certificate that the limit set needs 3n-4 gates exactly: w lies in the span of no n-1 of the other points (all dets non-zero);
# then the cone of w needs n leaves among the other points, hence n-2 helper gates that are not targets.
import sys, itertools, random
from fractions import Fraction as Fr
n = int(sys.argv[1]); random.seed(int(sys.argv[2]))
def add(u, a, v, b):   # a, b polynomials in e (lists); u, v lists (by power of e) of vectors
    L = max(len(u)+len(a), len(v)+len(b)) - 1
    w = [[Fr(0)]*n for _ in range(L)]
    for (x, c) in ((u, a), (v, b)):
        for i, vec in enumerate(x):
            for k, ck in enumerate(c):
                for j in range(n): w[i+k][j] += ck*vec[j]
    return w
E = [[[Fr(int(i == j)) for i in range(n)]] for j in range(n)]
def chain(order):
    nodes = []; cur = E[order[0]]
    for j in order[1:]:
        cur = add(cur, [Fr(1)], E[j], [Fr(1), Fr(random.choice([2,3,5,7,11,13,17,19,23,29,31,37,41,43])*random.choice([1,-1]))]); nodes.append(cur)
    return nodes
c1 = chain(list(range(n))); c2 = chain(list(range(n-1, -1, -1)))
u, v = c1[-1], c2[-1]
d = add(u, [Fr(1)], v, [Fr(-1)])
assert all(x == 0 for x in d[0]); w = d[1:]          # w = (u - v)/e : one gate with coefficients 1/e and -1/e
print("n =", n, "| border gates:", len(c1)+len(c2)+1)
lim = [tuple(x[0]) for x in c1+c2]
print("limits of the two chains:", [tuple(int(a) for a in t) for t in lim])
print("w(e) coefficient vectors by power of e:", [[int(a) for a in vec] for vec in w], "(degree 0 in e means w is exact for every e)")
F = set(tuple(int(a) for a in t) for t in lim) | set(tuple(int(i == j) for i in range(n)) for j in range(n))
F = sorted(F); wv = [int(a) for a in w[0]]
def det(M):
    M = [[Fr(x) for x in r] for r in M]; d = Fr(1); m = len(M)
    for c in range(m):
        p = next((r for r in range(c, m) if M[r][c] != 0), None)
        if p is None: return Fr(0)
        if p != c: M[c], M[p] = M[p], M[c]; d = -d
        d *= M[c][c]
        for r in range(c+1, m):
            f = M[r][c]/M[c][c]
            if f: M[r] = [a - f*b for a, b in zip(M[r], M[c])]
    return d
def rank(M):
    M = [[Fr(x) for x in r] for r in M]; r = 0
    for c in range(n):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]
        for i in range(r+1, len(M)):
            f = M[i][c]/M[r][c]
            if f: M[i] = [a - f*b for a, b in zip(M[i], M[r])]
        r += 1
    return r
zero = sum(1 for S in itertools.combinations(F, n-1) if rank([list(s) for s in S] + [wv]) == rank([list(s) for s in S]))
tot = sum(1 for _ in itertools.combinations(F, n-1))
print("distinct limit targets (not inputs):", len(F) - n + 1, "| fixed points:", len(F), "| (n-1)-subsets whose span contains w:", zero, "of", tot)
print("=> exact count >=", (len(F) - n + 1) + (n - 2), "if that number is 0 ; border count <=", 2*n - 1)
