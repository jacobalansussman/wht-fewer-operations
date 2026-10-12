# ac-2: a skeptic's reading of ab-8's order bound and "first open width", with ab-1's pair rule

11 October 2026, about 06:20 to 06:50 EDT, one agent, 30-minute box. Private research: nothing published, no git, no
Lean. **No circuit below any known count and no growth law below N log N beyond the published one comes out of this
object.** Marks: [ran] = run by me tonight with my own code (`ac-2/`); [read] = in a file or page I opened tonight;
[derived] = by hand tonight, checked by nobody; [guess]. Unit of cost: the engine's *moves* (one direction of the
transform applied to one whole array); gate counts (G) and (O) are not used anywhere here.

Words, as ab-8 uses them. *Stage*: a group of h address bits. *Label* of a pair (source, target): a subspace P of
dimension r of those bits, with a complement L (P and L meet only in 0); the source skips the r moves along P.
*Class* (h, r). *t knows s*: P_s lies inside L_t. *Total*: a shared sum of sources that targets read. *Scatter
matrix* M: M[t][s] = how much of source s target t holds after reading totals; M[t][t] = 1, and M[t][s] may be
non-zero only if t knows s. *kappa* = pairs / rank(M) = sources served per total. *Port*: a label with L = the
perpendicular of P. *Price law*: the saving is 1 - z, z the root of "sum over blocks of (rank/m)^z = number of arrays".

## 0. Verdict in eight lines

1. **The lemma is true.** kappa <= 1 + (2^(h-r) - 1)/(2^r - 1) for every family of labels of class (h, r). I checked
   the proof line by line (section 1) and by exact computation over ALL orders at widths 2 and 3 and random orders on
   eight classes, three of them larger than the author's (section 2): no violation.
2. **It is known.** It is the "largest set without a cycle" lower bound of index coding (Bar-Yossef, Birk, Jayram,
   Kol, 2006), specialised to subspaces by a random order. Known theory then says: this is the WEAKEST of the standard
   bounds, so the true kappa may be far below it; it says nothing for or against linear size (section 3).
3. **The arithmetic built on it is right.** My own pricing code gives 0.0450 (0.0553 merged) as the most over all
   classes with h <= 9, and first open classes (55, 24) and (23, 9), as claimed. Two small corrections: 687, not 690;
   206, not 210 (section 4).
4. **The exclusion "no 1e-1 up to width 9" lives in one cost model, and I measured how much it leans on it.** It
   survives if a total costs only r moves instead of h (then at most 0.081). It does not survive if a total can cost
   less than about 0.4 h moves in classes with r above h/2 (section 5). The second assumption, "a term is removed only
   if fully known", is not touched by the proof and I could not test it: if partial knowledge counts, the lemma says
   nothing.
5. **"Open from (55, 24)" is not evidence of life.** It only means this particular bound stops biting. Every family
   anybody has built at r near h/2 has kappa about 2; the bound there allows 129.
6. **ab-1's pair rule is correct as algebra** [derived], and its two counts are right [ran]: 56 and 240 tight
   characters at block sizes 4 and 5, every pair of directions covered. It kills "every direction once" and its
   multiples; it does not kill the linear programme's value 15/4 (section 6).
7. In the user's terms: **nothing yet.** No circuit size, no exponent. A ceiling on a what-if, and one dead candidate.
8. Side items (section 7): hybrid 4's lemma checked by hand, correct; ab-5 did read Find and Boyar; hybrid 1's
   recalled theorem exists as recalled; ab-4's no-return theorem not reviewed.

## 1. The claim, exactly, and the proof read line by line

**Claim.** v labels (P_t, L_t), each P_t of dimension r, P_t and L_t meeting only in 0, L_t of dimension h - r
(repeats allowed). M any v x v matrix over any field with M[t][t] = 1 and M[t][s] = 0 unless P_s lies inside L_t.
Then rank(M) >= v (2^r - 1)/(2^r + 2^(h-r) - 2).

**Proof as I re-derived it** [derived]. Order the non-zero words; first(U) = earliest non-zero word of U. I = labels
with first(P_t) earlier than first(L_t). For s, t in I, s different from t, M[t][s] non-zero: P_s is inside L_t, so
first(L_t) is not later than first(P_s), so first(P_t) < first(L_t) <= first(P_s). Three points I looked for and
found sound:
- *Ties.* Two labels of I with the same first(P) have M zero in both directions (each direction would need a strict
  inequality). So sorting I by first(P), ties in any order, gives a triangular block with ones on the diagonal.
- *Repeats.* Two copies of one label never know each other (P inside L is impossible), so they are covered.
- *The probability.* The non-zero words of P_t and of L_t are (2^r - 1) + (2^(h-r) - 1) different words; in a
  uniformly random order the earliest of them is equally likely to be any one. Exact, no approximation.
