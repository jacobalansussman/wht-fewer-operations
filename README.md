# The Walsh-Hadamard transform with fewer operations

**In short.** This repository holds small *circuits* (fixed lists of operations) for the Walsh-Hadamard
transform that need fewer operations than the textbook method, and it reports where that helps and where it
does not.

| what | the gain, and against what | checked by |
|---|---|---|
| **Proved**, with every addition, subtraction and multiplication by a constant counted as one | the exact transform on N = 8^j points in at most (5/6) N log2 N + N operations, against the textbook's N log2 N and Alman and Rao's 23/24 (2023), the smallest c that I found in print for a count of the form c·N log2 N plus a multiple of N; below the textbook from 512 points | Lean, a program that checks proofs |
| **Counted, with doublings free**, as they are for the adders of a chip | 19 operations at 8 points, against the textbook's 24 and the 22 in print; a family of circuits with (3/4) N log2 N + N/4, against the 7/8 in print (Coppersmith, Feig and Linzer, 1994) | Lean, for the bound (3/4) N log2 N + N/4 at every power of two and for the 19 at 8 points; exact replay by programs up to 16,384 points |
| **Measured on a chip** | built for an FPGA (a chip whose logic is set by loading a file into it) as one block of adders with no registers inside, the 8-point circuit takes 19 % to 21.5 % fewer logic cells than the textbook design on a Lattice iCE40, and the family 17.5 % to 23.1 % fewer from 16 to 256 points, by the same tools' counts; on a board it gave the same outputs as the textbook circuit on 597,750,000 test inputs | open-source chip tools; one board run |
| **Measured on processors** | at best a few percent less time in the main test: 5-6 % on an AMD Zen 4 server processor and 0-2 % on an AMD Zen 5, against the best textbook code I could write in the same program. Before the runs I set the bar for a gain worth pursuing at 10 % less time; neither reaches it. In 512-bit code on Zen 4, 4-11 % less time from 2^12 points, past the bar at one size, in two runs on one machine. No gain on AMD Zen 2, on a GPU, or on Zen 4 and Zen 5 at the sizes most libraries use; slower on an older Intel processor | exactness checked first; one timing run per chip (two for the 512-bit code on Zen 4), on rented cloud machines; the Zen 4 and Zen 5 results not yet read by a second agent |

**Not gained on paper.** It is a better constant, not a better order: counts that grow more slowly than
N log2 N are known, though they give no gain at the sizes anyone computes. With every operation charged, the
gain starts only at 512 points: 8 points cost 28 against 24, and 64 points cost the same as the textbook.
The two results do not combine (the 3/4 family becomes 7/8 when doublings are charged). Nothing here is
known to be the best possible.

**The price, also measured.**

- The circuits are twice as deep, so the chip's highest clock is lower: about 72 against 97 MHz at 8 points,
  by the tools' estimates.
- They are larger than the textbook design once registers are added for speed.
- At 8 points Alman and Rao's 22-adder step is smaller on the iCE40.
- On a Xilinx Artix-7 chip they took more space than the textbook once placed, in three of the four settings
  tried (about the same in the fourth).
- Put into the tuned library FFHT in place of its own step, on the one machine I timed for the first
  version, the new step did not make it faster at any size: it took 1 % to 24 % more time up to 2^19 points.
- My first speed figure for this revision, 11-15 % less time on AMD Zen 5, was wrong. The textbook code I
  compared against made the compiler add up to 12 needless copy instructions to each 8-point step. Written
  without them, the difference on that chip is 0-2 %, too small for one run to establish.

So this is a result about operation counts, with a measured saving in chip area in one kind of design, and
not a faster program: on processors the best I measured in the main test is a few percent, in one run per
chip, and in 512-bit code on Zen 4 it is 4-11 % from 2^12 points, in two runs on one machine.

