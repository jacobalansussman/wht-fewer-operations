# k-note: report on writing WAVE3-NOTE.md

2026-10-11, 00:19 to about 00:30 EDT, inside a 25-minute box. Private research: nothing published, no git, no Lean.
Marks: [read] in a file I opened tonight; [ran] an exact run of mine; [derived] by hand; [guess].

## What was written

`waves/wave-03/NOTE.md`: the note for the morning, in the seven sections asked
for, same layout and marks as `NOTE.md` and `WAVE2-NOTE.md`. About 2,600 words, between the lengths of the first two notes (2,459 and 2,914); that is more
than three printed pages, and I did not cut further because every cut left removed a number or a name from a wall's list.

Its first line says that nothing changes the order. It then reports what exists: the 19-gate circuit at 8 points (a constant),
the fact that this circuit and the 7-gate brick hold for the whole class of 2 x 2 kernels, the mirror number 24, and the
subset-sum identity.

## Sources

- [read in full] `WAVE2-NOTE.md` and `j-note.md` (layout, what the second wave already said),
  `g-4-zetalead/note-for-zeta-readers.md`, `g-0.md` sections 0, 6, 7, `WAVE5-PICKS.md` brief 9.
- [read, first 20 to 40 lines] `c-0.md`, `c-2.md`, `h-0.md`, `h-4.md`, `h-6.md`, `p-5.md`, `p-6.md`; the raw file
  `p-2-mirror64class/struct.out`; lines 738 to 744 of the README in the release tree.
- [read, single lines by search] `g-3.md`, `g-4.md`, `g-7.md` for five quoted figures (0.277, 112,000 bases, 23/24, Kennes,
  ceil(k/2) letters).
- For the eight developments, the recombination and the three attacks I used the summaries in my task text. I did not open
  `g-1.md`, `g-2.md`, `g-5.md`, `g-6.md`, `k-cross.md` or `c-1.md`. Any error in those summaries is now in the note.

## What I checked myself

[ran, exact fractions, `k-note/check.py`, output `k-note/check.out`, 4 seconds]

1. g-1's 19-gate circuit, typed from the gate list in my task text: 19 gates, and the computed 8 x 8 matrix is exactly H_8 in the
   natural order, every output with factor 1.
2. g-4's word Z = D(1,3/5) H D(1,-1/2) H D(1,1/3) H D(1,5/4), for k = 1 to 6: equal to the subset-sum matrix each time.
3. The brick identity. (a) For 200 random symmetric kernels, k (x) k = v v^T + det * P' exactly, as g-3 states it. (b) For 200
   random kernels with four non-zero entries, k (x) k minus a relabelling with scalings has rank one, as k-cross states it.
4. The mirror's 16 points (sign vectors of length 6 with an even number of minus signs, up to sign): 16 of them, every pair with
   inner product +-2 out of 6 (cosine 1/3), 120 pairs, 30 two-term vectors on the lines through pairs. These agree with g-0.

[derived, arithmetic only]

- The comparison of the two families in count (G). g-1's bricks give 19, 54, 132, 304, 736, 1,664, 3,648 at 8 to 512 points;
  e2-0's formula (3/4) N k + N/4 gives 20, 52, 128, 304, 704, 1,600, 3,584. So e2-0 is ahead from 16 points on, with a tie at 64.
  The note says this in line 2. I did not look for a mixture of the two.
- c-0's formula n k - n floor(k/3)/2 + n: 4,352 at k = 9; ties with the textbook at k = 6, 7, 8. So 512 is the first size below.
- 16 + 10 + 30 = 56; N + sqrt(N) + x = 20 + 4 = 24 at 16 points; 64 + 8 = 72; N - 2 + tau = 7, 19, 63 for tau = 5, 13, 49;
  2^(-0.1) = 0.933; 6049 / 8.7625e-4 = 6,903,281.

One slip of my own, caught: my first version of check 3 (b) subtracted the same signed swap with one common factor for every
kernel and reported "False". For a kernel that is not symmetric the relabelling carries row and column scalings that depend on
the kernel. With those the check passes on all 200.

