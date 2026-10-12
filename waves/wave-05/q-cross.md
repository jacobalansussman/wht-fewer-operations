# q-cross: the five waves side by side, four hybrids tried, and what to ask next

> Editor's note (11 October 2026): a critic corrected one step of this report. That what the transform has and its class lacks "is worth at most about N sqrt(log N) gates" does not follow ([r-2](r-2.md)).

11 October 2026, 01:00 to about 01:40 EDT, 40-minute box. Private. One agent; nothing reviewed, nothing in Lean, nothing published.
Marks: [ran] = exact run of mine tonight (files in `q-cross/`, whole numbers and fractions only; searches are annealers, so their
results are upper bounds); [derived] = by hand tonight, checked by nobody; [read] = from tonight's reports; [guess].
Gate count everywhere: **(G)**, a gate is any a*u + b*v, scalings free. Count (O), OpenAI's, is not used in this report.
Read: k-cross in full; the first page of each of the nine wave-4 reports (h-0 to h-8); the head and section list of m-cross (it
landed while I worked); the nine wave-5 results as handed to me; the first sections of WAVE3-NOTE; the wall list of j-cross.
I did not read the wave-5 reports in full, nor the skeptics b-*, c-*, nor the n-* reports.

**No circuit below a known count for the transform, and no growth law below N log N. Nothing here changes the order.**

Words. N = 2^k points; an *address* is k bits. *The transform*: the Walsh-Hadamard matrix H, entries +1 and -1. *Textbook*: N log2 N
gates. *Subset sums*: y_S = sum of x_T over the T inside S; its matrix Z has a 1 where T is inside S and 0 elsewhere. *Yates*: the
usual method for subset sums, (N/2) log2 N gates (4, 12, 32, 80, 192 at 4 to 64 points); with additions only it is optimal, with
subtraction nothing better is known [read: WAVE3-NOTE]. The transform is two calls of subset sums and one free scaling per point
(H = Z D Z^T, g-4), so **subset sums in O(N) gates would be the transform in O(N) gates.** *Kernel*: a 2 x 2 matrix; its *power*
applies it to every address bit; the *class* is all kernels with no zero entry, written [[1,1],[1,tau]]; the transform is tau = -1.
*Merge tree*: start from the N inputs, repeatedly replace two held sums by their sum; its *nodes* are the sets of inputs under each
sum. *Rectangle*: a set of rows times a set of columns with one number on it. *Letter*: the matrix written as a sum of tau
rectangles (node of an output tree) x (node of an input tree); it costs N - 2 + tau gates (k-cross). *Chain*: the most unbalanced
merge tree, x1, x1+x2, x1+x2+x3, ...; its nodes are the beginnings of one ordering.
New words of this report. *Two chains*: a letter whose two trees are both chains, with rectangles (an end of the row order) x
(a beginning of the column order) only. *Corner*: write the matrix as a picture, rows in one order and columns in another; a corner
is a 2 x 2 window of neighbouring cells whose "second difference" a - b - c + d is not zero (for a picture of 0s and 1s: a point where
the outline of the 1-region turns). The number of corners is the number of rectangles of the two-chain letter: gates = N - 2 + corners.

## 0. In ten lines

1. [ran, replayed exactly] **The letter that is quadratic for the transform is small for subset sums.** In two chains the subset-sum
   matrix has at most **5, 13, 30, 80 corners at 4, 8, 16, 32 points** (the transform's best letters have 5, 13, 45, 173 rectangles on
   any trees found tonight, and 7, 23, 72 in two chains). At 4 and 8 points every output is the previous output plus or minus ONE
   run of consecutive inputs. Gates: 7, 19, 44, 110, **above Yates (4, 12, 32, 80): not a record.** And the count per point
   (1.25, 1.6, 1.9, 2.5) rises about as fast as Yates' own (1, 1.5, 2, 2.5): **on this evidence it is N log N, not linear.** Hybrid 1.
2. [derived] What that count needs to matter: fewer than (N/2) log2 N - N corners. If every step changed one run, corners = 2N - 2 and
   subset sums would cost 3N - 4: below Yates from 64 points (188 against 192), and linear. At 16 points the search has 30 = 2N - 2
   corners; at 32 points it has 80 and 2N - 2 would be 62; at 64 points my search is too weak to say anything (261).
   **The measured numbers sit on (N/2) log2 N. What I do not have is a reason**: the wall that makes the transform's letters
   quadratic uses "two rows agree on half of the columns", and the rows of the subset-sum matrix are nested instead.
