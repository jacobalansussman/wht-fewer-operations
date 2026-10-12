# ah-cross: the ten waves side by side, four hybrids tried, and what to ask next

> Editor's note (11 October 2026): the critics of this wave corrected four statements of this report. Subset sums do have a volume, about 0.277 N √(log2 N) ([ai-2](ai-2.md)). The relation lemma is false over the rationals and true in arithmetic modulo 2 ([ai-1](ai-1.md)). "Beyond addresses of about 2^2059 bits" should read 2,060 bits ([ai-0](ai-0.md)). The weight of an operation depends on the letter chosen (ai-2). Also, what it says about published work was recalled and not read again.

11 October 2026, 09:06 to about 09:40 EDT, inside a 40-minute box. Private. One agent; nothing reviewed, nothing in Lean,
nothing published.
Marks: [ran] = run of mine this morning (files in `ah-cross/`, whole numbers or fractions); [derived] = by hand this
morning, checked by nobody; [read] = from the night's reports; [recalled] = from memory, no source read; [guess].
Gate count everywhere: **(G)**, a gate is any a*u + b*v, scalings free. Count (O), OpenAI's, is named where it is used.
Read: ae-cross in full; the first two sections of WAVE9-NOTE; the wall statements of j-cross and k-cross; the top of p-5
and d-0; the ten wave-10 results as handed to me (I opened only `ag-6-deepgates/class_depth.out` and three lines of ag-2).
Wave 10's skeptics had not landed. That is a limit of everything below.

**No circuit below a known count, no growth law below N log N, nothing of the 1e-1 kind. Nothing here changes the order.**

Words. N = 2^k points; an *address* is k bits; *weight* = number of ones; the *overlap* of two addresses = number of
common ones. *The transform* H: entries (-1)^overlap. T(N): least gates for H. *Subset sums* Z: output(T) = sum of the
inputs at the subsets of T; f(N) its least gate count; *Yates*: (N/2) log2 N gates for Z. *The class*: the matrices built
like H from any 2 x 2 block (*kernel*); here the kernel has rows (1, 1), (1, tau), so the k-th power has entries
tau^overlap; H is tau = -1 and Z (after relabelling) is tau = 0. *Class identity*: a circuit whose coefficients are
functions of tau and which computes the power of the kernel for every tau. *Minor*: the determinant of a square piece of
a matrix. *Relation among outputs*: a combination of output rows that is zero; its *length* is the number of rows in it.
*Helper*: a wire several outputs read. *Halving*: a gate that divides by 2.

## 0. In ten lines

1. **Wave 10 answered ae-cross's question: yes, degree 3 falls to N + o(N), and it does not matter.** ag-0 builds it, but
   the saving starts beyond addresses of about 2^2059 bits and the same obstruction returns at degree 4; ag-7 shows that
   from degree about log2 k on the price is at least 2N - o(N). The ladder gives no growth law.
2. **Four reports found one lemma** (section 2, RELATION-LENGTH): ag-0 and ag-7 independently, ag-4's floor, ag-5's
   kernel. The invariant is the length of the shortest relation among the outputs. It is empty at full rank.
3. **Wall DEPTH is not a wall against linear size.** ag-6: the same 19 gates carry 12 to 84 units of depth, depending on
   the kernel. ag-1: a halving weighs nothing. Hybrids 1 and 2 here: for class identities the ledger is a theorem
   (degree in tau), every record meets it, and all of it is paid by ONE diagonal matrix in H = Z D Z^T. The two matrices
   that cost (N/2) log2 N each in every known program, Z and its transpose, have no volume at all: largest minor 1 at
   4 points, 2 at 8 points [ran, exhaustive], against 16 and 4,096 for H.
4. Hybrid 1 [derived + ran at 4 points]: **class ledger.** With wires kept free of common polynomial factors, a gate
   (a u + b v)/c has weight max(deg a, deg b) - deg c, and the weights of a class identity add up to at least
   (N/2) log2 N. Gates of weight at most 1: at least (N/2) log2 N of them. The textbook is tight. A 9-gate circuit with
   one gate of weight 2 has only 3 gates of positive weight where 4 are "needed": the count of deep gates can fall,
   the count of gates did not.
