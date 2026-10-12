# ag-6 deep-gates: forms never want a coefficient above 3; a deep gate into an output has no choice; the specimen exists, and it sits in the transform's own class, where one gate carries as many units as one likes at the same count

11 October 2026, wave 10, agent "ag-6-deepgates", 60-minute box (07:39 to about 08:35 EDT). Private. One agent; nothing
reviewed, nothing in Lean, nothing published.
Marks: [ran] = computed in this box, exact (whole numbers; no arithmetic modulo a prime anywhere); [derived] = argued by hand
in this box, checked by nobody; [read] = from a file I opened; [recalled] = from memory, no source read; [guess].
Gate count everywhere: **(G)**, a gate is any a*u + b*v, scalings free. Count (O), OpenAI's, is not used.
Folder F = `waves/wave-10/ag-6-deepgates/`.
Read: ae-cross.md in full; ad-7.md in full; ab-2.md sections 0 to 3; WAVE10-PICKS section 7; `ab-2-tallpool/tallmin.c`;
`x-0-twojobs/tj.c`; `k-cross/class19.txt` and lines 20 to 27 of k-cross.md; the headline of p-0.md. Not read: wave 9's skeptics,
g-3, the other briefs of this wave.

**No circuit below a known count for the transform, and no growth law below N log N. Nothing here changes the order or a
constant.** What there is: the brief's two experiments with exhaustive answers at 4 inputs; three short lemmas that say why
a deep gate cannot pay when the outputs are sign vectors; and the specimen the brief asked for, found where nobody looked:
in the transform's own class of matrices, at the transform's best count, with as many units of depth per gate as one likes.
That last fact changes what wall DEPTH can mean.

Words. N = 2^k points. *The transform* H has entries (-1)^(common ones). *Wire*: a value a program holds, a vector over the
inputs, scaled to whole numbers with no common factor (*primitive*). *Form*: a wire with entries 0, +1, -1. *Full sign
vector*: a form with no zero. *Tall*: a wire with an entry of size 2 or more; *height* = its largest entry in size.
*Helper*: a wire of a circuit that is neither an input nor an output; gates = helpers + outputs.
Every gate between primitive wires u, v with primitive result w can be written in exactly one way as g*w = a*u + b*v with
whole numbers a, b without common factor and g > 0; I call (|a|, |b|)/g its *kind*, |a| and |b| its *coefficient sizes*.
*Depth of a gate*: the largest power of 2 that divides a, b or g (0 = all three odd; 1 = u +- 2v, or a halving; *deep* = 2
or more, for instance u +- 4v). *Shallow* = depth 0 or 1. *Unit of depth*: one factor 2 in the determinant of the outputs.
*Class of circuits*: all circuits whose coefficient sizes lie in a given set (and whose g obeys a stated rule).
*The class of matrices* (k-cross): what one gets like H from another 2 x 2 block (*kernel*); K_t is the kernel with rows
(1, t), (t, 1), entries t^(Hamming distance). *Class identity*: one wiring that works for every kernel, with coefficients
that depend on the kernel. *Correction* (ad-7): a gate hub + (multiple of a small wire). *Level*: the number of address
bits a piece of the transform depends on; H = sum over sets S of bits of (-2)^|S| (piece of S) has k + 1 levels.
*Morgenstern's bound* [recalled]: in a circuit of whole-number gates a*u + b*v without division, the largest N x N
determinant among the wires grows by a factor at most |a| + |b| per gate.

## 0. In twelve lines

1. [ran, exhaustive] **Experiment (a): no specimen with forms.** 4 inputs, every set of 2 to 8 targets that are forms,
   223,872 classes: the least count with coefficient sizes {1, 2} is never beaten by {1, 2, 4, 8}. Zero classes.
2. [ran, exhaustive] **Which coefficient ever pays: only 3.** Same sets, 4 to 7 targets: adding the single size c to
   {1, 2} saves a gate in 2, 3, 18, 68 classes for c = 3 and in **no class for c = 4, 5, 6, 7, 8, 9**. With all sizes 1 to 9
   allowed the savings are the same 2, 3, 18, 68; against the reference {1, 2, 3} nothing up to 9 saves anything. Division
   by the common factor changes no count. So the reason 4 does not pay is not that it is even: 5, 7 and 9 do not pay
   either. Section 2.
