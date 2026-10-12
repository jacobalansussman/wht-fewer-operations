# ai-2 (skeptic): the two determinant ledgers hold and are Morgenstern's 1973 argument; the conclusion drawn from hybrid 2 does not hold as written: subset sums have a volume of their own, of order N sqrt(log N)

> Editor's note (11 October 2026): the title says that two counts "are Morgenstern's 1973 argument". The author of this report did not open Morgenstern's paper and knew it from two later papers. What this report says about published work is as its author marked it: read through a tool that summarises, from an abstract, second hand, or from memory. See [Earlier papers](../README.md#earlier-papers).

11 October 2026, wave 10 skeptic, label ai-2, 30-minute box (about 09:26 to 09:50 EDT). Private. One agent; nothing reviewed,
nothing in Lean, nothing published. Marks: [ran] = computed by me in this box with my own code, exact (whole numbers or
fractions) unless I say "floating point"; [derived] = argued by hand here, checked by nobody; [read] = from a file or a
web page I opened; [recalled] = from memory, no source opened; [guess].
Gate count everywhere: **(G)**, a gate is any a*u + b*v, scalings free. Count (O), OpenAI's, is not used.
Folder F = `waves/wave-10/ai-2/`.

**No circuit, no saving exponent, nothing of the 1e-1 kind. Both ledgers are lower bounds for restricted circuits only.**

Words. N = 2^k points. H: the transform, entries (-1)^(number of common ones of the two addresses). Z: *subset sums*,
Z[T][x] = 1 when x is a subset of T. *Minor*: the determinant of a square piece of a matrix (any rows, any columns);
its *order* is its number of rows. *Primitive* wire: whole numbers with no common factor (or polynomials with no common
factor). *Flat* wire: entries 0, +1, -1. *Halving*: a gate (u +- v)/2. *Class identity*: a circuit with coefficients that
are functions of a letter and that computes the k-th power of a 2 x 2 block (the *kernel*) for every value of the letter.
*Singular values* of a matrix M: the square roots of the eigenvalues of M^T M; they measure how much M stretches volume.
*Bounded coefficients*: gates a*u + b*v with |a|, |b| at most a fixed number and NO free rescaling of wires.

## 0. Verdict in eight lines

1. **ag-1's ledger is a theorem** [derived again, two lines; ran at 4, 5, 6 inputs and on the 19-gate circuit]. It is
   Morgenstern's 1973 determinant argument with one choice added (every wire scaled to be primitive), which is what makes
   it meaningful in count (G). Nothing in it is new except the wording "a halving weighs 0".
2. **The flat-gate list is complete for every number of inputs** [derived + ran]: u +- v, u +- 2v, (u +- v)/2 and nothing
   else, with no limit on the coefficients tried. So "flat circuits need 0.3155 N log2 N gates besides halvings" holds.
3. **The class ledger is a theorem too** [derived again; ran at 8 points]: the same argument with "degree in the letter"
   in place of "size". The 8-point numbers that ah-cross read off ag-6's table are right: weights 1 (nine gates),
   2 (eight), 3 (two), 31 in all against a need of 24. I solved every gate as an identity in the letter.
4. **Gates of negative weight cannot cheat** [derived + ran]: the ledger's quantity is a maximum over a set of wires that
   only grows, so it never falls. 60 gates of negative weight in my random circuits: the largest minor grew on none.
5. **"Over all orders" does no harm to the ledgers** [ran]: the bound holds order by order. But it is exactly where
   hybrid 2 went wrong: for Z the determinant is 1 and the large minors sit at orders near 0.4 N to 0.5 N.
6. **Hybrid 2's table**: 1 at 4 points and 2 at 8 points are right; at 16 points the largest minor is **exactly 5**
   [ran, every minor, 35,059,677 up to symmetry], so the uncontrolled search had found the maximum; at 32 points
   "at least 16" is beaten by an explicit minor, **48** [ran].
7. **Hybrid 2's conclusion fails as written.** "Z has no volume at all" and "for Z no volume count forbids even a
   circuit of O(N) additions and subtractions with coefficients +1 and -1" are false for large N: the largest minor of
   Z is 2^(c N sqrt(log2 N)) with c tending to 0.277, so by Morgenstern such a circuit has at least
   0.277 N sqrt(log2 N) - N gates [derived from known lemmas; small cases ran]. Nearest true statement in section 4.