3. [ran] The same two-chain count for the transform is quadratic: 7, 24, 74, 262, 957 corners at 4 to 64 points in the best
   regular orders, 23 and 72 at 8 and 16 points after a search over both orders and all sign scalings. Weights that are not signs
   (powers of 3 on rows, of 2 on columns) did not lower 23. Hybrid 2.
4. [ran, with p-7's own exact tool] **h-1's second 52-gate circuit is two letters.** p-7's table had 54 as the best two-letter
   count at 16 points and "the gap between two letters and three is 2 gates"; with this circuit it is 0. Hybrid 3.
5. [derived + ran] **tau is a cross-ratio**: per address bit there are four points on a line (two inputs, two outputs) and tau is
   their cross-ratio. p-0's unexplained set {2, 1/2, the two sixth roots of unity} is exactly the set of cross-ratios whose four
   points have a symmetry that mixes inputs with outputs; the transform's extra symmetries all keep or swap the two sides. And
   tau = 2 is the transform with one input and one output exchanged on a bit. Hybrid 4.
6. One wall, hit by six reports of wave 5 and three earlier ones: **one form per node** (section 2, W-A). It is a wall for
   letters of the transform, on every tree shape anyone examined. It is not a wall for subset sums.
7. The class question (k-cross section 4) is answered as far as tonight can: for the full transform no saving is its own
   (p-0, h-6); its own savings sit in the symmetric corner; and the one program that changes the order uses exactly the symmetries
   the class does not have (p-0, h-7, m-cross, the tiny-units note: four reports, one statement). Section 1, C.
8. Status of the old walls: section 2. j-cross's U extended, M sharpened into a door, C pushed one size, S restated for letters;
   k-cross's L7 moved from 64 points to 32, L8 proved in pieces and found to be quadratic, not N log N.
9. Most surprising: line 1 against line 3. Most informative question: **how does the least number of corners of the subset-sum
   matrix grow?** Section 4.
10. Skeptics first: line 4 (it contradicts a count in p-7's table), then the two hand proofs behind W-A, then p-0's census.

## 1. Facts that explain each other

**A. Seven statements (six of wave 5, one of wave 3) are one fact used seven ways.** Two different rows of the transform agree, up to a factor, on
exactly half of the columns; and a node of a tree holds one form. From this: p-1's block law (as many flat blocks as checkerboards),
p-4's conservation law (half of the outer bits are always wrong, total mismatch j 4^j), p-8's cherry invariant (a repaired cherry is
frozen), p-6's partner lemma (partners along a path have total size at least N/2), p-3's count (one useful exception per coset,
3w/4 needed per block), p-7's cell lemma (one wire per cell forces a character), and k-cross 1 D (rectangles have total area at
least N(N-1)/4). Stated once as W-A in section 2. [derived: I matched the statements, I did not re-prove them]

**B. p-0's result was predictable from wave 1, and wave 1 says how much it is worth.** [read: i-wild idea 6, i-fields idea 3, d-7,
i-cross hybrid 2; derived: the match] Every kernel power commutes with permuting the address bits, so ONE change of basis, the same
for every kernel, cuts every member of the class into blocks of size at most k + 1; for the transform the blocks are the matrices
"transform on weight-only data" (p-0's 3 x 3 and 4 x 4 blocks are the first two). All dependence on the kernel is inside the blocks.
i-fields measured the blocks' total dense cost: about 1.6 sqrt(k) per point. So (i) a saving that belongs to the transform alone can
only live in the blocks, which is where p-0 found the only ones (4 against 5, 7 against 8); (ii) everything the transform has
that its class lacks is worth at most about N sqrt(log N) gates; the N log N is in an object with no kernel in it.
The same sqrt(log N) is g-4's floor for subset sums alone and p-5's "exchange fee" between members: one binomial, three reports.

**C. Where the order changes, in four reports.** p-0: address maps (invertible bit matrices on addresses) are symmetries of the
kernel power only at tau = -1. Tiny-units note: without address maps no unit saves a move at block size 3. h-7: every wire of
the published unit is (a vector over the batch) x (a tight wire in one of 946 oblique frames). m-cross line 5: read modulo 2 the unit's
120 x 120 centre is not one merge tree (all 7,140 pairs of classes overlap without nesting), while all 18 count-(G) circuits of the
night are one tree. So the count-(G) records use only what the class has, and the one object that changes the order uses only what
the class lacks. [read; the conjunction is mine] Nobody has a count-(G) circuit at small size that uses an address map to save a gate.

**D. m-cross's formula against p-1's floor.** m-cross: the records at 2, 4, 8 points are N - 1 + (N/2) log2 N (2, 7, 19; next 47,
111). As a letter that is (N/2) log2 N + 1 rectangles: 5, 13, 33, 81. p-1's floor for one letter on dual chains is 4, 11, 32, 108.
So a 47-gate letter at 16 points is not excluded (33 against a floor of 32), and at 32 points a circuit on the formula cannot be one
letter on dual chains (81 against 108). With p-7 (the staircase needs 1, 2, 3, 4, 5 letters at 4 to 64 points) and hybrid 3 below:
the records need more letters as N grows; no bounded number of letters is on the formula. [derived from read numbers]

**E. The same number for a different matrix.** [ran, hybrid 1] The two-chain count for SUBSET SUMS found by search is 5, 13, 30, 80:
at 4 and 8 points exactly m-cross's (N/2) log2 N + 1, at 16 points three below it, at 32 points one below it. I do not know why the formula of the
transform's records shows up as the corner count of the subset-sum matrix. [guess: (N/2) log2 N is the power of 2 in det H and the
gate count of Yates; a regular arrangement with one corner per Yates gate probably exists. The 30 says it is not a floor.]

