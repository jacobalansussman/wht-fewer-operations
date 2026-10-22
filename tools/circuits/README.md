# tools/circuits: small circuits for the Walsh-Hadamard transform

This folder holds explicit circuits for the Walsh-Hadamard transform on N = 2^k points that use fewer
operations than the textbook's N log2 N, with the programs that check them and the programs that found them.
A *circuit* is a list of lines; each line makes one new value from one or two earlier values. These circuits
lower the constant in front of N log2 N. They do not change the order of growth.

One command, run from the top folder of the repository, replays everything:

    python3 -B tools/circuits/run.py

It needs Python 3.9 or later with its standard library, about a minute and about 700 MB of memory.
It reads every circuit from its text file and checks it against the definition of the transform in exact
arithmetic. It prints the tables for N = 2 to 16,384: the textbook, Alman and Rao's published formulas, and
these circuits. It writes the Lean data file again from the 20-line program and compares it byte for byte with
`lean/Work/SmallWHT/H8Half.lean`, the file in the Lean project at the top of the repository. The last line is
`OK ...`, or `FAILED:` with the first difference.
`expected-output.txt` is what it printed in the recorded run; your output should be the same bytes. The default run
replays sizes up to 4,096 points; `--kmax 14` replays the last two sizes of the tables as well (8 to 9
minutes and about 3 GB of memory on a Linux machine; `expected-output-kmax14.txt`).

**The two counts.** In count (G) one gate is any a·u + b·v, so a multiplication by a constant is free. In
count (O) every addition, every subtraction and every multiplication by a constant costs one; this is the
gate set of OpenAI's circuit model.

| circuit | where | count (G) | count (O) | textbook | checked by |
|---|---|---|---|---|---|
| 4 points | `programs/h4_7gates.txt` | 7 | 11 | 8 | Python; Lean (the same 7 lines) |
| 8 points | `programs/h8_19gates.txt` | 19 | 31 | 24 | Python; Lean (the same 19 lines) |
| 8 points, every output halved | `programs/h8_half_20ops.txt` | 19 | 20 | 24 for the exact transform, which costs 28 by this route | Python; the 20 also by Lean (see below) |
| 16 points | `programs/h16_52gates.txt` | 52 | 84 | 64 | Python; Lean proves that a circuit of at most 52 lines exists (the theorem at 16 points), not this file |
| every N = 2^k from 4 | `gen.py`, construction 1 | (3/4) N log2 N + N/4 | | N log2 N | Lean, the bound at every N = 2^k (not the gate lists); Python, to 16,384 points |
| N a power of 8, exact transform | the 20-operation program in layers, then N multiplications | | (5/6) N log2 N + N | N log2 N | Lean (see below); Python at 8, 64, 512 and 4,096 points |

The last row is 4,352 operations at 512 points, against 4,608. Below 512 points it does not beat the textbook.

**What Lean checks.** The 20 operations, and the last row: the theorem `hadamard_pow8_circuit` in
`lean/Work/SmallWHT/` (the folder `lean/` at the top of the repository) says that for N = 8^j the exact
transform has a circuit in OpenAI's model with at most 20·j·8^(j-1) + 8^j gates. Its only data is the 20-line
program `lean/h8_half_o20.txt` of this folder. [VERIFY.md](../../VERIFY.md) says how these Lean files were
checked, and the limits of that check. The theorem `hadamard_mulAdd_circuit` in `lean/Work/WHT34/` says that
for N = 2^k the exact transform has a circuit of multiply-add lines with at most (3/4) N log2 N + N/4 lines, so
it covers the 52 and the rate 3/4; the 19 lines and the 7 lines are written out in
`lean/Work/WHT34/ChallengeWHT34Checks.lean`. Every other number here is checked by the Python programs of this
folder and not by Lean: the tables, and every list of gates above 8 points.

