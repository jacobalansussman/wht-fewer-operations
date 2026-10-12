# ad-1-linesums: all line sums of the finite plane, priced with free coefficients

11 October 2026, 06:22 to 07:08 EDT, one agent, 60-minute box. Private. Nothing reviewed, nothing in Lean, nothing published.
Marks: [ran] = run of mine this hour (files in `ad-1-linesums/`, whole numbers or exact arithmetic modulo a power of 2 unless a
line says floats); [derived] = by hand this hour, checked by nobody; [read] = from tonight's reports; [recalled] = memory; [guess].
Gate count everywhere: **(G)**, a gate is any a*u + b*v, scalings free.
Read: aa-cross in full, d-1 in full, brief 2 of WAVE9-PICKS, the two aa-cross spread scripts, j-machine's steiner.py.
Not read: ab-0, ab-3 (only as aa-cross quotes them), the skeptics' notes.

**No circuit below a known count. No growth law below N log N. The line sums were not priced below "log N gates per point"
by any construction, and section 1 says why they cannot be an easier problem than the transform. Nothing here changes the order.**

Words. N = q^2 points, q = 2^j, k = 2j address bits. *Line sums*: the N + q sums of the input over the lines of the plane
over the field with q elements. R(N) = least gates for all of them. T(N) = least gates for the transform.
*Cyclic form* [read: d-1]: take logarithms of the non-zero addresses in the field with N elements; the N - 1 lines that miss
the origin are the N - 1 cyclic shifts of one set D of q logarithms. So that part of R is one operator, "multiply by
D(t) = sum of t^d" in the ring of polynomials modulo t^(N-1) - 1. A *pass* is multiplication by a polynomial with few terms
(s terms cost s - 1 gates per point). A *prime above 2* is one way of reducing the (N-1)-th roots of unity modulo 2; there is
one for each orbit of the exponents under doubling. The *valuation* of a number at such a prime is how many times 2 divides it there.

## 0. In ten lines

1. **Required table** (section 2): gates per point are 3.75, 7.88, 15.94 adding-only and 5.44, 7.42, 9.70 through the transform at
   16, 64, 256 points; nothing I built or searched is below these. Largest coefficient: 1 and 2.
2. **Growth: like log N.** Through the transform the count is (9/8) log2 N + 1/2 per point; adding-only grows like q. No
   construction grows more slowly. [derived] R(N) >= T(N) - (q+1) T(q): if the transform costs c N log2 N, the line sums cost at
   least (c/2) N log2 N. The line-sum question IS the transform question in other coordinates, not an easier sibling.
3. **16 points, first experiment.** The annealer over the rationals (large and small coefficients in the pool), started from
   the empty circuit and from the adding-only circuit, about 196,000 circuits in all: nothing below 60, and none of the 1,324
   distinct circuits of 60 it recorded uses a coefficient other than +1 (section 3; weak evidence). Over the two-element field
   there IS a circuit with **57** gates [ran, replayed].
   It does not lift: the same wiring over the whole numbers is off by 2 x (a sum over a 2 x 2 rectangle) on 9 of 20 lines.
4. **The question to keep asking, answered** [ran + read]: over the rationals the only relations among the line sums are
   "two parallel classes have the same total" (rank N, so q relations). A line sum is never a combination of other line sums
   except total minus its q - 1 parallels. Modulo 2 there are 11 relations at 16 points; each lifts with a carry that is not a line.
5. **Second relation checked at 256 points** [ran]: the 136 zeros of the quadric are the union of 9 subspaces of 4 bits meeting
   pairwise in 0, and quadric sign(z) = -1 + 2 (number of the nine containing z) - 16 [z = 0] on all 256 addresses.
