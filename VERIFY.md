# Checking the Lean proofs yourself

Two parts of the result of this repository are proved in Lean. Lean is a proof checker: a program that reads a
proof written out in full detail and accepts it only if every step is correct. This page gives the commands
that run the check on your own machine, says what you should see, and says what was run for this
repository. The runs reported here were made by AI agents (Anthropic's Claude), at my direction, on Linux
machines that I rented: one on 11 October 2026, and two through Google Colab on 22 October 2026, for
revision 2. The seven files that revision 2 adds were also compiled on a Mac of mine.

## What is proved in Lean

Three theorems, for two results. Each says that there is a circuit that computes the exact Walsh-Hadamard
transform of `N` numbers with few operations: the first two for every `N = 8^j`, the third for every `N = 2^k`.

| theorem | file | number of operations |
|---|---|---|
| `OAI.ExactFourier.WHT8Half.hadamard_pow8_circuit` | `lean/Work/SmallWHT/TensorPow8.lean` | at most `20 * j * 8^(j-1) + 8^j` |
| `OAI.ExactFourier.WHT8Half.hadamard_pow8_circuit_real` | `lean/Work/SmallWHT/TensorPow8Real.lean` | the same number, written `(5/6) N log2 N + N` |
| `MultiplyAdd.hadamard_mulAdd_circuit` | `lean/Work/WHT34/SolutionWHT34.lean` | at most `(3k·2^k + 2^k)/4` lines on `N = 2^k` points, that is `(3/4) N log2 N + N/4`, each line one multiply-add |

A circuit is a list of operations, each applied to inputs or to earlier results. In the first two
theorems an operation, which the Lean files call a gate, is one addition, one subtraction or one
multiplication by a constant, and each counts as one. This way of counting is the circuit model of
OpenAI's repository openai/math. The 44 files of theirs that the proof uses are in `lean/OAI/`, unchanged
(`NOTICE`, section 1).

The third theorem counts differently. Each line of its circuits is one multiply-add, ±u ± c·v with c a
constant, and costs one, as in Coppersmith, Feig and Linzer (1994). The definitions are OpenAI's text
with the gate replaced by this line and the complex numbers by any commutative ring. The statement
alone is `lean/Work/WHT34/ChallengeWHT34.lean`, 91 lines that use nothing but Mathlib. Its header says
what was changed. The file `lean/Work/WHT34/ChallengeWHT34Checks.lean` proves 12 checks on the same
definitions, among them that the 19 lines at 8 points compute the transform.

The file `lean/Work/SmallWHT/ChallengeWHT8.lean` holds the statement of the first two theorems alone, with no
proof: 93 lines that use nothing but Mathlib, the standard library of mathematics for Lean. To see exactly what
the three theorems claim, that file and `lean/Work/WHT34/ChallengeWHT34.lean` are the only files you have to
read. The 19 lines at 8 points, and the other checks, are stated in `lean/Work/WHT34/ChallengeWHT34Checks.lean`.
That file imports the statement file and uses its definitions as they are; the comparison script does not
compare its theorems.

Nothing else in this repository is proved in Lean. In particular, the count of the 3/4 family with every
operation charged (rate 7/8), the counts at sizes that are not powers of 8 in the first count, and the lower
bounds 2N - 1 and 0.3155 N log2 N are checked by programs or argued on paper, not by Lean. The timings and the hardware figures are
measurements, not proofs, and this page does not cover them. Each has its own page that says what was run
and how to run it again:
[tools/circuits/fast/wht56/results/ffht/README.md](tools/circuits/fast/wht56/results/ffht/README.md) for
the timings and [tools/circuits/fpga/README.md](tools/circuits/fpga/README.md) for the hardware.

## What you need

- Linux, with `git` and `curl`. The whole check was run on Linux only.
- `elan`, the program that installs Lean. The Lean documentation gives this command for it:
  `curl https://elan.lean-lang.org/elan-init.sh -sSf | sh`. The right version of Lean (v4.34.1, named in
  `lean/lean-toolchain`) is then fetched without further action.
- An internet connection and about 12 GB of free disk.
- Memory: the comparison commands held up to 15.3 GB in one process in the runs reported below, and the
  fourth command alone 15.2 GB. Those machines have 50 GB; a smaller one was not tried. (On this page 1 GB of
  memory or disk is 2^30 bytes.)

## The commands

    sh lean/check.sh

runs everything. It is these four commands, run in the folder `lean/`:

    lake exe cache get
    LEAN_NUM_THREADS=4 lake build
    lake env lean --run tools/Compare.lean Work.SmallWHT.ChallengeWHT8 Work.SmallWHT.TensorPow8Real \
        OAI.ExactFourier.WHT8Half.hadamard_pow8_circuit OAI.ExactFourier.WHT8Half.hadamard_pow8_circuit_real
    lake env lean --run tools/Compare.lean Work.WHT34.ChallengeWHT34 Work.WHT34.SolutionWHT34 \
        MultiplyAdd.hadamard_mulAdd_circuit

`lake` is Lean's build program. The first command downloads Mathlib already compiled, in the exact revision
that `lean/lake-manifest.json` names, so that your machine does not have to compile it. The second compiles
the 58 files of the folder; to compile a file is to check its proofs. The third and the fourth compare each
statement-only file with what was proved (see "What the comparison commands add").

## What you should see

1. `lake exe cache get` ends with a line that says 8908 files were decompressed. (On a machine that has
   fetched them before, it says 8907, with one already decompressed, as in the runs of 22 October.)
2. `lake build` ends with `Build completed successfully (8984 jobs).`, and no line starts with `error`.
   The warning "declaration uses `sorry`" appears three times, twice for `Work.SmallWHT.ChallengeWHT8` and
   once for `Work.WHT34.ChallengeWHT34`, and for no other file. `sorry` is Lean's word for a missing proof;
   those two files state the theorems without proving them, on purpose. Among the lines printed are

       'OAI.ExactFourier.WHT8Half.hadamard_pow8_circuit' depends on axioms: [propext, Classical.choice, Quot.sound]
       'OAI.ExactFourier.WHT8Half.hadamard_pow8_circuit_real' depends on axioms: [propext, Classical.choice, Quot.sound]
       'MultiplyAdd.hadamard_mulAdd_circuit' depends on axioms: [propext, Classical.choice, Quot.sound]

   An axiom is a statement that is accepted without proof. These three are the standard axioms of Lean, on
   which most of Mathlib rests. A proof with a gap would show `sorryAx` in the list.
3. The third command prints, for each of the two theorems, three lines that start with `OK`, and ends with
   `RESULT: PASS`. The fourth prints three lines that start with `OK` for `MultiplyAdd.hadamard_mulAdd_circuit`,
   and ends with `RESULT: PASS`.

## What the comparison commands add

The proof files are long, and a long file could prove a theorem with the right name about the wrong thing.
`tools/Compare.lean` guards against that. It loads the statement-only file and the proof files separately
and checks three things for each theorem: the theorem that is proved is exactly the statement of the short
file; every definition that the statement uses is the same in both; and the proof rests on no axiom other
than the three above. The agents wrote this script. It is not Lean's official tool for this comparison,
which is called `comparator`; `comparator` was not run on this folder. In the night of 10 to 11 October,
in the folder where the six files of `lean/Work/SmallWHT/` were written, `comparator` accepted the same two
statements (`Your solution is okay!`), with a stand-in for its sandbox and with a configuration file that is
not in this repository. `comparator` was not run on the files of the 3/4 count.

## What was run

### 11 October 2026

On 11 October 2026 the agents ran the three commands on the rented Linux machine: Ubuntu 24.04, 8 threads
of a processor that reports itself as an Intel Xeon at 2.2 GHz, 50 GB of memory. Everything was new: the folder, the install of `elan` and of
Lean v4.34.1, and the download of Mathlib. Other jobs of mine were running on the machine at the same time.

| step | result | time | memory |
|---|---|---|---|
| `lake exe cache get` | Lean installed; Mathlib, at the revision that `lean/lake-manifest.json` names, and its 8 dependencies fetched; 8908 compiled files downloaded; exit code 0 | 185 s | 1.0 GB |
| `LEAN_NUM_THREADS=4 lake build` | 51 files compiled, 44 of OpenAI's and 7 others; `Build completed successfully (8977 jobs).`; exit code 0 | 647 s | 6.8 GB in the largest process; 20.8 GB for the four that ran at once, added up |
| `tools/Compare.lean` | three `OK` lines for each theorem; `RESULT: PASS`; exit code 0 | 67 s | 15.3 GB |

From the install of `elan` to the last line it took 899 s, 15 minutes. The disk held 11.6 GB at the end: 8.1 GB
for Mathlib and the compiled files (`lean/.lake`), 3.0 GB for Lean, 0.4 GB for the downloads. The sum of
20.8 GB counts the Mathlib files that the four processes share once for each of them, so the build needs
less than that; how much less was not measured.

The build printed the warning about `sorry` twice, both times for the statement-only file. It printed six
lines about axioms, for the two theorems above and four others, and each line named the same three axioms.
The 56 files of `lean/` that were built have the same checksums (sha256) as the files of this repository.
Afterwards `sh lean/check.sh` was run once in the same folder, where everything was already built: exit
code 0, `RESULT: PASS`, 108 s.

Two controls. A check that could not fail would prove nothing, so the checks were also run on two wrong
copies, kept outside the folder.

1. In a copy of `H8Half.lean` one of the 20 operations was changed: number 13, from an addition to a
   subtraction. Lean rejected the copy: `error: unsolved goals` in the theorem `circuit_computes`, exit code
   1. The unchanged file, compiled in the same way, passed with exit code 0.
2. In a copy of the statement-only file, 19 was written in place of 20 in the first statement. The comparison
   answered `FAIL: statement (type) differs between challenge and solution` for that theorem, and ended with
   `RESULT: FAIL`, exit code 1.

The 44 files of `lean/OAI/` were also compared with a new checkout of openai/math at the commit that
`NOTICE` names: all 44 are identical, byte for byte.

### 22 October 2026, for revision 2

The agents ran the four commands one at a time, then `sh lean/check.sh` once more, on two Linux machines
rented through Google Colab, each with 8 threads and 50 GB of memory, at the same time. On each the folder
`lean/` was new, with the seven files of the 3/4 count in it. Lean v4.34.1 and Mathlib's compiled files were
already on both machines from earlier work of mine. So `lake exe cache get` fetched the source of Mathlib
and of its 8 dependencies at the pinned revisions, but downloaded none of the compiled files: it only
unpacked them. The times and the memory are given for the first machine, then the second.

| step | result | time | memory |
|---|---|---|---|
| `lake exe cache get` | Mathlib and its 8 dependencies fetched at the pinned revisions; 8907 compiled files unpacked from the machine's cache, one already unpacked, none downloaded; exit code 0 | 144 s; 139 s | 1.0 GB; 1.0 GB |
| `LEAN_NUM_THREADS=4 lake build` | 58 files compiled, 44 of OpenAI's and 14 others; `Build completed successfully (8984 jobs).`; exit code 0 | 574 s; 636 s | 6.8 GB; 6.7 GB, in the largest process |
| `tools/Compare.lean`, the 5/6 count | three `OK` lines for each theorem; `RESULT: PASS`; exit code 0 | 88 s; 140 s | 15.2 GB; 14.0 GB |
| `tools/Compare.lean`, the 3/4 count | three `OK` lines for `MultiplyAdd.hadamard_mulAdd_circuit`; `RESULT: PASS`; exit code 0 | 26 s; 61 s | 15.2 GB; 15.2 GB |

The four commands took 14 and 16 minutes. The build printed the warning about `sorry` three times, twice for
`ChallengeWHT8.lean` and once for `ChallengeWHT34.lean`, and no other warning. It printed 19 lines about axioms:
the six of 11 October, one for `MultiplyAdd.hadamard_mulAdd_circuit` and twelve for the checks in
`ChallengeWHT34Checks.lean`; each line named the same three axioms. The 60 `.lean` files of the folder
`lean/` (the 58 modules, `lakefile.lean` and `tools/Compare.lean`) have the same checksums (sha256) on both
machines as the files of this repository. Afterwards
`sh lean/check.sh` was run once more in each folder, where everything was already built: exit code 0,
`RESULT: PASS` for both comparisons, 90 s and 108 s, 15.3 GB.

Two controls for the new files, run on both machines:

1. In a copy of `FamilyWHT34.lean`, kept outside the folder, one constant of the construction was changed from
   2 to -2. Lean rejected the copy: `error: ring failed, ring expressions not equal`, exit code 1.
2. In a copy of `ChallengeWHT34.lean`, built as a separate module and removed afterwards, `+ 2 ^ k` (the N/4
   of the bound) was left out. The comparison answered `FAIL: statement (type) differs between challenge and
   solution` and ended with `RESULT: FAIL`, exit code 1.

The seven files of the 3/4 count were also compiled on a Mac (Apple M4, macOS 26.6.2), in this folder, against
a Mathlib build of the same revision already on that machine: `Build completed successfully (8930 jobs).` in
74 s, with the one `sorry` warning of `ChallengeWHT34.lean` and 13 lines about axioms, each naming the same
three. The rest of the folder was not built on the Mac.

## Limits

- One run from nothing, on one machine, on 11 October; on 22 October two more runs, in new folders on two
  machines where Lean and Mathlib's compiled files were already present. The whole folder was not built on a
  Mac; the seven files of the 3/4 count were compiled on one.
- No person has read the Lean files yet. They were written by AI agents (Anthropic's Claude) under my
  direction. What stands behind the theorems is Lean's check, the comparison script and the controls.
- Lean checks that the theorems follow from the definitions. It does not check that the definitions say what
  I mean by them. That is why the statement-only file is short: the definition of a circuit there is OpenAI's
  (lines 25 to 62), and the definition of the transform is two lines (the matrix `hadamard k`, lines 72 and
  73). In `lean/Work/WHT34/ChallengeWHT34.lean` the definitions are lines 41 to 79: OpenAI's text with the
  changes that its header lists, and the matrix `hadamard R k` in lines 78 and 79.
- The theorems say that the circuits exist and bound their size. Lean does not print the circuit for a given
  `N`. The 20 operations for 8 points are written out in `lean/Work/SmallWHT/H8Half.lean`, one per line.
  Lean writes out the 19 lines at 8 points and the 7 at 4 points, in `ChallengeWHT34Checks.lean`, and no list
  of lines for the family above 8 points.
- The first two theorems cover `N = 8^j` only: 8, 64, 512, 4,096 and so on; the third covers every `N = 2^k`.
- The third theorem allows any constant in a line. The circuits use only ±1 and ±2, but the statement does not
  say so.
- `lake exe cache get` downloads compiled Mathlib files from the Mathlib project's server. Mathlib was not
  compiled from its source.

## Revision 2: what else can be checked, and what was run

Revision 2 (22 October 2026) adds three programs that check something and one folder of measurements. None of them
is a Lean check, and none of the measurements is a proof. **Revision 2 adds seven Lean files, the proof of the 3/4
count, in `lean/Work/WHT34/`; the files of the 5/6 count are unchanged. The whole Lean check was run again for
revision 2 (see "What was run").** Each command below is run from the top folder of the repository, and each ends with the
line shown when everything is right.

| command | what it checks | last line | needs |
|---|---|---|---|
| `python3 -B tools/circuits/count_tables.py` | builds the circuits of five constructions at 8 to 4,096 points, counts them in both counts, checks each on random whole numbers against the transform and its count against a formula; prints the exact count tables of the README | `OK: every built circuit equals its formula.  A Python check, not a proof.` | Python 3; about 5 s and 160 MB (`--kmax-gen 15`, which builds 32,768 points too: about 50 s and 1.5 GB) |
| `python3 -B measurements/2026-10-22/circuits/check_circuits.py` | replays the 12 circuit files that the timing programs used on every unit vector in exact arithmetic, and checks that the harnesses' copies are the same files | `OK: 12 circuit files, each exact on every unit vector.` | Python 3; under a second |
| `python3 -B measurements/2026-10-22/tables.py` | re-derives every figure of the measurements page from the raw files, and checks that the page quotes each one | `OK: every figure of measurements/2026-10-22/README.md re-derived from the raw files.  Measurements, not proofs.` | Python 3; under a second |
| `sh tools/fht-kernel/test.sh` | builds the kernel and checks it: exact on whole numbers at every size 2^0 to 2^20 in float and double, FFHT's return codes, a deliberately broken copy caught, code written for FFHT linked under FFHT's names, and the code word for word the timed code | `OK: exact on integer inputs at every size 2^0 to 2^20 in float and double, FFHT's return codes, broken copy caught.` | a C compiler; Python 3 for the last check; with `SIMDE_DIR` set, it also checks the AVX2 code through SIMDe |

**What was run.** On 22 October 2026 the agents ran all four commands on an Apple M4 with macOS: `count_tables.py`
in both forms, `check_circuits.py`, `tables.py`, and `test.sh` twice, natively (the portable code, since that machine
has no AVX2) and with `SIMDE_DIR` (the AVX2 code, emulated by SIMDe v0.8.2). Each ended with its last line. The
recorded outputs are `tools/circuits/expected-output-count-tables.txt`,
`measurements/2026-10-22/expected-tables.txt` and `tools/fht-kernel/tests/expected-macos-arm64*.txt`.

**The measurements themselves** were run on machines rented through Google Colab (AMD EPYC 9B45, 9B14 and 7B12, an
Intel Xeon of family 6 model 79, and an NVIDIA RTX PRO 6000 Blackwell Server Edition), not on the Mac. Every timing
program checks its own exactness before it times anything, on the machine where it runs; those checks are in the raw
outputs (`check_*.txt`). The sources of the four main x86 timing programs were also built on the Mac through SIMDe
and passed their exactness gates there (their READMEs under `measurements/2026-10-22/x86/` give the output; the
short kernel-level program of `harness-balance/` has no such build), and the GPU program's device code passed its
CPU check (`gpu/harness-wht/wht_cuda_cpucheck.cpp`).
`measurements/2026-10-22/README.md` says what was measured, how, and what it does not show.
