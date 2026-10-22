# The 8-point step inside FFHT: the timings

*Revision 2, 22 October 2026: AMD processors and AVX-512 were timed later, in a different test that keeps
FFHT's structure: see [measurements/2026-10-22/](../../../../../../measurements/2026-10-22/README.md). Apart from
this note and one line in section 5, this page is unchanged; it describes the timings of 11 October.*

This page is the long version of the section "Is it faster in practice?" of
[the README](../../../../../../README.md). The question: does the new 8-point step make a tuned library
for the Walsh-Hadamard transform faster? On the one machine that was timed, the answer is no.

The timings were made on 11 October 2026 by the AI agents (Anthropic's Claude) that I direct, on a Linux
machine that I rented. Two further agents then checked the reports against the raw outputs and the
sources. They could not time anything again, because the rented machine had gone offline. No person has
read the programs line by line.

**Words.**

- **Vector instructions.** Processor instructions that work on several numbers at once. Here one
  instruction handles 8 single-precision numbers ("floats", 4 bytes each) or 4 double-precision numbers
  ("doubles", 8 bytes each). AVX, AVX2 and FMA are the names of the sets of such instructions this machine
  has.
- **Register.** One of the 16 working slots inside the processor that such an instruction reads and
  writes. One register holds 8 floats or 4 doubles.
- **Fused multiply-add.** One instruction that computes a + b × c. With c = 2 it gives "a plus twice b" in
  one step. It belongs to the FMA set.
- **Cache.** Small, fast memory inside the processor. Data that does not fit there has to come from main
  memory, which is much slower.
- **Pass.** One sweep over the whole array: it loads every number once, does up to three levels of the
  transform, and stores every number once.
- **The step.** FFHT does three levels of the transform across 8 registers at a time. That is the textbook
  8-point step: 24 additions and subtractions. The new step does the same job with 19 additions and
  subtractions and one halving (20 operations, output halved), or with 7 additions and subtractions and 12
  fused multiply-adds (19 operations, output exact).
- **Chain.** The longest run of operations in which each one has to wait for the one before.

## 1. The answer

**Speed: fewer operations did not mean less time where I measured.** The test that counts is against FFHT
(<https://github.com/FALCONN-LIB/FFHT>), a well-known fast library for this transform. Its code is written
out as vector instructions, which work on 8 single-precision or 4 double-precision numbers at once, each
group held in one of the processor's 16 registers. FFHT already does three levels of the transform across 8
registers at a time, with the textbook's 24 additions and subtractions. I wrote the new 8-point step into
the code that FFHT's own generator produces, in place of that 24-operation block, in every pass that works
on 8 registers at once, and changed nothing else. On the one machine I timed, this did not make FFHT faster
at any size from 2^6 to 2^26 points in single precision or from 2^5 to 2^26 points in double precision.

I tried three forms: 20 operations with the output left divided by a power of two, which is not the same
output as FFHT's; 20 operations with 8 multiplications added in one pass so that the output is exact; and
19 operations with fused multiply-add (one instruction for "a plus twice b"), exact. Set against a second
build of FFHT's unchanged code, all 129 combinations of size and form took more time.

- From 2^7 to 2^19 points in single precision the changed FFHT took 11 to 18 % more time in the exact
  20-operation form, 4 to 9 % more with the output left divided, and 1 to 7 % more in the fused form. From
  2^6 to 2^19 points in double precision it took 12 to 24 %, 5 to 12 % and 4 to 11 % more. Two builds of
  identical code differed by less than 2 % in 83 of 87 cases and by 3.6 % at the worst, so at two
  single-precision sizes, 2^13 and 2^19, the 1 and 2 % of the fused form is not a difference this
  measurement can show.
- From 2^20 to 2^26 points (arrays of 4 MiB to 512 MiB), averaged over those seven sizes, it took 7 %
  (single precision) and 6 % (double) more time in the exact 20-operation form, 5 and 3 % more with the
  output left divided, and 3 and 2 % more in the fused form. At these sizes two timings of the same pair
  differed by up to 5 points, so no figure is given for a single size, and for the fused form the loss is
  too small for one run to establish. What the run shows for it is no gain.
- At the two smallest sizes, 2^6 points in single precision and 2^5 in double precision, a transform is a
  single block of FFHT's first pass, and the benchmark transforms the same array again and again, so each
  transform waits for the one before. There the loss was largest: 16 and 23 % with the output left divided,
  23 and 33 % exact, 10 and 15 % fused. With separate arrays the loss would be smaller; by how much was not
  measured.

The changed code does have fewer instructions, as the operation counts say: 20 or 19 arithmetic
instructions in place of 24 in each such block. Over a whole transform that is 2 to 8 % fewer vector
instructions with the output left divided, up to 10 % fewer in the fused form, and between 3 % more and 6 %
fewer in the exact 20-operation form. The likely reason for the lost time is the order in which the
operations depend on each other. In the textbook block no result is more than 3 operations away from the
loaded numbers. In the new step the last results are 7 operations away, 6 in the fused form. In a test of
one pass alone with the count held at 20, a block with a chain of 3 took 15 to 16 % less time than FFHT's
block, and the real block with its chain of 7 took 23 to 24 % more (one run, 15 repeats, 16 KiB of
single-precision and 2 KiB of double-precision data). In the same test, four operations fewer at an equal
chain were worth 4 to 5 % of a pass. So the saving is there and the chain outweighs it. What happens inside
the processor was not measured, so this is an explanation that fits, not a finding.

In my own plain C, compiled by gcc 13.3.0 with `-O3 -march=native` on the same machine, the new step took
less time than the textbook step only in double precision at the sizes 2^6, 2^9, 2^12 and so on to 2^27: 7
to 37 % less with exact output (best of 9 repeats, two runs that agree within 0.03 in the ratio). In double
precision at every other size from 2^4 to 2^26 it took 1 to 13 % more, and in single precision at every
size from 2^3 to 2^27 it took 2 to 51 % more. At 2^6 to 2^18 points the gain is larger than replacing 24
operations by 20 can give, which is 17 % at most. So it comes from how the compiler treats one pass of my
code and not from the operation count. The cause has not been found. FFHT took less time than each of my
plain C programs at every size from 2^3 to 2^27 points: my fastest plain C program took 1.3 to 4.1 times as
long as FFHT in single precision and 1.2 to 2.7 times as long in double precision.

**The fused form in a program of my own.** Counted with doubling free, the 8-point step has 19 operations
against the textbook's 24, and on a processor with a fused multiply-add each of the 19 is one instruction
and the output is the exact transform. I timed that form on one machine (the same rented machine, gcc
13.3, one thread, single precision) and it was not faster than the textbook step in the same program:
about 4 % more time at 2^12 and 2^15 points, where the data fits in the processor's cache (2 to 8 % over
ten runs), and the same time within 2 % at 2^26 points, where it does not.

**How this was measured.** On one rented virtual machine with the AVX2 and FMA instruction sets. It reports
itself as an Intel Xeon at 2.20 GHz, and other programs ran on it at full load the whole time. The compiler
was gcc 13.3.0. FFHT was the version it has stood at since March 2019, built by its own Makefile, with the
plan of passes it ships. One thread, kept on one processor. Times are wall-clock: the best of 15 repeats of
a loop of 0.2 s or more (9 repeats where a size was timed a second time, and for the plain C), with the
programs taking turns inside one process, on 11 October 2026. Each changed version returned exactly FFHT's
output on inputs of small integers at every size from 2^1 to 2^24 points, in single and double precision;
the version that leaves its output divided did so after multiplying by its power of two. Rounding errors on
general real-valued data were not compared. The timings were made by the AI agents I work with, in one run
unless said otherwise, and they have not been repeated on a second machine, with a second compiler, or by
anyone else. So this is a measurement of time on one machine in one library. It says nothing about other
processors, and nothing against the operation counts.

## 2. What was compared

1. **FFHT as shipped.** The library at its last version (March 2019), built by its own Makefile, with the
   plan of passes it ships. Its code is vector instructions written out one by one by its own generator
   program, so the compiler decides almost nothing.
2. **FFHT built a second time.** The same instructions at another place in the program. What it differs
   from (1) by is what no step can be credited with.
3. **My earlier plain C.** Three programs: the textbook step, the new step with exact output, the new step
   with the output left divided. They are ordinary C, and gcc turns them into vector instructions by
   itself. They are the programs of [wht56/c/](../../c/).
4. **The new step in FFHT's style, first way: inside FFHT's own generator.** The generator's 24-operation
   block was replaced by the new step in every pass that works on 8 registers. Nothing else changed. Three
   forms:
   - 20 operations, output left divided by a power of two. This is not FFHT's output; it is H x / 2^P,
     where P is the number of such passes.
   - 20 operations, and 8 multiplications added in one pass (one multiplication per number), which makes
     the output exact.
   - 19 operations with fused multiply-add, output exact. FFHT itself needs only AVX; this form also needs
     FMA.
5. **The new step in FFHT's style, second way: my own C with intrinsics.** Intrinsics are C functions that
   each stand for one vector instruction. This code follows FFHT's plan of passes and has the textbook step
   and the new step in the same text. Its whole-transform timings were still trial runs when the machine
   went offline. They do not count and no figure from them is used here. What counts from this style is a
   test of one pass alone, and the timing of the fused form in single precision above.

**Like-for-like pairs.** A pair is two programs that are the same code except for the 8-point step. FFHT
against the changed FFHT of (4) is such a pair: same loops, same loads and stores, same plan of passes,
same compiler flags. The textbook step and the new step in my own vector code (5) are another. My plain C
is a pair in its source, but not in what the compiler makes of it (section 3, last tables).

**Why the pairs are the real test.** A whole program differs from FFHT in many things at once: how the
first levels are done, the order of the loops, what the compiler chose. At 2^12 and 2^15 points in single
precision the textbook step in my own vector code took 13 to 14 % less time than FFHT, and the new
19-operation step in the same code took about 4 % more than that textbook. So "my program beats FFHT" would
have been true and would have said nothing about the step. Only a pair isolates the step. Every pair says
the same thing: the step gains nothing here.

## 3. The tables by size

**Conditions of every figure.** One rented Linux virtual machine with AVX2 and FMA. It reports itself as an
Intel Xeon at 2.20 GHz, but its core does not time like that model, so the processor is not named. Other
programs ran on it at full load the whole time. gcc 13.3.0. FFHT at its last version (March 2019; the
commit is under Sources), built by its own Makefile, with the plan of passes it ships. One thread, kept on one
processor. Times are wall-clock nanoseconds per point for one transform (the time of one transform divided
by the number of points): the best of the repeats, and in brackets the median. A repeat is a loop of 0.2 s
or more, and the programs take turns inside one process. 11 October 2026.

### FFHT, and FFHT with the step changed

"More time" is set against FFHT built again, from the best times. The **band** is how much the same
comparison moves when nothing has changed: two builds of identical code, and the same pair timed twice 40
to 60 minutes apart (that was done for the divided form only). It is about 2 points per size up to 2^19
points and about 5 points from 2^20. "n.d." means no measured difference.

**Single precision**

| k (2^k points) | array | repeats | FFHT | FFHT built again | 20 operations, exact | 20 operations, output divided | 19 operations fused, exact | more time than "built again": 20 exact / divided / 19 fused | band |
|---|---|---|---|---|---|---|---|---|---|
| 3 | 32 B | 15 | 1.960 (2.017) | 1.957 (2.016) | 1.948 (2.025) | 1.960 (2.015) | 1.961 (2.057) | n.d.: the step is not used, all five run the same instructions | ±2 points |
| 6 | 256 B | 15 | 0.504 (0.512) | 0.505 (0.515) | 0.624 (0.635) | 0.586 (0.598) | 0.558 (0.580) | +23.4 % / +15.9 % / +10.3 % ‡ | ±2 points |
| 9 | 2 KiB | 9 | 0.491 (0.502) | 0.490 (0.500) | 0.576 (0.588) | 0.532 (0.550) | 0.522 (0.535) | +17.6 % / +8.6 % / +6.7 % | ±2 points |
| 12 | 16 KiB | 15 | 0.574 (0.583) | 0.572 (0.581) | 0.669 (0.680) | 0.625 (0.645) | 0.598 (0.607) | +16.9 % / +9.2 % / +4.5 % | ±2 points |
| 15 | 128 KiB | 15 | 0.740 (0.759) | 0.743 (0.769) | 0.843 (0.857) | 0.797 (0.823) | 0.766 (0.789) | +13.5 % / +7.4 % / +3.2 % | ±2 points |
| 18 | 1 MiB | 9 | 0.898 (0.937) | 0.892 (0.899) | 1.024 (1.057) | 0.955 (0.963) | 0.926 (0.960) | +14.8 % / +7.1 % / +3.8 % | ±2 points |
| 21 | 8 MiB | 9 | 1.244 (1.297) | 1.240 (1.275) | 1.378 (1.408) | 1.343 (1.370) | 1.313 (1.334) | † | ±5 points |
| 24 | 64 MiB | 9 | 1.929 (1.973) | 1.926 (1.967) | 2.049 (2.068) | 1.967 (2.008) | 1.938 (2.024) | † | ±5 points |
| 26 (largest) | 256 MiB | 15 | 2.310 (2.354) | 2.302 (2.343) | 2.417 (2.482) | 2.365 (2.403) | 2.326 (2.391) | † | ±5 points |
| 20 to 26, mean of the seven sizes | 4 to 256 MiB | | | | | | | +7 % / +5 % / +3 % (fused: no gain shown, a loss not established) | |

**Double precision**

| k (2^k points) | array | repeats | FFHT | FFHT built again | 20 operations, exact | 20 operations, output divided | 19 operations fused, exact | more time than "built again": 20 exact / divided / 19 fused | band |
|---|---|---|---|---|---|---|---|---|---|
| 3 | 64 B | 15 | 1.639 (1.659) | 1.642 (1.666) | 1.643 (1.658) | 1.644 (1.656) | 1.640 (1.659) | n.d.: the step is not used, all five run the same instructions | ±2 points |
| 6 | 512 B | 15 | 0.730 (0.747) | 0.730 (0.742) | 0.902 (0.926) | 0.820 (0.841) | 0.808 (0.816) | +23.7 % / +12.4 % / +10.8 % | ±2 points |
| 9 | 4 KiB | 15 | 0.849 (0.876) | 0.847 (0.856) | 0.992 (1.007) | 0.900 (0.921) | 0.891 (0.901) | +17.0 % / +6.2 % / +5.2 % | ±2 points |
| 12 | 32 KiB | 15 | 1.028 (1.038) | 1.023 (1.038) | 1.209 (1.228) | 1.126 (1.145) | 1.094 (1.114) | +18.2 % / +10.1 % / +7.0 % | ±2 points |
| 15 | 256 KiB | 15 | 1.331 (1.357) | 1.335 (1.351) | 1.534 (1.574) | 1.436 (1.466) | 1.414 (1.476) | +15.0 % / +7.6 % / +6.0 % | ±2 points |
| 18 | 2 MiB | 15 | 1.771 (1.830) | 1.784 (1.808) | 1.990 (2.013) | 1.894 (1.913) | 1.856 (1.881) | +11.5 % / +6.2 % / +4.0 % | ±2 points |
| 21 | 16 MiB | 15 | 3.095 (3.235) | 3.083 (3.196) | 3.295 (3.465) | 3.160 (3.381) | 3.134 (3.338) | † | ±5 points |
| 24 | 128 MiB | 15 | 4.318 (4.429) | 4.284 (4.413) | 4.440 (4.673) | 4.400 (4.582) | 4.335 (4.495) | † | ±5 points |
| 26 (largest) | 512 MiB | 15 | 4.221 (4.320) | 4.205 (4.389) | 4.415 (4.562) | 4.369 (4.500) | 4.278 (4.447) | † | ±5 points |
| 20 to 26, mean of the seven sizes | 8 to 512 MiB | | | | | | | +6 % / +3 % / +2 % (fused: no gain shown, a loss not established) | |

Notes to both tables.

- **†** From 2^20 points two timings of the same pair differed by up to 5 points, so no percentage is given
  for a single size. The times are in the row; the comparison that holds is the mean of the seven sizes in
  the last row. No form was faster than FFHT at any of these sizes.
- **‡** At 2^6 points in single precision (and 2^5 in double precision, not in the table) a transform is a
  single block of FFHT's first pass, and the benchmark transforms the same array again and again. Each
  transform then waits for the one before, which charges a long chain of operations in full. With separate
  arrays the loss would be smaller; by how much was not measured in FFHT's code. The double-precision row
  k = 6 is one size above that case.
- **Repeats.** 15 in the main run. Nine single-precision sizes were disturbed by other programs in the main
  run and were timed a second time with 9 repeats; the table uses the second timing (k = 9, 18, 21, 24
  here). No sign changed.
- **How often each form was timed.** The form with divided output was timed twice, on different processors
  of the machine, and was slower at all 31 sizes of the second timing. The exact 20-operation form and the
  fused form in double precision were timed once.
- **The step only in the large passes.** With the new step used only in passes whose block of data is
  512 KiB or larger, the changed FFHT could not be told from FFHT: between 2 % less and 4 % more time with
  the output left divided, between 2 % less and 6 % more fused, from 2^17 points (double precision) or 2^18
  (single) to 2^26 (one run, 9 repeats).
- **What "all 129" is counted by.** By the best time of each program, against FFHT built again. `signs.py`
  prints three other countings as well. By the medians against FFHT built again, 127 of the 129 took more
  time and two took less, by under 1 % (single precision: the fused form at 2^13 points and the divided
  form at 2^22). By the best times against FFHT's first build, 127 took more, one the same and one 0.6 %
  less (double precision at 2^20 points: the divided and the fused form). By the medians against the first
  build, all 129 took more. None of these is a gain outside the band.
- **All sizes.** `python3 -B rows.py` prints these rows from the raw outputs, and `python3 -B signs.py` the
  sign of all 129 comparisons. [style-generator/out/main-table.md](style-generator/out/main-table.md) has
  every size from 2^3 to 2^26, with the number of instructions; in it `gT` is FFHT built again, `g20x` the
  exact 20-operation form, `g20s` the form with the output left divided and `g19f` the fused form.

### The pair in my own vector code (single precision only)

The 19-operation fused step against the textbook step in the same program, timed ten times on two
processors of the machine: about 4 % more time at 2^12 and 2^15 points (2 to 8 % over the ten runs), and
the same time within 2 % at 2^26 points. The sources are in [style-fused/](style-fused/) and the ten runs
in [fused-retiming/](fused-retiming/).

### My earlier plain C

Two full runs, the best of 9 repeats, gcc 13.3.0 with `-O3 -march=native`. Times are from the first run, in
ns per point, best (median). Each ratio is given for the first and the second run. The largest size here is
2^27.

**Single precision**

| k | FFHT | plain C, textbook step | plain C, new step, exact | plain C, new step, output divided | textbook C ÷ FFHT | new exact ÷ textbook | new divided ÷ textbook |
|---|---|---|---|---|---|---|---|
| 3 | 1.937 (1.949) | 3.048 (3.137) | 3.342 (3.393) | 3.316 (3.383) | 1.57, 1.58 | 1.10, 1.09 | 1.09, 1.08 |
| 6 | 0.505 (0.508) | 1.173 (1.211) | 1.435 (1.456) | 1.415 (1.425) | 2.32, 2.37 | 1.22, 1.21 | 1.21, 1.19 |
| 9 | 0.484 (0.492) | 0.877 (0.916) | 1.320 (1.327) | 1.282 (1.295) | 1.81, 1.83 | 1.51, 1.49 | 1.46, 1.45 |
| 12 | 0.568 (0.596) | 0.918 (0.922) | 1.370 (1.375) | 1.337 (1.340) | 1.62, 1.61 | 1.49, 1.49 | 1.46, 1.45 |
| 15 | 0.738 (0.747) | 1.065 (1.072) | 1.509 (1.519) | 1.485 (1.490) | 1.44, 1.44 | 1.42, 1.43 | 1.39, 1.40 |
| 18 | 0.897 (0.911) | 1.256 (1.280) | 1.735 (1.755) | 1.682 (1.696) | 1.40, 1.40 | 1.38, 1.39 | 1.34, 1.34 |
| 21 | 1.229 (1.293) | 1.686 (1.719) | 2.156 (2.183) | 2.137 (2.162) | 1.37, 1.33 | 1.28, 1.26 | 1.27, 1.24 |
| 24 | 1.915 (1.955) | 2.732 (2.789) | 3.102 (3.130) | 3.079 (3.111) | 1.43, 1.48 | 1.14, 1.13 | 1.13, 1.11 |
| 27 (largest) | 2.316 (2.363) | 3.172 (3.222) | 3.561 (3.639) | 3.496 (3.595) | 1.37, 1.37 | 1.12, 1.11 | 1.10, 1.09 |

**Double precision**

| k | FFHT | plain C, textbook step | plain C, new step, exact | plain C, new step, output divided | textbook C ÷ FFHT | new exact ÷ textbook | new divided ÷ textbook |
|---|---|---|---|---|---|---|---|
| 3 | 1.645 (1.665) | 3.324 (3.361) | 3.333 (3.410) | 3.212 (3.275) | 2.02, 2.02 | 1.00, 1.00 (n.d.) | 0.97, 0.96 |
| 6 | 0.732 (0.737) | 2.380 (2.398) | 1.722 (1.732) | 1.618 (1.631) | 3.25, 3.24 | 0.72, 0.73 | 0.68, 0.68 |
| 9 | 0.844 (0.857) | 2.314 (2.335) | 1.457 (1.472) | 1.405 (1.413) | 2.74, 2.72 | 0.63, 0.64 | 0.61, 0.61 |
| 12 | 1.021 (1.036) | 2.480 (2.501) | 1.663 (1.683) | 1.574 (1.597) | 2.43, 2.43 | 0.67, 0.67 | 0.63, 0.63 |
| 15 | 1.336 (1.377) | 2.772 (2.847) | 1.939 (1.984) | 1.871 (1.895) | 2.08, 2.10 | 0.70, 0.70 | 0.68, 0.67 |
| 18 | 1.780 (1.808) | 3.361 (3.380) | 2.532 (2.571) | 2.460 (2.477) | 1.89, 1.90 | 0.75, 0.75 | 0.73, 0.73 |
| 21 | 2.953 (2.991) | 4.498 (4.616) | 3.753 (3.894) | 3.615 (3.835) | 1.52, 1.52 | 0.83, 0.84 | 0.80, 0.81 |
| 24 | 4.248 (4.364) | 5.936 (6.056) | 5.487 (5.718) | 5.400 (5.496) | 1.40, 1.38 | 0.92, 0.91 | 0.91, 0.91 |
| 27 (largest) | 4.810 (4.851) | 6.665 (6.736) | 6.119 (6.196) | 6.089 (6.135) | 1.39, 1.38 | 0.92, 0.93 | 0.91, 0.91 |

**These double-precision rows mislead on their own.** They are all multiples of 3, and those are the only
sizes where the new step wins in my plain C. At the sizes between them it loses: at 2^10 and 2^11 points
the exact form takes 1.08 and 1.10 times the textbook's time, and over all other sizes from 2^4 to 2^26 it
takes 1 to 13 % more. In single precision it takes 2 to 51 % more at every size. And from 2^6 to 2^18
points the win is larger than 20 operations in place of 24 can give, which is 17 % at most. So it comes
from how gcc treats one pass of my code, not from the operation count. The cause was not found. The earlier
figure of 5 to 39 % less time, in [the wht56 README](../../README.md) under "Earlier runs", was measured
only in double precision at 2^9, 2^12, 2^15, 2^18 and 2^21 points. It is not a gain of the step.

## 4. Why the result is what it is

**The saving is real but small, and it is paid for with waiting.** In the loop of an ordinary 8-register
pass FFHT has 50 instructions: 8 loads, 8 stores, 24 additions and subtractions, and 10 for addresses and
the loop. The new step brings that to 46 (19 additions and subtractions and 1 multiplication), or to 45 in
the fused form (7 additions and subtractions and 12 multiply-adds). The loads, the stores and the loop do
not shrink. Over a whole transform that is 2 to 8 % fewer vector instructions with the output left divided
and up to 10 % fewer in the fused form. The exact 20-operation form has between 3 % more and 6 % fewer,
because it needs 8 extra multiplications in one pass, and in a test of one pass alone those cost about 7.7
cycles per block, more than their number explains (cause not found). That is why the exact 20-operation
form is the slowest. Registers are not the problem: the new step uses 13 of the 16, nothing is copied and
nothing is parked in memory. The likely problem is the order of the operations. In the textbook block no
result is more than 3 operations away from the loaded numbers, so the processor can work on many of them
side by side. In the new step 7 operations build one value and the rest wait for it (6 in the fused form).
In the one-pass test (one run, 15 repeats, 16 KiB of single-precision and 2 KiB of double-precision data),
a 20-operation block with a chain of 3 took 15 to 16 % less time than FFHT's block, the real block with its
chain of 7 took 23 to 24 % more, and four operations fewer at an equal chain were worth 4 to 5 % of a pass.
So the saving is there and the chain outweighs it. What happens inside the processor was not measured, so
this is an explanation that fits, not a finding. Fused multiply-add opens no second lane on this machine:
an addition, a multiplication and a multiply-add each took about 4 cycles, and about two of each can start
per cycle.

**Where memory traffic dominates.** Both versions load and store every number once per pass, so that part
of the work is identical. Up to 2^19 points the arithmetic sets the time, and there the loss is largest.
From 2^20 points (arrays of 4 MiB in single and 8 MiB in double precision) FFHT's own time per point
climbs, from 1.1 ns at 2^20 to 2.3 ns at 2^26 in single precision. I read that as the cost of moving data
to and from main memory; it was not measured separately. There the arithmetic is a smaller share of the
time and the loss shrinks to a few per cent. The machine reports caches of 32 KiB, 256 KiB and 55 MiB, but
those were not measured, and FFHT's time per point jumps by 34 % between arrays of 8 and 16 MiB (24 % in
double precision), far below 55 MiB. That is why this page gives bytes and not cache levels.

