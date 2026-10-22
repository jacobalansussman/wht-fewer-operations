import Work.WHT34.ChallengeWHT34

/-!
# Checks of the statement `Work.WHT34.ChallengeWHT34` (not a proof of it)

Controls on the definitions of the statement file, used exactly as they are written there:

1. `hadamard ℤ 1` and `hadamard ℤ 2` are the 2 x 2 and 4 x 4 Sylvester matrices, entry by entry.
2. The statement holds at `k = 0` (no line), `k = 1` (2 lines) and `k = 2` (the 7-line circuit of
   Coppersmith, Feig and Linzer, wired as `tools/circuits/programs/h4_7gates.txt`), over every
   commutative ring.  So the theorem is not false at the small sizes it includes.
3. The textbook count `k 2^k` breaks the bound for every `k ≥ 2`, so the textbook circuit is not a witness.
4. The model is not free: no circuit with fewer than 2 lines computes the 2-point transform over `ℤ`.
5. The model holds the 1994 circuit as printed; the bound is below the 1994 count from `k = 3`; and `hadamard`
   satisfies the 1994 recursion `H_n = H_{n/2} ⊗ H_2` at every size.
6. The bound `4 * size ≤ 3 k 2^k + 2^k` is the README's `(3/4) N log2 N + N/4`, with `N = 2^k`, read in `ℝ`.
7. The README's 19 lines at 8 points (`G8_19` of `tools/circuits/gen.py`) are a circuit of the model for
   `hadamard R 3`, over every commutative ring.
8. Every output costs a line of its own: for every `k ≥ 1`, over every commutative ring with `2 ≠ 0`
   (so `ℤ`, `ℚ`, `ℝ`, `ℂ`), every circuit that computes the `2^k`-point transform has at least `2^k` lines.
-/

namespace MultiplyAdd

/-! ## 1. The matrix -/

example : hadamard ℤ 1 = !![1, 1; 1, -1] := by
  ext i j; fin_cases i <;> fin_cases j <;> simp +decide

example : hadamard ℤ 2 = !![1, 1, 1, 1; 1, -1, 1, -1; 1, 1, -1, -1; 1, -1, -1, 1] := by
  ext i j; fin_cases i <;> fin_cases j <;> simp +decide

/-! ## 2. The statement at k = 0, 1, 2 -/

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

theorem statement_k0 (R : Type*) [CommRing R] :
    ∃ C : Circuit R (2 ^ 0), C.Computes (hadamard R 0) ∧ 4 * C.size ≤ 3 * 0 * 2 ^ 0 + 2 ^ 0 := by
  refine ⟨⟨0, .nil, ![⟨0, by decide⟩]⟩, ?_, by norm_num⟩
  intro x; funext i; fin_cases i
  simp [Circuit.eval, eval_nil_apply, Matrix.mulVec, dotProduct, hadamard]

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

