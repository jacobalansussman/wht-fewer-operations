# Left out of the second wave's folders

18 files, 1.6 MB in all. They are on my Mac and not in this repository.

I kept every program source and every text file of at most 100 KB (102,400 bytes). I left out larger files, compiled programs (they can be built again from the C sources that are here) and binary data. A report may still name a file from this list.

The last column was written by a script from each file's name and first line. I did not check the lines one by one.


## Text files over 100 KB: 8

| File | Size | What it was |
|---|---|---|
| `e2-3-drain/r8big/log.txt` | 305 KB | text table written or read by a program; 2,725 lines; it begins: `drain N=8 seed=301 K=2000 cs=2 target=H: bestU=22 at gate 21; ended g=` |
| `j-machine/r2/steiner_H4x2_s11_empty.jsonl` | 115 KB | trace of a search, one JSON record per line (a program's output, not a chat transcript); 178 lines; it begins: `{"task": "H4x2", "U": 23, "exact_total": 23, "aux_gates": 1, "dists": ` |
| `j-machine/r2/steiner_H8_s12_empty.jsonl` | 146 KB | trace of a search, one JSON record per line (a program's output, not a chat transcript); 140 lines; it begins: `{"task": "H8", "U": 53, "exact_total": 53, "aux_gates": 1, "dists": [6` |
| `j-machine/r2/steiner_Z8_s11_empty.jsonl` | 103 KB | trace of a search, one JSON record per line (a program's output, not a chat transcript); 187 lines; it begins: `{"task": "Z8", "U": 18, "exact_total": 18, "aux_gates": 1, "dists": [0` |
| `j-machine/r3/steiner_H8_s23_empty.jsonl` | 111 KB | trace of a search, one JSON record per line (a program's output, not a chat transcript); 119 lines; it begins: `{"task": "H8", "U": 53, "exact_total": 53, "aux_gates": 1, "dists": [6` |
| `j-machine/r3/steiner_K8_s21_empty.jsonl` | 168 KB | trace of a search, one JSON record per line (a program's output, not a chat transcript); 180 lines; it begins: `{"task": "K8", "U": 53, "exact_total": 53, "aux_gates": 1, "dists": [6` |
| `j-machine/r3/steiner_K8_s22_empty.jsonl` | 137 KB | trace of a search, one JSON record per line (a program's output, not a chat transcript); 144 lines; it begins: `{"task": "K8", "U": 57, "exact_total": 57, "aux_gates": 1, "dists": [7` |
| `j-machine/t3/steiner_H4_s1_empty.jsonl` | 132 KB | trace of a search, one JSON record per line (a program's output, not a chat transcript); 340 lines; it begins: `{"task": "H4", "U": 11, "exact_total": 11, "aux_gates": 1, "dists": [3` |


## Compiled programs: 7

| File | Size | What it was |
|---|---|---|
| `e-2-density/mincirc_pad` | 34 KB | compiled program (a machine-code executable); build it again from `mincirc_pad.c` |
| `e-2-density/mincirc_seed` | 34 KB | compiled program (a machine-code executable); build it again from `mincirc_seed.c` |
| `e-7-halftouch/altmin` | 66 KB | compiled program (a machine-code executable); build it again from `altmin.c` |
| `e-7-halftouch/anneal` | 50 KB | compiled program (a machine-code executable); build it again from `anneal.c` |
| `e2-3-drain/drain` | 50 KB | compiled program (a machine-code executable); build it again from `drain.c` |
| `e2-3-drain/drain2` | 66 KB | compiled program (a machine-code executable); its source is probably `drain.c` (the name is close; not checked) |
| `j-manyatonce/ds` | 34 KB | compiled program (a machine-code executable); build it again from `ds.c` |


## Binary data and archives: 3

| File | Size | What it was |
|---|---|---|
| `j-machine/r2.tgz` | 32 KB | compressed archive of outputs |
| `j-machine/r3.tgz` | 43 KB | compressed archive of outputs |
| `j-machine/r4.tgz` | 5 KB | compressed archive of outputs |

