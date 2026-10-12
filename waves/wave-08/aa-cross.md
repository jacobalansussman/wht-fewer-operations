# aa-cross: the eight waves side by side, four hybrids tried, and what to ask next

> Editor's note (11 October 2026): a later report corrected one figure. The "0.006" of a move per block that this report quotes for the published unit is a rate of the data arrays diluted 22 to 29 times ([ad-0](../wave-09/ad-0.md); line 10 (vi), "Corrections by the critics", in [the ninth note](../wave-09/NOTE.md)).

11 October 2026, 05:52 to about 06:30 EDT, 40-minute box. Private. One agent; nothing reviewed, nothing in Lean, nothing published.
Marks: [ran] = run of mine tonight (files in `aa-cross/`; whole numbers or fractions unless a line says floats or "modulo p");
[derived] = by hand tonight, checked by nobody; [read] = from tonight's reports; [recalled] = from memory, no source read; [guess].
Gate count everywhere: **(G)**, a gate is any a*u + b*v, scalings free. Count (O), OpenAI's, is not used.
Read: w-cross in full; the wall statements of j-cross and the headings of k-cross; the top of WAVE7-NOTE; the nine wave-8
results as handed to me; forty lines of ab-3 and thirty of d-1. I did not read the wave-8 reports in full, nor waves 1 to 6
again. That is a limit of everything below.

**No circuit below a known count, no growth law below N log N, nothing of the 1e-1 kind. Nothing here changes the order.**

Words. N = 2^k points; an *address* is k bits; x.y = number of common ones modulo 2; *weight* = number of ones.
*The transform* H: entries (-1)^(x.y). *Textbook*: N log2 N gates. T(N): least gates for H, relabelling and scaling free.
*Subset sums* Z, *Yates*: (N/2) log2 N gates for Z. *Neighbour sums* A: every address gets the sum of the inputs at its k
neighbours. *Convolution with g*: output(y) = sum over x of g(x + y) input(x), addresses added bit by bit modulo 2; its
*spectrum* is the transform of g (the convolution is a diagonal in the frame of the outputs). *Flat*: a coset of a subspace
of the address space. *Coset sum*: the convolution with the indicator of a flat. *Quadric*: the set where a form such as
y1 y2 + y3 y4 + ... is 1; *quadric signs*: +1 off it, -1 on it. For even k the transform is, up to free signs and one free
relabelling, the convolution with quadric signs, and its spectrum is quadric signs again [read: w-cross hybrid 1].
*Engine*: the published program's mechanism; a *block* is a stretch of an array's life between interruptions, a *move* one
step along one address direction; its price law is "sum over the blocks of an array of (rank/m)^z = 1", m the block width.

## 0. In ten lines

1. **Wave 8 measured one exchange rate four times, and it is one for one.** A wire that serves two contexts carries a
   foreign part; removing it cost exactly what the sharing saved in ab-4 (a "return": 552 cases, one gate bought, one
   repaid), ab-5 (a "delivery": tie at 8 points), ab-6 (the "leak": 2K - 2 calls, not 1.5 K) and ab-1 (removal by one
   block: "exactly zero-sum"). Section 2, wall REPAY.
