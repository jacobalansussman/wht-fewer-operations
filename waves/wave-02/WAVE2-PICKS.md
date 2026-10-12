# wht39 / ideas / WAVE2-PICKS: seven more ideas to develop for an hour each

Curator: j-pick, 2026-10-10, 21:39 to 21:48 EDT. Private research; nothing here is reviewed and nothing is in Lean.

Source: `PICKS.md` (the eight already running, and its closing list of 48 undeveloped ideas and four unexplained
anomalies), the eight generator reports `i-*.md`, and a skim of the four developer reports that had landed when I
wrote this (`d-1.md` plane, `d-4.md` codes, `d-5.md` border, `d-7.md` spin). Idea numbers are those of `PICKS.md` (0 to 76).

How the seven were chosen: surprise; something actually seen behind the idea; a first experiment that fits an hour on
small exact cases; variety. Not by odds. Nothing was dropped for "must be known" or "must be impossible".
None repeats a first-wave pick. Tags [read] [ran] [derived] [guess] are the generators' own unless I write "mine".

Generators represented: wild, represent, fields, backwards, model, hatch, play (seven of eight; the free ideas of
cousins were all attached to first-wave picks already).
Picks most people would call silly or impossible: 4 (`cutoff`, a wrong answer on purpose) and 7 (`shifts`, which its own
author filed under "silly").
Picks built on an unexplained anomaly: 6 (`conserved`, the 64 that came back in every count), 1 (`ring`, the Hankel
matrix one short of full rank at k = 6 only), 3 (`density`, the four encoder sizes 30, 34, 39, 60).

## Notes for all seven developers

- Generation and play first, criticism last. A [guess] is welcome as long as it is marked.
- Instrument: `python3 -B (not in this repository) wht35/bin/light.py <label> <max seconds, at most 600> <command...>`.
  Exact rational or Gaussian-rational arithmetic, or modulo large primes with the reason why that suffices. A circuit found
  modulo a prime is a candidate until lifted and replayed exactly; "none found modulo p" is not "none exists" unless argued.
- Say which count you use every time you quote a number of gates:
  (G) a gate is any a*u + b*v, scalings free: 4 points cost 7, 16 points 56;
  (O) OpenAI's count, additions and scalar multiplications each charged: 4 points cost 8, 16 points 64.
- Words used below. N = 2^k points. H: the plain +-1 Walsh-Hadamard matrix. *Overlap* of two addresses: the number of bit
  positions where both have a 1. *Weight*: the number of 1 bits. *Monomial* map: relabel and scale, free in count G.
  *Eigenspace*: H/sqrt(N) is a reflection, so every vector splits into a part H multiplies by +sqrt(N) and a part it
  multiplies by -sqrt(N).
- A minimum-circuit searcher in C seems to exist already in `d-0-zeta/` (`mincirc.c`, `mincirc_all.c`) [read: file names
  only, mine]. Ask its report `d-0.md` before writing your own. `i-play/n4.py` is the exhaustive 4-point census in count G.
- Files under `waves/<label>/` and `<label>.md`. No git, no Lean, publish nothing.

---

## Pick 1. `ring`: the transform as multiplication by ONE number, and dense letters whose inverse is sparse

From: wild 72 (the resolvent of a relabelling), the anomaly "the Hankel matrix of one period of the maximal-length
sequence is one short of full rank at k = 6 only" [wild], and the lead that the plane developer ended on (`d-1.md` sections 1 to 3 and 8).

