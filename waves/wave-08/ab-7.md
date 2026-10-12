# ab-7 the transform in a row: the row is the cube plus carries, and every carry costs; the Pascal cousin is dearer than subset sums at every size tried and its distance from them grows by a factor log N per binary digit; the transform itself IS a convolution for an addition with carries (power series modulo 2), 8 to 256 points, but its longest row has at most 2 log2 N points and the route through it costs more than the textbook

11 October 2026, about 04:45 to 05:30 EDT, 60-minute box. Private. One agent (label ab-7-transforminarow); nothing reviewed,
nothing in Lean, nothing published. Marks: [ran] = exact run of mine tonight, whole numbers or fractions (files in
`ab-7-transforminarow/`); [ran, exhaustive mod p] = `d-0-zeta/mincirc`, exhaustive over GF(p), so "none" means none modulo p
only; [derived] = by hand tonight, checked by nobody; [recalled] = from memory, no source opened; [read]; [guess].
Gate count everywhere: **(G)**, a gate is any a*u + b*v, scalings free. Count (O), OpenAI's, is not used.
Read: w-cross.md (sections 0 to 3 and 6), x-1.md in full, brief 8 of WAVE8-PICKS.md. Not read: the wave-7 skeptics (not landed),
the other wave-8 reports, k-cross beyond what w-cross quotes.

**No circuit below a known count, and no growth law below N log N. Nothing here changes the order.** What is new: the exact
distance between the row and the cube (a "carry" matrix, with its growth law); three cousins of subset sums with exact small
costs; the reason P D' P^T cannot be the transform, and what it is instead; a literal answer to "can the transform be put in
a row" (yes: it is a convolution for a second addition on the addresses, one with carries, with cycles of up to
2^ceil(log2(k+1)) points; run from 8 to 256 points); and three short lemmas that say why the row's cheap tricks stop at the
transform.

Words. N = 2^k points; an *address* is k bits, also read as a whole number 0 to N - 1. *The transform* H: entry (s, u) is
(-1)^(number of common ones). *Subset sums* Z: entry (s, t) is 1 when every one of t is a one of s. *Pascal* P: entry C(s, t),
the binomial number. *Prefix sums* T: entry 1 when t <= s as whole numbers. *Carry*: adding two whole numbers in binary
produces a carry where both have a one; t is a subset of s exactly when subtracting t from s needs no borrow.
*Convolution on a group G with kernel c*: the matrix with entry c(g - h). *Flat*: all entries of the same size.

## 0. In ten lines

1. [ran, 4 to 32 points] **The first experiment.** P D' P^T with D' = (-2)^t agrees with H modulo 2 only; half the difference
   has rank k - 1 modulo 2. With D'' = (-2)^(number of ones of t) it agrees modulo 4 and not modulo 8; a quarter of the
   difference has rank 2(k - 1) modulo 2. The entries wrong modulo 8 number N(N/2 - 1). Neither is close to H: the difference
   has rank N - 1 over the rationals, and the entries grow to 7 x 10^17 at 32 points.
2. [derived + ran] **The distance between the row and the cube is one matrix, W = Z^-1 P, and it is made of carries.** Row t of
   W is the list of coefficients of the product, over the ones i of t, of ((1 + y)^(2^i) - 1). Modulo 4: W = I + 2G, where G
   moves, for every pair of ADJACENT address bits, the pattern 01 to 10 and the pattern 10 to 11.
3. [ran, 4 to 128 points] **Growth law of the correction.** Non-zero entries of W modulo 2, 4, 8: N, N(k + 1)/2,
   N(k + 1)(k + 2)/8. Each further binary digit of agreement between the row and the cube multiplies the size of the
   correction by about (log2 N)/2. The correction is not small, not sparse and not of low rank (rank N - k modulo 2).
4. [ran, exhaustive mod p + one exact circuit] **Three cousins on 4 points cost 3, 4, 5 gates**: prefix sums T (carries
   allowed), subset sums Z (no carries), Pascal P (carries counted). At 8 points: 7, 12, and for P none with 12 modulo 3,
   none with 11 modulo 5. The row cousin that is Z modulo 2 is the dearest of the three.
