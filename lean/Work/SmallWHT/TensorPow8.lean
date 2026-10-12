import OAI.Computability.FourierCircuit.TensorCostAlgebra
import Work.SmallWHT.HadamardDigits

/-!
# The Walsh-Hadamard transform on `N = 8^j` points in at most `(5/6) N log2 N + N` gates

Everything is in OpenAI's circuit model (`OAI.ExactFourier`): every addition, every subtraction and every
multiplication by a constant costs one gate.  The transform is the exact one (every output has factor 1).

Input: the 20-gate circuit for one half of the 8-point transform (`H8Half.lean`).
Output: `hadamard_pow8_circuit`, a circuit for `hadamard (3 * j)` with at most `20 * (j * 8^(j-1)) + 8^j`
gates.  With `N = 8^j` and `log2 N = 3 j` that number is `(5/6) N log2 N + N`.

This file needs 43 files of openai/math that the earlier results of this repository do not use: the files
that `OAI/Computability/FourierCircuit/TensorCostAlgebra.lean` imports, directly or not.  They are in this
repository unmodified, beside `Core.lean`.  Names used from them:

* `LinearDAG n a` (Shears.lean): a program with `n` inputs and `a` outputs; `Circuit n` is the case `a = n`.
* `TypedDAG ι κ` (CircuitExtensions.lean): the same with inputs and outputs indexed by finite types.
* `CircuitCost.cost M` (CircuitCost.lean): the least number of gates of a circuit that computes `M`.
  `cost_le`: any circuit computing `M` bounds it.  `optimal`: some circuit attains it.
  `cost_tensor`: `cost (M ⊗ₖ N) ≤ card β * cost M + card α * cost N`.
  `cost_reindex`: renaming the coordinates by a bijection does not change the cost.
* `TensorAxis.Space α k`, `TensorAxis.power A k` (StreamSeries.lean): the `k`-fold Kronecker power of `A`,
  with `power A 0 = 1` and `power A (k+1) = power A k ⊗ₖ A`.  `card_space : card (Space α k) = card α ^ k`.
* `TensorAxis.funCoordinates`, `power_fun_reindex`, `Amplification.cost_group`,
  `Amplification.cost_reindexed_power` (TensorCostAlgebra.lean): bookkeeping for the coordinates of powers.
* `TypedDAG.scalar c C` (CircuitExtensions.lean): `C` followed by one multiplication by `c` on every output.
* `Cascade.power_smul` (CascadeWord.lean): `power (c • A) k = c^k • power A k`.
-/

namespace OAI
namespace ExactFourier
namespace WHT8Half

open scoped Kronecker
open CircuitCost TensorAxis Amplification

variable {α : Type} [Fintype α] [DecidableEq α]

/-! ## 1. Between `Circuit n` and `cost` -/

/-- A circuit of the model bounds the cost of its matrix.  (The converse of `exists_circuit` below.) -/
theorem cost_le_of_circuit {n : ℕ} (M : Matrix (Fin n) (Fin n) ℂ) (C : Circuit n)
    (hC : C.Computes M) : cost M ≤ C.size := by
  let e := Fintype.equivFin (Fin n)
  let D : LinearDAG n n := ⟨C.size, C.program, C.outputs⟩
  let T : TypedDAG (Fin n) (Fin n) :=
    ⟨(D.withInputs (fun i => e i)).withOutputs (fun j => e.symm j)⟩
  have hsize : T.size = C.size := LinearDAG.size_withInputs D (fun i => e i)
  have heval : Realizes T M := by
    intro x
    funext j
    have h1 : T.eval x j = D.eval x j := by
      change ((D.withInputs (fun i => e i)).withOutputs (fun j => e.symm j)).eval
        (x ∘ e.symm) (e j) = _
      rw [LinearDAG.eval_withOutputs, LinearDAG.eval_withInputs]
      simp [Function.comp_def]
    rw [h1]
    exact congrFun (hC x) j
  exact (cost_le M T heval).trans hsize.le

