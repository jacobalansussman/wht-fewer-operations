# The Walsh-Hadamard transform with fewer operations

**In one paragraph.** This repository holds small *circuits* (fixed lists of operations) for the
Walsh-Hadamard transform that need fewer operations than the textbook method, and it reports where that
helps and where it does not. *Gained on paper:* when every addition, subtraction and multiplication by a
constant counts as one, the exact transform on N = 8^j points takes at most (5/6) N log2 N + N operations,
against the textbook's N log2 N and the 23/24 that is the best I found in print (Alman and Rao, 2023); this
count is proved in Lean. When a doubling is free, as it is for the adders of a chip, the 8-point transform
takes 19 operations against the textbook's 24 and the 22 in print, and a family of circuits takes
(3/4) N log2 N + N/4 against the 7/8 in print (Coppersmith, Feig and Linzer, 1994); these are replayed
exactly by programs and are not in Lean. *Not gained on paper:* it is a better constant, not a better
exponent; with every operation charged the gain starts only at 512 points (8 points cost 28 against 24, and
64 points cost the same as the textbook); the two results do not combine (the 3/4 family becomes 7/8 when
doublings are charged); and nothing here is known to be the best possible. *Gained in measurement:* as an
FPGA design, built as one block of adders with no registers inside, the 8-point circuit takes 19 % to
21.5 % fewer logic cells than the textbook design on a Lattice iCE40 chip, and the family 17.5 % to 23.1 %
fewer from 16 to 256 points by the same tools' counts; on a board, the circuit gave the same outputs as the
textbook circuit on 597,750,000 test inputs. *The price, also measured:* the circuits are twice as deep, so
the highest clock is lower (about 72 against 97 MHz at 8 points, by the tools' estimates); they are larger
than the textbook design once registers are added for speed; at 8 points the 22-adder step of Alman and Rao
is smaller on that chip; and in software, put into the tuned FFHT library in place of its own step, the new
step did not make it faster at any size on the one machine timed (it took 1 % to 24 % more time up to 2^19
points). So this is a result about operation counts, with a measured saving in chip area in one kind of
design, and not a faster program. The circuits were found by AI agents (Anthropic's Claude) working under my
direction; no person has yet read the Lean files or checked the proofs line by line. The sections below
give each of these statements with its conditions.

The Walsh-Hadamard transform turns N numbers into N sums of those numbers, each with its own pattern of
plus and minus signs. The textbook program computes it with N log2 N additions and subtractions. This
repository has a *circuit*, which is a fixed list of operations, that computes the same transform on
N = 8^j points (8, 64, 512, 4,096 and so on; N points means a list of N numbers) with at most
(5/6) N log2 N + N operations, where every addition, every subtraction and every multiplication by a
constant counts as one. That count is proved in Lean, a program that checks proofs. I say *exact* for the
outputs themselves, as against all outputs multiplied by one common factor.

| points | textbook, N log2 N | Alman and Rao (2023), their exact count | this repository |
|---|---|---|---|
| 8 | 24 | 30 | 28 |
| 64 | 384 | 431 | 384 |
| 512 | 4,608 | 4,927 | **4,352** |
| 4,096 | 49,152 | 51,199 | **45,056** |

**It is a better constant, not a better exponent.** The number in front of N log2 N goes from 1 to 5/6 and
stays there however large N is. The best in print is 23/24, by Alman and Rao. A better exponent would be a
count that falls below every fixed fraction of N log2 N as N grows, such as N (log2 N)^0.999. This is not
that.

**At 8 points alone it is not a gain.** The exact 8-point transform costs 28 operations here, against the
textbook's 24. The reason is in how the circuit works. It computes the eight outputs *halved*, in 20
operations where the textbook needs 24. Putting the factor right costs one multiplication for each output.
At 8 points that is 8 more, so 28. On N = 8^j points the circuit is used in j layers (one layer runs it once
on every group of 8 numbers; step 7 of docs/UNDERSTAND.md), and the factor is put right once, at the very
end. Each layer saves N/2 operations and the end costs N. So at 64 points (j = 2) the count equals the
textbook's, and from 512 points (j = 3) on it is below.

I directed this work. The circuits were found by computer searches that AI agents (Anthropic's Claude)
wrote and ran. The same agents wrote the programs, the Lean proof and these pages. No person has yet read
the Lean files or the programs line by line. The builds, the checks, the timings and the hardware
measurements reported on these pages were run by the agents, at my direction, on a Mac mini of mine and on
a Linux machine that I rented.

To understand the result step by step, read [docs/UNDERSTAND.md](docs/UNDERSTAND.md): ten short steps, each
with a check to do by hand.

## The 8-point circuit

```
g1  = x0 + x7
g2  = x1 + x6
g3  = x2 - x5
g4  = x3 - x4
g5  = g1 - g2
g6  = g3 + g4
g7  = g5 - g6        the centre
m8  = 1/2*g7         the one multiplication
g9  = m8 - x7
g10 = m8 - x5
g11 = g9 + x6
g12 = g10 - x4
g13 = g11 + g4       half of output 7
g14 = g10 + x3       half of output 3
g15 = g5 - g14       half of output 5
g16 = g11 + g3       half of output 1
g17 = g12 + g2       half of output 6
g18 = g9 + x1        half of output 2
g19 = g18 + g6       half of output 4
g20 = g1 - g12       half of output 0
```

The inputs are x0 to x7. The eight marked lines are the eight outputs of the 8-point transform, each divided
by 2: output j is the sum of all the inputs, with a minus sign on x_c when j and c, written in binary, share
an odd number of 1-bits. For output 3 (011) and input 5 (101) there is one shared 1-bit, so x5 has a minus
sign there. That is 19 additions or subtractions and one multiplication. The file is
`tools/circuits/programs/h8_half_20ops.txt`.

## Check it yourself

Run these from the top folder, in a Unix shell (Linux or macOS; nothing here was tried on Windows). The
first five need Python 3.9 or later, called as `python3`, and nothing else, though the fourth also uses numpy
and a C compiler when they are there. The sixth needs a C compiler, called as `cc`; put `CC=gcc` in front of
the command to use another. They were run with Python 3.9.6 and 3.13.16, numpy 2.0.2 and 2.1.3, Apple
clang 21 and gcc 13.3.

| command | what it does | time | the last line it prints |
|---|---|---|---|
| `python3 docs/walkthrough.py all` | the numbers and the check of each of the ten steps | 1 second | `OK: all ten steps, every check passed.  A Python check, not a proof.` |
| `python3 -B tools/circuits/run.py` | reads every circuit from its text file, checks it against the definition of the transform in exact arithmetic up to 4,096 points, prints the tables, and writes the Lean data file again and compares it | about a minute, 700 MB of memory | `OK: 4 named circuits and the 20-line program replayed; every size up to 4096 points regenerated and replayed; 41 program files and the Lean data file reproduced byte for byte.  A Python check, not a proof.` |
| `python3 -B tools/circuits/multiply_add_check.py` | checks that no line of any circuit file has a constant on both of its terms (this is what makes the comparison with the 1994 paper fair; see below) | 1 second | `OK: 63 circuit files, 23715 lines; ...` |
| `(cd tools/circuits/fast && python3 -B -m wht56 --selftest)` | 30 tests of the circuits as working programs in Python, numpy and C | under a minute | `OK`; `OK (skipped=5)` without numpy; `OK (skipped=3)` without a C compiler |
| `python3 -B tools/circuits/ga_count.py` | the computation on the count of Grigoryan and Agaian (see "Credit, and what is in print") | 1 second | `OK: the recursion gives N log2 N at every size from 2 to 16384 points; ...` |
| `sh tools/circuits/fast/wht56/c/build_and_bench.sh` | compiles the C version three ways, checks the four C transforms against each other, and times them | under a minute | `CHECK OK: the four transforms agree at every size above` |
| `sh lean/check.sh` | builds the Lean proof and compares the statement with what was proved | 15 minutes | `RESULT: PASS` |

The second command replays every size up to 4,096 points. `python3 -B tools/circuits/run.py --kmax 14`
replays the two largest sizes of its tables as well, up to 16,384 points; that takes 9 minutes and 3 GB of
memory, and the last line then says `16384`.

The Lean check needs more than the others: Linux with `git`, `curl` and `elan` (the program that installs
Lean), an internet connection and about 12 GB of free disk. Its last step held 15.3 GB of memory in one
process on the machine where it was run, which has 50 GB; a smaller machine was not tried.
[VERIFY.md](VERIFY.md) has each command, what it prints and what was run. The Lean build was not run on a
Mac.

The timings and the hardware figures of the two sections further down have their own pages, each with
commands that need Python only and with what was run:
[the timings](tools/circuits/fast/wht56/results/ffht/README.md), section 6, and
[the hardware](tools/circuits/fpga/README.md), section 8.

## What is proved, and what is not

**Proved in Lean.** One statement, in two forms. The theorem
`OAI.ExactFourier.WHT8Half.hadamard_pow8_circuit` says: for every j there is a circuit on 8^j inputs that
computes the exact Walsh-Hadamard transform and has at most 20·j·8^(j-1) + 8^j gates. That number is
(5/6) N log2 N + N. A *gate* is one addition, one subtraction or one multiplication by a constant, in the
circuit model of OpenAI's repository openai/math. The theorem `hadamard_pow8_circuit_real` states the same
with the bound written as (5/6) N log2 N + N. The statement alone, without proof, is the 93-line file
`lean/Work/SmallWHT/ChallengeWHT8.lean`.

**Replayed exactly by programs, not in Lean.**

- The gate lists themselves above 8 points. Lean proves that a circuit of that size exists; it writes out
  the 20 gates for 8 points and no list for larger sizes. The lists at 64, 512 and 4,096 points are text
  files or are generated, and `run.py` checks each one on every input that is 1 in one place and 0
  elsewhere, in exact arithmetic. That settles every input, because each line only adds, subtracts or
  multiplies by a constant.
- Sizes that are not powers of 8. With a textbook layer for each binary digit left over, the count is below
  the textbook at every power of two from 512 on: for example 9,728 against 10,240 at 1,024 points.
  Replayed up to 16,384 points (`run.py --kmax 14`, above). Beyond that it rests on a short argument
  (Corollary 2 of [the paper](paper/explicit-wht-circuits.pdf)), which the agents wrote and no person has
  checked.
- Everything in the second count, below.

**Limits of the Lean check.** The build was run from nothing once, on one rented Linux machine, on
11 October 2026. No person has yet read the Lean files, including the definition of the transform that the
statement uses. Two controls were run: a copy with one gate changed was refused by Lean, and a copy of the
statement with 19 in place of 20 was refused by the comparison script. Lean's official comparison tool was
not run on this folder.

**Not claimed.**

- That 5/6 is the best possible. The only lower bound proved here is 2N - 1 operations, far below these
  counts (Proposition 6 of [the paper](paper/explicit-wht-circuits.pdf); the agents wrote its proof, and no
  person has read it).
- That the result is new. I searched; the section "Credit, and what is in print" says how far.
- Any count for the Fourier transform. Alman and Rao's paper turns a count for this transform into one for
  the Fourier transform. My count has not been put through that.

## A second way of counting: 19 operations at 8 points, and the rate 3/4

Some machines multiply and add in one instruction. Count one line a·u + b·v, with constants a and b, as one
operation, so that multiplying by a constant is free. I call this count (G), and the strict count above
count (O). The letters are only labels; O is the count of the circuit model of OpenAI's repository. In
count (G):

| | textbook | in print: Coppersmith, Feig and Linzer (1994), by their formulas | here |
|---|---|---|---|
| 8 points | 24 | 22 | **19** |
| 16 points | 64 | 56 | **52** |
| every N = 2^k from 4 | N log2 N | (7/8) N log2 N, plus N/8 when k is odd | **(3/4) N log2 N + N/4** |

The 19 lines are the circuit above before the halving: where it has `g9 = m8 - x7`, the 19-line circuit has
`g8 = g7 - 2*x7`. The 52 and the rate 3/4 come from a second construction, which I call the family. (The
*rate* is the number in front of N log2 N.)

The comparison is like for like. Coppersmith, Feig and Linzer (1994) count one multiply-add as one
operation: one value plus or minus the product of two others, which they write ±a ± bc. In these circuits
one factor of the product is always a constant. Every line of my circuits is one such operation, so the
comparison is in their own count: their formula gives 22 operations at 8 points and 56 at 16, and I have 19
and 52; their rate is 7/8 and mine is 3/4. Count (G) as defined above is a little wider than theirs in two
ways: it allows a constant on both terms, and it lets a multiplication on its own go free, where the 1994
paper charges one. My count-(G) circuits use neither: every line has two terms and at most one constant.
`multiply_add_check.py` checks that no line of any circuit file has a constant on both terms. They claim no
lower bound, and I do not claim that my counts are the least possible.

Status: these counts are not in Lean. Every circuit up to 16,384 points was replayed exactly by the Python
programs (the two largest sizes with `run.py --kmax 14`). For larger N the count of the family rests on a
short induction, written in the first lines of `tools/circuits/gen.py`, which the agents checked and no
person has read.

The two results have not been combined. With every operation charged, the rate of the family is 7/8, which
is worse than 5/6: for the exact transform at 64 points it costs 416 operations, against 384 by layers of
the 8-point circuit. On 11 October the agents tried six ways of mixing the two constructions in count (O)
and found nothing below 5/6. They also have an argument about the family alone: if its lines are kept as
they are, and only the power of 2 at which each value is held is changed, the rate cannot go below 7/8 in
that count. This is an argument and computations by the agents, not in Lean. Nobody has searched directly
for a 16-point circuit that gives the transform up to a common factor in 53 operations or fewer of
count (O). The best known has 56. With 53, layers of it would beat 5/6.

## Is it faster in practice?

Not in the test that counts. That test is FFHT (<https://github.com/FALCONN-LIB/FFHT>), a tuned open-source
library for this transform. I wrote the new 8-point step into the code that FFHT's own generator produces,
in place of its block of 24 additions and subtractions, and changed nothing else. On the one machine I
timed, this did not make FFHT faster at any size from 2^6 to 2^26 points in single precision or from 2^5 to
2^26 points in double precision: set against a second build of FFHT's unchanged code, all 129 combinations
of size and form took more time.

| form of the step | more time from 2^7 points (2^6 in double precision) to 2^19 points | more time from 2^20 to 2^26 points, on average |
|---|---|---|
| 20 operations, exact output | 11 to 24 % | 6 to 7 % |
| 20 operations, output left divided by a power of two, which is not FFHT's output | 4 to 12 % | 3 to 5 % |
| the 19 operations of the second count, each as one *fused multiply-add* (one instruction for "a plus twice b"), exact output | 1 to 11 % | 2 to 3 %, which is too small for one run to establish: no gain, and a loss not shown |

The likely reason is the chain of operations that wait for one another. In the textbook block no result is
more than 3 operations away from the loaded numbers; in the new step the last results are 7 operations
away, 6 in the fused form. What happens inside the processor was not measured, so this is an explanation
that fits, not a finding.

An earlier timing of my own plain C did show a gain, and it is not a gain of the step. Compiled by gcc
13.3.0 with `-O3 -march=native` on the same machine, the new step took less time than the textbook step
only in double precision at the sizes 2^6, 2^9, 2^12 and so on to 2^27: 7 to 37 % less with exact output.
In double precision at every other size from 2^4 to 2^26 it took 1 to 13 % more, and in single precision at
every size from 2^3 to 2^27 it took 2 to 51 % more. At 2^6 to 2^18 points the gain is larger than replacing
24 operations by 20 can give, which is 17 % at most, so it comes from how the compiler treats one pass of
my code and not from the operation count. The cause has not been found.

Conditions: one rented virtual machine with the AVX2 and FMA instruction sets (*vector instructions*, which
work on 8 or 4 numbers at once), with other programs running at full load; gcc 13.3.0; FFHT at its last
version (March 2019), built by its own Makefile; one thread; the best of 15 repeats (9 where a size was
timed a second time, and for the plain C); 11 October 2026; not repeated on a second machine or with a
second compiler. So this is time on one machine in one library. It says nothing about other processors,
and nothing against the operation counts. The long version, with the tables by size, the fused form in a
program of my own, the sources and how to run it again, is
[tools/circuits/fast/wht56/results/ffht/README.md](tools/circuits/fast/wht56/results/ffht/README.md). The
plain C timings, on that machine and on a Mac mini, are in
[bench.md](tools/circuits/fast/wht56/results/bench-by-size/bench.md).

## In hardware

On a chip the second count is the number of *adders*. A circuit there is a network of adders (an adder
adds or subtracts two numbers), and doubling a number costs nothing, because it only moves the wires by one
place. So the 19-operation circuit is 19 adders. The standard design is the textbook "butterfly" network,
24 adders at 8 points; the 8-point Hadamard module of the open video encoder xk265
(<https://github.com/openasic-org/xk265>) is that network.

I checked the circuits as designs for an FPGA: a chip whose logic is set by loading a file into it,
made of *logic cells* (on the chip used here, each a small lookup table, a carry bit and a one-bit memory).
Two open-source tools did the work: Yosys 0.69 turns a design into logic cells (*synthesis*), and nextpnr
0.11.1 counts the cells, gives each a place on the chip and wires them (*placement and routing*), and then
estimates the highest *clock*, the number of results the design can take in a second. Each design was built
as one block of adders with no *pipeline registers* inside (rows of one-bit memories between the adders,
which let the clock run faster), and compared with the textbook network built the same way. The 8- and
16-point designs were placed and routed; of the family, only the sizes named under Sources.

| circuit | logic cells, as one block of adders with no registers inside | the price in speed (estimates of the tools, not measurements) | with pipeline registers |
|---|---|---|---|
| 8 points, 19 adders; Lattice iCE40HX8K, 8-bit inputs, one output register | 274 against 349 for the textbook: 75 fewer (21.5 %); with the synthesis option `-dff`, 273 against 337: 64 fewer (19.0 %) | twice as deep; highest clock about 72 MHz against about 97 MHz | the textbook is the smaller design above about 85 MHz; at one adder per clock, 677 cells against 363 |
| 16 points, 52 adders; the same chip and conditions | 877 against 969: 9.5 % fewer (17.4 % fewer without the output register) | twice as deep; about 55 MHz against about 71 MHz | at one adder per clock, 1,732 cells against 1,013 |
| the family, 16 to 256 points; signed 9-bit inputs, no output register; cells counted before placement (from 128 points the designs do not fit this iCE40 chip) | 17.5 % fewer at 16 points, rising to 23.1 % fewer at 256, on a Lattice iCE40; 19.1 % to 22.0 % fewer on a Lattice ECP5. On paper the saving in adders is 18.8 % to 21.9 % at these sizes, and a quarter only in the limit | twice as deep; about 30 % slower on the iCE40 and about 37 % slower on the ECP5 | with a register after every adder level, 67 % to 70 % more iCE40 cells than the textbook, not fewer |

The 19-adder circuit is not the smallest design on this chip: the 22-adder step of Alman and Rao (2023)
takes 244 cells under the same conditions, and at 16 points the 1994 design of Coppersmith, Feig and Linzer
takes 720. With these tools a subtraction costs more cells than an addition on this chip, and about half of
the 8-point saving comes from having 9 subtractions against the textbook's 12, not from having fewer
adders. From 16 to 256 points the family takes 10 % to 14 % fewer cells than the 1994 design on the
ECP5, and about as many on the iCE40 (between 2 % fewer and 10 % more, depending on the size).

On an iCE40-HX8K FPGA board running at 12 MHz, the 19-adder 8-point Walsh-Hadamard circuit was run side by side with the textbook circuit on 597,750,000 test inputs, and the two gave the same outputs every time; a deliberately broken copy of the circuit, run alongside, was caught, which shows the test can fail. This checks only that the circuit computes the right values on a real chip: it says nothing about size or speed, and in this pipelined build the 19-adder circuit is the larger of the two designs. The lines the board sent, and the conditions, are in [tools/circuits/fpga/board/run-2026-10-11/](tools/circuits/fpga/board/run-2026-10-11/README.md).

No existing design was improved in this check. The long version, with the tables, the designs, what was and
was not placed and routed, and how to run the tools again, is
[tools/circuits/fpga/README.md](tools/circuits/fpga/README.md).

## How it was found, and the use of AI

On the night of 10 to 11 October 2026 I ran a search for a way to compute this transform in a number of
operations proportional to N. Ten groups of AI agents (Anthropic's Claude) worked on it one after another
at my direction; I call each group a *wave*. The search found no such thing. These circuits are a
by-product. A local search that started from the known 22-operation circuit at 8 points fell to a circuit
with 20 operations in the second count within seconds. That is not the circuit shown above. Reading it gave
the family. About an hour later, in the third wave, a random search fell to 19 in each of four runs and
never to 18. Halving the centre of that 19-operation circuit gives the 20 operations shown above, with
every operation charged.

The search programs are in [tools/circuits/search/](tools/circuits/search/README.md), as they were run, with
their outputs. The README there says for each program what it searches, what it found, how long it takes
and what it does not show. A search that finds nothing proves nothing: I do not claim that 19 is the least.

The folder [waves/](waves/) is the record of that night: about 180 working reports of the ten waves, with
their programs. [WHERE-THE-CIRCUITS-CAME-FROM.md](waves/WHERE-THE-CIRCUITS-CAME-FROM.md) follows the path to
the circuits report by report and explains the two strategies, 3/4 and 5/6, where they meet, and what came
of trying to combine them. [LEADS.md](waves/LEADS.md) lists what is still open, twelve leads for a better
constant and fifteen for a change of order, and what was tried and failed, so that nobody has to try it
again. The reports are the agents' own words: no person has reviewed them, nothing in that folder is in
Lean, and later reports correct earlier ones. Start with [waves/README.md](waves/README.md).

The agents wrote the programs, the Lean files, the paper and the text of this repository, searched the
literature, and read the two older papers named below, from copies I obtained: Coppersmith, Feig and Linzer
(1994) in full, and of Grigoryan and Agaian (2000) pages 172 and 178 to 183. Pages 173 to 177 of the second,
which set out its algorithm, were not read; the algorithm is taken from the proof and the program in its
appendix. The agents' work has not had a line-by-line review by a person.

## Credit, and what is in print

- **Alman and Rao (2023).** The method is theirs: write the 8-point table of signs as a part of low rank
  (every row a multiple of one row, or a sum of a few such) plus a sparse part (few entries that are not
  zero), and halve once. Their 8-point step costs 23 operations (22 additions or subtractions and one
  halving) where this one costs 20. Their count model is the strict one used here, so the table at the top
  compares the same task with the same things charged. Their theorem is wider than mine: it covers every
  power of two and any field (any system of numbers with the four operations), where my Lean statement
  covers the powers of 8 over the complex numbers. Their
  exact count first falls below the textbook at 16,777,216 points, and mine at 512. What the search added is
  which values to share inside the 8-point step.
- **Coppersmith, Feig and Linzer (1994).** The 4-point circuit with 7 operations is due to them (page 969),
  and so is the rate 7/8 in the second count. Everything in that count starts from their circuit.
- **OpenAI.** The circuit model, and the Lean theorems on the cost of applying a circuit along several
  groups of binary digits (tensor products), are from [openai/math](https://github.com/openai/math), under
  the Apache License 2.0. The 44 files under `lean/OAI/` are theirs, unmodified. [NOTICE](NOTICE) lists
  them, the two places where a few lines of theirs are repeated, and the commands that compare the files
  with their repository. **This repository is not a project of OpenAI.** OpenAI did not write, review or
  endorse it.
- **A count that is too small.** Grigoryan and Agaian (2000) state a count of 6·2^r - r^2 - 3r - 6 additions
  for the transform on N = 2^r points, about six per point (page 181). That count is too small. The
  recursion that its algorithm follows, as the program printed on that page carries it out, adds up to
  exactly N log2 N. And from 4,096 points on the stated count (24,390) is below (N/2) log2 N (24,576), a
  lower bound for circuits of additions and subtractions; the paper's own introduction gives 0.5 N log N as
  a lower bound for the Hadamard transform (page 172). `tools/circuits/ga_count.py` prints the computation.

I did not find these counts in the literature I searched: the papers that the indexes list as citing Alman
and Rao or the 1994 paper, arXiv, seven patents, and the first part of one survey. It is a search, not a
proof that the counts are new. [The note](notes/explicit-circuits.md), section 7, says what was read and
what was not. If you know a smaller count in print, I would be glad to hear of it and will credit it.

## The folders

| where | what |
|---|---|
| [docs/UNDERSTAND.md](docs/UNDERSTAND.md) | start here to understand the result: ten steps, each with a check; `docs/walkthrough.py` computes the numbers of each step |
| [paper/](paper/README.md) | the write-up as a paper, PDF and LaTeX source, with its two check programs; not peer reviewed |
| [notes/explicit-circuits.md](notes/explicit-circuits.md) | the full account: both counts, the tables, the Lean statement, the literature search, what has not been tried; the `.json` beside it has the figures in machine-readable form |
| [tools/circuits/](tools/circuits/README.md) | the circuits as text files (`programs/`), the checker and the generator, `run.py`, and what it printed in the recorded run |
| [tools/circuits/search/](tools/circuits/search/README.md) | the programs that found the circuits, as they were run |
| [tools/circuits/fast/wht56/](tools/circuits/fast/wht56/README.md) | the circuits as working programs in Python, numpy and C, with tests and the timings |
| [tools/circuits/fast/wht56/results/ffht/](tools/circuits/fast/wht56/results/ffht/README.md) | the 8-point step inside the library FFHT: the timings by size, my patch against FFHT's generator, the timing programs and their raw outputs. No file of FFHT is included |
| [tools/circuits/fpga/](tools/circuits/fpga/README.md) | the circuits as hardware: the generator of hardware descriptions, the designs, the scripts for the open-source tools, the result tables, and the sources of the self-test for a board |
| [waves/](waves/README.md) | the ten waves of the night of 10 to 11 October 2026. About 180 working reports by AI agents, with their programs and small outputs, sorted by wave; where the circuits came from; what is open and what is closed. Not reviewed by a person. Not in Lean. This folder is most of the repository: about 4,950 of its 5,700 files and 30 of its 44 MB. |
| [lean/](lean/) | the Lean project: `Work/SmallWHT/` has my six files, `OAI/` the 44 files of openai/math, `check.sh` the one command |
| [VERIFY.md](VERIFY.md) | how to check the Lean proof, and what was run |
| [NOTICE](NOTICE), [LICENSE](LICENSE), [CITATION.cff](CITATION.cff) | where each part comes from, the licence, how to cite |

## Licence

Apache License 2.0, the licence of openai/math: [LICENSE](LICENSE). [NOTICE](NOTICE) says which files are
OpenAI's and which are new.

## How to cite

Jacob Sussman, "The Walsh-Hadamard transform with fewer operations", 2026,
https://github.com/jacobalansussman/wht-fewer-operations. [CITATION.cff](CITATION.cff) has the same in a form
that programs read.

## Sources

- J. Alman, K. Rao, "Faster Walsh-Hadamard and Discrete Fourier Transforms From Matrix Non-Rigidity",
  STOC 2023, pages 455 to 462, doi 10.1145/3564246.3585188; <https://arxiv.org/abs/2211.06459>, version 2.
  The bound is their Theorem 1.1; the exact count is in the proof of their Theorem 6.2.
- D. Coppersmith, E. Feig, E. Linzer, "Hadamard transforms on multiply/add architectures", IEEE Transactions
  on Signal Processing 42(4), 1994, pages 969 to 970, doi 10.1109/78.285664.
- A. M. Grigoryan, S. S. Agaian, "Split manageable efficient algorithm for Fourier and Hadamard transforms",
  IEEE Transactions on Signal Processing 48(1), 2000, pages 172 to 183, doi 10.1109/78.815487. The stated
  count is on page 181 and the bound on page 172.
- openai/math, <https://github.com/openai/math>, at commit `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`.
- Lean 4, version 4.34.1; Mathlib at revision `d13f23b723b8a846827a245b89c10fc7d3f11612`, fetched by the
  build.
- FFHT, <https://github.com/FALCONN-LIB/FFHT>, at commit `fba727a3ff72c862260460631ae1cc8e3e44e861` (10 March
  2019, its last), under the MIT License. No file of it is in this repository.
- xk265, <https://github.com/openasic-org/xk265>, at commit `832e564a8e59dd90a18fb7ee8e2ed87d96aa03bc`,
  module `hadamard_trans_1d` in `rtl/fme/fme_satd_8x8.v`. No file of it is in this repository.
- The hardware figures: the open-source suite oss-cad-suite, release 2026-10-11, with Yosys 0.69+274
  (`synth_ice40`, default settings and with `-dff`) and nextpnr 0.11.1-59. At 8 and 16 points: chip
  iCE40HX8K in package CT256; cells identical over 20 placement seeds (66 to 76 MHz and 88 to 104 MHz over
  those seeds at 8 points); the design files proved equal to the transform for all inputs; the Alman and
  Rao figure is with its sums added in pairs (281 if added left to right); the 16-point figures with `-dff`
  are 870, 945 and 712; the pipelined figures are from 10 seeds, with a latency of 6 clocks against 3 at 8
  points and 8 against 4 at 16; the xk265 module built unchanged gives the textbook's cell counts in the
  default flow. For the family: cell counts after synthesis and packing, every wire at its exact width;
  placed and routed at 16 and 32 points for the iCE40-HX8K and at 64 and 128 points for the ECP5-85F; at 256
  points the counts are after packing and only the family and the 1994 design were routed; none of these
  sizes ran on a board.
- Dates. The searches: the night of 10 to 11 October 2026. The Lean build from nothing, the timings, the
  hardware measurements and the reading of the two older papers: 11 October 2026. The literature search: 10
  and 11 October 2026.
- The full list of what was read is in [notes/explicit-circuits.md](notes/explicit-circuits.md), section 10.
