# ag-0 ladder-degree-3: the third rung does fall to N + o(N), by a tower of lamps; the saving starts beyond any size one can write, and the fourth rung meets the same obstruction one level up

> Editor's note (11 October 2026): the critic corrected two statements of this report. For "more than 2^2059 bits" read 2,060 bits, and "the transform modulo 16 in 2N + o(N)" is off by N: 3N + o(N) by that route ([ai-0](ai-0.md)).

11 October 2026, 07:39 to about 08:20 EDT, inside a 60-minute box. Private. One agent; nothing reviewed, nothing in Lean, nothing published.
Marks: [ran] = exact run of mine in this hour, whole numbers, files in `ag-0-ladderdegree3/`; [derived] = by hand in this
hour, checked by nobody; [read] = from tonight's reports; [recalled] = from memory, no source opened; [guess].
Gate count everywhere: **(G)**, a gate is any a*u + b*v, scalings free. Count (O) is not used.

**No circuit for the transform below a known count, no growth law below N log N for the transform, none below
(1/2) N log2 N for subset sums. Nothing here changes the order.** What is here is a growth law for a smaller object
(polynomials of degree 3 at all cube points): N + o(N) gates, derived by hand and checked by exact runs only at toy
sizes (16 to 8,192 points). The o(N) is of "tower" type: it starts to beat the known 2N + o(N) only for addresses of
more than 2^2059 bits. It is a statement at infinity, not a circuit anyone can build.

Words. N = 2^k cube points, an address is k bits. *Degree-d object*: one output per address, one input per set S of at
most d bits, output(y) = sum of the inputs at the sets S inside y. c(d) = least gates / N. *Pair*: two partitions P1, P2
of the cube points; *good for degree d*: every polynomial of degree at most d is (a function of the P1 class) + (a
function of the P2 class); *classes* = classes of P1 plus classes of P2 = number of helper wires; V_d(k) = least
classes. *Selector*: t address bits a; the other m = k - t bits are y. In everything below **P1 forgets the selector**
(its class is y) and the value of the selector is called the *colour*; there are L = 2^t colours.
*Atom*: a group of s bits of y that belongs to one colour. *Active atom* of colour c at y: the one atom of colour c that
P2 forgets at the points (c, y); which atom is active may depend on the bits of y that do not belong to colour c.
*An atom fixes a bit q*: q has one and the same value at every y where that atom is active.
*Null to degree e*: a list of signed points whose signed sum of every monomial of degree at most e is zero.

## 0. In nine lines

1. **Why two helpers are the whole question** [derived, section 1]. In any circuit with N + h gates for degree d >= 2,
   all but at most h + (number of inputs) outputs are made by one gate from two wires that are not outputs. So "N + o(N) gates" is the same
   as "o(N) classes whose helpers cost o(N)"; chains output = output + helper cannot help.
2. **Rule D** [derived, section 2; it sorted 12 of 12 designs run correctly]. With P1 forgetting the selector, the pair is good
   for degree 3 as soon as: *for any two bits p, q in atoms of two different colours, p's atom fixes q or q's atom
   fixes p.* The proof is six lines of summation by parts.
3. **A family that obeys rule D with any number of colours** [derived; ran for 2 and 3 colours]: the *tower of lamps*.
   Level 1 is one atom; level j + 1 has one atom for EVERY value of all the bits of levels 1 to j; colour j forgets the
   level-j atom indexed by the present value of everything below. Bits: m_1 = s, m_(j+1) = m_j + s 2^(m_j).
   Classes = N (1/L + 2^(-s)). **So V_3(k) = o(N)**, where ad-6 had N/2 + o(N).
4. **Gates** [derived; the two facts it needs were run at 16, 2,048 and 8,192 points]: the P1 helper is again a
   polynomial of degree 3 in y, the P2 helper is a polynomial of degree 2 on each piece. So
   **c(3) <= 1 + 3/L + 2/2^s + o(1): degree 3 costs N + o(N).** Through ae-cross's dictionary: the transform modulo 16
   in 2N + o(N) [conditional on the recalled rule for transposed matrices, as in ae-cross].
