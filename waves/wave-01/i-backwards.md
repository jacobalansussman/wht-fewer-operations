# i-backwards: read a linear program backwards from the goal

10 October 2026, night. Private play, one agent, 35 minutes. Nothing here is reviewed, nothing is in Lean.
Marks: [read] [ran] [derived] [guess]. Scripts and outputs: `i-backwards/play1.py`, `play1.out`, `play2.py`, `play2.out` (exact integers and fractions, 3 s and 20 s).

Words. N = 2^k points, H the plain ±1 transform. *Wire*: one number inside a program; it is a linear form in the inputs. *Support* of a wire: how many inputs it uses. *Co-support*: how many outputs it is a combination of. *Eigenform*: a wire that the transform only multiplies by ±√N. *Self-dual code*: a subspace V of the addresses with V = V^perp (size √N).

## What a program of size c·N must look like

1. **The big numbers** [derived from Morgenstern as read in lit-lower-bounds.md]. The sum over steps of log2(|a|+|b|) is at least (N/2)·log2 N. With c·N steps the typical coefficient is about N^(1/2c). They can all sit in one place: see idea 1.
2. **The wires** [ran, N = 16]. Every wire of the textbook program has support × co-support = 16 exactly (16 wires each at (1,16), (2,8), (4,4), (8,2), (16,1)). The uncertainty principle says no wire can be below that curve. A program with fewer wires cannot afford k levels on the curve, so it must carry wires above it. The extreme case is an eigenform: it is input-side and output-side at once and needs no further work.
3. **Half the data is enough** [derived]. H = √N·(2·E·C − I), where C maps N numbers to N/2 and E maps them back (C picks coordinates of the +√N part). So the transform always factors through N/2 numbers plus the identity. The half-touch is automatic for the data; the open part is whether C and E can be cheap. The choice of C is free up to any invertible (N/2)×(N/2) matrix.
4. **The graph** [derived, standard]. Any a inputs and b outputs need a·b/N disjoint paths. Linear-size graphs with that property exist and are built as: sparse direct links, plus a squeeze to N/2 wires, the same again inside, and an expansion. That is the shape of item 3.
5. **Sparse system** [derived, standard]. A program with s steps exists exactly when H is a corner block of the inverse of a unit triangular matrix with at most 2 off-diagonal entries per row, of side N + s. Long chains (prefix sums) are allowed and are how dense matrices get linear programs.

## Ten ideas

### 1. All the volume in one diagonal: H = Z · D · Z^T
Z is the subset-sum matrix (Z[y,T] = 1 if T is inside y), D is diagonal with entries (−2)^|T|. [ran, k = 2 and 4: exact; the diagonal carries 32 = (N/2)·log2 N bits at N = 16.] Z has determinant 1 and entries 0/1. So a linear program for subset sums over a ring, used twice around N scalings, is a linear transform. Z = exp(L) with L the "remove one element" operator of the cube, so H = exp(L)·(−2)^count·exp(L^T) [derived].
Tried: the identity; nothing on Z's own cost. Textbook subset sums cost 32 at 16 points.
Start: exact search for a 16-point subset-sum program with subtraction below 32, or 8-point below 12.

### 2. Carry eigenforms: look for a cheap eigenbasis
Linear transform ⇔ linear change to some eigenbasis (cost within a factor 2 either way) [derived]. The eigenbasis is free up to GL(N/2) × GL(N/2).
Tried [ran, N = 16]: eigenvectors of plain H with 4 non-zeros: exactly 6 per sign, all on affine planes with entries ±1. They span 3 of the 8 dimensions per sign. Support 5 adds nothing; support 6 spans everything.
Start: at N = 16 and 64, search bases of the two eigenspaces by program cost, not by sparsity.

### 3. Relabel first: the transform is a reflection through a smaller space
Swapping columns 1 and 2 of H4 gives H4' = 2I − u·u^T, u = (1,−1,−1,−1) [ran]: a Householder reflection. Tensor powers: rank(H' − √N·I) = 6 at N = 16 and 28 at N = 64 [ran], which is N/2 − √N/2. No relabelling and re-signing can go lower [derived: trace of an orthogonal matrix built from H is at most √N].
Tried: 4 points cost 3 additions for u·x and 4 for 2x_i ∓ u·x: 7 with free doubling. In OpenAI's count a scalar multiplication costs one [read], so it is 8 there.
Mutation: allow two non-zeros per row in the sparse part. The known floor on changes at rank N/4 is only about N; nobody I know has measured the truth at 16 points [guess].

### 4. Fill the template "identity plus one projection" at 16 points
H16' = 4I − 8·E·C with C: 16 → 6 and E: 6 → 16 [ran: rank 6].
Tried by hand with the natural basis (contract digit 1, contract digit 2, remove the common part): 12 + 12 + 3 + 8 + 32 = 67 additions, against 56 for two Householder passes and 64 for the textbook. The 32 is the expansion plus the identity.
Start: exact search over the 36-parameter choice of basis for the cheapest (C, E) pair. A total under 56 would be a program that is not a pass per digit.

