# Understand the result in ten steps

This page goes from the definition to the result in ten short steps. Each step ends with one check that
takes under two minutes: a sum to do by hand, or one line to run. The answer is under a fold.

The result, in two sentences: the Walsh-Hadamard transform of N numbers can be computed with fewer
operations than the textbook's N log2 N, for example 4,352 in place of 4,608 at 512 points when every
operation is charged. It is a better constant, not a better exponent (step 10 says what that means).

To see the numbers of a step computed in front of you, run `python3 docs/walkthrough.py 5` (for step 5) or
`python3 docs/walkthrough.py all`. It needs only Python. It is a check by a program, not a proof.

I directed this work. AI agents (Anthropic's Claude) ran the computer searches that found the circuits, and
wrote the programs and the Lean files. They also searched the literature and read the two older papers
named in steps 4 and 10; [the note](../notes/explicit-circuits.md), section 7, says which pages. No person
has yet read the Lean files.

These ten steps follow one line of the work: the 8-point circuit and what is built from it. A second
construction, which gives 52 operations at 16 points in count (G), the second way of counting (step 3), is
not covered here. It is in [the note](../notes/explicit-circuits.md), section 2.

---

## Step 1. What the transform is

Take N numbers, where N is 2, 4, 8, 16 and so on. The *Walsh-Hadamard transform* turns them into N new
numbers. Each new number is the sum of all the inputs, each taken with a sign, + or -.

At 2 points: (a, b) becomes (a + b, a - b). So (5, 3) becomes (8, 2).

At 4 points the signs are these. Row j gives the signs for output j.

```
row 0    + + + +
row 1    + - + -
row 2    + + - -
row 3    + - - +
```

So (1, 2, 3, 4) becomes (10, -2, -4, 0): for example row 1 gives 1 - 2 + 3 - 4 = -2.

The rule behind the table, for any N: number the rows and the columns from 0 and write both numbers in
binary. The sign is - when the two numbers share an odd number of 1-bits, and + otherwise. Row 3 is 11 and
column 1 is 01; they share one 1-bit, so the sign is -.

The table is called H, the list of inputs x, and the transform H x. *Exact* means H x itself, with no
factor in front.

**Check.** Work out the transform of (3, 1, 4, 1) by hand.

<details><summary>Answer</summary>

(9, 5, -1, -1). Row by row: 3+1+4+1 = 9, 3-1+4-1 = 5, 3+1-4-1 = -1, 3-1-4+1 = -1.
`python3 docs/walkthrough.py 1` prints the same.

</details>

---

## Step 2. The textbook program and why it costs N log2 N

Done straight from the table, the transform costs about N × N additions. The textbook program is much
shorter. It does the 2-point step on pairs, in layers. At 4 points:

```
layer 1:   a = x0 + x1    b = x0 - x1    c = x2 + x3    d = x2 - x3
layer 2:   y0 = a + c     y2 = a - c     y1 = b + d     y3 = b - d
```

On (3, 1, 4, 1) layer 1 gives a = 4, b = 2, c = 5, d = 3, and layer 2 gives 9, 5, -1, -1 again.

Why N log2 N. Every layer pairs up all N values, and each pair costs one addition and one subtraction, so
a layer costs N operations. The number of each input, 0 to N - 1, written in binary, is its *address*.
There is one layer for each binary digit of the address, and an address has log2 N digits.

| points | layers | operations |
|---|---|---|
| 4 | 2 | 8 |
| 8 | 3 | 24 |
| 64 | 6 | 384 |
| 4,096 | 12 | 49,152 |

This program is called the butterfly. N log2 N is the number to beat.

**Check.** How many operations does the textbook program use at 512 points?

<details><summary>Answer</summary>

512 is 2^9, so 9 layers of 512 operations: 4,608. `python3 docs/walkthrough.py 2` runs the program and
counts.

</details>

---

## Step 3. Two ways of counting operations

A *circuit* here is a fixed list of lines. Each line makes one new value from values made earlier. The
question is how much one line may do for the price of one operation. There are two answers in use.

- **Count (G).** One operation is one a·u + b·v, where a and b are any fixed numbers. Multiplying by a
  constant is free.
- **Count (O).** Every addition, every subtraction and every multiplication by a constant costs one.

The letters are only labels; O is the count of OpenAI's circuit model (step 9).

| line | count (G) | count (O) |
|---|---|---|
| `u + v` | 1 | 1 |
| `u + 2*v` | 1 | 2 (a doubling, then an addition) |
| `1/2*u` | 0 | 1 |

The textbook program has only plain additions and subtractions, so it costs N log2 N in both counts.

Why both exist. Count (G) fits machines on which doubling costs nothing, or which multiply and add in one
instruction. The 1994 paper of step 4 counts that way: it charges one for a *multiply-add*, which is one
value plus or minus the product of two others (the paper writes ±a ± bc). Count (G) is a little wider in two
ways: it allows a constant on both terms, and it lets a multiplication on its own go free, where the 1994
paper charges one. No count-(G) circuit here uses either: every line has two terms and at most one constant.
Count (O) is the strict one. Alman and Rao, whose 23/24 is the smallest explicit constant of this kind that I
found in print (step 8 says what *explicit* means), count this way (step 8), and so
does the Lean statement (step 9).

Why both are on this page. The search found the small circuits in count (G). There they look best: 19
operations at 8 points. But a result in count (G) alone leaves a question open: what about the
multiplications? Step 6 answers it, and from there on everything is in count (O).

**Check.** What does the line `y3 = -h + 2*x0` cost in each count?

<details><summary>Answer</summary>

1 in count (G). 2 in count (O): one doubling, then one subtraction (2·x0 minus h).
`python3 docs/walkthrough.py 3` prints the cost of this line and of six others.

</details>

---

## Step 4. The known trick: 4 points in 7 operations

This step is not mine. It is where everything starts. In count (G), 4 points need 7 operations, not 8.
On the right is each value written in x0 to x3: + means +1, - means -1, a dot means 0.

```
p  = x0 + x1        + + . .
q  = x2 - x3        . . + -
h  = p + q          + + + -
y0 = h + 2*x3       + + + +
y1 = h - 2*x1       + - + -
y2 = h - 2*x2       + + - -
y3 = -h + 2*x0      + - - +
```

How it works. The value h is nearly every row of the table of step 1: each row differs from h, or from
-h, in one place. Adding or subtracting twice one input flips one sign. That is one operation per output.

In count (O) the same seven lines cost 11, because of the four doublings. So in the strict count this is
no gain yet.

**Credit.** Seven operations at 4 points are due to Coppersmith, Feig and Linzer (1994, page 969). They
compute one value that differs from three of the four outputs in a single sign, and get each of those
outputs by adding twice one input. They count one multiply-add, ±a ± b·c, as one operation, so a line such
as `y3 = -h + 2*x0` is one operation for them. From this circuit they get (7/8) N log2 N operations when N
is a power of 4, and N/8 more when N is an odd power of two. The circuit was found again by a computer
search (Samadi, Suzukake and Iwakura, 1998) and appears in a patent (Reshef and Alrod, filed 2002). A
4-point step with 7 additions or subtractions and one halving is in Alman and Rao (2023), from a
decomposition of Alman (2021). The listing above is another wiring of the same idea, with four doublings
where the 1994 circuit has three. The 1994 paper does not say whether 7 is the least.

**Check.** Run the seven lines by hand on (3, 1, 4, 1).

<details><summary>Answer</summary>

p = 4, q = 3, h = 7. Then y0 = 7 + 2 = 9, y1 = 7 - 2 = 5, y2 = 7 - 8 = -1, y3 = -7 + 6 = -1: the answer
of step 1. `python3 docs/walkthrough.py 4` checks the seven lines on every input.

</details>

---

## Step 5. The 8-point circuit: 19 operations and a centre

In count (G), 8 points take 19 operations. The textbook has 24. The smallest count at 8 points that I found
in print is 22, and it appears twice: the formula of the 1994 paper for odd powers of two,
(7/8) N log2 N + N/8, gives 22, and the 8-point step of Alman and Rao (step 8) has 22 additions or
subtractions and one halving. Each of the 19 lines below is one operation in the 1994 paper's own count, so
19 against 22 is like for like.

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
y3  = g9 + 2*x3      + - - + + - - +
y5  = -y3 + 2*g5     + - + - - + - +
y1  = g10 + 2*g3     + - + - + - + -
y6  = g11 + 2*g2     + + - - - - + +
y2  = g8 + 2*x1      + + - - + + - -
y4  = y2 + 2*g6      + + + + - - - -
y0  = -g11 + 2*g1    + + + + + + + +
```

The first seven lines merge the eight inputs into one value, g7. I call it the *centre*. It is not a row of
H. But a row and the centre both have a + or a - in every place, so every row is the centre with some signs
flipped. Flipping the sign of one input costs one operation: add or subtract twice that input. That is why
every later line takes a value that comes from the centre and adds or subtracts twice something small. The
something small is an input, or one of g1 to g6. Those were paid for on the way to the centre, and they
flip two or four signs at once.

The count: 7 lines to the centre, 4 shared lines (g8 to g11), and one last line for each of the 8 outputs.

Python checks these 19 lines on every input, and they are short enough to check by hand. Lean checks the
form of step 6, not this one.

**Check.** Two outputs by hand. y2 = g8 + 2·x1 = centre - 2·x7 + 2·x1. Write the signs of the centre, flip
the signs of x7 and x1, and compare with row 2 of H by the rule of step 1. Do the same for
y3 = centre - 2·x5 + 2·x3 and row 3.

<details><summary>Answer</summary>

Centre: + - - - + + - +. Flip x1 and x7: + + - - + + - -. Row 2 is 010 in binary, so the sign is - in the
columns whose second binary digit is 1: columns 2, 3, 6, 7. The same.
Flip x3 and x5 in the centre: + - - + + - - +. Row 3 (011): - where the column shares one 1-bit with 011:
columns 1, 2, 5, 6. The same. `python3 docs/walkthrough.py 5` prints, for each of the eight rows, where
it differs from the centre.

</details>

---

## Step 6. From 19 to 20: one halving removes the multiplications

In count (O) the 19 lines of step 5 cost 31: 19 additions or subtractions and 12 doublings. That is worse
than the textbook's 24.

Look at where the 12 doublings are. They are in the 12 lines after the centre, one in each. Each of those
lines is w ± 2·p, where w comes from the centre and p does not. So halve the centre once, and carry w/2 in
place of w. Then w ± 2·p becomes w/2 ± p, a plain addition or subtraction. Every output comes out halved.

```
g1 ... g7            as in step 5
m8  = 1/2*g7         the one halving
g9  = m8 - x7        g10 = m8 - x5       g11 = g9 + x6       g12 = g10 - x4
g13 = g11 + g4       half of row 7       g14 = g10 + x3      half of row 3
g15 = g5 - g14       half of row 5       g16 = g11 + g3      half of row 1
g17 = g12 + g2       half of row 6       g18 = g9 + x1       half of row 2
g19 = g18 + g6       half of row 4       g20 = g1 - g12      half of row 0
```

That is 19 additions or subtractions and 1 halving: **20 operations for H x / 2**, with nothing free. The
two lines of step 5 that began with a minus sign became plain subtractions (g15 and g20).

Two honest remarks. At 8 points alone this does not beat the textbook: undoing the halving costs 8 more
multiplications, 28 in all, against 24. The gain comes in step 7, where the factor is removed once at the
very end. And the device of one halving is not mine. It is Alman and Rao's; their 8-point step costs 23
operations where this one costs 20.

**Check.** Run the 20 lines by hand on x0 = 1 with all other inputs 0. What are the eight outputs?

<details><summary>Answer</summary>

g1 = 1, g2 = g3 = g4 = 0, g5 = 1, g6 = 0, g7 = 1, m8 = 1/2. Every later line gives 1/2. So all eight
outputs are 1/2, which is the first column of H (all +) divided by 2. `python3 docs/walkthrough.py 6`
checks the 20 lines on every input.

</details>

---

## Step 7. From 8 points to 8^j points

Take 64 numbers and write them in a square of 8 rows and 8 columns. Apply the 20-operation circuit to each
row, then to each column. That is 16 uses, 320 operations, and the result is H x / 4. Multiply each of the
64 values by 4. Total: 384.

Why this is the 64-point transform. An address of 6 binary digits is 3 digits for the column and 3 for the
row. The sign rule of step 1 counts shared 1-bits, and the shared bits of the two halves add up. So the
64-point sign is the 8-point sign for the column times the 8-point sign for the row. Running the circuit
along the rows puts the first of these signs on every term. Running it along the columns then puts the
second on. Each term ends with the product of the two, which is the 64-point sign.

For N = 8^j it is the same with j directions. I call one pass over one direction a *layer*.

- One layer is N/8 = 8^(j-1) uses of the circuit: 20 · 8^(j-1) operations.
- There are j layers: 20 · j · 8^(j-1) operations. Each layer halves, so the result is H x / 2^j.
- One multiplication by 2^j per output removes the factor: 8^j more.

Total: **20 j 8^(j-1) + 8^j**, which is the same number as (5/6) N log2 N + N. The 5/6 is 20/24: three
textbook layers cost 24 operations per 8 values, and one of these layers does the same work for 20.

| points | j | in the layers | at the end | total | textbook |
|---|---|---|---|---|---|
| 8 | 1 | 20 | 8 | 28 | 24 |
| 64 | 2 | 320 | 64 | 384 | 384 |
| 512 | 3 | 3,840 | 512 | **4,352** | 4,608 |
| 4,096 | 4 | 40,960 | 4,096 | **45,056** | 49,152 |

So 512 points is the first size below the textbook. When log2 N is not a multiple of 3, a textbook layer
serves each digit left over; that is checked by the Python programs, not by Lean.

**Check.** Compute the count at 512 points by hand: 20 × 3 × 64 + 512.

<details><summary>Answer</summary>

3,840 + 512 = 4,352, which is 256 below 4,608. `python3 docs/walkthrough.py 7` builds the layers, runs
them, and counts every operation as it is made: on every unit input (one input 1, the others 0) up to 512
points, and on a sample of inputs at 4,096 points.

</details>

---

## Step 8. The best explicit count in print, like for like

The smallest explicit count in count (O) that I found is in this paper: J. Alman and K. Rao, "Faster
Walsh-Hadamard and Discrete Fourier Transforms From Matrix Non-Rigidity", STOC 2023,
<https://arxiv.org/abs/2211.06459>. Their Theorem 1.1: for any field and any N that is a power of 2, at most
(23/24) N log2 N + (13/12) N operations. (A *field* is a system of numbers in which one can add, subtract,
multiply and divide, such as the fractions or the complex numbers.) *Explicit* means a count of the form
c·N log2 N plus a multiple of N, which one can work out at any size. Counts of a smaller order are also known
(step 10), but they give nothing at any size anyone computes.

The proof of their Theorem 6.2 gives the exact count: (22/24) N log2 N additions and subtractions (plus a
little when log2 N is not a multiple of 3), (1/24) N log2 N halvings, and N - 1 multiplications by a power
of two (this split is exact when log2 N is a multiple of 3; their total is exact at every size). For N a
power of 8 that is (23/24) N log2 N + N - 1.

The comparison is like for like: the same task (exact H x), and the same three things charged.

| at 8 points | additions and subtractions | halvings | multiplications by a power of two | total |
|---|---|---|---|---|
| Alman and Rao | 22 | 1 | 7 | 30 |
| this circuit | 19 | 1 | 8 | 28 |

Theirs are made on the inputs, at the start; mine on the outputs, at the end.

| points | textbook | Alman and Rao | this construction |
|---|---|---|---|
| 8 | 24 | 30 | 28 |
| 64 | 384 | 431 | 384 |
| 512 | 4,608 | 4,927 | **4,352** |
| 4,096 | 49,152 | 51,199 | **45,056** |

Their exact count first falls below the textbook at 2^24 = 16,777,216 points, and the bound of their
Theorem 1.1 at 2^27 points. Mine does at 512.

Where their result is wider than mine: it covers every power of two and any field, in a refereed paper. My
Lean statement covers the powers of 8, over the complex numbers. And the method is theirs: split the
8-point table into a part of low rank (rows that are all multiples of one row, or sums of a few such) plus
a sparse part (few entries that are not zero), and halve once (step 6). In the circuit of step 5 the centre
plays the first part and the sign flips the second. What the search added is which values to share inside
the 8-point step: 19 additions where theirs has 22.

In count (G) the comparison is with the 1994 paper of step 4, and it is like for like too: 19 against 22
at 8 points (step 5).

**Check.** Put 512 points into their formula: (23/24) × 512 × 9 + 512 - 1.

<details><summary>Answer</summary>

512 × 9 = 4,608. 4,608 × 23/24 = 192 × 23 = 4,416. 4,416 + 511 = 4,927.
`python3 docs/walkthrough.py 8` prints both tables from the formulas and finds the three crossing points.

</details>

---

## Step 9. What Lean proves, and what it does not

Lean is a proof assistant: a program that checks a proof line by line and accepts nothing it cannot check.
One statement of this work is checked by Lean. Here it is, cut into five lines:

```
1   theorem OAI.ExactFourier.WHT8Half.hadamard_pow8_circuit (j : ℕ) :
2       ∃ C : Circuit (2 ^ (3 * j)),
3         C.Computes (hadamard (3 * j))
4         ∧
5         C.size ≤ 20 * (j * 8 ^ (j - 1)) + 8 ^ j
```

1. The name, and "for every whole number j".
2. "There is a circuit C on 2^(3j) = 8^j inputs." `Circuit` is OpenAI's definition
   ([Core.lean](../lean/OAI/Computability/FourierCircuit/Core.lean)): a list of gates and a choice of
   outputs. A gate adds two earlier values, subtracts them, or multiplies one by a constant. A value may
   be used as often as one likes.
3. "C computes H": for every list x of complex numbers, the outputs are exactly H x. `hadamard k` is the
   table of step 1 on 2^k points, defined by the rule of shared 1-bits.
4. "and".
5. "C has at most 20 j 8^(j-1) + 8^j gates": the count of step 7. Every gate costs one, so this is
   count (O). (For j = 0, a single point, Lean reads 0 - 1 as 0 and the bound is 1. That case says nothing
   of interest.)

**How it was checked.** On 11 October 2026 the folder `lean/` of this repository was built from nothing on
one rented Linux machine, and Lean accepted the files with no error. [VERIFY.md](../VERIFY.md) has the
commands and what they print. The theorem rests only on the three standard axioms, the
basic assumptions that almost every Lean proof uses. The proof is in [TensorPow8.lean](../lean/Work/SmallWHT/TensorPow8.lean); the 20 gates are data in
[H8Half.lean](../lean/Work/SmallWHT/H8Half.lean); the statement alone, with no proof, is in
[ChallengeWHT8.lean](../lean/Work/SmallWHT/ChallengeWHT8.lean).

**What it does not prove.**

- Nothing in count (G): not the 19 operations of step 5, and not the 7 of step 4.
- Nothing for sizes that are not powers of 8.
- Not that the count is the smallest possible, and not that it is new.
- It says that a circuit exists. Above 8 points it does not write the gates out.
- No person has read the Lean files, including the definition `hadamard`, which was written that night.
  The check is one build, on one machine.

**Check.** Put j = 3 into line 5.

<details><summary>Answer</summary>

20 × (3 × 64) + 512 = 4,352: the 512-point number of step 7. The proof file, `TensorPow8.lean`, states it
as its own theorem, `hadamard_512_circuit`. `python3 docs/walkthrough.py 9` reads the 20 gates out of
`H8Half.lean`, compares them with the 20 lines of step 6, and runs them. It does not run Lean.

</details>

---

## Step 10. What this is not, and three questions to expect

- **Not a better exponent.** My count divided by the textbook's is 5/6 + 1/log2 N. It falls towards 5/6
  and stops there. A better exponent means a count that, for large N, gets below every fixed fraction of
  N log2 N, so that the ratio falls towards 0. The name comes from counts of the form N (log2 N)^z with z
  below 1; z is the exponent. OpenAI's result of 25 September 2026, for the Fourier transform, is of that
  stronger kind, and so is my repository wht-power-saving-lean for this transform, in a model of a computer
  with memory; this is not. Those results give nothing at any size anyone computes: their hidden constants
  are far too large.
- **Not a faster program.** The 8-point step was written into the generated code of FFHT, a tuned
  open-source library for this transform, in place of its block of 24 additions and subtractions. On the
  one machine that was timed, this did not make FFHT faster at any size from 2^6 to 2^26 points (from 2^5
  in double precision): all 129 combinations of size and form took more time than a second build of FFHT's
  unchanged code. The likely reason is that the operations of the new step wait for one another in a chain
  of 7, where the textbook's chain is 3; that is an explanation that fits, not a finding. It is time on one
  machine in one library, and it says nothing against the counts. [The README](../README.md) has the
  section, and [the page on FFHT](../tools/circuits/fast/wht56/results/ffht/README.md) every number.
  On 22 October 2026 the step was timed again, in a program that keeps FFHT's sequence of steps, on four
  processors, against the best textbook code in the same program. On AMD Zen 4 and Zen 5 it took a few
  percent less time, in one run each, not yet read by a second agent and below the bar of 10 % that I had
  set before the runs (0.940-0.952 and 0.977-0.996 of the fastest rival's time, in double precision, over
  builds by two compilers); on AMD Zen 2 there was no clear gain, and on an older Intel processor it was slower. My first figure that day,
  11-15 % less time on Zen 5, was wrong: the rival code carried avoidable register copies, and I retracted
  it. [The measurements of 22 October](../measurements/2026-10-22/README.md) have every number.
- **Not a better chip, except in one setting.** As hardware, where a doubling is only wiring, the 19-line
  circuit of step 5 is 19 adders against the textbook's 24 (an adder adds or subtracts two numbers). Built
  with open-source tools for one programmable chip, as one block of adders with no registers inside (a
  register is a row of one-bit memories between the adders, which lets the chip run at a faster beat), it
  takes 274 of the chip's units, called logic cells, against 349 (273 against 337 with another setting of
  the tools). It is twice as deep, so it is slower by the tools' estimates, it is larger than the textbook
  once registers are added for speed, and a 22-adder design from print is smaller on that chip. On a
  second kind of chip, a Xilinx Artix-7, it took more space than the textbook once placed (22 October 2026).
  [The README](../README.md) has the section "In hardware".
- **Not known to be the best possible.** I know no proof that 8 points need 19 operations, or that 5/6
  cannot be lowered.
- **New only as far as a search goes.** I did not find these counts in the literature I searched. The two
  older papers that matter most were read. The 1994 paper of step 4, <https://doi.org/10.1109/78.285664>,
  gives 22 operations at 8 points by its formula and the rate 7/8. Grigoryan and Agaian (2000),
  <https://doi.org/10.1109/78.815487>, state a count of about six additions per point. That count is an
  undercount: the recursion its algorithm follows adds up to exactly N log2 N.
  [The note](../notes/explicit-circuits.md), section 7, has the computation, says who read the papers, and
  lists what was not read.
- **Not found by hand.** Computer searches run by AI agents found the circuits, in one night.

**Three questions a specialist is likely to ask.**

1. *Is this already known?* I do not know of it in print. The search covered the papers that cite Alman
   and Rao or the 1994 paper, mostly by title and abstract, and arXiv and patents. It did not cover
   everything: the note, section 7, lists what was not read. It did not cover the hardware literature on
   shift-and-add synthesis of constant matrices, which counts adders the way count (G) does. If you know a
   smaller count, I would be glad to hear of it and will credit it.
2. *Is the comparison with Alman and Rao fair, and how far does it reach?* It is the same task with the
   same three things charged (step 8). It is narrower than their result in three ways. Lean covers the
   powers of 8 only; the other powers of two rest on Python checks up to 16,384 points (the README gives the
   command). Lean's statement is over the complex numbers; it is not stated for other fields. And it uses
   N multiplications by a power of two, on the outputs, where Alman and Rao use N - 1, on the inputs.
3. *Does it go further?* Alman and Rao's paper turns a count for this transform into a count for the
   Fourier transform. My count has not been put through that, so I claim nothing there. The smallest
   circuit at 16 points has not been looked for beyond local searches. And it does not touch the exponent.

**Check.** What is the ratio of my count to the textbook's at N = 8^10 points, where log2 N = 30?

<details><summary>Answer</summary>

5/6 + 1/30 = 26/30 = 0.8667. At 8^100 points it is 0.8367, and at 8^1000 points 0.8337: never below
5/6 = 0.8333. `python3 docs/walkthrough.py 10` prints the ratio at seven sizes.

</details>