5. [derived] P D' P^T can never be H for any diagonal D': H = Z D Z^T is the only way to write H as (unit triangular) x
   diagonal x (transpose) in this order of the addresses. What P D' P^T is: the same 2 x 2 kernel in its (N - 1)-fold
   symmetric power instead of its k-fold tensor power. The two powers agree modulo 2 (that is Lucas' theorem) and only there.
6. [ran] The row has its own transform with the same shape: the Fourier matrix of the cyclic group, x^(st), equals
   L D L^T with L the Pascal matrix of q-binomials at q = x. At x = -1 and 2 points this is H = Z D Z^T. So Z D Z^T is the
   cube's copy of a row identity, and the row's version costs more, not less (cyclic 4 points: 8 gates against 7).
7. [ran] **The transform can be put in a row, a short one.** Read an address as the power series 1 + a_1 x + ... + a_k x^k
   modulo 2 and multiply series (a second addition on addresses, with carries). At 8, 16, 32, 64, 128 and 256 points H is,
   up to free signs and relabellings, a convolution for that addition (twisted when k is odd): on Z/4 x Z/2, Z/8 x Z/2,
   Z/8 x Z/2 x Z/2, Z/8 x Z/4 x Z/2, Z/8 x Z/4 x Z/2 x Z/2, Z/16 x Z/4 x Z/2 x Z/2. Exhaustively at 8 and 16 points: never on a
   single cycle of N points. [derived] The longest cycle has 2^ceil(log2(k+1)) points, at most 2 log2 N; and the route
   "split along the cycles, act, merge" costs (4/3) N log2 N, more than the textbook (section 5).
8. [derived] Three lemmas say why the row's cheapness stops at H: outputs of H are independent (the one-helper trick needs
   outputs in a space of few dimensions); a flat kernel c with q * c = r needs (non-zeros of q) x (non-zeros of r) >= N, on
   any group and also without translation invariance; every rescaling of H into a group convolution is forced to have
   entries of size 1, so the trick that makes Pascal cheap (rescale by factorials) has nothing to grab.
9. [ran + recalled] Pascal is the specimen wave 7 asked for of **tall wires that pay**: with coefficients bounded by 1 it
   needs at least 0.0707 N^2 gates (a minor of that size), with free coefficients about N^1.585 or less.
10. State: a wall I can name (section 6). Five mutations in section 7; the one I would run first is a search over
    whole-number circuits whose outputs need only be Z modulo 2.

## 1. The first experiment [ran, `first.py`, `first.out`]

| points | D' = (-2)^t: agrees modulo | rank mod 2 of difference/2 | D'' = (-2)^(ones of t): agrees modulo | rank mod 2 of difference/4 | entries wrong mod 8 (D'') | largest entry (D'') |
|---|---|---|---|---|---|---|
| 4 | 2 | 1 | 4 | 2 | 4 of 16 | 31 |
| 8 | 2 | 2 | 4 | 4 | 24 of 64 | 3,423 |
| 16 | 2 | 3 | 4 | 6 | 112 of 256 | 158,636,511 |
| 32 | 2 | 4 | 4 | 8 | 480 of 1024 | 696,102,845,583,964,895 |

- Why [derived]: modulo 4 only the columns t with at most one 1 count for D'', and C(s, 2^i) is odd exactly when bit i of s
  is 1 (Lucas), so P D'' P^T = 1 - 2 (number of common ones) = H modulo 4. For D' only t = 0 and t = 1 count, so modulo 4 the
  product sees the lowest bit alone: the difference from H is 2 x (common ones among the other k - 1 bits).
- The same holds for EVERY whole-number matrix V that is Z modulo 2: V D'' V^T = H modulo 4. Agreement modulo 4 is not a
  property of Pascal. x-1 already has a matrix equal to H modulo 4 in 3N - k - 3 gates, so this buys nothing.
- H = P M P^T with M = W^-1 D W^-T: M is not near diagonal (42 of 56 off-diagonal entries non-zero at 8 points, 210 of 240
  at 16; its diagonal starts 1, -2, -10, -36, -74, -140, -532, -1864).

## 2. The row is the cube plus carries [derived + ran, `first.py`, `second.py` part A/B]

- **Both matrices are "coefficients to values".** P takes the coefficients of a polynomial in the basis of binomials C(x, t)
  to its values at 0, 1, ..., N - 1. Z does the same for the basis "product of the bits of x named by t". The step
  "x to x + 2^i" is (1 + step by one)^(2^i); on the cube it is counted as one new step. Hence
  **P = Z W, row t of W = coefficients of the product over the ones i of t of ((1 + y)^(2^i) - 1)** [checked at 4 to 32
  points]. W is triangular with ones on the diagonal and is the identity modulo 2.