The instruction counts are those of the agent that wrote the code. The agent that checked them confirmed
the written-out blocks (20, 28 and 19 instructions, 13 registers, no copies, chains of 7, 8 and 6) but
could not recount the compiled loops, because the machine was offline.

## 5. Limits

- **One machine.** A rented virtual machine. Its processor is not identified: it reports one model and
  times like a later one.
- **One compiler**, gcc 13.3.0, and for FFHT only its own flags.
- **Other jobs were running the whole time.** Three search programs at full load in every run, and more
  during the main single-precision run (nine sizes were timed again for that reason). The processor's
  second thread was busy for 4 to 24 % of every size that was kept. That hurts FFHT's block more than the
  new block, so it works in favour of the new step; "not faster" is safe against it.
- **A single thread.**
- **One run** for the exact 20-operation form and for the fused form in double precision. Only the divided
  form and nine single-precision sizes were timed twice.
- **The two agents that checked the main work measured nothing.** The machine went offline first. They
  checked the reports against the raw files and the sources. No version of FFHT with the step changed has
  passed an exactness check that its own author did not write.
- **How it was timed.** One array transformed again and again; inputs of -1, 0 and 1; ordinary 4 KiB memory
  pages; the program printed only the best, the median and the worst repeat.
- **Only the 8-point member was timed** (19 for 24). The larger circuits of the family, which are the ones
  that approach 3/4, were not.
