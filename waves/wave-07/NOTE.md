# Seventh wave of ideas: what came out (wht39)

> Editor's note (11 October 2026): where line 4 of section 1 says "a published result of 1973 (Morgenstern)", the critic z-0 had two later descriptions of that paper and not the paper. Line 10 (v) of the same section stands: the Lean theorem of my other repository states a saving of 8.762479e-4. The eighth note corrects two things in this note: "three blocks per exchange" (wall L19) is not a floor, and "two blocks with 7.4 %" is the worst way to have two blocks. See line 10, "Corrections", in [the eighth note](../wave-08/NOTE.md).

11 October 2026, about 05:30. Private. Nothing here is reviewed by a person or in Lean.
Marks: **[computed]** exact run tonight; **[argued]** by hand tonight; **[guessed]**; **[read]** from a report. "Mine" means I recomputed the formula for this note (`w-note/check.py`); I replayed no circuit. A search that is not exhaustive gives an upper bound only. "Modulo 3" means no circuit exists in arithmetic modulo 3: evidence, not a decision.

**What this wave was.** Ten agents each developed one idea (`x-0` to `x-9`), one recombined all seven waves and tried four hybrids (`w-cross`), three critics came last (`z-0`, `z-1`, `z-2`). Earlier notes: `NOTE.md`, `WAVE2-NOTE.md` to `WAVE6-NOTE.md`. The eighth wave (`ab-*`) is running the eight experiments of section 6 and is not covered.

**Words.** N = 2^k points; an address has k bits. The *textbook* computes the transform in N·log2 N gates. Count **(G)**: a gate is any a·u + b·v, scalings free. Count **(O)**: OpenAI's, each addition and each multiplication by a constant costs one. Numbers are (G). A *wire* is a value the program holds, written as N coefficients, one per input, scaled to whole numbers with no common factor. Its *height* is its largest coefficient; a wire of height 2^d "holds d binary digits". A *form* is a wire of height 1; a *tall* wire has height 2 or more. A *merge* is a gate that connects two groups of inputs not connected before. A *unit of volume* is one factor 2 of the transform's determinant; the transform needs (N/2)·log2 N of them. *Subset sums*: for every set S, the sum of the data over the subsets of S; the transform is two passes of subset sums around one layer of scalings. The *brick* (7 gates, 4 points), *the 19* (8 points) and the *staircase* (7, 20, 52, 128, 304) are the night's records. The *class*: all transforms built like ours from a 2 × 2 block [[1,1],[1,s]]; ours is s = −1.

## 1. What came out, in ten lines

