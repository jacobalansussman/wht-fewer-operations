# Fourth wave of ideas: what came out (wht39)

11 October 2026, about 01:45. Private. Nothing here is reviewed by a person or in Lean.
Marks: **[computed]** exact run tonight; **[argued]** by hand tonight, unchecked unless I say so; **[guessed]**; **[read]** from a paper or a report. "Mine" means I re-ran it for this note (`m-note/check.py`).

**What this wave was.** Nine agents each developed one idea (`h-0` to `h-8`), one recombined all four waves (`m-cross`), three critics came last (`n-0`, `n-1`, `n-2`). Earlier notes: `NOTE.md`, `WAVE2-NOTE.md`, `WAVE3-NOTE.md`. The fifth wave (`p-*`, `q-cross`) has landed and is not covered here.

**Words.** N = 2^k points, so an address has k bits. The *textbook* computes the transform H·x in N·log2 N gates. Count **(G)**: a gate is any a·u + b·v, scalings free. Count **(O)**: OpenAI's, each addition and each multiplication by a constant costs one. A *wire* is a value the program holds. Its *spread* is (its non-zeros written in the inputs) × (its non-zeros written in the outputs), never below N. A wire is *tight* when the spread equals N and *over the limit* when it is larger. A wire *mixes* an address bit when it is not (a two-point vector on that bit) × (a wire on the other bits). The *brick* is the 7-gate program for 4 points, *the 19* the 19-gate program for 8 points, the *staircase* the second wave's family (7, 20, 52, 128, 304 gates).

## 1. What came out, in ten lines

