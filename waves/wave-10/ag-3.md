# ag-3 sector-and-port: which free steps see the sign of the move

11 October 2026, about 07:00 to 08:00 EDT, one agent, 60-minute box. Private research: nothing published, no git, no
Lean, nobody has read this. **No circuit below any known count, no growth law below N log N, nothing that changes
the order. No two-shear exchange was found. The count "n + 1" is extended to a named class of free steps, with a
proof that is three lines plus an exact computation; outside that class it is NOT extended, and the hole is stated
as one small finite question.**
Unit of cost: the engine's **moves** and **blocks**. No gate counts are used.
Marks: [ran] = my run tonight, exact (phases are fourth roots of 1 kept as integers modulo 4; no floats, no primes);
[read] = in a file I opened; [derived] = by hand tonight, checked by nobody; [guess].
Files: `ag-3-sectorandport/jspace.py`, `jspace.out`, `j33.py`, `j33.out`.

Words (as in the brief). *Array*, *move*, *block*, *shear* (target += c x source moved along one direction), *free
step* (costs no move), *address map* (relabelling of addresses by an invertible bit matrix), *port* p (the direction an
exchange leaves out), *digit column* (one of f tensor factors), h = address bits per column. D = the move along p on
all columns. *Sign pattern*: multiply every entry by +-1 according to a fixed parity of its address. *Paid move*: a
move made on one array and charged. *Character*: a simultaneous eigenvector of all shifts on one column; it is named
by h bits chi, and a *configuration* is one character per column. In that basis every step of the engine is a
permutation with phases: D multiplies a configuration by i^(number of columns with chi.p = 1), a sign pattern
translates chi, an address map g sends chi to (inverse transpose of g) chi, a shift is a diagonal sign.

## 0. The answer in ten lines

1. [derived] **The lemma, in the form that travels.** Suppose there is a linear map J, not zero, on the data of one
   array with J a = a J for every free step a and J D = - D J. Then any word of free steps, shears and paid moves
   that hands f >= 1 free moves along p to its arrays contains at least f + 1 shears. (Section 2. ad-0's count is the
   case "free steps = scalars", where J carries one eigenvector to another.)
2. [derived + ran] **J exists, so the count holds, for:** all shifts and all sign patterns; every address map that
   fixes the port p and one parity psi that is odd on p (this contains every orthogonal map that fixes p); the
   address shear along p; the map exchanging p with a second direction q; every orthogonal map at once. An explicit
   J: the sign pattern psi applied to two columns only, on the data where the shift along p on those two columns
   acts as +1. Exact dimensions of the space of such J are in section 3.
3. [ran] **J disappears in exactly two places.** (a) When a free step treats all columns but at most one
   differently (a shift or a sign pattern on single columns): no J, at every size tried. With two columns left
   alike J is back. (b) When EVERY invertible address map is free: no J at 2 columns (h = 2, 3) and none at 3
   columns for h = 3; for h = 2 it comes back at 3 columns.
4. [derived] For h >= 3 and every invertible address map free, no J exists at any number of columns: the condition
   would need a whole number equal to an integer plus 3.5 (section 3). So the sector count is silent there.
5. [derived] **The hole the brief pointed at is real, and it is a parity.** With the one J that survives an address
   map carrying p to q (psi = p + q, or the all-ones parity, which every orthogonal map fixes), BOTH moves are odd.
   The comparison then sees only whether an array is owed an odd or an even number of moves. It still forbids "two
   shears give two free moves" when the word touches one direction, or hands one direction per array. It says
   nothing about a word in which each array PAYS one of its two moves and receives the other: 2 paid moves + 2
   shears for the 4 moves two arrays owe along p and q. That is the two-shear economy (1 free move per array per 2
   stages), and nothing here excludes it.
6. [derived] That residue reduces to a question about 8 x 8 matrices (section 4). Not decided tonight.
7. [read + derived] A point of fact that ad-0 left open: in the published word all the shears of one pair go along
   the SAME line u, each stage being served by a different helper set whose window contains u; the 4 moves "paid
   back" are the 4 leftover directions (one per later window), made in one block of rank 4. I also checked by hand
   that an exchange whose three shears go along three different directions with no address map gains nothing
   (6 catch-up moves for 6 left out). So "words whose two shears go along different directions" is not a hatch by
   itself; it needs the address map of line 5.
8. Answer to "which legal step sees the sign of the move, and what does it cost?": a step on single columns (not an
   engine letter; in OpenAI's model n per use, and with it the move itself becomes a sum of free steps, which is the
   textbook), or an address map that moves the port, which sees only the parity.
9. Growth law: none new. The stage block stays at r/(3h) for every word whose free steps fix the port; r/(2h) is
   not excluded for words that trade two directions through an address map, and not constructed either.
10. State: transformed into a better question (section 4).

## 1. What the published exchange is [read: `R/Work/BridgeGeom/Stage.lean` and `B2.lean` header comments, `R/Work/Bridge/Roles.lean`, README section 6; derived: the rest]

