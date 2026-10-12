#!/usr/bin/env python3
"""knows.py [ab-1-fewerblocks]  Exact whole numbers.  THE KNOWS GRAPH OF THE FAT PORTS.
A fat port of dimension r on h address bits = an r-dimensional subspace P of F_2^h that meets its perpendicular only in 0.
Two ports KNOW each other when P_s lies inside P_t-perp (every word of one overlaps every word of the other evenly).
For each (h, r): the number of ports by type, the degree of the knows graph by type, and the size of two explicit
families of ports no two of which know each other:
   STAR(x)  = all ports through one word x                       (two ports that share a non-zero word never know each other)
   CLUB(S)  = all ports that contain a word of S, S = x0 + C, x0 odd, C a self-orthogonal code inside x0-perp
              (any two words of S overlap oddly, so two ports that each hold one of them do not know each other)
A family of size a in an orbit of size v gives the ceiling  kappa <= v / a  for every sub-family of that orbit
(the orbit is vertex-transitive under the address maps that keep the overlap form; then v / alpha is the fractional
colouring number, an upper bound for |sub-family| / alpha(sub-family)).
usage: knows.py h r [dump]      dump = write the edge list of the knows graph to knows_h_r.edges (small cases only)"""
import sys, itertools, time
h, r = int(sys.argv[1]), int(sys.argv[2]); dump = len(sys.argv) > 3
N = 1 << h
PAR = [bin(x).count("1") & 1 for x in range(N)]
ONE = N - 1
def rref_bases(h, r):
    """all r-dimensional subspaces of F_2^h, each once, as reduced bases (leading bits = pivots, pivots cleared elsewhere)"""
    for piv in itertools.combinations(range(h - 1, -1, -1), r):          # piv[0] > piv[1] > ...
        free = []
        for i, p in enumerate(piv):
            free.append([b for b in range(p) if b not in piv])
        def rec(i, acc):
            if i == r:
                yield tuple(acc); return
            fb = free[i]
            for m in range(1 << len(fb)):
                v = 1 << piv[i]
                for j, b in enumerate(fb):
                    if m >> j & 1: v |= 1 << b
                acc.append(v)
                yield from rec(i + 1, acc)
                acc.pop()
        yield from rec(0, [])
def gram_det(b):
    n = len(b); G = [[PAR[b[i] & b[j]] for j in range(n)] for i in range(n)]
    for c in range(n):
        pv = next((i for i in range(c, n) if G[i][c]), None)
        if pv is None: return 0
        G[c], G[pv] = G[pv], G[c]
        for i in range(c + 1, n):
            if G[i][c]: G[i] = [x ^ y for x, y in zip(G[i], G[c])]
    return 1
def span(b):
    S = [0]
    for v in b: S += [s ^ v for s in S]
    return S
# the club: x0 = e_0 (bit 0), C = span of the disjoint pairs (bits 1,2), (3,4), ...
x0 = 1; pairs = [(1 << a) | (1 << (a + 1)) for a in range(1, h - 1, 2)]
S = set(x0 ^ c for c in span(pairs))
assert all(PAR[a & b] == 1 for a in S for b in S)
inS = [x in S for x in range(N)]
t0 = time.time()
ports = []; tot = 0
cnt = {}; club = {}; star = {}
starx = {"odd weight-1 word e0": 1, "even weight-2 word": 3, "all-ones word": ONE}
for b in rref_bases(h, r):
    tot += 1
    if not gram_det(b): continue
    sp = span(b)
    Palt = all(PAR[x] == 0 for x in sp)            # every word of P even: P is of the alternating kind
    Qalt = ONE in sp                               # the all-ones word lies in P: P-perp is of the alternating kind
    typ = ("P alternating" if Palt else "P odd") + ", " + ("P-perp alternating" if Qalt else "P-perp odd")
    cnt[typ] = cnt.get(typ, 0) + 1
    if any(inS[x] for x in sp): club[typ] = club.get(typ, 0) + 1
    for nm, x in starx.items():
        if x in sp: star[(typ, nm)] = star.get((typ, nm), 0) + 1
    if dump or h <= 7: ports.append((frozenset(sp), typ, b))
v = sum(cnt.values())
print("== h = %d, r = %d : %d subspaces of dimension r, %d ports (meet their perpendicular only in 0)   [%.0f s]" % (h, r, tot, v, time.time() - t0))
print("   club S: %d odd words that pairwise overlap oddly (x0 = e0 plus a self-orthogonal code of dimension %d)" % (len(S), len(pairs)))
for typ in sorted(cnt):
    c = cnt[typ]; cl = club.get(typ, 0)
    st = max([(star.get((typ, nm), 0), nm) for nm in starx])
    best = max(cl, st[0])
    print("   type [%s]: %d ports ; club holds %d ; best star holds %d (%s) ; ceiling kappa <= %d / %d = %.3f"
          % (typ, c, cl, st[0], st[1], c, best, c / best if best else float("inf")))
print("   all types together: club holds %d of %d : v / club = %.3f" % (sum(club.values()), v, v / sum(club.values())))
if ports:
    # degrees, by brute force over pairs (small cases)
    idx = {p[0]: i for i, p in enumerate(ports)}
    perp = lambda sp: frozenset(a for a in range(N) if all(PAR[a & p] == 0 for p in sp))
    deg = {}; edges = []
    if len(ports) <= 7000:
        P_perp = [perp(p[0]) for p in ports]
        for i, (sp, typ, b) in enumerate(ports):
            d = 0
            for j, (sq, tq, bq) in enumerate(ports):
                if j != i and all(x in P_perp[i] for x in bq):
                    d += 1
                    if j > i: edges.append((i, j))
            deg.setdefault(typ, set()).add(d)
        print("   degree of the knows graph by type:", {k: sorted(s) for k, s in deg.items()}, "; edges:", len(edges))
        # check: the club is a set no two of whose members know each other
        cl = [i for i, p in enumerate(ports) if any(inS[x] for x in p[0])]
        cls = set(cl); assert not any(i in cls and j in cls for i, j in edges)
        print("   check: no two members of the club know each other: True")
        if dump:
            with open("%s/knows_%d_%d.edges" % (sys.argv[3], h, r), "w") as f:
                f.write("%d %d\n" % (len(ports), len(edges)))
                for i, p in enumerate(ports): f.write("t %d %s\n" % (i, p[1].replace(" ", "_")))
                for i, j in edges: f.write("%d %d\n" % (i, j))
