# Measurements of 22 October 2026: does the circuit make a program faster?

**In short.** I timed whole Walsh-Hadamard transforms on four x86 server processors, rented by the hour, with the
circuits of this repository (above all the 20-operation 8-point step of the 3/4 family) as the step a program runs
on the numbers it holds in registers. Everything else was FFHT's own structure (FFHT is the fast Walsh-Hadamard
library of Andoni, Indyk, Laarhoven, Razenshteyn and Schmidt). The rival was the best textbook code I could write in
the same program, FFHT itself included. The figure is the circuit's time divided by the rival's: below 1 means the
circuit took less time.

| processor | double precision, 2^10 to 2^16 points | single precision, 2^10 to 2^20 | reading |
|---|---|---|---|
| AMD Zen 5 (EPYC 9B45) | 0.977-0.996 | 0.974-0.994 | 0-2 % less time: too small for one run to establish |
| AMD Zen 4 (EPYC 9B14) | 0.940-0.952 | 0.934-1.038 | 5-6 % less time in double; mixed in single |
| AMD Zen 2 (EPYC 7B12) | 0.928-1.001 (gcc) | 0.986-1.100 (gcc, to 2^16) | no clear gain |
| Intel Xeon, Broadwell | 1.065-1.134 (gcc) | 1.151-1.265 (gcc, to 2^16) | the circuit is slower |

The Zen 5 and Zen 4 figures take the best of the gcc and clang builds on each side (section 1). The Zen 2 and Intel
figures are g20 in the gcc build, from an earlier version of the program whose rival was handicapped in the circuit's
favour (section 2).

Before the runs I set a rule: at 0.90 of the rival's time or below (10 % less), the work would go on; at 0.95 or
above, it would count as no gain worth pursuing on that chip. Across builds, Zen 5 came out above 0.95 and Zen 4
between the two. On Zen 2 the double-precision figures were noisy and fell between the two; on the Intel chip the
circuit was slower.

At the sizes most libraries use, 64 to 512 points, there was no gain on Zen 4 (a run on Zen 5 finished after this
page was written and is not in this revision). On an NVIDIA GPU
and on a Xilinx Artix-7 chip there was no gain either. **My first figure that day was wrong:** I wrote that on Zen 5
the circuit took 11-15 % less time. The rival it beat carried register copies it did not need. With the rival
written fairly, the gain on that chip is 0-2 %.

Every program was checked exact before it was timed. Each figure comes from one rented machine per chip, one core
and one run. `tables.py` in this folder re-derives every figure on this page from the raw files. I directed this
work. AI agents (Anthropic's Claude) wrote the timing programs, ran them on machines I rented through Google Colab,
reviewed the results and wrote this page. No person has read the programs line by line.

---

## 1. How the test works

**The structure is FFHT's.** FFHT transforms 2^n numbers in passes. Each pass loads 8 vectors (of 8 single or 4
double precision numbers), does three levels of the transform on them in registers, and stores them. The order of
passes, the block sizes and the in-lane levels are FFHT's own, and a program (`check_plan.py`) compares the timed
program's sequence of passes with FFHT's generated code, pass by pass: "PLAN MATCH" for float and for double. Only
the step on the 8 vectors in registers changes:

| name | the 8-vector step |
|---|---|
| tb8 | the textbook: 24 additions and subtractions, FFHT's own step |
| tb8bal | the textbook with 12 of its additions written as multiply-adds by 1 (the "balanced" textbook). AMD's Zen cores add on two pipes and multiply-add on two others, so this lets all four work. Written with each multiply-add first |
| tb8balS | the same 24 operations, each pair written subtraction first. This is the fair rival (section 3) |
| g20 | the 20-operation step of the 3/4 family of this repository (`tools/circuits/programs/generated/G_family_8.txt`) |
| g19 | the 19-operation step (`tools/circuits/programs/h8_19gates.txt`) |
| g52 | the 52-operation 16-point step of the 3/4 family, as a 16-vector step |
| h20half | the 20-operation step whose output is halved; its output is not H x, so it is left out of every figure here |

