# harness-balance: one pass in registers, plain against balanced

This program asks one narrow question, at the kernel level (one step in registers, not a whole transform). AMD Zen
cores add on two pipes and multiply-add on two others. If half of the textbook's additions are written as
multiply-adds by 1, all four pipes can work: does that "balanced" textbook run faster, and do the circuits still
beat it? It times one pass over rows of 256 floats held in the L1 cache, built with `-march=native`, in AVX2 and
(where present) AVX-512, for the textbook, the balanced textbook (multiply-add first), the 19- and 22-operation
8-point steps, Alman and Rao's 22-operation step, and the 52-, 56- and 60-operation 16-point steps. Every kernel is
checked exact before anything is timed.

Results: [../../README.md](../../README.md), section "One step in registers".

## Run it again

On an x86-64 Linux machine with gcc, idle, from this folder:

    bash run.sh

About 2 to 4 minutes. `make_bench.py` writes `bench_avx2.c` and `bench_avx512.c` from the circuit files with
`gen.py`; gcc builds them with `-O3 -march=native` (and `-mprefer-vector-width=512` for AVX-512); every kernel is
checked exact (`CHECK_ONLY=1`); then two rounds of timing are pinned to CPU 1 (`out/res_*_r1.txt`, `_r2.txt`).

## A failure, kept

The first run on AMD Zen 4 stopped at its own exactness check (`../runs/zen4-balance-stopped/STOP.txt`): the
generator broadcast the wrong constant in AVX-512 code: it wrote `_mm512_set1_ps(*k+N)`, the first constant plus
N, where it meant `_mm512_set1_ps(*(k+N))`, the N-th constant. Nothing was timed. The generator was fixed and the run repeated (`../runs/zen4-balance/`).
`gen-before-fix.diff` shows the one changed line; the AMD Zen 2 run used the generator before the fix, which made no
difference there, since that machine has no AVX-512.
