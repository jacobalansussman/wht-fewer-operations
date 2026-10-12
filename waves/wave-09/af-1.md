# af-1: the skeptic's report on ad-1's inequality R(N) >= T(N) - (q+1) T(q)

> Editor's note (11 October 2026): what this report says about published work is as its author marked it: read through a tool that summarises, from an abstract, second hand, or from memory. Nobody checked those statements against the sources. Two older papers that the night's searches did not reach were read afterwards. See [Earlier papers](../README.md#earlier-papers).

11 October 2026, 07:33 to 07:55 EDT, one agent, 30-minute box. Private. Nothing in Lean, nothing published.
Marks: [ran] = run of mine this half hour, own code, whole numbers or exact fractions (files in `af-1/`); [derived] = by
hand this half hour, checked by nobody; [read] = from tonight's reports; [recalled] = memory; [guess].
Gate counts: **(G)** a gate is any a*u + b*v, scalings free; **(O)** OpenAI's count, additions and scalar
multiplications each charged. Each statement says which.
Read: ad-1.md in full, m2_16.py and m2_16.out, d-1.md sections 2 and 4, the passages of aa-cross, ae-cross, WAVE8-NOTE and
WAVE9-PICKS that state or use the relation. Not read: the rest of ad-1's folder (sections 4 to 6 of ad-1 are not the
object), OpenAI's model files, the lower-bound literature note (the path in the brief does not exist on this disk).

**Verdict: the inequality holds and is known. It is true in both counts, it uses no transposition and no scaling, and it
was already written in wave 1 (d-1 section 4) and read correctly by wave 9's curator (WAVE9-PICKS, notes). It is the
wave-8 relation itself, read from the other side: it proves nothing about the cost of the line sums and it closes
nothing; "closed" is ae-cross's word and it is too strong. The sentence "(c/2) N log2 N if the transform costs
c N log2 N" has a premise that the published theorem excludes; the form that survives is "the line sums and the
transform have the same exponent of log N". The 57-gate claim is right, and I can make its "does not lift" stronger for
that wiring; it says nothing about whether 57 or 59 gates exist over the rationals.**

Words. N = q^2 points, q = 2^j, k = 2j address bits. An address is a pair (a, b) of elements of the field with q
elements. The *spread* is the q + 1 sets S_c = {(a, c a)} and S_inf = {(0, b)}: each has q addresses, they cover all
addresses and share only 0. V_i = the addresses whose bit dot product with every member of S_i is even. A *line* is a
shifted copy of some V_i; there are N + q lines of q points each, and two lines share at most one point (an affine
plane). *Line sums*: the N + q sums of the input over the lines. R(N) = least gates for all of them. T(N) = least gates
for the transform H x, H the matrix of signs (-1)^(x.y), not normalised.

## 1. The claim, exactly

(a) **Slice identity.** For an output address y in S_i, (H x)(y) = sum over the q lines of direction i of
(+1 or -1) x (that line sum), and these signs make a q-point transform of the q line sums of direction i.
(b) **Hence T(N) <= R(N) + (q+1) T(q)**, which rearranged is the object: R(N) >= T(N) - (q+1) T(q).
(c) **Conversely R(N) <= T(N) + (q+1) T(q)** (count G): the q line sums of direction i are 1/q times the q-point
transform of the transform's outputs on S_i.
(d) ad-1's reading: "if the transform costs c N log2 N, the line sums cost at least (c/2) N log2 N; pricing the line
sums is a change of coordinates, not a reduction"; ae-cross's reading: "wave 9 closed the one relation of wave 8 whose
success would have passed the bar".
(e) Companion: 57 exclusive-or gates compute the 20 line sums at 16 points modulo 2 (adding-only needs 60); the same
wiring over the whole numbers is wrong on 9 lines, and paying for the carries costs 87.

## 2. Verification with my own code

`af-1/check.py`, `check.out` [ran]. At N = 4, 16, 64, 256, 1024, 4096 (ad-1 and aa-cross stopped at 256):
- the spread covers and meets in 0; there are N + q distinct lines; two lines of different directions meet in one point;
- (a) holds as an identity of matrix rows, on all (q+1) q rows (6, 20, 72, 272, 1056, 4160 rows);
- (b): on an integer input, the q+1 small transforms of the line sums reproduce all N outputs of the transform;
- (c): the small transforms of the transform's outputs on each S_i are exactly q times the line sums.
All true at all six sizes. (a) is in fact a one-line proof: x and its line's representative differ by a member of V_i,
whose dot product with y is even. [derived]

