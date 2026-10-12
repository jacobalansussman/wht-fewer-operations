# p-7-twoletters, experiment (b)+(d): fix the first letter L2 (inputs -> m middle wires, m >= N, written as explicit gates),
# then ask the integer programme for the second letter L1 (middle -> outputs) with the fewest rectangles over given trees.
# usage: run16.py <N> <start: half | bricks | pairs> <seed> <time limit per solve> <number of solves>
import sys, time, random, numpy as np
from fractions import Fraction as Fr
from twol import *
N = int(sys.argv[1]); start = sys.argv[2]; seed = int(sys.argv[3]); TLs = float(sys.argv[4]); nsol = int(sys.argv[5])
rng = random.Random(seed); H = Hmat(N); t0 = time.time()
prog0 = Prog(N); mid = []; basic = []     # basic: indices of N wires that form a square invertible set
def G(a, u, b, v): return prog0.gate(Fr(a), u, Fr(b), v)
for b in range(N // 4):
    x0, x1, x2, x3 = 4 * b, 4 * b + 1, 4 * b + 2, 4 * b + 3
    if start in ('half', 'bricks'):
        p1 = G(1, x0, 1, x1); p2 = G(1, x2, -1, x3)
        if b % 2 == 0: hub = G(1, p1, -1, p2); f1 = G(1, hub, 2, x2); f2 = G(-1, hub, 2, x0)     # 1111, 1-11-1
        else:          hub = G(1, p1, 1, p2);  f1 = G(1, hub, -2, x2); f2 = G(-1, hub, 2, x0)    # 11-1-1, 1-1-11
        basic += [len(mid), len(mid) + 1, len(mid) + 2, len(mid) + 3]
        mid += [(Fr(1), p1), (Fr(1), p2), (Fr(1), f1), (Fr(1), f2), (Fr(1), hub)]
        if start == 'bricks':
            if b % 2 == 0: f3 = G(1, hub, -2, x3); f4 = G(1, hub, -2, x1)      # 11-1-1 ; 1-1-11
            else:          f3 = G(1, hub, 2, x3);  f4 = G(1, hub, -2, x1)      # 1111 ; 1-11-1  (hub = 1 1 1 -1)
            mid += [(Fr(1), f3), (Fr(1), f4)]
    elif start == 'pairs':   # sums and differences of pairs, plus the single inputs (free)
        s0 = G(1, x0, 1, x1); d0 = G(1, x0, -1, x1); s1 = G(1, x2, 1, x3); d1 = G(1, x2, -1, x3)
        basic += [len(mid), len(mid) + 1, len(mid) + 2, len(mid) + 3]
        mid += [(Fr(1), s0), (Fr(1), d0), (Fr(1), s1), (Fr(1), d1), (Fr(1), x0), (Fr(1), x2)]
g2 = len(prog0.gates); m = len(mid)
L2 = np.array([[float(h[0] * t) for t in prog0.vec[h[1]]] for h in mid])
print("first letter: %s, %d gates, middle width m = %d, rank %d" % (start, g2, m, np.linalg.matrix_rank(L2)), flush=True)
Gs = np.zeros((N, m)); Gs[:, basic] = H @ np.linalg.inv(L2[basic]); Gs = np.round(Gs * 8) / 8
def informed(vecs, noise=0.3, fixed=None):
    mm = len(vecs); reps = {i: np.array(vecs[i], dtype=float) for i in range(mm)}; mem = {i: [i] for i in range(mm)}
    sign = np.ones(mm); merges = []; ids = {i: i for i in range(mm)}; nxt = mm
    while len(reps) > 1:
        best = None; keys = list(reps)
        for a in range(len(keys)):
            for b in range(a + 1, len(keys)):
                p, q = keys[a], keys[b]
                for sg in (1, -1):
                    sc = np.sum((np.abs(reps[p] - sg * reps[q]) < 1e-9) & (np.abs(reps[p]) > 1e-9)) + noise * rng.random()
                    if best is None or sc > best[0]: best = (sc, p, q, sg)
        _, p, q, sg = best
        for j in mem[q]: sign[j] *= sg
        rep = np.where(np.abs(reps[p] - sg * reps[q]) < 1e-9, reps[p], 0.0)
        merges.append((ids[p], ids[q])); mem[p] = mem[p] + mem[q]; reps[p] = rep; ids[p] = nxt; nxt += 1
        del reps[q]; del mem[q]
    return tree_from_merges(mm, merges), sign
def signs_for_tree(T, vecs):
    sign = np.ones(len(vecs)); rep = {}
    for i, (s, a, b) in enumerate(T):
        if a < 0: rep[i] = np.array(vecs[s[0]], dtype=float); continue
        sc = [np.sum((np.abs(rep[a] - sg * rep[b]) < 1e-9) & (np.abs(rep[a]) > 1e-9)) for sg in (1, -1)]
        sg = 1 if sc[0] >= sc[1] else -1
        for j in T[b][0]: sign[j] *= sg
        rep[i] = np.where(np.abs(rep[a] - sg * rep[b]) < 1e-9, rep[a], 0.0); rep[b] = sg * rep[b]
    return sign
flags = {16: [[8, 4, 2, 1], [8, 4, 1, 2], [4, 8, 2, 1], [1, 2, 4, 8], [12, 4, 2, 1], [8, 2, 4, 1]], 8: [[4, 2, 1], [6, 3, 1], [1, 2, 4]], 32: [[16, 8, 4, 2, 1]]}[N]
best = None
for it in range(nsol):
    if it % 2 == 0: Tout, a1 = informed(list(Gs), noise=0.3 if it else 0.0); how = "clustered rows"
    else:
        fl = flags[(it // 2) % len(flags)]; Tout = chain_tree(N, fl); a1 = signs_for_tree(Tout, list(Gs)); how = "chain %s" % fl
    Tm1, c1 = informed(list(Gs.T), noise=0.3 if it else 0.0)
    r = solve_letter(Tout, a1, Tm1, c1, None, L2, H, tl=TLs, mode='tau')
    if r is None: print("solve %d (%s): nothing found in the time limit" % (it, how), flush=True); continue
    import copy
    prog = copy.deepcopy(prog0)
    out = emit(prog, Tout, a1, Tm1, c1, r['rect'], mid)
    ok = all(out[y] is not None and [out[y][0] * t for t in prog.vec[out[y][1]]] == [(-1) ** bin(y & x).count('1') for x in range(N)] for y in range(N))
    used = sorted(set(j for (_, jn, _) in r['rect'] for j in Tm1[jn][0]))
    g = len(prog.gates)
    print("solve %d (%s): rectangles %d (solver status %d, lower bound %s), EXACT REPLAY %s, gates %d = %d + %d, wires used %d of %d  (%.0f s)"
          % (it, how, len(r['rect']), r['status'], r['bound'], ok, g, g2, g - g2, len(used), m, time.time() - t0), flush=True)
    if ok and (best is None or g < best):
        best = g
        with open("best16_%s_%d.txt" % (start, seed), "w") as f:
            f.write("# %d-point transform, %d gates count (G), exact replay passed; first letter '%s' (%d gates, middle %d wide), second letter %d rectangles\n" % (N, g, start, g2, m, len(r['rect'])))
            for t, (a_, u, b_, v) in enumerate(prog.gates): f.write("w%d = %s * w%d + %s * w%d\n" % (N + t, a_, u, b_, v))
            f.write("# rectangles of the second letter (output set | middle set | number):\n")
            for (i, j, mu) in r['rect']: f.write("#  %s | %s | %s\n" % (list(Tout[i][0]), list(Tm1[j][0]), mu))
            f.write("# output signs %s\n# middle signs %s\n" % (a1.astype(int).tolist(), c1.astype(int).tolist()))
print("done, best", best, "(%.0f s)" % (time.time() - t0))
