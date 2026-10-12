# ad-2 two-deliveries: what a second cancelling gate is worth, and what a cut really is

11 October 2026, 06:23 to 07:08 EDT, 60-minute box. Private research: nothing published, no git, no Lean, nothing reviewed.
Marks: [ran] = exact run of mine in this hour (files in `ad-2-twodeliveries/`); [derived] = by hand in this hour, checked by
nobody; [read] = from tonight's reports; [guess].
Gate count everywhere: **(G)**, a gate is u + v. **TWO-ELEMENT FIELD in every line of this report**: every form, circuit,
count and "NO" below is in arithmetic modulo 2, and "none modulo 2" is not "none" over the rationals.

**No circuit below a known count and no growth law below N log N came out of this hour. Nothing here changes the order.**
The 31-gate question at 16 points is NOT decided; it is decided negatively in two named classes (section 4).

Words. *Subset sums* Z on n points: the output at a set S is the sum of the inputs at all subsets of S. f(n) = least gates
for Z (4 and 12 at 4 and 8 points; Yates has (n/2) log2 n). *Cut*: 2n points split along one address bit into lower inputs
x' and upper inputs x''; the outputs are Z x' (lower) and Z x' + Z x'' (upper). A wire is a pair (a, b): its lower part a
and its upper part b. *Pure* wire: b = 0. *Mixed*: b not 0. Gates of a cut [read: ab-5]: *M2* (two mixed operands, mixed
result; at least f(n) of them), *injection* or *M3* (a pure wire added to a mixed one; at least n of them), pure gates, and
the *cancelling gate* or *delivery* (two mixed operands whose upper parts cancel: a pure form is handed to the lower half).
*extra* = (M2 gates - f(n)) + (injections - n). A circuit with 2 f(n) + n - 1 gates needs pure gates <= f(n) - 1 - extra.
s(W) = what a set W of forms saves the lower half when given at no cost (f(n) minus the least gates with W free).

## 0. In ten lines

1. **Experiment (i), the census of all 30,381 pairs of free forms at 8 points [ran, exhaustive].** Pair savings 0, 1, 2, 3,
   4, 5 occur 344, 11,732, 15,527, 2,619, 156, 3 times. The best pair (the total of all eight plus one of the three face
   outputs) saves 5 = 3 + 2, exactly the sum. 760 pairs save more than the sum of the two (755 by one gate, 5 by two);
   649 of those are explained by the third form a + b that one gate makes from the pair; **111 pairs have real synergy,
   always exactly one gate**. Section 1.
2. **Is the second delivery worth more because the first is there? In the lower half: rarely.** Of 60,762 ordered pairs
   the second form is worth more after the first in 1,520 (2.5 %), the same in 33,754, less in 25,488 (42 %). After the
   total, no form gains and 143 of the 212 that were worth something lose everything. Deliveries are mostly substitutes for each other. Section 1.
3. **The cut is a decorated circuit** [derived; validated by two runs at 8 points]. When the mixed part has exactly f(n)
   M2 gates, every mixed wire is a *version* of a wire of one minimum circuit C'' for Z on the upper inputs (same upper
   part, another lower part); a new version costs one injection; and **a cancelling gate is the sum of two versions of
   one wire**. All decorations come from one free choice per gate: which lower part each of its two operands carries.
   Section 2.
4. **Two deliveries that share exist, and their name is a bus** [derived]. A wire carried through r versions by r
   injections is a *bus*: ANY two of its versions can be added, one gate each. A second delivery on a bus costs no
   injection at all: yes, it is cheaper because the first is there. But the whole bus saves the lower half at most r - 2
   gates however many deliveries read it. Hence, in every cut with exactly f(n) M2 gates:
   **gates >= 2 f(n) + sum over the upper wires of min(injections on that wire, 2)**; Yates and the 8-point tie both
   meet it with equality. Below Yates means: the lower half enters through fewer wires than it has points. Checked on
   all 20,790 cuts of minimum circuits at 8 points that have 4 M2 gates: no violation; 198 of those cuts already hold
   TWO cancelling gates, all at a tie. Sections 2 and 3.
5. **With exactly n injections everything is forced** [derived; ran]: the injected lower parts are determined by which
   consumers use which version (they are (T transposed)^-1 Z, T the matrix of "which outputs does this version reach"), so a bus of
   length r without an idle injection needs a wire of C'' with r consumers whose reaches are independent.
