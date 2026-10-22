# Checking the Lean proof yourself

One part of the result of this repository is proved in Lean. Lean is a proof checker: a program that reads a
proof written out in full detail and accepts it only if every step is correct. This page gives the commands
that run the check on your own machine, says what you should see, and says what was run for this
repository. The runs reported here were made by AI agents (Anthropic's Claude), at my direction, on a Linux
machine that I rented.

## What is proved in Lean

Two theorems. Each says that for every `j` there is a circuit that computes the exact Walsh-Hadamard
transform of `N = 8^j` numbers with few operations.

| theorem | file | number of operations |
|---|---|---|
| `OAI.ExactFourier.WHT8Half.hadamard_pow8_circuit` | `lean/Work/SmallWHT/TensorPow8.lean` | at most `20 * j * 8^(j-1) + 8^j` |
| `OAI.ExactFourier.WHT8Half.hadamard_pow8_circuit_real` | `lean/Work/SmallWHT/TensorPow8Real.lean` | the same number, written `(5/6) N log2 N + N` |

A circuit is a list of operations, each applied to inputs or to earlier results. An operation, which the
Lean files call a gate, is one addition, one subtraction or one multiplication by a constant, and each
counts as one. This way of counting is the circuit model of OpenAI's repository openai/math. The 44 files of
theirs that the proof uses are in `lean/OAI/`, unchanged (`NOTICE`, section 1).

The file `lean/Work/SmallWHT/ChallengeWHT8.lean` holds the statement alone, with no proof: 93 lines that use
nothing but Mathlib, the standard library of mathematics for Lean. To see exactly what is claimed, that is
the only file you have to read.

Nothing else in this repository is proved in Lean. In particular, the counts in which a multiplication by a
constant is free are checked by the Python programs, not by Lean. The timings and the hardware figures are
measurements, not proofs, and this page does not cover them. Each has its own page that says what was run
and how to run it again:
[tools/circuits/fast/wht56/results/ffht/README.md](tools/circuits/fast/wht56/results/ffht/README.md) for
the timings and [tools/circuits/fpga/README.md](tools/circuits/fpga/README.md) for the hardware.

## What you need

- Linux, with `git` and `curl`. The check was run on Linux only.
- `elan`, the program that installs Lean. The Lean documentation gives this command for it:
  `curl https://elan.lean-lang.org/elan-init.sh -sSf | sh`. The right version of Lean (v4.34.1, named in
  `lean/lean-toolchain`) is then fetched without further action.
- An internet connection and about 12 GB of free disk.
- Memory: the last command held 15.3 GB in one process in the run reported below. That machine has 50 GB; a
  smaller one was not tried. (On this page 1 GB of memory or disk is 2^30 bytes.)

## The commands

    sh lean/check.sh

runs everything. It is these three commands, run in the folder `lean/`:

    lake exe cache get
    LEAN_NUM_THREADS=4 lake build
    lake env lean --run tools/Compare.lean Work.SmallWHT.ChallengeWHT8 Work.SmallWHT.TensorPow8Real \
        OAI.ExactFourier.WHT8Half.hadamard_pow8_circuit OAI.ExactFourier.WHT8Half.hadamard_pow8_circuit_real

`lake` is Lean's build program. The first command downloads Mathlib already compiled, in the exact revision
that `lean/lake-manifest.json` names, so that your machine does not have to compile it. The second compiles
the 51 files of the folder; to compile a file is to check its proofs. The third compares the statement-only
file with what was proved (see "What the third command adds").

## What you should see

1. `lake exe cache get` ends with a line that says 8908 files were decompressed.
2. `lake build` ends with `Build completed successfully (8977 jobs).`, and no line starts with `error`.
   The warning "declaration uses `sorry`" appears twice, for `Work.SmallWHT.ChallengeWHT8` and for no other
   file. `sorry` is Lean's word for a missing proof; that file states the two theorems without proving
   them, on purpose. Among the lines printed are

       'OAI.ExactFourier.WHT8Half.hadamard_pow8_circuit' depends on axioms: [propext, Classical.choice, Quot.sound]
       'OAI.ExactFourier.WHT8Half.hadamard_pow8_circuit_real' depends on axioms: [propext, Classical.choice, Quot.sound]

   An axiom is a statement that is accepted without proof. These three are the standard axioms of Lean, on
   which most of Mathlib rests. A proof with a gap would show `sorryAx` in the list.
3. The third command prints, for each of the two theorems, three lines that start with `OK`, and ends with
   `RESULT: PASS`.

## What the third command adds

The proof files are long, and a long file could prove a theorem with the right name about the wrong thing.
`tools/Compare.lean` guards against that. It loads the statement-only file and the proof files separately
and checks three things for each theorem: the theorem that is proved is exactly the statement of the short
file; every definition that the statement uses is the same in both; and the proof rests on no axiom other
than the three above. The agents wrote this script. It is not Lean's official tool for this comparison,
which is called `comparator`; `comparator` was not run on this folder. In the night of 10 to 11 October,
in the folder where the six files of `lean/Work/SmallWHT/` were written, `comparator` accepted the same two
statements (`Your solution is okay!`), with a stand-in for its sandbox and with a configuration file that is
not in this repository.

## What was run

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

## Limits

- One machine and one run from nothing. The folder was not built on a Mac.
- No person has read the Lean files yet. They were written by AI agents (Anthropic's Claude) under my
  direction. What stands behind the two theorems is Lean's check, the comparison script and the two controls.
- Lean checks that the theorems follow from the definitions. It does not check that the definitions say what
  I mean by them. That is why the statement-only file is short: the definition of a circuit there is OpenAI's
  (lines 25 to 62), and the definition of the transform is two lines (the matrix `hadamard k`, lines 72 and
  73).
- The theorems say that the circuits exist and bound their size. Lean does not print the circuit for a given
  `N`. The 20 operations for 8 points are written out in `lean/Work/SmallWHT/H8Half.lean`, one per line.
- The theorems cover `N = 8^j` only: 8, 64, 512, 4,096 and so on.
- `lake exe cache get` downloads compiled Mathlib files from the Mathlib project's server. Mathlib was not
  compiled from its source.

## Revision 2: what else can be checked, and what was run

Revision 2 (22 October 2026) adds three programs that check something and one folder of measurements. None of them
is a Lean check, and none of the measurements is a proof. **The Lean files are unchanged in revision 2, and the Lean
check was not run again.** Each command below is run from the top folder of the repository, and each ends with the
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
