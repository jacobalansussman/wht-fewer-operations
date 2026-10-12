# Explicit circuits for the Walsh-Hadamard transform below the textbook count

Author: Jacob Sussman. Text of 2026-10-11.

This note is the full account of the result of this repository: small circuits for the Walsh-Hadamard
transform, written out line by line, that use fewer operations than the textbook program at sizes people
run. The [README](../README.md) is the short version. [docs/UNDERSTAND.md](../docs/UNDERSTAND.md) goes
through the main circuit in ten steps, each with a check to do by hand.

**It is a better constant, not a better exponent.** Every count in this note is a fixed fraction of
N log2 N. Results that lower the exponent, such as OpenAI's of 25 September 2026 for the Fourier transform,
are of a smaller order (section 5).

**What is checked by Lean and what is not.**

- One statement is checked by Lean: for every j, the exact transform on N = 8^j points has a circuit with at
  most 20 j 8^(j-1) + 8^j gates, which is (5/6) N log2 N + N, in OpenAI's circuit model. Section 6 has the
  statement, where it is, and what the check covered.
- Everything else in this note is not checked by Lean: the 19 operations at 8 points, the 52 at 16, the rate
  3/4, and the rate 7/8 for the scaled transform. Those rest on exact replay by Python programs, which are in
  `tools/circuits/`.

I directed this work. The AI agents (Anthropic's Claude) that I ran wrote the programs, ran the searches,
wrote the Lean files, searched the literature and read the two older papers (section 7). Their reports have
not had a line-by-line human review, and no person has yet read the Lean files.

## 1. What this is

**Words.** N = 2^k is the number of points. H is the N × N matrix with the entry +1 or -1 in row j, column c
(both numbered from 0): +1 when j and c, written in binary, have an even number of 1-bits in common, and -1
otherwise. The *Walsh-Hadamard transform* of a list x of N numbers is H x. *Exact* means H x itself, with no
factor in front. The *textbook*
program is the butterfly: k layers of N additions and subtractions, N log2 N operations. The *address* of a
point is its number, 0 to N - 1, written with k binary digits, its *address bits*. The *rate* of a family of
circuits is the number in front of N log2 N in its count.

There are two ways to count, and every number below belongs to one of them.

- **Count (G).** One operation is one a·u + b·v, with any constants a and b. Multiplying by a constant is
  free.
- **Count (O).** Every addition, every subtraction and every multiplication by a constant costs one. This is
  the gate set of OpenAI's circuit model (`lean/OAI/Computability/FourierCircuit/Core.lean`) and the count of
  Alman and Rao.

The textbook costs N log2 N in both. A multiplication by 2 or by 1/2 costs one in count (O) and nothing in
count (G). No count-(O) program of this note changes a sign on its own, so it does not matter whether a bare
change of sign is charged.

Count (G) is wider than the count of the 1994 paper named below, in two ways. That paper charges one for a
*multiply-add*, which computes ±a ± b·c: two terms, with a product in one of them only, where count (G)
allows a constant on both terms. And that paper charges one for a multiplication on its own, which count (G)
lets go free. The count-(G) circuits of this note use neither: every line has two terms and at most one
constant (section 2). So the count (G) of each circuit of mine below is also its count in the 1994 paper's
own sense.

**The results.**

1. Count (G), 8 points: 19 operations. The textbook has 24, and the smallest count at 8 points that I found
   in print is 22. Not checked by Lean; replayed exactly, and short enough to check by hand (section 2).
2. Count (G), every N = 2^k from 4 points on: (3/4) N log2 N + N/4 operations. That is 7, 20, 52, 128, 304
   at 4 to 64 points. The best rate I found in print is 7/8, from 1994: (7/8) N log2 N operations when N is
   a power of 4 and N/8 more when N is an odd power of two, so 56 at 16 points. Not checked by Lean. Every
   circuit up to 16,384 points was replayed exactly; for larger N the count rests on a short induction,
   written out in the generator. The agents checked it twice, and no person has read it.
3. Count (O), exact H x, N a power of 8: (5/6) N log2 N + N operations. At 512 points that is 4,352 against
   the textbook's 4,608, and 512 is the first size where it is below the textbook. The best count I found in
   print is Alman and Rao's: at most (23/24) N log2 N + (13/12) N, and exactly (23/24) N log2 N + N - 1 when
   N is a power of 8. Their theorem covers every power of two and any field; my Lean statement covers the
   powers of 8, over the complex numbers. The count of mine is the one statement checked by Lean
   (section 6); the gate lists themselves are checked by the Python programs.
4. Count (O), the scaled transform H x / √N, N a power of 4: (7/8) N log2 N + N/4 operations, 60 at 16
   points. Not checked by Lean; replayed exactly up to 16,384 points. This is the family of result 2 with
   every operation charged. An argument, and exact computations at 4 to 64 points, say that the wiring of
   the family cannot go below the rate 7/8 in count (O) however its values are scaled (section 9). The
   agents made both on 11 October; neither is in Lean.

"New" means here: I did not find it in the literature I searched. Section 7 says what was searched, what was
read and what was not.

## 2. The circuits

**Four points, 7 operations, count (G). This one is known.** Seven operations at 4 points are due to
Coppersmith, Feig and Linzer (1994, page 969). They compute one value that differs from three of the four
outputs in a single sign, and get each of those outputs by adding twice one input. In their words, "we have
traded one addition for three multiplications by two, and all of the multiplies appear in m/a-ops." (An
"m/a-op" is their name for one operation: a multiply-add, a plain addition or a plain multiplication.) The
circuit was found again by a computer search (Samadi, Suzukake and Iwakura, 1998) and appears in a patent
(Reshef and Alrod, filed 2002). A 4-point step with 7 additions or subtractions and one halving is in Alman
and Rao (2023), from a decomposition of Alman (2021). The 1994 circuit is the starting point of everything
below. My listing is another wiring of the same idea, with four doublings where
theirs has three: theirs has 4 additions or subtractions and 3 multiply-adds, and mine has 3 and 4. In
count (O) theirs costs 10 and mine 11; the textbook costs 8. The paper does not say whether 7 is the least.

