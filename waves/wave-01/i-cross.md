# i-cross: the eight developments put side by side, three hybrids tried, and what to ask next

> Editor's note (11 October 2026): the critics of this wave and later reports corrected statements of this report. That every kernel is two calls of the transform is false over the rationals; the true statement is "at most six calls" ([a-0](a-0.md)). The bound "for any Jordan basis change" fails for the transform at 4 points (a-0). The middle term of that bound, of size N log log N, overtakes the dense one only beyond N = 2^4096. The "squares" route of hybrid 3, 62 operations at 16 points, is the textbook circuit in other coordinates, so its tie is not independent evidence ([a-1](a-1.md)). That every circuit below the textbook holds "a wire that is flat on both sides, the transform's own eigenvector" is wrong beyond 4 points: the true statement is "not tight" ([a-2](a-2.md)), and the third note withdraws the eigenvector reading. "Nobody has an example" of badly conditioned steps whose product is perfectly conditioned is false as stated: [g-3](../wave-03/g-3.md) has a family at 16 points, and that family buys nothing. The "conservation law" is one bit per operation for rotation-like gates, and the 60 operations of [e2-0](../wave-02/e2-0.md) break it. See the line "Taken back by the critics" in [the first note](NOTE.md) and the line "Taken back or corrected" in [the second note](../wave-02/NOTE.md).

2026-10-10, 40-minute box. Private. Marks: [ran] = exact run of mine tonight (files in `i-cross/`), [derived] = by hand tonight,
[read] = from the d- and i- reports, [guess] = marked guess. Nothing here is reviewed, nothing is in Lean.

## 0. In five lines

