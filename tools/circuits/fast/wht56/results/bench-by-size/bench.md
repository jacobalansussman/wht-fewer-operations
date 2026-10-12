# Benchmark by size: the new 8-point kernel on two machines

Made on the morning of 11 October 2026; the raw outputs carry the times. Status of everything
below: **measured, on two machines, twice on each**. Nothing here is a claim about any other machine.
The plain sentences are at the end, after the tables.

**Read this with it.** Later on the same day the 8-point step was timed inside FFHT, a tuned library for
this transform, where it was not faster at any size: [../ffht/README.md](../ffht/README.md). That test, and
not the plain C of this page, is the test that counts. The gain that this page reports on the Linux machine
at the sizes 8^j is not a gain of the step; sentences 4 and 5 at the end say where it comes from.

## What was timed

One array of N = 2^k numbers (64-bit floating point, "double"), held in memory, transformed in place by
one thread. Four programs, all from `src/wht56.c` and `src/kernels.h`, which are an unchanged snapshot of
the C programs in `../../c/` (`src/SNAPSHOT.sha256` holds their checksums):

1. **radix 2**: the textbook transform, one layer of additions and subtractions per pass over the array;
   k passes. `wht56_textbook_r2`.
2. **textbook radix 8**: the textbook again, but three layers per pass: each pass takes 8 numbers at a
   time and does 24 additions and subtractions on them. `wht56_textbook_r8`.
3. **new, exact**: the new 8-point kernel (19 additions and subtractions and one halving for each 8
   numbers) in the place of the 24; in the last pass every output is multiplied by 2^m as it is stored
   (m = k/3 rounded down), so the result is H x exactly. `wht56_k8`.
4. **new, up to scale**: the same without the final multiplications; the result is H x divided by 2^m.
   `wht56_k8_raw`.

Programs 2, 3 and 4 are organised the same way (same loops, same block size of 4,096 numbers for the
passes with a short stride), so a difference between them is a difference between the kernels.

**Sizes whose k is not a multiple of 3** (k = 10, 16, 20 here). The C program supports them like this:
the one or two address bits left over are done first by textbook radix-2 passes, the rest by 8-point
passes. This is the same in programs 2, 3 and 4. It is not the cheapest mix of the count tables in
`../../README.md`; it is what the C program does.

**32-bit integers: not measured.** The C program works on doubles only. The kernel halves a number, and
on whole numbers that halving is not always exact, so an integer version is a different program (the
numpy version of the same folder uses a 31-operation variant for integers). None was written here.

What was added to the snapshot, and nothing else: `src/bench_size.c` (the checks and the timing loop),
`src/run_bench.sh` (the two builds, the load average and the list of busy processes before and after),
`tables.py` (the tables below from the raw outputs). The raw outputs are in `raw/`.

## The check before timing

Before any timing, at every one of the 11 sizes, in every one of the 9 runs of the program (two runs of
two builds on two machines, and one control; 99 checks):
the input is filled with whole numbers from -1000 to 1000, and the output of **new, exact** is compared
with the output of **radix 2** by exact equality, on all N outputs. The same for textbook radix 8, and for
new-up-to-scale after multiplying by 2^m. At k up to 12, radix 2 is also compared with the definition
(every output summed directly in 64-bit integers). Then the same comparisons on real numbers between -1
and 1, up to rounding. **All passed** (the last line of each raw file is `CHECK OK`). This is a test on
one random input per size, not a proof; the proof is the Lean theorem, which is about the circuit and not
about this C code.

## Method

- Each timed loop repeats (copy the input into the work array, transform it). The number of repetitions
  is chosen per program and size so that one loop lasts about 0.30 s; the shortest loop of each row is in
  the last column of the tables.
- The copy alone is timed the same way. **Time of a transform = time of (copy, transform) minus time of
  (copy)**, minimum minus minimum and median minus median.
- 11 rounds per cell. In each round the five loops (copy and the four programs) run one after the other,
  and the order turns by one place each round, so drift of the machine falls on all of them.
- Cells show **minimum / median** over the 11 rounds, in **nanoseconds per point** for one whole
  transform (time of the transform divided by N).
- **Sign convention for the ratios: time of the new kernel divided by time of the other program, from the
  minima. Below 1 the new kernel took less time; 0.90 means 10% less time; 1.10 means 10% more.** One
  column gives exact / radix 8 from the medians, as a cross-check.
- "Largest spread" is the largest (median - minimum) / minimum over the five loops of the row, before the
  copy is taken off: a measure of how noisy that row was.
- Wall-clock time. One benchmark process at a time on each machine. The process was not tied to one
  processor core.
- **Everything was run twice.** In the first run the loops were set to 0.25 s, and in five rows of the
  Linux tables the shortest loop came out under 0.2 s (0.17 to 0.20 s). So the loop was lengthened to
  0.30 s and everything was run again. The second run is the **main run** (Tables 1 to 4). The first run is
  kept as a test of whether the numbers repeat (Table 5). In the main run two rows (Linux, scalar,
  k = 18 and 20) were disturbed by something else on the machine and their fastest loops lasted 0.12 s;
  those two rows are clean in the first run. Every row has at least one run with all loops above 0.2 s.
- Two controls were added after the first run showed two things that were not expected (see the plain
  sentences at the end): the Linux scalar build at `-O3` instead of `-O2` (Table 6), and the time of one
  single 8-point pass, by stride (the tables named "Control: one 8-point pass").

## The machines

| | Mac mini | rented Linux machine (the processor and the caches as the machine reports them; not measured) |
|---|---|---|
| processor | Apple M4: 4 fast cores, 6 slow cores | reports itself as an Intel Xeon at 2.20 GHz, a model of the Broadwell kind; a virtual machine, 4 cores seen as 8. The later timings in `../ffht/` found that its core does not time like that model |
| first cache (L1, data) | 128 KB per fast core (64 KB per slow core) | 32 KB per core |
| second cache (L2) | 16 MB, shared by the fast cores (4 MB for the slow ones) | 256 KB per core |
| third cache (L3) | none | 55 MB, shared by the cores (a virtual machine: other users of the host may share it too) |
| compiler | Apple clang 21.0.0 | gcc 13.3.0 |
| scalar build | `-std=c11 -O2 -fno-vectorize -fno-slp-vectorize` | `-std=c11 -O2 -fno-tree-vectorize` |
| vectorised build | `-std=c11 -O3 -mcpu=native` (NEON, 2 doubles per instruction) | `-std=c11 -O3 -march=native` (AVX2, 4 doubles per instruction) |
| other work during the runs | three other programs of mine, each using one core fully (3 busy processes listed before and after every run) | three other programs of mine, each using one core fully (3 listed before and after every run); a Lean build, another job of mine, was seen just before the runs |
| load average during the runs | 4.0 to 5.6 | 4.3 to 5.0 |