FFHT itself, built with the same compiler and flags, and an earlier whole transform of mine (`x86wht-tb`) are rivals
too. **The ratio** is a program's median time over the median time of the fastest rival. **Across builds** means the
fastest circuit of the gcc and the clang build against the fastest rival of both builds, at the sizes both builds
ran; this is the figure I quote first. **Per build** means inside one binary, where every program takes turns in
one process.

**The timing.** Every program runs in turns with the others in one process, at least 9 repeats of at least 0.2 s
each, the starting program rotating every round, on one core pinned for the whole run. Before each timing a check
refuses to time while another process uses more than 5 % of a core. The compilers were gcc 13.3.0 and clang 18.1.3
with `-O3 -mavx2 -mfma` (256-bit code), on Ubuntu 24.04.

**Same array and separate arrays.** In the *same-array* mode one buffer is transformed again and again. Since
H H = n I, the numbers grow and overflow to infinity after a few hundred calls, so most of the timed calls run on
infinities and NaNs: at least 90.5 % of the calls of every timing at 2^10 to 2^16, more than 99.9 % at the smallest
sizes, and at least 31 % at the largest. Every program meets the same data. Whether such values change the speed
was not measured directly; the timings on finite data (separate arrays, and many vectors per call, section 5) give
figures of the same size. In the *separate-array* mode each call meets a different array, from a ring of 64 MiB, so
the data comes from memory and stays finite. Each figure below says which mode it comes from.

**Exactness first.** Before anything is timed, every program in every binary, FFHT included, must give the exact
transform of random whole numbers at every size from 2^1 to 2^20, and a deliberately broken copy of the circuit (two
outputs swapped) must fail. In every run of this program and of its 512-bit and many-vector forms, every binary
passed and the broken copy was caught (one run of a kernel-level program stopped at its own check: section 11).

## 2. Results by chip

**AMD Zen 5** (EPYC 9B45, 48 virtual cores). Double precision, same array, across builds: **0.977-0.996**. Per build:
gcc 0.939-0.957, clang 0.977-0.996. In double precision, g20 alone: gcc 0.939-0.957, clang 0.977-0.996. The two
compilers disagree because clang's textbook is faster than gcc's; the across-builds figure is the one to quote.
Single precision, 2^10 to 2^20, same array, across builds: 0.974-0.994. Separate arrays (gcc, single precision, at
2^12, 2^16 and 2^20):
0.944-0.958. The run was not read by a reviewing agent after it finished; its program was reviewed before it ran.

**AMD Zen 4** (EPYC 9B14, 44 virtual cores). Double precision, same array, across builds: **0.940-0.952**. Per
build: gcc 0.940-0.952, clang 0.937-0.957; g20 alone: gcc 0.944-0.968, clang 0.938-0.957. Single precision, 2^10 to
2^20, across builds: 0.934-1.038 (mixed). Separate arrays (gcc, single precision): 0.965-0.969. Not read by a
reviewing agent after it finished.

Double precision by size (fastest exact circuit / fastest rival; same array):

| chip | points | gcc build | clang build | across builds |
|---|---|---|---|---|
| Zen 5 | 2^10 | 0.946 | 0.996 | 0.996 |
| Zen 5 | 2^12 | 0.957 | 0.990 | 0.990 |
| Zen 5 | 2^14 | 0.944 | 0.980 | 0.980 |
| Zen 5 | 2^16 | 0.939 | 0.977 | 0.977 |
| Zen 4 | 2^10 | 0.952 | 0.957 | 0.952 |
| Zen 4 | 2^12 | 0.945 | 0.937 | 0.945 |
| Zen 4 | 2^14 | 0.940 | 0.947 | 0.940 |
| Zen 4 | 2^16 | 0.944 | 0.942 | 0.944 |

