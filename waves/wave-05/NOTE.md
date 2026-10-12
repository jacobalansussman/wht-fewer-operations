# Fifth wave of ideas: what came out (wht39)

> Editor's note (11 October 2026): the sixth note corrects two things in this one. Of the corners of subset sums this note says "No wall of section 5 covers it"; the sixth note answers that two of its own results do (its lines 2 and 9). And the counts 5, 13, 30, 80 sat on Yates' line only by a coincidence of small sizes. See line 10, "Corrections", in [the sixth note](../wave-06/NOTE.md).

11 October 2026, about 02:05. Private. Nothing here is reviewed by a person or in Lean.
Marks: **[computed]** exact run tonight; **[argued]** by hand tonight; **[guessed]**; **[read]** from a report. "Mine" means I re-ran it for this note (`q-note/check.py`). A search that is not exhaustive gives an upper bound only. "Modulo primes" means no circuit exists in arithmetic modulo the primes named: evidence, not a decision.

**What this wave was.** Nine agents each developed one idea (`p-0` to `p-8`), one recombined all five waves and tried four hybrids (`q-cross`), three critics came last (`r-0`, `r-1`, `r-2`). Earlier notes: `NOTE.md`, `WAVE2-NOTE.md`, `WAVE3-NOTE.md`, `WAVE4-NOTE.md`. The sixth wave (`u-*`) is running and is not covered.

**Words.** N = 2^k points; an address has k bits. The *textbook* computes the transform H·x in N·log2 N gates. Count **(G)**: a gate is any a·u + b·v, scalings free. Count **(O)**: OpenAI's, each addition and each multiplication by a constant costs one. Numbers are (G) unless marked (O). A *kernel* is a 2 × 2 matrix; its *power* applies it to every address bit. Up to scalings a kernel without a zero is [[1,1],[1,τ]]; the *class* is all of these and the transform is τ = −1. *Subset sums*: for every set S, the sum of the data over the subsets of S; *Yates* is the usual method, (N/2)·log2 N gates. The transform is two calls of subset sums plus free scalings, so subset sums in O(N) would be the transform in O(N) [read, third wave]. A *merge tree* starts from the N inputs and keeps replacing two held sums by one; its *nodes* are the sets of inputs under each sum. A *chain* is the most lopsided tree: x1, x1+x2, x1+x2+x3, and so on. A *rectangle* is (a set of outputs) × (a set of inputs) with one number on it. A *letter* writes the transform, after one rescaling of rows and one of columns, as a sum of rectangles whose sides are nodes of two merge trees; it is a circuit of N − 2 + (rectangles) gates. The *brick* (7 gates, 4 points) and *the 19* (8 points) are letters with 5 and 13 rectangles. The *staircase* is the family 7, 20, 52, 128, 304 gates.

## 1. What came out, in ten lines

1. **Nothing beats the textbook in order, and this wave has no record in either count.** No saving of the 1e-1 kind, no linear size [read: all nine reports and the recombination]. It has one shape closed by an argument, one question answered at 4 points, and one new question about subset sums.
2. **The letter is closed for the transform, on the trees examined.** On the *standard trees* (rows grouped by their high address bits, columns by their low bits) the fewest rectangles lie between N + (19/256)·N² and (N² + 14)/6 from 32 points on: quadratic. At 32 points that is at least 138 gates against the 128 known [argued by `p-1` and `p-8`; the critic `r-1` found no error, re-ran the small cases with his own code and added the N² term]. Other tree shapes have one run at 8 points modulo 3 and a guess.
3. **One cause.** Two rows of the transform agree, up to a factor, on exactly half of the columns, and a tree node offers one sum. Six reports hit this from six sides (L13) [argued; `q-cross` matched the statements, it did not re-derive them].
4. **Every saving of the full transform belongs to the whole class of kernels** at 4, 8 and 16 points (section 2) [computed; half exact, half modulo primes].
5. **The transform's own savings exist only on *weight-only* data** (data that depends only on how many address bits are 1): 4 gates against 5 for every other kernel at k = 2, and 7 against 8 at k = 3 [computed; the 5 is argued exactly by `r-2`, the 8 is modulo primes; the 4-gate and 5-gate circuits are mine].
6. **Two tree steps stop at 16 points.** A *tree step* is a matrix of about 4N gates, and a bounded number of them would be linear size. Two steps of periodic shape are now excluded from 32 points on; before, from 64 [argued by `p-3`; the counting is exhaustive runs, the last rank step is by hand only].
7. **Bounded coefficients.** With bounded coefficients, [[1,1],[1,2]] costs two calls of the *orthonormal* transform (H divided by √N) plus about N·√(log N), and the reverse also holds. So no member is freer than the transform. A door: the volume argument gives a floor of N·log N / R, where R is the *condition number* (how nearly dependent the held wires may become); R of about log N would escape it [argued by `p-5`, on a theorem recalled from memory].
8. **Subset sums by the "mirror" route** (third wave): 5/4 of Yates or worse at every size; the cost moves into one table as dense as subset sums [computed, `p-2`].
9. **The surprise.** The cause in line 3 is special to the transform. For subset sums on two chains the same count is at most 5, 13, 30, 80 rectangles at 4 to 32 points, where the transform's best letters have 5, 13, 45, 173 [computed by `q-cross`; mine, with my own counter and replay]. It is not a record (above Yates) and not linear on this evidence. The sixth wave's search, still running, has 80 again at 32 points and 239 at 64 [mine for the count and replay of its files].
10. **Two corrections.** "Two letters cost 2 gates more than three at 16 points" is wrong: a second 52-gate circuit is two letters [computed by `q-cross`, and by `r-0` with his own program]. "What the transform has beyond its class is worth at most N·√(log N)" does not follow [argued, `r-2`].