The loop touches two arrays (the input and the work array), so the memory in use is twice the "array"
column of the tables.

## The tables

### Table 1. Mac mini (Apple M4), scalar build (main run)

Raw output: `raw/mac2-scalar.txt`

- `machine: mac2; Darwin 25.6.0 arm64`
- `compiler: Apple clang version 21.0.0 (clang-2100.1.1.101)`
- `build scalar: cc -std=c11 -O2 -fno-vectorize -fno-slp-vectorize -o bench_size_scalar bench_size.c wht56.c -lm`
- `start: Sun Oct 11 10:06:08 EDT 2026`
- `load: 10:06  up 40 days, 16:25, 6 users, load averages: 5.57 5.06 5.85`
- `count: 3`
- `end: Sun Oct 11 10:09:27 EDT 2026`
- `load: 10:09  up 40 days, 16:29, 6 users, load averages: 4.87 5.04 5.68`
- `count: 3`
- checks before timing: whole-number input, exact equality, 11 sizes passed; real input, up to rounding, 11 sizes passed; last line of the program: CHECK OK
- rounds per cell: 11

| k | N | array | radix 2 | textbook radix 8 | new, exact | new, up to scale | exact / radix 8 | exact / radix 2 | scale / radix 8 | scale / radix 2 | exact / radix 8 (medians) | largest spread | shortest loop |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 3 | 8 | 64 B | 0.876 / 0.908 | 0.883 / 0.905 | 0.923 / 0.950 | 0.880 / 0.912 | 1.045 | 1.053 | 0.997 | 1.005 | 1.050 | 5% | 0.28 s |
| 6 | 64 | 512 B | 1.288 / 1.334 | 0.562 / 0.589 | 0.577 / 0.611 | 0.536 / 0.567 | 1.027 | 0.448 | 0.954 | 0.416 | 1.038 | 5% | 0.28 s |
| 9 | 512 | 4 KB | 1.652 / 1.756 | 0.676 / 0.712 | 0.685 / 0.721 | 0.626 / 0.678 | 1.013 | 0.415 | 0.925 | 0.379 | 1.013 | 8% | 0.28 s |
| 10 | 1,024 | 8 KB | 1.849 / 1.922 | 0.859 / 0.908 | 0.860 / 0.906 | 0.815 / 0.866 | 1.001 | 0.465 | 0.948 | 0.441 | 0.998 | 7% | 0.25 s |
| 12 | 4,096 | 32 KB | 2.224 / 2.272 | 0.886 / 0.907 | 0.878 / 0.903 | 0.840 / 0.870 | 0.992 | 0.395 | 0.949 | 0.378 | 0.995 | 4% | 0.28 s |
| 15 | 32,768 | 256 KB | 2.908 / 3.017 | 1.263 / 1.312 | 1.247 / 1.284 | 1.233 / 1.267 | 0.988 | 0.429 | 0.977 | 0.424 | 0.979 | 4% | 0.29 s |
| 16 | 65,536 | 512 KB | 3.127 / 3.281 | 1.516 / 1.557 | 1.492 / 1.535 | 1.502 / 1.548 | 0.984 | 0.477 | 0.991 | 0.480 | 0.986 | 5% | 0.28 s |
| 18 | 262,144 | 2 MB | 3.668 / 3.753 | 1.569 / 1.627 | 1.518 / 1.600 | 1.497 / 1.559 | 0.967 | 0.414 | 0.954 | 0.408 | 0.983 | 6% | 0.27 s |
| 20 | 1,048,576 | 8 MB | 4.122 / 4.180 | 2.012 / 2.058 | 2.018 / 2.069 | 2.011 / 2.051 | 1.003 | 0.490 | 1.000 | 0.488 | 1.005 | 3% | 0.29 s |
| 21 | 2,097,152 | 16 MB | 4.298 / 4.467 | 1.892 / 1.925 | 1.872 / 1.925 | 1.864 / 1.907 | 0.990 | 0.436 | 0.986 | 0.434 | 1.000 | 5% | 0.28 s |
| 24 | 16,777,216 | 128 MB | 5.071 / 5.213 | 2.233 / 2.263 | 2.223 / 2.294 | 2.189 / 2.246 | 0.995 | 0.438 | 0.981 | 0.432 | 1.014 | 3% | 0.30 s |

### Table 2. Mac mini (Apple M4), vectorised build (main run)

Raw output: `raw/mac2-vec.txt`

- `machine: mac2; Darwin 25.6.0 arm64`
- `compiler: Apple clang version 21.0.0 (clang-2100.1.1.101)`
- `build vec: cc -std=c11 -O3 -mcpu=native -o bench_size_vec bench_size.c wht56.c -lm`
- `start: Sun Oct 11 10:09:27 EDT 2026`
- `load: 10:09  up 40 days, 16:29, 6 users, load averages: 4.87 5.04 5.68`
- `count: 3`
- `end: Sun Oct 11 10:12:46 EDT 2026`
- `load: 10:12  up 40 days, 16:32, 6 users, load averages: 4.90 4.96 5.51`
- `count: 3`
- checks before timing: whole-number input, exact equality, 11 sizes passed; real input, up to rounding, 11 sizes passed; last line of the program: CHECK OK
- rounds per cell: 11

