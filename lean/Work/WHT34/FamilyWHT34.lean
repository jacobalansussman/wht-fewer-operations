import Work.WHT34.ReachWHT34
import Work.WHT34.WhtWHT34

/-!
# The count-(G) family: `(3k+1) 2^(k-2)` multiply-add lines for the transform on `2^k` points

The family of the paper's Theorem B, built by its procedure `E(X, s)` (`paper/explicit-wht-circuits.tex`,
the section on count G), which is also written out in the first lines of `tools/circuits/gen.py`.  The four
quarter pieces of a block are named `q00, q01, q10, q11` here; they are gen.py's `q(L0), q(L1), q(R0), q(R1)`.

* `group_mid_alg`, `group_top_alg`: the algebra of the paper's hub lemma, as lines of the model.  Write
  `A = q00 + q01`, `B = q10 - q11`, the hub `M = A + c B` (`c = ±1`), and the four outputs
  `w00 = A + (q10 + q11)`, `w10 = A - (q10 + q11)`, `w01 = (q00 - q01) + B`, `w11 = (q00 - q01) - B`.  Each
  output is `±M ± 2 q` for one quarter value `q` (eight identities, one for each output and each `c`), and
  `w00 + w10 = 2A`, `w01 - w11 = 2B` (two more).  A group of three lines (a hub and two table lines) makes
  the two outputs of one half, and the five lines of the top make all four outputs.  The hub constant `c`
  and the quarter values used follow the choice rule: both lines of a group use quarter values with the
  same second index `τ` (gen.py's `c = -s` when `d < m/8` and `c = s` when `d >= m/8`).
* `E_spec`: the block of size `2^(j+1)` given by `Y`; with `ecount j` lines it makes the half `Half j σ Y` of
  its pieces, and the quarter values `Kept j Y` that its parent needs.
* `top_spec`: the whole transform of a block of size `2^(j+2)` with `2 ecount j + 5 2^j` lines.
* `four_ecount`: `4 ecount j = 2^(j+1) (3j + 2)`, so the total is `(3k+1) 2^(k-2)` for `k = j + 2`.
-/

namespace MultiplyAdd

variable {R : Type*} [CommRing R] {n : ℕ}

/-! ## One group of lines: the ten identities -/

/-- A middle group: hub `A + c B`, then the two outputs `w_{σ0}`, `w_{σ1}` of half `σ`, each one line from the
hub and one quarter value with second index `τ`.  Here `A = q00 + q01`, `B = q10 - q11`. -/
theorem group_mid_alg {m : ℕ} {S : Set (Form R n)} (h : Avail m S) {q00 q01 q10 q11 : Form R n}
    (hA : q00 + q01 ∈ S) (hB : q10 - q11 ∈ S) (σ : Bool) (τ : Prop) [Decidable τ]
    (hq0 : (if τ then q01 else q00) ∈ S) (hq1 : (if τ then q11 else q10) ∈ S) :
    ∃ T, Avail (m + 3) T ∧ S ⊆ T ∧
      (bif σ then (q00 + q01) - (q10 + q11) else (q00 + q01) + (q10 + q11)) ∈ T ∧
      (bif σ then (q00 - q01) - (q10 - q11) else (q00 - q01) + (q10 - q11)) ∈ T := by
  by_cases hτ : τ
  · simp only [hτ, ↓reduceIte] at hq0 hq1
    cases σ <;> simp only [Bool.cond_false, Bool.cond_true]
    · -- σ = 0, τ = 1: c = 1;  w00 = M + 2 q11,  w01 = M - 2 q01
      exact h.three hA hB hq1 hq0 1 1 2 1 (-2) (Or.inl rfl) (Or.inl rfl) (by module) (by module)
    · -- σ = 1, τ = 1: c = -1;  w10 = M - 2 q11,  w11 = M - 2 q01
      exact h.three hA hB hq1 hq0 (-1) 1 (-2) 1 (-2) (Or.inl rfl) (Or.inl rfl) (by module) (by module)
  · simp only [hτ, ↓reduceIte] at hq0 hq1
    cases σ <;> simp only [Bool.cond_false, Bool.cond_true]
    · -- σ = 0, τ = 0: c = -1;  w00 = M + 2 q10,  w01 = -M + 2 q00
      exact h.three hA hB hq1 hq0 (-1) 1 2 (-1) 2 (Or.inl rfl) (Or.inr rfl) (by module) (by module)
    · -- σ = 1, τ = 0: c = 1;  w10 = M - 2 q10,  w11 = -M + 2 q00
      exact h.three hA hB hq1 hq0 1 1 (-2) (-1) 2 (Or.inl rfl) (Or.inr rfl) (by module) (by module)

/-- The top group: hub `A + B`, two table lines, and the two partner lines `-w + 2A` and `w ± 2B`. -/
theorem group_top_alg {m : ℕ} {S : Set (Form R n)} (h : Avail m S) {q00 q01 q10 q11 : Form R n}
    (hA : q00 + q01 ∈ S) (hB : q10 - q11 ∈ S) (τ : Prop) [Decidable τ]
    (hq0 : (if τ then q01 else q00) ∈ S) (hq1 : (if τ then q11 else q10) ∈ S) :
    ∃ T, Avail (m + 5) T ∧ S ⊆ T ∧
      (q00 + q01) + (q10 + q11) ∈ T ∧ (q00 - q01) + (q10 - q11) ∈ T ∧
      (q00 + q01) - (q10 + q11) ∈ T ∧ (q00 - q01) - (q10 - q11) ∈ T := by
  by_cases hτ : τ
  · simp only [hτ, ↓reduceIte] at hq0 hq1
    -- τ = 1: w00 = M + 2 q11, w01 = M - 2 q01, w10 = -w00 + 2A, w11 = w01 - 2B
    obtain ⟨T, hT, hST, h00, h01, h10, h11⟩ := h.five hA hB hq1 hq0 1 2 1 (-2) (-2)
      (Or.inl rfl) (Or.inl rfl) (u0 := (q00 + q01) + (q10 + q11)) (u1 := (q00 - q01) + (q10 - q11))
      (u2 := (q00 + q01) - (q10 + q11)) (u3 := (q00 - q01) - (q10 - q11))
      (by module) (by module) (by module) (by module)
    exact ⟨T, hT, hST, h00, h01, h10, h11⟩
  · simp only [hτ, ↓reduceIte] at hq0 hq1
    -- τ = 0: w10 = M - 2 q10, w11 = -M + 2 q00, w00 = -w10 + 2A, w01 = w11 + 2B
    obtain ⟨T, hT, hST, h10, h11, h00, h01⟩ := h.five hA hB hq1 hq0 1 (-2) (-1) 2 2
      (Or.inl rfl) (Or.inr rfl) (u0 := (q00 + q01) - (q10 + q11)) (u1 := (q00 - q01) - (q10 - q11))
      (u2 := (q00 + q01) + (q10 + q11)) (u3 := (q00 - q01) + (q10 - q11))
      (by module) (by module) (by module) (by module)
    exact ⟨T, hT, hST, h00, h01, h10, h11⟩

/-! ## The same groups, on pieces of a block -/

/-- A middle group of the block `Y` of size `2^(j+2)` at hub index `d < 2^j`: from `A = (L, d)`,
`B = (R, 2^j + d)` and the two quarter values with second index `τ = [2^j ≤ 2d]`, three lines make the
pieces `σ 2^(j+1) + d` and `σ 2^(j+1) + 2^j + d` of `Y`. -/
theorem group_mid (j : ℕ) (Y : ℕ → Form R n) {d : ℕ} (hd : d < 2 ^ j) (σ : Bool) {m : ℕ}
    {S : Set (Form R n)} (h : Avail m S)
    (hA : wht (j + 1) Y d ∈ S) (hB : wht (j + 1) (shift Y (2 ^ (j + 1))) (2 ^ j + d) ∈ S)
    (hL : (if 2 ^ j ≤ 2 * d then wht j (shift Y (2 ^ j)) d else wht j Y d) ∈ S)
    (hR : (if 2 ^ j ≤ 2 * d then wht j (shift (shift Y (2 ^ (j + 1))) (2 ^ j)) d
      else wht j (shift Y (2 ^ (j + 1))) d) ∈ S) :
    ∃ T, Avail (m + 3) T ∧ S ⊆ T ∧
      wht (j + 1 + 1) Y (bif σ then 2 ^ (j + 1) + d else d) ∈ T ∧
      wht (j + 1 + 1) Y (bif σ then 2 ^ (j + 1) + (2 ^ j + d) else 2 ^ j + d) ∈ T := by
  obtain ⟨e0, e1, e2, e3⟩ := wht_two j Y hd
  rw [wht_lo j Y hd] at hA
  rw [wht_hi j _ d] at hB
  obtain ⟨T, hT, hST, h0, h1⟩ := group_mid_alg h hA hB σ (2 ^ j ≤ 2 * d) hL hR
  refine ⟨T, hT, hST, ?_, ?_⟩ <;> cases σ <;> simp only [Bool.cond_true, Bool.cond_false] at h0 h1 ⊢
  · rw [e0]; exact h0
  · rw [e2]; exact h0
  · rw [e1]; exact h1
  · rw [e3]; exact h1

/-- The top group at hub index `d < 2^j` of the block `Y` of size `2^(j+2)`: five lines make its four
pieces `d`, `2^j + d`, `2^(j+1) + d`, `2^(j+1) + 2^j + d`. -/
theorem group_top (j : ℕ) (Y : ℕ → Form R n) {d : ℕ} (hd : d < 2 ^ j) {m : ℕ}
    {S : Set (Form R n)} (h : Avail m S)
    (hA : wht (j + 1) Y d ∈ S) (hB : wht (j + 1) (shift Y (2 ^ (j + 1))) (2 ^ j + d) ∈ S)
    (hL : (if 2 ^ j ≤ 2 * d then wht j (shift Y (2 ^ j)) d else wht j Y d) ∈ S)
    (hR : (if 2 ^ j ≤ 2 * d then wht j (shift (shift Y (2 ^ (j + 1))) (2 ^ j)) d
      else wht j (shift Y (2 ^ (j + 1))) d) ∈ S) :
    ∃ T, Avail (m + 5) T ∧ S ⊆ T ∧
      wht (j + 1 + 1) Y d ∈ T ∧ wht (j + 1 + 1) Y (2 ^ j + d) ∈ T ∧
      wht (j + 1 + 1) Y (2 ^ (j + 1) + d) ∈ T ∧ wht (j + 1 + 1) Y (2 ^ (j + 1) + (2 ^ j + d)) ∈ T := by
  obtain ⟨e0, e1, e2, e3⟩ := wht_two j Y hd
  rw [wht_lo j Y hd] at hA
  rw [wht_hi j _ d] at hB
  rw [e0, e1, e2, e3]
  exact group_top_alg h hA hB (2 ^ j ≤ 2 * d) hL hR

/-! ## The block recursion -/

/-- Lines used by `E` on a block of size `2^(j+1)`: `E(2) = 1`, `E(2m) = 2 E(m) + 3 m / 2`. -/
def ecount : ℕ → ℕ
  | 0 => 1
  | j + 1 => 2 * ecount j + 3 * 2 ^ j

theorem four_ecount (j : ℕ) : 4 * ecount j = 2 ^ (j + 1) * (3 * j + 2) := by
  induction j with
  | zero => rfl
  | succ j ih =>
    have : 4 * ecount (j + 1) = 2 * (4 * ecount j) + 12 * 2 ^ j := by
      simp only [ecount]; ring
    rw [this, ih]
    ring

/-- The half of the pieces of the block `Y` of size `2^(j+1)` that `E(Y, σ)` makes: the pieces
`σ 2^j + a`, `a < 2^j` (that is, `(L, a) ± (R, a)`). -/
def Half (j : ℕ) (σ : Bool) (Y : ℕ → Form R n) : Set (Form R n) :=
  {F | ∃ a < 2 ^ j, F = wht (j + 1) Y (bif σ then 2 ^ j + a else a)}

/-- The quarter values of the block `Y` of size `2^(j+1)` that its parent needs: for every `d < 2^j`, the
piece `(Y_L, d)` when `τ = 0`, and `(Y_R, d)` when `τ = 1`, where `τ = [2^j ≤ 2d]`. -/
def Kept (j : ℕ) (Y : ℕ → Form R n) (T : Set (Form R n)) : Prop :=
  ∀ d < 2 ^ j, (if 2 ^ j ≤ 2 * d then wht j (shift Y (2 ^ j)) d else wht j Y d) ∈ T

theorem Kept.mono {j : ℕ} {Y : ℕ → Form R n} {T T' : Set (Form R n)} (h : Kept j Y T) (hT : T ⊆ T') :
    Kept j Y T' :=
  fun d hd => hT (h d hd)

theorem kept_zero (Y : ℕ → Form R n) (T : Set (Form R n)) (h : Y 0 ∈ T) : Kept 0 Y T := by
  intro d hd
  obtain rfl : d = 0 := by simpa using hd
  simpa [wht] using h

theorem kept_succ (j : ℕ) (Y : ℕ → Form R n) (T : Set (Form R n)) (hL : Half j false Y ⊆ T)
    (hR : Half j true (shift Y (2 ^ (j + 1))) ⊆ T) : Kept (j + 1) Y T := by
  intro d hd
  by_cases h : 2 ^ (j + 1) ≤ 2 * d
  · rw [ite_eq_left h]
    obtain ⟨a, rfl⟩ : ∃ a, d = 2 ^ j + a := ⟨d - 2 ^ j, by rw [pow_succ] at h; omega⟩
    exact hR ⟨a, by rw [pow_succ] at hd; omega, rfl⟩
  · rw [ite_eq_right h]
    exact hL ⟨d, by rw [pow_succ] at h; omega, rfl⟩

/-- `E(Y, σ)` on the block `Y` of size `2^(j+1)`, whose inputs are available: `ecount j` more lines make
the half `Half j σ Y` of its pieces and the quarter values `Kept j Y`. -/
theorem E_spec (j : ℕ) : ∀ (σ : Bool) (Y : ℕ → Form R n) (m : ℕ) (S : Set (Form R n)), Avail m S →
    (∀ t < 2 ^ (j + 1), Y t ∈ S) →
    ∃ T, Avail (m + ecount j) T ∧ S ⊆ T ∧ Half j σ Y ⊆ T ∧ Kept j Y T := by
  induction j with
  | zero =>
    intro σ Y m S h hY
    have h0 : Y 0 ∈ S := hY 0 (by norm_num)
    have h1 : Y 1 ∈ S := hY 1 (by norm_num)
    have hl := h.line h0 h1 1 (bif σ then -1 else 1) (Or.inl rfl)
      (F := wht 1 Y (bif σ then 2 ^ 0 + 0 else 0)) (by cases σ <;> simp [wht, shift, sub_eq_add_neg])
    refine ⟨_, hl.cast (by simp [ecount]), Set.subset_insert _ _, ?_, kept_zero Y _ (Set.mem_insert_of_mem _ h0)⟩
    rintro F ⟨a, ha, rfl⟩
    obtain rfl : a = 0 := by simpa using ha
    exact Set.mem_insert _ _
  | succ j ih =>
    intro σ Y m S h hY
    have hpow : 2 ^ (j + 1 + 1) = 2 ^ (j + 1) + 2 ^ (j + 1) := by ring
    obtain ⟨T1, h1, hS1, hH1, hK1⟩ := ih false Y m S h (fun t ht => hY t (by omega))
    obtain ⟨T2, h2, hS2, hH2, hK2⟩ := ih true (shift Y (2 ^ (j + 1))) _ T1 h1
      (fun t ht => hS1 (hY _ (by omega)))
    obtain ⟨T3, h3, hS3, hout⟩ := h2.iter 3 (2 ^ j)
      (fun d => {wht (j + 1 + 1) Y (bif σ then 2 ^ (j + 1) + d else d),
        wht (j + 1 + 1) Y (bif σ then 2 ^ (j + 1) + (2 ^ j + d) else 2 ^ j + d)})
      (fun d hd m' T hT hT2 => by
        obtain ⟨T', hT', hTT', w0, w1⟩ := group_mid j Y hd σ hT
          (hT2 (hS2 (hH1 ⟨d, hd, rfl⟩))) (hT2 (hH2 ⟨d, hd, rfl⟩))
          (hT2 (hS2 (hK1 d hd))) (hT2 (hK2 d hd))
        exact ⟨T', hT', hTT', Set.insert_subset_iff.2 ⟨w0, Set.singleton_subset_iff.2 w1⟩⟩)
    refine ⟨T3, h3.cast (by simp only [ecount]; ring), hS1.trans (hS2.trans hS3), ?_,
      kept_succ j Y T3 (hH1.trans (hS2.trans hS3)) (hH2.trans hS3)⟩
    rintro F ⟨a, ha, rfl⟩
    by_cases hlt : a < 2 ^ j
    · exact hout a hlt (Set.mem_insert _ _)
    · obtain ⟨d, rfl⟩ : ∃ d, a = 2 ^ j + d := ⟨a - 2 ^ j, by omega⟩
      have hd : d < 2 ^ j := by rw [pow_succ] at ha; omega
      exact hout d hd (Set.mem_insert_of_mem _ rfl)

/-- The top: the whole transform of the block `X` of size `2^(j+2)`, whose inputs are available, with
`2 ecount j + 5 2^j` more lines. -/
theorem top_spec (j : ℕ) (X : ℕ → Form R n) {m : ℕ} {S : Set (Form R n)} (h : Avail m S)
    (hX : ∀ t < 2 ^ (j + 1 + 1), X t ∈ S) :
    ∃ T, Avail (m + (2 * ecount j + 5 * 2 ^ j)) T ∧ ∀ a < 2 ^ (j + 1 + 1), wht (j + 1 + 1) X a ∈ T := by
  have hpow : 2 ^ (j + 1 + 1) = 2 ^ (j + 1) + 2 ^ (j + 1) := by ring
  obtain ⟨T1, h1, hS1, hH1, hK1⟩ := E_spec j false X m S h (fun t ht => hX t (by omega))
  obtain ⟨T2, h2, hS2, hH2, hK2⟩ := E_spec j true (shift X (2 ^ (j + 1))) _ T1 h1
    (fun t ht => hS1 (hX _ (by omega)))
  obtain ⟨T3, h3, hS3, hout⟩ := h2.iter 5 (2 ^ j)
    (fun d => {wht (j + 1 + 1) X d, wht (j + 1 + 1) X (2 ^ j + d), wht (j + 1 + 1) X (2 ^ (j + 1) + d),
      wht (j + 1 + 1) X (2 ^ (j + 1) + (2 ^ j + d))})
    (fun d hd m' T hT hT2 => by
      obtain ⟨T', hT', hTT', w0, w1, w2, w3⟩ := group_top j X hd hT
        (hT2 (hS2 (hH1 ⟨d, hd, rfl⟩))) (hT2 (hH2 ⟨d, hd, rfl⟩))
        (hT2 (hS2 (hK1 d hd))) (hT2 (hK2 d hd))
      refine ⟨T', hT', hTT', ?_⟩
      simp only [Set.insert_subset_iff, Set.singleton_subset_iff]
      exact ⟨w0, w1, w2, w3⟩)
  refine ⟨T3, h3.cast (by ring), fun a ha => ?_⟩
  have hj1 : 2 ^ (j + 1) = 2 ^ j + 2 ^ j := by ring
  by_cases h0 : a < 2 ^ j
  · exact hout a h0 (by simp)
  by_cases h1 : a < 2 ^ (j + 1)
  · obtain ⟨d, rfl⟩ : ∃ d, a = 2 ^ j + d := ⟨a - 2 ^ j, by omega⟩
    exact hout d (by omega) (by simp)
  by_cases h2 : a < 2 ^ (j + 1) + 2 ^ j
  · obtain ⟨d, rfl⟩ : ∃ d, a = 2 ^ (j + 1) + d := ⟨a - 2 ^ (j + 1), by omega⟩
    exact hout d (by omega) (by simp)
  · obtain ⟨d, rfl⟩ : ∃ d, a = 2 ^ (j + 1) + (2 ^ j + d) := ⟨a - 2 ^ (j + 1) - 2 ^ j, by omega⟩
    exact hout d (by omega) (by simp)

/-! ## The family on `2^(j+2)` points -/

/-- The family's circuit on `2^(j+2)` points computes the transform with `(3(j+2)+1) 2^j` lines, the
bound of the statement times 4 being an equality. -/
theorem family (R : Type*) [CommRing R] (j : ℕ) :
    ∃ C : Circuit R (2 ^ (j + 1 + 1)), C.Computes (hadamard R (j + 1 + 1)) ∧
      4 * C.size = 3 * (j + 1 + 1) * 2 ^ (j + 1 + 1) + 2 ^ (j + 1 + 1) := by
  obtain ⟨T, hT, hall⟩ := top_spec j (inputs R (j + 1 + 1)) (avail_inputs (R := R))
    (fun t ht => ⟨⟨t, ht⟩, by funext x; simp [inputs, ht]⟩)
  obtain ⟨C, hC, hsize⟩ := hT.circuit (hadamard R (j + 1 + 1)) (fun i => by
    have hi := hall i i.isLt
    rwa [wht_inputs] at hi)
  refine ⟨C, hC, ?_⟩
  rw [hsize]
  have h4 := four_ecount j
  have p1 : 2 ^ (j + 1) = 2 * 2 ^ j := by ring
  have p2 : 2 ^ (j + 1 + 1) = 4 * 2 ^ j := by ring
  rw [p1] at h4
  rw [p2]
  nlinarith

end MultiplyAdd