6. **The longest such bus is log2 n + 1 at 4 and 8 points, in EVERY minimum circuit** [ran: all 8 derivations at 4 points,
   all 6,960 derivations of the 2,802 minimum circuits at 8 points]: 3 and 4. Never 5 at 8 points.
7. **Experiment (ii), 16 points [ran].** Class A: C'' = Yates, 12 M2 gates, 8 injections (extra = 0), every way of
   grouping the consumers into versions with a bus of 3 or more: 390,378 structures, each with its forced lower parts,
   every tree, every set of deliveries. Least pure gates: 12 in 3,436 structures, never 11. **A delivery ties and never
   pays.** Five other minimum circuits (1,204,487 more structures): one gives the same table (I believe it is Yates
   with the bits permuted), one with a cancellation inside ties in 537 structures, two more tie in 1,418 and 499, one
   never gets below 14. **Never 11 in any.** Section 4.
8. **d(4) >= 2 in a class of 4.7 million structures** [ran; see section 4 for the run's last line]. Class B: C'' = Yates,
   8 independent injections plus ONE idle version placed anywhere on any wire, the cancelling gate delivering the lower
   total, pure part 10. The same program finds the 8-point tie (d(3) = 1) 224 times; at 16 points it finds nothing.
   ab-5 had six skeletons; this is every decoration of Yates with one idle version. The same NO for a minimum circuit
   with a cancellation inside (4.2 million structures). Not covered: the other C'', a 13th M2 gate, a ninth injection
   that IS used by a gate.
9. **Growth law it gives, as a ceiling and not as a circuit** [derived]: if every cut is tight and the longest bus is
   rho(n), then f(2n) >= 2 f(n) + 2n / rho(n), that is f(N)/N >= the sum over the levels of 1/rho. rho = 2 is Yates;
   rho = 3 for ever allows (1/3) N log2 N; rho = log2 n + 1 (what the minimum circuits have) allows N ln(log2 N); a
   saving exponent e needs buses of length about 2 (log2 N)^e / (1 - e) on nearly every injection, each saving its full
   ceiling: 3 to 5 for e = 0.1. Linear size needs bus lengths whose reciprocals have a finite sum. Measured so far,
   in the classes searched: every bus saves 0 net. Section 5.
10. The better question, section 6: **on a bus, the three injected wires and the delivered wire are four pure wires that
    add up to zero; when does the lower half need all four and yet have no cheaper relation among them?** In the
    ties I looked at (a handful of the 3,436) it has one.

## 1. Experiment (i): the census of pairs at 8 points [ran, exhaustive, two-element field]

Tool: `free8.c`, the same search as ab-5's `mincirc_free` (sets of m intermediate forms, a target is added the moment it
is a sum of two available forms), run in-process for many free sets. Checks first: 4 points without free form 4 gates, 8
points 12 gates; the single-form census reproduces ab-5's exactly (4 points: 2, 8, 1 forms saving 0, 1, 2; 8 points: 34,
168, 44, 1 forms saving 0, 1, 2, 3). Then all 247 x 246 / 2 = 30,381 pairs, each to its exact minimum (`p??.txt`,
`pairs_analyse.py`, about 3 minutes in all).

| saving of the pair | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| pairs | 344 | 11,732 | 15,527 | 2,619 | 156 | 3 |

| saving of the pair minus (saving of a) minus (saving of b) | -2 | -1 | 0 | +1 | +2 |
|---|---|---|---|---|---|
| pairs | 453 | 12,291 | 16,877 | 755 | 5 |

- The three pairs that save 5: the total x0 + ... + x7 with x0+x1+x2+x3, with x0+x1+x4+x5, with x0+x2+x4+x6 (the three
  outputs on a face through the origin). 5 = 3 + 2. Triples by hand: the total and two of those faces save 7, all three
  save 9 (`triples_top.out`): additive, and trivially so, because an output given free is an output not computed.
- The 5 pairs at +2 are two worthless forms whose sum is the total: one gate makes the total. Not synergy.
- Of the 760 pairs above the sum, 649 are explained by the third form a + b (one gate): the pair is worth what a + b and
  the better of the two are worth, minus that gate. **111 pairs are not explained that way.** Example: x1+x2 alone saves 0,
  x1+x3+x4+x5 alone saves 1, their sum saves 1, the pair saves 2. In every one of the 111 the excess is exactly 1.
