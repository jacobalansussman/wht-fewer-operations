# wht56: the circuits of this repository as working programs

This folder computes the Walsh-Hadamard transform of real data with the circuits of `tools/circuits/`: in
pure Python, in numpy and in C. It is here so that the operation counts can be seen on a running program,
and so that the question "is it faster?" has measured numbers. The name is the rate of the main circuit, 5/6.

**Words.** N = 2^k is the number of points. H is the N × N matrix with the entry +1 in row j, column i when
j and i, written in binary, have an even number of 1-bits in common, and -1 otherwise. The transform of a
list x is H x. The textbook program uses N log2 N additions and subtractions. *Count (O)* charges one for
every addition, every subtraction and every multiplication by a constant. *Count (G)* charges one for any
a·u + b·v, so a multiplication by a constant is free. The circuits, the credit to earlier work, and what is
checked by Lean and what is not, are in [notes/explicit-circuits.md](../../../../notes/explicit-circuits.md).

**How to run it.** From the folder that holds `wht56`, with Python 3.9 or later:

    python3 -B -m wht56 --selftest       the tests: 16 to 20 seconds on my Mac, 31 to 39 on the Linux machine
    python3 -B -m wht56 --count 9        the operations really performed at 2^9 points, by a counter
    python3 -B -m wht56 --table 14       the counts table up to 2^14 points
    python3 -B -m wht56 --bench          timings of the Python and numpy versions
    python3 -B -m wht56 --gen c --size 512 > wht512.c      straight-line code (also: --gen python)
    sh wht56/c/build_and_bench.sh        compile the C version three ways, check it, time it

    from wht56 import wht, Tally         # pure Python, exact on integers and fractions
    t = Tally(); y = wht(list(range(512)), tally=t); print(t.O)      # 4352
    from wht56.fast import fwht          # numpy: float64, complex128, int64
    y = fwht(a, norm='exact')            # or 'ortho' for H x / √N, or 'raw'

**The files.** `reference.py` is the pure-Python version, standard library only: the textbook; the
20-operation 8-point circuit in layers; any N = 2^k by the cheapest mix of 8-point, 4-point and 2-point
circuits; the family with (3/4) N log2 N + N/4 operations in count (G). `fast.py` is the numpy version.
`c/` is the C version for doubles, with a textbook to compare with, one address bit at a time (radix 2) and
three at a time (radix 8); the C functions need a length that is a power of two, and for any other length
they return at once and leave the array untouched. `codegen.py` writes straight-line Python and C for a given size, and it writes
the 8-point kernels of the numpy and C versions; no circuit is typed by hand. `circuits/` holds copies, byte
for byte, of six files of `tools/circuits/programs/`; the README of that folder says which one of their
headers is older than the rest of the repository. `tests/` has the tests and `results/` what the
programs printed in the recorded runs.

**The counts.** Every number below except the last column was counted on the running pure-Python program by
the tests, not only computed from a formula. The last column is N log2 N + N. "Raw" is what the 8-point
circuit leaves: H x divided by 2^m after m layers.

| points | textbook | (G) small circuits in layers | (G) family | (O) exact H x, 8-point circuit in layers | (O) raw | (O) H x / √N | textbook for H x / √N |
|---|---|---|---|---|---|---|---|
| 8 | 24 | 19 | 20 | 28 | 20 | 28 | 32 |
| 16 | 64 | 54 | 52 | 72 | 56 | 64 | 80 |
| 64 | 384 | 304 | 304 | 384 | 320 | 384 | 448 |
| 512 | 4,608 | 3,648 | 3,584 | 4,352 | 3,840 | 4,352 | 5,120 |
| 1,024 | 10,240 | 8,320 | 7,936 | 9,728 | 8,704 | 9,728 | 11,264 |
| 4,096 | 49,152 | 38,912 | 37,888 | 45,056 | 40,960 | 45,056 | 53,248 |
| 32,768 | 491,520 | 389,120 | 376,832 | 442,368 | 409,600 | 442,368 | 524,288 |

For N a power of 8 the exact transform costs 20 j 8^(j-1) + 8^j = (5/6) N log2 N + N in count (O). The
last N are the multiplications that remove the factor 1/2^m. For H x itself that is below the textbook from
512 points on. When the transform wanted is H x / √N, the textbook needs N multiplications too, so the
saving is a sixth of the additions and subtractions at every power of 8. (The 64 at 16 points is two
layers of the 4-point circuit with one halving each, which give H x / 4 with no multiplication at the end.)
At 8 and 16 points the layers cost more than the textbook (28 against 24, 72 against 64), and `wht()`
uses the textbook there. The column for H x / √N is what this folder computes. The note has lower numbers
for the scaled transform at even k (60, 352, 9,216 and 44,032 at 16, 64, 1,024 and 4,096 points); they
come from the family in count (O), and that program is not in this folder.

Integers cannot be halved, so on integer arrays the numpy version uses the 19-operation circuit, which
doubles instead: 31 operations for 8 points in count (O), more than the textbook's 24. Integer data gain in
count (G) only. The pure-Python `wht` on integers halves in exact fractions by default and multiplies back,
which is exact and slow; `wht(x, count='G')` stays in the integers.

