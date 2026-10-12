# i-play: smallest cases, played with and stared at

Label i-play, 2026-10-10. Private notes. Marks: [read], [ran], [derived], [guess].
Scripts and outputs: `waves/wave-01/i-play/` (`n4.py`, `replay.py`, `f3.py`, `clebsch.py`; `n4full.out`, `n4sub.out`, `replay.out`, `f3.out`, `clebsch.out`). All runs exact integer or rational arithmetic, about 30 seconds in total. `f3.py` (under a second) was run directly, the others under `light.py`. The last line of `replay.out` is a failed first attempt at the 3-point identity with wrong scalings; `f3.out` is the corrected run.

Time: I overran the 35-minute box, by my estimate by 15 to 20 minutes.

Gate model used throughout: one gate computes a*u + b*v with any coefficients; scalings and permutations are free.

Not done: I did not open the literature for the "60-addition" circuit (no web read). The 60 in the brief is an agent's derivation, 2 x 22 + 16 [read: `wht37/avenues/k-realworld.md:134`]. The search at 8 and 16 points was not run: only the 4-point case is exhaustive. The derivations marked "sketch" were done by hand in this session and nobody has checked them.

## 1. What I saw

**1.1 The 16-point transform takes 56 gates, not 60.** [ran: `replay.py`]
- One block on four entries: s = x0 + x1 + x2 + x3 (3 gates), then y_i = s - 2 x_i (4 gates). That is the matrix J - 2I (all ones, minus twice the identity), 7 gates against 8.
- J - 2I is the 4-point Walsh-Hadamard matrix up to signs and one swap: exact certificate printed (permutation (0,2,1,3), signs (1,-1,-1,-1 | -1,1,1,1)).
- Used on every pair of digit columns: 8 points 22 gates (7/8 on one pair, plain on the third column), 16 points 56, 64 points 336. Each product was replayed exactly and is a matrix of +-1 with M M^T = n I.
- So the saving at 16 is one trick used at every level pair. It gives the constant 7/8 and never grows.

**1.2 Census at 4 points.** [ran: `n4.py full`, 26 s]
- No circuit with 6 gates. Output gates could use any rational coefficients (span test); helper gates used ratios from {+-1, +-2, +-1/2, +-3, +-1/3}. A hand argument covers all coefficients [derived, sketch].
- 228 distinct gate sets with 7 gates. Every one contains a helper with all four entries non-zero that is not an output. Helper supports are (2,2,4) in 36 sets and (2,3,4) in 192.
- The helper is always a sign vector with an odd number of minus signs, e.g. x0 - x1 + x2 + x3. Those are exactly the vectors at Hamming distance 1 from every row of the transform (up to sign).

**1.3 Pruned 4-point transforms.** [ran: `n4.py sub`, 3 s]

Cheapest gate count for a live inputs and m wanted outputs:

| live inputs a | m = 1 | m = 2 | m = 3 | m = 4 |
|---|---|---|---|---|
| 3 | 2 | 3 | 4 | 5 |
| 4 | 3 | 4 | 6 | 7 |

- Define excess = gates - (a - 1) - (m - 1): what a circuit costs beyond one tree in and one tree out.
- Excess is 0 for every sub-rectangle with 3 live inputs or at most 2 wanted outputs. It is 1 for 3 or 4 outputs of 4 inputs. The textbook has excess 2.
- The table obeys the transposition rule (4 outputs of 3 inputs: 5; 3 outputs of 4 inputs: 6 = 5 + 1). [ran + derived]
- The fourth output costs 1 once three are paid for; the third costs 2.

**1.4 The 3-point Fourier matrix is also rank one plus diagonal.** [ran: `f3.py`, exact in Z[w]]
- F3 - r c^T is diagonal with c = (w, 1, 1), r = (1, w^2, w^2). So 5 gates against 6.

**1.5 Ranks of the tensor powers of J - 2I.** [ran: `replay.py`]
- n = 4: rank(M + 2I) = 1. n = 16: rank(M - 4I) = 6. n = 64: rank(M + 8I) = 28.
- The small rank is (N - sqrt N)/2 = 1, 6, 28, 120, ...

## 2. Pretty facts and anomalies

