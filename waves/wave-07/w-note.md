# w-note: how the seventh-wave note was made

11 October 2026, about 05:05 to 05:30 EDT, 25-minute box. One agent. Private; nothing published, no git, no Lean.

**Product.** `waves/wave-07/NOTE.md` (120 lines, about the length of the sixth note).

**First line of the note: nothing beats the textbook.** No circuit below a known count, no growth law below N log N.

## What I read

- In full: `WAVE6-NOTE.md` (for form and wall numbers), `w-cross.md`, `z-0.md`.
- Most of: `z-1.md`, `z-2.md`.
- Parts: `x-0.md` sections 3 and 6; `x-8.md` section 0; `x-9.md` section 2.
- The ten wave-7 results, the recombination and the three attacks as handed to me in the brief.
- Not read: the other seven `x-*` reports themselves, waves 1 to 5 again, any program. Not opened: any circuit file.

## What I ran [ran, `w-note/check.py`, output `w-note/check.out`, whole numbers and fractions; floats only for logarithms]

Formulas only. No circuit was replayed.

- `x-1`'s digit law (digit 0 = N − 1 gates, digit j = N × [P(Bin ≥ j) + P(Bin ≥ j+1)]) gives 7, 18, 41, 88, 183, 374, 757 modulo 4, equal to 3N − k − 3; 23, 57, 130, 282, 593, 1223 modulo 8, equal to 5N − (k² + 5k + 10)/2; 63, 152, 346, 756, 1605 modulo 16; third digit 5, 16, 42, 99, 219, 466; and all digits together exactly N·k at 4 to 256 points. All of `x-1`'s printed numbers.
- `x-6`'s closed form: 0.0998, 0.1001, 0.0997 for (2 blocks, 7.4 %), (3, 11.5 %), (6, 18 %); 0.13195 for (2, 10 %), `z-1`'s enclosure.
- The height bound at 8 points: 15, 9, 8 for heights 1, 2, 3 (`z-0`'s numbers); it passes the trivial 2N − 2 at 2^10 points for height 2 by two gates.
- `x-4` lemma D: least r = 2, 2, 3, 4, 13, 128, 410, 4682, 61681 (`z-2`'s table).
- Adding-only neighbour sums: 2, 12, 32, 96, 224, 576, 1280, 3072, 6656 (`z-2`'s list).
- `x-9`'s family: 7, 20, 52, 128, 304 and 28, 76, 192, 464.

## Choices I made

- **Section 2 answers the brief's question as it stands and says where the brief assumed more than exists.** The brief asks what "the exact searches at 8 and 16 points" found. Only the 4-point searches are exhaustive without restriction; at 8 points there are walks, one exhaustive search with six wires fixed, and 54 annealing runs; at 16 points one walk of 164 circuits that its author says tells nothing. The note's table says this row by row.
- **Section 3's rate law is given twice**: what the argument allows (constant falling like 1 / log M, order unchanged) and what was measured (never fell). They do not contradict each other: the bound is silent at every size run.
- **Wall numbers continue the sixth note.** `w-cross` groups wave 7 under HEIGHT, COSTS ADD, DISTANCE and the door PORTS. I mapped them to L4, L1 + L2, a new L16, and line 8; and added L17 (flag passes), L18 (two-piece hubs), L19 (three blocks per exchange). Lists of who hit L1 to L15 before wave 7 are copied from `WAVE6-NOTE.md`, not re-derived.
- **Idea G (constants that are not rational) is in "alive" with no experiment behind it.** It comes from `z-0`'s correction (the height wall needs rational numbers; the cost model charges one unit for any complex constant). It is not among `w-cross`'s eight experiments. Marked as a guess that it is worth one.
- **The critics' corrections are in line 10 and override the reports where they differ**: `x-6`'s cap 0.098 (one sub-class only; 0.126 and 0.101 on paper at h = 7, r = 3), `x-9`'s floor (the 19 is outside its class), "any coefficients" (rational only), "a constant fraction of gates" (only an average is argued), and the figure 8.762479e-4.
- I wrote "argued", never "proved", including for statements the critics checked line by line.

## Limits

- I matched statements across reports; I checked no argument myself beyond the arithmetic above.
- The eighth wave (`ab-0-neighboursums` to `ab-7-transforminarow`) has folders with runs in them and no reports yet. The note says it is running and takes nothing from it.
- "No object of the night has more than two of these" in section 7 is `w-cross`'s reading (the second pass of subset sums has two, the published unit one); I did not test it against every circuit.
- Section 2's anomaly ("some size has a first tall wire that pays") assumes the published program's constants are rational. `z-0` flags that nobody checked.

Files: `waves/wave-07/w-note/check.py`, `check.out`.
