# ab-5 cancellit: what is proved about subset sums and the cube with and without cancellation, and where the printed proof stops

> Editor's note (11 October 2026): the sentence on "the rational analogue of Aaronson's conjecture" is this agent's inference from a transfer that nobody has reviewed, and I claim nothing about any conjecture; the conjecture is known here only as Find and Boyar cite it. The sentence that "Find and Boyar's sufficient assumption is false for some minimum circuits" reports one agent's computation on small circuits: an assumption does not hold for those circuits; it does not say that their paper is wrong. The 4-point circuit in 7 operations and the rate 7/8 are due to Coppersmith, Feig and Linzer (1994), not to the patent filed in 2002 or to Alman and Rao (2023). What this report says about published work is as its author marked it: read through a tool that summarises, from an abstract, second hand, or from memory. See [Earlier papers](../README.md#earlier-papers).

11 October 2026, 04:42 to 05:32 EDT, 60-minute box. Private research: nothing published, no git, no Lean, nothing reviewed.
Marks: [read] = read today in the source named (I say "raw text" when I read the text itself and "summary" when a summarising
tool or a search result stood in between); [ran] = exact run of mine today, files in `ab-5-cancellit/`; [derived] = by hand
today, checked by nobody; [guess].
Gate counts. **(G)**: a gate is any a*u + b*v, scalings free; this is my count everywhere unless I say otherwise. The circuit
literature mostly counts **edges** (wires) of circuits whose gates may have many inputs; a circuit with g two-input gates has
2g edges. Count (O), OpenAI's, is not used here.

**No circuit below a known count and no growth law below N log N came out of this hour. Nothing here changes the order.**

Words. N = 2^k points, an address is k bits. *Subset sums* Z: output at S = sum of the inputs at all subsets of S; in the
literature the *Sierpinski*, *disjointness* or *Kneser-Sierpinski* matrix. *Yates*: (N/2) log2 N gates for Z. *Neighbour sums*
A: every address gets the sum of its k neighbours. *The transform* H: entries +1, -1; T(N) = its least cost.
*Adding-only (SUM) circuit*: gates u + v, no input is ever counted twice or cancelled; *OR circuit*: the same with repeats
allowed; *XOR circuit*: gates u + v over the field with two elements. *Cancellation*: any subtraction or any coefficient other
than 1. z = 1 - 8.7625e-4 (the published exponent). *The class*: tensor powers of 2 x 2 kernels [[1,1],[1,s]]; H is s = -1 and
Z is s = 0 (up to a free relabelling).

## 0. In ten lines

1. **The three questions of the brief have short answers.** Best known c in c N log2 N for Z: adding-only exactly 1/2 (a
   theorem); over the two-element field 1/2 and nothing better in print; with rational coefficients c tends to 0, but only
   through three calls of the transform (g-4's word, replayed here at 16 points) and only at astronomical size. Section 2.
2. **Proved separations between adding-only and cancelling circuits exist on these very matrices, of three kinds.** (a) The
   0/1 version of the transform costs of the order n log n edges for OR circuits and O(n) for XOR circuits, because its rank
   modulo 2 is log2 n [read, survey, raw text]. (b) Z over the rationals: adding-only exactly (N/2) log2 N, cancelling
   O(N (log N)^z) (g-4, with the published theorem). (c) One line, new here: the same for neighbour sums A, where
   adding-only needs at least (N/4) log2 N gates by a printed theorem (no 2 x 3 block of ones; Nechiporuk's bound), exactly
   (3/4) k N - N for even k by z-2's argument of tonight, and cancelling costs at most 2 T(N). Section 2.
3. **"Z in O(N) gates over the two-element field" is a named open question, conjectured false.** Aaronson conjectured
   N log N (Boyar and Find 2012, Find and Boyar 2014); the best lower bound in print is 3N - o(N) (Sergeev 2025); equality
   with Yates is checked in print only up to 8 x 8. **16 points is the first open size in the literature.** Section 2.
4. **Where the constant-factor savings for tensor powers come from: three sources, and only one is special to the
   transform.** (i) "low rank plus sparse" for the square of the kernel is an identity of the whole class [ran]: for every s,
   (kernel squared) = b b^T + (1 - s) P with b = (1,1,1,s). It pays 7 against 8 for every s except 0 and 1, and LOSES 5 against
   4 at s = 0, because the kernel with a zero costs one gate, not two. (ii) "rebalancing" is special to s = 0, lives in the
   edge count of depth-2 circuits, and is adding-only, so by the theorem of line 1 it can never beat Yates in gates.
   (iii) ports: the transform only, the one source that changed the order. Section 3.
5. **The printed lower-bound proof stops at one named place, and I can say what must pass through it.** Find and Boyar: the
   proof survives cancellation if no upper-half input reaches a lower-half output. Read as a lemma (section 5): in every cut
   along a bit, gates = (at least f(N/2) gates between two wires that both contain upper inputs) + (at least N/2 injections) + (pure lower gates), and a
   circuit below Yates needs, in every cut, a gate that cancels the whole upper half and delivers a lower-half form that is
   worth more gates than it costs. In a linear circuit the upper half must save one gate per lower-half point, in every cut.
6. [ran] **What one such gate can be worth.** At 8 points, two-element field, exhaustive: a single form given for free saves
   0 gates (34 forms), 1 (168), 2 (44) or 3 (one form: the total of all eight). At 4 points: at most 2 (the total). So one
   cancelling gate can be worth at most about log2 of the half size.
7. [ran] **The tie at 8 points is exactly this mechanism, paid for by one idle injection.** d-0's signed-helper circuit, read
   through the middle cut: 3 pure gates instead of 4 (one cancelling gate delivers the lower total), 5 injections instead of
   4. Net 0. This also shows that Find and Boyar's sufficient assumption is false for some minimum circuits at 8 x 8.
8. [ran] **At 16 points the delivery is worth 2 net, and in the six skeletons I could exhaust it is not available at 31.**
   Each skeleton fixes 18 to 29 gates and searches the rest exhaustively over the two-element field. All six say NO at 31;
   the four where I also ran 32 say YES. Not a proof for 16 points: a skeleton is an assumption.
9. A seed [ran]: over the two-element field Z is, after a free relabelling, an element of ORDER 3. It fixes
   (N + 2(-1)^k)/3 dimensions pointwise and acts on the rest as multiplication by a cube root of unity. Section 6.
10. Better question, section 7: **how many idle injections does the mixed part need to deliver the lower total, as a function
    of k?** 1 at k = 3. If it stays below k - 2, subset sums fall below Yates at once.

## 1. The table

Sources and dates in section 9. "Edges" = the literature's count; divide by 2 for a lower bound in two-input gates.

**Subset sums Z (N x N).**

| model | upper bound | lower bound | source, year, how read |
|---|---|---|---|
| adding-only (SUM), OR | (N/2) log2 N gates (Yates 1937) | **exactly (N/2) log2 N gates**: "any cancellation-free circuit that computes the n x n Sierpinski matrix has size at least (1/2) n log n" | Find and Boyar, arXiv:1305.3041v2 (17 Oct 2014), Theorem 10 and Proposition 4, OR circuits Theorem 11 [read, raw text]; Boyar and Find 2012, Theorem 4.1 [read, summary]; earlier Kennes 1992, independently Selezneva [read: as cited there]; survey (4.3): OR(D) ~ (1/2) n log n edges [read, raw text] |
| XOR (two-element field) | (N/2) log2 N | 3N - o(N) | Sergeev, Mat. Zametki 118:4 (2025) 607-624 [read: search summary of the abstract only; the page refused the connection]. Conjectured N log N: Aaronson, as cited by Find and Boyar [read, raw text]. Equality with Yates checked for N = 2, 4, 8: Find and Boyar ("we have experimentally verified that even for circuits where cancellation is allowed, the matrices S2, S4, S8 do not admit circuits smaller") [read, raw text]; d-0 tonight, also modulo 3, 5, 7 [read] |
| free coefficients, rationals | 3 T(N) in (G), hence O(N (log N)^z) | nothing above linear | g-4's word Z = D(1,3/5) H D(1,-1/2) H D(1,1/3) H D(1,5/4) [ran here at 16 points, exact]; no superlinear bound for any explicit matrix [read: lit-lower-bounds.md] |
| bounded coefficients | Yates (all coefficients 1) | determinant is 1, so the determinant bound gives nothing; 0.277 N sqrt(k) - N from minors | g-4 [read; derived there, unreviewed] |

**Neighbour sums A on the cube.**

| model | upper bound | lower bound | source |
|---|---|---|---|
| adding-only, OR | (3/4) N log2 N - N gates by pairing (even k) | **exactly that** (z-2, section 6, landed while I worked: N (k - 1 - floor(k/2)/2), derived there with a matching program [read]); from print alone at least (N/4) log2 N gates | [derived] Two addresses have at most 2 common neighbours, so A has no 2 x 3 block of ones; Nechiporuk (survey Theorem 3.9: "If A is (k+1, l+1)-free, then OR(A) >= \|A\|/(k l)", edges; here with their k = 1, l = 2) gives \|A\|/2 = (N/2) log2 N edges, and a circuit with g two-input gates has 2g edges. Upper: w-cross, x-5 [read] |
| XOR | as above | nothing | 12 at 8 points exhaustive modulo 2, 3, 5 (d-0); one block at 16 points 15 or 16 modulo 2 (w-cross) [read] |
| free coefficients | 2 T(N), hence O(N (log N)^z) | nothing above linear | [derived] A = H (diagonal with entries k - 2\|S\|) H / N |
| bounded coefficients | (3/4) N log2 N - N | about (N/2) log2 k for odd k | [guess-level: w-cross's rough determinant count with Morgenstern's bound] |

**The transform H** (and S, its 0/1 version: entry 1 when x.y is odd; H = J - 2S).

| model | upper bound | lower bound | source |
|---|---|---|---|
| adding-only, OR (for S) | (4 + o(1)) n log n edges | (2 - o(1)) n log n edges | survey section 4.4 [read, raw text] |
| XOR (for S) | **O(n)**, already in depth 3 | n | survey section 4.4: S = B B^T over the two-element field with B of log2 n columns [read, raw text] |
| free coefficients | O(N (log N)^z), z = 1 - 8.7625e-4 (this project); liminf 0 (OpenAI, 25 Sep 2026); (23/24) N log N in count (O) (Alman and Rao 2022) | nothing above linear | lit-lower-bounds.md, lit-constants.md [read] |
| bounded coefficients | N log2 N; (3/4) N log2 N with coefficients 1 and 2 (tonight) | (1/2) N log2 N for coefficients of size at most 1 (Morgenstern 1973) | lit-lower-bounds.md [read; Morgenstern not opened by anyone] |

## 2. The three things the brief wanted

**The best known c in c N log2 N for Z with cancellation.**
- Two-element field: 1/2. I found no construction in print that puts a single XOR gate below Yates at any size, and none
  at 2, 4, 8 exists. Lower bound 3N - o(N).
- Rationals: c tends to 0 like (log N)^(-8.7625e-4), through 3 T(N). [ran, `tests.py` T2] the word holds exactly at 16 points
  and costs 3 x 52 = 156 gates there against Yates's 32. g-4 put the crossover near log2 N = 1e888. Nothing below 1/2 at any
  size one can write.
- So the honest growth law for "Z with cancellation" is: N (log N)^z by transfer, N log N by every direct construction.

**Proved separations between adding-only and cancelling circuits, on matrices of this kind.**

| matrix | adding-only | cancelling | ratio | why |
|---|---|---|---|---|
| S, the 0/1 transform | at least (2 - o(1)) n log n edges | O(n) XOR | order log n | rank log2 n modulo 2 [read, survey] |
| Z, rationals | exactly (N/2) log2 N | O(N (log N)^z) | (log N)^(8.7625e-4), unbounded | g-4 + the published theorem |
| A, rationals | at least (N/4) log2 N (print); (3/4) N log2 N - N for even k (z-2) | at most 2 T(N) | the same, unbounded | [derived here] |
| a constructed family | 2n - 3 | n | 2 - o(1) | Svensson, in Boyar and Find 2012, Theorem 3.1 [read, summary] |
| non-explicit matrices | | | n / log^2 n | Find et al. 2013/2016, Corollary 3; Find and Boyar Theorem 4 [read, summary] |

Every separation of more than a constant factor that is proved for an explicit matrix has one of two reasons: low rank
modulo 2 (row 1), or the transform's own saving carried over (rows 2, 3). For a matrix that is invertible modulo 2, such as
Z, nothing is proved over the two-element field.

**Is "Z in O(N) gates over the two-element field" a named open problem?** Yes, from the lower-bound side.
- Find and Boyar [read, raw text]: "there are simple matrices that are conjectured to require circuits of size
  Omega(n log n). One such matrix is the Sierpinski matrix, (Aaronson, personal communication and [34])"; [34] is a thread on
  cstheory.stackexchange. And: "It is our hope that this might be a step towards proving an omega(n) lower bound for XOR
  circuits." And: "For this particular family of matrices, it is not obvious to what extent cancellation can help."
- Jukna and Sergeev 2013, Problem 7.11 [read, raw text]: "Do matrices A with XOR(A)/OR(A) -> infinity exist? Intersection
  matrix ... could be again a natural candidate to try." The intersection matrix is the complement of Z, so its XOR cost
  differs from Z's by at most about 2N [derived]. This is the same question.
- The same survey: "It is a long-standing open problem to exhibit explicit matrices requiring super-linear size" XOR circuits
  (in the words of Find et al. [read, summary]).
- For a cross-field note (g-4 saw it first): the rational analogue of Aaronson's conjecture is false, as a corollary of the
  published theorem. The conjecture itself, over the two-element field, is untouched: the transfer needs 1/2, 1/3 and 1/5.

## 3. Where the known savings for tensor powers come from (the brief's "keep asking")

**Source 1: low rank plus sparse, at a small power.** Alman and Rao (2022) and the 2002 patent get 7/8 from the fact that the
4-point transform is a rank-one matrix plus a sparse one. [derived + ran, `tests.py` T1, seven values of s, exact]:

    for every s:  [[1,1],[1,s]] squared (as a tensor) = b b^T + (1 - s) P,   b = (1,1,1,s),
    P = +1 at (0,3) and (3,0), -1 at (1,1) and (2,2).

As a program: w = x0 + x1 + x2 + s x3, then each output is w plus a multiple of one input. 7 gates against the textbook's 8,
for every s other than 0 and 1. **It is an identity of the class** (k-cross found the same for the 19-gate circuit).
At s = 0, which is subset sums, the same program has 5 gates and the textbook has 4: it loses. The reason is one line: the
identity saves 1 gate out of the 8 that a kernel without a zero costs, and the kernel with a zero costs 4 to begin with.
Two passes at 16 points: 40 gates against Yates's 32 (and 56 against 64 for a generic kernel). More generally every tensor
power of any fixed matrix is "low rank plus sparse" (Alman 2021; Kivva 2021 [read: lit-lower-bounds.md]), so this source is
not even special to the class.

**Source 2: rebalancing.** The depth-2 records for the disjointness matrix (N^1.272 Jukna and Sergeev 2013, N^1.258 Alman,
Guan, Padaki 2022, N^1.251 Sergeev 2022, N^1.2495 Alman and Li 2025, N^1.2449 Ye, arXiv:2603.15565, March 2026 [read:
abstract, summary]) use that the kernel [[1,1],[1,0]] has rows of unequal weight. That is special to s = 0. But these are
partitions of the ones into all-ones rectangles, that is adding-only circuits [read for the survey's own bound, where it
is written SUM_2(D); read for Alman and Li, through a summary of the paper's text: "expressing the 1s of R_d as the disjoint
union of several sets of the form A x B"; assumed for Ye], and they are counted in edges at depth 2. Alman and Li also
state that under SETH no somewhat balanced depth-2 circuit of size N^(1+o(1)) exists for the disjointness matrix [read,
summary], which closes the tensor-brick route to o(N log N) edges for Z as it does for H.
By the theorem in the table no adding-only circuit of any depth has fewer than (N/2) log2 N gates. **So this whole line of
work cannot put Z below Yates in count (G), by a theorem.** No test at 16 points is needed for it. (lit-constants.md made
the same point for H from the other side: edges are not gates.)

**Source 3: ports.** The transform splits along every subspace of the address space that meets its perpendicular in 0
(w-cross). Only s = -1. The only source that changed the order.

Answer to the brief: source 1 is an identity of the class and unprofitable exactly at Z; source 2 is special to Z and
provably worthless in gates; source 3 is special to H. Subset sums have no known source of their own.

## 4. The exact test at 16 points [ran]

"The best construction found for Z at 16 points" is, after the reading, one of three things. All are exact
(`tests.py`, `tests.out`; rational arithmetic).

| construction | gates (G) at 16 points | Yates |
|---|---|---|
| three calls of the transform and four diagonals (g-4's word, verified exactly at k = 4) | 3 x 52 = 156 (192 with the textbook transform) | 32 |
| source 1 at s = 0, two passes | 2 x 4 x 5 = 40 | 32 |
| source 2 (any adding-only circuit) | at least 32 by the theorem | 32 |

Nothing in the literature beats or ties Yates at 16 points except Yates.

## 5. Where the printed proof stops, and what must pass through that place

**The printed sentence** (Find and Boyar, raw text): "since S_n has full rank over F_2, a similar dimensionality argument to
that used when estimating C_3 holds even if the circuits use cancellation. Therefore we might replace the cancellation-free
assumption with the assumption that for the 2n x 2n Sierpinski matrix, there is no path from x_(n+i) to y_j for i >= 1,
j <= n. We have not been able to show whether or not this is the case for minimum sized circuits".

**The lemma it becomes** [derived; this is h-4's kill count seen from the other half, plus one term]. Take any circuit for Z
on 2n points over any field. Lower half x', upper half x''; the outputs are y' = Z x' and y'' = Z x' + Z x''. Sort the gates
by whether the result and the two operands contain upper inputs:

- **M2**: result and both operands contain upper inputs. Setting x' = 0 leaves a circuit for Z x'' made of these gates
  alone, so there are at least f(n) of them (f = least cost of Z).
- **M3, injections**: the result and exactly one operand contain upper inputs. The lower parts of the wires that contain
  upper inputs span a space that grows by at most one dimension per injection and must reach dimension n. At least n.
- **pure gates P**: the result contains no upper input. Either both operands are pure (P_int), or both contain upper inputs
  and these cancel (**P_c, a cancelling gate for this cut**). The pure gates compute Z x' from x' and from the forms W that
  the P_c gates deliver.

So **gates >= f(n) + n + |W| + f(Z_n given W for free)**, for the cut along every bit. Find and Boyar's assumption is W
empty. Consequences:
- A circuit below 2 f(n) + n has, in every one of its k cuts, cancelling gates whose forms W are worth more than |W| gates
  to the lower half.
- **Linear size.** If f(N) <= c N at N and f(N/2) = c N/2, the pure gates number at most (c - 1) N/2 while the lower half
  alone needs c N/2. In every cut the upper half must save the lower half N/2 gates: one per lower point.
- Write help(N) = 2 f(N/2) + N/2 - f(N). Then f(N) = (N/2) log2 N - sum over j of (N / 2^j) help(2^j). Known: help = 0 at
  4 and 8 points (d-0, exhaustive modulo 5 at 4 points and modulo 2, 3, 5, 7 at 8 points; "none modulo p" is not "none"). Over the rationals help is positive at astronomical size (line 1 of section 2).

**What one delivery is worth** [ran, `freeform8.py`, `freeform8.out`, `freeform4.out`; tool `mincirc_free`, which is d-0's
exhaustive `mincirc.c` plus wires given at no cost; it reproduces 12-not-11 at 8 points and 4-not-3 at 4 points first].
Two-element field. Least gates for Z when one extra form w is free:

| points | saving 0 | saving 1 | saving 2 | saving 3 |
|---|---|---|---|---|
| 4 (11 forms) | 2 | 8 | 1: the total | |
| 8 (247 forms) | 34 | 168 | 44 (six of them sums over a face, among them the outputs y_011, y_101, y_110) | 1: the total of all eight |

Other fields [ran, `freeform4p.out`, `freeform8p3.out`]: at 4 points over the fields with 3 and 5 elements (36 and 152
forms up to scaling) the total is again the only form that saves 2. At 8 points over the field with 3 elements the total
again gives 9 gates; the full census there stopped at the time limit after 222 of 3,280 forms (five of them save 2, all
with entries 0 and 1, none saves 3): unfinished, so signed forms are not excluded.

The total is worth k gates because Yates spends a private chain of k gates on the top output [derived: f(k) = 1 + f(k-1)].
So one cancelling gate is worth at most about log2 n [ran at 4 and 8 points; guess beyond], and a linear circuit needs of the order of n / log n deliveries per
cut even if their savings added up at the maximum, which nothing shows.

**The tie at 8 points is this mechanism** [ran, `d0cut.py`, whole numbers]. d-0's 12-gate circuit with one signed helper
(w = x4 + x6 + x5 on the way to the top total; h = y_001 - x6; y_101 = w + h), cut along the middle bit:
pure gates 3 (y_001, y_100 and the cancelling gate y_101) against the 4 that the lower half costs alone; injections 5 against
the 4 that are forced; M2 4. The cancelling gate delivers the lower total, the one form worth 2 at 4 points; the mixed part
pays with one injection (h) that serves no output. Net 0. Two remarks:
- Find and Boyar's sufficient assumption fails for this minimum circuit: x6 reaches y_101. It holds for other minimum
  circuits, which is all their argument would need.
- In a cut with exactly f(n) M2 gates, two wires with the same upper part can differ only by pure wires injected along the
  way [derived]. So there a cancelling gate is exactly **an adder with many inputs over the pure wires injected onto one
  mixed wire**, at the price of one gate. In the circuit above the three injected wires are y_001, x4, x5.

**16 points** [ran, `skel16.py`, `skel16b.py`, `skel16c.py`, `skelE.py`; two-element field; each run exhaustive for its budget].
If the lower total is delivered by one cancelling gate, the lower half costs 9 + 1 = 10 instead of 12. With the forced
12 + 8 on the other side that would be 30, or 31 with one idle injection. I fixed parts of such a circuit in advance and
searched the rest:

| skeleton (gates fixed in advance) | fixed | total 30 | total 31 | total 32 |
|---|---|---|---|---|
| A: lower half without the chain of its total (9), upper half transformed alone (12) | 21 | NO | NO | YES |
| A': lower half complete (12), upper half without the chain of its total (9) | 21 | NO | NO | YES |
| B: lower 9, the eight sums x'_j + x''_j, Yates on them (12) | 29 | NO | NO | YES |
| D1: lower 9, the eight sums, Yates on them without the chain of the grand total (9) | 26 | NO | NO | YES |
| D2: lower 9 and upper 9, both totals and all eight mixed outputs open | 18 | NO | NO (101 s) | not run |
| E: the direct analogue of the 8-point tie: lower 9, the sums t_j for all j but the last, Yates on them for every output but the grand total; open: the two totals, that is both private chains (7 gates by the textbook) | 25 | NO | NO (83 s) | not run |

D2 is the widest: it leaves 13 gates free for 9 outputs. E is the closest to the tie: at 8 points the same skeleton
(`skelE8.out`) gives NO at 11 and YES at 12, and at 16 points the two private chains cannot be had in 6 gates instead of
7. None of the six finds 31. So in these skeletons delivering the lower total costs the mixed part at least 2 extra gates
at 16 points, against 1 at 8 points.

**Why the delivery is cheap at 8 points, read off the tying circuit** [derived; the last sentence is a guess]. In the
coordinates of the cut write t_j = x'_j + x''_j. The grand total needs t_10 + t_11. The tying circuit computes it as
(t_10 + x'_11) + x''_11 instead of t_10 + (x'_11 + x''_11): the same two gates, but now two lower inputs (x'_10 and x'_11)
have been injected onto ONE upper form (x''_10), which is what a many-input adder needs. The wire t_11 is never formed, and
nothing else wanted it. Then one idle injection (y'_01 minus x''_10) lets one gate read off the lower total. So at 8
points the regrouping is free and the delivery costs one idle gate for a saving of one. At 16 points the lower total has
four pieces (y'_011, x'_100 + x'_101, x'_110, x'_111). To land the last three on one upper form the sum t_100 + t_101 +
t_110 + t_111 has to be regrouped across two levels, and that un-shares a wire (t_110, or t_101) that another output
needs: one extra gate, before the idle injection. In the two designs I worked by hand (not run, not checked) the cost,
counting the cancelling gate itself, was 3 gates to deliver x'_100 + ... + x'_111 (worth 2) and 4 gates to deliver the lower
total (worth 3). Guess: the regrouping costs one un-shared wire per level above the first, so d(k) >= k - 2 and
**delivering the half total always ties or loses**; this is h-4's "idle = excess" with a mechanism attached.

## 6. Seeds from the reading

1. **Over the two-element field Z has order 3.** [ran, `tests.py` T3, k = 1..5] With R = [[1,1],[1,0]], the tensor power M of R
   is Z with a free relabelling, and M^3 = 1 modulo 2. E = 1 + M + M^2 is an idempotent of rank (N + 2(-1)^k)/3:
   0, 2, 2, 6, 10 at 2 to 32 points. So Z fixes about N/3 dimensions pointwise and is "multiplication by a cube root of
   unity" on the other 2N/3 (R is multiplication by a generator of the four-element field). In a basis adapted to that
   splitting Z costs about N/3 gates, and the adapted bases form a huge family. This is the two-element-field cousin of
   "the transform is a reflection" and of i-cross's "cheapest basis of the mirror"; by w-cross's hybrid 2 I expect the same
   wall (the basis costs half of Z), but nobody has priced it over this field. x-7 met order 3 for bit matrices; I found no
   note of it for Z itself.
2. **The two-element field is the clean room.** No height, no transform (H is all ones modulo 2), no ports (the symmetries
   of the disjointness pattern are only the k! permutations of the bits). Every mechanism of the night is switched off
   there, and the literature's best lower bound is 3N. A proof of N log N there would contradict nothing published;
   a circuit below Yates there would be a mechanism that uses none of height, 1/2, or ports.
3. **Level pairs are nearly linear** (Kaski, Koivisto, Korhonen 2012 [read: search summary]): the sums over disjoint
   p-sets for all q-sets cost O((n^p + n^q) log n) adding-only gates for constant p, q. In our letters: the block of Z
   between two fixed low levels costs (inputs + outputs) x log k. It does not add up to less than Yates over all
   (k+1)^2 level pairs [derived: about 2 k N log k], because Yates shares across blocks; I note it as the one place where the
   literature has a near-linear adding-only circuit for a piece of Z.

## 7. The better question, and mutations

**Question.** In the cut along one bit, let d(k) = the least number of extra gates (idle injections or extra M2 gates)
the mixed part needs so that one cancelling gate delivers the total of the lower half. The delivery is worth k - 2 net
(k - 1 saved, 1 paid) [ran at k = 3, 4 for the saving]. d(3) = 1 [ran: the tie]. **Subset sums fall below Yates at the first
k with d(k) < k - 2.** At k = 4 that asks d = 1; six skeletons say at least 2. If d(k) >= k - 2 for every k, with a reason,
that reason is most of a proof that one delivery never pays, and the next object is two deliveries that share their cost.

Mutations:
1. **Decide 16 points over the two-element field** (the first size open in print). The lemma gives a strong filter for a
   SAT or a branching search: in each of the 4 cuts at most 11 pure gates, at least 12 M2 gates, at least 8 injections, and
   with one cancelling gate its form is one of 45 named forms (`freeform8.out`). No SAT solver is installed on the rented
   machine [ran: checked]; `mincirc_free` handles 4 free helpers at 16 points in about 100 s and 5 would take hours.
2. **d(k) by search**: fix only the lower 9 and the cancelling gate's two operands' upper parts; let the annealer of
   `j-machine/` minimise the gates of the mixed part. One number per run.
3. **Savings of two deliveries**: the census for pairs of free forms at 8 points (about 30,000 runs of 0.1 s): are savings
   ever more than additive? A linear circuit needs deliveries that share.
4. **Price the adapted basis of seed 1** at 4, 8, 16 points over the two-element field with `mincirc`.
5. **The same lemma for A** (brief 1 of this wave): cut the cube along a bit; A = [[A', 1],[1, A']], so the mixed part
   is two identity blocks and the lemma degenerates. A different cut is needed there; I did not find it.
6. Tell brief 5 (z-cut, running now as ab-4): the cut accounting above is the literature's own proof, and the term it
   lacks is "f(Z_n given W) + |W|".

**Growth law, as the brief asks.** None new below N log N. What the hour leaves is: (i) from print, for Z: adding-only
exactly (N/2) log2 N; two-element field between 3N - o(N) and (N/2) log2 N; rationals O(N (log N)^z) by transfer only.
(ii) [derived] f(N) = (N/2) log2 N - sum over j of (N / 2^j) help(2^j), where help(n) is what cancelling gates across the
top cut save at n points; help = 0 at 4 and 8 points, and linear size needs help(n) of the order of n/2 at every size.
(iii) [ran] one cancelling gate saves the lower half at most 2 and 3 gates at 4 and 8 points: like log2 n, not like n.
No growth law for the transform came out because everything here is about Z in fields where the transform does not exist
or about Z through the transform, where the published exponent is simply inherited.

## 8. Criticism, last

- z-2 (wave 7's critic) had the exact adding-only count for A before me; I saw it only at the end. My contribution for A is
  the printed source for the order and the one-line upper bound with cancellation.
- The table mixes counts. The survey and the gap papers count edges with unbounded fan-in; I converted only where I say so.
  The adding-only bound for A, (N/4) log2 N gates, is my conversion of an edge bound and nobody checked it.
- Sergeev 2025 (3N - o(N)) is read from a search summary only. Boyar and Find 2012, Find et al., Ye 2026 and Kaski,
  Koivisto, Korhonen 2012 were read through a summarising tool. Read as raw text: Find and Boyar 2014 (the passages quoted),
  the survey (sections 1.1, 3.3, 4.3, 4.4, chapter 7). Kennes, Selezneva, Morgenstern and the cstheory thread: not opened.
- "Rebalancing circuits are adding-only" is read for the survey's bound, read through a summary for Alman and Li, and
  assumed for Ye.
- The lemma of section 5 is a few lines, by hand, unreviewed. Its second remark (cancelling gate = many-input adder) is
  for cuts with exactly f(n) M2 gates only. I did not prove that a cut of a 31-gate circuit must be of that kind; one
  extra M2 gate is also allowed by the budget when the delivery is the total.
- The census at 8 points is complete over the two-element field only (over three elements 222 of 3,280 forms). Over other
  fields there are more forms and the numbers may differ; "none modulo 2" is not "none".
- The six skeletons are assumptions about 18 to 29 of the gates. They fix Yates's own wires for the parts they fix, and
  the 8-point tie already uses a wire (w) that Yates does not have. So they say little about circuits whose mixed part is
  built differently. They are six points, not a search.
- Seed 1 is a fact about a matrix, not a circuit.
- The overlap with g-4 is large for Z (its literature table has Kennes, Boyar and Find, the survey, Alman and Li, Sergeev).
  New here: the tables for A and H, the three kinds of proved separation, Find and Boyar's own sentence on where the proof
  stops and their computer check to 8 x 8, the class identity with its sign at s = 0, the lemma, the census, the skeletons.
- Nothing here changes the order, or any constant.

## 9. Sources (all read 11 October 2026)

- M. G. Find, J. Boyar, "Cancellation-Free Circuits in Unbounded and Bounded Depth", arXiv:1305.3041v2, 17 October 2014
  (journal version, Theoretical Computer Science; preliminary version FCT 2013). PDF text.
- J. Boyar, M. G. Find, "Cancellation-free circuits: An approach for proving superlinear lower bounds for linear Boolean
  operators", arXiv:1207.5321 (2012). ar5iv page, summarised.
- S. Jukna, I. Sergeev, "Complexity of Linear Boolean Operators", Foundations and Trends in TCS 9(1), 2013, 1-123; authors'
  PDF at web.vu.lt/mif/s.jukna/Knizka/linear.pdf, PDF text; the book's page of later comments (11 items, to 26 May 2025).
- M. Find, M. Goos, M. Jarvisalo, P. Kaski, M. Koivisto, J. H. Korhonen, "Separating OR, SUM, and XOR Circuits",
  arXiv:1304.0513; J. Comput. Syst. Sci. 82(5), 2016, 793-801. ar5iv page, summarised.
- I. S. Sergeev, "Lower Bounds for Additive Complexity of Linear Operators and Bilinear Algorithms for Matrix and Polynomial
  Multiplication over GF(2)", Mat. Zametki 118:4 (2025), 607-624. Search summary of mathnet.ru/eng/mzm14541 only.
- J. Alman, B. Li, "Kronecker Powers, Orthogonal Vectors, and the Asymptotic Spectrum", arXiv:2509.14489v1, 17 September
  2025. HTML, first 100,000 characters, summarised.
- L. Ye, "Improved Depth-2 Linear Circuits for Disjointness via Quenched Lyapunov Exponents", arXiv:2603.15565, 16 March
  2026, revised 3 September 2026. Abstract page, summarised.
- P. Kaski, M. Koivisto, J. H. Korhonen, "Fast Monotone Summation over Disjoint Sets", arXiv:1208.0554 (2012). Search summary.
- Project files: w-cross.md, WAVE8-PICKS.md, g-4.md, h-4.md (first part), d-0.md (first part), lit-constants.md,
  `wht33/research-2026-10-09/readers/lit-lower-bounds.md` (the path in the brief has one folder too many), k-cross.md (lines).

## Files

`waves/wave-08/ab-5-cancellit/`:
- `tests.py`, `tests.out`: T1 the class identity and its gate counts; T2 the three-call word at 16 points; T3 order 3.
- `mincirc_free.c`, `mincirc_free`: d-0's exhaustive search with an optional fifth argument, a file of wires given free.
- `freeform8.py`, `freeform8.out`, `freeform4.py`, `freeform4.out`: the census of single free forms (two-element field);
  `freeform4p.py`, `freeform4p.out` (3 and 5 elements, 4 points); `freeform8p3.py`, `freeform8p3.out` (3 elements, 8 points,
  unfinished). Note: with free wires the tool's line "circuit with n gates" counts the free wires too; my scripts read the
  budget line instead.
- `d0cut.py`, `d0cut.out`: d-0's tying circuit read through the middle cut.
- `skel16.py`, `skel16.out` (A, B, and a shallow C that decides nothing), `skel16b.py`, `skelD1.out`, `skelD2.out`,
  `skel16c.py`, `skelAp.out`, `skelE.py`, `skelE8.out`, `skelE16.out`; `rows_zeta2.txt`, `rows_zeta3.txt`, `rows_zeta4.txt` (targets), `free16_*.txt` (the fixed wires).
