# Third wave of ideas: what came out (wht39)

> Editor's note (11 October 2026): "the published exponent passes to that field" (line 5 of section 1, and section 3) is one agent's argument that nobody has reviewed; I do not claim it. The "one page in my voice" that section 3 names is a draft I have not published; it is not in this repository ([LEFT-OUT.md](LEFT-OUT.md)).

11 October 2026, about 00:30. Private. Nothing here is reviewed or in Lean.
Marks: **[computed]** exact run tonight; **[argued]** by hand tonight, unchecked unless I say so; **[guessed]**; **[read]** from a paper, or from the first lines of a report still being written. "Mine" means I re-ran it for this note (`k-note/check.py`).

**What this wave was.** Eight agents each developed one idea for an hour (`g-0` to `g-7`). One agent recombined all three waves (`k-cross`). Three critics came last (`c-0`, `c-1`, `c-2`). Earlier notes: `NOTE.md`, `WAVE2-NOTE.md`.

**Words.** N = 2^k points; H·x is the transform; the *textbook* costs N·log2 N. Count **(G)**: a gate is any a·u + b·v, scalings free. Count **(O)**: OpenAI's, each addition and each multiplication by a constant costs one. A *kernel* is a 2 × 2 matrix; its *power* is the N × N matrix that applies it to every address bit. The transform is the power of [[1,1],[1,−1]]. The *class* is all kernels with four non-zero entries. The *brick* is the known 7-gate program for 4 points. *Subset sums*: for every set S, the sum of the data over the subsets of S; its matrix Z is the power of [[1,0],[1,1]].

## 1. What came out, in ten lines

