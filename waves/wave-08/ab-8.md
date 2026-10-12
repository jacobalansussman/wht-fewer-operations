# ab-8 reconcile-caps: one table for the three ceilings, a bound that ties them together, and the verdict on 1e-1

> Editor's note (11 October 2026): the critic corrected two things in this report. The widths 690 and 210 should read 687 and 206, and "excluded" holds inside one cost model only ([ac-2](ac-2.md)).

11 October 2026, about 05:20 to 05:55 EDT, one agent, 60-minute box. Private research: nothing published, no git, no Lean,
nobody has read this. **No circuit below any known count and no growth law below N log N beyond the published one.**
Marks: [ran] = run by me tonight (programs and outputs in `ab-8-reconcilecaps/`; counts are exact whole numbers; every
saving is a root of the price law found by bisection in floats, and `eig.py` is floats); [read] = in a file I opened
tonight; [derived] = by hand tonight, checked by nobody unless a [ran] stands next to it; [guess].
Unit of cost: the engine's **moves** (one direction of the transform applied to one whole array). Gate counts (G) and (O)
are not used anywhere in this report.

Words. *Array*: one working copy of the data. *Block*: a run of moves on one array with no addition in between; its
*rank* is the number of moves. *m*: moves owed per array. *Price law* (the engine's own): the saving is 1 - z, z the root
of "sum over all blocks of (rank/m)^z = number of arrays". *Port* or *label* of a pair (source, target): a subspace P of
dimension r of the h address bits of a stage, with a complement L; the source skips the r moves along P. *Class* (h, r).
rho = r/h. *t knows s*: P_s lies inside L_t. *Scatter matrix* M: M[t][s] = how much of source s target t holds after
reading the shared sums (*totals*); M[t][t] = 1, and M[t][s] may be non-zero only if t knows s (only then can the
unwanted share be removed later). *kappa* = (number of pairs) / rank(M) = sources served per total. *Loss ratio*
lam = (moves spent on totals) / (r x number of pairs); in x-6's design every total costs h moves, so lam = h/(kappa r).
*Helpers per pair*: helper arrays per pair-index (the published unit: 783 for 120, that is 6.5). *Stages* s: 3 for the
plain exchange, 5 for the published bridged word; m = s h. A gain of any size needs lam < 2/3 (three stages) or < 0.8
(five) [derived: moves saved = r v (s - 1 - s lam); both studies say the same]. Idle moves of a data array are cut in
one of four ways, and the names matter below:
**A2** two idle blocks per array (k-levers; the published units have two); **A5** the published five-stage bank, unequal
blocks (x-6's five-stage rows); **B1** one idle block per array (what v-levers calls "merged", and x-6's ordinary
three-stage rows); **C0** no idle block at all, the catch-up melted into the next climb (what x-6 calls "merged").

## 0. The answer

1. **The curator's reading holds: the two studies compute one formula and differ only in which costs they set to
   zero.** One function (`price.py`) reproduces k-levers' printed figures to four digits, x-6's three tables to four
   digits and v-levers' ranges [ran]. Four lines of the draft dictionary are wrong and one is incomplete (section 1).
2. **Which idealisation carries the gap between 2.5e-2 and 0.12: the cost of the copies, almost alone.** At r = h/2,
   three stages, no helpers: 0.0228 (loss ratio 0.5144, two idle blocks) -> 0.0266 if only the idle blocks are merged
   -> 0.1018 if only the copies are made free -> 0.1198 with both [ran]. Copies: 0.079 of the 0.097.
3. **That idealisation is contradicted at r = h/2 and limited everywhere else by one inequality** [derived, section 3;
   checked exactly on five classes]: for every family of labels of class (h, r), with any complements,
   **kappa <= 1 + (2^(h-r) - 1)/(2^r - 1), about 1 + 2^(h-2r).** At r = h/2 it is 2 (x-6's "kappa <= 2", now also for
   the avenues' wider labels); in general the loss ratio is at least about (h/r) / (1 + 2^(h-2r)). So "ports that fill
   half the stage" and "many sources per total" exclude each other unless the stage is wide: the surplus h - 2r must be
   about 5 to 7 bits while r/h stays above 0.42.
4. **First experiment, done** [ran, exact counts]. For the six classes of the brief, with copies at the least cost the
   knows graph allows and helpers 0, the best figures are: three stages 1.9e-2 (class (6,2)); with x-6's merged word
   2.4e-2; five stages 2.4e-2. (5,2), (7,3), (9,4) cannot gain in three stages at all, (7,3) in no word. Over every
   class with h <= 9, by the bound of line 3 alone, at most 4.5e-2 (5.5e-2 merged). **Below 1e-1 by a factor 2 to 5: the
   mechanism is excluded at every block width up to 9.**
5. **Growth law in the block width h** [ran on the bound of line 3]: best saving, copies at the floor, helpers 0, three
   stages, one idle block: 0.045, 0.058, 0.077, 0.090, 0.098, 0.105, 0.113 at h = 9, 12, 20, 32, 48, 80, 200; it creeps
   to 0.1198 and never passes it. **1e-1 is first not excluded at h = 55, r = 24** (h = 23, r = 9 with the merged word;
   h = 690 with two idle blocks as published; h = 210 for five stages with one idle block; never with the published
   five-stage bank, whose corner is 0.078).
6. **Helpers decide independently of everything else** [ran]: with 0.51 helper arrays per pair or more (0.97 with the
   merged word) 1e-1 is out for every h and r even with free copies. The published unit has 6.5; the lowest floor
   anybody argued for E8 is 0.31, and at 0.31 the first open width moves to h = 170 (36 merged).
7. **Verdict: open on paper only. Not excluded outright, not searchable.** Everything at once is needed: a stage of 23
   to 60 bits or more, ports of dimension 9 to 26 (the class has more than 2^120 labels), a scatter whose kappa sits
   near the ceiling of line 3 (33 to 129 sources per total, hence at least 16 to 64 removals per target, section 5),
   fewer than half a helper per pair, a three-stage word for fat ports that nobody has built, and an engine that accepts
   fat labels. Nothing computed tonight supports any of the six; two are now contradicted below width 23.
8. **What a search can still decide** is smaller than 1e-1: whether fat ports save anything at all at small width
   (section 7, two named computations), and whether kappa for symmetric scatters follows a square-root law
   2^(h/2 - r) (section 6; nine graphs agree), which would move the first open width to about 95 (37 merged).
9. By-products. (a) The scatter problem is the *index coding* problem of network coding, and kappa = v / minrank
   (section 8). (b) **Thin ports: no scatter of any kind has kappa above 5, 9, 17 at h = 5, 7, 9**
   (1 + 2^((h-1)/2)) [ran, exact at 5 and 7; at 9 exact count 15 plus the eigenvalue bound, floats]. E7 has 9: it IS
   the full family at width 7 and meets the ceiling. E8 has 15 of 17. Width 5 cannot gain (the five-stage word needs
   more than 6.25): "no thin family below width 7" is a consequence, in x-6's cost model. (c) The avenues' labels are all complementary pairs (P, L); x-6's ports are the 20 of 560, 80 of
   9,920, 640 of 714,240 with L = P-perp [ran for the first two; counted for the third].

## 1. The dictionary, checked line by line

Confirmed [ran unless marked]:
- label = port; thin = dimension 1; class (h, a) = (h, r); m = s h; copies = totals; gain thresholds 2/3 and 0.8.
- loss ratio of E8 = 72/120 = 0.6 = 9/15 = h/kappa.
- v-levers' "R 0, cst 0" for E8, "1.6e-2 to 2.0e-2" = 1.576e-2 (published bank; this is x-6's 1.58e-2) to 1.987e-2 (one
  idle block). v-levers' "cst 0: 3.51e-3" is x-6's 3.5071e-3 [read both].
- x-6's 0.120 (three stages, r = h/2) is v-levers' 0.120: same shape B1, same number 0.1198.

Broken or incomplete:
1. **v-levers' "0.107 to 0.120 / 0.075 to 0.086" is not "three-stage / five-stage".** It is (five stages 0.1065, three
   stages 0.1198) with no helpers / (five stages 0.0746, three stages 0.0864) with ONE helper per pair, all with one
   idle block per array [ran `ceiling.py` section E; the same reading reproduces its "3.1e-2 to 4.0e-2 / 2.3e-2 to
   2.8e-2" for (6,3) at ratio 0.487: 0.0314, 0.0397 / 0.0227, 0.0282]. So x-6's five-stage 0.078 is NOT v-levers'
   0.075: x-6's 0.0784 is the five-stage corner with the published bank; v-levers' five-stage corner is 0.1065 because
   it grants one idle block. There are three unrelated numbers near 0.078: 0.0784 (five stages, r = h/2, published
   bank), 0.0783 (three stages, r = h/3), 0.0746 (five stages, r = h/2, one idle block, one helper per pair).
2. **"Merged" names two different things.** v-levers: idle moves in one block instead of two (B1). x-6: no idle block
   (C0). x-6's ordinary rows already assume v-levers' "merged". The published units have two idle blocks. Requirement
   (iv) of the brief is therefore two requirements: one idle block (needed for every figure above 0.102), and none
   (needed for 0.098 at r = h/3 and 0.147).
3. **The row "2.8e-3 to 3.6e-3" uses cst 72 (loss ratio 0.6), not 55.** It is E8 with 116 or 37 helpers (0.97 or 0.31
   per pair): 3.0644e-3 and 3.5887e-3 with one block per helper per stage, 2.8073e-3 with helper blocks 1,7,1 [ran; read
   k.out]. The rows with cst 55 (ratio 0.458) and 8 helpers are k-levers' 6.55e-3 and v-levers' 8.2e-3 [ran: 6.5564e-3,
   8.2038e-3].
4. **The avenues' labels are a wider class than x-6's ports.** A label there is a subspace with ANY complement: the
   nine "full family" sizes of fat-classes/NOTE.md (28, 120, 496, 2,016, 8,128, 32,640, 560, 9,920, 714,240) are all
   (number of a-dimensional subspaces) x 2^(a(h-a)) [derived from the counts read; `orderbound.py` builds 560 and
   9,920]. x-6's ports are the pairs with L = P-perp. So x-6's "kappa <= 2 at r = h/2" did not cover the avenues' class
   (4,2) or (6,3). Section 3 closes that hole inside x-6's cost model.
5. **"loss ratio = h/(kappa r)" is x-6's cost model only.** There every total is brought down all h moves. The
   avenues' search model lets a shared sum cost less (E8: argued floor 55 against 8 x 9 = 72; at (6,3) it has shapes of
   cost 1 and 2 [read fat-classes/NOTE.md lines 72 to 76]). The pricing of a given loss ratio is common to both; the
   floors (0.835, 0.8119, 0.5144, exactly 1) are the avenues' model, the kappa bounds are x-6's. Hatch H1 of section 9.
