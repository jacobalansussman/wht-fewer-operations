# harness-wht: the first timing program of the night (superseded)

This was the first program of 21 to 22 October 2026. It times three things on one core of an x86-64 processor:

- **one pass** (`pass`): one radix-8 or radix-16 pass over an array that fits in the L1 cache, with 1 to 4
  independent blocks interleaved per loop round. This is the kernel level: one step in registers, not a whole
  transform;
- **registers only** (`regs`): the step applied again and again to values held in registers, with no memory
  traffic. With one block this is bound by the latency of the chain of operations;
- **whole transforms** (`whole`) of 2^6 to 2^24 points in its own structure (in-lane levels, radix-16 passes inside
  blocks of 32 KB, radix-8 passes above), against FFHT and its own textbook.

It is kept as run, because its pass and register figures are quoted on the results page (section "One step in
registers"). Its whole-transform figures are **superseded** by [../harness-hybrid/](../harness-hybrid/), for two
reasons found by a reviewing agent: its whole transform looked up the step's function by name on every call (a
string comparison that charged the circuit variants more than the program's own textbook, and every program of its
own more than FFHT), and its balanced textbook was written multiply-add first,
the handicapped rival of the retraction. Its structure is also not FFHT's.

## Run it again

On an x86-64 machine with AVX2 and FMA, Ubuntu 24.04 or gcc, clang, git and python3 installed, idle:

    bash run.sh                # MODE=quick, 30 to 45 minutes
    MODE=full bash run.sh      # every binary, every size, about 2 hours

Builds: gcc and clang, `-O3 -mavx2 -mfma`, float and double; with AVX-512 also 256-bit code with 32 registers and
512-bit code (`-mavx512f -mavx512vl` added).

## Check the source without an x86 machine

    SIMDE=/path/to/simde bash build_simde_check.sh

Output on an Apple M4, macOS, Apple clang 21.0.0, SIMDe v0.8.2, 22 October 2026:

    avx2_f32: ALL PASS
    avx2_f64: ALL PASS
    avx512_f32: ALL PASS
    avx512_f64: ALL PASS

## Files

`bench_k0.c` (the program), `bench.h` (the timing protocol), `kernels_k0.h` (the steps; `python3 -B gen_x86.py`
with the argument list of `../retraction/gen_x86_args.txt` less `tb8_balS circuits/h8_textbook_24.txt` gives it
byte for byte), `gen_x86.py` and `gen_kernels.py` (the generator), `asmcount.py` and `summarize.py`, `run.sh`, the
shared `az_pre.sh` and `az_quiet.py`, and `circuits/`.
