# replay.py (ac-0): my own replay of ab-0's 15-gate circuit modulo 2, the facts the no-lift argument uses, the adding-only
# law, and one size further (64 and 256 points) by composition. Exact: integers and Fractions only. Count (G).
import re, sys, itertools
from fractions import Fraction as Fr
F = 'waves/wave-08/ab-0-neighboursums/'
pc = lambda x: bin(x).count('1')
ev = [x for x in range(16) if pc(x) % 2 == 0]; od = [x for x in range(16) if pc(x) % 2 == 1]
ROW = {y: [1 if pc(x ^ y) == 1 else 0 for x in ev] for y in od}          # row of output y over the 8 even inputs
print('inputs (columns) = even addresses', ev)

# ---- 1. replay modulo 2, wiring read from the authors' output file, values recomputed by me
wires = {j: [int(i == j) for i in range(8)] for j in range(8)}; wiring = {}; printed = {}
for line in open(F + 'B4_p2_m7_top_d2.out'):
    m = re.match(r'\s+g(\d+)\s+(TARGET|inter)\s+= \[([0-9 ]+)\]\s+from #(\d+) \+ 1\*#(\d+)', line)
    if m:
        g, u, v = int(m.group(1)), int(m.group(4)), int(m.group(5)); wiring[g] = (u, v)
        printed[g] = [int(c) for c in m.group(3).split()]
        wires[g] = [(a + b) % 2 for a, b in zip(wires[u], wires[v])]
assert len(wiring) == 15 and all(wires[g] == printed[g] for g in wiring)
got = {}
for g in wiring:
    for y in od:
        if wires[g] == ROW[y]: got.setdefault(y, g)
print('1. gates:', len(wiring), ' every printed vector reproduced; outputs found at gates:', {y: 'g%d' % g for y, g in sorted(got.items())})
print('   all 8 odd addresses present modulo 2:', sorted(got) == od)
for name in ('B4_p2_m7_top_d4.out',):
    w = {j: [int(i == j) for i in range(8)] for j in range(8)}; n = 0
    for line in open(F + name):
        m = re.match(r'\s+g(\d+)\s+(TARGET|inter)\s+= \[([0-9 ]+)\]\s+from #(\d+) \+ 1\*#(\d+)', line)
        if m: w[int(m.group(1))] = [(a + b) % 2 for a, b in zip(w[int(m.group(4))], w[int(m.group(5))])]; n += 1
    print('   second file', name, 'gates', n, 'all 8 outputs present modulo 2:', all(any(w[g] == ROW[y] for g in w) for y in od))
# the same wiring with every gate u+v over the integers: what comes out
wz = {j: [int(i == j) for i in range(8)] for j in range(8)}
for g in sorted(wiring): wz[g] = [a + b for a, b in zip(wz[wiring[g][0]], wz[wiring[g][1]])]
print('   same wiring, gates u+v over the integers: outputs right at', sorted(y for y in od if any(wz[g] == ROW[y] for g in wiring)), ' g19 =', wz[19])

# ---- 2. facts used by the no-lift argument (rationals)
def rank(M, p=0):
    M = [[(Fr(c) if p == 0 else c % p) for c in r] for r in M]; rk = 0
    for c in range(len(M[0])):
        pv = next((i for i in range(rk, len(M)) if M[i][c] != 0), None)
        if pv is None: continue
        M[rk], M[pv] = M[pv], M[rk]
        inv = 1 / M[rk][c] if p == 0 else pow(M[rk][c], -1, p)
        M[rk] = [x * inv if p == 0 else x * inv % p for x in M[rk]]
        for i in range(len(M)):
            if i != rk and M[i][c] != 0:
                f = M[i][c]; M[i] = [(a - f * b) if p == 0 else (a - f * b) % p for a, b in zip(M[i], M[rk])]
        rk += 1
    return rk
