# ad-0 rateperblock: which blocks of the published unit carry its saving, and at what rate

11 October 2026, 06:22 to 07:10 EDT, one agent, 60-minute box. Private research: nothing published, no git, no
Lean, nobody has read this. **No circuit below any known count and no growth law below N log N beyond the published
one. Nothing here changes the order. The bar of 1e-1 is not alive in the published mechanism; section 5 says by how
much and names the two integers that keep it out.**
Marks: [ran] = run of mine tonight (programs and outputs in `ad-0-rateperblock/`); counts of blocks and moves are exact
whole numbers; every saving, root and charge is a FLOAT (bisection on a sum of powers) and is called so; `shears.py`
is exact arithmetic (Gaussian rationals, and two small finite fields where it says so); `sector.py` is modulo
primes, a candidate-or-absence test only, and says so. [read] = in a file I
opened tonight; [derived] = by hand tonight, checked by nobody; [recalled]; [guess].
Unit of cost: the engine's **moves** and **blocks**. Gate counts (G) and (O) are not used anywhere.
**LEGAL** = a block list with a network behind it that the engine's checker accepts. **WHAT-IF** = a block list with no
network. The two are kept apart in every line.

Words. *Array*: one working copy of data. *Move*: one direction of the transform applied to one whole array. *Block*:
a run of moves on one array with no addition in between; its *rank* is its number of moves. m = moves every array is
owed (the *width*); W = number of arrays. *Price law* (the engine's own): the saving is e = 1 - z, z the root of
"sum over all blocks of (rank/m)^z = W". *Plain schedule*: two blocks per array, ranks m - 1 and 1; it saves nothing.
*Unit*: the published network: 4v *data arrays* in pairs, R *helper* arrays (they hold partial sums and make all m
moves), and *scratch copies* (extra blocks that belong to no array). *Stage*: one of the five groups of h directions
(m = 5h); an *invocation* is one run of the helper circuit in one stage. *Role climb*: the h - 1 moves a data array
makes in a stage in which it is a source (x) or a target (y). *Shear*: target += (a multiple of the source moved along
one direction). *Credit*: moves skipped against the plain schedule. *Charge* of a block at exponent z:
m (rank/m)^z - rank, in moves; it is 0 at z = 1.

## 0. The answer in twelve lines

1. [ran, exact counts, LEGAL] **All the credit of the unit sits in the data arrays; they are 38 % of the arrays and
   18 % of the blocks.** Fourth result (h = 9, m = 45): data arrays 480 moves skipped on 3,810 blocks, helpers 0 moves
   on 16,980 blocks, copies -360 moves on 40 blocks; unit 120 on 20,830.
2. [ran, LEGAL] **Rates.** Data arrays: 0.126 of a move per block, 0.168 per block beyond the plain schedule's two.
   Helpers: exactly 0. Copies: -9 moves per block. Unit: 0.0058. Second result (m = 110): 0.093 / 0.114, 0, -20,
   0.0085. First result (m = 80): 0.103 / 0.129, 0, -15.1, 0.0054. So aa-cross's "0.006" is a data-array rate of
   0.13 to 0.17 diluted 22 to 29 times by helper blocks and copies. It is not overhead all the way down.
3. [derived; checked to 3 decimals by the run] **The law is an exact ledger in moves:**
   (charge of every block of a live array) + (whole price of every scratch copy) = 4v, the moves the data arrays skip.
   At the unit's own root the 480 are spent: copies 75.1 %, helpers 18.3 %, data arrays 6.6 % (second result: 41.7,
   44.9, 13.4). [FLOATS, LEGAL]
4. [derived + ran] **The law charges entropy, not a count of blocks.** To first order the charge of a block of rank r
   is e r ln(m/r), so saving = D / S with S = sum of r ln(m/r) ("move-nats") and D the moves saved: 120 / 136,782 =
   8.773e-4 against the exact root 8.762e-4. The unit pays 1,140 move-nats per move saved; its data arrays alone 75;
   the bar of 1e-1 allows about 10; the plain schedule alone costs 4.8 per array.