/-- A circuit of the model that attains the cost.  This is `CircuitCost.exists_circuit` of openai/math
(`lean/OAI/Computability/FourierCircuit/Main.lean`, lines 196 to 210, Apache License 2.0), repeated here with
its proof, unchanged except for its name and for spacing, so that `Main.lean` and the six further files it
needs are not imported.  The statement and the proof below are OpenAI's; see `NOTICE`, section 2. -/
theorem exists_circuit_of_cost {n : ℕ} (M : Matrix (Fin n) (Fin n) ℂ) :
    ∃ C : Circuit n, C.size = cost M ∧ C.Computes M := by
  obtain ⟨T, hT, ht⟩ := optimal M
  let e := Fintype.equivFin (Fin n)
  let D : LinearDAG n n := (T.circuit.withInputs e.symm).withOutputs e
  let C : Circuit n := ⟨D.size, D.program, D.outputs⟩
  refine ⟨C, ?_, ?_⟩
  · change D.size = cost M
    change (T.circuit.withInputs e.symm).size = cost M
    rw [LinearDAG.size_withInputs]
    exact hT
  · intro x
    change D.eval x = M.mulVec x
    rw [LinearDAG.eval_withOutputs, LinearDAG.eval_withInputs]
    exact ht x

/-! ## 2. Kronecker powers: `j` factors on `q` points cost at most `j * q^(j-1)` times one factor -/

theorem cost_power_succ_le (A : Matrix α α ℂ) (j : ℕ) :
    cost (power A (j + 1)) ≤ (j + 1) * Fintype.card α ^ j * cost A := by
  induction j with
  | zero =>
    have h : cost (power A (0 + 1)) ≤
        Fintype.card α * cost (power A 0) + Fintype.card (Space α 0) * cost A :=
      cost_tensor (power A 0) A
    have h0 : cost (power A 0) = 0 := by simp [power]
    rw [h0] at h
    simpa [card_space] using h
  | succ j ih =>
    have h : cost (power A (j + 1 + 1)) ≤
        Fintype.card α * cost (power A (j + 1)) + Fintype.card (Space α (j + 1)) * cost A :=
      cost_tensor (power A (j + 1)) A
    rw [card_space] at h
    calc cost (power A (j + 1 + 1))
        ≤ Fintype.card α * cost (power A (j + 1)) + Fintype.card α ^ (j + 1) * cost A := h
      _ ≤ Fintype.card α * ((j + 1) * Fintype.card α ^ j * cost A) +
            Fintype.card α ^ (j + 1) * cost A :=
          Nat.add_le_add_right (Nat.mul_le_mul_left _ ih) _
      _ = (j + 1 + 1) * Fintype.card α ^ (j + 1) * cost A := by ring

theorem cost_power_le (A : Matrix α α ℂ) (j : ℕ) :
    cost (power A j) ≤ j * Fintype.card α ^ (j - 1) * cost A := by
  rcases j with _ | j
  · simp [power]
  · simpa using cost_power_succ_le A j

/-! ## 3. Scalars -/

omit [DecidableEq α] in
/-- One multiplication by a constant on every output: at most one more gate per output. -/
theorem cost_smul_le (c : ℂ) (M : Matrix α α ℂ) : cost (c • M) ≤ cost M + Fintype.card α := by
  obtain ⟨C, hC, hc⟩ := optimal M
  have h := cost_le (c • M) (TypedDAG.scalar c C) (TypedDAG.eval_scalar c C M hc)
  simpa [hC] using h

/-! ## 4. The count for the Kronecker powers of the 8-point matrix `H` -/

/-- One half of the 8-point matrix costs at most 20: the circuit of `H8Half.lean`. -/
theorem cost_half_H : cost ((1 / 2 : ℂ) • H) ≤ 20 :=
  (cost_le_of_circuit _ circuit circuit_computes).trans_eq circuit_size

/-- The scaled power: `(H / 2)^{⊗ j}` costs at most `20 * j * 8^(j-1)`. -/
theorem cost_power_half_H (j : ℕ) : cost (power ((1 / 2 : ℂ) • H) j) ≤ j * 8 ^ (j - 1) * 20 := by
  have h := cost_power_le ((1 / 2 : ℂ) • H) j
  simp only [Fintype.card_fin] at h
  exact h.trans (Nat.mul_le_mul_left _ cost_half_H)