**F. p-6's square root of 2 is one point of a curve.** [derived] p-6: on one chain used for rows and columns, a second difference
with non-sign weights vanishes only at the weight ratio sqrt 2 - 1, which is not rational. With two different chains the condition
for a block with an odd number of minus signs is (1 +- x)(1 +- y) = 2, x and y the ratios of the two rows and the two columns:
x = 1/3, y = 1/2 is a rational solution, and x = y gives sqrt 2 - 1. A block with an even number of minus signs still needs a ratio
of size 1. [ran, hybrid 2: with such weights allowed the 8-point count stays 23.]

**G. Three "other members" are one member.** [derived; 2 x 2 arithmetic checked in `xratio.py`] p-5's unimodular kernel [[1,1],[1,2]],
p-0's home of the hub-free 7-gate circuit (tau = 2), and p-2's "other reflection" [[1,-1],[0,-1]] (it is the symmetry of the four
points at tau = 2 that fixes one input and one output and exchanges the other two): all are tau = 2. And tau = 2 is what the 2-point
transform becomes when one input and one output change places: from y0 = x0 + x1, y1 = x0 - x1 one gets y0 = 2 x0 - y1, x1 = x0 - y1.

**H. The square root of N.** p-7 (two letters are one letter at sqrt N points), p-2 (the middle table has rank (N - sqrt N)/2; the
shortest relation among the hard points has sqrt N terms), g-7 (after half a transform, sqrt N copies of the sqrt N-point transform)
and g-0 are the equality case of the uncertainty principle seen four times (k-cross 1 H). Nothing new, but it is one cause.

## 2. The walls, each once

