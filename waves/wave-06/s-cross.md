# s-cross: the six waves side by side, four hybrids tried, and what to ask next

> Editor's note (11 October 2026): later reports corrected two statements of this report. That a reflection "brings 4 calls down to 2" also holds for every 2 by 2 rotation, and, as this report says itself, it is not a saving: 12 operations against 8 ([v-2](v-2.md)). And the circuit equal to the transform up to multiples of 4 does not use "a fact special to the prime 2": it works for the whole class ([x-1](../wave-07/x-1.md)).

11 October 2026, 02:47 to about 03:27 EDT, 40-minute box. Private. One agent; nothing reviewed, nothing in Lean, nothing published.
Marks: [ran] = run of mine tonight (files in `s-cross/`; whole numbers unless a line says "floats"); [derived] = by hand tonight,
checked by nobody; [read] = from tonight's reports; [guess].
Gate count everywhere: **(G)**, a gate is any a*u + b*v, scalings free. Count (O), OpenAI's, is not used in this report.
Read: m-cross and q-cross in full; the ten wave-6 results as handed to me (their reports not in full); one passage of u-8 and of
g-4. I did not read the skeptics' reports (a-, b-, c-, n-, r-) nor the wave notes. That is a limit of everything below.

**No circuit below a known count, and no growth law below N log N. Nothing here changes the order.**

Words. N = 2^k points; an *address* is k bits. *The transform*: the Walsh-Hadamard matrix H, entries +1 and -1. *Textbook*:
N log2 N gates. *Subset sums*: y_S = sum of x_T over the T inside S; matrix Z. *Yates*: the usual method for Z, (N/2) log2 N
gates. H = Z D Z^T with D a diagonal of powers of -2 (g-4), so Z in O(N) gates would give H in O(N) gates. *Two chains*: running
sums of the inputs in one order, each output = its neighbour plus or minus a few running sums; the *corners* count those terms
(q-cross). *Letter*: the same with a merge tree on each side instead of a chain. *Wire*: a value the program holds, a vector over
the inputs. *Primitive form* of a wire: the wire scaled to whole numbers with no common factor (scaling is free in count G).
*Sign vector*: entries +1, -1 on a set of addresses, 0 elsewhere. *Flag*: a chain of subspaces of the addresses, each of twice the
size of the one before; its cosets are the nodes of a merge tree. *Volume budget* (new here, section 3 hybrid 3): write every gate
between primitive forms as w = (a u + b v) / g with a, b whole numbers without common factor and g the common factor of the
result; the gate's budget is log2((|a| + |b|) / g).

## 0. In ten lines

1. **Wave 5's door is closed, four times, by one lemma.** u-0, u-1, u-2 and u-6 each proved by hand, within the same hour and
   without reading each other, that the two-chain program for subset sums is not linear and not even N log N in the long run
   (exponents 1.10 and 1.32). Section 2, L1. None of the four proofs has been read by a second person.
2. [read: g-4 section 6.3; q-cross quoted the bound as "below N for every size one could run" and did not draw this
   conclusion] **For LINEAR size that door was already shut in wave 3.** Every model
   wave 6 tried for subset sums (two chains, letters, trees, several chains) uses gates u + v and u - v (a two-chain picture also u + 2v at a checkerboard), and g-4's
   volume count gives at least N (0.277 sqrt(k) - 1) gates for any circuit of gates u + v, u - v, and 1.585 times fewer with u + 2v. What wave 6 adds is the much stronger "not below Yates".
3. **u-8 and u-9 proved the same theorem independently**: a circuit whose wires are sign vectors on the cosets of one flag has at
   least N - 1 + (N/2) log2 N gates. m-cross's guess is now a theorem in its class, twice derived, never reviewed. Section 2, L2.
4. [ran, hybrid 3] **Every record circuit has exactly (N/2) log2 N gates with coefficient 2, no larger coefficient, and no
   quotient gate**: 4, 12, 32, 192 at 4, 8, 16, 64 points. The determinant of H needs a budget of (N/2) log2 N; the records
   spend 1 unit on each join (N - 1 of them in the brick and the 19, more in the staircase), which bring no volume, and 1.585
   on each coefficient-2 gate, which brings exactly 1.
   Linear size, C N gates, needs an average budget of (log2 N)/(2C) per gate: coefficients that grow like a power of N.
5. [ran exact, hybrid 1] **u-7's rank-35 block, g-7's third turn and p-0's sixth roots of unity are one fact.** With D the diagonal
   of signs of a quadratic form Q, (D H)^3 = N^(3/2) x identity. The fixed space of that order-3 map has dimension (N + 2)/3 and
   a basis of vectors that each live on one side of the quadric (35 on Q = 1 and 51 on Q = 0 at 256 points); on the rest, H couples two
   spaces of dimension (N - 1)/3 at an angle of 60 degrees. An explanation, not a circuit.
