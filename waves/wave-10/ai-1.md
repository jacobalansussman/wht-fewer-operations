# ai-1: the private-wire lemma and the floor 2N - o(N), checked

> Editor's note (11 October 2026): what this report says about published work is as its author marked it: read through a tool that summarises, from an abstract, second hand, or from memory. Nobody checked those statements against the sources. Two older papers that the night's searches did not reach were read afterwards. See [Earlier papers](../README.md#earlier-papers).

11 October 2026, about 09:27 to 10:00 EDT. Private research: nothing published, no git, no Lean.
Object: ag-7.md section 4 and the files `ag-7-rankdial/private.py`, `lemma_ad6.py`, `law.py` with their outputs;
ah-cross.md section 2 ("RELATION-LENGTH") rests four reports on it.
Marks: [ran] = exact run of mine in this half hour, files in `ai-1/`; [derived] = by hand in this half hour, read by
nobody else; [read] = opened and read today; [recalled] = from memory, no source opened.
Gate count: **(G)** throughout, a gate is any a*u + b*v with scalings free. Count (O) is not used.

## Verdict in six lines

1. **The lemma is true over the two-element field, for every circuit, and the step from the graph to the number of
   gates is sound.** I re-derived both and found no gap. [derived]
2. **The table is right.** Every entry of ag-7's floating-point table agrees with my exact whole-number recomputation to
   the last printed digit or one unit below it (rounding). The recalled graph theorem is the right theorem. [ran]
3. **As ah-cross states it (no field named) the lemma is false over the rationals**, at the smallest size: 8 points,
   degree 2, a cycle of length 3 where the statement allows none shorter than 6. [ran, exact] ag-7 itself says this;
   ah-cross and ag-0 ("two authors, two fields") dropped the restriction. The user's model is over the rationals.
4. **The nearest true statement over the rationals** is about pieces with two cycles, not about cycles. I worked out
   the constant ag-7 left open: the floor arrives **three degrees later** than over the two-element field. [derived]
5. **Growth law: linear, with a ceiling of 2N.** L(d, k) >= N (1 + 2 / (1 + 2^(k / 2^d))) - rank. The method can
   never give more than 2N - rank, because a forest already satisfies the graph condition. [derived + ran]
6. **In the user's terms: nothing.** No circuit, no exponent. For the transform itself it gives less than a two-line
   count (2N - 2). Known theory says a hypothesis of this kind can never produce a floor above linear.

## 1. The claim, stated exactly

Words. N = 2^k *addresses* y (k bits). The object M(d, k) has one input c_S for each set S of at most d bits and one
output for each address: output(y) = sum of the c_S with S inside y. *Rank* R = number of such sets. A *relation* is a
set of outputs that, with non-zero coefficients, add to zero whatever the inputs. *delta* = the fewest outputs in a
relation. A *wire* is an input or the result of a gate. V = the number of wires that are not outputs (inputs count).

**Claim A (delta).** For M(d, k), delta = 2^(d+1) over every field; no relation at all when d >= k.

**Claim B (the lemma; two-element field; any N different outputs with delta > 4; any circuit).**
Each output that is not an input is made by one gate o = u + v. Then
(c) u and v are never both outputs;
(a) if exactly one of them is an output, call the other the *label* of o: no wire is the label of two outputs;
(b) otherwise draw an edge between u and v. Add one vertex z and an edge from z to each label.
The graph has V + 1 vertices, one edge for each output that is not an input, and **no cycle shorter than delta - 2**.

**Claim C (gates).** For M(d, k): gates = N + V - R, and the graph forces
N - 1 <= ((V+1)/2) (1 + ((V+1)/2)^(1/(2^d - 2))). So outputs per non-output wire <= (1/2)(1 + N^(1/(2^d - 2))), and
L(d, k) >= 2N - o(N) "from degree about log2 k on".

**Claim D (rationals).** "The same holds with a weaker graph condition and a constant I did not work out."

## 2. Verified with my own code

All programs are mine, written without reading ag-7's beyond their headers. Runs under `light.py`.

| what | how | result | file |
|---|---|---|---|
| Claim A, two-element field | every relation listed (the whole space, up to 2^22 vectors) | shortest = 2^(d+1) in all 12 cases decided, 4 to 64 points, d = 1 to 5 | `delta.py`, `delta.out` |
| Claim A, rationals | every set of 2^(d+1) - 1 outputs tested for independence modulo 1000003 (independent modulo a prime implies independent over the rationals) | all independent: 8 points d = 1, 2; 16 points d = 1, 2, 3; 32 points d = 1, 2 (3,365,856 sets) | same |
| Claim B on circuits that are NOT minimum circuits | 1,540 random circuits, 8 to 128 points, d = 2 to 5, 11 to 4,430 gates | no gate adds two outputs; no repeated label or edge; shortest cycle 6 at 8 points (claim: at least 6), none elsewhere | `anycircuit.py`, `anycircuit.out` |
| Claim C, the table | bisection, then the threshold confirmed by two exact whole-number tests | agrees with `law.out` everywhere (see below) | `moore_exact.py`, `moore_exact.out` |
| one size further | the same at 2^256 points | below | `moore_256.out` |
| Claim B over the rationals | exact fractions | false: a triangle | `rational.py`, `rational.out` |

Honest limit of the random test: random circuits almost never close a cycle away from 8 points, so the cycle clause is
tested by the proof, not by the run. ag-7's own checks (654 + 2,802 minimum circuits, ad-6's family) I did not re-run.

