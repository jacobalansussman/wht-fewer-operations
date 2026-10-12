# j-machine: let the machine propose

Private notes, 2026-10-10, 21:39 to 22:18 EDT. Nothing here is in Lean or reviewed. Tags: [read] [ran] [derived] [guess].
**Gate count used everywhere below: (G)** — a gate is any a*u + b*v, scalings and relabellings free. Nothing here is in
OpenAI's count (O). In count (G) the textbook costs N*log2(N): 8, 24, 64 at 4, 8, 16 points; best known tonight 7, 22, 56.

Words used. A *form* is a linear combination of the inputs. A *node* is a form the program has already built (the inputs are
nodes). For an output t, **d(t)** is the number of gates needed to finish t from the current nodes with no further sharing:
(fewest nodes whose combinations contain t) minus one. The **potential** is P = sum of d(t) over all outputs. The **drain**
of a gate is how much P falls when the gate is added. A **centre** is a form with every input in it that is not itself an
output but from which several outputs are one gate away.

## 1. What I built, and which design worked

Three searchers (a fourth program, the greedy builder, is in section 3), all in `j-machine/`, all run on the rented Linux machine (which was loaded: about 10 to 60 states a second).

| tool | what it varies | what happened [ran] |
|---|---|---|
| `slp.py` | the wiring; coefficients solved by Levenberg-Marquardt, 6 starts each | **Needle landscape.** 20,181 wirings at 4 points, 7 gates: 4 reach zero, all others end with squared error above 1. 14,694 wirings for two 4-point copies in 13 gates, 7,434 for 8 points in 21 gates, 152 for 16 points in 55: none reach zero, none come close. No wiring landed between 1e-20 and 1. |
| `relax.py` | every gate starts as a dense mix of all earlier nodes and is squeezed to two operands | 192 runs at 4 points, 7 gates: none hardened into a correct circuit. A failed tool; kept for the record. |
| `steiner.py` | **only the helper forms**; the outputs finish themselves; the energy is U = (gates built) + P, which is the size of an honest circuit | **Smooth landscape.** 4 points: 7 gates from nothing in 0.5 s, 42 different 7-gate shapes in 15 s. Two copies: 14 from nothing in 92 s. Every new best is replayed exactly in fractions. |

What the machine found, exact replays, count (G):

| target | textbook | known | from nothing | around the known circuit |
|---|---|---|---|---|
| 4-point transform | 8 | 7 | 7 | 4 further 7-gate wirings, each an isolated solution |
| two 4-point transforms at once | 16 | 14 | 14; never 13 in 16,944 states | no 13 in 14,489 states |
| 8-point transform | 24 | 22 | annealing: 24, 25, 28 (7,295 states); steepest drain: **23**, 25, 25, 27 | two more 22-gate shapes; no 21 in 3,480 states |
| subset-sum matrix, 8 points | 12 | 12 | 13 (17,767 states) | no 11 in 15,402 states |
| subset-sum matrix, 16 points | 32 | 32 | not run | no 31 in 3,135 states |
| cousin with entries 2^(Hamming distance), 8 points | 24 | ? | annealing 26, 26; steepest drain 25 | — |
| 4 of the 8 outputs (rows 0-3 of J4 x H2) | — | — | **12** | 11 by hand from the machine's shape [ran for rows 0,2,4,6 in `hand17.py`; the same for rows 0-3 by the transform's symmetry, derived] |
| 4 of the 8 outputs (rows 0,2,4,6) | — | — | 14 | 11 [ran, `hand17.py`] |
| 6 of the 8 outputs | — | — | 20 | 17 [ran, `hand17.py`] |

**Calibration, to be read before anything else:** from nothing the tool did NOT rediscover 22 at 8 points in five minutes, and
its 14 and 20 for partial targets are above what I can write by hand. So "no 21 found" and "no 13 found" are statements about
a slow tool on a busy machine, not about the transform. 16 points was not really run (a cap of 40 gates in my code rejected
every move from the 56-gate start; my bug).

## 2. Ideas

### 1. Search the helpers, not the wiring
Construction: the state is a list of helper forms, each on the line through two earlier nodes. The score is
U = (helpers built) + sum of d(t). U is always the size of a real circuit, so every state is an answer and every improvement
is exact. Moves: add a helper, delete one, change one. Rewrite the inner step (which 2, 3 or 4 nodes span this output) in C
modulo a large prime, with exact replay of each new best; that step is all the cost.
[ran] It is the only one of three designs that found the 7-gate circuit by itself, and it found 42 shapes of it.
[guess] In C it reaches 16 points, where nobody has searched at all (i-cousins: "k = 3, 4 minima are unknown").