The proof uses only "P and L share no non-zero word" and the knows rule. It holds over every field. It never uses
that L has dimension h - r (a smaller L only helps).

**What the claim is not.** It bounds the NUMBER of totals. The step to a saving needs three more things that are
assumptions, not theorems: every total costs h moves in one block per stage; a term can be removed only if fully
known; the list of block shapes (three or four blocks per data array). Section 5.

## 2. My own exact check [ran, `ac-2/lemma.py`, `rand.out`, `struct.out`; whole numbers and fractions]

Subspaces as bit masks; every pair of I compared directly (not through the proof's own index), up to 3,500 labels of
I per order.

| class | labels | orders | violations | mean of I | predicted | bound on kappa |
|---|---|---|---|---|---|---|
| (2,1) any complement | 6 | all 6 | 0 | exactly 3 | 3 | 2 |
| (3,1) any complement | 28 | all 5,040 | 0 | exactly 7 | 7 | 4 |
| (3,2) any complement | 28 | all 5,040 | 0 | exactly 21 | 21 | 1.33 |
| (3,1) ports | 4 | all 5,040 | 0 | exactly 1 | 1 | 4 |
| (4,2) any complement | 560 | 200 random | 0 | 280.00 | 280 | 2 |
| (5,2) any complement | 9,920 | 60 | 0 | 2,967.6 | 2,976 | 3.33 |
| (5,2) ports | 80 | 200 | 0 | 24.0 | 24 | 3.33 |
| (6,3) ports | 640 | 100 | 0 | 320.00 | 320 | 2 |
| **(6,2) ports** (new size) | 336 | 100 | 0 | 55.7 | 56 | 6 |
| **(7,3) ports** (new size) | 5,376 | 40 | 0 | 1,704.5 | 1,710.5 | 3.14 |
| **(6,2) any complement** (new size) | 166,656 | 6 | 0 | 27,414 | 27,776 | 6 |

Label counts agree with ab-8 (560, 9,920, 20, 80, 640, 336, 5,376). The author's third test (a random matrix with
the allowed support has rank at least the size of I) is weak: a random matrix has full rank. I replaced it by
structured matrices, 1 + c x (knows matrix) over 80 exact values of c: least rank 10 of 20 at (4,2) (the bound says
at least 10: **the bound is attained**), 64 of 80 at (5,2) (bound 24), 7 of 16 at (5,1). No violation.
Where the bound is tight [derived]: at every r = h/2 (the two labels (P, L) and (L, P) know each other: kappa 2).
Elsewhere nobody knows.

## 3. Is it known? Yes

- **Index coding.** Receivers = targets, messages = sources, "t knows s" = side information, totals = broadcast
  symbols. Bar-Yossef, Birk, Jayram, Kol, "Index coding with side information", FOCS 2006, IEEE Transactions on
  Information Theory 57 (2011) [read: search summary and the abstract, not the full text]: the least number of
  symbols of a linear code is the *minrank* of the knows graph, and for every graph it is at least the size of the
  largest set of vertices whose knows relation has no cycle. The reason is ab-8's: on such a set the matrix is
  triangular. ab-8's lemma is that theorem plus one count: a random order produces a cycle-free set of the stated
  size for the subspace relation. I did not find that count in print (one search); it is five lines.
- A correction to ab-8 section 8: the set in the order bound is cycle-free, not "no two know each other". The two
  coincide for ports (there knowing is mutual), not for labels with any complement.
- **What the known theory predicts.** The cycle-free bound is the weakest standard bound; the paper itself says it
  is not tight in general [read: search summary]. The gap can be very large: for a random graph on n vertices the
  largest such set has about 2 log2 n vertices while the minrank is about n / log n (Golovnev, Regev, Weinstein,
  arXiv:1607.04842, finite fields; Alon, Balla, Gishboliner, Mond, Mousset, arXiv:1809.01873, every field)
  [recalled, not opened tonight; check the numbers before quoting]. So
  the true ceiling on kappa may be far below 1 + 2^(h-2r), and "first open width 55" is an upper estimate of nothing.
  On "linear or not": nothing. The theory is about how many totals, and the engine's saving at its best what-if is
  0.12 to 0.15 even with free totals.

## 4. The arithmetic, redone [ran, `ac-2/price2.py`, floats for the root, exact fractions for the bound]

I re-coded the price law and the block lists from ab-8's description (not from its code) and scanned EVERY r from 1
to h - 1 (ab-8 scans only r up to h/2; the result is the same).

