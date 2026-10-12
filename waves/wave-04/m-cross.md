# m-cross: the four waves side by side, four hybrids tried, and what to ask next

11 October 2026, 00:44 to about 01:22 EDT, 40-minute box. Private. One agent; nothing reviewed, nothing in Lean, nothing published.
Marks: [ran] = exact run of mine tonight (files in `m-cross/`, whole numbers and fractions only); [derived] = by hand tonight, checked
by nobody; [read] = from tonight's reports; [guess].
Gate count everywhere: **(G)**, a gate is any a*u + b*v, scalings free, unless a line says (O) (OpenAI's count).
Read: k-cross, WAVE3-NOTE, the head and walls of j-cross, the nine wave-4 results, the heads of p-0 to p-7 (wave 5, still running).
I did not read the wave-4 reports in full, nor b-*, c-*.

Words. N = 2^k points. *The transform*: the Walsh-Hadamard matrix H. *Textbook*: N log2 N gates. *Wire*: a value the program holds,
written as a vector over the N inputs. *Tight / over the limit*: (non-zeros of a wire in the inputs) x (non-zeros in the outputs) equals
N / is larger. *Merge tree*: start from the N inputs and repeatedly join two held sums on disjoint sets of inputs; N - 1 gates.
New words of this report, all about the prime 2:
- *Primitive form* of a wire: the wire scaled (free in count G) so that its entries have odd denominators and are not all even.
- *Class* of a wire: its primitive form modulo 2, a 0/1 vector. For a wire with entries 0, +1, -1 the class is its set of non-zeros.
- A gate is a *survivor* if its result has a class no earlier wire has, and *dead* otherwise. (Name from h-6: let the kernel's entry
  tau go to 1 and these gates merge with an earlier wire. For the transform tau = -1, and tau - 1 = -2: "tau near 1" is "modulo 2".)
- Kind of a gate, from the classes of its two parents u, v and its result w: **J** (join) three different classes; **S** (shift) w has
  the class of a parent, i.e. w = u + (even number) * v; **Q** (difference quotient) the parents have one class and w another, i.e.
  w = (u - c v) / 2^m; **E** all three equal.
- *Order* of a dead gate: the largest m with w = (odd number) * (an earlier wire) modulo 2^m.

## 0. In eight lines

1. [ran] **Every circuit of the four waves that I could parse and replay (18 files: textbook, brick, the 19, two 21s, the 20, both
   52s, the 54, the staircase up to 64 points; five of the files are the critic c-1's own copies of the staircase) is, modulo 2,
   ONE merge tree.** It has exactly 2N - 1 classes, they are nested or
   disjoint, exactly N - 1 gates are survivors, and every other gate is dead. No circuit contains a Q gate or an E gate. Every dead
   gate has order 1 (one exception: one gate of the drain's 21). Section 3, hybrid 1.
2. [ran] So gates = (N - 1) + dead, and the whole night's saving is in the dead gates: N log2 N - N + 1 of them in the textbook,
   **exactly (N/2) log2 N in the brick and in the 19**. The records at 2, 4, 8 points are 2, 7, 19 = N - 1 + (N/2) log2 N. The next
   values of that formula are 47, 111, 255; the records there are 52, 128, 304. Hybrid 2.
3. Wave 4's three laws (h-0: gates + over-limit wires >= N log2 N; h-1: at most two skipped pieces per non-piece, limit rate 1/2;
   h-6: (N/2) log2 N shifts) are one count read three ways, and the count is the power of 2 in the determinant of H. Section 1.
4. Six wave-4 reports stop at one wall: **a wire pays once as long as its partners are tight.** h-8 proved it in a class
   (Proposition A). Section 2.
5. [ran] The one program known to change the order does NOT have the one-tree shape at its centre: the 120 x 120 matrix of the
   published unit (h-7), doubled and read modulo 2, has 120 different classes of 56 entries and **all 7,140 pairs overlap without
   nesting**. Hybrid 4.
6. [ran] Difference quotients of outputs are circular: a half piece made from two outputs serves only those two (28 of 28 at 8
   points, 120 of 120 at 16), a quarter piece only its four. Hybrid 3.
7. No circuit below any known count, no change of order. The floor of line 2 is a guess, and it is false at astronomical size for
   general circuits (the published program is below (1/2) N log2 N there). So it can hold only inside the hypotheses of line 1,
   and those three hypotheses (one tree, no Q gate, order 1) are the to-do list.
8. Most informative question: **which of the three hypotheses does a circuit with fewer than (N/2) log2 N dead gates break?**
   Smallest case: 18 gates at 8 points. Largest case: the published unit, which can be metered now. Section 4.

## 1. Facts that explain each other

**A. h-6's joins and shifts are the J and S kinds, defined with no frame and no tau.** [ran, `meter2.out`] Staircase: J/S = 3/4, 8/12,
20/32, 48/80, 112/192 at 4 to 64 points; the 19: 7/12. These are h-6's numbers. But the S count is not a law: the tensored 54 has
J/S = 30/24 and h-8's three-hub 21 has 11/10. What is the same in every file is the number of survivors, N - 1. The count that
means something is "dead" (S gates plus joins that land in a class already held), not "shift".

**B. One number, five reports.** (N/2) log2 N is: the power of 2 in det H (g-4: all of it sits in the diagonal D of H = Z D Z^T; and
(-1)^m = sum over j of (-2)^j C(m, j) is that identity entry by entry, so the j-th term is "what the transform is modulo 2^(j+1)");
Morgenstern's count in h-3; h-6's shift count; the dead gates of the brick and the 19 [ran]; and the limit of h-1's ladder
1/2 + 2^(-w). j-cross's "if a wire saves at most one gate the floor is (1/2) N log2 N" is the same floor from the other side.

**C. h-0's law in these words.** On every circuit that is on h-0's law, gates + over-limit wires = N log2 N [ran again here: brick,
19, 20, staircase to 64 points, the 54, h-8's 21; the second 52 is off by 4, the drain's 21 by 8, as h-0 and h-1 say]. With
gates = N - 1 + dead: **each over-limit wire removes exactly one dead gate from the textbook's N log2 N - N + 1.** If dead gates
cannot go below (N/2) log2 N, at most (N/2) log2 N - N + 1 wires can pay: 1 at 4 points, **5 at 8 points**, 17 at 16. That is h-0's
unexplained "the budget allows 6, 5 are saved" [derived from the guess of hybrid 2].

**D. Why the staircase stops at 3/4.** [ran, `dups.out`] Its dead gates beyond (N/2) log2 N number 1, 5, 17, 49 = (N/4)(k - 3) + 1, and
each is a named gate: a second, third, fourth hub on a support that already has a hub (hub16 at 8 points; hub14, hub30, hub38,
hub43, hub48 at 16). The 19 has one centre and no second wire in any smaller class (13 full wires, every other class one wire).
h-1's second 52 also has five, all on the full support. "One hub per support" is what the floor would need.

**E. Tensor products never sit on the floor.** [derived; checked on the 54] Write e(A) = gates - (N - 1) - (N/2) log2 N. Then
e(A x B) = n e(A) + m e(B) + (m - 1)(n - 1) for sizes m and n. This is h-0's "excess adds under tensor products" with the constant
made explicit: 19 x textbook-2 gives 0 + 0 + 7, and 54 = 47 + 7. Any circuit on the floor is not a product.

**F. The same wall in the batch world.** h-2's lemmas bite only on tight forms; the small-circuit proofs bite only on tight partners;
cutf3 needs no address map. Each lower-bound method of the night works on equality objects and is silent one step away
(k-cross's fact H).

**G. h-3's two worlds are the two scales of an S gate.** In count (O) a wire held at scale 1 and at scale 1/2 costs one operation; in
the meter that wire is the partner of S gates with coefficient 2. [guess] h-3's "five additions saved per crossing" is the 19's
five over-limit wires on one centre.

## 2. The walls

**One wall, stated once. Lemma P (pay once).** If no gate reads two over-limit wires, then gates >= N log2 N - (number of over-limit
wires) [h-8, Proposition A: derived there, one case closed only at 8 points]. Who hit it:
h-0 (with tight partners a non-tight wire is one gate from at most 4 outputs, any coefficients, 8 and 16 points);
h-1 (two skipped pieces per non-piece wire, so rate at least 1/2 + 2^(-w));
h-4 (for subset sums Yates's count holds until a gate touches two entangled wires);
h-5 (births per gate <= width of the wider parent; a hub pays for at most two doubles);
h-6 (the agreement rule: a shift needs a held partner that agrees with the current wire);
h-8 (the proof stops at the first gate with two over-limit parents);
h-7 from the far side (inside one level of the published unit a wire pays 0.004 of a gate).
What I add [ran]: all the circuits behind those six reports have one more thing in common that none of them measured: one merge
tree modulo 2, no Q gate, order 1.

**j-cross's walls.**
- **U (tight wires).** Sharpened twice (h-8's Proposition A lets one over-limit wire per gate in; h-5 has N log2 N for "every wire
  tight or a product" at 4 points modulo three primes). **Broken as a general law** by h-7's count: L1 and L2 must fail for the
  published program at about 2^1,152 address bits, by nesting. Not broken at any size one can search.
- **M (one magnitude).** Not broken; the lever is not there. h-1: t = 1 or -1 is forced on the staircase skeleton. h-0: the hub
  census holds for any coefficients. [ran] 17 of the 18 circuits have wires of one magnitude only; the one with two (the drain's
  21) is the most wasteful.
- **C (commuting steps).** Not touched by wave 4.
- **S (self-similarity).** Sharpened into a formula (E above) and given its exit by h-7: excess adds, saving multiplies.

## 3. Four hybrids, each tried

### Hybrid 1. The meter at the prime 2  (h-6's limit tau -> 1  x  the transform, where tau - 1 = -2  x  g-4's diagonal  x  h-0's meters)

Idea: h-6 found the pattern by letting tau be a symbol. At the transform the same degeneration is reduction modulo 2, and it
needs no frame, no table and no restriction on coefficients. So every circuit of the night can be metered.
Tried [ran, `meter2.py`, `meter2.out`, `laminar.py`, `laminar.out`]: every *.txt in the ideas folders that parses as one gate per
line and replays exactly as the transform at 4 to 64 points: 18 files. Results are lines 1 and 2 of section 0 and fact A.
Control [ran, `trial2.out`]: the textbook run forwards and then again (the second half undoes the first): the second half is all
Q gates (8 of 8, 24 of 24, 64 of 64). So the meter does see a circuit that runs backwards; the night's circuits do not.
Limit: 18 files is what parsed. The annealers' circuits of h-0, h-1 and the (O) programs of h-3 above 4 points are in other formats.

### Hybrid 2. The floor N - 1 + (N/2) log2 N  (h-0's law  x  h-1's ladder  x  j-failproof's exact minima  x  the meter)

Idea: put the two halves of the count next to the exact minima. Survivors: N - 1. Dead gates: at least (N/2) log2 N [guess].
Tried: N = 2: 1 + 1 = 2, the exact minimum. N = 4: 3 + 4 = 7, the exact minimum [read: j-failproof, p-0]. N = 8: 7 + 12 = 19, the
record, exact minimum open between 15 and 19. N = 16: 47 against 52; h-6 met the same 47 as "15 + 32" for one-centre programs.
[ran] In all 18 files dead >= (N/2) log2 N, with equality only at the brick and the 19; the excess of every other circuit is listed
gate by gate in `dups.out` for four of them.
What would follow if the guess holds in the one-tree class: the 19 is optimal there, the rate there is at least 1/2, and h-1's
ladder limit is a theorem. What is certain: it does not hold for all circuits at all sizes (line 7 of section 0).
[derived, a reduction, not run] In the one-tree class the dead gates are a shortest-network problem: every full wire is the centre
plus twice a whole-number combination of tree wires, a dead gate changes one coefficient, and the N outputs must be joined.
Two outputs differ on a half-space, and a half-space of the b-th bit of the tree's order is 2^(b-1) tree nodes; a Gray-code walk
uses bit b on N / 2^b edges; the product is N/2 per bit. That is where (N/2) log2 N comes from in this class. With two trees
in different bit orders the same sum would be O(N), IF the partner did not have to agree with the current wire; the agreement
rule (h-6) is exactly what takes it back. So "two trees" is the first hypothesis to leave.

### Hybrid 3. Top-down: difference quotients of outputs as partners  (h-0's "last step read backwards"  x  h-8's failing gate  x  Q gates)

Idea: every record builds partners bottom-up. A Q gate makes a partner from two finished wires: (h_a - h_b)/2 is h_a on a half-space.
Tried [ran, `trial2.py`, `trial2.out`]: at 8 and 16 points, every half piece made from two outputs, tested as the partner of a
coefficient-2 step between any two outputs: it serves exactly the pair that made it (28 of 28; 120 of 120). Every quarter piece
made from four outputs turns exactly its own four outputs into another sign vector (84 of 84; 840 of 840).
Reading: on wires with entries +1, -1 a Q gate only gives back what was paid. A Q gate that pays must have parents that are not
outputs, or have entries of two sizes (the wires with entries 1 and 3 that h-0 and h-8 saw arrive unasked are congruent to an
output modulo 4, which is the first place an order-2 step can start).

### Hybrid 4. The shadow modulo 2, and what the published unit does there  (h-7's dictionary  x  e2-3's cancellation meter  x  subset sums)

Idea: reduce a whole circuit modulo 2. [derived] If it has no Q gate, its J gates alone are a circuit of additions modulo 2 for the
target modulo 2 (S gates copy a class, they cost nothing there). For the transform the target modulo 2 is one row repeated, so
nothing is forced beyond N - 1. For subset sums (determinant 1) the target modulo 2 is the full subset-sum matrix over the
two-element field, so: **an exact subset-sum circuit with no Q gate has at least as many J gates as the best circuit over the
two-element field with cancellation allowed** (an open number in the literature as the reports quote it: Boyar and Find, 2012).
By g-4 the published exponent passes to subset sums; so either that open number is below N log N, or the three-call program
divides differences by 2 in an essential way. [guess] The control of hybrid 1 points to the second: a second call of the
transform is all Q gates.
Tried [ran, `e8shadow.py`, `e8shadow.out`]: I rebuilt the published unit's scatter matrix M from h-7's description as half the
table of inner products of one root per line of E8 (120 lines; entries 1 and +-1/2; 56 neighbours; M M = 15 M: all of h-7's
numbers come out). Doubled, it is primitive. Modulo 2: the diagonal vanishes, rank 8, 120 different classes of 56 entries, any
two share 24 or 28 entries, and all 7,140 pairs overlap without nesting. A circuit that computes it cannot be one merge tree
modulo 2. Not read from the certificate: h-7's unitmeter does that; this is the matrix only.
Reading: the small circuits of four waves never cancel modulo 2; the only order-changing program has at its centre an object
whose rows all cancel against each other modulo 2. e2-3's cancellation meter counted cancellation over the rationals, which
the records have; cancellation modulo 2 is a different thing, and they have none.

## 4. The most surprising thing, and the question that would tell the most

**Surprise.** After four waves and many shapes (staircase, walk, tensor, drain, annealed), every circuit has the same skeleton
modulo 2: one merge tree of N - 1 joins, and then only wires that repeat a class already held. The exact minima at 2 and 4 points
and the record at 8 are exactly N - 1 + (N/2) log2 N. Nobody chose this. [guess, from h-0's description of its pool as "entries 0, 1, -1
on sub-blocks"] the searches had overlapping supports available and did not keep them.

**Question. Which hypothesis does a circuit with fewer than (N/2) log2 N dead gates break: one tree, no difference quotient, or
order 1?** It is informative both ways. If none can be broken with profit at 8 and 16 points, the floor is real there, 19 is the
8-point minimum of everything searchable, and linear size cannot come from any circuit of the kinds built tonight. If one breaks,
it names the mechanism. And the published program must break at least one, so it can be asked directly.
Experiment, two ends.
(a) Small end, exact: at 8 points, the least number of dead gates in the one-tree class (the shortest-network form of hybrid 2,
over all merge trees and centres, coefficients any whole numbers); if it is 12, search for 18 gates with exactly one hypothesis
released at a time: 8 survivors (two overlapping supports); one Q gate; one order-2 step with entries up to 3.
(b) Large end, a measurement: run `m-cross/meter2.py`'s three tests on the published unit, written as a single-array circuit at
f = 1 with the batch index as the high address bits (h-7's `unitmeter.py` already parses the certificate): number of classes
against 2n - 1, pairs that overlap, Q gates, orders above 1, and dead gates against (n/2) log2 n. This also settles the conflict
h-8 found between a-2's ledger and h-7's dictionary, because that ledger assumes no cancellation between mixtures.

## 5. Three objects for a skeptic, in this order

1. **h-3, the only claim below a count on the list.** `h-3-orecord/o_16.txt`: 16 points, 56 operations in count (O) (the list had
   60), outputs H x / 2, not H x. `ox_512.txt`: H x exactly at 512 points in 4,352 operations (O) against 4,608. Growth
   (5/6) N log2 N + N for N a power of 8, said to be below the published 23/24 of Alman and Rao. Attack: is a halving one unit in
   R/OAI as h-3 reads it; is 23/24 still the best published constant; does it all rest on g-1's 19 (yes).
2. **The two hand proofs of the wall: h-8's Proposition A and h-5's theorem.** A: no gate reads two over-limit wires implies
   gates >= N log2 N - over-limit wires (one case closed only at 8 points). h-5: every wire entangled on at most b bits, the bits
   free to change, implies at least N log2 N / b gates (Lemma 2: births of a gate <= width of its wider parent; no violation on
   14,055 gates). Attack Lemma 2 with a wire of width 3 made in one gate (h-5 names x0 + x7), and A's unfinished cell-flip case.
3. **h-2: four arrays at block size 5 need all 20 moves in old letters** (17, 18, 19 excluded; it closes the 1e-1 case for that
   batch). Rests on two hand lemmas nobody read and a search program nobody reviewed, and uses only e2-2's necessary condition.
   Attack the zero-form lemma (used for exactly one of 70 vectors) and `cover.c`'s completeness.
Also for a skeptic, mine: the meter. The primitive form and the 18-file harvest are simple, but "new = N - 1 in every circuit"
should be re-run on the annealers' circuits, and the floor guess should be attacked first at 8 points.

## 6. Eight experiments for the next wave

Deepen what is alive:

1. **unit2adic** (h-7, h-8, hybrid 4). Section 4 (b). Inputs: `h-7-unitmeter/unitmeter.py`, `m-cross/meter2.py`, `laminar.py`,
   `e8shadow.py`. Output: for the scatter alone and for one E8 invocation, the five numbers of section 4 (b), and for every
   addition the number of sources on both sides before and after (h-8's `ledger-vs-unit`). One line answer wanted: which of
   "one tree, no Q, order 1" the unit breaks first, and where.
2. **onetree8** (h-0, h-6, h-8, hybrid 2). Section 4 (a), first half. Decide whether 12 dead gates is the minimum at 8 points for
   circuits that are one merge tree modulo 2 with no Q gate, any whole-number coefficients. Then 16 points: is 47 reachable in
   the class, or what is its minimum (52 known; the five gates to remove are named in `m-cross/dups.out`).
3. **eighteen** (the open exact minimum, 15 to 19). Section 4 (a), second half. Three searches for 18 gates at 8 points, each
   releasing one hypothesis: a pool with two merge trees (h-0's 304 vectors, required to use 8 or more classes that are not
   nested); h-5's `pairex.c` pool plus all difference quotients of pool wires; sign vectors plus wires with entries 1 and 3.
   Report for each the least (gates, dead gates) reached, exhaustive or not.

Nobody has tried:

4. **twotrees**. Circuits with two merge trees in different bit orders. Brief: at 16 points take the cube tree in orders
   (1,2,3,4) and (3,4,1,2). Count, exactly, the dead gates needed to join the 16 outputs when partners may come from either tree
   and must agree with the current wire. Hybrid 2's sum says O(N) without the agreement rule and (N/2) log2 N with one tree;
   measure what agreement costs with two, and with one tree per bit (which must give the textbook back).
5. **quotient**. The first useful Q gate. Brief: at 8 points list all wires congruent to an output modulo 4 with entries in
   {+-1, +-3}, and all pairs of them congruent to each other modulo 4; their quotients are new wires made in one gate from two
   over-limit wires (h-8's failing gate). How many outputs is such a quotient one gate from, and with which partners? h-0's
   census covers tight partners only. Then the same over the Gaussian integers, where 2 = -i (1 + i)^2 and a step can have
   half order (h-5: every hub is the real part of a product wire with factors (1, i)).
6. **shadow** (a lead for readers of the subset-sum literature as well). Brief: state and check the shadow lemma of hybrid 4 on
   h-4's 2,748 optimal 8-point subset-sum circuits (how many have a Q gate; is "idle" in h-4's identity the same as "dead"
   here); count the Q gates of g-4's three-call circuit at 8 and 16 points; read what is known since 2012 about circuits with
   cancellation for the subset-sum matrix over the two-element field. Claim nothing about any conjecture.

One hybrid:

7. **compose** (h-7's "excess adds, saving multiplies" x fact E x h-1's interleaving). Brief: fact E prices the tensor product at
   (m - 1)(n - 1) above the floor; the staircase composes two bricks at 16 points for 5 instead of 9. Enumerate the ways to
   compose two bricks, and a brick with the 19, by choosing which wires of the inner circuit the outer one reuses; compute e for
   each exactly. The growth of the least e decides the constant: rate = 1/2 + lim e / (N log2 N). A composition law with e
   growing slower than N log N would be the first rate-1/2 family; one with negative e breaks the floor.

One that sounds silly:

8. **precision**. Compute the transform only modulo 4, then modulo 8, and so on. [ran, `precision.py`, `precision.out`, 8 to 32
   points] H = sum over j of (-2)^j B_j with B_j(y, x) = C(number of common ones, j); B_j has rank C(k, j); the sum of the
   terms below j is congruent to H modulo 2^j and has rank 1 + k + ... + C(k, j-1). [ran, circuits replayed] A matrix
   congruent to H modulo 4 costs 22, 52, 114, 240, 494, 1004 gates at 8 to 256 points, under 4N (k sums over half-cubes, then
   all their subset sums); it is not H. In the real metric H cannot be approximated at all (all singular values equal); in the
   2-adic metric it has low rank until the precision reaches about k/2 - sqrt(k) digits: the binomial's spread once more
   (j-cross's "square root that would not go away"). Brief: the cheapest integer matrix congruent to H modulo 2^j at 16 and 32 points for j = 2, 3, 4, and whether the
   correction from j to j + 1 can reuse the wires of level j (the j-th correction is a difference quotient of order j: this is
   hybrid 3's question asked of non-outputs). It sounds like computing the wrong matrix on purpose.

## 7. Criticism, last

- The floor of hybrid 2 is three data points and a count on 18 files. It is known false for general circuits at astronomical
  size. I have no proof even in the one-tree class; the shortest-network argument is a sketch for one tree in bit order.
- "Every circuit is one merge tree modulo 2" covers the files that parsed. The pools searched tonight are biased to entries
  0, +1, -1 on sub-blocks, and annealers started from known circuits; the skeleton may be inherited from the seeds.
- The meter's "order" compares a wire with every earlier wire up to an odd factor; "dead" depends on gate order only through
  which of two equal classes came first. The counts new and dead do not depend on it; the split J/S does not either.
- The scatter matrix in hybrid 4 is rebuilt from h-7's numbers, not read from the certificate. The statement about the unit is
  about the matrix it must compute, not about its gates.
- Hybrid 4's lemma is three lines by hand. Its use for subset sums leans on a literature statement I only read in WAVE3-NOTE.
- Lemma P is h-8's, unreviewed; I list who hit it from their summaries.
- I did not resolve the conflict between h-7 and h-8; I only say which measurement would.
- Nothing here changes the order, or any constant.

Files: `waves/wave-04/m-cross/` : meter2.py, meter2.out (the meter on 18 circuits and the
textbook); laminar.py, laminar.out (one merge tree modulo 2); dups.py, dups.out (the staircase's extra dead gates by name);
trial2.py, trial2.out (inverse butterflies are Q gates; pieces from outputs are circular; the floor table); e8shadow.py,
e8shadow.out (the unit's scatter matrix modulo 2); precision.py, precision.out (ranks of the transform modulo 2^j; a matrix
congruent to H modulo 4 in under 4N gates). Every run went through light.py; the longest took 8 seconds.
