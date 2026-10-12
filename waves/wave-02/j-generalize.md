# j-generalize: widen the problem until it is linear, then walk back

10 October 2026, 21:39 to 22:05 EDT. Private. One agent, nothing reviewed, nothing in Lean, no critic.
Marks: [ran] computed tonight (files in `j-generalize/`), [derived] worked by hand here, [read] from tonight's notes or from memory of the literature (said which), [guess].
**Gate count used everywhere: (G)**, a gate is any a·u + b·v, scalings and relabellings free. Nothing here was re-priced in OpenAI's count (O).

Words. n = 2^k points, k address bits. H: the plain ±1 transform, entry (−1)^(number of bits where x and y are both 1). *Layer*: a butterfly (sum and difference) on one address bit over the whole array, n gates. *Textbook*: k layers, k·n gates. Z: the subset-sum matrix, Z[x][S] = 1 when the set of bits S lies inside x. *Level* of S: its number of bits.

## The one picture that came out

Along every axis I widened, the cost is read off a **meter**: a whole number that costs about n gates per unit and reads about k at the transform. Six meters, six different currencies, the same price:

| axis | easy end (linear) | the meter | reading at the transform | linearity is lost exactly when |
|---|---|---|---|---|
| numbers | integers modulo 2^b, b fixed | binary digits b of the answer; 2n gates per digit | k/2 digits already cost k·n | the modulus stops being a fixed power of 2 (the "small number" 2 stops being nilpotent) |
| group | none; best found is half price | levels of a subgroup chain at which representations *split* (levels where they *fuse* are free) | all k levels split: an abelian group is the most expensive group of its order | every level splits, i.e. the group is abelian |
| relabellings | 0 layers: relabel and phase only | rank of one k×k block over the two-element field | k | (it never is linear: this class is closed at exactly k layers) |
| data | rank r across the middle cut, r bounded | r | √n | the rank across a cut is unbounded |
| output | any n/log n outputs forming a subspace: 2n gates | number of cosets wanted | log n cosets | more than a bounded number of those cosets are wanted and they must be served one by one |
| exponent | deformation of the rank-one matrix to order b | order b; 2n per order | order k/2 | the deformation parameter is a real number (2), not an infinitesimal |

A meter that costs n per unit and reads k is n·log n. A linear program has to move one of these meters by more than a bounded amount per n gates. The published saving does that to the first meter of the engine (layers) by a factor (log n)^(−8.76e-4). The ideas below ask where the *other* meters can be cheated, because the floor theorem of `wht38/floor/` speaks only about layers.

## Ideas

### 1. Buy binary digits, not layers [ran]
**Fact.** H = Σ_j (−2)^j · Z_j·Z_j^T, where Z_j keeps only the sets of level j. So modulo 2^b only levels below b matter: H ≡ Σ_{j<b} (−2)^j Z_j Z_j^T. Checked for k = 1..6, every b; the truncated matrix has rank exactly Σ_{j<b} C(k,j) over the rationals (k ≤ 5).
**Program.** "Sums over all sub-cubes fixed by fewer than b bits" (one fold per bit, recursing with b on the folded half and b − 1 on the upper half), scale, and the mirror image. No butterfly anywhere. Replayed on random integers at k = 6, 8, 10: right modulo 2^b for every b, and exactly H·x at b = k + 1.
**Count** (gates per point): b = 1: 1; b = 2: 3; b = 3: 5; b = 4: 7; in general 2b − 1 while b is well below k/2. At k = 96: b = 24 costs 47, b = 48 costs 91.6, b = 72 costs 96.00 = the textbook. **The transform modulo 4 costs 3n. The transform modulo 2^(k/2) already costs the whole k·n: the upper half of the digits is free.**
*Is a digit really worth n?* Smallest test: a quadratic polynomial's 8 values from its 7 coefficients (the b = 3 synthesis at k = 3). The recursion uses 11 gates; exhaustive search over GF(3) and GF(5) with d-0-zeta's `mincirc`: no circuit with 10 [ran]. So at the smallest size the digit price is exact.
*Linearity is lost exactly when* the answer needs about k/2 binary digits, which it does for any data: outputs are of size about √n.
*Next.* 16 points, b = 3: the recursion gives 26 gates for "all 16 values of a quadratic from its 11 coefficients". Anything under 26 would say a digit can cost less than n.

