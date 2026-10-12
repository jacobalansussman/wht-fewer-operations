# ae-cross: the nine waves side by side, four hybrids tried, and what to ask next

> Editor's note (11 October 2026): the critics of this wave corrected three statements of this report. That wave 9 "closed" the line-sum route is too strong: it is as open as the transform ([af-1](af-1.md)). "The transform modulo 8 costs about 2N + o(N)" is off by N: 3N + o(N) by that route ([af-0](af-0.md)). And the 8-operation circuit that "belongs to the transform alone" works for every block ([af-2](af-2.md)).

11 October 2026, 07:09 to about 07:35 EDT, inside a 40-minute box. Private. One agent; nothing reviewed, nothing in Lean, nothing published.
Marks: [ran] = run of mine tonight (files in `ae-cross/`, whole numbers or fractions); [derived] = by hand tonight, checked by
nobody; [read] = from tonight's reports; [recalled] = from memory, no source read; [guess].
Gate count everywhere: **(G)**, a gate is any a*u + b*v, scalings free. Count (O), OpenAI's, is not used.
Read: aa-cross and WAVE8-NOTE in full; the wall statements of j-cross and section 2 of k-cross; the eight wave-9 results as
handed to me (I opened ad-7 only for its passage on "repeats"). Wave 9's skeptics had not landed. That is a limit of
everything below.

**No circuit below a known count, no growth law below N log N, nothing of the 1e-1 kind. Nothing here changes the order.**

Words. N = 2^k points; an *address* is k bits; *weight* = number of ones. *The transform* H: entries (-1)^(x.y).
T(N): least gates for H, relabelling and scaling free. *Subset sums* Z: output(T) = sum of the inputs at the subsets of T;
*Yates*: (N/2) log2 N gates for Z. *Superset sums*: the same with supersets (Z transposed). *Flat*: a subspace of addresses
or a shifted copy. *Polynomial of degree d at all cube points*: N outputs, one per address y, of a polynomial in the bits of
y; the inputs are its coefficients. *Helper*: a wire that several outputs read. *Halving*: a gate that divides by 2, possible
only where two whole-number wires agree modulo 2. *Engine*: the published program's mechanism.
*The class*: the matrices built like H from any 2 x 2 block (*kernel*) with rows (p, q), (r, s); H is the kernel
1, 1, 1, -1. *Repeat* (ad-7): a gate whose value modulo 2 equals an earlier wire. *Bus* (ad-2): one wire carried through
several versions that many gates read. R(N): least gates for all N + q line sums of the plane with q = sqrt N points per
line. *Reed-Muller code of degree d*: the tables of values, at all N cube points, of the polynomials of degree at most d;
its *encoder* computes the table from the coefficients; its *rate* is its dimension divided by N. *Parity-check code*:
the vectors that satisfy a given list of sparse linear equations (*checks*).

## 0. In ten lines

1. **Wave 9 closed the one relation of wave 8 whose success would have passed the bar.** The plane's line sums are not
   an easier sibling: R(N) >= T(N) - (sqrt N + 1) T(sqrt N) (ad-1, two lines); ad-5 adds that the whole family of flat
   sign patterns ties and the line-sum route is the dearest. What is left with a ceiling beyond the bar is on paper
   only: ad-2's buses (N ln(log N) if a bus ever keeps anything; realised saving 0) and ad-0's two-shear exchange (0.21
   on paper; first cases negative).
2. **Three walls carry all eight reports** (section 2): REPAY (sharing costs what it saves at full rank), STEP (a step that
   reads one flat moves the target by one unit, and the target is k/2, k or n + 1 units away), DEPTH (the transform is k
   binary digits deep and every known program pays about N per digit).
3. **One thing is alive, and it sits at the low-rank end**: polynomials of degree 2 at all N cube points in N + o(N) gates
   (ad-6). Hybrid 1 says what that is for the transform: **a binary digit is a degree**, so ad-6 is "the transform modulo 8
   in about 2N gates", and the growth law of T is the slope of a ladder whose first rung ad-6 just lowered.
