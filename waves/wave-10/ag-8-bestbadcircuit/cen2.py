#!/usr/bin/env python3
"""cen2.py (ag-8-bestbadcircuit): the census of 4-point circuits with 4 + m gates (count G) over GF(p), special against class.
Input: s<m>_<p>_<tau>.txt (p-0's mincirc_sets: every set of m helper points after which the four rows of K (x) K are made,
K = [[1,1],[1,tau]]) and s<m-1>_... (to drop quickly the sets that contain a shorter circuit).
A set is IRREDUNDANT if no helper can be left out.  WIRING = for each of the 4 + m non-input points, which two points it reads
(every acyclic choice; at most CAP per set).  SHAPE = wiring with names forgotten: least, over the 4! renamings of the inputs, of
the sorted list of (kind, expression down to the inputs).
Step 1: generic tau: all shapes G.   Step 2: tau = -1: a helper set is OF THE CLASS if one of its wirings has its shape in G,
SPECIAL if none has.  Sets are taken in random order inside a time budget; the fraction done is printed.
usage: cen2.py p m tauH tauG secondsG secondsH [seed]"""
import sys, itertools, os, random, time, pickle
p = int(sys.argv[1]); m = int(sys.argv[2]); tH = int(sys.argv[3]); tG = int(sys.argv[4]); secG = float(sys.argv[5]); secH = float(sys.argv[6])
random.seed(int(sys.argv[7]) if len(sys.argv) > 7 else 1); CAP = 4000
NP = 4 + m + 4; T0 = 4 + m
def canon_pt(v):
    f = next(x for x in v if x); iv = pow(f, -1, p); return tuple(x * iv % p for x in v)
def rows(tau): return [tuple(pow(tau, bin(w & x).count('1'), p) for x in range(4)) for w in range(4)]
E = [tuple(int(i == j) for j in range(4)) for i in range(4)]
PERMS = list(itertools.permutations(range(4)))
PAIRS = [(a, b) for a in range(NP) for b in range(a + 1, NP)]
def load(m_, tau):
    fn = 's%d_%d_%d.txt' % (m_, p, tau)
    return [tuple(sorted(tuple(int(x) for x in s.split(',')) for s in line.split()[1:])) for line in open(fn) if line.startswith('SET')]
def options(pts):
    """for each non-input point the pairs it is collinear with (rank <= 2: the four 3 x 3 minors vanish)."""
    opts = {c: [] for c in range(4, NP)}
    for a, b in PAIRS:
        u = pts[a]; v = pts[b]
        l01 = u[0] * v[1] - u[1] * v[0]; l02 = u[0] * v[2] - u[2] * v[0]; l03 = u[0] * v[3] - u[3] * v[0]
        l12 = u[1] * v[2] - u[2] * v[1]; l13 = u[1] * v[3] - u[3] * v[1]; l23 = u[2] * v[3] - u[3] * v[2]
        for c in range(4, NP):
            if c == a or c == b: continue
            w = pts[c]
            if (w[0] * l12 - w[1] * l02 + w[2] * l01) % p: continue
            if (w[0] * l13 - w[1] * l03 + w[3] * l01) % p: continue
            if (w[0] * l23 - w[2] * l03 + w[3] * l02) % p: continue
            if (w[1] * l23 - w[2] * l13 + w[3] * l12) % p: continue
            opts[c].append((a, b))
    return opts
def reach(opts, drop=None):
    done = set(range(4)); ch = True
    while ch:
        ch = False
        for c in range(4, NP):
            if c in done or c == drop: continue
            for a, b in opts[c]:
                if a in done and b in done: done.add(c); ch = True; break
    return done
TARG = set(range(T0, NP))
def irredundant(opts):
    for h in range(4, T0):
        if TARG <= reach(opts, drop=h): return False
    return True
def wirings(opts):
    """acyclic choices, by depth-first search in every order of making the points (a wiring is produced once: the choice dict)."""
    out = set(); nodes = list(range(4, NP))
    cnt = [0]
    for choice in itertools.product(*[opts[c] for c in nodes]):
        cnt[0] += 1
        if cnt[0] > 200000: break
        w = dict(zip(nodes, choice)); done = set(range(4)); ch = True
        while ch:
            ch = False
            for c in nodes:
                if c not in done and w[c][0] in done and w[c][1] in done: done.add(c); ch = True
        if len(done) == NP:
            out.add(choice)
            if len(out) >= CAP: break
    return [dict(zip(nodes, c)) for c in out]
