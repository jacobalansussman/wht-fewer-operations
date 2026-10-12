# i-note: report on writing NOTE.md

10 October 2026, about 22:33 to 23:02 EDT (time box 25 minutes, overrun by a few). Private. Nothing reviewed, nothing in Lean.
Marks: [read] [ran] [derived] [guess].

## What was written

`waves/wave-01/NOTE.md`: the note for the user, six sections as briefed, about 2,450 words.
The list of all 77 ideas takes about a quarter of it, so at normal type it runs past the three pages asked for, to about three and a half.

## Sources

- [read] The brief's summaries of the eight developments (d-0 to d-7), the recombination (i-cross) and the three attacks (a-0, a-1, a-2).
  Of the reports themselves I opened: `a-2.md` (verdict, statement and proof, in full for sections 0 to 2), `PICKS.md` (opening, and the
  closing list of titles), the headings of all eight generator reports `i-*.md`, and the opening 1,500 to 3,000 characters of
  `e-0.md` to `e-5.md` and `j-*.md`. Everything else in the note rests on the brief's summaries, not on my reading of the files.
- [read] Idea numbers 0 to 76: taken from `PICKS.md` (the 48 listed there by title) and, for the 29 inside the picks, matched by me
  to the generator reports' own headings in order. The wild report has 13 headed ideas and 11 numbers; "solve, do not apply" and
  "batches are not additive" have none. The model report's "which variants are linear" has none either. This matching is mine and
  could be off by one in a place I did not notice.

## One thing I checked by hand, and one thing I ran

- [derived] I re-did the tight-wire argument of `a-2.md` section 2 line by line (levels in a gate differ by at most one; for each
  d < k at least N gates cross level d; they are different gates for different d). I found no gap, given the known equality case of the
  uncertainty inequality. That is one more reader, not a review. The note calls it "argued".
- [ran, exact integers, `i-note/replay21.py`, output `i-note/replay21.out`, 1 s through light.py] An independent replay of the
  second wave's 8-point circuit `e-2-density/h8_21gates.txt` with my own parser: 21 gates, all 8 outputs equal the Walsh-Hadamard rows
  exactly. Wire profile (non-zeros in the inputs, non-zeros in the outputs): 15 of the 21 gate wires are tight; 6 are not:
  g14 (8, 4), g15 (8, 8), g16 (8, 4), g17 (8, 8), g25 (3, 8), g27 (8, 3). So the circuit that went one below the previous count has
  six over-spread wires, two of them full on both sides. I did not compute the slack sum of `a-2.md` section 6 for it.

## Judgment calls in the note

- Alive ideas: I listed four (mirror basis, copies that share, over-spread wires as material, limits). The brief's developments
  called only `border` "alive"; the other three come from the recombination's key question, d-6's growth law and a-2's slack form.
  C (over-spread wires) and its link to A are my own reading [guess where marked].
- I carried all the critics' corrections into a paragraph "Taken back by the critics", including the one that weakens the
  recombination's "most surprising" (the squares tie is the same circuit, not independent evidence).
- I did not write "proved" anywhere, including for W3.
- The second wave (e-0 to e-7, j-*) is outside this job. I used two of its results because they bear directly on the alive ideas
  (the 21-gate circuit; e-1's greedy run of the mirror experiment: 26 + 26 + 6 = 58 at 16 points) and said so. `e-6.md` had landed
  but I did not open it; `e-7` had no report yet.

## Limits

- No literature was read by me tonight. "Known" and "not found in a short search" in the note are the critics' words.
- The next-hour experiments in section 2 are proposals. For A, whether d-0's exhaustive searcher reaches 16 wires and 20 to 26 gates
  is untested [guess: it does not without new pruning]. For B and D the experiments are my suggestions, not the developers'.
- "Lower bound 20" for six mirror forms is the recombination's hand count; e-1's floor 46 for the whole program agrees with it
  (46 - 6 = 40 = 20 + 20) but neither was machine-checked.
