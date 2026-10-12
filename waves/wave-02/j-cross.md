# j-cross: both waves side by side, four hybrids tried, and what to ask next

2026-10-10, 23:04 to 23:44 EDT, 40-minute box. Private research: nothing published, no git, no Lean, nothing reviewed.
Marks: [ran] = exact run of mine tonight (files in `j-cross/`), [derived] = by hand tonight, [read] = from tonight's reports
(d-*, e-*, e2-*, a-*, g-0, NOTE.md, i-cross.md), [guess] = marked guess.
Gate counts: (G) = a gate is any a*u + b*v, scalings free. (O) = OpenAI's count, every addition and every multiplication by a constant charged.
Words. N = 2^k points. *Wire*: any linear form a program holds. For a wire, s = number of non-zeros when it is written in the inputs,
s' = number of non-zeros when it is written in the outputs. Always s*s' >= N (the uncertainty principle); a wire is *tight* when
s*s' = N, *over the limit* otherwise. *Product wire*: a wire that is a tensor product of one 2-vector per address bit; a wire is
*entangled on a bit* when cutting that bit from the rest does not split it into a product. *Hub*: a wire that is one gate from several outputs.

## 0. In seven lines

- Twenty developments stop at **four walls**, and each wall is now a lemma somebody proved in a restricted class (section 2).
- Read with three meters taken from three different reports, the wave's record (e2-0's programs, 7, 20, 52, 128, 304 gates (G))
  is the same thing at every size: **the gates saved equal the number of over-limit wires, exactly; every one of those wires has
  s*s' = 4N and is entangled on exactly two adjacent address bits; everything else is a tight product wire** [ran]. Hybrid 1.
- A new lemma: **a program whose wires are all product wires needs N log2 N gates, whatever the sizes of its coefficients**
  [derived; 4-point case exhaustive]. With blocks of b bits it is N log2 N / b. So large coefficients alone buy nothing; a saving
  needs entangled wires, and linear size needs wires entangled across a number of bits that grows with N. Hybrid 2.
- The last unexplained anomaly of the first list (the singular half-arc blocks) is **tight wires again**: the null vectors are
  characters on small cosets that happen to sit inside half of the multiplicative circle [ran at 16 and 64 points]. Not a door. Hybrid 3.
- **The 7-gate brick is not special to the Walsh-Hadamard matrix**: for every 2 x 2 kernel [[1,1],[1,tau]], kernel x kernel =
  (one rank-one matrix) + (tau - 1) * (a signed relabelling) [derived; ran on 948 kernels]. What is special to the transform is the mirror, not the hub. Hybrid 4.
- The question that would tell the most: **can one over-limit wire ever save more than one gate?** If never, the order is N log N
  (it would give (1/2) N log2 N as a lower bound); linear size needs about (1/2) log2 N gates saved per wire. First size where it can show: 8 points.
- I replayed e2-0's programs with my own parser: (G) at 4 to 64 points and (O) at 4, 16, 64 points (8, 60, 352 operations for H x / sqrt N) all check [ran].

## 1. Facts that explain each other (across the two waves)

1. **e2-0's staircase is e2-3's cancellation ladder and a-2's over-limit wires, one for one.** [ran, `meters.out`] For N = 4..64:
   gates 7, 20, 52, 128, 304; saving below N log2 N = 1, 4, 12, 32, 80 = (N/4)(k-1); over-limit wires 1, 4, 12, 32, 80, each with
   s*s' = 4N, each entangled on two adjacent bits; outputs at cancellation depth k-1 or k (e2-3's meter: the number of gates on a path
   that add two forms sharing an input). e2-3's guess "depth D saves at most (N/4) D" holds with exactly one unit of slack at every size.
2. **e-5's "one bit per operation" is what a-2's tight-wire theorem looks like in count (O), and e2-0 is the first single-array program that
   breaks it.** [ran] 64 bits in 60 operations at 16 points (1.067 per operation), 384 in 352 at 64 points (1.091); the only constant is 1/2
   (8 and 48 halvings). e-5 proved the law only for butterflies and sum-of-four gates; [guess] its annealer missed 60 because the hub steps are not reflections.
3. **e-1's question B is answered by e-4.** e-1 asked for an invertible K with K and K*h both cheap and proposed nested rows (running sums).
   e-4's corner theorem says that with one running-sum order per side at least (d/2) log2 d entries survive, and its sketch says about d^(3/2) [read].
   Chains with one order per side are out; several orders per side are what is left.
