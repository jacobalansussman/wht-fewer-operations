# j-manyatonce: change what it means to compute, many arrays at once

10 October 2026, 21:39 to 22:19 EDT. Private. One agent, 40 minutes, nothing in Lean, nobody has read this.

Marks: [read] = on a page or in a file I opened tonight; [ran] = exact computation tonight (programs in `j-manyatonce/`);
[derived] = worked out here by hand, unchecked by anyone; [guess] = a guess, including anything I only remember from papers.

Gate counts. **(G)**: a gate is any a·u + b·v, scalings free. **(O)**: OpenAI's count, additions and scalar multiplications each charged.
Every search below is in count (G), and is done modulo a small prime p (vectors with entries modulo p, taken up to a scalar).
"None found modulo p" is a statement about that prime only: a circuit with rational or complex coefficients could have a
coefficient that is zero or undefined modulo p and so be missed. It is evidence, not a proof.

Words. A *copy* is one array to be transformed. *m copies of A* is the block-diagonal matrix with m blocks A (written I_m ⊗ A):
m independent arrays, each multiplied by A. A *discount* is any circuit for m copies with fewer gates than m circuits for one copy.
A *direct-sum theorem* would say there is never a discount. c(N) is the cost per point of one N-point transform (so the textbook has
c(N) = log2 N), and c_m(N) the cost per point when m arrays of N points are served together.

## The one thing to take away

The question "one array in linear size" and the question "many arrays at a discount" are the same question, with an exact exchange rate,
and the literature has already drawn the map of where a discount can live:

- **Exchange rate** [derived]. The N²-point transform is two rounds of "N copies of the N-point transform" (rows, then columns).
  So c(M·N) ≤ c_M(N) + c(M). If N copies cost a fraction θ of N separate transforms, then c(N²) ≤ (1 + θ)·c(N), and the exponent is
  z = log2(1 + θ). The published z = 1 − 8.7625e-4 is the rate θ = 0.99879. A saving of 1e-1 is θ = 0.866. Linear size is θ → 0.
- **Where a discount cannot be** [read, Jukna's page for open problem 7.7 of Jukna and Sergeev's survey]. For circuits of depth two
  (one layer of sums in the middle) the cost of a direct sum is exactly the sum of the costs. For circuits without cancellation the
  same (a mixed wire that reaches an output leaves a cross term unless something cancels it). So a discount needs **both**
  cancellation **and** at least three layers.
- **Where a discount certainly is** [read, same page: Paul 1976, Corollary 2, credited to a referee]. For a typical n×n matrix A,
  n copies cost n^2.81 or less, not n·n²/log n, because "n copies of A" is the matrix product A·X and Strassen's method applies.
  So there is **no direct-sum theorem for linear circuits**, and nobody can prove n log n for the transform by forbidding discounts.
- **At the smallest sizes there is no discount** [ran]. Two 4-point transforms need 14 gates modulo 3 (complete search: no circuit with 13).
  No discount for any of 843 random small matrices over four fields, nor for a mixed pair.

So a discount, if it exists for the transform, starts at a size nobody has searched, in circuits with three or more layers and
mixed wires that cancel. Idea 2 says what such a circuit must look like.

## What I read

- Jukna, page "Problem 7.7" beside the survey *Complexity of Linear Boolean Operators* (Jukna and Sergeev, 2013), with notes dated
  22 May 2015 and 4 June 2017 [read tonight through a page summariser, not the PDF]. Stated there for circuits of XOR gates
  (arithmetic modulo 2). Both arguments work over any field [derived]: the depth-two proof splits each middle wire into the part
  used by A and the part used by B, and the cross terms it drops sum to zero in any field; Strassen's method is over any field.
- Shitov, "Counterexamples to Strassen's direct sum conjecture", Acta Mathematica 222 (2019) 363 to 379 [read: abstract]: tensor rank
  (the number of products a bilinear map needs) is not additive over direct sums. A 2025 arXiv paper (2507.17890) says the
  counterexamples are not explicit and only known to exist in very large spaces [read: search summary only]. Schönhage's older
  example for the limit version of rank is small and explicit [guess, from memory].
- Frandsen, Hansen, Miltersen, "Lower bounds for dynamic algebraic problems" (BRICS RS-98-11, 1998) and Reif and Tate's paper on
  dynamic algebraic algorithms: keeping a Fourier transform up to date. Upper bound about sqrt(n) per operation (Reif and Tate),
  lower bound (log n)²/log log n in the straight-line model [read: a search summary; the formula is an image on the page and I did
  not see it myself].