- A1. (N - sqrt N)/2 = 1, 6, 28, 120, 496 is three things at once: the smaller eigenvalue multiplicity of the symmetric form [ran], the distance from a bent function to every Walsh function (covering radius of the first-order Reed-Muller code) [derived], and the number of points where a quadratic form on 2m bits is odd [derived]. It contains the perfect numbers 6, 28, 496. At N = 4 it equals 1, and that is the whole 4-point trick.
- A2. -(J - 2I) is the convolution by (-1)^(x1 x2 + x1 + x2). That form is the norm of the field with 4 elements: it is 1 at every non-zero point. The trick is the anisotropic plane. [derived]
- A3. 16 points: transform = 4x - 2(row sum) - 2(column sum) + total, on a 4 x 4 array. That is J - 2A for the rook's graph, and it equals (J - 2I) tensor (J - 2I) entry for entry. [ran: `clebsch.py`] Read naively it costs 63 gates; ordered as two passes it costs 56. The order of combining is worth 7 gates.
- A4. 16 points again: transform = total - 2x - 2(sum over 5 neighbours) in the folded 5-cube (Clebsch graph). It is a Hadamard matrix: M M^T = 16 I [ran: `clebsch.py`]. That it is the Walsh-Hadamard matrix up to free maps rests on its sign pattern being a quadratic form [derived, not run].
- A5. A complex Hadamard matrix that is rank one plus diagonal, up to free scalings and a permutation, exists only for N = 2, 3, 4. Row orthogonality gives (1 + d_i) + conj(1 + d_j) = -(N - 2) with both terms of modulus 1. [derived]
- A6. For 2^d entries, "identity minus twice the average over a block" is a multi-controlled phase gate in the Hadamard basis. For d >= 3 it is outside the Clifford group, and it costs under 2N gates whatever d is. [derived]
- A7. Weight digits: (-i)^|y| depends on the two lowest binary digits of the weight |y|, and those are the symmetric functions e1 and e2 mod 2. One wide reflection has phase (-1)^(e0 + e1 + ... + ed): it carries a full-rank quadratic part e2 plus higher terms to cancel. [derived]
- A8. Every optimal 4-point circuit funnels all four inputs through one form and adds four bypass wires. No optimal circuit is a butterfly network.

## 3. Ideas

**I1. Count wide factors, not butterflies.**
- Construction. A wide factor is a direct sum of blocks, each "diagonal plus rank one", on any partition of the N entries. It costs 2N minus the number of blocks, whatever the block size. Between factors any permutation and any diagonal is free. Let m(k) be the fewest wide factors whose product is the transform on 2^k points. Size is at most 2 m(k) N, so bounded m(k) is linear size.
- Seen. m(2) = 1 and m(4) = 2 are the 7 and the 56 [ran]. One factor works only for N <= 4 (A5). Two factors work only for N <= 16: two outputs in one block of the first factor differ by a combination of two rows of the second factor, so pairs of blocks of the second factor cover N/2 entries, and the same read from the other side [derived, sketch]. With three factors the same argument gives nothing, because the rows of a two-factor product are already dense [derived, sketch].
- Why it might live. The floor "k Hadamards under Clifford moves" does not cover these factors (A6). Rigidity only forces one factor to have at least N/(4m) blocks [derived from the Kashin-Razborov bound, recalled, not re-read].
- First sign of life. Three wide factors for 256 points (under 1,536 gates against 1,792), or three factors for 64 points that are not the 4 x 4 x 4 product.

**I2. The same game inside the convolution algebra, where it becomes a covering puzzle.**
- Construction. Up to free diagonal phases the transform is the convolution with spectrum (-i)^|y|. A factor "1 + c times the average over cosets of a subgroup" has spectrum 1 + c on an affine subspace U and 1 elsewhere. So: write the quadratic phase as a product of m such factors, that is, write a full-rank quadratic form on k bits as a sum mod 2 of m indicators of affine subspaces, plus a free linear term.
- Seen. k = 2: one subspace (a point). k/2 subspaces of codimension 2 always work. k = 6 with two subspaces fails on point counts (28 = 32 - 4 needs the form to vanish on a hyperplane; 16 + 16 - 4 needs dimension 7) [derived]. Spectral norms give 3^m >= 2^(k/2), so m >= 0.315 k in this commuting game [derived, sketch].
- Why it might live. Between 0.315 k and 0.5 k nothing is known to me, and m below 0.4375 k would beat the constant 7/8. The puzzle is finite and exact at k = 8: three affine subspaces of an 8-bit space whose indicators sum mod 2 to a rank-8 quadratic form plus linear.
- First sign of life. Any k with m(k) < k/2.
- What it taught. A commuting game has a floor linear in k; the free maps between factors must fail to commute with them. That is the same lesson as the engine's floor, reached from the other side.

**I3. The law of excess under tensor product.**
- Construction. excess(A tensor B) <= n_B excess(A) + n_A excess(B) + 2 (n_A - 1)(n_B - 1) [derived]. For two 2-point butterflies the last term is 2 and the truth is 1. Compute the true cross term for every pair of small excess-0 matrices (2 x 2 with 3 x 3, 3 x 3 with 3 x 3, the 3-in-4-out rectangle with a butterfly) with `n4.py` generalised.
- Why it might live. Linear size is exactly "excess O(N)". The cross term is the only place the log comes from, and at the smallest case it is already not what the product rule says.
- First sign of life. A pair where the cross term is below (n_A - 1)(n_B - 1), or a family where it grows like n_A + n_B.
- Tried. The 4-point table of section 1.3 only.

**I4. Rate-changing layers built from zero-excess rectangles.**
- Construction. 3 inputs to 4 outputs costs 5 gates (zero excess); 4 inputs to 2 outputs costs 4 (zero excess). Build the transform from layers that expand by 4/3 and layers that fold by 2, instead of square layers. This is "fan-out and fold" from the floor note with a concrete zero-excess brick.
- Why it might live. Every square 4-point brick pays excess 1; the rectangular ones pay 0, and the floor theorem was argued for square steps.
- First sign of life. A 12-to-16 or 8-to-8 word made only of zero-excess bricks with fewer than 22 gates at 8 points.
- Tried. Only the brick costs [ran].

