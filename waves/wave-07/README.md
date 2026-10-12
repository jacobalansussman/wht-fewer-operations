# Seventh wave: every report

> **Before you run a program from this folder.** These programs were written in a hurry for my own machines, and no person has reviewed them. Read a script before you run it, and start it from the top folder of the repository; [../WHERE.md](../WHERE.md) says how. In this wave, `z-0/remote.sh` and `x-3-boxrelations/rs.sh` reached a rented machine; they now only print a message and stop.

Ran 11 Oct, 03:15 to 05:14 (Eastern time). **Read [NOTE.md](NOTE.md) first**: it is the wave's own summary, written last. The reports below are what it was written from, in the order the work was done.

**Status.** Everything in this folder is the work of AI agents (Anthropic's Claude) that I directed. No person has reviewed it, and none of it is in Lean (a proof checker: a program that checks a proof step by step). The one exception is not in this folder: a circuit with at most (5/6)·N·log2 N + N operations for N = 8^j points, which grew out of the third wave's 8-point circuit, was proved correct in Lean afterwards, and that proof is in the `lean/` folder of this repository. The reports are a record of one night and are not rewritten. A later wave sometimes corrected an earlier one; where they disagree, believe the later one. The titles in the tables below are the agents' own words, not my claims.

**What is here.** A *report* is one agent's write-up. Its *folder* holds the programs that agent wrote and their small outputs, so that a number can be computed again. Larger files, compiled programs and binary data are not here: [LEFT-OUT.md](LEFT-OUT.md) lists them.

**Names.** The reports call this wave's note `WAVE7-NOTE.md`; here it is [NOTE.md](NOTE.md). They call each other by short labels such as `g-1` or `e2-0`: [../WHERE.md](../WHERE.md) says which wave each label is in, what the other names in the reports mean, and how to run a program again. When a report says "the user", it means me.

**Editor's notes, and three things that are true of every report.** Some reports begin with a block that starts "Editor's note (11 October 2026)". I put it there where a later report corrected the report, or where a statement about someone else's work could mislead. It is the only text in a report that is not the agent's. It adds two lines, so a line number that another report gives for that report is two too small. A report without a note is not thereby right: part 3 of [../LEADS.md](../LEADS.md) lists what was withdrawn. What the reports say about published work is as their authors marked it, mostly read through a tool that summarises, from an abstract, second hand or from memory, and nobody checked those statements against the sources, except where a report says "raw text"; [Earlier papers](../README.md#earlier-papers) says what the two papers that matter most contain. Many reports begin with "Private" or "nothing published, no git": that was their status on the night they were written, and an order to the agents not to publish anything themselves. I decided to publish them afterwards.


## 2. The picks

One agent, the curator, chose which ideas to develop and wrote a brief (a task description) for each.

| Report | Its own title | Folder of programs |
|---|---|---|
| [WAVE7-PICKS.md](WAVE7-PICKS.md) | WAVE7-PICKS: ten briefs for developers (one hour each, heavier searches allowed) | none |

## 3. Developments

One agent per brief, about an hour each.

| Report | Its own title | Folder of programs |
|---|---|---|
| [x-0.md](x-0.md) | x-0 twojobs: can one gate both join inputs and carry volume? | [x-0-twojobs/](x-0-twojobs/) (47 files, 9 left out) |
| [x-1.md](x-1.md) | x-1 digits: the cost of binary digit j of the transform is N x [P(at least j heads) + P(at least j+1 heads)] in k fair tosses; the top half of the digits is free, the bottom half costs 2N each; the bottom d digits ARE the transform at its lightest outputs, where the volume count is silent and the only proven floor is 2N | [x-1-digits/](x-1-digits/) (26 files) |
| [x-2.md](x-2.md) | x-2 floorhatch: the floor's three hypotheses are one ("a clean cut"); the term N/2 + 1 survives every hatch and the factor 2 does not; no hatch wire saved a gate at 8 points | [x-2-floorhatch/](x-2-floorhatch/) (95 files, 1 left out) |
| [x-3.md](x-3.md) | x-3 boxrelations: when can a transform used as a box be shared? | [x-3-boxrelations/](x-3-boxrelations/) (43 files, 21 left out) |
| [x-4.md](x-4.md) | x-4 thirdturn-basis: the 120-degree rotation in its own basis is the half transform; what it turns into is "how many running-sum passes does a transform need" | [x-4-thirdturnbasis/](x-4-thirdturnbasis/) (16 files) |
| [x-5.md](x-5.md) | x-5 weightedz: the change of basis is a k-pass butterfly network again, by an exact identity; what it turned into | [x-5-weightedz/](x-5-weightedz/) (19 files) |
| [x-6.md](x-6.md) | x-6 unitasbox: the relation the published unit uses, and the growth law it allows | [x-6-unitasbox/](x-6-unitasbox/) (20 files) |
| [x-7.md](x-7.md) | x-7-rotate120: two mirrors cost what one transform costs, by a two-line lemma; what a pair really is, and where it could stop being additive | [x-7-rotate120/](x-7-rotate120/) (17 files) |
| [x-8.md](x-8.md) | x-8 nearlydependent: I pumped; can I spend? No. A landing's entropy is bounded by its volume, and the pump's moves make none | [x-8-nearlydependent/](x-8-nearlydependent/) (20 files, 3 left out) |
| [x-9.md](x-9.md) | x-9 growinghubs: a hub's coefficient is forced to +1 or -1; every other value costs N/2 more gates per level, and there is a coefficient-free reason | [x-9-growinghubs/](x-9-growinghubs/) (22 files) |

## 4. Recombination

One agent read every wave so far, put the results side by side and tried combinations of two ideas (the reports call them hybrids).

| Report | Its own title | Folder of programs |
|---|---|---|
| [w-cross.md](w-cross.md) | w-cross: the seven waves side by side, four hybrids tried, and what to ask next | [w-cross/](w-cross/) (27 files) |

## 5. Critics

Three agents came last and attacked the strongest results.

| Report | Its own title | Folder of programs |
|---|---|---|
| [z-0.md](z-0.md) | z-0: the height lemmas (x-0 lemmas 1 to 3, x-2 section 4.2, x-8's bridge), criticised | [z-0/](z-0/) (16 files) |
| [z-1.md](z-1.md) | z-1: criticism of x-6's growth law and caps for the published mechanism | [z-1/](z-1/) (9 files) |
| [z-2.md](z-2.md) | z-2: the two statements that close a model for linear size, and the two short lemmas, attacked | [z-2/](z-2/) (14 files) |

## 6. Side reports

How the wave's note was written.

| Report | Its own title | Folder of programs |
|---|---|---|
| [w-note.md](w-note.md) | w-note: how the seventh-wave note was made | [w-note/](w-note/) (2 files) |
