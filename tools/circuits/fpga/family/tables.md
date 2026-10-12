### Table 1. On paper (from the circuit text; widths exact, counted by gen_rtl.py)

| N | design | adders | of them subtractions | depth (adder levels) | adder bits W=9 | adder bits W=12 | pipelined register bits W=9: after adders + delay = total | the same, W=12 |
|---|---|---|---|---|---|---|---|---|
| 16 | textbook | 64 | 32 | 4 | 736 | 928 | 736 + 0 = 736 | 928 + 0 = 928 |
| 16 | 1994 | 56 | 8 | 8 | 664 | 832 | 664 + 984 = 1648 | 832 + 1272 = 2104 |
| 16 | family | 52 | 32 | 8 | 616 | 772 | 616 + 944 = 1560 | 772 + 1208 = 1980 |
| 32 | textbook | 160 | 80 | 5 | 1920 | 2400 | 1920 + 0 = 1920 | 2400 + 0 = 2400 |
| 32 | 1994 | 144 | 32 | 9 | 1776 | 2208 | 1776 + 1984 = 3760 | 2208 + 2560 = 4768 |
| 32 | family | 128 | 80 | 10 | 1584 | 1968 | 1584 + 2512 = 4096 | 1968 + 3184 = 5152 |
| 64 | textbook | 384 | 192 | 6 | 4800 | 5952 | 4800 + 0 = 4800 | 5952 + 0 = 5952 |
| 64 | 1994 | 336 | 48 | 12 | 4320 | 5328 | 4320 + 6528 = 10848 | 5328 + 8256 = 13584 |
| 64 | family | 304 | 192 | 12 | 3920 | 4832 | 3920 + 6368 = 10288 | 4832 + 8000 = 12832 |
| 128 | textbook | 896 | 448 | 7 | 11648 | 14336 | 11648 + 0 = 11648 | 14336 + 0 = 14336 |
| 128 | 1994 | 800 | 160 | 13 | 10688 | 13088 | 10688 + 13152 = 23840 | 13088 + 16608 = 29696 |
| 128 | family | 704 | 448 | 14 | 9440 | 11552 | 9440 + 15616 = 25056 | 11552 + 19456 = 31008 |
| 256 | textbook | 2048 | 1024 | 8 | 27648 | 33792 | 27648 + 0 = 27648 | 33792 + 0 = 33792 |
| 256 | 1994 | 1792 | 256 | 16 | 24832 | 30208 | 24832 + 38144 = 62976 | 30208 + 47360 = 77568 |
| 256 | family | 1600 | 1024 | 16 | 22272 | 27072 | 22272 + 37376 = 59648 | 27072 + 46208 = 73280 |

### Table 2 (W = 9). Synthesis, combinational variant, bare core (no wrapper, no placement)

| N | design | iCE40: SB_LUT4 | iCE40: SB_CARRY | ECP5: LUT4 | ECP5: CCU2C | ECP5: LUT4 + 2 x CCU2C | Xilinx 7: LUTs | Xilinx 7: CARRY4 |
|---|---|---|---|---|---|---|---|---|
| 16 | textbook | 1006 | 672 | 0 | 384 | 768 | 638 | 208 |
| 16 | 1994 | 772 | 496 | 154 | 288 | 730 | 608 | 156 |
| 16 | family | 842 | 532 | 0 | 310 | 620 | 577 | 166 |
| 32 | textbook | 2622 | 1760 | 0 | 992 | 1984 | 1662 | 544 |
| 32 | 1994 | 2154 | 1408 | 308 | 800 | 1908 | 1602 | 440 |
| 32 | family | 2142 | 1376 | 0 | 796 | 1592 | 1480 | 436 |
| 64 | textbook | 6558 | 4416 | 0 | 2496 | 4992 | 4158 | 1344 |
| 64 | 1994 | 5028 | 3264 | 1002 | 1872 | 4746 | 3956 | 1008 |
| 64 | family | 5266 | 3424 | 0 | 1968 | 3936 | 3657 | 1064 |
| 128 | textbook | 15934 | 10752 | 0 | 6016 | 12032 | 10110 | 3200 |
| 128 | 1994 | 12874 | 8448 | 2004 | 4768 | 11540 | 9706 | 2528 |
| 128 | family | 12630 | 8288 | 0 | 4736 | 9472 | 8802 | 2512 |
| 256 | textbook | 37886 | 25600 | 0 | 14336 | 28672 | 24062 | 7680 |
| 256 | 1994 | 29012 | 18944 | 5802 | 10752 | 27306 | 22816 | 5760 |
| 256 | family | 29726 | 19648 | 0 | 11168 | 22336 | 20770 | 5952 |