- Net worth in a cut (each delivery costs its own gate): best single form 3 - 1 = 2 (the total); best pair 5 - 2 = 3.
  The pair's net beats the best single net of its two forms in 131 pairs (5, 33, 90, 3 at pair net 0, 1, 2, 3).
- **The brief's question, in the lower half alone.** Worth of the second form alone against its worth once the first is
  given, over the 60,762 ordered pairs: more in 1,520, equal in 33,754, less in 25,488. With the total as the first form:
  of the other 246 forms none is worth more afterwards; 34 were worth 0 before; 54 keep their worth (only the three
  face outputs keep 2), 15 fall from 2 to 1, and 143 fall to 0.

So the lower half does not reward a second delivery: savings there are sub-additive in 42 % of pairs, additive at the
top, and super-additive by one gate in a few. If a second delivery is to be cheap, it must be cheap in the mixed part.

## 2. What a cut is: versions, offsets, buses [derived; two-element field, though nothing in the argument uses the field]

Assume the mixed part has exactly f(n) M2 gates (the lemma's minimum).

**Versions.** Put x' = 0: pure wires vanish, injections become copies, the M2 gates alone compute Z x''. If an M2 gate
made an upper part that already exists, deleting it would leave a circuit with f(n) - 1 gates. So the upper parts of the
M2 gates are f(n) different new forms: they are a minimum circuit C'' for Z on x''. Every mixed wire is (a, b) with b one
of the n + f(n) wires of C''. Call the wires with the same b the *versions* of b. The first version is the input (a = 0)
or the M2 gate's result; every other version is made from an earlier version of the same b by one injection. So the
versions of b form a tree whose edges are injected pure wires. **A cancelling gate adds two versions of one b and hands
over the sum of the injected wires on the tree path between them.** (ab-5 said "an adder with many inputs over the pure
wires injected onto one mixed wire"; this is that sentence with its tree.)

**A path of 1 or 2 injections delivers nothing new**: the sum of one or two pure wires costs at most one pure gate
anyway. A delivery beats a pure gate only when its path has 3 or more injections, and then by (path length - 2).

**Slots and offsets.** A *slot* of a wire b of C'' is one use of it: a gate of C'' that takes it, or its being an output.
Each slot uses one version; write d(slot) for that version's lower part minus the first version's. Let sigma(slot) be the
set of outputs that slot reaches (counted modulo 2: the outputs reached through the gate, or the output itself). Then the
lower parts of the upper outputs are right exactly when

    sum over all slots of  sigma(slot) (x) d(slot)  =  Z        (an n x n identity; 32 slots at n = 8 for Yates).

All solutions come from one free choice per M2 gate: which lower part each of its two operands carries in [derived: the
solution space has dimension 2 x f(n) x n, and "move a lower part from one operand of a gate to all users of its result"
spans it]. Yates is two of the solutions: every operand carries its mirror image (inject x'_j onto x''_j, n injections at
the inputs), or every operand carries nothing (add the finished lower output at the end, n injections at the outputs).

**With exactly n injections everything is forced.** Group the slots of each wire into classes by version. Each class k
with a non-zero offset d_k costs at least one injection and has a reach tau_k = the sum of its slots' sigma. The identity
reads sum_k tau_k (x) d_k = Z, and Z has rank n. So n injections means: the n reaches are a basis, and the offsets are
**d = (T transposed)^-1 Z**, T the matrix of reaches: no freedom at all, and the offsets are a basis too. A ninth
injection is *idle* when its reach depends on the others; the idle injection of the 8-point tie has reach 0 (its version
is used by no gate, only by the cancelling gate).

**Bus.** A wire with r injections on it. Any two of its r + 1 versions can be added: up to r (r + 1) / 2 deliveries,
one gate each, no further injection. **That is the object "two deliveries that share their cost".** Its ceiling
[derived]: r - 1 pure gates make every version's offset from one base version, and then every delivery is one pure gate
or none; so the bus saves the lower half at most r - 1 - (number of deliveries ending at the best base) <= r - 2 gates,
however many deliveries read it. With i idle injections on it the net is at most (r - i) - 2. So:

- one delivery on a path of r: at most r - 2;
- a second delivery on the same bus: no mixed cost, one gate, and it can only pay inside the same ceiling r - 2;
- a bus pays (net >= 1) only with 3 or more injections that are not idle, so only on a wire of C'' that has 3 slots
  with independent reaches. An idle injection never raises the ceiling; what it buys is freedom in the offsets (one free
  form v, added to every offset in the dependency).

**The cut inequality with buses** [derived from the ceiling, bus by bus]. Let r_b be the number of injections on the
wire b of C''. In every cut whose mixed part has exactly f(n) M2 gates,

    gates  >=  2 f(n) + sum over the wires b of min(r_b, 2).

Each wire that receives injections costs 1 if it receives one and 2 however many more it receives. Yates has n wires
with one injection each: 2 f(n) + n, with equality. The 8-point tie has three wires with 3, 1, 1 injections:
2 x 4 + 2 + 1 + 1 = 12, with equality again [checked by hand on ab-5's reading of d-0's circuit]. A circuit below Yates
needs sum of min(r_b, 2) < n while the sum of r_b is at least n: **the lower half must enter the upper computation
through fewer wires than it has points**, and through o(n) wires for a change of order.

## 3. The inequality on every minimum circuit at 8 points, and how long a bus can be [ran, two-element field]

`cutineq.py`, `cutineq.out`: all 6,960 derivations of ab-4's 2,802 minimum circuits (12 gates), each in its 3 cuts:
20,880 cases, gates sorted into M2, injections, pure, cancelling.

| M2 | injections | pure | cancelling | injections per upper wire | bound 8 + sum of min(r, 2) | cases |
|---|---|---|---|---|---|---|
| 4 | 4 | 4 | 0 | 1, 1, 1, 1 | 12 | 6,588 |
| 4 | 4 | 4 | 0 | 2, 1, 1 or 2, 2 | 12 | 9,540 |
| 4 | 4 | 3 | 1 | 2, 1, 1 or 2, 2 | 12 | 2,388 |
| 4 | 4 | 4 or 3 or 2 | 0 or 1 or 2 | **3, 1** | **11** | 828 + 576 + 90 |
| 4 | 4 | 2 | **2** | 2, 2 | 12 | 36 |
| 4 | 5 | 2 | 1 | 3, 1, 1 or 3, 2 | 12 | 672 |
| 4 | 5 | 1 | **2** | 3, 2 | 12 | 72 |
| 5 | 4 | 2 | 1 | (the version lemma does not apply) | | 90 |

- **No violation in the 20,790 cases with 4 M2 gates.** The bound is met with equality except in the 1,494 cases with
  the pattern 3, 1, where it says 11 and the circuit has 12: a bus of three injections, none idle, exists in a minimum
  circuit and still saves nothing.
- **Two cancelling gates in one cut already occur at 8 points: 198 cases** (90 on a bus of three with no idle
  injection, 72 with five injections, 36 on two wires). Nobody had looked. All are ties: 12 gates.
- The tie can also be paid by a fifth M2 gate in place of the fifth injection (90 cases, last row). So "extra" has two
  forms at 8 points, and my class B covers only the first.

Now the capacity.

`ranks.py`: for every wire of every minimum circuit, the rank of its slots' reaches = the longest bus without an idle
injection.

| lower half | minimum circuits (every way of deriving every wire) | largest rank on any wire |
|---|---|---|
| 4 points (cut of 8) | 8 | 3 (on 6 wires in all); never 4 |
| 8 points (cut of 16) | 6,960 derivations of ab-4's 2,802 wire sets | 4 in 4,314, 3 in 2,646; **never 5** |

In Yates the rank of a wire is (the number of consecutive stages it waits through) + 1 [derived], at most log2 n + 1,
reached only by x''_0; ranks 4, 3, 3 on x''_0, x''_4, x''_0 + x''_1 at 8 points and 2 or 1 elsewhere. The sum over the
wires of (rank - 2), the most all buses could save together, is at most 4 at 8 points in every minimum circuit.
Guess: log2 n + 1 is the maximum at every size.

## 4. Experiment (ii): 16 points [ran, two-element field]

Program `deco.py`. For a given C'' it enumerates every grouping of slots into classes with n independent reaches,
solves for the forced offsets, takes every spanning tree on the versions of every wire (the tree's edges are the
injected pure wires), every set of deliveries with a path of 3 or more, and asks `free8` for the exact least number of
pure gates (targets: the lower outputs and the injected wires; the deliveries free, one gate charged for each). A filter
from the census of section 1 comes first: a set D of deliveries can pay only if s(D) >= |D| + 1.
Check at 8 points (all 8 minimum circuits for the half): 42 structures with a bus; in 36 no delivery passes the filter,
in 6 the lower total is delivered and the pure part then costs 5; so 4 or more in all: no 11-gate circuit at 8 points
in this class, as known. `deco4_extra0.out`.

**Class A: 12 M2 gates, 8 injections (extra = 0), at least one bus of 3.**

| C'' | structures | least pure gates over them (12 = tie; 11 would be a 31-gate circuit) |
|---|---|---|
| Yates, textbook derivation (`deco8_yates1.out`) | 390,378 | 12 in 3,436; 13 in 17,415; 14 or more in 75,039; 294,488 fail the census filter (so 12 or more). **Never 11.** |
| derivation 3001 of ab-4's list (`deco8_d3001.out`) | 390,378 | the same table to the last digit (I believe it is Yates with the bits permuted; not checked) |
| derivation 5001 (rented machine, `deco8_d5001.out`) | 29,316 | 14 at best: this circuit's wires have rank 3 at most and its forced offsets are expensive |
| derivation 1501 (`deco8_d1501.out`; three wires of rank 3, none of rank 4) | 90,622 | 12 in 1,418; 13 in 4,909; 14 or more in 21,647; 62,648 fail the filter. **Never 11.** |
| derivation 4201 (`deco8_d4201.out`) | 335,460 | 12 in 499; 13 in 4,400; 14 or more in 46,533; 284,028 fail the filter. **Never 11.** |
| derivation 6501 (rented machine, `deco8_d6501.out`): a circuit that is NOT adding-only (it holds x''0+x''4+x''5+x''6 and makes an output by cancelling x''5) | 358,711 | 12 in 537; 13 in 5,495; 14 or more in 57,587; 295,092 fail the filter. **Never 11.** |

How to read the table: the counts are the least pure gates when at least one delivery is used; a structure listed at
13 or more is one where using its bus is worse than ignoring it (without deliveries every structure needs 12 or more,
because the pure part then contains a whole circuit for the lower half).

A tie of the new kind, for the record: the wire x''_0 + x''_1 in three versions with lower parts x'0+x'1+x'2+x'3,
x'0+x'1 and x'0+x'1+x'4+x'5 (so three of the lower OUTPUTS ride on one upper wire, injected in the order
y'_011, then x'2+x'3, then x'4+x'5), and one cancelling gate reads off y'_101. It costs one gate and replaces one gate.
The delivered wire is the sum of three injected wires, but two of them already add up to a wire the lower half has
(y'_011 + (x'2+x'3) = y'_001). That is the pattern in the ties I looked at.

**Class B, the brief's d(4): one idle version, the cancelling gate delivers the lower total.** With the total free the
lower half costs 9 [ran]; the delivery itself is 1; so 31 gates need 12 + 9 + 10 with every one of the 9 injected wires
free in one optimal 9-gate circuit given the total. Only 29 forms (the 8 inputs and 21 others) are free in that sense
[ran]. The program enumerates ALL groupings with 8 independent reaches (not only those with a bus), allows one more
version with any offset v at any place of any wire's tree (a leaf, as in the 8-point tie, or in the middle), requires
the total to be the difference of two versions, and evaluates exactly.
- Check at 8 points: the same program finds the tie 224 times (pure part 3 = 1 + 2; `d3_idle.out`). So d(3) = 1 is
  reproduced by a method that never saw d-0's circuit.
- 16 points, C'' = Yates (`d4_idle_yates.out`, 223 s): 4,698,161 groupings with 8 independent reaches; in 900,301 of
  them at most one wire lacks a tree made of wires that are free given the total; **in none of them is there an idle
  version and a tree with every injected wire free given the total and the total a difference of two versions.** Not
  one candidate reached the exact count. So with Yates above, 12 M2 gates and one idle version, delivering the lower
  total costs the mixed part at least 2: **d(4) >= 2 in this class**, against d(3) = 1.
- 16 points, C'' = derivation 6501, the circuit with a cancellation inside (`d4_idle_d6501.out`, 196 s): 4,233,567
  groupings, 403,095 with at most one wire lacking a tree, and again not one candidate. d(4) >= 2 there too.

**What this does and does not decide.** A 31-gate circuit has, in each of its four cuts, extra + pure <= 11. Excluded
here for the top cut when C'' is Yates: extra = 0 with any deliveries; one idle version with the total delivered.
Not excluded: the other minimum circuits as C'' (6 of 6,960 derivations run for class A, 2 for class B); one idle version with a PAIR of
deliveries worth 4 (159 pairs qualify by section 1); a ninth injection that is used by a gate; a 13th M2 gate, where
the version lemma fails; extra = 2 with one of the three pairs worth 5. 16 points stays open.

## 5. The growth law this gives: a ceiling in one class [derived; no circuit]

In the class "every cut has exactly f(n) M2 gates and no idle injection": by the cut inequality of section 2,
gates >= 2 f(n) + 2 x (number of buses), with the sum of r_b equal to n and r_b <= rho(n), the longest bus without an
idle injection. The best case is n / rho buses of full length, so

    f(2n) >= 2 f(n) + 2 n / rho(n),      that is      f(N) / N  >=  sum over the levels k of 1 / rho(2^(k-1)).

| longest bus rho | the least this class could cost |
|---|---|
| 2 | (1/2) N log2 N: Yates (no bus can pay) |
| 3 for ever | (1/3) N log2 N |
| 4 for ever | (1/4) N log2 N |
| log2 n + 1 (measured at 4 and 8 points) | N ln(log2 N) |
| about 2 (log2 N)^e / (1 - e) | (N/2) (log2 N)^(1 - e): buses of 3 to 5 for e = 0.1 up to N = 2^1000 |
| reciprocals with a finite sum, e.g. (log2 n)^1.1 | linear |

At the sizes run: f(8) >= 2 x 4 + 8/3, so 11, and f(16) >= 2 x 12 + 16/4 = 28, against the true 12 and the open 31 or 32.

Reading. (a) This is what "deliveries whose costs overlap at a rate that grows with the node" means in numbers: nearly
every one of the n injections of a cut must sit on a bus, the buses must get longer with n, and each must save its full
r - 2. (b) The capacity is not the obstacle: minimum circuits already have rho = log2 n + 1, enough on paper for
N log log N and far more than the user's bar needs. (c) What is missing is the first unit: **the realised net saving
of a bus is 0 at 8 points and 0 at 16 points in everything searched**, against ceilings of 1 and 2. (d) Idle injections
and extra M2 gates are outside the class; each costs one gate and buys one free form in the offsets.
Worth of the second delivery as a function of the first and of k, as the brief asks: in the mixed part, 0 extra cost
if it reads the same bus and the full cost of a new bus (3 or more non-idle injections on one wire) if it does not; in
the lower half, at most (ceiling r - 2) minus what the first already took, and r <= log2 n + 1 = k on the wires that
exist. A second delivery never raises a bus's ceiling; a second BUS does, and there can be about n / k of them.

## 6. Went around, and the better question

- The pair census said "no synergy to speak of in the lower half". Yes, and: then the sharing has to be in the mixed
  part; asking what a cancelling gate is there gave versions and the bus.
- The bus said "sharing is free". Yes, and: then count what a bus can save at all: r - 2, and with n injections the
  offsets are forced; that turned the search for 31 gates from guessed skeletons into a finite enumeration.
- The enumeration said "tie, never 11" at extra = 0. Yes, and: the 8-point tie lives at extra = 1, so I added the idle
  version; it reproduces d(3) = 1 and reports d(4) >= 2 for Yates.

**Better question.** A bus hands the lower half a relation: p1 + p2 + p3 + w = 0 among four pure wires, three paid for
as injections and w for one gate. It pays only if the lower half needs all four and has no other three-term relation
among wires it already owns that gives w in one gate. In the ties I looked at, the forced offsets are lower outputs
and mirror images of Yates's wires, and such a relation exists [guess that it always does at extra = 0]. **Which minimum circuits C'' and which groupings force
offsets whose bus relation is a genuinely four-term one for the lower half?** That is a question about the matrix
(T transposed)^-1 Z, not about a search.

## 7. Mutations (not judged)

1. **All 6,960 derivations for class A, and class B with every C''.** `deco.py` is Python and takes 3 minutes per
   Yates-like circuit; in C the whole list is a night on the rented machine. Output: the least pure count per C''.
2. **The general ninth injection**: 9 classes with one dependency among non-zero reaches; the offsets then have one
   free form v (255 choices). Same program with one more loop. This is the rest of extra = 1 with 12 M2 gates.
3. **The 13th M2 gate**: two M2 gates with the same upper part; the version trees become graphs with a cycle, and a
   cancelling gate may read around it. The version lemma has to be redone; I expect "one free form per extra gate".
4. **Pairs worth 4 or 5 on two buses**, with the census as the filter: 159 pairs. The total with a face output needs
   one bus through both if both are read from one bus (they are nested sums): a bus of 6, and no wire of rank 5 exists
   at 8 points, so at least 2 of its injections are idle: 12 + 10 + 9 = 31 exactly. That one design is a small exact
   search. Read from two buses, the pair needs two wires with 3 slots each, which Yates has.
5. **Prove rank <= log2 n + 1** for the slots of any wire of a minimum circuit, or find the first circuit near the
   minimum where one wire has many independent consumers. By section 5 this number is the whole growth law.
6. **The same decoration over other fields**: versions become (a, c b) with a scalar c; the identity and the forcing
   are unchanged [derived]. Over the rationals the answer must change at astronomical size (g-4's three transforms),
   so the bus relation must become four-term there. Where?
7. **32 points with Yates on 16 as C''**: ceiling 3 per bus on x''_0 (rank 5). Is the realised saving still 0? The
   enumeration is too large as written; the delivered form can be fixed to the 16-point total first.

## 8. Criticism, last

- Sections 2 and 5 are by hand, in an hour, unreviewed. What supports section 2 is that the program built on it
  reproduces three known answers at 8 points (no 11; the tie; d(3) = 1) and that the cut inequality holds on all
  20,790 cuts of section 3. That is one size.
- In section 3 the sorting of gates depends on the derivation (which two wires make each wire); I took every acyclic
  one, so one circuit appears several times.
- The version lemma needs exactly f(n) M2 gates, and f(8) = 12 is itself "exhaustive modulo 2". One more M2 gate is
  outside everything here.
- Class A and class B are for one cut and for C'' = Yates plus five samples that I picked by position in ab-4's list,
  not at random. A 31-gate circuit could use any of the 6,960 derivations there. "Never 11" is a statement about
  1.6 million structures, not about 16 points.
- The pure-part count ignores the order of events (an injected wire computed from a delivered form that depends on it
  would be circular). That can only make my counts too low, so the NO results stand and a YES would have needed a replay.
- The census filter rests on the pair census for sets of one or two deliveries; sets of three or more were sent to the
  exact search unfiltered.
- "Derivation 3001 is Yates with the bits permuted" is a guess from an identical table.
- The ceiling of section 5 is a ceiling: nothing shows a bus ever saves anything. I first wrote its table with a
  factor 2 too many and corrected it; nobody has checked the corrected one.
- The idle injection is modelled as one extra version of one wire. An injection whose reach is non-zero but dependent
  is a different thing and is mutation 2.
- Everything is modulo 2. Over the rationals subset sums do fall below Yates at astronomical size [read: g-4], so no
  argument here can be a field-free proof.
- Nothing here changes the order, or any constant.

## Files

`waves/wave-09/ad-2-twodeliveries/`:
- `free8.c`, `free8`: exact least gates for Z at 4 or 8 points with free forms and extra targets (modes single, pairs,
  list). `single8.txt`: the 247 single forms. `pA1.txt` ... `pC2.txt`: the 30,381 pairs (form a, form b, least gates;
  forms as bit masks, bit i = x_i). `pairs_analyse.py`: the tables of section 1. `triples_top.out`.
- `deco.py`: the decorated-cut search (usage `deco.py n source [limit]`; MODE=count, MODE=d4; START skips derivations).
  `deco4_extra0.out` (8 points, class A), `d3_idle.out` (8 points, class B: the tie), `deco8_yates1.out`,
  `deco8_d3001.out`, `deco8_d5001.out`, `deco8_d6501.out`, `deco8_d1501.out`, `deco8_d4201.out` (16 points, class A),
  `d4_idle_yates.out`, `d4_idle_d6501.out` (16 points, class B). The `.err` files hold the progress lines and the
  job runner's last line. Copies of `deco8_d5001.*` and `deco8_d6501.*` also on the rented machine under
  `(the Linux machine's working folder)/ad-2-twodeliveries/`.
  In MODE=d4 the output line "structures with n independent classes and a wire with >= 3 classes" counts ALL structures
  with n independent classes (the label is the other mode's).
- `ranks.py`, `ranks.out`: bus capacity of every minimum circuit at 8 points. `cutineq.py`, `cutineq.out`: the cut
  inequality on all of them. `z8_sets.txt`: ab-4's list, copied.
