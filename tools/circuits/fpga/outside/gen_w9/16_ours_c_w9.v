// Written by gen_rtl.py.  Do not edit by hand.
// 16-point Walsh-Hadamard transform, y_J = sum over i of (-1)^popcount(J & i) * x_i.
// Source circuit: tools/circuits/programs/h16_52gates.txt
// Inputs: 16 signed values of 9 bits.  Outputs: 16 signed values of 13 bits.
// Adders 52, depth 8 adder levels, adder bits 616 (chain bits 596).
// Variant c: combinational.  Latency 0.  clk is not used.
`default_nettype none
module wht_16_ours_c_w9 (
    input  wire                 clk,
    input  wire                 in_valid,
    input  wire [143:0] in_data,
    output wire                 out_valid,
    output wire [207:0] out_data
);
    wire signed [8:0] x0 = in_data[8:0];
    wire signed [8:0] x1 = in_data[17:9];
    wire signed [8:0] x2 = in_data[26:18];
    wire signed [8:0] x3 = in_data[35:27];
    wire signed [8:0] x4 = in_data[44:36];
    wire signed [8:0] x5 = in_data[53:45];
    wire signed [8:0] x6 = in_data[62:54];
    wire signed [8:0] x7 = in_data[71:63];
    wire signed [8:0] x8 = in_data[80:72];
    wire signed [8:0] x9 = in_data[89:81];
    wire signed [8:0] x10 = in_data[98:90];
    wire signed [8:0] x11 = in_data[107:99];
    wire signed [8:0] x12 = in_data[116:108];
    wire signed [8:0] x13 = in_data[125:117];
    wire signed [8:0] x14 = in_data[134:126];
    wire signed [8:0] x15 = in_data[143:135];
    wire signed [9:0] n_p1 = x0 + x1;   // level 1
    wire signed [9:0] n_p2 = x2 - x3;   // level 1
    wire signed [10:0] n_hub3 = n_p1 - n_p2;   // level 2
    wire signed [10:0] n_p4 = n_hub3 + (x2 <<< 1);   // level 3
    wire signed [10:0] n_p5 = (x0 <<< 1) - n_hub3;   // level 3
    wire signed [9:0] n_p6 = x4 + x5;   // level 1
    wire signed [9:0] n_p7 = x6 - x7;   // level 1
    wire signed [10:0] n_hub8 = n_p6 + n_p7;   // level 2
    wire signed [10:0] n_p9 = n_hub8 - (x6 <<< 1);   // level 3
    wire signed [10:0] n_p10 = (x4 <<< 1) - n_hub8;   // level 3
    wire signed [11:0] n_hub11 = n_p4 - n_p9;   // level 4
    wire signed [11:0] n_p12 = n_hub11 + (n_p6 <<< 1);   // level 5
    wire signed [11:0] n_p13 = (n_p1 <<< 1) - n_hub11;   // level 5
    wire signed [11:0] n_hub14 = n_p5 + n_p10;   // level 4
    wire signed [11:0] n_p15 = n_hub14 + (n_p7 <<< 1);   // level 5
    wire signed [11:0] n_p16 = n_hub14 - (n_p2 <<< 1);   // level 5
    wire signed [9:0] n_p17 = x8 + x9;   // level 1
    wire signed [9:0] n_p18 = x10 - x11;   // level 1
    wire signed [10:0] n_hub19 = n_p17 - n_p18;   // level 2
    wire signed [10:0] n_p20 = n_hub19 + (x10 <<< 1);   // level 3
    wire signed [10:0] n_p21 = (x8 <<< 1) - n_hub19;   // level 3
    wire signed [9:0] n_p22 = x12 + x13;   // level 1
    wire signed [9:0] n_p23 = x14 - x15;   // level 1
    wire signed [10:0] n_hub24 = n_p22 + n_p23;   // level 2
    wire signed [10:0] n_p25 = n_hub24 - (x14 <<< 1);   // level 3
    wire signed [10:0] n_p26 = (x12 <<< 1) - n_hub24;   // level 3
    wire signed [11:0] n_hub27 = n_p20 + n_p25;   // level 4
    wire signed [11:0] n_p28 = n_hub27 - (n_p22 <<< 1);   // level 5
    wire signed [11:0] n_p29 = (n_p17 <<< 1) - n_hub27;   // level 5
    wire signed [11:0] n_hub30 = n_p21 - n_p26;   // level 4
    wire signed [11:0] n_p31 = n_hub30 - (n_p23 <<< 1);   // level 5
    wire signed [11:0] n_p32 = n_hub30 - (n_p18 <<< 1);   // level 5
    wire signed [12:0] n_hub33 = n_p12 + n_p28;   // level 6
    wire signed [12:0] n_p34 = n_hub33 - (n_p20 <<< 1);   // level 7
    wire signed [12:0] n_p35 = (n_p4 <<< 1) - n_hub33;   // level 7
    wire signed [12:0] n_p36 = (n_p12 <<< 1) - n_p34;   // level 8
    wire signed [12:0] n_p37 = n_p35 + (n_p28 <<< 1);   // level 8
    wire signed [12:0] n_hub38 = n_p15 + n_p31;   // level 6
    wire signed [12:0] n_p39 = n_hub38 - (n_p21 <<< 1);   // level 7
    wire signed [12:0] n_p40 = (n_p5 <<< 1) - n_hub38;   // level 7
    wire signed [12:0] n_p41 = (n_p15 <<< 1) - n_p39;   // level 8
    wire signed [12:0] n_p42 = n_p40 + (n_p31 <<< 1);   // level 8
    wire signed [12:0] n_hub43 = n_p13 + n_p29;   // level 6
    wire signed [12:0] n_p44 = n_hub43 + (n_p25 <<< 1);   // level 7
    wire signed [12:0] n_p45 = n_hub43 - (n_p9 <<< 1);   // level 7
    wire signed [12:0] n_p46 = (n_p13 <<< 1) - n_p44;   // level 8
    wire signed [12:0] n_p47 = n_p45 - (n_p29 <<< 1);   // level 8
    wire signed [12:0] n_hub48 = n_p16 + n_p32;   // level 6
    wire signed [12:0] n_p49 = n_hub48 + (n_p26 <<< 1);   // level 7
    wire signed [12:0] n_p50 = n_hub48 - (n_p10 <<< 1);   // level 7
    wire signed [12:0] n_p51 = (n_p16 <<< 1) - n_p49;   // level 8
    wire signed [12:0] n_p52 = n_p50 - (n_p32 <<< 1);   // level 8
    wire signed [12:0] o0 = n_p36;
    wire signed [12:0] o1 = n_p41;
    wire signed [12:0] o2 = n_p44;
    wire signed [12:0] o3 = n_p49;
    wire signed [12:0] o4 = n_p37;
    wire signed [12:0] o5 = n_p42;
    wire signed [12:0] o6 = n_p45;
    wire signed [12:0] o7 = n_p50;
    wire signed [12:0] o8 = n_p34;
    wire signed [12:0] o9 = n_p39;
    wire signed [12:0] o10 = n_p46;
    wire signed [12:0] o11 = n_p51;
    wire signed [12:0] o12 = n_p35;
    wire signed [12:0] o13 = n_p40;
    wire signed [12:0] o14 = n_p47;
    wire signed [12:0] o15 = n_p52;
    assign out_data = {
        o15, o14, o13, o12, o11, o10, o9, o8,
        o7, o6, o5, o4, o3, o2, o1, o0
    };
    assign out_valid = in_valid;
    wire _unused_clk = clk;
endmodule
`default_nettype wire
