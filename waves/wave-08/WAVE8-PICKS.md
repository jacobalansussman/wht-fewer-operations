# WAVE 8 PICKS: nine briefs, one hour each

11 October 2026, about 05:00 EDT, agent "aa-pick", 15-minute box. Private. A curator's hand-over, not a verdict: nothing below is
ranked by odds, nothing was run by me, nothing is reviewed or in Lean. Marks: [read] = in a file I opened in this box
(w-cross.md and x-6.md in full; the heads of x-0, x-3, x-5; the avenues NOTE and the fat-label passages of v-levers and
k-levers; the heads of the tiny-unit notes); [derived] = by me, minutes old, checked by nobody; [guess].
Not opened by me: x-1, x-2, x-4, x-7, x-8, x-9 beyond single lines; the programs themselves beyond their first lines; the
wave-7 skeptics (z-*.md, WAVE7-NOTE.md had not landed).

**The user's bar.** Only a change of ORDER counts: a saving of 1e-1 or more (n (log n)^z with z at most 0.9), or linear size
O(n). Constants and records at one size are out of scope. Every brief must end with a growth law in N or a sentence saying
why none came out.

Folders. I = `waves`. C = `(not in this repository) verify/checks`.
R = `(not in this repository) wht-power-saving-r4-candidate` (READ ONLY).

## Words for all nine (read once)

- N = 2^k *points*. An *address* is a word of k bits. x.y = number of common ones of two addresses, modulo 2. *Weight* of an
  address = its number of ones. *The transform* H: N x N matrix with entries (-1)^(x.y). *Textbook*: N log2 N gates.
- Gate count **(G)**: a gate is any a*u + b*v of two earlier values, scalings free. (Count (O), OpenAI's, charges every
  addition and every scalar multiplication; say which one you use each time.) T(N) = least number of (G) gates for H.
- *Wire*: a value a program holds, written as a vector over the N inputs and scaled to whole numbers with no common factor.
  *Height* of a wire: its largest entry in absolute value. *Sign vector* or *form*: a wire of height 1.
- *Subset sums* Z: output at a set S = sum of the inputs at all subsets of S. H = Z D Z^T with D a diagonal of powers of -2.
  *Yates*: the standard (N/2) log2 N gates for Z.
- *Neighbour sums* A: every address receives the sum of the inputs at its k neighbours (addresses differing in one bit).
- *Convolution with q* (q a function on addresses): output(y) = sum over x of q(x + y) input(x), bits added modulo 2.
- *Class*: all k-th tensor powers of 2 x 2 kernels [[1,1],[1,s]]; H is s = -1. "An identity of the class" = a saving that
  works for every s, hence uses nothing special about H.
