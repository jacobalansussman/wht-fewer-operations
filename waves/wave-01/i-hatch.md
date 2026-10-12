# i-hatch: breaking the obstruction on purpose

> Editor's note (11 October 2026): this report was written before the paper of Coppersmith, Feig and Linzer (1994) had been read. The 4-point circuit in 7 operations and the rate 7/8 are due to that paper, not to the patent filed in 2002 or to Alman and Rao (2023). See [Earlier papers](../README.md#earlier-papers).

10 October 2026, about 20:45 to 21:20 EDT, agent "i-hatch". Private notes. No person has read this. No Lean, no git, nothing posted. Generation and play only: no odds and no verdicts in this file.

Marks: [read] read today at the place cited. [ran] run today; file given. [derived] my own argument, written here, checked by nobody. [guess].

Files: `waves/wave-01/i-hatch/` holds `play.py` + `play.out`, `flags.py` + `flags.out`, `flags5.py` + `flags5.out`, `flags4check.py` + `flags4check.out`, `codes.py` + `codes.out`. Every run went through `wht35/bin/light.py`.

Words. *n* = 2^k points; *k* = number of address bits. *H*: the plain ±1 Walsh-Hadamard matrix; *Q* = H/√n. *Gate*: one value a·u + b·v from two earlier values, any coefficients (the classical count; OpenAI's count charges a scaling separately, which changes constants only). *Monomial* matrix: one non-zero entry in each row and column (a relabelling with scalings; costs at most n). *Weight* |y|: number of 1 bits of y. *Flag*: a chain of subspaces of the bit vectors, 0 < W_1 < W_2 < ... < W_k, one dimension at a time. *Level* of y in a flag: the first W_j that contains y.

## The one thing to take away

The floor note says a linear program needs cheap steps that move every pair's diagonal, and that every such step found so far is the textbook butterfly in disguise. **There is a whole class of such steps that is not a butterfly: the flag step (idea 1).** One flag step costs about 3n gates whatever k is, has a dense kernel at every scale, mixes all digit columns, and moves the diagonal of every pair of columns when the flag is in general position [derived]. The textbook is "k flag steps, each using one level of its flag". The 7-gate program for 4 points (idea 7) is "one flag step using two levels". The question "how few flag steps make the transform" is a finite, exact, searchable question, and at 16 points it has answers that exist only at the transform's own point of the K_t family (idea 2). Plain products of such steps need 1, 2, 2, 3 of them at k = 2, 3, 4, 5 (exhaustive), which is k/2 and no better; I did not look beyond plain products.

## Ideas

### 1. Flag steps: the cheap move that reaches every scale [ran + derived]

**Construction.** Up to free diagonal phases the transform is the convolution with kernel (−i)^|x⊕x'| [read: task; derived again: (−1)^(x·x') = i^|x| · i^|x'| · (−i)^|x⊕x'|], and the spectrum of that convolution is a constant times i^|y| [derived]. (Whether the exponent is |y| or −|y| modulo 4 makes no difference to what follows.) Take a flag. Let E_j be "keep the part of the data whose frequencies lie in W_j"; in the address order adapted to the flag this is "replace each entry by the average of its block of 2^(k−j) entries". An operator T = Σ_j c_j E_j has a spectrum that depends only on the level of y. All block sums cost n − 1 additions (a tree). Going back down, R_j(block) = R_(j−1)(parent block) + c_j · sum(block), one gate per block: 2n − 2 gates. So **any operator whose spectrum is a function of the level in one flag costs at most 3n − 3 gates**, for every k [derived]. Its kernel is dense, and its relabelling mixes columns freely.

So: **the transform costs about 3·r·n gates if i^|y| is a product of r functions, each depending only on the level of y in its own flag.** Taking logarithms: find r flags and functions h_m with h_1(level_1(y)) + ... + h_r(level_r(y)) = |y| modulo 4. Textbook: r = k.

