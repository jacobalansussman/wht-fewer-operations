# ag-9: irrational constants (Gaussian integers, eighth roots of unity, sqrt 2, the golden ratio)

11 October 2026, 08:16 to about 09:10 EDT, 60-minute box. Developer ag-9-irrationalconsta, one agent. Private research: nothing
published, no git, no Lean, nobody has read this. Folder: `ag-9-irrationalconsta/` (all paths below are inside
`waves/`).
Marks: [read] = in a file I opened tonight; [ran] = my own run tonight (exact, or modulo a prime where said); [derived] = by
hand tonight, checked by nobody; [recalled] = from memory; [guess].
Gate count: **(G)** everywhere (a gate is any a*u + b*v, scalings free) unless **(O)** is said (OpenAI's: every addition,
subtraction and multiplication by a constant costs one).

**In one paragraph.** Constants that are not rational cannot change the order of growth as long as their degree stays
bounded. Reason, a short lemma [derived, and run exactly on one circuit]: a circuit with s gates whose constants lie in a
number field of degree d turns into a circuit with rational constants and at most d*d*s gates (2*d*d*s in count (O)). So for
Gaussian integers, sqrt 2 and the golden ratio (d = 2) the gain is at most a factor 4, for the eighth roots of unity (d = 4)
at most 16, and the saving exponent z is the same over the rationals and over every such field. No circuit below a
known count was found: at 4 points 7 gates is the minimum over every field of characteristic 0 and modulo 17 and 41
(exhaustive), and modulo 7, 13, 17 and 41 it is 7 for every 2 x 2 kernel of the transform's kind (780 pairs modulo 41,
exhaustive modulo each prime, not a proof for characteristic 0); at 8 points
168 annealing runs (504 million moves) modulo 3, 5, 7, 13, 17, 31, 41, 73 with every coefficient allowed, all started near the known
19-gate circuit, found no 18. **No growth law
below N log N. Nothing here passes the bar of 1e-1.** What stays open is only constants whose degree grows with N (at least
about sqrt(log2 N)), and that is the same open problem as rational circuits with unbounded coefficients.

Words. N = 2^k points; H = the transform, entries +1, -1. T_F(N) = least number of gates (G) for H when the constants may
be taken in the field F. *Number field of degree d*: the rationals with one more number adjoined that is a root of a
polynomial of degree d (sqrt 2: d = 2; i: d = 2; the eighth root z with z^4 = -1: d = 4); every number in it is written in
one way as q_0 + q_1*b_1 + ... + q_(d-1)*b_(d-1) with rational q's (for sqrt 2: q_0 + q_1*sqrt2). *Embedding*: one of the d
ways of reading such a number as a complex number (sqrt 2 can be read as +1.414 or as -1.414; both readings respect every
sum and product). *Unit*: a number of the ring whose inverse is also in the ring (1 + sqrt2, inverse sqrt2 - 1).
*Helper*: a wire that is not an output.

## 1. The lemma that decides the growth law [derived; run exactly on one circuit]

**Lemma (restriction of scalars).** Let K be a number field of degree d and A a matrix with rational entries. If A has a
circuit with s gates and constants in K (count (G)), it has a circuit with at most d*d*s gates and rational constants.
In count (O): at most 2*d*d*s.

Proof. Scalings are free, so write every gate as w = u + c*v. Write every wire in parts, w = w_0 + b_1*w_1 + ... +
b_(d-1)*w_(d-1), the parts being rational vectors. Multiplying by c is a d x d rational matrix C acting on the parts, so
part j of w is (part j of u) + sum over l of C_jl * (part l of v): a sum of at most d + 1 rational wires, d gates. There are
d parts: d*d gates. The inputs have one non-zero part, themselves. An output is lam * (a rational row) with lam in K not
zero, so one of its parts is a non-zero rational multiple of the row. (In count (O) each part costs d scalings and d
additions.) End of proof. Nothing about H is used.