6. cutf3's "k >= 3 W" counts moves, not blocks: at block size 3 without address maps nothing saves a move [read]. The
   tiny unit's 0.107 is 1 - ln(8/3)/ln 3: 3 arrays, 8 moves, each its own block [derived].

## 2. The one table [every "re-run" is `price.py` or `ceiling.py`, floats]

| saving | who | (h, r) | stages | loss ratio | helpers per pair | idle blocks | re-run | stands on / contradicted by |
|---|---|---|---|---|---|---|---|---|
| 8.7625e-4 | published, Lean | (9,1) | 5 | 0.6 | 6.5 | as certified, 16.5 blocks per array | [read zlaw.out] | the fact |
| 2.8e-3 to 3.6e-3 | k-levers | (9,1) | 5 | 0.6 (cst 72) | 0.97 to 0.31 | A5 | 3.06e-3, 3.59e-3 | helper floors argued by one agent, for E8 only |
| 6.55e-3 to 8.2e-3 | k-levers, v-levers | (9,1) | 5 | 0.458 (cst 55) | 0.07 | A5 to B1 | 6.556e-3, 8.204e-3 | in x-6's cost model E8 cannot go below 72 (8 ports that do not know each other); 55 needs cheaper totals |
| 3.51e-3 | x-6 = v-levers | (9,1) | 5 | 0 | 6.5 | as certified | [read both] | copies cannot be 0: kappa <= 17 at (9,1) (section 6) |
| 1.31e-2, 1.58e-2 | x-6 | (9,1) | 5 | 0 | 0 | as cut / A5 | 1.576e-2 (B1: 1.987e-2) | the same |
| 1.7e-2 to 2.5e-2 | k-levers | (6,3) | 3, 5 | 0.5144 | 1 or 0 | A2 | 2.28e-2, 1.72e-2; 2.48e-2, 1.94e-2 | x-6's model: each of the 640 ports knows exactly one, ratio >= 1, saving 0 [ran]; avenues' model: a floor with no family behind it |
| 7.3e-3 to 8.8e-3 | k-levers | (6,3) | 3, 5 | 0.5144 | 6.5 | A2 | 7.28e-3, 8.81e-3 | the same |
| 0.028 to 0.078 | x-6 | rho 0.2 to 0.5 | 5 | 0 | 0 | A5 | 0.0282, 0.0430, 0.0594, 0.0784 | copies free; at rho = 0.5 kappa <= 2 |
| 0.049 to 0.120 | x-6; v-levers' corner | rho 0.2 to 0.5 | 3 | 0 | 0 | B1 | 0.0485, 0.0707, 0.0940, 0.1198 | the same; five stages B1 0.1065; with one helper per pair 0.0864 / 0.0746 |
| 0.078 (0.048) | x-6 | r = h/3 | 3 (5) | 0 | 0 | B1 (A5) | 0.0783 (0.0483) | at (9,3) the ratio is at least 0.647: saving at most 0.0022 [ran] |
| 0.098 | x-6 | r = h/3 | 3 | 0 | 0 | C0 | 0.0980 | the same, and the word |
| 0.147 | x-6 | r = h/2 | 3 | 0 | 0 | C0 | 0.1467 | dead: kappa <= 2 |
| 0.107 | avenues, tiny unit | none | none | none | none | 8 blocks of rank 1 | 0.1072 | another mechanism; needs address maps (cutf3) |
| **0, 1.9e-2, 0, 7.1e-3, 2.2e-3, 0** | this report | (5,2) (6,2) (7,3) (8,3) (9,3) (9,4) | 3 | at the knows-graph floor: 0.75, 0.50, 0.88, 0.61, 0.65, 0.73 | 0 | B1 | section 4 | exact counts; nothing idealised except helpers, word, engine |
| **0.045 ... 0.100 at h = 55** | this report | best r for each h | 3 | at the order-bound floor | 0 | B1 | section 4 | the bound of section 3 |

