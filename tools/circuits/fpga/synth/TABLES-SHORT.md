**(a) 8 points, W = 8, unpipelined (variant c: input register, all adders, output register), 10 seeds**

| design | adders / adder bits / depth | logic cells (same for every seed) | against textbook | adders alone, no output register: cells | against textbook | max MHz, nextpnr: median [lowest - highest] | max MHz, icetime: median |
|---|---|---|---|---|---|---|---|
| textbook | 24 / 240 / 3 | 349 | - | 336 | - | 98.5 [92.8 - 103.6] | 96.7 |
| 1994 design | 22 / 226 / 5 | 295 | -54 (-15.5 %) | 286 | -50 (-14.9 %) | 90.8 [87.2 - 92.3] | 88.9 |
| Alman and Rao step | 22 / 226 / 6 | 244 | -105 (-30.1 %) | 241 | -95 (-28.3 %) | 73.6 [66.9 - 77.6] | 73.0 |
| this work | 19 / 199 / 6 | 274 | -75 (-21.5 %) | 251 | -85 (-25.3 %) | 73.3 [69.8 - 75.6] | 71.3 |

**(b) 8 points, W = 8, fewest logic cells that reach a clock target** (cells include all registers of the design; entry = variant, latency in clocks, cells, median MHz, seeds reaching the target)

| clock target | textbook | 1994 design | Alman and Rao step | this work | this work against textbook |
|---|---|---|---|---|---|
| 12 MHz (board oscillator) | c, 1, **349**, 98, 10/10 | c, 1, **295**, 91, 10/10 | c, 1, **244**, 74, 10/10 | c, 1, **274**, 73, 10/10 | -75 (-21.5 %) |
| 50 MHz | c, 1, **349**, 98, 10/10 | c, 1, **295**, 91, 10/10 | c, 1, **244**, 74, 10/10 | c, 1, **274**, 73, 10/10 | -75 (-21.5 %) |
| 75 MHz | c, 1, **349**, 98, 10/10 | c, 1, **295**, 91, 10/10 | p5, 2, **284**, 84, 10/10 | p5, 2, **331**, 84, 10/10 | -18 (-5.2 %) |
| 100 MHz | p2, 2, **354**, 151, 10/10 | p4, 2, **320**, 116, 10/10 | p3, 2, **304**, 125, 10/10 | p3, 2, **395**, 122, 10/10 | +41 (+11.6 %) |
| 125 MHz | p2, 2, **354**, 151, 10/10 | p3, 2, **348**, 153, 10/10 | p3, 2, **304**, 125, 7/10 | p2, 3, **464**, 154, 10/10 | +110 (+31.1 %) |
| 150 MHz | p2, 2, **354**, 151, 6/10 | p3, 2, **348**, 153, 6/10 | p2, 3, **389**, 171, 10/10 | p2, 3, **464**, 154, 9/10 | +110 (+31.1 %) |
| 216 MHz (textbook at one adder per clock) | p, 3, **363**, 216, 7/10 | none reaches it | p, 6, **630**, 238, 10/10 | none reaches it | - |

**(a) 8 points, W = 12, unpipelined (variant c: input register, all adders, output register), 10 seeds**

| design | adders / adder bits / depth | logic cells (same for every seed) | against textbook | adders alone, no output register: cells | against textbook | max MHz, nextpnr: median [lowest - highest] | max MHz, icetime: median |
|---|---|---|---|---|---|---|---|
| textbook | 24 / 336 / 3 | 493 | - | 480 | - | 89.3 [86.2 - 92.8] | 87.8 |
| 1994 design | 22 / 314 / 5 | 415 | -78 (-15.8 %) | 406 | -74 (-15.4 %) | 81.7 [79.8 - 85.8] | 79.8 |
| Alman and Rao step | 22 / 314 / 6 | 344 | -149 (-30.2 %) | 341 | -139 (-29.0 %) | 65.4 [61.7 - 66.9] | 64.5 |
| this work | 19 / 275 / 6 | 386 | -107 (-21.7 %) | 355 | -125 (-26.0 %) | 64.9 [63.5 - 68.0] | 62.8 |

**(b) 8 points, W = 12, fewest logic cells that reach a clock target** (cells include all registers of the design; entry = variant, latency in clocks, cells, median MHz, seeds reaching the target)