- Label space of the five-stage word: one block of h directions plus four more, m = 5h. Twins are "two pairs on the
  same line"; `open-directions.md` D.1 says k twins on one line need 2k + 1 runs. X runs from "its line" to
  everything, Y from 0 to u-perp; the stage of block c is served by the helper set g x rho^(c), not by g.
- Reading [derived]: the three (or five) shears of a pair are all along u. Each helper window has h directions; the
  pair uses u and h - 1 others in each. So the pair covers 1 + 5(h - 1) directions with shears and climbs, and 4 are
  left: the catch-up block of rank 4. Per array 5(h - 1) + 4 = m - 1. A two-shear exchange would give m = 2h,
  2(h - 1) + 1 = m - 1 moves: one move saved per 2h instead of per 3h. This is the brief's r/(2h).
- [derived, by exponents modulo 2] Three shears along three independent directions e1, e2, e3, arrays free to make
  moves along them in between, no address map: the shears must all equal one operator E in the data's own frame
  (forced by 1 - BA = 0, 1 - CB = 0), the sum of the two arrays' frames must visit e1 + E, e2 + E, e3 + E and
  return to 0, and that walk has length at least 6. No gain. ad-0's one-direction model is the right one.

## 2. The lemma [derived tonight; the n = 2 scalar case is ad-0's]