- The engine (the published, Lean-checked mechanism), in its own words. An *array* is one working copy of the data. A *move*
  is one direction of the transform applied to one whole array; only moves cost. *Block size* m: the number of moves each
  array is owed (45 in the published unit). A *unit* serves W arrays in fewer than W x m moves; the engine turns a unit into
  a saving 1 - z. A *block* (x-6's word, also the engine's) is a run of moves on one array with no addition in between; its
  *rank* is the number of moves in it. **Price law [read: x-6 section 6; the engine's own, v-tiny.md line 25]: z is the root
  of "sum over all blocks of the unit of (rank/m)^z = W".** With k equal blocks per array and a share rho of its directions
  never moved along: **saving = ln(1/(1-rho)) / (ln k + ln(1/(1-rho)))**. Saving 0.1 needs rho = 7.4 % at k = 2, 11.5 % at
  k = 3, 18 % at k = 6, 28 % at k = 20; one block per array gives n log log n. Published unit: k = 16.5, rho = 0.21 %.
  Program: `I/x-6-unitasbox/zlaw.py` (floats; function `root(blocks, m, W)` with blocks = list of (rank, count)).
- *Port* (x-6): a direction along which the transform splits off one move. For H the ports are the 2^(h-1) address words of
  odd weight on a block of h address bits; every other kernel of the class has only its h coordinate directions. *Fat port*
  of dimension r: a subspace P of the address space that meets its perpendicular P-perp only in 0 (w-cross hybrid 3 [ran]:
  20, 80, 336 of dimension 2 at h = 4, 5, 6; 640 of dimension 3 at h = 6). H = (transform on P) x (transform on P-perp).
- *Address map*: a relabelling of the addresses inside a block by an invertible bit matrix. A free step of the engine's game.

## Rules for every developer

Private research: publish nothing, no git, no Lean. Small exact runs through
`python3 -B C/wht35/bin/light.py <label> <max seconds, at most 600> <command...>` (exit code 75 = no free slot, retry).
Heavier runs: at most two jobs at a time, 20 minutes each, nice 19, on the rented Linux machine, files under
`(the Linux machine's working folder)/<your label>/`, results copied back. Exact rational or Gaussian-rational arithmetic, or modulo primes
with the reason why that suffices. A circuit found modulo a prime is a candidate until lifted and replayed exactly; "none
modulo p" is not "none". Mark every statement [read], [ran], [derived], [guess]. Generation first, play second, criticism
last. Plain English: explain a term before using it.

---

## 1. neighbour-sums: can the sum over the k neighbours of every address be had in O(N) gates?

**Idea.** A linear-size transform would force neighbour sums into O(N): A costs at most 2 T(N) + N (x-5: the "add one
element" step is L - Z L Z^-1 with L the diagonal of set sizes; w-cross hybrid 1: H is, up to free signs and a relabelling,
one polynomial of degree k in A, a multiple of exp(-i (pi/4) A)). So A is a NECESSARY test that is far simpler than H, and
no wall of the night speaks about it: the volume count asks only about (N/2) log2 k units [derived by w-cross, rough]. Every
count known grows like k N. Either answer moves the main question.

**Special words.** *Pairing count*: the hand construction of x-5, (3/4) k - 1 gates per point for even k (0.5, 2, 3.5 at 4,
16, 64 points). *The two blocks*: A maps even-weight addresses to odd-weight ones and back, so the matrix is two equal
(N/2) x (N/2) blocks; price one. *Volume count* (Morgenstern): the sum over gates of log2((|a|+|b|)/g) is at least log2 of
the determinant.

**Start from.** `I/d-0-zeta/mincirc` (exact minimum circuit over the field of p elements; usage `mincirc p n m [rowsfile]`,
m = number of intermediate values; source `mincirc.c`), `I/d-0-zeta/rows_nbr3.txt` (the 8-point matrix: 12 gates is exact
modulo 2, 3, 5 [read]), `I/d-0-zeta/rows.py`, the annealers `I/j-machine/slp.py` and `relax.py` (free coefficients in
floats, hits replayed in fractions), `I/w-cross/hyb.py`, `I/x-5.md` sections 6 and by-product 2.

**First experiment.** One block at 16 points (8 x 8, four ones per row, 16 gates by pairing): `mincirc` modulo 2, 3, 5 for
15, 14, 13 gates. Then the annealer with free coefficients at 32 and 64 points. Then the same for A + c x identity, c = 1, 2
(invertible, so the volume count is exact). Record the height of the wires of every best circuit.

**Growth law wanted.** Least gates per point as a function of k: like k (pairing), like log2 k, or bounded. Then the easy
half on paper: circuits with gates u + v only need at least c k N (the matrix has k N ones and no 2 x 3 block of ones;
w-cross recalled this, nobody derived it).

**Keep asking.** Does cancellation, or a coefficient other than 1, EVER save one gate against the best adding-only circuit?
If not at 16, 32 and 64 points, what is it about the cube that forbids it, given that volume does not?

---

## 2. fewer-blocks: change the objective of the engine's game from moves to BLOCKS per array

**One of the only two experiments of this wave aimed at the bar of 1e-1 (the other is brief 7).**

**Idea.** Every search of the engine's game so far has minimised moves. The price law does not reward that; it rewards
arrays whose climb is interrupted few times. Two blocks per array with 7.4 % of the directions skipped is a saving of 0.1;
the published unit has 16.5 blocks and 0.21 %. Nobody has optimised the number of blocks.

**Special words.** *Exchange* (x-6 section 1): the three-shear word that swaps "a move on one array" for three additions
between two arrays, c1 = D^-1 X; Y1 = Y + c1; c2 = D Y1; X2 = X - c2; c3 = D^-1 X2; Y3 = Y1 + c3. *Shear*: target += (source
moved backwards along the port). *Batch*: a sum of v sources that have each made the h - 1 moves they owe anyway is ONE
array; one transform backwards on it (h moves) delivers v different port moves. *Total*: such a sum, held in a scratch
array. *kappa* = v / (number of totals) = sources served per total (15 for the published E8 unit: 120 shears, 8 totals of 9
moves). *t knows s*: the unwanted share of source s in target t can be removed later by additions alone; for fat ports this
holds when P_s lies inside P_t-perp. *Knows graph*: ports as vertices, an edge when two ports know each other.
*Helper*: an array that is not data but holds intermediate values; the engine charges it all m moves (published: 783
helpers for 480 data arrays). *Legal network*: a program made only of the engine's steps (moves, additions with rational
coefficients, scratch arrays, shifts, phase letters, address maps) that leaves every live array holding the transform of
its own input, for every number of digit columns; rules in `C/wht35/wider/w-engine/GAME.md`, replay with
`C/wht35/wider/w-engine/regmachine.py` [paths read from the tiny-unit notes; files not opened by me]. *What-if count*: a
list of blocks with no network behind it.