### 2. The cheapest Smith form [derived from the identity of idea 1; search not run]
Z has integer entries and an integer inverse (it is triangular with ones on the diagonal). So H = Z · D · Z^T with D = diag((−2)^level) is a **Smith normal form** of H: two integer-invertible changes of basis around a diagonal of powers of 2 (2^j occurring C(k,j) times). All of the transform's "volume" (its determinant, which is what Morgenstern's n log n bound for bounded coefficients measures) sits in the free diagonal; the paid parts have determinant 1.
A Smith form is far from unique: H = (Z·G) · D · (D^(−1)·G^(−1)·D·Z^T) for every integer-invertible G such that D^(−1)·G^(−1)·D is again integral (entries of G^(−1) from level j down to a lower level i divisible by 2^(j−i)). That is a huge group of choices, and Z is only the one that respects the address bits.
**Construction:** search that orbit for a pair cheaper than Z, Z^T. In (G) the pair Z, Z^T costs k·n/2 + k·n/2 = k·n exactly, the textbook [ran: the b = k + 1 column of idea 1].
*First sign of life:* at 8 points a pair (U, V) with H = U·D·V and fewer than 22 gates in all (22 is the best known for 8 points in (G), from i-cousins); at 16 points fewer than 56.
*Why it might live:* no determinant argument can ever bound the cost of a determinant-1 integer matrix, and the first wave's zeta searches (d-0) fixed U = Z; nobody has moved inside the orbit.

