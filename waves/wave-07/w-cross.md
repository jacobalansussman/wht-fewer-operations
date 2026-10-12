# w-cross: the seven waves side by side, four hybrids tried, and what to ask next

> Editor's note (11 October 2026): later reports corrected three statements that this report carries. The ceiling 0.098 at r = h/3 covers one sub-class only ([z-1](z-1.md)). That an exchange cuts each array into "at least three blocks" is not a floor: programs that pass the engine's rules have two ([ab-1](../wave-08/ab-1.md), [ab-6](../wave-08/ab-6.md)). And "two blocks with 7.4 % skipped" is the worst way to have two blocks: one big block plus single moves needs 1.4 % at block size 45 (line 10, "Corrections", in [the eighth note](../wave-08/NOTE.md)).

11 October 2026, 04:23 to about 05:00 EDT, 40-minute box. Private. One agent; nothing reviewed, nothing in Lean, nothing published.
Marks: [ran] = run of mine tonight (files in `w-cross/`, whole numbers or Gaussian whole numbers, no floats); [derived] = by hand
tonight, checked by nobody; [read] = from tonight's reports; [recalled] = from memory, no source read; [guess].
Gate count everywhere: **(G)**, a gate is any a*u + b*v, scalings free. Count (O), OpenAI's, is not used.
Read: s-cross in full; the first five sections of WAVE6-NOTE; the four wall statements of j-cross; the ten wave-7 results as
handed to me (their reports not in full); two lines of d-0. I did not read the wave-7 reports themselves, the skeptics' files
v-*, nor waves 1 to 5 again. That is a limit of everything below.

**No circuit below a known count, and no growth law below N log N. Nothing here changes the order.**

Words. N = 2^k points; an *address* is k bits; x.y is the number of common ones of two addresses modulo 2. *The transform*: H,
entries (-1)^(x.y). *Textbook*: N log2 N gates. T(N): the least number of gates for the transform, relabelling and scaling of
inputs and outputs free. *Subset sums*: the matrix Z; H = Z D Z^T with D a diagonal of powers of -2; *Yates*: (N/2) log2 N gates
for Z. *Wire*: a value the program holds, a vector over the inputs. *Height* of a wire: its largest entry once scaled to whole
numbers with no common factor. *Sign vector*: a wire of height 1. *Neighbour sums*: every address gets the sum of the inputs at
its k neighbours (addresses that differ in one bit); matrix A. *Convolution with q*: output(y) = sum over x of q(x + y) input(x),
addresses added bit by bit modulo 2. *Port* (x-6): a direction along which the transform splits off one move.
*Class*: all k-th tensor powers of 2 x 2 kernels [[1,1],[1,s]] (k-cross); the transform is s = -1.

## 0. In ten lines

1. **Wave 7 hit three walls, each several times, and one door.** Section 2 states each once: HEIGHT (x-0, x-2, x-8, x-9, x-3,
   x-5), COSTS ADD (x-4, x-7, x-5, x-3), DISTANCE (x-9, x-2, x-1, x-7, x-4, x-8), and the door PORTS (x-6, x-3, the tiny-unit
   cut-set lemma).
2. **Height is necessary and not sufficient.** x-0 and x-2 derived the same bound independently (budget table 3, 8, 21 for
   entries up to 1, 2, 3): wires of height at most M cost about (N log2 N)/(4 log2 M + 4) gates. x-5's tower and x-9's hubs
   HAVE the height (budget (k/4) log2 k per point; coefficients up to 65537) and still cost k passes, or more than the
   textbook. So the volume count is not the wall that holds; it is only the first one a linear circuit must pass.
3. [derived + ran, hybrid 2] **"The cheapest basis" is the transform at half price, exactly.** For every V with V H V^T
   diagonal, T(N) <= 2 cost(V); and one such V costs sqrt(N) T(sqrt N) + N - sqrt(N). So i-cross's key question, x-5's first
   mutation and x-8's first mutation are one question, and it is the original one. Not a separate door.
