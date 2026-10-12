#!/usr/bin/env python3
"""unit2adic.py [u-5-unit2adic, 2026-10-11]  Reads the published certificate (read only).  Exact: fractions and whole numbers.

ONE invocation of the published unit written as ONE gate list (G) on a single array, f = 1 digit column:
  array = (register index r, the batch side) x (address a in F_2^h);  n = (number of registers) * 2^h points.
  Inputs: every register at frame 0 holding its own value (FULL contents are tracked, not only the 120 sources).
  A register whose start frame is not 0 (the x registers start at <port>) first gets a PROLOGUE of moves from frame 0.
Gates:
  move up   U -> U + z on register r : 2^h gates, gate at address a reads the wires (r, a) and (r, a + z);
  move down U + z -> U (only the scratch copies of the totals): 2^h gates, same parents;
  addition  v += c * u at a common frame : 2^h gates, gate at address a reads (u, a) and (v, a).
Dictionary (h-7): the wire (r, a) at frame U with content w is  w (x) (row a of frame_U);  row a is supported on the coset a + U
with entries of one modulus, so its primitive form modulo (1 + i) is the indicator of the coset.  Hence
  CLASS of a wire = (B, a + U),  B = the set of registers on which w has its least power of 2  (primitive form of w modulo 2).
All 2^h addresses of a layer behave alike, so the meter works on GROUPS (B, U): a group is 2^(h - dim U) classes, each class
holding 2^(dim U) wires of the layer.
  survivors of a layer = number of new classes;  dead = the rest.
  kind: move up = J (two disjoint cosets joined);  move down = Q (parents in one coset, result in a smaller one);
        addition: by the three batch classes (J / S / Q / E), and J is split into disjoint / nested / crossing parents.
  order of a dead gate: 1 if only the class repeats; m >= 2 if an earlier wire at the SAME frame and address has a content
        congruent to an odd multiple of w modulo 2^m (cap 6; exact copies give 6).
usage: python3 -I -B unit2adic.py <certificate.json.gz> [pairs]     ('pairs' = also count pairs of classes, slow)
"""
import sys, json, gzip, math
from fractions import Fraction as Fr
from collections import Counter, defaultdict

c = json.load(gzip.open(sys.argv[1]))
PAIRS = "pairs" in sys.argv[2:]
EMPTY = "empty" in sys.argv[2:]      # helpers start with nothing (the certificate checker's reading); default: every register holds its own value
h, v, R = c["h"], c["v"], c["R"]
nreg = 2 * v + R
NA = 1 << h
fr = [tuple(f) for f in c["frames"]]
kcls = lambda r: "x" if r < v else "y" if r < 2 * v else "s" if r < nreg else "c"

# ---------- subspaces of F_2^h as reduced bases ----------
def reduce_vec(x, basis):            # basis: dict leading bit -> vector (fully reduced not needed)
    while x:
        l = x.bit_length() - 1
        b = basis.get(l)
        if b is None: return x
        x ^= b
    return 0
def rref(vecs):
    basis = {}
    for x in vecs:
        x = reduce_vec(x, basis)
        if x: basis[x.bit_length() - 1] = x
    # full reduction
    ks = sorted(basis)
    for i, l in enumerate(ks):
        for l2 in ks[i + 1:]:
            if basis[l2] >> l & 1: basis[l2] ^= basis[l]
    return tuple(sorted(basis.values()))
def flag(o, f):
    """chain of reduced bases from span(o) up to span(f), one dimension at a time; None if span(o) is not inside span(f)"""
    bo = {x.bit_length() - 1: x for x in rref(o)}
    bf = {x.bit_length() - 1: x for x in rref(f)}
    if any(reduce_vec(x, dict(bf)) for x in o): return None
    cur = list(o); chain = [rref(cur)]
    for x in f:
        if reduce_vec(x, {y.bit_length() - 1: y for y in rref(cur)}):
            cur.append(x); chain.append(rref(cur))
    assert len(chain[-1]) == len(rref(f))
    return chain

# ---------- contents ----------
def val2(q):
    n, d, k = q.numerator, q.denominator, 0
    while n % 2 == 0: n //= 2; k += 1
    while d % 2 == 0: d //= 2; k -= 1
    return k
