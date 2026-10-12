# lift22b.py: take the modulo-5 circuit (10 gates) for layer 2 at 16 points with the head basis
#   g1 = x3 - x4, g2 = x2 - x4, g3 = x1 - x2 - x3 + x4   and try to lift it to the rationals, gate by gate.
import itertools, subprocess, re, sys
from fractions import Fraction as Fr
MC = "waves/wave-01/d-0-zeta/mincirc"
src = open("fam.py").read(); ns = {"__file__": "fam.py"}; exec(src[:src.index("def main():")], ns)
k = 4; p = 5; H = ns["heads"](k); up = ns["up"]
wires = [T for T in range(16) if bin(T).count("1") == 2]
G1 = [{4: 1, 8: -1}, {2: 1, 8: -1}, {1: 1, 2: -1, 4: -1, 8: 1}]
def vec(d): return [d.get(T, 0) for T in wires]
fixed = [vec({T: 1 for T in wires})] + [vec(up(g, k)) for g in G1]
heads2 = [vec(h) for h in H[2]]
def Dn(f): return [sum(f[n] for n, T in enumerate(wires) if (T >> i) & 1) for i in range(4)]
assert all(not any(Dn(h)) for h in heads2)
found = None
for (a, b), (c, d) in itertools.combinations([(1, 0), (0, 1), (1, 1), (1, 2), (1, 3), (1, 4)], 2):
    r1 = [(a * x + b * y) % p for x, y in zip(*heads2)]; r2 = [(c * x + d * y) % p for x, y in zip(*heads2)]
    open("rows22.txt", "w").write("\n".join(" ".join(str(x % p) for x in r) for r in fixed + [r1, r2]) + "\n")
    o = subprocess.run([MC, "5", "6", "4", "rows22.txt"], capture_output=True, text=True).stdout
    if "YES" in o: found = o; print("head forms modulo 5:", r1, r2); break
print(found); sys.stdout.flush()
if not found: sys.exit()
gates = [(m.group(1), int(m.group(3)), int(m.group(4)), int(m.group(5))) for m in re.finditer(r"g\d+\s+(TARGET|inter)\s*= \[([^\]]*)\]\s+from #(\d+) \+ (\d+)\*#(\d+)", found)]
pool = sorted(set(Fr(a, b) * s for a in range(1, 7) for b in range(1, 7) for s in (1, -1)), key=lambda f: (abs(f.numerator) + f.denominator, f))
def lifts(c): return [f for f in pool if f.denominator % p and (f.numerator * pow(f.denominator, p - 2, p) - c) % p == 0][:8]
def prop(u, v): return any(u) and any(v) and all(u[i] * v[j] == u[j] * v[i] for i in range(6) for j in range(6))
E = [[Fr(int(i == j)) for j in range(6)] for i in range(6)]
best = [None]
def rec(i, vals):
    if best[0]: return
    if i == len(gates):
        made = vals[6:]
        okfix = all(any(prop(t, v) for v in made) for t in fixed)
        hs = [v for v in made if any(v) and not any(Dn(v))]
        okhead = any(not prop(a, b) for a, b in itertools.combinations(hs, 2))
        if okfix and okhead: best[0] = list(vals)
        return
    kind, u, c, v = gates[i]
    for f in lifts(c):
        rec(i + 1, vals + [[x + f * y for x, y in zip(vals[u], vals[v])]])
rec(0, E)
if best[0]:
    print("LIFTED over the rationals: 10 gates. wires = pairs", [(T & -T).bit_length() * 10 + T.bit_length() for T in wires])
    for n, v in enumerate(best[0][6:]): print("  gate %2d = %s   %s" % (n + 1, [str(a) for a in v], "head (killed by remove-one)" if not any(Dn(v)) else ("fixed target" if any(prop(t, v) for t in fixed) else "helper")))
else: print("NO lift found with coefficients of numerator and denominator up to 6: stays a modulo-5 candidate")