3. [ran, exhaustive] **Experiment (b) at 4 points.** The transform costs 7 gates with sizes {1, 2}, and **8 without a
   gate of depth exactly 1**: 8 with {1} alone (the textbook), 8 with {1, 4, 8}, 8 with odd sizes up to 11. All 228 sets of
   helpers of 7-gate circuits in the classes {1, 2, 4, 8} and {1, 2, 3, 4, 8} are circuits with sizes 1 and 2: no best
   circuit holds a deep gate. One gate above, they are common: 4,560 of the 14,587 irredundant 8-gate circuits need one.
4. [ran, census of walks by x-0 and ab-2 + my own walk] **8 points.** None of the 26 printed circuits with 19 gates holds a
   deep gate or a halving. 19 of the 125 printed with 20 gates hold exactly one gate u +- 4v. In 17 of the 19 the tall
   wire can be exchanged for one form (or dropped), giving a circuit of the same size with sizes 1 and 2 only. With
   u +- 2v forbidden and u +- 4v, u +- 8v allowed, a walk from the textbook stays at 24 (weak: 161 distinct states); the
   same walker with {1, 2} goes from 24 to 19 in under a minute.
5. [derived] **Three lemmas** (section 4). TALL END: a deep gate has a tall parent or a tall result. NO CHOICE: if the
   result of a deep gate is a form, the tall parent determines it (round every entry modulo 4), so a tall wire feeds at
   most one output through deep gates; a gate u +- 2v leaves every sign free, and the 19 is a tree of such gates.
   RE-BRACKETING: (c + 2e') + 4v = c + 2(e' + 2v): a deep gate after a shallow one is two shallow gates with the middle
   wire changed from a form that others could share to a tall wire that nobody else can use.
6. [ran, exact] **The specimen exists, in the transform's class.** The 19-gate wiring computes the third power of K_t
   for every whole t tried (k-cross found this; I rebuilt it for t = 2, 3, 5, 7, 9, 15, 17, 31, 63). For odd t its gates
   are 7 merges of depth 0 and **12 corrections of depth exactly e = the number of factors 2 in t^2 - 1**: 3, 3, 4, 4, 5, 5,
   6, 7. The sum of the gate depths equals the depth of the determinant (36, 36, 48, 48, 60, 60, 72, 84): every unit is
   carried by a correction, e units per gate.
7. [ran + derived] **It beats every circuit with coefficients 1 and 2.** For t = 3: 19 gates with twelve gates u +- 8v
   (or +- 24v); a division-free circuit with sizes 1 and 2 needs at least 23 by Morgenstern. At 4 points [ran, exhaustive]:
   rows (1,3,3,9), (3,1,9,3), (3,9,1,3), (9,3,3,1) cost 7 gates with gates of depth 3 and **at least 8 in every circuit
   whose gates have depth at most 2** (sizes 1 to 7 and 9, no division by a multiple of 8), and at least 8 with odd sizes
   up to 9. **For u +- 4v exactly** [ran, exhaustive]: the kernel with rows (1,1), (1,-3), squared: rows (1,1,1,1),
   (1,-3,1,-3), (1,1,-3,-3), (1,-3,-3,9) cost 7 gates with deep gates and at least 8 when every gate has depth at most 1
   (sizes 1, 2, 3, 5, 6, 7, 9, no division by a multiple of 4). The smallest of all: rows (1,1), (1,-3): 2 gates with
   u - 4v, 3 with sizes 1 and 2.
8. **What that does to wall DEPTH.** The count 19 does not depend on t; the depth does (12 e units). So gates are not
   paid per unit of depth. A correction crosses one LEVEL and carries whatever a level weighs for that kernel: the
   kernel's determinant. For the transform a level weighs one factor 2, which is why ad-7 saw "one gate u +- 2v per
   unit". Section 6.
9. **Growth law: none.** In the specimen's family e is a property of the kernel, free at every N (t = 2^e - 1 gives
   e + 1), and the count is the same (3/4) N log2 N for every e [8 points: ran; 16 points: read in p-0; beyond: not
   checked]. Against circuits with sizes 1 and 2 the deep circuit wins by a factor that grows with e (0.42 e), but both
   are N log N. For the transform itself a gate that crosses two levels at once is a gate u +- 4v whose tall parent is the
   two-digit prefix of ONE output (lemma NO CHOICE): that is ae-cross's digit ladder, and its price is brief 1's question.