**The idea.** Read the N addresses as the field with N elements and take logarithms: the N - 1 non-zero addresses become
the cyclic group of order N - 1, and "multiply by the field's generator" is a relabelling that mixes every digit column.
In those coordinates the transform is one cyclic convolution: on the non-zero addresses H = (all ones) - 2 * (mask of the
elements of trace one). So the whole problem is: multiply by one fixed element M of the ring of polynomials in t modulo
t^(N-1) - 1. Cheap elements of that ring are of two kinds. Sparse ones: s terms cost (s - 1) gates per entry. And
INVERSES of sparse ones: solving y - c * (shifted y) = x costs about 4 operations per entry however dense the inverse is,
with entries c^(steps round the cycle). The second kind is a letter nobody has used: rows with unboundedly many terms at
bounded cost, and it moves every pair's diagonal. Target: M = (free scaling) x (a short product of sparse elements and
inverses of sparse elements). A bounded number of factors at every N is linear size. For k a power of two the group
splits as 3 x 5 x 17 x 257 x ... (the Fermat numbers) [derived, mine], a box with only log2 k sides, and the plane developer
derived that the transform is a product of log2 k masks, one per level of the tower of fields: N log log N if each level costs O(1).

**What was seen.**
- [ran, `d-1-plane/plane.py`, N = 4 to 256] The N - 1 lines that miss the origin are the cyclic shifts of one set D; at 16
  points D = {1, 2, 4, 8} modulo 15. Tower law: {trace to F_2 is 1} = {trace to F_q is 1} * {trace-one set of F_q} exactly, in the group ring.
- [ran, `d-1.md` section 3] At 16 points the 15 x 15 operator has five eigenvalues only: 4, -2, -1 and the pair (1 +- sqrt(-15))/2,
  the last on 8 dimensions. On every part that depends on the angle alone it is multiplication by -1.
- [derived, wild] On one bit (I - t * flip)^(-1) is the kernel [[1,t],[t,1]] up to a scalar: the family K_t is a product of k commuting resolvents.
- [ran, `i-wild/mseq.py`] One period of the sequence needs as many geometric sequences as it can (Hankel rank 8 of 8, 16 of 16,
  31 of 32, 64 of 64 at k = 4, 5, 6, 7): no single resolvent, and no short sum of them.
- [derived, mine] Of 15, 31, 63, 127 only 63 = 9 * 7 has a repeated prime factor. [guess, mine] The lost rank at k = 6 is that.
- [guess, plane developer] Two-term elements 1 +- t^a carry no factor of 2; three-term ones such as 1 + t + t^4 (the field's own
  defining polynomial) are the candidates for the primes above 2, whose exponents are binary digit sums (Stickelberger, recalled, unchecked).

