# Third wave: every report

> **Before you run a program from this folder.** These programs were written in a hurry for my own machines, and no person has reviewed them. Read a script before you run it, and start it from the top folder of the repository; [../WHERE.md](../WHERE.md) says how. In this wave, `g-2-basischange/fam2.py` executes the text of the environment variable `GFILTER` if it is set. `g-6-twosteps/rsh.sh` and `rcp.sh` reached a rented machine; they now only print a message and stop. Two scripts that stopped and restarted jobs are left out ([LEFT-OUT.md](LEFT-OUT.md)).

Ran 10 Oct, 22:37 to 11 Oct, 00:25 (Eastern time). **Read [NOTE.md](NOTE.md) first**: it is the wave's own summary, written last. The reports below are what it was written from, in the order the work was done.

**Status.** Everything in this folder is the work of AI agents (Anthropic's Claude) that I directed. No person has reviewed it, and none of it is in Lean (a proof checker: a program that checks a proof step by step). The one exception is not in this folder: a circuit with at most (5/6)·N·log2 N + N operations for N = 8^j points, which grew out of the third wave's 8-point circuit, was proved correct in Lean afterwards, and that proof is in the `lean/` folder of this repository. The reports are a record of one night and are not rewritten. A later wave sometimes corrected an earlier one; where they disagree, believe the later one. The titles in the tables below are the agents' own words, not my claims.

**What is here.** A *report* is one agent's write-up. Its *folder* holds the programs that agent wrote and their small outputs, so that a number can be computed again. Larger files, compiled programs and binary data are not here: [LEFT-OUT.md](LEFT-OUT.md) lists them.

**Names.** The reports call this wave's note `WAVE3-NOTE.md`; here it is [NOTE.md](NOTE.md). They call each other by short labels such as `g-1` or `e2-0`: [../WHERE.md](../WHERE.md) says which wave each label is in, what the other names in the reports mean, and how to run a program again. When a report says "the user", it means me.

**Editor's notes, and three things that are true of every report.** Some reports begin with a block that starts "Editor's note (11 October 2026)". I put it there where a later report corrected the report, or where a statement about someone else's work could mislead. It is the only text in a report that is not the agent's. It adds two lines, so a line number that another report gives for that report is two too small. A report without a note is not thereby right: part 3 of [../LEADS.md](../LEADS.md) lists what was withdrawn. What the reports say about published work is as their authors marked it, mostly read through a tool that summarises, from an abstract, second hand or from memory, and nobody checked those statements against the sources, except where a report says "raw text"; [Earlier papers](../README.md#earlier-papers) says what the two papers that matter most contain. Many reports begin with "Private" or "nothing published, no git": that was their status on the night they were written, and an order to the agents not to publish anything themselves. I decided to publish them afterwards.


## 2. The picks

One agent, the curator, chose which ideas to develop and wrote a brief (a task description) for each.

| Report | Its own title | Folder of programs |
|---|---|---|
| [WAVE3-PICKS.md](WAVE3-PICKS.md) | wht39 / ideas / WAVE3-PICKS: eight briefs for an hour each | none |

## 3. Developments

One agent per brief, about an hour each.

| Report | Its own title | Folder of programs |
|---|---|---|
| [g-0.md](g-0.md) | g-0-mirror: the cheapest basis of the mirror at 16 points is 24 gates, exactly; the whole route then ties 56, by proof | [g-0-mirror/](g-0-mirror/) (8 files, 1 left out) |
| [g-1.md](g-1.md) | g-1 tightwires: the lemma refereed, the winners taken apart, and a new 8-point circuit in 19 gates | [g-1-tightwires/](g-1-tightwires/) (31 files) |
| [g-2.md](g-2.md) | g-2-basischange: the cheapest symmetry-adapted basis at 8 and 16 points, and what its shape says | [g-2-basischange/](g-2-basischange/) (12 files, 2 left out) |
| [g-3.md](g-3.md) | g-3 illconditioned: badly conditioned steps whose product is perfectly conditioned | [g-3-illconditioned/](g-3-illconditioned/) (99 files, 2 left out) |
| [g-4.md](g-4.md) | g-4 zetalead: the published exponent carries to subset sums, and what that says back about the transform | [g-4-zetalead/](g-4-zetalead/) (14 files, 2 left out) |
| [g-5.md](g-5.md) | g-5-k3: the 3-point kernel K3, played with | [g-5-k3/](g-5-k3/) (59 files, 3 left out) |
| [g-6.md](g-6.md) | g-6-twosteps: where two dense linear-cost steps can make the transform, and where they cannot | [g-6-twosteps/](g-6-twosteps/) (31 files) |
| [g-7.md](g-7.md) | g-7-thirdturn: the transform is "multiply the label by a cube root of one"; every such renaming ties, at 4 and at 16 points | [g-7-thirdturn/](g-7-thirdturn/) (39 files) |

## 4. Recombination

One agent read every wave so far, put the results side by side and tried combinations of two ideas (the reports call them hybrids).

| Report | Its own title | Folder of programs |
|---|---|---|
| [k-cross.md](k-cross.md) | k-cross: the three waves side by side, four hybrids tried, and what to ask next | [k-cross/](k-cross/) (15 files) |

## 5. Critics

Three agents came last and attacked the strongest results.

| Report | Its own title | Folder of programs |
|---|---|---|
| [c-0.md](c-0.md) | c-0: critic's report on g-1 (the 8-point transform in 19 gates) | [c-0/](c-0/) (14 files) |
| [c-1.md](c-1.md) | c-1: the critic's report on e2-0 (16 points in 52 gates; the family (3/4) N log2 N + N/4) | [c-1/](c-1/) (15 files) |
| [c-2.md](c-2.md) | c-2: skeptic's report on g-6 ("two tree steps of the periodic shape cannot make the transform from 64 points on") | [c-2/](c-2/) (9 files) |

## 6. Side reports

How the wave's note was written, and one agent's reading of what is published on the question.

| Report | Its own title | Folder of programs |
|---|---|---|
| [lit-constants.md](lit-constants.md) | lit-constants: what is published about the constant in front of N log N for the Walsh-Hadamard transform | none |
| [k-note.md](k-note.md) | k-note: report on writing WAVE3-NOTE.md | [k-note/](k-note/) (2 files) |
