# WAVE9-PICKS: eight briefs, one per experiment of aa-cross section 6

11 October 2026, curator ae-pick, 15-minute box. Private research: publish nothing, no git, no Lean. Not ranked by odds.
Read for this: aa-cross.md in full; d-1.md in full; the summaries of ab-0, ab-1, ab-3, ab-5, ab-8, x-6; the outputs in
`aa-cross/`; `x-6-unitasbox/zlaw.py` and `zlaw.out`. I did not read ab-2, ab-4, ab-6, ab-7 beyond a few lines.
Marks: [read] = in a file I opened; [ran] = run by the named agent, not by me (I ran nothing); [derived] = arithmetic of
mine in this box, checked by nobody; [recalled] = from memory; [guess].
All paths are under `waves/` unless they start with R
(R = `(not in this repository) wht-power-saving-r4-candidate`, read only).

**The bar.** The user cares only about a saving of 1e-1 or more (O(n (log n)^0.9) or better) or linear size. Constants
at one size are of no interest. Every brief must end with a growth law in N, or say that it has none.
**The one experiment whose success would pass the bar is brief 2 (line-sums).** Brief 1 (rate-per-block) bears on the
bar directly: it says whether 1e-1 is alive in the published mechanism.

Common words. N = 2^k points; an *address* is k bits; x.y = number of common ones modulo 2; *weight* = number of ones.
*The transform* H: entries (-1)^(x.y). T(N) = least gates for H, relabellings of inputs and outputs and scalings free.
*Textbook*: N log2 N gates. Gate counts: **(G)** a gate is any a*u + b*v, scalings free; **(O)** OpenAI's, additions and
scalar multiplications each charged. Every brief below uses (G) unless it says moves and blocks.
*Convolution with g*: output(y) = sum over x of g(x + y) input(x), addresses added bit by bit modulo 2; g is its
*kernel*; its *spectrum* is H g (in the frame of the outputs the convolution is a diagonal with these entries).
*Flat*: a subspace of the address space or a shifted copy of one. *Coset sum* along a subspace V: every address gets the
sum of the inputs over its shifted copy of V (N - N/|V| gates; it is the convolution with the indicator of V).
*Quadric signs*: the function that is -1 where y1 y2 + y3 y4 + ... = 1 and +1 elsewhere. For even k the transform is,
up to free signs and one free relabelling, the convolution with quadric signs, and its spectrum is quadric signs again.
Night's counts (G) used below: 7, 19 (or 20 in the family), 52, 128, 304 gates at 4, 8, 16, 32, 64 points.

---

## 1. rate-per-block  (bears on the bar of 1e-1; engine's accounting, no search)

**Idea.** The published program is priced by a law that counts interruptions, not moves. An *array* is one working copy
of the data; a *move* is one direction of the transform applied to one whole array; a *block* is a run of moves on one
array with no addition in between, and its *rank* is its number of moves; m is the number of moves every array is owed
(the block width). **Price law** [read: zlaw.py; R/tools/gen/foldlib.py]: z is the root of
"sum over all blocks of (rank/m)^z = W", W the number of arrays; the saving is e = 1 - z. The plain schedule has 2
blocks per array (ranks m - 1 and 1) and saves nothing. aa-cross hybrid 3 solved the law for the shape "one big block of
rank m - s - d and s blocks of rank 1 per array" (d = moves saved per array): to first order
**d/s = m^e/(1 - e) - 1**, the moves that every extra block must buy. For e = 0.1: 0.28, 0.38, 0.63, 0.78 at
m = 4, 9, 45, 110 (exact roots 0.254, 0.373, 0.623, 0.776 at s = 1) [ran: `aa-cross/h3_rate.out`, floats]. The published
unit has 44.905 moves and 16.49 blocks per array at m = 45, so d = 0.095 and d/s is about 0.006 [ran: `zlaw.out`].
Nobody has asked how that 0.006 is distributed over the kinds of block.

**Words.** *Unit*: the published network; certificate 1 has h = 9, v = 120 pairs, R = 783 helper arrays, W = 1,263,
m = 45; certificate 2 has h = 22, v = 1,320, R = 9,412, W = 14,692, m = 110. *Classes of blocks* as the certificate
stores them [read: zlaw.py]: x and y (data arrays: sources and targets), s (helpers), c (scratch copies), plus four idle
block sizes that zlaw.py hard-codes. *Legal unit*: one with a network behind it that the engine's checker accepts.
*What-if*: a block list with no network. *Rate of a class*: moves saved per block of that class.

