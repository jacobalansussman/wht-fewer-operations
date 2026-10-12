# Eighth wave of ideas: what came out (wht39)

> Editor's note (11 October 2026): the ninth note corrects one figure of this note: "about 0.006 of a move per extra block" is a rate of the data arrays diluted 22 to 29 times. See line 10 (vi), "Corrections by the critics", in [the ninth note](../wave-09/NOTE.md).

11 October 2026, about 06:45. Private. Nothing here is reviewed by a person or in Lean.
Marks: **[computed]** exact run tonight; **[argued]** by hand tonight; **[guessed]**; **[read]** from a report. "Mine" means I recomputed the formula for this note (`aa-note/check.py`); I replayed no circuit. "None modulo 3" means no circuit exists in arithmetic modulo 3: evidence, not a decision. A *what-if* is arithmetic on a list of blocks that no known program realises.

**What this wave was.** Nine agents each developed one idea (`ab-0` to `ab-8`): the eight experiments of `WAVE7-NOTE.md` section 6 and one reconciliation of the earlier ceilings on the engine; one recombined all eight waves and tried four hybrids (`aa-cross`), three critics came last (`ac-0`, `ac-1`, `ac-2`). The ninth wave (`ad-*`) is running section 6 below and is not covered.

**Words.** N = 2^k points; an address has k bits. The *textbook* computes the transform in N·log2 N gates. Count **(G)**: a gate is any a·u + b·v, scalings free; all gate numbers here are (G). Count (O), OpenAI's, is not used. *Neighbour sums*: every address gets the sum of the inputs at its k neighbours (addresses one bit away). *Adding-only*: gates u + v, nothing ever cancels. *Subset sums*: for every set S, the sum of the data over the subsets of S; the classical count is (N/2)·log2 N (Yates). A *flat* is a subspace of addresses or a shifted copy of one; a *coset sum* gives every address the sum over its flat. The *engine* is the published program's mechanism: a *unit* transforms W arrays, each along m directions; a *move* is one direction on one array; a *block* is a stretch of an array's life with no interruption; a *stage* is a group of h address bits; a *port* is a set of r directions along which the transform splits off; a *total* is a shared sum that several arrays read; an array *knows* another when it can later remove that array's share from a total; *kappa* is the number of arrays one total serves; *helpers* are extra arrays that hold what must be removed; an *address map* is a free relabelling of the addresses inside a block; a *phase letter* is a free multiplication by signs or powers of i that depend on the address [my reading of `ab-1`]. The saving is 1 − z, with z the root of "sum over blocks of (rank/m)^z = W".

## 1. What came out, in ten lines