**Run** [ran, `restrict.py`, exact fractions]: on a 9-gate circuit over the numbers q_0 + q_1*sqrt2 (the specimen of section
6, 5 outputs on 4 inputs) the construction gives a rational circuit of 13 gates (the bound is 4 per helper and 2 per output
gate, 26); every part replays exactly.

**Consequences.**
- T_Q(N) / d^2 <= T_K(N) <= T_Q(N). **Linear size over a field of bounded degree is linear size over the rationals.** A
  program in O(n (log n)^z) with constants of degree d is one in O(d^2 n (log n)^z) with rational constants: the same z.
- Gaussian integers, sqrt 2, golden ratio: at most a factor 4. Eighth roots of unity: at most 16. Both sizes of the brief
  (6 against 7 at 4 points, 18 against 19 at 8) were therefore questions about a constant, whatever their answer.
- Numbers that satisfy no polynomial equation (pi, e) never help: a wiring with s gates computes H for the constants that
  solve a system of polynomial equations with rational coefficients, and such a system with a complex solution has a
  solution in a number field [recalled: Hilbert's Nullstellensatz]. But the degree of that field is not bounded by this
  argument.
- **What is left**: constants whose degree grows with N. If rational circuits really need c*N*log2 N gates, a circuit of C*N
  gates over K needs d >= sqrt(c*log2 N / C). At 2^40 points and C = 2, c = 1/2: degree 4 or more. So a degree that grows
  at least like sqrt(log2 N). I know no construction that uses a degree; the lemma's factor d*d is the cost of a generic
  multiplication table and may be far from sharp.
- z-0 had the same fact in the weaker form "in degree d the height lemma returns with (2M^2)^d" [read, z-0.md section 4
  item 1]. The lemma above needs no height and no bound on any wire.

**What the cost models give** [read]. The circuit model charges one unit for `scale (c : C)`, any complex constant
(`R/OAI/Computability/FourierCircuit/Core.lean` lines 9 to 17). The RAM model does not: "There is no instruction for an
arbitrary complex constant. A supplied specified root will be an input" (`R/OAI/Computability/FourierTransform/RAM.lean`
lines 27 to 29); scalars are made from the number 1 (`cone`), `inv` and the arithmetic, plus one root of unity whose order
the program chooses from the length (`Goal.lean` lines 46 to 56). So a RAM program's constants are rational combinations of
powers of one root of unity. All four rings of the brief are of that kind (i: order 4; sqrt 2 and the eighth roots: order
8; the golden ratio: order 5), and the degree can grow with n there, since the order is the program's choice.

## 2. Four points: 7 is the minimum over every field tried, and for the whole class of kernels

- **g-1's argument, checked line by line** [read g-1.md line 61; derived]. With 6 gates, 4 are outputs (every row of H has
  four non-zero entries, so no output is an input and no two outputs are parallel) and 2 are helpers. A wire with all four
  inputs in it has at least three gates at or under it, and the first such wire has only helpers strictly under it, so it
  is an output, the two helpers are exactly its tree, and each input enters once. A helper is then that output cut down to
  the inputs under it, times a non-zero constant: it is a vector with entries 0, +1, -1 whatever the coefficients were.
  The remaining test "is this output on the line through two held wires" is a rank of vectors with entries 0, +1, -1.
  A rank does not change when the field is enlarged. **Nothing uses the rationals.** The one hidden hypothesis is the
  characteristic: modulo a small prime a rank can drop, since the minors are small whole numbers and not only 0, +1, -1.
- g-1's own 60 cases run again [ran, `ref.py min4`, `g1_min4_replay.out`]: every case reaches 2 outputs, never 4.
- **Independent replay** [ran, `d-0-zeta/mincirc`, exhaustive modulo p]: `mincirc 17 4 2` and `mincirc 41 4 2` on
  `rows_had2.txt`: NO circuit with 6 gates modulo 17 and modulo 41; with one more wire, YES, 7 gates. 17 contains i, sqrt 2
  and the eighth roots (2 itself has order 8 modulo 17); 41 contains those and sqrt 5, the golden ratio, the fifth roots.