### 2. Full-drain gates: a potential a linear program must empty at a constant rate
For the N-point transform P starts at N(N-1) (every output needs all N inputs) and ends at 0. One gate can lower P by at most N
(one step for every output). So a program of size c*N must drain about N/c per gate **on average**: a constant fraction of its
gates must bring a constant fraction of ALL outputs one step closer. [derived]
The textbook at 8 points drains 4, 2, 1 per gate in its three layers: N/2, N/4, ..., 1. Each layer costs N gates and does half
the work of the one before; that is the log. [derived]
The 7-gate brick is different in kind: at 8 points, after the two pair sums of a block of four (drain 4 each), the gate that
completes the block sum drains 8: every output gets closer at once. [derived] Such a gate is a *full-drain gate*.
Construction: build programs greedily by drain (`greedy.py`: try every pair of nodes with coefficients +-1, +-2, +-1/2, add the
form that lowers P most). Then ask the question the profile poses: after the first N gates, which forms still drain N/4 or
more? The textbook has none. A linear program is exactly a supply of them that does not run out.
[ran] It works as a builder: 7 at 4 points and 14 for two copies with no search, 23 at 8 points (section 3).
Yes, and: steepest drain with a one-gate lookahead, or with ties broken by "is this form a by-product I will need", is a
polynomial-time builder that can be run at 16, 32, 64 points to see how its size grows with N. That growth curve is the
experiment: N*log N with a smaller constant, or something flatter.

### 3. Hang the outputs on a centre and pay for the corrections with the centre's own partial sums
The machine's 12-gate circuit for four of the eight outputs (`j-machine/r3/steiner_H8r0123_s21_empty_best.json`) [ran, exact]:
build ONE form c = (1,1,-1,-1,-1,1,-1,1) in 7 gates. It is not an output. Three outputs are c plus or minus twice a
two-input form, and those two-input forms are the first gates of the tree that built c. The fourth output hangs on the
last-but-one node of the same chain.
Read as a recipe [derived]: c is a sign vector at Hamming distance 2 from four rows (for the code made of the 16 signed rows at
8 points, such a c sits at distance 2 from 4 rows, 4 from 8, 6 from 4). The four pairs where it differs are disjoint, so make
them the bottom of c's tree: 4 + 3 + 4 = **11 gates for half the outputs**.
The known 22 is this twice [derived]: one centre made of the four pair SUMS serves four rows, a second centre made of the four
pair DIFFERENCES serves the other four, and the two halves share nothing. That is where a 21 would have to come from.
The rows of the second half differ from the first centre on a set with one input from each pair (I checked this by
orthogonality: it must meet every pair once). Hanging them on the first centre gives 15, 17, 21, 23 for 5, 6, 7, 8 outputs [ran, exact replay, `hand17.py`];
a second centre gives 19, 20, 21, 22 [derived]. **The fifth output is the expensive one** (4 gates either way, against 1 for the others).
Construction to try: aim `steiner.py` at five outputs (rows 0-3 and one row of the other half). Anything under 15 is a way for
the two halves to share, and that is the only kind of saving 8 points can have beyond 22.
At 16 points one centre serves ALL 16 rows (a bent function: distance 6 from every signed row), and the 16 corrections are the
blocks of the 16-point biplane (six points each, any two sharing two). Build that centre's tree so that the blocks are unions
of few tree nodes.
A picture that came out of the greedy 23-gate circuit (`j-machine/r4/greedy_H8_s2_best23.json`) [ran + derived]: after its
centre it walks to the outputs by changing ONE input at a time, sharing the intermediate stops. That is a tree in the cube of
sign vectors, rooted at the centre, with the rows as leaves and one gate per edge. If every edge changes a single input, each
of the 8 rows owns at least 2 edges (rows are 4 apart, so the stops within one step of a row belong to it alone): at least
7 + 16 = 23. **Single-input steps cannot beat 23 at 8 points, and at N points they cost at least N*N/4.** The 22-gate circuit
gets under 23 only because some of its steps change two inputs at once, using a pair form it already owns. So the general
shape of a cheap program is a tree of sign vectors in which every step's "what changes" is a form already built: a Steiner
tree whose allowed edges grow as the tree grows. Linear size means: N rows, each one step from two forms already there.

