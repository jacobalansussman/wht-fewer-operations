# ac-1: skeptic's report on ab-6's leak lemma

11 October 2026, 06:21 to about 06:35 EDT, one agent, 30-minute box (about half of it used). Private research: nothing published, no git, no Lean.

**Verdict: the lemma holds. I checked its proof line by line, found a second, elementary proof at K = 4, built a 7-call
program of my own and replayed it exactly, and pushed the numbers two sizes further (K = 32, 64). I did not find it in the
literature. It is a closed door, not an open one: in the user's terms it gives a saving of exactly 0 in the exponent.**

Marks: [ran] = exact run of mine tonight (whole numbers and fractions, `ac-1/check.py`, `ac-1/orb6.py`); [derived] = by hand
tonight; [read] = in a file or page I opened tonight; [guess].
Counts: CALLS to a box, with the glue free (no gates counted). Gate counts (G) and (O) are not used anywhere in this report,
and no statement here is a gate count.

## 1. The claim, stated exactly

Words. K = 2^k addresses. An *address map* g is an invertible k x k bit matrix; it permutes the addresses and P_g is the
K x K permutation matrix that does it. The *box* is P_g for an unknown g. A *call program* with r calls is a fixed list of
matrices L, M, P, Q (the *glue*, free, chosen once and for all, not allowed to depend on g): call j gets the input
w_j = L_j x + sum over i < j of M_ji c_i and returns c_j = P_g w_j; the output is Q x + sum of P_j c_j. It is *right* when the
output is P_g X P_g^T for every K x K table X (written as the vector x of its K^2 entries) and every one of the address maps.
r(K) is the least number of calls of a right program. The textbook program has 2K calls (K on the columns, K on the rows).

Under the address maps a K-vector is 2 numbers that never move (the entry at address 0 and the sum of the others) plus one
piece V of dimension d = K - 2 that cannot be split further. The table is then 5 numbers that never move, c copies of V,
and a remainder, Rest, that contains neither a fixed number nor a copy of V.

**Claim (ab-6, section 1).** r(K) >= c + ceil((Rest + d ceil(Rest/d)) / d). With c = 5, Rest = 1 at K = 4 this is 7, and
x-3 has a right program with 7 calls, so r(4) = 7 and 6 calls are impossible. With c = 6 and Rest = d(d - 2) - 1 for
K >= 8 it is 2K - 2.

Two remarks on the statement [derived].
- The formula is simply **c + 2 ceil(Rest/d)**: the inner ceiling is a whole number, so it comes out of the outer one.
- For K >= 8 the claim is a LOWER bound only. 2K - 2 <= r(K) <= 2K, and nobody has a program below 2K there. ab-6's table
  says "best program known: about 2K - 2 (x-3, rough)"; that is a rough count in x-3, not a program. ab-6's own section 7
  says so; its line 1 and the brief's wording ("needs at least") are right.

## 2. The proof, checked step by step [derived]

