## Combinational variant (c) against the definition

| size | design | W | step A: design = wide (bitwuzla) | step B: wide = definition (z3) | second opinion on B (yices, 30 s) | result |
|---|---|---|---|---|---|---|
| 8 | textbook | 8 | PASSED, 0.2 s | PASSED, 0.2 s | PASSED, 0.2 s | **proved** |
| 8 | ar2023 | 8 | PASSED, 1.0 s | PASSED, 0.2 s | PASSED, 0.2 s | **proved** |
| 8 | ar2023l | 8 | PASSED, 3.5 s | PASSED, 0.2 s | PASSED, 0.2 s | **proved** |
| 8 | cfl1994 | 8 | PASSED, 1.0 s | PASSED, 0.2 s | PASSED, 0.2 s | **proved** |
| 8 | cfl1994b | 8 | PASSED, 0.4 s | PASSED, 0.2 s | PASSED, 0.2 s | **proved** |
| 8 | ours | 8 | PASSED, 2.5 s | PASSED, 0.2 s | PASSED, 0.2 s | **proved** |
| 8 | textbook | 12 | PASSED, 0.1 s | PASSED, 0.1 s | PASSED, 0.1 s | **proved** |
| 8 | ar2023 | 12 | PASSED, 1.7 s | PASSED, 0.1 s | PASSED, 0.1 s | **proved** |
| 8 | ar2023l | 12 | PASSED, 2.3 s | PASSED, 0.1 s | PASSED, 0.1 s | **proved** |
| 8 | cfl1994 | 12 | PASSED, 1.4 s | PASSED, 0.1 s | PASSED, 0.1 s | **proved** |
| 8 | cfl1994b | 12 | PASSED, 0.4 s | PASSED, 0.1 s | PASSED, 0.1 s | **proved** |
| 8 | ours | 12 | PASSED, 1.6 s | PASSED, 0.1 s | PASSED, 0.1 s | **proved** |
| 8 | textbook | 16 | PASSED, 0.1 s | PASSED, 0.1 s | PASSED, 0.1 s | **proved** |
| 8 | ar2023 | 16 | PASSED, 1.6 s | PASSED, 0.1 s | PASSED, 0.1 s | **proved** |
| 8 | ar2023l | 16 | PASSED, 3.6 s | PASSED, 0.1 s | PASSED, 0.1 s | **proved** |
| 8 | cfl1994 | 16 | PASSED, 1.9 s | PASSED, 0.1 s | PASSED, 0.1 s | **proved** |
| 8 | cfl1994b | 16 | PASSED, 0.5 s | PASSED, 0.1 s | PASSED, 0.1 s | **proved** |
| 8 | ours | 16 | PASSED, 1.9 s | PASSED, 0.1 s | PASSED, 0.1 s | **proved** |
| 16 | textbook | 8 | PASSED, 0.4 s | PASSED, 0.2 s | PASSED, 0.2 s | **proved** |
| 16 | cfl1994 | 8 | PASSED, 14.8 s | PASSED, 0.2 s | PASSED, 0.2 s | **proved** |
| 16 | ours | 8 | PASSED, 9.0 s | PASSED, 0.1 s | TIMEOUT, 30.0 s; one output at a time: PASSED (16 of 16 outputs), 2.1 s | **proved** |
| 16 | textbook | 12 | PASSED, 0.3 s | PASSED, 0.1 s | PASSED, 0.1 s | **proved** |
| 16 | cfl1994 | 12 | PASSED, 10.8 s | PASSED, 0.1 s | PASSED, 0.1 s | **proved** |
| 16 | ours | 12 | PASSED, 10.0 s | PASSED, 0.1 s | TIMEOUT, 30.0 s; one output at a time: PASSED (16 of 16 outputs), 2.8 s | **proved** |
| 16 | textbook | 16 | PASSED, 0.4 s | PASSED, 0.1 s | PASSED, 0.1 s | **proved** |
| 16 | cfl1994 | 16 | PASSED, 13.9 s | PASSED, 0.1 s | PASSED, 0.1 s | **proved** |
| 16 | ours | 16 | PASSED, 16.3 s | PASSED, 0.1 s | TIMEOUT, 30.0 s; one output at a time: PASSED (16 of 16 outputs), 3.2 s | **proved** |
| 64 | textbook | 8 | PASSED, 18.1 s | PASSED, 0.4 s | PASSED, 0.5 s | **proved** |
| 64 | cfl1994 | 8 | TIMEOUT, 240.0 s | PASSED, 0.4 s | PASSED, 0.5 s | not proved (simulated only) |
| 64 | ours | 8 | TIMEOUT, 240.0 s | PASSED, 0.4 s | TIMEOUT, 30.0 s; one output at a time: TIMEOUT (32 of 64 outputs), 963.5 s | not proved (simulated only) |
| 8x8 | textbook | 8 | PASSED, 16.0 s | PASSED, 0.4 s | PASSED, 0.4 s | **proved** |
| 8x8 | ours | 8 | TIMEOUT, 240.0 s | PASSED, 0.4 s | PASSED, 0.5 s | not proved (simulated only) |