| k | N | array | radix 2 | textbook radix 8 | new, exact | new, up to scale | exact / radix 8 | exact / radix 2 | scale / radix 8 | scale / radix 2 | exact / radix 8 (medians) | largest spread | shortest loop |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 3 | 8 | 64 B | 0.956 / 0.978 | 1.118 / 1.167 | 1.391 / 1.444 | 1.357 / 1.404 | 1.244 | 1.455 | 1.214 | 1.420 | 1.237 | 5% | 0.29 s |
| 6 | 64 | 512 B | 1.122 / 1.137 | 0.541 / 0.558 | 0.595 / 0.612 | 0.581 / 0.597 | 1.100 | 0.531 | 1.073 | 0.517 | 1.096 | 3% | 0.29 s |
| 9 | 512 | 4 KB | 1.010 / 1.073 | 0.527 / 0.537 | 0.514 / 0.534 | 0.496 / 0.507 | 0.976 | 0.509 | 0.942 | 0.491 | 0.995 | 6% | 0.30 s |
| 10 | 1,024 | 8 KB | 1.128 / 1.157 | 0.609 / 0.625 | 0.619 / 0.639 | 0.595 / 0.608 | 1.017 | 0.549 | 0.978 | 0.528 | 1.022 | 3% | 0.30 s |
| 12 | 4,096 | 32 KB | 1.355 / 1.390 | 0.666 / 0.698 | 0.648 / 0.676 | 0.624 / 0.647 | 0.973 | 0.478 | 0.937 | 0.460 | 0.969 | 5% | 0.29 s |
| 15 | 32,768 | 256 KB | 1.780 / 1.801 | 0.932 / 0.949 | 0.888 / 0.903 | 0.887 / 0.908 | 0.953 | 0.499 | 0.951 | 0.498 | 0.952 | 2% | 0.29 s |
| 16 | 65,536 | 512 KB | 1.879 / 1.924 | 1.058 / 1.091 | 1.041 / 1.065 | 1.030 / 1.051 | 0.984 | 0.554 | 0.974 | 0.548 | 0.977 | 3% | 0.28 s |
| 18 | 262,144 | 2 MB | 2.122 / 2.174 | 1.096 / 1.138 | 1.067 / 1.099 | 1.064 / 1.100 | 0.973 | 0.503 | 0.971 | 0.501 | 0.966 | 4% | 0.30 s |
| 20 | 1,048,576 | 8 MB | 2.420 / 2.504 | 1.473 / 1.529 | 1.419 / 1.493 | 1.418 / 1.478 | 0.963 | 0.586 | 0.962 | 0.586 | 0.977 | 5% | 0.29 s |
| 21 | 2,097,152 | 16 MB | 2.449 / 2.577 | 1.321 / 1.343 | 1.257 / 1.325 | 1.236 / 1.269 | 0.951 | 0.513 | 0.936 | 0.505 | 0.987 | 5% | 0.28 s |
| 24 | 16,777,216 | 128 MB | 3.333 / 3.449 | 1.613 / 1.679 | 1.554 / 1.624 | 1.519 / 1.635 | 0.963 | 0.466 | 0.942 | 0.456 | 0.967 | 7% | 0.28 s |

### Table 3. rented Linux machine, scalar build (main run)

Raw output: `raw/linux2-scalar.txt`

- `machine: linux2; Linux 6.6.122+ x86_64`
- `compiler: gcc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0`
- `build scalar: gcc -std=c11 -O2 -fno-tree-vectorize -o bench_size_scalar bench_size.c wht56.c -lm`
- `start: Sun Oct 11 02:06:19 PM UTC 2026`
- `load:  14:06:19 up 20:14,  0 user,  load average: 4.55, 4.54, 4.91`
- `count: 3`
- `end: Sun Oct 11 02:09:56 PM UTC 2026`
- `load:  14:09:56 up 20:18,  0 user,  load average: 4.99, 4.69, 4.88`
- `count: 3`
- checks before timing: whole-number input, exact equality, 11 sizes passed; real input, up to rounding, 11 sizes passed; last line of the program: CHECK OK
- rounds per cell: 11

| k | N | array | radix 2 | textbook radix 8 | new, exact | new, up to scale | exact / radix 8 | exact / radix 2 | scale / radix 8 | scale / radix 2 | exact / radix 8 (medians) | largest spread | shortest loop |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 3 | 8 | 64 B | 2.515 / 2.554 | 2.735 / 2.774 | 2.967 / 3.171 | 2.706 / 2.712 | 1.085 | 1.180 | 0.990 | 1.076 | 1.143 | 7% | 0.26 s |
| 6 | 64 | 512 B | 2.957 / 3.132 | 1.951 / 2.004 | 2.432 / 2.484 | 2.138 / 2.153 | 1.246 | 0.822 | 1.096 | 0.723 | 1.240 | 6% | 0.30 s |
| 9 | 512 | 4 KB | 4.344 / 4.536 | 2.322 / 2.380 | 2.932 / 2.986 | 2.643 / 2.686 | 1.263 | 0.675 | 1.138 | 0.608 | 1.254 | 4% | 0.25 s |
| 10 | 1,024 | 8 KB | 4.656 / 4.783 | 2.972 / 3.044 | 3.526 / 3.602 | 3.251 / 3.320 | 1.187 | 0.757 | 1.094 | 0.698 | 1.183 | 4% | 0.30 s |
| 12 | 4,096 | 32 KB | 5.535 / 5.627 | 3.137 / 3.212 | 3.598 / 3.767 | 3.317 / 3.491 | 1.147 | 0.650 | 1.057 | 0.599 | 1.173 | 5% | 0.24 s |
| 15 | 32,768 | 256 KB | 6.706 / 6.776 | 3.458 / 3.515 | 4.291 / 4.373 | 4.016 / 4.045 | 1.241 | 0.640 | 1.161 | 0.599 | 1.244 | 16% | 0.28 s |
| 16 | 65,536 | 512 KB | 7.352 / 7.414 | 4.324 / 4.573 | 5.146 / 5.450 | 4.729 / 4.998 | 1.190 | 0.700 | 1.094 | 0.643 | 1.192 | 12% | 0.26 s |
| 18 | 262,144 | 2 MB | 9.200 / 16.991 | 5.133 / 9.648 | 5.769 / 11.308 | 5.344 / 10.743 | 1.124 | 0.627 | 1.041 | 0.581 | 1.172 | 107% | 0.12 s |
| 20 | 1,048,576 | 8 MB | 10.894 / 21.582 | 6.526 / 12.324 | 7.386 / 14.105 | 7.009 / 13.921 | 1.132 | 0.678 | 1.074 | 0.643 | 1.145 | 98% | 0.12 s |
| 21 | 2,097,152 | 16 MB | 12.527 / 12.641 | 6.389 / 7.145 | 7.393 / 7.544 | 6.926 / 7.321 | 1.157 | 0.590 | 1.084 | 0.553 | 1.056 | 11% | 0.23 s |
| 24 | 16,777,216 | 128 MB | 17.662 / 18.295 | 7.850 / 8.235 | 9.015 / 9.311 | 8.659 / 8.994 | 1.149 | 0.510 | 1.103 | 0.490 | 1.131 | 5% | 0.30 s |

