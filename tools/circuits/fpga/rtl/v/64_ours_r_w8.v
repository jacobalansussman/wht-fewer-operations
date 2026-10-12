// Written by gen_rtl.py.  Do not edit by hand.
// 64-point Walsh-Hadamard transform, y_J = sum over i of (-1)^popcount(J & i) * x_i.
// Source circuit: tools/circuits/programs/generated/G_family_64.txt
// This work: the family (3/4) N log2 N + N/4 at 64 points, written by tools/circuits/gen.py.  304 adders.
// Inputs: 64 signed values of 8 bits.  Outputs: 64 signed values of 14 bits.
// Adders 304, depth 12 adder levels, adder bits 3616 (chain bits 3488).
// Variant r: one register stage at the inputs, 1 at the outputs, nothing between.  Latency 2.
// Register bits: 512 at the inputs, 896 at the outputs, 2 valid bits.
`default_nettype none
module wht_64_ours_r_w8 (
    input  wire                 clk,
    input  wire                 in_valid,
    input  wire [511:0] in_data,
    output wire                 out_valid,
    output wire [895:0] out_data
);
    reg  signed [7:0] x0;
    reg  signed [7:0] x1;
    reg  signed [7:0] x2;
    reg  signed [7:0] x3;
    reg  signed [7:0] x4;
    reg  signed [7:0] x5;
    reg  signed [7:0] x6;
    reg  signed [7:0] x7;
    reg  signed [7:0] x8;
    reg  signed [7:0] x9;
    reg  signed [7:0] x10;
    reg  signed [7:0] x11;
    reg  signed [7:0] x12;
    reg  signed [7:0] x13;
    reg  signed [7:0] x14;
    reg  signed [7:0] x15;
    reg  signed [7:0] x16;
    reg  signed [7:0] x17;
    reg  signed [7:0] x18;
    reg  signed [7:0] x19;
    reg  signed [7:0] x20;
    reg  signed [7:0] x21;
    reg  signed [7:0] x22;
    reg  signed [7:0] x23;
    reg  signed [7:0] x24;
    reg  signed [7:0] x25;
    reg  signed [7:0] x26;
    reg  signed [7:0] x27;
    reg  signed [7:0] x28;
    reg  signed [7:0] x29;
    reg  signed [7:0] x30;
    reg  signed [7:0] x31;
    reg  signed [7:0] x32;
    reg  signed [7:0] x33;
    reg  signed [7:0] x34;
    reg  signed [7:0] x35;
    reg  signed [7:0] x36;
    reg  signed [7:0] x37;
    reg  signed [7:0] x38;
    reg  signed [7:0] x39;
    reg  signed [7:0] x40;
    reg  signed [7:0] x41;
    reg  signed [7:0] x42;
    reg  signed [7:0] x43;
    reg  signed [7:0] x44;
    reg  signed [7:0] x45;
    reg  signed [7:0] x46;
    reg  signed [7:0] x47;
    reg  signed [7:0] x48;
    reg  signed [7:0] x49;
    reg  signed [7:0] x50;
    reg  signed [7:0] x51;
    reg  signed [7:0] x52;
    reg  signed [7:0] x53;
    reg  signed [7:0] x54;
    reg  signed [7:0] x55;
    reg  signed [7:0] x56;
    reg  signed [7:0] x57;
    reg  signed [7:0] x58;
    reg  signed [7:0] x59;
    reg  signed [7:0] x60;
    reg  signed [7:0] x61;
    reg  signed [7:0] x62;
    reg  signed [7:0] x63;
    always @(posedge clk) begin
        x0 <= in_data[7:0];
        x1 <= in_data[15:8];
        x2 <= in_data[23:16];
        x3 <= in_data[31:24];
        x4 <= in_data[39:32];
        x5 <= in_data[47:40];
        x6 <= in_data[55:48];
        x7 <= in_data[63:56];
        x8 <= in_data[71:64];
        x9 <= in_data[79:72];
        x10 <= in_data[87:80];
        x11 <= in_data[95:88];
        x12 <= in_data[103:96];
        x13 <= in_data[111:104];
        x14 <= in_data[119:112];
        x15 <= in_data[127:120];
        x16 <= in_data[135:128];
        x17 <= in_data[143:136];
        x18 <= in_data[151:144];
        x19 <= in_data[159:152];
        x20 <= in_data[167:160];
        x21 <= in_data[175:168];
        x22 <= in_data[183:176];
        x23 <= in_data[191:184];
        x24 <= in_data[199:192];
        x25 <= in_data[207:200];
        x26 <= in_data[215:208];
        x27 <= in_data[223:216];
        x28 <= in_data[231:224];
        x29 <= in_data[239:232];
        x30 <= in_data[247:240];
        x31 <= in_data[255:248];
        x32 <= in_data[263:256];
        x33 <= in_data[271:264];
        x34 <= in_data[279:272];
        x35 <= in_data[287:280];
        x36 <= in_data[295:288];
        x37 <= in_data[303:296];
        x38 <= in_data[311:304];
        x39 <= in_data[319:312];
        x40 <= in_data[327:320];
        x41 <= in_data[335:328];
        x42 <= in_data[343:336];
        x43 <= in_data[351:344];
        x44 <= in_data[359:352];
        x45 <= in_data[367:360];
        x46 <= in_data[375:368];
        x47 <= in_data[383:376];
        x48 <= in_data[391:384];
        x49 <= in_data[399:392];
        x50 <= in_data[407:400];
        x51 <= in_data[415:408];
        x52 <= in_data[423:416];
        x53 <= in_data[431:424];
        x54 <= in_data[439:432];
        x55 <= in_data[447:440];
        x56 <= in_data[455:448];
        x57 <= in_data[463:456];
        x58 <= in_data[471:464];
        x59 <= in_data[479:472];
        x60 <= in_data[487:480];
        x61 <= in_data[495:488];
        x62 <= in_data[503:496];
        x63 <= in_data[511:504];
    end
    wire signed [8:0] n_p1 = x0 + x1;   // level 1
    wire signed [8:0] n_p2 = x2 - x3;   // level 1
    wire signed [9:0] n_hub3 = n_p1 - n_p2;   // level 2
    wire signed [9:0] n_p4 = n_hub3 + (x2 <<< 1);   // level 3
    wire signed [9:0] n_p5 = (x0 <<< 1) - n_hub3;   // level 3
    wire signed [8:0] n_p6 = x4 + x5;   // level 1
    wire signed [8:0] n_p7 = x6 - x7;   // level 1
    wire signed [9:0] n_hub8 = n_p6 + n_p7;   // level 2
    wire signed [9:0] n_p9 = n_hub8 - (x6 <<< 1);   // level 3
    wire signed [9:0] n_p10 = (x4 <<< 1) - n_hub8;   // level 3
    wire signed [10:0] n_hub11 = n_p4 - n_p9;   // level 4
    wire signed [10:0] n_p12 = n_hub11 + (n_p6 <<< 1);   // level 5
    wire signed [10:0] n_p13 = (n_p1 <<< 1) - n_hub11;   // level 5
    wire signed [10:0] n_hub14 = n_p5 + n_p10;   // level 4
    wire signed [10:0] n_p15 = n_hub14 + (n_p7 <<< 1);   // level 5
    wire signed [10:0] n_p16 = n_hub14 - (n_p2 <<< 1);   // level 5
    wire signed [8:0] n_p17 = x8 + x9;   // level 1
    wire signed [8:0] n_p18 = x10 - x11;   // level 1
    wire signed [9:0] n_hub19 = n_p17 - n_p18;   // level 2
    wire signed [9:0] n_p20 = n_hub19 + (x10 <<< 1);   // level 3
    wire signed [9:0] n_p21 = (x8 <<< 1) - n_hub19;   // level 3
    wire signed [8:0] n_p22 = x12 + x13;   // level 1
    wire signed [8:0] n_p23 = x14 - x15;   // level 1
    wire signed [9:0] n_hub24 = n_p22 + n_p23;   // level 2
    wire signed [9:0] n_p25 = n_hub24 - (x14 <<< 1);   // level 3
    wire signed [9:0] n_p26 = (x12 <<< 1) - n_hub24;   // level 3
    wire signed [10:0] n_hub27 = n_p20 + n_p25;   // level 4
    wire signed [10:0] n_p28 = n_hub27 - (n_p22 <<< 1);   // level 5
    wire signed [10:0] n_p29 = (n_p17 <<< 1) - n_hub27;   // level 5
    wire signed [10:0] n_hub30 = n_p21 - n_p26;   // level 4
    wire signed [10:0] n_p31 = n_hub30 - (n_p23 <<< 1);   // level 5
    wire signed [10:0] n_p32 = n_hub30 - (n_p18 <<< 1);   // level 5
    wire signed [11:0] n_hub33 = n_p12 - n_p28;   // level 6
    wire signed [11:0] n_p34 = n_hub33 + (n_p20 <<< 1);   // level 7
    wire signed [11:0] n_p35 = (n_p4 <<< 1) - n_hub33;   // level 7
    wire signed [11:0] n_hub36 = n_p15 - n_p31;   // level 6
    wire signed [11:0] n_p37 = n_hub36 + (n_p21 <<< 1);   // level 7
    wire signed [11:0] n_p38 = (n_p5 <<< 1) - n_hub36;   // level 7
    wire signed [11:0] n_hub39 = n_p13 + n_p29;   // level 6
    wire signed [11:0] n_p40 = n_hub39 + (n_p25 <<< 1);   // level 7
    wire signed [11:0] n_p41 = n_hub39 - (n_p9 <<< 1);   // level 7
    wire signed [11:0] n_hub42 = n_p16 + n_p32;   // level 6
    wire signed [11:0] n_p43 = n_hub42 + (n_p26 <<< 1);   // level 7
    wire signed [11:0] n_p44 = n_hub42 - (n_p10 <<< 1);   // level 7
    wire signed [8:0] n_p45 = x16 + x17;   // level 1
    wire signed [8:0] n_p46 = x18 - x19;   // level 1
    wire signed [9:0] n_hub47 = n_p45 - n_p46;   // level 2
    wire signed [9:0] n_p48 = n_hub47 + (x18 <<< 1);   // level 3
    wire signed [9:0] n_p49 = (x16 <<< 1) - n_hub47;   // level 3
    wire signed [8:0] n_p50 = x20 + x21;   // level 1
    wire signed [8:0] n_p51 = x22 - x23;   // level 1
    wire signed [9:0] n_hub52 = n_p50 + n_p51;   // level 2
    wire signed [9:0] n_p53 = n_hub52 - (x22 <<< 1);   // level 3
    wire signed [9:0] n_p54 = (x20 <<< 1) - n_hub52;   // level 3
    wire signed [10:0] n_hub55 = n_p48 - n_p53;   // level 4
    wire signed [10:0] n_p56 = n_hub55 + (n_p50 <<< 1);   // level 5
    wire signed [10:0] n_p57 = (n_p45 <<< 1) - n_hub55;   // level 5
    wire signed [10:0] n_hub58 = n_p49 + n_p54;   // level 4
    wire signed [10:0] n_p59 = n_hub58 + (n_p51 <<< 1);   // level 5
    wire signed [10:0] n_p60 = n_hub58 - (n_p46 <<< 1);   // level 5
    wire signed [8:0] n_p61 = x24 + x25;   // level 1
    wire signed [8:0] n_p62 = x26 - x27;   // level 1
    wire signed [9:0] n_hub63 = n_p61 - n_p62;   // level 2
    wire signed [9:0] n_p64 = n_hub63 + (x26 <<< 1);   // level 3
    wire signed [9:0] n_p65 = (x24 <<< 1) - n_hub63;   // level 3
    wire signed [8:0] n_p66 = x28 + x29;   // level 1
    wire signed [8:0] n_p67 = x30 - x31;   // level 1
    wire signed [9:0] n_hub68 = n_p66 + n_p67;   // level 2
    wire signed [9:0] n_p69 = n_hub68 - (x30 <<< 1);   // level 3
    wire signed [9:0] n_p70 = (x28 <<< 1) - n_hub68;   // level 3
    wire signed [10:0] n_hub71 = n_p64 + n_p69;   // level 4
    wire signed [10:0] n_p72 = n_hub71 - (n_p66 <<< 1);   // level 5
    wire signed [10:0] n_p73 = (n_p61 <<< 1) - n_hub71;   // level 5
    wire signed [10:0] n_hub74 = n_p65 - n_p70;   // level 4
    wire signed [10:0] n_p75 = n_hub74 - (n_p67 <<< 1);   // level 5
    wire signed [10:0] n_p76 = n_hub74 - (n_p62 <<< 1);   // level 5
    wire signed [11:0] n_hub77 = n_p56 + n_p72;   // level 6
    wire signed [11:0] n_p78 = n_hub77 - (n_p64 <<< 1);   // level 7
    wire signed [11:0] n_p79 = (n_p48 <<< 1) - n_hub77;   // level 7
    wire signed [11:0] n_hub80 = n_p59 + n_p75;   // level 6
    wire signed [11:0] n_p81 = n_hub80 - (n_p65 <<< 1);   // level 7
    wire signed [11:0] n_p82 = (n_p49 <<< 1) - n_hub80;   // level 7
    wire signed [11:0] n_hub83 = n_p57 - n_p73;   // level 6
    wire signed [11:0] n_p84 = n_hub83 - (n_p69 <<< 1);   // level 7
    wire signed [11:0] n_p85 = n_hub83 - (n_p53 <<< 1);   // level 7
    wire signed [11:0] n_hub86 = n_p60 - n_p76;   // level 6
    wire signed [11:0] n_p87 = n_hub86 - (n_p70 <<< 1);   // level 7
    wire signed [11:0] n_p88 = n_hub86 - (n_p54 <<< 1);   // level 7
    wire signed [12:0] n_hub89 = n_p34 - n_p78;   // level 8
    wire signed [12:0] n_p90 = n_hub89 + (n_p56 <<< 1);   // level 9
    wire signed [12:0] n_p91 = (n_p12 <<< 1) - n_hub89;   // level 9
    wire signed [12:0] n_hub92 = n_p37 - n_p81;   // level 8
    wire signed [12:0] n_p93 = n_hub92 + (n_p59 <<< 1);   // level 9
    wire signed [12:0] n_p94 = (n_p15 <<< 1) - n_hub92;   // level 9
    wire signed [12:0] n_hub95 = n_p40 - n_p84;   // level 8
    wire signed [12:0] n_p96 = n_hub95 + (n_p57 <<< 1);   // level 9
    wire signed [12:0] n_p97 = (n_p13 <<< 1) - n_hub95;   // level 9
    wire signed [12:0] n_hub98 = n_p43 - n_p87;   // level 8
    wire signed [12:0] n_p99 = n_hub98 + (n_p60 <<< 1);   // level 9
    wire signed [12:0] n_p100 = (n_p16 <<< 1) - n_hub98;   // level 9
    wire signed [12:0] n_hub101 = n_p35 + n_p79;   // level 8
    wire signed [12:0] n_p102 = n_hub101 + (n_p72 <<< 1);   // level 9
    wire signed [12:0] n_p103 = n_hub101 - (n_p28 <<< 1);   // level 9
    wire signed [12:0] n_hub104 = n_p38 + n_p82;   // level 8
    wire signed [12:0] n_p105 = n_hub104 + (n_p75 <<< 1);   // level 9
    wire signed [12:0] n_p106 = n_hub104 - (n_p31 <<< 1);   // level 9
    wire signed [12:0] n_hub107 = n_p41 + n_p85;   // level 8
    wire signed [12:0] n_p108 = n_hub107 + (n_p73 <<< 1);   // level 9
    wire signed [12:0] n_p109 = n_hub107 - (n_p29 <<< 1);   // level 9
    wire signed [12:0] n_hub110 = n_p44 + n_p88;   // level 8
    wire signed [12:0] n_p111 = n_hub110 + (n_p76 <<< 1);   // level 9
    wire signed [12:0] n_p112 = n_hub110 - (n_p32 <<< 1);   // level 9
    wire signed [8:0] n_p113 = x32 + x33;   // level 1
    wire signed [8:0] n_p114 = x34 - x35;   // level 1
    wire signed [9:0] n_hub115 = n_p113 - n_p114;   // level 2
    wire signed [9:0] n_p116 = n_hub115 + (x34 <<< 1);   // level 3
    wire signed [9:0] n_p117 = (x32 <<< 1) - n_hub115;   // level 3
    wire signed [8:0] n_p118 = x36 + x37;   // level 1
    wire signed [8:0] n_p119 = x38 - x39;   // level 1
    wire signed [9:0] n_hub120 = n_p118 + n_p119;   // level 2
    wire signed [9:0] n_p121 = n_hub120 - (x38 <<< 1);   // level 3
    wire signed [9:0] n_p122 = (x36 <<< 1) - n_hub120;   // level 3
    wire signed [10:0] n_hub123 = n_p116 - n_p121;   // level 4
    wire signed [10:0] n_p124 = n_hub123 + (n_p118 <<< 1);   // level 5
    wire signed [10:0] n_p125 = (n_p113 <<< 1) - n_hub123;   // level 5
    wire signed [10:0] n_hub126 = n_p117 + n_p122;   // level 4
    wire signed [10:0] n_p127 = n_hub126 + (n_p119 <<< 1);   // level 5
    wire signed [10:0] n_p128 = n_hub126 - (n_p114 <<< 1);   // level 5
    wire signed [8:0] n_p129 = x40 + x41;   // level 1
    wire signed [8:0] n_p130 = x42 - x43;   // level 1
    wire signed [9:0] n_hub131 = n_p129 - n_p130;   // level 2
    wire signed [9:0] n_p132 = n_hub131 + (x42 <<< 1);   // level 3
    wire signed [9:0] n_p133 = (x40 <<< 1) - n_hub131;   // level 3
    wire signed [8:0] n_p134 = x44 + x45;   // level 1
    wire signed [8:0] n_p135 = x46 - x47;   // level 1
    wire signed [9:0] n_hub136 = n_p134 + n_p135;   // level 2
    wire signed [9:0] n_p137 = n_hub136 - (x46 <<< 1);   // level 3
    wire signed [9:0] n_p138 = (x44 <<< 1) - n_hub136;   // level 3
    wire signed [10:0] n_hub139 = n_p132 + n_p137;   // level 4
    wire signed [10:0] n_p140 = n_hub139 - (n_p134 <<< 1);   // level 5
    wire signed [10:0] n_p141 = (n_p129 <<< 1) - n_hub139;   // level 5
    wire signed [10:0] n_hub142 = n_p133 - n_p138;   // level 4
    wire signed [10:0] n_p143 = n_hub142 - (n_p135 <<< 1);   // level 5
    wire signed [10:0] n_p144 = n_hub142 - (n_p130 <<< 1);   // level 5
    wire signed [11:0] n_hub145 = n_p124 - n_p140;   // level 6
    wire signed [11:0] n_p146 = n_hub145 + (n_p132 <<< 1);   // level 7
    wire signed [11:0] n_p147 = (n_p116 <<< 1) - n_hub145;   // level 7
    wire signed [11:0] n_hub148 = n_p127 - n_p143;   // level 6
    wire signed [11:0] n_p149 = n_hub148 + (n_p133 <<< 1);   // level 7
    wire signed [11:0] n_p150 = (n_p117 <<< 1) - n_hub148;   // level 7
    wire signed [11:0] n_hub151 = n_p125 + n_p141;   // level 6
    wire signed [11:0] n_p152 = n_hub151 + (n_p137 <<< 1);   // level 7
    wire signed [11:0] n_p153 = n_hub151 - (n_p121 <<< 1);   // level 7
    wire signed [11:0] n_hub154 = n_p128 + n_p144;   // level 6
    wire signed [11:0] n_p155 = n_hub154 + (n_p138 <<< 1);   // level 7
    wire signed [11:0] n_p156 = n_hub154 - (n_p122 <<< 1);   // level 7
    wire signed [8:0] n_p157 = x48 + x49;   // level 1
    wire signed [8:0] n_p158 = x50 - x51;   // level 1
    wire signed [9:0] n_hub159 = n_p157 - n_p158;   // level 2
    wire signed [9:0] n_p160 = n_hub159 + (x50 <<< 1);   // level 3
    wire signed [9:0] n_p161 = (x48 <<< 1) - n_hub159;   // level 3
    wire signed [8:0] n_p162 = x52 + x53;   // level 1
    wire signed [8:0] n_p163 = x54 - x55;   // level 1
    wire signed [9:0] n_hub164 = n_p162 + n_p163;   // level 2
    wire signed [9:0] n_p165 = n_hub164 - (x54 <<< 1);   // level 3
    wire signed [9:0] n_p166 = (x52 <<< 1) - n_hub164;   // level 3
    wire signed [10:0] n_hub167 = n_p160 - n_p165;   // level 4
    wire signed [10:0] n_p168 = n_hub167 + (n_p162 <<< 1);   // level 5
    wire signed [10:0] n_p169 = (n_p157 <<< 1) - n_hub167;   // level 5
    wire signed [10:0] n_hub170 = n_p161 + n_p166;   // level 4
    wire signed [10:0] n_p171 = n_hub170 + (n_p163 <<< 1);   // level 5
    wire signed [10:0] n_p172 = n_hub170 - (n_p158 <<< 1);   // level 5
    wire signed [8:0] n_p173 = x56 + x57;   // level 1
    wire signed [8:0] n_p174 = x58 - x59;   // level 1
    wire signed [9:0] n_hub175 = n_p173 - n_p174;   // level 2
    wire signed [9:0] n_p176 = n_hub175 + (x58 <<< 1);   // level 3
    wire signed [9:0] n_p177 = (x56 <<< 1) - n_hub175;   // level 3
    wire signed [8:0] n_p178 = x60 + x61;   // level 1
    wire signed [8:0] n_p179 = x62 - x63;   // level 1
    wire signed [9:0] n_hub180 = n_p178 + n_p179;   // level 2
    wire signed [9:0] n_p181 = n_hub180 - (x62 <<< 1);   // level 3
    wire signed [9:0] n_p182 = (x60 <<< 1) - n_hub180;   // level 3
    wire signed [10:0] n_hub183 = n_p176 + n_p181;   // level 4
    wire signed [10:0] n_p184 = n_hub183 - (n_p178 <<< 1);   // level 5
    wire signed [10:0] n_p185 = (n_p173 <<< 1) - n_hub183;   // level 5
    wire signed [10:0] n_hub186 = n_p177 - n_p182;   // level 4
    wire signed [10:0] n_p187 = n_hub186 - (n_p179 <<< 1);   // level 5
    wire signed [10:0] n_p188 = n_hub186 - (n_p174 <<< 1);   // level 5
    wire signed [11:0] n_hub189 = n_p168 + n_p184;   // level 6
    wire signed [11:0] n_p190 = n_hub189 - (n_p176 <<< 1);   // level 7
    wire signed [11:0] n_p191 = (n_p160 <<< 1) - n_hub189;   // level 7
    wire signed [11:0] n_hub192 = n_p171 + n_p187;   // level 6
    wire signed [11:0] n_p193 = n_hub192 - (n_p177 <<< 1);   // level 7
    wire signed [11:0] n_p194 = (n_p161 <<< 1) - n_hub192;   // level 7
    wire signed [11:0] n_hub195 = n_p169 - n_p185;   // level 6
    wire signed [11:0] n_p196 = n_hub195 - (n_p181 <<< 1);   // level 7
    wire signed [11:0] n_p197 = n_hub195 - (n_p165 <<< 1);   // level 7
    wire signed [11:0] n_hub198 = n_p172 - n_p188;   // level 6
    wire signed [11:0] n_p199 = n_hub198 - (n_p182 <<< 1);   // level 7
    wire signed [11:0] n_p200 = n_hub198 - (n_p166 <<< 1);   // level 7
    wire signed [12:0] n_hub201 = n_p146 + n_p190;   // level 8
    wire signed [12:0] n_p202 = n_hub201 - (n_p168 <<< 1);   // level 9
    wire signed [12:0] n_p203 = (n_p124 <<< 1) - n_hub201;   // level 9
    wire signed [12:0] n_hub204 = n_p149 + n_p193;   // level 8
    wire signed [12:0] n_p205 = n_hub204 - (n_p171 <<< 1);   // level 9
    wire signed [12:0] n_p206 = (n_p127 <<< 1) - n_hub204;   // level 9
    wire signed [12:0] n_hub207 = n_p152 + n_p196;   // level 8
    wire signed [12:0] n_p208 = n_hub207 - (n_p169 <<< 1);   // level 9
    wire signed [12:0] n_p209 = (n_p125 <<< 1) - n_hub207;   // level 9
    wire signed [12:0] n_hub210 = n_p155 + n_p199;   // level 8
    wire signed [12:0] n_p211 = n_hub210 - (n_p172 <<< 1);   // level 9
    wire signed [12:0] n_p212 = (n_p128 <<< 1) - n_hub210;   // level 9
    wire signed [12:0] n_hub213 = n_p147 - n_p191;   // level 8
    wire signed [12:0] n_p214 = n_hub213 - (n_p184 <<< 1);   // level 9
    wire signed [12:0] n_p215 = n_hub213 - (n_p140 <<< 1);   // level 9
    wire signed [12:0] n_hub216 = n_p150 - n_p194;   // level 8
    wire signed [12:0] n_p217 = n_hub216 - (n_p187 <<< 1);   // level 9
    wire signed [12:0] n_p218 = n_hub216 - (n_p143 <<< 1);   // level 9
    wire signed [12:0] n_hub219 = n_p153 - n_p197;   // level 8
    wire signed [12:0] n_p220 = n_hub219 - (n_p185 <<< 1);   // level 9
    wire signed [12:0] n_p221 = n_hub219 - (n_p141 <<< 1);   // level 9
    wire signed [12:0] n_hub222 = n_p156 - n_p200;   // level 8
    wire signed [12:0] n_p223 = n_hub222 - (n_p188 <<< 1);   // level 9
    wire signed [12:0] n_p224 = n_hub222 - (n_p144 <<< 1);   // level 9
    wire signed [13:0] n_hub225 = n_p90 + n_p202;   // level 10
    wire signed [13:0] n_p226 = n_hub225 - (n_p146 <<< 1);   // level 11
    wire signed [13:0] n_p227 = (n_p34 <<< 1) - n_hub225;   // level 11
    wire signed [13:0] n_p228 = (n_p90 <<< 1) - n_p226;   // level 12
    wire signed [13:0] n_p229 = n_p227 + (n_p202 <<< 1);   // level 12
    wire signed [13:0] n_hub230 = n_p93 + n_p205;   // level 10
    wire signed [13:0] n_p231 = n_hub230 - (n_p149 <<< 1);   // level 11
    wire signed [13:0] n_p232 = (n_p37 <<< 1) - n_hub230;   // level 11
    wire signed [13:0] n_p233 = (n_p93 <<< 1) - n_p231;   // level 12
    wire signed [13:0] n_p234 = n_p232 + (n_p205 <<< 1);   // level 12
    wire signed [13:0] n_hub235 = n_p96 + n_p208;   // level 10
    wire signed [13:0] n_p236 = n_hub235 - (n_p152 <<< 1);   // level 11
    wire signed [13:0] n_p237 = (n_p40 <<< 1) - n_hub235;   // level 11
    wire signed [13:0] n_p238 = (n_p96 <<< 1) - n_p236;   // level 12
    wire signed [13:0] n_p239 = n_p237 + (n_p208 <<< 1);   // level 12
    wire signed [13:0] n_hub240 = n_p99 + n_p211;   // level 10
    wire signed [13:0] n_p241 = n_hub240 - (n_p155 <<< 1);   // level 11
    wire signed [13:0] n_p242 = (n_p43 <<< 1) - n_hub240;   // level 11
    wire signed [13:0] n_p243 = (n_p99 <<< 1) - n_p241;   // level 12
    wire signed [13:0] n_p244 = n_p242 + (n_p211 <<< 1);   // level 12
    wire signed [13:0] n_hub245 = n_p102 + n_p214;   // level 10
    wire signed [13:0] n_p246 = n_hub245 - (n_p147 <<< 1);   // level 11
    wire signed [13:0] n_p247 = (n_p35 <<< 1) - n_hub245;   // level 11
    wire signed [13:0] n_p248 = (n_p102 <<< 1) - n_p246;   // level 12
    wire signed [13:0] n_p249 = n_p247 + (n_p214 <<< 1);   // level 12
    wire signed [13:0] n_hub250 = n_p105 + n_p217;   // level 10
    wire signed [13:0] n_p251 = n_hub250 - (n_p150 <<< 1);   // level 11
    wire signed [13:0] n_p252 = (n_p38 <<< 1) - n_hub250;   // level 11
    wire signed [13:0] n_p253 = (n_p105 <<< 1) - n_p251;   // level 12
    wire signed [13:0] n_p254 = n_p252 + (n_p217 <<< 1);   // level 12
    wire signed [13:0] n_hub255 = n_p108 + n_p220;   // level 10
    wire signed [13:0] n_p256 = n_hub255 - (n_p153 <<< 1);   // level 11
    wire signed [13:0] n_p257 = (n_p41 <<< 1) - n_hub255;   // level 11
    wire signed [13:0] n_p258 = (n_p108 <<< 1) - n_p256;   // level 12
    wire signed [13:0] n_p259 = n_p257 + (n_p220 <<< 1);   // level 12
    wire signed [13:0] n_hub260 = n_p111 + n_p223;   // level 10
    wire signed [13:0] n_p261 = n_hub260 - (n_p156 <<< 1);   // level 11
    wire signed [13:0] n_p262 = (n_p44 <<< 1) - n_hub260;   // level 11
    wire signed [13:0] n_p263 = (n_p111 <<< 1) - n_p261;   // level 12
    wire signed [13:0] n_p264 = n_p262 + (n_p223 <<< 1);   // level 12
    wire signed [13:0] n_hub265 = n_p91 + n_p203;   // level 10
    wire signed [13:0] n_p266 = n_hub265 + (n_p190 <<< 1);   // level 11
    wire signed [13:0] n_p267 = n_hub265 - (n_p78 <<< 1);   // level 11
    wire signed [13:0] n_p268 = (n_p91 <<< 1) - n_p266;   // level 12
    wire signed [13:0] n_p269 = n_p267 - (n_p203 <<< 1);   // level 12
    wire signed [13:0] n_hub270 = n_p94 + n_p206;   // level 10
    wire signed [13:0] n_p271 = n_hub270 + (n_p193 <<< 1);   // level 11
    wire signed [13:0] n_p272 = n_hub270 - (n_p81 <<< 1);   // level 11
    wire signed [13:0] n_p273 = (n_p94 <<< 1) - n_p271;   // level 12
    wire signed [13:0] n_p274 = n_p272 - (n_p206 <<< 1);   // level 12
    wire signed [13:0] n_hub275 = n_p97 + n_p209;   // level 10
    wire signed [13:0] n_p276 = n_hub275 + (n_p196 <<< 1);   // level 11
    wire signed [13:0] n_p277 = n_hub275 - (n_p84 <<< 1);   // level 11
    wire signed [13:0] n_p278 = (n_p97 <<< 1) - n_p276;   // level 12
    wire signed [13:0] n_p279 = n_p277 - (n_p209 <<< 1);   // level 12
    wire signed [13:0] n_hub280 = n_p100 + n_p212;   // level 10
    wire signed [13:0] n_p281 = n_hub280 + (n_p199 <<< 1);   // level 11
    wire signed [13:0] n_p282 = n_hub280 - (n_p87 <<< 1);   // level 11
    wire signed [13:0] n_p283 = (n_p100 <<< 1) - n_p281;   // level 12
    wire signed [13:0] n_p284 = n_p282 - (n_p212 <<< 1);   // level 12
    wire signed [13:0] n_hub285 = n_p103 + n_p215;   // level 10
    wire signed [13:0] n_p286 = n_hub285 + (n_p191 <<< 1);   // level 11
    wire signed [13:0] n_p287 = n_hub285 - (n_p79 <<< 1);   // level 11
    wire signed [13:0] n_p288 = (n_p103 <<< 1) - n_p286;   // level 12
    wire signed [13:0] n_p289 = n_p287 - (n_p215 <<< 1);   // level 12
    wire signed [13:0] n_hub290 = n_p106 + n_p218;   // level 10
    wire signed [13:0] n_p291 = n_hub290 + (n_p194 <<< 1);   // level 11
    wire signed [13:0] n_p292 = n_hub290 - (n_p82 <<< 1);   // level 11
    wire signed [13:0] n_p293 = (n_p106 <<< 1) - n_p291;   // level 12
    wire signed [13:0] n_p294 = n_p292 - (n_p218 <<< 1);   // level 12
    wire signed [13:0] n_hub295 = n_p109 + n_p221;   // level 10
    wire signed [13:0] n_p296 = n_hub295 + (n_p197 <<< 1);   // level 11
    wire signed [13:0] n_p297 = n_hub295 - (n_p85 <<< 1);   // level 11
    wire signed [13:0] n_p298 = (n_p109 <<< 1) - n_p296;   // level 12
    wire signed [13:0] n_p299 = n_p297 - (n_p221 <<< 1);   // level 12
    wire signed [13:0] n_hub300 = n_p112 + n_p224;   // level 10
    wire signed [13:0] n_p301 = n_hub300 + (n_p200 <<< 1);   // level 11
    wire signed [13:0] n_p302 = n_hub300 - (n_p88 <<< 1);   // level 11
    wire signed [13:0] n_p303 = (n_p112 <<< 1) - n_p301;   // level 12
    wire signed [13:0] n_p304 = n_p302 - (n_p224 <<< 1);   // level 12
    wire signed [13:0] o0 = n_p228;
    wire signed [13:0] o1 = n_p233;
    wire signed [13:0] o2 = n_p238;
    wire signed [13:0] o3 = n_p243;
    wire signed [13:0] o4 = n_p248;
    wire signed [13:0] o5 = n_p253;
    wire signed [13:0] o6 = n_p258;
    wire signed [13:0] o7 = n_p263;
    wire signed [13:0] o8 = n_p266;
    wire signed [13:0] o9 = n_p271;
    wire signed [13:0] o10 = n_p276;
    wire signed [13:0] o11 = n_p281;
    wire signed [13:0] o12 = n_p286;
    wire signed [13:0] o13 = n_p291;
    wire signed [13:0] o14 = n_p296;
    wire signed [13:0] o15 = n_p301;
    wire signed [13:0] o16 = n_p229;
    wire signed [13:0] o17 = n_p234;
    wire signed [13:0] o18 = n_p239;
    wire signed [13:0] o19 = n_p244;
    wire signed [13:0] o20 = n_p249;
    wire signed [13:0] o21 = n_p254;
    wire signed [13:0] o22 = n_p259;
    wire signed [13:0] o23 = n_p264;
    wire signed [13:0] o24 = n_p267;
    wire signed [13:0] o25 = n_p272;
    wire signed [13:0] o26 = n_p277;
    wire signed [13:0] o27 = n_p282;
    wire signed [13:0] o28 = n_p287;
    wire signed [13:0] o29 = n_p292;
    wire signed [13:0] o30 = n_p297;
    wire signed [13:0] o31 = n_p302;
    wire signed [13:0] o32 = n_p226;
    wire signed [13:0] o33 = n_p231;
    wire signed [13:0] o34 = n_p236;
    wire signed [13:0] o35 = n_p241;
    wire signed [13:0] o36 = n_p246;
    wire signed [13:0] o37 = n_p251;
    wire signed [13:0] o38 = n_p256;
    wire signed [13:0] o39 = n_p261;
    wire signed [13:0] o40 = n_p268;
    wire signed [13:0] o41 = n_p273;
    wire signed [13:0] o42 = n_p278;
    wire signed [13:0] o43 = n_p283;
    wire signed [13:0] o44 = n_p288;
    wire signed [13:0] o45 = n_p293;
    wire signed [13:0] o46 = n_p298;
    wire signed [13:0] o47 = n_p303;
    wire signed [13:0] o48 = n_p227;
    wire signed [13:0] o49 = n_p232;
    wire signed [13:0] o50 = n_p237;
    wire signed [13:0] o51 = n_p242;
    wire signed [13:0] o52 = n_p247;
    wire signed [13:0] o53 = n_p252;
    wire signed [13:0] o54 = n_p257;
    wire signed [13:0] o55 = n_p262;
    wire signed [13:0] o56 = n_p269;
    wire signed [13:0] o57 = n_p274;
    wire signed [13:0] o58 = n_p279;
    wire signed [13:0] o59 = n_p284;
    wire signed [13:0] o60 = n_p289;
    wire signed [13:0] o61 = n_p294;
    wire signed [13:0] o62 = n_p299;
    wire signed [13:0] o63 = n_p304;
    wire [895:0] out_comb = {
        o63, o62, o61, o60, o59, o58, o57, o56,
        o55, o54, o53, o52, o51, o50, o49, o48,
        o47, o46, o45, o44, o43, o42, o41, o40,
        o39, o38, o37, o36, o35, o34, o33, o32,
        o31, o30, o29, o28, o27, o26, o25, o24,
        o23, o22, o21, o20, o19, o18, o17, o16,
        o15, o14, o13, o12, o11, o10, o9, o8,
        o7, o6, o5, o4, o3, o2, o1, o0
    };
    reg  [895:0] out_q1;
    reg  [1:0] vld = 2'd0;
    always @(posedge clk) begin
        out_q1 <= out_comb;
        vld <= {vld[0:0], in_valid};
    end
    assign out_data = out_q1;
    assign out_valid = vld[1];
endmodule
`default_nettype wire
