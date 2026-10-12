# j-failproof: try to prove the lower bound, and keep what breaks each proof

Move: the dual of looking for an algorithm. I tried, by several standard methods, to prove that the transform on
N = 2^k points needs more than c*N gates when coefficients are unbounded. Each proof stops at a precise object.
That object is a blueprint for a cheap program, so I wrote it down and built its smallest instance.

Two gate counts are used and named each time. **(G)**: a gate is any a*u + b*v, scalings free, outputs needed up to scaling.
**(O)**: OpenAI's count, every addition or subtraction costs 1 and every multiplication by a constant costs 1.
Marks: [read] [ran] [derived] [guess]. Programs and outputs: `j-failproof/` (`min4.py`, `lu_orders.py`, `shears4.py`, `*.out`).
Private notes, nothing in Lean, nothing published. Time box 40 minutes.

Picture used throughout [derived; the first wave has it too, d-5.md section 1]: a vector up to scaling is a point of
projective space; the N inputs are the N coordinate points; **a gate puts a new point on the line through two points already held**.
Count (G) is the number of points added until the N "Hadamard points" (rows of H) are all there.

## 1. What is now settled about the true minimum at small sizes

| size | count (G) | count (O) |
|---|---|---|
| 4 points | **exactly 7** [derived by hand, all coefficients; ran: `g6.out` none with 6, `g7.out` 228 gate sets with 7] | **exactly 8** [ran, exhaustive: `o7.out`, `p7.out`; derived step below] |
| 8 points | between **15** and 22 [15: derived below; 22: read, first wave] | between 15 and 24 |
| N points | at least **2N - 1** for every N >= 4 [derived] | at least 2N - 1 |

- **(O) at 4 points is 8, the textbook, and I can say why.** A program of cost 7 in (O) would be a (G) program with at most
  7 gates; (G) needs 7, so all 7 operations would be additions or subtractions with no scaling anywhere. The search over every
  such program (vectors up to sign, so negation is given away free) finds none, both when the outputs must be the rows
  themselves and when each output may be any multiple of its row [ran: finite and complete]. With 8 there are exactly the three
  textbook pairings. So the 7-gate program is real only because one of its coefficients is 2 = sqrt(N); (O) charges that
  scaling and the total returns to 8. The normalised (orthogonal) transform H/2 also costs exactly 8 in (O): 7 additions and
  ONE halving placed on the hub. The first wave had not priced the 7 gates in (O) (i-cousins.md line 93).
- **2N - 1 in (G)** [derived]. The first gate whose support is all N inputs needs N - 1 gates in its cone, N - 2 of them with
  smaller support, so not outputs: 2N - 2 at least. Suppose exactly N - 2 helpers. Then they form a binary tree over the inputs
  and each helper is the first output y restricted to the leaves below it. Another output y' differs from y in sign on exactly
  half the inputs, a set D. Checking every line through two held points: y' is one gate away only if D (or its complement) is a
  subtree, there is at most one such y', and after it no third output is one gate away. So three outputs need N - 1 helpers.
  At 4 points this is tight. At 8 points it gives 15 against the known 22: **nobody knows the 8-point minimum to within 7 gates.**

## 2. Six proofs, and the object that stops each

**P1. Volume (Morgenstern).** det H = N^(N/2); a gate a*u + b*v multiplies the largest sub-determinant by at most |a| + |b|.
So s gates need |a| + |b| >= N^(1/(2c)) somewhere if s = c*N [derived]. The coefficients need not be astronomically large:
at N = 2^20 and c = 5 a factor 4 is enough, as far as this proof can see.
Sharper [derived]: in the **in-place** model whose moves are w_i <- w_i +- w_j (determinant 1) and w_i <- 2*w_i, any program
needs at least (N/2)*log2(N) doublings, because that is the power of two in det H (true even if the shears may use any
rational coefficient); the textbook uses one doubling per butterfly, so it is optimal there. That is an honest n log n theorem, and it names its own two exits:
(a) one scaling that carries more than a factor 2 (a single layer of sqrt(N) on N wires pays the whole determinant);
(b) copy a value and later forget a wire (then the determinant is paid by forgetting, which costs nothing).
*Object:* a program for the orthogonal matrix U = H/sqrt(N) made only of determinant-1 moves ("volume-free"). See idea 2.