**Start from.** `I/x-6.md` sections 5, 6, 8 and `I/x-6-unitasbox/zlaw.py`, `ports2.py`, `relation.py`;
`C/wht38/tiny/next/NOTE.md` and `C/wht38/tiny/next/amap/` (the full-game search with address maps, `salga.py`);
`I/w-cross/hyb34.py` (lists the fat ports); `R/tools/gen/foldlib.py`, `R/tools/whatif_copies.py` (the engine's own price).

**First experiment.** (a) On paper: for an exchange between two arrays, the least number of blocks each array is cut into.
x-6 says three ("every shear touches both arrays"): write the argument out and look for the word that breaks it (shears in
which the same array is source twice in a row; a shear whose target is a scratch array). (b) A table [derived by me,
unchecked: the number of totals is at least the largest set of ports no two of which know each other, since the scatter
matrix restricted to such a set is the identity; so kappa <= v / (that number), and E8 meets it exactly, 120 / 8 = 15]: for
(h, r) = (5,2), (6,2), (7,3), (8,3), (9,3), (9,4) compute the knows graph of the fat ports, its degree, its largest set
with no two knowing each other, and so the ceiling on kappa; put that kappa, with totals priced as blocks of rank h, into
`zlaw.root`. (c) In the tiny game at block size 4 and 5 with address maps, score candidate words by blocks per array.

**Saving it could reveal.** ln(1/(1-rho)) / (ln k + ln(1/(1-rho))): 0.1 at (k, rho) = (2, 7.4 %), (3, 11.5 %). Also the
floor question: can any array in any legal network make ONE block of rank below m (that would be n log log n).

**Keep asking.** How many times must an array's climb be interrupted, and by what? **At the end state plainly: was a LEGAL
network of the engine found, or only a what-if count.**

---

## 3. tall-pool: search where wires may be tall

**Idea.** The height lemma (x-0 lemma 3, x-2, both [derived], unreviewed): a circuit for H whose wires all have height at
most M has at least N - 1 + ((N/2) log2 N - (N - 1) log2 M) / log2(4 M^2) gates, whatever its coefficients. So C N gates need a
constant fraction of gates on wires of height about N^(1/(4C)), and every pool searched tonight (heights up to 7) could not
have held a linear circuit. Yet where tall wires were built (x-5's tower, x-9's hubs) they bought nothing. Nobody knows
what a tall wire that PAYS looks like. The one known specimen: the second pass of Z D Z^T, gates u + v between wires of
height up to N/2, at exactly N log2 N.

**Special words.** *Flag*: a chain of subspaces of the address space, each one dimension larger. *Coset* of a subspace U:
a set x + U. *Pool*: the set of wires a search may use. *Budget* of a gate w = (a u + b v)/g: log2((|a|+|b|)/g).
*Two frames*: wires built on cosets of two different flags, the second related to the first by an address map or by a port
splitting (w-cross hybrid 3).

**Start from.** `I/x-0.md` (lemmas 1 to 3, mutation 4), `I/x-0-twojobs/tj.c` (local walk over circuits with a pool given by
an ALLOW mask of entry sizes; `tj8`, `tj16` binaries; `exh8.c`), `I/x-0-twojobs/budget.py`, `I/u-4.md` (Z D Z^T),
`I/g-1-tightwires/h8_19gates.txt` (control: the 19-gate circuit at 8 points).

**First experiment.** Pool = wires of the form sum over j of 2^j f_j, with f_j sign vectors on the cosets of one flag (the
partial sums of Z D Z^T), coefficient cap removed. At 8 and 16 points report least gates as a function of the largest j
allowed. Then the same pool taken from two frames.

**Growth law wanted.** Gates against the height cap: flat or falling. If flat at 16 points, the size at which the height
lemma FORCES it to fall (solve the lemma for N at the gates-per-point you measured), and what a paying tall wire must look
like there (in the middle of the circuit, both operands of the last gate covering everything: w-cross fact C).

**Keep asking.** What is the smallest example, for any matrix at all, where a tall intermediate wire saves a gate? Take
that example and ask what H lacks.

---

## 4. convolution-ladder: a map of which convolutions on the cube are cheap

**Idea.** [w-cross hybrid 1, derived] Let c(q) be the least gates for the convolution with q. Then
T(N) <= max over q of c(q) <= 2 T(N) + N (transform, scale, transform back; and for even k, H is itself the convolution with
q(z) = +1 for weight 0 or 1 modulo 4, -1 for weight 2 or 3, up to free signs and a relabelling). So a linear transform
exists exactly when every convolution on the cube is linear. The q that depend on the weight only form a family with k + 1
parameters that contains the identity (0 gates), all-ones (N gates), neighbour sums, "lightest outputs" (spectrum 1 on
weights up to d, 0 above; x-1) and H. Nobody has drawn the map.

**Special words.** *Spectrum* of q: the values of H applied to q; a convolution is H^-1 x (diagonal of the spectrum) x H.
*Weight-only q*: q(z) depends only on the number of ones of z; then the convolution is a polynomial in A.

**Start from.** `I/w-cross/hyb.py` and `hyb.out` (builds these matrices exactly, k = 2 to 6), `I/j-machine/slp.py`,
`relax.py` (annealers), `I/d-0-zeta/mincirc` for exact small cases, `I/x-1.md` (lightest outputs), brief 1's results if
they have landed.

**First experiment.** At 16 and 32 points price a grid: q = indicator of weight exactly j; of weight at most j (balls);
spectrum = indicator of weights up to d; q = t^weight (this is a tensor power, cheap: a control); and H's own q. Free
coefficients, hits replayed exactly.

**Growth law wanted.** For each family, gates per point against k. The answer sought: the CHEAPEST q whose cost per point
grows with k in every construction, with its spectrum. Is H the only expensive corner, or is expense generic?

**Keep asking.** Tensor powers t^weight are linear and they span all weight-only q (k + 1 of them). What stops "a
combination of k + 1 cheap convolutions" from being cheap, and is there a q where that stop fails?

---

## 5. z-cut: a meter that reads on maps of determinant 1

**Idea.** All of the cost of H = Z D Z^T sits in the two passes of Z, where the determinant is 1 and the volume count reads
nothing. x-2 has a different meter. Cut the address set into two halves L and R by one address bit. Every gate is *new at L
only*, *new at R only*, *new at both* (B), or *new at neither* (E), where "new at L" means that the gate's wire, cut down to
L, is not already available from earlier wires cut down to L. Identity for every circuit and cut [read: x-2 line 54]:
gates = n(L) + n(R) - B + E, with n(L) = gates new at L. n(L) is at least the cost of the half-size problem. For H the rows
pair up as (h, h) and (h, -h) and that forces E >= N/2 + 1. For Z the rows are (z, 0) and (z, z), and w-cross's five-minute
look says the pair argument does NOT force E there: a gate that makes (z, z) can be new on R only.

**Special words.** As above; *B = 0 circuits*: no gate does new work on both halves at once (the textbook and Yates).

**Start from.** `I/x-2.md` (the identity and "wall 1"), `I/x-2-floorhatch/alldirs.py`, `meter.py`, `cleancuts.py`;
`I/u-7.md` (2,748 best 8-point circuits), `I/u-3.md` and `I/u-3-zletter/` (16-point circuits for Z),
`I/d-0-zeta/z8_p2_all.out`, `z8_p3_all.out` (all optimal 12-gate circuits for Z at 8 points modulo 2 and 3).

**First experiment.** Run the meter on every optimal Z circuit at 8 points, all three cuts: tabulate n(L), n(R), B, E.
Is E always N/2 (Yates) or can it be smaller with B > 0? Then decide on paper: is Yates optimal among circuits with B = 0.

**Growth law wanted.** With n(L) and n(R) each at least the cost at half size, the identity reads
cost(N) >= 2 cost(N/2) - B + E. So a forced E >= c N with B = 0 gives c N log2 N for that class of circuits, and a circuit
with E - B far below N/2 in one cut names the freedom a cheaper Z would use. State exactly which class of circuits your
recursion covers.

**Keep asking.** In which circuits can one gate do new work on both halves at once, and how many such gates can a Z-circuit
have? (For H, x-2 says a circuit below the floor needs about N/2 of them in every one of its N - 1 cuts.)

---

## 6. cancellation-literature: what is proved about Z and the cube with and without cancellation

**Idea.** Z is a well-known matrix under other names: the "T inside S" matrix, the disjointness or Sierpinski matrix,
Pascal's triangle modulo 2. Whether cancellation (subtraction, or coefficients) can beat adding-only circuits is a studied
question for exactly such matrices. One hour of reading may replace nights of search, in either direction.

**Special words.** *Adding-only (SUM) circuit*: gates u + v, every output a sum in which each input appears at most once.
*OR circuit*: the same with repetitions allowed. *XOR circuit*: over the two-element field. *Rectangle*: an all-ones
submatrix; adding-only cost is bounded below through the largest rectangles.

**Start from.** `C/wht33/research-2026-10-09/lenses/readers/lit-lower-bounds.md` (what is already on file),
`I/lit-constants.md`, `I/h-4.md` (zetafloor), `I/d-0.md`. To read on the web (names recalled by w-cross only: CHECK dates
and statements): Jukna and Sergeev, survey on the complexity of linear Boolean operators (2013); Find, Goos, Jarvisalo,
Kaski, Koivisto, Korhonen, "Separating OR, SUM and XOR circuits"; Kaski, Koivisto, Korhonen, "Fast monotone summation over
disjoint sets"; Bjorklund, Husfeldt, Kaski, Koivisto on the fast zeta transform; anything dated 2024 to 2026 on linear
circuits for Kronecker powers (Alman and co-authors).

**First experiment.** A one-page table: for Z, for the cube's neighbour sums A, and for H, the best known upper and lower
bounds in each model (adding-only, XOR, free coefficients, bounded coefficients), each with source, year and exact
statement. Then test the best construction found for Z at 16 points against Yates (32 gates) exactly.

**Growth law wanted.** The best known exponent or constant c in c N log N for Z with cancellation; any PROVED separation
between adding-only and cancelling circuits on a matrix of this kind; whether "Z in O(N) gates over the two-element field"
is a named open problem.

**Keep asking.** Where exactly does the known saving for Kronecker powers (below N log N by a constant factor) come from,
and is that source an identity of the whole class or special to one kernel?

---

## 7. chain-of-exchanges: arrays in a ring, each shear the end of one exchange and the start of the next

**One of the only two experiments of this wave aimed at the bar of 1e-1 (the other is brief 2).**

**Idea.** Two reports, never put together. x-3 (calls to a box, glue free): for the family "a box known only up to an
address map" the lower bound is 1.5 K calls against the textbook's 2K, and it would be met only by chains in which every
call is at once the second box for one piece of data and the first box for the next. x-6: an exchange cuts each array into
at least three blocks because every shear touches both arrays. Hybrid: put the arrays in a ring, array i exchanging with
array i + 1 along a port, so that one batched shear is the last shear of one exchange and the first of the next. If shears
are shared that way, the blocks per array could fall below three.

**Special words.** *Exchange*, *shear*, *batch*, *port*, *kappa*, *legal network*, *what-if count*: as in brief 2 (read its
word list). *Call program* (x-3): c_j = A (L_j x + sum over i < j of M_ji c_i), output = Q x + sum of P_j c_j; A is the box,
the fixed matrices L, M, P, Q are the *glue*. *Family*: the program must be right for every box of a given set.
*K*: the box acts on K points and the target is the box applied to rows and columns of a K x K table.

**Start from.** `I/x-3.md` (line 9 of its summary and the passage at lines 200 to 206), `I/x-3-boxrelations/perm7.py` (an
exact 7-call program at K = 4 for the six address maps; textbook 8, bound 6), `permbound.py`; `I/x-6.md` section 1 and 5,
`I/x-6-unitasbox/relation.py` (the exchange and the batch replayed at 16 addresses), `ports2.py`, `zlaw.py`;
`C/wht35/wider/w-engine/GAME.md` for what is legal.

**First experiment.** (a) Paper: a ring of n arrays, one port per neighbouring pair; write the word, count shears per
array and blocks per array as n grows; get rho and k and the saving by the price law. (b) K = 4 in x-3's exact setting: is
6 calls possible (modify `perm7.py`; exact fractions on all six maps). (c) h = 4 in x-6's setting: replay a ring of 3 and 4
arrays with `relation.py`'s machinery and find the first step where an unwanted term cannot be removed.

**Saving it could reveal.** Blocks per array below three at a skipped share rho: 0.1 needs (k, rho) = (2, 7.4 %). In x-3's
count, a < 2 calls per K at every size gives exponent log2 a: 1.5 K would be (log N)^0.585.

**Keep asking.** Where is the first place a legal network fails, and is that failure a property of the ring or of the
port? **At the end state plainly: was a LEGAL network of the engine found, or only a what-if count.**

---

## 8. the transform in a row: read the addresses as the whole numbers 0 to N - 1

**Idea (it sounds like changing the problem; try it anyway).** On the cube no three points lie on a line, and x-1 says that
is why a helper wire serves only one output from the third digit on. On a ROW of N points three points do lie on a line,
and there x-1's trick works: a polynomial of degree 2 at N points costs N + 1 gates, not 2N, one helper serving about N/2
gates (`I/x-1.md` section 5, `conic.py`). By Lucas' theorem Z is Pascal's triangle modulo 2: entry (s, t) is "s choose t"
modulo 2. So take the TRUE Pascal matrix P (entries s choose t, whole numbers), which lives on the row, and ask how far
P D' P^T is from H.

**Special words.** *Pascal matrix* P: N x N, entry C(s, t). *Shift by 1*: P is the matrix of "replace the polynomial p(x) by
p(x + 1)" in the basis of binomials, so it is cheap in the right basis and all its cost is the change of basis. *D'*: a
diagonal of powers of -2, either (-2)^t or (-2)^(number of ones of t).

**Start from.** `I/x-1.md` sections 5 and 9 and `I/x-1-digits/` (digits of H; circuits right modulo 2^(d+1)),
`I/d-0-zeta/mincirc`, `I/j-machine/slp.py`, `I/w-cross/hyb4b.py` (walk over whole-number bases V with V D V^T = H).

**First experiment.** Exact, 8, 16, 32 points: P D' P^T for both D'; its difference from H modulo 4, 8, 16; the rank of the
difference. The cheapest circuit for P and for its low columns by the one-helper trick. Then: is there a whole-number
matrix that is Z modulo 2, cheap in a row, and equal to Z modulo 4 or 8 (so that the correction is a small or sparse map)?

**Growth law wanted.** Gates for such a matrix as a function of N (N + O(1) per column family would be the surprise), and
the cost of the correction back to Z as a function of the power of 2 to which they agree.

**Keep asking.** Which whole-number lifts of "Z modulo 2" exist besides Z itself, and is any of them cheap for a reason
the cube cannot see?

---

## 9. reconcile-caps: three ceilings for the engine's own mechanism, one table, one verdict

**Idea.** Three numbers for what the engine's mechanism can reach do not agree: the avenues study (about 3e-3 for present
labels; 1.7e-2 to 2.5e-2 for "fat labels") and x-6 (0.028 to 0.12 for fat ports; 0.078 for scatters of the published kind;
0.098 and 0.147 with further idealisations). The bar is 1e-1. My reading in this box [read + derived, unchecked]: the two
studies compute the SAME formula and differ only in which costs they set to zero. The developer's job is to confirm or
break that reading line by line, and to answer: is 1e-1 by this mechanism excluded, open on paper, or open in a way one
could search; and if searchable, name the smallest exact search that decides it.