**What I ran** [ran: `flags.py` → `flags.out`, 17 s; exhaustive over all flags at k = 2, 3, 4].
- k = 2 (3 flags): one flag is enough: 0 < {00, 11} < everything. This is the 7-gate 4-point program.
- k = 3 (21 flags): one flag never; two flags: 24 pairs of 210. Example: 0 < {0,5} < {0,3,5,6} (the even-weight plane) with 0 < {0,7} < {0,1,6,7}.
- k = 4 (315 flags): one flag never; two flags: **54 pairs of 49,455**.
- k = 5 (9,765 flags): two flags never. Exhaustive up to permuting the bits: 15,379,875 pairs, 34 s [ran: `flags5.py` → `flags5.out`; the same code finds the 16-point solutions, `flags4check.out`]. Three flags work (pair, pair, single bit).

So the least number of flag steps is 1, 2, 2, 3 for k = 2, 3, 4, 5: the same count as "pair the bits" (k/2 rounded up), no better. At 3n gates per flag step that is 1.5·n·k, worse than the textbook's n·k; the 7-gate program is cheaper only because at 4 points two of its three terms merge into a relabelling.

**What it taught, and the mutation.** A product of flag steps of the convolution kind is commutative: everything is decided on the spectrum, the sizes of the factors' spectra must cancel separately from their phases, so every factor may as well be unitary, and a unitary flag step is local in its own tree distance (anomaly 10). That is a reason for "about k/2", and it says what to drop: commutativity. Mutate once: put arbitrary diagonal matrices (n free numbers each, cost n) between flag steps, or use the larger cheap class "any operator diagonal in the Haar basis of a flag" (n free numbers, about 4n gates) [derived]. Then the product is no longer commutative and the count of unknowns is r·n. Smallest program of that kind: 8 points, D_0 · T · D_1 · T' · D_2 with one flag used twice. Not run.

### 2. Identities that exist only at the transform's own point [ran]

Of the 54 two-flag solutions at 16 points, **27 solve |y| exactly** (they serve every member of the K_t family at once and are the "pair the bits" programs: 3 pairings × 3 × 3 inner choices [derived]) **and 27 solve it only modulo 4** [ran: `flags.out`]. The second kind is an identity for t = ±i alone. Example: flag A = 0 < {e1+e3} < span(e1, e3) < {y0 = y2}; flag B = 0 < {e0} < span(e0, e2) < {y1 = y3}. Each uses all four of its levels; neither is a tensor product of smaller programs.

Why it matters for the method: every construction so far treated the transform as a tensor power, which is a property of the whole family. This is the first place tonight where the special point t = −i (where i^4 = 1 wraps the weight around) buys identities the family does not have. Seed: classify these 27, find their shape at 64 points, and ask what replaces "modulo 4" for a kernel on m-bit digits.

### 3. Chains of codes in phase space [derived; not run]

A flag of frequencies is one kind of chain. The general kind: a chain of nested stabilizer codes (in the dictionary of `v-imports.md`: the free maps are the Hadamard-free Clifford group, so the natural objects are isotropic subspaces of the 2k-dimensional phase space). A "chain step" Σ_j c_j P_j, with P_j the projector on the j-th code, should again cost O(n) because the space halves at each level [guess, with the frequency case as proof of concept]. Position-diagonal matrices and flag convolutions are the two extreme cases. The search space is then pairs or triples of chains of codes at 8 and 16 points. The necessary condition for one chain step at 8 points is easy to state: some monomial M makes M·Q have eigenvalue multiplicities 4, 2, 1, 1; the trace bound of idea 7 allows multiplicity up to 5 at 8 points, so it is not excluded. Not run.

### 4. All the "volume" in one diagonal: the transform is the subset-sum transform in disguise [ran + derived]

