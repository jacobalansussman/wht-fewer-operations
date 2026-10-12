# ad-7 modulo 4: the 15-gate saving modulo 2 dies at 4, exactly and in every wiring; why; and what the second binary digit is made of

> Editor's note (11 October 2026): the ninth note records that this report's guess on repeated wires is false ([af-2](af-2.md)). See line 10 (iv), "Corrections by the critics", in [the ninth note](NOTE.md).

11 October 2026, wave 9, agent "ad-7-modulo4", 60-minute box (about 06:25 to 07:00 EDT). Private. One agent; nothing reviewed,
nothing in Lean, nothing published. Marks: [ran] = computed in this box, exact (whole numbers, or whole numbers modulo 2, 4, 8, 16);
[derived] = argued by hand in this box, checked by nobody; [read] = from a file I opened; [guess].
Gate count everywhere: **(G)**, a gate is any a*u + b*v, scalings free. Count (O), OpenAI's, is not used.
Folder F = `waves/wave-09/ad-7-modulo4/`.

**No circuit below a known count, no growth law below N log N, nothing of the 1e-1 kind. Nothing here changes the order.**
A circuit modulo 4 is not a circuit; this was a probe, and the probe has an answer.

Words. N = 2^k points; an *address* is k bits. *Neighbour sums* A: every address gets the sum of the inputs at its k neighbours.
*The block* B: the 8 x 8 half of A at 16 points, from even-weight inputs to odd-weight outputs (rows in `rows_B4.txt`).
Two outputs are *antipodal* if their addresses differ in all four bits; their rows add up to the all-ones row.
*Modulo 2^j*: whole numbers with remainders after division by 2^j; an *odd* number has an inverse there, an even one has not.
*Primitive* vector: whole numbers not all even. *Halving*: a gate (a*u + b*v)/2^e that is only possible because a*u + b*v is
all even. *Invariant factors* of a whole-number matrix: the diagonal d1 | d2 | ... it can be brought to by whole-number row and
column operations (the Smith form); r_j = how many of them are not divisible by 2^j = how many generators the rows need
modulo 2^j. *2-adic numbers*: what remains when one works modulo 2^j for every j at once.

## 0. In ten lines

1. [ran, exhaustive] **The block costs 15 gates modulo 2 and 16 modulo 4, modulo 8, and modulo every higher power of 2.**
   There are exactly 478 sets of helper wires that give 15 gates modulo 2 (up to the block's symmetries); **none of the 478
   lifts to modulo 4**, in any order and with any coefficients. The best any of them does modulo 4 is 6 of the 8 outputs.
2. [derived] So there is no 15-gate circuit over the 2-adic whole numbers, and none over the rationals **unless it contains a
   halving** (section 2 says exactly what that means). 16 is the adding-only count [read: ab-0], so in this class it is exact.
3. [ran] Why it dies at the first step: the block's invariant factors are 1, 1, 1, 1, 2 (then zeros). Modulo 2 the rows need 4
   generators; modulo 4 they already need all 5 that the rationals need. The saving is exactly one binary digit deep.
   Same at 64 points (16 generators modulo 2, all 22 modulo 4) and at 256 points (64, then 92 of 93).
4. [ran] The gates that die, in ab-0's circuit: g21 and g22, the two outputs 0 1 1 1 0 0 0 1 and 1 0 0 0 1 1 1 0 (an antipodal
   pair). They use a relation among four rows that is true modulo 2 and false modulo 4; the third output made the same way
   (g20) survives because its relation is an antipodal one, true over the whole numbers.
5. [ran] **Line sums of the finite plane** (20 x 16, 72 x 64, 272 x 256): invariant factors 1, 2, 4, ... with multiplicities
   9, 2, 5 / 27, 9, 9, 19 / 81, 36, 38, 36, 65. The rank N^0.79 modulo 2 is the first of k/2 + 1 digits; first digit
   3^(k/2), last digit 3^(k/2) - 2^(k/2) at all three sizes; the middle digits carry almost everything.
