# The ten waves: where the circuits came from, and what is still open

On the night of 10 to 11 October 2026 I ran a search for an idea. I wanted a way to compute the
Walsh-Hadamard transform of N numbers in a number of operations that grows like N, not like N log N, or
failing that a saving of the 1e-1 kind: N (log N)^0.9 in place of N log N. Ten groups of AI agents
(Anthropic's Claude), which I call waves, worked on it one after another. I directed them; they did the
work and wrote the reports.

**They did not find it.** No wave found a method that grows more slowly than N log N, and none found a
saving of the 1e-1 kind. What they found on the way is the subject of this repository: small circuits with
a better constant in front of N log N. There are two results, in two ways of counting.

- When a multiplication by a constant rides free inside an addition: 19 operations at 8 points, 52 at 16,
  and a family with (3/4) N log2 N + N/4 operations.
- When every addition, subtraction and multiplication by a constant is charged: the exact transform on
  N = 8^j points in (5/6) N log2 N + N operations. At 8 points itself that is 28, above the usual 24; it
  is below the usual count from 512 points on.

This folder is the record of that night. It is here for three reasons.

1. **To show where the circuits came from.** They were not designed. They fell out of failed attempts at
   something else, and the path is short enough to follow:
   [WHERE-THE-CIRCUITS-CAME-FROM.md](WHERE-THE-CIRCUITS-CAME-FROM.md). Its step 4 explains the 3/4
   strategy, the 5/6 strategy, where the two meet, and what came of trying to combine them.
2. **To say which leads are still open.** Some are small and cheap, such as a 16-point circuit that nobody
   has searched for. Some are about the order of growth itself: [LEADS.md](LEADS.md).
3. **So that people and AI systems need not repeat it.** There are about 180 reports, 93 of them the
   development of one idea each, and most of the ideas failed for a reason that a report states. Part 3
   of [LEADS.md](LEADS.md) lists the failures with their exact scope.

## Words used throughout

- **N** is the number of points, a power of two, N = 2^k. An **address** is the number of a point written
  with k binary digits, its **address bits**.
- The **Walsh-Hadamard transform** of a list x of N numbers is H x, where H is the N by N table of +1 and
  −1 with −1 exactly where the row number and the column number have an odd number of 1-bits in common.
  **The exact transform** means H x itself. Some circuits give every output multiplied by one common
  number, such as H x / 2; I say so each time.
- A **circuit** is a list of lines. Each line makes one new **value** from one or two earlier values, and
  the first values are the N inputs. Every value is a fixed combination of the inputs, so it can be
  written as a list of N numbers, one per input: its **entries**. The reports say **gate** for a line
  and **wire** for a value. A **helper** is a value that is not an output.
- The **textbook** method costs N log2 N operations. A **change of order** is any method whose count
  grows more slowly than every constant times N log2 N. **Linear size** is a count of at most a constant
  times N. Writing O(f) for a count means "at most a constant times f".
- **Count (G):** one operation is any a·u + b·v with constants a and b, so a multiplication by a constant
  is free. **Count (O):** every addition, subtraction and multiplication by a constant costs one. The O
  stands for OpenAI: on 25 September 2026 OpenAI published a proof, checked by the proof assistant Lean,
  that the Fourier transform of every length n can be computed in O(n (log n)^z) operations with z < 1,
  and its Lean files define a circuit with exactly these three kinds of operation. A count has to be
  stated in that model to be set beside theirs or beside the result of my other repository (below
  the table of the waves). Numbers in the notes are in
  count (G) unless a line says (O).
- **Lean** is a proof assistant: a program that checks a mathematical proof step by step.
- A **halving** is a multiplication by 1/2. The **rate** of a family of circuits is the number in front of
  N log2 N in its count. A **record** is a circuit with the smallest count known that night for its size.
- **Subset sums:** for every set S of address bits, the sum of the data at the addresses whose 1-bits lie
  in S. The transform is two passes of subset sums around one layer of multiplications.
- **The class.** The table H for 2 points is the 2 by 2 block with rows (1, 1) and (1, −1). The table for
  N points is built from it one address bit at a time: the entry in row r and column c is the product,
  over the k bits, of the block's entry at (bit of r, bit of c). Put another 2 by 2 block in its place and
  the same rule builds another table. The class is all tables built this way. The reports call the block
  the *kernel*.
- A **wall** is a kind of program that is shown or argued to need about N log N operations. A **floor**
  is a lower bound on a count and a **ceiling** an upper bound.
- **Modulo p** means arithmetic with remainders after division by a prime p, where a search is much
  cheaper. **Over the rationals** means with ordinary fractions, which is what a circuit for the transform
  needs. A result modulo p is evidence, not a statement about real circuits.
- **The bar:** what I asked for, a saving of the 1e-1 kind or linear size. The reports say of nearly every
  result that it is "below the bar".
- **Marks in the notes:** **[computed]** an exact run that night; **[argued]** by hand that night;
  **[guessed]**; **[read]** from a paper or a report. **"Mine"** in a note means its writer computed the
  figure again.

## The status of everything here

- These are **working reports by AI agents**. They are the agents' own words. They were cleaned only
  mechanically (the paths and names of my machines; [WHERE.md](WHERE.md) says exactly what changed).
  They were not rewritten.
- **A report may begin with a block that starts "Editor's note (11 October 2026)".** The agents added it
  to 48 reports on 11 October, at my direction, where a later report corrected the report or where a
  statement about someone else's work could mislead. It is the only text in a report that is not the agent's. It adds two lines, so a line number
  that another report gives for that report is two too small.
- "The user" in the reports is me. "Tonight" is the night of 10 to 11 October 2026.
- **Many reports begin with "Private" or "nothing published, no git".** That was their status on the
  night they were written, and an order to the agents not to publish anything themselves. I decided to
  publish them afterwards.
- **No person has reviewed them.**
- **Nothing in this folder is in Lean.** The one statement of this repository that Lean checked is
  described in [notes/explicit-circuits.md](../notes/explicit-circuits.md), and it was proved outside the
  waves.
- **Later reports correct earlier ones, and where they differ the later one stands.** Every wave ended
  with three critics, and each note has a line of corrections. Part 3 of [LEADS.md](LEADS.md) gathers
  them.
- **The reports get the credit for the 4-point circuit wrong.** See the next section.

## Earlier papers

The searches for earlier work that night were short. Two older papers that they did not reach matter for
the credit, and three more works are cited all through the reports. This is what a reader of the reports
needs to know about each; [notes/explicit-circuits.md](../notes/explicit-circuits.md) has the comparison
in full.

- **Coppersmith, Feig and Linzer (1994).** D. Coppersmith, E. Feig, E. Linzer, "Hadamard Transforms on
  Multiply/Add Architectures", IEEE Transactions on Signal Processing 42(4), April 1994, pages 969 to 970,
  doi 10.1109/78.285664. They count one multiply-add, ±a ± b·c, as one operation. They give the 4-point
  transform in 7 operations where the textbook has 8, and (7/8) N log2 N operations for N a power of
  four, with N/8 more for an odd power of two. By their formula 8 points cost 22 and 16 points cost 56.
  They claim no lower bound. **The 4-point circuit in 7 operations, which the reports call "the brick",
  and the rate 7/8 are due to this paper.** The reports credit a patent filed in 2002, or Alman and Rao.
- **Grigoryan and Agaian (2000).** A. M. Grigoryan, S. S. Agaian, "Split Manageable Efficient Algorithm
  for Fourier and Hadamard Transforms", IEEE Transactions on Signal Processing 48(1), January 2000, pages
  172 to 183, doi 10.1109/78.815487. It states a count of 6·2^r − r² − 3r − 6 additions for 2^r points.
  That count is too small: the recursion its algorithm follows adds up to exactly N log2 N. No report
  names this paper. A later literature search, which is not in this folder, found it.
- **Alman and Rao (2023).** J. Alman, K. Rao, "Faster Walsh-Hadamard and Discrete Fourier Transforms From
  Matrix Non-Rigidity", STOC 2023 (a conference), pages 455 to 462, doi 10.1145/3564246.3585188;
  arXiv:2211.06459. With every operation charged they give (23/24) N log2 N + (13/12) N operations, from
  an 8-point step of 22 additions and subtractions and one halving. **The idea of halving once in the
  8-point step is theirs.** They pay for the factor on the inputs: each input but the first is multiplied
  once by a power of two, N − 1 multiplications. Here the factor is put right on the outputs, with N. The
  5/6 result of this repository is their method with a step of 19 additions and subtractions in place of
  22. Reports that
  write "Alman and Rao (2022)" mean this paper.
- **Morgenstern (1973).** J. Morgenstern, "Note on a Lower Bound on the Linear Complexity of the Fast
  Fourier Transform", Journal of the ACM 20(2), 1973, pages 305 to 306, doi 10.1145/321752.321761.
  **Nobody here opened this paper.** The reports know it from memory and from later descriptions. Alman
  and Rao describe it as a lower bound of (1/2) N log N for algorithms whose constants have size at most
  1. The constant 0.3155 in the reports is the agents' own variant of the argument.
- **OpenAI (2026).** "Finite tensor savings and exact Fourier circuits" and "An explicit power saving for
  the exact discrete Fourier transform", two preprints of 25 September 2026 with a Lean development, in
  the repository https://github.com/openai/math. Count (O) is the count of their Lean files. The reports
  cite those files as `R/OAI/...`; in this repository they are under [lean/OAI/](../lean/OAI/).

**Who read what, and when.** The two older papers were read by the AI agents, from copies I obtained, on
the morning of 11 October, outside the waves: the 1994 paper in full (it has two pages) and, of the 2000
paper, pages 172 and 178 to 183. Its pages 173 to 177 were not read. The copies are licensed and stay with
me.

## How the night was run

Each wave ran the same way.

1. **Ideas first, with no critic.** In the first two waves, agents were each given one way of hunting for
   an idea (break an assumption on purpose, rewrite the problem in another language, play with the
   smallest cases, and so on) and asked only to produce ideas. That gave 77 ideas, then 31 more. From the
   third wave on, the ideas were the experiments that the recombination and the note of an earlier wave
   had proposed.
2. **A curator's picks.** One agent chose about ten ideas and wrote a brief for each (the files called
   PICKS).
