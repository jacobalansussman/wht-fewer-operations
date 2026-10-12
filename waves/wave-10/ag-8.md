# ag-8 the-best-bad-circuit: at 4 points the transform has no circuit of its own one gate above the least (exhaustive modulo 13 and 17); it has a third of its class's shapes; the first circuit that is the transform's own (by a hand lemma, machine test two thirds done) is at 16 points, costs the textbook count, and its family cannot be cheaper

11 October 2026, 07:55 to about 08:50 EDT, 60-minute box, one agent, label `ag-8-bestbadcircuit`. Private: nothing published, no git,
no Lean, nothing reviewed. Marks: [ran] = run of mine tonight (files in `ag-8-bestbadcircuit/`); [ran, mod p] = exhaustive over the
whole numbers modulo p, which is evidence and not a proof over the rationals; [derived] = by hand tonight, checked by nobody;
[read] = from tonight's reports; [guess]. **Count (G) throughout**: a gate is any a*u + b*v, scalings free.

**FIRST LINES. No circuit below a known count and no growth law below N log N. Nothing here changes the order.**
The idea was: the records are identities of the whole class of 2 x 2 kernels, so look one or two gates above the least for circuits
that work for the transform only. Result: **at 4 points there are none** at 7 and 8 gates (exhaustive modulo 13 and 17) and none at
9 gates in a pool of small wires; the one specimen the idea started from is not special (the skeptic af-2 said so; replayed here).
The transform does not have MORE shapes than its class one gate above the least, it has FEWER: 464 against about 1,364.
The first circuit I can show to be the transform's own is at 16 points, has 64 gates (the textbook count) and belongs to a family
that provably cannot go below N log2 N. So "special" and "cheaper" have not met anywhere.

Words. N = 2^k points; an *address* is k bits. *Kernel*: a 2 x 2 matrix; K_tau = [[1,1],[1,tau]] (every kernel without a zero is this
one after scaling rows and columns [read p-0]); its k-th tensor power has entry tau^(number of common ones of the two addresses);
tau = -1 is the transform H. *Wiring*: which two wires each gate reads. *Shape*: a wiring with all names forgotten. *Renaming* (frame):
a choice of which input is which address and which output gate is which row. A wiring is *of the class* if for a general tau, in
some renaming, coefficients exist; *special* if it works at tau = -1 and in no renaming at a general tau. *Helper*: a wire that is not an
output. *Irredundant*: no helper can be left out. *Pairing*: a way to split 4 points into two pairs (there are three). *Butterfly*:
two gates u + v, u - v on the same two wires. *Tight wire*: a row of the transform cut down to a flat (a subspace of addresses or a
shifted copy). *Over-limit wire*: any other wire that several outputs read (the hub of the 7-gate circuit).

## 0. In ten lines

1. [ran] **Census of the records: none is special.** With the wiring fixed and tau general (two random tau modulo 2^61 - 1, then exact
   fractions at tau = 3, 5/7, -2): the 7, 20, 52, 128, 304 work with the names unchanged; the 19 works in 288 of the 10,752 renamings
   that keep H. Same verdicts as h-6, p-0, k-cross, with a different tool (`wsolve.py`).
2. [ran] **The 8-gate circuit of ae-cross (hybrid 1) is of the class**: 32 of the 576 renamings, exact at tau = 3 and 5/7. Rename the
   outputs by a shift: g1 = a + tau b, g2 = c + tau d, g3 = g1 + g2 (row 01), g4 = b + d, g5 = g3 + (1-tau) g4 (row 00),
   g6 = g3 + (tau-1) g2 (row 11), g7 = b - c, g8 = g3 + (1-tau) g7 (row 10) [derived, checked by hand]. af-2 found this first [read].
3. [ran, mod 13 and mod 17] **Every circuit of 8 gates for the 4-point transform, sorted by shape.** Irredundant helper sets: 33,691
   (mod 13), 43,003 (mod 17). Shapes: **464, the same 464 at both primes. Every one is a shape of the general kernel. Special: 0.**