**Words, with the dictionary between the two studies** [my identification; check it first].
*Label* (avenues) = *port* (x-6): the subspace of a pair's h-bit block along which its source does not move inside an
invocation; *thin* = dimension 1, *fat* = dimension a (avenues) = r (x-6). *Class (h, a)*: width h, label dimension a.
*Stages* s: 3 for the plain exchange, 5 for the bridged word of the published unit; m = s x h. *Copy* = *total*: a sum of
sources in a scratch array, brought down h moves; *cst* = moves spent on copies (72 for E8 = 8 totals x 9; argued floor
55). *Loss* (avenues) = cst; *loss ratio* = loss / (a v) = h / (kappa r) in x-6's letters, since cst = (v / kappa) x h
[derived by me]. Check: E8 has 9 / 15 = 0.6, which is the "ratio 0.6 (what thin E8 has)" of k-levers. Both studies give the
same thresholds for any gain at all: ratio below 2/3 (three stages) or 0.8 (five stages). *Helper*: non-data array, charged
all its moves (E8: 783 for 480 data arrays, 6.5 per pair; argued floors 0.31 to 0.97 per pair). *Bank* / *idle climbs*:
the blocks a data array makes in the stages where it is not active; published: two blocks per array per idle stage;
"merged": one, which no design is known to allow.