4. Hybrid 1 [ran]: H = sum over j of (-2)^j E_j exactly, E_j(y, x) = number of j-subsets of the common ones of x and y;
   digit j at output y is a polynomial of degree j in y whose coefficients are the superset sums at level j.
   By-product: a circuit for the 4-point transform with 8 gates and 3 repeats, so ad-7's guess "repeats >= (N/2) log2 N"
   is false as stated; and that circuit works for the transform's kernel only, not for its class (k-cross's L5).
5. Hybrid 2 [ran + derived]: whatever the free signs and relabelling, the transform is at least (N - sqrt N)/2 reflections
   from the identity, with equality exactly for powers of ad-4's brick. It is ad-0's "the matrix -1 is not a product of n
   shears" for the whole matrix; as a lower bound it is linear and therefore harmless.
6. Hybrid 3 [ran + derived]: T(N) is, within a constant factor and O(N), the cost of ONE tall matrix: all outputs from the
   inputs of weight at most k/2. That is the encoder of the half-rate Reed-Muller code over the rationals. The night never
   asked for the cost of that *space* in its cheapest basis.
7. Hybrid 4 [ran + derived]: aa-cross's ceiling for helpers (degree at most log2 k, hence N log N / log log N) is a fact
   about TWO helpers per output. With three it disappears: the necessary condition becomes that of a parity-check code with
   three checks per symbol, which is no obstruction. Known constructions still give only degree h with h helpers.
8. Old walls: U sharpened (flat rank >= k, not k/2; the bound uses flatness, not the quadric); M located at the prime 2
   and given its first specimen of a coefficient that does the work of L passes (and the reason it is not enough);
   C extended to the whole family of flat patterns; S proved for the plane route. None broken. k-cross's rectangle count:
   untouched for the sixth wave.
9. Most surprising: ad-0's cascade. The engine's best block alone would give 6.8e-2, and misses the bar by 11.1 % against
   11.5 %; four paybacks then divide it by 78. Most informative question: **is the price of a digit ever below N beyond
   the first two, that is, does degree 3 cost N + o(N)?** Section 4.
10. Skeptics first: nothing in wave 9 claims a circuit below a known count over the rationals. In order: ad-6's
    N + o(N); ad-1's inequality R >= T - (q+1) T(q); ad-4's pair-kill theorem. Section 5.

## 1. Facts that explain each other

**A. ad-7's digits, ad-6's degrees and ad-1's "Smith decomposition" are one identity.** [ran, hybrid 1] H = Z D Z^T with
D = (-2)^(size of the set) splits by size: H = sum_j (-2)^j E_j. ad-7's "digit j has C(k, j) pieces" is rank E_j = C(k, j)
[ran, k = 2 to 5]. x-1's "about 2N per digit" is "N for the superset sums of one level, N for evaluating a degree at every
point". ad-6 lowers the second of these for degrees 0 to 2 together.

**B. ad-0's shears, ad-3's Lemma D, ad-4's pair-kill and ad-5's shear rank are one count.** Each says: a step controlled by
one flat changes an integer attached to the target by at most one (two per two bits in ad-4), and the target sits k/2, k,
m or n + 1 away. aa-cross's hybrid 4 was the first instance. Hybrid 2 is the same count for the whole matrix.

**C. ad-1 and ad-4 found the same identity independently** [read both]: at 256 points the quadric's signs are
-1 + 2 (number of nine 4-bit subspaces containing z) - 16 [z = 0]. Two programs, two authors: it can be taken as replayed.
ad-5's partial-spread patterns are the same nine subspaces with other choices.

**D. ad-2's bus is ad-6's helper.** [my reading] A helper class read by many outputs is a bus. In ad-6 every bus realises
its full ceiling (N outputs, o(N) helpers, one gate per output). In ad-2 the realised saving is 0 at 8 and 16 points.
The difference is rank: N outputs made by one gate each from V helpers have rank at most V, so at full rank V >= N and
nothing is left to share. REPAY is the full-rank end of a dial whose low-rank end is ad-6.

