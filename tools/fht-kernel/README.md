# tools/fht-kernel: a Walsh-Hadamard kernel with FFHT's entry points

This folder is a small C library for the Walsh-Hadamard transform. It has the same four functions, signatures and
return codes as FFHT (the fast Walsh-Hadamard library of Andoni, Indyk, Laarhoven, Razenshteyn and Schmidt), and it
runs FFHT's own plan of passes. The difference is the step it runs on the 8 vectors held in registers: by default
the 8-point member of the 3/4 family of this repository (g20: 20 operations when doublings are free, exact output;
`tools/circuits/programs/generated/G_family_8.txt`) instead of the textbook's 24 operations. It is not the 20-line
circuit shown in the top README, whose output is halved. Its code is the code of the timing program of 22 October
2026, cut down: a check (`check_same_as_harness.py`) shows that every step and every function of the plan is word for
word the code that was timed.

It has **not been timed as a library**. The program it is cut from took 0-2 % less time on AMD Zen 5 and 5-6 % less
on AMD Zen 4 than the best textbook code in the same structure (double precision, 2^10 to 2^16 points), gave no
clear gain on AMD Zen 2 and was slower on an Intel Broadwell Xeon:
[measurements/2026-10-22/](../../measurements/2026-10-22/README.md).

AI agents (Anthropic's Claude) wrote this folder at my direction, cut from the timing program they wrote. No person
has read the code line by line.

## The functions

| function | what it does |
|---|---|
| `int whtc_fht_float(float *buf, int log_n)` | y = H x in place on 2^log_n numbers, unnormalised, like FFHT's `fht_float` |
| `int whtc_fht_double(double *buf, int log_n)` | the same in double precision |
| `int whtc_fht_float_oop(float *in, float *out, int log_n)` | copies `in` to `out`, then transforms `out` (`in` unchanged) |
| `int whtc_fht_double_oop(double *in, double *out, int log_n)` | the same in double precision |
| `int whtc_fht_float_scaled(float *buf, int log_n, float scale)` | scale times H x, for example scale = 1/sqrt(n) for the orthonormal transform |
| `int whtc_fht_double_scaled(double *buf, int log_n, double scale)` | the same in double precision |
| `const char *whtc_step(void)` | which step and which code were compiled in, for example `"g20, AVX2 and FMA"` |
| `int whtc_plain_fht_float(...)`, `whtc_plain_fht_double(...)` | the portable code under its own names (always present) |

Every function returns 0 for `log_n` from 0 to 30 and 1 for any other value, as FFHT's code does (FFHT's README says
-1; its code returns 1). A `log_n` out of range touches no buffer; FFHT's `_oop` functions would first copy a
buffer of the wrong size. `log_n = 0` leaves the buffer as it is. The buffers need no alignment. The functions keep
no state and allocate nothing.

**Code written for FFHT.** Compile the library and your code with `-DWHTC_FFHT_NAMES`. The library then also
defines `fht_float`, `fht_double`, `fht_float_oop` and `fht_double_oop`, and `whtc.h` declares them along with
FFHT's C++ overloads `fht(...)`, so code written for FFHT compiles and links unchanged. Do not link it together with
FFHT itself in that case.

## Which code runs

- **AVX2 and FMA** (`whtc_avx2.c`) when the compiler targets them: `-mavx2 -mfma`, or `-march=native` on a recent
  x86-64 processor.
- **Portable C** (`whtc_plain.c`) otherwise, or with `-DWHTC_PLAIN`. It runs the same plan and the same step on plain
  C arrays of the same width (8 floats or 4 doubles) and gives the same results bit for bit; the tests check this. It
  is not meant to be fast.
- **The step**, chosen when compiling: `-DWHTC_STEP=G20` (the default), `TB8BALS` (the textbook with 12 of its
  additions written as multiply-adds by 1, each pair written subtraction first) or `TB8` (the textbook, FFHT's own
  step). TB8 and TB8BALS give the textbook's results bit for bit.

**Which step to use, from what I measured.** On AMD Zen 4 and Zen 5, g20 took 0.938-0.996 of the time of the best
textbook code in the same structure, depending on the chip and the compiler (double precision, 2^10 to 2^16; one
run per chip): G20 there, for a small gain that one run cannot establish. That is the only measurement that
favours G20, and this library itself has not been timed. On other processors I have no measurement that favours
any step of this folder over FFHT's own: TB8 (FFHT's own 24 operations) is the safe choice there. On AMD Zen 2 and
on the Intel Broadwell Xeon, G20 gave no gain
or was slower. On Zen 5 the TB8BALS step, with no circuit at all, took 0.80-0.84 of FFHT's time (and 0.90-0.93 on
Zen 4), but it was not timed on Zen 2 or on the Intel chip. Modern Intel processors, Apple and Arm processors were
not timed at all.

