import Work.SmallWHT.H8Half

/-!
# The matrix `hadamard k` is a product over binary digits

`hadamard k` (file `H8Half.lean`) is written with `Nat.testBit`, as the function `wht` of this repository is.
This file rewrites every entry as a product, over the `k` binary digits of the two addresses, of entries of the
2-point matrix `H2 = [[1, 1], [1, -1]]`.  That is the form in which OpenAI's files write a Kronecker power.
Only Mathlib and `H8Half.lean` are used.
-/

namespace OAI
namespace ExactFourier
namespace WHT8Half
noncomputable section

/-- The 2-point Walsh-Hadamard matrix `[[1, 1], [1, -1]]`. -/
def H2 : Matrix (Fin 2) (Fin 2) ℂ := fun a b => if a.val = 1 ∧ b.val = 1 then -1 else 1

/-- Entry `(j, l)` of `hadamard k` is the product over the digits `i < k` of `H2 (digit i of j) (digit i of l)`.
`finFunctionFinEquiv.symm j i` is Mathlib's name for digit `i` of `j` in base 2. -/
theorem hadamard_eq_digits (k : ℕ) (j l : Fin (2 ^ k)) :
    hadamard k j l =
      ∏ i : Fin k, H2 ((finFunctionFinEquiv.symm j) i) ((finFunctionFinEquiv.symm l) i) := by
  unfold hadamard
  rw [← Fin.prod_univ_eq_prod_range
    (fun i => if j.val.testBit i && l.val.testBit i then (-1 : ℂ) else 1) k]
  refine Finset.prod_congr rfl fun i _ => ?_
  simp [H2, finFunctionFinEquiv_symm_apply_val, Nat.testBit_eq_decide_div_mod_eq]

end
end WHT8Half
end ExactFourier
end OAI

#print axioms OAI.ExactFourier.WHT8Half.hadamard_eq_digits
