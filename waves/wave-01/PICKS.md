# wht39 / ideas / PICKS: eight ideas to develop for an hour each

Curator: i-pick, 2026-10-10. Private research; nothing here is reviewed and nothing is in Lean.

Source: the eight generator reports `i-hatch.md`, `i-represent.md`, `i-cousins.md`, `i-backwards.md`,
`i-play.md`, `i-fields.md`, `i-model.md`, `i-wild.md` in this folder (77 ideas, 105 anomalies).
Idea numbers below are the numbers in the combined list (0 to 76).

How the eight were chosen: for surprise, for something that was actually seen behind the idea,
for a first experiment that fits an hour on small exact cases, and for variety. Not by odds.
Nothing was dropped for "must be known" or "must be impossible". Every idea not picked is listed
at the end by title.

Tags: [read] [ran] [derived] [guess] are the generators' own unless I say "mine".

## Notes for all eight developers

- Generation and play first, criticism last. A [guess] is welcome as long as it is marked.
- Instrument: `python3 -B (not in this repository) wht35/bin/light.py <label> <max seconds, at most 600> <command...>`.
  Exact rational or Gaussian-rational arithmetic, or modulo large primes with the reason why that suffices.
  A circuit found modulo a prime is only a candidate until it is lifted and replayed exactly;
  "none found modulo p" is not "none exists" unless argued.
- Say which count you use every time you quote a number of gates. Two are in play:
  (G) a gate is any a*u + b*v, scalings free: 4 points cost 7, 16 points 56;
  (O) OpenAI's count, additions and scalar multiplications each charged: 4 points cost 8, 16 points 64.
- Files go under `waves/<your label>/` and `<your label>.md`.
- No git, no Lean, publish nothing. The release tree is read only.

Generators represented: all eight. Picks most people would call unlikely: 2 (plane), 4 (mod 4), 6 (border).

---

## Pick 1. `zeta`: subset sums with subtraction, the transform with its determinant taken out