**Start from.** `R/tools/certificate/gcert1-e8-r783.json.gz` and `gcert1-p11-pr193.json.gz`;
`x-6-unitasbox/zlaw.py` (takes the two paths, reproduces 8.7625e-4 and 7.4745e-4); `aa-cross/h3_rate.py`;
`ab-6-chainexchanges/ring.py` and `bystander_price.py`; `ab-8-reconcilecaps/price.py`. Other block lists that may be
legal units: `R/tools/e8/data/others/` (I saw the names only).

**First experiment.** For each certificate print, per class: number of blocks, their ranks, moves. Then for each class
two attributions, both labelled: (a) marginal, a what-if: delete the class or merge it into its neighbours, recompute the
root and the moves per array (zlaw.out already has three such rows: no copies 3.5071e-3, no copies and no helpers
1.3105e-2, one whole block per invocation 1.5758e-2); (b) accounting on the legal unit itself: against the plain
schedule, which blocks are shorter than they would be, and how many extra blocks each class adds. Print
rate = moves saved / blocks for each class and for the unit, next to the bar m^e/(1 - e) - 1 at the same m. Do the same
for ab-6's bystander word and ab-1's (m - 1 - d, 1) shape, marked WHAT-IF.

**What it could reveal.** Whether the saving sits in a few blocks at a high rate (then those blocks are the object to
enlarge, and the distance to the bar is their rate against 0.63) or is overhead all the way down. Linear size in this
law means one block per array; no rate reaches it.

**You must end with one sentence:** is any class of blocks of a LEGAL unit above 0.1 of a move per block, and what rate
the bar of 1e-1 needs at that width. Keep "legal" and "what-if" apart in every line.

**Question to keep asking.** Which interruption of an array buys the most, and what would it take to have only that kind?

---

## 2. line-sums  (THE ONE EXPERIMENT OF THIS WAVE WHOSE SUCCESS WOULD PASS THE BAR)

**Idea.** The transform at N points reduces to "all line sums of a finite plane" plus small transforms, and nobody has
priced the line sums with free coefficients. If they cost O(N), the transform costs O(N log log N).

**Exact definitions.** N = q^2, q = 2^j, k = 2j. Read an address as a pair (a, b) of elements of the field with q
elements, written in bits. A *spread* is a family of q + 1 subspaces S_0, ..., S_q of j address bits each that together
cover every address and meet pairwise only in 0 (the q + 1 lines through 0 of the plane: (a, c a) for each c, and
(0, b)). V_i = the perpendicular of S_i for the bit dot product; it also has j bits. **The line sums**: for every i and
every shifted copy c + V_i of V_i, L_i(c) = sum of the inputs over c + V_i. There are (q + 1) q = N + q of them, each
over q points, and two of these point sets share at most one point (they are the lines of an affine plane of order q).
R(N) = least gates (G) for all N + q line sums (d-1 writes Rad(q)).
**The slice identity** [read: d-1 section 2; ran at 16, 64, 256 points on every output: `aa-cross/h4_spread.out`]: for an
output address y in S_i the sign (-1)^(x.y) is the same for all x in one copy of V_i, so
(H input)(y) = sum over the q copies c + V_i of (-1)^(c.y) L_i(c): **the transform at the q outputs in S_i is the
q-point transform of the i-th family of line sums.** Every output lies in some S_i, hence
**T(N) <= R(N) + (q + 1) T(q)**, and conversely R(N) <= T(N) + (q + 1) T(q) [read: d-1 section 4].
If R(N) <= beta N at every size, gates per point are at most about beta log2 log2 N (9.4 against 256 at N = 2^256 for
beta = 1) [ran: h4_spread.out]. [derived, mine] The bar needs less than linear R: R(N) = O(N (log2 N)^0.9) already gives
T(N) = O(N (log2 N)^0.9), because the recursion halves log N at each level and the sum is geometric.
Second relation, for j even [ran at 16 points only, `aa-cross/h4_ruling.out`; beyond that recalled]: the +1 set of
quadric signs is the union of q/2 + 1 subspaces of a spread, so T(N) <= 2 R_half(N) + O(N), with R_half the line sums
along those directions only and no small transforms. Check it at 256 points first (9 subspaces of 4 bits).