```
p = x0 + x1      q = x2 - x3      h = p + q                              h has the signs + + + -
y0 = h + 2*x3    y1 = h - 2*x1    y2 = h - 2*x2    y3 = -h + 2*x0
```

**Eight points, 19 operations, count (G).** One line is one operation. On the right is the value of the line
written in x0 to x7: + means +1, - means -1 and a dot means 0. To check the circuit by hand, check each
pattern from the two lines it uses. The line y_j must come out as row j of H.

```
g1  = x0 + x7        + . . . . . . +
g2  = x1 + x6        . + . . . . + .
g3  = x2 - x5        . . + . . - . .
g4  = x3 - x4        . . . + - . . .
g5  = g1 - g2        + - . . . . - +
g6  = g3 + g4        . . + + - - . .
g7  = g5 - g6        + - - - + + - +      the centre; not an output
g8  = g7 - 2*x7      + - - - + + - -
g9  = g7 - 2*x5      + - - - + - - +
g10 = g8 + 2*x6      + - - - + + + -
g11 = g9 - 2*x4      + - - - - - - +
y7  = g10 + 2*g4     + - - + - + + -
y1  = g10 + 2*g3     + - + - + - + -
y6  = g11 + 2*g2     + + - - - - + +
y0  = -g11 + 2*g1    + + + + + + + +
y2  = g8 + 2*x1      + + - - + + - -
y3  = g9 + 2*x3      + - - + + - - +
y4  = y2 + 2*g6      + + + + - - - -
y5  = -y3 + 2*g5     + - + - - + - +
```

How it works. Seven operations merge the eight inputs into one value, the centre. Twelve more flip signs, by
adding twice an input or twice a piece that the merging left behind. Every partner in those twelve lines is
either an input or a value that was already paid for. Two of the 19 lines, y0 and y5, have a minus sign on
their first operand. Each of the 19 lines has two terms and one constant at most, so each is also one
operation in the count of the 1994 paper, which charges one for a multiply-add with any signs.

**The same circuit in count (O): H x / 2 in 20 operations.** Halve the centre once, right after the line g7.
Then every "2*" in the lines below it goes away: 19 additions and subtractions and one halving. The outputs
are the rows of H divided by 2. No line needs a bare change of sign.

**From 8 points to 8^j points, count (O).** Use the 20-operation circuit in layers, on three address bits at
a time. After j layers every output carries the factor 1/2^j. One multiplication per output at the end
removes it. That is 20 j 8^(j-1) + 8^j operations for exact H x, which is (5/6) N log2 N + N. At 8 points
that is 28, above the textbook's 24; the gain starts at 512 points. When k is not a multiple of 3, a textbook
layer serves each bit left over: with k = 3m + r, m at least 1 and r = 1 or 2, the count is N (k - m/2 + 1).

**The family, count (G): (3/4) N log2 N + N/4 for every N.** The textbook keeps every output of the
half-size transform on both halves of each block of addresses. The family keeps each on one half only, and
adds one more kind of value, which I call a *hub*: one half-size output on the lower half of a block plus a
different one on the upper half. A hub is one operation away from an output, and the second value that this
operation needs was made two levels below. So one value serves two neighbouring levels, and a level costs
3N/4 on average in place of N. In count (O), for N a power of 4, the same family gives H x / √N in
(7/8) N log2 N + N/4 operations: 60 at 16 points, against 64 by two layers of the 4-point circuit with its
value h halved once (that circuit gives H x / 2 at 4 points in 8 operations of count (O)). Both numbers
are for the scaled transform H x / 4. With 16 more multiplications for exact H x it is 76, above the
textbook's 64. For exact H x in count (O) the layers of the 8-point circuit are the better route. On
11 October the agents looked for a better choice of scales for the family, and for a mix of the family with
the 8-point circuit, in count (O). They found nothing below these numbers (section 9).

The generator that writes the family for any N, with the recursion spelled out in its first lines, is
`tools/circuits/gen.py`.

**The comparison with the 1994 paper is like for like.** Coppersmith, Feig and Linzer say on page 969 what
they count: one multiply-add, which computes ±a ± b·c, costs one, and so does a plain addition or a plain
multiplication. Count (G) allows a constant on both operands, which is more than that. My circuits do not
use it: every counted line has two terms and at most one multiplication by a constant, and a program checked
this for every circuit file (`python3 -B tools/circuits/multiply_add_check.py`). So each line is exactly one
of their operations. They give (7/8) N log2 N operations when N is a power of four and N/8 more when N is an
odd power of two, which is 22 at 8 points and 56 at 16. They print the formulas and the 7 at 4 points, not
the 22. On page 970 they add that a routine that takes 16 points at a time would have the same number of
operations: eight 4-point transforms, so 56. My circuits have 19 at 8 points, 52 at 16, and
(3/4) N log2 N + N/4 at every power of two from 4 on. They claim no lower bound, and I do not claim that
my counts are the least possible.

## 3. The tables

Exact H x in every column. "Textbook" is N log2 N. "(G) published" is computed from the two formulas of
Coppersmith, Feig and Linzer (1994, page 969): (7/8) N log2 N when N is a power of four, and N/8 more when N
is an odd power of two. "(G) family" is (3/4) N log2 N + N/4. "(G) layers" is the best
layering of the small circuits alone: the 8-point circuit on three bits at a time, then a textbook layer for
one bit left over or the 4-point circuit for two. "(O) Alman and Rao" is the exact count in the proof of
their Theorem 6.2, (23/24) N k + (N/24)(k mod 3) + N - 1 with k = log2 N; it charges what count (O)
charges. "(O) layers" is the 20-operation circuit on three bits at a time, a textbook layer for each
bit left over, and N multiplications at the end. In each of the two counts, bold marks the smallest number
of the row when it is one of this note's and is below the textbook. The row for 4 points shows the known 7
only; the three columns on the right start at 8 points.