theorem statement_k2 (R : Type*) [CommRing R] :
    ∃ C : Circuit R (2 ^ 2), C.Computes (hadamard R 2) ∧ 4 * C.size ≤ 3 * 2 * 2 ^ 2 + 2 ^ 2 := by
  -- wires: 0..3 inputs, 4 the constant 0, 5 + t line t
  let p : Program R 4 7 :=
    .step (.step (.step (.step (.step (.step (.step .nil
      (.addMul ⟨0, by decide⟩ 1 ⟨1, by decide⟩))          -- 5:  p1   = x0 + x1
      (.addMul ⟨2, by decide⟩ (-1) ⟨3, by decide⟩))       -- 6:  p2   = x2 - x3
      (.addMul ⟨5, by decide⟩ 1 ⟨6, by decide⟩))          -- 7:  hub3 = p1 + p2
      (.addMul ⟨7, by decide⟩ (-2) ⟨2, by decide⟩))       -- 8:  p4   = hub3 - 2*x2
      (.mulSub 2 ⟨0, by decide⟩ ⟨7, by decide⟩))          -- 9:  p5   = 2*x0 - hub3
      (.mulSub 2 ⟨5, by decide⟩ ⟨8, by decide⟩))          -- 10: p6   = 2*p1 - p4
      (.addMul ⟨9, by decide⟩ 2 ⟨6, by decide⟩)           -- 11: p7   = p5 + 2*p2
  refine ⟨⟨7, p, ![⟨10, by decide⟩, ⟨11, by decide⟩, ⟨8, by decide⟩, ⟨9, by decide⟩]⟩, ?_, by norm_num⟩
  intro x
  obtain ⟨f, rfl⟩ : ∃ f : ℕ → R, x = fun i => f i.val :=
    ⟨fun m => if h : m < 4 then x ⟨m, h⟩ else 0, by funext i; simp⟩
  funext i
  fin_cases i <;>
    simp +decide [Circuit.eval, p, eval_step_apply, eval_nil_apply, Gate.eval, Matrix.mulVec,
      dotProduct, hadamard, Fin.sum_univ_four, Finset.prod_range_succ] <;>
    ring

/-! ## 3. The textbook count does not meet the bound -/

theorem textbook_over_bound (k : ℕ) (hk : 2 ≤ k) : 3 * k * 2 ^ k + 2 ^ k < 4 * (k * 2 ^ k) := by
  have : 0 < 2 ^ k := by positivity
  nlinarith

/-! ## 4. The model charges for every new value -/

theorem no_one_line_butterfly :
    ¬ ∃ C : Circuit ℤ (2 ^ 1), C.Computes (hadamard ℤ 1) ∧ C.size ≤ 1 := by
  rintro ⟨⟨s, p, out⟩, h, hs⟩
  have h0 := congrFun (h ![1, 2]) 0
  have h1 := congrFun (h ![1, 2]) 1
  simp only [Circuit.eval, Matrix.mulVec, dotProduct, hadamard] at h0 h1
  interval_cases s
  · cases p
    generalize out 0 = a at h0; generalize out 1 = b at h1
    fin_cases a <;> simp +decide at h0
  · cases p with
    | step p g =>
      cases p
      generalize out 0 = a at h0; generalize out 1 = b at h1
      fin_cases a <;> fin_cases b <;> simp +decide [eval_step_apply, eval_nil_apply] at h0 h1
      all_goals linarith

/-! ## 5. The 1994 paper: its circuit, its count and its recursion -/

/-- The 4-point circuit printed by Coppersmith, Feig and Linzer (1994, page 969), line for line: four plain
additions or subtractions and three multiply-adds `z2 + 2 x`.  Their operations are lines of this model. -/
theorem cfl1994_four_point (R : Type*) [CommRing R] :
    ∃ C : Circuit R (2 ^ 2), C.Computes (hadamard R 2) ∧ C.size = 7 := by
  -- wires: 0..3 inputs, 4 the constant 0, 5 + t line t
  let p : Program R 4 7 :=
    .step (.step (.step (.step (.step (.step (.step .nil
      (.addMul ⟨1, by decide⟩ 1 ⟨2, by decide⟩))          -- 5:  z0 = x1 + x2
      (.addMul ⟨5, by decide⟩ 1 ⟨3, by decide⟩))          -- 6:  z1 = z0 + x3
      (.addMul ⟨0, by decide⟩ (-1) ⟨6, by decide⟩))       -- 7:  z2 = x0 - z1
      (.addMul ⟨0, by decide⟩ 1 ⟨6, by decide⟩))          -- 8:  y0 = x0 + z1
      (.addMul ⟨7, by decide⟩ 2 ⟨2, by decide⟩))          -- 9:  y1 = z2 + 2 x2
      (.addMul ⟨7, by decide⟩ 2 ⟨1, by decide⟩))          -- 10: y2 = z2 + 2 x1
      (.addMul ⟨7, by decide⟩ 2 ⟨3, by decide⟩)           -- 11: y3 = z2 + 2 x3
  refine ⟨⟨7, p, ![⟨8, by decide⟩, ⟨9, by decide⟩, ⟨10, by decide⟩, ⟨11, by decide⟩]⟩, ?_, rfl⟩
  intro x
  obtain ⟨f, rfl⟩ : ∃ f : ℕ → R, x = fun i => f i.val :=
    ⟨fun m => if h : m < 4 then x ⟨m, h⟩ else 0, by funext i; simp⟩
  funext i
  fin_cases i <;>
    simp +decide [Circuit.eval, p, eval_step_apply, eval_nil_apply, Gate.eval, Matrix.mulVec,
      dotProduct, hadamard, Fin.sum_univ_four, Finset.prod_range_succ] <;>
    ring