| clock target | textbook | 1994 design | Alman and Rao step | this work | this work against textbook |
|---|---|---|---|---|---|
| 12 MHz (board oscillator) | c, 1, **493**, 89, 10/10 | c, 1, **415**, 82, 10/10 | c, 1, **344**, 65, 10/10 | c, 1, **386**, 65, 10/10 | -107 (-21.7 %) |
| 50 MHz | c, 1, **493**, 89, 10/10 | c, 1, **415**, 82, 10/10 | c, 1, **344**, 65, 10/10 | c, 1, **386**, 65, 10/10 | -107 (-21.7 %) |
| 75 MHz | c, 1, **493**, 89, 10/10 | c, 1, **415**, 82, 10/10 | p5, 2, **400**, 78, 7/10 | p5, 2, **467**, 79, 9/10 | -26 (-5.3 %) |
| 100 MHz | p2, 2, **498**, 135, 10/10 | p4, 2, **448**, 106, 10/10 | p3, 2, **432**, 112, 10/10 | p3, 2, **563**, 111, 10/10 | +65 (+13.1 %) |
| 125 MHz | p2, 2, **498**, 135, 10/10 | p3, 2, **492**, 136, 10/10 | p2, 3, **553**, 150, 10/10 | p2, 3, **664**, 142, 10/10 | +166 (+33.3 %) |
| 150 MHz | p, 3, **507**, 193, 10/10 | p, 5, **699**, 183, 10/10 | p2, 3, **553**, 150, 5/10 | p, 6, **973**, 188, 10/10 | +466 (+91.9 %) |
| 193 MHz (textbook at one adder per clock) | p, 3, **507**, 193, 5/10 | none reaches it | p, 6, **901**, 203, 10/10 | none reaches it | - |

**(a) 16 points, W = 8, unpipelined (variant c: input register, all adders, output register), 10 seeds**

| design | adders / adder bits / depth | logic cells (same for every seed) | against textbook | adders alone, no output register: cells | against textbook | max MHz, nextpnr: median [lowest - highest] | max MHz, icetime: median |
|---|---|---|---|---|---|---|---|
| textbook | 64 / 672 / 4 | 969 | - | 944 | - | 71.1 [67.9 - 74.0] | 70.0 |
| 1994 design | 56 / 608 / 8 | 720 | -249 (-25.7 %) | 711 | -233 (-24.7 %) | 59.9 [56.4 - 62.0] | 58.6 |
| this work | 52 / 564 / 8 | 877 | -92 (-9.5 %) | 780 | -164 (-17.4 %) | 54.6 [52.6 - 56.8] | 53.5 |
| this work, other signs | 52 / 564 / 8 | 811 | -158 (-16.3 %) | 715 | -229 (-24.3 %) | 56.6 [52.8 - 59.1] | 55.4 |

**(b) 16 points, W = 8, fewest logic cells that reach a clock target** (cells include all registers of the design; entry = variant, latency in clocks, cells, median MHz, seeds reaching the target)

| clock target | textbook | 1994 design | this work | this work, other signs | this work against textbook |
|---|---|---|---|---|---|
| 12 MHz (board oscillator) | c, 1, **969**, 71, 10/10 | c, 1, **720**, 60, 10/10 | c, 1, **877**, 55, 10/10 | c, 1, **811**, 57, 10/10 | -92 (-9.5 %) |
| 50 MHz | c, 1, **969**, 71, 10/10 | c, 1, **720**, 60, 10/10 | c, 1, **877**, 55, 10/10 | c, 1, **811**, 57, 10/10 | -92 (-9.5 %) |
| 75 MHz | p2, 2, **980**, 134, 10/10 | p4, 2, **742**, 100, 10/10 | p5, 2, **990**, 80, 10/10 | p4, 2, **1016**, 89, 10/10 | +10 (+1.0 %) |
| 100 MHz | p2, 2, **980**, 134, 10/10 | p4, 2, **742**, 100, 6/10 | p3, 3, **1195**, 110, 10/10 | p2, 4, **1330**, 141, 10/10 | +215 (+21.9 %) |
| 125 MHz | p2, 2, **980**, 134, 9/10 | p3, 3, **956**, 129, 5/10 | p2, 4, **1406**, 144, 10/10 | p2, 4, **1330**, 141, 10/10 | +426 (+43.5 %) |
| 150 MHz | p, 4, **1013**, 205, 10/10 | p, 8, **1560**, 216, 10/10 | p, 8, **1732**, 213, 10/10 | p, 8, **1648**, 202, 10/10 | +719 (+71.0 %) |
| 205 MHz (textbook at one adder per clock) | p, 4, **1013**, 205, 7/10 | p, 8, **1560**, 216, 9/10 | p, 8, **1732**, 213, 8/10 | none reaches it | +719 (+71.0 %) |

