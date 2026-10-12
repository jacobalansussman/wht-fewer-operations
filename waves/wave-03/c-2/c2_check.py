#!/usr/bin/env python3
"""c2_check.py  (skeptic c-2, own code; nothing imported from g-6-twosteps)

Part T  Theorem 1 of g-6:  rank H[S,U] = |S||U|/N  <=>  U is a union of cosets of Stab(S)^perp.
        Method (different from g-6's E(E-N)=0 test):
          * rank over Q >= rank modulo p for every prime p (a minor that is non-zero modulo p is non-zero).
            So "rank mod p > |S||U|/N" PROVES strict inequality over Q.
          * every pair that the predicate calls an equality case, and every pair where the mod-p rank does not
            exceed the bound, is settled by an exact fraction-free (Bareiss) integer rank.
        Sizes: 8 points all pairs; 16 points one S per affine class x all U; 32 and 64 points structured samples.
Part N  the two-projection identities behind Lemma A (exact integer ranks).
Part A  Lemma A's rank inequality on random tree steps over the field F_p (the proof is field-free).
Part E  the exception count for a tree on 8 leaves (own search).
"""
import sys, random, itertools
import numpy as np

P = 1000003
rnd = random.Random(20261011)

def par(v):
    return bin(v).count("1") & 1

def Hmat(k):
    N = 1 << k
    return np.array([[1 - 2 * par(x & y) for y in range(N)] for x in range(N)], dtype=np.int64)