### 5. A half-dimensional space with sparse checks on which the transform is sparse
Template: H = S + B·M·C, S, B, C with boundedly many entries per row, M of side N/2 and *not* a smaller transform, recursing by the same template. Read backwards: the space Z = {z : Hz = S^T z} has dimension N/2 and is cut out by the sparse rows of B^T, like a low-density code.
Tried: S = √N·(relabelling). Then Z is an eigenspace and its checks are eigenvectors of the other sign. [ran, N = 16 relabelled] the 6-dimensional −4 space has no vector with fewer than 6 non-zeros. The uncertainty principle forces at least √N in general, so this choice dies.
What it taught: S must not be a relabelling. With two entries per row the checks are no longer eigenvectors and the uncertainty bound does not apply in that form. Not run.

### 6. Self-dual codes: in their basis the transform is a transposition
For a self-dual code V, take g(a,b) = (character b) × (indicator of the coset V + a). Then H·g(a,b) = ±√N·g(b,a) [derived; ran for both codes of length 4, all 16 pairs; fixed signs +,−,−,+]. The basis change is √N transforms of size √N.
The "diagonal of two digit columns" in tonight's floor theorem is the self-dual code {(v,v)}, and the floor's potential measures how far data leaves that code's coset states [derived]. The extended Hamming code behind E8 is self-dual [guess: this is why the E8 family worked].
Start: a program that walks through several self-dual codes sharing half their words (each step one layer of two-point sums [guess]). No pair of columns keeps its diagonal along such a walk, which is hatch (b) of the floor note with a map.

### 7. Count passes: z = log2(passes per squaring)
If N points cost a·√N·T(√N) + O(N), then z = log2 a [derived]. Two passes is the textbook; 1.5 gives z = 0.585; one pass gives N·log log N.
Tried: skip the diagonal blocks. With X the √N×√N array, the transform is X − 2·(parts of X that anticommute with the small reflection), which needs only the off-diagonal blocks of X in eigen-coordinates. Counted at 3 where the direct route costs 4. It died in ten minutes: computing one half of the eigen-coordinates costs at least (T − n)/2 by item 3, and in the product basis and the code basis it costs a full pass.
What it taught: the saving needs an eigenbasis whose two halves have separate programs with nothing shared. Mutation: use two different codes for the two sides of X.

### 8. One generator, and the nearest problem I can solve
After relabelling, H' = √N·(−1)^(number of u-digits) [derived]: a function of one operator that is a sum of k/2 local terms. A polynomial in that operator needs degree k/2, which is the textbook again.
Nearest solvable problem: apply the cube's neighbour-sum matrix (N·k non-zeros) in O(N) additions. By hand: the 2-cube costs 2 additions instead of 4 (both even points have the same neighbours); the 3-cube 14 instead of 16 [derived].
Start: exact search for the 4-cube neighbour sum below 48 additions. If it is linear, ask which functions of it are.

### 9. Unbalanced steps: differences and prefix sums as free changes of basis
A program with long chains is a sparse triangular solve (item 5). Prefix sums and differences cost N and have dense matrices.
Tried by hand: H times the difference operator in address order has half its entries zero in every column [derived: columns x and x+1 differ only where the low bits of y have odd parity]. Not run further.
Start: at N = 16, greedy choice of difference and prefix-sum operators on both sides, in several address orders, to minimise the non-zeros left.

### 10. Valiant backwards: cut the diagonal of idea 1 and recurse on what is left
Keep only sets T with at most d elements. The result has low rank and equals H exactly wherever x and y share at most d ones [ran, k = 4]:

| keep up to | rank | entries still wrong (of 256) |
|---|---|---|
| 0 | 1 | 120 |
| 1 | 5 | 67 |
| 2 | 11 | 13 |
| 3 | 15 | 1 |

The remainder depends only on the size of the overlap and lives on heavily overlapping pairs. Inputs and outputs of low weight are finished by the low part alone, so the recursion on the remainder touches only heavy addresses.
Start: at k = 6 and 8, count the work of the low part by subset sums on small sets, and see whether the remainder is the same problem on a smaller cube.

## Anomalies and pretty facts

- H = Z·D·Z^T: Morgenstern's whole volume sits in one diagonal [ran].
- Textbook wires lie exactly on support × co-support = N; Householder wires sit at (4,16) and (16,16) [ran].
- One column swap turns H4 into 2I − u·u^T [ran].
- In H4' every pair of coordinates has a preserved combination: y_a − u_a·u_b·y_b = 2·(x_a − u_a·u_b·x_b) [derived].
- Relabelled H is a reflection through codimension N/2 − √N/2 (6 at 16, 28 at 64), and that is the least any relabelling allows [ran, derived].
- Plain H16 has exactly 12 eigenvectors with 4 non-zeros: the coset states of the three self-dual codes of length 4. They span 6 of 16 dimensions [ran].
- Relabelled H16': the 10-dimensional +4 space is spanned by vectors with 4 non-zeros; the 6-dimensional −4 space has none below 6 [ran].
- In a self-dual code's basis the transform is a signed transposition [ran].
- The floor theorem's diagonal is a self-dual code [derived].
- Half of the eigen-coordinates already costs half a transform [derived].
- The 2-cube's neighbour sum costs 2 additions, not 4 [derived].

## Not done

No search was run for ideas 1, 4, 8, 9; the counts there are by hand. No literature was read tonight; "nobody has measured" in ideas 3 and 8 is my guess. The 60-addition 16-point program was not looked at.
