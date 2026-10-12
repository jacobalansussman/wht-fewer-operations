# Second wave: every report

> **Before you run a program from this folder.** These programs were written in a hurry for my own machines, and no person has reviewed them. Read a script before you run it, and start it from the top folder of the repository; [../WHERE.md](../WHERE.md) says how. In this wave, `b-1/run2.sh`, `run3.sh` and `run4.sh` each start eight jobs in the background and do not wait for them, `b-1/run5_finish19.sh` starts three, the scripts `e-7-halftouch/batch1.sh` to `batch6.sh` start up to eight jobs each, `e2-3-drain/drain.c` uses every processor core, and `e2-0-pieces/deep.py` and `deepN.py` start as many processes as their argument says. `e2-0-pieces/rsh.sh` reached a rented machine; it now only prints a message and stops.

Ran 10 Oct, 21:45 to 11 Oct, 00:13 (Eastern time). **Read [NOTE.md](NOTE.md) first**: it is the wave's own summary, written last. The reports below are what it was written from, in the order the work was done.

**Status.** Everything in this folder is the work of AI agents (Anthropic's Claude) that I directed. No person has reviewed it, and none of it is in Lean (a proof checker: a program that checks a proof step by step). The one exception is not in this folder: a circuit with at most (5/6)·N·log2 N + N operations for N = 8^j points, which grew out of the third wave's 8-point circuit, was proved correct in Lean afterwards, and that proof is in the `lean/` folder of this repository. The reports are a record of one night and are not rewritten. A later wave sometimes corrected an earlier one; where they disagree, believe the later one. The titles in the tables below are the agents' own words, not my claims.

**What is here.** A *report* is one agent's write-up. Its *folder* holds the programs that agent wrote and their small outputs, so that a number can be computed again. Larger files, compiled programs and binary data are not here: [LEFT-OUT.md](LEFT-OUT.md) lists them.

**Names.** The reports call this wave's note `WAVE2-NOTE.md`; here it is [NOTE.md](NOTE.md). They call each other by short labels such as `g-1` or `e2-0`: [../WHERE.md](../WHERE.md) says which wave each label is in, what the other names in the reports mean, and how to run a program again. When a report says "the user", it means me.

**Editor's notes, and three things that are true of every report.** Some reports begin with a block that starts "Editor's note (11 October 2026)". I put it there where a later report corrected the report, or where a statement about someone else's work could mislead. It is the only text in a report that is not the agent's. It adds two lines, so a line number that another report gives for that report is two too small. A report without a note is not thereby right: part 3 of [../LEADS.md](../LEADS.md) lists what was withdrawn. What the reports say about published work is as their authors marked it, mostly read through a tool that summarises, from an abstract, second hand or from memory, and nobody checked those statements against the sources, except where a report says "raw text"; [Earlier papers](../README.md#earlier-papers) says what the two papers that matter most contain. Many reports begin with "Private" or "nothing published, no git": that was their status on the night they were written, and an order to the agents not to publish anything themselves. I decided to publish them afterwards.


## 1. Ideas

Agents that only produced ideas. No critic took part at this stage.

| Report | Its own title | Folder of programs |
|---|---|---|
| [j-failproof.md](j-failproof.md) | j-failproof: try to prove the lower bound, and keep what breaks each proof | [j-failproof/](j-failproof/) (21 files) |
| [j-generalize.md](j-generalize.md) | j-generalize: widen the problem until it is linear, then walk back | [j-generalize/](j-generalize/) (9 files) |
| [j-machine.md](j-machine.md) | j-machine: let the machine propose | [j-machine/](j-machine/) (44 files, 10 left out) |
| [j-manyatonce.md](j-manyatonce.md) | j-manyatonce: change what it means to compute, many arrays at once | [j-manyatonce/](j-manyatonce/) (18 files, 1 left out) |

## 2. The picks

One agent, the curator, chose which ideas to develop and wrote a brief (a task description) for each.

| Report | Its own title | Folder of programs |
|---|---|---|
| [WAVE2-PICKS.md](WAVE2-PICKS.md) | wht39 / ideas / WAVE2-PICKS: seven more ideas to develop for an hour each | none |
| [WAVE2-PICKS-B.md](WAVE2-PICKS-B.md) | wht39 / ideas / WAVE2-PICKS-B: four more ideas to develop for an hour each | none |

## 3. Developments

One agent per brief, about an hour each.

| Report | Its own title | Folder of programs |
|---|---|---|
| [e-0.md](e-0.md) | wht39 / ideas / e-0-ring: the transform as multiplication by one number | [e-0-ring/](e-0-ring/) (21 files) |
| [e-1.md](e-1.md) | e-1-vcycle: one half-size problem that is not a transform, between two cheap frames | [e-1-vcycle/](e-1-vcycle/) (28 files) |
| [e-2.md](e-2.md) | wht39 / ideas / e-2-density: the exponent as a density of outputs | [e-2-density/](e-2-density/) (52 files, 2 left out) |
| [e-3.md](e-3.md) | e-3 cutoff: a cheap wrong answer, then the tails | [e-3-cutoff/](e-3-cutoff/) (12 files) |
| [e-4.md](e-4.md) | e-4 `passes`: pay in running sums, not butterflies | [e-4-passes/](e-4-passes/) (26 files) |
| [e-5.md](e-5.md) | e-5-conserved: what "64" is made of, and the first gate that makes more | [e-5-conserved/](e-5-conserved/) (40 files) |
| [e-6.md](e-6.md) | e-6-shifts: transform N shifted copies at once and read the diagonal | [e-6-shifts/](e-6-shifts/) (15 files) |
| [e-7.md](e-7.md) | e-7-halftouch: one half-length call plus a sparse remainder | [e-7-halftouch/](e-7-halftouch/) (83 files, 2 left out) |
| [e2-0.md](e2-0.md) | e2-0-pieces: programs built from "an output restricted to a piece" | [e2-0-pieces/](e2-0-pieces/) (35 files) |
| [e2-1.md](e2-1.md) | e2-1 `dictionary`: route through a non-abelian group and choose the free bijection | [e2-1-dictionary/](e2-1-dictionary/) (28 files) |
| [e2-2.md](e2-2.md) | e2-2-ladder: the batch discount, measured; and what the ladder really asks | [e2-2-ladder/](e2-2-ladder/) (31 files) |
| [e2-3.md](e2-3.md) | wht39 / ideas / e2-3-drain: steepest drain, and what the drain is made of | [e2-3-drain/](e2-3-drain/) (930 files, 3 left out) |

## 4. Recombination

One agent read every wave so far, put the results side by side and tried combinations of two ideas (the reports call them hybrids).

| Report | Its own title | Folder of programs |
|---|---|---|
| [j-cross.md](j-cross.md) | j-cross: both waves side by side, four hybrids tried, and what to ask next | [j-cross/](j-cross/) (14 files) |

## 5. Critics

Three agents came last and attacked the strongest results.

| Report | Its own title | Folder of programs |
|---|---|---|
| [b-0.md](b-0.md) | b-0: criticism of e2-0's mixed-hub circuit family | [b-0/](b-0/) (15 files) |
| [b-1.md](b-1.md) | b-1: the clique lemma, read by a second reader | [b-1/](b-1/) (41 files) |
| [b-2.md](b-2.md) | b-2: criticism of e-7's slack law (Lemma 4) and its "door" | [b-2/](b-2/) (4 files) |

## 6. Side reports

How the wave's note was written.

| Report | Its own title | Folder of programs |
|---|---|---|
| [j-note.md](j-note.md) | j-note: report on writing WAVE2-NOTE.md | [j-note/](j-note/) (2 files) |