**E. ad-3's "conjugator used twice", ad-5's "two layers paid in full, the shear is free" and ad-0's "the word pays 4 of 5
back" are k-cross's L1** (conjugation: half a transform going in, half coming out). ad-5 adds that the free middle may be
any map at all, linear or not, and the price does not move. So ad-5's own hatch (a control that is not a flat) is narrow
[derived]: after opening t bits ANY control of those bits is free, so the cost of a control is the number of bits it
reads, twice, never its shape.

**F. ad-7's census and k-cross's L5 say the same thing from two sides.** [guess] All best circuits have no halving and
only the coefficients 1 and 2 (ad-7); every saving is an identity valid for every 2 x 2 kernel (k-cross). A circuit that
is an identity in the kernel's entries cannot divide by something that depends on the kernel; and the one property the
transform has beyond its class, H H = N, can only be used by a circuit that halves. So no circuit of the night uses the
reflection. Hybrid 1 has a first specimen from outside the class (8 gates at 4 points, valid only when p s + q r = 0), and
the digit ladder is where such circuits come from: x-1's circuits modulo 4 and ad-6's route are of this kind.
Experiment 8 (the census) and experiment 6.

**G. ad-1's equivalence is w-cross's half price a fourth time**, now with the inequality in both directions:
T - (q+1) T(q) <= R <= T + (q+1) T(q).

## 2. The walls, each once

**REPAY (j-cross S; k-cross L1, L2).** *At full rank, a wire that serves two uses pays for the removal of the foreign part
what the sharing saved.* Wave 9: ad-2 (FORCED OFFSETS: on every bus inspected the cancelling gate replaces exactly one pure
gate; cut inequality gates >= 2 f(n) + sum of min(injections, 2), 20,790 cuts); ad-1 (EQUIVALENCE); ad-3 (nesting ties:
each level half the size, needed twice); ad-5 (BENT-FAMILY: 2 q T(q) for every member); ad-0 (the exact ledger: of the
unit's credit 75 % goes to copies and 18 % to helpers).
Status of **S**: proved for the plane route (ad-1, by hand, unreviewed), measured again in three classes. Not broken.
New and exact: the engine's version has a number, n + 1 shears for n free moves.

**STEP (j-cross U; aa-cross BENT; k-cross L3).** *Lemma. A function of r flat indicators is constant on a flat of
codimension r; the transform's pattern is constant on no flat above k/2.* Wave 9: ad-3 (Lemma D, j(k, c) >= (k/2 - 1)/c;
exact values 2, 4, 3); ad-4 (pair-kill: flat rank >= k, 2 log2 N in the doubled class, exactly 4 at 8 points even with
arbitrary free signs); ad-5 (m stages for every bijection of m bits, using only bijectivity); ad-0 (n + 1 shears);
hybrid 2 here.
Status of **U**: sharpened twice (k instead of k/2; flatness instead of the quadric). One number moved the other way:
the upper bound on the number of flats fell from 2^(k/2) to 2^(0.43 k) (ad-4). Not broken.

**DEPTH (j-cross M; k-cross L4).** *The quotient of the whole-number lattice by the transform's rows is a sum of cyclic
groups of order 2^j, C(k, j) of them; total depth (N/2) log2 N* [derived from H = Z D Z^T, Z having determinant 1]. Wave 9: ad-7 (ONE DIGIT: a saving modulo 2 dies at 4;
neighbour sums have invariant factors 1, 1, 1, 1, 2); ad-1 (SCALAR: at the primes above 2 a rational coefficient is a
scalar, so short cyclic passes have valuation at most 1; RESOLUTION: one pass can take any valuation but only on coarse
classes of primes); hybrid 1.
Status of **M**: located. It is Morgenstern's volume read at the prime 2, where it has a profile and not only a total.
[ran by ad-7, reading mine] the 3/4 family spends exactly (N/2) log2 N gates u +- 2v: one per unit of depth. By Morgenstern's bound
[recalled] a program of linear size needs coefficients that grow with N; in this picture it has to account for about
(log2 N)/2 units of depth per gate [guess: "units per gate" is not a proved per-gate bound]. The two visible ways are a
coefficient 2^e (ad-7: no best circuit has one) and a halving (none has one either).