2. **The engine's price law turns the user's bar into an exchange rate** [derived + ran, floats, hybrid 3]: with one big
   block and s single-move blocks per array, a saving e needs d/s >= m^e/(1 - e) - 1 moves saved per extra block. For
   e = 0.1 that is 0.28, 0.38, 0.63, 0.78 at block width 4, 9, 45, 110 (ab-1's table, now a formula). The published unit,
   as ab-1 and x-6 quote it, has 0.006. Linear size in this law means one block per array.
3. **ab-3's theorem proves ab-0's open law** [derived + ran, hybrid 4]: the least number of coset sums that add up to
   neighbour sums is exactly ceil(k/2) for every k. General form: flat rank >= k - D, D the largest dimension of a flat on
   which the spectrum is constant. The transform's own kernel needs exactly 4 coset sums at 16 points (bound: 2).
4. **ab-3's "two subspaces" question is a question about one graph** [derived + ran, hybrid 1]. Two partitions of the
   cube; the graph has the classes as vertices and the cube points as edges; the question is whether every cycle of the
   graph is a combination of signed cubes of dimension d + 1. Data: 8 classes forced at 8 points; 12 impossible, 14 found,
   13 open at 16 points; a family with 3N/4 + 2 classes for every k (exact to 64 points). And a ceiling: from degree
   about log2 k on, the classes number at least about 2N/3 [derived from a recalled bound], so this atom cannot give
   better than N log N / log log N. It is off the user's bar even if the answer is yes.
5. **The transform is the straightening of a quadric** [derived + ran, hybrid 2]: there is a convolution with the same
   number of -1 in its spectrum that costs under 2N gates (30 at 16 points, 124 at 64), and the transform is its conjugate by
   a permutation of the outputs. T(N) is, within a factor 2 and 2N, the cost of the cheapest such conjugator. A walk
   found only dense ones (92 of 256 entries at 16 points; a half-and-half construction should have about 64, not built).
6. **Three wave-8 results are wave 1's finite plane again** [ran: replay; the match is mine]: ab-0's "a blurred wire is a
   partial transform", ab-3's "codimension is sold at N/2 gates per unit" and d-1's slice theorem
   T(N) <= R(N) + (sqrt N + 1) T(sqrt N), R = all line sums of the affine plane of order sqrt N. R(N) = O(N) would give
   N log log N, which IS beyond the bar. I found no pricing of R with free coefficients in the part of d-1 I read.
7. Old walls: **S closed in its last named room** (ab-6, by hand); **C extended** from commuting steps to every formula
   of convolutions and every full layer (ab-3, ab-0); **U now blind to height and to the choice of group** (ab-2, ab-7);
   **M has two specimens of height that pays** (ab-2's 4 x 4, ab-7's Pascal) and a one-line reason why neither
   mechanism reaches the transform. k-cross: untouched except that two more bounds are identities of the class.
8. Most surprising: line 1. Most informative question: **which blocks of the published unit carry its saving, and at
   what rate per block?** Section 4.
9. Skeptics first: ab-0's 15-gate circuit modulo 2 (the only object below a count, in characteristic 2 only); ab-6's
   leak lemma; ab-8's order bound and its "first open width". Section 5.
10. A correction to myself, kept: I wrote a hand proof that 13 classes are impossible at 16 points; my own run refuted
    one of its steps (`h1_support.out`). 13 is open.

## 1. Facts that explain each other

**A. A return is a delivery.** [read; the match is mine] ab-4's *return* (a gate whose wire is zero on one half of a cut
and whose parent was not) and ab-5's *delivery* (a gate in which a whole half cancels and a form is handed to the other
half) are the same gate. ab-4's crossing-helper inequality and ab-5's cut lemma are the same bookkeeping of one cut with
different unknowns left over. ab-5's census answers ab-4's first mutation: one given value can save more than one gate
(0 to 3 at 8 points; the half total saves about log2 n), so "gates >= Yates - (number of returns)" is not the right
inequality. [derived] Even if every node of a cube tree got its total for nothing, the sum of log2 |X| over the nodes is
below 2N: single deliveries can never change the order. The order needs about |X|/2 deliveries per node (ab-4) whose
costs overlap (ab-5's mutation "two deliveries that share"). Both reports measured the same tie at 8 points.

**B. ab-3 closes ab-0.** Hybrid 4. ab-0 measured the flat rank 1, 2, 2, 3, 3, 4, 4 for k = 2 to 8 and left "a proof for
all k" open with a bound of order k / (log2 k)^2. ab-3's level-set-flats count gives ceil(k/2) in five lines.

**C. ab-0's two results are one.** [derived] The adding-only law N (k - 1 - floor(k/2)/2) is "r coset sums at N/2 gates
each, then r - 1 additions at every point" with r = k/2: N k/4 + N (k/2 - 1). So the cost of neighbour sums is not in
the coset sums; it is in adding them up at full resolution. That is ab-0's own second wall (to pay less, the additions
must happen on blurred wires, and a family of blurred wires that covers the spectrum is a partial transform).