**I5. A few shared helpers instead of one.**
- Construction. At 4 points one helper lies at distance 1 from all outputs. At 16 points a bent helper lies at distance 6 from all 32 signed outputs. Choose a small set of helper forms so that every output is one helper plus a bounded number of corrections, and ask the same of the helpers one level down.
- Seen. With one helper per level the corrections are (N - sqrt N)/2 per output. With helpers within distance below N/4 the helpers are distinct per output, so the helper matrix is "transform plus sparse" and must have lower rank to be easier; Kashin-Razborov says rank at least N/(4s) for s corrections per row [recalled].
- Mutation. Rank N/(4s) is linear, so the helper matrix must itself be computed recursively: factor it as fold, a transform on N/(4s) points, fan-out. For 16 points this gives T(N) = 5 T(N/4) + 7N/4, worse than the two-pass 4 T(N/4) + 7N/4 [derived]. The lesson of A3 again: the gain is in the order of combining.
- First sign of life. A helper family at 16 points where fold and fan-out are shared between helpers, bringing 5 T(N/4) to below 4.

**I6. Polar coordinates on the field with N elements.**
- Construction. In field coordinates the transform is the convolution by (-1)^Trace(Norm(x)) (A2 generalised) [derived, standard]. It commutes with multiplication by the norm-one group, cyclic of odd order sqrt N + 1. That is an address relabelling that mixes all digit columns, one of the escape hatches. Split the input by this group: sqrt N - 1 circles of sqrt N + 1 points plus the origin. The transform becomes, for each angular frequency, a sqrt N by sqrt N radial matrix whose entries are Kloosterman-type sums.
- Why it might live. At N = 4 there is one circle of 3 points and the radial matrix is 2 x 2: that is the 7-gate circuit. Nothing in the engine sees an odd-order symmetry.
- First sign of life. At N = 16 (three circles of five points): the 4 x 4 radial matrices being sparse, or rank one plus diagonal, for some angular frequency.
- Tried. Only the identification of the 5-point orbit with the Clebsch neighbours (A4).
- Cost to watch. The angular step needs fifth roots of unity, which the exact model may not give for free.

**I7. Is a pair of arrays cheaper than two singles?**
- Construction. Split every gate of a circuit for two arrays into its part on each array. A gate is paid twice only when both its operands mix the two arrays [derived]. So a pair can beat twice one only through gates fed by two mixed forms. Search directly: two 4-point arrays in 13 gates.
- Why it might live. A complex gate is such a doubly mixed gate with coupled coefficients; the real pair has more freedom than the complex single.
- First sign of life. 13 gates for two 4-point arrays, or 9 for two copies of the 3-in-4-out rectangle.
- Tried. The criterion only; depth 13 on 8 inputs was beyond the time box.

**I8. Transform, keep a subgroup of frequencies, transform back: linear already.**
- Construction. "Transform, keep the frequencies in a subgroup, transform back" is the average over cosets of the dual subgroup: under 2N gates for every subgroup [derived]. These projections are the wide factors of I2. Use non-commuting products of them with free diagonals between, as the only linear-size bricks that touch all columns at once.
- First sign of life. The 8-point transform as two such projections with one diagonal between, at any cost: existence first, since 8 is not a square and no symmetric form exists there.

**I9. Sparse inverse instead of circuit.**
- Construction. A circuit with s gates is the statement transform = C (I - L)^(-1) B with L strictly triangular, two entries per row [derived]. Drop "triangular": look for a sparse matrix on O(N) variables whose inverse contains the transform as a block and whose elimination has little fill. At 4 points it is the star on 5 vertices.
- Why it might live. Inverses of tree-like sparse matrices are dense and cost linear. The search space is graphs with weights, not words.
- First sign of life. At 16 points, a weighted graph on fewer than 56 edges-worth of unknowns with the transform as a block of its inverse.
- Tried. Nothing beyond the 4-point star, which all 228 optimal circuits share (A8).

**I10. Odd radix as a source of bricks.**
- Construction. The 3-point brick saves 1 in 6, the 4-point brick 1 in 8, and no larger single brick exists (A5). List every matrix on 5 to 8 points that is rank one plus diagonal on blocks after free maps, and ask which products of them are transforms of some group.
- First sign of life. A brick on 6 or 8 points with excess below the product rule that is not a tensor product of the 3- and 4-point bricks.

## 4. Which regularities will not go away

- Every saving seen is one form shared by all outputs of a block, plus one bypass per output. Excess 1 instead of 2.
- The brick stops at 4 points for a reason that is an equality: rank N/4 after N changes is the rigidity bound met exactly, and (N - sqrt N)/2 = 1.
- Wide factors cost 2N at any width. Two of them cannot pass 16 points; nothing I derived limits three.
- Commuting families of wide factors have a floor linear in k. Any gain must come from free maps that do not commute with the factors.