| points | textbook | (G) published | (G) family | (G) layers | (O) Alman and Rao | (O) layers |
|---|---|---|---|---|---|---|
| 4 | 8 | 7 | 7 | | | |
| 8 | 24 | 22 | 20 | **19** | 30 | 28 |
| 16 | 64 | 56 | **52** | 54 | 77 | 72 |
| 32 | 160 | 144 | **128** | 132 | 187 | 176 |
| 64 | 384 | 336 | **304** | **304** | 431 | 384 |
| 128 | 896 | 800 | **704** | 736 | 991 | 896 |
| 256 | 2,048 | 1,792 | **1,600** | 1,664 | 2,239 | 2,048 |
| 512 | 4,608 | 4,096 | **3,584** | 3,648 | 4,927 | **4,352** |
| 1,024 | 10,240 | 8,960 | **7,936** | 8,320 | 10,879 | **9,728** |
| 2,048 | 22,528 | 19,968 | **17,408** | 18,176 | 23,807 | **21,504** |
| 4,096 | 49,152 | 43,008 | **37,888** | 38,912 | 51,199 | **45,056** |

How to read it.

- In count (G) the circuits of this note are below the textbook and below the numbers I found in print from
  8 points on.
- In count (O) they are below the textbook from 512 points on, at every power of two that was computed (to
  16,384 points) and by the formula at every larger one. Below 512 points the textbook is still the smallest
  exact count I know: at 64, 128 and 256 points the layers tie with it, and at 8, 16 and 32 they are above
  it.
- In count (O) they are below Alman and Rao's count at every size from 8 points on. That count is above the
  textbook at every size in the table. By its formula it first falls below the textbook at
  2^24 = 16,777,216 points; the bound of their Theorem 1.1, (23/24) N log2 N + (13/12) N, at 2^27 points.

The scaled transform H x / √N in count (O), for even k. The textbook needs N multiplications more than
N log2 N for it. "Layers" is the layering of the small circuits that is cheapest when any common factor is
allowed, followed by N multiplications that bring the factor to 1/√N (none at 4 points, where the factor is
already 1/2). At 16 points this column is not the cheapest route by layers: two layers of the 4-point
circuit give H x / 4 in 64 operations with no multiplication at the end (section 2). The family's 60 is
below both.

| points | textbook and N multiplications | family, (7/8) N log2 N + N/4 | layers |
|---|---|---|---|
| 4 | 12 | 8 | 8 |
| 16 | 80 | **60** | 72 |
| 64 | 448 | **352** | 384 |
| 256 | 2,304 | **1,856** | 2,048 |
| 1,024 | 11,264 | **9,216** | 9,728 |
| 4,096 | 53,248 | **44,032** | 45,056 |

Every count of mine in these tables was replayed: the circuit was written to a text file, read back, and run
exactly on every unit input (one input 1, the others 0), up to 4,096 points on a Mac and up to 16,384 points
on a Linux machine. Above that the counts rest on the induction. One command does it again:
`python3 -B tools/circuits/run.py` (section 8). This is a check by Python programs, not by Lean.

## 4. How it was found

