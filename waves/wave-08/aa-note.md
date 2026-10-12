# aa-note: how WAVE8-NOTE.md was made, and what it rests on

> Editor's note (11 October 2026): a later report corrected one figure. The "0.006" of a move per block that this report quotes for the published unit is a rate of the data arrays diluted 22 to 29 times ([ad-0](../wave-09/ad-0.md); line 10 (vi), "Corrections by the critics", in [the ninth note](../wave-09/NOTE.md)).

11 October 2026, 06:30 to about 06:45 EDT, one agent, 25-minute box. Private; nothing published, no git, no Lean.
The note for the user is `waves/wave-08/NOTE.md`.

**Nothing beats the textbook: no circuit over the rationals below a known count, no growth law below N log N beyond the
published one, nothing of the 1e-1 kind, no linear size.** The note says so in its first line.

Marks here: [read] = in a file I opened; [ran] = `aa-note/check.py` (exact fractions; floats for the roots of the price
law), output `aa-note/check.out`; [not checked] = taken from a result summary.

## What I read

- In full: `aa-cross.md`, `ac-0.md`, `ac-2.md`, `WAVE7-NOTE.md`.
- In part: `ac-1.md` (verdict, statement, the first three steps of its check), `ab-0.md` (summary and sections 1, 2 and
  the start of 3), `ab-8.md` (sections 0 to 5), `ab-1.md` (its twelve lines), the word lists of `ab-6.md`.
- Only as the result summaries handed to me: `ab-2`, `ab-3`, `ab-4`, `ab-5`, `ab-7`, and the rest of `ab-1` and `ab-6`.
  Every figure of the note that comes from these is [not checked] by me.
- Not read: the published certificates, `x-6`, the avenues studies, the floor note, and `ad-5.md` (ninth wave, landed
  while I wrote; I saw its title only: "the quadric is the cheapest known member of its family").

## What I recomputed [ran]

1. Adding-only law N (k - 1 - floor(k/2)/2): 2, 12, 32, 96, 224, 576, 1280 for k = 2 to 8; per point 2, 3, 3.5 at 16,
   32, 64 points. Modulo-2 composition N (23k/32 - 1): 30 and 1216 at 16 and 256 points. Route through two transforms
   at the night's rate (2 T + N with T = 52, 128, 304): 120, 288, 672.
2. The bar as an exchange rate, m^e/(1 - e) - 1 for e = 0.1: 0.276, 0.384, 0.626, 0.778, 1.217 at m = 4, 9, 45, 110,
   1000. The published unit as quoted (0.095 moves saved per array over 16.5 blocks): 0.006. I did not open the
   certificates; that figure is quoted from `ab-1` and `x-6` through `aa-cross`.
3. Equal blocks: 2 blocks with 7.4 % skipped give 0.0998; 16.5 blocks with 0.21 % give 7.5e-4.
4. Order bound 1 + (2^(h-r) - 1)/(2^r - 1): 2, 3.33, 6, 2, 3.14, 5.43, 10, 3.07 at (4,2), (5,2), (6,2), (6,3), (7,3),
   (8,3), (9,3), (9,4); 129 at (55,24); 33.06 at (23,9). At (9,1) it is 256, so "about 1 + 2^(h-2r)" is off by a
   factor 2 for thin ports; the note uses "about" only for fat ports.
5. Leak lemma c + 2 ceil(Rest/d): 7, 14, 30, 62, 126 at K = 4 to 64 (textbook 8 to 128; 1.5 K = 6 to 96).
6. `ab-1`'s sub-game ceilings 1 - ln(moves)/ln m: 0, 0.0466, 0.1584, 0.2351 at m = 3 to 6; tiny unit 0.1072.
7. Line sums of the plane, adding-only (N + sqrt N)(sqrt N - 1): 60, 504, 4080.

No circuit was replayed by me and no search was run. Nothing was run on the rented machine.

## Choices a reader should know about

- **Wall numbers** continue `WAVE7-NOTE.md` (L1 to L19). I added L20 (layers and formulas of convolutions; j-cross's
  wall C with `d-1`, `ab-0`, `ab-3`) and L21 (sharing in adding-only circuits). The grouping of wave 8 under old walls
  is `aa-cross`'s; I matched statements, not arguments.
- **L19 is restated.** Wave 7's note wrote "at least three blocks per array". `ab-1` argues that is not a floor and
  `ab-6` replays legal words with two blocks per array. The note records this as correction (i).
- **Section 3's table is `ab-8`'s table shortened** to nine rows, with `ac-2`'s two corrections (687, 206) and its
  hatch table summarised in one bullet. The rows for `ab-1` (no address maps, no phase letters) and `ab-6` are added
  by me from their summaries; they are different mechanisms from the exchange with ports and the table says so in
  its second column.
- **"Phase letter"** is explained in the note by my reading of `ab-1` section 6 (free multiplication by signs or
  powers of i that depend on the address). I did not open the engine's own definition. Marked in the note.
- **"Excluded"** always carries "inside one cost model" in the note, as `ac-2` asked.
- **Section 7's last sentence** says that in the engine's price law linear size would need one block per array and
  that the floor note argues this cannot occur. Both halves are [read] (`aa-cross` hybrid 3; `WAVE7-NOTE.md` idea B);
  I did not open the floor note.
- **The word "proved" is not used.** Every lemma is "argued", including the two that a critic read line by line.

## Limits

- Length: about 3,600 words, the same as the wave-7 note. That is more than three printed pages; the tables and the
  list of who hit each wall account for the excess. The first section alone (ten lines) is the short version.
- The eight experiments of section 6 are `aa-cross`'s list, unchanged. Two further small computations named by the
  critics are in idea F of section 4: the pair rule added to `ab-1`'s linear programme, and removal of terms that are
  only partly known.
- `ab-4`'s no-return statement and `ab-5`'s cut lemma were read by no critic; the note marks them "argued once,
  unreviewed; possibly Find and Boyar's 2013 theorem restated".

Files: `waves/wave-08/aa-note/check.py`, `check.out`.
