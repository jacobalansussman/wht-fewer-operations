# af-2 skeptic: the pair-kill theorem holds and prices no gates; the 8-gate circuit's claim (i) holds at every size; its claim (ii) FAILS (the wiring is an identity of the class after all)

11 October 2026, about 07:36 to 07:46 EDT by the run stamps, inside a 30-minute box. Private. One agent; nothing in Lean, nothing published.
Marks: [ran] = my own code tonight, whole numbers or exact fractions (files in `af-2/`); [derived] = by hand tonight;
[read] = from the reports under attack or from a web search summary (said which); [guess].
Gate count: **(G)**, a gate is any a*u + b*v with scalings free. Count (O) is not used.

**For the user's bar: nothing. No circuit size, no saving exponent, nothing about linear size.** The theorem is a correct
lower bound on a count that is not gates. The one thing that changes tonight's picture is negative: the "first circuit
that uses something the class does not have" does not exist; that 8-gate wiring works for every kernel.

## Words

N = 2^k points; an address is k bits. A *flat* is a subspace of the address space or a shifted copy; a *signed flat* is
the function that is +1 or -1 on a flat by a sign (-1)^(b.z) and 0 off it. *Quadric signs* g: -1 where
z1 z2 + z3 z4 + ... = 1 (k even). *Flat rank* r_s(k): the least number of signed flats whose combination with rational
coefficients is g. B(u, z) = z1 u2 + z2 u1 + ... is the pairing that goes with g; *perpendicular* means B = 0; a
*Lagrangian* is a subspace of k/2 bits perpendicular to itself. *Doubled class*: read the N x N matrix H(x, y) = (-1)^(x.y)
as a function of the 2k bits (x, y). *Kernel*: a 2 x 2 matrix with rows K1 = (p, q), K2 = (r, s); its *square* is the
4 x 4 matrix with rows K1xK1, K1xK2, K2xK1, K2xK2 (the transform is the kernel 1, 1, 1, -1). *Repeat* (ad-7): a gate
whose value modulo 2 equals an earlier wire.

## 1. The claims, stated exactly

- **T (ad-4, section 2).** For even k >= 4, r_s(k) >= r_s(k - 2) + 2, hence r_s(k) >= k. Proof shape: in any
  decomposition with at least 3 flats, either two flats vanish together on a set W cut out by two parity conditions
  (Lemma A), or the same happens after transforming every term (Lemma B), or every flat is a shift of one Lagrangian
  and then at least 2^(k/2) are needed to cover the space.
- **D (the step).** H_N is not a combination of fewer than 2 log2 N signed flats of the doubled space.
- **(i) (ae-cross).** The 4-point transform has a circuit of 8 gates with coefficients +1, -2 and 3 repeats, so ad-7's
  guess "a halving-free circuit with coefficients +-1, +-2 has at least (N/2) log2 N repeats" is false as stated.
- **(ii) (ae-cross).** That wiring, with every coefficient free, computes the square of a kernel exactly when
  p s + q r = 0, so it serves the transform and no other member of the class.

## 2. Verdicts in one table

| claim | verdict | how I checked |
|---|---|---|
| T, pair-kill | **holds** | proof re-derived line by line; its case analysis machine-checked over ALL subspaces at k = 2, 4, 6; 16 points re-done exhaustively with my own program |
| D, 2 log2 N in the doubled class | **holds for H itself; false for H up to free row and column signs** (smallest case: 4 points, 2 flats) | relabelling checked; the brick checked |
| (i) 8 gates, 3 repeats | **holds, and at every size**: a family with exactly N - 1 repeats | exact circuits at 4 to 128 points |
| (ii) not an identity of the class | **FAILS** | the same wiring computes the square of every kernel with p, q, r non-zero; explicit coefficients, 414 kernels |

## 3. The pair-kill theorem  [derived + ran]

I rebuilt the proof and found no gap. The three places where it could have broken:

