# ab-1 fewer-blocks: what the engine's price really rewards, a ceiling table, and a floor that counts blocks

11 October 2026, 04:45 to about 05:40 EDT, one agent, 60-minute box. Private research: nothing published, no git, no Lean,
nobody has read this.

**Stated plainly, as the brief asks: NO LEGAL NETWORK OF THE ENGINE WAS FOUND. Everything below that carries a saving is a
WHAT-IF COUNT (a block list with no network behind it), or a ceiling, or a floor. No growth law below N log N beyond the
published one. Nothing here changes the order.**

Marks: [ran] = run of mine tonight (programs and outputs in `ab-1-fewerblocks/`); [read] = in a file I opened tonight;
[derived] = by hand tonight, checked by nobody; [guess]. Floats are named where used.
Gate counts: none. The unit of cost here is the engine's own: **moves** and **blocks**. Counts (G) and (O) are not used.

Words (the brief's, plus four of mine). *Array*: one working copy of the data. *Move*: one direction of the transform applied
to one whole array. *Block*: a run of moves on one array with no addition in between; its *rank* is its number of moves; the
engine's rule is rank at most m - 1 [read: GAME.md]. *Block size* m: moves each array is owed. *Unit*: serves W arrays in
fewer than W x m moves. *Price law*: z is the root of "sum over blocks of (rank/m)^z = W"; saving = 1 - z. *Port*, *fat port*,
*knows*, *total*, *kappa*, *exchange*, *shear*, *legal network*, *what-if count*: as in WAVE8-PICKS brief 2.
*Sub-game* (in this report): the engine's game with moves, additions, scratch arrays and shifts, but **without address maps
and without phase letters**. This is smaller than the tiny-unit notes' "sub-game without address maps", which keeps phase
letters. *Form of a block*: for a block along directions z_1..z_k, the symmetric bit matrix B = z_1 z_1^T + ... + z_k z_k^T
(arithmetic modulo 2). *Character*: a way of replacing every move by a sign so that products go to products.
*Switch*: a block seen through one character: it either does nothing or negates its array.

## 0. The answer in twelve lines

1. **No legal network.** One numerical hunt for one was run (section 4); its result is in section 4.5.
2. [derived + ran, floats] **The price law rewards something sharper than "few blocks": one big block per array plus blocks
   of rank 1.** With blocks (m - 1 - d, 1) per array, where d is the number of moves saved per array, the saving is, for small d, about
   d / (1 + ln m), against d / (m ln m) when the same moves are cut into single moves. Saving 0.1 then needs d = 0.25 moves
   per array at m = 4, 0.37 at m = 9, **0.62 at m = 45 (1.4 % of the moves, not 7.4 %)**, 0.78 at m = 110. The brief's
   "(k, rho) = (2, 7.4 %)" is the equal-blocks case, the worst way to have two blocks. (Table C1.)
3. [derived] (a) **"Three blocks per exchange" is not a floor.** In the exchange the array that is source, target, source
   has three climbs; the other (target, source, target) has two. With scratch targets the pair makes four climbs, two per
   array. What stops the word is not the count of blocks: two of those four climbs carry content that is thrown away
   (section 2). I did not reconstruct the published five-stage word.
4. [ran, exact] (b) **The ceiling table.** For r = 2 the largest set of ports no two of which know each other is computed
   exactly at h = 5 and 6 (integer program): ceilings on kappa 2.5 and between 3.48 and 3.75, both below the 3h/(2r)
   needed for any gain. For (7,3), (8,3), (9,3), (9,4) an explicit family (the *club*, section 3) gives ceilings 2.65,
   4.36, 4.64, 2.55. **(8,3) and (9,3) pass the threshold by a hair, and are worth 7.1e-3 and 2.2e-3 at the ceiling. No
   class with h at most 9 comes near 1e-1 in x-6's three-stage design.**
5. [derived + ran] **The ceiling is not flat in h.** The club has about 2^(r - (h+1)/2) of the ports, so the ceiling on
   kappa is about 2^((h+1)/2 - r): exponential in h for every r/h below 1/2, while the threshold 3h/(2r) is a constant.
   From h = 12 on the table no longer excludes anything. But at the ceiling with r = h/3 the three-stage what-if is still
   only 0.034 (h = 12), 0.067 (h = 24), 0.077 (h = 45): it tends to x-6's 0.078. The cap is the three-stage shape, not kappa.
6. [derived, the main by-product] **In the sub-game a unit is a product of switches, one per block.** The moves and
   shifts generate a commutative group; modulo shifts a block is its form B and the kernel is the identity matrix I. Every
   quadratic form Q on the m address bits gives a character: a move along z becomes (-1)^Q(z). Hence, for every Q with
   Q(e_1) + ... + Q(e_m) odd: **the number of blocks whose directions have an odd number of Q(z) = 1 is at least W.**
7. [derived; ran as a linear program, floats; the two moves bounds at m = 3 and 4 also checked in exact fractions,
   `lp_cert.py`] Consequences in the sub-game: **at least 2 blocks per live array, for every
   block size** (the plain schedule has exactly 2); at block size 3 at least 3 moves per array (the cut-set lemma's
   number, recovered in three lines); **at block size 4 at least 3.75 moves per array and no saving above 0.0466: the bar
   of 1e-1 is out of reach there**; at block size 5 at least 3.875 moves per array, saving at most 0.158; at block size 6
   at least 3.9375, saving at most 0.235.
8. [derived] The character inequalities can never ask for more than 4 - 2^(2-m) moves per array: the pattern **"every one
   of the 2^m - 1 directions once, for 2^(m-2) arrays"** satisfies all of them. As a what-if that is saving 0.158 at
   m = 5, 0.235 at m = 6, 0.37 at m = 9, 0.64 at m = 45 (Table C3). It is the first named object above the bar that no
   known inequality of the sub-game excludes. If it existed at every block size the engine would certify
   n (log n)^e for every e > 0 (z = ln 4 / ln m); that is a what-if of the largest kind and nothing more. In this linear program big blocks never help: a block is one switch whatever
   its rank.
9. [derived in the last ten minutes of the box + ran, exact] **That object does not exist at m = 4 and 5, with any number
   of scratch arrays** (the *pair rule*, section 4.4). Call a character *tight* when exactly W moves are active. If two
   moves are active in one tight character, the earlier one reads nothing of what the outputs receive from the later
   one. Every two directions share a tight character (105 of 105 pairs at m = 4, 465 of 465 at m = 5), which would make
   a 15 x 15 triangular matrix with ones on its diagonal have rank at most W = 4. So the linear program's optimum is not
   reached by the pattern it names, and the hunt of 4.5 was hunting something that is not there. Whether ANY pattern
   reaches 3.75 moves per array at m = 4, or anything below 4, is open; the pair rule is a new constraint to add.
10. (c) No small unit exists to re-score. Scored by blocks, the open tiny shapes are worth two to four times their
    score by moves in the full game (3 arrays in 8 moves at m = 3: 0.29 instead of 0.107; 3 in 10 at m = 4: 0.43
    instead of 0.13), if the floor theorem's block count could be met (Table C2).
11. [derived] The engine's group is the Clifford group in other words (section 6); the cut-set lemma's "kept subspaces"
    are its representations; the sub-game is the commutative corner where they are all one-dimensional.
12. State: **turned into a better question.** "How many times must a climb be interrupted" has the answer "once" in the
    sub-game (2 blocks per array, exactly the plain schedule). The open question is the least number of moves per
    array in the sub-game once the pair rule is added to the character inequalities: between 3.75 and 4 at m = 4.

**Growth law in N, as the brief requires.** None came out: no network, so no law n (log n)^z beyond the published one.
What came out are two laws ABOUT laws, both for the sub-game and both unreviewed: a floor (every unit there has at least
2 blocks and, at block sizes 4, 5, 6, at least 3.75, 3.875, 3.9375 moves per live array, so z >= 0.953, 0.842, 0.765), and
the limit of that floor (this family of inequalities can never force more than 4 moves per array, so it can never
exclude z = ln 4 / ln m). Why no network: the one candidate the floor names is excluded by the pair rule (line 9), and I had no other.

## 1. The price law, read once more [ran: `whatif.py`, floats]

Per array the budget is 1. A block of rank k costs (k/m)^z. A block of rank 1 costs m^(-z), about 0.03 at m = 45 and
z = 0.9; shortening the big block by d moves earns about z d / m. So for one big block and j blocks of rank 1 per array the
bar z = 0.9 needs d of about j (m^0.1 / 0.9 - 1) moves saved per array [derived, first order]; exactly, for j = 1
(Table C1, blocks (m - 1 - d, 1)):

| m | d = 0.1 | d = 0.25 | d = 0.5 | d = 1 | d for saving 0.1 | as a share of the moves |
|---|---|---|---|---|---|---|
| 4 | 0.042 | 0.099 | 0.179 | 0.306 | 0.254 | 6.4 % |
| 5 | 0.038 | 0.089 | 0.160 | 0.273 | 0.287 | 5.7 % |
| 9 | 0.030 | 0.071 | 0.128 | 0.216 | 0.373 | 4.1 % |
| 45 | 0.020 | 0.046 | 0.084 | 0.143 | 0.623 | 1.4 % |
| 110 | 0.017 | 0.039 | 0.071 | 0.120 | 0.776 | 0.7 % |

By moves alone the same d gives 0.0006, 0.0015, 0.0029, 0.0059 at m = 45. The published unit saves d = 0.095 moves per
array; in two blocks per array that would be about 0.02, in its 16.5 blocks it is 8.76e-4.
Reading: **the target is not "skip 7.4 % of the directions". It is "skip about half a move per array without cutting the
big block".** That is a much smaller share, and it gets smaller as m grows (like m^-0.9). All of it WHAT-IF.

## 2. (a) The exchange on paper [derived]

The exchange: c1 = D^-1 X; Y1 = Y + c1; c2 = D Y1; X2 = X - c2; c3 = D^-1 X2; Y3 = Y1 + c3. Result X2 = -D Y, Y3 = D^-1 X.
A batched shear reads its source at the *top* (after the h - r moves along its port's perpendicular) and writes its target
at the *bottom* (before those moves); the target then climbs and the unwanted terms are taken off at its top.

**The count.** What cuts a block is an addition INTO the array, or a read at a point where the array must stop (a block
letter is one atomic step). Array X is source, target, source: climb, read; write; climb; removal; climb, read. Three
climbs. Array Y is target, source, target: write; climb; removal, read; write; climb; removal. Two climbs. So x-6's
sentence "every shear touches both arrays, so three blocks" is right for X only: **2.5 per array on average, not 3.**

**The words that break it, and what each costs.**
- *Scratch targets.* Keep free copies X0, Y0 of the arrays at the bottom. Then X2 can be formed in X0 and Y3 in a copy of
  Y1 taken before Y1 climbed. The pair makes four climbs (X, Y1, X2, Y3), each one uninterrupted block of rank h - r: two
  blocks per array. But in one block of h address bits only the climbs of X2 and Y3 end in finished content; the climbs
  of X and Y1 exist only to feed the totals. Cost 4 (h - r) against the plain 2h: a loss unless r is above h/2, where no
  two ports know each other. So the exchange needs every climb to be "owed anyway", and that is what the stages (one
  shear per block of h address bits, m = 3h or 5h) are for. The stage shape, not the block count, is what the three-stage
  what-if 0.078 measures.
- *One shear into an empty array.* Z = D^-1 X is the port move itself; no exchange needed. Cost: X's climb (h - r, to feed
  the total) plus Z's climb (h - r): the same loss.
- *The same array source twice in a row* (shear 2 read from Y1 at the bottom, total moved UP by the whole block, written
  into X at the top): X_top - F Y1 = -F Y exactly, so Y is finished with no climb of its own. Then shear 3 is free
  (Y3 = Y1 - Y0). But the unwanted terms are now other pairs' FINISHED contents F y_s, which nobody else holds: the totals
  are simply the transform of rank(M) sums. This is batching by linearity and gives one output per total. It fails on
  information, not on blocks.
- **A removal that needs no "knowing".** In the commutative part, F = D_t G_t = D_s G_s for all ports, so
  G_t D_s^-1 = D_t^-1 G_s for EVERY pair s, t: the unwanted share of source s in target t, after t has climbed, is one port
  move of t applied to the top of s. So all unwanted terms of target t come off with ONE block of rank r on one scratch
  array holding sum over s of M_ts (top of s), whether t knows s or not. Cost r moves per target: exactly the r moves
  saved. Zero-sum, but with one-block arrays and no helpers, and it shows that "knows" is a way to make that block free
  (the sources pass through the needed label on their way up), not a law. The knows-graph ceilings of section 3 are
  ceilings for x-6's design only.

**So: how many times must a climb be interrupted, and by what?** In every word I could write, by exactly the additions
that bring in or take out another array's content at a label the array has to stand at. The interruptions are not forced
by the exchange (two blocks per array are possible); what is forced is that every climb be useful, and the words with two
blocks waste climbs. Section 4 turns this into a count that can be proved in the sub-game: at least one interruption per
array, always.

## 3. (b) The knows graph of the fat ports [ran, exact: `knows.py`, `mis.py`; outputs `knows_small.out`, `knows_big.out`, `mis_small.out`]

A fat port is a subspace P of dimension r that meets its perpendicular only in 0. Three kinds: "P odd" (P contains odd
words) or "P alternating" (all words of P even; r even), and P-perp odd or alternating (alternating exactly when the
all-ones word lies in P). Two ports know each other when each lies in the other's perpendicular.

Two families of ports no two of which know each other [derived, checked by machine for h up to 7]:
- *star*: all ports through one word (ports that share a non-zero word never know each other);
- *club*: all ports that contain a word of S = x0 + C, where x0 is an odd word and C a self-orthogonal code inside
  x0-perp. Any two words of S overlap oddly, so two ports holding one each do not know each other. |S| = 2^floor((h-1)/2).
For r = 1 the club is the largest possible set (differences of pairwise oddly overlapping odd words span a
self-orthogonal code) [derived]: 16 at h = 9. The published E8 family has 8 among its 120 ports and kappa = 15; the
ceiling for all 256 odd words is 16.

| (h, r) | ports | degree (ports known) | largest set, no two knowing | ceiling on kappa | 3h/(2r) needed | saving at the ceiling, three-stage (merged) | with free shears |
|---|---|---|---|---|---|---|---|
| (5,2) | 80 = 60 odd + 20 alternating | 4 | 24 of the 60 (exact; the club), 10 of the 20 (exact), 34 of 80 (exact) | 2.5 (odd), 2 (alternating) | 3.75 | 0 | 0.094 |
| (6,2) | 336 = 240 + 80 + 16 | 20 | 64 found, at most 69 (of the 240); 40 of 80 (exact); 91 of 336 (exact) | 3.48 to 3.75 | 4.5 | 0 | 0.078 |
| (7,3) | 5,376 = 5,040 + 336 | 8 (0 for the 336) | club 1,904 of 5,040 | at most 2.65 | 3.5 | 0 | 0.101 |
| (8,3) | 43,008 | not run | club 9,856 | at most 4.36 | 4 | 0.0071 (0.0088) | 0.088 |
| (9,3) | 348,160 | not run | club 73,920 of 342,720 | at most 4.64 | 4.5 | 0.0022 (0.0027) | 0.078 |
| (9,4) | 1,462,272 | not run | club 537,600 of 1,370,880 | at most 2.55 | 3.375 | 0 | 0.105 |
| (8,2) | 5,440 | not run | club 504 of 4,032 | at most 8 | 6 | 0.0146 (0.0180) | 0.060 |
| (9,2) | 21,760 | not run | club 1,920 of 16,320 | at most 8.5 | 6.75 | 0.0108 (0.0132) | 0.053 |
| (9,1) | 256 | 128 [derived] (0 for the all-ones word) | 16 (exact, by the argument above) | 16 (17 without the all-ones word) | 13.5 | 0.0044 (0.0051) | 0.029 |

How to read it. "Ceiling" = (ports of one kind) / (largest set no two of which know each other): the number of totals is
at least that set's size because the scatter matrix is the identity on it [the curator's derivation, which I re-derived:
an entry M_ts must be 0 when t does not know s]. For a family that is not one orbit the ceiling is the fractional colouring
number; I give the per-kind numbers. "At most" means the true ceiling may be lower: at (6,2) the club has 60 and the
integer program found 64, so the club is not always the largest. The alternating kind is not caught by the club; its star
bounds are weak (17 at (9,4)), but where it was computed exactly (h = 5, 6) its ceiling is 2. Saving columns:
`whatif.py`, floats; three-stage = per array blocks h-r, h-r, h-r, 2r and 1.5/kappa totals of rank h, m = 3h, no helpers.

