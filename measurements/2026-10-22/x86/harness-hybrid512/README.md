# harness-hybrid512: the same comparison in 512-bit code (AVX-512)

FFHT has no 512-bit code. This program first builds the best 512-bit textbook transform it can in FFHT's way: it
tries several forms of the in-lane levels and tunes the recursion thresholds on the textbook alone (`tune_*.txt`).
Then it puts the circuits into that tuned structure as the 8- or 16-vector step, and times them against 512-bit
textbooks, the copy-free balanced textbook, x86-wht's 512-bit codes and FFHT (its 256-bit code). The results page is
[../../README.md](../../README.md), section "512-bit code".

Status: one run on AMD Zen 5 (EPYC 9B45) and two on AMD Zen 4 (EPYC 9B14), on 22 October 2026; the second Zen 4 run
repeats the first on the same machine (`../runs/zen4-hybrid512-repeat/`), and the two agree within 1.6 %. No run was
read by a second, reviewing agent after it finished.

## Run it again

On an x86-64 machine with AVX-512F and AVX-512VL (AMD Zen 4 or Zen 5, Intel Xeon since Skylake-SP), Ubuntu 24.04 or
gcc, clang, git and python3 installed, idle, from this folder:

    bash run.sh

About 28 minutes on the 44- and 48-core machines of 22 October; under 1 GB of memory. It stops without AVX-512.
Builds: `gcc -O3` and `clang -O3`, both with `-mavx2 -mfma -mavx512f -mavx512vl`, float and double, each linking
FFHT built the same way. Same array at 2^8 to 2^20 (gcc: every size; clang: even sizes), separate arrays at 2^12,
2^16, 2^20 (gcc only). The exactness gate and the plan check run first, as in [../harness-hybrid/](../harness-hybrid/).

## Check the source without an x86 machine

    SIMDE=/path/to/simde FFHT=/path/to/FFHT bash build_simde_check.sh

Output on an Apple M4, macOS, Apple clang 21.0.0, SIMDe v0.8.2, 22 October 2026:

    avx512_f32: CHECK sweep total: 1782 hybrid transforms (every form, every threshold candidate) exact / ALL PASS
    avx512_f64: CHECK sweep total: 1914 hybrid transforms (every form, every threshold candidate) exact / ALL PASS
    ARITH: every FFHT step does m*log2(m) cross-vector add/sub (+6 per vector in its in-lane step): YES
    PLAN MATCH (float, 2^3..2^20, 1470 steps compared)
    ARITH: every FFHT step does m*log2(m) cross-vector add/sub (+4 per vector in its in-lane step): YES
    PLAN MATCH (double, 2^2..2^20, 7898 steps compared)

## Files

`bench_h512.c` is the program; it includes `bench_k0.c` (and `bench.h`, `kernels_k0.h`) and adds `kernels_h512.h`
(the subtraction-first balanced textbooks, `python3 -B gen_x86.py tb8_balS circuits/h8_textbook_24.txt tb16_balS
circuits/h16_textbook_64.txt` gives it byte for byte). `summarize_h512.py` writes `out/SUMMARY.md`;
`asmcount_h512.py` counts the instructions of the timed functions. `LICENSE-FFHT` is FFHT's MIT licence, for the
parts of FFHT in `bench_h512.c` ([NOTICE](../../../../NOTICE), section 8). The other files are as in
[../harness-hybrid/](../harness-hybrid/README.md). Four earlier launches of this job, two on each machine, hung in
the script and produced nothing: a bare `wait` in bash 5.2 waited forever, first at the builds and then at the
exactness gate. `run.sh` here is the fixed version that ran.
