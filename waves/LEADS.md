# What is still open, and what is closed

This page is the place to start if you want to continue the work of the ten waves. It has three parts:

1. [Leads for a better constant](#part-1-leads-for-a-better-constant): small, concrete, cheap to try.
2. [Leads for a change of order](#part-2-leads-for-a-change-of-order): what could, in principle, give fewer than a
   constant times N log N operations. None has a positive example.
3. [Closed doors](#part-3-closed-doors): what was tried and failed, with the exact scope of each failure, so
   that nobody has to try it again.

**Status of everything on this page.** It is a summary, written by AI agents (Claude) at my direction on
11 October 2026, of working reports by AI agents. No person has reviewed the reports. Nothing here is in
Lean, a proof assistant, except where a line says so. A lead is listed because no report closed it, not
because anything speaks for it. I have tried not to make any lead sound more promising than its critics
left it.

**What I am after.** A saving of the 1e-1 kind, N (log N)^0.9 in place of N log N, or a count that grows
like N. Part 2 is about that. Everything in part 1 is below that bar: it is listed because each lead is
cheap and a better constant is a result anyone can check.

**Marks.** **[computed]** an exact run by a program that night. **[computed modulo p]** a run in
arithmetic with remainders after division by a prime p: evidence, not a statement about circuits with
fractions. **[argued]** by hand that night, read at most by another agent. **[guessed]**. **[read]** from a
paper or a file. The reports write [ran], [derived] and [guess] for the first, third and fourth.
**[checked 11 October]** marks the few runs made on the morning after, by AI agents that checked this
folder with the reports' own programs; the command is given each time.

**One rule.** A search that finds nothing proves nothing. Only an exhaustive search gives a "no", and then
only for the kind of circuit, the size and the arithmetic it ran in. Each entry says which it was.

## Words

- **N** = 2^k points. The **address** of a point is its number in k binary digits, its **address bits**.
- The **transform** is H x, with H the N by N table of +1 and −1 (−1 where row and column have an odd
  number of 1-bits in common). The **textbook** program costs N log2 N operations, in k **levels**, one
  per address bit.
- A **circuit** is a list of lines; each line makes one new **value** from one or two earlier values. A
  value is a fixed combination of the inputs, so it is a list of N numbers, its **entries**. The reports
  say *gate* for a line and *wire* for a value. A **helper** is a value that is not an output. A
  **record** is a circuit with the smallest count known that night for its size.
- **Count (G):** one operation is any a·u + b·v. **Count (O):** every addition, subtraction and
  multiplication by a constant costs one; it is the count of the circuit model in OpenAI's Lean files
  ([README.md](README.md#earlier-papers)). A **halving** is a multiplication by 1/2.
- **Outputs.** In count (O) "the exact transform" means H x itself. "Up to one common factor" means every
  output multiplied by the same number, such as H x / 2. The programs differ in what they accept, and a
  "better" circuit can be an artefact of that: `mincirc` (subset sums, count (G)) accepts any multiple of
  an output; h-3's `oprice.py` wants each output as written, not its negative; the Lean statement needs
  H x itself.
- A small circuit **in layers** is applied to a few address bits at a time until all bits are used. The
  **rate** of a family is the number in front of N log2 N.
- **The 19:** the 8-point circuit with 19 operations in count (G). **The 20:** the same circuit in count
  (O), 19 additions and subtractions and one halving, giving H x / 2. **The family:** the circuits with
  (3/4) N log2 N + N/4 operations in count (G): 7, 20, 52, 128, 304 at 4 to 64 points.
  [WHERE-THE-CIRCUITS-CAME-FROM.md](WHERE-THE-CIRCUITS-CAME-FROM.md) describes them.
- A value is **held at two scales** when a circuit needs it once as v and once as 2v or v/2. In count (O)
  the second copy costs one multiplication.
- **Subset sums:** for every set S of address bits, the sum of the data at all addresses whose 1-bits lie
  in S. The usual method (Yates) costs (N/2) log2 N additions.
- The **class:** H is built, one address bit at a time, from the 2 by 2 block with rows (1, 1), (1, −1).
  The class is every table built the same way from a block (1, 1), (1, τ). The transform is τ = −1,
  subset sums are τ = 0. A **class identity** is one circuit whose constants are formulas in τ and which
  is right for every τ where the formulas make sense. The records are class identities, but their
  formulas break down when the block has a zero, so they do not cover subset sums.
- A **block of addresses** is the set of addresses that agree on some chosen bits; **one way of halving
  the addresses** fixes the bits one after another in a fixed order. A value **ties together** some
  address bits when its entries cannot be written as a pattern on some of those bits times a pattern on
  the others.
- A **floor** is a lower bound and a **ceiling** an upper bound. **o(N)** is a quantity that grows more
  slowly than N. **Over the rationals** means with ordinary fractions, as against modulo a prime.
- A **pool** is the list of candidate values a search may use. A **step** of a search is one change it
  tries.

## The circuits on file

| circuit | count | output | file | format |
|---|---|---|---|---|
| the 4-point circuit | 7 (G) | H x | [wave-02/e2-0-pieces/slp_4.txt](wave-02/e2-0-pieces/slp_4.txt) | `name = a * u + b * v` |
| the 19 | 19 (G) | H x | [wave-03/g-1-tightwires/h8_19gates.txt](wave-03/g-1-tightwires/h8_19gates.txt) | `g1 = x0 + x7` |
| the 20 | 20 (O) | H x / 2 | [wave-04/h-3-orecord/o_8.txt](wave-04/h-3-orecord/o_8.txt) | one operation per line |
| the family | 20, 52, 128, 304 (G) | H x | `slp_8.txt` to `slp_64.txt` in [wave-02/e2-0-pieces/](wave-02/e2-0-pieces/) | `name = a * u + b * v` |
| the family in count (O) | 60 at 16 points | H x / 4 | [wave-02/e2-0-pieces/oslp_16.txt](wave-02/e2-0-pieces/oslp_16.txt) | one operation per line |
| the second 52 | 52 (G) | H x | [wave-04/h-1-staircase3/slp16_52_from54.txt](wave-04/h-1-staircase3/slp16_52_from54.txt) | `name = a * u + b * v` |
| the 20 in layers | 56 at 16, 144 at 32, 3,840 at 512 (O) | H x up to a factor | `o_2.txt` to `o_512.txt` in [wave-04/h-3-orecord/](wave-04/h-3-orecord/) | one operation per line |
| the same, exact | 4,352 at 512 (O) | H x | `ox_2.txt` to `ox_256.txt` there; `ox_512.txt` is left out for size ([WHERE.md](WHERE.md) says how to make it again) | one operation per line |
| other circuits with 19 and 20 at 8 points | 19, 20 (G) | H x | printed inside the `.out` files of [wave-07/x-0-twojobs/](wave-07/x-0-twojobs/) and [wave-08/ab-2-tallpool/](wave-08/ab-2-tallpool/), as blocks that begin `CIRCUIT` | a list of values |

The agents wrote circuits in four text formats and no program converts between them. The cleaned copies
in [tools/circuits/programs/](../tools/circuits/programs/) are all in one format, and
`python3 -B tools/circuits/slp.py FILE` checks any file in it and prints both counts. A new circuit
should pass that checker.

---

## Part 1. Leads for a better constant

Twelve leads. For each: the question, what a yes would give in numbers, what has been tried and what is
already on file, where to start, and how long a similar run took that night. Each agent had a box of one
hour; the times below are of single runs inside those boxes. Commands are given from the top folder of
the repository; [WHERE.md](WHERE.md) says what the programs need.

**One thing three of these leads need and nobody has.** Leads 1.1, 1.2 and 1.3 ask for a search whose
goal is the count-(O) price. No such search exists. Every search program on file works in count (G) and
treats v and 2v as one value. The two pricing programs on file take a finished circuit and need from
half a minute to minutes for one 16-point circuit, which is too slow to be the score of a search, and
they return upper bounds when they stop at their limit. An exact price exists only for the family
(b-0's integer programme, which builds its own circuit and takes no file).

### 1.1 Sixteen points in count (O), outputs up to one common factor

**Question.** Is there a circuit that gives H x on 16 points, all outputs multiplied by one common number,
in fewer than 56 operations of count (O)?

**What a yes would give.** Used in layers on four address bits at a time, a 16-point circuit with c
operations costs (c/64) N log2 N + N for the exact transform.
- c = 55 or fewer improves every size whose k leaves remainder 1 on division by 3. At 1,024 points: 9,664
  in place of 9,728.
- c = 53 or fewer brings the rate below 5/6, because 53/64 is less than 5/6. At 65,536 points: 933,888 in
  place of 950,272 (textbook 1,048,576).

**What has been tried.** The 56 on file is not a 16-point design: it is one layer of the 20 and one
textbook layer ([h-3](wave-04/h-3.md), replayed by [n-0](wave-04/n-0.md)) **[computed]**. The best
H x / 4 that n-0 could make from the 56 costs 64. **No search has been run in count (O) at 16 points.**
Alman and Rao write that, despite some effort, they could not design an improved algorithm from a
16-point decomposition **[read]**.

**Already on file.**
- The family's 52 with the common factor left free: 60 for H x / 4, and 8 extra multiplications are the
  least for that wiring and that output; 72 for H x / 2; between 72 and 76 for H x
  ([b-0](wave-02/b-0.md), file `wave-02/b-0/scale_ilp.out`) **[computed; the "least" by an integer
  programme, an exact optimisation over whole-number choices]**. h-3's program gives the same 60 and, for
  the other factors from 1/16 to 4, upper bounds from 73 to 90 (`wave-04/h-3-orecord/oprice.out`).
  On 11 October, after the waves, the least for H x on that wiring was computed: 76 (lead 1.2).
- The second 52, found by [h-1](wave-04/h-1.md): at most 62 for H x / 2, 74 for H x / 4 and 78 for H x
  **[checked 11 October; upper bounds, the program stopped at its limit of 4 million steps]**. So neither
  52 is below 56 as it stands.

**Where to start.**
`python3 -B waves/wave-04/h-3-orecord/oprice.py waves/wave-02/e2-0-pieces/slp_4.txt waves/wave-04/h-1-staircase3/slp16_52_from54.txt`
The first file is the control: it must print 11 for the exact transform and 8 with the factor free. The
second took about three minutes. What is missing is the search: h-3 names the target, fewer than 54
operations in count (G) with at most two values held at two scales, and nothing on file can look for it.
h-1's search (`wave-04/h-1-staircase3/sa2.c`) scores helpers + A·(values it cannot make) + B·(outputs
missing); A and B are its seventh and eighth arguments, and its state is a set of values, not a circuit
with a scale for each value.

**How long.** h-1's count-(G) search fell from 54 to 52 in 48 seconds and then ran tens of millions of
steps inside its hour. b-0's integer programme for the scales gave proved answers at 16 points for
two of the three outputs and was stopped during 32 points; the report gives no time for it.

**Status.** Open. Not searched. The two circuits on file are priced and do not beat 56.

### 1.2 Mixing the 8-point circuit and the family in count (O)

**Question.** Can one circuit keep the family's low number of additions and need fewer halvings than the
family does?

**What a yes would give.** The family has 3/4 N log2 N additions and 1/8 N log2 N halvings; the 20 in
layers has 19/24 and 1/24. Any circuit with 3/4 additions and fewer than 1/12 halvings beats 5/6. With
1/24 it would be 19/24: 43,008 at 4,096 points in place of 45,056.

**What was tried in the waves.** No search in count (O). In count (G), [h-1](wave-04/h-1.md) let one
helper of the 19 serve neighbouring levels, the way the family does with the 4-point circuit, and found
nothing below 3/4 **[computed by random search: upper bounds only]**. Its second 52 is the one mix that
the waves left on file, and in count (O) it costs at most 62 (lead 1.1). [h-3](wave-04/h-3.md) measured
operations saved per halving: 1 for the 4-point circuit with one halving, 2 for the family, 5 for the 20.

**Tried on 11 October, after the waves: nothing below 5/6.** On the morning of 11 October three AI
agents took up this lead, outside the waves. Their programs are not in this repository, so no command is
given here. Section 9 of [notes/explicit-circuits.md](../notes/explicit-circuits.md) reports the same
check. No person has read their work, and none of it is in Lean. The mark **[computed on 11 October]**
below means an exact run by one of their programs.

- **The family's own wiring cannot do it.** Keep every line of the family, and choose freely at which
  power of 1/2 each value is held. A value that is needed at two scales costs one more operation. The
  least count of this kind was computed exactly at 4 to 64 points **[computed on 11 October; at 8 points,
  and at 16 points with a common factor, three programs written separately agree; the other entries rest
  on one program]**. At 4 points it is 8 with a common factor and 11 for the exact transform. From 8
  points on:

  | points | the family's wiring, outputs up to one common factor | the 20 in layers, the same | the family's wiring, exact transform | the 20 in layers, exact transform |
  |---|---|---|---|---|
  | 8 | 26 | 20 | 30 | 28 |
  | 16 | 60 | 56 | 76 | 72 |
  | 32 | 160 | 144 | 176 | 176 |
  | 64 | 352 | 320 | 416 | 384 |

  An argument gives the reason, and a bound for every size **[argued on 11 October]**. The family saves
  by using one value at two levels, once as it is and once doubled. Followed round a short loop of lines,
  from an output to its hub, down to the hub one level below and back, this asks for one value at two
  scales at once, whatever the constants. So every hub costs one more operation on every second level:
  at least (N/4)·floor(k/2) operations on top of the family's (3/4) N log2 N + N/4 lines, which is at
  least (7/8) N log2 N + N/8. At 4, 16 and 64 points the least count that was computed, 8, 60 and 352, is
  exactly the lines plus that number. So for this wiring 3/4 becomes 7/8, which is above 5/6. The
  argument covers the family's lines with any scales and any constants. It does not cover a wiring in
  which some value is made by a line that is not the family's.

- **Six mixes, none below the layers.** Six ways of putting levels of the family together with the
  8-point circuit were written as circuit files and replayed exactly: at 8 to 512 points by a second
  program, and at 4,096 points by the program that built them **[computed on 11 October]**. For the exact
  transform in count (O):

  | design | 64 points | 512 points | 4,096 points | rate |
  |---|---|---|---|---|
  | the 20 in layers (the reference) | 384 | 4,352 | 45,056 | 5/6 |
  | the family alone, with another top level | 416 | 4,736 | 48,128 | 7/8 |
  | the 8-point circuit at the bottom, the family above | 416 | 4,608 | 48,128 | 7/8 |
  | the family at the bottom, layers of the 20 above | 416 | 4,608 | 47,104 | 5/6, and N/2 more |
  | the 8-point circuit, a textbook level, one level of the family, repeated | 416 | 4,608 | 49,152 | 9/10 |
  | the 8-point circuit, a textbook level, three levels of the family, repeated | 384 (it is the layers) | 4,736 | 48,128 | 25/28 |

  From 64 points on, every mix that is not the layers themselves costs more than the layers. At 16 points
  the best block still has 56 operations, and 53 were needed (lead 1.1). The scales in the mixes were
  chosen by hand. An integer programme then looked for a cheaper choice of scales at 32, 64 and 128
  points and found none; in four of its five cases it proved that there is none. Above 128 points the
  scales were not checked for being the least.

**What is still untried.**

- Any wiring other than the family's and those six mixes. In particular the direct search of lead 1.1,
  for a 16-point circuit with 53 or fewer operations in count (O), has not been made. The best known has
  56, and nothing shows that 53 is impossible.
- Circuits that share values between the inside of the 8-point circuit and the levels of the family,
  beyond the six designs. One search for a 16-point circuit with a single centre found 64 operations. It
  tried 500 of 2,048 kinds of centre with a greedy rule, so it proves nothing.
- Larger blocks found by search, at 16 or 32 points, built like the 8-point circuit: one centre and one
  halving.
- Other choices inside the family: which half keeps which output, and the signs of the hubs. They were
  sampled at 8, 16 and 32 points (40, 80 and 12 draws, all with the same bound). At 64 points no valid
  draw came up in 200,000.
- The least counts where the programs reached their time limit. For the family's wiring at 128 points
  the least is between 832 and 864 with a common factor, and at least 928 for the exact transform
  (layers: 768 and 896). At 256 points the exact transform was not decided. The bound above passes the
  count of the layers for the exact transform only when k is above 21. So from 256 points up to that
  size the family's wiring is not proved worse than the layers for the exact transform; it is worse at
  16, 64 and 128 points and ties at 32.
- A lower bound for count (O) in general. Nothing here says that 5/6 is the best possible.

**Where to start.** The programs of the 11 October check are not here; the description above is what a
new program has to reproduce first. On file: the command of 1.1, on h-1's circuits at 16 points, and
for the family at 32 and 64 points with the output factor free, b-0's programme
`wave-02/b-0/scale_ilp.py` (it needs numpy and scipy, and was stopped during 32 points).

**Status.** Tried on 11 October. Closed for the family's own wiring (argued for every size; computed at
4 to 64 points) and for six mixes (computed). Open for every other wiring: the direct search of lead 1.1
has not been made.

### 1.3 An "up" unit at 8 points

**Question.** The 20 turns inputs at scale 1 into H x / 2. Is there a circuit for 2 · H x on 8 points in
27 operations or fewer of count (O)?

**What a yes would give.** Alternating the two gives the exact transform with no multiplications at the
end. With an up unit of u operations the cost is ((20 + u)/48) N log2 N for N a power of 64.
- u = 27: 376 at 64 points, below the textbook's 384. The first size below the textbook would be 64
  instead of 512.
- u = 23 or fewer: below the present count at 4,096 points (45,056).
- u = 20: the rate 5/6 with no "+ N": 40,960 at 4,096 points.

**What has been tried.** [h-3](wave-04/h-3.md): all five 19-operation circuits then on file cost exactly 28
for output scale 2, one too many **[computed; a restricted search, so upper bounds]**. Turning the
circuit around (reversing every line, which is called transposing) gives a down unit again **[argued]**.

**Already on file.** Later reports printed more circuits at 8 points: 26 printings with 19 operations and
125 with 20, in the `.out` files of [x-0](wave-07/x-0.md) and [ab-2](wave-08/ab-2.md), counted by
[ag-6](wave-10/ag-6.md). An AI agent that checked this folder on 11 October reports that the 26 printings
are 12 different circuits, and that all 12 price like h-3's five: 20 for H x / 2 and at most 28 for
2 · H x. I have not kept its scripts and nobody repeated that count.

**Where to start.** Control:
`python3 -B waves/wave-04/h-3-orecord/oprice2.py waves/wave-03/g-1-tightwires/sa8_known0.out`
must print 20 and 28. The search itself has to be written: one that keeps v and 2v apart and asks for
2 · H x. h-3 says the same ("the (O)-native pool nobody has searched").

**How long.** g-1's count-(G) search reaches 19 in 4 seconds. Nothing is known about a count-(O) search.

**Status.** Open. One restricted search, negative.

### 1.4 The least count at 8 points in count (G): is 18 possible?

**What is known.** At most 19. At least 2N − 1, which is 15 at 8 points: a five-line argument by hand in
[j-failproof](wave-02/j-failproof.md) **[argued]**, which later reports quote as known. After the waves a
proof of 2N − 1 was written out for my paper on these circuits; one AI agent read it and found no gap; no
person has checked it.

**What a yes would give.** 18 in layers is (3/4) N log2 N at powers of 8 with no "+ N/4": 3,456 at 512
points (family 3,584). If the 18 also needed only one halving, 19 operations of count (O): 4,160 at 512
points in place of 4,352.

**What has been tried.** Exhaustive, each inside one kind of circuit **[computed]**:
- one merge of the inputs, then a walk of sign flips
  ([WHERE-THE-CIRCUITS-CAME-FROM.md](WHERE-THE-CIRCUITS-CAME-FROM.md), step 2): 19 is the least
  ([g-1](wave-03/g-1.md), [c-0](wave-03/c-0.md));
- every value a list of 0, +1, −1 on one block of a single way of halving the addresses: 19 is the least
  ([v-0](wave-06/v-0.md); the program exhausts a counting game whose rules v-0 derived by hand in the
  same half hour);
- the family's own kind: 20 is the least ([b-0](wave-02/b-0.md));
- values that tie together at most two address bits, entries 0, +1, −1: nothing with 17 or fewer; 18 and 19
  undecided in that kind ([h-5](wave-04/h-5.md)).

Random or local searches, none of which found 18 **[computed; they prove nothing]**: g-1 (every exchange
of two helpers for one around each 19); [h-0](wave-04/h-0.md) (3.0 million neighbours of the 19 and the
20); [h-1](wave-04/h-1.md) (33.9 million steps); [x-0](wave-07/x-0.md) and [x-2](wave-07/x-2.md) (values
with entries up to 3, and values whose sets of non-zero places overlap without one containing the other;
54 runs); [ag-9](wave-10/ag-9.md) (168 runs, 504 million steps, modulo each of eight primes, every
constant allowed, all started near the 19).

**What the halving search of wave 10 excludes.** Very little at 8 points: [ag-1](wave-10/ag-1.md) put one
new halved value into the 19 and took two helpers out, 16,500 cases, none computes the transform. Its own
words: the full class "18 gates, one halving" was not searched. None of the 26 printed circuits with 19
operations contains a halving or a constant 4 ([ag-6](wave-10/ag-6.md)). At 4 points the same question is
settled by exhaustive search in each set of constants tried: 7 with constants 1 and 2, and neither a
halving nor a constant 4 or 8 changes any count (ag-6) **[computed]**.

**A caution.** The 20 and the 19 were both found by searches started from the 22-operation circuit.
Started from nothing, g-1's search found no circuit at all, and the searches of
[j-machine](wave-02/j-machine.md) did not get below 23. Two methods that started from nothing reached 21
([e-2](wave-02/e-2.md), [e2-3](wave-02/e2-3.md)) and no lower. So "no 18 found" may say more about where
the searches started than about 18.

**Where to start.** h-5's exhaustive run for 18 in its own kind: about four hours with that night's
pruning, by its author's estimate. For the search around the 19:
`python3 -B waves/wave-03/g-1-tightwires/sa8.py 6 1 known` (seconds, seed, start) falls from 22 to 20 in
a few seconds and its exchange step prints circuits with 19.

**Status.** Open between 15 (argued; a written proof that no person has read) and 19.

### 1.5 Eight points in count (O): below 20, or the exact transform below 24

**What is known.** Up to one common factor: between 15 and 20. The exact transform: between 15 and 24
([h-3](wave-04/h-3.md)). At 4 points the exact transform costs 8 in count (O), the textbook's number:
[j-failproof](wave-02/j-failproof.md) searched every program of 7 additions and subtractions
**[computed]**; that a program with a multiplication cannot do it in 7 rests on the bound of 7 in count
(G), which is argued (lead 1.4).

**The sharpest form.** With additions and subtractions only, is 24 the least at 8 points? h-3 argues that
a circuit of 19 plain additions and subtractions, if one existed, would give H x exactly.

**What a yes would give.** An exact 8-point circuit with c operations costs (c/24) N log2 N with no "+ N".
c = 23 would put the exact transform below the textbook at 8 points and at 64 (368 against 384). A "no"
would show that at 8 points every saving needs a value held at two scales.

**What has been tried.** Nothing exhaustive. Inside the one-merge-and-walk design the count-(O) least is
20 **[argued from the computed 19]**.

**Where to start.** h-3's suggestion: g-1's search with only the lines u + v and u − v, on a pool of
whole-number lists with entries 0, ±1, ±2. It cannot be run as it stands. g-1's pool has 304 values
(`wave-03/g-1-tightwires/pool.py`), and its programs treat v and 2v as one value and accept an output up
to a factor (`ref.py`); they have to be rewritten to keep scales apart and to ask for H x itself. The
pool h-3 means is not written down; all lists with entries 0, ±1, ±2 would be 390,625 at 8 points, too
many for that search. The control for a new program is the 4-point case:
`python3 -B min4.py O 7 pm1` in `wave-02/j-failproof/` (its saved output is `o7.out`).

**Status.** Open.

### 1.6 Sixteen points in count (G) below 52

**What is known.** At most 52, by two circuits of different shapes (the family's and h-1's). For circuits
whose values are lists of 0, +1, −1 on blocks of one way of halving, at least 47
([u-8](wave-06/u-8.md), [u-9](wave-06/u-9.md), read by [v-0](wave-06/v-0.md)) **[argued]**; whether 47 to
51 can be reached there was not decided.

**What a yes would give.** 51 would be the smallest count on file at 16 points. 48 or fewer would beat the
family at every power of 16 by layers alone (48: 786,432 at 65,536 points against 802,816).

**What has been tried** **[computed; local or random]**: remove any 2 of the 36 helpers of the 52 and add
any one, 892,124 cases ([e2-0](wave-02/e2-0.md)); 84 million steps of random search started from the 52,
and 5.6 million started from the 54 of the layered 19, which fell to the second 52; no 51
([h-1](wave-04/h-1.md)); 164 circuits around the 52
([x-0](wave-07/x-0.md), which says of itself that it "says nothing"); the one-merge-and-walk design, best
63 ([g-1](wave-03/g-1.md)); one "letter" (part 3, door 7), best 59 ([r-1](wave-05/r-1.md)).

**Where to start.** The tenth note's experiment 7: start from a least circuit for subset sums and ask how
many operations must be added to make it a class identity; the differences known are 3 and 7 at 4 and 8
points, and 15 at 16 points would be 47. No program for it is on file.

**Status.** Open between 47 (in one kind of circuit) and 52.

### 1.7 Thirty-two points, and the sizes between powers of 8

- Count (O), common factor: 144 at 32 points, from one layer of the 20 and two textbook layers
  ([h-3](wave-04/h-3.md)) **[computed]**. Fewer than 144 improves every size whose k leaves remainder 2.
- Count (G): 128 at 32 points (the family). [h-1](wave-04/h-1.md) searched the family's "half problem" at
  16 points, the smaller problem whose solution gives the 32-point circuit: 44, and 43 would give 126 at
  32 points; no 43 in 55 million steps **[computed; random]**.
- The general count for the exact transform in count (O) is N (k − m/2 + 1) for k = 3m + r
  ([n-0](wave-04/n-0.md)) **[computed to 4,096 points]**.

**Status.** Open, and small: the gain is a fraction of N.

### 1.8 Lean statements that are not written

Proved in Lean on the night of 10 to 11 October 2026, and built again from nothing on 11 October: the
count 20 j 8^(j−1) + 8^j for the exact
transform on 8^j points in OpenAI's circuit model. Not stated in Lean: sizes that are not powers of 8;
anything in count (G) (OpenAI's model has no operation a·u + b·v, so a second kind of gate would have to
be defined); the family (it is not a layering of a smaller circuit, so the proof must follow the
recursion of the program that generates it); the count (7/8) N log2 N + N/4 for H x / √N. See
[notes/explicit-circuits.md](../notes/explicit-circuits.md), section 6.

**Status.** Not started. Nothing in the waves bears on it. It needs no search; its effort is unknown.

### 1.9 Timing

Fewer operations are not the same as less time, and that is now measured. On 11 October 2026, after the
waves, the 8-point step was written into the generated code of FFHT, a tuned open-source library for this
transform, in place of its block of 24 additions and subtractions, with nothing else changed. On the one
machine that was timed it did not make FFHT faster at any size from 2^6 to 2^26 points in single precision
or from 2^5 to 2^26 points in double precision: set against a second build of FFHT's unchanged code, all
129 combinations of size and form took more time. From 2^7 points (2^6 in double precision) to 2^19 points
it took 11 to 24 % more time with 20 operations and exact output, 4 to 12 % more with the output left
divided by a power of two (which is not FFHT's output), and 1 to 11 % more with the 19 operations of count
(G), each written as one fused multiply-add (one instruction for "a plus twice b"). From 2^20 to 2^26
points it took 6 to 7 %, 3 to 5 % and 2 to 3 % more on average, and for the last form that is too small
for one run to establish. This is a measurement by AI agents on one rented machine with one compiler,
with other jobs running, not repeated by anyone. The tables, the conditions and the programs are in
[tools/circuits/fast/wht56/results/ffht/](../tools/circuits/fast/wht56/results/ffht/README.md).

The rough timings of my own plain C in [tools/circuits/fast/wht56/](../tools/circuits/fast/wht56/) are not
a gain of the step either. On the same machine, with the compiler's vector instructions, the new step took
less time than the textbook step only in double precision at the sizes 2^6, 2^9, 2^12 and so on (7 to
37 % less), and more at every other size and at every size in single precision; that gain is larger than
replacing 24 operations by 20 can give, so it comes from how the compiler treated one pass. The 1994 paper
met the same gap between counting and timing: its count predicts a gain of 12.5 %, and its authors measured
5.6 % to 7.4 % on their machine.

**What is still open.**

- **A version of the step with a shorter chain.** The likely reason for the lost time is the order in
  which the operations wait for one another. In the textbook block no result is more than 3 operations
  away from the loaded numbers. In the 19 and the 20 the last results are 7 operations away, 6 when each
  line is one fused multiply-add. In a test of one pass alone, a block of 20 operations with a chain of 3
  took 15 to 16 % less time than FFHT's block, and the real block with its chain of 7 took 23 to 24 %
  more. What happens inside the processor was not measured, so this is an explanation that fits, not a
  finding. Nobody has searched for a circuit with fewer than 24 operations and a chain shorter than 7.
  The searches of the waves counted operations, not depth. That search is the lead this measurement
  leaves, and it is a question about circuits, like leads 1.4 and 1.5.
- **Another processor.** One machine was timed, and its core handles additions and multiply-adds alike.
  Nothing was timed on a processor where they run on different units, on an ARM processor, or with wider
  vector registers, so nothing can be said about them.
- **The larger circuits.** Only the 8-point member was timed (19 for 24). The 16-point circuit of the
  family has 16 inputs, and the machine has 16 vector registers, so it cannot be done in registers alone
  as the 8-point step can.
- **A second run**, on a quiet machine, with every repeat printed, and a second compiler.
- **Depth in hardware.** As hardware the same depth costs clock speed and registers
  ([tools/circuits/fpga/](../tools/circuits/fpga/README.md)): on the one programmable chip for which it was
  placed and routed, the 19 takes fewer logic cells (the units such a chip is made of) than the textbook
  network only as a block with no registers inside, and at a lower clock by the tools' estimates. A search
  that minimises adder levels, or real cells, has not been made.

**Status.** Measured on one machine: no gain in time. Open: a step with a shorter chain, and another
processor.

### 1.10 The Fourier transform

Alman and Rao get their count for the Fourier transform from their count for the Walsh-Hadamard
transform. Their Lemma 1.1 says: if the Walsh-Hadamard transform can be computed in c N log N + O(N)
operations, the Fourier transform can be computed in (2c/3 + 28/9) N log N + O(N) real operations
**[read]**. With c = 1 that is their 34/9 and with their c = 23/24 it is their 15/4. **Nobody has put 5/6
into that lemma and checked the result.** To do so one has to read the lemma's proof, its lower-order
terms, and whether it needs the count at sizes that are not powers of 8, which is computed to 4,096
points and is not in Lean. So this is a lead, not a count. Separately, [e2-0](wave-02/e2-0.md) proposes
the family's hub with a root of unity (a complex number some power of which is 1) in place of the sign.
Nothing was tried.

### 1.11 The same wiring for every 2 by 2 block: a statement to prove

The 19 and the family work for every 2 by 2 block with four non-zero entries that was tried: 300 random
blocks for the 19 ([c-0](wave-03/c-0.md)), a census of every record with τ left general
([ag-8](wave-10/ag-8.md)) **[computed; not proved]**. A proof would give the rates 19/24 and 3/4 in count
(G) for that whole class of tables. It does not cover blocks with a zero, such as subset sums, where the
textbook needs only half as much.

### 1.12 Does a cheaper small circuit change the exponent of my other result?

Probably not. [h-3](wave-04/h-3.md) argues that the exponent of OpenAI's result is a formula in three
fixed numbers in which the cost of a small transform does not appear, and that a cheaper small circuit
changes only a constant **[read in OpenAI's file; argued; h-3 did not open my own formula]**.
[b-0](wave-02/b-0.md) had left the question open. Nobody checked it against the Lean files.

---

## Part 2. Leads for a change of order

Fifteen leads. The first seven come from the tenth note's list of what is alive (its item F is 2.13
here). The next five are older leads that no later wave closed. The last three are inside the mechanism
of my other, published result and concern the size of its saving. **None has a positive example.** After
ten waves the state is: nothing found gives fewer than a constant times N log N operations by a new
route, and nothing found forbids it.

Where a lead has a next experiment that a note or a report proposed, it is given. Where none was
proposed, the lead says so; I did not invent one.

### 2.1 Coupling two half-size subset sums

**In plain words.** The transform is two passes of subset sums around one layer of N multiplications, so
subset sums in a constant times N operations would give the transform in a constant times N
([g-4](wave-03/g-4.md), wave 3) **[argued; the identity computed for k up to 10]**. Subset sums on 2n
points are two half-size subset sums plus n additions that couple them. Yates pays 1/2 operation per point
at every doubling. Linear size needs that price to add up to a finite number over all doublings
([ah-cross](wave-10/ah-cross.md)) **[argued]**.

**Evidence against.** The least counts found are 0, 1, 4, 12 at 1 to 8 points: 1/2 at each of the three
doublings. At 8 points 11 is excluded by exhaustive search in arithmetic modulo 2, 3, 5 and 7
([d-0](wave-01/d-0.md)) **[computed modulo p]**. At 16 points:
- a random search over one shape of circuit found 32 in 28 runs of 28 and never 31
  ([u-3](wave-06/u-3.md));
- two local searches for 31, modulo 2 and modulo 3, one of 106.8 million steps, found none
  ([h-4](wave-04/h-4.md)); h-4 says they give "no information about 'no 31'", because its tool, started
  from nothing, does not even find the 32 of Yates;
- cut the data in a lower and an upper half along one address bit; over all 1,208 circuits for the
  upper half, three exhaustive searches, each inside one named class of circuits that cross the cut,
  found no 31 ([ag-2](wave-10/ag-2.md)) **[computed modulo 2]**. ag-2's own words: the question "is NOT
  decided".

**Evidence for.** None. What exists is the absence of an argument: over the rationals with free constants
no report bounds this price.

**The first open value.** 16 points: 32 or 31.

**Next experiments** (the tenth note's 4 and 5). (a) Subset sums at 16 points with every constant allowed,
modulo several primes: is 31 possible? (b) Two independent copies of subset sums on 4 and on 8 points: is
anything below twice one copy?

**Already on file, and what cannot be started.**
- (b) at 4 points is done: two copies need 8 operations and not 7, modulo 2, 3, 5 and 7 **[checked
  11 October, with d-0's program `mincirc`, on a file of the 8 rows of two copies]**. At 8 points (16
  inputs) it is beyond that program.
- (a) cannot be run with the exhaustive program: `wave-01/d-0-zeta/mincirc.c` needs p^n to be at most
  about 6 million, so at 16 points only p = 2 fits, and 31 operations there are out of its reach
  (d-0, h-4). The local tool fails its own control, as said above.
- h-4 proposes a cheaper step that nobody ran, `basis16`: fix one address bit and turn the 16-point
  question into many 8-point searches ([h-4](wave-04/h-4.md), section 9).
- Controls that do work: `cc -O2 -o mincirc mincirc.c`, then `./mincirc 2 8 4 rows_zeta3.txt` must say
  NO for 11 operations and `./mincirc 2 8 5 rows_zeta3.txt` YES for 12, in under a second.

**How long.** d-0's exhaustive program took 52 seconds modulo 5 and 6 minutes modulo 7 for subset sums at
8 points. Nothing is known for 16.

**One thing the last wave overlooked.** It lists "two copies of the 4-point transform: is 13 possible?" as
never tried. [j-manyatonce](wave-02/j-manyatonce.md) ran that search to the end modulo 3 (none; 117
seconds) and left it unfinished modulo 5, with its command in the report, and [d-6](wave-01/d-6.md) has a
hand argument for 14.

### 2.2 Subset sums with constants +1 and −1 only

**In plain words.** A count of volume (how fast a determinant can grow) asks at least
0.277 N √(log2 N) − N operations of a circuit for subset sums that only adds and subtracts; Yates spends
(N/2) log2 N ([ai-2](wave-10/ai-2.md)) **[argued from known lemmas; small cases computed]**. A circuit at
the lower figure would give the transform in about N √(log N) operations.

**Evidence.** Every count measured sits at Yates' figure. That the truth could be lower is **[guessed]**,
with no evidence. The lower figure passes the trivial N − 1 only beyond about 2^52 points, so no search can
see the gap. No argument closes it.

**A related loose end.** A polynomial of degree about 5 √k in the number of common 1-bits equals the
transform on 99 % of its entries (degree 71 for k = 1,024) **[computed]**. What is left over is a table
with no linear dependence among its rows, and nobody has counted what it costs
([ah-cross](wave-10/ah-cross.md), hybrid 4).

**Next experiment** (the tenth note's 5). The least number of ±1 operations for subset sums at 16 points.

### 2.3 Relations among mixed wires

**In plain words.** Cut the data of a circuit for subset sums in a lower and an upper half along one
address bit. A wire is *mixed* when it reads the upper half. A *relation* is a combination of wires that
is always zero. A set of r mixed wires whose upper parts cancel hands the lower half a sum of L terms for
r − 1 operations, a gain of L − r ([ag-2](wave-10/ag-2.md)) **[argued]**. A change of order needs L/r to
grow without bound.

**Evidence.** On all 20,880 cuts of least circuits at 8 points, every operation gained is paid back by
exactly one. At 16 points L/r is at most 2, on paper, for relations of two and of three wires. In all
13,447,158 cases reached, the sum handed over has exactly one term, and nobody knows why **[computed
modulo 2]**. Not searched: relations of four wires; two or more extra operations across the cut.

**Next experiment** (the tenth note's 1). The largest L/r at 32 points.

**What it needs that is not here.** ag-2's programs (`decoA.c`, `decoB.c`, `decoC.c` in
`wave-10/ag-2-firstbusthatpays/`) are fixed to 8 points in the upper half (`#define n 8`); the report
says they "run after changing the constants" and does not say which. Their input `z8_sets.txt`, the list
of all 2,802 least circuits at 8 points, is left out for size; [WHERE.md](WHERE.md) gives the command
that makes it again in 9 seconds. For 32 points the upper half must be Yates' circuit on 16 points
written in the same form, and no file holds it. The report says of its own programs that they have "no
positive control".

### 2.4 Two operations per output at a growing degree

**In plain words.** The j-th binary digit of the transform at an output is a polynomial of degree j in that
output's address bits ([ae-cross](wave-09/ae-cross.md)) **[computed for k = 2 to 6]**. So one can ask what
it costs to compute, from its coefficients, a polynomial of degree at most d at all N addresses. Degrees
1, 2 and 3 cost N + o(N) ([ad-6](wave-09/ad-6.md) and [af-0](wave-09/af-0.md) for degree 2;
[ag-0](wave-10/ag-0.md) and [ai-0](wave-10/ai-0.md) for degree 3, where the saving starts at addresses of
2,060 bits) **[computed and argued]**. The construction fails at degree 4. From degree about log2 k on,
any circuit costs at least about 1.67 N, and the floor rises towards 2 N as the degree grows
([ag-7](wave-10/ag-7.md), [ai-1](wave-10/ai-1.md)) **[argued; in arithmetic modulo 2; over the rationals
a weaker form, unreviewed]**. That floor comes from one lemma that four reports found independently
(wall L23): outputs with no short relation among them cannot share helpers. Its ceiling is 2N, so it can
never say more than "linear".

**The open question.** Nothing forbids 2N + o(N) operations at a degree that grows, and nothing builds it.
Tables with long relations and linear cost are known to exist **[read second hand by ai-1]**, which
speaks for the lead. [ag-5](wave-10/ag-5.md) built families with three helpers per output and one kind of
helper fewer than two helpers allow (29, 61, 125 kinds at 32, 64, 128 points) **[computed; these count
kinds of helper, which the report calls classes, not operations]**.

**Next experiment** (the tenth note's 2). The largest degree reached with three helpers per output and
o(N) kinds of helper: is it bounded? The tenth note warns that a search cannot see this below 1,024
points.

**Why even a yes would not be enough.** These are the low digits. The transform has k digits and 96 to
98 % of its coefficients sit in the middle ones **[computed, wave 9]**.

### 2.5 A shared deep operation in a class identity

**In plain words.** In a class identity every operation has a *weight*, its degree in τ, and the weights
add up to at least (N/2) log2 N ([ah-cross](wave-10/ah-cross.md), re-derived by
[ai-2](wave-10/ai-2.md)) **[argued; checked on circuits at 4 and 8 points]**. The textbook meets this
exactly. Every record of the night is a class identity. So linear size inside the class needs operations
of weight about log2 N that many outputs read.

**Evidence.** [ag-6](wave-10/ag-6.md) argues against it only for an operation that ends in an output. At 4
points a circuit with one operation of weight 2 has fewer heavy operations and not fewer operations
**[computed]**. A caution from the critic: the weight depends on which letter one calls τ; with another
letter the same count asks for nothing.

**Next experiments** (the tenth note's 3, 6 and 8; the first two are the cheapest of its eight). (3) Carry
τ as a letter through every record: which operations vanish at τ = −1 and at τ = 0, and does any family
lose a fixed share of its operations there? (6) At 4 points with τ a letter: the least count when every
operation's weight is at most 1, 2, 3, and with one shared operation of weight 2. (8) Put a cyclic shift
in place of τ, so that one circuit computes every block at once with constants ±1, and ask whether
counting then shows that no class identity is linear. No program for any of the three is on file.

**A standing anomaly from wave 7.** Circuits whose values are all lists of 0, +1, −1 cost at least
N − 1 + 0.315 N log2 N, and my published program is below that for large N. So at some size there is a
first value with larger entries that pays. Nothing says where **[argued; it rests on that program's
constants being rational, which nobody checked]**.

### 2.6 Constants whose degree grows with N

A constant that is a root of a polynomial of degree d is worth at most d² operations with rational
constants, so constants of bounded degree leave the order unchanged ([ag-9](wave-10/ag-9.md)) **[argued;
run on one circuit; no critic]**. What is left is a degree that grows at least like √(log2 N). OpenAI's
other model, a random-access machine, does allow that **[read by ag-9 in the Lean files]**. No
construction uses it, and no report proposes a first experiment.

### 2.7 Anomalies that were kept

- One operation above the least at 4 points, the transform has fewer different circuits than its class:
  464 against about 1,364 ([ag-8](wave-10/ag-8.md)) **[computed modulo 13 and 17]**.
- The first circuit argued to work for the transform and for no other block has 64 operations at 16
  points, the textbook count; its machine test was 65 % complete (ag-8) **[argued]**.
- The one saving found that only the transform has is on data that depend only on how many address bits
  are 1: 4 operations against 5 at k = 2, 7 against 8 at k = 3 ([p-0](wave-05/p-0.md),
  [r-2](wave-05/r-2.md)) **[computed; the 8 modulo primes]**. k = 4 is undecided, and I found no later report
  that took it up. It can never be worth more than about (log2 N)² operations **[argued, r-2]**.
- A case where a constant 4 does pay, though not for the transform: the 4 by 4 table with rows
  (1, 1, 1, 1), (1, −3, 1, −3), (1, 1, −3, −3), (1, −3, −3, 9) costs 7 operations with a line u ± 4v and
  has no 7-operation circuit without one ([ag-6](wave-10/ag-6.md)) **[computed, exhaustive]**.
- An unfinished search: on one 8 by 8 part of the neighbour-sum table at 16 points (lead 2.9),
  "15 operations and one division by 4" was excluded for 2,538 of 8,695 candidates and the other 6,157
  were not run; two or more halvings were not searched ([ag-1](wave-10/ag-1.md)) **[computed]**.

### 2.8 All line sums of a finite plane (older lead, not closed)

**In plain words.** Cut the address in two halves and read it as a point of a plane with √N points on
each line. There are N + √N lines. If the sums of the data over all lines cost a constant times N, the
transform costs about N log log N ([d-1](wave-01/d-1.md); the identity computed at 4 to 4,096 points by
[af-1](wave-09/af-1.md)) **[argued; computed]**.

**Evidence.** The least found is 60, 475 and 2,484 operations at 16, 64 and 256 points (the last two not
built end to end), which is 3.75, 7.42 and 9.70 per point: no construction grows more slowly than log N
per point ([ad-1](wave-09/ad-1.md)) **[computed at 16 points; composed or counted above]**. The reverse
relation holds too, so the line sums and the transform have the same exponent of log N **[argued twice]**.
The critic's verdict: this is the same open question in other coordinates, as open as the transform, with
nothing for it and nothing against. No report proposes a next experiment.

**For a better constant.** Fewer than 133 operations at 64 points, or 716 at 256, would beat the family.
The best found, 475, is far from that.

### 2.9 Neighbour sums at 32 points and beyond (older lead, not closed)

**In plain words.** Every address gets the sum of the data at its k neighbours, the addresses one bit away.
A transform of linear size would give neighbour sums of linear size, so this is a necessary test
([w-cross](wave-07/w-cross.md), [z-2](wave-07/z-2.md)) **[argued]**.

**Evidence.** 32, 96, 224 operations at 16, 32, 64 points, all by one circuit that only adds, about
(3/4) k − 1 per point ([ab-0](wave-08/ab-0.md), [ac-0](wave-08/ac-0.md)) **[computed]**. Subtraction saves
one operation, in arithmetic modulo 2 only, and that saving is gone modulo 4 in all 478 wirings
([ad-7](wave-09/ad-7.md)) **[computed, exhaustive]**. Above 16 points there is no evidence at all: the
exhaustive tool stops there and the random search failed its own control. The one defined job left is
the unfinished search of lead 2.7.

### 2.10 A half-size call plus a quarter-size call (older lead, never revisited)

Shape: H = S + A·C·B, where S, A and B are sparse (few non-zero entries in each row) and C is one
half-size and one quarter-size transform. That recursion would be linear. The obstruction that
[e-7](wave-02/e-7.md) found for one half-size call asks only 0.75 entries per row of A here **[argued;
re-run by the critic to 4,096 points]**. The critic [b-2](wave-02/b-2.md): this is only the place where
one argument stops; it is not evidence, and the only A it could build has rows that grow like N^(1/4). No
later wave returned to it, and no report proposes a next experiment.

### 2.11 Limits of cheap programs (older lead, never revisited)

A program that depends on a small number ε and is right only in the limit ε → 0 can be cheaper than any
exact program: 7 against 8 operations on 4 values, 2n − 1 against 3n − 4 on n values
([d-5](wave-01/d-5.md)) **[computed; the report gives the data that prove each case]**. Making it exact
multiplies its size by (d + 1)², d the order of the limit **[argued; standard]**. So a change of order
needs d to grow with N and a cheaper conversion. The 4-point circuit has no such gap **[argued]**. No
report proposes a next experiment.

### 2.12 Three steps, and trees that are not made of subspaces (older lead)

A bounded number of "tree steps" (tables that cost about 4N operations each) would be linear size. Two
steps whose pattern repeats along the addresses make the transform at 16 points and cannot from 32
points on ([g-6](wave-03/g-6.md), [c-2](wave-03/c-2.md), [p-3](wave-05/p-3.md)) **[argued]** (walls L7).
Sweeps of weighted sums along a chain of nested sets of addresses, which the reports call flag passes,
need at least about k / log2 k of them ([x-4](wave-07/x-4.md), [z-2](wave-07/z-2.md)) **[argued]** (wall
L17). Not covered by either: three repeating steps, and trees that are not made of such nested sets.

### 2.13 to 2.15 Inside the mechanism of my other result

My other repository, [wht-power-saving-lean](https://github.com/jacobalansussman/wht-power-saving-lean),
has the transform in O(N (log N)^z) operations with z = 1 − 8.762479e-4, a saving of about 8.7625e-4,
checked by Lean. The reports call its mechanism *the engine* and its small repeated program *the unit*.
The unit works on a batch of *arrays*, working copies of the data. A *move* is one direction of the
transform applied to one whole array; a move the unit can skip is *free*, the others are *paid*. A
*shear* adds a multiple of one array to another. A *stage* is one round of the engine's recursion and
its *width* the number of address bits it handles. These three leads concern the size of that saving.
The reports argue that none reaches 1e-1 and that this mechanism cannot give linear size.

- **2.13 Two paid moves and two shears.** Giving n arrays one free move each needs n + 1 shears, for
  every free step of a named kind ([ad-0](wave-09/ad-0.md), [ag-3](wave-10/ag-3.md)) **[argued; exact
  cases computed]**. For a relabelling of the addresses that moves the *port* (the set of directions
  along which the transform splits off), all that the argument still gives is whether a certain count is
  even or odd, so an exchange with two shears is neither excluded nor built. Its author: even a yes is
  not 1e-1.
- **2.14 Two hatches in the cost model.** The exclusion of 1e-1 up to stage width 9 holds in one cost
  model ([ab-8](wave-08/ab-8.md), [ac-2](wave-08/ac-2.md)) **[computed twice]**. The critic names what would
  break it: shared sums that cost much less than assumed, or removing a term that is only partly known.
  The second was not tested.
- **2.15 Helpers and scratch copies.** Of the moves the unit saves, 75 % pay for its scratch copies
  (extra arrays that hold a copy of the data) and 18 % for its helper arrays. With both removed entirely
  the saving would be 1.3e-2 ([ad-0](wave-09/ad-0.md)) **[computed; the 1.3e-2 is arithmetic on a
  program nobody has]**.

---

## Part 3. Closed doors

Each line: what was excluded, in which kind of circuit, up to which size, and how. "Lk" is the number the
notes give the wall. **Every wall fences one kind of program. None bounds a general circuit in count (G)
or (O).**

### The walls by number

The notes number the walls L1 to L24, and no single note states them all. This table says where each is.
The notes of waves 1 and 2 state walls without numbers.

| wall | name in the notes | in short | stated in full in | on this page |
|---|---|---|---|---|
| L1 | half and half; later "costs add" | a change of coordinates that makes the transform cheap costs half a transform going in and half coming out | [note 3](wave-03/NOTE.md), section 5 | door 10 |
| L2 | copies do not share | transforms on separate data cost the sum of their costs | [note 3](wave-03/NOTE.md); [note 6](wave-06/NOTE.md) | door 11 |
| L1 + L2 | repay | a value that serves two uses pays back what the sharing saved | [note 8](wave-08/NOTE.md) to [note 10](wave-10/NOTE.md) | door 12 |
| L3 | tight wires | | [note 3](wave-03/NOTE.md) | door 1 |
| L4 | volume; later height, depth, levels | values with small entries make a determinant grow slowly | [note 3](wave-03/NOTE.md); exact form in [note 7](wave-07/NOTE.md); [note 10](wave-10/NOTE.md) | door 3 |
| L5 | one class | every saving found also works for the other 2 by 2 blocks without a zero | [note 3](wave-03/NOTE.md); [note 10](wave-10/NOTE.md) | door 19, lead 1.11 |
| L6 | the extra value | an observation, not a wall: every saving holds a value beyond the N that a transform must hold (1 and 5 of them at 4 and 8 points) | [note 3](wave-03/NOTE.md), [note 4](wave-04/NOTE.md) | not on this page |
| L7 | two periodic steps stop | | [note 3](wave-03/NOTE.md), [note 5](wave-05/NOTE.md) | lead 2.12 |
| L8 | one sum of rectangles needs perpendicular trees | unreviewed; replaced by L13 | [note 3](wave-03/NOTE.md) | door 7 |
| L9 | pay once | | [note 4](wave-04/NOTE.md) | door 5 |
| L10 | width | | [note 4](wave-04/NOTE.md) | door 2 |
| L11 | no tensor product sits on the count N − 1 + (N/2) log2 N | taken into L14 | [note 4](wave-04/NOTE.md) | door 4 |
| L12 | old letters | the engine without relabellings of addresses: counting, plus two lemmas | [note 4](wave-04/NOTE.md), section 2 | door 23 |
| L13 | one form per node | the "letter" | [note 5](wave-05/NOTE.md) | door 7 |
| L14 | one tree of sign vectors | takes in L3, L9 and L11 | [note 6](wave-06/NOTE.md) | door 4 |
| L15 | one line through the cube | | [note 6](wave-06/NOTE.md), section 2 | door 13 |
| L16 | distance; later "bent", "step" | two rows of the transform differ on exactly N/2 points, so a step that reads one *flat* (a set of addresses closed under adding bit by bit, or a shifted copy of one) moves the target by one unit | [note 7](wave-07/NOTE.md), [note 9](wave-09/NOTE.md) | no door of its own; the reports behind doors 9 and 15 use it |
| L17 | flag passes | | [note 7](wave-07/NOTE.md) | lead 2.12 |
| L18 | two-piece hubs | | [note 7](wave-07/NOTE.md) | door 6 |
| L19 | three blocks per exchange; later "ports" | about the engine; its first form was withdrawn | [note 7](wave-07/NOTE.md), restated in [note 8](wave-08/NOTE.md) | door 24; "Where reports disagree", item 1 |
| L20 | layers | | [note 8](wave-08/NOTE.md) | door 9 |
| L21 | sharing in adding-only circuits | neighbour sums by additions only cost exactly N (k − 1 − floor(k/2)/2); subset sums by additions only cost (N/2) log2 N (read from summaries of Find and Boyar, 2013) | [note 8](wave-08/NOTE.md), [note 9](wave-09/NOTE.md) | lead 2.9 |
| L22 | two helpers | two kinds of helper per output carry degree about log2 k and no more | [note 9](wave-09/NOTE.md) | lead 2.4 |
| L23 | relation length | contains L22 | [note 10](wave-10/NOTE.md) | lead 2.4 |
| L24 | restriction of scalars | a constant of degree d is worth at most d² operations with rational constants | [note 10](wave-10/NOTE.md) | lead 2.6, door 17 |

### Kinds of circuit that cannot beat a constant times N log N

1. **Tight wires only** (L3). A wire is *tight* when (its non-zeros written in the inputs) × (its
   non-zeros written in the outputs) = N, the least possible. Every value the textbook holds is tight. A
   program of tight wires needs N log2 N operations, at every N. **[argued, ten lines]**
   [a-2](wave-01/a-2.md), refereed by [g-1](wave-03/g-1.md). I do not call this wall new: a-2 named a
   paper of 1979 (Papadimitriou) as the one to compare it with and could not open it.
2. **Wires that tie together at most b address bits** (L10): at least N log2 N / b.
   **[argued; no violation on 8.6 million test gates]** [h-5](wave-04/h-5.md), [n-1](wave-04/n-1.md).
3. **Wires with entries 0, +1, −1** (L4): at least 0.3155 N log2 N operations besides halvings; with whole
   numbers of size at most M the constant falls only like 1 / log M. The argument is the determinant
   argument that later papers attribute to Morgenstern (1973). It is taken here as Alman and Rao quote
   it, for Fourier programs whose constants have size at most 1; nobody here opened that paper ([README.md](README.md#earlier-papers)). The constant 0.3155 is the
   agents' own. **[argued; re-derived by three critics]** [z-0](wave-07/z-0.md),
   [ai-2](wave-10/ai-2.md). It holds for rational constants, and it says nothing once constants are
   free.
4. **Sign vectors on the blocks of one way of halving** (L14): every value a list of 0, +1, −1 whose
   non-zero places form one block. At least N − 1 + (N/2) log2 N, which is 2, 7, 19, 47, 111, 255. Every
   record of the night is of this kind, by one agent's reading of 31 circuits, so more searching inside
   it can only move a constant. **[argued by two agents; 7 and 19 by exhaustive search, the 19 through a
   counting game whose rules were derived by hand]** [u-8](wave-06/u-8.md), [u-9](wave-06/u-9.md),
   [v-0](wave-06/v-0.md). The critic shows the floor for a slightly larger kind, in which the direction
   of halving may differ from branch to branch.
5. **No operation reads two wires that are not tight** (L9): at least (2/3) N log2 N.
   **[argued; one case closed only at 8 points]** [h-8](wave-04/h-8.md), [n-1](wave-04/n-1.md).
6. **Pieces and two-piece hubs on one way of halving** (L18; a *piece* is one output restricted to a
   block of inputs, a *hub* is made of two pieces): at least (3/4) N log2 N + N/4, for every value of the
   hub's constant; any constant other than ±1 costs N/2 more per level (rate 5/4).
   **[argued; 20 exhaustive at 8 points; the 5/4 computed to 64 points]** [h-1](wave-04/h-1.md),
   [b-0](wave-02/b-0.md), [x-9](wave-07/x-9.md), [z-2](wave-07/z-2.md). The 19 is outside this kind.
7. **One "letter"** (L13): a shape of circuit in which every output is one earlier output plus sums taken
   from one fixed way of merging the inputs, a *merge tree*. On the standard trees (rows grouped by their
   high address bits, columns by their low bits) it needs a number of pieces that grows like N², and at
   least 138 operations at 32 points against the 128 known. **[argued; small cases computed]**
   [p-1](wave-05/p-1.md), [p-8](wave-05/p-8.md), [r-1](wave-05/r-1.md). Other trees: one run at 8 points
   modulo 3, and a guess.
8. **Two steps** (L7, L17): see lead 2.12 above.
9. **The same operation at every address** (L20): a program whose stages do the same thing at every
   address needs at least k/2 stages of N/2 operations or more. **[argued]** [ab-0](wave-08/ab-0.md),
   [ab-3](wave-08/ab-3.md), [ag-9](wave-10/ag-9.md).

### Routes that cost what they save

10. **Change of basis, something free, change back** (L1). The cheapest coordinates in which the
    transform becomes free cost half a transform to within N operations, going in and again coming out.
    **[argued; computed to 256 points]** [w-cross](wave-07/w-cross.md), [z-2](wave-07/z-2.md). The
    "mirror" of wave 1 is one case: its cheapest reading at 16 points costs exactly 24 and the route at
    least 56 ([g-0](wave-03/g-0.md)) **[computed; the lower side argued]**.
11. **Copies that share** (L2). A program that only calls a K by K table as a sealed box, and is right
    for every such table, makes at least 2K calls; for the one family where room was left, at least
    2K − 2 (7 calls at K = 4). **[argued twice]** [v-2](wave-06/v-2.md), [ab-6](wave-08/ab-6.md),
    [ac-1](wave-08/ac-1.md). Two copies of the 4-point transform: none with 13 operations, complete
    search modulo 3 ([j-manyatonce](wave-02/j-manyatonce.md)).
12. **Sharing is repaid one for one** (L1 + L2 as "repay"). Wherever one wire or one call served two
    uses, removing the part that the other use does not want cost what the sharing saved. The tenth note
    lists 45 reports that measured it. It is argued in five kinds of circuit and **not argued in
    general**: it is the wall that lead 2.1 would have to break.
13. **Subset sums by running sums in two orders** (L15; a running sum is the sum of everything up to a
    point): at least about N^1.32 / log N operations, more than Yates from about 2^51 points on.
    **[argued four times; read line by line by a critic]** [u-1](wave-06/u-1.md), [u-2](wave-06/u-2.md),
    [v-1](wave-06/v-1.md).
14. **The transform as subset sums, scalings, subset sums**: exactly N log2 N with Yates in both passes,
    and 14, 38, 88, 220 with running sums, against 8, 24, 64, 160. **[computed]** [u-4](wave-06/u-4.md).
15. **Large or growing constants.** Wires that are nearly multiples of each other bring back at most one
    unit of volume per operation, however large the constants ([x-8](wave-07/x-8.md)); a wire with larger
    entries pays only when the target has entries of different sizes, and the transform has not
    ([ab-2](wave-08/ab-2.md), [ab-7](wave-08/ab-7.md)). **[computed on small cases; argued]**
16. **Halvings and constants 4 and 8 at 4 points**: no profit for the transform, exhaustive in each set
    of constants tried ([ag-6](wave-10/ag-6.md)) **[computed]**. At 8 points only local searches (lead
    1.4). For another table a constant 4 does pay (lead 2.7).
17. **Constants that are not rational, of bounded degree** (L24): lead 2.6. At 4 points no circuit with 6
    operations modulo 17 or 41 **[computed modulo p]**.
18. **The digits of the transform, one at a time.** Circuits equal to the transform up to multiples of 4,
    8, 16 take 757, 1,223, 1,605 operations at 256 points; each low digit costs about 2N and all digits
    together exactly N log2 N ([x-1](wave-07/x-1.md)) **[computed, replayed]**. The cheap constructions
    for degrees 2 and 3 (lead 2.4) start to pay only at sizes nobody can build.
19. **Anything special to this transform.** Every record works for the whole class (lead 1.11). At 4
    points [r-2](wave-05/r-2.md) found 27 different 7-operation circuits, each right for every τ
    **[computed, exact]**, and a 28th only at τ = 2, 1/2 and two other values, never at the transform.
    That there is no 29th is computed modulo five primes only.

### Other small exact results

20. Four points: 7 operations in count (G) and not 6 (three hand arguments; exhaustive modulo primes).
    In count (O) the exact transform costs 8: no program of 7 additions and subtractions does it
    ([j-failproof](wave-02/j-failproof.md)) **[computed]**; that a multiplication cannot help rests on
    the 7 in count (G) **[argued]**.
21. Subset sums: 12 and not 11 at 8 points, modulo 2, 3, 5, 7 ([d-0](wave-01/d-0.md)) **[computed modulo
    p]**; 4 and not 3 at 4 points, modulo 5 in d-0 and modulo 2, 3 and 7 with the same program
    **[checked 11 October]**. With a free tree on each side, never below Yates at 4 to 32 points
    ([u-3](wave-06/u-3.md)) **[computed; exhaustive modulo 3 at 8 points, random search above]**.
22. The "squares" route of wave 1, the 16-point transform through the squares of the 4-point one in 62
    operations, is the textbook in other coordinates ([a-1](wave-01/a-1.md)) **[computed and argued]**.

### In the mechanism of my other result

23. In a simplified game without relabellings of addresses (L12), 4, 5 and 6 arrays cannot reach a saving
    of 1e-1 ([h-2](wave-04/h-2.md), [n-2](wave-04/n-2.md)) **[computed and argued; the model of the game
    was never audited]**.
24. A saving of 1e-1 by the engine's own mechanism is excluded up to stage width 9 inside one cost model
    ([ab-8](wave-08/ab-8.md), [ac-2](wave-08/ac-2.md)); above that it is open on paper only and cannot be
    searched. No part of an actual unit is near the rate that 1e-1 needs ([ad-0](wave-09/ad-0.md)).
    **[computed; nobody checked ad-0's replay of the unit's data files]**

### The six corrections of the tenth note

The last wave's critics corrected these statements of the same wave. Where a report in
[wave-10](wave-10/) says the first, read the second.

| | the report says | corrected to | by |
|---|---|---|---|
| i | subset sums "have no volume", so only one wall stands before linear size ([ah-cross](wave-10/ah-cross.md)) | false: their volume is about 0.277 N √(log2 N) | [ai-2](wave-10/ai-2.md) |
| ii | the relation lemma, stated without saying in which arithmetic (ah-cross) | false over the rationals (a cycle of three at 8 points, degree 2); it holds modulo 2, and over the rationals a weaker form arrives three degrees later | [ai-1](wave-10/ai-1.md) |
| iii | degree 3 pays "beyond addresses of 2^2059 bits" | 2,060 bits | [ai-0](wave-10/ai-0.md) |
| iv | "the transform up to multiples of 16 in 2N + o(N)" | 3N + o(N) by that route | ai-0 |
| v | [ag-4](wave-10/ag-4.md)'s floor of 3N/2 for the transform | below a two-line count, 2N − 2 | ai-1 |
| vi | the "weight" of an operation in a class identity (ah-cross) | it depends on the letter chosen; with another letter the same count asks for 0 | ai-2 |

### Statements in early reports that later reports withdrew

Later reports stand. This list is every item of the notes' own "taken back" and "corrections" lines. The
reports concerned carry an editor's note at the top.

- **Wave 1.** "Every block is two calls of the transform": false over the rationals; the true statement
  is "at most six calls" ([a-0](wave-01/a-0.md)). "Any Jordan basis works" (a claim about one family of
  changes of coordinates): fails at 4 points. The "log-log middle" overtakes the dense one only beyond
  N = 2^4096. The "squares" route is not independent evidence. That the circuits below the textbook hold
  "a wire that is flat on both sides, the transform's own eigenvector": wrong beyond 4 points; in the
  56-operation circuit the helpers are only not tight ([a-2](wave-01/a-2.md)), and the third note
  withdraws the eigenvector reading.
- **Wave 2.** "Below the textbook in OpenAI's count" holds only for the transform divided by √N
  ([b-0](wave-02/b-0.md)). "17 moves is open" (a question about the engine): closed
  ([b-1](wave-02/b-1.md)). The obstruction of lead 2.10 bounds the average row, not each row
  ([b-2](wave-02/b-2.md)). The first wave's guess "about the singular blocks" was wrong
  ([e-0](wave-02/e-0.md)). The "conservation law" at 16 points is one bit per operation for one kind of
  gate, and e2-0's 60 operations break it.
- **Wave 3.** Searches modulo 5 and modulo 7 gave two false circuits; later searches use larger primes
  ([g-3](wave-03/g-3.md)). The first wave's "nobody has badly conditioned steps with a perfectly
  conditioned product" is false as stated: g-3 has a family at 16 points, and it buys nothing.
- **Wave 4.** "56 operations at 16 points, below the list's 60" compares two different outputs
  ([n-0](wave-04/n-0.md)).
- **Wave 5.** "Two letters cost 2 operations more than three at 16 points": wrong
  ([r-0](wave-05/r-0.md)). "What the transform has beyond its class is worth at most N √(log N)": does not
  follow ([r-2](wave-05/r-2.md)). "No wall covers" wave 5's new question about subset sums: door 13 does.
- **Wave 6.** "A reflection needs two calls instead of four" (a reflection is a symmetric table that
  undoes itself): not a saving ([v-2](wave-06/v-2.md)). The circuit equal to the transform up to multiples
  of 4 "uses a fact special to the number 2": it works for the whole class ([x-1](wave-07/x-1.md)). The
  counts 5, 13, 30, 80 sat on Yates' line by a coincidence of small sizes. u-8's kind of circuit is larger
  than u-9's from 8 points on; the floor of door 4 holds for the larger one ([v-0](wave-06/v-0.md)).
- **Wave 7.** "With any coefficients" in door 3 must read "any rational coefficients". "At least three
  blocks per array" for the engine: not a floor; programs that pass the engine's rules have two
  ([ab-1](wave-08/ab-1.md), [ab-6](wave-08/ab-6.md)). The ceiling 0.098 on the engine's saving covers one
  narrower kind of unit only ([z-1](wave-07/z-1.md)). The floor of door 6 is not a floor for circuits: the
  19 is below it ([z-2](wave-07/z-2.md)). The Lean theorem of my other repository states a saving of
  8.762479e-4; "8.7625e-4", which many reports write, is that figure rounded up, and a saving of exactly
  8.7625e-4 is not what was proved (z-1).
- **Wave 8.** The explanation of the operation saved modulo 2 is wrong ([ac-0](wave-08/ac-0.md)). The
  stage widths 690 and 210 are 687 and 206 ([ac-2](wave-08/ac-2.md)). "0.006 of a move per block" is a
  rate for the data arrays alone, spread over 22 to 29 times as many blocks
  ([ad-0](wave-09/ad-0.md)). "Two blocks with 7.4 % of the moves skipped" is the worst way to have two
  blocks; one big block plus single moves needs 1.4 %. A "cheap control" planned for one experiment is
  the hard case itself ([ab-3](wave-08/ab-3.md)), and wave 7's "one specimen with tall wires" is not tall
  ([ab-2](wave-08/ab-2.md)).
- **Wave 9.** "Wave 9 closed the line-sum route": too strong ([af-1](wave-09/af-1.md)). "The transform
  modulo 8 in 2N + o(N)": 3N + o(N) ([af-0](wave-09/af-0.md)). The 8-operation circuit "that belongs to
  the transform and not to its class" works for every block ([af-2](wave-09/af-2.md)). ad-7's guess on
  repeated wires is false, and "at least 2 log2 N flats" fails once the signs of rows and columns are
  free (af-2). The briefs of the tenth wave ([WAVE10-PICKS](wave-10/WAVE10-PICKS.md)) were written before
  these critics reported and still carry the second statement; the ninth note says the third as well.
- **About earlier work.** The reports credit the 4-point circuit to Alman and Rao or to a patent filed in
  2002, and several call 7/8 "the best published rate" on that basis. The circuit and the rate are due to
  Coppersmith, Feig and Linzer (1994). Reports that write "Alman and Rao (2022)" mean the paper published
  in 2023. Full references: [README.md](README.md#earlier-papers).

### Where reports disagree and nothing later settles it

1. **How large a port can be** (a term of the engine: a set of directions along which the transform splits
   off). [x-6](wave-07/x-6.md) says at most a third of a stage. Its critic [z-1](wave-07/z-1.md) says that
   step is overstated: it holds for one narrower kind of unit, and between a third and a half nothing is
   decided. [ad-0](wave-09/ad-0.md), two waves later, builds its figure "1/9 of a stage" on x-6's third,
   which x-6 states "for scatters of the published kind", and the tenth note repeats the figure without
   that limit. Whether a port between a third and a half of a stage can be used is settled by no report.
2. **The lower bound 15 at 8 points.** In the waves it is one hand argument
   ([j-failproof](wave-02/j-failproof.md)) that later reports call "the known lower bound". Since then a
   proof was written out and read by one AI agent (lead 1.4). No person has checked it.
3. **Two copies of the 4-point transform.** See the end of lead 2.1: the last wave treats as untried what
   wave 2 had run modulo 3.
4. **A conflict between two readings of the published unit** ([h-7](wave-04/h-7.md) against
   [h-8](wave-04/h-8.md)). [u-5](wave-06/u-5.md) gives an answer **[argued; matched on three counts; not
   read from the engine]**. No critic read it.
