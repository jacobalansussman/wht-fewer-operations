# e-6-shifts, second run: every 2-dimensional subgroup K of the 16 addresses, both embeddings (x fanned out over the
# cosets of K, answer on K-perp; x written on K, zero elsewhere), every 16-point program; every 7-gate circuit met is
# compared with the census of 228 optimal 4-point gate sets (i-play/n4.py, imported and re-run here).
import sys, time, itertools
sys.path.insert(0, "waves/wave-02/e-6-shifts")
sys.path.insert(0, "waves/wave-01/i-play")
from fractions import Fraction as Fr
from math import gcd
import collapse as C
import n4
t0 = time.time()
sols, targets = n4.search(4, [0, 1, 2, 3], 7, True)
census = set(sols)
print("census: %d gate sets with 7 gates (%.0f s)" % (len(census), time.time() - t0)); sys.stdout.flush()
def to_int(v):
    # Gaussian-rational vector -> primitive integer tuple in n4's normal form, or None if not real
    if any(t.b != 0 for t in v): return None
    den = 1
    for t in v: den = den * t.a.denominator // gcd(den, t.a.denominator)
    return n4.norm(tuple(int(t.a * den) for t in v))
def classify(r, hs):
    nodes = [r["vecs"][h] for h in list(hs) + list(r["want"])]
    iv = [to_int(v) for v in nodes]
    if any(x is None for x in iv): return "complex", None
    fs = frozenset(iv)
    return ("census" if fs in census else "NOT-IN-CENSUS"), fs
Ks = C.subspaces2()
budget = float(sys.argv[1]) if len(sys.argv) > 1 else 400
progs = [("textbook", C.textbook()), ("two-pass 7x7", C.twopass()), ("two-pass mixed", C.twopass((0, 1, 2, 3), (3, 2, 1, 0))),
         ("rook chain", C.rook(False)), ("rook tree", C.rook(True))] + [("clebsch %d" % i, C.clebsch(i)) for i in range(4)]
FL = C.flags(4); LV = [C.level(c, 16) for c in FL]
pairs = [(i, j) for i in range(len(FL)) for j in range(i + 1, len(FL)) if C.mod4_solve(LV[i], LV[j], 4) is not None]
fl = []
for (i, j) in pairs:
    for first in ("B", "A"):
        fl.append(("flags %d,%d %s" % (i, j, first), C.twoflag(FL[i], FL[j], first)))
seen7 = {}; allnew = set(); allcx = 0
def do(name, pg, Klist, pool=True):
    global allcx
    hist = {}
    for K in Klist:
        for kind, f in (("pull", C.emb_pullback), ("sparse", C.emb_sparse)):
            E, outs = f(K)
            r = C.collapse(pg, E, C.H4rows, maxh_strict=4, maxh_pool=(3 if pool else None), want_sets=True)
            tags = {}
            for mode in ("strict", "pool"):
                if r[mode] == 7:
                    for hs in r[mode + "_sets"]:
                        tag, fs = classify(r, hs)
                        tags[(mode, tag)] = tags.get((mode, tag), 0) + 1
                        if tag == "census": seen7.setdefault(fs, set()).add(name.split()[0])
                        elif tag == "NOT-IN-CENSUS":
                            allnew.add(fs); print("     NEW?", name, kind, K, mode, sorted(fs))
                        else: allcx += 1
                if r[mode] is not None and r[mode] < 7:
                    print("     BELOW 7 ?!", name, kind, K, mode, r[mode])
            key = (kind, r["strict"], r["pool"])
            hist.setdefault(key, []).append((K, r["classes"], tuple(sorted(tags.items()))))
    print("%-18s gates=%3d" % (name, pg.ngates()))
    for k in sorted(hist, key=str):
        v = hist[k]
        print("   %-6s strict=%-4s pool=%-4s : %2d subgroups; classes %s; e.g. K=%s %s" % (
            k[0], k[1], k[2], len(v), sorted(set(c for _, c, _ in v)), v[0][0], dict(v[0][2])))
    sys.stdout.flush()
for name, pg in progs:
    do(name, pg, Ks)
# flags: all 108 on the diagonal, then as many as time allows on all 35 subgroups (strict only is cheap; pool too)
print("--- two-flag programs, diagonal subgroup only, all 108")
agg = {}
for name, pg in fl:
    E, outs = C.emb_pullback([0, 5, 10, 15])
    r = C.collapse(pg, E, C.H4rows, maxh_strict=4, maxh_pool=3, want_sets=True)
    k8 = None
    if r["strict"] == 8:
        k8 = frozenset(C.show(r["vecs"][h]) for h in r["strict_sets"][0])
    tg = {}
    if r["pool"] == 7:
        for hs in r["pool_sets"]:
            tag, fs = classify(r, hs); tg[tag] = tg.get(tag, 0) + 1
            if tag == "census": seen7.setdefault(fs, set()).add("flags")
            elif tag == "NOT-IN-CENSUS": allnew.add(fs); print("     NEW?", name, sorted(fs))
            else: allcx += 1
    agg.setdefault((r["classes"], r["strict"], len(r["strict_sets"]), r["pool"], tuple(sorted(tg.items())), k8), []).append(name)
for k, v in sorted(agg.items(), key=str):
    print("   classes=%s strict=%s (%d sets) pool=%s %s : %d programs; first strict helper set: %s" % (k[0], k[1], k[2], k[3], dict(k[4]), len(v), sorted(k[5]) if k[5] else None))
sys.stdout.flush()
print("--- two-flag programs, all 35 subgroups, as many as the time allows")
done = 0
for name, pg in fl[::9]:
    if time.time() - t0 > budget: break
    do(name, pg, Ks); done += 1
print("flag programs done on all subgroups:", done)
print("distinct census sets reached by some collapse: %d of %d ; sets not in census: %d ; pool sets with a complex helper: %d" % (len(seen7), len(census), len(allnew), allcx))
by = {}
for fs, names in seen7.items():
    for nm in names: by[nm] = by.get(nm, 0) + 1
print("census sets reached, by program family:", by)
