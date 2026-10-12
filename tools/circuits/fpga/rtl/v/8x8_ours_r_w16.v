// Written by gen_rtl.py.  Do not edit by hand.
// 64-point Walsh-Hadamard transform, y_J = sum over i of (-1)^popcount(J & i) * x_i.
// Source circuit: tools/circuits/programs/generated/G_layers_64.txt
// 2-D 8 x 8: the 19-adder circuit on rows, then on columns (16 transforms, 304 adders).
// Inputs: 64 signed values of 16 bits.  Outputs: 64 signed values of 22 bits.
// Adders 304, depth 12 adder levels, adder bits 6072 (chain bits 5912).
// Variant r: one register stage at the inputs, 1 at the outputs, nothing between.  Latency 2.
// Register bits: 1024 at the inputs, 1408 at the outputs, 2 valid bits.
`default_nettype none
module wht_8x8_ours_r_w16 (
    input  wire                 clk,
    input  wire                 in_valid,
    input  wire [1023:0] in_data,
    output wire                 out_valid,
    output wire [1407:0] out_data
);
    reg  signed [15:0] x0;
    reg  signed [15:0] x1;
    reg  signed [15:0] x2;
    reg  signed [15:0] x3;
    reg  signed [15:0] x4;
    reg  signed [15:0] x5;
    reg  signed [15:0] x6;
    reg  signed [15:0] x7;
    reg  signed [15:0] x8;
    reg  signed [15:0] x9;
    reg  signed [15:0] x10;
    reg  signed [15:0] x11;
    reg  signed [15:0] x12;
    reg  signed [15:0] x13;
    reg  signed [15:0] x14;
    reg  signed [15:0] x15;
    reg  signed [15:0] x16;
    reg  signed [15:0] x17;
    reg  signed [15:0] x18;
    reg  signed [15:0] x19;
    reg  signed [15:0] x20;
    reg  signed [15:0] x21;
    reg  signed [15:0] x22;
    reg  signed [15:0] x23;
    reg  signed [15:0] x24;
    reg  signed [15:0] x25;
    reg  signed [15:0] x26;
    reg  signed [15:0] x27;
    reg  signed [15:0] x28;
    reg  signed [15:0] x29;
    reg  signed [15:0] x30;
    reg  signed [15:0] x31;
    reg  signed [15:0] x32;
    reg  signed [15:0] x33;
    reg  signed [15:0] x34;
    reg  signed [15:0] x35;
    reg  signed [15:0] x36;
    reg  signed [15:0] x37;
    reg  signed [15:0] x38;
    reg  signed [15:0] x39;
    reg  signed [15:0] x40;
    reg  signed [15:0] x41;
    reg  signed [15:0] x42;
    reg  signed [15:0] x43;
    reg  signed [15:0] x44;
    reg  signed [15:0] x45;
    reg  signed [15:0] x46;
    reg  signed [15:0] x47;
    reg  signed [15:0] x48;
    reg  signed [15:0] x49;
    reg  signed [15:0] x50;
    reg  signed [15:0] x51;
    reg  signed [15:0] x52;
    reg  signed [15:0] x53;
    reg  signed [15:0] x54;
    reg  signed [15:0] x55;
    reg  signed [15:0] x56;
    reg  signed [15:0] x57;
    reg  signed [15:0] x58;
    reg  signed [15:0] x59;
    reg  signed [15:0] x60;
    reg  signed [15:0] x61;
    reg  signed [15:0] x62;
    reg  signed [15:0] x63;
    always @(posedge clk) begin
        x0 <= in_data[15:0];
        x1 <= in_data[31:16];
        x2 <= in_data[47:32];
        x3 <= in_data[63:48];
        x4 <= in_data[79:64];
        x5 <= in_data[95:80];
        x6 <= in_data[111:96];
        x7 <= in_data[127:112];
        x8 <= in_data[143:128];
        x9 <= in_data[159:144];
        x10 <= in_data[175:160];
        x11 <= in_data[191:176];
        x12 <= in_data[207:192];
        x13 <= in_data[223:208];
        x14 <= in_data[239:224];
        x15 <= in_data[255:240];
        x16 <= in_data[271:256];
        x17 <= in_data[287:272];
        x18 <= in_data[303:288];
        x19 <= in_data[319:304];
        x20 <= in_data[335:320];
        x21 <= in_data[351:336];
        x22 <= in_data[367:352];
        x23 <= in_data[383:368];
        x24 <= in_data[399:384];
        x25 <= in_data[415:400];
        x26 <= in_data[431:416];
        x27 <= in_data[447:432];
        x28 <= in_data[463:448];
        x29 <= in_data[479:464];
        x30 <= in_data[495:480];
        x31 <= in_data[511:496];
        x32 <= in_data[527:512];
        x33 <= in_data[543:528];
        x34 <= in_data[559:544];
        x35 <= in_data[575:560];
        x36 <= in_data[591:576];
        x37 <= in_data[607:592];
        x38 <= in_data[623:608];
        x39 <= in_data[639:624];
        x40 <= in_data[655:640];
        x41 <= in_data[671:656];
        x42 <= in_data[687:672];
        x43 <= in_data[703:688];
        x44 <= in_data[719:704];
        x45 <= in_data[735:720];
        x46 <= in_data[751:736];
        x47 <= in_data[767:752];
        x48 <= in_data[783:768];
        x49 <= in_data[799:784];
        x50 <= in_data[815:800];
        x51 <= in_data[831:816];
        x52 <= in_data[847:832];
        x53 <= in_data[863:848];
        x54 <= in_data[879:864];
        x55 <= in_data[895:880];
        x56 <= in_data[911:896];
        x57 <= in_data[927:912];
        x58 <= in_data[943:928];
        x59 <= in_data[959:944];
        x60 <= in_data[975:960];
        x61 <= in_data[991:976];
        x62 <= in_data[1007:992];
        x63 <= in_data[1023:1008];
    end
    wire signed [16:0] n_t1 = x0 + x7;   // level 1
    wire signed [16:0] n_t2 = x1 + x6;   // level 1
    wire signed [16:0] n_t3 = x2 - x5;   // level 1
    wire signed [16:0] n_t4 = x3 - x4;   // level 1
    wire signed [17:0] n_t5 = n_t1 - n_t2;   // level 2
    wire signed [17:0] n_t6 = n_t3 + n_t4;   // level 2
    wire signed [18:0] n_t7 = n_t5 - n_t6;   // level 3
    wire signed [18:0] n_t8 = n_t7 - (x7 <<< 1);   // level 4
    wire signed [18:0] n_t9 = n_t7 - (x5 <<< 1);   // level 4
    wire signed [18:0] n_t10 = n_t8 + (x6 <<< 1);   // level 5
    wire signed [18:0] n_t11 = n_t9 - (x4 <<< 1);   // level 5
    wire signed [18:0] n_t12 = n_t10 + (n_t4 <<< 1);   // level 6
    wire signed [18:0] n_t13 = n_t9 + (x3 <<< 1);   // level 5
    wire signed [18:0] n_t14 = (n_t5 <<< 1) - n_t13;   // level 6
    wire signed [18:0] n_t15 = n_t10 + (n_t3 <<< 1);   // level 6
    wire signed [18:0] n_t16 = n_t11 + (n_t2 <<< 1);   // level 6
    wire signed [18:0] n_t17 = n_t8 + (x1 <<< 1);   // level 5
    wire signed [18:0] n_t18 = n_t17 + (n_t6 <<< 1);   // level 6
    wire signed [18:0] n_t19 = (n_t1 <<< 1) - n_t11;   // level 6
    wire signed [16:0] n_t20 = x8 + x15;   // level 1
    wire signed [16:0] n_t21 = x9 + x14;   // level 1
    wire signed [16:0] n_t22 = x10 - x13;   // level 1
    wire signed [16:0] n_t23 = x11 - x12;   // level 1
    wire signed [17:0] n_t24 = n_t20 - n_t21;   // level 2
    wire signed [17:0] n_t25 = n_t22 + n_t23;   // level 2
    wire signed [18:0] n_t26 = n_t24 - n_t25;   // level 3
    wire signed [18:0] n_t27 = n_t26 - (x15 <<< 1);   // level 4
    wire signed [18:0] n_t28 = n_t26 - (x13 <<< 1);   // level 4
    wire signed [18:0] n_t29 = n_t27 + (x14 <<< 1);   // level 5
    wire signed [18:0] n_t30 = n_t28 - (x12 <<< 1);   // level 5
    wire signed [18:0] n_t31 = n_t29 + (n_t23 <<< 1);   // level 6
    wire signed [18:0] n_t32 = n_t28 + (x11 <<< 1);   // level 5
    wire signed [18:0] n_t33 = (n_t24 <<< 1) - n_t32;   // level 6
    wire signed [18:0] n_t34 = n_t29 + (n_t22 <<< 1);   // level 6
    wire signed [18:0] n_t35 = n_t30 + (n_t21 <<< 1);   // level 6
    wire signed [18:0] n_t36 = n_t27 + (x9 <<< 1);   // level 5
    wire signed [18:0] n_t37 = n_t36 + (n_t25 <<< 1);   // level 6
    wire signed [18:0] n_t38 = (n_t20 <<< 1) - n_t30;   // level 6
    wire signed [16:0] n_t39 = x16 + x23;   // level 1
    wire signed [16:0] n_t40 = x17 + x22;   // level 1
    wire signed [16:0] n_t41 = x18 - x21;   // level 1
    wire signed [16:0] n_t42 = x19 - x20;   // level 1
    wire signed [17:0] n_t43 = n_t39 - n_t40;   // level 2
    wire signed [17:0] n_t44 = n_t41 + n_t42;   // level 2
    wire signed [18:0] n_t45 = n_t43 - n_t44;   // level 3
    wire signed [18:0] n_t46 = n_t45 - (x23 <<< 1);   // level 4
    wire signed [18:0] n_t47 = n_t45 - (x21 <<< 1);   // level 4
    wire signed [18:0] n_t48 = n_t46 + (x22 <<< 1);   // level 5
    wire signed [18:0] n_t49 = n_t47 - (x20 <<< 1);   // level 5
    wire signed [18:0] n_t50 = n_t48 + (n_t42 <<< 1);   // level 6
    wire signed [18:0] n_t51 = n_t47 + (x19 <<< 1);   // level 5
    wire signed [18:0] n_t52 = (n_t43 <<< 1) - n_t51;   // level 6
    wire signed [18:0] n_t53 = n_t48 + (n_t41 <<< 1);   // level 6
    wire signed [18:0] n_t54 = n_t49 + (n_t40 <<< 1);   // level 6
    wire signed [18:0] n_t55 = n_t46 + (x17 <<< 1);   // level 5
    wire signed [18:0] n_t56 = n_t55 + (n_t44 <<< 1);   // level 6
    wire signed [18:0] n_t57 = (n_t39 <<< 1) - n_t49;   // level 6
    wire signed [16:0] n_t58 = x24 + x31;   // level 1
    wire signed [16:0] n_t59 = x25 + x30;   // level 1
    wire signed [16:0] n_t60 = x26 - x29;   // level 1
    wire signed [16:0] n_t61 = x27 - x28;   // level 1
    wire signed [17:0] n_t62 = n_t58 - n_t59;   // level 2
    wire signed [17:0] n_t63 = n_t60 + n_t61;   // level 2
    wire signed [18:0] n_t64 = n_t62 - n_t63;   // level 3
    wire signed [18:0] n_t65 = n_t64 - (x31 <<< 1);   // level 4
    wire signed [18:0] n_t66 = n_t64 - (x29 <<< 1);   // level 4
    wire signed [18:0] n_t67 = n_t65 + (x30 <<< 1);   // level 5
    wire signed [18:0] n_t68 = n_t66 - (x28 <<< 1);   // level 5
    wire signed [18:0] n_t69 = n_t67 + (n_t61 <<< 1);   // level 6
    wire signed [18:0] n_t70 = n_t66 + (x27 <<< 1);   // level 5
    wire signed [18:0] n_t71 = (n_t62 <<< 1) - n_t70;   // level 6
    wire signed [18:0] n_t72 = n_t67 + (n_t60 <<< 1);   // level 6
    wire signed [18:0] n_t73 = n_t68 + (n_t59 <<< 1);   // level 6
    wire signed [18:0] n_t74 = n_t65 + (x25 <<< 1);   // level 5
    wire signed [18:0] n_t75 = n_t74 + (n_t63 <<< 1);   // level 6
    wire signed [18:0] n_t76 = (n_t58 <<< 1) - n_t68;   // level 6
    wire signed [16:0] n_t77 = x32 + x39;   // level 1
    wire signed [16:0] n_t78 = x33 + x38;   // level 1
    wire signed [16:0] n_t79 = x34 - x37;   // level 1
    wire signed [16:0] n_t80 = x35 - x36;   // level 1
    wire signed [17:0] n_t81 = n_t77 - n_t78;   // level 2
    wire signed [17:0] n_t82 = n_t79 + n_t80;   // level 2
    wire signed [18:0] n_t83 = n_t81 - n_t82;   // level 3
    wire signed [18:0] n_t84 = n_t83 - (x39 <<< 1);   // level 4
    wire signed [18:0] n_t85 = n_t83 - (x37 <<< 1);   // level 4
    wire signed [18:0] n_t86 = n_t84 + (x38 <<< 1);   // level 5
    wire signed [18:0] n_t87 = n_t85 - (x36 <<< 1);   // level 5
    wire signed [18:0] n_t88 = n_t86 + (n_t80 <<< 1);   // level 6
    wire signed [18:0] n_t89 = n_t85 + (x35 <<< 1);   // level 5
    wire signed [18:0] n_t90 = (n_t81 <<< 1) - n_t89;   // level 6
    wire signed [18:0] n_t91 = n_t86 + (n_t79 <<< 1);   // level 6
    wire signed [18:0] n_t92 = n_t87 + (n_t78 <<< 1);   // level 6
    wire signed [18:0] n_t93 = n_t84 + (x33 <<< 1);   // level 5
    wire signed [18:0] n_t94 = n_t93 + (n_t82 <<< 1);   // level 6
    wire signed [18:0] n_t95 = (n_t77 <<< 1) - n_t87;   // level 6
    wire signed [16:0] n_t96 = x40 + x47;   // level 1
    wire signed [16:0] n_t97 = x41 + x46;   // level 1
    wire signed [16:0] n_t98 = x42 - x45;   // level 1
    wire signed [16:0] n_t99 = x43 - x44;   // level 1
    wire signed [17:0] n_t100 = n_t96 - n_t97;   // level 2
    wire signed [17:0] n_t101 = n_t98 + n_t99;   // level 2
    wire signed [18:0] n_t102 = n_t100 - n_t101;   // level 3
    wire signed [18:0] n_t103 = n_t102 - (x47 <<< 1);   // level 4
    wire signed [18:0] n_t104 = n_t102 - (x45 <<< 1);   // level 4
    wire signed [18:0] n_t105 = n_t103 + (x46 <<< 1);   // level 5
    wire signed [18:0] n_t106 = n_t104 - (x44 <<< 1);   // level 5
    wire signed [18:0] n_t107 = n_t105 + (n_t99 <<< 1);   // level 6
    wire signed [18:0] n_t108 = n_t104 + (x43 <<< 1);   // level 5
    wire signed [18:0] n_t109 = (n_t100 <<< 1) - n_t108;   // level 6
    wire signed [18:0] n_t110 = n_t105 + (n_t98 <<< 1);   // level 6
    wire signed [18:0] n_t111 = n_t106 + (n_t97 <<< 1);   // level 6
    wire signed [18:0] n_t112 = n_t103 + (x41 <<< 1);   // level 5
    wire signed [18:0] n_t113 = n_t112 + (n_t101 <<< 1);   // level 6
    wire signed [18:0] n_t114 = (n_t96 <<< 1) - n_t106;   // level 6
    wire signed [16:0] n_t115 = x48 + x55;   // level 1
    wire signed [16:0] n_t116 = x49 + x54;   // level 1
    wire signed [16:0] n_t117 = x50 - x53;   // level 1
    wire signed [16:0] n_t118 = x51 - x52;   // level 1
    wire signed [17:0] n_t119 = n_t115 - n_t116;   // level 2
    wire signed [17:0] n_t120 = n_t117 + n_t118;   // level 2
    wire signed [18:0] n_t121 = n_t119 - n_t120;   // level 3
    wire signed [18:0] n_t122 = n_t121 - (x55 <<< 1);   // level 4
    wire signed [18:0] n_t123 = n_t121 - (x53 <<< 1);   // level 4
    wire signed [18:0] n_t124 = n_t122 + (x54 <<< 1);   // level 5
    wire signed [18:0] n_t125 = n_t123 - (x52 <<< 1);   // level 5
    wire signed [18:0] n_t126 = n_t124 + (n_t118 <<< 1);   // level 6
    wire signed [18:0] n_t127 = n_t123 + (x51 <<< 1);   // level 5
    wire signed [18:0] n_t128 = (n_t119 <<< 1) - n_t127;   // level 6
    wire signed [18:0] n_t129 = n_t124 + (n_t117 <<< 1);   // level 6
    wire signed [18:0] n_t130 = n_t125 + (n_t116 <<< 1);   // level 6
    wire signed [18:0] n_t131 = n_t122 + (x49 <<< 1);   // level 5
    wire signed [18:0] n_t132 = n_t131 + (n_t120 <<< 1);   // level 6
    wire signed [18:0] n_t133 = (n_t115 <<< 1) - n_t125;   // level 6
    wire signed [16:0] n_t134 = x56 + x63;   // level 1
    wire signed [16:0] n_t135 = x57 + x62;   // level 1
    wire signed [16:0] n_t136 = x58 - x61;   // level 1
    wire signed [16:0] n_t137 = x59 - x60;   // level 1
    wire signed [17:0] n_t138 = n_t134 - n_t135;   // level 2
    wire signed [17:0] n_t139 = n_t136 + n_t137;   // level 2
    wire signed [18:0] n_t140 = n_t138 - n_t139;   // level 3
    wire signed [18:0] n_t141 = n_t140 - (x63 <<< 1);   // level 4
    wire signed [18:0] n_t142 = n_t140 - (x61 <<< 1);   // level 4
    wire signed [18:0] n_t143 = n_t141 + (x62 <<< 1);   // level 5
    wire signed [18:0] n_t144 = n_t142 - (x60 <<< 1);   // level 5
    wire signed [18:0] n_t145 = n_t143 + (n_t137 <<< 1);   // level 6
    wire signed [18:0] n_t146 = n_t142 + (x59 <<< 1);   // level 5
    wire signed [18:0] n_t147 = (n_t138 <<< 1) - n_t146;   // level 6
    wire signed [18:0] n_t148 = n_t143 + (n_t136 <<< 1);   // level 6
    wire signed [18:0] n_t149 = n_t144 + (n_t135 <<< 1);   // level 6
    wire signed [18:0] n_t150 = n_t141 + (x57 <<< 1);   // level 5
    wire signed [18:0] n_t151 = n_t150 + (n_t139 <<< 1);   // level 6
    wire signed [18:0] n_t152 = (n_t134 <<< 1) - n_t144;   // level 6
    wire signed [19:0] n_t153 = n_t19 + n_t152;   // level 7
    wire signed [19:0] n_t154 = n_t38 + n_t133;   // level 7
    wire signed [19:0] n_t155 = n_t57 - n_t114;   // level 7
    wire signed [19:0] n_t156 = n_t76 - n_t95;   // level 7
    wire signed [20:0] n_t157 = n_t153 - n_t154;   // level 8
    wire signed [20:0] n_t158 = n_t155 + n_t156;   // level 8
    wire signed [21:0] n_t159 = n_t157 - n_t158;   // level 9
    wire signed [21:0] n_t160 = n_t159 - (n_t152 <<< 1);   // level 10
    wire signed [21:0] n_t161 = n_t159 - (n_t114 <<< 1);   // level 10
    wire signed [21:0] n_t162 = n_t160 + (n_t133 <<< 1);   // level 11
    wire signed [21:0] n_t163 = n_t161 - (n_t95 <<< 1);   // level 11
    wire signed [21:0] n_t164 = n_t162 + (n_t156 <<< 1);   // level 12
    wire signed [21:0] n_t165 = n_t161 + (n_t76 <<< 1);   // level 11
    wire signed [21:0] n_t166 = (n_t157 <<< 1) - n_t165;   // level 12
    wire signed [21:0] n_t167 = n_t162 + (n_t155 <<< 1);   // level 12
    wire signed [21:0] n_t168 = n_t163 + (n_t154 <<< 1);   // level 12
    wire signed [21:0] n_t169 = n_t160 + (n_t38 <<< 1);   // level 11
    wire signed [21:0] n_t170 = n_t169 + (n_t158 <<< 1);   // level 12
    wire signed [21:0] n_t171 = (n_t153 <<< 1) - n_t163;   // level 12
    wire signed [19:0] n_t172 = n_t15 + n_t148;   // level 7
    wire signed [19:0] n_t173 = n_t34 + n_t129;   // level 7
    wire signed [19:0] n_t174 = n_t53 - n_t110;   // level 7
    wire signed [19:0] n_t175 = n_t72 - n_t91;   // level 7
    wire signed [20:0] n_t176 = n_t172 - n_t173;   // level 8
    wire signed [20:0] n_t177 = n_t174 + n_t175;   // level 8
    wire signed [21:0] n_t178 = n_t176 - n_t177;   // level 9
    wire signed [21:0] n_t179 = n_t178 - (n_t148 <<< 1);   // level 10
    wire signed [21:0] n_t180 = n_t178 - (n_t110 <<< 1);   // level 10
    wire signed [21:0] n_t181 = n_t179 + (n_t129 <<< 1);   // level 11
    wire signed [21:0] n_t182 = n_t180 - (n_t91 <<< 1);   // level 11
    wire signed [21:0] n_t183 = n_t181 + (n_t175 <<< 1);   // level 12
    wire signed [21:0] n_t184 = n_t180 + (n_t72 <<< 1);   // level 11
    wire signed [21:0] n_t185 = (n_t176 <<< 1) - n_t184;   // level 12
    wire signed [21:0] n_t186 = n_t181 + (n_t174 <<< 1);   // level 12
    wire signed [21:0] n_t187 = n_t182 + (n_t173 <<< 1);   // level 12
    wire signed [21:0] n_t188 = n_t179 + (n_t34 <<< 1);   // level 11
    wire signed [21:0] n_t189 = n_t188 + (n_t177 <<< 1);   // level 12
    wire signed [21:0] n_t190 = (n_t172 <<< 1) - n_t182;   // level 12
    wire signed [19:0] n_t191 = n_t17 + n_t150;   // level 6
    wire signed [19:0] n_t192 = n_t36 + n_t131;   // level 6
    wire signed [19:0] n_t193 = n_t55 - n_t112;   // level 6
    wire signed [19:0] n_t194 = n_t74 - n_t93;   // level 6
    wire signed [20:0] n_t195 = n_t191 - n_t192;   // level 7
    wire signed [20:0] n_t196 = n_t193 + n_t194;   // level 7
    wire signed [21:0] n_t197 = n_t195 - n_t196;   // level 8
    wire signed [21:0] n_t198 = n_t197 - (n_t150 <<< 1);   // level 9
    wire signed [21:0] n_t199 = n_t197 - (n_t112 <<< 1);   // level 9
    wire signed [21:0] n_t200 = n_t198 + (n_t131 <<< 1);   // level 10
    wire signed [21:0] n_t201 = n_t199 - (n_t93 <<< 1);   // level 10
    wire signed [21:0] n_t202 = n_t200 + (n_t194 <<< 1);   // level 11
    wire signed [21:0] n_t203 = n_t199 + (n_t74 <<< 1);   // level 10
    wire signed [21:0] n_t204 = (n_t195 <<< 1) - n_t203;   // level 11
    wire signed [21:0] n_t205 = n_t200 + (n_t193 <<< 1);   // level 11
    wire signed [21:0] n_t206 = n_t201 + (n_t192 <<< 1);   // level 11
    wire signed [21:0] n_t207 = n_t198 + (n_t36 <<< 1);   // level 10
    wire signed [21:0] n_t208 = n_t207 + (n_t196 <<< 1);   // level 11
    wire signed [21:0] n_t209 = (n_t191 <<< 1) - n_t201;   // level 11
    wire signed [19:0] n_t210 = n_t13 + n_t146;   // level 6
    wire signed [19:0] n_t211 = n_t32 + n_t127;   // level 6
    wire signed [19:0] n_t212 = n_t51 - n_t108;   // level 6
    wire signed [19:0] n_t213 = n_t70 - n_t89;   // level 6
    wire signed [20:0] n_t214 = n_t210 - n_t211;   // level 7
    wire signed [20:0] n_t215 = n_t212 + n_t213;   // level 7
    wire signed [21:0] n_t216 = n_t214 - n_t215;   // level 8
    wire signed [21:0] n_t217 = n_t216 - (n_t146 <<< 1);   // level 9
    wire signed [21:0] n_t218 = n_t216 - (n_t108 <<< 1);   // level 9
    wire signed [21:0] n_t219 = n_t217 + (n_t127 <<< 1);   // level 10
    wire signed [21:0] n_t220 = n_t218 - (n_t89 <<< 1);   // level 10
    wire signed [21:0] n_t221 = n_t219 + (n_t213 <<< 1);   // level 11
    wire signed [21:0] n_t222 = n_t218 + (n_t70 <<< 1);   // level 10
    wire signed [21:0] n_t223 = (n_t214 <<< 1) - n_t222;   // level 11
    wire signed [21:0] n_t224 = n_t219 + (n_t212 <<< 1);   // level 11
    wire signed [21:0] n_t225 = n_t220 + (n_t211 <<< 1);   // level 11
    wire signed [21:0] n_t226 = n_t217 + (n_t32 <<< 1);   // level 10
    wire signed [21:0] n_t227 = n_t226 + (n_t215 <<< 1);   // level 11
    wire signed [21:0] n_t228 = (n_t210 <<< 1) - n_t220;   // level 11
    wire signed [19:0] n_t229 = n_t18 + n_t151;   // level 7
    wire signed [19:0] n_t230 = n_t37 + n_t132;   // level 7
    wire signed [19:0] n_t231 = n_t56 - n_t113;   // level 7
    wire signed [19:0] n_t232 = n_t75 - n_t94;   // level 7
    wire signed [20:0] n_t233 = n_t229 - n_t230;   // level 8
    wire signed [20:0] n_t234 = n_t231 + n_t232;   // level 8
    wire signed [21:0] n_t235 = n_t233 - n_t234;   // level 9
    wire signed [21:0] n_t236 = n_t235 - (n_t151 <<< 1);   // level 10
    wire signed [21:0] n_t237 = n_t235 - (n_t113 <<< 1);   // level 10
    wire signed [21:0] n_t238 = n_t236 + (n_t132 <<< 1);   // level 11
    wire signed [21:0] n_t239 = n_t237 - (n_t94 <<< 1);   // level 11
    wire signed [21:0] n_t240 = n_t238 + (n_t232 <<< 1);   // level 12
    wire signed [21:0] n_t241 = n_t237 + (n_t75 <<< 1);   // level 11
    wire signed [21:0] n_t242 = (n_t233 <<< 1) - n_t241;   // level 12
    wire signed [21:0] n_t243 = n_t238 + (n_t231 <<< 1);   // level 12
    wire signed [21:0] n_t244 = n_t239 + (n_t230 <<< 1);   // level 12
    wire signed [21:0] n_t245 = n_t236 + (n_t37 <<< 1);   // level 11
    wire signed [21:0] n_t246 = n_t245 + (n_t234 <<< 1);   // level 12
    wire signed [21:0] n_t247 = (n_t229 <<< 1) - n_t239;   // level 12
    wire signed [19:0] n_t248 = n_t14 + n_t147;   // level 7
    wire signed [19:0] n_t249 = n_t33 + n_t128;   // level 7
    wire signed [19:0] n_t250 = n_t52 - n_t109;   // level 7
    wire signed [19:0] n_t251 = n_t71 - n_t90;   // level 7
    wire signed [20:0] n_t252 = n_t248 - n_t249;   // level 8
    wire signed [20:0] n_t253 = n_t250 + n_t251;   // level 8
    wire signed [21:0] n_t254 = n_t252 - n_t253;   // level 9
    wire signed [21:0] n_t255 = n_t254 - (n_t147 <<< 1);   // level 10
    wire signed [21:0] n_t256 = n_t254 - (n_t109 <<< 1);   // level 10
    wire signed [21:0] n_t257 = n_t255 + (n_t128 <<< 1);   // level 11
    wire signed [21:0] n_t258 = n_t256 - (n_t90 <<< 1);   // level 11
    wire signed [21:0] n_t259 = n_t257 + (n_t251 <<< 1);   // level 12
    wire signed [21:0] n_t260 = n_t256 + (n_t71 <<< 1);   // level 11
    wire signed [21:0] n_t261 = (n_t252 <<< 1) - n_t260;   // level 12
    wire signed [21:0] n_t262 = n_t257 + (n_t250 <<< 1);   // level 12
    wire signed [21:0] n_t263 = n_t258 + (n_t249 <<< 1);   // level 12
    wire signed [21:0] n_t264 = n_t255 + (n_t33 <<< 1);   // level 11
    wire signed [21:0] n_t265 = n_t264 + (n_t253 <<< 1);   // level 12
    wire signed [21:0] n_t266 = (n_t248 <<< 1) - n_t258;   // level 12
    wire signed [19:0] n_t267 = n_t16 + n_t149;   // level 7
    wire signed [19:0] n_t268 = n_t35 + n_t130;   // level 7
    wire signed [19:0] n_t269 = n_t54 - n_t111;   // level 7
    wire signed [19:0] n_t270 = n_t73 - n_t92;   // level 7
    wire signed [20:0] n_t271 = n_t267 - n_t268;   // level 8
    wire signed [20:0] n_t272 = n_t269 + n_t270;   // level 8
    wire signed [21:0] n_t273 = n_t271 - n_t272;   // level 9
    wire signed [21:0] n_t274 = n_t273 - (n_t149 <<< 1);   // level 10
    wire signed [21:0] n_t275 = n_t273 - (n_t111 <<< 1);   // level 10
    wire signed [21:0] n_t276 = n_t274 + (n_t130 <<< 1);   // level 11
    wire signed [21:0] n_t277 = n_t275 - (n_t92 <<< 1);   // level 11
    wire signed [21:0] n_t278 = n_t276 + (n_t270 <<< 1);   // level 12
    wire signed [21:0] n_t279 = n_t275 + (n_t73 <<< 1);   // level 11
    wire signed [21:0] n_t280 = (n_t271 <<< 1) - n_t279;   // level 12
    wire signed [21:0] n_t281 = n_t276 + (n_t269 <<< 1);   // level 12
    wire signed [21:0] n_t282 = n_t277 + (n_t268 <<< 1);   // level 12
    wire signed [21:0] n_t283 = n_t274 + (n_t35 <<< 1);   // level 11
    wire signed [21:0] n_t284 = n_t283 + (n_t272 <<< 1);   // level 12
    wire signed [21:0] n_t285 = (n_t267 <<< 1) - n_t277;   // level 12
    wire signed [19:0] n_t286 = n_t12 + n_t145;   // level 7
    wire signed [19:0] n_t287 = n_t31 + n_t126;   // level 7
    wire signed [19:0] n_t288 = n_t50 - n_t107;   // level 7
    wire signed [19:0] n_t289 = n_t69 - n_t88;   // level 7
    wire signed [20:0] n_t290 = n_t286 - n_t287;   // level 8
    wire signed [20:0] n_t291 = n_t288 + n_t289;   // level 8
    wire signed [21:0] n_t292 = n_t290 - n_t291;   // level 9
    wire signed [21:0] n_t293 = n_t292 - (n_t145 <<< 1);   // level 10
    wire signed [21:0] n_t294 = n_t292 - (n_t107 <<< 1);   // level 10
    wire signed [21:0] n_t295 = n_t293 + (n_t126 <<< 1);   // level 11
    wire signed [21:0] n_t296 = n_t294 - (n_t88 <<< 1);   // level 11
    wire signed [21:0] n_t297 = n_t295 + (n_t289 <<< 1);   // level 12
    wire signed [21:0] n_t298 = n_t294 + (n_t69 <<< 1);   // level 11
    wire signed [21:0] n_t299 = (n_t290 <<< 1) - n_t298;   // level 12
    wire signed [21:0] n_t300 = n_t295 + (n_t288 <<< 1);   // level 12
    wire signed [21:0] n_t301 = n_t296 + (n_t287 <<< 1);   // level 12
    wire signed [21:0] n_t302 = n_t293 + (n_t31 <<< 1);   // level 11
    wire signed [21:0] n_t303 = n_t302 + (n_t291 <<< 1);   // level 12
    wire signed [21:0] n_t304 = (n_t286 <<< 1) - n_t296;   // level 12
    wire signed [21:0] o0 = n_t171;
    wire signed [21:0] o1 = n_t190;
    wire signed [21:0] o2 = n_t209;
    wire signed [21:0] o3 = n_t228;
    wire signed [21:0] o4 = n_t247;
    wire signed [21:0] o5 = n_t266;
    wire signed [21:0] o6 = n_t285;
    wire signed [21:0] o7 = n_t304;
    wire signed [21:0] o8 = n_t167;
    wire signed [21:0] o9 = n_t186;
    wire signed [21:0] o10 = n_t205;
    wire signed [21:0] o11 = n_t224;
    wire signed [21:0] o12 = n_t243;
    wire signed [21:0] o13 = n_t262;
    wire signed [21:0] o14 = n_t281;
    wire signed [21:0] o15 = n_t300;
    wire signed [21:0] o16 = n_t169;
    wire signed [21:0] o17 = n_t188;
    wire signed [21:0] o18 = n_t207;
    wire signed [21:0] o19 = n_t226;
    wire signed [21:0] o20 = n_t245;
    wire signed [21:0] o21 = n_t264;
    wire signed [21:0] o22 = n_t283;
    wire signed [21:0] o23 = n_t302;
    wire signed [21:0] o24 = n_t165;
    wire signed [21:0] o25 = n_t184;
    wire signed [21:0] o26 = n_t203;
    wire signed [21:0] o27 = n_t222;
    wire signed [21:0] o28 = n_t241;
    wire signed [21:0] o29 = n_t260;
    wire signed [21:0] o30 = n_t279;
    wire signed [21:0] o31 = n_t298;
    wire signed [21:0] o32 = n_t170;
    wire signed [21:0] o33 = n_t189;
    wire signed [21:0] o34 = n_t208;
    wire signed [21:0] o35 = n_t227;
    wire signed [21:0] o36 = n_t246;
    wire signed [21:0] o37 = n_t265;
    wire signed [21:0] o38 = n_t284;
    wire signed [21:0] o39 = n_t303;
    wire signed [21:0] o40 = n_t166;
    wire signed [21:0] o41 = n_t185;
    wire signed [21:0] o42 = n_t204;
    wire signed [21:0] o43 = n_t223;
    wire signed [21:0] o44 = n_t242;
    wire signed [21:0] o45 = n_t261;
    wire signed [21:0] o46 = n_t280;
    wire signed [21:0] o47 = n_t299;
    wire signed [21:0] o48 = n_t168;
    wire signed [21:0] o49 = n_t187;
    wire signed [21:0] o50 = n_t206;
    wire signed [21:0] o51 = n_t225;
    wire signed [21:0] o52 = n_t244;
    wire signed [21:0] o53 = n_t263;
    wire signed [21:0] o54 = n_t282;
    wire signed [21:0] o55 = n_t301;
    wire signed [21:0] o56 = n_t164;
    wire signed [21:0] o57 = n_t183;
    wire signed [21:0] o58 = n_t202;
    wire signed [21:0] o59 = n_t221;
    wire signed [21:0] o60 = n_t240;
    wire signed [21:0] o61 = n_t259;
    wire signed [21:0] o62 = n_t278;
    wire signed [21:0] o63 = n_t297;
    wire [1407:0] out_comb = {
        o63, o62, o61, o60, o59, o58, o57, o56,
        o55, o54, o53, o52, o51, o50, o49, o48,
        o47, o46, o45, o44, o43, o42, o41, o40,
        o39, o38, o37, o36, o35, o34, o33, o32,
        o31, o30, o29, o28, o27, o26, o25, o24,
        o23, o22, o21, o20, o19, o18, o17, o16,
        o15, o14, o13, o12, o11, o10, o9, o8,
        o7, o6, o5, o4, o3, o2, o1, o0
    };
    reg  [1407:0] out_q1;
    reg  [1:0] vld = 2'd0;
    always @(posedge clk) begin
        out_q1 <= out_comb;
        vld <= {vld[0:0], in_valid};
    end
    assign out_data = out_q1;
    assign out_valid = vld[1];
endmodule
`default_nettype wire
