# i-wild: invert, exaggerate, combine

10 October 2026, about 20:50 to 21:15 EDT, agent "i-wild". Private notes. No person has read this. Nothing is in Lean. Nothing was posted.

Marks: [ran] = run tonight, files in `waves/wave-01/i-wild/`. [derived] = my own short argument, written here, checked by nobody. [read] = from the notes named in the task. [guess] = a guess.

Words. *N* = 2^k: length of the transform. *H*: the plain ±1 Walsh-Hadamard matrix, entry (−1)^(v·w). *Overlap* of two addresses: the number of bit positions where both have a 1. *Walsh weight*: the number of 1 bits of a frequency. *Information set* of a subspace: a set of coordinates whose values fix the whole vector.

This note is generation and play. No odds and no verdicts on purpose.

## What I played with on 16 points

**Play 1: half of the outputs determine the other half** (`enc16.py`, `enc16.out`, exact fractions, 21 s) [ran].
H = 4(I − 2P) at N = 16, P the projector on the 8-dimensional (−4)-eigenspace. So y = 4x − 8Px, and Px lies in a fixed 8-dimensional space, a linear code. Pick an information set T of 8 coordinates. Then

    y_rest = 4·x_rest − Γ_T·(4·x_T − y_T)

with Γ_T the code's 8×8 "encoder". Only the 8 outputs on T need a transform; the other 8 come from x and Γ_T.

