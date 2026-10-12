// Written by gen_rtl.py.  Do not edit by hand.
// 64-point Walsh-Hadamard transform, y_J = sum over i of (-1)^popcount(J & i) * x_i.
// Source circuit: tools/circuits/fpga/rtl/circuits/8x8_textbook.txt
// 2-D 8 x 8: the textbook 8-point transform on rows, then on columns (16 transforms, 384 adders).
// It is the same network of adders as 64_textbook, in another order of lines.
// Inputs: 64 signed values of 8 bits.  Outputs: 64 signed values of 14 bits.
// Adders 384, depth 6 adder levels, adder bits 4416 (chain bits 4416).
// Variant p2: a register after every second adder level.  Latency 3.
// Register bits: 2304 after adders, 0 in delay registers, 3 valid bits.
`default_nettype none
module wht_8x8_textbook_p2_w8 (
    input  wire                 clk,
    input  wire                 in_valid,
    input  wire [511:0] in_data,
    output wire                 out_valid,
    output wire [895:0] out_data
);
    wire signed [7:0] x0 = in_data[7:0];
    wire signed [7:0] x1 = in_data[15:8];
    wire signed [7:0] x2 = in_data[23:16];
    wire signed [7:0] x3 = in_data[31:24];
    wire signed [7:0] x4 = in_data[39:32];
    wire signed [7:0] x5 = in_data[47:40];
    wire signed [7:0] x6 = in_data[55:48];
    wire signed [7:0] x7 = in_data[63:56];
    wire signed [7:0] x8 = in_data[71:64];
    wire signed [7:0] x9 = in_data[79:72];
    wire signed [7:0] x10 = in_data[87:80];
    wire signed [7:0] x11 = in_data[95:88];
    wire signed [7:0] x12 = in_data[103:96];
    wire signed [7:0] x13 = in_data[111:104];
    wire signed [7:0] x14 = in_data[119:112];
    wire signed [7:0] x15 = in_data[127:120];
    wire signed [7:0] x16 = in_data[135:128];
    wire signed [7:0] x17 = in_data[143:136];
    wire signed [7:0] x18 = in_data[151:144];
    wire signed [7:0] x19 = in_data[159:152];
    wire signed [7:0] x20 = in_data[167:160];
    wire signed [7:0] x21 = in_data[175:168];
    wire signed [7:0] x22 = in_data[183:176];
    wire signed [7:0] x23 = in_data[191:184];
    wire signed [7:0] x24 = in_data[199:192];
    wire signed [7:0] x25 = in_data[207:200];
    wire signed [7:0] x26 = in_data[215:208];
    wire signed [7:0] x27 = in_data[223:216];
    wire signed [7:0] x28 = in_data[231:224];
    wire signed [7:0] x29 = in_data[239:232];
    wire signed [7:0] x30 = in_data[247:240];
    wire signed [7:0] x31 = in_data[255:248];
    wire signed [7:0] x32 = in_data[263:256];
    wire signed [7:0] x33 = in_data[271:264];
    wire signed [7:0] x34 = in_data[279:272];
    wire signed [7:0] x35 = in_data[287:280];
    wire signed [7:0] x36 = in_data[295:288];
    wire signed [7:0] x37 = in_data[303:296];
    wire signed [7:0] x38 = in_data[311:304];
    wire signed [7:0] x39 = in_data[319:312];
    wire signed [7:0] x40 = in_data[327:320];
    wire signed [7:0] x41 = in_data[335:328];
    wire signed [7:0] x42 = in_data[343:336];
    wire signed [7:0] x43 = in_data[351:344];
    wire signed [7:0] x44 = in_data[359:352];
    wire signed [7:0] x45 = in_data[367:360];
    wire signed [7:0] x46 = in_data[375:368];
    wire signed [7:0] x47 = in_data[383:376];
    wire signed [7:0] x48 = in_data[391:384];
    wire signed [7:0] x49 = in_data[399:392];
    wire signed [7:0] x50 = in_data[407:400];
    wire signed [7:0] x51 = in_data[415:408];
    wire signed [7:0] x52 = in_data[423:416];
    wire signed [7:0] x53 = in_data[431:424];
    wire signed [7:0] x54 = in_data[439:432];
    wire signed [7:0] x55 = in_data[447:440];
    wire signed [7:0] x56 = in_data[455:448];
    wire signed [7:0] x57 = in_data[463:456];
    wire signed [7:0] x58 = in_data[471:464];
    wire signed [7:0] x59 = in_data[479:472];
    wire signed [7:0] x60 = in_data[487:480];
    wire signed [7:0] x61 = in_data[495:488];
    wire signed [7:0] x62 = in_data[503:496];
    wire signed [7:0] x63 = in_data[511:504];
    wire signed [8:0] n_t1 = x0 + x1;   // level 1, stage 1
    wire signed [8:0] n_t2 = x0 - x1;   // level 1, stage 1
    wire signed [8:0] n_t3 = x2 + x3;   // level 1, stage 1
    wire signed [8:0] n_t4 = x2 - x3;   // level 1, stage 1
    wire signed [8:0] n_t5 = x4 + x5;   // level 1, stage 1
    wire signed [8:0] n_t6 = x4 - x5;   // level 1, stage 1
    wire signed [8:0] n_t7 = x6 + x7;   // level 1, stage 1
    wire signed [8:0] n_t8 = x6 - x7;   // level 1, stage 1
    wire signed [9:0] n_t9 = n_t1 + n_t3;   // level 2, stage 1
    reg  signed [9:0] n_t9_r1;
    wire signed [9:0] n_t10 = n_t1 - n_t3;   // level 2, stage 1
    reg  signed [9:0] n_t10_r1;
    wire signed [9:0] n_t11 = n_t2 + n_t4;   // level 2, stage 1
    reg  signed [9:0] n_t11_r1;
    wire signed [9:0] n_t12 = n_t2 - n_t4;   // level 2, stage 1
    reg  signed [9:0] n_t12_r1;
    wire signed [9:0] n_t13 = n_t5 + n_t7;   // level 2, stage 1
    reg  signed [9:0] n_t13_r1;
    wire signed [9:0] n_t14 = n_t5 - n_t7;   // level 2, stage 1
    reg  signed [9:0] n_t14_r1;
    wire signed [9:0] n_t15 = n_t6 + n_t8;   // level 2, stage 1
    reg  signed [9:0] n_t15_r1;
    wire signed [9:0] n_t16 = n_t6 - n_t8;   // level 2, stage 1
    reg  signed [9:0] n_t16_r1;
    wire signed [10:0] n_t17 = n_t9_r1 + n_t13_r1;   // level 3, stage 2
    wire signed [10:0] n_t18 = n_t9_r1 - n_t13_r1;   // level 3, stage 2
    wire signed [10:0] n_t19 = n_t11_r1 + n_t15_r1;   // level 3, stage 2
    wire signed [10:0] n_t20 = n_t11_r1 - n_t15_r1;   // level 3, stage 2
    wire signed [10:0] n_t21 = n_t10_r1 + n_t14_r1;   // level 3, stage 2
    wire signed [10:0] n_t22 = n_t10_r1 - n_t14_r1;   // level 3, stage 2
    wire signed [10:0] n_t23 = n_t12_r1 + n_t16_r1;   // level 3, stage 2
    wire signed [10:0] n_t24 = n_t12_r1 - n_t16_r1;   // level 3, stage 2
    wire signed [8:0] n_t25 = x8 + x9;   // level 1, stage 1
    wire signed [8:0] n_t26 = x8 - x9;   // level 1, stage 1
    wire signed [8:0] n_t27 = x10 + x11;   // level 1, stage 1
    wire signed [8:0] n_t28 = x10 - x11;   // level 1, stage 1
    wire signed [8:0] n_t29 = x12 + x13;   // level 1, stage 1
    wire signed [8:0] n_t30 = x12 - x13;   // level 1, stage 1
    wire signed [8:0] n_t31 = x14 + x15;   // level 1, stage 1
    wire signed [8:0] n_t32 = x14 - x15;   // level 1, stage 1
    wire signed [9:0] n_t33 = n_t25 + n_t27;   // level 2, stage 1
    reg  signed [9:0] n_t33_r1;
    wire signed [9:0] n_t34 = n_t25 - n_t27;   // level 2, stage 1
    reg  signed [9:0] n_t34_r1;
    wire signed [9:0] n_t35 = n_t26 + n_t28;   // level 2, stage 1
    reg  signed [9:0] n_t35_r1;
    wire signed [9:0] n_t36 = n_t26 - n_t28;   // level 2, stage 1
    reg  signed [9:0] n_t36_r1;
    wire signed [9:0] n_t37 = n_t29 + n_t31;   // level 2, stage 1
    reg  signed [9:0] n_t37_r1;
    wire signed [9:0] n_t38 = n_t29 - n_t31;   // level 2, stage 1
    reg  signed [9:0] n_t38_r1;
    wire signed [9:0] n_t39 = n_t30 + n_t32;   // level 2, stage 1
    reg  signed [9:0] n_t39_r1;
    wire signed [9:0] n_t40 = n_t30 - n_t32;   // level 2, stage 1
    reg  signed [9:0] n_t40_r1;
    wire signed [10:0] n_t41 = n_t33_r1 + n_t37_r1;   // level 3, stage 2
    wire signed [10:0] n_t42 = n_t33_r1 - n_t37_r1;   // level 3, stage 2
    wire signed [10:0] n_t43 = n_t35_r1 + n_t39_r1;   // level 3, stage 2
    wire signed [10:0] n_t44 = n_t35_r1 - n_t39_r1;   // level 3, stage 2
    wire signed [10:0] n_t45 = n_t34_r1 + n_t38_r1;   // level 3, stage 2
    wire signed [10:0] n_t46 = n_t34_r1 - n_t38_r1;   // level 3, stage 2
    wire signed [10:0] n_t47 = n_t36_r1 + n_t40_r1;   // level 3, stage 2
    wire signed [10:0] n_t48 = n_t36_r1 - n_t40_r1;   // level 3, stage 2
    wire signed [8:0] n_t49 = x16 + x17;   // level 1, stage 1
    wire signed [8:0] n_t50 = x16 - x17;   // level 1, stage 1
    wire signed [8:0] n_t51 = x18 + x19;   // level 1, stage 1
    wire signed [8:0] n_t52 = x18 - x19;   // level 1, stage 1
    wire signed [8:0] n_t53 = x20 + x21;   // level 1, stage 1
    wire signed [8:0] n_t54 = x20 - x21;   // level 1, stage 1
    wire signed [8:0] n_t55 = x22 + x23;   // level 1, stage 1
    wire signed [8:0] n_t56 = x22 - x23;   // level 1, stage 1
    wire signed [9:0] n_t57 = n_t49 + n_t51;   // level 2, stage 1
    reg  signed [9:0] n_t57_r1;
    wire signed [9:0] n_t58 = n_t49 - n_t51;   // level 2, stage 1
    reg  signed [9:0] n_t58_r1;
    wire signed [9:0] n_t59 = n_t50 + n_t52;   // level 2, stage 1
    reg  signed [9:0] n_t59_r1;
    wire signed [9:0] n_t60 = n_t50 - n_t52;   // level 2, stage 1
    reg  signed [9:0] n_t60_r1;
    wire signed [9:0] n_t61 = n_t53 + n_t55;   // level 2, stage 1
    reg  signed [9:0] n_t61_r1;
    wire signed [9:0] n_t62 = n_t53 - n_t55;   // level 2, stage 1
    reg  signed [9:0] n_t62_r1;
    wire signed [9:0] n_t63 = n_t54 + n_t56;   // level 2, stage 1
    reg  signed [9:0] n_t63_r1;
    wire signed [9:0] n_t64 = n_t54 - n_t56;   // level 2, stage 1
    reg  signed [9:0] n_t64_r1;
    wire signed [10:0] n_t65 = n_t57_r1 + n_t61_r1;   // level 3, stage 2
    wire signed [10:0] n_t66 = n_t57_r1 - n_t61_r1;   // level 3, stage 2
    wire signed [10:0] n_t67 = n_t59_r1 + n_t63_r1;   // level 3, stage 2
    wire signed [10:0] n_t68 = n_t59_r1 - n_t63_r1;   // level 3, stage 2
    wire signed [10:0] n_t69 = n_t58_r1 + n_t62_r1;   // level 3, stage 2
    wire signed [10:0] n_t70 = n_t58_r1 - n_t62_r1;   // level 3, stage 2
    wire signed [10:0] n_t71 = n_t60_r1 + n_t64_r1;   // level 3, stage 2
    wire signed [10:0] n_t72 = n_t60_r1 - n_t64_r1;   // level 3, stage 2
    wire signed [8:0] n_t73 = x24 + x25;   // level 1, stage 1
    wire signed [8:0] n_t74 = x24 - x25;   // level 1, stage 1
    wire signed [8:0] n_t75 = x26 + x27;   // level 1, stage 1
    wire signed [8:0] n_t76 = x26 - x27;   // level 1, stage 1
    wire signed [8:0] n_t77 = x28 + x29;   // level 1, stage 1
    wire signed [8:0] n_t78 = x28 - x29;   // level 1, stage 1
    wire signed [8:0] n_t79 = x30 + x31;   // level 1, stage 1
    wire signed [8:0] n_t80 = x30 - x31;   // level 1, stage 1
    wire signed [9:0] n_t81 = n_t73 + n_t75;   // level 2, stage 1
    reg  signed [9:0] n_t81_r1;
    wire signed [9:0] n_t82 = n_t73 - n_t75;   // level 2, stage 1
    reg  signed [9:0] n_t82_r1;
    wire signed [9:0] n_t83 = n_t74 + n_t76;   // level 2, stage 1
    reg  signed [9:0] n_t83_r1;
    wire signed [9:0] n_t84 = n_t74 - n_t76;   // level 2, stage 1
    reg  signed [9:0] n_t84_r1;
    wire signed [9:0] n_t85 = n_t77 + n_t79;   // level 2, stage 1
    reg  signed [9:0] n_t85_r1;
    wire signed [9:0] n_t86 = n_t77 - n_t79;   // level 2, stage 1
    reg  signed [9:0] n_t86_r1;
    wire signed [9:0] n_t87 = n_t78 + n_t80;   // level 2, stage 1
    reg  signed [9:0] n_t87_r1;
    wire signed [9:0] n_t88 = n_t78 - n_t80;   // level 2, stage 1
    reg  signed [9:0] n_t88_r1;
    wire signed [10:0] n_t89 = n_t81_r1 + n_t85_r1;   // level 3, stage 2
    wire signed [10:0] n_t90 = n_t81_r1 - n_t85_r1;   // level 3, stage 2
    wire signed [10:0] n_t91 = n_t83_r1 + n_t87_r1;   // level 3, stage 2
    wire signed [10:0] n_t92 = n_t83_r1 - n_t87_r1;   // level 3, stage 2
    wire signed [10:0] n_t93 = n_t82_r1 + n_t86_r1;   // level 3, stage 2
    wire signed [10:0] n_t94 = n_t82_r1 - n_t86_r1;   // level 3, stage 2
    wire signed [10:0] n_t95 = n_t84_r1 + n_t88_r1;   // level 3, stage 2
    wire signed [10:0] n_t96 = n_t84_r1 - n_t88_r1;   // level 3, stage 2
    wire signed [8:0] n_t97 = x32 + x33;   // level 1, stage 1
    wire signed [8:0] n_t98 = x32 - x33;   // level 1, stage 1
    wire signed [8:0] n_t99 = x34 + x35;   // level 1, stage 1
    wire signed [8:0] n_t100 = x34 - x35;   // level 1, stage 1
    wire signed [8:0] n_t101 = x36 + x37;   // level 1, stage 1
    wire signed [8:0] n_t102 = x36 - x37;   // level 1, stage 1
    wire signed [8:0] n_t103 = x38 + x39;   // level 1, stage 1
    wire signed [8:0] n_t104 = x38 - x39;   // level 1, stage 1
    wire signed [9:0] n_t105 = n_t97 + n_t99;   // level 2, stage 1
    reg  signed [9:0] n_t105_r1;
    wire signed [9:0] n_t106 = n_t97 - n_t99;   // level 2, stage 1
    reg  signed [9:0] n_t106_r1;
    wire signed [9:0] n_t107 = n_t98 + n_t100;   // level 2, stage 1
    reg  signed [9:0] n_t107_r1;
    wire signed [9:0] n_t108 = n_t98 - n_t100;   // level 2, stage 1
    reg  signed [9:0] n_t108_r1;
    wire signed [9:0] n_t109 = n_t101 + n_t103;   // level 2, stage 1
    reg  signed [9:0] n_t109_r1;
    wire signed [9:0] n_t110 = n_t101 - n_t103;   // level 2, stage 1
    reg  signed [9:0] n_t110_r1;
    wire signed [9:0] n_t111 = n_t102 + n_t104;   // level 2, stage 1
    reg  signed [9:0] n_t111_r1;
    wire signed [9:0] n_t112 = n_t102 - n_t104;   // level 2, stage 1
    reg  signed [9:0] n_t112_r1;
    wire signed [10:0] n_t113 = n_t105_r1 + n_t109_r1;   // level 3, stage 2
    wire signed [10:0] n_t114 = n_t105_r1 - n_t109_r1;   // level 3, stage 2
    wire signed [10:0] n_t115 = n_t107_r1 + n_t111_r1;   // level 3, stage 2
    wire signed [10:0] n_t116 = n_t107_r1 - n_t111_r1;   // level 3, stage 2
    wire signed [10:0] n_t117 = n_t106_r1 + n_t110_r1;   // level 3, stage 2
    wire signed [10:0] n_t118 = n_t106_r1 - n_t110_r1;   // level 3, stage 2
    wire signed [10:0] n_t119 = n_t108_r1 + n_t112_r1;   // level 3, stage 2
    wire signed [10:0] n_t120 = n_t108_r1 - n_t112_r1;   // level 3, stage 2
    wire signed [8:0] n_t121 = x40 + x41;   // level 1, stage 1
    wire signed [8:0] n_t122 = x40 - x41;   // level 1, stage 1
    wire signed [8:0] n_t123 = x42 + x43;   // level 1, stage 1
    wire signed [8:0] n_t124 = x42 - x43;   // level 1, stage 1
    wire signed [8:0] n_t125 = x44 + x45;   // level 1, stage 1
    wire signed [8:0] n_t126 = x44 - x45;   // level 1, stage 1
    wire signed [8:0] n_t127 = x46 + x47;   // level 1, stage 1
    wire signed [8:0] n_t128 = x46 - x47;   // level 1, stage 1
    wire signed [9:0] n_t129 = n_t121 + n_t123;   // level 2, stage 1
    reg  signed [9:0] n_t129_r1;
    wire signed [9:0] n_t130 = n_t121 - n_t123;   // level 2, stage 1
    reg  signed [9:0] n_t130_r1;
    wire signed [9:0] n_t131 = n_t122 + n_t124;   // level 2, stage 1
    reg  signed [9:0] n_t131_r1;
    wire signed [9:0] n_t132 = n_t122 - n_t124;   // level 2, stage 1
    reg  signed [9:0] n_t132_r1;
    wire signed [9:0] n_t133 = n_t125 + n_t127;   // level 2, stage 1
    reg  signed [9:0] n_t133_r1;
    wire signed [9:0] n_t134 = n_t125 - n_t127;   // level 2, stage 1
    reg  signed [9:0] n_t134_r1;
    wire signed [9:0] n_t135 = n_t126 + n_t128;   // level 2, stage 1
    reg  signed [9:0] n_t135_r1;
    wire signed [9:0] n_t136 = n_t126 - n_t128;   // level 2, stage 1
    reg  signed [9:0] n_t136_r1;
    wire signed [10:0] n_t137 = n_t129_r1 + n_t133_r1;   // level 3, stage 2
    wire signed [10:0] n_t138 = n_t129_r1 - n_t133_r1;   // level 3, stage 2
    wire signed [10:0] n_t139 = n_t131_r1 + n_t135_r1;   // level 3, stage 2
    wire signed [10:0] n_t140 = n_t131_r1 - n_t135_r1;   // level 3, stage 2
    wire signed [10:0] n_t141 = n_t130_r1 + n_t134_r1;   // level 3, stage 2
    wire signed [10:0] n_t142 = n_t130_r1 - n_t134_r1;   // level 3, stage 2
    wire signed [10:0] n_t143 = n_t132_r1 + n_t136_r1;   // level 3, stage 2
    wire signed [10:0] n_t144 = n_t132_r1 - n_t136_r1;   // level 3, stage 2
    wire signed [8:0] n_t145 = x48 + x49;   // level 1, stage 1
    wire signed [8:0] n_t146 = x48 - x49;   // level 1, stage 1
    wire signed [8:0] n_t147 = x50 + x51;   // level 1, stage 1
    wire signed [8:0] n_t148 = x50 - x51;   // level 1, stage 1
    wire signed [8:0] n_t149 = x52 + x53;   // level 1, stage 1
    wire signed [8:0] n_t150 = x52 - x53;   // level 1, stage 1
    wire signed [8:0] n_t151 = x54 + x55;   // level 1, stage 1
    wire signed [8:0] n_t152 = x54 - x55;   // level 1, stage 1
    wire signed [9:0] n_t153 = n_t145 + n_t147;   // level 2, stage 1
    reg  signed [9:0] n_t153_r1;
    wire signed [9:0] n_t154 = n_t145 - n_t147;   // level 2, stage 1
    reg  signed [9:0] n_t154_r1;
    wire signed [9:0] n_t155 = n_t146 + n_t148;   // level 2, stage 1
    reg  signed [9:0] n_t155_r1;
    wire signed [9:0] n_t156 = n_t146 - n_t148;   // level 2, stage 1
    reg  signed [9:0] n_t156_r1;
    wire signed [9:0] n_t157 = n_t149 + n_t151;   // level 2, stage 1
    reg  signed [9:0] n_t157_r1;
    wire signed [9:0] n_t158 = n_t149 - n_t151;   // level 2, stage 1
    reg  signed [9:0] n_t158_r1;
    wire signed [9:0] n_t159 = n_t150 + n_t152;   // level 2, stage 1
    reg  signed [9:0] n_t159_r1;
    wire signed [9:0] n_t160 = n_t150 - n_t152;   // level 2, stage 1
    reg  signed [9:0] n_t160_r1;
    wire signed [10:0] n_t161 = n_t153_r1 + n_t157_r1;   // level 3, stage 2
    wire signed [10:0] n_t162 = n_t153_r1 - n_t157_r1;   // level 3, stage 2
    wire signed [10:0] n_t163 = n_t155_r1 + n_t159_r1;   // level 3, stage 2
    wire signed [10:0] n_t164 = n_t155_r1 - n_t159_r1;   // level 3, stage 2
    wire signed [10:0] n_t165 = n_t154_r1 + n_t158_r1;   // level 3, stage 2
    wire signed [10:0] n_t166 = n_t154_r1 - n_t158_r1;   // level 3, stage 2
    wire signed [10:0] n_t167 = n_t156_r1 + n_t160_r1;   // level 3, stage 2
    wire signed [10:0] n_t168 = n_t156_r1 - n_t160_r1;   // level 3, stage 2
    wire signed [8:0] n_t169 = x56 + x57;   // level 1, stage 1
    wire signed [8:0] n_t170 = x56 - x57;   // level 1, stage 1
    wire signed [8:0] n_t171 = x58 + x59;   // level 1, stage 1
    wire signed [8:0] n_t172 = x58 - x59;   // level 1, stage 1
    wire signed [8:0] n_t173 = x60 + x61;   // level 1, stage 1
    wire signed [8:0] n_t174 = x60 - x61;   // level 1, stage 1
    wire signed [8:0] n_t175 = x62 + x63;   // level 1, stage 1
    wire signed [8:0] n_t176 = x62 - x63;   // level 1, stage 1
    wire signed [9:0] n_t177 = n_t169 + n_t171;   // level 2, stage 1
    reg  signed [9:0] n_t177_r1;
    wire signed [9:0] n_t178 = n_t169 - n_t171;   // level 2, stage 1
    reg  signed [9:0] n_t178_r1;
    wire signed [9:0] n_t179 = n_t170 + n_t172;   // level 2, stage 1
    reg  signed [9:0] n_t179_r1;
    wire signed [9:0] n_t180 = n_t170 - n_t172;   // level 2, stage 1
    reg  signed [9:0] n_t180_r1;
    wire signed [9:0] n_t181 = n_t173 + n_t175;   // level 2, stage 1
    reg  signed [9:0] n_t181_r1;
    wire signed [9:0] n_t182 = n_t173 - n_t175;   // level 2, stage 1
    reg  signed [9:0] n_t182_r1;
    wire signed [9:0] n_t183 = n_t174 + n_t176;   // level 2, stage 1
    reg  signed [9:0] n_t183_r1;
    wire signed [9:0] n_t184 = n_t174 - n_t176;   // level 2, stage 1
    reg  signed [9:0] n_t184_r1;
    wire signed [10:0] n_t185 = n_t177_r1 + n_t181_r1;   // level 3, stage 2
    wire signed [10:0] n_t186 = n_t177_r1 - n_t181_r1;   // level 3, stage 2
    wire signed [10:0] n_t187 = n_t179_r1 + n_t183_r1;   // level 3, stage 2
    wire signed [10:0] n_t188 = n_t179_r1 - n_t183_r1;   // level 3, stage 2
    wire signed [10:0] n_t189 = n_t178_r1 + n_t182_r1;   // level 3, stage 2
    wire signed [10:0] n_t190 = n_t178_r1 - n_t182_r1;   // level 3, stage 2
    wire signed [10:0] n_t191 = n_t180_r1 + n_t184_r1;   // level 3, stage 2
    wire signed [10:0] n_t192 = n_t180_r1 - n_t184_r1;   // level 3, stage 2
    wire signed [11:0] n_t193 = n_t17 + n_t41;   // level 4, stage 2
    reg  signed [11:0] n_t193_r2;
    wire signed [11:0] n_t194 = n_t17 - n_t41;   // level 4, stage 2
    reg  signed [11:0] n_t194_r2;
    wire signed [11:0] n_t195 = n_t65 + n_t89;   // level 4, stage 2
    reg  signed [11:0] n_t195_r2;
    wire signed [11:0] n_t196 = n_t65 - n_t89;   // level 4, stage 2
    reg  signed [11:0] n_t196_r2;
    wire signed [11:0] n_t197 = n_t113 + n_t137;   // level 4, stage 2
    reg  signed [11:0] n_t197_r2;
    wire signed [11:0] n_t198 = n_t113 - n_t137;   // level 4, stage 2
    reg  signed [11:0] n_t198_r2;
    wire signed [11:0] n_t199 = n_t161 + n_t185;   // level 4, stage 2
    reg  signed [11:0] n_t199_r2;
    wire signed [11:0] n_t200 = n_t161 - n_t185;   // level 4, stage 2
    reg  signed [11:0] n_t200_r2;
    wire signed [12:0] n_t201 = n_t193_r2 + n_t195_r2;   // level 5, stage 3
    wire signed [12:0] n_t202 = n_t193_r2 - n_t195_r2;   // level 5, stage 3
    wire signed [12:0] n_t203 = n_t194_r2 + n_t196_r2;   // level 5, stage 3
    wire signed [12:0] n_t204 = n_t194_r2 - n_t196_r2;   // level 5, stage 3
    wire signed [12:0] n_t205 = n_t197_r2 + n_t199_r2;   // level 5, stage 3
    wire signed [12:0] n_t206 = n_t197_r2 - n_t199_r2;   // level 5, stage 3
    wire signed [12:0] n_t207 = n_t198_r2 + n_t200_r2;   // level 5, stage 3
    wire signed [12:0] n_t208 = n_t198_r2 - n_t200_r2;   // level 5, stage 3
    wire signed [13:0] n_t209 = n_t201 + n_t205;   // level 6, stage 3
    reg  signed [13:0] n_t209_r3;
    wire signed [13:0] n_t210 = n_t201 - n_t205;   // level 6, stage 3
    reg  signed [13:0] n_t210_r3;
    wire signed [13:0] n_t211 = n_t203 + n_t207;   // level 6, stage 3
    reg  signed [13:0] n_t211_r3;
    wire signed [13:0] n_t212 = n_t203 - n_t207;   // level 6, stage 3
    reg  signed [13:0] n_t212_r3;
    wire signed [13:0] n_t213 = n_t202 + n_t206;   // level 6, stage 3
    reg  signed [13:0] n_t213_r3;
    wire signed [13:0] n_t214 = n_t202 - n_t206;   // level 6, stage 3
    reg  signed [13:0] n_t214_r3;
    wire signed [13:0] n_t215 = n_t204 + n_t208;   // level 6, stage 3
    reg  signed [13:0] n_t215_r3;
    wire signed [13:0] n_t216 = n_t204 - n_t208;   // level 6, stage 3
    reg  signed [13:0] n_t216_r3;
    wire signed [11:0] n_t217 = n_t19 + n_t43;   // level 4, stage 2
    reg  signed [11:0] n_t217_r2;
    wire signed [11:0] n_t218 = n_t19 - n_t43;   // level 4, stage 2
    reg  signed [11:0] n_t218_r2;
    wire signed [11:0] n_t219 = n_t67 + n_t91;   // level 4, stage 2
    reg  signed [11:0] n_t219_r2;
    wire signed [11:0] n_t220 = n_t67 - n_t91;   // level 4, stage 2
    reg  signed [11:0] n_t220_r2;
    wire signed [11:0] n_t221 = n_t115 + n_t139;   // level 4, stage 2
    reg  signed [11:0] n_t221_r2;
    wire signed [11:0] n_t222 = n_t115 - n_t139;   // level 4, stage 2
    reg  signed [11:0] n_t222_r2;
    wire signed [11:0] n_t223 = n_t163 + n_t187;   // level 4, stage 2
    reg  signed [11:0] n_t223_r2;
    wire signed [11:0] n_t224 = n_t163 - n_t187;   // level 4, stage 2
    reg  signed [11:0] n_t224_r2;
    wire signed [12:0] n_t225 = n_t217_r2 + n_t219_r2;   // level 5, stage 3
    wire signed [12:0] n_t226 = n_t217_r2 - n_t219_r2;   // level 5, stage 3
    wire signed [12:0] n_t227 = n_t218_r2 + n_t220_r2;   // level 5, stage 3
    wire signed [12:0] n_t228 = n_t218_r2 - n_t220_r2;   // level 5, stage 3
    wire signed [12:0] n_t229 = n_t221_r2 + n_t223_r2;   // level 5, stage 3
    wire signed [12:0] n_t230 = n_t221_r2 - n_t223_r2;   // level 5, stage 3
    wire signed [12:0] n_t231 = n_t222_r2 + n_t224_r2;   // level 5, stage 3
    wire signed [12:0] n_t232 = n_t222_r2 - n_t224_r2;   // level 5, stage 3
    wire signed [13:0] n_t233 = n_t225 + n_t229;   // level 6, stage 3
    reg  signed [13:0] n_t233_r3;
    wire signed [13:0] n_t234 = n_t225 - n_t229;   // level 6, stage 3
    reg  signed [13:0] n_t234_r3;
    wire signed [13:0] n_t235 = n_t227 + n_t231;   // level 6, stage 3
    reg  signed [13:0] n_t235_r3;
    wire signed [13:0] n_t236 = n_t227 - n_t231;   // level 6, stage 3
    reg  signed [13:0] n_t236_r3;
    wire signed [13:0] n_t237 = n_t226 + n_t230;   // level 6, stage 3
    reg  signed [13:0] n_t237_r3;
    wire signed [13:0] n_t238 = n_t226 - n_t230;   // level 6, stage 3
    reg  signed [13:0] n_t238_r3;
    wire signed [13:0] n_t239 = n_t228 + n_t232;   // level 6, stage 3
    reg  signed [13:0] n_t239_r3;
    wire signed [13:0] n_t240 = n_t228 - n_t232;   // level 6, stage 3
    reg  signed [13:0] n_t240_r3;
    wire signed [11:0] n_t241 = n_t21 + n_t45;   // level 4, stage 2
    reg  signed [11:0] n_t241_r2;
    wire signed [11:0] n_t242 = n_t21 - n_t45;   // level 4, stage 2
    reg  signed [11:0] n_t242_r2;
    wire signed [11:0] n_t243 = n_t69 + n_t93;   // level 4, stage 2
    reg  signed [11:0] n_t243_r2;
    wire signed [11:0] n_t244 = n_t69 - n_t93;   // level 4, stage 2
    reg  signed [11:0] n_t244_r2;
    wire signed [11:0] n_t245 = n_t117 + n_t141;   // level 4, stage 2
    reg  signed [11:0] n_t245_r2;
    wire signed [11:0] n_t246 = n_t117 - n_t141;   // level 4, stage 2
    reg  signed [11:0] n_t246_r2;
    wire signed [11:0] n_t247 = n_t165 + n_t189;   // level 4, stage 2
    reg  signed [11:0] n_t247_r2;
    wire signed [11:0] n_t248 = n_t165 - n_t189;   // level 4, stage 2
    reg  signed [11:0] n_t248_r2;
    wire signed [12:0] n_t249 = n_t241_r2 + n_t243_r2;   // level 5, stage 3
    wire signed [12:0] n_t250 = n_t241_r2 - n_t243_r2;   // level 5, stage 3
    wire signed [12:0] n_t251 = n_t242_r2 + n_t244_r2;   // level 5, stage 3
    wire signed [12:0] n_t252 = n_t242_r2 - n_t244_r2;   // level 5, stage 3
    wire signed [12:0] n_t253 = n_t245_r2 + n_t247_r2;   // level 5, stage 3
    wire signed [12:0] n_t254 = n_t245_r2 - n_t247_r2;   // level 5, stage 3
    wire signed [12:0] n_t255 = n_t246_r2 + n_t248_r2;   // level 5, stage 3
    wire signed [12:0] n_t256 = n_t246_r2 - n_t248_r2;   // level 5, stage 3
    wire signed [13:0] n_t257 = n_t249 + n_t253;   // level 6, stage 3
    reg  signed [13:0] n_t257_r3;
    wire signed [13:0] n_t258 = n_t249 - n_t253;   // level 6, stage 3
    reg  signed [13:0] n_t258_r3;
    wire signed [13:0] n_t259 = n_t251 + n_t255;   // level 6, stage 3
    reg  signed [13:0] n_t259_r3;
    wire signed [13:0] n_t260 = n_t251 - n_t255;   // level 6, stage 3
    reg  signed [13:0] n_t260_r3;
    wire signed [13:0] n_t261 = n_t250 + n_t254;   // level 6, stage 3
    reg  signed [13:0] n_t261_r3;
    wire signed [13:0] n_t262 = n_t250 - n_t254;   // level 6, stage 3
    reg  signed [13:0] n_t262_r3;
    wire signed [13:0] n_t263 = n_t252 + n_t256;   // level 6, stage 3
    reg  signed [13:0] n_t263_r3;
    wire signed [13:0] n_t264 = n_t252 - n_t256;   // level 6, stage 3
    reg  signed [13:0] n_t264_r3;
    wire signed [11:0] n_t265 = n_t23 + n_t47;   // level 4, stage 2
    reg  signed [11:0] n_t265_r2;
    wire signed [11:0] n_t266 = n_t23 - n_t47;   // level 4, stage 2
    reg  signed [11:0] n_t266_r2;
    wire signed [11:0] n_t267 = n_t71 + n_t95;   // level 4, stage 2
    reg  signed [11:0] n_t267_r2;
    wire signed [11:0] n_t268 = n_t71 - n_t95;   // level 4, stage 2
    reg  signed [11:0] n_t268_r2;
    wire signed [11:0] n_t269 = n_t119 + n_t143;   // level 4, stage 2
    reg  signed [11:0] n_t269_r2;
    wire signed [11:0] n_t270 = n_t119 - n_t143;   // level 4, stage 2
    reg  signed [11:0] n_t270_r2;
    wire signed [11:0] n_t271 = n_t167 + n_t191;   // level 4, stage 2
    reg  signed [11:0] n_t271_r2;
    wire signed [11:0] n_t272 = n_t167 - n_t191;   // level 4, stage 2
    reg  signed [11:0] n_t272_r2;
    wire signed [12:0] n_t273 = n_t265_r2 + n_t267_r2;   // level 5, stage 3
    wire signed [12:0] n_t274 = n_t265_r2 - n_t267_r2;   // level 5, stage 3
    wire signed [12:0] n_t275 = n_t266_r2 + n_t268_r2;   // level 5, stage 3
    wire signed [12:0] n_t276 = n_t266_r2 - n_t268_r2;   // level 5, stage 3
    wire signed [12:0] n_t277 = n_t269_r2 + n_t271_r2;   // level 5, stage 3
    wire signed [12:0] n_t278 = n_t269_r2 - n_t271_r2;   // level 5, stage 3
    wire signed [12:0] n_t279 = n_t270_r2 + n_t272_r2;   // level 5, stage 3
    wire signed [12:0] n_t280 = n_t270_r2 - n_t272_r2;   // level 5, stage 3
    wire signed [13:0] n_t281 = n_t273 + n_t277;   // level 6, stage 3
    reg  signed [13:0] n_t281_r3;
    wire signed [13:0] n_t282 = n_t273 - n_t277;   // level 6, stage 3
    reg  signed [13:0] n_t282_r3;
    wire signed [13:0] n_t283 = n_t275 + n_t279;   // level 6, stage 3
    reg  signed [13:0] n_t283_r3;
    wire signed [13:0] n_t284 = n_t275 - n_t279;   // level 6, stage 3
    reg  signed [13:0] n_t284_r3;
    wire signed [13:0] n_t285 = n_t274 + n_t278;   // level 6, stage 3
    reg  signed [13:0] n_t285_r3;
    wire signed [13:0] n_t286 = n_t274 - n_t278;   // level 6, stage 3
    reg  signed [13:0] n_t286_r3;
    wire signed [13:0] n_t287 = n_t276 + n_t280;   // level 6, stage 3
    reg  signed [13:0] n_t287_r3;
    wire signed [13:0] n_t288 = n_t276 - n_t280;   // level 6, stage 3
    reg  signed [13:0] n_t288_r3;
    wire signed [11:0] n_t289 = n_t18 + n_t42;   // level 4, stage 2
    reg  signed [11:0] n_t289_r2;
    wire signed [11:0] n_t290 = n_t18 - n_t42;   // level 4, stage 2
    reg  signed [11:0] n_t290_r2;
    wire signed [11:0] n_t291 = n_t66 + n_t90;   // level 4, stage 2
    reg  signed [11:0] n_t291_r2;
    wire signed [11:0] n_t292 = n_t66 - n_t90;   // level 4, stage 2
    reg  signed [11:0] n_t292_r2;
    wire signed [11:0] n_t293 = n_t114 + n_t138;   // level 4, stage 2
    reg  signed [11:0] n_t293_r2;
    wire signed [11:0] n_t294 = n_t114 - n_t138;   // level 4, stage 2
    reg  signed [11:0] n_t294_r2;
    wire signed [11:0] n_t295 = n_t162 + n_t186;   // level 4, stage 2
    reg  signed [11:0] n_t295_r2;
    wire signed [11:0] n_t296 = n_t162 - n_t186;   // level 4, stage 2
    reg  signed [11:0] n_t296_r2;
    wire signed [12:0] n_t297 = n_t289_r2 + n_t291_r2;   // level 5, stage 3
    wire signed [12:0] n_t298 = n_t289_r2 - n_t291_r2;   // level 5, stage 3
    wire signed [12:0] n_t299 = n_t290_r2 + n_t292_r2;   // level 5, stage 3
    wire signed [12:0] n_t300 = n_t290_r2 - n_t292_r2;   // level 5, stage 3
    wire signed [12:0] n_t301 = n_t293_r2 + n_t295_r2;   // level 5, stage 3
    wire signed [12:0] n_t302 = n_t293_r2 - n_t295_r2;   // level 5, stage 3
    wire signed [12:0] n_t303 = n_t294_r2 + n_t296_r2;   // level 5, stage 3
    wire signed [12:0] n_t304 = n_t294_r2 - n_t296_r2;   // level 5, stage 3
    wire signed [13:0] n_t305 = n_t297 + n_t301;   // level 6, stage 3
    reg  signed [13:0] n_t305_r3;
    wire signed [13:0] n_t306 = n_t297 - n_t301;   // level 6, stage 3
    reg  signed [13:0] n_t306_r3;
    wire signed [13:0] n_t307 = n_t299 + n_t303;   // level 6, stage 3
    reg  signed [13:0] n_t307_r3;
    wire signed [13:0] n_t308 = n_t299 - n_t303;   // level 6, stage 3
    reg  signed [13:0] n_t308_r3;
    wire signed [13:0] n_t309 = n_t298 + n_t302;   // level 6, stage 3
    reg  signed [13:0] n_t309_r3;
    wire signed [13:0] n_t310 = n_t298 - n_t302;   // level 6, stage 3
    reg  signed [13:0] n_t310_r3;
    wire signed [13:0] n_t311 = n_t300 + n_t304;   // level 6, stage 3
    reg  signed [13:0] n_t311_r3;
    wire signed [13:0] n_t312 = n_t300 - n_t304;   // level 6, stage 3
    reg  signed [13:0] n_t312_r3;
    wire signed [11:0] n_t313 = n_t20 + n_t44;   // level 4, stage 2
    reg  signed [11:0] n_t313_r2;
    wire signed [11:0] n_t314 = n_t20 - n_t44;   // level 4, stage 2
    reg  signed [11:0] n_t314_r2;
    wire signed [11:0] n_t315 = n_t68 + n_t92;   // level 4, stage 2
    reg  signed [11:0] n_t315_r2;
    wire signed [11:0] n_t316 = n_t68 - n_t92;   // level 4, stage 2
    reg  signed [11:0] n_t316_r2;
    wire signed [11:0] n_t317 = n_t116 + n_t140;   // level 4, stage 2
    reg  signed [11:0] n_t317_r2;
    wire signed [11:0] n_t318 = n_t116 - n_t140;   // level 4, stage 2
    reg  signed [11:0] n_t318_r2;
    wire signed [11:0] n_t319 = n_t164 + n_t188;   // level 4, stage 2
    reg  signed [11:0] n_t319_r2;
    wire signed [11:0] n_t320 = n_t164 - n_t188;   // level 4, stage 2
    reg  signed [11:0] n_t320_r2;
    wire signed [12:0] n_t321 = n_t313_r2 + n_t315_r2;   // level 5, stage 3
    wire signed [12:0] n_t322 = n_t313_r2 - n_t315_r2;   // level 5, stage 3
    wire signed [12:0] n_t323 = n_t314_r2 + n_t316_r2;   // level 5, stage 3
    wire signed [12:0] n_t324 = n_t314_r2 - n_t316_r2;   // level 5, stage 3
    wire signed [12:0] n_t325 = n_t317_r2 + n_t319_r2;   // level 5, stage 3
    wire signed [12:0] n_t326 = n_t317_r2 - n_t319_r2;   // level 5, stage 3
    wire signed [12:0] n_t327 = n_t318_r2 + n_t320_r2;   // level 5, stage 3
    wire signed [12:0] n_t328 = n_t318_r2 - n_t320_r2;   // level 5, stage 3
    wire signed [13:0] n_t329 = n_t321 + n_t325;   // level 6, stage 3
    reg  signed [13:0] n_t329_r3;
    wire signed [13:0] n_t330 = n_t321 - n_t325;   // level 6, stage 3
    reg  signed [13:0] n_t330_r3;
    wire signed [13:0] n_t331 = n_t323 + n_t327;   // level 6, stage 3
    reg  signed [13:0] n_t331_r3;
    wire signed [13:0] n_t332 = n_t323 - n_t327;   // level 6, stage 3
    reg  signed [13:0] n_t332_r3;
    wire signed [13:0] n_t333 = n_t322 + n_t326;   // level 6, stage 3
    reg  signed [13:0] n_t333_r3;
    wire signed [13:0] n_t334 = n_t322 - n_t326;   // level 6, stage 3
    reg  signed [13:0] n_t334_r3;
    wire signed [13:0] n_t335 = n_t324 + n_t328;   // level 6, stage 3
    reg  signed [13:0] n_t335_r3;
    wire signed [13:0] n_t336 = n_t324 - n_t328;   // level 6, stage 3
    reg  signed [13:0] n_t336_r3;
    wire signed [11:0] n_t337 = n_t22 + n_t46;   // level 4, stage 2
    reg  signed [11:0] n_t337_r2;
    wire signed [11:0] n_t338 = n_t22 - n_t46;   // level 4, stage 2
    reg  signed [11:0] n_t338_r2;
    wire signed [11:0] n_t339 = n_t70 + n_t94;   // level 4, stage 2
    reg  signed [11:0] n_t339_r2;
    wire signed [11:0] n_t340 = n_t70 - n_t94;   // level 4, stage 2
    reg  signed [11:0] n_t340_r2;
    wire signed [11:0] n_t341 = n_t118 + n_t142;   // level 4, stage 2
    reg  signed [11:0] n_t341_r2;
    wire signed [11:0] n_t342 = n_t118 - n_t142;   // level 4, stage 2
    reg  signed [11:0] n_t342_r2;
    wire signed [11:0] n_t343 = n_t166 + n_t190;   // level 4, stage 2
    reg  signed [11:0] n_t343_r2;
    wire signed [11:0] n_t344 = n_t166 - n_t190;   // level 4, stage 2
    reg  signed [11:0] n_t344_r2;
    wire signed [12:0] n_t345 = n_t337_r2 + n_t339_r2;   // level 5, stage 3
    wire signed [12:0] n_t346 = n_t337_r2 - n_t339_r2;   // level 5, stage 3
    wire signed [12:0] n_t347 = n_t338_r2 + n_t340_r2;   // level 5, stage 3
    wire signed [12:0] n_t348 = n_t338_r2 - n_t340_r2;   // level 5, stage 3
    wire signed [12:0] n_t349 = n_t341_r2 + n_t343_r2;   // level 5, stage 3
    wire signed [12:0] n_t350 = n_t341_r2 - n_t343_r2;   // level 5, stage 3
    wire signed [12:0] n_t351 = n_t342_r2 + n_t344_r2;   // level 5, stage 3
    wire signed [12:0] n_t352 = n_t342_r2 - n_t344_r2;   // level 5, stage 3
    wire signed [13:0] n_t353 = n_t345 + n_t349;   // level 6, stage 3
    reg  signed [13:0] n_t353_r3;
    wire signed [13:0] n_t354 = n_t345 - n_t349;   // level 6, stage 3
    reg  signed [13:0] n_t354_r3;
    wire signed [13:0] n_t355 = n_t347 + n_t351;   // level 6, stage 3
    reg  signed [13:0] n_t355_r3;
    wire signed [13:0] n_t356 = n_t347 - n_t351;   // level 6, stage 3
    reg  signed [13:0] n_t356_r3;
    wire signed [13:0] n_t357 = n_t346 + n_t350;   // level 6, stage 3
    reg  signed [13:0] n_t357_r3;
    wire signed [13:0] n_t358 = n_t346 - n_t350;   // level 6, stage 3
    reg  signed [13:0] n_t358_r3;
    wire signed [13:0] n_t359 = n_t348 + n_t352;   // level 6, stage 3
    reg  signed [13:0] n_t359_r3;
    wire signed [13:0] n_t360 = n_t348 - n_t352;   // level 6, stage 3
    reg  signed [13:0] n_t360_r3;
    wire signed [11:0] n_t361 = n_t24 + n_t48;   // level 4, stage 2
    reg  signed [11:0] n_t361_r2;
    wire signed [11:0] n_t362 = n_t24 - n_t48;   // level 4, stage 2
    reg  signed [11:0] n_t362_r2;
    wire signed [11:0] n_t363 = n_t72 + n_t96;   // level 4, stage 2
    reg  signed [11:0] n_t363_r2;
    wire signed [11:0] n_t364 = n_t72 - n_t96;   // level 4, stage 2
    reg  signed [11:0] n_t364_r2;
    wire signed [11:0] n_t365 = n_t120 + n_t144;   // level 4, stage 2
    reg  signed [11:0] n_t365_r2;
    wire signed [11:0] n_t366 = n_t120 - n_t144;   // level 4, stage 2
    reg  signed [11:0] n_t366_r2;
    wire signed [11:0] n_t367 = n_t168 + n_t192;   // level 4, stage 2
    reg  signed [11:0] n_t367_r2;
    wire signed [11:0] n_t368 = n_t168 - n_t192;   // level 4, stage 2
    reg  signed [11:0] n_t368_r2;
    wire signed [12:0] n_t369 = n_t361_r2 + n_t363_r2;   // level 5, stage 3
    wire signed [12:0] n_t370 = n_t361_r2 - n_t363_r2;   // level 5, stage 3
    wire signed [12:0] n_t371 = n_t362_r2 + n_t364_r2;   // level 5, stage 3
    wire signed [12:0] n_t372 = n_t362_r2 - n_t364_r2;   // level 5, stage 3
    wire signed [12:0] n_t373 = n_t365_r2 + n_t367_r2;   // level 5, stage 3
    wire signed [12:0] n_t374 = n_t365_r2 - n_t367_r2;   // level 5, stage 3
    wire signed [12:0] n_t375 = n_t366_r2 + n_t368_r2;   // level 5, stage 3
    wire signed [12:0] n_t376 = n_t366_r2 - n_t368_r2;   // level 5, stage 3
    wire signed [13:0] n_t377 = n_t369 + n_t373;   // level 6, stage 3
    reg  signed [13:0] n_t377_r3;
    wire signed [13:0] n_t378 = n_t369 - n_t373;   // level 6, stage 3
    reg  signed [13:0] n_t378_r3;
    wire signed [13:0] n_t379 = n_t371 + n_t375;   // level 6, stage 3
    reg  signed [13:0] n_t379_r3;
    wire signed [13:0] n_t380 = n_t371 - n_t375;   // level 6, stage 3
    reg  signed [13:0] n_t380_r3;
    wire signed [13:0] n_t381 = n_t370 + n_t374;   // level 6, stage 3
    reg  signed [13:0] n_t381_r3;
    wire signed [13:0] n_t382 = n_t370 - n_t374;   // level 6, stage 3
    reg  signed [13:0] n_t382_r3;
    wire signed [13:0] n_t383 = n_t372 + n_t376;   // level 6, stage 3
    reg  signed [13:0] n_t383_r3;
    wire signed [13:0] n_t384 = n_t372 - n_t376;   // level 6, stage 3
    reg  signed [13:0] n_t384_r3;
    wire signed [13:0] o0 = n_t209_r3;
    wire signed [13:0] o1 = n_t233_r3;
    wire signed [13:0] o2 = n_t257_r3;
    wire signed [13:0] o3 = n_t281_r3;
    wire signed [13:0] o4 = n_t305_r3;
    wire signed [13:0] o5 = n_t329_r3;
    wire signed [13:0] o6 = n_t353_r3;
    wire signed [13:0] o7 = n_t377_r3;
    wire signed [13:0] o8 = n_t211_r3;
    wire signed [13:0] o9 = n_t235_r3;
    wire signed [13:0] o10 = n_t259_r3;
    wire signed [13:0] o11 = n_t283_r3;
    wire signed [13:0] o12 = n_t307_r3;
    wire signed [13:0] o13 = n_t331_r3;
    wire signed [13:0] o14 = n_t355_r3;
    wire signed [13:0] o15 = n_t379_r3;
    wire signed [13:0] o16 = n_t213_r3;
    wire signed [13:0] o17 = n_t237_r3;
    wire signed [13:0] o18 = n_t261_r3;
    wire signed [13:0] o19 = n_t285_r3;
    wire signed [13:0] o20 = n_t309_r3;
    wire signed [13:0] o21 = n_t333_r3;
    wire signed [13:0] o22 = n_t357_r3;
    wire signed [13:0] o23 = n_t381_r3;
    wire signed [13:0] o24 = n_t215_r3;
    wire signed [13:0] o25 = n_t239_r3;
    wire signed [13:0] o26 = n_t263_r3;
    wire signed [13:0] o27 = n_t287_r3;
    wire signed [13:0] o28 = n_t311_r3;
    wire signed [13:0] o29 = n_t335_r3;
    wire signed [13:0] o30 = n_t359_r3;
    wire signed [13:0] o31 = n_t383_r3;
    wire signed [13:0] o32 = n_t210_r3;
    wire signed [13:0] o33 = n_t234_r3;
    wire signed [13:0] o34 = n_t258_r3;
    wire signed [13:0] o35 = n_t282_r3;
    wire signed [13:0] o36 = n_t306_r3;
    wire signed [13:0] o37 = n_t330_r3;
    wire signed [13:0] o38 = n_t354_r3;
    wire signed [13:0] o39 = n_t378_r3;
    wire signed [13:0] o40 = n_t212_r3;
    wire signed [13:0] o41 = n_t236_r3;
    wire signed [13:0] o42 = n_t260_r3;
    wire signed [13:0] o43 = n_t284_r3;
    wire signed [13:0] o44 = n_t308_r3;
    wire signed [13:0] o45 = n_t332_r3;
    wire signed [13:0] o46 = n_t356_r3;
    wire signed [13:0] o47 = n_t380_r3;
    wire signed [13:0] o48 = n_t214_r3;
    wire signed [13:0] o49 = n_t238_r3;
    wire signed [13:0] o50 = n_t262_r3;
    wire signed [13:0] o51 = n_t286_r3;
    wire signed [13:0] o52 = n_t310_r3;
    wire signed [13:0] o53 = n_t334_r3;
    wire signed [13:0] o54 = n_t358_r3;
    wire signed [13:0] o55 = n_t382_r3;
    wire signed [13:0] o56 = n_t216_r3;
    wire signed [13:0] o57 = n_t240_r3;
    wire signed [13:0] o58 = n_t264_r3;
    wire signed [13:0] o59 = n_t288_r3;
    wire signed [13:0] o60 = n_t312_r3;
    wire signed [13:0] o61 = n_t336_r3;
    wire signed [13:0] o62 = n_t360_r3;
    wire signed [13:0] o63 = n_t384_r3;
    assign out_data = {
        o63, o62, o61, o60, o59, o58, o57, o56,
        o55, o54, o53, o52, o51, o50, o49, o48,
        o47, o46, o45, o44, o43, o42, o41, o40,
        o39, o38, o37, o36, o35, o34, o33, o32,
        o31, o30, o29, o28, o27, o26, o25, o24,
        o23, o22, o21, o20, o19, o18, o17, o16,
        o15, o14, o13, o12, o11, o10, o9, o8,
        o7, o6, o5, o4, o3, o2, o1, o0
    };
    reg  [2:0] vld = 3'd0;
    always @(posedge clk) begin
        n_t9_r1 <= n_t9;
        n_t10_r1 <= n_t10;
        n_t11_r1 <= n_t11;
        n_t12_r1 <= n_t12;
        n_t13_r1 <= n_t13;
        n_t14_r1 <= n_t14;
        n_t15_r1 <= n_t15;
        n_t16_r1 <= n_t16;
        n_t33_r1 <= n_t33;
        n_t34_r1 <= n_t34;
        n_t35_r1 <= n_t35;
        n_t36_r1 <= n_t36;
        n_t37_r1 <= n_t37;
        n_t38_r1 <= n_t38;
        n_t39_r1 <= n_t39;
        n_t40_r1 <= n_t40;
        n_t57_r1 <= n_t57;
        n_t58_r1 <= n_t58;
        n_t59_r1 <= n_t59;
        n_t60_r1 <= n_t60;
        n_t61_r1 <= n_t61;
        n_t62_r1 <= n_t62;
        n_t63_r1 <= n_t63;
        n_t64_r1 <= n_t64;
        n_t81_r1 <= n_t81;
        n_t82_r1 <= n_t82;
        n_t83_r1 <= n_t83;
        n_t84_r1 <= n_t84;
        n_t85_r1 <= n_t85;
        n_t86_r1 <= n_t86;
        n_t87_r1 <= n_t87;
        n_t88_r1 <= n_t88;
        n_t105_r1 <= n_t105;
        n_t106_r1 <= n_t106;
        n_t107_r1 <= n_t107;
        n_t108_r1 <= n_t108;
        n_t109_r1 <= n_t109;
        n_t110_r1 <= n_t110;
        n_t111_r1 <= n_t111;
        n_t112_r1 <= n_t112;
        n_t129_r1 <= n_t129;
        n_t130_r1 <= n_t130;
        n_t131_r1 <= n_t131;
        n_t132_r1 <= n_t132;
        n_t133_r1 <= n_t133;
        n_t134_r1 <= n_t134;
        n_t135_r1 <= n_t135;
        n_t136_r1 <= n_t136;
        n_t153_r1 <= n_t153;
        n_t154_r1 <= n_t154;
        n_t155_r1 <= n_t155;
        n_t156_r1 <= n_t156;
        n_t157_r1 <= n_t157;
        n_t158_r1 <= n_t158;
        n_t159_r1 <= n_t159;
        n_t160_r1 <= n_t160;
        n_t177_r1 <= n_t177;
        n_t178_r1 <= n_t178;
        n_t179_r1 <= n_t179;
        n_t180_r1 <= n_t180;
        n_t181_r1 <= n_t181;
        n_t182_r1 <= n_t182;
        n_t183_r1 <= n_t183;
        n_t184_r1 <= n_t184;
        n_t193_r2 <= n_t193;
        n_t194_r2 <= n_t194;
        n_t195_r2 <= n_t195;
        n_t196_r2 <= n_t196;
        n_t197_r2 <= n_t197;
        n_t198_r2 <= n_t198;
        n_t199_r2 <= n_t199;
        n_t200_r2 <= n_t200;
        n_t209_r3 <= n_t209;
        n_t210_r3 <= n_t210;
        n_t211_r3 <= n_t211;
        n_t212_r3 <= n_t212;
        n_t213_r3 <= n_t213;
        n_t214_r3 <= n_t214;
        n_t215_r3 <= n_t215;
        n_t216_r3 <= n_t216;
        n_t217_r2 <= n_t217;
        n_t218_r2 <= n_t218;
        n_t219_r2 <= n_t219;
        n_t220_r2 <= n_t220;
        n_t221_r2 <= n_t221;
        n_t222_r2 <= n_t222;
        n_t223_r2 <= n_t223;
        n_t224_r2 <= n_t224;
        n_t233_r3 <= n_t233;
        n_t234_r3 <= n_t234;
        n_t235_r3 <= n_t235;
        n_t236_r3 <= n_t236;
        n_t237_r3 <= n_t237;
        n_t238_r3 <= n_t238;
        n_t239_r3 <= n_t239;
        n_t240_r3 <= n_t240;
        n_t241_r2 <= n_t241;
        n_t242_r2 <= n_t242;
        n_t243_r2 <= n_t243;
        n_t244_r2 <= n_t244;
        n_t245_r2 <= n_t245;
        n_t246_r2 <= n_t246;
        n_t247_r2 <= n_t247;
        n_t248_r2 <= n_t248;
        n_t257_r3 <= n_t257;
        n_t258_r3 <= n_t258;
        n_t259_r3 <= n_t259;
        n_t260_r3 <= n_t260;
        n_t261_r3 <= n_t261;
        n_t262_r3 <= n_t262;
        n_t263_r3 <= n_t263;
        n_t264_r3 <= n_t264;
        n_t265_r2 <= n_t265;
        n_t266_r2 <= n_t266;
        n_t267_r2 <= n_t267;
        n_t268_r2 <= n_t268;
        n_t269_r2 <= n_t269;
        n_t270_r2 <= n_t270;
        n_t271_r2 <= n_t271;
        n_t272_r2 <= n_t272;
        n_t281_r3 <= n_t281;
        n_t282_r3 <= n_t282;
        n_t283_r3 <= n_t283;
        n_t284_r3 <= n_t284;
        n_t285_r3 <= n_t285;
        n_t286_r3 <= n_t286;
        n_t287_r3 <= n_t287;
        n_t288_r3 <= n_t288;
        n_t289_r2 <= n_t289;
        n_t290_r2 <= n_t290;
        n_t291_r2 <= n_t291;
        n_t292_r2 <= n_t292;
        n_t293_r2 <= n_t293;
        n_t294_r2 <= n_t294;
        n_t295_r2 <= n_t295;
        n_t296_r2 <= n_t296;
        n_t305_r3 <= n_t305;
        n_t306_r3 <= n_t306;
        n_t307_r3 <= n_t307;
        n_t308_r3 <= n_t308;
        n_t309_r3 <= n_t309;
        n_t310_r3 <= n_t310;
        n_t311_r3 <= n_t311;
        n_t312_r3 <= n_t312;
        n_t313_r2 <= n_t313;
        n_t314_r2 <= n_t314;
        n_t315_r2 <= n_t315;
        n_t316_r2 <= n_t316;
        n_t317_r2 <= n_t317;
        n_t318_r2 <= n_t318;
        n_t319_r2 <= n_t319;
        n_t320_r2 <= n_t320;
        n_t329_r3 <= n_t329;
        n_t330_r3 <= n_t330;
        n_t331_r3 <= n_t331;
        n_t332_r3 <= n_t332;
        n_t333_r3 <= n_t333;
        n_t334_r3 <= n_t334;
        n_t335_r3 <= n_t335;
        n_t336_r3 <= n_t336;
        n_t337_r2 <= n_t337;
        n_t338_r2 <= n_t338;
        n_t339_r2 <= n_t339;
        n_t340_r2 <= n_t340;
        n_t341_r2 <= n_t341;
        n_t342_r2 <= n_t342;
        n_t343_r2 <= n_t343;
        n_t344_r2 <= n_t344;
        n_t353_r3 <= n_t353;
        n_t354_r3 <= n_t354;
        n_t355_r3 <= n_t355;
        n_t356_r3 <= n_t356;
        n_t357_r3 <= n_t357;
        n_t358_r3 <= n_t358;
        n_t359_r3 <= n_t359;
        n_t360_r3 <= n_t360;
        n_t361_r2 <= n_t361;
        n_t362_r2 <= n_t362;
        n_t363_r2 <= n_t363;
        n_t364_r2 <= n_t364;
        n_t365_r2 <= n_t365;
        n_t366_r2 <= n_t366;
        n_t367_r2 <= n_t367;
        n_t368_r2 <= n_t368;
        n_t377_r3 <= n_t377;
        n_t378_r3 <= n_t378;
        n_t379_r3 <= n_t379;
        n_t380_r3 <= n_t380;
        n_t381_r3 <= n_t381;
        n_t382_r3 <= n_t382;
        n_t383_r3 <= n_t383;
        n_t384_r3 <= n_t384;
        vld <= {vld[1:0], in_valid};
    end
    assign out_valid = vld[2];
endmodule
`default_nettype wire
