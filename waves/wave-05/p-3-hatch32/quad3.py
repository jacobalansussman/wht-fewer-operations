#!/usr/bin/env python3
"""quad3.py (p-3-hatch32): the quadric pair one level down, splits instead of subsets.
A split S = S1 + S2 (8 + 8) of the first tree needs nu(S1, U) <= 4 AND nu(S2, U) <= 4; the same for a split of U.
Then a pair of splits needs nu(S_i, U_j) <= 4 for the four pairs of 8-point nodes (8 x 8 blocks).
Ranks modulo 2^31 - 1 (lower bounds, so rejections are rigorous); the survivors' counts are recomputed exactly."""
import itertools, sys
from quad2 import H, N, bit, rank_mod, rank_exact, nu, stab
S = [x for x in range(N) if (bit(x, 0) & bit(x, 1)) ^ bit(x, 2) == 0]
U = [y for y in range(N) if (bit(y, 1) & bit(y, 3)) ^ bit(y, 4) == 0]
def passing(S, U):
    Uc = [y for y in range(N) if y not in U]
    ok = set()
    for S1 in itertools.combinations(S, 8):
        if nu(S1, U, Uc, rank_mod) <= 4: ok.add(S1)
    splits = []
    for S1 in ok:
        S2 = tuple(x for x in S if x not in S1)
        if S1 < S2 and S2 in ok: splits.append((S1, S2))
    return ok, splits
okS, spS = passing(S, U); okU, spU = passing(U, S)
print(f"8-point subsets of S passing: {len(okS)}; splits of S with both halves passing: {len(spS)}", flush=True)
print(f"8-point subsets of U passing: {len(okU)}; splits of U with both halves passing: {len(spU)}", flush=True)
from collections import Counter
print("stabiliser sizes of the halves in passing splits of S:", sorted(Counter((len(stab(a)), len(stab(b))) for a, b in spS).items()), flush=True)
print("stabiliser sizes of the halves in passing splits of U:", sorted(Counter((len(stab(a)), len(stab(b))) for a, b in spU).items()), flush=True)
def nu88(A, B):
    Bc = [y for y in range(N) if y not in B]
    return nu(A, B, Bc, rank_mod)
good = 0; ex = []; tried = 0
for (S1, S2) in spS:
    for (U1, U2) in spU:
        tried += 1
        if all(nu88(a, b) <= 4 for a in (S1, S2) for b in (U1, U2)):
            Uc1 = [y for y in range(N) if y not in U1]; Uc2 = [y for y in range(N) if y not in U2]
            if all(nu(a, b, [y for y in range(N) if y not in b], rank_exact) <= 4 for a in (S1, S2) for b in (U1, U2)):
                good += 1
                if len(ex) < 3: ex.append((S1, S2, U1, U2))
print(f"pairs of splits tried: {tried}; with all four 8 x 8 node pairs at nu <= 4 (exact): {good}; examples {ex}", flush=True)
