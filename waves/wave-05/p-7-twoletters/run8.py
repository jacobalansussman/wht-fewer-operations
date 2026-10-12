# p-7-twoletters: calibration and a local search over products of two letters. usage: run8.py <N> <seed> <seconds> <start>
import sys, time, random, numpy as np
from fractions import Fraction as Fr
sys.path.insert(0, sys.path[0])
from twol import *
N = int(sys.argv[1]); seed = int(sys.argv[2]); budget = float(sys.argv[3]); start = sys.argv[4] if len(sys.argv) > 4 else 'tree'
k = N.bit_length() - 1; rng = random.Random(seed); H = Hmat(N); t0 = time.time()
TL = 15.0 if N == 8 else 60.0

def rand_flag():
    gens = []; V = {0}
    while len(V) < N // 2:
        g = rng.randrange(1, N)
        if g in V: continue
        gens.append(g); V |= {v ^ g for v in V}
    return gens
def informed(vecs, noise=0.3):
    # greedy clustering of vectors that agree up to sign on many coordinates; returns (tree, signs)
    m = len(vecs); reps = {i: np.array(vecs[i], dtype=float) for i in range(m)}; mem = {i: [i] for i in range(m)}
    sign = np.ones(m); merges = []; ids = {i: i for i in range(m)}; nxt = m
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
    return tree_from_merges(m, merges), sign
def cost_total(L2d, L1d):
    g, g2, ok, prog, mid = replay(N, L2d, L1d)
    return (g if ok else None), g2, prog, mid

# ---- calibration: one letter
if N == 8:
    Tin = chain_tree(8, [7, 1, 2]); Tout = chain_tree(8, [6, 3, 1])
    c = np.array([1, -1, -1, -1, 1, 1, -1, 1.0]); a = np.array([-1, 1, 1, 1, 1, -1, 1, 1.0])
    r = solve_letter(Tout, a, Tin, c, None, None, H, tl=TL)
    print("calibration, one letter, g-1's trees and signs: programme cost", r['cost'], "rectangles", len(r['rect']), "status", r['status'], flush=True)
    idT = [((i,), -1, -1) for i in range(8)] + random_tree(8, rng)[8:]
    L2id = (idT, np.ones(8), idT, np.ones(8), [(i, i, Fr(1)) for i in range(8)])
    g, g2, ok, prog, mid = replay(8, L2id, (Tout, a, Tin, c, r['rect']))
    print("   exact replay: gates", g, "all outputs exact:", ok, flush=True)