5. **This answers ad-6's open case (c)** [ran]: three partitions of the 11-bit cube, none of them trivial, that work
   under one forgotten selector (8,192 points, exact). ad-6's own class (each side forgets a fixed set, or an atom
   chosen by a fixed selector) cannot do it, and I can say why in three lines (section 3).
6. **Price** [derived]: the bits needed grow like a tower in the number of colours. Four colours with one-bit atoms
   need 2,059 bits of y. Under rule D a third colour needs at least 2^(s 2^(s-2)) atoms, so inside rule D the excess
   cannot fall faster than about log log k / log k, and the tower gives 1 / log*(k). Section 4.
7. **(b), small sizes** [ran, on the recalled bound ad-6 used]: girth alone allows at best 55 classes at 64 points
   (56 known), 103 at 128 (108 known), 191 at 256 (208 known); below N/2 only from 16,384 points on. I searched
   nothing there: one class at one size is a constant.
8. **The fourth rung** [derived, section 5]: the tower fails degree 4 [ran], and what is missing is ad-6's obstruction
   one level up: two atoms of ONE colour and a lower bit that tells them apart. A sufficient rule for degree 4 (D4) is
   written down; I argue it has no finite design of this kind. With ag-7's lower bound of this same hour (2N - o(N)
   from degree about log2 k on) the ladder is: rungs 2 and 3 cost N + o(N), the third only beyond a size nobody can
   write; rung 4 is open with a named obstruction; nothing uniform up to degree k/2.
9. **(a), the exact ladder at 16 points**: not recomputed; ag-7 ran it [read, ag-7.md line 1 of its summary]: 8 points
   7, 11, 12 gates for degree 1, 2, 3 (modulo 2 and modulo 3, each equal to the textbook); 16 points 15, then 21 to 26,
   26 to 31, 31 or 32. No step at these sizes is below the textbook's.

## 1. Chains do not help: a circuit with N + o(N) gates is a pair [derived]

A relation among the outputs of the degree-d object (a combination that is zero whatever the inputs) involves at least
2^(d+1) outputs: scale it to whole numbers with no common factor and reduce modulo 2; what is left is a non-zero word of
the dual of the Reed-Muller code, whose least weight is 2^(d+1) [recalled; ag-7 derives the same number].
Take a circuit with N + h gates. Each output has its own gate. Call a gate *chained* if one of its two wires is another
output, the other wire w being a helper. Then w is a combination of two outputs. If the same w fed two chained gates,
four outputs would be dependent; for d >= 2 that needs 8. (Fed twice by the same two outputs it would make a loop.)
So each wire that is not an output feeds at most one chained gate: at most h + (number of inputs) chained gates, and
the inputs number about k^d / d!, which is o(N). A gate cannot read two outputs and produce a third (3 < 8).
**All but o(N) outputs are helper + helper** (a helper may be an input). The helpers are the vertices of a graph, the outputs its edges, and ad-6's pairs are the case where
the graph has two sides. (A graph with odd cycles and free coefficients is slightly more general; I did not use it.)
[read, after writing this] ag-7 found the same statement in the same hour, over the two-element field, as its
"private-wire lemma" (ag-7.md section 4), and checked it on 3,456 minimum circuits at 8 points. Two authors, two
fields. Its consequence there: at most about N^(1/6) outputs per helper at degree 3, which the tower respects.

## 2. Rule D, and why it is enough [derived; tested, section 6]

