# Eighth wave: every report

> **Before you run a program from this folder.** These programs were written in a hurry for my own machines, and no person has reviewed them. Read a script before you run it, and start it from the top folder of the repository; [../WHERE.md](../WHERE.md) says how. In this wave, `ab-0-neighboursums/rsh.sh` reached a rented machine; it now only prints a message and stops. Three scripts that stopped jobs are left out ([LEFT-OUT.md](LEFT-OUT.md)).

Ran 11 Oct, 04:43 to 06:40 (Eastern time). **Read [NOTE.md](NOTE.md) first**: it is the wave's own summary, written last. The reports below are what it was written from, in the order the work was done.

**Status.** Everything in this folder is the work of AI agents (Anthropic's Claude) that I directed. No person has reviewed it, and none of it is in Lean (a proof checker: a program that checks a proof step by step). The one exception is not in this folder: a circuit with at most (5/6)·N·log2 N + N operations for N = 8^j points, which grew out of the third wave's 8-point circuit, was proved correct in Lean afterwards, and that proof is in the `lean/` folder of this repository. The reports are a record of one night and are not rewritten. A later wave sometimes corrected an earlier one; where they disagree, believe the later one. The titles in the tables below are the agents' own words, not my claims.

**What is here.** A *report* is one agent's write-up. Its *folder* holds the programs that agent wrote and their small outputs, so that a number can be computed again. Larger files, compiled programs and binary data are not here: [LEFT-OUT.md](LEFT-OUT.md) lists them.

**Names.** The reports call this wave's note `WAVE8-NOTE.md`; here it is [NOTE.md](NOTE.md). They call each other by short labels such as `g-1` or `e2-0`: [../WHERE.md](../WHERE.md) says which wave each label is in, what the other names in the reports mean, and how to run a program again. When a report says "the user", it means me.

**Editor's notes, and three things that are true of every report.** Some reports begin with a block that starts "Editor's note (11 October 2026)". I put it there where a later report corrected the report, or where a statement about someone else's work could mislead. It is the only text in a report that is not the agent's. It adds two lines, so a line number that another report gives for that report is two too small. A report without a note is not thereby right: part 3 of [../LEADS.md](../LEADS.md) lists what was withdrawn. What the reports say about published work is as their authors marked it, mostly read through a tool that summarises, from an abstract, second hand or from memory, and nobody checked those statements against the sources, except where a report says "raw text"; [Earlier papers](../README.md#earlier-papers) says what the two papers that matter most contain. Many reports begin with "Private" or "nothing published, no git": that was their status on the night they were written, and an order to the agents not to publish anything themselves. I decided to publish them afterwards.


## 2. The picks

One agent, the curator, chose which ideas to develop and wrote a brief (a task description) for each.

| Report | Its own title | Folder of programs |
|---|---|---|
| [WAVE8-PICKS.md](WAVE8-PICKS.md) | WAVE 8 PICKS: nine briefs, one hour each | none |

## 3. Developments

One agent per brief, about an hour each.

| Report | Its own title | Folder of programs |
|---|---|---|
| [ab-0.md](ab-0.md) | ab-0 neighbour-sums: can the sum over the k neighbours of every address be had in O(N) gates? | [ab-0-neighboursums/](ab-0-neighboursums/) (58 files, 6 left out) |
| [ab-1.md](ab-1.md) | ab-1 fewer-blocks: what the engine's price really rewards, a ceiling table, and a floor that counts blocks | [ab-1-fewerblocks/](ab-1-fewerblocks/) (33 files, 3 left out) |
| [ab-2.md](ab-2.md) | ab-2 tallpool: the smallest tall wire that pays, and what the transform lacks | [ab-2-tallpool/](ab-2-tallpool/) (41 files, 4 left out) |
| [ab-3.md](ab-3.md) | ab-3 convolution-ladder: the map has two cheap ladders and one forced number, k/2; the "cheap control" of the brief is not cheap | [ab-3-convladder/](ab-3-convladder/) (51 files) |
| [ab-4.md](ab-4.md) | ab-4 z-cut: the pair argument reads on subset sums only in a tilted cut; what the plain cut gives instead is two exact statements: "Yates' count minus gates <= helper wires that straddle a cut", and "(N/2) log2 N for every circuit that never clears exactly the on-half of a wire" | [ab-4-zcut/](ab-4-zcut/) (16 files, 2 left out) |
| [ab-5.md](ab-5.md) | ab-5 cancellit: what is proved about subset sums and the cube with and without cancellation, and where the printed proof stops | [ab-5-cancellit/](ab-5-cancellit/) (32 files, 1 left out) |
| [ab-6.md](ab-6.md) | ab-6 chain-of-exchanges: arrays in a ring, shears shared between neighbouring exchanges | [ab-6-chainexchanges/](ab-6-chainexchanges/) (20 files, 3 left out) |
| [ab-7.md](ab-7.md) | ab-7 the transform in a row: the row is the cube plus carries, and every carry costs; the Pascal cousin is dearer than subset sums at every size tried and its distance from them grows by a factor log N per binary digit; the transform itself IS a convolution for an addition with carries (power series modulo 2), 8 to 256 points, but its longest row has at most 2 log2 N points and the route through it costs more than the textbook | [ab-7-transforminarow/](ab-7-transforminarow/) (23 files) |
| [ab-8.md](ab-8.md) | ab-8 reconcile-caps: one table for the three ceilings, a bound that ties them together, and the verdict on 1e-1 | [ab-8-reconcilecaps/](ab-8-reconcilecaps/) (46 files) |

## 4. Recombination

One agent read every wave so far, put the results side by side and tried combinations of two ideas (the reports call them hybrids).

| Report | Its own title | Folder of programs |
|---|---|---|
| [aa-cross.md](aa-cross.md) | aa-cross: the eight waves side by side, four hybrids tried, and what to ask next | [aa-cross/](aa-cross/) (16 files) |

## 5. Critics

Three agents came last and attacked the strongest results.

| Report | Its own title | Folder of programs |
|---|---|---|
| [ac-0.md](ac-0.md) | ac-0: criticism of ab-0's 15-gate circuit modulo 2 for one block of neighbour sums at 16 points | [ac-0/](ac-0/) (14 files, 3 left out) |
| [ac-1.md](ac-1.md) | ac-1: skeptic's report on ab-6's leak lemma | [ac-1/](ac-1/) (4 files) |
| [ac-2.md](ac-2.md) | ac-2: a skeptic's reading of ab-8's order bound and "first open width", with ab-1's pair rule | [ac-2/](ac-2/) (7 files) |

## 6. Side reports

How the wave's note was written.

| Report | Its own title | Folder of programs |
|---|---|---|
| [aa-note.md](aa-note.md) | aa-note: how WAVE8-NOTE.md was made, and what it rests on | [aa-note/](aa-note/) (2 files) |
