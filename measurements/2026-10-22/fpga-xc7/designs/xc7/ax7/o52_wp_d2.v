// Written by gen_ax7.py (wave 16, ax-7).  Do not edit by hand.
// 16-point WHT, word-parallel, registers placed by an integer program (min register bits).
// Source: tools/circuits/programs/h16_52gates.txt
// adders 52, depth 8; at most 2 adder level(s) per clock; latency 4; register bits 780 (after adders 564, delay 216).
`default_nettype none
module wht_o52_wp_d2 (
    input  wire clk,
    input  wire in_valid,
    input  wire [127:0] in_data,
    output wire out_valid,
    output wire [191:0] out_data
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
    reg signed [8:0] r_p1_b1;
    reg signed [8:0] r_p1_b2;
    reg signed [8:0] r_p2_b1;
    reg signed [8:0] r_p2_b2;
    reg signed [9:0] r_hub3_b1;
    reg signed [9:0] r_p4_b2;
    reg signed [9:0] r_p4_b3;
    reg signed [9:0] r_p5_b2;
    reg signed [9:0] r_p5_b3;
    reg signed [8:0] r_p6_b1;
    reg signed [8:0] r_p6_b2;
    reg signed [8:0] r_p7_b1;
    reg signed [8:0] r_p7_b2;
    reg signed [9:0] r_hub8_b1;
    reg signed [9:0] r_p9_b2;
    reg signed [9:0] r_p9_b3;
    reg signed [9:0] r_p10_b2;
    reg signed [9:0] r_p10_b3;
    reg signed [10:0] r_hub11_b2;
    reg signed [10:0] r_p12_b3;
    reg signed [10:0] r_p13_b3;
    reg signed [10:0] r_hub14_b2;
    reg signed [10:0] r_p15_b3;
    reg signed [10:0] r_p16_b3;
    reg signed [8:0] r_p17_b1;
    reg signed [8:0] r_p17_b2;
    reg signed [8:0] r_p18_b1;
    reg signed [8:0] r_p18_b2;
    reg signed [9:0] r_hub19_b1;
    reg signed [9:0] r_p20_b2;
    reg signed [9:0] r_p20_b3;
    reg signed [9:0] r_p21_b2;
    reg signed [9:0] r_p21_b3;
    reg signed [8:0] r_p22_b1;
    reg signed [8:0] r_p22_b2;
    reg signed [8:0] r_p23_b1;
    reg signed [8:0] r_p23_b2;
    reg signed [9:0] r_hub24_b1;
    reg signed [9:0] r_p25_b2;
    reg signed [9:0] r_p25_b3;
    reg signed [9:0] r_p26_b2;
    reg signed [9:0] r_p26_b3;
    reg signed [10:0] r_hub27_b2;
    reg signed [10:0] r_p28_b3;
    reg signed [10:0] r_p29_b3;
    reg signed [10:0] r_hub30_b2;
    reg signed [10:0] r_p31_b3;
    reg signed [10:0] r_p32_b3;
    reg signed [11:0] r_hub33_b3;
    reg signed [11:0] r_p34_b4;
    reg signed [11:0] r_p35_b4;
    reg signed [11:0] r_p36_b4;
    reg signed [11:0] r_p37_b4;
    reg signed [11:0] r_hub38_b3;
    reg signed [11:0] r_p39_b4;
    reg signed [11:0] r_p40_b4;
    reg signed [11:0] r_p41_b4;
    reg signed [11:0] r_p42_b4;
    reg signed [11:0] r_hub43_b3;
    reg signed [11:0] r_p44_b4;
    reg signed [11:0] r_p45_b4;
    reg signed [11:0] r_p46_b4;
    reg signed [11:0] r_p47_b4;
    reg signed [11:0] r_hub48_b3;
    reg signed [11:0] r_p49_b4;
    reg signed [11:0] r_p50_b4;
    reg signed [11:0] r_p51_b4;
    reg signed [11:0] r_p52_b4;
    reg signed [7:0] r_x0_b1;
    reg signed [7:0] r_x2_b1;
    reg signed [7:0] r_x4_b1;
    reg signed [7:0] r_x6_b1;
    reg signed [7:0] r_x8_b1;
    reg signed [7:0] r_x10_b1;
    reg signed [7:0] r_x12_b1;
    reg signed [7:0] r_x14_b1;
    wire signed [8:0] n_p1 = x0 + x1;   // stage 1 place 1
    wire signed [8:0] n_p2 = x2 - x3;   // stage 1 place 1
    wire signed [9:0] n_hub3 = n_p1 - n_p2;   // stage 1 place 2
    wire signed [9:0] n_p4 = r_hub3_b1 + (r_x2_b1 <<< 1);   // stage 2 place 1
    wire signed [9:0] n_p5 = (r_x0_b1 <<< 1) - r_hub3_b1;   // stage 2 place 1
    wire signed [8:0] n_p6 = x4 + x5;   // stage 1 place 1
    wire signed [8:0] n_p7 = x6 - x7;   // stage 1 place 1
    wire signed [9:0] n_hub8 = n_p6 + n_p7;   // stage 1 place 2
    wire signed [9:0] n_p9 = r_hub8_b1 - (r_x6_b1 <<< 1);   // stage 2 place 1
    wire signed [9:0] n_p10 = (r_x4_b1 <<< 1) - r_hub8_b1;   // stage 2 place 1
    wire signed [10:0] n_hub11 = n_p4 - n_p9;   // stage 2 place 2
    wire signed [10:0] n_p12 = r_hub11_b2 + (r_p6_b2 <<< 1);   // stage 3 place 1
    wire signed [10:0] n_p13 = (r_p1_b2 <<< 1) - r_hub11_b2;   // stage 3 place 1
    wire signed [10:0] n_hub14 = n_p5 + n_p10;   // stage 2 place 2
    wire signed [10:0] n_p15 = r_hub14_b2 + (r_p7_b2 <<< 1);   // stage 3 place 1
    wire signed [10:0] n_p16 = r_hub14_b2 - (r_p2_b2 <<< 1);   // stage 3 place 1
    wire signed [8:0] n_p17 = x8 + x9;   // stage 1 place 1
    wire signed [8:0] n_p18 = x10 - x11;   // stage 1 place 1
    wire signed [9:0] n_hub19 = n_p17 - n_p18;   // stage 1 place 2
    wire signed [9:0] n_p20 = r_hub19_b1 + (r_x10_b1 <<< 1);   // stage 2 place 1
    wire signed [9:0] n_p21 = (r_x8_b1 <<< 1) - r_hub19_b1;   // stage 2 place 1
    wire signed [8:0] n_p22 = x12 + x13;   // stage 1 place 1
    wire signed [8:0] n_p23 = x14 - x15;   // stage 1 place 1
    wire signed [9:0] n_hub24 = n_p22 + n_p23;   // stage 1 place 2
    wire signed [9:0] n_p25 = r_hub24_b1 - (r_x14_b1 <<< 1);   // stage 2 place 1
    wire signed [9:0] n_p26 = (r_x12_b1 <<< 1) - r_hub24_b1;   // stage 2 place 1
    wire signed [10:0] n_hub27 = n_p20 + n_p25;   // stage 2 place 2
    wire signed [10:0] n_p28 = r_hub27_b2 - (r_p22_b2 <<< 1);   // stage 3 place 1
    wire signed [10:0] n_p29 = (r_p17_b2 <<< 1) - r_hub27_b2;   // stage 3 place 1
    wire signed [10:0] n_hub30 = n_p21 - n_p26;   // stage 2 place 2
    wire signed [10:0] n_p31 = r_hub30_b2 - (r_p23_b2 <<< 1);   // stage 3 place 1
    wire signed [10:0] n_p32 = r_hub30_b2 - (r_p18_b2 <<< 1);   // stage 3 place 1
    wire signed [11:0] n_hub33 = n_p12 + n_p28;   // stage 3 place 2
    wire signed [11:0] n_p34 = r_hub33_b3 - (r_p20_b3 <<< 1);   // stage 4 place 1
    wire signed [11:0] n_p35 = (r_p4_b3 <<< 1) - r_hub33_b3;   // stage 4 place 1
    wire signed [11:0] n_p36 = (r_p12_b3 <<< 1) - n_p34;   // stage 4 place 2
    wire signed [11:0] n_p37 = n_p35 + (r_p28_b3 <<< 1);   // stage 4 place 2
    wire signed [11:0] n_hub38 = n_p15 + n_p31;   // stage 3 place 2
    wire signed [11:0] n_p39 = r_hub38_b3 - (r_p21_b3 <<< 1);   // stage 4 place 1
    wire signed [11:0] n_p40 = (r_p5_b3 <<< 1) - r_hub38_b3;   // stage 4 place 1
    wire signed [11:0] n_p41 = (r_p15_b3 <<< 1) - n_p39;   // stage 4 place 2
    wire signed [11:0] n_p42 = n_p40 + (r_p31_b3 <<< 1);   // stage 4 place 2
    wire signed [11:0] n_hub43 = n_p13 + n_p29;   // stage 3 place 2
    wire signed [11:0] n_p44 = r_hub43_b3 + (r_p25_b3 <<< 1);   // stage 4 place 1
    wire signed [11:0] n_p45 = r_hub43_b3 - (r_p9_b3 <<< 1);   // stage 4 place 1
    wire signed [11:0] n_p46 = (r_p13_b3 <<< 1) - n_p44;   // stage 4 place 2
    wire signed [11:0] n_p47 = n_p45 - (r_p29_b3 <<< 1);   // stage 4 place 2
    wire signed [11:0] n_hub48 = n_p16 + n_p32;   // stage 3 place 2
    wire signed [11:0] n_p49 = r_hub48_b3 + (r_p26_b3 <<< 1);   // stage 4 place 1
    wire signed [11:0] n_p50 = r_hub48_b3 - (r_p10_b3 <<< 1);   // stage 4 place 1
    wire signed [11:0] n_p51 = (r_p16_b3 <<< 1) - n_p49;   // stage 4 place 2
    wire signed [11:0] n_p52 = n_p50 - (r_p32_b3 <<< 1);   // stage 4 place 2
    always @(posedge clk) begin
        r_p1_b1 <= n_p1;
        r_p1_b2 <= r_p1_b1;
        r_p2_b1 <= n_p2;
        r_p2_b2 <= r_p2_b1;
        r_hub3_b1 <= n_hub3;
        r_p4_b2 <= n_p4;
        r_p4_b3 <= r_p4_b2;
        r_p5_b2 <= n_p5;
        r_p5_b3 <= r_p5_b2;
        r_p6_b1 <= n_p6;
        r_p6_b2 <= r_p6_b1;
        r_p7_b1 <= n_p7;
        r_p7_b2 <= r_p7_b1;
        r_hub8_b1 <= n_hub8;
        r_p9_b2 <= n_p9;
        r_p9_b3 <= r_p9_b2;
        r_p10_b2 <= n_p10;
        r_p10_b3 <= r_p10_b2;
        r_hub11_b2 <= n_hub11;
        r_p12_b3 <= n_p12;
        r_p13_b3 <= n_p13;
        r_hub14_b2 <= n_hub14;
        r_p15_b3 <= n_p15;
        r_p16_b3 <= n_p16;
        r_p17_b1 <= n_p17;
        r_p17_b2 <= r_p17_b1;
        r_p18_b1 <= n_p18;
        r_p18_b2 <= r_p18_b1;
        r_hub19_b1 <= n_hub19;
        r_p20_b2 <= n_p20;
        r_p20_b3 <= r_p20_b2;
        r_p21_b2 <= n_p21;
        r_p21_b3 <= r_p21_b2;
        r_p22_b1 <= n_p22;
        r_p22_b2 <= r_p22_b1;
        r_p23_b1 <= n_p23;
        r_p23_b2 <= r_p23_b1;
        r_hub24_b1 <= n_hub24;
        r_p25_b2 <= n_p25;
        r_p25_b3 <= r_p25_b2;
        r_p26_b2 <= n_p26;
        r_p26_b3 <= r_p26_b2;
        r_hub27_b2 <= n_hub27;
        r_p28_b3 <= n_p28;
        r_p29_b3 <= n_p29;
        r_hub30_b2 <= n_hub30;
        r_p31_b3 <= n_p31;
        r_p32_b3 <= n_p32;
        r_hub33_b3 <= n_hub33;
        r_p34_b4 <= n_p34;
        r_p35_b4 <= n_p35;
        r_p36_b4 <= n_p36;
        r_p37_b4 <= n_p37;
        r_hub38_b3 <= n_hub38;
        r_p39_b4 <= n_p39;
        r_p40_b4 <= n_p40;
        r_p41_b4 <= n_p41;
        r_p42_b4 <= n_p42;
        r_hub43_b3 <= n_hub43;
        r_p44_b4 <= n_p44;
        r_p45_b4 <= n_p45;
        r_p46_b4 <= n_p46;
        r_p47_b4 <= n_p47;
        r_hub48_b3 <= n_hub48;
        r_p49_b4 <= n_p49;
        r_p50_b4 <= n_p50;
        r_p51_b4 <= n_p51;
        r_p52_b4 <= n_p52;
        r_x0_b1 <= x0;
        r_x2_b1 <= x2;
        r_x4_b1 <= x4;
        r_x6_b1 <= x6;
        r_x8_b1 <= x8;
        r_x10_b1 <= x10;
        r_x12_b1 <= x12;
        r_x14_b1 <= x14;
    end
    wire signed [11:0] o0 = r_p36_b4;
    wire signed [11:0] o1 = r_p41_b4;
    wire signed [11:0] o2 = r_p44_b4;
    wire signed [11:0] o3 = r_p49_b4;
    wire signed [11:0] o4 = r_p37_b4;
    wire signed [11:0] o5 = r_p42_b4;
    wire signed [11:0] o6 = r_p45_b4;
    wire signed [11:0] o7 = r_p50_b4;
    wire signed [11:0] o8 = r_p34_b4;
    wire signed [11:0] o9 = r_p39_b4;
    wire signed [11:0] o10 = r_p46_b4;
    wire signed [11:0] o11 = r_p51_b4;
    wire signed [11:0] o12 = r_p35_b4;
    wire signed [11:0] o13 = r_p40_b4;
    wire signed [11:0] o14 = r_p47_b4;
    wire signed [11:0] o15 = r_p52_b4;
    assign out_data = {o15, o14, o13, o12, o11, o10, o9, o8, o7, o6, o5, o4, o3, o2, o1, o0};
    reg [3:0] vld = 0;
    always @(posedge clk) vld <= {vld[2:0], in_valid};
    assign out_valid = vld[3];
endmodule
