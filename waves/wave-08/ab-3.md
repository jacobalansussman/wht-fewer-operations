# ab-3 convolution-ladder: the map has two cheap ladders and one forced number, k/2; the "cheap control" of the brief is not cheap

11 October 2026, 04:45 to 05:25 EDT, 60-minute box. Private. One agent; nothing reviewed, nothing in Lean, nothing published.
Marks: [ran] = run of mine tonight (files in `ab-3-convladder/`, whole numbers or fractions, no floats); [derived] = by hand
tonight, checked by nobody; [read] = from tonight's reports; [guess].
Gate count everywhere: **(G)**, a gate is any a*u + b*v, scalings free. Count (O), OpenAI's, is not used.

**No circuit below a known count, and no growth law below N log N for the transform. Nothing here changes the order.**
What is new: the map the brief asked for, drawn by growth laws and not by records at one size; a correction to the brief
(its control family is the hard class itself); one small theorem with a short proof that gives the same forced number, k/2,
for the two bottom rungs (neighbour sums and the transform); and a sharper form of the open question.

## Words

N = 2^k points; an *address* is k bits; *weight* = number of ones. *The transform* H: entries (-1)^(common ones); T(N) = least
gates. *Convolution with q*: output(y) = sum over x of q(x + y) input(x), bits added modulo 2; c(q) = least gates.
*Spectrum* of q: the values s = H q; the convolution is H^-1 (diagonal s) H. *Weight-only* q: q depends on the weight of its
argument only; then s depends on the weight w of its argument only, and I write the spectrum as the list s(0), ..., s(k).
*Neighbour sums* A: q = 1 on weight 1; spectrum s(w) = k - 2w. *Flat*: a subspace of the address space, or a shifted copy of one;
its *dimension* is the number of free bits, its *codimension* k minus that. *Coset sum*: replace every value by the sum of the
values over a shifted copy of a fixed subspace U (cost N - N/|U| gates; every output inside one copy is the same wire).
In the spectrum a coset sum is the indicator (1 on, 0 off) of the flat perpendicular to U. *Low-pass of cutoff d*: the
convolution whose spectrum is 1 on weights up to d and 0 above (x-1's "lightest outputs", there and back).
*Class*: all k-th tensor powers of a 2 x 2 kernel [[1,1],[1,s]]; the transform is s = -1 (k-cross).
*Middle band* of a weight-only spectrum: its values on the weights d < w < k - d, for a fixed d, as k grows.

## 0. In ten lines

1. [ran + derived] **The brief's control is not cheap.** The convolution with q = t^weight is, entry by entry,
   t^|x| t^|y| (t^-2)^(common ones): the class member s = t^-2 with free scalings. So the tensor powers t^weight ARE the class,
   priced like the transform by every construction of the night; only t = 0, 1, -1 are linear. The transform is t = i.
   The premise of "k + 1 cheap tensor powers span everything" is false; section 4 answers the question with the right atoms.
2. [ran] **One line holds the whole weight-only family**: spectra rho^w. rho = 1 identity, rho = -1 the free relabelling
   "every address to its opposite", rho = 0 all-ones, rho = i and -i the transform, other rho the rest of the class.
   The low-pass filters are the derivatives at rho = 0; neighbour sums are the derivative at rho = 1. Section 1.
3. [ran] The transform, read as a sum: for even k, "for every address, add the inputs at distance 0 or 1 modulo 4" is
   (the total sum + a relabelled, re-signed transform) / 2. In the spectrum: the filter that keeps the weights 0 or 1
   modulo 4. The filter modulo 2 costs N/2 gates. So the transform is the step from 2 to 4. Section 1.
4. **The map** (section 2). Three price levels by every construction known: bounded gates per point (trivial middle band);
   about (3/4) k per point (neighbour sums; the transform and the class); about (3/2) k per point (everything else, through
   two transforms). Expense is generic: the spectra with a trivial middle band are a family of 2d + 4 parameters out of k + 1.
5. **Two ladders whose cost per point does not depend on k** (section 3): the sum of j independent shifts (neighbour sums on a
   subcube of j bits): at most (3/4) j - 1 per point; and the low-pass of cutoff d: at most 2d + 1 per point ([read] x-1's
   method; [ran] my own circuits, replayed: 4d + 1 by the cut-off textbook, and the way back at d per point by a pigeonhole
   split). So "the cheapest q whose cost grows with k" does not exist: along both ladders the cost grows with the ladder's own
   parameter, as slowly as one likes. The transform is the top of the second ladder (d = k).
6. [derived; the two facts it uses ran for k up to 5; the statement itself ran over all pairs of flats at k = 4, 5]
   **Theorem (level-set flats).** If a spectrum s is not constant on any
   flat of dimension above D, and s is ANY function of M indicator functions of flats, then M >= k - D. For neighbour sums and
   for the transform D = k/2, and no weight-only spectrum has a smaller D. So every scheme that builds either of them out of
   coset sums by sums, products or any polynomial uses at least k/2 of them; the product of 4-point reflections (the
   transform) uses exactly k/2, pairing (neighbour sums) uses k/2 pairs of shifts, that is k indicators. Section 4.
7. [derived] The same count with low-pass filters as atoms, in any frames: a low-pass of cutoff d supplies d + 1 units of
   codimension and costs 2d + 1 per point by the known method; a coset sum supplies 1 unit for at least 1/2 per point.
   Every atom known supplies codimension at a price of at least N/2 gates per unit. **A change of order inside this calculus
   needs an atom that supplies c units of codimension for o(c) N gates.** That is x-1's open question in a sharper form,
   and section 6 reduces its first case to one sentence: can the polynomials of degree 2 on the cube be split into two
   subspaces that each take only o(N) different value-vectors on the cube? (Degree 1: yes, the two halves of the bits.)
8. [ran, exhaustive modulo p] 8 points, "ball of radius 1" (neighbour sums plus the input itself): no circuit with 14 gates
   modulo 2, none with 13 modulo 3; adding-only greedy has 16. Neighbour sums alone: 12 [read: d-0]. Section 5.
9. The grid at 16 and 32 points asked for by the brief is in section 5, with a warning: at these sizes every sparse q is far
   below the route through the transform, so the grid cannot show the map; the growth laws do.
10. State: transformed into a better question (section 6). Criticism in section 7.

## 1. Identities [ran: `ident.out`, k = 2 to 8, whole numbers; derived where said]

**Free moves on a weight-only spectrum.** Reversing q (q(j) to q(k - j), composing with the relabelling "every address to its
opposite") multiplies the spectrum by (-1)^w. Multiplying q by (-1)^j (signs on inputs and outputs) reverses the spectrum,
s(w) to s(k - w). Both checked on random q at k = 3, 4, 5. Adding a multiple of the identity costs at most N gates; scaling
is free. So a spectrum is known up to: scale, reversal, the twist (-1)^w, and an added constant for N gates.

**The class.** t^(distance of x and y) = t^|x| t^|y| (t^-2)^(common ones of x and y) [ran, t = 2, 3, 1/2, -3 at k = 2, 3, 4].
So convolution with t^weight = (scaling) (k-th tensor power of [[1,1],[1,t^-2]]) (scaling). Its spectrum by weight is
(1 + t)^(k-w) (1 - t)^w: a geometric sequence rho^w with rho = (1 - t)/(1 + t). Real t gives the class members with s > 0;
the transform, s = -1, is t = i, rho = -i. [read: k-cross] the 19-gate circuit at 8 points exists for every kernel tried, so
the class is priced like the transform, N log N with a constant below 1, by everything known. Linear members: t = 0
(identity, 0 gates), t = 1 or -1 (rank one, N - 1 gates).

**The rho-line** [derived]. Every weight-only spectrum is a combination of k + 1 geometric sequences rho^w. Special points:

| rho | spectrum | what it is | gates |
|---|---|---|---|
| 1 | 1, 1, 1, ... | identity | 0 |
| -1 | 1, -1, 1, ... | every address to its opposite | 0 |
| 0 (and infinity) | 1, 0, 0, ... | all-ones (rank one) | N - 1 |
| i, -i | period 4 | the transform | T(N) |
| any other | geometric | a class member | like T(N), by everything known |
| j-th derivative at 0 | a single weight j | band of the low-pass ladder | about (2j + 1) N |
| first derivative at 1 | k - 2w | neighbour sums | about (3/4) k N |

The asymmetry between the last two rows is the asymmetry of the whole map: near rho = 0 the member has rank one and its
derivatives have low RANK (few numbers pass through the middle of the circuit, everything shares); near rho = 1 the member
is a relabelling and its derivatives are SPARSE but of full rank (nothing to squeeze through).

**The transform as a sum, and as a filter.** [ran] H's own q is +1 on weights 0, 1 modulo 4 and -1 on 2, 3; its spectrum is
2^(k/2) times +-1 by weight modulo 4 (k = 2, 4, 6, 8: minus on {2}, {0,3}, {0,1}, {1,2} modulo 4). And the q that is 1 on
distance 0 or 1 modulo 4 and 0 elsewhere has spectrum N/2 at weight 0 plus half of H's spectrum
(k = 4: 6, 2, 2, -2, -2 = 8,0,0,0,0 + (-2, 2, 2, -2, -2); k = 6: 28, -4, 4, 4, -4, -4, 4; k = 8: 136, -8, -8, 8, 8, ...).
So for even k [derived from this and w-cross hybrid 1]: c(sum over distance 0 or 1 modulo 4) = T(N) up to 2N gates, both ways.
The filter keeping weights congruent to 0 or 1 modulo 4 is the same object up to N gates. The filter modulo 2 (keep even
weights) is q = 1/2 on weights 0 and k: output(y) = (input(y) + input(opposite of y))/2, N/2 gates. Period 1 and 2: free.
Period 4: the transform. For odd k the spectrum of H's q has zeros (0, 4, 0, -4 at k = 3): it is one half of a complex
tensor power, and the equivalence costs two calls.

**Period 3** [ran]. The filter keeping weights divisible by 3 has, for k divisible by 3, a q supported on even weights with
q(2i) proportional to (-3)^i (k = 6: 22, 0, -2, 0, 6, 0, -18 times 1/64, the 22 being the identity's share). It is the real
part of the tensor power with t = i sqrt 3: a class member over the complex numbers, not a real tensor power.

**Other small facts** [derived, not run]. Subset sums Z = exp(D) with D = "sum over the addresses with one 1 removed"
(the k one-bit lowering maps commute and square to zero), and A = D + D^T: neighbour sums are log Z plus its transpose.
A is the derivative at t = 0 of the class family [[1,t],[t,1]]: differentiating a class circuit built from blocks of g bits
gives exactly the "grouping" circuit for A (the block's own neighbour sums, then k/g - 1 additions per point); for g = 2 this
is x-5's pairing. So the rate 3/4 of pairing and the rate of block-built class circuits are the same kind of count.

## 2. The map

Weight-only convolutions, k + 1 parameters, by the best construction known for each. "Per point" = gates / N, as k grows.

| family | spectrum by weight w | gates per point | grows with |
|---|---|---|---|
| identity; opposite address | 1; (-1)^w | 0 | nothing |
| filter modulo 2 | 1, 0, 1, 0, ... | 1/2 | nothing |
| all-ones | N, 0, 0, ... | 1 | nothing |
| low-pass of cutoff d (and its mirror at the top weights, and anything supported there) | 1 on w <= d, 0 above | 2d + 1 [read x-1: (d+1) + d]; 4d + 1 [ran, mine] | d only |
| any spectrum equal to a + b (-1)^w on d < w < k - d | free on the 2d + 2 end weights | about 4d + 5 | d only |
| sum of j independent shifts (neighbour sums on j of the k bits) | (number of chosen bits that are 0) - (number that are 1) | (3/4) j - 1 [read x-5; ran] | j only |
| neighbour sums A | k - 2w | (3/4) k - 1 | k |
| the transform's q; sums over distance 0 or 1 modulo 4 | period 4, two values | T(N)/N, about (3/4) k [read] | k |
| t^weight, t not 0, 1, -1 (the class) | rho^w | like the transform [read] | k |
| sphere of radius 2 | quadratic in w | two calls of A: (3/2) k - 1 | k |
| everything else: spheres and balls of radius 3 to k - 3, filters modulo 3, 5, 8, generic q | generic | 2 T(N)/N + 1, about (3/2) k | k |

Reading. (i) **Expense is generic.** The cheap region is "trivial middle band": the spectrum is a constant plus a multiple of
(-1)^w outside 2d + 2 weights at the two ends. That is a family of 2d + 4 parameters inside k + 1. (ii) Only three kinds of
weight-only q are known BELOW the generic price with a non-trivial middle band: neighbour sums, the transform, the class.
(iii) The transform is not an isolated expensive corner: it is one of the cheaper members of the expensive region.
(iv) Nothing known sits strictly between "bounded" and "about (3/4) k": no weight-only q with a non-trivial middle band and
cost per point growing slower than k by any construction I could find. [guess] that gap is real in every calculus of
section 4.

## 3. Two ladders, and why "the cheapest q that grows with k" does not exist

**Ladder J (sparse side).** q = 1 on j independent addresses. On N = 2^k points this is N/2^j copies of neighbour sums on j
bits, so the cost per point a_j does not depend on k: 0, 1/2, 3/2 at j = 1, 2, 3 (12 gates at 8 points, exhaustive modulo
2, 3, 5 [read: d-0]); at most 2 at j = 4 and at least 15/8 modulo 2 if the two halves cannot help each other [read: w-cross];
at most (3/4) j - 1. Neighbour sums on the whole cube is the top, j = k. So brief 1's question is a question about one
function of j: **is a_j bounded, or o(j)?** Whether copies can share is the old "copies do not share" question (WAVE6 L2).

**Ladder D (low-rank side).** The low-pass of cutoff d. [read: x-1] reading side (N inputs to the V lightest outputs) (d + 1) N,
writing side (a polynomial of degree d at all N cube points) d N. [ran, `lowpass.out`, circuits built and replayed for every
k <= 8 and d <= k] my first construction, the textbook cut off on both sides: per point 2.75, 3.75, 4.31, 4.62, 4.80, 4.89,
4.94 at d = 1 and k = 2..8 (limit 5 = 4d + 1); 4.38, 6.06, 7.19, 7.91, 8.35, 8.62 at d = 2 (limit 9). Bounded in k, as it
must be. [ran, `blocks.out`, replayed up to k = 14] a second way back, by pigeonhole: cut the bits into d + 1 blocks; every
product of at most d coordinates misses a block; so the polynomial is a sum of d + 1 pieces, each ignoring one block, and
costs d additions per point plus lower terms: 1.02 per point at d = 1, k = 14 (against 2.00 for the cut-off textbook),
2.37 at d = 2, k = 14 and falling (limit 2, against 4.00). Same limit as x-1's method, by a different route.
The top of this ladder, d = k, is the transform itself.

So at fixed j or fixed d both ladders are LINEAR in N, and both pay about one unit per point per step of the ladder. Take
j or d to grow like log log k and the cost per point grows as slowly as you like: there is no cheapest growing q. The right
question is the growth in the ladder's own parameter. The smallest open cases: a_4 (15/8 or 2), and whether a polynomial of
degree 2 at all cube points needs 2 N gates ([read: x-1] the proven floor is N - 1; x-1's reason "no three cube points on a
line" means no output is a combination of two other outputs, which I re-derived for sums of three two-block tables).

## 4. "What stops a combination of cheap convolutions from being cheap?"

First, the premise: tensor powers are not cheap (section 1). The convolutions that ARE cheap and that span everything are
the coset sums (at most N gates each; in the spectrum: indicators of flats; the single points are among them). Two rules
[derived]: a SUM of two convolutions costs both plus N gates (one addition per point); a PRODUCT costs both. So the cost of
a formula is about N times its number of atoms, and the question becomes: how few flats?

**Theorem (level-set flats)** [derived]. Let s be a function on the address space that is not constant on any flat of
dimension above D. If s = F(b_1, ..., b_M) with b_i the indicator of a flat and F any function at all, then M >= k - D.
*Proof.* Induction on M, for s restricted to any flat G: claim M >= dim G - D. If every b_i is constant on G, s is constant
on G and dim G <= D. Otherwise take a point z of G outside some flat. For every flat F_i not containing z choose a
hyperplane through F_i that misses z, and restrict to the other side of it: at most M - M' restrictions, where M' < M is the
number of flats through z. On the smaller flat G' the dropped indicators are 0 and s is a function of M' indicators, so
M' >= dim G' - D >= dim G - (M - M') - D. QED.

**The two bottom rungs have the same D** [ran for k <= 5, `flatwall.out`; derived for all k; k even from here on, for odd k
read (k - 1)/2 for the weight and (k + 1)/2 for the quadric]. The weight is constant on no
flat of dimension above k/2 (if all of c + S has one weight, every s in S has half its ones inside c, so S embeds in the
coordinates of c and in the others). A full-rank quadric sign, the transform's spectrum for even k, is constant on no flat of
dimension above k/2 (the standard fact about bent functions). And every weight-only function IS constant on the flat
"bits 1 and 2 differ, bits 3 and 4 differ, ...", of dimension k/2. So **neighbour sums and the transform have the smallest D
any weight-only spectrum can have, and need at least k/2 flats in any formula; pairing and the product of k/2 four-point
reflections use exactly k/2** (neighbour sums: between k/2 and k indicators, since a pair of shifts needs two).
For the transform this also says: its phase polynomial over the two-element field is not a sum of fewer than k/2 products of
linear forms of any degrees (a product of c forms is the indicator of a flat of codimension c). I expected high-degree
products to help by cancelling; they do not.

*Machine check of the statement itself* [ran, `thmcheck.out`, exhaustive over all 306 flats at 16 points and all 2,450 at 32
points, every single flat and every PAIR of flats, covering or not]. Weight: no single flat and no pair determines it, at
16 or at 32 points (theorem: at least 2 and at least 3; at 16 points the truth is at least 3, because two indicators give
four values and the weight has five). Quadric sign (weight 0 or 1 modulo 4 against 2 or 3): no single flat; exactly 10 pairs
at 16 points and 10 at 32 (theorem: at least 2 in both, since D = 2 and 3). The theorem is tight there.

**The same count with low-pass atoms, in any frame** [derived]. Let the atoms be arbitrary spectra a_i, atom i vanishing
outside a set B_i such that every point outside B_i lies on a flat of codimension at most c_i that misses B_i. If some
point lies outside all B_i, then any function of the atoms is constant on a flat of codimension at most c_1 + ... + c_M,
so c_1 + ... + c_M >= k - D. A flat has c = 1. A low-pass of cutoff d, in any relabelling of the address bits by an
invertible bit matrix, has c = d + 1 (a point outside the ball has d + 1 ones; fix them). Prices by the known methods:
coset sum, at least N/2 for 1 unit; low-pass, (2d + 1) N for d + 1 units; the transform on a block of c bits, about
(3/4) c N for c/2 units (it is a product of c/2 reflections, and its spectrum is constant on flats of codimension c/2).
With k/2 units needed, block transforms give (3/4) k N: the night's best rate for the transform, recovered by this count.
**Every atom known sells codimension at N/2 gates per unit or more, and neighbour sums and the
transform each need k/2 units.** That is N log N, from one count, for both rungs and for every mixture of the cheap corners.

**Is there a q where the stop fails?** Yes, exactly the cheap corners: their spectra are constant on huge flats (a low-pass is
0 on a flat of codimension d + 1), so the theorem asks nothing. And the low-pass shows what the calculus does not see: it is
linear although it is a sum of about k^d point atoms, because its circuit is NOT a formula of convolutions. Its middle stage
(N numbers squeezed to V numbers and back) is not a convolution at all. So:
- inside the calculus of commuting convolutions the count k/2 is forced [derived];
- the 7-gate circuit at 4 points is ONE atom of the calculus (identity minus half the coset sum); the textbook and the
  22 gates at 8 points [read: g-3] are formulas of atoms at the atoms' prices; the 19 at 8 points and the 3/4 family are
  cheaper than any such formula, so they share wires BETWEEN atoms [derived from the counts only; I did not take the
  circuits apart]; the published unit uses address maps. The savings of the night start exactly where the calculus ends.

## 5. The grid the brief asked for, and exact small cases

[ran, `grid.out`; every circuit replayed exactly; "adding-only greedy" = repeatedly merge the pair of wires that most rows
share; an upper bound, not a minimum; no free-coefficient annealing was run, see section 7]

| q | 8 points | 16 points | 32 points |
|---|---|---|---|
| sphere of radius 1 (neighbour sums) | 12 | 32 | 96 |
| sphere of radius 2 | 12 | 20 | 136 |
| sphere of radius 3 | 0 | 32 | 136 |
| ball of radius 1 | 16 | 48 | 112 |
| ball of radius 2 | 18 (15 with one subtraction: total minus opposite) | 64 | 136 |
| ball of radius 3 | 7 | 42 | 176 |
| low-pass d = 1 (cut-off textbook, both ways) | 30 | 69 | 148 |
| low-pass d = 2 | 35 | 97 | 230 |
| H's own q (= the transform) | 19 | 52 | 128 [read: the night's best] |
| t^weight, the control | 19 [read: k-cross, every kernel tried] | 64 by the textbook; I know no better for a general t | 160 by the textbook |
| route through two transforms, 2T + N | 46 | 120 | 288 |

Warning: at 16 and 32 points every sparse q is far below 2T + N, and the low-pass circuits are ABOVE the sparse ones; the
asymptotic order of section 2 is the reverse. C(k, j) terms per point against (3/2) k crosses near k = 10 for radius 2.
A grid at these sizes cannot draw the map. The control costs exactly what the transform costs: the brief's one sanity check
fails, which is finding 1.

Exact searches at 8 points [ran, `mc_*.out`, `d-0-zeta/mincirc`, exhaustive in each field; "none modulo p" is not "none"]:
- ball of radius 1 (the matrix identity + neighbour sums): no circuit with 14 gates or fewer modulo 2, none with 13 or fewer
  modulo 3 (14 modulo 3 ran out of its 300 seconds, undecided). Greedy: 16. So modulo 2 it is 15 or 16, against 12 for
  neighbour sums alone: adding the input back costs 3 or 4 gates at 8 points, not 8.
- the band "weight exactly 1" (rank 3 at 8 points, 4 different outputs up to sign): none with 9 gates or fewer modulo 3
  (10 ran out of time), none with 9 or fewer modulo 5. By hand it has 21 (three sums at 15, then 6 to spread them), so
  the gap is wide open.
- the low-pass of cutoff 1 (rank 4 at 8 points; the matrix with entries 4, 2, 0, -2 by distance): none with 13 gates or
  fewer modulo 3 (14 was interrupted when I stopped the queue; its file is empty). My cut-off textbook circuit has 30;
  x-1's route through the k + 1 sums gives 3N - k - 3 = 18 [read]. So between 14 and 18 modulo 3.

## 6. The better question

The brief asked for the cheapest q whose cost grows with k. The answer is that the family has two ladders with their own
parameters and one forced quantity. In order of what they would tell:

1. **Codimension per gate.** Is there any linear map on N points, built with o(c) N gates, whose spectrum (as a convolution)
   vanishes outside a set that every outside point escapes by a flat of codimension c? Flats: c = 1 for N/2. Low-pass:
   c = d + 1 for (2d + 1) N. The transform on c bits: c for (3/4) c N. An atom at o(c) N is the only way the calculus of
   section 4 can go below N log N, and "a polynomial of degree d at all cube points in o(d) N gates" (x-1's question) is one
   candidate. First test: degree 2, is 2N forced? x-1 has "none with 19 at 16 points modulo 2 or 3; 20 to 25 open".
   In other words [derived]: the atom's spectrum must live on a set B that meets every flat of dimension above k - c
   (a *blocking set*). Balls of radius c - 1 are blocking sets (about k^(c-1) points). Random sets of about c k 2^c points
   are too (union bound, not run), and the cut-off textbook reads the transform at m scattered outputs in about
   N (log2 m + 2) gates, so they also come out near 2N per unit. **Nobody has asked which blocking set is cheapest to
   read.** That is a search with a growth law attached: least gates to read the transform on a set that meets every flat
   of codimension c - 1, as a function of c, at 16 and 32 points first (c = 2: an affinely independent set of k + 1
   outputs, 2N - k - 2 gates, optimal [read: x-1]; c = 3 is the first open case).
   **The same question as pure geometry** [derived in the last quarter of the box, checked by nobody]. Fix d. Writing side:
   the output at address x is the vector o_x of all products of at most d coordinates of x (coordinates +1, -1), a vector
   with V entries, V about k^d/d!. Any helper wire is a vector with V entries and costs at most V - 1 gates, and V is
   tiny against N. So: **if there is a set of o(N) helper vectors such that every o_x lies in the span of two of them,
   the polynomial of degree d costs N + o(N) gates at all N cube points, the low-pass of cutoff d costs 3N + o(N) for
   every fixed d, and codimension is sold at o(c) N.** For d = 1 such a set exists: 2 sqrt(N) helpers, one per half
   address. For d = 2 I could not decide it. What I can say:
   (a) helpers that are functions of a quotient of the address (constant along some direction) cannot do it: the outputs
   then need c - 1 = d additions per point. It is the theorem of section 4 again, seen from the writing side.
   (b) x-1's wall ("from degree 2 on, a helper serves one output") is about gates "output = output + helper". Gates
   "output = helper + helper" are not covered. The only constraint I can prove on them: no three outputs lie in one plane,
   and more generally any linear relation among the o_x has at least 2^(d+1) terms [read: x-1; the minimum distance of a
   Reed-Muller code]. In the graph "two helpers are joined when they make an output" this forbids every small piece with
   more edges than vertices (fewer than 2^(d+1) edges). Graphs with N edges on N^(1-delta) vertices and no such piece
   exist, so this constraint does not forbid N + o(N). It forces the helper graph to look locally like a tree.
   (c) so the open object is: **a set of o(N) points such that every point o_x of the cube's image lies on a line
   through two of them, the lines forming a graph without small dense pieces.** Smallest test: 16 points, d = 2, where
   x-1 left 20 to 25 gates open; a helper + helper circuit there would have 15 output gates and at most 9 helpers.
   (d) the most regular way to get such helpers: **split the space of all polynomials of degree at most d into two
   subspaces Q1 + Q2, each of which takes only o(N) different value-vectors on the cube.** (Helper 1 at x = the part of
   the polynomial in Q1, helper 2 = the part in Q2; each helper has as many different values as its subspace has
   value-vectors.) Degree 1: Q1 = functions of the first half of the bits, Q2 = of the second half; sqrt(N) values each.
   Degree 2, what I found by hand: two subspaces "polynomials in all bits but a set T_i of delta k bits" have
   N^(1-delta) values each and miss only the delta^2 k^2 products of a bit of T_1 with a bit of T_2; subspaces that are not
   of that kind exist with few values (all polynomials of degree 2 in the k/2 pair sums x_1 + x_2, x_3 + x_4, ...:
   dimension about k^2/8, only 3^(k/2) = N^0.79 values), but the ones I tried need about 2 log2 k subspaces, not 2.
   Whether two suffice for degree 2 is the smallest question I can state whose answer "yes" would give a new linear
   object (low-pass of every fixed cutoff at 3N) and whose answer "no" would need a reason that is not volume, not
   distance, and not the theorem of section 4. It can be searched exactly at 64 points (22-dimensional space, 64 points).
2. **a_j.** Gates per point for the sum of j independent shifts, as a function of j alone. a_4 is 15/8 or 2 (brief 1).
3. **Leave the calculus on purpose.** The theorem says where NOT to look: any program whose stages are convolutions.
   Stages that are not convolutions are what the low-pass, the 19 and the published unit have in common. A census of the
   night's saving circuits by "which intermediate wires are outputs of a convolution" would say how far outside they are.
4. **The step from 2 to 4.** The filter modulo 2 is the pairing of an address with its opposite; the filter modulo 4 is the
   transform. Over the complex numbers the transform is, up to free phases, the convolution with spectrum i^w, and its
   square has spectrum (-1)^w: the transform is a square root of the free relabelling "opposite". Other real square roots of
   that relabelling cost O(N) (a shift along one bit with a sign read from two bits, applied to the half of the data that
   changes sign under "opposite" [derived, checked by hand only]). What is expensive is the square root that also commutes
   with every permutation of the address bits. Question: how much of that symmetry can be dropped before the root becomes
   cheap, and how much before it stops being the transform up to an address map.

## 7. Criticism, last

- **No annealing.** The brief asked for free coefficients at 16 and 32 points. I priced by constructions and by one greedy,
  all replayed exactly, and used exhaustive search only at 8 points. Every number in section 5 is an upper bound except
  where a field is named. The annealers in `j-machine/` take named tasks and needed adapting; I judged the grid uninformative
  at these sizes (section 5) and spent the time on growth laws. A free-coefficient search could still lower single entries.
- **The three price levels are prices of constructions.** No lower bound above N + something is behind any row of the map.
  "Everything else costs (3/2) k" means: I know nothing better than two transforms.
- **The theorem is about formulas of flats.** It does not bound circuits. It is tight for the transform in its own model and
  within a factor 2 for neighbour sums. Its extension to low-pass atoms assumes a point outside all the atoms' supports
  (true unless the atoms are very many) and uses the known PRICES of the atoms, which are upper bounds. If the low-pass of
  cutoff d were cheaper than d per point, the conclusion would fail; that is question 1, not a wall. The proof is a dozen
  lines and unreviewed; the two facts about flats were run only for k <= 5.
- The identification "the transform = sums over distance 0 or 1 modulo 4" needs k even and rests on w-cross hybrid 1
  (its identity ran there for k = 2 to 6; I ran the spectra for k = 2 to 8).
- The ladder D numbers at 2d + 1 are x-1's; mine are worse (4d + 1) or equal in the limit only (the pigeonhole way back,
  whose lower terms are large: 2.37 per point at d = 2, k = 14). The reading side at (d + 1) N by transposition is [read].
- "Copies do not share", used for ladder J, is an unproved assumption of the night.
- x-4 lemma A ("at least k/2 passes without the diagonals") is probably the same number for the same reason; I did not
  read its proof, so the theorem may be a restatement of it in the language of spectra, with the neighbour-sum half added.
- x-4 lemma D reached "about k / log2 k passes" in a neighbouring model with free diagonals between passes. My count gives
  k/2 because my atoms commute; non-commuting stages are outside it. The two statements do not contradict each other.
- Question 1's geometric form was written in the last quarter of the box. Step (b) uses a count of graphs (many edges, no
  small piece with more edges than vertices) that I recalled and did not check, and "the helpers cost o(N)" needs the
  number of helpers times V to be o(N), true for fixed d only. Nothing was built for d = 2. It is a target, not a result.
- Nothing here changes the order, or any constant.

Files: `waves/wave-08/ab-3-convladder/` : `ladder.py` (matrices, spectra, circuit
builder with exact replay; parts `ident`, `lowpass`, `grid`), `ident.out`, `lowpass.out`, `grid.out`; `blocks.py`,
`blocks.out` (the pigeonhole way back); `flatwall.py`, `flatwall.out` (largest flats with constant weight / constant quadric
sign, k = 2 to 5); `thmcheck.py`, `thmcheck.out` (the theorem on all single flats and pairs at k = 4, 5); `rows_*_k3.txt`, `mc.sh`, `mc_*.out` (exact searches at 8 points).