CAP = 6; MOD = 1 << CAP
def canon(w):
    """(B as frozenset, B as bit mask, [canonical form modulo 2^m for m = 1..CAP])"""
    if not w: return frozenset(), 0, [()] * CAP
    m0 = min(val2(q) for q in w.values())
    items = []
    for k in sorted(w):
        q = w[k] / Fr(2) ** m0
        items.append((k, q.numerator * pow(q.denominator, -1, MOD) % MOD))
    lead = next(p for k, p in items if p & 1); inv = pow(lead, -1, MOD)
    items = [(k, p * inv % MOD) for k, p in items]
    B = frozenset(k for k, p in items if p & 1)
    mask = 0
    if PAIRS:
        for k in B: mask |= 1 << k
    else:
        mask = hash(B)                       # lean mode: a 64-bit hash stands for the class (used only to count distinct classes)
    forms = [tuple((k, p % (1 << m)) for k, p in items if p % (1 << m)) for m in range(1, CAP + 1)]
    if not PAIRS: forms = [hash(f) for f in forms]
    return B, mask, forms

# ---------- state ----------
reg = [({} if (EMPTY and r >= 2 * v) else {r: Fr(1)}) for r in range(nreg)]          # FULL contents unless EMPTY
curU = [() for r in range(nreg)]                  # reduced basis of the current subspace
curF = [0] * nreg                                 # current frame index in the table (after prologue = start)
assert fr[0] == ()
seen = [set() for _ in range(CAP + 1)]            # seen[m]: (U, canonical form modulo 2^m)
groups = {}                                       # (Bmask, U) -> index of first layer
group_list = []                                   # (Bmask, U, layer index)
layers = []                                       # dict per layer
tot = dict(gates=0, surv=0, dead=0)
kinds = Counter(); orders = Counter(); first = {}
bkinds = Counter(); bfirst = {}; free = Counter(); tcount = Counter(); exact = set()                   # batch shadow (one gate per addition term)
bseen = [set() for _ in range(CAP + 1)]; bclasses = {}
ledger = []
nonnested = 0

def note_first(tag, desc):
    if tag not in first: first[tag] = (len(layers), desc)

def emit(kind, r, U, w, desc, parents):
    """one layer of 2^h gates whose results are the wires of register r at subspace U with content w"""
    if not w:
        free["moves on an empty register (no wire)"] += 1
        return frozenset(), 0
    B, mask, forms = canon(w)
    d = len(U)
    if kind == "copy":
        lead = w[min(w)]; exact.add((U, hash(tuple(sorted((k, q / lead) for k, q in w.items())))))
        for m in range(1, CAP + 1): seen[m].add((U, forms[m - 1]))
        free["scaled copies into an empty register (free in G)"] += 1
        return B, mask
    o = 0
    for m in range(1, CAP + 1):
        if (U, forms[m - 1]) in seen[m]: o = m
        else: break
    for m in range(1, CAP + 1): seen[m].add((U, forms[m - 1]))
    lead = w[min(w)]; ex = (U, hash(tuple(sorted((k, q / lead) for k, q in w.items()))))
    if o >= 2: free["layers of order above 1 whose content is exactly a scalar multiple of one held before at that label" if ex in exact else "layers of order above 1 that are NOT exact repeats"] += 1
    exact.add(ex)
    if o == 0:
        s = NA >> d
        group_list.append((mask, U, len(layers)))
        dd = NA - s
        if dd: orders[1] += dd
    else:
        s = 0; dd = NA; orders[o] += NA
        if o >= 2: note_first("dead gate of order above 1", desc + " | order %d" % o)
    tot["gates"] += NA; tot["surv"] += s; tot["dead"] += dd
    kinds[kind] += NA
    if kind.startswith("Q"): note_first("Q gate", desc)
    if kind == "E": note_first("E gate", desc)
    if kind == "J cross": note_first("J gate whose parents overlap without nesting (a join that cancels modulo 2)", desc)
    if kind == "J nested": note_first("J gate whose parents are nested (result = their difference modulo 2)", desc)
    layers.append((kind, r, d, len(w), s, dd, o))
    if kind == "J move": tcount[len(w)] += 1
    return B, mask

def sset(B, lim=14):
    L = sorted(B)
    return "{" + ",".join(kcls(k) + str(k if k < v else k - v if k < 2 * v else k - 2 * v) for k in L[:lim]) + (",... (%d)" % len(L) if len(L) > lim else "") + "}"

def setU(r, U, w_init=True):
    pass

