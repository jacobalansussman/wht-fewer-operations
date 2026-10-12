# ad-3-straightenquadri: an exchange is "a sign convolution on half the points"; j = 2 at 16 points, and at 64 points exactly 4 with single flats and exactly 3 = k/2 with unions of three; it cannot stay bounded

11 October 2026, 60-minute box. Private. One agent; nothing reviewed, nothing in Lean, nothing published.
Marks: [ran] = exact run of mine tonight (files in `ad-3-straightenquadri/`; whole numbers or fractions unless a line says
floats); [derived] = by hand tonight, checked by nobody; [read] = from tonight's reports; [recalled] = from memory; [guess].
Gate count everywhere: **(G)**, a gate is any a*u + b*v, scalings, signs and relabellings free. Count (O) is not used.
Read for this: aa-cross.md in full, WAVE9-PICKS brief 4, `aa-cross/h2_specperm.py` and its output, the top of g-0.md, the
lines of e-5, g-3, i-hatch, j-failproof that mention Ailon's potential. Nothing else of waves 1 to 8 was re-read.

**No circuit below a known count, no growth law below N log N. The route as briefed ties or loses, and I can say why.**

Words. N = 2^k points; an *address* is k bits; addresses are added bit by bit modulo 2; x.y = number of common ones
modulo 2. *The transform* H has entries (-1)^(x.y). *Convolution with spectrum s*, written C[s]: the matrix H diag(s) H / N
(in the frame of the outputs it is the diagonal s). A *pattern* is a set A of addresses; its convolution has spectrum -1
on A and +1 elsewhere, and is a reflection. *Flat*: a subspace of the address space or a shifted copy; its dimension is
the number of free bits. *Quadric*: the set where a form like y1 y2 + y3 y4 + ... is 1 (any non-degenerate one; at 16
and 64 points it has 6 and 28 addresses). The transform is, up to free signs and one relabelling, the convolution of a
quadric. *Start*: a hyperplane minus a flat of k/2 - 1 bits (also 6 and 28 addresses); its convolution costs under 2N.
*Exchange (u, T)*: T a set that is unchanged by adding u; the permutation of the outputs that sends y to y + u for y in
T and fixes the rest. *Class c*: T is a union of at most c flats (each unchanged by adding u). Exchanges that are affine
maps (T a hyperplane or everything) are free relabellings and are not counted. j(k, c): the least number of counted
exchanges of class c whose product carries the start to some quadric. D(f): the largest dimension of a flat on which a
pattern's sign is constant (D = k - 1 for the start, k/2 for a quadric [read: aa-cross, wall BENT]).

## 0. In nine lines

1. **j(4, c) = 2 for c = 1, 2, 3** [ran, exhaustive over all 8,008 sets]. The 6-sets at 16 points fall into only three
   classes up to affine maps: the start (840 sets, D = 3), the quadrics (448, D = 2) and everything else (6,720, D = 2,
   e.g. a plane plus a line); the middle class is one exchange from each end, already with a single flat.