**The proof of Claim B, re-derived [derived].** Merge wires that carry the same form; the count cannot rise.
(c) o = u + v with three outputs is a relation of 3 terms. (a) Two outputs with one label give o1 + u1 = o2 + u2. If
the four are different that is a relation of 4 terms. If u1 = u2 then o1 = o2. If o1 = u2 and u1 is not o2 then
u1 = o2 after cancelling, a contradiction; if o1 = u2 and o2 = u1 the two gates read each other, impossible in a
circuit. Cycle: give each vertex its form and z the form 0; around a cycle every vertex is counted twice, so the edge
values add to zero. An edge of kind (b) is worth its output; an edge at z is worth o + u. A cycle of length L passes z at
most once, so the sum is L different outputs plus at most 2 more. After cancelling, between L - 2 and L + 2 outputs
remain, at least one. That is a relation, so L + 2 >= delta. **No gap found.**

**The step to gates, re-derived [derived].** gates = (outputs that are not inputs) + (non-output wires that are not
inputs) = (N - 1) + (V - (R - 1)) = N + V - R, because c_0 is the only input that is an output. The graph theorem
(Alon, Hoory, Linial 2002: v vertices, average degree D >= 2, no cycle shorter than 2r, then
v >= 2 (1 + (D-1) + ... + (D-1)^(r-1))) with r = 2^d - 1 gives the displayed inequality in two lines. In whole numbers
it reads: v vertices and e edges are forbidden exactly when (2e - v)^r > (e - v + 1) v^r; that is what I tested.
The theorem is as ag-7 recalled it; I also recalled it and did not open the paper. [recalled]

**The table, exact [ran].** gates / N at least (rounded down; "cert" in the file marks exact confirmation; only
d = 16 was left to 80-digit decimals):

| k | d = 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|
| 16 | 1.1088 | 1.3480 | 1.6415 | 1.7480 | 1.7063 | 1.5683 | | | | |
| 32 | 1.0077 | 1.1079 | 1.3809 | 1.6727 | 1.8396 | 1.9218 | 1.9594 | 1.9722 | 1.9664 | 1.8903 |
| 64 | 1.0000 | 1.0077 | 1.1065 | 1.3908 | 1.6695 | 1.8339 | 1.9181 | 1.9597 | 1.9802 | 1.9952 |
| 128 | 1.0000 | 1.0000 | 1.0077 | 1.1085 | 1.3955 | 1.6681 | 1.8311 | 1.9158 | 1.9582 | 1.9897 |
| **256 (new)** | 1.0000 | 1.0000 | 1.0000 | 1.0077 | 1.1130 | 1.3977 | 1.6673 | 1.8297 | 1.9146 | 1.9788 |