- The eight developments describe **two** objects, not eight: the transform as an element of SL2 acting on k copies of a 2-point space
  (d-0, d-7, d-6, d-2), and the transform as a Clifford element fixing a quadratic form (d-3, d-4, d-1's Gauss sums). Section 1.
- They stop at **five** walls, and each wall was hit from at least two sides. Section 2.
- Three hybrids, each tried exactly. One removes a ceiling (the "max(a, 1/2)" in d-0's conditional becomes "log log"), one shows the whole
  question is a property of a class of kernels, one produced a new exact minimum (the antisymmetric square of the 4-point transform is a
  signed octahedron, 12 gates, no 10 or 11) and one more exact tie. Section 3.
- Most surprising: every reorganisation ties **to the last gate**, and the only thing that ever won is one kind of wire. Section 4.
- The question I would ask next is the one five ideas proposed independently and nobody ran: the cheapest basis of the mirror. Section 5.

## 1. Which facts explain each other

**A. d-0's Jordan basis is d-7's spin basis.** [ran, k = 2..8, `schur.py`] Take d-0's explicit Jordan basis of the add-one-element
operator U (matched pairs carry e_a - e_b, unmatched positions carry the sum of all i-subsets). It is word for word d-7's valence-bond basis.
In it, exactly: U is a weighted shift on each string; the subset-sum matrix Z = exp(U) is a Pascal block; the transform is
(-2)^(number of pairs) times a Krawtchouk block. Rank N checked modulo a large prime (non-zero determinant mod p implies non-zero over Q).
Consequences that were sitting in different reports:
- d-0's "H = Z D Z-transpose" is the lower-diagonal-upper factorisation of the 2 x 2 matrix, carried to every block:
  Krawtchouk = Pascal x diagonal x Pascal-transpose. d-7's K3 is the 3 x 3 Krawtchouk block.
- "On the antisymmetric part of two bits the transform is the number -2" [hatch] and "matched pairs carry e_a - e_b" [d-0] are one fact.
- The square root of log N: block size = number of unmatched positions = the spread of a binomial. It is the same square root in the
  leftover volume (d-0), the Schur block size (d-7), the overlap window and OpenAI's ceiling [guess for the last one].

**B. d-4's order-3 identity is d-3's quadratic form.** [derived] (T S/sqrt N)^3 = I with T = (-1)^Q0 is the relation "phase gate times
Hadamard has order 3". d-3's Z_4-valued form is the phase gate; its hidden symmetries y -> y + (y.v)v are the orthogonal group of the form;
d-3's "largest flat has dimension k/2", d-4's "a swap-kept basis shares at most k/2 directions" and d-0/d-7's "k/2 pairs" are all
"a maximal isotropic subspace has dimension k/2". d-3's invariant modulo 8 is the eighth root of unity in that order-3 relation [guess].

**C. The one helper.** [derived from read facts] The 7-gate brick's helper (i-play: "a sign vector with an odd number of minus signs,
distance 1 from every output") is u = (1,-1,-1,-1), a quadratic-form sign vector, i.e. one of d-4's eigenvectors (-1)^Q. It is the same
number before and after the transform (u.x = -(1/2) u.Hx). d-6's "non-product helper one flip from many outputs" at 13 gates is the same
kind of wire, and d-0's "overshoot and repay" helper is its triangular cousin. See wall W3.

**D. Unbounded coefficients.** d-0 ("the first pass must overshoot"), d-1 ("linear Rad needs large coefficients"), d-2 (the non-unitary
middle diagonal 1,-1,2,-2,3,-3,5,-5), d-3 ("far reach needs non-unitary steps"), d-5 (1/e) and Morgenstern say one thing. See W4.

**E. Parallel copies.** d-6's growth law, d-2's two-call lemma, d-7's "the basis change is a transform on every swap orbit", d-0's
recurrence cost(k) = 2 cost(k-1) + 2^(k-1), and my hybrid 3 all rewrite T(N) as cheap layers plus copies of smaller transforms on
disjoint data. See W2.

## 2. The walls, each stated once

**W1. Half and half (isotropy).** Any basis in which the transform becomes a relabelling with scalings is attached to a subspace that is
its own perpendicular, so it shares at most k/2 directions with the standard basis; getting in costs k/2 layers and getting out k/2.
Seen as: d-3's commuting floor (k/2 steps), d-4's overlap bound, d-0's "pair coupling costs k/4 per entry, twice that is Z's textbook",
d-7's exact tie "half in the basis change, half in the middle". [derived in the reports; the step "distance d = d layers" is recalled]

**W2. Direct sum.** "t copies of the n-point transform on disjoint data cost t times one." d-2 proved a case (two calls sharing a pairing:
both blocks are forced to be the half-size transform). d-6 stated the law (sharing a fraction above 1/2 at every size gives linear size).
Every identity found tonight ends in such copies. Note [derived]: a linear-size transform does NOT need copies to share (N copies at c N
each is already c N^2); the wall blocks every recursive route, not linear size as such.

**W3. Tight wires.** [guess, stated as a lemma to attack] Every wire of a circuit is a linear form; write it once in the inputs (s
non-zeros) and once in the outputs (s' non-zeros). Then s s' >= N, with equality exactly for "a character on a coset". The textbook and
every route that tied tonight use only equality wires. Every circuit that beat the textbook at small size contains a wire that is flat on
both sides (s s' = N^2). Conjecture: a circuit made only of equality wires needs N log2 N gates. If true, the to-do list is its hypothesis:
programs whose wires are mostly not coset characters.

**W4. Exactness.** With coefficients of bounded size the determinant forces N log N (Morgenstern; d-1's line-sum version; d-0's
cancellation-free version); a limit of cheap programs converts to an exact one at (d+1)^2 (d-5); a unitary linear-size step spreads a row
by O(1) bits (hatch: weight at tree distance d is at most 8 * 2^-d). One statement: **a linear-size program must be a product of badly
conditioned steps whose product is perfectly conditioned.** Nobody has an example of that shape for any flat unitary matrix.

**W5. One class.** [ran, `univ.py`, exact rationals, k = 2, 3, 4] Z = D H D H D H D H D with
D's = diag(1/32, 1/10), diag(3,1), diag(3,-2), diag(2,1), diag(1,-5/9), and the same holds for every tensor power with the product
diagonals; H = Z D Z-transpose; H diag(3,1) H and H diag(2,1) H are the full kernels with invariant tau = 4 and 9 (any tau other than 0, 1,
infinity is reached by two calls over the complex numbers [derived]). So cost(Z) <= 4 cost(H) + 5N, cost(H) <= 2 cost(Z) + N, and every
2 x 2 kernel with no zero entry costs at most 2 cost(H) + 3N. **Linear size, and the exponent z, are properties of the whole class of
Kronecker powers of an invertible 2 x 2 matrix that is not a relabelling.** This is a wall in the sense that no fact special to
t = -i (modulo 4, Clifford, E8, reflection) can be needed for the truth of "linear size"; it can still be the mechanism.

## 3. Three hybrids, each tried

### Hybrid 1. "One class": take d-0's Z-equivalence, d-3's "the generic point has the same floor", i-cousins' invariant tau

Idea: stop asking about the Walsh-Hadamard matrix; ask about the class, and choose the member that suits the tool.
Tried: `univ.py` above [ran]. What it gives:
- Lower-bound hunters should use Z (subset sums): it is the member with **no** small gain (4 and 12 gates at 4 and 8 points are exact
  minima in four fields, d-0), while H has one at 4 points (7 against 8). The gain at 4 points lives where the down pass meets the up pass.
- Construction hunters may use any member: a brick for a generic tau is a brick for H at twice the price.
- By-product for another community [derived; literature not checked tonight, mark as a lead]: the published exponent transfers to the
  **zeta / Moebius transform on the subset lattice** over the rationals: N (log N)^z operations with z = 1 - 8.7625e-4, against the
  k 2^(k-1) additions of Yates's method that exact-algorithm papers treat as the cost. Check dates and whether anyone states it.

### Hybrid 2. "Schur ledger": put d-7's spin basis into d-0's conditional, and a fast Pascal block into both

d-0 was stuck at: cost(Z) <= 2 cost(B) + O(N sqrt(log N)) for a Jordan basis change B, hence exponent max(a, 1/2). d-7 was stuck at:
dense middle 1.6 sqrt(k) per entry. Working piece from outside both: a Pascal block of size m is a Taylor shift, which is a convolution
with a fixed vector, O(m log m) operations with unbounded coefficients [recalled, standard; not re-derived].
Tried [ran, `schur.py`]: with multiplicities C(k,w) - C(k,w-1) and block size m = k - 2w + 1 the middle per entry is

| k | dense blocks | m log2 m model |
|---|---|---|
| 16 | 6.48 | 2.55 |
| 64 | 12.82 | 3.53 |
| 256 | 25.56 | 4.53 |
| 1024 | 51.08 | 5.53 |

(the dense column reproduces d-7's numbers; the model column is (1/2) log2 k + 0.5). So [derived]:
**T(N) <= cost(B) + cost(B^-1) + O(N log log N) for any Jordan basis change B of U.** The ceiling 1/2 is gone: a linear-size Jordan basis
would give N log log N. The whole log is in a basis change that does not depend on the kernel.
Where it stops [derived]: a pair-coupling tree for B obeys t_B(k) = 2 t_B(k/2) + c(k), so t_B(k) = k * sum c(2^i)/2^i >= k/4 from the
first level alone; in and out is k/2, half the textbook, before any higher coupling. A cheap B cannot be a tree of couplings.

### Hybrid 3. "Squares": d-7's untried two-block swap, with the 7-gate brick (i-play, i-cousins) and slice coordinates (x, x+y)

d-7 left "the symmetric square (10 x 10) and antisymmetric square (6 x 6) of the 4-point transform" as a mutation. 16 points = a 4 x 4
array F, transform = H F H, swap of the two digits = transpose. Working piece (mine, in the spirit of i-model's Zak coordinates): index the array by (x, m = x + y). Then [derived]
the entry (output pair u,v ; input pair x,y) vanishes unless (u+v).(x+y) = 0 (symmetric part) or = 1 (antisymmetric part).
Tried [ran, `squares.py`, `alt4_min.out`]:
- **Antisymmetric square of the 4-point transform = 2 x a signed octahedron** (6 x 6, four non-zeros per row, square = 16 I): two layers
  of three butterflies, **12 gates**. Exhaustive search (d-0's mincirc): no circuit with 10 or 11 gates over GF(3) or GF(5)
  (29.2 million last-level states at GF(5)). Not a proof over Q, as in d-0.
- Symmetric square: 26 gates by replay (two 7-gate blocks, three butterflies, three butterflies). Not minimised; lower bound 18.
- 16 points by this route: 12 (split) + 26 + 12 + 12 (merge) = **62**. Between the textbook's 64 and the known 56.
- General q: **T(q^2) <= 2(q^2 - q) + 2 T(q) + 4(q - 1) T(q/2)**, and at textbook prices the right side equals the left exactly at
  every size [arithmetic ran, q = 2..1024]. Structure behind it [ran, `slices.py`, q = 4, 8, 16, i.e. 16, 64, 256 points]: every block
  (output slice w, input slice m) of either square is zero or of rank one with a flat factor; the zero pattern is the one above; on each
  slice the factors form a full transform of the slice's size. So the middle is: transform every slice, one number per block, transform
  every output slice. At 256 points the antisymmetric square has 120 blocks, one per pair of 16 points. The split is one butterfly layer along the orbits of a linear involution of the
  addresses (not along a translation): an "address relabelling that mixes columns" from the floor note's hatch list. It trades
  exactly one layer for one layer, and the middle is 4(q-1) half-size transforms on disjoint slices: wall W2 again.
- To beat 56 this way the symmetric square would need 19 gates (one above its connectivity bound). I do not expect it [guess].

## 4. The most surprising thing

Not one of tonight's reorganisations is "about" the textbook count; each is **exactly** it: d-7's pair scheme (k N at k = 2..32), d-0's
chains (32 at 16 points, 12 at 8), d-1's level cost, hybrid 3's identity (all q), i-wild's "64 three times", i-model's "something is
conserved". Different mathematics, same integer. And against that, the single thing that ever went below, in four separate reports, is
one object: a wire that is flat on both sides, the transform's own eigenvector. A tie to the last gate from five directions is what a
conservation law looks like; W3 is my guess at its statement.

## 5. The question that would tell the most, and its experiment

**What is the cheapest basis of the mirror?** The transform (relabelled, symmetric form) is sqrt(N) (I - 2 E C), where C reads the
r = N/2 - sqrt(N)/2 coordinates of the -sqrt(N) eigenspace and E puts them back; ANY basis of that eigenspace will do.
[derived] T(N) <= cost(C) + cost(E) + N, and conversely a linear-size transform gives a linear-size C (apply it, subtract, keep r outputs).
So "linear size" is exactly "the mirror has a basis that costs O(1) gates per form, in and out". Proposed independently by d-2
(mutation 4), d-4 (mutations 1 and 4), d-6 (mutation 7), i-backwards (31) and i-wild (66); run by nobody.
Why it is the informative form: the target is a subspace, so the freedom is all of GL(r), which no tensor recursion sees; and the extreme
case is checkable by hand [derived]: one tree of sums yields at most sqrt(N) independent eigenforms (a tree block carrying an eigenform has
at least sqrt(N) points), so r forms need about sqrt(N)/2 trees that reuse each other's wires. Whether they can is the question.
Experiment (finite, 16 wires): exact least number of gates for ANY 6 forms spanning the eigenform space at 16 points (family target in
d-0's search, GF(3) and GF(5)); lower bound 20, the character basis costs 34 by my hand count [derived, not replayed].
Reading: near 20 means the freedom is real and the count per form is flat at the first size where it could fail; near 34 means the mirror
ties like everything else. Then the same at 64 points (r = 28) by heuristic, to see the per-form trend.

## 6. Three objects for skeptics

1. **Identity (W5 and Hybrid 2).** Claims: Z = D H D H D H D H D with the five rational diagonals above, for every tensor power; hence
   linear size and the exponent are class properties; and T(N) <= cost(B) + cost(B^-1) + O(N log log N) for any Jordan basis change B of U.
   Weakest joint: the O(m log m) Pascal block (recalled, needs complex roots of unity and unbounded coefficients; check it is a legal
   program in OpenAI's count).
2. **Circuit (Hybrid 3).** Claims: the antisymmetric square of the 4-point transform has exactly 12 gates (upper bound by replay, lower
   bound exhaustive over GF(3) and GF(5) only); the symmetric square has at most 26; the identity
   T(q^2) <= 2(q^2-q) + 2T(q) + 4(q-1)T(q/2) for every q (gate-by-gate replay only at q = 4; block structure checked at q = 4, 8, 16).
3. **Conjecture (W3).** Claim: a linear circuit for the N-point transform all of whose wires are characters on cosets has at least
   N log2 N gates (free scalings), and every circuit below that count contains a wire with s s' > N. Evidence: small cases only.
   A counterexample would be a tying or winning circuit of a new kind; a proof would say what a linear program must be made of.

## 7. Criticism, last

- Sections 1B, W3 and the "conservation law" are readings, not results. W3's definition of s' assumes the form is written in the outputs
  through the inverse transform; I checked it against the 4-point brick only.
- Hybrid 1 moves constants (factors 2 and 4); it changes what may be assumed, not any count.
- Hybrid 2's gain is conditional on a basis change nobody has; its own first level already costs half the textbook.
- Hybrid 3 saved nothing; its value is one exact minimum and one more exact tie.
- I did not read the web tonight. The zeta-transform lead needs a dated literature check before anyone repeats it.

Files: `waves/wave-01/i-cross/` : univ.py, univ.out; schur.py, schur.out; squares.py,
squares.out, rows_alt4.txt, rows_sym4.txt, alt4_min.out; slices.py, slices.out.
