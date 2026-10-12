# wht39 / ideas / WAVE2-PICKS-B: four more ideas to develop for an hour each

Curator: j-pickb, 2026-10-10, about 22:20 to 22:32 EDT. Private research; nothing here is reviewed and nothing is in Lean.

Source: the 31 ideas and 51 anomalies of the four new generators (`j-failproof.md`, `j-generalize.md`, `j-manyatonce.md`,
`j-machine.md`), as listed in my task text, checked against `PICKS.md` (eight running) and `WAVE2-PICKS.md` (seven running)
so that nothing here repeats them. Idea numbers are those of the task list (0 to 30).

How the four were chosen: surprise; something actually seen behind the idea; a first experiment that fits an hour on
small exact cases; variety. Not by odds. Nothing was dropped for "must be known" or "must be impossible".
Tags [read] [ran] [derived] [guess] are the generators' own unless I write "mine". Everything marked "mine" is unchecked.

Generators represented: all four (failproof in pick 1, generalize in pick 2, manyatonce in pick 3, machine in pick 4).
Pick most people would call unlikely: 2 (`dictionary`: go through a non-abelian group to compute an abelian transform).
What I did not do: I ran nothing. I read `PICKS.md` (head and tail), `WAVE2-PICKS.md` in full, and the file lists of the
four `j-*` folders; of the generator reports themselves I used the summaries in my task text.

## Notes for all four developers

- Generation and play first, criticism last. A [guess] is welcome as long as it is marked.
- Instrument: `python3 -B (not in this repository) wht35/bin/light.py <label> <max seconds, at most 600> <command...>`
  (exit code 75 means no free slot: retry a little later). Exact rational or Gaussian-rational arithmetic, or modulo large
  primes with the reason why that suffices. A circuit found modulo a prime is a candidate until lifted and replayed exactly;
  "none found modulo p" is not "none exists" unless argued. This Mac's python3 has no numpy [generalize]; the Linux machine has.
- Say which count you use every time you quote a number of gates:
  (G) a gate is any a*u + b*v, scalings free: 4 points cost exactly 7, 8 points at most 22, 16 points at most 56;
  (O) OpenAI's count, additions and scalar multiplications each charged: 4 points cost exactly 8, 16 points 64.
- Words used below. N = 2^k points. H: the plain +-1 Walsh-Hadamard matrix; its rows are the *outputs* (also called
  characters). A *form* or *point*: a linear combination of the inputs. A gate puts a new point on the line through two
  points already held. *Helper*: a point of a program that is neither an input nor an output.
  *Bent centre*: a +-1 vector that differs from every row of H in about half its places, (N - sqrt N)/2 or (N + sqrt N)/2.
- Tools that exist: `d-0-zeta/mincirc.c` (minimum-circuit search), `i-play/n4.py` (4-point census, count G),
  `j-machine/steiner.py` and `greedy.py` (helper search and steepest-drain builder; steiner.py has a 40-gate cap bug),
  `j-manyatonce/ds.c` (exhaustive direct-sum search modulo small primes), `j-failproof/hubcap8.py`, `min4.py`.
- Files under `waves/<label>/` and `<label>.md`. No git, no Lean, publish nothing.
  The release tree is read only.

---

## Pick 1. `pieces`: build programs from what the lower-bound proof says they are made of: outputs restricted to sets that are not subcubes

From: failproof 0 (pieces that are not subcubes), failproof 3 (two tetrahedra in perspective), failproof 5 (hub capacity),
failproof 6 (double duty by a staircase). Material: failproof 4 (the stabiliser rule for symmetric programs), machine 30(c).

**The idea.** In count (G) the failproof generator proved by hand that N points need at least 2N - 1 gates, and the proof
says something about shape: when the bound is tight, every helper is "an output restricted to a set of inputs" (equal to
a multiple of one row of H on a set S, zero elsewhere). The textbook is the special case where S is always a subcube, and
its n log n is exactly the cost of halving subcubes log N times. Nothing in the proof makes the sets halve. The one case
where the bound is met, 4 points in 7 gates, uses a set that is NOT a subcube: everything except one point. Its hub
(1, -1, -1, -1) is the first output with one entry flipped and, at the same moment, each other output with one entry
flipped. So build that calculus on purpose. A *piecewise character* is a vector for which the inputs split into a few
pieces and on each piece the vector is a multiple of some output. Allowed pieces: subcubes, complements of a point,
Hamming balls, zero sets of quadratic forms, unions of cosets. A gate joins two piecewise characters. Geometry of the
4-point case: the input tetrahedron and the output tetrahedron are in perspective from a point (the four lines from input
i to its matched output all pass through the hub), there are four such centres, and they form a third tetrahedron. At
8 points no two of the N^2 input-to-output lines meet, so a single hub is dead and the replacement has to be a small flat
that several lines cross, or a third family of points that both sides are near.

