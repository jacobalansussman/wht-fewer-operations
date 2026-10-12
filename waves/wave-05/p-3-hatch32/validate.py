#!/usr/bin/env python3
"""validate.py (p-3-hatch32): test the cell rule of p-3.md section 2 on REAL two-step words at 16 points (exact fractions).

For a word H = A.B and a subgroup W whose cosets are blocks of the first step and whose perpendicular's cosets are blocks
of the second (hypothesis (P)), with ANY meeting pattern of the blocks (no hypothesis (G)), it computes
  u_xi  = the one column direction of A[block xi, wires outside the block]   (None if that part is zero),
  q_eta = the one row direction of B[wires outside block eta, block eta]     (None if zero),
  the cells (xi, eta) = wires common to the two blocks, and which cells are exceptional (u_xi ~ chi_eta or q_eta ~ chi_xi),
and checks
  C1  an empty cell is exceptional;
  C2  in a non-exceptional cell, chi_eta lies in the span of the cell's columns of A (inside the block) and u_xi;
  C3  at most one cell with u_xi ~ chi_eta per xi, at most one with q_eta ~ chi_xi per eta;
  C5  the identity used for 16 x 2 (p-3.md section 4): combinations of the columns of H in block eta that kill q_eta lie in
      the span of the columns of A at the wires of block eta;
  C4  for EVERY pair (R, R') inside a block with rank A[R, wires outside R'] <= 1 (not only the nodes of one tree):
      the non-exceptional cells with no wire in R' have characters pairwise proportional on R, proportional to u_xi|R
      when that is not zero, and   w <= w / 2^rho(R) + (exceptional cells of the block) + |R|.
"""
import sys, itertools
from fractions import Fraction as Fr

def mul(A, B): return [[sum(a * b for a, b in zip(r, c)) for c in zip(*B)] for r in A]
def sub(M, rows, cols): return [[M[i][j] for j in cols] for i in rows]
def prop(u, v):
    """u, v proportional (either may be zero -> True)"""
    return all(u[i] * v[j] == u[j] * v[i] for i in range(len(u)) for j in range(i + 1, len(u)))
def rank_le1(M):
    rows = [r for r in M if any(r)]
    return all(prop(rows[0], r) for r in rows[1:]) if rows else True
def first_dir(M):
    for r in M:
        if any(r): return list(r)
    return None
def rank(M):
    M = [list(map(Fr, r)) for r in M]; rk = 0
    ncol = len(M[0]) if M else 0
    for c in range(ncol):
        piv = next((i for i in range(rk, len(M)) if M[i][c] != 0), None)
        if piv is None: continue
        M[rk], M[piv] = M[piv], M[rk]
        for i in range(len(M)):
            if i != rk and M[i][c] != 0:
                f = M[i][c] / M[rk][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[rk])]
        rk += 1
    return rk
def inv(M):
    n = len(M); A = [list(map(Fr, r)) + [Fr(int(i == j)) for j in range(n)] for i, r in enumerate(M)]
    for c in range(n):
        piv = next(i for i in range(c, n) if A[i][c] != 0)
        A[c], A[piv] = A[piv], A[c]
        d = A[c][c]; A[c] = [a / d for a in A[c]]
        for i in range(n):
            if i != c and A[i][c] != 0:
                f = A[i][c]; A[i] = [a - f * b for a, b in zip(A[i], A[c])]
    return [r[n:] for r in A]
def dot(a, b): return bin(a & b).count("1") & 1
def affdim(R):
    R = list(R); basis = []
    for p in R[1:]:
        v = p ^ R[0]
        for b in basis: v = min(v, v ^ b)
        if v: basis.append(v)
    return len(basis)

