#!/usr/bin/env python3
"""nu.py: the number nu(S,U) of "undecided directions" of a pair of sets.

nu(S,U) = number of eigenvalues of E/N strictly between 0 and 1, E = H[S,U] H[S,U]^T  (integers)
        = rank( E (N I - E) )           (E is symmetric, hence diagonalisable)
        = rank H[S,U] + rank H[S,U^c] - |S|.
Lemma A of g-6.md: if the N-point transform is a product of two tree steps then nu(S,U) <= 4 for EVERY node S of the first
tree (as a set of outputs) and EVERY node U of the second (as a set of inputs).  nu = 0 is the equality case of tight.py.

Census: floating-point rank of an integer matrix (numpy), then every pair with nu <= 4 recomputed exactly (fraction-free
elimination on Python integers).  So "nu <= 4" lines are exact; the counts of larger nu are floats.

usage: nu.py census16 | probe32 <seed>
"""
import sys, random, itertools
import numpy as np

def Hmat(k):
    N = 1 << k
    return np.array([[1 - 2 * (bin(x & y).count("1") & 1) for y in range(N)] for x in range(N)], dtype=np.int64)

def exact_rank(M):
    M = [[int(v) for v in row] for row in M]
    n, m = len(M), len(M[0]) if M else 0
    r = 0
    prev = 1
    for c in range(m):
        piv = next((i for i in range(r, n) if M[i][c] != 0), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        for i in range(r + 1, n):
            for j in range(c + 1, m):
                M[i][j] = (M[i][j] * M[r][c] - M[i][c] * M[r][j]) // prev
            M[i][c] = 0
        prev = M[r][c]
        r += 1
        if r == n:
            break
    return r

def nu_exact(H, S, U):
    N = H.shape[0]
    M = H[np.ix_(S, U)]
    E = M @ M.T
    F = E @ (N * np.eye(len(S), dtype=np.int64) - E)
    return exact_rank(F.tolist())

def nu_float(H, S, U):
    N = H.shape[0]
    M = H[np.ix_(S, U)].astype(float)
    E = M @ M.T
    w = np.linalg.eigvalsh(E) / N
    return int(np.sum((w > 1e-9) & (w < 1 - 1e-9)))

def stab(N, S):
    Ss = set(S)
    return [d for d in range(N) if all((x ^ d) in Ss for x in S)]

def perp(N, W):
    return [y for y in range(N) if all(bin(y & d).count("1") % 2 == 0 for d in W)]

def census16():
    k, N = 4, 16
    H = Hmat(k)
    # affine orbit representatives of the 8-subsets of 16 points
    gens = []
    for i in range(k):
        gens.append([x ^ (1 << i) for x in range(N)])
        for j in range(k):
            if i != j:
                gens.append([x ^ (((x >> j) & 1) << i) for x in range(N)])
    seen = set()
    reps = []
    for S in itertools.combinations(range(N), 8):
        if S in seen:
            continue
        reps.append(S)
        stack = [S]
        seen.add(S)
        while stack:
            T = stack.pop()
            for g in gens:
                V = tuple(sorted(g[x] for x in T))
                if V not in seen:
                    seen.add(V)
                    stack.append(V)
    print(f"16 points: {len(reps)} affine classes of 8-point sets S; U runs over all 12870 8-point sets")
    Us = list(itertools.combinations(range(N), 8))
    Ubits = np.zeros((len(Us), N), dtype=np.int64)
    for i, U in enumerate(Us):
        Ubits[i, list(U)] = 1
    total = {}
    for S in reps:
        HS = H[list(S), :]
        E = np.einsum("ay,uy,by->uab", HS, Ubits, HS).astype(float)
        w = np.linalg.eigvalsh(E) / N
        nus = np.sum((w > 1e-9) & (w < 1 - 1e-9), axis=1)
        hist = {}
        for v in nus:
            hist[int(v)] = hist.get(int(v), 0) + 1
        W = stab(N, S)
        low = [i for i in range(len(Us)) if nus[i] <= 4]
        ok = all(nu_exact(H, list(S), list(Us[i])) == nus[i] for i in low)
        ex = next((Us[i] for i in low if 0 < nus[i] <= 2), None)
        print(f"  S={S} |Stab|={len(W)}  nu histogram {dict(sorted(hist.items()))}  exact recheck of nu<=4: {ok}"
              + (f"  e.g. nu={nu_exact(H, list(S), list(ex))} at U={ex}" if ex else ""))
        for v, c in hist.items():
            total[v] = total.get(v, 0) + c
    print("  all classes together:", dict(sorted(total.items())))

def probe32(seed):
    k, N = 5, 32
    H = Hmat(k)
    rnd = random.Random(seed)
    bit = lambda x, i: (x >> i) & 1
    def show(name, S, U):
        print(f"  {name}: |S|={len(S)} |U|={len(U)} |Stab S|={len(stab(N, S))} |Stab U|={len(stab(N, U))} nu={nu_exact(H, S, U)}")
    print("32 points, named pairs (exact):")
    S = [x for x in range(N) if bit(x, 0) == 0]
    U = [y for y in range(N) if bit(y, 1) == 0]
    show("hyperplanes a.b = 0 (tight)", S, U)
    U = [y for y in range(N) if bit(y, 0) == 0]
    show("hyperplanes a.b = 1", S, U)
    S = [x for x in range(N) if (bit(x, 0) & bit(x, 1)) ^ bit(x, 2) == 0]
    U = [y for y in range(N) if (bit(y, 1) & bit(y, 3)) ^ bit(y, 4) == 0]
    show("quadric x0x1+x2 / quadric y1y3+y4", S, U)
    U = [y for y in range(N) if (bit(y, 0) & bit(y, 1)) ^ bit(y, 2) == 0]
    show("quadric x0x1+x2 / same quadric", S, U)
    S = [x for x in range(N) if (bit(x, 0) & bit(x, 1)) ^ (bit(x, 2) & bit(x, 3)) == 0]
    U = [y for y in range(N) if (bit(y, 0) & bit(y, 1)) ^ (bit(y, 2) & bit(y, 3)) == 0]
    show("quadric x0x1+x2x3 (20 points) / same", S, U)
    S = [x for x in range(N) if (bit(x, 0) & bit(x, 1)) ^ (bit(x, 2) & bit(x, 3)) ^ bit(x, 4) == 0]
    U = [y for y in range(N) if (bit(y, 0) & bit(y, 1)) ^ (bit(y, 2) & bit(y, 3)) ^ bit(y, 4) == 0]
    show("quadric x0x1+x2x3+x4 / same", S, U)
    U = [y for y in range(N) if (bit(y, 0) & bit(y, 2)) ^ (bit(y, 1) & bit(y, 3)) ^ bit(y, 4) == 0]
    show("quadric x0x1+x2x3+x4 / y0y2+y1y3+y4", S, U)
    U = [y for y in range(N) if bit(y, 4) == 0]
    show("quadric x0x1+x2x3+x4 / hyperplane y4", S, U)
    S = [x for x in range(N) if bin(x).count("1") <= 2]
    U = [y for y in range(N) if bin(y).count("1") <= 2]
    show("Hamming ball radius 2 / same", S, U)
    U = [y for y in range(N) if bin(y).count("1") % 2 == 0]
    show("Hamming ball radius 2 / even weight", S, U)
    S = [x for x in range(N) if bin(x).count("1") % 4 in (0, 1)]
    U = [y for y in range(N) if bin(y).count("1") % 4 in (0, 1)]
    show("weight mod 4 in {0,1} / same", S, U)
    U = [y for y in range(N) if bin(y).count("1") % 4 in (0, 3)]
    show("weight mod 4 in {0,1} / in {0,3}", S, U)
    # random pairs
    hist = {}
    for _ in range(300):
        S = rnd.sample(range(N), 16)
        U = rnd.sample(range(N), 16)
        v = nu_float(H, S, U)
        hist[v] = hist.get(v, 0) + 1
    print("  300 random pairs of 16-point sets, nu histogram (floats):", dict(sorted(hist.items())))
    # descent: 16-point sets, swap moves, minimise (nu, then sum of sin^2 cos^2); S kept away from sets with a stabiliser
    def score(S, U):
        M = H[np.ix_(S, U)].astype(float)
        w = np.linalg.eigvalsh(M @ M.T) / N
        mid = (w > 1e-9) & (w < 1 - 1e-9)
        return int(mid.sum()), float(np.sum(w[mid] * (1 - w[mid])))
    print("  descent from random starts (floats; final pair rechecked exactly):")
    for rs in range(6):
        S = rnd.sample(range(N), 16)
        U = rnd.sample(range(N), 16)
        cur = score(S, U)
        for it in range(4000):
            S2, U2 = list(S), list(U)
            if rnd.random() < 0.5:
                o = rnd.choice([x for x in range(N) if x not in S2])
                S2[rnd.randrange(16)] = o
            else:
                o = rnd.choice([x for x in range(N) if x not in U2])
                U2[rnd.randrange(16)] = o
            sc = score(S2, U2)
            if sc <= cur:
                S, U, cur = S2, U2, sc
            if cur[0] == 0:
                break
        S.sort(); U.sort()
        print(f"    start {rs}: nu={nu_exact(H, S, U)} |Stab S|={len(stab(N, S))} |Stab U|={len(stab(N, U))} S={S} U={U}")

if __name__ == "__main__":
    if sys.argv[1] == "census16":
        census16()
    else:
        probe32(int(sys.argv[2]))
