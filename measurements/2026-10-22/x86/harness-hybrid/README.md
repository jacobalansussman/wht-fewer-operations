# harness-hybrid: FFHT's structure with the circuits as its in-register step

This is the main timing program of 22 October 2026. It times whole transforms of 2^10 to 2^20 points on one core of
an x86-64 processor. It keeps the structure of FFHT, the fast Walsh-Hadamard library of Andoni, Indyk, Laarhoven,
Razenshteyn and Schmidt, and changes only the step that runs on the 8 vectors held in registers. The results page is
[../../README.md](../../README.md); the raw outputs are in [../runs/](../runs/).

## What it does

`run.sh` does everything, in this order:

1. It prints the machine (`out/machine.txt`) and the compilers (`out/tools.txt`).
2. It fetches FFHT and checks out commit `fba727a3`.
3. It builds one binary per compiler and vector width, each linking FFHT compiled with the same flags:
   `gcc -O3 -mavx2 -mfma` and `clang -O3 -mavx2 -mfma`, float and double (`-DXT=0` and `-DXT=2`). On a processor
   with AVX-512 it also builds gcc binaries with `-mavx512f -mavx512vl` added.
4. It checks that the step sequence of the hybrid equals FFHT's own generated code, step for step
   (`check_plan.py`, "PLAN MATCH"; `out/plan_check_*.txt`).
5. It runs the exactness gate in every binary (`out/check_*.txt`). Every program, FFHT included, must give the exact
   transform of random whole numbers at every size from 2^1 to 2^20. A deliberately broken copy of the circuit must
   fail it. Nothing is timed if the gate fails.
6. It times the programs, all in one process, taking turns: at least 9 repeats of at least 0.2 s each, the starting
   program rotating every round, pinned to one core. Before each timing a quiet check (`az_quiet.py`) refuses to
   time while another process uses more than 5 % of a core.
7. It writes `out/SUMMARY.md` from the raw timing files (`summarize_hyb.py`) and counts the instructions of every
   timed step function (`asmcount_hyb.py`, `out/asm_counts.txt`; the functions' disassembly is kept in `out/asm/`).

The programs in each binary:

| name | what it is |
|---|---|
| `FFHT` | FFHT itself, its own code |
| `hyb8-tb8` | FFHT's structure, written with intrinsics, with the textbook 8-point step (FFHT's own 24 operations) |
| `hyb8-tb8bal` | the same with half the additions written as multiply-adds by 1, multiply-add first |
| `hyb8-tb8balS` | the same 24 lines, each pair written subtraction first (the fair rival: see the retraction) |
| `hyb16-tb16` | the same structure with a 16-vector textbook step |
| `x86wht-tb`, `x86wht-tbbal` | the earlier whole transform of [../harness-wht/](../harness-wht/) |
| `hyb8-g19`, `hyb8-g20` | the circuits with 19 and 20 operations as the 8-vector step |
| `hyb8-h20half` | the 20-operation step whose output is halved (left out of every exact-output figure) |
| `hyb16-g52` | the 52-operation 16-point step of the 3/4 family |

## Run it again

On an x86-64 machine with AVX2 and FMA, Ubuntu 24.04 (or gcc, clang, git and python3 installed), leave the machine
idle and run, from this folder:

    bash run.sh

It takes about 12 minutes on an 8-core machine without AVX-512 and about 24 minutes with it. It needs less than
1 GB of memory and writes into `out/`; binaries and the FFHT clone go to `/content/build/x86-hybrid` on Colab and to
`$TMPDIR/az-build/x86-hybrid` elsewhere (`BUILD=...` overrides). `MODE=full` times every binary at every size
(about 48 minutes). `CORE=n` picks the core (default: the last one).

The runs of 22 October used gcc 13.3.0 and clang 18.1.3 on Ubuntu 24.04, on rented Google Colab machines: AMD EPYC
9B45 (Zen 5), AMD EPYC 9B14 (Zen 4), AMD EPYC 7B12 (Zen 2) and an Intel Xeon at 2.20 GHz, family 6 model 79
(Broadwell).

## Check the source without an x86 machine

`build_simde_check.sh` compiles `bench_hyb.c` with SIMDe, a library that emulates the x86 vector instructions, and
runs the exactness gate and the plan check. It times nothing. It needs clang, a SIMDe checkout and an FFHT checkout:

    SIMDE=/path/to/simde FFHT=/path/to/FFHT bash build_simde_check.sh

Output on an Apple M4, macOS, Apple clang 21.0.0, SIMDe v0.8.2, 22 October 2026:

    avx2_f32: ALL PASS
    avx2_f64: ALL PASS
    avx512_f32: ALL PASS
    avx512_f64: ALL PASS
    ARITH: every FFHT step does m*log2(m) cross-vector add/sub (+6 per vector in its in-lane step): YES
    PLAN MATCH (float, 2^3..2^20, 1470 steps compared)
    ARITH: every FFHT step does m*log2(m) cross-vector add/sub (+4 per vector in its in-lane step): YES
    PLAN MATCH (double, 2^2..2^20, 7898 steps compared)

## Files

| file | what it is |
|---|---|
| `run.sh` | the whole job |
| `bench_hyb.c` | the timing program: FFHT's plan written with intrinsics, the step chosen per program |
| `bench_k0.c`, `bench.h` | the earlier program it includes (types, kernels, the x86wht transform) and the timing protocol |
| `kernels_k0.h` | the steps, generated from `circuits/` by `gen_x86.py`: `python3 -B gen_x86.py $(cat ../retraction/gen_x86_args.txt) > kernels_k0.h` gives this file byte for byte |
| `gen_x86.py`, `gen_kernels.py` | the generator: one instruction per circuit line |
| `check_plan.py` | compares the hybrid's step sequence with FFHT's `fht_avx.c` |
| `summarize_hyb.py`, `asmcount_hyb.py` | the summary and the instruction counts |
| `az_pre.sh`, `az_quiet.py` | the shared preamble (machine record, build folder) and the quiet check |
| `build_simde_check.sh` | the correctness build for machines without x86 |
| `circuits/` | the circuit files, byte-identical to [../../circuits/](../../circuits/) |
| `pre-twin.diff` | the code of the five earlier runs (before the fair rival was added), as a difference from this code |
| `LICENSE-FFHT` | FFHT's MIT licence, for the parts of FFHT in `bench_hyb.c`: its recursion thresholds, in-lane sequences and order of passes ([NOTICE](../../../../NOTICE), section 8) |

Comments in the code name the AI agents that wrote or reviewed each part by labels such as `ax-1` or `ay-k0`, and
say "tonight" for the night of 21 to 22 October 2026. The code differs from the code as run only in the lines listed
in [../../CODE-AS-RUN.md](../../CODE-AS-RUN.md).