**W-A. One form per node (new as a single statement; it is k-cross's L8 grown up).** Lemma, as the reports have it between them:
*write the rescaled transform as a sum of tau rectangles over two merge trees. Two rows agree up to a factor on exactly N/2 columns
and a node offers one form, so a pair of sibling rows can share rectangles only where they agree; where they disagree the letter pays
single rows, single columns or single cells.* Consequences proved or measured: tau >= N^2/512 for any numbers when all cherries of
the input tree have one common direction (p-8, sketch); tau >= 4, 11, 32, 108 on dual chains with any numbers (p-1); the families
found are (N^2 + 14)/6 (p-1, p-8) and about N^1.5 in the ideal count (p-4); matchings need total node size N^2/4, so balanced trees are out from 16
points (p-6); two letters are one letter at sqrt N (p-7); two periodic steps stop at 16 points (p-3). Mine [ran]: in two chains
7, 23, 72 at 4, 8, 16 points and quadratic in the regular orders. **Who hit it: g-1, g-6, k-cross (wave 3); p-1, p-3, p-4, p-6, p-7,
p-8 (wave 5); hybrid 2 here.** Status: hand proofs, none checked by a second reader. NOT covered: overlapping rectangles with large numbers at
16 points (open between 32 and 45), trees whose cherries point in different directions, families that are not trees, three or more
letters. And it says **the growth of one letter is worse than the textbook**, which k-cross did not know: the letters found
lose to the textbook from 32 points (173 rectangles against the textbook's 130), and by p-1's floor no letter on dual chains can
match the best known circuit there (138 gates against 128). Its cause is absent for subset sums (hybrid 1).

**W-B. One class (k-cross L5, j-cross hybrid 4).** Sharpened to its end at 4 points (p-0: 27 shapes for every tau, none the
transform's own, exhaustive modulo four primes) and confirmed on every record at 8 and 16 points (h-6, p-0, including the circuit with
four-bit wires). **Broken in one corner**: weight-only data (4 against 5 gates, 7 against 8) and g-5's 12-gate circuit. Fact B says
that corner is worth at most N sqrt(log N).

**W-C. Conjugation, half and half (i-cross W1, j-cross C, k-cross L1).** p-2: on subset sums the mirror's obstruction is gone and
the count is still 5/4 of Yates or worse, because the cost moves from the helpers into a middle table as dense as subset sums itself.
p-5: every member of determinant 1 is two calls of the orthonormal transform plus N sqrt(log N). Sharpened, not broken.

**W-D. Volume (i-cross W4, j-cross M, k-cross L4).** p-5 turned it into a door: with condition number R the bound is N log N / R, so
linear size needs R of about log N only [derived there, resting on a theorem recalled from memory]. p-8 took something away from
the other side: on chain trees unbounded numbers do NOT help a letter, so "only boundedness forces N log N" is false for letters.
Still open, and still the only wall with a named door.

**W-E. Bounded re-use.** One wall under five names: j-cross U (tight wires; a-2), h-5 (wires entangled on at most b bits need
N log2 N / b gates), h-8 (no gate reads two over-limit wires implies gates + over-limit wires >= N log2 N), h-1 (a window of w
bits reaches 1/2 + 2^(-w) at best), p-3 and p-7 (two steps, two letters). Each says: a program whose wires are re-used to bounded
depth, in whatever sense, is N log N. Linear size needs wires entangled on about log N bits (h-5), gates that read two over-limit
wires (h-8), and a number of letters that grows (fact D).

**The older walls, status.** j-cross U: extended (h-5, h-8), not broken. j-cross M: W-D. j-cross C: two commuting or periodic steps
now excluded from 32 points on, not 64 (p-3; the last rank step by hand). j-cross S: restated for letters by p-7's cell lemma; not
broken. k-cross L2 (copies do not share): h-2 closed 4 arrays at block size 5 and showed the method goes silent from 5 arrays on;
no change in wave 5. k-cross L6 (the saving is an extra value): p-5 adds that at 4 points for [[1,1],[1,2]] it needs BOTH an extra
value and a coefficient 2. k-cross L7: moved (p-3). k-cross L8: now W-A.

## 3. Four hybrids, each tried

### Hybrid 1. Corners of subset sums (k-cross's rectangle count x p-6's chain x g-4's "the transform is two subset sums" x g-3's Potts shape)

Idea. Every report that counted rectangles counted them for the transform, where W-A makes them quadratic. p-6's partner lemma left
one tree shape standing, the chain, and g-3's Potts matrix (the only linear-size letter of the night) is on a chain. Nobody counted
rectangles for the OTHER matrix that would give the transform, subset sums, whose rows are nested and not half-agreeing.
In two chains a letter is easy to state. Put the outputs in one order and the inputs in another. Then
(matrix in these orders) = (running sums over the outputs, from the end) x M x (running sums over the inputs), where M is the table
of second differences. The program: N - 1 running sums F_1, F_2, ... of the inputs; then output after output,
y_a = y_(a+1) + (the non-zeros of row a of M, each times one F). Gates = N - 2 + (non-zeros of M). For a matrix of 0s and 1s the
non-zeros of M are the corners of the picture, and a row of M with two non-zeros says "this output is the next one plus or minus one
run of consecutive inputs", the trick of a running total and one subtraction.

Tried [ran: `cat3.py` on the Linux machine, an annealer over both orders, random starts; every result replayed on all basis vectors
with whole numbers by `zreplay.py`; outputs `cat3_4.out` to `cat3_32.out`]:

| points | corners found | gates | Yates | (N/2) log2 N + 1 | 2N - 2 | rows of M with at most 2 non-zeros |
|---|---|---|---|---|---|---|
| 4 | 5 | 7 | 4 | 5 | 6 | 4 of 4 |
| 8 | 13 | 19 | 12 | 13 | 14 | 8 of 8 |
| 16 | 30 | 44 | 32 | 33 | 30 | 13 of 16 |
| 32 | 80 (five runs: 80, 81, 84, 85, 85) | 110 | 80 | 81 | 62 | 21 of 32 |
| 64 | 261 (one run, from the Gray start; the search is too weak here) | 323 | 192 | 193 | 126 | 22 of 64 |

The regular arrangement (both orders a reflected Gray code) is far worse: 8, 22, 64, 190, 568, 1702 corners at 4 to 128 points,
tripling [ran, `cat3g.py`]; the search leaves it at once. The orders it finds are not Gray codes (at 16 points the output order
has steps that change two and four address bits).
What it is not: a record. Yates is cheaper at every size run, because the letter spends N - 2 gates on its two chains.
Reading: corners per point 1.25, 1.63, 1.88, 2.50 at 4 to 32 points against (1/2) log2 N + 1/N = 1.25, 1.63, 2.06, 2.53. The
search is on the Yates line and a little under it at 16 and 32 points; nothing in these numbers points to a bounded count per point.
What it would take [derived]: corners below (N/2) log2 N - N. If every step changed one run (true at 4 and 8 points), corners =
2N - 2, gates = 3N - 4: 188 at 64 points against Yates' 192, and linear; through H = Z D Z^T the transform at about 6N, below
(3/4) N log2 N from 512 points. At 16 points the search is at 2N - 2 by another route (three rows with 3 non-zeros, five with 1).
At 32 points it is 18 above 2N - 2, and only 21 of the 32 steps change one run: the pattern of 4 and 8 points does not continue in what the search finds.
A structure fact [derived]: if every output step changes exactly one run of inputs, each row of M is a +1 and a -1 at the two ends
of its run, so M is the incidence matrix of a graph on the N + 1 gaps between consecutive inputs (the two ends included); M is
invertible, so that graph is a tree, and subset sums = (running sums) x (differences along a tree) x (running sums).
Where it stops: four sizes, an annealer, upper bounds. The 80 at 32 points is the value a regular construction with one corner
per Yates gate would give, less one; at 64 points the annealer does not even reach that value (261 against 193), so beyond 32 points
my tool says nothing either way. The only lower bounds I have are N (rank) and, if
g-4's floor for bounded coefficients is right, N (0.28 sqrt(k) - 1), which is below N for every size one could run. Rectangles
that use single inputs or single outputs (allowed in a letter on chains) were not used; they can only lower the count.
The longer runs are `cat3g_32.out` (three random starts, 1.5 million moves each: 85, 84, 80) and `cat3g_64.out` (one Gray start,
2.5 million moves: 261), both replayed exactly.

### Hybrid 2. The same count for the transform (p-6's chain x p-1's block law x p-4's "try unbalanced trees")

Idea. p-6 showed matchings need chains; p-4 and p-6 both left "letters on chains" as the open shape; p-6 counted only a lower bound
((N/2) log2 N cells for bit-linear orders with sign scalings). Count the real thing.
Tried [ran: `cat1.py` local, `cat2.py` on the Linux machine, `cat4.py` local; exact integers; `cat2` replays L^T M L = the matrix]:
- Regular orders (rows in Gray code, columns in Gray code with the bits reversed), sign scalings optimised: 7, 24, 74, 262, 957
  corners at 4 to 64 points. The cells with value 2 number 18, 47, 103, 243 at 8 to 64 points, somewhat above p-6's lower
  bound (N/2) log2 N = 12, 32, 80, 192; the rest are
  cells with value 4, p-1's checkerboards, and they are the quadratic part (5, 26, 158, 713).
- Search over both orders and all sign scalings: 23 at 8 points (six runs), 72 at 16 points (three runs). The best letters on
  balanced trees have 13 and 45. So the chain is the worst shape tried, not the surviving one.
- Weights 3^i on rows and 2^j on columns, i, j from -2 to 2 (fact F): 23 again at 8 points in three runs, and the best solution
  found uses no weight.
Why [derived, rough]: a 2 x 2 window is free only if its two rows are equal or its two columns are equal there. "Rows equal"
spreads sideways and downwards until a corner stops it, and so does "columns equal". The picture is cut into regions of the two
kinds; inside a region all rows (or all columns) are equal, so no rectangle inside it has area above N (a rank-one block of the
transform has area at most N); the walls between regions are corners. Regions with no inscribed rectangle above N have total
wall length of order N^1.5 at least. This is W-A on the last tree shape, with the same N^1.5 that p-4 found on balanced trees.
Limits: "quadrant" rectangles only (single cells and single lines were not allowed as separate rectangles, so p-8's 14 at 8 points
for general chains is not contradicted by my 23); annealing; the N^1.5 argument is five lines and unchecked.

### Hybrid 3. The second 52 under p-7's meter (h-1's circuit x p-7's letter counter x p-0's "the only record with four-bit wires")

Idea. p-7 counted letters for e2-0's family (1, 2, 3, 4, 5) and proved by hand that e2-0's 52 is not two letters; its two-letter
column has 54 at 16 points. h-1 found a second 52 of another shape, and p-0 found it is the only record circuit with wires
entangled on all four address bits. Nobody put it under p-7's meter.
Tried [ran: `let52b.py`, which imports `p-7-twoletters/letters.py` unchanged; output `let52b.out`]:
- `h-1-staircase3/slp16_52_from54.txt`: replay exact; one letter: no assignment, search exhaustive (1,983 nodes);
  **two letters: found.** Letter 1 has 30 gates (14 up, 16 down), letter 2 has 22 gates (10 up, 12 down); 19 wires leave letter 1.
- `h-8-provethewrongthi/h8_21_three_hubs.txt` (8 points, 21 gates): two letters, not one (exhaustive, 91 nodes).
So the two-letter count at 16 points is at most 52, not 54, and at 16 points two letters do as well as three. p-7's sentence "the
honest gap between two letters and three is 2 gates" is wrong by those 2 gates, and its law "two letters are decided by the
one-letter count at sqrt N" (which gives 54 from the 19) does not describe this circuit: its middle is 19 wide, three more than N.
What it does not change: p-7's cell lemma (it is about perpendicular subgroup chains with one wire per cell) and the growth
argument beyond 16 points, which I did not redo. Whether the second 52 has cells with several wires, the freedom the lemma leaves,
is the first thing to read off it.

### Hybrid 4. tau is a cross-ratio (p-0's unexplained set x h-8's "a gate is three wires on a line" x p-2's other reflection x p-5's K)

Idea. In count (G) a wire matters only up to a factor, so a wire is a point of a projective space and a gate is three points on a
line (h-8). On one address bit the forms are a projective line carrying four points: the inputs e0, e1 and the outputs r0, r1.
Four points on a line have one invariant, the cross-ratio, and with inputs at 0 and infinity and r0 at 1 it is tau (or 1/tau).
p-0 saw an extra circuit shape exactly at tau = 2, 1/2 and the two sixth roots of unity, noticed these are short orbits of
tau -> 1/tau and tau -> 1 - tau, and wrote "tau -> 1 - tau is not a symmetry of the problem, so I do not know why its orbits show".
Tried [ran: `xratio.py`, exact fractions]: for each tau, all maps of the line that permute the four points.
- Generic tau (3, -2, 5/7, 1/3): 4 symmetries, all keep or swap {inputs} and {outputs}.
- tau = -1: 8 symmetries, **all keep or swap the two sides.**
- tau = 2 and tau = 1/2: 8 symmetries, **4 of which mix the sides**; at tau = 2 one of them fixes e0 and r1 and exchanges e1 with r0,
  with matrix [[-1,1],[0,1]], p-2's "other reflection" up to sign.
- [derived, not run: the sixth roots need a quadratic field] there the four points have 12 symmetries, with three-cycles that
  must mix the sides.
So the six values of the cross-ratio are the six ways of naming which two of the four points are "inputs", and p-0's set is
exactly: the cross-ratios with a symmetry that does not respect the split into inputs and outputs. The transform is the third
special value, and its extra symmetries do respect the split, which is why it is absent from p-0's list. This explains the SET.
It does not yet explain the circuit: I checked by hand that the mixing symmetry at tau = 2, applied to one or both bits, does not
carry p-0's hub-free circuit onto itself (it does swap its two product helpers, e1 x r0 and r0 x e1). [derived, small]
Use: fact G; and a new family of small exact problems (section 6, experiment 6).

## 4. The most surprising thing, and the question that would tell the most

**Surprise of this wave.** The letter, the object behind the 19, has no future for the transform: five reports independently
found its growth quadratic or N^1.5, worse than the textbook from 32 points, and for one cause (W-A). The surprise inside
the surprise, from hybrid 1: the cause is special to the transform. For subset sums the same count is 30 and 80 where the transform
has 45 and 173 (72 at 16 points in the same shape), and at 4 and 8 points every output is its neighbour plus or minus one run of
inputs. It is N log N there too, as far as I can see, but it is the textbook's N log N and not a quadratic.

**Question. How does the least number of corners of the subset-sum matrix grow with N, over all pairs of orders?**
Why it tells the most. (i) It is about linear size directly: bounded corners per point is subset sums in O(N) and the transform
in O(N); below (1/2) log2 N - 1 per point is already the first subset-sum circuit below Yates, a result for another field.
(ii) None of tonight's walls covers it: W-A needs half-agreeing rows; W-B is about the transform's class and subset sums are its
degenerate member; W-D gives N sqrt(log N) at most; W-E is about tight wires, and here the wires are running sums, which are
as far from tight as wires get (a running sum over half of the inputs is entangled on every bit, which is what h-5 says linear
size needs). (iii) It is finite and exact at each size, and a "no" would be the first lower bound of the night for subset sums
with subtraction, even if only in a model.
Experiment. (a) Exact minimum at 16 points: is 30 least, and is 29 = 2N - 3 (the pattern of 5 and 13) possible? An integer
programme or a SAT search over the two orders; the tree fact of hybrid 1 cuts the search when every row has at most two non-zeros.
(b) 32 and 64 points with a real annealer (C, incremental update of the 4 cells a swap touches, moves that reverse a segment),
seeded with the 16-point solution doubled in each of the three natural ways. Targets: 49 at 32 points, **129 at 64 points**; at or
below these the circuit beats Yates. Tonight: 80 and 261. The honest prior is that the answer is (N/2) log2 N minus a little;
the experiment is worth an hour because its "why" is not known and a proof of it would be a lower bound for subset sums. (c) Allow single inputs and single outputs as nodes. (d) The reason, if it fails: find which
outputs need many runs in every order. Tools: `q-cross/cat3.py`, `cat3g.py`, `zreplay.py`.

## 5. Three objects for a skeptic, in this order

1. **Hybrid 3: h-1's second 52 is two letters (it contradicts a count in p-7's table: 54 as the best two-letter list at 16
   points).** Exactly: under the definition coded in `p-7-twoletters/letters.py` (a letter = a nested family of merges, then a
   forest of down gates; wires of earlier letters pass through free), the gate list `h-1-staircase3/slp16_52_from54.txt` has an
   assignment with two letters and none with one. Attack: is the coded definition the one p-7's cell lemma is about; does the
   free pass-through hide the missing letter (19 wires leave letter 1); print the assignment and check it by hand.
2. **The two hand proofs that make W-A a wall.** p-8: tau >= N^2/512 for any numbers when all cherries have one direction
   ("a sketch, unreviewed"). p-1: tau >= 4, 11, 32, 108 for one letter on dual chains with any numbers ("checked only by
   consistency"; `p-1-letter16/lb.py`, `lb16.py`). They close the one-letter door at 32 points and beyond, and p-7's and my
   conclusions lean on them. Attack p-1's floor at 16 points first: it says 32, the best letter is 45, a record needs 37.
3. **p-0's census and its corner.** Exactly: at 4 points, 27 shapes of 7-gate circuit common to every tau, one more only at
   tau = 2, 1/2 and the sixth roots, none for the transform alone (exhaustive modulo 7, 11, 13, 17; two circuits replayed exactly);
   and on weight-only data the transform costs 4 and 7 gates where every other tau costs 5 and 8 (the 4 and the 7 exact, the "no
   4" and "no 7" for other tau modulo primes only). The whole class question rests on these. Attack "none modulo p is not none".
Not on the list because it claims no record: hybrid 1. Its numbers are replayed circuits and upper bounds; what needs an attack
there is only my sentence "no wall of tonight covers it".

## 6. Eight experiments for the next wave

Deepen what is alive:

1. **corners** (deepens hybrid 1). Section 4, parts (a) and (b). Inputs: `q-cross/cat3.py`, `cat3g.py`, `zreplay.py`,
   `cat3_16.out` (the 30). Output: the exact minimum at 16 points; best counts at 32, 64, 128 with the orders; corners per point at
   each size; one line saying whether 129 at 64 points was reached. Count (G); every circuit replayed with `zreplay.py`.
2. **weightladder** (deepens p-0, with fact B). Exact minima of ALL the blocks, not only the first: for k = 4, 5, 6 the blocks of
   size k + 1, k - 1, k - 3, ... for the transform and for tau = 2, with mincirc; then the sum over blocks with their
   multiplicities C(k,j) - C(k,j-1). That sum is the price of everything that depends on the kernel. Is the transform's
   advantage 1 gate per block, or does it grow? Inputs: `p-0-classtest/weightonly_exact.py`, `symk.sh`, `d-0-zeta/mincirc`.
3. **second52** (deepens hybrid 3 and p-7). Read `let52b.out`'s assignment: the two pairs of trees, the 19 middle wires, the
   cells that hold several wires. Then ask p-7's question again at 32 points: is there a two-letter list at 128 (e2-0 needs four
   letters, p-7's best two-letter list is 132)? Seed h-1's annealer with the second 52 tensored with a 2-point step.
Nobody has tried:

4. **zletter** (subset sums on any two trees). p-8's exact tool `p-8-fibonacci/dw.c` computes the least number of rectangles for
   one input tree and centre; change the target from H to Z (and to Z with free positive scalings) and run all 149 input trees at
   8 points: is anything below 13, and which tree shape wins when half-agreement is absent? Then the best shapes at 16 points
   against my 30.
5. **onerun** (a yes-or-no question with a proof at the end of it). Is there, for k = 5, an order of the 32 inputs and a path
   through the 32 outputs such that each output differs from the next by ONE run of consecutive inputs? (True at k = 2, 3; at
   k = 4 the search has 13 of 16 steps, at k = 5 it has 21 of 32.) By the tree fact this is: an ordered tree on 33 gaps whose partial sums are the 32
   down-sets. SAT or exhaustive with the tree constraint. A "no" with a reason is a lemma about subset sums with subtraction;
   a "yes" at k = 5 and 6 is a circuit of 3N - 4 gates, below Yates at 64 points.
6. **whichtwo** (from hybrid 4). On each address bit there are four points; the problem chooses two as inputs. At 4 points
   (two bits) compute with mincirc the exact minimum of all the problems "from products of two of the four points, make the
   products of the other two", for the four points of the transform (the three choices are tau = -1, 2, 1/2) and for the
   equianharmonic four (sixth roots). Then mixed choices: one bit read as tau = -1, the other as tau = 2. Is any below 7?
   And at 8 points, does p-0's hub-free circuit for tau = 2 combine with itself better than the brick (p-0's own mutation 5)?

One hybrid:

7. **zdz** (hybrid 1 x g-4's H = Z D Z^T x m-cross's meter). Build the transform at 16 and 64 points as (two-chain subset sums)
   x (free scalings) x (its transpose) from experiment 1's circuits, replay exactly, and put it under m-cross's meter modulo 2
   and h-0's meter: running sums are neither tight nor "one merge tree" wires, so this is the first count-(G) circuit for the
   transform that should break m-cross's three hypotheses. Count: 2 (N - 2 + corners). It needs corners below (3/8) N log2 N - N
   to pass the 3/4 family; report what the meters say even though it will not.

One that sounds silly:

8. **the spreadsheet trick.** Put the 16 inputs in a 4 x 4 table and keep the table of running totals (the "summed-area table"
   every graphics programmer uses: 2N gates, then any box is four look-ups). How many boxes does each subset sum need, and how
   many along a path of outputs where each differs from the last by a few boxes? Then 8 x 8 for 64 inputs, and tables with three
   and four sides. It sounds like school arithmetic; it is hybrid 1 with one more dimension, and i-fields idea 1 said the cube
   is "the worst shape for prefix sums" without counting differences along a path.

## 7. Criticism, last

- Hybrid 1 is four sizes and an annealer. "5, 13, 30, 80" are upper bounds, replayed exactly; they prove nothing about growth,
  and all four are within three of (N/2) log2 N + 1, the count of a method that would never beat Yates. While the runs were going I
  believed for some minutes that the count might be 2N - 2 at every size; the 32-point runs (80, not 62) took that away, and the
  64-point run is too weak to count. Line 2 of section 0 and section 4 are written after that correction.
  My sentence "no wall of tonight covers it" is an absence of argument, not an argument. I did not search the literature on
  subset sums in the group model beyond what WAVE3-NOTE quotes; a known lower bound for this shape (running sums, then few
  differences) may exist under the name of range-sum or dominance-sum structures.
- The arithmetic "3N - 4 beats Yates at 64 points" supposes every step changes one run, which the search does not have at 16
  points (it has 30 by a mixture of rows with 1, 2 and 3 non-zeros) and is 18 away from at 32.
- Hybrid 2's N^1.5 is a rough argument; the measured numbers (23, 72) are upper bounds in a restricted model (quadrants only).
- Hybrid 3 rests on p-7's program doing what its header says. I did not read its search code, only its report function.
- Hybrid 4 explains a set of four numbers with a classification that has exactly those numbers in it; that is cheap. Its test
  on the circuit failed.
- Section 2's W-A is my bundling of seven reports' own summaries; I did not check that their hypotheses match (trees, scalings,
  whether overlap is allowed differ from report to report).
- I read wave 5 through its result summaries, and wave 4 through first pages.

Files: `waves/wave-05/q-cross/` : cat1.py (transform, regular orders, local);
cat2.py, cat2_8.out, cat2_16.out (transform, search over orders; Linux machine, copied back); cat3.py, cat3_4.out, cat3_8.out,
cat3_16.out, cat3_32.out (subset sums, search over orders; Linux machine, copied back); cat3g.py (the same with a Gray start and
the longer runs); zreplay.py (exact replay of a subset-sum circuit from an output file); cat4.py, cat4_signs.out, cat4_weights.out
(transform at 8 points, weights 3^i and 2^j); let52b.py, let52b.out (letters of the second 52 and of the three-hub 21);
xratio.py (symmetries of the four points).