- **Not tried:** another processor (AMD, ARM, AVX-512, an Intel core with one addition unit); another
  compiler or other flags for FFHT; FFHT's SSE code; FFHT tuned again for this machine; the plan with one
  more 8-register pass (built and checked, never timed); the full table for my own vector code; whole
  numbers in FFHT's scheme; several threads; 2 MiB memory pages; small arrays transformed once each;
  rounding error on real-valued data; a search for a circuit with fewer than 24 operations and a chain
  shorter than 7.
  (AMD and AVX-512 were tried on 22 October 2026; see the line at the top.)

So nothing here says that the step is slower in general, or what it would do on another processor. And no
change was offered to FFHT or to any other library: there is no measured gain to offer.

## 6. The files, and how to run it again

Everything in this folder is mine (made by the AI agents under my direction) and under the Apache License
2.0, like the rest of the repository. **No file of FFHT is here.** FFHT is under the MIT License (copyright
2015 Alexandr Andoni, Piotr Indyk, Thijs Laarhoven, Ilya Razenshteyn, Ludwig Schmidt). Two things here are
derived from it. `style-generator/gen.py.patch` is a patch against FFHT's `gen.py`: it holds the few lines
of FFHT's file that a patch needs around each change. And `style-intrinsics/plans.json`, `plans.inc` and
`plans.txt` describe FFHT's plan of passes (which levels of the transform go into which pass at each
size), read from the code that FFHT's generator writes; the plan is FFHT's, the files are mine.

