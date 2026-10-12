# ag-7 rank-dial: the bus is switched off by the length of the shortest relation among the outputs, at degree about log2 k

11 October 2026, 07:39 to 08:16 EDT, inside a 60-minute box. Private research: nothing published, no git, no Lean, nothing reviewed.
Marks: [ran] = exact run of mine in this hour (files in `ag-7-rankdial/`); [derived] = by hand in this hour, checked by
nobody; [read] = from tonight's reports; [recalled] = from memory, no source opened; [guess].
Gate count everywhere: **(G)**, a gate is any a*u + b*v, scalings free. Count (O) is not used.
Fields: every exhaustive run is over the **two-element field** (and a few modulo 3, said each time). "None modulo 2" is
not "none" over the rationals. Section 4's lemma is proved for the two-element field and, in a weaker form, for any field.

**No circuit below a known count. No growth law below N log N for the transform. Nothing here changes the order.**
What is here is on the other side: a lower bound. From degree about log2 k on, the table of a polynomial of degree d at
all N cube points costs at least 2N - o(N) gates, in any circuit (section 4, derived in this hour, unreviewed). So the
road "N + o(N) at every degree" that ad-6 opened at degree 2 ends near degree log2 k. Linear size is not excluded by it.

Words. N = 2^k points; an *address* y is k bits. *The object* M(d, k): one output for each address y, one input c_S for
each set S of at most d bits, output(y) = sum of the c_S with S inside y. It is "every polynomial of degree at most d at
all cube points", and it is subset sums with only the inputs of size at most d kept. *Rank* R(d, k) = number of sets of
at most d bits. L(d, k) = least gates. *Helper*: a gate that is not an output. Every output except output(0) = c_0 needs
its own gate, so gates = N - 1 + helpers. *Textbook*: cut along the top bit and recurse,
T(d, k) = T(d, k-1) + T(d-1, k-1) + N/2; it tends to d gates per point for fixed d.
*Cut*: split the addresses along one bit into a lower and an upper half of n = N/2 points; an input is *upper* if its set
contains that bit. A wire is (lower part, upper part); *pure* = upper part 0, *mixed* otherwise. *Injection*: a gate
pure + mixed. *M2 gate*: mixed + mixed giving mixed. *Delivery*: mixed + mixed giving pure. *Versions* of an upper part:
the wires that carry it. *Bus*: an upper part with several versions (ad-2). *Relation*: a set of outputs whose sum
(with some non-zero coefficients) is zero whatever the inputs. *delta*: the number of outputs in the shortest relation.
For M(d, k), delta = 2^(d+1) over every field [derived in five lines, section 4]; at full rank there is no relation.

## 0. In ten lines

1. **The table** (section 1) [ran]. 8 points: 7, 11, 12 gates for d = 1, 2, 3, modulo 2 and modulo 3, each equal to the
   textbook. 16 points: d = 1 is 15; d = 2 is between 21 and 26 (no circuit with 20 gates modulo 2, exhaustive; none
   with 19 modulo 3); d = 3 is between 26 and 31; d = 4 is 31 or 32 (ad-2). The exact values for d = 2 and 3 at 16
   points were out of reach of the exhaustive tools in this hour. No bus has a realised saving in anything decided.
2. **8 points cannot show the dial** [ran + derived]: for d = 2 and d = 3 the lower half (4 points) has full rank, and
   the 654 and 2,802 minimum circuits have the same cut profiles. The first room is at 16 points.
3. **What a cut forces at rank below n** (section 2) [derived, two lines, the proof of ab-5 with rank in place of n]:
   M2 gates >= L(d-1, k-1), injections >= R(d, k-1), so for d >= 2: L(d, k) >= L(d-1, k-1) + R(d, k-1) + n - 1. At 16
   points, d = 2: 21, which is exactly where the exhaustive search stopped. The textbook pays n injections; only rank many are
   forced. **That is what full rank takes away: the n - rank injections that could be dropped.**