**What was seen.**
- [derived, failproof; key step machine-checked on 800 sampled trees at 8 points and 80 at 16] count (G) >= 2N - 1 for N >= 4.
- [ran, `j-failproof/g6.out`, `g7.out`] 4 points: no 6-gate program; 228 distinct 7-gate sets; every one contains a
  flipped-point vector; 36 lie entirely inside the 24-point configuration of the three tetrahedra.
- [ran, `hubcap8.out`, sample] 8 points, 125 trees under the first output, 141,204 candidate extra helpers: one extra helper
  brought 0 outputs 140,607 times, 1 output 546 times, 2 outputs 51 times, never 3. The best are "the first output with two entries flipped".
  (An earlier buggy run is kept under a name that says so; do not quote it.)
- [derived, machine] The known 22 at 8 points is 11 + 11 with no gate shared: one centre of pair sums, one of pair differences.
  [ran, `j-machine/hand17.py`] On one centre the fifth output costs 4 gates where the second, third, fourth cost 1 each.
- [derived, failproof] A helper one gate from an output needs a partner at least as big as the set where it disagrees with
  that output, and one vector cannot agree with many characters at once (Parseval), even with unbounded entries.
- [derived by hand, failproof] The cyclic symmetry of order 7 is the wrong one at 8 points (at least 29 gates): a symmetry
  helps only if helpers have stabilisers that grow with their support.
- The 8-point minimum in count (G) is unknown: somewhere in 15..22.

**First experiment.** 8 points, exact, count (G). (a) Build the pool of points: every vector that is a sum of at most two
pieces (output w restricted to S), S from the families above, coefficients in {+-1, +-2, +-1/2}, taken up to scaling.
Include the 240 real stabiliser states (support an affine subspace, signs given by a quadratic form). Print the pool size.
(b) List the pool's three-point lines (triples that are linearly dependent): these are the only possible gates.
(c) Find the smallest set of pool points that contains the 8 inputs and the 8 outputs and in which every other point lies
on a line through two earlier ones: integer programming, or iterative deepening modulo a large prime with exact replay.
Report the minimum inside the stabiliser pool, the minimum in the wider pool, and whether every 22 found is the 11 + 11 shape.
A 21 is news; a proved 22 inside the class says which pieces were missing. (d) For the best programs print, per helper, how
many outputs it is one gate from, and which piece shapes occur. (e) Fifteen minutes on the staircase: glue two of the
228 seven-gate 4-point programs into an 8-point program, pairing helper i of one with helper pi(i) of the other with pi not
the identity (low half at one stage, high half at another), and count. Then the same pool at 16 points, greedy.

**Question to keep asking.** Which pieces do shortest programs use, and do they have to halve? Is there a family of
pieces in which one helper serves a number of outputs that grows with N? What replaces "perspective from a point" at
8 points: perspective from a line, from a plane, or a third frame that both tetrahedra-analogues are near?

---

## Pick 2. `dictionary`: route through a non-abelian group, and choose the free bijection that nobody has chosen  (unlikely)

From: generalize 10 (fusing is free), generalize 12 (split the addresses by a tiling that is not a subgroup).
Material: the anomaly "other transform + bridge = textbook exactly, in every case priced" [generalize].

