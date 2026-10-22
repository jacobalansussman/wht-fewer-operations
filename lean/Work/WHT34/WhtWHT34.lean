import Work.WHT34.ModelWHT34

/-!
# The Walsh-Hadamard transform by halves, and its link to `hadamard`

`wht i u a` is entry `a` of the transform of the block `u 0, ..., u (2^i - 1)`, defined by the split on the
top bit (the textbook butterfly): the first half of the outputs is `H u_L + H u_R`, the second half
`H u_L - H u_R`.  `wht_eq_sum` turns it into the sum with signs `(-1)^(common 1-bits)`, and
`wht_inputs` identifies it with the rows of `hadamard R k`.
-/

namespace MultiplyAdd

/-- The block of `u` that starts at `a`. -/
def shift {V : Type*} (u : ℕ → V) (a : ℕ) : ℕ → V := fun t => u (a + t)

/-- Entry `a` of the Walsh-Hadamard transform of `u 0, ..., u (2^i - 1)`, by the split on the top bit. -/
def wht {V : Type*} [AddCommGroup V] : ℕ → (ℕ → V) → ℕ → V
  | 0, u, _ => u 0
  | i + 1, u, a =>
      if a < 2 ^ i then wht i u a + wht i (shift u (2 ^ i)) a
      else wht i u (a - 2 ^ i) - wht i (shift u (2 ^ i)) (a - 2 ^ i)

section
variable {V : Type*} [AddCommGroup V]

theorem wht_zero (u : ℕ → V) (a : ℕ) : wht 0 u a = u 0 := rfl

theorem wht_lo (i : ℕ) (u : ℕ → V) {a : ℕ} (ha : a < 2 ^ i) :
    wht (i + 1) u a = wht i u a + wht i (shift u (2 ^ i)) a := by
  simp only [wht, ite_eq_left ha]

theorem wht_hi (i : ℕ) (u : ℕ → V) (a : ℕ) :
    wht (i + 1) u (2 ^ i + a) = wht i u a - wht i (shift u (2 ^ i)) a := by
  simp only [wht, ite_eq_right (show ¬ 2 ^ i + a < 2 ^ i by omega), Nat.add_sub_cancel_left]

/-- Two steps of the butterfly: the four entries `d`, `2^j + d`, `2^(j+1) + d`, `2^(j+1) + 2^j + d` of a
block of size `2^(j+2)` from the four quarter pieces `q00, q01, q10, q11` (a 4-point transform). -/
theorem wht_two (j : ℕ) (Y : ℕ → V) {d : ℕ} (hd : d < 2 ^ j) :
    wht (j + 1 + 1) Y d =
      (wht j Y d + wht j (shift Y (2 ^ j)) d) +
        (wht j (shift Y (2 ^ (j + 1))) d + wht j (shift (shift Y (2 ^ (j + 1))) (2 ^ j)) d) ∧
    wht (j + 1 + 1) Y (2 ^ j + d) =
      (wht j Y d - wht j (shift Y (2 ^ j)) d) +
        (wht j (shift Y (2 ^ (j + 1))) d - wht j (shift (shift Y (2 ^ (j + 1))) (2 ^ j)) d) ∧
    wht (j + 1 + 1) Y (2 ^ (j + 1) + d) =
      (wht j Y d + wht j (shift Y (2 ^ j)) d) -
        (wht j (shift Y (2 ^ (j + 1))) d + wht j (shift (shift Y (2 ^ (j + 1))) (2 ^ j)) d) ∧
    wht (j + 1 + 1) Y (2 ^ (j + 1) + (2 ^ j + d)) =
      (wht j Y d - wht j (shift Y (2 ^ j)) d) -
        (wht j (shift Y (2 ^ (j + 1))) d - wht j (shift (shift Y (2 ^ (j + 1))) (2 ^ j)) d) := by
  have h1 : d < 2 ^ (j + 1) := by rw [pow_succ]; omega
  have h2 : 2 ^ j + d < 2 ^ (j + 1) := by rw [pow_succ]; omega
  refine ⟨?_, ?_, ?_, ?_⟩
  · rw [wht_lo (j + 1) Y h1, wht_lo j Y hd, wht_lo j _ hd]
  · rw [wht_lo (j + 1) Y h2, wht_hi j Y d, wht_hi j _ d]
  · rw [wht_hi (j + 1) Y d, wht_lo j Y hd, wht_lo j _ hd]
  · rw [wht_hi (j + 1) Y (2 ^ j + d), wht_hi j Y d, wht_hi j _ d]

end

