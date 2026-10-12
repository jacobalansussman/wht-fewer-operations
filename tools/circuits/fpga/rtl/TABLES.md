### 8 points

| design | W | adders | depth | adder bits | vs textbook | chain bits | p: register bits (after adders + delay = total) | p: latency | p2: register bits | p2: latency | r: register bits |
|---|---|---|---|---|---|---|---|---|---|---|---|
| textbook (`textbook`) | 8 | 24 | 3 | 240 |  | 240 | 240 + 0 = 240 | 3 | 168 | 2 | 152 |
| 1994 design (`cfl1994`) | 8 | 22 | 5 | 226 | -5.8 % | 220 | 226 + 198 = 424 | 5 | 254 | 3 | 152 |
| 1994 design, other order (`cfl1994b`) | 8 | 22 | 5 | 224 | -6.7 % | 218 | 224 + 220 = 444 | 5 | 278 | 3 | 152 |
| Alman and Rao step (`ar2023`) | 8 | 22 | 6 | 226 | -5.8 % | 216 | 226 + 394 = 620 | 6 | 312 | 3 | 152 |
| Alman and Rao step, left to right (`ar2023l`) | 8 | 22 | 8 | 235 | -2.1 % | 221 | 235 + 561 = 796 | 8 | 394 | 4 | 152 |
| this work (`ours`) | 8 | 19 | 6 | 199 | -17.1 % | 189 | 199 + 402 = 601 | 6 | 302 | 3 | 152 |
| textbook (`textbook`) | 12 | 24 | 3 | 336 |  | 336 | 336 + 0 = 336 | 3 | 232 | 2 | 216 |
| 1994 design (`cfl1994`) | 12 | 22 | 5 | 314 | -6.5 % | 308 | 314 + 294 = 608 | 5 | 358 | 3 | 216 |
| 1994 design, other order (`cfl1994b`) | 12 | 22 | 5 | 312 | -7.1 % | 306 | 312 + 316 = 628 | 5 | 390 | 3 | 216 |
| Alman and Rao step (`ar2023`) | 12 | 22 | 6 | 314 | -6.5 % | 304 | 314 + 574 = 888 | 6 | 444 | 3 | 216 |
| Alman and Rao step, left to right (`ar2023l`) | 12 | 22 | 8 | 323 | -3.9 % | 309 | 323 + 825 = 1148 | 8 | 566 | 4 | 216 |
| this work (`ours`) | 12 | 19 | 6 | 275 | -18.2 % | 265 | 275 + 586 = 861 | 6 | 430 | 3 | 216 |
| textbook (`textbook`) | 16 | 24 | 3 | 432 |  | 432 | 432 + 0 = 432 | 3 | 296 | 2 | 280 |
| 1994 design (`cfl1994`) | 16 | 22 | 5 | 402 | -6.9 % | 396 | 402 + 390 = 792 | 5 | 462 | 3 | 280 |
| 1994 design, other order (`cfl1994b`) | 16 | 22 | 5 | 400 | -7.4 % | 394 | 400 + 412 = 812 | 5 | 502 | 3 | 280 |
| Alman and Rao step (`ar2023`) | 16 | 22 | 6 | 402 | -6.9 % | 392 | 402 + 754 = 1156 | 6 | 576 | 3 | 280 |
| Alman and Rao step, left to right (`ar2023l`) | 16 | 22 | 8 | 411 | -4.9 % | 397 | 411 + 1089 = 1500 | 8 | 738 | 4 | 280 |
| this work (`ours`) | 16 | 19 | 6 | 351 | -18.8 % | 341 | 351 + 770 = 1121 | 6 | 558 | 3 | 280 |

### 16 points

| design | W | adders | depth | adder bits | vs textbook | chain bits | p: register bits (after adders + delay = total) | p: latency | p2: register bits | p2: latency | r: register bits |
|---|---|---|---|---|---|---|---|---|---|---|---|
| textbook (`textbook`) | 8 | 64 | 4 | 672 |  | 672 | 672 + 0 = 672 | 4 | 352 | 2 | 320 |
| 1994 design (`cfl1994`) | 8 | 56 | 8 | 608 | -9.5 % | 584 | 608 + 888 = 1496 | 8 | 741 | 4 | 320 |
| this work (`ours`) | 8 | 52 | 8 | 564 | -16.1 % | 544 | 564 + 856 = 1420 | 8 | 780 | 4 | 320 |
| textbook (`textbook`) | 12 | 64 | 4 | 928 |  | 928 | 928 + 0 = 928 | 4 | 480 | 2 | 448 |
| 1994 design (`cfl1994`) | 12 | 56 | 8 | 832 | -10.3 % | 808 | 832 + 1272 = 2104 | 8 | 1033 | 4 | 448 |
| this work (`ours`) | 12 | 52 | 8 | 772 | -16.8 % | 752 | 772 + 1208 = 1980 | 8 | 1084 | 4 | 448 |
| textbook (`textbook`) | 16 | 64 | 4 | 1184 |  | 1184 | 1184 + 0 = 1184 | 4 | 608 | 2 | 576 |
| 1994 design (`cfl1994`) | 16 | 56 | 8 | 1056 | -10.8 % | 1032 | 1056 + 1656 = 2712 | 8 | 1325 | 4 | 576 |
| this work (`ours`) | 16 | 52 | 8 | 980 | -17.2 % | 960 | 980 + 1560 = 2540 | 8 | 1388 | 4 | 576 |