**At the edges of the numbers.** "Exact on integers" holds for Python `int` and `Fraction`. numpy integers
given to the pure-Python programs are not recognised as integers. The numpy version computes integer arrays
in int64: sums that do not fit wrap around without a message, and uint64 values of 2^63 or more come out
wrong. With an infinity in the input the textbook gives an infinity in every output, and the new circuits
give NaN in some outputs, because they subtract two values that both contain that input. Close to the
largest double the 19-operation circuit and the family overflow where the textbook does not, and close to
the smallest the halving of the 20-operation circuit loses the value.

**The timings.** There are two sets, and the second is the one that counts.

*Against a tuned library.* On 11 October 2026 the 8-point step was written into the generated code of FFHT,
a tuned open-source library for this transform, in place of its block of 24 additions and subtractions. On
the one machine that was timed it did not make FFHT faster at any size from 2^6 to 2^26 points in single
precision or from 2^5 to 2^26 points in double precision: set against a second build of FFHT's unchanged
code, all 129 combinations of size and form took more time. [results/ffht/README.md](results/ffht/README.md)
has the tables by size, the conditions, the likely reason, the sources and how to run it again.

*My own plain C.* The rest of this section is about the C programs of this folder, timed against each
other. They are ordinary C that the compiler turns into machine instructions by itself, and on the Linux
machine FFHT took less time than each of them at every size (my fastest took 1.2 to 4.1 times as long). So
these numbers say how one compiler treated two programs of mine. They are not a measure of the step.

C, 64-bit floating-point numbers ("doubles"), in place, one thread, on two machines. The
main source is [results/bench-by-size/bench.md](results/bench-by-size/bench.md): 11 sizes from 8 to
16,777,216 points, two builds on each machine, everything run twice, with the method, the raw outputs and
the programs beside it. Two programs are compared. "New" is the exact transform with the 20-operation
kernel, its N multiplications included, done while the last pass stores its results. "Textbook" is the
textbook written the same way, three address bits per pass (radix 8). They differ in the 8-point kernel
only. The table gives the time of the new program divided by the time of the textbook, best loop against
best loop. Below 1 the new program took less time: 0.95 means 5% less. The second column is the same ratio
for the number of operations in count (O), as the C program does them.

| points | operations | Mac, scalar | Mac, vectorised | Linux, scalar | Linux, vectorised |
|---|---|---|---|---|---|
| 8 | 1.167 | 1.045 | 1.244 | 1.085 | 0.989 |
| 64 | 1.000 | 1.027 | 1.100 | 1.246 | 0.728 |
| 512 | 0.944 | 1.013 | 0.976 | 1.263 | 0.638 |
| 1,024 | 0.950 | 1.001 | 1.017 | 1.187 | 1.075 |
| 4,096 | 0.917 | 0.992 | 0.973 | 1.147 | 0.676 |
| 32,768 | 0.900 | 0.988 | 0.953 | 1.241 | 0.705 |
| 65,536 | 0.906 | 0.984 | 0.984 | 1.190 | 1.082 |
| 262,144 | 0.889 | 0.967 | 0.973 | 1.124 | 0.757 |
| 1,048,576 | 0.900 | 1.003 | 0.963 | 1.132 | 1.047 |
| 2,097,152 | 0.881 | 0.990 | 0.951 | 1.157 | 0.867 |
| 16,777,216 | 0.875 | 0.995 | 0.963 | 1.149 | 0.921 |

The conditions. Mac: a Mac mini with an Apple M4 processor, Apple clang 21.0.0; "scalar" is `-O2` with the
compiler's vectorisers switched off, "vectorised" is `-O3 -mcpu=native`. Linux: a rented virtual machine
that reports itself as an Intel Xeon at 2.20 GHz, gcc 13.3.0; "scalar" is `-O2 -fno-tree-vectorize`,
"vectorised" is `-O3 -march=native`, which allows vector instructions on four doubles at a time. Each machine was running
three other jobs that each kept one processor core busy. The runs were made on 11 October 2026. This is the
second of two runs. In the first run no ratio differed from these by more than 0.11, and on Linux,
vectorised, none by more than 0.02; `bench.md` has both runs.

What the numbers show.

- **In no build did the time follow the operation count, and none of these numbers isolates the 8-point
  step:** each compares what one compiler made of two programs.
- Mac, scalar: no difference from 64 points up, within 4% either way. At 8 points the new program took 5 to
  12% more time.
- Mac, vectorised: 2 to 5% less time from 4,096 points up, and 2 to 3% less at 512 points. More time at 8,
  64 and 1,024 points: 24 to 30%, 10% and 2% more.
- Linux, scalar: more time at every size, 12 to 26% more from 64 points up. A control with `-O3` in place of
  `-O2` gave the same.