Controls (a damaged design; the solver must find an input that shows the damage):

- 8 points, textbook, W = 8: design with wire n_t9 one bit too narrow = wide (must FAIL). Solver bitwuzla: FAILED in 0.2 s.
- 8 points, textbook, W = 8: wide with one sign changed at n_t13 = definition (must FAIL). Solver z3: FAILED in 0.2 s.
- 16 points, textbook, W = 8: design with wire n_t25 one bit too narrow = wide (must FAIL). Solver bitwuzla: FAILED in 0.2 s.
- 16 points, textbook, W = 8: wide with one sign changed at n_t33 = definition (must FAIL). Solver z3: FAILED in 0.2 s.
- 8 points, textbook, W = 12: design with wire n_t9 one bit too narrow = wide (must FAIL). Solver bitwuzla: FAILED in 0.1 s.
- 8 points, textbook, W = 12: wide with one sign changed at n_t13 = definition (must FAIL). Solver z3: FAILED in 0.1 s.
- 8 points, textbook, W = 16: design with wire n_t9 one bit too narrow = wide (must FAIL). Solver bitwuzla: FAILED in 0.1 s.
- 8 points, textbook, W = 16: wide with one sign changed at n_t13 = definition (must FAIL). Solver z3: FAILED in 0.1 s.
- 16 points, textbook, W = 12: design with wire n_t25 one bit too narrow = wide (must FAIL). Solver bitwuzla: FAILED in 0.3 s.
- 16 points, textbook, W = 12: wide with one sign changed at n_t33 = definition (must FAIL). Solver z3: FAILED in 0.1 s.
- 16 points, textbook, W = 16: design with wire n_t25 one bit too narrow = wide (must FAIL). Solver bitwuzla: FAILED in 0.3 s.
- 16 points, textbook, W = 16: wide with one sign changed at n_t33 = definition (must FAIL). Solver z3: FAILED in 0.1 s.
- 64 points, textbook, W = 8: design with wire n_t161 one bit too narrow = wide (must FAIL). Solver bitwuzla: FAILED in 1.8 s.
- 64 points, textbook, W = 8: wide with one sign changed at n_t193 = definition (must FAIL). Solver z3: FAILED in 0.5 s.
- 8x8 points, textbook, W = 8: design with wire n_t161 one bit too narrow = wide (must FAIL). Solver bitwuzla: FAILED in 0.9 s.
- 8x8 points, textbook, W = 8: wide with one sign changed at n_t193 = definition (must FAIL). Solver z3: FAILED in 0.4 s.
- 64 points, textbook, W = 8: design with wire n_t161 one bit too narrow = wide (must FAIL). Solver bitwuzla: FAILED in 2.1 s.
- 64 points, textbook, W = 8: wide with one sign changed at n_t193 = definition (must FAIL). Solver z3: FAILED in 0.5 s.

## Variants with registers (p, p2, r) against the combinational variant, delayed

