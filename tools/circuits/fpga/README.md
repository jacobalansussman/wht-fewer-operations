# tools/circuits/fpga: the circuits as hardware

This folder builds the circuits of this repository as hardware and compares them with the textbook network
and with two designs from print. It is the long version of the section "In hardware" of
[the README](../../../README.md).

The designs, the programs and the measurements of this folder were made on 11 October 2026 by the AI agents
(Anthropic's Claude) that I direct. A second agent then tried to break the 8-point result, and what is
written here is what that check let stand. No person has read the programs line by line.

**Words.**

- **FPGA**: a chip whose logic is set by loading a file into it. The one used here is a Lattice iCE40HX8K,
  which has 7,680 logic cells.
- **Logic cell**: the unit such a chip is made of. On the iCE40 one cell holds one small lookup table (any
  function of four bits), one carry bit and one flip-flop (a one-bit memory). On the Lattice ECP5 the
  comparable unit is a "LUT place", half a slice.
- **Adder**: the hardware that adds or subtracts two numbers. One line `a ± b` or `a ± 2b` of a circuit is
  one adder, because doubling a number only moves its wires by one place.
- **Carry chain**: the fast wire that hands the carry from each bit of an adder to the next. An 11-bit adder
  takes 11 cells in a row on it, so an adder is paid for per bit.
- **Adder level** and **depth**: an adder that reads only inputs is at level 1, and an adder is one level
  above the higher of the two values it reads. The depth of a circuit is its highest level.
- **Pipeline register**, **pipelining**: a row of flip-flops between adder levels, so that the clock can run
  faster. The answer then comes out some clocks later (the *latency*), and a value that has to wait for a
  later level needs flip-flops of its own.
- **Clock speed**: how many results a second the circuit can take. The tools estimate the highest clock, in
  MHz, from the longest path between two registers.
- **Synthesis**: the program step that turns the description of a circuit into logic cells (here the
  program Yosys). **Place and route**: the step that gives every cell a place on the chip and wires the
  cells together (here the program nextpnr). Only after it is there a speed figure. **Packing** is the
  first part of that step, in which the cells are counted. A **seed** is the random starting point of one
  placement run.

## 1. The answer in short

1. **Fewer cells, as one block of adders with no registers inside.** On the iCE40HX8K the 19-adder 8-point
   circuit takes 274 logic cells where the textbook network takes 349 (8-bit inputs, one output register):
   75 fewer, 21.5 %. With the synthesis option `-dff` it is 273 against 337: 64 fewer, 19.0 %. At 9, 12
   and 16 bits the saving is the same 19 % to 22 %.
2. **Not at the same speed.** The new circuits are twice as deep, so the tools put the highest clock of the
   8-point block at about 72 MHz against about 97 MHz for the textbook. These are estimates of the tools,
   not measurements. Once registers are added for speed, the textbook is the smaller design above about
   85 MHz; with a register after every adder it is 677 cells against 363.
3. **Not the smallest.** The 22-adder step of Alman and Rao (2023) takes 244 cells at 8 points under the
   same conditions. At 16 points and 8 bits my 52-adder circuit takes 877 cells against 969 for the
   textbook (9.5 % fewer), and the 1994 design of Coppersmith, Feig and Linzer takes 720.
4. **The family from 16 to 256 points** (section 5): as a block with no registers inside and 9-bit inputs,
   17.5 % to 23.1 % fewer iCE40 cells than the textbook and 19.1 % to 22.0 % fewer on a Lattice ECP5;
   slower; larger than the textbook when pipelined; against the 1994 design, fewer on the ECP5 and about
   equal on the iCE40.
5. **Where it could matter, and where not.** It gives fewer cells where the transform is built as one
   fully parallel block and the clock is slow enough to need no registers inside (below about 65 MHz for
   the 8-point block on this chip). It matters little where the transform is folded (most video encoders
   reuse one or two small transforms beside a large buffer), it does not fit serial designs, and it loses
   in fully pipelined ones. **No existing design was improved in this check.**

The cell counts are exact for these tools: the same in 20 placement runs, and both circuits are proved
equal to the transform for all inputs. One open-source tool chain was used. Only the iCE40 was placed,
routed and checked a second time.

On an iCE40-HX8K FPGA board running at 12 MHz, the 19-adder 8-point Walsh-Hadamard circuit was run side by side with the textbook circuit on 597,750,000 test inputs, and the two gave the same outputs every time; a deliberately broken copy of the circuit, run alongside, was caught, which shows the test can fail. This checks only that the circuit computes the right values on a real chip: it says nothing about size or speed, and in this pipelined build the 19-adder circuit is the larger of the two designs. The lines the board sent, and the conditions, are in [board/run-2026-10-11/](board/run-2026-10-11/README.md).

## 2. What the standard is

In every open hardware design and every paper that was read for this check, the transform is built as the
textbook "butterfly" network: log2 N layers, each of N adders. That is 24 adders at 8 points, 64 at 16
points (the 4 x 4 block of video coding) and 384 for a fully parallel 8 x 8 block.

Two examples in open code were built here, unchanged, through a thin wrapper of mine:

- the 8-point Hadamard module of the open HEVC video encoder xk265: module `hadamard_trans_1d` in
  `rtl/fme/fme_satd_8x8.v` of <https://github.com/openasic-org/xk265>;
- the 4 x 4 module of the H.264 encoder xk264: module `intra_hadamard4x4` in
  `rtl/intra/intra_hadamard4x4.v` of <https://github.com/openasic-org/xk264>.

The commits that were used are under Sources and in the commands of section 8.

Built with the same tools, the xk265 module gives exactly the cell counts of my own textbook design at 8,
9, 12 and 16 bits (349, 385, 493, 637), and the xk264 module does at 9 bits (1,065). So "textbook" below is
the design in use, and it was measured. The xk265 module, built unchanged at its own 9-bit width, takes 385
cells, and the 19-adder circuit at 9 bits takes 302. (With `-dff`: 377 and 301. The wrapper around the
module is checked by simulation.)

Neither repository has a licence file, and the headers of their files forbid redistribution. So their code
is not in this repository: [outside/](outside/) has the wrappers, and section 8 says how to fetch the two
repositories. Only these two modules were compared, as modules. The xk265 encoder itself folds the
transform (two 8-point transforms beside 768 register bits), so nothing follows for a whole encoder.

**What is already below the textbook, in print.**

- At 4 points, 7 additions in place of 8: the 1994 paper of Coppersmith, Feig and Linzer, and an expired
  patent filed in 2002 (US 7,003,536) that draws it as a hardware circuit. A variant with one halving is
  in the JPEG XR and AV1 reference code.
- At 8 points, nothing below 22 additions was found in print (the 1994 design, and Alman and Rao 2023),
  and nothing below 24 in any hardware code.
- For the main video use, SATD (a cost figure that sums the absolute values of a transformed block), a
  method of 2009 skips part of the transform. It needs 55 additions and 8 maximum operations at 4 x 4,
  where the textbook route needs 79 (Cancellier and others, 2015, Table I). With my 16-point circuit the
  count would be 67. This is arithmetic on published figures; nothing was built.

## 3. What was built, and how it was checked and measured

**The designs.** One generator, [rtl/gen_rtl.py](rtl/gen_rtl.py), turns a circuit file into Verilog (the
language hardware is described in): one adder per line of the circuit, every wire exactly as wide as its
values need, doubling and halving as wiring. Four designs were built:

- the textbook;
- the 1994 design (the 4-point circuit of Coppersmith, Feig and Linzer in layers);
- the 8-point step of Alman and Rao, taken from Algorithm 5 of their paper. No line was invented. It exists
  at 8 points only;
- this work: 19 adders at 8 points, 52 at 16, and 304 at 64 points in two forms (the family, and the
  19-adder circuit on the rows and then on the columns of an 8 x 8 block).

Inputs are signed numbers of 8, 9, 12 and 16 bits. Each design exists as one block of adders with no
registers inside (in the file names: `c`), and pipelined with a register after every adder level (`p`),
every second level (`p2`), and so on.

**That they compute the transform.** Every file was simulated against the definition of the transform with
100,000 random inputs and several thousand corner cases, in two simulators, with no mismatch. Deliberately
damaged copies were caught. Every unpipelined file is also proved equal to the transform for all inputs,
in two ways: with solvers ([rtl/formal/](rtl/formal/SUMMARY.md)), and by a second program written
separately that reads the Verilog text and uses no solver
([rtl/formal/static_proof.py](rtl/formal/static_proof.py), all 42 files, the 64-point ones included). The
pipelined forms with a register after every third to seventh level, and the wrappers around the outside
modules, are checked by simulation, not proved.

**How they were measured.** Each design was synthesised with Yosys 0.69 and placed and routed with nextpnr
0.11.1 for the iCE40HX8K (package CT256), inside the same small test frame: a shift register feeds the
inputs and a signature register collects the outputs. The frame's cells are subtracted (156 at 8 points and
8 bits). Each case was placed 10 times with different seeds (20 times for the textbook and this work at 8
and 16 points, 5 times at 64 points). That made 2,795 routed runs.

