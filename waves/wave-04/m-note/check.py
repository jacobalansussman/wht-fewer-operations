# m-note: small exact checks of objects quoted in WAVE4-NOTE.md. Whole numbers only. Count (G).
from math import log, gcd
from functools import reduce

def had(k):
    N = 1 << k
    return [[(-1) ** bin(i & j).count("1") for j in range(N)] for i in range(N)]

def unit(N, i):
    return tuple(1 if j == i else 0 for j in range(N))
def lin(a, u, b, v):
    return tuple(a * x + b * y for x, y in zip(u, v))

def cls(w):
    # class modulo 2 of the primitive form (wires here are whole-number vectors)
    g = reduce(gcd, [abs(x) for x in w])
    p = [x // g for x in w]            # entries now have gcd 1, so not all even
    return tuple(x & 1 for x in p)

def meter(name, N, wires, outs):
    # wires: list of gate results in order (vectors over the inputs); outs: the N outputs
    k = N.bit_length() - 1
    H = had(k)
    assert sorted(outs) == sorted(tuple(r) for r in H) or \
           sorted(tuple(abs(x) for x in o) for o in outs) == sorted(tuple(abs(x) for x in r) for r in H) and \
           {tuple(o) for o in outs} | {tuple(-x for x in o) for o in outs} >= {tuple(r) for r in H}, name
    held = {cls(unit(N, i)) for i in range(N)}
    surv = dead = 0
    for w in wires:
        c = cls(w)
        if c in held: dead += 1
        else: surv += 1; held.add(c)
    # nested or disjoint?
    sets = [frozenset(i for i, b in enumerate(c) if b) for c in held]
    lam = all(a <= b or b <= a or not (a & b) for a in sets for b in sets)
    # over-limit wires: s = non-zeros in the inputs, s' = non-zeros of the wire written in the outputs (w.H up to 1/N)
    over = set()
    for w in wires:
        s = sum(1 for x in w if x)
        t = sum(1 for r in H if sum(a * b for a, b in zip(w, r)))
        if s * t > N:
            g = reduce(gcd, [abs(x) for x in w]); p = tuple(x // g for x in w)
            if p[next(i for i, x in enumerate(p) if x)] < 0: p = tuple(-x for x in p)
            over.add(p)
    G = len(wires)
    print(f"{name}: N={N} gates={G} classes={len(held)} (2N-1={2*N-1}) one tree={lam} survivors={surv} (N-1={N-1}) "
          f"dead={dead} ((N/2)log2N={N*k//2}) over-limit wires={len(over)} gates+over={G+len(over)} (N log2 N={N*k})")

# textbook
def textbook(k):
    N = 1 << k
    cur = [unit(N, i) for i in range(N)]; wires = []
    for b in range(k):
        nxt = list(cur)
        for i in range(N):
            if not i >> b & 1:
                j = i | 1 << b
                nxt[i] = lin(1, cur[i], 1, cur[j]); nxt[j] = lin(1, cur[i], -1, cur[j])
                wires += [nxt[i], nxt[j]]
        cur = nxt
    return N, wires, cur
for k in (2, 3, 4):
    N, w, o = textbook(k); meter(f"textbook {N}", N, w, o)

# the brick, 7 gates at 4 points
x = [unit(4, i) for i in range(4)]
a = lin(1, x[0], 1, x[1]); b = lin(1, x[2], -1, x[3]); h = lin(1, a, 1, b)
o = [lin(1, h, 2, x[3]), lin(1, h, -2, x[1]), lin(1, h, -2, x[2]), lin(-1, h, 2, x[0])]
meter("brick", 4, [a, b, h] + o, o)

# g-1's 19 at 8 points (wiring as in k-note/check.py, from the wave-3 task text)
x = [unit(8, i) for i in range(8)]
g1 = lin(1, x[0], 1, x[7]); g2 = lin(1, x[1], 1, x[6]); g3 = lin(1, x[2], -1, x[5]); g4 = lin(1, x[3], -1, x[4])
g5 = lin(1, g1, -1, g2); g6 = lin(1, g3, 1, g4); g7 = lin(1, g5, -1, g6)
g8 = lin(1, g7, -2, x[7]); g9 = lin(1, g7, -2, x[5]); g10 = lin(1, g8, 2, x[6]); g11 = lin(1, g9, -2, x[4])
y = [None] * 8
y[7] = lin(1, g10, 2, g4); y[1] = lin(1, g10, 2, g3); y[6] = lin(1, g11, 2, g2); y[0] = lin(-1, g11, 2, g1)
y[2] = lin(1, g8, 2, x[1]); y[3] = lin(1, g9, 2, x[3]); y[4] = lin(1, y[2], 2, g6); y[5] = lin(-1, y[3], 2, g5)
ws = [g1, g2, g3, g4, g5, g6, g7, g8, g9, g10, g11, y[7], y[1], y[6], y[0], y[2], y[3], y[4], y[5]]
print("19: outputs equal H_8 in natural order:", [list(v) for v in y] == had(3))
meter("the 19", 8, ws, y)

# floor formula N - 1 + (N/2) log2 N against records
for k, rec in zip(range(1, 7), (2, 7, 19, 52, 128, 304)):
    N = 1 << k
    print(f"floor N={N}: {N - 1 + N * k // 2}  record {rec}  textbook {N * k}  (3/4)N log2 N + N/4 = {3 * N * k / 4 + N / 4}")

# h-3 / n-0 growth law in count (O), H x exactly: N(2.5 floor(k/3) + k mod 3) + N
for k in (3, 6, 9, 12):
    N = 1 << k
    print(f"(O) k={k}: {int(N * (2.5 * (k // 3) + k % 3) + N)} against textbook {N * k}")

# savings quoted in section 3: saving = 1 - log(moves/arrays)/log(block size)
for m, W, mv in ((5, 4, 17), (5, 4, 18), (5, 4, 19), (5, 5, 24), (5, 6, 26), (5, 19, 80), (4, 15, 59)):
    print(f"block {m}, {W} arrays, {mv} moves: saving {1 - log(mv / W) / log(m):.3e}")
print("counting floor 3.75 moves per array at block size 5: exponent", round(log(3.75) / log(5), 4))
# h-7: gates saved per over-limit wire, rides
print("h-7: 120/28135 =", round(120 / 28135, 5), " 120/389730 =", f"{120/389730:.2e}")