1. *Lemma A, "the restriction is in the same class".* W is a shift of the set perpendicular to u1 and u2; B(u1, u2) = 1
   makes that set non-degenerate, so g on W is again a bent quadratic sign pattern on k - 2 bits. There are two types of
   such forms (z1 z2 and z1 + z2 + z1 z2), but as sign patterns they differ by a shift and a global sign, so the flat
   rank is the same. [ran] All 480 restrictions at k = 4, all 8,064 at k = 6, 600 sampled at k = 8: bent and quadratic
   every time. A flat restricted to W is a flat or empty, and nothing in the argument needs the survivors to stay distinct.
2. *Lemma B, the twin.* The transform of the signed flat (a + V, sign b) is |V| times the signed flat (b + ordinary
   perpendicular of V, sign a). [ran] All 17,152 (subspace, shift, sign) triples at k = 4; 4,000 sampled at k = 6. With
   J = "swap the two bits of each pair", the transformed flat's perpendicular is J V, and J V_i is perpendicular to J V_j
   exactly when V_i is perpendicular to V_j. So the twin condition is the one ad-4 states. [derived]
3. *The exceptional case.* It is cleaner than written. [ran, exhaustive over all 5, 67, 2,825 subspaces at k = 2, 4, 6,
   every pair including a subspace with itself] **A pair of flats escapes both lemmas exactly when the direction of one
   is the perpendicular of the direction of the other** (0 exceptions in 4, 41, 1,480 escaping pairs). Three flats that
   escape pairwise are therefore three copies of one Lagrangian: 3, 15, 135 such triples, which is the number of
   Lagrangians. The covering count 2^(k/2) then applies. [derived] The two side conditions are fine: r >= 3 at k >= 4
   (with 2 flats, one lies in a half-space and g would be a single signed flat on the other half, which needs
   k - 1 <= k/2), and r_s(k - 2) + 2 <= 2^(k/2 - 1) + 2 <= 2^(k/2) from k = 4 on.

Independent of the proof [ran, `exh4.c`, whole-number Gram determinants]: at 16 points, 67 subspaces, 1,072 signed
flats; 0 of 574,056 pairs and 0 of 10,251,120 covering triples span g (480 of the triples are linearly dependent and
fall under the pair test). Controls: the same program finds 145 triples for a target made of 3 flats and 1 pair for a
target made of 2. The same counts as ad-4's `exh4.out`. So r_s(4) = 4 exactly.
Upper bounds re-run with my own search [ran]: 4 unsigned flats at 16 points; 11 at 256 points (8 alternating 4 x 4
matrices with invertible differences, identity checked on all 256 entries).

**Growth law of the flat rank: at least k, at most 2^(0.4324 k). Polynomial or exponential is open, and I did not
narrow it.** The method cannot do better than +2 per two bits: ad-4's own run shows decompositions where no
restriction kills more than two flats, and the sharp form above says why (the escaping pairs are a matching, so one
restriction is spent on one pair).

## 4. The step to the doubled class  [ran + derived]

The step is a relabelling: H(x, y) = (-1)^(x1 y1 + ... + xk yk) is the quadric on 2k bits with the pairs (x_i, y_i)
[ran at 4 points; true by inspection at every size]. 2k is always even, so T gives 2 log2 N for every N. **D holds.**
What it is worth:

- In count (G) rows and columns may be rescaled for nothing, and then D is false at the smallest size. [ran]
  With a = (+, +, +, -), a H_4 a = J - 2 P (all-ones minus twice a permutation matrix): **2 flats, against D's 4**
  (4 is exact for H_4 itself, by the exhaustive run). ad-4 says this in its section 7b; the headline "2 log2 N" should
  carry it. Nearest true statement [read, ad-4 7b; the rank computation re-derived, the rest not re-run]: with
  quadratic row and column signs and k even, the count is r_s(k), so at least log2 N; with arbitrary non-zero
  scalings the pair-kill does not apply (a restriction leaves the class) and only (log2 N)/2 is argued.
- "Flat of the doubled space" allows a linear sign only. With a quadratic sign on the piece, H is one piece (ad-4 section 7).
- No implication between gates and flats was shown in either direction, and I see none: T and D are not lower bounds
  on circuits, and few flats do not give few gates (the 11 flats at 16 points cost 136 gates). ad-4 says so itself.

