# x-2: classify the supports of a circuit found by hatch.c: are they cosets of subspaces, pairwise nested or disjoint, and of ONE chain?
import sys
N = int(sys.argv[1])
for path in sys.argv[2:]:
    sup = []
    for line in open(path):
        if line.startswith('w '):
            v = [int(t) for t in line[2:].split(':')[1].split()]; sup.append(frozenset(i for i in range(N) if v[i]))
    S = sorted(set(sup), key=lambda s: (len(s), sorted(s)))
    def direction(s):
        b = min(s); return frozenset(x ^ b for x in s)
    aff = all(all((x ^ y) in direction(s) for x in direction(s) for y in direction(s)) for s in S)
    lam = all(a <= b or b <= a or not (a & b) for a in S for b in S)
    dirs = sorted(set(direction(s) for s in S if len(s) < N and aff), key=len)
    chain = all(a <= b or b <= a for a in dirs for b in dirs)
    cross = [sorted(s) for s in S if not (max(s) < N // 2 or min(s) >= N // 2 or len(s) == N)]
    print('%s: %d distinct sets; all cosets of subspaces: %s; pairwise nested or disjoint: %s; the subspaces form one chain: %s; sets that cross the top cut: %s'
          % (path.split('/')[-1], len(S), aff, lam, chain, cross))
