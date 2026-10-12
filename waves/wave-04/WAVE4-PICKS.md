# wht39 / ideas / WAVE4-PICKS: nine briefs for an hour each

2026-10-10, about 23:50 EDT, 15-minute box, curator `m-pick`. Private research: nothing published, no git, no Lean.
I ran nothing. Marks: [read] = read tonight in the file named, [derived] = by hand tonight by me, unchecked, [guess] = marked guess.
Counts: **(G)** a gate is any a*u + b*v, scalings free; **(O)** OpenAI's count, every addition and every multiplication by a
constant charged. Say which one every time.
Read in full: `j-cross.md`, `e2-0.md`, `e2-2.md`, `a-2.md`, `WAVE3-PICKS.md`. Read in part (openings): `g-0.md`, `g-1.md`, `g-4.md`,
`e2-3.md`, `e-5.md`, `d-0.md`; the release README section 6 and the listing of `R/tools/`. Not read: `e-7.md`, the other g-reports.
The second wave's skeptics (`b-0.md`, `b-1.md`, `b-2.md`, `WAVE2-NOTE.md`) had not landed. Curator, not critic: nothing is ranked.

The nine are the eight experiments of `j-cross.md` section 7 plus `orecord` (its section 6, object 1, and `e2-0.md` mutation 2).
None repeats a wave-3 brief (mirror, tightwires, basischange, illconditioned, zetalead, k3, twosteps, thirdturn), so all nine are kept.
Two of them had to be re-aimed because a wave-3 report landed after `j-cross.md` was written: see note 2.

R = `(not in this repository) wht-power-saving-r4-candidate` (READ ONLY). I = `waves`.

## Notes for all nine developers

1. **Words.** N = 2^k points; H the Walsh-Hadamard matrix with entries 1 and -1, its rows are the outputs. A *wire* is any linear
   form a program holds, up to a scalar. s = its number of non-zeros written in the inputs, s' = its number of non-zeros written
   in the outputs. Always s*s' >= N. *Tight*: s*s' = N (a row of signs on a sub-block of the addresses). *Over the limit*:
   s*s' > N. *Product wire*: a tensor product of one 2-vector per address bit. *Entangled on a set of bits*: not a product across
   those bits. *Hub*: a wire that is one gate away from several outputs. *Helper*: a wire that is neither input nor output.