1. **Nothing beats the textbook.** No circuit below a known count, no growth law below N·log N, no saving of the 1e-1 kind, no linear size [read: ten reports, the recombination, three critics]. The wave leaves four walls as exact statements, each read by a critic, one door, and one smaller question that linear size depends on.
2. **Can one gate join and carry volume? Yes, and it has never paid.** At most N − 1 gates of any circuit can do both, so two-job gates can remove the linear part of the floor and never the (N/2)·log2 N part [argued, `x-0`; re-run by `z-0`]. No circuit of the night has a wire of two binary digits that profits from it (section 2).
3. **Coefficients that grow: no rate improved.** Nearly dependent wires land nothing; a growing hub coefficient makes the rate 5/4 where +1 or −1 gives 3/4 (section 3).
4. **The height wall is exact now.** Whole-number wires of height at most M cost at least N − 1 + ((N/2)·log2 N − (N − 1)·log2 M) / log2(4M²) gates, whatever the coefficients [argued twice, `x-0` and `x-2`; `z-0` found no wrong step]. It is a published result of 1973 (Morgenstern) with one bridge added. For C·N gates it asks for about (log2 N)/(4C) binary digits per gate on average.
5. **Costs add, four more times.** Two mirrors (`x-7`), the 120-degree split (`x-4`) and a change to a symmetry basis by any bracketing (`x-5`) cost a whole transform or more; the relations of a box that vary continuously (symmetric, a reflection, a rotation) save at most 3 calls at any size (`x-3`). The "cheapest basis" asked for since wave 1 costs half a transform to within N gates, so it is the original question [argued, `w-cross`; computed to 256 points, `z-2`].
6. **Flag passes cannot be linear.** A *flag pass* is one sweep of weighted sums along a chain of nested subspaces (at most 3N − 3 gates). The transform needs at least about k / log2 k passes, with free scalings in between [argued, `x-4`; `z-2` re-derived it and widened it]. Best case N·log N / log log N: a saving exponent of 0.
7. **The digits of the transform have a price list** [computed, replayed to 256 points, `x-1`; formula mine]. Whole-number circuits equal to the transform up to multiples of 4, 8, 16 take 757, 1,223, 1,605 gates at 256 points. Each low digit costs about 2N; all digits together cost exactly N·log2 N. The first d digits are the transform at its lightest outputs. There the only floor known is about 2N gates and the known route pays (d + 1)·N: a gap with no wall in it [argued].
8. **The door: ports.** A *port* is a set of address directions along which the transform splits into two smaller transforms. Ours has 2^(h−1) ports of one direction on h bits; every other member of the class that was tried has h [computed, `x-6`]. The ports are exactly the sets of directions that share nothing with their own perpendicular [argued for all sizes, computed to h = 6, `z-1`]. So the published saving is the first of the night that is not shared by the whole class. Its exponent follows a law that counts *blocks* (section 4, idea B).
9. **A smaller question that linear size depends on.** The transform is the hardest *convolution* on the cube (output(y) = sum over x of q(x + y)·input(x)): a linear transform exists exactly when every such convolution is linear [argued, `w-cross`; `z-2` agrees]. The simplest one nobody can do in O(N) is *neighbour sums* (every address gets the sum of its k neighbours). With additions only it costs exactly (3/4)·k·N − N for even k [argued, `z-2`; formula mine]. Whether subtraction helps is open.
10. **Corrections.** (i) Wave 6 guessed that the circuit equal to the transform up to multiples of 4 uses a fact special to the number 2. It does not: it works for the whole class [argued, `x-1`]. (ii) "With any coefficients" in the height wall must read "any rational coefficients" (section 3). (iii) `x-6`'s ceiling of 0.098 covers one sub-class only (idea B). (iv) `x-9`'s floor for hub circuits is not a floor for circuits: the 19 is below it (19 against 20) and outside its class [computed, `z-2`]. (v) The Lean theorem states a saving of 8.762479e-4; "8.7625e-4" is that figure rounded up [computed, `z-1`].

## 2. Can one gate do two jobs?

**Why ask.** The floor under every record (wave 6) is two budgets added: N − 1 gates that only join, and (N/2)·log2 N gates that each bring one unit. That is 7, 19, 47 at 4, 8, 16 points. A gate doing both would go under it.

**The lemma** [argued, `x-0`; `z-0` re-ran it on six circuits and 45,000 random gates, no violation]. Every circuit has exactly N − 1 merges. A merge a·u + b·v brings at most log2 of its larger coefficient: nothing if the new wire is a form, at most d units if it holds d digits. So two-job gates number at most N − 1 and grow like N, never like N·log N.

**The searches.** Only the 4-point rows are exhaustive without restriction.

| points | search | wires allowed | found |
|---|---|---|---|
| 4 | exhaustive, up to 228 million sets of helper wires | entries up to 1, 2, 3 | the same 228 circuits of 7 gates each time; none contains a tall wire |
| 4 | exhaustive modulo 5, 7, 11 (`x-9`) | any | 228 again; every helper has entries 0, +1, −1 |
| 8 | walks from the 19, about 2,400 circuits | entries up to 2; 0, 1, 2, 4; up to 3 | no 18; all 213 samples at 19 gates have 7 merges bringing 0 and 12 gates bringing 1 |
| 8 | exhaustive with six wires of the 19 fixed | height up to 2, six centres | no 18, also when the last merge carries a unit |
| 8 | 54 annealing runs (`x-2`) | crossing sets, any sets, tall wires | no 18; none of the eighteen 19s found has a tall wire or a crossing set |
| 16 | one walk, 164 circuits around the 52 | entries up to 2 | nothing below 52; says nothing |

All [computed]. Walks and annealing are not exhaustive. The two widest pools were walked with coefficients capped at 4.

