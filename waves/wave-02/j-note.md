# j-note: report on writing WAVE2-NOTE.md

2026-10-11, 00:03 to about 00:20 EDT, 25-minute box. Private research: nothing published, no git, no Lean.
Marks: [read] in a file I opened tonight; [ran] an exact run of mine; [derived] by hand; [guess].

## What was written

`waves/wave-02/NOTE.md`: the note for the morning, in the seven sections asked for, same layout and marks as the first wave's `NOTE.md`. About 2,900 words, which is some 18 % longer than `NOTE.md`; I did not cut further because every cut left removed a number.

Its first line says that nothing changes the order. It then reports the one object that beats the textbook by a constant: e2-0's family with (3/4) N log2 N + N/4 gates in count (G).

## Sources

- [read in full] `NOTE.md` (for layout and for what the first wave already said), `j-cross.md`, `j-failproof.md`, `j-generalize.md`.
- [read in part] `j-machine.md` section 2, `j-manyatonce.md` (take-away and ideas), `b-0.md` sections 4 to 9, `b-1.md` verdict and sections 5 to 7, `b-2.md` sections 4, 6, 7, 8, `e2-2.md` (head and the definition of fragmentation), `e2-0-pieces/slp_8.txt`.
- [read, first lines only] `g-0.md`, `g-1.md`, `h-3.md`, `h-7.md`, and the titles of `g-2` to `g-7` and `k-cross`. Used only in the paragraph "Not covered here".
- For the twelve developments (`e-0` to `e-7`, `e2-0` to `e2-3`) I used the summaries in my task text, not the reports themselves. Any error in those summaries is now in the note.

## What I checked myself

- [ran, exact fractions, `j-note/replay_slp.py`, output `j-note/replay_slp.out`] My own parser replays e2-0's count-(G) programs at 4, 8, 16, 32, 64 points: 7, 20, 52, 128, 304 gates, each equal to (3/4) N k + N/4; the outputs are exactly the N rows of H with factor 1; the only coefficient sizes are 1 and 2. ALL PASS. This is a fourth independent reader (after e2-0's own, j-cross's and b-0's).
- [derived] The 20 gates of `slp_8.txt` by hand, gate by gate, against the vectors in its comments: all 20 agree and the eight outputs are the eight Walsh rows.
- [derived] The identity of j-cross Hybrid 4, all 16 entries: for K = [[1,1],[1,tau]], K x K - u u^T with u = (1,1,1,tau) has exactly four non-zero entries, (0,3) and (3,0) equal to 1 - tau, (1,1) and (2,2) equal to tau - 1.
- [derived, arithmetic only] The formulas quoted: 37,888 gates at 4,096 points; 48,128 against 49,152 in count (O); the tie at 1,024; 60 and 352 for H x / sqrt N; 0.3155 = 1 / (2 log2 3); 2.111e-3 / 2.407 = 8.77e-4; 120 / 1,263 = 0.095; savings 1.5e-1 for (6, 7, 32) and 1.07e-1 for (5, 19, 80) from 1 - log(moves / arrays) / log(block size); the slack formula at rho = 3/4 (0.75) and at rho = 1/2 (N^(1/4) / 2.83, equal to 3 at N = 5,184); 4.45 sqrt(64) = 35.6.
- One small thing found: e-3's "4.45 sqrt(k) N" does not fit its own first figure (14.8 N at k = 16, where the formula gives 17.8 N); it fits from k = 64 on. The note quotes only the k = 64 figure.

## Judgment calls

- Marks: [ran] became [computed], [derived] became [argued], [guess] became [guessed]. Nothing is called proved; the developers' "Theorem A" and "corner theorem" appear as statements with the mark [argued].
- The first line says "nothing beats the textbook in order", because constants do beat it in count (G).
- I added a fifth wall, K (the clique lemma), to j-cross's four, marked "inside the engine only".
- Idea E (words of steps that do not commute, and the two identities with no circuit) is my grouping of mutations that several developers listed and nobody ran.
- "The 19-gate circuit must lie outside e2-0's class" is my inference [derived] from b-0's exhaustive search (no program of 19 gates or fewer inside the class) and g-1's first lines; I did not replay g-1's circuit.
- Section 4's last sentence ("a program with fewer than (1/2) N log2 N gates saves more gates than it has wires") is j-cross's argument restated; it assumes the published program reads as a circuit in count (G), which h-7's first lines say it does.
- Section 5 lists j-cross's eight experiments; the folders `h-0` to `h-7` show that seven of them were already running, with `h-3` an extra one (the record in OpenAI's count).

## Limits

- I did not open the twelve development reports or their folders, apart from e2-0's program files.
- The later waves (`g-*`, `h-*`, `k-cross`) are mentioned from their first lines only. If their notes are written, the 8-point record (19) and the count-(O) crossover (512 points) there supersede lines 2, 3 and 7 of this note.
- No literature was read by me; "no paper found" is the critics' short search.
- The note has no odds and no forecast; the phrase "the question that would tell the most" is j-cross's choice, which I kept after reading its section 8.

## Files

`waves/wave-02/NOTE.md`, `waves/wave-02/j-note.md`, `waves/wave-02/j-note/replay_slp.py`, `waves/wave-02/j-note/replay_slp.out`.
