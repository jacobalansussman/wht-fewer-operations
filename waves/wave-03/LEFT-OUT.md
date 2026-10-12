# Left out of the third wave's folders

10 files, 822 KB in all. They are on my Mac and not in this repository.

I kept every program source and every text file of at most 100 KB (102,400 bytes). I left out larger files, compiled programs (they can be built again from the C sources that are here) and binary data. A report may still name a file from this list.

One more file is held back for another reason, and two scripts are left out because they stop other programs; each has its own table below.

The last column was written by a script from each file's name and first line. I did not check the lines one by one.


## Text files over 100 KB: 4

| File | Size | What it was |
|---|---|---|
| `g-2-basischange/k4_l1_p5.out` | 183 KB | output of a program; 3,891 lines; it begins: `CH ((0, 0, 1, 4), (0, 1, 0, 4), (1, 0, 4, 0)) 6` |
| `g-2-basischange/k4_l2_p5_m3.out` | 131 KB | output of a program; 2,624 lines; it begins: `CH ((0, 0, 1, 4), (0, 1, 0, 4), (1, 0, 4, 0)) None` |
| `g-3-illconditioned/onpath7.txt` | 174 KB | text table written or read by a program; 5,250 lines; it begins: `# p=7 wires=4 best=8 : layer, then the wires (sorted), digits modulo p` |
| `g-4-zetalead/remote/steiner_Z16_s7_empty.jsonl` | 224 KB | trace of a search, one JSON record per line (a program's output, not a chat transcript); 176 lines; it begins: `{"task": "Z16", "U": 66, "exact_total": 66, "aux_gates": 1, "dists": [` |


## Compiled programs: 3

| File | Size | What it was |
|---|---|---|
| `g-0-mirror/search` | 33 KB | compiled program (a machine-code executable); build it again from `search.c` |
| `g-3-illconditioned/inplace` | 34 KB | compiled program (a machine-code executable); build it again from `inplace.c` |
| `g-5-k3/mincirc_odd` | 34 KB | compiled program (a machine-code executable); build it again from `mincirc_odd.c` |


## Scripts that managed jobs on my machines: 2

These stopped and restarted the agent's own jobs on the rented Linux machine by searching the list of running programs. They hold no result, and a stranger should not run them, so I left them out.

| File | Size | What it was |
|---|---|---|
| `g-5-k3/remote_restart.sh` | 1 KB | shell script: stops every running program whose command line names `run_steiner_k9.py`, moves three files into `old/` and starts two new background jobs |
| `g-5-k3/remote_wave2.sh` | 1 KB | shell script: stops the same programs and starts two new background jobs |


## Held back for my decision: 1

| File | Size | What it was |
|---|---|---|
| `g-4-zetalead/note-for-zeta-readers.md` | 8 KB | a draft note for readers who use the zeta transform, written by the agent in my voice and headed "Private draft. Not published."; the report g-4.md names it and says it is private until I say otherwise. Held back until I decide |

