# ab-2 tallpool: the smallest tall wire that pays, and what the transform lacks

11 October 2026, 04:45 to about 05:30 EDT, 60-minute box. Private. One agent; nothing reviewed, nothing in Lean, nothing published.
Marks: [ran] = exact run of mine tonight (whole numbers only; files in `ab-2-tallpool/`); [derived] = by hand tonight, checked by
nobody; [read] = from tonight's reports; [guess].
Gate count everywhere: **(G)**, a gate is any a*u + b*v, scalings free. Count (O), OpenAI's, is not used.
Read: w-cross.md in full, x-0.md in full, WAVE8-PICKS (word list and brief 3), the head of `x-0-twojobs/tj.c`, the 19-gate file.
Not read: u-4 (I recomputed its Z D Z^T instead of reading it), x-1, x-2, x-5, x-9, the skeptics' reports. Where I name
x-1, x-5, x-9 it is through w-cross's account of them.

**No circuit below a known count for the transform, and no growth law below N log N. Nothing here changes the order or a constant.**
What there is: the answer to the brief's "keep asking" (the smallest matrix with entries 0, +1, -1 for which a tall
intermediate wire saves a gate, found exhaustively, 112 specimens replayed exactly), the anatomy of those specimens, one
line that says why the transform's outputs cannot have it, a growth law for the trick (it saves one gate per row of a
grid), a count showing that no best-count circuit of the night has room for it, and the brief's first experiment (flat).

Words. N = 2^k points; *the transform* H has entries (-1)^(common ones). *Wire*: a value a program holds, a vector over the
inputs, scaled to whole numbers with no common factor. *Height*: its largest entry in absolute value. *Form*: a wire of
height 1 (entries 0, +1, -1). *Tall*: height 2 or more. *Full sign vector*: a form with no zero entry. *Helper*: a wire of a
circuit that is neither an input nor a target (an output); gates = helpers + targets. *Line through u and v*: all wires
a*u + b*v; a gate puts a new wire on the line through two wires already held. *Junction*: a wire that lies on three or
more lines of the circuit. *Class*: target sets that differ only by renaming the inputs and changing their signs.

## 0. In twelve lines

1. [ran, exhaustive] **The smallest matrix for which a tall intermediate wire saves a gate has 4 inputs and 4 rows.**
   Rows (1,0,-1,-1), (0,1,0,-1), (1,-1,1,0), (1,1,0,1): 7 gates with forms, 6 gates with the helper p = 2 x1 - x2 - x4.
   None on 3 inputs (any number of targets), none on 4 inputs with 3 targets or fewer. Section 2.
2. [ran] **112 classes of target sets found where a tall wire saves a gate (4 inputs with 4 to 7 targets, 5 inputs with 4);
   every one replayed exactly.** In 110 of the 112 the tall helper is the plain sum or difference of two TARGETS. The saving
   is exactly one gate in every class (no class with two gates saved). Height 2 is enough; height 3 and beyond buy nothing
   more at 4 and 5 inputs.
3. [ran] **Target sets made only of full sign vectors (no zero entry, like the rows of H): no saving in anything searched**:
   4 inputs, every set of 1 to 8 targets; 5 inputs, every set of 1 to 10; 6 inputs, sets of 2 and 3.
   **And none of the 112 specimens is a matrix of zeros and ones** after any change of signs (like the subset-sum matrix
   Z). A tall wire paid only where the targets have BOTH zeros and opposite signs. The rows of H have signs and no
   zeros; Z has zeros and no signs; H = Z D Z^T is made of two things each of which lacks one of the two.
4. [derived, one line] Why: **the sum or difference of two full sign vectors is twice a form. It is never tall.** The tall
   wire of the specimens is b - a for two needed wires a, b with DIFFERENT supports that agree on a shared part: the shared
   part cancels, the opposite part doubles, and b - a is cheaper than b. With full sign vectors the same subtraction gives
   the flip "hub + 2 x small form", which is the gate the 19-gate circuit is made of. The transform already uses the trick
   in the only shape its outputs allow.
5. [derived] **Growth law of the trick.** Needed wires R_i + a_j, a grid of q "rests" and r "tails": tall differences of
   tails save min(q, r) - 1 gates out of about q r + r. A saving along one side of a two-sided grid: its share goes to
   zero as the grid grows. This kind of tall wire cannot change the order, whatever the matrix. Section 3.
