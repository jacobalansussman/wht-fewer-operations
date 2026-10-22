# harness-small: the sizes libraries use, many vectors per call

Libraries that use the Walsh-Hadamard transform for vector search or for quantising language models transform many
short vectors, of 64 to 512 points, at a time. This program times exactly that. Each timed call transforms a batch
of B vectors of n points (n = 2^6 to 2^9, and 2^10 and 2^12 to overlap with [../harness-hybrid/](../harness-hybrid/)).
B is chosen so the batch fits in half of the core's L2 cache. The data stays finite: the program renormalises it and
counts the results that are not finite (none were). The results page is [../../README.md](../../README.md), section
"The sizes libraries use".

Programs: FFHT on each vector; x86-wht's transform on each vector; FFHT's structure with textbook, balanced and
circuit steps (`hyb8-*`, `hyb16-*`); and straight-line transforms, in which one 8- or 16-vector step does all of a
short vector (`sl8-*`, `sl16-*`, among them `sl16-g20x2`, two g20 steps). Each balanced textbook comes in both
orders (multiply-add first, and the fair subtraction-first `...balS`).

Status: one run on AMD Zen 4 (EPYC 9B14) and one on AMD Zen 5 (EPYC 9B45) (`../runs/zen5-small/`), 22 October
2026, neither read by a reviewing agent after it finished.

## Run it again

On an x86-64 machine with AVX2 and FMA (AVX-512 is used when present), Ubuntu 24.04 or gcc, clang, git and python3
installed, idle, from this folder:

    bash run.sh

About 25 minutes with AVX-512 and 14 without; under 100 MB of memory. Builds: gcc and clang, `-O3 -mavx2 -mfma`,
and with AVX-512 also `-O3 -mavx2 -mfma -mavx512f -mavx512vl`; float and double: 8 binaries on a machine with
AVX-512. `SIZES`, `BATCH_KB` and `CORE` can be set; see the head of `run.sh`.

## Check the source without an x86 machine

    SIMDE=/path/to/simde FFHT=/path/to/FFHT bash build_simde_check.sh

Output on an Apple M4, macOS, Apple clang 21.0.0, SIMDe v0.8.2, 22 October 2026:

    avx2_f32: 28 broken-copy runs caught, 104 PASS lines, 0 other FAIL lines / ALL PASS
    avx2_f64: 31 broken-copy runs caught, 106 PASS lines, 0 other FAIL lines / ALL PASS
    avx512_f32: 24 broken-copy runs caught, 95 PASS lines, 0 other FAIL lines / ALL PASS
    avx512_f64: 30 broken-copy runs caught, 108 PASS lines, 0 other FAIL lines / ALL PASS
    ARITH: every FFHT step does m*log2(m) cross-vector add/sub (+6 per vector in its in-lane step): YES
    PLAN MATCH (float, 2^3..2^20, 1470 steps compared)
    ARITH: every FFHT step does m*log2(m) cross-vector add/sub (+4 per vector in its in-lane step): YES
    PLAN MATCH (double, 2^2..2^20, 7898 steps compared)

## Files

`bench_small.c` is the program; it includes `bench_hyb.c` of this folder (the same as
[../harness-hybrid/bench_hyb.c](../harness-hybrid/bench_hyb.c) with its `main` renamed, so that the plan check can
reach it). `kernels_k0.h` adds the subtraction-first 16-point textbook; `gen_x86_args.txt` is the generator command
that gives it byte for byte. `summarize_small.py` writes `out/SUMMARY.md`. The other files are as in
[../harness-hybrid/](../harness-hybrid/README.md). `LICENSE-FFHT` is FFHT's MIT licence, for the parts of FFHT in
`bench_hyb.c` ([NOTICE](../../../../NOTICE), section 8).
