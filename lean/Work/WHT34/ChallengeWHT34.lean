import Mathlib

/-!
# Statement only: the Walsh-Hadamard transform on `N = 2^k` points in at most `(3/4) N log2 N + N/4` multiply-adds

Not part of github.com/openai/math.

This file contains NO proof: the theorem ends in `sorry`, on purpose.  It is the statement alone, written so
that a reader can check what is claimed without reading anything else.  It imports only Mathlib.

The circuit model is OpenAI's: the declarations from `Gate` to `Circuit.Computes` below are lines 25 to 62 of
`Work/SmallWHT/ChallengeWHT8.lean` (the same declarations as in OpenAI's
`OAI/Computability/FourierCircuit/Core.lean`), with two changes of meaning:
* the numbers are any commutative ring `R`, in place of the complex numbers;
* a line is one multiply-add, `v i + c * v j` or `c * v j - v i` with `c` a constant of `R`, in place of
  one addition, one subtraction or one multiplication by a constant.  With `c` free, the two forms are
  `±u ± c·v` with all four choices of sign: one operation `±a ± b·c` of Coppersmith, Feig and Linzer
  (1994, page 969), with one factor of the product a constant.  A plain addition or subtraction (`c = ±1`)
  and a plain multiplication `c·v` (through the 0 wire) are lines too, and each costs one, as in that paper.
The only other edits to the text are mechanical: `Gate`, `Program` and `Circuit` take `R` as an argument;
`Gate.eval`, `Program.eval`, `Circuit.eval` and `Circuit.Computes` take `[CommRing R]`; `ℂ` becomes `R`;
`Program` lands in `Type _` in place of `Type`; the first line of `Circuit.Computes` is split in two; and
`zeta` and `fourierMatrix`, which are not used here, are left out.  So, as in OpenAI's model: wires
`0 .. n-1` are the inputs, wire `n` is the constant 0, line `t` makes wire `n + 1 + t` from earlier wires,
the outputs name wires, and `size` is the number of lines.

After these declarations come one definition, the matrix `hadamard R k` (the formula of `hadamard k` in
`Work/SmallWHT/ChallengeWHT8.lean`, with `(-1 : R)` in place of `(-1 : ℂ)`), and the statement.

What the theorem does NOT say:
* that `(3/4) N log2 N + N/4` lines is the least possible: it is an upper bound, and no lower bound is
  claimed;
* anything about the strict count of the 5/6 theorem, where a multiplication by a constant is a gate of
  its own;
* which constants the circuit uses: any `c : R` is allowed (the construction needs only 1, -1, 2, -2);
* anything about depth, speed or rounding.
-/

namespace MultiplyAdd

/-- One line, cost one: `v i + c * v j`, or `c * v j - v i`, where `v i`, `v j` are available values and
`c` is a constant.  Each is one multiply-add `±a ± b·c` of Coppersmith, Feig and Linzer (1994). -/
inductive Gate (R : Type*) (w : ℕ) where
  | addMul (i : Fin w) (c : R) (j : Fin w)
  | mulSub (c : R) (j : Fin w) (i : Fin w)

def Gate.eval {R : Type*} [CommRing R] {w : ℕ} (v : Fin w → R) : Gate R w → R
  | .addMul i c j => v i + c * v j
  | .mulSub c j i => c * v j - v i

/-- A topologically ordered scalar DAG; available values are never consumed. -/
inductive Program (R : Type*) (n : ℕ) : ℕ → Type _ where
  | nil : Program R n 0
  | step {k : ℕ} (p : Program R n k) (g : Gate R (n + 1 + k)) : Program R n (k + 1)

def Program.eval {R : Type*} [CommRing R] {n : ℕ} : {k : ℕ} → Program R n k → (Fin n → R) →
    (Fin (n + 1 + k) → R)
  | 0, .nil, x => Fin.snoc x 0
  | _ + 1, .step p g, x =>
      let v := p.eval x
      Fin.snoc v (g.eval v)

/-- Outputs name available values, so permutations and arbitrary fanout are uncharged. -/
structure Circuit (R : Type*) (n : ℕ) where
  size : ℕ
  program : Program R n size
  outputs : Fin n → Fin (n + 1 + size)

def Circuit.eval {R : Type*} [CommRing R] {n : ℕ} (C : Circuit R n) (x : Fin n → R) : Fin n → R :=
  fun i => C.program.eval x (C.outputs i)

def Circuit.Computes {R : Type*} [CommRing R] {n : ℕ} (C : Circuit R n)
    (A : Matrix (Fin n) (Fin n) R) : Prop :=
  ∀ x, C.eval x = A.mulVec x

/-- The Walsh-Hadamard matrix on `2^k` points in natural (Sylvester) order, over `R`: the entry in row `j`
and column `l` is `(-1)^(number of common 1-bits of j and l)`. -/
def hadamard (R : Type*) [CommRing R] (k : ℕ) : Matrix (Fin (2 ^ k)) (Fin (2 ^ k)) R :=
  fun j l => ∏ i ∈ Finset.range k, if j.val.testBit i && l.val.testBit i then (-1 : R) else 1

/-- For every commutative ring `R` and every `k`, the exact (unscaled) Walsh-Hadamard transform on
`N = 2^k` points has a multiply-add circuit with at most `(3/4) N log2 N + N/4` lines.  Since `log2 N = k`,
the bound is written times 4, without division: `4 * size ≤ 3 k 2^k + 2^k`.  For `k ≥ 2` the bound is a
whole number, and a circuit with fewer lines can be padded with unused ones, so the theorem also gives a
circuit with exactly that many lines; for `k = 0` and `k = 1` it allows 0 and 2 lines (the identity and the
butterfly). -/
theorem hadamard_mulAdd_circuit (R : Type*) [CommRing R] (k : ℕ) :
    ∃ C : Circuit R (2 ^ k), C.Computes (hadamard R k) ∧ 4 * C.size ≤ 3 * k * 2 ^ k + 2 ^ k := by
  sorry

end MultiplyAdd
