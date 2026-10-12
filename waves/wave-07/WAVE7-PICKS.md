# WAVE7-PICKS: ten briefs for developers (one hour each, heavier searches allowed)

11 October 2026, about 03:30 EDT. Curator w-pick, 15-minute box. Private; nothing reviewed, nothing in Lean, nothing published.
Marks: [read] = from tonight's reports; [derived] = by hand by the curator in minutes, checked by nobody; [guess].
Read for this page: s-cross.md in full; p-5.md in full; the openings of u-4, u-5, u-7, u-8, u-9; u-8 section 3; g-4 section 6;
the start of e2-0.md and of gen.py; the headers of the tools named below. NOT read: the skeptics' reports of wave 6 (not landed),
the bodies of u-4, u-5, u-7, u-9. The briefs are not ranked.

**Only growth laws in N count.** A better count at one size (18 gates at 8 points, say) is of no interest in itself; where a
brief names such a number it is a test of whether a mechanism exists, and the report must say what the mechanism does as N grows.

Two things a developer should know before trusting s-cross.md:
- its hybrid 2 lists three results as "BOX_INV3", "BOX_REF3", "BOX_TWO": these are unfilled placeholders. The local `s-cross/box.out`
  is a failed run (no numpy on the Mac) and `box2.out` is absent. The 3-call searches for involutions and reflections have no
  recorded answer [read: the files].
- `d-0-zeta/mincirc` holds at most about 6 million projective points, so at 8 points it works only modulo 2, 3, 5, 7. "A large
  prime field" needs another tool (brief 9 says which).

## Words used on this page

- N = 2^k *points*; an *address* is k bits. *The transform* H: the N x N matrix with entry (-1)^(number of common ones of the two
  addresses). *Textbook*: N log2 N gates.
- Count **(G)**: a gate is any a*u + b*v of two earlier values, scalings free. Count **(O)**: OpenAI's, additions and scalar
  multiplications each charged. Every brief uses (G) unless it says otherwise.
- *Wire*: a value the program holds, written as a vector over the N inputs. *Primitive form*: the wire scaled to whole numbers
  with no common factor. *Form* or *sign vector*: a wire with entries 0, +1, -1; its *set* is where it is not 0.
- *Flag*: a chain of subspaces of the addresses, each twice the size of the one before. Its *cosets* are the nodes of a *merge
  tree* (the sets on which partial sums live). *One-flag class*: circuits whose wires are all sign vectors on such nodes. Every
  record circuit of the night is in it. *The floor* of that class: f(N) = N - 1 + (N/2) log2 N gates (7, 19, 47, 111 at 4 to 32
  points), proved by hand twice (u-8 section 3, u-9 section 4), unreviewed.
- *Join*: a gate adding two wires on disjoint sets. *Shift*: w -> w - 2v where v equals w on v's set (it flips the sign of w
  there). *Quotient gate*: (u - v)/2 or (u + v)/2 of two wires that agree modulo 2.