| where | what |
|---|---|
| `rows.py`, `signs.py` | print the tables of section 3 and the sign of the 129 comparisons from the raw outputs; Python only |
| `harness/` | the timing program (`harness.c`, `engine.inc`), FFHT and my plain C beside it (`variants.c`, `ours/`), the check against the definition (`naive.c`), two looks at the processor (`cpufreq.c`, `ports.c`), and the script that runs a timing under a lock on the quietest processor (`locked_run.sh`) |
| `plain-c/` | the raw outputs of the two runs of my plain C beside FFHT, and the exactness check |
| `style-generator/gen.py.patch`, `k8kernel.py` | the change to FFHT's generator: the patch makes it call `k8kernel.py`, which writes the block of 8 registers in one of the forms |
| `style-generator/build_variants.sh`, `harness/`, `run_harness.sh`, `redo.sh`, `lockwait.py`, `tables.py` | write and build each form by FFHT's own Makefile, link them into one timing program, run it, time disturbed sizes again, print the tables |
| `style-generator/kloop/`, `kloop_gen.py`, `kloop_table.py` | the test of one pass alone |
| `style-generator/out/` | the raw outputs: `time-float-run1.txt`, `time-double-run1.txt` and `time-redo-run1.txt` (the tables of section 3), `time-*-where.txt` (the step only in the large passes), `kloop-1.txt` and `lat-1.txt` (one pass alone; what one instruction costs), `check-1-24.txt` (exactness), and the tables written from them |
| `style-intrinsics/` | my own C with intrinsics: sources, the one-pass test (`out/kstep-1.txt`) and the instruction counts. Its trial timings of whole transforms are not here |
| `style-fused/` | the 19-operation fused form in a program of my own: sources and the outputs of the one complete single-precision run |
| `fused-retiming/` | the second timing of that form by another agent: a timer and a checker of its own, and the ten runs |