**AMD Zen 2** (EPYC 7B12, 8 virtual cores) and **Intel Xeon at 2.20 GHz, family 6 model 79 (Broadwell)** (8 virtual
cores). These two ran the earlier version of the program, whose fastest rival was the balanced textbook written
multiply-add first. That rival is handicapped (section 3), so these runs can only flatter the circuit. g20 against
the fastest rival, same array, 2^10 to 2^16:

| chip | double, gcc | single, gcc | single, clang | reading |
|---|---|---|---|---|
| Zen 2 | 0.928-1.001 | 0.986-1.100 | 0.994-1.047 | no clear gain (the double figures are noisy) |
| Broadwell | 1.065-1.134 | 1.151-1.265 | 1.023-1.062 | the circuit is slower |

Both runs were read by a reviewing agent after they finished.

## 3. The figure I retracted

My first figure that day was that on Zen 5, FFHT's structure with g20 took **0.847-0.889** of the time of
the fastest rival (double precision, gcc, 2^10 to 2^16, three runs on the same machine): 11-15 % less time. That
was wrong, and here is how.

The fastest rival in those runs was the balanced textbook, tb8bal, written with each multiply-add before the
subtraction of the same pair. An x86 multiply-add overwrites one of its inputs. When it comes first, both inputs are
still needed by the subtraction, so the compiler copies one of them to another register first. A reviewing agent
compiled the program on an Apple M4 for x86-64 and read the machine code: the balanced textbook's inner loop had 55
instructions
against the circuit's 35, and 12 of the 55 were register copies the circuit did not need. Written subtraction first
(tb8balS), the same 24 operations round the same way and need no copies under clang. The inner loops in
instructions: tb8bal 55, tb8balS 43, g20 35 instructions (clang 21, double precision). In the binaries timed on
Zen 5 afterwards, the register copies in one 8-point step (double precision, 256-bit) were:

| compiler | tb8bal (multiply-add first) | tb8balS (subtraction first) | g20 |
|---|---|---|---|
| clang 18.1.3 | 12 | 0 | 0 |
| gcc 13.3.0 | 8 | 4 | 3 |

With tb8balS added as a rival, on the same machine, the figure fell to the 0-2 % of section 2 (across builds;
4-6 % against gcc's own build, whose tb8balS still carries one more copy than g20). On Zen 4 the copies cost almost
nothing: there the subtraction-first rival took 0.99-1.00 of the time of the multiply-add-first one, against
0.89-0.93 on Zen 5. That is why the Zen 4 figure did not move. The three earlier runs are kept in
`x86/runs/zen5-hybrid-retracted-*`, their code is `x86/harness-hybrid/` with `pre-twin.diff` undone, and the evidence
is in `x86/retraction/`. The Zen 2 and Intel runs of section 2 used the same earlier code.

## 4. 512-bit code (AVX-512)

These are single runs, not read by a reviewing agent after they finished. A repeat on Zen 4 finished after this
page was written; it is not in this revision. FFHT has no 512-bit code, so this program first tuned a 512-bit
textbook transform in FFHT's way (the form of
the in-lane levels and the recursion thresholds, chosen on the textbook alone) and then put the circuits into it.
Across builds, at the sizes both compilers ran (2^8-2^20, even sizes), against the fastest 512-bit rival:

| chip | single precision | double precision |
|---|---|---|
| Zen 5 | 0.940-1.018 | 0.946-1.007 |
| Zen 4 | 0.886-1.002 | 0.913-1.037 |

The gcc build alone, at the odd sizes, looks better (down to 0.796 on Zen 5 and 0.801 on Zen 4 in single precision;
0.896 and 0.938 in double), but only against gcc's own, weaker textbook.

## 5. The sizes libraries use (64 to 512 points)