### 4. Peel a centre and look at what is left: a tower of half-norm remainders
Write H = 1*c^T - 2E with c a bent centre (N = 4, 16, 64). E has entries 0, +-1. [ran, exact integers, `tower.py`]:
rows of E have (N - sqrt N)/2 or (N + sqrt N)/2 non-zeros (1 or 3; 6 or 10; 28 or 36; flipping a row's sign picks the small
one), and **E*E^T = (N/4)*I + a matrix of rank exactly 2** at all three sizes (computed before any sign flips). [derived: 4EE^T = N*I + N*J - 1w^T - w1^T, w = Hc.]
So the remainder is again "an orthogonal matrix plus low rank", at half the norm and under half the density. At N = 4, E is a
relabelling and the tower ends: that is the 7-gate circuit. Construction: peel again. Find the form c2 and the rank-one (or
rank-two) piece whose removal from E leaves the sparsest remainder E2; compute its Gram matrix; repeat. After log2(sqrt N)
halvings the norm is 1, where an orthogonal 0,+-1 matrix is a free relabelling. Each peel costs about 2N gates if the peeled
piece has rank one, which gives N*log N again [derived], so the whole question is whether the peeled pieces of successive
levels can share their trees (idea 3) — the remainders get sparser, and a sparse level should cost less than 2N.

### 5. The subset-sum side has slack that the transform does not
For the subset-sum matrix Z (output x = sum of the inputs y contained in x) the potential starts at
sum over x of (2^|x| - 1) = 3^k - 2^k: 19 at 8 points, 65 at 16, against 56 and 240 for the transform. [derived]
Since H = Z*D*Z^T and D is free in count (G), the transform costs at most twice Z. So **the free diagonal manufactures the
difference between N^1.585 and N^2 of potential.** A linear program for Z needs an average drain of only about N^0.585 per gate,
far below the cap N; a linear program for H needs drain at the cap. The textbook for Z uses (k/2)*2^k gates, average drain
about 2*(1.5)^k/k.
[ran] Allowing subtraction and coefficients up to 8, the machine found nothing below 12 at 8 points or 32 at 16 (small samples).
Construction: run idea 1's tool on Z at 16 and 32 points with the moves biased toward forms that are sums over *intervals of
the subset order* cut by subtraction (a node that is "everything below x except what is below y"): those are the forms with
high drain for Z that the textbook never builds.

### 6. Outputs are not priced equally: the cost curve c(m) of the first m outputs
At 8 points, upper bounds [ran, exact replay, `hand17.py`; 22 is the known circuit]: c(1) = 7, c(4) = 11, c(5) = 15, c(6) = 17, c(7) = 21, c(8) = 22.
Seven gates buy the first output, one gate each buys the next three, then the price jumps. Construction: compute this curve
honestly (the tool on every orbit of m-subsets of rows at 8 points, then at 16) and look at WHERE it jumps. A linear program
needs c(m) to climb by O(1) per output all the way; each jump is a place where a new centre had to be bought. At 16 points one
bent centre is at distance 6 from all 16 rows, so the first guess is one jump only — and the question becomes the price of the
16 six-point corrections.

### 7. Nothing is "almost" a circuit, so count instead of solving
[ran] In about 42,000 wirings the squared error after optimisation was either below 1e-20 or above 1; never between.
(Limit: a start still above 0.5 after 8 steps was abandoned, so a wiring that converges very slowly would have been missed.) Every
exact circuit found had solution family of dimension 0 (the coefficients are pinned once scalings are fixed), with coefficients
1 and 2 only. No coefficient ran away to infinity anywhere; the pool offered 8 and 1/8 and the best circuits never used them
except in ways that cancel out.
Consequence [guess]: for these targets a wiring either works over the rationals with small numbers or not at all, so floating
point is the wrong instrument and exhaustive search modulo a small prime is the right one (isolated rational solutions survive
reduction modulo almost every prime). Construction: exhaustive search at 8 points for 21 gates modulo 5 and 7, organised by
idea 1's score as a bound (a state with U > 21 + slack is cut) and by the two-centre structure of idea 3.
The border route (coefficients to infinity) showed no sign of life in this sample; d-5-border says the same for 4 points.

### 8. Two copies at the smallest scale, and what to mutate
[ran] Two 4-point transforms on separate inputs: 14 from nothing, built as two DIFFERENT 7-gate shapes side by side; no 13.
So in count (G) the published kind of saving (several arrays served together) does not show at this size. Yes, and: the copies
that could share are not independent ones. Mutations worth one run each: (a) two transforms of the same four inputs with
different scalings (H and H*D: 8 outputs, 4 inputs), where every helper is shared; (b) the transform and the subset-sum matrix
of the same inputs; (c) H(x+y) and H(x-y) together, which is exactly the 8-point problem seen as "two copies on related data" —
its two halves are idea 3's two centres.