def check(name, A, B, n, W, Sp_of, Up_of):
    N = 1 << n
    H = [[Fr(-1 if dot(x, y) else 1) for y in range(N)] for x in range(N)]
    assert mul(A, B) == H, "A.B is not the transform"
    Wp = [y for y in range(N) if all(dot(y, d) == 0 for d in W)]
    w, c = len(W), len(Wp)
    Scos = sorted(set(tuple(sorted(x ^ d for d in W)) for x in range(N)))
    Ucos = sorted(set(tuple(sorted(y ^ d for d in Wp)) for y in range(N)))
    Z = list(range(N))
    info = []
    Sp = [sorted(Sp_of(S)) for S in Scos]; Up = [sorted(Up_of(U)) for U in Ucos]
    assert sorted(sum(Sp, [])) == Z and sorted(sum(Up, [])) == Z, "wire sets are not partitions"
    us, qs = [], []
    for S, S1 in zip(Scos, Sp):
        out = [z for z in Z if z not in S1]
        M = sub(A, S, out); assert rank_le1(M), "block of A is not a node"
        us.append(first_dir(list(zip(*M))))
    for U, U1 in zip(Ucos, Up):
        out = [z for z in Z if z not in U1]
        M = sub(B, out, U); assert rank_le1(M), "block of B is not a node"
        qs.append(first_dir(M))
    pattern = [[len(set(S1) & set(U1)) for U1 in Up] for S1 in Sp]
    exc = [[False] * len(Ucos) for _ in Scos]; kind = [[""] * len(Ucos) for _ in Scos]
    for i, S in enumerate(Scos):
        for j, U in enumerate(Ucos):
            chi_eta = [H[x][U[0]] for x in S]; chi_xi = [H[S[0]][y] for y in U]
            e1 = us[i] is not None and prop(us[i], chi_eta)
            e2 = qs[j] is not None and prop(qs[j], chi_xi)
            exc[i][j] = e1 or e2; kind[i][j] = ("u" if e1 else "") + ("q" if e2 else "")
    c1 = all(exc[i][j] or pattern[i][j] > 0 for i in range(len(Scos)) for j in range(len(Ucos)))
    c2 = True
    for i, S in enumerate(Scos):
        for j, U in enumerate(Ucos):
            if exc[i][j]: continue
            wires = sorted(set(Sp[i]) & set(Up[j]))
            cols = [[A[x][z] for x in S] for z in wires] + ([us[i]] if us[i] is not None else [])
            chi_eta = [H[x][U[0]] for x in S]
            if rank(cols + [chi_eta]) != rank(cols): c2 = False
    c3 = all(sum('u' in kind[i][j] for j in range(len(Ucos))) <= 1 for i in range(len(Scos))) and \
         all(sum('q' in kind[i][j] for i in range(len(Scos))) <= 1 for j in range(len(Ucos)))
    # C5: for every eta with q_eta defined and every t orthogonal to q_eta, the combination sum_gamma t(gamma) H[., (eta, gamma)]
    #     (a combination of the coset characters chi_eta on the blocks xi, with weights the transform of t) lies in the span
    #     of the columns of A at the wires of block eta.  For c = 2 and q_eta ~ chi_f: the coset character on block f+1 itself.
    c5 = True; c5n = 0
    for j, U in enumerate(Ucos):
        if qs[j] is None: continue
        q = qs[j]; cols = [[A[x][z] for x in range(N)] for z in Up[j]]
        rk = rank(cols)
        piv = next(i for i in range(len(q)) if q[i] != 0)
        for i in range(len(q)):
            if i == piv: continue
            t = [Fr(0)] * len(q); t[i] = q[piv]; t[piv] = -q[i]          # t . q = 0
            v = [sum(t[g] * H[x][U[g]] for g in range(len(U))) for x in range(N)]
            c5n += 1
            if rank(cols + [v]) != rk: c5 = False
    print(f"   C5 ({c5n} combinations): {c5}", flush=True)
    tests = fails = tight = 0
    for i, S in enumerate(Scos):
        nexc = sum(exc[i])
        for s in range(2, w):
            for R in itertools.combinations(S, s):
                for R1 in itertools.combinations(Sp[i], s):
                    out = [z for z in Z if z not in R1]
                    if not rank_le1(sub(A, R, out)): continue
                    tests += 1
                    G = [j for j in range(len(Ucos)) if not exc[i][j] and not (set(Up[j]) & set(R1))]
                    chis = [[H[x][Ucos[j][0]] for x in R] for j in G]
                    ok = all(prop(chis[0], v) for v in chis[1:]) if chis else True
                    if us[i] is not None:
                        uR = [us[i][S.index(x)] for x in R]
                        if any(uR): ok = ok and all(prop(uR, v) for v in chis)
                    # refined form (kind u never helps): constrained cells <= w/2^rho - [u is a character],
                    # hence w <= w/2^rho + (kind-q cells) + |R|
                    hasu = any('u' in kind[i][j] for j in range(len(Ucos)))
                    nq = sum('q' in kind[i][j] for j in range(len(Ucos)))
                    ok = ok and len(G) <= w // (1 << affdim(R)) - (1 if hasu else 0)
                    bound = w // (1 << affdim(R)) + nq + s
                    ok = ok and w <= bound
                    tight += (w == bound)
                    fails += (not ok)
    print(f"{name}: shape {w} x {c}; wires per cell {pattern}; exceptional cells per block {[sum(r) for r in exc]} "
          f"kinds {sorted(set(k for r in kind for k in r if k))}; u defined {[x is not None for x in us]}; "
          f"C1 {c1}  C2 {c2}  C3 {c3};  C4: {tests} pairs (R, R') with the rank property, {fails} violations, {tight} with equality", flush=True)

H4 = [[Fr(-1 if dot(a, b) else 1) for b in range(4)] for a in range(4)]
I4 = [[Fr(int(a == b)) for b in range(4)] for a in range(4)]
def kron(P, Q): return [[P[a][b] * Q[c][d] for b in range(len(P)) for d in range(len(Q))] for a in range(len(P)) for c in range(len(Q))]