### Table 3 (W = 9). Synthesis, pipelined variant (a register after every adder level), bare core

| N | design | iCE40: SB_LUT4 | iCE40: flip-flops | ECP5: LUT4 + 2 x CCU2C | ECP5: flip-flops | Xilinx 7: LUTs | Xilinx 7: shift-register LUTs (SRL16E + SRLC32E) | Xilinx 7: flip-flops | Xilinx 7: CARRY4 |
|---|---|---|---|---|---|---|---|---|---|
| 16 | textbook | 1040 | 740 | 768 | 740 | 672 | 1 | 736 | 208 |
| 16 | 1994 | 718 | 1616 | 664 | 1616 | 622 | 214 | 968 | 180 |
| 16 | family | 919 | 1554 | 620 | 1554 | 583 | 169 | 1042 | 166 |
| 32 | textbook | 2720 | 1925 | 1984 | 1925 | 1760 | 1 | 1920 | 544 |
| 32 | 1994 | 2060 | 3693 | 1776 | 3693 | 1644 | 427 | 2404 | 488 |
| 32 | family | 2378 | 4062 | 1592 | 4062 | 1504 | 525 | 2480 | 436 |
| 64 | textbook | 6816 | 4806 | 4992 | 4806 | 4416 | 1 | 4800 | 1344 |
| 64 | 1994 | 4688 | 10572 | 4320 | 10572 | 4064 | 1555 | 5874 | 1168 |
| 64 | family | 5916 | 10180 | 3936 | 10180 | 3732 | 1457 | 5800 | 1064 |
| 128 | textbook | 16576 | 11655 | 12032 | 11655 | 10752 | 1 | 11648 | 3200 |
| 128 | 1994 | 12256 | 23309 | 10688 | 23309 | 9984 | 3121 | 13888 | 2848 |
| 128 | family | 14312 | 24766 | 9472 | 24766 | 9008 | 3793 | 13376 | 2512 |
| 256 | textbook | 39424 | 27656 | 28672 | 27656 | 25600 | 1 | 27648 | 7680 |
| 256 | 1994 | 27040 | 61328 | 24832 | 61328 | 23456 | 9547 | 32380 | 6656 |
| 256 | family | 33904 | 58928 | 22336 | 58928 | 21296 | 9473 | 30496 | 5952 |

### Table 4 (W = 9). After packing by nextpnr (--pack-only), wrapper subtracted

iCE40: logic cells (ICESTORM_LC; one cell = one LUT4 + carry + one flip-flop).  ECP5: TRELLIS_COMB (LUT4 places; a CCU2C takes two) and TRELLIS_FF.  In brackets: the wrapper alone (null core), which was subtracted.

| N | design | iCE40 cells, combinational | iCE40 cells, pipelined | ECP5 COMB, combinational | ECP5 COMB + FF, pipelined |
|---|---|---|---|---|---|
| 16 | textbook | 1040 (wrapper 356) | 1140 (wrapper 356) | 1025 (wrapper 209; FF 0) | 1025 + 740 = 1765 |
| 16 | 1994 | 783 (wrapper 356) | 1715 (wrapper 356) | 923 (wrapper 209; FF 0) | 889 + 1616 = 2505 |
| 16 | family | 858 (wrapper 356) | 1904 (wrapper 356) | 829 (wrapper 209; FF 0) | 829 + 1554 = 2383 |
| 32 | textbook | 2720 (wrapper 740) | 2965 (wrapper 740) | 2625 (wrapper 449; FF 0) | 2625 + 1925 = 4550 |
| 32 | 1994 | 2206 (wrapper 740) | 4119 (wrapper 740) | 2421 (wrapper 449; FF 0) | 2353 + 3693 = 6046 |
| 32 | family | 2183 (wrapper 740) | 4975 (wrapper 740) | 2105 (wrapper 449; FF 0) | 2105 + 4062 = 6167 |
| 64 | textbook | 6816 (wrapper 1540) | 7398 (wrapper 1540) | 6529 (wrapper 961; FF 0) | 6529 + 4806 = 11335 |
| 64 | 1994 | 5103 (wrapper 1540) | 11220 (wrapper 1540) | 5899 (wrapper 961; FF 0) | 5665 + 10572 = 16237 |
| 64 | family | 5369 (wrapper 1540) | 12464 (wrapper 1540) | 5153 (wrapper 961; FF 0) | 5153 + 10180 = 15333 |
| 128 | textbook | 16576 (wrapper 3204) | 17926 (wrapper 3204) | 15617 (wrapper 2049; FF 0) | 15617 + 11655 = 27272 |
| 128 | 1994 | 13150 (wrapper 3204) | 25645 (wrapper 3204) | 14357 (wrapper 2049; FF 0) | 13889 + 23309 = 37198 |
| 128 | family | 12881 (wrapper 3204) | 30314 (wrapper 3204) | 12289 (wrapper 2049; FF 0) | 12289 + 24766 = 37055 |
| 256 | textbook | 39424 (wrapper 6660) | 42504 (wrapper 6660) | 36865 (wrapper 4353; FF 0) | 36865 + 27656 = 64521 |
| 256 | 1994 | 29439 (wrapper 6660) | 65056 (wrapper 6660) | 33451 (wrapper 4353; FF 0) | 32001 + 61328 = 93329 |
| 256 | family | 30321 (wrapper 6660) | 72112 (wrapper 6660) | 28737 (wrapper 4353; FF 0) | 28737 + 58928 = 87665 |