### 3. Fusing is free: route through a non-abelian group, and choose the dictionary [ran for the bridges]
Every group of order 2^k has a chain of subgroups with steps of index 2. For the Fourier transform of such a group along its chain (Baum's method [read, from memory]) each level either *splits* a representation in two (one layer on that part of the data) or *fuses* two into one of twice the dimension (a relabelling, free). So cost = n·(k − average of log2(dimension)), the average weighted by dimension² [derived]. Abelian: nothing fuses, k·n. Extraspecial group of order 2^(2m+1) (half of the data in one representation of dimension 2^m): 1.5m + 1 layers per point against 2m + 1 [derived; table in `play2.out`]. Heisenberg group over a field of 2^e elements: about 2e against 3e. Floor of this method: k/2, since no dimension exceeds √n.
**All 2-groups share a skeleton.** With labels adapted to the chains, "constant on cosets of the j-th subgroup" means the same thing in both groups, so the bridge (our transform) × (the other group's transform)^(−1) is block-diagonal with blocks 1, 1, 2, 4, ..., n/2 [ran: cyclic group of order 8, 16, 32 against Z_2^k, floating point; D4 and Q8 against Z_2^3, exact: blocks 1,1,1,1,4 with the 4-block full].
**Z_4 against Z_2×Z_2** [ran, exact]: bridge = identity on two points and a square root of the swap on the other two. For Z_4^(k/2) against Z_2^k the bridge costs k/4 gates per point: a quarter of the transform, not free.
In every case I priced, (other group's transform) + (bridge) = textbook exactly: the levels the other group fuses for free are the levels the bridge has to pay. **Linearity is lost exactly when** every level splits.
**Construction (what is new):** the bridge depends on a choice nobody has used: the *dictionary*, the bijection between the other group's elements and our addresses. Relabelling is free, and there are n! dictionaries; I only tried the chain-adapted one. Look for a group G and a dictionary σ for which the bridge is cheaper than the levels G saved.
*Room for it* [derived]: the bridge must at least rebuild every row that is not already a character, one gate each. At order 8 (D4, Q8) that is 4 gates and the saving is 4: no room. At order 32 (extraspecial, one representation of dimension 4) the saving is 32 gates and the count only asks for 16.
*Tried by hand at 32 points* [derived, not run]: a linear or affine dictionary changes nothing (it carries characters to characters, so the bridge only has its rows permuted and signed). A dictionary that adds a quadratic function of the other four bits to the central bit keeps 4 non-zeros in every row of the 16×16 block and only moves the small transform from the row index to the column index. And 4 per row is forced: a character is spread over all 32 elements and a matrix entry of the big representation over 8. So the dictionary has to be non-affine in a way that is not a quadratic twist of the centre, and the block will have at least 64 non-zeros whatever it is; the gain can only come from sharing among them.
*First sign of life:* at 32 points, a dictionary between an extraspecial group and Z_2^5 whose bridge costs under 28 gates (32 by layers, 28 with the 7-gate 4-point brick).

### 4. The relabel-and-phase class is closed at exactly k layers, with a one-line potential [ran + derived]
The floor note's hatch (b) is "a relabelling that mixes columns", and it says nobody had looked. Take the class: any linear relabelling of addresses over the two-element field (free), any quadratic ±1/±i phase (free), and as the paid step a butterfly layer on one address bit, hence after relabelling on any direction. Each such program moves shifts and sign patterns around by a 2k×2k matrix over the two-element field; relabellings and phases never change the column space of its upper-right k×k block, and a layer swaps one column into it. So **layers ≥ rank of that block, and the transform has rank k** [derived].
[ran] Whole group searched for k = 2 (720 elements) and k = 3 (1,451,520 elements): the least number of layers equals the rank for every element, and the transform needs 2 and 3.
So hatch (b), with phases, buys nothing as long as layers are whole. **What the potential cannot see** is a layer applied to part of the array (a butterfly on one direction, only on the points of a sub-cube). Haar's transform is exactly that, and it is linear. A program of partial layers with free relabellings and phases between them is no longer described by one 2k×2k matrix.
*Construction:* partial steps on sub-cubes, of both kinds (butterflies, and one-sided steps v ← v + c·u with large c as in Z), with a free linear relabelling between any two.
*First sign of life:* 16 points with fewer than 56 gates, or any rank-like quantity that a partial layer raises by more than (points touched)/n.

### 5. Split the addresses by a tiling that is not a subgroup [derived; not run]
The textbook splits the address space as (subgroup A) + (subgroup V). Generalise to any two *sets* A, V such that every address is a + v in exactly one way (a tiling). Then for every frequency y, output(y) = Σ_a Σ_v (−1)^(a·y)·(−1)^(v·y)·x(a+v): **H is the row-by-row Kronecker product of its two partial matrices H[·,A] and H[·,V]** [derived].
Tried by hand: (i) V = the ball {0, e_1, ..., e_k}, A = the Hamming code (k = 2^r − 1). It collapses to k + 1 transforms of size n/(k+1) followed by an ordinary transform of size k + 1 on each class: the textbook split into r and k − r bits, in the code's coordinates. (ii) If one of the two sets is a subgroup, changing the other only changes free signs. So every tiling with a periodic factor is the textbook.
What is left: tilings in which neither factor is periodic. They do not exist at small sizes: from memory, not checked tonight, the first ones need about 6 address bits, and the stronger kind in which both sets span the whole space needs 10 (Cohen, Litsyn, Vardy, Zémor 1996; Östergård and Vardy 2004). That is exactly why no search at 4, 8 or 16 points can have met them.
*First sign of life:* for one such tiling, the number of distinct rows of H[·,A] and H[·,V] up to sign, compared with |A| and |V| (for subgroups the rows repeat perfectly, and that repetition is the whole textbook saving).

### 6. In "train" coordinates the transform is free; n log n is the price of writing the answer as a table [ran: one count]
Write the data as a chain of small tensors, one per address bit (a tensor train). The transform acts on each bit separately, so it only touches each link: 4n/3 butterflies in all for data of full rank [ran: 1.333 per point at k = 16, 24], and nothing at all if the data are a √n×√n matrix X held between two trivial halves: then "H·x" is the unevaluated product H'·X·H'.
Data of rank r across the middle cut cost about r·n (multiplying out is the cost, the transform is not), so linear for bounded r. **Linearity is lost exactly when** the answer must be expanded: the model wants a table.
*Construction:* look for a representation of the answer that is (a) reachable in O(n) and (b) from which each single output is a combination of O(1) stored numbers. That is a linear program, of depth two after the representation. The train fails (b); summed-area tables (i-fields, idea 1) are another candidate; the two have not been combined.

### 7. Every family with a free transform is an eigenspace, and two of them give only one equation [derived; an idea that died and what it taught]
For any free step g (relabel and scale) with (g·H)² = n, the vectors c with H·c = √n·g^(−1)·c form a family of dimension n/2 on which the transform costs nothing. Take two such families and split x = a + b. Using the two reflections R_i = g_i·H/√n, whose product R_2·R_1 = g_2·g_1^(−1) is a free step m, the split is (1 − m)·a = x − R_2·x. The right-hand side contains the transform. Every pair of free families gives this same single equation.
*What it taught:* a family is only useful if its transform is cheap for a reason other than being an eigenspace. The list of those that I know: spectrum on a subspace of n/log n points (2n gates), support on such a subspace, low rank across a cut (idea 6), degree below b (idea 1, about b gates per point). Their dimensions are all o(n), so a bounded number of them cannot span everything.
*Mutation:* allow log n families and ask that they *share* work. That is the direct-sum question again (the published result's own mechanism), now with a concrete instance: the log2(k) low address bits fold in n·log log n gates in all, and what remains is k separate transforms of size n/k. T(n) = n·log log n + k·T(n/k). Serving those k small arrays together for O(n) would give n·log log n.

### 8. Where the mass sits: weight blocks [ran]
Cut H into blocks by the number of 1 bits of the input address (w) and of the output address (v). For odd k (5, 7) the rank of block (v, w) is exactly C(k, min(v, w, k−v, k−w)) [ran, exact]. So the four corners of this (k+1)×(k+1) picture are of tiny rank (idea 1 is the top-left corner; the two complement relabellings, which are free, give the other three), and the centre is of full rank. The ranks sum to 560 at n = 128, 4.4 times n, growing like √k.
**Linearity is lost exactly in** the central band of about √k levels, where almost all addresses live. A program has to be good only there: for inputs and outputs whose weight is k/2 ± a few √k.
*Construction:* choose coordinates in which the mass is *not* central. Weight is tied to a basis of the address space, and a non-linear relabelling of addresses (free) with another of frequencies (free) changes which blocks are full. Ask for a pair of relabellings under which the matrix has a nested low-rank frame carrying most of the points.
*First sign of life:* at 64 points, an ordering of rows and columns in which the leading i×j blocks have rank well below min(i, j) for most (i, j). In the weight ordering the leading square blocks have full rank.

## Anomalies and pretty facts

1. **Half the digits are free.** H modulo 2^(k/2) costs the same as H. [ran]
2. **Z·D·Z^T is the Smith normal form of H**, and the *same* Z serves the whole family with entries t^(overlap): T_t = Z·diag((t−1)^level)·Z^T for every t [ran: t = −1, 3, −5, 7, k ≤ 6]. Only the diagonal moves along the line; the rank-one point is t = 1 (diagonal = one entry) and the transform is t = −1.
3. In the language of 2×2 matrices this is the factorisation lower-triangular × diagonal × upper-triangular of [[1,1],[1,−1]], raised to the k-th Kronecker power; the free steps are the diagonal and the swap, and by Bruhat's decomposition every other 2×2 matrix needs two triangular factors. [derived]
4. **For even k the middle weight class folds in half**: block ranks at k = 4 are 3 where the formula says 4 and 6; at k = 6, 5, 10, 10 where it says 6, 15, 20 [ran]. Explained in two minutes: complementing an address of weight k/2 gives another of the same weight whose column is ± the same. It is the butterfly along the all-ones direction, seen as a rank drop.
5. In the relabel-and-phase class, least layers = rank of the block for *every* one of the 1,451,520 elements at k = 3, not only for the transform. [ran]
6. An abelian group is the most expensive group of its order for the chain method. [derived]
7. Which outputs are cheap alone [derived by the transposition rule (reversing a circuit changes its gate count by inputs minus outputs); the reversed 14-gate case was then searched: exactly 10 gates over GF(5) and GF(7), so 10 + 4 = 14]. At 8 points there are two kinds of 4-output sets. A plane costs 11 gates (4 folds and the 7-gate 4-point transform); the four independent outputs 0, e1, e2, e3 cost 14. Two planes: 11 + 11 = 22 = the best known whole transform, so nothing is shared and nothing is lost. At 4 points any 2 outputs cost 4 gates (2 per output) and all 4 cost 7 (1.75 per output): the whole transform is the cheapest set of outputs per output.
8. Any 3 point-evaluations of a quadratic polynomial on the cube are independent (in fact any 7), which is what blocks "two shared tables and one gate per output" for the digit program. [derived]
9. Two unrelated ways of gaining binary digits both charge "two per digit": the level recursion of idea 1 (2n gates per digit), and the classical polynomial that sharpens an approximate projection, which multiplies the precision by m at degree 2m − 1. [derived; the second was not run on the transform]

## Not done, and limits

- Everything is in count (G). The digit program uses about k·n/2 scalings by powers of −2 at full depth; (O) charges them.
- "Modulo 2^b" is not a step of OpenAI's machine (its data are exact numbers); idea 1 is a statement about a variant, and about the formal version with an infinitesimal. I did not look for a way to use it on exact data.
- Idea 2's orbit search, idea 3's dictionary search, idea 5 at 10 bits and idea 8's reordering were not run.
- The bridge to cyclic groups was checked in floating point only.
- Baum's method, the existence of non-periodic tilings from 10 bits, and the maximal dimensions for the Heisenberg group are from memory, not read tonight.
- The search "no 10-gate circuit" is exhaustive over GF(3) and GF(5), not over the rationals.

## Files
`waves/wave-02/j-generalize/`: `play1.py`, `play1.out` (digits, Smith form, counts); `play2.py`, `play2.out` (groups, bridges, train count; run on the Linux machine because this Mac has no numpy); `play3.py`, `play3.out` (relabel class for k = 2, 3; weight-block ranks); `rows_quad8.txt` and `rows_indep4_T.txt` (targets for `../d-0-zeta/mincirc`; verdicts in `mincirc.out`; that file comes from a second, sub-second run that I started directly instead of through the light runner, by mistake).
