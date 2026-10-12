# Where each report is, and how to run a program again

The agents worked in one flat folder and gave every report a short label, such as `g-1` or `e2-0`. The reports cite each other by these labels. Here the reports are sorted into ten folders, one per wave, so this page says where each label went.

**Status of everything listed here.** The work of AI agents (Anthropic's Claude) that I directed. No person has reviewed it, and none of it is in Lean (a proof checker). The one proof in Lean, of a circuit with at most (5/6)·N·log2 N + N operations for N = 8^j points, is in the `lean/` folder of this repository, not in these folders.

## Names the reports use

- **The notes.** `NOTE.md` is the first wave's note. `WAVE2-NOTE.md` to `WAVE10-NOTE.md` are the notes of the later waves. Each one is now the file `NOTE.md` inside its wave's folder.
- **Paths that begin with `waves/`** are counted from the top folder of this repository. The agents wrote the full path of the folder on my Mac; a script replaced that by the file's new place. In a shell script, where a line `cd waves/...` had been such a full path, the script also added ` || exit 1` after it, so that a script started from the wrong folder stops instead of working where it was started. Nothing else on those lines changed.
- **`waves` on its own** stands for the flat working folder. A brief that says "files go under `waves/<label>/`" means the folder that is now `waves/wave-NN/<label>/`.
- **`(not in this repository)`** in front of a name marks a file of mine that is not published here. In programs and outputs the same mark is spelled `not-in-this-repository/`, so that a script stays well formed. The names that follow it:
  - `wht35/bin/light.py` is a small wrapper of mine that ran one command with a time limit and a memory cap, so that it could not disturb other jobs on the machine. Its two arguments are a label and the seconds allowed.
  - `wht33/fatlabels/venv/bin/python` is a Python on my Mac that has numpy and scipy installed.
  - `wht-power-saving-r4-candidate` is a working copy of my other repository at its fourth revision. That repository has the saving of 8.762479e-4, which the reports round to 8.7625e-4. Some reports shorten its name to `R`, so `R/OAI/Computability/FourierCircuit/Core.lean` is OpenAI's Lean file inside that copy; in this repository the same file is `lean/OAI/Computability/FourierCircuit/Core.lean`. The reports call its mechanism "the engine" and its result "the published unit".
  - `upstream/openai-math` is a copy on my Mac of OpenAI's public repository https://github.com/openai/math, which holds its preprints and Lean files.
  - other names that begin with `wht33`, `wht35`, `wht37` or `wht38` are folders of my earlier work on the same problem.
- **`(the Linux machine's working folder)`**: some heavier runs were made on a rented Linux machine. Its copies of the files are not here; what an agent copied back is in that agent's folder.
- **Twelve small shell scripts reached that machine** (`rsh.sh`, `rcp.sh`, `remote.sh`, `rs.sh` in seven folders). In each, the line with the command, the key file, the port and the host name was replaced by a line that prints "remote login removed" or "remote copy removed" and stops. They are kept because the reports name them. Five other scripts, which stopped or restarted jobs on my machines, are left out; `wave-03/LEFT-OUT.md` and `wave-08/LEFT-OUT.md` list them.
- **`(a temporary folder)`** in two saved outputs stands for a temporary folder of the session that ran the command.
- **`[path cut short]`**: the wrapper printed the command line it had run and cut it at a fixed length, in a few places in the middle of a path.
- **"The user"** is me.
- **"Private", "nothing published", "no git"** at the top of many reports: that was their status on the night they were written, and an order to the agents not to publish anything themselves. I decided to publish them afterwards.
- **"Editor's note (11 October 2026)"** at the top of 48 reports was added by the agents at my direction. It adds two lines, so a line number that another report gives for that report is two too small.

## Running a program again

This copy was tried on three programs only: `wave-01/d-0-zeta/mincirc.c` builds with the command below and runs; after the links of point 3 were made, `wave-05/p-7-twoletters/letters.py` ran from the top folder and printed the same first lines as its saved output, and `wave-06/u-4-zdz/crosscheck.py` ran from its own folder. The other programs have not been run again from this copy. On 11 October, while the leads were checked, four more were run from this copy and behaved as the reports say: `wave-04/h-3-orecord/oprice.py`, `wave-03/g-1-tightwires/sa8.py`, and `mincirc.c` and `mincirc_all.c` of `wave-01/d-0-zeta/`. What a reader will need:

**What the programs need.** Python 3.9 or later. Of the 801 Python programs, 83 import numpy, scipy or sympy; the rest use the standard library only. There are 93 C programs; `cc -O2` builds them, 25 of them use the mathematics library and may need `-lm` as well, and one (`wave-02/e2-3-drain/drain.c`) needs `-fopenmp`. A build writes the compiled program next to the source, inside this repository: do not commit it, or build it outside, for example `cc -O2 -o ../mincirc waves/wave-01/d-0-zeta/mincirc.c` from the top folder puts it one level above the repository. Read a script before you run it: some start up to eight jobs at once, and each wave's index names those.

1. **Compiled programs are not here.** Each wave's `LEFT-OUT.md` names them, with the C source where the names match. Build one with a C compiler inside its folder, for example `cc -O2 -o mincirc mincirc.c`. Some sources need `-lm` or `-fopenmp` as well. More than a hundred places call one compiled program, `waves/wave-01/d-0-zeta/mincirc`; build that one first.
2. **Paths that begin with `waves/`** inside a program are counted from the top folder of the repository, so start such a program from there.
3. **Programs that reach into another agent's folder** write `../<folder>/`. In the flat working folder every folder was a neighbour of every other. Here a neighbour may be in another wave. `sh waves/link-waves.sh` makes, in every wave folder, a link to each folder of the other waves, and then these paths work again. `sh waves/link-waves.sh undo` removes the links. Do not commit them.
4. **The wrapper.** Where a command begins with `python3 -B not-in-this-repository/wht35/bin/light.py <label> <seconds>`, leave the wrapper, its label and its number of seconds out and run the rest.
5. **Missing inputs.** A program may ask for a file that is listed in `LEFT-OUT.md` or marked as not in this repository. I did not check which of these can be made again from what is here, except for three that a lead of [LEADS.md](LEADS.md) needs:
   - `wave-09/ad-2-twodeliveries/z8_sets.txt` (lead 2.3), the list of all least circuits for subset sums at 8 points modulo 2. Build `wave-01/d-0-zeta/mincirc_all.c` and run `mincirc_all 2 8 5 100000 < waves/wave-01/d-0-zeta/rows_zeta3.txt > z8_sets.txt`. It takes about 9 seconds and prints 2,802 sets. The fourth argument, the largest number of sets to print, is not in the program's usage line. The file made this way has one line fewer than the original (2,811 against 2,812), and I did not check that the sets come in the same order; the reports name a set by its number in the original order.
   - `wave-04/h-3-orecord/ox_512.txt` (the exact transform at 512 points in 4,352 operations). `python3 -B orec.py` in that folder writes it again in a few seconds, together with the other `o_N.txt` and `ox_N.txt` files, which it overwrites. The same program is also in this repository as `tools/circuits/programs/generated/O_layers8_512_exact.txt`.
   - the long outputs of `wave-04/h-4-zetafloor/` at 16 points (lead 2.1). They are logs of random searches, and the report gives their results; a new run gives a new log, not the same one.
6. **Arguments that the programs do not explain.** `mincirc p n m rowsfile` asks whether subset sums or another table given by its rows has a circuit with m helpers modulo p; it needs p^n to be at most about 6 million. In `wave-04/h-1-staircase3/sa.c` and `sa2.c` the arguments `A` and `B` are the weights that the search puts on a helper it cannot make and on a missing output. The runs made on the Linux machine have no saved command line; the runs made on my Mac end with a line `cmd=...` that gives it.
7. **Four ways of writing a circuit.** g-1 writes `g1 = x0 + x7`; e2-0 and h-1 write `name = a * u + b * v`; g-1's search `sa8.py` prints a list of values; the walking searches of waves 7 and 8 print blocks that begin `CIRCUIT`. No program here converts between them. The cleaned circuits in `tools/circuits/programs/` use one format, and `python3 -B tools/circuits/slp.py FILE` checks a file in it.

## Every label

167 reports. The ten notes are not in the table: each is `NOTE.md` in its wave's folder.

| Label | Wave | Report | Folder of programs |
|---|---|---|---|
| `a-0` | 1 | [wave-01/a-0.md](wave-01/a-0.md) | [a-0/](wave-01/a-0/) |
| `a-1` | 1 | [wave-01/a-1.md](wave-01/a-1.md) | [a-1/](wave-01/a-1/) |
| `a-2` | 1 | [wave-01/a-2.md](wave-01/a-2.md) | [a-2/](wave-01/a-2/) |
| `aa-cross` | 8 | [wave-08/aa-cross.md](wave-08/aa-cross.md) | [aa-cross/](wave-08/aa-cross/) |
| `aa-note` | 8 | [wave-08/aa-note.md](wave-08/aa-note.md) | [aa-note/](wave-08/aa-note/) |
| `ab-0` | 8 | [wave-08/ab-0.md](wave-08/ab-0.md) | [ab-0-neighboursums/](wave-08/ab-0-neighboursums/) |
| `ab-1` | 8 | [wave-08/ab-1.md](wave-08/ab-1.md) | [ab-1-fewerblocks/](wave-08/ab-1-fewerblocks/) |
| `ab-2` | 8 | [wave-08/ab-2.md](wave-08/ab-2.md) | [ab-2-tallpool/](wave-08/ab-2-tallpool/) |
| `ab-3` | 8 | [wave-08/ab-3.md](wave-08/ab-3.md) | [ab-3-convladder/](wave-08/ab-3-convladder/) |
| `ab-4` | 8 | [wave-08/ab-4.md](wave-08/ab-4.md) | [ab-4-zcut/](wave-08/ab-4-zcut/) |
| `ab-5` | 8 | [wave-08/ab-5.md](wave-08/ab-5.md) | [ab-5-cancellit/](wave-08/ab-5-cancellit/) |
| `ab-6` | 8 | [wave-08/ab-6.md](wave-08/ab-6.md) | [ab-6-chainexchanges/](wave-08/ab-6-chainexchanges/) |
| `ab-7` | 8 | [wave-08/ab-7.md](wave-08/ab-7.md) | [ab-7-transforminarow/](wave-08/ab-7-transforminarow/) |
| `ab-8` | 8 | [wave-08/ab-8.md](wave-08/ab-8.md) | [ab-8-reconcilecaps/](wave-08/ab-8-reconcilecaps/) |
| `ac-0` | 8 | [wave-08/ac-0.md](wave-08/ac-0.md) | [ac-0/](wave-08/ac-0/) |
| `ac-1` | 8 | [wave-08/ac-1.md](wave-08/ac-1.md) | [ac-1/](wave-08/ac-1/) |
| `ac-2` | 8 | [wave-08/ac-2.md](wave-08/ac-2.md) | [ac-2/](wave-08/ac-2/) |
| `ad-0` | 9 | [wave-09/ad-0.md](wave-09/ad-0.md) | [ad-0-rateperblock/](wave-09/ad-0-rateperblock/) |
| `ad-1` | 9 | [wave-09/ad-1.md](wave-09/ad-1.md) | [ad-1-linesums/](wave-09/ad-1-linesums/) |
| `ad-2` | 9 | [wave-09/ad-2.md](wave-09/ad-2.md) | [ad-2-twodeliveries/](wave-09/ad-2-twodeliveries/) |
| `ad-3` | 9 | [wave-09/ad-3.md](wave-09/ad-3.md) | [ad-3-straightenquadri/](wave-09/ad-3-straightenquadri/) |
| `ad-4` | 9 | [wave-09/ad-4.md](wave-09/ad-4.md) | [ad-4-flatrank/](wave-09/ad-4-flatrank/) |
| `ad-5` | 9 | [wave-09/ad-5.md](wave-09/ad-5.md) | [ad-5-whichbent/](wave-09/ad-5-whichbent/) |
| `ad-6` | 9 | [wave-09/ad-6.md](wave-09/ad-6.md) | [ad-6-twohelpers/](wave-09/ad-6-twohelpers/) |
| `ad-7` | 9 | [wave-09/ad-7.md](wave-09/ad-7.md) | [ad-7-modulo4/](wave-09/ad-7-modulo4/) |
| `ae-cross` | 9 | [wave-09/ae-cross.md](wave-09/ae-cross.md) | [ae-cross/](wave-09/ae-cross/) |
| `ae-note` | 9 | [wave-09/ae-note.md](wave-09/ae-note.md) | [ae-note/](wave-09/ae-note/) |
| `af-0` | 9 | [wave-09/af-0.md](wave-09/af-0.md) | [af-0/](wave-09/af-0/) |
| `af-1` | 9 | [wave-09/af-1.md](wave-09/af-1.md) | [af-1/](wave-09/af-1/) |
| `af-2` | 9 | [wave-09/af-2.md](wave-09/af-2.md) | [af-2/](wave-09/af-2/) |
| `ag-0` | 10 | [wave-10/ag-0.md](wave-10/ag-0.md) | [ag-0-ladderdegree3/](wave-10/ag-0-ladderdegree3/) |
| `ag-1` | 10 | [wave-10/ag-1.md](wave-10/ag-1.md) | [ag-1-halvingornothing/](wave-10/ag-1-halvingornothing/) |
| `ag-2` | 10 | [wave-10/ag-2.md](wave-10/ag-2.md) | [ag-2-firstbusthatpays/](wave-10/ag-2-firstbusthatpays/) |
| `ag-3` | 10 | [wave-10/ag-3.md](wave-10/ag-3.md) | [ag-3-sectorandport/](wave-10/ag-3-sectorandport/) |
| `ag-4` | 10 | [wave-10/ag-4.md](wave-10/ag-4.md) | [ag-4-cheapestgenerato/](wave-10/ag-4-cheapestgenerato/) |
| `ag-5` | 10 | [wave-10/ag-5.md](wave-10/ag-5.md) | [ag-5-threehelpers/](wave-10/ag-5-threehelpers/) |
| `ag-6` | 10 | [wave-10/ag-6.md](wave-10/ag-6.md) | [ag-6-deepgates/](wave-10/ag-6-deepgates/) |
| `ag-7` | 10 | [wave-10/ag-7.md](wave-10/ag-7.md) | [ag-7-rankdial/](wave-10/ag-7-rankdial/) |
| `ag-8` | 10 | [wave-10/ag-8.md](wave-10/ag-8.md) | [ag-8-bestbadcircuit/](wave-10/ag-8-bestbadcircuit/) |
| `ag-9` | 10 | [wave-10/ag-9.md](wave-10/ag-9.md) | [ag-9-irrationalconsta/](wave-10/ag-9-irrationalconsta/) |
| `ah-cross` | 10 | [wave-10/ah-cross.md](wave-10/ah-cross.md) | [ah-cross/](wave-10/ah-cross/) |
| `ah-note` | 10 | [wave-10/ah-note.md](wave-10/ah-note.md) | [ah-note/](wave-10/ah-note/) |
| `ai-0` | 10 | [wave-10/ai-0.md](wave-10/ai-0.md) | [ai-0/](wave-10/ai-0/) |
| `ai-1` | 10 | [wave-10/ai-1.md](wave-10/ai-1.md) | [ai-1/](wave-10/ai-1/) |
| `ai-2` | 10 | [wave-10/ai-2.md](wave-10/ai-2.md) | [ai-2/](wave-10/ai-2/) |
| `b-0` | 2 | [wave-02/b-0.md](wave-02/b-0.md) | [b-0/](wave-02/b-0/) |
| `b-1` | 2 | [wave-02/b-1.md](wave-02/b-1.md) | [b-1/](wave-02/b-1/) |
| `b-2` | 2 | [wave-02/b-2.md](wave-02/b-2.md) | [b-2/](wave-02/b-2/) |
| `c-0` | 3 | [wave-03/c-0.md](wave-03/c-0.md) | [c-0/](wave-03/c-0/) |
| `c-1` | 3 | [wave-03/c-1.md](wave-03/c-1.md) | [c-1/](wave-03/c-1/) |
| `c-2` | 3 | [wave-03/c-2.md](wave-03/c-2.md) | [c-2/](wave-03/c-2/) |
| `d-0` | 1 | [wave-01/d-0.md](wave-01/d-0.md) | [d-0-zeta/](wave-01/d-0-zeta/) |
| `d-1` | 1 | [wave-01/d-1.md](wave-01/d-1.md) | [d-1-plane/](wave-01/d-1-plane/) |
| `d-2` | 1 | [wave-01/d-2.md](wave-01/d-2.md) | [d-2-letters/](wave-01/d-2-letters/) |
| `d-3` | 1 | [wave-01/d-3.md](wave-01/d-3.md) | [d-3-mod4/](wave-01/d-3-mod4/) |
| `d-4` | 1 | [wave-01/d-4.md](wave-01/d-4.md) | [d-4-codes/](wave-01/d-4-codes/) |
| `d-5` | 1 | [wave-01/d-5.md](wave-01/d-5.md) | [d-5-border/](wave-01/d-5-border/) |
| `d-6` | 1 | [wave-01/d-6.md](wave-01/d-6.md) | [d-6-excess/](wave-01/d-6-excess/) |
| `d-7` | 1 | [wave-01/d-7.md](wave-01/d-7.md) | [d-7-spin/](wave-01/d-7-spin/) |
| `e-0` | 2 | [wave-02/e-0.md](wave-02/e-0.md) | [e-0-ring/](wave-02/e-0-ring/) |
| `e-1` | 2 | [wave-02/e-1.md](wave-02/e-1.md) | [e-1-vcycle/](wave-02/e-1-vcycle/) |
| `e-2` | 2 | [wave-02/e-2.md](wave-02/e-2.md) | [e-2-density/](wave-02/e-2-density/) |
| `e-3` | 2 | [wave-02/e-3.md](wave-02/e-3.md) | [e-3-cutoff/](wave-02/e-3-cutoff/) |
| `e-4` | 2 | [wave-02/e-4.md](wave-02/e-4.md) | [e-4-passes/](wave-02/e-4-passes/) |
| `e-5` | 2 | [wave-02/e-5.md](wave-02/e-5.md) | [e-5-conserved/](wave-02/e-5-conserved/) |
| `e-6` | 2 | [wave-02/e-6.md](wave-02/e-6.md) | [e-6-shifts/](wave-02/e-6-shifts/) |
| `e-7` | 2 | [wave-02/e-7.md](wave-02/e-7.md) | [e-7-halftouch/](wave-02/e-7-halftouch/) |
| `e2-0` | 2 | [wave-02/e2-0.md](wave-02/e2-0.md) | [e2-0-pieces/](wave-02/e2-0-pieces/) |
| `e2-1` | 2 | [wave-02/e2-1.md](wave-02/e2-1.md) | [e2-1-dictionary/](wave-02/e2-1-dictionary/) |
| `e2-2` | 2 | [wave-02/e2-2.md](wave-02/e2-2.md) | [e2-2-ladder/](wave-02/e2-2-ladder/) |
| `e2-3` | 2 | [wave-02/e2-3.md](wave-02/e2-3.md) | [e2-3-drain/](wave-02/e2-3-drain/) |
| `g-0` | 3 | [wave-03/g-0.md](wave-03/g-0.md) | [g-0-mirror/](wave-03/g-0-mirror/) |
| `g-1` | 3 | [wave-03/g-1.md](wave-03/g-1.md) | [g-1-tightwires/](wave-03/g-1-tightwires/) |
| `g-2` | 3 | [wave-03/g-2.md](wave-03/g-2.md) | [g-2-basischange/](wave-03/g-2-basischange/) |
| `g-3` | 3 | [wave-03/g-3.md](wave-03/g-3.md) | [g-3-illconditioned/](wave-03/g-3-illconditioned/) |
| `g-4` | 3 | [wave-03/g-4.md](wave-03/g-4.md) | [g-4-zetalead/](wave-03/g-4-zetalead/) |
| `g-5` | 3 | [wave-03/g-5.md](wave-03/g-5.md) | [g-5-k3/](wave-03/g-5-k3/) |
| `g-6` | 3 | [wave-03/g-6.md](wave-03/g-6.md) | [g-6-twosteps/](wave-03/g-6-twosteps/) |
| `g-7` | 3 | [wave-03/g-7.md](wave-03/g-7.md) | [g-7-thirdturn/](wave-03/g-7-thirdturn/) |
| `h-0` | 4 | [wave-04/h-0.md](wave-04/h-0.md) | [h-0-onepergate/](wave-04/h-0-onepergate/) |
| `h-1` | 4 | [wave-04/h-1.md](wave-04/h-1.md) | [h-1-staircase3/](wave-04/h-1-staircase3/) |
| `h-2` | 4 | [wave-04/h-2.md](wave-04/h-2.md) | [h-2-clique17/](wave-04/h-2-clique17/) |
| `h-3` | 4 | [wave-04/h-3.md](wave-04/h-3.md) | [h-3-orecord/](wave-04/h-3-orecord/) |
| `h-4` | 4 | [wave-04/h-4.md](wave-04/h-4.md) | [h-4-zetafloor/](wave-04/h-4-zetafloor/) |
| `h-5` | 4 | [wave-04/h-5.md](wave-04/h-5.md) | [h-5-ladderbound/](wave-04/h-5-ladderbound/) |
| `h-6` | 4 | [wave-04/h-6.md](wave-04/h-6.md) | [h-6-classhub/](wave-04/h-6-classhub/) |
| `h-7` | 4 | [wave-04/h-7.md](wave-04/h-7.md) | [h-7-unitmeter/](wave-04/h-7-unitmeter/) |
| `h-8` | 4 | [wave-04/h-8.md](wave-04/h-8.md) | [h-8-provethewrongthi/](wave-04/h-8-provethewrongthi/) |
| `i-backwards` | 1 | [wave-01/i-backwards.md](wave-01/i-backwards.md) | [i-backwards/](wave-01/i-backwards/) |
| `i-cousins` | 1 | [wave-01/i-cousins.md](wave-01/i-cousins.md) | [i-cousins/](wave-01/i-cousins/) |
| `i-cross` | 1 | [wave-01/i-cross.md](wave-01/i-cross.md) | [i-cross/](wave-01/i-cross/) |
| `i-fields` | 1 | [wave-01/i-fields.md](wave-01/i-fields.md) | [i-fields/](wave-01/i-fields/) |
| `i-hatch` | 1 | [wave-01/i-hatch.md](wave-01/i-hatch.md) | [i-hatch/](wave-01/i-hatch/) |
| `i-model` | 1 | [wave-01/i-model.md](wave-01/i-model.md) | [i-model/](wave-01/i-model/) |
| `i-note` | 1 | [wave-01/i-note.md](wave-01/i-note.md) | [i-note/](wave-01/i-note/) |
| `i-play` | 1 | [wave-01/i-play.md](wave-01/i-play.md) | [i-play/](wave-01/i-play/) |
| `i-represent` | 1 | [wave-01/i-represent.md](wave-01/i-represent.md) | [i-represent/](wave-01/i-represent/) |
| `i-wild` | 1 | [wave-01/i-wild.md](wave-01/i-wild.md) | [i-wild/](wave-01/i-wild/) |
| `j-cross` | 2 | [wave-02/j-cross.md](wave-02/j-cross.md) | [j-cross/](wave-02/j-cross/) |
| `j-failproof` | 2 | [wave-02/j-failproof.md](wave-02/j-failproof.md) | [j-failproof/](wave-02/j-failproof/) |
| `j-generalize` | 2 | [wave-02/j-generalize.md](wave-02/j-generalize.md) | [j-generalize/](wave-02/j-generalize/) |
| `j-machine` | 2 | [wave-02/j-machine.md](wave-02/j-machine.md) | [j-machine/](wave-02/j-machine/) |
| `j-manyatonce` | 2 | [wave-02/j-manyatonce.md](wave-02/j-manyatonce.md) | [j-manyatonce/](wave-02/j-manyatonce/) |
| `j-note` | 2 | [wave-02/j-note.md](wave-02/j-note.md) | [j-note/](wave-02/j-note/) |
| `k-cross` | 3 | [wave-03/k-cross.md](wave-03/k-cross.md) | [k-cross/](wave-03/k-cross/) |
| `k-note` | 3 | [wave-03/k-note.md](wave-03/k-note.md) | [k-note/](wave-03/k-note/) |
| `lit-constants` | 3 | [wave-03/lit-constants.md](wave-03/lit-constants.md) | none |
| `m-cross` | 4 | [wave-04/m-cross.md](wave-04/m-cross.md) | [m-cross/](wave-04/m-cross/) |
| `m-note` | 4 | [wave-04/m-note.md](wave-04/m-note.md) | [m-note/](wave-04/m-note/) |
| `n-0` | 4 | [wave-04/n-0.md](wave-04/n-0.md) | [n-0/](wave-04/n-0/) |
| `n-1` | 4 | [wave-04/n-1.md](wave-04/n-1.md) | [n-1/](wave-04/n-1/) |
| `n-2` | 4 | [wave-04/n-2.md](wave-04/n-2.md) | [n-2/](wave-04/n-2/) |
| `p-0` | 5 | [wave-05/p-0.md](wave-05/p-0.md) | [p-0-classtest/](wave-05/p-0-classtest/) |
| `p-1` | 5 | [wave-05/p-1.md](wave-05/p-1.md) | [p-1-letter16/](wave-05/p-1-letter16/) |
| `p-2` | 5 | [wave-05/p-2.md](wave-05/p-2.md) | [p-2-mirror64class/](wave-05/p-2-mirror64class/) |
| `p-3` | 5 | [wave-05/p-3.md](wave-05/p-3.md) | [p-3-hatch32/](wave-05/p-3-hatch32/) |
| `p-4` | 5 | [wave-05/p-4.md](wave-05/p-4.md) | [p-4-formula/](wave-05/p-4-formula/) |
| `p-5` | 5 | [wave-05/p-5.md](wave-05/p-5.md) | [p-5-unimodular/](wave-05/p-5-unimodular/) |
| `p-6` | 5 | [wave-05/p-6.md](wave-05/p-6.md) | [p-6-selftranspose/](wave-05/p-6-selftranspose/) |
| `p-7` | 5 | [wave-05/p-7.md](wave-05/p-7.md) | [p-7-twoletters/](wave-05/p-7-twoletters/) |
| `p-8` | 5 | [wave-05/p-8.md](wave-05/p-8.md) | [p-8-fibonacci/](wave-05/p-8-fibonacci/) |
| `PICKS` | 1 | [wave-01/PICKS.md](wave-01/PICKS.md) | none |
| `q-cross` | 5 | [wave-05/q-cross.md](wave-05/q-cross.md) | [q-cross/](wave-05/q-cross/) |
| `q-note` | 5 | [wave-05/q-note.md](wave-05/q-note.md) | [q-note/](wave-05/q-note/) |
| `r-0` | 5 | [wave-05/r-0.md](wave-05/r-0.md) | [r-0/](wave-05/r-0/) |
| `r-1` | 5 | [wave-05/r-1.md](wave-05/r-1.md) | [r-1/](wave-05/r-1/) |
| `r-2` | 5 | [wave-05/r-2.md](wave-05/r-2.md) | [r-2/](wave-05/r-2/) |
| `s-cross` | 6 | [wave-06/s-cross.md](wave-06/s-cross.md) | [s-cross/](wave-06/s-cross/) |
| `s-note` | 6 | [wave-06/s-note.md](wave-06/s-note.md) | [s-note/](wave-06/s-note/) |
| `u-0` | 6 | [wave-06/u-0.md](wave-06/u-0.md) | [u-0-cornerssearch/](wave-06/u-0-cornerssearch/) |
| `u-1` | 6 | [wave-06/u-1.md](wave-06/u-1.md) | [u-1-cornerstheory/](wave-06/u-1-cornerstheory/) |
| `u-2` | 6 | [wave-06/u-2.md](wave-06/u-2.md) | [u-2-onerun/](wave-06/u-2-onerun/) |
| `u-3` | 6 | [wave-06/u-3.md](wave-06/u-3.md) | [u-3-zletter/](wave-06/u-3-zletter/) |
| `u-4` | 6 | [wave-06/u-4.md](wave-06/u-4.md) | [u-4-zdz/](wave-06/u-4-zdz/) |
| `u-5` | 6 | [wave-06/u-5.md](wave-06/u-5.md) | [u-5-unit2adic/](wave-06/u-5-unit2adic/) |
| `u-6` | 6 | [wave-06/u-6.md](wave-06/u-6.md) | [u-6-twotrees/](wave-06/u-6-twotrees/) |
| `u-7` | 6 | [wave-06/u-7.md](wave-06/u-7.md) | [u-7-quotient/](wave-06/u-7-quotient/) |
| `u-8` | 6 | [wave-06/u-8.md](wave-06/u-8.md) | [u-8-compose/](wave-06/u-8-compose/) |
| `u-9` | 6 | [wave-06/u-9.md](wave-06/u-9.md) | [u-9-checkerboards/](wave-06/u-9-checkerboards/) |
| `v-0` | 6 | [wave-06/v-0.md](wave-06/v-0.md) | [v-0/](wave-06/v-0/) |
| `v-1` | 6 | [wave-06/v-1.md](wave-06/v-1.md) | [v-1/](wave-06/v-1/) |
| `v-2` | 6 | [wave-06/v-2.md](wave-06/v-2.md) | [v-2/](wave-06/v-2/) |
| `w-cross` | 7 | [wave-07/w-cross.md](wave-07/w-cross.md) | [w-cross/](wave-07/w-cross/) |
| `w-note` | 7 | [wave-07/w-note.md](wave-07/w-note.md) | [w-note/](wave-07/w-note/) |
| `WAVE10-PICKS` | 10 | [wave-10/WAVE10-PICKS.md](wave-10/WAVE10-PICKS.md) | none |
| `WAVE2-PICKS` | 2 | [wave-02/WAVE2-PICKS.md](wave-02/WAVE2-PICKS.md) | none |
| `WAVE2-PICKS-B` | 2 | [wave-02/WAVE2-PICKS-B.md](wave-02/WAVE2-PICKS-B.md) | none |
| `WAVE3-PICKS` | 3 | [wave-03/WAVE3-PICKS.md](wave-03/WAVE3-PICKS.md) | none |
| `WAVE4-PICKS` | 4 | [wave-04/WAVE4-PICKS.md](wave-04/WAVE4-PICKS.md) | none |
| `WAVE5-PICKS` | 5 | [wave-05/WAVE5-PICKS.md](wave-05/WAVE5-PICKS.md) | none |
| `WAVE6-PICKS` | 6 | [wave-06/WAVE6-PICKS.md](wave-06/WAVE6-PICKS.md) | [s-pick/](wave-06/s-pick/) |
| `WAVE7-PICKS` | 7 | [wave-07/WAVE7-PICKS.md](wave-07/WAVE7-PICKS.md) | none |
| `WAVE8-PICKS` | 8 | [wave-08/WAVE8-PICKS.md](wave-08/WAVE8-PICKS.md) | none |
| `WAVE9-PICKS` | 9 | [wave-09/WAVE9-PICKS.md](wave-09/WAVE9-PICKS.md) | none |
| `x-0` | 7 | [wave-07/x-0.md](wave-07/x-0.md) | [x-0-twojobs/](wave-07/x-0-twojobs/) |
| `x-1` | 7 | [wave-07/x-1.md](wave-07/x-1.md) | [x-1-digits/](wave-07/x-1-digits/) |
| `x-2` | 7 | [wave-07/x-2.md](wave-07/x-2.md) | [x-2-floorhatch/](wave-07/x-2-floorhatch/) |
| `x-3` | 7 | [wave-07/x-3.md](wave-07/x-3.md) | [x-3-boxrelations/](wave-07/x-3-boxrelations/) |
| `x-4` | 7 | [wave-07/x-4.md](wave-07/x-4.md) | [x-4-thirdturnbasis/](wave-07/x-4-thirdturnbasis/) |
| `x-5` | 7 | [wave-07/x-5.md](wave-07/x-5.md) | [x-5-weightedz/](wave-07/x-5-weightedz/) |
| `x-6` | 7 | [wave-07/x-6.md](wave-07/x-6.md) | [x-6-unitasbox/](wave-07/x-6-unitasbox/) |
| `x-7` | 7 | [wave-07/x-7.md](wave-07/x-7.md) | [x-7-rotate120/](wave-07/x-7-rotate120/) |
| `x-8` | 7 | [wave-07/x-8.md](wave-07/x-8.md) | [x-8-nearlydependent/](wave-07/x-8-nearlydependent/) |
| `x-9` | 7 | [wave-07/x-9.md](wave-07/x-9.md) | [x-9-growinghubs/](wave-07/x-9-growinghubs/) |
| `z-0` | 7 | [wave-07/z-0.md](wave-07/z-0.md) | [z-0/](wave-07/z-0/) |
| `z-1` | 7 | [wave-07/z-1.md](wave-07/z-1.md) | [z-1/](wave-07/z-1/) |
| `z-2` | 7 | [wave-07/z-2.md](wave-07/z-2.md) | [z-2/](wave-07/z-2/) |