**The second check.** A separate agent tried to break the result. It proved the files again on the text
that was measured, wrote its own textbook generator (349 cells in all six orders of the layers), tried all
30 sign choices of the textbook, changed tool options, added 10 new seeds, and recomputed about 60 table
entries from the raw logs. The figures held. It corrected three things: the saving is 64 to 75 cells and not
75 alone, because one tool option helps the textbook more; the speed is "about 72 MHz, 66 at the lowest
seed" and not 73; and "at the same speed" was not shown. Its small result tables are in
[synth/second-check/](synth/second-check/); its programs are not in this repository, apart from the proof
named above.

## 4. The table: 8 points, 16 points and the 8 x 8 block

Chip iCE40HX8K (CT256). Yosys 0.69+274, `synth_ice40`, default settings; the second figure in the cells
column is with the option `-dff`. nextpnr-ice40 0.11.1-59, default settings. Cells are those of the design
alone, with one output register for the unregistered block and with all its own registers for the pipelined
forms. MHz is nextpnr's estimate after routing: median [lowest - highest] over the seeds.

| Size, input bits | Design | Adders on paper (adder levels) | Logic cells, no clock constraint: default / `-dff` | Against textbook | Highest clock of that block, MHz | Fewest cells at one faster clock (100 MHz; 50 MHz for the 8 x 8 block) | A register after every adder level: cells; MHz | Latency in clocks: block / faster clock / every level |
|---|---|---|---|---|---|---|---|---|
| 8 points, 8 bits | textbook | 24 (3) | 349 / 337 | - | 97.2 [87.6 - 103.6] | 354 | 363; 216 [205 - 235] † | 1 / 2 / 3 |
| | the xk265 module | 24 (3) | 349 / not run | the same cells as the textbook | 99.6 [96.6 - 106.4] † | not built | not built | 1 / - / - |
| | 1994 design | 22 (5) | 295 / 287 | -54 (-15.5 %) / -50 (-14.8 %) | 90.8 [87.2 - 92.3] | 320 | 491; 208 [195 - 236] † | 1 / 2 / 5 |
| | Alman and Rao step | 22 (6) | 244 / 242 | -105 (-30.1 %) / -95 (-28.2 %) | 74.1 [66.9 - 77.6] † | 304 | 630; 238 [219 - 239] † | 1 / 2 / 6 |
| | **this work** | 19 (6) | **274 / 273** | **-75 (-21.5 %) / -64 (-19.0 %)** | 72.9 [65.9 - 75.6] † | 395 (41 more than the textbook, +11.6 %) | 677 (314 more, +86.5 %); 203 [190 - 237] † | 1 / 2 / 6 |
| 16 points, 8 bits | textbook | 64 (4) | 969 / 945 | - | 71.2 [66.3 - 77.0] | 980 | 1,013; 205 [198 - 211] † | 1 / 2 / 4 |
| | the xk264 4 x 4 module, fixed at 9 bits | 64 (4) | at 9 bits: 1,065 / 1,049 | the same cells as the textbook at 9 bits in the default flow | 66.8 [63.1 - 72.4] | not built | not built | 1 / - / - |
| | 1994 design | 56 (8) | 720 / 712 | -249 (-25.7 %) / -233 (-24.7 %) | 59.9 [56.4 - 62.0] | 742 (6 of 10 seeds reach 100 MHz) | 1,560; 216 [200 - 230] † | 1 / 2 / 8 |
| | **this work** | 52 (8) | **877 / 870** | **-92 (-9.5 %) / -75 (-7.9 %)** | 54.8 [52.4 - 57.6] † | 1,195 (215 more, +21.9 %) | 1,732 (719 more, +71.0 %); 213 [195 - 229] † | 1 / 3 / 8 |
| | this work, other signs | 52 (8) | 811 / 804 | -158 (-16.3 %) / -141 (-14.9 %) | 56.6 [52.8 - 59.1] † | 1,330 | 1,648; 202 [191 - 208] † | 1 / 4 / 8 |
| 8 x 8 block (64 points), 8 bits | textbook | 384 (6) | 6,337 / not run | - | 42.3 [40.1 - 43.2] | 6,370 | 6,630; 167 [167 - 172] | 1 / 2 / 6 |
| | 1994 design | 336 (12) | 4,704 / not run | -1,633 (-25.8 %) | 38.9 [37.7 - 39.8] | 4,959 | 10,293; does not fit the chip, no speed | 1 / 3 / 12 |
| | **this work**, 19-adder circuit on rows, then columns | 304 (12) | **4,649** / not run | **-1,688 (-26.6 %)** | 34.0 [33.3 - 34.8] † | 4,992 (1,378 fewer, -21.6 %) | 12,425; does not fit the chip, no speed | 1 / 2 / 12 |
| | this work, family circuit | 304 (12) | 5,370 / not run | -967 (-15.3 %) | 33.8 [33.3 - 35.4] † | 6,324 (46 fewer, -0.7 %) | 11,427; does not fit the chip, no speed | 1 / 2 / 12 |