def canon_shape(w):
    best = None
    for pi in PERMS:
        lab = {i: 'abcd'[pi[i]] for i in range(4)}
        def ex(h):
            if h in lab: return lab[h]
            a, b = ex(w[h][0]), ex(w[h][1])
            lab[h] = '(' + (a + b if a < b else b + a) + ')'
            return lab[h]
        key = tuple(sorted(('T' if h >= T0 else 'h') + ex(h) for h in range(4, NP)))
        if best is None or key < best: best = key
    return best
def prep(tau):
    R = [canon_pt(r) for r in rows(tau)]
    sets = sorted(set(load(m, tau))); small = set(load(m - 1, tau))
    left = [S for S in sets if not any(tuple(x for j, x in enumerate(S) if j != i) in small for i in range(m))]
    random.shuffle(left)
    return R, sets, left
def show(pts, w):
    return ' | '.join('%s%d=%s<-(%d,%d)' % ('h' if n < T0 else 'T', n, ','.join(map(str, pts[n])), w[n][0], w[n][1]) for n in sorted(w))
# ---------- step 1: generic ----------
R, sets, left = prep(tG); t0 = time.time(); G = {}; nirr = 0; done = 0; nw = 0; capped = 0
for S in left:
    if time.time() - t0 > secG: break
    done += 1; pts = E + list(S) + R
    if len(set(pts)) < NP: continue
    opts = options(pts)
    if not irredundant(opts): continue
    nirr += 1; ws = wirings(opts); nw += len(ws); capped += len(ws) >= CAP
    for w in ws:
        c = canon_shape(w)
        if c not in G: G[c] = (pts, w)
print('GENERIC p=%d tau=%d: %d sets, %d after the quick filter, %d of them examined (%.0f s), %d irredundant, %d wirings (%d sets capped), %d shapes'
      % (p, tG, len(sets), len(left), done, time.time() - t0, nirr, nw, capped, len(G)), flush=True)
# ---------- step 2: the transform ----------
R, sets, left = prep(tH); t0 = time.time(); nirr = 0; done = 0; nclass = 0; nspec = 0; capped = 0
SP = {}; HS = {}; CL = {}; HSETS = []
for S in left:
    if time.time() - t0 > secH: break
    done += 1; pts = E + list(S) + R
    if len(set(pts)) < NP: continue
    opts = options(pts)
    if not irredundant(opts): continue
    nirr += 1; ws = wirings(opts); capped += len(ws) >= CAP
    cs = [(canon_shape(w), w) for w in ws]
    for c, w in cs: HS.setdefault(c, (pts, w))
    HSETS.append((S, sorted(set(c for c, w in cs))))
    hit = [c for c, w in cs if c in G]
    if hit:
        nclass += 1
        for c in set(hit): CL[c] = CL.get(c, 0) + 1
    else:
        nspec += 1
        key = min(c for c, w in cs)          # name a special set by its least shape
        if key not in SP: SP[key] = [0, pts, next(w for c, w in cs if c == key), len(cs)]
        SP[key][0] += 1
print('TRANSFORM p=%d tau=%d: %d sets, %d after the quick filter, %d of them examined (%.0f s), %d irredundant (%d capped): %d OF THE CLASS (a wiring whose shape exists at the generic tau), %d SPECIAL (no wiring does)'
      % (p, tH, len(sets), len(left), done, time.time() - t0, nirr, capped, nclass, nspec), flush=True)
print('shapes seen at the transform: %d ; of them also generic: %d ; generic shapes not seen at the transform: %d' % (len(HS), sum(c in G for c in HS), sum(c not in HS for c in G)))
print('\nSPECIAL shapes, one labelled specimen each (points modulo %d; nodes 0-3 inputs, then helpers h, then targets T = rows 00,01,10,11):' % p)
for i, (c, (n, pts, w, nws)) in enumerate(sorted(SP.items(), key=lambda kv: -kv[1][0])):
    print('SP%03d sets=%d wirings_of_specimen=%d' % (i, n, nws)); print('    ' + show(pts, w))
print('\nCOMMON shapes, specimens at the transform (the most frequent 12):')
for i, (c, n) in enumerate(sorted(CL.items(), key=lambda kv: -kv[1])[:12]):
    print('CO%03d sets=%d' % (i, n)); print('    ' + show(*HS[c]))
print('\nshapes absent at the transform, specimens at the generic tau (first 8):')
for i, c in enumerate([c for c in G if c not in HS][:8]):
    print('AB%03d' % i); print('    ' + show(*G[c]))
pickle.dump({'p': p, 'm': m, 'tH': tH, 'tG': tG, 'G': {c: G[c] for c in G}, 'HSETS': HSETS, 'HS': HS}, open('cen2_%d_%d_%d.pkl' % (p, m, tG), 'wb'))