### Table 5 (W = 9). Place and route (nextpnr 0.11.1-59, --freq 200, seeds 1, 2, 3), wrapper subtracted

| N | design | variant | chip | cells per seed (wrapper subtracted) | maximum frequency per seed, MHz | median MHz | note |
|---|---|---|---|---|---|---|---|
| 16 | textbook | combinational | iCE40-HX8K ct256 | 1040 / 1040 / 1040 | 70.03 / 74.56 / 69.65 | 70.03 |  |
| 16 | 1994 | combinational | iCE40-HX8K ct256 | 783 / 783 / 783 | 55.93 / 55.63 / 55.71 | 55.71 |  |
| 16 | family | combinational | iCE40-HX8K ct256 | 858 / 858 / 858 | 50.59 / 46.81 / 49.24 | 49.24 |  |
| 16 | textbook | pipelined | iCE40-HX8K ct256 | 1140 / 1140 / 1140 | 192.79 / 195.16 / 188.22 | 192.79 |  |
| 16 | 1994 | pipelined | iCE40-HX8K ct256 | 1715 / 1715 / 1715 | 207.94 / 195.16 / 215.47 | 207.94 |  |
| 16 | family | pipelined | iCE40-HX8K ct256 | 1904 / 1904 / 1904 | 200.08 / 208.25 / 208.25 | 208.25 |  |
| 32 | textbook | combinational | iCE40-HX8K ct256 | 2720 / 2720 / 2720 | 58.12 / 59.45 / 60.00 | 59.45 |  |
| 32 | 1994 | combinational | iCE40-HX8K ct256 | 2206 / 2206 / 2206 | 46.62 / 44.63 / 47.05 | 46.62 |  |
| 32 | family | combinational | iCE40-HX8K ct256 | 2183 / 2183 / 2183 | 40.71 / 40.63 / 40.50 | 40.63 |  |
| 32 | textbook | pipelined | iCE40-HX8K ct256 | 2965 / 2965 / 2965 | 177.68 / 181.98 / 190.22 | 181.98 |  |
| 32 | 1994 | pipelined | iCE40-HX8K ct256 | 4119 / 4119 / 4119 | 176.37 / 180.12 / 186.25 | 180.12 |  |
| 32 | family | pipelined | iCE40-HX8K ct256 | 4975 / 4975 / 4975 | 181.23 / 187.48 / 193.05 | 187.48 |  |
| 64 | textbook | combinational | iCE40-HX8K ct256 | 6816 / 6816 / 6816 | - / - / - | - | does not fit: 8356 logic cells with the wrapper, 7,680 on the chip |
| 64 | 1994 | combinational | iCE40-HX8K ct256 | 5103 / 5103 / 5103 | 38.35 / 37.55 / 37.58 | 37.58 |  |
| 64 | family | combinational | iCE40-HX8K ct256 | 5369 / 5369 / 5369 | 33.43 / 33.57 / 33.84 | 33.57 |  |
| 64 | textbook | pipelined | iCE40-HX8K ct256 | 7398 / 7398 / 7398 | - / - / - | - | does not fit: 8938 logic cells with the wrapper, 7,680 on the chip |
| 64 | 1994 | pipelined | iCE40-HX8K ct256 | 11220 / 11220 / 11220 | - / - / - | - | does not fit: 12760 logic cells with the wrapper, 7,680 on the chip |
| 64 | family | pipelined | iCE40-HX8K ct256 | 12464 / 12464 / 12464 | - / - / - | - | does not fit: 14004 logic cells with the wrapper, 7,680 on the chip |
| 64 | textbook | combinational | ECP5 LFE5U-85F CABGA381 | 6529 COMB + 0 FF / 6529 COMB + 0 FF / 6529 COMB + 0 FF | 57.39 / 56.76 / 57.05 | 57.05 |  |
| 64 | 1994 | combinational | ECP5 LFE5U-85F CABGA381 | 5899 COMB + 0 FF / 5899 COMB + 0 FF / 5899 COMB + 0 FF | 38.42 / 39.34 / 40.10 | 39.34 |  |
| 64 | family | combinational | ECP5 LFE5U-85F CABGA381 | 5153 COMB + 0 FF / 5153 COMB + 0 FF / 5153 COMB + 0 FF | 35.85 / 35.82 / 35.43 | 35.82 |  |
| 64 | textbook | pipelined | ECP5 LFE5U-85F CABGA381 | 6529 COMB + 4806 FF | 232.07 | 232.07 |  |
| 64 | 1994 | pipelined | ECP5 LFE5U-85F CABGA381 | 5665 COMB + 10572 FF | 215.24 | 215.24 |  |
| 64 | family | pipelined | ECP5 LFE5U-85F CABGA381 | 5153 COMB + 10180 FF | 236.85 | 236.85 |  |
| 128 | textbook | combinational | ECP5 LFE5U-85F CABGA381 | 15617 COMB + 0 FF / 15617 COMB + 0 FF / 15617 COMB + 0 FF | 46.18 / 45.26 / 47.14 | 46.18 |  |
| 128 | 1994 | combinational | ECP5 LFE5U-85F CABGA381 | 14357 COMB + 0 FF / 14357 COMB + 0 FF / 14357 COMB + 0 FF | 34.64 / 33.39 / 34.10 | 34.10 |  |
| 128 | family | combinational | ECP5 LFE5U-85F CABGA381 | 12289 COMB + 0 FF / 12289 COMB + 0 FF / 12289 COMB + 0 FF | 29.31 / 29.34 / 30.38 | 29.34 |  |
| 128 | textbook | pipelined | ECP5 LFE5U-85F CABGA381 | 15617 COMB + 11655 FF | 200.56 | 200.56 |  |
| 128 | 1994 | pipelined | ECP5 LFE5U-85F CABGA381 | 13889 COMB + 23309 FF | 195.58 | 195.58 |  |
| 128 | family | pipelined | ECP5 LFE5U-85F CABGA381 | 12289 COMB + 24766 FF | 200.04 | 200.04 |  |
| 256 | textbook | combinational | ECP5 LFE5U-85F CABGA381 | 36865 COMB + 0 FF | - | - | not routed: stopped by hand after 6 of its 10 minutes, with 92,550 connections still to route (111,173 at the start of routing); after placement the tool estimated 30.98 MHz |
| 256 | 1994 | combinational | ECP5 LFE5U-85F CABGA381 | 33451 COMB + 0 FF | 27.26 | 27.26 |  |
| 256 | family | combinational | ECP5 LFE5U-85F CABGA381 | 28737 COMB + 0 FF | 25.54 | 25.54 |  |