## 5. Claim (i): holds, and the guess fails at every size  [ran]

The 8 gates a+b, c+d, s = their sum, b+d, s - 2(b+d), s - 2(c+d), b+c, s - 2(b+c) give the four rows of H_4; residues
modulo 2 of the gates: 1100, 0011, 1111, 0101, 1111, 1111, 0110, 1111, so 3 repeats; the guess asked for 4. Correct.
ad-7's wording (its question 5) is about every halving-free circuit with coefficients +-1, +-2, not about minimum
circuits, so this is a counterexample to the guess as written.
**One size more, and all sizes.** H = J - 2 E with E(y, x) = 1 where x.y is odd. Compute all sums "inputs with x.y
odd" by additions only (block by block: the sum for (y', 0) is low + high, for (y', 1) it is low-odd + high-even), then
one gate s - 2 (that sum) per output. Every adding gate is a new 0/1 pattern, so the only repeats are the N - 1 outputs.

| N | 4 | 8 | 16 | 32 | 64 | 128 |
|---|---|---|---|---|---|---|
| gates (G), coefficients +1 and -2 only | 8 | 28 | 84 | 228 | 580 | 1,412 |
| repeats | 3 | 7 | 15 | 31 | 63 | 127 |
| ad-7's guess (N/2) log2 N | 4 | 12 | 32 | 80 | 192 | 448 |
| textbook gates | 8 | 24 | 64 | 160 | 384 | 896 |

Outputs equal H exactly at every size. Gates = 2 N log2 N - 3N + 4 [derived from the recursion, matches the six runs];
repeats = N - 1, which ad-7 already showed is the least possible. So **the number of repeats has no floor above N - 1**,
and the repeats saved are paid for with more adding gates (about twice the textbook in total). The weaker form
"gates >= N - 1 + (N/2) log2 N for coefficients +-1, +-2" (7, 19, 47) is not touched by this family: it stays a guess.

## 6. Claim (ii): fails  [derived + ran]

`h1_class.py` put the row K1xK1 on the gate g3 (the first full sum) and tested only that placement. Put the MIXED row
K1xK2 on g3 instead and the same wiring works for every kernel with p, q, r non-zero:

    g1 = pr a + ps b        g2 = qr c + qs d        g3 = g1 + g2                      = K1xK2
    g4 = p b + q d          g5 = (p/r) g3 + ((qr - ps)/r) g4                          = K1xK1
    g6 = (r/p) g3 + (s/q - r/p) g2                                                    = K2xK2
    g7 = b - c              g8 = g3 + (qr - ps) g7                                    = K2xK1

Same eight gates, same inputs to each gate, same four output gates. [ran] Exact on 414 kernels with rational entries
(p, q, r non-zero, determinant non-zero), among them the three kernels reported as failures: (1, 2, 3, 5),
(1, 1, 1, -2), (2, 1, 1, 3). [ran] All 24 ways of placing the four rows on the four output gates, by a span test:

| kernel | p s + q r | placements that work |
|---|---|---|
| (1,1,1,-1), (1,2,3,-6), (2,3,5,-15/2) | 0 | 4: g3 may carry any row |
| (1,2,3,5), (1,1,1,-2), (2,1,1,3) | 11, -1, 7 | 2: g3 carries K1xK2 or K2xK1 |
| (1,0,1,1), (1,1,1,0) | 1 | 2 (the same two) |
| (1,1,0,1) the subset-sum kernel, (0,1,1,1) | 1 | 0 |