- **The whole class of kernels** [ran, `scan4.py`, `scan4_p*.out`]. Up to free scalings every 2 x 2 kernel with non-zero
  entries is K_t = (1, 1; 1, t); the transform is t = -1. For the 4-point matrix K_t (x) K_s, exhaustive search:

  | prime | pairs (t, s), t <= s, t and s not 0 or 1 | least gates |
  |---|---|---|
  | 7 | all 15 | 7 for every pair |
  | 13 | all 66 | 7 for every pair |
  | 17 | all 120 | 7 for every pair |
  | 41 | all 780 | 7 for every pair |

  So no special constant (a root of unity of order 3, 4, 5, 8, 10, 20, 40, sqrt 2, the golden ratio, anything else in
  these fields) makes a 4-point kernel square cheaper. At this size the count is a property of the class, as k-cross said
  of the 19, and the class has no cheap member.
- What a search modulo p covers [the curator's derivation, WAVE10-PICKS section 10; I agree]: a circuit over the ring shows
  up modulo all but finitely many primes that split, so "NO modulo 17 and 41" is evidence; here the field-free argument
  makes it a proof for characteristic 0. Every exhaustive search of the night modulo 5, 13, 37 already contained i, and
  modulo 7 already sqrt 2.

## 3. Eight points: no 18 with every coefficient allowed [ran; an annealer's result, not a minimum]

Tool: `fpgame.c` (x-2's `hatch.c` with the arithmetic replaced by the whole numbers modulo p). A wire is a point (a vector
up to scale); a set of wires is a circuit when every wire lies on the line through two wires derived before it; the walk
replaces one helper at a time (a combination of two held wires with ANY non-zero coefficient, or a held wire changed on a
block, a hyperplane or one entry, or a random vector). Pool 0: any coefficient. Pool 1: only +-1, +-2, +-1/2 (control).
Pool 2: half and half.

Checks of the tool. The 19-gate circuit of g-1 is accepted modulo 17 with the right parents (`control_seed19_accepted.out`).
From a random start pool 1 finds a 19-gate circuit modulo 17 after 2.6 million moves (`control_random19_pool1.out`); pool 0
finds none in 3 million (`control_random19_pool0.out`): with every coefficient allowed the walk does not build a circuit
from nothing. From the 20-gate circuit with one helper dropped (15 runs modulo 41, 1.5 million moves each,
`control_from20.out`): a 19 is found in 3 of 3 runs with pool 1, 2 of 6 with pool 0 and 1 of 6 with pool 2. So the walk
can take one gate off a known circuit, in about one run in three when all 40 coefficients compete. That is the power of
the search below: it looks near the known 19, not everywhere.

Runs for 18 gates (10 helpers), each 3 million moves, started from the 19-gate circuit with one helper dropped at random
unless said:

| prime | what it contains | pool | file | runs | moves | least number of underivable wires (runs) |
|---|---|---|---|---|---|---|
| 3 | only +1, -1 | 0 | `l3_pool0.out` | 11 | 33 million | 2 (11) |
| 5 | i | 0 | `l5_pool0.out` | 10 | 30 million | 2 (10) |
| 7 | sqrt 2, cube roots of 1 | 0 | `l7_pool0.out` | 17 | 51 million | 2 (17) |
| 13 | i, cube roots of 1 | 0 | `l13_pool0.out` | 12 | 36 million | 2 (7), 3 (1), 4 (1), 8 (3) |
| 17 | i, sqrt 2, eighth roots | 2 | `l17_pool2.out` | 28 | 84 million | 2 (19), 3 (3), 4 (1), 8 (5) |
| 17 | the same | 0 | `r17_pool0.out` (Linux) | 7 | 21 million | 2 (4), 3 (2), 4 (1) |
| 31 | sqrt 2, sqrt 5, golden ratio, fifth roots; no i | 2 | `l31_pool2.out` | 6 | 18 million | 2 (5), 8 (1) |
| 41 | i, sqrt 2, eighth roots, sqrt 5, golden ratio, fifth roots | 2 | `l41_pool2.out` | 28 | 84 million | 2 (16), 3 (2), 8 (10) |
| 41 | the same | 0 | `r41_pool0.out` (Linux) | 8 | 24 million | 2 (2), 4 (1), 8 (5) |
| 41 | the same, colder walk (temperature 0.12) | 0 | `l41_pool0_cold.out` | 13 | 39 million | 2 (4), 3 (1), 8 (8) |
| 41 | the same, started from the 20-gate circuit with two helpers dropped | 0 | `l41_from20_pool0.out` | 22 | 66 million | 4 (1), 8 (21): this start does not hold |
| 73 | i, sqrt 2, eighth roots, cube roots | 2 | `l73_pool2.out` | 6 | 18 million | 2 (4), 4 (1), 8 (1) |

**168 runs, 504 million moves, no circuit with 18 gates.** (A second pair of jobs on the Linux machine, modulo 31 and 73,
finished no run in 14 minutes: the machine was loaded, load 11 to 12, and my jobs ran at the lowest priority. The two rows
for 31 and 73 are local runs of five minutes each.)

Least number of wires left underivable: 2 in the best runs of every prime, never 1, never 0. A run that ends on 8 has lost
the seed. Modulo 17 the residues cannot tell i from 4, sqrt 2 from 6 or the eighth root from 2, so those runs also contain the
images of rational circuits whose wires have entries up to 8 in size, as long as no two of their wires fall together
modulo 17 [derived]. Modulo 3 the only coefficients are +1 and -1: no 18 in small
characteristic either.
Not done: an exact pool over a + b*i or a + b*sqrt2 (the runs modulo split primes contain those rings, and a hit would have
been lifted; there was none to lift); 16 points; a start that is not the 19. The exact minimum at 8 points stays open, 15 to
19, as before.

## 4. Count (O) and the unitary form [derived; nothing run]

The unitary form is U = D H D with D = diag(i^weight), entries i^(Hamming distance). Hence in count (O), where the outputs
must be exact, |T_O(U) - T_O(H)| <= 2N (the two diagonals; the signs -1 can be absorbed by turning additions into
subtractions, which would leave N [guess]). At 2 points: H costs 2 (one addition, one subtraction); U = (x + i*y, i*x + y)
costs 4 by hand (i*y, x + i*y, x - i*y, times i) and I see no 3. At 16 points: at most 56 + 32 = 88 for U x / 2 against
h-3's 56 for H x / 2. **In count (O) the unitary form is dearer than H, by something between 0 and 2N, and can never be
cheaper by more than 2N.** In count (G) the two cost the same, since diagonal scalings are free. A difference of order N
cannot change the order of growth. No reason was found to price it by search.

Two identities met on the way [derived]:
- **The transform is a convolution, over the Gaussian integers only.** weight(x xor y) = weight x + weight y - 2*(x.y),
  so i^(weight(x xor y)) = i^(weight x) * i^(weight y) * (-1)^(x.y). Hence H = D' C D' with D' = diag(i^(-weight)) and C the
  convolution over the cube with the kernel i^weight (output(x) = sum over y of i^(weight(x xor y)) * input(y)). This puts the transform inside WAVE7's
  idea D (kernels that depend only on the number of ones); over the rationals it is not a convolution at all. The kernel is
  its own spectrum up to a factor: its transform is (1+i)^k * (-i)^weight.
- **U = constant * exp(i*pi*A/4), A the adjacency matrix of the cube** (N*k/2 edges). [recalled: this is the uniform mixing
  of the quantum walk on the cube at time pi/4.]
- Neither gives a count. Among circuits that commute with all translations of the cube (every step is "array = a*array +
  b*shifted array", N gates each) the kernel needs k steps, because one step at most doubles the number of non-zero entries
  of the kernel and the kernel i^weight has all 2^k: N log2 N, the textbook [derived; the same shape as j-cross's lemma on
  product wires].

## 5. Keep asking: what does a wire carry that is small in one embedding and large in the other?

z-0's example: e = (sqrt2 - 1)^j, u = (1, 0), v = (1, e), w = (0, 1) = (v - u)/e. Read with sqrt 2 = +1.414, v is almost u and
the gate has the huge coefficient (1 + sqrt2)^j. Read with sqrt 2 = -1.414, e is huge, v is almost w, and the same gate has
coefficients of size about 1. [derived]
- **It carries two ordinary rational wires, nothing more.** v = v_0 + sqrt2*v_1 with v_0, v_1 rational; the two readings are
  v_0 + 1.414*v_1 and v_0 - 1.414*v_1. Section 1 turns every gate on v into at most 4 rational gates on v_0 and v_1.
- **Both readings are circuits for H**, because H is rational. Morgenstern's ledger (the largest determinant of N wires may
  grow by at most |a| + |b| per gate, [recalled]) must be paid in each reading separately. A gate that is expensive in one
  reading and free in the other pays in one ledger only. A circuit below N log N needs large coefficients in EVERY
  reading.
- **What is really new with sqrt 2 is the units.** Among whole numbers and among Gaussian integers the only units are +-1
  (and +-i): a coefficient is large only if it contains a prime or a denominator, and that is what the height of a wire
  measured. In the rings of sqrt 2, of the golden ratio and of the eighth roots there are units of every size,
  (1 + sqrt2)^j. So size and arithmetic come apart: this is exactly why the height lemma fails there (z-0), and it is all
  that fails. The underlying wall, "small coefficients force N log N", is about sizes of complex numbers and never asked
  whether they were rational.
- **Can a gate cash it in?** Not as volume: with wires scaled to largest entry 1, the gate w = u + E*v with E huge gives w
  almost equal to v and gains nothing; volume is gained only where two nearly parallel wires are subtracted, and nearly
  parallel wires are as cheap with rational constants (v = (1, 1/1000)) as with units. The unit only keeps the entries'
  digits short, and neither cost model charges digits.
- Roots of unity alone are the opposite case: they have size 1 in every reading, so a count-(O) program whose scalings all
  have size at most 1 needs at least (N/2) log2 N additions for H x exactly [Morgenstern, recalled; derived for this case].
  A large constant has to be built (for example 1/(1 - root)), as in the rational case (2, 4, 16, ...).

## 6. A specimen where sqrt 2 would save a gate: built, not settled [ran in part; the claim is a guess]

Aim: the brief's "one specimen where sqrt 2 saves a gate that no rational coefficient saves". By section 1 such a specimen
can only be a constant, so I gave it little time.
Design [derived]: helpers with sqrt 2 in them, each one gate from two inputs: h1 = e1 + a*e2, h2 = e2 + b*e3, h3 = e3 + c*e1,
h4 = e1 + d*e4. Outputs: the point where the line h_i h_j meets its mirror line (sqrt 2 replaced by -sqrt 2), for the pairs
12, 13, 23, 14, 34; that point is its own mirror, so it is rational. 9 gates over the numbers q_0 + q_1*sqrt2 against 10
by the plain way (each output has three non-zero entries and costs 2 alone). A helper with sqrt 2 in it lies on only one
rational line, so no output can sit on a line through it and a rational point. For given outputs, finding the helpers of
this wiring is the old problem of drawing a triangle inside a triangle with its sides through three given points
[recalled: Castillon's problem], a quadratic equation; here its two roots are the sqrt-2 helpers and their mirror, so
this wiring has no rational solution unless the system has further roots [guess]. Other wirings with 9 gates are not
excluded by this.
[ran, `spec4.py`, exact]: with a = 1 + 2*sqrt2, b = 3 - sqrt2, c = -2 + 3*sqrt2, d = 5 + 2*sqrt2 the outputs are
(1, -5, -14, 0), (1, 21, -2, 0), (14, 3, 11, 0), (4, 7, 0, 17), (11, 0, 2, 51) and every output lies on the line of its two
helpers (`spec4_b.txt`).
**What failed** [ran, `spec4_*_mincirc.out`]: `mincirc` finds circuits with 8 gates modulo 13, 17, 19 and 23 alike, with or
without a square root of 2 in the field. **What the failure is made of** [derived]: with 5 outputs and 3 or 4 helpers the
conditions outnumber the free coefficients by 2 or 1, so each wiring has a solution modulo p with chance about 1/p^2 or
1/p, and there are far more wirings than p^2 = 529; the hits are accidents of small primes (one I checked modulo 17 is
false over the rationals: (1, 1, -1, 0) + 4*(0, 1, 1, 0) is (1, 5, 3, 0), which equals (7, 1, 4, 0) only modulo 17). For the
transform at 4 points this trap is absent (the "NO" has no accidents to hide behind). So a search modulo small primes
cannot settle a specimen of this kind; it needs an exact search over wirings with the incidences solved in fractions.
The rational minimum of this matrix is not determined: 9 over sqrt 2, between 7 and 10 over the rationals. A first
version in three inputs (`spec3.py`) fails more plainly: a plane modulo a small prime is full (with 7 held points the lines
through pairs already cover every point modulo 13).

## 7. Going around, twice

1. "No 6 at 4 points with sqrt 2" became "is there ANY constant t for which the kernel square is cheaper": no (section 2).
2. "No specimen for H" became "what would a specimen be worth": at most a factor d*d (section 1), and then "where can a
   degree grow": the RAM model hands out one root of unity of any order, and a root of unity is a bounded coefficient
   (section 5). So the growing degree would have to come with large constants built from the root; no construction.

## 8. Growth law, wall, what is left

- **Growth law: none below N log N.** For constants in a field of degree d: T_K(N) >= T_Q(N)/d^2; whatever the rational
  rate is, the rate with such constants is the same up to the factor d^2.
- **Wall (named): RESTRICTION OF SCALARS.** A number of degree d is d rational numbers and a multiplication table; a gate
  on it is at most d*d rational gates. Together with wave 7's height wall this closes "bounded wires and bounded degree".
- Open, and outside this idea: constants of degree growing like sqrt(log2 N) or more. That question has no arithmetic left
  in it; it is "circuits with unbounded complex coefficients", Valiant's problem, the same as for rational circuits with
  tall wires.
- Mutations worth a brief, in order of my belief (all low):
  1. Is the factor d*d ever real? Find a rational matrix family with T_K = o(T_Q) for a growing degree. The one known
     candidate [recalled] is multiplication by a fixed polynomial modulo x^N - 1: N log N with the complex roots of unity,
     N log N loglog N known without them. If a loglog is all a growing degree ever buys, the idea is dead for the bar.
  2. The exact rational search that settles the specimen of section 6 (a constant; only for the record).
  3. The convolution form H = D' C D' with the kernel i^weight (section 4): run WAVE7's "map of convolutions" with Gaussian
     kernels q(weight), where the transform is a member and not a limit.

## Files (in `ag-9-irrationalconsta/`)

`fpgame.c` (the annealer modulo p; usage in its header), `batch.sh`, `seed8_19.txt`, `seed8_20.txt` (helpers of the known
circuits, from h-1); `control_*.out` (the checks of the tool); `l*_*.out` (local runs), `r*_*.out` (runs on the Linux
machine, copied back; nothing of mine is left running there); `g1_min4_replay.out` (g-1's 60 cases, run again); `scan4.py`, `scan4_p7.out`, `scan4_p13.out`, `scan4_p17.out`, `scan4_p41.out`, `scan4_p41_diag.out`;
`restrict.py`, `restrict.out` (the lemma on one circuit); `spec4.py`, `spec4_a.txt`, `spec4_b.txt`, `spec4_*_rows.txt`,
`spec4_*_mincirc.out`; `spec3.py`, `spec3_rows.txt`, `spec3_mincirc.out` (the plane version).
Not done: the lemma is run on one circuit of degree 2 only; no exact pool over a ring; nothing at 16 points; the count (O)
prices of section 4 are by hand; Morgenstern's article was not opened; the specimen's rational minimum is open.