10. KEEP ASKING, answered [derived + ran]: for u + 4v to be an output y, v is forced by u: v = (y - u)/4 is a form on the
    set where u has entries of size 3 or 5 (4 where y is zero), and u, v, y lie on one line with the two parts of y. In everything printed a
    tall wire serves at most two outputs, one through the deep gate and one through a shallow gate (5 circuits).
11. 5 inputs with 4 targets [ran]: no saving for {1, 2, 4, 8} in the 4,980 of 5,606 classes that need at most 3
    helpers; the other 626 were not tested. Not done: the class census of the 52, 128, 304 with t = 3 (I rebuilt the
    19 only).
12. State: the idea turned into a better question. Not "can a gate carry two units" (it can carry seven) but: **the count
    follows levels, not digits; is there a circuit, for any kernel, in which one gate crosses two levels and serves more
    than one output?** Lemma NO CHOICE says where it cannot be; the one place tried where it could be (4 points, the
    kernel with rows (1,1), (1,-3), size 16 allowed) has no such circuit at the best count [ran, exhaustive].

## 1. The tool and its controls [ran]

`deepmin.c` (in F; it starts from ab-2's `tallmin.c`). A wire is a primitive whole-number vector up to sign. A class of
circuits is a set of allowed coefficient sizes and a rule for g. There is NO cap on heights: the class decides which wires
can appear. For a set of targets it finds the least number of helpers in a reference class by trying 0, 1, 2, ... helpers,
exhaustively each time, and then asks whether one helper fewer suffices in a challenger class. At a node every wire one
allowed gate away from the wires held is a candidate; a target one allowed gate away is taken at once; a candidate tried at
a node is not tried again under its later siblings (a wire that can be made now can be made first). Target sets: all sets
of m forms on 4 inputs, one per class under permutations and sign changes of the inputs (ab-2's loop), or a file.
Controls.
- The transform at 4 points: 3 helpers, 7 gates, in the class {1, 2}.
- 4 inputs, 4 targets, reference {1, 2}: the histogram of helpers is 78, 244, 137, 7, 1 for 0 to 4 helpers, the same as
  ab-2's histogram for circuits of forms [read: `ab-2-tallpool/n4_m4_M3.out`].
- Challenger {1, 2, 3}: 2, 3, 18, 68 classes with a saving at 4, 5, 6, 7 targets. ab-2 found 2, 3, 18, 70 with tall wires of
  any coefficient and noted that all but 2 of the 70 use a coefficient 3. The two programs agree, and the first specimen
  printed is ab-2's (helper 2 x1 - x2 - x4, last gate with coefficient 3).
- 2 points, rows (1,3), (3,1): 3 gates with {1, 2}, 2 with a coefficient 3, as by hand.

## 2. Experiment (a): forms on 4 inputs [ran, exhaustive in each class]

| targets | classes | {1,2} against {1,2,4,8} | {1,2} against {1,2,3} | {1,2} against {1,2,c}, c = 4, 5, 6, 7, 8, 9 | {1,2} against all of 1..9 | {1,2,3} against all of 1..9 |
|---|---|---|---|---|---|---|
| 2 | 15 | 0 | 0 | | | |
| 3 | 82 | 0 | 0 | | | |
| 4 | 467 | 0 | **2** | 0, 0, 0, 0, 0, 0 | 2 | 0 |
| 5 | 2,408 | 0 | **3** | 0, 0, 0, 0, 0, 0 | 3 | 0 |
| 6 | 11,329 | 0 | **18** | 0, 0, 0, 0, 0, 0 | 18 | 0 |
| 7 | 46,180 | 0 | **68** | 0, 0, 0, 0, 0, 0 | 68 | 0 |
| 8 | 163,391 | 0 | **133** | | | |

(An entry is the number of classes of target sets in which the second class of circuits needs one gate fewer than the
first. Two gates fewer: never.) Also [ran]: with no division at all (g = 1) instead of free division, the histograms and
all the savings at 4 to 7 targets are the same; {1, 2, 3} against {1, 2, 3, 4, 8}: 0 at 4 to 7 targets; targets that are
full sign vectors, 1 to 8 of them: 0 for {1, 2, 4, 8}. Files `n4_*.out`.
**So on 4 inputs a circuit for forms never wants a coefficient other than 1, 2 and 3, up to size 9; and a gate
u +- 4v or u +- 8v never does what gates u +- v and u +- 2v cannot.**

Why 3 and nothing larger [derived, a sketch, not a proof]. In every specimen the wire that pays is a junction p: it lies
on three lines of the circuit. Two of them are "p = sum of two targets", which puts an entry 2 in p where the two targets
agree; the third is "target = c x - p" for an input x, which needs that entry to be c - 1. So c = 3: three forms that agree
at one input and cancel elsewhere, 1 + 1 + 1. For c = 4 the junction would need an entry 3, which is not the sum of two
forms; it is form + 2 x form, and then the line through x and the target already holds the form, so a shallow gate does
the job without p. A coefficient c asks for c - 1 forms that agree at a point, and preparing them costs what it saves.

5 inputs, 4 targets, {1, 2} against {1, 2, 4, 8} [ran on the rented machine in two halves, 11 minutes each,
`linux/n5_m4_ref6_ch278_hcap3_split*.out`]: 5,606 classes; reference helpers 0, 1, 2, 3 in 113, 687, 2,011, 2,169
classes and 4 or more in 626. **No saving in any of the 4,980 classes that need at most 3 helpers.** The 626 that need
more were not tested (the search stops at 3 helpers), so 5 inputs is 89 % done. The histogram agrees with ab-2's for
circuits of forms (113, 687, 2,009, 2,167, 630) up to 6 classes that move down by one, and ab-2 reports exactly 6
classes at 5 inputs where a tall wire saves a gate with coefficients 1 and 2 only.

## 3. Experiment (b): the transform [ran]

**4 points, exhaustive in each class** (`h4_*.out`, and the runs quoted in section 1):

| class of circuits | least gates |
|---|---|
| sizes {1, 2} | 7 |
| sizes {1} (the textbook's class) | 8 |
| sizes {1, 4, 8}, any division: u +- 2v forbidden, deep gates allowed | 8 |
| odd sizes {1, 3, 5, 7, 9, 11}, odd division: no gate of depth 1 or more | 8 |

A deep gate does not replace the gate u +- 2v: forbid it and the count is the textbook's, whatever else is allowed.
All circuits with 7 gates: 228 sets of helpers in the class {1, 2, 4, 8}, the same 228 in {1, 2, 3, 4, 8}, every one
realisable with sizes 1 and 2. With 8 gates in the class {1, 2, 4, 8}: 47,821 sets of 4 helpers, 14,587 in which no helper can
be dropped, and 4,560 of those cannot be built with sizes 1 and 2 in any order. So one gate above the least, a deep gate
is an ordinary thing. By hand, the simplest: y3 = (1,-1,-1,1) = u + 4 x3 with u = (1,-1,-1,-3) = y1 - 2 (x2 + x3); u is
"the first two digits of y3" (section 6).

**8 points.** Exhaustive search is out of reach (11 helpers). What there is:
- Census [ran, `census8.py`, `census8.out`] of every circuit printed by the walker `tj` in x-0's and ab-2's runs; those
  walks allow every coefficient up to 40 and entries up to 7 or 15, and the ledger prints for each wire its cheapest
  parents. 19 gates: 26 circuits, kinds 182 x (1,1) and 312 x (1,2), no deep gate, no halving. 20 gates: 125 circuits;
  **19 hold exactly one gate of kind (1,4)**, with 7 + 12 + 1 or 8 + 11 + 1 gates of kinds (1,1), (1,2), (1,4). 21 gates:
  18 circuits, no deep gate, one halving. 52 and 53 gates at 16 points: 9 circuits, none.
- Anatomy of the 19 [ran, `reassoc.py`, `exchange.py`]. In 16 the deep gate makes an OUTPUT from a tall wire of height 3
  that a gate of kind (1,2) made; in 11 of these the tall wire has no other use, in 5 it has a second use (in the two I
  printed, a second output through a shallow gate). In 3 the deep gate makes the tall wire (form + 4 x form) and a
  shallow gate rounds it. Take the tall wire out and put ONE form in its place: 16 times that gives a circuit of the same 20 gates with sizes 1 and 2 only;
  once the tall wire can simply be dropped (19 gates); twice no single form will do.
  Example (`ab-2-tallpool/t8_A15.out`): u = y' + 2 w6 = (1,-1,1,3,-3,-1,1,-1), output = u - 4 w4 with w4 = x3 - x4; the
  same output is y' + 2 e with e = w6 - 2 w4 = (0,0,1,-1,1,-1,0,0).
- A walk in the class {1, 4, 8} [ran, `tjd.c` = tj with the coefficient sizes of every gate restricted; `t8_amk274_s5.out`]:
  from the textbook's 24 gates, 300 seconds, 12,744 steps, 161 distinct circuits, best 24. Control (`t8_ctl_amk6.out`): the
  same program in the class {1, 2} goes from 24 to 19 within 40 seconds. The walk is local and found few neighbours;
  "24" is weak evidence. With the 4-point result it reads: without u +- 2v, nothing found below the textbook.

## 4. Three lemmas [derived]

**TALL END.** Let w = u + 2^e v with e >= 2, u and w primitive and different. Then u and w agree modulo 4 in every
entry and differ somewhere, so one of them has an entry of size 2 or more. In general one of them has height at least
2^(e-1). Two forms are never joined by a deep gate. The same holds for a deep halving (u +- v)/2^e: the two parents agree
modulo 2^e up to sign.

**NO CHOICE.** Let w = u + 2^e v with e >= 2 and w a form. Then w is the vector obtained from u by reducing every entry
modulo 4 into {-1, 0, 1}; v = (w - u)/2^e. So u determines w and v: **a wire is the parent "u" of deep gates into at most
one form.** (For the general kind g w = a u + b v with b a multiple of 4 and a, g odd: w is +-u modulo 4, the same
conclusion.) Contrast with e = 1: w is u modulo 2, which fixes the support of w and leaves every sign free. That freedom
is what the 19-gate circuit lives on: from its centre a tree of gates u +- 2v, each full sign vector feeding two more
(all outputs of H are the same vector modulo 2, and all different modulo 4). In general a gate of depth e has no choice
whenever its result has height below 2^(e-1).
Counting classes: the outputs of H fall into 1 class modulo 2 and N classes modulo 4. The outputs of subset sums fall
into N classes already modulo 2, which may be why no saving of this kind has been seen for subset sums [guess].

**RE-BRACKETING.** (c + 2 e') + 4 v = c + 2 (e' + 2 v). A sum of weighted wires costs (number of terms - 1) gates
however it is bracketed; a saving can only come from a partial sum that two outputs share. Bracketed with the deep gate
last, the partial sum is u = c + 2e', tall, and by NO CHOICE it reaches one output only through a deep gate (in 5
printed circuits it reaches a second through a shallow gate). Bracketed with shallow gates, the
partial sum is e = e' + 2v, a form, which other outputs may share. For sign vectors: e' is the right set with the wrong
signs on a part B, and the deep gate with v = (the form on B) repairs the signs after the flip instead of before it.
So in this pattern, for outputs that are forms, the shallow bracketing is never worse and can be better. This is what the table of
section 2 and the 16 exchanges of section 3 show; I have no proof for circuits in which the tall wire is made by
something other than one shallow gate.

## 5. The specimen: the transform's own class [ran, exact; `class_depth.py`, `class_depth.out`]

k-cross found that the 19-gate wiring computes the third power of every kernel tried, with coefficients that depend on
the kernel (`k-cross/class19.txt` has t = 2 and t = 3 written out). Read those coefficients as functions of t: the merges
use t, the corrections use t^2 - 1 (times a power of t). I rebuilt the circuit from that one formula for nine values of t,
replayed each in whole numbers against the entries t^(Hamming distance), and reduced every gate to primitive wires.

| t | kinds of the 7 merges | kinds of the 12 corrections | depth of each correction | sum of gate depths | determinant of the outputs | sizes 1 and 2 without division need at least (from the factors 2 alone) |
|---|---|---|---|---|---|---|
| 3 | (1,3) | (1,8), (1,8)/3, (3,8), (1,24) | 3 | 36 | 2^36 | 23 gates |
| 5 | (1,5) | (1,24), (1,24)/5, (5,24), (1,120) | 3 | 36 | 2^36 x 3^12 | 23 |
| 7 | (1,7) | (1,48), (1,48)/7, (7,48), (1,336) | 4 | 48 | 2^48 x 3^12 | 31 |
| 9 | (1,9) | (1,80), (1,80)/9, (9,80), (1,720) | 4 | 48 | 2^48 x 5^12 | 31 |
| 15, 17 | (1,t) | (1,224), ... ; (1,288), ... | 5 | 60 | 2^60 x odd | 38 |
| 31 | (1,31) | (1,960), ... | 6 | 72 | 2^72 x odd | 46 |
| 63 | (1,63) | (1,3968), ... | 7 | 84 | 2^84 x odd | 53 |

(For t = 2 the determinant is 3^12: no factor 2 at all, and the same 19 gates.)
- **A gate u +- 2^e v carries e units of depth, e = 3 to 7 here, in a circuit of 19 gates for a matrix built exactly like
  the transform.** All 12 e units of the determinant sit in the 12 corrections; the merges carry none.
- Against coefficients 1 and 2 [derived from Morgenstern, recalled]: a division-free circuit with sizes 1 and 2 multiplies
  the largest determinant by at most 3 per gate, and the outputs (rows with an entry 1, so primitive; scalings and
  relabellings cannot remove a factor 2) have determinant at least 2^(12 e). So at least 12 e / log2(3) gates: 23 for
  t = 3. The deep circuit has 19. (With the rows exactly as they stand the odd part of the determinant counts too and
  the program prints 35, 43, 48, ... for t = 5, 7, 9; the column keeps to what no scaling of the inputs can change.)
- 4 points [ran, exhaustive, `k3x2_*.out`]: the second power of K_3, rows (1,3,3,9), (3,1,9,3), (3,9,1,3), (9,3,3,1):
  7 gates in the class {1, 3, 8, 24}; **no circuit with 7 gates** in the class of sizes {1, 2, 3, 4, 5, 6, 7, 9} with no
  division by a multiple of 8 (every gate of depth at most 2; 200 seconds), and none with odd sizes {1, 3, 5, 7, 9} and
  odd division. So here the deep gate is not a way of writing something shallow: without it one gate more is needed.
- 2 points [ran]: rows (1,1), (1,-3): x + y, then (x + y) - 4y: 2 gates; 3 gates with sizes 1 and 2 (exhaustive). This is
  the smallest matrix where a gate u +- 4v beats every circuit with coefficients 1 and 2. It is a specimen only against
  {1, 2}: the single gate x - 3y does it too.
- 4 points, the same kernel squared [ran, exhaustive, `km3x2_*.out`]: rows (1,1,1,1), (1,-3,1,-3), (1,1,-3,-3),
  (1,-3,-3,9). The determinant of the kernel is -4, so a level weighs two factors 2. 7 gates exist in the class of sizes
  {1, 2, 3, 4, 6, 8, 9, 12}; **none with 7 gates when every gate has depth at most 1** (sizes {1, 2, 3, 5, 6, 7, 9}, no
  division by a multiple of 4; 91 seconds), and none in the class {1, 2, 4} either (the merges need an odd size above 1).
  This is the brief's specimen in its own words, a gate u +- 4v that beats every circuit of shallow gates tried, for a
  4 x 4 matrix; an odd coefficient cannot stand in for the 4 here. The first circuit the program printed, replayed by
  hand:  a = x0 + x1;  b = x2 + x3;  y0 = a + b = (1,1,1,1);  y2 = a - 3b = (1,1,-3,-3);  h = 4 x0 - 3 y0 = (1,-3,-3,-3);
  y1 = h + 4 x2 = (1,-3,1,-3);  y3 = h + 12 x3 = (1,-3,-3,9).  Three gates of depth 2 (h, y1, y3) carry 6 of the 8 units;
  the pair y0, y2 carries the other 2 the textbook's way. All 7-gate circuits in that class: 126 sets of helpers, none
  of them buildable with shallow gates (`km3x2_enum3_4958.out`). For K_3 squared: 66 sets in the class {1, 3, 8, 24}, none
  buildable with gates of depth at most 2 (`k3x2_enum3_class.out`).
- The transform is the member of the class where a level weighs one factor 2: t = -i gives t^2 - 1 = -2. Its gate
  u +- 2v IS its deep gate. Section 3's table (7 gates with it, 8 without) and the K_3 line above (7 with depth 3, 8
  without) are the same statement for two kernels.
The specimens do not have "entries of one size", and they are not orthogonal up to scale. Among matrices with entries
+-1 the search of section 2 found none (full sign vectors: none), and at 4 and 8 points the transform is the only
orthogonal one up to relabelling and signs [recalled].

## 6. What this says about wall DEPTH, and the growth law

ae-cross states DEPTH as: "the transform is k binary digits deep and every known program pays about N per digit", and
guesses that a linear program must account for about (log2 N)/2 units per gate. ad-7 measured one gate u +- 2v per unit.
Section 5 says [ran at 8 points]: change the kernel and the same program, gate for gate, carries 3, 4, 5, 6, 7 units per
correction. The number of corrections does not move. So:
- **Units of depth are not what the gates are paid for.** The 12 corrections at 8 points, and the (N/2) log2 N of the
  3/4 family, count LEVEL CROSSINGS [my reading]: each correction multiplies one more factor (t^2 - 1) into part of a
  wire, that is, moves that part one level up (k-cross counts the same gates as rectangles). What a crossing weighs is the kernel's determinant: one factor 2 for the transform, e factors for K_t.
  "One gate per unit" was a property of the number -2, not of the gates.
- **The hoped-for law fails in a precise way.** The brief: if a gate can carry e units, corrections could fall towards
  (N/2) log2 N / e. A gate can carry e units, for every e, at every N, and the corrections stay (N/2) log2 N, because the
  matrix that is e times deeper is e times deeper at every level. How e may grow with N in the specimen's family: it
  need not grow with N at all; it is a free parameter of the kernel (t = 2^e - 1 gives e + 1).
- **For the transform itself** the only way to use a gate u +- 4v is to cross two levels at once. Its tall parent is then
  the output's first two digits, D0 - 2 D1(y) in ae-cross's notation (D_j(y) = the sum of the level-j pieces inside y),
  which by NO CHOICE belongs to that output alone. N such parents are N different wires of rank k + 1, and ad-6 makes them
  all in N + o(N) gates. So a deep gate in a program for H is one rung of ae-cross's digit ladder, and whether it pays is
  exactly brief 1's question (does a level ever cost less than N). Nothing in this box moves that.
- **Two levels with one gate, tried where NO CHOICE does not forbid it** [ran, exhaustive, `km3x2_enum3_with16.out`].
  For the kernel (1,1), (1,-3) squared a level weighs 4, two levels weigh 16, and one output has an entry 9, tall
  enough for a gate of depth 4. Allow the size 16 as well: the 7-gate circuits are the same 126 sets of helpers, every
  one buildable without it. So at the best count no gate crosses two levels, here either. (For the transform this is
  the "228 of 228" of section 3.)
- Wall, restated: **LEVELS. A correction crosses one level whatever the level weighs; a gate that crosses two has a
  private parent when the outputs are sign vectors.** DEPTH in the 2-adic sense is not a wall in count (G): the class
  shows depth riding free.
- A correction to the brief's premise [derived; ab-2 item 8 has the same number]: Morgenstern does not force a growing
  coefficient below (N/2) log2 N. That threshold is for gates u +- v alone. With gates u +- 2v allowed it is
  (N/2) log2 N / log2(3) = 0.315 N log2 N, far below the 0.75 of the best family. For K_3 the same bound stands at
  0.946 N log2 N, above 0.75: there the deep coefficient is forced, and there it is.
- One reading [derived, one line]: over the Gaussian whole numbers 2 = -i (1 + i)^2, the outputs with entries
  (-i)^(distance) are one class modulo (1 + i)^2 and N classes modulo (1 + i)^3, so the transform's flip u +- 2v is
  already a gate two half-digits deep with full fan-out. The half-digits in between are empty (ad-7 said so).

## 7. What I would try next (mutations)

1. **levels-census** (an hour, decisive for the reading): substitute the kernel K_3 into the 52, 128 and 304 of e2-0 and
   into the second 52; solve the coefficients; count the gates of depth 3. Prediction: 32, 80, 192, the same wires as the
   gates u +- 2v of ad-7's census. If a record circuit is NOT a class identity, its deep gates are the first thing to look
   at (it would be using something only the transform has).
2. **two-levels-with-fan-out**: is there, for any kernel, a circuit in which one gate crosses two levels and its tall
   parent serves two outputs? NO CHOICE forbids it when outputs are forms and the gate ends in an output; it does not
   forbid a tall parent that serves two tall wires, each rounded later. Exhaustive at 4 points with `deepmin` on the
   second power of K_3 with gates of depth 6 allowed; then the 16-point rows modulo 4.
3. **the two circuits that resist the exchange** (20 gates, 8 points): a tall wire serving two outputs, one deeply and
   one shallowly, where no single form does. Classify them; they are the only objects found where a tall wire does
   something a form does not for sign-vector outputs.
4. **finish 5 inputs**: the 626 classes that need 4 or more helpers (the challenger must be searched at 3 helpers,
   about half a minute per class as the program stands), then 5 targets, and 6 inputs with full sign vectors.
5. **prove the table of section 2**: "for targets that are forms, sizes {1, 2, 3} suffice". The sketch in section 2 is
   a start; a proof would be a small theorem about junctions of three lines among forms.
6. **halvings**: the class of this box allows them (free division) and none was ever needed at 4 inputs. Brief 2
   (halving-or-nothing) asks the same at 8 points for the transform; lemma TALL END applies to a halving by 4 as well.

## 8. Criticism, last

- Experiment (a) is exhaustive only inside classes of circuits with coefficient sizes up to 9. A coefficient 10 or more
  was never tried. The forms are on 4 inputs; at 5 inputs only 4 targets, only {1, 2, 4, 8}, and 626 of 5,606 classes
  are undecided.
- "Only 3 pays" is a table plus a sketch. I did not check that the 68 and the 133 are the same classes as ab-2's.
- The census at 8 points counts circuits that two other agents' walks happened to print from the 19; "none of 26" is not
  "none". The walk without u +- 2v is weak.
- RE-BRACKETING is proved only for the pattern "tall wire made by one shallow gate, used once". Two of 19 circuits are
  outside it.
- Section 5 at 8 points is a replay of one wiring for nine kernels, not a statement about least counts: I do not know
  that 19 is the least for K_3, only that it is the transform's best count and that sizes 1 and 2 need 23. Morgenstern's
  bound is recalled, and I applied it to primitive outputs with a three-line argument about scalings.
- "The count follows levels, not digits" rests on k-cross's class identity at 8 points (replayed here), on p-0's sentence
  for the 52 (read, not replayed), and on nothing at 32 and 64 points. Mutation 1 is the test.
- The kernel K_t is the transform's kind only in k-cross's sense. It is not orthogonal and its entries are not of one
  size; the brief's strict version of the question (orthogonal, one size) has the answer "none found", not a specimen.
- The reading of DEPTH is negative for the idea as briefed: a deep gate is not a way to fewer gates in anything here.
- Nothing here changes the order, or any constant.

Files in F: `deepmin.c` (the search; binaries deepmin2f, deepmin4, deepmin4e, deepmin4f, deepmin4g, deepmin5 are the same
source at different moments and input counts); `n4_m*_ref*_*.out`, `n4_full_*.out` (section 2); `h4.txt`, `h4_enum4_278.out`,
`h4_odd2730_div1.out` (section 3, 4 points); `census8.py`, `census8.out`, `census8b.py`, `census8b.out`, `census4.out`,
`reassoc.py`, `reassoc.out`, `exchange.py`, `exchange.out` (the walks' circuits); `tjd.c`, `s24.txt`, `t8_amk274_s5.out`,
`t8_ctl_amk6.out` (walks in a class); `class_depth.py`, `class_depth.out` (section 5, 8 points); `k3.txt`, `k3x2.txt`,
`k3x2_shallow766_div5.out`, `k3x2_odd682_div1.out`, `km3.txt`, `km3x2.txt`, `km3x2_*.out` (section 5, 2 and 4 points);
`k3x2_enum3_class.out`, `km3x2_enum3_4958.out`, `km3x2_enum3_with16.out` (all 7-gate circuits of the two deep kernels); `runA.sh`, `runB2.sh`,
`runC.sh`, `runE.sh` (the batches; `runB.sh` was stopped, its 5-input part was too slow on this machine);
`linux/n5_m4_ref6_ch278_hcap3_split0.out`, `..._split1.out` (the 5-input runs, copied back from the rented machine).