### Table 4. rented Linux machine, vectorised build (main run)

Raw output: `raw/linux2-vec.txt`

- `machine: linux2; Linux 6.6.122+ x86_64`
- `compiler: gcc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0`
- `build vec: gcc -std=c11 -O3 -march=native -o bench_size_vec bench_size.c wht56.c -lm`
- `start: Sun Oct 11 02:09:56 PM UTC 2026`
- `load:  14:09:56 up 20:18,  0 user,  load average: 4.99, 4.69, 4.88`
- `count: 3`
- `end: Sun Oct 11 02:13:30 PM UTC 2026`
- `load:  14:13:30 up 20:21,  0 user,  load average: 4.34, 4.53, 4.78`
- `count: 3`
- checks before timing: whole-number input, exact equality, 11 sizes passed; real input, up to rounding, 11 sizes passed; last line of the program: CHECK OK
- rounds per cell: 11

| k | N | array | radix 2 | textbook radix 8 | new, exact | new, up to scale | exact / radix 8 | exact / radix 2 | scale / radix 8 | scale / radix 2 | exact / radix 8 (medians) | largest spread | shortest loop |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 3 | 8 | 64 B | 2.638 / 2.690 | 3.227 / 3.345 | 3.191 / 3.298 | 3.134 / 3.171 | 0.989 | 1.210 | 0.971 | 1.188 | 0.986 | 3% | 0.29 s |
| 6 | 64 | 512 B | 2.027 / 2.067 | 2.358 / 2.403 | 1.716 / 1.742 | 1.617 / 1.654 | 0.728 | 0.846 | 0.686 | 0.798 | 0.725 | 3% | 0.27 s |
| 9 | 512 | 4 KB | 1.978 / 1.991 | 2.334 / 2.390 | 1.488 / 1.523 | 1.417 / 1.451 | 0.638 | 0.752 | 0.607 | 0.717 | 0.637 | 3% | 0.26 s |
| 10 | 1,024 | 8 KB | 2.025 / 2.034 | 1.623 / 1.645 | 1.744 / 1.768 | 1.666 / 1.694 | 1.075 | 0.861 | 1.026 | 0.823 | 1.075 | 2% | 0.30 s |
| 12 | 4,096 | 32 KB | 2.312 / 2.335 | 2.550 / 2.709 | 1.723 / 1.969 | 1.651 / 1.683 | 0.676 | 0.745 | 0.648 | 0.714 | 0.727 | 14% | 0.29 s |
| 15 | 32,768 | 256 KB | 2.818 / 2.851 | 2.812 / 2.841 | 1.981 / 1.968 | 1.895 / 1.911 | 0.705 | 0.703 | 0.674 | 0.672 | 0.693 | 22% | 0.30 s |
| 16 | 65,536 | 512 KB | 3.002 / 3.043 | 2.270 / 2.301 | 2.457 / 2.496 | 2.340 / 2.365 | 1.082 | 0.819 | 1.031 | 0.780 | 1.085 | 4% | 0.29 s |
| 18 | 262,144 | 2 MB | 4.662 / 4.757 | 3.514 / 3.587 | 2.660 / 2.740 | 2.624 / 2.689 | 0.757 | 0.571 | 0.747 | 0.563 | 0.764 | 4% | 0.30 s |
| 20 | 1,048,576 | 8 MB | 6.393 / 6.600 | 3.550 / 3.681 | 3.716 / 3.849 | 3.696 / 3.886 | 1.047 | 0.581 | 1.041 | 0.578 | 1.046 | 5% | 0.28 s |
| 21 | 2,097,152 | 16 MB | 7.515 / 7.992 | 4.518 / 4.677 | 3.919 / 4.124 | 3.708 / 4.002 | 0.867 | 0.521 | 0.821 | 0.493 | 0.882 | 6% | 0.28 s |
| 24 | 16,777,216 | 128 MB | 12.719 / 13.096 | 5.962 / 6.179 | 5.488 / 5.574 | 5.419 / 5.590 | 0.921 | 0.431 | 0.909 | 0.426 | 0.902 | 3% | 0.31 s |

### Table 5. Do the ratios repeat? The first run beside the main run: new exact / textbook radix 8

Each cell: the ratio in the first run, the ratio in the main run (from the minima), then in brackets the textbook radix 8 time of the main run divided by that of the first run (1.00 means the machine gave the same time twice).

| k | Mac scalar | Mac vectorised | Linux scalar | Linux vectorised |
|--:|--:|--:|--:|--:|
| 3 | 1.117, 1.045 [0.98] | 1.304, 1.244 [1.05] | 1.090, 1.085 [0.98] | 0.990, 0.989 [1.01] |
| 6 | 1.043, 1.027 [0.95] | 1.102, 1.100 [1.07] | 1.244, 1.246 [1.01] | 0.724, 0.728 [0.99] |
| 9 | 1.010, 1.013 [0.93] | 0.972, 0.976 [1.01] | 1.259, 1.263 [1.00] | 0.645, 0.638 [0.99] |
| 10 | 1.014, 1.001 [0.96] | 1.123, 1.017 [1.14] | 1.197, 1.187 [1.00] | 1.092, 1.075 [1.01] |
| 12 | 0.999, 0.992 [0.97] | 0.972, 0.973 [1.03] | 1.163, 1.147 [1.00] | 0.684, 0.676 [0.99] |
| 15 | 0.979, 0.988 [0.99] | 0.926, 0.953 [1.01] | 1.227, 1.241 [0.98] | 0.705, 0.705 [0.98] |
| 16 | 0.999, 0.984 [1.01] | 0.961, 0.984 [0.97] | 1.164, 1.190 [0.97] | 1.064, 1.082 [0.98] |
| 18 | 0.999, 0.967 [1.03] | 0.967, 0.973 [0.99] | 1.173, 1.124 [1.06] | 0.754, 0.757 [1.01] |
| 20 | 0.990, 1.003 [0.98] | 0.998, 0.963 [1.02] | 1.148, 1.132 [1.01] | 1.051, 1.047 [0.98] |
| 21 | 1.011, 0.990 [1.03] | 0.980, 0.951 [1.00] | 1.169, 1.157 [1.01] | 0.874, 0.867 [1.00] |
| 24 | 1.000, 0.995 [1.03] | 0.962, 0.963 [1.01] | 1.160, 1.149 [1.03] | 0.907, 0.921 [0.99] |
| largest change of the ratio | 0.072 | 0.106 | 0.049 | 0.019 |

