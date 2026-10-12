# Second wave of ideas: what came out (wht39)

> Editor's note (11 October 2026): where this note says "the best rate before was 7/8", that rate is due to Coppersmith, Feig and Linzer (1994), a paper nobody here had read when the note was written. "Alman and Rao's 23/24 (2022)" is their paper published in 2023. See [Earlier papers](../README.md#earlier-papers).

11 October 2026, just after midnight. Private. Nothing here is reviewed or in Lean.
Marks: **[computed]** exact run tonight; **[argued]** by hand tonight, unchecked unless I say so; **[guessed]**; **[read]** from a paper or an earlier note.

**What this wave was.** Twelve agents each developed one idea for an hour: seven untouched first-wave ideas, the half-touch experiment, and four of 31 new ideas. The new ideas came from four new moves: try to establish the lower bound and keep what stops each attempt; widen the problem until it is linear, then walk back; serve many arrays at once; let a machine propose circuits. One agent recombined both waves; three critics came last. The first wave is in `NOTE.md`.

**Words.** N = 2^k points; H·x is the transform. Count **(G)**: a gate is any a·u + b·v, scalings free. Count **(O)**: OpenAI's, every addition and every multiplication by a constant costs one. The *textbook* costs N·log2 N in both. A *wire* is a linear form the program holds. Its *spread* is (its non-zeros written in the inputs) × (its non-zeros written in the outputs); it is never below N. A wire with spread N is *tight*, any other is *over the limit*. A wire is *entangled* on some address bits when it does not split into a part on those bits times a part on the rest. A *hub* is a wire one gate away from several outputs.

## 1. What came out, in ten lines

