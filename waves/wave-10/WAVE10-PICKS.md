# WAVE10-PICKS: ten briefs (the nine experiments of ae-cross section 6, and irrational constants)

> Editor's note (11 October 2026): these briefs were written before the critics of the ninth wave had reported, as the ninth note says. Where a brief says "the transform modulo 2^(d+1) in about 2N + o(N)", read 3N + o(N) ([af-0](../wave-09/af-0.md), [ai-0](ai-0.md)).

11 October 2026, curator ah-pick, 15-minute box. Private research: publish nothing, no git, no Lean. Not ranked by odds.
Read for this: ae-cross.md in full; ad-6.md in full; ad-0.md sections 0, 1, 5 to 8; ad-2.md sections 0, 6, 7 and its
file list; ad-7.md sections 0, 1, 3, 6; ab-2.md lines 24 to 40 and 109 to 125; WAVE7-NOTE.md sections 3 and 4; z-0.md
section 4 item 1; g-1.md line 61 and `g-1-tightwires/min4.out`; the header comments of `d-0-zeta/mincirc.c` and
`ab-2-tallpool/tallmin.c`. Not read: WAVE8-NOTE beyond its headings, ad-1, ad-3, ad-4, ad-5, any skeptic of wave 9
(none had landed). I ran nothing.
Marks: [read] = in a file I opened; [ran] = run by the named agent, not by me; [derived] = by hand in this box, checked
by nobody; [recalled] = from memory; [guess].
All paths are under `waves/` unless they start with R
(R = `(not in this repository) wht-power-saving-r4-candidate`, read only).

**The bar.** Only a saving of 1e-1 or more (O(n (log n)^0.9) or better) or linear size counts. Constants at one size
are of no interest; every brief ends with a growth law in N or says it has none.
**Brief 4 (sector-and-port) bears on the bar of 1e-1 directly**: it tests the one integer (three shears per exchange)
that keeps the published mechanism's best block at 11.1 % against the 11.5 % that 1e-1 asks.
**One thing a developer of brief 10 must know before starting**: g-1 already claims that 7 gates is the least at 4
points over EVERY field of characteristic 0 (`g-1-tightwires/min4.out`, argument in g-1.md line 61, unreviewed). If that
argument is right, the 4-point half of brief 10 is closed and the hour belongs to 8 points.

Common words. N = 2^k points; an *address* is k bits; *weight* = number of ones. *The transform* H: entries (-1)^(x.y),
x.y = number of common ones. T(N) = least gates for H, relabellings and scalings free. *Textbook*: N log2 N gates.
Gate counts: **(G)** a gate is any a*u + b*v, scalings free; **(O)** OpenAI's, additions and scalar multiplications each
charged. Every brief uses (G) unless it says moves and blocks. *Subset sums* Z: output(T) = sum of the inputs at the
subsets of T; *Yates* = the textbook circuit for Z, (N/2) log2 N gates. *Helper*: a wire that several outputs read.
Night's counts (G): 7, 19, 52, 128, 304 gates at 4, 8, 16, 32, 64 points (files `e2-0-pieces/slp_*.txt`,
`g-1-tightwires/h8_19gates.txt`).
Tools named below: `d-0-zeta/mincirc` (exhaustive least-gate search modulo a prime p; usage `mincirc p n m [rowsfile]`,
n = number of inputs, must be even, p^n at most about 6e6, m = number of wires that are not outputs; a NO is exhaustive
modulo p only); `ad-7-modulo4/enum2` (the same, printing every solution); `ad-2-twodeliveries/free8` (least gates
modulo 2 at 4 or 8 inputs with some forms given free); `ab-2-tallpool/tallmin.c` (exact, whole numbers: does a wire
with large entries save a gate).

---

## 1. ladder-degree-3

