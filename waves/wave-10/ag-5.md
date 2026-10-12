# ag-5 three-helpers: the first case is built (29 classes at 32 points, 61 at 64, 125 at 128), by choosing the kernel first; no growth law

11 October 2026, about 07:40 to 08:35 EDT, 60-minute box. Private. One agent; nothing reviewed, nothing in Lean, nothing published.
Marks: [ran] = run of mine tonight, whole numbers, files in `ag-5-threehelpers/`; [derived] = by hand tonight, checked by
nobody; [read] = from tonight's reports; [recalled] = from memory, no source opened; [guess].
Gate count where gates are mentioned: **(G)**, a gate is any a*u + b*v, scalings free. Most of this report counts classes, not gates.

**No circuit below a known count, no growth law below N log N for the transform, nothing of the 1e-1 kind. Nothing here
changes the order.** What is here: the first families where a third helper does what two provably cannot (one class, at
32 and at 64 points); the first bound beyond the rank for three helpers (it is tiny, and exact at 32 points); a way of
searching that works where the two obvious ones fail on known answers; and a derived recursion that says what a third
helper buys in classes (a lot) and in gates (nothing).

Words. N = 2^k cube points, an address is k bits. *Polynomials of degree at most d at all cube points*: one output per
address y, output(y) = sum of the inputs at the sets S of at most d bits contained in y. RM(d) = the space of these
tables, D = its dimension = number of sets of at most d bits. *Helper*: a wire several outputs read. A *class* of a
partition of the cube points is one helper. h partitions are *good for degree d* when every table in RM(d) is a sum of h
functions, one constant on the classes of each partition. V = *classes* = total over the h partitions. M = the *incidence
matrix*: N rows (outputs), V columns (classes), h ones per row. *Character* chi_S(y) = (-1)^(number of ones of y in S);
H_d = span of the characters with more than d bits = the functions whose moments up to degree d all vanish. *Flat*: a
subspace of addresses or a shifted copy. c_h(d) = the limit (it is non-increasing in k, section 5) of the least V/N for
h helpers at degree d; "o(N) classes" means c_h(d) = 0.

## 0. In ten lines

1. **Built [ran, exact, replayed from the files]: three partitions good for degree 3 at 32 points with 29 classes,
   good for degree 4 at 64 points with 61 classes, and good for degree 5 at 128 points with 125 classes.** Two helpers
   need 30 [read: ad-6, by girth], 62 and 126 [ad-6 has 62, and its step gives 64 + 62 = 126; one fewer is excluded by a
   count, derived here, section 4]. So the third helper buys exactly one class, N - 3 against N - 2, at three sizes.
2. **29 is the exact minimum for three helpers at 32 points** [derived bound + ran]: the new bound below gives 29.
3. **First bound beyond the rank for h >= 3** [derived, ten lines, section 3]:
   V >= (D + h - 2) * h 2^d / (h 2^d - 1). It beats the rank bound D + h - 1 by a factor 1 + 1/(h 2^d) only. It is not
   a ceiling. With INJECTIVITY (V >= h N^(1/h), section 1) it is all I have: nothing known forbids V = N^(1/3 + o(1))
   for three helpers at any fixed degree. **I found no bound of girth type for three helpers and I now think there is
   none of the counting kind** (section 3, last paragraph).
4. **How the families were found: kernel first** (section 2). Good for degree d is the same as: every function that sums
   to zero on every class has vanishing moments up to degree d. So choose that space K of functions first, inside H_d,
   and then look for partitions into classes on which K sums to zero. Annealing on partitions and greedy merging of
   classes both FAIL to find the known two-helper optima (controls); kernel-first finds the known 14 at 16 points and
   the new 29, 61 and 125 within a minute each (try 988, 1,468 and 193 of a random draw). It has one confirmed control
   out of two tried (section 2).
5. Three ways to say the problem that I did not find in tonight's reports [derived]: (a) the kernel K; (b) **a sumset**:
   the least V is the least |A_1| + ... + |A_h| such that A_1 + ... + A_h contains the N moment vectors
   m(y) = (all monomials of degree at most d at y); (c) RM(d) inside a sum of h subalgebras of the functions on the cube.
   (b) is where the classical field is: sumsets covering points of a curved set, incidence bounds (section 1).
