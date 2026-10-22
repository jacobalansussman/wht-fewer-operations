import Work.WHT34.FamilyWHT34

/-!
# Proof of `Work.WHT34.ChallengeWHT34`: the transform on `2^k` points in `(3/4) N log2 N + N/4` multiply-adds

The definitions are those of the statement, copied character for character in `ModelWHT34.lean`.  The
theorem below is the statement's, with the same name and the same text.

* `k = 0` and `k = 1`: the identity (no line) and the butterfly (2 lines), checked line by line.
* `k = j + 2`: the family of `FamilyWHT34.lean` (the paper's Theorem B, which carries the 4-point idea of
  Coppersmith, Feig and Linzer to every power of two), with exactly `(3k+1) 2^(k-2)` lines, so `4 * size`
  equals the bound.
-/

namespace MultiplyAdd

/-- `k = 0`: no line; the output is the input. -/
theorem statement_k0 (R : Type*) [CommRing R] :
    ∃ C : Circuit R (2 ^ 0), C.Computes (hadamard R 0) ∧ 4 * C.size ≤ 3 * 0 * 2 ^ 0 + 2 ^ 0 := by
  refine ⟨⟨0, .nil, ![⟨0, by decide⟩]⟩, ?_, by norm_num⟩
  intro x; funext i; fin_cases i
  simp [Circuit.eval, eval_nil_apply, Matrix.mulVec, dotProduct, hadamard]

/-- `k = 1`: the butterfly, two lines. -/
theorem statement_k1 (R : Type*) [CommRing R] :
    ∃ C : Circuit R (2 ^ 1), C.Computes (hadamard R 1) ∧ 4 * C.size ≤ 3 * 1 * 2 ^ 1 + 2 ^ 1 := by
  -- wires: 0, 1 inputs, 2 the constant 0, 3 + t line t
  let p : Program R 2 2 :=
    .step (.step .nil (.addMul ⟨0, by decide⟩ 1 ⟨1, by decide⟩)) (.addMul ⟨0, by decide⟩ (-1) ⟨1, by decide⟩)
  refine ⟨⟨2, p, ![⟨3, by decide⟩, ⟨4, by decide⟩]⟩, ?_, by norm_num⟩
  intro x; funext i
  fin_cases i <;>
    simp +decide [Circuit.eval, p, eval_step_apply, eval_nil_apply, Gate.eval, Matrix.mulVec,
      dotProduct, hadamard, Fin.sum_univ_two]

/-- For every commutative ring `R` and every `k`, the exact (unscaled) Walsh-Hadamard transform on
`N = 2^k` points has a multiply-add circuit with at most `(3/4) N log2 N + N/4` lines.  Since `log2 N = k`,
the bound is written times 4, without division: `4 * size ≤ 3 k 2^k + 2^k`.  For `k ≥ 2` the bound is a
whole number, and a circuit with fewer lines can be padded with unused ones, so the theorem also gives a
circuit with exactly that many lines; for `k = 0` and `k = 1` it allows 0 and 2 lines (the identity and the
butterfly). -/
theorem hadamard_mulAdd_circuit (R : Type*) [CommRing R] (k : ℕ) :
    ∃ C : Circuit R (2 ^ k), C.Computes (hadamard R k) ∧ 4 * C.size ≤ 3 * k * 2 ^ k + 2 ^ k := by
  rcases k with _ | _ | j
  · exact statement_k0 R
  · exact statement_k1 R
  · obtain ⟨C, hC, hsize⟩ := family R j
    exact ⟨C, hC, hsize.le⟩

end MultiplyAdd

#print axioms MultiplyAdd.hadamard_mulAdd_circuit
