# ac-0: criticism of ab-0's 15-gate circuit modulo 2 for one block of neighbour sums at 16 points

11 October 2026, wave 8 skeptic, 30-minute box (06:21 to 06:51 EDT). Private; nothing reviewed, nothing in Lean.
Marks: [read] in a file or page I opened; [ran] computed in this box with my own code, exact (integers, fractions, or a
named prime field); [derived] argued by me here, checked by nobody; [guess]. Gate count is (G) throughout: a gate is any
a*u + b*v, scalings free; modulo 2 that is simply u + v. Folder F = `waves/wave-08/ac-0/`.

Words. 16 points = the 16 addresses of 4 bits. *Neighbour sums*: output(y) = the sum of the inputs at the 4 addresses that
differ from y in one bit. *One block*: the 8 outputs at addresses with an odd number of ones, each a sum of 4 of the
8 inputs at addresses with an even number of ones; an 8 x 8 matrix of zeros and ones, "row y" for output y. Inputs are
numbered x0..x7 = even addresses 0, 3, 5, 6, 9, 10, 12, 15. *Adding-only circuit*: gates u + v with nothing ever
cancelling. *Antipode* of y: y with all four bits flipped. *Lift*: the same wiring (which gate reads which two wires) with
other coefficients, correct over the rationals.

## Verdict in one paragraph

**Everything ab-0 claims about this object holds, and I could make each claim a little stronger. It is an instance of a
known phenomenon, and it gives nothing in the user's terms.** The circuit is right modulo 2 with 15 gates; 14 is impossible
modulo 2 and 15 is impossible for adding-only circuits (both by my own exhaustive search); the wiring has no lift for ANY
coefficients, zero included, and with the rows allowed to sit at any gates. One sentence of ab-0 is wrong as an explanation:
its "recursion behind it" yields 32 gates at 16 points, the adding-only count, not 30; it does not explain the saved gate.
Carried to larger sizes the saved gate gives, modulo 2 only, N (23k/32 - 1) gates against N (3k/4 - 1): the same order,
a constant 23/32 in place of 24/32. Over the rationals: no circuit, no count beaten, no saving exponent, and no bearing on
the transform, which does not exist modulo 2 (its matrix is all ones there).

## 1. The claim, precisely

(a) There is a circuit of 15 gates u + v over the field with two elements whose wires include all 8 rows of the block.
(b) No such circuit has 14 gates. (c) A circuit of gates u + v in which nothing cancels needs 16, and in general the whole
neighbour-sum map on N = 2^k points needs exactly N (k - 1 - floor(k/2)/2) such gates. (d) The wiring of (a) computes the
block over the rationals for no choice of coefficients. Not claimed: any circuit over the rationals, any count beaten there.

## 2. My own verification  [ran unless marked]

- **Replay** (`replay.py`, `replay.out`): wiring read from `B4_p2_m7_top_d2.out`, values recomputed; all 15 printed vectors
  reproduced; the 8 rows sit at g17, g14, g20, g21, g22, g12, g18, g15 (outputs 1, 2, 4, 7, 8, 11, 13, 14). The second
  file `..._top_d4.out` also replays: 15 gates, 8 rows. With every gate u + v over the integers the same wiring gives
  only 5 right outputs (1, 2, 11, 13, 14); g19 comes out as [0 1 1 0 2 1 1 2].
- **14 gates modulo 2: none; 15: yes** (`xs.c`, written from scratch, no code shared with `mincirc`; `xs_xor_m6.out`,
  `xs_xor_m7.out`). Exhaustive over sets of 6 extra wires, 54,789,105 final states, 9 seconds. My search prunes
  differently from `mincirc` (its counts differ from level 3 on: 9,666 against 21,174) and reaches the same verdict.
- **Adding-only: 15 gates none, 16 yes** (`xs_add_m7.out`, `xs_add_m8.out`; same program, wires restricted to subsets of
  a row and sums to disjoint supports). So "15 where adding-only needs 16" is exact at this size.
- **Ranks** of the block: 5 over the rationals and modulo 3, 5, 7; 4 modulo 2. At 64 points 22 and 16; at 256 points
  64 modulo 2, a quarter of N each time (`more.out`).

## 3. The no-lift claim: does it cover coefficients other than signs?  Yes, and more