**Known counts** (G):

| N | q | adding-only (exact: no two lines share two points) | through the transform, T(N) + (q+1) T(q) | floor: N + q distinct outputs | (1/2) log2 N per point |
|---|---|---|---|---|---|
| 16 | 4 | 60 (3.75 per point) | 87 = 52 + 5 x 7 (5.44) | 20 | 2 |
| 64 | 8 | 504 (7.88) | 475 = 304 + 9 x 19 (7.42) | 72 | 3 |
| 256 | 16 | 4080 (15.94) | d-1 printed 2744 with older counts; 2484 = 1600 + 17 x 52 if the pieces family continues [derived, mine: its five counts fit (3/4) N log2 N + N/4; not replayed] (9.70) | 272 | 4 |

Adding-only is (N + q)(q - 1), about N^1.5 [read: aa-cross fact D]. The rank of the line-sum matrix is 16, 64, 256 over
the rationals and modulo 3, but 9, 27, 81 modulo 2 (3^(k/2), about N^0.79) [ran: h4_spread.out].
[derived, mine] At 16 points this route cannot beat 52 (20 + 35 = 55), so no record is at stake there: only the way
gates per point move from 16 to 64 to 256 matters.
**Warning to carry** [read: d-1 section 7, derived there]: with coefficients of bounded size R needs about
(N/4) log2 N gates (determinant argument: det(R^T R) = q^(N-1)(q + N)). A linear R must use coefficients that grow.

**Start from.** `d-1.md`, `d-1-plane/plane.py` (the cyclic form: the N - 1 lines missing the origin are the cyclic
shifts of one set D of q logarithms, D = {1, 2, 4, 8} modulo 15 at 16 points; on the 8 "mixed" dimensions the operator
satisfies D^2 - D + 4 = 0), `aa-cross/h4_spread.py`, `h4_ruling.py`; searches: `d-0-zeta/mincirc` (exhaustive modulo p:
`mincirc p n m rowsfile`), annealers `j-machine/steiner.py`, `slp.py`, `relax.py` (the tasks must be added).

**First experiment.** 16 points: the 20 x 16 matrix; decide 59 and below with the annealers over the rationals (large
and small coefficients in the pool on purpose) and exhaustively modulo 2 and 3 (a circuit modulo p is a candidate until
lifted and replayed exactly; "none modulo p" is not "none"). Then 64 points by annealer and by structure (the tower law
of d-1 section 2: the mask is a product of masks one level down). Then the circuit over the two-element field suggested
by the rank 3^(k/2): about N^0.79 log N gates, and what stops it lifting.

**Required output.** Gates per point at 16, 64 and, by any construction, 256 points, each with the LARGEST COEFFICIENT
USED, next to the three reference columns above; and one line: does gates per point grow like q, like log N, or more
slowly.

**Question to keep asking.** Subtraction provably pays here (4080 against at most 2744 at 256 points) but so far only
through the transform itself: is there any way to get a line sum from other line sums and a few large multiples that
does not pass through a transform?

---

## 3. two-deliveries  (subset sums at 16 points over the two-element field)

**Idea.** *Subset sums* Z: the output at a set S is the sum of the inputs at all subsets of S. *Yates*: (N/2) log2 N
gates (32 at 16 points). Cut the cube along one bit into a lower and an upper half. A *delivery* (ab-5), the same gate
as ab-4's *return*: a gate in which the whole upper half cancels, so that a form of the lower half is handed over
ready-made. The *mixed part*: the gates between wires that both contain upper inputs. The *cut lemma* [read: ab-5 line
5]: in every cut, gates = (mixed gates, at least the cost of the half) + (at least N/2 injections) + (pure lower gates);
a circuit below Yates needs, in every cut, a delivery worth more than it costs. One delivery was measured to tie
(8 points) and to cost at least 2 in six skeletons at 16 points. d(k) = least extra gates the mixed part needs so that
one cancelling gate delivers the total of the lower half; the delivery is worth k - 2 net; d(3) = 1 [ran: ab-5].
[derived: aa-cross fact A] Single deliveries can never change the order; the order needs about half a node's size in
deliveries whose costs overlap. Nobody has built two that share.

