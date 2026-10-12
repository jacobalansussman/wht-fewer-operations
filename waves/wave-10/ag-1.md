# ag-1 halving-or-nothing: one halving never gives the right wire in the block at 14 or 15 gates; a halving is a line used downhill and weighs nothing in the determinant ledger

11 October 2026, wave 10, agent "ag-1-halvingornothing", 60-minute box (about 07:35 to 08:35 EDT). Private. One agent; nothing
reviewed, nothing in Lean, nothing published. Marks: [ran] = computed in this box, exact (whole numbers, or whole numbers
modulo 2, 4, 8, 16); [derived] = argued by hand in this box, checked by nobody; [read] = from a file I opened; [guess].
Gate count everywhere: **(G)**, a gate is any a*u + b*v, scalings free. Count (O), OpenAI's, is not used.
Folder F = `waves/wave-10/ag-1-halvingornothing/`.

**No circuit below a known count, no growth law below N log N, nothing of the 1e-1 kind. Nothing here changes the order.**
A circuit modulo 8 or 16 is not a circuit; the searches below are searches for an obstruction, and they found one each time.

Words. N = 2^k points. *The block* B: at 16 points, the 8 x 8 half of the neighbour-sum matrix (every address gets the sum of
the inputs at its 4 neighbours), from even-weight inputs to odd-weight outputs (`rows_B4.txt`, rebuilt by `mkB.py`).
*Primitive* vector: whole numbers with no common factor; every wire is scaled to be primitive. *Residue* of a wire: the wire
modulo 2. *Halving*: a gate (a*u + b*v)/2^e, a and b odd, e >= 1; possible only when u and v have the same residue; e is its
*depth*. *Line*: over the rationals a gate puts a new point on the line through two points (wires up to scaling), so a gate
is three points on a line and a choice of which one is made from the other two. *Shadow*: a circuit read modulo 2.
*Real gate*: a gate whose residue is new and is the sum of two earlier residues. *Wasted gate*: one whose residue repeats.
*Flat*: a wire all of whose entries are 0, +1 or -1.

## 0. In ten lines

1. [ran, exhaustive modulo 2] With ONE form given free, the block costs 12 real gates for 14 of the 255 forms (the 8
   targets themselves, and the 6 sums of two antipodal pairs of inputs), 13 for 160 more, 14 or more for the other 81.
   So the shadow the brief asked for exists in plenty: 16 helper sets for a 14-gate circuit and 8,695 for a 15-gate one.
2. [ran] **None of them lifts.** With wires modulo 8 before the halving and modulo 4 after (a halving by exactly 2): 0 of
   16 sets at 14 gates, 0 of 8,695 at 15 gates, and 0 of the 16 with one more gate of any kind. About 3.6e9 halvings were
   examined; **not one produces the residue the shadow needs.** Wires modulo 16 (halving by 2 or 4): 0 of 16 and 0 of
   2,038; of the last family (6,657 sets) only the first 500 were run, 0 lift (section 2).
3. [ran + derived] At 14 gates the reason is exact and holds for every depth: in those shadows every three wires that are
   on a line modulo 2 are a gate and its two operands, and a halving on such a triple gives a point of the same line, which
   an ordinary gate gives too (line lemma, section 1). **The block has no 14-gate circuit with one halving, of any depth.**
4. [ran] At 15 gates halvings on "accidental" triples do occur (about 1.04 million examined) and 178,080 of them make a
   residue no wire has yet. They are real; none is the right one.
5. [derived] What a halving is: three points u, v, h on a line with v = u + 2h; without halvings the line may be used to
   make u or v, with a halving to make h. **A halving is a line used downhill.** It can save a gate only if two wires that
   agree modulo 2 were both cheap for reasons that have nothing to do with each other.