def bareiss_rank(M):
    M = [[int(v) for v in r] for r in M]
    if not M:
        return 0
    nr, nc = len(M), len(M[0])
    r = 0
    prev = 1
    for c in range(nc):
        piv = next((i for i in range(r, nr) if M[i][c] != 0), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        for i in range(r + 1, nr):
            for j in range(c + 1, nc):
                M[i][j] = (M[i][j] * M[r][c] - M[i][c] * M[r][j]) // prev
            M[i][c] = 0
        prev = M[r][c]
        r += 1
        if r == nr:
            break
    return r

def batch_rank_mod(M, p=P):
    """M: (B, r, c) int64.  Rank of each matrix modulo p."""
    M = M % p
    B, r, c = M.shape
    row = np.zeros(B, dtype=np.int64)
    ar = np.arange(r)[None, :]
    idx = np.arange(B)
    for col in range(c):
        colv = M[:, :, col]
        mask = (colv != 0) & (ar >= row[:, None])
        has = mask.any(axis=1)
        if not has.any():
            continue
        b = idx[has]
        pr = mask.argmax(axis=1)[has]
        rr = row[has]
        tmp = M[b, pr, :].copy()
        M[b, pr, :] = M[b, rr, :]
        M[b, rr, :] = tmp
        pivrow = M[b, rr, :]                       # (nb, c)
        pivval = pivrow[:, col]                    # (nb,)
        factor = M[b, :, col].copy()               # (nb, r)
        factor[ar <= rr[:, None]] = 0
        sub = M[b]
        scale = np.where(ar <= rr[:, None], 1, pivval[:, None])
        sub = (scale[:, :, None] * sub - factor[:, :, None] * pivrow[:, None, :]) % p
        M[b] = sub
        row[has] += 1
    return row

def stab(S, N):
    Ss = set(S)
    return [d for d in range(N) if all((x ^ d) in Ss for x in Ss)]

def perp(W, N):
    return [y for y in range(N) if all(par(y & d) == 0 for d in W)]

def predicate(S, U, N):
    if len(U) in (0, N) or len(S) in (0, N):
        return None
    Wp = perp(stab(S, N), N)
    Us = set(U)
    return all((y ^ d) in Us for y in Us for d in Wp)

# ---------------------------------------------------------------- Part T, exhaustive at 8 and 16
def part_T_exhaustive(k):
    N = 1 << k
    H = Hmat(k)
    nm = 1 << N
    masks = np.arange(nm, dtype=np.int64)
    bits = ((masks[:, None] >> np.arange(N)[None, :]) & 1).astype(np.int64)
    popc = bits.sum(axis=1)
    # shift permutations on masks
    def shift_mask(d):
        out = np.zeros(nm, dtype=np.int64)
        for y in range(N):
            out |= ((masks >> y) & 1) << (y ^ d)
        return out
    SH = {d: shift_mask(d) for d in range(1, N)}
    if k == 3:
        reps = list(range(1, nm - 1))
    else:
        gens = []
        for i in range(k):
            gens.append([x ^ (1 << i) for x in range(N)])
            for j in range(k):
                if i != j:
                    gens.append([x ^ (((x >> j) & 1) << i) for x in range(N)])
        gm = []
        for g in gens:
            out = np.zeros(nm, dtype=np.int64)
            for x in range(N):
                out |= ((masks >> x) & 1) << g[x]
            gm.append(out.tolist())
        seen = bytearray(nm)
        reps = []
        for S0 in range(1, nm - 1):
            if seen[S0]:
                continue
            reps.append(S0)
            seen[S0] = 1
            st = [S0]
            while st:
                S = st.pop()
                for g in gm:
                    T = g[S]
                    if not seen[T]:
                        seen[T] = 1
                        st.append(T)
    pairs = 0; n_eq = 0; n_pred = 0; bad = 0; exact_used = 0
    for S in reps:
        Sl = [x for x in range(N) if (S >> x) & 1]
        s = len(Sl)
        W = stab(Sl, N)
        Wp = perp(W, N)
        per = np.ones(nm, dtype=bool)
        for d in Wp:
            if d:
                per &= (SH[d] == masks)
        per[0] = False; per[-1] = False
        HS = H[Sl, :]
        rk = np.zeros(nm, dtype=np.int64)
        CH = 8192
        for a in range(0, nm, CH):
            blk = HS[None, :, :] * bits[a:a + CH, None, :]
            rk[a:a + CH] = batch_rank_mod(blk)
        # bound: s*|U|/N ; strict if rk*N > s*|U|
        strict = rk * N > s * popc
        strict[0] = True; strict[-1] = True     # trivial U excluded from the comparison
        # cases needing an exact rank: predicted equality, or not proved strict
        todo = np.nonzero(per | ~strict)[0]
        eq = np.zeros(nm, dtype=bool)
        for U in todo:
            U = int(U)
            if U in (0, nm - 1):
                continue
            Ul = [y for y in range(N) if (U >> y) & 1]
            r = bareiss_rank(HS[:, Ul].tolist())
            exact_used += 1
            assert r * N >= s * len(Ul)
            if r * N == s * len(Ul):
                eq[U] = True
        pairs += nm - 2
        n_eq += int(eq.sum()); n_pred += int(per.sum())
        bad += int((eq != per).sum())
    print(f"[T] N={N}: {len(reps)} sets S, {pairs} pairs; equality cases (exact rank) {n_eq}; predicted {n_pred}; "
          f"disagreements {bad}; exact ranks computed {exact_used}", flush=True)

# ---------------------------------------------------------------- Part T, samples at 32 and 64
def rand_subgroup(k, dim):
    N = 1 << k
    basis = []
    span = {0}
    while len(basis) < dim:
        v = rnd.randrange(1, N)
        if v not in span:
            basis.append(v)
            span |= {s ^ v for s in span}
    return sorted(span)

def union_of_cosets(W, N, howmany):
    reps = []
    seen = set()
    for x in range(N):
        if x not in seen:
            reps.append(x)
            seen |= {x ^ w for w in W}
    pick = rnd.sample(reps, howmany)
    out = set()
    for x in pick:
        out |= {x ^ w for w in W}
    return sorted(out)

def part_T_sample(k, trials):
    N = 1 << k
    H = Hmat(k)
    cases = []
    for t in range(trials):
        mode = rnd.randrange(4)
        if mode == 0:
            S = sorted(rnd.sample(range(N), rnd.randrange(1, N)))
        else:
            W = rand_subgroup(k, rnd.randrange(1, k))
            nc = N // len(W)
            S = union_of_cosets(W, N, rnd.randrange(1, nc + 1) if nc > 1 else 1)
        if len(S) == N:
            continue
        Wp = perp(stab(S, N), N)
        um = rnd.randrange(5)
        if um == 0 or um == 1:
            ncw = N // len(Wp)
            if ncw < 2:
                U = sorted(rnd.sample(range(N), rnd.randrange(1, N)))
            else:
                U = union_of_cosets(Wp, N, rnd.randrange(1, ncw))
                if um == 1:                       # toggle one point: should break equality
                    y = rnd.randrange(N)
                    Us = set(U); Us ^= {y}; U = sorted(Us)
        elif um == 2:
            V = rand_subgroup(k, rnd.randrange(1, k))
            U = union_of_cosets(V, N, rnd.randrange(1, N // len(V)))
        elif um == 3:
            U = sorted(rnd.sample(range(N), rnd.randrange(1, N)))
        else:                                     # a sub-union of a bigger period: periodic under less than needed
            V = rand_subgroup(k, max(1, k - 2))
            U = union_of_cosets(V, N, rnd.randrange(1, N // len(V)))
        if len(U) in (0, N):
            continue
        cases.append((S, U))
    n_eq = n_pred = bad = 0
    for S, U in cases:
        pred = predicate(S, U, N)
        blk = np.zeros((1, len(S), len(U)), dtype=np.int64)
        blk[0] = H[np.ix_(S, U)]
        rp = int(batch_rank_mod(blk)[0])
        if rp * N > len(S) * len(U) and not pred:
            eq = False
        else:
            r = bareiss_rank(H[np.ix_(S, U)].tolist())
            eq = (r * N == len(S) * len(U))
        n_eq += eq; n_pred += bool(pred); bad += (eq != bool(pred))
    print(f"[T] N={N}: {len(cases)} sampled pairs; equality cases {n_eq}; predicted {n_pred}; disagreements {bad}", flush=True)

# ---------------------------------------------------------------- Part N: nu identities
def part_N(k, trials):
    N = 1 << k
    H = Hmat(k)
    bad = 0
    hist = {}
    for t in range(trials):
        S = sorted(rnd.sample(range(N), rnd.randrange(1, N)))
        U = sorted(rnd.sample(range(N), rnd.randrange(1, N)))
        if t % 3 == 0:
            W = rand_subgroup(k, rnd.randrange(1, k)); S = union_of_cosets(W, N, 1)
            U = union_of_cosets(perp(W, N), N, 1) if t % 2 else U
        Sc = [x for x in range(N) if x not in S]; Uc = [y for y in range(N) if y not in U]
        r = lambda a, b: bareiss_rank(H[np.ix_(a, b)].tolist()) if a and b else 0
        r11, r10, r01, r00 = r(S, U), r(S, Uc), r(Sc, U), r(Sc, Uc)
        M = H[np.ix_(S, U)]
        E = M @ M.T
        nu = bareiss_rank((E @ (N * np.eye(len(S), dtype=np.int64) - E)).tolist())
        ok = (nu == r11 + r10 - len(S)) and (r11 + r10 + r01 + r00 == N + 2 * nu)
        bad += (not ok)
        hist[nu] = hist.get(nu, 0) + 1
    print(f"[N] N={N}: {trials} pairs, identities nu = r(S,U)+r(S,U^c)-|S| and sum of four ranks = N+2nu: failures {bad}; "
          f"nu histogram {sorted(hist.items())}", flush=True)

# ---------------------------------------------------------------- Part A: Lemma A on random tree steps over F_p
def random_tree(items):
    """returns list of nodes (frozensets) of a random binary tree on items, and the parent map via nested tuples"""
    items = list(items)
    rnd.shuffle(items)
    nodes = []
    def build(lst):
        nodes.append(frozenset(lst))
        if len(lst) == 1:
            return ("leaf", lst[0])
        cut = rnd.randrange(1, len(lst))
        return ("node", frozenset(lst), build(lst[:cut]), build(lst[cut:]))
    t = build(items)
    return t, nodes

def tree_step(N, t):
    """A[i][j] = a_i * F(lowest common node, side of i) * b_j off the diagonal, random diagonal; entries in F_p."""
    a = [rnd.randrange(1, P) for _ in range(N)]
    b = [rnd.randrange(1, P) for _ in range(N)]
    A = [[0] * N for _ in range(N)]
    def leaves(t):
        return [t[1]] if t[0] == "leaf" else list(t[1])
    def rec(t):
        if t[0] == "leaf":
            A[t[1]][t[1]] = rnd.randrange(1, P)
            return
        L, R = leaves(t[2]), leaves(t[3])
        fL = rnd.randrange(1, P); fR = rnd.randrange(1, P)
        for i in L:
            for j in R:
                A[i][j] = a[i] * fL % P * b[j] % P
        for i in R:
            for j in L:
                A[i][j] = a[i] * fR % P * b[j] % P
        rec(t[2]); rec(t[3])
    rec(t)
    return A

def part_A(k, trials):
    N = 1 << k
    tested = attained = viol = 0
    for _ in range(trials):
        t1, n1 = random_tree(range(N)); t2, n2 = random_tree(range(N))
        A = np.array(tree_step(N, t1), dtype=object); B = np.array(tree_step(N, t2), dtype=object)
        perm = list(range(N)); rnd.shuffle(perm)        # middle wire z of A is row perm[z] of B
        Bp = B[perm, :]
        M = (A.dot(Bp)) % P
        M = np.array(M.tolist(), dtype=np.int64)
        for S in n1:
            if not 1 < len(S) < N:
                continue
            Sp = {perm[z] for z in S}
            for U in n2:
                if not 1 < len(U) < N:
                    continue
                blk = M[np.ix_(sorted(S), sorted(U))][None, :, :].copy()
                r = int(batch_rank_mod(blk)[0])
                bound = len(Sp & U) + 2
                tested += 1; attained += (r == bound); viol += (r > bound)
    print(f"[A] N={N}: {trials} random pairs of tree steps over F_p, {tested} pairs of nodes; "
          f"rank <= |S' meet U'| + 2 violated {viol} times, attained {attained} times", flush=True)

# ---------------------------------------------------------------- Part E: exceptions for a tree on w leaves (w = 8)
def part_E(kw, emax):
    w = 1 << kw
    FULL = (1 << w) - 1
    pts = lambda m: [x for x in range(w) if (m >> x) & 1]
    def perp_dirs(R):
        p = pts(R)
        return [e for e in range(w) if all(par(e & (q ^ p[0])) == 0 for q in p)]
    PERP = {}
    def rule(R, Rp, X):
        good = [e for e in range(w) if not ((Rp | X) >> e) & 1]
        if len(good) <= 1:
            return True
        if R not in PERP:
            PERP[R] = set(perp_dirs(R))
        pd = PERP[R]
        return all((e ^ good[0]) in pd for e in good)
    def submasks_of_size(m, n):
        p = pts(m)
        for c in itertools.combinations(p, n):
            yield sum(1 << v for v in c)
    for e in range(0, emax + 1):
        found = None
        nX = 0
        for Xs in itertools.combinations(range(w), e):
            X = sum(1 << v for v in Xs)
            nX += 1
            memo = {}
            def feas(R, Rp):
                key = (R, Rp)
                if key in memo:
                    return memo[key]
                res = None
                if rule(R, Rp, X):
                    p = pts(R)
                    if len(p) == 1:
                        res = f"{p[0]}>{pts(Rp)[0]}"
                    else:
                        first = p[0]; rest = p[1:]
                        done = False
                        for n1 in range(0, len(rest)):
                            for extra in itertools.combinations(rest, n1):
                                R1 = (1 << first) | sum(1 << v for v in extra)
                                R2 = R ^ R1
                                for R1p in submasks_of_size(Rp, n1 + 1):
                                    x = feas(R1, R1p)
                                    if x is None:
                                        continue
                                    y = feas(R2, Rp ^ R1p)
                                    if y is not None:
                                        res = f"({x} {y})"; done = True; break
                                if done: break
                            if done: break
                memo[key] = res
                return res
            r = feas(FULL, FULL)
            if r is not None:
                found = (Xs, r); break
        if found:
            print(f"[E] w={w}: {e} exceptional columns SUFFICE for the rule: X={found[0]} tree {found[1]}", flush=True)
            break
        else:
            print(f"[E] w={w}: no tree, no matching with {e} exceptional columns ({nX} sets X tried)", flush=True)

if __name__ == "__main__":
    what = sys.argv[1]
    if what == "T3": part_T_exhaustive(3)
    if what == "T4": part_T_exhaustive(4)
    if what == "T5": part_T_sample(5, int(sys.argv[2]))
    if what == "T6": part_T_sample(6, int(sys.argv[2]))
    if what == "N": part_N(4, 300); part_N(5, 120)
    if what == "A": part_A(4, 8); part_A(5, 3)
    if what == "E": part_E(3, 3)
