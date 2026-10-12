import sys, itertools, collections
from lib import *
k = int(sys.argv[1]); N = 1 << k; fn = sys.argv[2]
pairs = []
for line in open(fn):
    p = line.split('|'); pairs.append((tuple(map(int, p[1].split())), tuple(map(int, p[2].split()))))
print("pairs", len(pairs))
# check the reformulations on every optimal pair
ok1 = ok2 = ok3 = True; dvals = collections.Counter(); twos = 0; prof = collections.Counter(); cprof = collections.Counter(); incomparable = 0
for rows, cols in pairs:
    c, M = corners(rows, cols)
    t, per = steps_count(rows, cols)
    if t != c: ok1 = False
    if bonds_count(rows, cols) != c: ok2 = False
    d = sum(1 for v in per if v == 1)
    if all(v <= 2 for v in per) and c != 2 * N - d: ok3 = False
    dvals[d] += 1
    if any(abs(v) == 2 for r in M for v in r): twos += 1
    prof[tuple(per)] += 1
    cprof[tuple(sum(1 for a in range(N) if M[a][b]) for b in range(N))] += 1
    for a in range(N - 1):
        S, Sp = rows[a], rows[a+1]
        if (S & Sp) not in (S, Sp): incomparable += 1
print("two salesmen formula holds:", ok1, " bonds formula holds:", ok2, " 2N-d holds:", ok3)
print("number of prefix steps d:", dict(dvals), " pictures with an entry +-2 in M:", twos, " incomparable neighbouring outputs (total):", incomparable)
print("non-zeros per output step (first row first) -> pictures:"); [print("  ", p, n) for p, n in sorted(prof.items())]
print("non-zeros per input bond -> pictures:"); [print("  ", p, n) for p, n in sorted(cprof.items())]
# classes under permutations of the address bits
def perm_bits(x, pm): return sum(1 << pm[i] for i in range(k) if x >> i & 1)
seen = set(); classes = []
for rows, cols in pairs:
    if (rows, cols) in seen: continue
    orb = set()
    for pm in itertools.permutations(range(k)):
        orb.add((tuple(perm_bits(x, pm) for x in rows), tuple(perm_bits(x, pm) for x in cols)))
    seen |= orb; classes.append((min(orb), len(orb)))
print("classes up to permuting the address bits:", len(classes))
full = N - 1
# the other symmetry: complement all addresses and exchange the two orders
def dual(rows, cols): return (tuple(full ^ x for x in cols), tuple(full ^ x for x in rows))
cls2 = set(); 
for (rows, cols), sz in classes:
    dr, dc = dual(rows, cols); cd, _ = corners(dr, dc)
    orbd = min((tuple(perm_bits(x, pm) for x in dr), tuple(perm_bits(x, pm) for x in dc)) for pm in itertools.permutations(range(k)))
    cls2.add(min((rows, cols), orbd))
    print("  rows", rows, "cols", cols, "orbit", sz, "| dual has", cd, "corners", "(self-dual class)" if orbd == (rows, cols) else "")
    c, M = corners(rows, cols); t, per = steps_count(rows, cols)
    wr = [bin(x).count('1') for x in rows]; wc = [bin(x).count('1') for x in cols]
    print("      sizes of outputs", wr, " sizes of inputs", wc, " step non-zeros", per)
    # the gap tree: each step = edge between gaps (gap g = before input g; gap N = after the last)
    edges = []
    for a in range(N):
        nzs = [(b, M[a][b]) for b in range(N) if M[a][b]]
        if len(nzs) == 1: edges.append((0, nzs[0][0] + 1))
        elif len(nzs) == 2: edges.append((nzs[0][0] + 1, nzs[1][0] + 1))
        else: edges.append(tuple(b + 1 for b, _ in nzs))
    deg = collections.Counter(x for e in edges for x in e)
    print("      gap edges (step a joins gaps):", edges, " degrees of gaps 0..N:", [deg[g] for g in range(N + 1)])
print("classes up to bit permutations AND the dual:", len(cls2))