**The table to verify and complete** (every row from the files named; "0" = the cost is ignored).

| saving | who | (h, r) | stages | loss ratio | helpers per pair | data-array blocks | rests on / contradicted by |
|---|---|---|---|---|---|---|---|
| 8.7625e-4 | published [Lean] | (9, 1) | 5 | 0.6 | 6.5 | as certified (16.5 blocks per array) | nothing: it is the fact |
| 2.8e-3 to 3.6e-3 | k-levers | (9, 1) | 5 | 0.46 (cst 55 for 120 shears; my arithmetic, confirm which cst that row used) | 0.31 to 0.97 (argued floors nobody is near) | as published | floors argued by one agent |
| 3.51e-3 | x-6 what-if | (9, 1) | 5 | 0 | 6.5 | as published | copies >= 55 argued, so not reachable |
| 1.31e-2, 1.58e-2 | x-6 what-if | (9, 1) | 5 | 0 | 0 | as cut / one block per stage | same; v-levers "R 0, cst 0" gives 1.6e-2 to 2.0e-2: agreement |
| 1.7e-2 to 2.5e-2 | k-levers | (6, 3) | 3 or 5 | 0.5144 (a table floor, no family) | 1 or 0 | two idle blocks | no fat family is known with ratio below 1; x-6 says kappa <= 2 at r = h/2, that is ratio >= 1 |
| 7.3e-3 to 8.8e-3 | k-levers | (6, 3) | 3 or 5 | 0.5144 | 6.5 | two idle blocks | the same |
| 0.028 to 0.078 | x-6 what-if | r/h = 0.2 to 0.5 | 5 | 0 | 0 | one block per stage | v-levers "formula corner" 0.075 to 0.086 at (8, 4): agreement |
| 0.049 to 0.120 | x-6 what-if | r/h = 0.2 to 0.5 | 3 | 0 | 0 | one block per stage | v-levers 0.107 to 0.120: agreement; r = h/2 dead (kappa <= 2) |
| 0.078 (0.048 five-stage) | x-6 | r = h/3 | 3 | 0 | 0 | one block per stage | symmetric scatters with M M = kappa M need r <= h/3 |
| 0.098 | x-6 | r = h/3 | 3 | 0 | 0 | three blocks h - r, h, h per array ("merged", a word nobody has) | the same, plus the missing word |
| 0.147 | x-6 | r = h/2 | 3 | 0 | 0 | merged | dead: kappa <= 2 |
| 0.107 (3 arrays in 8 moves, block size 3) | avenues, tiny unit | none | none | none | none | none | a DIFFERENT mechanism; excluded without address maps by the cut-set lemma (cutf3: k >= 3 W); open in the full game |