6. [derived, small cases ran] The determinant ledger (Morgenstern's argument with every wire primitive): each gate
   (a*u + b*v)/c raises the largest minor by at most (|a| + |b|)/c. A gate u +- v is worth 1 unit, u +- 2v is worth 1.585,
   **a halving (u +- v)/2 is worth 0.** The transform needs (N/2) log2 N units. So the brief's hope is the wrong way round:
   a halving carries no depth; in an in-place program it hands depth back and must be repaid.
7. [derived + ran at 3, 4 and 5 inputs] **Flat class.** Between flat wires the only gates are u +- v, u +- 2v and
   (u +- v)/2. Every record of the night is flat [read: ad-7]. Hence any flat circuit for the transform, with any number
   of halvings, has at least (N/2) log2 N / log2 3 = 0.3155 N log2 N gates that are not halvings. The order cannot change
   inside the flat class; the 3/4 family is within a factor 2.38 of that floor. [ran] At 4 points the least total weight
   of a flat circuit, halvings free, is exactly 8 = N log2 N, twice what the determinant asks.
8. [ran] 8 points: around the 19-gate circuit, add any one of the 300 halves of its 78 pairs of agreeing wires and remove
   any two helpers: 16,500 states, no circuit with 18 gates; add one and remove one: 0 of 3,300 compute the transform.
   The full class "18 gates, one halving" was NOT searched. [read] g-1's pool searches already allowed halvings.
9. Growth law: none. Units of depth per halving: 0 in the ledger of line 6 at every size; -e for a halving by 2^e in an
   in-place program [derived].
10. Halvings join the things that tie, with sizes: block at 14 (every depth) and 15 (depth 1, complete; depth 2, partly);
    transform at 8 points in one exchange radius. What remains of ae-cross's "no wall covers" is the deep coefficient.

## 1. What a halving is  [derived]

Take wires as points (primitive vectors up to sign). A gate is a line with three marked points. Reduce modulo 2: a line
through two points with different residues keeps its three residues p, q, p + q, and every gate on it is of kind (i) or
(ii) of ad-7. If two of its points have the SAME residue, write them u and v = u + 2h. Then the points of that line are of
two sorts: those with u's residue (odd multiples of u plus even multiples of h) and the rest (residue of h, or of u + h).
One gate without halving, from u and v, reaches only the first sort. So:

**A halving is the use of a line u, v = u + 2h, h in the direction "from u and v to h".** The same three points used the
other way (v from u and h) are a gate u + 2h of ad-7's kind (ii). Every gate u +- 2v of the records is a line of this sort
used uphill: y5 = -y3 + 2 g5 in the 19-gate circuit is the line {y3, y5, g5}; the halving would be g5 = (y3 + y5)/2.

**Line lemma.** Let V = alpha p + beta q (alpha, beta odd) and let u be a third wire with the residue of p + q. If u lies on
the rational line through p and q (in particular if u is the gate on p and q, or p is the gate on u and q), then every
halving (u - s V)/2^e lies on that line too, and it is an ordinary gate on p and q (their residues differ, so no content is
even). The wire V was not needed. Likewise if V = u + 2^f z, the half is a combination of u and z: one ordinary gate
(or, if u and z already agree modulo 2, a halving of that earlier pair).
So a halving that cannot be replaced at no cost needs an **accidental triple**: three wires on a line modulo 2 and not on a
line over the rationals (or three wires with one residue). That is the answer to the brief's "where can two wires agree
modulo 2 for free": where a residue has two unrelated derivations.

**Single line.** For three targets u, v, h on one line and nothing else, halving never wins: wherever u and v are
proportional on a set of coordinates, h is proportional to them there or vanishes, so any sharing between the circuits of u
and v is available to u and h; make h and u, then v = u + 2h. Every specimen I tried to build by hand for experiment 6(b)
(a matrix where one halving beats every circuit without) died of this: the relation that defines the half can be solved for
another of its wires at the same cost (five attempts on paper, 3 to 6 inputs, all tie; nothing run; not a proof that no
specimen exists).

## 2. The first experiment: the block  [ran]

Tools in F. `enumfree.c`: forms modulo 2 on 8 inputs, the 8 rows of B as targets, one form w given free; lists every set of
m helper forms that reaches all targets (same search as ad-2's `free8.c` and ad-7's `enum2.c`). `lifth.c`: for a helper set
and its w, searches every order and every lift with wires modulo 2^P; every helper and target residue gets one wire, made
by a gate a + c*b with c odd; one pair of gates is made together, the wasted gate V = p + c*q (residue of a third wire u)
and the halving H = (u - s*V)/2^e, 1 <= e <= P - 2, which must have the residue w; targets must be odd multiples of the
rows. Option "extra": one more wire of any residue by any gate a + c*b, usable everywhere, V may then also be
p + (even)*q on a second wire with u's residue, and a target may be an even correction of a wire with its residue.

Controls. (a) `enumfree` with no free form and 14 gates: 0 records (35 s), as ab-0 and ad-7 found. (b) `lifth` on a
hand-made 11-gate circuit whose second target can only be reached through a halving (`ctl_rows.txt`): found, with the
halving shown; same input with the wrong residue declared, or with one needed helper left out: no lift; helper left out but
"extra" on: found again, through a wasted gate of the second kind. (c) ad-7's result is the case "no halving" and is used,
not re-run: no circuit with 15 gates modulo 4 [read].

The 255 forms fall in 15 classes under the block's 192 symmetries (`w_orbits.txt`); one representative each:

| free form w (code; number of forms; weight) | least real gates with w free | helper sets |
|---|---|---|
| a target row (23; 8; 4) | **12** | 12 sets of 5; 6,657 sets of 6 |
| two antipodal pairs of inputs (60; 6; 4) | **12** | 4 sets of 4; 1,952 sets of 5 |
| 7 (32; 3), 25 (24; 3), 27 (48; 4), 31 (32; 5), 61 (24; 5) | 13 | 12, 8, 46, 12, 8 sets of 5 |
| 3, 15, 24, 63, 126, 127, 255 (73 forms) | 14 or more | none at 13 |
| an input (8 forms) | not run: the half would repeat a residue, so all 15 real gates are still needed | |

A circuit with G gates and one halving has, modulo 2: the halving (a free form), at least one wasted gate, and real gates.
So 14 gates = 12 real + wasted + halving (no room left), and 15 gates = 13 real + wasted + halving, or 12 real + these two
+ one more gate of any kind. All three shapes were lifted:

| class | sets | wires modulo 8 (halving by 2) | wires modulo 16 (halving by 2 or 4) |
|---|---|---|---|
| 14 gates | 4 + 12 | 0 lift; 1.0e6 halvings examined, 0 with residue w, 0 on an accidental triple | 0 lift |
| 15 gates, 13 real, w in a 13-class | 86 | 0 lift; 5.6e6 examined, 0 with residue w | 0 lift |
| 15 gates, 13 real, w = two antipodal pairs | 1,952 | 0 lift; 3.0e8 examined, 0 with residue w | 0 lift; 3.2e10 examined, 0 with residue w |
| 15 gates, 13 real, w = a target | 6,657 | 0 lift; 1.2e9 examined, 0 with residue w | PARTLY RUN: at least 500 of the 6,657 sets (the first 300 of the first half of the list and the first 200 of the second half), 0 lift, 0 with residue w; then the time limit |
| 15 gates, 12 real + one more gate of any kind | 4 + 12 | 0 lift; 2.1e9 examined, 0 with residue w | ONE of the 16 sets run to the end (w = two antipodal pairs, helper set 5 18 72 160): 0 lift, 10.7 million nodes, 1.8e10 examined, 0 with residue w; the other 15 not run |

The most targets any partial lift reaches is 4 of 8 (2 or 3 for some sets): without the free form the shadow stalls early,
and the halving never supplies it.

**What is proved by this, and for which class.**
- [ran + derived] **14 gates, one halving, every depth: none.** The count of accidental triples in the 16 sets is 0 over
  every order and lift visited, so by the line lemma any halving there, of any depth, is an ordinary gate; that leaves a
  circuit without halving with at most 14 gates, and there is none even modulo 2.
- [ran] **15 gates, exactly one halving, by 2 and not by 4: none**, in every shadow (the table's middle column is complete:
  every helper set of the three shapes, every order, every choice of odd coefficients modulo 8).
- [ran] 15 gates, one halving by 4: none in 2,538 of the 8,695 tight sets and in 1 of the 16 sets with one more gate; the
  rest not run.
- Not covered: a halving by 8 or more at 15 gates; two or more halvings; all of this is 2-adic, so odd denominators are
  included (they are invisible at the prime 2).
With ad-7 (no 15-gate circuit without halving): **a rational circuit for the block with 15 gates, if there is one,
contains a halving by 4 or more, or at least two halvings.**

**Looking at the failure.** At 15 gates the search does meet accidental triples: 3,498 halvings on them in the 86 sets and
1,036,032 in the 1,952 sets, of which 672 and 177,408 give a residue that no wire has yet (`lifth_acc.c`). So a halving
does create new residues there. What it creates is a wire supported where the two operands disagree (for flat wires u and
v, (u - v)/2 lives where they differ and (u + v)/2 where they agree: a halving cuts a support in two with a second wire as
the mask). The forms the block wants free are a whole target row or the sum over a plane of inputs; the wires present
before the halving are inputs, pair sums and the few targets reachable without w, and no two of them agree modulo 2 with
the right difference.

Rented machine, modulo 16, the 6,657 sets with w = a target, two halves of the list (`t23part_aa`, `t23part_ab`), 1,150
seconds each at nice 19: the progress lines in `r_aa.out` and `r_ab.out` stop at 300 and 200 sets done, no lift, no
halving with the residue w. The machine was loaded (about 4.5 seconds per set); the whole list needs about 8 hours there.

## 3. The transform at 8 points  [ran, a neighbourhood only]

All 8 outputs have the all-ones residue, so here wires agree modulo 2 everywhere: in the 19-gate circuit of g-1, 13 wires
(g7 to g11 and the outputs) share it. `h8_halves.py`, exact whole numbers:
- 78 pairs of agreeing wires; their halves (u - s*v)/2^e with s = +-1, +-3: 12 are wires of the circuit already (each is a
  gate u +- 2v read downhill), 300 are new, and 59 of the 300 are also one ordinary gate from the circuit's wires.
- Controls: the circuit replays (19 gates); removing one or two helpers and adding nothing never works (0 of 11, 0 of 55).
- **Add one new half, remove two helpers (18 gates): 0 of 16,500 states.** Add one, remove one (19 gates with the half in
  use): 0 of 3,300. The 19-gate circuit cannot trade a helper for a half, not even at equal count.
Class covered: exchange radius "one half in, two helpers out" around one circuit. Not covered: every other 18-gate wiring.
The brief's design (shadow first) gives nothing at 8 points: the transform's shadow is the all-ones matrix, 7 real gates,
and every other gate is a repeat, so the shadow does not narrow the lift; the full class is a search over 10 helpers among
millions of vectors modulo 8. [read] g-1's annealer and exchange searches used every collinear triple of its pool of 304
flat wires in every direction, so halvings inside the pool were always allowed there; none of its 19-gate results has one.

## 4. The ledger: what a halving weighs  [derived; gate list ran]

Morgenstern's argument, with scalings fixed by "every wire primitive". Let D be the largest absolute value of a square
minor of the matrix whose rows are the wires made so far. D = 1 for the inputs. A new wire w = (a*u + b*v)/c (a, b coprime
whole numbers, c the common factor removed) changes any minor through w into (a/c)(the minor with u) + (b/c)(the minor with
v), so D grows by at most the factor (|a| + |b|)/c, and never shrinks. The 8 or N outputs form a minor of size N^(N/2).
**Sum over gates of max(0, log2((|a| + |b|)/c)) >= (N/2) log2 N.** [ran, `ledger_check.py`: 2,400 random gates on 4 inputs,
222 of them with an even common factor, largest minor recomputed after each: no violation; the only halvings after which
the largest minor grew are those with |a| + |b| > c, such as (3u - v)/2.] Weights: u +- v: 1; u +- 2v: 1.585; u +- 2^e v: about e;
a halving (u +- v)/2^e: 0; a division by an odd common factor: 0 as well. The 19-gate circuit spends 26.02 for a need of 12
[ran]; the 3/4 family spends about 1.04 N log2 N for a need of 0.5 N log2 N; the textbook spends N log2 N. Every known
circuit pays about twice the determinant.

In-place form (each step overwrites one of N cells, x_i <- a x_i + b x_j): the determinant is the product of the factors a,
so the 2-adic size of the a's adds up to exactly (N/2) log2 N. A halving is a = 1/2: one unit handed back, to be repaid.

**The factor two, at 4 points** [ran, `minweight4.py`, exhaustive over the 40 flat wires, halvings free and applied as soon
as they are possible]: no flat circuit for the 4-point transform has total weight below 8 (3,670 states with the limit
7.999; with the limit 8 the search returns the textbook, eight gates u +- v). So with halvings free the least weight is
exactly N log2 N = twice the determinant. Why halvings do not help there [derived]: a flat half has a smaller support than
its operands, so no output is a half; and the two halves of two outputs are the two pair sums that give back the same
two outputs.

**Flat class.** If u, v and (a*u + b*v)/c are all flat and u, v are not proportional, the gate is u +- v, u +- 2v (when the
support of v is inside that of u) or the halving (u +- v)/2 (exactly when u and v have the same support, that is the same
residue) [derived; enumerated at 3, 4 and 5 inputs, `flatgates.py`: 66 + 36 + 18, 540 + 232 + 116 and 4,020 + 1,320 + 660
gates of the three kinds, no other kind].
So in a flat circuit every gate weighs at most log2 3 and the halvings weigh 0:
**flat circuits for the transform have at least 0.3155 N log2 N gates besides their halvings**, however many halvings.
ad-7's census says every record is flat and uses 1 and 2 only; this says the two facts are one, and that the order cannot
move while wires stay flat. A linear program needs an average weight of (log2 N)/(2c) per gate for cN gates: entries (after
removing common factors) that grow like a power of N on most wires. A halving does not supply that; a deep coefficient does.
Note that a gate u + 4v never makes an output from a flat u: the output's entries are +-1, so u would need entries +-3.

## 5. "Yes, and", three times

1. *The shadow has hits and no lift: what is the failure made of?* The half must have one prescribed residue and never has
   it. Go around: ask which residues a halving CAN make (section 2: supports cut by a mask) and where masks are plentiful.
   That is the transform, where every output is a mask for every other. Done in section 3: plentiful, and useless near 19.
2. *A halving is a line read downhill: turn the question into "which lines must be read downhill".* A circuit is a set of
   points and lines with an order. A halving saves a gate exactly if some smallest point set can be ordered only by reading
   a line u, u + 2h, h towards h. On one line this never happens (section 1). It needs two lines through u and two through
   v that make both cheap while h is two gates from everything. The specimen for 6(b) is a small incidence figure, not a
   matrix family; I did not find it and each hand attempt was undone by re-rooting the relation.
3. *If a halving carries no depth, what does?* Section 4: only (|a| + |b|)/c > 2, that is a coefficient 2^e or a large odd
   one. So of ae-cross's two uncovered gates, one (the halving) is a combinatorial device at best and the other is the only
   carrier of the missing factor log N. The useful form of the question: a wire with entries of size about 2^e that is ONE
   gate from flat wires and from which several outputs are one gate each. u + 4v = output forces u non-flat (entries +-3):
   overshoot and come back.

## 6. Mutations

1. **overshoot-wires** (the part of experiment 6 that can carry depth). At 8 points, exhaustive over wires with entries in
   {0, +-1, +-2, +-3}: which non-flat wires are one gate from two flat wires AND one gate (u +- 4v or (u +- v)/2) from an
   output? Count how many outputs one such wire serves. A wire serving r outputs with weight-2 gates is the first object
   that pays more than one unit per gate.
2. **the figure for 6(b)**: search directly for the incidence figure of yes-and 2 at 4 or 5 inputs: point sets of at most
   9 points over the whole numbers modulo 8 whose only orderings read a line downhill, compared with the least halving-free
   count of the same targets (`lifth.c` with the wasted gate optional does the second half).
3. **finish the block at 15**: wires modulo 32 and 64 (the packing in `lifth.c` holds 4 bits per entry and must be widened),
   and two halvings (shadow: two free forms, 11 or 12 real gates; `enumfree` needs a second free form).
4. **the factor two in the ledger**: every known circuit spends twice the determinant: 8 (textbook) and 9.34 (7 gates) at 4
   points for a need of 4; 24 (textbook), 26.02 (19 gates), 27.02 (20 gates) at 8 points for a need of 12; the textbook is
   exactly twice at every size. Is "sum of weights >= N log2 N" a theorem for flat circuits? If so the flat floor doubles
   to 0.63 N log2 N, the 3/4 family is within 19 % of it, and with N - 1 real gates forced it reads 7, 18, 46 at 4, 8, 16
   points (7 is the known least; the records are 19 and 52). [guess beyond 4 points.] **At 4 points it is true** [ran,
   section 4]. Next: the same least-weight search at 8 points (3,280 flat wires, limit just below 24; needs C).
   A halving has weight 0, so it is the natural counterexample to look for first.
5. **18 at 8 points without halving first**: ad-7's second mutation (lift x-1's circuits modulo 4) decides whether 18
   exists in the class without halvings; only then is "a halving gives 18" a comparison.