**Verdict of the table.** With h at most 9 and x-6's design, the best class is (8,2) at 1.5e-2 and nothing reaches 1e-1.
The classes with r/h near 0.4, where the free-shear ceiling is near 0.1, fail the threshold outright.
**Growth law of the ceiling.** v / club is about 2^(ceil((h+1)/2) - r) (exact values 8.5, 4.64, 2.55 at h = 9 against
8, 4, 2). For r = h/3: about 8, 16, 32, 256 at h = 12, 18, 24, 45, against a threshold of 4.5. So for larger h the count
of totals stops being the obstacle; the three-stage what-if at the ceiling is then 0.034, 0.056, 0.067, 0.077, with limit
0.078 (0.098 merged). No family of fat ports with kappa anywhere near these ceilings is known (x-6 mutation 2).

## 4. The sub-game is a game of switches [derived; linear programs ran, floats]

**4.1 The dictionary.** A move along z is the matrix dir(z) = (1+i)/2 + (1-i)/2 shift(z) [read: GAME.md]. All of these and
all shifts commute. Take f digit columns and in each column a sign pattern x -> (-1)^(y.x); the product of these patterns
is a common eigenvector, on which dir(z) acts as i^(number of columns whose y has y.z = 1) and shift(z) as a sign.
For every quadratic form Q on the address bits there is a choice of columns with dir(z) -> (-1)^Q(z) and every shift -> +1:
for the term z_1 take two columns y = e_1; for the term z_1 z_2 take columns e_1, e_2 and three times e_1 + e_2
(because 2 z_1 z_2 = z_1 + z_2 - [z_1 + z_2 odd]). So Q needs a bounded number of columns, and the engine demands every
number of columns. On that eigenvector a block along z_1..z_k acts as (-1)^<Q,B>, with <Q,B> = Q(z_1) + ... + Q(z_k)
modulo 2, and the kernel as (-1)^(Q(e_1) + ... + Q(e_m)) = (-1)^<Q,I>.
The same in matrices: modulo the shifts the group generated by the moves is the group of symmetric bit matrices under
addition; a move along z is z z^T, a block along independent z_1..z_k is B = sum z_j z_j^T (rank k, not alternating), the
kernel is I. [read: x-6 line 3, in other words: the product of moves along a basis equals the kernel exactly for the bases
with Z Z^T = I.] A fat port P is the projection matrix onto P; "climb all but the port" is I + (projection), of rank h - r.

