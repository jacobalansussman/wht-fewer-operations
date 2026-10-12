# wht39 / ideas / WAVE3-PICKS: eight briefs for an hour each

2026-10-10, 15-minute box, curator `k-pick`. Private. I ran nothing. Marks: [read] = read tonight in the file named,
[derived] = by hand tonight by me, unchecked, [guess] = marked guess. Counts: (G) a gate is any a*u + b*v, scalings free;
(O) OpenAI's count, additions and scalar multiplications each charged. Say which one every time.
Read in full: `i-cross.md`, `a-0.md` (verdict, section 3), `a-1.md` (verdict, section 6), `a-2.md` (verdict, sections 1, 2, 6, 7).
Read in part: the search, mutation and closing sections of `d-0.md` to `d-7.md`; the leftover lists of `PICKS.md`, `WAVE2-PICKS.md`,
`WAVE2-PICKS-B.md`. Not read: the e- and e2- reports. `NOTE.md` had not landed.

## Notes for all eight developers

1. **The skeptics have landed and they change three briefs.** [read]
   - `a-2.md`: the tight-wire conjecture (i-cross W3) is PROVED by hand for every N = 2^k in ten lines (section 2), and one part of
     the reading is wrong: at 16 points the helpers of the 56-gate circuit have s s' = 4N, not N^2. A stronger inequality with slack
     is in section 6. Unreviewed.
   - `a-0.md`: the subset-sum matrix is THREE calls of the transform, not four; "every kernel is two calls" is false over the
     rationals (true statement: constants 4 and 6); "any Jordan basis of U" is false for the transform at 4 points (true for the
     subset-sum matrix, and for the transform with the bases named in brief 3).
   - `a-1.md`: i-cross Hybrid 3 (the squares) is the textbook circuit in other coordinates; it is not picked again.
2. **Tool facts.** [read: `d-0-zeta/mincirc.c` header; `j-machine/steiner.py` header]
   - `mincirc p n m [rowsfile]`: exhaustive over GF(p), count (G), fixed target rows, n even, and p^n at most about 6 million.
     So 8 wires work for p = 3, 5, 7; 10 wires for p = 3 (5^10 = 9.8 million is just over); **16 wires work as written only over
     GF(2)**, where all signs are lost. 3^16 = 43 million needs larger tables (Linux machine); 5^16 does not fit any table.
     It has no "family target": that has to be added (stop when the available points lying in a given subspace reach full rank).
     Its shortcut "take a target the moment it lies on a line" is argued for fixed targets only; for a family it needs its own
     argument or must be dropped [derived, my caution].
   - `steiner.py <task> <seconds> <seed> <outdir> [mode] [temp] [goal]`: heuristic, searches helper forms only, count (G),
     replays every new best in exact fractions. `slp.py` does not work.
   - A circuit found modulo a prime is a candidate until lifted and replayed exactly. "None modulo p" is not "none".
3. Known small circuits to take apart: 7 gates at 4 points, 22 at 8, 56 at 16, 336 at 64, in `i-play/replay.py`, `replay.out`
   [read: `i-play.md` 1.1]. Exact minima: 4 points need exactly 7 in (G) and 8 in (O); 8 points between 15 and 22 [`j-failproof.md`].
4. Do not repeat wave 2: ring, vcycle, density, cutoff, passes, conserved, shifts, halftouch, pieces, dictionary, ladder, drain.
   Read the neighbour's report (`e-*.md`, `e2-*.md`) if your brief names one.
5. Generation first, play second, criticism last. Report the growth law you see, not only the count.

---

## Brief 1. `mirror`: the cheapest basis of the mirror