4. [ran, hybrid 3] **x-6's port counts are the counts of the subspaces P of the address space that meet their perpendicular
   only in 0**: 2^(h-1) of dimension 1; 20 and 80 of dimension 2 at h = 4, 5 (x-6's numbers); 336 and 640 of dimensions 2
   and 3 at h = 6. (I matched counts and proved the splitting; I did not read x-6's definition in its program.)
   The transform splits along every such P; other kernels split only along coordinates. That is the one property of the night
   that is not an identity of the class, and three reports found it from three sides.
5. [derived + ran, hybrid 1] **The transform is one function of the neighbour-sum operator**: product of (1 - i X_j) =
   (-i)^distance = a multiple of exp(-i (pi/4) A), and with free signs and a free relabelling H is the convolution with
   q(z) = +,+,-,-,+,+,... by weight. Hence T(N) <= max over q of cost(convolution with q) <= 2 T(N): the transform is the
   hardest convolution on the cube, and neighbour sums are the simplest one that nobody can do in O(N).
6. [ran, hybrid 4] A walk by two-column moves through the whole-number bases that diagonalise H reaches 108 of them at 4
   points (with the same four sign patterns of the diagonal that x-8 found by enumeration) and 32,191 at 8 points within
   five moves. None is sparser than Z.
7. Old walls: j-cross M sharpened twice (bounded wires, not bounded coefficients); S proved in three more classes; C run at
   last and relaxed from k/2 to about k / log2 k passes; U confirmed from the M side. k-cross's "identity of the class" has its
   exact boundary now. Section 2.
8. Most surprising: the only order-changing mechanism has a growth law that counts blocks, and on paper it tops out near 0.1,
   the standing bar (x-6). Section 4.
9. Most informative question: **are neighbour sums on the cube possible in O(N) gates?** Necessary for a linear transform,
   needs almost no volume (about (N/2) log2 k units), and every count known grows like k N. First datum [ran]: at 16 points
   one half of the matrix (8 outputs) has no circuit with 14 gates modulo 2, 13 modulo 3, 12 modulo 5; pairing gives 16.
   Section 4.
10. Skeptics first: the height lemmas (x-0 lemma 3, x-2, x-8's bridge); x-6's growth law and its caps; x-4's lemma D with
    x-9's class floor. Section 5.

## 1. Facts that explain each other

**A. One bound, two authors, one meter.** [read; the match is mine] x-0 lemma 2 (largest (|a|+|b|)/g is 3, 8, 21, 43, 73, 157
for entries up to 1, 2, 3, 4, 5, 7; at most 4 M^2) and x-2's sixth and seventh lines (3, 8, 21; gates >= (N/2) log2 N /
(2 + 2 log2 M)) are the same count. x-8's bridge (entropy at an orthogonal landing <= 2 log2 |det|; in place the determinant is
multiplied by a/g only) says the entropy meter of wave 5 reads the same quantity. x-3's priced glue (b) (about log K binary
digits per glue gate) and s-cross's ledger are it again. Five reports, one number.

**B. Height without profit.** [read] x-5: the tower of couplings carries about (k/4) log2 k units of volume per point from
k = 8 on, more than the k/2 the transform needs, and is still k passes. x-9: hubs with coefficient t = 2^j or 2^(2^(j-1)) cost
(5/4) N log2 N, more than the textbook; "the volume ledger's budget is spent without volume". x-0: at 4 points (exhaustive) and
8 points (sampled) tall wires and gates of more than one unit appear one gate above the floor, never at it. Together: tall
wires are required in the long run (A) and unprofitable wherever anyone has built them. What a tall wire that pays looks like
is not known from any small case.

**C. Why a tall wire does not pay near an output.** [read: x-9 lemma A; the link is mine] A wire can be one gate from an
output with a small witness only if it is a sign vector off the witness. So tall wires sit in the middle of a circuit, and the
last gate into an output has two operands that both cover everything ("two hubs, no small partner", x-9's open hatch).
The one specimen of that shape is the second pass of Z D Z^T: gates u + v between wires of height up to N/2. It exists, at
exactly N log2 N [read: u-4]. So x-0's requirement and x-9's hatch are met by the same known object, and its whole cost is the
two passes of Z, where the determinant is 1 and no meter reads anything (x-8).

**D. Three reports arrive at one family.** [read + derived] x-5 (H = N V^T D^-1 V for every V with V H V^T diagonal), x-8 (whole
-number A of determinant 1 with A D A^T = H; H = Z D Z^T is the Smith normal form) and i-cross's key question (the cheapest
basis of the mirror; g-0: 24 gates at 16 points) are the same family. Hybrid 2 prices it from both sides. x-7's two-line lemma
(two mirrors cost at least T(N), and the free pair costs exactly T(N)) is the same kind of statement: a reformulation that
contains the trivial member is a place to search, never a mechanism.

**E. x-4's "the coupling U is the identity" is the tensor split.** [derived] With H' the transform in the pairing of the
quadric, F the half transform and S the exchange of the two half-addresses, x-4's result is H' = F S F, that is
H = (H_s on the first half)(H_s on the second half). s-cross's 60-degree picture, g-7's third turn and x-7's stabilizer triples
(j1 + j2 >= k always) are this one cut of the address bits. That is why the weights add up to exactly 1.

**F. Three names for one symmetry.** [ran, hybrid 3; read] x-6: the transform has 2^(h-1) ports, every other kernel h.
x-3: the family "a box known only up to an address map" is the only one where the call bound stays a constant factor under
2K (1.5 K), with an exact 7-call program at K = 4. The tiny-unit cut-set lemma (cutf3): without address maps no unit saves a
move at block size 3. u-5 and m-cross: the published unit breaks "one merge tree" first. All four say: the saving that changed
the order uses the freedom to change the frame of the address space, which the transform has (every invertible bit matrix is
a relabelling of its inputs and outputs) and no other member of the class has.

