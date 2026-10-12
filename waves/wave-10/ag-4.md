# ag-4: the cheapest generator of the half-rate space of low-degree polynomials

> Editor's note (11 October 2026): a critic corrected one bound of this report. Its floor "T(N) >= (3/2) N" for the transform is below a count of two lines, 2N − 2 ([ai-1](ai-1.md)).

11 October 2026, about 07:40 to 08:30 EDT, inside a 60-minute box. Private. One agent; nothing reviewed, nothing in Lean,
nothing published. Idea: ae-cross hybrid 3 and WAVE10-PICKS section 5. I am this idea's friend; the criticism is last.
Marks: [ran] = run of mine tonight (files in `ag-4-cheapestgenerato/`); [derived] = by hand tonight, checked by nobody;
[read] = from a file or a web page opened tonight; [recalled] = from memory; [guess].
Gate count everywhere: **(G)**, a gate is any a*u + b*v, scalings and copies free. Count (O) is not used.

**No circuit below a known count, no growth law below N log N. Nothing here changes the order. The route "cheap space,
therefore cheaper transform" is closed by an identity (section 4). What is new is a floor lemma (section 3), the exact
answer at 8 points, and one object, the "majority mirror" (section 4).**

Words. N = 2^k points; an *address* is k bits; *weight* = number of ones. *Character* of x: the function
y -> (-1)^(x.y). *The space* S_k (k odd): span of the characters of weight at most (k-1)/2 = all polynomials of degree at
most (k-1)/2 in the address bits, as tables of N values; dimension N/2. *Generator*: a circuit on n free inputs whose N
outputs, as the inputs vary, fill exactly the space (n = its dimension). *Dual distance* d of a space: the least number
of outputs that satisfy a linear relation on the whole space; for polynomials of degree at most r it is 2^(r+1)
[derived: induction on k, six lines; the classical fact over two elements holds over the rationals]. *Hidden wire*: a
wire of the circuit that is not an output. T(N): least gates for the transform H.

## 0. In ten lines

1. **8 points: the least over ALL generators is exactly 6 gates** (the brief asked: between 4 and 6). Proof in three
   lines [derived], and exhaustive search modulo 3, 5 and 7 [ran]: none with 5, exactly 30 with 6 for each prime.
2. 16 points, degree at most 1: no generator with 13 gates modulo 3 [ran, exhaustive modulo 3 only]; 14 = N - 2 is known.
3. **A generator is a geometric object**: n + G points containing the N "cube points", each non-input on a line through
   two earlier ones. The gates sort by how many hidden wires they touch, and that gives a floor:
4. **Floor lemma [derived]. If the dual distance is at least 5, every generator has at least N - n/2 gates** (n = the
   dimension). For the half-rate space, k >= 5: **at least (3/4) N**, not N/2. For the transform itself: T(N) >= (3/2) N
   for N >= 8. With an unproved graph step the half-rate floor rises to N - o(N) [guess]. All of this is linear.
5. Best known generator [ran, built and replayed exactly at 32 and 128 points: 50 and 308 gates]: per point
   (k - 0.80 sqrt k)/2, against (k - 0.48 sqrt k)/2 for the monomial encoder. The freedom of basis saves a term of order
   sqrt(log N) per point and nothing in the leading term. So **g(N) is between 3/4 and (log2 N - 0.80 sqrt(log2 N))/2**.
6. **The even-weight points are an information set, and the interpolation is a mirror** [ran k = 3, 5, 7; derived]:
   S_k = { (u on the even points, M u on the odd points) }, M orthogonal, M^2 = 1, entries a function of distance only,
   and M = (half-size transform) x (sign of the MAJORITY function) x (inverse half-size transform). Every polynomial of
   degree below k/2 has the same energy on the even and on the odd points.
7. **The change of basis is a half-size transform, identically** [derived]: for EVERY generator A, with U its part on
   the even points, (change of basis to the characters) = 2 H_{N/2} U. And H_N = diag(1, M) (H_2 x H_{N/2}).
8. So the brief's law reads T(N) <= 2 T(N/2) + N + cost(M): the space's cost enters only as an additive term, where the
   textbook has cost 0 (its M is a relabelling). **Whatever g(N) is, this route does not change the order.**