**(a) 16 points, W = 12, unpipelined (variant c: input register, all adders, output register), 10 seeds**

| design | adders / adder bits / depth | logic cells (same for every seed) | against textbook | adders alone, no output register: cells | against textbook | max MHz, nextpnr: median [lowest - highest] | max MHz, icetime: median |
|---|---|---|---|---|---|---|---|
| textbook | 64 / 928 / 4 | 1353 | - | 1328 | - | 65.4 [61.6 - 70.0] | 64.3 |
| 1994 design | 56 / 832 / 8 | 1008 | -345 (-25.5 %) | 999 | -329 (-24.8 %) | 55.9 [54.0 - 56.8] | 54.3 |
| this work | 52 / 772 / 8 | 1221 | -132 (-9.8 %) | 1092 | -236 (-17.8 %) | 49.3 [46.6 - 50.1] | 48.5 |
| this work, other signs | 52 / 772 / 8 | 1123 | -230 (-17.0 %) | 995 | -333 (-25.1 %) | 53.6 [51.4 - 54.9] | 52.3 |

**(b) 16 points, W = 12, fewest logic cells that reach a clock target** (cells include all registers of the design; entry = variant, latency in clocks, cells, median MHz, seeds reaching the target)

| clock target | textbook | 1994 design | this work | this work, other signs | this work against textbook |
|---|---|---|---|---|---|
| 12 MHz (board oscillator) | c, 1, **1353**, 65, 10/10 | c, 1, **1008**, 56, 10/10 | c, 1, **1221**, 49, 10/10 | c, 1, **1123**, 54, 10/10 | -132 (-9.8 %) |
| 50 MHz | c, 1, **1353**, 65, 10/10 | c, 1, **1008**, 56, 10/10 | p7, 2, **1354**, 54, 10/10 | c, 1, **1123**, 54, 10/10 | +1 (+0.1 %) |
| 75 MHz | p3, 2, **1363**, 96, 10/10 | p4, 2, **1034**, 90, 10/10 | p4, 2, **1526**, 85, 10/10 | p4, 2, **1411**, 85, 10/10 | +163 (+12.0 %) |
| 100 MHz | p2, 2, **1364**, 119, 10/10 | p3, 3, **1344**, 119, 10/10 | p3, 3, **1659**, 104, 9/10 | p2, 4, **1858**, 126, 10/10 | +295 (+21.6 %) |
| 125 MHz | p, 4, **1397**, 181, 10/10 | p2, 4, **1442**, 130, 7/10 | p2, 4, **1966**, 133, 10/10 | p2, 4, **1858**, 126, 6/10 | +569 (+40.7 %) |
| 150 MHz | p, 4, **1397**, 181, 10/10 | p, 8, **2200**, 182, 10/10 | p, 8, **2420**, 189, 10/10 | p, 8, **2304**, 185, 10/10 | +1023 (+73.2 %) |
| 181 MHz (textbook at one adder per clock) | p, 4, **1397**, 181, 5/10 | p, 8, **2200**, 182, 7/10 | p, 8, **2420**, 189, 10/10 | p, 8, **2304**, 185, 9/10 | +1023 (+73.2 %) |

**64 points and the 8 x 8 block, W = 8, unpipelined (variant c)**

| design | adders / adder bits / depth | logic cells of the design | against textbook | with the standard harness (1,412 cells): whole image of 7,680 | lean harness: max MHz nextpnr, median [lowest - highest], seeds |
|---|---|---|---|---|---|
| textbook (also the 8 x 8 block) | 384 / 4416 / 6 | 6337 | - | 7749 (does not fit) | 42.3 [40.1 - 43.2], 5 |
| 1994 design | 336 / 3984 / 12 | 4704 | -1633 (-25.8 %) | 6116 | 38.9 [37.7 - 39.8], 5 |
| this work, family | 304 / 3616 / 12 | 5370 | -967 (-15.3 %) | 6782 | 33.8 [33.3 - 35.4], 5 |
| this work, 19-adder circuit in two layers | 304 / 3640 / 12 | 4650 | -1687 (-26.6 %) | 6062 | 34.0 [33.3 - 34.8], 5 |