5. Hybrid 2 [ran]: where the volume lives (line 3). So every determinant argument of the night is silent on the question
   "is Z linear", and that question IS the linear question.
6. Hybrid 3 [derived + ran, k = 3, 5]: **one code for the whole class.** The columns of weight below k/2 span the same
   space for every tau. So the half-rate space, its floor, the majority mirror, the ladder, the towers and the helpers
   of wave 10 are facts about the class; none can use tau = -1. The transform is the orthogonal basis of a chain of
   spaces that every member shares.
7. Hybrid 4 [ran]: **the window.** As a polynomial in the overlap, (-1)^overlap needs degree k on all of 0..k but only
   about 5 sqrt(k) on the values that occur for 99 % of the entries: degree 71 of 1,024 at 2^1024 points. The part that
   is left has full rank, and splitting it returns the textbook recursion.
8. Old walls: M/DEPTH derived as a lemma for two classes (unreviewed) and shown harmless for linear size; S/REPAY measured unit for unit in three
   more rooms and still unproved; U/STEP extended (ag-3's J, ag-8's "special means tight"); C unchanged; k-cross's
   "one class" strengthened three ways. None broken.
9. Most surprising: ag-6's free ride of depth. Most informative question: **is the cost of coupling two half-size
   subset-sum transforms ever below one gate per pair, over the rationals with free coefficients?** Section 4.
