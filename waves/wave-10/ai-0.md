# ai-0, critic of ag-0's tower of lamps: the law holds and is now built and proved; two side claims are wrong; nothing for the transform

11 October 2026, about 09:28 to 10:05 EDT (30-minute box, overrun by a few minutes). Private. One agent; nothing in
Lean, nothing published.
Marks: [ran] = exact run of mine in this hour, whole numbers, my own code, files in `ai-0/`; [derived] = by hand in this
hour, checked by nobody else; [read] = from tonight's reports or from a web page; [guess].
Gate count everywhere: **(G)**, a gate is any a*u + b*v, scalings free. Every gate built here is u + v or u - v, so
the counts are the same in OpenAI's count (O).

## Verdict

**The main claim holds.** A polynomial of degree at most 3 in k bits can be evaluated at all N = 2^k cube points with
N (1 + 3/L + 2/2^s) + o(N) gates, by the tower with L colours and atoms of s bits. I replaced the authors' evidence
(a solve at three toy sizes) by a closed formula for both helpers, a seven-line proof for every L and s, and a circuit
built gate by gate and replayed on every input at 2,048, 8,192 and 32,768 points.

**Two things said around it are wrong, in opposite directions.**
- "It starts to beat 2N only for addresses of more than 2^2059 bits": no. By the authors' own count it beats 2N at
  **2,060 address bits** (three working colours out of four, atoms of 2 bits): 1.943 N against 2.008 N [ran, count
  only]. That is still 2^2060 points; nobody can build it.
- "The transform modulo 16 in 2N + o(N)": no. By that route it is **3N + o(N)**, the same slip of N that af-0 found
  in ae-cross.

**For the user's bar: nothing.** The object is a matrix with N rows and about k^3/6 columns. It was already of linear
size (3N by the textbook). The result moves its leading constant from 2 to 1 at sizes no machine holds. It says
nothing about the order of the transform, and ag-0 says so itself in its third line.

## 1. The claim, stated exactly

Words. An *address* is k bits; N = 2^k. The *degree-3 object* has one input per set S of at most 3 bits and one output
per address x: output(x) = the sum of the inputs at the sets S inside x. (It evaluates a polynomial of degree at most 3
in the bits at every cube point.) A *helper* is a wire that is not an output. *Two helpers per output* means every
output is one gate, helper + helper.

Split the address into (a, y): a = t *selector* bits, its value is the *colour*; y = the other m bits. The *tower*
with L colours and atoms of s bits arranges the bits of y in levels: level 0 is one group of s bits (an *atom*); level
j has one atom for every value of all the bits below it. So the levels start at bit 0, s, s + s 2^s, ... and four levels
with one-bit atoms need 1 + 2 + 8 + 2,048 = 2,059 bits. Colour c *forgets*, at the point (c, y), the level-c atom
whose index is the present value of all lower bits of y.

- (a) **Two helpers.** Every polynomial F of degree at most 3 is F(a, y) = A(y) + B_a(y with the forgotten atom
  erased). The number of helper values is N (1/L + 2^-s) when all 2^t colours work.
- (b) **The helpers are cheap.** A is itself a polynomial of degree at most 3 in y. B_c is of degree at most 2 on each
  *piece* (the points where the bits below level c have one fixed value).
- (c) **Count.** Gates <= N (1 + 3/L + 2/2^s) + o(N), and <= N (1 + 2/L + 1/2^s) + o(N) with ad-6's degree-2 circuit
  inside. Letting L and s grow: N + o(N). The o(N) falls like 1/log*(k) (log* = how many times one takes log2 before
  reaching 1).
- Side claims: (d) it beats the known 2N + o(N) only from 2^2059 address bits on; (e) through ae-cross's dictionary the
  transform modulo 16 costs 2N + o(N); (f) the tower is not good for degree 4.

## 2. What I checked, with my own code

