# ah-note: how WAVE10-NOTE.md was made, and its limits

11 October 2026, about 09:42 to 10:05 EDT, 25-minute box. Private. One agent; nothing reviewed, nothing in Lean, nothing published.
The note: `waves/wave-10/NOTE.md`. Arithmetic of mine: `ah-note/check.py`, `ah-note/check.out`.

**Nothing beats the textbook. The note says so in its first line.**

## What I read

In full: `WAVE9-NOTE.md` (for the format and the wall numbers), `ah-cross.md`, `ai-0.md`, `ai-1.md`, `ai-2.md`,
`ag-7-rankdial/TABLE.txt`. In part (headers, summaries, a few lines found by search): `ag-0.md`, `ag-1.md`, `ag-2.md`,
`ag-6.md`, `ag-8.md`, `ag-9.md`, `ae-cross.md`, `af-0.md`, `ad-6.md`. For `ag-3`, `ag-4`, `ag-5` I used only the result
summaries handed to me in the brief. I opened no certificate and replayed no circuit.

## What I computed (count (G), whole numbers, one run of one second through light.py)

The textbook count for "degree at most d at all 2^k cube points":
sum over i = 1..k of 2^(i-1) * (C(k-i, 0) + ... + C(k-i, d-1)).
[derived by me from Yates with only the inputs of size at most d kept; 13 controls agree: ag-7's nine entries at 4, 8, 16
points and ai-0's four textbook figures at 2,048, 8,192, 32,768 and 131,072 points.] From it: the table of section 2 at
16, 32, 64 points, the steps between degrees, and the cost "2 * gates(M) + N - rank" of the route M D M^T for the transform
up to multiples of 2^(d+1), with textbook pieces. At degree d = k the route gives N log2 N, as it must. Nobody built these
routes; they are counts. I did not compare them with x-1's circuits modulo 4.

## Where the note departs from ah-cross (the critics landed after it)

1. Hybrid 2's conclusion ("subset sums have no volume; only REPAY stands before O(N)") is reported as corrected by ai-2:
   the largest minor of Z is 2^(0.277 N sqrt(log2 N)) up to a factor 2^N, so +-1 circuits for Z need at least
   0.277 N sqrt(log2 N) - N gates. The note does not say that walls DEPTH/LEVELS were "removed"; it says they stop at free
   coefficients, which is the classical situation.
2. RELATION-LENGTH carries its field: modulo 2 as stated; over the rationals the weaker form of ai-1, three degrees later
   (twenty minutes old, unreviewed). "2N - o(N)" is given as 1.67 N to 1.96 N at c = 0 to 3.
3. ag-0's "2^2059 bits" is given as 2,060 address bits (2^2060 points), and "modulo 16 in 2N + o(N)" as 3N + o(N).
4. ag-4's 3N/2 for the transform is replaced by ai-1's two-line 2N - 2.
5. The class ledger is given with ai-2's caution that the weight depends on the letter chosen.
6. One idea is added to the "alive" list that ah-cross does not have: ai-2's gap for +-1 circuits for subset sums,
   between 0.277 N sqrt(log2 N) and (N/2) log2 N. It is the only item of the wave that would pass the bar (exponent 1/2)
   and it is marked as a guess with the evidence against it (every count sits at Yates; the lower figure is trivial
   below about 2^52 points).

## Walls: numbering

Continued from WAVE9-NOTE: L1+L2 repay, L4 depth (renamed levels), L16 step, L5 one class, L20 layers, L19 ports. New:
L23 relation length (it contains L22, two helpers) and L24 restriction of scalars. The lists "who hit it" for waves 1 to 9
are copied from WAVE9-NOTE (L4 with h-3 added, as ah-cross names it); I did not re-check them against the reports.

## Limits

- Six of the ten developments had no critic (ag-2, ag-3, ag-5, ag-6, ag-8, ag-9); ag-4 had one side remark. Their figures
  are quoted from their authors' summaries.
- ag-2's NO results are modulo 2 and rest, by its own words, on three results it did not re-run. ag-9's 8-point search is
  a random walk near the known circuit. ag-1's halving searches leave a halving by 8 or more and two halvings open.
- The note is about 24 KB, a little longer than WAVE9-NOTE; section 5 carries the long name lists the brief asked for.
- "Most surprising" is my choice, made after the critics: see the last sentence of the note's section 7 and line 4 of
  its section 1.