How to read it.

- **Cells have no spread.** Every design gave the same cell count in every placement run, so every
  difference in cells is exact for these tools and settings.
- **† marks speeds whose difference is inside the seed-to-seed spread**, so it is not a difference: this
  work against the Alman and Rao step as a block; the xk265 module against my textbook; this work against
  its "other signs" form at 16 points; the two forms of this work at 64 points; and all the speeds with a
  register after every adder level at 8 points and at 16 points. The gap between this work and the textbook
  as a block is outside the spread at every size.
- **"Fewest cells at one faster clock"** is the pipelined form with the fewest cells whose median estimate
  reaches the target. At 8 points that is a register after every second level for the textbook and after
  every third level for this work. The 64-point entries are taken from the table of measured forms in
  [synth/TABLES.md](synth/TABLES.md); fewer forms were built there, because many do not fit the chip.
- **Other widths, 8 points, textbook against this work, default / `-dff`:** 9 bits 385 / 373 against
  302 / 301; 12 bits 493 / 481 against 386 / 385; 16 bits 637 / 625 against 498 / 497. That is 19.3 % to
  21.8 % fewer.
- **Other widths, 16 points:** 12 bits 1,353 / 1,329 against 1,221 / 1,214 (9.8 % and 8.7 % fewer). At 64
  points only 8 bits fits the chip.
- **The outside modules at their own 9-bit width:** the xk265 module takes 385 cells (377 with `-dff`) and
  the 19-adder circuit 302 (301). The xk264 4 x 4 module takes 1,065 (1,049) and my 16-point circuit 963
  (956).
