#!/usr/bin/env python3
"""unitmeter.py  [h-7-unitmeter, 2026-10-11]  Reads the published certificate (read only), writes nothing there.

The published unit read with the wave's meters.  One INVOCATION of the helper circuit is replayed exactly
(rational arithmetic, the same replay as R/tools/gx/gx.py: check1 for the frames, scal for the contents; the
few helper functions are re-typed here so that nothing is imported from the release tree).

Dictionary (stated before measuring).  Registers: 120 x (sources), 120 y (targets), 783 slots (helpers).
Every register holds, at every moment,   frame_P ( sum_t w_t x_t )   applied digit by digit (f digits):
  - P = its current label, a subspace of F_2^9 inside the invocation (dimension d = dim P);
  - w = its x-content, a rational vector over the 120 sources (t = number of non-zeros).
A WIRE of the unit at f digit columns = (register, moment, address a).  As a linear form it is
       (the vector w on the batch index)  (x)  (row a of frame_P, f times)
so it is a PRODUCT across the cut batch | address.  Its non-zeros: written in the inputs  s  = t * 2^(d f),
written in the outputs s' = t' * 2^((9-d) f); for the x-content t' = t (target S ends with exactly x_S), so
s*s' = t^2 * n: over the limit by the factor t^2, all of it on the batch side.
A BLOCK of rank r on a register = r moves = r*f layers of n gates (G), i.e. r*f*n new wires, all with the w of
that register at that time.  An ADDITION (one term a*u into v) = n gates (G), n new wires.

usage: python3 -I -B unitmeter.py <certificate.json.gz>
"""
import sys, json, gzip, math
from fractions import Fraction as Fr
from collections import Counter, defaultdict

def gate_regs(g):
    if g[0] == "neg":
        return [g[2]], [], []
    if g[0] == "out":
        return [g[2]] + [t for t, _, _ in g[3]] + list(g[4]), [(t, g[2], Fr(a, b)) for t, a, b in g[3]], g[4]
    if g[0] == "in":
        return [g[2]] + [s for s, _, _ in g[3]], [(g[2], s, Fr(a, b)) for s, a, b in g[3]], []
    raise AssertionError("unknown gate kind")

c = json.load(gzip.open(sys.argv[1]))
assert c["format"] == "gcert/1"
h, v, R = c["h"], c["v"], c["R"]
nreg = 2 * v + R
fr = [tuple(f) for f in c["frames"]]
dim = [len(f) for f in fr]
cls = lambda r: "x" if r < v else "y" if r < 2 * v else "s"
cur = list(c["start"])
reg = [({r: Fr(1)} if r < v else {}) for r in range(nreg)]
ver = [0] * nreg                       # version of the wire state (register, frame, content)
reads = Counter()                      # (register, version) -> number of gate terms that read it
blocks = []                            # (class, rank, t at the time, dim before, phase)
adds = Counter()                       # additions (one term each) by (class of source, class of target)
adds_t = []                            # (t of the source, t of the target before, t after)
tmax = Counter()

def climb(r, f, ph):
    o = cur[r]
    if o != f:
        blocks.append((cls(r), dim[f] - dim[o], len(reg[r]), dim[o], ph))
        cur[r] = f
        ver[r] += 1

def axpy(t, s_reg, src, co):
    d = reg[t]
    before = len(d)
    for k, u in src.items():
        w = d.get(k, 0) + co * u
        if w:
            d[k] = w
        else:
            d.pop(k, None)
    ver[t] += 1
    adds[(cls(s_reg) if s_reg is not None else "c", cls(t))] += 1
    adds_t.append((len(src), before, len(d)))
    tmax[cls(t)] = max(tmax[cls(t)], len(d))

def run(gates, ph):
    for g in gates:
        regs, pairs, _ = gate_regs(g)
        for r in regs:
            climb(r, g[1], ph)
        if g[0] == "neg":
            reg[g[2]] = {k: -u for k, u in reg[g[2]].items()}
        elif g[0] == "out":
            src = dict(reg[g[2]])
            for t, a, b in g[3]:
                reads[(g[2], ver[g[2]])] += 1
                axpy(t, g[2], src, Fr(a, b))
        else:
            for s, a, b in g[3]:
                reads[(s, ver[s])] += 1
                axpy(g[2], s, reg[s], Fr(a, b))

run(c["A"], "A")
# the scatter cut: every retained total is copied to a scratch array, the copy comes down to frame 0 (dim f moves)
tot = {}
copy_blocks = []
for k, s, f in c["ret"]:
    assert cur[s] == f
    tot[k] = dict(reg[s])
    copy_blocks.append(("c", dim[f], len(tot[k]), dim[f], "cut"))
scat_reads = Counter()
def scat_row(t):
    sc = c["scat"]
    if "table" in sc:
        return [(k, Fr(a, b)) for k, a, b in sc["table"][t]]
    sin, sout = Fr(*sc["inside"]), Fr(*sc["outside"])
    return [(k, sin if c["ports"][t] >> k & 1 else sout) for k in range(h)]
for t in range(v):
    for k, co in scat_row(t):
        if co == 0:
            continue
        scat_reads[k] += 1
        axpy(v + t, None, tot[k], co)
y_after_scatter = Counter(len(reg[v + t]) for t in range(v))
run(c["B"], "B")
for r in range(nreg):
    climb(r, c["final"][r], "final")
assert all(reg[t] == {t: 1} for t in range(v)) and all(reg[v + t] == {t: 1} for t in range(v)), "scalar identity"
blocks += copy_blocks

def bucket(t):
    for lo, hi in ((0, 0), (1, 1), (2, 2), (3, 4), (5, 8), (9, 16), (17, 32), (33, 64), (65, 10**6)):
        if lo <= t <= hi:
            return "%d" % lo if lo == hi else "%d-%d" % (lo, hi)