4. [ran, mod p] **The class has about three times as many shapes**: 1,410 (tau = 6 and 11 mod 13), 1,370 and 1,364 (tau = 3 and 5
   mod 17); 1,364 at all of them; **900 of those have no irredundant circuit at the transform.** [ran, exact] What happens to them at
   tau = -1: in 321 a gate DIES (its coefficient is a multiple of 1 + tau and the circuit becomes a 7-gate one); in 519 the circuit
   survives but a helper has become unnecessary (or two wires coincide); in 41 a coefficient has a pole; 65 unclear. Section 3.
5. [ran] 9 gates at 4 points, helpers from the 32 wires with entries 0, +1, -1: 2,928 irredundant helper sets, all of the class.
6. [derived + ran] **Why 4 points cannot be special.** Through the transform pass |AGL(k,2)| / (2 k!) different one-parameter
   families of class matrices: **6, 112, 6,720 at 4, 8, 16 points.** A wiring is of the class when the matrices it can compute contain
   one of them. At 4 points a wiring of 8 gates computes a family of dimension up to 8 in a space of dimension 9. Section 4.
7. [derived; machine test 65 % done, no counter-example] **The first special circuit: 16 points, 64 gates.** A textbook network whose four inner 4-point blocks use all
   THREE pairings. With two pairings it is of the class (8 points: 1,536 of 10,752 renamings [ran]; 16 points: 16 of 204 renamings
   in a 1-in-400 slice [ran]); with three it cannot be, by a counting lemma. Machine test of the three-pairing network: section 5, line MIXFULL.
8. [derived] **It cannot be cheap.** That circuit is made of tight wires only, and a program of tight wires costs N log2 N (a-2's
   lemma, L3; a two-line version of the reason in section 5). Growth law of everything special found: rate 1.0 against the records' 3/4.
9. What H H = N is, seen from the class [derived]: the inner product of two rows of the class is 2^a (1 + tau)^d (1 + tau^2)^b with
   d their distance; **orthogonality is "1 + tau divides it d times".** Its linear shadow is the dying gate of line 4.
10. Better question (section 6): not "which wirings are special" but **"which class circuits lose gates at tau = -1, and how many"**,
    and for a special saving: **an over-limit wire that exists only at tau = -1**. At 4 points there is none (all 228 helper sets of
    7 gates and all sets of 8 are of the class).

## 1. The tools, and their controls

- `wsolve.py` [ran]. Fix a wiring; a wire is a point up to scale; a gate g = (u, v) says g lies in the span of u and v. Inputs and
  outputs are known points. Each wire carries a subspace known to contain it; the rules S_g <= S_u + S_v, S_u <= S_g + S_v,
  S_v <= S_g + S_u are iterated. A subspace that becomes 0 is a proof that no coefficients exist (for that tau, that renaming); all
  wires down to points with every gate a true gate is YES. Modulo 2^61 - 1 at random tau, and the same code in exact fractions.
  `solve_branch`: where the propagation stalls on a line, try every point of the line (small primes 31 and 37 only).
  Controls: tau = -1 with the names unchanged says YES for every record; the 19 gives 288 renamings, k-cross's and h-6's number
  (36 x 8) found independently.