Note the two different "0.078": five stages at r = h/2, and three stages at r = h/3.

**What would all have to come true for 1e-1** [read: x-6 lines 259 to 262; the list is mine]: (i) ports with r/h >= 0.42
(three stages) or >= 0.34 (merged blocks); (ii) at that r a scatter with loss ratio near 0, that is kappa very large,
while x-6 argues kappa <= 2 at r = h/2 and the avenues' floors give ratio >= 0.835 at (4, 2), exactly 1 for spread
families at every h = 2a, no gain possible in (5, 3); (iii) no helpers at all (published 6.5 per pair); (iv) every data
array one whole block per stage; (v) for 0.098 and above, the merged word; (vi) the Lean engine accepting fat labels at
all (open, fat/NOTE.md lines 101 to 104). The tension to settle first: (i) asks for LARGE r/h and (ii) for LARGE kappa, and
the number of ports a fat port knows falls as r/h rises (1 at r = h/2; 4 at (5, 2) [ran by x-6]).

**Start from.** `C/wht37/avenues/NOTE.md`, `v-levers.md` (section 3 and avenue 3, lines 96 to 110 and 166 to 196),
`k-levers.md` (points 5 and 6, lines 98 to 115), their programs in `C/wht37/avenues/v-levers/` and `k-levers/`
(`whatif.py`, `whatif2.py`, `k.py`), `C/wht35/fat-classes/NOTE.md`, `C/wht35/fat/NOTE.md`; `I/x-6.md` sections 5 and 6,
`I/x-6-unitasbox/zlaw.py`, `ports2.py`, `e8m.py`; `C/wht38/tiny/next/cutf3.md`, `C/wht38/tiny/filter/joint/NOTE.md`;
`R/tools/whatif_copies.py`.