### Table 2 (W = 12). Synthesis, combinational variant, bare core (no wrapper, no placement)

| N | design | iCE40: SB_LUT4 | iCE40: SB_CARRY | ECP5: LUT4 | ECP5: CCU2C | ECP5: LUT4 + 2 x CCU2C | Xilinx 7: LUTs | Xilinx 7: CARRY4 |
|---|---|---|---|---|---|---|---|---|
| 16 | textbook | 1294 | 864 | 0 | 480 | 960 | 830 | 256 |
| 16 | 1994 | 988 | 640 | 202 | 360 | 922 | 776 | 192 |
| 16 | family | 1076 | 688 | 0 | 390 | 780 | 733 | 208 |
| 32 | textbook | 3342 | 2240 | 0 | 1248 | 2496 | 2142 | 672 |
| 32 | 1994 | 2730 | 1792 | 404 | 1008 | 2420 | 2034 | 544 |
| 32 | family | 2712 | 1760 | 0 | 992 | 1984 | 1864 | 532 |
| 64 | textbook | 8286 | 5568 | 0 | 3072 | 6144 | 5310 | 1664 |
| 64 | 1994 | 6324 | 4128 | 1290 | 2304 | 5898 | 4964 | 1248 |
| 64 | family | 6610 | 4336 | 0 | 2432 | 4864 | 4569 | 1320 |
| 128 | textbook | 19966 | 13440 | 0 | 7424 | 14848 | - | - |
| 128 | 1994 | 16042 | 10560 | 2580 | 5888 | 14356 | - | - |
| 128 | family | 15726 | 10400 | 0 | 5808 | 11616 | - | - |
| 256 | textbook | 47102 | 31744 | 0 | 17408 | 34816 | - | - |
| 256 | 1994 | 35924 | 23552 | 7338 | 13056 | 33450 | - | - |
| 256 | family | 36734 | 24448 | 0 | 13600 | 27200 | - | - |