/-- The exact power: `H^{⊗ j}` costs at most `20 * j * 8^(j-1) + 8^j`. -/
theorem cost_power_H (j : ℕ) : cost (power H j) ≤ 20 * (j * 8 ^ (j - 1)) + 8 ^ j := by
  have h2 : power H j = (2 : ℂ) ^ j • power ((1 / 2 : ℂ) • H) j := by
    rw [Cascade.power_smul, smul_smul, ← mul_pow]
    norm_num
  have h3 := cost_smul_le ((2 : ℂ) ^ j) (power ((1 / 2 : ℂ) • H) j)
  rw [← h2, card_space, Fintype.card_fin] at h3
  calc cost (power H j) ≤ cost (power ((1 / 2 : ℂ) • H) j) + 8 ^ j := h3
    _ ≤ j * 8 ^ (j - 1) * 20 + 8 ^ j := Nat.add_le_add_right (cost_power_half_H j) _
    _ = 20 * (j * 8 ^ (j - 1)) + 8 ^ j := by ring

/-! ## 5. From the powers of `H` to `hadamard (3 * j)` -/

/-- `hadamard k` is the `k`-fold Kronecker power of `H2` with its coordinates renamed: an address of `k`
bits is read as its `k` binary digits. -/
theorem hadamard_eq_reindex (k : ℕ) :
    hadamard k = Matrix.reindex ((funCoordinates (α := Fin 2) k).trans finFunctionFinEquiv)
      ((funCoordinates (α := Fin 2) k).trans finFunctionFinEquiv) (power H2 k) := by
  rw [← reindex_comp, power_fun_reindex]
  ext j l
  exact hadamard_eq_digits k j l

/-- In the vocabulary of openai/math: the cost of `hadamard k` is the cost of the Kronecker power. -/
theorem cost_hadamard (k : ℕ) : cost (hadamard k) = cost (power H2 k) := by
  rw [hadamard_eq_reindex, cost_reindex]

theorem cost_power_H_eq (j : ℕ) : cost (power H j) = cost (power H2 (3 * j)) := by
  have hH : H = (Matrix.reindex ((funCoordinates (α := Fin 2) 3).trans finFunctionFinEquiv)
      ((funCoordinates (α := Fin 2) 3).trans finFunctionFinEquiv) (power H2 3) :
      Matrix (Fin 8) (Fin 8) ℂ) := hadamard_eq_reindex 3
  rw [hH, cost_reindexed_power, ← cost_group]

/-- **Cost of the Walsh-Hadamard matrix on `8^j` points**, as a Kronecker power of `[[1, 1], [1, -1]]`. -/
theorem cost_power_H2 (j : ℕ) : cost (power H2 (3 * j)) ≤ 20 * (j * 8 ^ (j - 1)) + 8 ^ j := by
  rw [← cost_power_H_eq]
  exact cost_power_H j

/-- The same for the matrix `hadamard (3 * j)`, in natural order. -/
theorem cost_hadamard_pow8 (j : ℕ) : cost (hadamard (3 * j)) ≤ 20 * (j * 8 ^ (j - 1)) + 8 ^ j := by
  rw [cost_hadamard]
  exact cost_power_H2 j

/-- **Main statement.**  For every `j` there is a circuit of OpenAI's model, on `N = 2^(3 j)` points, that
computes the exact Walsh-Hadamard transform `hadamard (3 * j)` with at most `20 * (j * 8^(j-1)) + 8^j`
gates.  For `j ≥ 1` this number equals `(5/6) N log2 N + N`. -/
theorem hadamard_pow8_circuit (j : ℕ) :
    ∃ C : Circuit (2 ^ (3 * j)),
      C.Computes (hadamard (3 * j)) ∧ C.size ≤ 20 * (j * 8 ^ (j - 1)) + 8 ^ j := by
  obtain ⟨C, hC, hc⟩ := exists_circuit_of_cost (hadamard (3 * j))
  exact ⟨C, hc, hC.le.trans (cost_hadamard_pow8 j)⟩

/-- The size at 512 points: 4352 gates, against `512 * 9 = 4608` for the textbook circuit. -/
theorem hadamard_512_circuit :
    ∃ C : Circuit (2 ^ 9), C.Computes (hadamard 9) ∧ C.size ≤ 4352 := by
  obtain ⟨C, hc, hs⟩ := hadamard_pow8_circuit 3
  exact ⟨C, hc, hs.trans (by norm_num)⟩

end WHT8Half
end ExactFourier
end OAI

#print axioms OAI.ExactFourier.WHT8Half.hadamard_pow8_circuit
#print axioms OAI.ExactFourier.WHT8Half.hadamard_512_circuit
