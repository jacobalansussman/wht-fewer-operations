# wht39 / ideas / WAVE5-PICKS: nine briefs for an hour each

2026-10-11, about 00:10 EDT, 15-minute box, curator `q-pick`. Private research: nothing published, no git, no Lean.
I ran nothing. Marks: [read] = read tonight in the file named; [derived] = by hand tonight by me, checked by nobody; [guess].
Counts: **(G)** a gate is any a*u + b*v, scalings free; **(O)** OpenAI's count, additions and scalar multiplications each
charged. Every number below is (G) unless a line says (O).
Read in full: `k-cross.md`, `WAVE4-PICKS.md`. Read in part: `g-6.md` sections 3 and 4, `g-0.md` section 4, the passages of
`g-1.md`, `g-3.md`, `g-4.md`, `g-5.md`, `e2-0.md` that the experiments start from, the heads of the programs in `k-cross/`,
the file listings of the g-, e2-0-, d-0- and h-folders. Not landed when I wrote: every `h-*.md`, `c-*.md`, `WAVE3-NOTE.md`,
`b-1.md`, `WAVE2-NOTE.md`. Curator, not critic: nothing is ranked, nothing is thrown away.

The nine are the experiments of `k-cross.md` section 6. None repeats a wave-4 brief word for word, so all nine are kept.
Three had to be re-aimed because a wave-4 developer is already standing on part of the ground (note 3). The ninth,
`fibonacci`, is k-cross's "sillier one", taken seriously; k-cross's other silly one ("divide by zero on purpose") is folded
into brief 5 because both need the same symbolic solve.

I = `waves`.   R = the release tree (READ ONLY).

## Notes for all nine developers

1. **Words.** N = 2^k points. *The transform*: the Walsh-Hadamard matrix H, entries 1 and -1. *Kernel*: a 2 x 2 matrix; its
   *power* is the Kronecker product of k copies (H is the power of [[1,1],[1,-1]]). *The class*: the powers of all invertible
   kernels that are not relabellings with scalings. *Textbook*: N log2 N gates (8, 24, 64, 160, 384 at 4 to 64 points).
   *Merge tree*: start from the N inputs and repeatedly replace two held sums by one weighted sum; N - 1 gates; its *nodes*
   are the sets of inputs under each sum (2N - 1 of them, the single inputs included). *Rectangle*: a set of rows times a set
   of columns with one number on it, zero elsewhere. *Tree rectangle*: row set a node of one tree, column set a node of another.
   *tau*: the number of tree rectangles whose sum is the matrix (after rescaling rows and columns).