## 2. Is every saving an identity of the whole class of kernels?

**For the full transform, yes, wherever it could be tested.**

- **4 points, the complete list.** Seven gates are needed for every member [argued in ten lines by `r-2`]. There are 27 shapes of 7-gate circuit, and each exists with τ left as a symbol [computed, exact]. A 28th shape exists only at τ = 2, 1/2 and the two sixth roots of unity, never at the transform [computed, exact, over all 576 namings of inputs and outputs]. There is no 29th, so none for the transform alone: exhaustive modulo 7, 11, 13, 17 and 19, two programs, identical counts [computed, modulo primes]. The transform only has more placements of each shape.
- **The 28th shape has no hub.** A *helper* is a wire that is not an output; a *hub* is a helper that reads every input. Every helper set of the transform contains a hub (228 of 228) [computed, exact]. For [[1,1],[1,2]] there is a 7-gate circuit whose helpers read 2, 2 and 3 inputs [computed; mine]. So "every saved gate is paid for by one wide wire" is true of the transform at 4 points and false in the class.
- **Why that set of τ.** On one address bit there are four values, two inputs and two outputs: four points on a line, and τ is the number that says how they sit (their *cross-ratio*). The special set is exactly where the four points have a symmetry that mixes inputs with outputs; the transform's extra symmetries never do [computed, `q-cross`]. This explains the set, not the circuit.
- **8 points.** The 19's shape has the same 288 placements at seven other values of τ [computed modulo a large prime].
- **16 points.** Both 52-gate circuits exist for other kernels, including the one whose wires mix all four address bits (exact at τ = −2 and −3) [computed]. `p-0` first took that one for an exception: it moved in only 1 renaming of 1,300.

**The exceptions.** Weight-only data (line 5) and the third wave's 12-gate circuit for one mixed problem. Both use the zero 1 + τ, which only the transform has. The next size (k = 4) is undecided. A weight-only block has (k + 1)² entries, so it can never be worth more than about (log2 N)² gates [argued, `r-2`].

**What it means for the order.** Every member of the class costs at most 8 transforms [argued, `r-2`], so for the order the class is one problem and no other member is an easier place to hunt. Separately, *address maps* (relabelling the addresses inside a block by an invertible bit matrix) are symmetries of a kernel power only at τ = −1 [argued, not run], and the tiny-units note says the published engine's savings need them. So the small circuits use what the class has, and the one program that changes the order uses what only the transform has [guessed]. Nobody has a small count-(G) circuit that saves a gate with an address map.

## 3. Growth laws

Brackets: ratio to the baseline of the same block. Wave 5 has no number in count (O); those rows are the fourth wave's.