## 3. The order bound [derived; checked exactly by `orderbound.py`]

**Lemma.** Let a family have v labels (P_t, L_t), each P_t of dimension r, P_t and L_t complementary in the h bits
(repeats allowed), and let M be any v x v matrix with M[t][t] = 1 and M[t][s] = 0 unless P_s lies inside L_t. Then
rank(M) >= v (2^r - 1) / (2^r + 2^(h-r) - 2), that is **kappa <= 1 + (2^(h-r) - 1)/(2^r - 1)**.

Proof. Put the non-zero address words in any order and call first(U) the earliest non-zero word of a subspace U. Let I
be the set of labels with first(P_t) earlier than first(L_t). If s and t are in I and M[t][s] is not 0, then P_s lies in
L_t, so first(L_t) is not later than first(P_s), hence first(P_t) is strictly earlier than first(P_s). Sorted by
first(P), M restricted to I is triangular with ones on the diagonal: rank(M) >= |I|. For a random order the earliest
of the (2^r - 1) + (2^(h-r) - 1) non-zero words of P_t and L_t lies in P_t with probability (2^r - 1)/(2^r + 2^(h-r) - 2),
so some order has |I| at least v times that. Done. Five lines, no property of the transform is used except the rule
"remove only what is known".
[ran: for the wide classes (4,2) (560 labels) and (5,2) (9,920) and for x-6's ports at (4,2), (5,2), (6,3): triangular
in every order tried; mean |I| over 200 orders 280.00, 2,978.8, 10.00, 23.88, 320.00 against the predicted 280, 2,976,
10, 24, 320.]