**G. Digits are levels.** [derived] x-1's digit j of H is the part of Z D Z^T that passes through the sets of size j (rank
C(k, j), factor (-2)^j). Its law "digit j costs N [P(Bin >= j) + P(Bin >= j+1)]" is Yates cut by level, and "the bottom d
digits are the transform at its lightest outputs" is the statement that Z is triangular. x-1's "identities of the whole class"
is then no surprise: the level cut exists for every s (factor (s - 1)^j).

**H. The transform as a walk.** [ran, hybrid 1] The given fact "entries (-i)^(Hamming distance)" is exp(-i (pi/4) A) with A the
neighbour sums. Every member exp(-i t A) is a tensor power of one 2 x 2 kernel, so it is in the class and the 19-gate circuit
computes it; t = pi/4 is where ports appear (F), and t = pi/2 is a free relabelling (every address to its opposite). x-5's
"a linear transform forces neighbour sums into O(N)" and x-7's "quadric translates" are two corollaries of the same picture.

**I. One distance, six reports.** Section 2, wall DISTANCE.

## 2. The walls, each once

**HEIGHT (j-cross M, i-cross W4, s-cross L4).** *Lemma. A circuit for H whose wires all have height at most M has at least
N - 1 + ((N/2) log2 N - (N - 1) log2 M) / log2(4 M^2) gates, with any coefficients.* Who hit it: x-0 (lemmas 1 to 3), x-2
(wall 1), x-8 (bridge lemma, for orthogonal landings in whole numbers), x-3 (glue with bounded coefficients needs 2K calls in
the limit), x-9 (a growing coefficient is spent without volume), x-5 (the count is passed and nothing is gained).
Status: **sharpened**. j-cross M said "bounded coefficients"; it now says "bounded wires", which is weaker as a hypothesis
(coefficients may be anything) and covers every pool the night has searched. Derived twice, unreviewed. Consequence: C N gates
need a constant fraction of gates on wires of height about N^(1/(4C)). Not sufficient (fact B). Asymptotic only: it excludes a
saving of 0.1 only for log2 N near 100,000 (x-2).

**COSTS ADD (j-cross S and C; WAVE6-NOTE L1 "half and half" and L2 "copies do not share").** *Lemma. Every route of the form
"change of basis, something free, change of basis back" or "stage on some address bits, stage on the others" costs at least
T(N) in all, and the member that is free on one side costs exactly T(N).* Who hit it: x-7 (pairs of mirrors; stabilizer pairs
are cuts of the address bits), x-4 (the 120-degree split is two half transforms), x-5 (every bracketing of couplings costs the
same N (k - E[d])), x-3 (any family with two boxes differing by rank 1 or 2 needs 2K - O(1) calls), hybrid 2 here.
Status of **S**: proved in three more classes (continuous families of boxes; stabilizer pairs; trees of couplings with dense
blocks), each by hand, unreviewed. Open where the box has discrete relations: the address maps (1.5 K).
Status of **C**: its hatch "alternate two kinds of step that do not commute" was never run before wave 7. x-4 ran it: passes
of flag kernels with free diagonals in between need at least k/2 passes without the diagonals (lemma A) and at least about
k / log2 k with them (lemma D). Relaxed, not broken: N log N / log log N at best in that model. Not covered: trees that are
not coset trees.

**DISTANCE (j-cross U).** *Lemma. Two different rows of H differ on exactly N/2 points; more generally a non-zero combination
of the evaluations of polynomials of degree d at cube points has at least 2^(d+1) terms. Hence: a wire is one gate from n
outputs only with witnesses of at least (N/2)(1 - 1/sqrt n) points; in every cut the rows pair up and N/2 + 1 gates are new on
neither half; from the third digit on a helper serves one output; supports of two mirrors multiply to N.* Who hit it: x-9
(lemmas A, S, P), x-2 (E >= N/2 + 1), x-1 (no three cube points on a line; dependencies of 2^(d+1) terms), x-7 (supports
multiply, so costs add), x-4 (support sqrt N is least for a fixed vector), x-8 (a flat unitary matrix is rank (N - sqrt N)/2
from every signed relabelling). [derived: the match] These are the minimum distances of the Reed-Muller codes, read on wires.
Status of **U**: confirmed from the other side. j-cross wrote "breaking M without breaking U is worthless"; x-9 measured it
(rate 5/4 against 3/4). Not broken by any small circuit.

**The door: PORTS.** Not a wall. Fact F and hybrid 3. Its own ceiling (x-6): with one-dimensional ports the design is flat in
h; with fat ports the engine's accounting caps the saving at 0.078 to 0.147 on paper. And x-2: sign vectors on crossing sets
still pay 0.315 N log2 N, so frames without height cannot change the order.