## 7. Criticism, last

- Everything in section 2 is a search for lifts of shadows; its completeness rests on my reading of which shadows a
  one-halving circuit can have (three shapes) and on the elimination of a wasted gate of the second kind in the tight
  shapes. I checked that argument by hand only. The controls show the lifter finds a halving when one is needed, not that
  it never misses one.
- The symmetry reduction to 15 representatives of w is mine (192 symmetries, checked to permute the rows); ad-7 used the
  same group for the first gate.
- "Every depth" at 14 gates uses the count "0 accidental triples", which is conservative (a wire's recorded gate is the
  first found), and the line lemma.
- Depth 2 at 15 gates is incomplete, deeper halvings and two halvings are untouched. "One halving never saves a gate in
  the block" is established only for a halving by 2.
- Section 3 is one exchange radius around one circuit. It says nothing about 18 in general.
- Section 4's inequality is Morgenstern's with a choice of scaling; I recalled the theorem and re-derived the two-line
  argument, I did not open a source; the check on random circuits is at 4 inputs. The flat-gate list is derived and
  enumerated only at 3, 4 and 5 inputs (with |a|, |b| up to 4 in the enumeration).
- "Every record is flat" is ad-7's census [read], not re-run here.
- I ran one 64-second timing trial of `lifth` outside the slot runner by mistake.
- Nothing here changes the order, or any constant.

Files in F: `mkB.py`, `rows_B4.txt`, `w_orbits.txt`; `enumfree.c`, `enum_m5.out`, `enum_m6_T.out`, `sets_m5.txt`,
`sets_T23.txt`, `tight14_*.txt`, `tight15_*.txt`; `lifth.c` (final), `lifth_v1` (binary of the first version, used for the
runs without "extra"), `lifth_acc.c` (counts accidental triples), `lift_*_P3.out`, `lift_*_P4.out`, `liftx_*` (with one
extra gate), `ctl_rows.txt` (control); `h8_halves.py`, `h8_halves.out`; `flatgates.py`; `ledger_check.py`; `minweight4.py`; `r_aa.out`, `r_ab.out` (rented
machine).
`flatgates.py`, `ledger_check.py` and `minweight4.py` print to the terminal (a few seconds each; arguments 3, 4, 5; none;
7999 or 8000); their outputs are quoted in sections 4 and 6 and were not saved. `liftx_w60_P4_set1.out` and `_set3.out` are
not results (no free slot; stopped by me).
