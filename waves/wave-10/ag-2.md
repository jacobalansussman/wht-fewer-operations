# ag-2 the-first-bus-that-pays: every upper circuit, the ninth injection, and a third room (the triangle)

11 October 2026, 07:39 to about 08:35 EDT, 60-minute box. Private research: nothing published, no git, no Lean, nothing reviewed.
Marks: [ran] = exact run of mine in this hour (files in `ag-2-firstbusthatpays/`); [derived] = by hand in this hour, checked
by nobody; [read] = from tonight's reports; [guess].
Gate count everywhere: **(G)**, a gate is u + v. **TWO-ELEMENT FIELD in every line of this report**: every form, circuit,
count and "NO" is in arithmetic modulo 2. "None modulo 2" is not "none" over the rationals.

**No circuit below a known count and no growth law below N log N came out of this hour. Nothing here changes the order.**
The 31-gate question at 16 points is NOT decided. It is decided negatively in three named classes, for every upper circuit.
No bus paid. No delivery of any kind paid.

Words (as in ad-2). *Subset sums* Z on n points: output(S) = sum of the inputs at the subsets of S; f(n) = least gates
(4 and 12 at 4 and 8 points; Yates has (n/2) log2 n; at 16 points Yates has 32 and the question is 31). *Cut*: 2n points
split along one address bit into lower inputs x' and upper inputs x''; outputs Z x' and Z x' + Z x''. A wire is a pair
(lower part, upper part). *Pure*: upper part 0. *Mixed*: not. *M2 gate*: two mixed operands, mixed result. *Injection*: a
pure wire added to a mixed one. *Cancelling gate* or *delivery*: two mixed operands whose upper parts cancel; it hands a
pure form to the lower half. *Upper circuit* C'': the M2 gates seen with x' = 0; when there are exactly f(n) of them it is
a minimum circuit for Z on x''. *Version*: a mixed wire with the upper part of a wire of C'' and some lower part; a new
version costs one injection. *Slot*: one use of a wire of C'' (a gate that takes it, or its being an output). *Reach* of a
slot: the set of upper outputs it feeds, counted modulo 2. *Class*: the slots of one wire that use the same version; its
reach is the sum of its slots' reaches; its *offset* is that version's lower part minus the first version's. *Bus*: one
wire with 3 or more classes. *Derivation*: a minimum circuit as a list of gates (one wire set can be wired in several ways).
New words of this report. *Relation*: a set of mixed wires whose upper parts add up to 0. *Triangle*: a relation of three.
*Terms* L of a pure form: when the n injected wires are linearly independent, every lower part is a sum of some of them
in exactly one way; L is how many.

## 0. In ten lines

1. **The brief's first experiment is done** [ran]. `deco.py` ported to C (`decoA.c`); it reproduces ad-2's numbers on three
   upper circuits to the last digit (structures 29,316 / 390,378 / 90,622; ties 0 / 3,436 / 1,418). Then **every** upper
   circuit: the 6,960 derivations of the 2,802 minimum circuits at 8 points reduce, under the 6 permutations of the three
   address bits, to 470 wire sets with 1,208 derivations. Class A (12 M2 gates, 8 injections, a bus, up to 4 deliveries):
   **284,617,105 structures, never 11 pure gates. No 31-gate circuit in class A for any upper circuit.** Section 2.
2. **The brief's second experiment is done** [ran]: the general ninth injection (`decoB.c`): 9 classes whose reaches have
   one dependency, or 8 and one version used by nothing, the free form v taking every value that makes the lower total a
   difference of two versions of a wire with 4 or more classes. 500,858,276 structures, 1,746 million (structure, v) pairs,
   all 1,208 derivations: **none passes the exact search.** With 12 M2 gates and 9 injections, d(4) >= 2 for every upper
   circuit (ad-2 had it for 2 circuits and the idle kind only). Section 3.
3. **The brief's third item turned into a new room** [derived]. A 13th M2 gate with the upper part of an existing wire is
   not "one free form": it is **an injection whose pure wire need not exist**. It adds versions of two wires a and b and
   makes a new version of c = a + b whose offset is the sum of theirs. A cancelling gate then reads a sum over THREE wires.
   I call it a triangle. Section 4.