2. **The one formula of this wave** [read: k-cross 1 A]. A matrix that is a sum of tau tree rectangles over two merge trees
   costs **N - 2 + tau** gates. [derived, mine] Over two forests of f trees each it costs N - 2f + tau (a layer of four 4-point
   bricks at 16 points: 16 - 8 + 20 = 28). In this count the textbook is tau = N log2 N - N + 2, that is **6, 18, 50, 130, 322**
   at 4 to 64 points; the best known are **5** (the 7-gate brick) and **13** (g-1's 19 gates); e2-0's 52 gates at 16 points
   would be 38 if that circuit has this form (nobody has checked). **Linear size is exactly "tau at most c * N".**
3. **What wave 4 is already doing** [read: listings of `I/h-6-classhub/`, `I/h-4-zetafloor/`]. `h-6-classhub` has `gen_tau.py`
   (the staircase for kernels [[1,1],[1,tau]]), `solve19.py` and `k19_tau_*.txt` (g-1's 19 carried to other tau), `limit.py`.
   `h-4-zetafloor` has an annealer and `rows_zeta4.txt` (subset sums at 16 points). Briefs 1, 5 and 6 below start from those
   folders and from `h-6-*.md`, `h-4-*.md` if they have landed; they do not redo them.
4. **The user cares about the ORDER, not constants.** A record at one size is not news. News is a quantity that, followed in
   k, bends: tau(k)/2^k staying bounded, gates/(N log2 N) still falling at the largest size you can reach, the largest size
   that s steps can make growing faster than 4^s. Every brief names its growth law; report the sequence even when it is ugly.
5. **Tools.** `I/k-cross/`: `hyb3.py` (full exact test "does this rectangle shape exist for this kernel", all 8! wirings),
   `hyb4.py` (writes and replays the 19-gate circuit for a kernel, exact fractions), `class19.txt` (seven circuits),
   `rect.py`, `rect2.py` (fewest rectangles for one design by an integer programme, scipy HiGHS, **floating point: candidates
   only**; about a minute per 16-point design on the Linux machine), `hyb.py`, `hyb2.py` (rank lemma, mirror ranks).
   `I/d-0-zeta/mincirc.c`, `mincirc_all.c` (exhaustive minimum circuits over GF(p), 8 wires for p = 3, 5, 7).
   `I/g-1-tightwires/exact8.py` (exact minimum of the one-centre model at 8 points), `h8_19gates.txt`.
   A circuit found modulo a prime or by a float solver is a candidate until replayed exactly. "None modulo p" is not "none".
6. Generation first, play second, criticism last. Mark every statement. Explain a term before using it.

---

## Brief 1. `classtest`: is there any saving that belongs to the transform alone?

**From.** `k-cross.md` section 4 and section 6 item 1; section 3 hybrid 2.
**The idea, in my words.** Three waves looked for what is special about the transform. The two circuits that actually save
gates (7 at 4 points, 19 at 8) turned out to work, wire for wire, for the powers of every kernel tried, even [[1,2],[3,4]].
If EVERY saving is of that kind, the special structure (signs, reflection, eigenvectors) is decoration, and the hunt for
linear size may move to whichever member of the class is easiest. If ONE saving exists only for the transform, that is the
first thing the special structure has ever bought. Either answer redirects the night.
**Objects.** `I/e2-0-pieces/slp_8.txt`, `slp_16.txt` (20 and 52 gates, the 3/4 family; `e2-0.md` section 3 for the mixed-hub
lemma: a hub that holds one character on one half and its other extension on the other half); `I/g-5-k3/brick12.py`
(12 gates for K3 (x) H2, a 3-point kernel times a 2-point one); `I/k-cross/hyb3.py`, `hyb4.py` as templates;
`I/h-6-classhub/gen_tau.py`, `gen_tau.out` (wave 4 has started the symmetric one-parameter case [[1,1],[1,tau]]);
`I/d-0-zeta/mincirc_all.c` and its outputs (ALL optimal circuits, not one).
**First experiment.** (a) Read what `h-6` already settled for 20 and 52 with tau = 2, 1/3. Then do what it does not:
NON-symmetric kernels ([[1,2],[3,4]], [[2,7],[5,3]], [[1,100],[1,1]]). Keep each wiring, free every coefficient, necessary
conditions on supports first, then one exact linear solve; replay with fractions. (b) The converse, which nobody has run:
enumerate ALL 7-gate circuits for the 4-point transform over GF(5) and GF(7) with `mincirc_all`, sort them by wiring shape,
and test every shape on a generic kernel. A shape that exists at [[1,1],[1,-1]] and at no generic kernel is the object
sought. Then the same at 8 points on the shapes in `I/g-1-tightwires/sa8_known*.out` and the two 21-gate circuits
(`I/e2-3-drain/h8_21gates_drain.txt`). (c) g-5's 12 for a generic 3 x 3 kernel times a generic 2 x 2 one.
**Growth law.** For each kernel K, the rate r_K(k) = gates / (N log2 N) of the staircase at k = 2..6 (for the transform:
0.875, 0.833, 0.8125, 0.80, 0.79, limit 3/4) and the size of the largest coefficient at each k. News is a kernel whose
rate curve falls FASTER than the transform's, or whose coefficients must grow with k (then the bounded-coefficient wall
does not apply to it); a table where all kernels agree to the gate is the class law, and says so.
**The question to keep asking.** What is the smallest statement about 2 x 2 matrices that a saving uses? (The brick uses
"k (x) k = rank one + det * signed swap".) If every saving is such a statement, what is the list of ALL such statements at
third and fourth powers, and is the list finite?

## Brief 2. `letter16`: one letter at 16 points, outside the family that gave 49

**From.** `k-cross.md` section 3 hybrid 1 and section 6 item 2; `g-1.md` sections 4 to 6.
**The idea.** Write the 16-point transform as few tree rectangles (note 2). k-cross ran two designs, both with a "bent"
centre (a sign vector whose transform is again a sign vector) and with the two trees made of cosets of a chain of subgroups
and of the chain of perpendicular subgroups. Both gave exactly 49 rectangles, 63 gates, and both needed 16 single cells
with the number +4 to repair places covered twice. At 8 points nothing is covered twice. The repairs are where this
family starts to lose; a design without them would sit at 33 rectangles, 47 gates, under the record 52.
**Objects.** `I/k-cross/rect2.py` (the tool; edit `designs`), `rect2.out` (the two lists of 49 rectangles), `rect.py`
(the sweep and its weak proxy); `I/g-1-tightwires/fwq16.py`, `fw4_quad.out`, `fw4_any.out` (g-1's 869 designs, best 63).
**First experiment.** Leave the family in four directions, a few designs each, on the Linux machine: (a) centres that are
not bent (three-valued transform; then the output scalings are not signs: free them); (b) output sign vectors that are not
the centre's transform; (c) chains perpendicular at some levels only; (d) trees that are NOT chains of subgroups (a node of
3, 5, 6 points; caterpillars). Before any solver run, apply the rank lemma of k-cross 1 B (rank of the block on a row node
and a column node is at most 2 + rectangles strictly inside) as a filter. Also raise the bound on the numbers from 4 to 64:
the Potts matrix reaches N + 1 rectangles only with a number of size N. Replay every candidate exactly.
**Growth law.** In the family run so far the rectangles per point, (tau - 1)/N, are 1, 1.5, 3 at 4, 8, 16 points: faster
than log N, so that family dies. Report the same three-term sequence for every new family; news is a family where
(tau - 1)/N grows by a constant per step or less (1, 1.5, 2 is already 1/2 N log N), and above all one where the number
of repair cells per point does not grow.
**The question to keep asking.** Why do the rectangles tile at 8 points and overlap at 16? k-cross says tau - 1 is "the
fewest tree rectangles tiling the set where a quadratic form of x + Ly equals 1": is the overlap forced by the quadratic
form having rank 4, and is there a centre of a different kind (cubic, or not a function of a form at all) whose set tiles?

## Brief 3. `mirror64class`: the mirror route on the one member where the obstruction is absent

**From.** `k-cross.md` section 3 hybrid 3 and section 6 item 3; `g-0.md` sections 2 to 5 and its last mutation.
**The idea.** Every kernel power, times a suitable relabelling with scalings, is "identity minus twice a projection" onto a
space of dimension (N - sqrt N)/2, the *mirror* (1, 6, 28 at 4, 16, 64 points). Computing the transform = reading the
mirror coordinates and writing them back. g-0 proved this route ties 56 at 16 points for the transform, and the reason was
one fact: no two of the 16 mirror points are perpendicular, so reading cheaply and writing cheaply exclude each other.
k-cross found that this fact fails for exactly one member, the subset-sum kernel [[1,1],[1,0]]: there 7 of 16, 167 of 256,
3,319 of 4,096 entries of the mirror matrix are zero. Nobody has run g-0's search on that member.
**Objects.** `I/g-0-mirror/search.c` (reduced model: 16 target points, 30 helper points, "a point on a line through two
present points may be added"; it is written for the transform's point set and must be rebuilt for the new one), `model.py`,
`tables.txt`, `replay16.py`; `I/k-cross/hyb.py` parts 2 and 3 and `hyb2.py` parts B and C (they build the mirror matrix
for any kernel and count its zeros); `I/d-0-zeta/rows_zeta*.txt`, `I/h-4-zetafloor/rows_zeta4.txt`.
**First experiment.** (a) Build the mirror of the subset-sum power at 16 points exactly: the 16 points, which pairs are
perpendicular, the short linear relations among them. (b) Cheapest basis of that mirror (count helpers as g-0 did), then
the cheapest read-and-write, against that kernel's textbook 32 and k-cross's rough floor 36. (c) At 64 points the textbook
is 192: use the perpendicular pairs to split the mirror into pieces that are read and written separately, and count.
(d) Same for [[1,1],[1,2]] and for a kernel with a zero in another place.
**Growth law.** [derived, mine, from k-cross's three figures] the mirror matrix has 9, 89, 777 non-zeros at 4, 16, 64 points:
2.25, 5.6, 12.1 per row, roughly N^0.6 per row, so it gets sparse fast. The law to report is (cost of read-and-write) /
((N/2) log2 N) at 4, 16, 64 and by recursion 256; news is that ratio falling from one size to the next, because a mirror
that is sparse AND nearly orthogonal can be applied directly at about its number of non-zeros.
**The question to keep asking.** g-0's tie came from one geometric fact. Which member of the class has the MOST
perpendicular pairs of mirror points, and is the count of such pairs a quantity one can push through the three-call word
between subset sums and the transform (`g-4.md`) without losing it?

## Brief 4. `hatch32`: decide the one case that g-6's floor leaves exactly tight

**From.** `k-cross.md` section 1 C and section 6 item 4; `g-6.md` sections 3, 4 and mutation 1; `g-3.md` section 6.
**The idea.** A *tree step* (g-3 says *tree letter*) is a matrix that costs a linear number of gates because every block
between sibling nodes of one tree has rank one. Butterfly layers and brick layers are tree steps, so k/2 steps always
suffice; a BOUNDED number of steps at every size would be linear size. g-6 argued that two steps of the "periodic" shape
cannot make the transform from 64 points on, and found that at 32 points, shape 8 x 4, the count comes out 12 exceptions
needed against 12 available. A tie in a counting argument is either a last coincidence or a construction. g-6 could not
decide; g-3 met the same open case from the other side ("two letters at 32 points").
**Objects.** `g-6.md` lines 113 to 172 (the block law, the exception count, and the paragraph "The 8 x 4 hatch at 32 points,
fully specified": each of the 4 blocks of the first step has one column of kind E1 and two free columns of kind E2, each
of the 8 blocks of the second step is used once, the tree inside an 8-point block is caterpillar-like with leaf pairs in
different directions); `I/g-6-twosteps/emin8.py` (exhaustive tree and exception search at 8 points), `nu.py`, `quad.py`,
`deep.py`, `lemmaB_check.py`; `I/g-3-illconditioned/treeexact.py`, `treejac.py`, `treeword.py`.
**First experiment.** (a) Enumerate the combinatorial skeletons the paragraph allows (tree on 8 leaves, which column is E1,
which two are E2, the matching of 32 middle wires), cut down by symmetry. (b) For each skeleton the unknowns are scalings:
polynomial equations; solve modulo two large primes with an analytic Jacobian (Newton over GF(p)), lift, replay exactly.
Filter first with k-cross's rank lemma and g-6's test nu <= 4. (c) If every skeleton is empty, write down which equation
kills it; then the shape 16 x 2, which the count does not exclude either. (d) Drop hypothesis (G) ("every block meets
every block in one middle wire") and see what the count becomes.
**Growth law.** Let N(s) be the largest size that s tree steps can make. Bricks give N(s) = 4^s, which is N log N. The
whole question of order is the growth of N(s): if N(2) = 16 and N(3) = 64 the law is 4^s and this door is shut for
periodic shapes; N(2) = 32 breaks the pattern at its first term, and then N(3) (g-6 section 5) is the number to get,
because N(s) growing like 2^(s^2) would already be N sqrt(log N), a saving of 1/2.
**The question to keep asking.** g-6's anomaly: the pair of quadric sets {x0 x1 + x2 = 0}, {y1 y3 + y4 = 0} passes the
two-step test at 32 points without being periodic, and fails by a growing margin after (nu = N/8). Is there a shape
between "periodic" and "quadric" whose margin does not grow?

## Brief 5. `formula`: the rule in k behind the class identity, and where its constants vanish

**From.** `k-cross.md` section 6 items 5 and 9 ("divide by zero on purpose"), section 3 hybrid 2, section 1 E.
**The idea.** At k = 2 the saving is one line of algebra: for a kernel with entries a, b, c, d, the square k (x) k is a
rank-one matrix plus det(k) times a signed swap; 5 rectangles. At k = 3 there are 13 rectangles and the same wiring works
for every kernel tried, with constants that depend on the kernel (for [[1,2],[2,1]]: 2, 4, 8, 3, 6, 3/4). Nobody knows
the identity behind k = 3. If it is the k = 2 identity applied in a pattern, the pattern has a k = 4 term and a k-th
term, and the count of rectangles in that term is a growth law obtained by algebra, not by search.
**Objects.** `I/k-cross/class19.txt` (seven circuits), `hyb4.py` (the linear solve that produces the twelve constants),
`hyb3.py` (the 13 rectangles as `terms`, the 288 placements); `I/h-6-classhub/solve19.py`, `k19_tau_*.txt`, `limit.py`
(wave 4, the symmetric one-parameter case: read its report first); `I/g-3-illconditioned/brick.py`.
**First experiment.** (a) Redo `hyb4.py`'s solve with a, b, c, d as symbols (sympy, or exact interpolation from many
rational kernels): the twelve constants and the scalings as rational functions; factor them. (b) Read the 13 rectangles as
a pattern over the three address bits: which are "the k = 2 identity on bits 1,2 inside a block of bit 3", which are new.
Write H_8 = (rank one) + sum, and try to DERIVE it by applying the k = 2 identity twice. (c) Guess the k = 4 pattern from
it, count its rectangles, test it exactly on three kernels. (d) Divide by zero: on the zero set of each constant a gate
drops (18 or fewer for that kernel's cube); list those kernels; is any of them equivalent to the transform, or to a kernel
with no zero entry, for this placement or another of the 288? Where a constant blows up, what does the circuit become?
**Growth law.** The sequence tau_class(k) of the rule: 5, 13, then whatever the pattern gives at k = 4, 5, 6 (50, 130, 322
is the textbook). News is tau_class(k)/2^k growing slower than k, or the saving tau_textbook - tau_class (1, 5, ...)
growing faster than N; also the degree of the constants as polynomials in the kernel's entries as a function of k, since
degree growing with k is the "large coefficients" that the bounded-coefficient wall cannot see.
**The question to keep asking.** Cayley-Hamilton gave k = 2 (a 2 x 2 matrix of trace zero squares to a number). What is the
statement about THREE copies? The third power of a kernel splits into symmetry types under permuting the copies (the
fully symmetric part has dimension 4, two copies of a 2-dimensional type); do the 13 rectangles respect that splitting?

## Brief 6. `unimodular`: the member of the class with no determinant floor

**From.** `k-cross.md` section 4 (second half) and section 6 item 6; `g-4.md` section 6.3; `d-0.md`.
**The idea.** Every proved N log N floor for bounded coefficients counts volume: the transform has determinant N^(N/2) and
a gate with small coefficients can only multiply volume by a constant. The kernel K = [[1,1],[1,2]] (= Z Z^T, Z the
subset-sum kernel) has determinant 1 and no zero entry, so for its powers that count says nothing at all; g-4's
finer count by singular values gives only N sqrt(log N) for Z. So here is a member of the class, with integer entries
and small coefficients, where NOTHING proved forces N log N. Either a cheap bounded family exists for it, or a new kind
of floor does; both would be new.
**Objects.** `I/d-0-zeta/mincirc.c`, `rows.py` (makes row files for a target), `rows_zeta2.txt`, `rows_zeta3.txt`;
`I/g-4-zetalead/fields.py` part D and `g-4.md` lines 240 to 272 (the singular-value floor Z_bc(N) >= N (0.277 sqrt(k) - 1)
and the remark that upper and lower bound would meet at N sqrt(log N) given a cheap change to the "Schur basis");
`I/h-4-zetafloor/` (wave 4 on Z itself: annealer, `lemmas.py`); `I/k-cross/hyb4.py` (the 19 for any kernel).
**First experiment.** (a) Exact minimum for K (x) K (4 points) and K (x) K (x) K (8 points) with coefficients +1, -1 only,
then with 2 allowed, then free modulo 5 and 7; textbook is 8 and 24 (two gates per 2 x 2 block), k-cross's class identity
gives at most 7 and 19 with some coefficients: are those coefficients bounded for THIS kernel? (b) g-4's singular-value
floor for the powers of K: K's singular values are the squares of Z's; compute the bound as a function of k exactly as
`fields.py` does. (c) Push a circuit for K's power to the transform and back through g-4's word (subset sums = three calls
and four diagonals): which direction keeps coefficients bounded? (d) [[2,1],[1,1]] and the Fibonacci-like [[1,1],[1,0]]^2.
**Growth law.** Two sequences in k: the proved floor for K's powers divided by N (expected like sqrt(k), [guess]) and the
best bounded-coefficient count divided by N (textbook: k). News is the second one bending below c * k at k = 3, 4, 5, or a
construction at N * k^(1/2) for all k: that would be the order N sqrt(log N) for a member of the class, a saving of 1/2,
and the next question would be the price of carrying it to the transform.
**The question to keep asking.** If the volume is not there to be paid for, what else does a circuit for K's power have to
"make"? Name a quantity (rank of sub-blocks, spread of a wire on both sides, number of distinct partial sums) that grows
like N log N for K and that one gate can raise only by a constant; or find the circuit that shows there is none.

## Brief 7. `selftranspose`: one tree, used forwards and backwards, with a matching in the middle

**From.** `k-cross.md` section 6 item 7 and section 1 A; `e-1.md` (the transposition principle: running a linear circuit
backwards computes the transposed matrix at the same cost up to N' - N gates).
**The idea.** The transform is symmetric. If H = F^T M F, where F computes N' linear forms from the inputs with c gates and
M only pairs those forms up (a relabelling with scalings), then the transform costs 2c + N' - N: F forwards, M free, F
backwards. The 7-gate brick is this with F = (the four inputs and their sum), c = 3, N' = 5. In words: the quadratic form
x^T H x is a sum of squares of forms and products of disjoint pairs of forms, all taken from one cheap family.
[derived, mine] If F is a merge tree, c = N - 1 and N' <= 2N - 1, so ANY such identity costs at most 3N - 3 gates: it
would be linear size on the spot. So for merge trees it must fail at some size (or the order is linear), and the size
and the reason of the first failure are what this brief is after.
**Objects.** k-cross's 13 rectangles (`I/k-cross/hyb3.py`, `terms`) and g-1's two trees (they are DIFFERENT trees, each the
chain of perpendiculars of the other: k-cross 1 B says one letter needs that); `I/g-1-tightwires/h8_19gates.txt`;
the symmetric versions of the transform: H itself, and H times a signed relabelling P with H P symmetric (the brick uses
one: k-cross 1 E).
**First experiment.** (a) 4 points: list every merge tree F and every matching M with H or H P = F^T M F; is the brick the
only one? (b) 8 points, the exact linear-algebra test k-cross describes: for every merge tree on 8 leaves (up to symmetry),
every admissible P, and every matching on at most 12 of its 15 forms, is x^T (H P) x in the span? Twelve gives 18 gates,
below the 19. A matching on all 15 would be 21, on 13 it is 19 again. Record the least N' per tree. (c) If trees fail,
let F be a tree plus a few extra gates (c = 8, 9) and repeat: record the least c for which some matching exists.
(d) Explain by a parameter count why the two trees of the 19 cannot be made equal.
**Growth law.** The least cost c_min(k) of a family F whose forms, squared and paired, give the transform: 3 at 4 points
(c/N = 0.75). News is c_min(k)/N staying bounded at k = 3 and 4; if instead c_min grows like (N/2) log2 N the route is the
conjugation wall L1 again ("half a transform each way") and the report should say that it is.
**The question to keep asking.** A matching uses each form once. The brick's hub is used once, as a square. What is the
largest number of DISJOINT pairs of nodes of one tree whose products can appear in x^T H x at all, and does that number
grow like N or like sqrt N?

## Brief 8. `twoletters`: the transform as a product of two sparse rectangle forms

**From.** `k-cross.md` section 6 item 8, section 1 B and C; `g-6.md` section 3 (Lemma A); `g-3.md` section 6.
**The idea.** One letter (one sum of tree rectangles) cannot be linear when the numbers are bounded, and k-cross found 49
rectangles at 16 points for the designs it tried. Two brick layers are two letters with 20 rectangles each (56 gates).
Between them lies an unexplored space: H_16 = L1 L2 where each factor is a sum of rectangles over its OWN pair of trees
(or forests), with a sparse middle and not a diagonal one. g-3's letters, g-6's steps and g-1's walk are three corners of
this one space. The middle index set need not have 16 elements: a factor may be 16 x 20, which is the "extra value" that
every saving so far has needed (k-cross 1 G).
**Objects.** `I/k-cross/rect2.py` (one letter; the constraint is linear in the numbers once the trees are fixed);
`I/g-6-twosteps/nu.py`, `tight.py`, `grid.py`, `deep.py` (g-6's test: for row node S and column node U a quantity nu,
computed from ranks of four blocks of H, must be at most 4 for two rank-one steps); `I/g-3-illconditioned/treeword.py`
(a float search that failed as a tool: read why in `g-3.md` section 6 before reusing it); `I/e2-0-pieces/slp_16.txt`.
**First experiment.** (a) Write e2-0's 52-gate circuit and the 54-gate tensored 19 as products of rectangle forms: how many
letters, how many rectangles each, what are the middle sets? That gives the search a known point that is not bricks.
(b) Fix L1's trees (forests of 4-point and 8-point pieces), solve for L2 = L1^(-1) H when L1 is square, and count L2's
rectangles with `rect2.py`'s programme; alternate (fix L2, improve L1). (c) Use g-6's nu and k-cross's rank lemma to
discard tree pairs before any solve. (d) Rectangular middles: 16 x 17 up to 16 x 24.
**Growth law.** With L letters allowed, the least total number of rectangles T_L(k). Bricks: T = (k/2)(5N/4) with L = k/2.
News is T_2(k)/N staying bounded from k = 4 to k = 5 (it cannot for one letter with bounded numbers), or, more modestly,
the middle width growing while the total falls; report T_2 at 16 and 32 points and the middle width at the optimum.
**The question to keep asking.** In a product of two letters the middle wires are neither inputs nor outputs. What must a
middle wire look like, in both languages at once (as a sum of inputs, as a combination of outputs), for both factors to
have large rectangles? k-cross 1 D says a linear count needs rectangles of average area of order N.

## Brief 9. `fibonacci`: two data points fit a linear law; get the third   (the silly one, taken seriously)

**From.** `k-cross.md` section 6, last lines ("5 and 13 are Fibonacci numbers and 16 points should give 34; the run says 49
for two designs"), section 1 B and D, section 3 hybrids 1 and 4.
**The idea.** The fewest tree rectangles known are 5 at 4 points and 13 at 8. Two terms fit anything. [derived, mine] They
fit **tau = 2N - 3** (5, 13, 29, 61: gates 3N - 5 = 7, 19, 43, 91, which is LINEAR SIZE); they fit every second Fibonacci
number (5, 13, 34, 89, 233: gates 48, 119, 295 at 16, 32, 64 points, under the records 52, 128, 304, but growing like
2.618^k, so worse than the 3/4 family from 256 points and worse than the textbook from 512); they fit "textbook minus 1, minus 5" (6 - 1, 18 - 5, 50 - ?). The third term separates the
three laws, and 49 was measured on two designs of one family with numbers bounded by 4. [derived, mine, a few lines,
unchecked] k-cross's rank lemma does NOT exclude a linear tau: rectangles strictly inside a quarter block are also
strictly inside a half block, so the lemma's bounds at different levels do not add; it gives about N - 8, no more. The
only thing that forces N log N rectangles tonight is boundedness of the numbers.
**Objects.** `I/k-cross/hyb.py` part 1 (5 and 13 written out), `rect.py`, `rect2.py`, `rect2.out`;
`I/g-1-tightwires/exact8.py` (13 is the exact minimum only inside the one-centre, subgroup-chain model);
`I/g-3-illconditioned/potts.py` (the one flat matrix with N + 1 rectangles, using a number of size N).
**First experiment.** (a) Is 13 the true tau at 8 points over ALL pairs of merge trees, ALL row and column scalings and
unbounded numbers? Trees on 8 leaves up to symmetry are few; for each pair the problem is "fewest columns of a fixed
dictionary that span a target" once the scalings are fixed, and the scalings are few after normalising: do it exactly
(rank tests modulo a prime, then lift), not with the float solver. 12 or fewer is 18 gates. (b) How do the 13 contain
the 5: restrict the 13 rectangles to each half of the inputs and outputs and see which rectangles are "the 4-point
picture twice" and which are new; write the substitution rule (each rectangle of step k becomes which rectangles of step
k + 1); iterate it once and count. (c) Ask each candidate law what its 29 or 34 rectangles at 16 points would have to be:
by k-cross 1 D the non-root rectangles must have total area at least N(N - 1)/4 = 60; 28 rectangles means average area
above 2.1, 33 means 1.8; list the shapes that allow it and test those shapes only.
**Growth law.** This brief IS the growth law: the sequence tau(k), exactly at k = 2, 3 and as tightly as possible at k = 4,
with the recursion it obeys. tau(k + 1) = 2 tau(k) + constant is linear size; = 3 tau(k) - tau(k - 1) is Fibonacci and
loses in the end; = 2 tau(k) + c * 2^k is N log N with constant c/2 (the textbook has c = 2; the pair 5, 13 read this way
gives c = 3/4, that is 32 rectangles at 16 points and a constant 3/8, half of e2-0's 3/4) [derived, mine].
**The question to keep asking.** A recursion needs a reason: what operation turns a rectangle decomposition at k into one
at k + 1 while adding only a bounded number of rectangles per old rectangle, and why does tensoring (which multiplies) do
worse than it? The Potts matrix does it with one large number; is there a matrix in the class that is "Potts-like" on a
hierarchy of blocks?

---

## Left for a sixth wave (nothing is thrown away)

- k-cross section 5: the three objects for a skeptic (g-1's count (O) line at 512 points, e2-0's induction beyond k = 6,
  g-6's hand counts for trees with 16 and 32 leaves).
- k-cross 1 H: every tying construction is built from "equality objects" of the uncertainty principle; nobody has built a
  circuit from wires that MISS equality by a fixed factor on purpose.
- Complex kernels and the limit towards a zero entry for the 19 (k-cross section 7 says untested).
- The literature question k-cross leaves open: is "19 gates for the third power of a generic 2 x 2 kernel", or the count
  N - 2 + tau, known? (A dated search; knowledge may be older than October 2026.)

What I did not do: I ran nothing and checked none of the numbers I quote. Mine and unchecked: the forest count N - 2f + tau;
the textbook tau sequence 6, 18, 50, 130, 322; the three laws through 5 and 13 and their gate counts; the remark that the
rank lemma gives only a linear bound; the non-zero counts 9, 89, 777 (subtractions from k-cross's figures) and "N^0.6";
the bound 3N - 3 for a tree with a matching in brief 7; N(s) = 2^(s^2) giving N sqrt(log N) in brief 4.