5. [derived, exact] **The bar, block by block.** Give every block the share beta of its array's m moves that it stands
   for. A block pays for itself at saving e exactly when it leaves out at least the fraction 1 - beta^(e/(1-e)) of
   those moves. For 1e-1: 7.4 % for half an array, 11.5 % for a third, 16.4 % for a fifth, 34 % for a single move of
   45, and 0.25 % for a block that stands for 44 of 45. Big blocks pay with tiny skips; single moves can never pay.
6. [ran, FLOATS] **Where an interruption falls decides its price.** One extra cut of a plain array costs, at 1e-1 and
   m = 45, 0.56 of a move one step from an end, 2.2 at 8 steps, 3.2 in the middle (m = 110: 0.70, 3.2, 7.8).
   aa-cross's 0.63 is the cheapest place only. The published unit cuts its data arrays at the stage boundaries.
7. [ran, FLOATS; every number but the last is a WHAT-IF, the last is LEGAL] **The cascade from the best block to the unit (h = 9):** a role
   climb taken whole leaves out 1 of 9 directions and would alone give 6.82e-2 -> the word pays 4 of 5 back: 1.58e-2
   -> cuts inside the climbs: 1.31e-2 -> helpers: 3.51e-3 -> copies: 8.76e-4. Factors 4.33, 1.20, 3.74, 4.00. Second
   result: 2.81e-2 -> 6.58e-3 -> 5.55e-3 -> 1.28e-3 -> 7.47e-4 (4.27, 1.19, 4.33, 1.71).
8. [derived + ran exactly] **Why the word pays back, and why three.** In the sector where the move acts as -1 every
   shear is a transvection (identity plus a matrix of rank 1), and giving n arrays one free move each means writing
   the matrix -1 as a product of them. -1 is never a product of n transvections (three lines, section 5); n + 1
   suffice. So an exchange needs at least n + 1 shears for n free moves (3 for a pair, 5 for the bridged word's two
   pairs: both published words are optimal) and at least 3 stages, since a stage holds n/2 shears. Net skip of a
   stage block: at most r/(3h), r the port dimension.
9. **The wall, in two integers.** 3 (line 8) and x-6's r <= h/3: the best stage block leaves out 1/9 = 11.1 % of its
   stage; a third of an array needs 11.5 %. That is x-6's ceiling 0.098, now with a reason for each factor. With
   helpers and copies in, nothing is near.
10. [ran, FLOATS, WHAT-IF] In the published unit moves are scarce and blocks are not: one more skipped move per data
    array multiplies the saving by 5.0; merging every helper into one block per invocation by 1.46; merging helpers'
    single moves in pairs by 1.05.
11. Mutations: section 8. The one that bears on the order: a free step that tells the sector +1 from -1. First
    case tried [ran, modulo primes]: address maps and sign patterns acting alike on all columns do not supply one at
    2 bits per column (two and three columns, two primes) nor at 3 bits per column (two columns, one prime).
12. State: a wall I can name.

**The one sentence.** Yes: in the three published units (LEGAL) the data arrays' blocks are above 0.1 of a move per
block beyond the plain schedule's two (0.168 in the fourth result, 0.114 in the second, 0.129 in the first; per block
0.126, 0.093, 0.103; four further block lists of the E8 search, not checked by me, give 0.17 to 0.26), the helpers'
blocks are at exactly 0, the copies at -9 to -20 and the units as wholes at 0.005 to 0.009, while the bar of 1e-1
needs 0.63 of a move per single-move block at width 45 (0.72 at 80, 0.78 at 110) and, for blocks of the size the data
arrays really have, 1.5 moves per role climb at width 45 (3.8 at width 110) against the 0.2 that the five-stage word
leaves each stage block after paying back.

## 1. The classes of the legal unit [ran: `ledger.py`, `ledger.out`; exact counts]

I replayed the frame ids of each certificate to get the ordered block ranks of every register of one invocation; the
histograms equal the stored ones (asserted), and the roots are the published 8.7625e-4 and 7.4745e-4 (FLOATS).
The unit's list is 5 invocations plus the idle blocks of the twins [read: `R/tools/gx/gxunit.py`].

Fourth result, h = 9, v = 120, R = 783, m = 45, W = 1,263, D = 120 moves saved of 56,835:

