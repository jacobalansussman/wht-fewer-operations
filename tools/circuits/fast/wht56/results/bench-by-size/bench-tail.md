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