The same for new, up to scale / textbook radix 8 (first run, main run):

| k | Mac scalar | Mac vectorised | Linux scalar | Linux vectorised |
|--:|--:|--:|--:|--:|
| 3 | 1.090, 0.997 | 1.274, 1.214 | 1.007, 0.990 | 0.928, 0.971 |
| 6 | 0.962, 0.954 | 1.111, 1.073 | 1.090, 1.096 | 0.667, 0.686 |
| 9 | 0.932, 0.925 | 0.922, 0.942 | 1.154, 1.138 | 0.613, 0.607 |
| 10 | 0.957, 0.948 | 1.091, 0.978 | 1.100, 1.094 | 1.039, 1.026 |
| 12 | 0.941, 0.949 | 0.953, 0.937 | 1.024, 1.057 | 0.663, 0.648 |
| 15 | 0.961, 0.977 | 0.942, 0.951 | 1.149, 1.161 | 0.679, 0.674 |
| 16 | 0.980, 0.991 | 0.943, 0.974 | 1.079, 1.094 | 1.010, 1.031 |
| 18 | 0.974, 0.954 | 0.936, 0.971 | 1.099, 1.041 | 0.732, 0.747 |
| 20 | 0.968, 1.000 | 0.986, 0.962 | 1.087, 1.074 | 1.008, 1.041 |
| 21 | 1.001, 0.986 | 0.963, 0.936 | 1.109, 1.084 | 0.888, 0.821 |
| 24 | 1.021, 0.981 | 0.962, 0.942 | 1.107, 1.103 | 0.896, 0.909 |

### Table 6. Control: Linux machine, scalar code at -O3 (the flags of the earlier runs)

Raw output: `raw/linux-O3novec.txt`

- `machine: linux-O3novec; Linux 6.6.122+ x86_64`
- `compiler: gcc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0`
- `build linux-O3novec: gcc -std=c11 -O3 -fno-tree-vectorize -o bench_size_linux-O3novec bench_size.c wht56.c -lm`
- `start: Sun Oct 11 02:13:31 PM UTC 2026`
- `load:  14:13:31 up 20:21,  0 user,  load average: 4.34, 4.53, 4.78`
- `count: 3`
- `end: Sun Oct 11 02:17:09 PM UTC 2026`
- `load:  14:17:09 up 20:25,  0 user,  load average: 4.40, 4.53, 4.73`
- `count: 3`
- checks before timing: whole-number input, exact equality, 11 sizes passed; real input, up to rounding, 11 sizes passed; last line of the program: CHECK OK
- rounds per cell: 11

| k | N | array | radix 2 | textbook radix 8 | new, exact | new, up to scale | exact / radix 8 | exact / radix 2 | scale / radix 8 | scale / radix 2 | exact / radix 8 (medians) | largest spread | shortest loop |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 3 | 8 | 64 B | 2.421 / 2.526 | 2.798 / 2.866 | 3.023 / 3.227 | 2.786 / 2.984 | 1.080 | 1.248 | 0.996 | 1.151 | 1.126 | 6% | 0.30 s |
| 6 | 64 | 512 B | 3.019 / 3.065 | 1.926 / 1.973 | 2.459 / 2.486 | 2.121 / 2.180 | 1.276 | 0.814 | 1.101 | 0.702 | 1.260 | 3% | 0.29 s |
| 9 | 512 | 4 KB | 4.379 / 4.489 | 2.337 / 2.364 | 2.910 / 2.960 | 2.631 / 2.665 | 1.245 | 0.665 | 1.126 | 0.601 | 1.252 | 3% | 0.30 s |
| 10 | 1,024 | 8 KB | 4.812 / 5.161 | 3.055 / 3.219 | 3.463 / 3.645 | 3.265 / 3.424 | 1.133 | 0.720 | 1.069 | 0.678 | 1.132 | 7% | 0.30 s |
| 12 | 4,096 | 32 KB | 5.561 / 5.643 | 3.114 / 3.243 | 3.762 / 3.816 | 3.296 / 3.427 | 1.208 | 0.676 | 1.058 | 0.593 | 1.177 | 4% | 0.29 s |
| 15 | 32,768 | 256 KB | 6.777 / 7.071 | 3.663 / 3.719 | 4.296 / 4.387 | 3.978 / 4.056 | 1.173 | 0.634 | 1.086 | 0.587 | 1.180 | 18% | 0.21 s |
| 16 | 65,536 | 512 KB | 7.275 / 7.526 | 4.333 / 4.442 | 5.106 / 5.149 | 4.712 / 4.831 | 1.179 | 0.702 | 1.088 | 0.648 | 1.159 | 12% | 0.25 s |
| 18 | 262,144 | 2 MB | 8.775 / 8.947 | 4.623 / 4.670 | 5.606 / 5.650 | 5.243 / 5.340 | 1.213 | 0.639 | 1.134 | 0.597 | 1.210 | 7% | 0.26 s |
| 20 | 1,048,576 | 8 MB | 10.762 / 11.013 | 6.304 / 6.441 | 7.289 / 7.406 | 6.905 / 6.975 | 1.156 | 0.677 | 1.095 | 0.642 | 1.150 | 3% | 0.30 s |
| 21 | 2,097,152 | 16 MB | 12.987 / 13.398 | 6.345 / 6.599 | 7.463 / 7.689 | 7.027 / 7.343 | 1.176 | 0.575 | 1.108 | 0.541 | 1.165 | 4% | 0.29 s |
| 24 | 16,777,216 | 128 MB | 18.078 / 18.495 | 7.845 / 8.159 | 9.184 / 9.281 | 8.838 / 8.950 | 1.171 | 0.508 | 1.127 | 0.489 | 1.138 | 3% | 0.26 s |

