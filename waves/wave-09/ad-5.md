# ad-5 which-bent: the quadric is the cheapest known member of its family, and within a factor 2 of the dearest

11 October 2026, 60-minute box, one agent. Private. Nothing reviewed, nothing in Lean, nothing published.
Marks: [ran] = run of mine tonight, whole numbers, files in `ad-5-whichbent/` (run on the rented Linux machine because this
Mac's python has no numpy; outputs copied back); [derived] = by hand tonight, checked by nobody; [read] = tonight's
reports; [recalled] = from memory, no source opened; [guess]. Gate count everywhere: **(G)**, a gate is any a*u + b*v.

**No circuit below a known count. No growth law below N log N. Nothing here changes the order.** What follows is the
answer to the brief's question, two exact laws, and one statement that covers the whole family.

Words. N = 2^k points, k even, m = k/2, q = 2^m = sqrt N. An address is a pair (x1, x2) of half-addresses of m bits.
*Convolution with g*: C_g[y, x] = g(x + y). *Bent pattern*: values +1/-1, spectrum (its transform) of constant size q.
*Quadric*: g = (-1)^(x1 . x2). *MM pattern* (Maiorana and McFarland's family): g = (-1)^(x1 . p(x2)), p a bijection of
the half-addresses; s = the inverse of p. *PS pattern* (partial spread): -1 on q/2 members of a spread, 0 removed
(PS-), or +1 on q/2 + 1 members (PS+). *MM class*: everything obtained from an MM pattern by an invertible relabelling
of the addresses, a shift and a character; all of that is free in count (G). T(N) = least gates for the transform.
A = "the q-point transform applied to x1 inside every column x2" (cost q T(q)).

## 1. The answer in six lines

1. **Every MM convolution is two layers of small transforms with a shear between them** [derived, ran at 64 and 256
   points on every entry]: C_g = A SHEAR_s A, with no scaling, where SHEAR_s is the permutation
   (w, x2) -> (w, x2 + s(w)). So cost(C_g) <= 2 q T(q) for EVERY bijection p, linear or not: (3/4) N log2 N + N/2
   with the night's small counts. The quadric is the case "s linear".
2. **Every pattern with a spectrum of signs costs at most 2 T(N)** [derived: C_g = H D H / q, D a free diagonal], and
   T(N) IS the cost of the quadric's convolution. **So the quadric is within a factor 2 of the dearest member, and it
   is the cheapest known one.** The family ties in the order; the spread of known prices is the factor 2.
3. **At 64 points every non-quadric pattern I built prices at exactly 304 gates, the transform's own best count**
   (2 x 8 x 19), although its convolution is a different Hadamard matrix (not the transform relabelled; section 3).
4. **At 256 points two partial-spread patterns are outside the MM class** [ran: Dillon's test over all 200,787
   subspaces]. For them I have only 2 T(N) (12.5 gates per point) or the line-sum route (17.5).
5. **What the quadric has that the others lack is choice, not a cheaper law**: it is an MM pattern for 135 different
   splits at 64 points and 2,295 at 256 (all the self-perpendicular subspaces); every other pattern has exactly 1, or 0.
6. **The walls BENT and LAYERS use bentness only** (section 4): in the calculus where a stage is a shift controlled by
   a flat, a bijection of m bits needs m stages whatever it is, and at 64 points the linear ones need exactly 3 and
   ALL 4,872 non-linear ones exactly 4 [ran, exhaustive]. There the quadric is the unique cheapest class.

## 2. First experiment: prices

Patterns [ran, `bent3.py`, `bent3.out`]: all bent (every spectrum entry of size q checked).
Correction to the brief: **y^3 is not a bijection of the field with 16 elements** (3 divides 15; it takes 6 values).
I used y^3 at q = 8 and y^7, 1/y at q = 16. The recalled fact "cubic bent patterns exist at 64 points" holds [ran].

Counts used: T(4), T(8), T(16), T(64) = 7, 19, 52, 304 [read: the night's family]; T(256) = 1600 [read from the
brief, derived there from the family's law, not replayed by anyone]. Line-sum route for PS- = (q/2 coset-sum families,
adding only, N - q gates each) + (the total, N - 1) + (add the families at every point, (q/2 - 1) N) + (combine with
the total and the point itself, 2N); identity C = J - 2 (sum of the q/2 coset-sum matrices) + q I [ran at 64 and 256].

| N | pattern | degree | in the MM class | best construction | gates | per point | largest coefficient |
|---|---|---|---|---|---|---|---|
| 64 | quadric | 2 | yes (135 splits) | the night's family | 304 | 4.75 | as in e2-0 (not re-read) |
| 64 | x1 . p(x2), p = y^3 | 3 | yes (1 split) | A SHEAR A | 304 = 2 x 8 x 19 | 4.75 | those of the 19-gate circuit |
| 64 | PS-, slopes of trace 1 = x1 . (1/x2) | 3 | yes (1) | A SHEAR A | 304 | 4.75 | same |
| 64 | PS-, slopes {2,3,4,7}; PS+ same + infinity | 3 | yes (1) | relabel, then A SHEAR A | 304 | 4.75 | same |
| 64 | any PS-, line-sum route | | | 224 + 63 + 192 + 128 | 607 | 9.48 | q = 8 |
| 256 | quadric | 2 | yes (2,295) | the night's family | 1600 | 6.25 | as in e2-0 |
| 256 | x1 . p(x2), p = y^7 or 1/y | 4 | yes (1) | A SHEAR A | 1664 = 2 x 16 x 52 | 6.50 | those of the 52-gate circuit |
| 256 | PS-, slopes of trace 1 | 4 | yes (1); it IS x1 . (1/x2) [ran] | A SHEAR A | 1664 | 6.50 | same |
| 256 | PS-, 8 generic slopes | 4 | **no** (0 of 200,787) | transform, signs, transform | 3200 | 12.5 | as in e2-0 |
| 256 | PS+, the same slopes + infinity | 4 | **no** | transform, signs, transform | 3200 | 12.5 | as in e2-0 |
| 256 | any PS-, line-sum route | | | 1920 + 255 + 1792 + 512 | 4479 | 17.5 | q = 16 |

"In the MM class" is Dillon's test [recalled criterion; ran]: a subspace V of m bits such that the pattern's exponent
has all second differences along V equal to 0. At 64 points all five non-quadric patterns pass with exactly one V
(consistent with the recalled fact that every bent pattern at 64 points is in the MM class; I did not enumerate all).
The "relabel" rows at 64 points use that test's verdict; I did not write the relabelling out.

**Growth, per point** [derived from the constructions]: quadric (3/4) k + 1/4; MM class (3/4) k + 1/2; PS outside
the MM class (3/2) k + 1/2 through the transform, about sqrt N through line sums. **All of order k. No member of the
family has a construction that grows more slowly than k.** The line-sum route is the worst here, not the best.
A general PS pattern of the field plane is a combination of q patterns x1 . (c / x2) [derived]; that route costs
4 q T(q), the same 2 T(N). I found nothing between 1 and 2 transforms for a pattern outside the MM class.

## 3. Identities and regularities [ran unless marked]

- **C = A SHEAR_s A.** Reason [derived]: for fixed (x2, y2) the q x q block of C_g is the single character
  chi_w chi_w^T with w = p(x2 + y2), a rank-one block; in the frame of the small transform on x1 it is one entry.
  In words: *the w-th small-transform coefficient of output column y2 is taken from input column y2 + s(w)*.
- **C = product of m one-bit shears**, the i-th being "shift x2 by the i-th unit where bit i of s(w) is 1", each
  = (projector onto a set of characters of x1) in every column, plus a combination. For s linear the set is a
  hyperplane and the stage is one butterfly layer: the textbook. This holds for every map s, bijective or not: the
  convolution is orthogonal for every s, flat (all entries of one size) exactly when s is a bijection.
- **C_g = Phi^T C_quadric Phi / q^2 with Phi = (H_q P_s H_q) in every column** (P_s the permutation matrix of s).
  This is aa-cross's conjugator (hybrid 2) in a product form: all its cost sits in one q x q orthogonal matrix,
  "the permutation s seen through the small transform". Non-zero entries of that small matrix: 8 of 64 (linear: a
  permutation), **29 of 64** for y^3 and for 1/y; 16 of 256 (linear), **151 of 256** for y^7 and 1/y.
  Consequence [derived]: T(N) <= cost(C_g) + 2 q cost(small Phi). If s is linear up to t exchanges of two values,
  the small Phi is t rank-one corrections, so cost(C_g) = T(N) up to about 4 t N: **a linear circuit for any one
  pattern within a bounded number of column exchanges of the quadric would be a linear transform.** The target is a
  neighbourhood, not one matrix.
- **Different matrices, same price.** Rank over the two-element field of the 0/1 matrix [exponent of g at x + y]:
  quadric 8 and 10 (k + 2); cubic patterns at 64 points: 14, all five; at 256 points: 30 (the three in the MM class),
  36 (PS+ generic), 42 (PS- generic). Changing signs of rows and columns moves this rank by at most 2 [derived], so
  at 256 points these are four Hadamard matrices no two of which are the same up to relabelling and signs, and none
  but the first is the transform. The 304 at 64 points is therefore not the transform's count in disguise.
- **Number of splits.** Subspaces passing Dillon's test: quadric 135 = 3 x 5 x 9 and 2,295 = 3 x 5 x 9 x 17 (the
  subspaces that lie in their own perpendicular); every non-quadric MM pattern: exactly 1; generic PS at 256: 0.
- **Largest flat on which the pattern is constant**: m = k/2 for all twelve patterns (searched: every flat of
  dimension m and m + 1). So wall BENT's number D = k/2 is the same for the whole family at these sizes.
- Each spectrum has 28 / 36 entries -q / +q at 64 points and 120 / 136 at 256: one type, so by `h2_specperm` every
  pair is conjugate by a permutation of the outputs.

## 4. Which property did each wall use: bent, or quadratic?

| wall or fact | what it really used | evidence |
|---|---|---|
| BENT: constant on no flat above k/2 | **bent** | [recalled: true of every bent pattern] ; [ran] D = k/2 for all twelve. Patterns with D below k/2 exist from k = 10 [recalled], so they are worse, not better: the quadric has the largest D possible |
| aa-cross hybrid 4: flat rank >= k - D | **bent** (the proof never mentions the form) | [read] |
| LAYERS: k/2 stages | **bijectivity of s = bentness** | lemma below; [ran] m = 2, 3 |
| fact E, HEIGHT: all entries of one size | **bent** by definition | |
| the rate 3/4 (k-cross: an identity of the whole class of third powers) | **neither**: it is inherited through A for every MM pattern | row "A SHEAR A" of the table |
| the 135 and 2,295 splits; the tensor form; "a relabelled transform" | **quadratic** | section 3 |

**Lemma (flat shears)** [derived]. Call an *elementary shear* a map w -> v [w in F], F a flat of half-addresses or the
complement of one, v fixed; its convolution costs about 2N gates (one coset sum in every column, one combination per
point), and shears compose by adding the maps. A sum of r elementary shears is constant on a flat of codimension r
(for each term halve the current flat so that it lies inside F or misses it). A bijection is constant on no flat of
dimension 1 or more, so **r >= m = k/2 for every bijection**: m stages at about 2N gates, the textbook order, with no
use of linearity. This is wall LAYERS for the whole MM family.
**Exact search** [ran, `shearrank.py`, `shearrank.out`, breadth-first over all 2^21 maps of 3 bits fixing 0, 51 flats,
301 elementary terms up to constants; constants free]: every map has rank at most 4; the 168 linear bijections have
rank exactly 3; **all 4,872 non-linear bijections have rank exactly 4**, in each of the three non-linear classes
(1,176, 2,352 and 1,344 bijections with 3, 1 and 0 affine combinations of output bits; with the linear class these
are four classes, the number recalled for bent patterns at 64 points). At m = 2 all 6 bijections are linear, rank 2.
So in this calculus the quadric is the strictly cheapest class and non-linearity costs one stage, not fewer.

**Flat rank with bounded coefficients** [derived]. If a bent pattern is a sum of r terms c_i (character)(indicator of
a flat), then pairing with g gives N = sum c_i <g, term_i>, and each pairing is at most q in size (a bent pattern sums
to at most q on any flat, with any character). So **sum |c_i| >= sqrt N for every bent pattern**: with coefficients
of bounded size the flat rank is at least sqrt N / c, and MM patterns attain sqrt N with coefficients 1 (one signed
flat per column). PS- uses q/2 + 2 flats, one of them with coefficient q. The linear lower bound k/2 is all that
survives when coefficients are free. Same split as everywhere tonight: bounded coefficients, a proof; free, nothing.

## 5. The one statement for the family, and "yes, and" three times

**Statement (BENT-FAMILY)** [guess; equivalent in order to T(N) = N log N for the first line only]:
for every bijection s of m bits, the matrix A SHEAR_s A needs c N m gates. Known about it: (a) it is at most
2 q T(q) for all s; (b) for linear s it IS the transform; (c) in the flat-shear calculus it is at least 2 N m for
all s [lemma]; (d) with bounded coefficients it is at least (N/2) log2 N / log(2c) for all s, because every one of
these matrices is a Hadamard matrix [recalled: the determinant bound]. It asks about a set of q! matrices with one
proof shape, and its hatch is visible: a stage that is not controlled by a flat.

- Failure 1: "a non-linear p might be cheaper". It is not, in any route I have: the two layers of A are paid in full
  and the shear is free. *Yes, and*: then the cost is entirely in A, and the question becomes whether SHEAR_s can
  make the two layers share. For linear s they collapse to a tensor product (the night's family uses that; saving
  N/4 at 256 points). For non-linear s there is one split only, so nothing to choose.
- Failure 2: "a cheap pattern could be carried to the transform". The carrier is the small Phi, dense for power maps
  (29 of 64, 151 of 256). *Yes, and*: for s near linear it is a few rank-one corrections, which widens the target
  (section 3) but only inside a neighbourhood where the costs agree up to O(N) anyway.
- Failure 3: "partial-spread patterns bring the plane's line sums". They do, but at 256 points the line-sum route is
  the dearest (17.5 per point), and the generic ones leave the MM class. *Yes, and*: these are the first members of
  the family for which nothing better than two full transforms is known; whether a pattern outside the MM class can
  be priced below 2 T(N) is a clean small question (mutation 2).

## 6. Mutations

1. **A shear controlled by something that is not a flat.** The lemma's only hatch. Find sets S of characters of m
   bits whose projector costs O(q) gates and which are not flats or complements (unions sharing work, sets built by
   the night's 19-gate circuit), then redo `shearrank.py` with them as extra generators: does any bijection of 3 or 4
   bits drop below m stages? If one does for a LINEAR bijection it is a transform below textbook order of stages.
2. **Price a pattern outside the MM class below 2 T(N)**, at 256 points (the two PS patterns of `bent3.py`), by
   annealer or by structure; or show that Dillon's test failing forces two transforms. Decides whether the family
   has two price levels or one.
3. **Non-bijective s as a dial.** A SHEAR_s A is orthogonal for every map s; s constant costs 0, s linear of rank r
   costs a transform on 2r bits. Measure the cost against the flat-shear rank r(s) for all maps of 2 bits (64 maps,
   16 points, exhaustive tools reach it): is cost = 2 N r(s) exactly, or does some map pay less than its rank?
   A map that pays less than its rank is the specimen every wall of the night says cannot exist.
4. **Spreads that do not come from a field** (256 points) were not built; their PS patterns are the natural
   candidates for "outside the MM class with extra structure". Not tried for lack of time.
5. **Why exactly one split?** 135 and 2,295 against 1: count the splits of all four classes at 64 points and of
   patterns one column exchange away from the quadric; the 3/4 constructions may be using exactly this number.

## 7. Criticism, last

- The prices are upper bounds by construction, with the night's small counts taken as read (T(256) = 1600 is a
  formula nobody replayed). "Cheapest known" is not "cheapest".
- "Within a factor 2 of the dearest" is the trivial bound C = H D H / q; it is true of any pattern whose spectrum is
  signs, bent or not, and I include it because it is the honest answer to "cheapest, dearest or typical".
- A SHEAR A is elementary and surely classical for this family [guess]; what is new tonight is only that it puts
  the night's walls on all of the family at once. Statement BENT-FAMILY for linear s is the old open problem.
- The flat-shear lemma bounds a calculus, not circuits. Its unit price 2N per stage is my reading. The exhaustive
  result is for m = 3 only; "non-linear costs exactly one more stage" is one data point.
- Dillon's test, the bound D <= k/2 for all bent patterns, non-normal patterns at k >= 10, the four classes at 64
  points and the determinant bound are recalled; no source was opened. The test's outcome "0 subspaces" for the two
  generic PS patterns is a run; that it means "not in the MM class" rests on the recalled criterion.
- I tried one generic choice of slopes at each size, and no annealer: no search could have found a cheap circuit
  for a non-quadric pattern, so the tie at 304 is a tie of constructions.
- Nothing here changes the order, or any constant.

Files: `waves/wave-09/ad-5-whichbent/` : bent3.py, bent3.out (twelve
patterns at 64 and 256 points: bentness, degree, ranks, flats, Dillon's test, the four identities);
shearrank.py, shearrank.out (flat-shear rank of every map of 2 and of 3 bits).