| class | blocks | per array | moves | move-nats S | ranks (rank: count) |
|---|---|---|---|---|---|
| x-role climbs (5 invocations) | 1,415 | 2.95 | 4,800 | 11,032 | 1:590 2:160 3:105 4:15 5:75 6:250 7:120 8:100 |
| y-role climbs (5 invocations) | 1,435 | 2.99 | 4,800 | 11,591 | 1:400 2:185 3:170 4:270 5:90 6:260 7:50 8:10 |
| idle and catch-up | 960 | 2.00 | 11,520 | 13,503 | 20:240 16:240 8:240 4:240 |
| **data arrays (the three above)** | 3,810 | 7.94 | 21,120 = 480 x 44 | 36,126 | |
| helpers (5 invocations) | 16,980 | 21.69 | 35,235 = 783 x 45 | 100,077 | 1:9465 2:2675 3:2315 4:415 5:910 6:1145 7:45 8:10 |
| scratch copies | 40 | not arrays | 360 | 579 | 9:40 |
| **unit** | 20,830 | 16.49 | 56,715 | 136,782 | |

Second result, h = 22, v = 1,320, R = 9,412, m = 110, W = 14,692, D = 3,080 of 1,616,120: data arrays 56,760 blocks
(10.75 per array; x-role always 2, 18, 1; y-role always 18, 1, 1, 1), helpers 304,535 blocks (32.36 per array), copies
110 blocks of rank 20; unit 361,405 blocks.

How one invocation is cut [ran, exact]: fourth result, x-role climbs of 8 moves: commonest patterns 1-1-6 (34 arrays),
1-7 (24), one block of 8 (20), 2-6 (16); y-role: 6-1-1 (25), 4-4 (20), 6-2 (15). Helpers: 4.34 blocks per invocation
(3 blocks: 142 helpers, 4: 360, 5: 195); commonest 6-1-1-1 (104), 3-3-1-1-1 (71). A helper costs 25.6 move-nats per
invocation on average, between the least possible (one block of 9: 14.5) and the most (nine single moves: 34.3).

## 2. The ledger and the rates [ran: `ledger.out`, `brief.out`; charges are FLOATS on exact counts; LEGAL]

Identity [derived from the law by subtracting the moves]: sum over live blocks of [m (r/m)^z - r] + sum over copies of
m (r/m)^z = 4v. The run gives 480.000 and 5280.000.

| at the unit's own root | fourth result | second result |
|---|---|---|
| credit (moves the data arrays skip, one each) | 480 | 5,280 |
| spent on the copies (their 360 / 2,200 moves and their charge) | 360.5 = 75.1 % | 2,202.8 = 41.7 % |
| spent on the helpers' blocks | 87.8 = 18.3 % | 2,369.2 = 44.9 % |
| spent on the data arrays' own blocks | 31.7 = 6.6 % (x 2.0, y 2.1, idle 2.5) | 708.0 = 13.4 % |

| block list (first three LEGAL) | saving (FLOAT) | unit, per block | data arrays, per block / beyond two per array | helpers | copies | bar at this width |
|---|---|---|---|---|---|---|
| fourth result (h = 9) | 8.7625e-4 | 0.0058 | 0.126 / 0.168 | 0 | -9 | 0.626 |
| second result (h = 22) | 7.4745e-4 | 0.0085 | 0.093 / 0.114 | 0 | -20 | 0.778 |
| first result (h = 16) | 5.3992e-4 | 0.0054 | 0.103 / 0.129 | 0 | -15.1 | 0.722 |
| `others/covering` (R = 2,366) | 3.9240e-4 | 0.0031 | 0.169 / 0.256 | 0 | -9 | 0.626 |
| `others/transplant` (R = 1,670) | 5.0732e-4 | 0.0036 | 0.142 / 0.198 | 0 | -9 | 0.626 |
| `others/triangle-top` (R = 1,159) | 6.8052e-4 | 0.0050 | 0.127 / 0.171 | 0 | -9 | 0.626 |
| `others/triangles` (R = 1,475) | 5.5352e-4 | 0.0037 | 0.132 / 0.180 | 0 | -9 | 0.626 |

