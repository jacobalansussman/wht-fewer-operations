# ab-6 chain-of-exchanges: arrays in a ring, shears shared between neighbouring exchanges

11 October 2026, 04:42 to about 05:40 EDT, one agent, 60-minute box. Private research: nothing published, no git, no Lean,
nobody has read this. **No circuit below any known count and no growth law below N log N beyond the published one.
Nothing here changes the order.**

**Legal network or what-if count? Stated plainly: three LEGAL WORDS of the engine were built and replayed exactly, and
none of them is a unit: each uses MORE moves than the plain schedule (12 against 8, 20 against 12, 52 against 36).
Every saving figure in this report is a WHAT-IF COUNT, a block list with no network behind it.**

Marks: [ran] = exact run of mine tonight (whole numbers and fractions; programs in `ab-6-chainexchanges/`); [ran floats] =
least-squares search in floating point, a hit is a candidate and "none" is not a proof; [derived] = by hand tonight, checked
by nobody; [read] = in a file I opened tonight; [guess].
Counts. On x-3's side: CALLS to a box, glue free (no gates are counted). On the engine's side: MOVES and BLOCKS, the engine's
own units. Gate counts (G) and (O) are not used anywhere.

Words beyond the brief's list. *Stage*: one group of address bits in which every array of the word climbs once.
*Climb*: the block an array makes in a stage (all of the stage's directions except one port-sized hole). *Hole*: the
directions of a stage that an array does not move along. *Total*: a sum of arrays that have climbed, copied into a
scratch array and brought down through the whole stage (h moves); it delivers to every reader the sources moved backwards
along their ports. *Leak*: on x-3's side, the copy of a datum that the FIRST box it passes sends to the output.

## 0. In twelve lines

1. [derived; three of x-3's numbers reproduced] **The room that x-3 left at 1.5 K is not there.** For the family "a box
   known only up to an address map", a call program needs at least **2K - 2 calls for every K >= 8, and exactly 7 at
   K = 4** (so 6 is impossible; x-3's exact program has 7). Textbook 2K. The saving is 2 calls at every size: a = r/K tends
   to 2, exponent log2 a tends to 1. The chain "every call is the second box for one datum and the first box for the
   next" cannot exist. Section 1.
2. Why, in one sentence: the first box a datum passes sends a plain copy of it (moved once) to the output; the output map
   has to kill that copy, and killing it uses up as many output numbers as the datum has. A call cannot be a first box for
   free.
3. [ran, `leakbound.py`] The numbers: K = 4, 8, 16: leak bound 7, 14, 30; textbook 8, 16, 32; x-3's telescoping bound 6,
   12, 24. On the two halves of the table at K = 4 the same lemma gives 4 (skew) and 3 (symmetric): exactly what x-3's
   float searches found.
4. [derived + ran] On the engine's side the exchange algebra does allow a ring, and it is legal. Three exact replays in a
   formal register machine (the engine's own formal game restricted to additions, shifts and blocks; no address maps):
   the plain exchange in 3 stages; a new **two-stage exchange with a bystander** (3 arrays, 4 shears); and **a ring of 4
   arrays that does two rounds of exchanges in 5 stages instead of 6** (stage 3 is the last shear of round one and the
   first of round two). `ring.py`, `ring2.py`. All three end with every live array holding the kernel of its own input.
5. [ran] In those legal words the data arrays make FEWER blocks than x-6 counted: 2 blocks per array for the plain
   exchange (x-6: at least 3), and ONE block for one array of the bystander word, which never moves along the port.
   But the words lose moves, because each total serves one source (kappa = 1). The blocks are real; the saving is not.
6. [derived] What the ring shares is STAGES, not SHEARS. R rounds take 2R + 1 stages instead of 3R, so the skipped share
   rises from r/(3h) towards r/(2h). The number of shears per filled hole stays 3/2. (The published bridged word has 5/4.)
7. [ran floats, price law] **In the engine's accounting the ring is worse than one round.** Each round adds a block to every
   array, and the price law charges for blocks. WHAT-IF saving with shears and helpers free, r = h/3:
   0.119, 0.105, 0.095, 0.082, 0.068 for R = 1, 2, 3, 5, 10 rounds. The best member of the family is R = 1.
7b. [ran floats, what-if] **The best block list of the hour is the two-stage word with a bystander**, because it has two
   stages (m = 2h) and one array of three in a single block: 0.204 at r = h/3, 0.129 at r = h/5, 0.075 at h = 9, r = 1
   with shears and helpers free; 0.120, 0.042, 0 with every shear paying h/15. The plain exchange gives 0.119, 0.077,
   0.047 (free). Same skipped share on average, r/(3h); the difference is blocks. Section 4b. NO NETWORK behind it.
8. [what-if] R = 1 is the plain exchange with its climbs merged (blocks h-r, 2(h-r), 2r on one array and 2(h-r), h+r on
   the other): 0.119 at r = h/3, 0.077 at r = h/5, 0.047 at h = 9, r = 1, all with shears and helpers FREE. With every
   shear paying h/kappa moves, kappa = 15: 0.082, 0.038, 0.005. x-6's count for the same word was 0.078 (free).
   So the bar 0.1 is reached only on paper, at r = h/3, with free shears and free helpers. No network.
9. [derived] Three small laws of the exchange algebra: (a) every port is filled for an EVEN number of contents
   (determinant); (b) two arrays alone need three stages per port (two-line proof), a third array brings it to two;
   (c) a content that hops twice along the same port has gained nothing (D D is a free relabelling) [ran].
10. Where does the legal network first fail? Not in the ring: the ring is legal. It fails at the price: (i) a ring does not
    lower the number of totals, and totals are what the published unit pays for; (ii) more rounds per unit means more
    blocks per array; (iii) [ran, `ring.py` (5)] at the smallest batch, one total for two sources, each SOURCE is cut in
    two, because the unwanted share a target must lose is the other source in the middle of its climb. (i) and (ii) are
    properties of the word, (iii) of the batch. On x-3's side the failure IS a property of the chain (line 2).
11. The better question it leaves: **which words keep an array in ONE block while it is written once at the bottom and read
    once at the top?** In the bystander word one array of three does exactly that. Price law: one block per array is
    n log log n. Section 5.
12. State: a wall I can name on both sides (the leak; blocks per round), and three legal words that are not units.

## 1. x-3's side: the leak lemma, and why the chain does not exist

Setting [read: x-3 section 4]. K = 2^k addresses. The box is P_g, the relabelling of the addresses by an invertible bit
matrix g. Target: P_g X P_g^T for a K x K table X. Call program: c_j = P_g (L_j x + sum over i < j of M_ji c_i), output =
Q x + sum of P_j c_j, the glue L, M, P, Q fixed and free. x-3: lower bound 1.5 K by the telescoping lemma; an exact program
with 7 calls at K = 4; "whether 6 is possible is open; the bound 1.5 K would be met only by chains in which every call is
at once the second box for one piece of data and the first box for the next".

**Reduction** [derived]. Address 0 is fixed and the non-zero addresses are permuted, any two pairs alike (2-transitive), so
a K-vector is 2 fixed numbers plus one piece V of dimension d = K - 2 on which the box acts by an irreducible
representation rho(g) [ran: <chi, chi> = 1 at K = 4, 8, 16]. Fixed numbers pass through a call unchanged, so without loss
a program is d_j = rho(g) (A_j x + sum over i < j of m_ji d_i), output = Q x + sum of P_j d_j. The table is
(2 + V) x (2 + V) = 4 fixed numbers + 4 copies of V + V (x) V, and V (x) V = 1 fixed number + mV copies of V + Rest, where
Rest contains neither a fixed number nor a copy of V. [ran, `leakbound.py`: mV = 1 at K = 4, mV = 2 at K = 8 and 16;
Rest = 1, 23, 167 dimensions.] At K = 4 Rest is the one number that is multiplied by the sign of the permutation.

**Leak lemma** [derived]. Let c = the number of copies of V in the table (5 at K = 4, 6 from K = 8 on). Then
**calls >= c + ceil( (Rest + d ceil(Rest / d)) / d )**, which is 7 at K = 4 and 2K - 2 for every K >= 8.

Proof. Keep only the tau = c d + Rest output numbers that depend on g, and call P the tau x (r d) matrix that reads them
from the r calls.
(1) P has rank tau: the differences of the target between two boxes span all of those coordinates. So the kernel of P has
dimension r d - tau.
(2) Take an input t in Rest. As a function of g, the target for t is made of entries of the representations in Rest; it
has no part made of entries of rho(g), and no constant part. Project the identity "P (outputs of the calls) + constant =
target" onto the functions of g that are entries of rho(g) (a linear projection on functions; P is a fixed matrix, so the
two commute). Result: P kills the rho-part of the calls' outputs, for every t in Rest and every g.
(3) Order the calls. Let R_j be the inputs t in Rest that have not entered any of the first j calls directly. For t in
R_(j-1), the calls before j output nothing that depends on t, and call j outputs rho(g) A_j t exactly: a pure rho-part.
If A_j is not zero on R_(j-1), these vectors span all of V in the coordinates of call j as g and t vary (V is
irreducible), with zeros in all earlier calls. Different j give independent vectors (leading coordinates differ). So the
killed space has dimension at least d times the number nu of calls at which R_j gets smaller.
(4) Every t in Rest must enter some call (otherwise its output would not depend on g), and one call lowers the dimension
of R_j by at most d. So nu >= ceil(Rest / d).
(5) r d - tau >= d ceil(Rest / d). QED.

Numbers [ran, `leakbound.py`]:

| K | copies of V | Rest | leak bound | textbook 2K | telescoping bound (x-3) | best program known |
|---|---|---|---|---|---|---|
| 4 | 5 | 1 | **7** | 8 | 6 | 7 (x-3, exact) |
| 8 | 6 | 23 | **14** | 16 | 12 | about 2K - 2 (x-3, rough) |
| 16 | 6 | 167 | **30** | 32 | 24 | about 2K - 2 (x-3, rough) |

General K >= 8 [derived]: Rest = d (d - 2) - 1, ceil(Rest / d) = d - 2, bound = 6 + 2 (d - 2) = 2K - 2.

Checks against things already measured [read: x-3 section 4]. Full table at K = 4: the bound is 7 and x-3 has an exact
7-call program, so **r(4) = 7 exactly and experiment (b) is answered: 6 calls are not possible.** Skew part of the table
(2 copies of V and the sign): bound 2 + ceil(3/2) = 4; x-3's float search found 4 and none at 3 in 17 starts. Symmetric
part (3 copies of V, no Rest): bound 3; x-3 found 3 in 40 of 40 starts. Three numbers, three agreements.

The K = 4 case by hand, as a picture of the mechanism [derived]. With 6 calls the 12 output numbers must give 11 target
numbers, so the output map kills exactly one direction. The sign is +1 on the three even permutations, so the three
versions of the calls' outputs for the datum t (identity and the two 3-cycles) must lie on one line. But the first call
that t enters outputs rho(g) a, and a, rho a, rho^2 a are the corners of a triangle (a 3-cycle has no real eigenvector
in the plane V). Contradiction.

Growth law of this section: **a = r/K tends to 2; the saving in the call recursion is bounded (2 calls); exponent
log2 a tends to 1.** The address-map family joins every other family of x-3: no change of order. What the lemma says about
chains: a call that is "first box for the next datum" pays d output numbers of leak for it, exactly what a separate
call would have cost. Sharing is impossible in this model for any datum whose target is of degree 2 in the box.
Limit of the lemma: it is a statement about programs that are right for the WHOLE family with free glue. For the
transform itself the box is known and the model says nothing directly (x-3's own caveat).

A float search for 6 calls at K = 4 was started before the proof and stopped (`sixcall.py`, `linux/r6.out`: 6 starts,
residuals 2.2 to 6.0, no hit). It is weak and not needed.

## 2. The engine's side: the exchange algebra of stages ("the hole game")

What a stage is [derived from x-6 section 1 and u-5; the address-map detail of the published five-stage word I did not
read from the generator]. A stage is a group of address bits. In it every array does, in this order: is written (any
number of times) at the bottom, climbs (one block, everything except its hole), is read (any number of times) at the top.
A shear goes from an array that has climbed to an array that has not: a copy of the source comes down through the block
span(port, the source's climb), which leaves the source moved backwards along the port, and the target adds it.
Consequences:
- inside one stage the shears form chains: X_0 -> X_1 -> X_2 is legal (X_1 is written, climbs, is read). So a stage is a
  unit triangular matrix in the order in which the arrays climb, with one port move on each shear;
- two arrays cannot shear into each other in the same stage;
- between stages every rational mixing of the arrays is free.
With D = the move along a port, D D = a free relabelling, so over the two "characters" D -> +1, -1 a word is right when
the product of its stage matrices is (free mixing) x diag(+-1), with -1 exactly on the contents that got the port.

Identities [derived; the second and third replayed exactly in section 3]:
- **Plain exchange**, 3 stages: L(x) U(-1/x) L(x) = [[0, -1/x], [x, 0]]. x-6's and u-5's.
- **Two rounds, both arrays at once**: with J = [[0, 1/x], [-x, 0]], (1 + J)(1 + J) = 2 J. Two rounds of simultaneous
  cross-shears do the exchange. NOT legal as stages (each array would be source at the top and target at the bottom of the
  same stage).
- **Two-stage exchange with a bystander** (legal): three arrays. Stage A is the chain 3 -> 2 -> 1 with coefficient x,
  stage B the chain 1 -> 2 -> 3 with coefficient -1/x. Product B A = [[1, x, x^2], [-1/x, 0, 0], [1/x^2, 0, 1]].
  Start with A_3 = c_3 - (relabelled c_1) and finish with A_1 -= (relabelled A_3), both free: arrays 1, 2 end holding
  x c_2 and -(1/x) c_1, array 3 holds c_3 untouched. Two contents get the port move in TWO stages; the third array is a
  catalyst that pays its own port move.
- **Odd-even ring** (legal): even arrays are sources in odd stages and targets in even stages. Round one (pairs (0,1),
  (2,3), ...) uses stages 1, 2, 3; round two (pairs (1,2), (3,0), ...) uses stages 3, 4, 5, oriented so that its first
  shear also goes from even to odd arrays. In the shared stage every odd array is written by both neighbours and every even
  array is read by both. R rounds take 2R + 1 stages, every content gets R different ports.

Small laws [derived]:
- (a) Determinant: the product of the stage matrices has the same determinant for both signs, so every port is filled for
  an even number of contents. [ran floats: three contents all filled, never found.]
- (b) Two arrays, two stages: impossible. If u W v = - u' W v' with u, u' the two sign versions of one stage (both unit
  triangular in the same order), then u'^-1 u is unipotent and equals -W (v' v^-1) W^-1, which has eigenvalue -1.
  [ran floats: 0 of 20 starts; the 3-stage control hits in 14 of 20.] With a third array two stages suffice
  [ran floats: 12 of 30 starts; then the exact word above].
- (c) A content that hops twice along the same port is back where it started up to a free relabelling [ran, `ring.py` (4)].
  So in a ring every content needs a NEW port at every round.

Float searches of this game (`holegame.py`, Linux machine, heavily loaded tonight): the controls above, plus: four arrays,
two stages, all four contents filled: none in 30 starts; two arrays, three stages, two ports at once: none in 30. The
searches for ring targets in fewer stages did not finish in the box (the solver was too slow on the loaded machine; one
more hit was saved before I stopped them: three arrays, four stages, two contents with two ports each, which is two
bystander words in a row).
My first guess "at most one port per content per three array-stages" is FALSE: the 4-ring fills 8 in 20.

## 3. Three legal words, replayed exactly [ran: `ring.py`, `ring2.py`]

The machine. dir(z) and shift(z) are diagonal in the basis of characters: dir(z) = i^(y.z), shift(z) = (-1)^(y.z). So a
product of them is one function q(y) with values in Z/4, and two products are the same matrix exactly when the functions
are equal. A term "[g] v_l" is stored as (l, q); additions are free, a block adds its directions to q and counts its rank.
By GAME.md section 5 [read] a word that is right as such a formal sum is right for every number of digit columns. Not
covered: address maps and address-dependent phase letters (not used).

| word | arrays | stages | every live array ends at the kernel | moves (plain) | blocks per live array | scratch blocks |
|---|---|---|---|---|---|---|
| plain exchange, port 0111, h = 4 | 2 | 3 | True | 12 (8) | [1, 2], [2, 1] | 3 of rank 2 |
| two-stage exchange with a bystander, port 0111, h = 4 | 3 | 2 | True | 20 (12) | [3], [1, 2], [1, 2, 1] | 2, 2, 3, 3 |
| odd-even ring, two rounds, 9 coordinate directions | 4 | 5 | True | 52 (36) | [1,2,2,2], [2,2,3] twice | 12 of rank 2 |

Control: the bystander word without its fourth shear is wrong, as it must be.
A fourth replay, the smallest batch [ran, `ring.py` (5)]: two pairs with ports 0111 and 1011 (they know each other), ONE
total of 4 moves for the two shears. Each target then holds three terms; the unwanted one is the other source after the
two moves it shares with the target's climb, and it comes off by an addition. The state afterwards equals "each target +=
its source moved backwards along its own port, everybody climbed", exactly. Blocks: sources [2, 1] and [2, 1], targets
[3], [3], the total [4]. So already at kappa = 2 the source's climb is cut by the read in its middle. [derived] A climb
through p-perp passes through ONE subspace of dimension h - 2, so a source can serve the removal for at most one target
that knows it out of its own climb; every further one needs a helper array with its own climb. That is where the
published unit's 6.5 helpers per pair come from, and it is the first place where "two blocks per array" fails.
What the table shows. (i) x-6 wrote "an exchange cuts each array into at least three blocks because every shear touches
both arrays". In a legal word it is TWO: X is read after its first climb and written before its second, and nothing
touches it between its second and third climb; the same for Y. x-6's third cut comes from taking the unwanted terms off
at the top of a stage; that step does not exist here because each total has one source. Whether it can be deferred in a
real batch is not decided (section 5). (ii) Array 1 of the bystander word makes ONE block of rank 3 = m - 1 and never
moves along the port. That answers x-6's mutation 6 in its weak form: a live array in a legal word can make a single
block of rank below m. It says nothing yet about units, because this word loses 8 moves. (iii) Every word loses, by
exactly the moves of its scratch copies minus the port moves saved: the whole question is the batch (kappa), as u-5 said.

## 4. The price law on the ring [ran floats: `ring2.py`; what-if block lists, no network behind them]

Shape. R rounds, S = 2R + 1 stages of h directions, port of dimension r, m = S h. Each stage has a native hole of r
directions per array; a round fills the hole of its middle stage, so R holes are filled and R + 1 are caught up by paid
moves. Skipped share rho = R r / ((2R + 1) h). Blocks: an even array (h-r), R times 2(h-r), and (R+1) r; an odd array R
times 2(h-r) and (h-r) + (R+1) r. Shears: 3 per exchange, so 3R per pair of arrays per unit, counted as 3R/kappa blocks of
rank h per pair when priced ("kappa") and as nothing when free.

| r/h | R | stages | skipped share | blocks per array | saving, shears free | kappa = 60 | kappa = 15 | kappa = 5 |
|---|---|---|---|---|---|---|---|---|
| 1/3 | 1 | 3 | 0.111 | 2.5 | **0.119** | 0.110 | 0.082 | 0.011 |
| 1/3 | 2 | 5 | 0.133 | 3.5 | 0.105 | 0.096 | 0.071 | 0.010 |
| 1/3 | 3 | 7 | 0.143 | 4.5 | 0.095 | 0.087 | 0.064 | 0.009 |
| 1/3 | 10 | 21 | 0.159 | 11.5 | 0.068 | 0.063 | 0.046 | 0.006 |
| 1/5 | 1 | 3 | 0.067 | 2.5 | 0.077 | 0.067 | 0.038 | 0 |
| 1/5 | 2 | 5 | 0.080 | 3.5 | 0.065 | 0.056 | 0.031 | 0 |
| 1/9 | 1 | 3 | 0.037 | 2.5 | 0.047 | 0.036 | 0.005 | 0 |
| 1/9 | 3 | 7 | 0.048 | 4.5 | 0.033 | 0.025 | 0.003 | 0 |

For comparison, the plain exchange as x-6 counted it (three blocks of h-r and one of 2r): 0.078 at r = h/3, 0.029 at 1/9.
Reading. Helpers are free in every column (the published unit has 783 helpers for 480 data arrays). With free shears the
saving FALLS with the number of rounds: the skipped share saturates at r/(2h) while the blocks per array grow like R, and
the law is ln(1/(1-rho)) / (ln k + ln(1/(1-rho))). With priced shears it is the same: one round is the best row in every
column. **Growth law of the ring in the engine's accounting: saving of order
rho0 / (2 ln R) for R rounds, rho0 = r/h: it goes to 0 with the length of the ring.** The idea "longer ring, fewer blocks"
is the wrong way round: the ring has more blocks, not fewer.
The count in the brief's own terms: blocks per array are 2.5 for one round, R + 1.5 for R rounds; never below 2 except
for single arrays (section 3, ii).

### 4b. The bystander word in the price law [ran floats: `bystander_price.py`; what-if, no network]

Three arrays, two stages, m = 2h. Arrays 1 and 2 never move along the port (share r/(2h) each), the bystander pays
everything; average skipped share r/(3h), the same as the plain exchange. Blocks, catch-up merged: array 1 one block of
2h - r; array 2 blocks h - r and h; the bystander h - r and h + r. Four shears per three arrays.

| r/h | block list | shears free | kappa = 60 | kappa = 15 | kappa = 5 |
|---|---|---|---|---|---|
| 1/3 | bystander, catch-up merged | **0.204** | 0.183 | 0.120 | 0 |
| 1/3 | bystander, catch-up in blocks of its own | 0.115 | 0.104 | 0.069 | 0 |
| 1/3 | plain exchange, merged | 0.119 | 0.110 | 0.082 | 0.011 |
| 1/5 | bystander, merged | 0.129 | 0.107 | 0.042 | 0 |
| 1/5 | plain exchange, merged | 0.077 | 0.067 | 0.038 | 0 |
| 1/9 | bystander, merged | 0.075 | 0.052 | 0 | 0 |
| 1/9 | plain exchange, merged | 0.047 | 0.036 | 0.005 | 0 |

Reading. On paper the two-stage word is the better shape wherever shears are cheap (kappa of 60 or more), and it is
above the bar 0.1 for r >= h/5 with free shears. It needs four totals where the exchange needs three, so it loses at the
published kappa = 15 with thin ports. What stands between this table and a network: a batch for ports of dimension h/5 or
more with large kappa (x-6: none known; scatters of the published kind stop at h/3), helpers that cost nothing (they are
62 % of the published unit's arrays), and the merging of the catch-up moves. [derived, ten minutes, one construction only] The obvious way to let
one bystander serve two pairs with different ports in the same two stages fails: each pair's first array is left holding a
relabelled copy of the other pair's content, and nobody holds that content without its port move. Not a proof that no
shared bystander exists; the float search for it (five arrays, two stages) did not finish.

## 5. Where it fails, and what I changed ("yes, and")

1. Tried: 6 calls at K = 4 by a float search. Slow, no hit. Asked what a 6-call program would be made of: the sign must
   ride on a call that carries a triple, so that call's output carries a plain copy of the sign's datum. Counting where
   that copy can go gave the triangle argument, then the leak lemma for every K. The chain is closed on x-3's side.
2. Tried: "one batched shear = last of one exchange and first of the next". As a SHEAR this cannot be: the two have
   different sources and targets. Changed to: the two shears sit in one STAGE. That works (odd-even ring) and is legal.
3. Tried: fewer stages per round by any means (float search of the hole game). Found the two-stage word with a
   bystander, wrote it in fractions, replayed it. It has 4 shears for 2 ports (worse than 3) and the same ports per
   array-stage (1/3) as the plain exchange.
4. Tried: the price law on the ring. It goes the wrong way. What the failure is made of: one block per array per round.
   Changed the question to: which array is cut least? Answer in the three words: the array that is written once at the
   bottom and read once at the top (array 1 of the bystander word), one block.
5. First place a legal network fails as a UNIT: at kappa. Every word here has kappa = 1. With kappa > 1 a target also holds
   unwanted shares of other sources, and x-6's removal step at the top of the stage cuts the block again. That is a
   property of the batch (of the ports and which of them know each other), not of the ring.

## 6. Mutations

1. `one-block-arrays`: design a word around arrays that are written once and read once. In the bystander word 1 array of 3
   is of that kind, and that alone lifts the what-if from 0.119 to 0.204 at r = h/3 (section 4b). Also: an exact search
   of the exchange algebra of section 2 (`holegame.py` is the float version) for words with TWO stages and more than one
   single-block array per catalyst. Is there a word in which a fixed FRACTION of the arrays is, with the others as catalysts that are
   shared among many pairs (one catalyst serving kappa pairs through a total)? Price: an array with one block of rank
   (1 - rho) m contributes (1 - rho)^z; the catalysts and totals pay the rest.
2. `deferred-removal`: in a real batch (kappa > 1), can the unwanted shares be taken off one stage later, after the target
   has climbed two stages in one block? The helpers hold "source after h - 2 moves"; they would have to climb with the
   target. This decides whether 2 blocks per array (section 3, i) survives batching. Tool: `x-6-unitasbox/e8m.py`, the
   certificate's own block list.
3. `leak-lemma-for-the-engine`: the lemma of section 1 is a count of what the first box sends on. The engine's formal
   game has the same shape (a term that has made a port move sits in the target until something kills it). Does the
   projection argument give a floor on totals per shear, that is on kappa? It would be the first floor of that kind.
4. `skeptic-first`: the leak lemma is 40 minutes old. Check step (2) (the projection onto the entries of rho) and step (3)
   (independence), and run an exact search at K = 4 for 6 calls as a test (the reduced problem in `sixcall.py` has 192
   unknowns).
5. `ring-ports-not-coordinates`: `ring2.py` uses coordinate ports. Replay the ring with ports of odd weight 3 inside one
   block and one total for two sources that know each other: the smallest case with kappa = 2.

## 7. Criticism, last

- The leak lemma is by hand and unreviewed. It reproduces three numbers of x-3 (7, 4, 3), one of them an exact program,
  the other two float searches. The multiplicities are exact [ran]. x-3's "plain construction about 2K - 2" is rough, so
  "r(K) = 2K - 2" is a lower bound that probably is tight, not a proved value, for K >= 8.
- The stage rule of section 2 is my reading of x-6 and u-5. I did not read the published five-stage word; in particular
  how one port serves three stages there (address maps, "twins") is replaced here by the block span(port, climb), which
  the replays show to be legal but which a batch with many different ports may not allow.
- The replays cover additions, shifts and blocks only. They are formal sums, hence right for every number of digit
  columns if GAME.md section 5 is right [read, not re-proved]. They were not run through `regmachine.py` (it needs numpy,
  which this Mac's python does not have).
- Every saving in section 4 is a what-if: block lists, floats, helpers free, unwanted terms ignored, removal deferred,
  catch-up moves merged where convenient. The R = 1 row is the plain exchange of the published design with merged blocks;
  it is not a new mechanism. 0.119 at r = h/3 needs a scatter for ports of dimension h/3, which x-6 says is the edge of
  what scatters of the published kind allow, and it needs free helpers.
- The hole-game searches are floats, few starts, and most of the list did not finish. "None" there is not "none".
- The ring replay has 4 arrays and coordinate ports: it shows the stage sharing, nothing about batching.
- Nothing here is a unit, a circuit, a bound on gates, or a change of order.

Files: `waves/wave-08/ab-6-chainexchanges/`: `leakbound.py`, `leakbound.out`
(multiplicities and the leak bound, exact); `ring.py`, `ring.out` (formal machine; plain exchange, bystander word and
the smallest batch, exact); `bystander_price.py`, `bystander_price.out` (price law on the bystander word, floats); `ring2.py`, `ring2.out` (the 4-ring, exact; the price-law table, floats); `holegame.py`, `holejobs*.sh` (float
search of the exchange algebra); `sixcall.py` (float search for 6 calls, superseded by the lemma); `linux/` (outputs copied
back from the Linux machine).