In the raw outputs the name of the machine was removed, and so was the folder of one program of another
job in the lists of busy programs. The files that recorded the load every ten seconds are not here.

**What can be run without the machine.** With Python 3.9 or later, from this folder:

    python3 -B signs.py          # 129 cells; "best vs gT ... cells <= 0: []" means all 129 took more time
    python3 -B rows.py           # the rows of section 3
    (cd style-generator && python3 -B tables.py final=out/time-float-run1.txt,out/time-double-run1.txt,out/time-redo-run1.txt | cmp - out/tables-final.md)
                                 # the table of every size, written again from the raw outputs: no difference

And the first step of the benchmark, which needs `git`, `patch` and Python only. It writes FFHT's code
again with the changed generator and checks that the textbook setting gives FFHT's own file:

    git clone https://github.com/FALCONN-LIB/FFHT.git
    git -C FFHT checkout fba727a3ff72c862260460631ae1cc8e3e44e861
    cd style-generator
    cp ../FFHT/gen.py gen.py && patch gen.py gen.py.patch
    mkdir -p gen/gT gen/g19f
    FFHT_K8_KERNEL=textbook FFHT_PLAN=../FFHT/hall_of_fame_avx.txt FFHT_OUT=gen/gT python3 -B gen.py
    cmp gen/gT/fht_avx.c ../FFHT/fht_avx.c && echo "the textbook setting writes FFHT's own file"
    FFHT_K8_KERNEL=fma19 FFHT_PLAN=../FFHT/hall_of_fame_avx.txt FFHT_OUT=gen/g19f python3 -B gen.py

