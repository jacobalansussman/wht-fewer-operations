# Fourth wave: every report

> **Before you run a program from this folder.** These programs were written in a hurry for my own machines, and no person has reviewed them. Read a script before you run it, and start it from the top folder of the repository; [../WHERE.md](../WHERE.md) says how. In this wave, `n-2/w5_look.py` and `n-2/compare.py` load pickle files, a format that can run code: never give them a pickle file from somewhere else (their own are left out). `h-0-onepergate/rsh.sh` and `rcp.sh` reached a rented machine; they now only print a message and stop.

Ran 10 Oct, 23:35 to 11 Oct, 01:40 (Eastern time). **Read [NOTE.md](NOTE.md) first**: it is the wave's own summary, written last. The reports below are what it was written from, in the order the work was done.

**Status.** Everything in this folder is the work of AI agents (Anthropic's Claude) that I directed. No person has reviewed it, and none of it is in Lean (a proof checker: a program that checks a proof step by step). The one exception is not in this folder: a circuit with at most (5/6)·N·log2 N + N operations for N = 8^j points, which grew out of the third wave's 8-point circuit, was proved correct in Lean afterwards, and that proof is in the `lean/` folder of this repository. The reports are a record of one night and are not rewritten. A later wave sometimes corrected an earlier one; where they disagree, believe the later one. The titles in the tables below are the agents' own words, not my claims.

**What is here.** A *report* is one agent's write-up. Its *folder* holds the programs that agent wrote and their small outputs, so that a number can be computed again. Larger files, compiled programs and binary data are not here: [LEFT-OUT.md](LEFT-OUT.md) lists them.

**Names.** The reports call this wave's note `WAVE4-NOTE.md`; here it is [NOTE.md](NOTE.md). They call each other by short labels such as `g-1` or `e2-0`: [../WHERE.md](../WHERE.md) says which wave each label is in, what the other names in the reports mean, and how to run a program again. When a report says "the user", it means me.

**Editor's notes, and three things that are true of every report.** Some reports begin with a block that starts "Editor's note (11 October 2026)". I put it there where a later report corrected the report, or where a statement about someone else's work could mislead. It is the only text in a report that is not the agent's. It adds two lines, so a line number that another report gives for that report is two too small. A report without a note is not thereby right: part 3 of [../LEADS.md](../LEADS.md) lists what was withdrawn. What the reports say about published work is as their authors marked it, mostly read through a tool that summarises, from an abstract, second hand or from memory, and nobody checked those statements against the sources, except where a report says "raw text"; [Earlier papers](../README.md#earlier-papers) says what the two papers that matter most contain. Many reports begin with "Private" or "nothing published, no git": that was their status on the night they were written, and an order to the agents not to publish anything themselves. I decided to publish them afterwards.


## 2. The picks

One agent, the curator, chose which ideas to develop and wrote a brief (a task description) for each.

| Report | Its own title | Folder of programs |
|---|---|---|
| [WAVE4-PICKS.md](WAVE4-PICKS.md) | wht39 / ideas / WAVE4-PICKS: nine briefs for an hour each | none |

## 3. Developments

One agent per brief, about an hour each.

| Report | Its own title | Folder of programs |
|---|---|---|
| [h-0.md](h-0.md) | h-0 onepergate: can one over-limit wire pay for more than one saved gate? | [h-0-onepergate/](h-0-onepergate/) (27 files) |
| [h-1.md](h-1.md) | h-1 staircase3: the three-bit brick taken apart, interleaved, and why the saving does not double | [h-1-staircase3/](h-1-staircase3/) (106 files, 3 left out) |
| [h-2.md](h-2.md) | h-2-clique17: four arrays at block size 5 need all 20 moves; and the place where the lemma goes silent | [h-2-clique17/](h-2-clique17/) (50 files, 7 left out) |
| [h-3.md](h-3.md) | h-3-orecord: the record in OpenAI's own count, priced with OpenAI's own files | [h-3-orecord/](h-3-orecord/) (36 files, 1 left out) |
| [h-4.md](h-4.md) | h-4 zetafloor: subset sums, a meter that is an identity, and the exact place where the floor proof stops | [h-4-zetafloor/](h-4-zetafloor/) (32 files, 14 left out) |
| [h-5.md](h-5.md) | h-5 ladderbound: programs whose wires are entangled on at most two bits | [h-5-ladderbound/](h-5-ladderbound/) (42 files, 4 left out) |
| [h-6.md](h-6.md) | h-6 classhub: nothing dies on the way. Every record of tonight is one program for ALL 2 x 2 kernels, written on integer tables | [h-6-classhub/](h-6-classhub/) (40 files, 1 left out) |
| [h-7.md](h-7.md) | h-7-unitmeter: the published unit read with tonight's meters | [h-7-unitmeter/](h-7-unitmeter/) (14 files) |
| [h-8.md](h-8.md) | h-8 provethewrongthing: the proof of L1 written out, the place where it stops, and what stands on each side of that place | [h-8-provethewrongthi/](h-8-provethewrongthi/) (15 files, 1 left out) |

## 4. Recombination

One agent read every wave so far, put the results side by side and tried combinations of two ideas (the reports call them hybrids).

| Report | Its own title | Folder of programs |
|---|---|---|
| [m-cross.md](m-cross.md) | m-cross: the four waves side by side, four hybrids tried, and what to ask next | [m-cross/](m-cross/) (12 files) |

## 5. Critics

Three agents came last and attacked the strongest results.

| Report | Its own title | Folder of programs |
|---|---|---|
| [n-0.md](n-0.md) | n-0: critic's report on h-3 (56 operations at 16 points, and the 5/6 rate) | [n-0/](n-0/) (10 files) |
| [n-1.md](n-1.md) | n-1: criticism of one object: h-8 Proposition A and h-5's width theorem | [n-1/](n-1/) (8 files) |
| [n-2.md](n-2.md) | n-2: criticism of h-2 ("four arrays at block size 5 need all 20 moves in old letters") | [n-2/](n-2/) (35 files, 11 left out) |

## 6. Side reports

How the wave's note was written.

| Report | Its own title | Folder of programs |
|---|---|---|
| [m-note.md](m-note.md) | m-note: report on writing WAVE4-NOTE.md | [m-note/](m-note/) (2 files) |
