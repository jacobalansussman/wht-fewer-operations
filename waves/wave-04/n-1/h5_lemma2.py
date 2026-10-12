# n-1: independent exact test of h-5 Lemma 2 (births of a gate <= max(1, width of the wider parent)).
# Integers only. A gate is alpha*w = v + beta*u  (count G: any a*u + b*v).
# K(i,t): forms equal to (1,t) on bit i times anything.  birth at (i,t): w in K(i,t), u and v outside.
import sys, itertools, random
from collections import Counter

def analyse(vec, k):
    """(mask of entangled bits, pure sign per bit: +1, -1, or 0 when the factor is not pure or the bit is entangled)"""
    N = 1 << k
    E = 0
    pure = [0] * k
    for i in range(k):
        m = 1 << i
        idx = [x for x in range(N) if not x & m]
        a = [vec[x] for x in idx]
        b = [vec[x | m] for x in idx]
        if a == b:
            pure[i] = 1
            continue
        if all(p == -q for p, q in zip(a, b)):
            pure[i] = -1
            continue
        piv = next(j for j in range(len(a)) if a[j] or b[j])
        pa, pb = a[piv], b[piv]
        if any(pa * b[j] - a[j] * pb for j in range(len(a))):
            E |= m
    return E, pure

def norm(vec):
    f = next((x for x in vec if x), 0)
    return tuple(vec) if f > 0 else tuple(-x for x in vec)

def run(k, U, W, coefs, label):
    N = 1 << k
    infoU = {u: analyse(u, k) for u in U}
    hist = Counter()
    viol = 0
    viol_sharp = 0
    lemma1_viol = 0
    ngates = 0
    examples = {}
    for w in W:
        Ew, pw = analyse(w, k)
        pureset = [i for i in range(k) if pw[i]]
        for u in U:
            Eu, pu = infoU[u]
            S = [i for i in pureset if pu[i] != pw[i]]
            if len(S) < 2:
                continue
            for (al, be) in coefs:
                v = tuple(al * w[x] - be * u[x] for x in range(N))
                if not any(v):
                    continue
                ngates += 1
                Ev, pv = analyse(v, k)
                # Lemma 1: v is outside K exactly where u is
                for i in pureset:
                    if (pv[i] == pw[i]) != (pu[i] == pw[i]):
                        lemma1_viol += 1
                eu = bin(Eu).count("1")
                ev = bin(Ev).count("1")
                c = len(S)
                hist[(c, eu, ev)] += 1
                if c > max(1, eu, ev):
                    viol += 1
                    if viol <= 5:
                        print("VIOLATION", label, "w", w, "u", u, "v", v, "births", c, "eu", eu, "ev", ev)
                Sm = sum(1 << i for i in S)
                if not ((Sm & ~Eu) == 0 or (Sm & ~Ev) == 0):
                    viol_sharp += 1
                nzu = sum(1 for x in u if x)
                if c == k and nzu == 2 and eu == k and "onegate" not in examples:
                    examples["onegate"] = (w, u, v, al, be, c, eu, ev)
                if c >= 2 and max(eu, ev) == c and min(eu, ev) == 0 and ("lop%d" % c) not in examples:
                    examples["lop%d" % c] = (w, u, v, al, be, c, eu, ev)
    print("==", label, ": k =", k, " gates tested with 2 or more births:", ngates)
    print("   violations of Lemma 2 (births > max(1, e(u), e(v))):", viol)
    print("   violations of the sharper form (birth set inside E(u) or inside E(v)):", viol_sharp)
    print("   violations of Lemma 1 (parents both in or both out):", lemma1_viol)
    print("   histogram (births, e(u), e(v)) -> count:")
    for key in sorted(hist):
        print("     ", key, hist[key])
    for name, ex in examples.items():
        print("   example", name, ": w =", ex[0], " u =", ex[1], " v =", ex[2], " alpha, beta =", ex[3], ex[4],
              " births", ex[5], " e(u)", ex[6], " e(v)", ex[7])
    sys.stdout.flush()

def kron(a, b):
    # a on the low bits, b on the high bits
    return tuple(x * y for y in b for x in a)

if __name__ == "__main__":
    which = sys.argv[1]
    random.seed(20261011)
    if which == "8":
        k = 3
        U = sorted({norm(v) for v in itertools.product((-1, 0, 1), repeat=8) if any(v)})
        W = [u for u in U if sum(1 for p in analyse(u, k)[1] if p) >= 2]
        # more w: pure on two bits, the third factor with entries up to 3
        extra = set()
        two = [(1, 2), (2, 1), (1, -2), (2, -1), (1, 3), (3, 1), (1, -3), (3, -1), (2, 3), (3, -2)]
        pures = [(1, 1), (1, -1)]
        for f in two:
            for p in pures:
                for q in pures:
                    extra.add(norm(kron(kron(f, p), q)))
                    extra.add(norm(kron(kron(p, f), q)))
                    extra.add(norm(kron(kron(p, q), f)))
        W = W + sorted(extra)
        print("8 points: |U| =", len(U), " |W| =", len(W))
        coefs = [(1, 1), (1, -1), (1, 2), (1, -2), (2, 1), (2, -1), (1, 3), (3, 1)]
        run(k, U, W, coefs, "8 points, every u with entries 0,+1,-1")
    else:
        k = 4
        pures = [(1, 1), (1, -1)]
        F = [(1, 0), (0, 1), (1, 1), (1, -1), (1, 2)]
        four = sorted({norm(v) for v in itertools.product((-1, 0, 1), repeat=4) if any(v)})
        U = set()
        # width at most 2: a 4-vector on a pair of bits times 2-vectors on the two other bits
        def place(pairvec, pair, f1, f2):
            others = [i for i in range(4) if i not in pair]
            vec = [0] * 16
            for x in range(16):
                bits = [(x >> i) & 1 for i in range(4)]
                vec[x] = pairvec[bits[pair[0]] + 2 * bits[pair[1]]] * f1[bits[others[0]]] * f2[bits[others[1]]]
            return norm(vec)
        for pair in itertools.combinations(range(4), 2):
            for pv in four:
                for f1 in F:
                    for f2 in F:
                        U.add(place(pv, pair, f1, f2))
        nstruct = len(U)
        # two entangled pairs (width 4 made of two pairs), a sample
        for _ in range(1500):
            a = random.choice(four); b = random.choice(four)
            U.add(norm(kron(a, b)))
        # sparse wires (2, 3, 4 non-zeros) and random wires
        for _ in range(1500):
            vec = [0] * 16
            for x in random.sample(range(16), random.choice((2, 2, 3, 4))):
                vec[x] = random.choice((-1, 1))
            U.add(norm(vec))
        for _ in range(1500):
            vec = [random.choice((-1, 0, 1)) for _ in range(16)]
            if any(vec):
                U.add(norm(vec))
        U = sorted(U)
        W = set()
        for signs in itertools.product(pures, repeat=4):
            W.add(norm(kron(kron(signs[0], signs[1]), kron(signs[2], signs[3]))))
        rest = [(1, 0), (0, 1), (1, 2), (2, -1), (1, 3)]
        for pos in range(4):
            for signs in itertools.product(pures, repeat=3):
                for r in rest:
                    fac = list(signs)
                    fac.insert(pos, r)
                    W.add(norm(kron(kron(fac[0], fac[1]), kron(fac[2], fac[3]))))
        W = sorted(W)
        print("16 points: |U| =", len(U), "(structured width<=2:", nstruct, ")  |W| =", len(W))
        coefs = [(1, 1), (1, -1), (1, 2), (2, 1)]
        run(k, U, W, coefs, "16 points, structured and random u")