6. [derived, hybrid 2] **A sealed box is never shared.** A fixed linear program that reaches (A x A) on a K x K table only through
   calls to A, and is right for every A, makes at least 2K calls: the textbook's rows and columns. So any composition law with
   fewer inner calls than directions (u-5's a < m) must use a property of the transform itself. [ran] At K = 2 the property
   "reflection" (A^2 = 1 and A symmetric) brings 4 calls down to 2; "A^2 = 1" alone did not. Not a saving: the glue is the box.
7. Status of the old walls: section 2. j-cross U proved in a class; M turned into a ledger; S proved for sealed boxes; C untouched.
8. Most surprising: both objects of wave 6 that get under a floor do it one binary digit down (u-9's 3.2 N circuit congruent to
   H modulo 4; u-5: in the published unit every wanted term sits exactly one digit under an odd mixture). Section 4.
9. Most informative question: **can one gate do two jobs, join inputs and carry volume?** Section 4.
10. Skeptics first: the common floor of u-8 and u-9, then the four proofs behind L1, then the box lemma of this report.

## 1. Facts that explain each other

**A. Four reports, one count.** [read; the match is mine] u-0's block lemma, u-1's window lemma, u-2's nested runs and u-6's
three lemmas all count the same thing: a run of L consecutive inputs that lies inside "the inputs below S" forces S to contain
the union of those inputs, a set of at least log2 L elements, so a long run serves only the few outputs just above its union,
and one line through the cube has only N runs of each length. u-3's section 6 has it again for the chain as an input tree.
Stated once as L1.

**B. Two reports, one theorem.** [read] u-8 ("one gate, one half-restriction": the N rows have only N/2 distinct pairs of
halves, a gate changes one half) and u-9 (the recursion t(k) >= 2 t(k-1) + N/2 + 1 on the cosets of one flag, quotient gates
allowed) reach N - 1 + (N/2) log2 N for the same class by what look like the same count. u-8 metered 24 circuits inside the
class, u-9 31 of 54. Neither read the other. Stated once as L2. Consequence both draw: 7 and 19 are optimal in the class, 16
points lies between 47 and 52, the rate there is at least 1/2.

**C. Three counts that land on (N/2) log2 N to the gate.** [read] u-3: subset sums as a letter on free trees costs 4, 12, 32
gates at 4, 8, 16 points, Yates' number exactly, and 81 at 32 points. u-9: H modulo 4 in two chains or any spanning model costs
exactly (N/2) log2 N odd cells. u-4: the transform as Z D Z^T with Yates in both passes costs exactly N log2 N. With m-cross's
"one number, five reports" that is eight. [derived] They are not one cause. For H the number is the volume (line 4 of section 0).
For Z the determinant is 1 and volume gives only N sqrt(log N); there the number comes from "one family per side" (L3).

**D. The volume door has three names.** [derived + ran, hybrid 3] j-cross's wall M says bounded coefficients cost N log N.
In the primitive scaling the same count is a budget, and three things of the night are that budget seen from different sides:
(i) the diagonal D of H = Z D Z^T, powers of 2 up to N, supplies all of it for free: the only circuits of the night whose
coefficients grow are the Z D Z^T ones (coefficient 16 at 32 points, `pmeter.out`); (ii) a quotient gate, m-cross's Q, has g > 1
and LOWERS the budget, so a program that divides must have multiplied by more somewhere else; (iii) u-5's "2-adic depth adds
under nesting" is the growth of coefficients the budget asks for: d nested units put the answer d digits down, a ratio 2^d.
[derived] The published program beats N log N, so by this count its coefficient ratios must grow with N; u-5 measured order 1
inside one invocation, so the growth can only come from the nesting.

**E. Two requirements for linear size, side by side.** [derived from g-4's bound and hybrid 3] For H directly: average budget
(log2 N)/(2C) per gate. For subset sums: 0.277 sqrt(log2 N)/C per gate, the rest coming free from D. The Z route asks for far
less coefficient growth than the direct route. It still asks for some, which no model of waves 5 and 6 had.

**F. The third turn.** Hybrid 1. u-7's quadric block (wave 6), g-7's third turn and u-7's (H S)^3 identity over the Gaussian
integers (waves 3 and 6), and q-cross's remark that p-0's special values are the cross-ratios 2, 1/2 and the sixth roots of
unity (wave 5): the transform times a diagonal of signs is a rotation of order 3, and 60 degrees is its angle.

**G. u-4's hub circuits say what a join can do.** [ran, hybrid 3] In the records the N - 1 joins bring no volume. In u-4's
`hubparity8.txt` (26 gates) there are 19 gates of the kind u + v and only 7 with coefficient 2 for a budget need of 12: 5 units
of volume are carried by joins (hybrid 3, reading iii). So "a join carries no volume" is a property of the one-flag class, not of
circuits; it is the hypothesis L2 uses and the one to break.

**H. u-5's recursion and the box.** [read + derived] u-5: cost per point obeys c(mF) = a c(F) + b for a unit with a inner
moves per array over m directions; the textbook has a = m, the published unit a = 44.905 for m = 45, a = 1 would give
N log log N. Hybrid 2's lemma says a = m is forced as long as the inner transform is used as a sealed box; u-8's exact
composition law says the same inside the one-flag class (cross term >= 0). Both stop at "a partner on a crossing support".

## 2. The walls, each once

**L1. One line through the cube.** *In a two-chain program for subset sums, a step between outputs whose larger set has s
elements must switch about 2^(s-1) inputs, all inside that set; as r runs of one order of the inputs, one of them has length
2^(s-1)/r and so sits inside only the sets just above its union; there are N windows of each length. Supply against demand
forces r to grow like a power of N for most steps.* Who hit it: u-0 (block lemma; corners per point at least 2^(c k / log k)),
u-1 (window lemma; N^1.10), u-2 (nested runs; (5/2)^k / O(k), and one run per step impossible from 16 points on a path, 32 on
a tree, exhaustive), u-6 (any number of chains up to a power of k, any output tree), u-3 section 6 (chain as input tree).
Status: four hand proofs, each with numerical checks of its inequalities, none read by a second person; the exponents differ
(1.10, 1.32) and nobody compared the proofs. Not covered: signs and weights on both sides, helper wires that are not outputs,
tables of running sums in two or more dimensions, several letters with a free order in the middle.

**L2. One flag.** *A circuit for H whose wires are all sign vectors on the cosets of one flag has at least N - 1 +
(N/2) log2 N gates, quotient gates allowed.* Who hit it: u-8, u-9 (proofs); m-cross (as a guess, on 18 files); h-6 (as
"15 + 32" for one-centre programs); u-6 from the side (a second tree with agreement gains nothing and sits inside the volume
wall); u-7 (a quotient used as a partner obeys the product law of a tight wire: at most N/|D| outputs). Status: two hand
proofs, unreviewed; exhaustive only at 2 and 4 points. Hypotheses, which are the hatches: sign vectors (u-9's wires that carry
a 2 outside their set already give 3.2 N modulo 4); one flag (a support that crosses the flag, an address map inside the
program, the published unit's shape); affine sets.

**L3. One family per side.** *A letter gives each output as ONE earlier output plus nodes of ONE nested-or-disjoint family.*
For H this is q-cross's W-A (quadratic). For Z it is u-3's level lemma (at most about k rows of each size are one node from
another row) and the measured tie with Yates; for H modulo 4 it is u-9's crossing lemma. Status: for Z, exhaustive modulo 3
at 8 points, annealers at 16 and 32; no proof that a letter cannot go below Yates.

**L4. Volume (j-cross M, i-cross W4, q-cross W-D).** Not broken. Sharpened into a ledger (hybrid 3) and extended to Z by
g-4's minors. Its door has a size now (fact E). u-6 placed "two trees" inside it.

**L5. Sealed box (j-cross S).** Proved for sealed boxes by hybrid 2's lemma [derived tonight, unreviewed]; exact inside the
one-flag class by u-8's composition law. Open exactly where the box has relations of its own.

**The older walls, status.** j-cross **U** (tight wires): proved with its constant inside the one-flag class (L2); extended to
quotients by u-7's partner bound; broken as a general law only by the published unit, as m-cross said. j-cross **M**: L4.
j-cross **C** (commuting steps): not touched by wave 6. j-cross **S**: L5. k-cross "every saving so far is an identity of the
whole class": not re-tested in wave 6; u-9's modulo-4 circuit uses a fact special to the prime 2 (for odd numbers, multiplying
is adding modulo 4), so it is a candidate for the first object that is NOT an identity of the class [guess, not run].
k-cross's rectangle count and q-cross's W-A: unchanged. q-cross's "no wall covers the corner count": answered by L1, and for
linear size it was covered by L4 all along (line 2 of section 0). m-cross's three hypotheses: u-5 answered which one the unit
breaks first (one tree, at 2 % of the program); u-4 showed a circuit can leave "one tree" for free and gain nothing.

## 3. Four hybrids, each tried

### Hybrid 1. The quadric block is the third turn (u-7's rank 35 x g-7's third turn x p-0's sixth roots x "the wire flat on both sides")

Idea. u-7 found that the block of the 256-point transform on the 120 addresses with Q = 1 is 8 I - 24 P with P of rank 35, and
asked what it is. Nobody looked at the other block, the block between them, or asked why.
Tried [ran, `quadric.py` on the Linux machine, `quadric.out`; the identity "product of (M - eigenvalue) = 0" is checked in whole
numbers, the multiplicities then follow from the trace; `r3.py`, `r3.out`, pure whole numbers]. Take Q = x1 x2 + x3 x4 + ... on
2n bits and write the transform with the pairing that belongs to Q (the plain transform with the two bits of each pair exchanged
in the output address: a relabelling, free). Split the addresses into Q = 0 and Q = 1. u-7's numbers (trace 120, the equation
M^2 + 8M - 128 = 0) are those of this pairing; with the plain pairing the same block has four eigenvalues [ran, `quadric.out`].

| points | block Q = 1 | block Q = 0 | block between |
|---|---|---|---|
| 16 | 6 points: -4 once, +2 five times | 10 points: +4 five times, -2 five times | rank 5 |
| 64 | 28 points: -8 seven times, +4 twenty-one times | 36 points: +8 fifteen times, -4 twenty-one times | rank 21 |
| 256 | 120 points: -16 thirty-five times, +8 eighty-five times | 136 points: +16 fifty-one times, -8 eighty-five times | rank 85 |

So [ran]: (N + 2)/3 independent eigenvectors of the transform live entirely on one side of the quadric (1 + 5, 7 + 15, 35 + 51), and on what
remains the transform is sqrt(N) times [[-1/2, (sqrt 3 / 2) U], [(sqrt 3 / 2) U^T, +1/2]]: two spaces of dimension (N - 1)/3
(5, 21, 85) coupled at 60 degrees.
Why [ran for N = 4, 16, 64; derived for the rest]: with D the diagonal of the signs (-1)^Q, (D H)^3 = N^(3/2) x identity
(8, 64, 512 times the identity, exact) and the trace of D H is sqrt N. So R = D H / sqrt N has order 3, fixed space of dimension
(N + 2)/3, and each of the two other eigenvalues (N - 1)/3 times. If R v = v then R (D v) = D v, so the fixed space splits into
vectors with D v = v (on Q = 0, eigenvalue +sqrt N of H) and D v = -v (on Q = 1, eigenvalue -sqrt N): the table.
What it gives: an explanation of three anomalies (fact F), and the fixed space has a basis of vectors that are zero on half of
the points. [derived] The indicator of a subspace of sqrt N addresses on which Q vanishes is one of them: a tight wire that is
an eigenvector. What it does not give: a circuit. The projection onto the fixed space is (1 + R + R^2)/3, which costs what the
transform costs; the split moves the cost into the two changes of basis and the coupling U. Count of sub-problems if each
projection were two calls at N/4 points (u-7's "a 64 x 28 block of the 64-point transform") and U one call at N/3: 4/4 + 1/3,
above 1, so no linear recursion from this split as it stands [guess, rough].

### Hybrid 2. Calls to a sealed box (u-5's recursion x u-8's composition law x j-cross S x j-manyatonce)

Idea. Every composition of the night treats the inner circuit either as a box or opens it; u-5 says the order changes only if
the number a of inner moves per array drops below the number m of directions. Ask the cleanest version: a K x K table X, wanted
A X A^T, the program may call the box A on any vector it has built, and must be right for every A.
Lemma [derived tonight, unreviewed]. Let the calls be c_j = A (L_j x + sum over i < j of M_ji c_i), j = 1..r, and the outputs
Q x + sum of P_j c_j, with fixed matrices L, M, P, Q, equal to (A x A) x for every K x K matrix A. Then r >= 2K.
Proof sketch: replace A by t A and compare powers of t. Degree 1: sum of P_j E L_j = 0 for every matrix E, so the tensor
sum of P_j (x) L_j vanishes; if the L_j span s dimensions, the P_j satisfy s independent relations and span at most r - s.
Degree 2: the answer has rank K^2 and passes through the L_i on the way in and the P_j on the way out, each of rank at most K,
so s >= K and r - s >= K. The textbook (K calls on rows, K on columns) is therefore optimal for a sealed box.
The hatch: the proof scales A, so it says nothing once the program may use a relation of the box, such as A^2 = 1 or A = A^T.
Tried [ran, FLOATS, least squares from random starts, `box.py`, `box2.py` on the Linux machine; a hit is a candidate only, no hit
is not a proof], K = 2:
- every box, 4 calls: found at once (5 of 6 starts, residual 1e-15, and right on fresh boxes). Control passed.
- every box, 3 calls: none in 60 starts (best residual 0.24). Agrees with the lemma.
- every involution (A^2 = 1, trace 0, not symmetric), 3 calls: none in 24 starts; 2 calls: none in 12 starts.
- every reflection (A = 1 - 2 u u^T, so A^2 = 1 AND A = A^T), 3 calls: **found in 24 of 24 starts** (residual 1e-16, right on
  fresh reflections); 2 calls: **found in 12 of 12 starts.**
Then by hand, and checked exactly [derived + ran, `refl2.py`, 65 cases in fractions]: write the table as
X = alpha 1 + beta J + [[p, q], [q, -p]] (J the quarter turn). For a reflection A, A A^T = 1 and det A = -1 make the first two
parts free, and the third comes out of TWO NESTED calls: (t, u) = A sz A (p, q) with sz = diag(1, -1), because A sz A is the
reflection at twice the angle. So for 2 x 2 reflections a = 1 call per line, where a sealed box needs 2.
Criticism at once: this is not a saving. The glue (alpha, beta, p, q from the four entries, and back) is two butterflies on each
side, and a butterfly IS the box at K = 2; for the transform's own kernel A sz A is just the exchange of p and q, and the whole
thing is the textbook's four butterflies in another arrangement. And K = 2 is special: two of the four dimensions of the table
are free there (the identity and the quarter turn); at general K only the identity is [derived, quick]. What survives is the
statement of the hatch: **the relation that lets calls be shared is "symmetric and an involution" together (a reflection);
A^2 = 1 alone did not do it in the search**, and the mechanism is a conjugate A M A of a fixed matrix M by the box, which is
again a reflection. Whether anything of it is left at K = 4 with a glue of O(K^2) gates is experiment 4.
Where it stops: K = 2 only; the searches are floats; the lemma is for two directions (I expect m K^(m-1) for m directions, not
derived); glue is not counted in the box model, and at K = 2 the glue is the box.

### Hybrid 3. The product-formula meter (m-cross's meter at the prime 2 x Morgenstern's volume x u-6's 1.585 x u-4's circuits)

Idea. m-cross metered every circuit at the prime 2 (classes, dead gates, quotient gates). j-cross's wall M is the same circuit
measured by size. Put both on one ledger. In primitive scaling a gate is w = (a u + b v)/g. [derived; it is Morgenstern's
argument in this scaling] Every N x N minor of the held wires is at most the product of (|a| + |b|)/g over the gates so far, so
**sum over gates of log2((|a| + |b|)/g) >= (N/2) log2 N** for the transform. A gate u + v or u - v brings at most 1, a gate
u + 2v at most 1.585 (u-6's number), a quotient gate (g = 2) with a = b = 1 brings 0.
Tried [ran, `pmeter.py`, `pmeter.out`, exact fractions; each file checked to hold every row of H]:

| circuit | points | gates | gates u +- v | gates u +- 2v | larger | quotient gates | budget | needed |
|---|---|---|---|---|---|---|---|---|
| brick (`slp_4`) | 4 | 7 | 3 | 4 | 0 | 0 | 9.3 | 4 |
| the 19 | 8 | 19 | 7 | 12 | 0 | 0 | 26.0 | 12 |
| staircase | 8 | 20 | 8 | 12 | 0 | 0 | 27.0 | 12 |
| staircase | 16 | 52 | 20 | 32 | 0 | 0 | 70.7 | 32 |
| staircase and 19 x 19 | 64 | 304 | 112 | 192 | 0 | 0 | 416.3 | 192 |
| u-4, Yates twice | 8 / 16 | 24 / 64 | 12 / 32 | 12 / 32 | 0 | 0 | 31.0 / 82.7 | 12 / 32 |
| u-4, hub minus parity sums | 8 | 26 | 19 | 7 | 0 | 0 | 30.1 | 12 |
| u-4, two chains twice | 8 | 38 | 21 | 16 | 1 (coefficient 4) | 0 | 48.7 | 12 |
| u-4, two chains twice | 32 | 220 | 114 | 87 | 19 (up to 16) | 0 | 302.0 | 80 |

Reading. (i) In every record the number of coefficient-2 gates is exactly (N/2) log2 N: this is m-cross's count of shifts and
h-6's law, now read as "one unit of volume per coefficient-2 gate, none per merge". (ii) No circuit of the night has a quotient
gate or a coefficient above 2, except the Z D Z^T circuits, where the large coefficients are the diagonal D and nothing else.
(iii) The hub circuit is the only one where gates u + v carry volume: each output is the hub minus twice a sum, so its 7
coefficient-2 gates account for a factor 2^7 of the determinant 2^12 exactly, and the 19 joins build a matrix of determinant 32
[derived]: 5 of the 12 units are carried by joins. (iv) The budget is never
the binding constraint at these sizes: the records hold more than twice what they need.
What it says about linear size [derived]: C N gates need an average budget of (log2 N)/(2C) per gate. No search of the night
has ever produced a gate with coefficient 4 that earns its keep, and the searches' pools (entries 0, +1, -1) could not hold one.

### Hybrid 4. The volume of subset sums, measured (g-4's minors x wave 6's models x the ledger of hybrid 3)

Idea. Z has determinant 1, so nobody in waves 5 and 6 thought of volume. But the ledger bounds every minor, not only the
determinant, and g-4 computed that Z has huge minors [read: g-4 section 6.3, "Z_bc(N) >= N (0.277 sqrt(k) - 1)", derived + ran
there]. Every program of wave 6 for Z (two chains, several chains, letters on any trees, trees with extra vertices) has gates
u + v and u - v only, so each is bound by that count.
Tried [ran, `zminor.py`, exact whole numbers]: the largest minor of Z at 8 points is exactly 2 (exhaustive over all 12,870
minors; rows {12}, {13}, {23} against columns {1}, {2}, {3}); at 16 points a 100-second search finds 5 (a lower bound on
the largest minor). So at sizes one can run the count is empty (1 gate at 8 points), as g-4 says: its bound passes N only
near k = 52 and 2N near k = 117.
Consequence [derived from g-4's bound; the bound itself is g-4's and unreviewed]: corners per point of ANY two-chain picture of
subset sums, plain or signed, with any helper wires made by adding and subtracting, are at least 0.277 sqrt(k) - 2 for every k
when no step has a coefficient 2, and at least 0.17 sqrt(k) - 2 when some have (budget 1.585 instead of 1).
"Corners per point stay bounded" was impossible before the search began. This is far weaker than L1 (a power of N) but needs no
order, no runs, no trees: it covers every hatch L1 lists except weights. And it says what a linear circuit for Z must have:
gates whose coefficients grow, average budget 0.277 sqrt(k)/C. The only known formula for Z with growing numbers in it is
i-cross W5, Z = D H D H D H D H D, which costs four transforms.

## 4. The most surprising thing, and the question that would tell the most

**Surprise of this wave.** Two reports that did not know of each other found the same way under a floor. u-9: allow a wire to
carry a 2 outside its own set and a circuit of 3.2 N gates is congruent to the transform modulo 4, below the one-flag floor from
32 points on, with every wire still a node of one cube tree modulo 2. u-5: in the published unit, the only program that changes
the order, every wanted term sits exactly one binary digit under an odd mixture and comes out by one quotient, the last gate of
its target. Hybrid 3 says why that is the direction the volume count points to: what linear size needs is wires that hold
several binary digits at once, about (log2 N)/(2C) of them per gate. Against that: no circuit of six waves holds two.

**Question. Can one gate do two jobs: join inputs and carry volume?** The floor N - 1 + (N/2) log2 N is two budgets added:
N - 1 gates that only connect, and (N/2) log2 N gates that each carry one unit of volume. L2 proves they cannot be merged in the
one-flag class. Any circuit below the floor has a gate that does both, or a gate that carries more than one unit. u-4's hub
circuit has joins that carry volume (and wastes more than it gains); u-9's modulo-4 circuit has wires that are a form plus twice
another form; nobody has an exact circuit that profits from either.
Experiment (small, exact, both ways informative). At 8 points, exhaustive or annealed search over wires with entries
0, +1, -1 on ARBITRARY supports (3,280 primitive vectors) plus "form + 2 x form on a disjoint set", gates any a u + b v that
lands in the pool. For each circuit found print three numbers: gates, gates u +- v that carry volume (the budget ledger of
`pmeter.py` run on a maximal minor after each gate), and the largest coefficient. Target 18 gates. A "no" at 18 with this pool
makes 19 the minimum of everything the night can express and says the two budgets do not merge at 8 points even off the flag;
a "yes" names the gate that does two jobs. This is u-7's `form-economy-8` with the ledger added. Then the same at 16 points
against 47.

## 5. Three objects for a skeptic, in this order

Nothing in wave 6 or here claims to beat a known count, so the order is by how much rests on each.
1. **The common floor of u-8 (section 3) and u-9 (section 4).** Exactly: a circuit for H in which every wire is a sign vector
   supported on a coset of one flag of subspaces (u-8: on a node of one affine merge tree, split direction free by branch) has
   at least N - 1 + (N/2) log2 N gates, with any gates between such wires, quotient gates included. Attack: are the two classes
   the same class; does either proof use that the partner of a shift is held; u-9's own remark that the agreement rule is not
   charged; try to build an in-class circuit with 18 gates at 8 points by hand (u-9's `game8.py` found none by annealing).
2. **The four proofs behind L1.** u-1's window lemma and its entropy arithmetic (exponent 1.10); u-2's nested-runs bound
   ((5/2)^k / (400 (1 + ln N))); u-0's block lemma; u-6's three lemmas for several chains. Exactly what each claims is in its
   "best" paragraph. Attack: the two exponents should be compared (is 1.32 right, then 1.10 is merely weaker; if they use
   different models say so); u-1's step "each output is the top of at most two steps"; u-2's claim for trees of bounded degree.
3. **The box lemma of this report (hybrid 2)**, and with it g-4's minor bound as I use it in hybrid 4. Exactly: r >= 2K calls
   for a fixed linear program right for every K x K matrix A; and corners per point >= 0.277 sqrt(k) - 2 for every
   add-and-subtract program for Z. Attack: the degree argument when a call's input mixes degrees; whether g-4's bound on the
   sum of squared minors really gives one large minor; whether "largest minor" in Morgenstern's count needs the wires primitive.
Also: hybrid 1's table is exact, but its last paragraph (no linear recursion from the split) is a rough count.

## 6. Eight experiments for the next wave

Deepen what is alive:

1. **twojobs** (the question of section 4; deepens u-7's form-economy-8, u-4's hub circuits, hybrid 3). Brief: as in section 4.
   Inputs: `u-7-quotient/qa.py` (the 3,280 vectors), `u-4-zdz/hubparity8.txt`, `s-cross/pmeter.py`, h-0's and h-5's search
   programs. Output: least gates found at 8 points in the pool with arbitrary supports; for the best circuits the ledger
   (how many joins carry volume, how many units per coefficient-2 gate); one line: was 18 reached. Count (G).
2. **digits** (deepens u-9's 3.2 N circuit and u-5's "one digit down"). Brief: u-9's circuit is congruent to H modulo 4. Find
   the cheapest whole-number circuit congruent to H modulo 8 at 16, 32, 64 points, starting from u-9's wires, and report the
   growth law of the cost of the third digit in N (u-9 expects about 2N more). Then the real question: for j digits, is the
   cost j x 2N, or can a wire that holds two digits serve two layers? Exactness needs k digits, so anything above N/2 per
   digit loses to the textbook; say plainly which side of that line the third digit falls. Inputs: `u-9-checkerboards/dirty.py`,
   `m-cross/precision.py`.
3. **floorhatch** (deepens L2). Brief: take the proof of u-8 section 3 and release ONE hypothesis at a time at 8 points, by
   exhaustive search in the game form of `u-9-checkerboards/cleangame.py`: (a) one wire on a set that crosses the flag;
   (b) one wire that is a form plus 2 x a form; (c) one node that is not an affine set. For each: is 18 reachable, and if
   not, does the proof's count still go through with that wire. Output: a table hatch / least gates / which line of the proof
   breaks.

Nobody has tried:

4. **boxrelations** (from hybrid 2). Brief: a sealed box needs 2K calls; at K = 2 a reflection needs 2 (`s-cross/refl2.py`),
   but there the glue is the box. Do K = 4 honestly: the family is all reflections 1 - 2P with P a projection of rank 2 in 4
   dimensions (the 4-point transform divided by 2 is one of them). Find the least number r of calls, AND the number of glue
   gates, for A X A^T on a 4 x 4 table: `s-cross/box.py` with K = 4 and the reflection family (floats first, then exact), for
   r = 7, 6, 5, 4. Also the families "A^2 = 1 only" and "A symmetric only" as controls. Report r, glue gates, and r x 7 + glue
   against the 16-point record 52 and textbook 64. The growth question behind it: is there any K with fewer than 2K calls and
   glue below (K^2/2) log2 K? A "no" at K = 4 with a reason extends the box lemma to reflections.
5. **thirdturn-basis** (from hybrid 1). Brief: the fixed space of R = D H / sqrt N has dimension (N + 2)/3 and a basis of
   vectors that vanish on half of the points. Find its sparsest basis at 16 and 64 points (candidates: indicators of the
   subspaces of sqrt N addresses on which Q vanishes), the cost in gates of the projection onto it, and what the coupling U
   between the two (N - 1)/3-dimensional spaces is in that basis (is it a smaller transform?). Output: gates for H at 16 and
   64 points by "project, scale, couple", against 52 and 304; and the recursion it would give. Inputs: `s-cross/quadric.py`,
   `u-7-quotient/qf.py`, `qh.py`.
6. **weightedz** (from hybrid 4 and fact E). Brief: every model for subset sums so far has gates u + v, u - v. Search at 8
   and 16 points for circuits for Z with coefficients 2 and 1/2 allowed (and for D1 Z D2 with free diagonals D1, D2, the
   same problem in count G): is anything below 12 or 32? Then the growth question in g-4's own terms: Z cut into its
   weight blocks costs N sqrt(log N) plus a change of basis; price that change of basis when coefficients may grow like
   2^sqrt(k). Inputs: `d-0-zeta/mincirc`, `u-3-zletter/` annealers, g-4 section 6.3.

One hybrid:

7. **unit-as-box** (u-5's three-shear exchange x hybrid 2's lemma x hybrid 3's ledger). Brief: write u-5's exchange
   (X, Y) -> (-D Y, D^-1 X) as a call program in the sense of hybrid 2: which calls to "a move along the port" does the
   published unit avoid, and which relation of the moves lets it (my guess: moves along different directions commute and a
   sum of two arrays held after different moves is a shear along the difference). Then run `pmeter.py` on one E8 invocation
   read from the certificate (u-5's `unit2adic.py` parses it): the budget, the quotient gates (u-5 counted 98,304) and the
   largest coefficient. Prediction from fact D: budget per gate above that of the plain schedule. One line wanted: the
   relation the unit uses that a sealed box does not have.

One that sounds silly:

8. **rotate by 120 degrees.** Forget the transform; compute R = D H / sqrt N, which is the transform up to free signs and
   satisfies R^3 = 1. A rotation of order 3 can be written as two reflections, or as three shears, in many ways. Brief:
   at 4 and 16 points list the ways to write R as a product of two reflections 1 - 2 P1 and 1 - 2 P2 whose mirrors have
   sparse bases (the 60-degree coupling of hybrid 1 says the mirrors meet at 60 degrees on (N - 1)/3 planes), and price each
   with `d-0-zeta/mincirc`; g-0 priced ONE mirror (24 gates at 16 points, the route ties 56) but never a pair at 60 degrees.
   It sounds like trading one transform for two; the reason to try is that each of the two mirrors can be chosen, and the
   single mirror of the transform cannot.

## 7. Criticism, last

- I read wave 6 through its result summaries. Where I say two proofs are "the same" (L1, L2) I matched their statements, not
  their steps. The exponents 1.10 and 1.32 in L1 may belong to slightly different models.
- Line 2 of section 0 rests on g-4's minor bound, which is derived and unreviewed; q-cross knew the bound and still wrote that
  no wall covers the corner count, so check that I am not misreading what g-4's bound applies to (it bounds circuits with
  coefficients of size 1; a two-chain program is one).
- The ledger of hybrid 3 is Morgenstern's argument; it is a floor on the budget, not on gates, and it was nowhere binding.
  "Carries volume" for a single gate is not defined; I only compared totals.
- Hybrid 1 explains numbers. Its only step towards a circuit is a rough count that says no.
- Hybrid 2's lemma is twenty minutes old. The two-call formula for 2 x 2 reflections is exact, and it is the textbook in
  disguise: I count calls and not glue, and at K = 2 the glue is two more boxes. "A^2 = 1 alone does not do it" is 36 float
  starts, not a proof.
- Hybrid 4's new runs are tiny (the largest minor at 8 points is 2); the content is g-4's.
- The question of section 4 is close to m-cross's ("which hypothesis breaks") and to u-7's own next experiment; what is new is
  only the ledger that says what to look for in an answer.
- Nothing here changes the order, or any constant.

Files: `waves/wave-06/s-cross/` : quadric.py, quadric.out (the transform split by a
quadric at 4 to 256 points; Linux machine, copied back); r3.py, r3.out ((D H)^3 at 4, 16, 64 points); box.py, box2.py, box.out,
box2.out (calls to a box, floats; Linux machine, copied back; box.out was copied while its last cases were still running);
refl2.py (the two-call formula for 2 x 2 reflections, exact fractions); pmeter.py, pmeter.out (the volume ledger on 11 circuits);
zminor.py, zminor3.out, zminor4.out (largest minors of the subset-sum matrix).
