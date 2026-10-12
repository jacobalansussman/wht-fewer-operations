import Work.SmallWHT.TensorPow8

/-!
# The count of `TensorPow8.lean` in the usual form: `(5/6) N log2 N + N`

`TensorPow8.lean` bounds the number of gates by the integer `20 * (j * 8^(j-1)) + 8^j`.  This file rewrites
that integer: with `N = 2^(3 j)` points it is `(5/6) * N * log2 N + N` (real numbers, `Real.logb 2`).
-/

namespace OAI
namespace ExactFourier
namespace WHT8Half

/-- `20 * j * 8^(j-1) = (5/6) * 8^j * (3 j)`, for every `j` (both sides are 0 at `j = 0`). -/
theorem count_eq (j : ℕ) :
    (20 : ℝ) * ((j : ℝ) * (8 : ℝ) ^ (j - 1)) = 5 / 6 * (8 : ℝ) ^ j * (3 * (j : ℝ)) := by
  rcases j with _ | j
  · simp
  · rw [Nat.add_sub_cancel, pow_succ]
    push_cast
    ring

/-- **The exact Walsh-Hadamard transform on `N = 2^(3 j)` points has a circuit of OpenAI's model with at
most `(5/6) N log2 N + N` gates.** -/
theorem hadamard_pow8_circuit_real (j : ℕ) :
    ∃ C : Circuit (2 ^ (3 * j)), C.Computes (hadamard (3 * j)) ∧
      (C.size : ℝ) ≤
        5 / 6 * (2 : ℝ) ^ (3 * j) * Real.logb 2 ((2 : ℝ) ^ (3 * j)) + (2 : ℝ) ^ (3 * j) := by
  obtain ⟨C, hc, hs⟩ := hadamard_pow8_circuit j
  refine ⟨C, hc, ?_⟩
  have hlog : Real.logb 2 ((2 : ℝ) ^ (3 * j)) = ((3 * j : ℕ) : ℝ) := by
    rw [Real.logb_pow, Real.logb_self_eq_one (by norm_num), mul_one]
  have h8 : (2 : ℝ) ^ (3 * j) = (8 : ℝ) ^ j := by
    rw [pow_mul]
    norm_num
  have hsR : (C.size : ℝ) ≤ 20 * ((j : ℝ) * (8 : ℝ) ^ (j - 1)) + (8 : ℝ) ^ j := by
    exact_mod_cast hs
  rw [hlog, h8]
  push_cast
  linarith [count_eq j, hsR]

end WHT8Half
end ExactFourier
end OAI

#print axioms OAI.ExactFourier.WHT8Half.hadamard_pow8_circuit_real