- **The Alman and Rao figure depends on a choice the paper leaves open.** With its sums of several terms
  added in pairs it takes 244 cells; added left to right it takes 281. The 1994 design in its other order
  (plain layer first) takes 286 (279 with `-dff`), which is 12 cells (6) more than this work.
- **"Other signs"** is the same 16-point circuit with nine intermediate values kept as their negatives. It
  has the same adders and depth and fewer subtractions. It is the best of a random search, not proved best.
- **Why 9.5 % here and 17.5 % in section 5 for 16 points.** Section 5 counts the block without an output
  register and at 9 bits. Counted that way here it is 780 cells against 944 at 8 bits (17.4 % fewer). With
  the output register the saving shrinks by 72 cells (from 164 to 92), because many outputs of the new
  circuit also feed other adders and then need a register cell of their own (97 such cells against 17).
- **Size times delay is worse for this work:** cells times the longest path is 4 % to 12 % higher at 8
  points and 17 % to 29 % higher at 16 points.
- **Other chip families, 8 points, 8 bits, synthesis only (no placement, no speed):** 196 against 256
  lookup-table places on a Lattice ECP5 (23.4 % fewer), 208 against 252 on an Intel Cyclone V (17.5 %
  fewer), 185 against 206 lookup tables on a Xilinx 7-series (10.2 % fewer). On these three, this work is
  the smallest of the four designs.

**Why the result is what it is.** On this chip an adder costs one logic cell per bit, so fewer adders mean
fewer cells: 199 adder bits against 240 at 8 points and 8 bits. A subtraction costs one more lookup table
per bit, because under these tools the carry chain cannot take an inverted number for free. The textbook
has 12 subtractions and the new circuit 9, and that is about half of the saving: of the 77 lookup tables
saved, 41 are adder bits and 36 are these inverters. It is also why the Alman and Rao step, with one
subtraction, is the smallest design here, and why the 1994 design wins at 16 points (8 subtractions against
32). The price comes from depth and reuse. The new circuit has 6 adder levels where the textbook has 3, so
the unregistered block is slower. When registers are added for speed, a register right behind an adder is
free, because it sits in the adder's own cell. A value that waits several levels for its next use needs
cells of its own: with a register after every adder, the new circuit has 410 such cells and the textbook
27. In the textbook no value ever waits. The new circuit reuses values several levels later, and that reuse
is exactly how it saves adders.

## 5. The family from 16 to 256 points

The three designs here are the textbook (N k adders for N = 2^k points), the 1994 design ((7/8) N k adders,
and N/8 more when k is odd) and the family ((3/4) N k + N/4 adders). All figures: signed 9-bit inputs,
every wire at its exact width, outputs of 9 + k bits; Yosys 0.69+274 with default settings; cells counted
by nextpnr 0.11.1-59 after packing, with the cost of the test wrapper subtracted. This part was made as a
separate job and checked by a second agent, who recounted the circuits with a reader of its own, simulated
the 32-point designs again, reran one synthesis on each chip family and the 16-point placement, and read
every other figure again from the raw logs. Nothing failed.

**Table A. One block of adders, no flip-flops inside.** Each cell of the table reads textbook / 1994 /
family.

| N | adders on paper | iCE40 logic cells | family against textbook, iCE40 | family against 1994, iCE40 | ECP5 LUT places | family against textbook, ECP5 | family against 1994, ECP5 | how far the runs got |
|---|---|---|---|---|---|---|---|---|
| 16 | 64 / 56 / 52 | 1,040 / 783 / 858 | 17.5 % fewer | 9.6 % more | 1,025 / 923 / 829 | 19.1 % fewer | 10.2 % fewer | iCE40-HX8K: placed and routed, three seeds. ECP5: packed only. |
| 32 | 160 / 144 / 128 | 2,720 / 2,206 / 2,183 | 19.7 % fewer | 1.0 % fewer | 2,625 / 2,421 / 2,105 | 19.8 % fewer | 13.1 % fewer | iCE40-HX8K: placed and routed, three seeds. ECP5: packed only. |
| 64 | 384 / 336 / 304 | 6,816 / 5,103 / 5,369 | 21.2 % fewer | 5.2 % more | 6,529 / 5,899 / 5,153 | 21.1 % fewer | 12.6 % fewer | iCE40-HX8K: 1994 and family placed and routed, three seeds; the textbook does not fit the chip with the wrapper (8,356 cells against 7,680), packed only. ECP5-85F: placed and routed, three seeds. |
| 128 | 896 / 800 / 704 | 16,576 / 13,150 / 12,881 | 22.3 % fewer | 2.0 % fewer | 15,617 / 14,357 / 12,289 | 21.3 % fewer | 14.4 % fewer | iCE40: packed only (nothing fits). ECP5-85F: placed and routed, three seeds. |
| 256 | 2,048 / 1,792 / 1,600 | 39,424 / 29,439 / 30,321 | 23.1 % fewer | 3.0 % more | 36,865 / 33,451 / 28,737 | 22.0 % fewer | 14.1 % fewer | iCE40: packed only. ECP5-85F: 1994 and family placed and routed, one seed; the textbook's routing was stopped, packed only. |