6. **The cyclic form priced exactly** [ran at 16, 64, 256]: the valuation of D at every prime above 2 is a difference of binary
   digit sums (Stickelberger's rule), it ranges from 0 to j inside one component, and the total is j (N - q)/2.
7. **New lemma, wall SCALAR** [derived, and ran on every case at three sizes]: a pass with two or three terms and rational
   coefficients of ANY size has valuation at most 1 at every prime (beyond a common power of 2), except where its roots of
   unity are cube roots of unity. So in the cyclic form with short passes, coefficient size buys nothing: at least j passes,
   whatever the coefficients. Least number of three-term passes with D's valuations: 2, 7, more than 8 at 16, 64, 256 points,
   which is 4, 14, more than 16 gates per point, worse than adding-only (3, 7, 15). At 16 points d-1's guess is exactly true
   [ran]: on the mixed part D = t^10 ((1 - t)(1 - t^4)(1 + t + t^4))^2, and that costs 8 gates per point against 3.
8. **First specimen tonight of a large coefficient replacing passes** [ran]: at 64 points the pass a + b (t^9 + t^18 + t^36)
   costs 3 gates per point for every a, b, and with (a, b) = (2, 3), (-14, 3), (-46, -45) it has valuation 4, 8, 12 at three of
   the six top primes and 0 at the other three. At 256 points a + b (t^17 + t^34 + t^68 + t^136), 4 gates per point, reaches
   valuation 22 at eight of sixteen primes with (a, b) = (-1220, 989). Reason: the bracket satisfies a quadratic equation, so its L-th power is a + b times
   itself. **Valuation is free; resolution is not**: such a pass sees the primes only in two classes (wall RESOLUTION, section 5).
9. Reading that ties it to the rest of the night [derived]: "H = Z D Z^T" (transform = subset sums, a diagonal of powers of -2,
   subset sums transposed) is a Smith decomposition, the diagonal costs nothing in count (G), and the whole cost of the transform
   is the cost of a matrix that is invertible modulo 2. Volume arguments say nothing about such a matrix.
10. Most useful next step: section 7, item 1 (flat bases), then item 2 (the mask as a product of two passes of higher degree).

## 1. Why the line sums cannot be easier than the transform [derived]

T(N) <= R(N) + (q+1) T(q) and R(N) <= T(N) + (q+1) T(q) [read: d-1]. Write t(k) = T/N and r(k) = R/N. Then
r(k) >= t(k) - (1 + 1/q) t(k/2). If t(k) = c k, then r(k) >= c k/2 - small: half a transform at least. Conversely, if
r(k) <= C k^a with a < 1, then t(k) <= C k^a (1 + 2^-a + 4^-a + ...) x (a bounded product): the curator's claim checks out by
hand. So R grows more slowly than log N per point exactly when T does. Pricing R is a change of coordinates.
The three coordinates in which I looked at R this hour:
- **three layers** [derived from the slice identity]: R without its vertical lines = (q small transforms on the intercept) x
  (q small transforms on x, each relabelled by a field multiplication) x (q small transforms on y). Count 3 q T(q), which equals
  T(N) + (q+1) T(q) to leading order. Without the field multiplication in the middle the three layers would collapse.
- **cyclic** (sections 4 and 5): one multiplication by D(t) plus q + 1 sums through the origin (N - 1 gates).
- **modulo 2** (section 3): rank 3^j, and a cheap circuit that does not lift.

## 2. The required table (count G)

| N | q | (1/2) log2 N | floor N + q | adding-only | through the transform | cyclic, three-term passes | two-element field only |
|---|---|---|---|---|---|---|---|
| 16 | 4 | 2 | 20 = 1.25 | 60 = **3.75** | 87 = **5.44** | 2 passes needed: 4.0 | **57 = 3.56** [ran] |
| 64 | 8 | 3 | 72 = 1.13 | 504 = **7.88** | 475 = **7.42** | 7 passes needed: 14.0 | not built |
| 256 | 16 | 4 | 272 = 1.06 | 4080 = **15.94** | 2484 = **9.70** | more than 8 passes: above 16 | not built |

Largest coefficient used. Adding-only: 1. Through the transform: 2 [ran: I parsed the coefficient sizes of
`e2-0-pieces/slp_4.txt`, `slp_8.txt`, `slp_16.txt`, `slp_64.txt` and read `g-1-tightwires/h8_19gates.txt`: only 1 and 2 occur],
plus one free scaling by 1/q per direction. The 256-point entry is the curator's arithmetic (1600 + 17 x 52), not replayed; its
coefficient size is 2 if the pieces family continues [guess]. Two-element field: every gate is an exclusive or; it is not a
rational circuit. Cyclic column: [ran] the least number of three-term passes (inverses allowed) whose valuations match D's on
the top component, times 2 gates per point; it is a necessary condition, not a circuit, and it covers the N - 1 lines off the origin.
Adding-only, through-the-transform and floor columns are [read] from the brief.

**One line: gates per point grow like log N (through the transform, (9/8) log2 N + 1/2 with tonight's 3/4 family) and like q
adding-only; I found no construction that grows more slowly, and by section 1 one exists only if the transform itself is
below N log N.**

## 3. First experiment, 16 points

**Rationals, annealer** [ran, floats with exact replay of each best; `run_pl.py` adds the task to j-machine's `steiner.py`].
State = auxiliary gates u + c v, c from the pool {1, 2, 3, 4, 8, 3/2 and inverses, both signs}; energy = size of an honest
circuit. Four runs: two from the empty circuit (700 seconds each), two from the 40 pair sums of the adding-only circuit (560
seconds each, no restarts). Result: see the last lines of this section.
Limits: at most 40 auxiliary gates, exact distance only for spans of 3 nodes, no control run on a matrix where subtraction is
known to pay; aa-cross's warning about walks applies. Silence here is weak evidence.
**Exhaustive search modulo 2 and 3 at 59 gates was not attempted**: mincirc enumerates circuits of about a dozen gates.

**Two-element field: 57 gates** [ran: `m2_16.py`, `m2_16.out`, all 20 outputs replayed modulo 2].
Points (x, y), lines y = m x + c and the columns x = const. Rows H_c and columns V_x: 24 gates. h_c = sum of the two other
non-zero rows (3 gates). v_x = V_x + V_0 (3 gates). The three slanted lines through the origin (9 gates). Then for m, c non-zero:
L_m(c) = L_m(0) + h_c + v_(c/m), 9 gates for the nine sums h + v and 9 more. Total 57 against 60.
Where it comes from [derived]: modulo 2 the indicator of a line is a product of j affine forms, and three "half spaces" whose
directions add to zero have indicators adding to 1. Ranks modulo 2 of the first 1, 2, 3, 4, 5 directions: 4, 7, 8, 9, 9 [ran]:
the third and the fourth direction add one dimension each and the fifth adds none.
**What stops the lift** [ran]: over the whole numbers
L_m(c) = h_c - L_m(0) - V_(c/m) - V_0 + **2 x (sum over the rectangle {0, c/m} x {0, c})**, exactly, for all nine lines.
The carry is a sum over a set of 4 points that is not a line. Paying for the nine rectangles gives 87 gates, not 57. In general
[derived] three half-space indicators with directions adding to zero sum to 1 + 2 x (indicator of their common flat): each
relation of the two-element field lifts with a term of one higher codimension and one more factor 2, and there are j levels.
Growth over the two-element field [read, search summary only: Gashkov and Sergeev 2010]: for the plane of prime order p the
line sums cost O(p^2 log p log log p) exclusive ors against p^3 without cancellation. So the two-element field has a
near-linear circuit and the gap to N^1.5 is known. The "N^0.79" of the rank cannot be a gate count: N inputs must be read.

Annealer result [ran]. Empty start: 43,628 and 43,929 circuits evaluated, best 60; no recorded state held more than 4
auxiliary gates, so these two runs stayed next to the empty circuit and say nothing. Start from the adding-only circuit:
56,613 and 52,191 circuits evaluated with 39 or 40 auxiliary gates held, best 60, never 59; 370 + 262 distinct circuits of 60
recorded there, and **not one of them uses a coefficient other than +1** (the walk proposed 2, 3, 4, 8, 3/2 and their inverses
all the time). So near the adding-only circuit, one or two gates away, subtraction and large multiples buy nothing at 16
points. A saving that needs many gates changed at once (as the 57 modulo 2 does: it rebuilds 9 lines) is out of this walk's
reach. Logs: `pl_s1.log`, `pl_s2.log`, `pl_seed11.log`, `pl_seed12.log`, `pl_out.tgz`.

## 4. The second relation at 256 points [ran: `ruling256.py`, `ruling256.out`]

Quadric Q = y1 y2 + y3 y4 + y5 y6 + y7 y8. It has 136 zeros and 270 subspaces of 4 bits on which it vanishes. Nine of them meet
pairwise in 0, their union is the zero set, each is its own perpendicular for Q's pairing, and
(-1)^Q(z) = -1 + 2 x (number of the nine containing z) - 16 [z = 0] on all 256 addresses. So "T(N) <= 2 R_half(N) + O(N)" holds
at 256 points with R_half = coset sums along these nine subspaces. I did NOT check that the nine are part of one plane (a
spread of 17), nor price R_half. Adding-only R_half costs 9 x 240 = 2160 [derived], above the whole transform (1600 by the curator's arithmetic).

## 5. The cyclic form, priced exactly [ran: `cyc.py`, `cyc4.out`, `cyc6.out`, `cyc8.out`, `period.py`, `period.out`]

Method. Exact arithmetic in the ring of whole numbers modulo 2^8 (2^24 in period.py) extended by a root of the field's
polynomial; tau = the root of unity in it; the valuation at prime number a is the power of 2 dividing the value at tau^a.

**(a) Stickelberger's rule holds for D at all three sizes**: valuation at the prime of a = digits(b) - digits(b mod (q-1)),
b = -a, with j in place of the second term when q - 1 divides b. Total over the N - 1 roots: 12, 84, 480 = j (N - q)/2 [derived
formula, matches]. By component:

| N | components where D is a unit or a plain power of 2 | mixed components: valuations at their primes |
|---|---|---|
| 16 | orders 1, 3, 5 | order 15: 2 primes, valuations 0 and 2 |
| 64 | orders 1, 3, 9; order 7 has 1 and 2 | order 21: 0 and 3; order 63: 6 primes, valuations 3, 3, 1, 2, 0, 0 |
| 256 | orders 1, 3, 5, 17; order 15 has 1 and 3 | order 51: 0, 1, 3, 4; order 85: 8 primes, 0 to 4; order 255: 16 primes, 0 to 4 (5, 2, 2, 2, 5 of each) |

The spread inside every mixed component is exactly j (2; 3 and 3; 4, 4 and 4). The log N of the textbook is, in these
coordinates, the number of binary digits.

**(b) Lemma (wall SCALAR)** [derived]. Let x, y be roots of unity of odd order and a, b, c rationals. At a prime above 2:
a + b x has valuation min(v(a), v(b)) unless x = 1; a + b x + c y has valuation at most min + 1 unless x and y are cube
roots of unity. Proof sketch: a rational number reduces into the two-element field, the roots of unity reduce into a field
with 2^k elements and are their own canonical lifts; valuation 1 needs 1 + x + y = 0 there; valuation 2 needs in addition
sqrt(x y) to be a combination of 1, x, y with coefficients 0 or 1 (the carry of adding canonical lifts), which forces
x^2 + x + 1 = 0. [ran] All pairs e < f, all 16 odd classes of the two coefficients modulo 8, at 16, 64, 256 points: 108, 2056,
31676 cases of valuation 2 or more, every one in the cube-root case.
Consequence: with passes of at most three terms, each pass moves the valuation by at most 1 at any prime, whatever its
coefficients. D needs spread j, so at least j such passes; the exact least numbers are larger because a three-term pass
vanishes at few primes (1 or 3 of 6 at 64 points; 1, 2 or 8 of 16 at 256 points):

| N | top-component primes | spread | least number of three-term passes | gates per point | D itself |
|---|---|---|---|---|---|
| 16 | 2 | 2 | 2 | 4 | 3 |
| 64 | 6 | 3 | 7 | 14 | 7 |
| 256 | 16 | 4 | more than 8 | more than 16 | 15 |

[ran: `unit15.py`, exact fractions] At 16 points d-1's guess ("the mask is a unit times a few trinomials, 1 + t + t^4 is the
candidate") is exactly true on the mixed part: 1 + t + t^4 has norm 16, D / (1 + t + t^4)^2 is a unit, and
**D = t^10 ((1 - t)(1 - t^4)(1 + t + t^4))^2** modulo the 15th cyclotomic polynomial. Two three-term passes and four two-term
passes: 8 gates per point, against 3 for D itself. So the hatch exists and costs more than what it replaces, and it gets worse
with size: most trinomials see one prime, and the number of primes is about N / log2 N.

**(c) Going around it once: four terms.** [ran] The scan of all four-term passes at 16 and 64 points found valuations up to 5
and 4 at single top primes with coefficients 3 and 5. The best at 64 points: 1 + 3 (t^9 + t^18 + t^36), valuations
(4, 0, 4, 0, 4, 0). [derived] t^9 + t^18 + t^36 is the number (-1 + sqrt(-7))/2, of norm 2; 2 splits in that quadratic field.
[ran, period.out] its L-th power is a + b times itself, so ONE pass of 3 gates per point has valuation L at half the primes
for every L (checked to L = 12; coefficients grow like 2^(L/2)). Same at 256 points with d-1's quadratic number
t^17 + t^34 + t^68 + t^136 (valuation 2L at 8 of 16 primes, 4 gates per point; checked to L = 11, the run's cap is 24).
At 16 points the best four-term pass is 1 + 5 t + 5 t^4 + 3 t^10: valuation 5 at one of the two top primes, 0 at the other.
This is exactly what Morgenstern's warning asks for: a coefficient that grows, doing the work of L passes.

**(d) Why it does not finish the job (wall RESOLUTION)** [derived]. A pass can have HIGH valuation at a chosen prime only if
it has more free rational coefficients than the dimension, over the 2-adic numbers, of the space spanned by the values of its
groups of terms at that prime (then the coefficients can approximate a 2-adic relation). The cleanest case is dimension 1: a
sum over a whole doubling-orbit of exponents, whose value is a 2-adic number. An orbit of top order has k = log2 N terms (half
orbits have values in a space of dimension 2 and need one more coefficient, and so on: about k + 1 terms either way); orbits
with fewer terms come from roots of unity of small order and see the primes only through that small order. At 64 points D's valuations along the
cyclic group of the six primes are 3, 3, 1, 0, 0, 2; their part of order 6 is not zero (5 + sqrt(3) i), so no product of passes
of the quadratic and cubic kind has D's valuations. A pass that separates all six has 7 terms: 6 gates per point, against 7 for D.
In short: valuation L costs nothing, a class of primes costs its orbit length, and D's pattern (binary digit sums) lives at
full resolution. D itself is the miracle: q terms, where a generic element with its valuations has about N.
[guess] The general statement "an s-term rational pass that separates r classes of primes has s >= about log2 r" is not proved.

## 6. Three readings that connect to the night

- **The transform's Smith decomposition** [derived]. Over the whole numbers H = Z D Z^T (Facts of the brief) with Z of
  determinant 1 and D = diagonal of (-2)^weight. In count (G) the diagonal is free. So T(N) <= 2 cost(Z), and every other
  pair (P, Q) invertible modulo 2 with H = P D Q gives a program. The valuations weight(x) are the binary digit sums of
  Stickelberger's rule: the subset-sum matrix plays, in address coordinates, the part that the 2-adic unit plays in the cyclic
  ones. All of the cost sits in a matrix whose determinant is odd, where Morgenstern's volume argument is silent.
- **Flat bases: one formula, two known programs** [derived; ran at 16 points, `flatbasis.py`, `flatbasis.out`]. Take ANY N flats
  (cosets of subspaces of the address bits) whose indicators form an invertible matrix B. Then
  **H = P x (diagonal of the flats' sizes) x B^-1**, where each column of P is a pattern of +1 and -1 on the perpendicular
  subspace and 0 elsewhere. With the coordinate subcubes this is H = Z D Z^T (Yates on both sides; 81 + 81 non-zeros). With 16
  of the plane's 20 lines it is the slice theorem: P is five 4-point transforms (64 non-zeros) and B^-1 is "write the input as a
  combination of lines" (121 non-zeros, entries 0 and +-1). So Yates and the plane are two points of one family, and every
  other flat basis is a program nobody has priced. First look [ran, `flatsearch.py`, crude size = non-zeros of P plus non-zeros
  of B^-1, which is NOT a gate count; 240 seconds of hill climbing over 306 flats, the whole space left out by an oversight]:
  mixed bases reach 152 (94 + 58) against 162 for Yates and 185 for the lines; typical best profile: one point, five pairs,
  nine flats of 4 points, one of 8. A 6 % gain in a crude size is not a result; the object is.
- **REPAY and the carry.** The 57-gate circuit shares h_c + v_x between three lines modulo 2; over the whole numbers each
  sharing is repaid by one rectangle. Same exchange rate as aa-cross's wall, seen as a 2-adic carry.

## 7. What I would do next

1. **flat-bases** (new, section 6): H = P x sizes x B^-1 for any flat basis. At 16 points price B^-1 and P in real gates for
   the 152-basis of `flatsearch.out` and for the best bases under a gate-count proxy (not non-zeros); is any pair below
   2 x 32, or below 52 in all? Then 64 points, with the plane's lines for the middle sizes and subcubes at the ends. The
   growth law to look for: cost(B^-1) + cost(P) per point as the mix of flat sizes changes from "all sizes" (Yates) to
   "one size" (the plane).
2. **two-passes-of-higher-degree**: at 64 points D's top valuations (3, 3, 1, 0, 0, 2) minus a quadratic pass (free valuation on
   alternate primes) leave a pattern with values in {0, 1, 2}; find the pass with fewest terms that has it (search over sums of
   one or two doubling-orbits with rational coefficients; exact test in `cyc.py`). If 4 or 5 terms suffice, the cyclic part at
   64 points costs under 7 per point and the same question at 256 becomes a growth law.
3. **the unit at 64 points**: at 16 points the unit is (1 - t)^2 (1 - t^4)^2 up to a shift (`unit15.py`). At 64 and 256 points
   I matched valuations only; find 7 trinomials with D's valuations on the order-63 part and the two-term product that is left.
   If the number of two-term factors grows like the rank of the unit group (about N/2), the cyclic class is dead for a second reason.
4. **modulo 4** (aa-cross item 8) on the 57-gate circuit: the carries are 9 rectangles; is there a wiring whose carries are lines?
5. **R_half at 256**: price the nine-subspace coset sums of section 4 by the pieces family.

## 8. Criticism, last

- The idea as posed did not move: no line-sum circuit below the two known counts at any size, and section 1 says the question
  is equivalent to the transform's. I am reporting coordinates and walls, not a saving.
- The annealer had no control run, its empty-start half did not explore, and its seeded half explores only the neighbourhood
  of the adding-only circuit. "Nothing below 60 at 16 points over the rationals" is NOT established; the first experiment of
  the brief is still open over the rationals. A fair next try: seed it with the 57-gate wiring plus its nine rectangles (87).
- The 57 is over the two-element field only, at one size, and such gaps are in the literature for prime orders; I did not build
  64 or 256 points there, and I did not check the Gashkov and Sergeev statement beyond a search summary.
- Section 5 is about one class: programs that are products of sparse cyclic passes. A general circuit need not be cyclic. The
  lemma in (b) is a sketch; its support is the exhaustive scan (odd coefficient classes modulo 8, three sizes), not a proof
  read by anyone. "Least number of passes" matches valuations on the top component only and ignores the unit, so the true cost
  in that class is higher, and inverse passes cost more than 2 gates per point.
- (d) is argued, not proved; the only hard fact in it is the non-zero order-6 component at 64 points, done by hand.
- The Smith reading and the flat-basis formula may restate u-4 (zdz) or g-0 (mirror), which I did not read. The flat-basis
  search used a crude size, left out the whole space as a flat, and ran four minutes.
- Section 4 checks the relation, not that the nine subspaces extend to a plane.

Files: `waves/wave-09/ad-1-linesums/` : m2_16.py, m2_16.out (57 gates modulo 2, the
carry identity, ranks); ruling256.py, ruling256.out; flatbasis.py, flatbasis.out, flatsearch.py, flatsearch.out (section 6); cyc.py, cyc4.out, cyc6.out, cyc8.out (valuations, trinomial scan, least
passes, four-term scan at 16 and 64); period.py, period.out; unit15.py, unit15.out (the mask as a square at 16 points);
run_pl.py with copies of j-machine's steiner.py and slp.py, pl_s1.log, pl_s2.log, pl_seed11.log, pl_seed12.log, pl_out.tgz (annealer). cyc.py and the annealer
ran on the rented Linux machine (numpy); everything else under light.py.

Sources
- https://mathnet.ru/eng/da608 (Gashkov, Sergeev, "On the complexity of linear Boolean operators with thin matrices", 2010; search summary only)
- https://arxiv.org/pdf/1701.08557 (Grinchuk, Sergeev, thin circulant matrices; title only)
- `aa-cross.md`, `d-1.md`, `WAVE9-PICKS.md` brief 2, `e2-0-pieces/slp_*.txt`, `g-1-tightwires/h8_19gates.txt`