**k-cross, status.** "Every saving tested so far is an identity of the whole class": extended by x-1 (the circuits congruent
to H modulo 2^(d+1) are identities of the class too; s-cross's guess that the modulo-4 object is special to the prime 2 is
wrong) and given its boundary by x-6 (the published saving is not one). The rectangle count: untouched in wave 7.
"A reflection is a property of the class": x-3 adds that the relation which shares calls at K = 2 is A A^T = 1, not
reflection, and that it is worth at most 3 calls at every size.

**What no wall covers, after seven waves.** A circuit that has, all at once: wires of height like a power of N in the middle;
last gates between two such wires; in every one of its N - 1 cuts about N/2 gates that are new on both halves (x-2); frames
that cross. The second pass of Z D Z^T has the first two properties; the published unit has the last.

## 3. Four hybrids, each tried

### Hybrid 1. The hardest convolution (x-5's neighbour sums x x-4's quadric identity x x-7's quadric translates x "(-i)^distance" x k-cross's class)

Idea. x-5 found that a linear transform would force neighbour sums into O(N). x-4 found H(x,y) = q(x) q(x+y) q(y) for the signs
q of a quadric. Put them together and ask which convolution the transform is, and whether it is one of many.
Tried [ran, `hyb.py`, `hyb.out`; k = 2 to 6, all entries, Gaussian whole numbers]:
- product over the k bits of (1 - i X_j) = the matrix of (-i)^(distance), X_j being "flip bit j". True for k = 2..6. Since
  (1 - i X)/sqrt 2 = exp(-i (pi/4) X) and A = X_1 + ... + X_k, this matrix is 2^(k/2) exp(-i (pi/4) A).
- with q(z) = +1 for weight 0 or 1 modulo 4 and -1 for weight 2 or 3 (the signs of the symmetric quadric, "choose 2 of the
  ones"): H(x, M y) = q(x) q(x+y) q(y) with M the bit matrix "all ones minus identity". True for k = 2..6; M is a relabelling
  when k is even. So for even k the transform is, up to free signs and a free relabelling, the convolution with q.
- q depends on the weight only, so this convolution is a polynomial in A. Its degree is exactly k for k = 2..6, and its
  spectrum is flat (all values +-2^(k/2), by weight: -8,-8,8,8,-8,-8,8 at 64 points).
Lemma [derived]. Let c(q) be the least number of gates for the convolution with q. Then c(q) <= 2 T(N) for every q
(transform, scale, transform back; the scaling is free in count (G)), and T(N) <= c(q) for the q above. So **T(N) <= max over q of c(q) <= 2 T(N)**: a linear
transform exists exactly when every convolution on the cube is linear.
What it gives. (i) A ladder of necessary conditions, from easy to hard: sums over a subspace (linear, known), neighbour sums
(the generator; d-0 priced it at 12 gates at 8 points, exhaustive modulo 2, 3, 5 [read]; by pairing 2N at 16 points; x-5's
hand count (3/4) k N), sums over a ball of radius 2, x-1's "lightest outputs" (the convolution whose spectrum is 1 on weights
up to d and 0 above), and at the top the transform itself. (ii) [derived] A program that uses neighbour sums as a sealed box
needs k calls: the polynomial has degree k and A has k + 1 different eigenvalues. This is x-3's sealed-box lemma and x-4's
"k/2 passes" for a third kind of box. (iii) [derived, rough] Neighbour sums need almost no volume: the eigenvalues of A are
k - 2w, typically of size sqrt k, so about (N/2) log2 k units. For neighbour sums the height wall asks nothing that grows
with N faster than log log N. Whatever makes them cost k N is not volume.
Where it stops: no circuit. I priced nothing new; the statement is an equivalence and a list.

### Hybrid 2. The cheapest basis is half a transform (x-5's family x x-8's Smith form x x-4's half transform x i-cross's key question)

Idea. Two reports of this wave end on "search the family of all V with V H V^T diagonal for a cheap member". x-4 has, without
saying so, a member: the half transform followed by sums and differences of exchanged pairs.
Tried [ran, `hyb.py`, `hyb.out`, 4, 16, 64 points, all entries]: write an address as (a, b), two halves. H' is the transform
with the two halves of the output address exchanged (a free relabelling). F is the transform on the first half only. B replaces
the two values at (a, b) and (b, a), a < b, by their sum and difference. V = B F. Then V H' V^T is diagonal (values N, 2N, -2N)
and H' = N V^T (that diagonal)^-1 V, exactly.
Lemma [derived; the transposition rule "V^T costs what V costs" is recalled]. c*(N) = least cost of a V with V H' V^T
diagonal. Then **T(N)/2 <= c*(N) <= sqrt(N) T(sqrt N) + N - sqrt(N)**. Left: H' = N V^T D^-1 V (x-5). Right: the V above.
If T(N) = c N log2 N the two sides are (c/2) N log2 N and (c/2) N log2 N + N. If T is linear, so is c*, and the other way.
Numbers: 28 + 12 = 40 gates at 16 points and 152 + 56 = 208 at 64 points with the night's 7 and 19, against T/2 = 26 and 152.
What it gives: the question "what is the cheapest basis of the mirror", open since wave 1, has the answer "half a transform,
to within N gates", and searching the family is searching circuits of the shape V^T D V, which loses at most a factor 2.
A cheap V would be a cheap transform; no argument makes V easier than H. Two wave-7 mutations can be dropped as separate
routes. Where it stops: the lemma compares least costs; it does not say the cheap member is easy to find.