The saving of the family against the textbook on paper, for comparison: in adders 18.8 %, 20.0 %, 20.8 %,
21.4 %, 21.9 %; in adder bits (the widths of all adder results added up, 9-bit inputs) 16.3 %, 17.5 %,
18.3 %, 19.0 %, 19.4 %. On paper the saving in adders is 1/4 - 1/(4k), which is a quarter only in the
limit of large N. The measured saving stays within 1.3 percentage points of that at every size, so at 256
points it is 22 % to 23 %, not 25 %.

Xilinx 7-series, synthesis with Yosys only (no placement, no vendor tool): the family has 9.6 %, 11.0 %,
12.0 %, 12.9 % and 13.7 % fewer lookup tables than the textbook and 20.2 %, 19.9 %, 20.8 %, 21.5 % and
22.5 % fewer carry cells (CARRY4).

**Table B. Speed of that block**: maximum clock frequency reported by nextpnr after routing, flip-flops of
the wrapper on both sides, median of three seeds. These are estimates of the tool.

| N | chip | textbook | 1994 | family | family against textbook |
|---|---|---|---|---|---|
| 16 | iCE40-HX8K | 70.03 MHz | 55.71 | 49.24 | 29.7 % slower |
| 32 | iCE40-HX8K | 59.45 | 46.62 | 40.63 | 31.7 % slower |
| 64 | ECP5-85F | 57.05 | 39.34 | 35.82 | 37.2 % slower |
| 128 | ECP5-85F | 46.18 | 34.10 | 29.34 | 36.5 % slower |
| 256 | ECP5-85F, one seed | not routed | 27.26 | 25.54 | no figure |

The three seeds differ by about 8 % (family at 16 points: 46.81, 49.24, 50.59 MHz; textbook: 69.65, 70.03,
74.56).

**Table C. Pipelined**: iCE40 logic cells after packing, flip-flops included; in brackets the number of
stages, which is also the number of clock periods the answer takes. The 16- and 32-point designs with a
stage after every level were placed and routed for the iCE40-HX8K and all reach about the same clock (188
to 215 MHz at 16 points, tool estimates); the larger ones are packed only.

| N | textbook, a stage after every level | 1994, a stage after every level | family, a stage after every level | family against textbook | family, a stage after every second level | against textbook at the same number of stages |
|---|---|---|---|---|---|---|
| 16 | 1,140 (4) | 1,715 (8) | 1,904 (8) | 67.0 % more | 1,545 (4) | 35.5 % more |
| 32 | 2,965 (5) | 4,119 (9) | 4,975 (10) | 67.8 % more | 4,045 (5) | 36.4 % more |
| 64 | 7,398 (6) | 11,220 (12) | 12,464 (12) | 68.5 % more | 10,146 (6) | 37.1 % more |
| 128 | 17,926 (7) | 25,645 (13) | 30,314 (14) | 69.1 % more | 24,694 (7) | 37.8 % more |
| 256 | 42,504 (8) | 65,056 (16) | 72,112 (16) | 69.7 % more | 58,776 (8) | 38.3 % more |

The last two columns come from a second, small generator ([family/gen_p2.py](family/gen_p2.py)), checked by
simulation at 32 points; they are packed only, and in that form two adders sit between flip-flops, so its
clock would be slower than the textbook's.

**Why the measured saving is not the saving on paper.**

- **The paper counts adders; a chip pays for every bit of every adder.** The family's adders are a little
  wider on average (13.9 bits against 13.5 at 256 points), so in adder bits its saving is 16.3 % to 19.4 %,
  below the 18.8 % to 21.9 % in adders. Two things push the other way: every adder has a small fixed cost,
  and an adder `a ± 2b` needs no cell for its lowest bit. The net result lands within 1.3 points of the
  adder figure.
- **The formula itself is not a quarter at these sizes.** The N/4 term costs 6.3 points at 16 points and
  3.1 points at 256.
- **On the iCE40 a subtraction costs about twice an addition** (25 lookup tables against 13 for 12-bit
  numbers). The textbook and the family have about the same share of subtractions (50 % and 62 % to 64 %),
  so their comparison is not disturbed. The 1994 design has only 14 % to 22 %, and that is why the family
  does not beat it on the iCE40 although it has fewer adders.
- **The tool reshapes the designs.** Yosys merges two additions of the 1994 design into one three-term
  sum, which costs it cells on the ECP5; with every line kept as one adder the family's advantage over the
  1994 design on the ECP5 after synthesis is 6.6 % to 11.4 %. On Xilinx the tool finds lookup tables that
  the two halves of a textbook butterfly can share, which is why the saving in Xilinx lookup tables is only
  9.6 % to 13.7 %.
- **Pipelining turns the saving into a loss because the family is twice as deep.** It has 2k adder levels
  against k, and many values are used several levels after they are made, so they wait in flip-flops:
  37,376 flip-flop bits of waiting at 256 points, where the textbook needs none, against 5,376 adder bits
  saved. On the iCE40 a flip-flop right behind an adder is free (same cell); a waiting flip-flop takes a
  cell of its own.

## 6. What was and was not placed and routed