**Construction.** Let Z be the subset-sum matrix (entry 1 when T ⊆ S; the tensor power of [[1,0],[1,1]]). Then exactly
- H = Z · D · Zᵀ with D = diag((−2)^|T|) [ran: k = 1..6, `play.out` part A];
- H · Zᵀ = Zᵀ · (complement relabelling × 2^|S|): the transform is *similar to a monomial matrix* through Z [ran: k = 1..6];
- Z = d_1 H d_2 H d_3 H d_4 with product-form diagonals (2×2 check, hence every k) [ran].

So the transform has a linear-size program **if and only if** the subset-sum transform has one, up to a factor 3 and O(n) scalings [derived]. Morgenstern's determinant, (n/2)·log2 n bits, sits entirely in the one diagonal D: n scalings, no additions. What is left, Z, is a 0/1 triangular matrix with determinant 1. Its own volume (product of its singular values above 1) is only **0.277·√k bits per entry** against k/2 for H [ran: k = 4 … 4096, the constant settles at 0.2769].

**Why it is a door.** The bounded-coefficient bound says nothing about the normalised transform Q at all (all singular values 1), and says only n·√(log n) about Z. So "the cheapest way to manufacture the determinant with O(n) gates" has a plain answer: n scalings; the determinant was never the obstruction. And the subset-sum transform is a different object to think about: prefix sums along a chain cost O(n) with subtraction; the Boolean lattice is a union of about n/√k symmetric chains. First program to write: subset sums on 16 points in fewer than 32 additions, subtraction allowed.

### 5. The diagonal is a self-dual code [ran + derived]

**Pretty fact.** The witness of the floor theorem, "the data where two digit columns agree", is the indicator of the code {(u, u)}, which is its own dual. The indicator of *any* self-dual code is an eigenvector of H with exactly √n non-zero entries, the fewest possible [ran: `codes.out`: the diagonal at 16 and 64 points, and the extended Hamming code of length 8 at 256 points]. That last code is the one under the E8 lattice. [guess] This is why an E8 family could work "where nothing said it should": self-dual codes are exactly the minimal eigen-shapes of the transform, and the diagonal is merely the smallest of them.

**Construction.** For a code C contained in its dual, of dimension j: the functions supported on the dual and constant along C form an invariant space of dimension n/4^j on which H acts as 2^j times the transform of size n/4^j [ran at k = 6, j = 2]. The full splitting gives H = B · (relabelling ⊗ smaller transform) · B⁻¹ with B a transform over C on each coset. Price identity: t(k) ≤ 2·t(j) + t(k − 2j) per entry [derived].

**What it taught.** Two-sided identities (B on the left, B⁻¹ on the right) always pay twice, so they tie with the textbook exactly; the floor theorem is the statement that the diagonal code is kept by every cheap step. Mutation: replace the single code by a *chain* C_1 < C_2 < ... (this is idea 3), or look for a one-sided identity: a cheap B whose image basis H·B is again cheap. For bases of stabilizer states, "cheap" on both sides is exactly what a flag-like, many-scale basis could offer and a single-scale one cannot.

### 6. In the total-spin basis the transform is almost free [ran + derived]

Every matrix M⊗M⊗...⊗M commutes with permuting the bits, so in the basis that splits the data by total spin it falls into small blocks of size k − 2j + 1. Applying those blocks densely costs **1.60·√k per entry** against the textbook's k [ran: `play.out` part C; 6.5 at k = 16, 51 at k = 1024]. On the antisymmetric part of two bits H⊗H is the plain number −2 [ran]. The whole cost is the basis change, and the basis change does not depend on M.

Two things follow. (a) [derived] Blocks applied to the antisymmetric half of an array (with respect to swapping two columns) are invisible to the floor's potential: that half is zero on diagonal inputs, so the floor's weight must be paid on the symmetric half alone. This is the "blocks only where the data is known to vanish" hatch with a concrete carrier. (b) Built bit by bit or by halving, the basis change costs Θ(k) per entry, because per-entry cost adds up over tensor factors [derived; I fell into this twice]. So the lesson is sharp: **what must be beaten is "cost adds over tensor factors", and the transform itself is not where the cost lives.** The same √k appears in idea 4's volume count. [guess] The two are the same fact: the typical spin block has size √k.