### Control: one 8-point pass by stride, Mac mini (Apple M4), scalar build

Raw output: `raw/mac-pass-scalar.txt`. Cells: minimum / median, nanoseconds per point for ONE pass over 2,048 numbers.

- `build scalar: cc -std=c11 -O2 -fno-vectorize -fno-slp-vectorize -o bench_pass_scalar bench_pass.c -lm`
- `start: Sun Oct 11 10:12:48 EDT 2026`
- `load: 10:12  up 40 days, 16:32, 6 users, load averages: 4.83 4.94 5.50`
- `load: 10:13  up 40 days, 16:32, 6 users, load averages: 4.75 4.91 5.47`
- check (new pass = half the textbook pass, exactly): passed at every stride

| stride | textbook 8-point pass | new pass | new pass with scaled stores | new / textbook | scaled / textbook |
|--:|--:|--:|--:|--:|--:|
| 1 | 0.197 / 0.198 | 0.177 / 0.180 | 0.233 / 0.234 | 0.902 | 1.182 |
| 2 | 0.241 / 0.244 | 0.228 / 0.230 | 0.285 / 0.284 | 0.943 | 1.179 |
| 4 | 0.234 / 0.237 | 0.219 / 0.226 | 0.268 / 0.279 | 0.932 | 1.144 |
| 8 | 0.219 / 0.233 | 0.214 / 0.219 | 0.262 / 0.269 | 0.976 | 1.196 |
| 16 | 0.230 / 0.240 | 0.229 / 0.230 | 0.271 / 0.282 | 0.994 | 1.180 |
| 64 | 0.244 / 0.246 | 0.229 / 0.240 | 0.284 / 0.286 | 0.939 | 1.165 |
| 256 | 0.235 / 0.241 | 0.221 / 0.230 | 0.269 / 0.276 | 0.941 | 1.146 |

### Control: one 8-point pass by stride, Mac mini (Apple M4), vectorised build

Raw output: `raw/mac-pass-vec.txt`. Cells: minimum / median, nanoseconds per point for ONE pass over 2,048 numbers.

- `build vec: cc -std=c11 -O3 -mcpu=native -o bench_pass_vec bench_pass.c -lm`
- `start: Sun Oct 11 10:13:21 EDT 2026`
- `load: 10:13  up 40 days, 16:32, 6 users, load averages: 4.75 4.91 5.47`
- `load: 10:13  up 40 days, 16:33, 6 users, load averages: 5.05 4.97 5.47`
- check (new pass = half the textbook pass, exactly): passed at every stride

| stride | textbook 8-point pass | new pass | new pass with scaled stores | new / textbook | scaled / textbook |
|--:|--:|--:|--:|--:|--:|
| 1 | 0.200 / 0.202 | 0.181 / 0.184 | 0.201 / 0.207 | 0.907 | 1.005 |
| 2 | 0.162 / 0.177 | 0.175 / 0.174 | 0.201 / 0.207 | 1.085 | 1.242 |
| 4 | 0.161 / 0.162 | 0.157 / 0.157 | 0.183 / 0.186 | 0.975 | 1.137 |
| 8 | 0.155 / 0.161 | 0.144 / 0.150 | 0.170 / 0.178 | 0.928 | 1.097 |
| 16 | 0.158 / 0.158 | 0.150 / 0.149 | 0.172 / 0.175 | 0.945 | 1.087 |
| 64 | 0.155 / 0.160 | 0.146 / 0.145 | 0.165 / 0.175 | 0.939 | 1.063 |
| 256 | 0.152 / 0.160 | 0.146 / 0.152 | 0.166 / 0.174 | 0.960 | 1.096 |

### Control: one 8-point pass by stride, rented Linux machine, scalar build

Raw output: `raw/linux-pass-scalar.txt`. Cells: minimum / median, nanoseconds per point for ONE pass over 2,048 numbers.

- `build scalar: gcc -std=c11 -O2 -fno-tree-vectorize -o bench_pass_scalar bench_pass.c -lm`
- `start: Sun Oct 11 02:17:11 PM UTC 2026`
- `load:  14:17:11 up 20:25,  0 user,  load average: 4.40, 4.53, 4.73`
- `load:  14:17:45 up 20:26,  0 user,  load average: 4.35, 4.50, 4.72`
- check (new pass = half the textbook pass, exactly): passed at every stride

| stride | textbook 8-point pass | new pass | new pass with scaled stores | new / textbook | scaled / textbook |
|--:|--:|--:|--:|--:|--:|
| 1 | 0.776 / 0.795 | 0.873 / 0.881 | 1.162 / 1.177 | 1.124 | 1.497 |
| 2 | 0.977 / 1.010 | 0.852 / 0.873 | 1.348 / 1.376 | 0.872 | 1.380 |
| 4 | 0.859 / 0.928 | 0.909 / 0.947 | 1.264 / 1.307 | 1.059 | 1.473 |
| 8 | 0.799 / 0.804 | 0.894 / 0.901 | 1.212 / 1.217 | 1.119 | 1.516 |
| 16 | 0.772 / 0.812 | 0.873 / 0.891 | 1.180 / 1.187 | 1.131 | 1.529 |
| 64 | 0.756 / 0.785 | 0.873 / 0.905 | 1.159 / 1.202 | 1.154 | 1.532 |
| 256 | 0.747 / 0.752 | 0.861 / 0.873 | 1.150 / 1.157 | 1.153 | 1.539 |

### Control: one 8-point pass by stride, rented Linux machine, vectorised build

Raw output: `raw/linux-pass-vec.txt`. Cells: minimum / median, nanoseconds per point for ONE pass over 2,048 numbers.

- `build vec: gcc -std=c11 -O3 -march=native -o bench_pass_vec bench_pass.c -lm`
- `start: Sun Oct 11 02:17:45 PM UTC 2026`
- `load:  14:17:45 up 20:26,  0 user,  load average: 4.35, 4.50, 4.72`
- `load:  14:18:20 up 20:26,  0 user,  load average: 4.32, 4.48, 4.70`
- check (new pass = half the textbook pass, exactly): passed at every stride