The same argument inside the words of even weight gives, for families of *all-even* ports (every word of P of even
weight; they exist for even r): kappa <= 1 + (2^(h-1-r) - 1)/(2^r - 1) [derived; equals the exact value 2 at (5,2) and
(9,4), where such ports know exactly one other of their kind].

Values: 2 at every r = h/2; 3.33 (5,2); 6 (6,2); 3.14 (7,3); 5.43 (8,3); 10 (9,3); 3.07 (9,4); 256 at (9,1), where it
says nothing (thin ports are not limited by it; they are limited by rho = 1/(s h)).

**A second bound, sharper at small width: stars** [derived, ran]. If X is a set of words any two of which overlap
oddly, the ports that contain a word of X do not know each other. There is such an X with 2^floor((h-1)/2) odd words (a
word u plus a space of even, mutually orthogonal words). Ports come in three *types* that the symmetries of the dot
product cannot mix: *all-even*; *one* (the all-ones word lies in P); *general*. Inside a type every port looks like
every other [derived: a non-degenerate space of bit vectors is fixed up to symmetry by its dimension and by whether
all its words are even, and the address space is P plus P-perp], so the share of a type that one star holds bounds
kappa for every sub-family of that type. For general ports this gives about 2^(h - r - floor((h-1)/2)), the square
root of the order bound; for all-even ports stars are weak and the order bound is what is left.

