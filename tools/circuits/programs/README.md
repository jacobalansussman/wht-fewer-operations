# tools/circuits/programs: the circuits as text

One format for every file. A line is `name = term`, `name = term + term` or `name = term - term`, where a
term is a name, or a number times a name (`2*x3`, `1/2*g7`), with an optional minus sign in front. `#` starts
a comment. The inputs are `x0`, `x1`, ...; the outputs are the names that start with `y`, and in the files
written by `gen.py` the output `yJ` is row J of the transform. The first lines of `../slp.py` give the
format and the two counts in full. `python3 -B tools/circuits/slp.py FILE` checks any file and prints its
counts.

- `h4_7gates.txt`, `h8_19gates.txt`, `h8_half_20ops.txt`, `h16_52gates.txt`: the four named circuits, each
  with a header that says what it is and whose it is.
- Every line of every file in this folder is a renaming of an output, one multiplication by a constant, or a
  sum or difference of two terms of which at most one carries a constant. No line has a constant on both
  terms. So each counted line is one operation of Coppersmith, Feig and Linzer (1994, page 969), who charge
  one for a multiply-add, ±a ± b·c, for a plain addition and for a plain multiplication. In the two-term
  lines the constant is 2 or -2, apart from one 4 in the earlier 21-gate circuit of `as_found/`.
  `python3 -B tools/circuits/multiply_add_check.py` counts the shapes over the 63 files.
- `generated/`: what `gen.py` writes, for every size up to 64 points, and two files at 512 points.
  `G_` files are written for count (G), `O_` files for count (O). `family` is the construction with
  (3/4) N log2 N + N/4 gates; `layers` and `layers8` apply the small circuits along the address bits;
  `textbook` is the usual program. `_exact` files give the transform itself; `_factor` files give it times
  a power of 1/2, named in the first line. `O_layers8_512_exact.txt` is the 512-point program with 4,352
  operations. `run.py` writes all of these again and compares them byte for byte.
- `as_found/`: the files as the searches left them, unchanged. `h8_19gates.txt` is the 19-gate circuit and
  `h8_21gates.txt` an earlier one with 21 gates. `slp_N.txt` is the family at N points and `oslp_N.txt` the
  same for count (O), with every output times a power of 1/2. `h3_o_N.txt` is the 20-operation circuit in
  layers, with every output times a power of 1/2, and `h3_ox_N.txt` the same followed by N multiplications,
  which gives the transform itself. The names are working names of the search runs.

**One header is older than the rest of the repository.** `h8_half_20ops.txt`, line 6, names the Lean file
as `Work/SmallWHT/H8Half.lean`. In this repository it is `lean/Work/SmallWHT/H8Half.lean`. That file is kept
byte for byte as it was when it was checked and timed (`../fast/wht56/circuits/SHA256SUMS` has the
checksums). The comment lines 7 to 11 of `h4_7gates.txt` were written again once the 1994 paper had been
read; its operations are the same lines as before.
