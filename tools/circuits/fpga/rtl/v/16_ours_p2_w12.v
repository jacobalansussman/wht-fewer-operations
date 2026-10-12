// Written by gen_rtl.py.  Do not edit by hand.
// 16-point Walsh-Hadamard transform, y_J = sum over i of (-1)^popcount(J & i) * x_i.
// Source circuit: tools/circuits/programs/h16_52gates.txt
// This work: the 52-adder circuit (the family at 16 points).
// Inputs: 16 signed values of 12 bits.  Outputs: 16 signed values of 16 bits.
// Adders 52, depth 8 adder levels, adder bits 772 (chain bits 752).
// Variant p2: a register after every second adder level.  Latency 4.
// Register bits: 772 after adders, 312 in delay registers, 4 valid bits.
`default_nettype none
module wht_16_ours_p2_w12 (
    input  wire                 clk,
    input  wire                 in_valid,
    input  wire [191:0] in_data,
    output wire                 out_valid,
    output wire [255:0] out_data
);
    wire signed [11:0] x0 = in_data[11:0];
    wire signed [11:0] x1 = in_data[23:12];
    wire signed [11:0] x2 = in_data[35:24];
    wire signed [11:0] x3 = in_data[47:36];
    wire signed [11:0] x4 = in_data[59:48];
    wire signed [11:0] x5 = in_data[71:60];
    wire signed [11:0] x6 = in_data[83:72];
    wire signed [11:0] x7 = in_data[95:84];
    wire signed [11:0] x8 = in_data[107:96];
    wire signed [11:0] x9 = in_data[119:108];
    wire signed [11:0] x10 = in_data[131:120];
    wire signed [11:0] x11 = in_data[143:132];
    wire signed [11:0] x12 = in_data[155:144];
    wire signed [11:0] x13 = in_data[167:156];
    wire signed [11:0] x14 = in_data[179:168];
    wire signed [11:0] x15 = in_data[191:180];
    reg  signed [11:0] x0_r1;
    reg  signed [11:0] x2_r1;
    reg  signed [11:0] x4_r1;
    reg  signed [11:0] x6_r1;
    reg  signed [11:0] x8_r1;
    reg  signed [11:0] x10_r1;
    reg  signed [11:0] x12_r1;
    reg  signed [11:0] x14_r1;
    wire signed [12:0] n_p1 = x0 + x1;   // level 1, stage 1
    reg  signed [12:0] n_p1_r1;
    reg  signed [12:0] n_p1_r2;
    wire signed [12:0] n_p2 = x2 - x3;   // level 1, stage 1
    reg  signed [12:0] n_p2_r1;
    reg  signed [12:0] n_p2_r2;
    wire signed [13:0] n_hub3 = n_p1 - n_p2;   // level 2, stage 1
    reg  signed [13:0] n_hub3_r1;
    wire signed [13:0] n_p4 = n_hub3_r1 + (x2_r1 <<< 1);   // level 3, stage 2
    reg  signed [13:0] n_p4_r2;
    reg  signed [13:0] n_p4_r3;
    wire signed [13:0] n_p5 = (x0_r1 <<< 1) - n_hub3_r1;   // level 3, stage 2
    reg  signed [13:0] n_p5_r2;
    reg  signed [13:0] n_p5_r3;
    wire signed [12:0] n_p6 = x4 + x5;   // level 1, stage 1
    reg  signed [12:0] n_p6_r1;
    reg  signed [12:0] n_p6_r2;
    wire signed [12:0] n_p7 = x6 - x7;   // level 1, stage 1
    reg  signed [12:0] n_p7_r1;
    reg  signed [12:0] n_p7_r2;
    wire signed [13:0] n_hub8 = n_p6 + n_p7;   // level 2, stage 1
    reg  signed [13:0] n_hub8_r1;
    wire signed [13:0] n_p9 = n_hub8_r1 - (x6_r1 <<< 1);   // level 3, stage 2
    reg  signed [13:0] n_p9_r2;
    reg  signed [13:0] n_p9_r3;
    wire signed [13:0] n_p10 = (x4_r1 <<< 1) - n_hub8_r1;   // level 3, stage 2
    reg  signed [13:0] n_p10_r2;
    reg  signed [13:0] n_p10_r3;
    wire signed [14:0] n_hub11 = n_p4 - n_p9;   // level 4, stage 2
    reg  signed [14:0] n_hub11_r2;
    wire signed [14:0] n_p12 = n_hub11_r2 + (n_p6_r2 <<< 1);   // level 5, stage 3
    reg  signed [14:0] n_p12_r3;
    wire signed [14:0] n_p13 = (n_p1_r2 <<< 1) - n_hub11_r2;   // level 5, stage 3
    reg  signed [14:0] n_p13_r3;
    wire signed [14:0] n_hub14 = n_p5 + n_p10;   // level 4, stage 2
    reg  signed [14:0] n_hub14_r2;
    wire signed [14:0] n_p15 = n_hub14_r2 + (n_p7_r2 <<< 1);   // level 5, stage 3
    reg  signed [14:0] n_p15_r3;
    wire signed [14:0] n_p16 = n_hub14_r2 - (n_p2_r2 <<< 1);   // level 5, stage 3
    reg  signed [14:0] n_p16_r3;
    wire signed [12:0] n_p17 = x8 + x9;   // level 1, stage 1
    reg  signed [12:0] n_p17_r1;
    reg  signed [12:0] n_p17_r2;
    wire signed [12:0] n_p18 = x10 - x11;   // level 1, stage 1
    reg  signed [12:0] n_p18_r1;
    reg  signed [12:0] n_p18_r2;
    wire signed [13:0] n_hub19 = n_p17 - n_p18;   // level 2, stage 1
    reg  signed [13:0] n_hub19_r1;
    wire signed [13:0] n_p20 = n_hub19_r1 + (x10_r1 <<< 1);   // level 3, stage 2
    reg  signed [13:0] n_p20_r2;
    reg  signed [13:0] n_p20_r3;
    wire signed [13:0] n_p21 = (x8_r1 <<< 1) - n_hub19_r1;   // level 3, stage 2
    reg  signed [13:0] n_p21_r2;
    reg  signed [13:0] n_p21_r3;
    wire signed [12:0] n_p22 = x12 + x13;   // level 1, stage 1
    reg  signed [12:0] n_p22_r1;
    reg  signed [12:0] n_p22_r2;
    wire signed [12:0] n_p23 = x14 - x15;   // level 1, stage 1
    reg  signed [12:0] n_p23_r1;
    reg  signed [12:0] n_p23_r2;
    wire signed [13:0] n_hub24 = n_p22 + n_p23;   // level 2, stage 1
    reg  signed [13:0] n_hub24_r1;
    wire signed [13:0] n_p25 = n_hub24_r1 - (x14_r1 <<< 1);   // level 3, stage 2
    reg  signed [13:0] n_p25_r2;
    reg  signed [13:0] n_p25_r3;
    wire signed [13:0] n_p26 = (x12_r1 <<< 1) - n_hub24_r1;   // level 3, stage 2
    reg  signed [13:0] n_p26_r2;
    reg  signed [13:0] n_p26_r3;
    wire signed [14:0] n_hub27 = n_p20 + n_p25;   // level 4, stage 2
    reg  signed [14:0] n_hub27_r2;
    wire signed [14:0] n_p28 = n_hub27_r2 - (n_p22_r2 <<< 1);   // level 5, stage 3
    reg  signed [14:0] n_p28_r3;
    wire signed [14:0] n_p29 = (n_p17_r2 <<< 1) - n_hub27_r2;   // level 5, stage 3
    reg  signed [14:0] n_p29_r3;
    wire signed [14:0] n_hub30 = n_p21 - n_p26;   // level 4, stage 2
    reg  signed [14:0] n_hub30_r2;
    wire signed [14:0] n_p31 = n_hub30_r2 - (n_p23_r2 <<< 1);   // level 5, stage 3
    reg  signed [14:0] n_p31_r3;
    wire signed [14:0] n_p32 = n_hub30_r2 - (n_p18_r2 <<< 1);   // level 5, stage 3
    reg  signed [14:0] n_p32_r3;
    wire signed [15:0] n_hub33 = n_p12 + n_p28;   // level 6, stage 3
    reg  signed [15:0] n_hub33_r3;
    wire signed [15:0] n_p34 = n_hub33_r3 - (n_p20_r3 <<< 1);   // level 7, stage 4
    reg  signed [15:0] n_p34_r4;
    wire signed [15:0] n_p35 = (n_p4_r3 <<< 1) - n_hub33_r3;   // level 7, stage 4
    reg  signed [15:0] n_p35_r4;
    wire signed [15:0] n_p36 = (n_p12_r3 <<< 1) - n_p34;   // level 8, stage 4
    reg  signed [15:0] n_p36_r4;
    wire signed [15:0] n_p37 = n_p35 + (n_p28_r3 <<< 1);   // level 8, stage 4
    reg  signed [15:0] n_p37_r4;
    wire signed [15:0] n_hub38 = n_p15 + n_p31;   // level 6, stage 3
    reg  signed [15:0] n_hub38_r3;
    wire signed [15:0] n_p39 = n_hub38_r3 - (n_p21_r3 <<< 1);   // level 7, stage 4
    reg  signed [15:0] n_p39_r4;
    wire signed [15:0] n_p40 = (n_p5_r3 <<< 1) - n_hub38_r3;   // level 7, stage 4
    reg  signed [15:0] n_p40_r4;
    wire signed [15:0] n_p41 = (n_p15_r3 <<< 1) - n_p39;   // level 8, stage 4
    reg  signed [15:0] n_p41_r4;
    wire signed [15:0] n_p42 = n_p40 + (n_p31_r3 <<< 1);   // level 8, stage 4
    reg  signed [15:0] n_p42_r4;
    wire signed [15:0] n_hub43 = n_p13 + n_p29;   // level 6, stage 3
    reg  signed [15:0] n_hub43_r3;
    wire signed [15:0] n_p44 = n_hub43_r3 + (n_p25_r3 <<< 1);   // level 7, stage 4
    reg  signed [15:0] n_p44_r4;
    wire signed [15:0] n_p45 = n_hub43_r3 - (n_p9_r3 <<< 1);   // level 7, stage 4
    reg  signed [15:0] n_p45_r4;
    wire signed [15:0] n_p46 = (n_p13_r3 <<< 1) - n_p44;   // level 8, stage 4
    reg  signed [15:0] n_p46_r4;
    wire signed [15:0] n_p47 = n_p45 - (n_p29_r3 <<< 1);   // level 8, stage 4
    reg  signed [15:0] n_p47_r4;
    wire signed [15:0] n_hub48 = n_p16 + n_p32;   // level 6, stage 3
    reg  signed [15:0] n_hub48_r3;
    wire signed [15:0] n_p49 = n_hub48_r3 + (n_p26_r3 <<< 1);   // level 7, stage 4
    reg  signed [15:0] n_p49_r4;
    wire signed [15:0] n_p50 = n_hub48_r3 - (n_p10_r3 <<< 1);   // level 7, stage 4
    reg  signed [15:0] n_p50_r4;
    wire signed [15:0] n_p51 = (n_p16_r3 <<< 1) - n_p49;   // level 8, stage 4
    reg  signed [15:0] n_p51_r4;
    wire signed [15:0] n_p52 = n_p50 - (n_p32_r3 <<< 1);   // level 8, stage 4
    reg  signed [15:0] n_p52_r4;
    wire signed [15:0] o0 = n_p36_r4;
    wire signed [15:0] o1 = n_p41_r4;
    wire signed [15:0] o2 = n_p44_r4;
    wire signed [15:0] o3 = n_p49_r4;
    wire signed [15:0] o4 = n_p37_r4;
    wire signed [15:0] o5 = n_p42_r4;
    wire signed [15:0] o6 = n_p45_r4;
    wire signed [15:0] o7 = n_p50_r4;
    wire signed [15:0] o8 = n_p34_r4;
    wire signed [15:0] o9 = n_p39_r4;
    wire signed [15:0] o10 = n_p46_r4;
    wire signed [15:0] o11 = n_p51_r4;
    wire signed [15:0] o12 = n_p35_r4;
    wire signed [15:0] o13 = n_p40_r4;
    wire signed [15:0] o14 = n_p47_r4;
    wire signed [15:0] o15 = n_p52_r4;
    assign out_data = {
        o15, o14, o13, o12, o11, o10, o9, o8,
        o7, o6, o5, o4, o3, o2, o1, o0
    };
    reg  [3:0] vld = 4'd0;
    always @(posedge clk) begin
        x0_r1 <= x0;
        x2_r1 <= x2;
        x4_r1 <= x4;
        x6_r1 <= x6;
        x8_r1 <= x8;
        x10_r1 <= x10;
        x12_r1 <= x12;
        x14_r1 <= x14;
        n_p1_r1 <= n_p1;
        n_p1_r2 <= n_p1_r1;
        n_p2_r1 <= n_p2;
        n_p2_r2 <= n_p2_r1;
        n_hub3_r1 <= n_hub3;
        n_p4_r2 <= n_p4;
        n_p4_r3 <= n_p4_r2;
        n_p5_r2 <= n_p5;
        n_p5_r3 <= n_p5_r2;
        n_p6_r1 <= n_p6;
        n_p6_r2 <= n_p6_r1;
        n_p7_r1 <= n_p7;
        n_p7_r2 <= n_p7_r1;
        n_hub8_r1 <= n_hub8;
        n_p9_r2 <= n_p9;
        n_p9_r3 <= n_p9_r2;
        n_p10_r2 <= n_p10;
        n_p10_r3 <= n_p10_r2;
        n_hub11_r2 <= n_hub11;
        n_p12_r3 <= n_p12;
        n_p13_r3 <= n_p13;
        n_hub14_r2 <= n_hub14;
        n_p15_r3 <= n_p15;
        n_p16_r3 <= n_p16;
        n_p17_r1 <= n_p17;
        n_p17_r2 <= n_p17_r1;
        n_p18_r1 <= n_p18;
        n_p18_r2 <= n_p18_r1;
        n_hub19_r1 <= n_hub19;
        n_p20_r2 <= n_p20;
        n_p20_r3 <= n_p20_r2;
        n_p21_r2 <= n_p21;
        n_p21_r3 <= n_p21_r2;
        n_p22_r1 <= n_p22;
        n_p22_r2 <= n_p22_r1;
        n_p23_r1 <= n_p23;
        n_p23_r2 <= n_p23_r1;
        n_hub24_r1 <= n_hub24;
        n_p25_r2 <= n_p25;
        n_p25_r3 <= n_p25_r2;
        n_p26_r2 <= n_p26;
        n_p26_r3 <= n_p26_r2;
        n_hub27_r2 <= n_hub27;
        n_p28_r3 <= n_p28;
        n_p29_r3 <= n_p29;
        n_hub30_r2 <= n_hub30;
        n_p31_r3 <= n_p31;
        n_p32_r3 <= n_p32;
        n_hub33_r3 <= n_hub33;
        n_p34_r4 <= n_p34;
        n_p35_r4 <= n_p35;
        n_p36_r4 <= n_p36;
        n_p37_r4 <= n_p37;
        n_hub38_r3 <= n_hub38;
        n_p39_r4 <= n_p39;
        n_p40_r4 <= n_p40;
        n_p41_r4 <= n_p41;
        n_p42_r4 <= n_p42;
        n_hub43_r3 <= n_hub43;
        n_p44_r4 <= n_p44;
        n_p45_r4 <= n_p45;
        n_p46_r4 <= n_p46;
        n_p47_r4 <= n_p47;
        n_hub48_r3 <= n_hub48;
        n_p49_r4 <= n_p49;
        n_p50_r4 <= n_p50;
        n_p51_r4 <= n_p51;
        n_p52_r4 <= n_p52;
        vld <= {vld[2:0], in_valid};
    end
    assign out_valid = vld[3];
endmodule
`default_nettype wire