| size | design | W | p | p2 | r |
|---|---|---|---|---|---|
| 8 | textbook | 8 | PASS, latency 3, 1 s | PASS, latency 2, 1 s | PASS, latency 2, 1 s |
| 8 | ar2023 | 8 | PASS, latency 6, 1 s | PASS, latency 3, 1 s | PASS, latency 2, 1 s |
| 8 | ar2023l | 8 | PASS, latency 8, 1 s | PASS, latency 4, 1 s | PASS, latency 2, 2 s |
| 8 | cfl1994 | 8 | PASS, latency 5, 1 s | PASS, latency 3, 1 s | PASS, latency 2, 2 s |
| 8 | cfl1994b | 8 | PASS, latency 5, 1 s | PASS, latency 3, 1 s | PASS, latency 2, 1 s |
| 8 | ours | 8 | PASS, latency 6, 2 s | PASS, latency 3, 2 s | PASS, latency 2, 1 s |
| 8 | textbook | 12 | PASS, latency 3, 1 s | PASS, latency 2, 1 s | PASS, latency 2, 1 s |
| 8 | ar2023 | 12 | PASS, latency 6, 1 s | PASS, latency 3, 1 s | PASS, latency 2, 1 s |
| 8 | ar2023l | 12 | PASS, latency 8, 1 s | PASS, latency 4, 1 s | PASS, latency 2, 2 s |
| 8 | cfl1994 | 12 | PASS, latency 5, 1 s | PASS, latency 3, 1 s | PASS, latency 2, 2 s |
| 8 | cfl1994b | 12 | PASS, latency 5, 1 s | PASS, latency 3, 1 s | PASS, latency 2, 1 s |
| 8 | ours | 12 | PASS, latency 6, 2 s | PASS, latency 3, 2 s | PASS, latency 2, 1 s |
| 8 | textbook | 16 | PASS, latency 3, 2 s | PASS, latency 2, 1 s | PASS, latency 2, 2 s |
| 8 | ar2023 | 16 | PASS, latency 6, 1 s | PASS, latency 3, 1 s | PASS, latency 2, 1 s |
| 8 | ar2023l | 16 | PASS, latency 8, 2 s | PASS, latency 4, 2 s | PASS, latency 2, 2 s |
| 8 | cfl1994 | 16 | PASS, latency 5, 2 s | PASS, latency 3, 1 s | PASS, latency 2, 2 s |
| 8 | cfl1994b | 16 | PASS, latency 5, 2 s | PASS, latency 3, 2 s | PASS, latency 2, 2 s |
| 8 | ours | 16 | PASS, latency 6, 3 s | PASS, latency 3, 2 s | PASS, latency 2, 2 s |
| 16 | textbook | 8 | PASS, latency 4, 4 s | PASS, latency 2, 3 s | PASS, latency 2, 4 s |
| 16 | cfl1994 | 8 | PASS, latency 8, 5 s | PASS, latency 4, 4 s | PASS, latency 2, 5 s |
| 16 | ours | 8 | PASS, latency 8, 15 s | PASS, latency 4, 18 s | PASS, latency 2, 8 s |
| 16 | textbook | 12 | PASS, latency 4, 7 s | PASS, latency 2, 4 s | PASS, latency 2, 6 s |
| 16 | cfl1994 | 12 | PASS, latency 8, 10 s | PASS, latency 4, 5 s | PASS, latency 2, 7 s |
| 16 | ours | 12 | PASS, latency 8, 16 s | PASS, latency 4, 20 s | PASS, latency 2, 8 s |
| 16 | textbook | 16 | PASS, latency 4, 8 s | PASS, latency 2, 6 s | PASS, latency 2, 8 s |
| 16 | cfl1994 | 16 | PASS, latency 8, 9 s | PASS, latency 4, 8 s | PASS, latency 2, 10 s |
| 16 | ours | 16 | PASS, latency 8, 20 s | PASS, latency 4, 41 s | PASS, latency 2, 12 s |

Controls:

- 8 points, cfl1994, W = 8: p with x2 taken one stage early = combinational delayed (must FAIL): FAIL in 0 s.
- 16 points, cfl1994, W = 8: p with x2 taken one stage early = combinational delayed (must FAIL): FAIL in 1 s.

## Combinational variant (c) against the definition, in three steps (run_formal3.py)

| size | design | W | A1: every wire of wide fits (z3; yices) | A2: design = wide where every wire fits (bitwuzla) | B: wide = definition (z3; yices) | result |
|---|---|---|---|---|---|---|
| 16 | textbook | 8 | PASSED, 0.4 s; PASSED, 0.1 s | PASSED, 0.3 s | PASSED, 0.1 s; PASSED, 0.1 s | **proved** |
| 16 | cfl1994 | 8 | PASSED, 0.2 s; PASSED, 0.1 s | PASSED, 4.8 s | PASSED, 0.1 s; PASSED, 0.1 s | **proved** |
| 16 | ours | 8 | PASSED, 0.3 s; PASSED, 0.1 s | PASSED, 11.2 s | PASSED, 0.1 s; TIMEOUT, 30.0 s; one output at a time: PASSED (16 of 16 outputs), 2.1 s | **proved** |

Controls:

- 16 points, textbook, W = 8: wire n_t25 fits 9 bits, one fewer than it needs (must FAIL). Solver z3: FAILED in 0.1 s.
- 16 points, textbook, W = 8: design with wire n_t25 one bit too narrow = wide wherever every wire fits (must FAIL). Solver bitwuzla: FAILED in 0.3 s.