9. Where the logarithm sits in the best known generator [ran]: in gates that touch three hidden wires and no output
   (20 of 50, 182 of 308, 1164 of 1674). A linear-size generator would need O(N) of those.
10. Skeptics first: the floor lemma (section 3, eight lines); the identity of line 7; the 13-gate "no" is modulo 3 only.

## 1. What was run

| what | result | file |
|---|---|---|
| 8 points, degree <= 1, all generators, 4 gates (no hidden point) | none; p = 3, 5, 7 | `rig8.out` |
| same, 5 gates (one hidden point; 32, 148, 392 candidates) | none; p = 3, 5, 7 | `rig8.out` |
| same, 6 gates (two hidden points; 496, 10,878, 76,636 pairs) | 30 for each prime | `rig8.out`, `rig8_p7_all.out` |
| 16 points, degree <= 1, 13 gates (two hidden points, 5,460 pairs) | none, p = 3 | `rig16_p3_h2.out` |
| 16 points, degree <= 1, 14 gates, the search with three hidden points | stopped at 400 s, no answer; 14 is known from ae-cross | `rig16_p3_h3.out` |
| best known generator built and replayed in whole numbers | k = 3, 5, 7: 6, 50, 308 gates; outputs orthogonal to every character of weight above k/2; rank N/2 (modulo 1000003, which can only underestimate) | `build.py`, `build.out` |
| the mirror M, fractions | k = 3, 5, 7: all statements of line 6 true | `mirror.py`, `mirror.out` |
| H_N = diag(1, M) (H_2 x H_{N/2}); change of basis = 2 H_{N/2} U | true on every entry, k = 3, 5, 7 (U random at k = 3, 5) | `identity.py`, `identity.out` |
| growth of the known generators | k = 3 to 41 | `table.py`, `table.out` |

The search program `rig.py` uses the reformulation of section 2 and is exhaustive modulo p; a "none" is a statement
modulo that prime. At 8 points the "none" is also proved over every field of odd or zero characteristic (below).

**The 30 generators with 6 gates at 8 points** [ran, p = 7, classified]. The two hidden wires are, as points of space:
two edge directions (3); an edge direction and a face-diagonal direction (12); an edge direction and the centre of a
face (6); an edge direction and the centre of the cube (3); the centre of the cube and the centre of a face (6).
"Direction" means a difference f(y + e) - f(y); "centre" means a half-sum such as (f(y) + f(opposite y))/2.
The count 30 is the same for p = 3, 5, 7, so I take it as the count over the rationals [guess].

## 2. The reformulation: a generator is a rigging of the cube

[derived] Fix the space S of dimension n. Each output is a linear function on S, that is a point of the projective space
of dimension n - 1; for degree at most 1 these are the 8 or 16 corners of a cube, for higher degree the corners after the
map y -> (all monomials of degree at most r at y). A circuit with n inputs and G gates is a set of n + G points that
contains those N points and can be built from n of its points by adding, one at a time, a point on the line through two
points already present. Each gate is one collinear triple. The points that are not outputs are the hidden wires; there
are h = G - (N - n) of them, so **gates = (N - n) + hidden wires**: the whole question is how few hidden wires suffice.

8 points, proof of "exactly 6" [derived]. No three corners of a cube are collinear, so every gate uses a hidden point.
With 5 gates there is one hidden point w, every gate is a line through w and two corners, two such lines share only w,
and 5 lines need 10 corners. So at least 6; ae-cross's generator has 6.

## 3. The floor lemma

Setting. A circuit with n inputs, G gates, N outputs filling a space S of dimension n. Let C be the relations among the
outputs (the vectors orthogonal to S); assume every output occurs in some relation and the dual distance d is at least 5.
Each gate is one relation among three wires. [derived] The relations among all wires are exactly the combinations of
the G gate relations, and C is the set of those combinations in which every hidden wire cancels.

*Step 1.* If a set F of gates touches fewer hidden wires than it has gates, some combination of F cancels all of them,
so C contains a relation among the outputs that F touches. Hence F touches at least d outputs.
*Step 2.* A gate with no hidden wire would be a relation among 3 outputs: none exists. Two gates that each touch one and
the same single hidden wire would give a relation among at most 4 outputs: so each hidden wire belongs to at most one
gate of the kind (one hidden wire, two outputs). Call their number t1; t1 <= h. Every other gate touches at most one
output.
*Step 3.* Every output is touched by some gate. So N <= 2 t1 + (G - t1) = G + t1 <= G + h = 2G + n - N.
**Hence G >= N - n/2.**