**Idea.** Read in base 2, the transform is a ladder: H = sum over j of (-2)^j E_j, where E_j(y, x) = number of j-subsets
of the common ones of x and y, and binary digit j of an output is a polynomial of degree j in the bits of the output's
address [ran by ae-cross, k = 2 to 6]. The textbook pays about N gates per rung. ad-6 found the one place in nine waves
where a rung costs less in the leading term: every polynomial of degree at most 2 at all N cube points in N + o(N)
gates, against 2N. Ask whether the third rung does the same.
**Words.** *Polynomials of degree at most d at all cube points*: the matrix with one output per address y and one input
per set S of at most d bits, output(y) = sum of the inputs at the sets S contained in y. It is Z with only the inputs
of size at most d kept. c(d) = least gates / N. *Pair*: two partitions P1, P2 of the cube points. *Good for degree d*:
every polynomial of degree at most d is (a function of the P1 class) + (a function of the P2 class). *Classes* = number
of classes of P1 plus of P2; each class is one helper wire, each output one gate, so gates = N + cost of the helpers.
V_d(k) = least classes. *Selector and atoms* (ad-6's family): address = (a, y) with a = t selector bits; the bits of y
are cut into 2^t groups, the atoms; P1 forgets a; P2 keeps a and all of y except the atom numbered a.
**Known [read, unreviewed].** Degree 2: classes about 2N log2(k)/k, gates N (1 + O(log k / k)), built and replayed to
k = 16. Degree 3: the family fails at every size tried; what is missing is one monomial, a_i y_p y_r with p and r in two
different atoms and a_i telling the two atoms apart. Best known: V_3(k) <= N/2 + V_2(k - 1), that is 16, 30, 56, 108,
208 classes at k = 4 to 8, and gates at most (d - 1) N + o(N) for degree d (derived, not built). The girth bound does
not forbid two helpers at degree 3 from k = 8 on.
**Start from.** ad-6.md (sections 1, 4, 6); `ad-6-twohelpers/verify.py` (its function `good` tests any pair exactly),
`circuit2.py`, `law.py`; ae-cross.md section 4; `ae-cross/h1_digits.py`; `d-0-zeta/mincirc`.
**First experiment.** (a) The exact ladder at 16 points: least gates for degree at most d, d = 1 to 4, modulo 2 with
`mincirc` (5, 11, 15, 16 inputs; pad odd counts with one dummy input [derived from the usage line]; modulo 3 only
d <= 2 fits the size limit). Report each step. Brief 8 computes the same table for another purpose: agree on it, do not
both spend the hour there. (b) 64 and 128 points: search two partitions good for degree 3 with fewer than 56 and 108
classes, letting BOTH forgotten sets depend on the point (ad-6's wall COORDINATES is exactly "P1 forgets the same bits
everywhere"). (c) ad-6's open case: four partitions R_00, R_01, R_10, R_11 of the y cube whose joins in pairs are each
good for degree 2.
**Growth law.** If degree 3 costs N + o(N), the recursion cost(d) = N + cost(d)/2^t + cost(d - 1)/2^s gives every fixed
degree in N + o(N) [derived by ae-cross, conditional], and the transform modulo 2^(d+1) in about 2N + o(N). The order of
T moves only if c(d) stays o(d) up to d near k/2, where 96 to 98 % of the coefficients sit [ran by ae-cross]: linear
size is c bounded, the bar is c(k/2) at most a constant times k^0.9. A NO with a proof would be the first lower bound
above N for an explicit tall matrix in count (G).
**Keep asking.** Is any step of the ladder below N; and what does the monomial a_i y_p y_r need that a pair in which
neither side forgets a fixed set of bits could not give?

## 2. halving-or-nothing

**Idea.** Scale every wire of a rational circuit to whole numbers with no common factor. Then each gate is one of three
kinds [read: ad-7 section 1]: (i) both coefficients odd; (ii) u + 2^e v, a copy modulo 2 and a correction in a higher
binary digit; (iii) a *halving*, (a*u + b*v)/2^e with a, b odd, possible only when u and v are the same vector modulo 2.
Every record of the night (7, 19, 20, 52, 128, 304) has no halving at all [ran by ad-7]. The ladder "modulo 2, 4, 8,
..." is exactly the class without halvings, so every wall proved on that ladder is silent about them. A halving is also
the only kind of gate that could use what the transform has beyond its class, H H = N (ae-cross fact F, a guess).
Decide in the smallest cases whether one halving ever saves a gate.
**Words.** *Modulo 2^j*: whole numbers up to multiples of 2^j; a wire is known up to an odd factor; an output delivered
as 2 x (row) does not count. *The block* B: at 16 points, the 8 x 8 half of the neighbour-sum matrix (every address
gets the sum of the inputs at its 4 neighbours) from even-weight inputs to odd-weight outputs; 15 gates modulo 2, 16
modulo 4 and above, and none of the 478 helper sets that give 15 modulo 2 lifts to modulo 4 [ran by ad-7].
**Known.** At 4 points the exhaustive counts modulo 3, 5, 7, 11, where 1/2 is an ordinary number, equal the adding-only
counts [read: ad-7 quoting ab-0], and 7 is claimed least for H over every field of characteristic 0 (g-1). So 4 points
are closed for H; open from 8 points. Counted modulo 2, a halving is one wasted gate (the second wire with the same
residue) and one free point [derived by ad-7].
**Start from.** ad-7.md sections 1 to 3 and 6; `ad-7-modulo4/` (`enum2.c`, `lift.c`, `census.py`, `rows_B4.txt` if
present, else rebuild B); `ad-2-twodeliveries/free8` (least gates modulo 2 at 8 inputs with free forms).
**First experiment.** The block B, which has 8 inputs: a 15-gate rational circuit with one halving looks modulo 2 like
at most 13 real gates, one copy and one free form. For each of the 255 non-zero forms w modulo 2, run `free8` with w
given free and ask for B in 13 gates. For every hit, fix the wiring and solve for coefficients with wires modulo 8
before the halving and modulo 4 after (extend `lift.c`). Then the same design for H at 8 points and 18 gates: the
modulo-2 shadow must be the all-ones matrix in 7 gates plus the wasted gate and the free form; say exactly which class
you covered, a full exhaustive search at 18 gates is probably out of reach in an hour [guess].
**Growth law.** None by itself. What it decides: by Morgenstern's bound [recalled] a program of linear size needs
coefficients that grow, and 2-adically the total depth is (N/2) log2 N units; the records spend exactly one gate
u +- 2v per unit. A halving that saves one gate at 8 or 16 points is the first gate that carries more than its unit;
the law to report is then units of depth per halving as the size doubles. If nothing is found, kind (iii) joins the
list of things that tie, with sizes.
**Keep asking.** Where in a circuit can two different wires agree modulo 2 for free, and what does the lower half do
with their half-difference that it could not do with either?

## 3. the-first-bus-that-pays

**EVERY STATEMENT HERE IS MODULO 2 (two-element field).** A circuit modulo 2 is a candidate until lifted.
**Idea.** Cut subset sums on 2n points along one address bit. ad-2 showed that the upper half of any tight circuit is a
decorated copy of a minimum circuit for n points, and that a wire carried through r versions (a *bus*) lets a second,
third, ... delivery to the lower half cost one gate and no new injection. On paper a bus saves up to r - 2 gates; in
every class searched the realised saving is exactly 0. Find the first bus whose saving is not 0, in the two rooms the
searches did not enter.
**Words.** f(n) = least gates for Z on n points (4 and 12 at 4 and 8 points; Yates gives 32 at 16; the question is 31).
*Cut*: lower inputs x', upper inputs x''; outputs Z x' and Z x' + Z x''. A wire is a pair (lower part, upper part);
*pure* = upper part 0; *mixed* otherwise. *M2 gate*: two mixed operands, mixed result (at least f(n) of them).
*Injection*: a pure wire added to a mixed one (at least n). *Cancelling gate* or *delivery*: two mixed operands whose
upper parts cancel, handing a pure form to the lower half. *extra* = (M2 gates - f(n)) + (injections - n). *Version*:
a mixed wire with the same upper part as a wire of the upper circuit C'' and another lower part. *Bus*: one wire of C''
carried through r versions by r injections. d(k): ad-2's name for what the delivered lower total costs at 2^k points
(1 at 8 points, the tie; at least 2 in the classes searched at 16); its exact definition is in ad-2.md lines 233 to
247, read them, I did not check it.
**Known [ran by ad-2].** Cut inequality in every cut with exactly f(n) M2 gates: gates >= 2 f(n) + sum over upper wires
of min(injections, 2); no violation on 20,790 cuts. Longest bus in every minimum circuit: 3 and 4 at 4 and 8 points.
At 16 points with C'' = Yates and five other minimum circuits, about 1.6 million structures: never 11 pure gates.
Not covered: the remaining C'' among the 6,960 derivations of the 2,802 minimum circuits at 8 points; a 13th M2 gate;
a ninth injection that IS used by a gate.
**Start from.** ad-2.md sections 2 to 7; `ad-2-twodeliveries/deco.py` (usage `deco.py n source [limit]`, MODE=count or
d4, START skips derivations), `ranks.py`, `cutineq.py`, `z8_sets.txt`.
**First experiment.** Port `deco.py` to C (3 minutes per upper circuit in Python) and run all 6,960 upper circuits on
the rented machine, classes A and B. Then add the loop for the general ninth injection (9 classes with one dependency;
the offsets then have one free form, 255 choices). Then redo the version lemma for two M2 gates with the same upper
part (ad-2 expects one free form per extra gate).
**Growth law [derived by ad-2, a ceiling and not a circuit].** If every cut is tight and the longest bus is rho(n),
f(2n) >= 2 f(n) + 2n / rho(n). rho = 3 for ever allows (1/3) N log2 N; rho = log2 n + 1, which the minimum circuits
have, allows N ln(log2 N), far below the bar; linear size needs bus lengths whose reciprocals have a finite sum. All of
this is for Z modulo 2; the transform costs at most two Z and N over the rationals (H = Z D Z^T), and ad-7 saw a
modulo-2 saving die at modulo 4, so a 31 would still have to be lifted.
**Keep asking.** A bus hands the lower half a relation p1 + p2 + p3 + w = 0 among four pure wires. When does the lower
half need all four and yet own no cheaper relation that gives w in one gate?

## 4. sector-and-port  (THIS ONE BEARS ON THE USER'S BAR OF 1e-1; engine's accounting, moves and blocks, not gates)

**Idea.** ad-0 opened the published unit and found that its best block does not lose to the bar at the top: a data
array's climb through one stage leaves out 1 of 9 directions, 11.1 %, and 1e-1 asks 11.5 % of a block that stands for a
third of an array. What keeps it out is one integer. Giving n arrays one free move each needs at least n + 1 shears,
because in the part of the data where the move acts as -1 every shear is a matrix "identity plus rank one" and -1 is
never a product of n of those. Hence 3 stages per free move. With 2 shears per exchange the same ports would give 0.21
[FLOAT, WHAT-IF, ad-0]. The proof uses exactly one fact: every free step takes the same value where the move is +1 and
where it is -1. Find a free step that does not, or extend the count to the steps not yet covered.
**Say it plainly.** This is the only experiment of the ten aimed at 1e-1 inside the published mechanism. Even a yes is
not yet 1e-1: helpers and scratch copies divide the published saving by 3.74 and 4.00 after the exchange has taken its
4.33 [ran by ad-0, FLOATS]. It would remove the first and best-understood of four paybacks.
**Words.** *Array*: one working copy of the data. *Move*: one direction of the transform applied to one whole array.
*Block*: a run of moves on one array with no addition in between; *rank* = its number of moves. m = moves each array
owes; W = number of arrays. *Price law* (the engine's): the saving is 1 - z, z the root of sum over blocks of
(rank/m)^z = W. *Stage*: one of five groups of h directions (m = 5h). *Shear*: target += c x (source moved along one
direction). In phased form the move is D = a + b x shift, a = (1 + i)/2, b = (1 - i)/2, D^2 = the shift. *Sector*: the
part of the data on which D acts as +1, or as -1 (the -1 sector exists from two digit columns on). *Free step*: costs
no move: sums of whole arrays with scalar coefficients, and relabellings. *Address map*: a relabelling of the addresses
inside a block by an invertible bit matrix. *Port*: the directions an exchange leaves out; r = its dimension; ad-0
shows r does not change the count. *Digit column*: one of the f tensor factors the move acts on.
**Known [ran by ad-0].** `shears.py` (exact, Gaussian rationals): the three-shear exchange works at 1, 2, 3 columns;
a two-shear exchange exists on one column and dies from two on. `sector.py` (modulo primes: a candidate-or-absence test
only): with free steps widened to every permutation of a column's 4 addresses times a sign pattern, acting alike on
all columns, the two-shear exchange (solvable exactly when D + D U D = V) has no solution at 2 or 3 columns modulo
10009 and 1000033; nor with the 10,752 affine-map-and-sign steps at 3 bits per column, modulo 10009 only.
**Not tried.** Steps that treat the columns differently (the floor note's hatch (a)); words whose two shears go along
different directions; an address map g that carries the port direction p to another direction q, after which the two
sectors are no longer compared with themselves.
**Start from.** ad-0.md sections 5 and 8; `ad-0-rateperblock/shears.py`, `sector.py` (argument `small` by default; read
the note on the row-order bug in section 7); x-6.md sections 1 and 5; the floor theorem and its hatches,
`(not in this repository) wht38/floor/NOTE.md`; the tiny-unit notes named in the task (every saving
of the small game needs an address map). ae-cross hybrid 2 gives a guide: aim at the dressed target of largest trace.
**First experiment.** Exact small search: n = 2 arrays, two directions p and q, free steps including the address maps
that exchange p and q, at most 2 shears per array: is the matrix -1 reachable in the sector comparison? Do it modulo
two primes first, then exactly in Gaussian rationals for any hit. Second: the same with free steps that differ from
column to column.
**Growth law.** In the engine's law a two-shear exchange turns the stage block's net share from r/(3h) into r/(2h):
with r <= h/3, 16.7 % against a need of 7.4 % (blocks of 2h/3 and h, m = 2h), which is the 0.21 above before helpers
and copies. A NO with a proof extends "n + 1" to address maps and closes the engine's road to 1e-1 at its first
payback.
**Keep asking.** Which legal step of the engine sees the sign of the move, and what does it cost?

## 5. cheapest-generator

**Idea.** ae-cross hybrid 3: within a constant factor and O(N), T(N) is the cost of ONE tall matrix, all outputs of Z
from the inputs of weight at most k/2. Its column space is the space of all polynomials of degree at most k/2 in the
address bits, evaluated at all cube points: the half-rate Reed-Muller code over the rationals. All night the matrix was
priced in the monomial basis. Nobody asked for the cost of the *space*: the cheapest circuit on N/2 free inputs whose N
outputs span it.
**Words.** *Character of weight w*: the function y -> (-1)^(x.y) for an address x of weight w. *The space* S_k (k odd):
the span of the characters of weight at most k/2; dimension N/2; equivalently the vectors orthogonal to every character
of weight above k/2 [derived: characters are orthogonal]. *Generator*: any N x N/2 matrix with column space S_k.
*Monomial encoder*: the generator whose inputs are the polynomial's coefficients. *Change of basis*: the N/2 x N/2
matrix between two generators.
**Known [ran by ae-cross, k = 3 to 6].** For degree at most 1 the generator whose inputs are the values at 0 and at the
k unit points costs N - 2 against N - 1 for the monomials; the floor is N - k - 1. For the half-rate space the floor is
N/2 and nothing below the monomial encoder is known. A cheap generator alone is not a cheap transform: the change of
basis is needed once for each half of the input [derived by ae-cross]. [recalled by ae-cross, no source read] codes
with encoders of linear size exist (Spielman 1996); none is known for this code.
**Start from.** ae-cross.md hybrid 3; `ae-cross/h3_rm.py`, `h3_rm.out`; `d-0-zeta/mincirc` for exact counts once a
generator is fixed; g-4.md for "subset sums = three transforms and four diagonals".
**First experiment.** 8 points (k = 3, degree at most 1, 4 inputs): decide exhaustively the least gates over ALL
generators; the answer lies between 4 and 6. A generator circuit is a circuit on 4 inputs with 8 outputs of rank 4, all
orthogonal to the four characters of weight 2 and 3: search circuits, test the outputs. Then degree at most 1 and 2 at
16 points, then 32 points (16 inputs: not exhaustive; anneal on the circuit with the orthogonality test as the goal).
For the best generator found, price the change of basis to the monomials. Read the coding literature on encoders of
Reed-Muller codes over large fields or characteristic 0 (check dates; knowledge may be older than October 2026).
**Growth law.** g(N) = least gates per point of the space. If g stays bounded and the change of basis costs b(N/2),
T(N) is about 2 b(N/2) + O(N): the order changes only if b is not again a half-size transform. Report both numbers per
size and whether b looks like T(N/2).
**Keep asking.** Which basis of the space of low-degree polynomials is cheapest to evaluate everywhere, and is the price
of leaving the monomials always a transform of half the size?

## 6. three-helpers

**Idea.** aa-cross's ceiling for helpers (degree at most log2 k, hence N log N / log log N at best) is a fact about TWO
helpers per output: outputs are edges of a graph and short cycles are forbidden. With three helpers per output the
outputs are edges of a hypergraph, the forbidden thing becomes "a small set of outputs touching too few classes", and
that is the condition under which a parity-check code with three checks per symbol has large distance; such codes exist
[recalled by ae-cross: Gallager]. So for three helpers no known count forbids o(N) classes at high degree. Nothing is
built. Build the first case.
**Words.** As in brief 1: *polynomials of degree at most d at all cube points*; a *class* of a partition of the cube
points is one helper wire. *h partitions good for degree d*: every polynomial of degree at most d is a sum of h
functions, one of the class of each partition; each output then costs h - 1 gates. *Classes* = total over the h
partitions. *Necessary condition* [derived by ae-cross, five lines, unreviewed]: every set of fewer than 2^(d+1)
outputs touches at least as many classes as it has outputs.
**Known [ran by ae-cross, `h4_three.py`].** Three partitions (forget an outer selector bit; inside each half aa-cross's
pair) carry every monomial of degree at most 3 and none of degree 4 at 32 and 64 points, with 44 and 84 classes, more
than N: correctness only. Where classes are flats chosen by the point, h helpers reach degree h and no more [derived].
**Start from.** ae-cross.md hybrid 4; `ae-cross/h4_three.py`; ad-6.md sections 1, 4, 5; `ad-6-twohelpers/verify.py`.
**First experiment.** At 64 and 128 points: the largest degree carried by three partitions with fewer than N classes
in all, classes NOT required to be flats (subspaces or their shifts). Test goodness by rank in exact fractions at 64
points (the space of sums of three class functions must contain every monomial of degree at most d). Start from random
partitions that satisfy the necessary condition, then anneal on the number of monomials carried. State the condition
as a program and check it on every candidate. The first open case with a number: three helpers, degree 4, classes
below N; or two helpers, degree 3, from k = 8.
**Growth law.** With h helpers and o(N) classes, degree d costs (h - 1) N + o(N). Known constructions give d = h, slope
1 per degree. Any family where the degree grows faster than the number of helpers gives c(d) = o(d) on the ladder of
brief 1, which is what the order needs; a bound of girth type for hypergraphs would be the first ceiling for h >= 3.
**Keep asking.** What is the largest degree per helper, and does it stay 1 when the classes are not flats?

## 7. deep-gates

**Idea.** The transform is (N/2) log2 N units of 2-adic depth deep (its determinant is 2 to that power) and every
record spends exactly one gate u +- 2v per unit [ran by ad-7: 4, 12, 32, 80, 192 such gates]. No record contains a
coefficient 4 or larger. By Morgenstern's bound [recalled] a program below (N/2) log2 N must contain a coefficient that
grows, and a linear one has to account for about (log2 N)/2 units per gate [guess of ae-cross; no per-gate bound is
proved]. Nobody has seen a single gate u +- 4v do work that two gates u +- 2v cannot. Find the smallest specimen, for
any matrix at all, or show that depth moves one unit per gate in everything searchable.
**Words.** *Deep gate*: u + 2^e v with e >= 2, wires scaled to whole numbers without common factor. *Unit of depth*: one
factor 2 in the determinant. *Tall wire* (ab-2): a wire with an entry of size above 1. *Specimen*: a small target
matrix and a circuit with a deep gate that beats, by at least one gate, every circuit whose coefficients are 1 and 2.
**Known [ran by ab-2, exhaustive].** The analogous specimen for a coefficient 2 exists: 4 inputs, rows (1,0,-1,-1),
(0,1,0,-1), (1,-1,1,0), (1,1,0,1), 7 gates with entries 0 and +-1 on every wire, 6 with the helper 2 x1 - x2 - x4.
112 such classes, the saving always exactly one gate; none when every target is a full sign vector, none for a matrix
of zeros and ones: H has signs and no zeros, Z has zeros and no signs.
**Start from.** ad-7.md section 3 (the census table) and section 6 mutation 3; ab-2.md sections 2 to 4;
`ab-2-tallpool/tallmin.c` (usage in its header); `ad-7-modulo4/census.py`; `g-1-tightwires/sa8.py` and
`e2-0-pieces/walk.py` (annealers at 8 points and beyond).
**First experiment.** (a) Change `tallmin.c` so that the reference count is "least gates with coefficients +-1, +-2"
and the challenger may use +-4 and +-8: smallest target set on 4 and 5 inputs where the challenger wins; then restrict
to targets that are orthogonal up to scale with entries of one size. (b) At 8 points, search for H with gates u + 4v
and u + 8v allowed and u +- 2v forbidden, then taxed: what is the least count, and does any circuit at 19 or 20 use a
deep gate?
**Growth law.** If a gate u + 2^e v can carry e units of depth in a circuit for a matrix of the transform's kind, the
count of correction gates could fall from (N/2) log2 N towards (N/2) log2 N / e, and e growing like log N is linear
size; the report must say how e may grow with N in the specimen's family. If only one unit per gate is ever seen, wall
DEPTH gains its first per-gate evidence, with sizes.
**Keep asking.** What would the wire v have to be for u + 4v to be an output or one gate from two outputs?

## 8. the-rank-dial

**Idea.** A helper read by many outputs is a bus (ae-cross fact D). In ad-6, at low rank, every bus pays in full: N
outputs, o(N) helpers, one gate per output. In ad-2, at full rank, the realised saving of every bus is 0. The reason
offered is rank: N outputs made by one gate each from V helpers have rank at most V, so at full rank V >= N and
nothing is left to share. Between the two ends there is a dial, the degree d, and nobody has turned it. Find the rank
at which the bus stops paying and the invariant that turns it off.
**Words.** The object is the matrix of brief 1: subset sums with only the inputs of size at most d kept (rank = number
of sets of at most d bits: 5, 11, 15, 16 at 16 points for d = 1 to 4). *Bus*, *cut*, *injection*, *delivery*,
*version*: as in brief 3 (ad-2.md section 2). *Realised saving* of a bus: gates saved in the lower half minus what
the bus cost. *Decorated-cut search*: ad-2's exact enumeration of all ways to decorate a minimum upper circuit.
**Start from.** ad-2.md sections 2 to 5; `ad-2-twodeliveries/deco.py`, `free8.c`, `ranks.py`; ad-6.md section 1;
`d-0-zeta/mincirc`, `ad-7-modulo4/enum2` (prints every minimum circuit).
**First experiment.** 16 points, d = 1, 2, 3, 4, over the two-element field (and modulo 3 for d <= 2, where the size
limit of `mincirc` allows it): least gates; in every minimum circuit the longest bus and its realised saving. One
table: d, rank, least gates, gates per point, longest bus, realised saving. Brief 1 computes the first three columns
too: share them. Then say which quantity changes between the last d where a bus pays and the first where it does not.
**Growth law.** By ad-2's ceiling, f(2n) >= 2 f(n) + 2n / rho(n) with rho the longest paying bus: the law is rho as a
function of rank/N. If buses pay up to a rank that is a fixed fraction of N, the low-degree part of the transform is
linear and the whole cost sits in the middle digits; if they stop at rank o(N), ad-6 is the end of that road.
**Keep asking.** What does a bus need from the lower half that full rank takes away?

## 9. the-best-bad-circuit

**Idea.** Every record of the night seems to be an identity of the whole class of 2 x 2 kernels: replace 1, 1, 1, -1
by letters and the same circuit still computes the tensor power (k-cross; checked for the 19-gate circuit). Then no
record uses what only the transform has: H H = N, the reflection, the eigenvectors. A circuit that does use it must
FAIL for a perturbed kernel, and such circuits may be worse at small sizes, which is why a search for the least count
never keeps them. So look for circuits that are slightly worse and special.
**Words.** *Kernel*: a 2 x 2 matrix K; its k-th tensor power is the N x N matrix whose entry is the product of the
entries of K picked by the bits of the two addresses; H is the case K = (1, 1; 1, -1). *Wiring*: which two wires each
gate reads, coefficients left free. A wiring is *of the class* if for a kernel with general entries some choice of
coefficients computes its tensor power; *special* if it works for H and fails for the kernel (1, 1; 1, -1 + e).
*Halving*: as in brief 2.
**Start from.** k-cross.md section 2; d-2.md and `d-2-letters/` (the letter programs `lm.c`, `lm2.c`, `lm3.c`); p-0.md
and `p-0-classtest/`; `g-1-tightwires/h8_19gates.txt`, `c19.py`; `e2-0-pieces/slp_4.txt` to `slp_64.txt`;
`ae-cross/h1_digits.py` (an 8-gate circuit at 4 points: a+b, c+d, their sum s, b+d, s - 2(b+d), s - 2(c+d), b+c,
s - 2(b+c)); `ad-7-modulo4/enum2` (prints every solution of `mincirc`).
**First experiment.** The census first: for each record (7, 19, 52, 128, 304) fix the wiring, put letters in the kernel
and decide whether coefficients exist (solve exactly, or modulo a large prime at a random kernel and then confirm).
Then enumerate all circuits for the 4-point transform with 8 and 9 gates (`enum2` modulo 13 or 37, m = 4 and 5) and for
8 points with 20 and 21 as far as the machine goes; keep the wirings that are special. Report what they contain that
the records do not: a halving, a wire that is a sum of whole rows, an eigenvector of H, a use of H H = N.
**Growth law.** For every special circuit: its count when composed with itself (4 -> 16 -> 256 points) against the
records' (3/4) N log2 N. Only a special circuit can have a rate that is not a property of the whole class, and the
class contains kernels for which no saving exponent is expected; a special family whose rate falls with the size is
what to look for. If the census shows that some record is already special, say which, at once.
**Keep asking.** What can a circuit do with H H = N that it cannot do for a neighbouring kernel?

## 10. irrational-constants

**Idea.** The cost model charges one unit for ANY complex constant (`scale (c : ℂ)`, R/OAI/Computability/
FourierCircuit/Core.lean [read by z-0]). The height wall of wave 7 is a statement about whole-number wires: with
entries of size at most M, coefficients are bounded and one gate brings at most about 2 log2 M + 2 units, so C N gates
need whole numbers of about (log2 N)/(4C) digits. With sqrt 2 this fails in the smallest case [ran by z-0]:
e = (sqrt 2 - 1)^j, u = (1, 0), v = (1, e), w = (0, 1) = (v - u)/e; every entry has size at most 1 and the coefficient
(1 + sqrt 2)^j has no limit. No pool or annealer of nine waves contained a constant that is not rational, and the
transform's own unitary form has entries (-i)^(Hamming distance) up to free phases. Run the experiment wave 7 left
unassigned.
**Words.** *Gaussian integers*: a + b i. *Ring of the eighth roots of unity*: whole-number combinations of 1, z, z^2,
z^3 with z^4 = -1; it contains i and sqrt 2. *Golden ratio*: (1 + sqrt 5)/2. *A prime p splits* in such a ring when the
ring maps onto the whole numbers modulo p: for the eighth roots, p = 1 modulo 8 (17, 41, 73); for sqrt 5, p = +-1
modulo 5 (11, 19, 29, 31, 41). 41 has all of i, sqrt 2, sqrt 5; 17 has no sqrt 5 [derived: 17 = 2 modulo 5].
*Unitary form*: H with its entries replaced by (-i)^distance times free phases, that is D1 H D2 with diagonal D1, D2.
**Why a search modulo p covers the ring, and what it does not cover [derived, checked by nobody].** Take a circuit over
the ring's fraction field and a prime ideal above p with residue field the numbers modulo p. Scale each wire to be
primitive there and reduce: a gate stays a gate (the reduced wire lies on the line through the two reduced operands)
unless the two operands reduce to the SAME point; that collision is the ring's version of a halving (brief 2). For one
fixed circuit only finitely many primes have a collision or a vanishing coefficient, so a circuit over the ring shows
up modulo all but finitely many split primes. Hence: a NO modulo 17 and 41 is evidence and not a proof; a YES is a
candidate to lift. Two consequences worth stating in the report: every exhaustive search of the night modulo 5, 13 or
37 already contained i, and modulo 7 already contained sqrt 2 (3^2 = 2), so "no irrational constant was ever in a
pool" is true of the exact pools and annealers, not of the exhaustive searches. And in count (G) diagonal scalings are
free, so over any field that contains i the unitary form costs exactly what H costs.
**Already claimed [read: g-1.md line 61, `g-1-tightwires/min4.out`; unreviewed].** "No 6-gate circuit at 4 points over
any field of characteristic 0": with 6 gates, 4 are outputs and 2 are helpers; the first wire containing all four
inputs needs three gates under it, so it is an output and the helpers are its tree; 60 cases, none reaches all four
outputs. If the argument uses nothing about the field, the minimum at 4 points is 7 for Gaussian integers, eighth
roots, sqrt 2, the golden ratio and the unitary form alike.
**Start from.** z-0.md section 4 item 1 and `z-0/small.py`; WAVE7-NOTE.md section 3; g-1.md line 61,
`g-1-tightwires/ref.py` (mode `min4`), `sa8.py`, `flipwalk.py`, `pool.py`; `d-0-zeta/mincirc`, `rows_had2.txt`,
`rows_had3.txt`; `e2-0-pieces/pool.py`, `walk.py`; x-8.md (nearly dependent wires).
**First experiment.** (a) 4 points, ten minutes: check g-1's argument line by line for a hidden use of the rationals,
and replay it independently with `mincirc 17 4 2` and `mincirc 41 4 2` on `rows_had2.txt` (6 gates = 4 outputs + 2
other wires; 41^4 is inside the size limit). (b) 8 points, the hour: `mincirc` cannot go there (p^8 must stay below
6e6, so p <= 7, and 18 gates means 10 free wires). Put the constants in the pool instead: run g-1's and e2-0's
annealers for 18 gates with wires and coefficients modulo 17 and 41 (all coefficients allowed), and exactly over the
Gaussian integers and over a + b sqrt 2 with small a, b. Lift any hit: fix the wiring, solve the coefficient equations
in the ring, replay exactly. (c) In count (O), where scalings are charged, price the unitary form at 4 and 16 points
with Gaussian coefficients against the 60 operations known for H x / 4 at 16 points.
**What an irrational constant could do that a rational one cannot.** Keep every wire small in every entry while the
coefficients grow without limit; a rational circuit cannot (that is the height lemma). In a number field of fixed
degree d with "size" taken over all conjugates the lemma returns with the bound (2 M^2)^d [derived by z-0, not run], so
a real escape needs constants whose degree grows with N, or wires small in one embedding and large in a conjugate one.
Morgenstern's bound [recalled] still charges coefficients by their absolute value, so the escape is not "bounded
coefficients" but "bounded wires". x-8 found that the textbook rate does not depend on how nearly dependent the wires
are, for rational coefficients only.
**Growth law.** The height wall gives at least N log2 N / (4 + 4 log2 M) gates for whole-number wires of size at most
M. For the eighth roots of unity the same form with d = 4 is expected; the experiment's law is whether the least count
found at 8 and 16 points with irrational pools falls below the rational records at all. A single specimen where
sqrt 2 saves a gate that no rational coefficient saves, for any matrix of the transform's kind, would be the first
object of the night outside the height wall; none found means the wall extends in practice, with sizes.
**Keep asking.** What does a wire that is small in one embedding and large in its conjugate carry, and can a gate
cash it in?