### Table 3 (W = 12). Synthesis, pipelined variant (a register after every adder level), bare core

| N | design | iCE40: SB_LUT4 | iCE40: flip-flops | ECP5: LUT4 + 2 x CCU2C | ECP5: flip-flops | Xilinx 7: LUTs | Xilinx 7: shift-register LUTs (SRL16E + SRLC32E) | Xilinx 7: flip-flops | Xilinx 7: CARRY4 |
|---|---|---|---|---|---|---|---|---|---|
| 16 | textbook | 1328 | 932 | - | - | - | - | - | - |
| 16 | 1994 | 910 | 2072 | - | - | - | - | - | - |
| 16 | family | 1171 | 1974 | - | - | - | - | - | - |
| 32 | textbook | 3440 | 2405 | - | - | - | - | - | - |
| 32 | 1994 | 2588 | 4701 | - | - | - | - | - | - |
| 32 | family | 3002 | 5118 | - | - | - | - | - | - |
| 64 | textbook | 8544 | 5958 | - | - | - | - | - | - |
| 64 | 1994 | 5840 | 13308 | - | - | - | - | - | - |
| 64 | family | 7404 | 12724 | - | - | - | - | - | - |
| 128 | textbook | 20608 | 14343 | - | - | - | - | - | - |
| 128 | 1994 | 15136 | 29165 | - | - | - | - | - | - |
| 128 | family | 17768 | 30718 | - | - | - | - | - | - |
| 256 | textbook | 48640 | 33800 | - | - | - | - | - | - |
| 256 | 1994 | 33184 | 75920 | - | - | - | - | - | - |
| 256 | family | 41776 | 72560 | - | - | - | - | - | - |

### Table 4 (W = 12). After packing by nextpnr (--pack-only), wrapper subtracted

iCE40: logic cells (ICESTORM_LC; one cell = one LUT4 + carry + one flip-flop).  ECP5: TRELLIS_COMB (LUT4 places; a CCU2C takes two) and TRELLIS_FF.  In brackets: the wrapper alone (null core), which was subtracted.

| N | design | iCE40 cells, combinational | iCE40 cells, pipelined | ECP5 COMB, combinational | ECP5 COMB + FF, pipelined |
|---|---|---|---|---|---|
| 16 | textbook | - | - | - | - |
| 16 | 1994 | - | - | - | - |
| 16 | family | - | - | - | - |
| 32 | textbook | - | - | - | - |
| 32 | 1994 | - | - | - | - |
| 32 | family | - | - | - | - |
| 64 | textbook | - | - | - | - |
| 64 | 1994 | - | - | - | - |
| 64 | family | - | - | - | - |
| 128 | textbook | - | - | - | - |
| 128 | 1994 | - | - | - | - |
| 128 | family | - | - | - | - |
| 256 | textbook | - | - | - | - |
| 256 | 1994 | - | - | - | - |
| 256 | family | - | - | - | - |

### Table 5 (W = 12). Place and route (nextpnr 0.11.1-59, --freq 200, seeds 1, 2, 3), wrapper subtracted

| N | design | variant | chip | cells per seed (wrapper subtracted) | maximum frequency per seed, MHz | median MHz | note |
|---|---|---|---|---|---|---|---|

### Table 6 (W = 9). The answer: one block per size