The last five rows use the stored histograms only; I did not run the engine's checker on them. Their roots equal the
figures in their file names, and the first result's equals its published figure.
Gross view of the data arrays [read: `R/tools/gen/foldlib.py`, list B2u: every data array makes five stage climbs of
h - 1 and one catch-up block of 4]: each of the 10v role climbs leaves out one direction, 0.42 of a move per block of
the x and y classes (0.33 and 0.25 in the second result); the idle class nets -0.75 per block. Net: 5 left out, 4 paid
back, 1 kept per array, 0.2 per stage block.
The bar 0.626 is for single moves cut off the end of an array. The data arrays' blocks are not of that kind. In their
own terms [ran, FLOATS, ranks held fixed]: at 1e-1 the data arrays' blocks would be charged 8.4 moves per array
(second result 20.1, first 15.4) against the 1 they skip; the whole unit 12.5 moves per array (32.8; 23.8) against
0.095 (0.210; 0.111).

## 3. The law read block by block [derived; tables ran: `shape.py`, `shape.out`, FLOATS; no certificate involved]

- **Entropy.** Charge of a block of rank r at saving e: m^e r^(1-e) - r = e r ln(m/r) + O(e^2). Summed over an array
  it is m times the entropy (in nats) of the way the array's moves are cut into blocks. So
  **saving = (share of moves skipped) / (mean entropy of the cutting)** to first order: fourth result 0.002111 /
  2.407 = 8.77e-4. The plain schedule has entropy 0.107; five equal stage blocks have ln 5 = 1.609.
- **Chain rule.** Cutting a block of B moves into a and b costs a ln(B/a) + b ln(B/b): cheap when one piece is tiny or
  B is small. Measured on the fourth result [ran]: the five-stage structure costs 13.9 move-nats per stage block of a
  data array and 14.5 per stage block of a helper; a cut inside a stage costs 3.7 and 3.3. Of the unit's 136,782
  move-nats, 63.5 % are the stage structure itself (helpers 41.5, data 22.0), 36.1 % are cuts inside stages (helpers
  31.7, data 4.4), 0.4 % the copies. (The copies cost on the credit side, not here.)
- **Self-paying blocks** (line 5 of section 0). Exact: the law holds as soon as every block has rank <= m beta^(1/z).
  In moves, a stage of h directions in a word of s stages must leave out h (1 - s^(-1/9)) for 1e-1: 1.47 of 9 with
  five stages, 1.03 of 9 with three, 0.67 of 9 with two.
- **The published stage block taken whole** leaves out exactly 1 of h and would pay for itself at
  e_block = ln(h/(h-1)) / ln(m/(h-1)) [WHAT-IF]: five stages 0.068 at h = 9 (0.102 at h = 6, 0.152 at h = 4); three
  stages 0.097 at h = 9; two stages 0.145 at h = 9, 0.104 at h = 13. So the rate of the best kind of block is at 68 %
  of the bar in skipped share (11.1 % against 16.4 %) before any loss. Everything after that is loss.
- **How many helpers a data array can afford** [WHAT-IF]: with data arrays at the 0.068 above and g helpers per data
  array, each one block of h per stage: 0.055, 0.046, 0.034, 0.026 at g = 0.25, 0.5, 1, 1.63 (the fourth result has
  1.63). With helpers on the plain schedule instead: 0.067, 0.066, 0.064, 0.061. The helpers' cost is their being cut
  into five stage blocks, not their number.

## 4. Marginal what-ifs: delete or merge one class [ran, FLOATS; every row except the first is a WHAT-IF]

| block list (h = 9, m = 45) | W | blocks per array | moves saved per array | saving |
|---|---|---|---|---|
| LEGAL: the unit | 1,263 | 16.49 | 0.095 | 8.7625e-4 |
| copies deleted | 1,263 | 16.46 | 0.380 | 3.5071e-3 |
| helpers deleted, copies kept | 480 | 8.02 | 0.250 | 3.2582e-3 |
| helpers and copies deleted (data arrays as cut) | 480 | 7.94 | 1 | 1.3105e-2 |
| the same, x-role climbs whole / y-role climbs whole / both | 480 | 6.24 / 6.20 / 4.50 | 1 | 1.419e-2 / 1.443e-2 / 1.576e-2 |
| the same, catch-up block merged into a neighbour | 480 | 4.00 | 1 | 1.679e-2 |
| nothing paid back: five blocks of 8 per data array (no word does this) | 480 | 5.00 | 5 | 6.819e-2 |
| unit, every helper one block of 9 per invocation | 1,263 | 6.15 | 0.095 | 1.2831e-3 |
| unit, helpers on the plain schedule, copies deleted | 1,263 | 4.26 | 0.380 | 1.1880e-2 |
| unit, helpers' single moves merged in pairs | 1,263 | 12.75 | 0.095 | 9.204e-4 |
| unit, helpers' blocks merged across the four stage boundaries | 1,263 | 14.01 | 0.095 | 9.333e-4 |
| unit, one more move skipped by every data array | 1,263 | 16.49 | 0.475 | 4.3612e-3 |

