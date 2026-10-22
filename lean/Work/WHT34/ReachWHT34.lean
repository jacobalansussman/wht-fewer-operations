import Work.WHT34.ModelWHT34

/-!
# Which functions of the input a program makes available

`Avail m S` says: some program of the model with exactly `m` lines has every function in `S` on one of its
wires.  Every lemma below adds lines to the end of a program, so the proof of the construction never
computes a wire number.  Only `Avail.line` (one more line) and `Avail.circuit` (choose the outputs) touch
`Program`.
-/

namespace MultiplyAdd

/-- A function of the input vector: the values a circuit computes are such functions. -/
abbrev Form (R : Type*) (n : ℕ) := (Fin n → R) → R

variable {R : Type*} [CommRing R] {n : ℕ}

/-- Some program with `m` lines has every function of `S` on one of its wires. -/
def Avail (m : ℕ) (S : Set (Form R n)) : Prop :=
  ∃ p : Program R n m, ∀ f ∈ S, ∃ w : Fin (n + 1 + m), ∀ x, p.eval x w = f x

theorem Avail.mono {m : ℕ} {S T : Set (Form R n)} (h : Avail m S) (hT : T ⊆ S) : Avail m T := by
  obtain ⟨p, hp⟩ := h
  exact ⟨p, fun f hf => hp f (hT hf)⟩

theorem Avail.cast {m m' : ℕ} {S : Set (Form R n)} (h : Avail m S) (e : m = m') : Avail m' S :=
  e ▸ h

/-- The empty program has every input on a wire. -/
theorem avail_inputs : Avail (R := R) (n := n) 0 (Set.range fun (i : Fin n) (x : Fin n → R) => x i) := by
  refine ⟨.nil, ?_⟩
  rintro f ⟨i, rfl⟩
  refine ⟨⟨i.val, by omega⟩, fun x => ?_⟩
  rw [eval_nil_apply, dite_eq_left i.isLt]

/-- One more line `σ f + c g`, with `σ = ±1` and `f`, `g` available: `addMul` for `σ = 1`, `mulSub` for
`σ = -1`. -/
theorem Avail.line {m : ℕ} {S : Set (Form R n)} (h : Avail m S) {f g : Form R n} (hf : f ∈ S)
    (hg : g ∈ S) (σ c : R) (hσ : σ = 1 ∨ σ = -1) {F : Form R n} (hF : F = σ • f + c • g) :
    Avail (m + 1) (insert F S) := by
  obtain ⟨p, hp⟩ := h
  obtain ⟨i, hi⟩ := hp f hf
  obtain ⟨j, hj⟩ := hp g hg
  subst hF
  have old : ∀ (q : Program R n (m + 1)), (∀ x (w : Fin (n + 1 + m)),
      q.eval x ⟨w.val, by omega⟩ = p.eval x w) → ∀ G ∈ S, ∃ w : Fin (n + 1 + (m + 1)),
      ∀ x, q.eval x w = G x := by
    intro q hq G hG
    obtain ⟨w, hw⟩ := hp G hG
    exact ⟨⟨w.val, by omega⟩, fun x => (hq x w).trans (hw x)⟩
  rcases hσ with rfl | rfl
  · refine ⟨.step p (.addMul i c j), ?_⟩
    rintro G (rfl | hG)
    · refine ⟨⟨n + 1 + m, by omega⟩, fun x => ?_⟩
      rw [eval_step_apply, dite_eq_right (lt_irrefl _)]
      simp [Gate.eval, hi, hj]
    · exact old _ (fun x w => by rw [eval_step_apply, dite_eq_left w.isLt]) G hG
  · refine ⟨.step p (.mulSub c j i), ?_⟩
    rintro G (rfl | hG)
    · refine ⟨⟨n + 1 + m, by omega⟩, fun x => ?_⟩
      rw [eval_step_apply, dite_eq_right (lt_irrefl _)]
      simp [Gate.eval, hi, hj]
      ring
    · exact old _ (fun x w => by rw [eval_step_apply, dite_eq_left w.isLt]) G hG

/-- Choosing the outputs: if every row of `A x` is available, there is a circuit with that many lines. -/
theorem Avail.circuit {m : ℕ} {S : Set (Form R n)} (h : Avail m S) (A : Matrix (Fin n) (Fin n) R)
    (hA : ∀ i, (fun x => A.mulVec x i) ∈ S) : ∃ C : Circuit R n, C.Computes A ∧ C.size = m := by
  obtain ⟨p, hp⟩ := h
  choose w hw using fun i => hp _ (hA i)
  exact ⟨⟨m, p, w⟩, fun x => funext fun i => hw i x, rfl⟩

