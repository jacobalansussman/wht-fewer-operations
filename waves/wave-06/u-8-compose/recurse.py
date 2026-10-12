# u-8-compose: test step (b) of the proof in u-8.md by machine, and write e as a sum of deltas over ALL nodes.
# A circuit is kept as its ordered list of wires (sign vectors up to sign).  rec() checks that every wire is ONE gate from earlier
# wires (a join of two wires on the two halves of its support, or a shift of an earlier wire of the same support by a held
# partner that agrees with it), builds the two projections (wires inside the half, plus the half-restrictions of the full
# wires, in circuit order), checks the same of them, and recurses.  Asserts e = e(left) + e(right) + delta at every node.
import sys
exec(open('compose.py').read().split("if __name__ == '__main__':")[0])
def nrm(v):
    s = next((1 if t > 0 else -1) for t in v if t != 0)
    return tuple(0 if t == 0 else (1 if t * s > 0 else -1) for t in v)
def supp(v): return frozenset(i for i, t in enumerate(v) if t != 0)
def fl(n): return (n - 1) + (n // 2) * (n.bit_length() - 1)
def derivable(w, have, bysupp, N):
    S = supp(w)
    if len(S) == 1: return True
    for T, lst in bysupp.items():                      # join: two earlier wires on complementary halves of S
        if T < S and 2 * len(T) == len(S):
            if nrm([w[i] if i in T else 0 for i in range(N)]) in have and nrm([w[i] if i in S - T else 0 for i in range(N)]) in have: return True
    for u in bysupp.get(S, []):                        # shift: earlier wire u on S, partner = u on the set where w and u differ
        for sg in (1, -1):
            D = [i for i in S if w[i] != sg * u[i]]
            if D and len(D) < len(S) and nrm([u[i] if i in D else 0 for i in range(N)]) in have: return True
    return False
def rec(wires, node, N, acc, bad):
    n = len(node)
    if n == 1: return 0
    have = {tuple(int(i == j) for j in range(N)) for i in node}; bysupp = {}
    for i in node: bysupp.setdefault(frozenset([i]), []).append(tuple(int(i == j) for j in range(N)))
    for w in wires:
        if not derivable(w, have, bysupp, N): bad.append((n, w))
        have.add(w); bysupp.setdefault(supp(w), []).append(w)
    halves = [T for T in bysupp if 2 * len(T) == n and T < node]
    assert len(halves) == 2 and halves[0] | halves[1] == node, (n, len(halves))
    full = [w for w in wires if supp(w) == node]
    e_here = len(wires) - fl(n); tot = 0; d = len(full) - n // 2 - 1
    for H in halves:
        proj = []; seen = set()
        for w in wires:
            if supp(w) <= H: r = w
            elif supp(w) == node: r = nrm([w[i] if i in H else 0 for i in range(N)])
            else: continue
            if len(supp(r)) > 1 and r not in seen: seen.add(r); proj.append(r)
        held = {w for w in wires if supp(w) == H}
        d -= len({w for w in proj if supp(w) == H} - held)
        tot += rec(proj, H, N, acc, bad)
    assert d >= 0 and e_here == tot + d, (n, e_here, tot, d)
    acc[n] = acc.get(n, 0) + d
    return e_here
def run(label, g):
    N = npts(g); out, W = outputs(g, N); wires = []; seen = set()
    for (name, *_ ) in g:
        w = nrm(W[name])
        if w not in seen: seen.add(w); wires.append(w)
    acc = {}; bad = []
    e = rec(wires, frozenset(range(N)), N, acc, bad)
    print('%-24s N=%3d gates=%4d distinct wires=%4d  e=%3d = sum of deltas by node size %s   wires not one gate from earlier ones, in the circuit or in any projection: %d'
          % (label, N, len(g), len(wires), e, ' '.join('%d:%d' % (s, acc[s]) for s in sorted(acc)), len(bad)))
brick = parse(ID + 'h-6-classhub/brick_m1.txt'); n19 = parse(ID + 'g-1-tightwires/h8_19gates.txt')
t2 = [('s', F(1), 'x0', F(1), 'x1'), ('d', F(1), 'x0', F(-1), 'x1')]
st = {N: parse(ID + 'e2-0-pieces/slp_%d.txt' % N) for N in (8, 16, 32, 64)}
t4 = tensor(t2, t2)
for lab, g in (('textbook 4', t4), ('brick', brick), ('the 19', n19), ('staircase 8', st[8]), ('staircase 16', st[16]), ('staircase 32', st[32]), ('staircase 64', st[64]),
               ('second 52 (h-1)', parse(ID + 'h-1-staircase3/slp16_52_from54.txt')), ('textbook 16', tensor(t4, t4)), ('brick x textbook4', tensor(brick, t4)),
               ('textbook4 x brick', tensor(t4, brick)), ('brick x brick', tensor(brick, brick)), ('staircase8 x t2', tensor(st[8], t2)), ('t2 x staircase8', tensor(t2, st[8])),
               ('19 x t2', tensor(n19, t2)), ('t2 x 19', tensor(t2, n19)), ('brick x 19', tensor(brick, n19)), ('19 x brick', tensor(n19, brick)),
               ('brick x staircase8', tensor(brick, st[8])), ('staircase8 x brick', tensor(st[8], brick)), ('19 x 19', tensor(n19, n19)),
               ('staircase8 x staircase8', tensor(st[8], st[8])), ('brick x staircase16', tensor(brick, st[16])), ('staircase16 x brick', tensor(st[16], brick))):
    run(lab, g)
