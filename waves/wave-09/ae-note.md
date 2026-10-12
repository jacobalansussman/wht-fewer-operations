# ae-note: how WAVE9-NOTE.md was written

11 October 2026, 07:50 to about 08:00 EDT, one agent, 25-minute box. Private. Nothing in Lean, nothing published, no git.
The note for the user is `waves/wave-09/NOTE.md`.

**First line of the note, and of this report: nothing beats the textbook. No circuit below a known count, no growth law below N log N beyond the published one, nothing of the 1e-1 kind, no linear size.**

## What I read

- In full: `WAVE8-NOTE.md` (as the model for the format and for the wall numbers), `ae-cross.md`.
- In part: `ad-0.md` sections 0 to 3 and the passages on the two-shear what-if (lines 218 to 230, 258 to 268); `ad-1.md` sections 0 to 2; `af-0.md` sections 1 and 2; `af-1.md` sections 1 to 4; `af-2.md` sections 1 to 3; the head of `WAVE10-PICKS.md`.
- Only as the summaries handed to me: `ad-2`, `ad-3`, `ad-4`, `ad-5`, `ad-6`, `ad-7`.
- Not read: the programs and outputs of any of them; the certificates; OpenAI's files.

## What I recomputed (`ae-note/check.py`, `ae-note/check.out`, run through light.py, 1 second)

- The bar per block, 1 − β^(e/(1−e)) at e = 0.1: 7.41 %, 11.49 %, 16.37 %, 34.49 %, 0.25 % (floats). Agrees with `ad-0`.
- The bar per single-move block, m^e/(1−e) − 1: 0.626, 0.722, 0.778 at m = 45, 80, 110 (floats). Agrees.
- The fourth result's rates from `ad-0`'s exact counts: 480/3,810 = 0.126; 480/2,850 = 0.168; unit 120/20,830 = 0.0058; copies −9. Agrees. I did not open the certificates.
- The cascade's factor: 4.33 × 1.20 × 3.74 × 4.00 = 77.7, and 6.82e-2 / 8.7625e-4 = 77.8.
- Line sums, count (G): additions (N + q)(q − 1) = 60, 504, 4,080; through the transform T(N) + (q + 1) T(q) = 87, 475, 2,484 with the night's counts 7, 19, 52, 304, 1,600; per point 5.44, 7.42, 9.70; the targets T(N) − (q + 1) T(q) = 17, 133, 716. Agrees with `ad-1` and `af-1`. The exact per-point figure is (9/8) k + 1/2 plus a term that shrinks like k/√N, so "(9/8) log2 N + 1/2" is written with "about".
- `af-2`'s family 2 N log2 N − 3N + 4 = 8, 28, 84, 228, 580, 1,412. Agrees.

I replayed no circuit.

## Where the note departs from the recombination, and why

The three critics landed after `ae-cross` and after `WAVE10-PICKS`. The note follows the critics:

1. `ae-cross` line 1 says wave 9 "closed" the line-sum relation. `af-1`: the inequality is the wave-8 relation with one term moved across, it was already in wave 1 (`d-1` section 4), and it gives no number because no lower bound on the transform is known. The note says "not an easier problem, not closed".
2. `ae-cross` hybrid 1 prices the transform modulo 8 at 2N + o(N). `af-0`: turning a circuit round changes the count by (outputs − inputs), so that route gives 3N + o(N). The note says so, and section 4 A states the ladder question without the 2N.
3. `ae-cross` calls its 8-gate circuit the first circuit from outside the class. `af-2` gives explicit coefficients for every kernel with p, q, r non-zero. The note withdraws it, and says that experiment 8 has lost its first specimen.
4. `ad-4`'s "2 log2 N flats in the doubled class" fails with free row and column signs (`af-2`). The note says the number of flats does not price gates.

Two readings are mine and are marked as readings: that the single-move rate 0.63 understates the distance for the data arrays' real blocks (it is `ad-0`'s own remark, and I put its two figures 1.5 and 3.8 in the table); and the last sentence of section 7 (every circuit tested so far works for every kernel, so none of those uses what only the transform has). The census of all the night's best circuits has not been run; the note says "the circuits tested".

## Limits

- `ad-0`, `ad-2`, `ad-3`, `ad-5` and `ad-7` had no critic. Everything quoted from them is their authors' word. In particular the table of section 2 rests on `ad-0`'s replay of the certificates' block lists, and on `x-6`'s "ports of at most a third of a stage", both unreviewed.
- Wall numbers L1 to L21 are taken from `WAVE8-NOTE.md`; the lists of who hit each wall in waves 1 to 8 are copied from there, not re-derived. I mapped `ae-cross`'s REPAY, STEP, DEPTH, LAYERS to L1 + L2, L16, L4, L20; `ae-cross` itself says that calling the five "step" lemmas one wall is a reading. L22 (two helpers) is a new number of mine.
- The note is about 4,000 words, a little longer than `WAVE8-NOTE.md`; the lists of labels in section 5 account for most of the difference.
- Section 6 lists the eight experiments of `ae-cross`. Wave 10 runs them as ten briefs (the halving experiment split in two, plus constants that are not rational), written before the critics landed.