Columns: adders and adder bits are on paper.  LUTs are after synthesis of the combinational variant (iCE40: SB_LUT4; ECP5: LUT4 + 2 x CCU2C; Xilinx 7-series: LUTs, and CARRY4 cells).  "Placed" is after place and route with the wrapper subtracted (median of the seeds that ran; iCE40-HX8K logic cells, ECP5-85F TRELLIS_COMB); where a design was only packed, the packed figure is given with "(packed)".  MHz is the median maximum frequency of the combinational variant between the wrapper's registers.  The last three columns are the pipelined variant, registers included: iCE40 logic cells after packing; ECP5 COMB + FF after packing; Xilinx LUTs + shift-register LUTs + flip-flops after synthesis.

| N | design | adders | adder bits | iCE40 LUT4 | ECP5 LUT | Xilinx LUT | Xilinx CARRY4 | iCE40 placed cells | ECP5 placed COMB | depth | iCE40 MHz | ECP5 MHz | pipelined: iCE40 cells | pipelined: ECP5 COMB+FF | pipelined: Xilinx LUT+SRL+FF |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 16 | textbook | 64 | 736 | 1006 | 768 | 638 | 208 | 1040 | 1025 (packed) | 4 | 70.03 | - | 1140 | 1765 | 1409 |
| 16 | 1994 | 56 | 664 | 772 | 730 | 608 | 156 | 783 | 923 (packed) | 8 | 55.71 | - | 1715 | 2505 | 1804 |
| 16 | family | 52 | 616 | 842 | 620 | 577 | 166 | 858 | 829 (packed) | 8 | 49.24 | - | 1904 | 2383 | 1794 |
| 16 | **family / textbook** | 0.812 | 0.837 | 0.837 | 0.807 | 0.904 | 0.798 | 0.825 | 0.809 | 2.000 | 0.703 | - | 1.670 | 1.350 | 1.273 |
| 16 | **family / 1994** | 0.929 | 0.928 | 1.091 | 0.849 | 0.949 | 1.064 | 1.096 | 0.898 | 1.000 | 0.884 | - | 1.110 | 0.951 | 0.994 |
| 32 | textbook | 160 | 1920 | 2622 | 1984 | 1662 | 544 | 2720 | 2625 (packed) | 5 | 59.45 | - | 2965 | 4550 | 3681 |
| 32 | 1994 | 144 | 1776 | 2154 | 1908 | 1602 | 440 | 2206 | 2421 (packed) | 9 | 46.62 | - | 4119 | 6046 | 4475 |
| 32 | family | 128 | 1584 | 2142 | 1592 | 1480 | 436 | 2183 | 2105 (packed) | 10 | 40.63 | - | 4975 | 6167 | 4509 |
| 32 | **family / textbook** | 0.800 | 0.825 | 0.817 | 0.802 | 0.890 | 0.801 | 0.803 | 0.802 | 2.000 | 0.683 | - | 1.678 | 1.355 | 1.225 |
| 32 | **family / 1994** | 0.889 | 0.892 | 0.994 | 0.834 | 0.924 | 0.991 | 0.990 | 0.869 | 1.111 | 0.872 | - | 1.208 | 1.020 | 1.008 |
| 64 | textbook | 384 | 4800 | 6558 | 4992 | 4158 | 1344 | 6816 (packed) | 6529 | 6 | - | 57.05 | 7398 | 11335 | 9217 |
| 64 | 1994 | 336 | 4320 | 5028 | 4746 | 3956 | 1008 | 5103 | 5899 | 12 | 37.58 | 39.34 | 11220 | 16237 | 11493 |
| 64 | family | 304 | 3920 | 5266 | 3936 | 3657 | 1064 | 5369 | 5153 | 12 | 33.57 | 35.82 | 12464 | 15333 | 10989 |
| 64 | **family / textbook** | 0.792 | 0.817 | 0.803 | 0.788 | 0.880 | 0.792 | 0.788 | 0.789 | 2.000 | - | 0.628 | 1.685 | 1.353 | 1.192 |
| 64 | **family / 1994** | 0.905 | 0.907 | 1.047 | 0.829 | 0.924 | 1.056 | 1.052 | 0.874 | 1.000 | 0.893 | 0.911 | 1.111 | 0.944 | 0.956 |
| 128 | textbook | 896 | 11648 | 15934 | 12032 | 10110 | 3200 | 16576 (packed) | 15617 | 7 | - | 46.18 | 17926 | 27272 | 22401 |
| 128 | 1994 | 800 | 10688 | 12874 | 11540 | 9706 | 2528 | 13150 (packed) | 14357 | 13 | - | 34.10 | 25645 | 37198 | 26993 |
| 128 | family | 704 | 9440 | 12630 | 9472 | 8802 | 2512 | 12881 (packed) | 12289 | 14 | - | 29.34 | 30314 | 37055 | 26177 |
| 128 | **family / textbook** | 0.786 | 0.810 | 0.793 | 0.787 | 0.871 | 0.785 | 0.777 | 0.787 | 2.000 | - | 0.635 | 1.691 | 1.359 | 1.169 |
| 128 | **family / 1994** | 0.880 | 0.883 | 0.981 | 0.821 | 0.907 | 0.994 | 0.980 | 0.856 | 1.077 | - | 0.860 | 1.182 | 0.996 | 0.970 |
| 256 | textbook | 2048 | 27648 | 37886 | 28672 | 24062 | 7680 | 39424 (packed) | 36865 (packed) | 8 | - | - | 42504 | 64521 | 53249 |
| 256 | 1994 | 1792 | 24832 | 29012 | 27306 | 22816 | 5760 | 29439 (packed) | 33451 | 16 | - | 27.26 | 65056 | 93329 | 65383 |
| 256 | family | 1600 | 22272 | 29726 | 22336 | 20770 | 5952 | 30321 (packed) | 28737 | 16 | - | 25.54 | 72112 | 87665 | 61265 |
| 256 | **family / textbook** | 0.781 | 0.806 | 0.785 | 0.779 | 0.863 | 0.775 | 0.769 | 0.780 | 2.000 | - | - | 1.697 | 1.359 | 1.151 |
| 256 | **family / 1994** | 0.893 | 0.897 | 1.025 | 0.818 | 0.910 | 1.033 | 1.030 | 0.859 | 1.000 | - | 0.937 | 1.108 | 0.939 | 0.937 |

