#!/usr/bin/env python3
"""slp2lean.py: check a small program for a scaled Walsh-Hadamard transform exactly (every addition, every
subtraction and every multiplication by a constant is one operation), then write it
as Lean source in the circuit model of OpenAI's file lean/OAI/Computability/FourierCircuit/Core.lean.

The text that this program writes into the Lean file is kept exactly as it was when the Lean files were
built, so that the file it writes is byte for byte lean/Work/SmallWHT/H8Half.lean.  That text names paths
inside the Lean project (the folder lean/ at the top), and where it says "this repository" it means the
repository in which the Lean files were first written, wht-power-saving-lean (see NOTICE, section 3).

usage: python3 -B slp2lean.py <program.txt> <log2 of the number of points> <scale, e.g. 1/2> <Lean namespace> <out.lean>

Program text: one operation per line,  t = u + v ,  t = u - v  or  t = c * u  (c a fraction); '#' starts a comment;
inputs are x0, x1, ...  The outputs are FOUND, not named: for every row j the program must hold a wire equal to
scale * (row j of H), where H[j][l] = (-1)^(number of common 1-bits of j and l).
Standard library only.  The check is exact (fractions).  It prints one line that starts with CHECK."""
import sys
from fractions import Fraction as F

path, k, scale, ns, out = sys.argv[1], int(sys.argv[2]), F(sys.argv[3]), sys.argv[4], sys.argv[5]
n = 1 << k
names = {"x%d" % i: i for i in range(n)}          # wire numbers of the Lean model: 0..n-1 inputs, n = the constant 0,
form = [[F(int(i == j)) for j in range(n)] for i in range(n)] + [[F(0)] * n]   # n+1+t = operation number t (from 0)
gates, text = [], []
for line in open(path, encoding="utf-8"):
    line = line.split("#")[0].strip()
    if not line:
        continue
    lhs, rhs = [s.strip() for s in line.split("=")]
    t = rhs.split()
    assert len(t) == 3 and lhs not in names, line
    if t[1] == "*":
        c, u = F(t[0]), names[t[2]]
        gates.append(("scale", c, u)); form.append([c * a for a in form[u]])
    else:
        u, v = names[t[0]], names[t[2]]
        assert t[1] in "+-", line
        gates.append(("add" if t[1] == "+" else "sub", u, v))
        s = 1 if t[1] == "+" else -1
        form.append([a + s * b for a, b in zip(form[u], form[v])])
    names[lhs] = n + len(gates)
    text.append(line)
size = len(gates)
outs = []
for j in range(n):
    row = [scale * (-1) ** bin(j & l).count("1") for l in range(n)]
    hits = [w for w in range(n + 1 + size) if form[w] == row]
    assert hits, "no wire holds scale * row %d" % j
    outs.append(hits[0])
kinds = {g[0] for g in gates}
print("CHECK ok: %s: %d points, %d operations (%d add/sub, %d scale), every row j of (%s)*H is held by a wire; outputs %s"
      % (path, n, size, sum(g[0] != "scale" for g in gates), sum(g[0] == "scale" for g in gates), scale, outs))

def frac(c):
    return "(%d / %d : ℂ)" % (c.numerator, c.denominator) if c.denominator != 1 else "(%d : ℂ)" % c.numerator
def idx(w):
    return "⟨%d, by decide⟩" % w