6. **What the third helper buys in classes, derived (section 5):** c_h(h) = 0 and c_h(d) <= 1/2 + c_(2h-2)(d-1)/2.
   Two helpers: degree j + 2 with N (1 - 2^-j) classes. Three helpers: degree 2^j + j + 2 with N (1 - 2^-j) classes:
   degree 5 at N/2, degree 8 at 3N/4, degree 13 at 7N/8. The first step is checked exactly at its smallest size.
7. **In gates it buys nothing** [derived]: each route above costs d - 1 gates per point, the same slope 1 per degree as
   the textbook. Classes below N are not the currency. The only thing that would bend the slope is still:
   **degree above h with o(N) classes**, that is c_2(3) = 0 or c_3(4) = 0. Open; not touched by a search at 64 points,
   because the rank bound itself is above N/2 there (first size where c_3(4) < 1/2 could show: 1,024 points).
8. Answer to "does the degree per helper stay 1 when the classes are not flats": at 32 points the optimum uses only
   flats (pairs along one bit and 2-dimensional affine flats); at 64 and 128 points the families found use four-point
   classes that are not flats (16 of 35, 52 of 67); I do not know whether they are needed. At o(N) classes: no example
   either way, and no bound.
9. Walls named: KERNEL-MEASURE-ZERO (a random good family has trivial kernel and N + h - 1 classes; every class below
   that is one designed dependency) and, for the selector route to two helpers at degree 3, CIRCULAR-SELECTORS
   (section 6): two selector families must each be exponentially larger than the other.
10. Skeptics first: the bound of section 3; the exclusion of 61 for two helpers (uses a recalled extremal fact for
    graphs with four independent cycles); the recursion of section 5 (one case run, the rest derived).

## 1. Three ways to say "good for degree d" [derived]

**(a) Kernel.** Let K = the functions g on the cube with zero sum on every class of every partition (the left kernel of
M). The partitions are good for degree d **exactly when K lies in H_d**: every such g has all moments up to degree d
equal to zero. (Column space of M contains RM(d) iff its orthogonal complement lies in that of RM(d).) dim K = N - rank M
>= N - V + h - 1. For two helpers K is the cycle space of a graph and an element is a weighted solution of the
Prouhet-Tarry-Escott problem on the cube (two multisets of points with equal moments up to degree d).

**The necessary condition, corrected.** ae-cross's condition "fewer than 2^(d+1) outputs touch at least as many classes"
is necessary but is NOT the girth for two helpers: one cycle of length L touches L classes and passes the count, yet it
is a dependency. The right statement: **any fewer than 2^(d+1) rows of M are linearly independent** (a non-zero element
of H_d has at least 2^(d+1) non-zero values). The full condition, necessary and sufficient, is K inside H_d; the program
tests that exactly by rank (`balanced.py: missing`), and `verify_objects.py: hall_small` tests the counting form exactly
for sets of up to 7 outputs (no violator in any saved family).
Two consequences [derived]: on every flat of dimension at most d the rows are independent; on every flat of dimension
d + 1 there is at most one dependency, the parity of the flat.

**(b) Sumset.** Let m(y) be the vector of all monomials of degree 1 to d at y. Then
   least V = min { |A_1| + ... + |A_h| : A_1 + ... + A_h contains m(y) for every y },  A_i finite sets of vectors.
(Class of y in partition i = which element of A_i its representation uses; conversely a_i(class) = the h helper values of
all monomials.) For two helpers: the graph sits in space, every edge y is the translation m(y). Degree 1 is "cover the
cube by a sumset": h N^(1/h). In general the joint map y -> (class_1, ..., class_h) must be one-to-one as soon as d >= 1,
so **V >= h N^(1/h)** (INJECTIVITY). The classical neighbours [recalled, nothing read]: sumsets that contain many points
of a convex curve (Elekes, Nathanson, Ruzsa: (A + B) meets a convex curve in at most about (|A||B|)^(2/3) points, which
for |A| = |B| gives V >= N^(3/4), the same exponent as ad-6's girth bound for degree 2), and sum-product: written in
characters the N moment vectors form a group under entrywise product, and the question is how well a multiplicative
group is covered by an h-fold additive sumset. A set with no additive relations at all cannot be covered below N + h - 1.

**(c) Subalgebras.** The functions constant on the classes of a partition form a subalgebra of the functions on the
cube. Good for degree d: RM(d) lies in a sum of h subalgebras; V = sum of their dimensions.

**A negative that came for free [derived]: symmetric classes are far worse than flats.** If the classes of partition i
are the orbits of a group of coordinate permutations and bit flips (these keep the degree), each piece may be taken of
degree at most d, and counting invariants of degree d gives h >= b^d when the bits are permuted in blocks of b. So level
sets of block weights (the first non-flat classes one thinks of) need exponentially many helpers. What saves the
selector families is that their classes are NOT orbits of a degree-preserving group.

## 2. The first experiment: what failed, what worked

All exact checks: whole numbers, fraction-free elimination (`balanced.py: exact_rank`).
**Controls of the test** [ran, `tool.py check`, on the rented machine]: ad-6's family at 32 points (24 classes, good
for degree 2, 4 dimensions missing at degree 3) and ae-cross's three partitions (44 and 84 classes, ranks 29 and 57, good
for degree 3, not 4) are reproduced.