- **Carry law** [derived, checked at 4 to 128 points]: (1 + y)^(2^i) = 1 + y^(2^i) + 2 y^(2^(i-1)) modulo 4, so
  W = I + 2G modulo 4 with G = sum over i = 1..k-1 of G_i, where G_i has a 1 in row t, column t - 2^(i-1) for every t whose
  bit i is 1. On the two bits (i, i-1) that is: 10 takes from 01, and 11 takes from 10. G has (k - 1) N/2 ones.
  The same entry appears at 4 points in all three cousins: T_4 - Z_4 is the single entry (row 10, column 01), and
  P_4 - Z_4 = 2 x (that entry and the two entries of row 11).
- **Growth** [ran]:

| points | non-zeros of W mod 2 | mod 4 | mod 8 | mod 16 | mod 32 | all of W | Yates' gates for Z |
|---|---|---|---|---|---|---|---|
| 8 | 8 | 16 | 20 | 22 | 24 | 24 | 12 |
| 16 | 16 | 40 | 60 | 74 | 84 | 104 | 32 |
| 32 | 32 | 96 | 168 | 230 | 288 | 448 | 80 |
| 64 | 64 | 224 | 448 | 676 | 910 | | 192 |
| 128 | 128 | 512 | 1152 | 1912 | 2758 | | 448 |

  Modulo 4: N(k + 1)/2 exactly [derived]. Modulo 8: N(k + 1)(k + 2)/8, fits all six sizes [ran; not derived]. Modulo 16: no
  formula fitted; about N k^3/48 [guess]. So the answer to the brief's question "the cost of the correction back to Z as a
  function of the power of 2 to which the two agree" is: **it goes the wrong way.** A row matrix that agrees with Z to q
  binary digits is Z times a correction with about N (log2 N)^(q-1) / (2^(q-1) (q-1)!) entries; the first correction alone
  (G) is k - 1 passes over adjacent bit pairs, as large as Yates' whole circuit.
- (W - I)/2 has rank N - k modulo 2 (2, 5, 12, 27 at 4 to 32 points) and W - I has rank N - 2 over the rationals: no
  low-rank shortcut either.
- A word that recurs [guess, a coincidence until shown otherwise]: j-cross found that every gate saved in the small circuits
  is paid for by a wire "entangled on two adjacent address bits"; the carry operator G lives on exactly such pairs.

## 3. Three cousins and what they cost [ran + derived]

Three whole-number matrices with ones on the diagonal, on the same N addresses:

| matrix | entry (s, t) | meaning | 4 points | 8 points | law |
|---|---|---|---|---|---|
| T, prefix sums | 1 if t <= s | carries allowed | 3 | 7 | N - 1, exact (one gate per output is forced) |
| digitwise T in base 2^j | 1 if every base-2^j digit of t <= that of s | carries allowed inside a digit | | | (k/j)(1 - 2^-j) N [derived] |
| Z, subset sums | 1 if t inside s | no carries | 4 | 12 | (N/2) log2 N (Yates) |
| P, Pascal | C(s, t) | carries counted (the power of 2 in C(s, t) is the number of carries) | 5 | at least 13 mod 3, at least 12 mod 5 | see below |

- 4 points [ran, exhaustive mod p, `mc.out`]: Z: none with 3 gates modulo 3, 5, 7 (the known answer; it checks the tool).
  P: none with 4 gates modulo 5, 7, 11; an exact circuit with 5 [derived, replay by eye]:
  o1 = a0 + a1; u = a1 + a2; o2 = o1 + u; t = a0 + a3; o3 = t + 3u. (Modulo 3 P has a 4-gate circuit because C(3,1) and
  C(3,2) vanish there: a small-prime accident.)
- 8 points [ran, exhaustive mod p]: P: none with 12 gates modulo 3 (236 s), none with 11 modulo 5; 12 modulo 5 not decided
  (stopped at 240 s). No upper bound searched (finite differences give 28).
- **The ladder of dominance sums.** Z's pattern is contained in "digitwise at most in base 4", that in base 16, and so on up
  to T. Costs fall along the ladder from (1/2) N log2 N to N - 1: rates per N log2 N of 1/2, 3/8, 7/24, 15/64. And
  Z = (T_4 minus the one carry entry) to the tensor power k/2. So **subset sums are prefix sums in log2 N dimensions with
  sides of length 2**, and the cost of prefix sums on a grid is (number of dimensions) x N: linear for any fixed number of
  long sides, N log N for the cube. That is the cleanest form I found of "why the row is cheap and the cube is not".
