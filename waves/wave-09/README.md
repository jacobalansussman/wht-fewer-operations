# Ninth wave: every report

> **Before you run a program from this folder.** These programs were written in a hurry for my own machines, and no person has reviewed them. Read a script before you run it, and start it from the top folder of the repository; [../WHERE.md](../WHERE.md) says how.

Ran 11 Oct, 06:21 to 07:57 (Eastern time). **Read [NOTE.md](NOTE.md) first**: it is the wave's own summary, written last. The reports below are what it was written from, in the order the work was done.

**Status.** Everything in this folder is the work of AI agents (Anthropic's Claude) that I directed. No person has reviewed it, and none of it is in Lean (a proof checker: a program that checks a proof step by step). The one exception is not in this folder: a circuit with at most (5/6)·N·log2 N + N operations for N = 8^j points, which grew out of the third wave's 8-point circuit, was proved correct in Lean afterwards, and that proof is in the `lean/` folder of this repository. The reports are a record of one night and are not rewritten. A later wave sometimes corrected an earlier one; where they disagree, believe the later one. The titles in the tables below are the agents' own words, not my claims.

**What is here.** A *report* is one agent's write-up. Its *folder* holds the programs that agent wrote and their small outputs, so that a number can be computed again. Larger files, compiled programs and binary data are not here: [LEFT-OUT.md](LEFT-OUT.md) lists them.

**Names.** The reports call this wave's note `WAVE9-NOTE.md`; here it is [NOTE.md](NOTE.md). They call each other by short labels such as `g-1` or `e2-0`: [../WHERE.md](../WHERE.md) says which wave each label is in, what the other names in the reports mean, and how to run a program again. When a report says "the user", it means me.

**Editor's notes, and three things that are true of every report.** Some reports begin with a block that starts "Editor's note (11 October 2026)". I put it there where a later report corrected the report, or where a statement about someone else's work could mislead. It is the only text in a report that is not the agent's. It adds two lines, so a line number that another report gives for that report is two too small. A report without a note is not thereby right: part 3 of [../LEADS.md](../LEADS.md) lists what was withdrawn. What the reports say about published work is as their authors marked it, mostly read through a tool that summarises, from an abstract, second hand or from memory, and nobody checked those statements against the sources, except where a report says "raw text"; [Earlier papers](../README.md#earlier-papers) says what the two papers that matter most contain. Many reports begin with "Private" or "nothing published, no git": that was their status on the night they were written, and an order to the agents not to publish anything themselves. I decided to publish them afterwards.


## 2. The picks

One agent, the curator, chose which ideas to develop and wrote a brief (a task description) for each.

| Report | Its own title | Folder of programs |
|---|---|---|
| [WAVE9-PICKS.md](WAVE9-PICKS.md) | WAVE9-PICKS: eight briefs, one per experiment of aa-cross section 6 | none |

## 3. Developments

One agent per brief, about an hour each.

| Report | Its own title | Folder of programs |
|---|---|---|
| [ad-0.md](ad-0.md) | ad-0 rateperblock: which blocks of the published unit carry its saving, and at what rate | [ad-0-rateperblock/](ad-0-rateperblock/) (20 files) |
| [ad-1.md](ad-1.md) | ad-1-linesums: all line sums of the finite plane, priced with free coefficients | [ad-1-linesums/](ad-1-linesums/) (23 files, 1 left out) |
| [ad-2.md](ad-2.md) | ad-2 two-deliveries: what a second cancelling gate is worth, and what a cut really is | [ad-2-twodeliveries/](ad-2-twodeliveries/) (39 files, 2 left out) |
| [ad-3.md](ad-3.md) | ad-3-straightenquadri: an exchange is "a sign convolution on half the points"; j = 2 at 16 points, and at 64 points exactly 4 with single flats and exactly 3 = k/2 with unions of three; it cannot stay bounded | [ad-3-straightenquadri/](ad-3-straightenquadri/) (46 files, 5 left out) |
| [ad-4.md](ad-4.md) | ad-4 flat-rank: the number of coset sums that add up to the transform's kernel is at least k (not k/2), exactly 4 at 16 points, at most 11 at 256; free row and column signs halve it (the 7-gate brick is 2 flats); it does not price gates | [ad-4-flatrank/](ad-4-flatrank/) (36 files, 1 left out) |
| [ad-5.md](ad-5.md) | ad-5 which-bent: the quadric is the cheapest known member of its family, and within a factor 2 of the dearest | [ad-5-whichbent/](ad-5-whichbent/) (4 files) |
| [ad-6.md](ad-6.md) | ad-6 two-helpers: the answer for degree 2 is "o(N)", by a family one can write in two lines | [ad-6-twohelpers/](ad-6-twohelpers/) (6 files) |
| [ad-7.md](ad-7.md) | ad-7 modulo 4: the 15-gate saving modulo 2 dies at 4, exactly and in every wiring; why; and what the second binary digit is made of | [ad-7-modulo4/](ad-7-modulo4/) (21 files, 4 left out) |

## 4. Recombination

One agent read every wave so far, put the results side by side and tried combinations of two ideas (the reports call them hybrids).

| Report | Its own title | Folder of programs |
|---|---|---|
| [ae-cross.md](ae-cross.md) | ae-cross: the nine waves side by side, four hybrids tried, and what to ask next | [ae-cross/](ae-cross/) (10 files) |

## 5. Critics

Three agents came last and attacked the strongest results.

| Report | Its own title | Folder of programs |
|---|---|---|
| [af-0.md](af-0.md) | af-0: criticism of ad-6's "N + o(N) for degree 2" | [af-0/](af-0/) (10 files) |
| [af-1.md](af-1.md) | af-1: the skeptic's report on ad-1's inequality R(N) >= T(N) - (q+1) T(q) | [af-1/](af-1/) (4 files) |
| [af-2.md](af-2.md) | af-2 skeptic: the pair-kill theorem holds and prices no gates; the 8-gate circuit's claim (i) holds at every size; its claim (ii) FAILS (the wiring is an identity of the class after all) | [af-2/](af-2/) (6 files, 1 left out) |

## 6. Side reports

How the wave's note was written.

| Report | Its own title | Folder of programs |
|---|---|---|
| [ae-note.md](ae-note.md) | ae-note: how WAVE9-NOTE.md was written | [ae-note/](ae-note/) (2 files) |
