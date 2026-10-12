# lift.py (d-0-zeta): replay over the rationals the 8-point subset-sum circuits found over GF(3) that use a signed helper.
# A digit 2 of GF(3) is read as -1. A point becomes available when it lies in the span of two available points (one gate).
# Success = all 5 helpers and all 7 non-input outputs become available: 12 gates over Q.
from fractions import Fraction as F
import itertools, re, sys
def in_span(w, u, v):
    # exact: is w = a u + b v for rationals a, b ?
    n = len(w)
    for i, j in itertools.combinations(range(n), 2):
        det = u[i] * v[j] - u[j] * v[i]
        if det != 0:
            a = F(w[i] * v[j] - w[j] * v[i], det); b = F(u[i] * w[j] - u[j] * w[i], det)
            return all(a * u[t] + b * v[t] == w[t] for t in range(n)), (a, b)
    return False, None
Z = [[1 if (T & S) == T else 0 for T in range(8)] for S in range(8)]      # index = bits, same order as the Kronecker rows
targets = [tuple(r) for r in Z[1:]]
def replay(helpers, show=False):
    avail = [tuple(int(i == j) for j in range(8)) for i in range(8)]; todo = [tuple(h) for h in helpers] + targets; gates = []
    ch = True
    while ch and todo:
        ch = False
        for w in list(todo):
            for u, v in itertools.combinations(avail, 2):
                ok, ab = in_span(w, u, v)
                if ok:
                    avail.append(w); todo.remove(w); gates.append((w, ab, u, v)); ch = True; break
    if show:
        for w, ab, u, v in gates: print("     %s = %s * %s + %s * %s%s" % (w, ab[0], u, ab[1], v, "   (output)" if w in targets else ""))
    return not todo, len(gates)
lines = [l for l in open("z8_p3_all.out") if l.strip().startswith("example")]
for l in lines:
    hs = [[(-1 if c == "2" else int(c)) for c in h] for h in re.findall(r"\[(\d+)\]", l)]
    ok, g = replay(hs)
    print("signed helpers %s : replay over Q %s, gates %d   helpers %s" % (l.split()[2], "OK" if ok else "FAILS", g, hs))
print("one signed circuit in full:")
l = [l for l in lines if " 1 signed" in l][3]
replay([[(-1 if c == "2" else int(c)) for c in h] for h in re.findall(r"\[(\d+)\]", l)], show=True)