4. **The relation rule** [derived, exactly n injections]: any set R of mixed wires whose upper parts add to 0 can be added
   up with |R| - 1 gates and hands over a pure form of L terms; replacing that adder by L - 1 pure gates gives an honest
   circuit; so **gates >= 2 f(n) + n - sum over relations of (L - |R|)**. A bus is |R| = 2 (ad-2's r - 2). A triangle is
   |R| = 3: it pays L - 3, and L is the sum of three path lengths, so **wires with only two injections can take part** and
   the rank-3 wire is no longer needed. Section 4.
5. **The triangle is real at 8 points** [ran, `rule8.py`]: the 90 cuts of minimum circuits with a fifth M2 gate (ad-2's
   last row) each deliver a form of exactly 3 terms: a triangle that gains 0. The rule's prediction "pure gates + sum of
   (L - 1) >= f" holds on all 20,880 cuts. **On paper the triangle is five times roomier** [ran, C'' = Yates-like derivation 3001, all 4,698,161 groupings]: a bus
   of 3 or more exists in 390,378 groupings (8 %), longest 4, paper saving 2; a triangle with L >= 4 exists in 2,015,273
   (43 %), longest 6, paper saving 3.
6. **Realised: 0 again** [ran, `decoC.c`]. Triangle whose new version is used only by the cancelling gate, delivering the
   lower total (the only form that passes the census at this budget): all 1,208 derivations, 4,465,822,908 groupings, the
   total readable off a triangle in 72,118,500 of them: no candidate. So d(4) >= 2 there too.
7. **The regularity that will not go away** [ran]: in every complete choice of trees the joint search reached in the
   triangle room (13,447,158 of them, all 1,208 upper circuits), the delivered total has exactly L = 1 term: it IS one of the
   eight injected wires. Whenever the eight injected wires fit inside a lower half of 9 gates and the total can be read off
   a triangle at all, the triangle returns what was injected. L = 2, 3, 4 never occur. Section 4.
8. **What a cut is, one level up** [derived]: the reaches are wires (and partial fan-out sums) of the TRANSPOSED upper
   circuit, which computes superset sums. So a cut with n injections is a way of writing
   Z = sum over the n injections of (a wire of a circuit for Z transposed) x (a wire of a circuit for Z),
   and Yates is the two trivial ways (Z = Z . 1 = 1 . Z). A delivery is a short cycle of the upper circuit that passes
   many of the places where those terms are attached. Section 5.
9. **Growth law**: none new as a circuit. As a bound [derived]: ad-2's f(2n) >= 2 f(n) + 2n / rho becomes
   f(2n) >= 2 f(n) + n - (sum over the relations of L - |R|), and the entry price falls from "one wire with 3 independent
   consumers" to "4 injections around one gate". An order change still needs the relations of a cut to return nearly n
   gates in all, so L / |R| must grow without bound; at 16 points its largest value on paper is 2 for buses and for
   triangles alike (4/2 and 6/3). Section 6.
10. Still open at 16 points, named: a 13th M2 gate whose result is ALSO used by gates; 13 different upper forms (a
    non-minimum upper circuit); two or more deliveries with 9 injections (159 pairs qualify by ad-2's census); relations
    of four or more wires (two extra M2 gates); five or more deliveries in class A.

## 1. Tools and their checks [ran]

All three programs share one skeleton, a C port of `ad-2-twodeliveries/deco.py` with ad-2's exact search (`free8.c`)
compiled in. Input: `z8_sets.txt` (ab-4's 2,802 wire sets), `single8.txt` and `p??.txt` (ad-2's census of one and two
free forms). For one upper circuit a run takes 1 to 5 seconds (Python: 3 minutes).

- `decoA.c` (class A). For every grouping of slots into 8 classes with independent reaches and at least one wire with 3
  or more classes: forced offsets d = T^-1 Z; every set Dl of 1 to MAXD version differences on bus wires; three tests in
  order: (census) |Dl| + f(Z | Dl free) <= BOUND; (single edge) every wire's versions are connected by differences e with
  |Dl| + f(Z and e | Dl free) <= BOUND; (joint, exact) a spanning tree on every wire's versions, every delivery joining
  two versions at tree distance 3 or more, and |Dl| + f(Z and all injected wires | Dl free) <= BOUND, pruned wire by wire.
  BOUND = 11 is a 31-gate candidate, BOUND = 12 a tie.
- Checks against ad-2 [ran]: 6,960 derivations from 2,802 wire sets (same). Derivation 5001: 29,316 structures, none at
  12 (ad-2: 14 at best). Derivation 3001: 390,378 structures, 4,698,161 groupings in all, **3,436 structures at 12**
  (ad-2: 3,436). Derivation 1501: 90,622 structures, **1,418 at 12** (ad-2: 1,418). These were found by a different
  organisation of the search (necessary tests first, exact search last), so the agreement is a real check of both.
- Symmetry [derived, then sampled]: permuting the three address bits of both halves at once maps a cut circuit to a cut
  circuit with the same counts, so only wire sets that are the least of their 6 images need be run: 470 sets, 1,208
  derivations (Burnside would give 467 if no set were symmetric). A sample WITHOUT the reduction is in section 2a.
- `decoB.c` and `decoC.c` have **no positive control of their own**: both rooms are new and I know no circuit in them at
  16 points. They reuse the enumeration and the exact search that passed the checks above. What I could check
  independently is their algebra: a separate Python script took 40 structures printed by each at the tie level and
  recomputed the identity "sum of reach (x) offset = Z", the trees, and that the delivered form is the claimed sum
  (decoB: 9 classes, a sum of 3 tree edges of one wire; decoC: the number of terms L by brute force): 40 of 40 and
  40 of 40 [ran]. The 40 of decoB are all of the kind with a version used by nothing (they come first). See section 9.

## 2. Class A for every upper circuit [ran]

12 M2 gates, exactly 8 injections (extra = 0), a wire with 3 or more classes, delivery sets of size 1, 2 and 3 (size 4
in section 2a). Runs: `A_m4_r0.out`, `A_m4_r1.out` (rented machine), `A_m20_r*.out` (ten local runs). Together they cover every one of the
1,208 derivations exactly once (checked from the progress lines).

| | count |
|---|---|
| upper circuits (derivations, up to permutations of the address bits) | 1,208 (all 6,960) |
| structures (grouping with 8 independent reaches and a bus) | 284,617,105 |
| (structure, delivery set) passing the census, sizes 1 / 2 / 3 | 74,141,853 / 116,022,432 / 52,449,107 |
| ... then the single-edge test | 4,797,270 / 16,543,857 / 13,735,418 |
| ... then the exact joint search (pure + deliveries <= 11) | **0 / 0 / 0** |

**No structure of class A reaches 11, for any upper circuit.** ad-2 had 6 upper circuits and 1.6 million structures.
Four deliveries, and a sample without the symmetry reduction: section 2a.

What "tie" looks like across circuits (only where I ran BOUND = 12): 3,436 of 390,378 structures for the Yates-like
derivation 3001, 1,418 of 90,622 for derivation 1501, 0 of 29,316 for derivation 5001. I did not run the tie census for all
1,208; it is 10 times slower and a tie is a constant.

### 2a. Late runs

- **Four deliveries** [ran, `A4_m20_r*.out`, 20 of 20 runs finished, 1,208 derivations]: the same 284,617,105 structures; delivery
  sets of size 4: 16,722,480 pass the census, 4,520,355 the single-edge test, **0** the exact joint search. Never 11.
  Five or more deliveries: not run.
- **Without the symmetry reduction** [ran, the 174 derivations with index 7 modulo 40 of the full list of 6,960]:
  class A, `Anosym_m40_r7.out`: 40,551,655 structures, none at 11. Ninth injection, `Bnosym_m40_r7.out`: 71,414,690
  structures, 248,260,426 (structure, v) pairs, none. So the reduction did not hide anything in that sample.

## 3. The general ninth injection [ran]

12 M2 gates, 9 injections. Budget: 12 + 9 + pure + deliveries <= 31, so pure + deliveries <= 10. With one delivery w the
census needs f(Z | w free) <= 9, and by ad-2's census only the lower total has that (it saves 3). So the delivered form is
the total, the pure part is exactly an optimal 9-gate circuit given the total, and every injected wire lies in it.
Path length: replacing the cancelling gate by a chain of pure gates over the injected wires of its tree path (length p)
gives a pure circuit for Z, so 9 + (p - 1) >= 12: **the path has at least 4 injections**, hence a wire with at least 4
classes [derived]. With 9 classes the reaches have rank 8 and exactly one dependency Dep; the offsets are d0 + v on the
classes of Dep with v any form [read: ad-2]. A class of reach 0 is allowed (a block of slots whose reaches cancel) and so
is a version used by no gate at all (ad-2's idle version; I call it a ghost).

`decoB.c` enumerates every such structure with a wire of 4 or more classes; for each pair of versions on such a wire it
solves for the v that makes their difference the total (v is determined when exactly one of the two is in Dep; when
both or neither are, the difference does not depend on v and all 256 values of v are tried); then the single-edge test and
the exact joint search with the delivery at tree distance 4 or more.

| | count |
|---|---|
| upper circuits | 1,208 (all 6,960 up to bit permutations) |
| structures (9 classes of rank 8, ghost included, a wire with >= 4 classes) | 500,858,276 |
| (structure, v) with the total a difference of two versions on such a wire | 1,746,350,528 |
| ... then the single-edge test | 1,331,640 |
| ... then the exact joint search | **0** |

Files `B_m20_r*.out` (twenty local runs, each derivation once).
**With 12 M2 gates and a ninth injection of any kind, one delivery cannot give 31 gates, whatever the upper circuit.**
In ad-2's words: d(4) >= 2 in this class, against d(3) = 1. (d(k) as ad-2 lines 233 to 247 define it: what the mixed part
must spend beyond f(n) M2 gates and n injections so that a cancelling gate hands the lower total to a lower half whose
injected wires are all free given the total.)
Not covered here: two deliveries with 9 injections (pure + 2 <= 10 needs a pair that saves 4 or 5: 159 pairs by ad-2's
census).
Tie level, one circuit [ran, derivation 3001, BOUND = 11, 513 s]: 16,310,721 structures with a wire of 3 or more classes;
108,094 of them pass the exact joint search with one delivery on a path of 3. So the program does say YES when the budget
is one gate larger. Two warnings: that count ignores the order of events (section 4 shows a false tie of that kind in
the triangle room), and at this budget my pruning skips wires whose consumers have rank 2, so it is not a census of ties.

## 4. The third room: a 13th M2 gate is an injection whose pure wire need not exist [derived; then ran]

ad-2 expected "one free form per extra M2 gate". Playing with it gives something else.
Take a gate c = a + b of C''. It used one version of a and one of b; call the result the first version of c. Now spend
one more M2 gate on OTHER versions of a and b. The result has upper part c again, so it is a new version of c, and its
offset is (offset of that version of a) + (offset of that version of b). No pure wire was computed for it. It is an
injection paid in the mixed part: one gate, no pure wire, but the "injected form" is not free, it is a sum of offsets that
are already there. A cancelling gate between this new version and any version of c hands the lower half

    w = (path sum on a) + (path sum on b) + (path sum on c),

a sum that runs over three wires. More generally:

**Relation rule** [derived]. Let the injected wires be linearly independent (exactly n injections; then they are a basis
E of the lower forms, because the offsets are). Every lower part of every mixed wire is a sum of injected wires, in one way.
A relation R (mixed wires whose upper parts add to 0) can be added with |R| - 1 gates, the last of them cancelling; it
hands over a pure form w; let L be its number of terms in E. Replace that adder by a chain of L - 1 pure gates over the L
injected wires. Nothing else changes: the mixed part still has at least f(n) M2 gates and n injections, and the pure part,
now without deliveries, computes Z x' and all of E, at least c(Z and E) >= f(n) gates. Hence

    gates  >=  2 f(n) + n + (c(Z and E) - f(n))  -  sum over the relations of (L - |R|).

- Bus: |R| = 2 and L = path length p: p - 2. That is ad-2's ceiling.
- Triangle at a gate c = a + b: |R| = 3 and L = p_a + p_b + p_c, the three tree distances from the versions the gate
  itself used. It pays L - 3. With (p_a, p_b, p_c) = (2, 1, 1) the paper saving is 1 **without any wire of rank 3**.
- L = 1 means the relation returns one injected wire: nothing. L <= |R| never pays.
- The rule also says what any extra M2 gate can be worth: it lengthens a relation by one wire, so it pays only if that
  wire brings at least two more terms.

**The rule on real circuits at 8 points** [ran, `rule8.py`, `rule8.out`]. All 6,960 derivations of the minimum circuits
at 8 points, each in its 3 cuts (lower half 4 points, f(4) = 4): 20,880 real 12-gate circuits cut in two. For each: the
injected wires E, the delivered forms, their number of terms L in E. Predictions of the rule: every delivered form lies
in the span of E; pure gates + sum of (L - 1) >= 4; and the 90 cuts with a fifth M2 gate must deliver a form of 3 terms
or more.

| M2 | injections | pure | cancelling | L of each delivered form | pure + sum of (L - 1) | cases |
|---|---|---|---|---|---|---|
| 4 | 4 | 4 | 0 | (none) | 4 | 16,956 |
| 4 | 4 | 3 | 1 | 2 | 4 | 2,784 |
| 4 | 4 | 3 | 1 | **3** (a bus that gains 1) | **5**: the lower half it serves is one gate too dear | 180 |
| 4 | 4 | 2 | 2 | 2 and 2 | 4 | 126 |
| 4 | 5 | 2 | 1 | **3** (E dependent: 3, or 3 or 4) | 4: paid by the fifth injection | 672 |
| 4 | 5 | 1 | 2 | 2 and 3, or (1 or 2) and (3 or 4) | 4 or more: paid by the fifth injection | 72 |
| **5** | 4 | 2 | 1 | **3: a triangle** | 4: paid by the fifth M2 gate | 90 |

No delivered form outside the span, no violation, and the 90 cuts with five M2 gates all deliver exactly three terms.
(In the two rows with five injections E is dependent and a form has two expansions; I tested with the longer one, so
the test is weaker there.)
**So the triangle is not a paper object: it is in 90 cuts of minimum circuits at 8 points**, and there it gains
L - |R| = 0. The table is the wall REPAY in the words of this report: at 8 points a relation gains one gate in three
ways (a bus of 3, a bus of 3 with a fifth injection, a triangle of 3), and each time exactly one gate is paid back, by a
dearer lower half, by the injection, or by the M2 gate. A real saving is the first line of such a table in which the
gain column exceeds the paid column; at 16 points the three programs above found no such line.

**Paper capacity at 16 points** [ran: `decoCstat` with STAT=1, C'' = derivation 3001, every one of the 4,698,161 groupings
with 8 independent reaches]:

| the most classes on one wire (bus length r) | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| groupings | 1,145,728 | 3,162,055 | 380,919 | 9,459 |

| the most classes on the three wires of one gate (triangle L) | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|
| groupings | 290,176 | 2,392,712 | 1,761,864 | 245,638 | 7,771 |

A bus that could pay (r >= 3) exists in 8 % of the groupings and saves at most 2 on paper; a triangle that could pay
(L >= 4) exists in 43 % and saves at most 3. (The first table's last two entries add up to 390,378, ad-2's class A count:
a check.) The same over a tenth of the list (121 derivations, 440,204,791 groupings, `stat_m10_r0.out`): bus length
1 / 2 / 3 / 4 in 132,627,072 / 280,027,487 / 26,940,353 / 609,879 groupings (r >= 3: 6 %); triangle L = 2 / 3 / 4 / 5 / 6 in
32,673,594 / 240,265,837 / 147,769,721 / 18,918,832 / 576,807 (L >= 4: 38 %). Never a bus of 5, never L = 7.

**The search** [ran, `decoC.c`]. 13 M2 gates (the 12 of C'' and one triangle gate), 8 injections, the new version used by
nothing but the cancelling gate. Budget 13 + 8 + pure + 1 <= 31: pure <= 9, so again the delivered form must be the lower
total and the pure part an optimal circuit given the total. For every grouping with 8 independent reaches (no bus needed),
every three wires whose upper parts add to 0 and every choice of their versions: is the sum of the three lower parts the
total? Then the single-edge test, the joint search over trees, and at the end the relation rule: L >= 4 and
c(Z and injected, nothing free) <= 8 + L.

| | count |
|---|---|
| upper circuits | 1,208 (all 6,960 up to bit permutations), files `C_m20_r*.out`, each derivation once |
| groupings with 8 independent reaches (no bus needed) | 4,465,822,908 |
| ... in which the lower total is the sum of three versions whose upper parts add to 0 | 72,118,500 |
| ... then the single-edge test | 6,332,820 |
| ... then the joint search and the relation rule (L >= 4) | **0** |
| complete choices of trees reached by the joint search | 13,447,158, **every one with L = 1** |

**With 13 M2 gates of this kind and 8 injections there is no 31-gate candidate, whatever the upper circuit**: d(4) >= 2
here as well.
Independent check of the algebra [ran]: for 40 structures printed at the tie level a separate Python script recomputed
the identity "sum of reach (x) offset = Z" and the number of terms L by brute force over the 256 subsets of the injected
wires: 40 of 40 agree (`C_tie_examples_d3001.txt`).

**The regularity.** Every complete choice of trees that the joint search reached (all eight injected wires inside one
9-gate lower half, total readable off a triangle) has **L = 1**: the total is itself one of the eight injected wires, and
the triangle hands back what was put in. Not one case of L = 2, 3 or 4, in any batch. For L = 2 and 3 there is a reason of
sorts [derived, with a gap]: a 9-gate lower half that holds injected wires adding up to the total in 2 or 3 terms would
give Z in 10 or 11 gates; the gap is that the 9-gate circuit may itself use the total. For L >= 4 I have no reason. It
says that the two demands "the eight injected wires are a basis that lives in a cheap lower circuit" and "the upper
circuit's reaches for that basis let a short cycle pass four of them" have not met once.

At the tie level (BOUND = 11, one circuit, derivation 3001) the same program reports 5,965 structures, all with L <= 3.
**I checked one by hand and it is not a real tie**: the delivered form is y'_001 + y'_011 + y'_111, so the lower total must
exist before the delivery, and the 10-gate count had used the delivered form to make the total. The count ignores the
order of events, as ad-2's does; that can only make it too low. So the NO results stand, and I do not claim that ties
exist in the triangle room.

## 5. What a cut is, one level up [derived]

Write the n injected wires as the rows e_j of a matrix E and the reaches of the injections as columns rho_j (the reach of
an injection is the sum of the reaches of the versions behind it in its tree). ad-2's identity reads

    Z  =  sum over the injections j of  rho_j (x) e_j .

The e_j are wires of the lower circuit: forms that a circuit for Z on x' has or can afford. The rho_j are sums of slot
reaches of one wire of C''. Turn C'' around (every gate becomes a fan-out, every fan-out a gate): the turned circuit
computes Z transposed, superset sums, and the value on a wire is exactly that wire's reach. So **the rho_j are wires, or
partial fan-out sums, of a minimum circuit for Z transposed**. A cut with n injections is a way of writing Z as n products
"(wire of a circuit for Z transposed) times (wire of a circuit for Z)". Yates's two cuts are Z = Z . 1 (inject the inputs)
and Z = 1 . Z (inject the outputs); injecting the wires after stage one of the lower half onto the matching upper wires is
the middle one, and it ties too [derived by hand at 8 points].
In this picture the pure part must hold all of E AND all of Z x'; the mixed part computes Z x'' + (the rest of the work on
E); a relation is the only way the rest of that work comes back to the lower half without being paid twice.
A remark on what a cut is as a whole: its outputs are Z x' and Z (x' + x''), two copies of Z on the inputs x' and
u = x' + x'', and u costs n additions either way. So f(2n) lies within n of the cost of two copies of Z on unrelated
inputs. If two copies always cost twice one (the direct-sum question for linear circuits, which I believe is open
[recalled]), this gives only f(2n) >= 2 f(n) - n: it does not protect Yates's "+ n" at all. Whatever protects it is
about the n additions, that is, about relations. I did not get further.