**Who did what.** I directed this work. The circuits were found by computer searches that AI agents
(Anthropic's Claude) wrote and ran. The same agents wrote the programs, the Lean proofs, the timing programs
and these pages. No person has yet read the Lean files or the programs, or checked the proofs, line by line.
The builds, the checks, the timings and the hardware measurements reported on these pages were run by the
agents, at my direction, on a Mac mini of mine and on a Linux machine that I rented, and, on 22 October 2026,
on virtual machines rented through Google Colab.

**Where to go next.** [docs/UNDERSTAND.md](docs/UNDERSTAND.md) explains the result in ten short steps, each
with a check to do by hand. Then: [what is counted](#what-is-counted) ·
[check it yourself](#check-it-yourself) · [what is proved](#what-is-proved-and-what-is-not) ·
[the kernel](tools/fht-kernel/README.md) (not yet timed as a library) ·
[the measurements of 22 October](measurements/2026-10-22/README.md) · [open directions](#open-directions).
The sections below give each of these statements with its conditions.

## What is counted

The Walsh-Hadamard transform turns N numbers into N sums of those numbers, each with its own pattern of plus
and minus signs. N points means a list of N numbers. The textbook program computes it with N log2 N additions
and subtractions. I say *exact* for the outputs themselves, as against all outputs multiplied by one common
factor.

A *circuit* is a fixed list of lines. Each line makes one new value from the inputs or from earlier values,
and a value can be used again as often as needed. I count the lines in two ways, and every number on this page
belongs to one of them. I call them count (O) and count (G). The letters are only labels; O is the count of
the circuit model of OpenAI's repository.

| | count (O): every operation charged | count (G): doublings free |
|---|---|---|
| an addition or a subtraction of two values | 1 | 1 |
| a doubling or a halving of a value | 1 | 0: it is folded into the line that uses it |
| a line a·u + b·v, with constants a and b | 1, plus 1 for each constant other than +1 or -1 | 1 |
| the multiplication of every output by 2^j at the end of the 5/6 circuit | 1 for each output, N in all | 0 |
| where it is the natural count | the circuit model of OpenAI's repository openai/math (see "Relation to OpenAI's family 130"), the Lean proof of the 5/6 count, and Alman and Rao's paper | the adders of a chip, where a doubling only moves wires; processors with a fused multiply-add; the Lean proof of the 3/4 count, which charges one for each line ±u ± c·v |

In count (O) a constant can be any number; nothing bounds its size. Every constant in my circuits is a power
of 2 with a sign (1, 2, 1/2 or 2^j). So in count (G) nothing is free except doublings and halvings, and
count (O) is the same as "doublings charged".

The 1994 paper of Coppersmith, Feig and Linzer has a third count: one *multiply-add* (one value plus or minus
the product of two others) is one operation, and a multiplication on its own is one too. Every line of my
count-(G) circuits has two terms and at most one constant, so their count of my circuits is count (G). The
section "A second way of counting" has the details.

A classical result of Morgenstern (1973), which I know from later papers' statements of it, says that if
every constant has absolute value at most 1, the
Fourier transform needs at least (1/2) N log2 N operations, and the same argument gives the same bound for
this transform. Every count on this page is above that, so the result does not rule any of them out. It also
does not cover my exact circuits as they stand: their last step multiplies every output by 2^j, a constant
that grows with N.

## The count, and how it compares

This repository has a circuit that computes the exact transform on N = 8^j points (8, 64, 512, 4,096 and so
on) with at most (5/6) N log2 N + N operations, where every addition, every subtraction and every
multiplication by a constant counts as one. That count is proved in Lean, a program that checks proofs.

| points | textbook, N log2 N | Alman and Rao (2023), their exact count | this repository |
|---|---|---|---|
| 8 | 24 | 30 | 28 |
| 64 | 384 | 431 | 384 |
| 512 | 4,608 | 4,927 | **4,352** |
| 4,096 | 49,152 | 51,199 | **45,056** |

**It is a better constant, not a better order.** The number in front of N log2 N goes
from 1 to 5/6 and stays there however large N is. The count is below the textbook from 512 points on. Among
counts of the form c·N log2 N plus a multiple of N, with every operation charged, the smallest c I found in
print is 23/24, by Alman and Rao (2023). Their count first goes below the textbook at 16,777,216 points.

A better *order* (or exponent) would be a count that falls below every fixed fraction of N log2 N as N grows,
such as N (log2 N)^0.999. This is not that. Counts of that kind are known. In the same circuit model,
OpenAI's family 130 (the part of its repository openai/math titled "Exact Fourier transforms below
n log n") proves that the Fourier transform has circuits with fewer than c·n log2 n operations for
every c > 0, at some very large lengths that it does not name. For this transform, my repository
[wht-power-saving-lean](https://github.com/jacobalansussman/wht-power-saving-lean) proves in Lean a count of
order N (log2 N)^z with z = 1 - 1.57e-3, in OpenAI's model of a computer with memory. So in the limit the
number in front of N log2 N can be made as small as you like. Those results give nothing at any size anyone
computes: their hidden constants are far too large. This repository is about explicit circuits, with
exact counts at sizes you can write down.

| construction, every operation charged | first size below the textbook |
|---|---|
| this repository, 5/6 | 512 points (above it at 8, 16 and 32; equal at 64, 128 and 256) |
| Alman and Rao, their exact count | 16,777,216 points (the bound of their Theorem 1.1: 134,217,728) |
| OpenAI's family 130, and the results in a model of a computer | no size known: they prove existence, or an order of growth, only |

**At 8 points alone it is not a gain.** The exact 8-point transform costs 28 operations here, against the
textbook's 24. The reason is in how the circuit works. It computes the eight outputs *halved*, in 20
operations where the textbook needs 24. Putting the factor right costs one multiplication for each output.
At 8 points that is 8 more, so 28. On N = 8^j points the circuit is used in j layers (one layer runs it once
on every group of 8 numbers; step 7 of docs/UNDERSTAND.md), and the factor is put right once, at the very
end. Each layer saves N/2 operations and the end costs N. So at 64 points (j = 2) the count equals the
textbook's, and from 512 points (j = 3) on it is below.

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

## A second way of counting: 19 operations at 8 points, and the rate 3/4

Count (G), defined in "What is counted", charges one for each line a·u + b·v with constants a and b, so
that multiplying by a constant is free; some machines do such a line in one instruction. In count (G):

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
lower bound, and I do not claim that my counts are the least possible. "In print" here means in the
literature I searched. That search did not cover the hardware literature on shift-and-add synthesis of
constant matrices, whose tools count adders the way count (G) does (see [open directions](#open-directions),
item 2).

Status: proved in Lean, at every power of two. The theorem `MultiplyAdd.hadamard_mulAdd_circuit` says that
for every k there is a circuit on N = 2^k inputs whose outputs are exactly the transform of the inputs, with
at most (3/4) N log2 N + N/4 lines. In that theorem a line is one multiply-add ±u ± c·v, with u and v inputs
or earlier lines and c a constant, and it costs one; a multiplication on its own costs one too. So each line
is one operation of the 1994 paper and one line of count (G), and the bound holds in both counts. The numbers
may be in any commutative ring: the whole numbers, the rationals, the real and the complex numbers among
them. The definitions are those of OpenAI's circuit model, with this line as the gate. The statement alone is
the 91-line file `lean/Work/WHT34/ChallengeWHT34.lean`, which uses nothing but Mathlib. The 19 lines at
8 points are proved in Lean as well (`hadamard_eight_19` in `lean/Work/WHT34/ChallengeWHT34Checks.lean`).
Every circuit up to 16,384 points was also replayed exactly by the Python programs (the two largest sizes
with `run.py --kmax 14`). Before the Lean proof, the count of the family for larger N rested on a short
induction, written in the first lines of `tools/circuits/gen.py`, which the agents checked and no person has
read; no person has read the Lean files either.

The two results have not been combined. With every operation charged, the rate of the family is 7/8, which
is worse than 5/6: for the exact transform at 64 points it costs 416 operations, against 384 by layers of
the 8-point circuit. On 11 October the agents tried six ways of mixing the two constructions in count (O)
and found nothing below 5/6. They also have an argument about the family alone: if its lines are kept as
they are, and only the power of 2 at which each value is held is changed, the rate cannot go below 7/8 in
that count. This is an argument and computations by the agents, not in Lean. Nobody has searched directly
for a 16-point circuit that gives the transform up to a common factor in 53 operations or fewer of
count (O). The best known has 56. With 53, layers of it would beat 5/6.

## Exact counts from 8 to 32,768 points

Every cell is the exact transform H x. In each row the smallest count is in bold. "(Lean)" marks the sizes
that the Lean theorem of the first count covers (the powers of 8). In the first table every entry of the
column "3/4 family" is also an upper bound proved in Lean, and so is the 19 at 8 points.

**Doublings free: count (G), the number of adders in hardware.**

| points | textbook | Coppersmith, Feig and Linzer (1994) | Alman and Rao (2023) | 5/6 circuit | 3/4 family |
|---:|---:|---:|---:|---:|---:|
| 8 | 24 | 22 | 22 | **19** | 20 |
| 16 | 64 | 56 | 60 | 54 | **52** |
| 32 | 160 | 144 | 152 | 140 | **128** |
| 64 | 384 | 336 | 352 | **304** | **304** |
| 128 | 896 | 800 | 832 | 736 | **704** |
| 256 | 2,048 | 1,792 | 1,920 | 1,728 | **1,600** |
| 512 | 4,608 | 4,096 | 4,224 | 3,648 | **3,584** |
| 4,096 | 49,152 | 43,008 | 45,056 | 38,912 | **37,888** |
| 32,768 | 491,520 | 434,176 | 450,560 | 389,120 | **376,832** |

**Doublings charged: count (O), OpenAI's circuit model.**

| points | textbook | Coppersmith, Feig and Linzer (1994) | Alman and Rao (2023) | 5/6 circuit | 3/4 family, rescaled | 3/4 family, each doubling charged |
|---:|---:|---:|---:|---:|---:|---:|
| 8 | **24** | 28 | 30 | 28 (Lean) | 34 | 32 |
| 16 | **64** | 80 | 77 | 72 | 76 | 84 |
| 32 | **160** | 192 | 187 | 176 | 192 | 208 |
| 64 | **384** | 480 | 431 | **384** (Lean) | 416 | 496 |
| 128 | **896** | 1,088 | 991 | **896** | 992 | 1,152 |
| 256 | **2,048** | 2,560 | 2,239 | **2,048** | 2,112 | 2,624 |
| 512 | 4,608 | 5,632 | 4,927 | **4,352** (Lean) | 4,864 | 5,888 |
| 4,096 | 49,152 | 61,440 | 51,199 | **45,056** (Lean) | 48,128 | 62,464 |
| 32,768 | 491,520 | 606,208 | 503,807 | **442,368** (Lean) | 483,328 | 622,592 |

What each column is, and who stated it (k = log2 N):

| column | the circuit | formula | who stated it |
|---|---|---|---|
| textbook | k layers of butterflies | N k | folklore |
| Coppersmith, Feig and Linzer, doublings free | their 4-point circuit as printed on their page 969, applied along each pair of address bits, then one textbook layer if k is odd | (7/8) N k, plus N/8 if k is odd | their formulas |
| Coppersmith, Feig and Linzer, doublings charged | the same circuit with each doubling charged: 10 operations per 4-point block | 10 (N/4) (k div 2) + N (k mod 2) | my reading; they never counted this way |
| Alman and Rao, doublings free | their 8-point step (22 additions or subtractions, one halving) along each group of three address bits, with textbook layers for the bits left over, as in their proof | (11/12) N k + (N/12) (k mod 3) | my reading of their circuit |
| Alman and Rao, doublings charged | not built: they apply their input doublings once, and layering their step would charge them in every layer | (23/24) N k + (N/24) (k mod 3) + N - 1 | their total, in the proof of their Theorem 6.2 |
| 5/6 circuit, doublings charged | the 20-operation 8-point step along groups of three bits, textbook layers for the bits left over, then N final multiplications | N (k - m/2 + 1) with m = k div 3; that is (5/6) N k + N when 3 divides k | this repository; Lean for N = 8^j |
| 5/6 circuit, doublings free | the same circuit, which is layers of the 19-operation circuit with no scaling | 19 (N/8) (k div 3) + N (k mod 3) | this repository |
| 3/4 family, doublings free | the family | (3/4) N k + N/4 | this repository; Lean, as an upper bound, for every N = 2^k |
| 3/4 family, rescaled | the family with halvings in place of doublings, then N multiplications | (7/8) N k + N/4 + N when k is even; (7/8) N k + 5N/8 + N when k is odd | this repository; this is the "7/8 when doublings are charged" above |
| 3/4 family, each doubling charged | the count-(G) circuit itself, counted in count (O) | no formula claimed | computed |

At the sizes that libraries often use, 64 to 256 points, the family takes 20.8 % to 21.9 % fewer operations
than the textbook when doublings are free; when they are charged, the 5/6 circuit only ties the textbook
there, and the family is above it. The charged column for the 1994 circuit is an unkind reading of a
circuit made for machines with a multiply-add; its authors never gave it.

`python3 -B tools/circuits/count_tables.py` builds every one of these circuits up to 4,096 points, counts it
with the repository's own counter, checks it on random whole-number inputs, and checks that the count equals
the formula. It writes no file. A run that also builds 32,768 points is recorded beside it in
`tools/circuits/expected-output-count-tables.txt`. This check ties each number to a circuit; it is weaker
than `run.py`, which checks every circuit on every unit input.

## What is proved, and what is not

**Proved in Lean.** Two results. The first is one statement, in two forms. The theorem
`OAI.ExactFourier.WHT8Half.hadamard_pow8_circuit` says: for every j there is a circuit on 8^j inputs that
computes the exact Walsh-Hadamard transform and has at most 20·j·8^(j-1) + 8^j gates. That number is
(5/6) N log2 N + N. A *gate* is one addition, one subtraction or one multiplication by a constant, in the
circuit model of OpenAI's repository openai/math. The theorem `hadamard_pow8_circuit_real` states the same
with the bound written as (5/6) N log2 N + N. The statement alone, without proof, is the 93-line file
`lean/Work/SmallWHT/ChallengeWHT8.lean`. Lean reports that both theorems depend only on its three standard
axioms, `propext`, `Classical.choice` and `Quot.sound`.

The second is the count with doublings free. The theorem `MultiplyAdd.hadamard_mulAdd_circuit` says: for
every commutative ring and every k, there is a circuit on 2^k inputs that computes the exact Walsh-Hadamard
transform with at most (3k·2^k + 2^k)/4 lines, each one multiply-add ±u ± c·v. That number is
(3/4) N log2 N + N/4. The statement alone, without proof, is the 91-line file
`lean/Work/WHT34/ChallengeWHT34.lean`. Lean reports that the theorem depends only on its three standard
axioms. Beside it, `ChallengeWHT34Checks.lean` proves on the same definitions that the 19 lines at 8 points
and the 1994 paper's 4-point circuit compute the transform, and that every circuit for the transform in this
model has at least N lines, from 2 points on, when 2 is not 0.

**Replayed exactly by programs, not in Lean.**

- The gate lists themselves above 8 points. Lean proves that a circuit of that size exists; it writes out
  the 20 gates for 8 points and no list for larger sizes. The lists at 64, 512 and 4,096 points are text
  files or are generated, and `run.py` checks each one on every input that is 1 in one place and 0
  elsewhere, in exact arithmetic. That settles every input, because each line only adds, subtracts or
  multiplies by a constant.
- Sizes that are not powers of 8. With a textbook layer for each binary digit left over, the count is below
  the textbook at every power of two from 512 on: for example 9,728 against 10,240 at 1,024 points.
  Replayed up to 16,384 points (`run.py --kmax 14`, below). Beyond that it rests on a short argument
  (Corollary 2 of [the paper](paper/explicit-wht-circuits.pdf)), which the agents wrote and no person has
  checked.
- In the second count, the circuit files above 8 points and the family's count with every operation
  charged (rate 7/8). Lean proves that circuits of at most the stated sizes exist; it writes out the 7 lines at
  4 points and the 19 at 8 points, and no list for larger sizes.

**Claim by claim.**

| claim | sizes | status | how to check |
|---|---|---|---|
| the exact transform in at most 20 j 8^(j-1) + 8^j operations, count (O): `hadamard_pow8_circuit` | N = 8^j, every j | **Lean** | `sh lean/check.sh` |
| the same bound written as (5/6) N log2 N + N: `hadamard_pow8_circuit_real` | N = 8^j | **Lean** | the same |
| 4,352 operations at 512 points: `hadamard_512_circuit` | 512 | **Lean**; its axioms are printed by the build, but the comparison script does not compare it | the same |
| the 20 operations of the 8-point circuit compute the transform halved | 8 | **Lean**; the gates are data in `H8Half.lean`, written by a program from the text file | the same |
| the gate lists of the 5/6 circuit | 64, 512 and 4,096 | **programs** | `python3 -B tools/circuits/run.py` |
| count (O) at the powers of two that are not powers of 8; below the textbook from 512 points | 2^k | **programs** up to 16,384 points; beyond, Corollary 2 of the paper, the agents' proof, read by no person | `run.py --kmax 14` |
| 19 operations at 8 points, count (G): `hadamard_eight_19` | 8 | **Lean**, on the definitions of the statement file itself; and **programs** | `sh lean/check.sh`; `run.py`; `python3 docs/walkthrough.py all` |
| at most (3/4) N log2 N + N/4 lines, each one multiply-add, count (G) and the 1994 count: `hadamard_mulAdd_circuit` | every 2^k | **Lean**; also **programs** up to 16,384 points | `sh lean/check.sh`; `run.py` |
| the family with every operation charged, rate 7/8 | powers of 4 | **programs** up to 16,384 points | `run.py` |
| every count-(G) line is one multiply-add of the 1994 paper | all circuit files | **program** | `python3 -B tools/circuits/multiply_add_check.py` |
| the lower bound 2N - 1 operations, in either count | every N | **paper**, Proposition 6: the agents' proof, read by a second agent, two of its steps checked by a program at 4 and 8 points; read by no person | `paper/lowerbound_check.c` |
| the count-(G) circuits need at least 0.3155 N log2 N operations | every N | **argument** by the agents ([the note](notes/explicit-circuits.md), section 5); not reviewed, not in Lean | none |
| the family's wiring cannot go below 7/8 in count (O), however its values are scaled | computed at 4 to 64 points | **argument and computations** by the agents (the note, section 9); not in Lean | none: those programs are not in this repository |
| Grigoryan and Agaian's stated count is too small | 2 to 16,384 points | **program** | `python3 -B tools/circuits/ga_count.py` |
| the exact count tables above | the nine sizes | **programs**; the charged column of Alman and Rao is their published total, and two columns are my readings of other people's circuits | `python3 -B tools/circuits/count_tables.py` |
| times, logic cells, the board run | as stated | **measurements**, not proofs | their own pages |

**Limits of the Lean check.** The build was run from nothing once, on one rented Linux machine, on
11 October 2026. No person has yet read the Lean files, including the definition of the transform that the
statement uses. Two controls were run: a copy with one gate changed was refused by Lean, and a copy of the
statement with 19 in place of 20 was refused by the comparison script. Lean's official comparison tool was
not run on this folder. Revision 2 adds the seven files of the 3/4 count in `lean/Work/WHT34/`; the files of
the 5/6 count are unchanged. The whole Lean folder was built again for revision 2, as a new copy on each of two
Linux machines rented through Google Colab, where Lean and Mathlib's compiled files were already present
(VERIFY.md, "What was run"), and two controls were run on the new files: a copy with one constant 2 changed
to -2 was refused by Lean, and a copy of the statement with N/4 left out of the bound was refused by the
comparison script. Lean's official comparison tool was not run on the new files.

**Not claimed.**

- That 5/6 is the best possible. The best lower bound proved here is 2N - 1 operations, far below these
  counts (Proposition 6 of [the paper](paper/explicit-wht-circuits.pdf); the agents wrote its proof, and no
  person has read it); Lean proves only the weaker N lines (from 2 points on), in the model of the second
  count. Morgenstern's (1/2) N log2 N, for constants of size at most 1, is also below every count here.
- That the result is new. I searched; the section "Credit, and what is in print" says how far. It is a
  search, not a proof. I have not searched the hardware literature on shift-and-add synthesis of constant
  matrices, which counts adders the way the second count does.
- Any count for the Fourier transform. Alman and Rao's paper turns a count for this transform into one for
  the Fourier transform. My count has not been put through that.
- An asymptotic record. Counts of smaller order are known: OpenAI's family 130 in the same circuit model
  (for the Fourier transform, at lengths it does not name), and my wht-power-saving-lean for this transform
  in OpenAI's machine model. Neither gives anything at sizes anyone computes.
- That 19 operations is the least at 8 points.
- That all of the second count is in Lean. The bound (3/4) N log2 N + N/4 and the 19 at 8 points are;
  the lower bound 0.3155 N log2 N and the rate 7/8 with every operation charged are not. Corollary 2,
  which carries the first count to sizes that are not powers of 8, is the agents' argument, and no person
  has read it.
- That the Lean statement of the second count says which constants the circuits use. It allows any
  constant; the circuits use only ±1 and ±2.
- Peer review. The paper has not been reviewed and was not submitted anywhere.

What is not claimed about speed and hardware is listed in the sections
["Is it faster in practice?"](#is-it-faster-in-practice) and ["In hardware"](#in-hardware).

## Relation to OpenAI's family 130

The circuit model and part of the Lean proof come from OpenAI's family 130, "Exact Fourier transforms below
n log n", in [openai/math](https://github.com/openai/math), and in particular from its paper "Finite tensor
savings and exact Fourier circuits" (25 September 2026; community page:
<https://mathcommunity.github.io/oai-math-revised/papers/Finite-tensor-savings-and-exact-Fourier-circuits-September-25-2026/>).
That paper proves that the Fourier transform has circuits with fewer than c·n log2 n operations for every
c > 0, at some very large lengths. This repository is about a different transform, the Walsh-Hadamard
transform, and about explicit circuits at sizes people use. It uses three things of OpenAI's:

- the definition of a circuit and of its size, word for word (lines 25 to 62 of `ChallengeWHT8.lean` are
  lines 12 to 49 of their `ExactFourier.lean`);
- the 44 Lean files under `lean/OAI/`, unmodified, which hold the cost of a matrix and the rule for the cost
  of a tensor product;
- one theorem, repeated with its proof in `TensorPow8.lean`.

The Lean statement of the second count uses the same definitions with the gate replaced by a multiply-add
line and the complex numbers by any commutative ring; it imports none of OpenAI's files.

It uses none of the paper's main argument. The 5/6 proof is one new 20-gate circuit, OpenAI's rule for the
cost of a tensor product applied j times, and N final multiplications. The family's second paper, "An
explicit power saving for the exact discrete Fourier transform", works in a model of a computer with memory;
my repository wht-power-saving-lean is a Lean follow-up of it, and two files here come from that repository
(`lean/WHTCheck/Solution.lean` and `lean/tools/Compare.lean`; [NOTICE](NOTICE), section 3). **This
repository is not a project of OpenAI.**

## Check it yourself

Run these from the top folder, in a Unix shell (Linux or macOS; nothing here was tried on Windows). The
first five need Python 3.9 or later, called as `python3`, and nothing else, though the fourth also uses numpy
and a C compiler when they are there. The sixth needs a C compiler, called as `cc`; put `CC=gcc` in front of
the command to use another. They were run with Python 3.9.6 and 3.13.16, numpy 2.0.2 and 2.1.3, Apple
clang 21 and gcc 13.3. The next four were added in revision 2: the seventh, the ninth and the tenth need
Python 3 and nothing else, and the eighth needs a C compiler. The eighth runs the vector code on x86-64
processors with
AVX2 and FMA; elsewhere it runs only the plain C, unless the SIMDe library is given (its page says how).

| command | what it does | time | the last line it prints |
|---|---|---|---|
| `python3 docs/walkthrough.py all` | the numbers and the check of each of the ten steps | 1 second | `OK: all ten steps, every check passed.  A Python check, not a proof.` |
| `python3 -B tools/circuits/run.py` | reads every circuit from its text file, checks it against the definition of the transform in exact arithmetic up to 4,096 points, prints the tables, and writes the Lean data file again and compares it | about a minute, 700 MB of memory | `OK: 4 named circuits and the 20-line program replayed; every size up to 4096 points regenerated and replayed; 41 program files and the Lean data file reproduced byte for byte.  A Python check, not a proof.` |
| `python3 -B tools/circuits/multiply_add_check.py` | checks that no line of any circuit file has a constant on both of its terms (this is what makes the comparison with the 1994 paper fair; see above) | 1 second | `OK: 63 circuit files, 23715 lines; ...` |
| `(cd tools/circuits/fast && python3 -B -m wht56 --selftest)` | 30 tests of the circuits as working programs in Python, numpy and C | under a minute | `OK`; `OK (skipped=5)` without numpy; `OK (skipped=3)` without a C compiler |
| `python3 -B tools/circuits/ga_count.py` | the computation on the count of Grigoryan and Agaian (see "Credit, and what is in print") | 1 second | `OK: the recursion gives N log2 N at every size from 2 to 16384 points; ...` |
| `sh tools/circuits/fast/wht56/c/build_and_bench.sh` | compiles the C version three ways, checks the four C transforms against each other, and times them | under a minute | `CHECK OK: the four transforms agree at every size above` |
| `python3 -B tools/circuits/count_tables.py` | builds the circuits of the exact count tables up to 4,096 points, counts them and checks each count against its formula | a few seconds, about 160 MB | `OK: every built circuit equals its formula.  A Python check, not a proof.` |
| `sh tools/fht-kernel/test.sh` | builds the kernel with FFHT's entry points and tests it: exact on whole-number inputs, FFHT's return codes, the rounding on real inputs, and a broken copy that must fail | about 4 seconds (about 8 with SIMDe) | `OK: exact on integer inputs at every size 2^0 to 2^20 in float and double, FFHT's return codes, broken copy caught.` |
| `python3 -B measurements/2026-10-22/tables.py` | re-derives every figure of the measurements of 22 October from the raw timing files | under a second | `OK: every figure of measurements/2026-10-22/README.md re-derived from the raw files.  Measurements, not proofs.` |
| `python3 -B measurements/2026-10-22/circuits/check_circuits.py` | replays the 12 circuit files of the measurements of 22 October in exact arithmetic, and checks that the timing programs used exactly these files | under a second | `OK: 12 circuit files, each exact on every unit vector.` |
| `sh lean/check.sh` | builds the two Lean proofs and compares each statement with what was proved | about 15 minutes | `RESULT: PASS` |

The second command replays every size up to 4,096 points. `python3 -B tools/circuits/run.py --kmax 14`
replays the two largest sizes of its tables as well, up to 16,384 points; that takes 9 minutes and 3 GB of
memory, and the last line then says `16384`.

The Lean check needs more than the others: Linux with `git`, `curl` and `elan` (the program that installs
Lean), an internet connection and about 12 GB of free disk. Its comparison steps held up to 15.3 GB of
memory in one process on the machines where they were run, which have 50 GB; a smaller machine was not tried.
[VERIFY.md](VERIFY.md) has each command, what it prints and what was run. The whole Lean check was not run on a
Mac; the seven files of the 3/4 count were compiled on one.

The timings and the hardware figures of the two sections further down have their own pages, each with
commands that need Python only and with what was run:
[the timings](tools/circuits/fast/wht56/results/ffht/README.md), section 6,
[the hardware](tools/circuits/fpga/README.md), section 8, and
[the measurements of 22 October](measurements/2026-10-22/README.md).

## Is it faster in practice?

Not in general. I timed it twice. For the first version, inside the library FFHT on one machine, the new step
did not make FFHT faster at any size. For this revision, in FFHT's structure on four processors and on a GPU,
the
best circuit took 5-6 % less time than the best textbook code on AMD Zen 4 and 0-2 % less on AMD Zen 5, in
one run each; there was no clear gain on AMD Zen 2, the circuit was slower on an older Intel processor, and
on the GPU it made no difference. Before those runs I set a rule: at 0.90 of the rival's time or below
(10 % less), the work would go on; at 0.95 or above, it would count as no gain worth pursuing on that chip.
Across builds, Zen 5 came out above 0.95, and Zen 4 between the two. With 512-bit code on Zen 4, in two runs on
the same machine, the circuit came out below 0.90 at one size and between the two at most others (below).

### 11 October: FFHT on one rented machine

It was not faster in the test that I then took as the one that counts: FFHT
(<https://github.com/FALCONN-LIB/FFHT>; Andoni, Indyk, Laarhoven, Razenshteyn and Schmidt, 2015), a tuned
open-source library for this transform. I wrote the new 8-point step into the code that FFHT's own generator
produces, in place of its block of 24 additions and subtractions, and changed nothing else. On the one
machine I timed, this did not make FFHT faster at any size from 2^6 to 2^26 points in single precision or
from 2^5 to 2^26 points in double precision: set against a second build of FFHT's unchanged code, all 129
combinations of size and form took more time.

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

### 22 October: four processors and a GPU, in FFHT's structure, against a fair rival

**How the test works.** My timing program keeps FFHT's sequence of steps exactly; a check compares it with
the code that FFHT's own generator writes. Only the 8-point step done inside the registers is swapped. In
the same program, and taking turns with the circuit, run these rivals: FFHT itself, built with the same
compiler and flags; the textbook 8-point step; and the *balanced* textbook, in which half of the 24 additions
are done as multiply-adds by 1, so that both kinds of arithmetic unit are kept busy. The balanced textbook is
written two ways, multiply-add first and subtraction first; the reason is the retraction below.

- The *ratio* is the circuit's median time divided by the median time of the fastest rival. Below 1 means
  the circuit is faster: 0.94 means 6 % less time.
- Each figure is the median of 9 repeats of at least 0.2 seconds, on one pinned core, with a check that the
  machine was otherwise quiet.
- Every program was built with gcc 13.3.0 and with clang 18.1.3. *Across builds* means the best circuit
  over both builds against the best rival over both builds, at the sizes both compilers ran.
- Before any timing, every program had to give exact outputs on whole-number inputs at every size from 2^1
  to 2^20, and a deliberately broken copy had to be caught.
- *The circuit* means the fastest, at each size, of three circuits with exact output: the 8-point member of
  the 3/4 family (g20: 20 operations when doublings are free;
  `tools/circuits/programs/generated/G_family_8.txt`), the 19-operation circuit, and the family's 16-point
  member (52 operations). The 20-line circuit shown at the top of this page leaves its output halved, which
  is not FFHT's output, so it is left out.
- *Same array* means one buffer is transformed again and again. Its numbers soon overflow to infinity and
  "not a number", for every program alike: in at least 90.5 % of the timed calls at 2^10 to 2^16 (more than
  99.9 % at the smallest sizes, at least 31 % at the largest). Whether such values change the speed was not
  measured directly; the timings on finite data give figures of the same size. *Separate arrays* and runs
  with many vectors per call keep the data finite. Each figure below says which.

| chip | precision and sizes | the circuit's time / the fastest rival's | data | status |
|---|---|---|---|---|
| AMD Zen 5 (EPYC 9B45) | double, 2^10 to 2^16 | **0.977-0.996** across builds: 0-2 % less time | same array | one run; its program was reviewed before the run, its results were not |
| | single, 2^10 to 2^20 | 0.974-0.994 across builds; 0.944-0.958 with separate arrays (gcc only, at 2^12, 2^16 and 2^20) | same array; separate | the same run |
| | many vectors per call, 64 to 512 points | 0.986-1.760, best over all 8 builds: **no gain** (1.760 is at 64 points in single precision, against a 512-bit textbook layout that has no circuit version; without it 0.986-1.037). At 1,024 points 1.015 (double) and 1.018 (single); at 4,096 points 1.013 and 0.959 | finite | one run, not reviewed |
| AMD Zen 4 (EPYC 9B14) | double, 2^10 to 2^16 | **0.940-0.952** across builds: 5-6 % less time | same array | one run, not reviewed |
| | single, 2^10 to 2^20 | 0.934-1.038 across builds, mixed; 0.965-0.969 with separate arrays (gcc only) | same array; separate | the same run |
| | many vectors per call, 64 to 512 points | 0.972-1.107, best over all 8 builds: **no gain** (1.107 is at 64 points in single precision, against a 512-bit textbook layout that has no circuit version; without it 0.972-1.013). At 1,024 points 0.979 (double) and 0.983 (single); at 4,096 points 0.981 and 0.967 | finite | one run, not reviewed |
| AMD Zen 2 (EPYC 7B12) | double, 2^10 to 2^16 | gcc 0.928-1.001, noisy: **no clear gain** | same array | one run, reviewed; against the older rival with register copies, which can only favour the circuit |
| | single, 2^10 to 2^16 | gcc 0.986-1.100; clang 0.994-1.047 | same array | the same run |
| Intel Xeon at 2.20 GHz, family 6 model 79 (Broadwell) | double, 2^10 to 2^16 | gcc 1.065-1.134: **the circuit is slower** | same array | one run, reviewed; the older rival |
| | single, 2^10 to 2^16 | gcc 1.151-1.265; clang 1.023-1.062 | same array | the same run |

"Reviewed" means that a second agent read the run's results after it finished.

**The figure I retracted.** My first figure on 22 October was that on Zen 5 the circuit took 0.847-0.889 of
the fastest rival's time in double precision, built with gcc, in three runs: 11-15 % less time. That was
wrong. The fastest rival then was the balanced textbook written multiply-add first. On these processors a
multiply-add writes its result over one of its inputs, so the compiler had to copy that input to another
register (one of the processor's few working slots for numbers) before each one: 12 avoidable copies
per 8-point step in clang's code and 8 in gcc's, where the circuit's step has 0 and 3. A reviewing agent
found the copies by reading the compiled code while it checked my claim. Written subtraction first, the
same 24 operations, with the same signs and the same rounding, carry 0 copies under clang and 4 under gcc.
Against that fair rival the circuit takes 0.977-0.996 of the time across builds: 0-2 % less. Under gcc the
fair rival still has one copy more than the circuit (4 against 3); under clang both have none, so that is the
clean comparison. On Zen 4 the two ways of writing the rival take the same time. The first three runs stay
in the record, with their figures, on [the measurements page](measurements/2026-10-22/README.md).

**The sizes libraries use.** At 64 to 512 points, with many vectors per call and finite data, neither Zen 4
nor Zen 5 shows a gain (the table above).

**One step alone.** Timed as one pass in the registers rather than as a whole transform, a step gains more
when the processor is kept busy with independent work: on Zen 2 the 16-point family step took 0.780-0.785
of the textbook step's time and the 8-point step 0.829-0.843; on Zen 5 and Zen 4 with 512-bit code the
16-point step took 0.784-0.792. The rivals of these one-pass tests did not yet include the subtraction-first
form. But when each operation waits for the last, the 8-point step was 1.96 times slower than the textbook
on Zen 5. Inside a whole transform the gain shrinks to the figures of the table. One run each.

**Two by-products, with no new mathematics.** In FFHT's structure, the subtraction-first balanced textbook
on its own takes 0.80-0.84 of the time of the best FFHT build on Zen 5 (double precision, 2^10 to 2^16,
across builds), and 0.90-0.93 on Zen 4. And FFHT has no 512-bit code: on Zen 5 a tuned 512-bit textbook
takes 0.40-0.50 of FFHT's time in double precision and 0.37-0.46 in single, at 2^10 to 2^20; on Zen 4,
0.64-0.75 and 0.56-0.72 (0.65-0.76 and 0.56-0.72 in the repeat). On Zen 5 the fastest 512-bit textbook was
1.30-1.41 times as fast as the fastest 256-bit program, circuit or not (double precision, 2^10 to 2^16). One
run each, except the 512-bit test on Zen 4, which ran twice on one machine; the 512-bit runs are not reviewed.

**512-bit code.** With the circuit inside 512-bit code (AVX-512), not reviewed, across builds, at the even
sizes 2^8 to 2^20: on Zen 5, in one run, 0.940-1.018 in single precision and 0.946-1.007 in double; on Zen 4
0.886-1.002 and 0.913-1.037 in a first run, and 0.886-1.003 and 0.907-1.037 in a second run on the same
machine. The two Zen 4 runs agree within 1.6 % at every size. Together they give 0.886-0.954 in single
precision from 2^12 points and 0.907-0.959 in double from 2^10: 4-11 % less time. At one size, 2^18 points in
single precision, both runs gave 0.886, past the bar of 0.90; at 2^8 points neither precision gains, nor
single precision at 2^10 (0.996-0.997). Both runs are on one machine, so they show that the figure repeats
there, not that it holds on other Zen 4 machines.

**Rounding.** On whole-number inputs every program is exact. On real inputs, in double precision, the
circuits differ from the textbook by at most 3.9e-16 relative to the largest output at 2^10 and 2^20, the
sizes the timing program checks; the kernel's own test finds up to 4.5e-16 at 2^5 to 2^20. In single
precision their error against a double-precision reference is 1.1e-7 to 1.7e-7, against 0.8e-7 to 1.3e-7 for the
textbook. So the circuit is not bit-identical to FFHT on real data.

**On a GPU, nothing.** On an NVIDIA RTX PRO 6000 Blackwell Server Edition, whole rows of 256 MiB are limited
by memory and tie (0.9999-1.0001). In the GPU kernel of Dao's fast-hadamard-transform, the circuits took
0.966-1.043 of its own time over 18 settings: net zero. The tensor-core kernel HadaCore takes 0.594-0.722 of
the time of Dao's, so the bar on a GPU is elsewhere. A figure of 0.82 at 4 MiB sits on the 4.1 µs floor of a
kernel launch and is not a circuit result.

**A separate test, not of these circuits.** Some language models rotate vectors whose length is not a power
of two, such as 28 × 1,024. Dao's GPU library does the 28-point part as plain signed sums. Sanjeet, Colbert
and co-authors (PeRQ, arXiv:2601.22347, Appendix A.1 and Table 4) compute that part with shared sums over
groups of four, which halves the additions of the rotation (252 additions at 28 points). I timed their form,
and a circuit of mine with 235 additions found by a randomized greedy search for shared sums, against Dao's
unchanged kernel (batches of 4,096 vectors, half precision):

| length | my greedy circuit / Dao | groups of four (Sanjeet, Colbert and co-authors) / Dao |
|---|---|---|
| 28 × 1,024 (LLaMA-3.3-70B) | 0.952-0.967 | 0.955-0.963 |
| 28 × 512 (LLaMA-3.1-8B, Mistral-7B) | 1.169-1.178, a loss | 0.995-1.005 |

The published form does as well where mine gains, and it does not lose where mine does. An earlier form of
grouped sums, for 12 and 20 points, is in US patent 9,081,731. My part is the greedy circuit and the
measurement.

**What these measurements do not show.**

- That it is faster on processors in general. There is no gain on AMD Zen 2. On an Intel Broadwell chip the
  circuit is slower. Modern Intel chips (Sapphire Rapids and later), Apple processors and Arm library code
  are untimed in this test.
- That it is faster on AMD in general. Each figure comes from one rented cloud machine per chip, one pinned
  core and one run (the 512-bit test on Zen 4 ran twice, on the same machine), and the clock frequency was
  not controlled.
- That the gain comes from fewer additions. The 19-operation circuit was slower than the 20-operation
  family step in 13 of 16 double-precision timings on Zen 4 and Zen 5, and I do not know why.
- A gain at the sizes most libraries use, 64 to 512 points. On Zen 4 and on Zen 5 there is none.
- The same results as FFHT bit for bit. They are the same on whole-number inputs. On real inputs they differ
  by rounding, so the circuit is not a drop-in where a library promises bit-identical output.
- The fastest code on these chips. On Zen 5 plain 512-bit textbook code was 1.30-1.41 times as fast as the
  fastest 256-bit program, circuit or not.
- Several cores, throughput, or a whole application. No library and no end-to-end workload was measured.
- That the kernel folder below is fast as a library. It was cut from the timing program and checked for
  exactness, but it has not been timed on its own.
- FFHT as its own authors time it. FFHT was built with the same flags as each program and timed in my
  program, not by its own Makefile and its own test program. Sizes below 2^6 were not timed.

The full results, the programs that produced them, the raw outputs, what went wrong during the night and
how to run it all again are on [the measurements page](measurements/2026-10-22/README.md).

### A kernel with FFHT's entry points

[tools/fht-kernel/](tools/fht-kernel/README.md) holds the timed program's 8-point step, the 20-operation
member of the 3/4 family, as a small C library: vector code for x86-64 processors with AVX2 and FMA, and
plain C for other processors. It has the four functions of FFHT, with the same arguments and the same return
codes (`fht_float`, `fht_double` and
their out-of-place forms), under its own names, and under FFHT's names when it is compiled with one flag. It
also has a form that multiplies the output by a given factor. The 8-point step is chosen when it is
compiled: the circuit, or one of the two textbooks.

- Its outputs equal FFHT's on whole-number inputs. On real inputs the rounding differs (its page gives the
  numbers), so it is not a drop-in where bit-identical output is promised.
- It was cut from the program that measured a few percent less time on AMD Zen 4 and Zen 5 (the table
  above). It has not been timed as a library itself.
- When to use it, as a measurement: on the chips I measured, the circuit step on AMD Zen 4 and Zen 5, where
  the gain was small and from one run per chip. I have no measurement that favours it on other processors.
  Its page gives the rule in full.
- It has no 512-bit code. On Zen 5, plain 512-bit textbook code was faster than any 256-bit code (above), so
  a 512-bit form is [open direction](#open-directions) 6.

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

On an iCE40-HX8K FPGA board running at 12 MHz, the 19-adder 8-point Walsh-Hadamard circuit was run side by
side with the textbook circuit on 597,750,000 test inputs, and the two gave the same outputs every time; a
deliberately broken copy of the circuit, run alongside, was caught, which shows the test can fail. This
checks only that the circuit computes the right values on a real chip: it says nothing about size or speed,
and in this pipelined build the 19-adder circuit is the larger of the two designs. The lines the board sent,
and the conditions, are in
[tools/circuits/fpga/board/run-2026-10-11/](tools/circuits/fpga/board/run-2026-10-11/README.md).

No existing design was improved in this check. The long version, with the tables, the designs, what was and
was not placed and routed, and how to run the tools again, is
[tools/circuits/fpga/README.md](tools/circuits/fpga/README.md).

### 22 October: a Xilinx chip, and a loss

On 22 October the 19-adder 8-point circuit and the 52-adder 16-point circuit were placed on a Xilinx Artix-7
(xc7a100t) with the open-source tools openXC7, with 5 placement seeds each. The circuits use fewer of the
chip's *carry blocks*, the part that does the additions: 57 against 72 at 8 points (20.8 % fewer) and 156
against 192 at 16 points (18.8 % fewer). But once placed they take more of the chip's *slices*, its units of
area: at 8 points 13.1 % more with 3 adder levels per clock and 29.8 % more with 2; at 16 points 31.4 % more
with 2 levels, and 0.9 % fewer with 4. Against Alman and Rao's 8-point step the 19-adder circuit takes 8.4 %
fewer slices, with 2 adder levels per clock. A textbook built by hand from three-input adders, a design from
another study placed in the same run, uses fewer carry blocks than the 19-adder circuit (54 against 57 at
8 points). So on this chip it is not a gain. Its limits: open-source tools only, no maker's tools, no file
was made to load into a chip, and the designs used 2 % of the chip or less. A
radar design measured the same night is not about these circuits and is not in this repository. The figures
are on [the measurements page](measurements/2026-10-22/README.md).

What is not claimed in hardware: a smaller design on every FPGA. Artix-7 is a loss; on the iCE40, Alman and
Rao's 22-adder step is smaller; and with registers the circuits are larger. Power was not measured.

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

On 22 October 2026 I had the circuits timed on more processors and on a GPU, and placed on an FPGA of a
second maker, a Xilinx Artix-7. AI agents at my direction wrote the timing programs, ran them on virtual
machines rented through Google Colab, and read the results. A reviewing agent, checking my first speed
figure, found that the fastest
rival carried avoidable register copies; that figure is retracted above. The same agents wrote the count
program, the kernel in `tools/fht-kernel/`, the measurements page and the changes to these pages, and checked
the literature again. As before, no person has read their code line by line.

## Credit, and what is in print

- **Alman and Rao (2023).** The method is theirs: write the 8-point table of signs as a part of low rank
  (every row a multiple of one row, or a sum of a few such) plus a sparse part (few entries that are not
  zero), and halve once. Their 8-point step costs 23 operations (22 additions or subtractions and one
  halving) where this one costs 20. Their count model is the strict one used here, so the table in "The
  count, and how it compares" compares the same task with the same things charged. Their theorem is wider
  than mine: it covers every
  power of two and any field (any system of numbers with the four operations), where my Lean statement
  in their count covers the powers of 8 over the complex numbers. Their
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
- **FFHT**, the library of the timings, is by Andoni, Indyk, Laarhoven, Razenshteyn and Schmidt; its README
  asks users to cite their paper "Practical and Optimal LSH for Angular Distance" (NIPS 2015). The kernel
  folder keeps FFHT's four entry points, and the kernel folder and the timing programs under
  `measurements/2026-10-22/x86/` keep its plan of passes and a few of its lines, under FFHT's MIT licence;
  [NOTICE](NOTICE) says which files.

**What came before.** Coppersmith, Feig and Linzer (1994) found the 4-point circuit with 7 operations and
the rate 7/8 when doublings are free; everything in my second count starts from their circuit. Alman and Rao
(2023) found, to their knowledge, the first count below N log2 N with every operation charged, 23/24, and
the method mine follows. Alman (2021) studied circuits for this transform in a count of wires and showed
that large constants help shallow circuits. Morgenstern (1973) proved the lower bound (1/2) N log2 N for
circuits whose constants are at most 1 in size. OpenAI's family 130 (2026) proved that, with constants of
any size, the Fourier transform can be computed with fewer than any fixed fraction of n log2 n operations,
at some lengths; my circuit model and part of my Lean proof are theirs. I have not searched the hardware literature on shift-and-add
synthesis of constant matrices, which counts adders the way my second count does.

I did not find these counts in the literature I searched: the papers that the indexes list as citing Alman
and Rao or the 1994 paper, arXiv, seven patents, and the first part of one survey. It is a search, not a
proof that the counts are new. [The note](notes/explicit-circuits.md), section 7, says what was read and
what was not. If you know a smaller count in print, I would be glad to hear of it and will credit it.

## What changed in revision 2

Revision 2 is dated 22 October 2026. The first version is of 11 October 2026.

- **A correction.** The first version said "The best in print is 23/24, by Alman and Rao." That was wrong
  as written: counts of smaller order are in print, for the Fourier transform in the same circuit model and
  for this transform in a model of a computer with memory. It now says that 23/24 is the smallest constant
  that I found in print for a count of the form c·N log2 N plus a multiple of N, and that this repository
  gives a better constant, with exact counts at sizes one can write down, not a better order. The same
  correction is made where the first version said "the published record" or "the record":
  [docs/UNDERSTAND.md](docs/UNDERSTAND.md), steps 3, 8 and 10, and the index `notes/explicit-circuits.json`.
  The note, the paper and [tools/circuits/README.md](tools/circuits/README.md) already said "I found in
  print"; the note and that README now add the qualifier "of the explicit form", and the paper keeps its
  text of 11 October with a dated note in [paper/README.md](paper/README.md).
- **A sentence kept, with a qualifier.** The first version called the work "not a faster program", on the
  strength of one machine. On 22 October, in the main test, two AMD processors showed a few percent less
  time, in one run each and below the bar I had set before the runs; in 512-bit code on Zen 4, two runs on
  one machine showed 4-11 % less time from 2^12 points, past the bar at one size. The sentence stays, and
  now says so.
- **New sections:** what is counted, with Morgenstern's bound; exact counts from 8 to 32,768 points; a
  claim-by-claim proof status, with the axioms that Lean reports; the relation to OpenAI's family 130; open
  directions, each with a first experiment.
- **The measurements of 22 October**, on AMD, Intel, NVIDIA and Xilinx hardware, with the losses and with
  the figure I retracted: [measurements/2026-10-22/](measurements/2026-10-22/README.md).
- **A kernel with FFHT's entry points**, with tests of exactness and rounding:
  [tools/fht-kernel/](tools/fht-kernel/README.md).
- **A count program** for the exact count tables: `tools/circuits/count_tables.py`.
- **The 3/4 count proved in Lean.** The first version said that the second count was replayed by
  programs and was not in Lean. Revision 2 adds a Lean proof that the family's bound,
  (3/4) N log2 N + N/4, holds at every power of two, in a model where each line is one multiply-add,
  over any commutative ring, and a proof that the 19 lines at 8 points compute the transform. The files
  are in `lean/Work/WHT34/`, and `sh lean/check.sh` checks them too.
- **Prior art added:** Alman (2021), Morgenstern (1973), OpenAI's family 130 by name, FFHT's paper, and,
  for the separate GPU test only, PeRQ and US patent 9,081,731; and the gap in the literature search stated
  (shift-and-add synthesis in hardware).
- In [the note](notes/explicit-circuits.md), passages marked "Revision 2" in sections 1, 5, 7, 9 and 10:
  the new measurements in brief, Morgenstern's bound, the literature added, and the lists of what has not
  been tried, which now say what was tried on 22 October. Its `.json` has the exact count tables and the
  figures of 22 October.
- The title of step 8 of docs/UNDERSTAND.md, a note on the paper's status in [paper/README.md](paper/README.md),
  the machines of 22 October in the list of who ran what, and pointers from the pages on FFHT and on the FPGA
  to the new measurements.

**Unchanged:** the Lean proof of the 5/6 count, every circuit file, the 11 October measurements, the paper,
and the record in `waves/`. That record describes 11 October, so three of its pages, `waves/README.md`,
`waves/WHERE-THE-CIRCUITS-CAME-FROM.md` and section 1.8 of `waves/LEADS.md`, still describe count (G) as not
in Lean; on that point revision 2 supersedes them.

## Open directions

Each comes with a first experiment. [waves/LEADS.md](waves/LEADS.md) stays the long list.

1. **A 16-point step, up to a common factor, with 53 operations or fewer of count (O).** Layers of it would
   beat 5/6. *First experiment:* a SAT or integer-programming search at 16 points with a limit on depth,
   started from the 56-operation step.
2. **Shift-and-add optimisers on the 8-point matrix.** *First experiment:* run an open tool for
   constant-matrix multiplication (for example FloPoCo's shift-and-add operators) on the 8 × 8 Hadamard
   matrix with shifts free, and see whether it reaches 19 adders or fewer. Then search those papers'
   benchmark tables for Hadamard entries.
3. **The constants in the Lean statement of the second count.** It allows any constant; the circuits
   use only ±1 and ±2. *First experiment:* state the form with every constant in {1, -1, 2, -2}; the
   proof already builds such a circuit.
4. **Combining the two constructions.** Six ways were tried, and none went below 5/6. *First experiment:*
   the first lead of part 1 of `waves/LEADS.md` that is not closed.
5. **Speed on the deciding chips.** *First experiment:* run the 22 October timing program on a modern Intel
   server processor (Sapphire Rapids or later) and on a second Zen 4 and Zen 5 machine, with finite data in
   every mode.
6. **A 512-bit kernel.** With 512-bit code on Zen 4, two runs on one machine both reached 0.886 (2^18 points,
   single precision); neither is reviewed. *First experiment:* have a second agent read both runs and repeat
   the test on a second Zen 4 machine, then add a 512-bit form to `tools/fht-kernel/` only if the reading
   holds.
7. **Why the 20-operation family step usually beats the 19-operation circuit in time.** *First
   experiment:* a model of how the two steps load the arithmetic units of Zen 4 and Zen 5 (for example `llvm-mca -mcpu=znver4` and `znver5`), set
   beside the measured ratios.
8. **FFHT's own step, balanced.** The first by-product above. *First experiment:* time FFHT with only its
   8-vector step rewritten subtraction-first, on Intel and on AMD, built by FFHT's own Makefile and timed
   with its own test program.
9. **Rounding.** *First experiment:* a bound on the worst-case error of the 20-line step against the
   textbook, checked by the kernel's rounding test at 2^5 to 2^20 points with inputs chosen to make the error
   large.
10. **FPGA: power and the makers' tools.** *First experiment:* place the 19-adder circuit and the textbook on
    an Artix-7 with Xilinx's own tools and compare slices and power at the same clock.
11. **A person reading the Lean statement.** The 93-line `lean/Work/SmallWHT/ChallengeWHT8.lean` is the
    whole claim of the first count, and the 91-line `lean/Work/WHT34/ChallengeWHT34.lean` that of the
    second. *First experiment:* read them against the definition of the transform in
    [docs/UNDERSTAND.md](docs/UNDERSTAND.md).

## The folders

| where | what |
|---|---|
| [docs/UNDERSTAND.md](docs/UNDERSTAND.md) | start here to understand the result: ten steps, each with a check; `docs/walkthrough.py` computes the numbers of each step |
| [paper/](paper/README.md) | the write-up as a paper, PDF and LaTeX source, with its two check programs; not peer reviewed; the version of 11 October |
| [notes/explicit-circuits.md](notes/explicit-circuits.md) | the full account: both counts, the tables, the Lean statements, the literature search, what has not been tried; the `.json` beside it has the figures in machine-readable form |
| [tools/circuits/](tools/circuits/README.md) | the circuits as text files (`programs/`), the checker and the generator, `run.py`, and what it printed in the recorded run; `count_tables.py`, the exact count tables |
| [tools/circuits/search/](tools/circuits/search/README.md) | the programs that found the circuits, as they were run |
| [tools/circuits/fast/wht56/](tools/circuits/fast/wht56/README.md) | the circuits as working programs in Python, numpy and C, with tests and the timings |
| [tools/circuits/fast/wht56/results/ffht/](tools/circuits/fast/wht56/results/ffht/README.md) | the 8-point step inside the library FFHT: the timings by size, my patch against FFHT's generator, the timing programs and their raw outputs. No file of FFHT is included |
| [tools/circuits/fpga/](tools/circuits/fpga/README.md) | the circuits as hardware: the generator of hardware descriptions, the designs, the scripts for the open-source tools, the result tables, and the sources of the self-test for a board |
| [tools/fht-kernel/](tools/fht-kernel/README.md) | a small C library with FFHT's four entry points and the circuit as its 8-point step, AVX2 and plain C, with tests of exactness and rounding; not timed as a library |
| [measurements/2026-10-22/](measurements/2026-10-22/README.md) | the timings of 22 October on AMD, Intel and NVIDIA hardware and the Artix-7 placement: the programs as run, the raw outputs, the retracted figure, and a program that re-derives every figure |
| [waves/](waves/README.md) | the ten waves of the night of 10 to 11 October 2026. About 180 working reports by AI agents, with their programs and small outputs, sorted by wave; where the circuits came from; what is open and what is closed. Not reviewed by a person. Not in Lean. This folder is most of the repository: about 4,950 of its 6,930 files and 30 of its 54 MB. |
| [lean/](lean/) | the Lean project: `Work/SmallWHT/` has my six files for the 5/6 count, `Work/WHT34/` my seven for the 3/4 count, `OAI/` the 44 files of openai/math, `check.sh` the one command |
| [VERIFY.md](VERIFY.md) | how to check the Lean proofs, and what was run |
| [NOTICE](NOTICE), [LICENSE](LICENSE), [CITATION.cff](CITATION.cff) | where each part comes from, the licence, how to cite |

## Licence

Apache License 2.0, the licence of openai/math: [LICENSE](LICENSE). [NOTICE](NOTICE) says which files are
OpenAI's and which are new. It also lists the parts of other people's work and their licences: FFHT's plan of
passes and a few of its lines, which the kernel folder and the timing programs of 22 October keep under
FFHT's MIT licence. No code of Dao's fast-hadamard-transform, HadaCore, SIMDe or VkFFT is included; the
scripts fetch them. If you would like the kernel folder under the MIT licence for your project, open an
issue on this repository and ask me.

## How to cite

Jacob Sussman, "The Walsh-Hadamard transform with fewer operations", 2026, revision 2 of 22 October 2026,
https://github.com/jacobalansussman/wht-fewer-operations. [CITATION.cff](CITATION.cff) has the same in a form
that programs read. This revision has no permanent identifier yet; cite the revision and its date.

## Sources

- J. Alman, K. Rao, "Faster Walsh-Hadamard and Discrete Fourier Transforms From Matrix Non-Rigidity",
  STOC 2023, pages 455 to 462, doi 10.1145/3564246.3585188; <https://arxiv.org/abs/2211.06459>, version 2.
  The bound is their Theorem 1.1; the exact count is in the proof of their Theorem 6.2.
- D. Coppersmith, E. Feig, E. Linzer, "Hadamard transforms on multiply/add architectures", IEEE Transactions
  on Signal Processing 42(4), 1994, pages 969 to 970, doi 10.1109/78.285664.
- A. M. Grigoryan, S. S. Agaian, "Split manageable efficient algorithm for Fourier and Hadamard transforms",
  IEEE Transactions on Signal Processing 48(1), 2000, pages 172 to 183, doi 10.1109/78.815487. The stated
  count is on page 181 and the bound on page 172.
- J. Alman, "Kronecker Products, Low-Depth Circuits, and Matrix Rigidity", STOC 2021;
  <https://arxiv.org/abs/2102.11992>.
- J. Morgenstern, "Note on a Lower Bound on the Linear Complexity of the Fast Fourier Transform", Journal of
  the ACM 20(2), 1973, pages 305 to 306, doi 10.1145/321752.321761. Known through the statements of Alman and
  Rao, of OpenAI's papers and of N. Ailon (arXiv:1403.1307); not read in the original.
- OpenAI, "Finite tensor savings and exact Fourier circuits" and "An explicit power saving for the exact
  discrete Fourier transform", both of 25 September 2026, family 130 of
  [openai/math](https://github.com/openai/math); the community page of the first:
  <https://mathcommunity.github.io/oai-math-revised/papers/Finite-tensor-savings-and-exact-Fourier-circuits-September-25-2026/>.
- J. Sussman, wht-power-saving-lean, <https://github.com/jacobalansussman/wht-power-saving-lean>, read at
  commit `86e575e28ed94890872dcff1bb2621d7ff559cbd` (20 October 2026): the Walsh-Hadamard saving 1.5699306e-3,
  of 13 October 2026.
- A. Andoni, P. Indyk, T. Laarhoven, I. Razenshteyn, L. Schmidt, "Practical and Optimal LSH for Angular
  Distance", NIPS 2015; <https://arxiv.org/abs/1509.02897>. The paper that FFHT's README asks users to cite.
- S. Sanjeet, I. Colbert, P. Monteagudo-Lago, G. Franco, Y. Umuroglu, N. J. Fraser, "Pushing the Limits of
  Block Rotations in Post-Training Quantization" (PeRQ), ICML 2026; <https://arxiv.org/abs/2601.22347>,
  version 2: Appendix A.1 and Table 4. Cited for the separate GPU test only.
- M. A. Herman, T. H. Weston, "Efficient transforms and efficient row generation for Kronecker products of
  Hadamard matrices", US patent 9,081,731 B2, granted 14 July 2015. Cited for the separate GPU test only.
- openai/math, <https://github.com/openai/math>, at commit `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`.
- Lean 4, version 4.34.1; Mathlib at revision `d13f23b723b8a846827a245b89c10fc7d3f11612`, fetched by the
  build.
- FFHT, <https://github.com/FALCONN-LIB/FFHT>, at commit `fba727a3ff72c862260460631ae1cc8e3e44e861` (10 March
  2019, its last), under the MIT License. No file of it is in this repository; the kernel folder and the
  timing programs of 22 October keep its plan of passes and a few of its lines, under its licence, as
  [NOTICE](NOTICE) says.
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
- The measurements of 22 October 2026. Processors: AMD EPYC 9B45 (Zen 5), AMD EPYC 9B14 (Zen 4), AMD EPYC
  7B12 (Zen 2) and Intel Xeon at 2.20 GHz, family 6 model 79 (Broadwell), each a virtual machine rented
  through Google Colab. Compilers: gcc 13.3.0 and clang 18.1.3, on Ubuntu 24.04. GPU: NVIDIA RTX PRO 6000
  Blackwell Server Edition, driver 580.82.07, CUDA 13.0, PyTorch 2.11. Third-party code, fetched by the
  scripts and not included: FFHT at the commit above; SIMDe v0.8.2 at commit
  `71fd833d9666141edcd1d3c109a80e228303d8d7`; Dao-AILab/fast-hadamard-transform at commit
  `e7706faf8d1c3b9f241e36860640ad1dac644ede`; HadaCore, in pytorch-labs/applied-ai, at commit
  `2391954b19988bd76cf3c2ea84c1ce74b68d568b`; VkFFT at commit `066a17c17068c0f11c9298d848c2976c71fad1c1`,
  whose part of the GPU test failed to run. The Artix-7 placement: openXC7 of 19 October 2026, with
  nextpnr-xilinx `e7a6fb0e` and Yosys 0.69+274. The run of each figure is named in the sources section of
  [the measurements page](measurements/2026-10-22/README.md).
- Dates. The searches: the night of 10 to 11 October 2026. The Lean build from nothing, the timings, the
  hardware measurements and the reading of the two older papers: 11 October 2026. The literature search: 10
  and 11 October 2026. The timings on AMD, Intel and NVIDIA hardware, the Artix-7 placement, the count
  tables, the kernel, a second check of the literature, the Lean proof of the 3/4 count and a second build of
  the Lean folder: 22 October 2026.
- The full list of what was read is in [notes/explicit-circuits.md](notes/explicit-circuits.md), section 10.
