import WHTCheck.Solution
import Work.SmallWHT.H8Half

/-!
# The 20-gate circuit and the function `wht` of this repository

`H8Half.lean` states its result for the matrix `hadamard k`.  This file checks that `hadamard k` is the matrix
of `OAI.PowerSaving.WHT.wht k`, the Walsh-Hadamard transform in which the main theorems of the repository are
stated, so that the circuit computes one half of `wht 3`.
-/

namespace OAI
namespace ExactFourier
namespace WHT8Half
open OAI.PowerSaving.WHT

/-- `wht k` is multiplication by the matrix `hadamard k`. -/
theorem wht_eq_mulVec (k : ℕ) (x : Fin (2 ^ k) → ℂ) : wht k x = (hadamard k).mulVec x := rfl

/-- Every output of the 20-gate circuit is one half of the corresponding output of `wht 3`. -/
theorem circuit_eval_eq_wht (x : Fin 8 → ℂ) (j : Fin 8) :
    circuit.eval x j = (1 / 2 : ℂ) * wht 3 x j := by
  rw [circuit_computes_hadamard x, Matrix.smul_mulVec]
  rfl

end WHT8Half
end ExactFourier
end OAI

#print axioms OAI.ExactFourier.WHT8Half.circuit_eval_eq_wht