1. **Nothing beats the textbook in order.** No saving of the 1e-1 kind and no linear size. What exists is, again, a better constant.
2. **8 points in 19 gates**, count (G) (`g-1`; textbook 24, best before 20) [computed: three programs of the author, the critic's, and mine]. In OpenAI's count the same wiring gives H·x itself in (5/6)·N·log2 N + N operations when 3 divides k: 4,352 against 4,608 at 512 points, the first size below the textbook [computed by the critic]. The best published rate is 23/24 (Alman and Rao, 2023) [read by the critic through a summary, not the paper itself]. In count (G) the second wave's family (rate 3/4) stays ahead from 16 points on, with a tie at 64 [argued, arithmetic].
3. **The 19 is not about the transform.** The same wiring with other numbers computes the 8-point power of every kernel tried: nine besides the transform, six written out and replayed, among them [[1,2],[3,4]] [computed, `k-cross`]. The brick likewise holds for every kernel of the class [computed: `g-3`, `k-cross`, and mine on 200 random kernels].
4. **The mirror experiment has an exact answer: 24** (section 2).
5. **Subset sums are three calls of the transform**, at every size [computed; mine for k up to 6]. The published exponent passes to that field (section 3).
6. **Flatness is not what makes the transform hard.** A matrix is *flat on both sides* when it and its inverse have all entries of one size. The Potts matrix (a number t on the diagonal, 1 elsewhere, t + 1/t = 2 − N) is flat on both sides at every N and costs 2N − 1 gates [computed for N = 5 to 64, `g-3`]. An argument for N log N must use more: small coefficients, or that H/√N preserves lengths [argued].
7. **Where the known lower bound lives.** H = Z·D·Zᵀ with D one diagonal. The known bound for small coefficients (Morgenstern's: such gates grow a determinant slowly) is paid in full by D. For Z alone the same method gives only N·(0.28·√k − 1) [argued, table computed, `g-4`].
8. **The saving is an extra value.** No 4-point program that holds only 4 numbers has 7 moves modulo 5, 7 or 13, whatever the coefficients [computed, exhaustive, by two agents separately]. The brick holds a fifth number. Over the rationals this is [guessed].
9. **Two-step words stop.** Write H as a product of *tree steps* (matrices of about 4N gates each). In the one shape studied, two steps make the transform at 16 points [computed by the critic] and cannot from 64 points on [argued by `g-6`, and again by the critic]. One case is left at 32 points (section 4, D).
10. **Alive:** the class question; counting rectangles; the mirror's growth law; words of three steps; a discount on many copies.

## 2. The mirror experiment

**The question.** At 16 points the transform, after a free relabelling of its outputs, is a *reflection*: it changes the data only along a 6-dimensional subspace, which the reports call the *mirror*. So one route is: read 6 coordinates along the mirror, do a small 6 × 6 step, write back, correct the input. The first wave asked for the cheapest way to read: the fewest gates that compute six independent forms of the mirror. The known ends were 20 and 34.

**The number: 24 gates**, count (G), 4 per form (`g-0`). The circuit is replayed exactly [computed]. The matching lower bound is a hand argument on machine-checked facts, read by nobody [argued].

**What it means.**
- The choice of basis matters: 24 against 34 for the obvious basis.
- It does not give a transform. Read + middle + write is at least 30, so the route costs at least 56 [argued, for this three-part shape only]. The night's best at 16 points is 52.
- The reason is geometric. The mirror carries 16 special points, 16 lines at one common angle [computed; mine: cosine 1/3]. No two are perpendicular. A basis that is cheap to read is then expensive to write back, gate for gate.
- Growth: cost = N + √N + x(N), where x is the number of helper points needed. A linear-size basis means x(N) = O(N). One exact value exists, x(16) = 4. At 64 points there are only bounds, 72 to 204 gates, and what made 16 cheap, relations among four points, is gone (the shortest has eight) [argued].
- Every kernel tried has such a mirror (dimension 1, 6, 28 at 4, 16, 64 points), and "never perpendicular" held for the four kernels of the class that were tried [computed, `k-cross`]. For the subset-sum kernel most pairs are perpendicular. That is where the search goes next (`p-2`, running).

## 3. The lead for another field: subset sums and Moebius transforms

**What transfers** (`g-4`). Subset sums = multiply by (5/4)^|S|, transform, by (1/3)^|S|, transform, by (−1/2)^|S|, transform, by (3/5)^|S| [computed for k up to 10; mine up to 6; the argument is a short calculation on two numbers]. So over the rationals the subset-sum transform (the zeta transform), its inverse (the Moebius transform) and superset sums cost O(N·(log N)^(1 − 8.7625e-4)), and subset convolution O(N·(log N)^(2 − 8.7625e-4)) [argued]. With additions alone the method in use is exactly optimal [read: Kennes 1992, as quoted by Kaski, Kohonen and Westerbaeck, 2016], so subtraction and division help by a growing factor. Two calls can never do it [argued].

**Literature** (five searches, four papers opened; not a survey) [read]. Alman and Li (arXiv:2509.14489, 17 September 2025) call the classical method the best known circuit and print the reverse identity. Boyar and Find (2012): optimal for XOR circuits without cancellation, general case open. Alman (2023): a speed-up over the two-element field in bit operations, a different model. Nobody found states the three-call identity, or an exact subset-sum transform below N log N.

**Not claimed.** No gain at any real size: with every constant set to 1 the crossover is log2 N near 10^888. Nothing without subtraction, nothing where one cannot divide by 2, 3 and 5, nothing over the two-element field, nothing about bits. The statement is not in Lean. I do not claim it is new to everyone.

**Where.** One page in my voice, private: `g-4-zetalead/note-for-zeta-readers.md`. Working file: `g-4.md`.

**One figure to look at.** README line 742 says log2 log2 n must exceed "about 8e6"; 6049 / 8.7625e-4 is 6.90e6 [computed by `g-4` and by me; I did not check which constants that line uses].

## 4. The ideas that are alive

**A. Is any saving special to the transform?** Every saving of three waves is an identity of the whole class: the brick, the 19, and the 3/4 family, even with a different kernel on each bit [read: `h-6`, first lines]. For kernels with entries t^(distance between addresses) the 19 is a fact about distances: distance(x, y) = q(x) + q'(y) + m(x, y), with m in {−2, 0, 2}, and the cells with m ≠ 0 covered by twelve rectangles [computed at t = 2, 3]. The transform needs m only modulo 4. If that never saves a rectangle, the transform's special structure is description, not a lever, and the search may move to the member easiest to search. *Next:* rectangles at 16 points, whole numbers against modulo 4 (`p-0`, `p-4`, running).

**B. Count rectangles instead of searching circuits.** The 19 unrolls into a tree on the inputs, a tree on the outputs, and the matrix written as a sum of τ constant blocks (a node of one tree × a node of the other); gates = N − 2 + τ. τ = 5 and 13 at 4 and 8 points [computed]. Two numbers fit several laws; one of them, τ = 2N − 3, is linear [guessed: a fit]. The third number so far is 49 at 16 points: two designs of one family, a floating-point solver, not replayed [computed, weak]. That is 63 gates, above 52. *Next:* the least τ at 8 points over all pairs of trees; 16 points outside that family (`p-1`); products of two such sums (`p-7`).

**C. The mirror's growth law** (section 2). *Next:* x(64), and the same search on the subset-sum kernel.

**D. Short words.** About k/2 tree steps make the transform, at about twice the textbook's cost [computed at 8 and 16 points, `g-3`]. A bounded number of steps would be linear size. One step fails from 8 points on [argued]. Two fail from 64 points on in the periodic shape; at 32 points one case remains, exactly tight: 16 exceptions needed, 16 available [argued by the critic]. For three steps the argument gives no bound at all [argued twice]. Limits of two-step products are not covered either. *Next:* decide the 32-point case exactly (`p-3`); then three steps at 64 points.

**E. A discount on many copies.** After half a transform, the rest is √N copies of the √N-point transform done together (`g-7`) [argued]. A discount d on such batches at every squaring gives exponent 1 + log2 d; d = 0.933 would be a saving of 1e-1. Seen so far: 7/8 once, from the brick, and no discount for two copies of a 3-point cousin [computed modulo 3, 5, 7]. *Next:* two and four copies of the 4-point transform, exactly.

## 5. The walls, as lemmas

All [argued] unless marked; small cases [computed].

- **L1. Half and half.** If H = B⁻¹·(cheap middle)·B, then B costs half a transform and B⁻¹ the other half. Exact at 4 points (4 + 4); 32 + 32 over about 112,000 bases at 16 points; 192 + 192 at 64. Hit by `d-0`, `d-3`, `d-4`, `d-7`, `g-0`, `g-2`, `g-5`, `g-7`.
- **L2. Copies do not share.** Transforms on separate data cost the sum. First exact case: two copies of the 3-point cousin cost exactly 8 [computed modulo 3, 5, 7]. Hit by `d-2`, `d-6`, `e-3`, `e-6`, `e-7`, `e2-1`, `e2-2`, `j-manyatonce`, `g-5`, `g-6`, `g-7`. Not broken.
- **L3. Tight wires.** A *wire* is a value the program holds. Its *spread* is (its non-zeros written in the inputs) × (its non-zeros written in the outputs), never below N; *tight* means equal to N. If every wire is tight, or is a product of one two-point vector per bit with entries of any size, the program needs N·log2 N gates. From `a-2`, refereed by `g-1`; hit by `e-0`, `e-1`, `e-2`, `e-4`, `e2-1`, `e2-3`. Its old reading, "the winning wire is an eigenvector of the transform", is withdrawn (lines 3 and 6).
- **L4. Volume.** A gate with coefficients of size c buys about log2 c bits of determinant; the transform needs (N/2)·log2 N. Programs whose values are all vectors of 0, +1, −1 need at least 0.315·N·log2 N. Linear size with c·N gates needs coefficients near N^(1/(2c)). Hit by `d-5`, `e-5`, `e2-0`, `j-failproof`, `g-1`, `g-3`, `g-4`, `g-5`. Large numbers alone bought nothing wherever tried [computed: 4 points in place; one 8-point design, numbers up to 1,024].
- **L5. One class.** The transform and subset sums are one question for the order (three calls one way, two the other). At 4 and 8 points the whole class shares its circuits. Hit by `d-0`, `a-0`, `g-3`, `g-4`, `g-5`, `k-cross`.
- **L6. The extra value** (new). Line 8. In rectangle words: the circuit's middle holds 1 and 5 values more than N at 4 and 8 points, and those are the saving. `g-3`, `g-7`.
- **L7. Two periodic steps stop** (new). Idea D. `g-6`, `c-2`; `g-3`'s open case is the same question.
- **L8. One sum of rectangles needs perpendicular trees** (new, unreviewed). Unless the two trees are subgroup chains perpendicular to each other, about N²/8 rectangles are needed. `k-cross`; the 19's trees are exactly that case [computed].

No wall covers a program whose wires mix many address bits inseparably, with coefficients growing like a power of N, and with work shared between copies.

*Corrected this wave.* Small primes gave two false circuits (modulo 5 and modulo 7; `g-3`): later searches use 13 and 37. The first wave's "nobody has badly conditioned steps with a perfectly conditioned product" is false as stated (`g-3` has a family at 16 points), and that family buys nothing [computed].

## 6. The next eight experiments

Folders `p-0` to `p-7` were already running when I wrote this.

1. `classtest`: are the 20, the 52 and a 12-gate cousin identities of the whole class?
2. `mirror64class`: the mirror search on the subset-sum kernel, exact at 16 points, bounds at 64.
3. `hatch32`: decide the last two-step case at 32 points (now the shape 16 × 2).
4. `exponent` / `formula`: cover "distance minus q minus q'" by rectangles at 16 to 64 points, whole numbers against modulo 4.
5. `unimodular`: the kernel [[1,1],[1,2]], which has no determinant bound. First lines [read, `p-5`]: its best counts already use coefficients 1 and 2 only, and its question turns into "does H/√N need N log N gates with small coefficients".
6. `selftranspose`: one tree used forwards and backwards. First lines [read, `p-6`]: none at 8 points in its model; only chain-like trees survive.
7. `twoletters` / `letter16`: products of two rectangle sums at 16 points, against 52.
8. (silly) `tletter` / `fibonacci`: run the 19 with t as a letter; get the third term of 5, 13, … exactly.

## 7. What this says about linear size

Nothing found in three waves gives linear size or moves the exponent, and nothing found forbids it: each wall is about one class of programs [argued], and each saving is a constant (19/24 and 3/4 in count (G), 5/6 in OpenAI's count) [computed]. The new information is mostly about where not to look: the two things that save gates use nothing special to the transform [computed], every route through a change of basis has paid half going in and half coming out [computed at 4, 16, 64 points], and large numbers alone have bought nothing in any exact experiment [computed, small sizes]. What remains open and finite is short: three-step words, sums of rectangles whose count per point stays bounded, and a discount on batches of copies, with the mirror's helper count x(64) as the first number to get.
