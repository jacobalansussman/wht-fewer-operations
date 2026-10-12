#!/usr/bin/env python3
"""tight.py: equality cases of the block rank bound  rank H[S,U] >= |S||U|/N.

Claim to test (g-6, Theorem 1):  rank H[S,U] = |S||U|/N   <=>   U is a union of cosets of Stab(S)^perp,
where Stab(S) = {d : S + d = S}.  (Then S is a union of cosets of W = Stab(S) and U of cosets of W^perp.)

Exact test, integers only.  With M = H[S,U] (entries +-1) and E = M M^T:  all non-zero eigenvalues of E are <= N and
their sum is |S||U|, so rank = |S||U|/N  <=>  every non-zero eigenvalue is N  <=>  E (E - N I) = 0  (E is symmetric).
k = 3: every pair (S,U).   k = 4: S over one representative of each orbit of the affine group, U over all 65,536 sets.
"""
import sys
import numpy as np

def run(k):
    N = 1 << k
    H = np.array([[1 - 2 * (bin(x & y).count("1") & 1) for y in range(N)] for x in range(N)], dtype=np.int64)
    masks = np.arange(1 << N, dtype=np.int64)
    bits = ((masks[:, None] >> np.arange(N)[None, :]) & 1).astype(np.int64)     # bits[m, y] = 1 if y in set m

    def stab(S):
        return [d for d in range(N) if all(((S >> (x ^ d)) & 1) for x in range(N) if (S >> x) & 1)]

    def perp(W):
        return [y for y in range(N) if all(bin(y & d).count("1") % 2 == 0 for d in W)]

    # orbit representatives of subsets under the affine group
    if k == 3:
        reps = list(range(1, (1 << N) - 1))           # all proper non-empty sets, no reduction
    else:
        gens = []
        for i in range(k):
            gens.append([x ^ (1 << i) for x in range(N)])                       # translation
            for j in range(k):
                if i != j:
                    gens.append([x ^ (((x >> j) & 1) << i) for x in range(N)])  # transvection
        seen = bytearray(1 << N)
        reps = []
        for S0 in range(1, (1 << N) - 1):
            if seen[S0]:
                continue
            reps.append(S0)
            stack = [S0]
            seen[S0] = 1
            while stack:
                S = stack.pop()
                for g in gens:
                    T = 0
                    for x in range(N):
                        if (S >> x) & 1:
                            T |= 1 << g[x]
                    if not seen[T]:
                        seen[T] = 1
                        stack.append(T)
    print(f"k={k} N={N}: {len(reps)} sets S to test (k=3: all; k=4: affine orbit representatives)")
    n_eq = 0
    n_pairs = 0
    bad = 0
    noncoset = 0
    examples = []
    for S in reps:
        Sl = [x for x in range(N) if (S >> x) & 1]
        HS = H[Sl, :]                                           # s x N
        E = np.einsum("ay,uy,by->uab", HS, bits, HS)            # (2^N, s, s)
        EE = np.einsum("uab,ubc->uac", E, E)
        eq = np.all(EE == N * E, axis=(1, 2))
        eq[0] = False
        eq[-1] = False                                          # U empty or everything: trivial
        W = stab(S)
        Wp = perp(W)
        # predicate: U is Wp-periodic
        per = np.ones(1 << N, dtype=bool)
        for d in Wp:
            if d == 0:
                continue
            shifted = np.zeros_like(bits)
            for y in range(N):
                shifted[:, y] = bits[:, y ^ d]
            per &= np.all(shifted == bits, axis=1)
        per[0] = False
        per[-1] = False
        n_pairs += (1 << N) - 2
        n_eq += int(eq.sum())
        bad += int((eq != per).sum())
        # equality cases where S or U is not a coset of a subgroup
        if eq.any():
            s = len(Sl)
            S_coset = (len(W) == s)
            idx = np.nonzero(eq)[0]
            for U in idx[:2000]:
                Ul = [y for y in range(N) if (int(U) >> y) & 1]
                U_coset = all((int(U) >> (Ul[0] ^ a ^ b)) & 1 for a in Ul for b in Ul)
                if not (S_coset and U_coset):
                    noncoset += 1
                    if len(examples) < 6 and 1 < len(W) < N and len(Wp) > 1:
                        examples.append((Sl, Ul, len(W)))
    print(f"  pairs tested {n_pairs}, equality cases {n_eq}, disagreements with the predicate {bad}")
    print(f"  equality cases in which S or U is not a coset (counted on at most 2000 U per S): {noncoset}")
    for Sl, Ul, w in examples:
        print(f"    example: S={Sl} U={Ul} |Stab(S)|={w} rank={len(Sl)*len(Ul)//N}")

if __name__ == "__main__":
    run(int(sys.argv[1]))