Setting: n arrays, each a vector of a space V; a word is a product of (i) free steps A in GL_n(span of the free
steps on one array), (ii) shears 1 + E_ts x (a D^(+-1) a'), t not s, a and a' free, (iii) paid moves, array t <-
a D^(+-1) a' array t. Goal: the word equals G x diag(D on f of the arrays, 1 on the others), G free.
- Let J be as in line 1. Its kernel and image are invariant under every step, so J is an isomorphism between two
  pieces of the data on which free steps look alike and D has opposite signs. Write d for their dimension.
- Conjugating the word by J turns D into -D and nothing else. So (J word J^-1) x word^-1 is on one side
  G diag(-1 on f arrays, 1) G^-1 and on the other a product of one factor per shear and per paid move: a shear gives
  1 - 2 E_ts x (..), "identity plus a nilpotent of rank d" (a block transvection); a paid move gives -1 on one array
  (a block reflection). Free steps cancel.
- With no paid move along p: -1 on f arrays is a product of k block transvections. Each fixes a subspace of
  codimension d; k < f leaves a fixed vector. If k = f: t_2 ... t_f = -1 + N_1 fixes some v not 0, so N_1 v = 2v, and
  N_1 N_1 = 0 gives v = 0. So k >= f + 1.
- With paid moves mixed in: if tau_1 ... tau_n = -1 with every factor fixing a hyperplane (blocks: codimension d),
  the same step shows tau_1 has the eigenvalue -1, and -1 being central the product can be rotated: every factor is
  a reflection. So one shear among them forces one factor more: free moves f need f + 1 shears, however the paid
  moves are interleaved. [derived; not checked by exhaustion in the block case]
- Moves along directions orthogonal to p commute with the J of line 2 and count as free steps (ad-0 section 8.2,
  now with the reason: psi = p is even on them).

## 3. Where J exists [ran: `jspace.py`, exact; `jspace.out`, `j33.out`]

Method: in the character basis J a = a J says J[a j, a k] = phase x J[j, k], and J D = -D J says J[j, k] = 0 unless
D has opposite values at j and k. So dim(J space) = number of orbits of pairs of configurations on which both hold;
a union-find with phases counts them. Controls: one column gives 0 (D has only the eigenvalues 1 and i there: the
two-shear exchange of ad-0 exists); adding D itself to the free steps gives 0; a permutation of columns changes
nothing essential.

| free steps (shifts and sign patterns alike on all columns always included) | h=2 f=2 | h=2 f=3 | h=3 f=2, p=001 | h=3 f=2, p=111 |
|---|---|---|---|---|
| scalars only | 32 | 768 | 512 | 512 |
| shifts and sign patterns | 4 | 96 | 16 | 16 |
| + orthogonal maps fixing p | (none but 1) | | 10 | 5 (all of them) |
| + all maps fixing p and psi = p | | | 5 | |
| + address shear along p (x2 -> x2 + p) | 2 | 48 | 8 | |
| + map exchanging p and q | 1 | 21 | 4 | |
| + every orthogonal map | 1 (same) | 21 | 1 | 5 |
| + every invertible address map | **0** | 2 | **0** | **0** |
| + shift along p on column 0 only | **0** | 32 | **0** | **0** |
| + shift along p on each column separately | **0** | **0** | **0** | **0** |
| + shift along p on all columns but two | 4 | 32 | 16 | 16 |
| + every sign pattern on each column separately | **0** | **0** | **0** | **0** |
| + shifts and signs on all columns but two | 4 | 4 | 16 | 16 |

Further [ran, `j33.out`]: h = 3, f = 3, every invertible address map: 0 (both ports); every orthogonal map: 56;
h = 2, f = 4, every address map: 56.
- [derived] J at f columns gives J at f + 1 (act on the first f). So one f with a J closes the two-shear exchange
  for every word valid at all sizes.
- [derived] The explicit J of line 2: Z_psi on columns 1 and 2. It turns D into -(D^-1 on those two columns) x D
  elsewhere, which is -D where the shift along p on the two columns is +1. It commutes with a column-alike address
  map g exactly when g fixes psi. The all-ones parity is fixed by every orthogonal map and is odd on every odd
  word: one J for the engine's whole group, but then every move is odd (line 5).
- [derived] No J for every invertible map at h >= 3. An orbit of pairs needs two multisets of f characters whose
  counts on every hyperplane complement differ by 2 modulo 4. Fourier inversion gives the multiplicity of the zero
  character the value (integer) + 7 x 4 / 8 = integer + 3.5. At h = 2 the same sum is 3 x 4 / 4 = 3 and the triple
  of the three non-zero characters works: that is the J found at f = 3.
- sector.py (ad-0) found no solution of its one word family with every permutation of 4 addresses at f = 2, where
  the table says there is no J. I can give a reason on the 4 configurations (chi, chi): with 1 = the all-ones vector
  and d = D 1, the number d^T M 1 vanishes for every M in A + D A D and equals 4 for M = D [derived, by hand].
  That is one family, not a count; with every invertible address map free the question is open (it is not the
  engine's case: its maps are orthogonal).

## 4. The better question

Two arrays, two orthogonal directions p and q, free: scalars, shifts, sign patterns, the map exchanging p and q.
Every array owes both moves. **Is there a word with 2 paid moves and 2 shears?** (Known: 4 paid moves; 2 paid + 3
shears. The lemma excludes 2 shears with no paid move, and 2 shears + paid moves along one direction only.)
Smallest faithful model [derived]: f = 2, the 4 configurations (chi, chi). There the free steps on one array are
C + C + (2 x 2 matrices): two marked lines e1, e2 and a plane F; P and Q exchange the lines with the plane, and
every "free x move x free" is an arbitrary operator exchanging them. On two arrays: an 8-dimensional space
E1 + E2 + F (2 + 2 + 4), free group GL2 x GL2 x GL4, target "exchange E1 and E2"; a paid move exchanges a line of E1
plus a line of E2 with a plane of F; a shear adds one array's odd image to the other. Question: target in
(free)(step)(free)(step)(free)(step)(free)(step)(free) with two steps paid and two shears? A solution here is
necessary, not sufficient (it must then hold on all configurations and all f). A NO here closes the hole for this
pair of directions. I did not run it; a crude dimension count does not decide it [guess].
Design: modulo a prime p = 1 mod 4 first (the six orders of the four steps; normalise the free factors by the
stabilisers), then lift; or exact elimination, since every equation is bilinear in consecutive free factors.

## 5. What failed, and what I changed

- "Shears along different directions": tried first by hand as frames modulo 2; no gain, 6 for 6 (section 1). Changed
  to: the directions must be tied by an address map.
- "Prove n + 1 for address maps": the proof went through for every map fixing the port and a parity, and I expected
  the address shear along p and the exchange p <-> q to escape. The run said J exists for both. Reading the J it
  printed (it carries (3,3) to (0,0)) gave psi = p + q and then the all-ones parity.
- "So every orthogonal map is covered": no. With that J both moves are odd and the comparison is a parity; what is
  covered is one direction at a time. This is the hole of section 4.
- I did not get to a search for the two-shear word itself beyond ad-0's family.

## 6. Mutations

1. `mixed-word` (section 4): the only form in which a two-shear exchange can still exist inside the engine's group.
2. `parity-ledger`: with the all-ones J, every unit of the engine satisfies a parity identity between moves owed,
   paid moves and shears on each J-piece. Does the published five-stage word meet it with equality somewhere? It
   would say which of its shears are "forced by parity" and which by the line.
3. `three-columns-at-h-2`: at h = 2 the triple of the three non-zero characters is an invariant of every address
   map. Is there an analogue for the orthogonal group at larger h that is odd for one line only? That would extend
   the count past the parity.
4. `single-column steps priced`: hatch (a) is where J dies. Charge a single-column step its true cost (n per use)
   and ask for the cheapest word: the floor note says textbook; the J space says why nothing in between exists
   while two columns are left alike.

## 7. Criticism, last

- The lemma is derived tonight and read by nobody. Its group-theory step in the block case (nilpotents of rank d,
  paid moves mixed in) was not checked by exhaustion; ad-0 checked the scalar case at 2 x 2 and 4 x 4 over small
  fields.
- The model is ad-0's: arrays as rows over an algebra, shears with coefficient free x move x free, one shear per
  array per stage read from x-6. The engine's letters were not put in one by one. "The engine's address maps are
  orthogonal" is my reading of the Lean headers (the classes are indexed by the orthogonal group of the label
  space), not a checked statement about every letter.
- Section 1 is a reading of comments in Lean files and a hand computation; I did not replay the word.
- The J table is exact but small: h <= 3, f <= 4. "No J" is a statement about this lemma only; it is not a
  two-shear exchange.
- The integrality argument of section 3 covers J between configurations of one array; it was checked against the
  runs at f = 2, 3 only.
- Even a yes to section 4 is not 1e-1: helpers and copies remain (ad-0: factors 3.74 and 4.00).
- Nothing here is a circuit, a gate count or a change of order.