**The idea.** Every group with N = 2^k elements has its own Fourier transform (split a function on the group into the
group's irreducible pieces, called representations). Computed along a chain of subgroups, each level of the chain does one
of two things to each piece: it *splits* it in two, which costs one butterfly layer on that part of the data, or it
*fuses* two pieces into one of twice the dimension, which is a free relabelling. So the cost per point is
k minus the average of log2(dimension), and our group, where every piece has dimension 1 and nothing ever fuses, is the
MOST expensive group of its order. The extraspecial group of order 2^(2m+1) pays 1.5m + 1 layers per point against our
2m + 1. To get our transform from another group's: H = (bridge) x (the other group's transform) x (dictionary), where the
dictionary is the bijection between the other group's elements and our addresses. A dictionary is a relabelling, so it is
free, and there are N! of them. In every case priced tonight, with dictionaries that respect the address bits (linear or
affine), cost(other transform) + cost(bridge) came out EXACTLY the textbook. That is what a hidden conserved quantity
looks like, and the published result shows that this kind of additivity is not a law of nature. Nobody has tried a
dictionary that is not affine. The same thought in the abelian world is generalize 12: split the addresses as A + V with
every address a + v in exactly one way, where neither A nor V is a subgroup; then H is the row-by-row product of two
partial matrices whose repetition pattern is not the textbook's. Such splittings exist only from about 6 address bits
[generalize, from memory], so no search at 4, 8 or 16 points can ever have met one.
What a solution would look like [guess, mine]: the best single group only halves the paid levels (floor k/2). An order
change needs a chain of dictionaries, each turning half of the remaining split levels into fuses, k, k/2, k/4, ..., with
bridges that stay cheap; that sum is linear.

**What was seen.**
- [ran, exact] Z_4 against Z_2 x Z_2: the bridge is the identity on two points and a square root of the swap on the other two;
  for Z_4^(k/2) against Z_2^k it costs k/4 gates per point.
- [ran, exact] D4 and Q8 against Z_2^3: bridge blocks 1, 1, 1, 1, 4 with the 4-block full (20 non-zeros).
  [ran, floating point] Cyclic groups of order 8, 16, 32: blocks 1, 1, 2, 4, ..., N/2.
- [derived] Linear and affine dictionaries change nothing (characters go to characters). A quadratic twist of the central
  bit keeps 4 non-zeros per row of the bridge, and 4 per row is forced for the extraspecial group of order 32.
- [derived] Room: at order 8 the bridge must rebuild 4 rows and the group saved 4 gates, no room. At order 32 the counting
  bound for the bridge is 16 gates and the saving is 32: room that does not exist at order 8.
- [derived, not run] A tiling with one periodic factor is the textbook: radius-1 balls tiled by the Hamming code collapse to
  the textbook split in the code's coordinates.

**First experiment.** (a) 8 points, exact (D4 over the rationals, Q8 over the Gaussian rationals), count (G): for every
dictionary up to the symmetries that change nothing (affine maps of the addresses on one side, automorphisms and
translations of the group on the other: a few dozen classes at most) compute the bridge B = H x (dictionary)^-1 x (group
transform)^-1, its block shape, its non-zeros, and its least gate count with the minimum-circuit searcher. Is
cost(group transform) + cost(B) the same number for every class, and is it ever below 22? (b) 32 points, both extraspecial
groups: dictionaries that are affine (control), quadratic twists of one and of two bits, and dictionaries that respect
the subgroup chain down to level j but scramble below it; record non-zeros per row of the bridge and an upper bound on
its gates. Target: under 28 (32 by layers, 28 with the 7-gate brick). (c) Twenty minutes with pencil: try to PROVE
cost(other) + cost(bridge) >= k N for dictionaries that respect the chain, and write down the first step that a
non-affine dictionary breaks. (d) Fifteen minutes: construct one splitting A + V of the 6-bit addresses with |A| = |V| = 8
and neither set periodic, and count the distinct rows up to sign of H restricted to the columns in A and to those in V,
against 8 and 8.

**Question to keep asking.** Is the exact additivity a theorem, and about what: the chain, the affine dictionary, or the
count? What must a dictionary do to make the bridge cheaper than the levels the group fused? Which group, and which
second dictionary, would halve the paid levels again?

---

## Pick 3. `ladder`: the saving that already works is a batch discount; measure it, name its gates, and climb a ladder of batch sizes

From: manyatonce 16 (exchange rate and ladder), 17 (doubly mixed gates: private encoders, shared core, private decoders),
21 (the pending-transform flag and the shear "y += H x"), 22 (structured batches of one array), generalize 14 (log n cheap
families must share work). Material: manyatonce 18 and 19 (Strassen on the Hadamard block; shifted copies), already inside
the running pick `shifts`. Not a repeat of the running pick `excess`: that one asked whether TWO copies share anything at
the smallest scale (`d-6.md`); this one changes the target.