**First experiment.** N = 16, exact, in the ring Q[t]/(t^15 - 1) split into its four pieces (the divisors 1, 3, 5, 15 of 15), with
Gaussian rationals allowed as coefficients. (a) List every element with 2 or 3 terms and small coefficients (include
coefficients that are not units, such as 2 and 1 + i) and its value on each piece. (b) Search for M = D-mask (or the
transform's own element J - 2 * mask) as (scalar on each piece that a free map can supply) x product of at most four
such elements, each allowed in the numerator or in the denominator. Count gates in G and in O, with a denominator charged
as one forward and one backward pass round the cycle. Beat 56 (G). (c) The same at N = 64 with the mask of 8 terms.
(d) Twenty minutes: the Hankel rank at k = 8, 9, 10 (255, 511, 1023 have no repeated prime factor) and k = 12 (4095 has one),
modulo two large primes, to settle the guess above.

**Question to keep asking.** Which sparse elements are "prime" for this ring, and how many does the transform's element need:
k of them (the textbook in disguise) or about log k (one per level of the tower)? What does a denominator buy that no
numerator can?

---

## Pick 2. `vcycle`: one half-size problem that is NOT a transform, between two dense-but-cheap frames

From: represent 13 (V-cycle through a Gram inverse), fields 56 (invariant planes span{x, Hx}), backwards 31 (cheap eigenbasis),
backwards 33 (fill "identity plus one projection" at 16 points), wild 66 (the eigenspace as a code), represent 12 and model 60
(the transform has the spectrum of matrix transposition; chain instead of lattice).

**The idea.** Every linear-time method in numerics and coding has the shape T(n) = T(n/2) + c*n: cheap, one half-size call,
cheap. For the transform the algebra allows it: H = sqrt(N) * I - 2 sqrt(N) * L * (R L)^(-1) * R for ANY L whose columns span
the -sqrt(N) eigenspace and ANY R that kills the other one. The middle is "apply the inverse of an (N/2) x (N/2) matrix",
which need not be a transform at all. The floor note set this aside because eigenvectors have at least sqrt(N) non-zeros,
"so L is not cheap". That step reads cheap as sparse. A pyramid of block sums is dense and costs under N additions in
total. And cheap eigenvectors exist at every scale: (a function constant on the cosets of a subgroup D) minus (its
transform, a function constant on the cosets of the dual subgroup). So choose L and R from such differences taken ACROSS
scales, as a wavelet basis takes one layer per scale, and look at what R L becomes. The freedom is enormous (any basis
of an N/2-dimensional space; N^2/2 numbers) and every choice anyone has tried was a tensor power.

**What was seen.**
- [derived, represent] With L = (H - sqrt N) on a half-cube the child is exactly ONE half-size transform, but L and R each need a call: 3 calls.
- [derived, fields] For any x, span{x, Hx} is invariant, so H = V * (swap) * V^(-1) with V = [X | HX] for any N x N/2 matrix X; every X tried needs the half transform twice.
- [ran, `i-wild/enc16.py`] At 16 points 7,280 of 12,870 coordinate sets determine the eigenspace part; the "encoder" has 37 to 64 non-zeros;
  the sparse ones belong to sets that span the whole cube, the dense ones (64) to the textbook's choice.
- [ran, represent, model] After a free relabelling the -sqrt(N) space shrinks to (N - sqrt N)/2 = 6 at 16 points: then only 6 numbers pass through the middle.
- [ran, `d-4.md` item 5, tonight] With S the transform written with an all-plus diagonal and T a free sign diagonal, (T S)^3 = 1,
  and on a subspace of dimension (N + 2)/3 the transform EQUALS a free sign change. One third of the space costs nothing.
- [derived, model] A chain of nested averages costs O(N); the Boolean lattice of averages costs N log N. Same reflections otherwise.

**First experiment.** 16 points, exact rationals. Take the relabelled form with the 6-dimensional -4 space. Generate the
cheap eigenvectors: for every subgroup D of sizes 2, 4, 8 and every sign pattern, (coset function on D) - (its image).
(a) What do they span, and how few cover the 6 dimensions (and the 8 of the plain form)? (b) For each spanning choice
of L, and R from the same family on the other side, compute R L exactly; record its number of non-zeros, whether it is
triangular after reordering, and the non-zeros of its inverse. Target from represent: an inverse with fewer than 16
non-zeros. (c) For the best choice count the whole program, frames plus middle, in count G against 56. Then 64 points
(a 28-dimensional middle) with frames drawn from three scales.

**Question to keep asking.** Is there a frame for which the middle matrix R L is sparse or triangular, so that the child is
a solve and not a transform? Which third of the space does d-4's identity hand over for free, and can the frame be
built around it?

---

## Pick 3. `density`: the exponent is a density of outputs: find an output set that is not a subspace

From: wild 68 (the exponent is a density), wild 67 (bent relabelling), with the anomalies "the encoder sizes over all 4,048
information sets take only four values, 30, 34, 39, 60" [wild] and "(N - sqrt N)/2 = 1, 6, 28, 120, 496 is three things at once" [play].

**The idea.** All translates of a set of outputs cost the same (multiply the input by a sign pattern first). So the
transform costs N (log N)^z as soon as SOME set of about N / (log N)^z outputs can be computed in O(N), and linear size
means a set of constant density at linear cost. The textbook's sets are subspaces: N / log N outputs for about 2N, and
that is z = 1. Nobody has asked what the best set of m outputs is when it is not required to be a subspace: a union of
subspaces that share their folds, a ball, the zero set of a quadratic form, an information set of the eigenspace code.
This turns the order question into a table that can be computed at 16 and 32 points: f(m) = the least cost of any m outputs.

**What was seen.**
- [derived, wild; greedy program reproduces it] Outputs in a subspace of dimension d cost N + (d - 1) 2^d additions: 15, 16, 20, 32 at 1, 2, 4, 8 outputs of 16.
  The first output costs 15, the second 1 more.
- [derived, wild] All outputs of weight at most w cost at most (2w + 1) N: the cost grows with the RADIUS of the set, not with its size.
- [ran, `i-play/n4.py`] At 4 points: 3, 4, 6, 7 gates (count G) for 1, 2, 3, 4 outputs: the third output costs 2, the fourth costs 1.
- [ran, `i-wild/enc16.py`] In the bent form only 6 outputs of 16 need a transform; the other 10 follow by a 10 x 6 encoder whose
  sparsest form has 30 entries, all +-1, for 192 sets; the histogram of sizes has only four values. Nobody has said which sets these are.
- [ran, wild] The trade seen so far: structured set, dense encoder; or sparse encoder, scattered set. Total 28 + 20 + 16 = 64 again.

**First experiment.** 16 points, exact. (a) Compute f(m) for m = 1 to 8 in count G and in count O: enumerate m-subsets of
outputs up to the affine symmetries of the cube (few orbits for small m), and for each orbit find the cheapest pruned
circuit (exhaustive where the searcher reaches, otherwise best found and say so). Print f(m) beside the subspace values.
Any m with f(m) below the subspace law is the first sign. (b) Identify the 192 sets with the 30-entry encoder and the
sets behind 34, 39, 60 geometrically (zero sets of quadratic forms? unions of planes?) and say why there are four values.
(c) For the best non-subspace set found, count its translates needed to cover all 16 outputs and the work they share.

**Question to keep asking.** What shape of set gets its (m+1)-th output for less than a subspace does? Is there a set whose
cost depends on something smaller than its radius? And what is the encoder of a set that is cheap: can "cheap set" and
"sparse encoder" ever be had together?

---

## Pick 4. `cutoff`: a cheap wrong answer that is exactly right on almost every entry, then pay only for the tails  (silly: wrong on purpose)

From: wild 70 and backwards 39 (one thought found twice). Attached: hatch 9 (two factors each almost of rank one), fields 53 (fast
multipole: push the kernel into the short-range regime).

**The idea.** The entry of H at (x, y) is (-1)^overlap. Summing the data over all addresses that contain a small set S, for
every S of at most d elements, then scaling, then spreading back, produces every matrix whose entry is a polynomial of
degree d in the overlap. A polynomial of degree d can equal (-1)^t on any d + 1 consecutive values of t. Overlaps of two
random addresses sit at k/4 give or take 0.43 sqrt(k). So with d about 2.25 sqrt(k) the cheap matrix equals the transform
on 99 % of all entries, and the generator's count for it is (d + 1) N operations: N sqrt(log N), a saving of 5e-1, for
an answer that is wrong only on pairs with unusually small or large overlap. The error is again a function of the
overlap alone, and it lives on a thin set of pairs. The idea is to stop there on purpose, look hard at what is left, and
ask whether the leftover is a smaller copy of the same problem (overlaps confined to a narrower window once addresses
are split into weight classes, or into codes with few distinct overlaps, which is where the E8 family lives).
[recalled, mine, unchecked] This polynomial-in-the-overlap matrix is how the Walsh-Hadamard matrix was shown not to be
rigid; that work stops at "low rank plus sparse". Nobody in these notes has used the form as the first step of an exact
program in a model where huge coefficients are free. That is not a reason to stop: read `readers/lit-lower-bounds.md`
for the dates and then go on.

**What was seen.**
- [ran, `i-wild/zeta16.py`] The form cut off at |S| <= d equals the transform on every pair with overlap <= d: all pairs at N = 16 and 64, every d.
  At N = 64, d = 2: 83 % of entries exact; d = 3: 96 %; d = 4: 99.5 %.
- [ran, count only] The window that holds 99 % of pairs is 9, 18, 36, 72, 143 wide at k = 16, 64, 256, 1024, 4096: 2.25 sqrt(k).
- [ran, `i-backwards/play2.py`, k = 4] Keeping sets up to size 0, 1, 2, 3 gives rank 1, 5, 11, 15 and leaves 120, 67, 13, 1 wrong entries of 256.
- [derived, not run] The cost law (d + 1) N for the cut-off sums is a counted recursion; nobody has built it. Nobody has built the tail correction.
- [derived, mine] The cut-off form passes through only C(k, <= d) numbers, far fewer than N. So it is also a narrow waist: a place where the data provably narrows.

**First experiment.** Work first with polynomials in the overlap t, which needs no matrices: for k = 16, 64, 256 and the
window centred at k/4, compute exactly the degree-d polynomial p equal to (-1)^t on the window, its coefficients in the
basis C(t, j) (they will be huge: record their size), and the leftover r(t) = (-1)^t - p(t) outside the window. Then at
k = 8 and 10 with real matrices: (a) implement the cut-off sums and count operations against the (d + 1) N law;
(b) build the leftover matrix r(overlap), restricted to pairs of weight classes (|x|, |y|), and for each pair of classes
record the range of overlaps that occurs, the rank, and whether a second cut-off form with its own window is exact there;
(c) add up: how many (class pair, window) pieces cover everything, and what do they cost together against k N.

**Question to keep asking.** Is the leftover the same problem on fewer addresses, and if so what is the recursion and its
solution? Which splitting of the addresses makes every overlap window narrow at once? What do the huge coefficients do
here that bounded ones could not?

---

## Pick 5. `passes`: pay in running sums, not butterflies

From: fields 50 (summed-area tables, wavelet lifting), backwards 38 (differences and prefix sums as free changes of basis),
represent 16 (change the metric: exponential kernels with a sparse inverse).

**The idea.** A running sum along a chain of d entries, y_i = x_i + c_i * y_(i-1), costs d - 1 gates whatever d is, and its
matrix is dense (a full triangle). A transform kernel on d points costs d log d. Image processing and wavelets removed
their logs exactly this way. So make the pass the paid letter: write the kernel on a digit of d = 2^m values as
H_d = M_0 * P_1 * M_1 * ... * P_h * M_h, with M_j free monomial maps and P_j passes, each with its own d - 1 coefficients, in
either direction, and (the wrap-around variant) round a cycle. The transform then costs h * N per digit against m * N.
A win is h(d) < log2 d for a single d; h bounded as d grows is linear size. The same thought from the other end: on a
path, a cycle or a tree the kernel t^distance costs O(N) because its inverse is tridiagonal; the cube is the expensive
end of a family whose other end is linear, and the Gray map (which turns two bits with Hamming distance into the cycle
of length 4 with its own distance) is a bridge between them.

**What was seen.**
- [ran, `i-fields/play.py`] In the floor note's own count ONE pass on a digit moves the diagonal of two digit columns by d - 1 dimensions,
  the same as the full kernel, for d = 2 to 8, at cost N and not N * m. The floor does not price passes.
- [ran] d = 2: H_2 = T * diag(1, -2) * T-transpose: two passes; one pass leaves a zero.
- [ran, weak] d = 4, two passes of the fixed all-ones running sum, all 24 relabellings, scalings on a grid of 18 values: no Hadamard matrix,
  at best 2 of 6 row pairs orthogonal. Passes with their own coefficients were not tried; three passes were barely sampled.
- [derived, backwards] H times the difference operator in address order has half its entries zero in every column.
- [derived by hand, represent] On the cycle of length 4 the kernel (1, t, t^2, t) has a tridiagonal-circulant inverse only at t = 0: the wrap-around breaks it.

**First experiment.** Solve, do not sample. d = 4: for each choice of directions and relabellings, treat the coefficients of
two general passes and the three diagonals as unknowns and solve the polynomial system "product = monomial x H_4"
exactly (Groebner basis or elimination by hand; over the Gaussian rationals; a search modulo a prime first is fine if
lifted). If two passes are impossible, say what forces it. Then d = 8 with three general passes and with two (the win).
Then allow one wrap-around pass (the inverse of I - c * cyclic shift). Side experiment, ten minutes: at 16 points apply
differences on both sides of H in plain order, Gray-code order and field-logarithm order, and count the non-zeros left.

**Question to keep asking.** What is h(d) for d = 4, 8, 16: does it grow like log d, or stop? What does a pass with free
coefficients reach that a pass of plain sums cannot, and is it the large coefficients?

---

## Pick 6. `conserved`: 64 came back in every count. What is conserved, and where does it first break?

From: the anomaly carried by no first-wave pick [model anomaly 8, wild]: at 16 points 64 additions came back from the
textbook, the eigenspace encoder and the bent encoder (28 + 20 + 16), and every reorganisation the model generator priced
in OpenAI's count (Grover form, Bell basis, Zak recursion, fold-then-transform) landed exactly on the textbook, never
below. Attached: represent 11 (scaling debt).

**The idea.** A number that comes back from several unrelated constructions is a conservation law that nobody has written
down. Either it is a theorem about count O at small sizes, and then its hypotheses are the to-do list for breaking it;
or it is false, and the first program with 63 shows how. And there is a fixed point to steer by: the published program
and OpenAI's own DO go below N log2 N in count O, at their unit's size. So the law, whatever it is, holds at 16 points and
fails somewhere between 16 points and the unit. Finding the smallest size where count O first dips, and the single step
that does it, would say what the saving is made of, in a form small enough to exaggerate. In count G the same matrix
costs 56: the whole gap between the two counts at 16 points is 8 scalings, one per 4-point block. Represent's remark:
an uneven output scale is a debt that commutes with later passes on other digits, so it might be carried and paid once.

**What was seen.**
- [ran + derived, wild] 28 + 20 + 16 = 64 for the bent encoder, though the pieces have nothing to do with butterflies.
- [derived, model] Every reorganisation tried tonight lands on exactly the textbook count in OpenAI's count, not below.
- [ran, represent, play] The 4-point block is 7 additions + 1 multiplication = 8 in count O, a tie; 56 additions + 8 multiplications = 64 at 16 points [derived, mine].
- [ran, `i-play/clebsch.py`] The same 16-point matrix read as "4x - 2(row sum) - 2(column sum) + total" costs 63 naively and 56 ordered as two passes (count G): the order of combining is worth 7.
- [read, model] OpenAI's tensor step uses only the coefficients (1 +- i)/2, +-1/2, +-1.
- [derived, mine] Morgenstern's determinant count gives only 32 at 16 points for coefficients of size at most 1, so it is not the law.

**First experiment.** (a) 4 points, exhaustive, count O, three conventions: outputs exact; outputs allowed any fixed
scaling (debt); inputs and outputs both. Is the minimum 8 in all three, or 7 in one? `i-play/n4.py` is the starting
code. (b) Collect every 64-count program at 16 points named above and tabulate, gate by gate, candidate conserved
quantities: additions and scalings separately; the excess of first-wave pick 7; the floor note's pair-diagonal potential;
the sum over wires of log2(support x co-support) from i-backwards item 2. Which one totals the same for all of them?
(c) Read the smallest unit in `R/OAI/` and in the engine that beats the textbook in count O; state its size and its
count against N log2 N, and find the first step in it for which the quantity from (b) is not conserved.

**Question to keep asking.** What exactly do the programs that cost 64 have in common that the published unit lacks? Is the law about
count O, or about 16 points being too small, and what is the smallest size at which it fails?

---

## Pick 7. `shifts`: transform N shifted copies at once and read the diagonal  (silly)

From: wild 75 (filed by its author under "silly"), fields 54 (the transform is "conjugate a matrix by H"; Strassen tuned to a
known factor), wild's "batches are not additive".

**The idea.** Put the N copies of the data shifted by every address (XOR shifts) into an N x N array X. It costs nothing:
fan-out is free. Then H * X * H = N * diag(Hx): the answer is the diagonal of a two-sided transform of X, which is the
N^2-point transform applied to very special data, with only N of its N^2 outputs wanted. So the N-point transform is
a pruned N^2-point transform: inputs confined to an N-dimensional subspace, N outputs read. That sounds like going
backwards. But it is a machine for making N-point programs out of N^2-point identities, and the interesting N^2-point
identities are the ones that are NOT a tensor product of two N-point programs: the 27 two-flag identities that hold
only modulo 4, the line sums of the plane, "4x - 2 rows - 2 columns + total", the symplectic form of d-4. Each of them,
fed the array X and collapsed (equal wires merged, dead gates dropped), becomes an N-point program that nobody designed.
Second half: for an N = q^2 array M the transform is q * (2 * pinch(M) - M), where pinch keeps the part of M that commutes
with the small reflection. That is a conditional expectation, the kind of map that averaging over a group computes, and
a fixed matrix times a generic one is where direct sums are known to fail (N copies of a generic matrix cost less than N times one).

**What was seen.**
- [derived, wild] H * X * H = N * diag(Hx). Nothing was run.
- [derived, wild] H's XOR-diagonals are its own rows times the parity sign: H(v + a, v) = (-1)^|v| * H(a, v).
- [derived, fields] By hand, Strassen's seven products with left factor [[h, h], [h, -h]]: three left factors vanish and the four left are the textbook.
- [derived, mine] Row w of H * X is the single number (Hx)_w times a sign pattern, so the plain two-sided route gains nothing; only identities that are not "left then right" can.
- [ran, hatch, play] Non-product identities at 16 points exist: 27 two-flag identities valid only modulo 4; the 56-gate and the Clebsch forms.

**First experiment.** N = 4, so X is 4 x 4 and the big transform has 16 points. Write a collapser: take a 16-point program
as a list of gates, substitute the 4 unknowns of X for its 16 inputs, merge wires that are the same linear form up to
scaling, drop gates no wanted output depends on, and count what survives (count G and count O). Run it on every
16-point program in the folder: textbook, the 56-gate two-pass, each of the 54 two-flag identities of `i-hatch/flags.py`,
the row-and-column form and the Clebsch form of `i-play/clebsch.py`. A collapse to 7 that is not one of the 228 known
optimal sets, or any collapse whose shape is new, is the sign of life; 6 would contradict the census and so is a check.
Then N = 16 from 256-point programs (two levels of the 56-gate program, and the Hamming-code atoms of `d-4`), target under 56.
Also try other free embeddings in place of XOR shifts: field-multiplication shifts, and the 4 x 4 array "x on the diagonal, zero elsewhere".

**Question to keep asking.** Which free embedding of N numbers into N^2 makes a big identity collapse the furthest? Is there
an N^2-point identity whose collapse is cheaper than any N-point program built directly: a saving that exists only
because one went up before coming down?

---

## Left for a third wave (nothing is thrown away)

Still undeveloped after both waves, by title and number: 6 monomial plus nested remainder; 8 the tiling theorem as a map;
11 rows near a common centre (only its "debt" half is in pick 6); 17 the chirp as a short product of coset indicators;
32 relabel first; 34 a half-dimensional space with sparse checks; 49 odd radix as a source of bricks; 61 a short sum of
cheap tensor products; 63 a linear exact transform for data in a fixed finite ring; 64 the outrageous program; 65 pointer trees.
Three I would open next, for the same reasons and not by odds: 49 with the fact that bits per gate peak at 6 points
(1.244) and that a rank-one-plus-diagonal flat matrix exists only at 2, 3, 4 points; 65 with 64, a second reading of
`RAM.lean` atom by atom for any step whose price does not grow with what it moves; and the new question the spin developer
ended on (`d-7.md` item 6): the Kronecker power of the 3-point kernel [[1,1,1],[2,0,-2],[1,-1,1]] on 9 numbers in fewer than 24 additions.

Ideas inside these seven: 72 (pick 1); 12, 13, 31, 33, 56, 60, 66 (pick 2); 67, 68 (pick 3); 39, 70, 53 and hatch 9 as material (pick 4);
16, 38, 50 (pick 5); the anomaly of 64 with 11 as material (pick 6); 54, 75 (pick 7).

What I did not do: I ran nothing. I read `PICKS.md` and the eight generator reports in full; of the developer reports I read only the summaries and closing sections of d-1, d-4, d-5, d-7 (d-0, d-2, d-3, d-6
had no report yet). Statements marked "mine" are unchecked.
