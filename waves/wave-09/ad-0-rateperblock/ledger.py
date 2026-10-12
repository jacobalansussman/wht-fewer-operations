#!/usr/bin/env python3
"""ledger.py [ad-0-rateperblock]  Which blocks of the published unit carry its saving, and at what rate per block.

Reads a gcert/1 certificate (read only), replays the frame ids to get the ORDERED block ranks of every register of one
invocation (same replay as R/tools/gx/gxcore.py label_data; the histograms are compared with the stored `blocks`),
builds the unit's block list (5 invocations + the idle blocks of the twins, R/tools/gx/gxunit.py) and prints:
  1. per class: blocks, moves, rank histogram                                    [exact counts, LEGAL unit]
  2. the ledger at the unit's own root z*: every class's charge                  [FLOATS, LEGAL unit]
  3. rates = moves saved / blocks, next to the bar                               [exact fractions printed as floats]
  4. marginal what-ifs (delete or merge one class)                               [FLOATS, WHAT-IF: no network]
Price law (the engine's own): z is the root of  sum over blocks of (rank/m)^z = W ; saving e = 1 - z.
Rewritten (exactly) in moves:   sum over LIVE blocks of [ m (r/m)^z - r ]  +  sum over scratch copies of m (r/m)^z  =  4v
  left: what every block is CHARGED at exponent z (0 at z = 1);  right: the moves the data arrays skip (one each).
First order in e:  charge of a block of rank r = e * r ln(m/r)  ("move-nats" S);  e ~ D / S,  D = 4v - 5 cst.
All roots are FLOATS (bisection)."""
import sys, json, gzip, math
from collections import Counter

def root(blocks, m, W):
    """blocks: iterable of (rank, count). largest e with sum n (r/m)^(1-e) < W"""
    bl = [(r, n) for r, n in blocks if n]
    mom = lambda e: sum(n * (r / m) ** (1 - e) for r, n in bl)
    if mom(0.0) >= W: return 0.0
    lo, hi = 0.0, 1.0
    if mom(hi) < W: return 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if mom(mid) < W: lo = mid
        else: hi = mid
    return lo

def S(blocks, m):      # move-nats
    return sum(n * r * math.log(m / r) for r, n in blocks)
def Q(blocks, m, e):   # exact charge in moves at saving e (live blocks)
    return sum(n * (m * (r / m) ** (1 - e) - r) for r, n in blocks)
def nb(blocks): return sum(n for r, n in blocks)
def mv(blocks): return sum(r * n for r, n in blocks)
def hist(seqs):
    c = Counter()
    for s in seqs:
        for r in s: c[r] += 1
    return sorted(c.items())
def times(bl, k): return [(r, k * n) for r, n in bl]
def bar(m, e): return m ** e / (1 - e) - 1
def barr(m, r, e): return m ** e * r ** (1 - e) - r

def replay(d):
    h, v, R = d["h"], d["v"], d["R"]
    dim = [len(f) for f in d["frames"]]
    n = 2 * v + R
    cur = list(d["start"]); seq = [[] for _ in range(n)]
    def regs(g): return [g[2]] + [t[0] for t in g[3]] + (list(g[4]) if g[0] == "out" else [])
    def climb(r, f):
        if cur[r] != f:
            assert dim[f] > dim[cur[r]]
            seq[r].append(dim[f] - dim[cur[r]]); cur[r] = f
    for g in d["A"]:
        for r in regs(g): climb(r, g[1])
    cop = [dim[f] for _, s, f in sorted(d["ret"])]
    for g in d["B"]:
        for r in regs(g): climb(r, g[1])
    for r, f in enumerate(d["final"]): climb(r, f)
    startdim = [dim[f] for f in d["start"]]
    return seq, cop, startdim

