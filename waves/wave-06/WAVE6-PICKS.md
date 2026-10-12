# WAVE6-PICKS: ten briefs for one-hour developers

11 October 2026, about 01:25 to 01:45 EDT. Private. One curator (label s-pick); nothing reviewed, nothing in Lean, nothing published.
Marks: [read] = from tonight's reports; [ran] = exact run of mine tonight (two small programs in `s-pick/`, whole numbers);
[derived] = worked out by me while writing, checked by nobody; [guess].
Read in full: q-cross.md, m-cross.md. Read in part: the headers of the tools named below, the outputs `q-cross/zreplay.out`,
`q-cross/cat3_*.out`, `m-cross/meter2.out`, `m-cross/dups.out`. Not read: the wave-4 and wave-5 reports themselves, the skeptics
(n-*, r-*; the wave-4 and wave-5 notes had not landed).
Not ranked by odds. Constants are not the aim: every brief asks for a GROWTH LAW in N.
Gate count: **(G)** everywhere (a gate is any a*u + b*v, scalings free), unless a line says (O) (OpenAI's count).

What I ran myself, so that the definitions below are tested and not only copied:
- [ran, exhaustive, `s-pick/c4.py`] At 4 points the least number of corners of the subset-sum picture is **5** over all 24 x 24
  pairs of orders, and multiplying inputs and outputs by -1 in every possible way does not lower it.
- [ran, `s-pick/c2.py`, `s-pick/c2.out`] The same count **modulo 2** (only odd second differences counted) is **4** at 4 points
  (exhaustive), **12** at 8 points (a small annealer), 30 at 16 points (a very weak run that says nothing). See brief 10.

---

## Words used by all the briefs (read once)

**The objects.** N = 2^k points. An *address* is k bits, read as a subset of {1..k}. *The transform* H: entry (y, x) is
(-1)^(number of common ones). *Subset sums* Z: y_S = sum of x_T over the T inside S; entry (S, T) is 1 if T is inside S, else 0.
*Textbook*: N log2 N gates for H. *Yates*: the usual method for Z, (N/2) log2 N gates (4, 12, 32, 80, 192 at 4 to 64 points).
*Why Z matters* [read: g-4; derived again here]: (-1)^m = (1 - 2)^m = sum over j of C(m, j) (-2)^j, so
H = Z D Z^T with D the diagonal matrix (-2)^(size of J); and Z^T is Z with every address complemented [derived:
"S inside T" is "complement of T inside complement of S"]. Scalings are free in count (G). So **the transform costs at most two
subset-sum circuits; subset sums in O(N) gates is the transform in O(N) gates.**

**Words of q-cross (briefs 1 to 5 and 10).**
- *Merge tree*: start from N values, repeatedly replace two held sums by their sum (N - 1 gates). Its *nodes* are the sets under
  each sum. *Chain*: the most unbalanced merge tree, x1, x1+x2, x1+x2+x3, ...; its nodes are the beginnings of one ordering.
- *Rectangle*: (a set of outputs) x (a set of inputs) with one number on it. *Letter*: the matrix written as a sum of rectangles
  whose row sets are nodes of one merge tree on the outputs and whose column sets are nodes of one merge tree on the inputs.
  A letter with tau rectangles is a circuit of N - 2 + tau gates [read: k-cross, through q-cross].
- *Picture*: the matrix drawn with the outputs (rows) in one chosen order and the inputs (columns) in another. In the code
  (`q-cross/cat3.py`, `zreplay.py`) `rows[a]` is the address of the a-th output, `cols[b]` the address of the b-th input,
  A[a][b] = Z[rows[a]][cols[b]], and one extra row and one extra column of zeros are added AFTER the last row and column.
- *Second difference*: M[a][b] = A[a][b] - A[a+1][b] - A[a][b+1] + A[a+1][b+1], for a, b from 0 to N - 1.
- *Corner*: a pair (a, b) with M[a][b] not zero. In a picture of 0s and 1s it is a point where the outline of the 1-region turns.
  Windows that would reach above the first row or left of the first column are not counted; windows that reach into the added
  zeros are. *The corner count* of a pair of orders is the number of non-zeros of M.
- *The two-chain program* (it is what `zreplay.py` replays): F_b = x_(cols[0]) + ... + x_(cols[b]) (running sums, N - 1 gates);
  then, from the last output upwards, y_a = y_(a+1) + sum over b of M[a][b] F_b (one gate per non-zero, less one for the very
  first). Gates = N - 2 + corners. It is the letter on two chains.
- *Run*: a set of inputs that are consecutive in the input order. *Prefix*: a run that starts at the first input (it is one F_b).
  *One-run step*: an output step whose row of M has at most two non-zeros, +1 and -1 at the two ends of a run: "this output is
  the next output plus or minus one run". A prefix step has ONE non-zero.
- *Plain / signed*: plain = the picture of Z as it is; signed = every input and every output may first be multiplied by -1.
  The best pictures found at 4, 8, 16, 32 points are plain (all signs equal in the output files) [read: the .out files].
- *The tree fact* [read: q-cross hybrid 1]: call the N + 1 places before, between and after the inputs *gaps*. If every step is a
  one-run step, each row of M is an edge between two gaps, and since M is invertible the N edges form a tree on the N + 1 gaps.
- [derived, mine; it matches the runs at 4 and 8 points] In that case **corners = 2N - d, d = the number of prefix steps**
  (edges at the leftmost gap): 5 = 8 - 3 at 4 points, 13 = 16 - 3 at 8 points (step sizes 1,1,2,1 and 1,1,2,2,2,1,2,2).
- [derived, mine] In the plain picture a one-run step joins two outputs S, S' with one INSIDE the other, and the run is the
  set of inputs inside the larger and not inside the smaller.
- [derived, mine; use it to write fast searches] **With the input order fixed, the corner count is a sum over neighbouring
  outputs**: the row a of M depends only on rows a and a+1 of the picture. So the best output order for a fixed input order is a
  shortest path through N cities (a travelling-salesman path) with distance w(S, S') = number of places where the difference of
  the two rows changes value along the input order; and the same holds with the roles exchanged. Reversing a segment of an order
  changes only the two rows (or columns) of M at the segment's ends.

**Words of m-cross (briefs 5 to 9).**
- *Wire*: a value the program holds, written as a vector over the N inputs. *Tight*: (non-zeros of the wire in the inputs) x
  (non-zeros when written in the outputs) = N. *Over the limit*: that product is larger than N.
- *Primitive form* of a wire: the wire rescaled (free in count G) so that its entries have odd denominators and are not all even.
  *Class* of a wire: its primitive form modulo 2, a 0/1 vector; for a wire with entries 0, +1, -1 it is the set of its non-zeros.
- *Survivor*: a gate whose result has a class that no earlier wire has. *Dead gate*: any other gate. So gates = survivors + dead.
- *Kinds of gate*, from the classes of the parents u, v and of the result w. **J** (join): three different classes. **S** (shift):
  w has the class of a parent, w = u + (even number) * v. **Q gate** (difference quotient): the two parents have ONE class and
  w another, w = (u - c v) / 2^m: the gate subtracts two wires that are equal modulo 2 and divides by a power of 2. **E**: all
  three classes equal. *Order* of a dead gate: the largest m with w = (odd number) * (an earlier wire) modulo 2^m.
- *One merge tree modulo 2*: the classes of all wires of the circuit number exactly 2N - 1 and any two are nested or disjoint;
  then exactly N - 1 gates are survivors (the merges of that tree). [read: true of all 18 circuits m-cross could parse.]
- *The floor (a guess of m-cross)*: dead gates >= (N/2) log2 N for a circuit that is one merge tree modulo 2 with no Q gate and
  all dead gates of order 1. *Excess*: e = gates - (N - 1) - (N/2) log2 N. The *brick* (4 points, 7 gates,
  `h-6-classhub/brick_m1.txt`) and *the 19* (8 points, `g-1-tightwires/h8_19gates.txt`) have e = 0. The *staircase*
  (`e2-0-pieces/slp_4.txt` to `slp_64.txt`: 7, 20, 52, 128, 304 gates) has e = (N/4)(k - 3) + 1 from 8 points on.
- *Hub*: a wire with all N entries +1 or -1 that is not an output (the brick's `hub3`). *Partner*: the second parent v of a shift
  w = u + 2c v. *Agreement rule* [read: h-6, lines 159 to 199; my wording]: a shift of a wire u with entries +1, -1 by a partner v
  gives entries +1, -1 again only if v equals u (up to one factor) on the support of v.
- *The published unit*: the small program the published exponent is built from. h-7 describes it as 120 sources, 120 targets and
  783 helper slots; its *scatter matrix* is 120 x 120 with 1 on the diagonal and +1/2 or -1/2 on 56 neighbours (the 120 lines of
  the E8 root system) [read: h-7 through m-cross; `m-cross/e8shadow.py` rebuilds it].
- *Address map*: relabelling the addresses by an invertible k x k matrix of bits. It is a symmetry of H and of no other member
  of H's class [read: p-0 through q-cross], and by the tiny-units note every saving in the engine's small game needs one.

**Machines and formats.** Small exact runs: `python3 -B (not in this repository) wht35/bin/light.py <label>
<seconds> <command>` (no numpy there). Heavier runs: the rented Linux machine (numpy, gcc), files under
`(the Linux machine's working folder)/<label>/`, two jobs at most, 20 minutes each, nice 19. A gate-list file is one gate per line,
`name = a * u + b * v`, inputs `x0`, `x1`, ... (see `h-6-classhub/brick_m1.txt`); `m-cross/meter2.py` parses that.

---

## 1. corners-search: the least number of corners of the subset-sum picture, 16 to 128 points

**The idea.** Draw the subset-sum matrix with the outputs in one order and the inputs in another, and count the corners of the
picture. The two-chain program turns a picture with c corners into a circuit of N - 2 + c gates. If the best pictures have a
bounded number of corners per point, subset sums cost O(N) gates and so does the transform. Tonight's numbers are 5, 13, 30, 80
at 4 to 32 points from a slow annealer written in Python, and nothing usable at 64 points. Nobody knows the law.

**Definitions used**: picture, second difference, corner, two-chain program, run, prefix, plain / signed (all above).

**Start from.** `q-cross/cat3.py` (the annealer: swaps, segment reversals, sign flips; it recomputes the whole of M at every
move, which is why it dies at 64 points); `q-cross/cat3g.py` (the same with a Gray-code start and a temperature argument);
`q-cross/zreplay.py` (exact replay of a result file on all N basis vectors: every count you report must pass it);
`q-cross/cat3_16.out` (the 30: rows 13 12 4 5 7 1 3 11 9 8 10 14 6 2 0 15, columns 2 3 7 6 4 14 12 8 10 11 9 1 5 13 15 0),
`cat3_32.out`, `cat3g_32.out` (80 to 85), `cat3g_64.out` (261); `s-pick/c4.py` (the exhaustive 4-point count, 30 lines).

**First experiment.**
(a) A real annealer in C. Three facts make every move cheap [derived, mine, verify on the 16-point file first]: the count is a
sum over neighbouring rows and also a sum over neighbouring columns; a swap touches four rows (or columns) of M; a segment
reversal touches two. Keep each row as a bit word in column order and each column as a bit word in row order; the cost of a pair
of neighbours is then a few shifts, exclusive-ors and bit counts. Moves: swap, reverse a segment, move a segment elsewhere
(the three classical moves for a travelling-salesman path), alternately on rows and on columns.
(b) Because the problem is two interlocked shortest-path problems, also try: fix the input order, solve the output order to
optimality (at 16 points exactly, by the standard dynamic programme over subsets of cities, 2^16 x 16 states; at 32 to 128 points
with a strong path heuristic), then fix the outputs and solve the inputs, and repeat until nothing moves.
(c) Seeds. Double the 16-point solution in each natural way: Z at 2N points is the block matrix [[Z, 0], [Z, Z]], so an order of
2N addresses can be (first copy, then second copy), (first copy, then second copy reversed), or (each address followed by its
twin); take all nine pairs of choices for rows and columns, print their corner counts before any search, then anneal each.
(d) The exact minimum at 16 points: is it 29 = 2N - 3 (the pattern of 5 and 13) or 30? One route: by the formula corners =
2N - d, a 29 needs all sixteen steps to be one-run steps with three prefix steps, which is brief 3's yes-or-no question at
k = 4 with one more condition; any picture with a step of three or more non-zeros needs more prefix steps elsewhere. Another:
exhaust the input orders up to the symmetries (permuting the k bits acts on rows and columns together; complementing all
addresses and exchanging the two orders is a symmetry too [derived, check]) and solve each output order exactly.

**Targets.** 32 points: at most 62 is 2N - 2; at most 49 beats Yates. 64 points: at most 126 is 2N - 2; **at most 129 beats
Yates.** 128 points: 2N - 2 is 254; at most 321 beats Yates. Report, at each size: the best count, corners per point, the list
"non-zeros per step" (zreplay prints it), the number of prefix steps, the orders, and the replay line.

**The growth law it could reveal.** corners(N) / N at 16, 32, 64, 128. Three outcomes to tell apart: bounded (linear size);
(1/2) log2 N + constant (Yates' law again, by another road); something between, such as sqrt(log N) or log log N.

**The question to keep asking.** When the count stops falling, WHICH steps are expensive? Print for the best picture the outputs
whose step has four or more non-zeros and look at their sizes as subsets. An anomaly to explain [read: `zreplay.out`]: in the
best 32-point pictures the steps are almost all 2 or 4 non-zeros and come in a repeating rhythm (2, 2, 4, 4, 2, 2, 2, 2, 4, 4, ...).
The annealer has found something regular; say what it is.

---

## 2. corners-theory: the same question by thought

**The idea.** Either prove that the corners of the subset-sum picture must grow faster than N in every pair of orders, or find
the doubling rule: orders for 2N points made from orders for N points with corners(2N) at most 2 corners(N) + O(N) (that gives
N log N) or at most 2 corners(N) + O(1) (that gives linear). Tonight has neither a proof nor a construction; q-cross's last
word is "what I do not have is a reason".

**Definitions used**: picture, corner, run, prefix, one-run step, the tree fact, plain / signed.

**Start from.** q-cross.md sections 3 (hybrid 1) and 4; `q-cross/zreplay.out` (the step sizes at every size);
`s-pick/c4.py` for exhaustive play at 4 points (change three lines to print ALL optimal pairs of orders, not one);
the 8-point best: rows 5 4 6 2 3 1 0 7, columns 4 6 2 3 1 5 7 0.

**Three reformulations to work with** [derived, mine, unchecked; test each on the 4-point and 8-point solutions before trusting it].
1. *Two salesmen.* For a fixed input order the count is the length of the output path under the distance w(S, S') = number of
   places where the difference of rows S and S' changes value along the inputs (the right end counts, the left end does not).
   A lower bound on the path is the weight of a minimum spanning tree in that distance. So: for which input orders does every
   output have a neighbour at distance 1 or 2?
2. *Bonds.* Call two inputs that are neighbours in the input order a bond. corners = the sum, over the N bonds (T, T') (the
   last input with the added zero column is a bond too), of the number of places along the OUTPUT order where the function
   g(S) = [T inside S] - [T' inside S] changes value (g counts as 0 after the last output, so the end is a place too). When T' = T plus one element e, g is the indicator of a face of the cube:
   the S that contain T and not e. So the question is about two walks through the cube: how often must one walk enter and leave
   the faces named by the other walk's steps? Small T name huge faces; the empty set has two bonds, and each is entered once
   for every output step in its direction.
3. *One run everywhere means 2N - d.* With d prefix steps the count is 2N - d. How large can d be? Each prefix step says "a
   beginning of the input order is exactly the inputs inside S' and not inside S". By hand at 4 and 8 points d = 3.

**First experiment (by hand and with a 30-line program).** List every optimal pair of orders at 4 points (exhaustive) and at
8 points (exhaustive over input orders up to symmetry, exact dynamic programme over outputs: 8 cities). Describe them in words:
which chain of subsets do the prefix steps follow, which step is the two-run step, what the tree on the gaps looks like. Then
try to write the 8-point picture as "two copies of the 4-point picture plus a seam" in each of the three doubling ways of
brief 1 (c), and count what the seam costs. Then say what changes at 32 points, where the search has only 21 one-run steps of
32 and the count jumps to 80.

**Lower-bound attempts worth an honest half hour.** (i) Which outputs force many runs in EVERY input order? The inputs inside
S form a sub-cube of size 2^|S|; two outputs of middle size share a sub-cube of about the square root of that. Count, for a
fixed input order, how many of the N sub-cubes can be few runs at once (an order has only N - 1 bonds, and a set with r runs
cuts 2r of them). (ii) A rank or entropy argument on blocks: cut the picture into a x b blocks of consecutive rows and columns;
a block with no corner strictly inside has the form (function of the row) + (function of the column); how many such blocks can
tile a picture of Z? (iii) The literature under other names [guess, from memory, check dates and hypotheses]: subset sums are
"dominance sums" on the cube, and off-line range-sum lower bounds in the model with subtraction (Chazelle's work of the 1990s;
I recall a bound of order N log log N for off-line orthogonal range counting, and stronger bounds only with bounded
coefficients or without subtraction). q-cross did not search this literature.

**Variations the task asks about.** Allow single inputs and single outputs as extra nodes (a rectangle may then be one cell,
one row segment or one column segment: the letter on chains in full; p-8's exact tool counts this, see brief 4). Allow three
chains: Z = (running sums over outputs) x M1 x (running sums over a middle order) x M2 x (running sums over inputs), with
gates about 3N + non-zeros of M1 and M2: does the obstruction of (i) move when the middle order is free?

**The growth law it could reveal.** A proof of corners >= c N log N (or N sqrt(log N), or N log log N) in the two-chain model,
which would be the first lower bound of the night for subset sums WITH subtraction, in a model; or a doubling rule with a
bounded seam, which is a linear circuit.

**The question to keep asking.** The transform's letters are quadratic because two rows agree on exactly half of the columns.
The rows of Z are nested instead. What, exactly, does nesting forbid?

---

## 3. onerun: can every output be its neighbour plus or minus one run, at 32 points?

**The idea.** A yes-or-no question that ends in a statement either way. Is there an order of the 32 inputs and a path through
the 32 outputs such that the last output is one run of consecutive inputs and every other output differs from the next by plus
or minus ONE run? Yes at 4 and 8 points [read; 4 points confirmed exhaustively, ran]; at 16 points the search has 13 such steps
of 16, at 32 points 21 of 32 [read]. A yes at 32 and 64 points is a subset-sum circuit of at most 3N - 4 gates (92 and 188;
Yates has 80 and 192), and if it continues it is linear size. A no with a reason is a lemma about subset sums with subtraction.

**Definitions used**: run, prefix, one-run step, gap, the tree fact, plain / signed.

**Start from.** q-cross.md hybrid 1 ("A structure fact") and section 6 experiment 5; `q-cross/zreplay.py`; `s-pick/c4.py`.

**Three facts that cut the search** [derived, mine, check on the 8-point solution first].
1. Plain version: a one-run step joins S and S' with S inside S', and the run is exactly {T : T inside S', T not inside S}.
   So the output path is a path through all 2^k subsets in which neighbours are always comparable (one inside the other). If S'
   is S plus one element e the run is the set of T between {e} and S', which has 2^|S| members.
2. For a FIXED output path the question "is there an input order making all N sets runs?" is the *consecutive-ones problem*
   (given a family of sets, order the ground set so that each set is consecutive), solvable in linear time by the classical
   PQ-tree method of Booth and Lueker, and a no always comes with a small forbidden configuration (Tucker's list). So the
   search is over output paths only, and a no has a certificate one can print.
3. The N runs form a tree on the N + 1 gaps. Counting inputs: the input T lies in as many runs as the membership "T inside S"
   changes along the path (plus one if T is inside the last output). The empty set lies in one run only, the last output.

**First experiment.** k = 4 first, exactly (the search says 13 of 16; is 16 of 16 impossible?). Depth-first search over output
paths with comparable neighbours, adding one step at a time and testing the consecutive-ones property of the sets so far
(it can only get harder, so the search prunes early); or one SAT instance: order variables for every pair of inputs with
transitivity, successor variables for the output path, and for every candidate step the clause "no input outside the set lies
between two inputs of the set". Then k = 5. Then the signed version (inputs and outputs may be negated first; a step is then a
run in the signed running sums), and the version where the path may be a TREE of outputs (each output = one earlier output plus
or minus one run): that version is still 3N gates and is strictly easier to satisfy.

**The growth law it could reveal.** Yes at k = 4, 5, 6: gates 3N - 4, linear. No at k = 4 or 5: the least number of runs per
step that IS possible (two runs per step is still 5N gates and still linear); so if "one" fails, ask at once for the least r
such that every step is at most r runs, and how r grows with k.

**The question to keep asking.** If no: which three or four outputs cannot be consecutive-ones together in any order, and does
the same configuration exist for r runs at larger k?

---

## 4. zletter: subset sums on any two trees, not only chains

**The idea.** A letter may use any merge tree on the inputs and any merge tree on the outputs. For the transform every tree
shape examined gives a count that grows quadratically (the cause: two rows agree on half of the columns). For subset sums only
the two-chain shape was counted (5, 13, 30, 80). p-8 wrote an exact tool that, for ONE input tree, finds the least number of
rectangles over ALL output trees and all numbers; nobody pointed it at Z.

**Definitions used**: merge tree, node, chain, rectangle, letter (gates = N - 2 + rectangles).

**Start from.** `p-8-fibonacci/dw.c` (header: "exact minimum number of tree rectangles for the 2^K-point transform over GF(P),
for ONE column merge tree and ONE column scaling, minimised over ALL row merge trees, all row scalings and all numbers"; it is a
shortest-network (Steiner tree) dynamic programme on the P^N vectors; usage `dw P K [w] < lines "m1 .. m_(N-1)  c0 .. c_(N-1)"`,
the m's are the internal nodes of the input tree as bit masks, the c's the input scalings; with `w` it prints the network);
`p-8-fibonacci/trees8.txt` (the input trees at 8 points up to symmetry, one per line after a count; q-cross says 149);
`dw2.c`, `dwg.c`, `dws.c`, `branch3.py` (p-8's tools for 16 points, where the exact programme is too large; read p-8.md
section 1 before using them); `p-8-fibonacci/h8_13rect_19gates_replayed.txt` (the format of a replayed letter).

**First experiment.** In `dw.c` the targets are the lines through the rows of H; replace the rows of H by the rows of Z (and note
that the symmetry classes in `trees8.txt` were computed for H: Z has fewer symmetries, only permutations of the k bits, so
either run every tree in every orientation or recompute the classes). Run all input trees at 8 points modulo 3 and modulo 5
(a count modulo a prime is a candidate until one network is lifted to whole numbers and replayed). Questions: is anything below
13; which tree shapes win; is the chain best, worst or in the middle (for the transform it was the worst shape tried, 23
against 13 on balanced trees). Then, at 16 points, the best two or three shapes against the two-chain 30, with p-8's 16-point
tools or with an annealer over (two trees, rectangle list) seeded from the 8-point winners doubled.

**The growth law it could reveal.** rectangles(N) / N for the best tree shape at 8, 16, 32 points; and WHICH shape: if the
winning input tree is "a chain of chains" or follows the nesting of the subsets (a tree whose nodes are down-sets), that shape
is a construction to continue by hand.

**The question to keep asking.** Yates' method is itself a letter-like object with zero rectangles to spare and (N/2) log2 N
gates in its trees' place. Between "two chains, all the cost in corners" and "Yates, all the cost in the sums", is there a
tree shape where both are O(N)?

---

## 5. zdz: build the transform from two-chain subset sums and read it with the meters

**The idea.** H = Z D Z^T. Take the best two-chain circuit for Z, use it twice with the free scalings (-2)^|J| between, and you
have a circuit for the transform of 2 (N - 2 + corners) gates whose wires are running sums: neither tight wires nor wires of
one merge tree. m-cross found that every one of the 18 transform circuits of the night is one merge tree modulo 2 with no Q
gate and order 1, and that the published unit's centre is not. This should be the first small circuit that breaks the
pattern. It will not be a record; the point is what the meters show, because whatever they show is what "a circuit of the
other kind" looks like at small size.

**Definitions used**: two-chain program, corner; wire, class, survivor, dead gate, kinds J / S / Q / E, order, one merge tree
modulo 2, tight / over the limit.

**Start from.** `q-cross/cat3_16.out` and the best 64-point orders that brief 1 produces (or `cat3g_64.out`, 261 corners, to
have something at once); `q-cross/zreplay.py` (it builds the gate list in memory: make it WRITE the gate list in the
`name = a * u + b * v` format); `m-cross/meter2.py`, `laminar.py`, `dups.py` (the meter modulo 2); `h-0-onepergate/opg.py` and
`meters16.out` (h-0's meter: gates + over-limit wires against N log2 N); `g-4-zetalead/calls3.py`, `verify.py` (g-4's own
check of the identity).

**First experiment.** (1) First pass: v = Z^T x. No transposed circuit is needed: complement every address and use the Z
circuit [derived above]. (2) Scale v_J by (-2)^|J| (free). (3) Second pass: y = Z v. Replay exactly on all basis vectors at
16 and 64 points. (4) Before metering, write down a prediction. Mine [guess]: after the scaling, the class of a running sum is
decided by its terms of LEAST weight |J| only, so the second pass holds many classes that overlap without nesting; the count of
classes will exceed 2N - 1; and the output steps y_a = y_(a+1) + ... will be Q gates or gates of order above 1 wherever two
neighbouring outputs agree modulo 2 (all outputs of H agree modulo 2). (5) Meter: number of classes against 2N - 1, pairs of
classes that overlap without nesting, counts of J / S / Q / E, the orders of the dead gates, survivors and dead gates,
over-limit wires and h-0's sum.

**The growth law it could reveal.** The break-even: 2 (N - 2 + corners) < (3/4) N log2 N needs corners < (3/8) N log2 N - N + 2
(10 at 16 points, which is impossible because M is invertible and so has at least N non-zeros; 82 at 64 points; 210 at 128);
linear size needs corners = O(N). And a second law, the one this brief is really
for: in this circuit, how do the number of Q gates and the highest order grow with N? If every order-changing circuit must have
Q gates of growing order, that is a shape to search for directly.

**The question to keep asking.** The floor "dead gates >= (N/2) log2 N" is a guess for one-tree circuits. Does this circuit
have FEWER dead gates than (N/2) log2 N while having more gates in total, and if so, which survivors paid for them?

---

## 6. unit2adic: which of "one merge tree, no Q gate, order 1" does the published unit break first

**The idea.** All the small circuits of the night share three properties modulo 2, and inside those properties the count seems
stuck at N - 1 + (N/2) log2 N. The published program is the only object known to change the order, so it must break at least
one of the three. Measure which, where in the unit, and how early. The answer is a specification for an order-changing step.

**Definitions used**: wire, primitive form, class, survivor, dead gate, kinds J / S / Q / E, order, one merge tree modulo 2,
the published unit, scatter matrix, address map.

**Start from.** `h-7-unitmeter/unitmeter.py` (it parses the published certificate, read only, and replays one invocation with
exact fractions; usage in its header: `python3 -I -B unitmeter.py <certificate.json.gz>`; the path of the certificate is in
h-7.md section 2 and in `unitmeter.out`); its dictionary: every register holds (a vector w over the 120 sources) x (a row of a
frame, digit by digit), so a wire of the unit is a product across the cut batch | address; `h-7-unitmeter/scatter.py`,
`frames.py`, `depth.py`; `m-cross/meter2.py`, `laminar.py` (the three tests), `m-cross/e8shadow.py` and `.out` (the scatter
matrix doubled and read modulo 2: 120 classes of 56 entries, every pair overlapping without nesting, rank 8); h-8.md around
lines 40 and 217 (the conflict between a-2's ledger and h-7's dictionary, which this measurement settles).

**First experiment.** Write the unit as ONE gate list on a single array: the batch index (which of the 120 sources) as the high
address bits, f = 1 digit column, every block move and every addition expanded into its gates (G). Do the scatter alone first
(the 120 x 120 centre), then one whole E8 invocation. Run the meter and report five numbers for each: classes against 2n - 1;
pairs of classes that overlap without nesting; Q gates; dead gates of order above 1; dead gates against (n/2) log2 n, n the
array length. Then locate: the first gate, in program order, that breaks each property, with its two parents printed. And for
every addition, the number of sources on both sides before and after (h-8's `ledger-vs-unit`).

**The growth law it could reveal.** How the three counts scale with the unit's own size parameters (number of sources, frame
dimension, digits f): if the number of Q gates per wire, or the order, grows with the nesting depth of the published
construction, that names the mechanism by which the saving multiplies while the excess only adds [read: h-7's phrase].

**The question to keep asking.** The unit's wires are products (batch vector) x (frame row). Is the overlap without nesting
entirely on the batch side (120 E8 lines), entirely on the address side (oblique frames, that is address maps), or does it need
both at once? A small circuit of the same kind would have to copy exactly that.

---

## 7. twotrees: circuits with two merge trees in different bit orders

**The idea.** In a one-tree circuit every output is reached from a hub by shifts whose partners are wires of that one tree.
m-cross's count: two outputs differ on a half-space; a half-space of the b-th bit of the tree's order is 2^(b-1) tree nodes; a
Gray-code walk through the outputs uses bit b on N / 2^b steps; the product is N/2 per bit, hence (N/2) log2 N dead gates. With
a second tree in another bit order the half-spaces that were expensive in the first tree are single nodes in the second, and
the same sum is O(N), if the partner did not have to agree with the wire it shifts. Nobody has measured what agreement
costs with two trees.

**Definitions used**: merge tree, class, survivor, dead gate, shift (S gate), hub, partner, agreement rule, one merge tree
modulo 2, address map.

**Start from.** m-cross.md hybrid 2 (the last paragraph is the whole argument) and experiment 4; h-6.md lines 159 to 199 (the
agreement rule and the measured cost: "the agreement rule costs a factor of about two against the free metric");
`h-6-classhub/onecentre16.c` and `onecentre16_quad.out` (h-6's exact count for one-centre programs at 16 points with the
agreement rule: adapt it instead of starting from nothing); `g-1-tightwires/pool.py` and h-0's pool of 304 vectors
(`h-0-onepergate/opg.py`); `m-cross/meter2.py` to confirm that what you build really has two trees (more than 2N - 1 classes,
some pairs overlapping without nesting).

**The cube tree in bit order (b1, b2, b3, b4)** is the merge tree whose nodes are the sets of addresses that agree on b1; on
b1 and b2; on b1, b2, b3; and the single addresses. A *tree wire* is a wire with entries +1, -1 on one node and 0 elsewhere.

**First experiment.** 16 points; trees in orders (1,2,3,4) and (3,4,1,2). Count exactly: (a) the survivors needed to hold both
trees (2 (N - 1) less the nodes they share); (b) the least number of shifts that reach all 16 outputs from one hub when a
partner may be any held tree wire of either tree and must agree with the current wire; charge every extra tree wire (a second
sign pattern on a node already held) as the gate it is; (c) the same without the agreement rule, to see the O(N) of the
sketch appear; (d) the control: one tree per bit (four trees), which must give the textbook back. Then 32 and 64 points with a
search in place of exhaustion. Mutations to try at once: three trees; the second tree OBLIQUE, meaning the first tree
carried by an address map such as "bit 3 becomes bit 3 + bit 1" (its nodes are cosets of subspaces that are not coordinate
sub-cubes; on such a node every output is still a single sign pattern, a property only the transform has in its class).

**The growth law it could reveal.** Dead gates with two trees as a function of N: (N/2) log2 N again, a smaller multiple of
N log N, or c N. And the price list: how many sign patterns per node a walk through all outputs needs (one form per node is
the wall named W-A in q-cross; here a node may hold several, each paid for).

**The question to keep asking.** Agreement says the partner must already look like the wire on its support. Which walk through
the outputs keeps the wire looking like a FEW patterns on the nodes of the second tree for a long time?

---

## 8. quotient: the first useful Q gate

**The idea.** A Q gate subtracts two wires that are equal modulo 2 (or modulo 4) and divides by 2 (or 4): one gate that reads
two over-limit wires and writes something new, the one kind of gate that h-8's proof of the wall cannot handle and that no
circuit of the night contains. m-cross tried the obvious ones, (h_a - h_b)/2 for two outputs, and found them circular: such a
piece serves only the outputs that made it. A Q gate that pays must have parents that are not outputs. The nearest candidates:
wires with entries of two sizes, 1 and 3, that are equal to an output modulo 4.

**Definitions used**: wire, class, Q gate, order, over the limit, partner, shift, dead gate, the floor.

**Start from.** m-cross.md hybrid 3 and experiment 5; `m-cross/trial2.py`, `trial2.out` (the circularity runs: 28 of 28 pairs
at 8 points, 120 of 120 at 16; and the control: a second textbook pass is all Q gates); h-8.md (Proposition A and "the failing
gate": the first gate with two over-limit parents); h-0's census `h-0-onepergate/census.py`, `anyex.py` (which wires are one
gate from how many outputs, tight partners only); h-5.md lines 134 to 180 and `h-5-ladderbound/cplx.py` (every hub is the real
part of one complex product wire with factors (1, i) and (1, -i)).

**First experiment.** 8 points. For each output h (a row of H), the wires equal to h modulo 4 with entries in {1, -3} where h
is +1 and {-1, 3} where h is -1: 2^8 of them, u = h - 4 h*a for a 0/1 vector a (h*a = h on the set a, 0 elsewhere).
Two such wires for the same h give the quotient (u - v)/4 = h*(b - a): [derived] ANY vector of the form "h on one set, -h on
another, 0 elsewhere" comes out of ONE Q gate. So the Q gate is cheap and universal; the whole cost is in its parents.
Measure: (a) for each quotient wire, how many outputs is it one gate from, and with which partners (h-0's census covers tight
partners only: extend it); (b) what do the parents cost: which wires with entries 1 and 3 are one or two gates from wires a
record circuit already holds (take the 19 and the brick's hub as the stock), and do two of them for the same h come for less
than two gates each; (c) the smallest closed loop: stock -> two parents -> quotient -> k outputs, with the gate count of the
loop against k. Then the same over the Gaussian integers, where 2 = -i (1 + i)^2: a quotient by (1 + i) is a step of half
order, and wires equal modulo (1 + i) are far more common than wires equal modulo 2.

**The growth law it could reveal.** Births per gate. h-5's bound says a gate gives birth to at most (width of its wider parent)
new useful directions when wires are entangled on few bits; a quotient of two full-width parents has no such limit. If a
quotient wire at N points can serve a number of outputs that grows with N, the floor (N/2) log2 N of dead gates does not
apply to circuits with Q gates, and one should ask at once how the count of such loops scales from 8 to 16 to 32 points.

**The question to keep asking.** Where do two different cheap wires that are equal modulo 4 come from? (In the published unit
they come from the 120 lines of E8, whose inner products are all 0 or +1/2 or -1/2; brief 6 is the other end of this question.)

---

## 9. compose: composition laws, and whether the excess can grow slower than N log N

**The idea.** Excess e = gates - (N - 1) - (N/2) log2 N measures how far a circuit sits above m-cross's floor. The tensor
product has a law: e(A x B) = n e(A) + m e(B) + (m - 1)(n - 1) for sizes m and n [read: m-cross fact E, derived there and
checked on the 54-gate circuit]. From it [derived, mine]: tensor powers of a circuit with N0 points, k0 address bits and excess
e0 have rate 1/2 + (N0 - 1 + e0) / (N0 k0), which is 7/8 for the brick and 19/24 for the 19, and would tend to 1/2 only along a
sequence of ever larger circuits on the floor. So the tensor product can never change the order, and the term to kill is
(m - 1)(n - 1): the second factor rebuilds its hubs once per coordinate of the first. The staircase composes two bricks at 16
points with 5 where the tensor product pays 9, by letting the outer circuit reuse wires of the inner one. No one has
enumerated the ways to do that.

**Definitions used**: survivor, dead gate, excess, hub, brick, the 19, staircase, one merge tree modulo 2, floor, tensor product
(apply A to the low address bits inside every block, then B to the high bits across blocks, or interleaved).

**Start from.** `h-6-classhub/brick_m1.txt`; `g-1-tightwires/h8_19gates.txt`; `e2-0-pieces/slp_4.txt` to `slp_64.txt` and
`gen.py` (the staircase generator); `h-0-onepergate/h16_54gates_tensor.txt` (19 x textbook-2, e = 7); `h-1-staircase3/`
(`slp16_52_from54.txt`, the second 52 of another shape; `sa.c`, the annealer; `mkseed.py`; h-1.md section 4 on interleaving);
`m-cross/meter2.py` and `dups.py` (they print e's ingredients and NAME the extra dead gates: in the staircase each is a second,
third, fourth hub on a support that already holds a hub; `m-cross/dups.out`).

**First experiment.** Two bricks at 16 points. The outer brick acts on four blocks; it needs, for each of its 7 gates, wires of
the inner circuits as inputs. Enumerate the choices: which inner wires (inputs, pair sums, hub, outputs) each outer gate
reads, and in which of the block's four coordinates; for each consistent choice build the gate list, replay exactly, and
compute e. The tensor product (e = 9) and the staircase (e = 5) must both appear in the list: that is the test of the
enumeration. Report the least e and the full table. Then a brick with the 19 (32 points) and the 19 with itself (64 points), by
the same program or, where the enumeration is too large, by the annealer seeded with each composition.

**The growth law it could reveal.** e_min(N) under the best composition law: c N log N with c below 1/4 (a better constant
only, of no interest here); o(N log N) (the first family of rate 1/2, which is the floor reached); or NEGATIVE and of order
N log N (the floor broken, which is the only outcome that touches the order). Write the law you find in the form
e(A o B) = n e(A) + m e(B) + cross(m, n) and say how cross grows: (m - 1)(n - 1) for the tensor product; what for the staircase;
and whether any composition has a cross term that is negative.

**The question to keep asking.** In the published program "excess adds, saving multiplies" [read: h-7]. In these small
circuits the saving of the inner circuit is spent once per block. What would the outer circuit have to read so that one
inner saving is used by ALL blocks, and is that reading an address map?

---

## 10. checkerboards: the corner count modulo 2 and modulo 4 (my choice; it joins the two recombinations, which were written in the same hour and never met)

**Why this one.** q-cross found that the corner picture is cheap for Z and quadratic for H. m-cross found that everything of the
night lives modulo 2 and that "tau near 1" is "modulo 2". Put together they say something neither says alone:
- [derived] In a picture of 0s and 1s a second difference is +2 or -2 exactly when the 2 x 2 window is a checkerboard
  (1 0 / 0 1 or 0 1 / 1 0). **Modulo 2 a checkerboard is free.** So the corner count of Z over the two-element field is at most
  the whole-number count, and the difference is the number of checkerboards a picture can afford.
- [ran, `s-pick/c2.py`] It is strictly smaller at the two sizes I could run: **4 against 5 at 4 points (exhaustive), 12 against
  13 at 8 points (annealer).** At 4 points 4 = N means M modulo 2 is a permutation matrix: the 4-point subset-sum matrix is
  (running sums) x (a permutation) x (running sums) modulo 2. At 16 points my run (two short starts) only found 30 again.
- [read: q-cross hybrid 2] For the TRANSFORM in two chains the quadratic part of the count is exactly "the cells with value 4,
  the checkerboards" (5, 26, 158, 713 of them at 8 to 64 points in the regular orders) and the rest are cells with value 2
  (18, 47, 103, 243, a little above (N/2) log2 N). So **modulo 4 the transform's quadratic wall is not there**: on these
  four numbers its two-chain count grows like N log N, not like N^2. And m-cross's experiment 8 (precision) has a matrix equal to H modulo 4 in under 4N gates
  by another method [read: `m-cross/precision.py`, `.out`].
- [read: m-cross hybrid 4, the shadow lemma, three lines by hand there] An exact subset-sum circuit with no Q gate gives, by
  keeping its J gates, a circuit of additions over the two-element field for Z modulo 2 (the Sierpinski matrix), whose cost
  with cancellation allowed is an open number in the literature as the reports quote it (Boyar and Find, 2012). The two-chain
  picture modulo 2 is a concrete family of such circuits WITH cancellation: the running sums cancel all the time.

**The idea, in one sentence.** Count corners modulo 2 for Z and modulo 4 (then 8, 16) for H, find how those counts grow, and then
ask what it costs to repair the picture from "right modulo 2^j" to "right modulo 2^(j+1)": the repair is a matrix supported on
the checkerboards, divided by 2, which is exactly a layer of Q gates.

**Definitions used**: picture, second difference, corner, two-chain program (over the two-element field the gates are
exclusive-ors: N - 2 + odd corners of them); class, Q gate, order; checkerboard (above).

**Start from.** `s-pick/c2.py`, `s-pick/c2.out` (pure Python, slow: rewrite the count in C with the tricks of brief 1; modulo
2 a row of the picture is a bit word and the cost of two neighbouring rows is the number of 0/1 changes in their exclusive-or);
`q-cross/cat1.py`, `cat2.py` (the transform's pictures and their value-2 and value-4 cells); `m-cross/precision.py`,
`precision.out` (H = sum over j of (-2)^j B_j with B_j(y, x) = C(number of common ones, j); the partial sums are H modulo 2^j
and have rank 1 + k + ... + C(k, j-1)); `m-cross/meter2.py` (to count the Q gates of a repair layer);
h-4's 2,748 optimal 8-point subset-sum circuits (`h-4-zetafloor/`, for the shadow lemma's check) and
`g-4-zetalead/note-for-zeta-readers.md` (what was read of the subset-sum literature, with dates).

**First experiment.** (1) Z modulo 2 at 16, 32, 64, 128 points with a real annealer: odd corners per point, and the number of
checkerboards in the best pictures. Is it N + o(N)? (At 4 points it is N exactly.) (2) H modulo 4: the least number of cells of
value 2 (cells of value 4 free) over both orders and sign scalings at 8, 16, 32, 64 points, against p-6's lower bound
(N/2) log2 N for bit-linear orders. (3) The repair. Take the best picture of (1) at 8 and 16 points. Delete the entries +2 and -2 from its M
(keep the signs of the odd entries): that gives a whole-number matrix Z' = (running sums) x (M without its 2s) x (running
sums) equal to Z modulo 2. In the SAME two orders the remainder (Z - Z') / 2 is one rectangle per checkerboard, so nothing is
gained there [derived]; the experiment is to treat (Z - Z') / 2 as a new matrix: its rank, its least corner count over OTHER
pairs of orders, and whether its rows are combinations of wires the first layer already holds. Repeat (repair of the repair)
until the remainder is zero; total the gates. (4) Lift every modulo-2 circuit
that claims a count and replay it; a count modulo 2 is a statement about exclusive-or circuits only.

**The growth laws it could reveal.** (a) Odd corners of Z per point: bounded would be a linear-size circuit of exclusive-ors
with cancellation for the Sierpinski matrix, a statement for another community (claim nothing about any conjecture; check the
literature since 2012 first), and by the shadow lemma a hard limit on what exact circuits WITHOUT Q gates can do would follow
from its failure. (b) The number of repair layers and the cost of each as functions of N: if the layers number about log N
and each costs about N, that is N log N once more and the count (N/2) log2 N = "the power of 2 in the determinant of H"
[read: m-cross fact B] has been met a sixth time; if the layers shrink geometrically, the total is linear.

**The question to keep asking.** Everything cheap tonight is cheap modulo 2 and pays for the higher binary digits one at a time.
Is there any pair of orders in which the checkerboards of one layer are the corners of the next, so that one set of running
sums serves every digit?

---

## What these ten share, in three lines

Briefs 1 to 4 ask one question from four sides (search, proof, a yes-or-no instance, other tree shapes): the corners of the
subset-sum picture. Briefs 6 to 9 ask m-cross's question from four sides: which of "one tree, no Q gate, order 1" must go.
Briefs 5 and 10 are the two bridges between them. Every count above that is not marked [ran] or [read] with a file is mine and
unchecked; the three reformulations in brief 2 and the cost formula in brief 9 should be tested on the smallest case first.

Files of mine: `waves/wave-06/s-pick/c4.py` (4 points, exhaustive, plain and signed),
`c2.py`, `c2.out` (corners modulo 2 at 4, 8, 16 points). Both ran through light.py; the longer took 6 seconds.