**P2. Entropy (Ailon's potential).** Potential of an invertible matrix M: the entropy of the table L = M o M^(-T) (entry by
entry product of M with its inverse transpose; rows and columns of L sum to 1). Identity: 0. H: N*log2(N). A 2x2 rotation moves
at most 2 bits, hence n log n for rotation programs [read, from memory of Ailon 2013; i-hatch.md measured the signed version].
Where it stops [derived]: the potential is blind to every scaling, every relabelling and **every triangular matrix** (for
triangular M the table L is the identity). In H = Z D Z^T (Z = subset sums, D diagonal) the first two factors carry zero
potential and all N*log2(N) bits arrive in the last (N/2)*log2(N) gates: 2 bits per gate, twice a rotation's rate per gate.
*Object:* a single move w_i <- w_i + c*w_j delivering about log N bits, which needs rows i, j whose entries in L are large with
both signs (a row and its dual row nearly perpendicular before cancellation). See idea 3.

**P3. Counting helpers (the 2N - 1 proof pushed further).** To go beyond 2N - 1 one wants "each extra helper enables at most
two more outputs", which would give 2.5N - 3 (7 at 4 points, 17 at 8) [guess]. Measured at 8 points [ran, sample, `hubcap8.out`]:
125 random trees under the first output, 141,204 candidate extra helpers (any point a*u + b*v on two held points, ratio from ten
values): one extra helper brought 0 outputs 140,607 times, 1 output 546 times, 2 outputs 51 times, never 3. The best ones are
hubs again: y0 with two entries flipped, built from y0 and a pair already in the tree. It stops at a **hub**: one helper r that is one gate
away from many outputs. At 4 points the hub is r = (1,-1,-1,-1), with y = r + 2*e_i for three outputs and y0 = -r + 2*e_0.
All 228 seven-gate sets found contain such a point [ran]. What limits a hub [derived]: r one gate from output y_w means
y_w - c*r is something already held, of support at least the number of places where r and y_w disagree; and one vector cannot
agree with many characters at once (Parseval: the squared correlations sum to 1; unbounded entries do not help, the agreement
sets of different magnitudes are disjoint). So a hub's partners are big and are themselves "an output restricted to a piece".
*Object:* cheap ways to make an output restricted to a piece that is not a subcube. See idea 1.

**P4. Restriction.** Set half the inputs to zero: the program becomes one for N/2 points with each output twice. The proof
wants "two disjoint half-size programs survive" (T(N) >= 2T(N/2) + N) and only gets "one survives" (T(N) >= T(N/2) + N/2, linear).
*Object:* gates doing double duty: the low half and the high half of one gate are helpers of two half-size programs at
DIFFERENT stages. In the hub program at 4 points the chain x0-x1, x0-x1-x2, x0-x1-x2-x3 has its low half already final while its
high half walks through all stages [derived]. In the textbook both halves are always at the same stage.

**P5. Cuts and connectivity.** A circuit needs rank(H[R,C]) disjoint paths from inputs C to outputs R; linear-size graphs with
all such paths exist (superconcentrators), so this proves nothing. The property connectivity lacks is **coincidence**: half of
all 2x2 minors of H vanish (rows w, w', columns x, x' with (w+w').(x+x') even), and already in the textbook almost none of these
zeros is forced by the graph (two disjoint paths exist; the determinant vanishes because coefficients agree) [derived].
A linear program must satisfy about N^2 equations with c*N free coefficients. Only symmetry does that. See idea 5.

**P6. Rank / rigidity.** "H is far from low rank, so it is expensive" stops because H is not rigid [read, lit-lower-bounds.md].
Its smallest instance IS the 7-gate program: H_4 = 2*(signed relabelling) - (rank one), cost 3 + 4 [derived].
The same form with rank (N - sqrt N)/2 costs N times the rank and is useless beyond 4 points; P3 says why (Parseval).