**D. Blur, codimension, and the finite plane.** [ran: `h4_spread.out`; d-1 had it first] Take a *spread*: sqrt N + 1
subspaces of k/2 address bits that cover every address and meet pairwise in 0. The transform at the outputs in one of
them is the small transform of the sums over the cosets of its perpendicular (checked on every output at 16, 64, 256
points). So T(N) <= R(N) + (sqrt N + 1) T(sqrt N), with R(N) the cost of all N + sqrt N coset sums: the line sums of an
affine plane. This is d-1's slice theorem of wave 1. In ab-3's currency the spread is an atom that supplies k/2 units
of codimension for R(N) gates; in ab-0's words every one of its wires is blurred. If R(N) <= beta N at every size the
recursion gives beta log2 log2 N gates per point (9.4 against 256 at N = 2^256 for beta = 1). New in my run: the line-sum
matrix has rank 9, 27, 81 modulo 2 (3^(k/2)) against 16, 64, 256 over the rationals and modulo 3, and with additions only
it costs exactly (N + sqrt N)(sqrt N - 1) = 60, 504, 4080 because no two lines share two points. It is a matrix where
subtraction provably pays (ab-5's list of separations has this kind). The converse R <= T(N) + (sqrt N + 1) T(sqrt N)
makes R "half a transform or more" if T is N log N: w-cross's half-price statement a third time.
[derived + recalled: Dillon's partial-spread functions; ran at 16 points only, `h4_ruling.out`] When k/2 is even the
quadric's plus set is the union of sqrt(N)/2 + 1 subspaces of a spread. At 16 points: 6 planes lie inside the 10 zeros
of y1 y2 + y3 y4, two triples of them meet pairwise in 0 and cover the zeros, and on all 256 entries
quadric signs(x + y) = -1 + 2 (number of the three planes containing x + y) - 4 [x = y]. So the transform is, up to
free signs, one relabelling and multiples of the identity and the all-ones matrix, "line sums along half the
directions, then spread back": T(N) <= 2 R_half(N) + O(N), with no small transforms at all. (At 16 points this route
costs about 100 gates against 52: it is not a record, it is a relation.)

**E. Why height pays elsewhere and not here.** [read: ab-2, ab-7; the link is mine] The two specimens of tall wires that
pay are a *translation* (ab-2: the difference of two needed wires with different supports and opposite signs on part of
the overlap; needs zeros and signs together) and a *rescaling* (ab-7: Pascal's matrix becomes a convolution after a
diagonal of factorials). The transform's rows have signs and no zeros, and every rescaling of it into a convolution has
entries of one size. Both are the statement "all entries of H have the same size". So wave 8 answers w-cross's fact B
("what does a tall wire that pays look like?") twice, and both answers exclude a flat matrix for one reason.

**F. The same k/2 in the engine.** [guess: same number, not proved the same lemma] ab-8's bound "sources per total at
most 1 + 2^(h - 2r)" and ab-1's ceiling 2^((h+1)/2 - r) are governed by the surplus h - 2r of a port of dimension r in h
bits. A subspace that lies in its own perpendicular has dimension at most h/2; ab-3's D = k/2 is the same fact about
flats on which a quadric is constant. If it is one lemma, ab-8's WIDTH wall is the engine's copy of wall BENT below.

**G. Three prices of one law.** [ran, floats, hybrid 3] ab-1's "one big block plus single moves", x-6's "k equal blocks,
share rho skipped" and ab-6's "the ring adds a block per round and loses" are the same root of the same equation. In the
first shape it reads as a rate: moves saved per extra block.

## 2. The walls, each once

**REPAY (j-cross S; i-cross W2 "sharing between two copies"; w-cross COSTS ADD).** *Pattern, proved in the classes
named: when one wire or one call serves two contexts, the part that belongs to the other context must be removed, and
the removal costs at least what the sharing saved.* Who hit it in wave 8: ab-6 (leak lemma: a first box sends a plain
copy to the output and killing it uses up what a separate call would have supplied: 7 calls at K = 4, 2K - 2 from
K = 8); ab-1 (the unwanted terms of a target come off with one block of rank r whether or not it "knows" the sources:
exactly zero-sum, so "knows" is a discount and not a law); ab-4 (no return at any node of one cube tree forces Yates'
count for Z; one return buys one gate and costs one, 552 of 552); ab-5 (cut lemma; delivering the half total costs 1 at
8 points and at least 2 in six skeletons at 16); ab-2 (where the translation does pay, it saves min(q, r) - 1 on a grid
whose cost is q r).
Status of **S**: x-3 had left one family at 1.5 K (boxes known up to an address map). ab-6 closes it at 2K - 2, by
hand, unreviewed. S is now argued in every class anyone has named. What is NOT one for one: the published unit (the
"knows" discount), ab-2's grid (lower order), and three matrices that are not the transform: Pascal, the plane's line
sums, the 0/1 transform. In all three the saving passes through a rescaling or through the spectrum.

**BENT (j-cross U; w-cross DISTANCE).** *Lemma. The transform's sign pattern is a non-degenerate quadric. It is
constant on no flat of dimension above k/2, and neither is the spectrum k - 2 (weight) of neighbour sums, because the
directions of a flat of constant weight are even words that are pairwise perpendicular.* Who hit it: ab-3 (any function
of M flat indicators needs M >= k/2); ab-0 (flat rank ceil(k/2); two addresses share at most two neighbours); ab-7 (on
every abelian group that carries H, a relation q * c = r with flat c has (non-zeros of q)(non-zeros of r) >= N); ab-2
(a wire one gate from two outputs has partners covering N/2 points at any height); hybrid 2 here (a piecewise affine
straightening of the quadric needs sqrt(N)/2 pieces); ab-8, if fact F holds.
Status of **U**: sharpened three ways. It no longer needs bounded height (ab-2), it holds on every group, with or
without carries (ab-7), and for sums of coset sums it is exact (hybrid 4). Not broken.

**LAYERS (j-cross C).** *Lemma. A program whose stages are convolutions, or full layers (the same gate at every
address up to shifts and signs), needs k/2 stages for the transform and for neighbour sums alike, at N/2 gates per
stage or more.* ab-0: k - 1 layers for A and k for H in the full-layer class; ab-3: every known atom sells codimension
at N/2 gates per unit and k/2 units are needed; block transforms give back exactly the night's (3/4) N log2 N.
Status of **C**: extended from "steps that commute" to "any formula of convolutions". Its hatches are named: gates not
repeated at every address (ab-0), and stages that are not convolutions (ab-3: the low-pass is linear for that reason).
x-4's relaxation to k / log2 k passes stands; hybrid 1 meets the same ceiling from another side.

**HEIGHT (j-cross M).** Sharpened in the other direction: with the best known rate 3/4 the height lemma forces nothing
(ab-2: it bites only below 0.316 N log2 N), no best-count circuit of the night holds a tall wire, and the two tall
mechanisms that do pay are excluded for H by fact E. Height is still required in the long run (w-cross) and still has
no specimen on the transform.

**The door, PORTS, now has three ceilings of its own.** WIDTH (ab-8: 1e-1 is excluded by exact counts at every block
width up to 9, and open on paper only from width 23 to 55 upward); TWO BLOCKS (ab-1: without address maps and phase
letters at least 2 blocks per array, at most 0.0466 at block size 4); BLOCKS PER ROUND (ab-6: a ring of exchanges adds
a block per round). Hybrid 3 puts all three in one unit of measure.

**k-cross, status.** "Every saving tested is an identity of the class": two more (ab-4's tilted-cut bound; ab-5's
"low rank plus sparse" pays for every kernel except s = 0 and 1). "A reflection is a property of the class": ab-5 adds
that Z, after a free relabelling, has order 3 modulo 2. The rectangle count: untouched for the fifth wave running.

**What no wall covers, after eight waves.** A circuit that has, all at once: gates not repeated at every address;
a return at some node of every cube tree and more than N/2 crossing gates in every cut; output gates with two tall
operands, or wires built on two crossing frames; deliveries whose costs overlap; a stage that is not a convolution.
In the engine: partial knowledge, shared sums that cost less than a full descent, and block widths above 23.

## 3. Four hybrids, each tried

### Hybrid 1. Two helpers as one graph (ab-3's last question x the DISTANCE wall x extremal graphs)

Idea. ab-3 asks: can the polynomials of degree at most d on the cube be written as (a function of a coarse label 1) +
(a function of a coarse label 2), with o(N) labels of each kind? Then a polynomial of degree d costs N + o(N) gates at
all points. Make it a picture: label 1 and label 2 are two partitions P1, P2 of the N points. Draw a graph whose
vertices are the classes of both and whose edges are the cube points (a point joins its two classes).
Criterion [derived]. A function is "label 1 part plus label 2 part" exactly when its alternating sum around every cycle
of the graph is 0. So the question is: **do all cycles of the graph lie in the span of the characters of weight above
d**, that is, are they combinations of signed cubes of dimension d + 1? Consequences [derived]: (i) the graph has no
cycle shorter than 2^(d+1) (a relation among the values of polynomials of degree d has at least 2^(d+1) terms: the
DISTANCE wall); (ii) classes - components >= number of monomials of degree at most d; (iii) by the Moore bound for
graphs of given girth and average degree [recalled: Alon, Hoory, Linial], N/t classes force (2t - 1)^(2^d - 1) <= N/t,
so for 2^d above k + 1 the classes number more than 2N/3. Degree 1: girth 4, sqrt N + sqrt N classes, the two halves.
Tried [ran, `h1_graph.py`, `h1_graph.out`, `h1_support.py`, `h1_support.out`].
- 8 points, degree 2: 8 classes are forced by (ii), and attained: P1 forgets bit 1; P2 forgets bit 2 where bit 1 is 1
  and bit 3 where bit 1 is 0. The graph is one 8-cycle, the cube walked as a Gray code.
- A family for every k: P1 forgets bit 1; P2 keeps only bit 2 where bit 1 is 0, and forgets bit 2 where bit 1 is 1.
  Classes N/2 + N/4 + 2. Every polynomial of degree at most 2 is covered at 8, 16, 32, 64 points (fractions) and 128
  (modulo 1000003); degree 3 is not (1, 2, 3, 4, 5 monomial directions missing). The graph is two hubs joined by N/4
  paths of four edges.
- 16 points: 12 classes are impossible [derived: at 12 every class indicator would itself have degree at most 2, and
  no such function is supported on 3 points or fewer, ran]. 14 is the family's count. 13 is open: my first proof used
  "a polynomial of degree 2 supported on 4 points is a constant on a face", which is false (100 such supports, only 24
  are faces: x1 (x2 - x3) is one). The random walk failed its own control (it did not find the 14), so its silence at
  12 and 13 says nothing.
  A second walk seeded from the 14 (merge two classes, then move single points; `h1_seed13.out`, 515,386
  evaluations) came within one missing direction of a 13 and found none. Weak evidence; 13 stays open.
What it gives. The first examples below N (3N/4 + 2), an exact test for any candidate, and a ceiling: by (iii) the
two-helper atom stops at degree about log2 k, so it sells at most log2 k units of codimension for N gates and the
transform would still cost N log N / log log N, x-4's ceiling for flag passes from a different model. That is not a
saving exponent. Where it stops: I do not know whether the classes can be o(N) for degree 2; 8 of 8 and 13 or 14 of 16
do not say. A generalised quadrangle has the right girth with N^(3/4) vertices; the labelling I tried by hand
(point bits plus direction bits) fails.

### Hybrid 2. Straightening the quadric (ab-3's ladder x ab-0's price list x w-cross hybrid 1 x wall BENT)

Idea. In the frame of the outputs a convolution is a diagonal, and a permutation pi of the outputs carries one
convolution to another. Cheap convolutions are those whose spectrum is built from a few flats. The transform's spectrum
is quadric signs. Is there a cheap pattern with the same number of -1, and what does the carrying cost?
Tried [ran, `h2_specperm.py`, `h2_specperm.out`, 16 and 64 points, whole numbers].
- The pattern sigma' = -1 on (a hyperplane minus a subspace of dimension k/2 - 1) has as many -1 as the quadric (6 and
  28). Its convolution is -X_u + (2/|V|) (sum over a subspace V of k/2 + 1 bits): checked entry by entry. Cost at
  most 2N - N/|V| gates: 30 and 124.
