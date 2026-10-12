# q-note: report on writing WAVE5-NOTE.md

> Editor's note (11 October 2026): the sixth note corrected what this report calls "the one question no wall covers": two results of the sixth wave do cover it. See line 10, "Corrections", in [the sixth note](../wave-06/NOTE.md).

2026-10-11, about 01:55 to 02:05 EDT, inside a 25-minute box. Private research: nothing published, no git, no Lean.
Marks: [read] in a file I opened tonight; [ran] an exact run of mine; [derived] by hand; [guess].

## What was written

`waves/wave-05/NOTE.md`: the note for the morning, in the seven sections asked
for, same layout, marks and wall numbers as the four earlier notes. About 3,250 words including a 19-row table (WAVE4-NOTE has
2,726). That is more than three printed pages; the table of section 3 is the extra. I cut one idea paragraph and several
sentences and stopped where the next cut removed a number or a name from a wall's list.

Its first line says that nothing beats the textbook in order and that the wave has no record in either count.

## Sources

- [read in full] `WAVE4-NOTE.md`, `m-note.md` (layout, wall numbering), `q-cross.md`.
- [read, first 40 to 60 lines] `r-0.md`, `r-1.md`; `h-3.md` section 2 (the count (O) table).
- [read, single lines by search] `p-0.md` (definition of hub), `p-3.md` and `WAVE3-NOTE.md` (tree step; the earlier
  ill-conditioning result of `g-3`), `p-5.md` (the conditioning door), the headings of `WAVE6-PICKS.md`.
- For the nine developments, the recombination's lists and the three attacks I used the summaries in my task text. I did not
  open `p-1.md` to `p-8.md` or `r-2.md`. Any error in those summaries is now in the note.

## What I checked myself

[ran, whole numbers and fractions only, `q-note/check.py`, output `q-note/check.out`, 1 second, through light.py]

1. The two-chain circuits for subset sums, with my own counter and my own replay (not `zreplay.py`): from the orders in
   `q-cross/cat3_4.out`, `cat3_8.out`, `cat3_16.out`, `cat3g_32.out` the corners are 5, 13, 30, 80, the circuits have 7, 19, 44,
   110 gates and return every subset sum on all basis vectors. Steps that change at most one run: 4 of 4, 8 of 8, 13 of 16,
   21 of 32, as q-cross says.
2. The same counter on two output files of the sixth wave's search, which is still running (`u-0-cornerssearch/r32.out`,
   `r64.out`): 80 corners at 32 points (its file shows five restarts, all 80) and 239 at 64 points (301 gates, Yates 192), both
   replayed. 239 is better than q-cross's 261 and still far above the Yates line (193). These are raw files of a running
   agent, not a report; the note says so.
3. p-0's hub-free 7-gate circuit for [[1,1],[1,2]] at 4 points: all four outputs right.
4. p-0's weight-only circuits at k = 2: the 5-gate circuit is right at seven values of tau; the 4-gate circuit at tau = -1.
   (The 7-gate circuit at k = 3 was not re-run.)
5. Arithmetic of every law in the table: (N^2 + 14)/6 = 5, 13, 45, 173, 685 and 4t - 7 the same; T(k) = 8 T(k-2) - 3 = 5, 13,
   37, 101, 293, 805; textbook rectangles 6, 18, 50, 130, 322, 770; N + (19/256) N^2 = 108, 368, 1344; the ratios.

My first replay printed "False" on every file: I had taken running sums from the wrong end. The corner counts were right
from the start; the fixed replay prints True on all seven files.

I did not re-run any search, any census, any letter count, or anything in Lean.

## Things the user may want to know that are not in the task text

- **The sixth wave is already running four of the recombination's eight experiments**, as five jobs (`corners` twice,
  `onerun`, `zletter`, `zdz`). Not picked up: `second52`, `whichtwo`, `weightladder`, `spreadsheet`. Section 6 marks which.
- **`u-2-onerun` has output files** that look like answers at k = 4 and k = 5. I did not interpret them, because I did not read
  what its program counts. They are not in the note.
- **Two different things are called "chains"** in the reports. q-cross's "two chains" are the most lopsided trees; p-1's
  "dual chains" are balanced trees built on chains of subgroups. The note calls the second "the standard trees" and keeps
  "chain" for the first.
- **The conditioning door was not untouched.** My task text has p-5 calling ill-conditioning "the unexplored door". WAVE3-NOTE
  records that `g-3` built badly conditioned steps with a well-conditioned product at 16 points and that they bought nothing.
  Idea C in the note says both. I first wrote "no search of the night used it" and took it out.
- **The idea with no experiment.** The recombination's eight experiments contain nothing on that door. Idea C gives p-5's own
  proposed experiment (its section on entropy pumps) and says where it comes from.
- **"Closed" is narrower than it sounds.** The quadratic floor is argued for two families of trees (the standard trees; trees
  whose smallest pairs all point one way) and read by one critic. Other trees have one modulo-3 run at 8 points and a guess.
  Line 2 and section 7 say "on the trees examined".
- **The surprise needs its caveat next to it.** The subset-sum count 5, 13, 30, 80 is an upper bound from a random local
  search; it equals Yates' count at 32 points and is above the Yates line at 64 in the one long run so far. The note does not
  present it as a lead towards linear size, only as the one question no wall covers.
- **Count (O).** The fifth wave produced no number in OpenAI's count. The (O) rows of the table are h-3's, from the fourth
  wave, with the critic's correction (56 at 16 points is for H x / 2).

## Judgment calls

- Marks: [ran] became [computed], [derived] became [argued], [guess] became [guessed]. Nothing is called proved; r-1's "now
  proved quadratic" appears as "argued; a second reader found no error".
- Wall numbering continues `WAVE4-NOTE.md`: L1 to L12 keep their numbers, L8 is replaced by a new L13 (one form per node).
- I avoided "entangled", "annealer", "cherry", "bent", "character", "coset". "Mixes an address bit" stands for entangled,
  "search" (with "upper bound") for annealer, "smallest pairs" for cherries.
- Section 2 gives the class question in the order 4, 8, 16 points, then the exceptions, then what it means for the order.
- Section 4 has five ideas. I removed a sixth (one letter with overlap at 16 points) into L13's "not covered" list.
- No odds anywhere. Section 7 is three sentences.

## Limits

- None of the nine development reports was read in full; three were searched for single definitions. `r-2.md` was not
  opened, and `r-0.md` and `r-1.md` only at the head.
- No literature was read by me.
- The note is longer than three printed pages.

## Files

`waves/wave-05/NOTE.md`,
`waves/wave-05/q-note.md`,
`waves/wave-05/q-note/check.py`,
`waves/wave-05/q-note/check.out`.