**Failure 1: annealing on partitions** (`tool.py anneal`, energy = distance of RM(d) from the column space, 150,000 to
350,000 steps a run). Control: two helpers, degree 3, 32 points, 30 classes (exists, ad-6): NOT found in three runs;
three helpers at 30 and 28 classes: not found; 64 points, degree 4, 63 classes: not found. Worthless as evidence.
**Failure 2: start from single points and merge classes while the family stays good** (`coarsen.py`). Control: two
helpers, degree 2, 16 points (optimum 14): ends at 17 = N + 1 in six runs of six; degree 3 at 32 points: 33 = N + 1.
*What the failure is made of* (KERNEL-MEASURE-ZERO): random merging ends where K = 0, which is V = N + h - 1. Every class
below that needs one new element of K, and it must fall in H_d, a subspace; a random merge never does it.
**Yes, and: choose K first.** Take K inside H_d by hand. A class is *K-balanced* when every g in K sums to zero on it.
Partitions into K-balanced classes automatically have K in their kernel; the family is good as soon as the rank of M is
N - dim K, and then V >= N - dim K + h - 1. (`balanced.py`, `balanced2.py`, `balanced3.py`: enumerate the balanced pairs
and the balanced 4-sets that contain no balanced pair, draw exact covers of the cube at random, compute the rank.)
Kernels tried: *top r* = parity times (1, x_1, ..., x_r), x_i = +-1 the i-th bit; these are the characters on all
bits and on all bits but one, so they lie in H_(k-2).

| points | degree | helpers | kernel | classes (sizes) | result [ran] | two helpers | rank bound | bound of section 3 |
|---|---|---|---|---|---|---|---|---|
| 16 | 2 | 2 | top 2 | 14 (8, 6) | found, try 119: **control, the known optimum** | 14 | 12 | 13 |
| 32 | 3 | 3 | top 3 | 30 (10, 10, 10) | found, try 39 | 30 | 28 | 29 |
| 32 | 3 | 3 | top 4 | **29 (8, 10, 11)** | found, try 988; exact check: 0 missing at degree 3 | 30 | 28 | 29 |
| 64 | 4 | 3 | top 2 | 63 (21, 21, 21) | found, try 8 | 62 | 59 | 60 |
| 64 | 4 | 3 | top 3 | 62 (20, 21, 21) | found, try 125 | 62 | 59 | 60 |
| 64 | 4 | 3 | top 4 | **61 (19, 20, 22)** | found, try 1,468 of the second split; three other splits: no (1,500 tries each) | 62 | 59 | 60 |
| 64 | 4 | 3 | top 5 | 60 | NOT found; see the note under the table | 62 | 59 | 60 |
| 64 | 3 | 3 | characters containing bits 1, 2 (11) or bit 1 (16) | 55, 50 | NOT found: best ranks 48 of 53 and 32 of 48 in 200 tries | 56 | 44 | 45 |
| 128 | 5 | 3 | top 3 | 126 (42, 42, 42) | found, try 79 | 126 | 122 | 123 |
| 128 | 5 | 3 | top 4 | **125 (41, 42, 42)** | found, try 193; exact check: 0 missing at degree 5 | 126 | 122 | 123 |
| 128 | 5 | 3 | top 5 | 124 | NOT found: best rank 117 of 122 in 20 tries, first generator only | 126 | 122 | 123 |