**LAYERS (j-cross C).** Extended by ad-5 to every flat sign pattern of the Maiorana-McFarland kind and by ad-3 to
exchanges ((7/8) N log2 N or more). Not broken.

**k-cross.** L5 "one class": widened to the family of flat patterns (ad-5: different Hadamard matrices, same 304 at 64
points). Rectangle count: ad-4 gives a handle (a flat of rank 2^t is 2^t rectangles moved by one linear map) and no number.

**What no wall covers, after nine waves.** A circuit with a halving or a deep coefficient; a bus at full rank that keeps
anything (a 13th mixed gate or a used ninth injection, ad-2); three or more helpers per output; the cost of a space as
opposed to a matrix (hybrid 3). In the engine: a step cheaper than a move that tells the +1 part from the -1 part, and an
address map that carries the port (ad-0).

## 3. Four hybrids, each tried

### Hybrid 1. A binary digit is a degree (ad-7's ladder x ad-6's N + o(N) x x-1's price per digit x g-4's H = Z D Z^T)

Idea. ad-7 reads the transform digit by digit in base 2; ad-6 evaluates polynomials of low degree cheaply. They are the
same expansion: (-1)^m = (1 - 2)^m = sum_j (-2)^j C(m, j) with m the number of common ones of x and y.
Tried [ran, `h1_digits.py`, `h1_digits.out`, whole numbers, k = 2 to 6].
- H = sum_j (-2)^j E_j on every entry; H is congruent to the sum up to j = d modulo 2^(d+1), for every d.
- rank E_j = C(k, j) for k = 2 to 5 (modulo 1000003, which can only underestimate; the values equal the upper bound).
- On integer data, digit j at output y equals the sum of the superset sums sigma_J over the j-sets J inside y: a
  polynomial of degree j in the bits of y.