- `cen2.py` + p-0's `mincirc_sets` [ran, mod p]. All sets of 4 helper points after which the four rows are made; keep the
  irredundant ones; list every acyclic wiring of each; shape = least, over the 24 renamings of the inputs, of the sorted list of
  (kind, expression of the node down to the inputs). A helper set of the transform is of the class if one of its wirings has a
  shape that occurs at the general tau. Controls: 126 and 228 helper sets at 7 gates (p-0's numbers); the pool search of line 5,
  which judges with `wsolve` instead of shape tables, agrees at 8 gates (2,179 sets, 42 shapes, all of the class).
- A first run on an 18 % sample of the generic sets called 4 helper sets special. With the full table they are of the class. Kept as
  `t_quick.out`; it is wrong and is the reason every number above is from complete runs.

## 2. The census at 4 points  [ran, mod p; `cen2_p13_t6.out`, `cen2_p13_t11.out`, `cen2_p17_t3.out`, `cen2_p17_t5.out`, `merge4.out`]

| | sets of 4 helpers | irredundant | wirings | shapes |
|---|---|---|---|---|
| transform, mod 13 | 81,475 | 33,691 | not counted | 464 |
| transform, mod 17 | 108,499 | 43,003 | not counted | 464 (the same) |
| tau = 6, 11 mod 13 | 45,486 | 21,446 | 59,746 | 1,410 |
| tau = 3 mod 17 | 58,758 | 25,974 | 70,994 | 1,370 |
| tau = 5 mod 17 | 58,710 | 25,926 | 70,946 | 1,364 |

Shapes present at tau = 11 mod 13 and at tau = 5 mod 17: 1,364. Shapes of the transform among them: 464 of 464. Helper sets of the
transform with no wiring of a generic shape: 0 of 33,691 and 0 of 43,003. The counts of sets grow with p because 8-gate circuits come
in one-parameter families; the number of shapes does not.
So at 7 gates the transform has "more placements of the same 27 shapes" [read p-0]; at 8 gates it has **a third of the shapes**.
Limits: modulo two primes; a rational circuit that degenerates modulo both 13 and 17 would be missed. 9 gates exhaustively was out of
reach (hours); the pool run of line 5 is exhaustive over its pool only (201,376 sets of 5 helpers).

## 3. Where the other 900 shapes go: the dying gate  [ran, exact fractions; `collapse.py`, `collapse.out`]

For each class shape absent at the transform I took its labelled specimen and solved the same wiring exactly at tau = -1 and at
tau = 3 (946 specimens of the run tau = 11 mod 13).

| at tau = 3 | at tau = -1 | shapes |
|---|---|---|
| exists | exists, every gate a true gate (so: redundant at the transform, or two wires coincide; not told apart) | 519 |
| exists | exists, **but a gate has become a copy of one of its operands** | 321 |
| exists | no coefficients (a pole at tau = -1) | 41 |
| no coefficients over the rationals at tau = 3 (the shape lives modulo p: a square root, or an accident) | no | 46 |
| propagation stalls | various | 19 |

Specimen of the second line: h4 = (c, d), h5 = (b, d), h6 = (a, h5), row 11 = (c, h6), h7 = (h4, row 11), row 00 = (b, h7),
row 01 = (d, h7), row 10 = (h5, row 11). At tau = -1 the wire h4 is c itself: one gate fewer, 7 gates.
Reading. The transform's "own" economy at this size is not a wiring of its own. It is a class wiring in which one coefficient is a
multiple of 1 + tau. At 4 points this buys nothing new, because the class reaches 7 by itself. p-0's weight-only data (4 gates
against 5, 7 against 8) and g-5's K3 (the zero entry 1 + tau) are the same event where it does buy a gate.

## 4. Why nothing is special at 4 points: the transform is a crossing of many class curves  [derived; counts match the runs]

The renamings that keep H up to signs: inputs x -> A x + b, outputs w -> A^-T w + c: 2^k |AGL(k,2)| of them (96; 10,752; 5,160,960).
The class curve tau -> K_tau^(x k) is kept, as a set, by 2^(k+1) k! of them (swap rows and columns of the kernel on all bits in step,
tau -> 1/tau; permute the bits): 16, 96, 768. So the number of different class curves through the transform is

    |AGL(k,2)| / (2 k!)  =  6, 112, 6,720   at 4, 8, 16 points      (it grows like 2^(k^2)).