8. What survives for the user: in count (G), where coefficients are free, no volume argument forbids linear size for Z
   or for H. That was known in 1973. What changes is the picture "the whole ledger sits on one diagonal": it does not.

## 1. The two claims, stated exactly

**A (ag-1, whole numbers).** Scale every wire of a circuit to be a primitive whole-number vector. A gate then reads
w = (a u + b v)/c with a, b whole numbers without common factor and c the common factor of the entries of a u + b v;
(a, b, c) is determined by the gate up to sign. Let D_m be the largest absolute value of a minor of order m of the matrix
whose rows are all the wires made so far. Then after the gate D_m is at most max(1, (|a| + |b|)/c) times what it was,
for every m. Since the N outputs of H have determinant N^(N/2):
**sum over gates of max(0, log2((|a| + |b|)/c)) >= (N/2) log2 N.**
Corollary: if every wire is flat, each gate weighs at most log2 3 and a halving weighs 0, so the gates that are not
halvings number at least (N/2) log2 N / log2 3 = 0.3155 N log2 N.

**B (ah-cross hybrid 1, degree in a letter).** Kernel (1, 1; 1, tau). Keep every wire as a vector of polynomials in tau
with no common factor. A gate is w = (a u + b v)/c with polynomials a, b (no common factor) and c; its weight is
max(deg a, deg b) - deg c. The largest degree of a minor of order m rises by at most max(0, weight). The outputs have
determinant (tau - 1)^((N/2) log2 N). **So the positive weights add up to at least (N/2) log2 N**, and a class identity
ALL of whose gates have weight at most 1 has at least (N/2) log2 N gates of weight exactly 1. (The task's short form
"gates of weight at most 1 number at least (N/2) log2 N" needs the word "all".)

Proof of both, in one line [derived]: a minor through the new row equals (a M_u + b M_v)/c, where M_u and M_v are the
same minor with the new row replaced by u and by v; take sizes (A) or degrees (B). Minors not through the new row are
old. Neither is a circuit; both are lower bounds, and only for circuits whose weights are capped.

## 2. What I checked myself  [ran; programs and outputs in F]

| claim | authors' check | mine | result |
|---|---|---|---|
| flat-gate list | 3, 4, 5 inputs, coefficients up to 4 | 4 and 5 inputs, coefficients SOLVED from the three wires, no limit (`flat.py`) | 540 + 232 + 116 and 4,020 + 1,320 + 660 gates of the three kinds, no other kind: the same counts as ag-1 |
| ledger A on random circuits | 2,400 gates, 4 inputs | 2,100 gates at 4 inputs (every order separately), 1,400 at 5 and 420 at 6 inputs (top order); coefficients up to 9; 376 gates with an even common factor, 60 of weight below 0 | 0 violations; the largest minor grew on no gate of weight below 0 |
| 19 gates at 8 points | 26.02 | replayed from the file: computes H, every wire flat, 7 gates u +- v and 12 gates u +- 2v | 26.02 against a need of 12 |
| least weight of a flat circuit at 4 points, halvings free | 8 (depth-first search) | 8.0 (my own shortest-path search over sets of the 40 flat wires, 19,113 states settled) | the same |
| ledger B | four circuits at 4 points; 8-point weights read off ag-6 | 8 points, kernel (1, t; t, 1): the 19 wires as vectors of powers of t, every gate solved as c w = a u + b v and checked as an identity in t on all 8 coordinates (`classledger.py`) | weights 1 x 9, 2 x 8, 3 x 2 = 31; need 24 (the determinant is (1 - t^2)^12); the proof's inequality on 1,051 sampled non-zero minors of order 8: 0 violations, attained 528 times |
| largest minor of Z | all minors at 4 and 8 points; hill climbing at 16 and 32 | all minors at 4, 8 AND 16 points (`zmax16.c`); explicit minors to 2,048 points (`zvol.py`) | 1, 2, 5; at least 48 at 32 points |