- For every permutation pi with sigma(pi(y)) = sigma'(y): C_quadric = Phi C_sigma' Phi^T with Phi = H P_pi H / N.
  [derived] So T(N) <= 2 cost(Phi) + 2N, and cost(Phi) <= 2 T(N): the transform is linear exactly when one of these
  conjugators is. There are (N/2 + sqrt(N)/2)! (N/2 - sqrt(N)/2)! of them.
- A walk over pi (exchange two images inside one level set) reached 92 non-zero entries of 256 at 16 points and 2,321
  of 4,096 at 64 points.
- [derived, rough, not built] A pi that is affine on each of P pieces costs about (P + log2 P) N. On each piece the
  quadric must restrict to a form of rank at most 2, so P >= sqrt(N)/2: N^1.5, the half-and-half route again (I expect
  about 64 non-zeros at 16 points; my walk's 92 is above that, so the walk is weak).
- The rule "the transposed matrix costs the same" is used for Phi^T; it is recalled, as in w-cross.
- [derived] A pi that exchanges y with y + u on a set S costs one convolution (the projector onto S and S + u) plus N.
  So conjugators are themselves built from projectors onto unions of flats.
What it gives: a third member of the family "equivalent to the transform within a factor 2" (after w-cross's hardest
convolution and cheapest basis), with a search space that is purely combinatorial: a permutation. Where it stops: every
structured conjugator I can price runs into wall BENT with the number sqrt(N)/2.

### Hybrid 3. The bar as an exchange rate (ab-1's block shape x x-6's law x ab-6's ring x the published numbers)

Idea. ab-1 found that the price law rewards one big block plus single moves. Solve the law in that shape for the
quantity a designer controls.
Tried [ran, FLOATS, WHAT-IF block lists, `h3_rate.py`, `h3_rate.out`]. With one block of rank m - s - d and s blocks of
rank 1 per array (d = moves saved per array) the law is (1 - (s + d)/m)^z + s m^(-z) = 1. To first order in s m^(-z):
**d/s = m^e/(1 - e) - 1**, e = 1 - z the saving.

| saving e | m = 4 | m = 9 | m = 45 | m = 110 | m = 1000 |
|---|---|---|---|---|---|
| 0.01 | 0.024 | 0.033 | 0.049 | 0.059 | 0.082 |
| 0.10 | 0.276 | 0.384 | 0.626 | 0.778 | 1.217 |
| 0.50 | 3.0 | 5.0 | 12.4 | 20.0 | 62.2 |

The table is the first-order formula (rough in its last row). Exact roots agree with ab-1's table (0.254, 0.373,
0.623, 0.776 for s = 1). At m = 45 the exact rate falls only from 0.62 at s = 1 to 0.57 at s = 15. The published unit as quoted (d = 0.095, 16.5 blocks, m = 45) has d/s = 0.006; put in this shape the law
gives 1.3e-3 (published 8.7625e-4, so the real block list is somewhat worse than this shape), and the same d in 2, 3,
5, 9 blocks would give 0.019, 0.0097, 0.0049, 0.0025.
What it gives: one number to optimise and one bar: **every interruption of an array must buy 0.28 to 0.78 of a move**,
more at larger width, against 0.006 today; and the reading of "linear": z falls to 0 only when the number of blocks per
array is 1 (two equal blocks with 99 % of the directions skipped still give z = 0.15). Where it stops: a restatement of
the engine's own law; it does not say any rate above 0.006 is legal. I did not open the certificates.