4. **e-7's "child length + rank of the remainder >= N", e-3's "the leftover is the whole transform again", e-6's "a collapse is a direct
   program", e2-1's "other transform + bridge = textbook", g-0's "the mirror route gives 56 by proof" and d-7 / g-2's "the basis change
   contains the transform" are one statement**: every split into a cheap part and a remainder leaves transforms of total length N. Wall S below.
5. **The square root that would not go away** (first wave: block size, overlap window, leftover volume) now has two more members with
   reasons: e-3's cut-off degree 2.2 sqrt(k) is the binomial's spread, and e-0's "a denominator buys sqrt(k / 2 pi) per entry" is the
   mean absolute deviation of the same binomial [read]. One distribution, five readings.
6. **Order-3 relations are one relation.** d-4's (T S)^3 = 1, e-0's product formula with the cube root of unity, and e-6's fractional-linear
   side door are images of the relation (x -> 1/(x+1))^3 = identity. [derived] And e-6's hope that a long word in that group beats two
   transforms cannot work: every element of the group is (free) * (inversion) * (free) or free (the Bruhat decomposition, recalled), so
   every word identity only says "the dense matrix equals free * itself * free".
7. **e2-1's two escape conditions meet e2-0's record and my lemma.** e2-1: a linear program needs values of several magnitudes and
   three-term relations that jump levels. Hybrid 2 shows the first without the second is worth nothing (product wires of any
   magnitudes give N log2 N). The record has the second with coefficients 1 and 2 only.
8. **g-0's "ties at 56" and e2-0's 52 are not in conflict**: the 52-gate program does not pass through the six mirror coordinates.
   With Hybrid 4 this reads: the mirror is special to the transform and ties; the hub is common to the whole class and wins.

## 2. The walls, each stated once, with who hit it

**Wall U (uncertainty, the tight-wire wall).** A program whose wires are all tight needs N log2 N gates [a-2, proved]. The same wall:
e2-1 Theorem A (coset characters), e2-3 lemma 1 (no gate adds two forms sharing an input), e-1's coset-atom lemma
(cost(F) + cost(S F) >= |F| log2 N), e-4's corner theorem (a rank-one block has area at most d), e2-3's Parseval drain law, e-2's
"an eigenvector has at least sqrt N entries", e-7 Lemma 1, d-0's cancellation-free count, and now Hybrid 2 (product wires) and
Hybrid 3 (the half-arc null vectors). Hypothesis to break: use over-limit, entangled wires.

**Wall M (one magnitude).** If every value is, up to scale, a 0/+1/-1 vector, the gates have |a| + |b| <= 3 and Morgenstern gives
0.315 N log2 N [e2-1 B, e2-0, failproof]. Same wall: e-5 (rotation gates make at most about 1.2 bits per operation), e-0 (numerators
only: (k-2)/2), e-3 (the leftover has the determinant of H), first wave W4. Hypothesis to break: values with magnitude ratios growing with N.
[derived, Hybrid 2] Breaking M without breaking U is worthless.

**Wall C (commuting steps, half and half).** Steps that commute, or that live in one commutative ring, need k/2 of them, each of cost
at least N: d-3, e-6 (at least ceil(k/2) flags), e-0 (both rings), e-4 (all passes on one side: log2 d + 1 letters), first wave W1.
A constant factor at best. Hypothesis to break: alternate two kinds of step that do not commute (e-0 mutation 2, e-4 mutation 1; not run by anyone).