def main(path):
    d = json.load(gzip.open(path)); h, v, R, cst = d["h"], d["v"], d["R"], d["cst"]
    m, W = 5 * h, 4 * v + R
    seq, cop, sd = replay(d)
    xs, ys, ss = seq[:v], seq[v:2 * v], seq[2 * v:]
    Hx, Hy, Hs, Hc = hist(xs), hist(ys), hist(ss), sorted(Counter(cop).items())
    st = {k: sorted((int(r), n) for r, n in d["blocks"][k].items()) for k in "xysc"}
    assert (Hx, Hy, Hs, Hc) == (st["x"], st["y"], st["s"], st["c"]), "replayed histograms differ from the stored ones"
    assert all(sum(s) == h - 1 for s in xs + ys) and sum(cop) == cst
    ext = sum(sd[2 * v:])
    assert sum(map(sum, ss)) + ext == R * h
    idle = [(2 * h + 2, 2 * v), (2 * h - 2, 2 * v), (h - 1, 2 * v), (4, 2 * v)]
    C = {"x-role (5 inv.)": times(Hx, 5), "y-role (5 inv.)": times(Hy, 5), "idle/catch-up": idle,
         "helpers (5 inv.)": times(Hs, 5), "scratch copies (5 inv.)": times(Hc, 5)}
    live = C["x-role (5 inv.)"] + C["y-role (5 inv.)"] + idle + C["helpers (5 inv.)"]
    cps = C["scratch copies (5 inv.)"]
    allb = live + cps
    D = W * m - mv(allb)
    assert D == 4 * v - 5 * cst - 5 * ext, (D, ext)
    e = root(allb, m, W)
    print("=" * 150)
    print("LEGAL UNIT %s\n  h=%d v=%d R=%d cst=%d  m=%d  W=%d arrays (4v=%d data, %d helpers)  D=%d moves saved of %d  (helper start labels above 0: %d moves, counted as moves made)"
          % (path.split("/")[-1], h, v, R, cst, m, W, 4 * v, R, D, W * m, ext))
    print("  root of the law, fill -> infinity: saving e* = %.5e  [FLOAT]" % e)
    print("\n1. CLASSES [exact counts; LEGAL]            blocks   per array   moves    per array  move-nats S   S per array   rank: count")
    arr = {"x-role (5 inv.)": 4 * v, "y-role (5 inv.)": 4 * v, "idle/catch-up": 4 * v, "helpers (5 inv.)": R, "scratch copies (5 inv.)": None}
    for k, bl in C.items():
        a = arr[k]
        print("  %-26s %8d   %9s  %8d   %9s  %11.1f   %9s     %s" % (k, nb(bl), "%.3f" % (nb(bl) / a) if a else "-", mv(bl), "%.3f" % (mv(bl) / a) if a else "-",
              S(bl, m), "%.2f" % (S(bl, m) / a) if a else "-", " ".join("%d:%d" % (r, n) for r, n in bl)))
    data = C["x-role (5 inv.)"] + C["y-role (5 inv.)"] + idle
    print("  %-26s %8d   %9.3f  %8d   %9.3f  %11.1f   %9.2f" % ("DATA ARRAYS (x+y+idle)", nb(data), nb(data) / (4 * v), mv(data), mv(data) / (4 * v), S(data, m), S(data, m) / (4 * v)))
    print("  %-26s %8d   %9.3f  %8d   %9.3f  %11.1f   %9.2f" % ("UNIT", nb(allb), nb(allb) / W, mv(allb), mv(allb) / W, S(allb, m), S(allb, m) / W))
    print("  plain schedule, same arrays: 2 blocks per array (m-1, 1), S per array = %.3f move-nats" % S([(m - 1, 1), (1, 1)], m))

    print("\n2. THE LEDGER AT THE UNIT'S OWN ROOT e* [FLOATS; LEGAL].  Credit: the data arrays skip %d moves (one each).  It is spent on:" % (4 * v))
    tot = 0.0
    for k, bl in C.items():
        q = Q(bl, m, e) + (mv(bl) if k.startswith("scratch") else 0)
        tot += q
        print("  %-26s charge %10.3f moves = %6.2f %% of the credit   (per block %.5f ; first order e*S = %.3f%s)"
              % (k, q, 100 * q / (4 * v), q / nb(bl), e * S(bl, m), " + the copies' own %d moves" % mv(bl) if k.startswith("scratch") else ""))
    print("  %-26s        %10.3f  (must equal 4v = %d)" % ("sum", tot, 4 * v))
    print("  first-order law e ~ D / S(unit) = %d / %.1f = %.5e   (exact root %.5e)" % (D, S(allb, m), D / S(allb, m), e))
    print("  move-nats per move saved: unit %.1f ; data arrays alone %.1f ; the bar 1e-1 allows about %.1f (first order 1/e; exact below)" % (S(allb, m) / D, S(data, m) / (4 * v), 10.0))

    print("\n3. RATES = moves saved / blocks  [exact ratios shown as decimals].  Bar at this width for saving 1e-1, single-move blocks: m^e/(1-e) - 1 = %.3f ; saving 1e-2: %.3f" % (bar(m, 0.1), bar(m, 0.01)))
    print("   rank-aware bar (what ONE block of rank r is charged at saving 1e-1, in moves): " + " ; ".join("r=%d: %.3f" % (r, barr(m, r, 0.1)) for r in sorted({1, 2, 4, h - 1, h, 2 * h - 2, 2 * h + 2})))
    rows = [("LEGAL  unit, all blocks", D, nb(allb), W),
            ("LEGAL  data arrays (credit 4v; x, y and idle blocks)", 4 * v, nb(data), 4 * v),
            ("LEGAL  helpers (credit 0)", 0, nb(C["helpers (5 inv.)"]), R),
            ("LEGAL  scratch copies (credit -5 cst; not arrays)", -5 * cst, nb(cps), 0)]
    for name, cr, n, a in rows:
        print("   %-56s moves saved %6d  blocks %7d : per block %8.4f ; per block beyond one per array %8.4f ; beyond two per array (plain) %8.4f"
              % (name, cr, n, cr / n, cr / (n - a) if n > a else float("nan"), cr / (n - 2 * a) if n > 2 * a else float("nan")))
    print("   gross view [read: R/tools/gen/foldlib.py, list B2u]: every data array makes 5 stage climbs of h-1 (role or idle: 5 directions left out) and one catch-up block of 4 (4 of them paid back);")
    print("   so the 10v role climbs leave out 10v moves, and the idle class (10v idle stage climbs and the 4v catch-up blocks, merged as published) nets 10v - 16v = -6v:")
    for k in ("x-role (5 inv.)", "y-role (5 inv.)"):
        print("   LEGAL  %-22s gross moves skipped %5d  blocks %6d : %.4f per block" % (k, 5 * v, nb(C[k]), 5 * v / nb(C[k])))
    print("   LEGAL  %-22s gross moves skipped %5d  blocks %6d : %.4f per block" % ("idle/catch-up", -6 * v, nb(idle), -6 * v / nb(idle)))

    print("\n4. WHAT-IF block lists (NO NETWORK behind any of them) [FLOATS].  Columns: blocks per array, moves saved per array, move-nats per array, saving, credit the list would need for 1e-1 (moves per array)")
    def wi(name, blocks, Wn):
        Dn = Wn * m - mv(blocks); en = root(blocks, m, Wn)
        need = Q(blocks, m, 0.1)               # the law at e = 0.1 holds iff (sum over blocks of m (r/m)^0.9 - r) <= D ; ranks held fixed
        print("   %-92s W=%6d  blk/arr %6.2f  d %7.4f  S/arr %7.2f  saving %.4e  NET moves per array that these blocks would be charged at 1e-1 (ranks held fixed): %6.2f"
              % (name, Wn, nb(blocks) / Wn, Dn / Wn, S(blocks, m) / Wn, en, need / Wn))
        return en
    hx, hy, hsb = C["x-role (5 inv.)"], C["y-role (5 inv.)"], C["helpers (5 inv.)"]
    wi("LEGAL (for reference) the unit as it is", allb, W)
    wi("WHAT-IF (a1) scratch copies deleted", live, W)
    wi("WHAT-IF (a2) helpers deleted, copies kept (W = 4v)", data + cps, 4 * v)
    wi("WHAT-IF (a3) helpers and copies deleted: the data arrays as the certificate cuts them", data, 4 * v)
    whole = [(h - 1, 10 * v)]
    wi("WHAT-IF (a4) as (a3), x-role climbs merged to one block h-1 per invocation", whole[:0] + [(h - 1, 5 * v)] + hy + idle, 4 * v)
    wi("WHAT-IF (a5) as (a3), y-role climbs merged to one block h-1 per invocation", [(h - 1, 5 * v)] + hx + idle, 4 * v)
    wi("WHAT-IF (a6) as (a3), both merged (x-6's row: 4.5 blocks per data array)", whole + idle, 4 * v)
    wi("WHAT-IF (a7) as (a6), the catch-up 4 merged into a neighbour: X1,Y1 = 3x(h-1), 2h+2 ; X2,Y2 = 2h-2, h-1, h-1, h+3", [(h - 1, 6 * v + 2 * v + 2 * v), (2 * h + 2, 2 * v), (2 * h - 2, 2 * v), (h + 3, 2 * v)], 4 * v)
    wi("WHAT-IF (a8) as (a6), no catch-up at all: every data array 5 blocks of h-1 (5 moves skipped; no word does this)", [(h - 1, 20 * v)], 4 * v)
    wi("WHAT-IF (b1) unit with every helper one block of rank h per invocation, copies kept", data + [(h, 5 * R)] + cps, W)
    wi("WHAT-IF (b2) the same, copies deleted", data + [(h, 5 * R)], W)
    wi("WHAT-IF (b3) helpers on the plain schedule (m-1, 1), copies deleted", data + [(m - 1, R), (1, R)], W)
    wi("WHAT-IF (b4) helpers on the plain schedule, data merged as (a6), copies deleted", whole + idle + [(m - 1, R), (1, R)], W)
    wi("WHAT-IF (b5) helpers cut into single moves (the worst cutting), copies deleted", data + [(1, R * m)], W)
    wi("WHAT-IF (c1) unit as it is with the helpers' rank-1 blocks each merged into a rank-1 neighbour (pairs of singles -> 2)", data + cps + times([(r, n) for r, n in Hs if r != 1] + [(2, dict(Hs).get(1, 0) // 2)] + ([(1, 1)] if dict(Hs).get(1, 0) % 2 else []), 5), W)
    wi("WHAT-IF (c2) unit as it is, ONE more move skipped by every data array (taken from a block of rank 2h-2)", [(r, n) for r, n in allb if r != 2 * h - 2] + [(2 * h - 2, dict(allb)[2 * h - 2] - 4 * v), (2 * h - 3, 4 * v)], W)
    # the two shapes of the brief
    print("\n5. THE TWO SHAPES OF THE BRIEF [FLOATS; WHAT-IF]")
    for dd in (D / W, 4 * v / W, 1.0):
        en = root([(m - 1 - dd, 1), (1, 1)], m, 1)
        print("   WHAT-IF ab-1's shape (m-1-d, 1) at m = %d with d = %.4f : saving %.4e ; rate d per block beyond one = %.4f ; bar %.3f" % (m, dd, en, dd, bar(m, 0.1)))
    for hh, r in ((9, 3), (9, 1), (h, 1)):
        mm = 2 * hh
        bl = [(2 * hh - r, 1), (hh - r, 1), (hh, 1), (hh - r, 1), (hh + r, 1)]
        en = root(bl, mm, 3); dn = (3 * mm - mv(bl)) / 3
        print("   WHAT-IF ab-6's bystander word, catch-up merged, h = %d, r = %d, m = %d, 3 arrays, helpers and shears free: blocks/array %.2f, d = %.3f, saving %.4f ; rate per block beyond one = %.3f ; bar at m = %d: %.3f"
              % (hh, r, mm, 5 / 3, dn, en, dn / (5 / 3 - 1), mm, bar(mm, 0.1)))
    # look at the cuts
    print("\n6. LOOK: how the certificate cuts one invocation [exact; LEGAL]")
    for nm, sq in (("x-role", xs), ("y-role", ys)):
        c = Counter(tuple(s) for s in sq)
        print("   %s climbs of h-1 = %d moves, block ranks in order (pattern: count), %d arrays, mean %.2f blocks: " % (nm, h - 1, len(sq), sum(map(len, sq)) / len(sq))
              + " ".join("%s:%d" % ("".join(map(str, p)) if h < 10 else "-".join(map(str, p)), n) for p, n in c.most_common(14)))
    c = Counter(len(s) for s in ss)
    print("   helpers, blocks per invocation (number of blocks: helpers): " + " ".join("%d:%d" % kv for kv in sorted(c.items())))
    c = Counter(tuple(s) for s in ss)
    print("   helpers, commonest patterns: " + " ".join("%s:%d" % ("".join(map(str, p)) if h < 10 else "-".join(map(str, p)), n) for p, n in c.most_common(12)))
    sn = [sum(r * math.log(m / r) for r in s) for s in ss]
    print("   helpers, move-nats per invocation: least %.2f, mean %.2f, most %.2f ; one block of rank h would be %.2f, h single moves %.2f" % (min(sn), sum(sn) / len(sn), max(sn), h * math.log(m / h), h * math.log(m)))
    f1 = Counter(s[0] for s in ss); l1 = Counter(s[-1] for s in ss)
    print("   helpers, rank of the FIRST block (rank: helpers): " + " ".join("%d:%d" % kv for kv in sorted(f1.items())) + " ; of the LAST block: " + " ".join("%d:%d" % kv for kv in sorted(l1.items())))
    # merging the helpers' last block of one invocation with their first block of the next (WHAT-IF; the engine counts them apart)
    mg = Counter()
    for s in ss:
        if len(s) == 1:
            mg[m] += 0  # a helper with one block per invocation: 5 blocks of h -> would become one block of 5h (not proper); keep apart
            mg[s[0]] += 5
            continue
        for r in s[1:-1]: mg[r] += 5
        mg[s[0]] += 1; mg[s[-1]] += 1; mg[s[-1] + s[0]] += 4
    print("   WHAT-IF (c3): every helper's last block of an invocation merged with its first block of the next:")
    wi("WHAT-IF (c3) helpers' blocks merged across the four stage boundaries, rest as it is", data + cps + sorted(mg.items()), W)
    # 7. the stage structure against the cuts inside a stage (move-nats; chain rule: cutting a block of B moves into a and b costs a ln(B/a) + b ln(B/b))
    print("\n7. WHERE THE CHARGE COMES FROM [FLOATS on exact counts; LEGAL].  move-nats S = sum r ln(m/r); the saving is D / S to first order")
    S_plain = S([(m - 1, 1), (1, 1)], m)
    sd_stage = S([(h - 1, 10 * v)] + idle, m); sd_all = S(data, m)
    sh_stage = S([(h, 5 * R)], m); sh_all = S(hsb, m)
    tot = S(allb, m)
    rowsS = [("data arrays: the five stages (role climbs whole, idle blocks as published)", sd_stage, nb([(h - 1, 10 * v)] + idle)),
             ("data arrays: cuts inside the role climbs", sd_all - sd_stage, nb(data) - nb([(h - 1, 10 * v)] + idle)),
             ("helpers: the five stages (one block of h per invocation)", sh_stage, 5 * R),
             ("helpers: cuts inside an invocation", sh_all - sh_stage, nb(hsb) - 5 * R),
             ("scratch copies", S(cps, m), nb(cps))]
    for nm, x, k in rowsS:
        print("   %-78s %11.1f move-nats = %5.1f %%   blocks (or extra cuts) %6d : %6.2f move-nats each" % (nm, x, 100 * x / tot, k, x / k))
    print("   %-78s %11.1f           (the same arrays on the plain schedule: %.1f)" % ("sum", tot, W * S_plain))
    print("   skipped share, step by step [exact fractions]: a role climb skips 1 of h = %.4f of its stage ; the word pays 4 of 5 back: 1/m = %.5f per data array ;"
          " data arrays are %d of %d arrays: %.5f ; the copies take %d of %d back: D/(W m) = %.6f" % (1 / h, 1 / m, 4 * v, W, 4 * v / (W * m), 5 * cst, 4 * v, D / (W * m)))
    print("   mean entropy of the cutting, S/(W m) = %.4f nats per array (plain %.4f ; five equal stage blocks ln 5 = %.4f) ; saving ~ skipped share / entropy = %.4e"
          % (tot / (W * m), S_plain / m, math.log(5), D / tot))
    return dict(h=h, v=v, R=R, m=m, W=W, D=D, e=e)

def brief(path):
    """one line per unit from the stored histograms alone (gcert/1 or carrier-cert/1)"""
    d = json.load(gzip.open(path) if path.endswith(".gz") else open(path)); h, v, R, cst = d["h"], d["v"], d["R"], d["cst"]
    m, W = 5 * h, 4 * v + R
    H = {k: [(int(r), 5 * n) for r, n in d["blocks"][k].items()] for k in "xysc"}
    idle = [(2 * h + 2, 2 * v), (2 * h - 2, 2 * v), (h - 1, 2 * v), (4, 2 * v)]
    data = H["x"] + H["y"] + idle; allb = data + H["s"] + H["c"]
    D = W * m - mv(allb); e = root(allb, m, W)
    qd, qs, qc = Q(data, m, e), Q(H["s"], m, e), Q(H["c"], m, e) + mv(H["c"])
    print("   %-40s h=%2d v=%4d R=%5d W=%5d D=%5d  saving %.4e | moves saved per block: unit %.4f, data arrays %.4f (beyond plain's two: %.4f), helpers 0, copies %.1f | credit 4v spent on: data %4.1f %%, helpers %4.1f %%, copies %4.1f %% | blocks per array: data %.2f, helper %.2f"
          % (path.split("/")[-1][:40], h, v, R, W, D, e, D / nb(allb), 4 * v / nb(data), 4 * v / (nb(data) - 8 * v), -5 * cst / nb(H["c"]),
             100 * qd / (4 * v), 100 * qs / (4 * v), 100 * qc / (4 * v), nb(data) / (4 * v), nb(H["s"]) / R))
    casc = [("stage block alone, nothing paid back (WHAT-IF)", root([(h - 1, 20 * v)], m, 4 * v)),
            ("the word's 4 of 5 paid back, climbs whole (WHAT-IF)", root([(h - 1, 10 * v)] + idle, m, 4 * v)),
            ("data arrays as cut (WHAT-IF)", root(data, m, 4 * v)),
            ("with the helpers (WHAT-IF)", root(data + H["s"], m, W)),
            ("with the copies: the unit (LEGAL)", e)]
    print("        cascade: " + " -> ".join("%s %.3e" % kv for kv in casc) + "   | factors: " + ", ".join("%.2f" % (casc[i][1] / casc[i + 1][1]) for i in range(4))
          + " | charged at 1e-1 with ranks held fixed, moves per array: data arrays alone %.2f (they skip 1), whole unit %.2f (it skips %.3f)" % (Q(data, m, 0.1) / (4 * v), Q(allb, m, 0.1) / W, D / W))

if __name__ == "__main__":
    if sys.argv[1] == "brief":
        print("OTHER BLOCK LISTS, from the stored histograms only (I did not run the engine's checker on them; the first two are the published certificates) [FLOATS on exact counts]")
        for p in sys.argv[2:]: brief(p)
    else:
        for p in sys.argv[1:]: main(p)