Why it works [derived]: K1xK2 and K2xK1 agree on the inputs a and d, so they differ by a multiple of b - c; K1xK1 is
p/r times K1xK2 on a and c; K2xK2 is a multiple of K1xK2 on each half. None of this uses the transform.
**Nearest true statement.** With K1xK1 (or K2xK2) on g3 the wiring works exactly when p s + q r = 0 (the condition is
(ps)^2 = (qr)^2); with a mixed row on g3 it works for every kernel whose first column has no zero [ran, `zero.py`:
3,042 random invertible kernels with p and r non-zero, zeros allowed elsewhere, every one has a working placement;
of 689 with p = 0 or r = 0, 608 have none and 81 have two]. For the transform's
own kernel the four placements are one circuit up to signs of the inputs, which is why the test did not see the others.
In letters, r K1xK1 = p g3 + (qr - ps) g4 and pq K2xK2 = qr g3 + (ps - qr) g2 are polynomial identities, so the wiring
passes ae-cross's own census test ("replace the kernel by letters").
**Consequences.** (a) ae-cross's sentences "this wiring serves the transform and no other member of the class" and
"the first circuit I know of tonight that uses something the class does not have" should be withdrawn. (b) Its
experiment 8 ("the best bad circuit") has no first specimen. (c) k-cross's observation stands without exception:
every circuit of the night that has been tested is an identity of the whole class of 2 x 2 kernels. (d) The reason
offered ("it peels the first digit, and digits belong to the transform alone") describes how the circuit was found,
not what it needs.

## 7. Known?

- The count is a restricted *stabilizer rank*: a signed flat is a stabilizer state with no quadratic phase and g is a
  graph state (ad-4's reading, which I agree with [derived]). For the unrestricted problem: Peleg, Shpilka, Volk,
  "Lower bounds on stabilizer rank", arXiv 2106.03214 (2021; ITCS 2022): order n for n copies of a magic state, by
  quadratic functions on affine subspaces and their derivatives [read: search summary]. Mehraban and Tahmasbi,
  "Quadratic lower bounds on the approximate stabilizer rank: a probabilistic approach", arXiv 2305.10277 (2023; STOC
  2024): nearly n^2 for the approximate version [read: search summary]. Exponential is believed and unproved.
- The older bound k/2 is the *parity kill number* count (how many parities must be fixed to make a function constant):
  O'Donnell, Sun, Tan, Wright, Zhao, "A composition theorem for parity kill number", arXiv 1312.2143 (2013) [read:
  search summary].
- The statement T itself (flat rank of quadric signs at least k, by killing two flats with two parities) I did not
  find in four searches. I opened no paper. It is elementary and of the same family as the above, so "new as far as I
  can find" is weak evidence of novelty.
- What the known theory predicts for "linear or not": nothing. These are bounds on the number of pieces in a
  dictionary, and they are stuck at linear or quadratic in the number of bits, that is log N or (log N)^2. They do not
  bound gates. The 8-gate circuit is a rewriting of H = J - 2 E; I looked for no literature on it.

## 8. In the user's terms

- Circuit size for n points: none from T or D. From (i): 2 n log2 n - 3n + 4 gates (G), worse than the textbook.
- Saving exponent: none.
- Linear size: untouched. With (ii) gone, no circuit of the night uses a property that only the transform has, so the
  question "what does the transform have that its class does not" has, as of now, no example of a circuit that needs it.

## 9. What I did not check

ad-4's 64-point searches and its section 7b ("exactly 4 at 8 points with arbitrary signs"); the general
2^(k/2 - 1) + 3 upper bound (recalled there); Lemma B at 64 points beyond a sample of 4,000; the literature beyond four
search summaries. The proof of T was read and re-derived by one agent in half an hour; it is short, but it is not in Lean.

## Files

`waves/wave-09/af-2/` : `exh4.c`, `exh4.out` (16 points, exhaustive, with two
controls); `check.py`, `check.out` (A the dichotomy over all subspaces; B Lemma A; C Lemma B; D upper bounds; E the
doubled class and the brick; F claim (i) and the family; G claim (ii), 24 placements and explicit coefficients);
`zero.py`, `zero.out` (claim (ii) on kernels with a zero entry).

## Sources

- Peleg, Shpilka, Volk: https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITCS.2022.110 and https://eccc.weizmann.ac.il/report/2021/077
- Mehraban, Tahmasbi: https://www.quics.umd.edu/events/quadratic-lower-bounds-stabilizer-rank-probabilistic-approach
- O'Donnell, Sun, Tan, Wright, Zhao: https://arxiv.org/pdf/1312.2143