Libraries for vector search and for quantising language models transform many short vectors at a time. On Zen 4 I
timed batches of vectors of 64 to 4,096 points, each batch sized to fit in the L2 cache, with the data kept finite
(610 of 610 timings ended on finite data), in 8 builds (gcc and clang; single and double; 256- and 512-bit). The
fastest exact circuit over all 8 builds against the fastest rival over all 8 builds:

- at 64 to 512 points: **0.972-1.107, no gain** (1.107 is at 64 points in single precision, against a 512-bit
  textbook layout that has no circuit version; without it 0.972-1.013);
- at 1,024 points: 0.979 in double and 0.983 in single precision;
- at 4,096 points: 0.981 in double and 0.967 in single precision.

One run, not read by a reviewing agent after it finished. A run of the same test on Zen 5 finished after this page
was written; it is not in this revision.

## 6. By-products, with no new mathematics

These two findings need nothing from this repository's mathematics. I report them because a reader who uses FFHT
may care.

**A faster textbook step inside FFHT.** On Zen 5, FFHT's own structure with the balanced textbook step written
subtraction first took 0.796-0.837 of FFHT's time (double precision, 2^10 to 2^16, across builds). Per build,
against FFHT built the same way: gcc 0.844-0.904, clang 0.795-0.830. On Zen 4: 0.904-0.932 across builds (gcc
0.903-0.931, clang 0.927-0.943).

**512-bit code.** On Zen 5 the tuned 512-bit textbook of section 4 took 0.40-0.50 of FFHT's time in double precision
and 0.37-0.46 in single precision, at 2^10 to 2^20 (across builds). In the main Zen 5 run, inside the same 512-bit
binary, FFHT took 1.68-1.80 times as long as the fastest 512-bit textbook (double, 2^10 to 2^16), and that 512-bit
textbook was 1.30-1.41 times as fast as the fastest 256-bit program of either build, circuits included. On Zen 4 the
tuned 512-bit textbook took 0.64-0.75 of FFHT's time in double and 0.56-0.72 in single precision.

## 7. One step in registers (the kernel level)

These figures time one pass of the step over data in the L1 cache, not a whole transform, against the faster of the
textbook and the balanced textbook (written multiply-add first):

- Zen 2, 256-bit, gcc: g52 against the 16-point textbook 0.780-0.785 (0.780 / 0.785 in single / double
  precision); g20 against the 8-point textbook 0.829-0.843 (0.829 / 0.843).
- Zen 5 and Zen 4, 512-bit, rows of 256 floats: g52 0.784-0.792 on the two chips (Zen 5 0.784-0.787, Zen 4
  0.789-0.792, two rounds each); a 22-operation step of depth 4 0.737 on Zen 5 and 0.947-0.949 on Zen 4.
- A latency-bound test on Zen 5 (the step applied again and again to the same values in registers, one chain at a
  time): g20 took 1.96 times as long as the textbook.

The step itself gains when the processor can overlap many independent steps, and loses when it cannot; inside a
whole transform the gain shrinks to the figures of section 2.

## 8. Rounding

On whole-number inputs every program is exact. On real inputs (numbers in [-1, 1)) the circuits round differently
from the textbook. From the exactness gates of the Zen 5 and Zen 4 runs, the largest error relative to the largest
output, at 2^10 and 2^20:

- double precision, against the textbook in double (which is FFHT's own result here: the textbooks and FFHT all show
  0.0e+00): the circuits differ by 2.2e-16 to 3.9e-16, g20 by 2.2e-16 to 3.7e-16;
- single precision, against a double-precision reference: the circuits 1.1e-07 to 1.7e-07, the textbooks
  7.9e-08 to 1.3e-07.

So the circuit is **not** bit-identical to FFHT on real data. The kernel folder of this repository measures the same
thing at every size from 2^5 to 2^20 (`tools/fht-kernel/`, `tests/test_rounding.c`).

## 9. GPU