**One gate above the floor everything exists** [computed, replayed]. At 8 points with 20 gates: a merge w8 = w6 + 2·x7 that joins the two halves and carries one unit (`x-0-twojobs/spec8_mergevolume20.txt`); and a gate with coefficient 4 that brings exactly 2 units from a wire of height 3. Each is paid for by one gate that brings nothing. The two-job merge saves a join and then needs a subtraction of its own, where the 19 shares one clean centre between two wires.

**Does any circuit hold two binary digits in a wire and profit? No** [computed for what was searched]. At 4 points none exists. At 8 points none was found: tall wires appear in 15 of 276 samples at 20 gates and in none of 55 at 19. At 16 points there is no information.

**The anomaly that stays.** "Minimum circuits contain only forms" cannot hold at every size: forms alone cost at least N − 1 + 0.315·N·log2 N, and the published program is below that in the long run [argued; rests on line 4 and on that program's constants being rational, which nobody checked]. So some size has a first tall wire that pays. Nothing says where.

## 3. Coefficients that grow

**Nearly dependent wires** (`x-8`). A wire is *nearly dependent* when it almost equals a combination of the others; numbers on the way become huge. Wave 5 had a "pump" that drives a meter called entropy this way. The hope was to spend it at the end. Found [computed, all states up to 5 to 7 moves on 3 and 4 wires]: the most entropy that can be brought back to an honest state after m moves is 2, 2, 4, 4, 6 for m = 2 to 6 (the last depth incomplete). That is never more than one unit per move, the textbook rate. It is the same whether the numbers on the way are held small or left free, and the same with coefficients up to 3 and 4. From the pumped states the nearest honest states hold 0. Why [argued; `z-0` checked 67 matrices]: at a landing with orthogonal rows, entropy is at most 2·log2 of the determinant, and a move changes the determinant only by the coefficient on the wire it overwrites. The pump uses coefficient 1 there, so it lands nothing. **The rate does not depend on how ill-conditioned the way is.** Not covered: landings whose rows are not orthogonal, irrational coefficients, circuits with extra wires; and the runs stop below ten moves.

**Growing hub coefficients** (`x-9`). A *hub* is a wire A + t·B made of two pieces [computed, exact replay, 4 to 64 points; 1,213 schedules of t scanned at 8 and 16 points]:

| hub coefficient t | gates at 8, 16, 32, 64 points | rate × N·log2 N |
|---|---|---|
| +1 or −1 (the staircase) | 20, 52, 128, 304 | 3/4 |
| 2, 3, 1/2, i, 1 + i | 28, 76, 192, 464 | 5/4 |
| growing: 2^j, or 2^(2^(j−1)) (65,537 at 32 points) | 28, 76, 192, 464 | 5/4 |

Exactly: (3/4)·N·log2 N + N/4 + (N/2) × (levels where t is not +1 or −1) [formula mine]. Why [argued]: a wire is one gate from an output only where it agrees with that output up to sign. A hub with two sizes of entry cannot, so its correcting wires double in size and nobody else uses them.

**The rate as a function of the allowed size** [argued; `z-0` checked each step].
- One gate between wires of height M brings at most log2(4M² − 6M + 3), about 2d + 2 units for d digits [computed to M = 32]. Never more than proportional to d.
- With all wires of height at most M: at least about N·log2 N / (4 + 4·log2 M) gates. The order stays N·log N; only the constant falls, like 1 / log M.
- C·N gates need on average at least (log2 N)/(4C) − 1 digits per gate. At 2^40 points that is 4 digits for 2N gates [mine].
- **Measured, the rate never fell as the size allowed rose**: flat at 4 points (exhaustive), flat at 8 (sampled), worse for hubs. `x-5`'s tower has coefficients up to about √k, more volume than needed from k = 8, and still k passes.
- Limits. The wall is silent at every size run: it gives 15, 9, 8 gates at 8 points for heights 1, 2, 3, against 19 known and the trivial 14 [mine]. It says nothing about irrational constants: with √2, wires with entries of size at most 1 take coefficients without limit [computed, `z-0`]. "A constant fraction of gates on tall wires" is not shown; only the average is.

## 4. The ideas that are alive

**A. Neighbour sums.** Necessary for a linear transform (at most two transforms). It needs almost no volume, so the height wall is silent. Data: 2 and 12 gates at 4 and 8 points; at 16 points one half (16 gates by pairing) has no circuit with 14 modulo 2, 13 modulo 3, 12 modulo 5 [computed, `w-cross`]. Growth like k·N would be the first evidence against linear size that does not go through volume. Growth like N would name the first cancellation that pays. *Next:* 1 and 6.

**B. Fewer blocks per array.** The published program repeats a *unit*: W arrays, each transformed along m directions; a *block* is a run of such steps on one array with no addition in between. The exponent z solves: sum over blocks of (rank/m)^z = W. `z-1` recomputed both published savings from the certificates with exact enclosures: 8.762482e-4 and 7.474549e-4 [computed]. With k equal blocks per array and a share ρ of directions skipped, saving = L / (ln k + L), L = ln(1/(1 − ρ)). The published unit has 16.5 blocks and ρ = 0.21 %. Two blocks with 7.4 % would be 0.1 [mine]. One block would be n·log log n, and the floor note argues one block cannot occur. On paper, fat ports give 0.126 and 0.101 at h = 7 with ports of 3 directions [computed arithmetic on block lists that no known network realises, `z-1`]. Linear size is out for this mechanism: at least three blocks per array [argued]. *Next:* 2.

**C. A tall wire that pays.** Line 4 says it must exist in any linear whole-number circuit; sections 2 and 3 say nobody has seen one. The one specimen with tall wires in the middle and last gates between two of them is the second pass of subset sums, at exactly N·log2 N. *Next:* 3.

**D. The map of convolutions.** Kernels q that depend only on the number of ones form a family with k + 1 numbers. It holds the identity, neighbour sums, the lightest outputs of line 7 and the transform. Is the transform the only dear corner? *Next:* 4.

**E. A meter for the part of determinant 1.** In count (G) scalings are free, so volume was never the cost: all of it sits in the two passes of subset sums, where no meter of the night reads anything [argued, `x-8`]. `x-2` has an identity true for every circuit and every cut: gates = (gates new on the left half) + (new on the right) − (new on both) + (new on neither), with at least N/2 + 1 new on neither. A linear circuit needs about N/2 gates new on both in every one of its N − 1 cuts. *Next:* 5.

**F. Address maps as the relation.** A program that calls a K × K box and must be right for a family of boxes needs 2K − 3 calls or more for each continuous family tried [argued, `x-3`; unreviewed]. The one family where the bound stays lower (1.5·K) is "the box up to a relabelling of addresses", with an exact 7-call program at K = 4 against 8 [computed]. This is the ports again. *Next:* 7.

**G. Constants that are not rational.** The height wall does not cover them, and the cost model charges one unit for any complex constant [read, `z-0`]. No pool of the night contained one. No experiment is assigned yet. [guessed that it is worth one]

**H. The transform in a row.** On a line, one wire served N/2 gates (a polynomial of degree 2 at N points in N + 1 gates) [computed, `x-1`]. On the cube no three points lie on a line. *Next:* 8.

## 5. The walls, as lemmas

All [argued] unless marked. Numbers continue `WAVE6-NOTE.md`.

- **L1 + L2. Costs add** (was "half and half" and "copies do not share"). A route "change of basis, something free, change back", or "a stage on some address bits, a stage on the rest", costs at least a whole transform. L1: `d-0`, `d-3`, `d-4`, `d-7`, `g-0`, `g-2`, `g-5`, `g-7`, `p-2`, `p-5`, `u-4`, `s-cross`. L2: `d-2`, `d-6`, `e-3`, `e-6`, `e-7`, `e2-1`, `e2-2`, `j-manyatonce`, `g-5`, `g-6`, `g-7`, `h-2`, `n-2`, `s-cross`, `v-2`, `u-8`. Now `x-7`, `x-4`, `x-5`, `x-3`, `w-cross`, `z-2`. Open only for address maps (idea F).
- **L4. Height** (was "volume"; line 4). `d-5`, `e-5`, `e2-0`, `j-failproof`, `g-1`, `g-3`, `g-4`, `g-5`, `h-1`, `n-0`, `p-5`, `p-8`, `u-6`, `s-cross`, `v-2`; now `x-0`, `x-2`, `x-8`, `x-3`, `x-9`, `x-5`, `z-0`. Sharpened from "bounded coefficients" to "bounded wires". Necessary, not sufficient.
- **L5. One class of kernels.** `d-0`, `a-0`, `g-3`, `g-4`, `g-5`, `k-cross`, `h-6`, `p-0`, `r-2`; now `x-1` (the digit circuits too) and `x-3` (the relation that shares calls at K = 2 is worth at most 3 calls at any size). Its boundary is known now: ports (`x-6`).
- **L6. The extra value.** `g-3`, `g-7`, `p-5`; now `x-8`.
- **L7. Two periodic tree steps** stop at 16 points. `g-6`, `c-2`, `p-3`. See L17.
- **L10. Width.** `h-5`, `n-1`. **L12. Old letters.** `e2-2`, `h-2`, `n-2`, the tiny-units note. **L13. One form per node.** `g-1`, `g-6`, `k-cross`, `p-1`, `p-3`, `p-4`, `p-6`, `p-7`, `p-8`, `q-cross`, `u-3`, `u-9`. **L15. One line through the cube.** `u-0`, `u-1`, `u-2`, `u-6`, `u-3`, `v-1`. Not touched in wave 7.
- **L14. One tree of sign vectors.** `u-8`, `u-9`, `v-0`, `m-cross`, `h-6`, `u-6`, `u-7`; now `x-2`: its three hypotheses are one, "no gate is new on both halves".
- **L16. Distance** (new as a lemma). Two rows of the transform differ on exactly N/2 points. Hence: a wire is one gate from n outputs only with correcting wires of at least (N/2)·(1 − 1/√n) points; N/2 + 1 gates are new on neither half in every cut; from the third digit on a helper serves one output. `j-cross`, `x-9`, `x-2`, `x-1`, `x-7`, `x-4`, `x-8`. The grouping is `w-cross`'s; statements were matched, not arguments.
- **L17. Flag passes** (new; line 6). `x-4`, `z-2`. Two passes are impossible from 32 points on, over the real numbers. Not covered: trees that are not made of subspaces.
- **L18. Two-piece hubs** (new). In that class at least (3/4)·N·log2 N + N/4 gates for every coefficient. `x-9`, `z-2`. The 19 is outside the class.
- **L19. Three blocks per exchange** (new; the published mechanism). `x-6`, `z-1`, the floor note. Ports of half the directions are dead; between a third and a half nothing is decided.

Each wall fences one shape of program. None bounds a general circuit in count (G) or (O).

## 6. The next eight experiments

All eight are running in the eighth wave as this is written.

1. `neighbour-sums`: least gates at 16, 32, 64 points with free coefficients; like k·N, like N·log k, or like N?
2. `fewer-blocks`: search the engine's small game for 2 or 3 blocks per array with fat ports; does a legal network exist?
3. `tall-pool`: wires "sum of 2^j × form" with no cap on coefficients at 8 and 16 points; do gates fall as j grows?
4. `convolution-ladder`: price a grid of convolutions at 16 and 32 points; which are linear, where does the cost jump?
5. `z-cut`: the cut identity applied to subset sums; a floor that reads where the determinant is 1?
6. `cancellation-literature`: what is published on subset sums and the cube with and without subtraction; then one test.
7. `chain-of-exchanges`: arrays in a ring, one shear ending one exchange and starting the next; blocks per array?
8. (silly) `transform-in-a-row`: true Pascal's triangle in place of subset sums, on a line where three points do align.

## 7. What this says about linear size

Nothing found in seven waves gives linear size or moves the exponent, and nothing forbids it in the counts that matter: every wall fences a class, and the strongest one is silent at every size anyone can run [argued; each read by one critic, by no person]. The walls now say what a linear program would have to be, all at once: typical gates on whole numbers of about (log2 N)/(4C) digits or on irrational constants, last gates between two such wires, about N/2 gates shared by the two halves in every cut, and use of the transform's own symmetry, the ports; no object of the night has more than two of these [argued for each part; the list is `w-cross`'s reading]. The published mechanism cannot be that program, whether it can reach 1e-1 is open on paper only, and the cheapest test of linear size is now neighbour sums in O(N), which the eighth wave is measuring [argued; that the test will be visible by 64 points is guessed].