**The three attacks named in the brief, answered.**
1. *Direction of each use of the transposition rule.* There is none. (b) and (c) are compositions of circuits: the
   outputs of one are the inputs of the next. The transposition rule appears in ae-cross's hybrid 3, not here. [derived]
2. *Same normalisation on both sides.* Yes for the object: (b) uses the plain sign matrix at N points and at q points
   and no scaling at all, so R(N) >= T(N) - (q+1) T(q) holds word for word in count (G) **and in count (O)**. In (G)
   an R-circuit that delivers each line sum up to its own scale is still enough, because the first gates of the small
   transforms absorb the scales. Only the converse (c) divides by q: free in (G), at most N scalings more in (O) (scale
   the inputs once), which is d-1's "+ N + q". [derived]
3. *Free relabelling.* (b) needs the q outputs of each small transform renamed to the addresses of S_i, and (c) the
   reverse. In a circuit count, (G) or (O), naming a wire costs nothing, and T and R do not depend on how addresses are
   named. In a model that charges for moving data (the engine's address maps) these q + 1 renamings are a cost that the
   inequality ignores. I did not check OpenAI's model text for this. [derived; the last sentence unchecked]

So (a), (b), (c) are correct. Nothing to repair in the inequality.

## 3. What the inequality does and does not say (this is where the object is over-read)

**It is the same relation.** Wave 8's relation is (b). The object is (b) with one term moved across. "R(N) = O(N) would
give T(N) = O(N log log N)" and "if T is large then R is large" are one statement and its contrapositive. So wave 9 did
not close the relation; it restated it. And it is not new tonight: d-1 section 4 (wave 1) has, word for word,
"T(N) - (q+1) T(q) <= Rad(q) <= T(N) + (q+1) T(q) + N + q ... Rad and T have the same order unless T is already nearly
linear." [read] And the curator of wave 9 wrote before ad-1 ran: "R(N) = O(N (log N)^c) and T(N) = O(N (log N)^c) are
the same statement for c < 1. So brief 2 is not an easier problem; its value is a matrix with a different shape."
[read: WAVE9-PICKS, notes of the curator] That reading is the right one. What I add below is the constants, the case
c = 0, count (O), and the remark on the premise.

**It gives no number.** The right-hand side needs a lower bound on T(N), and for free coefficients no lower bound above
linear is known for the transform [recalled]. With tonight's counts the expression T(N) - (q+1) T(q) is 17, 133, 716 at
16, 64, 256 points (count G) [ran], but those use *upper* bounds on T(N), so they bound nothing; at 16 points 17 is
below the trivial floor of 20 (one gate per distinct output).

**The premise of the "(c/2)" sentence is false at large size.** The published program gives T(N) = O(N (log N)^z) with
z = 1 - 8.7625e-4 in count (O), hence in (G). So T(N) / (N log2 N) tends to 0 and there is no constant c > 0 for which
"the transform costs c N log2 N" at all sizes. [derived from the published theorem]

**The nearest true statement** [derived; write t(k) = T/N and r(k) = R/N at N = 2^k]:
- If r(k) <= C k^a for every even k, with 0 < a <= 1, then t(k) <= (2 C / (1 - 2^-a)) k^a + 2 for k a power of 2 (the
  recursion halves k, the sum is geometric, and the product of the factors 1 + 1/q is at most 2); for other k add at
  most 2 log2 k per point (an odd k is reached from k - 1 by one layer of two-point transforms, one gate per point).
- If t(k) <= C k^a for every k, then r(k) <= 3 C k^a.
- So **the least exponent a with cost O(N (log N)^a) is the same number for the line sums and for the transform.**
- At a = 0 the two sides differ: transform linear implies line sums linear; line sums linear implies only
  T = O(N log log N). "Line sums in O(N)" sits between "transform in O(N)" and "transform in O(N log log N)".
- If T(N) is asymptotically c N (log2 N)^z, then R(N) >= c (1 - 2^-z) N (log2 N)^z (1 - o(1)). At z = 1 this is ad-1's
  c/2. Without that regularity only the exponent statement holds: the lower bound needs the constant of T at size N
  and at size q to agree within a factor 2^z.

**Free corollary** [derived]: by (c) the line sums of the plane cost O(N (log N)^(1 - 8.7625e-4)) in count (O). It
follows from the published theorem in one line; I did not see it stated in tonight's notes (d-1 has "N log N at most").

**Consistency check that came out right** [derived; Morgenstern's theorem recalled]: with coefficients of bounded size
the determinant argument gives about (N/2) log2 N for the transform (determinant N^(N/2)) and about (N/4) log2 N for
the line sums (the matrix R^T R = q I + J has determinant q^(N-1) (q + N)): the ratio is exactly the one half of (d).

**Fair wording for the notes.** Not "closed". Rather: *the line sums are neither easier nor harder than the transform;
the exponent is shared; the plane is a second coordinate system for the same open question.* That is a reason not to
expect the line sums to fall by themselves. It is not evidence against linear size, and it is not a wall: a wall fences
a class of circuits, and this fences none.

## 4. The companion claim: 57 gates over the two-element field

`af-1/lift.py`, `lift.out` [ran], the program rewritten by me as an explicit list of gates.
- 57 exclusive-or gates, all 20 line sums right modulo 2. Confirmed.
- The same wiring with every coefficient +1 over the whole numbers: 11 of 20 right, 9 wrong. Confirmed (ad-1's text
  says "9 of 20", its output file "9 of 9": the same nine).
- **Stronger than ad-1 tested: no choice of coefficients repairs this wiring.** ad-1 tried only +1. In any lift the 11
  wires that are rows, columns and lines through the origin are outputs, so they are fixed up to a scale; each of the
  other nine lines is then forced into the span of five given line sums (its parallel through the origin, two rows, two
  columns). Over the rationals, and modulo 3, 5, 7, none of the nine lies in that span; modulo 2 all nine do. The cause
  is the rank: 16 over the rationals, 9 modulo 2.
- The paid-for program (coefficients 1, -1, 2) replays exactly with **87** gates. The arithmetic is right. It is one
  way of paying, not a least cost, and it equals the "through the transform" count 52 + 5 x 7 only by coincidence.
- What the claim does **not** show: that no rational circuit with 57, 58 or 59 gates exists. Over the rationals the
  count at 16 points is known only to lie between 20 and 60. ad-1 says this itself in its section 8; ae-cross's
  "does not lift" should be read as "this wiring does not lift".
- One size further, 64 points [ran]: rank 27 modulo 2, 64 modulo 3, 64 modulo 2147483647 (so 64 over the rationals:
  a rank modulo a prime never exceeds the rational rank). The shortest relation among lines modulo 2 has 9 lines (5 at
  16 points): all sums of at most 4 lines are distinct, and the nine lines y = m x + m^2 together with x = 0 add to
  zero. So a line obtained from a relation costs q - 1 gates, the same as adding its q points, at both sizes; the three
  gates saved at 16 points come only from partial sums shared between relations. I did not build a 64-point circuit
  over the two-element field, so there is no growth law for that count here, and it would not be a rational circuit.

## 5. Known?

- The slice identity is the Fourier slice theorem of the finite Radon transform (the Radon transform of a finite plane
  is its table of line sums). E. D. Bolker, "The finite Radon transform", Contemporary Mathematics 63 (1987), 27-50;
  P. Diaconis and R. L. Graham, "The Radon transform on Z_2^k", Pacific J. Math. 118 (1985), 323-345; F. Matus and
  J. Flusser, "Image representation via a finite Radon transform", IEEE Trans. PAMI 15 (1993), 996-1006 (p x p images,
  p prime); Kingston and Svalbe, generalised finite Radon transform, 2006-2007, who state a discrete Fourier slice
  theorem. None is on arXiv. [bibliographic details confirmed by search today; texts not read; that each states the
  slice theorem is recalled for the first three]
- Circuits over the two-element field far smaller than circuits without cancellation: Find, Goos, Jarvisalo, Kaski,
  Koivisto, Korhonen, "Separating OR, SUM, and XOR circuits", 2013, arXiv:1304.0513 [abstract read]; Gashkov and
  Sergeev 2010 (a p^2 x p^2 matrix of weight p^3 with no 2 x 2 block of ones, exclusive-or cost O(p^2 log p log log p))
  [search summary only: the summary does not say this matrix is the plane's line matrix, as ad-1 assumed]; survey:
  Jukna and Sergeev, "Complexity of linear Boolean operators", 2013. The gap 57 against 60 is a small case of that.
- The shortest relation of q + 1 lines is the classical fact that q + 2 lines of a projective plane of even order, no
  three through a point, cover every point 0 or 2 times (a dual hyperoval). [recalled]
- Not found: a paper that states "line sums and transform have the same circuit exponent". It is two lines from the
  slice theorem. Five searches are not a survey.
- **What the known theory predicts for "linear or not": nothing.** With bounded coefficients both need N log N. With
  free coefficients both are open, and they are open together.

## 6. Does it scale; what it gives in the user's terms

- Scaling: the identity and both compositions hold at every size (a theorem; replayed to 4096 points). The sandwich
  T(N) - (q+1) T(q) <= R(N) <= T(N) + (q+1) T(q) is exact as a statement and gives, with the family (3/4) N k + N/4,
  the *upper* bound (9/8) k + 1/2 gates per point for the line sums (5.44, 7.42, 9.70, 11.88, 14.07 at 2^4 to 2^12)
  [ran, arithmetic on counts; the entries from 256 points on use the formula, not built circuits].
- Circuit size for n points: none new for the transform. For the line sums: O(n (log n)^(1 - 8.7625e-4)) in count (O),
  inherited from the published theorem.
- Saving exponent: none. Change of order: none.
- The one useful number in the sandwich is a target, not a bound [ran, arithmetic]: a line-sum circuit with fewer than
  T(N) - (q+1) T(q) gates (known counts, G) is a better transform. That is 133 gates at 64 points and 716 at 256
  (2.08 and 2.80 per point, about (3/8) k), against floors of 72 and 272 and best known line-sum counts of 475 and
  2484. At 16 points the target (17) is below the floor (20), so 16 points can decide nothing about this route.
- What it changes for the search: the line-sum relation stays exactly as alive as it was at the end of wave 8. It
  should be taken off the list of "closed" things and off the list of "shortcuts": a linear circuit for the line sums
  is a transform in N log log N, no less, and the plane is one more coordinate system in which to look for it.

## 7. Limits of this report

- Section 3's exponent statement is by hand, in 30 minutes, read by nobody. "The published program gives a bound in
  count (O)" is the brief's description of the published result; I did not open the release tree.
- I did not read OpenAI's model text; "relabelling is free" is the circuit reading of counts (G) and (O).
- "No lower bound above linear for free coefficients" is recalled, not looked up today.
- The literature check is five searches and one abstract.

Files: `waves/wave-09/af-1/` : check.py, check.out (plane, slice identity and
both compositions at 4 to 4096 points; the table of section 6); lift.py, lift.out (57 gates, the lift test with free
coefficients, 87 gates, ranks and shortest relations at 16 and 64 points). Both ran under light.py, one second each.

Sources
- https://msp.org/pjm/1985/118-2/p09.xhtml (Diaconis, Graham 1985)
- https://link.springer.com/article/10.1007/s00454-020-00207-x (cites Bolker 1987 with volume and pages)
- https://arxiv.org/pdf/1101.0076 (cites Matus, Flusser 1993 with volume, pages, DOI 10.1109/34.254058)
- https://researchportalplus.anu.edu.au/en/publications/generalised-finite-radon-transform-for-nn-images/ (Kingston, Svalbe)
- https://arxiv.org/abs/1304.0513 (Find, Goos, Jarvisalo, Kaski, Koivisto, Korhonen 2013)
- https://mathnet.ru/eng/da608 and https://geodesic.mathdoc.fr/item/DA_2010_17_3_a0 (Gashkov, Sergeev 2010; search summary only, the page refused the connection)
- https://nowpublishers.com/article/Details/TCS-063 (Jukna, Sergeev 2013)
- `ad-1.md`, `ad-1-linesums/m2_16.py`, `m2_16.out`, `d-1.md` section 4, `aa-cross.md`, `ae-cross.md`, `WAVE9-PICKS.md` brief 2
