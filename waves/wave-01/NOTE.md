# Ideas first, criticism last: what came out (wht39)

10 October 2026, late evening. Private. Nothing here is reviewed or in Lean.
Marks: **[computed]** exact run tonight; **[argued]** by hand tonight, checked by nobody else; **[guessed]**; **[read]** from a paper or an earlier note.

**How it was run.** Eight agents each took one move a mathematician makes when hunting for an idea: break the obstruction's assumptions on purpose; rewrite the object in other languages; study its nearest relatives; read a solution backwards from the goal; play with the smallest cases; ask what other fields did; read the cost model like a lawyer; invert, exaggerate, combine. No odds, no critic. That gave 77 ideas. Eight were developed for an hour each, one agent recombined them, and only then did three critics attack the three best objects.

**Words.** N = 2^k points. A *gate* is one step a·u + b·v, scalings free (not OpenAI's count, which charges scalings too). The *textbook* costs N·log2 N gates: 8, 24, 64 at 4, 8, 16 points; best known 7, 21, 56. A *wire* is any linear form the program holds. *Subset sums*: for every set, the sum of the data over its subsets.

## 1. What came out, in ten lines

1. No change of order. Every object below ties the textbook or wins a constant factor; the published saving, 8.7625e-4, stands.
2. The suspected "conservation law" now has a statement. Call a wire *tight* if (its non-zeros written in the inputs) × (its non-zeros written in the outputs) = N, the least the uncertainty principle allows. A program of tight wires only needs N·log2 N gates, at every N [argued, ten lines; its one lemma computed with 0 exceptions up to 64 points].
3. So every saving lives in wires that are not tight. A second-wave 8-point circuit in 21 gates (was 22) replays exactly, and 6 of its 21 wires are over the limit [computed].
4. The transform is subset sums, one scaling, subset sums transposed. Subset sums are three transforms and four scalings, at every size [computed k = 1..5; argued in general]. So the published exponent carries over to subset sums [argued; literature not checked].
5. Subset sums never beat their own textbook: 4 and 12 gates at 4 and 8 points, exhausted over four finite fields [computed; not an argument over the rationals].
6. The mirror. After a free swap of address bits in pairs, the transform is √N × (identity minus twice a projection). The projected space has dimension N/2 − √N/2 = 1, 6, 28, 120, with one basis vector per quadratic form of one kind [computed at 4, 16, 64]. The 120 match the labels of the published E8 unit [argued from counts; the meaning is guessed].
7. A limit of cheap programs can be cheaper than any exact program: 7 against 8 gates on 4 wires, 2n − 1 against 3n − 4 on n wires [computed, with certificates]. The transform's 4-point brick has no such gap [argued].
8. One growth law would remove the log: if N parallel copies of the N-point transform shared more than half of their extra gates, the size would be linear [argued]. Nothing yet shows that they share anything.
9. Four unrelated routes (chains of the cube, a symmetry-adapted basis, self-dual codes, identities special to the transform's own point) end at one count: k/2 layers in and k/2 out [argued; computed at small sizes]. One wall, not four.
10. Alive: the cheapest basis of the mirror, and copies that share. Both are finite questions at small sizes.

## 2. The ideas that are alive

**A. The cheapest basis of the mirror.** The transform costs at most (read the mirror's coordinates) + (put them back) + N, and a linear transform would give a linear mirror [argued]. So linear size is exactly "some basis of the mirror costs O(1) gates per form, in and out". Any basis will do, a freedom no tensor recursion sees. One tree of sums carries at most √N mirror forms, so the forms must reuse each other's wires [argued]. A second-wave greedy search at 16 points found 26 gates for the six forms (58 for the whole program, against 56 known), and 34 for bases built from characters [computed, greedy, one family only]. The lower bound is 20 [argued]. *Next hour:* the exact least cost of six forms spanning the mirror at 16 points, with bases outside the character family, above all nested ones (like running sums, where supports 1, 2, …, N cost one gate each). Near 20: the freedom is real. Near 26 to 34: the mirror ties too. Whether the searcher reaches 16 wires is untested.

**B. Copies that share.** The log is the cross term of a tensor product: parallel copies that share nothing [argued]. If N copies each pay only 1/ρ of the extra gates, the extra per point obeys, nearly, f(2k) = 2 + (2/ρ)·f(k). ρ = 1 is the textbook, ρ = 2 gives N log log N, ρ > 2 gives linear size, and a saving of 1e-1 needs only ρ = 1.07 [argued; table computed]. Seen: 13 gates for a small product where the product rule gives 14; the shared piece is a helper that is not a product of one form on each factor [computed]. Against: two 4-point copies need 14, not 13 [argued, unchecked]. *Next hour:* exhaust all products of small sign matrices on 6 wires, sort them into "shares" and "does not", and find the rule.

**C. Wires far over the limit as building material.** The tight-wire argument has a form with slack: summed over all gates, log2(1 + 2P/N) is at least N·log2 N, where P is the largest product of the two non-zero counts among the gate's three wires [argued; checked by runs]. So in a program of c·N gates a fixed share of the gates touch wires with P at least N^(1+1/(2c)) [argued, by averaging, not sharp]. The over-spread wire is the bulk of a linear program, not an occasional helper; a fixed brick saves only a constant factor. *Next hour:* compute this sum for the 7-, 21- and 56-gate circuits and the published unit; then look for forms whose spread grows with N at one gate each. The mirror's forms may be such [guessed], which ties C to A.

**D. Limits.** The gap in line 7 is seen only at small size. Making a limit program exact multiplies its size by (d + 1)², d the order of the limit [argued], so a change of order needs d to grow with N and a cheaper conversion. *Next hour:* at 8 points, let two wires of the 21-gate circuit approach each other and look for 20 [guessed].

## 3. The walls, as lemmas

**W1. Half and half** [argued; computed at k = 4]. Any basis in which the transform becomes a relabelling with scalings shares at most k/2 directions with the standard basis. So k/2 layers in, k/2 out: the textbook. Hit by `mod4` (at least k/2 commuting steps), `codes` (39 such bases at 16 points, the closest being the three self-dual codes), `zeta` and `spin` (an exact tie: half in the basis change, half in the middle).

**W2. Copies do not share** [argued in two small cases only]. "t copies of the n-point transform cost t times one." Hit by `letters` (two calls on one pairing are both forced to be the half-size transform), `excess`, `spin`, `zeta` and the recombined "squares" route. It blocks every recursion. It does not block linear size as such.

**W3. Tight wires** [argued for every N]. Line 2 above. A tight wire has a level, log2 of its non-zeros; a gate joins levels at most one apart; each of the k levels needs N gates. Among tight-wire programs the same count gives the textbook figure for subset sums. The inequality is known [read]; the critic did not find the circuit statement in a short search.

**W4. Exactness** [read + argued]. Bounded coefficients force N log N (Morgenstern). The same holds for all line sums of a finite plane (`plane`). Limits convert at (d + 1)² (`border`). So a linear program is a product of badly conditioned steps whose product is perfectly conditioned. Met separately by `zeta`, `plane`, `letters`, `mod4`, `border`.

**W5. One class** [argued; computed on 2,000 random cases]. For every invertible rational 2 × 2 matrix that is not a relabelling with scalings, its tensor powers cost the same as the transform up to constants 4 and 6 and a linear term. So no fact special to the Walsh-Hadamard point can be *needed* for linear size. It can still be the mechanism.

**Taken back by the critics.** The "squares" route (62 gates at 16 points) is the textbook circuit in other coordinates; its tie is not independent evidence. "Every kernel is two calls of the transform" is false over the rationals. "Any Jordan basis works" fails at 4 points. The log-log middle overtakes the dense one only beyond N = 2^4096. In the 56-gate circuit the helpers are not full on both sides; the true statement is only "not tight".

## 4. The most surprising thing, and the question that would tell the most

Reorganisations from unrelated mathematics landed on the textbook count to the last gate, and the only thing that ever went below was one kind of object: a helper wire that is not a character on a coset. Within the night that pattern became a short argument (W3) that puts every possible saving in the wires over the uncertainty limit. [guessed: it is the law behind the other ties too; argued only for the textbook and subset sums.]

The question: **what is the cheapest basis of the mirror?** It is linear size restated with the most freedom, it is finite at 16 and 64 points, and it has had a greedy run only.

## 5. Everything that was thought of (77, numbered as in `PICKS.md`; → marks the eight developed)

*Break the obstruction.* 0 Flag steps, dense at every scale. 1 Identities true only at the transform's own point → `mod4`. 2 Chains of codes in phase space → `letters`. 3 All the volume in one scaling → `zeta`. 4 The floor's diagonal is a self-dual code → `codes`. 5 The total-spin basis → `spin`. 6 Relabelling plus a nested low-rank remainder. 7 Coefficients that grow by design → `border`. 8 The tiling theorem as a map. 9 Two factors, each almost of rank one.

*Other languages.* 10 Words in coset reflections → `letters`. 11 Rows near a common centre. 12 The transform as matrix transpose. 13 V-cycle through a Gram inverse. 14 Symmetry sectors: mostly tiny blocks → `spin`. 15 Rank-one blocks on a self-dual code → `codes`. 16 Change the metric: kernels with a sparse inverse. 17 The chirp as a short product of coset sums. 18 Apply one projector of rank N/4 instead. 19 The cube's neighbour sum as a stepping stone.

*Cousins.* 20 The Grover-diffusion family: a linear cousin. 21 How few layers of reflections. 22 Bits of entropy per gate as the currency. 23 Aim at subset sums → `zeta`. 24 Cube neighbour sums, the nearer problem. 25 One fixed matrix times an arbitrary matrix. 26 Schur-Weyl basis → `spin`. 27 Products of tree-diagonal operators → `letters`. 28 Sparse stencil layers are the textbook. 29 Rank-deficient neighbours of the Hadamard block.

*Backwards from the goal.* 30 All the volume in one diagonal → `zeta`. 31 Carry eigenforms: a cheap eigenbasis. 32 Relabel first: reflect through a smaller space. 33 Fill "identity plus one projection" at 16 points. 34 A half-size space with sparse checks. 35 Self-dual codes make it a transposition → `codes`. 36 Count passes per squaring. 37 The nearest solvable problem. 38 Differences and running sums as changes of basis. 39 Cut the diagonal and recurse on heavy addresses.

*Play.* 40 Count wide factors, not butterflies → `letters`. 41 A covering puzzle in the convolution algebra. 42 The law of excess under tensor product → `excess`. 43 Layers from zero-excess rectangles → `excess`. 44 A few shared helpers instead of one. 45 Polar coordinates on the field with N elements. 46 Is a pair of arrays cheaper than two singles? 47 Keep a subgroup of frequencies → `letters`. 48 A sparse inverse instead of a circuit. 49 Odd radix as a source of bricks.

*Other fields.* 50 Pay in running sums. 51 Subset sums, a scaling, superset sums → `zeta`. 52 Retire coordinates as wavelets do → `spin`. 53 Fast multipole and the butterfly algorithm. 54 Strassen tuned to a known factor. 55 Self-dual codes and theta functions → `codes`. 56 The V-cycle read backwards (multigrid). 57 Border circuits → `border`.

*The cost model.* 58 Line sums of a finite plane → `plane`. 59 Spend the unused power: ill-conditioning → `border`. 60 A transpose in disguise: chain instead of lattice. 61 A short sum of cheap tensor products. 62 A model in which the transform is free → `codes`. 63 A linear exact transform over a fixed finite ring. 64 The outrageous program: one remainder per output. 65 Pointer trees: relabelling at geometric cost.

*Wild.* 66 Transform only an information set. 67 A free signed relabelling minus a low-rank matrix. 68 The exponent is a density of outputs. 69 A square root of a free relabelling → `mod4`. 70 A cheap wrong answer, exact on most entries. 71 A basis that ignores the transform → `spin`. 72 A new letter: the resolvent of a relabelling. 73 The linear recursion read backwards. 74 (silly) Characteristic 2 first → `mod4`. 75 (silly) N shifted copies at once. 76 (silly) Differentiate a family → `border`. Unnumbered, same agent: "solve, do not apply"; "(silly) batches are not additive".

*Not covered here.* A second wave in the same folder (`e-0` to `e-7`, `j-*`) was still writing. The six reports I opened say they found no change of order. I used two of its results (the 21-gate circuit, the greedy mirror run) and nothing else.

## 6. What this says about linear size

Nothing found tonight gives linear size or moves the exponent, and nothing found forbids it: each wall is a statement about one class of programs, and no lower bound above linear is known outside those classes [read]. What changed is the description of the target: a linear program, if there is one, is mostly wires spread far beyond the uncertainty limit, is built from badly conditioned steps, is not a recursion on copies of itself, and need not use anything that only the Walsh-Hadamard point has [argued]. The honest state is "open, with a sharper target and one finite experiment not yet run exactly", not "closer".
