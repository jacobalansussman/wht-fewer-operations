# e-6-shifts, size pushed once: N = 16 out of 256-point programs.
# The 256-point program is "four passes of the 7-gate 4-point program", one per base-4 digit (1,792 gates, count G);
# this is two levels of the 56-gate program.  x (16 unknowns) is fanned out over the cosets of a 4-dimensional
# subgroup K of the 256 addresses; the 16 answers sit on K-perp.  Collapse, strict mode, greedy with local improvement
# (an upper bound on the true strict minimum).  Exact rationals.
# Prediction to test [derived in e-6.md]: 28*(number of passes that open two new directions) + 16*(passes that open one)
# = 56, 60 or 64, depending only on how K sits relative to the four digits.
import sys, random, time
sys.path.insert(0, "waves/wave-02/e-6-shifts")
import collapse as C
pc = C.pc
def prog256(variants=(0, 0, 0, 0), kern="seven"):
    p = C.Prog(256); w = list(range(256))
    for dgt in range(4):
        sh = 2 * dgt
        for base in range(256):
            if (base >> sh) & 3: continue
            idx = [base | (a << sh) for a in range(4)]
            o = C.h4_seven(p, [w[i] for i in idx], variants[dgt]) if kern == "seven" else C.h4_text(p, [w[i] for i in idx])
            for a in range(4): w[idx[a]] = o[a]
    p.out = {P: w[P] for P in range(256)}; return p
def rank2(vs):
    basis = []
    for v in vs:
        for b in basis: v = min(v, v ^ b)
        if v: basis.append(v)
    return len(basis)
def emb(Pb):
    # K-perp has basis Pb (4 independent 8-bit vectors); pi(p) = (Pb_i . p)_i
    E = []
    for p in range(256):
        s = sum(((pc(Pb[i] & p) & 1) << i) for i in range(4)); E.append(C.unit(16, s))
    outs = {}
    for w in range(16):
        P = 0
        for i in range(4):
            if (w >> i) & 1: P ^= Pb[i]
        outs[P] = w
    return E, outs
def greedy(prog, E, outs, rng, tries=40):
    N = 16
    vals = C.evaluate(prog, E)
    ids = {}
    def cid(v):
        k = C.nkey(v)
        if k is None: return None
        if k not in ids: ids[k] = len(ids)
        return ids[k]
    inp = set(cid(C.unit(N, j)) for j in range(N))
    wid = [cid(v) for v in vals]
    good = all(C.nkey(vals[prog.out[P]]) == C.nkey(C.Hrow(4, w)) for P, w in outs.items())
    want = [wid[prog.out[P]] for P in outs]
    deriv = {}
    for gi_, (a, u, b, v) in enumerate(prog.gates):
        if v is None: continue
        o = wid[prog.n + gi_]; cu = wid[u]; cv = wid[v]
        if o is None or cu is None or cv is None or a.z() or b.z(): continue
        if cu == cv or o == cu or o == cv: continue
        d = (min(cu, cv), max(cu, cv))
        L = deriv.setdefault(o, [])
        if d not in L: L.append(d)
    # every derivation in the list was made by a gate later than the gates that made its arguments, so any choice is acyclic
    def cost(choice):
        seen = set(); st = [w for w in want if w not in inp]
        while st:
            f = st.pop()
            if f in seen or f in inp: continue
            seen.add(f)
            g, h = deriv[f][choice.get(f, 0)]
            st.append(g); st.append(h)
        return len(seen), seen
    choice = {}
    best, seen = cost(choice)
    for _ in range(tries):
        improved = False
        for f in list(seen):
            if len(deriv[f]) < 2: continue
            cur = choice.get(f, 0)
            for alt in range(len(deriv[f])):
                if alt == cur: continue
                choice[f] = alt
                c2, s2 = cost(choice)
                if c2 < best: best, seen, cur, improved = c2, s2, alt, True
                else: choice[f] = cur
        if not improved: break
    return good, len(ids), best
if __name__ == "__main__":
    rng = random.Random(6); t0 = time.time()
    for kern in ("seven", "text"):
        pg = prog256(kern=kern)
        print("256-point program, kernel=%s, gates(G)=%d" % (kern, pg.ngates())); sys.stdout.flush()
        D = [[1 << (2 * d), 2 << (2 * d)] for d in range(4)]
        named = [("diagonal: digit1=digit3, digit2=digit4", [0x11, 0x22, 0x44, 0x88]),
                 ("digit1=digit2, digit3=digit4", [0x05, 0x0A, 0x50, 0xA0]),
                 ("K-perp = digits 1,2 (plain: x on digits 1,2)", [0x01, 0x02, 0x04, 0x08])]
        tests = list(named)
        while len(tests) < (14 if kern == "seven" else 6):
            Pb = [rng.randrange(1, 256) for _ in range(4)]
            if rank2(Pb) == 4: tests.append(("random", Pb))
        for name, Pb in tests:
            # how K sits: pi restricted to the first i digits; pi(e) for a unit address e is the column of the 4x8 matrix Pb
            col = lambda e: sum(((pc(Pb[i] & e) & 1) << i) for i in range(4))
            incr = []; acc = []
            for d in range(4):
                r0 = rank2(acc); acc = acc + [col(D[d][0]), col(D[d][1])]; incr.append(rank2(acc) - r0)
            pred = sum({2: 28, 1: 16, 0: 0}[r] for r in incr) if kern == "seven" else 64
            E, outs = emb(Pb)
            good, ncls, best = greedy(pg, E, outs, rng)
            print("  %-46s K-perp basis %s  new directions per pass %s  predicted %d  collapse(strict, greedy) %d  classes %d  embedding ok=%s  [%.0fs]" % (
                name, [hex(x) for x in Pb], incr, pred, best, ncls, good, time.time() - t0)); sys.stdout.flush()
