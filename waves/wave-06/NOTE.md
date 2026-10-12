# Sixth wave of ideas: what came out (wht39)

> Editor's note (11 October 2026): line 9 of section 1 gives 0.315·N·log2 N as "a published result of 1973, Morgenstern". Nobody here opened that paper, and 0.315 is the agents' own variant of its argument, for coefficients 1 and 2. The seventh note also corrects one guess of this note: the circuit of u-9 does not use a fact special to the number 2; it works for the whole class. See line 10, "Corrections", in [the seventh note](../wave-07/NOTE.md).

11 October 2026, about 04:00. Private. Nothing here is reviewed by a person or in Lean.
Marks: **[computed]** exact run tonight; **[argued]** by hand tonight; **[guessed]**; **[read]** from a report. "Mine" means I re-ran it for this note with my own counter (`s-note/check.py`). A search that is not exhaustive gives an upper bound only. "Modulo 3" means no circuit exists in arithmetic modulo 3: evidence, not a decision.

**What this wave was.** Ten agents each developed one idea (`u-0` to `u-9`), one recombined all six waves and tried four hybrids (`s-cross`), three critics came last (`v-0`, `v-1`, `v-2`). Earlier notes: `NOTE.md`, `WAVE2-NOTE.md` to `WAVE5-NOTE.md`. The seventh wave (`x-*`) is running and is not covered.

**Words.** N = 2^k points; an address has k bits. The *textbook* computes the transform in N·log2 N gates. Count **(G)**: a gate is any a·u + b·v, scalings free. Count **(O)**: OpenAI's, each addition and each multiplication by a constant costs one. Numbers are (G). *Subset sums*: for every set S, the sum of the data over the subsets of S; *Yates* is the usual method, (N/2)·log2 N gates. The transform is two passes of subset sums and one layer of scalings, so subset sums in O(N) would be the transform in O(N). A *wire* is a value the program holds, written as N coefficients, one per input. A *sign vector* is a wire whose coefficients are 0, +1, −1 after one scaling; its *set* is where they are not 0. A *merge tree* starts from the N inputs and keeps replacing two held sums by one; a *chain* is the most lopsided tree (running sums). *Bounded coefficients*: every gate is u + v, u − v or a multiplication by a number of size at most 2. That is a narrower count than (G) and (O), where one operation may multiply by any number. The *brick* (7 gates, 4 points), *the 19* (8 points) and the *staircase* (7, 20, 52, 128, 304) are the night's records.

## 1. What came out, in ten lines