Setting. P1 forgets the selector. At colour c, P2 forgets the active atom of colour c. Draw the *y graph*: its points
are the y, and y, y' are joined by an edge of colour c when they differ only inside the active atom of colour c.
A polynomial of degree 3 in (a, y) is F(a, y) = c0(y) + Q_a(y), c0 of degree 3 and each Q_a of degree 2 in y.
We need A(y) with Q_c - (A - c0) constant along every edge of colour c. Such an A exists exactly when, for every closed
walk in the y graph, the sum over its edges of Q_colour(start) - Q_colour(end) is zero. That holds for every choice of
one quadratic per colour (more than degree 3 asks for) exactly when **the edges of each colour, taken alone, are null
to degree 2** (signed: + start, - end). For degree 3 alone this is sufficient; the exact condition for t = 2 is in
section 3.
Check the monomials. Constants: clear. One bit y_p: only moves of p's colour change it, and the walk is closed. Two bits
of one colour: the same. Two bits p, q of two colours j and l: write K(p, q) = sum over the moves that change p of
(change of y_p) * (value of y_q at that moment). Because the walk is closed, K(p, q) + K(q, p) = 0 (the product y_p y_q
returns to its value). If p's atom fixes q at the value c, then K(p, q) = c * (total change of y_p on that atom) = 0.
If q's atom fixes p, then K(q, p) = 0 and so K(p, q) = 0. That is rule D. It gives more than degree 3: every function
"one cubic in y, plus a quadratic in y that depends on the colour in any way at all".
What rule D is made of: ad-6's missing monomial a_i y_p y_r is K(p, r) for two atoms of two colours neither of which
looks at the other. ad-6's family has fixed atoms, so no atom fixes anything.

## 3. The tower of lamps, and ad-6's open case (c)