def climb(r, f, ph):
    """bring register r from its current subspace to frame f, one move per dimension"""
    global nonnested
    if curF[r] == f: return
    ch = flag(curU[r], fr[f]) if len(fr[f]) >= len(curU[r]) else None
    if ch is None:
        nonnested += 1
        raise AssertionError("frame change that is not an inclusion: register %d, %s -> %s" % (r, curU[r], fr[f]))
    B = canon(reg[r])[0]
    for a, b in zip(ch, ch[1:]):
        emit("J move", r, b, reg[r], "%s: move up on %s%d, dim %d -> %d, content class %s (t=%d); parents: the wires (r, a) and (r, a+z), classes (B, a+U) and (B, a+z+U)"
             % (ph, kcls(r), r, len(a), len(b), sset(B), len(reg[r])), None)
    curU[r] = ch[-1]; curF[r] = f

def addkind(Bt, Bs, Bn):
    if Bt == Bs == Bn: return "E"
    if Bt == Bs: return "Q add"
    if Bn == Bt or Bn == Bs: return "S"
    if not (Bt & Bs): return "J disjoint"
    if Bt <= Bs or Bs <= Bt: return "J nested"
    return "J cross"

def xcount(w): return sum(1 for k in w if k < v)

def axpy(t, s_name, src, co, ph, U):
    d = reg[t]
    Bt = canon(d)[0]; Bs = canon(src)[0]
    before = (len(d), xcount(d))
    for k, u in src.items():
        w = d.get(k, 0) + co * u
        if w: d[k] = w
        else: d.pop(k, None)
    Bn = canon(d)[0]
    kd = "copy" if before[0] == 0 else addkind(Bt, Bs, Bn)
    if not d: kd = "zero"
    desc = "%s: addition %s%d += (%s) * %s at dim %d | classes: target %s, source %s, result %s" % (ph, kcls(t), t, co, s_name, len(U), sset(Bt), sset(Bs), sset(Bn))
    emit(kd, t, U, d, desc, None)
    if kd in ("copy", "zero"):
        ledger.append((ph, s_name, "%s%d" % (kcls(t), t), len(U), len(src), xcount(src), before[0], before[1], len(d), xcount(d), kd, -1)); return
    # batch shadow: one gate per addition term, frames forgotten
    _, mask, forms = canon(d)
    o = 0
    for m in range(1, CAP + 1):
        if forms[m - 1] in bseen[m]: o = m
        else: break
    for m in range(1, CAP + 1): bseen[m].add(forms[m - 1])
    bkinds[kd] += 1; bkinds["new" if o == 0 else "dead order %d" % o] += 1
    if o == 0: bclasses[mask] = len(ledger)
    ledger.append((ph, s_name, "%s%d" % (kcls(t), t), len(U), len(src), xcount(src), before[0], before[1], len(d), xcount(d), kd, o))

for r in range(nreg):
    if not reg[r]: continue
    _, _, forms = canon(reg[r])
    exact.add(((), hash(((r, Fr(1)),))))
    for m in range(1, CAP + 1): seen[m].add(((), forms[m - 1])); bseen[m].add(forms[m - 1])
    mk = canon(reg[r])[1]
    group_list.append((mk, (), -1)); bclasses[mk] = -1


# prologue
for r in range(nreg):
    if c["start"][r] != 0: climb(r, c["start"][r], "prologue")
n_prologue = len(layers)

def gate_regs(g):
    if g[0] == "neg": return [g[2]]
    if g[0] == "out": return [g[2]] + [t for t, _, _ in g[3]] + list(g[4])
    return [g[2]] + [s for s, _, _ in g[3]]

def run(gates, ph):
    for g in gates:
        for r in gate_regs(g): climb(r, g[1], ph)
        U = rref(fr[g[1]])
        if g[0] == "neg":
            reg[g[2]] = {k: -u for k, u in reg[g[2]].items()}
        elif g[0] == "out":
            src = dict(reg[g[2]])
            for t, a, b in g[3]: axpy(t, "%s%d" % (kcls(g[2]), g[2]), src, Fr(a, b), ph, U)
        else:
            for s, a, b in g[3]: axpy(g[2], "%s%d" % (kcls(s), s), reg[s], Fr(a, b), ph, U)

run(c["A"], "A")
n_A = len(layers)
# the cut: copies of the totals come down to frame 0
totc = {}
for k, s, f in c["ret"]:
    assert curF[s] == f
    totc[k] = dict(reg[s])
    ch = flag((), fr[f])
    B = canon(totc[k])[0]
    for a, b in zip(ch[::-1], ch[::-1][1:]):
        emit("Q move down", nreg + k, b, totc[k], "cut: move DOWN on the scratch copy of total %d, dim %d -> %d, content class %s (t=%d); parents: the wires (copy, a) and (copy, a+z), both of class (B, a+U+z)"
             % (k, len(a), len(b), sset(B), len(totc[k])), None)