### Hybrid 3. Ports are orthogonal splittings (x-6's ports x x-3's address maps x the tiny cut-set lemma x m-cross's "one merge tree")

Idea. x-6 counted ports by machine: 2^(h-1) for the transform, h for every other kernel; 20 and 80 of dimension 2.
Guess: a port is a subspace P of the address space with P and P-perp meeting only in 0. Then the address space is P plus
P-perp, x.y splits into the two parts, and H is (transform on P) times (transform on P-perp).
Tried [ran, `hyb34.py`, `hyb34.out`, exhaustive over all subspaces]:

| address bits h | dimension 1 | dimension 2 | dimension 3 |
|---|---|---|---|
| 3 | 4 of 7 | 4 of 7 | |
| 4 | 8 of 15 | 20 of 35 | 8 of 15 |
| 5 | 16 of 31 | 80 of 155 | 80 of 155 |
| 6 | 32 of 63 | 336 of 651 | 640 of 1395 |

Dimension 1: the 2^(h-1) words of odd weight. Dimension 2 at h = 4, 5: 20 and 80. Both are x-6's numbers. And at 8 points
along p = 111: H(x, y) = (-1)^(a b) (-1)^(u.v) with x = a p + u, y = b p + v, u and v even words, on all 64 entries.
What it gives: (i) one sentence for fact F: **the transform splits along every orthogonal splitting of the address space;
the class splits only along coordinates.** About half of all subspaces are ports. (ii) x-6's "at dimension h/2 each port
knows exactly one other subspace" is P and P-perp. (iii) with x-2's sixth line: a circuit whose wires are sign vectors in
any mixture of frames still pays 0.315 N log2 N. So ports can change the order only together with height. No report has put
a tall wire through a port; x-6 measured largest coefficient 6 inside one invocation of the unit.
Where it stops: a count and an identity. I did not build any circuit that uses two frames.

### Hybrid 4. Walking the whole-number bases (x-8's Smith form and its second class x x-5's family x hybrid 2)

Idea. x-8 listed the whole-number bases of determinant +-1 that diagonalise H at 4 points by enumeration (7 with entries up
to 2; 2 classes once the inputs may be relabelled and negated; one class not a tensor product). Enumeration stops at 4
points. A walk does not: from one pair (A, D) with A D A^T = H, every 2 x 2 whole-number matrix g of determinant +-1 that
keeps D diagonal gives another pair, A g^-1 and g D g^T. For example the two entries (1, -2) of D become (-1, 2) by
g = [[1,1],[2,1]].
Tried [ran, `hyb4b.py`, `hyb4b.out`; every pair checked to give H exactly]: breadth-first walk from (Z, D) with moves of
entries up to 3 (4 points) or 2 (8 points).
- 4 points, 6 moves, entries of A up to 3: 108 pairs up to order and sign of columns. Four sign patterns of the diagonal:
  (1,-2,-2,4) which is Z's, (1,2,-2,-4), (-1,-2,2,4), (-1,2,2,-4). They are exactly the four patterns in x-8's
  `adapted4.out` [read]. Non-zeros of A: 9 (twelve bases, Z among them) up to 16. None below 9.
- 8 points, 3 moves, entries up to 2: 274 pairs. Non-zeros 27 (123 bases, Z among them) to 36. None below 27.
- 8 points, 5 moves, moves with entries up to 2, bases with entries up to 3 (`hyb4c.out`): 32,191 pairs, every one checked
  to give H. Non-zeros 27 (330 bases, Z among them), 28 (330), 29 (828), and up. None below 27.
What it gives: the Smith form fixes the sizes of the diagonal entries, not their signs, and two-column moves pass from one
sign pattern to another; Z is a sparsest member of everything walked. Non-zeros are only a proxy for gates (gates <= non-zeros - N).
By hybrid 2 a cheaper member would be a cheaper transform, so this walk is a search for the transform in other clothes.
I could not match x-8's representative rows to my labelling (`x8basis.py`: four orientations, 24 relabellings, no hit;
x-8 also allows negated inputs, which I did not try). Only the sign patterns are matched.

