# invariants of a case (F1, F2, beta): s[i][j] = dim(V_i ∩ V'_j), r[i][j] = dim{x in V_i : beta(x, V'_j) = 0}, i, j = 0..k-1
# (V_i = span of the last k-i basis vectors of flag 1 = the subgroup whose cosets are the depth-i blocks).
import sys, re, collections
pc = lambda v: bin(v).count("1")
def span(vs):
    S = {0}
    for b in vs: S |= {v ^ b for v in S}
    return S
def bil(beta, x, y, k):
    s = 0
    for i in range(k):
        if (x >> i) & 1: s ^= pc(beta[i] & y) & 1
    return s
def table(F1, F2, beta, k):
    lg = lambda n: n.bit_length() - 1
    V = [span(F1[i:]) for i in range(k)]; Vp = [span(F2[j:]) for j in range(k)]
    s = tuple(tuple(lg(len(V[i] & Vp[j])) for j in range(k)) for i in range(k))
    r = tuple(tuple(lg(len([x for x in V[i] if all(bil(beta, x, y, k) == 0 for y in F2[j:])])) for j in range(k)) for i in range(k))
    rt = tuple(tuple(lg(len([y for y in Vp[j] if all(bil(beta, x, y, k) == 0 for x in F1[i:])])) for j in range(k)) for i in range(k))
    return s, r, rt
if __name__ == "__main__":
    k = int(sys.argv[1]); stat = collections.defaultdict(lambda: [0, 0, collections.Counter()])
    for line in open(sys.argv[2]):
        tag = line.split()[0]; ok = "conv=0/" not in line
        if tag.startswith("F2="):
            m = re.match(r"F2=(\d+);beta=(\d+)", tag); F1 = [4, 2, 1]; F2 = [int(c) for c in m.group(1)]; beta = [int(c) for c in m.group(2)]
        else:
            m = re.match(r"F=([\d.]+)/([\d.]+);beta=([\d.]+)", tag); F1 = [int(c) for c in m.group(1).split(".")]; F2 = [int(c) for c in m.group(2).split(".")]; beta = [int(c) for c in m.group(3).split(".")]
        t = table(F1, F2, beta, k); e = stat[t]; e[0] += 1; e[1] += ok
        if ok:
            d = re.search(r"family_dim=(\d+)", line); e[2][int(d.group(1))] += 1
        if ok and len(sys.argv) > 3: print("SOLVED", tag, t)
    mixed = sum(1 for e in stat.values() if 0 < e[1] < e[0])
    print("classes: %d ; all solved: %d ; none solved: %d ; mixed: %d" % (len(stat), sum(1 for e in stat.values() if e[1] == e[0]), sum(1 for e in stat.values() if e[1] == 0), mixed))
    for t, e in sorted(stat.items(), key=lambda kv: -kv[1][1] / kv[1][0]):
        if e[1]: print("  s=%s r=%s rt=%s : %d/%d dims=%s" % (t[0], t[1], t[2], e[1], e[0], dict(e[2])))
