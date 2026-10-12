# ab-4 z-cut: the pair argument reads on subset sums only in a tilted cut; what the plain cut gives instead is two exact statements: "Yates' count minus gates <= helper wires that straddle a cut", and "(N/2) log2 N for every circuit that never clears exactly the on-half of a wire"

> Editor's note (11 October 2026): what this report says about published work is as its author marked it: read through a tool that summarises, from an abstract, second hand, or from memory. Nobody checked those statements against the sources. Two older papers that the night's searches did not reach were read afterwards. See [Earlier papers](../README.md#earlier-papers).

11 October 2026, 04:45 to about 05:30 EDT. Developer ab-4-zcut, one-hour box. Private; nothing reviewed, nothing in Lean,
nothing published. Count **(G)** everywhere: a gate is any a*u + b*v of two earlier values, scalings free.
Marks: [read] from tonight's reports; [ran] a program of this folder, exact rational arithmetic; [derived] by hand in this
hour, checked by nobody else; [guess]. Files: `waves/wave-08/ab-4-zcut/`.

**No circuit below Yates' count and no growth law below (1/2) N log2 N. Nothing here changes the order.**

Words. N = 2^k points; an address is k bits. *Subset sums* Z: the output at a set S is the sum of the inputs at all subsets
of S. *Yates*: the standard (N/2) log2 N gates (4, 12, 32 at 4, 8, 16 points); c(N) = least number of gates for Z.
*Wire*: a value the program holds, a vector over the N inputs, taken up to a factor. *Cut* by one address bit: L = the
addresses with that bit off, R = those with it on; a wire is written (a, b), a = its entries on L, b = its entries on R.
The rows of Z are then (z, 0) and (z, z), z running over the rows of the half-size Z. *Class* of a wire at a projection:
the projected vector up to a factor; *trivial* when it is zero or a single input. A gate is *new* at a projection when its
class there is not trivial and was not seen on an earlier wire. n(L), n(R) = number of gates new at L, at R;
B = gates new at both, E = gates new at neither; gates = n(L) + n(R) - B + E [read: x-2]. n(L) and n(R) do not depend on
the order of the gates; B and E do, E - B does not. *Helper*: a gate that is not an output. *Waste* of a half: n(L) - c(N/2).
*Crossing* wire: non-zero on both halves. *Pure* wire across a cut: a and b proportional (or one of them zero); *mixed*
otherwise.

## 0. In eleven lines

1. **First experiment** [ran, `zmeter.py`]: all 2,748 optimal 12-gate circuits for Z at 8 points (the mod-3 list, lifted and
   replayed over the rationals; the mod-2 list gives the same picture on 2,622), three cuts each, B minimised and
   maximised over ALL valid orders of the gates. In the plain cut E - B is 4 = N/2 (5,946 cases) or **3** (2,298 cases), never less.
   E = 3 with B = 0 exists (1,356 cases). So **E >= N/2 is NOT forced for Z in the plain cut, even with B = 0**, as w-cross suspected.
   Every case with E - B = 3 has one wasted class on one half (n = 5 against c(4) = 4); the sum is always 12.
2. **The pair argument is not lost, it is tilted** [derived; ran on 2,748 circuits x 3 cuts at three pairs, `zpencil.py`, and on the mod-2 list of 2,622 at a fourth]. Replace
   "entries on R" by the projection a + s*b for a number s. For every pair s, t other than -1 and "infinity" (the plain R),
   the two rows (z, 0), (z, z) have the same class at both projections, so **E(s, t) >= N/2 for every circuit**, and
   n(s) >= c(N/2). The plain cut is the pair (0, infinity): it uses one of the two forbidden values, which is the whole
   reason E is not forced there. Measured: least E = 4 at (1, 2), (1/2, -3), (0, 1), (0, -2); least E = 3 at (0, infinity),
   (-1, infinity), (0, -1).
3. The same holds for every 2 x 2 kernel [[1,1],[1,sigma]] with forbidden values -1 and -1/sigma [derived]. So this
   meter is an identity of the whole class: it reads on Z exactly as on the transform and cannot tell them apart.
4. **New, special to Z (the zero in its kernel): the deviation lemma** [derived; rank checked on all 2,748 x 3,
   `zcross.py`]. In every circuit for Z, at least N/2 gates have a non-zero R-part whose class on R was already seen, and
   the differences between their L-parts and the L-part of the first wire of that class span the whole L-space.
5. **Hence, for every circuit and every cut** [derived; ran]: gates >= n(L) + n(R) + N - X, X = number of crossing gates.
   The N/2 outputs (z, z) cross; so **gates >= 2 c(N/2) + N/2 - (number of crossing helpers)**.
6. **Down a whole cube tree** [derived; ran on 2,748 circuits x 6 trees x 7 nodes, `ztree.py`]:
   **(N/2) log2 N - gates <= sum over the nodes X of Xh(X)**, Xh(X) = the number of distinct classes, among the wires cut
   down to X, that are non-zero on both halves of X and are not a row of Z on X. Every gate saved below Yates needs its
   own helper wire that straddles a cut. No hypothesis on wires, coefficients or field.
7. **By-product, unconditional** [derived]: c(N) >= c(N/2) + N - 1, so c(N) >= 2N - 2 - log2 N (4, 11, 26 at 4, 8, 16
   points; known: 4, then 12 with no 11 modulo 2 or 3 [read: d-0], then at most 32). Linear, so of no use for the order; it is the first reading of this meter on Z
   that is not the trivial N - 1.
8. **The resource is abundant and, at 8 points, worth nothing** [ran]: only 6 of the 2,748 circuits have no straddling
   helper in some tree; in one cut up to 5 of the 5 helpers straddle; and all of them together never buy more than ONE
   gate at a node, which is always paid back by one wasted class below. The theorem allows one gate per straddling helper.
   A cheaper Z lives exactly in the gap between "one per helper" and "at most one in all, repaid".
9. **The class theorem of the hour ("no return")** [derived; section 3b]. Call a gate a *return* at a node X when its wire
   is zero on the on-half of X, non-zero on the off-half, and one of its two parents is non-zero on the on-half (the gate
   clears, exactly, everything its parents held there). **A circuit for Z with no return at any node of one cube tree has
   at least (N/2) log2 N gates**, whatever its coefficients and whatever else it cancels. Every circuit without
   cancellation is in this class for every tree, and the class is wider: clearing an off-half is allowed. Measured at 8
   points [ran, `zreturn.py`]: 2,214 of the 2,748 optimal circuits are in the class (for all six trees; they are exactly
   those with a cancellation-free derivation), 534 are outside it for every tree and still cost 12. **A cheaper Z must use
   returns.** Other classes (section 4): tilted-clean: exactly (N/2) log2 N; at most (1 - eps)|X| crossing classes per
   node: eps N log2 N; plain-clean (B = 0 in the plain cut): only c(N/2) + N - 1 proved.
10. **Size pushed once** [ran, `z16.py`, u-3's own 32-gate circuit at 16 points, which has no cancellation]: in its four
    plain cuts E - B = 5, 6, 7, 8 against N/2 = 8 (waste 3, 2, 1, 0, always on the off-half), crossing helpers 11, 10, 11,
    5 of 17; and in all four cuts the gates living on the off-half alone are exactly 12 = c(8), the R-repeats exactly
    8 = N/2, n(R) exactly 12: the equalities line 9 forces. The deficit of E - B grew from 1 to 3; it is repaid each time.
11. The wall is the one already named W2 (sharing between two copies, "direct sum") [read: i-cross, j-manyatonce]. What
    this hour adds is where the sharing has to sit for Z: in helper wires that straddle a cut, and in gates that come back
    from the on-half by exact cancellation; about N/2 straddling helpers per level for a linear-size circuit.

## 1. The first experiment [ran]

`../d-0-zeta/mincirc_all` re-run with every solution printed (`z8_p2_full.out`: 2,802 sets of 5 helpers modulo 2;
`z8_p3_full.out`: 2,772 modulo 3). Lifted (digit 2 read as -1) and replayed over the rationals by `zmeter.py`: 2,622 and
2,748 replay as 12-gate circuits (the others need another lift; not pursued). For each circuit and each of the three cuts:
n(L), n(R), E - B, and the least and largest B over all valid orders (a walk over the 4,096 subsets of gates).

| plain cut, 2,748 circuits x 3 cuts | n(L), n(R) | E - B | least B | cases |
|---|---|---|---|---|
| both halves optimal | 4, 4 | 4 | 0 | 5,922 |
| both halves optimal, a shared gate forced | 4, 4 | 4 | 1 | 24 |
| L wasteful | 5, 4 | 3 | 0 | 1,350 |
| L wasteful, a shared gate forced | 5, 4 | 3 | 1 | 942 |
| R wasteful | 4, 5 | 3 | 0 | 6 |

(The rows with least B = 0 and E - B = 3 sum to 1,356; `meter_p3.out` has the finer split by largest B, which reaches 4.)
- E - B = N/2 - 1 happens in 2,298 of 8,244 cases; then one half holds 5 classes. gates = n(L) + n(R) + (E - B) = 12
  always. So at 8 points the meter's content is: waste + (E - B) = N/2 exactly, which is the optimality of 12 restated.
- Per circuit: 480 have E - B = 4 in all three cuts; 2,238 have exactly one cut with 3; 30 have two.
- One circuit with E = 3, B = 0, read at the cut of bit 0 (helpers 00001010, 00110010, 10111010, 11111010, 11111110): its
  R-half is a chain 1100, 1110, 1111 and then 1010 = 1110 - 0100; the last gate is (1010 | 1010) = (1111 | 1110) -
  (0101 | 0100): new on R only, old on L. The join "rides", as the brief hoped. The price is the wire (0101 | 0100), whose
  L-part is a fifth class on L.

## 2. The pencil of cuts [derived, then ran]

For a number s let P_s(a, b) = a + s*b; P_infinity(a, b) = b. Every P_s turns the circuit into a circuit for the half-size
Z (the images of the inputs are single inputs), so n(s) >= c(N/2) for every s. Rows: P_s(z, 0) = z and
P_s(z, z) = (1 + s) z. For s other than -1 and infinity both are the class z, so the later of the two is not new at s; the
pair for the empty set is the trivial class. Hence for s, t outside {-1, infinity}: E(s, t) >= N/2, and
gates = n(s) + n(t) - B(s, t) + E(s, t) >= 2 c(N/2) + N/2 - B(s, t).
- Check (`zpencil.py`, least E over all orders): (1, 2): 4 to 8; (1/2, -3): 4 to 8; (0, 1): 4 to 8; (0, -2) (`meter_p2.out`):
  4 and more. With a forbidden value: (0, infinity) 3 to 5; (-1, infinity) 3 to 5; (0, -1) 3 to 7.
- What a tilted cut is: the plain cut after the change of inputs x_L = p + q, x_R = s p + t q. In the coordinates p, q a
  wire (a, b) reads (a + s b, a + t b), and Z is (the kernel [[1,1],[1+s,1+t]], no zero) x (half-size Z), computed from
  starting values that are no longer single coordinates but are still free.
- A pure wire z x (lambda, mu) has the same class z at every s but one. A mixed wire has a different class at every s: it
  is new at every generic s at once. For generic s: n(s) = M + P, M = mixed gates, P = distinct classes among pure gates,
  and gates = M + P + (pure gates that repeat a class), the last term >= N/2. So **a circuit for Z at N points is a line
  of circuits for Z at N/2 points** (wires a + s*b), in which pure wires stand still and mixed wires move.
- Measured at 8 points: M + P runs from 4 to 8; M + P = 4 (an optimal half-circuit at generic s) happens only with M = 0;
  with M = 1, 2, 3, 4 mixed gates the least M + P is 5, 6, 6, 7. Only 24 of the 2,748 circuits are pure in all three cuts (product wires
  only); in a cut up to 4 of the 12 gates are mixed. Mixed wires are everywhere and replace pure repeats one for one.
- With all s at once the meter gives only gates >= c(N/2) + N/2: a mixed gate is new at every s, so no factor 2 can come
  from counting projections. The factor 2 needs B = 0 at some pair, and that is a property of a class, not of Z.

## 3. The deviation lemma and the crossing-helper inequality [derived; ran]

Take any circuit for Z and a plain cut. For each class on R (single inputs included) take the FIRST wire that has it,
(f, b). Call a later gate with the same class on R an *R-repeat*; scaled to (a', b), its *deviation* is a' - f.
- **Lemma.** The deviations of the R-repeats span the whole L-space. So there are at least N/2 R-repeats.
  Proof: let D be their span. A gate new on R has two parents with non-zero, non-proportional R-parts (a parent with zero
  R-part would make the R-part proportional to the other parent's). Each parent's L-part is f of its class plus a deviation.
  So f(new class) is a combination of earlier f's modulo D; f = 0 on the inputs of R; so every f lies in D. The output
  (z, z) is either first in its class (z = f) or a repeat (z = f + deviation): z is in D for every row z. D is everything.
- On L the pairs give the same: at least N/2 gates with a non-zero L-part are not new on L.
- Count: G_L = gates non-zero on L, G_R = gates non-zero on R, X = gates non-zero on both. gates + X = G_L + G_R >=
  n(L) + N/2 + n(R) + N/2. **gates >= n(L) + n(R) + N - X**; equivalently E - B >= N - X.
- X = N/2 (the outputs (z, z)) + Xh, Xh = crossing helpers. **gates >= 2 c(N/2) + N/2 - Xh.**
- Down a tree: the gates new at a node X, cut down to X, are a circuit for Z on X [read: x-2 section 1], so the same
  inequality holds there: n(X) >= n(X0) + n(X1) + |X|/2 - Xh(X). Summing: **gates >= (N/2) log2 N - sum over nodes of Xh(X).**
- Unconditional by-product: gates with zero R-part >= N/2 - 1 (the outputs (z, 0)); gates with non-zero R-part >=
  n(R) + N/2. So c(N) >= c(N/2) + N - 1 and c(N) >= 2N - 2 - log2 N.
- A wire with m non-zero entries straddles at most m - 1 nodes of a tree (the branch points of its support). So
  (N/2) log2 N - gates <= sum over helpers of (support - 1).
- Checks: `zcross.py`: G_L - n(L) >= 4, G_R - n(R) >= 4, the inequality, and deviation rank 4, on 2,748 x 3; least slack
  0 (Yates' own cut). `ztree.py`: the node inequality on 2,748 circuits x 6 trees x 7 nodes.

| at the root, 2,748 x 6 trees | crossing helpers Xh | gates bought (Xh - slack) | cases |
|---|---|---|---|
| | 0 | 0 | 150 |
| | 1, 2, 3, 4, 5 | 0 | 1,164; 2,568; 3,912; 3,762; 336 |
| | 2, 3, 4, 5 | 1 | 12; 816; 3,756; 12 |

At nodes of size 4: Xh = 0, 1, 2, never a gate bought. Least over the six trees of the total of Xh: 0 for 6 circuits
(Yates in its six bit orders), 1 to 6 for the other 2,742.
- For the transform H the same count gives nothing: all N outputs cross. The inequality is special to kernels with a zero.
- R-repeats are 4 or 5 in every case: the number of gates touching R is 8 or 9 of 12, so the gates that live on L alone
  are 4 or 3: when only the three outputs live on L alone (552 cases) the L-half is computed entirely by crossing wires.

## 3b. The no-return theorem [derived; consistency ran]

The count of section 3 splits the gates of any circuit as (gates that live on L alone) + (gates that touch R), and the
lemma bounds the second group: gates touching R >= n(R) + N/2. The first group contains the outputs (z, 0).
- If no gate living on L alone has a parent that touches R (no return at the root), the gates living on L alone are by
  themselves a circuit for Z on L. Then gates >= (a circuit for Z on L) + (a circuit for Z on R, the classes new on R) +
  N/2, with no sharing possible between the two groups because they are disjoint sets of gates.
- The condition passes to both pieces: a gate of either piece is a gate of the circuit with the same parents, read on a
  smaller block, so "no return at every node of the tree below" is inherited. Hence t(N) >= 2 t(N/2) + N/2 in the class
  and **gates >= (N/2) log2 N**. Yates is in the class; so is every circuit whose gates only add (positive
  coefficients on vectors of one sign): a sum cannot vanish on a half unless both parents do.
- The class is wider than "no cancellation": w = u - v may clear any part of u that is not a whole on-half of a node on
  which w survives; in particular clearing an off-half ((0, b) = (a, b) - (a, 0)) is allowed.
- [read: web search summaries only, 05:25 EDT; the papers themselves not opened] (1/2) n log n for this matrix (they call
  it the Sierpinski matrix) in circuits without cancellation, and tight, is a known theorem: Boyar and Find,
  "Cancellation-free circuits: an approach for proving superlinear lower bounds for linear Boolean operators",
  arXiv:1207.5321 (2012), and "Cancellation-Free Circuits in Unbounded and Bounded Depth", arXiv:1305.3041 (2013). The
  summaries say the authors could not decide whether the restriction is needed and checked 2, 4, 8 points by machine, and
  that the bound supports a conjecture of Aaronson. Their setting is circuits of additions modulo 2. So the statement
  above is their theorem (in count (G), any field) with its hypothesis cut down to the one cancellation event the
  recursion cannot stand. I did not check whether their proof already gives this wider class.
- Measured, 8 points (`zreturn.py`, every possible parent pair of every gate considered): a derivation with no return
  exists in all six trees for 2,214 circuits and in no tree for 534; the 2,214 are exactly the circuits that have a
  cancellation-free derivation. So at this size the wider class holds no optimal circuit that the narrow one misses.
- **The price of a return at 8 points** (`zprice.py`, least number of returns at the root over all derivations): in
  7,692 of the 8,244 (circuit, cut) cases no return is needed at the root, and the gates on L alone are 4 = c(4), those
  touching R are 8 = c(4) + N/2. In the other 552 cases exactly ONE return is needed, the gates on L alone are 3 (one
  short of a half-circuit) and those touching R are 9 (one more than the lemma's minimum). One return buys one gate on
  the off-half and costs one gate on the other side, every time. Never two returns at the root.
- Measured, 16 points (`z16.py`, `z16.out`): `u-3-zletter/z16_32gates_letter.txt` (32 gates, additions only) in its four
  plain cuts: n(L) = 14, 13, 12, 15; n(R) = 12 each time; E - B = 6, 7, 8, 5; crossing helpers 10, 11, 5, 11; gates on
  the off-half alone 12, R-repeats 8 each time. A second stored circuit (33 gates) has E - B = 6, 6, 6, 7.
  The crossing-helper inequality holds at every node of all 24 trees for both; least total of Xh over the trees: 15 and 19.

## 4. Growth laws, and exactly which class each covers [derived]

| class of circuits for Z | recursion | result |
|---|---|---|
| every circuit | c(N) >= c(N/2) + N - 1 | 2N - 2 - log2 N |
| at each level some tilted cut (s, t) has B = 0, and both projected circuits are again in the class | t(N) >= 2 t(N/2) + N/2 | exactly (N/2) log2 N; Yates with twin halves is in it |
| at every node X of one cube tree at most (1 - eps)|X| classes cross (outputs included) | n(X) >= n(X0) + n(X1) + eps|X| | eps N log2 N |
| no straddling helper at any node of one tree | same with Xh = 0 | exactly (N/2) log2 N |
| **no return at any node of one tree** (contains every cancellation-free circuit) | t(N) >= 2 t(N/2) + N/2 | exactly (N/2) log2 N |
| B = 0 in the plain cut only | nothing beyond the first line | open: E = 3 < N/2 occurs at 8 points |

- "Is Yates optimal among circuits with B = 0 in the plain cut?" Not decided. At 8 points yes (12 is the minimum there
  for all circuits, exhaustively modulo 2 and 3 [read: d-0]). On paper I get only the first line; the pair argument fails there.
- What a circuit below Yates needs: in every tree a return at some node (an output or helper on an off-half made by
  clearing exactly what two wires held on the on-half), and, in every plain cut and at every level: more than N/2 crossing gates, i.e. crossing
  helpers at least equal to the saving plus the waste. For linear size: about |X|/2 straddling helper classes at almost
  every node, as many as there are outputs; with C N gates, each wire must straddle about (log2 N)/(2C) nodes on
  average, and be new and not a row of Z at each.
- In a tilted cut the same circuit needs B(s, t) > waste for all s, t outside the two forbidden values.

## 5. Went around, three times

1. "E is not forced" (the plain cut, section 1) became "which projections force it": all but two on a line of
   projections (section 2). The failure was made of the zero in Z's kernel: the row (z, 0) vanishes on R.
2. "B cannot be assumed zero" (the pencil gives no factor 2) became "count what the zero does give": half of the outputs do
   not cross, so repeats on the two sides cannot be the same gates unless wires cross (section 3). That turned the unknown B
   into a visible quantity, the straddling helpers.
3. "Straddling helpers are everywhere, so the inequality forbids nothing" became "split the gates by where they live
   instead of where they are new": the two groups are disjoint, so sharing cannot enter, and the only thing that can break
   the recursion is a gate that comes back from the on-half (section 3b).

## 6. Mutations (not judged)

0. **Price a return.** The no-return theorem says every saving below Yates passes through returns. Count them: with rho
   returns at the root the gates on the off-half alone are a circuit for the half-size Z that is GIVEN rho extra values.
   How much can one given value save? If at most one gate each, then gates >= (N/2) log2 N - (number of returns, over
   the nodes). First data (section 3b): at 8 points a return saves exactly one gate on the off-half and is repaid by one
   gate touching R. In general the saving of a return is at most the cost of its wire computed inside the off-half. If one given value can save many gates, that value is the object to look for: a wire on the off-half
   that is expensive from below and cheap as a difference of two wires that reach into the on-half.
   What such a pair looks like [derived, sketch]: a return is (a, b) minus (a', b), two wires with the SAME R-part and
   different L-parts, and the value that comes back is a - a', a deviation of section 3. L-parts ride along the gates of
   the R-half linearly, so a wire's L-part is fixed by which of its leaves were "labelled" copies of the inputs. Two
   versions of one R-wire that differ on a set D of leaves share no gate above D: every wire on the way whose support
   meets D exists twice. The value returned is the wire cut down to D, worth at most |D| - 1 gates on the off-half, and
   the doubled gates above D number at least about as many unless they are wanted for other outputs. The saving, if it
   exists, is a family of outputs whose doubled gates coincide. That is the direct-sum wall again, now as a statement
   about one concrete object: versions of the R-half's wires that differ only in their L-parts.

1. **Price a straddling helper.** The theorem allows one gate per (helper, node). Measured at 8 points: at most one in all at
   a node, and repaid. Prove "a crossing helper class is new on L or on R at the node where it is counted and so pays for
   itself", or find the configuration where two straddling helpers buy two. A finite question at 16 points if restricted
   to helpers that straddle the root only.
2. **Search where the inequality says to.** Seed a 16-point search with circuits whose helpers straddle at two levels at
   once (the chain circuit of section 1 composed with itself), and score by sum of Xh minus waste instead of by gates.
3. **The missing half.** The lemma gives (gates touching R) >= n(R) + N/2. Yates' recursion would follow from "the gates
   living on L alone are a half-circuit, c(N/2) of them", and that is false: 3 instead of 4 in 552 cases. At 8 points each
   missing one is made up by exactly one more gate touching R. Prove that compensation as a statement about deviations
   ("a deviation that also does L's work cannot be independent of the others"), or find where it fails. [guess]
4. **Rigidity.** If the optimal circuits for the half-size Z are isolated (no one-parameter families), every circuit with a
   mixed wire has M + P >= c(N/2) + 1 at generic s (else the line of circuits would be such a family). Measured at 8
   points: true (least M + P = 5, 6, 6, 7 for M = 1, 2, 3, 4). A proof of "M mixed wires waste about M/2" would be new.
5. **Ports as constraints.** The pair argument needs exactly a splitting of the rows as (two rows) x (half-size rows): a
   port in x-6's sense. Z has its k coordinate ports (plus the collapses s_i = s_j, three rows to one); H has many more.
   Each port is a pencil of cuts where sharing must go unpaid. So the meter constrains H in more directions than Z.
6. The same lemma for kernels [[1,1],[0,1]] x anything and for neighbour sums (rows with many zeros on a half).

## 7. Criticism, last

- Everything measured is at 8 points, on circuits with entries 0, +1, -1 that come from exhaustive lists modulo 2 and 3
  (so "all optimal circuits" means: all whose helper sets exist modulo 3 and replay with the naive lift; 24 sets did not).
- The inequality of section 3 counts a resource that almost every optimal circuit has in plenty. By itself it forbids
  nothing below Yates; it only says where a saving would have to be.
- Sections 2 and 3 are hand-derived in an hour. The lemma's proof is short; the reader should check the step "a gate new
  on R has two parents with non-proportional non-zero R-parts" and the bookkeeping of trivial classes.
- The by-product 2N - 2 - log2 N is linear; I did not check whether it is already known.
- The pencil's lower bound is the same for every 2 x 2 kernel: by k-cross's test it cannot be what separates H.
- The size was not pushed to 16 points by machine. By hand: composing 8-point circuits doubles the waste at an inner cut,
  so E - B = (3/8) N is reachable at Yates' count, always repaid [derived, not run].
- "Clean" classes are defined by the property the proof needs; "no straddling helper" and "no return" are the two that
  can be read off the wires.
- The no-return theorem was derived in the last twenty minutes of the hour. At 8 and 16 points it can only be checked for
  consistency (every circuit there has Yates' count or more); its proof is three lines and should be read by a skeptic.
  At 8 points the class contains no optimal circuit beyond the cancellation-free ones, so its extra width is unproven use.
- The known cancellation-free bound is quoted from search summaries of two arXiv papers, not from the papers; whether
  their proof already covers the no-return class is not checked. If it does, section 3b is a restatement.

## Files

`zmeter.py` (replay + plain and tilted meter, least and largest B over all orders), `meter_p2.out`, `meter_p3.out`;
`zpencil.py`, `pencil_p3.out` (mixed and pure wires, n(s) at twelve values of s, least E at six pairs);
`zcross.py`, `cross_p3.out` (deviation lemma, crossing-wire inequality); `ztree.py`, `tree_p3.out` (the inequality at every
node of the six trees); `zreturn.py`, `return_p3.out` (membership in the no-return class, all parent pairs, six trees); `zprice.py`,
`price_p3.out` (least number of returns at the root, and what they buy); `z16.py`, `z16.out` (the
meters on u-3's stored 16-point circuits); `z8_p2_full.out`, `z8_p3_full.out` (every optimal helper set modulo 2 and 3,
from d-0's `mincirc_all`).