/-- The sign `(-1)^(number of common 1-bits of a and t below bit i)`, as in `hadamard`. -/
def sgn (R : Type*) [CommRing R] (i a t : ℕ) : R :=
  ∏ l ∈ Finset.range i, if a.testBit l && t.testBit l then (-1 : R) else 1

theorem sgn_succ (R : Type*) [CommRing R] (i a t : ℕ) :
    sgn R (i + 1) a t = sgn R i a t * (if a.testBit i && t.testBit i then (-1 : R) else 1) :=
  Finset.prod_range_succ _ _

theorem sgn_congr (R : Type*) [CommRing R] {i a a' t t' : ℕ} (ha : ∀ l < i, a.testBit l = a'.testBit l)
    (ht : ∀ l < i, t.testBit l = t'.testBit l) : sgn R i a t = sgn R i a' t' := by
  unfold sgn
  refine Finset.prod_congr rfl fun l hl => ?_
  rw [Finset.mem_range] at hl
  rw [ha l hl, ht l hl]

theorem testBit_two_pow_add_self {i t : ℕ} (ht : t < 2 ^ i) : (2 ^ i + t).testBit i = true := by
  rw [Nat.testBit_two_pow_add_eq, Nat.testBit_lt_two_pow ht]
  rfl

/-- The transform by halves is the signed sum. -/
theorem wht_eq_sum (R : Type*) [CommRing R] {V : Type*} [AddCommGroup V] [Module R V] (i : ℕ) :
    ∀ (u : ℕ → V) (a : ℕ), a < 2 ^ i → wht i u a = ∑ t ∈ Finset.range (2 ^ i), sgn R i a t • u t := by
  induction i with
  | zero =>
    intro u a _
    simp [wht, sgn]
  | succ i ih =>
    intro u a ha
    rw [pow_succ, mul_two, Finset.sum_range_add]
    by_cases hai : a < 2 ^ i
    · rw [wht_lo i u hai, ih u a hai, ih (shift u (2 ^ i)) a hai]
      congr 1
      · refine Finset.sum_congr rfl fun t ht => ?_
        rw [Finset.mem_range] at ht
        rw [sgn_succ, Nat.testBit_lt_two_pow ht]
        simp
      · refine Finset.sum_congr rfl fun t ht => ?_
        rw [Finset.mem_range] at ht
        rw [sgn_succ, Nat.testBit_lt_two_pow hai,
          sgn_congr R (a' := a) (t' := t) (fun l _ => rfl)
            (fun l hl => Nat.testBit_two_pow_add_gt hl t)]
        simp [shift]
    · obtain ⟨a', rfl⟩ : ∃ a', a = 2 ^ i + a' := ⟨a - 2 ^ i, by omega⟩
      have ha' : a' < 2 ^ i := by rw [pow_succ] at ha; omega
      rw [wht_hi i u a', ih u a' ha', ih (shift u (2 ^ i)) a' ha', sub_eq_add_neg,
        ← Finset.sum_neg_distrib]
      congr 1
      · refine Finset.sum_congr rfl fun t ht => ?_
        rw [Finset.mem_range] at ht
        rw [sgn_succ, Nat.testBit_lt_two_pow ht,
          sgn_congr R (a' := a') (t' := t) (fun l hl => Nat.testBit_two_pow_add_gt hl a')
            (fun l _ => rfl)]
        simp
      · refine Finset.sum_congr rfl fun t ht => ?_
        rw [Finset.mem_range] at ht
        rw [sgn_succ, testBit_two_pow_add_self ha', testBit_two_pow_add_self ht,
          sgn_congr R (a' := a') (t' := t) (fun l hl => Nat.testBit_two_pow_add_gt hl a')
            (fun l hl => Nat.testBit_two_pow_add_gt hl t)]
        simp [shift]

/-- The inputs of a circuit on `2^k` points, as functions of the input vector (`0` past the end). -/
def inputs (R : Type*) [CommRing R] (k : ℕ) : ℕ → (Fin (2 ^ k) → R) → R :=
  fun t x => if h : t < 2 ^ k then x ⟨t, h⟩ else 0

/-- Row `a` of `hadamard R k` is the transform by halves of the inputs. -/
theorem wht_inputs (R : Type*) [CommRing R] (k : ℕ) (a : Fin (2 ^ k)) :
    wht k (inputs R k) a.val = fun x => (hadamard R k).mulVec x a := by
  rw [wht_eq_sum R k _ a.val a.isLt]
  funext x
  simp only [Finset.sum_apply, Pi.smul_apply, smul_eq_mul, Matrix.mulVec, dotProduct, hadamard]
  rw [← Fin.sum_univ_eq_sum_range]
  refine Finset.sum_congr rfl fun t _ => ?_
  simp [sgn, inputs, t.isLt]

end MultiplyAdd