The runs agree: a fixed circuit is of the class in a multiple of 16 (4 points) or 96 (8 points) renamings: 48 = 3 x 16 (the 7),
32 = 2 x 16 (hybrid 1), 288 = 3 x 96 (the 19), 1,536 = 16 x 96 (mixed textbook).
A wiring with G gates computes a family of matrices of dimension at most G, up to scalings; all matrices up to scalings have
dimension (N-1)^2 = 9, 49, 225. "Special" means: that family contains the transform and none of the 6 (112, 6,720) curves through it.
At 4 points G = 7 or 8 against 9: there is no room, and the census finds none. At 8 points 19 to 24 against 49: room, and still every
8-point circuit tested is of the class (the 19, the 20, the two mixed textbook networks here; h-6's 21). At 16 points: section 5.

## 5. The first special circuit, and why it is dear  [derived; machine check at the end]

What only the transform has, in one sentence: **any two of its rows agree on exactly half the points and differ on the other half**
(that is H H = N). For the class this is true only for rows at distance 1; at distance 2 one of the two halves survives; beyond,
nothing. So the transform can pair its rows in N - 1 directions, the class in k. At 4 points: three pairings against two.
Construction (`gen_mixed.py`, `mixed_4_0120.txt`, 64 gates, replays exactly as H): the textbook network at 16 points, in which the
four 4-point blocks (the two low address bits) pair their points as (0,1)(2,3), (0,2)(1,3), (0,3)(1,2), (0,1)(2,3).
Lemma [derived]. In such a network every output is a binary tree over all inputs, and a node of level j is read, further up, by
N / 2^j outputs. For a general tau those outputs must be proportional on the node's inputs. Level 1: 8 rows proportional on a pair of
addresses, and the other 8 on the same pair: only if the pair differs in one bit (at two bits the classes have sizes 4, 8, 4). Level
2: four classes of 4 rows: only if the four addresses are a square. Level 3: a cube. Then the two halves must cut their cubes into
squares the same way (the top gates join equal names), and inside a square only two pairings are edges. So a network that uses
three pairings is of no class, in any renaming, affine or not.
Controls [ran]: with two pairings the lemma allows it and the solver finds it: 8 points, pairings (0,1) and (0,2): 1,536 of 10,752
renamings; 16 points, pairings 0,0,1,1: of the class with the names unchanged.
MIXFULL [ran, `mixfull_0120_p0.out`, `_p1.out`, `_p0b.out`, `_p1b.out`; general tau modulo 2^61 - 1]: the renamings that keep H, reduced
by the network's own symmetries, number 80,640. **Tried: 52,800 (65 %). YES: 0. Undecided: 0. NOT COMPLETE** (the rented machine slowed
down; the matrices come in a fixed order, so the 35 % left are not a random remainder). For comparison the two-pairing network says YES
in 16 of 204 (8 %). So: special by the lemma, and no counter-example in two thirds of the affine renamings; the run does not prove it.
Why it is dear [derived; this is a-2's lemma L3 in the smallest case]. A tight wire on a pair {x, x + d} with sign e can only be read by
outputs whose row has value e on d: half of them, and each butterfly above it serves two of those. Counting at 8 points: 16 uses of
level-1 wires, at most 2 per wire, so 8 wires, so 24 gates. Mixing pairings changes which wires are used, never how many.
**Growth law of the special object: N log2 N exactly (64; 2,048 at 256 points), against the records' (3/4) N log2 N + N/4 (52; 1,600).**
A special 4-point circuit, if one exists at 9 gates or more outside my pool, composes to at least (9/8) N log2 N (72; 2,304).

## 6. What the idea turned into

"Yes, and" 1: special wirings do not exist near the least count at 4 points, so I asked where the transform's own shapes are. Answer:
it has none; it has fewer. "Yes, and" 2: then what do the missing shapes do at tau = -1? A third of them lose a gate. "Yes, and" 3:
where is the first wiring of the transform's own? Where three pairings can meet in one circuit: 16 points; and it is a tight network.
So the two halves of the idea separate:
- **special without an over-limit wire** = a network of butterflies in directions that no single frame makes coordinate. Exists from
  16 points on, in great number, always at N log2 N. Closed by L3.
- **special with an over-limit wire** = a hub that agrees with many rows on large parts and has no class frame. At 4 points the
  transform's four hubs are the class's two in other frames [read p-0]; at 16 points every quadratic bent sign pattern is a product
  of 4-point hubs in some frame [recalled: all quadratic bent functions in 4 variables are equivalent]; [guess] the first hub without a class
  frame is a bent pattern that is not quadratic, at 64 points. ad-5 measured that family: 304 again [read]. That is the one place where
  "special and cheaper" is not excluded by anything here, and one wave has already been there.
- **the dying gate** (section 3) is the mechanism by which the transform is cheaper than its class where it is (p-0's weight-only
  data, g-5's K3). On the full transform it is repaid: H_4 = K3 + 1 after a change of basis of 2 + 2 gates, 4 + 2 + 2 = 8 [derived].

Experiments, in order of value:
1. **dying-gates at 8 and 16 points.** Carry tau as a symbol through h-6's exact tools; for every class circuit known (the 19, 20,
   21, the two 52s) and every circuit the annealers produce for tau = 3, count the gates whose coefficient vanishes at tau = -1.
   A class family in which a fixed fraction of the gates dies at tau = -1 would be a growth law for the transform that its class does
   not have. The staircase has none (its coefficients are 1 - tau and powers of tau [read h-6]); nobody has looked for one.
2. **special at 8 points.** The tangent test: for a circuit of the transform compute the tangent space of its family and test the
   112 class directions (linear algebra, no search). Run it on g-1's 213 samples at 19 gates and on every 20 and 21. Either a special
   8-point circuit at 20 or 21, or "none in 49 dimensions with 112 curves", which would want a reason.
3. **a hub without a class frame at 64 points**, built on a cubic bent pattern and counted against 304; ad-5's tools.
4. MIXFULL to the end: the 27,840 renamings left (`mixfull.py mixed_4_0120.txt part 2 seconds start`; start indices 11468 for part 0
   and 14933 for part 1), and a second reading of the lemma of section 5 by someone else.

## 7. Criticism, last

- The census is modulo 13 and 17. "No special circuit of 8 gates" is a statement about circuits that survive reduction modulo both.
- "Of the class" is decided by shape tables at four generic (p, tau); the 464 shapes were not each replayed with tau as a symbol.
  The pool run (42 shapes at 8 gates, 43 at 9) used the solver instead and agrees.
- 46 "class" shapes have no rational circuit at tau = 3 in the labelling of their specimen. I did not find out whether they need a
  square root or are accidents of the prime. They do not touch the transform's 464.
- Section 4's dimension count is a count, not a proof that special wirings cannot exist at 4 points with 9 or more gates.
- Section 5's lemma is by hand. The machine test covers the renamings that keep H, reduced by the network's own symmetries (every
  output shift; input shifts inside a block), a reduction that is also by hand.
- The special object costs the textbook count. I found nothing special below N log2 N, and one lemma says this family never will be.
- I did not enumerate 8 points with 20 and 21 gates: no exhaustive tool reaches it (modulo 7 every tau is one of p-0's special values).
- Nothing here speaks for linear size. What it does is remove a hope ("the records miss the transform's own circuits") at the sizes
  one can enumerate, and name the two mechanisms left: a dying gate, and a hub without a class frame.

Files: `waves/wave-10/ag-8-bestbadcircuit/` : wsolve.py (the wiring solver), rec_id.out,
rec2.out (records), h1.txt, h1_frames.out (hybrid 1); cen2.py, merge.py, cen2_*.out, merge4.out (the 8-gate census; the input sets
and two 15 to 20 MB tables stayed on the rented machine under (the Linux machine's working folder)/ag-8-bestbadcircuit/, cen2_13_4_11.pkl is here);
collapse.py, collapse.out (section 3); pool9.py, pool9_m5b.out (9 gates; pool9_m5.out is the run before branching, mostly
undecided); gen_mixed.py, mixed_*.txt, mixtest.py, mixfull.py, mixfull_*.out (section 5); t_quick.out and census8.py (first attempts,
superseded).