These commands were run on a Mac on 11 October 2026, from this folder as it is published: the patch
applied, and the file was FFHT's own, byte for byte.

**The whole benchmark.** It needs a Linux machine with an x86 processor that has AVX2 and FMA, and gcc,
make, git, python3, patch, binutils and tmux. Do not put the word "bench" into a folder name or a command
line there: the run script waits for as long as it sees a process with that word. The commands below are
put together from the scripts and the reports. **They have not been run from a clean machine**, and after
the folder names in the scripts were changed from those of the rented machine to relative ones, the scripts
were not run again: that machine is gone.

    # 1. FFHT at the commit used, built by its own Makefile (about 5 seconds), inside this folder
    git clone https://github.com/FALCONN-LIB/FFHT.git
    git -C FFHT checkout fba727a3ff72c862260460631ae1cc8e3e44e861
    make -C FFHT

    # 2. my plain C beside FFHT (the last tables of section 3): about 17 minutes
    cd harness
    make && build/harness check -k 1 27
    sh run_time.sh ../plain-c/time-new.txt -t both -k 3 27 -r 9
    cd ..

    # 3. FFHT with the step changed (the first tables of section 3)
    cd style-generator
    cp ../FFHT/gen.py gen.py && patch gen.py gen.py.patch    # FFHT's generator with my change
    sh build_variants.sh        # stops unless the textbook setting writes FFHT's own file byte for byte
    (cd harness && make && build/harness check -t both -k 1 24)
    tmux -L ffht-rerun new -d 'sh run_harness.sh new 15 3 26 ffht,gT,g20x,g20s,g19f'
    # results: out/time-float-new.txt and out/time-double-new.txt, each with a .watch file of the load
    python3 -B tables.py new=out/time-float-new.txt,out/time-double-new.txt > out/tables-new.md

    # 4. one pass alone (the test behind section 4): about 3 minutes
    make -C kloop
    python3 -B lockwait.py sh harness/locked_run.sh out/kloop-new.txt kloop/kloop 15