**A closed formula for the helpers** [derived; then ran]. Write F(a, y) = c0(y) + Q_a(y): c0 = the monomials without
a selector bit (degree at most 3 in y); Q_a = the rest at selector value a (degree at most 2 in y, since each of those
monomials spends a degree on the selector). For a bit q of level l let iota(q) be the value of the lower bits at which
q's atom is the forgotten one. Define a quadratic A'(y):
- coefficient of y_p y_q = the coefficient of y_p y_q in Q_c, c the LOWER of the two levels;
- coefficient of y_q = (coefficient of y_q in Q_l) + the sum, over the lower bits p that are 1 in iota(q), of
  (coefficient of y_p y_q in Q_l) - (coefficient of y_p y_q in A').

Put **A = c0 + A'** and **B_c = Q_c - A'**. Then F = A + B_c trivially, A has degree at most 3, B_c is one quadratic in
y for the whole colour, and the only thing to prove is that B_c does not move when the forgotten atom moves.
Proof. Fix a piece and a bit p of the forgotten atom. A monomial y_p y_q of B_c with q NOT a lower bit has coefficient
(Q_c) - (A') = 0, because the lower of the two levels is c. A monomial y_p y_q with q a lower bit is, on this piece, a
constant times y_p; adding those to the coefficient of y_p gives exactly the expression that the second rule makes
zero. So no monomial containing p survives on the piece. Nothing used that L is small, that s is 1, or that Q_c came
from degree 3: any one quadratic per colour will do. **So (a) and (b) hold for every L and s.** This does not go
through the authors' rule D; I did not test rule D on designs other than the tower.

**The circuit, built from that formula and replayed** [ran, `check.py`, `run3.out`, `run4.out`]. Every wire carries its
exact linear form in the inputs and can only be made by my "add" (which counts a gate); the outputs are compared with
the wanted form for every input, so each line is a proof for all inputs at that size.

| tower | k | points | gates (G), built | per point | textbook (3 per point) | best known without the tower* |
|---|---|---|---|---|---|---|
| 2 colours, 1-bit atoms | 4 | 16 | 36 | 2.250 | 31 = 1.94 | |
| 2 colours, 2-bit atoms | 11 | 2,048 | 5,867 | 2.865 | 6,064 = 2.96 | 2.81 |
| 3 colours of 4, 1-bit atoms | 13 | 8,192 | 23,766 | 2.901 | 24,469 = 2.99 | 2.69 |
| the same + 2 free bits | 15 | 32,768 | 94,467 | 2.883 | 98,166 = 3.00 | |
| the same + 4 free bits | 17 | 131,072 | 377,109 (count only) | 2.877 | 393,043 = 3.00 | |

All outputs right on every unit input in the four built rows. *ad-6's degree-2 circuit plus one variable at a time,
by ad-6's count-only law [ran their `law.py` untouched; af-0 replayed that circuit up to k = 20].
The limit of the 3-colour rows is 2.875 = 1 + 3/4 (A) + 2/8 + 2/8 + 1/8 (the three colours; the top one is of degree
1 on each piece) + 2/4 (the fourth selector value, which forgets nothing). **At every size one can build, the tower
loses to what was already known this night.**

**The pair itself, by my own walk** [ran, `check.py good`, `run1-before-counter-fix.out`, `run2-first.out`]: good for
degree 2 and 3 and not for degree 4 at 16, 2,048 and 8,192 points, with 16, 1,536 and 7,168 classes; good for degree 3
at 32,768 points (28,672 classes). The authors' figures are confirmed, (f) included.

**One size further than the authors** [ran, `symbolic.py`, `sym.out`]. They ran neither four colours nor three colours
with atoms of more than one bit. With y of 2,058 bits (3 colours, 2-bit atoms) and of 2,059 bits (4 colours, 1-bit
atoms) I drew one random whole-number quadratic per colour, built A' by the formula and checked every coefficient
condition of the proof: 4,216,926 and 4,218,986 identities, all hold; and 60 random points per colour with the
forgotten atom redrawn give the same value of B_c. With A' = 0 the same test fails everywhere, as it must. (The
identities are linear in the random numbers, drawn below 2^20, so a false one survives with chance under 2^-19.)

## 3. The four attacks I was asked to make

1. **The helper claim (seen by the authors at three toy sizes).** True for all sizes, by the formula and proof above.
   It is no longer an observation.
2. **Does the count include forming the coefficients of each piece ("computing the atoms")?** In ag-0 it is one
   sentence ("a polynomial in m per piece, negligible"). In my built circuit it is counted: 377 of 23,766 gates at
   8,192 points (1.6 %), 490 of 94,467 at 32,768 (0.5 %), 607 of 377,109 at 131,072 (0.16 %). In general the top colour
   has 2^(bits below it) pieces and each needs at most (1 + m)(1 + o + o^2/2) gates for its coefficients, o = number of
   bits below; a piece has 2^(m - o - s) points and m - o is exponential in o. So this term is o(N) [derived]. At
   2,060 bits it is under 2 * 10^9 gates against N = 2^2060 [ran, `big.out`]. **The count stands.**
3. **"2^2059 bits".** Wrong, too pessimistic. ag-0 says the bound "drops below the known 2N only with L >= 4 and
   s >= 2". With the textbook inside, L = 4 and s = 2 give 1 + 3/4 + 2/4 = 2.25, which is not below 2. With ad-6's
   degree-2 circuit inside, **three working colours of four with 2-bit atoms** already give 31/16 = 1.9375 in the
   limit, and that tower needs 2 + 8 + 2,048 + 2 selector bits = 2,060 bits. Counted in whole numbers with ad-6's law
   inside: at most **1.942924 N at k = 2,060 against 2.007889 N** for the best route without the tower. Four colours
   with 1-bit atoms (k = 2,061) only tie: 2.0059 against 2.0079. The next step down (three colours, 3-bit atoms,
   1.84) needs 402,653,213 bits. [ran, `big.py`, `big.out`; count only, ad-6's law is not replayed at these sizes.]
4. **"The transform modulo 16 in 2N + o(N)".** Wrong by N. The dictionary is: transform = M D M^T modulo 16, M the
   degree-3 matrix (N rows, about k^3/6 columns), D a diagonal. The tower prices M at N + o(N). M^T is M's circuit
   turned round (every wire reversed, a fan-out becomes an addition), and turning round changes the gate count by
   exactly (outputs - inputs) of the original, here N - k^3/6. So M^T costs 2N + o(N) and the route costs
   **3N + o(N)**; and not less by this route, since M needs at least N - 1 gates (every output but one is a new
   linear form) [derived; same argument as af-0 section 6]. Also, "the transform modulo 16" is another matrix, of
   rank about k^3/6; it is not the transform.

## 4. Is it known?

I did not find it in print [three web searches, not a survey]. What I found or recall:
- Degree 1 is settled exactly: Zhengrui Li, Sian-Jheng Lin, Yunghsiang S. Han, "On the Exact Lower Bounds of Encoding
  Circuit Sizes of Hamming Codes and Hadamard Codes", 2018, arXiv:1804.09903 [read: abstract only].
- Degree d in d operations per point along a Gray code (an ordering of the cube points that changes one bit at a
  time): Bouillaguet and co-authors, CHES 2010 [recalled, not opened]. That is the textbook count used here.
- Nothing on N + o(N) for degree 2 or 3, and nothing on the size of encoders of Reed-Muller codes (the code whose
  words are these lists of values) of order 2 or more.

What the known theory predicts for "linear or not": nothing is at stake. The object is linear already; the only open
quantity was the constant, and N - 1 gates are needed, so 1 is the end of the road. The proved lower bounds for
explicit linear maps are a small constant times N [read: survey arXiv:1811.04828, search summary only], so no theory
forbids or promises anything for larger degree.

## 5. Does it scale? The growth law

Per point, the cost is a staircase: 1 + 2/L + 1/2^s (+ what the idle selector values cost), and a new step is reached
only when the next tower fits: k = 4, 13, 2,061 for 2, 3, 4 colours with 1-bit atoms; the fifth colour needs about
2^2059 bits. Between steps the cost per point is flat [ran: 2.90, 2.88, 2.88 at k = 13, 15, 17, limit 2.875].
So gates = N (1 + an excess of the order of 1/log*(k)): N + o(N) with about the slowest o one ever meets. The
authors' law is confirmed. I measured the staircase only on its second and third steps; the fourth is a count.
For degree 4 the tower fails at every size tried (theirs and mine); I did not attack their sketch that no finite
design of this kind exists.

## 6. In the user's terms

- **For the transform on n points: no circuit size, no saving exponent.** The transform needs every degree up to
  log2 n, and most of its weight sits at degrees near (log2 n)/2 [read, ae-cross]. One cheap rung at degree 3 is a
  constant on a term that was already linear.
- For the degree-3 object on n points: n (1 + 2/L + 1/2^s) + o(n) gates with L about log*(log2 n); first below the
  known 2n at n = 2^2060.
- By-product that may be of use elsewhere: the helpers serve "one cubic in y plus ANY quadratic in y per colour",
  with an explicit formula. That is a much larger space than degree 3.

## 7. What fails, smallest case, nearest true statement

| claim in ag-0 | status | nearest true statement |
|---|---|---|
| tower good for degree 3, classes N (1/L + 2^-s) | holds [derived for all L, s; ran] | as stated |
| both helpers of low degree | holds [derived; ran] | A = c0 + A', B_c = Q_c - A', section 2 |
| gates <= N (1 + 3/L + 2/2^s) + o(N) | holds [built at 3 sizes] | as stated; the top colour costs 1 per helper, not 2 |
| beats 2N only beyond 2^2059 address bits | **fails** | beats 2N at k = 2,060: 1.943 N against 2.008 N [count only] |
| "below 2N only with L >= 4 and s >= 2" | **fails**; smallest case L = 4, s = 2 with textbook helpers: 2.25 | with ad-6 inside: 3 colours of 4, s = 2 |
| transform modulo 16 in 2N + o(N) | **fails**; smallest case of the slip: 1 number copied to N places costs 0 gates, N numbers summed cost N - 1 | 3N + o(N) by that route |
| not good for degree 4 | holds at 16, 2,048, 8,192 points [ran] | as stated |

## 8. Not checked

- Rule D as a general sufficient condition, and the nine non-tower designs of `designs.out`.
- ag-0 section 1 ("N + o(N) gates forces two helpers") and the lower bound "a third colour needs 2^(s 2^(s-2)) atoms".
- ag-0 section 5 (rule D4, "no finite design for degree 4") and the 4-bit example of `q4.out`.
- ad-6's law at k near 2,060 is its authors' count-only code; nobody has replayed a circuit beyond k = 20.
- Whether another design does degree 3 in N + o(N) at a size one can build. Girth alone allows it from 16,384 points
  on [read, ag-0 line 7]; nobody has a candidate.

## Files

`waves/wave-10/ai-0/`
- `check.py`: my tower, my walk ("good"), my builder with exact replay ("build") and its count-only twin ("count").
- `run3.out`, `run4.out`: the built circuits (16; 2,048; 8,192; 32,768 points) and the count at 131,072.
- `run1-before-counter-fix.out`, `run2-first.out`: the walks. Their gate lines are 8 to 13 gates too high (they counted
  the forming of coefficients that are the zero form); `run3.out` and `run4.out` are the corrected counts.
- `symbolic.py`, `sym.out`: the coefficient test at 2,058 and 2,059 bits, with its control.
- `big.py`, `big.out`: whole-number counts at k = 2,060 and 2,061. Its closed form is an upper bound (it charges the
  top colour 2 per helper; the built circuit needs 1), which is why it prints 24,377 for the main terms at k = 13
  where the built circuit has 23,389.
- The runs with numpy were made on the rented Linux machine under `(the Linux machine's working folder)/ai-0/` (this Mac's python has
  no numpy); outputs copied back; nothing of mine is left running there.

## Sources

- ag-0.md and `ag-0-ladderdegree3/` (designs.py, designs.out, check_helpers.out, W_L3_s1.out); ad-6.md and
  `ad-6-twohelpers/law.py`; af-0.md section 6; ae-cross.md hybrid 1.
- https://arxiv.org/abs/1804.09903 (abstract read 11 October 2026).
- https://arxiv.org/pdf/1811.04828 (seen through a search summary only).