- 7,280 of the 12,870 sets T are information sets.
- Γ_T has between 37 and 64 non-zero entries. The 16 information sets that lie in an affine 3-dimensional subspace (the textbook's choice) all give 64: there Γ_T is the half-size transform in disguise.
- The sparsest Γ_T (37 entries, 832 sets, entries 0, ±1, ±2) all belong to sets T that span the whole cube.
- **Bent variant.** With f = v1·v2 + v3·v4, D_f the signs (−1)^f and P_B the relabelling that swaps bits 1↔2 and 3↔4, the matrix G = D_f·H·P_B·D_f is symmetric with all-ones diagonal (asserted exactly in the script). G − 4I has rank **6**, not 8. So the 16-point transform is "a free signed relabelling minus a rank-6 matrix". Only 6 outputs need a transform. The encoder is 10×6; its sparsest form has 30 entries, all ±1 (192 sets; the histogram has only four values: 30, 34, 39, 60).
- Count at 16 [derived from the run]: 6 outputs taken from an 8-point transform after one fold cost 28 additions; encoder 30 − 10 = 20; combining 16. Total **64**, the textbook's number again. But the sparse encoders belong to sets T that are not inside a 3-dimensional subspace, so the 28 is not available together with the 20.

What it taught: the choice is "T structured, encoder dense" or "encoder sparse, T scattered". The trade is never free at 16 points, and the textbook sits at one end of it.

**Play 2: how the cost grows with the number of outputs wanted, and what the transform is as a grading** (`grow16.py`, `grow16.out`, 6 s) [ran].

- Outputs in a subspace of dimension d cost N + (d − 1)·2^d additions [derived]; the greedy sharing program reproduces 15, 16, 20, 32 at 1, 2, 4, 8 outputs. The first output costs 15, the second costs 1 more, the last 8 cost 32.
- Outputs taken in order of Walsh weight or at random are dearer in the middle of the range (41 against 27 at 5 outputs). These are upper bounds from a greedy program that finds 72 for the full transform where the textbook has 64, so only the subspace column is exact.
- Exact check: with D = diag(i^weight), H = D·K·D where K has entries (−i)^distance, and K = (1 − i)^k · Σ_j i^j·E_j, E_j the projector on Walsh functions of weight j. **The transform is the splitting of the data by Walsh weight modulo 4.** The splitting modulo 2 is free: Σ_j (−1)^j·E_j is the relabelling "complement the address".

**Play 3: a cheap wrong answer** (`zeta16.py`, `zeta16.out`, 20 s) [ran]. For idea 5 below.

- H = ζᵀ·diag((−2)^|S|)·ζ, and the product cut off at |S| ≤ d equals the transform on every pair of addresses with overlap ≤ d: checked on all pairs at N = 16 and N = 64, every d.
- At N = 64, d = 2: 83 % of the matrix entries are exact; d = 3: 96 %; d = 4: 99.5 %. At N = 16, d = 2: 95 %. At these sizes the cut-off saves almost nothing (the partial ζ costs 2.53·N at d = 2 against 3·N in full at N = 64); the point is the growth law.
- Window of consecutive overlaps that holds 99 % of all pairs: 9, 18, 36, 72, 143 wide at k = 16, 64, 256, 1024, 4096. That is 2.25·√k. For 99.99 %: 3.4·√k.
- [[1,0],[1,1]] = diag(−1/15, −1/6)·H2·diag(3/2, −1/2)·H2·diag(1, 2)·H2·diag(−3/2, 5/2)·H2, exact. So the subset-sum transform ζ is four transforms and four diagonal scalings.
- Schur-Weyl count for idea 6: (operations of the block part)/N is 3.4, 6.5, 12.8, 25.6, 51.1 at k = 4, 16, 64, 256, 1024, about 1.6·√k; against N·k that is a factor 0.84, 0.41, 0.20, 0.10, 0.05.

**Play 4: one resolvent is not enough** (`mseq.py`, `mseq.out`, 3 s) [ran]. For idea 7 below. One period of a ±1 maximal-length sequence, read as a sum of geometric sequences, needs as many of them as it can: the Hankel matrix of one period has rank 8 of 8, 16 of 16, 31 of 32, 64 of 64 at k = 4, 5, 6, 7. (That the transform on non-zero addresses is this sequence in multiplicative coordinates is the standard fact I relied on; the script checks only that the sequences are maximal-length.) Mutation: products of a few resolvents along *different* cycles, not a sum along one.

## The ideas

### 1. The eigenspace as a code: transform only an information set [ran, Play 1]
Construction: write H = √N(I − 2P). Choose an information set T of the (−√N)-eigenspace. Compute y_T by any means, then y_rest = √N·x_rest − Γ_T(√N·x_T − y_T). Cost = cost(y on T) + cost(Γ_T) + O(N).
Mutation after the run ("yes, and"): do not ask Γ_T to be sparse. Ask it to be a *smaller* transform. For a self-dual code C the eigenvectors χ_a·1_(C+b) have support √N and Γ_T splits into blocks of size about √N [derived]; such a Γ_T would cost (N/4)·log N instead of the (N/2)·log N of the second half-size call [guess]. The question is which T go with it.

### 2. Bent relabelling: the transform is a free relabelling minus a matrix of rank (N − √N)/2 [ran at 16; derived in general]
The reflection fact says rank N/2. Conjugating by a bent quadratic sign pattern and a relabelling gives a symmetric Hadamard matrix with constant diagonal, trace N, so its (−√N)-eigenspace has dimension N/2 − √N/2.
[derived] With real signed relabellings this is the minimum possible (trace argument). With a diagonal correction alone, N/2 is the minimum (the off-diagonal block is a half-size transform). With complex phases or unequal scalings on the relabelling I have no bound: untouched.

### 3. The exponent is a density [derived]
Outputs on a subspace of codimension log2(k) cost about 2N. All translates of an output set cost the same (multiply the input by a character). So: *the transform costs N·(log N)^z exactly when some set of N/(log N)^z outputs can be computed in O(N)*, and linear size means a set of constant density. The textbook's sets are subspaces. Subspaces of constant density cost a constant fraction of everything. So the object to search for is an output set that is **not** a subspace: a union of subspaces that share folds, a Hamming ball, a code.
Seen: all outputs of Walsh weight ≤ w cost at most (2w + 1)·N [derived from the fold recursion c_w = c_(w−1) + 2]. Cost grows with the *radius*, not with the number of outputs.

### 4. A square root of a free relabelling [ran for K; derived for C]
OpenAI's 2×2 matrix C = ½[[1+i, 1−i],[1−i, 1+i]] satisfies C² = bit flip. So C^(⊗k) is a square root of "complement the address", which costs nothing. Another square root of the same relabelling costs O(N): apply C to each pair (v, complement of v). The two roots differ by one involution R that is +1 on Walsh weights 0, 3 mod 4 and −1 on weights 1, 2 mod 4: a quadratic sign pattern on the frequency side.
Construction to try: all of the transform's cost is in R. R is a reflection whose mirror is "weights 0 or 3 mod 4". Apply idea 1 to R instead of H.

### 5. A cheap wrong answer that is exactly right on most of the matrix [derived, not run]
H = ζᵀ·diag((−2)^|S|)·ζ, where ζ sums the data over all addresses containing the set S (the LDU form of [[1,1],[1,−1]] in every bit). Keep only sets S of size ≤ d. Then:
- ζ restricted to |S| ≤ d costs about (d + 1)·N, by "fold when the bit is not in S, restrict to half when it is": c_d = 1 + c_(d−1).
- The truncated product equals (−1)^overlap for every pair of addresses with overlap ≤ d, because Σ_(j≤d) C(t, j)(−2)^j = (−1)^t for t ≤ d.
- With other coefficients the window of exact overlaps can be any d + 1 consecutive values. Overlaps of random pairs sit at k/4 ± 0.43·√k.
So about N·√(log N) operations give a matrix that agrees with the transform on all but a fixed small fraction of its entries, and the error is again a function of the overlap alone, supported in the tails. At d = k the count is the textbook's. [ran, Play 3: exactness on the window at N = 16, 64; the 2.25·√k window. The cost law (d + 1)·N is my recursion, run only as a count.]
Same object, other words [derived]: H = exp(F)·(−2)^weight·exp(E) for the raising and lowering operators E, F of the cube; ζ = exp(E). **A linear-size transform exists exactly when a linear-size subset-sum (zeta, or Möbius) transform exists** (Play 3: ζ is four transforms and four scalings; H is two ζ's and one scaling). Subset sums are prefix sums in k dimensions on a 2×2×…×2 array, a 0/1 problem with its own literature.
Mutation: split addresses into classes inside which overlaps are confined to a narrow window (codes with few distinct overlaps; this is where the E8 and Reed-Muller families live), and use one low-degree form per pair of classes.

### 6. Schur-Weyl: a basis that does not depend on the transform [derived]
H = H2^(⊗k) commutes with every permutation of the k bit positions. In the basis that splits (C²)^(⊗k) by symmetry type, *every* operator g^(⊗k) is a direct sum of blocks of size k − 2j + 1 (Krawtchouk matrices), each repeated C(k,j) − C(k,j−1) times. The typical block has size about √k. So in that basis the transform costs at most about N·√(log N) with dense blocks.
By hand at k = 4: blocks of size 5, 3, 1 with multiplicities 1, 3, 2; 54 entries against the textbook's 64 operations.
All the remaining cost is in the change of basis, which keeps the Hamming weight of addresses (it is block diagonal on the weight layers) and is the same for every 2×2 kernel. Its obvious program adds one bit at a time with 2×2 rotations and costs N·k. Nobody in these notes has asked what that weight-preserving map costs.

### 7. A new cheap letter: the resolvent of a relabelling [derived]
For an address relabelling Π and a scalar c, solving y − c·Πy = x costs about 4 operations per entry (one pass around each cycle to get one value, one pass back). The matrix (I − cΠ)^(−1) is dense on every cycle, with entries c^(steps along the cycle). So *rows with unboundedly many terms cost a bounded number of operations per entry*.
- On one bit, (I − t·flip)^(−1) is the kernel [[1,t],[t,1]] up to a scalar: the K_t family is a product of k commuting resolvents.
- Prefix sums are the case Π = shift. A relabelling that mixes two digit columns in long cycles (multiplication by a generator of the field with d² elements) gives a letter that moves the pair's diagonal and has no bound on the number of sums. This is hatch (b) of the floor note with the "bounded number of sums" removed at linear cost.
- Known fact to combine it with [guess that it applies as stated]: in multiplicative coordinates the transform on the N − 1 non-zero addresses is a circulant whose first row is a maximal-length shift-register sequence.

### 8. Solve, do not apply [derived]
One system A·y = B·x with A, B sparse: each row a of A has A-row and B-row supports with product ≥ N, so the two matrices have at least 2·N^1.5 entries together; at N = 16 that is 128, reached by (I⊗H4^(−1))·y = (H4⊗I)·x. A chain of such systems with helper unknowns is a circuit. What is left over as new is idea 7: systems that are not triangular but cyclic.

### 9. The linear recursion read backwards [derived]
On an n×n array, t(n²) = c·t(n) + O(1) per entry with c·n calls of size n. c = 2 is the textbook, c = 1 gives N·log log N, c < 1 gives O(N). Rank allows c = 1/2: H⊗H − n·I has rank n²/2. All the cost then sits in the frame of eigenvectors. In the frame of a self-dual code the frame map is "transform every column of an n×n array Ĉ that satisfies Ĉ = −(signs)∘Ĉᵀ". So a sufficient target is: **column-transform a signed-symmetric n×n array with fewer than n calls of size n.**

### 10. (silly) Characteristic 2 first
Modulo 2 the transform is the all-ones matrix, rank one, cost N. Exactly, H = J − 2B with B the 0/1 matrix of overlap parities, and the integer overlap matrix has rank k. Lifting digit by digit leads to idea 5.

### 11. (silly) Transform N shifted copies at once
Put the N XOR-shifts of x in a matrix X. Then H·X·H = N·diag(Hx). The answer is the diagonal of a two-sided transform of a matrix that costs nothing to write down. Fan-out, one two-sided call on structured data, read the diagonal.

### 12. (silly) Differentiate a family
Coefficients are unbounded, so a family of cheap programs that tends to the target can be turned into an exact one by running it at a few parameter values and combining. G(u) = Σ_j u^j·E_j is a polynomial of degree k in u; G(1) is the identity, G(−1) the complement relabelling, G(0) and G′(0) cost O(N) (weights 0 and 1), likewise at infinity, and G′(1) is the hypercube's adjacency matrix. The target is G(i). Ask what G costs at points other than 0, ±1, ∞, and whether jets at the cheap points determine it more cheaply than k steps.

### 13. (silly) Batches are not additive
OpenAI's unit is a mass-production effect: W arrays for less than W times one array. Schönhage's sum of two disjoint matrix products costs less than the two apart. Exaggerate: take W = N arrays, so the batch is an N×N matrix, and ask for H applied to all columns as one object (idea 11 is its smallest case).

## Anomalies and pretty facts

- C^(⊗k) is a square root of "complement the address" [derived].
- The transform is the grading of the Walsh basis by weight mod 4; the grading mod 2 is free [ran].
- 64 came back in every count at 16 points: textbook, eigenspace encoder, bent encoder (28 + 20 + 16) [ran + derived].
- √(log N) appears three times: the typical Schur-Weyl block, the width of the overlap window, and the ceiling δ ≤ 1/2 of OpenAI's generic amplification [derived, read]. [guess] one phenomenon.
- The bent form drops the reflection's rank by exactly √N/2 [ran at 16].
- The encoder histogram in the bent form has only four values, 30, 34, 39, 60 [ran].
- Exactly 16 information sets lie in an affine 3-space, and all give the dense encoder [ran].
- H's XOR-diagonals are its own rows times the parity sign: H(v+a, v) = (−1)^|v|·H(a, v) [derived].
- The truncated ζ-form at full degree, the Schur cascade and the fold recursion all cost the textbook's N·k [derived].
- Greedy pair sharing does not find the butterfly: 72 at 16 points [ran].
- The transform and the subset-sum transform are the same problem up to a factor 4 and O(N) [ran for the 2×2 identity, derived for the tensor power].
- The Hankel matrix of one period of the maximal-length sequence is one short of full rank at k = 6 (31 of 32) and full at k = 4, 5, 7 [ran].
- The cut-off at d = 0 is the all-ones matrix, cost N; it already equals the transform on 53 % of the entries at N = 16 and 51 % at N = 64 (the pairs with even overlap) [ran].

## Not done

- Ideas 6, 7, 9 have only counts behind them, no program that computes a transform. Idea 5's exactness on the window is run; its cost law is a counted recursion; nobody has built the tail correction.
- The add counts in Play 2 other than the subspace column are heuristic upper bounds.
- I did not check any of this against the literature tonight.