ag-7's entries differ from these by at most one unit in the fourth decimal (it rounds to nearest, I round down). Its two
rows at k = 8 differ in the third decimal because V must be a whole number; they describe nothing real.

## 3. Where it fails, and the nearest true statement

**Smallest failing case of the statement as ah-cross gives it [ran, exact fractions].** 8 points, degree 2,
rationals, delta = 8. Take the outputs o1 = out(a,b), o2 = out(a,c), o3 = out(b,c) and the three wires
w1 = (o1 + o2 - o3)/2, w2 = (o1 - o2 + o3)/2, w3 = (-o1 + o2 + o3)/2. None is a multiple of an output, and
o1 = w1 + w2, o2 = w1 + w3, o3 = w2 + w3. A circuit may compute these wires, so the graph has a cycle of length 3;
the statement allows none shorter than 6. Reason: three outputs in the span of three wires need not be dependent when
2 is not 0. With free coefficients the same is true of cycles of every length, even ones too.

**What survives over the rationals [derived].** (c) and (a) hold word for word (I checked the case u1 = u2, which the
two-element proof does not need: it gives a relation of 3 terms). For the graph: a connected piece with more edges
than non-z vertices gives a non-empty relation with at most twice as many terms as edges. (Non-empty: among the
outputs with a non-zero coefficient take the one made last; nothing later reads it.) So, with T = 2^d - 1:
**every connected piece with at most T edges has at most as many edges as vertices.** That is ag-7's sentence; it is
correct.

**The constant ag-7 did not work out [derived, unreviewed].** Let the graph have v vertices and (1 + eps) v edges.
Drop the pieces with at most one cycle. Two cycles of length at most T/4 lie more than T/2 apart (else their union with
a path is a piece with two cycles and at most T edges). Around each such cycle there are at least T/4 further vertices
within distance T/4 (else the piece, having a second cycle, would give a small piece with two cycles). So there are
fewer than 4v/T short cycles; delete one edge from each. What is left has no cycle of length T/4 or less and at least
(1 + eps - 4/T) v edges, and the graph theorem gives

    eps <= 4/T + (1/2) ((v/2)^(1/(r-1)) - 1),   r = floor((floor(T/4) + 1)/2),   about (2.77 k + 4) / 2^d.

Over the two-element field the same quantity is about 0.35 k / 2^d. A factor of 8: **three degrees later.**
Numbers (`rational.out`, floating point): at 2^64 points the floor over the rationals is 1.39 N at degree 8, 1.83 N
at degree 10, 1.96 N at degree 12, where the two-element field has these at degrees 5, 7 and 9.
For small degree the rational version says almost nothing: at d = 2, T = 3 and the only constraint is "two labels are
never joined by an edge". So **"N^(1/4) outputs per wire at degree 2, N^(1/8) at degree 3" are two-element statements
only**, and ad-6's girth bound for pairs of partitions does not transfer to free coefficients.

**Three smaller corrections.**
- "L >= 2N - o(N) for d >= log2 k + c" (ag-7 section 0, line 7) is true only if c grows. For fixed c the floor is
  N (1 + 2/(1 + 2^(2^-c))): 1.667 N at c = 0, 1.828 N at c = 1, 1.914 N at c = 2, 1.957 N at c = 3. ag-7 section 6
  states it correctly ("(2 - e) N for 2^d >= C(e) k").
- ag-0's "N^(1/6) outputs per helper at degree 3" is the cruder of ag-7's two forms; the finer form gives N^(1/8).
  Both are two-element statements. ag-0 proves (a) and (c) over the rationals, correctly, and nothing about cycles.
- ag-4's floor "T(N) >= (3/2) N for the transform" is below a two-line count [derived]: the output made first depends
  on all N inputs, which needs N - 1 gates of two operands; the other N - 1 outputs are N - 1 further gates.
  **2N - 2.** ag-7's lemma applied to inputs and outputs together also gives 2N - o(N), no more. ag-4's lemma
  (G >= N - n/2, needing only delta >= 5) is consistent with ag-7's and weaker wherever both apply
  (half rate: 3N/4 against N - o(N)).

## 4. Is it known?