On an NVIDIA RTX PRO 6000 Blackwell Server Edition (CUDA 13.0), the circuits as the per-thread step of a row kernel
tied the textbook on 256 MiB of data: 0.9999-1.0001, since the kernel waits on memory. Patched into Dao-AILab's
fast-hadamard-transform, the 19- and 52-operation steps gave 0.966-1.043 over 18 settings: no net change. HadaCore,
which uses the tensor cores, took 0.594-0.722 of Dao's time (0.996-0.997 at 512 points), so that is where the bar
for a GPU is. One figure looks like a gain and is not: at 4 MiB the circuit's call takes 4.1 µs against the
textbook's 5.0 µs (ratio 0.82), but in the other 4 MiB setting every program, the textbook too, took 4.1 µs, the
shortest call time of the test. That ratio measures this floor, not the circuit. One run, read by a reviewing agent.

### A separate test: the rotation of language models

This test is not about the circuits of this repository. Some language models are quantised with a Hadamard rotation
of a length such as 28 x 512 or 28 x 1,024; Dao's library does its 28-point part as dense signed sums. The idea of
computing that part with shared sums, and its count of additions, are from Sanjeet, Colbert et al.
(arXiv:2601.22347, Appendix A.1 and Table 4): sums over groups of four, 252 additions at 28 points. My part is a
circuit found by a randomized greedy search, with 235 additions, and one measurement (batch of 4,096 vectors,
half-precision formats):

| length | greedy circuit (mine) / Dao | groups of four (Sanjeet, Colbert et al.) / Dao |
|---|---|---|
| 28 x 1,024 (LLaMA-3.3-70B) | 0.952-0.967 | 0.955-0.963 |
| 28 x 512 (LLaMA-3.1-8B, Mistral-7B) | 1.169-1.178, a loss | 0.995-1.005 |

The published form does as well where mine gains and does not lose where mine does. Code and results:
`gpu/kpart/`.

## 10. Xilinx Artix-7