Smallest program: at 16 points, do H on four bits through the spin basis and count gates against 32. Not run.

### 7. Monomial plus low rank: 7 gates at 4 points, and exactly how far that goes [ran + derived]

H_4 = u·vᵀ + 2·(a relabelling with signs), u = v = (1, 1, 1, −1): one sum of four, then one gate per output: **7 gates instead of 8** [ran]. (I believe this is the known non-rigidity trick behind the 7/8 and 23/24 constants in the literature [guess from memory; not re-read today].)

How far can "relabelling + low rank" go? [derived] For any monomial M with unit entries, trace(M⁻¹Q) ≤ √n, so the eigenvalue 1 of M⁻¹Q has multiplicity at most (n + √n)/2, hence **rank(Q − M) ≥ (n − √n)/2**. The tensor powers of the 4-point relabelling meet this exactly: ranks 1, 6, 28 at n = 4, 16, 64 [ran]. So 4 points is the only size where the remainder has rank one, and the best possible remainder is always about half the space. Mutation: stop asking the remainder to be low rank, ask it to be *nested* (a chain of projectors, rank n/2, n/4, ...): that is the flag step again, reached from the other side.

### 8. Coefficients that grow by design: the entropy potential stops counting [ran, floating point]

The only potential argument known for the normalised transform (Ailon's: rows as probability vectors, at most 2 bits moved per rotation) assumes well-conditioned gates [from the task's summary and my memory; those files were not read today]. I measured the same potential in its signed form for arbitrary row operations [ran: `play.out` part D, random search, floats]:
- coefficients ±1 only, 3 wires, 8 gates: 22.8 bits (the 3-wire maximum for an orthogonal matrix is 4.75);
- coefficients up to 8, 3 wires, 4 gates: 17.8 bits; up to 64: 826 bits; 4 wires, 4 gates, up to 64: 6,345 bits.

So one ill-conditioned gate can move hundreds of bits; the potential is not even bounded by its final value. In the program H = Z·D·Zᵀ the potential is exactly 0 through the first two factors (a triangular matrix has potential 0 [derived]) and all n·log2 n bits arrive in the last one. Construction to start on: a 3-wire, 4-gate example solved by hand, to see which shape of gate carries many bits, then ask for a family whose jump per gate grows like log n while the coefficients stay polynomial.

### 9. The nearest problem with an honest n·log n theorem, and what it uses [derived; not run]

Tile the phase plane with boxes of area n (Walsh wave packets: the standard basis is tall thin boxes, the Walsh basis short wide ones, Haar a mix). Every tiling is an orthonormal basis; one butterfly re-cuts two adjacent boxes. The sum over boxes of log2(width) goes from 0 to n·k, and one butterfly adds at most 2. Hence at least (n/2)·k butterflies: the textbook, exactly. Every symmetric tiling gives a textbook-cost program, so there is a large family of ties, which is what the night kept finding.

The proof uses three things: the intermediate data are coefficients in an orthonormal basis; that basis consists of single boxes; a gate touches two boxes. Flag steps violate the second and third (a block sum is not a box coefficient of the current basis, and the downward pass reuses each sum at every finer scale); idea 8 violates the first. This is the cleanest map I have of where to dig.

### 10. Two factors, each almost of rank one [derived; not run]

