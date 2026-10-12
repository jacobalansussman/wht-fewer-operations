# u-8-compose: (1) is every wire a sign vector (entries 0, +c, -c) on an affine set, with supports nested or disjoint?
# (2) the top-level delta of u-8.md section 3:  delta = |W| - N/2 - 1 - n_L - n_R,  W = full wires, L and R = the two halves
# (the two largest proper supports), n_L = number of L-restrictions of full wires (up to sign) not held as wires on L.
import sys
exec(open('compose.py').read().split("if __name__ == '__main__':")[0])
def sgn(w, idx):
    v = [w[i] for i in idx]; s = 1 if v[0] > 0 else -1
    return tuple(int(s * (1 if t > 0 else -1)) for t in v)
def run(label, g):
    N = npts(g); k = N.bit_length() - 1; out, W = outputs(g, N)
    sup = {}; signok = True; affine = True
    for (name, *_ ) in g:
        w = W[name]; S = tuple(i for i in range(N) if w[i] != 0)
        if len({abs(w[i]) for i in S}) != 1: signok = False
        Ss = set(S)
        if any((a ^ b ^ c) not in Ss for a in S[:1] for b in S for c in S): affine = False
        sup.setdefault(S, []).append(name)
    sets = [set(S) for S in sup]
    lam = all(a <= b or b <= a or not (a & b) for i, a in enumerate(sets) for b in sets[i + 1:])
    halves = [S for S in sup if len(S) == N // 2]
    L, R = halves[0], halves[1]; assert len(halves) == 2 and set(L) | set(R) == set(range(N))
    full = [W[n] for n in sup[tuple(range(N))]]
    res = []
    for H in (L, R):
        held = {sgn(W[n], H) for n in sup[H]}
        res.append(len({sgn(w, H) for w in full} - held))
    images = {(sgn(w, L), sgn(w, R)) for w in full}
    d = len(full) - N // 2 - 1 - res[0] - res[1]
    GL = sum(len(v) for S, v in sup.items() if set(S) <= set(L)); GR = sum(len(v) for S, v in sup.items() if set(S) <= set(R))
    fl = lambda n: (n - 1) + (n // 2) * (n.bit_length() - 1)
    eL = GL + res[0] - fl(N // 2); eR = GR + res[1] - fl(N // 2)
    assert eL + eR + d == len(g) - fl(N)
    print('      projections: left %d gates (e = %d), right %d gates (e = %d);  e(left) + e(right) + delta = %d' % (GL + res[0], eL, GR + res[1], eR, eL + eR + d))
    print('%-24s N=%3d gates=%4d  sign vectors=%s affine supports=%s nested or disjoint=%s (%d supports)  full wires=%3d  n_L=%2d n_R=%2d  distinct images=%3d  delta=%3d   e=%3d'
          % (label, N, len(g), signok, affine, lam, len(sup), len(full), res[0], res[1], len(images), d, len(g) - (N - 1) - N * k // 2))
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
