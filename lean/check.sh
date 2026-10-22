#!/bin/sh
# Builds the Lean project in this folder and compares each statement with its proof.
# Needs: git, curl and elan (the Lean installer).  Run:  sh lean/check.sh
# VERIFY.md, in the folder above, says what to expect, how long it takes and how much memory it needs.
set -e
cd "$(dirname "$0")"
# 1. Fetch Mathlib at the pinned revision, already compiled.
lake exe cache get
# 2. Compile the 58 modules of this folder.  The axioms of the main theorems are printed on the way.
LEAN_NUM_THREADS="${LEAN_NUM_THREADS:-4}" lake build
# 3. Compare the two statements of Work/SmallWHT/ChallengeWHT8.lean with the two theorems that are proved.
lake env lean --run tools/Compare.lean Work.SmallWHT.ChallengeWHT8 Work.SmallWHT.TensorPow8Real \
    OAI.ExactFourier.WHT8Half.hadamard_pow8_circuit OAI.ExactFourier.WHT8Half.hadamard_pow8_circuit_real
# 4. Compare the statement of Work/WHT34/ChallengeWHT34.lean with the theorem that is proved.
lake env lean --run tools/Compare.lean Work.WHT34.ChallengeWHT34 Work.WHT34.SolutionWHT34 \
    MultiplyAdd.hadamard_mulAdd_circuit
