# ad-6 two-helpers: the answer for degree 2 is "o(N)", by a family one can write in two lines

11 October 2026, about 06:15 to 07:15 EDT, 60-minute box. Private. One agent; nothing reviewed, nothing in Lean, nothing published.
Marks: [ran] = run of mine tonight, whole numbers, files in `ad-6-twohelpers/`; [derived] = by hand tonight, checked by
nobody; [read] = from tonight's reports; [recalled] = from memory, no source opened; [guess].
Gate count everywhere: **(G)**, a gate is any a*u + b*v, scalings free. Count (O) is not used.

**No circuit for the transform below a known count and no growth law below N log N for the transform. Nothing here
changes the order. What is here: a growth law for a smaller object (polynomials of degree 2), N + o(N).**

Words. N = 2^k cube points, an address is k bits. A *pair* is two partitions P1, P2 of the cube points; it is *good for
degree d* when every polynomial of degree at most d in the bits is (a function of the P1 class) + (a function of the
P2 class). *Classes* = number of classes of P1 plus number of classes of P2. V(k) = least classes of a pair good for
degree 2. The *graph* of a pair: vertices = classes, edges = cube points.

## 0. In eight lines

1. **V(k) = o(N). The ratio V(k)/N falls to 0, like 2 log2(k) / k.** [derived, then ran exactly for k = 3 to 12]
   Family "selector and atoms", section 1. Classes/N: 0.875, 0.75, 0.6875 at 16, 32, 64 points; 0.50 at k = 10;
   0.34 at k = 16; 0.13 at k = 64; 0.03 at k = 400 (`verify.out`, `law.out`). aa-cross's family stays at 0.75.
2. **Gates: a polynomial of degree 2 at all N cube points costs N + o(N).** [ran] The circuit is built and replayed:
   right on every unit input for k = 3 to 9 (exact), on random whole numbers to k = 16 (`circuit2.py`, `circuit2.out`).
   Gates/N: 1.48 at k = 16; by a count-only copy checked against the built circuits: 1.25 at k = 32, 1.15 at k = 64,
   1.03 at k = 400 (`law.out`). The plain way costs about 2N. The approach to N is slow: excess about 1.5 log2(k)/k.
   This answers ab-3's "first test: degree 2, is 2N forced?" with no.
3. **V(4) = 14 and V(5) = 24 exactly; V(6) is 40 to 44.** [derived from a RECALLED theorem; no exhaustive search was
   run] Section 2. The lower bound uses only "no cycle shorter than 8" and the Moore bound for irregular graphs.
4. **What the best graph looks like:** at 8, 16, 32 points it is a complete two-sided graph with every edge cut in two
   (2 x 2, 2 x 4, 4 x 4). In general: the cube point (a, y) is a *flag* (a corner y together with a direction a) of a
   grid with 2^t directions; P1 classes are the corners, P2 classes are the lines of the grid. Section 3.
5. **Ceiling, as the brief asked.** Girth alone forces classes >= about 2 N^(3/4) for degree 2 and, from degree about
   log2 k on, classes > 2N/3 [read: aa-cross, recalled bound]. So two helpers alone give at best N log N / log log N for
   the transform: not a saving exponent. And in ab-3's price list the new atom sells 3 units for 3N + o(N), one N per
   unit, against N/2 per unit for a coset sum. **It is a constant-factor object. Off the bar unless degree grows.**
6. **Degree 3 does not follow.** The family fails degree 3 at every size tried [ran], for a reason I can name (section
   4). What I have for degree d: classes <= N/2 + V_{d-1}(k - 1) [derived + ran for d = 3, 4], so gates per point at
   most d - 1 instead of d [derived, not built]. That is one unit saved, not o(d).
7. **Wall named: COORDINATES.** In the class "P1 forgets a fixed set of bits, P2 forgets a subspace chosen by those
   bits", the forgotten subspaces must sit on pairwise disjoint sets of coordinates [derived]. That is why the
   generalised quadrangle with its N^(3/4) classes cannot be labelled this way, and why this class stops at N log k / k.
8. Better question, section 6: is there a pair where NEITHER partition forgets a fixed set of bits?

## 1. The family (the object of this report)

Split the address into (a, y): a = t *selector* bits, y = the other m = k - t bits. Split the m bits of y into 2^t
groups, the *atoms*, one for each value of a.

- **P1 forgets a.** Its class is y. 2^m classes of 2^t points.
- **P2 knows a and every bit of y except the atom whose index is a.** With atoms of s bits: 2^t * 2^(m - s) classes.

Classes = 2^(k - t) * (1 + sum over atoms of 2^(-size)). With t about log2 k - log2 log2 k and s about t this is
about 2N * log2(k) / k.

Why it works [derived, five lines]. Write q(a, y) = q0(y) + sum_i a_i L_i(y) + c(a), q0 the part in y alone, L_i linear
in y. For a selector value b let L_b = sum_i b_i L_i and let L_b|atom b be its terms in the bits of atom b. Put
   A(y) = q0(y) + sum over b of (L_b | atom b),
   B_a  = c(a) + sum over b != a of ((L_a - L_b) | atom b).