### Hybrid 4. Flat rank by level sets (ab-0's flat rank x ab-3's theorem)

Idea. ab-0: how few coset sums add up to neighbour sums? ab-3: a spectrum that is a function of M flat indicators is
constant on a flat of dimension k - M.
Lemma [derived]. The spectrum of c * (indicator of a flat a + V) is a constant times a sign pattern on the
perpendicular of V, and 0 off it. Starting from the whole space, each term costs at most one dimension: if the current
flat is not inside that perpendicular, move to a half of it that misses the perpendicular; if it is inside, move to the
half where the sign is constant. So a sum of r coset sums has a spectrum that is constant on a flat of dimension k - r,
and **flat rank >= k - D**. For neighbour sums D = floor(k/2) (wall BENT), pairs attain it: **exactly ceil(k/2) for
every k**.
Tried [ran, `h5_flatrank.py`, `h5_flatrank.out`, exhaustive over all flats, fractions].

| kernel | k | D | bound | flat rank found |
|---|---|---|---|---|
| neighbour sums | 3 / 4 | 1 / 2 | 2 / 2 | 2 / 2 |
| neighbour sums plus the point itself | 3 / 4 | 1 / 2 | 2 / 2 | 2 / 3 |
| sphere of radius 2 | 3 / 4 | 2 / 3 | 1 / 1 | 2 / 2 |
| quadric signs (the transform's kernel at even k) | 4 | 2 | 2 | more than 3 [ran]; at most 4 [derived]: exactly 4 |

D(neighbour sums) = 2, 3 at k = 5, 6 over all 2,451 and 26,387 flats.
What it gives: ab-0's open item closed (it rests on ab-3's unreviewed count, re-derived here in my own words), and a
new number: the transform's kernel at 16 points is not a sum of 3 coset sums, while it is a product of 2 four-point
pieces. Multiplying out (1 - 2 [y1 = y2 = 1]) (1 - 2 [y3 = y4 = 1]) gives 4 flats, and the kernel searched is that
quadric after a shift of the addresses and a change of sign [derived], so the flat rank is 2, 4 at 4 and 16 points:
2^(k/2) so far. [derived] T(N) <= 2N x (flat rank of the kernel), and the flat rank lies between k/2 and 2^(k/2).
Nobody has asked how it grows; two data points say exponentially [guess]. Where it stops: the bound is not tight off neighbour sums (three rows of the table).

