What the programs of wht56 printed on the morning of 11 October 2026 (US Eastern time).

mac-*    Apple M4 (10 cores, 16 GB), macOS (Darwin 25.6.0, arm64), Apple clang 21.0.0.
         System Python 3.9.6 (no numpy) and a second Python 3.9.6 with numpy 2.0.2.
         Every command ran at low priority (nice 15).  Load average about 30 to 58.
linux-*  rented virtual machine; it reports itself as an Intel Xeon at 2.20 GHz, 8 threads,
         50 GB, Linux 6.6 (x86_64), gcc 13.3.0, Python 3.13.16 with numpy 2.1.3.  Load average
         about 13.  gcc -march=native is -march=broadwell there (AVX2 and FMA, no AVX-512); the
         later timings in ffht/ found that its core does not time like that model.

*-selftest*            python3 -B -m wht56 --selftest   (the last run, with the files as they are now)
files-sha256.txt       the files as they were tested and timed, not as they are now; the copy on
                       the Linux machine had the same hashes.  Eleven of the files were corrected
                       after the timings (see below), so a check of this list against the folder
                       reports those eleven as changed
*-counts.txt           python3 -B -m wht56 --count 9 ; --count 10 ; --table 14
                       (printed again later on 11 October; see the end of this file)
*-python-numpy-bench*  python3 -B -m wht56 --bench       (two runs on each machine)
*-c-bench-run1.txt     sh wht56/c/build_and_bench.sh <dir> 9   on the Mac (best of 9 runs),
                       ... <dir> 15 on Linux; made with a first version of c/bench.c that had
                       no column for processor time; nothing else differs
*-c-bench-run2.txt, *-c-bench-run3.txt
                       the same with the present c/bench.c: best of 25 runs on the Mac, of 15
                       on Linux.  The tables of ../README.md are run 2.
*-c-bench-run4.txt     the same once more, with a third build added to the script: -O3 and no
                       other option (build "plain")
asm/                   k.c and asmcount.py: the three 8-point kernels as functions, and a count of
                       the instructions in the vector loop that gcc writes for each (Linux only);
                       k_native.s is the assembly that was counted
linux-python-numpy-bench-*, mac-python-numpy-bench-*, *-counts.txt: see above.

Runs made later the same morning by a second AI agent that reviewed the folder, with the same
script and the same files:
linux-c-bench-run5.txt, -run6.txt
                       sh wht56/c/build_and_bench.sh <dir> 15, load average about 9
linux-c-bench-run7-and-python-numpy-bench-run3.txt
                       the same at load average about 4, the quietest run; then --bench
linux-c-bench-run7-repeats-small.txt
                       the binaries of run 7 three more times at 2^9 and 2^12 points, best of 25
linux-c-bench-other-flags.txt
                       gcc -O2, -O3 -march=native -fno-tree-vectorize, and -O1; one run of 15 each
mac-c-bench-run5.txt, -run6.txt
                       nice -n 15 sh wht56/c/build_and_bench.sh <dir> 25, load average 12 to 30
mac-python-numpy-bench-run3.txt
                       python3 -B -m wht56 --bench

files-sha256.txt lists the files as they were timed.  After the timings these were corrected:
c/wht56.c and c/wht56.h (a length that is not a power of two is now refused; the kernels and
the passes are the same text), c/bench.c (the sizes are checked), reference.py, fast.py,
codegen.py, plans.py, __main__.py (arguments are checked; comments), tests/, README.md.
*-selftest*-after-corrections.txt are the tests run again after that.

The runs on the Mac went through a guard program that adds one last line of its own, which
begins with LIGHT and holds a working label and, in some files, the name of a folder.  That
line was taken out of every file of this folder.  Where a line printed by --bench held the
name of a working folder, on the Mac or on the Linux machine, the folder name was replaced
by <folder> (the six files *-python-numpy-bench-run*.txt and
linux-c-bench-run7-and-python-numpy-bench-run3.txt).  Nothing else was changed in them.

Both machines were running other jobs.  The timings are rough.

bench-by-size/         a later benchmark of the same morning, on quieter machines: 11 sizes
                       from 2^3 to 2^24 points, among them three that are not powers of 8, two
                       builds on each machine, everything twice, and two controls.
                       bench.md has the tables and what they say in plain sentences; raw/ has what
                       the programs printed; src/ has the programs as they were run (wht56.c,
                       wht56.h, kernels.h, bench.c and build_and_bench.sh are the files of ../c/,
                       byte for byte; the others were written for this benchmark).  It is the main
                       source for the plain C timings in ../README.md.  The runs listed above were
                       all at powers of 8, and bench.md says what that hid.

ffht/                  the timings that count, made later on 11 October: the 8-point step written
                       into the generated code of the library FFHT, in place of its 24-operation
                       block, and timed on the Linux machine.  It was not faster at any size.
                       ffht/README.md has the tables by size, the conditions, the sources, the raw
                       outputs and how to run it again.  No file of FFHT is in that folder; it
                       holds a patch against FFHT's generator.  The gain that the runs listed above
                       show on the Linux machine with vector instructions is not a gain of the
                       step: ffht/README.md, section 3, says what it is.

The last changes, made when the folder was placed in this repository (11 October):
__main__.py and plans.py: the words about the 1994 paper of Coppersmith, Feig and Linzer were
corrected once the paper had been read (its formula for an odd power of two is theirs), and
the year printed for Alman and Rao's paper is now 2023.  No number changed.  mac-counts.txt
and linux-counts.txt were then printed again on both machines; they are the same bytes on
both.  Against the files they replace, every number is the same; three lines differ in their
words, two blank lines are gone and two closing lines are new.  README.md and LICENSE-NOTE.txt
were rewritten.
The tests were run again after that: 30 tests, OK, on the Mac with both Pythons (5 skipped
without numpy) and on the Linux machine.  So files-sha256.txt, which lists the files as they
were timed, no longer matches README.md, LICENSE-NOTE.txt, __main__.py and plans.py either.
Later the same day, in bench-by-size/: three words in the first comment line of src/bench_size.c
were changed ("written for this benchmark"), and src/ADDED.sha256 has its new checksum; the
program is the same.  In bench-head.md and bench-tail.md some sentences were reworded and the
clock times were taken out of the first line (the raw outputs keep them); bench.md was written
again from them by tables.py, and no number in it changed.
circuits/h4_7gates.txt: five comment lines (7 to 11) were written again once the 1994 paper had
been read; no line of the circuit changed.  circuits/SHA256SUMS has the new checksum, so
files-sha256.txt no longer matches these two files either.