def start_state():
    if start == 'tree':      # middle = every node form of a random chain tree with a random sign centre (one letter written as two)
        Tin = chain_tree(N, rand_flag()); c = np.array([rng.choice([1.0, -1.0]) for _ in range(N)])
        L2 = np.array([[c[x] if x in s else 0.0 for x in range(N)] for (s, _, _) in Tin])
    elif start == 'bricks':  # characters on blocks of 4, plus the block hubs, plus the single inputs
        rowsl = []
        for b in range(N // 4):
            for ch in range(4):
                v = np.zeros(N); v[4 * b:4 * b + 4] = [(-1) ** bin(ch & x).count('1') for x in range(4)]; rowsl.append(v)
            v = np.zeros(N); v[4 * b:4 * b + 4] = [1, 1, -1, 1]; rowsl.append(v)
            v = np.zeros(N); v[4 * b:4 * b + 2] = [1, 1]; rowsl.append(v)
            v = np.zeros(N); v[4 * b + 2:4 * b + 4] = [1, -1]; rowsl.append(v)
        L2 = np.array(rowsl)
    elif start == 'half':   # e2-0's first letter: per block (1100),(001-1),(1111),(1-11-1) or (1100),(001-1),(11-1-1),(1-1-11), plus hubs
        rowsl = []
        for b in range(N // 4):
            pats = [[1, 1, 0, 0], [0, 0, 1, -1]] + ([[1, 1, 1, 1], [1, -1, 1, -1], [1, 1, -1, 1]] if b % 2 == 0 else [[1, 1, -1, -1], [1, -1, -1, 1], [1, 1, 1, -1]])
            for p_ in pats:
                v = np.zeros(N); v[4 * b:4 * b + 4] = p_; rowsl.append(v)
        L2 = np.array(rowsl)
    return L2

def solve_L2(L2target, L1mat):
    # a letter for the middle forms; rows = wires. If L1mat is given the constraint is L1 * L2 = H (L2 free), else L2 = L2target.
    m = L2target.shape[0]
    Tm2, a2 = informed(list(L2target)); Tin, c2 = informed(list(L2target.T))
    if rng.random() < 0.3: Tin = chain_tree(N, rand_flag())
    if L1mat is None: r = solve_letter(Tm2, a2, Tin, c2, None, None, L2target, tl=TL)
    else: r = solve_letter(Tm2, a2, Tin, c2, L1mat, None, H, tl=TL)
    return None if r is None else (Tm2, a2, Tin, c2, r['rect'])
def solve_L1(L2mat, guess=None):
    m = L2mat.shape[0]
    G = guess if guess is not None else H @ np.linalg.pinv(L2mat)
    G = np.round(G * 16) / 16
    Tm1, c1 = informed(list(G.T)); Tout, a1 = informed(list(G))
    if rng.random() < 0.5: Tout = chain_tree(N, rand_flag()); a1 = np.array([rng.choice([1.0, -1.0]) for _ in range(N)])
    r = solve_letter(Tout, a1, Tm1, c1, None, L2mat, H, tl=TL)
    return None if r is None else (Tout, a1, Tm1, c1, r['rect'])

best = None; nrun = 0
while time.time() - t0 < budget:
    nrun += 1
    L2 = start_state(); L2d = solve_L2(L2, None)
    if L2d is None: continue
    L1d = solve_L1(L2)
    if L1d is None: continue
    g, g2, prog, mid = cost_total(L2d, L1d)
    if g is None: print("  start: replay failed (float candidate rejected)", flush=True); continue
    print("run %d start %s: m = %d, gates %d = %d + %d  (%.0f s)" % (nrun, start, L2.shape[0], g, g2, g - g2, time.time() - t0), flush=True)
    cur = (g, L2d, L1d)
    stale = 0
    while stale < 6 and time.time() - t0 < budget:
        g, L2d, L1d = cur
        _, _, prog, mid = cost_total(L2d, L1d)
        L2mat = wires_matrix(prog, mid, N); L1mat = letter_matrix(*L1d)
        if rng.random() < 0.5:
            n1 = solve_L1(L2mat, L1mat); cand = None if n1 is None else (L2d, n1)
        else:
            n2 = solve_L2(L2mat, L1mat); cand = None if n2 is None else (n2, L1d)
        if cand is None: stale += 1; continue
        gg, gg2, _, _ = cost_total(*cand)
        if gg is not None and gg <= g:
            stale = stale + 1 if gg == g else 0
            cur = (gg, cand[0], cand[1])
            if gg < g: print("   -> %d = %d + %d  (%.0f s)" % (gg, gg2, gg - gg2, time.time() - t0), flush=True)
        else: stale += 1
    if best is None or cur[0] < best[0]:
        best = cur
        g, L2d, L1d = cur; _, g2, prog, mid = cost_total(L2d, L1d)
        used = [j for j in range(len(mid)) if np.any(letter_matrix(*L1d)[:, j])]
        print("BEST so far: %d gates = %d + %d, middle wires used by the second letter: %d of %d" % (g, g2, g - g2, len(used), len(mid)), flush=True)
        with open(sys.path[0] + "/best_%d_%s_%d.txt" % (N, start, seed), "w") as f:
            f.write("# %d-point transform, %d gates count (G), product of two letters, exact replay passed; gate = a*u + b*v\n" % (N, g))
            f.write("# wires 0..%d are the inputs; middle wires used: %d; gates of the first letter (inputs -> middle): %d\n" % (N - 1, len(used), g2))
            for t, (a_, u, b_, v) in enumerate(prog.gates): f.write("w%d = %s * w%d + %s * w%d\n" % (N + t, a_, u, b_, v))
            f.write("# rectangles letter 2->middle: %d ; letter middle->out: %d\n" % (len(L2d[4]), len(L1d[4])))
            f.write("# middle forms used (as sums of inputs):\n")
            W = wires_matrix(prog, mid, N)
            for j in used: f.write("#   z%d = %s\n" % (j, [int(t) if float(t).is_integer() else float(t) for t in W[j]]))
print("done: runs", nrun, "best", None if best is None else best[0], "(%.0f s)" % (time.time() - t0))
