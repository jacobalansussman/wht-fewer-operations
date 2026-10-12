# Sixth wave: every report

> **Before you run a program from this folder.** These programs were written in a hurry for my own machines, and no person has reviewed them. Read a script before you run it, and start it from the top folder of the repository; [../WHERE.md](../WHERE.md) says how.

Ran 11 Oct, 01:38 to 03:50 (Eastern time). **Read [NOTE.md](NOTE.md) first**: it is the wave's own summary, written last. The reports below are what it was written from, in the order the work was done.

**Status.** Everything in this folder is the work of AI agents (Anthropic's Claude) that I directed. No person has reviewed it, and none of it is in Lean (a proof checker: a program that checks a proof step by step). The one exception is not in this folder: a circuit with at most (5/6)·N·log2 N + N operations for N = 8^j points, which grew out of the third wave's 8-point circuit, was proved correct in Lean afterwards, and that proof is in the `lean/` folder of this repository. The reports are a record of one night and are not rewritten. A later wave sometimes corrected an earlier one; where they disagree, believe the later one. The titles in the tables below are the agents' own words, not my claims.

**What is here.** A *report* is one agent's write-up. Its *folder* holds the programs that agent wrote and their small outputs, so that a number can be computed again. Larger files, compiled programs and binary data are not here: [LEFT-OUT.md](LEFT-OUT.md) lists them.

**Names.** The reports call this wave's note `WAVE6-NOTE.md`; here it is [NOTE.md](NOTE.md). They call each other by short labels such as `g-1` or `e2-0`: [../WHERE.md](../WHERE.md) says which wave each label is in, what the other names in the reports mean, and how to run a program again. When a report says "the user", it means me.

**Editor's notes, and three things that are true of every report.** Some reports begin with a block that starts "Editor's note (11 October 2026)". I put it there where a later report corrected the report, or where a statement about someone else's work could mislead. It is the only text in a report that is not the agent's. It adds two lines, so a line number that another report gives for that report is two too small. A report without a note is not thereby right: part 3 of [../LEADS.md](../LEADS.md) lists what was withdrawn. What the reports say about published work is as their authors marked it, mostly read through a tool that summarises, from an abstract, second hand or from memory, and nobody checked those statements against the sources, except where a report says "raw text"; [Earlier papers](../README.md#earlier-papers) says what the two papers that matter most contain. Many reports begin with "Private" or "nothing published, no git": that was their status on the night they were written, and an order to the agents not to publish anything themselves. I decided to publish them afterwards.


## 2. The picks

One agent, the curator, chose which ideas to develop and wrote a brief (a task description) for each.

| Report | Its own title | Folder of programs |
|---|---|---|
| [WAVE6-PICKS.md](WAVE6-PICKS.md) | WAVE6-PICKS: ten briefs for one-hour developers | [s-pick/](s-pick/) (3 files) |

## 3. Developments

One agent per brief, about an hour each.

| Report | Its own title | Folder of programs |
|---|---|---|
| [u-0.md](u-0.md) | u-0 corners-search: the least number of corners of the subset-sum picture | [u-0-cornerssearch/](u-0-cornerssearch/) (17 files, 1 left out) |
| [u-1.md](u-1.md) | u-1 corners-theory: the corners of the subset-sum picture grow like a power of N above 1. A wall, with its reason. | [u-1-cornerstheory/](u-1-cornerstheory/) (12 files, 1 left out) |
| [u-2.md](u-2.md) | u-2 (onerun): can every output be its neighbour plus or minus ONE run of inputs? | [u-2-onerun/](u-2-onerun/) (37 files, 3 left out) |
| [u-3.md](u-3.md) | u-3 zletter: with a free tree on each side, subset sums cost 4, 8, 20, 52 rectangles, and the gate count lands on Yates' number (4, 12, 32) and then one above it (81) | [u-3-zletter/](u-3-zletter/) (111 files, 10 left out) |
| [u-4.md](u-4.md) | u-4 zdz: the transform as (subset sums) x (scalings) x (subset sums), read with the meters modulo 2 | [u-4-zdz/](u-4-zdz/) (60 files) |
| [u-5.md](u-5.md) | u-5 unit2adic: the published unit under the modulo-2 meter | [u-5-unit2adic/](u-5-unit2adic/) (20 files, 3 left out) |
| [u-6.md](u-6.md) | u-6 twotrees: two merge trees do not buy the order, and why; then the same idea moved to subset sums, where it meets a new wall | [u-6-twotrees/](u-6-twotrees/) (21 files, 4 left out) |
| [u-7.md](u-7.md) | u-7 quotient: the first useful Q gate. What a quotient can and cannot buy | [u-7-quotient/](u-7-quotient/) (16 files) |
| [u-8.md](u-8.md) | u-8 compose: composition laws for the excess, and a proof that it cannot go negative in the night's class | [u-8-compose/](u-8-compose/) (21 files) |
| [u-9.md](u-9.md) | u-9 checkerboards: every record circuit of the night belongs to one class (sign vectors on the cosets of one chain of subspaces); that class has the floor N - 1 + (N/2) log2 N; a wire that carries a 2 outside its own set breaks the floor modulo 4 | [u-9-checkerboards/](u-9-checkerboards/) (48 files, 2 left out) |

## 4. Recombination

One agent read every wave so far, put the results side by side and tried combinations of two ideas (the reports call them hybrids).

| Report | Its own title | Folder of programs |
|---|---|---|
| [s-cross.md](s-cross.md) | s-cross: the six waves side by side, four hybrids tried, and what to ask next | [s-cross/](s-cross/) (15 files) |

## 5. Critics

Three agents came last and attacked the strongest results.

| Report | Its own title | Folder of programs |
|---|---|---|
| [v-0.md](v-0.md) | v-0: the common floor of u-8 and u-9, checked | [v-0/](v-0/) (13 files, 2 left out) |
| [v-1.md](v-1.md) | v-1: the four proofs behind "one line through the cube", checked | [v-1/](v-1/) (10 files, 3 left out) |
| [v-2.md](v-2.md) | v-2: the box lemma, the two-call formula for reflections, and the volume bound for subset sums, checked | [v-2/](v-2/) (14 files) |

## 6. Side reports

How the wave's note was written.

| Report | Its own title | Folder of programs |
|---|---|---|
| [s-note.md](s-note.md) | s-note: how WAVE6-NOTE.md was made, what I re-ran, and its limits | [s-note/](s-note/) (6 files) |