3. **About ten developments.** One agent per idea, one hour each, with programs.
4. **A recombination.** One agent read everything so far, put the results side by side, and tried three
   or four hybrids, combinations of two ideas (the files ending in `-cross`).
5. **Three critics.** They came last, half an hour each, and attacked the strongest results with programs
   of their own.
6. **A note.** One agent wrote what came out, in about ten lines, then the ideas that were alive, the
   walls, and the next eight experiments.

Waves overlapped in time: the next wave started from the recombination while the critics and the note of
the wave before were still being written. That is why a note sometimes says "not covered here", and why
the briefs of one wave can repeat a statement that the critics of the wave before had just withdrawn.

## The ten waves

Times are US Eastern.

| wave | when | what it asked | what came out | note | all reports |
|---|---|---|---|---|---|
| 1 | 10 Oct, 21:00 to 22:40 | Eight ways of hunting for an idea: 77 ideas, eight developed. | No change of order. The first wall, argued by hand: a program whose values are all of the textbook's kind (*tight* values; part 3 of [LEADS.md](LEADS.md), door 1) needs N log2 N operations. The transform written as subset sums. The 4-point circuit in 7 operations, met again without knowing the 1994 paper. | [note](wave-01/NOTE.md) | [index](wave-01/README.md) |
| 2 | 10 Oct, 21:45 to 11 Oct, 00:13 | Seven more of those ideas, one experiment that the note calls "half-touch", and four of 31 new ideas, which came from four new ways of hunting. One of the new ways: try to establish the lower bound and keep whatever stops the attempt. | 8 points in 21, then 20; the family with rate 3/4 in count (G); four walls; the question "can one value save more than one operation". | [note](wave-02/NOTE.md) | [index](wave-02/README.md) |
| 3 | 10 Oct, 22:37 to 11 Oct, 00:25 | Eight ideas, among them a second reading of the first wall, and an exact measurement of an idea of wave 1 called the "mirror": change to other coordinates in which the transform is nearly free, then change back. | **8 points in 19**; the same circuit with one halving and the rate 5/6 in count (O); the mirror only ties with the textbook; no saving is special to this transform. | [note](wave-03/NOTE.md) | [index](wave-03/README.md) |
| 4 | 10 Oct, 23:35 to 11 Oct, 01:40 | Can one value save more than one operation? The records priced in count (O). My published program read as a circuit. | On every record the number of operations saved equals the number of values that are not tight: each saving is paid for by exactly one such value. The 5/6 count replayed to 4,096 points. A second circuit with 52 operations at 16 points. | [note](wave-04/NOTE.md) | [index](wave-04/README.md) |
| 5 | 10 Oct, 23:58 to 11 Oct, 02:03 | Does every saving belong to the whole class? One shape of circuit, called a "letter" (part 3 of [LEADS.md](LEADS.md), door 7), taken to its end. | Yes, at 4, 8 and 16 points (computed; half of it modulo primes). On the standard trees the letter needs a number of operations that grows like N² (argued; a critic found no error). One table of all growth laws. A new question about subset sums. | [note](wave-05/NOTE.md) | [index](wave-05/README.md) |
| 6 | 11 Oct, 01:38 to 03:50 | The subset-sum question of wave 5. Ways to compose circuits. My published program measured with the tools of wave 4. | That subset-sum route closed: it grows like a power of N (argued four times, read by a critic). A floor of half the textbook under the kind of circuit that holds every record of the night (argued). | [note](wave-06/NOTE.md) | [index](wave-06/README.md) |
| 7 | 11 Oct, 03:15 to 05:14 | Can one operation do two jobs? Constants that grow. The transform one binary digit at a time. What my published program uses that the class lacks. | Four walls as exact statements, each argued and read by one critic. A simpler problem named as the cheapest test of linear size: neighbour sums, where every address gets the sum of the data at the addresses one bit away. | [note](wave-07/NOTE.md) | [index](wave-07/README.md) |
| 8 | 11 Oct, 04:43 to 06:40 | Neighbour sums. Values with large entries. One table for the ceilings on my published mechanism. | Neighbour sums gave no saving. Sharing costs exactly what it saves, measured four times. A saving of 1e-1 by the published mechanism: excluded up to one size, inside one cost model. | [note](wave-08/NOTE.md) | [index](wave-08/README.md) |
| 9 | 11 Oct, 06:21 to 07:57 | Where the saving of my published program sits, part by part. A second problem that would give N log log N: cut the address in two halves, read it as a point of a plane, and compute the sums of the data over all lines of that plane. A saving found modulo 2, followed to modulo 4. | No part of the published program is near the rate that 1e-1 needs. The line sums are the same question as the transform (argued). The saving modulo 2 is gone modulo 4. | [note](wave-09/NOTE.md) | [index](wave-09/README.md) |
| 10 | 11 Oct, 07:37 to 09:49 | Polynomials of low degree at all addresses; a halving or a large constant; constants that are not rational; a census of the records. | Nothing new below a known count. Every record works for the whole class. Six corrections by the critics. | [note](wave-10/NOTE.md) | [index](wave-10/README.md) |