The same rows for the second result are in `ledger.out` (copies deleted 1.2815e-3; helpers and copies deleted
5.5451e-3; climbs whole 6.5794e-3; nothing paid back 2.8093e-2).
The two shapes of the brief [FLOATS, WHAT-IF]: ab-1's (m - 1 - d, 1) at m = 45 gives 1.89e-2 with the unit's
d = 0.095, 6.67e-2 with d = 0.38 (no copies) and 0.1425 with d = 1, the data arrays' own rate; the bar there is
d = 0.623. ab-6's bystander word with the catch-up merged (h = 9, m = 18, three arrays, shears and helpers free) has
1.67 blocks per array and d = 2 at r = 3 (saving 0.2045, rate 3.0 per block beyond one, bar 0.483) and d = 0.667 at
r = 1 (0.0747, rate 1.0). Both what-ifs sit above the bar in rate; neither has a network.

## 5. Why four of five are paid back: the exchange as a product of transvections [derived; `shears.py` exact]

Setting [read: x-6 section 1]. In phased form the move along a direction is D = a + b * shift with a = (1+i)/2,
b = (1-i)/2, and D^2 = the shift, a free relabelling. On f digit columns the move is the f-th tensor power. A shear is
target += c D^(+-1) source. Free steps are sums of whole arrays with scalar coefficients. Goal for n arrays: every
array ends holding D^(+-1) of one data array (free steps may sort out which).
- [ran, exact] D has the eigenvalues 1 and i on one column, and 1, i, -1 from two columns on (all four fourth roots
  of 1 from three). The three-shear exchange Y += D^-1 X; X -= D Y; Y += D^-1 X gives X = -D y, Y = D^-1 x at
  f = 1, 2, 3.
- [ran, exact] **On one column a two-shear exchange exists**: premix X = x + u y with u = (i-1)/2 (free), then
  Y += D X, X -= D^-1 Y, and a free clean-up. It works because D^-1 is a combination of 1 and D there. It is worth
  nothing (two calls for two moves) and **its last step is impossible from two columns on**, where 1, D, D^-1 are
  independent. This is the floor note's "one column: everything is free" seen in the exchange.
- [derived] Restrict to the part of the data on which D acts as -1 (it exists from two columns on). There D^-1 = -1
  too, every shear is the matrix 1 - c e_t e_s^T against 1 + c e_t e_s^T on the part where D = 1, and the free steps
  are the same matrices on both parts. Comparing the two parts: the goal says (word at D = -1) = -(word at D = 1),
  and the quotient of the two is a product of k transvections, k the number of shears. So **-1 must be a product of k
  transvections of n x n matrices.**
- [derived, three lines] -1 is not a product of n transvections t_i = 1 + a_i b_i^T (b_i . a_i = 0). Fewer than n fix
  a vector. If t_1 ... t_n = -1 then t_2 ... t_n = -1 + a_1 b_1^T; the left side fixes some v not 0 (n - 1 conditions),
  so a_1 (b_1 . v) = 2v, v is a multiple of a_1, and then b_1 . v = 0: contradiction. [ran: over the fields of 3 and 5
  elements -1 is not a product of 2 transvections of 2 x 2 matrices and is one of 3; over the field of 3 it is not a
  product of 4 of 4 x 4 matrices (exhaustive: 229,581 products of two against themselves) and is one of 5.]
  [recalled: Dieudonne's theorem, a scalar matrix other than 1 needs n + 1.] For odd n the determinant already
  forbids it: arrays gain in pairs only.
- Consequences [derived]. **n free moves cost at least n + 1 shears**: 3 for a pair, 5 for the bridged word's four
  arrays. Both published words meet the bound; no cleverer word exists in this algebra. A stage holds at most n/2
  shears (each array is in one shear per stage [read: x-6 section 5]), so **at least 3 stages per free move**: an
  array leaves out a direction in each of 3 (or 5) stage blocks and keeps one. Net skipped share of a stage block:
  r/(3h) in a three-stage word, r/(5h) in the published one.
- [derived] **Ports of dimension r do not change the count.** With r commuting moves D_1 ... D_r, look at the data
  on which D_1 acts as -1 and the others as +1. Whatever a shear's coefficient is (any combination of products of the
  D_i), it is one scalar there and another where all D_i are +1, so it is a transvection or nothing; the goal is -1
  again. So at least n + 1 shears, whatever r is, and the three-shear exchange with D = D_1 ... D_r attains it for a
  pair. A fat port raises what a shear carries, not the number of stages. The same holds if the arrays make moves
  along other directions between the shears: those steps take one value on both parts.
