import Mathlib

/-!
# The Walsh-Hadamard transform written as a sum: the function `wht`

This file holds one definition, `wht`, and three small checks of it.  It is not from github.com/openai/math.

Why it is here.  The theorems of this repository are stated for the matrix `hadamard k` of
`Work/SmallWHT/H8Half.lean`.  The file `Work/SmallWHT/H8Bridge.lean` checks that multiplying by that matrix
is the function `wht` below, in which each output is written out as a sum of the inputs with signs.

Where it comes from.  Lines 26 to 30 and 32 to 45 of this file are lines 35 to 39 and 66 to 79 of the file
`WHTCheck/Solution.lean` of the repository github.com/jacobalansussman/wht-power-saving-lean, unchanged.
That file has 474 lines: after this definition it goes on to programs for another model of computation,
which nothing here uses, and it imports 40 files of openai/math for them.  Only the definition is repeated
here, so that this repository needs none of that.  The module keeps the name `WHTCheck.Solution` and the
namespace `OAI.PowerSaving.WHT` of that file, because `H8Bridge.lean` was written and checked against that
file and is kept here unchanged.  This file imports only Mathlib.
-/

namespace OAI
namespace PowerSaving
namespace WHT
noncomputable section

/-- Walsh-Hadamard transform of length `2^k` in natural (Sylvester) order:
`wht k x j = ∑ l, (-1)^(number of common 1-bits of j and l) * x l`. -/
def wht (k : ℕ) (x : Fin (2^k) → ℂ) : Fin (2^k) → ℂ :=
  fun j => ∑ l : Fin (2^k),
    (∏ i ∈ Finset.range k, if j.val.testBit i && l.val.testBit i then (-1 : ℂ) else 1) * x l

/-! Sanity checks of the definition `wht` (sizes 2 and 4). -/
example (x : Fin 2 → ℂ) : wht 1 x (0 : Fin 2) = x 0 + x 1 := by
  change ∑ l : Fin 2, (∏ i ∈ Finset.range 1,
    if (0:ℕ).testBit i && l.val.testBit i then (-1 : ℂ) else 1) * x l = _
  simp [Fin.sum_univ_two]
example (x : Fin 2 → ℂ) : wht 1 x (1 : Fin 2) = x 0 - x 1 := by
  change ∑ l : Fin 2, (∏ i ∈ Finset.range 1,
    if (1:ℕ).testBit i && l.val.testBit i then (-1 : ℂ) else 1) * x l = _
  simp [Fin.sum_univ_two, sub_eq_add_neg]
example (x : Fin 4 → ℂ) : wht 2 x (3 : Fin 4) = x 0 - x 1 - x 2 + x 3 := by
  change ∑ l : Fin 4, (∏ i ∈ Finset.range 2,
    if (3:ℕ).testBit i && l.val.testBit i then (-1 : ℂ) else 1) * x l = _
  simp +decide [Fin.sum_univ_four, Finset.prod_range_succ]
  ring

end
end WHT
end PowerSaving
end OAI