| stride | textbook 8-point pass | new pass | new pass with scaled stores | new / textbook | scaled / textbook |
|--:|--:|--:|--:|--:|--:|
| 1 | 1.584 / 1.607 | 0.792 / 0.803 | 0.871 / 0.881 | 0.500 | 0.550 |
| 2 | 0.705 / 0.720 | 0.726 / 0.732 | 0.849 / 0.879 | 1.029 | 1.205 |
| 4 | 0.391 / 0.399 | 0.401 / 0.407 | 0.464 / 0.469 | 1.026 | 1.186 |
| 8 | 0.303 / 0.303 | 0.330 / 0.355 | 0.409 / 0.411 | 1.091 | 1.352 |
| 16 | 0.254 / 0.263 | 0.288 / 0.292 | 0.359 / 0.364 | 1.135 | 1.413 |
| 64 | 0.214 / 0.217 | 0.251 / 0.254 | 0.321 / 0.322 | 1.176 | 1.500 |
| 256 | 0.216 / 0.218 | 0.244 / 0.268 | 0.309 / 0.320 | 1.134 | 1.434 |

### Table 7. Operation count at the same sizes (count (O): every operation costs one)

As the C program does it: k mod 3 textbook layers, then 8-point passes of 20 operations per 8 points, then N multiplications for the exact form.

| k | N | textbook operations | new, exact | new, up to scale | exact / textbook | scale / textbook |
|--:|--:|--:|--:|--:|--:|--:|
| 3 | 8 | 24 | 28 | 20 | 1.167 | 0.833 |
| 6 | 64 | 384 | 384 | 320 | 1.000 | 0.833 |
| 9 | 512 | 4,608 | 4,352 | 3,840 | 0.944 | 0.833 |
| 10 | 1,024 | 10,240 | 9,728 | 8,704 | 0.950 | 0.850 |
| 12 | 4,096 | 49,152 | 45,056 | 40,960 | 0.917 | 0.833 |
| 15 | 32,768 | 491,520 | 442,368 | 409,600 | 0.900 | 0.833 |
| 16 | 65,536 | 1,048,576 | 950,272 | 884,736 | 0.906 | 0.844 |
| 18 | 262,144 | 4,718,592 | 4,194,304 | 3,932,160 | 0.889 | 0.833 |
| 20 | 1,048,576 | 20,971,520 | 18,874,368 | 17,825,792 | 0.900 | 0.850 |
| 21 | 2,097,152 | 44,040,192 | 38,797,312 | 36,700,160 | 0.881 | 0.833 |
| 24 | 16,777,216 | 402,653,184 | 352,321,536 | 335,544,320 | 0.875 | 0.833 |

## What the numbers say, in plain sentences

"Less time" and "more time" below always compare the new kernel with the **textbook radix 8** (the same
program with the 24-operation kernel) unless radix 2 is named. Percentages come from the ratio columns of
the main run; the first run is quoted where it differs.

1. **Mac, scalar build: no difference for the exact transform.** From 64 points (k = 6) up, the exact
   transform with the new kernel took the same time as the textbook radix 8, within 4% either way (within
   5% in the first run). At 8 points it took 5 to 12% more. Up to a scale factor (no final
   multiplications) it took 0 to 8% less; 4 to 8% less from 64 to 4,096 points in both runs.

2. **Mac, vectorised build: a small gain from 4,096 points up.** For k = 12 to 24 the exact transform took
   2 to 5% less time (0 to 7% less in the first run), and 2 to 3% less at 512 points. It took more time at
   the small sizes: 24 to 30% more at 8 points, 10% more at 64 points, 2% more at 1,024 points (12% more in
   the first run, in a noisy row). Up to a scale factor: 2 to 6% less from 512 points up.

3. **Linux, scalar build: the new kernel was slower at every size.** The exact transform took 12 to 26%
   more time from 64 points up (8 to 9% more at 8 points), in both runs. Up to a scale factor it still took
   4 to 16% more. The control at `-O3` (Table 6) gave the same: 13 to 28% more for the exact transform.

4. **Linux, vectorised build: faster at some sizes, slower at others, and the reason is not the kernel's
   operation count.** When k is a multiple of 3, the exact transform took 24 to 36% less time for k = 6 to
   18, 13% less at k = 21 and 8% less at k = 24 (9% in the first run). When k is not a multiple of 3
   (k = 10, 16, 20) it took 5 to 8% **more** time. Both runs agree to within 0.02 in every ratio.

5. **Why sentence 4 looks like that (the per-pass control).** One single 8-point pass was timed alone, for
   each distance ("stride") between the 8 numbers. On Linux, vectorised, at stride 1 the textbook pass
   took 1.58 nanoseconds per point and the new pass 0.79. That textbook figure is twice what the *same*
   pass takes in the scalar build (0.78): gcc's vector code for that one pass of the textbook is poor. At
   every other stride the new pass took 3 to 18% **more** time than the textbook pass. A pass with stride
   1 exists in this program only when k is a multiple of 3. So the whole gain of sentence 4 comes from
   that one pass and from what this compiler did with the textbook code there. A textbook program that
   treated that pass differently would probably not lose; none was written, so this last sentence is
   an expectation, not a measurement. (In the same build the textbook radix 8 is even slower than radix 2
   at k = 6 and 9 in both runs and at k = 12 in the main run, which fits the same explanation.)

6. **The same control on the Mac.** There the new pass took 1 to 10% less time than the textbook pass at
   every stride in the scalar build, and 2 to 9% less in the vectorised build except at stride 2 (about
   8% more). The pass that also multiplies its outputs (the last pass of the exact transform) took 14 to 20%
   more than a textbook pass in the scalar build, 0 to 24% more in the vectorised build. That is why the
   exact transform comes out level on the Mac: the last pass gives back what the others gain.

7. **Against radix 2.** From 64 points up the exact transform with the new kernel took 40 to 49% of the
   radix-2 time on the Mac scalar build, 47 to 59% on the Mac vectorised build, 51 to 82% on the Linux
   scalar build and 43 to 86% on the Linux vectorised build. This is mostly not the new kernel: the
   textbook radix 8 is within 5% of it on the Mac and is quicker than it on the Linux scalar build. Doing
   three layers per pass is the big effect: each number is loaded and stored once per three layers
   instead of once per layer.

