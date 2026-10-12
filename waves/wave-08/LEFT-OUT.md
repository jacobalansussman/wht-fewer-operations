# Left out of the eighth wave's folders

22 files, 1.7 MB in all. They are on my Mac and not in this repository.

I kept every program source and every text file of at most 100 KB (102,400 bytes). I left out larger files, compiled programs (they can be built again from the C sources that are here) and binary data. A report may still name a file from this list.

Three scripts are left out for another reason: they stop other programs. They are in their own table at the end.

The last column was written by a script from each file's name and first line. I did not check the lines one by one.


## Text files over 100 KB: 4

| File | Size | What it was |
|---|---|---|
| `ab-0-neighboursums/flats6.txt` | 500 KB | text table written or read by a program; 26,387 lines; it begins: `0 1` |
| `ab-1-fewerblocks/knows_7_3.edges` | 322 KB | list of edges of a graph written by a program; 25,537 lines; it begins: `5376 20160` |
| `ab-4-zcut/z8_p2_full.out` | 258 KB | output of a program; 2,812 lines; it begins: `p=2 n=8 rows=8 non-input distinct targets=7 intermediates allowed m=5 ` |
| `ab-4-zcut/z8_p3_full.out` | 255 KB | output of a program; 2,782 lines; it begins: `p=3 n=8 rows=8 non-input distinct targets=7 intermediates allowed m=5 ` |


## Compiled programs: 10

| File | Size | What it was |
|---|---|---|
| `ab-0-neighboursums/flat3` | 33 KB | compiled program (a machine-code executable); build it again from `flat3.c` |
| `ab-0-neighboursums/mincirc_top` | 34 KB | compiled program (a machine-code executable); build it again from `mincirc_top.c` |
| `ab-2-tallpool/tallmin3` | 50 KB | compiled program (a machine-code executable); its source is probably `tallmin.c` (the name is close; not checked) |
| `ab-2-tallpool/tallmin4` | 50 KB | compiled program (a machine-code executable); its source is probably `tallmin.c` (the name is close; not checked) |
| `ab-2-tallpool/tallmin5` | 50 KB | compiled program (a machine-code executable); its source is probably `tallmin.c` (the name is close; not checked) |
| `ab-2-tallpool/tallmin6` | 50 KB | compiled program (a machine-code executable); its source is probably `tallmin.c` (the name is close; not checked) |
| `ab-5-cancellit/mincirc_free` | 34 KB | compiled program (a machine-code executable); build it again from `mincirc_free.c` |
| `ac-0/lift3` | 33 KB | compiled program (a machine-code executable); build it again from `lift3.c` |
| `ac-0/liftp` | 33 KB | compiled program (a machine-code executable); build it again from `liftp.c` |
| `ac-0/xs` | 33 KB | compiled program (a machine-code executable); build it again from `xs.c` |


## Binary data and archives: 5

| File | Size | What it was |
|---|---|---|
| `ab-1-fewerblocks/refl_lm_m4_W4_S0_try1.npy` | 1 KB | array of numbers saved by a Python program (NumPy binary format) |
| `ab-1-fewerblocks/refl_lm_m4_W4_S0_try2.npy` | 1 KB | array of numbers saved by a Python program (NumPy binary format) |
| `ab-6-chainexchanges/linux/hole_n2_S3_H1_seq_1-1.npy` | 280 bytes | array of numbers saved by a Python program (NumPy binary format) |
| `ab-6-chainexchanges/linux/hole_n3_S2_H1_seq_1-1-0.npy` | 392 bytes | array of numbers saved by a Python program (NumPy binary format) |
| `ab-6-chainexchanges/linux/hole_n3_S4_H2_seq_12-12-0.npy` | 680 bytes | array of numbers saved by a Python program (NumPy binary format) |


## Scripts that managed jobs on my machines: 3

These stopped the agent's own jobs by walking the list of running programs. They hold no result, and a stranger should not run them, so I left them out. The report `ab-0.md` names them as `kill*.sh`.

| File | Size | What it was |
|---|---|---|
| `ab-0-neighboursums/kill.sh` | 1 KB | shell script: walks the list of running programs and stops those that work in this agent's folder and whose command line names one of four job names |
| `ab-0-neighboursums/kill5.sh` | 1 KB | shell script: the same, for two other job names |
| `ab-0-neighboursums/kill6.sh` | 1 KB | shell script: the same, with no test of the job name: it stops every program that works in that folder |