1. **Nothing beats the textbook.** No circuit over the rationals below a known count, no growth law below N·log N beyond the published one, nothing of the 1e-1 kind, no linear size [read: nine reports, the recombination, three critics].
2. **Neighbour sums, the test of linear size set by wave 7, gave no saving.** The cheapest circuit at every size is additions only: (3/4)·k − 1 gates per point for even k. Cancellation saves one gate, in arithmetic modulo 2 only (section 2).
3. **One exchange rate was measured four times, and it is one for one.** When one wire or one call serves two uses, the foreign part must be removed, and the removal cost exactly what the sharing saved: subset-sum circuits cut in two (`ab-4`, 552 cases of 552), the same cut read from the literature (`ab-5`, a tie at 8 points), programs that call a box (`ab-6`), the engine's exchange words (`ab-1`) [computed and argued, each in its own class].
4. **The bar of 1e-1 by the engine's own mechanism: excluded up to stage width 9 inside one cost model, open on paper only above that, and not searchable** (section 3). In one unit of measure: 1e-1 asks for 0.28 to 0.78 moves saved per extra block at block sizes 4 to 110; the published unit has about 0.006 [computed, floats; mine; the unit's figures are quoted from `x-6` and `ab-1`, nobody reopened the certificates].
5. **Objects that now exist** [computed, replayed by their authors]: a 15-gate circuit modulo 2 for half of the neighbour sums at 16 points, where adding-only needs 16 (`ab-0`; replayed by `ac-0`); the smallest matrix where a wire with a coefficient 2 saves a gate, 4 × 4, 6 gates against 7 (`ab-2`); the transform written as a convolution on a row with carries, 8 to 256 points (`ab-7`); legal exchange words for a ring of arrays, each using more moves than the plain schedule (`ab-6`).
6. **Walls that are now exact statements**, each read by a critic unless marked: the adding-only law for neighbour sums, N·(k − 1 − floor(k/2)/2) [argued twice]; the *leak lemma*, at least 2K − 2 calls where wave 7 had left room at 1.5·K [argued twice; not found in print]; the *order bound*, kappa ≤ 1 + (2^(h−r) − 1)/(2^r − 1) [argued twice; known in index coding, a part of network coding]; "neighbour sums and the transform both need k/2 coset sums or more" [argued twice]; for subset sums a *no-return* statement and a *cut lemma* [argued once, unreviewed; possibly Find and Boyar's 2013 theorem restated].
7. **Why coefficients that grow never paid** [computed + argued, `ab-2`, `ab-7`]. A tall wire pays in two known ways: as the difference of two needed wires that have zeros and opposite signs (112 specimens, all saving exactly one gate), or after a rescaling that turns a matrix into a convolution (Pascal's triangle). Both need entries of different sizes. All entries of the transform have one size.
8. **Still alive** (section 4): the rate per block inside the published unit; all line sums of a finite plane, the one relation here whose success would pass the bar; deliveries that share their cost; three reformulations with a search space of their own.
9. **Most surprising.** Four unrelated objects gave the same rate, exactly one for one, and the published unit is the only specimen on the transform that keeps anything: about 0.006 of a move per extra block [read: `aa-cross`].
10. **Corrections.** (i) Wave 7 wrote "at least three blocks per array" for the engine. That is not a floor: legal words have two [argued, `ab-1`; computed, `ab-6`]. (ii) Wave 7's "two blocks with 7.4 % of the moves skipped" is the worst way to have two blocks; one big block plus single moves needs 1.4 % at the published block size 45 [computed, floats]. (iii) The "cheap control" planned for the map of convolutions is the hard class itself (`ab-3`); wave 7's "one specimen with tall wires" is not tall (`ab-2`). (iv) `ab-0`'s explanation of its saved gate is wrong; the gate comes from one plane sum used three times (`ac-0`). (v) `ab-8`'s widths 690 and 210 are 687 and 206, and its "excluded" holds in one cost model only (`ac-2`).

## 2. Neighbour sums on the cube

| points | least found, rationals | per point | least possible, adding-only | modulo 2 | odd primes |
|---|---|---|---|---|---|
| 16 | 32 | 2 | 32 | 30 found; one half costs exactly 15 (16 adding-only) | one half: none with 14 modulo 3, none with 13 modulo 5 |
| 32 | 96 | 3 | 96 | no data | no data |
| 64 | 224 | 3.5 | 224 | 216 found | no data |

All found circuits are the *pairing* circuit: add the inputs in pairs of directions, each pair serving two outputs [computed, replayed for k = 2 to 8 by `ab-0` and `ac-0`; formula mine]. The route through two transforms costs 120, 288, 672 at 16, 32, 64 points [mine], far above.

- **Adding-only law** [argued, `ab-0`; read line by line and extended to positive scalings by `ac-0`; exhaustive for one half at 16 points: 16 yes, 15 no]. Two addresses share at most two neighbours, so a gate serves at most two outputs. The order N·k without cancellation is classical (Nechiporuk 1969) [read, `ac-0`]; the constant 3/4 was not found in print.
- **Does cancellation save a gate? Once, modulo 2** [computed twice with two programs]. 15 gates for one half at 16 points; 14 is impossible there. The reason is special to the number 2: the outputs at the four neighbours of any address add to 0 modulo 2. The wiring has no version over the rationals for any coefficients [argued; all 4^15 choices modulo 3 fail, computed]. Carried to large sizes it gives N·(23k/32 − 1) against N·(24k/32 − 1), modulo 2 only (1,216 against 1,280 at 256 points): the same order.
- **Does a coefficient save a gate? No, in anything searched** [computed]. Over the rationals no circuit below pairing at any size. Exhaustive searches modulo small odd primes found nothing below pairing at 4, 8 and 16 points (the 16-point half costs 15 or 16 modulo 3; the 8-point figure is read from wave 1). There is no evidence at all at 32 or 64 points: the exhaustive tool stops at 16 and the random search failed its own control.
- **Why this is not an easier test than the transform** [argued, `ab-0`, corrected once by its author]. In circuits that do the same thing at every address, the only way below k − 1 full layers is a wire that takes one value on a whole flat, and such wires are a transform on part of the bits. Neighbour sums fall below adding-only only if a transform runs under about 9/16 of the textbook rate; the night's best is 3/4. Neighbour sums need exactly ceil(k/2) coset sums [argued, `ab-3`, `aa-cross`, read by `ac-2`; computed to k = 8].

**For linear size:** everything measured grows like k per point; nothing grows like log k or stays bounded. That is not a floor for general circuits. Wave 7 guessed the answer would be visible by 64 points. It is not: no tool reaches 32.

## 3. The bar of 1e-1 by the engine's own mechanism

One formula, the engine's price law, gives every figure; the studies differ only in which costs they set to zero [computed, `ab-8`; re-coded by `ac-2`]. Floats throughout. An *idle block* is a block of catch-up moves outside the exchange (the published units have two per array); a *merged word* has none, and nobody has built one.

| saving | what it is | what it assumes | status |
|---|---|---|---|
| 8.7625e-4 | the published unit | nothing | Lean; ports of 1 direction in 9, five stages, 6.5 helpers per pair, 16.5 blocks per array |
| 2.8e-3 to 8.2e-3 | the same unit, fewer helpers, cheaper totals | helper floors argued by one agent; totals at 55 moves instead of 72 | what-if |
| 1.7e-2 to 2.5e-2 | "fat" ports, 3 directions in 6 (earlier study) | a floor with no family behind it | in the stricter model the saving is 0: each port knows exactly one other |
| 0.078, 0.120, 0.147 | ports of half the stage: five stages, three stages, merged word | totals free, no helpers | dead: kappa ≤ 2 at r = h/2 |
| 0 to 0.019 (0.024) | six classes up to width 9, totals at their least exact count | no helpers; a word nobody has built | [computed] |
| at most 0.045 (0.055 merged) | every class up to width 9, by the order bound | each total costs h moves; a term is removed only if fully known; no helpers | [computed twice] |
| 0.058, 0.077, 0.090, 0.098, 0.105, 0.113 | widths 12, 20, 32, 48, 80, 200 | the same, and that the bound is reached | a ceiling on a what-if; tends to 0.1198 |
| 0.0466; 0.158; 0.235 | block sizes 4, 5, 6 with no address maps and no phase letters | a linear programme; exact at size 4 | ceilings only; the one named pattern that meets them is excluded at sizes 4 and 5 by the pair rule |
| 0.119; 0.204 | `ab-6`'s plain exchange and three-array word, ports of a third of the stage | additions and helpers free | 0.204 becomes 0.120 if each addition step pays h/15 moves |

- **The gap between 2.5e-2 and 0.12 is carried by free totals, almost alone** [computed]. One total serves at most about 1 + 2^(h − 2r) arrays, and large ports use up exactly that surplus h − 2r. First width not excluded: (h, r) = (55, 24); (23, 9) with a merged word nobody has; 687 with two idle blocks as published; never with the published five-stage shape [computed twice]. Helpers decide on their own: above 0.51 helper arrays per pair 1e-1 is out at every width; the published unit has 6.5.
- **How much it leans on the cost model** [computed, `ac-2`]. If a total costs r moves instead of h the exclusion up to width 9 survives (at most 0.081). It fails if a total can cost under about 0.4·h moves with ports above half the stage, or if a term may be removed when only partly known. The second was not tested.
- **Fewer blocks (`ab-1`): no legal network, only counts.** Without address maps and phase letters every array has at least 2 blocks at every block size [argued], and at least 15/4 moves at block size 4 [computed, exact]. The *pair rule* [argued; `ac-2` checked the algebra and the counts 105 of 105 and 465 of 465] removes the one pattern above the bar. Removing unwanted terms with one more block is exactly zero-sum.
- **Chain of exchanges (`ab-6`): legal words, no unit.** Every word replayed uses more moves than the plain schedule (12 against 8, 20 against 12, 52 against 36) [computed]. A ring of arrays is legal and shares stages (2R + 1 stages for R rounds instead of 3R), but adds a block to every array per round, and the price law charges blocks: 0.119, 0.105, 0.095, 0.082, 0.068 for 1, 2, 3, 5, 10 rounds [floats, what-if].

**Plain answer.** Excluded at every stage width up to 9, inside one cost model. Above that it is open on paper only: this particular bound stops biting, which is not a lead. It is not searchable: the first open classes have more than 2^120 labels. Six things are needed at once and nothing computed tonight supports any of them.

## 4. The ideas that are alive

**A. The rate per block of the published unit.** It is the only object where the one-for-one rate fails, and the reason is special to the transform (ports). Nobody has looked at which of its blocks buy the 0.006. If a few do, their rate alone is the number to set against 0.63 at block size 45. *Next:* 1. This is about 1e-1, not linear size.

**B. All line sums of a finite plane.** Cut the address in two halves and read it as a point of a plane with √N points per line. If the N + √N sums over all lines cost O(N) gates, the transform costs N·log log N [argued in wave 1, `d-1`; replayed at 16, 64, 256 points by `aa-cross`]. With additions only they cost exactly 60, 504, 4,080 [mine]; modulo 2 the matrix has rank only 9, 27, 81. Nobody has priced it with free coefficients. *Next:* 2.

**C. Deliveries that share their cost.** A *delivery* is a gate in which a whole half cancels and hands a value to the other half. One delivery is worth about log2 n gates and cost exactly what it saved at 8 points. A circuit below Yates' count needs many whose costs overlap. 16 points is the first size open in the literature for subset sums [read, `ab-5`]. *Next:* 3.

**D. Straightening the quadric.** The transform equals a cheap convolution (under 2N gates) seen through a change of frame built from one permutation of the outputs; it has linear size exactly when one such change of frame has [argued; identity checked at 16 and 64 points]. The search space is permutations. The structured ones priced so far cost about N^1.5 [argued, rough]. *Next:* 4.

**E. How many coset sums make the transform.** Exactly 2 and 4 at 4 and 16 points; between k/2 and 2^(k/2) in general [computed + argued]. *Next:* 5. [guessed: exponential, ending in a statement]

**F. The engine's two hatches.** Terms removed when only partly known; totals that cost fewer than r moves (`ac-2`). And one small exact run nobody has done: add the pair rule to `ab-1`'s linear programme and solve again.

**G. Anomalies kept.** Four savings exist modulo 2 and die over the rationals (*next:* 8). Constants that are not rational: still no experiment.

## 5. The walls, as lemmas

All [argued] unless marked. Numbers continue `WAVE7-NOTE.md`.

- **L1 + L2. Costs add, now "repay".** A wire or call that serves two uses pays for the removal of the foreign part at least what the sharing saved. Waves 1 to 7: `d-0`, `d-2`, `d-3`, `d-4`, `d-6`, `d-7`, `e-3`, `e-6`, `e-7`, `e2-1`, `e2-2`, `j-manyatonce`, `g-0`, `g-2`, `g-5`, `g-6`, `g-7`, `h-2`, `n-2`, `p-2`, `p-5`, `u-4`, `u-8`, `s-cross`, `v-2`, `x-3`, `x-4`, `x-5`, `x-7`, `w-cross`, `z-2`. Wave 8: `ab-6` (leak lemma: 7 calls at K = 4, 2K − 2 from K = 8; `ac-1` agrees), `ab-1`, `ab-4`, `ab-5`, `ab-2`. Its last named room is closed. Not one for one: the published unit, and three matrices that are not the transform.
- **L4. Height.** Wires of height at most M cost about N·log2 N / (4 + 4·log2 M) gates. Waves 1 to 7: `d-5`, `e-5`, `e2-0`, `j-failproof`, `g-1`, `g-3`, `g-4`, `g-5`, `h-1`, `n-0`, `p-5`, `p-8`, `u-6`, `s-cross`, `v-2`, `x-0`, `x-2`, `x-3`, `x-5`, `x-8`, `x-9`, `z-0`. Wave 8: `ab-2`, `ab-7`. It forces nothing above 0.316·N·log2 N gates, and the best known rate is 0.75. No best-count circuit holds a tall wire.
- **L5. One class of kernels.** Every saving tested is shared by all transforms built from a 2 × 2 block. `d-0`, `a-0`, `g-3`, `g-4`, `g-5`, `k-cross`, `h-6`, `p-0`, `r-2`, `x-1`, `x-3`. Two more in wave 8: `ab-4`'s tilted-cut bound, `ab-5`'s "low rank plus sparse".
- **L16. Distance, now "bent".** The transform's sign pattern is constant on no flat of dimension above k/2; the same holds for neighbour sums seen in the frame of the outputs. Waves 2 to 7: `j-cross`, `x-9`, `x-2`, `x-1`, `x-7`, `x-4`, `x-8`. Wave 8: `ab-3`, `ab-0`, `ab-7`, `ab-2`, `aa-cross`. Now blind to height and to the choice of group.
- **L17. Flag passes** stand (`x-4`, `z-2`). **L20. Layers** (new as a lemma; wave 2's "commuting steps"). A program whose stages are convolutions, or the same gate at every address, needs k/2 stages at N/2 gates or more each. `d-1`, `j-cross`, `ab-0`, `ab-3`. Hatches: gates not repeated at every address; stages that are not convolutions.
- **L19. Ports**, restated (`x-6`, `z-1`, the floor note). Three ceilings: *width* (`ab-8`, `ac-2`), *two blocks* without address maps and phase letters (`ab-1`), *a block per round* (`ab-6`). "Three blocks per exchange" is withdrawn.
- **L21. Sharing in adding-only circuits** (new). Neighbour sums: exactly N·(k − 1 − floor(k/2)/2). `z-2`, `ab-0`, `ac-0`. Subset sums: (N/2)·log2 N [read: Find and Boyar 2013], widened to circuits with no return (`ab-4`, unreviewed).
- **L6, L7, L10, L12, L13, L14, L15, L18:** not touched in wave 8.

Each wall fences one shape of program. None bounds a general circuit in count (G) or (O).

## 6. The next eight experiments

Running in the ninth wave as this is written.

1. `rate-per-block`: from the published certificates, which classes of blocks carry the saving, in moves per extra block, against the bar 0.63.
2. `line-sums`: least gates for all line sums of the plane at 16 and 64 points with free coefficients; gates per point against (1/2)·log2 N.
3. `two-deliveries`: subset sums at 16 points modulo 2 in 31 gates, with two cancelling gates whose costs overlap.
4. `straighten-the-quadric`: carriers built from j local exchanges; does j grow more slowly than k/2?
5. `flat-rank-of-the-transform`: the value at 64 points (8 or fewer?), and the growth law.
6. `which-bent-function`: price three other flat sign patterns at 256 points; is the quadric the dearest or one of many?
7. `two-helpers`: least number of classes for two partitions that carry every polynomial of degree 2 (8 at 8 points; 13 or 14 at 16).
8. (silly) `modulo-4`: does the 15-gate circuit survive modulo 4 and 8, and if not, which gate dies?

## 7. What this says about linear size

Nothing found in eight waves gives linear size or moves the exponent, and the wave that was to test linear size on its simplest necessary case found the same growth, k per point, with no cancellation that pays over the rationals [computed at 4 to 16 points; argued for adding-only and for same-at-every-address circuits; no evidence at 32 points or more]. Nothing forbids it either: every wall fences a class, the sharing rate of exactly one for one is argued in five classes and for no general circuit, and what no wall covers is a circuit with gates not repeated at every address, deliveries whose costs overlap, and stages that are not convolutions, all at once [argued; the list is `aa-cross`'s reading]. In the published mechanism's price law linear size would need one block per array, which the floor note argues cannot occur [read]; its road to 1e-1 is open on paper only; the one relation now on the table whose success would change the order is the line sums of a finite plane in O(N) gates, which would give N·log log N and which nobody has priced [argued].