8. **Caches.** The Mac's fast cores have 128 KB of first-level cache and share 16 MB of second-level
   cache; there is no third level. The Linux machine reports 32 KB and 256 KB per core and a shared 55 MB
   third level; these sizes were not measured, and the later timings beside FFHT (`../ffht/README.md`,
   section 4) found its time per point jumping between arrays of 8 and 16 MB, far below 55 MB. The
   benchmark holds two arrays (input and work array), so by the reported sizes the first-level cache is
   outgrown above k = 13 on the Mac and above k = 11 on Linux, the Linux second level above k = 14, the
   Mac second level above k = 20, the Linux third level above k = 21. On the Mac the time per pass rose
   only a little with size (vectorised textbook radix 8: 0.17 nanoseconds per point per pass at k = 12,
   0.20 at k = 24) and the ratio new / textbook did not move with it. On Linux each step up in size cost
   more once the array had left the second-level cache (vectorised textbook radix 8: going from k = 12
   to 15 added 0.26 nanoseconds per point, from 15 to 18 added 0.70, from 18 to 21 added 1.00, from 21 to
   24 added 1.44; each step is one more pass), and about the same for the new kernel. The time then goes to moving memory, not to arithmetic, and the ratio moves toward 1
   (0.68 at k = 12, 0.76 at k = 18, 0.87 at k = 21, 0.92 at k = 24).

9. **Measured gain against the gain in operation count** (count (O), every operation costs one; Table 7).
   At k = 12 the new kernel does 8.3% fewer operations than the textbook for the exact transform and
   16.7% fewer up to a scale factor. Measured at k = 12, exact: 1% less time (Mac scalar), 3% less (Mac
   vectorised), 15% more (Linux scalar), 32% less (Linux vectorised, the compiler effect of sentence 5).
   At k = 24 the count says 12.5% fewer; measured: 0.5% less, 4% less, 15% more, 8% less. At k = 3 the
   exact count is 28 against 24 (16.7% more) and at k = 6 the counts are equal; the exact count is below
   the textbook only from k = 9. **In no build did the time follow the operation count.** One pass has 8
   loads and 8 stores whichever kernel is used, and the new kernel's operations depend on each other in
   a longer chain (7 steps deep against 3); whether that is the cause was not tested.

10. **How far to trust this.** Each machine ran three other jobs that each kept one core busy all the
    time (load average 4.0 to 5.6 on the Mac's 10 cores, 4.3 to 5.0 on the Linux machine's 4 cores seen
    as 8), so on Linux the benchmark shared a physical core with another job. In most rows the median was within 8% of
    the minimum; some Linux rows had 10 to 30%, and one Mac row 13%. In the main run two Linux scalar rows
    (k = 18 and 20) were disturbed: the medians are twice the minima and the fastest loops lasted only
    0.12 s; for those two rows use the first run, which was clean and gives 17% and 15% more time. Every
    row has at least one run in which all its loops lasted more than 0.2 s. Between the two runs the
    ratio new exact / textbook radix 8 changed by at most 0.02 on Linux vectorised, 0.05 on Linux scalar,
    0.07 on Mac scalar (at 8 points; 0.03 elsewhere) and 0.11 on Mac vectorised (one noisy row at 1,024
    points in the first run; 0.06 elsewhere). So differences of 3% or less on the Mac are inside the
    noise, and the Linux signs (slower in scalar code; faster or slower in vectorised code according to
    k) are solid. Two machines, two compilers, one program layout, doubles only: nothing here says what
    another machine, another compiler or a tuned library would do.

## What this means for "at which sizes does it have a use"

On these two machines the new kernel did not buy running time in proportion to its operation count at
any size. In short: on the Mac, from 4,096 points up, a gain of 2 to 5% with
vector instructions and none without; up to a scale factor, up to 8%; on the Linux machine, a loss in
scalar code, and in vectorised code a large gain at sizes 8^j that comes from one pass the compiler
handled badly for the textbook, with a small loss at the other sizes. At 8 and 64 points the exact form
is not cheaper even in the count. The result is a result about the number of operations.

## What this changes in the earlier runs

The folder above this one (`../`) holds seven earlier runs on the Linux machine and six on the Mac, made the
same morning with `../../c/bench.c`, when both machines were more heavily loaded. All of them were at sizes
whose k is a multiple of 3 (2^9, 2^12, 2^15, 2^18 and 2^21 points). At those sizes, on the Linux machine with
vector instructions, the new kernel was faster in every one of those runs, by 5 to 39%. The runs here, on
quieter machines, show three things about that: (a) at k = 10, 16 and 20 the sign is the other way; (b) the
gain at multiples of 3 comes from the stride-1 pass alone, and from what the compiler did with the textbook
code there; (c) in scalar code on Linux the new kernel is slower by 12 to 28%, at `-O2` and at `-O3`. So
"faster on one machine with vector instructions" is not a fair summary of the earlier runs. Sentences 4
and 5 above are.

## Files

- `src/` : `wht56.c`, `wht56.h`, `kernels.h`, `bench.c`, `build_and_bench.sh` (snapshot, unchanged;
  `SNAPSHOT.sha256`); added: `bench_size.c`, `run_bench.sh`, `run_one.sh`, `bench_pass.c`, `run_pass.sh`.
- `raw/mac2-scalar.txt`, `raw/mac2-vec.txt`, `raw/linux2-scalar.txt`, `raw/linux2-vec.txt` : main run.
- `raw/mac-scalar.txt`, `raw/mac-vec.txt`, `raw/linux-scalar.txt`, `raw/linux-vec.txt` : first run.
- `raw/linux-O3novec.txt` : control, Linux scalar at `-O3`.
- `raw/mac-pass-*.txt`, `raw/linux-pass-*.txt` : control, one pass by stride.
- `tables.py` : writes this file from `bench-head.md`, the raw outputs and `bench-tail.md`.
- To repeat: `sh src/run_bench.sh raw <label> 11`, then `sh src/run_pass.sh raw <label> 9`, then
  `python3 -B tables.py`.