## 4. The first experiment [ran: `knows.py` exact counts, `ceiling.py`]

| class | ports by type | each knows | ceiling on kappa: order; by type | loss ratio at least | best saving, helpers 0: 3 stages B1 / C0 / 5 stages B1 |
|---|---|---|---|---|---|
| (4,2) | 4 all-even, 12 general, 4 one | 1 | 2; 1, 2, 1 | 1 | 0 / 0 / 0 |
| (5,2) | 20, 60 | 4 | 3.33; 2, 2.5 | 0.75 | 0 / 0 / 0.0047 |
| (6,2) | 80, 240, 16 | 20 | 6; 2, 3.75, 1 | 0.50 (0.80 inside one type) | 0.0192 / 0.0236 / 0.0235 |
| (6,3) | 640 general | 1 | 2 | 1 | 0 / 0 / 0 |
| (7,2) | 336, 1,008 | 80 | 11.3; 3.69, 4.5 | 0.43 | 0.0239 / 0.0294 / 0.0247 |
| (7,3) | 5,040 general, 336 one | 8; the 336 know nobody | 3.14; 2.65 | 0.88 | 0 / 0 / 0 |
| (8,2) | 1,344, 4,032, 64 | 336 | 22; 6.6, 8, 8 | 0.18 | 0.0431 / 0.0532 / 0.0359 |
| (8,3) | 43,008 general | 80 | 5.43; 4.36 | 0.61 | 0.0071 / 0.0087 / 0.0168 |
| (8,4) | 5,376, 80,640, 5,376 | 1 | 2 | 1 | 0 / 0 / 0 |
| (9,2) | 5,440, 16,320 | 1,344 | 43.3; 10.1, 8.5 | 0.24 | 0.0338 / 0.0414 / 0.0284 |
| (9,3) | 342,720 general, 5,440 one | 640; the 5,440 know nobody | 10; 4.64 | 0.65 | 0.0022 / 0.0028 / 0.0119 |
| (9,4) | 91,392 all-even, 1,370,880 general | 16 [derived, not printed] | 3.07; 2, 2.55 | 0.73 | 0 / 0 / 0.0071 |
| control (9,1) | 255 general, the all-ones word | 128 | 256; 17 | 0.53 | E8 has kappa 15, ratio 0.6: inside the ceiling |
| control (7,1) | 63 general, the all-ones word | 32 | 64; 9 (largest set exactly 7) | 0.78 | E7 has kappa 9 [read x-6]: it meets the ceiling |
| control (5,1) | 15 general, the all-ones word | 8 | 16; 5 (largest set exactly 3) | 1 | no gain: agrees with "nothing below width 7" |

