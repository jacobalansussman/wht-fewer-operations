import Mathlib

/-!
# Statement only: the Walsh-Hadamard transform on `N = 8^j` points in at most `(5/6) N log2 N + N` gates

Module `Work.SmallWHT.ChallengeWHT8` (not part of github.com/openai/math).

This file contains NO proof: both theorems end in `sorry`, on purpose.  It is the statement alone, written so
that a reader can check what is claimed without reading anything else.  It imports only Mathlib.

Lines 25 to 62 are lines 12 to 49 of `lean/ComparatorChallenges/ExactFourier.lean` of openai/math, unchanged:
OpenAI's statement of the circuit model.  A gate is one addition, one subtraction or one multiplication by a
constant, and `Circuit.size` is the number of gates.  The same declarations are in
`OAI/Computability/FourierCircuit/Core.lean`, which the proofs import.  After them come one definition, the
matrix `hadamard k`, and the two statements.

The proofs are in `H8Half.lean`, `HadamardDigits.lean`, `TensorPow8.lean` and `TensorPow8Real.lean`, where
the same definition and the same two statements appear under the same names.
-/

namespace OAI

namespace ExactFourier

/-- One charged scalar gate, referencing only available values. -/
inductive Gate (w : ℕ) where
  | add (i j : Fin w)
  | sub (i j : Fin w)
  | scale (c : ℂ) (i : Fin w)

def Gate.eval {w : ℕ} (v : Fin w → ℂ) : Gate w → ℂ
  | .add i j => v i + v j
  | .sub i j => v i - v j
  | .scale c i => c * v i

/-- A topologically ordered scalar DAG; available values are never consumed. -/
inductive Program (n : ℕ) : ℕ → Type where
  | nil : Program n 0
  | step {k : ℕ} (p : Program n k) (g : Gate (n + 1 + k)) : Program n (k + 1)

def Program.eval {n : ℕ} : {k : ℕ} → Program n k → (Fin n → ℂ) →
    (Fin (n + 1 + k) → ℂ)
  | 0, .nil, x => Fin.snoc x 0
  | _ + 1, .step p g, x =>
      let v := p.eval x
      Fin.snoc v (g.eval v)

/-- Outputs name available values, so permutations and arbitrary fanout are uncharged. -/
structure Circuit (n : ℕ) where
  size : ℕ
  program : Program n size
  outputs : Fin n → Fin (n + 1 + size)

def Circuit.eval {n : ℕ} (C : Circuit n) (x : Fin n → ℂ) : Fin n → ℂ :=
  fun i => C.program.eval x (C.outputs i)

noncomputable def zeta (n : ℕ) : ℂ := Complex.exp (2 * Real.pi * Complex.I / (n : ℂ))
noncomputable def fourierMatrix (n : ℕ) : Matrix (Fin n) (Fin n) ℂ :=
  fun j k => zeta n ^ (j.val * k.val)

def Circuit.Computes {n : ℕ} (C : Circuit n) (A : Matrix (Fin n) (Fin n) ℂ) : Prop :=
  ∀ x, C.eval x = A.mulVec x

end ExactFourier

namespace ExactFourier
namespace WHT8Half
noncomputable section

/-- The Walsh-Hadamard matrix on `2^k` points in natural (Sylvester) order: the entry in row `j` and column
`l` is `(-1)^(number of common 1-bits of j and l)`.  Entry formula copied from `OAI.PowerSaving.WHT.wht`. -/
def hadamard (k : ℕ) : Matrix (Fin (2 ^ k)) (Fin (2 ^ k)) ℂ :=
  fun j l => ∏ i ∈ Finset.range k, if j.val.testBit i && l.val.testBit i then (-1 : ℂ) else 1

/-- For every `j` there is a circuit on `N = 2^(3 j)` points that computes the exact Walsh-Hadamard transform
with at most `20 * (j * 8^(j-1)) + 8^j` gates. -/
theorem hadamard_pow8_circuit (j : ℕ) :
    ∃ C : Circuit (2 ^ (3 * j)),
      C.Computes (hadamard (3 * j)) ∧ C.size ≤ 20 * (j * 8 ^ (j - 1)) + 8 ^ j := by
  sorry

/-- The same count in the usual form: at most `(5/6) N log2 N + N` gates. -/
theorem hadamard_pow8_circuit_real (j : ℕ) :
    ∃ C : Circuit (2 ^ (3 * j)), C.Computes (hadamard (3 * j)) ∧
      (C.size : ℝ) ≤
        5 / 6 * (2 : ℝ) ^ (3 * j) * Real.logb 2 ((2 : ℝ) ^ (3 * j)) + (2 : ℝ) ^ (3 * j) := by
  sorry

end
end WHT8Half
end ExactFourier

end OAI