| count | 4 | 8 | 16 | 32 | 64 | law and status |
|---|---|---|---|---|---|---|
| **Transform, gates (G):** textbook | 8 | 24 | 64 | 160 | 384 | N·log2 N |
| best known (the 19, staircase) | 7 (0.875) | 19 (0.79) | 52 (0.81) | 128 (0.80) | 304 (0.79) | towards 3/4 [computed, earlier waves] |
| staircase for three other kernels | 7 | 20 | 52 | 128 | 304 | same law [computed, `p-0`] |
| best list of two letters | 7 | 19 | 52 | 132 | 304 | upper bounds [computed, `p-7`, `r-0`] |
| one letter, best found | 7 | 19 | 59 (0.92) | 203 (1.27) | 747 (1.95) | N − 2 + (N² + 14)/6 [computed to 32, then the law] |
| one letter, standard trees, floor | 6 | 17 | 46 | 138 | 430 | quadratic [argued, `p-1`, `r-1`] |
| **Transform, rectangles:** textbook | 6 | 18 | 50 | 130 | 322 | N·log2 N − N + 2 |
| one letter, best found | 5 | 13 | 45 | 173 | 685 | (N² + 14)/6; `p-1` and `p-8` independently |
| the 13's rule repeated, ideal | 5 | 13 | 37 | 101 | 293 | N^1.5; 805 against 770 at 128 points; not on trees from 16 [computed, `p-4`] |
| the same rule on trees | 5 | 13 | 49 | 177 | 705 | doubles per bit [computed, greedy] |
| two chains | 7 | 23 | 72 | 262 | 957 | last two in regular orders only [computed, `q-cross`] |
| **Subset sums, gates (G):** Yates | 4 | 12 | 32 | 80 | 192 | (N/2)·log2 N |
| two chains, rectangles | 5 | 13 | 30 | 80 | 239 | upper bounds from search [computed; mine] |
| two chains, gates | 7 (1.75) | 19 (1.58) | 44 (1.38) | 110 (1.38) | 301 (1.57) | N − 2 + rectangles |
| mirror route | | | 41 (1.28) | | 306 (1.59) | 41 direct; 306 and 1,846 (1.80, at 256 points) in a redundant form, not assembled end to end [computed, `p-2`] |
| **Weight-only block:** transform / others | 4 / 5 | 7 / 8 | open | | | sizes k = 2, 3, 4 |
| **Transform, operations (O):** textbook | 8 | 24 | 64 | 160 | 384 | N·log2 N |
| up to one common factor | 8 | 20 (0.83) | 56 (0.875) | 144 (0.90) | 320 (0.83) | [read, `h-3`] |
| H·x exactly | 8 | 24 | 64 | 160 | 384 | ties; 4,352 against 4,608 at 512 points [read] |

**What the table says about the order.** For the transform every row is either a constant between 0.79 and 0.875 times N·log2 N, or it grows faster than the textbook. No row bends towards a bounded number of gates per point. The one-letter rows are quadratic. The subset-sum row sits on Yates' line through 32 points (30 and 80 against 32 and 80) and above it at 64, where the search is weak. Nothing in it points to linear size [computed for the numbers, guessed for the trend].

## 4. The ideas that are alive

**A. Corners of subset sums.** Put the outputs in one order and the inputs in another, and draw the 0/1 matrix as a picture. The two-chain circuit is: running sums of the inputs, then each output = the next output plus a few running sums. Its rectangles are the *corners* of the picture, the places where its outline turns. Bounded corners per point would be subset sums in O(N) and the transform in O(N). No wall of section 5 covers it: L13 needs half-agreeing rows, and running sums mix every address bit [argued by `q-cross`; an absence of argument, not an argument]. Measured: on Yates' line. *Next:* 1.

**B. One run per step.** At 4 and 8 points every subset sum is its neighbour plus or minus one run of consecutive inputs [computed; mine]. If that held at every size the cost would be 3N − 4. The search has it for 13 of 16 steps and 21 of 32. A "no" with a reason would be a first lower bound for subset sums with subtraction, in a model. *Next:* 2.

**C. Nearly dependent wires** (line 7). Volume is the only wall with a named door. It was tried once: the third wave's `g-3` built badly conditioned steps with a well-conditioned product at 16 points, and they bought nothing [computed]. `p-5` adds that the door is mild (a condition number of about log N) and that a gain needs three nearly dependent wires; every saving found so far uses an extra value instead [read]. The recombination's list has no experiment for it. *Next (from `p-5`):* search at 4 and 8 points for gates on nearly dependent wires that gain more than well-conditioned gates can and still end in a well-conditioned output.

**D. More letters.** `p-7` argues that two letters are one letter at √N points, so a bounded number stays N·log N (unchecked). The staircase's lists use 1, 2, 3, 4, 5 letters at 4 to 64 points, but the second 52 is two, and at 32 points two letters have 132 gates against 128. Whether the number of letters must grow is open. *Next:* 3.

**E. Which two of the four points are the inputs.** Choosing a different pair turns τ = −1 into 2 or 1/2, where the hub-free circuit lives. Mixed choices, one per address bit, are new small problems. *Next:* 6.

## 5. The walls, as lemmas

All [argued] unless marked; small cases [computed]. Numbers continue `WAVE4-NOTE.md`.