## 4. The most surprising thing, and the question that would tell the most

**Surprise of this wave.** Four agents with different objects (subset-sum circuits cut in two, the literature's cut
proof, call programs for a box, the engine's exchange words) each isolated the elementary act of sharing and measured
its price, and each got exactly one for one: 552 of 552 returns, the 8-point tie, 2K - 2, "exactly zero-sum". Three
of them proved it for a class. Against that, the published unit keeps 0.006 of a move per extra block and is the only
specimen on the transform that keeps anything. The whole published theorem lives in the gap between 1.000 and 0.994.

**Question. Which blocks of the published unit carry its saving, and at what rate per block?**
Why this one. (i) It is the only object where REPAY is known to fail, and by wave 7 the reason is known to be special
to the transform (ports). (ii) Hybrid 3 gives the bar in the same unit: 0.63 at width 45. Whether 1e-1 is alive in the
engine is the question "can the rate rise a hundredfold", and nobody has looked at how the present 0.006 is distributed:
if a few blocks buy most of it, the rate of those blocks alone is the number to compare with 0.63; if it is spread
evenly, the unit is overhead all the way down (helpers are 62 % of its arrays [read: ab-6]). (iii) ab-8 says copies carry
almost all of the gap between 2.5e-2 and 0.12, and ab-1 says "knows" is a discount: both are statements about which
blocks could go. (iv) It needs no search.
Experiment. From the two published certificates (R, read only; `x-6-unitasbox/zlaw.py` already reads the block lists)
compute, for each class of blocks (data, scratch, copies, helpers, idle), the change of the root z when that class is
merged into its neighbours or deleted, and the moves it saves; print rate = moves saved per block for each class and
for the unit; do the same for ab-6's bystander word and ab-1's (m - 1 - d, 1) shape as what-ifs. Output: one table, and
one sentence: is any class of blocks of a legal unit already above 0.1 of a move per block.

## 5. Three objects for a skeptic, in this order

1. **ab-0's 15-gate circuit modulo 2** for one block of neighbour sums at 16 points (`ab-0-neighboursums/
   B4_p2_m7_top_d2.out`, `verify15.py`). The only object of the wave below a count (adding-only needs 16). Claims
   exactly: it is correct in arithmetic modulo 2; 14 gates are excluded modulo 2; the wiring has no lift to the
   rationals for any coefficients (hand argument plus 0 of 32,768 sign choices). It does NOT claim a rational circuit.
   Attack: replay it; check the no-lift argument covers coefficients other than signs; check the exact adding-only
   law N (k - 1 - floor(k/2)/2) it is compared with.
2. **ab-6's leak lemma**: for boxes known up to an address map, at least 2K - 2 calls for every K >= 8 and exactly 7
   at K = 4 (so 6 is impossible). It closes the last room of wall S and was written by hand in an hour. Attack: its
   steps 2 and 3 as the author names them; the exact search for 6 calls at K = 4 (`sixcall.py`, 192 unknowns).
3. **ab-8's order bound and "first open width"**: sources per total at most 1 + (2^(h-r) - 1)/(2^r - 1) for every
   family of labels of class (h, r); hence 1e-1 by the engine's mechanism excluded up to width 9 (at most 4.5e-2) and
   open on paper only from (55, 24), or (23, 9) with a merged word. This decides whether the user's bar is alive in the
   engine. Attack: the random-order proof; the cost model it lives in (every total costs h moves; removal only if fully
   known); the four corrected dictionary lines. With it, ab-1's pair rule, which its author calls its least trusted line.
Also: ab-4's no-return theorem and ab-5's cut lemma may be Boyar and Find's proof restated (neither author read the
paper itself). Mine: hybrid 4's lemma (five lines); hybrid 1's ceiling (iii) rests on a recalled theorem.

## 6. Eight experiments for the next wave

Deepen what is alive:

1. **rate-per-block** (the question of section 4; deepens x-6, ab-1, ab-8, hybrid 3). Brief as in section 4. Inputs:
   the certificates under R, `x-6-unitasbox/zlaw.py`, `aa-cross/h3_rate.py`, `ab-6-chainexchanges/ring.py`. Output: the
   rate table by class of block; the best rate of any legal sub-unit; the bar m^e/(1 - e) - 1 next to it.
2. **line-sums** (deepens d-1, ab-0's break-even, ab-3's atom; the one route here whose success would pass the bar).
   Brief: R(N) = least gates for the N + sqrt N line sums of the plane. T(N) <= R(N) + (sqrt N + 1) T(sqrt N), and for
   k/2 even T(N) <= 2 R_half(N) + O(N) (fact D; true at 16 points, `aa-cross/h4_ruling.out`; check it at 256 points
   first, where the half spread has 9 subspaces of 4 bits). Price R at 16 and 64 points with free coefficients (annealers in `j-machine/`; exhaustive modulo 2 and 3
   for 16 points with `d-0-zeta/mincirc`): adding-only 60 and 504, through the transform 87 and 475. Report gates per
   point against (1/2) log2 N. Then the rank 3^(k/2) modulo 2: is there a circuit over the two-element field with
   about N^0.79 log N gates, and what stops it lifting.
3. **two-deliveries** (deepens ab-5 and ab-4, fact A). Brief: decide 31 gates for subset sums at 16 points over the
   two-element field, with the cut lemma as a filter in all four cuts and with TWO cancelling gates whose mixed parts
   overlap; measure d(4), the least mixed overhead that delivers the half total. Tools: `ab-5-cancellit/mincirc_free.c`,
   `freeform8.out`. Output: d(4), or a 31; and for pairs of free forms at 8 points whether the second is ever worth
   more than the first.

Nobody has tried:

4. **straighten-the-quadric** (hybrid 2). Brief: search the conjugators Phi = H P_pi H / N by structure, not by walk:
   pi a product of j exchanges "y with y + u on a set S that is a union of at most c flats", each costing about
   (c + 1) N gates. Least j as a function of k for c = 1, 2, 3 at 16 and 64 points, exactly. k/2 ties the textbook;
   anything growing more slowly is a growth law. `aa-cross/h2_specperm.py` has the two patterns and the check.
5. **flat-rank-of-the-transform** (hybrid 4). Brief: T(N) <= 2N x (least number of coset sums that add up to quadric
   signs); bounds k/2 and 2^(k/2); exactly 2 and 4 at 4 and 16 points. Decide the value at 64 points (at most 8; a 7
   would already mean N^0.47 in place of N^0.5 by tensoring);
   then allow flats of the doubled address space (x, y), which contains k-cross's rectangles (5, 13, 49) and the
   convolution flats at once. Wanted: the growth law, or a proof that it is exponential (try ab-8's random-order
   argument). `aa-cross/h5_flatrank.py` enumerates flats.
6. **which-bent-function.** Brief: for k >= 8 there are sign patterns as flat as the quadric that are not quadrics
   (partial-spread patterns, patterns built from a non-linear permutation) [recalled]. Each gives an orthogonal
   convolution. Price three of them at 256 points by the night's constructions and by fact D. If one is cheaper than
   the quadric, find what the quadric lacks; if all tie, BENT is a wall for the whole family and can be attacked as one.

One hybrid:

7. **two-helpers** (hybrid 1: ab-3's last question x DISTANCE x extremal graphs). Brief: least total number of classes
   V(k) of two partitions of the cube whose graph has every cycle in the span of the characters of weight above 2.
   Known: V(3) = 8, V(4) = 13 or 14, V(k) <= 3N/4 + 2. Decide V(4); compute V(5) and V(6) (whole-number programme, or
   exhaustive over partitions into subcubes); try to label the flags of a generalised quadrangle (N^(3/4) classes) by
   cube points. Report V(k)/N. Note the ceiling: degree log2 k at most, so this is a constant-factor object unless it
   combines with something else. `aa-cross/h1_graph.py` has the exact test.

One that sounds silly:

8. **modulo 4.** A circuit modulo 4 is not a circuit. But four savings of the night exist in arithmetic modulo 2 and
   die over the rationals: ab-0's 15 gates, ab-7's row that equals the cube modulo 2 only, ab-5's "Z has order 3", the
   line sums' rank N^0.79. Nobody has looked in between. Brief: for ab-0's 16-point block find the least gates over
   the whole numbers modulo 4 and modulo 8 (coefficients 1, 2, 3; a new small search tool). If 15 survives every
   power of 2 there is a circuit over the 2-adic numbers, hence one with algebraic coefficients [derived: a system of
   polynomial equations solvable in one field of characteristic 0 is solvable in algebraic numbers]. If it dies at 4,
   record which gate dies: x-1's price list says each further digit costs 2N for the transform.

## 7. Criticism, last

- I read wave 8 through its result summaries. "One wall" means I matched statements, not proofs. REPAY is a pattern
  with five proofs in five classes, not a theorem; BENT's list includes ab-8 only as a guess.
- Hybrids 1 and 2 are reformulations. w-cross already warned that equivalences have cost this project time. Hybrid 1
  comes with its own ceiling, which says it cannot reach the bar; I report it because the ceiling is the finding.
- Hybrid 1's walk failed its control and one of my hand proofs was wrong; 13 at 16 points is open. Consequence (iii)
  uses a recalled theorem and treats "classes" as the cost, which is ab-3's reading, not checked by me.
- Hybrid 2's walk is weak: it did not find the 64-entry conjugator I can describe.
- Hybrid 3 is floats on what-if block lists, in one idealised shape; the published figures d = 0.095 and 16.5 blocks are
  quoted from ab-1 and x-6, not recomputed from the certificates.
- Hybrid 4 leans on ab-3's theorem; my five-line version is unreviewed. The table's last row is a search that stopped
  at 3 terms plus a hand construction with 4. The flat rank is probably exponential, in which case experiment 5 ends
  in a statement and not in a circuit.
- Fact D's second half (half the lines of the plane give the transform) is derived from a recalled classical fact and
  was run at 16 points only; for k/2 even beyond that it is recalled, and for k/2 odd I claim nothing.
- The question of section 4 is about the engine, not about linear size. I chose it because it is the only place where
  the night's universal exchange rate is known to fail. For linear size itself I have no question better than
  w-cross's, and wave 8 answered that one in the negative in every class it could analyse.
- Nothing here changes the order, or any constant.

Files: `waves/wave-08/aa-cross/` : h1_graph.py, h1_graph.out, h1_support.py,
h1_support.out, h1_seed13.py, h1_seed13.out (hybrid 1); h2_specperm.py, h2_specperm.out (hybrid 2); h3_rate.py, h3_rate.out (hybrid 3, floats);
h5_flatrank.py, h5_flatrank.out (hybrid 4); h4_spread.py, h4_spread.out (fact D: the slice identity on a spread, ranks
of the line-sum matrix, the recursion); h4_ruling.py, h4_ruling.out (fact D, second half, 16 points).