Port counts agree with w-cross (20, 80, 336; 640) and degrees with x-6 (1 at (4,2), 4 at (5,2)). The ceiling used is
the smaller of the order bound and the sum of the type ceilings (types that know nobody left out). Rows with r = 2 at
h >= 7 have loose ceilings (only stars and the order bound; section 6 has tighter numbers for symmetric scatters).
"Every sub-family" is covered: the order bound is for any family; the type ceilings by the symmetry argument.
What the brief asked: **the best figure over its six classes is 1.9e-2 (2.4e-2 with either relaxation of the word); the
mechanism is excluded within x-6's design at h <= 9.** No class passes, so there is no search target for 1e-1 here.

Growth in h, order bound alone (`ceiling.py` B, C): best saving 0.029, 0.043, 0.045, 0.058, 0.068, 0.077, 0.083, 0.090,
0.095, 0.098, 0.100, 0.102, 0.105, 0.108, 0.113, 0.117 at h = 6, 8, 9, 12, 16, 20, 24, 32, 40, 48, 56, 64, 80, 100,
200, 500 (three stages, one idle block). With the sharper type ceilings (the star factor 1.34 is the worst seen in
eight exact classes; an estimate): first open class (60, 26) instead of (55, 24); merged (25, 10) instead of (23, 9).

## 5. What 1e-1 needs, with numbers, and what contradicts each [ran `price.py` section 3, `ceiling.py` C, D]

