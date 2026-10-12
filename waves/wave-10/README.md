# Tenth wave: every report

> **Before you run a program from this folder.** These programs were written in a hurry for my own machines, and no person has reviewed them. Read a script before you run it, and start it from the top folder of the repository; [../WHERE.md](../WHERE.md) says how. In this wave, `ag-8-bestbadcircuit/merge.py` and `collapse.py` load pickle files, a format that can run code: never give them a pickle file from somewhere else (their own are left out). `ag-5-threehelpers/rsh.sh` and `ag-8-bestbadcircuit/rsh.sh` reached a rented machine; they now only print a message and stop.

Ran 11 Oct, 07:37 to 09:49 (Eastern time). **Read [NOTE.md](NOTE.md) first**: it is the wave's own summary, written last. The reports below are what it was written from, in the order the work was done.

**Status.** Everything in this folder is the work of AI agents (Anthropic's Claude) that I directed. No person has reviewed it, and none of it is in Lean (a proof checker: a program that checks a proof step by step). The one exception is not in this folder: a circuit with at most (5/6)·N·log2 N + N operations for N = 8^j points, which grew out of the third wave's 8-point circuit, was proved correct in Lean afterwards, and that proof is in the `lean/` folder of this repository. The reports are a record of one night and are not rewritten. A later wave sometimes corrected an earlier one; where they disagree, believe the later one. The titles in the tables below are the agents' own words, not my claims.

**What is here.** A *report* is one agent's write-up. Its *folder* holds the programs that agent wrote and their small outputs, so that a number can be computed again. Larger files, compiled programs and binary data are not here: [LEFT-OUT.md](LEFT-OUT.md) lists them.

**Names.** The reports call this wave's note `WAVE10-NOTE.md`; here it is [NOTE.md](NOTE.md). They call each other by short labels such as `g-1` or `e2-0`: [../WHERE.md](../WHERE.md) says which wave each label is in, what the other names in the reports mean, and how to run a program again. When a report says "the user", it means me.

**Editor's notes, and three things that are true of every report.** Some reports begin with a block that starts "Editor's note (11 October 2026)". I put it there where a later report corrected the report, or where a statement about someone else's work could mislead. It is the only text in a report that is not the agent's. It adds two lines, so a line number that another report gives for that report is two too small. A report without a note is not thereby right: part 3 of [../LEADS.md](../LEADS.md) lists what was withdrawn. What the reports say about published work is as their authors marked it, mostly read through a tool that summarises, from an abstract, second hand or from memory, and nobody checked those statements against the sources, except where a report says "raw text"; [Earlier papers](../README.md#earlier-papers) says what the two papers that matter most contain. Many reports begin with "Private" or "nothing published, no git": that was their status on the night they were written, and an order to the agents not to publish anything themselves. I decided to publish them afterwards.


## 2. The picks

One agent, the curator, chose which ideas to develop and wrote a brief (a task description) for each.

| Report | Its own title | Folder of programs |
|---|---|---|
| [WAVE10-PICKS.md](WAVE10-PICKS.md) | WAVE10-PICKS: ten briefs (the nine experiments of ae-cross section 6, and irrational constants) | none |

## 3. Developments

One agent per brief, about an hour each.

| Report | Its own title | Folder of programs |
|---|---|---|
| [ag-0.md](ag-0.md) | ag-0 ladder-degree-3: the third rung does fall to N + o(N), by a tower of lamps; the saving starts beyond any size one can write, and the fourth rung meets the same obstruction one level up | [ag-0-ladderdegree3/](ag-0-ladderdegree3/) (8 files) |
| [ag-1.md](ag-1.md) | ag-1 halving-or-nothing: one halving never gives the right wire in the block at 14 or 15 gates; a halving is a line used downhill and weighs nothing in the determinant ledger | [ag-1-halvingornothing/](ag-1-halvingornothing/) (36 files, 8 left out) |
| [ag-2.md](ag-2.md) | ag-2 the-first-bus-that-pays: every upper circuit, the ninth injection, and a third room (the triangle) | [ag-2-firstbusthatpays/](ag-2-firstbusthatpays/) (174 files, 4 left out) |
| [ag-3.md](ag-3.md) | ag-3 sector-and-port: which free steps see the sign of the move | [ag-3-sectorandport/](ag-3-sectorandport/) (6 files) |
| [ag-4.md](ag-4.md) | ag-4: the cheapest generator of the half-rate space of low-degree polynomials | [ag-4-cheapestgenerato/](ag-4-cheapestgenerato/) (13 files) |
| [ag-5.md](ag-5.md) | ag-5 three-helpers: the first case is built (29 classes at 32 points, 61 at 64, 125 at 128), by choosing the kernel first; no growth law | [ag-5-threehelpers/](ag-5-threehelpers/) (34 files) |
| [ag-6.md](ag-6.md) | ag-6 deep-gates: forms never want a coefficient above 3; a deep gate into an output has no choice; the specimen exists, and it sits in the transform's own class, where one gate carries as many units as one likes at the same count | [ag-6-deepgates/](ag-6-deepgates/) (112 files, 8 left out) |
| [ag-7.md](ag-7.md) | ag-7 rank-dial: the bus is switched off by the length of the shortest relation among the outputs, at degree about log2 k | [ag-7-rankdial/](ag-7-rankdial/) (92 files, 2 left out) |
| [ag-8.md](ag-8.md) | ag-8 the-best-bad-circuit: at 4 points the transform has no circuit of its own one gate above the least (exhaustive modulo 13 and 17); it has a third of its class's shapes; the first circuit that is the transform's own (by a hand lemma, machine test two thirds done) is at 16 points, costs the textbook count, and its family cannot be cheaper | [ag-8-bestbadcircuit/](ag-8-bestbadcircuit/) (37 files, 1 left out) |
| [ag-9.md](ag-9.md) | ag-9: irrational constants (Gaussian integers, eighth roots of unity, sqrt 2, the golden ratio) | [ag-9-irrationalconsta/](ag-9-irrationalconsta/) (40 files, 1 left out) |

## 4. Recombination

One agent read every wave so far, put the results side by side and tried combinations of two ideas (the reports call them hybrids).

| Report | Its own title | Folder of programs |
|---|---|---|
| [ah-cross.md](ah-cross.md) | ah-cross: the ten waves side by side, four hybrids tried, and what to ask next | [ah-cross/](ah-cross/) (11 files) |

## 5. Critics

Three agents came last and attacked the strongest results.

| Report | Its own title | Folder of programs |
|---|---|---|
| [ai-0.md](ai-0.md) | ai-0, critic of ag-0's tower of lamps: the law holds and is now built and proved; two side claims are wrong; nothing for the transform | [ai-0/](ai-0/) (9 files) |
| [ai-1.md](ai-1.md) | ai-1: the private-wire lemma and the floor 2N - o(N), checked | [ai-1/](ai-1/) (9 files) |
| [ai-2.md](ai-2.md) | ai-2 (skeptic): the two determinant ledgers hold and are Morgenstern's 1973 argument; the conclusion drawn from hybrid 2 does not hold as written: subset sums have a volume of their own, of order N sqrt(log N) | [ai-2/](ai-2/) (10 files, 1 left out) |

## 6. Side reports

How the wave's note was written.

| Report | Its own title | Folder of programs |
|---|---|---|
| [ah-note.md](ah-note.md) | ah-note: how WAVE10-NOTE.md was made, and its limits | [ah-note/](ah-note/) (2 files) |