In the K_t family K_s·K_t = (1 + st)^k·K_((s+t)/(1+st)), and t = ±1 are the two rank-one members (cost n − 1 additions). Writing t = tanh φ, the transform is φ = iπ/4, and φ = (R + iπ/4) + (−R) for every R: **the transform is the product of two members that are both exponentially close to rank one**, one near t = 1 on the unit circle and one near t = −1 on the real line. Each is a polynomial in its small distance ε from rank one whose term of order w is the weight-w part of the spectrum. The weight ≤ w part of the Walsh spectrum costs about 2·w·n by a tree, not k·n [derived: merging two blocks of j bits costs C(j, ≤ w) additions]. Smallest program: at 16 and 64 points, split the spectrum into the cheap ends (weights near 0 and near k) and the middle, and see what the middle looks like in the block-sum basis of a flag.

### What the other hypotheses gave when broken [derived]

- **One batched call for several arrays.** A linear map cannot serve W independent arrays with fewer than W independent calls unless the arrays sit in subspaces whose images can be told apart cheaply. The only cheap instance is "known zeros": H of size W·n is H_W ⊗ H_n, so one big call equals W small calls plus n·W·log W gates. That is the tensor identity, not a saving. The mutation that survives is idea 5: a smaller transform rides inside the big one on the functions living on (dual of C)/C.
- **A unit whose shape changes with n.** The flag step is such a unit: it contains blocks of every size at once, at geometrically falling cost.

## Anomalies and pretty facts

1. The floor theorem's diagonal is a self-dual code, and self-dual codes are the eigenvectors of the transform with the fewest non-zeros (√n) [ran].
2. At 16 points exactly half of the two-flag identities (27 of 54) hold only modulo 4, that is, only at t = ±i [ran].
3. The subset-sum matrix conjugates the transform into a relabelling with scalings: H·Zᵀ = Zᵀ·(complement × 2^|S|) [ran].
4. √k appears twice from unrelated counts: leftover volume of the subset-sum transform (0.277·√k bits per entry) and the dense cost of the transform in the spin basis (1.60·√k per entry) [ran].
5. rank(Q − M) ≥ (n − √n)/2 for every monomial M, met exactly at 4, 16, 64 points; 4 points is the only size with remainder of rank one [derived + ran].
6. With coefficients ±1 only, 8 row operations on 3 wires reach a signed entropy of 22.8 bits; the orthogonal maximum is 4.75 [ran, floats].
7. A triangular matrix has entropy potential exactly 0, so in H = Z·D·Zᵀ the whole potential arrives in the last third of the program [derived].
8. The transform is the product of two operators each exponentially close to rank one, for every choice of the rapidity R [derived].
9. On the antisymmetric part of two bits the transform is the number −2; in the spin basis it is a scalar on a share 2.2e-2 of the space at k = 16 and 4.9e-5 at k = 1024 [ran].
10. A unitary flag step is local in its own tree distance: the weight of its kernel at distance δ is at most 8·2^(−δ) [derived]. Reaching far needs non-unitary steps, which is where ideas 4 and 8 point.

## Not done, and limits of what was done

- The flag search covers plain products of convolution-type flag steps only: one flag at k ≤ 4, two flags at k ≤ 5, both exhaustive. Three flags at k = 6 or 7 were not searched.
- Diagonals between flag steps, Haar-diagonal steps, sums of products, and chains of codes were not run at all. These are the mutations the search points to.
- The symmetry cut in `flags5.py` (first flag's smallest subspace taken as one representative per Hamming weight) is my own argument; the 16-point re-run shows the code finds solutions, not that the cut is right.
- Part D of `play.py` is floating point and a random search; its numbers are lower bounds on what a few gates can do.
- The cost claims for flag steps (3n − 3 gates) and for the weight ≤ w spectrum are derived, not implemented.
- The claim "linear for H iff linear for subset sums" rests on three exact identities that I ran; the cost bookkeeping around them is mine alone.
- I read `NOTE.md` and `f-break.md` of wht38/floor in full and `f-model.md` by search; the wht37 and wht33 files were used only through the task's summary.
- What I recall of the literature (the 7/8 and 23/24 constants, Ailon's potential, the n·√(log n) reading of the volume bound for triangular 0/1 matrices) is from memory, not checked today.
