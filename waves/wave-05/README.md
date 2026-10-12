# Fifth wave: every report

> **Before you run a program from this folder.** These programs were written in a hurry for my own machines, and no person has reviewed them. Read a script before you run it, and start it from the top folder of the repository; [../WHERE.md](../WHERE.md) says how. In this wave, `p-1-letter16/jobB.sh`, `jobC.sh` and `jobD.sh` wait in a loop for another program to end. `p-1-letter16/rsh.sh` and `rcp.sh` reached a rented machine; they now only print a message and stop.

Ran 10 Oct, 23:58 to 11 Oct, 02:03 (Eastern time). **Read [NOTE.md](NOTE.md) first**: it is the wave's own summary, written last. The reports below are what it was written from, in the order the work was done.

**Status.** Everything in this folder is the work of AI agents (Anthropic's Claude) that I directed. No person has reviewed it, and none of it is in Lean (a proof checker: a program that checks a proof step by step). The one exception is not in this folder: a circuit with at most (5/6)·N·log2 N + N operations for N = 8^j points, which grew out of the third wave's 8-point circuit, was proved correct in Lean afterwards, and that proof is in the `lean/` folder of this repository. The reports are a record of one night and are not rewritten. A later wave sometimes corrected an earlier one; where they disagree, believe the later one. The titles in the tables below are the agents' own words, not my claims.

**What is here.** A *report* is one agent's write-up. Its *folder* holds the programs that agent wrote and their small outputs, so that a number can be computed again. Larger files, compiled programs and binary data are not here: [LEFT-OUT.md](LEFT-OUT.md) lists them.

**Names.** The reports call this wave's note `WAVE5-NOTE.md`; here it is [NOTE.md](NOTE.md). They call each other by short labels such as `g-1` or `e2-0`: [../WHERE.md](../WHERE.md) says which wave each label is in, what the other names in the reports mean, and how to run a program again. When a report says "the user", it means me.

**Editor's notes, and three things that are true of every report.** Some reports begin with a block that starts "Editor's note (11 October 2026)". I put it there where a later report corrected the report, or where a statement about someone else's work could mislead. It is the only text in a report that is not the agent's. It adds two lines, so a line number that another report gives for that report is two too small. A report without a note is not thereby right: part 3 of [../LEADS.md](../LEADS.md) lists what was withdrawn. What the reports say about published work is as their authors marked it, mostly read through a tool that summarises, from an abstract, second hand or from memory, and nobody checked those statements against the sources, except where a report says "raw text"; [Earlier papers](../README.md#earlier-papers) says what the two papers that matter most contain. Many reports begin with "Private" or "nothing published, no git": that was their status on the night they were written, and an order to the agents not to publish anything themselves. I decided to publish them afterwards.


## 2. The picks

One agent, the curator, chose which ideas to develop and wrote a brief (a task description) for each.

| Report | Its own title | Folder of programs |
|---|---|---|
| [WAVE5-PICKS.md](WAVE5-PICKS.md) | wht39 / ideas / WAVE5-PICKS: nine briefs for an hour each | none |

## 3. Developments

One agent per brief, about an hour each.

| Report | Its own title | Folder of programs |
|---|---|---|
| [p-0.md](p-0.md) | p-0 classtest: at 4 points no saving belongs to the transform alone; one belongs to other kernels; the transform's own show on weight-only data only; even the 52 with four-bit wires moves to other kernels | [p-0-classtest/](p-0-classtest/) (56 files, 1 left out) |
| [p-1.md](p-1.md) | p-1 letter16: one letter at 16 points, outside the family that gave 49 | [p-1-letter16/](p-1-letter16/) (41 files) |
| [p-2.md](p-2.md) | p-2 mirror64class: the mirror route on subset sums. The obstruction is gone, the count is not: 5/4 of Yates at every size reached; and everything except one table is linear | [p-2-mirror64class/](p-2-mirror64class/) (27 files) |
| [p-3.md](p-3.md) | p-3-hatch32: the 8 x 4 tie at 32 points is decided (empty), the tie moves to 16 x 2 and is decided too (empty) | [p-3-hatch32/](p-3-hatch32/) (18 files) |
| [p-4.md](p-4.md) | p-4 formula: the rule behind the 5 and the 13, what it gives in k, and the pattern that stops at 16 points | [p-4-formula/](p-4-formula/) (25 files, 3 left out) |
| [p-5.md](p-5.md) | p-5-unimodular: the member with no determinant floor, played; and what it turned into | [p-5-unimodular/](p-5-unimodular/) (18 files) |
| [p-6.md](p-6.md) | p-6-selftranspose: one tree, forwards and backwards, a matching in the middle | [p-6-selftranspose/](p-6-selftranspose/) (7 files) |
| [p-7.md](p-7.md) | p-7-twoletters: two letters are one letter at the square-root size; the 3/4 family is not two letters | [p-7-twoletters/](p-7-twoletters/) (18 files) |
| [p-8.md](p-8.md) | p-8 fibonacci: the third term is 45, the law is "four times, minus seven", and one letter is quadratic | [p-8-fibonacci/](p-8-fibonacci/) (56 files, 5 left out) |

## 4. Recombination

One agent read every wave so far, put the results side by side and tried combinations of two ideas (the reports call them hybrids).

| Report | Its own title | Folder of programs |
|---|---|---|
| [q-cross.md](q-cross.md) | q-cross: the five waves side by side, four hybrids tried, and what to ask next | [q-cross/](q-cross/) (22 files) |

## 5. Critics

Three agents came last and attacked the strongest results.

| Report | Its own title | Folder of programs |
|---|---|---|
| [r-0.md](r-0.md) | r-0: criticism of "h-1's second 52-gate circuit is two letters" | [r-0/](r-0/) (3 files) |
| [r-1.md](r-1.md) | r-1: criticism of the two hand proofs behind "one form per node" (p-1's floor, p-8's lemma) | [r-1/](r-1/) (8 files) |
| [r-2.md](r-2.md) | r-2: criticism of p-0's census at 4 points and of the weight-only gap | [r-2/](r-2/) (30 files, 1 left out) |

## 6. Side reports

How the wave's note was written.

| Report | Its own title | Folder of programs |
|---|---|---|
| [q-note.md](q-note.md) | q-note: report on writing WAVE5-NOTE.md | [q-note/](q-note/) (3 files) |