2. **What changed after `j-cross.md` was written** [read: `g-1.md`, opening and sections 4 to 8].
   - **8 points in 19 gates (G)**, `I/g-1-tightwires/h8_19gates.txt`: seven gates merge the inputs into ONE sign vector (the
     "centre", signs + - - - + + - +), then twelve gates each flip the signs on a single input or on a piece the merge left behind.
     Tensored: 54 at 16 points and 304 at 64. So the table of records in (G) is now: **4 points 7 (exact minimum), 8 points 19
     (minimum between 15 and 19), 16 points 52, 32 points 128, 64 points 304** (the last three from `I/e2-0-pieces/slp_*.txt`).
   - g-1 reports that the 19 uses five full-support over-limit wires (s*s' = 4N and 8N), each read by only two gates. Five gates
     saved, five such wires: if that count is right, the law L1 below holds again with equality [read, not counted by me].
   - In (O): H_8 x / 2 in 20 operations, and (5/6) N log2 N + N for N a power of 8 [read, g-1].
   - `g-0.md`: the cheapest basis of the mirror at 16 points is exactly 24 gates and that route ties 56. `g-4.md`: the subset-sum
     matrix is three calls of the transform for every k, and with additions alone it needs exactly k 2^(k-1) (it cites Kennes;
     Boyar and Find).
3. **The two guessed laws of `j-cross.md` section 4** (read off seven circuits, five of them one family).
   **L1**: gates saved below N log2 N <= number of over-limit wires. **L2**: gates saved <= (1/2) * sum over wires of log2(s*s'/N).
   [derived, j-cross] L1 would force gates >= (1/2) N log2 N, so the published result must break it at some size; L2 allows linear size.
   The number that decides the order: **gates saved per over-limit wire**. Linear size needs it to grow like (1/2) log2 N.
4. **The walls** (`j-cross.md` section 2): U (all wires tight => N log2 N, proved in `a-2.md` section 2), M (one magnitude:
   coefficients 1 and 2 cannot go below 0.315 N log2 N), C (commuting steps), S (every split leaves transforms of total length N).
   The product-wire lemma: all wires products => N log2 N whatever the coefficients; with a fixed partition into blocks of b bits, N log2 N / b.
5. **Tools, with their limits** [read: `WAVE3-PICKS.md` note 2; file listings].
   - `I/j-cross/meters.py` (prints s, s', entangled bits of every wire of a program file), `budget.py`, `prod4.py` (exhaustive
     product-wire search at 4 points with label coordinates), `hubclass.py`. Read each header before use.
   - `I/e2-0-pieces/`: `gen.py` (builds and replays the staircase family), `replay.py`, `walk.py` (local walk on helper sets),
     `deep.py`, `pool.py` (the 240 stabiliser vectors at 8 points), `oslp.py`, `ocheck.py`.
   - `I/g-1-tightwires/`: `sa8.py` (annealer on helper sets in a pool of 304 wires), `exact8.py` (exact minimum of the one-centre
     model), `flipwalk.py`, `ledger19.py`.
   - `I/d-0-zeta/mincirc.c`: exhaustive over GF(p), count (G), fixed targets; 8 wires fit for p = 3, 5, 7; 16 wires only over
     GF(2) as written (3^16 needs larger tables on the Linux machine). `I/j-machine/steiner.py`: heuristic over helper forms,
     replays exactly. `slp.py` does not work.
   - A circuit found modulo a prime is a candidate until lifted and replayed exactly. "None modulo p" is not "none".
6. Generation first, play second, criticism last. Report the growth law you see and every anomaly that will not go away, not only the count.
   When the skeptics' reports land (`I/b-*.md`, `I/WAVE2-NOTE.md`), read the part on your object.

---

## Brief 1. `onepergate`: can one over-limit wire pay for more than one saved gate?

**From.** `j-cross.md` section 5 and section 7 item 1; `a-2.md` section 6; `g-1.md`.
**The idea, in my words.** Every circuit of tonight that beats the textbook pays one "badly spread" wire for each gate it saves.
If that exchange rate is a law, the order is N log N for ever. If one wire can ever pay for two gates, that wire is the first
sample of what an order-changing program is made of. The search is therefore not for fewer gates but for a better exchange rate.
**Objects.** The seven circuits measured in `I/j-cross/meters.out` and `budget.out`; the new 19 (`I/g-1-tightwires/h8_19gates.txt`,
`ledger19.out`); the two 21s (`I/e2-3-drain/h8_21gates_drain.txt`, e-2's in `I/e-2-density/`); pools in `I/e2-0-pieces/pool.py`
and `I/g-1-tightwires/pool.py`.
**First experiment.** (a) Run the three meters on the 19: count its over-limit wires, s, s', entangled bits for each. Is it
19 + 5 = 24, on the law again? (b) 8 points, exact search for a circuit with (gates) + (over-limit wires) < 24: 19 gates with at
most 4 such wires, or 18 with at most 5, 20 with at most 3. Pool: the 240 stabiliser vectors, all sign vectors, the vectors with
entries 0, 1, -1, 2, -2 entangled on all three bits, and at least one pool with entries that are NOT bounded (ratios 3, 1/3, a
free parameter t), because wall M says bounded entries cannot change the order. (c) 16 points: (gates) + (over-limit wires) < 64
(the record is 52 + 12).
**Report.** For every hit, each wire's s, s', entangled bits and how many gates read it. For a clean "none", say exactly in which
pool, and explain the waste of the two 21s (3 saved with 6 and with 11 over-limit wires).
**The question to keep asking.** What would a wire look like that is read by many gates, each of which lands on an output or on a
tight wire? Leak 2 of `e2-0.md` has one: the one-flip hub is one gate from ALL N outputs, with partners that cost a whole
transform. Is there anything between "4 outputs, free partners" and "N outputs, dear partners"?

## Brief 2. `staircase3`: hubs that overlap on three address bits, and the rate as the window grows

**From.** `j-cross.md` section 7 item 2; `e2-0.md` sections 3, 5 and mutation 4; `g-1.md`.
**The idea.** e2-0's family saves a gate with every hub that joins two pieces on two adjacent bits, and by interleaving (each
level's hub input is the next level's partner) it gets 3/4 where the plain 4-point brick gets 7/8. Its wall lemma covers only
two-piece hubs on one chain of halvings. A hub that joins four quarter pieces of four different characters is entangled on three
adjacent bits and is outside the lemma. j-cross's target "8 points in 19" has since been reached by g-1 with a different design
(one centre, then flips), whose plain tensor rate is 19/24. Nobody has interleaved a three-bit brick.
**Objects.** `I/e2-0-pieces/gen.py`, `slp_8.txt`, `slp_16.txt`; the mixed-hub lemma and the recursion D(m) = 2 D(m/2) + 3m/4 in
`e2-0.md` section 3; `I/g-1-tightwires/h8_19gates.txt`, `exact8.py`, `flipwalk.py`.
**First experiment.** (a) Write g-1's 19 in e2-0's language of pieces: which wires are pieces of which characters on which
sub-blocks, and what plays the part of the "witness"? (b) Interleave it: at 16 and 64 points let the leftovers of one three-bit
window be the partners of the next, overlapping by one and by two bits. Targets in (G): 16 points under 52, 64 points under 304,
8 points in 18. (c) Extend `gen.py` to four-piece hubs with partners three levels down and print the recursion it obeys.
**Report.** The rate r(w) for a window of w bits: 7/8 and 3/4 at w = 2 (plain, interleaved), 19/24 at w = 3 plain, and what
interleaving gives. [guess, mine] if interleaving doubles the saving as it did at w = 2, w = 3 would give 7/12.
**The question to keep asking.** Does r(w) tend to zero as w grows, or to a positive constant? With coefficients 1 and 2 it
cannot pass 0.315 (wall M), so say at which window the coefficients would have to grow, and try `e2-0.md` mutation 5 (hub
M = A + t*B with t depending on the level) on the same skeleton.

## Brief 3. `clique17`: four arrays in 17 moves at block size 5 (the 1e-1 case inside the engine)

**From.** `j-cross.md` section 6 object 2 and section 7 item 3; `e2-2.md` sections 1, 2, 7, 8.
**Why it matters, plainly.** With k single moves per array at block size m the engine's exponent is z = log k / log m.
4 arrays in 17 moves at block size 5 is k = 17/4, z = log 4.25 / log 5 = 0.899: **a saving of 1.0e-1 in the user's terms**
[read e2-2; arithmetic redone by hand]. 18 moves would be 6.5e-2 and 19 moves 3.2e-2 [derived]. So both outcomes count:
a proof that 17 is impossible closes the only 1e-1 case that counting leaves open in this game; a construction is a result.
**Definitions the developer needs** [read: `e2-2.md` section 2].
- An *array* is one working copy of the data. A *unit* is the fixed small program the engine repeats at every scale. Each of
  the W live arrays must be transformed along all m directions of the label space (m-bit vectors); m is the *block size*. One
  direction on one array is a *move*. A *block* is a run of r moves on one array done as one call (r its rank).
- *Old letters*: the unit may use only (i) constant rational matrices that mix whole arrays (free), (ii) address shifts on one
  array (free), (iii) moves along directions (paid). No address maps, no phases. Any number of extra *scratch* arrays is allowed.
  An **old-letter unit** is a word in these letters that is right on the W live arrays.
- In the basis where all old letters are diagonal, the only thing a word can see is one *quadratic form* q on m-bit vectors
  (degree two, no constant term). A block with directions z_1..z_r has the label S = z_1 z_1^T + .. + z_r z_r^T (a symmetric
  m x m bit matrix) and multiplies its array by (-1)^q(S). q *selects* the block when q(S) = 1. The whole transform is S = I.
  The unit is right when, for EVERY q, the selected sign changes multiply to (-1)^q(I) on the live arrays.
- *Counting*: every q with q(I) = 1 selects at least W blocks. Such a q is **tight** when it selects exactly W.
- **Clique lemma** (e2-2, derived tonight, one exact test, no second reader): with old letters and any number of scratch
  arrays, a set of blocks any two of which are selected together by some tight form has at most W members. Proof idea: for a
  tight form the vectors u_i (column of the constants before block i) and w_i (row of the constants after it) satisfy
  w_i.u_i = 1 and w_i.u_j = 0 for i after j; a pairwise-joined set of size t then gives a triangular t x t table of rank t that
  is a product through W dimensions.
- Known [read]: counting allows 16 moves for W = 4, m = 5 (every odd-weight direction once), and that design is the only
  16-move count vector (`uniq5.out`); the lemma excludes it. 17 was proved by the solver in five of eight cases, the solver's
  bound is 18 in the other three. 17, 18, 19 are open.
**Objects.** `I/e2-2-ladder/clique.py`, `clique.out`, `milp.py`, `milp5_W4.out`, `uniq5.py`, `uniq5.out`, `lemma_test.py`,
`pairs.py`, `refl.py` (unfinished search for reflections realising a count vector; it lacks scratch arrays). The scipy runs
need the Linux machine. Neighbours: `(not in this repository) wht38/tiny/filter/joint/NOTE.md` and
`wht38/tiny/next/cutf3.md` (a cut-set lemma: at block size 3 without address maps nothing is saved), `wht35/wider/w-size.md` section 5.
**First experiment.** (a) Re-derive the lemma independently and test its last step on words that are not plain schedules in
disguise. (b) Enumerate every count vector with 17 single moves for W = 4, m = 5 that passes counting (up to permutations of
the coordinates), and for each run the clique test: put the lemma into the integer programme as "no W + 1 blocks pairwise
joined by tight forms". (c) For every vector that survives, search for the constants: the conditions are polynomial equations
in the mixing matrices (U_A (1 + 2 C_A)^(-1) W_A^T = 1 or 0 for every q); solve modulo a large prime with 0, 1, 2 scratch
arrays, lift and replay exactly. (d) If nothing survives, write the proof; then block size 6.
**The question to keep asking.** The lemma says a unit needs FEW tight forms: most forms must get their -1 from reflections that
do not commute. What is the smallest set of non-commuting reflections with enough short relations (e2-2 names root systems)?
And does the lemma survive address maps, where the cut-set lemma says every saving at block size 3 must live?

## Brief 4. `orecord`: the record in OpenAI's own count, priced with OpenAI's own files

**From.** `j-cross.md` section 6 object 1; `e2-0.md` sections 4, 6, mutation 2; `e-5.md`; `g-1.md` opening.
**The idea.** Count (G) lets scalings ride free; OpenAI's count does not. e2-0 claims H x / 4 at 16 points in 60 operations (O)
(textbook 64 for H x) and (7/8) N log2 N + N/4 for H x / sqrt N at powers of 4; g-1 claims (5/6) N log2 N + N at powers of 8.
e-5 had a law, "one bit per operation", proved only for butterflies and sum-of-four gates, with a measured ceiling of about
1.2 bits per operation for a wider gate. [derived, mine] 1/1.2 = 5/6: g-1's rate sits exactly on e-5's measured ceiling.
Coincidence, or the same object seen twice?
**Objects.** `I/e2-0-pieces/oslp_4.txt`, `oslp_16.txt`, `oslp_64.txt`, `oslp.py`, `ocheck.py`, `oprice2.py`;
`I/g-1-tightwires/c19.py`; `I/e-5-conserved/`; OpenAI's model in `R/OAI/Computability/FourierTransform/` (e2-0 cites `RAM.lean`
lines 163 and 188 for the `scale` atom billed one; read `Cost.lean` and `Goal.lean` for what the statement asks); Alman and Rao,
arXiv:2211.06459 (23/24 and the 7/8 variant).
**First experiment.** (a) Read OpenAI's statement: does it want H x exactly, and is a halving one operation? Price both records
for H x itself and for sizes that are not powers of 4 or 8. (b) Exact minimum in (O) at 8 points for H x and for H x up to a
common scale (the textbook is 24; e-5 excluded below 24 only in a class); at 16 points, anything under 60. (c) Tabulate
operations per address bit per point for windows of 2 and 3 bits and for the interleaved family, and compare each with e-5's
bits-per-operation meter. (d) A dated literature check on the constants.
**The question to keep asking.** In (O), is there a ceiling on bits made per operation that holds for EVERY gate (then N log N
in (O) follows with a constant), or does the ceiling rise with the width of the gate? e-5 saw it rise from 4 to 6 points and
fall again by 12: is that fall a fact about one gate shape or about all?

## Brief 5. `zetafloor`: subset sums, where there is no hub

**From.** `j-cross.md` section 7 item 4; `d-0.md`; `a-2.md` section 2 by-products; `g-4.md`.
**The idea.** Linear size is a property of the whole class of 2 x 2 kernels (three calls of the transform give subset sums, two
subset-sum transforms give the transform). The transform has a hub at 4 points; subset sums have none: 4 gates at 4 points and
12 at 8 are exact minima in several fields, and tight wires alone need Yates's count k 2^(k-1). So subset sums are the member
of the class where a lower bound looks most provable, and a proof for them at all sizes would settle the order for everyone.
But the published result, pushed through the three calls, says subset sums DO fall below Yates at astronomical size [read g-4].
So the exact minimum must leave k 2^(k-1) somewhere, and nobody has seen the first wire that does it.
**Objects.** `I/d-0-zeta/mincirc.c`, `mincirc_all.c`, `rows_zeta*.txt`, `z8_p3_all.out` (2,772 optimal 8-point circuits, 150 with
one signed helper); `I/j-cross/prod4.py`; `g-4.md` (the word Z = D H D H D H D).
**First experiment.** (a) 16 points: is 32 the exact minimum in (G)? mincirc with 16 wires needs enlarged tables over GF(3) on
the Linux machine, or a restricted exhaustive search (helpers with entries 0, 1, -1; helpers entangled on two bits); then a
second prime. (b) Take the 150 signed circuits apart with the meters: is the signed helper over the limit, and why does it tie?
(c) Try the proof: product-wire lemma plus ONE entangled wire => still (N/2) log2 N for subset sums? Then two wires. Find the
number of entangled wires at which the proof stops.
**The question to keep asking.** What does the transform have at 4 points that subset sums lack, in one sentence that a proof can
use? (j-cross Hybrid 4: every kernel [[1,1],[1,tau]] has the brick; subset sums are the limit tau to infinity.) And the mirror
image: push the 7-gate brick through H = Z D Z-transpose and see what it becomes for Z.

## Brief 6. `ladderbound`: wires entangled on at most two bits

**From.** `j-cross.md` Hybrid 2 and section 7 item 5.
**The idea.** Product wires give N log2 N. The staircase uses wires entangled on one pair of adjacent bits and reaches
(3/4) N log2 N + N/4. Conjecture to prove or break: if every wire is (a product over the other bits) times (any 4-vector on ONE
pair of bits, the pair free to change from wire to wire), the program needs (3/4) N log2 N gates. At 8 points that says 18;
the staircase has 20 and g-1's 19 uses wires entangled on three bits. So 8 points already separates 18, 19 and 20 in this class.
**Objects.** The product-wire proof (`j-cross.md` section 4, Hybrid 2: each gate "is born along" one bit; N gates per bit);
`I/j-cross/prod4.py` (label coordinates: 8 labels per axis suffice for programs of at most 8 gates); `I/e2-0-pieces/slp_8.txt`.
**First experiment.** (a) Exhaustive at 8 points over product-times-one-pair wires, coordinates as labels as in `prod4.py`,
for 18, 19, 20 gates; replay any hit exactly. (b) By hand: redo the per-bit count with one entangled pair allowed. Which step
of "fix a bit i; the wires whose i-th factor is (1,1)" survives when bit i may be entangled with one neighbour?
(c) Wires that are sums of two product wires in different partitions (j-cross says its lemma does not cover them).
**Report.** The exact minimum in the class at 8 points, and a guessed law c(b) for "entangled on at most b bits": c(1) = 1,
c(2) = 3/4 ?, c(3) = ? If c(b) behaves like 1/b or like 2^(-b), say which, because that is the difference between needing
log N entangled bits and needing log log N.
**The question to keep asking.** Is the price of a wire its number of entangled bits, or its s*s'? The two meters agree on every
circuit so far (two bits, 4N); find a wire where they disagree and see which one the gate count follows.

## Brief 7. `classhub`: the brick for every kernel, followed out to the kernel with a zero

**From.** `j-cross.md` Hybrid 4 and section 7 item 6; `d-0.md`.
**The idea.** For K = [[1,1],[1,tau]], K x K = u u^T + (tau - 1) P with u = (1,1,1,tau) and P a signed relabelling. So every
kernel without a zero entry has the 7-gate brick, and the hub is not special to the transform. At tau = infinity the kernel is
subset sums (after scaling), where the exact minimum is the textbook's and no hub exists. Somewhere on the way each saved gate
must die or turn into something else. Watching it die is a way to see what a saving is made of.
**Objects.** `I/j-cross/hubclass.py`, `hubclass.out`; `I/e2-0-pieces/gen.py` (the staircase at tau = -1); `I/d-0-zeta/mincirc.c`;
`d-5.md` (programs whose coefficients blow up near a limit point).
**First experiment.** (a) Build the staircase for tau = 2 and tau = 1/3 at 8 and 16 points: do 20 and 52 survive, exactly?
Replay with fractions. (b) Carry tau as a symbol: write the 7-gate and 20-gate programs with coefficients that are rational
functions of tau, and list which coefficients go to 0 or to infinity as tau goes to infinity, to 1 (rank one) and to 0.
(c) Exact minimum at 4 points as a function of tau over a few primes: 7 for generic tau; where does it drop (tau = 1 surely)?
(d) Does g-1's 19 exist for every tau?
**The question to keep asking.** At tau = -1 only, P fixes u and the brick is a relabelling times a reflection. Is there a
special tau of a different kind, a root of unity of order 3, 4 or 6, where K x K x K has an identity that other tau lack?
The Fourier statement supplies i: try tau = i and tau = a cube root of unity.

## Brief 8. `unitmeter`: read the published unit with tonight's meters

**From.** `j-cross.md` section 7 item 7 and section 8 ("the published program is a circuit in count (G): assumed, not checked");
`e2-2.md` section 1; `e-5.md` item 7.
**The idea.** The published program is the only one known that MUST break L1 (it is below N log N in order). Tonight's meters
have never been pointed at it. Find the wires that pay for more than one saved gate each: they exist, and they are in a file.
**Where the published unit is described** (R is read only).
- In words: `R/README.md` section 6 "The design" (W = 1,263 arrays = 480 data + 783 helpers, block size m = 45, 56,715 moves
  in place of 56,835, D = 120; a helper holds a signed sum of several sources) and section 7 (the scratch copies);
  `R/notes/how-the-e8-unit-was-found.md`, `R/notes/scratch-copies.md`, `R/notes/open-directions.md`, `open-directions-2.md`.
- As data: `R/tools/certificate/gcert1-e8-r783.json.gz` (the certificate: labels, gates, block histograms).
- As programs: `R/tools/ccheck.py` (reference checker that reads only the JSON and replays every gate; its header names the
  conditions), `R/tools/whatif_copies.py` (builds the block list of one unit from a certificate), `R/tools/e8/` (`README.md`,
  `replay.py`, `sched.py`), `R/tools/gx/`, `R/tools/rebuild/`.
- As Lean: `R/Work/Block/Word.lean`, `Engine.lean` (the letters: `Move.localM`, `Move.shift`, `BMove.block`),
  `R/Work/GCert/Data/E8Price.lean`, `R/OAI/Computability/FourierTransform/DirectionalWords.lean`, `BinaryFrames.lean`.
- Already measured: `I/e2-2-ladder/unit_batch.py`, `unit_batch.out` (saving = fraction of moves saved / fragmentation,
  8.76e-4 = 2.11e-3 / 2.41).
**First experiment.** (a) Decide what a "wire" of the unit is: an array's content at one moment, as a linear form in the 480
data arrays AND in the address (the label of the frame it is held in). State the dictionary before measuring. (b) From the
certificate, for every array at every step: the number of sources it mixes (the batch side of s) and its label (the address
side); then s, s' and entangled bits in j-cross's sense for the smallest size the unit runs at (f = 1), or symbolically.
(c) Count: moves saved (120 per unit) against over-limit wires. Which wires are read by the most blocks?
(d) Reduce: is there a toy version (a few pairs, small h) of the same word that is a genuine circuit on a few hundred points
and already breaks L1? That toy would be the smallest known L1-breaker.
**The question to keep asking.** The unit's cheap steps are additions of WHOLE arrays, which cost n and not n log n. In count
(G) on a single array, what are they: gates between wires that differ on high address bits only? If so the unit is "entangled
across the batch index", and the meter that matters is entanglement between the batch bits and the address bits.

## Brief 9. `provethewrongthing`: try to prove L1, and find the step that must fail  (silly)

**From.** `j-cross.md` section 7 item 8; `a-2.md` sections 2 and 6.
**The idea.** L1 (gates saved <= over-limit wires) would give (1/2) N log2 N for every program [derived, j-cross: saved gates
<= over-limit wires <= gates]. That contradicts the published result, so the proof cannot exist. Write it anyway, as far as it
goes. a-2's level count is the frame: with tight wires only, every level d needs N gates that cross it. Let one wire be over
the limit and charge to it every crossing it spares. The step where one wire is found to spare an unbounded number of crossings
is a drawing of an order-changing gate.
**Objects.** `a-2.md` section 2 (level, gate lemma, crossing count) and section 6 (the version with slack:
s_w <= (1 + 2P/N) s_u, and the sum over gates of log2(1 + 2 P_g/N) >= N log2 N); `I/j-cross/budget.py`; the ledgers in
`I/g-1-tightwires/ledger.out`, `ledger19.out` (g-1 section 2 says "the ledger has a second side": read it).
**First experiment.** (a) Give an over-limit wire a level interval [log2 s, log2(N/s')] in place of a level and redo the gate
lemma for intervals. (b) Prove L1 for circuits with exactly one over-limit wire; then two that never meet in a gate; then two
that do. Write down the first case you cannot do. (c) Test that case by machine at 8 points: a small exact search for circuits
with exactly j over-limit wires, j = 1, 2, 3, and their least gate counts. Is it 24 - j each time?
(d) Take the failing step to brief 8's object: does the published unit do exactly that?
**The question to keep asking.** In a-2's slack inequality a wire with s*s' = P is worth log2(1 + 2P/N) per gate THAT TOUCHES
IT, and nothing bounds how many gates touch it. L1 says "once". What forces "once" in every small circuit: the wire, or the
partners the other gates would need?

---

## Left for a fifth wave (nothing is thrown away)

- `j-cross.md` section 6 object 3: e-7's slack law (one half child plus one quarter child) has still not been re-derived by a second hand.
- Wall C's untried hypothesis: alternate two kinds of step that do not commute (e-0 mutation 2, e-4 mutation 1).
- `e2-0.md` leaks: quadric pieces at 16 points (leak 1); the circulant of size N - 1 behind the one-flip hub (leak 2, mutation 7).
- `e2-2.md` section 8: amortised 4-point transform (3 and 4 copies in fewer than 21 and 28 gates); the clique lemma for the
  full game with address maps; reflection families other than E8.
- `g-1.md` section 7 mutations; the exact 8-point minimum (15 to 19).

What I did not do: I ran nothing and checked none of the numbers I quote. The savings 6.5e-2 and 3.2e-2 for 18 and 19 moves,
the remark that 5/6 equals one over e-5's ceiling of 1.2, and the guess 7/12 in brief 2 are my own arithmetic of tonight.