n_cut = len(layers)
def scat_row(t):
    sc = c["scat"]
    if "table" in sc: return [(k, Fr(a, b)) for k, a, b in sc["table"][t]]
    sin, sout = Fr(*sc["inside"]), Fr(*sc["outside"])
    return [(k, sin if c["ports"][t] >> k & 1 else sout) for k in range(h)]
for t in range(v):
    assert curF[v + t] == 0
    for k, co in scat_row(t):
        if co: axpy(v + t, "copy%d" % k, totc[k], co, "scatter", ())
n_scat = len(layers)
after_scatter = [dict(reg[v + t]) for t in range(v)]
run(c["B"], "B")
n_B = len(layers)
for r in range(nreg): climb(r, c["final"][r], "final")
n_end = len(layers)

# ---------- what the invocation computes ----------
okx = all(reg[t] == {t: 1} for t in range(v))
oky = all(reg[v + t] == {t: 1, v + t: 1} for t in range(v))
oks = all(reg[r] == {r: 1} for r in range(2 * v, nreg))
print("helpers at the end: %d hold nothing; contents held by the others, x / y / helper values: %s" % (sum(1 for r in range(2 * v, nreg) if not reg[r]), [sum(1 for r in range(2 * v, nreg) for q in reg[r] if lo <= q < hi) for lo, hi in ((0, v), (v, 2 * v), (2 * v, nreg))]))
print("certificate h=%d v=%d R=%d; registers %d; addresses per register 2^%d = %d; n = %d points" % (h, v, R, nreg, h, NA, nreg * NA))
print("FULL contents replayed.  At the end: x_t holds x_t alone: %s;  y_t holds y_t + x_t: %s;  every helper holds its own value alone: %s" % (okx, oky, oks))
if not oks:
    bad = [(r, len(reg[r])) for r in range(2 * v, nreg) if reg[r] != {r: 1}]
    print("   helpers that end with something else: %d, e.g. %s" % (len(bad), bad[:5]))
print("final frames: x dim %s, y dim %s, helpers dim %s; port_t outside the final frame of y_t for all t: %s" % (
    sorted({len(curU[t]) for t in range(v)}), sorted({len(curU[v + t]) for t in range(v)}), sorted({len(curU[r]) for r in range(2 * v, nreg)}),
    all(reduce_vec(c["ports"][t], {x.bit_length() - 1: x for x in curU[v + t]}) for t in range(v))))

def report(lo, hi, name):
    L = layers[lo:hi]
    g = len(L) * NA; s = sum(x[4] for x in L); dd = sum(x[5] for x in L)
    kk = Counter(); oo = Counter()
    for x in L:
        kk[x[0]] += NA
        if x[6] == 0:
            if NA - x[4]: oo[1] += NA - x[4]
        else: oo[x[6]] += NA
    print("  %-38s layers %6d  gates %9d  survivors %8d  dead %9d | kinds %s | dead by order %s" % (name, len(L), g, s, dd, dict(sorted(kk.items())), dict(sorted(oo.items()))))