- [read] Golovnev, Kulikov, Williams, "Circuit Depth Reductions", arXiv:1811.04828: for explicit matrices the strongest
  floor for linear circuits is 3n - o(n), Chashkin 1994 (Discrete Math. and Appl. 4(3), 229-257). He first shows 2n - o(n)
  for the log n x n check matrix of the Hamming code; for m outputs the recorded floor is 2n + m - o(n).
- [derived] Turning a circuit around (the transposition rule: gates change by outputs minus inputs) turns Chashkin's
  2n - o(n) into the trivial "each of n different outputs needs a gate". ag-7's lemma, turned around, would read:
  an R x N check matrix of a code of distance at least C log N costs at least 3N - 3R - eN (3N - 2R - eN when no
  column is a unit vector). For R = o(N) that is above
  the 2n + m - o(n) the survey records for few outputs. **I could not open Chashkin's paper. Either this is a small
  new statement or it is inside that paper; a specialist must look before anyone writes "new".** I found the
  statement nowhere in three searches.
- [read, second hand: S. Jukna's comment page to his book] Chashkin also proved an UPPER bound: there are m x n
  matrices with any k columns independent, m = O(k ln n), for every k up to n / log n, computed by O(n) gates.
  Turned around: **there are tall matrices with no relation shorter than k and linear cost.** So the hypothesis
  "long shortest relation" can never yield a floor above linear, whatever the argument. This answers ag-7's "better
  question" for the class: c is bounded for some matrices with long relations; a proof that c(d) grows for M(d, k)
  would have to use more than delta.
- [recalled] Codes of constant rate and linear distance with encoders of linear size exist (Gelfand, Dobrushin,
  Pinsker 1973; Spielman 1996). Same message.

What known theory predicts for "linear or not": nothing either way. Floors of this family stop at a constant times N
(3n has stood since 1994), and they are compatible with linear size.

## 5. Does it scale

[ran + derived] One size further (2^256 points) the table repeats itself: the floor depends only on c = d - log2 k,

    L(d, k) >= N (1 + 2 / (1 + 2^(k / 2^d))) - R - O(1)        [two-element field],

observed 1.6415, 1.6727, 1.6695, 1.6681, 1.6673 at c = 0 for k = 16 to 256 (limit 5/3), and 1.8396, 1.8339, 1.8311,
1.8297 at c = 1 (limit 1.8284). It is a constant between 1 and 2 times N. **Ceiling of the method: 2N - R**, reached
when the graph is a forest; no refinement of the graph condition can pass it. At full rank there is no relation and
the lemma is empty.

## 6. In the user's terms

- Circuit size for n points: **none.** It is a floor, and for the transform the floor is the trivial 2n - 2.
- Saving exponent: **none.**
- What it does: it closes "N + o(N) gates at every degree" above degree log2 k (two-element field) or log2 k + 3
  (rationals, my constant, unreviewed). That is a statement about a constant, which is outside the bar.
- For the wall list of ah-cross: RELATION-LENGTH should carry its field. Over the rationals its true form is "no small
  piece with two cycles", and by Chashkin's upper bound the wall can never be more than a constant.

## 7. What I did not do

- I did not open Chashkin 1994 or Alon-Hoory-Linial 2002; both are cited from memory or second hand.
- The rational constant of section 3 is twenty minutes old and read by nobody.
- I did not re-run ag-7's two checks, and did not test the lemma on any circuit over the rationals beyond the triangle.
- I did not look at ag-7 section 5 (the second step, "3N - 2 rank - P"); it is outside this object.

## Files

`waves/wave-10/ai-1/`: `delta.py`, `delta.out`; `anycircuit.py`,
`anycircuit.out`; `moore_exact.py`, `moore_exact.out`, `moore_256.out`; `rational.py`, `rational.out`.

## Sources

- Golovnev, Kulikov, Williams, Circuit Depth Reductions: https://arxiv.org/pdf/1811.04828 (read 11 October 2026)
- S. Jukna, comments to "Boolean Function Complexity", comment 9: https://web.vu.lt/mif/s.jukna/boolean/comment9.html (read 11 October 2026, through a summarising reader)