- Controls reproduced: 0.1198, 0.1467, 0.1018, 0.1065, 0.0784 (corner, five shapes); 0.0864 and 0.0746 (one helper
  per pair); 0.0783, 0.0980, 0.0483 (r = h/3); 0.0228 and 0.0266; 0.0314, 0.0397, 0.0227, 0.0282; 3.0644e-3,
  3.5887e-3, 6.5564e-3, 8.2038e-3; 1.5758e-2. So the four corrected dictionary lines are right as arithmetic.
  Limit of this check: I used the block lists as ab-8 states them; I did not open k-levers, v-levers or x-6 to see
  that these are the lists those studies used.
- All classes with h <= 9, totals at the order bound, helpers 0: at most **0.0450** (three stages, one idle block),
  **0.0553** (merged), 0.0417 (two idle blocks), 0.0397 (five stages, one idle block), 0.0298 (published bank).
  Confirmed.
- First open class: **(55, 24)** at 0.10021 (width 54: 0.09947); merged **(23, 9)** at 0.10087 (width 22: 0.09972).
  Confirmed. Corrections: two idle blocks **687**, r = 338 (ab-8: 690, a scan in steps of 5); five stages with one
  idle block **206**, r = 99 (ab-8: 210, same reason).
- **Growth law of the ceiling** (not of any program): 0.0450, 0.0583, 0.0766, 0.0900, 0.0977, 0.1051, 0.1130,
  0.1167, 0.1181, 0.1193 at h = 9, 12, 20, 32, 48, 80, 200, 500, 1,000, 4,000. Fit: 0.1198 - c ln(h)/h with c
  between 0.24 and 0.28 over h = 50 to 4,000. Merged: towards 0.1467. I pushed h from 500 to 4,000; no change of law.

## 5. The cost model, attacked [ran, `ac-2/hatch.py`]

**(a) "Every total costs h moves."** ab-8 names this hatch (H1) and gives no number. Numbers: keep the number of
totals at the order bound and let a total be ONE block of rank f x h. Best what-if saving over all classes, h <= 9:

| a total costs | 3 stages, one idle block | merged | 5 stages, one idle block | published bank |
|---|---|---|---|---|
| h (ab-8) | 0.0450 | 0.0553 | 0.0397 | 0.0298 |
| 0.76 h (the ratio 55/72 argued for the published unit) | 0.0507 | 0.0628 | 0.0454 | 0.0340 |
| 0.51 h (the ratio the avenues argue at (6,3)) | 0.0592 | 0.0735 | 0.0668 | 0.0566 |
| 0.40 h | 0.0826 | 0.0783 | **0.1037** | 0.0876 |
| 0.35 h | **0.1038** | 0.0919 | **0.1210** | **0.1020** |
| r (it does only the moves the source skipped) | 0.0654 | 0.0813 | 0.0558 | 0.0418 |

Every figure above 0.1 sits at class (9, 8): a source that skips 8 of 9 moves and a private total that costs less
than the moves it replaces. With r <= h/2 nothing passes 0.1 at width <= 9 until a total is a block of rank 1 (0.110,
merged, class (8,4)). **Nearest robust statement: if a total costs at least r moves in one block, 1e-1 is excluded
at every width up to 9 (at most 0.081), and the first open classes become (47, 21) and, merged, (18, 7).** Whether
"at least r" is forced I did not prove [guess: someone must make the r skipped moves]. The two models already
disagree by a factor 2 at (6,3) (loss ratio at least 1 against 0.5144 [read ab-8]), so this is not an idle hatch.

**(b) "A term is removed only if fully known."** The proof's second line needs P_s inside L_t. If a target may
remove a term when P_s only meets L_t, the order argument gives nothing useful (the analogous set needs ALL of P_t
before ALL of L_t, probability one over a binomial coefficient) [derived]. Not tested. This is the assumption I
would attack next: it is where x-6 itself said "partial knowledge".

**(c) The shapes.** The ceilings 0.1198 and 0.1467 come from block lists with four and three blocks per data array.
They are the exchange with ports, not everything the engine can certify. ab-1's own linear programme shows that the
engine's sub-game inequalities alone allow 0.158 at block size 5. So the sentence "this decides whether the bar is
alive in the engine" should read: "in the exchange-with-ports mechanism as x-6 priced it".

**(d) Helpers are set to 0 everywhere.** That is generous to the mechanism; it only strengthens an exclusion.

## 6. ab-1's pair rule (section 4.4 there)

**Claim.** In the sub-game (characters on which every shift acts as +1, so every move is a sign), write the unit as
1 + L X (1 - T X)^-1 R: X the diagonal of (move - 1), L what the W live arrays receive from each move, R what each
move reads from the inputs, T what a later move reads from an earlier one. A *tight* character has exactly W active
moves and kernel value -1. Then any set of moves that pairwise share a tight character has at most W members.