L = []
A = L.append
A("import OAI.Computability.FourierCircuit.Core")
A("")
A("/-!")
A("# The %d-point Walsh-Hadamard transform, scaled by %s, in %d operations" % (n, scale, size))
A("")
A("Written by `slp2lean.py` from `%s`; do not edit by hand." % path.split("/")[-1])
A("")
A("The model is OpenAI's circuit model of `OAI/Computability/FourierCircuit/Core.lean` (namespace")
A("`OAI.ExactFourier`): a `Program n k` is a list of `k` gates on `n` inputs, each gate one addition, one")
A("subtraction or one multiplication by a constant, and each gate costs one.  A `Circuit n` is a program with a")
A("choice of `n` output wires; its `size` is the number of gates.  Wire numbers: `0 .. n-1` are the inputs,")
A("`n` is the constant 0, and `n+1+t` is the result of gate number `t` (counted from 0).")
A("")
A("This file adds nothing to the model.  It contains: the matrix `hadamard k` (same formula as the function")
A("`OAI.PowerSaving.WHT.wht` of this repository), two lemmas that read one wire of a program, the program as")
A("data, and the statement that the circuit computes `(%s) * H` with `%d` gates." % (scale, size))
A("-/")
A("")
A("namespace OAI")
A("namespace ExactFourier")
A("namespace %s" % ns)
A("noncomputable section")
A("")
A("/-- The Walsh-Hadamard matrix on `2^k` points in natural (Sylvester) order: the entry in row `j` and column")
A("`l` is `(-1)^(number of common 1-bits of j and l)`.  Entry formula copied from `OAI.PowerSaving.WHT.wht`. -/")
A("def hadamard (k : ℕ) : Matrix (Fin (2 ^ k)) (Fin (2 ^ k)) ℂ :=")
A("  fun j l => ∏ i ∈ Finset.range k, if j.val.testBit i && l.val.testBit i then (-1 : ℂ) else 1")
A("")
A("/-- The same matrix for `k = %d`, with the index type written `Fin %d`. -/" % (k, n))
A("def H : Matrix (Fin %d) (Fin %d) ℂ :=" % (n, n))
A("  fun j l => ∏ i ∈ Finset.range %d, if j.val.testBit i && l.val.testBit i then (-1 : ℂ) else 1" % k)
A("")
A("theorem H_eq_hadamard : H = hadamard %d := rfl" % k)
A("")
A("/-- Reading a wire of the empty program: an input, or the constant 0. -/")
A("theorem eval_nil_apply {n : ℕ} (x : Fin n → ℂ) (i : Fin (n + 1 + 0)) :")
A("    (Program.nil : Program n 0).eval x i = if h : i.val < n then x ⟨i.val, h⟩ else 0 := by")
A("  by_cases h : i.val < n")
A("  · simp [Program.eval, Fin.snoc, h, Fin.castLT]")
A("  · simp [Program.eval, Fin.snoc, h]")
A("")
A("/-- Reading a wire after one more gate: an older wire, or the value of the new gate. -/")
A("theorem eval_step_apply {n k : ℕ} (p : Program n k) (g : Gate (n + 1 + k)) (x : Fin n → ℂ)")
A("    (i : Fin (n + 1 + (k + 1))) :")
A("    (Program.step p g).eval x i =")
A("      if h : i.val < n + 1 + k then p.eval x ⟨i.val, h⟩ else g.eval (p.eval x) := by")
A("  by_cases h : i.val < n + 1 + k")
A("  · simp [Program.eval, Fin.snoc, h, Fin.castLT]")
A("  · simp [Program.eval, Fin.snoc, h]")
A("")
A("/-! ## The program, one definition per gate -/")
A("")
A("def p0 : Program %d 0 := .nil" % n)
for t, g in enumerate(gates):
    if g[0] == "scale":
        body = ".scale %s %s" % (frac(g[1]), idx(g[2]))
    else:
        body = ".%s %s %s" % (g[0], idx(g[1]), idx(g[2]))
    A("/-- wire %d:  `%s` -/" % (n + 1 + t, text[t]))
    A("def p%d : Program %d %d := .step p%d (%s)" % (t + 1, n, t + 1, t, body))
A("")
A("/-- The circuit: the %d gates above, and for every row `j` the wire that holds `(%s) * (row j of H)`. -/" % (size, scale))
A("def circuit : Circuit %d where" % n)
A("  size := %d" % size)
A("  program := p%d" % size)
A("  outputs := ![%s]" % ", ".join(idx(w) for w in outs))
A("")
A("theorem circuit_size : circuit.size = %d := rfl" % size)
A("")
A("/-- **The %d-point Walsh-Hadamard transform, scaled by %s, has a circuit with %d gates** in OpenAI's" % (n, scale, size))
A("model (every addition, subtraction and multiplication by a constant costs one). -/")
A("theorem circuit_computes : circuit.Computes (%s • H) := by" % frac(scale))
A("  intro x")
A("  obtain ⟨f, rfl⟩ : ∃ f : ℕ → ℂ, x = fun i => f i.val :=")
A("    ⟨fun m => if h : m < %d then x ⟨m, h⟩ else 0, by funext i; simp⟩" % n)
A("  funext i")
A("  fin_cases i <;>")
A("    simp +decide [Circuit.eval, circuit, %s," % ", ".join("p%d" % t for t in range(size, -1, -1)))
A("      eval_step_apply, eval_nil_apply, Gate.eval, Matrix.mulVec, dotProduct, H,")
A("      Fin.sum_univ_eight, Finset.prod_range_succ] <;>")
A("    ring")
A("")
A("/-- The same statement with the matrix written `hadamard %d`. -/" % k)
A("theorem circuit_computes_hadamard :")
A("    circuit.Computes (%s • (hadamard %d : Matrix (Fin %d) (Fin %d) ℂ)) :=" % (frac(scale), k, n, n))
A("  circuit_computes")
A("")
A("/-- Both facts in one statement. -/")
A("theorem exists_circuit :")
A("    ∃ C : Circuit %d, C.size = %d ∧ C.Computes (%s • (hadamard %d : Matrix (Fin %d) (Fin %d) ℂ)) :=" % (n, size, frac(scale), k, n, n))
A("  ⟨circuit, circuit_size, circuit_computes_hadamard⟩")
A("")
A("end")
A("end %s" % ns)
A("end ExactFourier")
A("end OAI")
A("")
A("#print axioms OAI.ExactFourier.%s.exists_circuit" % ns)
open(out, "w", encoding="utf-8").write("\n".join(L) + "\n")
print("wrote", out, len(L), "lines")