## 6. Growth law [derived; a bound, no circuit]

With relations of any length: f(2n) >= 2 f(n) + n - G, G = the sum over the relations of (L - |R|). (Stated for exactly
n injections; with more injections count L by injection events and add the extra injections to the right-hand side.)
ad-2's table is the case |R| = 2. Four remarks.
- Entry price. A bus needs one wire with 3 independent consumers. A triangle needs 4 injections around one gate, which
  38 to 43 % of all groupings have (section 4). So the room is not small; the realised saving is 0 for another reason.
- A ceiling in one sub-class. If no injected wire lies on two relations, each wire of a relation contributes (its path
  length - 1), so G <= n - (number of wires that receive injections): with paths of length p everywhere,
  f(2n) >= 2 f(n) + n/p, half of ad-2's 2n/p. With p <= log2 n + 1 that is still N ln(log N) at best: far below the
  user's bar on paper, and unrealised.
- No ceiling in general. Relations may share injected wires (a bus of 4 versions already has 6 of them), and the sum
  above then counts a term several times; the honest quantity is "the pure cost of all the delivered forms from E, minus
  the gates of the relations", and the only bound I have for it is f(n). The far end shows it is not empty talk: with
  2 f(n) M2 gates (C'' once on x'' and once on x' + x'') n relations of two wires hand over ALL of Z x' and the pure part
  is empty: 2 f(n) + 2n gates, n worse than Yates. Yates is one end (pure part f(n), no relation), that is the other
  (pure part 0, n relations), and every search I know of tonight sits within one gate of the Yates end (m = 0 or 1 extra
  M2 gates). **The middle of that line (f(n) + m M2 gates, pure part f(n) - q, k relations, saving q - m - k) is where a
  saving has to be if there is one, and m larger than 1 has not been looked at** [read: the briefs; I did not check
  every report]. At 8 points no minimum circuit has m >= 2 in any cut [read: ad-2's table, M2 is 4 or 5].
- For an order change G must be n - o(n) per cut, so the average of L / |R| must grow without bound. At 16 points the
  largest L / |R| on paper is 6/3 for a triangle against 4/2 for a bus: the same 2. I have no size where it is larger.
**Measured: every relation of 2 or 3 wires, in everything searched at 16 points, saves 0.**

## 7. Went around

- "Port and run all 6,960" could have been a night; yes, and: put the necessary tests first and the exact search last,
  and use the symmetry: the whole of class A took minutes, which left time for the other two rooms.
- "The general ninth injection has 255 free forms"; yes, and: the delivery fixes v except in one case, so the loop
  over v nearly disappears.
- "Redo the version lemma for a 13th M2 gate"; yes, and: do not redo it, read the gate as an injection that costs no
  pure wire. That gave the triangle and the relation rule, and moved the entry price from rank 3 to rank 2.
- The triangle said "FOUND, 7,245 structures" at the first run. It was the total injected and read back (L = 1). Asking
  what that failure was made of gave the term count L and the test L >= 4; and then the regularity "L is always 1".

## 8. Mutations (not judged)

1. **The 13th M2 gate whose result is used by gates.** Then the new version takes over some slots of c, and an injection
   on a reaches PART of c's consumers: finer reaches for one gate. No delivery is needed for that, so it costs 1 and saves
   nothing alone; with a relation it changes which bases E are possible. Same program, one more loop over the slots of c.
2. **Thirteen different upper forms**: C'' not minimum. The version lemma holds for it as it stands; what changes is the
   list of circuits (13-gate circuits for Z at 8 points, far more than 2,802). `d-0-zeta/mincirc` can list them.
3. **Explain L = 1.** Take one optimal 9-gate circuit given the total, list every basis E inside it, compute
   T = Z E^-1 and ask directly which columns are slot sums of some minimum circuit turned around. It is a question about
   pairs (circuit for Z, circuit for Z transposed), not about a search over structures.
4. **Relations of four wires** (two extra M2 gates): L - 4 with L up to 8. Only worth it where L >= 5.
5. **Two deliveries with 9 injections**: the 159 pairs worth 4 or 5.
6. **32 points**: f(16) is not known, so "exactly f(n) M2 gates" cannot be used; with Yates on 16 as C'' and 32 as the
   budget the same three programs run after changing the constants, and the paper ratio L / |R| can be measured there.
   That number, not the search, is what a growth law needs.
7. **Other fields**: the relation rule uses nothing about the field [derived]. Over the rationals a version is (a, c b)
   with a scalar c and a relation is a linear dependency with any coefficients, so there are more relations per circuit.

## 9. Criticism, last

- Everything is modulo 2, for one cut of 16 points, with exactly 12 or 13 M2 gates. A 31-gate circuit may have a cut
  outside all three classes; the open ones are listed in line 10 of section 0.
- All NO results rest on ad-2's version lemma (by hand, unreviewed) and on f(8) = 12 and the list of 2,802 minimum
  circuits (exhaustive modulo 2, ab-4's run, not re-run by me).
- The relation rule, the reading of the 13th gate, the transposed-circuit remark and the ceilings of section 6 are by
  hand in this hour. The rule's proof assumes the adder's gates are used for nothing else. Its purification half was
  tested on the 20,880 cuts at 8 points (section 4) and held; that is one size, and those circuits are all ties.
- `decoB.c` and `decoC.c` have no positive control: I know no circuit in either room at 16 points, and my programs handle
  only the cut of 16. The right control is the 8-point tie with a fifth M2 gate (ad-2: 90 cuts; `rule8.py` confirms each
  is a triangle of 3 terms) and ad-2's 224 ties with an idle version; that needs the programs generalised to n = 4.
  Not done. Only their algebra was checked (section 1).
- The triangle search covers the "idle" 13th gate only and only relations of three wires of C'' as they stand.
- The symmetry reduction is argued, and sampled without reduction on a fortieth of the list (section 2a), not run in full.
- The joint search ignores the order of events (a delivered form used to build a wire the delivery needs). That makes
  counts too low, never too high: the NO results stand; the "ties" of the triangle room do not (one checked, false).
- Delivery sets in class A: sizes 1 to 4. ad-2's program took all sizes (for its six circuits).
- The keys of the joint-search cache are 64-bit hashes of (delivered forms, injected set): a collision could turn a YES
  into a NO. I consider it negligible and did not measure it.
- The rented machine was loaded (load 10). The two class A jobs for half of the list finished there and are used; I
  stopped my two triangle jobs there after 7 minutes and ran the triangle room, the ninth injection and the rest
  locally. The partial triangle files from that machine (`C_m4_r*.err`) are kept and are not used in any count.
- Nothing here changes the order, or any constant.

## Files

`waves/wave-10/ag-2-firstbusthatpays/`:
- `decoA.c` (class A; usage `decoA z8_sets.txt single8.txt <dir of p??.txt> M r [MAXD] [stop after derivation]`, runs the
  derivations with index = r modulo M; environment BOUND (11 = candidate, 12 = tie), SYM=1 for the symmetry reduction).
  `decoB.c` (ninth injection; BOUND 10 = candidate). `decoC.c` (triangle; BOUND 10 = candidate; STAT=1 prints the paper
  capacity instead; the runs used the binary built before STAT was added, `decoCstat` is the one with it).
- `A_m4_r0.out`, `A_m4_r1.out`, `A_m20_r*.out`: class A, all 1,208 derivations. `A4_m20_r*.out`: class A with up to four
  deliveries. `Anosym_m40_r7.out`, `Bnosym_m40_r7.out`: samples without the symmetry reduction.
- `B_m20_r*.out`: ninth injection, all 1,208. `C_m20_r*.out`: triangle. `C_m4_r*.err`: the abandoned rented runs.
- `stat_m10_r0.out`: paper capacity on a tenth of the list. `*.err`: progress lines and the job runner's last line.
- `rule8.py`, `rule8.out`: the relation rule on the 20,880 cuts of minimum circuits at 8 points.
- `C_tie_examples_d3001.txt`, `B_tie_d3001_partial.out`: structures printed at the tie level, used for the independent
  check of the algebra (the second run was cut at 240 s on purpose).
- Copies of `decoA.c`, `decoC.c` and the inputs on the rented machine under `(the Linux machine's working folder)/ag-2-firstbusthatpays/`.