**The reduction to V is right.** A call returns the two fixed numbers of its input unchanged. Those two numbers are
themselves glue applied to x and to earlier outputs, so by induction on the calls anything that reads them can read x and
the V-parts of earlier calls instead. So a program is, without loss, d_j = rho(g)(A_j x + sum over i < j of m_ji d_i) with
d_j in V, output Q x + sum of P_j d_j, where rho(g) is how g acts on V. (I looked for a leak here: the fixed part of a
call's input may depend on g through earlier calls. It may; it is still glue applied to earlier V-parts.)

**Step 1 (the output map has full rank on the numbers that depend on g): right.** The vectors (target for g) minus (target
for the identity) span everything except the 5 fixed numbers, because a vector orthogonal to all of them is fixed by every
map. [ran, K = 4: the rank is 11.]

**Step 2 (the projection): right.** For a datum t in Rest, each output number of the target is, as a function of g, a
combination of entries of the matrices by which g acts on Rest. Entries of the matrices of two different unsplittable
pieces are orthogonal as functions on the group (Schur's orthogonality relations, a textbook theorem; it needs that V does
not occur in Rest, which is how Rest is defined, and it holds over the real numbers because V stays unsplittable over the
complex numbers, [ran] <chi, chi> = 1). The projection "keep the part of a function of g that is made of entries of
rho(g)" is linear and acts on each coordinate separately, so it commutes with the fixed matrix P. It sends the right-hand
side to 0 and the constant term Q t to 0. So P kills the rho-part of the calls' outputs for every t in Rest and every g.
[ran, K = 4, on my own 7-call program: that rho-part spans 3 dimensions and the output map sends all of it to 0, exactly.]

**Step 3 (independence by leading call): right.** For t that no earlier call has taken in directly, the earlier calls
return 0, and call j returns rho(g) A_j t exactly, which is its own rho-part. As g and t vary these span all of V in the
coordinates of call j (V cannot be split), with zeros in all earlier calls. Vectors that lead at different calls are
independent by the usual staircase argument: in a vanishing combination look at the earliest leading call; only its own
vectors are non-zero there. What the later calls contain does not matter. So the killed space has dimension at least
d times (the number of calls at which the set of not-yet-entered data shrinks).

**Steps 4 and 5: right.** A datum of Rest that enters no call gives an output that does not depend on g, while its target
does (Rest has no fixed number). One call takes in at most d new dimensions. So at least ceil(Rest/d) calls lead, and
r d - (c d + Rest) >= d ceil(Rest/d).

**A second proof at K = 4 that does not use step 2** [derived, ingredients ran]. With r calls there are 2r call outputs
and 11 output numbers that depend on g [ran], so the output map kills exactly 2r - 11 dimensions. The one datum t of Rest
is multiplied by the sign of the permutation, which is +1 on the identity and on the two 3-cycles c and c^2. So the calls'
outputs for t at c and at c^2, minus those at the identity, are both killed. In the first call that takes t in, these two
differences are (rho(c) - 1) a and (rho(c^2) - 1) a with a not zero, and their determinant is
3 a1^2 + 3 a1 a2 + 3 a2^2 [ran], which is never zero. So at least 2 dimensions are killed: 2r >= 13, r >= 7. This is ab-6's
"triangle"; it stands on its own.

## 3. My own computations [ran, exact]

`ac-1/check.py`, `ac-1/check.out`, `ac-1/orb6.out`. Nothing of ab-6's or x-3's code was reused; the multiplicities are
computed by a different method (counting orbits, no sum over the group) and cross-checked by the sum over the group.

| K | V unsplittable | copies of V in V x V | c | Rest | ab-6's formula | c + 2 ceil(Rest/d) | textbook 2K | x-3's bound 1.5 K |
|---|---|---|---|---|---|---|---|---|
| 4 | yes | 1 | 5 | 1 | 7 | 7 | 8 | 6 |
| 8 | yes | 2 | 6 | 23 | 14 | 14 | 16 | 12 |
| 16 | yes | 2 | 6 | 167 | 30 | 30 | 32 | 24 |
| 32 | yes | 2 | 6 | 839 | 62 | 62 | 64 | 48 |
| 64 | yes | 2 | 6 | 3719 | 126 | 126 | 128 | 96 |

K = 4, 8, 16 agree with ab-6's `leakbound.out`. K = 32 and 64 are new.

At K = 4, in the full model (4-vectors, 16-entry tables, the six permutation boxes; no reduction used):
- **A 7-call program of my own, right on all 6 maps and all 16 unit tables (96 cases, which is all cases because the
  program is linear), in fractions.** Five calls whose inputs are maps that commute with the family (found by averaging a
  random whole-number matrix over the six maps), and a nested pair for the sign: I fixed two vectors and solved 6 linear
  equations exactly for the glue between the two calls. So r(4) <= 7 independently of x-3's `perm7.py`.
- Controls: the same program without its 7th call has no output glue; 12 programs "five one-call pieces plus ONE more call
  with random whole-number glue" have no output glue either. These controls only show the solver can say no. The proof of
  "6 is impossible" is section 2, not a search.

The float search in ab-6 (`sixcall.py`: 6 starts at 6 calls, no hit) is no evidence either way: its companion at 7 calls
(`linux/r7.out`) is empty, so the search never showed it can find the program that exists. ab-6 says the same ("weak and
not needed"). An exact search over all 6-call programs is not feasible (hundreds of unknowns, polynomial equations) and,
with two proofs, not needed.

## 4. Scaling: the growth law

[derived, and ran up to K = 64] The number of copies of V in V x V is (orbits on triples of addresses) - 6 (orbits on
pairs) + 12 (orbits on single addresses) - 8. An orbit of a triple is fixed by which sums of its members are zero, that
is by a subspace of the 3-bit space, and all 16 subspaces occur as soon as k >= 3 (at k = 2 only 15). So the count is
16 - 30 + 24 - 8 = **2 for every K >= 8**, c = 6, Rest = d(d - 2) - 1, and

**r(K) >= 2K - 2 for every K >= 8; r(4) = 7; r(K) <= 2K always. So a = r/K lies between 2 - 2/K and 2 and tends to 2.**

How tight is 2K - 2 for K >= 8 [derived]: with 2K - 2 calls the output map may kill (d - 1)^2 dimensions and the lemma
forces it to kill d(d - 2): one dimension to spare at every size (25 against 24 at K = 8). With 2K - 3 calls it would have
to kill more than it can. So a program at 2K - 2 would have to be a perfect chain; I tried the obvious shortening of the
textbook program by hand (five minutes, one construction) and it loses information (it projects before the box acts). [guess] the truth at K = 8 is 15 or
16. This is a question about a constant and I did not pursue it.

## 5. Known or not

Not found. I searched for the model (a linear program with calls to an unknown matrix, the target A X A^T, a lower bound
on the number of calls) and found nothing that states it. The nearest literature goes the other way: learning properties
of an unknown matrix from adaptive matrix-vector products (Sun, Woodruff, Yang, Zhang, "Querying a matrix through
matrix-vector products", 2019, arXiv:1906.05736 [read: abstract]) and the Kronecker variant (Meyer, Swartworth, Woodruff,
"Understanding the Kronecker matrix-vector complexity of linear algebra", 2025, arXiv:2502.08029 [read: abstract]).
Neither counts calls for computing (A x A) x. The tools of the proof are textbook (Schur's orthogonality relations, a
dimension count). Four searches in a 30-minute box is not a literature review; "new" here means "a small lemma in a model
of our own making that I could not find".

What the known theory says about "linear or not": nothing through this lemma. Those papers allow the next query to depend
on earlier answers, and in that setting **this family costs ONE call** [derived]: feed the box the vector whose entry at
address x is the number x; the answer shows where every address went, so g is known, and the rest is free glue. The
lemma's 2K - 2 is therefore the price of a program that is linear and blind to g, not a price of information. And the
transform is one known box, where every bound of this family kind is empty (x-3's own caveat, which stands).

## 6. In the user's terms

- Circuit size for n points: **nothing**. The lemma counts calls with free glue for a family of boxes; it gives no circuit
  and no bound on gates for the transform.
- Saving exponent: **0**. In x-3's call recursion (cost per point c(K^2) = a c(K) + b, exponent log2 a) the lemma gives
  a >= 2 - 2/K, so along a tower K = 4, 16, 256, ... the calls are at least 2^j times (7/8)(15/16)(255/256)... = 0.817:
  a constant factor at best, and only if the bound were met at every level, which is known only at K = 4. The one small
  case with a < 1.866 (K = 4: a = 1.75) does not repeat at the next size (a >= 1.875 at K = 16).
- What it does: it closes the last room in x-3's wall S. x-3's telescoping bound left 1.5 K for the address-map family
  (0.415 in the exponent if it could be met); the leak lemma says the room is not there. The reason is short and worth
  keeping: the first box a datum passes sends on a plain once-moved copy of it, and killing that copy costs as many output
  numbers as a second call would have. A call cannot be "first box for the next datum" for free.
- What it does not touch: the engine. There the address maps are known and used on purpose; the lemma is about programs
  that do not know them. ab-6's mutation 3 (does the same count give a floor on totals per shear in the engine's game?) is
  untested and is the only forward lead in this object.

## 7. Does anything fail?

No failing case found. Corrections, all small:
1. The formula simplifies to c + 2 ceil(Rest/d).
2. "Best program known about 2K - 2" for K >= 8 should read "2K (textbook); 2K - 2 is the lower bound". r(K) for K >= 8
   is 2K - 2, 2K - 1 or 2K.
3. The bound belongs to linear programs with fixed glue. With glue that may look at a call's answer the family costs one
   call (section 5). That is the right model for a linear circuit, but the sentence "sharing is impossible in this model"
   should carry the words "linear" and "blind to g".
4. `sixcall.py` is not evidence (section 3).

Not checked: whether 2K - 2 is reached at K = 8; any version with calls to the inverse box as well (the same proof goes
through, because the entries of rho(g^-1) are entries of rho(g) transposed [derived, one line]); anything in Lean.

Files: `waves/wave-08/ac-1/check.py`, `check.out` (the table for K = 4 to 32, and
everything at K = 4), `orb6.py`, `orb6.out` (K = 64).

Sources: https://arxiv.org/abs/1906.05736 ; https://arxiv.org/abs/2502.08029 ; https://proceedings.mlr.press/v267/meyer25a.html