/-- From `k = 3` on, the bound is below the count of Coppersmith, Feig and Linzer, `(7/8) N log2 N` (times 8:
`2 (3k 2^k + 2^k) < 7k 2^k`); for odd `k` their count is `N/8` higher still. -/
theorem cfl_over_bound (k : ℕ) (hk : 3 ≤ k) : 2 * (3 * k * 2 ^ k + 2 ^ k) < 7 * k * 2 ^ k := by
  have : 0 < 2 ^ k := by positivity
  nlinarith

/-- The recursion of the 1994 paper, its equation (2), `H_n = H_{n/2} ⊗ H_2`: entry `(j, l)` of
`hadamard R (k+1)` is entry `(j/2, l/2)` of `hadamard R k` times entry `(j%2, l%2)` of `hadamard R 1`. -/
theorem hadamard_kron (R : Type*) [CommRing R] (k : ℕ) (j l : Fin (2 ^ (k + 1))) :
    hadamard R (k + 1) j l =
      hadamard R k ⟨j.val / 2, Nat.div_lt_of_lt_mul (j.isLt.trans_eq (pow_succ' 2 k))⟩
          ⟨l.val / 2, Nat.div_lt_of_lt_mul (l.isLt.trans_eq (pow_succ' 2 k))⟩ *
        hadamard R 1 ⟨j.val % 2, by simp; omega⟩ ⟨l.val % 2, by simp; omega⟩ := by
  simp only [hadamard, Finset.prod_range_succ', Nat.testBit_div_two]
  congr 1
  simp [Nat.testBit_zero]

/-! ## 6. The bound is the README's formula -/

/-- `4 * s ≤ 3 k 2^k + 2^k` says exactly that `s ≤ (3/4) N log2 N + N/4` for `N = 2^k`, in `ℝ`, with the
logarithm of Mathlib (`Real.logb 2`).  So the statement is the README's count, in the form of the second
theorem of `Work/SmallWHT/ChallengeWHT8.lean`. -/
theorem bound_iff_real (k s : ℕ) :
    4 * s ≤ 3 * k * 2 ^ k + 2 ^ k ↔
      (s : ℝ) ≤ 3 / 4 * (2 : ℝ) ^ k * Real.logb 2 ((2 : ℝ) ^ k) + (2 : ℝ) ^ k / 4 := by
  have hlog : Real.logb 2 ((2 : ℝ) ^ k) = k := by
    rw [Real.logb_pow, Real.logb_self_eq_one (by norm_num), mul_one]
  rw [hlog, ← Nat.cast_le (α := ℝ)]
  push_cast
  constructor <;> intro h <;> linarith

/-! ## 7. The README's 19 lines at 8 points -/

/-- The 19 lines of the README at 8 points (`tools/circuits/gen.py`, `G8_19`), in this model. -/
theorem hadamard_eight_19 (R : Type*) [CommRing R] :
    ∃ C : Circuit R (2 ^ 3), C.Computes (hadamard R 3) ∧ C.size ≤ 19 := by
  -- wires: 0..7 inputs, 8 the constant 0, 9 + t line t
  let p : Program R 8 19 :=
    .step (.step (.step (.step (.step (.step (.step (.step (.step (.step (.step (.step (.step (.step
    (.step (.step (.step (.step (.step .nil
      (.addMul ⟨0, by decide⟩ 1 ⟨7, by decide⟩))       -- 9:  g1  = x0 + x7
      (.addMul ⟨1, by decide⟩ 1 ⟨6, by decide⟩))       -- 10: g2  = x1 + x6
      (.addMul ⟨2, by decide⟩ (-1) ⟨5, by decide⟩))    -- 11: g3  = x2 - x5
      (.addMul ⟨3, by decide⟩ (-1) ⟨4, by decide⟩))    -- 12: g4  = x3 - x4
      (.addMul ⟨9, by decide⟩ (-1) ⟨10, by decide⟩))   -- 13: g5  = g1 - g2
      (.addMul ⟨11, by decide⟩ 1 ⟨12, by decide⟩))     -- 14: g6  = g3 + g4
      (.addMul ⟨13, by decide⟩ (-1) ⟨14, by decide⟩))  -- 15: g7  = g5 - g6
      (.addMul ⟨15, by decide⟩ (-2) ⟨7, by decide⟩))   -- 16: g8  = g7 - 2 x7
      (.addMul ⟨15, by decide⟩ (-2) ⟨5, by decide⟩))   -- 17: g9  = g7 - 2 x5
      (.addMul ⟨16, by decide⟩ 2 ⟨6, by decide⟩))      -- 18: g10 = g8 + 2 x6
      (.addMul ⟨17, by decide⟩ (-2) ⟨4, by decide⟩))   -- 19: g11 = g9 - 2 x4
      (.addMul ⟨18, by decide⟩ 2 ⟨12, by decide⟩))     -- 20: y7  = g10 + 2 g4
      (.addMul ⟨17, by decide⟩ 2 ⟨3, by decide⟩))      -- 21: y3  = g9 + 2 x3
      (.mulSub 2 ⟨13, by decide⟩ ⟨21, by decide⟩))     -- 22: y5  = -y3 + 2 g5
      (.addMul ⟨18, by decide⟩ 2 ⟨11, by decide⟩))     -- 23: y1  = g10 + 2 g3
      (.addMul ⟨19, by decide⟩ 2 ⟨10, by decide⟩))     -- 24: y6  = g11 + 2 g2
      (.addMul ⟨16, by decide⟩ 2 ⟨1, by decide⟩))      -- 25: y2  = g8 + 2 x1
      (.addMul ⟨25, by decide⟩ 2 ⟨14, by decide⟩))     -- 26: y4  = y2 + 2 g6
      (.mulSub 2 ⟨9, by decide⟩ ⟨19, by decide⟩)       -- 27: y0  = -g11 + 2 g1
  refine ⟨⟨19, p, ![⟨27, by decide⟩, ⟨23, by decide⟩, ⟨25, by decide⟩, ⟨21, by decide⟩,
    ⟨26, by decide⟩, ⟨22, by decide⟩, ⟨24, by decide⟩, ⟨20, by decide⟩]⟩, ?_, le_rfl⟩
  intro x
  obtain ⟨f, rfl⟩ : ∃ f : ℕ → R, x = fun i => f i.val :=
    ⟨fun m => if h : m < 8 then x ⟨m, h⟩ else 0, by funext i; simp⟩
  funext i
  fin_cases i <;>
    simp +decide [Circuit.eval, p, eval_step_apply, eval_nil_apply, Gate.eval, Matrix.mulVec,
      dotProduct, hadamard, Fin.sum_univ_eight, Finset.prod_range_succ] <;>
    ring

/-! ## 8. Every output costs a line of its own, for every `k ≥ 1`

A control that the model charges for what it computes: no output can be an input or the constant 0, and no
two outputs can share a wire. -/

section OutputsCost

variable {R : Type*} [CommRing R]

theorem snoc_val {n : ℕ} (x : Fin n → R) (w : ℕ) (hw : w < n + 1) :
    (Fin.snoc x 0 : Fin (n + 1) → R) ⟨w, hw⟩ = if h : w < n then x ⟨w, h⟩ else 0 := by
  by_cases h : w < n
  · simp [Fin.snoc, h, Fin.castLT]
  · simp [Fin.snoc, h]

/-- Lines never overwrite the inputs or the constant 0. -/
theorem eval_low {n : ℕ} (x : Fin n → R) : ∀ {s : ℕ} (p : Program R n s) (w : Fin (n + 1 + s))
    (hw : w.val < n + 1), p.eval x w = (Fin.snoc x 0 : Fin (n + 1) → R) ⟨w.val, hw⟩
  | 0, .nil, _, _ => rfl
  | _ + 1, .step p g, w, hw => by
      rw [eval_step_apply, dite_eq_left (by omega)]
      exact eval_low x p _ hw

theorem hadamard_entry (k : ℕ) (i l : Fin (2 ^ k)) :
    hadamard R k i l = 1 ∨ hadamard R k i l = -1 := by
  unfold hadamard
  apply Finset.prod_induction _ (fun a : R => a = 1 ∨ a = -1)
  · rintro a b (rfl | rfl) (rfl | rfl) <;> simp
  · simp
  · intro t _; split <;> simp

theorem hadamard_col_pow (k b : ℕ) (hb : b < k) (i : Fin (2 ^ k)) (h : 2 ^ b < 2 ^ k) :
    hadamard R k i ⟨2 ^ b, h⟩ = if i.val.testBit b then -1 else 1 := by
  unfold hadamard
  rw [Finset.prod_eq_single b]
  · simp
  · intro t _ htb
    simp [Ne.symm htb]
  · intro hn; exact absurd (Finset.mem_range.2 hb) hn

theorem exists_bit_ne (k : ℕ) (i i' : Fin (2 ^ k)) (h : i ≠ i') :
    ∃ b < k, i.val.testBit b ≠ i'.val.testBit b := by
  have hv : i.val ≠ i'.val := fun e => h (Fin.ext e)
  by_contra hcon
  push Not at hcon
  apply hv
  apply Nat.eq_of_testBit_eq
  intro b
  by_cases hb : b < k
  · exact hcon b hb
  · have hp : 2 ^ k ≤ 2 ^ b := Nat.pow_le_pow_right (by norm_num) (by omega)
    rw [Nat.testBit_eq_false_of_lt (lt_of_lt_of_le i.isLt hp),
      Nat.testBit_eq_false_of_lt (lt_of_lt_of_le i'.isLt hp)]

/-- Over any commutative ring with `2 ≠ 0`, a circuit for the `2^k`-point transform (`k ≥ 1`) has at
least `2^k` lines: its outputs are `2^k` different lines. -/
theorem size_ge_outputs (h2 : (2 : R) ≠ 0) (k : ℕ) (hk : 1 ≤ k) (C : Circuit R (2 ^ k))
    (hC : C.Computes (hadamard R k)) : 2 ^ k ≤ C.size := by
  obtain ⟨s, p, out⟩ := C
  have h1 : (1 : R) ≠ 0 := by intro h; apply h2; linear_combination 2 * h
  have hne1 : (-1 : R) ≠ 1 := by intro h; apply h2; linear_combination -h
  have hnz : ∀ i l, hadamard R k i l ≠ 0 := by
    intro i l
    rcases hadamard_entry (R := R) k i l with e | e <;> rw [e]
    · exact h1
    · exact neg_ne_zero.2 h1
  have h2k : 2 ≤ 2 ^ k := by
    calc 2 = 2 ^ 1 := by norm_num
      _ ≤ 2 ^ k := Nat.pow_le_pow_right (by norm_num) hk
  -- the circuit at a unit vector gives one column of the matrix
  have key : ∀ i l, p.eval (Pi.single l 1) (out i) = hadamard R k i l := by
    intro i l
    have := congrFun (hC (Pi.single l 1)) i
    simpa [Circuit.eval, Matrix.mulVec, dotProduct, Pi.single_apply] using this
  -- no output is an input or the constant 0
  have high : ∀ i, 2 ^ k + 1 ≤ (out i).val := by
    intro i
    by_contra hlt
    have hw : (out i).val < 2 ^ k + 1 := by omega
    by_cases hin : (out i).val < 2 ^ k
    · obtain ⟨l, hl⟩ : ∃ l : Fin (2 ^ k), l.val ≠ (out i).val := by
        by_cases h0 : (out i).val = 0
        · exact ⟨⟨1, by omega⟩, by simp [h0]⟩
        · exact ⟨⟨0, by omega⟩, by simp; omega⟩
      have e := key i l
      rw [eval_low _ p (out i) hw, snoc_val, dite_eq_left hin] at e
      have hz : (Pi.single l (1 : R) : Fin (2 ^ k) → R) ⟨(out i).val, hin⟩ = 0 := by
        rw [Pi.single_apply, ite_eq_right]
        intro he; apply hl; rw [← he]
      exact hnz i l (e.symm.trans hz)
    · have e := key i ⟨0, by omega⟩
      rw [eval_low _ p (out i) hw, snoc_val, dite_eq_right hin] at e
      exact hnz i _ e.symm
  -- no two outputs share a wire
  have inj : Function.Injective out := by
    intro i i' hii
    by_contra hne
    obtain ⟨b, hb, hbit⟩ := exists_bit_ne k i i' hne
    have hp : 2 ^ b < 2 ^ k := Nat.pow_lt_pow_right (by norm_num) hb
    have e1 := key i ⟨2 ^ b, hp⟩
    have e2 := key i' ⟨2 ^ b, hp⟩
    rw [hii] at e1
    have e := e1.symm.trans e2
    rw [hadamard_col_pow k b hb i hp, hadamard_col_pow k b hb i' hp] at e
    cases hb1 : i.val.testBit b <;> cases hb2 : i'.val.testBit b <;> simp [hb1, hb2] at e hbit
    · exact hne1 e.symm
    · exact hne1 e
  -- so the outputs are `2^k` different lines among the `s` lines
  let f : Fin (2 ^ k) → Fin s := fun i =>
    ⟨(out i).val - (2 ^ k + 1), by have := (out i).isLt; have := high i; omega⟩
  have hf : Function.Injective f := by
    intro i i' e
    apply inj
    apply Fin.ext
    have e' := congrArg Fin.val e
    simp only [f] at e'
    have := high i; have := high i'
    omega
  simpa using Fintype.card_le_of_injective f hf

end OutputsCost

/-- The instance over `ℤ`: with the statement's bound, every witness has between `N` and
`(3/4) N log2 N + N/4` lines. -/
theorem int_size_ge (k : ℕ) (hk : 1 ≤ k) (C : Circuit ℤ (2 ^ k)) (hC : C.Computes (hadamard ℤ k)) :
    2 ^ k ≤ C.size :=
  size_ge_outputs (by norm_num) k hk C hC

end MultiplyAdd

#print axioms MultiplyAdd.statement_k0
#print axioms MultiplyAdd.statement_k1
#print axioms MultiplyAdd.statement_k2
#print axioms MultiplyAdd.textbook_over_bound
#print axioms MultiplyAdd.no_one_line_butterfly
#print axioms MultiplyAdd.cfl1994_four_point
#print axioms MultiplyAdd.cfl_over_bound
#print axioms MultiplyAdd.hadamard_kron
#print axioms MultiplyAdd.bound_iff_real
#print axioms MultiplyAdd.hadamard_eight_19
#print axioms MultiplyAdd.size_ge_outputs
#print axioms MultiplyAdd.int_size_ge
