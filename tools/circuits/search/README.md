# tools/circuits/search: the programs that found the circuits

These are the search programs as they were run, with the outputs they wrote. I directed a team of AI agents
(Anthropic's Claude); they wrote these programs and ran them, and the programs are not tidied. The comments
use working words. "g-1", "e2-0-pieces", "d-0-zeta" and "j-machine" are the working names of the four runs,
and "a-2", "e-2-density" and "g-1-tightwires" are three more names of the same kind. Each is the label of a
report in the folder [waves/](../../../waves/README.md) at the top of the repository, or of the folder of
programs beside that report; [waves/WHERE.md](../../../waves/WHERE.md) has a table that says where each
one is. For example "g-1.md, section 1" is `waves/wave-03/g-1.md`. A "brief" is the task a run was given,
"the report" is what the run wrote at its end, and "tonight" is the night of 10 to 11 October 2026. Where a
recorded output ended with a line added by the job wrapper, that line was removed. One output that ended in
a crash is left out.

All four folders count as count (G) does: one gate is any a·u + b·v, and a multiplication by a constant is
free. The words: a *helper* is a value that a circuit makes and that is not an output. A *pool* is a fixed
list of candidate helpers. A *sign vector* is a list of +1 and -1.

One rule for reading every line below: **a search that finds nothing proves nothing.** "No circuit with 18
gates found" is a statement about the search. Only the two exhaustive programs, `mincirc.c` and `exact8.py`,
give a "no" that is a fact, and then only for the prime or the design they ran in. Nothing in this folder is
checked by Lean.

"Checked from a fresh copy" below means: this folder was copied to an empty place and the command was run
there, by the agents. On the Mac that was the system `python3` (3.9.6, standard library) or `cc`. Two of the
programs that were run again, `flipwalk.py` and `steiner.py`, need numpy, which the Mac's system Python does
not have; those were run on a Linux machine with Python 3.13 and numpy 2.1.

## 1. `walk19/`: the search that found the 19 gates at 8 points

- **`sa8.py`** (with `pool.py`, `ref.py`, `ledger.py`). The state is a set of helpers taken from a pool of 304
  values at 8 points: every sign vector on a coset of the addresses whose signs follow a rule of degree at most
  3. A state is a circuit when every helper and every output lies on a line through two values made before it.
  The program anneals: it adds, removes and swaps helpers.
  - *What it found.* Started from the 22-gate circuit (two 4-point circuits and one textbook layer, which is
    how the 1994 paper of Coppersmith, Feig and Linzer treats an odd power of two), each of
    four runs fell to 21, 20 and then 19 gates within 20 seconds (`sa8_known0.out` to `sa8_known3.out`). Then it
    tried every exchange around the 19: remove one helper, or remove two and add any one of the 288 others.
    That is 15,356 states, and none is a circuit with 18 gates.
  - *How long.* You give the seconds. Checked from a fresh copy: `python3 -B sa8.py 20 0 known` reached 19
    gates after 4 s and ended in 23 s.
  - *What it does not show.* It does not show that 19 is the least. The exchange test is local, and the pool
    is one pool. Started from nothing instead of from the 22, the same program found no circuit at all, so
    the result needed a known circuit to start from.
- **`flipwalk.py`** (needs numpy) and **`exact8.py`**. Reading the 19-gate circuit gave a design: build one
  sign vector by merging pairs, then blocks of four, then all eight (7 gates); then walk from sign vector to
  sign vector, each step flipping one input or one piece that the merging left behind. `flipwalk.py` samples
  such designs and builds the walk with a shortest-path rule, so its numbers are upper bounds.
  `exact8.py` computes the exact least number of gates of this design at 8 points, over all sign vectors and
  all ways of merging.
  - *What they found.* `exact8.py`: the least is exactly 19 (`exact8.out`). `flipwalk.py` at 16 points
    (`fw4_quad.out`, `fw4_any.out`, `fwq16.out`): nothing below 63, which is far above the 52 of the family.
  - *How long.* `python3 -B exact8.py`: 5 s, checked from a fresh copy. `python3 -B flipwalk.py 3 5 1 any`
    (8 points, 5 seconds, seed 1): 19 gates at once, checked from a fresh copy on Linux.
  - *What they do not show.* "Exactly 19" is about this one design, not about all circuits. Whether 18 gates
    are possible at 8 points is open as far as I know. The 16-point numbers are upper bounds of a heuristic.
- `c19.py` and `replay8.py` are two more replays of the circuit, written apart from the checker of this
  repository (`python3 -B c19.py`, 3 s, checked from a fresh copy). `ledger*.py`, `flat.py` and the other
  outputs belong to side questions of the same run.

## 2. `family/`: the walk that found 20 gates, and the family with rate 3/4

- **`walk.py`** (with `pool.py`). A plain local walk over 8-point circuits whose helpers come from a pool of
  240 values. It drops a helper, swaps one, or removes two and adds one.
  - *What it found.* From the 22-gate circuit it fell to 21 and then 20 gates in three seconds
    (`walk_stab_1.out`). Checked from a fresh copy: `python3 -B pool.py stab`, then
    `python3 -B walk.py stab 15 1`: 20 gates, 7 s.
  - *What it does not show.* `deep.py` then removed any 3 helpers of the 20-gate circuit and added any 2 from
    the pool: 868,418 tries, no circuit with 19 gates (`deep_stab_3.out`). The 19-gate circuit of section 1
    exists all the same: two of its helpers are outside that pool. This is the rule above in one example.
- **`gen.py`**: the generator of the family, as first written. Reading the 20-gate circuit piece by piece
  gave a recursion, and `gen.py k` writes the circuit for 2^k points and replays it in exact fractions.
  - *What it found.* (3/4) N log2 N + N/4 gates for every N = 2^k: 7, 20, 52, 128, 304 gates at 4, 8, 16, 32,
    64 points (`gen.out`, `slp_4.txt` to `slp_64.txt`). The header of `gen.py` says 124 at 32 points; that
    is a slip, and the program prints 128.
  - *How long.* Under a second each. Checked from a fresh copy: `python3 -B gen.py 2` to `gen.py 6` wrote the
    five recorded files again, byte for byte.
  - *What it does not show.* The count for every k is an argument (the recursion in the first lines of
    `../gen.py`); the programs replay it up to 4,096 points, and up to 16,384 with `run.py --kmax 14`.
    `deepN.py` found no 51 at 16 points by removing 2 helpers and adding 1 (`deep16_2.out`); that is local too.
- `oslp.py` and `ocheck.py` rewrite the same circuits for count (O), where every operation is charged, and
  check them (`oslp_4.txt`, `oslp_16.txt`, `oslp_64.txt`). `milp.py` (needs numpy and scipy) is an integer
  programme that ran for 9 minutes, found nothing and proved nothing (`milp_stab.out`). `milp.py`,
  `deep.py`, `deepN.py` and the `oprice` programs were not run again.

## 3. `mincirc/`: the exhaustive search for a least circuit

- **`mincirc.c`** (with `rows.py`, which prints the matrix to aim at). It works with whole numbers modulo a
  prime p. It runs through every set of m helpers and says whether some circuit with that many gates exists.
  - *What it found.* For the 4-point Walsh-Hadamard transform: a circuit with 7 gates, and none with 6,
    both modulo 5 and modulo 7. It was written for another transform, the subset-sum transform. There it
    found that 8 points need 12 gates, the textbook count, and not 11, modulo 5 and modulo 7
    (`z8_p5_m4.out`, `z8_p7_m4.out`). `mincirc_all.c` lists every least circuit (`z8_p2_all.out`,
    `z8_p3_all.out`).
  - *How long.* The 4-point cases: under a second. The 8-point subset-sum cases: 52 s modulo 5, 6 minutes
    modulo 7. Checked from a fresh copy: `cc -O2 -o mincirc mincirc.c`, `python3 -B rows.py had 2 > rows.txt`,
    `./mincirc 5 4 2 rows.txt` (answers NO, 6 gates) and `./mincirc 5 4 3 rows.txt` (answers YES, 7 gates).
  - *What it does not show.* None found modulo a prime is not none: for example, a circuit with fractions
    whose denominators the prime divides is not seen. And it was not run on the 8-point Walsh-Hadamard
    transform: the 19-gate circuit has 11 helpers, and the runs here go up to 5. So it says nothing about
    whether 19 is the least.

## 4. `helpers/`: the search over helpers only

- **`steiner.py`** (needs numpy; it imports the `slp.py` of this folder, which is not the `slp.py` of
  `tools/circuits/`). It anneals over the helpers only and lets every output finish itself from the nearest
  helpers. Its score is the size of the circuit that this gives. Every new best is replayed in exact
  fractions.
  - *What it found.* At 4 points, 7 gates from nothing in half a second
    (`recorded/steiner_H4_s1_empty.jsonl`). At 8 points from nothing its best was 24 gates, the textbook
    count, above the 22 known then. It found none of the circuits of this repository. The two searches above
    work the same way: they search over sets of helpers and let the outputs follow.
  - *How long.* You give the seconds. Checked from a fresh copy on Linux:
    `python3 -B steiner.py H4 8 1 out` reached 7 gates after 0.3 s.
  - *What it does not show.* Anything about the least count. It is a slow random search.