**4.2 The inequality.** Fix Q and look at the program on that eigenvector, and on the eigenvector with y = 0 in every
column (same number of columns), where every move, shift and the kernel act as +1. On both, an addition is the same
rational matrix on the list of arrays and a shift is 1; a block is "multiply one array by -1" on the first when
<Q,B_j> = 1, and nothing otherwise. So the two programs differ by a matrix of rank at most the number of blocks with
<Q,B_j> = 1, and on the W live arrays that difference must be -2 times the identity whenever <Q,I> = 1:

  **for every Q with <Q,I> = 1:  #{ blocks j : <Q,B_j> = 1 } >= W.**

Averaging over all such Q: every block form other than 0 and I is active for exactly half of them, and a block has rank at
most m - 1, so it is never I. **Hence at least 2W blocks.** The plain schedule (blocks m - 1 and 1) meets it.
**The brief's floor question** ("can any array in any legal network make ONE block of rank below m") has to be asked of
the total, because a free copy moves an array's second block onto a scratch array. Asked of the total: in the sub-game
the answer is no, with room: 2 blocks per live array, never fewer. In the full game only the floor theorem's
1 + 2^-m is known [read]; the gap between 1 + 2^-m and 2 is exactly what address maps and phase letters would have to
buy, and nobody has a unit that buys any of it at small size.
[ran, exact, `check_eig.py`] The dictionary of 4.1 was checked on the engine's own matrices at m = 2 and 3 for all 8 and
64 quadratic forms: on the prescribed columns every move acts as (-1)^Q(z), every shift as +1, the kernel as (-1)^<Q,I>.
Also [derived]: the number of active blocks has the parity of W for every such Q, that is sum of all B_j = W I modulo 2
(a determinant).
This is the tiny-unit notes' cut-set lemma (W x dem <= sum of cap) for the one-dimensional kept subspaces; what is new is
that in the sub-game the whole family is explicit, so the best bound is a small linear program.

