# i-represent: the transform in other languages, and what each one suggests

10 October 2026, late evening. Private. One agent, 35 minutes, generation first. Nothing here is reviewed, nothing is in Lean.
Labels: [ran] = computed exactly in `i-represent/play.py` (output `i-represent/play.out`, 1 second); [derived] = worked by hand here, not machine-checked; [read] = from the notes named in the task; [guess] = unsupported.

Words. N = 2^k points. H: the plain ±1 transform. U: the unitary form, entries ((1+i)/2)^k · (−i)^(Hamming distance); U equals H up to free diagonal phases [read]. P: the antipodal map z → complement of z (a free relabelling). J: the all-ones matrix. *Coset sum over D*: replace every entry by the sum over its coset of a subgroup D of the address group.

What was NOT done: no search was run at 16 or 64 points. The 16- and 64-point work is the exact identities in sections 1 to 4 (k = 2, 4, 6, 8) and a block-size table up to k = 256. Every idea below stops at "first thing to run".

## 0. Three facts that reorganised my picture

**F1. The transform generates an algebra of dimension four.** [derived] U has eigenvalue i^j on Fourier level j, so U⁴ = I and U² = (scalar) · P. Everything computable from U by sums and products is a·I + b·P + c·U + d·U⁻¹. So no "function of the transform" is sparse except a·I + b·P. This kills every plan of the form "write U as a rational function of something sparse built from U" (Cayley transform, resolvent), and it says exactly which matrices are as good as U: any a·I + b·P + c·U + d·U⁻¹ with the pair (c, d) non-degenerate.

**F2. One of those is a real, flat, symmetric reflection whose entries depend only on distance mod 4.** [ran, k = 4 and 6] U = R·Q, where R mixes each antipodal pair (cost O(N)) and Q = ±1/√N everywhere, Q² = I, with sign pattern by distance (−,+,+,−,−) at k = 4 and (−,−,+,+,−,−,+) at k = 6: period 4, two of each sign. So the problem is the kernel sum output(y) = Σ_z s(distance(y,z)) x(z) with s = ++−−++−−…
The trace of Q is −√N exactly [ran: −4, −8]. So the two eigenspaces have dimensions (N+√N)/2 and (N−√N)/2, not N/2 and N/2. Those are the dimensions of symmetric and antisymmetric n×n matrices, n = √N.

**F3. Coset sums cost less than N additions for ANY subgroup, and for 8 or more elements they are outside the Clifford group.** [derived] The operator G = I − (c/|D|)·(coset sum over D, possibly sign-twisted) costs at most 2N additions whatever the size of D. For |D| = 4 and c = 2 it is a Clifford element; for |D| ≥ 8 it is a reflection about a code of codimension ≥ 3, the same kind of object as a multiply-controlled sign flip. The count "one array needs k Hadamards" [read] is a count inside the Clifford group. It does not cover words in these letters.

## 1. Ideas

