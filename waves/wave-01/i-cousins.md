# i-cousins: the frontier among the Hadamard transform's cousins

10 October 2026, night. Private. One agent, about 40 minutes (5 over the box). Nothing reviewed, nothing in Lean.
Marks: [ran] = exact computation in `i-cousins/play1.py`, `play2.py`, `play3.py`; [derived] = worked by hand here; [read] = from the notes named in the task; [guess].

**Cost model used here** (not OpenAI's): a linear circuit whose gate is z = u + c·v with any constant c; scalings and relabellings are free; cost = number of gates. Whether OpenAI's model prices a doubling was **not checked**, so the "7 gates" below must be re-priced before it is quoted anywhere.

## 1. The map

Kronecker powers M^(⊗k) of a 2×2 matrix M = [[a,b],[c,d]], up to free scalings and swaps, have **one** invariant: τ = ad/(bc), with τ and 1/τ the same. [derived]

| M | τ | cost of M^(⊗k), n = 2^k | mechanism |
|---|---|---|---|
| two zeros (monomial) | 0/0 | 0 | relabelling |
| rank one | 1 | n − 1 + fan-out | everything passes through one number |
| triangular: zeta, Möbius, disjointness | 0 or ∞ | ≤ (n log n)/2 | textbook only |
| Hadamard, K_t at t = ±i | −1 | ≤ n log n | textbook only |
| any other | other | ≤ n log n | textbook only |

Two pretty points: τ = −1 is the only fixed point of τ → 1/τ besides rank one. And the whole line collapses:

**One class.** [ran for the identities, derived for the consequence]
- H = L · diag(1, −2) · U with L, U the down and up zeta matrices. So Hadamard ≤ 2 zeta transforms.
- H·diag(3/2, −1/2)·H·diag(1, 1/2)·H = [[2,0],[5/2,3/2]], a zeta up to scaling. So zeta ≤ 3 Hadamards.
- H·diag(a,b)·H has τ = ((a+b)/(a−b))², always a square; over GF(5) two Hadamards reach only τ = −1. A non-square τ needs three.

So every invertible, non-monomial 2×2 Kronecker power costs the same up to a factor of at most 3, and **the exponent z transfers exactly**. Inside 2×2 Kronecker powers there is no linear cousin except rank one. The frontier is elsewhere.

**Where it is.** For a d×d matrix of rank r < d, write M = A·B through r dimensions; the digit-by-digit recursion shrinks, cost ≈ c·n·d/(d − r): **linear**. [derived] Haar is the same mechanism (recursion a·T(n/b) + n with a = 1, b = 2). Splitting M = A + B does not help because rank(A) + rank(B) ≥ rank(M): the pieces need d sub-transforms between them.

> It fails for Hadamard exactly because H is invertible on every digit: each digit hands d full-size independent sub-problems to the rest (a = b), and no way is known to run d copies of one transform for less than d times its price.

## 2. Smallest circuits [ran]

Exhaustive at n = 4 over GF(5) (all sets of up to 3 intermediate forms; 4 for the smaller ones):

| matrix | gates | textbook |
|---|---|---|
| rank one J⊗J | 3 | 3 |
| zeta L⊗L | 4 | 4 |
| **Hadamard H⊗H** | **7** | 8 |
| generic τ = 2, [[1,1],[1,2]]⊗2 | **7** | 8 |
| Haar, 4 points | 6 | 6 |
| cube neighbour sums A_2 | 2 | 4 |
| A_2 + I | 6 | |

- No 6-gate circuit for H⊗H over GF(7), GF(11), GF(13) either (all pairs of intermediates). A minimum over Q could only be lower than these at finitely many primes, so 7 is very likely the minimum over Q; not proved.
- The 7-gate circuit over Q, checked exactly on the unit vectors: w1 = a+b, w2 = c+d, y0 = w1+w2, y2 = w1−w2, w3 = 2a − y0, y3 = w3 + 2d, y1 = w3 + 2c.
- How the minimum grows: k = 1: zeta 1, Hadamard 2. k = 2: 4 and 7 (so Hadamard < 2 zeta). k = 3: zeta ≤ 12 (greedy over GF(7), 1,905 tries, never below 12); Hadamard ≤ 22 by composing the 7-gate block [derived]; my greedy never got below 40 for Hadamard or generic: a bad heuristic, no information. k = 4: Hadamard ≤ 56 as eight 7-gate blocks [derived]; no search. **k = 3, 4 minima are unknown.**

Why 7: H_4 = 2P + (rank one), P a permutation: the 4-point transform is one Householder reflection, J − 2I up to relabelling. [derived, then ran]

## 3. Ideas

**1. The Grover-diffusion family: a unitary Kronecker cousin that is linear.** G_d = J_d − (d/2)·I satisfies G² = (d²/4)·I for every d [ran, d = 2..9]. It costs 2d − 1 gates. So G_d^(⊗k) on n = d^k points costs under 2n per factor: 2n·log n / log d. At n = 2^24: 21 gates per point as 4^12, 15 as 8^8, 7.9 as 64^4, **4 as 4096^2** [ran]. G_4 is the Hadamard transform, and d = 4 is the only flat member.
> Linear for a stated reason: each tensor factor is identity plus rank one, and the price is per factor, not per bit. It fails for Hadamard because flatness forces factor size 4, hence log₄ n factors.
*Next:* drop "Kronecker": layers of identity-plus-rank-one blocks on arbitrary partitions of the n addresses (idea 2).

**2. Householder depth of H_n.** Write H_n = (monomial) × L layers, each layer an arbitrary partition of the addresses into blocks with one reflection per block (cost < 2n per layer). O(1) layers would be O(n). Two constraints [derived]: (i) for any signed permutation P, rank(H − √n·P) ≥ (n − √n)/2, by a trace count; tight: (J−2I)^⊗2 − 4I has rank 6, the cube with +8I rank 28, while Sylvester's H_16 − 4I has rank 8 [ran]. So the layers hold at least (n − √n)/2 blocks. (ii) every address must reach all n, so (block size)^L ≥ n. With equal blocks this gives L ≥ about log n / log log n: **the budget leaves room for n log n / log log n, not for n**.
*Tried:* at n = 16 the −1 eigenspace has dimension 6; six orthogonal reflections cost Σ(2·support − 1); by hand I found support 6 (66 gates, worse than 56). Not searched.
*First sign:* an orthogonal basis of that 6-dimensional space with total support under 31.

**3. Bits per gate.** Row entropy of a flat n×n unitary is log n bits, n log n in all. A butterfly makes 1 bit per gate; the 4-point reflection 1.143; a d-point reflection peaks at **d = 6 with 1.244** (d = 5: 1.235, d = 8: 1.182) [ran, floats]. A rank-one piece of a unitary carries bounded row-mass, so reflections give at most (2 log d)/d bits per gate for large d [derived]: this is Morgenstern's bound seen as entropy. More than O(1) bits per gate needs **large shared components that cancel**, as J does in H = 2B − J.
*Construction:* a flat unitary (not Sylvester) built from 5-, 6-, 7-point reflections. *First sign:* any flat unitary of order 36 under 162 gates (that is 7/8 · 36 · log₂ 36).

**4. Aim at the zeta transform instead.** By "one class", O(n) for subset sums ⟺ O(n) for Hadamard, and any exponent carries over. Zeta has an order, a Möbius inverse and 3^k non-zeros; without subtraction it needs (n log n)/2 [read, from memory of Boyar–Find; not re-checked], so every gain must come from cancellation.
*Tried:* n = 4 is exactly 4; n = 8 greedy stays at 12. *First sign:* 11 gates at n = 8, or 31 at n = 16.

**5. Cube neighbour sums, the nearer problem.** A_k x = sum over the k neighbours. H ∝ exp(iπA/4), a polynomial of degree k in A [derived]; A = H·D·H/n, so A ≤ 2 Hadamards, and a lower bound for A is one for H. A_2 costs 2 gates, not 4: rank 2, because the neighbourhoods of 00 and 11 coincide [ran]. A is singular for even k (nullity C(k, k/2)).
*First sign:* A_4 under 48 gates by a route that is not two transforms.

**6. Direct sum is the hinge.** O(n) needs N copies of H_N for O(N) each, i.e. X ↦ H_N·X for an N×N matrix X in O(N²): Alman's reduction [read], read as a question about one fixed matrix. For generic matrices direct sum does fail at N copies (fast matrix multiplication).
*Tried by hand:* two copies of zeta_4 cannot share a gate (8, not 7) [derived]. Two copies of H_4 under 14 gates: not run.
*First sign:* any fixed invertible matrix whose two copies cost less than twice one.

**7. Schur–Weyl.** H^(⊗k) is one element of SL(2) acting on (C²)^(⊗k). In a Schur basis it is block diagonal, blocks of size ≤ k + 1; with a fast block transform the middle costs 2.08, 2.55, 3.04, 3.53, 4.03 per point at k = 8, 16, 32, 64, 128 against the textbook's k [ran]: it grows like ½·log₂ k. All of n log n then sits in the basis change S, the same S for every 2×2 M. Built qubit by qubit, S is k layers of n/2 rotations [derived]: no gain yet.
*Next:* S need not be the full Schur basis; any cheap basis in which H has small blocks will do.

**8. Product of Haar-diagonal operators.** Operators diagonal in the Haar basis of any tree on the addresses cost O(n). K_i⊗K_i (the 4-point transform up to phases) is diagonal in the Haar basis of the tree {00,11 | 01,10}: its double eigenvalue has eigenvectors e01 − e10 and e00 − e11 [derived by hand, not run]. One tree fails from k = 3: eigenvectors need support ≥ √n and a Haar basis has only about 2√n such vectors. With translation-invariant factors and linear flags at least k/2 flags are needed [derived, rough].
*Next:* arbitrary leaf orders and arbitrary diagonals, where that bound says nothing. *First sign:* H_8 as two such factors.

**9. Sparse stencils cannot do it.** If each layer is a convolution with an s_j-point stencil, supports multiply, so Π s_j ≥ n and Σ(s_j − 1) ≥ log₂ n: the textbook is optimal in that class [derived]. Linear layers must be dense but structured (constant on cosets: rank one again).

**10. Rank-(d−1) neighbours.** H_d = (rank d − 1) + (rank 1); the first part alone is linear with constant about d. *Tried:* the recursion still needs d sub-transforms. *Next:* pick the rank-one part so its sub-transform is one already computed.

## 4. Anomalies and pretty facts

See the structured list returned with this report; the main one is that the 4-point transform takes 7 gates, not 8.

## 5. Not done

- k = 3 and k = 4 minima: no exhaustive search; the greedy for Hadamard is useless as written.
- The 7 gates were not re-priced in OpenAI's model, and "60 additions at 16 points" was not traced to its source. In this model eight 7-gate blocks give 56 [derived].
- No literature was read tonight; "Boyar–Find" and the minimum-support results are from memory.
- Ideas 2, 3, 6, 8 have hand trials only.