**P7. Triangular factorisation.** "H = L*U needs dense L, U" is true and proves nothing, since a dense triangular matrix can be cheap.
Played anyway [ran, `lu*.out`, exact]: over re-orderings of rows and columns, 4 points: all 388 admissible orders give exactly 9 + 9
non-zeros; 8 points: 786 admissible orders, never below 27 + 27, the subset-sum order; pivots always powers of two; 16 points: 599
of 600 random orders hit a vanishing leading minor. So H = Z D Z^T is, as far as seen, the sparsest triangular sandwich.

## 3. Ideas (constructions to start on)

**1. Pieces that are not subcubes.** Every helper in a shortest program is forced to be "an output restricted to a set of
inputs" (proof of 2N - 1). The textbook only ever restricts to subcubes. The 4-point hub restricts to "everything except one
point": r = y0 with one entry flipped, and it is at the same time y1, y2, y3 with one entry flipped. Build the calculus: nodes are
piecewise characters (sum over pieces S_j of c_j * y_{w_j} on S_j); a gate joins two; allowed pieces are complements of points,
quadrics, Hamming balls. *Tried:* derived the 2N - 1 theorem and the hub's Parseval limit; at 4 points all 228 optimal sets pass through
the flipped-point vector. *Next:* the same exact search at 8 points with helpers restricted to piecewise characters (a finite set).

**2. The volume-free program.** Pay the whole determinant with one layer of sqrt(N), then compute U = H/sqrt(N) by moves of
determinant 1 only: U (with spare wires that start and end at zero) as a product of O(N) shears w_i <- w_i + c*w_j, c any
rational. Copy-and-forget programs convert to this form at a constant factor [derived sketch: compute into spare wires, clear the
inputs with the transposed program, uncompute]. This is the "length of a matrix in elementary generators", studied for rings
(for 2x2 matrices over Z[1/p] five elementary factors always suffice, because coefficients may be huge [read, from memory:
Vsemirnov 2014]); nobody asks it for sparse length at fixed matrices. *Tried* [ran, `shears4.out`]: at 4 points a 9-shear program
for H/2 (replayed exactly); none with 6 or fewer for c in {+-1, +-2, +-1/2} (`shears4b.out`), so 7, 8 or 9 there, against 7 gates with copying.
*Next:* exact shortest shear word for H_4/2, then H_16/4 (the first size where a non-product word could show).

**3. Potential-blind moves first, then few rich moves.** Scalings, relabellings and triangular matrices cost Ailon's potential
nothing. Arrange the program as (blind block)(short rich block)(blind block)...: use running sums and triangular solves to
reach a state where single shears deliver many bits each. *Tried:* derived the blindness; measured the triangular sandwich over
orderings (P7): it is rigid at 4 and 8 points, so the gain cannot come from re-ordering one sandwich. *Mutation:* three or more
triangular factors, each a running sum along a different ordering (cost N - 1, dense); the hub r is exactly a running sum.

**4. Two simplexes in perspective.** The 7 gates exist because the coordinate tetrahedron and the Hadamard tetrahedron are in
perspective from a point: the four lines e_i -> y_pi(i) meet in r. There are four such centres, the vertices of a third
tetrahedron (the four +-1 vectors with an odd number of minus signs): the classical desmic triple, the 24-cell [derived; the
name from memory]. H_4 = 2*(Householder reflection in r)*(signed relabelling). At N >= 8 **no two of the N^2 lines from an
input point to an output point meet** [derived: a common point would have support <= 2 in both bases, and the product of the
two supports is at least N]. *Mutation:* perspective from a small flat instead of a point, or through a third FRAME: at 8 points
find the cheapest program inside the 240 real stabiliser states (three-term relations only), a finite search by integer programming.

