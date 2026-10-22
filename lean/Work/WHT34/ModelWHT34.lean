import Mathlib

/-!
# The multiply-add circuit model (proof side of `Work.WHT34.ChallengeWHT34`)

Lines 41-79 of `ChallengeWHT34.lean` (from `Gate` to `hadamard`), copied character for character, in the
same namespace `MultiplyAdd`, so that the solution states the same theorem about the same declarations.
After them come two lemmas that read a wire of a program (as in `Work/SmallWHT/H8Half.lean`).
-/

namespace MultiplyAdd

/-- One line, cost one: `v i + c * v j`, or `c * v j - v i`, where `v i`, `v j` are available values and
`c` is a constant.  Each is one multiply-add `±a ± b·c` of Coppersmith, Feig and Linzer (1994). -/
inductive Gate (R : Type*) (w : ℕ) where
  | addMul (i : Fin w) (c : R) (j : Fin w)
  | mulSub (c : R) (j : Fin w) (i : Fin w)

def Gate.eval {R : Type*} [CommRing R] {w : ℕ} (v : Fin w → R) : Gate R w → R
  | .addMul i c j => v i + c * v j
  | .mulSub c j i => c * v j - v i

/-- A topologically ordered scalar DAG; available values are never consumed. -/
inductive Program (R : Type*) (n : ℕ) : ℕ → Type _ where
  | nil : Program R n 0
  | step {k : ℕ} (p : Program R n k) (g : Gate R (n + 1 + k)) : Program R n (k + 1)

def Program.eval {R : Type*} [CommRing R] {n : ℕ} : {k : ℕ} → Program R n k → (Fin n → R) →
    (Fin (n + 1 + k) → R)
  | 0, .nil, x => Fin.snoc x 0
  | _ + 1, .step p g, x =>
      let v := p.eval x
      Fin.snoc v (g.eval v)

/-- Outputs name available values, so permutations and arbitrary fanout are uncharged. -/
structure Circuit (R : Type*) (n : ℕ) where
  size : ℕ
  program : Program R n size
  outputs : Fin n → Fin (n + 1 + size)

def Circuit.eval {R : Type*} [CommRing R] {n : ℕ} (C : Circuit R n) (x : Fin n → R) : Fin n → R :=
  fun i => C.program.eval x (C.outputs i)

def Circuit.Computes {R : Type*} [CommRing R] {n : ℕ} (C : Circuit R n)
    (A : Matrix (Fin n) (Fin n) R) : Prop :=
  ∀ x, C.eval x = A.mulVec x

/-- The Walsh-Hadamard matrix on `2^k` points in natural (Sylvester) order, over `R`: the entry in row `j`
and column `l` is `(-1)^(number of common 1-bits of j and l)`. -/
def hadamard (R : Type*) [CommRing R] (k : ℕ) : Matrix (Fin (2 ^ k)) (Fin (2 ^ k)) R :=
  fun j l => ∏ i ∈ Finset.range k, if j.val.testBit i && l.val.testBit i then (-1 : R) else 1

/-- Reading a wire of the empty program: an input, or the constant 0 (as in `H8Half.lean`). -/
theorem eval_nil_apply {R : Type*} [CommRing R] {n : ℕ} (x : Fin n → R) (i : Fin (n + 1 + 0)) :
    (Program.nil : Program R n 0).eval x i = if h : i.val < n then x ⟨i.val, h⟩ else 0 := by
  by_cases h : i.val < n
  · simp [Program.eval, Fin.snoc, h, Fin.castLT]
  · simp [Program.eval, Fin.snoc, h]

/-- Reading a wire after one more line: an older wire, or the value of the new line. -/
theorem eval_step_apply {R : Type*} [CommRing R] {n k : ℕ} (p : Program R n k) (g : Gate R (n + 1 + k))
    (x : Fin n → R) (i : Fin (n + 1 + (k + 1))) :
    (Program.step p g).eval x i =
      if h : i.val < n + 1 + k then p.eval x ⟨i.val, h⟩ else g.eval (p.eval x) := by
  by_cases h : i.val < n + 1 + k
  · simp [Program.eval, Fin.snoc, h, Fin.castLT]
  · simp [Program.eval, Fin.snoc, h]

end MultiplyAdd