**Check** [derived]. On a character X is -2 on the active set A and 0 elsewhere, so the unit is
1 - 2 L_A (1 + 2 T_A)^-1 R_A, and the requirement is L_A (1 + 2 T_A)^-1 R_A = 1. If A has W members all three are
W x W, so R_A L_A = 1 + 2 T_A. K = R L is one matrix of rank at most W for the whole program. For two moves of a
set S that pairwise share tight characters, the entry of K is 1 on the diagonal and 0 when the row's move is earlier.
K on S is triangular with unit diagonal: S has at most W members. Correct. The pair may be covered by a different
tight character for each pair; that is fine. I also re-derived the normal form by multiplying out a product of
rank-one switches. What I did NOT check: that the engine's sub-game is exactly this (each move one switch with the
same rank-one matrix on every character). ab-1's own exact check at block sizes 2 and 3 covers the signs of the
moves on these characters [read], not the normal form.

**Counts** [ran, all 64, 1,024 and 32,768 quadratic forms]. Forms with kernel value -1, by number of active
directions: block size 4: 56 with 4, then 136, 216, 88, 16 with 6, 8, 10, 12. Block size 5: 240 with 8, then 4,320,
9,152, 2,592, 80. Pairs of directions lying together in a tight character: **105 of 105 and 465 of 465**. Block
size 3: 12 tight, 12 of 21 pairs. So ab-1's 56, 240, 105, 465 are right, and "every direction once" (15 moves for 4
arrays, 31 for 8) is impossible. So is every multiple of it (two copies of one direction share every tight character
of that direction) [derived].

**Limit.** The rule kills that minimiser, not the linear programme's value. Another list of moves with 15/4 moves
per array at block size 4 is not excluded. Nearest useful statement: add "no W + 1 moves pairwise share a tight
character" to the programme and solve again. That is one small exact computation and nobody has run it.

## 7. Side items

- **Hybrid 4 (flat rank >= k - D)** [derived, two minutes]: correct. If the current flat is not inside the
  perpendicular of V, its intersection with it is empty or a smaller flat, so one half of the current flat misses
  it; if it is inside, the sign is constant on one half. After r terms every term is constant on a flat of dimension
  at least k - r.
- **Hybrid 1's ceiling**: the recalled theorem exists as recalled (Alon, Hoory, Linial, "The Moore bound for
  irregular graphs", 2002: the Moore bound holds with average degree) [recalled by me too, not opened].
- **ab-5** did read Find and Boyar (arXiv:1305.3041, version 2, raw text, its line 68), so "neither author read the
  paper" is out of date for ab-5. The theorem: every circuit without cancellation for the n x n subset-sum
  (Sierpinski) matrix has at least (1/2) n log n gates, and this is attained [read: search summary of the abstract].
- **ab-4's no-return theorem**: not reviewed. ab-4 itself says (its lines 164 to 169) that it is Find and Boyar's
  theorem with the hypothesis cut down, and that it did not check whether their proof already covers it.

## 8. The six questions of the brief

1. Claim: section 1.
2. Verified: sections 2, 4, 6. True at every size tried.
3. Known: yes, section 3.
4. Scale: three larger classes for the lemma; the ceiling pushed to width 4,000; law 0.1198 - about 0.25 ln(h)/h.
5. User's terms: nothing yet. No circuit size for n points, no saving exponent. It removes territory: the exchange
   with ports cannot reach 1e-1 at width <= 9 unless totals cost less than r moves or partial knowledge is allowed.
6. It does not fail. The overstatement is in the summary sentence, not in the lemma: "excluded by the engine's
   mechanism" should carry its two assumptions, and "open from (55, 24)" should not be read as a lead.

## 9. Criticism of this report

- Thirty minutes. The cost model was probed with what-if block lists of my own making; rank f x h for a total is
  not a design anybody has.
- The price controls reproduce ab-8's figures, and I did not open the three studies those figures are compared with.
- The literature was checked by two searches and memory; the full text of neither paper was opened.
- The structured rank test at (6,2) did not finish in the box.
- Not read: the wave-8 skeptics' other reports, x-6 itself, the engine's files.

Sources: [Bar-Yossef, Birk, Jayram, Kol, FOCS version](https://www.ee.technion.ac.il/people/zivby/papers/indexing/indexing.focs.pdf);
[journal version](https://birk.net.technion.ac.il/files/2021/01/BarYossefBirkJayramKol-IndexCodingWithSideInformationIEEE_TransIT2011.pdf);
[Find and Boyar, arXiv:1305.3041](https://arxiv.org/pdf/1305.3041); [Boyar and Find, arXiv:1207.5321](https://arxiv.org/pdf/1207.5321).

Files: `waves/wave-08/ac-2/`: lemma.py, rand.out, struct.out (the lemma);
price2.py, price2.out (the price law redone); hatch.py, hatch.out (cheaper totals; tight characters).
