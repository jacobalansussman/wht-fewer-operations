# s-note: how WAVE6-NOTE.md was made, what I re-ran, and its limits

11 October 2026, about 03:42 to 04:05 EDT, 25-minute box. Private. One agent; nothing reviewed, nothing in Lean, nothing published.
The note for the user is `waves/wave-06/NOTE.md`. Gate count (G) throughout.

**First line of the note, and of this report: nothing beats the textbook in order, and wave 6 has no record.**

## What I read

In full: `v-0.md`, `v-1.md` (the two critics whose objects carry the note), `WAVE5-NOTE.md` (for the numbering of the walls and
the form). Most of `s-cross.md` (sections 0, 1, 2, 4, 5, 6, 7). The verdict and section 1 of `v-2.md`; the opening of `u-5.md`.
The ten developments `u-0` to `u-9` only through the result summaries handed to me. Wave 7 (`x-*`) not at all: four of its
reports had landed and I did not open them, so the note says only that the wave is running.

## What I re-ran ("mine"), files in `s-note/`

`check.py` -> `check.out`, `gray.py` -> `gray.out`; whole numbers only; through light.py, 1 second each.

| check | result | agrees with |
|---|---|---|
| corners of `u-0-cornerssearch/` a8, a16, r32, r64_first, t128, counted by my own counter from the saved orders | 13, 30, 80, 239, 715 | u-0, v-1 |
| steps that are a single run, same files | 7 of 8, 13 of 16, 21 of 32, 20 of 64, 24 of 128; most runs in one step 2, 2, 3, 4, 7 | WAVE5-NOTE (13 of 16, 21 of 32); the fall at 64 and 128 is new here |
| steps between nested outputs, same files | all, except 1 of 128 at 128 points | u-0 ("all output steps join nested sets") |
| Gray order on both sides, 4 to 512 points | 7·3^(k-2) + 2 walking forward (9, 23, 65, ...), exactly 7·3^(k-2) with the output walk reversed (7, 21, 63, 189, 567, 1701) | v-1 has the first form; the second is 2 better and changes nothing |
| u-2's displayed bound (5/2)^k / (400 (1 + ln N)) | passes N at k = 43, 3N at 48, Yates at 59 | v-1's correction (u-2's 35, 41, 51 are for the exact sum, which I did not recompute) |

Nothing I ran contradicts a report.

## Choices made in the note

- The walls keep the numbering of the earlier notes (L1 to L13) and get two new numbers: L14 (one tree of sign vectors; it takes
  in the old L3, L9, L11) and L15 (one line through the cube). s-cross numbers its walls L1 to L5 differently; I did not use
  its numbers. The sealed-box lemma is filed under the old L2 (copies do not share).
- "Bounded or log N or undecided" for the corners: I wrote "not bounded, and faster than log N: a power of N", marked argued and
  read by one critic. The measured numbers alone would not decide it (the bound is empty below 2^35 points); the statement
  rests on v-1's reading of four hand arguments.
- I kept one sentence that could be over-read: "N·sqrt(log N) is left open, a saving of 5e-1". It is v-2's remark that the
  volume method cannot exclude it. It is the absence of a bound, and the note says so.
- Section 7's "what a linear program would have to be" joins three walls (volume, the floor, the sealed box). Each is argued in
  its own model; the conjunction is mine and is no more than the sum of its parts.

## Limits

- Twenty-five minutes. I matched statements across reports and critics; I re-derived nothing.
- Everything about the published unit in section 3 is u-5's, read from its summary and its first lines; no critic of this wave
  attacked u-5, u-3, u-4, u-7 or u-9. The note marks them computed because their authors ran them, not because a second
  program confirmed them.
- The note is about 3,600 words, a little over the three pages asked for; the walls section with its lists of labels is the
  long part.