## 4. The most surprising thing, and the question that would tell the most

**Surprise of this wave.** x-6. The only program that changes the order was written as a call program for the first time, and
its saving turned out not to be an identity of the class (ports), and to obey a law nobody had written: z is the root of
"sum over the unit's blocks of (rank/m)^z = W", which reproduces the published 8.7625e-4 and 7.4745e-4 from the
certificates. In that law the order depends on the number of BLOCKS per array and the share rho of directions skipped:
saving = ln(1/(1-rho)) / (ln k + ln(1/(1-rho))). Two blocks with 7.4 % skipped is 0.1; one block is n log log n. The
published unit has 16.5 blocks and 0.21 %. And the same report's caps for this mechanism, 0.078 to 0.147 on paper, straddle
the standing bar of 0.1. So the bar is not out of reach of the existing mechanism on paper, and nobody has optimised the
quantity the law says to optimise. (All of it: floats, what-if block lists, one author.)

**Question. Are neighbour sums on the cube possible in O(N) gates?**
Why this one. (i) It is necessary: T(N) linear gives neighbour sums in 2 T(N) (x-5; hybrid 1). (ii) It is the simplest
convolution that is not trivially linear, and the transform is one polynomial in it. (iii) No known wall speaks: volume asks
only about (N/2) log2 k; the matrix has k N ones and no 2 x 3 block of ones, so circuits that only add need of the order of
k N gates [recalled: the standard count for matrices without large all-ones blocks], and the whole question is whether
cancellation or coefficients help. At 8 points they do not: 12 gates, exhaustive modulo 2, 3, 5 [read: d-0]. (iv) Both
answers move the main question: a growth like k N with any coefficients, argued or even only measured to 64 points, is the
first evidence against linear size that does not go through volume; a growth like N or N log k names the first cancellation
that pays on the cube, and the next rung (sums over a ball of radius 2, then x-1's lightest outputs) is the same experiment.
First datum [ran, `w-cross/nbr4_p*.out`, `d-0-zeta/mincirc`, exhaustive in each field; "none modulo p" is not "none"].
The matrix splits into two equal blocks (even addresses read odd ones). One block at 16 points is 8 outputs from 8 inputs,
four ones per row, rank 5; pairing gives 16 gates. There is NO circuit with 14 gates or fewer modulo 2, none with 13 or
fewer modulo 3, none with 12 or fewer modulo 5, none with 11 or fewer modulo 7 (13 modulo 5 was stopped at 420 seconds,
undecided). So modulo 2 the block costs 15 or 16, and
free coefficients did not help as far as each field was searched. Gates per point so far: 0.5, 1.5 and (modulo 2, and if
the two blocks cannot help each other, which I did not prove) at least 1.875 at 4, 8, 16 points. That does not yet separate "like k" from "like log2 k" (pairing: 0.5, 2, 3.5, 5 at k = 2, 4, 6, 8;
log2 k: 1, 2, 2.6, 3): 64 points is the first size that tells.
Experiment. Finish the block at 16 points (15 gates modulo 2 is about an hour of `mincirc`; 14 modulo 3 about 40 minutes);
annealer with
free coefficients at 32 and 64 points; report gates per point against the pairing count ((3/4) k - 1 per point for even k:
0.5, 2, 3.5 at 4, 16, 64 points) and against log2 k. Then the same for
"neighbour sums plus c times the input" for c = 1, 2 (the matrix is then invertible and the volume count exact).

## 5. Three objects for a skeptic, in this order

Nothing in wave 7 or here claims to beat a known count. The order is by how much rests on each.
1. **The height lemmas.** x-0 lemma 3: a circuit for H whose wires all have height at most M has at least
   N - 1 + ((N/2) log2 N - (N - 1) log2 M) / log2(4 M^2) gates, with any coefficients; x-0 lemma 1: exactly N - 1 merges, each
   bringing at most log2 of its larger coefficient; x-2's version (N/2) log2 N / (2 + 2 log2 M); x-8's bridge (whole-number
   matrix with orthogonal primitive rows: entropy <= 2 log2 |det|, equality only for entries 0, +-1). Attack: is the per-gate
   budget really bounded by the height of the WIRES when the gate's result has a large common factor; x-0's own limit (the
   per-gate volume depends on the order of the wires and its total can exceed (N/2) log2 N); do x-0 and x-2 define height
   the same way; look for the statement in the literature on bounded-coefficient lower bounds.
2. **x-6's growth law and caps**, with my reading of ports. Exactly: z is the root of sum over blocks of (rank/m)^z = W and
   this reproduces both published savings; with k equal blocks and skipped share rho the saving is
   ln(1/(1-rho)) / (ln k + ln(1/(1-rho))); ports of dimension r exist for r below h/2 and the mechanism caps at 0.147
   (r = h/2, dead), 0.098 (r = h/3, merged blocks), 0.078 (four blocks). Attack: recompute both published savings from the
   certificates in exact arithmetic; the step "kappa at most 2 at r = h/2"; whether the what-if block lists correspond to any
   legal network; my claim that ports are exactly the subspaces meeting their perpendicular in 0 (I matched counts at
   h <= 5 and one identity, not x-6's definition line by line).
3. **x-4 lemma D and x-9's class floor**, the two statements that close a model for linear size. x-4: with flag kernels and
   free diagonals, the number r of passes satisfies r >= 2^(ceil(k/r) - 2), so about k / log2 k; lemma C (r >= 3 from 32
   points on) has one case by hand and one sketched. x-9: in the class "products on one chain, two-piece hubs with any
   coefficient, three gate shapes" at least (3/4) N log2 N + N/4 gates, called by its author the least secure statement.
   Attack: the count "block-diagonal plus low rank on cosets" in lemma D; the four hatches x-9 lists.
Also mine: the two lemmas of hybrids 1 and 2 are a few lines each and rest on the transposition rule in count (G), recalled
by x-5 and by me, read by nobody tonight. Hybrid 2's upper side is exact at 4, 16, 64 points; hybrid 1's needs k even.

## 6. Eight experiments for the next wave

Deepen what is alive:

1. **neighbour-sums** (the question of section 4; deepens x-5 mutation 3 and hybrid 1). Brief: as in section 4. Inputs:
   `d-0-zeta/mincirc`, `d-0-zeta/rows_nbr3.txt` (the 8-point matrix), `w-cross/rows_nbr4half.txt` and `nbr4_p*.out` (one
   block at 16 points: 15 or 16 modulo 2), `j-machine/` annealers. Output: least gates at 16, 32,
   64 points for neighbour sums and for neighbour sums plus the input; gates per point against the pairing count
   ((3/4) k - 1 for even k) and against log2 k; for
   the best circuits the height of the wires. One line: does cancellation or a coefficient other than 1 ever save a gate.
   Then try to prove the easy half: with gates u + v only, at least c k N.
2. **fewer-blocks** (deepens x-6; the only brief aimed at the bar 0.1). Brief: in x-6's law the saving is
   ln(1/(1-rho)) / (ln k + ln(1/(1-rho))) for k blocks per array and a share rho of directions skipped. Take the tiny engine
   game (`wht38/tiny/`) and change the objective from moves to BLOCKS per array: search exchange words that cut each array
   into 2 or 3 blocks, using fat ports (hybrid 3: 20, 80, 336 ports of dimension 2 at h = 4, 5, 6). Output: the least k
   found for rho >= 5 %, the saving by `x-6-unitasbox/zlaw.py`, and for each candidate whether a legal network exists (not a
   what-if list). Also x-6's own floor question: can any array make ONE block of rank below m.
3. **tall-pool** (deepens x-0 mutation 4 and fact C). Brief: every pool searched tonight has bounded height, so by the height
   lemma none could hold a linear circuit. Search at 8 and 16 points in the pool of wires sum over j of 2^j f_j, f_j sign
   vectors on the cosets of one flag (the partial sums of Z D Z^T), with the coefficient cap removed. Report least gates as a
   function of the largest j allowed: flat, or falling? Then the same with the f_j taken from two frames (hybrid 3). A flat
   answer at 16 points says height does not pay below some size; x-0's argument says it must pay eventually.

Nobody has tried:

4. **convolution-ladder** (from hybrid 1). Brief: T(N) <= max over q of c(q) <= 2 T(N). Convolutions whose q depends on
   the weight only form a family with k + 1 parameters that contains the identity (0 gates), all-ones (N gates), neighbour
   sums, x-1's lightest outputs and the transform. At 16 and 32 points price a grid of them (annealer, free coefficients)
   and draw the map: which are linear, where does the cost jump, is the transform the only expensive corner or is expense
   generic. Output: the cheapest q whose cost per point grows with k in every construction, with its spectrum.
5. **z-cut** (a meter for maps of determinant 1). Brief: x-2's identity gates = n(L) + n(R) - B + E holds for every circuit
   and cut, and for H gives E >= N/2 + 1 from pairs of rows (h, h), (h, -h). Apply it to subset sums: the rows are (z, 0) and
   (z, z). My first look [derived, five minutes]: the pair argument does NOT give E >= N/2 there, because a gate that makes
   (z, z) can be new on the right half only, so a join can ride on a gate of the right half's circuit. Decide it: is Yates
   optimal among circuits with B = 0, what is the forced E, and does a Z-circuit below Yates need shared gates in every cut.
   Tools: `x-2-floorhatch/alldirs.py`, the 2,748 best 8-point circuits of u-7, u-3's 16-point circuits. All of the cost
   of H sits in Z-like maps where volume reads nothing; this would be the first meter that reads there.
6. **cancellation-literature** (reading, then one test). Brief: Z is the matrix "T inside S", known as the disjointness or
   Sierpinski matrix; it is Pascal's triangle modulo 2. Read what is proved about it and about the cube's neighbour sums in
   circuits that only add, in circuits over the two-element field, and with arbitrary coefficients: the survey by Jukna and
   Sergeev on linear Boolean operators (2013), "Separating OR, SUM and XOR circuits" (Find, Goos, Jarvisalo, Kaski, Koivisto,
   Korhonen), "Fast monotone summation over disjoint sets" (Kaski, Koivisto, Korhonen), the fast zeta transform papers of
   Bjorklund, Husfeldt, Kaski, Koivisto [all recalled by name only; check dates and statements]. Wanted: the best known
   count for Z with cancellation, any separation between adding-only and cancelling circuits on a matrix of this kind, and
   whether "Z in O(N) over the two-element field" is a named open problem. Then test the best construction found at 16 points.

One hybrid:

7. **chain-of-exchanges** (x-3's address-map family x x-6's blocks x hybrid 3). Brief: x-3 says 1.5 K calls for the
   address-map family would need chains in which each call is the second box for one piece of data and the first box for
   the next; x-6 says an exchange cuts each array into at least three blocks because every shear touches both arrays. Put
   them together: arrays in a ring, array i exchanging with array i + 1 along a port, so that one batched shear is the last
   shear of one exchange and the first of the next. Count blocks per array in the limit of a long ring, first on paper, then
   at K = 4 in x-3's exact setting (`x-3-boxrelations/perm7.py`: is 6 calls possible) and at h = 4 in x-6's (`ports2.py`).
   Output: blocks per array and rho for the ring, the saving by x-6's law, and the first place where a legal network fails.

One that sounds silly:

8. **the transform in a row.** Read the addresses as whole numbers 0 to N - 1 on a line, where three points do lie on a line
   and x-1's one-helper trick works (a polynomial of degree 2 at N points in N + 1 gates). By Lucas' theorem Z is Pascal's
   triangle modulo 2, entry "s choose t". Brief: take P, the true Pascal matrix, and D' a diagonal of powers of -2. Compute
   P D' P^T at 8, 16, 32 points and its difference from H modulo 4, 8, 16 for the two natural D' ((-2)^t and (-2)^(number of
   ones of t)); find the cheapest circuit for P (it is "shift a polynomial by 1": N - 1 gates in the basis of binomials, the
   cost is the change of basis) and for its low columns by the one-helper trick; ask whether some whole-number matrix that
   is Z modulo 2 is both cheap in a row and close to Z modulo higher powers of 2. It sounds like changing the problem;
   the reason to try is that the row is the one place tonight where a single wire served N/2 gates.

## 7. Criticism, last

- I read wave 7 through its result summaries. Where I say reports hit "one wall" I matched statements, not proofs. The three
  walls of section 2 are my grouping; DISTANCE in particular puts six lemmas under one sentence that I did not prove implies
  each of them.
- Hybrid 1 is an equivalence, and equivalences have cost this project time before: it does not make anything cheaper. Its
  use is the ladder. The claim "adding-only circuits need of the order of k N for neighbour sums" is recalled, not derived.
  The volume estimate (N/2) log2 k is rough and for odd k (for even k the matrix is singular).
- Hybrid 2 closes two proposed routes only as SEPARATE routes. A search of that family is still a legitimate search for the
  transform. The transposition rule is recalled.
- Hybrid 3: I matched x-6's counts and proved the splitting; I did not read x-6's definition of a port in its program.
- Hybrid 4 measured non-zeros, not gates, in a small ball around Z (five moves, entries up to 3). "None sparser" is a
  statement about that ball. x-8's "2 classes" is a count up to relabelling and negation of inputs; my 108 is not reduced
  that way, so the two numbers do not contradict each other.
- The key question may be as hard as the main one: no lower bound above linear is known for any explicit matrix with free
  coefficients, so a "no" for neighbour sums can at best be measured, not proved. I chose it because both outcomes are
  visible at 16 to 64 points, which is not true of the main question.
- Section 4's surprise rests on one report's floats and what-if lists.
- Nothing here changes the order, or any constant.

Files: `waves/wave-07/w-cross/` : hyb.py, hyb.out (hybrids 1 and 2); hyb34.py,
hyb34.out (hybrid 3; its hybrid-4 part is a first try with reflections that found only column exchanges, superseded);
hyb4b.py, hyb4b.out (hybrid 4); hyb4c.py, hyb4c.out (the deeper walk at 8 points); x8basis.py, x8basis.out (the failed
match with x-8's rows); rows_nbr4half.txt, nbr4_p2_m4.out to nbr4_p7_m3.out (neighbour sums, one block at 16 points,
`mincirc` in the fields with 2, 3, 5, 7 elements).
