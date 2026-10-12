# Independent replay of e-2-density/h8_21gates.txt: exact integers, own parser.
import sys
class V:
    def __init__(s, c): s.c = tuple(c)
    def __add__(s, o): return V(a + b for a, b in zip(s.c, o.c))
    def __sub__(s, o): return V(a - b for a, b in zip(s.c, o.c))
    def __neg__(s): return V(-a for a in s.c)
    def __rmul__(s, k): return V(k * a for a in s.c)
env = {"x%d" % i: V(1 if j == i else 0 for j in range(8)) for i in range(8)}
gates = 0
for line in open(sys.argv[1]):
    line = line.split("#")[0].strip()
    if not line or "=" not in line: continue
    lhs, rhs = [t.strip() for t in line.split("=", 1)]
    env[lhs] = eval(rhs, {"__builtins__": {}}, env)
    if lhs.startswith("g"): gates += 1
ok = True
for s in range(8):
    row = tuple((-1) ** bin(s & x).count("1") for x in range(8))
    if env["y%d" % s].c != row: ok = False; print("output", s, "differs", env["y%d" % s].c)
print("gates:", gates, "| all 8 outputs equal the Walsh-Hadamard rows exactly:", ok)
# s * s' of each gate wire (non-zeros of the form, non-zeros of its transform)
H = [[(-1) ** bin(s & x).count("1") for x in range(8)] for s in range(8)]
prof = []
for name, v in env.items():
    if name.startswith("g"):
        s1 = sum(1 for a in v.c if a)
        s2 = sum(1 for r in H if sum(a * b for a, b in zip(r, v.c)))
        prof.append((name, s1, s2, s1 * s2))
print("wires with s*s' > 8 (not tight):", [(n, a, b) for n, a, b, p in prof if p > 8])
print("tight wires:", sum(1 for p in prof if p[3] == 8), "of", len(prof))