**First experiment** (the smallest exact search I can name [derived, unchecked]). The number of totals is at least the
largest set of ports no two of which know each other (on such a set the scatter matrix is the identity), so
kappa <= v / (that number) for every sub-family; E8 meets this with equality (120 / 8 = 15). For each (h, r) with
0.3 <= r/h < 0.5 and h <= 9, that is (5, 2), (6, 2), (7, 3), (8, 3), (9, 3), (9, 4): build the knows graph on the fat ports
(P_s inside P_t-perp), compute exactly its degree and the largest ratio (size of a sub-family) / (largest subset with no
two knowing each other) (a fractional-colouring linear program, or the independence number when the graph is
vertex-transitive), turn it into the least loss ratio h / (kappa r), and put THAT cost of copies, with helpers still 0,
into `zlaw.root`. If the best figure over all six classes is below 1e-1 the mechanism is excluded within x-6's design
(sources summed at the top, unwanted terms removed only for known sources) and only x-6's hatch "partial knowledge"
(mutation 3) is left; if some class passes, that class is the search target for briefs 2 and 7.

**Saving at stake.** 1e-1, yes or no, for the only mechanism that has ever changed the order.

**Keep asking.** Which single idealisation carries most of the gap between 2.5e-2 and 0.12, and is it one that something
proved or computed tonight already contradicts? Do the avenues' labels have to meet their perpendicular only in 0, as
x-6's ports do, or is the avenues' class of labels wider (then x-6's "kappa <= 2" does not cover it)?