| what | synthesised | packed (cells counted) | placed and routed (a speed estimate) | checked a second time |
|---|---|---|---|---|
| 8 and 16 points, 8, 9, 12 and 16 bits, iCE40HX8K | yes | yes | yes, 10 seeds (20 for the textbook and this work at 8 bits) | yes |
| 64 points and the 8 x 8 block, 8 bits, iCE40HX8K | yes | yes | yes, 5 seeds, for the forms that fit the chip | entries recomputed from the logs |
| 8 and 16 points on a Lattice ECP5 (LFE5U-25F) | yes | yes | yes | no |
| 8 and 16 points on a Xilinx 7-series and an Intel Cyclone V | yes | no | no | synthesis rerun |
| the family, 16 and 32 points, iCE40HX8K | yes | yes | yes, three seeds | the 16-point runs |
| the family, 64 points | yes | yes | iCE40HX8K: the 1994 design and the family (the textbook does not fit); ECP5-85F: all three, three seeds | figures read again from the logs |
| the family, 128 points | yes | yes | ECP5-85F, three seeds; nothing fits the iCE40HX8K | figures read again from the logs |
| the family, 256 points | yes | yes | ECP5-85F, one seed, the 1994 design and the family only | figures read again from the logs |
| the family on a Xilinx 7-series | yes | no | no | the 32-point pair |

## 7. Limits, and what has not been done

- **One tool chain:** the open-source tools. The makers' own tools (Lattice iCEcube2 or Radiant, Xilinx
  Vivado, Intel Quartus) were not run. About half of the gain on the iCE40 is the subtraction effect,
  which belongs to this chip's cell under these tools.
- **Two chip families of one maker measured after packing**, the others after synthesis only.
- **No speed was measured.** Every MHz figure is an estimate of the open-source timing models.
- **No custom-silicon estimate.** There is only a rough gate count without a cell library or timing:
  11.2 % fewer at 8 points and 8.4 % fewer at 16 points. In custom silicon a waiting flip-flop and an adder
  bit have other relative costs, so neither the saving nor the pipelined loss carries over.
- **No power measurement.**
- **No retiming and no hand-placed registers.** The registers sit after every K-th adder level. The open
  tools do not move registers across carry chains. Register places chosen by hand or by a search were not
  tried.
- **Sizes and widths:** 8 and 16 points at 8, 9, 12 and 16 bits; 64 points at 8 bits only; the family at
  9 bits (at 12 bits only synthesis was run, with ratios within 0.007 of the 9-bit ones on iCE40 and ECP5).
  The Alman and Rao step exists at 8 points only.
- **Proofs:** the pipelined forms with a register after every third to seventh level and the wrappers
  around the outside modules are checked by simulation, not proved. For the family, the proof of equality
  on all inputs covers the 16-point pair at 9 bits only; the other sizes rest on simulation.
- **No existing design was changed.** Only the 8-point module of xk265 and the 4 x 4 module of xk264 were
  compared, as modules.
- **No test of whether a designer's own adder-sharing tool** (da4ml, FloPoCo) already finds 22 or 19
  adders from the 8-point matrix.
- **No search for a circuit that is good as hardware.** The circuits were found by counting operations.
  Nobody has searched for one with few adder levels, or for one that is small in real cells.
- **The literature search has gaps:** abstracts only for six of the papers, summaries only for the two
  patents, no Chinese-language sources, no vendor catalogues behind a login.

## 8. The files, and how to run them again

Everything here is mine (made by the AI agents under my direction) and under the Apache License 2.0, like
the rest of the repository. The code of the two outside encoders is not included.

| where | what |
|---|---|
| `rtl/gen_rtl.py` | the generator: a circuit text file in, Verilog out. It reads the circuits of `tools/circuits/programs/` and writes the 1994 design and the Alman and Rao step itself |
| `rtl/circuits/` | the circuits that the generator writes: the 1994 design at 8, 16 and 64 points, the Alman and Rao step in two orders of its sums, the textbook 8 x 8 block |
| `rtl/v/` | the 177 design files: size, design (`textbook`, `cfl1994`, `ar2023`, `ours`, `def` for the definition), form (`c`, `p`, `p2`, `r`) and input width are in the name. `rtl/MANIFEST.sha256` lists them |
| `rtl/designs.json`, `rtl/TABLES.md`, `rtl/COUNTS.txt` | adders, levels, adder bits and register bits of every design on paper, and the count of the same by Yosys (`check_counts.py`) |
| `rtl/sim/` | the simulation against the definition (`golden.py` writes the vectors and the test bench, `run_sim.sh` runs two simulators, `RESULTS.txt` is what they printed) and the test with damaged copies |
| `rtl/formal/` | the proofs: with solvers (`run_formal.py`, `run_seq.py`, `SUMMARY.md`), and without (`static_proof.py`, `static_proof.txt`) |
| `synth/run.py` | synthesis, placement and routing of one design with one seed, inside the test frame; prints one record |
| `synth/batch.py`, `synth/gen_extra.py`, `synth/resign.py`, `synth/second.py`, `synth/postsim.py` | all cases two at a time; the further pipelined forms; the "other signs" circuits (`synth/resigned/`); the other chip families; the placed netlist against its source |
| `synth/results/` | one record for every run, as `run.py` printed it (the folder names in the records were made relative) |
| `synth/analyze.py`, `synth/TABLES.md`, `synth/TABLES-SHORT.md`, `synth/summary.json` | the tables, written from the records |
| `synth/second-check/` | small result tables of the second check: default against `-dff`, the 20 seeds, cells times delay, the other chip families, the outside modules |
| `family/` | the family from 16 to 256 points: `fam.py` (circuits, counts on paper, designs, wrappers, test vectors), `mkjobs.py` and `runq.py` (the jobs, two at a time with a memory limit), `collect.py` (the tables), `tables.md`, `results.json`, `paper.json`, `keynums.py`; `gen_p2.py` and `recount.py` from the second check |
| `board/` | the sources of the self-test: `selftest/selftest_top.v` (three pipelined 8-point circuits with 12-bit inputs: the textbook, the 19-adder circuit and a deliberately broken copy, with a comparator and a serial report), the pin file `selftest/hx8k.pcf`, the model of what it sends (`expected.py`, `compare.py`), the build and the simulations (`selftest/build.sh`, `selftest/sim.sh`) |
| `outside/` | the wrappers around the two outside modules (`wrappers/`), my designs at 9 bits (`gen_w9/`), the build and its check (`build_examples.sh`, `check/`) |