6. [ran + derived] **Every modulo-2 saving of the night is the constant term of one binomial expansion** (section 4):
   transform H = sum over sets S of bits of (-2)^|S| (rank-one piece); neighbour sums A^2 = k + 2 A_2; subset sums relabelled,
   cube = sum over S of 2^|S| (piece). Digit j always has C(k, j) pieces. So the answer to the brief's question is: **the
   first digit of something, and the something is the textbook ladder**, k digits long.
7. [ran] Read as 2-adic objects, **all of the night's best exact circuits for the transform (7, 19, 20, 52, 128, 304 gates)
   contain no halving and no coefficient other than +-1 and +-2.** The family of e2-0 has exactly (N/2) log2 N gates of the
   kind u +- 2v and N (k + 1)/4 of the kind u +- v at every size from 4 to 64 points; the 19-gate circuit has 12 and 7.
   Modulo 2 each of them collapses to N - 1 gates, the least possible.
8. Growth law: none. What the probe says about growth is negative for the saving and specific about where to look:
   the two kinds of gate that the modulo-2^j ladder cannot see or has never met (halvings; corrections 4v, 8v, ...) are
   exactly the ones no circuit of the night uses.
9. The wall, in one sentence: a saving that lives in the modulo-2 rank lasts as many digits as the invariant factors allow,
   and for neighbour sums that is one.
10. Not done: free wiring modulo 4 for more than 15 gates (not needed: 16 exists); a circuit modulo 2 for the line sums and its
    lift (no small circuit to start from; the profile in line 5 is what I have); ab-7's row (I did not open ab-7).

## 1. What "a circuit modulo 4" means here, and how a scaling by 2 is treated

A circuit modulo 2^j: wires are vectors of whole numbers modulo 2^j; a gate is a*u + b*v with a, b any numbers modulo 2^j
(even ones included); a wire is known up to an ODD factor (odd factors are invertible, so they are the free scalings); an output
counts as computed when a wire is an odd multiple of its row. A wire 2*u is not a gate: it is absorbed in the coefficient of
the gate that uses it. **An output delivered as 2 x (row) does not count**: modulo 4 it knows the row only modulo 2, so allowing
it would turn the question back into the modulo-2 question. That is the one place where "scalings are free" must be restricted.

Three facts [derived]:
- **Tower.** A circuit modulo 2^(j+1) is one modulo 2^j, so the least count C_j can only grow with j, and it is at most the
  count of any whole-number circuit. If ONE wiring works modulo 2^j for every j, it works over the 2-adic whole numbers
  (finitely many choices at each level, each level restricts to the one below), hence with algebraic coefficients [read:
  aa-cross].
- **Reduction lemma.** Let c be the least count modulo 2. In a circuit with exactly c gates modulo 2^j, every coefficient is
  odd: a gate with an even coefficient is a copy (or zero) modulo 2 and could be dropped there, leaving c - 1 gates modulo 2.
  So at c gates the modulo-2^j question is: list the minimum circuits modulo 2, and for each try to choose odd coefficients.
  With wires known up to odd factors, each gate is u + s*v, s odd: 2 choices modulo 4, 4 modulo 8.
- **What the ladder does not see.** Take any rational circuit and scale every wire to a primitive whole-number vector. Then
  each gate is one of three kinds: (i) both coefficients odd (a real gate modulo 2); (ii) one odd, one even, u + 2^e v
  (a copy modulo 2, a correction in digit e + 1); (iii) a *halving*, (a*u + b*v)/2^e with a, b odd, possible only when u and
  v are the same vector modulo 2. The ladder modulo 2, 4, 8, ... is exactly the class without kind (iii).

## 2. The first experiment: the 16-point block  [ran]

Tools (all in F). `enum2.c` = ab-0's `mincirc_top.c` changed to print EVERY solution instead of stopping at the first.
`lift.c` = for a set of helper wires modulo 2, search every order and every lift modulo M (M = 2, 4, 8, 16; outputs must be
the rows up to odd factors; a lifted helper tried first at one node is not tried again below, which loses nothing because a
wire that can be made now can be made first).
Controls. (a) 14 gates modulo 2: no solution in either class (`enum_m6_d2.out`, `enum_m6_d4.out`), as w-cross and ab-0 found.
(b) `lift` with M = 2 lifts all 478 sets (it must). (c) The adding-only 16-gate pairing circuit (8 pair gates, `control16.txt`)
lifts at M = 2, 4, 8, 16 (it must: it is a whole-number circuit). (d) ab-0's own circuit is among the 478 (set 3 5 13 20 40
102 192) and stops at 6 outputs, the two missing being the ones ab-0's hand argument names.
The symmetry reduction is ab-0's: every circuit starts with a gate on two inputs; the block's symmetries (shifts by even
addresses, permutations of the four bits) are permutations of rows and columns of the whole-number matrix, so they respect
lifting; the 28 pairs of inputs fall in two classes (distance 2 and distance 4) [derived: 24 + 4 pairs, one orbit each].