- *Volume budget* (s-cross hybrid 3; it is Morgenstern's argument): write each gate between primitive forms as w = (a u + b v)/g,
  a and b whole numbers without common factor, g the common factor of the result. The gate's budget is log2((|a| + |b|)/g). The
  budgets of a circuit for H add up to at least (N/2) log2 N. A circuit of C*N gates therefore needs (log2 N)/(2C) per gate on
  average: coefficients that grow like a power of N, or wires that hold several binary digits at once.
- *Subset sums* Z: y_S = sum of x_T over the T inside S. *Yates*: the usual method, (N/2) log2 N gates. H = Z D Z^T with D the
  diagonal of the numbers (-2)^|S|, so Z in O(N) gates gives H in O(N) gates.
- Running exact programs: `python3 -B (not in this repository) wht35/bin/light.py <label> <seconds> <command>`.
  All paths below are under `waves/`.

---

## 1. twojobs: can one gate both join inputs and carry volume?

**Idea.** The floor f(N) is two budgets added: N - 1 gates that only connect inputs (joins, which bring no volume) and
(N/2) log2 N gates that each bring exactly one unit of volume (the coefficient-2 gates; every record has exactly that many
[read: s-cross hybrid 3]). In the one-flag class the two cannot be merged. Any circuit under the floor has a gate that does
both jobs or a gate that brings more than one unit. If each gate brings at most c units whatever N is, gates >= (N/2) log2 N / c
and the order stands; linear size needs gates that bring about log2 N units.
**Known specimens.** `u-4-zdz/hubparity8.txt` (26 gates): 5 of the 12 units are carried by joins, and it wastes more than it
gains. u-9's *dirty wires* (a form plus twice another form outside its set) get under the floor modulo 4 only.
**Start from.** `s-cross/pmeter.py` (the ledger; input format: see its `term` parser and the files it was run on),
`u-7-quotient/qa.py` (builds the 3,280 primitive vectors with entries 0, +1, -1 at 8 points), `e2-0-pieces/walk.py` (a local
walk: drop a helper, swap one, remove two and add one), `j-machine/steiner.py`, the search programs in `h-0-onepergate/` and
`h-5-ladderbound/`.
**First experiment.** At 8 points, pool = the 3,280 forms on ARBITRARY sets plus "form + 2 x form on a disjoint set"; a gate is
any a*u + b*v that lands in the pool. Walk from the 19 and from hubparity8. For every circuit kept, print: gates; the excess
e = gates - f(N); the number of joins that carry volume; the units brought per coefficient-2 gate; the largest coefficient.
Then widen the pool one step at a time (form + 4 x form; three forms) and repeat at 16 points against 47.
**Growth law it could reveal.** The largest number of volume units one gate can bring, as a function of the number d of binary
digits a wire may hold: constant (order stands), proportional to d (a circuit of N log N / d gates), or more.
**Keep asking.** Which gate here did two jobs, and would the number of such gates grow like N or like N log N?

## 2. digits: the transform one binary digit at a time

**Idea.** u-9 has a whole-number circuit of about 3.2 N gates (10, 26, 54, 110, 214, 418, 814 at 4 to 256 points) whose outputs
equal H modulo 4. It works because for odd numbers multiplying is adding modulo 4: (1 + 2a)(1 + 2b) = 1 + 2(a + b). A row of H
is a product of k sign vectors, so modulo 4 it is a sum, which a tree assembles with one gate per output. The published unit
does the mirror image: every wanted term sits one digit under an odd mixture and comes out by one quotient [read: u-5]. Exactness
needs k digits. So the question is the cost of digit j.
**Words.** *Dirty wire*: scaled to be odd on its set, it has entries equal to 2 modulo 4 outside its set. Digit expansion [read:
`m-cross/precision.py`]: H = sum over j of (-2)^j B_j, with B_j(y, x) = the binomial number C(m, j), m = the number of common
ones of y and x. Modulo 8 a *carry* appears: the product of two sign vectors is their sum minus 1 plus 4 x (the indicator of
where both are -1) [read: u-9 section 5].
**Two starting facts** [derived, minutes old, check them first]. (i) B_j = W_j^T W_j, where W_j has one row for each set U of j
address bits and entry 1 where U is inside the address: the digit expansion IS H = Z D Z^T sorted by the size of S. So "the cost
of digit j" is "the cost of the level-j slice of subset sums, in and out". (ii) B_j is zero wherever the two addresses have
fewer than j common ones, and the number of pairs with at least j common ones falls below N once j is above about 0.81 k: the
top fifth of the digits has fewer than N non-zero entries in all.
**Start from.** `u-9-checkerboards/dirty.py`, `dirty.out`; `m-cross/precision.py`; u-9.md sections 5 and 8 (item 2, "the carry
at modulo 8": 16 points, the 16 products of 4 x 4 sign vectors).
**First experiment.** Extend dirty.py to a circuit congruent to H modulo 8 at 16, 32, 64 points (annealed, replayed on all N x N
entries); record the extra gates for the third digit, c_3(N). Then c_4. Then the real question: build the digits from the TOP
(j = k downwards, where the slices are sparse) and from the bottom at once, and see where they meet.
**Growth law.** c_j(N), the cost of digit j. A constant times N per digit gives N log N and changes nothing. The order changes
only if the sum over j of c_j(N) is O(N) (costs that fall with j from both ends), or if one wire holding two digits serves two
layers, so that the number of layers is k/d.
**Keep asking.** Does any wire here hold two digits that are both used later, and what stops a wire from holding three?

## 3. floorhatch: release the floor's hypotheses one at a time, and measure what each buys as N grows

**Idea.** The floor theorem (u-8 section 3) is a recursion: gates >= 2 f(N/2) + N/2 + 1. Its steps use exactly three
hypotheses: every wire is a sign vector; every set is a node of ONE merge tree; every node is an affine set split into two
parallel halves. The hypotheses are the list of things to try.
**The proof in four lines** [read]. L, R = the halves of the root. (a) A full wire (no zero entry) is made only by a join of an
L-wire and an R-wire or by a shift of a full wire. (b) Projecting everything onto L gives a circuit of the same kind for the
half-size transform. (c) Each full wire has an image (its restriction to L, its restriction to R); the N rows give only N/2 + ...
distinct images because rows come in pairs, and one gate changes one coordinate of the image. (d) So full wires >= N/2 + 1 + the
new restrictions, and the recursion follows.
**Start from.** `u-9-checkerboards/cleangame.py` (the class as an exhaustive game; exact at 2 and 4 points),
`u-9-checkerboards/game8.py` (annealer at 8 points; found no 18), `u-8-compose/delta.py` and `recurse.py` (they check steps
(b), (c) on a given circuit), u-8.md section 3.
**First experiment.** Add ONE kind of illegal wire to the game and rerun at 8 points, then at 16 with the annealer:
(a) wires on a set that crosses the tree (a coset of a subspace not in the flag); (b) wires that are a form plus 2 x a form
outside their set; (c) wires on a set that is not affine (three quarters of a node). For each: least gates found, and the exact
line of (a) to (d) that fails when `recurse.py` is run on the circuit.
**Growth law.** Not "is 18 reachable" but: how many gates does ONE hatch wire save, as a function of the size of the node it
crosses? If the answer is "at most a constant", a circuit needs about N log N hatch wires and the floor's order survives; if a
wire crossing a node of size s saves about s or log s gates, say which, and write the recursion that replaces
t(k) >= 2 t(k-1) + N/2 + 1.
**Keep asking.** Which line of the proof used the hypothesis I just dropped, and is the term N/2 in the recursion still forced?

## 4. boxrelations: when can a transform used as a box be shared?

**Idea.** Every composition of the night calls a smaller transform on rows and then on columns: 2K calls of a K-point box for
K^2 points. s-cross hybrid 2 argues that 2K is forced for a *sealed* box. So any gain must use a relation of the box itself.
**Words.** *Call program*: the inputs are a K x K table x; call j computes c_j = A (L_j x + sum over i < j of M_ji c_i); the
outputs are Q x + sum of P_j c_j; L, M, P, Q are fixed matrices and A is the box. *Sealed*: the program must give (A x A) x for
EVERY matrix A. Lemma [read; derived there, twenty minutes old, unreviewed]: a sealed box needs r >= 2K calls (replace A by
t*A and compare powers of t). The proof says nothing once A^2 = 1 or A = A^T may be used.
**Start from.** `s-cross/box.py`, `box2.py` (least squares in floats; they need numpy, so run them on the Linux machine). The
results for involutions and reflections were never recorded: redo them first.
**First experiment.** K = 2, three calls, exactly: (i) every A with A^2 = 1; (ii) every symmetric A; (iii) both; (iv) A = one
fixed matrix, the 2-point transform. Method: the unknowns enter one group at a time linearly (fix L and M, solve P and Q by exact
linear algebra over the rationals or a large prime), so alternate exact solves from random starts, or find a float candidate
and recover the fractions. Then K = 4. In case (iv) the count is: least number of K-point transforms, applied to any vectors the
program builds, that give the K^2-point transform with O(K^2) other gates.
**Growth law.** r(K), the number of calls. With r(K) = a K and u-5's recursion c(K^2) = (a) c(K) + b for the cost per point:
a = 2 is the textbook (log N); the cost per point is (log N)^(log2 a), so a <= 1.866 is a saving of 1e-1, a = 1 gives
N log log N, a < 1 gives linear size [derived from u-5's recursion; check the arithmetic]. Report r(2), r(4) and, if a pattern
shows, the relation that produced it.
**Keep asking.** Which relation of the box did this program use, and does the transform have it at every size?

## 5. thirdturn-basis: the transform as a rotation by 120 degrees, in its own basis

**Idea.** Take k even, Q(x) = x1 x2 + x3 x4 + ... on the address bits, D = the diagonal of the signs (-1)^Q(x), and write the
transform with the two bits of each pair exchanged in the output address (a relabelling, free). Then R = D H / sqrt(N) satisfies
R^3 = 1 [read: s-cross hybrid 1, exact at 4, 16, 64 points]. Its fixed vectors form a space of dimension (N + 2)/3, and each
lives entirely on Q = 0 or entirely on Q = 1 (1 + 5 at 16 points, 7 + 15 at 64, 35 + 51 at 256). On the rest, H couples two
spaces of dimension (N - 1)/3 through a matrix U "at 60 degrees". One explicit fixed vector: the indicator of a subspace of
sqrt(N) addresses on which Q vanishes.
**Start from.** `s-cross/quadric.py`, `quadric.out`, `r3.py`; `u-7-quotient/qf.py`, `qh.py` (the 120-point block at 256 points
through the E8 roots; its 64 x 28 sign matrix is 28 columns of a 64-point transform); g-7.md (the third turn); g-0.md (how one
mirror was priced).
**First experiment.** At 16 and 64 points, exact: (i) the sparsest basis of the fixed space (try the indicators of all subspaces
of sqrt(N) addresses on which Q vanishes, with signs; do they span it; how many are needed); (ii) the gates (G) of the projection
onto it; (iii) the coupling U written in the bases that (i) suggests: is it a transform at fewer points, a subset-sum matrix, or
neither? Then count gates for H by "project, scale, couple".
**Growth law.** The recursion T(N) = sum of T(pieces) + c N that the split gives. Add the fractions size(piece)/N: below 1 is
linear, equal to 1 is N log N, above 1 is worse. s-cross's rough count is 4/4 + 1/3; the hour should replace "rough" by the true
pieces.
**Keep asking.** Is U a smaller copy of something I already know how to compute, and what is its size?

## 6. weightedz: subset sums with coefficients that grow

**Idea.** For subset sums the determinant is 1, so the volume wall is far lower: with coefficients of size 1, at least
N (0.277 sqrt(k) - 1) gates (g-4 section 6.3), against (k/2) N for Yates. Every model of waves 5 and 6 used gates u + v, u - v
only and all tied Yates. Linear size for Z needs an average budget of only 0.277 sqrt(k)/C per gate, far less than the direct
route for H. Nobody has searched Z with growing coefficients.
**Words.** *Weight blocks*: sort the sets by size; Z is then a block matrix whose blocks are inclusion matrices between levels.
*Symmetric-chain basis* B: a change of basis in which Z = B^-1 (Pascal blocks) B; the Pascal blocks cost O(N sqrt(log N)) with
coefficients 1 [read: g-4 6.4, i-cross hybrid 2, d-0 section 4]. So everything is the price of B.
**Start from.** `d-0-zeta/mincirc` (exact minimum modulo 3, 5, 7 with free coefficients; `z8_p3_all.out`, `z8_p5_m4.out`,
`z8_p7_m4.out` are already runs for Z at 8 points: read them before searching again), `u-3-zletter/` annealers,
`g-4-zetalead/fields.py` part D, `s-cross/zminor.py`.
**First experiment.** (i) Read what mincirc already says for Z at 8 points with free coefficients (is 12 the minimum modulo 5
and 7?). (ii) The growth part: build B exactly at k = 4, 6, 8 (16, 64, 256 points) from a symmetric chain decomposition, with
rational entries, and count its gates when coefficients are free: greedy elimination first, then anything better. Print
gates(B)/N and the largest coefficient against k.
**Growth law.** gates(B_k)/N as a function of k. Bounded would give Z, and so H, in O(N sqrt(log N)) gates: a saving of 0.5 in
the exponent. Growing like sqrt(k) gives the same. Growing like k says the change of basis is the transform again.
**Keep asking.** Where exactly does B need a large coefficient, and is that the same place where Yates spends its k/2?

## 7. unit-as-box: what relation does the published unit use that a sealed box does not have?

**Idea.** The published program is the only object that beats N log N. u-5 reads it as one identity: with D the move along a
direction p (*move* = one direction of the transform applied to one whole array), three additions between two arrays,
Y += D^-1 X, X -= D Y, Y += D^-1 X, give (X, Y) -> (-D Y, D^-1 X): both contents have moved along p and no move along p was
made. Brief 4's lemma says a sealed box cannot be shared. So the unit is not using its moves as sealed boxes. Name the relation.
**Words.** *Unit*: 120 source arrays, 120 target arrays, 783 helpers; five *invocations* of one helper circuit. *Port* of pair
t: its direction p_t, a 9-bit word. u-5's recursion: if a unit takes each array through m directions with a moves and b
additions per array, the cost per point obeys c(m F) = a c(F) + b; the textbook has a = m, the unit a = 44.905 for m = 45.
**Start from.** u-5.md lines 40 to 48, 204 to 212, 280 to 297; `u-5-unit2adic/unit2adic.py` (usage in its header: it reads the
published certificate, read only, with `python3 -I -B`), the ledgers `gcert1-e8-r783.ledger.tsv`, `s-cross/pmeter.py`,
tree R = `(not in this repository) wht-power-saving-r4-candidate` (READ ONLY; README sections 6 and 7).
**First experiment.** (i) Write the three-shear exchange as a call program in the sense of brief 4 (calls = moves along one
direction): count its calls against the sealed-box count, and list which relations it needs (guess of s-cross: moves along
different directions commute, and a sum of two arrays held after different moves is a shear along the difference).
(ii) Run the volume ledger on ONE invocation: total budget, quotient gates (u-5 counted 98,304), largest coefficient, budget per
gate against the plain schedule.
**Growth law.** a as a function of m and of the dimension r of a port. u-5: with one-dimensional ports the mechanism saves at
most one direction per array per unit. With ports of dimension r the count becomes 4 v r - 5 (rank) h. A saving of 1e-1 needs
a = m^0.9 (30.8 for m = 45), linear size a < 1: say which r, if any, the relation allows.
**Keep asking.** If the relation is "moves commute", why does it stop at one direction per array?

## 8. rotate by 120 degrees: two mirrors that can be chosen

**Idea.** With R = D H / sqrt(N) as in brief 5, R^3 = 1. A rotation is a product of two reflections in many ways; the single
mirror of the transform cannot be chosen, the pair can. g-0 priced one mirror (24 gates at 16 points, the route ties 56), never
a pair.
**Starting facts** [derived, minutes old, check first]. (i) The pairs are exactly: S1 any matrix with S1^2 = 1 and
S1 R S1 = R^-1, and S2 = S1 R. (ii) S1 = D is one of them, with S2 = H / sqrt(N): the trivial pair, one mirror free and the
other the whole transform. All others are S1 = D g with g commuting with R and D g D = g^-1; R's commuting matrices form a
large family (free maps on a space of dimension (N + 2)/3 and on one of (N - 1)/3 complex dimensions). (iii) If both mirrors
had bases of vectors with at most w1 and w2 non-zeros and every address lay in at most c of them, every row of R would have at
most (c w1)(c w2) non-zeros; R has N. So w1 w2 >= N / c^2: both mirrors sparse is impossible, sqrt(N) each is not excluded.
**Start from.** `s-cross/r3.py`, `quadric.py`; `g-0-mirror/` and g-0.md; `d-0-zeta/mincirc` (4 points directly; at 16 points
price a mirror through a basis as g-0 did).
**First experiment.** At 4 points list every S1 with entries in a small set (0, +-1, +-1/2, then free modulo 5 and 7) and price
S1 and S1 R. At 16 points parametrise g, and minimise (non-zeros of a basis of the mirror of S1) + (the same for S2); price the
best pairs.
**Growth law.** min over pairs of cost(S1) + cost(S2) at 4, 16, 64 points against N log2 N, and the shape of the best pair:
weights near sqrt(N) on both sides, or one side dense.
**Keep asking.** The transform's own eigenvectors need at least sqrt(N) non-zeros; does any such rule bind a mirror that only
has to turn R into its inverse?

## 9. nearlydependent: the one wall with a named door that no search has used

**Idea.** The volume argument, and Ailon's sharper form of it, forbid linear size only for circuits whose wires stay well
conditioned: about N log N / R gates when every intermediate state has condition number at most R [recalled in p-5, not
re-read]. For linear size R need only be about log N. So the door is mild. It was tried once (g-3: badly conditioned steps with
a well-conditioned product at 16 points bought nothing).
**Words.** *Quasi-entropy* of an invertible matrix M: p_il = M_il (M^-1)_li, Phi(M) = - sum of p log2 |p|. It adds over
Kronecker products: k N for H, 0 for subset sums. A well-conditioned gate raises it by about 2 at most. *Pump* (p-5 section 4):
on THREE wires with in-place moves row_i +- row_j, the largest |Phi| after m = 2..6 moves is 4, 6.5, 10.8, 14.8, 27.1: per move
2.0, 2.2, 2.7, 3.0, 4.5 and climbing; extremal state at m = 6: rows (0,3,5), (1,1,0), (1,3,3). On two wires it cannot happen.
Nobody knows how fast a pump can be SPENT, that is, brought back to a well-conditioned state that keeps the entropy.
**Start from.** `p-5-unimodular/inplace.py` (pump table and the meter), `words.py`; g-3.md and `g-3-illconditioned/`; d-5.md and
`d-5-border/border.py` (wave 1's huge coefficients); `d-0-zeta/mincirc.c` (note its limit: modulo 7 at most at 8 points).
**First experiment.** (i) Round trips. Extend inplace.py: 3 and 4 wires, one extra value allowed, moves with coefficients 1 and
2; for each m find the largest Phi of an END state all of whose p-entries have size at most 1 (well conditioned), reached
through any states. G(m) = that Phi / m is the round-trip gain per gate. (ii) A family with a parameter: circuits of fixed shape
whose coefficients are polynomials in e, exact for every e, with wires that become dependent as e -> 0; at 4 points look for 6
gates in the limit (7 is the minimum modulo 5 and 7 [read: p-5]), at 8 points for fewer than 19 (the minimum lies in 15..19).
Tool for a large field: fix the wiring, state "gate w lies in the span of u and v" as vanishing 3 x 3 minors, hill-climb over a
prime near 10^6, then lift and replay in fractions and read the sizes of the numbers.
**Growth law.** G(m) against m and against the condition number R allowed on the way: if G grows like R, linear size needs only
R about log N and the pump is a brick; if G stays near 2 for round trips, that is a new floor with no conditioning hypothesis.
Second law: least gates at 8 points as a function of the largest coefficient t (t = 1, 2, 4, ..., free).
**Keep asking.** I pumped; can I spend? What is the cheapest way back to a well-conditioned state, and does it give the gain back?

## 10. growinghubs: hubs A + t*B with t growing with the level

**Idea.** The second wave's family (7, 20, 52, 128, 304 gates; rate 3/4) rests on *mixed hubs* with coefficients +-1 only. If
every wire is, up to scale, a vector of 0, +1, -1, every gate has |a| + |b| <= 3 and the volume count gives at least
0.3155 N log2 N gates. A hub with a coefficient t that grows with the level is the only kind that leaves that world; with
coefficients up to t the same count gives N log2 N / (2 log2(1 + t)), which is linear for t a power of N. Never run.
**Words.** A cube of size m has halves L, R and each half has quarters. A character of the half is y_alpha. For a character
gamma of a quarter, a = (gamma, +) and b = (gamma, -) are its two extensions to a half. *Mixed hub*: M = (y_a on L) + c (y_b on
R). *Mixed-hub lemma* [read: e2-0 section 3]: with c = +-1 each of the four characters (a,+), (a,-), (b,+), (b,-) of the cube is
ONE gate from M, the partner (*witness*) being y_gamma on one quarter, a wire the grandchild already made. Recursion:
D(m) = 2 D(m/2) + 3m/4, T(N) = 2 D(N/2) + 5N/4 = (3/4) N log2 N + N/4.
**Starting fact** [derived, minutes old, check first]. With a free coefficient, M_t = (y_a on L) + t (y_b on R), the output
(a,+) minus M_t is zero on L and equals ((1 - t) y_gamma on the first quarter of R, (1 + t) y_gamma on the second). So the
witness is no longer a quarter piece but the weighted piece (gamma on R1) + s (gamma on R2) with **s = (1 + t)/(1 - t)**. That
map sends 1 -> infinity -> -1 -> 0 -> 1: the +-1 family lives on its one short orbit, which is why its witnesses are plain
pieces. A general t has an orbit of four weights t, (1+t)/(1-t), -1/t, (t-1)/(t+1); t = i and t = -i are fixed (a hub that is
its own witness, over the Gaussian rationals). Every wire of this game is (a character of a quarter) x (a vector of 4 numbers on
the four quarters), so the whole game is played in a space of 4 numbers per node and character.
**Start from.** `e2-0-pieces/gen.py` (the generator: functions `D`, `top`, `gate`, `solve2`; it replays in fractions),
`slp_8.txt`, `slp_16.txt`, e2-0.md sections 2, 3 and 5 (what keeps the rate at 3/4), WAVE2-NOTE.md idea A.
**First experiment.** Give gen.py one free coefficient t_j per level j and a table of the weighted pieces each node holds.
At 8 and 16 points solve for the t_j (as unknowns: the conditions "three wires are dependent" are polynomial) that make the
witness a node needs equal to a wire some lower node already holds for another purpose. Count gates as a function of the t_j.
Try the orbit of four, then t = i with Gaussian rationals, then t_j = 2^j.
**Growth law.** The rate r in gates = r N log2 N as a function of how fast t may grow: t bounded, t = k, t = 2^k, t = N. Below
3/4 is news for the family; below 1/2 is under the rate of the one-flag floor; a rate that falls like 1 / log t changes the
order.
**Keep asking.** With a free t, can one helper serve three levels in place of two, and what does the fourth weight of the orbit
want to be used for?