B = [ROW[y] for y in od]
print('2. rank of the block: rationals', rank(B), ' modulo 2, 3, 5, 7:', [rank(B, p) for p in (2, 3, 5, 7)])
dep = [S for r in (2, 3, 4) for S in itertools.combinations(od, r) if rank([ROW[y] for y in S]) < r]
print('   dependent sets of at most 4 rows over the rationals:', dep)
print('   every one is two antipodal pairs:', all(len(S) == 4 and sorted(S) == sorted(set(S) | {y ^ 15 for y in S}) for S in dep))
dep3 = [S for r in (2, 3, 4) for S in itertools.combinations(od, r) if rank([ROW[y] for y in S], 3) < r]
print('   the same list modulo 3:', dep3 == dep, '  modulo 5:', [S for r in (2, 3, 4) for S in itertools.combinations(od, r) if rank([ROW[y] for y in S], 5) < r] == dep)
# generic support of each gate under arbitrary coefficients = union of supports
sup = {j: {j} for j in range(8)}
for g in sorted(wiring): sup[g] = sup[wiring[g][0]] | sup[wiring[g][1]]
can = {g: [y for y in od if {j for j in range(8) if ROW[y][j]} <= sup[g]] for g in sorted(wiring)}
print('   rows that fit inside the largest possible support of each gate:', {('g%d' % g): v for g, v in can.items()})
print('   wiring:', {('g%d' % g): wiring[g] for g in sorted(wiring)})

# ---- 3. adding-only law N (k - 1 - floor(k/2)/2): the pairing circuit, built and replayed over the integers
def pairing(k):
    N = 1 << k; gates = 0; out = {}
    pair = {}
    for j in range(k // 2):
        a, b = 1 << (2 * j), 1 << (2 * j + 1)
        for y in range(N):
            key = (j, min(y, y ^ a ^ b))
            if key not in pair:
                v = {}; v[y ^ a] = 1; v[y ^ b] = 1; pair[key] = v; gates += 1
    for y in range(N):
        terms = [pair[(j, min(y, y ^ (1 << (2 * j)) ^ (1 << (2 * j + 1))))] for j in range(k // 2)]
        if k % 2: terms.append({y ^ (1 << (k - 1)): 1})
        acc = dict(terms[0])
        for t in terms[1:]:
            for x, c in t.items(): acc[x] = acc.get(x, 0) + c
            gates += 1
        assert acc == {y ^ (1 << j): 1 for j in range(k)}
    return gates
for k in range(2, 9):
    g = pairing(k); law = Fr(1 << k) * (k - 1 - Fr(k // 2, 2))
    print('3. k =', k, ' N =', 1 << k, ' pairing circuit gates', g, ' law', law, ' equal:', g == law)

# ---- 4. one size further modulo 2: A_k = sum over groups of four bits of A_4 on that group (k = 4m), each A_4 by two
#         copies of the 15-gate block circuit; replayed modulo 2 with bitsets
def block15(inp_even, inp_odd_unused=None): pass
def a4_mod2(vals):
    # vals: dict address(0..15) -> python int bitset (the value as a set of original inputs, modulo 2). returns outputs, gates
    out = {}; gates = 0
    for parity in (0, 1):
        ins = [x for x in range(16) if pc(x) % 2 == parity]            # this block's inputs
        # the circuit was written for inputs = even addresses; for the other block translate by e_1 (address ^ 1)
        tr = 0 if parity == 0 else 1
        w = {j: vals[ev[j] ^ tr] for j in range(8)}
        for g in sorted(wiring): w[g] = w[wiring[g][0]] ^ w[wiring[g][1]]; gates += 1
        for y, g in got.items(): out[y ^ tr] = w[g]
    return out, gates
def big(k):
    N = 1 << k; m = k // 4; gates = 0
    acc = None
    for grp in range(m):
        sh = 4 * grp; part = {}
        for base in range(N):
            if (base >> sh) & 15: continue
            vals = {a: 1 << (base | (a << sh)) for a in range(16)}
            o, g = a4_mod2(vals); gates += g
            for a in range(16): part[base | (a << sh)] = o[a]
        if acc is None: acc = part
        else:
            for y in range(N): acc[y] ^= part[y]; gates += 1
    ok = all(acc[y] == sum(1 << (y ^ (1 << j)) for j in range(k)) for y in range(N))
    return gates, ok
for k in (4, 8):
    g, ok = big(k); N = 1 << k
    print('4. k =', k, ' N =', N, ' gates modulo 2:', g, ' correct modulo 2:', ok, '  N(23k/32 - 1) =', Fr(N) * (Fr(23 * k, 32) - 1), '  adding-only law:', Fr(N) * (k - 1 - Fr(k // 2, 2)))