### Idea 1. Words in coset reflections (one array, no scratch, not Clifford)
Letters: free relabellings and scalings, and G(D, signs, c) = I − (c/|D|)·(twisted coset sum over D), D any subgroup of the address group, including D spanning bits of several digit columns. Each letter costs ≤ 2N. Ask for the shortest word equal to H up to free relabelling and scaling. A word of bounded length at every N is a linear-size program.
- Tried: H_4 is ONE letter: I − J/2 on four points is ±1/2 everywhere and squares to I [ran]. That gives a 7-addition 4-point transform (idea 2). I − J/2 on 8 and on 16 points is still flat (all entries ±1/2) and invertible (eigenvalues 1 and −3, resp. −7) [ran]: flatness is not what stops a short word once c is not the unitary value.
- Tried: how fast one letter spreads a basis vector, per addition spent (the quantity behind Ailon's bound for rotations [read]): |D| = 4: 1.143 bits per addition; |D| = 8: 1.182; |D| = 16: 0.878; textbook butterfly 1.000 [ran]. The 8-point reflection is the best letter per addition, and it is the first non-Clifford one.
- What rank allows [derived]: for a unitary-scaled monomial M, rank(H − M) ≥ (N − √N)/2 (trace argument). A letter adds rank N/|D|. So a word over |D| = 8 needs at least 4 letters by rank, and nothing I know asks for more than a bounded number.
- Why it touches the floor theorem: a letter with D spanning two digit columns moves that pair's diagonal. It is hatch (a)/(b) of the floor note with a concrete alphabet.
- First thing to run: at 16 points, all words of ≤ 3 letters with |D| ∈ {4, 8, 16}, general c, signed permutations between, tested for "equals a scaled-monomial image of H_16"; then 64 points with ≤ 4 letters.

### Idea 2. Rows near a common centre: the 4-point transform in 7 additions, and "scaling debt"
The three non-constant rows of H_4 each differ from (1,−1,−1,−1) in one place. So: s = x1+x2+x3; y0 = x0+s; w = x0−s; y_j = w + 2x_j. Seven gates if a gate is a·u + b·v [ran: equals H_4 on 1,296 integer inputs].
- In OpenAI's count (a scalar multiplication costs 1) it is 7 additions + 1 multiplication = 8, a tie with the textbook: compute w/2 once and emit (y0, y1/2, y2/2, y3/2). That uneven output scale is a *debt* that commutes with every later pass on other digits, so it is paid once at the end, O(N) in total [derived].
- In the gate count with free scalars it gives (7/8)·N·log2 N by repetition, and 56 gates at 16 points. The task quotes "60 additions known at 16 points"; I did not check which count that figure uses. If it is the free-scalar count, 56 is below it. [guess that this is not already known; unchecked]
- What it teaches: the saving comes from "low rank + monomial" (I − J/2), i.e. the transform is as non-rigid as possible at one rank. Yes-and: carry uneven scaling debts through a whole program so that NO pass pays a multiplication; in OpenAI's count that turns every tie of this kind into a win.
- First thing to run: the cheapest 16-point program in OpenAI's count when output debts are allowed (any diagonal), by exhaustive search over programs of ≤ 60 operations built from coset sums and corrections.

### Idea 3. The transform is "transpose" in the right basis (a sixth language)
For N = n², −Q has the spectrum of the map X → Xᵀ on n×n matrices: +1 on a space of dimension n(n+1)/2, −1 on n(n−1)/2 [ran for the trace; derived for the rest]. Transpose is a free relabelling. So H = V⁻¹·(transpose)·V, and ALL the cost is in the intertwiner V, which is free up to any invertible map on symmetric matrices and any on antisymmetric ones: an enormous freedom nobody has used.
Construction: V is n functionals fixed by H (the n-sparse ones supported on cosets of a self-dual code exist, section 3) plus (N−n)/2 pairs (φ, φ∘H) with φ chosen freely.
- Tried by hand: φ = differences along one bit gives V = one half-size call and V⁻¹ = another: the textbook, 2 calls [derived].
- Mutation to run: take φ from a pyramid (half of the Haar functions at every scale, frequency sets chosen as subgroups). All coset sums along a chain of subgroups cost < N in total, and the partners φ∘H are again coset functions at the dual scale [derived], so φ∘H costs calls of sizes N/4, N/8, …: total child volume N/2, the V-cycle shape. What is not known is the cost of V⁻¹ for that choice.
- First sign of life: at 16 points, a choice of 6 pairs whose V and V⁻¹ together use child calls on fewer than 16 numbers.

### Idea 4. V-cycle through a Gram inverse (the reflection language, done with dense-but-cheap parts)
H = √N·I − 2√N·L·(R·L)⁻¹·R for ANY L whose columns span the −√N eigenspace and any R annihilating the other one [derived]. The child problem is then "apply the inverse of the N/2 × N/2 matrix R·L", which need not be a transform at all.
- The floor note excluded the half-touch identity because eigenvectors have ≥ √N non-zero entries, "so the left part is not cheap". That step assumes cheap = sparse. A pyramid of coset sums is dense and costs O(N). The exclusion does not cover it. [derived; this is a correction to §5 of the floor note]
- Tried by hand: L = (H − √N) restricted to a half-cube. Then R·L is a multiple of √N·I + H_(N/2), whose inverse is (√N·I − H_(N/2))·(2/N): the child IS a half-size transform, exactly one [derived]. But this L and R each need a call themselves (3 calls in all).
- Cheap vectors in the eigenspace do exist: (coset function on D) − (its image, a coset function on the dual subgroup), for every D and every sign pattern [derived]. A spanning set of N/2 of them, taken across scales, is the object to look for.
- First sign of life: at 16 points, 8 such differences, spanning, whose 8×8 matrix R·L has an inverse with fewer than 16 non-zero entries or is triangular after reordering.

### Idea 5. Symmetry sectors: almost all of the transform is tiny blocks
H commutes with permuting the k bits. In a basis adapted to that symmetry it is a direct sum of Krawtchouk matrices of size k−2j+1, with multiplicity C(k,j) − C(k,j−1) [derived, standard]. Work in the middle, per point, if the blocks are applied densely: 3.38, 6.48, 12.82, 25.56 at k = 4, 16, 64, 256, against the textbook's 4, 16, 64, 256: it grows like 1.6·√k. With a fast block algorithm (log of block size): 1.62, 2.55, 3.53, 4.53 [ran].
So: transform ≤ 2·(change to ANY permutation-adapted basis) + N·O(√log N). The whole order question moves to "how cheap is a permutation-adapted basis change on N numbers".
- Tried by hand: the standard pairwise coupling costs k·N/4 at its first level alone, so it is Θ(N log N) as it stands; at 4 and 16 points it ties or loses (8 against 8; about 72 against 64) [derived].
- Why it may live: (i) the first coupling step is a butterfly on only the half of the array where two bits differ, which is the floor note's unexplored hatch "blocks only where the pair's digits disagree"; (ii) we do not need the full adapted basis, only one in which the blocks stay small; (iii) OpenAI's own files are named SectorIdentities, ToeplitzIdentities, CirculantUpdates [read: file names only], so their construction may already be a first step on this road.
- First sign of life: a 64-point basis change, adapted to permutations of the 6 bits within two groups of 3, costing under 96 additions each way.

### Idea 6. The kernel on a self-dual code: rank-one blocks, and why E8 may have worked
For any self-dual binary code D, the kernel (−i)^distance restricted to (coset of D) × (coset of D) has rank ONE [ran: all 256 blocks for the [8,4,4] Hamming code at k = 8; also the code of four pairs], because i^weight is a ±1 character on a self-orthogonal code [derived]. So the N×N matrix is a √N × √N array of rank-one blocks: the exact "complementary low rank" shape of butterfly algorithms.
- As it stands this is the textbook in a rotated frame (two layers of √N-size transforms) [derived].
- The fast-multipole trick needs rank to SHRINK with scale. Here it does along a chain of codes D_1 ⊂ D_2 ⊂ … only if the cross-level transfer maps are cheap. Nobody has written those transfer maps for a chain of self-dual codes of lengths 8, 16, 24, 32 (Hamming, its sums, Golay).
- [guess] the E8 lattice family in the published unit works because E8 is built on exactly this code: every coset pair is rank one.
- First sign of life: transfer matrices between the cosets of d8+ ⊂ … at 16 bits being sparse (O(1) per row) rather than 16×16 dense.

### Idea 7. Exponential kernels are linear-size when the inverse is sparse: change the metric
t^distance on a path, cycle or tree costs O(N), because the inverse matrix is tridiagonal or tree-shaped (two-pass recurrence). On Z_m^r with Lee distance the same kernel costs O(N·r), independent of m [derived]. The cube is the member m = 2, and also m = 4 by the Gray map, which is an isometry from (Z_4, Lee) to (two bits, Hamming) [derived]. So the transform sits at the expensive end of a family whose other end (r = 1, a single cycle of length N) is linear.
- Tried by hand at m = 4: the circulant (1, t, t², t) has a tridiagonal-circulant inverse only for t = 0, so the 4-cycle already fails; the wrap-around is what breaks it [derived].
- Mutation: do not ask for the same kernel. Ask which unimodular kernels on the long cycle Z_N of the form e^(iθ·|j|) plus a bounded-rank correction are free-equivalent to the Fourier matrix of some group of order N. The Fourier half of the published theorem is the natural target here, not the Walsh half.
- First sign of life: at N = 8 or 16, a kernel (sparse-inverse circulant + rank ≤ 2) that is a scaled unitary with flat entries.

### Idea 8. The group algebra: the transform is multiplication by one element
H = D·(multiplication by γ)·D with γ = Π_j (1 + i·g_j) in the group algebra of Z_2^k [derived from the read identity]. Under the substitution g_j = X^(2^j), γ is the generating function of i^(binary digit sum), a Thue–Morse-type function with T(X) = (1 + iX)·T(X²). Cheap multipliers in a group algebra: sparse elements; subgroup indicators (coset sums); and inverses of sparse elements when the group has long cycles.
- Tried by hand: Z_2^k has no long cycles; the inverse of an element on r generators has up to 2^r terms, no recurrence [derived]. Dead as stated.
- What it taught, and the mutation: γ has a short description as a product of k two-term factors; the question "is γ a product of O(1) factors, each a sum of O(1) coset indicators with signs?" is finite at each N and I know no obstruction except that the factors together must involve k independent linear forms, so some factors need medium-size subgroups. Medium-size subgroups are exactly where coset sums stay cheap (F3) while the Clifford count stops applying. This is idea 1 in commutative clothing: there the letters are reflections, here they are convolutions.
- First sign of life: at 16 points, i^weight as a product of two elements each a sum of ≤ 3 signed coset indicators.

### Idea 9. Apply one projector of rank N/4 instead of the transform
From F1: U = (2Π₀ − (I+P)/2) + i·(2Π₁ − (I−P)/2), where Π₀, Π₁ project on Fourier levels ≡ 0 and ≡ 1 mod 4 [derived]. After one cheap fold by the antipodal map (N additions) the problem is two half-size problems, each "apply a projector of rank about N/4 on N/2 numbers", living on the folded cube. A rank-N/4 projector is Π = B·A with B: N/4 → N/2 and A: N/2 → N/4: a quarter-size bottleneck in the middle. That is a place where the data provably narrows, which the tensor picture never shows.
- Not tried beyond the algebra. First sign of life: at 16 points, the 8×8 even-sector projector (rank 4 ± 1) factored through 4 numbers with both factors under 8 additions.

### Idea 10. The cube's adjacency matrix as a stepping stone
A = sum of the k bit-flips, k ones per row; U = exp(−i(π/4)·A) up to a scalar [read]. Is A itself linear-size? Naively (k−1)·N additions. Sharing sums over pairs of directions gives 3kN/4 − N [derived: the sum over directions 1 and 2 is the same for y and y+e1+e2]; at k = 2 the 4-cycle's adjacency matrix has rank 2 and costs 2 additions for 4 outputs. A is the simplest non-trivial element of the same commutative algebra as U, it is real and sparse, and no one in these notes has asked for its cost. If even A needs N log N, that is a cleaner lower-bound target than U; if A is O(N), the three-term recurrence gives every distance matrix at O(N) each and the question becomes how many are needed.
- First sign of life: the exact minimum number of additions for A at 8 and 16 points (naive 16 and 48; pair sharing gives 12 and 32).

## 2. Per language: cheapest known there, and what I did

| Language | Cheapest known in that language | Tried at small size | Came out |
|---|---|---|---|
| (a) kernel sum on the cube | butterfly shape, N log N; linear only when rank shrinks with scale | blocks on self-dual code cosets, k = 8 | all 256 blocks rank one; shape is butterfly, not multipole (idea 6) |
| (b) the family K_t | cheap members only t = 0, ∞ (identity, antipodal map), ±1 (rank one, absorbing) | span of the four cheap members | covers the whole algebra only at k ≤ 3; at 8 points about 26 additions against 24 [derived] |
| (c) reflection | none below N log N | Gram-inverse form; trace of Q | child is exactly one half-size transform but the frame costs two more; eigenspaces are (N±√N)/2 (ideas 3, 4) |
| (d) polynomial evaluation / group algebra | Yates, N log N | product form of γ | idea 8; symmetric sector is a Möbius substitution on degree-k polynomials (idea 5) |
| (e) propagator of the cube graph | polynomial of degree k in A: k applications | cost of A itself | 3kN/4 − N by pair sharing; idea 10 |

## 3. Anomalies and pretty facts (kept because they did not go away)

1. The transform generates a 4-dimensional algebra: span{I, P, U, U⁻¹}. [derived]
2. U is a square root of the antipodal map (U² = scalar·P), and differs from the trivial pairwise square root R by a REAL flat reflection Q. [ran]
3. Q's sign depends only on distance mod 4, pattern ++−−. [ran]
4. trace(Q) = −√N: eigenspace dimensions (N±√N)/2, the dimensions of symmetric and antisymmetric √N×√N matrices; the transform is conjugate to matrix transpose. [ran + derived]
5. For unitary-scaled monomial M, rank(H − M) ≥ (N−√N)/2, and I − J/2 tensor powers meet it with equality. The task's "rank exactly N/2" is the value for M = √N·I; a relabelled M does slightly better. [derived]
6. H_4 = 2·(I − J/2) up to relabelling: the 4-point transform is the Grover diffusion on four points, one coset reflection, 7 additions. [ran]
7. I − J/2 is flat and invertible on 8 and 16 points too; it stops being orthogonal, not flat. [ran]
8. The 8-point reflection I − J/4 spreads more per addition (1.18 bits) than a butterfly (1.00). [ran]
9. (−i)^distance is rank one on every pair of cosets of ANY self-dual code, doubly even or not. [ran + derived]
10. H has an eigenbasis of vectors with at most 2√N non-zero entries built from those cosets; √N of them have exactly √N, meeting the support bound. [derived]
11. In a permutation-adapted basis the transform is blocks of average size about 1.6·√(log2 N). [ran]
12. Lee distance on Z_4 is Hamming distance on two bits; exponential Lee kernels on Z_m^r cost O(N·r) whatever m is. [derived]
13. A coset sum costs under N additions for every subgroup size; only sizes 2 and 4 give Clifford reflections. [derived]

## 4. If I had one more hour
Idea 1 at 16 points (three-letter words over the 8- and 16-point reflections), because it is a finite search, it is outside every count made so far, and fact 8 says the 8-point letter is individually better than a butterfly. Then idea 4's 8-vector spanning set at 16 points, because it tests the one step of the floor note that I think is wrong as written.