ab-0's hand argument is free of the coefficients (it intersects two planes), but it takes for granted that in a lift every
gate still holds the row it held modulo 2, and that no coefficient is 0. Both gaps close:

- [ran] Whatever the coefficients, a gate's vector is zero outside the union of the inputs below it. Rows that fit:
  g12 only row 11; g14 only 2; g15 only 14; g17 only 1; g18 only 13; g19 rows 11 or 13; g20 any; g21 rows 7, 11, 13, 14;
  g22 rows 1, 8, 11, 13; the other six gates none. So row 4 can only be g20; then row 7 only g21 and row 8 only g22; then
  rows 2 and 14 only g14 and g15.
- [ran] Over the rationals (and modulo 3 and 5) the only dependent sets of at most 4 rows are the six sets made of two
  antipodal pairs (row y + row antipode(y) = the all-ones row). Rows 2, 4, 7, 14 contain no antipodal pair: independent.
- [derived] g20 = s g19 + t g14 must be a multiple of row 4 with g14 a multiple of row 2, so s is not 0 and g19 lies in
  the plane of rows 4 and 2. In the same way g19 lies in the plane of rows 7 and 14. The two planes meet only in 0, so
  g19 = 0 and g20 is a multiple of row 2: contradiction. Modulo 2 the four rows ARE dependent (they are the four
  neighbours of address 0110, and the sum of the outputs at the four neighbours of any address is 0 modulo 2); that is
  the whole trick, and it is false in every field where 2 is not 0.
- [ran] Independent sweep, `lift3.c`: all 4^15 = 1,073,741,824 choices of coefficient pairs up to scaling modulo 3
  (u alone, v alone, u + v, u - v at each gate): 0 give the 8 rows; the most any choice gives is 6. This contains every
  sign choice, so it re-proves ab-0's "0 of 32,768". With a sound cut (`liftp.c`): 0 also modulo 5, 7, 11, 13. Positive
  control: modulo 2 exactly 1 choice works, the circuit itself (`ctl_p2.out`).
  A sweep modulo p is a statement in that field; the proof over the rationals is the three lines above.

Limit, as ab-0 says: this kills one wiring (and the second one was not examined by me), not "15 gates over the rationals".

## 4. The adding-only law N (k - 1 - floor(k/2)/2)

- [derived] I checked ab-0's proof line by line; it is correct for gates u + v. The two facts it needs: an output's gates
  form a tree on its k neighbours (nothing may appear twice), and two addresses share at most 2 neighbours, so only a gate
  on two inputs can serve two outputs, and it serves exactly two.
- [ran] The pairing circuit, built and replayed over the integers by my code, has exactly that many gates for k = 2..8:
  2, 12, 32, 96, 224, 576, 1280. At the 16-point block my exhaustive search gives 16 and not 15.
- [derived, new here, unchecked] **The law also holds when positive scalings are allowed** (gates a*u + b*v with a, b > 0),
  which ab-0 left open. For output y let p be the number of two-input-support gates below it that feed larger gates, r the
  number of raw inputs that feed larger gates, g the number of gates with three or more inputs in their support. Those g
  gates serve y alone, join p + r sources into one wire (so g >= p + r - 1), and the sources must cover the k neighbours
  (2p + r >= k). A two-support gate serves at most two outputs. So the gates are at least the sum over y of
  g + p/2 >= (3/2) p + r - 1, whose least value under 2p + r >= k is k - 1 - floor(k/2)/2.
- Known theory [read: titles and abstracts tonight; the statements from memory, not re-read]: a 0/1 matrix in which no two
  rows share three ones needs a number of adding-only gates proportional to its number of ones (Nechiporuk 1969;
  Mehlhorn 1979; Pippenger 1980; Wegener 1980; survey Jukna and Sergeev, "Complexity of Linear Boolean Operators", 2013).
  The cube has N k ones and that property, so "adding-only is of order N k" is classical; the exact constant 3/4 for the
  cube I did not find in print in the time I had.

## 5. Is the object known?