**Object.** [read: `d-4.md` section 4; `i-cross.md` section 5] Relabel the columns so the kernel is (-1)^(p1.y2 + p2.y1), the
address cut in two halves: the matrix S is symmetric with diagonal +1. S = sqrt(N) (I - 2 E C). The -sqrt(N) eigenspace has
dimension r = N/2 - sqrt(N)/2 (1, 6, 28, 120) and is spanned by the sign vectors (-1)^Q of the "elliptic" quadratic forms Q.
C is ANY r independent forms from that space, E puts them back. T(N) <= cost(C) + cost(E) + N, and a linear-size transform gives
a linear-size C. So linear size is exactly: the mirror has a basis costing O(1) gates per form, in and out.
**Known ends at 16 points (r = 6), count (G).** Lower bound 20 and character basis 34 [i-cross, hand counts, not replayed];
38 for the six coefficients on the quadric [d-4]; six separate reflections 66 in all [i-cousins].
**First experiment.** The exact least number of gates for any 6 independent forms in the eigenspace at 16 points: add the family
target to mincirc (note 2), GF(3) with enlarged tables and a second prime by a restricted search; replay over the rationals whatever
is found. Then cost(E) for the same basis (if the six forms are not perpendicular a 6 x 6 Gram inverse sits in between: count it).
Then 64 points (r = 28) with steiner.py, and 256 if it runs.
**Reading.** Report c(N) = cost(C)/r at 16, 64, 256. Near 20 at 16 points and flat c: the freedom of choosing the basis is real.
Near 34 and c growing like log N: the mirror ties like everything else. The 16-point total will not beat 56 even at the lower
bound (20 + about 30 + 16) [derived, rough]: this is a trend experiment, not a record attempt.
**Material.** Every eigenform has at least sqrt(N) non-zeros (s = s', s s' >= N [a-2]), so a form built alone costs sqrt(N) - 1:
everything is in sharing. One tree of sums yields at most sqrt(N) independent eigenforms [i-cross]. The mirror is the graph
{(u, -u - sqrt2 Q'u)} over the half cube, Q' the half-size normalised transform [d-2, regularity 3]. Try also the +sqrt(N) space.

## Brief 2. `tightwires`: the proved lemma, its slack, and programs built on over-spread wires

**Object.** [read: `a-2.md`] A wire is a linear form; s = non-zeros written in the inputs, s' = non-zeros written in the outputs.
s s' >= N, equality exactly for a character on a coset ("tight"). a-2 proves: tight wires only => at least N log2 N gates (every
level holds N wires; a gate's three levels differ by at most one). With slack: **the sum over gates of log2(1 + 2 P_g / N) is at
least N log2 N**, P_g the largest s s' among the gate's three wires. So cN gates force a wire with s s' >= (N^(1+1/c) - N)/2, a
fixed brick on q points tensored up saves at most a factor log2(1 + 2q), and in a linear program the over-spread wire is the bulk.
**Do.** (a) Referee: rewrite a-2's proof independently, machine-check the gate lemma on all triples at 4, 8, 16, and the slack
inequality on random circuits. Check that 7 is the least at 4 points over ALL coefficients (a-2 tested entries 0, 1, -1 only).
(b) Take apart the winners (note 3): for the 7-, 22-, 56- and 336-gate circuits list every non-tight wire with s, s', and the
rise of log2 s at each gate; print the ledger against N log2 N. (c) USE it: build circuits whose helpers have s s' growing with N.
Pools to try: the quadratic sign vectors (-1)^Q (s = s' = N, the transform's own eigenvectors; 6 + 10 of them at 16 points); a
tight wire times such a vector on a sub-cube (s s' = N 4^j); at 8 points, which is not a square, forms flat on both sides with
entries in 1, -1, i, -i (the statement supplies i).
**First experiment.** 8 points: pool search (mincirc at p = 3, 5, 7 fits 8 wires; steiner.py seeded with pool wires) for 21 gates
or fewer; the minimum is only known to lie between 15 and 22. Then 16 points below 56 with the 16 quadratic sign vectors as pool.
**Reading.** Which wires carry the rise, and whether one over-spread wire can serve more than a bounded number of gates.

## Brief 3. `basischange`: a symmetry-adapted basis change that is not a tree

**Object.** [read: `d-0.md` section 4, `d-7.md`, `i-cross.md` A and Hybrid 2; built in `i-cross/schur.py`, k = 2..8] U = "add one
element". Bracket-match the k coordinates; a matched pair (a, b) carries e_a - e_b, the unmatched ones carry the sums of all
j-subsets. In this basis the subset-sum matrix is Pascal blocks and the transform is (-2)^(pairs) times Krawtchouk blocks.
T(N) <= cost(B) + cost(B inverse) + middle; the middle is O(N log log N) when a root of unity of order 2m is supplied and
O(N log log N log log log N) with rationals and i only [a-0 3.4].
**Corrections to carry.** [a-0 3.3] For the transform with factor 1 the allowed bases are those whose string heads have one size
and are killed by "remove one element": any basis of each head space (dimension C(k,w) - C(k,w-1)). For an arbitrary Jordan basis
of U there is a factor-2 version. A tree of pair couplings costs k/4 per entry each way from its first level alone [i-cross].
**First experiment.** k = 3 (8 points): head spaces of dimension 1 and 2, so the freedom is GL(2) and a scaling per string.
Exact minimum of cost(B) and of cost(B inverse) over that freedom: mincirc at 8 wires, p = 3, 5, 7, outer loop over the bases of
the head space modulo p; lift and replay. k = 4 (16 points): head spaces 1, 3, 2, freedom GL(3) x GL(2); tools as in note 2.
Compare with the bit-at-a-time build (k - 1.6 sqrt(k) per entry [d-7]) and the layer costs 10, 6, 6 at 16 points [d-7].
**Reading.** The shape of the minimum: a tree of pairings, or wires reused across weight layers? A bulk coordinate depends on at
least 2^(pairs) inputs [d-7, recalled], so as in brief 1 the cost per form is all sharing: say whether the two briefs meet.
Signpost, not verdict [a-0]: a linear-size B would make every bit-permutation-invariant operator cheap.

## Brief 4. `illconditioned`: badly conditioned steps whose product is perfectly conditioned

**Object.** [read: `i-cross.md` W4] With bounded coefficients the determinant forces N log N; a unitary linear-size step spreads
a row by O(1) bits. So a linear-size program must be a product of badly conditioned steps with a perfectly conditioned product,
and nobody has an example of that shape for any flat unitary matrix.
**Material.** H = Z D Z-transpose and Z = D H D H D H D (three calls [a-0 3.1]); d-5's door matrix (2n - 1 gates in the limit,
3n - 4 exactly; 7 against 8 at 4 wires) and its conversion price (d+1)^2; d-5's question "is the transform the first-order digit
of a cheaper family": a matrix M0 with a program of size s0 and a first-order change of coefficients whose derivative is
(relabelling with scalings) x H gives H in 4 s0; candidates M0: the rank-one members at t = 1, -1, the identity, the complement
relabelling; G(u) = u^W with G(i) the transform (census at k = 4 never run). d-2 regularity 5: solved two-letter words have factor
spreads of several hundred at 32 points. Untouched ideas that belong here: failproof 1 (all of the determinant in one layer, the
rest shears), failproof 2 (triangular steps are invisible to the entropy proof), generalize 9 (H = U Sigma V with U, V of
determinant 1 and Sigma diagonal: the volume bound says nothing about U and V; minimise over that orbit).
**First experiment.** At 4, 8, 16 points: least gate count of a program "shears, one diagonal layer, shears" for H with shear
coefficients free in a large prime field (say 2^31 - 1, which stands in for unbounded); lift by rational reconstruction and replay
exactly. Check 4 points against 7 (G) and 8 (O). For each program found, print each step's condition number (floats, labelled as
a measurement) and the product's.
**Reading.** How the best count grows at 4, 8, 16, and whether coefficient size buys gates at all at 8 points (below 22).
Second target: the smallest flat unitary of ANY size (3-point Fourier matrix, minimum 5 gates [d-5]; sizes 5, 6, 7) with a
program below its bounded-coefficient minimum.

## Brief 5. `zetalead`: the lead for the subset-sum (zeta) and Moebius transforms

**Object.** [read: `i-cross.md` W5 and Hybrid 1; `a-0.md` 3.1, 3.2, section 4] Z = subset-sum matrix, [[1,0],[1,1]] to the k-th
tensor power. a-0's sharper form: Z = D(1/4,1/5) H D(3/2,-1/2) H D(2,1) H D(1,5/3), three calls, three is least;
cost(Z) <= 3 T(N) + 4N; H = Z D Z-transpose gives T(N) <= 2 cost(Z) + N. For every invertible 2 x 2 rational matrix M that is not
a relabelling with scalings: T(N) <= 4 cost(M_N) + O(N) and cost(M_N) <= 6 T(N) + O(N). "Two calls for every kernel" is false over
the rationals (the invariant tau must be a square).
**Do.** (a) Prove the identities for all k by hand from the 2 x 2 case and the rule (AB) tensor (AB) = (A tensor A)(B tensor B);
verify exactly for k = 1..6; give the exact overhead in (G) and in (O) (count the diagonal entries equal to 1). (b) Literature
with dates: Yates's method; Bjorklund, Husfeldt, Kaski, Koivisto on fast subset convolution and zeta transforms; Alman and
co-authors on Kronecker powers and the disjointness matrix (a-0 says Alman and Li 2025 reduce the class to it: read it); Jukna and
Sergeev; OpenAI's paper in `R/OAI/` and the notes in `wht33/research-2026-10-09/`. Does anyone state an o(N log N) exact zeta
transform, or the transfer? (c) What transfers: fields and rings where 2 and the diagonal entries are invertible. What does not:
semirings such as min-plus; say what happens to subset convolution, which uses ranked zeta transforms. (d) A one-page note in plain
English for readers of that field, with a list of what is NOT claimed. Publish nothing.
**Say plainly in the note.** The exponent carries, the constant does not: compute the size at which 3 T(N) + 4N falls below
Yates's k 2^(k-1) at a saving of 8.7625e-4. Small sizes show no gain at all: 12 gates at 8 points is an exact minimum in four
fields [d-0], and tight wires alone need Yates's count [a-2].

## Brief 6. `k3`: the 3-point kernel that would carry a saving down to exponent 1/2

**Why.** [read: `d-7.md` short version 3 to 6 and section 8; `a-1.md` section 6] Adapt only to swapping the two bits of each
pair: the basis change is a smaller Walsh-Hadamard transform and the middle is the Kronecker power of ONE fixed 3-point kernel,
K3 = [[1,1,1],[2,0,-2],[1,-1,1]]. Recursion t(k) = 2 t(about k/4) + (cost of the K3 power): any saving exponent for K3 passes
undiluted to the transform, down to exponent 1/2, and a linear-size K3 power gives N * 2.5 * sqrt(log N). a-1 reached the same
object from the squares: T(4^j) <= 2 sum C(j,s) 2^(j-s) T(2^s) + sum C(j,t) kappa(3^t). Two reports, one question, never run.
**First experiment.** K3 tensor K3 on 9 numbers in fewer than 24 gates (G); textbook 24, volume bound 12 [d-7]. mincirc needs an
even number of wires: add a dummy tenth wire or lift the restriction; GF(3) fits, GF(5) is just over the table limit (note 2).
K3 has an entry 0 and an entry 2, so GF(2) is useless. Then 27 numbers below 108 by steiner.py. Also price K3 itself in (O).
**Play.** K3 is the 3 x 3 Krawtchouk block: Pascal x diagonal x Pascal-transpose [i-cross A]. It contains a 2 x 2 Hadamard block
[a-1], so its powers contain the transform on 2^t of the 3^t points: is the rest cheaper than that part? Odd-radix facts nobody
has used [read: `WAVE2-PICKS.md` end; a-2]: bits per gate peak at 6 points; for groups of odd prime-power order tight wires
cannot compute the transform at all, so every odd-radix circuit is over-spread from its first gate.
**Reading.** 24 exact: one more tie, and say what is conserved. 23 or fewer: a brick of a new kind; run d-7's recursion with it.

## Brief 7. `twosteps`: can a bounded number of dense linear-cost steps make the transform?

**Object.** [read: `d-3.md` section 4; `d-2.md` sections 5 to 7; `i-play.md` line 61] A tree step: sum up a tree, scale each node,
spread back down; O(N) gates, dense kernel. L(N) = least number of tree steps, with free relabellings and arbitrary scalings
between, whose product is the N-point transform. L(4) = 1, L(8) = L(16) = 2, L(N) <= ceil(k/2), and commuting steps need k/2.
**If L(N) is bounded the transform has linear size.**
**What is contested.** d-3: nothing excludes L(32) = 2; the requirement sits exactly on the rank bound for blocks of a Hadamard
matrix (a rows, b columns, rank at least ab/N), with equality for subgroup-shaped blocks "only" [guess]. i-play: a sketch that
two factors work only up to 16 points and that the same argument says nothing for three. d-2: two letters sharing a finest
pairing exist only at 8 points [derived]; only 270 flag pairs were tried at 32 points, in floats; general trees and arbitrary
relabellings between letters were never tried; three letters at 128 points (commuting needs four) was not run.
**First experiment.** (1) Classify the equality cases of the block rank bound at 16 and 32 points: sets A of rows and B of columns
with rank(H[A,B]) = |A||B|/N that are not cosets. Exact, small. A non-coset equality case is the brick; none is the start of a
floor for non-commuting steps. (2) L(32) = 2 as a polynomial system (two trees, three scalings of 32 entries) modulo a large
prime, trees NOT restricted to subgroup chains; lift any solution. (3) Three steps at 64 (a tie with commuting) and at 128 (the
first size where three would win).
**Reading.** Either a proof that two steps are forced back into the commuting shape, level by level, or the first word that
beats k/2. Neighbour: wave 2-B `pieces` (outputs on sets that are not subcubes): read its report first.

## Brief 8. `thirdturn`: the transform is a renaming of the data in threes  (silly)

**The seed.** [read: `d-4.md` section 4, ran there at 4, 16, 64] With S the symmetric form of brief 1 and T the free sign change
(-1)^Q0 for a hyperbolic quadratic form Q0, the matrix R = T S / sqrt(N) satisfies R^3 = I, has trace 1, and equals the identity
on a subspace U of dimension (N+2)/3 (2 of 4, 6 of 16, 22 of 64); the rest is (N-1)/3 planes turned by a third of a turn.
[derived, mine, unchecked] A relabelling made of (N-1)/3 three-cycles and one fixed point has exactly these invariants, so over
the rationals R = B-inverse P B with P that relabelling. Relabellings are free, so **T(N) <= cost(B) + cost(B inverse)**, with no
middle at all. B is: pick (N-1)/3 seed forms f; its rows are f, f R, f R^2 for each seed, plus one fixed form. The freedom is the
whole centraliser of P, about N^2/3 parameters, which no tensor recursion sees.
**Why it is not obviously dead.** A seed with f, fR, fR^2 all tight has sqrt(N) non-zeros each (wall W1, half and half); the
question is whether seeds can share wires so that the 3 forms of a seed cost O(1) more gates, which W1 does not address.
**First experiment.** 4 points by hand and by mincirc: R = (1/2)[[1,1,1,1],[1,1,-1,-1],[1,-1,1,-1],[-1,1,1,-1]], seed e_0 gives
the forms x0, x0+x1+x2+x3, x0+x1+x2-x3 [derived, check it]; least cost(B) + cost(B inverse) over all seeds against 7. Then 16
points: five seeds and one fixed form; search seeds for the cheapest 16 forms (steiner.py; pool: coordinates, line indicators of
the 3 x 3 grid of zeros of Q0, which span U's first part at 16 points [d-4]). There are N choices of T: try sharing one B
between two of them.
**Reading.** Per-form cost of B at 4, 16, 64 against brief 1's c(N): if the two agree, they are one object; if not, keep the cheaper.
Material: d-4 mutations 1 and 2 (cheap projector onto U; several U_a at once); the exact identity
S/sqrt(N) = (3/N) sum over a of (sign) T_a P(U_a) - (2/sqrt(N)) I [d-4, ran at 4 and 16].

---

## Left for a fourth wave (nothing is thrown away)

- From the developers' mutations, not picked: d-0's shared repayment at 16 points and "prove 12 by hand, face by face"; d-1's
  Stickelberger reading (inside wave 2 `ring`); d-4's check of the E8 unit against the reflection identity, and hybrid bases as a
  walk for many arrays; d-6's "two copies" search beyond 4 points (inside `ladder`); d-7's triples instead of pairs and the
  flag-adapted basis; d-3's symmetry-respecting floor statement (a lead for the floor note).
- Untouched ideas still open: 6, 8, 11, 17, 32, 34, 61, 63, 64, 65 (PICKS.md list); failproof 4, 7; generalize 8, 11, 15;
  machine 27, 30 (WAVE2-PICKS-B.md list). 49 (odd radix) is material for brief 6; failproof 1, 2 and generalize 9 for brief 4.
- Anomalies no brief carries: the six "meters" that each read about k [generalize]; half of all 2 x 2 minors of H vanish with
  almost none forced by the wiring [failproof]; the quantised misses 8.000, 32.00, 48.00 of failed two-letter fits [d-2].

What I did not do: I ran nothing and checked none of the numbers I quote. The three-cycle statement in brief 8 and the
"16-point total cannot beat 56" remark in brief 1 are my own hand arithmetic from tonight.