**Start from.** `ab-5.md` sections 5 and 7; `ab-5-cancellit/mincirc_free.c` (exhaustive modulo p with free start forms
in its fifth argument), `freeform8.out` (what each of 247 free forms saves at 8 points: 0, 1, 2 or 3), `skel16*.py`;
`ab-4.md` section 3b ("no return").

**First experiment.** (i) The census for PAIRS of free forms at 8 points (about 30,000 runs of 0.1 s): is the saving of
a pair ever more than the sum of the two? (ii) 31 gates at 16 points over the two-element field with the cut lemma as a
filter in all four cuts and TWO cancelling gates whose mixed parts overlap; report d(4), or a 31-gate circuit (16 points
is the first size open in print [read: ab-5 line 3]).

**Growth law it could reveal.** d(k) < k - 2 at some k puts subset sums below Yates; deliveries whose costs overlap at
a rate that grows with the node are the only route here to a change of order. A proof of d(k) >= k - 2 with a reason is
most of a proof that one delivery never pays. Two-element field only: say so in every line.

**Question to keep asking.** Is the second delivery ever cheaper because the first is there?

---

## 4. straighten-the-quadric  (nobody has tried)

**Idea.** In the frame of the outputs a convolution is a diagonal, and a permutation pi of the outputs carries one
convolution into another. Take sigma = quadric signs (the transform's spectrum) and sigma' = -1 exactly on
(a hyperplane minus a subspace of k/2 - 1 bits): both have the same number of -1 (6 at 16 points, 28 at 64). The
convolution with spectrum sigma' costs under 2N gates (30 and 124) [ran: `aa-cross/h2_specperm.out`]. For every pi with
sigma(pi(y)) = sigma'(y), the *conjugator* Phi = H P_pi H / N satisfies C_quadric = Phi C_sigma' Phi^T, so
T(N) <= 2 cost(Phi) + 2N and cost(Phi) <= 2 T(N): the transform is linear exactly when some conjugator is [derived
there]. An *exchange*: the permutation that swaps y with y + u for y in a set S and fixes the rest; it costs one
convolution plus N, and about (c + 1) N gates when S is a union of at most c flats [derived there, not built].

**Start from.** `aa-cross/h2_specperm.py` (both patterns and the entry-by-entry check; its random walk is weak, do not
reuse it as evidence).

**First experiment.** Exact, 16 points: breadth-first over products of j exchanges with S a union of at most c flats
(c = 1, 2, 3); the least j for which the image of sigma' is the -1 set of some non-degenerate quadric (any of them will
do: relabellings are free). Then 64 points. Report j(k, c).

**Growth law.** j = k/2 ties the textbook. j growing more slowly than k (log k, or bounded) with bounded c is a growth
law below N log N; bounded j and c is linear size. A piecewise affine pi needs at least sqrt(N)/2 pieces [derived
there], so the exchanges must not be affine on few pieces.

**Question to keep asking.** What is the fewest "swap along one direction on a simple set" steps that bend a hyperplane
into a quadric, and why would it have to be k/2?

---

## 5. flat-rank-of-the-transform  (nobody has tried)

**Idea.** *Flat rank* of a kernel g: the least number of flat indicators whose combination (any coefficients) is g.
Each term is one coset sum, under N gates, so T(N) <= 2N x (flat rank of quadric signs). Known [read: aa-cross hybrid
4]: flat rank >= k - D, with D the largest dimension of a flat on which the spectrum is constant; for quadric signs
D = k/2, so the bound is k/2; an upper bound of order 2^(k/2); more than 3 at 16 points [ran: `aa-cross/h5_flatrank.out`].
Nobody has asked how it grows. Linear growth in k ties the textbook; anything slower is a growth law; bounded is linear
size (the bound k/2 excludes that for plain flats of the address space, so the interesting step is the wider class
below).
**Fix one definition first** [derived, mine]: ab-0 allows *signed* flats (+1 or -1 on the flat by a sign (-1)^(a.z));
`h5_flatrank.py` enumerates 51 and 307 flats at k = 3, 4, which is the number of unsigned ones. With signs, 16 points
has 4 (one signed flat per value of half the bits); without signs aa-cross's ruling gives 5
(quadric signs(z) = -1 + 2 x (three planes) - 4 [z = 0]). Report both.