- The cost model: I used i-model.md's reading of R/OAI (every data operation is linear; control cannot depend on data; scalars are
  computed on the word side and each operation is charged). I did not open the Lean files myself tonight.

## What I ran

| What | Result | Where |
|---|---|---|
| One 4-point transform, count (G), mod 3 and mod 5 | 7 gates; none with 6 | `ds.c`, `runs.out` |
| **Two 4-point transforms in 13 gates, mod 3** | **none**: complete search, 119,043,675 nodes, 117 s | `ds.c`, label j-many-p3; line copied into `runs.out` |
| The same mod 5 | **not finished**: 8 parts, 560 s each on the Linux machine (load 25), all stopped by the clock; no circuit printed in the part covered | `linux/p5_F5_part*.out` |
| Two butterflies in 3 gates | impossible [derived]: four outputs, no two proportional, none an input | |
| 4-point transform + 4-point subset-sum table in 10 gates (they cost 7 and 4) | none mod 3, none mod 5 | `mixed.txt`, `runs.out` |
| The 3-in-4-out rectangle (4-point transform with one input removed; i-play's suggestion): one copy 5 gates | two copies: none with 9 (mod 3, 5, 7), 10 found; three copies: none with 14 (mod 3, 5), 15 found | `rect.out` |
| Sanity: does the search find the 2-copy circuits that exist | yes (two 3-point matrices: 8 = 4 + 4 for one; 10 = 5 + 5 and none with 9 for the other) | `runs.out` |
| Random invertible matrices, two copies in one gate fewer than twice one | 0 of 60 (3×3 mod 5), 0 of 300 (3×3 mod 7), 0 of 300 (4×4 mod 3), 0 of 60 + 123 (4×4, 5×5 mod 2) | `scan.py`, `scanB.out` |
| N shifted copies, N = 4, 8, 16; general batch in shift-and-sign coordinates, N = 4, 8; two copies as three shears, N = 2, 4, 8 | all identities hold exactly | `play.py`, `play.out` |

The scan only covers matrices whose one-copy circuit has at most 3 gates that are not outputs (depth of search), so it says nothing
about matrices that are expensive for their size. A fifth scan (4×4 mod 5) was stopped by the clock with no result and is not counted.

## Ideas

### 1. The exchange rate, and a ladder: how many copies before each one is linear? [derived]

- **Construction.** Stop asking for one array. Ask for the smallest batch size g(N) at which a batch of g(N) arrays of N points
  costs O(1) per point. Then c(g(N)·N) ≤ O(1) + c(g(N)), by the two-rounds identity above, applied with the batch as the second leg.
- **The ladder.** g(N) = N^a for a fixed a gives c(n) = O(log log n). g(N) = log N gives c(n) ≤ C + c(log n), which is
  n·log\*(n) total (log\* is the number of times one must take a logarithm to get below 1; it is at most 5 for any real n).
  g(N) = constant is linear size.
- **Why it might live.** It replaces "find a linear circuit" by a graded family of easier targets, and the published result already
  sits on the first rung (a discount at one fixed batch size, compounded: this is how the job's brief describes it; I did not check it in the engine). The engine's unit serves W arrays; what is its θ as W grows?
- **First sign of life.** Any batch size m and any N with a circuit for m copies of the N-point transform under m times the best
  known single one.
- **Tried.** The numbers above (z against θ) [ran: `play.out`], and the smallest case by search: m = 2, N = 4, no discount modulo 3.
- **Caution on direction.** A discount gives an exponent. An exponent does not give back a discount: one direction only.

### 2. A discount must be made of doubly mixed gates: count them [derived, extends i-play I7]

- **Construction.** Take any circuit for A ⊕ B (A on array 1, B on array 2). Set array 2 to zero: what is left is a circuit for A, in
  which a gate has become free if one of its operands vanished or the two became proportional. So
  gates(A ⊕ B) ≥ gates(A) + gates(B) − d, where d counts the gates whose two operands are both genuinely mixed (independent
  on array 1 **and** independent on array 2). Count (G); in count (O) the leftover scalings cost.
- **What it says about the shape.** For m copies the discount is at most (m − 1) times the number of such gates. A large discount
  needs **most gates to be doubly mixed**: private cheap encoders per array, a big shared core working on mixtures of all the
  arrays, private cheap decoders. The encoders cannot act on the batch index alone (they would commute with the copies and do nothing)
  [derived]: each encoder must mix the batch index with the address inside the array.
- **Why it might live.** Paul's example has exactly this shape (Strassen adds blocks of X before multiplying), and the depth-two
  theorem says the core cannot be one layer.
- **First sign of life.** One invertible, cheap E on (batch) × (array) for which E·(I ⊗ H)·E⁻¹ is cheaper than I ⊗ H.
- **Tried.** The complete search for d ≥ 1 at two 4-point arrays modulo 3: none. Mixed pair, the rectangle (two and three copies) and 843 random matrices: none.
  What it taught: at these sizes the shared core has no room, since every output needs its own gate and only 5 or fewer are left.

### 3. Paul's trick on the transform itself: what Strassen does to a Hadamard block [derived]

- **Construction.** Write the 2N-point transform as blocks [[H, H], [H, −H]] and run Strassen's seven-product recipe for
  (this matrix)·X. The seven left factors are sums of blocks.
- **Tried by hand.** Three of the seven products vanish identically (H − H, H − H, H − H); the other four are H, −H, 2H, 2H. So
  Strassen's recipe degenerates to the textbook: four calls and the same additions. The discount for typical matrices comes from left
  factors that are *new* matrices; for the transform every block combination is 0 or a multiple of H.
- **Yes, and.** So choose a block splitting in which the combinations are new and *cheaper*: split by a subgroup that is not a
  coordinate plane (cosets of a code), or split H into "all-ones part plus sparse part" (the 4-point transform is J − 2·I, the fact
  behind 7 gates) and run a fast-matrix-multiplication recipe on that pair. Target: n copies of the n-point transform from fewer
  than 4 batches of half size, where the batches are of cheaper matrices.
- **First sign of life.** A recipe at 4 × 4 blocks whose left factors, evaluated on the transform, have total cost below 4 transforms.

### 4. N shifted copies: the closed form, and the batch in shift-and-sign coordinates [ran]

- **Closed form.** Let X hold the N shifts of x (X[a][b] = x[a XOR b]). Then H·X = diag(Hx)·H: output w of copy b is ±(Hx)[w].
  Cost: one transform plus copying with signs, so c(N)·N + 0 in count (G) for N² outputs. A batch costs what its degrees of freedom cost.
- **General batch.** Every N×N batch is a sum of N "twisted shift families" (a family of shifts multiplied by one sign pattern c),
  and H·X = Σ_c (shift by c)·diag(H m_c)·H, where m is the table of coefficients [ran, N = 4, 8]. Each of the three steps
  (find m, transform its columns, assemble) is again "N copies of an N-point transform".
- **What it taught.** In batch language: (N copies of H) × (the free relabelling (b, a) → (b, a XOR b)) = (a free sign pattern) × (N copies of H).
  The batch transform turns a free relabelling into a free diagonal. Same fact as i-wild 4 and 11, now as a statement about batches.
- **Yes, and.** A batch with s twisted families costs s transforms plus (s − 1)·N² additions. So the useful question is the reverse:
  which *cheap* preprocessing of a general batch concentrates it on few families? First thing to run: at N = 4, the rank of a general
  X in the 16 families after each of the free relabellings.

### 5. Online against offline: the one place where a logarithm is known to be saved by batching [read + guess]

- **Fact.** Keeping running totals up to date costs about log n per operation when updates and queries are interleaved, and O(1) per
  operation when all the queries come at the end (prefix sums) [guess: Fredman and Saks 1989, Pătraşcu and Demaine 2004, from memory].
  The whole logarithm is the price of not knowing the queries in advance. The offline trick: each answer is the previous answer plus one term.
- **For the transform.** Online: split N = a·b, keep the half-transformed array; update costs b, query costs a, so about sqrt(N) each
  [derived]; the known lower bound is far below (see "What I read"). If that bound is as the summary says, it is above log n, and then
  **no program at n log n or below can be an online one**: it must use the fact that all N outputs are wanted together.
- **Construction.** Order the outputs along a tree, in a cheap new basis T of the inputs, so that each output is its parent plus O(1)
  terms: minimise (gates of T) + (total number of differing entries along the tree of rows of H·T⁻¹).
- **Tried.** At 4 points this is exactly the 7-gate circuit (T adds the total sum; every row is then the centre plus one term) [derived].
  At 16 points the same star, built from total, row sums and column sums, costs 63 by my count, against 56 for nesting [derived, by hand].
  The minimum over T was not run.
- **First sign of life.** A basis T at 16 points with (gates of T) + (tree weight) below 56.

### 6. Data in product form: the transform costs under 2N gates on the parameters [derived + ran the counts]

- **Fact.** A product u₁ ⊗ … ⊗ u_k (k factors of 2 numbers) is transformed by k butterflies: 2k gates. A general array of N = 2^k
  numbers is a sum of about N/(k + 1) products [guess: the generic rank, with small exceptions]. So in product coordinates the whole
  transform costs about 2N·k/(k + 1) gates: 1.81 N at k = 8, 1.91 N at k = 20 [ran: `play.out`]. In "chain of small matrices" form
  (tensor train) it is 8N/3. **All of n log n is in packing and unpacking**, and both are products of data values, which the model
  forbids in the transform.
- **Linear version.** Keep a "pending transform" flag on each coordinate instead of applying it. Flags pass through every operation on
  other coordinates, and two flags on the same coordinate cancel for free (H·H = N). A program pays only for flags still up at the end.
- **Tried.** Two copies as three shears: diag(H, H⁻¹) = [[I, H], [0, I]]·[[I, 0], [−H⁻¹, I]]·[[I, H], [0, I]]·(swap with a sign), exact at
  N = 2, 4, 8 [ran]. Three "add the transform of one array to another" steps make two transforms: no gain, 3 against 2.
- **Yes, and.** The shear "y += H·x" is a new unit of account. It is the natural step of an in-place program, and a batch of them
  with a common x is free of charge after the first (fan-out). Ask for the cost of the transform counted in shears with shared sources.

### 7. What a free table can do [derived]

- **Fact.** A table that does not depend on the data can only supply coefficients. The run is a fixed linear circuit, so a table of
  O(N) scalars is exactly the coefficient list of a linear-size circuit. Nothing more, and nothing less: count (G) *is* the table model.
- **Construction.** In count (G), copying x into many differently scaled copies is free. So a batch whose columns are known multiples,
  or known diagonal rescalings D_j·x, of ONE array is free to build, and any discount for *that structured batch* is a speed-up for one array.
  The target "N independent copies" can be weakened to "N known rescalings of one array, of which one answer is read".
- **Tried.** With D_j = sign patterns the batch is the shifted family of idea 4 (free). With D_j = second-degree sign patterns
  ((−1)^(a₁a₂) and the like) the batch is "all quadratic-phase transforms of x at once"; not run.

## Anomalies and pretty facts

- No direct-sum theorem can exist for linear circuits (Paul 1976), yet depth two and no-cancellation each have one. The transform's
  best known circuits beyond the textbook (OpenAI's, the published one) are, I believe, deeper than two and use cancellation [guess, not checked].
- Strassen's seven products on the Hadamard block: three vanish, four remain. The recipe that beats every typical matrix is exactly neutral here.
- Counting parameters gives no lower bound at all for copies: the family "A ⊕ A" has as many free parameters as A.
- Two 4-point transforms: modulo 3, 14 is exact; the search space was 119 million nodes for 5 spare gates.
- 843 random small matrices over the fields with 2, 3, 5, 7 elements, and not one pair shares a gate.
- Online transform: update × query ≈ N by the obvious split, and the known lower bound is only polylogarithmic. A wide open gap next door.
- Two transforms are three shears (the standard way to write diag(A, A⁻¹) as a product of elementary steps).
- The rectangle and the square behave alike: 5, 10, 15 gates for one, two, three copies of the 3-in-4-out rectangle; exactly additive.

## Not done, and limits

- The search for 13 gates modulo 5 is unfinished. To finish: `ds 5 8 5 <part> 8 < h4x2.txt`, about 3.8 billion nodes in all [estimate].
  Nothing was run over the rationals or with the fourth root of unity; modulo 5 would cover the latter (2² = −1 there).
- Three copies of the 4-point transform (20 gates): not run; too deep for this program.
- Count (O) was not searched at all.
- The literature facts on dynamic transforms come from search summaries; the 1976 paper of Paul was not opened.
- Nothing here was compared with what the published engine's unit actually does with its W arrays.