### Table 6 (W = 12). The answer: one block per size

Columns: adders and adder bits are on paper.  LUTs are after synthesis of the combinational variant (iCE40: SB_LUT4; ECP5: LUT4 + 2 x CCU2C; Xilinx 7-series: LUTs, and CARRY4 cells).  "Placed" is after place and route with the wrapper subtracted (median of the seeds that ran; iCE40-HX8K logic cells, ECP5-85F TRELLIS_COMB); where a design was only packed, the packed figure is given with "(packed)".  MHz is the median maximum frequency of the combinational variant between the wrapper's registers.  The last three columns are the pipelined variant, registers included: iCE40 logic cells after packing; ECP5 COMB + FF after packing; Xilinx LUTs + shift-register LUTs + flip-flops after synthesis.

| N | design | adders | adder bits | iCE40 LUT4 | ECP5 LUT | Xilinx LUT | Xilinx CARRY4 | iCE40 placed cells | ECP5 placed COMB | depth | iCE40 MHz | ECP5 MHz | pipelined: iCE40 cells | pipelined: ECP5 COMB+FF | pipelined: Xilinx LUT+SRL+FF |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 16 | textbook | 64 | 928 | 1294 | 960 | 830 | 256 | - | - | 4 | - | - | - | - | - |
| 16 | 1994 | 56 | 832 | 988 | 922 | 776 | 192 | - | - | 8 | - | - | - | - | - |
| 16 | family | 52 | 772 | 1076 | 780 | 733 | 208 | - | - | 8 | - | - | - | - | - |
| 16 | **family / textbook** | 0.812 | 0.832 | 0.832 | 0.812 | 0.883 | 0.812 | - | - | 2.000 | - | - | - | - | - |
| 16 | **family / 1994** | 0.929 | 0.928 | 1.089 | 0.846 | 0.945 | 1.083 | - | - | 1.000 | - | - | - | - | - |
| 32 | textbook | 160 | 2400 | 3342 | 2496 | 2142 | 672 | - | - | 5 | - | - | - | - | - |
| 32 | 1994 | 144 | 2208 | 2730 | 2420 | 2034 | 544 | - | - | 9 | - | - | - | - | - |
| 32 | family | 128 | 1968 | 2712 | 1984 | 1864 | 532 | - | - | 10 | - | - | - | - | - |
| 32 | **family / textbook** | 0.800 | 0.820 | 0.811 | 0.795 | 0.870 | 0.792 | - | - | 2.000 | - | - | - | - | - |
| 32 | **family / 1994** | 0.889 | 0.891 | 0.993 | 0.820 | 0.916 | 0.978 | - | - | 1.111 | - | - | - | - | - |
| 64 | textbook | 384 | 5952 | 8286 | 6144 | 5310 | 1664 | - | - | 6 | - | - | - | - | - |
| 64 | 1994 | 336 | 5328 | 6324 | 5898 | 4964 | 1248 | - | - | 12 | - | - | - | - | - |
| 64 | family | 304 | 4832 | 6610 | 4864 | 4569 | 1320 | - | - | 12 | - | - | - | - | - |
| 64 | **family / textbook** | 0.792 | 0.812 | 0.798 | 0.792 | 0.860 | 0.793 | - | - | 2.000 | - | - | - | - | - |
| 64 | **family / 1994** | 0.905 | 0.907 | 1.045 | 0.825 | 0.920 | 1.058 | - | - | 1.000 | - | - | - | - | - |
| 128 | textbook | 896 | 14336 | 19966 | 14848 | - | - | - | - | 7 | - | - | - | - | - |
| 128 | 1994 | 800 | 13088 | 16042 | 14356 | - | - | - | - | 13 | - | - | - | - | - |
| 128 | family | 704 | 11552 | 15726 | 11616 | - | - | - | - | 14 | - | - | - | - | - |
| 128 | **family / textbook** | 0.786 | 0.806 | 0.788 | 0.782 | - | - | - | - | 2.000 | - | - | - | - | - |
| 128 | **family / 1994** | 0.880 | 0.883 | 0.980 | 0.809 | - | - | - | - | 1.077 | - | - | - | - | - |
| 256 | textbook | 2048 | 33792 | 47102 | 34816 | - | - | - | - | 8 | - | - | - | - | - |
| 256 | 1994 | 1792 | 30208 | 35924 | 33450 | - | - | - | - | 16 | - | - | - | - | - |
| 256 | family | 1600 | 27072 | 36734 | 27200 | - | - | - | - | 16 | - | - | - | - | - |
| 256 | **family / textbook** | 0.781 | 0.801 | 0.780 | 0.781 | - | - | - | - | 2.000 | - | - | - | - | - |
| 256 | **family / 1994** | 0.893 | 0.896 | 1.023 | 0.813 | - | - | - | - | 1.000 | - | - | - | - | - |