Files of the three best: `best_k5_d3_29classes.txt`, `best_k6_d4_61classes.txt`, `best_k7_d5_125classes.txt`; replay
from the files alone on this machine: `verify_objects.py`, output `verify_objects.out` (partitions of the cube: yes;
ranks 27, 59, 123; missing 0 at degree d and 4 at degree d + 1; class sizes 2 and 4 only).
Note on 60 at 64 points: with top 5 the only balanced pairs are the 32 pairs along the last bit, and my first generator
let two partitions use the same pair (two equal columns), which costs rank: best 55 of 58 in 6,000 tries. With that
forbidden (`balanced3.py`, `runs9.out`) the best rank is 57 of 58, one short, in 31 families drawn (60 tries, 29 without
a cover). 60 is open, and it equals the lower bound.
Not reproduced: the second control (two helpers, degree 3, 32 points, 30 classes) with kernel top 2 and classes 16 + 14
(best rank 28 of 29 in 300 tries). The known family may have another kernel or another class profile; I did not look.
Also not reproduced with kernel-first: ad-6's two-helper 62 at 64 points. So kernel-first with my two class shapes is a
tool with one confirmed control, not a complete search; every NOT above is "not found", never "none".

What the objects look like [ran]. At 32 points all 29 classes are flats: 10 pairs along one bit and 19 affine flats of
dimension 2. At 64 points: 26 pairs along one bit, 35 four-point classes of which 19 are flats and 16 are not.
At 128 points: 58 pairs (49 along one bit), 67 four-point classes of which 15 are flats. So away from the smallest size
the families found are mostly NOT made of flats; whether flats alone reach the same counts was not tried.

## 3. The first bound beyond the rank for three helpers [derived]

**Claim.** If h partitions with V classes are good for degree d on N = 2^k points, then
   V >= (D + h - 2) * h 2^d / (h 2^d - 1).
Proof. The column space U of M has dimension at most V - (h - 1) (each partition's columns add up to the all-ones
vector) and contains RM(d). Write U = RM(d) + E with E = U intersected with H_d; dim E <= e := V - h + 1 - D. Every class
indicator is (a polynomial of degree at most d) + (an element of E). Take any e + 1 classes of ONE partition: their
E-parts are dependent, so some non-trivial combination of their indicators is a polynomial of degree at most d; it is not
zero (the classes are disjoint), and a non-zero polynomial of degree at most d is non-zero on at least 2^(k-d) cube
points. So the e + 1 smallest classes of a partition hold at least 2^(k-d) points together; they hold at most
(e + 1) N / V_i. Hence V_i <= (e + 1) 2^d for each i, V <= h (V - h + 2 - D) 2^d, which is the claim. QED
Values: 29 at (h, d, k) = (3, 3, 5), met by the family found, so **the least number of classes for three helpers at
degree 3 on 32 points is exactly 29** [derived + ran]. 60 at (3, 4, 6): found 61. 45 at (3, 3, 6). 123 at (3, 5, 7).
The extreme case e = 0 is clean: then every class indicator is itself a polynomial of degree at most d, so every class
has at least 2^(k-d) points and V <= h 2^d.

**Why I think no bound of girth type exists for three helpers.** For two helpers a dependency is forced to be SMALL
(a graph with more edges than vertices has a short cycle), and small dependencies are forbidden; that is the girth bound.
For three helpers the forced dependencies can all be large: ae-cross's remark [recalled there: Gallager] is that
parity-check matrices with three ones per column have codes of distance proportional to N. What replaces girth is not a
count but a containment, K inside H_d, and the only general consequence I could extract is the factor 1 + 1/(h 2^d)
above. For fixed d it leaves room down to the larger of D (which is about (log N)^d) and h N^(1/h). The obstruction, if there is one, is structural
(which spaces K of codimension o(N) inside H_d have enough balanced classes), not a Moore-type count.

## 4. Why two helpers cannot do 29 or 61 [derived; uses one recalled fact]

Two helpers: K is the cycle space of a graph with N edges and V vertices; no cycle shorter than 2^(d+1). V = N - 3 (29 or
61) means at least 4 independent cycles. A graph with 4 independent cycles and no cycle shorter than g has at least
9 g / 4 edges [recalled; the extremal graph is the complete two-sided graph on 3 + 3 vertices with every edge stretched:
9 four-cycles, each edge in 4 of them; I checked the prism by the same double count (5 g / 2) and not the skeletons with
repeated edges]. With g = 16: 36 > 32. With g = 32: 72 > 64. With 3 independent cycles the count is 2 g = N exactly (the
complete graph on 4 vertices, every triangle of length exactly g), which is why 30 and 62 are possible and tight.
With g = 64: 144 > 128. So at the top degree d = k - 2: two helpers N - 2, three helpers N - 3 at 32, 64 and 128
points; the bound of section 3 is N - k + 2. Whether three helpers follow N - k + 2 further (60 at 64 points, 123 at 128)
or stay at N - 3 is the open cell of the table. [guess] N - 3 may be the truth for this family of kernels: "top 5"
leaves only the pairs along one bit, and three partitions cannot all live on them.