- [derived from ad-6's count + the recalled rule that a transposed matrix costs the same up to the difference of its
  sides] the transform modulo 8 costs about 2N + o(N) gates: N + o(N) for the superset sums of levels 0, 1, 2 (the
  transpose of ad-6's matrix) and N + o(N) for ad-6 itself. x-1's ladder charges about 2N for each further digit.
- Where the mass is [ran]: the levels within sqrt(k) of k/2 hold 96 to 98 % of the N coefficients at k = 16 to 1024; half
  of sqrt(k) on each side holds 70 to 79 %. The digits that matter are the middle ones.
- The ladder [ran, a what-if on ad-6's reported excess]: with the textbook recursion on top of ad-6's degree-2 base,
  degree d costs about d - 0.85 gates per point at k = 64 instead of d: the slope in d is 1 either way (30.2 against 30.4
  at degree 32).
- By-product [ran, exact]: a+b, c+d, their sum s, b+d, s - 2(b+d), s - 2(c+d), b+c, s - 2(b+c) is the 4-point transform in
  8 gates with 3 gates whose value modulo 2 repeats an earlier wire. ad-7 guessed at least (N/2) log2 N = 4. The weaker
  form "gates >= N - 1 + (N/2) log2 N" (7, 19, 47) is not touched by this.
- **That circuit is not an identity of the class** [ran, `h1_class.py`, `h1_class.out`, six kernels; derived for all].
  With the wiring fixed and every coefficient free, it computes the square of a kernel with rows (p, q), (r, s) exactly
  when p s + q r = 0. A kernel with p s + q r = 0 is the transform's own kernel with its rows and columns rescaled, so
  this wiring serves the transform and no other member of the class. Reason: it peels the first digit (H = J - 2 [x.y
  odd]), and the expansion in digits belongs to the transform alone. It has one gate more than the least; it is the
  first circuit I know of tonight that uses something the class does not have.
What it gives: one dictionary for walls DEPTH and LAYERS, and the reading of the one live result. Where it stops: ad-6's
gain is one unit, not a slope; the middle digits are full rank, where fact D says helpers have nothing to share.

### Hybrid 2. The nearest the transform gets to the identity (ad-4's brick x ad-0's shear count x ad-3's reflections)

Idea. ad-4: with free signs the 4-point transform is J - 2P, one reflection. ad-0: an exchange is a product of shears and
the count is forced by the target. Ask the same for the whole matrix: over all free signs and relabellings, how small can
the part of the space that the transform moves be?
Lemma [derived]. M = (signs) H (signs) (relabelling) / sqrt N is orthogonal with entries +-1/sqrt N, so its trace is at
most sqrt N. The trace is at least (dimension fixed) - (dimension not fixed). So M fixes at most (N + sqrt N)/2 dimensions
and is a product of no fewer than (N - sqrt N)/2 reflections, or of that many shears.
Tried [ran, `h2_trace.py`, `h2_trace.out`, fractions]. 4 points, all 6,144 signed relabelled transforms: the least
codimension of the fixed space is 1 (64 matrices, all of trace 4). Powers of the brick 2I - J at 16 and 64 points:
6 and 28, equal to the bound.
What it gives: the brick is "one reflection", and its powers are the nearest any dressed transform comes to the identity.
g-0's question (the cheapest basis of the mirror) cannot be dodged by shrinking the mirror: it has (N - sqrt N)/2
dimensions at best. Where it stops: the bound is linear. It says a general circuit needs N/2 gates, which everyone knew;
all of log N comes from how sparse each step is, and this count is blind to that.

### Hybrid 3. The transform as one encoder (hybrid 1 x Yates x the complement of an address x coding theory)

Idea. Split the inputs of Z by weight: low (at most k/2) and high. For odd k each half has N/2 inputs.
Tried [ran, `h3_rm.py`, `h3_rm.out`, k = 3, 5, 7, every entry].
- The block "all outputs from the high inputs" is the block "low outputs from low inputs", transposed and relabelled by
  complementing addresses, and it is zero on the low outputs.
- The block "all outputs from the low inputs" has as its column space exactly the characters of weight at most k/2: it
  is the evaluation of all polynomials of degree at most k/2 at all cube points.
[derived] So cost(Z) <= 2 cost(low block) + 1.5 N (N/2 by a closer count), and cost(low block) <= cost(Z). With g-4 (subset sums = three
transforms) and H = Z D Z^T: **T(N) equals, within a constant factor and O(N), the cost of the tall matrix that encodes
the half-rate Reed-Muller code in the monomial basis, over the rationals.**
New question it opens: the cost of the *space*. Any N x N/2 matrix with the same column space is a generator; the monomial
one is only one of them. For the affine code [ran, k = 3 to 6] the generator that takes the values at 0 and at the unit
points as inputs costs N - 2 against N - 1; the floor is N - k - 1. For the half-rate space the floor is N/2 and I know
no generator below the monomial one. [derived] A cheap generator alone does not give a cheap transform: the change of
basis is a second matrix of size N/2, needed once for each half of the input, which is the textbook recursion.
[recalled, no source read] Codes with encoders of linear size exist (Spielman 1996); I know no such encoder for this code
and no proof that there is none.
What it gives: a sixth member of the family "equivalent to the transform" (after the mirror, the hardest convolution, the
conjugator, the line sums and the bent family), in a field with its own literature, and one question nobody asked.
Where it stops: a reformulation; w-cross warned about those.

### Hybrid 4. Three helpers (aa-cross's graph x ad-6's selectors x parity-check codes)

Idea. aa-cross: with two helper classes per output the outputs are the edges of a graph, a relation among fewer than
2^(d+1) values of polynomials of degree d cannot exist, so short cycles are forbidden and the classes number more than
2N/3 from degree log2 k on. With h helpers the outputs are edges of a hypergraph.
[derived] Necessary condition for h helpers: every set of fewer than 2^(d+1) outputs touches at least as many classes as
it has outputs (otherwise the helpers force a relation that the polynomials do not have). For h = 2 this is the girth.
For h = 3 it is the condition under which a parity-check code with three checks per symbol has large distance, and such
codes exist with distance proportional to their length [recalled: Gallager]. So for three helpers neither the rank
(classes >= number of monomials, which is o(N) up to degree k/2 - sqrt k) nor the distance forbids o(N) classes at high
degree. The ceiling N log N / log log N is special to two.
Tried [ran, `h4_three.py`, `h4_three.out`, fractions].
- Three partitions (forget an outer selector bit; inside each half, aa-cross's pair) carry every monomial of degree at
  most 3 and none of degree 4, at 32 and 64 points. This only confirms "h helpers reach degree h"; at these sizes the
  class counts (44 of 32, 84 of 64) are above N: the run tests correctness, not the count.
- 64 outputs on 32 classes drawn at random: with two helpers a set of 3 to 5 outputs with too few classes always exists;
  with three helpers none up to 5 in five drawings. A toy, not evidence.
[derived] In the families where classes are flats chosen by the point, h helpers reach degree h and no more: covering all
addresses of weight at most d by subspaces needs d + 1 of them, and a selector saves one.
What it gives: the first open case with a number: **three helpers, degree 4, o(N) classes** (or two helpers, degree 3,
which the girth bound allows from k = 8 on). Where it stops: even "every fixed degree in N + o(N)" would leave the middle
digits, which are full rank.

## 4. The most surprising thing, and the question that would tell the most

**Surprise of this wave.** ad-0 opened the published unit and found that it does not lose to the bar at the top. A data
array's stage climb, taken whole, would give a saving of 6.8e-2; the best block keeps 11.1 % of its stage against the
11.5 % that 1e-1 asks of a third of an array. Then four separate paybacks divide by 4.33, 1.20, 3.74 and 4.00, and the
published 8.76e-4 is what is left. The mechanism is within a hair of the bar before its overheads and a factor 78 from it
after them, and the first factor has a three-line reason (n + 1 shears).

**Question. Is the price of a digit ever below N beyond the first two? Concretely: do the polynomials of degree 3 at all
N cube points cost N + o(N) gates?**
Why this one. (i) ad-6 is the only place in nine waves where a price of "N per unit" was beaten in the leading term, and
hybrid 1 says the unit is a binary digit of the transform. (ii) The obstruction at degree 3 is one named monomial
(a selector bit times two bits from two different atoms), not a wall. (iii) If it falls, the recursion
cost(d) = N + cost(d)/2^t + cost(d - 1)/2^s gives every fixed degree in N + o(N) [derived, conditional], and the question
moves to how uniform that is as d approaches k/2. If it cannot fall, the proof is the first lower bound above N for an
explicit tall matrix in count (G), and it would say why each digit costs N. (iv) Two helpers are not excluded at degree 3
by the girth bound from k = 8 on, and three helpers are not excluded at all (hybrid 4).
Experiment. (a) Exact ladder at 16 and 32 points: least gates for "all polynomials of degree at most d at all cube
points", d = 1 to k, modulo 2 and modulo 3 with the exhaustive tools of ad-2 and d-0 (the top rung is subset sums, 32 at
16 points). Report the step from each rung to the next. (b) 64 and 128 points: search two partitions good for degree 3
with fewer than 56 and 108 classes (ad-6's numbers), letting BOTH forgotten sets depend on the point; `ad-6-twohelpers/
verify.py` tests any candidate exactly. (c) The same with three partitions for degree 4. Output: one table, and one
sentence: is any step of the ladder below N.

## 5. Three objects for a skeptic, in this order

Nothing in wave 9 claims a circuit below a known count over the rationals. The 57-gate circuit of ad-1 is over the
two-element field and its author shows it does not lift (87 after paying the carries).

1. **ad-6's N + o(N)** (`ad-6-twohelpers/circuit2.py`, `law.py`). Claims exactly: every polynomial of degree at most 2
   at all N cube points in N (1 + O(log k / k)) gates; built and replayed to k = 16, counted to k = 400; classes about
   2 N log2(k)/k. It does NOT claim anything for the transform. Attack: replay at k = 8 from the coefficients; check
   that the inputs are the coefficients and not something already summed; check V(4) = 14, which rests on a recalled
   theorem. It is the base of this note's key question.
2. **ad-1's inequality R(N) >= T(N) - (q+1) T(q)** (report, section on EQUIVALENCE). Claims: the line sums of the plane
   cost at least (c/2) N log2 N if the transform costs c N log2 N. It closes the only route that would have passed the
   bar. Attack: the direction of each use of the transposition rule; whether "T" on both sides is the same normalisation.
3. **ad-4's pair-kill theorem** (ad-4.md section 2): flat rank of quadric signs >= k. Claims that two flats can always be
   removed by one restriction of codimension 2 or its twin, unless all are shifts of one subspace. Case analysis by hand.
   Attack: the exceptional case, and the step to "2 log2 N in the doubled class".
Also: ad-0's lemma is a model, not a statement about the engine (its author says so), and "4 of 5 paid back" is read from
a block list. Mine: hybrid 3's "constant factor" uses the transposition rule and g-4, both taken on trust; hybrid 4's
necessary condition is five lines; the claim in fact F is a guess.

## 6. Eight experiments for the next wave

Deepen what is alive:

1. **ladder-degree-3** (section 4; deepens ad-6 and hybrid 1). Brief as in section 4. Inputs: `ad-6-twohelpers/`,
   `ae-cross/h1_digits.py`, the exhaustive tools in `d-0-zeta/` and `ad-2-twodeliveries/`. Output: the exact ladder at 16
   and 32 points; degree 3 with fewer than 56 classes at 64 points or a reason; the slope.
2. **the-first-bus-that-pays** (deepens ad-2). The two rooms outside the version lemma at 16 points over the two-element
   field: a 13th mixed gate, and a ninth injection that is used. Port `deco.py` to C and run all 6,960 upper circuits on
   the rented machine. The ceiling of this mechanism is N ln(log N), which passes the bar; what is missing is one bus
   whose realised saving is not 0. Output: d(4), or a 31.
3. **sector-and-port** (deepens ad-0; the only mutations there that bear on the order). Exact small search: 2 arrays,
   directions p and q, address maps that exchange p and q, at most 2 shears per array: is the matrix -1 reachable? And a
   step cheaper than a move that acts differently where the move is +1 and where it is -1, with digit columns treated
   differently. Guide from hybrid 2: aim at the dressed target of largest trace. Output: an exchange with two shears per
   free move, or the count n + 1 extended to address maps.

Nobody has tried:

4. **cheapest-generator** (hybrid 3). Least gates for ANY N x N/2 matrix whose columns span the characters of weight at
   most k/2, at 8 and 32 points (k odd), and for degree at most 1 and 2 at 16 points; exhaustive where possible.
   Compare with the monomial encoder. Then price the change of basis between the best generator found and the
   monomials. Read the coding literature for encoders of Reed-Muller codes over large fields (check dates). Output: gates
   per point of the space against the matrix, and whether the change of basis is again a half-size transform.
5. **three-helpers** (hybrid 4). Largest degree carried by three partitions with fewer than N classes in all, at 64 and
   128 points; classes need not be flats. State and test the condition "every set of fewer than 2^(d+1) outputs touches
   at least as many classes". Output: degree 4 with three helpers and o(N) classes, or the first bound of girth type for
   hypergraphs in this problem.
6. **deep-gates-and-halvings** (wall DEPTH; ad-7's first and third mutations, neither run). The 3/4 family uses exactly
   one gate u +- 2v per unit of 2-adic depth, and no record has a halving. (a) Exhaustive at 8 points with wires modulo 8
   before one halving gate and modulo 4 after: does a halving give the transform in 18 gates? Same class for the
   16-point block of neighbour sums at 15. (b) Find the smallest matrix of any kind (orthogonal up to scale, entries of
   one size) in which a gate u +- 4v or a halving saves a gate over every circuit with coefficients 1 and 2; ab-2 found
   the analogous 4 x 4 specimen for a coefficient 2. Output: the specimen or the circuit, or "depth moves one unit per
   gate in everything searched", with sizes.

One hybrid:

7. **the-rank-dial** (ad-2's bus x ad-6's helpers x hybrid 1; fact D). Subset sums restricted to the inputs of size at
   most d, at 16 points over the two-element field and over the rationals modulo 3, d = 1 to 4, with ad-2's exact
   decorated-cut search. For each d: least gates, the longest bus in a minimum circuit, and its realised saving. The bus
   pays in full at rank 11 (degree 2) and nothing at rank 16; find the rank at which it stops. Output: the table, and
   the invariant that turns the saving off.

One that sounds silly:

8. **the-best-bad-circuit.** Look for circuits that are worse. Every record is (by fact F, a guess) an identity of the
   whole class of 2 x 2 kernels, so none uses what only the transform has. First the census: in every record (7, 19, 52,
   128, 304) replace the kernel by letters and check whether the circuit is an identity in the letters. Then enumerate circuits for the 4-point and
   8-point transform with one or two gates MORE than the least (8 and 9; 20 and 21) and keep those that fail for the
   kernel with entries 1, 1, 1, -1 + e. The 8-gate circuit of hybrid 1 is the first specimen [ran]. Report what they contain that
   the records do not (a halving, a wire that is a sum of whole rows, a use of H H = N), and whether their count at 16
   points grows more slowly than the records' when composed with themselves.

## 7. Criticism, last

- I read wave 9 through its result summaries. "One wall" means I matched statements, not proofs. STEP joins five lemmas
  with different integers (k/2, k, m, n + 1, (N - sqrt N)/2); calling them one count is my reading.
- Hybrid 1 is an expansion of (1 - 2)^m. Its content is the dictionary, not a circuit. "Modulo 8 in 2N + o(N)" is
  derived from ad-6's unreviewed count and a recalled rule; I built no circuit. The ladder table is a what-if.
- The refutation of ad-7's guess is at 4 points with one more gate than the least; ad-7's statement was about circuits
  with coefficients 1 and 2 and no halving, which mine is, but its author may have meant minimum circuits only.
- Hybrid 2's bound is linear and proves nothing about gates. I include it because it answers "can free signs shrink the
  mirror" with an exact number.
- Hybrid 3 is the sixth equivalence of the night. Its one new question (the space against the matrix) may be empty:
  I showed that a cheap generator does not by itself give a cheap transform.
- Hybrid 4 removes a ceiling; it builds nothing. The random drawing is a toy. "No obstruction" is not "possible".
- The key question is about the low-rank end. The transform's mass is in the middle digits, at full rank, and nothing
  in this note touches them. A yes at degree 3 would be a second rung, not a growth law.
- I did not find anything that speaks for linear size. After nine waves the list of what no wall covers is shorter and
  more exact, and every item on it is a single small search.
- Nothing here changes the order, or any constant.

Files: `waves/wave-09/ae-cross/` : h1_digits.py, h1_digits.out (hybrid 1 and the
8-gate circuit); h1_class.py, h1_class.out (that circuit against other kernels); h2_trace.py, h2_trace.out (hybrid 2); h3_rm.py, h3_rm.out (hybrid 3); h4_three.py, h4_three.out
(hybrid 4).