Why 4 and 5 inputs settle the flat-gate list at every size [derived]: whether (a u + b v)/c is flat is decided coordinate
by coordinate, and it depends only on which pairs (u_i, v_i) occur. Up to sign there are four non-zero pairs: (1, 0),
(0, 1), (1, 1), (1, -1). Four coordinates show every combination; a fifth adds the pair (0, 0). By hand: (1, 0) and
(0, 1) present forces u +- v; (1, 0) with one of the mixed pairs forces u -+ v or u -+ 2v; only the two mixed pairs
(same support) forces (u +- v)/2; (1, 0) with both mixed pairs admits no gate.

Honest limits of my checks. In the 8-point check of B the wire vectors are read from ag-6's listing at t = 3 (every
entry there is a power of 3, so the exponents are unambiguous); the gates, their weights and the identity in t are mine.
The outputs are the rows t^(Hamming distance) after one relabelling of addresses (0,1,2,3,7,6,5,4) [ran]. I did not
check B for the kernel (1, 1; 1, tau) at 8 points, and I did not re-run ah-cross's four 4-point circuits. The least
flat weight at 8 points (ag-1's open question, is it 24?) is beyond this box: 3,280 flat wires.

## 3. The attacks, one by one

**Normalisation of wires.** In count (G) scalings are free, so a determinant bound means nothing until the scale of
each wire is fixed. "Primitive" fixes it canonically, and then (a, b, c) is a property of the gate, not a choice
[derived]. The price: the weight (|a| + |b|)/c of a general gate is unbounded, so A bounds only circuits whose wires
are restricted (flat, or entries of bounded size). This is the usual bounded-coefficient restriction in other clothes.
For B there is a second freedom that the authors did not mention: the weight depends on the letter chosen. With
s = 1/(tau - 1) the kernel's primitive rows are (1, 1) and (s, s + 1), their determinant is 1, and the same lemma
gives a need of 0 [derived]. With t, tau = t^-2, the need is N log2 N instead of (N/2) log2 N. Each is a true
statement; "weight at most 1" is a restriction relative to a coordinate and not a property of the circuit.

**Negative weights.** No cheat is possible [derived]: the quantity is the largest minor (or largest degree) over ALL
wires made so far, a set that only grows; a gate of weight below 0 contributes 0, not a credit. What a division does
do is lower the weight of the gate it sits in: in the 19-gate identity two gates divide by t (g8 and y5), and without
that the sum would be 33, not 31 [ran]. A halving is the whole-number case of this.

**"Largest minor over all orders".** Harmless for A and B: the inequality holds order by order [ran at 4 inputs], and
only "the final value is at least the determinant of the outputs" is used. The order matters in the other direction:
Morgenstern's bound for a target matrix is the logarithm of its largest minor of ANY order, not of its determinant.

**Only four circuits at 4 points; 8-point weights read off a table.** Repaired above: 8 points computed, 31 against 24.

**The conclusion from hybrid 2.** Section 4.

## 4. Where it fails: Z has volume  [derived from known lemmas; small cases ran]

ah-cross, hybrid 2: "Z and its transpose have no volume at all", "for Z no volume count forbids even a circuit of O(N)
additions and subtractions with coefficients +1 and -1", hence "walls M, DEPTH and LEVELS say nothing about linear
size; what stands between the night and O(N) is REPAY alone".

Three facts.
1. [ran] The sum of the squares of all minors of order r of a matrix M is the r-th coefficient of det(1 + x M^T M)
   (Cauchy-Binet). Checked for Z at 4 and 8 points against every minor: 9, 16, 9, 1 and 27, 193, 594, 870, 594, 193,
   27, 1.
2. [derived] Z is the k-th power of the block (1, 0; 1, 1), whose singular values are phi = 1.618 and 1/phi. So the
   singular values of Z are phi^(k - 2j), C(k, j) times each. The sum of log2 over those above 1 is
   U(k) = log2(phi) * k * C(k-1, floor((k-1)/2)), which grows like **0.277 N sqrt(log2 N)**.
3. [derived] Hence log2(largest minor of Z) lies between U(k) - N and U(k). (Upper: a minor of order r is at most the
   product of the r largest singular values. Lower: fact 1, and there are at most 4^N minors.)

| points | largest minor of Z | how | upper bound 2^U | H's determinant |
|---|---|---|---|---|
| 4 | 1 | every minor [ran] | 2^1.4 | 2^4 |
| 8 | 2 | every minor [ran] | 2^4.2 | 2^12 |
| 16 | 5 (order 7 or 9) | every minor [ran] | 2^8.3 | 2^32 |
| 32 | at least 48 (order 10) | explicit, elimination [ran] | 2^20.8 | 2^80 |
| 64 | at least 1,458 (order 15) | the same | 2^41.7 | 2^192 |
| 128 | at least 47,775,744 (order 35) | the same | 2^97.2 | 2^448 |
| 256 | at least 9,760,764,780,783,360 (order 56) | the same | 2^194.4 | 2^1024 |
| 512, 1,024, 2,048 | at least 2^109, 2^243, 2^453 | eigenvalue formula, checked against elimination up to 256 points | 2^437, 2^875, 2^1924 | 2^2304, 2^5120, 2^11264 |

The explicit minor: rows = the sets with k - s elements, columns = the sets with s elements; the entry says "the small
set is inside the large one", that is "disjoint from its complement". At 32 points with s = 2 it is the adjacency
matrix of the Petersen graph, determinant 48. Its determinant in general is the product of C(k-s-j, s-j) to the power
C(k, j) - C(k, j-1) [recalled, the eigenvalues of the Kneser graph; ran against elimination in 14 cases].
The rigorous lower bound from fact 3 is weak at small sizes and becomes positive at 1,024 points (2^24.8; 2^123 at
2,048) [ran, exact coefficients]; per point it is 0.05 at k = 14, 0.57 at k = 32, 1.00 at k = 52, 1.77 at k = 100,
7.76 at k = 1,000, always within N of U(k) [ran, `zgrowth.py`, floating point].

**Consequence (Morgenstern).** A circuit for subset sums whose gates are a u + b v with |a|, |b| at most 1 has at least
log2(largest minor of Z) >= 0.277 N sqrt(log2 N) - N gates. In ag-1's ledger: a flat circuit for Z has at least that
number divided by log2 3 of gates that are not halvings. So O(N) additions and subtractions for Z IS forbidden by a
volume count. The bound passes the trivial count N - 1 only beyond about 2^52 points, so it is a statement about order,
not about any size one can run.

**Nearest true statement.** The volume of Z is of order N sqrt(log N): smaller than the transform's (N/2) log2 N by
the factor 1.8 sqrt(log2 N), and not zero. In H = Z D Z^T the diagonal D does not carry the whole ledger; with
bounded coefficients each factor Z must pay about 0.277 N sqrt(log2 N) itself. A linear program for Z needs wires that
are not flat, as one for H does; only the height of the wall differs (sqrt(log N) per gate instead of log N).
With free coefficients (count (G)) no volume argument says anything, for Z or for H. That part of ah-cross's sentence
is right, and it is the classical situation, not a finding about Z.

## 5. Is it known?

- **Ledger A: known.** J. Morgenstern, "Note on a lower bound of the linear complexity of the fast Fourier transform",
  Journal of the ACM 20 (1973) 305-306: with coefficients of size at most 1 the largest minor of any order at most
  doubles per gate, so the transform needs (1/2) n log2 n gates [read: the J. ACM bibliography page and the summaries
  in the two papers below; I did not open Morgenstern's text]. A gate (u + v)/2 has |a| + |b| = 1 there, so "a halving
  weighs 0" is already inside the 1973 statement. ag-1's addition is the primitive scaling and the constant 0.3155
  for flat wires (Morgenstern's own form with coefficients up to 2 gives 0.25).
- **The singular-value form: known.** B. Chazelle 1998 [recalled]; R. Raz 2002 [recalled]; P. Buergisser and M. Lotz,
  "Lower bounds on the bounded coefficient complexity of bilinear maps", arXiv cs/0301016 (2003), who extend
  Morgenstern's bound "in a unitarily invariant way" to singular values and show that the n log n bound survives up to
  (1 - epsilon) n gates with unbounded coefficients ("help gates") [read: abstract and search summaries only].
  Section 4 is that theory applied to Z. I did not find the number 0.277 N sqrt(log N) for subset sums stated anywhere;
  in a 30-minute box that means little. Find, Goos, Jarvisalo, Kaski, Koivisto and Korhonen, "Separating OR, SUM and
  XOR circuits", arXiv 1304.0513, say the existence of small circuits for the zeta transform "is not currently
  understood satisfactorily" [read: search summary].
- **Ledger B: the method is the same; I did not find the degree form stated.** It is a two-line variant and I would not
  call it new without a real search.
- N. Ailon, arXiv 1305.4745 and 1403.1307 [read: titles and abstracts in the search results]: a lower bound of order
  (n log n)/R for the Fourier transform in an "R-well-conditioned" model. Same message from another side.
- **What the known theory predicts for "linear or not".** With bounded coefficients or flat wires: never, the order is
  n log n (1973). With free coefficients: no superlinear lower bound is known for any explicit matrix [recalled], so
  theory forbids nothing and offers nothing. A linear program must have, on most gates, coefficients (after removing
  common factors) of size a power of N; Buergisser and Lotz add that fewer than (1 - epsilon) n such gates are not
  enough for their problems. In H = Z D Z^T the diagonal is exactly n such gates, at the edge of that theorem [guess
  that their theorem transfers to H; not checked].

## 6. Does it scale, and what it gives in the user's terms

- Growth laws observed. Ledger A: need (N/2) log2 N at every size (a theorem); spent 8 and 24 by the textbook at 4 and
  8 points [derived], 26.02 by the 19 gates [ran]. Ledger B in the letter t: need N log2 N; spent 24 by the textbook [derived], 31 by the
  19 gates [ran]. Largest minor of Z: 1, 2, 5, at least 48, ...; log2 of it is 0.277 N sqrt(log2 N) up to an error of
  at most N [derived].
- In the user's terms: **nothing yet.** No circuit size, no saving exponent. The ledgers say where a linear program
  cannot be (flat wires; class identities with weights capped), and section 4 adds that the subset-sum route is under
  the same restriction.
- One question this leaves, the only thing here that touches the bar [guess, no evidence for it]: with coefficients
  +1 and -1, subset sums are known to cost at most (N/2) log2 N (Yates) and, by section 4, at least about
  0.277 N sqrt(log2 N). If a circuit met the lower figure, T(N) <= 2 f(N) + N would give the transform in
  O(N sqrt(log N)) gates, an exponent of 1/2. Every count of the night (12 gates at 8 points, the minimum modulo
  2, 3, 5, 7 [read: d-0]) sits at Yates, so the evidence is against it; but the gap between the two figures is real,
  and no argument I know closes it. The cheapest test: the least number of +-1 gates for Z at 16 points, where Yates
  spends 32 and the volume asks 2.3.
- The sqrt(log N) here and the one in ah-cross's hybrid 4 (the window of degree about 5 sqrt(k)) are the same
  concentration of a sum of k coin flips [derived]; I did not pursue whether that is more than a coincidence of form.

## 7. Criticism of my own report

- Section 4's lower bound uses Morgenstern's theorem for a minor of any order as I recalled it and as two secondary
  sources describe it; I did not open the 1973 note. My own two-line proof (section 1) covers it.
- The explicit minors beyond 256 points are from a recalled eigenvalue formula, checked by elimination in the 14 cases
  up to 256 points only.
- The 16-point search uses floating-point elimination to scan and exact whole numbers only to recheck the winner of
  each order; determinants there are whole numbers below 2^20, so rounding is safe, but it is not an exact scan.
- The published engine lives in a RAM cost model, not in linear circuits; none of this was compared with it [guess:
  it is not a flat circuit, as by 1973 it cannot be].
- I searched the literature for a few minutes. "Not found" is not "new".

Files in F: `flat.py`, `flat.out`; `classledger.py`, `classledger.out`; `zvol.py`, `zvol.out`; `zgrowth.py`,
`zgrowth.out`; `zmax16.c`, `zmax16`, `zmax16.out`. All runs through `light.py`, each under 40 seconds.

Sources opened or returned by search: https://projects.csail.mit.edu/jacm/References/morgenstern1973:305.html ;
https://arxiv.org/abs/cs/0301016 ; https://ar5iv.arxiv.org/html/1305.4745 ; https://ar5iv.labs.arxiv.org/html/1403.1307 ;
https://arxiv.org/pdf/1304.0513 ; https://arxiv.org/html/2509.14489v1 (Kronecker powers and the disjointness matrix,
2025, title only).