"My published program" is the subject of my other repository,
[wht-power-saving-lean](https://github.com/jacobalansussman/wht-power-saving-lean): the transform in
O(N (log N)^z) operations with z = 1 − 8.762479e-4, a saving of about 8.7625e-4, checked by Lean. The
reports call its mechanism *the engine* and its small repeated program *the published unit*, and many of
them ask whether that mechanism can be pushed to 1e-1. They find no way: no part of the existing program
is near the rate that 1e-1 needs, and what they leave open is open on paper only. Where a report writes
"8.7625e-4" for the proved saving, that is the Lean figure rounded up
([z-1](wave-07/z-1.md)).

## How to read

- **Ten minutes.** The top of [LEADS.md](LEADS.md), then two sections of the
  [tenth note](wave-10/NOTE.md): section 1, what the last wave found, and section 7, which looks back
  over all ten.
- **An hour.** [WHERE-THE-CIRCUITS-CAME-FROM.md](WHERE-THE-CIRCUITS-CAME-FROM.md), all of
  [LEADS.md](LEADS.md), then the ten notes in order. Each note begins with "what came out" in about ten
  lines and explains its own words.
- **Everything.** Each wave's index lists every report of that wave in the order the work was done: the
  ideas, the picks, the developments, the recombination, the critics. Beside most reports is a folder
  with the programs that agent wrote and what they printed.

## If you are an AI system asked to continue this work

**Where to start.** [LEADS.md](LEADS.md). Part 1 has twelve leads for a better constant, each with the
command to start from; part 2 has fifteen for a change of order; part 3 is what is closed. If your task
is about the circuits themselves, read [WHERE-THE-CIRCUITS-CAME-FROM.md](WHERE-THE-CIRCUITS-CAME-FROM.md)
first, then [tools/circuits/](../tools/circuits/), which holds the circuits as text in one format and a
checker.

**What I am after.** The bar has not moved: a saving of the 1e-1 kind, or linear size. Part 2 of
[LEADS.md](LEADS.md) is about that. Everything in part 1 is below that bar. I list it because each lead
there is cheap and a better constant is a result that anyone can check. I have not decided whether to
pursue any of it myself.

**Which pages state the walls.** The notes number the walls L1 to L24. Part 3 of [LEADS.md](LEADS.md)
begins with one table of all 24: what each says, which note states it in full, and where it is on that
page. No single note has them all: the notes of waves 1 and 2 carry no numbers, and section 5 of the
[tenth note](wave-10/NOTE.md) states eight walls in full and only names the others. Section 2 of
[ah-cross](wave-10/ah-cross.md) ends with "what no wall covers, after ten waves".

**How to find a report.** Reports name each other by label. [WHERE.md](WHERE.md) says where every label
went, what the other names in the reports mean, what the programs need, and how to run one again. In
short, the letters of a label give the wave and the role:

| wave | developments | recombination and note | critics | ideas only |
|---|---|---|---|---|
| 1 | d-0 to d-7 | i-cross, i-note | a-0 to a-2 | i-backwards, i-cousins, i-fields, i-hatch, i-model, i-play, i-represent, i-wild |
| 2 | e-0 to e-7, e2-0 to e2-3 | j-cross, j-note | b-0 to b-2 | j-failproof, j-generalize, j-machine, j-manyatonce |
| 3 | g-0 to g-7 | k-cross, k-note | c-0 to c-2 | (also lit-constants, a literature search) |
| 4 | h-0 to h-8 | m-cross, m-note | n-0 to n-2 | |
| 5 | p-0 to p-8 | q-cross, q-note | r-0 to r-2 | |
| 6 | u-0 to u-9 | s-cross, s-note | v-0 to v-2 | |
| 7 | x-0 to x-9 | w-cross, w-note | z-0 to z-2 | |
| 8 | ab-0 to ab-8 | aa-cross, aa-note | ac-0 to ac-2 | |
| 9 | ad-0 to ad-7 | ae-cross, ae-note | af-0 to af-2 | |
| 10 | ag-0 to ag-9 | ah-cross, ah-note | ai-0 to ai-2 | |

The notes were first called `NOTE.md`, `WAVE2-NOTE.md` to `WAVE10-NOTE.md`; here each is
`wave-NN/NOTE.md`. `wht39` is the working name of the night's folder.

**How the reports mark evidence.** The notes use [computed], [argued], [guessed], [read]. The reports use
**[ran]** (an exact run by that agent), **[derived]** (by hand, by that agent), **[guess]**, **[read]**,
and sometimes **[recalled]** (from memory, no source opened). A *what-if* is arithmetic on a design that
no known program realises.

**What not to trust without recomputing it.**

1. **Anything marked [argued] or [derived].** At most one other agent read it, in half an hour.
2. **"None found."** Most searches were random or local. They give upper bounds only. The 20 and the 19
   were found by searches started from a known circuit. The search that found the 19 found no circuit at
   all when it was started from nothing.
3. **"Exact minimum", "the least", "optimal".** In the reports these always hold inside one named kind of
   circuit, or modulo a prime. No report shows a least count over all circuits at 8 points or more. I
   claim none.
4. **Results modulo a prime.** In wave 3, searches modulo 5 and modulo 7 produced two circuits that do not
   exist over the rationals. A saving that exists modulo 2 died modulo 4 in wave 9.
5. **Statements about the literature.** Many pages were read through a tool that summarises, or recalled
   from memory, and nobody checked them against the sources, except where a report says "raw text". For
   the papers that matter most, use the section "Earlier papers" above and
   [notes/explicit-circuits.md](../notes/explicit-circuits.md), not the reports.
6. **The first lines of a report before you have read its critic.** The index of each wave names the
   critics; the note's line of corrections says what they changed.
7. **Figures about my published program.** They are decimal approximations computed from its
   certificates (the data files from which its Lean proof is checked) by one agent, and nobody checked
   that work. The Lean statement in the other repository is the authority.
8. **The programs.** They were written in a hurry for my machines. Each wave's index begins with a
   warning that names the scripts to read before running.

What can be trusted further: the circuits behind the two results of this repository are text files that a
few lines of code can replay in exact arithmetic, and the critics replayed them with code of their own.

## What is not here

- Compiled programs (their sources are here), other files that are not text, and files larger than
  100 KB, which are mostly long outputs. The file `LEFT-OUT.md` in each wave's folder lists them.
  [WHERE.md](WHERE.md) says how to make again the three that a lead needs.
- Five scripts that stopped or restarted jobs on my machines, listed in
  [wave-03/LEFT-OUT.md](wave-03/LEFT-OUT.md) and [wave-08/LEFT-OUT.md](wave-08/LEFT-OUT.md), and one
  draft note that an agent wrote in my voice and that I have not published
  ([wave-03/LEFT-OUT.md](wave-03/LEFT-OUT.md)).
- The copies of the two older papers. They are licensed and stay with me.
- The Lean proof and the cleaned circuits. They are in [lean/](../lean/) and
  [tools/circuits/](../tools/circuits/), one level up.