Placed and routed with open tools (openXC7) on an xc7a100t, 5 seeds each. The circuits use fewer carry blocks:
57 against 72 (-20.8 %) at 8 points and 156 against 192 (-18.8 %) at 16 points. But once placed they use more
slices: at 8 points 95 against 84 (+13.1 %) with 3 adder levels per clock and 109 against 84 (+29.8 %) with 2; at
16 points 289 against 220 (+31.4 %) with 2 levels and 226 against 228 (-0.9 %) with 4. Against Alman and Rao's
22-adder step at 2 levels: 109 against 119 (-8.4 %). A ternary-adder textbook placed in the same run (another
study's design, built by hand from three-input adders) used fewer carry blocks than the 19-adder circuit:
54 against 57. **Not a gain.** There is no vendor tool (Vivado) and no bitstream. The device was almost empty:
the largest design used 316 of the chip's 15,850 slices (2.0 %), so a fuller chip could place differently. One
run, read by a reviewing agent. Code and results: `fpga-xc7/`.

## 11. What went wrong

| what | effect | fixed? |
|---|---|---|
| The balanced rival was written multiply-add first and carried register copies | the retracted 11-15 % (section 3) | yes: the subtraction-first twin; under gcc it still carries one copy more than g20 |
| The first program looked up the step's function by name on every call | the circuit variants paid for extra string comparisons | in the main program, yes; the first program's runs keep it and are superseded |
| Same-array data overflows to infinity | most same-array calls run on infinities and NaNs, for every program alike | no; the separate-array and many-vector timings keep the data finite |
| The kernel-level program's generator broadcast the wrong constant in AVX-512 code | its Zen 4 run stopped at its exactness check before timing | yes |
| The 512-bit program's script waited forever (a bare `wait` in bash) | four launches produced nothing | yes |
| CUDA 13 removed a field the GPU program read | the first GPU launch built nothing; the FFT part failed in both launches | the GPU program yes, the FFT part no |
| Short GPU timings fall on a coarse grid of the timer, and the "past the L2 cache" sizes fit in this card's large L2 | small-batch GPU figures cannot resolve a few percent | no |
| openXC7 counts the pass-through LUTs it adds at carry inputs as LUTs | an early reading of a LUT saving, 461 against 586 (-21.3 %), only restated the carry-block count | the reading was corrected; this page quotes carry blocks and slices |
| The greedy K-part circuit needs more registers than a GPU thread has: in the compiler's report, 189 of 243 of its 28-point kernels keep values on the stack, against 1 of 243 of Dao's | a 17-18 % loss at 28 x 512, probably from that | no; the published form does not lose there |

## 12. What these measurements do not show

- **Faster on processors in general.** There is no gain on Zen 2, and on the Broadwell Xeon the circuit is slower.
  Modern Intel processors (Sapphire Rapids and later), Apple and Arm processors were not timed in this test.
- **Faster on AMD in general.** Each figure comes from one rented machine per chip, one pinned core and one run (the
  512-bit runs have no repeat in this revision). The processor's clock frequency was not controlled.
- **That the gain comes from fewer additions.** The 19-operation step was slower than the 20-operation step in
  13 of 16 double-precision timings on Zen 5 and Zen 4 (2 compilers, 4 sizes, 2 chips). Why is not known.
- **A gain at the sizes most libraries use**, 64 to 512 points: on Zen 4 there is none; a run on Zen 5 is not in
  this revision. The
  smallest size timed is 64 points (2^6); 32 points (2^5) was not timed.
- **The same results as FFHT bit for bit.** They are the same on whole numbers; on real inputs they differ by
  rounding (section 8).
- **The fastest code on these chips.** On Zen 5 a plain 512-bit textbook is faster than any 256-bit program,
  circuit or not (section 6).
- **FFHT as its authors build and time it.** FFHT was built with each binary's own flags and timed in my program,
  not with its own Makefile and its own timing program.
- **Several cores, throughput, or a whole application.** No library and no end-to-end workload was measured.
- **That `tools/fht-kernel/` is fast as a library.** It is cut from the timed program (a check shows the code is the
  same), but it has not been timed on its own.
- **A smaller design on every FPGA.** On the Artix-7 it is a loss (section 10).
- **Any power figure.** Power was not measured.
- **The K-part saving as mine.** The grouped sums are Sanjeet, Colbert et al.'s (section 9).

## 13. Not yet done

Two runs finished after this page was written and have not been read by a second agent, so they are not in this
revision: the library-size test of section 5 on Zen 5, and a repeat of the 512-bit run of section 4 on Zen 4. Not
done at all: a review, by a second agent, of the Zen 5 and Zen 4 runs of sections 2, 4 and 5 and of the full
x86-wht run on Zen 4; a same-array control with finite data; timing `tools/fht-kernel/` against FFHT; and a modern
Intel processor.

## 14. How to run it again

| what | command, from the folder | needs | time |
|---|---|---|---|
| the main test (sections 2, 3, 6, 8) | `bash run.sh` in `x86/harness-hybrid/` | x86-64 Linux with AVX2 and FMA; gcc, clang, git, python3; it fetches FFHT at commit `fba727a3` | 12-24 min |
| 512-bit (sections 4, 6) | `bash run.sh` in `x86/harness-hybrid512/` | AVX-512F and VL | about 28 min |
| library sizes (section 5) | `bash run.sh` in `x86/harness-small/` | AVX2 and FMA (AVX-512 used if present) | about 25 min |
| kernel level (section 7) | `bash run.sh` in `x86/harness-wht/` and in `x86/harness-balance/` | AVX2 and FMA; gcc | 30-45 min; 2-4 min |
| GPU (section 9) | `bash run.sh` in `gpu/harness-wht/`, `gpu/kpart/dao-cse/`, `gpu/kpart/three-forms/` | an NVIDIA GPU, CUDA 13, PyTorch | 25-50 min; about 10 and 15 min |
| Xilinx (section 10) | `bash run.sh xc7` in `fpga-xc7/` | Ubuntu 24.04 x86-64; it downloads the tools | about 35 min |
| the figures of this page | `python3 -B measurements/2026-10-22/tables.py` | Python 3 | under a second |
| the circuit files | `python3 -B measurements/2026-10-22/circuits/check_circuits.py` | Python 3 | under a second |

Each folder's README gives the details, the compilers and the flags. The READMEs of the four main x86 programs also
give a check of their source that runs without an x86 processor (through SIMDe, a library that emulates the x86
vector instructions), and the GPU program's README a check of its device code on an ordinary processor; those checks
pass on an Apple M4. The scripts install missing compilers with apt, which needs root; with the compilers installed
they need no root.

## 15. The code as run and as published

The code here is the code that ran, with private details taken out: paths on my computer, the names of the machines
that launched the jobs, and internal labels. Every changed line is listed, old against new, in
[CODE-AS-RUN.md](CODE-AS-RUN.md), with what was removed from the raw outputs (process lists, container names). Four
diffs give the code of the earlier runs: `x86/harness-hybrid/pre-twin.diff`,
`x86/harness-balance/gen-before-fix.diff`,
and `gpu/harness-wht/before-cuda13-fix.diff` with `before-mkdir-fix.diff`. Labels such as `ax-h0` or `ay-k1` left in
code comments name the AI agents that wrote or reviewed that part, and "wave 16" names the round of work of 21-22
October 2026.

## 16. Files

| path | what it is |
|---|---|
| `tables.py`, `expected-tables.txt` | re-derives every figure of this page from the raw files, and checks that this page quotes each one; what it printed |
| `circuits/` | the 12 circuit files the programs used, and `check_circuits.py`; 7 are byte-identical to files in `tools/circuits/programs/`, 5 are new |
| `x86/harness-*/` | the timing programs, each with its README |
| `x86/retraction/` | the machine-code evidence for section 3 |
| `x86/runs/` | the raw outputs of every x86 run (below) |
| `gpu/harness-wht/`, `gpu/runs/` | the GPU program and its two launches |
| `gpu/kpart/` | the separate language-model test: code, generator, results |
| `fpga-xc7/` | the Artix-7 run: designs, tools, results |
| `CODE-AS-RUN.md` | every line changed from the code as run |

Raw text files over 16 KB are stored compressed (`.gz`, made with Python's `gzip`, no time stamp), except the
summaries and machine records, which stay plain; each run's disassembly folder `asm/` is one `asm.tar.gz`.
`tables.py` reads both. The x86 run folders of the main programs have `machine.txt` (the machine), `tools.txt` (the
compilers), `run.log`, `quiet.log` (the quiet checks), `check_*.txt` (the exactness gates), `SUMMARY.md` and the
timing files; the other folders have the same kinds of file under the names their scripts gave them.

## Sources

**Machines.** All rented through Google Colab on 21-22 October 2026, Ubuntu 24.04, gcc 13.3.0, clang 18.1.3: AMD
EPYC 9B45 (Zen 5, family 26 model 2; also hosting the GPU, an NVIDIA RTX PRO 6000 Blackwell Server Edition, driver
580.82.07, CUDA 13.0, PyTorch 2.11); AMD EPYC 9B14 (Zen 4, family 25 model 17); AMD EPYC 7B12 (Zen 2, family 23 model
49); Intel Xeon at 2.20 GHz (family 6 model 79, Broadwell; a machine of the same model ran the Xilinx job). The
SIMDe checks ran on an
Apple M4 under macOS with Apple clang 21.0.0.

**Third-party code, fetched by the scripts, not included.** FFHT (FALCONN-LIB/FFHT, MIT) at
`fba727a3ff72c862260460631ae1cc8e3e44e861`; SIMDe (MIT) v0.8.2, `71fd833d9666141edcd1d3c109a80e228303d8d7`;
Dao-AILab/fast-hadamard-transform (BSD 3-Clause) at `e7706faf8d1c3b9f241e36860640ad1dac644ede`; HadaCore
(pytorch-labs/applied-ai, BSD 3-Clause), its latest commit on 22 October, `2391954b19988bd76cf3c2ea84c1ce74b68d568b`;
VkFFT (MIT) at `066a17c17068c0f11c9298d848c2976c71fad1c1` (its part of the GPU test failed to run); openXC7 release
2026-10-19 (nextpnr-xilinx `e7a6fb0e`, prjxray-db `6a6debcd`); YosysHQ oss-cad-suite release 2026-10-11 (Yosys
0.69+274). The size of the Artix-7 (15,850 slices) is from Xilinx's data sheet DS180, "7 Series FPGAs Data Sheet:
Overview". No file of FFHT is included; its recursion thresholds, in-lane sequences and order of passes are written
again in `x86/harness-hybrid/bench_hyb.c`, `x86/harness-small/bench_hyb.c` and `x86/harness-hybrid512/bench_h512.c`
and stay under FFHT's MIT licence (NOTICE, section 8; a copy of `LICENSE-FFHT` is in each of those folders).

**Papers.** FFHT: A. Andoni, P. Indyk, T. Laarhoven, I. Razenshteyn, L. Schmidt, "Practical and optimal LSH for
angular distance", NIPS 2015, arXiv:1509.02897. The grouped sums of section 9: Sanjeet, Colbert et al.,
arXiv:2601.22347, Appendix A.1 and Table 4. Alman and Rao's 8-point step: arXiv:2211.06459v2, Algorithm 5.

**Runs.** Folder under `x86/runs/` (or as named) and the job id it came from:

| folder | job id | chip |
|---|---|---|
| `zen5-hybrid` | x86-hybrid-1792681963-92221 | Zen 5 |
| `zen5-hybrid-retracted-1`, `-2`, `-3` | x86-hybrid-1792675051-74788, -1792676289-79401, -1792677531-82494 | Zen 5 |
| `zen4-hybrid` | x86-hybrid-1792683460-1797 | Zen 4 |
| `zen2-hybrid` | x86-hybrid-1792673518-71890 | Zen 2 |
| `intel-hybrid` | x86-hybrid-1792675656-75640 | Broadwell |
| `zen5-hybrid512`, `zen4-hybrid512` | x86-hybrid512-1792689261-12769, -12771 | Zen 5, Zen 4 |
| `zen4-small` | x86-hybrid-small-1792685022-5717 | Zen 4 |
| `zen5-wht`, `zen4-wht-quick`, `zen4-wht-full`, `zen2-wht`, `intel-wht` | x86-wht-1792671240-65893, -1792669473-57365, -1792672075-68529, -1792669250-55536, -1792673579-72098 | |
| `zen5-balance`, `zen4-balance-stopped`, `zen4-balance`, `zen2-balance`, `intel-balance` | x86-balance-1792670945-64604, -1792669445-56929, -1792671758-67457, -1792669043-54620, -1792673375-71565 | |
| `gpu/runs/rtx6000-wht`, `gpu/runs/rtx6000-wht-failed-build` | gpu-wht-1792669903-59258, -1792669718-58048 | GPU |
| `gpu/kpart/runs/dao-cse`, `gpu/kpart/runs/three-forms` | gpu-dao-1792669272-55598, gpu-hk3-1792670256-61566 | GPU |
| `fpga-xc7/results` | fpga-xc7-1792671207-65723 | Broadwell (tools) |

**Reviews.** "Read by a reviewing agent" means a second AI agent read the run's results after it finished, in a
review written the same day: the three retracted Zen 5 runs and the Zen 2 and Intel runs of the main program; the
first Zen 2 run of the first program; the GPU run; the Xilinx run. The program of the main Zen 5 run was reviewed
before it ran. The reviews themselves are working notes and are not in this repository.
