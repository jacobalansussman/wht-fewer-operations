# more.py (ac-0): (a) 64 points modulo 2 by composition A_6 = A_4 (x) 1 + 1 (x) A_2, with the 15-gate block inside A_4;
# (b) ranks of one block at 64 points; (c) the rational circuit closest to the 15-gate wiring: how many gates does the
# antipodal relation give over the integers. Exact integers / Fractions / bitsets. Count (G).
import re, itertools
from fractions import Fraction as Fr
F = 'waves/wave-08/ab-0-neighboursums/'
pc = lambda x: bin(x).count('1')
ev = [x for x in range(16) if pc(x) % 2 == 0]; od = [x for x in range(16) if pc(x) % 2 == 1]
ROW = {y: [1 if pc(x ^ y) == 1 else 0 for x in ev] for y in od}
wiring = {}
for line in open(F + 'B4_p2_m7_top_d2.out'):
    m = re.match(r'\s+g(\d+)\s+(TARGET|inter)\s+= \[([0-9 ]+)\]\s+from #(\d+) \+ 1\*#(\d+)', line)
    if m: wiring[int(m.group(1))] = (int(m.group(4)), int(m.group(5)))
OUT = {1: 17, 2: 14, 4: 20, 7: 21, 8: 22, 11: 12, 13: 18, 14: 15}       # output address -> gate (replay.out)
def a4(vals):
    out = {}; gates = 0
    for tr in (0, 1):
        w = {j: vals[ev[j] ^ tr] for j in range(8)}
        for g in sorted(wiring): w[g] = w[wiring[g][0]] ^ w[wiring[g][1]]; gates += 1
        for y, g in OUT.items(): out[y ^ tr] = w[g]
    return out, gates
k = 6; N = 64; gates = 0; part4 = {}; part2 = {}
for base in range(0, N, 16):
    o, g = a4({a: 1 << (base | a) for a in range(16)}); gates += g
    for a in range(16): part4[base | a] = o[a]
for low in range(16):
    p = (1 << (low | 16)) ^ (1 << (low | 32)); q = (1 << low) ^ (1 << (low | 48)); gates += 2
    part2[low] = p; part2[low | 48] = p; part2[low | 16] = q; part2[low | 32] = q
acc = {}
for y in range(N): acc[y] = part4[y] ^ part2[y]; gates += 1
ok = all(acc[y] == sum(1 << (y ^ (1 << j)) for j in range(k)) for y in range(N))
print('(a) 64 points modulo 2: gates', gates, ' correct modulo 2:', ok, ' adding-only law:', 64 * (5 - Fr(3, 2)))

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
for kk in (4, 6, 8):
    NN = 1 << kk; e = [x for x in range(NN) if pc(x) % 2 == 0]; o = [x for x in range(NN) if pc(x) % 2 == 1]
    Bm = [[1 if pc(x ^ y) == 1 else 0 for x in e] for y in o]
    print('(b) k =', kk, ' block', len(Bm), ' rank modulo 2:', rank(Bm, 2), ' modulo 3:', rank(Bm, 3), (' rationals: %d' % rank(Bm)) if kk < 8 else '')

# (c) over the integers: keep g8..g18 (11 gates, five outputs 11, 2, 14, 1, 13 by adding only), then the antipodal relation
# out(y) + out(y^15) = S (sum of all 8 inputs) gives out(4) = out(13) - out(11) + out(2) in 2 gates; outputs 7 and 8 then need
# S: S = out(13) + out(2) (1 gate), out(7) = S - out(8) ... count the cheapest completion by brute force over short programs
have = {11: ROW[11], 2: ROW[2], 14: ROW[14], 1: ROW[1], 13: ROW[13]}
S = [1] * 8
sub = lambda a, b: [x - y for x, y in zip(a, b)]; add = lambda a, b: [x + y for x, y in zip(a, b)]
d = sub(ROW[13], ROW[11]); r4 = add(d, ROW[2]); s = add(ROW[13], ROW[2]); r7 = sub(s, ROW[8]);
print('(c) integers: out(13)-out(11)+out(2) = out(4):', r4 == ROW[4], '; out(13)+out(2) = all-ones:', s == S, '; out(7) = S - out(8):', r7 == ROW[7], '; out(8) = S - out(7), so one of 7, 8 must still be built from inputs')
print('    count: 11 (five outputs) + 2 (output 4) + 1 (S) + 3 (output 8 = x0 + x9 + x10 + x12 from inputs, no pair available) + 1 (output 7 = S - output 8) = 18 > 16')