1. **Nothing beats the textbook in order.** No saving of the 1e-1 kind, no linear size [read: all nine reports]. One better constant in OpenAI's count; the rest is walls that are now exact statements.
2. **The constant, count (O).** H·x exactly in (5/6)·N·log2 N + N operations when 3 divides k: 4,352 against 4,608 at 512 points [computed by `h-3`, and again by the critic with his own programs]. It is the 19 used on three address bits at a time: 20 operations where the published 8-point circuit of Alman and Rao (STOC 2023; their count is (23/24)·N·log2 N) has 23 [read by the critic, who found no later constant in a short search]. It needs an outside replay before it is said aloud.
3. **One correction.** The reported "56 operations at 16 points, below the list's 60" compares two outputs, H·x/2 and H·x/4. The 60 stands [computed by the critic].
4. **One gate per wire, exactly.** On every record, gates + over-limit wires = N·log2 N: 1 such wire in the brick, 5 in the 19, 4 in the 20, 12 in the staircase's 52 [computed: `h-0`, `m-cross`; mine for the brick and the 19].
5. **One skeleton.** Read modulo 2, all 18 circuit files that could be replayed have the same shape (section 2) [computed, `m-cross`]. Its count, N − 1 + (N/2)·log2 N, is 2, 7, 19 at 2, 4, 8 points: the two exact minima and the record. Then 47, 111, 255, where the records are 52, 128, 304. That it is a floor is [guessed], and by section 3 it cannot hold for all circuits at all sizes.
6. **"Pay once" is now a lemma for a class** (L9, section 5) [argued by `h-8`; the critic read it and it stands, with one gap].
7. **Narrow wires cannot change the order** (L10) [argued by `h-5`; no violation on the critic's 8.6 million test gates].
8. **No saving is special to the transform.** The staircase exists for every invertible 2 × 2 matrix without a zero in place of [[1,1],[1,−1]]; the 19 too, after renaming the inputs [computed, `h-6`].
9. **The 1e-1 case in the batch game is closed for 4, 5 and 6 arrays**, in one restricted game, and open beyond [computed + argued, section 3].
10. **The published program, read as a circuit, has no wire that pays for two gates either.** It wins by nesting [computed + argued, section 3].

## 2. Can one over-limit wire save more than one gate?

If each over-limit wire saves at most one gate, the best possible count is (1/2)·N·log2 N [argued, second wave]. Linear size needs wires that pay for many.

**Answer at 8 and 16 points: none was found.** Among circuits where no gate reads two over-limit wires, none can exist [argued, L9]. The exact minimum at 8 points is still open, between 15 and 19.

| what was searched | points | how complete | result |
|---|---|---|---|
| 304 wires with entries 0, +1, −1: all circuits near the 19 and the 20, plus a random local search (`h-0`) | 8 | local | gates + over-limit wires is never below 24, at any gate count from 19 to 24, in about 3 million states [computed] |
| every non-tight wire whose partners are tight, any coefficients (`h-0`) | 8, 16 | exact | it is one gate away from at most 4 outputs [computed] |
| wires that mix at most two bits, entries 0, +1, −1 (`h-5`) | 8 | exhaustive in that pool | nothing with 17 gates or fewer; 20 reached; 18 and 19 undecided [computed; the 17 rests on one program version] |
| random local search started at the records (`h-1`) | 8, 16 | local | no 18, no 51; a second 52 of another shape, with 16 over-limit wires for 12 gates saved [computed] |

**The skeleton modulo 2** [computed, `m-cross`; mine for the textbook, the brick and the 19]. Scale each wire to whole numbers that are not all even, and keep only odd or even: that is the wire's *class*. In all 18 files the classes form one *merge tree*: N − 1 gates each join two disjoint sets of inputs, and every other gate lands on a class already held. Call those gates *dead*. So gates = N − 1 + dead. The textbook has N·log2 N − N + 1 dead gates; the brick and the 19 have exactly (N/2)·log2 N. On the records each over-limit wire removes one dead gate. No circuit of the night has a gate that divides a difference by 2 (a *difference-quotient* gate). A caution: the searches drew on wires with entries 0, +1, −1 and started from known circuits, so the skeleton may be inherited from them [guessed by `m-cross`].

**Where the arguments stop.** At the first gate that reads two over-limit wires [argued, `h-8`]. The 19 contains such gates and is still one for one [computed].

## 3. The 1e-1 case, and the published unit read as a circuit

**The game.** The engine repeats one small program, the *unit*, on a batch of *arrays* (working copies of the data). Each array must be transformed along m directions (m is the *block size*); one direction on one array is a *move*. In *old letters*, mixing whole arrays is free, moves are paid, and there are no *address maps* (relabellings of the addresses inside a block). Four arrays at block size 5 cost 20 moves plainly; 17 would be a saving of 1.0e-1.

**Result: 17, 18 and 19 are excluded** [computed + argued, `h-2`]. All 70 ways (up to symmetry) to place at most 19 moves that pass a counting test are listed, and two hand lemmas exclude every one. The critic rebuilt the list and both lemmas with his own programs: the same 70. He went further: 5 arrays need at least 24 of 25 moves (saving at most 2.5e-2), 6 arrays at least 26 of 30 (at most 8.9e-2) [computed]. All of it rests on a model of the game from the second wave that nobody has audited.

**What it does not close.** Seven arrays are undecided. The lemmas only bite when the counting test holds with equality; they say nothing about 19 arrays in 80 moves, which would be 1.07e-1 [argued]. Old letters can never be linear: counting alone forces 3.75 moves per array at block size 5, an exponent of at least 0.82 [argued]. The published units use address maps, which this game leaves out.

**The published unit as a circuit** (`h-7`).
- Every wire is (a mixture over the batch) × (a tight wire on the address) [read + argued].
- One level saves 120 moves and makes at least 28,135 moves on mixtures: 0.0043 gates saved per over-limit wire [computed]. The small circuits get 1.
- It beats "one gate per wire" only by nesting: each level multiplies the cost by (1 − 2.11e-3), and the rule can first fail after about 328 nested levels, near 2^1152 address bits [argued, rough]. So the rule is not a law, yet it holds at every size one can search. There is no toy version: in count (G) the unit first goes below the textbook for arrays of 2^7,290 points [argued].
- Its centre is a 120 × 120 matrix built on the 120 lines through the roots of E8, a very symmetric arrangement in 8 dimensions [computed]. Read modulo 2, all its rows overlap without nesting: 7,140 of 7,140 pairs [computed by `m-cross` from a rebuilt matrix, not from the published file]. No circuit for it can be one merge tree modulo 2. It is the one object of the night outside the skeleton.

**A conflict to resolve.** `h-8` argues that this reading and a counting argument of the second wave cannot both be complete: together they would demand more moves than the unit has once arrays are large [argued]. This is a conflict between two of the night's reports, not a doubt about the release, which Lean checks. Experiment 1 measures it.

## 4. The ideas that are alive

**A. Which hypothesis must a better circuit break?** The skeleton has three: one merge tree modulo 2; no difference-quotient gate; dead gates that repeat an earlier wire modulo 2 but not modulo 4. The published program must break at least one [argued, given the guessed count of line 5]. *Next:* experiments 1, 2, 3.

**B. Two merge trees at once.** Nobody has built a circuit whose classes overlap. Inside one tree, joining the N outputs costs N/2 gates per address bit. With two trees in different bit orders the same count is about 1.5·N, if a partner need not agree in sign with the wire it corrects [argued, sketch]. That "if" is the rule `h-6` kept hitting. *Next:* 4.

**C. A difference-quotient gate that pays.** Quotients of two finished outputs only give back what was paid [computed: 28 of 28 at 8 points, 120 of 120 at 16]. One that pays must start from wires with entries of two sizes [argued]; wires with entries 1 and 3 turned up unasked in two searches. *Next:* 5.

**D. Composition.** A *tensor product* runs one circuit on some address bits and another on the rest; it adds the excess of both (L11). The staircase composes two bricks more cheaply: 5 above the count of line 5 at 16 points, where the tensor product gives 9 [computed; the 9 is from L11]. In the published unit, excess adds while saving multiplies. *Next:* 7.

**E. The transform one binary digit at a time.** A whole-number matrix that agrees with H modulo 4 costs under 4·N gates at 8 to 256 points [computed, replayed; it is not H]. In ordinary distance H cannot be approximated at all; digit by digit it stays simple until about k/2 digits [computed at 8 to 32 points]. *Next:* 8.

**F. Subset sums** (for every set S, the sum of the data over the subsets of S; the transform is two calls of it). `h-4` names the first gate its counting argument cannot handle, the *triangle*: three wires, each mixing a different pair of bits. At 8 points it loses by one gate, 13 against 12 [computed; modulo 3 only]. A lead for that field: an exact circuit below the usual count must divide a difference by 2, or beat the best circuit over the two-element field [argued, three lines]. *Next:* 6.

## 5. The walls, as lemmas

All [argued] unless marked; small cases [computed]. L1 to L8 keep their numbers from `WAVE3-NOTE.md`.

- **L1. Half and half.** A change of basis costs half a transform going in and half coming out. `d-0`, `d-3`, `d-4`, `d-7`, `g-0`, `g-2`, `g-5`, `g-7`.
- **L2. Copies do not share.** `d-2`, `d-6`, `e-3`, `e-6`, `e-7`, `e2-1`, `e2-2`, `j-manyatonce`, `g-5`, `g-6`, `g-7`; now `h-2`, `n-2`. The published unit is the one known exception: 120 moves saved in 56,835.
- **L3. Tight wires.** If every wire is tight, or a product of one two-point vector per bit, the program needs N·log2 N gates. `a-2`, `e-0`, `e-1`, `e-2`, `e-4`, `e2-1`, `e2-3`, `g-1`. Sharpened into L9.
- **L4. Volume.** Small coefficients grow a determinant slowly. `d-5`, `e-5`, `e2-0`, `j-failproof`, `g-1`, `g-3`, `g-4`, `g-5`; now `h-1` (the staircase forces coefficients +1 and −1) and `n-0` (the 5/6 family needs at least (1/6)·N·log2 N additions).
- **L5. One class.** The transform shares its circuits with every invertible 2 × 2 matrix without a zero. `d-0`, `a-0`, `g-3`, `g-4`, `g-5`, `k-cross`; now `h-6`.
- **L6. The extra value.** The saving is a value held beyond N. `g-3`, `g-7`. Its counts at 4 and 8 points, 1 and 5, are also the over-limit wires of the brick and the 19 [computed, mine; that they are one thing is guessed].
- **L7. Two periodic steps stop.** `g-6`, `c-2`. **L8. One sum of rectangles needs perpendicular trees.** `k-cross`.
- **L9. Pay once** (new). If no gate reads two over-limit wires, gates ≥ N·log2 N − (number of over-limit wires). `h-8`; hit by `h-0`, `h-1`, `h-4`, `h-5`, `h-6`. The critic: one case is closed only at 8 points and for a single over-limit wire; what is shown for the whole class is slightly weaker and still gives (2/3)·N·log2 N. So any circuit below 2/3 has a gate with two over-limit wires.
- **L10. Width** (new). If every wire mixes at most b address bits, gates ≥ N·log2 N / b. `h-5`, `n-1`. Linear size needs wires that mix about log2 N bits. A weak fence: such a wire can cost one gate.
- **L11. No tensor product sits on the count of line 5** (new). With e = gates − (N − 1) − (N/2)·log2 N, e(A × B) = n·e(A) + m·e(B) + (m − 1)(n − 1) [checked on one circuit]. `h-0`, `m-cross`.
- **L12. Old letters** (new). Counting, plus two lemmas that need equality. `e2-2`, `h-2`, `n-2`; the cut-set note of the tiny-units search is the same wall at block size 3.

Every lower-bound method of the night works on objects that meet a bound with equality and is silent one step away.

## 6. The next eight experiments

1. `unit2adic`: meter the published unit modulo 2; name the first hypothesis it breaks, and the gate; settle the conflict of section 3.
2. `onetree8`: is 19 the minimum at 8 points among one-tree circuits? Then: is 47 reachable at 16 points?
3. `eighteen`: three searches for 18 gates at 8 points, each releasing one hypothesis.
4. `twotrees`: circuits with two merge trees in different bit orders; what agreement costs.
5. `quotient`: the first useful difference-quotient gate, over the whole numbers and over the numbers a + b·i.
6. `shadow`: the subset-sum lemma of idea F on the 2,748 optimal 8-point circuits; a lead for that field's readers.
7. `compose`: ways to compose two bricks, and a brick with the 19; can the excess grow slower than N·log N?
8. (silly) `precision`: compute the transform modulo 4, then 8, then 16.

## 7. What this says about linear size

Nothing found in four waves gives linear size or moves the exponent, and nothing forbids it: every wall fences one class of programs [argued]. The fourth wave adds a necessary shape: a linear program must be full of gates that read two over-limit wires, with wires that mix about log2 N address bits, and it cannot be one merge tree modulo 2 [argued from L9 and L10; the last part rests on a guessed count]. The only program known to change the order gets there by nesting a tiny gain hundreds of levels deep, not by a clever wire, so the question is now narrow: is there a small circuit that leaves the skeleton and still pays [guessed that this is the right question].