**The idea.** The N^2-point transform is two rounds of "N copies of the N-point transform" (rows, then columns). So if N
copies together cost a fraction theta of N separate transforms, the exponent is z = log2(1 + theta). The published
z = 1 - 8.7625e-4 corresponds to theta = 0.99879; a saving of 1e-1 needs theta = 0.866; z = 0.5 needs theta = 0.414.
That turns "find a linear program" into a ladder of easier questions: what is the smallest batch size g(N) at which a
batch costs O(1) per point? g(N) = N^a gives n log log n; g(N) = log N gives n log*(n); g constant is linear. And the
literature fixes the shape of any discount: depth-two circuits and circuits without cancellation are exactly additive,
while the one proven discount for linear circuits (Paul 1976: n copies of a typical n x n matrix through fast matrix
multiplication) has the shape private encoder per array, a big core that works on mixtures of ALL arrays, private
decoders. Setting one array to zero shows why: gates(A and B together) >= gates(A) + gates(B) - d, where d counts the
gates whose two operands are both mixed on both arrays. So a large discount needs most gates doubly mixed, and the
encoder must mix the batch index with the address inside the array (an encoder on the batch index alone commutes with
the copies and gains nothing). Two cheap ways to feed a core: in count (G) a batch whose columns are known rescalings
D_j x of ONE array is free to build, so any discount on such a structured batch is a speed-up for a single array; and
"add the transform of one array to another" (a shear) is free after the first when many shears have a common source.

**What was seen.**
- [derived; `j-manyatonce/play.out`] The recursion c(M N) <= c_M(N) + c(M) and the z-to-theta table. One direction only.
- [ran, `ds.c`, complete] Two 4-point transforms in 13 gates modulo 3: none (119,043,675 nodes). Modulo 5 did not finish.
  843 random small invertible matrices over the fields with 2, 3, 5, 7 elements: no pair of copies shares a gate.
  The 3-in-4-out rectangle costs exactly 5, 10, 15 for one, two, three copies. So at tiny sizes everything is additive.
- [derived by hand] Strassen's seven products on [[H, H], [H, -H]]: three vanish and four are H, -H, 2H, 2H. The recipe that
  beats every typical matrix is exactly neutral on the transform with the coordinate splitting. Other splittings: not run.
- [ran, exact, N = 2, 4, 8] diag(H, H^-1) is three shears and a signed swap. [ran, N = 4, 8, 16] With X the N shifted copies
  of x, H X = diag(Hx) H: a batch costs what its degrees of freedom cost, not its number of entries.
- [read, task text] The published result is itself a direct-sum saving: several arrays served together by fewer steps than
  separately. Not done by anyone tonight: comparing any of this with what the published engine's unit does with its arrays.

**First experiment.** (a) Reading, 20 minutes, read only: `R/Work/GFrame/Engine/`, `R/Work/Block/` and `d-6.md`. State the
published unit as a batch: how many arrays, of what size, at what cost against separate transforms (its measured theta),
and mark its gates as private encoder, doubly mixed core, private decoder. Which single number in it would have to change
to reach theta = 0.866? (b) The nearest problem that CAN be solved: make Paul's discount explicit. For a typical n x n
matrix A, count gates (G) for "A times an n x n array" through Strassen with one factor fixed, at n = 2, 4, 8, 16, 32,
against n separate copies; find the crossover size. Then put A = H_n with a splitting that is not by a coordinate (blocks
by cosets of a code; or H_4 = J - 2I, "all ones plus sparse") and count which left factors vanish, repeat, or get cheaper.
(c) Encoder search at 4 copies of the 4-point transform (28 gates separately, count G): for cheap invertible E that mix
batch index b with address a ((b, a) -> (b, a XOR b), (b, a) -> (a + b, a), sparse triangular maps), compute
E (I tensor H) E^-1 exactly and bound its gates; any total under 28 is the sign. (d) Structured batch at N = 4 and 16:
columns D_j x with D_j second-degree sign patterns such as (-1)^(a1 a2); compute the rank of the batch in the N^2 twisted
shift families of manyatonce 19 and whether the batch transform restricted to such batches is cheaper per column than one transform.

**Question to keep asking.** Where exactly is the published discount made, and what stops it from being bigger: the batch
size, the unit size, or the coefficients? What is the smallest batch at which theta < 1 for the plain transform? Does the
discount grow with the batch (a ladder) or saturate (a constant)?

