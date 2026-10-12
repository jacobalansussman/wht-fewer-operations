# ad-4 flat-rank: the number of coset sums that add up to the transform's kernel is at least k (not k/2), exactly 4 at 16 points, at most 11 at 256; free row and column signs halve it (the 7-gate brick is 2 flats); it does not price gates

> Editor's note (11 October 2026): a critic corrected one bound of this report. "At least 2 log2 N" flats fails once the signs of rows and columns are free: 2 flats at 4 points ([af-2](af-2.md)).

11 October 2026, about 06:24 to 07:08 EDT, 60-minute box. Private. One agent; nothing reviewed, nothing in Lean, nothing published.
Marks: [ran] = run of mine tonight (files in `ad-4-flatrank/`; whole numbers or fractions unless a line says FLOATS);
[derived] = by hand tonight, checked by nobody; [read] = from tonight's reports or from a web search summary (said where);
[recalled] = from memory, no source read; [guess].
Gate count everywhere: **(G)**, a gate is any a*u + b*v, scalings free. Count (O), OpenAI's, is not used.

**No circuit below a known count, no growth law below N log N, nothing of the 1e-1 kind. Nothing here changes the order.**
What is new: two exact values (4 flats at 16 points; 4 flats at 8 points of the doubled class even with free signs),
one theorem that doubles the known lower bound (k, not k/2), one construction that beats the known upper bound (11, not
16), the family in which the bound drops (free row and column signs: the 7-gate brick is "2 flats"), and the reason why
the number of flats is the wrong count for gates (the right one is k-cross's rectangle count).

## Words

N = 2^k points; an *address* is k bits. *Flat*: a subspace of the address space or a shifted copy of one; its *dimension*
is the number of free bits. *Signed flat*: the function that is +1 or -1 on a flat, by a sign (-1)^(b.z), and 0 off it
(taken up to a factor); *unsigned*: the sign is +1 everywhere. *Coset sum*: the convolution with a flat's indicator
(N - N/|V| gates; with a sign it is one more free rescaling on each side). *Quadric signs* g: -1 where
z1 z2 + z3 z4 + ... = 1, +1 elsewhere (k even); the transform is, up to free signs and one relabelling, the convolution
with g. *Flat rank* r(k): the least number of flats whose combination, with any rational coefficients, is g; r_s with
signed flats, r_u with unsigned ones (r_s <= r_u). *B*: the pairing B(u, z) = g(u+z) g(u) g(z) g(0) read as a bit; two
address sets are *perpendicular* when B vanishes between them; a *Lagrangian* is a subspace of k/2 bits perpendicular to
itself. *Doubled address space*: the 2k bits (x, y) of an output address and an input address; H(x, y) = (-1)^(x.y) is
quadric signs on those 2k bits, so **the flat rank of the N-point transform in the doubled class is r(2k)**.
A flat of the doubled space, read as an N x N matrix, touches 2^p rows and 2^q columns and has rank 2^t: it is "sum the
inputs over 2^t classes of 2^(q-t) columns, hand each sum to 2^(p-t) outputs".

## 0. In ten lines

1. [ran, exhaustive, exact] **16 points: the flat rank is exactly 4, signed and unsigned.** No 2 and no 3 of the 1,072
   signed flats span g (10,251,120 covering triples, whole-number Gram determinants; control: the same program finds
   ab-0's 7 pairs for neighbour sums). 4 unsigned flats: g = 1 - 2 [z1 z2 = 11] - 2 [z3 z4 = 11] + 4 [z = 1111].
   The curator's "5 without signs" is the count of aa-cross's ruling, not the minimum.
2. [derived] **Theorem (pair kill). r_s(k + 2) >= r_s(k) + 2, so the flat rank of quadric signs on k bits is at least k**,
   signed or unsigned. aa-cross and ab-3 had k/2. Tight at k = 2 and 4. Section 2.
3. [ran, exact] **The upper bound 2^(k/2) is not the truth: at 256 points 11 unsigned flats suffice** (16 by the product):
   g = -1 + 2 (nine subspaces of 4 bits that meet pairwise in 0) - 16 [z = 0]. The nine subspaces were found by a search
   (8 alternating 4 x 4 matrices with invertible differences, plus one) and the identity checked on all 256 entries.
   [recalled, not run] The same exists whenever k is a multiple of 4: 2^(k/2 - 1) + 3 flats. Powers of the 11 give
   r(k) <= 2^(0.4324 k). Section 3.
4. The table. k = 2, 4, 6, 8: lower bound 2, 4, 6, 8; upper bound 2, 4, 8, 11; exact 2, 4, open, open.
   **Growth law: between k and 2^(0.43 k). I could not decide polynomial against exponential.** Section 5 says why.
5. [ran] 64 points: between 6 and 8. No decomposition into 5, 6 or 7 flats that is invariant under an isometry of order
   5 or 7 (all orbits; FLOATS for the test), none of the kind "two orbits of an isometry of order 3, plus at most one
   invariant flat" (EXACT; 11.3 million covering pairs and 9.33 thousand million covering triples for one of the two
   classes of such isometries, pairs only for the other). My local search says nothing about 7: its control failed. Section 4.
6. **Doubled class** [ran + derived]: the transform at 4, 8, 16 points is a sum of 4, at most 8, at most 11 flats of the
   doubled space (k-cross's rectangles: 5, 13, 49), and of at least 2 log2 N at every size. Prices in gates: section 6.
   The 11 at 16 points are the constant, one row, one point and eight matrices with a single 1 in every row:
   H_16 = -J + 2 [x = 0] + 2 (sum over 8 matrices S of [y = S x]) - 16 [x = y = 0]. As a circuit it costs 136 gates
   (textbook 64): every output adds 8 inputs.
7. [derived] **Why the number of flats does not price gates.** Adding r pieces at the outputs costs up to N per piece,
   and r >= k (plain class), 2k (doubled class), k again (doubled class with free quadratic signs, line 8):
   "T(N) <= 2N x flat rank" can never go below 2 N log2 N in these classes, and the textbook is N log2 N. (With arbitrary
   free signs only k/2 is proved beyond 8 points, which would allow a tie and no more.) What does price gates is the *total rank* (sum of 2^t over the pieces) on a shared system of supports:
   for supports taken from two chains of subspaces, gates <= 4N + total rank. That is k-cross's "N - 2 + rectangles" with
   a flat of rank 2^t counted as 2^t rectangles. Total rank is at least N always and exactly N for the product
   decomposition (which is H = Z D Z^T, supports on the Boolean lattice, price Yates'). Section 6.
8. [derived + ran] **Which family makes the bound fail: free signs on rows and columns** (free in count (G)). With row
   signs a and column signs b, a(x) H(x,y) b(y) is no longer the quadric on 2k bits. At 4 points, a = b = (+,+,+,-):
   **a H b = J - 2 P, the constant and one permutation matrix: 2 flats instead of 4. That is the night's 7-gate brick.**
   With quadratic signs the least rank of the form x.y + alpha(x) + beta(y) is 2, 4, 4 at k = 2, 3, 4 (all pairs, run)
   and k for every even k, so the N-point transform is a member of the k-bit class, not the 2k-bit one: exactly 2, 4, 4
   flats at 4, 8, 16 points, at least log2 N (the theorem again), at most sqrt N. With ARBITRARY signs: **exactly 4 at
   8 points** [derived case analysis + exact run: no sign-rescaled 8-point transform is a combination of 3 signed
   flats], so non-quadratic signs buy nothing there; in general only 3 (N >= 8) and (log2 N)/2 as lower bounds.
   **Open: 3 or 4 at 16 points with arbitrary signs.** Section 7b.
   The other family where the bound is void: pieces that carry a quadratic sign, which are small transforms themselves.
9. [derived] The object has a name elsewhere: a signed flat is a *stabilizer state without quadratic phases* and g is a
   *graph state*; r_s is a restricted *stabilizer rank*. In the unrestricted problem the best exact lower bound I found
   is linear (Peleg, Shpilka, Volk 2021 [read: one search summary, not the paper]), by the same kind of restriction
   argument. Section 5.
10. [ran] A regularity I cannot explain: in all 54 eight-flat decompositions found at 64 points, the most flats that one
    restriction can remove equals the most that one projection can remove (4, 3 or 2 removed: 37, 8, 9 cases).

## 1. 16 points, decided  [ran]

`fr.c`, mode `exh`: all 67 subspaces, all 1,072 signed flats up to a factor (16 x 67), target g. For every pair and every
triple whose supports cover the 16 points, the Gram determinant of (flats, g) in whole numbers: zero exactly when g is
in the span. Result (`exh4.out`): pairs 0, triples 0 of 10,251,120. Control (`ctl4_nb.out`): with the target replaced by
the neighbour-sums kernel the same code finds 7 pairs, which is ab-0's "7 ways" at k = 4.
[derived] Two terms on one support can be replaced by two terms on its halves, so distinct supports lose nothing (ab-0's
remark). [derived] All bent quadratic sign patterns on k bits are one class under shifts, invertible bit matrices, a
global sign and (for signed flats) characters; a shift suffices to absorb a linear term, so r_u is a class number too.
Shapes of 4-flat solutions found by `fr 4 ls 4` and replayed exactly (`verify.out`): dimensions (4,2,2,0) (the product),
(3,3,2,0), (3,2,2,1), (2,2,2,2) (a partition of the 16 points into four non-parallel planes, g a signed constant on each),
and, by the symmetric search, (4,1,1,1): **g = 1 - 2 (three pairs of points)**, the six points where g = -1 paired off.

## 2. The pair-kill theorem  [derived; the dichotomy ran on 60 decompositions]

Notation: a flat is a + V; U = the set of addresses perpendicular to V. A flat of dimension k is a *character*
(U = 0), of dimension 0 a *point* (V = 0).

**Lemma A (restriction).** Let u1, u2 have B(u1, u2) = 1 and let W = {z : B(u1, z) = c1, B(u2, z) = c2}. W has k - 2 free
bits and g restricted to W is a bent quadratic sign pattern on k - 2 bits (same class). A flat a + V misses W as soon as
some non-zero u in {u1, u2, u1 + u2} lies in U with the wrong constant. A flat that meets W restricts to a flat.
So if two flats i, j that are not characters have U_i not perpendicular to U_j, take u1 in U_i, u2 in U_j with
B(u1, u2) = 1 and the two wrong constants: both flats disappear, and r - 2 >= r_s(k - 2).

**Lemma B (projection).** The transform of a signed flat is a signed flat (dimension d becomes k - d, V becomes the
ordinary perpendicular of V), and the transform of g is a multiple of a member of the class. So Lemma A holds on the
other side: if two flats that are not points have V_i not perpendicular to V_j, both can be removed. (This uses signs:
the transform of an unsigned flat is signed. The induction runs in the signed class; r_u >= r_s.)

**Dichotomy.** Suppose neither lemma applies to a decomposition with r >= 3 flats.
A point has U = everything, so with any other non-character it is a pair for Lemma A; a character has V = everything,
so with any other non-point it is a pair for Lemma B. With r >= 3 this leaves no points and no characters. For two
remaining flats, V_i perpendicular to V_j gives V_j inside U_i, and U_i perpendicular to U_j gives U_i inside V_j: so
V_j = U_i for all i different from j, and with three flats all V are one Lagrangian L. Then every flat is a shifted
copy of L, the flats must cover the space, and r >= 2^(k/2).

**Theorem.** For even k >= 4: r_s(k) >= min(r_s(k - 2) + 2, 2^(k/2)), and r_s(k - 2) <= 2^(k/2 - 1), so
**r_s(k) >= r_s(k - 2) + 2 and r_s(k) >= k** (r_s(2) = 2: g is not a character and every smaller flat has a zero).
(r >= 3 at k >= 4 by killing one flat: any non-character lies in half the space.)

Checks [ran]: k = 4 gives 4, the exhaustive value. On the 6 decompositions at 16 points and 54 at 64 points that my search
found, a pair for Lemma A and a pair for Lemma B exist every time, and the restriction was carried out: 2 flats survive
at 16 points (r_s(2) = 2), 4 to 6 at 64 (`verify.out`). Lemma B was replayed in whole numbers on 70 decompositions
(`dualcheck.py`, `dualcheck.out`): every transform is a multiple of a signed flat of the complementary dimension, the
transformed identity holds, the two chosen flats vanish on the restricted set, and the transform of g there is bent on
k - 2 bits; 2 flats survive at 16 points, 4 to 6 at 64. No decomposition with 3, 4 or 5 flats at 64 points turned up in
the symmetric searches of section 4 (the theorem says there is none).
What it gives. aa-cross's "flat rank >= k - D = k/2" becomes k. In the doubled class: **the N-point transform is not a
sum of fewer than 2 log2 N flats of the doubled space.** What it does not give: anything above linear.

## 3. Eleven flats at 256 points: the product bound falls  [ran, exact; general k recalled]

Write the 8 bits as (x, y), 4 and 4, with g = (-1)^(x.y). The 136 zeros of x.y are the union of nine subspaces of 4 bits
that meet pairwise in 0: {x = 0} and the eight graphs {y = S x}, S running over 8 alternating matrices (symmetric, zero
diagonal) whose pairwise differences are invertible. `verify.py` finds such a set by a small search (64 alternating
matrices, 28 invertible) and checks on all 256 entries
   g = -1 + 2 [x = 0] + 2 (sum over the eight S of [y = S x]) - 16 [x = y = 0].
That is 1 + 9 + 1 = **11 unsigned flats; the product gives 16.** Reason it works: for x not 0 the eight values S x are
exactly the eight y with x.y = 0.
[recalled: Dillon, Dye, Kantor; "orthogonal spreads", "Kerdock sets"; not read tonight] Such sets exist for every k
divisible by 4, with 2^(k/2 - 1) + 1 subspaces: 2^(k/2 - 1) + 3 flats (5, 11, 35, 131 at k = 4, 8, 12, 16; at k = 4 the
product's 4 is better). [ran, `dualcheck.out`] For k = 6 there is none: of the 30 subspaces of 3 bits on which g = +1,
120 pairs meet in 0 only and no three do; five would be needed.
[derived] Flats multiply: r(k1 + k2) <= r(k1) r(k2). So r(k) <= 11^(k/8) = 2^(0.4324 k) for k divisible by 8 [from the run],
and 35^(k/12) = 2^(0.4274 k) if the recalled k = 12 set is right. Still exponential.
[derived] Inside the class "subspaces through 0 on which g = +1, plus the constant, plus the point" this is optimal: the
subspaces must cover the zeros.
[read: one web search summary] Cohen and Shinkar, "The complexity of DNF of parities": the least number of flats whose
UNION is exactly the set where x.y = 1 is 2^(k/2) - 1. That is the count without cancellation, on the other level set.

## 4. 64 points: between 6 and 8  [ran]

Lower bound 6: section 2. Upper bound 8: the product; also many others (below).
- **Symmetric searches** (`fr.c` mode `sym`; an isometry h of g of prime order, built from reflections; a decomposition
  = one orbit of flats under h plus at most 2 invariant flats; FLOATS for the test, tolerance 1e-7, every hit printed
  for exact replay). Order 5 (36,152 orbits, 40 invariant flats): **none with 5, 6 or 7 flats** (`sym6_p5.out`).
  Order 7 (25,828 orbits, 4 invariant flats): none with 7; **10 with 8** (the constant plus seven flats of 4 points
  that tile the 28 points where g = -1, and signed variants); 50 with 9 (`sym6_p7.out`). Order 3, one orbit plus at most
  2 of the first 60 invariant flats: none with 3, 4, 5 (`sym6_p3.out`).
- **Two orbits of an isometry of order 3, plus at most one invariant flat** (6 or 7 flats; EXACT, whole-number Gram
  determinants on the orbit sums, `fr.c` mode `sym2`; 60,220 orbits, 140 invariant flats): see the line SYM2 at the end
  of this section.
- **Local search** (`fr.c` mode `ls`, FLOATS; replace one flat at a time by the best of all 180,800): finds 8 flats in
  about 20 steps (54 decompositions replayed exactly, `verify.out`); with 7 flats nothing in 1,100 seconds (least
  squared residual 8 of 64), with 6 nothing (16 of 64) (`ls6_r7_s11.out`, `ls6_r6_s12.out`).
  **This silence is not evidence.** Control: restricted to unsigned flats the search does not find the known 8
  (`ls6_r8_unsigned_ctl.out`, and an annealed variant `ls2_r8_unsigned_ctl.out`): it finds only decompositions that are
  partitions (each flat a signed constant of g), and 7 flats cannot partition 64 points into flats on which g is a
  signed constant (those have at most 8 points). A 7 would have to cancel, and the search is blind to that.
- [derived] Counting conditions any decomposition satisfies: the flats cover the space (sum of 2^d >= 2^k); so do their
  transforms (sum of 2^(k-d) >= 2^k); and sum of 2^min(d, k-d) >= 2^(k/2) (rank of the matrix g(x + y) on two
  complementary Lagrangians). With 6 or 7 flats at k = 6 these force both large and small flats; they do not exclude 6.

SYM2 [ran, exact]: the isometries of order 3 fall in two classes (4 or 16 fixed addresses). Class with 4 fixed
addresses, complete: two orbits (6 flats): 11,343,450 covering pairs, **0 span g**; two orbits plus one of the 140
invariant flats (7 flats): 9,330,332,760 covering triples, **0 span g** (`sym2_6_p3_part0.out`, `sym2_6_p3_part1.out`).
Class with 16 fixed addresses (2,144 invariant flats): two orbits only, 2,915,880 covering pairs, 0 span g
(`sym2_6_p3_seed2_noinv.out`); with an invariant flat: not run (too many).
Control of this mode (`sym2_4_p2_ctl.out`): at 16 points with an involution it finds 24 five-flat decompositions,
replayed exactly, and no four-flat one of the shape "two orbits" (four-flat ones of other shapes exist).

## 5. Growth law: what I can and cannot say

Known now: k <= r_s(k) <= r_u(k) <= 2^(0.4324 k) (k divisible by 8).
**Why the kill method stops at "+2".** [ran, `kill.py`, `kill.out`] For each of the 54 eight-flat decompositions at 64
points I computed the fewest flats that survive any restriction of Lemma A (336 planes x 4 constants) and any projection
of Lemma B. Survivors: 4 in 37 cases, 5 in 8 cases, 6 in 9 cases. So there are decompositions in which no restriction
and no projection removes more than 2 flats: eight shifted Lagrangians, pairwise non-parallel, tiling the space.
A proof of more than "+2 per two bits" has to use minimality, or a third operation. The spread of section 3 is of the
same rigid kind (a restriction removes 2 subspaces and the point: 11 becomes 8).
**Unexplained** [ran]: in all 54 cases the two minima are equal, although the two families of tests are different (the
restriction uses the rules with an even number of ones on the plane's three directions, the projection those with an odd
number, by my reading of the formulas).
**The same problem under another name.** [derived] sign(z) x [z in flat] with a linear sign is a stabilizer state whose
phase has no quadratic part; g is a graph state (k/2 pairs). r_s is a stabilizer rank with a restricted dictionary and a
stabilizer target. [read: one web search summary of arXiv 2106.03214] For the unrestricted stabilizer rank of n copies
of a magic state the proved lower bound is of order n, by "a function of few stabilizer terms is simple on a large
flat": the level-set argument of ab-3 and section 2. [recalled] Later work reaches about n^2 for an approximate version;
exponential is believed and unproved. I take this as a warning: "exponential" may be true here and hard to prove.
**ab-8's random-order argument**, the suggested tool: I did not find the triangular family it needs. It wants labels
with "t sees s only if P_s lies in L_t"; flats in a decomposition have no such one-sided relation (two flats see each
other through their intersection symmetrically). Not a proof that it cannot work.
**A route to "exponential" that I did not finish** [guess]: split a decomposition into large flats, small flats and
middle flats. By covering, the middle flats alone (dimension within s of k/2) must cover whatever the large and small
ones leave, at most 2^(k/2 + s) points each. So a polynomial decomposition needs polynomially many large flats whose
combination already agrees with g on almost all of the space. A combination of few flats of small codimension is a
function of few parities on a large flat; g restricted to a flat of more than k/2 bits is far from every such function
in the mean, but "agrees on almost all points with unbounded coefficients" is not "correlates", and that gap is where I stopped.

## 6. The doubled class and its prices  [ran: `price.py`, `price.out`, `verify.out`; the flag bound derived]

Number of flats for H: N = 4: exactly 4 (5 rectangles). N = 8: 6 to 8 (13 rectangles). N = 16: 8 to 11 (49 rectangles).
Lower bound 2 log2 N at every N; upper bound N, and N/2 + 3 when log2 N is even [recalled beyond 16 points].
Price of a decomposition whose pieces are computed one by one and added at the outputs:
   sum over pieces of (2^q - 2^t)  +  sum over pieces of 2^p  -  N.

| decomposition | N | flats | total rank | price, pieces apart | textbook |
|---|---|---|---|---|---|
| product (one rectangle [x contains S][y contains S] per set S; it is H = Z D Z^T) | 4 / 8 / 16 | 4 / 8 / 16 | 4 / 8 / 16 | 10 / 38 / 130; shared: 8 / 24 / 64 | 8 / 24 / 64 |
| best of 6 found by search | 4 | 4 | 4 | 9 | 8 |
| best of 54 found by search | 8 | 8 | 16 (least seen 14) | 40 (median 51) | 24 |
| spread (section 3) | 16 | 11 | 1 + 1 + 1 + 1 + 7 x 16 = 116 | 136 | 64 |

[derived] **Flags.** If the row supports of all pieces are cosets of the members of one chain of subspaces, and the column
supports likewise, then all class sums cost under 2N (a binary tree), spreading the results back costs under 2N, and
each piece costs its rank: **gates <= 4N + total rank.** With rank-one pieces this is k-cross's N - 2 + rectangles.
[derived] Total rank >= N (ranks add up to at least the rank of H). The product attains N, on supports that form the
Boolean lattice, whose sums cost (N/2) log2 N each side: the textbook count again, exactly.
So the idea turns into k-cross's open count with one new handle: **a flat of rank 2^t is 2^t rectangles moved by one
linear map.** The number of flats is at least 2 log2 N and says nothing about gates; the total rank is at least N and
is the gates. Between "N flats of rank 1 on the lattice" and "11 flats of total rank 116 on no system at all" I found
no decomposition whose supports sit on a system of linear cost with total rank near N; k-cross's 5, 13, 49 are that
question on two trees.

## 7. Which family makes k/2 fail  [derived]

Apply the transform to the y side only. H becomes N times the identity: the single flat {x = y} of the doubled space.
A flat of the doubled space becomes a block (a flat of rows times a flat of columns) filled with a bilinear sign of
rank t. So: **in the class "flats with a quadratic sign" the transform has rank 1 and the bound k (or k/2) is void;
in the class "flats with a linear sign" it has rank at least 2 log2 N.** In between, pieces whose quadratic sign has
rank at most rho: the level-set count gives (number of pieces) x max(1, rho/2) >= k/2 [derived, rough], and such a
piece is a transform on rho/2 bits per block, priced (rho/2) N by the textbook. Pieces x price stays at N log2 N / 2 or
above in every class I can price. The bound fails only where the piece is the thing being computed. This is ab-3's
"codimension is sold at N/2 gates per unit" seen from the side of sums; the sum adds its own N per piece on top.

### 7b. Free signs on rows and columns  [ran: `rescale.py`, `rescale.out`; the bounds derived]

In count (G) every row and every column of the matrix may be rescaled for nothing. So the right target is not H but
a(x) H(x, y) b(y) for the best sign vectors a, b (or any non-zero numbers). Write a = (-1)^alpha(x), b = (-1)^beta(y).
- 4 points, alpha = x1 x2, beta = y1 y2: x.y + x1 x2 + y1 y2 = (x1 + y2)(x2 + y1). So a H b = 1 - 2 [y2 = x1 + 1, y1 = x2 + 1]
  = J - 2 P [ran]. Two flats; total rank 1 + 4 = 5 = k-cross's five rectangles; price 3 + 4 = 7 gates. The brick.
- 16 points, the same signs on each pair of bits: J - 2 (P on the low pair) - 2 (P on the high pair) + 4 (P on both) [ran]:
  4 flats, total rank 25. [derived, not run] As pieces apart it costs about 75 gates; as a product of two bricks 56.
- [ran, all pairs of quadratic alpha, beta] the form x.y + alpha(x) + beta(y) has least rank 2, 4, 4 at k = 2, 3, 4
  (1 of 4, 28 of 64, 28 of 4,096 pairs reach it). [derived] For even k: take alpha with an invertible alternating
  matrix A and beta with its inverse; the rank is k. A sign pattern (-1)^q with q of rank rho has the flat rank of the
  rho-bit class. So **with quadratic signs the number of flats is r_s(k) for even k: 2 at 4 points, 4 at 16, 6 to 8 at
  64 points, 8 to 11 at 256, at least log2 N, at most sqrt N**; and r_s(4) = 4 at 8 points.
- [derived] Arbitrary signs. (i) At least 3 flats for N >= 8: two flats that cover everything are the constant and a
  flat F, and then the matrix is a rank-one sign pattern times J - 2 [F], which has orthogonal rows only for N = 4; or
  two half-spaces, and then the matrix has at most 4 different rows. (ii) x.y + alpha(x) + beta(y) is affine on no
  flat of the doubled space of dimension above 3k/2 (the row-only and column-only directions of the flat must be
  perpendicular), so by the level-set count at least k/2 flats. The pair-kill theorem does not apply: a restriction no
  longer gives a member of the same class.
- **8 points, arbitrary signs: exactly 4** [derived + ran exact: `fr.c` mode `rs`, `rs6.out`; control `rs4.out`].
  Suppose M = a H b is a combination of 3 signed flats of the 6-bit doubled space; they cover the 64 cells.
  Case A, one of them is a character: after multiplying by it, M = c0 + (two signed flats). If c0 is not +1 or -1 the
  two flats cover everything, and M is a signed constant on a half-space, which (ii) forbids (dimension 5 > 4.5). If
  c0 = +1 or -1, M = +-(1 - 2 [E]) and, going through how two signed flats can add up to a function with the two values
  0 and -2 c0, E is a flat, or F1 + F2 (disjoint), or F1 minus F2 (nested), or F1 xor F2 (meeting in half of one).
  Run: 26,387 flats and 222,524,587 such sets E, test "(1 - 2[E]) times H is a rank-one sign pattern" in bit masks:
  **0 hits** (at 4 points the same code finds the brick: 4 single flats).
  Case B, three proper flats: one is a half-space F1; the other half is covered by the other two. Either F2 is the
  complementary half-space, and then M = (-1)^(l l') (1 - 2 [F3]) up to a character, with (-1)^(l l') a signed constant
  on F3. Run over all pairs of linear forms and all flats: 51,535,764 tested, 6,720 are sign-rescaled transforms (these
  are H_2 x brick, 4 flats), **0 of them with a signed constant on F3**. Or F2, F3 cut the other half in two quarters:
  quarter + quarter is a partition with M a signed constant on a half-space (forbidden by (ii)); half-space + quarter
  puts +-1 +- 1 on a doubly covered region; three half-spaces give a pattern with 6 characters of size 1/2, which by
  the sum of squares must collapse to 4, a rank-2 quadratic pattern, whose matrix has at most 4 different rows.
  So 3 is impossible and 4 is attained (H_2 x brick). The case analysis is by hand, tonight, unreviewed; the runs are exact.
  One step of it is machine-checked at 16 points (`twoflat.py`, `twoflat.out`): of the 56,677 combinations of two signed
  flats that take only the values 0 and 1, every support is a flat, a disjoint union, a nested difference or a
  symmetric difference with the intersection half of one flat; none falls outside.
- What this says about the idea. The saving of the brick (7 against 8) is visible in this count as "2 flats instead
  of 4". At 8 points arbitrary signs do no better than quadratic ones. If at larger sizes the number with arbitrary signs
  grew like log N while the number with quadratic signs grows like a power of N, non-quadratic signs would be doing
  something no circuit of the night does; 16 points (3 or 4) is the first place to look.
  It still would not price gates by itself (section 6).

## 8. Criticism, last

- The theorem of section 2 is one page by hand, tonight. Lemma B, which I trusted least, was replayed exactly on 70
  decompositions (`dualcheck.out`); the dichotomy's case analysis is by hand only. The exhaustive value 4 at 16 points
  agrees with the theorem; at 64 points it is tested only by "no symmetric decomposition with 5 or fewer flats found".
- The 11 at 256 points is exact. The general 2^(k/2 - 1) + 3 is recalled. The non-existence at k = 6 is a run.
- 64 points is not decided. The symmetric searches cover a small part of the space (three conjugacy classes, three
  shapes); the test inside `sym` is in floats; "none found" is not "none".
- The price column counts pieces apart; I did not look for sharing between the pieces of a found decomposition.
- The flag bound "4N + total rank" is derived, not run on an example; it is k-cross's formula in other words.
- The stabilizer-rank reading rests on two web search summaries and memory; I did not open the papers.
- Section 7b's "exactly 4 at 8 points with arbitrary signs" stands on a hand case analysis of how three signed flats
  can cover and add up; the two runs inside it are exact, the list of cases is not machine-checked.
- Nothing here bears on the 1e-1 bar. The honest summary for the user: this idea, as a route to a circuit, is closed by
  the theorem (more pieces than the textbook has layers), and what survives is k-cross's rectangle count.

## What I would run next (one experiment)

**The flat rank of a H b over ALL sign vectors a, b at 16 points: 3 or 4?** (8 points is done: 4, section 7b.)
The case analysis of section 7b carries over word for word except for the bound (ii), which at k = 4 allows signed
constants on flats of dimension 6 of the 8-bit doubled space, so the partition cases reopen; `fr.c` mode `rs` runs
at K = 8 after replacing the 64-bit masks by 256-bit ones (417,199 subspaces; pairs of flats need the rented machine).
A 3 would be the first object of the night that needs a non-quadratic sign. A 4 would say: free signs halve the
number of bits once (from 2k to k) and do nothing more, and then the theorem's log2 N is the floor in every class
of this report. Then, and only then, the same question for the TOTAL RANK on two chains (section 6), which is gates.

Files: `waves/wave-09/ad-4-flatrank/` : fr.c (modes exh, ls, ls2, sym, sym2, rs),
verify.py, verify.out (exact replays, the spread, the dichotomy), dualcheck.py, dualcheck.out (Lemma B; k = 6 has no
spread), rescale.py, rescale.out, rs4.out, rs6.out, twoflat.py, twoflat.out (section 7b), kill.py, kill.out, price.py,
price.out, exh4.out,
ctl4_nb.out (control), ls4_r4.out, ls4_r3.out, ls6_r8_ctl.out, ls6_r8_more.out, ls6_r7_s11.out, ls6_r6_s12.out,
ls6_r7_unsigned.out, ls6_r8_unsigned_ctl.out, ls2_r8_unsigned_ctl.out (failed controls), sym4_p3.out, sym4_p2.out,
sym6_p5.out, sym6_p7.out, sym6_p3.out, sym2_4_p2_ctl.out, sym2_6_p3_part0.out, sym2_6_p3_part1.out,
sym2_6_p3_seed2_noinv.out, sym2_6_p3_part0of64.out (timing). The rented machine holds copies under
(the Linux machine's working folder)/ad-4-flatrank/ ; nothing is running there.
