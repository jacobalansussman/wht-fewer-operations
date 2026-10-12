#!/usr/bin/env python3
"""h-0 onepergate / perlevel.py : is L1 true LEVEL BY LEVEL?  8 points, pool P304, count (G).  Exact (the circuits are sets of
collinear integer vectors, as in saw.py).
Guess tested: for d = 1, 2:   T_d + 2 * V_d >= 8,   where T_d = tight helpers of level d (s = 2^d) and
V_d = over-limit helpers whose s' lies in the band (8/2^d, 16/2^d]  (d = 1: s' = 8;  d = 2: s' = 4).
Summed over d this is L1.  Every circuit the weighted annealer visits is tested; a counterexample is printed.
usage: perlevel.py <seconds> <seed> <start>
"""
import sys, time, random, math
src = open(__file__.rsplit('/', 1)[0] + '/saw.py').read().split("if __name__ == '__main__':")[0]
exec(src)
def profile(H):
    T1 = sum(1 for w in H if not over[w] and S[w] == 2); T2 = sum(1 for w in H if not over[w] and S[w] == 4)
    V1 = sum(1 for w in H if over[w] and T[w] == 8); V2 = sum(1 for w in H if over[w] and T[w] == 4)
    return T1, V1, T2, V2
secs, seed, st = float(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
rng = random.Random(seed); H = start(st); E, miss, dead = energy(H); t0 = time.time(); it = 0; seen = {}
while time.time() - t0 < secs:
    it += 1; temp = 0.6 * (1 - 0.6 * (((time.time() - t0) % 40.0) / 40.0))
    H2 = list(H); m = rng.random()
    if m < 0.35 or not H2:
        avail, _ = closure(H2); w = rng.choice(cand)
        for _ in range(6):
            if w not in H2 and any((avail & mm) == mm for mm in just[w]): break
            w = rng.choice(cand)
        if w in H2: continue
        H2.append(w)
    elif m < 0.7: H2.pop(rng.randrange(len(H2)))
    else:
        H2.pop(rng.randrange(len(H2))); w = rng.choice(cand)
        if w in H2: continue
        H2.append(w)
    E2, miss2, dead2 = energy(H2)
    if E2 <= E or rng.random() < math.exp(-(E2 - E) / temp):
        H, E, miss, dead = H2, E2, miss2, dead2
        if miss == 0 and dead == 0: seen[frozenset(H)] = (cost(H), profile(H))
bad = []; tab = {}; slack = {}
for Hs, (c, (T1, V1, T2, V2)) in seen.items():
    a, b = T1 + 2 * V1, T2 + 2 * V2
    if a < 8 or b < 8: bad.append((c, T1, V1, T2, V2, sorted(Hs)))
    if c == 24: tab[(T1, V1, T2, V2)] = tab.get((T1, V1, T2, V2), 0) + 1
    slack[(a - 8, b - 8)] = slack.get((a - 8, b - 8), 0) + 1
print('seed %d start %s: %d moves, %d different circuits, least cost %d' % (seed, st, it, len(seen), min(c for c, _ in seen.values())))
print('   circuits breaking the level-by-level guess (T_1 + 2 V_1 < 8 or T_2 + 2 V_2 < 8): %d' % len(bad))
for b in bad[:6]:
    print('      cost %d: T_1 = %d, V_1 = %d, T_2 = %d, V_2 = %d' % b[:5])
    for w in b[5]: print('         (%d,%d)%s %s' % (S[w], T[w], ' OVER' if over[w] else '', list(ws[w])))
print('   circuits by (slack at level 1, slack at level 2):', sorted(slack.items()))
print('   the cost-24 circuits by (T_1, V_1, T_2, V_2):', sorted(tab.items()))
