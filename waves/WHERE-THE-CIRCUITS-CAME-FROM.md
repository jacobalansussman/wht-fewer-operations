# Where the circuits came from

This page follows the two results of this repository back through the ten waves, step by step, and names
the report behind each step. It is for a reader who wants to check where a number was first computed, who
computed it again, and what was only argued. Step 4 explains the two strategies behind the two results,
where they meet, and what came of trying to combine them.

**Status.** The steps below were taken by AI agents (Anthropic's Claude) that I directed on the night of
10 to 11 October 2026. No person has reviewed their reports. One statement was checked by Lean, a proof
assistant: a program that checks a mathematical proof step by step (step 6). Everything else rests on
programs that replay the circuits in exact arithmetic, or on arguments made by hand that night.

**Marks.** After each step: **[computed]** an exact run by a program; **[argued]** by hand, checked by
nobody outside the agents; **[read]** from a paper or a file; **[Lean]** checked by Lean. The reports
themselves write [ran] for computed, [derived] for argued and [guess] for guessed.

## The words

- **N** is the number of points, a power of two, N = 2^k. The **address** of a point is its number written
  with k binary digits, its **address bits**.
- The **transform** of a list x of N numbers is H x, where H is the N by N table of +1 and −1 with −1
  exactly where the row number and the column number have an odd number of 1-bits in common. The **exact
  transform** is H x itself, as against H x with every output multiplied by one common number.
- A **circuit** is a list of lines. Each line makes one new **value** from one or two earlier values; the
  first values are the inputs. Every value is a fixed combination of the inputs, so it can be written as
  a list of N numbers, one per input: its **entries**. A **helper** is a value that is not an output.
- The **textbook** program is the butterfly: k **levels**, one per address bit, each of N additions and
  subtractions, N log2 N operations in all.
- **Count (G):** one operation is one a·u + b·v with any constants a and b, so a multiplication by a
  constant rides free inside an addition. The reports call an operation in this count a *gate*.
- **Count (O):** every addition, every subtraction and every multiplication by a constant costs one. This
  is the gate set of OpenAI's circuit model, the definition of a circuit in the Lean files that OpenAI
  published in September 2026 with its own result on the Fourier transform. It is the count in which
  Alman and Rao (2023) state their result, and the one in which my Lean statement is made.
- A **halving** is a multiplication by 1/2. A **doubling** is a multiplication by 2.
- The **rate** of a family of circuits is the number in front of N log2 N in its count.
- To use a small circuit **in layers** is to apply it to a few address bits at a time, group of addresses
  by group, until every bit has been used. The textbook is the 2-point circuit in layers.
- A **block** of addresses is the set of addresses that agree on some chosen bits. Fixing the bits one
  after another, always in the same order, cuts the addresses into halves, quarters and so on. I call
  one such order **a way of halving the addresses**.
- A value **ties together** some address bits when its entries cannot be written as a pattern on some of
  those bits times a pattern on the others.

Full references for the papers named below are in the section "Earlier papers" of
[README.md](README.md#earlier-papers).

## The results being traced

1. Count (G): 19 operations at 8 points, 52 at 16, and a family with (3/4) N log2 N + N/4 operations at
   every N = 2^k. Replayed by programs. Not in Lean.
2. Count (O): the exact transform on N = 8^j points in (5/6) N log2 N + N operations, from an 8-point
   circuit of 19 additions and subtractions and one halving. The count is checked by Lean.

## Step 0. The starting brick: four points in 7 operations (1994)

The 4-point transform costs 8 operations by the textbook. Coppersmith, Feig and Linzer (1994) do it in 7.
They compute one value that differs from three of the four outputs in a single sign, and get each of those
outputs by adding twice one input. Their count is of multiply-adds, ±a ± b·c, each costing one, and they
give (7/8) N log2 N for N a power of four and N/8 more for an odd power of two. By that formula 8 points
cost 22 and 16 points cost 56. They claim no lower bound. **[read: by the agents, from a copy of the paper
I obtained, on the morning of 11 October, outside the waves]**

The waves did not know that paper. The first wave met the same circuit on its own, twice:

- [i-cousins](wave-01/i-cousins.md) wrote a 7-gate circuit for 4 points and checked it on the unit inputs
  (one input 1, the others 0), and noted that composing it gives at most 22 at 8 points and 56 at 16.
  **[computed]** for the 7, **[argued]** for the 22 and the 56.
- [i-play](wave-01/i-play.md) found it as "the sum of all four, minus twice each input", listed 228
  different sets of helpers that give 7 operations, and replayed 22, 56 and 336 operations at 8, 16 and 64
  points. **[computed]**

So the numbers every later report starts from, "7, 22, 56", are the 1994 numbers. The reports call the
4-point circuit "the brick". Where they credit it, they credit Alman and Rao or a patent filed in 2002
([lit-constants](wave-03/lit-constants.md)); the credit belongs to the 1994 paper.

**Is 7 the least at 4 points?** Three reports argue by hand that 6 operations are not enough in count (G)
([j-failproof](wave-02/j-failproof.md), [g-1](wave-03/g-1.md), [r-2](wave-05/r-2.md)), and exhaustive
searches in arithmetic modulo small primes agree. **[argued; computed modulo primes]** j-failproof's
argument is the case N = 4 of a bound for every size: at least 2N − 1 operations, which is 15 at 8
points. After the waves, on the morning of 11 October, a proof of that bound was written out for my
paper on these circuits. One AI agent read it and found no gap, and a program checked two steps of it at
4 and 8 points. No person has checked it, and the 1994 paper does not state it. Until a person has, read
"7 is the least at 4 points" and "at least 15 at 8 points" as argued.

## Step 1. The second wave: 21, then 20, then the family (count (G))

- Two agents each found 8 points in 21 operations: [e-2](wave-02/e-2.md) and [e2-3](wave-02/e2-3.md).
  **[computed]**
- [e2-0](wave-02/e2-0.md) was asked to try to establish a lower bound and to keep whatever stopped the
  attempt. It supposed that a program holds only *pieces*: one output restricted to a block of inputs. A
  plain local walk over sets of helpers, started from the 22-operation circuit, fell to 21 and then to 20
  in three seconds. **[computed]**
- Read line by line, the 20 holds a value that is not a piece. e2-0 calls it a **hub**: one half-size
  output on the lower half of a block plus a different half-size output on the upper half. A hub is one
  operation away from four outputs, and the second value that this operation needs was made two levels
  below. So one helper serves two neighbouring levels.
- Used as a rule at every size, this gives the family: (3/4) N log2 N + N/4 operations, which is 7, 20, 52,
  128, 304 at 4 to 64 points, with constants ±1 and ±2 only. e2-0 derived the count for every k from a
  short recursion and ran it for 4 to 64 points. **[argued for every size; computed at 4 to 64 points]**

Who computed it again:

- [b-0](wave-02/b-0.md), a critic, wrote a generator of its own, sharing no code with e2-0, and replayed
  every size from 4 to 4,096 points in exact whole numbers; it also read e2-0's files with a reader of its
  own. **[computed]** It then searched exhaustively at 8 points: inside the family's own kind of circuit
  (pieces and hubs on one fixed way of halving the addresses) no circuit has 19 operations or fewer.
  **[computed; one program, not cross-checked]**
- [c-1](wave-03/c-1.md), a second critic, re-derived the recursion in ten lines and reproduced the counts
  from 4 to 8,192 points with a program of its own. **[argued; computed]**
- [h-1](wave-04/h-1.md) argued that inside that kind of circuit the family's count cannot be improved.
  **[argued by hand; not checked by a program]** That is a statement about one kind of circuit. The next
  step leaves that kind.

## Step 2. The third wave: eight points in 19 (count (G))

[g-1](wave-03/g-1.md) had been asked to referee an argument about "tight wires" (part 3 of
[LEADS.md](LEADS.md), door 1, explains the term). On the way it ran a random search over sets of helpers
(simulated annealing) inside a pool of 304 candidate values at 8 points, started from the 22-operation
circuit. All four runs fell to 21, 20 and then 19 within seconds, and none found 18. Started from
nothing, the same program found no circuit at all. **[computed]**

The 19 operations, as g-1 printed them:

```
g1 = x0 + x7     g2 = x1 + x6     g3 = x2 - x5     g4 = x3 - x4
g5 = g1 - g2     g6 = g3 + g4
g7 = g5 - g6                         the centre: signs + - - - + + - + ; not an output
g8 = g7 - 2 x7   g9 = g7 - 2 x5
g10 = g8 + 2 x6  g11 = g9 - 2 x4
y7 = g10 + 2 g4  y1 = g10 + 2 g3     y6 = g11 + 2 g2   y0 = -g11 + 2 g1
y2 = g8 + 2 x1   y3 = g9 + 2 x3
y4 = y2 + 2 g6   y5 = -y3 + 2 g5
```

Seven operations merge the eight inputs into one value, the centre. Twelve more each flip some signs, by
adding twice an input or twice a value that the merging left behind. Every second operand in those twelve
lines is an input or a value already paid for.

Who computed it again, and what was shown about 19:

- g-1 replayed it with three separate programs. [c-0](wave-03/c-0.md), a critic, read only the text file of
  the circuit and replayed it with its own code. **[computed]**
- Inside the design "one merge of the inputs, then a walk of sign flips", 19 is the least at 8 points: an
  exact program of g-1, and a second one of c-0 that also covers every *balanced* way of merging, where
  the inputs are joined two at a time, then the pairs, then the fours (315 ways). **[computed]** Later,
  [v-0](wave-06/v-0.md) showed by exhaustive search that 19 is the least in a second kind of circuit:
  every value a list of 0, +1, −1 whose non-zero places form one block of a single way of halving the
  addresses. **[computed; the program exhausts a counting game whose rules v-0 derived by hand in the
  same half hour, and nobody has read it]**
- None of this says that 19 is the least over all circuits. Whether 18 is possible is open
  ([LEADS.md](LEADS.md), lead 1.4).
- [h-1](wave-04/h-1.md) read the 19 in the family's language: it is a hub on two address bits that are not
  neighbours (bits 0 and 2), plus two values that tie three bits together and are each shared by two sign
  flips. That sharing is the 2 in 19 = 21 − 2. **[computed for the reading of each value; argued for the
  count 21]**

## Step 3. From 19 to 20 operations with one halving, and to 5/6 (count (O))

In count (O) the 19 lines above would cost more than 19, because each "2 ·" is a multiplication. The way
round is in the first lines of [g-1](wave-03/g-1.md): halve the centre once, right after g7. Then every
"2 ·" below it goes away, because the second operand is already twice as large as the halved centre needs
it to be. The result is 19 additions and subtractions and one halving, 20 operations, and the outputs are
the rows of H divided by 2. **[computed]**

**The halving is not new, and the method is not mine.** Alman and Rao (2023) halve once in their 8-point
step and pay for the factor by multiplying the inputs by powers of two, N − 1 multiplications in all. Their
step has 22 additions and subtractions and one halving, 23 operations. What the search added is a step with
19 additions and subtractions, 20 operations. The rest of the 5/6 count is the same bookkeeping, with the
factor put right on the outputs (N multiplications) in place of the inputs. Two critics said so that night ([c-0](wave-03/c-0.md), [n-0](wave-04/n-0.md)). **[read]**

From there to the published count:

- **g-1** ran three layers of the 20-operation circuit: H x / 8 at 512 points in 3,840 operations
  **[computed]**. It counted 512 final multiplications by 8 to get H x itself in 4,352, against the
  textbook's 4,608, and wrote the law (5/6) N log2 N + N for N a power of 8. **[argued: the final
  multiplications were counted, not run]**
- **[c-0](wave-03/c-0.md)**, the critic, ran the final multiplications as operations: 4,352 at 512 points,
  9,728 at 1,024 and 45,056 at 4,096, each compared with the exact transform. It read OpenAI's file
  `Core.lean` and confirmed that a gate there is an addition, a subtraction or a multiplication by any
  constant, one unit each, and that the circuit must compute H x itself, not a multiple. **[computed;
  read]**
- **[h-3](wave-04/h-3.md)** wrote the programs to files for every size from 2 to 512 points, had them
  replayed by a separate reader and by e2-0's checker, and gave the rule that explains the count: the
  count-(O) price of a count-(G) circuit is its operations plus the number of extra copies of values that
  must be **held at two scales** (a value v is needed once as v and once as 2v or v/2, and making the
  second copy costs one multiplication). The 8-point circuit has one such value, the centre.
  **[computed; the rule is argued]**
- **[n-0](wave-04/n-0.md)**, a second critic, wrote a checker from nothing and a builder that orders the
  work differently, replayed h-3's files, and checked 4,096 points on every unit input: 45,056. It gave
  the count for every power of two: (5/6) N log2 N + (1 + (k mod 3)/6) N, with a textbook layer for each
  address bit left over. **[computed to 4,096 points on all unit inputs; spot checks to 32,768]** It also
  corrected one sentence of h-3: "56 operations at 16 points, where the list had 60" compares two different
  outputs (H x / 2 and H x / 4).

At 8 points itself the exact transform costs 28 this way, above the textbook's 24. The count is below the
textbook from 512 points on.

## Step 4. The two strategies, and whether they combine

Both results grow from the same brick, the 1994 idea of a helper that is one sign flip away from several
outputs. They share that helper in two different ways.

- **The 3/4 strategy (the family).** One hub serves two neighbouring levels of the transform. Every pair of
  neighbouring levels saves N/4 operations, where the 4-point circuit in layers saves N/4 on every second
  pair.
- **The 5/6 strategy (the 8-point circuit in layers).** One centre serves all eight outputs of a block,
  through a walk of sign flips, and the values left over from building the centre are the second operands
  of the walk.

**Why each wins in its own count.** [h-3](wave-04/h-3.md) gives the reason. In count (G) only the
additions and subtractions are charged. In count (O) there is one more charge for every value that must
be held at two scales, and that charge is one halving.

| | additions and subtractions, per N log2 N | halvings, per N log2 N | count (G) rate | count (O) rate, outputs up to one common factor |
|---|---|---|---|---|
| textbook | 1 | 0 | 1 | 1 |
| the 4-point circuit with one halving, in layers (Alman and Rao, 2023, their Algorithm 9) | 7/8 | 1/8 | 7/8 | 1 |
| the family | 3/4 | 1/8 | **3/4** | 7/8 |
| the 8-point circuit in layers | 19/24 | 1/24 | 19/24 | **5/6** |

**[computed for the circuits up to 512 points; the rates are what the counts tend to]** The second row
is not the 1994 circuit as printed: that one has no halving, and with its three doublings charged it
costs 10 at 4 points in count (O).

So the family is ahead in count (G), 3/4 against 19/24, and the 8-point circuit is ahead in count (O), 5/6
against 7/8: over three levels it needs one halving where the family needs three. For the exact
transform count (O) charges one more multiplication per output at the end, which is the "+ N"; Alman and
Rao pay the same kind of charge on the inputs, N − 1. The family's count (O) form gives the scaled transform H x / √N for N a
power of 4 in (7/8) N log2 N + N/4 operations (60 at 16 points), and the exact transform only in
(7/8) N log2 N + (5/4) N, which is first below the textbook at 4,096 points ([b-0](wave-02/b-0.md),
[c-1](wave-03/c-1.md)). **[computed]**

**Where the two meet.**

- In count (G) the best circuit on file is the 8-point circuit at 8 points (19 against the family's 20), and
  the family from 16 points on (52 against 54 by layers), with a tie at 64 points (304 both ways).
  **[computed]**
- **What bringing them together would mean, in numbers.** The family has the fewer additions (3/4) and the
  8-point circuit the fewer halvings (1/24). A circuit with the family's 3/4 and fewer than 1/12 halvings
  would beat 5/6 in count (O). With 1/24 halvings its rate would be 19/24, which is 43,008 operations at
  4,096 points in place of 45,056. **[my arithmetic on the table above; no such circuit is known]**
- **The one circuit on file that mixes them.** [h-1](wave-04/h-1.md) interleaved the 19 across levels the
  way the family interleaves the 4-point circuit. Its random search, started from two copies of the 19
  under a textbook level (54 operations), landed on a second circuit with 52 operations at 16 points, of
  a different shape from the family's 52: in h-1's words, "two unfinished 19s under a top level". It ties
  the family in count (G) and found nothing below (3/4) N log2 N. **[computed by random search; such a
  search gives upper bounds only]**
- **That mix in count (O).** The waves never priced it. Priced on 11 October with h-3's program, it costs
  at most 62 operations for H x / 2 (52 and 10 extra copies), where one layer of the 20 and one textbook
  layer cost 56 for the same output, and the family costs 60 for H x / 4. **[computed twice on 11 October
  by AI agents checking this folder; the program stopped at its limit of 4 million steps, so 62 is an
  upper bound, and with a smaller limit the same program stops 8 above the proved price of the family's
  52]** So the one mix that the waves left on file
  does not beat either strategy in count (O). This is lead 1.1 of [LEADS.md](LEADS.md), with the command.
- **Tried on 11 October, after the waves: the two do not combine in count (O).** Three AI agents built
  six ways of putting levels of the family together with the 8-point circuit and replayed them. For the
  exact transform, from 64 points on, every mix that is not the layers themselves costs more than the
  layers. For the family's own wiring there is an argument that count (O) cannot go below
  (7/8) N log2 N however its values are scaled: the family uses one value at two levels, once as it is
  and once doubled, and when doubling is charged each hub needs one more halving on every second level.
  The least count for that wiring, computed exactly at 4 to 64 points, agrees: 60 at 16 points with a
  common factor, against 56 by layers. The 8-point circuit shares values only inside its own three
  levels, so it pays for one halving. **[computed and argued on 11 October by AI agents, outside the
  waves; their programs are not in this repository; read by no person; not in Lean]** This covers the
  family's wiring and those six mixes, not every circuit. Lead 1.2 of [LEADS.md](LEADS.md) has the
  numbers and what is still untried.

In short: nobody has put the two ideas into one circuit that beats both. In count (G) one random search
tried and tied. In count (O) six mixes were built and none beats the layers, and the family's own wiring
cannot. A direct search for a new 16-point circuit in count (O) has not been made.

## Step 5. Neither circuit is about this transform in particular

H is built from the 2 by 2 block with rows (1, 1) and (1, −1), one address bit at a time. Put another 2 by
2 block with four non-zero entries in its place and the same wiring still works, with other constants.

- [k-cross](wave-03/k-cross.md): the 19 for nine other blocks, six of them written out and replayed.
- [c-0](wave-03/c-0.md): the 19 for 300 random blocks, solving every constant as an exact linear system.
- [h-6](wave-04/h-6.md): the family for every block without a zero entry, and the 19 after renaming the
  inputs.
- [ag-8](wave-10/ag-8.md), in the last wave: a census of every record (7, 19, 20, 52, 128, 304) with the
  block left general.

**[computed in each case; not proved]** Blocks with a zero entry, such as the one for subset sums, are
not covered: there the recipe divides by zero. For the search for a change of order this was the main
lesson of the night: no saving found uses anything that only the Walsh-Hadamard transform has.

## Step 6. What was proved in Lean, and what was only replayed

The Lean work is not part of the waves. It was done the same night, on a separate track, and is described
in [notes/explicit-circuits.md](../notes/explicit-circuits.md), section 6, with the limits of that check.

- **[Lean]** For every j there is a circuit on 8^j inputs, in OpenAI's circuit model, that computes the
  exact transform and has at most 20 j 8^(j−1) + 8^j gates. That number is (5/6) N log2 N + N for N = 8^j.
  The 20 gates of the 8-point circuit are data in the file
  [lean/Work/SmallWHT/H8Half.lean](../lean/Work/SmallWHT/H8Half.lean), with a proof that they compute
  H / 2. No person has reviewed the Lean files.
- **Replayed by Python programs only:** the 19 operations at 8 points in count (G); the 52 at 16; the family
  and its count; the count (7/8) N log2 N + N/4 for the scaled transform. Each circuit is written to a text
  file, read back and run exactly on every unit input. One command in
  [tools/circuits/](../tools/circuits/) does it again.
- **Argued only:** the family's count beyond the sizes that were replayed (a short recursion, checked twice
  by the agents). Every "least" on this page holds inside one named kind of circuit; none is over all
  circuits.
- **Not in Lean, and not replayed outside the night:** everything else in this folder.

## Step 7. What the comparison with earlier work rests on

During the third wave [lit-constants](wave-03/lit-constants.md) searched for published counts for under
half an hour. It found 7/8 as the best published rate when doublings are free, and Alman and Rao's 23/24
when every operation is charged. **[read]** That search missed the 1994 paper. It was found by a later
search and read on the morning of 11 October, outside the waves, and so were seven pages of a paper of
2000 whose abstract states about six additions per point.

- The 1994 paper counts one multiply-add as one operation. Every line of the count-(G) circuits here has
  two terms and at most one multiplication by a constant, so each line is one of their operations, and the
  comparison is in their own count: 19 against 22 at 8 points, 52 against 56 at 16, 3/4 against 7/8.
  **[read; the shape of every line counted by `tools/circuits/multiply_add_check.py`]**
- The count stated by Grigoryan and Agaian (2000), 6·2^r − r² − 3r − 6 additions for 2^r points, is too
  small: the recursion its algorithm follows adds up to exactly N log2 N. **[read; computed]**

What was searched in the literature, and what is still not read (Morgenstern's paper of 1973 and pages
173 to 177 of the 2000 paper among it), is in
[notes/explicit-circuits.md](../notes/explicit-circuits.md).

## The trace in one table

| step | what | first report | computed again by | mark |
|---|---|---|---|---|
| 0 | 4 points in 7 operations; 22 and 56 by layers | Coppersmith, Feig, Linzer (1994); met again by [i-cousins](wave-01/i-cousins.md), [i-play](wave-01/i-play.md) | every later report | read; computed |
| 1 | 8 points in 21 | [e-2](wave-02/e-2.md), [e2-3](wave-02/e2-3.md) | | computed |
| 1 | 8 points in 20; the family 7, 20, 52, 128, 304; rate 3/4 | [e2-0](wave-02/e2-0.md) | [b-0](wave-02/b-0.md) to 4,096 points, [c-1](wave-03/c-1.md) to 8,192 | computed; the count for every size argued |
| 2 | 8 points in 19 | [g-1](wave-03/g-1.md) | [c-0](wave-03/c-0.md) | computed |
| 3 | 20 operations with one halving; (5/6) N log2 N + N | the halving: Alman and Rao (2023), who scale the inputs where this scales the outputs; the 19: [g-1](wave-03/g-1.md) | [c-0](wave-03/c-0.md), [h-3](wave-04/h-3.md), [n-0](wave-04/n-0.md) to 4,096 points | computed |
| 4 | the price rule that relates the two counts | [h-3](wave-04/h-3.md) | [b-0](wave-02/b-0.md) priced the family the same way | computed; the rule argued |
| 4 | a circuit that mixes the two strategies: 52 at 16 points in count (G), at most 62 in count (O) | [h-1](wave-04/h-1.md); priced on 11 October | | computed; upper bounds |
| 5 | both circuits work for other 2 by 2 blocks | [k-cross](wave-03/k-cross.md), [h-6](wave-04/h-6.md) | [c-0](wave-03/c-0.md), [ag-8](wave-10/ag-8.md) | computed |
| 6 | the count at N = 8^j | Lean files in [lean/Work/SmallWHT/](../lean/Work/SmallWHT/) | | Lean |