- **Pascal with bounded and with free coefficients** [ran `second.py` part D; recalled: Morgenstern's theorem, a circuit
  whose coefficients are at most 1 in size has at least log2 of any minor gates]. The minor of P on rows N/2.., columns
  N/4.., size N/4 has log2 = 4.3, 17.8, 72.1, 289.4, 1159.0 at 8 to 128 points: 0.0707 N^2. So with bounded coefficients
  P needs of the order of N^2 gates. With free coefficients [derived, not built]: C(s, t) = s! x (1/t!) x (1/(s - t)!),
  so P = (scale by 1/t!), then multiply by the FIXED series sum of y^j / j!, then (scale by s!). A fixed polynomial
  product is a linear circuit of about N^1.585 gates by Karatsuba's method with rational coefficients, and of the order of
  N log N if roots of unity may be used. The wires in between are scaled by factorials. This is a proven case of
  "tall wires pay", by a quadratic-to-nearly-linear margin, and its mechanism is one sentence: **a diagonal change of
  scale turns the matrix into a translation-invariant one.** Section 6 asks whether H has such a rescaling (it has not).

## 4. Why P D' P^T is not H, and what the row's own transform is [derived; ran `second.py` parts C, E]

- **Uniqueness.** A matrix has at most one factorisation (triangular with unit diagonal) x diagonal x (its transpose).
  For H in the natural order of addresses it is Z D Z^T. So P D' P^T differs from H for every diagonal D', and more
  generally the only V with V = Z W, W unit triangular, V D' V^T = H is Z itself.
- **What it is instead.** Take the 2 x 2 kernel h = [[1,1],[1,-1]] = [[1,0],[1,1]] diag(1,-2) [[1,1],[0,1]]. Its k-fold
  tensor power is H = Z D Z^T. Its (N - 1)-fold symmetric power (how h acts on polynomials of degree N - 1 in two letters) is
  an N x N matrix K with the same shape of factorisation, Pascal-type factors and the diagonal (-2)^t. [ran] K K = 2^(N-1) I
  at 4 to 32 points: K is a mirror too. All entries of K are odd; (K - J)/2 has rank 2 modulo 2 for every N, against k for H.
  So the row has a mirror of its own; it is not H, and it agrees with H modulo 2 only.
- **Lucas' theorem is the statement that the two powers agree modulo 2.** [recalled: Steinberg's tensor product theorem] In
  characteristic 2 the (N - 1)-fold symmetric power of the 2 x 2 kernel IS the tensor product of its k "twisted" copies; for
  [[1,0],[1,1]] the twist does nothing, and that is "C(s, t) is odd exactly when t is inside s". Over the whole numbers the
  two powers are different representations (one irreducible, one not), so no whole-number change of basis carries one to
  the other. This is why section 2's correction cannot be small.
- **The q-ladder** [ran: the identity as polynomials in x for s, t < 8]. With [s, j] the q-binomial at q = x and [j]! the
  q-factorial: **x^(st) = sum over j of [s, j] [t, j] x^(j(j-1)/2) (x - 1)^j [j]!**. At x = -1 on 2 points this is
  H = Z D Z^T with the entry -2. At x = i on 4 points [ran]: the Fourier matrix i^(st) = L D L^T with
  L = [[1,0,0,0],[1,1,0,0],[1,1+i,1,0],[1,i,i,1]], D = (1, -1+i, 2+2i, 4i), and L is Z modulo the prime 1 + i.
  At x = -1 on N points the q-Pascal matrix is (Pascal of size N/2) tensor [[1,0],[1,1]]; at x = 1 it is P.
  So "which whole-number lifts of Z modulo 2 exist": one for every way of grouping the bits into digits (Pascal of size
  2^j to the tensor power k/j), and over the rings with roots of unity one for every abelian group of order N; the
  product L D L^T is that group's Fourier matrix. Z itself is the member for the group of the cube. None of the others is
  cheaper at the sizes checked: Pascal on 4 points 5 gates against 4; [ran, exhaustive mod p, `mc2.out`] the cyclic Fourier
  matrix on 4 points 8 gates (none with 7 modulo 13 and 17; the 7-gate circuit found modulo 5 needs i = -3 and does not
  lift) against 7 for H.

## 5. The transform literally in a row [ran, `torus.py`, `torus2.py`; derived]