4. **The fine dial** (section 3) [ran]. Keep the affine part and add the pair terms c_ij one at a time; the pairs kept
   form a graph G on the bits. All 4 graphs at 8 points and 9 of the 11 at 16 points are decided exactly. Helpers:
   a forest costs exactly one per edge; the triangle 4; the four-cycle 5. In every decided case
   helpers = the least, over the orders of the bits, of the sum of (2^(number of earlier neighbours) - 1): the textbook.
5. **The quantity that changes** [derived]: a helper "slope" in direction i is the difference of
   2^(k - 1 - neighbours of i) pairs of outputs, so it can serve that many. It can serve more than one exactly when
   some pair ij is missing, and a missing pair is exactly a relation among FOUR outputs (y, y+i, y+j, y+i+j). When
   the last pair comes in, delta jumps from 4 to 8 and every slope is read once. Rank moves by one unit; delta doubles.
6. **Private-wire lemma** (section 4) [derived; checked mechanically on all 3,456 minimum circuits at 8 points and on
   ad-6's circuit up to 2,048 points; sharp on both]. Two-element field, delta > 4. Make a graph: one vertex for every
   wire that is not an output, one extra vertex z; one edge for every output (between its two operands if neither is
   an output; between z and the operand that is not an output otherwise). Then no wire labels two outputs, two outputs are never added to make a third, and
   **the graph has no cycle shorter than delta - 2**. So N - 1 edges must fit on (non-output wires + 1) vertices
   without short cycles.
7. **Growth law for the bus** [derived from 6 and a recalled graph bound]. Outputs per non-output wire
   <= (1/2)(1 + N^(1/(2^d - 2))), and about N^(1/2^d) for small d. At degree 2 that leaves a power of N (ad-6 lives
   there); at degree log2 k + 3 it is below 1.05. So for log2 k + c <= d and rank o(N): **L(d, k) >= 2N - o(N)**,
   against N + o(N) at d = 2 and the textbook's d N. At 2^64 points: at least 1.39 N at degree 5, 1.83 N at degree 7, 1.98 N at degree 10 (`law.out`).
   Over the rationals the same holds with a weaker graph condition and a constant I did not work out.
8. **Answer to the brief.** The bus stops paying at degree about log2 k = log2 log2 N, that is at rank about
   k^(log2 k): far below any fixed fraction of N. The invariant is delta, not rank: at the same rank a matrix with
   short relations is cheap (a forest of pairs), and d = 1 has rank k + 1 and no helper at all. ad-6's N + o(N) cannot
   go beyond degree about log2 k, now for every circuit and not only for circuits with two helpers per output. For a
   fixed degree such as 3 it stays open (floor N + about N^(7/8)).
9. **The second step, tried** (section 5) [derived, a sketch; its three facts checked on all 6,960 derivations of the
   full-rank minimum circuits at 8 points]: "a private wire for every private wire" would give 3N, then d N, then
   N log N. Where the graph is a forest of small trees (*groups*): a private wire made as (a wire of its own group) +
   (a wire from outside) needs an outside wire of its own, and a group can lend at most one. So
   **gates >= 3N - 2 rank - P**, P = the number of private wires made from TWO wires that both lie outside their
   group. The third N is paid unless P is about N. Wall named: OUTSIDE-PAIR.
10. Better question (section 6): **c(d) = lim L(d, k)/N is 1 at d = 1 and 2, at least 2 - o(1) from log2 k on, and at
    most d - 1. Is it bounded?** L(k/2, k) = O(N) would be linear size for the transform (ae-cross hybrid 3).

## 1. First experiment: the table [ran; two-element field unless said]

Tools. `rows.py` writes M(d, k). `d-0-zeta/mincirc` (exhaustive over sets of helpers) and my `mincirc2.c`: the same
program with one rule added, *a helper that could already have been made before the previous helper was added must have
a larger number than it*. Every set of helpers has such an order (swap neighbours that break it), so a NO stays
exhaustive. It visits 2.4 times fewer states at 4 helpers and reproduces 9 known answers (8 points d = 2, 3 modulo 2 and
3; 16 points d = 2 at 3 and 4 helpers). `ad-7-modulo4/enum2` lists every minimum circuit; `cuts.py` sorts each in each
cut. The number of minimum circuits for d = 3 at 8 points, 2,802, is ab-4's number: the chain of tools agrees.

| points | d | rank | least gates | gates per point | textbook | forced by the cut (section 2) | longest bus in a minimum circuit | realised saving |
|---|---|---|---|---|---|---|---|---|
| 8 | 1 | 4 | 7 (mod 2, mod 3) | 0.875 | 7 | 7 | 4: the one upper input carries all 4 upper outputs | 0 |
| 8 | 2 | 7 | 11 (mod 2, mod 3) | 1.375 | 11 | 10 | 3 (234 of 1,962 cuts), else 1 or 2 | 0 |
| 8 | 3 | 8 | 12 (mod 2, mod 3) | 1.5 | 12 | 11 | 3 (666 of 8,406 cuts), else 1 or 2 | 0 |
| 16 | 1 | 5 | 15 (mod 2, mod 3) | 0.94 | 15 | 15 | 8: the one upper input carries all 8 upper outputs | 0 |
| 16 | 2 | 11 | **21 to 26**: no 20 modulo 2 (exhaustive, 7.5 minutes), no 19 modulo 3 | 1.31 to 1.63 | 26 | 21 | not computed | 0 to 5, not decided |
| 16 | 3 | 15 | **26 to 31**: nothing run; the lower end is the cut bound | 1.63 to 1.94 | 31 | 26 | not computed | 0 to 5, not decided |
| 16 | 4 | 16 | 31 or 32 [read: ad-2] | 1.94 or 2 | 32 | 27 | 4, saving nothing [read: ad-2] | 0 or 1 |

*Longest bus* here = the largest number of wires with one upper part, minus one; it does not depend on how the circuit
is derived. *Realised saving* = textbook minus least gates.
Cut profiles at 8 points (`cuts_k3.out`), as (new upper parts, further versions, pure gates):
d = 2: (3, 4, 4) in 1,716 cuts, (3, 5, 3) in 234, (4, 4, 3) in 12. d = 3: (4, 4, 4) in 7,824, (4, 5, 3) in 570,
(5, 4, 3) in 12. The same three shapes with one more M2 gate: at 8 points degree 2 and degree 3 are the same game,
because the lower half, 4 points, has rank 4 at both. In every minimum circuit a helper is read by at most 3 outputs.

What was not done: the exact value and the census of minimum circuits for d = 2 and d = 3 at 16 points. The search
needs 6 to 11 helpers for d = 2; five helpers took 7.5 minutes on the rented machine, each further one costs about fifty
times more. The developer of ladder-degree-3 computes the same three columns: `ag-7-rankdial/TABLE.txt` is for them.

## 2. What a cut forces when the lower half has rank below n [derived]

Put the lower inputs to zero: pure wires vanish, an injection becomes a copy, so the M2 gates alone compute the upper
parts of the upper outputs, which are M(d-1, k-1): **M2 gates >= L(d-1, k-1)**. Now look at lower parts: an upper input
has lower part 0, an M2 gate stays in the span of what it reads, an injection adds one pure wire. The lower parts of the
upper outputs are M(d, k-1), of rank R(d, k-1): **injections >= R(d, k-1)**. The lower outputs need n - 1 gates of
their own, and the n upper outputs are n different mixed gates. So

    L(d, k) >= max(n, L(d-1, k-1) + R(d, k-1)) + n - 1          (the n matters only at d = 1).

Values: 3, 4 at 4 points (d = 1, 2), both exact; 7, 10, 11 at 8 points (true 7, 11, 12); 15, 21, 26, 27 at 16 points.
The textbook count is L(d, k-1) + L(d-1, k-1) + n. The difference has two parts:

- **injection room = n - R(d, k-1)**, the number of independent relations among the lower outputs;
- **delivery room = L(d, k-1) - (n - 1)**, the helpers of the lower half.

At full rank the first room is 0 and ad-2 found the second unused. At d = 2 and large k, ad-6's circuit uses both almost
in full: its mixed part is n outputs and o(n) helpers, so o(n) injections, and its lower outputs are all deliveries
(each is A(y) + B(class), two versions of one upper part) [derived from ad-6's formulas, not run].
One more consequence [derived]: when the injections number exactly the rank, every injected wire reaches (counted
modulo 2) a set of upper outputs that is a codeword of the code of degree d on k - 1 bits, so at least n / 2^d of them.
A bus in ad-2's sense is long because the code has heavy words; at full rank the bound is 1.
If both rooms were used in full at every cut the cost would be N + (a sum of ranks): linear at every d, the transform
included. Unrolled, the inequality is that statement as a floor: about N + rank, never more than 2N. It is linear and
therefore harmless as a lower bound; what it gives is the two rooms by name.

## 3. The fine dial: one pair term at a time [ran; two-element field]

`graphs.py`: for a graph G on the k bits, the matrix "affine function + sum over the edges ij of G of c_ij y_i y_j at
all cube points"; rank k + 1 + edges. Least helpers by `mincirc2`, every graph up to renaming the bits.

| points | graph of pair terms | rank | least helpers | least over orders of the sum of (2^(earlier neighbours) - 1) |
|---|---|---|---|---|
| 8 | none / one edge / path / triangle | 4 / 5 / 6 / 7 | 0 / 1 / 2 / 4 | 0 / 1 / 2 / 4 |
| 16 | none; one edge; two edges (touching, apart) | 5; 6; 7 | 0; 1; 2, 2 | 0; 1; 2, 2 |
| 16 | three edges: star, path, triangle | 8 | 3, 3, 4 | 3, 3, 4 |
| 16 | four-cycle | 9 | 5 (no 4, exhaustive; a 5 found) | 5 |
| 16 | triangle with a pendant edge | 9 | 5 (no 4, exhaustive; a 5 found) | 5 |
| 16 | all but one pair | 10 | 6 or 7 (no 5, exhaustive) | 7 |
| 16 | all six pairs (d = 2) | 11 | 6 or more (no 5) | 11 |

Reading [derived]. The textbook adds the bits in some order; output(y + i) = output(y) + slope, and the slope
c_i + sum of c_ij over the earlier neighbours j of i inside y takes 2^(earlier neighbours) values, one of them an input.
Each slope is a helper read by 2^(i - 1 - earlier neighbours) outputs. So:

- a forest: one helper for each rank unit, every helper read by many outputs;
- the complete graph: N - 1 - k helpers, every helper read by ONE output;
- **in all 13 decided cases the least equals the textbook.** The first two cases where they could differ are the last two
  rows (7 and 11); they need 5 to 10 helpers and were not decided.

Which relation does a shared slope use? Two outputs pairs (y, y+i) and (y', y'+i) with one slope: a relation among four
outputs. Four-term relations exist exactly when a pair term is missing (the second difference in directions i, j is
c_ij). So within degree 2 the dial has one click: **delta = 4 while any pair is missing, delta = 8 when none is.**

## 4. The private-wire lemma [derived; mechanical check at 8 points]

delta for M(d, k) [derived]: a relation is a function lambda on the cube that every monomial of degree at most d sums
to zero against. Split on one bit, lambda = (lambda_0, lambda_1): lambda_1 kills degree d - 1 and lambda_0 + lambda_1
kills degree d on k - 1 bits. If one of the two is zero the other kills degree d: induction on k. If neither, each
kills degree d - 1 and has at least 2^d points. So delta >= 2^(d+1); the (d+1)-fold difference attains it. Any field.

**Lemma (two-element field).** Take any circuit for N different outputs whose shortest relation has delta > 4 terms.
Let W be the wires that are not outputs (inputs included), V their number. Each output that is not an input has one
gate o = u + v. Then:
(c) u and v are never both outputs (that would be a relation among 3 outputs).
(a) If u is an output and v is not, call v the *label* of o. No wire is the label of two outputs: o1 + u1 = o2 + u2 is
    a relation among four different outputs, or else the two gates read each other in a circle.
(b) Otherwise u and v are both in W: draw the edge {u, v}.
Add a vertex z standing for the zero form, and an edge {z, label} for each output of kind (a). Around any cycle each
vertex is counted twice, so the edge values add up to zero; an edge of kind (b) is worth its output, an edge at z is
worth o + u. A cycle of length L therefore gives a relation among at most L + 2 outputs, and it is not empty because
the L outputs that own the edges are different and at most two of them can be cancelled. Hence
**the graph, on V + 1 vertices with N - 1 edges, has no cycle shorter than delta - 2.** Without z: N - 1 <= V + (edges of a
graph on V vertices with no cycle shorter than delta).

Mechanical check [ran, `private.py`, `private.out`]: on all 654 minimum circuits for d = 2 at 8 points (delta = 8), in
each of their 1,176 ways of deriving the outputs: no gate of kind (c), no repeated label, shortest cycle exactly 6 in 36
derivations and none in the other 1,140. On all 2,802 minimum circuits for d = 3 (no relation at all), 5,148
derivations: always a forest. So delta - 2 is attained, and the statement is not vacuous as a statement; as a bound on
gates it is vacuous at these sizes (the inputs alone are enough vertices).
Second check, on a circuit that shares heavily [ran, `lemma_ad6.py`, `lemma_ad6.out`]: ad-6's circuit for degree 2,
rebuilt with its own program and read modulo 2, k = 3 to 11. At 2,048 points 2,022 of its 2,047 outputs are
helper + helper. At every size: no gate of kind (c), no repeated label, no repeated edge, shortest cycle exactly 6,
and shortest cycle that avoids z exactly 8 from 32 points on (none below).

Numbers [ran in floating point from the lemma and one RECALLED theorem, `law.py`, `law.out`]. Recalled (Alon, Hoory,
Linial 2002, not looked up; ad-6 leaned on the same): a graph with v vertices, average degree D >= 2 and no cycle
shorter than 2r has v >= 2 (1 + (D-1) + ... + (D-1)^(r-1)). With r = 2^d - 1 this gives
N - 1 <= ((V+1)/2) (1 + ((V+1)/2)^(1/(2^d - 2))), and gates >= N - 1 + V - (rank - 1).

| k (N = 2^k) | d = 2 | 3 | 4 | 5 | 6 | 7 | 8 | 10 | 12 |
|---|---|---|---|---|---|---|---|---|---|
| 16: gates / N at least | 1.11 | 1.35 | 1.64 | 1.75 | 1.71 | 1.57 | | | |
| 32 | 1.008 | 1.11 | 1.38 | 1.67 | 1.84 | 1.92 | 1.96 | 1.97 | 1.89 |
| 64 | 1.000 | 1.008 | 1.11 | 1.39 | 1.67 | 1.83 | 1.92 | 1.98 | 1.995 |
| 128 | 1.000 | 1.000 | 1.008 | 1.11 | 1.40 | 1.67 | 1.83 | 1.96 | 1.99 |

(The bound falls again when the rank stops being small: the inputs are non-output wires too. At full rank it says nothing.)
For d = 2 the form without z gives V >= about 2 N^(3/4): ad-6's girth bound for pairs of partitions, now for every
circuit over the two-element field. ad-6's family has 2 N log2(k)/k: the gap at degree 2 is still open.

**Over the rationals, scalings free** [derived, rougher]. (c) and (a) hold word for word. A cycle through z still gives a
relation. A cycle that avoids z does not (L outputs in the span of L wires need not be dependent), but any connected
piece with more edges than non-z vertices does, with at most twice as many terms as edges. So every piece with fewer
than delta/2 edges has at most one cycle, and none if it contains z. A graph with (1 + e) times more edges than
vertices has two cycles within about (1/e) log(vertices) of each other [recalled as a standard fact, not looked up],
so again V >= (1 - e) N once 2^d is a large multiple of k. I did not work out the constant.

**Statement in the brief's terms.** The longest bus, as outputs per non-output wire, obeys
rho <= (1/2)(1 + N^(1/(2^d - 2))), and by the form without z about N^(1/2^d) for small d: N^(1/4) at d = 2, N^(1/8)
at d = 3, 2^(k/2^d) in general. It is below 1 + e as soon as 2^d > k/e. In rank: the bus pays while rank is below about k^(log2 k). **What a bus needs from the
lower half is a short relation; full rank has none, and degree d has none shorter than 2^(d+1).**

## 5. Went around, four times

- *The exhaustive search stops at 20 gates.* Yes, and: ask what a cut forces at low rank. It forces rank many
  injections, not n; that gave 21 by hand, the number the machine had just reached, and the two rooms of section 2.
- *8 points show nothing* (d = 2 and d = 3 are the same game there). Yes, and: turn the dial by single inputs instead of
  whole degrees. That gave the graph table, "a forest costs one helper per rank unit", and the four-term relation.
- *"Rank is the reason" is not true as stated.* d = 1 has rank k + 1 and no helper, because outputs feed outputs; and a
  generic matrix of rank r costs about N r / log N [recalled counting], far more than this one. Yes, and: what a shared
  wire always creates is a relation among the outputs that read it. That gave the lemma, which does not mention rank.
- *Try the lemma twice*: the private wires are N new forms; if each needed a private wire of its own the count would
  be 3N, then d N. [derived, a sketch; regime assumed: the graph is a forest of trees, the *groups*, whose diameters are
  well below delta/3.] Inside a group two wires differ by the sum of the outputs on the tree path between them: a
  *light* form made of outputs that belong to that group. From "no short relation":
  (1) a group makes at most one of its wires from two of its own;
  (2) if w = m + x with m in w's group and x outside it, then x is the path sum from m to w, and different w have
      different x;
  (3) **a group holds at most one wire that is such an x**: two of them would differ by a path of their own group and
      also by paths of the groups that read them, three sets of outputs with different owners, a short relation.
  Count [derived]. A forest with N - 1 edges, g groups and I isolated wires has N - 1 + g + I vertices. Its group
  wires that are not inputs number at least N - 1 + g - 1 - R; at most g are made inside (1); let P be made by a gate
  whose two operands BOTH lie outside the wire's group; the rest are of shape (2), each with its own x, of which at
  most g sit in groups (3). So I >= N - R - P - g - 2, the g cancels, and
  **non-output wires >= 2N - R - P - 4, gates >= 3N - 2R - P - 4.**
  Mechanical check of (1), (2), (3) where there is no relation at all [ran, `level2.py`, `level2.out`]: the 2,802
  minimum circuits for d = 3 at 8 points in all their 6,960 complete derivations (ad-2's number, found independently):
  no derivation breaks any of the three, and no helper is (an output) + (a wire of its own group). Of the 34,800 helper
  gates none is inside a group, 10,272 are of shape (2) and 24,528 have both operands outside (5,496 of them for
  isolated wires); at that size most operands are inputs, so this says nothing yet about P when the rank is small.
  At d = 2 and 8 points (delta = 8, trees too long for the regime) fact (2) fails in 156 of 1,608 derivations and 270
  helpers are (an output) + (a wire of their own group), both through the one 8-term relation, as they may; (1) and (3)
  hold there too.
  My first count here (sqrt(N) groups reading each other in a grid) missed (3) and was wrong.
  What is left is the gate w = a + b with a and b both outside w's group. It ties the base wires of three groups
  together; the only constraint I found is that a group may use each pair of other groups once, and N^(1/3) groups
  satisfy that. **The wall has a name: OUTSIDE-PAIR.** If circuits with P about N do not exist beyond degree 3 the
  floor is 3N and the same question returns one level down; if they do, that gate is the shape of a cheap circuit.

## 6. Growth law, and the better question

- Law found, a floor and not a circuit: **L(d, k) >= (2 - e) N - R(d, k) for 2^d >= C(e) k** [derived; two-element field
  with C explicit through the recalled bound; any field with C not worked out]. With ad-6: c(1) = c(2) = 1;
  c(3) between 1 and 2; c(d) between 2 - o(1) and d - 1 from degree log2 k + c on, where c(d) = L(d, k)/N for large k.
- For the transform: a floor of 1.5 N for the half-rate encoder of ae-cross's hybrid 3, linear, harmless. At full rank
  the lemma is empty: there is no relation to forbid.
- **The lemma is about the space, not the matrix** [derived]. Relations among the outputs depend only on the space the
  outputs span, so the same graph exists for ANY matrix with that column space (any generator of the code of degree
  d, ae-cross's "cost of the space"). If s of its outputs are inputs: gates >= 2N - rank - s - eN >= 2N - 2 rank - eN.
  For the cheapest-generator brief: no change of basis brings a code with long relations and small rank below about
  2N; at half rate the floor is N, twice the number of outputs that have to be made.
- The brief's two branches: buses do NOT pay up to a rank that is a fixed fraction of N. They stop at rank about
  k^(log2 k). So "the low-degree part is linear with constant 1" is false beyond degree log2 k, and what remains of the
  hope is the constant: **is c(d) bounded?** The lemma says each output owns a wire; it does not say each owned wire
  owns another. A proof that it does would be a proof of N log N for an explicit matrix, which nobody has for any
  matrix; a circuit in which it does not (degree 4 in 2N + o(N)) would be the second rung.
- Smallest test of the better question [derived]: degree 4 at all cube points. Floor 2N - o(N) only from k about 128
  on; ceiling 3N + o(N) (ad-6's step). How to try for 2N: outputs = (table of degree 4 on fewer bits) +
  (a private wire), with the private wires, a table of total degree 4 and degree 3 in the non-selector bits, written
  as (function of one partition class) + (function of another) with o(N) classes. The lemma applied to that table
  alone forbids it when its own shortest relation is long; ad-6 allows it when that relation has 8 terms. By section 5
  a circuit below 3N must make a positive fraction of its private wires from two wires that both lie outside their
  own group (in the regime of section 5).

## 7. Mutations (not judged)

1. **Decide the last two rows of section 3** (7 and 11 helpers at 16 points). A search that uses the cut inequality
   and the bit symmetries to prune; `mincirc2` has neither. This is also the d = 2 line of the first table.
2. **Second level on purpose.** Search circuits for degree 3 or 4 of the shape "output = parent output + private wire,
   private wires in sqrt(N) tree-shaped groups reading each other": is there one with 2N + o(N) at degree 4?
3. **The lemma for other tall matrices.** Any N different forms with no relation shorter than about 4 log2 N and rank
   below e N cost (2 - e) N. Which matrices of the night have long relations? (The low levels of superset sums, the
   transpose of this object, by the transposition rule only up to the difference of the sides.)
4. **A third kind of gate.** The lemma sorts output gates into (a) and (b). Do the same for the gates of the private
   wires, with the relations among outputs AND private wires of small depth, and find the exact inequality between
   the number of groups and their sizes. First target: gates >= 3N - 2 rank - P as a theorem, with the regime (small
   trees) justified and not assumed, or with "long-range" gates counted into P; then a bound on P itself.
5. **Relations with coefficients.** Over the rationals a cycle away from z is free. Is there a circuit over the
   rationals that uses this (short cycles in the helper graph that carry no relation) and beats the two-element count
   for some M(d, k)? The smallest case is the 6-cycle at 8 points.
6. **The same dial for the engine** (moves and blocks): the worth of a shared label there should be its number of
   readers minus one, and the readers of one label are tied by a relation among blocks. Not looked at.
7. **Literature**: lower bounds for linear circuits that compute a code of large dual distance. I did not search; the
   lemma may be a known exercise.

## 8. Criticism, last

- The lemma and everything after it in section 4 were derived in under an hour and read by nobody. The two checks
  test its three statements on real circuits, where it is sharp; they do not test the step from the graph to a number
  of gates, and no size where that number bites can be searched exhaustively.
- The numbers in the table of section 4 rest on a theorem I recalled and did not look up, and on floating point.
  The qualitative statement "2N - o(N) from degree log2 k + c on" needs only that a graph with noticeably more edges
  than vertices has a cycle of length O(log), which is safer; the constant c is not pinned.
- 2N is a constant. It closes "N + o(N)" above degree log2 k; it says nothing about the order, nothing at full rank,
  and nothing about degree 3, which stays open (floor N + N^(7/8)).
- The rational version is a sketch. "At most twice as many terms as edges" and the two-cycles fact are stated, not
  proved line by line.
- Section 5's fourth turn (the second step) is a sketch. Its first version was wrong and its second had an arithmetic
  slip (2.5 N where the count gives 3N - 2 rank - P); the present one is fifteen minutes old. It holds in a regime (the
  graph a forest, the trees of diameter well below delta/3) that I assumed and did not justify: a tree can be a long
  path, and a gate between two far ends of it escapes all three facts. The check at 8 points is at full rank, where
  the inequality itself is empty. "N^(1/3) groups satisfy that" is a count of the one constraint I found, not a
  construction, and other constraints may exist.
- The first experiment is incomplete: at 16 points d = 2 is "21 to 26" and d = 3 is "26 to 31"; the columns "longest
  bus" and "realised saving" are filled only where the minimum circuits could be listed (8 points) or were read.
- The cut inequality of section 2 is derived; the only support is that it never exceeds a known value and equals the
  exhaustive floor at 16 points, d = 2.
- "Least = textbook in all 13 decided graphs" is 13 small graphs, modulo 2. The two undecided rows are the interesting ones.
- `mincirc2`'s ordering rule is argued in two lines and checked on 9 known answers.
- I did not read ag-0's results (none had landed) and searched no literature.
- Nothing here changes the order, or any constant.

## Files

`waves/wave-10/ag-7-rankdial/`:
- `rows.py` (the matrix M(d, k)), `rows_k*_d*.txt`; `climb.sh`; `out_p*_k*_d*_m*.txt` (every mincirc answer of section 1).
- `mincirc2.c`, `mincirc2`: d-0's exhaustive search with the ordering rule and an optional split of the first level.
- `TABLE.txt`: the table of section 1, for the developer of ladder-degree-3.
- `enum_k3_d2.txt`, `enum_k3_d3.txt`: every minimum circuit at 8 points (enum2). `cuts.py`, `cuts_k3.out`: the cuts.
- `graphs.py`, `graphs_k3.out`, `graphs_k4.out`, `g_k*_*.rows`, `g_k*_*.sol`: the fine dial; `remote/`: the runs made on
  the rented machine (`r2_k4_d2_m5.txt`: no 20 gates for d = 2; `r2_c4_m5.txt`: the four-cycle; `r2_tripend_m5.txt`: the
  triangle with a pendant edge; `r2_k4minus_m5.txt`: all but one pair).
- `private.py`, `private.out`: the mechanical check of the lemma at 8 points. `level2.py`, `level2.out`: the check of the
  three facts of the second step. `lemma_ad6.py`, `lemma_ad6.out`: the same on
  ad-6's circuit. `law.py`, `law.out`: its numbers. `mod3_k4_d2.out`: 16 points, d = 2, modulo 3.
