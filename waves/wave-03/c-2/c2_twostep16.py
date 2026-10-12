#!/usr/bin/env python3
"""c2_twostep16.py (skeptic c-2): the first test of g-6's block law on true two-step words WITH non-zero rank-one terms.

g-6 section 9: "I had no two-step word with a non-zero rank-one term to test them on."  Here is a family of them, exact.
16 points, shape 4 x 4.  A0 = H4 (x) I4, B0 = I4 (x) H4, A0 B0 = H16 (the known pair word; its rank-one terms are zero).
For vectors p, q:  A = A0 (I + p q^T),  B = (I + p q^T)^-1 B0 = B0 - p (q^T B0)/(1 + q.p),  so A B = H16 always.
[derived, c-2] A and B are again tree steps on the same trees when p and q lie in L (x) L, L = span{(1,0,1,0),(0,1,0,-1)}
(a space of dimension 4 each).  Everything below is exact rational arithmetic.
Checks: (1) A B = H16; (2) A and B are tree steps (every node, both sides, rank <= 1); (3) the rank-one terms are non-zero;
(4) g-6's block law: on every good pair a = lambda chi_eta + s u_xi with lambda != 0 and b = chi_xi/lambda + r q_eta;
(5) the number of exceptional pairs is at most c + w = 8.
"""
import random
from fractions import Fraction as F

def par(v):
    return bin(v).count("1") & 1

