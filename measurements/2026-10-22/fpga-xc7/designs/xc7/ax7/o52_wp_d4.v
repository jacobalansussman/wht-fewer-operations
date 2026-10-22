// Written by gen_ax7.py (wave 16, ax-7).  Do not edit by hand.
// 16-point WHT, word-parallel, registers placed by an integer program (min register bits).
// Source: tools/circuits/programs/h16_52gates.txt
// adders 52, depth 8; at most 4 adder level(s) per clock; latency 2; register bits 388 (after adders 388, delay 0).
`default_nettype none
module wht_o52_wp_d4 (
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
    reg signed [8:0] r_p2_b1;
    reg signed [9:0] r_p4_b1;
    reg signed [9:0] r_p5_b1;
    reg signed [8:0] r_p6_b1;
    reg signed [8:0] r_p7_b1;
    reg signed [9:0] r_p9_b1;
    reg signed [9:0] r_p10_b1;
    reg signed [10:0] r_hub11_b1;
    reg signed [10:0] r_hub14_b1;
    reg signed [8:0] r_p17_b1;
    reg signed [8:0] r_p18_b1;
    reg signed [9:0] r_p20_b1;
    reg signed [9:0] r_p21_b1;
    reg signed [8:0] r_p22_b1;
    reg signed [8:0] r_p23_b1;
    reg signed [9:0] r_p25_b1;
    reg signed [9:0] r_p26_b1;
    reg signed [10:0] r_hub27_b1;
    reg signed [10:0] r_hub30_b1;
    reg signed [11:0] r_p34_b2;
    reg signed [11:0] r_p35_b2;
    reg signed [11:0] r_p36_b2;
    reg signed [11:0] r_p37_b2;
    reg signed [11:0] r_p39_b2;
    reg signed [11:0] r_p40_b2;
    reg signed [11:0] r_p41_b2;
    reg signed [11:0] r_p42_b2;
    reg signed [11:0] r_p44_b2;
    reg signed [11:0] r_p45_b2;
    reg signed [11:0] r_p46_b2;
    reg signed [11:0] r_p47_b2;
    reg signed [11:0] r_p49_b2;
    reg signed [11:0] r_p50_b2;
    reg signed [11:0] r_p51_b2;
    reg signed [11:0] r_p52_b2;
    wire signed [8:0] n_p1 = x0 + x1;   // stage 1 place 1
    wire signed [8:0] n_p2 = x2 - x3;   // stage 1 place 1
    wire signed [9:0] n_hub3 = n_p1 - n_p2;   // stage 1 place 2
    wire signed [9:0] n_p4 = n_hub3 + (x2 <<< 1);   // stage 1 place 3
    wire signed [9:0] n_p5 = (x0 <<< 1) - n_hub3;   // stage 1 place 3
    wire signed [8:0] n_p6 = x4 + x5;   // stage 1 place 1
    wire signed [8:0] n_p7 = x6 - x7;   // stage 1 place 1
    wire signed [9:0] n_hub8 = n_p6 + n_p7;   // stage 1 place 2
    wire signed [9:0] n_p9 = n_hub8 - (x6 <<< 1);   // stage 1 place 3
    wire signed [9:0] n_p10 = (x4 <<< 1) - n_hub8;   // stage 1 place 3
    wire signed [10:0] n_hub11 = n_p4 - n_p9;   // stage 1 place 4
    wire signed [10:0] n_p12 = r_hub11_b1 + (r_p6_b1 <<< 1);   // stage 2 place 1
    wire signed [10:0] n_p13 = (r_p1_b1 <<< 1) - r_hub11_b1;   // stage 2 place 1
    wire signed [10:0] n_hub14 = n_p5 + n_p10;   // stage 1 place 4
    wire signed [10:0] n_p15 = r_hub14_b1 + (r_p7_b1 <<< 1);   // stage 2 place 1
    wire signed [10:0] n_p16 = r_hub14_b1 - (r_p2_b1 <<< 1);   // stage 2 place 1
    wire signed [8:0] n_p17 = x8 + x9;   // stage 1 place 1
    wire signed [8:0] n_p18 = x10 - x11;   // stage 1 place 1
    wire signed [9:0] n_hub19 = n_p17 - n_p18;   // stage 1 place 2
    wire signed [9:0] n_p20 = n_hub19 + (x10 <<< 1);   // stage 1 place 3
    wire signed [9:0] n_p21 = (x8 <<< 1) - n_hub19;   // stage 1 place 3
    wire signed [8:0] n_p22 = x12 + x13;   // stage 1 place 1
    wire signed [8:0] n_p23 = x14 - x15;   // stage 1 place 1
    wire signed [9:0] n_hub24 = n_p22 + n_p23;   // stage 1 place 2
    wire signed [9:0] n_p25 = n_hub24 - (x14 <<< 1);   // stage 1 place 3
    wire signed [9:0] n_p26 = (x12 <<< 1) - n_hub24;   // stage 1 place 3
    wire signed [10:0] n_hub27 = n_p20 + n_p25;   // stage 1 place 4
    wire signed [10:0] n_p28 = r_hub27_b1 - (r_p22_b1 <<< 1);   // stage 2 place 1
    wire signed [10:0] n_p29 = (r_p17_b1 <<< 1) - r_hub27_b1;   // stage 2 place 1
    wire signed [10:0] n_hub30 = n_p21 - n_p26;   // stage 1 place 4
    wire signed [10:0] n_p31 = r_hub30_b1 - (r_p23_b1 <<< 1);   // stage 2 place 1
    wire signed [10:0] n_p32 = r_hub30_b1 - (r_p18_b1 <<< 1);   // stage 2 place 1
    wire signed [11:0] n_hub33 = n_p12 + n_p28;   // stage 2 place 2
    wire signed [11:0] n_p34 = n_hub33 - (r_p20_b1 <<< 1);   // stage 2 place 3
    wire signed [11:0] n_p35 = (r_p4_b1 <<< 1) - n_hub33;   // stage 2 place 3
    wire signed [11:0] n_p36 = (n_p12 <<< 1) - n_p34;   // stage 2 place 4
    wire signed [11:0] n_p37 = n_p35 + (n_p28 <<< 1);   // stage 2 place 4
    wire signed [11:0] n_hub38 = n_p15 + n_p31;   // stage 2 place 2
    wire signed [11:0] n_p39 = n_hub38 - (r_p21_b1 <<< 1);   // stage 2 place 3
    wire signed [11:0] n_p40 = (r_p5_b1 <<< 1) - n_hub38;   // stage 2 place 3
    wire signed [11:0] n_p41 = (n_p15 <<< 1) - n_p39;   // stage 2 place 4
    wire signed [11:0] n_p42 = n_p40 + (n_p31 <<< 1);   // stage 2 place 4
    wire signed [11:0] n_hub43 = n_p13 + n_p29;   // stage 2 place 2
    wire signed [11:0] n_p44 = n_hub43 + (r_p25_b1 <<< 1);   // stage 2 place 3
    wire signed [11:0] n_p45 = n_hub43 - (r_p9_b1 <<< 1);   // stage 2 place 3
    wire signed [11:0] n_p46 = (n_p13 <<< 1) - n_p44;   // stage 2 place 4
    wire signed [11:0] n_p47 = n_p45 - (n_p29 <<< 1);   // stage 2 place 4
    wire signed [11:0] n_hub48 = n_p16 + n_p32;   // stage 2 place 2
    wire signed [11:0] n_p49 = n_hub48 + (r_p26_b1 <<< 1);   // stage 2 place 3
    wire signed [11:0] n_p50 = n_hub48 - (r_p10_b1 <<< 1);   // stage 2 place 3
    wire signed [11:0] n_p51 = (n_p16 <<< 1) - n_p49;   // stage 2 place 4
    wire signed [11:0] n_p52 = n_p50 - (n_p32 <<< 1);   // stage 2 place 4
    always @(posedge clk) begin
        r_p1_b1 <= n_p1;
        r_p2_b1 <= n_p2;
        r_p4_b1 <= n_p4;
        r_p5_b1 <= n_p5;
        r_p6_b1 <= n_p6;
        r_p7_b1 <= n_p7;
        r_p9_b1 <= n_p9;
        r_p10_b1 <= n_p10;
        r_hub11_b1 <= n_hub11;
        r_hub14_b1 <= n_hub14;
        r_p17_b1 <= n_p17;
        r_p18_b1 <= n_p18;
        r_p20_b1 <= n_p20;
        r_p21_b1 <= n_p21;
        r_p22_b1 <= n_p22;
        r_p23_b1 <= n_p23;
        r_p25_b1 <= n_p25;
        r_p26_b1 <= n_p26;
        r_hub27_b1 <= n_hub27;
        r_hub30_b1 <= n_hub30;
        r_p34_b2 <= n_p34;
        r_p35_b2 <= n_p35;
        r_p36_b2 <= n_p36;
        r_p37_b2 <= n_p37;
        r_p39_b2 <= n_p39;
        r_p40_b2 <= n_p40;
        r_p41_b2 <= n_p41;
        r_p42_b2 <= n_p42;
        r_p44_b2 <= n_p44;
        r_p45_b2 <= n_p45;
        r_p46_b2 <= n_p46;
        r_p47_b2 <= n_p47;
        r_p49_b2 <= n_p49;
        r_p50_b2 <= n_p50;
        r_p51_b2 <= n_p51;
        r_p52_b2 <= n_p52;
    end
    wire signed [11:0] o0 = r_p36_b2;
    wire signed [11:0] o1 = r_p41_b2;
    wire signed [11:0] o2 = r_p44_b2;
    wire signed [11:0] o3 = r_p49_b2;
    wire signed [11:0] o4 = r_p37_b2;
    wire signed [11:0] o5 = r_p42_b2;
    wire signed [11:0] o6 = r_p45_b2;
    wire signed [11:0] o7 = r_p50_b2;
    wire signed [11:0] o8 = r_p34_b2;
    wire signed [11:0] o9 = r_p39_b2;
    wire signed [11:0] o10 = r_p46_b2;
    wire signed [11:0] o11 = r_p51_b2;
    wire signed [11:0] o12 = r_p35_b2;
    wire signed [11:0] o13 = r_p40_b2;
    wire signed [11:0] o14 = r_p47_b2;
    wire signed [11:0] o15 = r_p52_b2;
    assign out_data = {o15, o14, o13, o12, o11, o10, o9, o8, o7, o6, o5, o4, o3, o2, o1, o0};
    reg [1:0] vld = 0;
    always @(posedge clk) vld <= {vld[0:0], in_valid};
    assign out_valid = vld[1];
endmodule