**Wall S (self-similarity, or volume).** Every identity "transform = cheap * (smaller transforms) * cheap + sparse" has smaller
transforms of total length at least N [e-7 Lemma 5; e-3; e-6; e2-1; g-0; d-7; first wave W2]. Hypothesis to break, in two places
only: (i) parts that change with N (e-7's half child plus quarter child, where its slack law leaves room); (ii) copies that share,
which is how the published result saves and which e2-2's clique lemma limits for the old letters.

No wall covers a program that is at once: made of entangled over-limit wires, with growing magnitudes, non-commuting, and not a recursion on copies.

## 3. The four anomalies at the end of PICKS.md

- **"64 came back in every count; something is conserved".** Explained, and then broken. It is N log2 N bits made at one bit per (O)
  operation by rotation gates [e-5], equivalently wall U [a-2]. e2-0's 60 at 16 points (for H x / 4) is below it [ran: replayed].
- **(N - sqrt N)/2 = 1, 6, 28, 120.** Explained as one fact [derived from e-1, g-0, d-4]: "N signs that sum to sqrt N have that many
  minus signs", read three times (the trace of a symmetric flat matrix with diagonal +1; a bent sign vector against a character; a
  quadratic form's odd points). e-1 and g-0 add the geometry: the N sparsest vectors of that space are equiangular lines.
- **Encoder sizes 30, 34, 39, 60.** Explained by e-2: encoder columns are codewords of weight 6, 8 or 11 and only four mixtures occur [read].
- **The singular Hankel block.** e-0 corrected the statement (it depends on the starting point; even k only). Mechanism found here, Hybrid 3.

## 4. Four hybrids, each tried

### Hybrid 1. Three meters on the record (e2-3's depth, a-2's s*s', e-5's bits, read on e2-0's programs)

Stuck: e2-3 had a guessed law and only its own circuits; a-2 had a slack inequality nobody had seen tight; e-5 had a law and no exception.
Working piece: e2-0's explicit programs. Tried [ran, `meters.py`, `meters.out`, `budget.py`, `budget.out`]: the table in section 1,
item 1, and for the two 21-gate circuits of the wave: saving 3 with 6 over-limit wires (e-2) and 11 (e2-3), several of them entangled
on all three bits with s*s' = 8N. So the wide wires exist at 8 points, and the circuits that use them save less than the staircase that does not.
Two laws to attack, both [guess]:
- **L1 (one gate per wire): gates saved <= number of over-limit wires.** Holds in all seven circuits (1/1, 4/4, 12/12, 32/32, 80/80, 3/6, 3/11).
  [derived] L1 would give gates >= (1/2) N log2 N, a superlinear lower bound, so by the published result it must fail at very large
  size (if the published program reads as a circuit in count (G), which I assume and did not check).
- **L2 (budget): gates saved <= (1/2) * sum over wires of log2(s*s'/N).** Tight on e2-0's family and the brick, slack on the two 21s
  (6.6 and 13.6 against 3). [derived] L2 allows linear size and then asks for at least about 2N wires, nearly all flat on both
  sides; in the limit it is the known bound 2N - 2.
The truth between L1 and L2 is the order question in one number: gates saved per over-limit wire.

### Hybrid 2. Entangled wires (e2-1's Theorem A, freed from its magnitudes; the stabiliser language of d-4 and e-4)

Stuck: e2-1 asked for values with growing magnitudes and proposed rows of t^(Hamming distance) on flats. Working piece: Theorem A's level count.
**Lemma [derived].** If every wire is a product wire (any entries), a gate a*u + b*v = w forces u and v to agree in all bits but one,
so each gate "is born along" one bit. Fix a bit i. The wires whose i-th factor is (1,1) are either born along i or made from two
wires with the same i-th factor, so the other-bits parts of those born along i must span N/2 dimensions; the same for (1,-1).
Hence at least N gates per bit, N log2 N in all. With a fixed partition of the bits into blocks of b and wires that are products
across blocks: at least N per block, N log2 N / b in all. [ran, `prod4.py`] 4 points, coordinates as labels (8 labels per axis, enough
for every program of at most 8 gates): no product-wire program with 4, 5, 6 or 7 gates; 8 reached. The hub (1,1,1,-1) is the smallest non-product wire.
What it says: the brick is "blocks of 2" (bound 1/2, reached 7/8); the staircase is "pairs that overlap" (no fixed partition, reached 3/4);
linear size needs wires entangled across about log N bits at once, or partitions that change from wire to wire. Not covered: wires
that are sums of two product wires in different partitions.

### Hybrid 3. The half-arc null vectors are tight atoms (e-0's anomaly, a-2's tight wires, d-1's multiplicative order)

Stuck: e-0 found inputs on half the multiplicative circle whose transform vanishes on half of it and proposed them for the hatch
"blocks only on known zeros". Tried [ran, `arc16.py`, `arc16.out`, exact rationals]: at 16 points all 7 singular starting points have
null spaces spanned by vectors with 4 non-zeros whose transform has 4 non-zeros (s*s' = 16 = N): a character on a coset of a
2-dimensional subgroup, for example signs (-,+,-,+) on theta^5, theta^7, theta^9, theta^10, with transform on theta^9, theta^11,
theta^13, theta^14; or sums of two shifted copies sharing a point. At 64 points the two I opened in the long runs have 8 and 8
non-zeros (tight again); a third has 14 and 14 and I did not decompose it. [derived] The profile 1, 2, .., r, r, .., 2, 1 is the number of multiplicative shifts of one such
atom that keep both supports inside their arcs. Even k only, because only then is there an atom with s = s' = sqrt N. [guess] It fades
with k because an additive coset cannot stay inside a short multiplicative arc (the sum-product phenomenon). So these zeros are
the equality cases of wall U and give no block that the textbook does not already have.

### Hybrid 4. The hub belongs to the whole class (first wave W5 "one class", put under the brick)

Stuck: everyone treated the 7-gate brick as a property of the transform's own point. Working piece: W5 says the order is a property
of all 2 x 2 kernels with no zero entry. Tried [ran, `hubclass.py`, `hubclass.out`]: 948 kernels [[1,a],[b,c]], 49 values of the
invariant tau = c/(ab): every one has (kernel x kernel) = rank one + one non-zero per row and column.
**Identity [derived, all 16 entries by hand]:** for K = [[1,1],[1,tau]], K x K = u u^T + (tau - 1)(E11 + E22 - E03 - E30), u = (1,1,1,tau).
So every such kernel has the 7-gate brick, and every Kronecker power costs at most (7/8) N log2 N in (G). At tau = -1, and only there, the relabelling P
fixes u and K x K = -2 P (I - u u^T / 2): a relabelling times a reflection, which is where the mirror of dimension N/2 - sqrt(N)/2
comes from; for other tau the rank-one-plus-relabelling form does not survive tensor powers as a small mirror [derived, not run].
Reading: of the two special-looking objects, the hub is class-wide and is what wins; the mirror is point-special and ties.
Not tried: whether e2-0's staircase (3/4) also exists for every tau.

## 5. The most surprising thing, and the question that would tell the most

**Most surprising.** A (3/4) N log2 N family exists (the first wave's best rate was 7/8), its (O) form computes H x / 4 at 16
points in 60 operations against the textbook's 64, and under the meters it is as plain as it could be: one saved gate per over-limit
wire, every such wire the smallest entangled wire there is, coefficients 1 and 2. Nothing found tonight saves more than one gate per over-limit wire.

**The question.** Can one over-limit wire save more than one gate? Linear size needs the saving per wire to grow like
(1/2) log2 N; L1 says it is 1 for ever. **Experiment (finite):** at 8 points, search exactly for a circuit with
(gates) + (over-limit wires) < 24, that is 20 gates with at most 3 over-limit wires or 19 with at most 4, in a pool that contains
the 240 stabiliser vectors and the sign and 0/+1/-1/+2/-2 vectors entangled on three bits (s*s' = 8N is the first spread that L2
lets save 1.5). Then 16 points: gates + over-limit wires < 64 (the record has 52 + 12 = 64). A hit is the first wire that pays
more than its keep and shows what such a wire looks like; a clean "none" at 8 and 16 points, with the 21s' waste explained, is the
strongest small-size evidence yet for N log N. Each candidate modulo a prime must be lifted and replayed exactly.

## 6. Three objects for skeptics

1. **Circuit family (e2-0).** Claims: 20 gates (G) at 8 points; (3/4) N log2 N + N/4 at every N; in (O), H x / sqrt N in
   (7/8) N log2 N + N/4 operations for N a power of 4 (60 at 16 points, 352 at 64), said to improve both leading constants of Alman
   and Rao. Where: `e2-0-pieces/slp_8.txt`, `slp_16.txt`, `oslp_16.txt`, `oslp_64.txt`, `gen.py`. My replay agrees through 64 points.
   Attack: whether OpenAI's statement and count accept H x / sqrt N and a halving as one operation; the formula beyond 64 points; a
   dated literature check; the wall lemma "two-piece hubs on one chain end at 3/4". A developer hour on the (O) side would price the
   programs with the project's own checker and OpenAI's files (R/OAI, read only), including H x itself and sizes that are not powers of 4.
2. **Lemma (e2-2, clique lemma) with the solver's uniqueness claim.** Claims: in an old-letter unit with W live arrays and any
   scratch arrays, blocks pairwise selected together by tight forms number at most W; hence 4 arrays need all 16 moves at block size 4
   and at least 17 of 20 at block size 5. Where: `e2-2.md` section 2, `e2-2-ladder/clique.py`, `uniq.out`, `uniq5.out`. It is the
   only statement of the wave that bears on a saving of 1e-1 inside the engine (17 of 20 would be 1.0e-1); if it is wrong, the 16-of-20 design that counting allows is back.
3. **Law (e-7, Lemma 4, the slack law).** Claims: for a remainder sqrt(N) times a relabelling and a middle of rho*N numbers, each row
   of the outer sparse matrix needs at least rho / (2 sqrt(rho - 1/2 + 1/(2 sqrt N))) entries; unbounded at rho = 1/2, 0.75 at
   rho = 3/4, so the floor note's obstruction is gone for one half child plus one quarter child (still linear). Where: `e-7.md`
   section 4. Derived once, never re-derived; it is the only "door" claimed in the wave.

## 7. Eight experiments for the next wave (one hour each)

1. **`onepergate` (deepen).** Section 5's experiment: 8 points, gates + over-limit wires < 24; then 16 points < 64. Report s, s', entangled bits of every wire of every hit.
2. **`staircase3` (deepen).** Extend e2-0's generator to hubs that join four quarter pieces of four characters (entangled on three
   adjacent bits), partners three levels down. Its wall lemma does not cover this. Target: 8 points in 19, 16 points under 52; the rate for a window of w bits.
3. **`clique17` (deepen, the 1e-1 case).** e2-2's smallest open case: 4 arrays in 17 moves at block size 5, old letters with scratch arrays. Exact search or a proof from the clique lemma.
4. **`zetafloor` (nobody tried).** Linear size is a class property, and subset sums have no hub (4 and 12 are exact minima). Find the
   exact minimum for subset sums at 16 points with entangled wires allowed (is it 32?), and try to prove (N/2) log2 N for subset sums
   from the product-wire lemma plus one entangled wire. A proof at all sizes would settle the order for the whole class.
5. **`ladderbound` (nobody tried).** Prove or break: programs whose wires are entangled on at most two bits (any pair, changing from
   wire to wire) need (3/4) N log2 N. Exhaustive at 8 points over product-times-one-pair wires with label coordinates as in `prod4.py`.
6. **`classhub` (nobody tried).** With K x K = u u^T + (tau - 1) P: build the staircase for tau = 2 and tau = 1/3; then let tau go
   to infinity (the kernel tends to subset sums) and record at which tau each saved gate disappears.
7. **`unitmeter` (hybrid: e2-2's batch law, e-5's bits, a-2's s*s', L1).** Read the published unit as a circuit on its 1,263 arrays
   and compute, per wire, s, s' and the moves saved per over-limit wire. It is the only known program that must break L1; find the wires that do it.
8. **`provethewrongthing` (silly).** Try to prove L1, hence (1/2) N log2 N, by charging each saved gate to one over-limit wire in
   a-2's level count. The published result says the proof must fail; the step where it fails is the shape of an order-changing gate.

## 8. Criticism, last

- L1 and L2 are guesses read off seven circuits, five of them one family. L2's constant 1/2 is fitted to that family.
- The product-wire lemma is derived once, by me, tonight; the run covers 4 points only (the 8-point run in `prod4.out` used 4 labels and stopped at 12 gates: a sanity run).
- Hybrid 3 explains 16 points fully and 64 points in part; "fades with k" is a guess; I did not test odd k beyond e-0's data.
- Hybrid 4's identity is elementary and may be folklore; the sentence about the mirror for other tau is by hand only.
- "The published program is a circuit in count (G)" is assumed, not checked against the engine.
- I did not read the web. The second 21-gate circuit's over-limit count (11) differs from NOTE.md's "6 of 21", which was the other circuit.
- The Mac's shared runner had no free slot at first; `meters`, `arc16`, `prod4` ran once on the Linux machine (`*.lx.out`, copied back) and again here (`*.out`); the two agree.

Files: `waves/wave-02/j-cross/`: meters.py, meters.out; budget.py, budget.out; prod4.py,
prod4.out, prod4.lx.out; arc16.py, arc16.out; hubclass.py, hubclass.out.