| | modulo 2 | modulo 4 | modulo 8 |
|---|---|---|---|
| 14 gates | none (0 records in both classes) | none (by the tower) | none (by the tower) |
| 15 gates | **478 sets of 7 helpers** (428 with a first gate at distance 2, 60 at distance 4, 10 in both; 195,456 records with repeats) | **0 of 478 lift** | 0 of 478 |
| most outputs any lift of a set reaches | 8 (all 478) | 6 (414 sets), 5 (64 sets) | 6 (414), 5 (64) |
| 16 gates | yes | yes (adding-only) | yes |

Files: `enum_m7_d2.out`, `enum_m7_d4.out` (396 and 359 seconds), `lift4_d2.out`, `lift4_d4.out`, `lift4_all.out`, `lift2_*.out`.
With the reduction lemma: **least count 15, 16, 16, 16, ... modulo 2, 4, 8, 16, ...** The answer for modulo 8 and beyond needs
no run (the tower), and the run modulo 8 agrees.

**Consequence [derived from the above].** No circuit with 15 gates exists in which every wire, scaled to a primitive
whole-number vector, is an odd-denominator combination of two earlier ones. In particular none with whole-number coefficients
and outputs equal to odd multiples of the rows. A rational 15-gate circuit, if there is one, contains a halving. This is a
statement about the rationals that the searches modulo 3 and 5 could not give (ab-0: none with 14 modulo 3, none with 13
modulo 5, 15 modulo 3 not run), and it leaves 15 open only inside the halving class.