How long: step 3 took 25 minutes for single precision and 11 minutes for double precision on the busy
machine (30 and 2 attempts thrown away because of other programs). On a quiet machine it should be about 10
minutes each. The whole of it, once, is about an hour.

The run scripts keep the discipline by themselves: they wait while another benchmark runs, take a lock
(the folder `/tmp/ffht-timing.LOCK`), keep the program on the quietest processor, write the load and the
busy programs before and after, and time a size again when the processor's second thread was busy for more
than 25 % of it.

**What a second run should add.** First `lscpu` and the test of what one operation costs, so that the
processor is known. Then: every repeat printed (the program printed only the best, the median and the
worst); two full runs ten minutes apart on two processors; separate arrays at 2^6 to 2^10 points; an
exactness check on every vector version that its author did not write. And another kind of processor: one
on which additions and multiply-adds run on different units, an ARM processor, a processor with AVX-512.

## Sources

- FFHT: <https://github.com/FALCONN-LIB/FFHT>, commit `fba727a3ff72c862260460631ae1cc8e3e44e861` (10 March
  2019, its last), MIT License. Its own flags: `gcc -O3 -march=native -std=c99` and warnings.
- Compiler: gcc 13.3.0. My plain C and the timing program: `-O3 -march=native`. My own vector code:
  `-std=gnu11 -O3 -march=native -fno-tree-reassoc -Wa,-mbranches-within-32B-boundaries`.
- The machine: a rented Linux virtual machine with 8 processor threads; it reports an Intel Xeon at
  2.20 GHz with AVX2 and FMA.
- The circuits: `tools/circuits/programs/h8_half_20ops.txt` (20 operations) and `h8_19gates.txt` (19).
- Every figure in the tables of section 3 was read again from the raw outputs of this folder by `rows.py`
  and `signs.py`.
- Date of all runs: 11 October 2026.