- Linux, vectorised: 8 to 36% less time at the sizes 8^j from 64 points up, and 5 to 8% more at 1,024, 65,536
  and 1,048,576 points. This is not a gain of the step. A control that timed one pass alone shows where it
  comes from. In the pass over neighbouring numbers, gcc's vector code for the textbook kernel took twice
  the time of its scalar code for the same pass. This program has that pass only at the sizes 8^j. At every
  other distance between the 8 numbers the new pass took 3 to 18% more time than the textbook pass. So it
  comes from what the compiler did with one pass of the textbook, not from the smaller count. The later
  runs beside FFHT say the same over every size from 2^3 to 2^27 points: in double precision the new step
  took less time than the textbook step only at the sizes 2^6, 2^9, 2^12 and so on (7 to 37 % less with
  exact output) and 1 to 13 % more at every other size from 2^4 to 2^26; in single precision it took 2 to
  51 % more at every size. At 2^6 to 2^18 points the gain is larger than replacing 24 operations by 20 can
  give, which is 17 % at most. The cause has not been found.
- Without the last multiplications, which leaves H x divided by a power of two: on the Mac the new program
  took 0 to 8% less time than the textbook in scalar code, and 2 to 6% less from 512 points up in vectorised
  code. On Linux in scalar code it still took 4 to 16% more.
- Against the textbook with one address bit per pass (radix 2), the new exact program took 40 to 59% of the
  time on the Mac and 43 to 86% on Linux, from 64 points up. That is mostly not these circuits: the radix-8
  textbook does about as well. Three layers per pass load and store each number once where radix 2 does it
  three times.
- How far to trust it. Differences of 3% or less on the Mac are inside the noise. The Linux signs repeat in
  both runs. It is two machines, two compilers, one program layout and doubles only. Nothing here says what
  another machine or another compiler would do. What the step does inside a tuned library is on the page
  named at the top of this section.

The same gap between counting and timing is in the 1994 paper of Coppersmith, Feig and Linzer: its count
predicts a gain of 12.5%, and the authors measured 5.6% to 7.4% on their machine (pages 969 and 970).

**Earlier runs.** `results/` also holds seven earlier runs on the Linux machine and six on the Mac, made the
same morning with `c/build_and_bench.sh`, when both machines were more heavily loaded
(`results/README.txt` says which file is which). They timed 2^9, 2^12, 2^15, 2^18 and 2^21 points only. All
five sizes are powers of 8. On the Linux machine with vector instructions the new program took 5 to 39% less
time in every one of those runs. That is not a gain of the step: the runs by size above, and the runs beside
FFHT, show that it holds in double precision at the powers of 8 only, that the new step took more time at
every other size and at every size in single precision, and that it comes from how the compiler treated one
pass of the textbook. In scalar code on the Linux machine the earlier runs disagreed with each other while
the machine was busy, and the quietest of them showed the new program 19 to 29% slower, as above. On the Mac the earlier
runs showed no steady difference. In numpy the new kernel was not faster in any steady way: over three runs
on each machine it was between 10% slower and 8% faster than the radix-8 textbook up to 2^18 points. In pure
Python the new programs were slower than the textbook in most runs.

What gcc writes for the main loop of each kernel on the Linux machine with `-march=native` was counted
by a small program (`results/asm/`): 41 instructions for the textbook kernel, 24 of them additions and
subtractions; 35 for the new kernel, with 19 additions and subtractions and one multiplication; 43 for the
new kernel with the last multiplications. So the compiler writes what the circuits say. Why the new kernel
is slower in scalar code on that machine was not found. One pass has 8 loads and 8 stores whichever kernel
is used, and the operations of the new kernel depend on each other in a longer chain, 7 steps deep against
3. In these programs that was not tested. In FFHT's code a test of one pass alone points the same way (a
20-operation block with a chain of 3 took less time than FFHT's block, and the real block with its chain of
7 took more); it is an explanation that fits, not a finding.

**What this is not.**

- It is not a faster program. Inside the tuned library FFHT the step was not faster at any size, on the
  one machine that was timed. The plain C timings are two machines, one compiler on each, one morning, with
  other jobs running.
- It is not a proof. The tests compare every program with the definition of the transform up to 1,024
  points and with the textbook program up to 32,768 points, on integers exactly and on floats and complex
  numbers to rounding. Nothing in this folder is checked by Lean. The Lean statements of this repository
  are about numbers of operations: for N a power of 8 in `lean/Work/SmallWHT/`, and, with each multiply-add
  line counted as one, for every N = 2^k in `lean/Work/WHT34/`, both under `lean/` at the top.
- It is not a tuned library: one thread, no vector instructions written by hand, C for doubles only.
- It is a better constant, not a better exponent. Every count here is a fixed fraction of N log2 N.

The AI agents (Anthropic's Claude) that I directed wrote these programs and ran them on 11 October 2026. A
second agent reviewed the folder the same morning; the three latest of the earlier runs, the paragraph on
the edges of the numbers and the check of the length in the C functions come from that review. A third
wrote and ran the benchmark by size, and others the timings beside FFHT. The programs have not had a line-by-line human review.

**Licence.** Apache-2.0, like the rest of this repository: [LICENSE](../../../../LICENSE) and
[NOTICE](../../../../NOTICE) at its top. `LICENSE-NOTE.txt` in this folder says the same in a few lines.
