# k-cross: the three waves side by side, four hybrids tried, and what to ask next

10 October 2026, 23:25 to about 00:05 EDT, 40-minute box. Private. One agent; nothing reviewed, nothing in Lean, nothing published.
Marks: [ran] = exact run of mine tonight (files in `k-cross/`); [ran, solver] = floating-point solver output, a candidate only;
[derived] = by hand tonight, checked by nobody; [read] = from tonight's reports; [guess].
Gate count everywhere: **(G)**, a gate is any a*u + b*v, scalings free, unless a line says (O) (OpenAI's count).
Read: i-cross, NOTE, the heads of all twelve wave-2 reports (e-0 to e-7, e2-0 to e2-3), j-manyatonce's head, the eight wave-3 results.
`j-cross.md` and `WAVE2-NOTE.md` had not landed when I started; I did not read them.

Words. N = 2^k points. *The transform*: the Walsh-Hadamard matrix H, entries +1 and -1. *Kernel*: a 2 x 2 matrix; its *power* is the
Kronecker product of k copies (the transform is the power of [[1,1],[1,-1]]). *The class*: all powers of invertible kernels that are not
relabellings with scalings. *Textbook*: N log2 N gates (8, 24, 64 at 4, 8, 16 points). Best known tonight: 7, 19 (g-1), 52 (e2-0).
*Merge tree*: start from the N inputs, repeatedly replace two held sums by one weighted sum of them, N - 1 gates; its *nodes* are the
sets of inputs under each sum. *Rectangle*: a set of rows times a set of columns, with one number on it and zero elsewhere.

## 0. In nine lines

1. [ran] g-1's 19-gate circuit is one object read twice: a merge tree on the inputs, and a second merge tree on the OUTPUTS run backwards.
   In matrix words: after flipping the signs of some rows and columns, the 8-point transform is a sum of **13 rectangles** whose row sets
   are nodes of one tree and whose column sets are nodes of another. Gates = N - 2 + (number of rectangles). The 7-gate brick is 5
   rectangles, g-3's Potts matrix is N + 1 rectangles at every N. Section 3, hybrid 1.
2. [ran] **The 19-gate circuit is not about the transform.** The same 19 gates, same wiring shape, compute the third power of every
   kernel I tried: nine kernels besides the transform, six of them with the circuit written out and replayed exactly, among them
   non-symmetric ones. Their textbook is 24. With g-3's result for the 7-gate brick, every saving that has been tested is an identity
   of the whole class. The reason, for kernels with entries t^(Hamming distance): the identity lives in the exponent. There are
   whole-number functions q, q' with distance(x,y) - q(x) - q'(y) equal to -2, 0 or +2 everywhere, and the cells with -2 and +2
   are tiled by twelve rectangles. The transform (t = i) reads this modulo 4. Hybrid 2.
3. [derived + ran] "The transform is a reflection" is not special either: every 2 x 2 kernel times a suitable relabelling with scalings
   has trace zero, so its square is a number (Cayley-Hamilton). Every power in the class is a slanted reflection with a mirror of the
   same dimension 1, 6, 28. What the transform adds is only that the mirror is read and written in the same space. Hybrid 3.
4. [ran] g-1's two trees are exactly g-6's equality case (cosets of a subgroup chain against cosets of the chain of perpendiculars):
   all 49 pairs of nodes have the least rank allowed. g-1 and g-6 found the same configuration from opposite ends. Section 1.
5. [ran, solver] Large constants buy nothing in this count at 8 points: for g-1's design the fewest rectangles is 13 whether the numbers
   on them are bounded by 4, 64 or 1024. At 16 points two designs give exactly 49 rectangles, 63 gates: g-1's heuristic 63 was the
   true minimum of its model there, and one tree pair loses to tensoring. Hybrids 1 and 4.
6. The walls of i-cross: W1 and W2 sharpened, W3 proved but its reading broken, W4 broken in the letter and sharpened in substance,
   W5 proved and extended from "same order" to "same circuits". Section 2.
7. Most surprising: line 2. Most informative question: **is any saving NOT an identity of the class?** Section 4.
8. No change of order anywhere. Every object of the three waves is N log N with a constant between 0.75 and 1.
9. Skeptics first: g-1's 19 (and its count-(O) claim at 512 points), then e2-0's 52 and its 3/4 family, then g-6's floor. Section 5.

## 1. Which facts explain each other

**A. g-1's walk is a merge tree on the outputs, transposed.** [ran, `hyb.py` part 1] Unroll the twelve "walk" gates of the 19-gate
circuit with the thirteen forms they read (the centre and twelve tree forms) as symbols. The 8 x 13 matrix that comes out has columns
supported on nested-or-disjoint sets of outputs, each column proportional to one sign vector a* = (-,+,+,+,+,-,+,+) on its set. That is
the transpose of a merge tree on the outputs. So H_8 = (tree on outputs)^T x (a matching of 13 forms) x (tree on inputs):

    H_8(y,x) = a*(y) c(x) * [ 1 - 2 * (sum of 12 indicator rectangles) ],     c = (+,-,-,-,+,+,-,+) g-1's centre.

Count [derived]: a tree costs N - 1; the transposed tree costs N - 1 + (forms used - N); feeding it costs (rectangles - forms used).
**Total N - 2 + tau**, tau the number of rectangles. Brick: 5, gives 7. g-1: 13, gives 19. Potts matrix (g-3): root plus N diagonal
cells, N + 1, gives 2N - 1. g-1's own formula "2N - 2 + full wires that are not outputs" is the same count. Nobody had written the
transposition; g-1.md does not contain the word.

**B. g-1's trees are g-6's equality case.** [ran, `hyb2.py` part A] Row nodes: cosets of <6> inside the even-weight addresses;
column nodes: cosets of <7> inside <7,1>. Each chain is the chain of perpendiculars of the other. All 49 pairs (row node, column node)
have rank exactly |A||B|/N (or 1 below that), the minimum of g-6's Theorem 1. And [derived] it has to be so: in a sum of tree
rectangles, **rank H[A,B] <= 2 + (rectangles strictly inside A x B)** for every row node A and column node B (rectangles that contain
the block's rows give one common row pattern, those that contain its columns one common column pattern). Trees in the same bit order
would need about N^2/8 rectangles. The "+2" is the "+2" of g-6's Lemma A. Checked on the 13 rectangles: holds on all 49 pairs.

**C. g-3's tree letters are g-6's tree steps.** [derived] A tree letter (entry = a function of the lowest common ancestor, free scalings)
is a sum of rectangles node x node on ONE tree with the same node on both sides; every sibling block has rank one, which is g-6's
definition of a step. So g-3's open case "two letters at 32 points" is g-6's "8 x 4 hatch, 12 exceptions needed, 12 available". One
question, two reports. The rectangle form of A is the mixed case neither wrote: one letter between two DIFFERENT trees with a sparse
middle instead of a diagonal one.

**D. g-1's hub theorem, g-3's wall (a) and the rigidity of the transform are one count.** [derived] Row y of the rescaled transform
agrees with the centre off the union E_y of the column sets of its rectangles. Two rows of the transform agree up to scale on at most
N/2 columns, so |E_y| + |E_y'| >= N/2 for every pair (g-1's "the two partners' supports add to at least N/2"). Summed: the rectangles
other than the root have total area at least N(N-1)/4. So a linear number of rectangles needs rectangles of average area of order N,
the largest a one-signed rectangle of the transform can have (Lindsey's lemma [recalled]). g-1's twelve have areas 2 and 4.

**E. The reflection, the brick and the mirror are one identity of 2 x 2 matrices.** [derived + ran, hybrid 3] For every kernel k with
non-zero off-diagonal entries, k (x) k = (rank one) + det(k) * (a signed swap with scalings b/c and c/b). g-3 had this for symmetric
kernels. Multiply by the swap: det * (identity - 2 * a rank-one projection). Tensor powers: identity minus twice a projection of rank
(N - sqrt N)/2. That is g-0's mirror, i-cross's "key question" object, for every kernel. g-7's "after a half transform the twisted
transform is a relabelling" is the same statement in another basis.

**F. Volume.** g-4 ("the determinant bound is the price of one diagonal"), g-1 wall A (finite alphabets), g-5 ("the limit constant is
gates per bit of determinant of the best brick, over 2"), g-3 ("a shear of coefficient c buys 2 log2(e c) bits"), e2-0 (coefficients
+-1 and +-2 only) are one ledger: each gate with coefficients of size c buys at most about log2 c bits of volume and the transform
needs (N/2) log2 N. Stated once in section 2 as L4.

**G. The extra value.** g-3 (in place on 4 wires: 8 moves modulo 5, 7, 13) and g-7 (no 7-gate in-place program modulo 5 and 7) are the
same experiment run twice with the same answer. In rectangle words [derived]: the middle of the circuit holds tau values, and tau - N =
1, 5 at 4 and 8 points. A program with tau = N is a relabelled textbook-type factorisation. The saving IS the extra values.

**H. Equality in the uncertainty principle.** a-2's tight wires (characters on cosets), g-6's Theorem 1 (least rank exactly for periodic
pairs), g-0's "the shortest relation among mirror points has sqrt N terms", g-7's "sqrt N non-zeros per row for a turn of any order",
e2-1's coset characters with a level: all are "equality holds exactly on subgroup-shaped objects", and all the tying constructions are
built from equality objects only.

## 2. The walls, each once, with who hit it and what happened to W1..W5

**L1. Conjugation (was W1, half and half).** If H = B^-1 (cheap middle) B, then B costs half a transform and B^-1 the other half.
Hit by: d-0, d-3, d-4, d-7 (wave 1); g-7 (4+4, 32+32, 192+192, about 112,000 bases); g-2 (basis change 0.5, 1.0, 1.375 gates per
entry, the middle is extra); g-0 (reading plus writing the mirror plus middle >= 30 at 16 points, because two mirror points are never
perpendicular); g-5 (the recursion closes as t(k) = 4 t(k/4)). **Status: sharpened with exact counts, not proved beyond 4 points.**
New [ran, hybrid 3]: g-0's "never perpendicular" is true for every kernel without a zero entry and false exactly for the subset-sum
kernel, where 7 of 16, 167 of 256, 3,319 of 4,096 entries of the mirror matrix are zero.

**L2. Copies do not share (was W2).** Hit by: d-2, d-6 (wave 1); e2-2 (the batch discount measured), j-manyatonce (exchange rate
z = log2(1 + theta); no discount in depth two or without cancellation [read there]); g-5 (two copies of K3 cost exactly 8 modulo 3, 5,
7); g-6 (two tree steps in the periodic shape: every block is the smaller transform plus one rank-one term, and nesting removes the
term); g-7 (a discount 0.933 at every squaring would be a saving of 1e-1). **Status: sharpened; first exact instance; not broken.**
e2-0's 3/4 family is not a break: it computes each character on one half only and pays hubs, a constant.

**L3. Equality objects cost N log N (was W3, tight wires).** Proved by a-2, refereed by g-1, which added the output-side ledger and
wall B (product vectors with any entries still tie). **Status: proved as a statement about programs of tight wires. Its reading in
i-cross, "the winning wire wins because it is flat on both sides, an eigenvector of the transform", is broken three times**: g-3 (the
brick exists for every kernel, flat or not; the Potts matrix is flat on both sides and linear), g-1 (in the 19 the over-spread wires
serve two gates each, there is no hub), and line 2 above (the 19 exists for kernels that have no flat eigenvector at all).

**L4. Volume (was W4, exactness).** Bounded coefficients force c N log N. **Status: "nobody has an example of badly conditioned steps
with a perfectly conditioned product" is false in the letter** (g-3: (B1 + cJ)(B2 - c/(1+8c) J) = B1 B2), **and true in every case
looked at**: the bad conditioning was a rank-one term added and removed (g-3); in place at 4 points coefficient size buys nothing
(g-3); in the rectangle count at 8 points constants up to 1024 buy nothing (hybrid 4). Sharpened by g-4: all of the volume sits in one
diagonal of H = Z D Z^T, and the proved floor for the two shears alone is N sqrt(log N).

**L5. One class (was W5).** **Status: proved for the word** (g-4: subset sums = three calls of the transform at every k, and three is
least) **and extended**: g-3 (the 7-gate brick is an identity of every symmetric kernel), hybrid 3 (of every kernel with non-zero
off-diagonal entries), hybrid 2 (the 19-gate circuit too), g-5 (K3 is the transform on symmetric data, circular). It is now "same
circuits at 4 and 8 points", not only "same order".

**New in wave 3, not in i-cross.** L6, the extra value (G above; g-3, g-7). L7, two periodic steps stop at 32 points (g-6; hand counts).
L8, one letter needs dual trees (B above; mine, derived tonight, seen by nobody).

## 3. Four hybrids, each tried

### Hybrid 1. "Two hierarchies": g-1's walk + the transposition principle (e-1 used it) + g-3's tree letters + g-6's Theorem 1

Idea: stop describing g-1's circuit as a walk. It is the transform written as few rectangles over two trees; count rectangles.
Tried [ran, `hyb.py` part 1, `hyb2.py` part A]: the facts A and B of section 1, exactly, at 4 and 8 points. Then a sweep at 16 points
[ran, solver, `rect.py` on the Linux machine]: for centres c that are sign vectors of a bent quadratic form, a* its transform, and the
315 chains with their perpendicular chains, the solution of least sum of |numbers| was computed and its rectangles counted.
The sweep's best was 53 rectangles (6,122 of the 141,120 designs tried in 13 minutes, in random order; most gave 56 to 62). The proxy is weak: at 8 points it returns 24
rectangles where the true minimum is 13, so the sweep only ranks designs.
[derived, not run] For a bent centre the rescaled transform is J - 2E with E(y,x) = 1 when Q(x + Ly) = 1 (Q the quadratic form, L a
fixed linear map): at 16 points E is 6 translations, 96 cells; at 8 points my run counts 32 cells, and g-1's twelve rectangles cover
them exactly once (areas 4+4+2+2+2+2+2+2+2+2+4+4 = 32). So tau - 1 is "the fewest tree rectangles tiling the set where a quadratic
form of x + Ly is 1". This is e-0's ring and e-6's shift picture meeting g-1's circuit.
Then the true minimum for two of those designs [ran, solver, `rect2.py`]: **49 rectangles, both times** (the solver's lower bound
meets its best solution, 44 and 61 seconds), so 63 gates. That is g-1's figure "63 at best over 869 designs" to the gate, from a
different tool. The 49 are: the root; 16 rectangles (4 rows x 1 column); 16 rectangles (1 row x 4 columns); and 16 single cells with
the number +4 that repair double covering. So in this family the count per point is (tau - 1)/N = 1, 1.5, 3 at 4, 8, 16 points:
it grows faster than log N. One letter loses to tensoring (54) and to e2-0 (52) at 16 points. The single cells are new at 16 points:
at 8 the twelve rectangles tile without overlap, at 16 a tiling by the same shapes does not exist for these designs.
Where it stops: with sign scalings the constants are bounded, so L4 gives tau >= about 0.3 N log N. One letter of this kind cannot be
linear; it is a way to count, and a constant.

### Hybrid 2. "Nineteen for everybody": W5's class + g-3's census of the brick + g-1's circuit

Idea: g-3 showed the 7-gate brick does not use unitarity. Ask the same of the 19.
Tried [ran, `hyb3.py`, `hyb4.py`, circuits in `k-cross/class19.txt`]. Fix the 13-rectangle shape. For a kernel power K, run over all
8! input wirings and all output labellings; necessary conditions first (pairs of rows proportional on prescribed sets), then the full
exact test (solve for the two scaling vectors and the twelve numbers).
- The transform (control): 10,752 placements pass. 10,752 = 168 x 64 is the order of the transform's own symmetry group [guess: one
  solution up to symmetry].
- Kernels with entries t^(Hamming distance), t = 2, 3, 1/2, -2, 5; [[1,2],[3,4]]; [[1,2],[2,3]]: **288 placements pass, each time.**
- Written out and replayed on all 8 basis vectors with exact fractions, 19 gates each, every output a non-zero multiple of the right
  row: [[1,2],[2,1]], [[1,3],[3,1]], [[1,2],[3,4]], [[1,2],[2,3]], [[2,7],[5,3]], [[1,100],[1,1]], and the transform.
  For [[1,2],[2,1]] the constants are 2, 4, 8, 3, 6, 3/4.
So at 8 points the third power of a kernel with no zero entry costs at most 19, against its textbook 24 (two gates per 2 x 2 block)
and 22 by g-3's brick. [guess: for every such kernel; the conditions are polynomial identities and held at nine unrelated points.]
A correction to my own first run: with the input wiring of g-1's file no output labelling passes for t = 2 (0 of 40,320); the generic
kernel needs the pairing by the top address bit, not by the complement. I nearly reported "special to the transform" from that.
**Why it holds: read it in the exponent.** [ran, `expo.py`, t = 2 and t = 3, one placement] Write the centre as t^q(x) and the row
scalings as t^q'(y). The whole numbers q (1,2,2,1,0,1,3,2 over the columns) and q' (-1,0,0,1,0,1,-1,0 over the rows) are the same for
t = 2 and t = 3, and

    Hamming distance(x,y) = q(x) + q'(y) + m(x,y),    m = 0 on 32 cells, +2 on 16 cells, -2 on 16 cells.

The twelve rectangles tile the 32 cells where m is not 0, and m is constant on each. So for every t the kernel power is
(rank one) x [1 + (t^2 - 1) on six rectangles + (t^-2 - 1) on six rectangles]: no linear algebra, a fact about distances on the cube.
In the three written circuits every constant is the determinant times a monomial in the kernel's entries [ran, three kernels], as in
the brick identity. For the transform t = i, so t^2 = t^-2 = -1: the two kinds of cell become one kind, and q, q' matter only modulo 4.
**That is the exact difference between the transform and the rest of the class: the class must tile m as a whole number, the transform
only m modulo 4.** d-3's "weight modulo 4" is this freedom. At 8 points the freedom buys nothing (12 rectangles either way); it shows
only in the number of placements, 10,752 against 288.
Where it stops: it is a constant, like everything. What it changes is what may be assumed, and what to search (section 4).

### Hybrid 3. "The mirror without unitarity": g-0's mirror + g-3's brick identity + one line of 2 x 2 algebra

Idea: g-0 ended on "which matrices have mirror points that CAN be perpendicular? For those the same count would go below."
Tried [ran, `hyb.py` parts 2 and 3, `hyb2.py` parts B and C]:
- k (x) k - det * (scaled swap) has rank one for 300 random rational kernels, symmetric or not.
- (kernel x a diagonal chosen to make the trace zero)^2 is a multiple of the identity, 200 random kernels.
- Rank of (kernel power x relabelling - number): 1, 6, 28 at 4, 16, 64 points for the transform, [[1,2],[2,3]], [[1,2],[2,1]],
  [[2,1],[1,3]]. I had predicted 7 and 37 for the non-unitary ones by hand; the run corrected me, and the reason is the trace.
- Zero entries of that matrix: none for the four kernels above; 7 of 16, 167 of 256, 3,319 of 4,096 for [[1,1],[1,0]] (subset sums up
  to relabelling). [derived] A zero needs a zero entry in the kernel.
Reading: the mirror, its dimension and g-0's obstruction belong to the class. The one member where the obstruction is absent is subset
sums, whose textbook is already half (4, 12, 32) and where d-0 found no gain at 4 and 8 points. At 16 points a mirror route costs at
least N + 2(N - r) = 36 > 32 there, so it cannot help before 64 points [derived, rough].

### Hybrid 4. "Large constants in a count that has Potts in it": g-3's question + W4 + the rectangle count

Idea: the Potts matrix is the only flat matrix of the night with linear size, and it gets there with one number of size N on N + 1
rectangles. So in this count large numbers are known to pay for SOME matrix. Do they pay for the transform at 8 points?
Tried [ran, solver, `rect.py`, first block of `rect.out`]: g-1's two trees and sign vectors, all 225 rectangles node x node allowed,
fewest rectangles with numbers bounded by 4, by 64, by 1024: **13, 13, 13** (HiGHS reports optimal each time; the 1024 run returns a
different 13 from the other two). So for this design 13 is the minimum, and size buys nothing.
Limits: one design (trees and sign vectors fixed); a floating-point integer programme, not a proof; row and column scalings were
signs, not free numbers.

## 4. The most surprising thing, and the question that would tell the most

**Surprise.** The best 8-point circuit of the night computes the third power of [[1,2],[3,4]] as well as it computes the transform.
Three waves looked for what is special about the transform (reflection, eigenvectors, Clifford group, weight modulo 4, 27 lines,
equiangular lines, E8), and the two things that actually save gates, the brick and the 19, use none of it. Even "it is a reflection"
is a property of 2 x 2 matrices of trace zero.

**Question. Is any saving NOT an identity of the class?** In the form hybrid 2 gives it: **does tiling "distance minus q minus q'"
modulo 4 ever need fewer rectangles than tiling it as a whole number?**
Why it tells the most. If the answer is no, the special structure of the transform (reflection, Clifford group, weight modulo 4, E8)
is a description and not a lever; the search may move to whichever member of the class is easiest to search or has the weakest proved
floor; and the savings are facts about distances on the cube, for which one can look for a rule in k instead of a search at each size.
If the answer is yes at some size, that is the first lever the transform's own structure has given, and it says where: in cells that
differ by 4 in the exponent.
Experiment (exact, small, startable now), in two parts.
(a) At 16 points, the fewest rectangles for the kernel with t = 2 (tool: `rect2.py` with the target replaced by the kernel power and
the scalings t^q, t^q' searched over quadratic whole-number q; `expo.py` shows how to read q off a solution), against the 49 found for
the transform. Fewer than 49 for the transform's best design than for any whole-number design is a "yes".
(b) Take the gate lists of e2-0's 20 at 8 points and 52 at 16 points and of g-5's 12 for K3 (x) H2, keep the wiring, free every
coefficient, and solve for t = 2, 3 and for [[1,2],[3,4]] as in `hyb3.py`. e2-0's family rests on a "mixed-hub lemma"; if the lemma
holds for every kernel the 3/4 rate is a class rate too.

## 5. Three objects for a skeptic, in this order

1. **g-1: 8 points in 19 gates (claims to beat the best known 20, 21, 22).** Exactly: count (G); circuit in
   `g-1-tightwires/h8_19gates.txt`; every output with factor 1; by tensoring 54 at 16 points and 304 at 64. Count (O): H_8 x / 2 in 20
   operations, and "H_512 x in 4352 against 4608", where the 512 final multiplications are counted, not run. Attack the count-(O)
   line first: does OpenAI's model in R/OAI charge what g-1 charges, and is 4608 the right comparison. Then "19 is the exact minimum
   of the one-tree model" (a dynamic programme; my solver run agrees for one design only). Attached, mine and unreviewed: the same
   circuit for other kernels, `k-cross/class19.txt`.
2. **e2-0: 16 points in 52 gates and T(N) <= (3/4) N log2 N + N/4 (claims to beat 56 and the 7/8 rate).** Exactly: explicit programs
   at 4 to 64 points with coefficients +-1, +-2, replayed by two programs; the general statement is [derived] from the mixed-hub
   lemma and a sign rule, [ran] for k = 2..6 only; count (O): the orthonormal 16-point transform in 60. No critic has seen it (the
   a- reports predate it). Attack the induction for k > 6 and the count-(O) normalisation.
3. **g-6: two tree steps of the periodic shape do not make the transform from 64 points on.** Exactly: Theorem 1 (checked
   exhaustively at 8 and 16 points) is solid; the floor rests on the block law (only its first line was run) and on hand counts for
   trees with 16 and 32 leaves. It also says the 32-point case is exactly tight (12 = 12). It is the only impossibility claim of the
   wave that bears on a growth law, and the weakest in evidence.

## 6. Eight experiments for the next wave

Deepen what is alive:

1. **classtest** (deepens g-1, e2-0, g-5). Are e2-0's 20 and 52 and g-5's 12 identities of the class? Brief: section 4 (b). Inputs:
   `e2-0-pieces/slp_8.txt`, `slp_16.txt`, `g-5-k3/brick12.py`; templates `k-cross/hyb3.py`, `hyb4.py`, `expo.py`. Output per circuit:
   the number of placements that pass for t = 2, 3 and [[1,2],[3,4]], one replayed circuit or the first gate that fails, and, if it
   passes, its exponent reading (q, q', the values of m). Count (G).
2. **mirror64class** (deepens g-0). g-0's growth law on the member where its obstruction is absent. Brief: for the subset-sum
   kernel the mirror matrix is mostly zeros (hybrid 3: 167 of 256, 3,319 of 4,096). Run g-0's `search.c` on that kernel's 16 mirror
   points, then 64, and compare with that kernel's textbook 32 and 192. This is g-0's last mutation with the matrix now named.
3. **hatch32** (deepens g-6 and g-3, which ask the same thing). Decide the 8 x 4 hatch at 32 points. Brief: with the structure of g-6
   section 4 fixed the unknowns are scalings; solve modulo two primes with an analytic Jacobian, lift, replay exactly. Use the rank
   test of section 1 B as a filter before any solver starts. Empty: two periodic steps stop at 16 points. Non-empty: the first word
   shorter than k/2 steps.

Nobody has tried:

4. **exponent** (section 4 (a)). Search in the exponent, with no linear algebra. Brief: at 16, 32 and 64 points, choose whole-number
   quadratic functions q, q' and two hierarchies, and tile the cells where distance - q - q' is not 0 by rectangles on which it is
   constant; count rectangles, once as whole numbers and once modulo 4. This is a combinatorial search that reaches sizes where gate
   searches cannot. Gates = N - 2 + rectangles. Report the count per point at each size for both versions.
5. **unimodular**. The member with no determinant floor. Brief: K = [[1,1],[1,2]] = Z Z^T (determinant 1, no zero entry). Exact
   minimum at 4 points with coefficients +-1 only (d-0's mincirc), then 8; the singular-value floor for its powers as g-4 did for Z.
   The question: is a bounded-coefficient family for this member forced to N log N by anything proved? If not, it is the member on
   which a slower growth could first be seen without large coefficients.
6. **selftranspose**. Circuits of the form F^T M F. Brief: the transform is symmetric, so if H = F^T M F with M a relabelling with
   scalings on N' forms and F costing c gates, transposition gives 2c + N' - N. The brick is F = (hub, x0..x3), c = 3, N' = 5: 7.
   At 8 points, over merge trees F (c = 7): is the quadratic form x^T H x a combination of squares and of products of DISJOINT pairs
   of at most 12 of the 15 tree forms? Twelve gives 18 gates. One exact linear solve per tree and matching.

One hybrid:

7. **twoletters** (g-3's letters x g-6's steps x g-1's walk). Products of two rectangle forms. Brief: H_16 = L1 L2, each factor a
   sum of rectangles over its own pair of trees. Brick layers are the case 20 + 20 rectangles, 56 gates; one letter is 49 rectangles,
   63 gates (hybrid 1). Minimise rectangles(L1) + rectangles(L2), with g-6's test (nu at most 4 for every pair of nodes) and the rank
   lemma of 1 B as filters, starting from the brick layers and from e2-0's 52 read as letters. First step, cheap: one letter at 16
   points outside the family I ran (centres that are not bent, chains perpendicular at some levels only) with `rect2.py`.

One that sounds silly:

8. **let t be a letter.** Run the 19-gate circuit with t as an unknown instead of a number. It then computes, for 8 points, a
   polynomial in t at every output whose coefficients are the sums of the data over all points at distance 0, 1, 2, 3: all sphere
   sums around all points at once. Brief: count the scalar operations of that polynomial circuit and compare with computing the
   sphere sums one radius at a time; then ask the reverse, whether the transform is cheaper as "all sphere sums, then one weighted
   sum per point" (k + 1 numbers per point, weights i^d) than directly. It sounds like paying more to get more; the exponent reading
   says the circuit never used the value of t.
   (My first silly one died in the box: 5 and 13 rectangles are Fibonacci numbers, so 34 at 16 points; the run says 49.)

## 7. Criticism, last

- Everything in hybrids 1 and 4 at 16 points is a floating-point integer programme on two designs (and a weak proxy on the rest).
  "49" is the solver's certified optimum for those two designs with numbers bounded by 4; it was not replayed exactly and says
  nothing about other designs or larger numbers.
- "The 19 holds for the whole class" is nine kernels and a guess. The exponent reading explains it for the kernels t^(Hamming
  distance) (checked at t = 2 and 3, one placement of 288); for non-symmetric kernels I have the circuits and no explanation.
  I did not test kernels with complex entries or the limit towards a zero entry beyond [[1,100],[1,1]].
- The rank lemma of 1 B and the area count of 1 D are a few lines each, derived in the box, checked on one circuit.
- 1 C (tree letters = tree steps) is from the two reports' definitions as summarised to me, not from reading both in full.
- "Every saving tested is a class identity" covers two savings: 7 and 19. e2-0's 20 and 52 are untested; that is experiment 1.
- I read the wave-2 reports' first pages only, and no literature. Whether "19 gates for the third power of a generic 2 x 2 kernel"
  or the rectangle count is known, I do not know.
- None of this changes the order. The honest state after three waves: three constants (7/8, 19/24, 3/4), all with bounded
  coefficients, all (where tested) identities of 2 x 2 matrices, and no example yet of a large coefficient saving a gate for the
  transform at any size.

Files: `waves/wave-03/k-cross/` : hyb.py, hyb.out (rectangle form; brick for all kernels;
mirror ranks); hyb2.py, hyb2.out (rank lemma on g-1's trees; trace zero; zeros of the mirror matrix; necessary conditions over all
wirings); hyb3.py, hyb3.out (full exact test, eight kernels); hyb4.py, hyb4.out, class19.txt (seven 19-gate circuits, replayed);
expo.py, expo.out (the identity in the exponent); rect.py, rect.out, rect2.py, rect2.out (solver runs on the Linux machine, copied back).