| requirement | number | status tonight |
|---|---|---|
| (i) share of the stage skipped, rho = r/h | >= 0.425 (three stages, one idle block); >= 0.341 (merged, C0); >= 0.492 (two idle blocks, as published); >= 0.477 (five stages, one idle block); impossible with the published five-stage bank | no fat word of any shape exists |
| (ii) sources per total at that rho | one idle block: kappa >= 92, 40, 26, 19 at rho = 0.44, 0.46, 0.48, 0.50; merged: >= 40, 20, 10 at rho = 0.38, 0.42, 0.50 | **contradicted jointly with (i) for h < 55 (h < 23 merged) by the order bound**; at rho = 0.5 for every h |
| (iii) helpers per pair | <= 0.51 (0.97 merged) even with free copies at r = h/2; at 0.31 the first open width is 170 (36 merged) | published 6.5; no design below it; and see the removal count below |
| (iv) one idle block per data array | without it: rho >= 0.492, first open width 690 | published units have two |
| (v) no idle block (x-6's merged word) | needed only to open widths 23 to 54 and to pass 0.1198 | nobody has such a word |
| (vi) the Lean engine accepts fat labels | | open [read fat/NOTE.md 101 to 104] |

A count that ties (ii) to (iii) [derived]: a matrix with unit diagonal whose rows have on average q non-zero entries
off the diagonal has rank at least v/(2q + 1) (Turan's bound on the graph of non-zero entries; v/(q + 1) if the pattern
is symmetric). So a scatter with kappa sources per total has at least (kappa - 1)/2 unwanted terms per target, each of
which must be removed with something a helper holds: 16 to 64 removals per target at the first open classes, to be paid
with fewer than 0.51 helper arrays per pair. E8: 56 removals per target, 6.5 helpers per pair.

The tension the brief asked to settle first: **(i) wants r near h/2, (ii) wants many known partners, and the number of
partners is governed by the surplus h - 2r alone: kappa <= 1 + 2^(h-2r).** At fixed rho the surplus is (1 - 2 rho) h,
so the only way out is width: h >= 7/(1 - 2 x 0.436) = 55.

## 6. Symmetric scatters: eigenvalues [ran `eig.py`, floats on exact 0/1 matrices]

For a symmetric positive scatter (the published E8 kind) kappa is at most n/theta, theta being Lovasz's number of the
knows graph (x-6 section 5); inside one type that is 1 + d/|smallest eigenvalue| [derived: one type is one orbit on
ports and on knowing pairs; quoted from memory: for such graphs theta equals Hoffman's ratio].

| type, class | ports | each knows | smallest eigenvalue | kappa of a symmetric scatter at most | 2^(h/2 - r) |
|---|---|---|---|---|---|
| general (9,1) (thin) | 255 | 128 | -8 | 17 (E8: 15) | 11.3 |
| general (5,2) / all-even (5,2) | 60 / 20 | 3 / 1 | -2 / -1 | 2.5 / 2 | 1.4 |
| general (6,2) / all-even (6,2) | 240 / 80 | 16 / 4 | -8 / -4 | 3 / 2 | 2 |
| general (7,2) / all-even (7,2) | 1,008 / 336 | 60 / 20 | -18.42 / -8 | 4.26 / 3.5 | 2.8 |
| all-even (8,2) | 1,344 | 80 | -32 | 3.5 | 4 |
| all-even (9,2) | 5,440 | 336 | -64 | 6.25 | 5.7 |

Readings. (a) **E8 is nearly the best possible scatter for thin ports at h = 9**: 15 against a ceiling of 17 (the
eigenvalue bound says no set of ports that do not know each other exceeds 15, the star has 15, so 17 is the exact
ceiling for every scatter and every sub-family, symmetric or not), loss ratio 0.6 against 0.529. (b) [guess from these nine graphs] kappa of a symmetric scatter is at most about
1.8 x 2^(h/2 - r), the square root of the order bound, for every type. If that is a law, the first open width for 1e-1
with symmetric scatters is about 95 (about 37 merged) [derived from the frontier of section 5]. (c) All-even planes at
h = 7, 8, 9: ceilings 3.5, 3.5, 6.25. A three-stage gain needs kappa above 5.25, 6, 6.75 and a five-stage gain above
4.375, 5, 5.625: **no symmetric scatter on all-even planes gains in three stages at h <= 9; at (9,2) a five-stage
gain is not excluded (6.25 against 5.625), and that is the one small fat target these numbers leave.**

## 7. The smallest exact computations that are still worth running

None of them can give 1e-1 (section 4); they decide the growth law and whether fat ports save at all.
1. **The smallest eigenvalue for every class and type, as a formula.** The knows graph of one type has few distinct
   eigenvalues (3 to 6 above). They can be had exactly from a table of size (number of relative positions of two
   ports) squared, built from ONE port: minutes for (9,3), (9,4), (11,4), (12,4), with no graph of a million vertices
   in memory. Outcome A: 1 + d/|smallest| stays near 2^(h/2 - r): symmetric scatters are out below width 95. Outcome
   B: some type beats it: that type is the first place to look for a fat family.
2. **All-even planes at (9,2): 5,440 ports, each knowing 336 of its kind; is there a symmetric scatter with kappa
   between 5.625 and 6.25?** Equivalent: 5,440 unit vectors in at most 967 dimensions, perpendicular whenever two
   planes are not orthogonal. Tried at once [ran `eigdim.py`, floats]: the scatter that keeps all the symmetry,
   (adjacency + |smallest eigenvalue|) / |smallest eigenvalue|, has kappa 1.02 here, 1.09 at (7,2), and only 2.1 for
   thin ports at h = 9 where E8 reaches 15. What the failure is made of: E8's scatter has entries +1/2 AND -1/2; a
   scatter with large kappa has to break the symmetry by a choice of signs (x-6: "the unit uses the roots, a choice of
   sign per pair"). So the search is for a SIGNING: signs on the knowing pairs of a sub-family such that the signed
   matrix has its smallest eigenvalue with multiplicity v - v/kappa. For E8 that is eigenvalue -2 with multiplicity
   112 out of 120. Nobody has posed the fat case this way. It would be the first fat family that saves anything (a
   five-stage saving of a few 1e-3 before helpers, nowhere near the bar).
3. **Class (6,2) with types mixed: 336 ports, is kappa above 4.5 possible?** It is the smallest class where a
   three-stage gain of any size is not excluded (order bound 6; inside one type at most 3.75; all 336 together at least
   91 ports that do not know each other, so at most 3.69 for the full family). It is also one of the avenues' "never
   examined" classes. Exact: the largest weighted set of ports no two of which know each other, as a linear programme
   over the three types (three numbers), then, if it leaves room, the least rank of M over the rationals.

## 8. The same problem in another field [derived; literature from memory, not opened tonight]

Targets = receivers, sources = messages, "t knows s" = receiver t has message s as side information, totals = the
broadcast symbols. The least number of totals for a family is the *minrank* of its knows graph over the rationals:
this is linear **index coding** (Bar-Yossef, Birk, Jayram, Kol, 2006), and minrank is Haemers' bound (1978) on the
Shannon capacity. Known there: (largest set no two of which know each other) <= minrank <= (least number of groups
that all know each other). The order bound of section 3 is the first inequality with an explicit set; E8 meets it with
equality (8). The engine's extra rule, that every total costs h moves and helpers cost blocks, has no counterpart
there. If this parallel is wanted for the leads file, it should be checked against the papers first.

## 9. What failed, and what I changed

- "Use the largest set of ports that do not know each other, class by class" (the brief): exact search does not finish
  at 240 ports. What the failure is made of: I only need a large set, not the largest. Changed to explicit sets
  (stars), which give a valid ceiling for every sub-family by symmetry.
- Stars are useless for all-even ports (a set of even words overlapping oddly has at most h + 1 members [derived]).
  Went around: the order argument of section 3, which needs no star and no symmetry, and covers the avenues' wider
  labels as well.
- The order bound says nothing for thin ports (256 at h = 9). Went around: eigenvalues (section 6).
- Not closed, each a hatch out of x-6's design: **H1** totals that are not brought down all h moves (the avenues' cost
  model; E8: 55 against 72); the order bound still gives the NUMBER of totals, not their cost. **H2** x-6's "partial
  knowledge" (remove a term when P_s is only partly inside L_t); the proof of section 3 breaks at its second line.
  **H3** more than one shear per stage. **H4** address maps inside a stage (the tiny-unit game).

## 10. Criticism, last

- Every saving is a what-if block list. The bounds of sections 3 to 6 limit the cost of copies only; helpers, the word
  and the engine are still idealised in every figure of section 4, so those figures are ceilings, not candidates.
- The lemma is five lines and one hour old; its check is on five small classes. The model it lives in (M[t][t] = 1,
  zero unless known, totals = rank) is x-6's reading of the certificate, not the Lean engine.
- "Types are orbits" is derived from the classification of non-degenerate forms over two elements as I remember it;
  the runs agree (one degree per type) but do not prove it. If it failed, the per-type ceilings would need an average
  over the true orbits; the order bound would not change.
- The mixed-type ceiling is a crude sum. The star factor 1.34 and the square-root law are fits to eight and nine
  graphs. `eig.py` is floats; "theta = Hoffman's ratio" is from memory.
- The largest sets found by greedy search are lower bounds; no exact maximum was finished above 20 ports except where
  marked. That only makes the ceilings looser than the truth.
- The first open classes (55, 24), (23, 9), (60, 26), (25, 10) come from float roots within 2e-4 of 0.1; the widths
  could be off by a few bits. I did not re-run the published certificate; row 1 is read.
- Not read: the wave-7 skeptics, WAVE7-NOTE.md, the other wave-8 reports; whatif_copies.py; the scripts behind the
  avenues' floors.

Files: `waves/wave-08/ab-8-reconcilecaps/`: price.py, price.out (the one
pricing function, controls, ladder, frontier); knows.py, knows_<h>_<r>.out (ports by type, degrees, stars, greedy sets;
fifteen classes); orderbound.py, orderbound.out (the lemma checked); ceiling.py, ceiling.out (ceilings into the price
law, growth in h, first open widths); eig.py, eig.out (eigenvalues by type), eigdim.py, eigdim.out (multiplicities; the
fully symmetric scatter and its small kappa); both need the numpy of `wht33/fatlabels/venv`.