The phenomenon is known; this instance I did not find. That circuits of additions modulo 2 can be smaller than circuits in
which nothing cancels is standard: Boyar and Find, "Cancellation-free circuits in unbounded and bounded depth", 2013,
arXiv:1305.3041 (the gap can be a factor of order n/(log n)^2); Find, Göös, Järvisalo, Kaski, Koivisto, Korhonen,
"Separating OR, SUM, and XOR circuits", arXiv:1304.0513, J. Comput. Syst. Sci. 2016 (matrices with O(n) gates modulo 2
that need about n^2/(log n)^2 without cancellation).
What that theory predicts for "linear or not": **nothing against, nothing for.** No lower bound above linear is known for
any explicit matrix in circuits modulo 2, so O(N) for neighbour sums modulo 2 is not excluded; and the known gaps are
existence results for specially built matrices, not methods for this one. Neither statement crosses to the rationals.

## 6. One size further, and the growth law

- [derived] ab-0's "recursion behind it" (split by the last bit; half of the outputs are the (k-1)-bit neighbour sums of
  the other half; "saves N/2 gates at each even k") costs 2 c(k-1) + N/2 with c the adding-only count, which is
  N (3k/4 - 1): 32 at 16 points, 224 at 64. It TIES adding-only; it does not give 30. The saved gate has another source:
  g19 = x3 + x5 + x10 + x12 (addresses) is the sum of the inputs on one plane, and modulo 2 it equals the sum of two
  outputs for four different pairs (13,11), (2,4), (14,7), (1,8); one gate makes it, three outputs take it.
- [ran] The only way I found to carry the gate upward is composition: for k = 4m, apply the 16-point circuit to each group
  of four bits and add the m results. Built and replayed modulo 2: **30 gates at 16 points, 216 at 64 (four bits plus a
  pair), 1216 at 256**, against adding-only 32, 224, 1280.
- **Growth law observed, modulo 2 only: N (23k/32 - 1) for k a multiple of 4**, against N (24k/32 - 1). The order is
  unchanged; the constant drops by one part in 24. I found no way to make the gain grow with k: the relation used at
  larger even k (output(y) + output(y + e_a + e_b) = neighbour sums in the other k - 2 directions of a folded input)
  again ties [derived, rough]. Whether neighbour sums modulo 2 can be had below order N k is open, to my knowledge
  [guess: I know no bound and no construction, and I searched the literature for ten minutes only].
- Not done: no search at 32 or 64 points (the exhaustive method stops at 16 points; 15 gates there already took
  54 million states), and ab-0's "none with 14 modulo 3, none with 13 modulo 5" were not re-run by me.

## 7. In the user's terms

Nothing. No circuit over the rationals at any size, no formula for n points over the rationals, no saving exponent.
The transform itself has no version modulo 2. The object is a clean small fact about the number 2.
What it does leave for the generators, as an anomaly worth one line: the saving modulo 2 comes from a *plane sum shared by
several outputs*, a wire that is a different combination of outputs at different addresses. Over the rationals the only
relations among these 8 rows are the antipodal ones, and the natural completion by them costs me 18 gates (ab-0 counts
17 by its route) against 16 [ran: the identities; the count is by hand, not minimised].

## 8. Did anything fail?

No claim failed. The one statement to correct is the explanation in ab-0 section 2 ("a recursion behind it ... saves N/2
gates"): the nearest true statement is "that recursion equals the adding-only count at every even k; the 15 comes from
one plane sum used three times, and composes to N (23k/32 - 1) modulo 2".

## Sources

- https://arxiv.org/pdf/1305.3041 (Boyar, Find, 2013)
- https://arxiv.org/pdf/1304.0513 (Find, Göös, Järvisalo, Kaski, Koivisto, Korhonen; journal version 2016)
- https://web.vu.lt/mif/s.jukna/Knizka/linear.pdf (Jukna, Sergeev, 2013)
- https://arxiv.org/pdf/1207.5321 (Boyar, Find, 2012, the cancellation-free model)

## Files (all in F)

`replay.py`, `replay.out` (replay, ranks, dependent sets, supports, pairing law k = 2..8, composition at 16 and 256
points); `more.py`, `more.out` (64 points, ranks to 256 points, the antipodal identities); `xs.c`, `xs` and
`xs_xor_m6.out`, `xs_xor_m7.out`, `xs_add_m7.out`, `xs_add_m8.out` (my exhaustive search, modulo 2 and adding-only);
`lift3.c`, `lift3`, `lift3_p3.out` (all coefficient choices modulo 3); `liftp.c`, `liftp`, `liftp.out` (modulo 3, 5, 7,
11, 13 with the support cut); `ctl_p2.out` (positive control). Nothing was run on the rented machine.