**4.3 The linear program** [ran: `lp.py` (all forms, m = 2, 3, 4) and `lp_sym.py` (reduced by the address maps that keep
I; m = 3, 4, 5, 6); the two agree at m = 3 and 4; HiGHS, floats]. Minimise the cost of a multiset of block forms subject
to the inequalities.

| block size m | least moves per array | least blocks per array | least exponent z the inequalities allow | largest saving | the minimiser |
|---|---|---|---|---|---|
| 2 | 2 | 2 | 1 | 0 | plain |
| 3 | 3.000 | 2 | 1 | 0 | plain-like |
| 4 | 3.750 | 2 | 0.9534 | 0.0466 | every direction once, 4 arrays in 15 moves |
| 5 | 3.875 | 2 | 0.8416 | 0.1584 | every direction once, 8 arrays in 31 moves |
| 6 | 3.9375 | 2 | 0.7649 | 0.2351 | every direction once, 16 arrays in 63 moves |

Exact check [ran, `lp_cert.py`, fractions]: the float program's dual weights, rounded to fractions, are 3 characters of
weight 1 at m = 3 and 14 characters with weights in halves, quarters and eighths at m = 4 (each with exactly 4 active
directions), total 15/4; for every one of the 540 block forms the weight of the characters on which it is active is at most
its rank. Adding the inequalities of 4.2 with these weights gives **at least 15/4 moves per live array at block size 4**,
with no floats left in the argument. The m = 5 and 6 values and all price values are floats.
By hand at m = 3 [derived]: the three forms Q1 = z1 + z1 z2 + z1 z3 + z2 z3 and its two images under exchanging the bits
are active on {100, 011}, {010, 101}, {001, 110}; each direction is active for at most one of the three, so 3W <= moves.
That is the cut-set note's "k >= 3W at block size 3" (there for a larger class: phase letters allowed).
In general [derived]: a non-zero quadratic form has at least 2^(m-2) ones (the minimum distance of the second Reed-Muller
code; checked at m = 4, 5 by `tight.py`), so "every direction once" serves W = 2^(m-2) arrays in the program:
(2^m - 1)/2^(m-2) = 4 - 2^(2-m) moves per array. The program's optimum is that number at m = 4, 5, 6 [ran]; for larger m it is at most
that number [derived]. **So this family of inequalities can never prove more than 4 moves per array, and it allows the exponent to
fall like ln 4 / ln m.**
In the program a block of rank k is one switch and costs more than a move; the minimisers use single moves only. Big
blocks are valuable in the full game for a reason the sub-game does not have (in a larger representation a block of
rank k changes many dimensions at once: that is the floor theorem's weight 1 - 2^-k).

**4.4 The object the program names.** [derived] A unit of the sub-game with single moves is, once the additions are
absorbed (they are invertible when there is no scratch): a list of directions z_1..z_B
and matrices P_j = u_j v_j^T (v_j.u_j = 1) on the W + S arrays such that for every character psi of the group,
product over j of (1 + (psi(z_j) - 1) P_j) maps (x, 0) to (psi(kernel) x, anything). The candidate: B = 2^m - 1, all
directions, W = 2^(m-2).
- [derived] *The program as a branching program.* Write x_j for
  (move j) - 1, X for the diagonal matrix of the x_j, and let L (W x B), R (B x W) and T (B x B, zero unless the row's
  move comes later than the column's) be rational matrices: L_j = what the live arrays finally receive from switch j,
  R_j = what switch j reads from the inputs, T_ij = what switch i reads from switch j. With enough scratch arrays these
  are free, and the program is  1 + L X (1 - T X)^-1 R.  **A unit of the sub-game with B single moves for W arrays is a
  triple (L, T, R) with  1 + L X (1 - T X)^-1 R = (kernel) x identity  in the group algebra**; on a character every x_j
  is 0 or -2. This is a branching program whose NODES carry the moves, computing W copies of one element at once: the
  unit question in the sub-game is a direct-sum question (can W copies be had for fewer than W times the nodes of one),
  with the relations of the group as the only source of sharing. For fixed T and R the equations are linear in L, so
  an exact search is: choose the time order and T, R over small rationals, solve for L.
- [derived, ten minutes old; the pair count ran exactly, `tight.py`] **The pair rule.** Take a tight character (exactly W
  active moves, set A, and <Q,I> = 1). Its equation is L_A (1 + 2 T_A)^-1 R_A = 1 with L_A and R_A square of size W. So
  both are invertible and R_A L_A = 1 + 2 T_A: for moves i, j of A, (row R_i).(column L_j) is 1 when i = j, 0 when i comes
  before j, and 2 T_ij when i comes after j. Now K = R L is one B x B matrix of rank at most W for the whole program.
  **Hence any set of moves that pairwise share a tight character has at most W members** (on it K is triangular with
  ones on the diagonal). The plain schedule meets this with equality (moves of different arrays share tight characters,
  moves of one array never do). For "every direction once" the tight characters are the affine subspaces of
  codimension 2 that miss 0 and hold an odd number of unit words: 56 at m = 4, 240 at m = 5, and every two directions
  lie together in one (105 of 105, 465 of 465 pairs). All 2^m - 1 moves would be such a set: impossible, 15 > 4, 31 > 8.
  This holds for any number of scratch arrays. (My first version of this argument, for no scratch arrays only, went
  through switches that annihilate each other pairwise; the pair rule replaces it.)
  [ran, floats, `pairrule_check.py`] One test of the rule on something that knows nothing of it: the two solutions the
  least-squares hunt found for the plain pattern (4 arrays, 16 moves, m = 4). There the tight characters are "the four
  copies of one direction". Prediction: R_p.L_q = 0 for an earlier and a later copy of the same direction. Found:
  2.5e-13 and 1.5e-15 at most, while pairs of different directions, which the rule does not bind, go up to 8.4 and 27;
  rank of K = 4 in both.

**4.5 The hunt** [ran, floats, `refl.py`; NOT a proof either way]. Least squares over the matrices P_j for a random order
of the 15 directions, 4 live arrays, on the 1,024 characters with values +1, -1 (then to be checked on all 16,384).
Controls: 2 arrays in 6 plain moves at m = 3 is found to 4e-15 on all characters; a 5-move list for 2 arrays stalls at
error 0.5. Then at m = 4, 4 live arrays, "every direction once", each try a new random order of the 15 moves:
- my own least-squares loop (`refl_lm.py`; on the plain 16-move pattern it reaches 1e-13 in 2 of 6 random starts):
  1 scratch array, 1 try, error 0.37; 2 scratch arrays, 8 tries, errors 0.36 to 0.65; 8 scratch arrays, 1 try, 0.65;
- the library solver, 60 evaluations per try (`refl.py`; on the plain pattern it reaches 8e-2, 3e-4, 5e-7, 5e-4 in four
  tries, all still falling): 3 scratch arrays, errors 0.32 and 0.37 in the tries finished when I stopped looking.
No solution. By the pair rule of 4.4 there is none to find; the hunt agrees with it and proves nothing by itself.

## 5. (c) The tiny game scored by blocks [ran: `whatif.py`, floats; WHAT-IF]

No unit that saves a move is known at block size 3, 4 or 5 in any game [read: tiny/next/NOTE.md], and a block list whose
ranks add up to W m certifies nothing whatever its grouping [read: GAME.md section 4]. So there is no word to re-score; I
scored the open SHAPES instead: W arrays in k moves, cut into single moves (the score every search printed) against the
best grouping into blocks that the floor theorem allows in the full game (sum of (1 - 2^-rank) >= W (1 - 2^-m)).

| m | shape | moves per array | score by moves | best by blocks, full game | block ranks |
|---|---|---|---|---|---|
| 3 | 3 arrays in 8 | 2.667 | 0.107 | 0.290 | 2,2,2,2 |
| 4 | 3 in 10 | 3.333 | 0.132 | 0.430 | 3,3,3,1 |
| 4 | 3 in 11 | 3.667 | 0.063 | 0.239 | 3,3,3,2 |
| 4 | 4 in 15 | 3.750 | 0.047 | 0.224 | 3,3,3,3,3 |
| 5 | 2 in 9 | 4.500 | 0.066 | 0.261 | 4,4,1 |
| 5 | 4 in 17 | 4.250 | 0.101 | 0.484 | 4,4,4,4,1 |
| 5 | 8 in 31 | 3.875 | 0.158 | 0.724 | 4 x 7, 2, 1 |

Reading: in the full game a shape that saves ONE move can be above the bar if its moves sit in W + 1 blocks (3 in 11 at
m = 4: 0.24; 2 in 9 at m = 5: 0.26). The searches of the full game ranked shapes by moves and stopped at the bar by
moves (3.48 moves per array at m = 4); by blocks, shapes up to 3.9 moves per array are of interest.
In the sub-game the picture is the opposite (section 4): the grouping cannot help beyond the program's bound, 0.0466 at
m = 4 and 0.158 at m = 5 (the "sub-game" column printed by `whatif.py` uses only "at least 2W blocks" and is superseded
by the linear program).

## 6. The group is the Clifford group [derived, minutes old; one number checked]

dir(z) is a quarter turn about the Pauli operator "X on the bits of z"; a phase letter is a quarter turn about a Z-type
Pauli operator; a shift is an X-type Pauli operator; an address map is a circuit of controlled-NOT gates. So the free maps
are the Clifford operations that permute the addresses up to phases, the paid letters are the quarter turns of X type, and
the kernel is a Hadamard gate on every bit up to free maps. The quotient (all) / (free) has 371,589,120 / 2,752,512 = 135
elements at m = 3 [arithmetic on GAME.md's two numbers], which is the number of maximal self-orthogonal subspaces of six
bits under the symplectic form, 3 x 5 x 9. The sub-game's symmetric matrices are the cell of those subspaces that are
graphs. Use: the cut-set lemma for the full game is "for every representation rho of this group, sum over blocks of
rank(rho(block) - 1) >= W rank(rho(kernel) - 1)", and the representations of the Clifford group on f columns are known
objects (the commutant of its tensor powers is spanned by self-dual codes). d-4 (self-dual codes) and the tiny-unit
cut-set search were looking at the same list.

## 7. What failed, and what I changed

- *"Minimise blocks in the tiny game"* (the brief): there is no unit to score. What it is made of: a grouping only matters
  once a move is saved. Changed to: score the open shapes (Table C2), and ask which shapes are worth searching by blocks.
- *"The exchange leaves three blocks"*: two are possible; the failure is wasted climbs, not interruptions. Changed to: ask
  for the floor on interruptions directly. That gave the switch picture and "2 blocks per array" in the sub-game.
- *"The knows graph caps kappa"*: at small h yes; the cap grows like 2^(h(1/2 - r/h)). Changed to: the cap is the stage
  shape. And the removal identity of section 2 shows the knows relation is a discount, not a law.
- *"Big blocks are the lever"*: true for the price, false in the sub-game's inequalities, where a block is one switch.
  The lever in the sub-game is the opposite one: many single moves, each direction once.

## 8. Mutations

1. `pair-rule-program`: add the pair rule to the character inequalities and solve in whole numbers at m = 4 and 5:
   is there any multiset of moves for W arrays with fewer than m W moves in which every character with <Q,I> = 1 has at
   least W active moves and no W + 1 moves pairwise share a tight character? A "no" for all small W would be the first
   sign that the sub-game has no unit at these sizes; a "yes" names the next object. The same two tests applied to the
   published unit (if it can be written without address maps and phase letters, which I did not check) would be a test
   of this whole section.
2. `lp-with-phases`: add phase letters (the group is then no longer commutative; representations of dimension 2^j). Does
   3.75 at m = 4 survive? The cut-set note has 3.058 there.
3. `lp-full-game`: the same program over the representations of the Clifford group (section 6) at m = 3: is 3 arrays in
   8 moves excluded, and what is the least price by BLOCKS there?
4. `half-a-move`: units for the full game that save about half a move per array with every array in two blocks
   (Table C1): search with the block price as objective, at m = 4 the shapes 3 in 11 and 4 in 15.
5. `removal-by-one-block`: section 2's identity gives a design with one-block arrays and no helpers that is exactly
   zero-sum. Find the cheapest way to batch the v removal blocks (they are again "one port move per array").
6. `club-families`: is there a family of fat ports whose scatter has rank near the club's size? (x-6 mutation 2, now
   with the target number: v / 2^(ceil((h+1)/2) - r).)

## 9. Criticism, last

- **Section 4 is an hour old and unreviewed.** The inequality rests on: (i) moves and shifts commute and their common
  eigenvectors over f columns give every character used (checked exactly on the engine's matrices at m = 2, 3 by `check_eig.py`; no word was replayed
  with `regmachine.py`); (ii) the program is the identity at zero columns; (iii) a block is one rank-one change. The m = 3
  value agrees with the cut-set note and the plain schedule meets every bound with equality, which is a check of the
  set-up, not of the m = 4 and 5 numbers. The linear programs are floats.
- The sub-game here has **no phase letters**; the tiny-unit notes' sub-game has them. My 3.75 at block size 4 is a
  stronger number for a smaller class than their 3.058. The published units use address maps and are outside both.
- "At most 0.0466 at m = 4" bounds what the engine certifies for units of this sub-game only.
- The linear program's minimiser is fractional. "Every direction once" is a solution of the inequalities, not a unit, and
  the pair rule says it is not one. **The pair rule is ten minutes old.** It rests on the form
  1 + L X (1 - T X)^-1 R of a program with single moves (derived by following what each move reads and what the outputs
  receive; blocks of rank above 1 need one line more: a block is one switch, so the same form holds with one x per
  block) and on one float test (`pairrule_check.py`). A skeptic should start there.
- Table B: only (5,2) and parts of (6,2) are exact; the rest are upper ceilings from one explicit family; the alternating
  kind has only star bounds. The ceilings assume x-6's design (unwanted terms removed only for known sources); section 2
  itself shows a removal outside that design. Savings at the ceiling use x-6's three-stage block list, which nobody has
  built for fat ports.
- Section 2 is paper. I did not reconstruct the five-stage word, so "two of four climbs are wasted" is a statement about
  the exchange in one block of address bits, not about the published design.
- Section 6: the dictionary is derived; one index was checked. The sentence about the commutant is from memory.
- Tables C1 to C3 are what-if counts. The floor theorem used in C2 is itself "argued", not proved [read].
- Nothing here is a circuit, a network, or a change of order.

Files: `waves/wave-08/ab-1-fewerblocks/`: knows.py, knows_small.out,
knows_big.out, knows_4_2.edges to knows_7_3.edges (ports, kinds, degrees, club and star families); mis.py, mis_small.out
(exact largest sets, integer program, run on the Linux machine); whatif.py, whatif.out (all what-if tables, floats);
lp.py, lp_234.out, lp_sym.py, lp_sym_345.out, lp_sym_6.out (the character floor as a linear program); lp_cert.py,
lp_cert.out (exact certificate of the moves bound at m = 3, 4); check_eig.py, check_eig.out (the dictionary on the
engine's matrices, exact); tight.py (tight characters, exact); pairrule_check.py, pairrule_check.out, refl_lm_m4_W4_S0_try1.npy, try2.npy (test of
the pair rule on found plain solutions); refl.py, refl_lm.py,
refl_controls.out, refl_lm_*.out, refl_scipy_*.out (the numerical hunt and its controls; refl_4_4_0.out and
refl_4_4_2.out are two runs stopped before their first result).
