# verify15.py: replay the 15-gate circuit found modulo 2 for one block of neighbour sums at 16 points (count (G)),
# show it is right modulo 2, and that this wiring has no lift to the rationals; ranks of the block in several fields.
import itertools, re
from fractions import Fraction
ev = [x for x in range(16) if bin(x).count('1') % 2 == 0]; od = [x for x in range(16) if bin(x).count('1') % 2 == 1]
T = [[1 if bin(x ^ y).count('1') == 1 else 0 for x in ev] for y in od]
gates = []; kinds = []
for line in open('B4_p2_m7_top_d2.out'):
    mm = re.match(r'\s+g(\d+)\s+(TARGET|inter)\s+= \[([0-9 ]+)\]\s+from #(\d+) \+ (\d+)\*#(\d+)', line)
    if mm: gates.append((int(mm.group(4)), int(mm.group(6)))); kinds.append((mm.group(2), [int(c) for c in mm.group(3).split()]))
print('gates read:', len(gates))
def run(signs, mod=None):
    rows = [[int(i == j) for j in range(8)] for i in range(8)]
    for (u, v), s in zip(gates, signs):
        r = [rows[u][j] + s * rows[v][j] for j in range(8)]
        rows.append([c % mod for c in r] if mod else r)
    return rows
rows = run([1] * 15, 2)
ok2 = all(rows[8 + i] == kinds[i][1] for i in range(15)) and sorted(r for (kd, r) in kinds if kd == 'TARGET') == sorted(T)
print('replay modulo 2: every gate as printed and the 8 targets are exactly the 8 rows of the block:', ok2)
def rank(M, p):
    M = [[Fraction(c) if p == 0 else c % p for c in r] for r in M]; rk = 0
    for c in range(len(M[0])):
        piv = next((i for i in range(rk, len(M)) if M[i][c] != 0), None)
        if piv is None: continue
        M[rk], M[piv] = M[piv], M[rk]
        inv = 1 / M[rk][c] if p == 0 else pow(M[rk][c], -1, p)
        M[rk] = [x * inv if p == 0 else x * inv % p for x in M[rk]]
        for i in range(len(M)):
            if i != rk and M[i][c] != 0:
                f = M[i][c]; M[i] = [(a - f * b) if p == 0 else (a - f * b) % p for a, b in zip(M[i], M[rk])]
        rk += 1
    return rk
print('rank of the 8 x 8 block: rationals', rank(T, 0), ' mod 2:', rank(T, 2), ' mod 3:', rank(T, 3), ' mod 5:', rank(T, 5), ' mod 7:', rank(T, 7))
for k in (3, 5, 6):
    N = 1 << k; e = [x for x in range(N) if bin(x).count('1') % 2 == 0]; o = [x for x in range(N) if bin(x).count('1') % 2 == 1]
    B = [[1 if bin(x ^ y).count('1') == 1 else 0 for x in e] for y in o]
    print('  k =', k, 'block', len(B), 'rank rationals', rank(B, 0), 'mod 2', rank(B, 2), 'mod 3', rank(B, 3))
# lifts with coefficients +1/-1 on every gate: does any choice give the targets up to sign over the integers?
Tset = {tuple(r) for r in T} | {tuple(-c for c in r) for r in T}; hits = 0
tidx = [i for i in range(15) if kinds[i][0] == 'TARGET']
for signs in itertools.product((1, -1), repeat=15):
    rows = run(signs)
    if all(tuple(rows[8 + i]) in Tset for i in tidx): hits += 1
print('sign patterns (+1/-1 on each of the 15 gates) that give all 8 targets over the integers:', hits, 'of', 2 ** 15)
# antipodal relation over the rationals: T(y) + T(y + 1111) = all ones
print('T(y) + T(y+1111) = all-ones row for every odd y:', all([a + b for a, b in zip(T[od.index(y)], T[od.index(y ^ 15)])] == [1] * 8 for y in od))