print("\n(1) THE GATE LIST, one layer = 2^h = %d gates (G)" % NA)
report(0, n_prologue, "prologue (x: 0 -> <port>)")
report(n_prologue, n_A, "phase A")
report(n_A, n_cut, "cut (copies of the totals come down)")
report(n_cut, n_scat, "scatter")
report(n_scat, n_B, "phase B")
report(n_B, n_end, "final blocks")
report(0, n_end, "ALL")
nin = sum(1 for r in range(nreg) if not (EMPTY and r >= 2 * v))
n = nin * NA
print("\nreading: %s; input registers %d; free events: %s" % ("helpers start EMPTY" if EMPTY else "every register holds its own value", nin, dict(free)))
ncls = sum(NA >> len(U) for (_, U, _) in group_list)
print("\n(2) FIVE NUMBERS, whole invocation, n = %d" % n)
print("  classes: %d   (2n - 1 = %d; groups (B, U): %d; distinct B: %d; distinct U: %d)" % (ncls, 2 * n - 1, len(group_list), len({g[0] for g in group_list}), len({g[1] for g in group_list})))
print("  survivors (= classes - n): %d   against n - 1 = %d" % (tot["surv"], n - 1))
print("  Q gates: %d  (move down %d, additions %d);  E gates: %d" % (kinds["Q move down"] + kinds["Q add"], kinds["Q move down"], kinds["Q add"], kinds["E"]))
print("  dead gates of order above 1: %d  (by order: %s)" % (sum(q for o, q in orders.items() if o >= 2), dict(sorted(orders.items()))))
print("  dead gates: %d   against (n/2) log2 n = %.0f  and against the plain schedule's dead gates" % (tot["dead"], n / 2 * math.log2(n)))
plain_moves = sum(len(curU[r]) for r in range(nreg))
plain_surv = sum((NA >> 1) - (NA >> (len(curU[r]) + 1)) * 2 // 2 * 0 for r in range(nreg))
ps = sum(sum(NA >> dd for dd in range(1, len(curU[r]) + 1)) for r in range(nreg))
print("  plain schedule (every register alone from frame 0 to its final frame): %d moves = %d gates, survivors %d, dead %d" % (plain_moves, plain_moves * NA, ps, plain_moves * NA - ps))
print("  this gate list: %d gates = %d move layers up + %d down + %d addition layers" % (tot["gates"], sum(1 for x in layers if x[0] == "J move"), sum(1 for x in layers if x[0] == "Q move down"), sum(1 for x in layers if x[0] not in ("J move", "Q move down"))))
print("  kinds of all gates: %s" % dict(sorted(kinds.items())))

print("\n(3) FIRST LAYER IN PROGRAM ORDER THAT BREAKS EACH PROPERTY (layer index; phases end at %s)" % [n_prologue, n_A, n_cut, n_scat, n_B, n_end])
for tag, (i, desc) in sorted(first.items(), key=lambda kv: kv[1][0]):
    print("  [%6d] %s\n           %s" % (i, tag, desc))

print("\n(4) BATCH SHADOW (frames forgotten; one gate per addition term; inputs = the %d registers)" % nreg)
print("  gates %d; kinds and new/dead: %s" % (len(ledger), dict(sorted(bkinds.items()))))
print("  classes: %d  against 2 * %d - 1 = %d" % (len(bclasses), nreg, 2 * nreg - 1))
bm = sorted(bclasses)
if PAIRS:
    cross = nest = 0
    for i, a in enumerate(bm):
        for b in bm[i + 1:]:
            x = a & b
            if x:
                if x == a or x == b: nest += 1
                else: cross += 1
    print("  pairs of batch classes: nested %d, overlapping without nesting %d, of %d" % (nest, cross, len(bm) * (len(bm) - 1) // 2))

# scatter alone
print("\n(5) THE SCATTER ALONE (the %d targets right after the scatter, full contents)" % v)
SB = [canon(w)[1] for w in after_scatter]
sizes = Counter(bin(b).count("1") for b in SB)
cr = sum(1 for i in range(v) for j in range(i) if SB[i] & SB[j] and SB[i] & SB[j] not in (SB[i], SB[j]))
print("  classes: %d distinct of %d, sizes %s; own value y_t in its class: %s; source x_t in its class: %s" % (len(set(SB)), v, dict(sizes), any(SB[t] >> (v + t) & 1 for t in range(v)), any(SB[t] >> t & 1 for t in range(v))))
print("  pairs overlapping without nesting: %d of %d;  2-adic values of the entries of one row: %s" % (cr, v * (v - 1) // 2, dict(Counter(val2(q) for q in after_scatter[0].values()))))
L = [x for x in ledger if x[0] == "scatter" and x[11] >= 0]
print("  scatter gates (batch shadow): %d; kinds %s; new/dead %s" % (len(L), dict(Counter(x[10] for x in L)), dict(Counter("new" if x[11] == 0 else "dead order %d" % x[11] for x in L))))

# ledger
print("\n(6) LEDGER: every addition term, number of contents on both sides before and after (full contents; x-only in the file)")
rise = Counter(); big = 0.0; clip = 0.0
hist = Counter()
for (ph, sname, tname, d, ts, tsx, tb, tbx, ta, tax, kd, o) in ledger:
    if kd in ("copy", "zero"): continue
    lo = min(ts, tb); r = math.log2(ta / lo) if ta > lo else 0.0
    hist[(ph, "cancel" if ta < max(ts, tb) else "grow" if ta > max(ts, tb) else "same")] += 1
    big = max(big, r); rise[ph] += r
print("  additions by phase and effect on the number of contents: %s" % dict(sorted(hist.items())))
print("  sum over additions of log2(after / smaller side), by phase: %s; largest single rise %.2f" % ({k: round(x, 1) for k, x in rise.items()}, big))
upm = sum(1 for x in layers if x[0] == "J move")
print("  a-2's count for this gate list (per 2^h gates): moves up %d (rise 1 each) + additions %.1f = %.1f; needed for the registers' final frames: %d" % (upm, sum(rise.values()), upm + sum(rise.values()), plain_moves))
with open(sys.argv[1].split("/")[-1].split(".")[0] + (".empty" if EMPTY else "") + ".ledger.tsv", "w") as fo:
    fo.write("phase\tsource\ttarget\tframe_dim\tt_source\tt_source_x\tt_target_before\tt_target_before_x\tt_target_after\tt_target_after_x\tkind\tbatch_order\n")
    for row in ledger: fo.write("\t".join(str(z) for z in row) + "\n")

# ---------- pairs of classes ----------
if PAIRS:
    print("\n(7) PAIRS OF CLASSES THAT OVERLAP WITHOUT NESTING, by where the crossing is (groups in program order)")
    def elems(U):
        s = 1
        for x in U:
            t = 0; y = s; i = 0
            # shift every element by xor with x
            e = [j for j in range(NA) if s >> j & 1]
            for j in e: s |= 1 << (j ^ x)
        return s
    Us = {}; Bs = {}
    for (mask, U, li) in group_list:
        if U not in Us: Us[U] = (len(Us), elems(U))
        if mask not in Bs: Bs[mask] = len(Bs)
    byB = defaultdict(list)
    for gi, (mask, U, li) in enumerate(group_list): byB[mask].append((Us[U][0], gi))
    Ul = [None] * len(Us)
    for U, (i, e) in Us.items(): Ul[i] = (e, len(U))
    urel = {}
    def UR(i, j):
        k = (i, j) if i <= j else (j, i)
        r = urel.get(k)
        if r is None:
            ei, di = Ul[k[0]]; ej, dj = Ul[k[1]]
            x = ei & ej
            dx = bin(x).count("1").bit_length() - 1
            code = 1 if di == dj == dx else 2 if dx == di else 3 if dx == dj else 4    # 2: first inside second
            r = urel[k] = (code, NA >> dx)
        if i <= j: return r
        return ((3 if r[0] == 2 else 2 if r[0] == 3 else r[0]), r[1])
    cnt = Counter(); firstp = {}
    Bl = sorted(byB, key=lambda m: min(g for _, g in byB[m]))
    def bump(tag, q, g1, g2):
        cnt[tag] += q
        k = max(g1, g2)
        if tag not in firstp or k < firstp[tag][0]: firstp[tag] = (k, min(g1, g2))
    for i, a in enumerate(Bl):
        la = byB[a]
        # same batch class: address crossing only
        for p in range(len(la)):
            for q in range(p):
                code, w = UR(la[p][0], la[q][0])
                if code == 4: bump("same batch class, frames cross (address side alone)", w, la[p][1], la[q][1])
        for b in Bl[i + 1:]:
            x = a & b
            if not x: continue
            lb = byB[b]
            if x == a or x == b:
                small, large = (la, lb) if x == a else (lb, la)
                for (u1, g1) in small:
                    for (u2, g2) in large:
                        code, w = UR(u1, u2)
                        if code == 4: bump("batch classes nested, frames cross (address side alone)", w, g1, g2)
                        elif code == 3: bump("batch classes nested one way, frames nested the other way (needs both sides)", w, g1, g2)
            else:
                for (u1, g1) in la:
                    for (u2, g2) in lb:
                        code, w = UR(u1, u2)
                        if code == 4: bump("batch classes cross and frames cross", w, g1, g2)
                        else: bump("batch classes cross, frames nested or equal (batch side alone)", w, g1, g2)
    allp = ncls * (ncls - 1) // 2
    print("  all pairs of classes: %d" % allp)
    for tag, q in sorted(cnt.items(), key=lambda kv: -kv[1]):
        g1, g2 = firstp[tag]
        def gd(g):
            mask, U, li = group_list[g]
            B = frozenset(k for k in range(nreg) if mask >> k & 1)
            return "group %d: B=%s at dim %d, first made in layer %d (%s)" % (g, sset(B, 8), len(U), li, layers[li][0] if li >= 0 else "input")
        print("  %12d  %s\n                first pair: %s  x  %s" % (q, tag, gd(g1), gd(g2)))
    print("  total overlapping without nesting: %d" % sum(cnt.values()))