## 3. Drain profiles from the greedy run
`greedy.py`, count (G), exact replay of each result; one run per line. The profile lists the drain of each gate in order; after
the profile ends, every remaining gate drains 1 or 2. [ran]

| target | start P | size reached | drain of gates 1, 2, 3, ... |
|---|---|---|---|
| 4-point transform | 12 | **7** | 2, 3, 3, then 1, 1, 1, 1 |
| two 4-point transforms | 24 | **14** | 2, 3, 3, 2, 3, 3, then eight 1s |
| 8-point transform, run 2 | 56 | **23** | 4, 4, 4, 4, 5, 7, **8**, 4, 2, 1, 1, 1 (P = 16 after 8 gates) |
| 8-point transform, runs 1, 4, 3 | 56 | 25, 25, 27 | 4,4,4,4,4,4,4,7,2,2,2,2 / 4,4,4,4,4,6,4,5,2,2,2,2,1 / 4,4,4,4,4,4,5,5,2,2,2,1,... |
| cousin, entries 2^(Hamming distance), 8 points | 56 | 25 | 4, **6, 6**, 5, 4, 6, 7, then 1s (P = 18 after 7 gates) |
| subset-sum matrix, 8 points | 19 | 13 | 4, 2, 2, 2, then 1s |

What I see in it:
- **Steepest drain finds 7 and 14 with no search at all, and 23 at 8 points** (one gate from the best known, and better than
  the annealer's 24). In run 2 gate 7 is a full-drain gate: it completes a sign vector (-1,1,-1,-1,1,1,1,1) that is not an
  output, and gate 8 completes a second sign vector. P is 16 after 8 gates.
- The known 22-gate circuit is SLOWER at first: after its 8 pair gates P is still 24, and it reaches 16 only at gate 11.
  It wins in the endgame. So the count at 8 points is decided by the last 16 units of potential, where gates drain 1 or 2;
  greed about the centre costs one gate there. A search that keeps both (a fast centre AND by-products that serve the
  endgame) is the obvious next run.
- At 4 points the profile is 2, 3, 3: the second and third gates each help three of the four outputs. Greedy builds a
  ladder, not the balanced "sum of sums".
- **Anomaly: the cousin drains faster than the transform at the start** (6 and 6 against 4 and 4 for gates 2 and 3). At
  the transform's own point the early gates can help only half the outputs; away from it they can help three quarters.
  The transform makes up for it later (its centre gates drain 7 and 8). I do not know what this means.

## 4. Anomalies and pretty facts
- The squared error is two-valued: zero or above 1. No near misses in about 42,000 wirings. [ran]
- All 7-gate wirings found are isolated solutions with coefficients 1 and 2. [ran]
- The 42 seven-gate shapes at 4 points include ladders (a chain of signed partial sums with an output read off the middle),
  circuits where one OUTPUT is the centre for the others, and circuits with two centres. The balanced "sum, then subtract" is
  one shape among many. [ran]
- At 8 points the machine's first 24 from nothing is not the textbook: one centre built by a chain, a second centre one gate
  away, outputs hung on both (`j-machine/r2/steiner_H8_s11_empty.jsonl`). [ran]
- 22 at 8 points is 11 + 11 with no gate shared between the halves. [derived]
- E*E^T = (N/4)*I + rank 2, exactly, at 4, 16, 64 points. [ran]
- The transform's potential is N(N-1); the subset-sum matrix's is 3^k - 2^k; the free diagonal between Z and Z^T makes up the rest. [derived]
- The cousin with entries 2^(Hamming distance) ended where the transform did from nothing (25 and 26 against 23 to 28), but
  its early gates drain 6 where the transform's drain 4. [ran, weak]
- The steepest path is not the best path: it reaches P = 16 three gates sooner than the known circuit and finishes one gate worse. [ran]

## 5. Not done, and limits
- 16 points: not searched (my cap bug). The relaxation tool: not debugged. The hand counts 11, 15, 17, 21 are replayed exactly but are upper bounds only.
- Free relabellings and scalings of inputs and outputs are already inside count (G) (a relabelling is a rewiring, a scaling is
  absorbed by the next gate), so "equal to the transform after relabelling and scaling" is the same target. [derived]
- All searches are samples. Nothing here is a lower bound.

## 6. Files
`j-machine/slp.py` (wiring + Levenberg-Marquardt, exact replay), `relax.py`, `steiner.py` (the tool that worked), `greedy.py`,
`tower.py`, `hand17.py`, `look.py` (prints the best circuits); results `r1/` (slp), `r2/`, `r3/` (steiner), `r4/` (greedy), `t3/` (4-point shapes).