- With x-6's r <= h/3 for scatters of the published kind: at most 1/9 of a stage, 11.1 %; a block that stands for a
  third of an array needs 11.5 % (section 3). The two-stage bar would be 7.4 %: with 2 stages per free move the same
  ports would give 0.21 [FLOAT, WHAT-IF: blocks 2h/3 and h, m = 2h].
- The bridged word buys fewer shears per free move (1.25 against 1.5) with a worse share per data array (1 of 5h
  against 1 of 3h). The ledger says why that was right for the unit: 87 to 93 % of the credit goes to helpers and
  copies, which are paid per shear.

## 6. What the brief asked, answered

- Does the saving sit in a few blocks at a high rate? **Yes, in the stage blocks of the data arrays: 1 direction of h
  left out per stage block gross (0.42 of a move per block as cut), 0.2 net after the word's pay-back.** They are the
  object to enlarge. Their distance to the bar, in their own currency: 11.1 % of a stage left out against 16.4 %
  (five stages), then a factor 5 for the pay-back (3 at best, by section 5).
- Which interruption of an array buys the most? The stage boundary of a data array. What would it take to have only
  that kind? No pay-back (excluded in the exchange algebra by section 5: at best two of three), no helpers cut into
  stage blocks, no copies; then 0.068 at h = 9, and 1e-1 only for h <= 6 with five stages or h <= 8 with three, where
  no scatter is known to pass its threshold [read: x-6, ab-1].
- Linear size in this law is one block per array; the floor note already excludes it inside the engine [read].

## 7. What failed, and what I changed

- "Rate = moves saved per block, compare with 0.63." The comparison is wrong for blocks that are not single moves:
  0.168 against 0.626 looks like a factor 3.7; in charge it is 8.4 moves against 1. Changed to the charge of each
  block, which gave the ledger (section 2), the entropy reading and the self-paying share (section 3).
- "Attribute the credit to the x and y classes." The credit is one move per data array; which of its five stage
  blocks "owns" it is not defined. Changed to: gross view per class (labelled), net view per array, and the charge,
  which is defined per block.
- "The idle class pays the port moves back" (my first print-out). Wrong split: every stage climb, idle or not, leaves
  out a direction, and one catch-up block of 4 pays back [read: foldlib B2u]. The class totals did not change.
- "Have only the stage block": first tried as a block list (0.068). Then asked what forbids it and found the
  transvection count. Then tried to go under 3 with a premix: a two-shear exchange, true on one column, dead from two.
  Then widened the free steps to address maps and sign patterns (mutation 1): still dead at the sizes tried.
- `sector.py`'s first run listed the rows of its matrices in a different order from the columns; the control
  "D^2 is a free step" caught it at three columns. Fixed and rerun; the first output is kept as
  `sector-firstrun-rowbug.out` and is not quoted.
- My first column "moves to skip for 1e-1" added D twice; corrected before any number was quoted here.

## 8. Mutations