## Things the user may want to know that are not in the task text

- **The 19 is not the record at 16 points or beyond.** g-0, g-1 and the recombination still say "56, the best known count" at
  16 points; e2-0's 52 (confirmed by critic c-1) is lower, and the 3/4 family is ahead of g-1's tensor products at every size
  from 16 points except 64. The note compares the mirror route's 56 with 52.
- **"Never perpendicular" is narrower than the recombination says.** It writes "holds for every kernel without a zero entry".
  k-cross ran four kernels. The raw output of the run now in progress (`p-2-mirror64class/struct.out`) shows 4 perpendicular
  pairs of 256 for [[1,1],[1,2]] at 16 points and none at 64 [read]. The note says "held for the four kernels tried".
- **The hatch brief is partly out of date.** The recombination's `hatch32` asks for the 8 x 4 case; critic c-2 argues that case
  is impossible and that 16 x 2 is the one left. The note's sections 4 D and 6 say 16 x 2.
- **Two meanings of "letter".** g-3's tree letter (about 4N gates; one letter never makes the transform from 8 points on) and
  k-cross's letter (a sum of rectangles over two trees; one makes the 8-point transform with 13 rectangles) are different
  families. The note calls the first "tree steps" and the second "sums of rectangles" and never uses the word letter alone.
- **A figure in the public README.** g-4 flagged line 742 ("log2 log2 n exceeds a/(1 - z), about 8e6"); with a = 6049 and
  8.7625e-4 the quotient is 6.90e6. The line carries two figures, "8e6 (c) [6e6]", and I did not work out which constants each
  uses. 6049 / 7.47e-4 is 8.1e6, so the first figure may date from an earlier saving [guess]. Worth one look before the next
  revision; I changed nothing in the release tree.
- **Kennes 1992 and Alman-Rao 2023 were not read at the source.** g-4 has Kennes as quoted by Kaski, Kohonen and Westerbaeck
  (2016); c-0 has the 23/24 "through a summarising reader, not the PDF by eye". The note says so in both places.

## Judgment calls

- Marks: [ran] became [computed], [derived] became [argued], [guess] became [guessed]. Nothing is called proved; g-6's
  "Theorem 1" and "Lemma A" appear as statements with the mark [argued].
- Section 2 calls the 6-dimensional eigenspace "the mirror", as g-0 does, and describes the reflection as "changes the data
  only along a 6-dimensional subspace", which is the accurate half of the picture for a reader who has not seen the reports.
- Section 4 has five ideas, not the eight of the recombination's list: I merged the two rectangle experiments (B), put the
  unimodular member and the symmetric circuits into section 6 with the first lines of their reports, since both reports
  already say what they turned into, and added E (a discount on many copies) because it is the only idea of the wave that
  comes with a number for the 1e-1 bar.
- Idea B quotes the fit tau = 2N - 3 from `WAVE5-PICKS.md` brief 9 and marks it [guessed: a fit]. Two points fit anything; I
  kept it because it is the one place tonight where a linear law is a stated, testable candidate.
- Wall lists: I joined the recombination's lists with those of `WAVE2-NOTE.md` (its U, M, C, S walls are L3, L4, L1, L2 here).
  The second wave's "commuting steps" wall is folded into L1 and L7.
- Section 6 lists the recombination's eight experiments under the names of the folders actually running (`p-0` to `p-7`);
  `letter16`, `formula` and `fibonacci` are the fifth-wave names for parts of `twoletters`, `exponent` and `tletter`.
- No odds anywhere. Section 7 is three sentences.

## Limits

- I opened five of the fifteen third-wave reports only in part and five not at all.
- The later waves (`h-*`, `p-*`) are quoted from first lines, marked [read], in three places: h-6 (the 3/4 family holds for
  every kernel), p-5, p-6. If their notes are written they supersede section 4 A and section 6.
- No literature was read by me.
- The note is longer than three printed pages.

## Files

`waves/wave-03/NOTE.md`,
`waves/wave-03/k-note.md`,
`waves/wave-03/k-note/check.py`,
`waves/wave-03/k-note/check.out`.
