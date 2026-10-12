import OAI.Computability.FourierCircuit.Core

/-!
# The 8-point Walsh-Hadamard transform, scaled by 1/2, in 20 operations

Written by `slp2lean.py` from `h8_half_o20.txt`; do not edit by hand.

The model is OpenAI's circuit model of `OAI/Computability/FourierCircuit/Core.lean` (namespace
`OAI.ExactFourier`): a `Program n k` is a list of `k` gates on `n` inputs, each gate one addition, one
subtraction or one multiplication by a constant, and each gate costs one.  A `Circuit n` is a program with a
choice of `n` output wires; its `size` is the number of gates.  Wire numbers: `0 .. n-1` are the inputs,
`n` is the constant 0, and `n+1+t` is the result of gate number `t` (counted from 0).

This file adds nothing to the model.  It contains: the matrix `hadamard k` (same formula as the function
`OAI.PowerSaving.WHT.wht` of this repository), two lemmas that read one wire of a program, the program as
data, and the statement that the circuit computes `(1/2) * H` with `20` gates.
-/

namespace OAI
namespace ExactFourier
namespace WHT8Half
noncomputable section

/-- The Walsh-Hadamard matrix on `2^k` points in natural (Sylvester) order: the entry in row `j` and column
`l` is `(-1)^(number of common 1-bits of j and l)`.  Entry formula copied from `OAI.PowerSaving.WHT.wht`. -/
def hadamard (k : ℕ) : Matrix (Fin (2 ^ k)) (Fin (2 ^ k)) ℂ :=
  fun j l => ∏ i ∈ Finset.range k, if j.val.testBit i && l.val.testBit i then (-1 : ℂ) else 1

/-- The same matrix for `k = 3`, with the index type written `Fin 8`. -/
def H : Matrix (Fin 8) (Fin 8) ℂ :=
  fun j l => ∏ i ∈ Finset.range 3, if j.val.testBit i && l.val.testBit i then (-1 : ℂ) else 1

theorem H_eq_hadamard : H = hadamard 3 := rfl

/-- Reading a wire of the empty program: an input, or the constant 0. -/
theorem eval_nil_apply {n : ℕ} (x : Fin n → ℂ) (i : Fin (n + 1 + 0)) :
    (Program.nil : Program n 0).eval x i = if h : i.val < n then x ⟨i.val, h⟩ else 0 := by
  by_cases h : i.val < n
  · simp [Program.eval, Fin.snoc, h, Fin.castLT]
  · simp [Program.eval, Fin.snoc, h]

/-- Reading a wire after one more gate: an older wire, or the value of the new gate. -/
theorem eval_step_apply {n k : ℕ} (p : Program n k) (g : Gate (n + 1 + k)) (x : Fin n → ℂ)
    (i : Fin (n + 1 + (k + 1))) :
    (Program.step p g).eval x i =
      if h : i.val < n + 1 + k then p.eval x ⟨i.val, h⟩ else g.eval (p.eval x) := by
  by_cases h : i.val < n + 1 + k
  · simp [Program.eval, Fin.snoc, h, Fin.castLT]
  · simp [Program.eval, Fin.snoc, h]

/-! ## The program, one definition per gate -/