---

## Pick 4. `drain`: a linear program is a cheap list of forms in which every output is a combination of O(1) of them; let a machine build it by steepest drain

From: machine 24 (full-drain gates), machine 23 (search the helpers, not the wiring), machine 25 (hang the outputs on a
centre), machine 26 (peel a centre and recurse), machine 28 (the cost curve of the first m outputs), generalize 13 (an
answer format with O(1) read-out), manyatonce 20 (online against offline: each output is its parent plus a few terms).
Four generators' versions of one picture.

**The idea.** Count (G). At any moment a program holds a set S of forms. For each output t let d(t) be the fewest forms
of S that combine to t, minus one: the gates still needed for t alone. The potential P is the sum of d(t) over the
outputs. It starts at N(N - 1), ends at 0, and one gate can lower it by at most N. So a program of c N gates must drain
N / c per gate on average: most of its gates bring a constant fraction of ALL outputs one step closer. The textbook
drains N/2, N/4, ..., 1 per gate, layer by layer, and that halving is the log. Read from the other end, a linear program
is a data structure: about c N stored numbers, built by c N gates, from which every output is a combination of O(1)
of them (prefix sums do exactly this for interval sums, and remove exactly a logarithm). One form can drain a great deal:
with a bent centre c in hand, every output is c minus twice the sum of the inputs where it differs, so every d(t) falls
from N - 1 to about (N - sqrt N)/2 at once [derived, mine], half of all the potential. What is left is the matrix E in
H = (all ones) x c^T - 2E, with entries 0 and +-1, and E E^T = (N/4) I + (rank 2): half the norm, orthogonal again up to
rank 2. So the questions are whether there is a second such form for E, and a third, and whether the forms that the
centre's own tree passes through can be chosen to be the corrections.

**What was seen.**
- [ran, exact replays, `j-machine/greedy.py`] Steepest drain with no search: 7 gates at 4 points (profile 2, 3, 3, 1, 1, 1, 1);
  23 at 8 points (profile 4, 4, 4, 4, 5, 7, 8, 4, 2, 1, 1, 1, ...; circuit in `j-machine/r4/greedy_H8_s2_best23.json`), where
  one gate drains all 8 outputs. Greedy has P = 16 after 8 gates; the known 22-gate circuit only after 11, yet finishes one better.
- [derived, machine] With steps that change one input at a time, N points cost at least N*N/4 (23 at 8 points, and greedy sits
  exactly on it). The 22 gets under it only through steps that change two inputs at once.
- [ran, exact integers, `tower.py`] At N = 4, 16, 64: row weights of E are 1 or 3, 6 or 10, 28 or 36; rank(E E^T - (N/4) I) = 2;
  [derived] 4 E E^T = N I + N J - 1 w^T - w 1^T with w = H c. The second peel was not run.
- [ran, weak] The cousin with entries 2^(Hamming distance) drains faster at the start (6 and 6 against 4 and 4) and ends in
  the same place. At the transform's own point an early gate can help only half the outputs.
- [ran, generalize] Data of rank r across the middle cut cost about r N: linear for bounded rank. Butterflies to transform
  all links of a full-rank chain of small tensors: 1.33 N. All of n log n is then in writing the answer out as a table.
- [ran, `slp.py`] The error over about 42,000 wirings is two-valued (below 1e-20 or above 1): nothing is almost a circuit,
  so search exactly or modulo a prime, never by floating-point solving.
- Limits [machine]: steiner.py did not rediscover 22 at 8 points from nothing; 16 points was never searched (40-gate cap bug).

**First experiment.** (a) Make d(t) cheap: C or plain Python modulo a large prime, checking spans of 2, 3, 4 forms and using
an honest upper bound beyond that; replay every best circuit exactly. Fix the 40-gate cap. Run the steepest-drain builder
at 16 points (the number to beat is 56), then 32 and 64 with the bound, with one gate of lookahead. Record the drain of
every gate. Report how the size grows (N log N, N^2/4, or something else) and how many gates drain at least N/2.
(b) Full-drain gates by hand and machine at 16 points: with S = the inputs plus the tree of one bent centre, which single
extra forms lower d(t) for at least 12 of the 16 outputs? The 16 corrections are the six-point blocks of a biplane
(16 blocks, any two share 2 points): choose the centre's tree so that each block is a union of few tree nodes, and count.
(c) Second peel: at 16 and at 64 points search for the form and the rank-one or rank-two piece whose removal from E leaves
the sparsest remainder (targets: row weight 6 -> 2 at 16 points, 28 -> 12 at 64). (d) The read-out target stated as a
puzzle at 64 points: at most 128 stored numbers, built in under 128 gates, each output a combination of at most 3.