2. **At 64 points j(6, 1) = 4 exactly, j(6, 3) = 3 exactly, j(6, 2) is 3 or 4** [ran]. Lower bounds, exhaustive with
   positive controls: no product of one or two single-flat exchanges reaches a quadric (1,077,780,816 products), and
   none of them is even ONE exchange with an ARBITRARY set T away from a quadric; the same for one exchange of class 2
   (8,550,234 sets) or class 3 (6,800,286,108 sets) followed by an arbitrary one. Upper bound: a path of 4 single-flat
   exchanges, found by a beam search and replayed (flats of 16, 16, 8, 4 addresses); its first two go along one
   direction and merge into ONE exchange on a union of three flats, which gives the 3. So **j(k, 1) = 2, 4** (twice
   Lemma D's bound; k - 2 or 2^(k/2 - 1) for all two points can say) and **j(k, 3) = 2, 3 = k/2: the textbook's tie.**
3. **Why it cannot stay bounded** [derived; a five-line lemma, section 2]: one exchange of class c lowers D by at most
   c. So **j(k, c) >= (k/2 - 1)/c**. This is wall BENT again; the exchanges do not go around it.
4. **Why a hyperplane is a bad place to start** [derived]: no single exchange, with ANY set T, carries a set that lies
   inside a hyperplane to a quadric (k >= 4). That is the 2 at 16 points for every c.
5. **The dictionary** [derived; ran on 750 flat exchanges and 60 random sets T at 16 points, 0 failures]: the
   conjugator of an exchange is Phi = I - 2 diag([u.x = 1]) Pi_T. It is the identity on the half u.x = 0, and on the
   half u.x = 1 it is the reflection whose spectrum is -1 on T: **an exchange costs exactly one sign convolution on N/2
   points.** For a flat T of dimension d that is 2^(d-1) reflections "x minus twice the mean" on N/2^d points each:
   N - 2^(d-1) gates, about N, whatever the size of the flat (dimension k - 1: free; dimension k - 2: 7N/8).
6. **One product built and priced** [ran, fractions, all 256 entries]: start, two single-flat exchanges, 16 points:
   14 + 14 + 30 + 14 + 14 = **86 gates** (textbook 64, night's best 52). Law of the family: 2 x (about N per flat) x j
   + 2N, with j c >= k/2 - 1: **(7/8) N log2 N - O(N) or more** with these circuits for the reflections; with the
   measured j = 4 it is 592 gates at 64 points against the textbook's 384. Not a growth law below N log N.
7. **In function language** [derived, ran]: the exchange replaces f by f + t (f(y) + f(y+u)), t the indicator of T.
   Cut the addresses by the bit along u: the two halves f0, f1 become mux(t; f0, f1) and mux(t; f1, f0). So an
   exchange is a **controlled swap of the spectra of two arrays, at the price of one sign convolution with spectrum t
   before and one after.**
8. **Where the 2N log N goes** [derived]: one exchange from the quadric, with any T, leaves the quadric untouched on a
   hyperplane, hence two untouched copies of the quarter-size quadric; T must contain a third, and T is applied twice.
   Four quarter-size transforms plus O(N): the textbook recursion T(N) = 4 T(N/4) + O(N), which is exactly critical
   (three copies in place of four would be linear size). In the accounting by restrictions one exchange can only tie.
9. **The wall, named**: an exchange program made of flats is a rotation program (each reflection on m points is
   2m - 2 rotations), so Ailon's potential [recalled, as in e-5 and j-failproof] caps it at N log N; measured [floats]:
   on the way in the two exchanges give 16 bits each for 14 gates, the cheap start 9.7 bits for 30 gates. State: a wall
   I can name.

## 1. The dictionary, and the price of one exchange

[derived] Let P be the permutation matrix of the exchange (u, T) in the frame of the outputs: P = diag(1 - t) + X_u
diag(t), with t the indicator of T and X_u the shift by u. Conjugating by H turns X_u into the sign diagonal
(-1)^(u.x) and diag(t) into the convolution Pi_T whose spectrum is t (a projector). So
**Phi = H P H / N = I - 2 diag([u.x = 1]) Pi_T**, and for any pattern f, C[f after the exchange] = Phi C[f] Phi.
Because T is unchanged by adding u, the kernel of Pi_T lives on the addresses with u.x = 0, so Pi_T does not mix the two
halves u.x = 0 and u.x = 1. Hence Phi = (identity on one half) + (the reflection I - 2 Pi_T on the other half).
[ran: `build16.py` part 1, all 750 single-flat exchanges at 16 points; `mux16.py` part 1, 60 random sets T and random f.]

For a flat T = a + V of dimension d (u in V): Pi_T g (x) = (|V|/N) x (signed sum of g over x + V-perp), V-perp having
m = N/2^d addresses. On the half u.x = 1 there are 2^(d-1) shifted copies of V-perp, and on each Phi is "g minus twice
its signed mean": m - 1 gates for the sum and m for the outputs, 2m - 1 gates; for m = 2 it is a signed swap and free.

| flat of dimension | k - 1 | k - 2 | k - 3 | 1 (a transposition) |
|---|---|---|---|---|
| reflections x points each | N/4 x 2 | N/8 x 4 | N/16 x 8 | 1 x N/2 |
| gates per exchange, one side | 0 (an affine map) | 7N/8 | 15N/16 | N - 1 |

So the price is per flat, not per address moved: swapping two outputs costs as much as swapping N/4 of them.
Family law [derived]: T(N) <= 2 x (sum of the exchanges) + (cost of the start) = about 2 j c N + 2N.

## 2. Two lemmas that answer "why would it have to be k/2?"

**Lemma D** [derived]. If T is a union (or any Boolean combination) of c flats, the exchange (u, T) lowers D by at most
c. Proof. Let f be constant on a flat G. Go through the c flats F_i in turn: if the current G' meets F_i in a proper,
non-empty part, that part lies in an affine hyperplane of G'; replace G' by the parallel hyperplane that misses it (one
dimension lost). At the end G' has dimension at least dim G - c and lies inside T or outside T. Outside T the exchange
does nothing on G'. Inside T the new pattern on the flat G' + u reads f on G'. Either way the new pattern is constant
on a flat of dimension dim G - c.
[ran: `bfs16.out`, every 6-set times every counted exchange for c = 1, 2, 3: no violation. The check is weak: D only
takes the values 2 and 3 on 6-sets at 16 points.]
Consequence: **j(k, c) >= (k/2 - 1)/c**, and more generally (D(any start) - k/2)/c from any start. With about N gates
per flat per side this is 2 (k/2 - 1) N + 2N = N log2 N if the bound were attained with the dearest flats and
(7/4)(k/2 - 1) N + 2N = (7/8) N log2 N + N/4 with the cheapest (dimension k - 2). The second number is the product of
k/2 four-point blocks at 7 gates each, i.e. nothing new. D is a weak invariant: at 16 points the first exchange takes D
from 3 to 2 and the second changes nothing in D, yet both are needed.

**Lemma H** [derived]. For k >= 4 no single exchange, with any set T, carries a set inside a hyperplane to a quadric.
Proof. Read backwards: the exchange applied to a quadric Q gives g = Q + t l with l(y) = Q(y) + Q(y+u), an affine form
(a quadric's differences are affine). On l = 0, g = Q, which is unchanged by adding u and not identically 0. On l = 1,
g(y+u) = g(y) + 1: exactly one address of every pair {y, y+u} is in g. A hyperplane a.y = b containing all of g either
has a.u = 1 (then it holds one address of each pair, impossible on l = 0) or a.u = 0 (then it holds whole pairs, so on
l = 1 it holds everything, so it IS l = 1, and the part on l = 0 is outside). [ran: 16 points, j = 2 for every c <= 3;
64 points, no single exchange reaches a quadric.]

**The same backwards reading is a fast test** [derived, used in `k6.c`]: g is one exchange (any T) from a quadric
exactly when some direction u has g(y) + g(y+u) equal to an affine form l, and g on l = 0 extends to a quadric (64
candidate extensions at 64 points, each replayed). Controls [ran: `k6_P.out`]: 200 of 200 planted single-flat
exchanges and 200 of 200 planted exchanges on random sets recognised; 3 of 3 planted two-exchange sets found by the
two-step search.

## 3. The first experiment

16 points [ran: `bfs16.c`, `bfs16.out`, breadth-first over all 8,008 sets, 540 / 2,220 / 3,480 counted exchanges for
c = 1 / 2 / 3]. Distance matrix between the three affine classes, the same for c = 1, 2, 3:

| from \ to | start (840) | middle (6,720) | quadrics (448) |
|---|---|---|---|
| start | 0 | 1 | 2 |
| middle | 1 | 0 | 1 |
| quadrics | 2 | 1 | 0 |

**j(4, 1) = j(4, 2) = j(4, 3) = 2**, and by Lemma H it is 2 for arbitrary T as well.

64 points [ran: `k6.c`; the stabiliser of the start has three orbits on directions u (inside the removed flat's
directions, inside the hyperplane's, outside), so the first exchange is taken from three representatives and all later
ones are unrestricted; 2,388 flats of dimension 1 to 4 per direction].

| what was tried | number | quadrics reached |
|---|---|---|
| one single-flat exchange (all 63 directions) | 150,444 | 0 |
| two single-flat exchanges | 1,077,780,816 | 0 (and no bent pattern of higher degree either) |
| one single-flat exchange, then one exchange with ANY T | 7,164 | 0 |
| one class-2 exchange, then one exchange with ANY T | 8,550,234 | 0 |
| two single-flat exchanges, then one exchange with ANY T | 1,077,780,816 | 0 |
| one class-3 exchange, then one exchange with ANY T | 6,800,286,108 | 0 |

So **j(6, 1) >= 4 and j(6, 2), j(6, 3) >= 3** (files `k6_A.out`, `k6_B1.out`, `k6_B2.out`, `k6_C.out`,
`k6_B3_0a/0b/1a/1b/2a/2b.out`; the class-3 run is 3 orbits x 2,266,762,036 unions of three flats). Lemma D alone gives
2 and 1.
Upper bound [ran: `k6.c` mode S; a beam search over single-flat exchanges guided by the sum over v of |r(v)|^p, where
r(v) = 64 - 2 #{y : pattern(y) != pattern(y+v)} is 0 for every v exactly on bent patterns; every path found is printed
and replayed from the start]:
- p = 1, beam 2,500 (`k6_S2500_p1.out`): **a quadric after 4 single-flat exchanges**: u = 11 on a flat of 16
  addresses, u = 11 on another flat of 16, u = 15 on a flat of 8, u = 2 on a flat of 4. Scores 768, 288, 192, 0.
- p = 2, beam 60 (`k6_S60.out`): a quadric after 5 (flats of 16, 16, 8, 4, 2; `anf64.out` has its polynomials, degree 5
  in between, no structure that I can see); p = 2 with beam 6,000 and p = 4 with beam 2,500 found nothing within 4
  (`k6_S6000.out`, `k6_S2500_p4.out`): the guide matters, and a beam's silence says nothing.
**So j(6, 1) = 4.** The first two exchanges of the 4-path go along the same direction u = 11, so together they are
one exchange on the symmetric difference of the two flats: 24 addresses, a union of three flats of 8 and of no two
flats [ran: `compose.py`, `compose.out`, which also replays the merged 3-exchange path]. **So j(6, 3) = 3 = k/2**, and
this path gives only j(6, 2) <= 4.

| j(k, c) | c = 1 | c = 2 | c = 3 | Lemma D, c = 1 / 2 / 3 |
|---|---|---|---|---|
| 16 points | 2 | 2 | 2 | 1 / 1 / 1 (and 2 by Lemma H) |
| 64 points | 4 | 3 or 4 | 3 | 2 / 1 / 1 (and 2 by Lemma H) |

Price of the 4-exchange product by the table of section 1 [derived, not built]:
56 + 56 + 60 + 62 = 234 gates per side, 2 x 234 + 124 = 592 gates at 64 points (textbook 384, night's best 304).
**Growth: j(k, 1) = 2, 4 and j(k, 3) = 2, 3 at k = 4, 6.** For single flats that is twice Lemma D's k/2 - 1 both
times: if it is k - 2 the family costs about 2 N log2 N, if it is 2^(k/2 - 1) it is N^1.5; two points do not decide.
For unions of three it is k/2 both times, the value the brief called "ties the textbook" (in count of exchanges; in
gates the family is dearer, since a union of three flats costs up to three times a flat). Nothing here grows more slowly
than k. The anomaly to keep: **each unit of D costs two single-flat exchanges, not one, and the pair that works shares
its direction.**

**Price of one found product, built** [ran: `build16.py`, `build16.out`, exact fractions]. Start {4,6,8,10,12,14};
exchange 1: u = 1 on the plane {0,1,4,5}; exchange 2: u = 3 on the plane {0,3,8,11}; result {5,6,10,11,12,14}, a
quadric. Circuit Phi2, Phi1, C_start, Phi1, Phi2 with 14, 14, 30, 14, 14 gates: **86 gates**; it equals the convolution
of the quadric on all 256 entries, and 4 times that matrix is (-1)^(q(x) + q(z) + B(x, z)) with B bilinear and
invertible, i.e. the 16-point transform up to free signs and one relabelling.

## 4. Going around, four times

**(a) Change the start.** Any cheap pattern will do. Lemma D still gives (D(start) - k/2)/c, and every pattern I can
price has D >= k - (its number of flats). At 16 points the middle class (a plane plus a line, two flats) is one
exchange from the quadric; its convolution costs about 58 by the obvious circuit [derived, not built], so 58 + 28 = 86
again.

**(b) Let T be anything cheap, not a union of flats.** By section 1 the cost of an exchange is the cost of a sign
convolution with spectrum t on N/2 points: the original problem one bit smaller. Two candidates. A *decision list*
(an interval of addresses in dictionary order: up to k nested flats whose projector costs O(N) in all, the Haar
transform [derived, not built]): by the proof of Lemma D it lowers D by at most 1, however many flats it has [derived]. A *smaller
quadric*: point 8 of section 0. In general the fall of D on a flat G is at most the codimension of the largest subflat
of G on which t is constant, so the wanted object is **a sign pattern with a linear-size convolution that is constant on
no large subflat of large flats**, which is the transform's own question.

**(c) Nest instead of composing.** Let T itself be "a cheap pattern after one exchange", and so on down. Level i acts
on N/2^i points but is needed 2^i times, because a conjugation uses its conjugator twice: every level costs the same,
and Lemma D needs k/2 levels. Tie [derived]. If a controlled swap could be had for ONE application of its sign
convolution instead of two, this tower would be a geometric series and the transform would be linear; I found no
identity of that kind. (The one-sided rule that does exist, C[f + g] = C[f] C[g], needs t on all four quarters.)

**(d) Let the conjugator be anything.** Every conjugator of the start into the quadric is (a permutation conjugator)
x (anything commuting with the start's convolution); its columns are a basis of the mirror and of its complement. That
is g-0's question (24 gates for the mirror at 16 points, route ties 56) [read], so the permutation conjugators are a
thin slice of something already priced once.

**Why (a) to (c) tie: the accounting by restrictions** [derived; ran the identities in `mux16.py` parts 2 and 3].
Cut by the bit along u: C[f] costs at most C[f0] + C[f1] + 2N on the two half-size arrays. The exchange turns the pair
(f0, f1) into (mux(t; f0, f1), mux(t; f1, f0)) for 2 x cost(t). For the quadric y1 y2 + Q', the pair is
(Q', y2 + Q'); whatever t is, the pair before the exchange still equals Q' on y2 = 0 in both arrays, so two quarter
copies of Q' remain, and on y2 = 1 the arrays are e and e + 1 with t = Q' + e there. Total
2 cost(Q') + 2 cost(Q' + e) + 2 cost(e) + O(N), and cost(Q') <= cost(Q' + e) + cost(e): **at best 4 cost(Q') + O(N)**.
This is aa-cross's wall REPAY once more, here with a one-line proof, but ONLY inside this accounting: it assumes an
array costs the sum of its restrictions. Two exchanges along different directions are not covered by this argument (the
untouched region is no longer a hyperplane).

**Ailon's potential** [ran, FLOATS, `mux16.out` part 4; the bound itself is recalled]. Potential of an orthogonal matrix
= minus the sum of M_ij^2 log2 M_ij^2; 0 for the identity, N log2 N for the transform. Along the 86-gate product:
16, 32, 41.7, 48, 64. The conjugator Phi1 Phi2 alone holds 32 bits = half of the transform's 64 for 28 gates (1.14 bits
per gate, better than the textbook's 1); the cheap start earns 9.7 bits with 30 gates. Every stage of an exchange
program is orthogonal and every flat reflection on m points is 2m - 2 rotations, so the whole class is a rotation
program and is capped at order N log N by that potential. A conjugator that beats it must be computed through
intermediate wires that are far from orthogonal, even though the conjugator itself is a product of reflections.
[derived, a sketch only] A four-point reflection can raise a row's potential by at most 2 bits; an exchange made of
them touches half the rows on the left and half the columns on the right, so it adds about 2N bits at most, and
k N bits are needed: j >= k/2 for flats of dimension k - 2. That is 2 at 16 points (attained) and 3 at 64 (not
attained by single flats: the truth is 4).

## 5. The wall, and what the experiment turned into

**Wall (BENT, in the form "one unit of D per flat, about N gates per flat, and every conjugator used twice").** Exactly:
(i) Lemma D; (ii) the price table of section 1 (an upper bound for each reflection: I did not prove that a reflection on
m points needs 2m - 1 gates); (iii) conjugation. Together: exchange programs built from flats, priced this way, cost
(7/8) N log2 N - O(N) or more. They are also rotation programs (Ailon). The measured counts are worse than Lemma D
predicts (2 and 4 against 1 and 2 for single flats).

**The question it turned into.** The textbook recursion is 4 T(N/4) + 2N, and 3 T(N/4) + O(N) would be linear. The
exchange is a legal move that lets two arrays trade spectral components for two sign convolutions. One exchange
provably ties in the accounting by restrictions. **Do two exchanges along different directions, with arbitrary T,
ever cost less than the product rule says, when every piece is priced exactly?** That is decidable at 16 points: all
pairs (u1, T1), (u2, T2) carrying some pattern g to the quadric (the backwards test of section 2 enumerates them), with
g, T1 and T2 priced by exhaustive minimum circuits on 8 and 16 points (`d-0-zeta/` mincirc). A single case with
cost(g) + 2 cost(T1) + 2 cost(T2) below 52 would be the first specimen of sharing that is not repaid.

## 6. Mutations for the next wave

1. **two-exchange audit** (the question above; 16 points, exact pricing of every piece).
2. **two exchanges per unit of D**: j(k, 1) = 2, 4 against Lemma D's 1, 2. Find the invariant that makes it so
   (candidates: the number of flats of each dimension on which the pattern is constant; the sum over v of |r(v)|, which
   guided the beam to the 4-path when the sum of squares did not), prove j(k, 1) >= k - 2 or find the third value at
   256 points with the same beam (masks of 256 bits; `k6.c` mode S is the template). k - 2 against 2^(k/2 - 1) is the
   whole question for this family: 6 or 8 at 256 points.
3. **one-sided swap**: is there any pair of patterns (f, f after an exchange) whose convolutions differ by ONE
   application of a sign convolution with spectrum t on N/2 points plus O(N) gates? A yes makes tower (c) a geometric
   series. Smallest case: 8 points, t a single point, exhaustive.
4. **decision-list exchanges**: T an interval in dictionary order costs O(N) for up to k flats; Lemma D says one unit
   of D each. Run the breadth-first search at 16 and 64 points with intervals in ALL bit orders as the move set and see
   whether j falls below what single flats need (it cannot fall below k/2 - 1).
5. **start from the middle**: at 64 points list the patterns that are one single-flat exchange from the quadric and
   price their convolutions; the D-count says none is cheap, the list would say how far from cheap.

## 7. Criticism, last

- The brief asked for j(k, c) at 64 points. I give j(6, 1) = 4, j(6, 3) = 3 and j(6, 2) in {3, 4}. Deciding class 2
  needs two class-2 exchanges before the arbitrary one, far too many to list; a meet-in-the-middle needs canonical
  forms under the affine group, which I did not write.
- The lower bound 4 for single flats rests on the recogniser "one exchange with any T from a quadric" (section 2),
  whose completeness is a derivation of mine; its controls test planted cases only.
- The three-orbit reduction of the first exchange is argued by hand (transitivity of the stabiliser on three kinds of
  direction), not run. The positive controls test the recognisers, not this reduction.
- Lemma D's machine check is nearly empty at 16 points (D takes two values). The proof is five lines; read it.
- "An exchange costs one sign convolution on N/2 points" is exact for one exchange, but the prices in the table are
  my circuits for flats (upper bounds), and a product of exchanges may cost less than the sum of its factors. Nothing
  here bounds that from below except Ailon's potential, which I quote from memory and from tonight's reports, and
  which covers rotation programs only.
- Two jobs on the rented machine (class 3, two of the three orbits) were stopped by their 20-minute limit before
  printing anything; the same runs were then done on this Mac in halves. Nothing was lost but time.
- Point 8 of section 0 and section 4's "one exchange can only tie" hold in an accounting that prices an array by the
  sum of its restrictions. That is the direct-sum assumption, not a theorem.
- The 86-gate circuit is far above 52. It was built because the brief asked for a priced product, not as a candidate.
- The start of the brief is a poor one (Lemma H); I kept it because the brief fixed it, and report the middle class.
- Nothing here changes the order, or any constant.

Files: `waves/wave-09/ad-3-straightenquadri/` : bfs16.c, bfs16.out (16 points,
exhaustive distances and the Lemma D check); k6.c (64 points: modes A, B, C, P), k6_A.out, k6_B1.out, k6_B2.out,
k6_C.out, k6_P.out (controls), k6_B3_0a/0b/1a/1b/2a/2b.out (class 3, three orbits in halves), k6_S2500_p1.out (the
4-exchange path), compose.py, compose.out (its first two exchanges merged: class 3 in 3), k6_S60.out, k6_S6000.out, k6_S2500_p4.out (other beams), anf64.py, anf64.out (polynomials along the
5-exchange path); build16.py, build16.out (the dictionary and the 86-gate product);
mux16.py, mux16.out (the mux identity, the untouched hyperplane, the potential in floats).