### 64 points

| design | W | adders | depth | adder bits | vs textbook | chain bits | p: register bits (after adders + delay = total) | p: latency | p2: register bits | p2: latency | r: register bits |
|---|---|---|---|---|---|---|---|---|---|---|---|
| textbook (`textbook`) | 8 | 384 | 6 | 4416 |  | 4416 | 4416 + 0 = 4416 | 6 | 2304 | 3 | 1408 |
| 1994 design (`cfl1994`) | 8 | 336 | 12 | 3984 | -9.8 % | 3840 | 3984 + 5952 = 9936 | 12 | 4950 | 6 | 1408 |
| this work (`ours`) | 8 | 304 | 12 | 3616 | -18.1 % | 3488 | 3616 + 5824 = 9440 | 12 | 5216 | 6 | 1408 |
| textbook (`textbook`) | 12 | 384 | 6 | 5952 |  | 5952 | 5952 + 0 = 5952 | 6 | 3072 | 3 | 1920 |
| 1994 design (`cfl1994`) | 12 | 336 | 12 | 5328 | -10.5 % | 5184 | 5328 + 8256 = 13584 | 12 | 6718 | 6 | 1920 |
| this work (`ours`) | 12 | 304 | 12 | 4832 | -18.8 % | 4704 | 4832 + 8000 = 12832 | 12 | 7072 | 6 | 1920 |
| textbook (`textbook`) | 16 | 384 | 6 | 7488 |  | 7488 | 7488 + 0 = 7488 | 6 | 3840 | 3 | 2432 |
| 1994 design (`cfl1994`) | 16 | 336 | 12 | 6672 | -10.9 % | 6528 | 6672 + 10560 = 17232 | 12 | 8486 | 6 | 2432 |
| this work (`ours`) | 16 | 304 | 12 | 6048 | -19.2 % | 5920 | 6048 + 10176 = 16224 | 12 | 8928 | 6 | 2432 |

### 8 x 8 block (16 transforms of 8 points; the same function as 64 points)

| design | W | adders | depth | adder bits | vs textbook | chain bits | p: register bits (after adders + delay = total) | p: latency | p2: register bits | p2: latency | r: register bits |
|---|---|---|---|---|---|---|---|---|---|---|---|
| textbook (`textbook`) | 8 | 384 | 6 | 4416 |  | 4416 | 4416 + 0 = 4416 | 6 | 2304 | 3 | 1408 |
| this work (`ours`) | 8 | 304 | 12 | 3640 | -17.6 % | 3480 | 3640 + 7584 = 11224 | 12 | 5648 | 6 | 1408 |
| textbook (`textbook`) | 12 | 384 | 6 | 5952 |  | 5952 | 5952 + 0 = 5952 | 6 | 3072 | 3 | 1920 |
| this work (`ours`) | 12 | 304 | 12 | 4856 | -18.4 % | 4696 | 4856 + 10528 = 15384 | 12 | 7704 | 6 | 1920 |
| textbook (`textbook`) | 16 | 384 | 6 | 7488 |  | 7488 | 7488 + 0 = 7488 | 6 | 3840 | 3 | 2432 |
| this work (`ours`) | 16 | 304 | 12 | 6072 | -18.9 % | 5912 | 6072 + 13472 = 19544 | 12 | 9760 | 6 | 2432 |

### Widths of the adders, W = 8 (how many adders have each output width)

| size | design | adders by output width |
|---|---|---|
| 8 | textbook | 8 of 9 bits, 8 of 10 bits, 8 of 11 bits |
| 8 | 1994 design | 2 of 9 bits, 12 of 10 bits, 8 of 11 bits |
| 8 | 1994 design, other order | 8 of 9 bits, 2 of 10 bits, 12 of 11 bits |
| 8 | Alman and Rao step | 7 of 9 bits, 2 of 10 bits, 13 of 11 bits |
| 8 | Alman and Rao step, left to right | 3 of 9 bits, 1 of 10 bits, 18 of 11 bits |
| 8 | this work | 4 of 9 bits, 2 of 10 bits, 13 of 11 bits |
| 16 | textbook | 16 of 9 bits, 16 of 10 bits, 16 of 11 bits, 16 of 12 bits |
| 16 | 1994 design | 4 of 9 bits, 24 of 10 bits, 4 of 11 bits, 24 of 12 bits |
| 16 | this work | 8 of 9 bits, 12 of 10 bits, 12 of 11 bits, 20 of 12 bits |
| 64 | textbook | 64 of 9 bits, 64 of 10 bits, 64 of 11 bits, 64 of 12 bits, 64 of 13 bits, 64 of 14 bits |
| 64 | 1994 design | 16 of 9 bits, 96 of 10 bits, 16 of 11 bits, 96 of 12 bits, 16 of 13 bits, 96 of 14 bits |
| 64 | this work | 32 of 9 bits, 48 of 10 bits, 48 of 11 bits, 48 of 12 bits, 48 of 13 bits, 80 of 14 bits |
| 8x8 | textbook | 64 of 9 bits, 64 of 10 bits, 64 of 11 bits, 64 of 12 bits, 64 of 13 bits, 64 of 14 bits |
| 8x8 | this work | 32 of 9 bits, 16 of 10 bits, 104 of 11 bits, 32 of 12 bits, 16 of 13 bits, 104 of 14 bits |