**Which gate dies, and why.** In ab-0's circuit five outputs are made by adding only, then g19 = (0 0 1 0 1 0 1 1) +
(0 1 0 0 1 1 0 1), then three outputs g19 + (an earlier output). Modulo 4, with g19 taken as the difference of the two
(0 1 3 0 0 1 3 0 up to sign), the first of the three survives: 1 0 1 1 0 0 1 0 = g19 + 1 1 0 1 0 1 0 0, because these four
rows are two antipodal pairs and "pair + pair = all-ones + all-ones" holds over the whole numbers. The other two (g21, g22)
use four rows that are not two antipodal pairs; their sum is 0 2 2 2 2 2 2 4, zero modulo 2 and not zero modulo 4 with any
signs (ab-0's two-line argument, now also the outcome of the search for every one of the 478 sets).
The same thing in one number [ran, `profile.py`, `profile1.out`, `profile2.out`]:

| block of neighbour sums | size | rational rank | invariant factors | generators needed modulo 2, 4, 8 |
|---|---|---|---|---|
| 16 points | 8 x 8 | 5 | 1 (x4), 2 (x1) | 4, 5 |
| 64 points | 32 x 32 | 22 | 1 (x16), 2 (x5), 6 (x1) | 16, 22 |
| 256 points | 128 x 128 | 93 | 1 (x64), 2 (x21), 6 (x7), 12 (x1) | 64, 92, 93 |

The modulo-2 rank is N/4 per block at all three sizes; one digit later the full rational rank is back (all but one direction
at 256 points). **For neighbour sums the saving is an accident of the number 2 in the strict sense: it is one digit deep at
every size tried.** The identity behind it is A^2 = k + 2 A_2 (A_2 = sums over the addresses at distance 2) [read: ab-0;
ran: `ident.py`]: modulo 2 it says A^2 = 0 for even k; the second digit IS A_2, which costs as much as A.

## 3. "Yes, and", twice

**First detour: if unit coefficients cannot lift it, what can? Halvings.** The reduction lemma covers gates of kinds (i) and
(ii) of section 1. A halving takes two wires that agree modulo 2 and returns half their difference, a vector that modulo 2 is
new. Counting modulo 2, a halving costs one wasted gate (the second wire with the same residue) and buys one free point. So a
15-gate rational circuit for the block would look modulo 2 like: at most 13 real gates, one copy, one free point. I did not
search this class (it needs wires modulo 8 before the halving and modulo 4 after; no tool in the box). What I did instead was
ask whether any circuit of the night uses the hatch [ran, `census.py`, `census.out`]:

| circuit | gates | wires not primitive | halvings | gates u +- v | gates u +- 2v | gates left modulo 2 | modulo 4 |
|---|---|---|---|---|---|---|---|
| e2-0, 4 points | 7 | 0 | 0 | 3 | 4 | 3 | 7 |
| e2-0, 8 points | 20 | 0 | 0 | 8 | 12 | 7 | 20 |
| g-1, 8 points | 19 | 0 | 0 | 7 | 12 | 7 | 19 |
| e2-0, 16 points | 52 | 0 | 0 | 20 | 32 | 15 | 52 |
| e2-0, 32 points | 128 | 0 | 0 | 48 | 80 | 31 | 128 |
| e2-0, 64 points | 304 | 0 | 0 | 112 | 192 | 63 | 304 |

("Gates left modulo 2^j": reduce the exact circuit modulo 2^j, drop a gate whose value is an odd multiple of an earlier wire,
then drop what no output uses.) Regularities, all [ran]:
- no halving, no non-primitive wire, no coefficient 4 or larger, anywhere;
- gates u +- 2v: exactly (N/2) log2 N = 4, 12, 32, 80, 192, in the 19-gate circuit too; gates u +- v: N (k + 1)/4 in the
  family, N - 1 in the 19-gate circuit;
- modulo 2 every one collapses to N - 1 gates, which is the least possible for the all-ones matrix; modulo 4 nothing
  collapses (the wires have entries 0, +1, -1, which modulo 4 are still distinct).
WAVE7-NOTE reports "all 213 samples at 19 gates have 7 merges bringing 0 and 12 gates bringing 1" [read]. In this reading:
7 = N - 1 is the cost of the transform modulo 2 and is forced; 12 = (N/2) log2 N is the number of second-digit corrections.
[derived] In a circuit without halvings the first number is at least N - 1, and the number of gates whose value modulo 2
repeats an earlier wire is at least N - 1 (N outputs with one residue). The kind of gate is not the right count (the textbook
writes its repeats as u - v after u + v and has no gate u +- 2v at all); the count that does not depend on the writing is
**repeats = gates minus distinct residues modulo 2**: 4, 12 (19 gates), 13 (20 gates), 37, 97, 241 in the table, against
(N/2) log2 N = 4, 12, 12, 32, 80, 192; the textbook has N log2 N - N + 1. Whether repeats must number (N/2) log2 N when
coefficients stay +-1, +-2 looks like Morgenstern's bounded-coefficient theorem in other words [guess; not proved here].
What this detour gives: the three ways a coefficient can be "unbounded" are different things 2-adically: 2^e (a correction
that skips digits), 2^(-e) (a halving), and a large odd number (invisible at the prime 2). Every circuit of the night uses
none of the three. Morgenstern says a circuit below (N/2) log2 N must use at least one.

**Second detour: is the tower modulo 2, 4, 8 the only road between 2 and the rationals?** [derived] With i available,
2 = -i (1 + i)^2, so "modulo (1 + i)" gives half-digits. The transform with entries (-i)^(distance) is the product over the
bits b of (1 - i X_b), X_b = the swap along bit b, and 1 - i X_b = (1 + X_b) - (1 + i) X_b. Expanding: digit j in powers of
(1 + i) is the sum, over sets S of j bits, of (swap along S) x (sum over the subcube spanned by the other bits): coset sums
of growing codimension, C(k, j) of them. It is the same ladder as below with the same count; the half-digits are empty.
Odd primes: the transform's determinant is a power of 2, so modulo 3^j, 5^j, ... nothing collapses and there is no ladder.
So the prime 2 is the only place where the transform has digits at all.

## 4. One expansion behind all the modulo-2 savings  [ran: `ident.py`, k = 2 to 5, whole numbers; the reading is mine]

| object | identity over the whole numbers | modulo 2 | digit j |
|---|---|---|---|
| transform | H = sum over sets S of bits of (-2)^|S| (E on the bits of S, all-ones on the others), E = [[0,0],[0,1]] | all-ones matrix, rank 1, N - 1 gates | C(k, j) rank-one pieces; x-1's level j |
| subset sums, rows relabelled (M = [[1,1],[1,0]] on each bit) | (M tensor k)^3 = sum over S of 2^|S| (M on the bits of S, identity elsewhere), from M^3 = 1 + 2M | the identity: "order 3" | C(k, j) pieces; second digit = sum over the bits of one-bit M's |
| neighbour sums | A^2 = k + 2 A_2, and A A_j = (j + 1) A_(j+1) + (k - j + 1) A_(j-1) | A^2 = 0 for even k | A_j, the sums at distance j: a ladder with a division by j + 1 at each rung |
| line sums of the plane | (profile only) invariant factors 2^j with multiplicities 9, 2, 5 / 27, 9, 9, 19 / 81, 36, 38, 36, 65 at 16, 64, 256 points | rank 3^(k/2) = N^0.79 | k/2 + 1 digits; first 3^(k/2), last 3^(k/2) - 2^(k/2) |

Transform at 16 points: invariant factors 1, 2 (x4), 4 (x6), 8 (x4), 16 [ran], the binomial row, as H = Z D Z^T says.
**So the modulo-2 saving is never an accident and never a promise: it is the constant term of (1 + 2t) tensor k, and the
expansion has k + 1 terms.** By the term-by-term route each digit of the transform costs about 2N and the total is exactly
N log2 N [read: x-1]. The neighbour-sum ladder is the same object seen from below: the transform with entries
(-i)^(distance) is sum over j of (-i)^j A_j, so the rung "A_2 = (A^2 - k)/2" that kills the 15-gate circuit is the first
halving on the way from neighbour sums to the transform [derived].

A relation that survives more than one digit, for contrast [derived, not run]: in the plane of order q = sqrt N the q + 1
lines through a point p add up to (all-ones) + q x (the point p), and the q lines of a parallel class add up to all-ones. So
"the lines through a point = a parallel class" holds modulo sqrt N, k/2 digits deep, and fails at the next digit by a single
point [ran at 16 points, `linerel.py`]. At 16 points this is part of why the rows need only 11 generators modulo 4 and all 16
modulo 8. I see no gate in it: it has q + 1 terms where a line costs q - 1 gates. The shortest relations modulo 2 among the 20
lines [ran]: none with 4 lines or fewer; exactly 48 with 5 lines, each of them five lines of five different directions with no
three through a point (48 is the number of such figures [derived]); over the whole numbers their sum is 2 x (the ten meeting
points), so these die at 4. A five-term relation makes a line in 4 gates where it costs 3 directly. **Low rank modulo 2 is
not yet a cheap circuit modulo 2**: at 16 points I know no circuit for the line sums below the adding-only 60 even there.

## 5. Growth law

None below N log N. The numbers the brief asked for:
- **How many digits does a saving survive?** Neighbour sums: one (16, 64, 256 points). Line sums: the rank deficit lasts
  k/2 digits, but thins fast: generators needed modulo 2, 4, 8, 16, 32 at 256 points are 81, 117, 155, 191, 256. Transform:
  all k, with generators 1, 1 + k, 1 + k + C(k, 2), ...
- **What does each digit cost?** Block at 16 points: the second digit costs 1 gate (15 to 16) and restores the whole
  count. Transform: by x-1's route about 2N per digit, N - 1 for the first [read]; upper bounds on the least count of H
  modulo 2, 4, 8 from x-1's route and the exact circuits together: 7, 18, 19 at 8 points; 15, 41, 52 at 16; 31, 88, 128 at
  32; 63, 183, 282, then 304 exact, at 64.
- **Is the cost per digit bounded as N grows?** Not by any route known: it is about 2N for each of the lower k/2 digits,
  although digit j has only C(k, j) rank-one pieces. That gap (rank C(k, j), cost 2N) is x-1's open question about the
  lightest outputs, not a new one; this probe adds only that the same gap is there for line sums (first and last digit of
  rank N^0.79, cost unknown) and that for neighbour sums there is no gap to exploit (the second digit has the full rank).

## 6. What I would try next (mutations)

1. **halving-or-nothing** (small, decisive for the hatch). Already known [read: ab-0]: at 4 points the exhaustive counts
   modulo 3, 5, 7, 11, where 1/2 exists, equal the adding-only counts, so there a halving buys nothing. Open from 8 points. Exhaustive at 4 and 8 points over the whole numbers modulo 8 with
   ONE halving gate allowed (wires modulo 8 before it, modulo 4 after): does a halving ever save a gate against the
   halving-free minimum, for the transform (7, 19) or for the 4-point pieces A + 1, A + 2 (6 gates modulo 3, 5, 7, 11 [read:
   ab-0])? If never at these sizes, kind (iii) joins the list of things that tie.
2. **lift x-1's modulo-4 circuits.** x-1 has circuits congruent to H modulo 4 with 3N - k - 3 gates (18, 41 at 8, 16
   points; the best exact are 19, 52). Apply this box's test to them: fix the wiring, ask for coefficients modulo 8, 16, ...
   The first digit at which each dies, and the least number of added gates per digit, is the cost of a digit measured from
   below instead of by a construction. `lift.c` does this for unit coefficients; even coefficients need the general solver.
