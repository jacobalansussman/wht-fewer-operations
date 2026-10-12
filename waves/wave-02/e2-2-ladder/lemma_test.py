#!/usr/bin/env python3
"""lemma_test.py -- a test of the formula behind the clique lemma.  Exact rational arithmetic.  [e2-2-ladder]
Word = g_0 D_1 g_1 ... D_k g_k on R arrays (W live, the rest scratch); D_i changes the sign of array l_i when q(z_i) = 1.
Formula (e2-2.md, section 2): live part of the word = live part of (g_0 ... g_k) - 2 U_A (1 + 2 C_A)^(-1) W_A^T,
A = the blocks selected by q.  Part 1 checks it on random words (right or wrong: it is an identity), every form q.
Part 2 builds words that ARE right (plain schedules hidden behind random mixing with scratch), finds the tight forms and
checks the triangular pattern w_i.u_i = 1, w_i.u_j = 0 for i after j, and the clique bound.
"""
import random, itertools
from fractions import Fraction as Fr
random.seed(20261010)
def mm(A, B): return [[sum(A[i][t] * B[t][j] for t in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def eye(n): return [[Fr(int(i == j)) for j in range(n)] for i in range(n)]
def inv(A):
    n = len(A); M = [list(r) + e for r, e in zip(A, eye(n))]
    for c in range(n):
        p = next(r for r in range(c, n) if M[r][c] != 0); M[c], M[p] = M[p], M[c]
        x = M[c][c]; M[c] = [v / x for v in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c]; M[r] = [a - f * b for a, b in zip(M[r], M[c])]
    return [r[n:] for r in M]
def rnd(n):
    while True:
        A = [[Fr(random.randint(-2, 2)) for _ in range(n)] for _ in range(n)]
        try: inv(A); return A
        except StopIteration: pass
def qval(Q, z, pairs):
    return sum(1 for t, (i, j) in enumerate(pairs) if Q >> t & 1 and z >> i & 1 and z >> j & 1) & 1
def prod(ms, n):
    P = eye(n)
    for M_ in ms: P = mm(P, M_)
    return P
def check_word(m, W, R, g, blocks):
    """returns (#forms checked, #formula failures, data for part 2)"""
    k = len(blocks); pairs = [(i, j) for i in range(m) for j in range(i, m)]
    G = prod(g, R)
    U = [[prod(g[:i + 1], R)[a][blocks[i][0]] for a in range(W)] for i in range(k)]          # u_i (live rows)
    Wt = [[prod(g[i + 1:], R)[blocks[i][0]][b] for b in range(W)] for i in range(k)]         # w_i (live columns)
    C = [[prod(g[i + 1:j + 1], R)[blocks[i][0]][blocks[j][0]] if i < j else Fr(0) for j in range(k)] for i in range(k)]
    fails = 0; n = 0; out = []
    for Q in range(1 << len(pairs)):
        sel = [i for i in range(k) if qval(Q, blocks[i][1], pairs)]
        P = eye(R)
        for i in range(k + 1):
            P = mm(P, g[i])
            if i < k and i in sel:
                l = blocks[i][0]
                P = [[-v if c == l else v for c, v in enumerate(row)] for row in P]
        live = [row[:W] for row in P[:W]]
        if sel:
            Mx = [[Fr(int(a == b)) + 2 * C[i][j] for b, j in enumerate(sel)] for a, i in enumerate(sel)]
            Mi = inv(Mx)
            UA = [[U[i][a] for i in sel] for a in range(W)]
            WA = [[Wt[i][b] for b in range(W)] for i in sel]
            corr = mm(mm(UA, Mi), WA)
        else:
            corr = [[Fr(0)] * W for _ in range(W)]
        pred = [[G[a][b] - 2 * corr[a][b] for b in range(W)] for a in range(W)]
        n += 1; fails += (pred != live)
        qI = sum(Q >> t & 1 for t, (i, j) in enumerate(pairs) if i == j) & 1
        out.append((Q, sel, qI, live))
    return n, fails, (U, Wt, out)
# part 1: random words
tot = bad = 0
for trial in range(40):
    m = random.choice([2, 3]); R = random.choice([2, 3, 4]); W = random.randint(1, R); k = random.randint(1, 6)
    g = [rnd(R) for _ in range(k + 1)]
    blocks = [(random.randrange(R), random.randrange(1, 1 << m)) for _ in range(k)]
    n, f, _ = check_word(m, W, R, g, blocks); tot += n; bad += f
print("part 1: %d random words, %d (word, form) cases, formula wrong in %d" % (40, tot, bad))
# part 2: right words: plain schedule on W arrays, hidden by random mixing on R = W + scratch arrays between the blocks.
# g_0 = T_0, then block on array l in direction e_j, then T^-1 T' ...: write word = T_0^-1? simpler: conjugate each block:
# word = prod_i (T_i D_i T_i^-1) with T_i commuting with nothing in particular is NOT right in general, so use one T:
# word = T^-1 [plain schedule with permutation matrices and scratch-only mixing in between] T, T mixing live arrays only.
rightwords = tight_total = viol = cliqueviol = 0
for trial in range(30):
    m = 3; W = random.choice([2, 3]); S = random.choice([0, 1]); R = W + S
    T = rnd(W); Ti = inv(T)
    def emb(A):
        M_ = eye(R)
        for a in range(W):
            for b in range(W): M_[a][b] = A[a][b]
        return M_
    order = [(l, 1 << j) for l in range(W) for j in range(m)]; random.shuffle(order)
    k = len(order); g = [emb(Ti)]
    for i in range(k - 1):
        # between blocks: an invertible map that is diagonal on the live arrays (keeps the schedule right) and
        # does anything on the scratch ones, plus scratch -> scratch only
        M_ = eye(R)
        for a in range(W): M_[a][a] = Fr(random.choice([1, 2, -1, 3]))
        if S: M_[W][W] = Fr(random.choice([1, 2])); M_[W][random.randrange(W)] = Fr(random.randint(-1, 1))
        g.append(M_)
    scale = [Fr(1)] * W
    for M_ in g[1:]:
        for a in range(W): scale[a] *= M_[a][a]
    fin = eye(R)
    for a in range(W): fin[a][a] = 1 / scale[a]
    g.append(mm(fin, emb(T)))
    n, f, (U, Wt, out) = check_word(m, W, R, g, order)
    ok = all(live == [[Fr((-1) ** qI * int(a == b)) for b in range(W)] for a in range(W)] for (Q, sel, qI, live) in out)
    if not ok: continue
    rightwords += 1; bad += f
    joined = set()
    for Q, sel, qI, live in out:
        if qI == 1 and len(sel) == W:
            tight_total += 1
            for a in sel:
                for b in sel:
                    d = sum(Wt[a][t] * U[b][t] for t in range(W))
                    if (a == b and d != 1) or (a > b and d != 0): viol += 1
                    if a < b: joined.add((a, b))
    # clique bound: brute force over subsets of blocks pairwise joined
    for r in range(W + 1, min(k, W + 2) + 1):
        for T_ in itertools.combinations(range(k), r):
            if all((a, b) in joined for a, b in itertools.combinations(T_, 2)): cliqueviol += 1
print("part 2: %d right words built (with mixing; scratch in some); tight forms met: %d; triangular pattern violated: %d; sets of more than W blocks pairwise joined: %d; formula wrong: %d"
      % (rightwords, tight_total, viol, cliqueviol, bad))
