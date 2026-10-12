# First wave: every report

> **Before you run a program from this folder.** These programs were written in a hurry for my own machines, and no person has reviewed them. Read a script before you run it, and start it from the top folder of the repository; [../WHERE.md](../WHERE.md) says how.

Ran 10 Oct, 21:00 to 22:40 (Eastern time). **Read [NOTE.md](NOTE.md) first**: it is the wave's own summary, written last. The reports below are what it was written from, in the order the work was done.

**Status.** Everything in this folder is the work of AI agents (Anthropic's Claude) that I directed. No person has reviewed it, and none of it is in Lean (a proof checker: a program that checks a proof step by step). The one exception is not in this folder: a circuit with at most (5/6)·N·log2 N + N operations for N = 8^j points, which grew out of the third wave's 8-point circuit, was proved correct in Lean afterwards, and that proof is in the `lean/` folder of this repository. The reports are a record of one night and are not rewritten. A later wave sometimes corrected an earlier one; where they disagree, believe the later one. The titles in the tables below are the agents' own words, not my claims.

**What is here.** A *report* is one agent's write-up. Its *folder* holds the programs that agent wrote and their small outputs, so that a number can be computed again. Larger files, compiled programs and binary data are not here: [LEFT-OUT.md](LEFT-OUT.md) lists them.

**Names.** The reports call this wave's note `NOTE.md`; here it is [NOTE.md](NOTE.md). They call each other by short labels such as `g-1` or `e2-0`: [../WHERE.md](../WHERE.md) says which wave each label is in, what the other names in the reports mean, and how to run a program again. When a report says "the user", it means me.

**Editor's notes, and three things that are true of every report.** Some reports begin with a block that starts "Editor's note (11 October 2026)". I put it there where a later report corrected the report, or where a statement about someone else's work could mislead. It is the only text in a report that is not the agent's. It adds two lines, so a line number that another report gives for that report is two too small. A report without a note is not thereby right: part 3 of [../LEADS.md](../LEADS.md) lists what was withdrawn. What the reports say about published work is as their authors marked it, mostly read through a tool that summarises, from an abstract, second hand or from memory, and nobody checked those statements against the sources, except where a report says "raw text"; [Earlier papers](../README.md#earlier-papers) says what the two papers that matter most contain. Many reports begin with "Private" or "nothing published, no git": that was their status on the night they were written, and an order to the agents not to publish anything themselves. I decided to publish them afterwards.


## 1. Ideas

Agents that only produced ideas. No critic took part at this stage.

| Report | Its own title | Folder of programs |
|---|---|---|
| [i-backwards.md](i-backwards.md) | i-backwards: read a linear program backwards from the goal | [i-backwards/](i-backwards/) (4 files) |
| [i-cousins.md](i-cousins.md) | i-cousins: the frontier among the Hadamard transform's cousins | [i-cousins/](i-cousins/) (3 files) |
| [i-fields.md](i-fields.md) | i-fields: what other fields did when they met this shape | [i-fields/](i-fields/) (2 files) |
| [i-hatch.md](i-hatch.md) | i-hatch: breaking the obstruction on purpose | [i-hatch/](i-hatch/) (10 files) |
| [i-model.md](i-model.md) | i-model: the cost model read like a lawyer and like a child | [i-model/](i-model/) (4 files) |
| [i-play.md](i-play.md) | i-play: smallest cases, played with and stared at | [i-play/](i-play/) (9 files) |
| [i-represent.md](i-represent.md) | i-represent: the transform in other languages, and what each one suggests | [i-represent/](i-represent/) (2 files) |
| [i-wild.md](i-wild.md) | i-wild: invert, exaggerate, combine | [i-wild/](i-wild/) (8 files, 1 left out) |

## 2. The picks

One agent, the curator, chose which ideas to develop and wrote a brief (a task description) for each.

| Report | Its own title | Folder of programs |
|---|---|---|
| [PICKS.md](PICKS.md) | wht39 / ideas / PICKS: eight ideas to develop for an hour each | none |

## 3. Developments

One agent per brief, about an hour each.

| Report | Its own title | Folder of programs |
|---|---|---|
| [d-0.md](d-0.md) | d-0-zeta: subset sums with subtraction, played on small exact cases | [d-0-zeta/](d-0-zeta/) (32 files, 2 left out) |
| [d-1.md](d-1.md) | wht39 / ideas / d-1-plane: all line sums of a finite plane | [d-1-plane/](d-1-plane/) (4 files) |
| [d-2.md](d-2.md) | d-2-letters: short non-commuting words in linear-cost letters | [d-2-letters/](d-2-letters/) (19 files, 12 left out) |
| [d-3.md](d-3.md) | d-3-mod4: what only the transform's own point has | [d-3-mod4/](d-3-mod4/) (8 files) |
| [d-4.md](d-4.md) | d-4-codes: self-dual codes, atoms from several codes, and the E8 door | [d-4-codes/](d-4-codes/) (6 files) |
| [d-5.md](d-5.md) | d-5-border: limits of cheap programs (Pick 6) | [d-5-border/](d-5-border/) (5 files) |
| [d-6.md](d-6.md) | d-6-excess: where the log is born | [d-6-excess/](d-6-excess/) (9 files) |
| [d-7.md](d-7.md) | d-7-spin: the symmetry-adapted basis, built and played with | [d-7-spin/](d-7-spin/) (6 files) |

## 4. Recombination

One agent read every wave so far, put the results side by side and tried combinations of two ideas (the reports call them hybrids).

| Report | Its own title | Folder of programs |
|---|---|---|
| [i-cross.md](i-cross.md) | i-cross: the eight developments put side by side, three hybrids tried, and what to ask next | [i-cross/](i-cross/) (11 files) |

## 5. Critics

Three agents came last and attacked the strongest results.

| Report | Its own title | Folder of programs |
|---|---|---|
| [a-0.md](a-0.md) | a-0: criticism of the object "Identity: one class, and the log-log middle" | [a-0/](a-0/) (6 files) |
| [a-1.md](a-1.md) | a-1: criticism of "Circuit" (i-cross Hybrid 3: the squares of the 4-point transform, 62 gates at 16 points) | [a-1/](a-1/) (9 files, 1 left out) |
| [a-2.md](a-2.md) | a-2: criticism of "tight wires tie" (i-cross W3) | [a-2/](a-2/) (9 files) |

## 6. Side reports

How the wave's note was written.

| Report | Its own title | Folder of programs |
|---|---|---|
| [i-note.md](i-note.md) | i-note: report on writing NOTE.md | [i-note/](i-note/) (2 files) |