1. `sector-test` (the only one that bears on the order). The count n + 1 comes from one fact: every free step takes
   the same value where the move is +1 and where it is -1. A step cheaper than a move that tells the two apart would
   allow two shears per exchange, two stages per free move, and a stage block at r/(2h) against a bar of 7.4 %.
   Tried tonight, a first case [ran: `sector.py`, `sector.out`, MODULO the primes 10009 and 1000033]: free steps
   widened to every monomial step that acts alike on all columns (any permutation of the 4 addresses of a column of
   2 bits, times a sign pattern: 96 steps). The two-shear exchange X' = x + U y; Y += D X'; X' -= D^-1 Y; Y += V X'
   works exactly when D + D U D = V [derived]. Result: solvable on one column (where the move itself is such a step),
   **not solvable on two or three columns** (the span of the steps has dimension 64 and 96, with D . D 76 and 144, and
   D is outside). "Not solvable modulo p" means: a solution over the Gaussian rationals would need p in a denominator;
   two primes were tried. At 3 bits per column and two columns, with the 1,344 invertible affine maps and 8 sign
   patterns (10,752 steps, span of dimension 1,324, with D . D 1,468): not solvable either, for the port 001
   and for the port 111 [ran, modulo 10009 only; `sector-h3-001.out`, `sector-h3-111.out`].
   Not tried: steps that treat the columns differently (the floor note's hatch (a); in the engine no letter does),
   and words whose two shears go along different directions.
2. `what-the-count-does-not-cover`. [derived] The count n + 1 survives every step that takes the same value on the two
   sectors: scalars, the shift along the port, and also moves along OTHER directions made between the shears (they
   commute with the port's move and do not see its sign). So an exchange cannot be shortened by interleaving it with
   moves the arrays owe anyway. What it does not cover is a step that carries the port to another direction (an
   address map g with g p not p): then the two sectors are no longer compared with themselves. The tiny-unit notes
   say every saving of the small game needs an address map [read: the brief]; this says why from the other side.
   The exact question for a search: n = 2 arrays, directions p and q, address maps that exchange p and q, at most
   2 shears per array: is -1 reachable? `sector.py` covers the sub-case "both shears along p" at 2 and 3 bits per column only.
3. `charge-as-objective`. Every search of the tiny game minimised moves. The exact objective is the root of the law,
   and the cheap filter is the self-paying share: an array of two blocks that skips one move gives 0.14 at m = 45.
   (ab-1 named the question; this gives the test.)
4. `edge-exchange`: is there any identity that gives an array a free move with all its additions within c moves of
   the start or the end of its life? The law prices such cuts at 0.56 to 0.92 of a move at m = 45, the middle at 3.2.
5. Not a route to the bar, for the record: helpers and copies. With both gone the fourth result's block list gives
   1.3e-2 and the second's 5.5e-3.

## 9. Criticism, last

- Sections 1 and 2 are bookkeeping on published files. Their only new content is the split by class and the ledger
  identity; the what-if rows "no copies", "no copies and no helpers", "whole blocks" were in x-6 and I reproduce them.
- The first-order "entropy" reading is the law's own Taylor expansion; the per-block criterion is sufficient, not
  necessary (blocks may subsidise each other, and in every legal unit they do).
- Section 5 is a model: arrays as rows of a matrix over the algebra of one move, free steps = scalar matrices, one
  direction, one shear per array per stage. The engine also has address maps and phase letters, which I did not put
  in; the published words meet the bound, which is evidence for the model, not a proof that it is complete. The
  three-line lemma is elementary and I checked it by exhaustion only at 2 x 2 and 4 x 4 over small fields.
  Dieudonne's theorem is recalled, not read tonight.
- "A stage holds n/2 shears" and "r <= h/3" are read from x-6, unreviewed.
- `sector.py` tests one family of two-shear words (scalar shears along one direction, free premix and clean-up from
  monomial steps that act alike on all columns), modulo primes, at 4 and 8 addresses per column. It is a first
  case, not a theorem about address maps.
- I did not reconstruct the five-stage word array by array; "4 of 5 paid back" is read from the generator's block
  list, and which role owns the free move is not determined here.
- The five extra block lists were not passed through the checker by me.
- Everything with a decimal point is a float. Nothing here is a circuit, a gate count or a change of order.

Files: `waves/wave-09/ad-0-rateperblock/`: ledger.py, ledger.out (classes,
ledger, rates, what-ifs, cuts, for the two published certificates); brief.out (seven block lists, one line and one
cascade each; made by `ledger.py brief`); shape.py, shape.out (the law block by block; floats); shears.py, shears.out
(the exchange algebra and the transvection count; exact); sector.py, sector.out, sector-h3-001.out, sector-h3-111.out (mutation 1:
two-shear exchange with address maps and sign patterns; modulo primes).