**The tools.** The open-source suite oss-cad-suite, release 2026-10-11, from
<https://github.com/YosysHQ/oss-cad-suite-build>. Unpack it and say where it is:

    export OSS_CAD_SUITE=/path/to/oss-cad-suite

The programs of this folder take the tools from there. Run at most two heavy jobs at a time; the largest
job that was watched held about 1 GB of memory (the synthesis of a 256-point design). All commands below are given from `tools/circuits/fpga`. The times are those
of a Mac mini with an Apple M4 processor.

**Without the tools, Python 3.9 or later only.**

    python3 -B rtl/formal/static_proof.py $(ls rtl/v/*_c_w*.v | grep -v _def_)     # 42 lines "PROVED"; under a second
    python3 -B synth/analyze.py                  # writes the three table files again from synth/results/; they must not change
    python3 -B family/keynums.py                 # the ratios of section 5, from family/results.json
    python3 -B rtl/gen_rtl.py --all              # writes rtl/v/, rtl/circuits/ and rtl/designs.json again; they must not change
    (cd rtl/v && shasum -a 256 -c ../MANIFEST.sha256)

**The two headline designs** (2 seconds each):

    python3 -B synth/run.py rtl/v/8_ours_c_w8.v --seed 1 --work /tmp/wht-fpga                              # "lc_dut": 274
    python3 -B synth/run.py rtl/v/8_textbook_c_w8.v --seed 1 --work /tmp/wht-fpga                          # "lc_dut": 349
    python3 -B synth/run.py rtl/v/8_ours_c_w8.v --seed 1 --dff --tag ours_dff --work /tmp/wht-fpga         # "lc_dut": 273
    python3 -B synth/run.py rtl/v/8_textbook_c_w8.v --seed 1 --dff --tag textbook_dff --work /tmp/wht-fpga # "lc_dut": 337

**The designs: counts, simulation, proofs.**

    python3 -B rtl/check_counts.py               # Yosys counts the adders of every file: 10 seconds
    python3 -B rtl/sim/golden.py && sh rtl/sim/run_sim.sh             # simulation against the definition -> rtl/sim/RESULTS.txt
    python3 -B rtl/formal/run_formal.py --sizes 8,16 --widths 8,12,16 # proofs, unregistered block
    python3 -B rtl/formal/run_seq.py --sizes 8,16 --widths 8,12,16    # proofs, the forms p, p2 and r

**All the measurements on the iCE40.** The recorded runs took 104 minutes of machine time in all (31
minutes for 8 points, 39 for 16 points, 21 for 64 points), run two at a time. `batch.py` skips a run that
is already in `synth/results/<group>.jsonl`, so move `synth/results/` aside to repeat from nothing.

    python3 -B synth/gen_extra.py                # the further pipelined files -> synth/v_extra/
    python3 -B synth/resign.py                   # the "other signs" circuits -> synth/v_resigned/
    python3 -B synth/batch.py g8                 # 8 points, every design, form and width, 10 seeds
    python3 -B synth/batch.py g16
    python3 -B synth/batch.py g64lean --seeds 5  # 64 points and the 8 x 8 block
    python3 -B synth/batch.py gnoreg             # blocks without an output register
    python3 -B synth/batch.py gS                 # the "other signs" circuits
    python3 -B synth/analyze.py
    python3 -B synth/second.py synth             # other chip families, synthesis only
    python3 -B synth/second.py ecp5              # ECP5 placed and routed

The groups `g8` and `g16` include the two outside modules, so fetch them first:

    mkdir -p outside/cores && cd outside/cores
    git clone https://github.com/openasic-org/xk265 openasic-org_xk265
    git -C openasic-org_xk265 checkout 832e564a8e59dd90a18fb7ee8e2ed87d96aa03bc
    git clone https://github.com/openasic-org/xk264 openasic-org_xk264
    git -C openasic-org_xk264 checkout b59222e67fb77917a3afe97941c9a25b2b3a41f9
    cd ../..
    sh outside/build_examples.sh                 # synthesises the two modules beside my designs and prints the cells
    sh outside/check/run_sim.sh                  # simulates the wrappers against the definition

**The family.** The steps `circuits` and `paper` need Python only and take a second. The measurements were
422 jobs, 103 minutes of machine time in all, run two at a time. Their logs (82 MB) are not in this
repository, so `collect.py` can write `tables.md` again only after the jobs have been run again.

    python3 -B family/fam.py circuits            # the 17 circuits -> family/circuits/, each checked exactly
    python3 -B family/fam.py paper               # the counts on paper -> family/paper.json; it must not change
    python3 -B family/fam.py rtl                 # the designs and wrappers -> family/v/
    cd family && mkdir -p jobs/pending jobs/done jobs/running logs synth_out synth_keep pnr
    python3 -B mkjobs.py syn9c pnr9_ice40        # writes the job scripts of the named groups into jobs/pending/
    python3 -B runq.py                           # runs them, two at a time, each under a memory limit of 2 GB;
                                                 # it ends when the file jobs/STOP is made (touch jobs/STOP)
    python3 -B collect.py > tables.md

The groups of jobs are the names in the function `main` of `mkjobs.py`; the two above are the synthesis of
the unregistered blocks and the placement for the iCE40 at 16, 32 and 64 points.

**The self-test image, without a board.**

    sh board/selftest/build.sh                   # 11 seconds; the last line must print
                                                 # 862e639ac245137342eecf32261cd13064ddcc8cfd8a84b839909e1c5ffc7300
    sh board/selftest/sim.sh short               # the design in a simulator, 13 report lines against the model: 20 seconds
    sh board/selftest/sim.sh fault               # two damaged builds must be reported as failures: 10 seconds
    sh board/selftest/sim.sh chip                # the netlist decoded from the image, first report line: 1 minute

In the pair that the self-test holds, pipelined and with 12-bit inputs, the 19-adder circuit is the larger
design (973 cells against 507). The loader is not in this repository.

**What was run again from this folder as it is published.** On 11 October 2026, on the Mac mini: the four
commands that need Python only; the four commands for the two headline designs (274, 349, 273, 337);
`check_counts.py`; `analyze.py`; `fam.py circuits` and `fam.py paper`; `outside/build_examples.sh` and
`outside/check/run_sim.sh`, with new clones of the two repositories at the commits named above; the build
of the self-test image and its three simulations above. Not run again from this folder: the simulations
and solver proofs of `rtl/`, the batches, the other chip families and the jobs of the family. Before
publication the folder names inside the programs were changed from those of the machine they ran on to
relative ones, and the one comment line that names the source circuit in each design file was rewritten
the same way; the design files are otherwise the files that were measured.

## Sources

- Tools, each as the program printed it: Yosys 0.69+274 (git 7513f8df8); nextpnr-ice40 and nextpnr-ecp5
  0.11.1-59-g837d0eed; Icarus Verilog 14.0 (devel); Verilator 5.053; SymbiYosys 0.69; bitwuzla 0.9.1;
  Z3 4.15.5; yices 2.7.0; icestorm as shipped in the release (it prints no version). All from oss-cad-suite
  2026-10-11 for macOS on Apple silicon. `synth/tools_used.txt` has the lines.
- Conditions of the 8-point figures: chip iCE40HX8K in package CT256; `synth_ice40` with default settings
  and with `-dff`; nextpnr with `--hx8k --package ct256 --seed S --freq 400`; cells identical over 20
  placement seeds (66 to 76 MHz and 88 to 104 MHz over those seeds); both files proved equal to the
  transform for all inputs; the Alman and Rao figure is with its sums added in pairs (281 if added left to
  right); the 16-point figures with `-dff` are 870, 945 and 712; the pipelined figures are from 10 seeds,
  with a latency of 6 clocks against 3; the xk265 module built unchanged gives the textbook's cell counts
  in the default flow.
- Conditions of the family's figures: cell counts after synthesis with Yosys 0.69+274, default settings,
  and packing with nextpnr 0.11.1-59, every wire at its exact width; placed and routed at 16 and 32 points
  for the iCE40-HX8K and at 64 and 128 points for the ECP5-85F; at 256 points the counts are after packing
  and only the family and the 1994 design were routed; none of these sizes ran on a board.
- xk265, <https://github.com/openasic-org/xk265>, commit `832e564a8e59dd90a18fb7ee8e2ed87d96aa03bc`, file
  `rtl/fme/fme_satd_8x8.v`; xk264, <https://github.com/openasic-org/xk264>, commit
  `b59222e67fb77917a3afe97941c9a25b2b3a41f9`, file `rtl/intra/intra_hadamard4x4.v`. Fetched on 11 October
  2026.
- D. Coppersmith, E. Feig, E. Linzer, "Hadamard transforms on multiply/add architectures", IEEE
  Transactions on Signal Processing 42(4), 1994, doi 10.1109/78.285664.
- J. Alman, K. Rao, "Faster Walsh-Hadamard and Discrete Fourier Transforms From Matrix Non-Rigidity",
  <https://arxiv.org/abs/2211.06459>, version 2, Algorithm 5.
- E. Reshef, I. Alrod, "Reduced complexity fast Hadamard transform", US patent 7,003,536, filed 2002,
  expired. Read through a tool that summarises pages.
- Cancellier, Seidel, Bräscher, Güntzel, Agostini, "Exploring Optimized Hadamard Methods to Design
  Energy-Efficient SATD Architectures", Journal of Integrated Circuits and Systems 10(2), 2015,
  <https://doi.org/10.29292/jics.v10i2.412>.