Question: is H, up to free signs and relabellings of inputs and outputs, a convolution on a group that has a long cycle?
Then the rows of the group would be rows in the brief's sense. Test, exhaustive over all 2^(N-1) sign kernels c with
c(0) = +1: the matrix c(g - h) has orthogonal rows, and after scaling its first row and column to +1 its rows are closed
under entrywise product (closed means: the rows are the N characters of the cube's group, so the matrix is H relabelled).
"Twisted" in direction j: the entry changes sign when the subtraction wraps around in that direction (equivalently the
kernel is a sign times a power of a root of unity).

| points | group | plain kernels that give H | twisted kernels that give H |
|---|---|---|---|
| 8 | Z/8 | 0 | 0 |
| 8 | Z/4 x Z/2 | 0 | 16 for each of the three twists |
| 8 | Z/2 x Z/2 x Z/2 | 0 | 32 for each of the seven twists (all + with all three twisted is the given fact "(-i)^distance") |
| 16 | Z/16 | 0 | 0 |
| 16 | Z/8 x Z/2 | 64 (of 192 with orthogonal rows) | 0 (64 with orthogonal rows for one twist, none of them H) |
| 16 | Z/4 x Z/4 | 192 (all) | 0 |
| 16 | Z/4 x Z/2 x Z/2, Z/2^4 | 448 each (all) | not run |

- One kernel on Z/8 x Z/2, written as two polynomials in the generator x of the 8-cycle: c0 = 1 - x - x^2 + x^3 - x^4 -
  x^5 + x^6 + x^7 and c1 = -1 + x - x^2 + x^3 + x^4 + x^5 + x^6 + x^7. Then c0 - c1 = 2(1 - x - x^4 - x^5) is -4x where
  x^4 = 1 and +4 where x^4 = -1, and c0 + c1 is 4x^3 and -4x^2 there [derived]. So on each of the four pieces cut out by
  the subgroup {x^4, second letter} the kernel is a single shifted copy: the transform is "split into 4 pieces, shift each
  piece, merge". Cost 2 x 4 x (7 gates) = 56, the tie that g-0 found for the mirror's basis. The long cycle adds nothing here.
- **Explicit replay** [ran, `replay16.py`, `replay16.out`]: for the kernel above, signs r, s and relabellings pi, sigma of
  the 16 group elements by 4-bit addresses with c(g - h) = r(g) s(h) (-1)^(common ones of pi(g) and sigma(h)) on all 256
  entries. In those addresses "add one along the 8-cycle" is an invertible bit matrix plus a shift, of order 8, and
  (matrix - identity) has its third power non-zero and its fourth zero: one chain of four bits, each added into the next.
  That is Pascal's rule C(s+1, j) = C(s, j) + C(s, j-1) modulo 2.
- **Law for the longest row** [derived; the ingredient "the symmetries of H act on its rows by invertible bit matrices plus
  shifts" is recalled]. A group over which H is a (twisted) convolution acts on the N rows through such maps. A map of
  2-power order of that kind is a (k + 1) x (k + 1) triangular bit matrix with ones on the diagonal, whose order is at most
  2^ceil(log2(k+1)). So the longest cycle has **4 points at N = 8, 8 points at N = 16 to 128, 16 points from N = 256**: at most
  2 log2 N. Both exhaustive runs agree (4 yes and 8 no at 8 points; 8 yes and 16 no at 16 points).
  How the row sits in the cube: point s of the cycle goes to the address with bits C(s,1), C(s,2), ..., C(s,k) modulo 2,
  and "s to s + 1" is Pascal's rule on the bits. Lucas' theorem again, used in the opposite direction.
- **Which group it is** [derived; matches both exhaustive runs; run to 256 points below; not proved for general k]. Read an address a_1 ... a_k as
  the power series 1 + a_1 x + ... + a_k x^k with coefficients modulo 2, cut off after x^k, and MULTIPLY such series. That is
  a second addition on the cube's addresses, with carries, and every "add u" is an invertible bit matrix plus a shift. The
  group is the product, over the odd j up to k, of a cycle of 2^ceil(log2((k+1)/j)) points (generated by 1 + x^j):
  Z/4 x Z/2 at k = 3 and Z/8 x Z/2 at k = 4, exactly the two groups the exhaustive search found; Z/8 x Z/2 x Z/2 at k = 5;
  Z/8 x Z/4 x Z/2 at k = 6 (run below to k = 8). (These are the "Witt vectors" of the two-element field, the standard way to build whole
  numbers modulo 2^m out of bits with carries [recalled].) About half of its factors are still Z/2: the transform's row is
  mostly cube.
- **Pushed to 256 points** [ran, `witt.py`, `witt.out`, `witt678.out`; exact]. Rows labelled by the series itself; columns
  labelled by a one-to-one map w chosen so that every group element is a symmetry of H up to signs (all such w are
  enumerated through their values on the generators 1 + x^j, j odd). "H = signs x (twisted) convolution x signs" is then a
  linear system modulo 2 in the unknown signs and kernel, solved exactly:

| points | group of series | result |
|---|---|---|
| 8 | Z/4 x Z/2 | 4 labellings, each works with one twist |
| 16 | Z/8 x Z/2 | 16 labellings, 8 work, plain |
| 32 | Z/8 x Z/2 x Z/2 | 32 labellings, 16 work, twisted |
| 64 | Z/8 x Z/4 x Z/2 | works, plain (stopped at the first) |
| 128 | Z/8 x Z/4 x Z/2 x Z/2 | works, twisted (stopped at the first) |
| 256 | Z/16 x Z/4 x Z/2 x Z/2 | works, plain (stopped at the first) |

  The 16-cycle appears at 256 points, where the law says it should. Plain for even k, twisted for odd k (a plain sign
  kernel needs N to be a square). [recalled, not looked up: matrices that are convolutions up to such signs are called
  group-developed or cocyclic in design theory, and Sylvester's matrix is known to be one over many groups; I do not
  know whether this particular family is written down.]
- **What these rows buy: nothing by the obvious route** [derived, not built]. Splitting a cycle of n = 2^e points into its
  rational pieces (x^(n/2) = +1 or -1, then again on the +1 part) costs 2 - 2/n gates per point, against e for the full
  transform of e bits. The group has about k/4 factors of 1 bit, k/8 of 2 bits, k/16 of 3 bits, and so on, so splitting
  along all cycles costs (2/3) N log2 N in the limit (the sum over e of (2 - 2^(1-e)) / 2^(e+1)), against 1 for the cube's
  own split, which is H itself. But a convolution is computed as split, act on the pieces, merge, and that pays the split
  twice: (4/3) N log2 N even if the middle were free (it is not: the pieces are large). The average factor has 2 bits; the
  route would need more than 4. Splitting each of the about k/2 factors once only (x^(n/2) = +1 or -1) and merging costs
  about N log2 N, and there the middle can be free (it is at 16 points, first bullet): that is the known route "half
  transform on sqrt N points, relabel, half transform back", the usual tie. So the row form of H is a frame, not a saving.

## 6. The wall, in three lemmas [derived]

The row is cheap in exactly two ways tonight. (a) x-1's helper: outputs that span few dimensions (a polynomial of degree 2
has three coefficients). (b) Recurrences along the row: prefix sums, and Pascal after rescaling; in both the operator is a
ratio of sparse expressions in the step-by-one map.

- **Lemma 1 (a) needs dependence.** A helper serves two outputs only if three or four outputs are dependent; the N outputs
  of H are independent and two rows differ on exactly N/2 points. (This is w-cross's DISTANCE; nothing new.)
- **Lemma 2 (uncertainty).** Let c be a flat kernel on any abelian group of order N (all Fourier coefficients of size
  sqrt N), and q * c = r. Then (non-zeros of q) x (non-zeros of r) >= N. Proof: sum |r|^2 = N sum |q|^2, and
  sum |r|^2 <= (non-zeros of r) (sum |q|)^2 <= (non-zeros of r)(non-zeros of q) sum |q|^2. The same holds row by row
  without translation invariance: a combination of m rows of H has at least N/m non-zeros [recalled: the uncertainty
  principle for finite abelian groups]. So "H = (sparse triangular)^-1 x (sparse)" costs at least 2 N^1.5 in one level,
  and nesting it log N times is the textbook. Prefix sums and Pascal escape because their kernels are far from flat.
- **Lemma 3 (no tall rescaling).** If diag(a) H diag(b), with rows and columns relabelled, is a convolution c(g - h) on a
  finite abelian group, then all entries of c have the same size. Proof: rescaling does not change the 2 x 2 cross-ratios,
  which are +-1 for H; so for every step d the ratio c(u + d)/c(u) is the same up to sign for all u, say +-rho_d; going
  around the cycle of d returns to the start, so rho_d has size 1. Hence the rescaling has entries of one size, c is flat,
  and Lemma 2 applies. On a
  single cycle of N >= 8 points there is no such kernel at all [ran at 8 and 16, plain and twisted; recalled for larger N:
  Turyn's theorem for the plain case].

Together: the brief's hope was a matrix that is Z modulo 2 and cheap in a row for a reason the cube cannot see. The cheap
row objects are T (not Z modulo 2: it differs by the carry entries) and rescaled convolutions (Pascal: Z modulo 2, but
dearer than Z, and at distance "k - 1 passes" already modulo 4). The transform itself does live on rows, those of the
addition with carries of section 5, but they have at most 2 log2 N points, its kernel there is flat (Lemma 2 applies), and
the route through them costs 4/3 of the textbook.

## 7. Mutations ("yes, and")

1. **Search the lifts directly.** Nobody has searched for the cheapest whole-number matrix that is Z modulo 2 with the
   rest free. [derived] *Shadow lemma*: scale every wire to whole numbers without common factor and reduce modulo 2 (its
   shadow). A gate either copies a shadow, or adds two different shadows, or meets two EQUAL shadows (a collision) and
   then reads the next binary digit, where a carry is the entrywise AND of two shadows. A circuit without collisions for
   any lift of Z is at least as large as the best adding-modulo-2 circuit for Z. So a lift cheaper than Yates must use
   collisions, and collisions give the one operation (AND) under which Z's rows are closed: row(s) AND row(s') =
   row(s AND s'). Tool needed: a search over circuits modulo 8 with the target "any row whose shadow is the row of Z";
   8 points, 11 gates. A fact that makes it finite [derived]: from two wires u, v one gate reaches exactly the three
   shadows of the whole-number points of the plane through u and v (two of them are the shadows of u and v when those
   differ; when they are equal the plane holds two new ones). I had no time to build it. (For H the meter is silent: the 19-gate circuit and the textbook have no
   collision at all; every gate after the first 7 is "odd times a wire plus even times a wire".)
2. **Tree passes.** The row's cheap map in general form is a pass over a merge tree (sums and differences of sibling
   blocks, 2(N - 1) gates; a chain gives prefix sums, a balanced tree the Haar transform; maps of this kind with a
   relabelling in between are tall and ill-conditioned for free). Question: how many tree passes, over DIFFERENT trees
   with relabellings and scalings in between, does H need? One is impossible for N > 2 (Lemma 2); log2 N is the textbook.
   A number that stays bounded as N grows would be linear size. This is k-cross's "sum of rectangles over two merge
   trees" extended to more than two trees; the existence question is exact and finite at 8 and 16 points.
3. **The dominance ladder as a target for the engine.** The matrices "digitwise at most in base 2^j" cost
   (k/j)(1 - 2^-j) N and contain Z's pattern; Z = (T_4 - carry)^(tensor k/2). Is there a product formula for H through the
   base-4 or base-16 member with a correction of fewer than N log N gates? I found none; the expansion of the tensor
   power has 2^(k/2) terms.
4. **The second addition and address maps.** "Multiply by the series u" is an invertible bit matrix plus a shift on the
   addresses: an address map in the engine's sense (free there), and "add one along the row" is Pascal's rule on the bits.
   Blocks of 45 bits admit cycles of 64 points. The engine's units need address maps (the tiny-unit cut-set lemma); the
   commuting family of all multiplications by series is a structured supply of N of them that nobody has tried as a
   pool. I did not test whether the published unit's maps are of this kind.
5. **For brief 3 (tall pool).** Pascal on 8 to 32 points is a ready-made test of whether a search with tall wires can find
   a circuit below the bounded-coefficient floor (0.0707 N^2: 4, 18, 72 gates at 8, 16, 32 points; the floor passes the
   trivial N - 1 from 16 points on, 18 against 15, so the test starts there).

## 8. Growth laws found

| object | numbers | law | status |
|---|---|---|---|
| P D' P^T against H, D' = (-2)^t | agrees mod 2; rank mod 2 of half the difference 1, 2, 3, 4 | k - 1 | ran 4 to 32 points; derived |
| the same, D'' = (-2)^(ones of t) | agrees mod 4; rank 2, 4, 6, 8; entries wrong mod 8: 4, 24, 112, 480 | 2(k - 1); N(N/2 - 1) | ran; first derived |
| correction W = Z^-1 P modulo 4 | 6, 16, 40, 96, 224, 512 non-zeros | N(k + 1)/2 | derived, ran 4 to 128 points |
| the same modulo 8 | 6, 20, 60, 168, 448, 1152 | N(k + 1)(k + 2)/8 | ran; fits six sizes; not derived |
| prefix sums / subset sums / Pascal, 4 points | 3 / 4 / 5 gates | | exact circuit for each; "none below" modulo p only for Pascal |
| Pascal, 8 points | none with 12 (mod 3), none with 11 (mod 5) | | exhaustive mod p |
| digitwise dominance in base 2^j | | (k/j)(1 - 2^-j) N | derived |
| Pascal, coefficients bounded by 1 | log2 minor 4.3, 17.8, 72.1, 289.4, 1159.0 | at least 0.0707 N^2 | ran; theorem recalled |
| Pascal, free coefficients | | at most about N^1.585 (rational), N log N (roots of unity) | derived, not built |
| longest cycle of a group that carries H | 4, 8, 8, 8, 8, 16 at 8 to 256 points | 2^ceil(log2(k+1)), at most 2 log2 N | attained: ran 8 to 256 points; not exceeded: exhaustive at 8 and 16, derived beyond |
| splitting along all cycles of the series group | | (2/3) N log2 N; H by split, act, merge: at least (4/3) N log2 N | derived |
| cyclic Fourier matrix, 4 points | 8 gates (H: 7) | | exhaustive mod 13, 17 |

No total below (N/2) log2 N for subset sums or below the known counts for H came out, and none is claimed.

## 9. Criticism, last

- The idea as briefed fails for a structural reason (section 4): the row and the cube are two different powers of the same
  2 x 2 kernel and coincide modulo 2 only. I found no way around that; the mutations change the question.
- "Pascal is dearer than Z" rests on 4 points (solid: exact circuit, and no 4-gate circuit modulo three primes) and on
  8 points modulo 3 and 5 only. Modulo 3 the 8-point Pascal matrix is a different matrix (Lucas in base 3), so that run is
  weak evidence about the rationals. "None modulo p" is not "none".
- The law for the longest row: "attained" is run from 8 to 256 points; "not exceeded" uses a recalled fact about the
  symmetry group of H and was checked exhaustively only at 8 and 16 points. At 64 points the first non-trivial
  prediction (no convolution on Z/16 x Z/4, although that group is known to carry matrices with orthogonal sign rows)
  was not run: 2^63 kernels is out of reach for the method used.
- `witt.py` tests one way of labelling rows (the series itself) and the column labellings compatible with it. "Works" is
  certified by an exact solution of the sign system; "does not work" for a given labelling says nothing about others.
- The closure test in `torus.py` normalises by row 0 and column 0; I argued by hand that this decides "is H relabelled".
  The twisted runs covered the groups listed, not Z/4 x Z/2 x Z/2 or Z/2^4 at 16 points.
- Lemmas 2 and 3 are half an hour old and checked by nobody. They close one-level uses of a row (one sparse relation, one
  rescaling); they say nothing about circuits that are not of that shape.
- The 2/3 and 4/3 of section 5 are counts by hand of a route nobody built; they say that route loses, not that every
  use of the second addition loses.
- The N^1.585 and N log N figures for Pascal with free coefficients are the standard route, not built or replayed here; in
  count (G) with rational coefficients only, the N log N figure is not available.
- Literature: nothing was looked up. Steinberg's theorem, Morgenstern's theorem, Turyn's theorem, the symmetry group of H
  and the q-binomial identity are from memory; the identity alone was checked by machine.

Files (`waves/wave-08/ab-7-transforminarow/`): `first.py`, `first.out` (section 1,
W's closed form, ranks); `second.py`, `second.out` (carry law, size of W modulo 2^q, q-Pascal identity, Pascal's minor, the
spin matrix K); `rows_pascal4.txt`, `rows_pascal8.txt`, `mc.sh`, `mc.out` (minimum circuits modulo p for Z and P at 4 points
and P at 8; `mc4.out` is a failed first launch, ignore); `rows_h4.txt`, `rows_f4_p5.txt`, `rows_f4_p13.txt`,
`rows_f4_p17.txt`, `mc2.sh`, `mc2.out` (H and the cyclic Fourier matrix at 4 points); `torus.py`, `torus.out` (plain
kernels, all five abelian groups of order 16); `torus2.py`, `torus2.out` (plain and twisted kernels, orders 8 and 16);
`replay16.py`, `replay16.out` (explicit signs and relabellings at 16 points; "add one" as a bit map);
`witt.py`, `witt.out` (k = 3, 4, 5, all labellings), `witt678.out` (k = 6, 7, 8, stopped at the first that works).
