#!/usr/bin/env python3
"""ring.py [ab-6-chainexchanges, 2026-10-11]   EXACT, whole numbers and fractions only.
A formal register machine for the engine's steps WITHOUT address maps and without address-dependent phase letters:
additions (any rational combinations, free), shifts (free), blocks of directions (paid: rank = number of moves).
Why this is the engine's own formal game on those letters: dir(z) and shift(z) are all diagonal in the basis of characters,
dir(z) = i^(y.z), shift(z) = (-1)^(y.z); so a product of them IS the function q(y) in Z/4 with matrix i^q(y), and two
products are the same matrix exactly when the functions are equal.  A term "[g] v_l" is stored as (l, q).  By GAME.md
section 5 [read] a word is right for every number of digit columns exactly when it is right as such a formal sum.
h = 4, 16 addresses, m = 4.  Port p = 0111; an orthonormal basis of p-perp: 1110, 1101, 1011 (all of weight 3)."""
from fractions import Fraction as Fr
h = 4; N = 1 << h
wt = lambda x: bin(x).count("1"); par = lambda y, z: wt(y & z) & 1
QF = tuple(wt(y) % 4 for y in range(N))                       # the kernel dir(e1)...dir(e4)
class Machine:
    def __init__(s, nlive, nscratch):
        s.n = nlive + nscratch; s.live = nlive
        s.a = [dict() for _ in range(s.n)]
        for l in range(nlive): s.a[l][(l, (0,) * N)] = Fr(1)
        s.blocks = [[] for _ in range(s.n)]                   # ranks of the block letters, per array
    def block(s, r, zs, sign):                                # one block letter of rank len(zs); sign[j] = +1: dir(z), -1: dir(z)^-1 = dir(z) shift(z)
        assert 1 <= len(zs)
        new = {}
        for (l, q), c in s.a[r].items():
            q2 = tuple((q[y] + sum(sg * par(y, z) for z, sg in zip(zs, sign))) % 4 for y in range(N))
            new[(l, q2)] = c
        s.a[r] = new; s.blocks[r].append(len(zs))
    def shift(s, r, z):
        s.a[r] = {(l, tuple((q[y] + 2 * par(y, z)) % 4 for y in range(N))): c for (l, q), c in s.a[r].items()}
    def add(s, t, coef, src):                                 # array t += coef * array src   (free)
        for k, c in list(s.a[src].items()):
            v = s.a[t].get(k, 0) + Fr(coef) * c
            if v: s.a[t][k] = v
            else: s.a[t].pop(k, None)
    def copy(s, t, src): s.a[t] = dict(s.a[src])
    def scale(s, r, c): s.a[r] = {k: Fr(c) * v for k, v in s.a[r].items()}
    def swap(s, r, t): s.a[r], s.a[t] = s.a[t], s.a[r]
    def ok(s): return all(s.a[l] == {(l, QF): Fr(1)} for l in range(s.live))
    def moves(s): return sum(sum(b) for b in s.blocks)
p = 0b0111; U = (0b1110, 0b1101, 0b1011)
mvs = lambda z: 1 if wt(z) % 4 == 1 else -1                   # relation.py's rule: forwards for weight 1 mod 4, backwards for 3 mod 4
def climb(M, r, zs): M.block(r, list(zs), [mvs(z) for z in zs])
def descend(M, r, zs): M.block(r, list(zs), [-mvs(z) for z in zs])
# check of the frame: the product of the moves along p and U is the kernel
M = Machine(1, 0); climb(M, 0, (p,) + U); print("(0) moves along p and the orthonormal basis of p-perp give the kernel:", M.ok())

def report(name, M, plain):
    print("%s\n    every live array ends holding exactly the kernel applied to its own input (formal sum): %s" % (name, M.ok()))
    print("    moves %d (plain schedule %d); blocks per array, live then scratch: %s" % (M.moves(), plain, M.blocks))

# (1) the three-shear exchange as three stages; stage k = everything in the block B_k = span(p, U_k) except p.
#     Legal word; ONE pair, so every total serves one source (kappa = 1) and nothing is saved.
M = Machine(2, 1); X, Y, S = 0, 1, 2
climb(M, X, U[0:1]);                 M.copy(S, X); descend(M, S, (p, U[0]));                    M.add(Y, 1, S)      # Y += x X,  x = (move along p)^-1
climb(M, Y, U[0:2]);                 M.copy(S, Y); descend(M, S, (p, U[1])); M.shift(S, p);     M.add(X, -1, S)     # X -= x^-1 Y
climb(M, X, U[1:3]);                 M.copy(S, X); descend(M, S, (p, U[2]));                    M.add(Y, 1, S)      # Y += x X
climb(M, Y, U[2:3])
M.swap(X, Y); M.scale(Y, -1); M.shift(X, p)                                                                          # free: exchange back, sign, relabel
report("(1) plain exchange, 3 stages, the port p never moved along by X or Y:", M, 8)