- **L1. Half and half.** A change of basis costs half a transform in and half out. `d-0`, `d-3`, `d-4`, `d-7`, `g-0`, `g-2`, `g-5`, `g-7`; now `p-2` (line 8) and `p-5` (line 7).
- **L2. Copies do not share.** `d-2`, `d-6`, `e-3`, `e-6`, `e-7`, `e2-1`, `e2-2`, `j-manyatonce`, `g-5`, `g-6`, `g-7`, `h-2`, `n-2`. The published unit is the one exception.
- **L3. Tight wires** need N·log2 N gates. `a-2`, `e-0`, `e-1`, `e-2`, `e-4`, `e2-1`, `e2-3`, `g-1`. Sharpened into L9.
- **L4. Volume.** Small coefficients grow a determinant slowly. `d-5`, `e-5`, `e2-0`, `j-failproof`, `g-1`, `g-3`, `g-4`, `g-5`, `h-1`, `n-0`; now `p-5` (the door of idea C) and `p-8` (for a letter, large numbers do not help either).
- **L5. One class.** `d-0`, `a-0`, `g-3`, `g-4`, `g-5`, `k-cross`, `h-6`; now `p-0`, `r-2`: complete at 4 points, broken only on weight-only data.
- **L6. The extra value.** `g-3`, `g-7`; `p-5`: for [[1,1],[1,2]] at 4 points the saving needs an extra value and a coefficient 2.
- **L7. Two periodic tree steps** are excluded from 32 points on. `g-6`, `c-2`, `p-3`. Not covered: trees cut along curved sets, limits, three steps.
- **L9. Pay once.** If no gate reads two over-limit wires, gates ≥ N·log2 N − (over-limit wires). `h-8`; `h-0`, `h-1`, `h-4`, `h-5`, `h-6`.
- **L10. Width.** Wires that mix at most b bits need N·log2 N / b gates. `h-5`, `n-1`.
- **L11. No tensor product sits on the count N − 1 + (N/2)·log2 N.** `h-0`, `m-cross`.
- **L12. Old letters.** `e2-2`, `h-2`, `n-2`, the tiny-units note.
- **L13. One form per node** (new; replaces L8). Sibling rows share rectangles only on the half where they agree, and pay single rows, columns or cells elsewhere. Consequences: line 2; a letter that uses every node once needs trees of depth about N/4 (`p-6`); the 13's rule repeated is N^1.5 (`p-4`); two letters are one letter at √N (`p-7`); L7. Hit by `g-1`, `g-6`, `k-cross`, `p-1`, `p-3`, `p-4`, `p-6`, `p-7`, `p-8`, `q-cross`. A second reader checked two of these arguments only (`r-1`). Not covered: overlapping rectangles at 16 points (open between 32 and 45; a record needs 37), trees whose smallest pairs point in different directions, families that are not trees, three or more letters, and subset sums.

The fifth wave's walls all fence one shape, the letter. They say nothing about a circuit that is not a bounded number of letters; the textbook itself is not one letter.

## 6. The next eight experiments

Four are already running in the sixth wave (marked *running*).

1. `corners` (*running*, as a search and as theory): the least number of corners of the subset-sum picture at 16 to 128 points; is 129 reached at 64 points?
2. `onerun` (*running*): can every subset sum be its neighbour plus or minus one run, at 16 and 32 points? Yes or no, with the reason.
3. `second52`: read the two-letter 52; is there a two-letter list of 128 gates at 32 points?
4. `zletter` (*running*): one letter for subset sums on any two trees, not only chains; is anything below 13 at 8 points?
5. `zdz` (*running*): build the transform from two-chain subset sums and put it under the fourth wave's meters.
6. `whichtwo`: all the 4-point problems "from two of the four points make the other two"; is any below 7 gates?
7. `weightladder`: exact cost of every weight-only block for k = 4, 5, 6; does the transform's advantage grow?
8. (silly) `spreadsheet`: the inputs in a 4 × 4 table of running totals; how many boxes does each subset sum need along a path?

## 7. What this says about linear size

Nothing found in five waves gives linear size or moves the exponent, and nothing forbids it: the fifth wave closed the most concrete shape anyone had, the letter, which is quadratic for the transform on the trees examined [argued; a second reader found no error]. It also showed that the small savings of the night belong to a whole class of kernels, while the one program that changes the order uses symmetries only the transform has, and the two kinds of saving have not yet met in one circuit [computed for the first part, guessed for the second]. The one linear-size question that no wall covers is now about subset sums, and its first measurements (5, 13, 30, 80, then 239) sit on or above the N·log N line, with no reason known either way [computed; the reading is guessed].