3. **deep corrections.** Search (annealer or exhaustive at 8 points) with gates u + 4v and u + 8v allowed and u +- 2v
   forbidden or taxed. No circuit of the night has one. Morgenstern forces something of this kind below (N/2) log2 N.
4. **the plane's profile.** Prove or break "first digit 3^(k/2), last digit 3^(k/2) - 2^(k/2)" at 1024 points
   (`profile.py L...` needs a faster Smith form), and price the first digit alone: least gates for the line sums modulo 2
   at 16 points (20 outputs of rank 9; adding-only 60). That is brief 2's question with the target count N + N^0.79.
5. **count the repeats.** In a halving-free circuit for H with coefficients +-1, +-2, is the number of gates whose value
   modulo 2 repeats an earlier wire at least (N/2) log2 N? True in all six circuits above and in the textbook, with
   equality at 4 points and in the 19-gate circuit. If it is a theorem it is a floor N - 1 + (N/2) log2 N for that class
   (7 and 19 at 4 and 8 points, where it is attained; 47 at 16, where the best is 52), and the 52 would have 5 gates to lose.

## 7. Criticism, last

- The headline is a negative result at one size about a count that was never a rational circuit. Its use is the lemma and
  the consequence "15 needs a halving", not the number 16.
- "478 sets" rests on ab-0's symmetry reduction (I re-derived the orbit count by hand, did not re-run it) and on d-0's
  search engine as modified by ab-0 and by me; controls (a) to (d) of section 2 are what I have. The positive control for
  M = 4 is a 16-gate circuit, not a 15-gate one (there is none).
- The reduction lemma needs "none with 14 modulo 2", which is exhaustive only through the same engine.
- The halving class was described, not searched. The census shows that nobody uses it, which is not evidence that it is
  useless.
- Section 4 is a reading: three identities that are easy and one profile. ab-7's row was not examined at all.
- The line-sum formula (3^(k/2) and 3^(k/2) - 2^(k/2)) is three data points. [guess]
- "Morgenstern in other words" (section 3, mutation 5) is a guess; I recalled the theorem and did not open a source.
- Nothing here changes the order, or any constant.

Files in F: `profile.py`, `profile1.out`, `profile2.out`, `profile3.out` (invariant factors); `enum2.c`, `enum_m6_d2.out`,
`enum_m6_d4.out`, `enum_m7_d2.out`, `enum_m7_d4.out` (all minimum circuits modulo 2); `lift.c`, `lift2_d2.out`, `lift2_d4.out`,
`lift4_d2.out`, `lift4_d4.out`, `lift4_all.out`, `lift8_all.out`, `control16.txt` (lifting); `census.py`, `census.out` (the best circuits as
2-adic objects); `ident.py`, `ident.out` (the three identities); `linerel.py`, `linerel.out` (shortest relations among the lines).