10. Skeptics first: ag-0's tower (the only claim that beats a known growth, 2N, for a tall matrix); ag-7's private-wire
    lemma; the two ledgers (ag-1's and mine). Section 5.

## 1. Facts that explain each other

**A. ag-0's lemma, ag-7's private-wire lemma, ag-4's floor lemma and ag-5's kernel are one statement.** [read all four]
Each says: a wire shared by several outputs forces a short relation among those outputs; if the outputs have no relation
shorter than delta, sharing is limited. ag-0: all but h + (inputs) outputs are one gate from two non-output wires.
ag-7: the graph of outputs on non-output wires has no cycle shorter than delta - 2. ag-4: gates >= N - n/2 when
delta >= 5. ag-5: every class below N + h - 1 is one designed relation that must lie in a prescribed space.

**B. ag-5's "in gates it changes nothing" and ag-7's floor 2N are the same fact.** [derived] A gate has two operands, so
an output with h helpers costs h - 1 gates. N + o(N) is exactly "two helpers". ag-7 says two helpers stop at degree
about log2 k; three helpers cost 2N by definition. So the ladder reads: 1 gate per point up to degree 3 (ag-0), at least
2 from degree log2 k on, and the open question is whether 2 gates per point (three helpers) carry an unbounded degree.

**C. ag-1's ledger, ag-6's levels, ad-7's census, h-3's ledger in count (O) and p-5's "all of that floor is one
diagonal" are one ledger**, and hybrid 1 gives its exact form for class identities. ag-6's table is the ledger read at
different kernels: per correction gate 1, 3, 4, 5, 6 or 7 units, same gates.

**D. ag-8's "no record is special", ag-6's replay of the 19 for nine kernels, and hybrid 3 say the same thing from three
sides.** The records are class identities (ag-8); their depth is the kernel's (ag-6); and the spaces the wave studied
are the class's (hybrid 3). What only the transform has is that its basis of those spaces is orthogonal, and ag-8 finds
no cheap circuit that uses it (special circuits exist at 16 points and are made of tight wires: 64 gates).

**E. ag-2's products and k-cross's rectangles are the same object.** [my reading] ag-2: a cut with n injections writes Z
as n products (a wire of a circuit for Z transposed) x (a wire of a circuit for Z). k-cross: the transform is a sum of
rectangles over two merge trees, gates = N - 2 + rectangles. Both count rank-one pieces with structured sides. ag-2's
relation rule (a relation of |R| wires hands over a form of L terms) is the first rule for when two rectangles merge.

**F. ag-4's CONJUGATION, ag-2's "line of designs" and ag-8's "the dying gate is repaid by the change of basis" are
k-cross's L1 with exact constants.** ag-4: leaving ANY generator of the half-rate space costs 2 H_(N/2) U. ag-2: from
Yates to "compute Z twice and subtract" every design pays n per cut. [derived, section 4] In one line:
f(2n) = D(n) +- n, where D(n) is the cost of two independent copies of Z on n points. The growth law of subset sums is
a direct-sum question plus or minus one gate per pair.

**G. ag-3's parity and ag-1's "a halving weighs nothing" have the same shape.** [my reading] In both, the invariant that
proves the wall (the sign of a move under J; the determinant) is blind exactly on the step that is left open (an address
map that moves the port; a halving). The open hatches of the night are the places where the proving invariant is zero.

**H. ag-9 closes the constants.** A constant of bounded degree is worth a bounded factor (restriction of scalars); the
class parameter is a free ride (ag-6); so the only constants left are those whose degree or size grows with N, which is
the old open problem and, by hybrid 2, can all be put on one diagonal.

## 2. The walls, each once

**RELATION-LENGTH (new in this wave; four authors).** *Lemma [read: ag-7 section 4, ag-0; unreviewed]. If no relation
among the outputs has fewer than delta terms, the outputs read non-output wires along a graph with no cycle shorter than
delta - 2.* Hit by: ag-0 (lemma, and wall INDEX: one more degree needs atoms indexed by every bit that could tell two of
them apart, a tower); ag-7 (2N - o(N) from degree about log2 k); ag-4 (N - n/2; 3N/4 for the half-rate space); ag-5
(KERNEL-MEASURE-ZERO); before them aa-cross's girth and ae-cross's hybrid 4. For degree d, delta = 2^(d+1).
Status: a floor that is a constant times N, and empty at full rank, where there is no relation at all. It prices the
tall, low-rank pieces of the transform; it cannot see the transform.

**REPAY (j-cross S; k-cross L1, L2).** *At full rank a wire that serves two uses pays, for removing the foreign part,
what the sharing saved.* Wave 10: ag-2 (unit for unit on all 20,880 cuts at 8 points; no bus, no ninth injection, no
triangle for any of the 1,208 upper circuits at 16 points; modulo 2); ag-4 (exact: 2 H_(N/2) U for every generator);
ag-8 (the gate that dies at tau = -1 is repaid by the change of basis); ag-1 (five paper specimens of a halving all tie).
Status of **S**: measured in three more rooms, exact in one more route, still not proved. One regularity unexplained:
ag-2's L = 1 in 13,447,158 cases.

**STEP (j-cross U; k-cross L3).** Wave 10: ag-3 (the count n + 1 extended to every free step that fixes the port; beyond
that only a parity); ag-4 (the majority is constant on no flat of small codimension); ag-8 (a circuit special to the
transform at 16 points is made of tight wires and costs N log2 N). Status of **U**: not broken; its reach is now
"tight wires, or steps that fix the port".

**LEVELS (was DEPTH; j-cross M; k-cross L4).** *Lemma [derived here, hybrid 1; ran at 4 points]. In a class identity the
gate weights add up to at least (N/2) log2 N.* Hit by: ag-1 (the whole-number version: weights log2((|a|+|b|)/c), a
halving weighs 0, flat wires need 0.3155 N log2 N gates besides halvings); ag-6 (the count follows levels, not digits);
ag-9 (bounded-degree constants cannot help); ad-7, h-3, p-5 before them.
Status of **M**: now a derived lemma for two classes, both unreviewed (ag-1's flat wires; class identities with gates
of weight at most 1), and
**removed from the list of obstacles to linear size**: in H = Z D Z^T the diagonal D pays the whole ledger with N free
scalings (N multiplications in count (O)), and Z has nothing to pay (hybrid 2). What the wall still says: a program of
linear size cannot keep its wires flat (ag-1) and, if it is a class identity, needs gates of weight about log2 N.

**LAYERS (j-cross C).** ag-9: among circuits that commute with all translations the kernel needs k steps of N gates.
Unchanged.

**k-cross L5 "one class".** Strengthened three ways: census (ag-8: 0 special among all 8-gate circuits at 4 points),
depth (ag-6), spaces (hybrid 3). Rectangle count: ag-2's relation rule is the first statement about merging rectangles;
no number yet.

**What no wall covers, after ten waves.** (a) Z over the rationals with free coefficients at 16 points and beyond: no
ledger applies, the minimum is settled only to 8 points and only modulo 2, 3, 5, 7 (12; d-0), and ag-2's searches are
modulo 2.
(b) Relations of four or more wires and two or more extra mixed gates (ag-2's "middle of the line"). (c) Two gates per
output (three helpers) at growing degree. (d) A class identity with a SHARED gate of weight 2 or more (ag-6's NO CHOICE
covers only gates that end in an output). (e) ag-3's mixed word (2 paid moves + 2 shears). (f) Constants of growing
degree. (g) Whether two copies cost twice one.

## 3. Four hybrids, each tried

### Hybrid 1. The class ledger (ag-1's ledger x ag-6's levels x ag-8's "every record is of the class")

Idea. ag-1 measures a gate by size and needs flat wires; ag-6 shows depth is a parameter of the kernel. Let the
parameter be a letter: in a class identity the right measure of a gate is its degree in tau.
Lemma [derived]. Keep every wire as a vector of polynomials in tau with no common factor. A gate is then
w = (a u + b v)/c with polynomials a, b, c; call max(deg a, deg b) - deg c its *weight*. Any minor of the matrix of all
wires that uses the new row is (a M_u + b M_v)/c for two old minors, so the largest degree of a minor rises by at most
the weight. It starts at 0. The outputs are the rows tau^overlap, whose determinant is (tau - 1)^((N/2) log2 N).
**So the positive weights add up to at least (N/2) log2 N, and a class identity whose gates have weight at most w has at
least (N/2) log2 N / w gates of positive weight.** Linear size inside the class needs gates of weight about log2 N.
Tried [ran, `h1_ledger.py`, `h1_ledger.out`, 4 points, need = 4; the rule "a minor rises by at most the weight" checked
on every minor of every order after every gate].

| circuit | gates | weights | sum | gates of positive weight |
|---|---|---|---|---|
| textbook | 8 | 0,1,0,1,0,1,0,1 | 4 | 4 |
| ag-6's seven gates, tau a letter | 7 | 0,0,0,1,1,1,2 | 5 | 4 |
| the 8 gates of ae-cross and ag-8 | 8 | 1,1,0,0,1,1,0,1 | 5 | 5 |
| nine gates, mine | 9 | 0,0,0,0,1,1,0,0,2 | 4 | 3 |

- The textbook meets the ledger exactly, at every size [derived: its gates are u + v and u + tau v].
- The 7-gate circuit spends 5: the gate saved is paid by one unit of weight, on a gate of weight 2 that ends in an output.
- The nine gates: a = x0+x1, b = x2+x3, y0 = a+b, c = x1+x3, y1 = y0 + (tau-1)c, y2 = y0 + (tau-1)b, q = y1+y2,
  q' = q - y0, y3 = q' + (tau-1)^2 x3. Three gates of positive weight where every circuit with weights at most 1 has
  four. A deep gate lowers the number of deep gates, not the number of gates: the two weight-free gates q, q' pay for it.
- 8 points [read: the gate kinds in ag-6's `class_depth.out`, which fit polynomials in t at all nine values; arithmetic
  mine]: for the kernel (1, t; t, 1), where the need is N log2 N = 24, the 19 gates have weights 1 (nine gates), 2 (eight)
  and 3 (two): 31 in all. Five gates saved against the textbook, seven units overspent.
What it gives: wall LEVELS as a lemma, valid for every class identity whatever its coefficients; "exactly (N/2) log2 N
gates u +- 2v" (ad-7) becomes "at least", and the reason. Where it stops: it is a necessary condition only, and
hybrid 2 shows it can be met for nothing. It says nothing about circuits that are not class identities (none is known
below the textbook, ag-8). I did not search for the least gate count under a weight limit.

### Hybrid 2. Where the volume lives (g-4's H = Z D Z^T x every ledger of the night x p-5's quasi-entropy)

Idea. Every determinant argument (ag-1, ag-6, ad-7, h-3, hybrid 1) charges the transform for its determinant. In
H = Z D Z^T the determinant is all in D. Ask how much volume the other two factors have.
Tried [ran, `h2_minor.py`, `h2_minor_long.py`, outputs `h2_minor*.out`, whole numbers].

| points | largest minor of Z | how | determinant of H |
|---|---|---|---|
| 4 | 1 | all minors | 16 |
| 8 | 2 | all 12,869 minors, every order | 4,096 |
| 16 | at least 5 | hill climbing, exact determinants, NOT a maximum | 2^32 |
| 32 | at least 16 | the same | 2^80 |

(The 32-point output file is headed "k=4" by a slip in the label; it is the run with argument 5.)
[derived] A minor made as a product of minors of the two halves has order (order_1 x order_2), so product minors of
less than full order give at most N^c log N units with c < 1, and at full order the determinant is 1. [read: p-5] The
quasi-entropy, the other meter of the night, is exactly 0 for Z.
What it gives. **The ledger is paid in full by N scalings, free in count (G) and N multiplications in count (O).** So:
T(N) <= 2 f(N) + N, f(N) <= 3 T(N) + O(N) (g-4), and for Z no volume count forbids even a circuit of O(N) additions and
subtractions with coefficients +1 and -1. [recalled, no source read] Yates is known to be best only when subtraction is
not allowed. Walls M, DEPTH and LEVELS therefore say nothing about linear size; what stands between the night and
O(N) is REPAY alone, on Z, and REPAY is measured, not proved, modulo 2, to 16 points.
Where it stops: a relocation, not a circuit. The 16- and 32-point numbers are lower bounds on the largest minor from a
search without a control; a large minor of an unusual shape is not excluded.

### Hybrid 3. One code for the whole class (ag-4's half-rate space x ag-8's class x ae-cross's "a digit is a degree")

Idea. ag-4 priced the space spanned by the transform's low columns. Is that space the transform's, or the class's?
[derived, two lines] Column x of the k-th power of the kernel is the function y -> tau^overlap = product over the ones
i of x of (1 + (tau - 1) y_i): a polynomial of degree weight(x) in the bits of y with leading coefficient
(tau - 1)^weight(x). So for every tau other than 1 the columns of weight at most d span exactly the polynomials of
degree at most d.
Tried [ran, `h3_onecode.py`, `h3_onecode.out`, fractions, k = 3 and 5, tau = -1, 3, 5/7, -2, 2]: the low columns have
rank N/2, together with the transform's low columns still N/2 (the same space), and rank N/2 on the even-weight points
(ag-4's information set) in all ten cases.
What it gives.
- Everything wave 10 learned about spaces is a fact about the class: ag-4's floor and mirror M, ag-7's dial, ag-0's
  towers, ag-5's kernels. None of it can use tau = -1, so none of it can separate the transform from members such as
  Z (tau = 0) or p-5's kernel (tau = 2).
- "A binary digit is a degree" (ae-cross) holds for every member: the power of the kernel is the sum over j of
  (tau - 1)^j E_j with the SAME E_j. A level is a degree; the digit is whatever tau - 1 is. That is ag-6's LEVELS.
- The transform is the member whose columns are orthogonal: it is the orthogonal basis of a chain of spaces
  (degree at most 0, 1, ..., k) that all members share. ag-8 says no circuit below the textbook uses that.
Where it stops: it explains why ten waves found nothing special; it does not find anything.

### Hybrid 4. The window (ae-cross's digits x ag-7's dial x where the mass is x the literature on non-rigidity)

Idea. ae-cross expands (-1)^m, m = overlap, around m = 0 and needs every degree up to k. But m is concentrated: for
two random addresses it is near k/4 within a few sqrt(k). Interpolate (-1)^m on a window of values only.
Tried [ran, `h4_window.py`, `h4_window.out`, exact counts].

| k | window covering all but 10 % of the entries | all but 1 % | all but 1e-6 |
|---|---|---|---|
| 64 | degree 11 | 17 | 32 |
| 256 | 22 | 35 | 67 |
| 1,024 | 45 | 71 | 135 |
| 4,096 | 91 | 142 | 270 |

At 2^1024 points a polynomial of degree 71 in the overlap equals the transform on 99 % of its entries and has rank at
most 2^368 of 2^1024. Exact check at 64 points: the polynomial through m = 0..3 differs from the transform on 154 of
4,096 entries and has rank 42, the bound.
[derived, from the ladder's known price of at most d - 1 gates per point (ag-5) and the transposition rule] The
polynomial part costs O(N sqrt(log N)) gates. [recalled, not re-read] This is the mechanism behind the published
statement that the transform is not rigid (Alman and Williams, 2017).
Where it stops. The part that is left (a function of the overlap that lives on the two tails) has full rank, because H
is invertible and the polynomial part has small rank; every output is wrong by its tail. Splitting the address in two
and using the window on each half gives four products whose costs add up to the textbook recursion T(N) = 2 sqrt(N)
T(sqrt N) [derived]: REPAY again. One question survives: the cost of the tail matrix alone, which nobody has priced.

## 4. The most surprising thing, and the question that would tell the most

**Surprise of this wave.** ag-6: the 19-gate wiring computes the third power of the kernel (1, t; t, 1) for nine values
of t with the same gates, and its twelve correction gates carry 3, 4, 5, 6 or 7 units of depth each. For nine waves
"depth" was one of the three walls. It is a parameter. With hybrid 2 the consequence is plain: the determinant, the
digits, the halvings and the large coefficients all concern one diagonal matrix, and a diagonal matrix is free.
(Runner-up: ag-0's degree 3, true and useless below 2^2059 address bits.)

**Question. Is the cost of coupling two half-size subset-sum transforms ever below one gate per pair, over the
rationals with free coefficients?**
Why this one. (i) [derived] Z on 2n points is (Z a, Z a + Z b). Hence f(2n) <= D(n) + n and D(n) <= f(2n) + n, with
D(n) the cost of two independent copies. Write e(n) = (f(2n) - 2 f(n)) / 2n, the coupling cost per point. Linear size
for Z, hence for H, needs the sum of e over all doublings to be finite. Yates has e = 1/2 at every step.
(ii) [read: d-0] the least counts found are 0, 1, 4, 12 at 1, 2, 4, 8 points: e = 1/2, 1/2, 1/2. At 8 points 11 is
excluded by exhaustion over the fields with 2, 3, 5 and 7 elements, which is not yet a proof over the rationals. The
first open value is at 16 points (32 or 31). (iii) By hybrids 1 to 3 no ledger and no fact about spaces bears on it; by ag-2 it is
exactly "does the gain per relation, L / |R|, grow with n" (2 at 16 points on paper, for buses and for triangles).
(iv) It splits into two questions that have never been separated: is D(n) below 2 f(n) (do copies share), and is the
+ n avoidable.
Experiment. (a) Exact: least gates for two independent copies of Z on 4 points (8 inputs; is 7 possible?) and of H on
4 points (is 13 possible?) with `d-0-zeta/mincirc` over the two-, three- and five-element fields. (b) Z at 16 points
with ALL coefficients: ag-9's annealer `fpgame.c` pointed at Z modulo several primes, control = it finds 12 at 8 points
and 32 at 16; any 31 is lifted and replayed in fractions. (c) ag-2's paper ratio L / |R| at 32 points with Yates on 16
above, for buses, triangles and relations of four wires, modulo 2 and with rational dependencies. Output: e(8), D(4),
and one number, the largest L / |R| at 32 points.

## 5. Three objects for a skeptic, in this order

Nothing in wave 10 claims a circuit for the transform below a known count.

1. **ag-0's tower of lamps** (`ag-0-ladderdegree3/designs.py`, report sections on rule D and on the helpers). It is the
   only claim of the wave that beats a known growth: polynomials of degree 3 at all N cube points in N + o(N) gates
   against 2N. Claims exactly: rule D is sufficient; the tower with L colours and atoms of s bits obeys it with
   N (1/L + 2^-s) classes; the two helpers are again of low degree, so gates <= N (1 + 3/L + 2/2^s) + o(N). Built once:
   3 colours, 8,192 points, 7,168 classes. Attack: the helper claim (run at three toy sizes only); whether the count
   includes computing the atoms; the size 2^2059; and "via ae-cross's dictionary that is the transform modulo 16 in
   2N + o(N)": the wave-9 critic (af-0) corrected that dictionary's figure by N, and the correction may apply here.
2. **ag-7's private-wire lemma and the floor 2N - o(N)** (ag-7.md section 4; `ag-7-rankdial/private.py`,
   `lemma_ad6.py`). Claims: over the two-element field, with shortest relation delta > 4, no gate adds two outputs and
   the graph has no cycle shorter than delta - 2; hence at most (1/2)(1 + N^(1/(2^d - 2))) outputs per non-output wire.
   Section 2 above rests four reports on it. Attack: the step from the graph to the gate count, which no check tests;
   the recalled graph theorem; the passage to the rationals ("a rougher argument whose constant I did not work out").
3. **The two ledgers**: ag-1's (`ag-1-halvingornothing/flatgates.py`, `ledger_check.py`; claims a halving weighs 0 and
   flat wires need 0.3155 N log2 N gates besides halvings) and mine (hybrid 1). They are the same argument. Attack: the
   normalisation of wires (whole numbers with no common factor there, polynomials with no common factor here) and
   whether a gate of negative weight can be used to cheat the count; in mine, that I checked four circuits at 4 points
   and read the 8-point weights off another agent's table.
Also: ag-5's 29 classes at 32 points beat the two-helper count 30, in classes not gates (`best_k5_d3_29classes.txt`);
ag-8's lemma that the mixed 16-point network is special is by hand and its machine test covered 65 % of the renamings;
ag-4's floor lemma is eight lines. Mine: hybrid 2's numbers at 16 and 32 points are lower bounds from an uncontrolled
search; "REPAY alone stands between the night and O(N)" is a reading, not a theorem.

## 6. Eight experiments for the next wave

Deepen what is alive:

1. **relation-ratio** (deepens ag-2; part (c) of section 4). 32 points, Yates on 16 above: for buses, triangles and
   relations of four or more wires list the largest L / |R| a relation could hand over, and at 16 points open the middle
   of ag-2's line (two or more extra mixed gates). Inputs: `ag-2-firstbusthatpays/` (decoA.c, decoB.c, decoC.c,
   rule8.py). Output: the ratio as a function of n (it is 2 at 16 points). If it does not grow, the relation rule gives
   REPAY as a theorem for cuts; if it grows, the first size where a relation could pay.
2. **two-gates-per-output** (deepens ag-0, ag-5, ag-7; fact B). ag-7: at least 2 gates per point from degree log2 k on.
   Three helpers cost exactly 2. Does a third helper carry more than one extra degree with o(N) classes? Start from
   ag-0's bad triple at degree 4 (three atoms) and ag-5's kernel-first tool; test designs exactly with ag-0's walk at
   2^11 to 2^13 points. Output: the largest degree reached at 2N + o(N), and whether it grows with k. A bounded number
   of gates per point at unbounded degree would be the first growth law of the ladder.
3. **dying-gates** (deepens ag-8; uses hybrid 1). Carry tau as a letter through every record and every annealer output
   at 8 and 16 points (ag-8's `wsolve.py`, h-6's tools). For each circuit: the weights of hybrid 1, the gates whose
   coefficient vanishes at tau = -1 (the transform) and at tau = 0 (subset sums), and what is left of the circuit there.
   Output: a table, and whether any family loses a fixed fraction of its gates at tau = -1.

Nobody has tried:

4. **direct-sum-exact** (part (a) of section 4). Least gates for two independent copies of Z on 4 and on 8 points and of
   H on 4 points, exhaustive modulo 2, 3, 5 with `d-0-zeta/mincirc`. Output: D(4), D(8) against 8 and 24, and 13 or 14
   for H. One copy shared across two problems at any size is the first failure of k-cross's L2 in count (G).
5. **subset-sums-with-every-coefficient** (hybrid 2; part (b) of section 4). Nothing forbids large or fractional
   coefficients in a circuit for Z, and nobody has searched for one: d-0 is exhaustive to 8 points, ag-2 is modulo 2.
   Point ag-9's `fpgame.c` at Z at 16 points modulo 3, 5, 7, 13, 31 with all coefficients, with the two controls of
   section 4. Also finish hybrid 2's table: the true largest minor of Z at 16 points (branch and bound by order).
6. **weight-against-gates** (hybrid 1). Exhaustive at 4 points with tau a letter and coefficients from the products of
   1, tau, tau - 1 up to degree 3: the least number of gates when every weight is at most 1, at most 2, at most 3, and
   the least number of positive-weight gates at 7, 8, 9 gates. Then the same weights for the 19 and 20 at 8 points in
   the kernel (1, 1; 1, tau). Statement to prove or refute: a class identity with weights at most 1 needs N log2 N
   gates, i.e. the textbook is best there and every gate saved costs a unit of weight.

One hybrid:

7. **deform-from-Z** (ag-8's class curves x d-0's minimum circuits x hybrids 2 and 3). Z is the member tau = 0 and has
   no volume; the transform is tau = -1. Take d-0's minimum circuits for Z at 8 points (12 gates) and compute, by linear
   algebra on the tangent at tau = 0, the fewest gates that must be added for the circuit to become a class identity.
   The differences known are 3 and 7 (7 - 4, 19 - 12), that is N - 1. Output: is T_class(N) = f(N) + N - 1 at 16
   points (47 against the record 52), and is there an additive law T <= f + O(N) in place of T <= 2f + N.

One that sounds silly:

8. **tau-is-a-shift.** Put a cyclic shift of k + 1 slots in place of tau. A class identity then computes, for every
   output address, the sums of the inputs sorted by overlap: every kernel of the class at once, k + 1 times more than
   was asked, with multiplication by tau a relabelling and every remaining coefficient +1 or -1. In that form a class
   identity is a circuit of additions, subtractions and shifts, where counting arguments of the kind that prove Yates
   best without subtraction have a chance. Try: 4 and 8 points, least number of additions for the sorted sums
   (exhaustive at 4), and whether the bound of hybrid 1 can be raised from "(N/2) log2 N / w" to "c N log2 N for every
   class identity". A yes would prove that no class identity is linear, and say that a linear program must use
   orthogonality.

Held over, not chosen: ag-3's mixed word (2 paid moves + 2 shears). It is the engine's one open integer, and its author
shows that even a yes stays below 1e-1.

## 7. Criticism, last

- I read wave 10 through its result summaries. "One lemma, four authors" matches statements, not proofs.
- Hybrid 1 is Morgenstern's argument with degree in place of size. It may be known. It is five lines, an hour old, and
  checked on four circuits at 4 points. Its normalisation is a choice; another choice gives another true inequality.
- Hybrid 2 says where an argument does not apply. p-5 had the same thought for the kernel (1, 1; 1, 2) ("all of that
  floor is one diagonal"); what I add is the table of minors of Z and the sentence about linear size. That Z and H are
  equivalent within a constant was known since wave 3.
- Hybrid 3 is two lines of algebra. Its value is as a filter: it tells which of the wave's results cannot bear on the
  transform as opposed to its class.
- Hybrid 4 is an approximation, and the night's subject is exact. I include it for its one number (sqrt(log N) for
  99 % of the entries) and because the tail matrix has not been priced. I did not re-read the paper I cite.
- The key question is the oldest one in new words: it is REPAY on Z. What is new is only that the other walls have been
  cleared away from it and that it has a smallest undecided instance in each of two halves (D(4); f(16) with free
  coefficients).
- I found nothing that speaks for linear size, and nothing that speaks against it beyond measurements modulo 2 at 16
  points and below.
- Nothing here changes the order, or any constant.

Files: `waves/wave-10/ah-cross/` : h1_ledger.py, h1_ledger.out (hybrid 1);
h2_minor.py, h2_minor.out, h2_minor_long.py, h2_minor_k4.out, h2_minor_k5.out (hybrid 2); h3_onecode.py, h3_onecode.out
(hybrid 3); h4_window.py, h4_window.out (hybrid 4).
