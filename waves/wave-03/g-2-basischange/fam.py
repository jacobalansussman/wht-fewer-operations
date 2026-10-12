# fam.py (g-2-basischange): least number of gates, count (G), for the analysis map B^-1 of a symmetry-adapted basis,
# minimised over the freedom "any basis of each head space", modulo a prime p (outer loop over bases, inner exhaustive mincirc).
# usage: fam.py k p layers(comma list or 'all') mmax [orbits]      layers: which weight layers are put on the wires together
import sys, itertools, subprocess, os, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from math import comb
MC = "waves/wave-01/d-0-zeta/mincirc"
def heads(k):
    # valence-bond head vectors (i = 0) per number of pairs w, as dict subsetmask -> coefficient
    N = 1 << k; groups = {}
    for x in range(N):
        st = []; pr = []
        for pos in range(k):
            if (x >> pos) & 1: st.append(pos)
            elif st: pr.append((st.pop(), pos))
        groups.setdefault(tuple(sorted(pr)), None)
    H = {}
    for M in groups:
        pv = {0: 1}
        for (a, b) in M:
            nv = {}
            for idx, c in pv.items():
                nv[idx | (1 << a)] = nv.get(idx | (1 << a), 0) + c; nv[idx | (1 << b)] = nv.get(idx | (1 << b), 0) - c
            pv = nv
        H.setdefault(len(M), []).append(pv)
    return H
def up(v, k):
    o = {}
    for T, c in v.items():
        for j in range(k):
            if not (T >> j) & 1: o[T | (1 << j)] = o.get(T | (1 << j), 0) + c
    return {T: c for T, c in o.items() if c}
def proj_points(f, p):
    out = []
    for c in itertools.product(range(p), repeat=f):
        nz = [x for x in c if x]
        if nz and nz[0] == 1: out.append(c)
    return out
def rank_mod(rows, p):
    A = [list(r) for r in rows]; r = 0
    for c in range(len(A[0]) if A else 0):
        piv = next((i for i in range(r, len(A)) if A[i][c] % p), None)
        if piv is None: continue
        A[r], A[piv] = A[piv], A[r]; inv = pow(A[r][c], p - 2, p)
        for i in range(len(A)):
            if i != r and A[i][c] % p:
                f = A[i][c] * inv % p; A[i] = [(x - f * y) % p for x, y in zip(A[i], A[r])]
        r += 1
    return r
def main():
    k = int(sys.argv[1]); p = int(sys.argv[2]); mmax = int(sys.argv[4])
    layers = list(range(1, k)) if sys.argv[3] == 'all' else [int(x) for x in sys.argv[3].split(',')]
    use_orbits = len(sys.argv) > 5
    H = heads(k); wmax = max(min(i, k - i) for i in layers)
    wires = [T for i in layers for T in range(1 << k) if bin(T).count("1") == i]
    n = len(wires) + (len(wires) & 1)
    choices_w = {}
    for w in range(1, wmax + 1):
        f = len(H[w]); pts = proj_points(f, p)
        choices_w[w] = [c for c in itertools.combinations(pts, f) if rank_mod(c, p) == f]
    ws = sorted(choices_w)
    def rows_for(choice):
        rows = []
        for i in layers:
            for w in range(0, min(i, k - i) + 1):
                if w == 0: gs = [{0: 1}]
                else:
                    gs = []
                    for c in choice[w]:
                        g = {}
                        for a, ca in enumerate(c):
                            for T, v in H[w][a].items(): g[T] = (g.get(T, 0) + ca * v) % p
                        gs.append(g)
                for g in gs:
                    v = dict(g)
                    for _ in range(i - w): v = up(v, k)
                    rows.append([v.get(T, 0) % p for T in wires] + [0] * (n - len(wires)))
        return rows
    def canon_key(rows):
        # orbit key under permutations of the k coordinates: the set of projective target rows, minimised
        best = None
        for perm in itertools.permutations(range(k)):
            def mapT(T): return sum(1 << perm[j] for j in range(k) if (T >> j) & 1)
            idx = [wires.index(mapT(T)) for T in wires]
            rr = []
            for r in rows:
                q = [0] * len(wires)
                for a, b in enumerate(idx): q[b] = r[a]
                lead = next(x for x in q if x); inv = pow(lead, p - 2, p); rr.append(tuple(x * inv % p for x in q))
            key = tuple(sorted(rr))
            if best is None or key < best: best = key
        return best
    total = 0; seen = set(); hist = {}; best = None
    tf = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False); tf.close()
    for combo in itertools.product(*[choices_w[w] for w in ws]):
        choice = dict(zip(ws, combo)); rows = rows_for(choice); total += 1
        if rank_mod(rows, p) < len(rows):
            hist['degenerate'] = hist.get('degenerate', 0) + 1; continue
        if use_orbits:
            key = canon_key(rows)
            if key in seen: continue
            seen.add(key)
        with open(tf.name, "w") as fh:
            for r in rows: fh.write(" ".join(map(str, r)) + "\n")
        res = None
        for m in range(0, mmax + 1):
            out = subprocess.run([MC, str(p), str(n), str(m), tf.name], capture_output=True, text=True).stdout
            if "YES" in out:
                res = (m, out); break
        ntar = len(rows)
        g = (ntar + res[0]) if res else None
        hist[g] = hist.get(g, 0) + 1
        if 1 in choice:
            gv = []
            for c in choice[1]:
                vec = [0] * k
                for a, ca in enumerate(c):
                    for T, v in H[1][a].items(): vec[T.bit_length() - 1] = (vec[T.bit_length() - 1] + ca * v) % p
                gv.append(vec)
            bk = None
            for perm in itertools.permutations(range(k)):
                rr = []
                for vec in gv:
                    q = [vec[perm[j]] for j in range(k)]; lead = next(x for x in q if x); inv = pow(lead, p - 2, p); rr.append(tuple(x * inv % p for x in q))
                key = tuple(sorted(rr))
                if bk is None or key < bk: bk = key
            print("CH", bk, g); sys.stdout.flush()
        if res and (best is None or g < best[0]): best = (g, choice, rows, res[1]); print("new best %d gates, choice %s" % (g, choice)); sys.stdout.flush()
    os.unlink(tf.name)
    print("k=%d p=%d layers=%s wires=%d(+%d dummy) targets=%d  bases tried %d (%s)" % (k, p, layers, len(wires), n - len(wires), len(rows), total, "one per orbit of S_k: %d" % len(seen) if use_orbits else "all"))
    print("histogram {gates: number of bases}  (None = more than targets+%d): %s" % (mmax, dict(sorted(hist.items(), key=lambda t: str(t[0])))))
    if best:
        print("BEST %d gates. wires (subset masks): %s" % (best[0], wires)); print("choice (coefficients on valence-bond heads):", best[1]); print(best[3])
main()