On the night of 10 to 11 October 2026 I ran a search for ideas towards a transform of linear size, with a team
of AI agents (Anthropic's Claude) that I directed. It found no change of order. These circuits fell out of
it. The searches below count as count (G) does.

One move of that search was to try to prove that N log2 N operations are needed, and to keep whatever stops
the attempt. The attempt supposed that a program holds only *pieces*: one output restricted to a block of
inputs. A local search in a slightly wider pool of values was started from the known circuit with 22
operations at 8 points: two 4-point circuits and one textbook layer, which is how the 1994 paper treats an
odd power of two. It fell to 20 within seconds. The 20 held a value that is not a piece, the hub of
section 2. It is what stops the proof. Used as a rule at every size, it is the family.

About an hour later a random search over sets of helper values (simulated annealing), again started from the
22, fell to 19 in each of four runs and never to 18. Started from nothing it found no circuit at all.

This history is taken from the reports and outputs of that night. `tools/circuits/search/README.md` says
which of the search programs were run again from a fresh copy, and what each search does not show.

Two remarks on what these circuits are.

- **They are not about this transform in particular.** H is built from copies of the 2 × 2 matrix with rows
  (1, 1) and (1, -1). With another 2 × 2 matrix with four non-zero entries in its place, the same 19 lines
  worked for every one that was tried (300 random ones), with other constants and up to a renaming of inputs
  and outputs and a scaling of each output. The family did too, in one program that no second program
  repeated. Both are computed, not proved.
- **The method is not mine.** Splitting a small transform into a part of low rank (a matrix whose rows are
  all multiples of one row, or sums of a few such) plus a sparse part (a matrix with few non-zero entries),
  and the single halving, are how Alman and Rao get a step of 23 operations at 8 points (30 for the exact
  8-point transform, by their count). What the searches added is which values to share.

## 5. What this is not

- **It is not a change of order.** OpenAI's result of 25 September 2026, for the Fourier transform, is below
  c·N log N for every constant c once N is large enough. My other repository,
  [wht-power-saving-lean](https://github.com/jacobalansussman/wht-power-saving-lean), is about a result of
  that kind for this transform. Nothing here depends on it, and nothing here is of that kind. The count-(G)
  circuits here cannot be: every value they hold is a list of 0, +1 and -1 in terms of the inputs (checked
  by program on the 19-operation circuit and on the family at 16, 64 and 512 points). So the constants of a
  line satisfy |a| + |b| ≤ 3, and for programs of that kind an argument from Morgenstern's determinant bound
  gives at least 0.3155·N log2 N operations. That argument was made by the agents and has not been reviewed;
  it is not in Lean. The count-(O) programs also hold values with entries 1/2, 1/4 and 1/8, and the argument
  has not been written out for them.
- **Most of it is not checked by Lean.** One count has a Lean statement (section 6). Nothing in count (G) is
  in Lean, and neither is the 7/8 family for the scaled transform.
- **It is not a faster program.** The test that counts is against FFHT, a tuned open-source library for
  this transform. Its code is *vector instructions* (instructions that work on 8 or 4 numbers at once),
  written out by its own generator, and it does three levels of the transform in one block of 24 additions
  and subtractions. The 8-point step was written into that generated code in place of the block, with
  nothing else changed. On the one machine that was timed, this did not make FFHT faster at any size from
  2^6 to 2^26 points in single precision or from 2^5 to 2^26 points in double precision: set against a
  second build of FFHT's unchanged code, all 129 combinations of size and form took more time. From 2^7
  points (2^6 in double precision) to 2^19 points it took 11 to 24 % more time with 20 operations and exact
  output, 4 to 12 % more with the output left divided by a power of two, which is not FFHT's output, and 1
  to 11 % more with the 19 operations of count (G), each written as one *fused multiply-add* (one
  instruction for "a plus twice b"). From 2^20 to 2^26 points it took 6 to 7 %, 3 to 5 % and 2 to 3 % more
  on average; for the fused form that is too small for one run to establish, so there the finding is no
  gain, not a loss. The likely reason is the chain of operations that wait for one another: in the textbook
  block no result is more than 3 operations away from the loaded numbers, and in the new step the last
  results are 7 operations away, 6 in the fused form. What happens inside the processor was not measured,
  so this is an explanation that fits, not a finding. The earlier timings of my own plain C are not a gain
  of the step either. Compiled by gcc 13.3.0 with `-O3 -march=native` on the same machine, the new step
  took less time than the textbook step only in double precision at the sizes 2^6, 2^9, 2^12 and so on to
  2^27: 7 to 37 % less with exact output. In double precision at every other size from 2^4 to 2^26 it took
  1 to 13 % more, and in single precision at every size from 2^3 to 2^27 it took 2 to 51 % more. At 2^6 to
  2^18 points the gain is larger than replacing 24 operations by 20 can give, which is 17 % at most, so it
  comes from how the compiler treats one pass of my code and not from the operation count; the cause has
  not been found. On a Mac mini (Apple M4, a kind of processor for which FFHT's own repository has no
  code), the same plain C took 2 to 5 % less time than the textbook written the same way from 4,096 points
  up when the compiler wrote vector instructions, 2 to 30 % more at 8, 64 and 1,024 points, and the same
  time within 4 % from 64 points up when it did not. Differences of 3 % or less are inside the noise
  there, and no tuned library was timed on that machine, so these figures compare what one compiler made
  of two programs of mine; they do not isolate the step. The conditions of the timings beside FFHT: one
  rented virtual machine with the AVX2 and FMA instruction sets, other programs running at full load, gcc
  13.3.0, FFHT at its last version (March 2019) built by its own Makefile, one thread, the best of 15
  repeats (9 where a size was timed a second time, and for the plain C), 11 October 2026, not repeated on a
  second machine or with a second compiler. It is time on one
  machine in one library, and it says nothing about other processors and nothing against the operation
  counts. Every number is in
  [the page on FFHT](../tools/circuits/fast/wht56/results/ffht/README.md) and, for the plain C, in
  `tools/circuits/fast/wht56/results/bench-by-size/bench.md`. The 1994 paper shows the same gap between
  counting and timing: its count predicts a gain of 12.5%, and the authors measured 5.6% to 7.4% on their
  machine (an IBM RISC System/6000 Model 530, 64 to 4,096 points, pages 969 and 970).
- **As hardware it saves cells in one setting, and it is not the smallest design.** On a chip, count (G) is
  the number of *adders* (an adder adds or subtracts two numbers), because doubling a number only moves its
  wires by one place. The circuits were built for an FPGA, a chip whose logic is set by loading a file into
  it and which is made of *logic cells* (on the chip used here, each a small lookup table, a carry bit and a
  one-bit memory), with the open-source tools Yosys 0.69 and nextpnr 0.11.1. As one block of adders with no
  *pipeline registers* inside (rows of one-bit memories between the adders, which let the clock run
  faster), with 8-bit inputs and one output register, the 19-adder 8-point circuit takes 274 logic cells on
  a Lattice iCE40HX8K where the textbook network takes 349, which is 75 fewer (21.5 %), or 273 against 337
  (64 fewer, 19.0 %) with the synthesis option `-dff`. The saving has a price: the circuit is twice as
  deep, so the tools estimate its highest clock at about 72 MHz against about 97 MHz for the textbook
  (timing estimates, not measurements), and once pipeline registers are added for speed the textbook is
  the smaller design above about 85 MHz (at one adder per clock, 677 cells against 363). It is also not the
  smallest design on this chip: the 22-adder step of Alman and Rao (2023) takes 244 cells under the same
  conditions, and at 16 points my 52-adder circuit takes 877 cells against 969 for the textbook (9.5 %
  fewer with one output register; 17.4 % fewer without it) and 720 for the 1994 design of Coppersmith, Feig
  and Linzer. With these tools a subtraction costs more cells than an addition on this chip, and about half
  of the 8-point saving comes from having 9 subtractions against the textbook's 12, not from having fewer
  adders. The family from 16 to 256 points, with signed 9-bit inputs and no output register, takes
  17.5 % fewer logic cells than the textbook network at 16 points, rising to 23.1 % fewer at 256, on a
  Lattice iCE40, and 19.1 % to 22.0 % fewer on a Lattice ECP5, as a single block of adders with no
  registers inside (cells counted before placement; from 128 points the designs do not fit that iCE40
  chip). It is about 30 % slower than the textbook block on the iCE40 and about 37 % slower on
  the ECP5 by the tools' timing estimates, and with a register after every adder level it needs 67 % to
  70 % more iCE40 cells than the textbook network instead of fewer. Against the 1994 design it takes 10 %
  to 14 % fewer cells on the ECP5 and about as many on the iCE40 (between 2 % fewer and 10 % more,
  depending on the size). The standard in the hardware designs that were read is the textbook network; the
  8-point Hadamard module of the open video encoder xk265 is that network. On an iCE40-HX8K FPGA board running at 12 MHz, the 19-adder 8-point Walsh-Hadamard circuit was run side by side with the textbook circuit on 597,750,000 test inputs, and the two gave the same outputs every time; a deliberately broken copy of the circuit, run alongside, was caught, which shows the test can fail. This checks only that the circuit computes the right values on a real chip: it says nothing about size or speed, and in this pipelined build the 19-adder circuit is the larger of the two designs. No existing design was improved in this check.
  [tools/circuits/fpga/README.md](../tools/circuits/fpga/README.md) has the tables, the conditions, what
  was and was not placed and routed, and the designs.
- **It is not known to be optimal.** With free constants I found no lower bound above linear for this
  transform. The only lower bound proved here is 2N - 1 operations, in either count: 7 at 4 points, 15 at 8 and
  31 at 16. It is Proposition 6 of [the paper](../paper/explicit-wht-circuits.pdf). The agents wrote its
  proof on the morning of 11 October 2026, and a second agent read it. A program checks two steps of it on
  every case at 4 and 8 points (`paper/lowerbound_check.c`). No person has read the proof, and it is not in
  Lean. So the least count at 8 points is between 15 and 19. The number 19 is the exact minimum only among
  circuits of its own shape, one merge of the inputs followed by a walk of sign flips: two exhaustive
  searches, written separately, agree on that. At 16 points the local searches found nothing below 52,
  which proves nothing.
- **It is "new" only as far as the search of section 7 goes.**

## 6. The statement that Lean checked

The statement, in OpenAI's circuit model:

    theorem OAI.ExactFourier.WHT8Half.hadamard_pow8_circuit (j : ℕ) :
        ∃ C : Circuit (2 ^ (3 * j)),
          C.Computes (hadamard (3 * j)) ∧ C.size ≤ 20 * (j * 8 ^ (j - 1)) + 8 ^ j

In words: for every j there is a circuit on 8^j inputs that computes the exact transform and has at most
20 j 8^(j-1) + 8^j gates. That number is (5/6) N log2 N + N for N = 8^j.

**The words of the statement.**

- `Circuit n` is OpenAI's: a list of gates on n inputs and a choice of n outputs. A gate is `add i j`,
  `sub i j` or `scale c i`, with c any complex constant, and each gate costs one. A gate may use any earlier
  value any number of times. `C.size` is the number of gates. `C.Computes A` says that for every input x
  the outputs are the matrix A times x. These are in `lean/OAI/Computability/FourierCircuit/Core.lean` (55
  lines).
- `hadamard k` is the matrix H on 2^k points, with the entry formula of section 1. It is defined in
  `lean/Work/SmallWHT/H8Half.lean`. The theorem `wht_eq_mulVec` in `lean/Work/SmallWHT/H8Bridge.lean` says
  that multiplying by this matrix is the function `wht` of `lean/WHTCheck/Solution.lean`, in which every
  output is written as a sum of the inputs with signs. The two use the same formula, so this is a second
  way to read the definition, not an independent check of it.

**The files**, all in `lean/Work/SmallWHT/`:

| file | what it holds | the names to look for |
|---|---|---|
| `H8Half.lean` | the 20 gates of section 2 as data, and the proof that they compute H / 2 on 8 points | `exists_circuit` |
| `HadamardDigits.lean` | the entries of `hadamard k` as a product over binary digits | `hadamard_eq_digits` |
| `TensorPow8.lean` | the count for 8^j points | `hadamard_pow8_circuit`, `hadamard_512_circuit` (at most 4,352 gates at 512 points) |
| `TensorPow8Real.lean` | the same count written as (5/6) N log2 N + N | `hadamard_pow8_circuit_real` |
| `H8Bridge.lean` | the link with `wht` | `wht_eq_mulVec`, `circuit_eval_eq_wht` |
| `ChallengeWHT8.lean` | the two statements alone, without proofs | |

`H8Half.lean` is written by a program, `tools/circuits/lean/slp2lean.py`, from the 20 lines of
`tools/circuits/lean/h8_half_o20.txt`. The one command of section 8 writes it again and compares.

**How the proof goes.** The 8-point circuit is checked gate by gate. For 8^j points the proof uses OpenAI's
own Lean development of circuit costs. The *tensor product* of two matrices applies the first to some of the
address bits and the second to the others. Its cost is at most (size of the second) × (cost of the first) +
(size of the first) × (cost of the second). By induction, j layers of the
8-point circuit cost at most j 8^(j-1) × 20 gates and compute H divided by 2^j. One `scale` gate per output
removes the factor. This uses 44 files of OpenAI's repository: `Core.lean`, which holds the circuit model,
and 43 files on the cost of tensor products. They are under `lean/OAI/Computability/FourierCircuit/`,
unmodified. One short theorem of theirs is repeated with its proof inside `TensorPow8.lean`, so that seven
more of their files are not needed; the file and the [NOTICE](../NOTICE) say so.

**What the check covered.** On 11 October 2026 the folder `lean/` was built from nothing with `lake`, Lean's
build program, on a rented Linux machine, on Lean 4 (version 4.34.1). Mathlib's compiled files came from its
cache. The 51 files of the folder were compiled from source: 44 of OpenAI's and 7 others. Lean accepted them
with no error, and with no warning other than the two that are expected for `ChallengeWHT8.lean`, which
states the two theorems without proofs. The theorems depend on the three standard axioms only (`propext`,
`Classical.choice`, `Quot.sound`). `lean/tools/Compare.lean` then found both statements of
`ChallengeWHT8.lean` identical to the theorems that are proved. [VERIFY.md](../VERIFY.md) has the commands,
what they print, the time and the memory.

**The limits of that check.**

- One machine, and one run from nothing. It was not built on a Mac.
- `Compare.lean` is a script that the agents wrote. It is not Lean's official tool for this comparison, which
  is called `comparator`, and `comparator` was not run on this folder. In the night of 10 to 11 October, in
  the folder where the six files were written, `comparator` accepted the same two statements, with a
  stand-in for its sandbox and with a configuration file that is not in this repository.
- The matrix `hadamard` in the statement is a definition written that night. No person has read the
  statement.
- Two controls were run. A copy of the 8-point file with one gate changed from an addition to a subtraction
  was refused by Lean. A copy of the statement with the bound 20 changed to 19 was refused by
  `Compare.lean`.
- The statement says that a circuit of that size exists. For 8 points the circuit is data in the file. Above
  8 points the proof builds it by tensor products inside Lean's logic, and no gate list is written out. The
  gate lists up to 512 points are the text files of `tools/circuits/programs/`, checked by Python.
- No person has reviewed the Lean files.

**Not stated in Lean.** Sizes that are not powers of 8. The scaled transform in natural order (the file has
it for the tensor power only, as `cost_power_half_H`). Anything in count (G): OpenAI's model has no gate
a·u + b·v, so a second gate type would have to be defined, and that would no longer be OpenAI's model. The
7/8 family: it is not a tensor power of a smaller circuit, so its proof would have to follow the recursion
of the generator.

## 7. What was searched in the literature

The search was made by the agents, in three rounds, on 10 and 11 October 2026. The two older papers were read
by the AI agents, from copies I obtained. Coppersmith, Feig and Linzer (1994) has two pages, and both were
read. Of Grigoryan and Agaian (2000) the agents read page 172 (the introduction) and pages 178 to 183: the
comparison tables, the paragraph on the Hadamard transform, the conclusions, and the appendix with the proof
of the count and the programs. Pages 173 to 177 were not read. By the outline on page 172 they hold the
part on the Fourier transform and also the section that sets out the algorithm for the Hadamard transform.
So the algorithm is taken here from pages 179 to 181: the paragraph on its count, the proof of the count and
the program.

What else was read or searched:

- every paper that the citation indexes list as citing Alman and Rao (15 items) or the 1994 paper of
  Coppersmith, Feig and Linzer (26 items), most of them by title and abstract;
- the text of Alman and Rao's paper, of Feig's survey chapter of 1999, of Voronenko and Püschel (2007), and
  of one conference paper of 2003 on Hadamard matrices of other orders;
- the statements of Alman's paper of 2021 on circuits counted in wires, in its source text, and a paper of
  2005 in which the first author of the paper of 2000 describes its algorithm;
- about thirty queries to arXiv and about thirty web searches, among them searches for 8 points in 19, 20 or
  21 additions and for an exact minimum at small sizes;
- seven patents, through a tool that summarises pages.

What came out:

- Nothing I found has 8 points below 22 operations, 16 points below 56, a rate below 7/8 with free
  constants, or a rate below 23/24 with every operation charged.
- The 22 at 8 points appears twice. The formula of Coppersmith, Feig and Linzer for odd powers of two,
  (7/8) N log2 N + N/8, gives 22 at 8 points (page 969; they print the formula, not the number). The 8-point
  step of Alman and Rao (2023) uses 22 additions or subtractions and one halving, which is 22 operations
  when the halving is free and 23 when it is counted.
- The rate 7/8 with free halvings is in print twice as well: in the 1994 paper, and in Section 6.1 of Alman
  and Rao, who build a second algorithm from a 4-point step with 7 additions or subtractions and one halving
  and say that it does not use fewer operations in total than the textbook.
- The 1994 paper has no circuit of its own at 8 or 16 points, claims no lower bound, and does not say
  whether 7 is the least at 4 points. One of its authors wrote in 1999 that the 4-point result "has not been
  extended, and it may in fact be rather hard to extend except in most trivial (and uninteresting) ways"
  (Feig, 1999). The 8-point and 16-point circuits of this note are below the formulas of the 1994 paper in
  that paper's own count (section 2).
- No exact minimum for 8 or 16 points was found in print, in either count.

**The count stated by Grigoryan and Agaian (2000).** Their paper states that its algorithm computes the
Hadamard transform on N = 2^r points with 6·2^r - r^2 - 3r - 6 additions and subtractions (page 181). Its
abstract says that the algorithm "uses on the average no more than six operations of additions per sample".
That count is too small. The algorithm applies a "paired transform" of length N, which costs 2N - 2
additions and subtractions and splits the transform into transforms of lengths N/2, N/4, ..., 2, 1. These
are computed the same way. The recursion that the algorithm follows,
T(N) = (2N - 2) + T(N/2) + T(N/4) + ... + T(1) with T(1) = 0, has the solution T(N) = N log2 N exactly.

| points | stated count | the recursion, which is N log2 N | (N/2) log2 N |
|---|---|---|---|
| 2 | 2 | 2 | 1 |
| 4 | 8 | 8 | 4 |
| 8 | 24 | 24 | 12 |
| 16 | 62 | 64 | 32 |
| 2,048 | 12,128 | 22,528 | 11,264 |
| 4,096 | 24,390 | 49,152 | 24,576 |
| 16,384 | 98,060 | 229,376 | 114,688 |

The stated count agrees with the recursion at 2, 4 and 8 points and is smaller from 16 points on (62 against
64). From 4,096 points on it is also below (N/2) log2 N (24,390 against 24,576). That number is a lower
bound for circuits of additions and subtractions, by the determinant argument of Morgenstern (1973) as Alman
and Rao quote it; and the paper's own introduction gives 0.5 N log N as a lower bound for the Hadamard
transform (page 172). So the algorithm, as the program on page 181 carries it out, has the textbook count in
another order, and the count stated in the paper is not a count below N log2 N.

How this was checked. `python3 -B tools/circuits/ga_count.py` prints the three columns for 2 to 16,384
points. The paper does not print the recursion; the agents wrote it down from the description of the
algorithm on pages 179 to 181. A second check agrees with it: programmed from the description that the
paper's first author gives in a later paper (Grigoryan and Bhamidipati, 2005), the algorithm used exactly
N log2 N additions and subtractions at every size that was run, 2 to 4,096 points. That program is not in
this repository. Frigo and Johnson (2007) commented on the same paper's algorithm for the Fourier transform.
Their comment is known here from its abstract, and this note says nothing about the Fourier counts of the
paper.

What was not read, and so limits the word "new":

- **Most of a survey by Sergeev (2025)**: pages 50 to about 170. Its contents list a section called "Linear
  circuits for Sylvester matrices".
- **Papers by Sarukhanyan, Agaian, Astola and Egiazarian (2002 to 2011)**, known from their abstracts apart
  from one conference paper. Their abstracts say that their method beats the classical transform from order
  96 on. As far as I can tell they are about Hadamard matrices of other orders.
- **The circuit papers that count wires.** Alman (2021) states circuits with (1.81 + o(1)) N log2 N wires,
  with gates of any number of inputs. That is a third count. These papers were read in part only, but the
  agents converted their constructions into count (G) exactly: a gate with f inputs becomes f - 1 operations.
  The best that comes out is the rate 7/8, from the 4-point block, and it is the 1994 circuit again. Every
  other construction that was converted is above the textbook. This is a computation by the agents that no
  person has reviewed. It converts the published circuits as they are, and does not exclude that a new
  circuit built on their ideas does better. Alman and Rao write of that paper that its algorithms "do not
  give improved arithmetic operation counts".
- The paper of Samadi and others (1998) is known from its abstract, and Morgenstern's paper (1973) as Alman
  and Rao quote it. One index, DBLP, was not searched. Literature in Russian, Chinese and Japanese was seen
  only as far as the indexes returned it.
- No specialist has read this work.

If you know a smaller count in print, I would be glad to hear of it and will credit it here.

## 8. The files

The circuits, the programs that check them and the programs that found them are in `tools/circuits/`. Its
`README.md` describes each file.

- **The one command**, run from the top folder of the repository: `python3 -B tools/circuits/run.py`. It
  needs Python 3.9 or later and its standard library, about a minute and about 700 MB of memory. It reads
  every circuit from its text file, checks it against the definition of the transform in exact arithmetic,
  prints the tables, writes `H8Half.lean` again from the 20-line program and compares it with the file in
  `lean/Work/SmallWHT/`. Its last line is `OK ...` or `FAILED:` with the first difference.
  `expected-output.txt` is what it printed in the recorded run.
- **The circuits as text**, in `programs/`: `h4_7gates.txt`, `h8_19gates.txt` (the 19 lines of section 2),
  `h8_half_20ops.txt` (the count-(O) version), `h16_52gates.txt`; the circuits exactly as the searches left
  them, in `as_found/`; and what the generator writes, in `generated/`.
- **The checker and the generator**: `slp.py` defines the text format and the two counts and checks a
  circuit exactly; `gen.py` states the constructions as recursions and writes the circuits; `tables.py`
  regenerates, replays and prints the tables.
- **Two small checks for the comparison with the older papers**: `multiply_add_check.py` shows that every
  line of every circuit file is one operation of the 1994 paper, and `ga_count.py` prints the table of
  section 7.
- **The search programs**, in `search/`, as they were run, with a README that says for each what it
  searches, what it found, how long it takes and what it does not show.
- **The circuits as working programs**, in `fast/wht56/`: pure Python, numpy and C, with their tests and
  the plain C timings of section 5. The timings against FFHT are in `fast/wht56/results/ffht/`: the tables
  by size, the patch against FFHT's generator, the timing programs and their raw outputs. No file of FFHT
  is included.
- **The circuits as hardware**, in `fpga/`: the generator of hardware descriptions, the designs, the
  scripts for the open-source tools, the result tables of section 5, and the sources of the self-test.
- **For Lean**, in `tools/circuits/lean/`: the 20-line program and the program that writes `H8Half.lean`
  from it. The Lean project itself is the folder `lean/` at the top of the repository.

[explicit-circuits.json](explicit-circuits.json), beside this note, has the figures of this note in
machine-readable form, each marked as checked by Lean or as computed in Python.

## 9. What has not been tried, and one thing that was

- Lean statements for count (G), for the 7/8 family, and for sizes that are not powers of 8.
- The exact minimum at 8 points. It is between 15 and 19. The 15 is the lower bound of the paper, whose
  proof no person has read (section 5).
- 16 points beyond local searches, in either count. In count (O) a 16-point circuit would need 53 operations
  or fewer, up to a common factor, to beat the rate 5/6 when it is used in layers. The best known has 56.
  Nobody has searched for one directly, and nothing shows that 53 is impossible.
- Timing beyond section 5. The step is now timed inside a tuned library, FFHT, on one machine, and it was
  not faster there. Still untried: a second family of processors (one on which additions and multiply-adds
  run on different units, an ARM processor, one with wider vector instructions); a second compiler; several
  threads; the larger circuits of the family, of which only the 8-point member was timed.
- A form of the step with a shorter chain. The 8-point step has a chain of 7 operations (6 with fused
  multiply-add) where the textbook has 3. Nobody has searched for a circuit with fewer than 24 operations
  and a shorter chain. The test of one pass alone says what a 20-operation block with a chain of 3 would
  be worth on that machine: 15 to 16 % of a pass.
- Hardware beyond section 5. One open-source tool chain, two chip families of one maker after packing, no
  measurement of speed or power, nothing in custom silicon. Still untried: a search for a circuit with few
  adder levels, or one that is small in real logic cells and not only in adders; registers placed by hand
  or by a search; a chip maker's own tools; any real design. No existing design was changed.
- The same question for the Fourier transform. Alman and Rao's paper turns a count for this transform into
  a count for the Fourier transform; my count has not been put through that.
- A lower bound for count (O). Nothing here says that 5/6 is the best possible.
- Reading the texts named at the end of section 7.

**Tried on 11 October 2026, with nothing found: the family together with the 8-point circuit in count (O).**
The family has the better rate when constants are free (3/4), and the 8-point circuit has the better rate
when every operation is charged (5/6), so the agents tried to combine them. Six ways of mixing levels of the
family with layers of the 8-point circuit were built and replayed exactly up to 512 points, and by one
program up to 4,096. For the exact transform, from 64 points on, every mix that is not just the layers
costs more than the layers. At 16 points the best block still has 56 operations.

For the family's own wiring there is an argument that count (O) cannot go below (7/8) N log2 N however its
values are scaled. The family saves by using one value at two levels, once as it is and once doubled. When
doubling is charged, that forces one more halving for each hub on every second level, and 3/4 becomes 7/8.
The least count for that wiring was computed exactly at 4, 8, 16, 32 and 64 points, and it agrees with the
argument: at 16 points it is 60 up to a common factor and 76 for the exact transform, against 56 and 72 by
layers. At 8 points, and at 16 points up to a common factor, three programs written separately agree.

Status: an argument and computations by the AI agents, made in one morning; not in Lean; read by no person.
The programs are not in this repository. It covers the family's wiring and those six mixes. It does not
show that no other circuit beats 5/6.

## 10. Sources

The literature was read and searched on 10 and 11 October 2026. Section 7 says who read what.

- D. Coppersmith, E. Feig, E. Linzer, "Hadamard transforms on multiply/add architectures", IEEE Transactions
  on Signal Processing 42(4), pages 969 to 970, 1994, doi 10.1109/78.285664. Both pages.
- E. Feig, "Complexity theory of transforms in signal processing", chapter 9 of the Digital Signal
  Processing Handbook, CRC Press, 1999. The source of the sentence quoted in section 7.
- Y. Voronenko, M. Püschel, "Mechanical derivation of fused multiply-add algorithms for linear transforms",
  IEEE Transactions on Signal Processing 55(9), 2007, doi 10.1109/TSP.2007.896116. It describes the 1994
  circuit.
- S. Samadi, Y. Suzukake, H. Iwakura, "On automatic derivation of fast Hadamard transform using genetic
  programming", IEEE APCCAS 1998, pages 327 to 330, doi 10.1109/APCCAS.1998.743763. Known from its abstract.
- E. Reshef, I. Alrod, "Reduced complexity fast Hadamard transform", US patent 7,003,536, filed 15 August
  2002. Read through a tool that summarises pages.
- J. Alman, K. Rao, "Faster Walsh-Hadamard and Discrete Fourier Transforms From Matrix Non-Rigidity",
  STOC 2023, pages 455 to 462, doi 10.1145/3564246.3585188; arXiv:2211.06459, version 2: Theorem 1.1 (the
  bound), Section 2.2, Section 6.1, and Theorem 6.2 with its proof (the exact count).
- A. M. Grigoryan, S. S. Agaian, "Split manageable efficient algorithm for Fourier and Hadamard transforms",
  IEEE Transactions on Signal Processing 48(1), pages 172 to 183, 2000, doi 10.1109/78.815487. Pages 172 and
  178 to 183; see section 7.
- A. M. Grigoryan, V. S. Bhamidipati, "Method of flow graph simplification for the 16-point discrete Fourier
  transform", IEEE Transactions on Signal Processing 53(1), pages 384 to 389, 2005. Read in the
  copy that its first author keeps on his university's web pages. It describes the algorithm of the paper
  of 2000.
- M. Frigo, S. G. Johnson, IEEE Transactions on Signal Processing 55(4), 2007, doi 10.1109/TSP.2006.889087.
  Known from its abstract.
- I. S. Sergeev, "Etudes on the methods of designing efficient circuits", survey, version of 28 May 2025.
  Pages 1 to 49.
- J. Alman, "Kronecker products, low-depth circuits, and matrix rigidity", arXiv:2102.11992 (2021). Its
  statements were read in the source text. J. Alman, Y. Guan, A. Padaki, "Smaller low-depth circuits for
  Kronecker powers", arXiv:2211.05217 (2022): abstract and introduction.
- S. Agaian, H. Sarukhanyan, K. Egiazarian, J. Astola, "Williamson-Hadamard transforms: design and fast
  algorithms", ICEST 2003. Read in full. Their papers of 2002, 2003 and 2005 and the book "Hadamard
  Transforms" (SPIE, 2011): abstracts or records.
- J. Morgenstern, "Note on a lower bound on the linear complexity of the fast Fourier transform", Journal of
  the ACM 20 (1973). Known through Alman and Rao and through OpenAI's preprints.
- OpenAI, "Finite tensor savings and exact Fourier circuits" and "An explicit power saving for the exact
  discrete Fourier transform", both of 25 September 2026, in [openai/math](https://github.com/openai/math).
  The gate set of count (O) is that of `lean/OAI/Computability/FourierCircuit/Core.lean`.
- The indexes used: OpenAlex, Crossref, Semantic Scholar, OpenCitations, the arXiv API, Google Scholar,
  Google Patents.
- For the timings of section 5: FFHT, <https://github.com/FALCONN-LIB/FFHT>, at commit
  `fba727a3ff72c862260460631ae1cc8e3e44e861` (10 March 2019, its last), under the MIT License; gcc 13.3.0.
  No file of FFHT is in this repository.
- For the hardware figures of section 5: the open-source suite oss-cad-suite, release 2026-10-11, with
  Yosys 0.69+274 and nextpnr 0.11.1-59; the chips Lattice iCE40HX8K (package CT256) and Lattice ECP5; the
  8-point module `hadamard_trans_1d` of xk265, <https://github.com/openasic-org/xk265>, at commit
  `832e564a8e59dd90a18fb7ee8e2ed87d96aa03bc`, file `rtl/fme/fme_satd_8x8.v`, of which no file is in this
  repository. `tools/circuits/fpga/README.md` has the conditions of every figure.