**Is 512-bit code better?** On Zen 5 a plain 512-bit textbook was 1.30-1.41 times as fast as the fastest 256-bit
program, circuits included. This folder has no 512-bit code.

## Results compared with FFHT's

On whole-number inputs the results are exact, and so the same as FFHT's. On other inputs G20 rounds differently from
the textbook. `tests/test_rounding.c` measures this at every size from 2^5 to 2^20 on numbers uniform in [-1, 1),
relative to the largest output, against the textbook in the same precision (which is what FFHT computes) and against
the exact transform (computed in double-double arithmetic):

| | G20 against the textbook | G20 against the exact transform | the textbook against the exact transform |
|---|---|---|---|
| float | at most 1.98e-07 | at most 1.56e-07 | at most 1.46e-07 |
| double | at most 4.54e-16 | at most 2.89e-16 | at most 2.44e-16 |

So G20 is about as accurate as the textbook, but **not bit-identical to FFHT**. Do not use it where bit-identical
output is promised. One more observation: on inputs from a plain 64-bit linear congruential generator, whose
structure lines up with the transform, both the textbook and G20 showed about four times these errors; the tests use
xorshift64*, as the timing program did.

## Build and test

    sh tools/fht-kernel/test.sh

It needs a C compiler (`CC`, default `cc`) and builds into `tools/fht-kernel/build/`. On x86-64 with AVX2 and FMA it
tests the AVX2 code; elsewhere the portable code. With `SIMDE_DIR=/path/to/simde` (SIMDe v0.8.2) it also tests the
AVX2 code through SIMDe, which emulates the x86 instructions on any machine; `WHTC_FETCH_SIMDE=1` fetches SIMDe
first. For each build it runs:

- `tests/test_exact.c`, for each of the three steps: whole numbers in [-4, 4] at every size from 2^0 to 2^20, float
  and double, equal to a plain textbook transform number for number (every intermediate value is a whole number below
  2^24, so float is exact too); the portable code equal to the compiled code on whole and real inputs; `_oop` and
  `_scaled`; FFHT's return codes;
- `tests/test_rounding.c` (the table above);
- a deliberately broken copy (`-DWHTC_BREAK`: one line of g20 with a wrong sign), which must fail the exactness test;
- `tests/ffht_names.c` and `tests/ffht_overloads.cpp`: code written for FFHT, linked under FFHT's names;
- `check_same_as_harness.py` (Python 3): the code is the timed code.

The last line is `OK: exact on integer inputs at every size 2^0 to 2^20 in float and double, FFHT's return codes,
broken copy caught.` On an Apple M4 with macOS it takes about 4 seconds, and about 8 with `SIMDE_DIR`; the outputs of
22 October 2026 are `tests/expected-macos-arm64.txt` (the portable code) and `tests/expected-macos-arm64-simde.txt`
(the AVX2 code through SIMDe). The AVX2 code has not been run natively on an x86 processor in this form; the
timing program it is cut from was, with the exactness gate described in the measurements.

To use the library in your project, compile `whtc_avx2.c` and `whtc_plain.c` with your flags and include `whtc.h`:

    cc -O2 -mavx2 -mfma -c whtc_avx2.c whtc_plain.c

## Timing it against FFHT

    sh tools/fht-kernel/bench.sh

x86-64 Linux with AVX2 and FMA only. It fetches FFHT at the commit named in the sources of the measurements page,
builds this library three times (G20, TB8BALS, TB8) and FFHT with the same flags into one program, and times them
taking turns on one pinned core, with the protocol of the measurements. **It has not been run yet.**

## Files

| file | what it is |
|---|---|
| `whtc.h` | the public header |
| `whtc_avx2.c`, `whtc_plain.c` | the AVX2 code and the portable code (and the shared entry points) |
| `whtc_steps.h` | the steps, word for word from the timed program |
| `whtc_ffht_plan.h` | FFHT's thresholds, in-lane sequences and plan of passes, word for word from the timed program |
| `whtc_impl.h`, `whtc_names.h` | internal: one precision of the kernel; the names and the choice of step |
| `check_same_as_harness.py` | compares the two files above with the timed program, block by block |
| `test.sh`, `tests/` | the tests and their recorded outputs |
| `bench.sh`, `tests/bench_whtc.c` | the timing against FFHT (not run yet) |
| `LICENSE-FFHT` | FFHT's licence |

## Licence

The new code in this folder is under the Apache License 2.0, as the rest of this repository (`LICENSE` at the top).
The parts named in `whtc_ffht_plan.h` (FFHT's recursion thresholds, its in-lane instruction sequences and its order
of passes) and the C++ overloads in `whtc.h` are FFHT's, under FFHT's MIT licence, which `LICENSE-FFHT` reproduces
with its copyright line. No file of FFHT is included. If a project needs this folder under the MIT licence as well,
open an issue on this repository and ask me.