**Credit.** Seven operations at 4 points are due to Coppersmith, Feig and Linzer (1994, page 969). They
count one multiply-add, ±a ± b·c, as one operation, and give (7/8) N log2 N operations when N is a power of
four and N/8 more when N is an odd power of two. Their formula gives 22 operations at 8 points and 56 at 16.
Every line of my count-(G) circuits has two terms and at most one multiplication by a constant, so each
line is one of their operations: 19 against 22, 52 against 56 and the rate 3/4 against 7/8 are comparisons
in their own count. They claim no lower bound, and I do not claim that my counts are the least possible.
The best count of the explicit form c·N log2 N plus a multiple of N that I found in print for the exact
transform with everything charged is Alman and Rao's (2023) (counts of a smaller order are in print; see the
README):
at most (23/24) N log2 N + (13/12) N, and (23/24) N log2 N + N - 1 when N is a power of 8. The method of
the 20-operation circuit is theirs too: the 8-point matrix written as a part of low rank plus a sparse part,
and one halving. The circuit model is OpenAI's. I did not find the other rows of the table in the literature
I searched: the papers that the indexes list as citing those two, seven patent pages, arXiv, and the first
part of one survey. `ga_count.py` prints the computation on the count that Grigoryan and Agaian (2000)
state; [the note](../../notes/explicit-circuits.md), section 7, says what it shows and has the literature
search.

**Files.** `slp.py` defines the text format, the two counts and the exact checker. `gen.py` states the
constructions as recursions. `tables.py` prints the tables. `multiply_add_check.py` checks that every line
of every circuit file is one operation in the sense of the 1994 paper, and `ga_count.py` prints the
computation on the count of Grigoryan and Agaian; each takes a second and ends with `OK ...`.
`count_tables.py` (added in revision 2) builds the circuits of five constructions, the textbook, Coppersmith,
Feig and Linzer's, Alman and Rao's, the 5/6 circuit and the 3/4 family, at 8 to 4,096 points, checks each, and
prints the exact count tables of the README in both counts, to 32,768 points (about 5 s; it ends with `OK ...`;
`expected-output-count-tables.txt` is what it printed).
`programs/` has the circuits as text. `fast/wht56/` has them as working programs and `fpga/` as hardware
(both described below). `search/`
has the search programs as they were run; its README says for each what it searches, what it found, how
long it takes and what it does not show. `lean/` (in this folder) has the 20-line program and the program
that writes the Lean data file from it; it is not the Lean project, which is the folder `lean/` at the top.
I found these circuits on the night of 10 to 11 October 2026 with a team of AI agents (Anthropic's Claude)
that I directed, as a by-product of a search for a transform of linear size, which I did not find.
The agents wrote the programs here and ran them.

**The circuits as working programs.** [fast/wht56/](fast/wht56/README.md) computes the transform of real
data with these circuits, in pure Python, in numpy and in C, so that the counts can be seen on a running
program: a counter in the pure-Python version performs 4,352 operations at 512 points. Its tests compare
every program with the definition of the transform up to 1,024 points; from the folder `fast/` the command
is `python3 -B -m wht56 --selftest`. Its README has the timings. The test that counts is
in [fast/wht56/results/ffht/](fast/wht56/results/ffht/README.md): the 8-point step written into the
generated code of FFHT, a tuned open-source library for this transform, in place of its block of 24
additions and subtractions. On the one machine that was timed it did not make FFHT faster at any size from
2^6 to 2^26 points (from 2^5 in double precision); all 129 combinations of size and form took more time
than a second build of FFHT's unchanged code. In my own plain C on two machines the time did not follow the operation count either, and
the gain it showed at some sizes on one machine comes from how the compiler treated one pass, not from the
step. Nothing in that folder is checked by Lean, and `run.py` does not run it.
A kernel with FFHT's entry points and the 20-operation 8-point step of the 3/4 family, cut from the timing program
of 22 October 2026,
is in [../fht-kernel/](../fht-kernel/README.md); the timings of that day are in
[measurements/2026-10-22/](../../measurements/2026-10-22/README.md).

**The circuits as hardware.** [fpga/](fpga/README.md) builds the circuits for an FPGA (a chip whose logic
is set by loading a file into it, made of units called logic cells) with open-source tools. As one block
of adders with no registers inside (rows of one-bit memories between the adders, which let the clock run
faster), the 19-adder 8-point circuit takes 274 logic cells where the textbook network takes 349 on a
Lattice iCE40HX8K, or 273 against 337 with the synthesis option `-dff`. It is twice as deep, so it is slower by the
tools' estimates (about 72 MHz against about 97 MHz), it is larger than the textbook once registers are
added for speed, and it is not the smallest design on that chip: the 22-adder step of Alman and Rao takes
244 cells. No existing design was improved. That README has the tables, the family from 16 to 256 points,
and how to run the tools again.
