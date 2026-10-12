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