Level 1: one atom U_1 of s bits. Level j + 1: one atom of s bits for each of the 2^(m_j) values of the m_j bits below.
Colour j forgets the level-j atom whose index is the present value of all lower bits (colour 1 forgets U_1).
Rule D holds: of two atoms of different levels, the higher one is active at exactly one value of every lower bit.
(In group words: the regular wreath product, iterated; ad-6's family is the two-level case B wr A.)
Each P2 class has 2^s points, each P1 class L points: **classes = N (1/L + 2^(-s))**.
[ran, `designs.py`, `designs.out`, exact walk of ad-6's `verify.good`]
- 2 colours, s = 1: 16 points, 16 classes, good for degree 3, not 4. (ad-6's "one more degree".)
- 2 colours, s = 2: 2,048 points, 1,536 classes = 0.75 N, good for degree 3, not 4. (Also ad-6's.)
- **3 colours, s = 1: y has 1 + 2 + 8 = 11 bits; with 2 selector bits (the fourth colour forgets nothing) 8,192 points,
  7,168 classes, good for degree 3, not 4.** New: three non-trivial partitions under one selector.
- The tree in which a level-j atom is indexed only by the ACTIVE atoms above it (7 bits instead of 11): 4 violations of
  rule D, not good for degree 3. The index must contain every lower bit, active or not: that is where the tower
  comes from. Lamps indexed by parities (the free metabelian group in its lamp coordinates, 12 bits): 48 violations,
  not good.
(c) exactly [derived]: for t = 2 the four partitions R_00..R_11 must satisfy: the joins (R_00 v R_01, R_10 v R_11) and
(R_00 v R_10, R_01 v R_11) good for degree 2 (ad-6's two conditions) AND (R_00 v R_01 v R_10, R_11) good for degree 1;
together these are also sufficient. Why ad-6 found none [derived]: if each of the two good pairs is of ad-6's kind
(selector alpha with atoms X_alpha; selector beta with atoms W_beta) and all four common refinements forget something,
then alpha must meet each of the 2^|beta| disjoint atoms W_beta, and beta each of the 2^|alpha| atoms X_alpha:
|alpha| >= 2^|beta| and |beta| >= 2^|alpha|, impossible. The tower escapes because its pairs of colours are not of
that kind: neither colour 2 nor colour 3 forgets a fixed set.
Also [ran]: two-colour designs in which NEITHER colour forgets a fixed set and both obey rule D exist at every size
tried ("caterpillar": colour 0 forgets alpha_i with i the first non-zero beta; colour 1 forgets beta_i with i the first
non-zero alpha; 5, 7, 9, 11 bits, all good for degree 3). They save no class, and their P1 helper is NOT a low-degree
polynomial (degree 3, 4, 6, 6 in y), so they give no gate law. They answer the brief's "keep asking" (such pairs exist) and not
its hope.

## 4. Gates, the law, and its price

[ran, `check_helpers.py`, `check_helpers.out`] In the tower, for 2 colours (s = 1, 2) and 3 colours (s = 1): the P1
helper A, as a function of y, has degree exactly 3 for every input; the P2 helper of colour c, on each piece "lower
bits fixed" (one atom active, a subcube), has degree at most 2 in the free bits.
[derived] So: N output gates; A at 2^m = N/L points, at most 3 gates per point by the textbook; the P2 helpers at
N/2^s points in all, at most 2 gates per point; forming the restricted coefficients costs a polynomial in m per piece,
which is negligible. **Gates <= N (1 + 3/L + 2/2^s) + o(N) whenever k >= log2 L + m_L(s).** With ad-6's degree-2 law
inside, 1 + 2/L + 1/2^s. Nothing was built gate by gate beyond the exact solve of U and V at 8,192 points.
The price. m_2 = s + s 2^s; m_3 = m_2 + s 2^(m_2); m_4(s = 1) = 11 + 2^11 = 2,059; m_4(s = 2) is about 2^2059.
The bound drops below the known 2N only with L >= 4 and s >= 2. **As a function of k the excess is about 1/log*(k)**
(log* = the number of times one takes log2 before reaching 1). At every size a machine could hold, ad-6's
N/2 + V_2(k - 1) is better.
Is the tower forced? [derived, rough] Inside rule D: an atom that fixes f atoms is active on at most a 2^(-sf) part of
the states. If two colours both have fewer than 2^(s(j+1)-1) atoms, with j = 2^s / 4, then in one of them some atom is
active on more than a 2^(-s) part and therefore fixes nothing; two such atoms of two colours break rule D. So all
colours but two have at least about 2^(s 2^(s-2)) atoms: doubly exponential in s for the third colour already.
Among designs given by one order of the atoms ("later fixes all earlier"), 3 colours with one-bit atoms need exactly
1 + 2 + 8 bits: the tower is the least [derived from Kraft's equality, small case only].
Rule D is sufficient, not necessary, and "P1 forgets a selector" is a choice. Girth alone asks only for N^(7/8) classes.

## 5. The fourth rung

[ran] Every tower tried fails degree 4. [derived] What it is made of: degree 4 needs each colour null to degree 3.
Triples of bits of three different colours are fine under rule D; two bits of one atom and a third are fine. The one
bad triple: p and q in two DIFFERENT atoms alpha, alpha' of one colour, r in an atom beta of another colour, alpha and
alpha' both active only at a fixed value of r, two different values, and beta fixing neither. In the tower: any two
atoms of one level and a lower bit on which their indices differ. It is ad-6's missing monomial again (a bit that
tells two atoms apart, times one bit of each), with "selector" replaced by "everything below".
Sufficient for degree 4 [derived, not run]: rule D plus **rule D4**: for every atom beta and every other colour, the
atoms of that colour that beta does not fix all need the same value of beta ("home").
Yes, and (1): make beta fix every atom that needs it away from home (mutual looking: an atom can be switched off only
when it is back at zero). Then when the top atom is non-zero and every lower atom of the other colour is away from
home, no atom of that colour may be active; a new atom above the top is needed, and so on without end [derived,
sketch]. I found no finite design, and believe there is none of this kind.
Yes, and (2): D4 is only sufficient. [ran, `q4.py`, `q4.out`] On 4 bits there is a two-colour design that obeys
rule D, breaks D4 and is still good one degree higher: colour 0 forgets p1 where q1 = 0 and p2 where q1 = 1; colour 1
forgets q2 where p1 = p2 = 0 and q1 elsewhere. Alone it is a pair good for degree 3 on 16 points (one 16-cycle, 16
classes); with a selector bit it is good for degree 4 on 32 points (32 classes, no saving). There
the sum Z = sum over moves on alpha of (change of p) * q vanishes by itself. A design with large atoms in which Z
vanishes for a reason is the open door; I have no candidate.
Where this leaves the ladder. Rung 2: N + O(N log k / k) (ad-6). Rung 3: N + O(N / log* k) (here). Rung 4: open, with
a named obstruction. ag-7 (same hour, unreviewed): from degree about log2 k on, at least 2N - o(N) in any circuit.
So "c(d) stays bounded up to d near k/2" is not reached by this road at all: each rung is cheap only beyond a size
that grows faster than any tower in the rung's number. **For the transform: no growth law.**

## 6. What was run, and what was not

- `tower.py`, `W_L3_s1.out`: the tower, built directly, 3 colours: good for degree 2 and 3, not 4.
- `designs.py`, `designs.out`, `q4.py`, `q4.out`: 12 designs; rule D counted exactly over all states; goodness by
  ad-6's exact walk; degree of the P1 helper by a Moebius transform. Rule D has 0 violations in 9 designs, all 9 good
  for degree 3; it is violated in 3, all 3 not good. (Rule D is proved sufficient only. A first, wrongly coded
  caterpillar at three sizes also violated it and was not good; that output was overwritten.)
- `check_helpers.py`, `check_helpers.out`: degrees of both helper families; the girth window k = 5 to 16.
- Not run: any tower with 4 colours (2,059 bits); any atom of more than 1 bit with 3 colours (2,058 bits); the gate
  count as a built circuit; rule D4; any search at 64 or 128 points; part (a) (ag-7 has it).

## 7. Mutations

1. **Least atoms.** The least number of bits of a design with L colours, atoms of s bits, each colour null to degree 2
   in every closed walk (not rule D: the exact condition K(p, q) = 0). Smallest case: 3 colours, one-bit atoms, fewer
   than 11 bits; exhaustive over three perfect matchings of the 7- to 10-bit cube is too large, a search over
   activation functions that read at most 3 bits is not. If the answer is 11, the tower is the truth and the excess is
   1/log*(k); if less, there is a second mechanism.
2. **No selector.** A two-colour design obeying D and D4 (or with Z = 0) is by itself a pair good for degree 3 with
   N * 2^(1-s) classes and no selector. The 4-bit example is the s = 1 case. Is there one with s = 2 (first possible
   size 16,384 points by the Moore bound)?
3. **The exact (c) at small size**: four non-trivial partitions on fewer than 2,059 bits, using the three conditions of
   section 3 directly.
4. **Three helpers with coloured atoms**: rule D with one more forgotten thing per point. ae-cross's hybrid 4 says the
   ceiling of two helpers disappears; the bad triple of section 5 has exactly three atoms in it.
5. **The home rule as a theorem**: prove that D + D4 has no finite design, or find the regress's fixed point.
6. **Use the room**: the tower serves "a cubic plus ANY colour-dependent quadratic". Which functions of interest to the
   transform (quadric signs on a subcube, ad-6 mutation 5) are of that form?

## 8. Criticism, last

- The headline is derived by hand in 45 minutes. The proof of rule D is short and the runs agree with it 12 times out
  of 12, but the largest tower run has one-bit atoms and three colours; "any number of colours" is the proof, not a run.
- The gate law rests on two facts seen at three toy sizes (A is cubic, B is piecewise quadratic) and on a hand formula
  for A that I derived and did not write into a program. No circuit was replayed from the coefficients.
- The o(N) is 1/log*(k). For every k below 2^2059 the construction is worse than ad-6's. Nobody can use it.
- The lower bound "third colour needs 2^(s 2^(s-2)) atoms" is for rule D only, and is rough. The claim that D + D4 has
  no finite design is a sketch.
- The Moore window uses the theorem ad-6 recalled and did not look up. I did not look it up either.
- Literature: one web search, two minutes. What it returned is the plain way only: one addition per point for an affine
  function along a Gray code, and d operations per point for degree d (Bouillaguet and others' enumeration over the
  two-element field; a 2023 extension to other fields, eprint.iacr.org/2023/619). Nothing on N + o(N) for degree 2 or
  3, and nothing on the size of encoders of Reed-Muller codes. One search is not a survey: it may be known, and so may
  the wreath-product reading (it is a Cayley graph of large girth with cube coordinates).
- I read ag-7's summary only, not its proof of 2N - o(N).
- The user's bar is the order of the transform. This report is about rung 3 of a ladder whose rungs near k/2 carry the
  mass. Nothing here speaks for linear size or for a saving of 1e-1. What it adds is the reason: each rung needs the
  next layer of atoms to be indexed by everything that could tell two of them apart, and each such layer costs an
  exponential in the number of address bits.

Files: `waves/wave-10/ag-0-ladderdegree3/` : tower.py, W_L3_s1.out;
designs.py, designs.out; check_helpers.py, check_helpers.out; q4.py, q4.out.