Checks. Single relation on N outputs (n = N - 1): the lemma gives (N + 1)/2, the truth is N - 2. Degree at most 2
(ad-6's N + o(N)): the lemma gives N - n/2, consistent, and shows that ad-6's count is the floor up to its o(N).
The built generators satisfy both inequalities [ran: 32 <= 56, 128 <= 240, 512 <= 992].

Consequences [derived].
- Half-rate space, k >= 5 (dual distance 2^((k+1)/2) >= 8): **G >= (3/4) N**. At 32 points: at least 24, known 50.
- The transform. Take as "outputs" the N inputs and the N outputs of a circuit for H together: they fill the graph of H,
  a space of dimension N in 2N coordinates. A relation among them is a vector x together with its transform, and
  [recalled: the uncertainty inequality for finite groups] (non-zero entries of x) times (non-zero entries of Hx) is
  at least N, so the dual distance is at least 2 sqrt N >= 5 for N >= 8. The lemma gives **T(N) >= (3/2) N**. Linear, harmless.
- [guess, with a sketch] If d grows faster than (log N)^2, the gates that touch one or two hidden wires form a graph on
  the hidden wires in which no connected piece with fewer than d/2 edges has two cycles, so they number at most
  (1 + o(1)) h, and then G >= (3/2) N - n - o(N): N - o(N) at half rate, (3/2) N - o(N) for degree between 2 log2 k
  and k/2 - sqrt k. The step I did not prove: a graph with h vertices and (1 + e) h edges has a connected piece with
  two cycles and O(log h / e) edges. The one-cycle version is a theorem of Bollobas and Szemeredi (2002) [read tonight
  in two papers that quote it, not in the original]. If the step holds, **ad-6's "N + o(N) per rung" cannot continue
  beyond degree about 2 log2 k**: the price of the low-degree end rises to (3/2) N there. Still linear.
- What the lemma cannot do: gates that touch three hidden wires cost nothing in it. A floor above linear would have to
  bound those, and that is the general open problem of lower bounds for linear circuits [recalled].

## 4. The mirror, and the identity that closes the route

Let E be the even-weight points and O the odd ones, X the characters of weight at most (k-1)/2.

Facts [ran k = 3, 5, 7, fractions; each also derived].
- A polynomial of degree below k/2 that vanishes on E is zero: f times (1 + parity) would have its spectrum both low and
  high. So **E is an information set**: the N/2 values on E are free and determine the rest.
- The characters of X restricted to E form a Hadamard matrix of order N/2: it is the transform of the group E, because
  x and its complement give the same character of E and X holds exactly one of each such pair.
- The interpolation matrix M (odd values from even values) is orthogonal; relabelled by y -> y + e_1 it is symmetric
  with M^2 = 1, and its entries depend only on the distance. Kernel by distance: k = 3: 1/2, -1/2 (distances 1, 3);
  k = 5: 3/8, -1/8, 3/8; k = 7: 5/16, -1/16, 1/16, -5/16. Every entry is non-zero.
- **M = H' D H'^-1**, H' the transform on k - 1 bits, D = the sign -1 on the frequencies of weight at least (k+1)/2
  and +1 below: the majority function, ties to +. Equivalently M = 1 - 2 (projection onto the high characters of the
  (k-1)-cube); trace 2, 6, 20 as predicted.
- Since S_k and its orthogonal complement are exchanged by the parity sign, energy on E = energy on O for every f in S_k.

The identity [ran on every entry at k = 3, 5, 7, and the change of basis with a random U at k = 3 and 5, fractions,
`identity.out`; derived for every odd k]. Order the points as (E, O) and the frequencies as (X, complements). Then
**H_N = diag(1, M) (H_2 x H_{N/2})**. And for any generator A of S_k, with U = its N/2 x N/2 part on E:
A = (U ; M U), and the change of basis from A's inputs to the characters is H[X, .] A = 2 H' U.

What it says about the brief's two numbers.
- b (the change of basis): for the generator with inputs = values on E it is exactly the half-size transform. For any
  other generator it is 2 H' U, and a transform built from that generator has to undo U again: U cancels identically.
  **The price of leaving the generator's basis is always one transform of half the size.**
- g (the space): cost(space) <= cost(M) <= 2 T(N/2); and cost(M) <= cost(A) + cost(U^-1) for every generator A.
- T(N) <= 2 T(N/2) + N + cost(M) by this route; the textbook is the same line with the majority replaced by one
  frequency bit (then M is a relabelling, cost 0). **So the half-rate space is the textbook recursion with a dearer
  middle term. It is k-cross's L1 (a conjugation: half a transform in, half out) once more.**
- The family behind it: every sign pattern D on the half-size frequency cube gives such a splitting; one frequency bit
  gives the textbook, the majority gives the half-rate Reed-Muller code. The space is cheap exactly when the
  conjugated sign H' D H'^-1 is.

## 5. Growth law

[ran, `table.out`] Gates per point of the half-rate space, k odd. "space" = split on one bit, f = (u, u + v), with both
ends free (degree 0: copies; full degree: outputs are inputs) and the exact ends N - 2 at degree 1 and k - 1.
"mono" = the same recursion for the matrix in the monomial basis.

| k | N | space | space/N | mono | mono/N | floor 3N/4 |
|---|---|---|---|---|---|---|
| 3 | 8 | 6 (exact least) | 0.75 | 7 | 0.875 | 6 by proof |
| 5 | 32 | 50 | 1.5625 | 57 | 1.78 | 24 |
| 7 | 128 | 308 | 2.41 | 346 | 2.70 | 96 |
| 9 | 512 | 1674 | 3.27 | 1861 | 3.63 | 384 |
| 21 | 2^21 | | 8.65 | | 9.33 | 0.75 |
| 41 | 2^41 | | 17.93 | | 18.97 | 0.75 |

space/N = (k - c sqrt k)/2 with c = 0.866, 0.838, 0.827, 0.820, ... 0.803 at k = 41 (it looks like it tends to
sqrt(2/pi) = 0.798 [guess]); mono/N has c = 0.72 falling to 0.48. **Both are (1/2) N log2 N to leading order.**
b(N/2) = T(N/2) exactly (section 4). Law by this route: T(N) = 2 T(N/2) + O(N) + cost(M), no better than the textbook.

## 6. "Yes, and": four turns

1. *The monomial matrix is dear; free the basis.* Done: ends free. Saves 0.16 sqrt k gates per point, leading term
   untouched. What the failure is made of: the split on one bit halves the problem and keeps both halves near half rate
   for k - O(sqrt k) steps.
2. *Then do not split on a bit; take another information set.* The even points: the generator becomes one orthogonal
   matrix M. Its cost by the transform is 2 T(N/2); by its own rank form (1 minus twice a projection of rank about N/4)
   it needs an orthonormal generator of the high band on k - 1 bits and its transpose, which adds about 3/4 of a gate
   per point for each bit instead of 1/2 [derived, a rough count, no circuit built]: dearer.
3. *Then let the generator be a pair of cheap convolutions.* S_k is a free module of rank one over the group algebra of
   E, so every pair (a, b) with (transform of b) = (majority sign) x (transform of a) and a invertible gives the generator
   u -> (a * u, b * u). Then a + b is a low-degree polynomial and a - b is orthogonal to all of them, so their supports
   have at least sqrt(N/2) points: sparse kernels are out [derived]. Kernels built from O(1) subspace indicators are out
   too: the majority is constant on no flat of small codimension. This is ae-cross's wall STEP in a new place.
4. *Then read the floor lemma backwards.* Its equality case says what a generator of about (3/2) N gates must look like:
   the outputs sit one each on the edges of a graph on the hidden wires that is almost a forest, and about N/2 gates
   among hidden wires close the relations. Each relation of the dual is then a "tripod": three paths of that forest,
   along which its entries follow a fixed profile. The lightest dual words here are the faces of dimension (k+1)/2 with
   alternating signs, and such a face IS a path with alternating signs if the forest walks it in Gray-code order.
   **Question this leaves: is there a tree whose edges are the N cube points in which N/2 independent alternating faces
   of dimension (k+1)/2 are each a path or a tripod?** In reflected Gray order only about sqrt(N/2) faces are. I did not
   get further. A yes would be a generator of the space in about (3/2) N gates; by section 4 it would make the majority
   mirror cheap only if the part U is cheap to invert, and it would not by itself move T.

## 7. Literature [read tonight: search summaries only, the papers were not opened]

- No result found on a linear-size encoder for Reed-Muller codes, nor a lower bound for one; the standard encoder is
  the N log N one (Kronecker power of a 2 x 2 triangular matrix with rows selected by weight).
- Exact lower bounds for encoding circuits of Hamming and Hadamard codes over two elements: arXiv 1804.09903 (2018).
- Encoders of good codes in bounded depth, upper and lower bounds on wires: Gal, Hansen, Koucky, Pudlak, Viola
  (quoted in arXiv 2402.00378).
- Capacity-achieving codes with linear-size encoders of inverse-Ackermann depth: arXiv 2512.11443 (December 2025).
- Girth of graphs with n vertices and n + k edges, at most (2(n + k)/(3k)) (log k + log log k + 4): Bollobas and
  Szemeredi 2002, as quoted in arXiv 2311.12302 and 2210.12243.
- [recalled, ae-cross] Spielman 1996: codes with linear-size encoders exist. Those codes are built for it.

## 8. What to try next (only what bears on a growth law)

1. **The tree of faces** (turn 4): for k = 5, search trees or sparse graphs on about 32 hidden wires, one output per
   edge, plus 16 gates among hidden wires, whose outputs fill S_5; the target is fewer than 50 gates, the proved floor
   is 24 (the true least is probably well above it: with dual distance 8 the marked hidden wires must be far apart
   [guess, not counted]). The law to look for: do the gates that touch three hidden wires stay O(N) as k grows.
2. **The sign family**: for which sign patterns D on the frequency cube is H' D H'^-1 cheap? Characters: cost 0.
   Quadratic signs: about one transform. Majority: unknown, at most two transforms. A pattern D that is not a function
   of few flats and still has a cheap conjugate would be the first counterexample to wall STEP.
3. **Prove or kill the graph step of section 3**; with it, the price of ad-6's ladder is pinned between N and (3/2) N
   up to degree log2 k and at least (3/2) N beyond.
4. The order of T by this family of routes is the question whether two half-size transforms on unrelated data cost
   less than twice one. Nothing in the space S_k touches that; j-manyatonce is where it lives.

## 9. Criticism, last

- The floor lemma is eight lines by hand, checked by nobody. Its numbers are linear: it cannot bear on the bar.
- "Exactly 6" at 8 points is proved; "14" at 16 points has its lower half modulo 3 only, and the run meant to exhibit
  14 by search did not finish (ae-cross's 14-gate generator stands).
- I did not anneal at 32 points, as the brief asked: the box went to the lemma and the mirror. The number 50 is the
  split-on-a-bit generator, replayed exactly; nobody has searched below it.
- The (3/2) N floor for large dual distance rests on an unproved graph step; it is marked a guess.
- The mirror facts are run at k = 3, 5, 7 and derived for all odd k; the derivation uses only that the characters are
  orthogonal and that complementing a frequency multiplies its character by the parity. The identity of section 4 is
  short and makes the idea, as a route to a faster transform, a relabelling of the textbook: the sixth or seventh time
  tonight that a reorganisation ties exactly.
- "Sparse kernels are out" and "flat kernels are out" in turn 3 are derived in a few lines each and exclude only
  translation-invariant generators.
- I found nothing that speaks for linear size. What is left is one concrete search (the tree of faces) whose success
  would give a linear-size generator of the SPACE, and section 4 says why that alone would not move the transform.

Files: `waves/wave-10/ag-4-cheapestgenerato/` : rig.py (exhaustive search over
generators modulo p for degree at most 1), rig8.out, rig8_p7_all.out, rig16_p3_h2.out, rig16_p3_h3.out (timed out);
build.py, build.out (the 6, 50, 308, 1674-gate generators, replay and gate types; the 1674-gate one is counted, not
replayed); mirror.py, mirror.out; identity.py, identity.out; table.py, table.out.
