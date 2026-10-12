# p-7-twoletters, the "better question": is the 8-point map M8 (four whole characters and four half characters of an 8-block,
# the job of e2-0's first two letters, 16 gates there) ONE letter in 16 gates?  Float solver, candidates replayed exactly.
# usage: m8.py <seed> <seconds per solve> <number of solves>
import sys, time, random, itertools, numpy as np
from fractions import Fraction as Fr
from twol import *
seed = int(sys.argv[1]); TLs = float(sys.argv[2]); nsol = int(sys.argv[3]); rng = random.Random(seed); t0 = time.time()
ch = [np.array([(-1) ** bin(c & x).count('1') for x in range(4)], dtype=float) for c in range(4)]
Z = np.zeros(4)
def informed(vecs, noise):
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
best = None
for it in range(nsol):
    eps = [rng.choice([1, -1]) for _ in range(4)] if it else [1, 1, 1, 1]
    side = [rng.randrange(2) for _ in range(4)] if it else [0, 0, 1, 1]
    rowsl = []
    for c in range(4):
        rowsl.append(np.concatenate([ch[c], Z]) if side[c] == 0 else np.concatenate([Z, ch[c]]))
    for c in range(4): rowsl.append(np.concatenate([ch[c], eps[c] * ch[c]]))
    T = np.array(rowsl)
    # input tree: pairs, blocks of 4, root; centre of the "three agree" kind on each block, random which entry differs
    pr = rng.choice([[(0, 1), (2, 3)], [(0, 2), (1, 3)], [(0, 3), (1, 2)]]) if it else [(0, 1), (2, 3)]
    sets = [pr[0], pr[1], (0, 1, 2, 3), (4 + pr[0][0], 4 + pr[0][1]), (4 + pr[1][0], 4 + pr[1][1]), (4, 5, 6, 7), tuple(range(8))]
    Tin = tree_from_sets(8, sets)
    cc = np.ones(8); cc[rng.randrange(4) if it else 2] = -1; cc[4 + (rng.randrange(4) if it else 3)] = -1
    if rng.random() < 0.5 and it: cc[4:] *= -1
    Tout, ar = informed(list(T * cc), 0.0 if it == 0 else 0.6)
    r = solve_letter(Tout, ar, Tin, cc, None, None, T, tl=TLs, mode='full')
    if r is None: print("solve %d: nothing" % it, flush=True); continue
    prog = Prog(8); out = emit(prog, Tout, ar, Tin, cc, r['rect'], [(Fr(1), i) for i in range(8)])
    ok = all(out[y] is not None and [float(out[y][0] * t) for t in prog.vec[out[y][1]]] == list(T[y]) for y in range(8))
    g = len(prog.gates)
    print("solve %d: eps %s side %s pairs %s centre %s: programme value %d (status %d, bound %s), exact replay %s, GATES %d  (%.0f s)"
          % (it, eps, side, pr, cc.astype(int).tolist(), r['cost'], r['status'], r['bound'], ok, g, time.time() - t0), flush=True)
    if ok and (best is None or g < best):
        best = g
        with open("m8_best_%d.txt" % seed, "w") as f:
            f.write("# M8 as one letter: %d gates (G), exact replay passed. target rows (as sums of x0..x7):\n" % g)
            for row in T: f.write("#   %s\n" % row.astype(int).tolist())
            for t, (a_, u, b_, v) in enumerate(prog.gates): f.write("w%d = %s * w%d + %s * w%d\n" % (8 + t, a_, u, b_, v))
            f.write("# outputs: %s\n" % [(str(h[0]), "w%d" % h[1]) for h in out])
print("done, best", best, "(%.0f s)" % (time.time() - t0))