**Start from.** `aa-cross/h5_flatrank.py` (enumerates all flats, exact fractions), `ab-0-neighboursums/flat3.c` and
`flatrank.py`, `ab-3.md` line 6 (the level-set-flats theorem), `aa-cross/h4_ruling.py`.

**First experiment.** Decide 4 at 16 points (signed and unsigned); the value at 64 points (at most 8). Then widen the
class: flats of the DOUBLED address space (x, y) of 2k bits, whose indicators are N x N 0/1 matrices; this class
contains the convolution flats and k-cross's *rectangles* (the transform as a sum of 5, 13, 49 of them at 4, 8, 16
points). Least number of such flats for H at 4, 8, 16 points, and the price of each in gates.

**Growth law.** The function r(k), or a proof that it is exponential (ab-8's random-order argument is the suggested
tool).

**Question to keep asking.** Is the transform a short sum of cheap pieces in ANY family of pieces, and which family
makes k/2 fail?

---

## 6. which-bent-function  (nobody has tried)

**Idea.** A *bent pattern* is a function g with values +1 and -1 on the addresses whose spectrum H g has every entry of
the same size sqrt N (k even). The convolution with g, divided by sqrt N, is then an orthogonal matrix, "as flat as the
transform". Quadric signs are one bent pattern; there are others that are not quadrics [recalled by aa-cross for k >= 8;
recalled by me: cubic ones already exist at k = 6, Rothaus's four classes; check a source before using it]. Two
families [recalled]: *partial-spread patterns* (-1 on the union of q/2 subspaces of a spread without 0, or +1 on
q/2 + 1 of them, q = sqrt N) and patterns g(x, y) = (-1)^(x . p(y)) with p a permutation of the half-addresses (p
linear gives a quadric; p not linear does not). Every wall of the night (BENT, LAYERS) was stated for the quadric.
Is the quadric the cheapest of its family, the dearest, or typical?

**Start from.** `aa-cross/h4_ruling.py` and `h4_spread.py` (spreads at 16, 64, 256 points), `j-machine/tower.py`
("H = 1 c^T - 2E with c a bent centre"), `aa-cross/h2_specperm.py` (two bent patterns of the same type are conjugate by
a permutation of the outputs, brief 4). For a partial-spread pattern the convolution is
(multiple of all-ones) + 2 x (sum of the chosen families of line sums, spread back) + (multiple of the identity), so
its cost is at most the line sums along half the directions plus O(N): brief 2's R_half with ANY spread, including the
spreads that do not come from a field (they exist at 256 points [recalled]).

**First experiment.** Price three bent convolutions at 256 points (one quadric, one partial-spread pattern that is not a
quadric, one with p not linear, for example p(y) = y^3 or 1/y in the field with 16 elements) by the night's
constructions and by fact D; before that, the same at 64 points with a cubic bent pattern if the recalled fact holds,
where annealers can still run. Report gates per point for each and the largest coefficient.

**Growth law.** If one bent convolution has a construction whose gates per point grow more slowly than k, find what the
quadric lacks and whether a cheap conjugator (brief 4) carries it to the transform. If all tie, BENT is a wall for the
whole family and can be attacked as one statement.

**Question to keep asking.** Which property of the quadric did each wall really use: being bent, or being quadratic?

---

## 7. two-helpers  (one hybrid; note its ceiling)

**Idea.** ab-3 asked: can every polynomial of degree at most d in the address bits be written as (a function of a coarse
label 1) + (a function of a coarse label 2), with far fewer than N labels of each kind? Then such a polynomial costs
N + o(N) gates at all points. aa-cross hybrid 1 made it a picture: the two labels are two partitions P1, P2 of the N
cube points; draw the graph whose vertices are the classes of both and whose edges are the cube points (a point joins
its class in P1 to its class in P2). **Criterion** [derived there]: a function is "label 1 part + label 2 part" exactly
when its alternating sum around every cycle of the graph is 0. So the question is whether every cycle lies in the span
of the *characters* (the functions (-1)^(a.x)) of weight above d. V(k) = least total number of classes for d = 2.
Known [ran: `aa-cross/h1_graph.out`]: V(3) = 8; V(4) is 13 or 14 (12 is excluded; a hand proof against 13 was refuted by
its author's own run); a family with 3N/4 + 2 classes for every k (P1 forgets bit 1; P2 keeps only bit 2 where bit 1 is
0 and forgets bit 2 where bit 1 is 1), exact to 64 points.
**Ceiling to state in the report** [derived there from a recalled bound]: from degree about log2 k on, the classes
number at least about 2N/3, so this atom alone gives at best N log N / log log N: not a saving exponent, off the bar
unless it combines with something else.

