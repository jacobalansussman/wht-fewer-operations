# m-note: report on writing WAVE4-NOTE.md

2026-10-11, about 01:31 to 01:42 EDT, inside a 25-minute box. Private research: nothing published, no git, no Lean.
Marks: [read] in a file I opened tonight; [ran] an exact run of mine; [derived] by hand; [guess].

## What was written

`waves/wave-04/NOTE.md`: the note for the morning, in the seven sections asked for,
same layout and marks as the three earlier notes. About 2,700 words (the earlier ones have 2,459, 2,914 and 2,587). That is more
than three printed pages. I cut one table row and several sentences and stopped where the next cut removed a number or a name
from a wall's list.

Its first line says that nothing changes the order. It then reports: the constant in OpenAI's count (5/6), the "one gate per
over-limit wire" regularity, the one-merge-tree skeleton modulo 2, the two new lemmas (pay once, width), the batch result for 4,
5 and 6 arrays, and the published unit read as a circuit.

## Sources

- [read in full] `WAVE3-NOTE.md`, `k-note.md` (layout, wall numbering), `m-cross.md`.
- [read, first 60 to 80 lines] `n-0.md`, `n-1.md`, `n-2.md`, `h-7.md`; the first 30 lines of `q-cross.md`.
- [read, single lines by search] `h-8.md` (the conflict passage), `n-0.md` (the literature paragraph, the "60" passages).
- For the nine developments I used the summaries in my task text. I did not open `h-0.md` to `h-6.md`. Any error in those
  summaries is now in the note.

## What I checked myself

[ran, whole numbers only, `m-note/check.py`, output `m-note/check.out`, 1 second, through light.py]

1. The 19 (wiring as in `k-note/check.py`): outputs are exactly H_8 in natural order.
2. The meter modulo 2, written from the definition in `m-cross.md`, not from its code. Textbook at 4, 8, 16 points, the brick and
   the 19: each has exactly 2N - 1 classes, nested or disjoint, and N - 1 gates that make a new class. Dead gates: 5, 17, 49 for
   the textbook (N log2 N - N + 1); 4 for the brick and 12 for the 19 ((N/2) log2 N).
3. Over-limit wires (non-zeros in the inputs times non-zeros of the wire written in the outputs, above N): none in the textbook,
   1 in the brick, 5 in the 19. So gates + over-limit wires = 8 and 24, as h-0 says.
4. Arithmetic: the count N - 1 + (N/2) log2 N is 2, 7, 19, 47, 111, 255; the staircase formula gives 7, 20, 52, 128, 304; the (O)
   law gives 28, 384, 4,352, 45,056 at k = 3, 6, 9, 12; the savings 1.01e-1, 6.5e-2, 3.2e-2 (17, 18, 19 moves for 4 arrays),
   2.5e-2, 8.9e-2, 1.07e-1, 1.2e-2; exponent 0.8213 for 3.75 moves per array at block size 5; 120/28,135 = 0.0043.

I did not re-run any search, any census, or anything on the published certificate.

## Things the user may want to know that are not in the task text

- **A decision, not a result.** The 5/6 constant in OpenAI's count is the one thing of the wave that an outsider could check and
  that is below a published figure (Alman and Rao, 23/24). It does nothing for the order, so it is below the standing bar. The
  note says only that it needs an outside replay. Whether it is worth a paragraph anywhere is the user's call.
- **The "60" is not beaten.** The task text lists h-3's 56 as below a count on the list. The critic n-0 shows the two numbers are
  for different outputs (H x / 2 and H x / 4). Line 3 of the note says so.
- **One link nobody stated** [ran for the numbers, guess for the meaning]: the third wave's wall "the saving is an extra value"
  counted 1 and 5 extra values at 4 and 8 points. Those are the numbers of over-limit wires in the brick and the 19. The note
  puts this under L6 and marks the identification as guessed.
- **Proposition A is weaker than its summary.** The critic n-1: what is shown for every circuit of the class is
  gates >= N log2 N - V - F (F counts one kind of hub), which still gives (2/3) N log2 N. The note states L9 with that caveat.
- **A detail of h-2 that failed** [read, n-2]: h-2 expected the 20-move patterns that pass both lemmas to be sums of four
  frames only; the critic found exactly one more. It saves nothing and is not in the note.
- **The skeleton may be an artefact.** m-cross's own criticism: the pools were wires with entries 0, +1, -1 and the searches
  started from known circuits. The note carries that caution in section 2.
- **"2^1152 address bits"** is h-7's figure for where the one-gate-per-wire rule can first fail; in points that is 2^(2^1152).
- **The h-7 / h-8 conflict is unresolved.** The note says it is between two reports of the night and not about the release.

## Judgment calls

- Marks: [ran] became [computed], [derived] became [argued], [guess] became [guessed]. Nothing is called proved; h-8's
  "Proposition A" and h-5's "theorem" appear as lemmas L9 and L10 with the mark [argued].
- I avoided the words "entangled", "kernel", "annealer", "hub" and "product wire". "Mixes an address bit" stands for entangled;
  "random local search" for annealer.
- Wall numbering continues `WAVE3-NOTE.md` (L1 to L8) and adds L9 to L12, so the three notes can be read together.
- Section 2's table has four searches; I dropped h-0's "one wire replacing two or three" (36,084 candidates, none) and h-8's
  census (spread at most 4N) for length.
- Section 4 has six ideas; the recombination's eight experiments are all in section 6, under its folder names.
- No odds anywhere. Section 7 is three sentences.

## Limits

- Seven of the nine development reports were not opened. The note is as good as the summaries handed to me.
- No literature was read by me.
- The note is longer than three printed pages.

## Files

`waves/wave-04/NOTE.md`,
`waves/wave-04/m-note.md`,
`waves/wave-04/m-note/check.py`,
`waves/wave-04/m-note/check.out`.