# (2) the two-stage word with a bystander: 3 arrays, 2 stages, 4 shears; contents 1 and 2 get the port move, content 3 does not.
#     glue identity [derived]:  B A = [[1, x, x^2], [-1/x, 0, 0], [1/x^2, 0, 1]]  for A = chain 3 -> 2 -> 1 with x, B = chain 1 -> 2 -> 3 with -1/x.
M = Machine(3, 1); A1, A2, A3, S = 0, 1, 2, 3
M.copy(S, A1); M.shift(S, p); M.add(A3, -1, S)                                                                       # A3 = c3 - x^-2 c1  (free)
UA, UB = U[0:1], U[1:3]
climb(M, A3, UA); M.copy(S, A3); descend(M, S, (p,) + UA); M.add(A2, 1, S)                                           # stage A: 3 -> 2
climb(M, A2, UA); M.copy(S, A2); descend(M, S, (p,) + UA); M.add(A1, 1, S)                                           #          2 -> 1
climb(M, A1, UA + UB)                                                                                                # A1: stage A and stage B in ONE block
M.copy(S, A1); descend(M, S, (p,) + UB); M.shift(S, p); M.add(A2, -1, S)                                             # stage B: 1 -> 2
climb(M, A2, UB); M.copy(S, A2); descend(M, S, (p,) + UB); M.shift(S, p); M.add(A3, -1, S)                           #          2 -> 3
climb(M, A3, UB)
M.copy(S, A3); M.shift(S, p); M.add(A1, -1, S)                                                                       # A1 -= x^2 A3   (free)
climb(M, A3, (p,))                                                                                                   # the bystander pays its own port move
M.swap(A1, A2); M.scale(A1, -1); M.shift(A2, p)
report("(2) two-stage exchange with a bystander (arrays 1, 2 never move along p; array 3 does):", M, 12)

# (3) control: the same word (2) with the last shear left out must fail
M = Machine(3, 1)
M.copy(S, A1); M.shift(S, p); M.add(A3, -1, S)
climb(M, A3, UA); M.copy(S, A3); descend(M, S, (p,) + UA); M.add(A2, 1, S)
climb(M, A2, UA); M.copy(S, A2); descend(M, S, (p,) + UA); M.add(A1, 1, S)
climb(M, A1, UA + UB)
M.copy(S, A1); descend(M, S, (p,) + UB); M.shift(S, p); M.add(A2, -1, S)
climb(M, A2, UB); climb(M, A3, UB)
M.copy(S, A3); M.shift(S, p); M.add(A1, -1, S); climb(M, A3, (p,)); M.swap(A1, A2); M.scale(A1, -1); M.shift(A2, p)
print("(3) control, word (2) without its fourth shear: right? %s  (must be False)" % M.ok())

# (4) a ring of three arrays, three two-stage words in a row is NOT possible at h = 4 (one port, D D = a relabelling):
#     what the algebra gives instead: a content that takes the same port move twice has gained nothing.
M = Machine(2, 1); X, Y, S = 0, 1, 2
M.copy(S, X); M.block(S, [p], [-1]); M.add(Y, 1, S)           # Y += D^-1 X
M.copy(S, Y); M.block(S, [p], [-1]); M.add(Y, -1, Y); M.add(Y, 1, S)   # Y := D^-1 (y + D^-1 x): the term of x has passed the port twice
tx = [q for (l, q) in M.a[Y] if l == 0][0]
print("(4) a content that hops twice along the same port sits at the level of a free relabelling (shift by p) of its start:",
      tx == tuple((2 * par(y, p)) % 4 for y in range(N)))

# (5) the smallest batch: ONE total for TWO sources whose ports know each other (kappa = 2).  Ports p1 = 0111, p2 = 1011,
#     a = 1101, b = 1110: an orthonormal basis.  Source t climbs p_t-perp; the total comes down the whole block (4 moves);
#     both targets read it; target t climbs p_t-perp and then holds an unwanted share of the other source, which is that
#     source after the two moves a, b: a value the source held in the MIDDLE of its climb.
p1, p2, aa, bb = 0b0111, 0b1011, 0b1101, 0b1110
M = Machine(4, 3); X1, Y1, X2, Y2, S, H1, H2 = 0, 1, 2, 3, 4, 5, 6
climb(M, X1, (aa, bb)); M.copy(H1, X1); climb(M, X1, (p2,))                 # source 1: cut in two by the read of H1
climb(M, X2, (aa, bb)); M.copy(H2, X2); climb(M, X2, (p1,))
M.copy(S, X1); M.add(S, 1, X2); descend(M, S, (p1, p2, aa, bb))             # one total, 4 moves, two shears
M.add(Y1, 1, S); M.add(Y2, 1, S)
climb(M, Y1, (aa, bb, p2)); climb(M, Y2, (aa, bb, p1))
before = (len(M.a[Y1]), len(M.a[Y2]))
M.add(Y1, -1, H2); M.add(Y2, -1, H1)                                        # the unwanted shares come off by additions alone
# expected: Y_t = (climb of p_t-perp)(y_t + x^-1... the source moved backwards along p_t), X_t = (climb)(x_t)
E = Machine(4, 1)
for (xs, ys, pt, G) in ((0, 1, p1, (aa, bb, p2)), (2, 3, p2, (aa, bb, p1))):
    E.copy(4, xs); descend(E, 4, (pt,)); E.add(ys, 1, 4); climb(E, ys, G); climb(E, xs, G)
same = all(M.a[r] == E.a[r] for r in range(4))
print("(5) one total for two sources (kappa = 2): terms in the targets before the removal %s; after the removal the state equals"
      " 'each target += its source moved backwards along its own port, everybody climbed': %s" % (before, same))
print("    blocks per array: sources %s %s (cut by the helper's read), targets %s %s, the total %s; 4 moves for 2 shears (2 single moves would do)"
      % (M.blocks[X1], M.blocks[X2], M.blocks[Y1], M.blocks[Y2], M.blocks[S]))