1. **Nothing beats the textbook in order.** No program below the published n·(log n)^(1 − 8.7625e-4) at large n, and no saving of the 1e-1 kind. What exists is a better constant.
2. **A family of circuits** (`e2-0`) with (3/4)·N·log2 N + N/4 gates in count (G): 7, 20, 52, 128, 304 at 4 to 64 points, coefficients ±1 and ±2. The best rate before was 7/8 [computed; replayed by four separate programs, one of them mine, and through 4,096 points by the critic].
3. **In OpenAI's count** the family gives H·x/√N in (7/8)·N·log2 N + N/4 operations: 60 at 16 points against 64 [computed]. OpenAI's statement wants H·x itself, N operations more: above the textbook at 16 points (72 to 76), below it only from 4,096 points (48,128 against 49,152) [computed by the critic]. The constant 7/8 is below Alman and Rao's 23/24 (2022) [read]; a short search found no paper with it.
4. **What the record is made of.** At every size from 4 to 64 points, gates saved = number of over-limit wires, exactly (1, 4, 12, 32, 80). Each such wire has spread 4N, the smallest above the limit, and is entangled on two neighbouring bits. Every other wire is tight [computed, `j-cross`].
5. **Four walls are now statements** (section 3). New: large coefficients alone buy nothing [argued]; programs whose values are all vectors of 0, +1, −1 cannot go below 0.3155·N·log2 N [argued from Morgenstern's bound: small coefficients grow a determinant slowly].
6. **New exact identities** [computed]. The 16-point transform as one ring element: twice a product of two three-term elements, plus three subgroup sums (`e-0`). A cube identity: three twisted copies of the transform multiply to N times a small map, at 16, 64, 256 points (`e-0`). An inverse identity: the transform is, up to a tiny corner, the inverse of a matrix that is 79 % zeros at 256 points (`e-3`). For every 2 × 2 matrix [[1,1],[1,τ]] (τ = −1 is the transform), its tensor square = (rank one) + (τ − 1)·(signed relabelling): the 7-gate brick is not special to the transform (`j-cross`; I re-derived it by hand).
7. **Exact small counts.** 4 points cost exactly 8 in count (O) [computed, exhaustive]. Every size needs at least 2N − 1 gates in (G) [argued]; the 8-point minimum is between 15 and 20. However the rows and columns of H are ordered, at least (d/2)·log2 d of its 2 × 2 windows have an odd number of minus signs (`e-4`) [argued; exhaustive at 4 and 8 points].
8. **Inside the engine** (`e2-2`, critic `b-1`). A *move* is one direction of the transform on one array. The published saving obeys saving = (fraction of moves saved) / (fragmentation) = 2.111e-3 / 2.407 = 8.77e-4 [computed]; fragmentation is the price of cutting transforms into smaller calls. A new "clique lemma", argued twice independently, closes the smallest case that would have given 1.0e-1 [computed, exhaustive]. It bites on tiny batches only.
9. **The one "door" claimed** (`e-7`: one half-size call plus one quarter-size call would still be linear) is only the absence of an argument. The critic's one construction needs rows that grow like N^(1/4) [computed at 16, 64, 256 points].
10. **Alive:** wires that pay more than one gate each; wider hubs, or hubs with growing coefficients; batches of 7 to 19 arrays in the engine; the half-plus-quarter identity; words of steps that do not commute.

## 2. The ideas that are alive

**A. The staircase of hubs (`e2-0`).** A *piece* is one output restricted to a block of inputs. A lower-bound attempt stopped at one object: a helper that is one output on the lower half of a block and a different output on the upper half. It is one gate from four outputs, and its partner is a piece the level below already made, so one helper serves two neighbouring levels. Growth: (3/4)·N·log2 N + N/4, the same order. Inside its own class 20 is the least at 8 points [computed by the critic, exhaustive]; "3/4 is the end" beyond that is [guessed]. *Next hour:* hubs joining four quarter-pieces across three bits; hubs A + t·B with t growing with the level, the only kind that leaves the 0, ±1 world.

**B. Can one over-limit wire save more than one gate? (`j-cross`).** In all seven circuits measured, gates saved ≤ number of over-limit wires. As a law that would mean at least (1/2)·N·log2 N gates [argued]: order N log N. Linear size needs about (1/2)·log2 N gates saved per wire [guessed, from a second law fitted to the same circuits]. The two 21-gate circuits of this wave hold wires of spread 8N and waste them: 3 gates saved with 6 and 11 over-limit wires [computed]. *Next hour:* at 8 points search exactly for gates + over-limit wires < 24; at 16 points for < 64 (the record is 52 + 12).

**C. Batches inside the engine (`e2-2`, `b-1`).** Every array is transformed along m directions (m is the *block size*). The published unit saves 0.095 moves per array out of 45; 1e-1 needs about 9.7 [computed]. Counting plus the clique lemma forbid any saving with 11 or fewer arrays at block size 4, and 16, 17, 18 moves of 20 for 4 arrays at block size 5 [computed, exhaustive]. Larger batches pass both tests: block size 6, 7 arrays, 32 moves of 42 would give 1.5e-1; block size 5, 19 arrays, 80 of 95 would give 1.07e-1. Neither is built, and passing two tests is not existence. All of it rests on `e2-2`'s reading of the engine, unchecked against the Lean. *Next hour:* the full form of the lemma (a triangular table) on those shapes; then solve the 7-array shape exactly.

**D. Half child plus quarter child (`e-7`, `b-2`).** Shape: H = S + A·C·B, with S, A, B sparse and C made of smaller transforms. With a middle of 3N/4 numbers the known obstruction asks only 0.75 entries per row of A on average [argued; re-run by the critic up to 4,096 points], and T(N) = T(N/2) + T(N/4) + cN is linear. Seen: an exact one-call identity at 16 points (68 gates plus the child, against 64), and one construction at 3N/4 whose rows grow like N^(1/4). The open question has a name: does the transform's eigenspace sit in a space of dimension 3N/4 spanned by vectors of bounded weight (Paturi and Pudlák) [read by the critic]. *Next hour:* the B side of that construction at 16 and 64 points, by exact linear algebra.

**E. Not run by anyone.** Words that alternate two kinds of step that do not commute: every wall about one kind of step uses commutativity or one fixed order, and `e-4` argued that nothing known forbids a constant number of running-sum passes in different orders. Also, the cube and inverse identities of line 6 have no circuit yet. *Next hour:* at 8 points, every word (running sums)·(differences)·(running sums)·(differences) with two orders; the cost of the right side of the cube identity at 64 points.

## 3. The walls, as lemmas

**U. Tight wires.** A program whose wires are all tight needs N·log2 N gates in (G) [argued in the first wave]. Four new forms, each [argued] with small cases [computed]: all wires are characters on cosets, k·N gates (`e2-1`); no gate adds two forms sharing an input, N·log2 N (`e2-3`); all wires are products of one 2-vector per address bit, with entries of any size, N·log2 N, or N·log2 N / b for products over fixed blocks of b bits (`j-cross`); the window count of line 7 (`e-4`). Ran into it: `e-1`, `e-2` and `e-7` (an eigenvector has at least √N entries), `e-0` (its unexplained null vectors are tight wires), `e2-3` (greedy building wins at 4 and 8 points, then grows like N²/2), first-wave `zeta`.

**M. One magnitude.** If every value is, up to scale, a vector of 0, +1, −1, every gate has |a| + |b| ≤ 3 and the transform needs N·log2 N / (2·log2 3) = 0.3155·N·log2 N gates [argued from Morgenstern]. Ran into it: `e2-0` (the record itself), `e2-1`, `j-failproof`, `e-5` (rotation-like gates make at most about 1.2 bits per operation of an entropy that reaches N·log2 N bits), `e-0`, `e-3`, first-wave W4. New [argued]: breaking M without breaking U is worth nothing.

**C. Commuting steps.** Steps that commute, or live in one commutative ring, need about k/2 of them at N gates or more each: a constant factor at best [argued]. Ran into it: `e-6` (at least k/2 steps of its kind), `e-0` (two rings), `e-4` (running sums all on one side need log2 d + 1 passes), first-wave W1.

**S. Self-similarity.** In every identity "transform = cheap × (smaller transforms) × cheap + sparse remainder" that is reused at every scale, the smaller transforms have total length at least N [argued; computed at 32 and 64 points]. Ran into it: `e-7`, `e-3` (a cheap wrong answer exists, 99 % of entries right for 35N additions against 64N at k = 64 [computed], but the leftover costs the whole again [argued]), `e-6` (a 16-point program cut out of a 256-point identity is still a 16-point program), `e2-1` (another group's transform plus the bridge back is the textbook, to the gate), first-wave W2. Open in two places: parts that change with N (idea D) and copies that share (idea C).

**K. Inside the engine only: the clique lemma.** The engine's bookkeeping splits into sectors, one per quadratic form. A form is *tight* if exactly W moves serve it, W the number of live arrays. Moves pairwise served together by tight forms number at most W [argued by `e2-2` and again by `b-1`]. It can add at most one array's worth of moves to the count, whatever the batch size [argued].

No wall covers a program that is at once made of entangled over-limit wires, with growing magnitudes, non-commuting, and not a recursion on copies.

## 4. The most surprising thing, and the question that would tell the most

The record came from a failed lower-bound attempt, and it is as plain as it could be: one saved gate per over-limit wire at five sizes, each such wire the smallest there is, coefficients 1 and 2. Three meters invented in three different reports give the same reading. Nothing found tonight saves more than one gate per over-limit wire. The published program must do so somewhere: a program with fewer than (1/2)·N·log2 N gates saves more gates than it has wires [argued].

The question: **can one over-limit wire save more than one gate, and what does such a wire look like?** It is finite at 8 and 16 points (idea B), and the published unit is a known place to look.

## 5. The next eight experiments

The workflow had already started 1 to 7 when I wrote this (folders `h-0` to `h-7`).

1. `onepergate`: 8 points, gates + over-limit wires < 24; then 16 points, < 64.
2. `staircase3`: hubs of four quarter-pieces on three address bits; 16 points under 52.
3. `clique17`: now "19 of 20 for 4 arrays at block size 5", and the two shapes of idea C.
4. `zetafloor`: the exact 16-point minimum for subset sums (for every set, the sum of the data over its subsets): is it 32? An argument for (N/2)·log2 N there would settle the order for the whole class.
5. `ladderbound`: do programs whose wires are entangled on at most two bits need (3/4)·N·log2 N?
6. `classhub`: rebuild the staircase for τ = 2 and τ = 1/3; let τ grow and watch each saved gate.
7. `unitmeter`: read the published unit with the same meters; find the wires that carry its 120 saved moves.
8. (silly) `provethewrongthing`: try to argue "one gate per wire", which the published result says is false. The step that fails is the shape of an order-changing gate.

## 6. Everything else that was thought of (31 new ideas; → marks the four developed)

*Establish the lower bound, keep what stops the attempt.* 1 → Pieces that are not subcubes (`e2-0`). 2 The volume-free program: the whole determinant in one scaling layer. 3 Potential-blind moves first: the entropy argument cannot see triangular matrices. 4 Two simplexes in perspective: the 7 gates are a classical figure. 5 Programs that are unions of orbits of a symmetry; died at 8 points. 6 Hub capacity: see which configuration resists first. 7 Double duty by a staircase: one gate serving two half-size programs. 8 In OpenAI's count, put every scaling on a hub.

*Widen until linear, then walk back.* 9 Buy binary digits, not layers: modulo 2^b the transform costs about (2b − 1)·N gates [computed]. 10 The cheapest Smith normal form: integer sandwiches around one diagonal. 11 → Fusing is free: through a non-abelian group, with a chosen dictionary (`e2-1`). 12 Relabellings and phases close at exactly k layers; partial layers are the way out. 13 A tiling of the addresses that is not a subgroup. 14 In "train" coordinates the transform is free; the cost is writing the table. 15 Every free family is an eigenspace; log n families must share work. 16 The cost lives in the central weight band; move the mass.

*Many arrays at once.* 17 → The exchange rate between a batch discount and the exponent (`e2-2`). 18 A discount must be made of doubly mixed gates. 19 Paul's trick: Strassen's recipe on the transform itself. 20 N shifted copies: a closed form. 21 Online against offline: each output is its parent plus a few terms. 22 Data in product form; a "pending transform" flag. 23 What a free table can do: exactly a linear circuit, no more.

*Let the machine propose.* 24 Search the helpers, not the wiring. 25 → Full-drain gates: a potential a linear program must empty steadily (`e2-3`). 26 Hang the outputs on a centre. 27 Peel a centre and recurse on the remainder. 28 The subset-sum side has slack the transform lacks. 29 Outputs are not priced equally: 7, 11, 15, 17, 21, 22 gates for 1, 4, 5, 6, 7, 8 outputs at 8 points [computed]. 30 Nothing is "almost" a circuit: count modulo a prime. 31 Two copies at the smallest scale: 14 gates, not 13 [computed modulo 3].

*Taken back or corrected.* "Below the textbook in OpenAI's count" holds for H·x/√N only. "17 moves is open": closed. The obstruction of idea D bounds the average row, not each row. The first wave's guess about the singular blocks was wrong (`e-0`). The "conservation law" at 16 points is one bit per operation for rotation-like gates, and `e2-0`'s 60 operations break it.

*Not covered here.* Later reports (`g-*`, `h-*`, `k-cross`) were still being written. Their first lines say [read, first lines only]: 8 points in 19 gates (G), which by the critic's search must lie outside `e2-0`'s class; exact H·x below the textbook in count (O) from 512 points (4,352 against 4,608), rate 5/6; every wire of the published unit is a mix across arrays times a tight wire on the addresses. All still N log N.

## 7. What this says about linear size

Nothing found in this wave gives linear size or moves the exponent, and nothing found forbids it: every wall is a statement about one class of programs, and the best rates found (3/4 in count (G), 7/8 in OpenAI's count) are constants. What the wave adds is a measured description of the target: a linear program needs coefficients that grow like a power of N [argued from Morgenstern], wires entangled across more and more address bits or across blocks that change from wire to wire [argued], and wires that each save about (1/2)·log2 N gates [guessed], while no circuit seen tonight has a wire that saves more than one. The state is "open, with a better constant in hand and one sharp finite question", not "closer".