/-- `k` independent groups of `cost` lines each, whose operands lie in `S0`, one after the other. -/
theorem Avail.iter {S0 : Set (Form R n)} {m : ℕ} (h : Avail m S0) (cost k : ℕ)
    (Out : ℕ → Set (Form R n))
    (step : ∀ d < k, ∀ m' T, Avail m' T → S0 ⊆ T → ∃ T', Avail (m' + cost) T' ∧ T ⊆ T' ∧ Out d ⊆ T') :
    ∃ T, Avail (m + cost * k) T ∧ S0 ⊆ T ∧ ∀ d < k, Out d ⊆ T := by
  induction k with
  | zero => exact ⟨S0, h.cast (by simp), fun _ hx => hx, fun d hd => absurd hd (Nat.not_lt_zero _)⟩
  | succ k ih =>
    obtain ⟨T, hT, h0, hout⟩ := ih (fun d hd => step d (by omega))
    obtain ⟨T', hT', hTT', hout'⟩ := step k (by omega) _ T hT h0
    refine ⟨T', hT'.cast (by ring), h0.trans hTT', fun d hd => ?_⟩
    rcases Nat.lt_succ_iff_lt_or_eq.1 hd with hd | rfl
    · exact (hout d hd).trans hTT'
    · exact hout'

/-- Three lines: a hub `M = A + c B`, then `σ1 M + c1 q` and `σ2 M + c2 q'`. -/
theorem Avail.three {m : ℕ} {S : Set (Form R n)} (h : Avail m S) {A B q q' : Form R n} (hA : A ∈ S)
    (hB : B ∈ S) (hq : q ∈ S) (hq' : q' ∈ S) (c σ1 c1 σ2 c2 : R) (hσ1 : σ1 = 1 ∨ σ1 = -1)
    (hσ2 : σ2 = 1 ∨ σ2 = -1) {w0 w1 : Form R n} (h0 : w0 = σ1 • (A + c • B) + c1 • q)
    (h1 : w1 = σ2 • (A + c • B) + c2 • q') :
    ∃ T, Avail (m + 3) T ∧ S ⊆ T ∧ w0 ∈ T ∧ w1 ∈ T := by
  have g1 := h.line hA hB 1 c (Or.inl rfl) (F := A + c • B) (by rw [one_smul])
  have g2 := g1.line (Set.mem_insert _ _) (Set.mem_insert_of_mem _ hq) σ1 c1 hσ1 h0
  have g3 := g2.line (Set.mem_insert_of_mem _ (Set.mem_insert _ _))
    (Set.mem_insert_of_mem _ (Set.mem_insert_of_mem _ hq')) σ2 c2 hσ2 h1
  refine ⟨_, g3.cast (by omega), fun x hx => ?_, Set.mem_insert_of_mem _ (Set.mem_insert _ _),
    Set.mem_insert _ _⟩
  exact Set.mem_insert_of_mem _ (Set.mem_insert_of_mem _ (Set.mem_insert_of_mem _ hx))

/-- Five lines: a hub `M = A + B`, then `u0 = σ1 M + c1 q`, `u1 = σ2 M + c2 q'`, `u2 = -u0 + 2 A` and
`u3 = u1 + c3 B`. -/
theorem Avail.five {m : ℕ} {S : Set (Form R n)} (h : Avail m S) {A B q q' : Form R n} (hA : A ∈ S)
    (hB : B ∈ S) (hq : q ∈ S) (hq' : q' ∈ S) (σ1 c1 σ2 c2 c3 : R) (hσ1 : σ1 = 1 ∨ σ1 = -1)
    (hσ2 : σ2 = 1 ∨ σ2 = -1) {u0 u1 u2 u3 : Form R n} (h0 : u0 = σ1 • (A + (1 : R) • B) + c1 • q)
    (h1 : u1 = σ2 • (A + (1 : R) • B) + c2 • q') (h2 : u2 = (-1 : R) • u0 + (2 : R) • A)
    (h3 : u3 = (1 : R) • u1 + c3 • B) :
    ∃ T, Avail (m + 5) T ∧ S ⊆ T ∧ u0 ∈ T ∧ u1 ∈ T ∧ u2 ∈ T ∧ u3 ∈ T := by
  obtain ⟨T, hT, hST, h0T, h1T⟩ := h.three hA hB hq hq' 1 σ1 c1 σ2 c2 hσ1 hσ2 h0 h1
  have g4 := hT.line h0T (hST hA) (-1) 2 (Or.inr rfl) h2
  have g5 := g4.line (Set.mem_insert_of_mem _ h1T) (Set.mem_insert_of_mem _ (hST hB)) 1 c3
    (Or.inl rfl) h3
  refine ⟨_, g5.cast (by omega), fun x hx => Set.mem_insert_of_mem _ (Set.mem_insert_of_mem _ (hST hx)),
    Set.mem_insert_of_mem _ (Set.mem_insert_of_mem _ h0T),
    Set.mem_insert_of_mem _ (Set.mem_insert_of_mem _ h1T),
    Set.mem_insert_of_mem _ (Set.mem_insert _ _), Set.mem_insert _ _⟩

end MultiplyAdd