print("certificate: h=%d v=%d R=%d  (registers: %d x, %d y, %d slots), replayed exactly, scalar identity holds" % (h, v, R, v, v, R))
tb = defaultdict(lambda: [0, 0])
order = ["0", "1", "2", "3-4", "5-8", "9-16", "17-32", "33-64", "65-1000000"]
for k, r, t, d, ph in blocks:
    e = tb[(k, bucket(t))]
    e[0] += 1; e[1] += r
print("\n(1) blocks and moves of ONE invocation, by class and by t = number of sources the register mixes at that time")
print("    class   " + "".join("%12s" % ("t=" + b) for b in order) + "       total")
tot_moves = 0
for k in "xysc":
    row = [tb[(k, b)] for b in order]
    print("    %s blocks" % k + "".join("%12d" % e[0] for e in row) + "%12d" % sum(e[0] for e in row))
    print("    %s moves " % k + "".join("%12d" % e[1] for e in row) + "%12d" % sum(e[1] for e in row))
    tot_moves += sum(e[1] for e in row)
print("    all moves of one invocation: %d (certificate N = %d, of which the copies cst = %d)" % (tot_moves, c["N"], c["cst"]))
mix = sum(r for k, r, t, d, ph in blocks if t >= 2)
one = sum(r for k, r, t, d, ph in blocks if t == 1)
zero = sum(r for k, r, t, d, ph in blocks if t == 0)
bud = sum(r * math.log2(t) for k, r, t, d, ph in blocks if t >= 2)
share = sum(r * (t - 1) for k, r, t, d, ph in blocks if t >= 2)
print("    moves on a single source (t=1): %d;  on a mixture (t>=2): %d;  on a register with no x-content (t=0): %d" % (one, mix, zero))
print("    sum over mixture moves of log2 t = %.1f   (the L2 budget of these wires, per f*n, is this number)" % bud)
print("    sum over mixture moves of (t-1) = %d   (moves that the sharing would save if nothing had to be undone)" % share)
print("    largest t ever held: " + ", ".join("%s %d" % (k, tmax[k]) for k in "xys") + "; the 8 totals mix " + str(sorted(len(tot[k]) for k in tot)))
print("    y registers right after the scatter mix: " + str(sorted(y_after_scatter.items())))
print("    mean rank of a block by t: " + ", ".join("t=%s: %.2f" % (b, sum(tb[(k, b)][1] for k in "xysc") / max(1, sum(tb[(k, b)][0] for k in "xysc"))) for b in order))
dd = defaultdict(lambda: [0, 0])
for k, r, t, d, ph in blocks:
    if t >= 2:
        e = dd[d]; e[0] += r; e[1] += r * math.log2(t)
print("    mixture moves by the dimension d of the label BEFORE the block: " + ", ".join("d=%d: %d" % (d, dd[d][0]) for d in sorted(dd)))

print("\n(2) additions of ONE invocation (one term a*u into v = n gates (G); sign changes are free in (G))")
na = sum(adds.values())
print("    by (source class -> target class): " + ", ".join("%s->%s %d" % (a, b, n) for (a, b), n in sorted(adds.items())) + ";  total %d" % na)
mixadds = sum(1 for a, b, e in adds_t if e >= 2)
print("    additions whose result is a mixture (t>=2): %d; whose result is a single source or empty: %d" % (mixadds, na - mixadds))
canc = sum(1 for a, b, e in adds_t if e < max(a, b))
print("    additions that CANCEL (result mixes fewer sources than its larger operand): %d" % canc)

print("\n(3) fan-out: how many addition terms read one wire state (register at one frame with one content)")
fo = Counter(reads.values())
print("    histogram {reads: states}: " + str(sorted(fo.items())))
print("    each scratch copy of a total is read by: " + str(sorted(scat_reads.values())) + " targets")
top = sorted(reads.items(), key=lambda kv: -kv[1])[:5]
print("    most-read register states inside the gate lists: " + ", ".join("%s%d read %d times" % (cls(r), r, n) for (r, _), n in top))

# ---- the unit: five invocations + the twins' idle blocks ----
W, m = 4 * v + R, 5 * h
idle = 2 * v * ((2 * (h - 1) + 4) + 2 * (h - 1) + (h - 1) + 4)
unit_moves = 5 * tot_moves + idle
Dd = W * m - unit_moves
A_unit = 5 * na
print("\n(4) one UNIT = five invocations + idle blocks of the twins (as R/tools/whatif_copies.py builds it)")
print("    W = %d arrays, m = %d, plain %d moves, unit %d moves, D = %d moves saved" % (W, m, W * m, unit_moves, Dd))
print("    additions per unit (five invocations; the free gates between twins are NOT in the certificate): >= %d" % A_unit)
print("    count (G), arrays of n = 2^(%d f) points, blocks done by the textbook:" % m)
print("       textbook  W*m*f*n = %d f n ;  unit  (%d f + %d) n ;  saved  (%d f - %d) n" % (W * m, unit_moves, A_unit, Dd, A_unit))
print("       first f with a positive saving: %d  (arrays of 2^%d points)" % (A_unit // Dd + 1, m * (A_unit // Dd + 1)))
print("    over-limit wires (t>=2) per unit: (%d f + %d) n ;  L1 ratio saved/over-limit -> %d/%d = %.5f as f grows" % (5 * mix, 5 * mixadds, Dd, 5 * mix, Dd / (5 * mix)))
print("    L2 budget per unit: (1/2) sum log2(t^2) = %.0f f n ;  saved/budget -> %.6f" % (5 * bud, Dd / (5 * bud)))
print("    share count per unit: %d ;  D / share = %.6f" % (5 * share, Dd / (5 * share)))