**Start from.** `aa-cross/h1_graph.py` (the exact test for any pair of partitions), `h1_support.py`; ab-3.md lines 270
to 295.

**First experiment.** Decide V(4) exactly (a whole-number programme, or exhaustive over partitions into subcubes; the
random walk failed its control, so do not use it). Then V(5), V(6); report V(k)/N. Then try to label the flags of a
generalised quadrangle (a graph with no short cycles and N^(3/4) vertices) by cube points.

**Growth law.** V(k) = o(N) for degree 2 would be a new cheap atom (degree-2 polynomials at N + o(N) gates); V(k)/N
bounded below says the atom is a constant-factor object. Say which, and what it would have to combine with.

**Question to keep asking.** Does the ratio V(k)/N fall with k, and what does the best graph look like?

---

## 8. modulo 4  (the one that sounds silly)

**Idea.** A circuit modulo 4 is not a circuit. But four savings of the night exist in arithmetic modulo 2 and die over
the rationals: ab-0's 15 gates for one block of neighbour sums at 16 points (adding-only needs 16; *neighbour sums*:
every address gets the sum of the inputs at its k neighbours; a *block* is the half of the matrix from even-weight
inputs to odd-weight outputs, 8 x 8); ab-7's row that equals the cube modulo 2 only; ab-5's "subset sums have order 3";
the line sums' rank N^0.79 (brief 2). Nobody has looked between modulo 2 and the rationals. If a saving survives
modulo 4, 8, 16, ... for ever, there is a circuit over the 2-adic numbers, hence one with algebraic coefficients
[derived: aa-cross section 6]. If it dies at 4, the gate that dies names the obstruction.

**Start from.** `ab-0-neighboursums/B4_p2_m7_top_d2.out` (the 15-gate circuit modulo 2), `verify15.py` (replay, and the
argument that this wiring has no rational lift), `mincirc_top.c` and `d-0-zeta/mincirc.c` (exhaustive over a field: a
new small tool is needed for the whole numbers modulo 4 and 8, coefficients 1, 2, 3, where 2 is not invertible; say how
scalings by 2 are treated in the count), `rows_B4.txt`.

**First experiment.** Least gates for ab-0's 16-point block over the whole numbers modulo 4, then modulo 8. First with
the wiring of the 15-gate circuit fixed (coefficients only: a small exhaustive lift, each digit a linear system over the
two-element field), then with free wiring. Record which gate fails at 4 if one does. The same lifting test on the
line-sum matrix at 16 points if time remains.

**Growth law.** None by itself at one size. What it could reveal is a class of circuits (2-adic or algebraic
coefficients) in which the modulo-2 ranks N^0.79 and "rank 4 where the rationals have 5" survive; x-1's price list says
each further binary digit costs 2N for the transform, so the number to report is how many digits a saving survives and
what each digit costs.

**Question to keep asking.** Is the modulo-2 saving an accident of the number 2, or the first digit of something?

---

## Notes of the curator

- [derived, mine] "Through the transform 87 and 475" in aa-cross is T(N) + (q + 1) T(q) with the night's counts
  (52 and 7; 304 and 19). I checked the arithmetic, not the circuits.
- [derived, mine] Since R and T bound each other, R(N) = O(N (log N)^c) and T(N) = O(N (log N)^c) are the same statement
  for c < 1. So brief 2 is not an easier problem; its value is a matrix with a different shape (lines that meet once,
  rank N^0.79 modulo 2, a cyclic form) on which nobody has run a search with free coefficients.
- Briefs 4, 5 and 7 are reformulations by their author's own account; brief 7 carries its own ceiling. I kept them
  because the task is one brief per experiment, and I did not rank.
- Skeptics' files ac-*.md and WAVE8-NOTE.md had not landed when I wrote this.
