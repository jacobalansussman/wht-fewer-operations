import Lake
open System Lake DSL

-- Lake project for the circuit result of this repository: the Walsh-Hadamard transform with fewer
-- operations.  `lake build` builds everything in this folder.
-- Package name, toolchain (lean-toolchain), package option and Mathlib revision are those of the
-- lakefile of github.com/openai/math (lean/lakefile.lean at commit fd4aeeb); every other
-- dependency of that lakefile is dropped because the files used here import only Mathlib.
package OAI where
  version := v!"0.1.0"
  fixedToolchain := true
  leanOptions := #[⟨`autoImplicit, false⟩]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "d13f23b723b8a846827a245b89c10fc7d3f11612"

-- Files of github.com/openai/math (lean/OAI/Computability/FourierCircuit/), unmodified;
-- only the 44 files that the theorems of this repository depend on.
@[default_target]
lean_lib OAI.Computability where
  roots := #[`OAI.Computability]
  globs := #[`OAI.Computability.+]

-- The transform written as a sum (`wht`), one small file; not from openai/math.
@[default_target]
lean_lib WHTCheck where globs := #[`WHTCheck.+]

-- The 20-gate circuit and the proofs (`Work.SmallWHT.*`), with the statement-only module
-- `Work.SmallWHT.ChallengeWHT8`; not from openai/math.
@[default_target]
lean_lib Work where globs := #[`Work.+]