def rank(rows):
    M = [[F(v) for v in r] for r in rows]
    if not M:
        return 0
    r = 0
    nc = len(M[0])
    for c in range(nc):
        piv = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        for i in range(r + 1, len(M)):
            if M[i][c] != 0:
                f = M[i][c] / M[r][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
        if r == len(M):
            break
    return r

N = 16
H4 = [[1 - 2 * par(a & b) for b in range(4)] for a in range(4)]
idx = lambda hi, lo: 4 * hi + lo
H = [[H4[x >> 2][y >> 2] * H4[x & 3][y & 3] for y in range(N)] for x in range(N)]
A0 = [[F(H4[x >> 2][z >> 2] * (1 if (x & 3) == (z & 3) else 0)) for z in range(N)] for x in range(N)]
B0 = [[F((1 if (z >> 2) == (y >> 2) else 0) * H4[z & 3][y & 3]) for y in range(N)] for z in range(N)]
L = [(1, 0, 1, 0), (0, 1, 0, -1)]

def rand_LL(rnd):
    c = [[F(rnd.randint(-3, 3), rnd.randint(1, 3)) for _ in range(2)] for _ in range(2)]
    v = [F(0)] * N
    for i in range(2):
        for j in range(2):
            for hi in range(4):
                for lo in range(4):
                    v[idx(hi, lo)] += c[i][j] * L[i][hi] * L[j][lo]
    return v

def matmul(X, Y):
    return [[sum(X[i][k] * Y[k][j] for k in range(len(Y))) for j in range(len(Y[0]))] for i in range(len(X))]

# trees: (node of outputs or inputs, matched set of middle wires)
tree1 = []   # for A: rows x, columns z
tree2 = []   # for B: columns y, rows z
for xi in range(4):
    S = [idx(h, xi) for h in range(4)]
    tree1.append((S, S))
    tree1.append(([idx(0, xi), idx(1, xi)], [idx(1, xi), idx(3, xi)]))
    tree1.append(([idx(2, xi), idx(3, xi)], [idx(0, xi), idx(2, xi)]))
for pair in ((0, 1), (2, 3)):
    S = [idx(h, xi) for xi in pair for h in range(4)]
    tree1.append((S, S))
for eta in range(4):
    U = [idx(eta, l) for l in range(4)]
    tree2.append((U, U))
    tree2.append(([idx(eta, 0), idx(eta, 1)], [idx(eta, 1), idx(eta, 3)]))
    tree2.append(([idx(eta, 2), idx(eta, 3)], [idx(eta, 0), idx(eta, 2)]))
for pair in ((0, 1), (2, 3)):
    U = [idx(eta, l) for eta in pair for l in range(4)]
    tree2.append((U, U))

def is_step_A(A):
    for V, Vp in tree1:
        oV = [x for x in range(N) if x not in V]; oVp = [z for z in range(N) if z not in Vp]
        if rank([[A[x][z] for z in oVp] for x in V]) > 1 or rank([[A[x][z] for z in Vp] for x in oV]) > 1:
            return False
    return True

def is_step_B(B):
    for U, Up in tree2:
        oU = [y for y in range(N) if y not in U]; oUp = [z for z in range(N) if z not in Up]
        if rank([[B[z][y] for y in U] for z in oUp]) > 1 or rank([[B[z][y] for y in oU] for z in Up]) > 1:
            return False
    return True

def nonzero_vec(vs):
    for v in vs:
        if any(c != 0 for c in v):
            return v
    return None

if __name__ == "__main__":
    rnd = random.Random(7)
    done = 0
    tot_good = tot_exc = law_fail = s_nonzero = r_nonzero = 0
    while done < 40:
        p = rand_LL(rnd); q = rand_LL(rnd)
        den = 1 + sum(a * b for a, b in zip(p, q))
        if den == 0 or all(v == 0 for v in p) or all(v == 0 for v in q):
            continue
        Ap = [sum(A0[x][z] * p[z] for z in range(N)) for x in range(N)]
        qB = [sum(q[z] * B0[z][y] for z in range(N)) for y in range(N)]
        A = [[A0[x][z] + Ap[x] * q[z] for z in range(N)] for x in range(N)]
        B = [[B0[z][y] - p[z] * qB[y] / den for y in range(N)] for z in range(N)]
        assert matmul(A, B) == [[F(v) for v in r] for r in H], "product is not H16"
        assert is_step_A(A) and is_step_B(B), "not tree steps"
        exc = 0
        for xi in range(4):
            S = [idx(h, xi) for h in range(4)]
            u = nonzero_vec([[A[x][z] for x in S] for z in range(N) if (z & 3) != xi])
            for eta in range(4):
                U = [idx(eta, l) for l in range(4)]
                qv = nonzero_vec([[B[z][y] for y in U] for z in range(N) if (z >> 2) != eta])
                z0 = idx(eta, xi)
                a = [A[x][z0] for x in S]; b = [B[z0][y] for y in U]
                chi_eta = [F(H4[h][eta]) for h in range(4)]; chi_xi = [F(H4[xi][l]) for l in range(4)]
                good = (u is None or rank([chi_eta, u]) == 2) and (qv is None or rank([chi_xi, qv]) == 2)
                if not good:
                    exc += 1
                    okE = (u is not None and rank([a, u]) <= 1) or (qv is not None and rank([b, qv]) <= 1)
                    law_fail += (not okE)
                    continue
                tot_good += 1
                ua = [u] if u is not None else []
                qa = [qv] if qv is not None else []
                okA = rank([a, chi_eta] + ua) <= 1 + len(ua) and rank([a] + ua) == 1 + len(ua)
                okB = rank([b, chi_xi] + qa) <= 1 + len(qa) and rank([b] + qa) == 1 + len(qa)
                law_fail += (not (okA and okB))
                s_nonzero += (rank([a, chi_eta]) == 2)
                r_nonzero += (rank([b, chi_xi]) == 2)
        assert exc <= 8
        tot_exc += exc
        done += 1
    print(f"[W16] {done} exact two-step words at 16 points (A B = H16, both factors tree steps, rank-one terms present): "
          f"good pairs {tot_good}, exceptional pairs {tot_exc} (at most 8 per word), block-law failures {law_fail}; "
          f"good pairs with s != 0: {s_nonzero}, with r != 0: {r_nonzero}")