1. **Nothing beats the textbook in order, and this wave has no record.** No saving of the 1e-1 kind, no linear size [read: ten reports, the recombination, three critics]. It has two walls that are now exact statements, each read by a critic, and a measured anatomy of the published unit.
2. **The fifth wave's open door is closed.** The "two-chain" program for subset sums (section 2) needs at least about N^1.32 / log N gates, which is more than Yates' count from about 2^51 points on [argued four times, independently, by `u-0`, `u-1`, `u-2`, `u-6`; the critic `v-1` read all four line by line, found no wrong step, and tested every inequality up to 512 points].
3. **The corner counts**: 5 and 13 are exact; 30 and 80 are the best of many searches; 239 and 715 are weak (section 2) [computed; mine for the recount].
4. **Every record of the night lives in one class, and that class has an exact floor.** If every wire is a sign vector whose set is a node of one *tree of halvings* (the cube cut into two parallel halves, each half cut again, down to single addresses), the transform costs at least N − 1 + (N/2)·log2 N gates: 2, 7, 19, 47, 111, 255 [argued by `u-8` and `u-9` independently; `v-0` read both and found no gap]. 7 and 19 are the exact minimum of the class [computed, exhaustive at 4 and 8 points with `v-0`'s own program, which nobody has read]; 16 points lies between 47 and 52. So no circuit of this kind goes below half the textbook, and more searching inside it can only move a constant.
5. **Subset sums with a free tree on each side lands on Yates to the gate**: 4, 12, 32 gates at 4, 8, 16 points, then 81 against 80 at 32. At 8 points this is exhaustive over all 135,135 input trees modulo 3, with none at 11 [computed, `u-3`]. Never below.
6. **The transform built as (subset sums) × (scalings) × (subset sums)** [computed, `u-4`]: with two chains it costs 14, 38, 88, 220 gates against the textbook's 8, 24, 64, 160; with Yates in both passes exactly N·log2 N. Neither saves. No other factor of that triangular kind is cheaper (exhaustive at 8 points).
7. **The published unit under the fourth wave's meter** (section 3): it breaks "one merge tree" and "no Q gate", never "order 1" [computed, `u-5`].
8. **A new object that is not the transform**: a whole-number circuit of about 3.2·N gates (814 at 256 points) whose outputs equal the transform up to multiples of 4 [computed, replayed on all entries, `u-9`]. It is under the floor of line 4 from 32 points on, because its wires carry a 2 outside their own set. Exactness needs log2 N binary digits, and each further digit is expected to cost about 2N [guessed, `u-9`], so as it stands it is N·log N again.
9. **Volume, with numbers.** A circuit with bounded coefficients needs about 0.315·N·log2 N gates for the transform (a published result of 1973, Morgenstern, recalled from memory), and at least 0.277·N·√(log2 N) − N for subset sums (the same method, in the form of Bürgisser and Lotz 2003) [read and re-derived, `v-2`]. So linear size by adding and subtracting only was excluded before this wave began. Neither number bounds counts (G) or (O).
10. **Corrections.** (i) The fifth note said of the corners "no wall covers it": lines 2 and 9 do. (ii) 5, 13, 30, 80 sat on Yates' line by a coincidence of small sizes: (N/2)·log2 N + 1 is 5, 13, 33, 81. (iii) The recombination's "a reflection needs two calls instead of four" also holds for every 2 × 2 rotation, and it is not a saving: 12 gates against 8 [computed, `v-2`]. (iv) `u-8`'s class is larger than `u-9`'s from 8 points on; the floor holds for the larger one [argued, `v-0`].

## 2. The corners of the subset-sum matrix

**The picture.** Put the outputs in one order (rows) and the inputs in another (columns), and write 1 where the input set lies inside the output set. The two-chain program makes running sums of the inputs in the column order, then gets each output from the next one by adding or subtracting a few running sums. A *step* is two neighbouring outputs. A *corner* is one term of a step: a place where the difference of the two rows changes value. A *run* is a stretch of consecutive inputs on which that difference is one non-zero value. The program costs N − 2 + corners gates.

| points | 4 | 8 | 16 | 32 | 64 | 128 |
|---|---|---|---|---|---|---|
| least corners found | 5 | 13 | 30 | 80 | 239 | 715 |
| how it is known | exhaustive | exhaustive | 44 of 44 restarts; never 29 | 5 of 5 restarts | one unfinished restart | one short restart |
| corners per point | 1.25 | 1.63 | 1.88 | 2.50 | at most 3.73 | at most 5.59 |
| gates, N − 2 + corners | 7 | 19 | 44 | 110 | 301 | 841 |
| Yates | 4 | 12 | 32 | 80 | 192 | 448 |
| regular order (Gray walk) on both sides | 7 | 21 | 63 | 189 | 567 | 1,701 |

**Exact and not.** 5 and 13 are minima over all pairs of orders, by three programs of three agents (`u-1`, `u-4`, `v-1`) [computed]. 30 is not shown minimal. The last two columns are upper bounds. The regular order is the one in which every step changes one address bit (a *Gray walk*). My own counter gives 13, 30, 80, 239, 715 on the saved orders and exactly 7·3^(k−2) for the regular order. On the saved orders the share of steps that are a single run falls with size: 7 of 8, 13 of 16, 21 of 32, 20 of 64, 24 of 128, and the largest number of runs in one step rises: 2, 2, 3, 4, 7 [computed; mine].

**What the theory found.** If L consecutive inputs all lie inside one output set, that set contains their union, which has at least log2 L elements. So a long run serves only the few outputs just above its union, and one order of the inputs has only N stretches of each length. A step between two large outputs must switch half of a sub-cube. Supply against demand forces the runs per step to grow like a power of N [argued; `u-1` calls it the window lemma]. The strongest version (`u-2`) gives corners ≥ (5/2)^k / (400·(1 + ln N)). So the least corner count lies between N^1.32 / log N and 0.78·N^1.585. Also: "every step is one run" is possible at 4 and 8 points, impossible at 16 on a path and at 32 on a tree [computed, exhaustive; the critic re-ran the path with a different program and the same node counts; the tree rests on one author].

**Plainly.** Corners per point are **not bounded, and they do not grow like log N: they grow like a power of N** [argued; read by one critic, by no person]. Per extra address bit the corner count is multiplied by something between 2.5 and 3, where Yates' count is multiplied by a little over 2. The bound is below one corner per point until 2^35 points, so at sizes one can run only the measurements speak, and they rise at every size. **For linear size this route is closed.** Two neighbours were tried and do no better: two or three input chains save about a third and still grow by 1.25 to 1.55 per doubling up to 128 points (`u-6`); tables of running totals in two dimensions, in regular shape, triple per bit as well (`u-2`) [computed]. Not covered by the arguments: *helper wires* that are not outputs (the one thing all four arguments need, and Yates has them), signs or scalings on both sides (a sketch only), several orders inside one step.

## 3. What an order-changing step looks like

**The meter** (fourth wave). Scale each wire to whole numbers that are not all even and keep only odd or even: that is the wire's *class*. Every record obeys three rules. *One merge tree*: any two classes are nested or disjoint. *No Q gate*: a Q gate takes two wires of the same class and returns half their difference. *Order 1*: a gate that lands on a class already held repeats an earlier wire up to multiples of 2, never up to multiples of 4 (unless it is an exact copy).

**The published unit** [computed, `u-5`: one invocation, 122,880 points, 10,146 layers, read from the certificate].
- *One merge tree* breaks first, 2 % into the program (layer 220): one source array is held after transforms along two sets of address bits that cross. 497,457 classes where a tree allows 245,759.
- *No Q gate* breaks second, at exactly two places: the 72 moves that bring 8 large totals down (36,864 Q gates) and the last addition into each of the 120 targets (61,440).
- *Order 1* is never broken.
- The anatomy: contents held on crossing sets; a few large sums brought down; a scatter that leaves each target holding 2 × (the wanted term) plus an odd mixture of 56 others; the mixture removed by additions only, ending in one halving per target. The wanted term sits exactly one binary digit under what the wire shows. The second result's unit obeys the same law (1,320 targets, one halving each).
- In the engine's terms the cost per point obeys c(m·F) = a·c(F) + b. The textbook has a = m; the unit has a = 44.905 for m = 45; linear size needs a below 1, and a = 1 would be n·log log n. This mechanism gains one direction per array per unit, so it cannot reach 1e-1 [argued; agrees with the avenues study].

**Do small circuits break the rules too? Yes, and none profits.**
- `u-4`'s subset-sums circuit with Yates leaves the tree with no Q gate and order 1, at exactly the textbook count. Leaving the tree is free and buys nothing [computed].
- `u-4`'s two-chain version breaks the tree and the order (up to about log2 N − 1), with Q gates in one arrangement only (6 at 32 points). It is above the textbook [computed].
- The records break none. In every record no difference of two full wires occurs twice, so a Q gate would have nothing to reuse; none of the 2,748 best 8-point subset-sum circuits has one [computed, `u-7`].
- `u-9`'s circuit of line 8 stays one tree, with no halving, and gets under the floor another way: two sizes of entry in one wire.

So the unit's signature, crossing sets plus one halving that lifts out a term one digit down, is not in any small circuit that saves a gate [computed for the parts; the reading is guessed].

## 4. The ideas that are alive

**A. One gate, two jobs.** The floor of line 4 is two budgets added: N − 1 gates that only connect, and (N/2)·log2 N gates that each carry one factor 2 of the transform's determinant. Inside the class they cannot merge. Outside it, `u-4` has a 26-gate circuit at 8 points whose joins carry 5 of the 12 factors, and wastes more than it gains [computed, `s-cross`]. *Next:* 1.

**B. Two binary digits in one wire.** The two objects that get under a floor do it one digit down (lines 7 and 8). By the volume count, C·N gates need multipliers that grow by about (log2 N)/(2C) digits per gate on average [argued; Morgenstern's argument as a ledger]. Against it: no exact circuit of six waves holds two digits, and every record has multipliers of at most 2 [computed]. *Next:* 2.

**C. The transform as a box with relations.** A program that only *calls* a K × K box A to get A·X·Aᵀ, and is right for every A, makes at least 2K calls [argued, `s-cross`; re-derived by `v-2`]. For a reflection whose mirror has half the dimension, which is what the transform is, the best count anyone has gives only K − 1 [argued, `v-2`]. K calls with cheap glue would be N·log log N. There is no sign such a program exists: at K = 2 the glue costs a whole transform, and a few starts at K = 3 found nothing [computed, floats]. *Next:* 4.

**D. Subset sums with multipliers that grow.** Every subset-sum model of waves 5 and 6 adds and subtracts only. Line 9 says none can be linear. It leaves N·√(log N) open even for them. With the one layer of scalings in the middle (N operations) that would be the transform at a saving of 5e-1 [argued, `v-2`: a missing bound, not evidence; every model measured is on or above Yates]. Through subset sums the growth needed is far smaller than directly: about 0.277·√(log2 N)/C digits per gate. *Next:* 6.

**E. The third turn.** The transform times a diagonal of signs, divided by √N, is a rotation by 120 degrees: its cube is the identity [computed exactly at 4, 16 and 64 points, `s-cross`]. This explains three stray facts of earlier waves (a block of rank 35, the "third turn", sixth roots of unity). It gives no circuit yet. *Next:* 5 and 8.

**F. The floor's three hatches.** A *hatch* is a hypothesis of a wall that a better circuit could break. The floor has three: wires with entries of two sizes, sets that cross the tree, halves that are not parallel. The published unit uses the second and `u-9`'s circuit the first; no report names a circuit that uses the third. *Next:* 3 and 7.

## 5. The walls, as lemmas

All [argued] unless marked. Numbers continue `WAVE5-NOTE.md`.

- **L1. Half and half.** A change of basis costs half a transform in and half out. `d-0`, `d-3`, `d-4`, `d-7`, `g-0`, `g-2`, `g-5`, `g-7`, `p-2`, `p-5`; now `u-4` (line 6) and `s-cross` (idea E).
- **L2. Copies do not share**, now with a lemma: the sealed box of idea C. `d-2`, `d-6`, `e-3`, `e-6`, `e-7`, `e2-1`, `e2-2`, `j-manyatonce`, `g-5`, `g-6`, `g-7`, `h-2`, `n-2`; now `s-cross`, `v-2`, and `u-8` (inside the class of L14, joining two circuits never costs less than the sum). Open where the box has relations of its own; the published unit is the one exception.
- **L4. Volume.** Small multipliers grow a determinant slowly. `d-5`, `e-5`, `e2-0`, `j-failproof`, `g-1`, `g-3`, `g-4`, `g-5`, `h-1`, `n-0`, `p-5`, `p-8`; now `u-6` (a second merge tree sits inside it), `s-cross` (every record has exactly (N/2)·log2 N gates with multiplier 2 [computed]) and `v-2` (for subset sums the method gives 0.277·N·√k to within N, and can give no more).
- **L5. One class of kernels** (every saving found also works for the other 2 × 2 building blocks without a zero). `d-0`, `a-0`, `g-3`, `g-4`, `g-5`, `k-cross`, `h-6`, `p-0`, `r-2`. Not re-tested; `u-9`'s circuit uses a fact special to the number 2 and may be the first exception [guessed].
- **L6. The extra value.** `g-3`, `g-7`, `p-5`.
- **L7. Two periodic tree steps** stop at 16 points. `g-6`, `c-2`, `p-3`.
- **L10. Width.** Wires that mix at most b bits need N·log2 N / b gates. `h-5`, `n-1`.
- **L12. Old letters.** `e2-2`, `h-2`, `n-2`, the tiny-units note.
- **L13. One form per node** (a *letter*: each output is one earlier output plus nodes of one merge tree of the inputs). `g-1`, `g-6`, `k-cross`, `p-1`, `p-3`, `p-4`, `p-6`, `p-7`, `p-8`, `q-cross`; now `u-3` (subset sums: only about k rows of each size can be one node away from another row; the tie with Yates is measured, not argued) and `u-9` (the transform up to multiples of 4 costs exactly (N/2)·log2 N on two chains and at least (N/4)·log2 N in any letter).
- **L14. One tree of sign vectors** (new; takes in L3 tight wires, L9 pay once, L11). The statement of line 4, halving gates allowed. `u-8`, `u-9`, `v-0`; before as a guess `m-cross`, `h-6`; from the side `u-6` and `u-7` (a halved difference used as a partner serves at most N / (size of its set) outputs). In the class, flipping the sign of a wire on a node needs a second held wire that agrees with it there, its *partner*. The floor is the exact value of the game in which no partner is needed [computed to 128 points, `v-0`]; the gap up to the staircase is the price of partners.
- **L15. One line through the cube** (new). Section 2. `u-0`, `u-1`, `u-2`, `u-6`, `u-3`, `v-1`. The nearest published theory (sums over boxes in a fixed dimension; subset sums without subtraction) does not reach it [read, `v-1`, three searches].

Each wall fences one shape of program. None bounds a general circuit in count (G) or (O).

## 6. The next eight experiments

All eight are running in the seventh wave as this is written.

1. `twojobs`: at 8 points, wires with entries 0, +1, −1 on any set, plus "sign vector + 2 × sign vector"; is 18 gates reached, and which gate does two jobs?
2. `digits`: the cheapest circuit equal to the transform up to multiples of 8; does the third digit cost more or less than N/2?
3. `floorhatch`: release one hypothesis of the floor at a time at 8 points; which hatch reaches 18?
4. `boxrelations`: calls and glue for a 4 × 4 reflection used as a box; is anything under 8 calls with cheap glue?
5. `thirdturn-basis`: the sparsest basis of what the 120-degree rotation leaves fixed, and the recursion it gives.
6. `weightedz`: subset sums with multipliers 2 and 1/2 allowed; anything below 12 or 32 gates, and the price of growing multipliers.
7. `unit-as-box`: which relation of its moves does the published unit use that a sealed box lacks?
8. (silly) `rotate120`: the rotation as two mirrors that can be chosen; does the pair cost less than the one mirror of the transform?

## 7. What this says about linear size

Nothing found in six waves gives linear size or moves the exponent, and nothing forbids it in the counts that matter: the sixth wave closed the one concrete linear-size hope the fifth had left, and put an exact floor of half the textbook under the class that holds every record of the night [argued; each read by one critic, by no person]. Together the walls now describe what a linear program would have to be: its multipliers must grow with N, it must leave that class by one of the hatches of idea F, and it must use a relation of the transform itself instead of calling it as a box [argued; the first part is the 1973 result for bounded coefficients]. The only program that changes the order does all of this in a thin form, one binary digit and one direction per unit, its saving is 8.7625e-4 and that mechanism cannot reach 1e-1 [argued, `u-5`]; no small circuit does any of it at a profit, and whether one can is what the seventh wave is testing [computed for the unit's anatomy; the reading is guessed].