## 5. Growth laws: what a third helper buys in classes, and why it buys nothing in gates [derived]

**Products.** A good family on g bits is good on k > g bits with the same V/N (keep the new bits in every class). So the
least V/N is non-increasing in k and c_h(d) is its limit.
**Selectors (the known step, restated for h).** P_1 forgets t selector bits a; on each value of a the other h - 1
partitions are a family good for degree d - 1 on the remaining bits. Proof: q(a, y) - q(0, y) has degree at most d - 1
in y. So V_h,d(k) <= 2^(k-t) + 2^t V_(h-1),(d-1)(k - t) and, with ad-6's V_2,2 = o(N), **c_h(h) = 0** for every h >= 2.
**Halving (ad-6's "one more degree per bit", for h helpers).** P_1 forgets one bit a. Let S_1, ..., S_(2h-2) be 2h - 2
partitions good for degree d - 1 on the other bits; use h - 1 of them on the half a = 0 and the other h - 1 on the half
a = 1. With q = q_0 + a q_1 and q_1 = sum of s_j(S_j): P_1 carries q_0 + (the first h - 1 terms), the half a = 0
subtracts them, the half a = 1 adds the others. So
   **V_h,d(k) <= N/2 + V_(2h-2),(d-1)(k - 1),   c_h(d) <= 1/2 + c_(2h-2)(d - 1) / 2.**
[ran, smallest case, `verify_objects.py` last line: h = 3, d = 3, k = 5 from "forget bit 0, forget bit 1, forget bit 2,
one class" on the 4-cube: 41 classes, 0 missing at degree 3, 1 missing at degree 4.]
For h = 2 the number of helpers does not grow (2h - 2 = 2): degree j + 2 with N (1 - 2^-j) + o(N) classes (ad-6).
For h = 3 it doubles: 3, 4, 6, 10, 18, ..., 2^j + 2. So **three helpers reach degree 2^j + j + 2 with
N (1 - 2^-j) + o(N) classes: c_3(5) <= 1/2, c_3(8) <= 3/4, c_3(13) <= 7/8.** Degree d costs a fraction about 1 - 1/d of
N in classes, against 1 - 4 / 2^d for two helpers. This is the precise sense in which ae-cross's "the ceiling is special
to two" is true, on the side of constructions.
**Gates.** Evaluate the half a = 0 recursively and the half a = 1 as q_0 + (2h - 2 helper terms):
e_d = e_d / 2 + (h - 1) + o(1), so e_d = 2h - 2 gates per point for the degree that 2h - 2 helpers reach plus one,
i.e. again **d - 1 per point**. Every route I can build costs one N per degree. Classes below N do not lower the gate
count: gates per point = number of helper terms an output adds up, plus the cost of the helpers; a family with V = cN
only moves cost into the helpers.
**Growth law for the brief's ladder: none.** c(d) = d - 1 + o(1) by every construction here; c(d) = o(d) needs a family
with o(N) classes whose degree exceeds its number of helpers. First open cases: c_2(3) = 0? c_3(4) = 0?
A size remark that kills small searches for these: the rank bound D + h - 1 is above N/2 for (d, k) = (3, up to 7) and (4, up to 9). A
three-helper family for degree 4 below N/2 classes cannot exist under 1,024 points; for two helpers at degree 3 below
N/2, under 256 points.

## 6. Two helpers, degree 3, by selectors: the condition and where it circles [derived]

Shape: P_1 forgets t selector bits a; P_2 on the face a is a partition R_a of the other bits. Exact condition, monomial by
monomial: for every set A of selector bits and every monomial y^T with |T| <= d - |A|,
y^T lies in U(join of the R_a with a not containing A) + U(join of the R_a with a containing A), where U(.) = functions
constant on the classes and *join* = the finest partition coarser than all. (This contains ad-6's necessary condition on
"joins" and shows it is sufficient when taken for all A.) For d = 3 and one selector bit i it says: the two joins over
the faces a_i = 0 and a_i = 1 form a pair good for degree 2.
Try: let each of these pairs be ad-6's own pair (forget a selector set S_i / forget an atom chosen by S_i) and take R_a =
the common refinement. For R_a to have few classes on every face, the forgotten sets must overlap on every face, which
needs bits of S_1 inside the atoms of the second pair for most of its 2^|S_2| selector values, and the same with 1 and 2
exchanged: |S_1| >= about 2^|S_2| and |S_2| >= about 2^|S_1|. Impossible (CIRCULAR-SELECTORS). Giving up one face of four
brings back N/2 + o(N), ad-6's number. So with two selector bits and pairs of ad-6's kind, 1/2 is not beaten.
Yes, and: what this failure is made of is ad-6's COORDINATES wall (forgotten sets on disjoint coordinates). The classes
found in section 2 at 32 points are affine flats along directions that are NOT coordinate sets; a pair good for degree 2
whose forgotten directions are general subspaces is exactly what the circle needs and is a search at 64 points with the
kernel-first tool (two helpers, degree 2, below 44 classes; ad-6's V(6) is between 40 and 44).

## 7. Mutations

1. **Kernel-first at degree 2 with two helpers, 64 points, below 44 classes** (ad-6's open V(6)): K = a space of
   dimension 22 to 25 inside H_2 spanned by parities of 3-dimensional flats that are not coordinate subcubes.
2. **A family of kernels that grows**: "top r" lives at degree k - 2 only. The same idea one level down: K = (a fixed
   character on k - j bits) times (functions of bounded degree in the signs of r chosen bits). Which (j, r) keep
   balanced classes of 2 and 4 points?
3. **Sumset literature**: read what is known on covering a set with few additive relations by a three-fold sumset
   (the cube's moment vectors have relations only of size 2^(d+1) or more); an incidence bound for three-fold sumsets
   and "curved" point sets would be the ceiling the brief asked for, if one exists.
4. **60 at 64 points and 123 or 124 at 128 points**: does the third helper follow the bound N - k + 2 at the top degree?
   Needs classes of 6 points in the generator.
5. **Exhaustive at 32 points for two helpers at degree 3 inside kernel-first** (to repair the second control).
6. **Selectors with general directions** (section 6) for c_2(3) < 1/2.

## 8. Criticism, last

- The two families are at the TOP degree (d = k - 2), where classes are N minus a constant. They say nothing about o(N).
  They are a first case, as the brief asked, and one class is all the third helper buys there.
- "Two helpers cannot do 61" rests on a recalled extremal fact and a sketch; ad-6's 62 I read and did not replay.
- The bound of section 3 is ten lines by hand. Its use of "a non-zero polynomial of degree at most d has at least
  2^(k-d) non-zero values on the cube" is standard [recalled].
- Section 5 is derived; only its smallest instance was run. c_h(h) = 0 uses ad-6's unreviewed V_2,2 = o(N).
- The classes-versus-degree law of section 5 looks strong and is worth nothing in gates. I report it because it is the
  exact content of "three helpers are different from two", and so that nobody takes classes below N for a saving.
- Kernel-first is one confirmed control out of two tried; every negative in the table is a failure to find.
- I did not open the sumset or incidence literature; the parallels in section 1 are from memory.
- Nothing here changes the order, or any constant of the transform.

## 9. Last runs

- 64 points, degree 4, 60 classes (kernel top 5, no class shared by two partitions): rank 57 of 58 at best (`runs9.out`).
  A longer run of the same (2,500 tries a split) was stopped by me before it printed anything; it is not evidence.
- 128 points, degree 5 (`jobE.out`, rented machine, replayed here for the 125): 126 found, **125 found**, 124 not found
  (20 tries with the generator that lets partitions share a pair; not a serious attempt).
- Slip to know about: my first table for 32 points used three fours too few per family (`runs5.out`: 33, 32, 31 classes,
  all good, none below the kernel's own count); `runs7.out` has the right counts. `runs6.out` (128 points on this
  machine) asked for 123 classes with a kernel that allows 124 and is void.

Files: `waves/wave-10/ag-5-threehelpers/` : `tool.py` (exact test, annealer,
controls; needs numpy, ran on the rented machine), `coarsen.py` (merging search), `balanced.py`, `balanced2.py`,
`balanced3.py` (kernel-first), `verify_objects.py`, `verify_objects.out` (replay of the saved families and the halving
lemma), `best_k5_d3_29classes.txt`, `best_k6_d4_61classes.txt`, `best_k7_d5_125classes.txt`, `k6_d4_62classes.txt`,
`runs1.out` to `runs9.out` (runs8.out holds a header only: stopped), `jobA.out` to `jobE.out` (remote runs, copied back; A and B
are the annealer), `rsh.sh` (the ssh line).