def p0 : Program 8 0 := .nil
/-- wire 9:  `g1  = x0 + x7` -/
def p1 : Program 8 1 := .step p0 (.add ⟨0, by decide⟩ ⟨7, by decide⟩)
/-- wire 10:  `g2  = x1 + x6` -/
def p2 : Program 8 2 := .step p1 (.add ⟨1, by decide⟩ ⟨6, by decide⟩)
/-- wire 11:  `g3  = x2 - x5` -/
def p3 : Program 8 3 := .step p2 (.sub ⟨2, by decide⟩ ⟨5, by decide⟩)
/-- wire 12:  `g4  = x3 - x4` -/
def p4 : Program 8 4 := .step p3 (.sub ⟨3, by decide⟩ ⟨4, by decide⟩)
/-- wire 13:  `g5  = g1 - g2` -/
def p5 : Program 8 5 := .step p4 (.sub ⟨9, by decide⟩ ⟨10, by decide⟩)
/-- wire 14:  `g6  = g3 + g4` -/
def p6 : Program 8 6 := .step p5 (.add ⟨11, by decide⟩ ⟨12, by decide⟩)
/-- wire 15:  `g7  = g5 - g6` -/
def p7 : Program 8 7 := .step p6 (.sub ⟨13, by decide⟩ ⟨14, by decide⟩)
/-- wire 16:  `h   = 1/2 * g7` -/
def p8 : Program 8 8 := .step p7 (.scale (1 / 2 : ℂ) ⟨15, by decide⟩)
/-- wire 17:  `a8  = h - x7` -/
def p9 : Program 8 9 := .step p8 (.sub ⟨16, by decide⟩ ⟨7, by decide⟩)
/-- wire 18:  `a9  = h - x5` -/
def p10 : Program 8 10 := .step p9 (.sub ⟨16, by decide⟩ ⟨5, by decide⟩)
/-- wire 19:  `a10 = a8 + x6` -/
def p11 : Program 8 11 := .step p10 (.add ⟨17, by decide⟩ ⟨6, by decide⟩)
/-- wire 20:  `a11 = a9 - x4` -/
def p12 : Program 8 12 := .step p11 (.sub ⟨18, by decide⟩ ⟨4, by decide⟩)
/-- wire 21:  `z7  = a10 + g4` -/
def p13 : Program 8 13 := .step p12 (.add ⟨19, by decide⟩ ⟨12, by decide⟩)
/-- wire 22:  `z3  = a9 + x3` -/
def p14 : Program 8 14 := .step p13 (.add ⟨18, by decide⟩ ⟨3, by decide⟩)
/-- wire 23:  `z5  = g5 - z3` -/
def p15 : Program 8 15 := .step p14 (.sub ⟨13, by decide⟩ ⟨22, by decide⟩)
/-- wire 24:  `z1  = a10 + g3` -/
def p16 : Program 8 16 := .step p15 (.add ⟨19, by decide⟩ ⟨11, by decide⟩)
/-- wire 25:  `z6  = a11 + g2` -/
def p17 : Program 8 17 := .step p16 (.add ⟨20, by decide⟩ ⟨10, by decide⟩)
/-- wire 26:  `z2  = a8 + x1` -/
def p18 : Program 8 18 := .step p17 (.add ⟨17, by decide⟩ ⟨1, by decide⟩)
/-- wire 27:  `z4  = z2 + g6` -/
def p19 : Program 8 19 := .step p18 (.add ⟨26, by decide⟩ ⟨14, by decide⟩)
/-- wire 28:  `z0  = g1 - a11` -/
def p20 : Program 8 20 := .step p19 (.sub ⟨9, by decide⟩ ⟨20, by decide⟩)

/-- The circuit: the 20 gates above, and for every row `j` the wire that holds `(1/2) * (row j of H)`. -/
def circuit : Circuit 8 where
  size := 20
  program := p20
  outputs := ![⟨28, by decide⟩, ⟨24, by decide⟩, ⟨26, by decide⟩, ⟨22, by decide⟩, ⟨27, by decide⟩, ⟨23, by decide⟩, ⟨25, by decide⟩, ⟨21, by decide⟩]

theorem circuit_size : circuit.size = 20 := rfl

/-- **The 8-point Walsh-Hadamard transform, scaled by 1/2, has a circuit with 20 gates** in OpenAI's
model (every addition, subtraction and multiplication by a constant costs one). -/
theorem circuit_computes : circuit.Computes ((1 / 2 : ℂ) • H) := by
  intro x
  obtain ⟨f, rfl⟩ : ∃ f : ℕ → ℂ, x = fun i => f i.val :=
    ⟨fun m => if h : m < 8 then x ⟨m, h⟩ else 0, by funext i; simp⟩
  funext i
  fin_cases i <;>
    simp +decide [Circuit.eval, circuit, p20, p19, p18, p17, p16, p15, p14, p13, p12, p11, p10, p9, p8, p7, p6, p5, p4, p3, p2, p1, p0,
      eval_step_apply, eval_nil_apply, Gate.eval, Matrix.mulVec, dotProduct, H,
      Fin.sum_univ_eight, Finset.prod_range_succ] <;>
    ring

/-- The same statement with the matrix written `hadamard 3`. -/
theorem circuit_computes_hadamard :
    circuit.Computes ((1 / 2 : ℂ) • (hadamard 3 : Matrix (Fin 8) (Fin 8) ℂ)) :=
  circuit_computes

/-- Both facts in one statement. -/
theorem exists_circuit :
    ∃ C : Circuit 8, C.size = 20 ∧ C.Computes ((1 / 2 : ℂ) • (hadamard 3 : Matrix (Fin 8) (Fin 8) ℂ)) :=
  ⟨circuit, circuit_size, circuit_computes_hadamard⟩

end
end WHT8Half
end ExactFourier
end OAI

#print axioms OAI.ExactFourier.WHT8Half.exists_circuit