6. [derived; the case list ran] **A tall wire of height 2 that is one gate from two outputs of H, each time with a form as
   partner, and is not on the line through the two outputs, lives only on the half where the two outputs agree, and its
   partners cover more than the other half.** For several outputs: it lives on the points where they all agree (N/4 for
   three or four). So near the outputs a tall wire is smaller than a hub and its partners larger. That is w-cross fact C
   with sizes. Section 4.
7. [ran, walks, weak] **The transform against the height cap: flat.** 8 points, pools with entries up to 7 and up to 15:
   245 and 159 distinct circuits visited from the 19, none of 18. 16 points, entries up to 3 and up to 7: 41 and 95
   circuits from the 52, none of 51; that is too few to say anything (section 1). With x-0 (entries up to 3) and g-1's proof at 4 points: 7, 19 for every cap tried.
7b. [ran] **The brief's "one known specimen" is not tall.** In the second pass of Z D Z^T (one address bit at a time)
   every wire is a power of 2 times a form on a subcube: as a primitive wire its height is 1, at 8, 16, 32, 64 points. The
   "height N/2" is a common factor, and every gate between the primitive wires is "form - 2 x form": the flip again.
   Only when the sum is cut by levels (x-1's digits) are the partial sums tall: largest heights 1, 7, 17, 15, 1 at 16
   points and 1, 11, 49, 111, 129, 63, 1 at 64. So the specimen is not one. The tall wires that are known in circuits for
   H sit one gate above the best count (53 of the 121 circuits of 20 gates at 8 points that the walks printed) or above
   the textbook (x-1's levels, x-5's tower, x-9's hubs); no circuit AT its best known count holds one.
8. [derived from x-0 lemma 3] **Where the lemma forces height.** At the 16-point rate of 3.25 gates per point a circuit of
   forms is impossible from 256 points on; height 2 is impossible from 65,536 points on; height 3 from 2^23; height 7 from
   2^39. At any rate c N log2 N with c >= 0.316 the lemma forces nothing, ever; the best family known has c = 3/4. The
   published program is below 0.316 N log2 N only for log2 N above about 10^572. Section 5.
9. Side fact [ran]: among the 343 classes of invertible 4 x 4 matrices with entries 0, +1, -1 exactly one has a circuit
   below "n - 1 + log2 of the determinant" (the count if every gate that is not a merge brought one unit): determinant 12,
   6 gates, forms only. So forms can bring more than one unit per gate without paying it back when the determinant has a
   factor 3. For determinants that are powers of 2 no class does, at this size.
10. [ran] **The best circuits have no place for it.** In the 19, the 52 and the whole (3/4) family up to 64 points
    (304 gates, 52,768 tall sums or differences of two wires) no tall difference occurs for two pairs of wires. In 74 of
    121 circuits of 20 gates at 8 points one does. Section 4(c).
11. State: the idea turned into a better question. Not "which pool", but: **where in a circuit for the transform are there
    two needed wires with different supports that agree on a shared part, both wanted on top of the same two or more
    rests?** Section 6 says where to look and what to run.

## 1. The first experiment: the transform against the height cap [ran]

The pool of the brief, "sum over j of 2^j f_j with f_j forms", is contained in "all wires with entries up to 2^(J+1) - 1",
which is what `x-0-twojobs/tj8` and `tj16` take as a mask. That larger pool contains the one-flag pool and every two-frame
pool at once, so I ran it and did not build the smaller ones. Walks with kicks from the known circuits:

| points | entries allowed (largest j) | coefficients tried up to | seconds | distinct circuits visited | best |
|---|---|---|---|---|---|
| 8 | up to 7 (j <= 2) | 40 | 300 | 245 | 19 |
| 8 | up to 15 (j <= 3) | 40 | 300 | 159 | 19 |
| 8 | up to 3 (j <= 1) [read: x-0] | 4 | 140 | 536 | 19 |
| 8 | up to 1 (forms) [read: x-0] | 2 | - | 7,741 | 19 |
| 8 | up to 2, from the staircase 20 | 8 | 300 | 1651 | 19 |
| 16 | up to 7 | 40 | 400 | 2 | 52 |
| 16 | up to 7 | 6 (a restriction) | 570 | 95 | 52 |
| 16 | up to 3 | 18 | 575 | 41 | 52 |

Files `t8_A7.out`, `t8_A15.out`, `t8_A2_stair.out`, `t16_A7.out`, `t16_A7_K6.out`, `t16_A3.out`. Control: the walker is x-0's, which found the 19
from the staircase 20 at once. Least gates as a function of the largest j allowed: **7, 7, 7 at 4 points (g-1's proof: 7 for
every coefficient), 19, 19, 19, 19 at 8 points for j <= 0, 1, 2, 3 (walks), 52, 52 at 16 points for j <= 1, 2 (next to
no information: with a tall pool each step of the walker costs seconds to minutes).** Flat. The walks are local and small; at 8 points "flat" is evidence, at 16
points it is nothing. I did not spend more on it, because sections 2 to 4 say what the walk would have to stumble on.

**The pool of the brief, looked at** [ran, `zdz_heights.py`, exact, 8 to 64 points]. The partial sums of the second pass
of Z D Z^T, taken one address bit at a time, are (-2)^(something) times a form on a subcube: 24, 64, 160, 384 wires at
8, 16, 32, 64 points, none of height above 1 once the common factor (up to N/2) is removed. The 12, 32, 80, 192 gates
between them are all of the kind (1, 2): a form minus twice a form inside it. So this pool is the forms pool, the specimen
"gates between wires of height N/2" of w-cross fact C is a circuit of flips, and fact C's sentence should read "height N/2
before scaling". The same sums cut by LEVEL (all T inside S with at most j elements) are tall: the entry at x is the sum
over i <= j of (-2)^i (m choose i) with m = number of common ones of x and S; largest heights by j: 1, 5, 7, 1 (8 points),
1, 7, 17, 15, 1 (16), 1, 9, 31, 49, 31, 1 (32), 1, 11, 49, 111, 129, 63, 1 (64). Those are x-1's digits, which cost more
than the textbook.

## 2. The smallest example, for any matrix at all [ran, exhaustive]

Program `tallmin.c`. A wire is a point of projective space, a gate puts a point on the line through two points held. For a
set of targets of height 1: h1 = least number of helpers when helpers must be forms (exhaustive); then the question whether
h1 - 1 helpers suffice when helpers may be tall. All helpers but the last range over every wire of height at most 3 (4 inputs)
or 2 (5 and 6 inputs); the LAST helper may have any height up to 1000, because it must be the meeting point of a line through
two wires held and a line through a waiting target and a wire held, and that point is computed, not searched. Every set of
m targets among all wires of height 1, one per class. Control: the four rows of H at 4 points come out at 3 helpers, 7
gates, as known.

| inputs | targets | classes | classes where a tall helper saves a gate |
|---|---|---|---|
| 3 | 2 to 10 | 5, 11, 17, ... | 0 |
| 4 | 2, 3 | 15, 82 | 0, 0 |
| 4 | 4 | 467 | **2** |
| 4 | 5, 6, 7 | 2,408; 11,329; 46,180 | 3; 18; 70 |
| 5 | 2, 3 | 31, 359 | 0, 0 |
| 5 | 4 | 5,606 | 19 |
| 4, full sign vectors only | 1 to 8 | 1, 2, 2, 4, 2, 2, 1, 1 | 0 |
| 5, full sign vectors only | 1 to 10 | 1, 2, 3, 8, 11, 18, 19, 25, 19, 18 | 0 |
| 6, full sign vectors only | 2, 3 | 3, 5 | 0 |

All 112 savings replayed by a separate program (`replay.py`: every wire rebuilt as a*u + b*v of two earlier wires in whole
numbers; 112 of 112 "replay OK"). Two gates saved: tested at 4 inputs (4 to 7 targets) and at 5 inputs with 4: never.
With every helper held to height 2 the counts are the same: 2, 3, 18, 70 at 4 inputs (`height_curve_n4.out`) and 19 at
5 inputs (`n5_m4_M2_last2.out`): **against the height cap these small matrices take one step down at height 2 and are
flat after it.**

**The smallest specimen** (4 inputs, 4 targets, `n4_m4_M3.out`, replayed):

    targets  t1 = ( 1, 0,-1,-1)   t2 = ( 0, 1, 0,-1)   t3 = ( 1,-1, 1, 0)   t4 = ( 1, 1, 0, 1)
    h  = x1 - x4            form
    t1 = h - x3
    t2 = x2 - x4
    p  = 2 h - t2           = (2,-1,0,-1)     the tall wire
    t3 = p - t1
    t4 = 3 x1 - p

Six gates; with forms seven (exhaustive). p is a junction of three lines: the line through h and t2 (which makes it), the
line through t1 and t3 (p = t1 + t3) and the line through x1 and t4 (p = 3 x1 - t4). Each of the last two hands over a
target for one gate. The targets satisfy t1 + t3 + t4 = 3 x1.

**The specimen with nothing but ones and twos** (5 inputs, 4 targets, `n5_m4_M2.out` number 6, replayed):

    targets  t1 = x1 - x3 - x4 - x5   t2 = x2 - x3 - x4 - x5   t3 = x1 + x3 - x5   t4 = x2 + x3 - x5
    a  = x3 - x5            form
    d  = 2 x3 + x4          the tall wire: a merge that carries a unit
    t3 = x1 + a             t4 = x2 + a
    t1 = t3 - d             t2 = t4 - d

Six gates; with forms seven. Read it as a grid: two rests (x1, x2) and two tails, a = x3 - x5 and b = -x3 - x4 - x5. The
targets are rest + tail. The tall wire is d = a - b: x5, where the tails agree, cancels; x3, where they are opposite,
doubles; x4, where only b lives, stays. d costs one gate, b would cost two, and b is never made.

Statistics over the 112 [ran, `lines.py`, `replay.py`]: the tall helper is a plain sum or difference of two targets in 110.
The other two are at 5 inputs: in number 5 the tall helper x1 - 2 x5 is the sum of a target and a form helper, twice
(the same cancellation, with a helper in the place of a target); number 14 is a three-line junction with a coefficient 3.
The tallest helper has height 2 in 111 and 3 in one (which also has a circuit with height 2 only); at 4 inputs with 4 to 6 targets every specimen has a gate with a coefficient 3 and at 7 targets all but
2 of 70; at 5 inputs 6 of 19 use only coefficients 1 and 2. So an odd prime is not needed. Zeros are: no specimen consists
of full sign vectors.

## 3. Anatomy, and the growth law of the trick [derived]

**The translation.** Call a tall wire d a *translation* when it is b - a for two needed wires: one gate "T - d" turns every
wire T that ends in a into the wire that ends in b. For forms a and b: d is 0 where they agree, +-2 where they are opposite,
+-1 where only one of them lives. It is tall exactly when a and b overlap with opposite signs AND one of them lives
somewhere the other does not. If a and b have the same support, d is twice a form: the flip, which is not tall.

In words: subtracting d = 2f - c from a wire **extends it onto new points (c) and flips part of it (f) in one gate**.
Forms need two gates for that, or a second tail made in full.

**When it pays.** Tails a = e + f and b = e - f + c (e the shared part, f the flipped part, c the extension; three forms on
disjoint sets), rests R_1..R_q, tails a_1..a_r of this kind with the same e. Needed: all R_i + a_j.
(Take a_1 = e + f and a_j = e - f + c_j for j >= 2, with e, f and the c_j already held.)
- forms, making the tails: 1 gate for a_1, 2 for each other tail, then q r: 2r - 1 + q r.
- forms, putting e into the rests: q gates for R_i + e, r - 1 for the parts c_j - f, then q r: q + r - 1 + q r.
- tall: a_1 (1 gate), r - 1 translations 2f - c_j (one gate each), then q r: r + q r.
Saving: min(2r - 1, q + r - 1) - r = **min(q, r) - 1**. At q = r = 2: one gate (7 against 6, the specimen above). On a q by
q grid: q - 1 gates out of about q^2. [derived; checked by machine only at q = r = 2.]
**The saving lives on one side of a grid whose cost is its area.** A wire d serves a whole row for one gate, but every cell
still costs its own gate. This is the same arithmetic as the hub: a helper is worth (number of lines through it) - 2.

**Why no specimen saves two.** [guess] In every class found the tall wire is one junction; two tall junctions would need two
independent pairs of tails on the same rests, which needs more than 5 inputs or more than 7 targets. Not a law, a size.

## 4. What H lacks [derived], and where a paying tall wire would have to sit

**(a) Zeros.** Every specimen has targets with zero entries, and the tall wire is made of two wires whose supports differ.
The rows of H have no zero. For two full sign vectors u, v: u + v and u - v have entries 0 and +-2 only, so both are twice a
form. The lines through two outputs of H carry, apart from the outputs, only the two half-forms (u + v)/2 and (u - v)/2 and
wires a u + b v with |a| different from |b|, which have full support and two sizes of entry. So the specimens' mechanism,
in the only shape full sign vectors allow, is "wire +- 2 x form", the flip. The best circuits (19 at 8 points: four hubs,
each output one flip from a hub or an output) are made of it.

**(b) The distance of the rows, at any height.** [derived, two lines; it is x-9's lemma A read without the word "form"]
If a wire u is one gate from two outputs y, y' with partners d, d' (u = a y + b d = a' y' + b' d'), then a y - a' y' =
b' d' - b d is a non-zero combination of two rows of H. It is non-zero on at least N/2 points (on all N if |a| is not
|a'|). So **the two partners together cover at least half of the points, whatever the heights of u, d, d'.** A wire one
gate from q outputs has at least q - 1 partners that cover N/4 points or more. Height does not enter: the distance wall
is blind to it. A tall wire can no more have small partners near the outputs than a hub of forms can.
The detail for height 2, which shows where such a wire lives: suppose a tall wire u of height 2 is one gate from an output y with a FORM v as partner.
[ran, `near_output.py`, exhaustive on 4 and 5 points with coefficients up to 8: 2,272 and 7,200 such wires] Then u is, up
to sign, a full sign vector with a set Z of entries set to zero and a set D doubled; that full sign vector is y itself
(6,480 of the 7,200) or the one other full sign vector on the line through y and v (720; then u has no zero at all). My
first list by hand had missed the second case; the machine found it. [derived from that] If u is also one gate from a
second output y' with a form as partner, and u is not on the line through y and y', then both times the full sign vector
is the output itself, y' = +-y wherever u is not zero, so **y and y' differ only inside Z.** Rows of H differ on exactly
N/2 points. So Z contains that half, u lives on the half where y and y' agree, and the partners v, v' cover more than N/2
points each and are mirror images on the half where the outputs differ. (A tall wire ON the line through two outputs is
(3y + y')/2 or (3y - y')/2: full, useless, since that line already holds the two half-forms.) With q outputs through one tall wire: it lives on the points where all q
agree (N/4 for three or four outputs out of one family of four), and each partner covers the rest.
Compare a hub of forms: at 8 points one full sign vector is one flip of a PAIR away from four outputs at once [ran,
`near_output.py`: p = (y_a + y_b + y_c - y_d)/2 for four rows whose labels add up to zero, all 56 choices; the four pairs
are disjoint and cover the 8 points]. So near the outputs a form hub has small partners, a tall wire has large ones. A tall wire does not pay there
unless its partner is tall too ("two hubs, no small partner", x-9's hatch, still open).

**(c) So a paying tall wire sits in the middle**, where needed wires do have zeros. What it needs there, from section 3:
two needed wires a, b with different supports, agreeing on a shared part e, both wanted on top of the same rests, at least
two rests. In a circuit built on the cosets of ONE flag, the supports of any two wires are nested or disjoint, and every
circuit known tonight makes one wire per coset on the way up (the 19: seven merges, one per node of the tree). There is no
grid at all on the way up; the grid is at the outputs (hubs times flips), where everything is full. That is why no walk
found a tall wire at the floor: **the best circuits have no place where two tails with different supports are both needed.**
[ran, `census.py`] The count that shows it. Take all wires of a known circuit (inputs, helpers, outputs) and every sum and
difference of two of them:

| circuit | wires | tall sums or differences | of these, connecting two or more pairs of wires | forms as sums or differences | connecting 1, 2, 3, 4 pairs |
|---|---|---|---|---|---|
| the 19 at 8 points | 27 | 240 | **0** | 385 | 326, 41, 18, 0 |
| the staircase 20 at 8 points | 28 | 296 | **0** | 388 | 340, 28, 16, 4 |
| the 52 at 16 points | 68 | 1,848 | **0** | 2,536 | 2,412, 84, 32, 8 |

In the specimens of section 2 the tall wire connects two pairs (t3 - t1 = t4 - t2). In the three transform circuits no tall
difference occurs twice; every difference that occurs twice or more is a form.
[ran, `census_walks.py`, `census_walks.out`] The same count on every circuit that x-0's walks and mine printed (ledger
samples, some circuits possibly twice):

| points | gates | circuits printed | with a tall difference that connects two or more pairs | most pairs | circuits that hold a tall wire |
|---|---|---|---|---|---|
| 8 | 19 | 22 | **0** | 1 | 0 |
| 8 | 20 | 121 | **74** | 3 | 53 |
| 8 | 21 | 18 | 10 | 2 | 1 |
| 8 | 22 to 26 | 5 | 2 | 2 | 0 |
| 16 | 52 | 6 | **0** | 1 | 0 |
| 16 | 53 | 2 | 1 | 2 | 1 |

[ran, `census_slp.py`, `census_slp.out`] And on the whole (3/4) family of e2-0-pieces, 7, 20, 52, 128, 304 gates at 4 to
64 points (each first checked to hold every row of H): 38; 296; 1,848; 10,240; 52,768 tall sums or differences of two
wires, **not one of them occurring twice, at any size**; forms occur for up to 4 pairs (at 64 points: 432 twice, 192
three times, 32 four times). The family has no grid, and the number of tall differences that fail to repeat grows like
the square of the circuit.

**At the floor there is no grid; one gate above the floor most circuits have one** (a tall wire that is the difference of
two or three pairs of their wires), and in none of them is that tall wire itself in the circuit. This is x-0's "one gate
above the floor everything exists" seen from the side of section 3. The walker's exhaustive move "add one wire, drop two"
includes "add the translation and drop what it replaces", and it never went below 19, so at 8 points these grids are
worth exactly the one gate that the 20 has too many. [derived, sketch] That no tall difference repeats is forced when the
wires with zeros have nested or disjoint supports, one wire per support: "full - tree wire = full' - tree wire'" gives
"twice a form = a difference of two tree wires", which needs two different wires on one support.
Two frames change exactly this: cosets of two different flags cross, and a wire on one, minus a wire on the other, is
"form + 2 x form on disjoint sets" (x-0's dirty wire) on the union minus the part where they agree. x-0's exhaustive search
around the 19's tree kept one tree and found nothing; that is consistent with the above and says nothing about two trees.

**(d) Zeros and signs, both.** [ran, `unate.py`] Of the 112 specimens none consists of full sign vectors, and none can be
turned into a matrix of zeros and ones by changing the signs of inputs and targets. Since the search went through every
class of target sets at its sizes, this says: with 4 inputs and up to 7 targets, or 5 inputs and 4 targets, no tall wire
saves a gate for a zero-one matrix, and none for a set of full sign vectors. [derived] The reason is the same line twice:
the difference of two zero-one vectors is a form, and the sum or difference of two full sign vectors is twice a form. The
tall translation b - a needs a place where a and b are opposite (signs) and a place where only one of them lives (zeros).
In a circuit for the transform both exist only in the middle: the inputs' side is all zeros and few signs, the outputs'
side all signs and no zeros. For the subset sums they exist nowhere, unless a circuit brings in minus signs on purpose.

**(e) What the smallest specimens have and H does not, in one line each.**
- t1 + t3 + t4 = 3 x1: three targets whose sum lives on ONE input. For H a combination of r rows lives on at least N/r
  points (w-cross wall DISTANCE).
- two targets that differ on fewer than half of their points and by more than a flip (x1 + a and x1 + b).
- an odd number of targets whose sum has a zero entry. For full sign vectors a sum of an odd number is odd everywhere.

## 5. The lemma solved for N [derived from x-0 lemma 3 and its table; arithmetic ran]

Lemma (x-0, unreviewed): wires of height at most M give at least N - 1 + ((N/2) log2 N - (N - 1) log2 M) / B(M) gates,
B(M) = log2 of the largest (|a| + |b|)/g, which is 1.585, 3, 4.39, 5.43, 6.19, 7.30 for M = 1, 2, 3, 4, 5, 7.
- A circuit with c gates per point exists only while log2 N <= 2 [(c - 1) B(M) + log2 M]:

| gates per point | forms | height 2 | height 3 | height 4 | height 5 | height 7 |
|---|---|---|---|---|---|---|
| 2.375 (the 19 at 8 points) | 2^4 | 2^10 | 2^15 | 2^18 | 2^21 | 2^25 |
| 3.25 (the 52 at 16 points) | 2^7 | 2^15 | 2^22 | 2^28 | 2^32 | 2^38 |
| 5 | 2^12 | 2^26 | 2^38 | 2^47 | 2^54 | 2^63 |

  (largest N allowed.) So "flat at 16 points" turns into: **if 3.25 gates per point is to be held, the first wire of height 2
  is forced at 256 points, the first of height 3 at 65,536, height 4 at 2^23.** Nobody holds 3.25 per point: the best
  family grows like (3/4) log2 N per point.
- For a rate c N log2 N the lemma needs c >= 1/(2 B(M)): 0.316, 0.167, 0.114, 0.092, 0.081, 0.069 for M = 1, 2, 3, 4, 5, 7.
  **Between 0.316 and the known 0.75 the lemma is silent: forms are allowed by volume, and what is missing is a form
  gate that brings more than one unit and is not paid back** (the 19 has none: twelve gates, one unit each). Side fact 9
  shows such gates exist for a 4 x 4 matrix of determinant 12 (`det12.py`: hub (1,1,-1,-1), three flips of single inputs,
  one merge wire that is itself an output), so they are not forbidden in general.
- The published program (exponent 1 - 8.7625e-4) is below the forms floor only when log2 N exceeds about 10^572 (with
  constant 1). A saving of 0.1 would force tall wires from log2 N of about 100,000 on (x-2's number).
- What the forced wire must look like there, from section 4: not one gate from two outputs with a small partner; a
  translation between two needed wires with different supports, or one of two tall operands of an output gate.

## 6. Mutations

0. **The cheapest test, run tonight (section 4c): no best-count circuit has a grid.** Not the 19, not the 52, not the
   (3/4) family up to 64 points; 74 of the 121 circuits of 20 gates do. Still to run: every other best-count circuit of the night
   (`census.py` takes a helper list), and the 2,748 best 8-point circuits for the subset sums (h-4's list), where by
   section 4(d) no repeat is expected. If one has a tall difference that occurs twice, apply the translation there.
   Otherwise "one wire per support" is a property of everything the night has found, and a search has to leave it on
   purpose (item 1). The (3/4) family at 32 and 64 points is far above the one-unit floor (128 against 111, 304 against
   255): that gap is where a grid could be worth a gate.
1. **Grid hunt in two frames at 8 points (exact, finite).** Fix TWO merge trees whose pairs cross (the second the image of
   the first under an address map). Enumerate the wires d = b - a with a on a coset of the first, b on a coset of the
   second, a and b agreeing on part of the overlap (d is "form + 2 x form"); for each d list the pairs of full sign vectors
   (T, T - d) and (T', T' - d) that are both within two flips of outputs. A d that serves two such pairs is the specimen of
   section 2 inside the transform. Tools: `tallmin.c` for the line arithmetic, `x-0-twojobs/exh8.c` with a second tree in
   place of the free helpers. Outcome either way is small: an 18, or the statement that at 8 points no translation between
   two frames serves two rows.
2. **Two tall operands (x-9's hatch) by the same exhaustive method.** `tallmin` finds the last helper as the meeting point
   of two lines, at any height. Run it on sub-problems of H that fit: the rows of H at 8 points with one or two inputs
   deleted (full sign vectors on 6 and 7 inputs), 4 to 8 of them at a time.
   My runs at 6 inputs stopped at 3 targets (time).
3. **Several translations in one wire.** d = 2f - c does two things in one gate (a flip and an extension). A wire
   c + 2f + 4g applied to a wire of height 2 would do three. This is the pool of the brief read as "a wire that carries j
   translations", and the height it needs grows like 2^j, which is the lemma's N^(1/(4C)) when j grows like log N. The
   question that decides it: in section 3's count a translation saves one gate per ROW. Is there a matrix where one
   translation of j digits saves j gates per row? Search: `tallmin` on 6 inputs, targets with zeros, non-last helpers
   up to height 4, looking for the first class where height 3 or 4 beats height 2 (at 4 inputs there is none).
4. **Turn section 4(b) into a count.** With form partners, a tall wire serves q outputs only from the N/2^(q-1) points
   where they agree. Add up over a whole circuit: how many output gates can have a tall operand at all before the partners'
   cost exceeds the forms count? This would make "tall wires do not pay near the outputs" a lemma with a number, and
   leave exactly the hatch "both operands tall".
5. **The determinant-12 anomaly.** For which sign matrices does a circuit of forms go below n - 1 + log2(det)? At 4 inputs
   one class, with a factor 3 in the determinant. If "never when the determinant is a power of 2" holds at 5 and 6 inputs,
   that is a reason, special to the prime 2, why the 19 is rigid ("clean at the floor", x-0's unexplained regularity).
   `excess.py` does the census from `tallmin`'s output.

## 7. Criticism, last

- Nothing here is about a growth law for the transform. The specimens are 4 x 4 and 4 x 5 matrices with zeros; the transform
  has none, and my own section 4 says the mechanism does not carry over to its outputs.
- "Exhaustive" means: targets of height 1; all helpers but the last of height at most 3 (4 inputs) or 2 (5, 6 inputs); the
  last of any height up to 1000; one saved gate (two saved gates tested at 4 inputs and at 5 inputs with 4 targets). A
  circuit with two helpers of height 4 or more is outside it. The forms count h1 is exhaustive without restriction.
- The search for full sign vectors is small: at 6 inputs only 8 classes (2 and 3 targets); 4 targets did not finish.
  "No saving for full sign vectors" is a regularity on tiny cases with a one-line reason for ONE mechanism (sum or
  difference of two targets), not a theorem. x-0's argument from the published program says it must fail at some size.
- Section 3's count min(q, r) - 1 is by hand, for one family of tails (shared part, flipped part, extension), and compares
  three circuits I thought of; it is machine-checked only at q = r = 2. "Cannot change the order, whatever the matrix"
  is a statement about that family.
- Section 4(b) covers tall wires of height 2 with a form as partner. Height 3 and more, and two tall operands, are not
  covered. The case list is by machine on 4 and 5 points only (my hand list was wrong and the run corrected it); the step
  from the list to "differ only inside Z" is by hand.
- The walks of section 1 are local, short and start from one circuit each; at 16 points they visited almost nothing.
  The one-flag and two-frame pools of the brief were not built as such; I used the larger pool that contains them.
- The 4-inputs program does not search targets of height above 1, so "the smallest example for any matrix" means "for any
  matrix with entries 0, +1, -1". With tall targets the question is empty (the helper can be a scaled target).
- Section 5 inherits x-0's lemma, which is unreviewed.

Files, all in `waves/wave-08/ab-2-tallpool/`:
`tallmin.c` (the exhaustive search; compile with -DNN=3, 4, 5, 6; usage `tallmin m MT MLAST [full] [hcap]`), binaries
`tallmin3` to `tallmin6`; outputs `n4_m2_M3.out` to `n4_m6_M3.out`, `n4_m7_M2.out`, `n4_full_M3.out`, `n4_m4_verbose.out`,
`n5_m23_M2.out`, `n5_m4_M2.out`, `n5_m4_M2_save2.out` (the two-gate test), `n5_m4_M2_last2.out` (every helper of height
at most 2),
`n5_full_M2.out`, `n5_full_M2_m78.out`, `n5_full_M2_m9to16.out` (valid for 9 and 10 targets only: the program holds at most
10 targets), `n6_full_M2.out`, `height_curve_n4.out`; `replay.py`, `replay_lib.py` (exact replay of every saving, gate
kinds, index of the target lattice), `lines.py` (lines through two targets), `excess.py` (the census against the
one-unit floor), `det12.py` (the determinant-12 circuit), `zdz_heights.py` (heights of the wires of Z D Z^T), `near_output.py` (the case list of section 4(b) and the
four-output hub), `unate.py` (no specimen is a zero-one matrix), `census.py` (tall and form differences inside the 19, the 20 and the 52), `census_walks.py`, `census_walks.out` (the
same on every circuit printed by the walks), `census_slp.py`, `census_slp.out` (the same on the (3/4) family to 64 points); the walks `t8_A7.out`, `t8_A15.out`, `t16_A7.out`,
`t16_A7_K6.out`, `t16_A3.out`, `t8_A2_stair.out` (height 2 from the staircase 20). Two jobs were started on the Linux machine (6 inputs with 4 full sign vectors; 5 inputs with every helper of
height at most 2); the machine was loaded, neither finished, I stopped both by process id after 8 minutes and nothing of
mine runs there. Their partial outputs are in `linux/` and are not used.