Then A + B_a = q0 + L_a + c(a) = q, A is a function of y, and B_a does not contain the bits of atom a. Nothing used
that L_a is linear in a: **the family serves every function "one polynomial of degree 2 in y, plus an affine function
of y that may depend on a in any way"**, a space much larger than degree 2.

[ran, `verify.py`, `verify.out`] Exact test (walk the graph, integers only; controlled against aa-cross's rank test in
fractions on 18 cases, all agree). Good for degree 2 at every k from 3 to 12 and t = 1, 2, 3, and by the rank test in
fractions for k = 3 to 6 and every t. Note: `verify.py` died of memory in its LAST table (my bug: it tried t up to
k - 1 at k = 22); everything above that table is complete, and `law.py` prints the table instead.

| k | 3 | 4 | 5 | 6 | 7 | 8 | 10 | 12 | 16 | 24 | 32 | 64 | 128 | 400 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| classes / N | 1 | 0.875 | 0.75 | 0.6875 | 0.625 | 0.594 | 0.500 | 0.4375 | 0.344 | 0.273 | 0.211 | 0.130 | 0.067 | 0.030 |
| gates / N for degree 2 | 1.63 | 1.81 | 1.97 | 2.02 | 1.95 | 1.92 | 1.75 | 1.63 | 1.48 | 1.35 | 1.25 | 1.15 | 1.07 | 1.03 |

Classes: tested exactly to k = 12, formula above that. Gates: built and replayed to k = 16, count-only copy above
(the copy reproduces all 14 built counts, `law.out` line 1).

The circuit [ran, `circuit2.py`]. A is again a polynomial of degree 2 in y: the same program on m bits. B_a is an
affine function of the bits outside atom a: evaluated by halving (helper + helper). One output gate per point.
E2(k) = N + E2(k - t) + 2^t * (2^(k - t - s) + small). **Growth law: E2(k) = N (1 + O(log k / k)).**
At small sizes it is NOT a record (29 gates at 16 points; x-1 has 20 to 25 open there). Constants were not the aim.

## 2. V(4), V(5), V(6)

[derived] Lower bound from girth only. A good pair has no cycle shorter than 8 [read: aa-cross]. Strip hanging edges:
that removes as many vertices as edges, so it never lowers classes - N. What remains has every degree at least 2,
and the Moore bound for irregular graphs [RECALLED: Alon, Hoory, Linial 2002] says n >= 2 (1 + (d-1) + (d-1)^2 + (d-1)^3)
with d = 2 * edges / n. I checked by hand that adding hanging edges back cannot beat the bound taken at N edges.
[ran, `law.py`] Least n allowed: 14 at 16 points, 24 at 32, 40 at 64, 68 at 128, 116 at 256.

- **V(4) = 14.** 13 would need 16 edges on 13 vertices, average degree 2.46, bound 15.4 > 13. Attained (aa-cross).
- **V(5) = 24 = 3N/4.** 23 gives bound 23.25 > 23. Attained by the family with t = 1 (tested exactly).
- **V(6): 40 to 44.** Inside "P1 forgets one bit" 44 is exact [derived: the P2 classes form a triangle-free graph with
  32 edges, so at least 12 of them by Mantel]. Below 44 needs a pair of another kind.
- V(7): 68 to 80. V(8): 116 to 152.