if __name__ == "__main__":
    # index = 4 * (high pair) + (low pair);  A = H4 (x) I acts on the high pair, B = I (x) H4 on the low pair
    A = kron(H4, I4); B = kron(I4, H4)
    W4 = [0, 4, 8, 12]                      # the high pair varies: blocks of A
    check("brick word, read as 4 x 4", A, B, 4, W4,
          lambda S: [z for z in range(16) if z % 4 == S[0] % 4], lambda U: [z for z in range(16) if z // 4 == U[0] // 4])
    # read as 8 x 2: W8 = high pair anything, low pair in {0, t}, t = 3 (t.t = 0, so the perpendicular is {0, 3} in the low pair)
    W8 = [4 * a + b for a in range(4) for b in (0, 3)]
    def Sp8(S): return [z for z in range(16) if (z % 4) in set(x % 4 for x in S)]
    def Up8(U):                            # the two wires z = (y1, z2) whose row of H4 is NOT constant on the block's low pairs
        y1 = U[0] // 4; lows = [y % 4 for y in U]
        k = 0 if lows[0] in (0, 3) else 1  # two blocks per y1: give one the wires with z2.3 = 0, the other z2.3 = 1
        return [4 * y1 + z2 for z2 in range(4) if dot(z2, 3) == k]
    try:
        check("brick word, read as 8 x 2 (blocks meet in 0 or 2 wires)", A, B, 4, W8, Sp8, Up8)
    except AssertionError as ex:
        print("brick 8 x 2 with k as chosen:", ex, "-> trying the other assignment", flush=True)
        def Up8b(U):
            y1 = U[0] // 4; lows = [y % 4 for y in U]
            k = 1 if lows[0] in (0, 3) else 0
            return [4 * y1 + z2 for z2 in range(4) if dot(z2, 3) == k]
        check("brick word, read as 8 x 2 (blocks meet in 0 or 2 wires)", A, B, 4, W8, Sp8, Up8b)
    # a word whose blocks talk: A_c = A + c p r^T with p = eps (x) pi, r = delta (x) rho, eps = (1,-1,-1,-1), delta = (-1,1,1,1)
    eps = [1, -1, -1, -1]; dl = [-1, 1, 1, 1]
    for c, pi, rho in ((Fr(1, 3), [1, 2, 3, 5], [1, 0, 0, 0]), (Fr(-2, 7), [1, 1, 1, 1], [2, 1, -1, 3]), (Fr(5), [0, 1, 0, 2], [1, 1, 0, 0])):
        p = [Fr(eps[a] * pi[b]) for a in range(4) for b in range(4)]
        r = [Fr(dl[a] * rho[b]) for a in range(4) for b in range(4)]
        Ac = [[A[i][j] + c * p[i] * r[j] for j in range(16)] for i in range(16)]
        Hm = [[Fr(-1 if dot(x, y) else 1) for y in range(16)] for x in range(16)]
        Bc = mul(inv(Ac), Hm)
        check(f"talking word c = {c}, pi = {pi}, rho = {rho}, read as 4 x 4", Ac, Bc, 4, W4,
              lambda S: [z for z in range(16) if z % 4 == S[0] % 4], lambda U: [z for z in range(16) if z // 4 == U[0] // 4])
    # words whose outgoing directions ARE characters (kind-u cells, the pinned coset of p-3.md section 2):
    # p = chi_e (x) pi on the high pair, r arbitrary.  The block-level hypotheses hold for any p, r (the blocks of A_c talk
    # through one rank-one term); C4 then tests whatever pairs (R, R') still have the rank property.
    for c, e, pi, r in ((Fr(1, 2), 1, [1, 2, 3, 5], [1, 2, -1, 3, 0, 1, 1, -2, 2, 0, 1, 1, -1, 3, 1, 2]),
                        (Fr(-3, 5), 3, [1, 1, 2, 1], [1] * 16),
                        (Fr(2), 2, [1, -1, 1, 3], [(-1 if dot(a, 2) else 1) * (b + 1) for a in range(4) for b in range(4)])):
        p = [Fr((-1 if dot(a, e) else 1) * pi[b]) for a in range(4) for b in range(4)]
        Ac = [[A[i][j] + c * p[i] * Fr(r[j]) for j in range(16)] for i in range(16)]
        Hm = [[Fr(-1 if dot(x, y) else 1) for y in range(16)] for x in range(16)]
        Bc = mul(inv(Ac), Hm)
        check(f"character-direction word c = {c}, u = chi_{e} (x) {pi}, read as 4 x 4", Ac, Bc, 4, W4,
              lambda S: [z for z in range(16) if z % 4 == S[0] % 4], lambda U: [z for z in range(16) if z // 4 == U[0] // 4])