### Table 7 (W = 9). Sensitivity: every adder line kept as written ("(* keep *)" on every adder wire), combinational

By default yosys merges the two additions z0 = x1 + x2, z1 = z0 + x3 of the 1994 circuit into one sum of three (a row of full adders in LUTs and one carry chain).  With the attribute it cannot.  Textbook and family were run this way at 16 and 32 points only, as a control.

| N | design | iCE40 SB_LUT4: default -> kept | ECP5 LUT4 + 2 x CCU2C: default -> kept | Xilinx LUTs: default -> kept | Xilinx CARRY4: default -> kept |
|---|---|---|---|---|---|
| 16 | textbook | 1006 -> 1006 | 768 -> 768 | 638 -> 638 | 208 -> 208 |
| 16 | 1994 | 772 -> 716 | 730 -> 664 | 608 -> 612 | 156 -> 180 |
| 16 | family | 842 -> 878 | 620 -> 620 | 577 -> 582 | 166 -> 166 |
| 32 | textbook | 2622 -> 2622 | 1984 -> 1984 | 1662 -> 1662 | 544 -> 544 |
| 32 | 1994 | 2154 -> 2042 | 1908 -> 1776 | 1602 -> 1610 | 440 -> 488 |
| 32 | family | 2142 -> 2250 | 1592 -> 1592 | 1480 -> 1494 | 436 -> 436 |
| 64 | 1994 | 5028 -> 4644 | 4746 -> 4320 | 3956 -> 3972 | 1008 -> 1168 |
| 128 | 1994 | 12874 -> 12106 | 11540 -> 10688 | - | - |
| 256 | 1994 | 29012 -> 26708 | 27306 -> 24832 | - | - |

Family (default) divided by 1994 (kept), W = 9, combinational:

| N | adders | adder bits | iCE40 SB_LUT4 | ECP5 LUT4 + 2 x CCU2C | Xilinx LUTs | Xilinx CARRY4 |
|---|---|---|---|---|---|---|
| 16 | 0.929 | 0.928 | 1.176 | 0.934 | 0.943 | 0.922 |
| 32 | 0.889 | 0.892 | 1.049 | 0.896 | 0.919 | 0.893 |
| 64 | 0.905 | 0.907 | 1.134 | 0.911 | 0.921 | 0.911 |
| 128 | 0.880 | 0.883 | 1.043 | 0.886 | - | - |
| 256 | 0.893 | 0.897 | 1.113 | 0.899 | - | - |