This rests on one recalled theorem. An independent check of the one fact needed at 16 points ("no graph with all
degrees >= 2, no cycle shorter than 8, and 3 more edges than vertices, on at most 16 edges") is a small exhaustive
job I did not have time to run; the 3 x 3 two-sided graph with every edge cut in two (18 edges) is the example just
above the line. The brief's whole-number programme was not run.

## 3. What the best graph looks like

- 8 points: one 8-cycle (2 x 2 two-sided graph, edges cut in two). 16: 2 x 4. 32: 4 x 4, which meets the Moore bound.
- General: corners y of a grid with 2^t directions and 2^s values per direction; lines = a direction a and a corner
  with that coordinate erased; cube point = (corner, direction). Every 8-cycle is "change coordinate a, switch to
  direction a', change coordinate a', switch back, undo, undo": the product of three differences on three disjoint
  groups of bits (selector, atom a, atom a'), so it has no part of degree below 3. That is the whole proof again.
- With t = 1 this is the *thin* generalised quadrangle (a grid). The thick one would have class size N^(1/4) on both
  sides; the family has class sizes about log N / log log N. The gap between 2 N^(3/4) and 2 N log2(k)/k is open.

## 4. Where it stops, and two ways round that were tried

**Failure 1: degree 3.** [ran] Missing directions for degree 3: 2, 4, 6 at k = 4, 5, 6 with t = 1; 6 at k = 6, t = 2.
[derived] What it is made of: the monomial a_i y_p y_r with p and r in two different atoms b, b' and a_i telling b from
b'. Where a = b the P2 class does not see y_p, where a = b' it does not see y_r, and y_p y_r is not (a function without
y_p) + (a function without y_r).
*Yes, and (1):* spend one bit per degree. P1 forgets one bit a; P2 is R1 where a = 0 and R2 where a = 1, (R1, R2) a
good pair for degree d - 1 on the other bits. Then q = [q0 + r1(R1)] + [-r1(R1) or r2(R2)]. So
**V_d(k) <= N/2 + V_{d-1}(k - 1)**. [ran, exact] degree 3: 16, 30, 56, 108, 208 classes at k = 4 to 8 (0.81 N at k = 8,
tending to N/2); degree 4: 32, 62, 120, 236 at k = 5 to 8. 16 at k = 4 is forced by the dimension count; 30 at k = 5 is forced by
girth 16 and the same recalled bound (29 classes: bound 33.8) [derived]. The table in `verify.out` runs to k = 11. For gates [derived, not built]: e_d <= e_{d-1} + 1 with e_2 = 1, so **degree d costs at most (d - 1) N + o(N)**
against d N. One unit saved once; the slope in d is unchanged.
*Yes, and (2):* t selector bits for degree 3, four partitions R_a of the y cube. Necessary [derived]: the joins
(R_00 v R_01, R_10 v R_11) and (R_00 v R_10, R_01 v R_11) must each be good for degree 2. I found no such four. Open.

**Failure 2: the generalised quadrangle.** The affine quadrangle on q^3 points with q of its q + 2 directions has
exactly q^4 = N flags and 2 N^(3/4) classes, and no short cycles. Labelling "P1 forgets the direction, P2 = direction
and point modulo that direction's line" fails: [derived] if P1 forgets the selector a and P2 at a forgets a subspace
L_a of the y bits, then walking a square (step in L_a, step in L_a') forces v_p v'_p = 0 for every bit p, every v in
L_a, v' in L_a'. **The L_a must live on disjoint sets of bits.** Lines of a quadrangle through a point do not.
So inside this class the family is the answer up to the balance of atom sizes, and the class stops at t <= log2 k:
classes >= about N / k. Not run: a non-linear labelling of the quadrangle's flags (first size with a possible gain:
256 points, 128 classes against the family's 152; `verify.good` tests any candidate exactly).

## 5. Growth law and what it would have to combine with

- Law found: **V(k) <= 2 N log2(k)/k (1 + o(1)); E2(k) = N + O(N log k / k).** Lower bound known: 2 N^(3/4) (girth).
- For the transform: none. In ab-3's calculus [read] an atom is priced by gates per unit of codimension. Low-pass of
  cutoff 2 = read side + write side + N, now 3N + o(N) for 3 units: 1 N per unit. Coset sums: N/2 per unit. No gain.
  With the "one more degree" step: (2(d - 1) + 1) N for d + 1 units, tending to 2N per unit. Worse than coset sums.
- To bear on the order it needs degree d at o(d) N. Two helpers cannot do it beyond d about log2 k (the ceiling of
  line 5). So the idea must combine with one of: (i) outputs that are sums of r helpers with r growing slower than d
  (a hypergraph instead of a graph; nobody has stated its girth-type bound); (ii) the extra room of section 1: the
  family evaluates 2^t unrelated affine functions glued onto one quadratic for the price of one; aa-cross hybrid 2
  ("a piecewise affine straightening of the quadric needs sqrt(N)/2 pieces") is the place where glued affine pieces
  are the currency [guess: the two have not met].

## 6. Mutations

1. **Neither side forgets a fixed set.** Section 4 shows the wall is "P1 forgets the same bits everywhere". Search
   pairs of partitions into subcubes where both free sets depend on the point, at 64 points, target below 44.
2. **V_3(k) below N/2?** Smallest test: 64 and 128 points, anything below 56 and 108 classes.
3. **Label the affine quadrangle's flags non-linearly** at 256 points (128 classes).
4. **Three helpers.** Least classes of three partitions good for degree d; which d does 2N + o(N) reach?
5. **Use the room:** which functions beyond degree 2 does the family serve, and is quadric signs on a subcube one?
6. **Independent check of V(4) = 14** without the recalled theorem (exhaustive, small).

## 7. For the skeptics

- V(4), V(5) and every lower bound rest on a theorem I recalled and did not look up. The upper bounds do not.
- "N + o(N)" is slow: at 65,536 points the circuit has 1.48 N gates, at 2^64 points 1.15 N.
- The gate law above k = 16 comes from a count-only copy of the builder, not from built circuits.
- e_d <= d - 1 is derived, not built. The disjoint-support lemma of section 4 is derived, not run.
- I did not search the literature for "evaluating a quadratic form at all points of the cube"; the N + o(N) may be known.
- I read aa-cross sections 0 to 3 and ab-3 lines 255 to 300 only.

Files: `waves/wave-09/ad-6-twohelpers/` : verify.py, verify.out (exact test,
the family, the "one more degree" step); circuit2.py, circuit2.out (the degree-2 circuit, built and replayed);
law.py, law.out (count-only law, class table, girth bounds).