**Question to keep asking.** After the first centre is spent, what does a gate that helps every output look like, and is
there a supply of them that does not run out? Does a set of m good forms cut the potential by 2^m (the log again) or by
much more? Which stored numbers would make every output a combination of three?

---

## Everything else, by title (nothing is thrown away)

Not picked, free for the next wave. The note after a title says which running pick is its neighbour, so that whoever
opens it reads that report first.

From failproof:
- 1. The volume-free program: all of the determinant in one layer, the rest by shears (neighbours: `letters`, `border`)
- 2. Potential-blind moves first: triangular matrices are invisible to the entropy proof (neighbours: `passes`, `zeta`)
- 4. Programs that are unions of orbits, with orbit-stabiliser accounting (its stabiliser rule is material for pick 1)
- 7. In OpenAI's count, put every scaling on a hub (neighbour: `conserved`, which asked the same 4-point question)

From generalize:
- 8. Buy binary digits, not layers: the transform modulo 2^b in about (2b - 1) n gates (neighbours: `cutoff`, `zeta`)
- 9. The cheapest Smith normal form of H (neighbour: `zeta`, which fixed the outer factors to Z)
- 11. The relabel-and-phase class is closed at exactly k layers; partial layers are the way out
  (a folder `e-7-halftouch/` exists; I saw only its name and do not know whether it covers this)
- 15. The cost lives in the central weight band: choose coordinates where the mass is not central (neighbour: `cutoff`)

From manyatonce:
- 18. Paul's trick on the transform itself: Strassen's recipe with left factors that are new, cheaper matrices
  (inside `shifts` by hand; its non-coordinate splitting is step (b) of pick 3)
- 19. N shifted copies: closed form, and a general batch in shift-and-sign coordinates (neighbour: `shifts`; material for pick 3)

From machine:
- 27. The subset-sum side has slack that the transform does not (neighbour: `zeta`)
- 29. Nothing is almost a circuit, so count modulo a prime instead of solving (a method; used in picks 1 and 4)
- 30. Two copies at the smallest scale, and which copies could share (neighbour: `excess`; its case (c) is material for pick 1)

Ideas inside the four picks: 0, 3, 5, 6 (pick 1); 10, 12 (pick 2); 14, 16, 17, 21, 22 (pick 3); 13, 20, 23, 24, 25, 26, 28 (pick 4).
That is 18 inside and 13 listed above: 31.

Three I would open next, for the same reasons and not by odds:
- 2 with 1: measure the entropy potential gate by gate along the 7-gate program and look for ONE shear, on a small state
  after a running-sum block, that delivers more than 2 bits. A linear program needs about log N bits per gate, and the only
  potential proof known for the normalised transform cannot see triangular matrices at all.
- 11: steps on a sub-cube only, with a free linear relabelling between any two. The exact rank law (least layers = rank of a
  k x k block, for all 1,451,520 elements at k = 3) says the potential needs WHOLE layers; Haar is made of partial ones and is linear.
- 8 with 9: the second meter (binary digits, 2n gates each, half of them free) and the orbit of Smith normal forms that
  nobody has walked.

Anomalies that no pick carries and that would not go away while I read:
- Six unrelated meters each cost about n gates per unit and each reads about k at the transform: layers, binary digits,
  splitting levels of a subgroup chain, rank of a k x k block in the relabel class, rank across a cut, cosets of outputs [generalize].
  Nobody has said whether they are one quantity.
- Half the digits are free: the transform modulo 2^(k/2) already costs the whole k n [generalize, ran, count G].
- Half of all 2x2 minors of H vanish and almost none of those zeros is forced by the wiring, even in the textbook:
  about N^2 coincidences against c N free coefficients [failproof, derived].
- At 8 points a plane of 4 outputs costs 11 gates and four independent outputs cost 14; per output, the whole transform
  is the cheapest set at 4 points [generalize, derived by transposition, partly ran, count G].
