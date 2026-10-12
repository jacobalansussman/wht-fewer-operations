# ab-0 neighbour-sums: can the sum over the k neighbours of every address be had in O(N) gates?

> Editor's note (11 October 2026): the critic corrected this report's explanation of the operation it saves in arithmetic modulo 2: that operation comes from one plane sum used three times ([ac-0](ac-0.md)). The scripts that it lists as `kill*.sh` stopped jobs on my machines and are not in this repository ([LEFT-OUT.md](LEFT-OUT.md)).

11 October 2026, wave 8, agent "ab-0-neighboursums", 60-minute box (04:44 to 05:44 EDT). Private. Nothing here is reviewed
or in Lean. Marks: [read] = in a file I opened; [ran] = computed in this box, exact (integers, fractions, or a named prime
field); [derived] = argued by me in this box, checked by nobody; [guess]. Gate count is (G) throughout: a gate is any
a*u + b*v, scalings free. Folder F = `waves/wave-08/ab-0-neighboursums/`.

Words. N = 2^k points; an address is k bits; e_j = the address with a single one at place j; E = {e_1, .., e_k}.
A = neighbour sums: output(y) = sum over j of input(y + e_j), bits added modulo 2. *One block*: the outputs at odd-weight
addresses as sums of the inputs at even-weight addresses, an (N/2) x (N/2) matrix; A is two copies of it.
*Adding-only circuit*: gates u + v, nothing else. *Uniform circuit*: every wire exists at every address y and is the same
combination of inputs seen from y (wire(y) = sum over z of q(z) input(y + z); q is the wire's *kernel*); a step is
new(y) = a * w1(y) + b * w2(y + g) for a fixed shift g, done at all N addresses, one gate per point. *Coset sum*: for a
subspace V of the address space, every address receives the sum of the inputs on its coset of V, possibly with signs
(-1)^(a.z); it costs fewer than N gates whatever the dimension of V, because all addresses of a coset receive the same value
up to sign. Its kernel is a *signed flat*: +1 or -1 on an affine subspace, 0 elsewhere. *Flat rank* r(k): the least number of
signed flats whose combination is the indicator of E, that is, the least number of coset sums whose combination is A.

## Summary

1. [derived] **The adding-only law is exact: N (k - 1 - floor(k/2)/2) gates**: (3/4) k - 1 per point for even k,
   (3/4)(k - 1) for odd k. x-5's pairing count is the minimum for gates u + v, not just a construction. (Section 1.)
2. [ran] **Cancellation does save a gate, once, and only modulo 2: one block at 16 points has a circuit with 15 gates over
   the field with two elements; adding-only needs 16.** With w-cross's "none with 14" the least modulo 2 is exactly 15.
   It is an artifact of the number 2: A^2 = k + 2 x (sums at distance 2), which is 0 modulo 2 for even k, so modulo 2 the
   block has rank 4 where the rationals have 5. The wiring found has no lift to the rationals (0 of 32,768 sign choices; and
   a two-line argument for any coefficients). It is NOT a circuit over the rationals and beats nothing. (Section 2.)
3. [ran] Over the odd primes the exhaustive search has still found nothing below adding-only: 4-point A + 1 and A + 2 cost
   6 modulo 3, 5, 7, 11; 8 points 12 [read: d-0]; the 16-point block has **no circuit with 14 gates modulo 3 and none with 13 modulo 5**
   (new; w-cross had 13 and 12), so it costs 15 or 16 modulo 3 and 14 to 16 modulo 5. This completes the brief's list
   "15, 14, 13 gates modulo 2, 3, 5": yes, no, no.
4. [derived] **A is the universal convolution** (folding, section 3): for a circuit that does the same thing at every
   address, a scheme for A is a scheme for the convolution with ANY k addresses in ANY number of bits. Solid consequences:
   (a) a circuit made of full layers (one gate at every address, the same up to shifts and signs) needs k - 1 layers for A
   and k for the transform, with any coefficients: the textbook transform is optimal in that class; (b) A is not a
   combination of fewer than about 4k/(log2 k)^2 coset sums. **Neither is a bound in gates once wires may be "blurred"**
   (the same value up to sign on whole cosets of a subspace): a blurred step costs N divided by the size of the subspace.
   In the middle of the box I wrote that no translation-invariant scheme gives O(N); that was too strong and is withdrawn.
   What is true is a price list: in a translation-invariant circuit a gate costs 2^(dimension of the affine hull of its
   support in the Fourier picture); the pairing circuit and the route through the transform are both of this kind; and a
   cheap circuit of this kind for A is a cheap transform on part of the bits. So inside this class A is not a simpler
   test than H; it is the same question.
5. [ran + derived] Flat rank: **r(k) = 1, 2, 2, 3, 3, 4, 4 for k = 2 to 8, which is ceil(k/2): pairs are never beaten
   there**, although big flats with cancellation were allowed; in general at most ceil(k/2), at least about 4k/(log2 k)^2.
6. **Growth law.** Everything I can prove or measure grows like k per point: exactly (3/4) k for adding-only circuits;
   k - 1 for full-layer circuits with any coefficients; number of coset sums ceil(k/2) up to k = 8. Nothing found grows like
   log2 k or stays bounded. The only growth below k that I know for A comes from the transform itself: A costs at most
   2 T(N) + N [read: x-5], so the published theorem gives O(N k^z), z = 1 - 8.7625e-4 [derived; it assumes the published
   program unrolls into a circuit of that size, which I did not check]. That is below the adding-only minimum once k is
   astronomically large: cancellation does pay for neighbour sums over the rationals, but so far only through the
   transform. No circuit over the rationals below a known count at any size tried. The annealer runs are not evidence.

## 1. Adding-only circuits: exactly N (k - 1 - floor(k/2)/2)  [derived]

Take a circuit whose gates are u + v only. Every wire is a sum of inputs with whole-number coefficients at least 0. An output
has every coefficient equal to 1 and nothing can cancel, so every wire that leads to output y is the plain sum of a subset
of y's k neighbours, and two wires added on the way to y have disjoint subsets. Hence the gates leading to y form a binary
tree with the k neighbours as leaves: exactly k - 1 gates, of which at most floor(k/2) are *pair gates* (two inputs added),
since pair gates of one tree are disjoint.
Two different addresses have at most 2 common neighbours (none unless they differ in exactly two bits a, b; then y + e_a and
y + e_b). So a gate that lies in the trees of two outputs is a pair gate, and it lies in at most two trees.
Count: gates >= sum over y of (k - 1) minus (shared pair gates) >= N (k - 1) - N floor(k/2)/2.
Pairing the directions (1,2), (3,4), ... meets it: the pair gate input(y + e_1) + input(y + e_2) serves y and y + e_1 + e_2.
Values: 2, 12, 32, 96, 224 gates at 4, 8, 16, 32, 64 points; per block 6, 16, 48, 112 at 8 to 64 points, replayed exactly
[ran on the rented machine: `nb.py check`].
The same argument for A + identity (k + 1 terms; two balls still share at most 2): N (k - floor((k+1)/2)/2); 6 at 4 points.
Limit: gates u + v with no scalings. With positive scalings the trees can overlap (for example
(a+b)/2 + (b+c)/2 + (a+c)/2); I expect the same count and did not prove it.

## 2. The first experiment: one block at 16 points, exhaustively  [ran]

Tool. `mincirc_top` = d-0's `mincirc` with one change: the FIRST intermediate value is restricted to given points. The
block's symmetries (translations by even addresses and permutations of the four bits) put the 28 pairs of inputs into two
orbits, distance 2 (24 pairs) and distance 4 (4 pairs) [ran: orbit count in the build step], and every circuit starts with a
gate on two inputs, so one representative per orbit suffices (four modulo 3: each orbit with coefficient +1 and -1).
Controls: the reduced search says "no" at 13 and 14 gates modulo 2 and at 13 gates modulo 3, as the full search did
[read: w-cross/nbr4_p*.out], in a fourteenth of the time.

**15 gates modulo 2: YES** (`B4_p2_m7_top_d2.out`, found in 1 second; a second one in `B4_p2_m7_top_d4.out`). Inputs in
column order = even addresses 0, 3, 5, 6, 9, 10, 12, 15. Five outputs are made by adding only; then
one wire g19 = (output 0 0 1 0 1 0 1 1) + (output 0 1 0 0 1 1 0 1), and the last three outputs are g19 + (an earlier output),
one gate each. Replayed modulo 2 by `verify15.py`: all 8 rows of the block, 15 gates.
Why it works modulo 2 only [derived + ran]. A^2 = k + 2 (sums at distance 2). For even k this is 0 modulo 2, so the sum of the
outputs at the k neighbours of any address vanishes modulo 2: relations with k terms. Ranks of the block [ran]:
16 points: 5 over the rationals and modulo 3, 5, 7, but 4 modulo 2; 64 points: 22 over the rationals, 16 modulo 2.
Over the rationals the relations at 16 points are "output(y) + output(y + 1111) = sum of all inputs" [ran], which involve
the all-ones row and are no cheaper than the pairing: I count 17 gates by that route against 16.
No lift, for any coefficients [derived by hand]: g19 lies in the plane of its own gate, spanned by the outputs
0 0 1 0 1 0 1 1 and 0 1 0 0 1 1 0 1; the gate that makes output 0 1 1 1 0 0 0 1 from g19 and output 0 0 0 1 0 1 1 1 needs
g19 in the plane of those two; solving a(first) + b(second) = s(third) + t(fourth) entry by entry gives a = b = s and
a + b = 0, so the two planes meet only in 0 unless 2 = 0. And none of the 2^15 choices of +1/-1 on the gates gives the
eight outputs over the integers [ran].
A recursion behind it [derived]: split the addresses by the last bit, A = (A' on each half) + (swap the halves). For even k,
A'^2 = 1 modulo 2, and then (outputs of the second half) = A' (outputs of the first half): half of the outputs are the
(k-1)-bit neighbour sums of the other half. That saves N/2 gates at each even k, the same slope (3/4) k as pairing. So even
in the field where cancellation pays, I see no change of growth.

**So the brief's question "does cancellation ever save one gate against the best adding-only circuit" has the answer:
yes modulo 2 at 16 points (15 against 16), for a reason that is special to the number 2; over odd primes and the rationals,
not in anything searched.**

**14 gates modulo 3: NO** in all four classes (`B4_p3_m6_d2p.out`, `d2m`, `d4p`, `d4m`; 101 to 190 seconds each, about
52 million final states each) [ran]. With the control above this is "none with 14 or fewer modulo 3". So modulo 3 the
block costs 15 or 16; "none modulo 3" is not "none".
**13 gates modulo 5: NO** in all six classes (first gate on two inputs at distance 2 or 4, coefficient 1, -1 or 2; the
coefficients 2 and 3 are exchanged by swapping the two inputs) (`B4_p5_m5_*.out`, 8 to 15 seconds each) [ran].
15 gates modulo 3 would need about 4 hours per class even reduced (the last level grows by a factor of about 107); not run.
Volume, for the record [ran, floats]: log2 of the product of the non-zero eigenvalues of A + 1 is 10.2, 52.3, 245.2 at
16, 64, 256 points, under one unit per point against 3, 4.5, 6 gates per point for pairing plus one. Volume asks nothing.
4-point A + 1 and A + 2: 6 gates, none with 5, modulo 3, 5, 7, 11 [ran, full `mincirc`] (modulo 3 the second matrix is A - 1).
Heights: every best circuit known over the rationals is the pairing circuit, all wires of height 1.

## 3. A is the universal convolution; what that proves and what it does not  [derived]

**Folding.** Let pi be any linear map from the k-bit addresses onto m-bit addresses, and feed A only inputs that are constant
on the cosets of the kernel of pi. Then A acts as the convolution on m bits with the k addresses pi(e_1), .., pi(e_k)
(repeats allowed), and since the e_j are a basis, pi can send them to ANY k addresses. A translation-invariant scheme for A
folds, step by step, into a scheme of the same shape for every one of these convolutions (a shift g becomes pi(g); a coset
sum over V becomes a coset sum over pi(V), or zero). A is the hardest convolution with k terms.

**Full layers: k - 1 for A, k for the transform.** Let a step be: at EVERY address y one gate
new(y) = a * (+-)w1(y + g1) + b * (+-)w2(y + g2), with fixed shifts g1, g2, fixed non-zero a, b and signs following fixed
patterns (-1)^(c.y); N gates per step. (The textbook transform is of this kind: the butterfly.) Write every wire family as
a combination of the operators "shift by g, then signs by c"; each step adds at most one dimension to the span of the pairs
(g, c) in use. The outputs of A, in any order and with any scalings, use shifts spanning k - 1 dimensions; the rows of the
transform use all 2^k shifts. So **at least k - 1 steps for A and k for the transform, whatever the coefficients: the
textbook's N log2 N is optimal among full-layer circuits**, and every circuit of the night below N log2 N must contain
gates that are not done at every address. [Possibly j-cross's product-wire lemma in other clothes; not compared.]

**Number of coset sums.** Take m with 2^m = k. Every set S of m-bit addresses has at most k elements, so its indicator is a
folding of the indicator of a subset of E (dropping elements of E restricts to a coordinate subspace, which only removes
or shrinks terms). r signed flats span a space of dimension at most r, which contains at most 2^r vectors with entries 0
and 1; the number of signed flats on m bits is 2^m times the number of subspaces, at most 2^(m^2/4 + m + 2.9). So
2^(2^m) <= 2^(r (m^2/4 + m + 3.9)): **r(k) >= k / ((log2 k)^2/4 + log2 k + 3.9)** (empty below k of a few hundred).

**Why this is not a bound in gates: the price list.** Call a circuit *covariant* when its set of wires is closed, up to
signs, under translating the input. Describe a wire family by the function h on the "Fourier side" (the transform of its
kernel). The input is h = 1; a coset sum over V is the indicator of V-perp; A is L(a) = k - 2 (weight of a) = the sum of
the k sign patterns (-1)^(a_j). A family whose h is supported in an affine subspace of dimension d has only 2^d different
wires up to sign, so **a gate that makes it costs 2^d, not N.** Sharp wires (d = k) are the expensive ones.
On a coset G of V-perp the k sign patterns collapse to the classes of E modulo V, each with a signed multiplicity, and a
class of multiplicity 0 needs nothing. So a covariant circuit for A that first cuts the data along V costs, per point,
(a transform on V, there and back) + the average over the pieces of (surviving classes - 1).
V spanned by e_1 + e_2 alone: on half of the Fourier side the pair cancels and on the other half it is one pattern; this is
the pair gate. V = everything: every piece is one point, nothing survives to be added, and the cost is the transform twice:
A = H L' H / N. Pairs on all bits AND full cutting would leave only k/4 - 1 additions per point on average instead of
k/2 - 1, but the cutting costs k per point with the textbook (section 6, question 3, for the break-even rate).
**So among covariant circuits the cheap ways to do A are transforms on part of the bits, and "A in O(N)" is the transform
question again**, not an easier one. The full-layer bound k - 1 holds only for circuits without blurred wires.
What is not covariant: circuits whose gates are not repeated at every address, such as the 15-gate circuit modulo 2.

## 4. Flat rank at small sizes  [ran, exact]

E sits in the odd-weight hyperplane, an affine space of dimension k - 1 in which it is an affine basis.
| k | signed flats | one flat | two flats | r(k) |
|---|---|---|---|---|
| 3 | 20 | no | yes (4 ways) | 2 |
| 4 | 128 | no | yes (7 ways) | 2 |
| 5 | 1072 | no | **no** (120 support candidates, 0 exact solutions) | 3 |
| 6 | | | no (restrict to k = 5) | 3 (three pairs) |
| 7 | 180,800 | | | **4**: no three flats (below) |
| 8 | | | | 4 (not below r(7); four pairs) |
`flatrank.py` is exhaustive over all pairs of signed flats. A flat of dimension d holds at most d + 1 points of E and
2^d - d - 1 points that must be cancelled. One decomposition at k = 4 is not "two pairs": the plane through three points of E,
minus a signed pair that is +1 on the plane's fourth point and -1 on the fourth point of E; one term both removes rubbish
and creates a wanted point. Generalised [derived]: a flat of dimension d plus signed pairs gives 2^d points of E for
2^d - d terms, worse than pairs from d = 3 on; a signed plane removes two rubbish points and creates two wanted ones.
Three flats at k = 7 (`flat3.c`, exhaustive over all triples of different supports among the 26,387 flats of the
6-dimensional affine space, by two necessary conditions: E is covered, and a point covered once lies in E; two terms on
the same support can always be replaced by two terms on its two halves, so different supports lose nothing):
348,123,691 pairs, 364 triples of supports pass, all of two shapes: three hyperplanes covering every point 0 or 2 times
(301), or two parallel hyperplanes and the whole space (63). `flat3check.py` kills all 364 by a lemma [derived]: on a flat
of dimension 3 or more, a combination of two sign patterns that takes only the values 0 and 1, with its ones affinely
independent, is identically 0 (it is constant up to sign on the whole flat or on each half, and 4 or more points of a
flat are never affinely independent); in both shapes every region is such a flat carrying two terms, so E would be empty.
**So r(7) = 4.** Control: the same program with six points lists the 15 ways to split them into three pairs, and the
plane-and-signed-pair variants [ran, `flat3_ctl_k6.out`].
So up to k = 8 the best "sum of coset sums" is the pairing, even with flats of every dimension and cancellation.

## 5. Runs that are not evidence

`nb.py` wraps the annealer `j-machine/slp.py` (floats, free coefficients) with these targets. In its "seed" mode nothing
was evaluated (deleting any gate of the pairing circuit breaks an output's support, and the annealer's start test never
passes); likewise from a random start at 8 points. From a start that passes the test (one wire holding all inputs, one gate
per output) the CONTROL failed: 13,518 wirings with 16 gates for the 16-point block, no zero, although a 16-gate circuit
exists; the 15-gate run from the same kind of start recorded nothing in the 7 minutes before I stopped it.
So the annealer says nothing about 15 gates over the rationals, nor about 32 and 64 points, which I did not reach.
The second half of the brief's first experiment (annealer at 32 and 64 points, A + c at 16 points) is not done.

## 6. What it became

- The question "A in O(N)?" has an exact answer for adding-only circuits and for full-layer circuits. For covariant
  circuits with blurred wires it turned into the transform question itself (section 3), which is a disappointment for the
  idea "A is a far simpler necessary test" and should be said plainly. What is left that is really about A:
  **circuits that are not covariant, where a wire is useful to many outputs because it is a different combination at
  different addresses.** The only specimen is the 15-gate circuit modulo 2.
- Better question 1 (search): 15 gates for the 16-point block modulo 3 or over the rationals. The modulo-2 circuit shows what
  a saving looks like (a difference of two outputs reused three times); over the rationals the relations are the antipodal
  ones, and the question is whether any circuit uses them at a profit. About 16 hours of `mincirc_top` modulo 3 (four
  classes, they can run side by side).
- Better question 2 (paper): is r(k) = ceil(k/2) for every k? True to k = 8. The induction "restrict to the span of E
  minus two points and lose one flat" works whenever some flat is a point or a pair, and fails on the plane through three
  points of E, which needs three points removed; a proof needs a better potential.
- Better question 3 (the price list as a search space) [derived, rough]: cut along the k/2 pair directions with a
  transform that costs c times the textbook. That is c k per point there and back, and on each piece what is left is the
  neighbour sums of a cube with about k/4 directions. So cost(k) = c k + cost(k/4), about (4/3) c k per point, which is
  below the adding-only minimum (3/4) k as soon as c is below 9/16. The night's best rate is 3/4 [read: task text]. So a
  transform at 9/16 of the textbook, at a size where it can be applied to half of the bits, would be the first circuit
  for A over the rationals in which cancellation pays; and conversely any proof that A needs (3/4) k per point would
  bound every transform from below by (9/16) n log2 n. Is there a V, not made of pairs, with a better threshold?
- Better question 4: the same folding for H. By w-cross hybrid 1, H is up to free signs the convolution with one quadratic
  sign pattern; its foldings are convolutions with the push-forwards of that pattern. Is one of them generic?

## 7. Criticism, last

- Section 3 is one hour old and I corrected it once already: the first version claimed a bound in gates for all
  translation-invariant schemes, which fails because blurred wires are cheap. What stands: the full-layer bound (a narrow
  class in which every step costs N), the bound on the NUMBER of coset sums (not on gates), and the price list, which is
  a way of counting, not a theorem about a minimum. The class "covariant" is my own definition.
- The 15-gate circuit is modulo 2 only. I showed that this one wiring does not lift, not that no 15-gate circuit exists
  over the rationals. "None modulo p" is not "none", and modulo 3 the search stops at 14.
- Section 1 excludes scalings. Section 4 is exhaustive for two flats; the three-flat "no" rests on a program one hour old,
  its one control, and a hand lemma. r(k) = ceil(k/2) is checked to k = 8 and guessed beyond; the proved lower bound is
  only 4k/(log2 k)^2.
- The remark that the published theorem gives A in O(N k^z) takes for granted that the published program is a linear
  circuit of that size in count (G); I read that from the task text, not from the release.
- No annealer evidence at all; nothing at 32 or 64 points beyond the adding-only law and the ranks.
- Nothing here changes the order, or any constant, for the transform.

## Files

F: `nb.py` (targets, pairing seed, `check`), `mincirc_top.c`, `mincirc_top` (symmetry-reduced exhaustive search),
`rows_B4.txt`, `top_d2.txt`, `top_d4.txt`, `top3_*.txt`, `top5_*.txt`, `B4_p5_m5_*.out` (13 gates modulo 5), `B4_p2_m7_top_d2.out`, `B4_p2_m7_top_d4.out` (the two 15-gate
circuits modulo 2), `verify15.py` (replay modulo 2, ranks, no lift), `B4_p3_m6_*.out` (14 gates modulo 3),
`flatrank.py` (two flats), `genflats.py`, `flat3.c`, `flat3`, `flats6.txt`, `flat3_k7.out`, `flat3check.py`,
`flat3_ctl_k6.out` (three flats at k = 7 and the control), `rows_A2c1.txt`, `rows_A2c2.txt`, `out/`, `out2/`, `job*.log`
(annealer logs), `rsh.sh`, `kill*.sh`, `chain*.sh`, `job*.sh` (run scripts). Copies of the programs and outputs are also
on the rented machine under `(the Linux machine's working folder)/ab-0-neighboursums/`; nothing is running there.
