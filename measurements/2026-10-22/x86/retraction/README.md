# The evidence for the retracted figure

On 22 October I first wrote that, on AMD Zen 5, FFHT's structure with the 20-operation circuit took 11-15 % less time
than the fastest rival. That figure was wrong. The fastest rival was the balanced textbook, and its code, as written,
made the compiler copy registers it did not need to copy. The results page tells the story
([../../README.md](../../README.md), section "The figure I retracted"). This folder holds the evidence a reviewing
agent gathered before the corrected run, on an Apple M4, by compiling the timing program for x86-64 with clang 21
and reading the machine code. Nothing here was run on an x86 processor.

## Why the copies appear

An x86 multiply-add overwrites one of its inputs. The balanced textbook computes each pair of outputs from the same
two inputs, a + b (written as a multiply-add, b times 1 plus a) and a - b. When the multiply-add comes first, both
inputs are still needed afterwards, so the compiler first copies one of them to another register. When the
subtraction comes first, the multiply-add is the last use of its inputs and no copy is needed. The two orders do the
same 24 operations on the same numbers and round the same way.

## Files

| file | what it shows |
|---|---|
| `asm_counts_clang21_x86_64-linux.txt` | per timed step function and per build: additions and subtractions, multiply-adds, loads, stores, shuffles and register copies (`regmov`) |
| `asm_counts_clang21_mtune.txt` | the same for clang's tuning for Zen 5, Zen 4 and Haswell: the copies are there in every tuning |
| `innerloop_clang21.txt` | the instructions in the inner loop of one 8-point step: balanced textbook, multiply-add first, 55; subtraction first, 43; the 20-operation circuit, 35 |
| `innerloop.py` | the program that counts them from the disassembly |
| `clang21_avx2_f64_hsteps.asm` | the disassembly of the step functions, double precision, 256-bit |
| `gen_x86_args.txt` | the argument list of `gen_x86.py` that makes `../harness-hybrid/kernels_k0.h` |

The corrected run then counted the copies in the timed binaries themselves, gcc's as well as clang's, in
`../runs/zen5-hybrid/asm_counts.txt` (the column `regmov`; the code is in `asm.tar.gz` there).