From: hatch 3, cousins 23, backwards 30, fields 51 (one thought found four times independently).
Attached: cousins 24, represent 19, backwards 37 (the cube's neighbour sum, the easier sibling); the four-transform word from wild 70.

**The idea.** With Z the subset-sum matrix (the k-th tensor power of [[1,0],[1,1]]), the transform is
H = Z * diag((-2)^|T|) * Z-transpose. All of Morgenstern's (N/2) log2 N bits of determinant sit in one layer of N scalings.
What is left is a 0/1 triangular matrix of determinant 1. In the other direction Z is a word of four transforms and four
diagonals, so a linear program for one is a linear program for the other, up to a constant. So stop attacking H. Attack Z,
a combinatorial object with an order, a Moebius inverse, chain decompositions, and a community (subset convolution,
lattices with few irreducibles, range sums in the group model) that has never met this problem. Every gain on Z must come
from subtraction, and with subtraction no superlinear lower bound is known to the generators [guess, from memory].
Z = exp(L) with L the "remove one element" operator of the cube, and the cube's neighbour sum is A = L + L-transpose:
Z, A and H live in one small algebra, and A is strictly easier than H (A = H D H / n).

**What was seen.**
- [ran] H = Z D Z^T exact for k = 1..6; H * Z^T = Z^T * (complement relabelling x 2^|S|) exact for k = 1..6 (`i-hatch/play.out`; also `i-backwards/play1.py` section B, `i-cousins/play1.py`).
- [ran] [[1,0],[1,1]] = diag(-1/15,-1/6) H2 diag(3/2,-1/2) H2 diag(1,2) H2 diag(-3/2,5/2) H2 exactly (`i-wild/zeta16.py`).
- [ran] Leftover volume of Z is 0.277*sqrt(k) bits per entry for k = 4 to 4096, against k/2 for H.
- [derived] A triangular matrix has entropy potential exactly 0: in H = Z D Z^T all n log n bits arrive in the last third of the program.
- [ran, `i-cousins/play1.py`, `play2.py`] Exhaustive at 4 points over GF(5): zeta 4 gates, Hadamard 7. Greedy at 8 points over GF(7), 1,905 tries: never below 12 (weak). These two scripts are the seed of the search to build.
- [ran / by hand] The neighbour sum costs 2 gates, not 4, at 4 points (rank 2); 14, not 16, on the 3-cube by hand.

**First experiment.** Build one exact minimum-circuit search (count G; meet in the middle or iterative deepening over a small
prime field, candidates lifted and replayed over the rationals) and point it at three targets in this order:
the 8-point zeta (is 11 possible; the standard method gives 12), the 3-cube neighbour sum (below 12), and then the 16-point
zeta (below 32) with whatever pruning the 8-point answer suggests. Second, by hand and then by machine: take the
symmetric chain decomposition of the 4-cube (6 chains), do prefix sums along chains, and write down exactly what
correction is left to reach Z; count it.

**Question to keep asking.** What can subtraction do for Z that sums alone cannot: where in the Boolean lattice is there a large
shared sum that two outputs want with opposite signs? If the 8-point minimum is 12, what forces it, in words, without
using a determinant?

---

## Pick 2. `plane`: all line sums of a finite plane, a concrete target of N log log N  (unlikely)

From: model 58. Attached: play 45 (polar coordinates on the same field), anomaly "H = 2R - J, R the point-hyperplane incidence matrix".

**The idea.** Take N = q^2, q = 2^m, and read the addresses as the plane over the field with q elements. The plane has q + 1
directions. They split the non-zero frequencies into q + 1 classes, and the transform restricted to one class is just the
length-q transform of the q sums of the data over the parallel lines of that direction (the slice theorem). So
T(N) <= Rad(sqrt N) + (sqrt N + 1) T(sqrt N), where Rad is the cost of all N + sqrt N line sums, and the converse holds
too. If all line sums can be had in O(N) operations, the cost per entry obeys t(N) = t(sqrt N) + O(1): N log log N.
The folds are along directions that are column-mixing relabellings (multiplication by a field element), so every cheap
step moves every pair's diagonal, which is what the floor theorem says a faster program must do. The same field gives a
second coordinate system: the norm-one group (cyclic, odd order sqrt N + 1) cuts the plane into the origin and
sqrt N - 1 circles, and the transform commutes with rotating them.

**What was seen.**
- [ran, exact, `i-model/play4.py`] Fold onto the lines of each direction, run q + 1 small transforms, compare with the textbook
  transform at lengths 4, 16, 64, 256: equal every time. The folds are exactly the 6, 20, 72, 272 lines of the plane.
- Naive fold counts 6, 60, 504, 4080 against the textbook's 8, 64, 384, 2048.
- [ran, `i-play/clebsch.py`] At 16 points "total - 2x - 2(sum over the 5 points of the norm-one orbit of x)" is a Hadamard
  matrix; at 4 points the single circle of 3 points is exactly the 7-gate circuit. The 5-point orbit is the
  neighbourhood in the folded 5-cube, which the script calls the Clebsch form. [recalled, mine, unchecked] The Clebsch
  graph is also the Cayley graph of the non-zero cubes in the 16-element field, which would tie it to the norm-one group.

**First experiment.** The 16-point plane: 5 directions, 4 lines each, 4 points per line, two lines of different directions
meet in exactly one point. Write the 20 x 16 incidence matrix, compute its rank and all linear relations among the
20 line sums exactly, then search for a circuit with subtraction that produces all 20 in 59 or fewer operations (count G
and count O both). Start from structure, not from brute force: two directions are the row and column sums of a 4 x 4
table, the other three are the three mutually orthogonal Latin squares of order 4. Then the same question at 64 points
(72 lines, under 504). In parallel, compute the 4 x 4 radial matrices of idea 45 for each angular frequency at N = 16 and
look at them. Twenty minutes on the literature of the finite (discrete periodic) Radon transform and its fast
algorithms, with dates.

**Question to keep asking.** Do two directions share any work beyond the grand total? In which coordinates do the q + 1
folds become one fold plus relabellings? What is the exact cost of Rad at the smallest sizes, as a sequence?

---

## Pick 3. `letters`: count letters, not butterflies: short non-commuting words in dense linear-cost steps

From: hatch 2, represent 10, play 40, cousins 27, play 47 (one thought: letters that cost O(N) at any width, with free maps between).
Attached as "what the commuting game already told us": hatch 0, play 41, cousins 28; as material: cousins 20, 21, 22.

**The idea.** A letter is any step that costs O(N) however wide it is: "identity minus c times the average over a block",
on the cosets of a subgroup D that may span bits of several digit columns or on any partition of the addresses; more
generally any operator diagonal in the Haar basis of a flag of subgroups (block sums up a tree, one gate per block on the
way down). Relabellings and position-diagonal scalings are free. Let m(k) be the fewest letters whose product is the
2^k-point transform. Bounded m(k) is linear size. If the letters commute the game is closed: the exhaustive search and
two counting arguments give about k/2, because commuting factors may as well be unitary and a unitary flag step is local.
So drop commutativity: put non-scalar diagonals and relabellings between the letters, and let the factors be badly
conditioned while the product stays unitary.

**What was seen.**
- [ran, exact] 4 points is ONE letter (I - J/2, 7 gates); 16 points is two letters (56); 64 points 336.
- [ran] I - J/2 on 8 and on 16 points is still flat (all entries of equal size) and invertible: it loses orthogonality, not flatness.
- [derived] For |D| of 8 or more the letter is outside the Clifford group, so "one array needs k Hadamards" does not speak about it.
- [ran, floats] Bits of spread per gate: butterfly 1.000, 4-point reflection 1.143, 8-point 1.182, 6-point 1.244 (the peak).
- [ran, exhaustive, `i-hatch/flags.py`, `flags5.py`] Least number of commuting flag steps: 1, 2, 2, 3 at k = 2, 3, 4, 5.
- [derived] Two-factor necessary condition: the matrix of H between two many-scale bases must equal their overlap matrix up to row and column scalings.
- [derived] The only bound found for non-commuting words is by rank: a constant.

**First experiment.** 8 points, which is not a square, so no symmetric form exists there. For every pair of flags (or trees)
T, T', solve exactly for diagonals D0, D1, D2 in D0 * T * D1 * T' * D2 = (monomial) * H_8, using the two-factor condition
to prune. The sign is one solution whose middle diagonal is not a scalar. Then 16 points: words of at most three letters
with |D| in {4, 8, 16}, D spanning both columns, that are not the product of two 4-point reflections. Then 32 points with
two flag steps, where the commuting class needs three.

**Question to keep asking.** What does a non-commuting letter do that a butterfly cannot: what quantity does it raise by more than
a constant per gate? And what is the true lower bound on m(k) once diagonals sit in between, since rank gives only a constant?

---

## Pick 4. `mod4`: use what only the transform's own point has  (unlikely)

From: hatch 1, wild 69, wild 74. Attached: hatch 0 (the data), represent 18.

**The idea.** Every construction so far, and the floor theorem itself, uses the tensor-power structure. The whole family K_t
(entries t^distance) shares that structure, so none of it can be what makes the transform special. The transform is
one point of the family, t = -i, and there i^4 = 1: the Hamming weight only matters modulo 4. Up to free phases the
transform is the splitting of the Walsh basis by weight modulo 4. The coarser splitting modulo 2 is free (it is the
complement relabelling), and modulo 2 the matrix itself is all ones: rank one, cost N. So the whole n log n is the price
of ONE binary digit, the second digit of the weight, a quadratic sign on the frequency side. Look for identities that
exist only at this point and build with those.

**What was seen.**
- [ran, `i-hatch/flags.out`] Of the 54 two-flag identities at 16 points, 27 are exact for the whole family and 27 hold only modulo 4,
  that is only at t = +-i. Example: 0 < {e1+e3} < span(e1,e3) < {y0=y2} with 0 < {e0} < span(e0,e2) < {y1=y3}.
  Each uses all four levels and neither is a tensor product of smaller programs.
- [ran, `i-wild/grow16.py`] H = D K D with D = diag(i^weight); K = (1-i)^k sum_j i^j E_j; sum_j (-1)^j E_j is the complement relabelling.
- [derived] OpenAI's 2x2 matrix C squares to the bit flip, so its tensor power is a square root of a free relabelling;
  a second square root of the same relabelling costs O(N); the two differ by one involution R, +1 on weights 0, 3 mod 4, -1 on 1, 2.
- [ran] The all-ones matrix already equals the transform on 53 % of entries at N = 16 and 51 % at N = 64.

**First experiment.** Print the 27 modulo-4-only identities, sort them by symmetry and by which levels each flag uses, and find
the rule that generates them (27 = 3 x 3 x 3 on the exact side: is there a matching count on this side?). Then test the
rule at 64 points: do not enumerate pairs of flags (there are about 10^11), grow candidates from the 16-point ones and
search near them for an identity that is not built from 16-point pieces. Third, if time: for a kernel on m-bit digits,
as in the published unit, what replaces "modulo 4"?

**Question to keep asking.** What does t = -i have that a generic t lacks, written as an identity small enough to be used as a brick?
What does the second binary digit of a weight cost when the first is free?

---

## Pick 5. `codes`: walk through self-dual codes, and atoms from several codes at once (the E8 door)

From: hatch 4, represent 15, backwards 35, fields 55, model 62. Attached: wild 73, backwards 36.

**The idea.** The floor theorem's witness, "the data on which two digit columns agree", is the indicator of the self-dual code
{(u,u)}. For ANY self-dual code C the functions (character) x (indicator of a coset of C) form a basis in which the
transform is a signed transposition times sqrt(N), and the kernel (-i)^distance has rank one on every pair of cosets. So
what the floor theorem really uses is: every cheap step of the engine keeps one self-dual code. The positive form of
"move every pair's diagonal" is then a program whose steps keep no single code: a walk through several self-dual codes
that share half their words, or, since fan-out is free in the model, an overcomplete set of atoms taken from several
codes at once on which the transform is a relabelling (transform = synthesis x monomial x analysis; a one-sided version
would give t(n) = t(sqrt n) + O(1)). And [guess] this is why the E8 family worked where nothing said it should:
E8 sits on the length-8 Hamming code, the next self-dual code after the diagonal.

**What was seen.**
- [ran, `i-backwards/play1.py` section D] H g(a,b) = +-4 g(b,a) for all 16 pairs, for the diagonal code and for {0000,1100,0011,1111}.
- [ran, `i-backwards/play1.py` section C, `play2.py`] The 12 minimal-support eigenvectors of H16 are exactly the coset states of the three self-dual codes of length 4; they span 6 of 16 dimensions.
- [ran, `i-hatch/codes.out`] H 1_C = sqrt(N) 1_C for the diagonal at 16 and 64 points and for the extended Hamming code at 256.
- [ran, `i-represent/play.py`] All 256 coset-pair blocks have rank one for the Hamming code at k = 8, and for the code made of four pairs.
- [ran] Bell basis: the 4-point transform is a signed permutation times 2. Zak basis: the cyclic Fourier transform of length m^2 is monomial, lengths 4 to 36.
- [derived] Staying in one code costs the textbook exactly: t(k) <= 2 t(j) + t(k - 2j).

**First experiment.** N = 16. The three self-dual codes of length 4 give three bases of 16 atoms, 48 atoms in all. Compute exactly
(a) the three 16 x 16 transfer matrices between the bases: non-zeros per row, block shape, are they monomial times small
blocks; (b) the action of H on the 48 atoms as a signed permutation, and the cheapest analysis and synthesis pair for a
closed subset of at most 32 atoms (count G, target under 56). Then N = 256 with the Hamming code: its automorphism group
acts on the 16 cosets; are two cosets' 16-point coset transforms one call and a relabelling?

**Question to keep asking.** Read the published E8 unit in this language: which self-dual code does each of its cheap steps keep,
and does any step change the code? If one does, that is the mechanism, and it should be done on purpose.

---

## Pick 6. `border`: spend the model's unused power: huge coefficients, limits, and families through the target  (unlikely)

From: fields 57, model 59, wild 76, hatch 7. Attached: hatch 9.

**The idea.** The cost model prices an exact complex number of any size at one unit and asks nothing about stability. Every
program so far, OpenAI's and the published one, uses coefficients of size at most 1, which is exactly the regime where
n log n is believed to be forced. The set of matrices with s-gate programs is not closed: a family of cheap programs
H(e) = H + e^p E can converge to a matrix that needs more gates, and then a fixed number of evaluations combined
recover H exactly. That is the border-rank trick, the source of every matrix-multiplication exponent since 1980.
The transform sits on ready-made families: G(u) = sum_j u^j E_j has degree k, is free or O(N) at u = 0, +-1, infinity
with cheap first derivatives there, and the target is u = i; and the transform is a product of two members of K_t each
exponentially close to rank one. A linear program needs about log n bits per gate; nothing known forbids that once
conditioning is given up.

**What was seen.**
- [read] `R/OAI` RAM.lean and Goal.lean: no bound on complex values, only on integers. OpenAI's tensor step uses only (1+-i)/2, +-1/2, +-1.
- [ran, floats, random search, `i-hatch/play.py` and `play.out`, the entropy part] Signed row entropy: 8 gates on 3 wires with coefficients +-1 reach 22.8 bits
  (orthogonal maximum 4.75); 4 gates on 3 wires with coefficients up to 64 reach 826 bits; 4 gates on 4 wires reach 6,345 bits.
- [derived] The determinant bound is 0 for the unitary transform. The swap is a limit of lower-times-upper products and is not one.
- [ran + derived, `i-cousins/play1.py`, `play2.py`, `i-play/n4.py`] At 4 points 7 gates is the exact minimum found (no 6-gate circuit over GF(5), GF(7), GF(11), GF(13); hand sketch for all coefficients).

**First experiment.** The smallest border question, exactly: is there a one-parameter family of 6-gate programs (count G) whose
matrix is (monomial) x H_4 + O(e)? Enumerate the 6-gate shapes, give each coefficient the form c * e^m with small integer
m, and solve order by order in e. Do the same for the 3-point Fourier matrix with 4 gates (exact minimum 5). If either
border count is below the exact count, count what exactness then costs: how many values of e, and how many gates the
evaluations share. Second: G(u) at k = 4, is there any u other than 0, +-1, infinity and the fourth roots of unity where
G(u) costs fewer than 32 gates, and what do the jets at the cheap points determine?

**Question to keep asking.** Is there any matrix family at all in this gate model whose border count is below its exact count
with evaluations that share most of their gates? One example, of any matrix, is the door.

---

## Pick 7. `excess`: where the log is born: the cross term of a tensor product, rectangular bricks, two copies at once

From: play 42, play 43. Attached: cousins 25 and play 46 (direct sum at the smallest size), cousins 29, play 44, play 48.

**The idea.** Define excess = gates - (inputs - 1) - (outputs - 1): what a circuit costs beyond one tree in and one tree out.
Linear size is exactly "excess O(N)". Under tensor product the product rule gives
excess(A x B) <= n_B excess(A) + n_A excess(B) + 2 (n_A - 1)(n_B - 1), and that last cross term is the only place the log
comes from. At the smallest case it is already wrong: for two butterflies the rule says 2 and the truth is 1.
Rectangular bricks are cheaper still: 3 inputs to 4 outputs in 5 gates and 4 inputs to 2 outputs in 4 gates have excess
zero, while every square 4-point brick pays 1. So measure the cross term exactly on small pairs and look for a pair or a
family where it grows like n_A + n_B. The same instrument answers the direct-sum question nobody has tested at tiny
size: are two copies of the 4-point transform cheaper than twice one?

**What was seen.**
- [ran, exhaustive, `i-play/n4.py`, `n4full.out`, `n4sub.out`] 4-point table: excess 0 for every sub-rectangle with 3 live inputs or at
  most 2 wanted outputs; excess 1 for 3 or 4 outputs of 4 inputs; the textbook has excess 2. The table obeys the transposition rule (5 gates one way, 6 the other).
- [ran] The fourth output of a 4-point block costs 1 gate once three are paid for; the third costs 2.
- [ran] All 228 optimal 4-point gate sets have one full-support helper that is not an output: a star on 5 vertices.
- [ran, `i-play/f3.py`] The 3-point Fourier matrix is rank one plus diagonal: 5 gates against 6.
- [derived] A pair of arrays can beat twice one only through gates whose two operands both mix the arrays. Two copies of the 4-point zeta cannot share a gate.
- [derived, twice, the hard way, hatch 5] "Per-entry cost adds over tensor factors: that additivity, not the transform, is the thing to beat."

**First experiment.** Generalise `n4.py` to rectangular targets on up to 6 or 8 wires and compute the exact minimum for
A x B for every pair of small bricks with known cost: butterfly with the 3-point Fourier brick, 3-point with 3-point,
the 3-in-4-out rectangle with a butterfly. Tabulate true cross term against (n_A - 1)(n_B - 1). Then two searches with a
gate budget: two 4-point arrays in 13 gates, two 3-in-4-out rectangles in 9. Then an 8-point word made only of
zero-excess bricks under 22 gates.

**Question to keep asking.** Which pairs have a cross term below the product rule, and what exactly is shared when they do?
Is there a brick whose excess under repeated product stays proportional to its perimeter rather than its area?

---

## Pick 8. `spin`: the cheapest symmetry-adapted basis: all of n log n in one kernel-free basis change

From: hatch 5, represent 14, cousins 26, fields 52, wild 71 (found five times; the square root of log N would not go away).

**The idea.** The transform commutes with permuting the k bit positions. In any basis adapted to that symmetry (total spin,
Schur-Weyl) every 2x2 tensor power is a direct sum of blocks of size k - 2j + 1, typically about sqrt(k). Applied densely
the blocks cost 1.6 sqrt(k) per entry; with a fast block algorithm, half of log2 k. So the transform itself is nearly
free there, and the whole n log n has moved into one basis change that does not depend on which kernel is applied, keeps
the Hamming weight of addresses, is real, and is far from unique: any invertible change inside each multiplicity space
is allowed, or one can adapt only to a subgroup of the permutations. The textbook coupling bases were designed for
physics. Nobody has asked which symmetry-adapted basis is cheapest as a circuit. A linear-size basis change would give
N sqrt(log N), a saving of 5e-1; N (log N)^0.9 already gives 1e-1. Second half of the same thought: on the antisymmetric
part of two bits the transform is the plain number -2, and that part is zero on the floor theorem's diagonal inputs, so
blocks placed only on antisymmetric halves weigh nothing in the floor's potential: a concrete carrier for the hatch
"blocks only on known zeros", which the floor note lists as having no program.

**What was seen.**
- [ran, by formula] Dense middle cost per entry 3.38, 6.48, 12.82, 25.56, 51.08 at k = 4, 16, 64, 256, 1024 (textbook k);
  with a fast block transform 2.08, 2.55, 3.04, 3.53, 4.03 at k = 8 to 128.
- [ran] H x H maps e01 - e10 to -2 times itself.
- [by hand] Two bits through singlet and triplet: 2 + 4 + 2 = 8, exactly the textbook's 8. Standard pairwise coupling ties at 4 points and loses at 16 (about 72 against 64).
- [ran counts, read] sqrt(k) turns up four times from unrelated counts: the block size here, the width of the overlap window in the
  truncated subset-sum form, the leftover volume of Z (0.277 sqrt(k) bits per entry), and the ceiling 1/2 of OpenAI's generic amplification.
- No basis was built in code by any of the five generators.

**First experiment.** k = 4, 16 points: blocks of size 5, 3, 1 with multiplicities 1, 3, 2; the basis change is block diagonal
on the weight layers (sizes 1, 4, 6, 4, 1). Build one symmetry-adapted basis exactly, then search the freedom inside the
multiplicity spaces (GL(3) x GL(2) and the scalings) for the cheapest circuit in and out, target: in + middle + out under
64 (count O) or 56 (count G). Then k = 6 adapted only to permutations within two groups of 3 bits: under 96 additions
each way. If time, the engine variant: a two-column unit whose blocks sit only on antisymmetric halves, counted against the floor's count.

**Question to keep asking.** Is the cost of the weight-preserving basis change really additive over tensor factors, or is that only
how everyone built it? What is the cheapest circuit for "split one weight layer by symmetry type", a question about
subset-inclusion maps and designs? And why does sqrt(log N) appear four times?

---

## Everything else, by title (nothing is thrown away)

Ideas attached to a pick as material are marked with the pick. The rest are free to be picked up next.
Three groups I would open first if a ninth hour appears, chosen for the same reasons and not by odds:
the information-set and output-density group (66, 67, 68 with 12, 31, 33, 56, 60), the cut-off subset-sum form (39, 70),
and the new dense letters that are not reflections (50, 38, 72).

From hatch:
- 0. Flag steps: a cheap step with a dense kernel at every scale, which is not a butterfly (material for picks 3 and 4)
- 6. Monomial plus nested remainder (from 'monomial plus low rank')
- 8. The tiling theorem: the nearest problem with an honest n log n proof, used as a map
- 9. Two factors, each almost of rank one (material for pick 6)

From represent:
- 11. Rows near a common centre: 4-point transform in 7 additions, with scaling debt carried to the end
- 12. The transform is matrix transpose in the right basis
- 13. V-cycle through a Gram inverse, with dense-but-cheap frames
- 16. Change the metric: exponential kernels with sparse inverse
- 17. The chirp as a short product of sums of coset indicators
- 18. Apply one projector of rank N/4 instead of the transform (material for pick 4)
- 19. The cube's adjacency matrix as a stepping stone (material for pick 1)

From cousins:
- 20. Grover-diffusion Kronecker family: a unitary cousin that is linear (material for pick 3)
- 21. Householder depth of H_n: how few reflection layers (material for pick 3)
- 22. Bits per gate: entropy as the currency, cancelling giants as the only way past O(1) (material for picks 3 and 6)
- 24. Cube neighbour sums: the nearest unsolved easier problem (material for pick 1)
- 25. Direct sum as the hinge: one fixed matrix times an arbitrary matrix (material for pick 7)
- 28. Sparse stencil layers are provably the textbook (material for pick 3)
- 29. Rank-deficient neighbours of the Hadamard block (material for pick 7)

From backwards:
- 31. Carry eigenforms: look for a cheap eigenbasis
- 32. Relabel first: a reflection through a smaller space
- 33. Fill 'identity plus one projection' at 16 points
- 34. A half-dimensional space with sparse checks on which the transform is sparse
- 36. Count passes: z = log2(passes per squaring) (material for pick 5)
- 37. One generator, and the nearest problem I can solve (material for pick 1)
- 38. Unbalanced steps: differences and prefix sums as free changes of basis
- 39. Valiant backwards: cut the diagonal and recurse on heavy addresses

From play:
- 41. The covering puzzle inside the convolution algebra (material for pick 3)
- 44. A few shared helpers instead of one (material for pick 7)
- 45. Polar coordinates on the field with N elements (material for pick 2)
- 46. Is a pair of arrays cheaper than two singles (material for pick 7)
- 48. Sparse inverse instead of circuit (material for pick 7)
- 49. Odd radix as a source of bricks

From fields:
- 50. Pay in running sums, not butterflies (summed-area tables, lifting scheme)
- 53. Fast multipole and butterfly: push the kernel into the short-range regime
- 54. The transform is 'conjugate a matrix by H': Strassen tuned to a known factor
- 56. The V-cycle read backwards: invariant planes span{x, Hx}

From model:
- 60. The transform is a transpose in disguise: Grover form, chain instead of lattice
- 61. A short sum of cheap tensor products
- 63. A linear exact transform inside OpenAI's own machine, for data in a fixed finite ring
- 64. The outrageous program, written where it is allowed: one remainder per output
- 65. Pointer trees: relabelling at geometric cost, zeros for free

From wild:
- 66. The eigenspace as a code: transform only an information set
- 67. Bent relabelling: the transform is a free signed relabelling minus a matrix of rank (N - sqrt N)/2
- 68. The exponent is a density of outputs
- 70. A cheap wrong answer that is exact on most of the matrix (and: the transform is the subset-sum transform)
- 72. A new cheap letter: the resolvent of a relabelling
- 73. The linear recursion read backwards: column-transform a signed-symmetric array (material for pick 5)
- 75. (silly) Transform N shifted copies at once and read the diagonal

Ideas inside the picks: 3, 23, 30, 51 (pick 1); 58 (pick 2); 2, 10, 27, 40, 47 (pick 3); 1, 69, 74 (pick 4);
4, 15, 35, 55, 62 (pick 5); 7, 57, 59, 76 (pick 6); 42, 43 (pick 7); 5, 14, 26, 52, 71 (pick 8).
That is 29 inside and 48 listed above: 77.

Anomalies that no pick carries yet and that would not go away while I read:
- 64 additions came back in every count at 16 points (textbook, eigenspace encoder, bent encoder 28 + 20 + 16), and every
  reorganisation in OpenAI's count lands on exactly the textbook, never below: "something is conserved" [model, wild]. Nobody has said what.
- (N - sqrt N)/2 = 1, 6, 28, 120, 496 is at once an eigenvalue multiplicity, the distance from a bent function to every Walsh function,
  and the count of odd points of a quadratic form [play].
- In the bent form the encoder sizes over all 4,048 information sets take only four values: 30, 34, 39, 60 [wild].
- The Hankel matrix of one period of the maximal-length sequence is one short of full rank at k = 6 only [wild].