**5. Circuits that are unions of orbits, with orbit-stabiliser accounting.** The proofs P5 and P3 both end at symmetry. Demand
that the SET of points of the program be invariant under a group Gamma acting on inputs and outputs. Then
gates = sum over orbits of |Gamma| / |stabiliser|, and a program is described by one rule per orbit.
*Tried, and it died at 8 points, usefully* [derived]: Gamma = the Singer cycle (multiplication by a generator of the field with
8 elements, order 7, prime, so no subgroups). Every helper orbit has 7 points and one support size; two orbits reach support 4
at most and cannot build the sum of the seven non-zero inputs (the two 4-sets overlap in one point and the coefficients cannot be
made to agree there), so such a program needs three helper orbits: at least 29 gates against the known 22. The count 22 = 8 + 2*7 is
numerology. *What it taught:* the tree under the first output has log2 N different support sizes, so a linear invariant
program needs helpers whose stabiliser grows in proportion to their support (orbit of a helper of support s has about N/s points).
For translations that is the textbook with one change: on each coset of a subgroup of size 2^j the textbook keeps all 2^j sign
patterns, and a linear program may keep only a summable fraction of them. For the multiplicative group it is sums over cosets of
multiplicative subgroups (Gaussian periods, Rader's form), which needs N - 1 to have many divisors. *Next:* at 16 points
(N - 1 = 15 = 3*5) count the cheapest program invariant under the cycle of order 15 whose helpers are sums over cosets of the
subgroups of orders 3 and 5; my rough count gives more than 56 [guess], so the group to try is the one generated by
translations AND a cycle.

**6. Double duty by a staircase.** From P4: pair helper i of one half-size program with helper pi(i) of the other, where pi is
not the identity. Two chains of lengths m and n combined along a staircase cost m + n, not m*n. *Tried:* read the 4-point hub
this way (low half final, high half walking). [guess] for more than chains.

**7. Push the helper count: is 22 optimal at 8 points?** The 2N - 1 argument is a finite case analysis on lines; one more
round (exactly N - 1 helpers: a tree plus one free point, or a cone with one input used twice) is a bounded exact search with
one unknown coefficient. A proof of 16, 17, ... at 8 points shows which configuration is the first to resist, and that
configuration is the candidate for a program below 22. *Tried:* the first round, by hand (section 1), its key step machine-checked on 800 sampled trees at 8 points and 80 at 16 (`tree8.out`, `tree16.out`: never more than 2 outputs from a bare tree), and the one-extra-helper census above.

**8. In (O), put every scaling on a hub.** At 4 points the normalised transform costs 8 in (O) with one halving serving four
outputs. In (O) a saving must share its scalings; count scalings per output as the currency. *Tried:* the exact (O) minimum at 4 points.

## 4. Anomalies and pretty facts

- (O) at 4 points: 8 for H, 8 for H up to scaling of outputs, 8 for the orthogonal H/2, by two unrelated programs. This is the first
  exact instance of "the count always comes back" (PICKS.md, the 64 at 16 points). The volume bound alone would allow 4.
- Every admissible re-ordering of the 4-point matrix gives a triangular sandwich with exactly 9 + 9 non-zeros.
- The potential that proves n log n for rotations cannot see triangular matrices at all.
- In place, with unit shears and doublings, the textbook's number of doublings is provably optimal.
- In place and without scaling, the 4-point orthogonal transform takes at least 7 shears (for the small coefficient set), 9 found; with one copy it takes 7 gates. Copying is worth up to 2 gates at 4 points.
- The in-place doubling theorem holds even when shears may use ANY rational coefficient: the only thing it charges is the factor 2.
- The hub is at once: the centre of perspective, a bent function, the Householder vector, and the rank-one part of "H is not rigid".

## 5. Limits

A first run of the hub census counted degenerate lines (a helper proportional to a held point) and reported gains of 6 and 7;
that was a bug, the file is kept as `hubcap8.first-run-with-degenerate-lines.out`, and the corrected run is the one quoted.

The 2N - 1 proof and the Singer exclusions are hand derivations of tonight, not re-checked by machine beyond 4 points. "228 sets" and
"no program with 6 shears or fewer" hold for the stated coefficient sets only; the 7-gate census with a wider coefficient set was stopped by the memory cap (`g7w.out`). Ailon, Vsemirnov and the desmic name are from memory. Nothing at 8
points was searched. No web reading was done.
