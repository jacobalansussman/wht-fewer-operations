// Written by gen_rtl.py.  Do not edit by hand.
// 64-point Walsh-Hadamard transform written from the definition:
// y_J = sum over i of (-1)^popcount(J & i) * x_i, one expression per output, 14 bits.
// A reference for the equivalence proofs; not a design to be measured.
`default_nettype none
module wht_64_def_c_w8 (
    input  wire                 clk,
    input  wire                 in_valid,
    input  wire [511:0] in_data,
    output wire                 out_valid,
    output wire [895:0] out_data
);
    wire signed [13:0] x0 = $signed(in_data[7:0]);
    wire signed [13:0] x1 = $signed(in_data[15:8]);
    wire signed [13:0] x2 = $signed(in_data[23:16]);
    wire signed [13:0] x3 = $signed(in_data[31:24]);
    wire signed [13:0] x4 = $signed(in_data[39:32]);
    wire signed [13:0] x5 = $signed(in_data[47:40]);
    wire signed [13:0] x6 = $signed(in_data[55:48]);
    wire signed [13:0] x7 = $signed(in_data[63:56]);
    wire signed [13:0] x8 = $signed(in_data[71:64]);
    wire signed [13:0] x9 = $signed(in_data[79:72]);
    wire signed [13:0] x10 = $signed(in_data[87:80]);
    wire signed [13:0] x11 = $signed(in_data[95:88]);
    wire signed [13:0] x12 = $signed(in_data[103:96]);
    wire signed [13:0] x13 = $signed(in_data[111:104]);
    wire signed [13:0] x14 = $signed(in_data[119:112]);
    wire signed [13:0] x15 = $signed(in_data[127:120]);
    wire signed [13:0] x16 = $signed(in_data[135:128]);
    wire signed [13:0] x17 = $signed(in_data[143:136]);
    wire signed [13:0] x18 = $signed(in_data[151:144]);
    wire signed [13:0] x19 = $signed(in_data[159:152]);
    wire signed [13:0] x20 = $signed(in_data[167:160]);
    wire signed [13:0] x21 = $signed(in_data[175:168]);
    wire signed [13:0] x22 = $signed(in_data[183:176]);
    wire signed [13:0] x23 = $signed(in_data[191:184]);
    wire signed [13:0] x24 = $signed(in_data[199:192]);
    wire signed [13:0] x25 = $signed(in_data[207:200]);
    wire signed [13:0] x26 = $signed(in_data[215:208]);
    wire signed [13:0] x27 = $signed(in_data[223:216]);
    wire signed [13:0] x28 = $signed(in_data[231:224]);
    wire signed [13:0] x29 = $signed(in_data[239:232]);
    wire signed [13:0] x30 = $signed(in_data[247:240]);
    wire signed [13:0] x31 = $signed(in_data[255:248]);
    wire signed [13:0] x32 = $signed(in_data[263:256]);
    wire signed [13:0] x33 = $signed(in_data[271:264]);
    wire signed [13:0] x34 = $signed(in_data[279:272]);
    wire signed [13:0] x35 = $signed(in_data[287:280]);
    wire signed [13:0] x36 = $signed(in_data[295:288]);
    wire signed [13:0] x37 = $signed(in_data[303:296]);
    wire signed [13:0] x38 = $signed(in_data[311:304]);
    wire signed [13:0] x39 = $signed(in_data[319:312]);
    wire signed [13:0] x40 = $signed(in_data[327:320]);
    wire signed [13:0] x41 = $signed(in_data[335:328]);
    wire signed [13:0] x42 = $signed(in_data[343:336]);
    wire signed [13:0] x43 = $signed(in_data[351:344]);
    wire signed [13:0] x44 = $signed(in_data[359:352]);
    wire signed [13:0] x45 = $signed(in_data[367:360]);
    wire signed [13:0] x46 = $signed(in_data[375:368]);
    wire signed [13:0] x47 = $signed(in_data[383:376]);
    wire signed [13:0] x48 = $signed(in_data[391:384]);
    wire signed [13:0] x49 = $signed(in_data[399:392]);
    wire signed [13:0] x50 = $signed(in_data[407:400]);
    wire signed [13:0] x51 = $signed(in_data[415:408]);
    wire signed [13:0] x52 = $signed(in_data[423:416]);
    wire signed [13:0] x53 = $signed(in_data[431:424]);
    wire signed [13:0] x54 = $signed(in_data[439:432]);
    wire signed [13:0] x55 = $signed(in_data[447:440]);
    wire signed [13:0] x56 = $signed(in_data[455:448]);
    wire signed [13:0] x57 = $signed(in_data[463:456]);
    wire signed [13:0] x58 = $signed(in_data[471:464]);
    wire signed [13:0] x59 = $signed(in_data[479:472]);
    wire signed [13:0] x60 = $signed(in_data[487:480]);
    wire signed [13:0] x61 = $signed(in_data[495:488]);
    wire signed [13:0] x62 = $signed(in_data[503:496]);
    wire signed [13:0] x63 = $signed(in_data[511:504]);
    wire signed [13:0] o0 = x0 + x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8 + x9 + x10 + x11 + x12 + x13 + x14 + x15 + x16 + x17 + x18 + x19 + x20 + x21 + x22 + x23 + x24 + x25 + x26 + x27 + x28 + x29 + x30 + x31 + x32 + x33 + x34 + x35 + x36 + x37 + x38 + x39 + x40 + x41 + x42 + x43 + x44 + x45 + x46 + x47 + x48 + x49 + x50 + x51 + x52 + x53 + x54 + x55 + x56 + x57 + x58 + x59 + x60 + x61 + x62 + x63;
    wire signed [13:0] o1 = x0 - x1 + x2 - x3 + x4 - x5 + x6 - x7 + x8 - x9 + x10 - x11 + x12 - x13 + x14 - x15 + x16 - x17 + x18 - x19 + x20 - x21 + x22 - x23 + x24 - x25 + x26 - x27 + x28 - x29 + x30 - x31 + x32 - x33 + x34 - x35 + x36 - x37 + x38 - x39 + x40 - x41 + x42 - x43 + x44 - x45 + x46 - x47 + x48 - x49 + x50 - x51 + x52 - x53 + x54 - x55 + x56 - x57 + x58 - x59 + x60 - x61 + x62 - x63;
    wire signed [13:0] o2 = x0 + x1 - x2 - x3 + x4 + x5 - x6 - x7 + x8 + x9 - x10 - x11 + x12 + x13 - x14 - x15 + x16 + x17 - x18 - x19 + x20 + x21 - x22 - x23 + x24 + x25 - x26 - x27 + x28 + x29 - x30 - x31 + x32 + x33 - x34 - x35 + x36 + x37 - x38 - x39 + x40 + x41 - x42 - x43 + x44 + x45 - x46 - x47 + x48 + x49 - x50 - x51 + x52 + x53 - x54 - x55 + x56 + x57 - x58 - x59 + x60 + x61 - x62 - x63;
    wire signed [13:0] o3 = x0 - x1 - x2 + x3 + x4 - x5 - x6 + x7 + x8 - x9 - x10 + x11 + x12 - x13 - x14 + x15 + x16 - x17 - x18 + x19 + x20 - x21 - x22 + x23 + x24 - x25 - x26 + x27 + x28 - x29 - x30 + x31 + x32 - x33 - x34 + x35 + x36 - x37 - x38 + x39 + x40 - x41 - x42 + x43 + x44 - x45 - x46 + x47 + x48 - x49 - x50 + x51 + x52 - x53 - x54 + x55 + x56 - x57 - x58 + x59 + x60 - x61 - x62 + x63;
    wire signed [13:0] o4 = x0 + x1 + x2 + x3 - x4 - x5 - x6 - x7 + x8 + x9 + x10 + x11 - x12 - x13 - x14 - x15 + x16 + x17 + x18 + x19 - x20 - x21 - x22 - x23 + x24 + x25 + x26 + x27 - x28 - x29 - x30 - x31 + x32 + x33 + x34 + x35 - x36 - x37 - x38 - x39 + x40 + x41 + x42 + x43 - x44 - x45 - x46 - x47 + x48 + x49 + x50 + x51 - x52 - x53 - x54 - x55 + x56 + x57 + x58 + x59 - x60 - x61 - x62 - x63;
    wire signed [13:0] o5 = x0 - x1 + x2 - x3 - x4 + x5 - x6 + x7 + x8 - x9 + x10 - x11 - x12 + x13 - x14 + x15 + x16 - x17 + x18 - x19 - x20 + x21 - x22 + x23 + x24 - x25 + x26 - x27 - x28 + x29 - x30 + x31 + x32 - x33 + x34 - x35 - x36 + x37 - x38 + x39 + x40 - x41 + x42 - x43 - x44 + x45 - x46 + x47 + x48 - x49 + x50 - x51 - x52 + x53 - x54 + x55 + x56 - x57 + x58 - x59 - x60 + x61 - x62 + x63;
    wire signed [13:0] o6 = x0 + x1 - x2 - x3 - x4 - x5 + x6 + x7 + x8 + x9 - x10 - x11 - x12 - x13 + x14 + x15 + x16 + x17 - x18 - x19 - x20 - x21 + x22 + x23 + x24 + x25 - x26 - x27 - x28 - x29 + x30 + x31 + x32 + x33 - x34 - x35 - x36 - x37 + x38 + x39 + x40 + x41 - x42 - x43 - x44 - x45 + x46 + x47 + x48 + x49 - x50 - x51 - x52 - x53 + x54 + x55 + x56 + x57 - x58 - x59 - x60 - x61 + x62 + x63;
    wire signed [13:0] o7 = x0 - x1 - x2 + x3 - x4 + x5 + x6 - x7 + x8 - x9 - x10 + x11 - x12 + x13 + x14 - x15 + x16 - x17 - x18 + x19 - x20 + x21 + x22 - x23 + x24 - x25 - x26 + x27 - x28 + x29 + x30 - x31 + x32 - x33 - x34 + x35 - x36 + x37 + x38 - x39 + x40 - x41 - x42 + x43 - x44 + x45 + x46 - x47 + x48 - x49 - x50 + x51 - x52 + x53 + x54 - x55 + x56 - x57 - x58 + x59 - x60 + x61 + x62 - x63;
    wire signed [13:0] o8 = x0 + x1 + x2 + x3 + x4 + x5 + x6 + x7 - x8 - x9 - x10 - x11 - x12 - x13 - x14 - x15 + x16 + x17 + x18 + x19 + x20 + x21 + x22 + x23 - x24 - x25 - x26 - x27 - x28 - x29 - x30 - x31 + x32 + x33 + x34 + x35 + x36 + x37 + x38 + x39 - x40 - x41 - x42 - x43 - x44 - x45 - x46 - x47 + x48 + x49 + x50 + x51 + x52 + x53 + x54 + x55 - x56 - x57 - x58 - x59 - x60 - x61 - x62 - x63;
    wire signed [13:0] o9 = x0 - x1 + x2 - x3 + x4 - x5 + x6 - x7 - x8 + x9 - x10 + x11 - x12 + x13 - x14 + x15 + x16 - x17 + x18 - x19 + x20 - x21 + x22 - x23 - x24 + x25 - x26 + x27 - x28 + x29 - x30 + x31 + x32 - x33 + x34 - x35 + x36 - x37 + x38 - x39 - x40 + x41 - x42 + x43 - x44 + x45 - x46 + x47 + x48 - x49 + x50 - x51 + x52 - x53 + x54 - x55 - x56 + x57 - x58 + x59 - x60 + x61 - x62 + x63;
    wire signed [13:0] o10 = x0 + x1 - x2 - x3 + x4 + x5 - x6 - x7 - x8 - x9 + x10 + x11 - x12 - x13 + x14 + x15 + x16 + x17 - x18 - x19 + x20 + x21 - x22 - x23 - x24 - x25 + x26 + x27 - x28 - x29 + x30 + x31 + x32 + x33 - x34 - x35 + x36 + x37 - x38 - x39 - x40 - x41 + x42 + x43 - x44 - x45 + x46 + x47 + x48 + x49 - x50 - x51 + x52 + x53 - x54 - x55 - x56 - x57 + x58 + x59 - x60 - x61 + x62 + x63;
    wire signed [13:0] o11 = x0 - x1 - x2 + x3 + x4 - x5 - x6 + x7 - x8 + x9 + x10 - x11 - x12 + x13 + x14 - x15 + x16 - x17 - x18 + x19 + x20 - x21 - x22 + x23 - x24 + x25 + x26 - x27 - x28 + x29 + x30 - x31 + x32 - x33 - x34 + x35 + x36 - x37 - x38 + x39 - x40 + x41 + x42 - x43 - x44 + x45 + x46 - x47 + x48 - x49 - x50 + x51 + x52 - x53 - x54 + x55 - x56 + x57 + x58 - x59 - x60 + x61 + x62 - x63;
    wire signed [13:0] o12 = x0 + x1 + x2 + x3 - x4 - x5 - x6 - x7 - x8 - x9 - x10 - x11 + x12 + x13 + x14 + x15 + x16 + x17 + x18 + x19 - x20 - x21 - x22 - x23 - x24 - x25 - x26 - x27 + x28 + x29 + x30 + x31 + x32 + x33 + x34 + x35 - x36 - x37 - x38 - x39 - x40 - x41 - x42 - x43 + x44 + x45 + x46 + x47 + x48 + x49 + x50 + x51 - x52 - x53 - x54 - x55 - x56 - x57 - x58 - x59 + x60 + x61 + x62 + x63;
    wire signed [13:0] o13 = x0 - x1 + x2 - x3 - x4 + x5 - x6 + x7 - x8 + x9 - x10 + x11 + x12 - x13 + x14 - x15 + x16 - x17 + x18 - x19 - x20 + x21 - x22 + x23 - x24 + x25 - x26 + x27 + x28 - x29 + x30 - x31 + x32 - x33 + x34 - x35 - x36 + x37 - x38 + x39 - x40 + x41 - x42 + x43 + x44 - x45 + x46 - x47 + x48 - x49 + x50 - x51 - x52 + x53 - x54 + x55 - x56 + x57 - x58 + x59 + x60 - x61 + x62 - x63;
    wire signed [13:0] o14 = x0 + x1 - x2 - x3 - x4 - x5 + x6 + x7 - x8 - x9 + x10 + x11 + x12 + x13 - x14 - x15 + x16 + x17 - x18 - x19 - x20 - x21 + x22 + x23 - x24 - x25 + x26 + x27 + x28 + x29 - x30 - x31 + x32 + x33 - x34 - x35 - x36 - x37 + x38 + x39 - x40 - x41 + x42 + x43 + x44 + x45 - x46 - x47 + x48 + x49 - x50 - x51 - x52 - x53 + x54 + x55 - x56 - x57 + x58 + x59 + x60 + x61 - x62 - x63;
    wire signed [13:0] o15 = x0 - x1 - x2 + x3 - x4 + x5 + x6 - x7 - x8 + x9 + x10 - x11 + x12 - x13 - x14 + x15 + x16 - x17 - x18 + x19 - x20 + x21 + x22 - x23 - x24 + x25 + x26 - x27 + x28 - x29 - x30 + x31 + x32 - x33 - x34 + x35 - x36 + x37 + x38 - x39 - x40 + x41 + x42 - x43 + x44 - x45 - x46 + x47 + x48 - x49 - x50 + x51 - x52 + x53 + x54 - x55 - x56 + x57 + x58 - x59 + x60 - x61 - x62 + x63;
    wire signed [13:0] o16 = x0 + x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8 + x9 + x10 + x11 + x12 + x13 + x14 + x15 - x16 - x17 - x18 - x19 - x20 - x21 - x22 - x23 - x24 - x25 - x26 - x27 - x28 - x29 - x30 - x31 + x32 + x33 + x34 + x35 + x36 + x37 + x38 + x39 + x40 + x41 + x42 + x43 + x44 + x45 + x46 + x47 - x48 - x49 - x50 - x51 - x52 - x53 - x54 - x55 - x56 - x57 - x58 - x59 - x60 - x61 - x62 - x63;
    wire signed [13:0] o17 = x0 - x1 + x2 - x3 + x4 - x5 + x6 - x7 + x8 - x9 + x10 - x11 + x12 - x13 + x14 - x15 - x16 + x17 - x18 + x19 - x20 + x21 - x22 + x23 - x24 + x25 - x26 + x27 - x28 + x29 - x30 + x31 + x32 - x33 + x34 - x35 + x36 - x37 + x38 - x39 + x40 - x41 + x42 - x43 + x44 - x45 + x46 - x47 - x48 + x49 - x50 + x51 - x52 + x53 - x54 + x55 - x56 + x57 - x58 + x59 - x60 + x61 - x62 + x63;
    wire signed [13:0] o18 = x0 + x1 - x2 - x3 + x4 + x5 - x6 - x7 + x8 + x9 - x10 - x11 + x12 + x13 - x14 - x15 - x16 - x17 + x18 + x19 - x20 - x21 + x22 + x23 - x24 - x25 + x26 + x27 - x28 - x29 + x30 + x31 + x32 + x33 - x34 - x35 + x36 + x37 - x38 - x39 + x40 + x41 - x42 - x43 + x44 + x45 - x46 - x47 - x48 - x49 + x50 + x51 - x52 - x53 + x54 + x55 - x56 - x57 + x58 + x59 - x60 - x61 + x62 + x63;
    wire signed [13:0] o19 = x0 - x1 - x2 + x3 + x4 - x5 - x6 + x7 + x8 - x9 - x10 + x11 + x12 - x13 - x14 + x15 - x16 + x17 + x18 - x19 - x20 + x21 + x22 - x23 - x24 + x25 + x26 - x27 - x28 + x29 + x30 - x31 + x32 - x33 - x34 + x35 + x36 - x37 - x38 + x39 + x40 - x41 - x42 + x43 + x44 - x45 - x46 + x47 - x48 + x49 + x50 - x51 - x52 + x53 + x54 - x55 - x56 + x57 + x58 - x59 - x60 + x61 + x62 - x63;
    wire signed [13:0] o20 = x0 + x1 + x2 + x3 - x4 - x5 - x6 - x7 + x8 + x9 + x10 + x11 - x12 - x13 - x14 - x15 - x16 - x17 - x18 - x19 + x20 + x21 + x22 + x23 - x24 - x25 - x26 - x27 + x28 + x29 + x30 + x31 + x32 + x33 + x34 + x35 - x36 - x37 - x38 - x39 + x40 + x41 + x42 + x43 - x44 - x45 - x46 - x47 - x48 - x49 - x50 - x51 + x52 + x53 + x54 + x55 - x56 - x57 - x58 - x59 + x60 + x61 + x62 + x63;
    wire signed [13:0] o21 = x0 - x1 + x2 - x3 - x4 + x5 - x6 + x7 + x8 - x9 + x10 - x11 - x12 + x13 - x14 + x15 - x16 + x17 - x18 + x19 + x20 - x21 + x22 - x23 - x24 + x25 - x26 + x27 + x28 - x29 + x30 - x31 + x32 - x33 + x34 - x35 - x36 + x37 - x38 + x39 + x40 - x41 + x42 - x43 - x44 + x45 - x46 + x47 - x48 + x49 - x50 + x51 + x52 - x53 + x54 - x55 - x56 + x57 - x58 + x59 + x60 - x61 + x62 - x63;
    wire signed [13:0] o22 = x0 + x1 - x2 - x3 - x4 - x5 + x6 + x7 + x8 + x9 - x10 - x11 - x12 - x13 + x14 + x15 - x16 - x17 + x18 + x19 + x20 + x21 - x22 - x23 - x24 - x25 + x26 + x27 + x28 + x29 - x30 - x31 + x32 + x33 - x34 - x35 - x36 - x37 + x38 + x39 + x40 + x41 - x42 - x43 - x44 - x45 + x46 + x47 - x48 - x49 + x50 + x51 + x52 + x53 - x54 - x55 - x56 - x57 + x58 + x59 + x60 + x61 - x62 - x63;
    wire signed [13:0] o23 = x0 - x1 - x2 + x3 - x4 + x5 + x6 - x7 + x8 - x9 - x10 + x11 - x12 + x13 + x14 - x15 - x16 + x17 + x18 - x19 + x20 - x21 - x22 + x23 - x24 + x25 + x26 - x27 + x28 - x29 - x30 + x31 + x32 - x33 - x34 + x35 - x36 + x37 + x38 - x39 + x40 - x41 - x42 + x43 - x44 + x45 + x46 - x47 - x48 + x49 + x50 - x51 + x52 - x53 - x54 + x55 - x56 + x57 + x58 - x59 + x60 - x61 - x62 + x63;
    wire signed [13:0] o24 = x0 + x1 + x2 + x3 + x4 + x5 + x6 + x7 - x8 - x9 - x10 - x11 - x12 - x13 - x14 - x15 - x16 - x17 - x18 - x19 - x20 - x21 - x22 - x23 + x24 + x25 + x26 + x27 + x28 + x29 + x30 + x31 + x32 + x33 + x34 + x35 + x36 + x37 + x38 + x39 - x40 - x41 - x42 - x43 - x44 - x45 - x46 - x47 - x48 - x49 - x50 - x51 - x52 - x53 - x54 - x55 + x56 + x57 + x58 + x59 + x60 + x61 + x62 + x63;
    wire signed [13:0] o25 = x0 - x1 + x2 - x3 + x4 - x5 + x6 - x7 - x8 + x9 - x10 + x11 - x12 + x13 - x14 + x15 - x16 + x17 - x18 + x19 - x20 + x21 - x22 + x23 + x24 - x25 + x26 - x27 + x28 - x29 + x30 - x31 + x32 - x33 + x34 - x35 + x36 - x37 + x38 - x39 - x40 + x41 - x42 + x43 - x44 + x45 - x46 + x47 - x48 + x49 - x50 + x51 - x52 + x53 - x54 + x55 + x56 - x57 + x58 - x59 + x60 - x61 + x62 - x63;
    wire signed [13:0] o26 = x0 + x1 - x2 - x3 + x4 + x5 - x6 - x7 - x8 - x9 + x10 + x11 - x12 - x13 + x14 + x15 - x16 - x17 + x18 + x19 - x20 - x21 + x22 + x23 + x24 + x25 - x26 - x27 + x28 + x29 - x30 - x31 + x32 + x33 - x34 - x35 + x36 + x37 - x38 - x39 - x40 - x41 + x42 + x43 - x44 - x45 + x46 + x47 - x48 - x49 + x50 + x51 - x52 - x53 + x54 + x55 + x56 + x57 - x58 - x59 + x60 + x61 - x62 - x63;
    wire signed [13:0] o27 = x0 - x1 - x2 + x3 + x4 - x5 - x6 + x7 - x8 + x9 + x10 - x11 - x12 + x13 + x14 - x15 - x16 + x17 + x18 - x19 - x20 + x21 + x22 - x23 + x24 - x25 - x26 + x27 + x28 - x29 - x30 + x31 + x32 - x33 - x34 + x35 + x36 - x37 - x38 + x39 - x40 + x41 + x42 - x43 - x44 + x45 + x46 - x47 - x48 + x49 + x50 - x51 - x52 + x53 + x54 - x55 + x56 - x57 - x58 + x59 + x60 - x61 - x62 + x63;
    wire signed [13:0] o28 = x0 + x1 + x2 + x3 - x4 - x5 - x6 - x7 - x8 - x9 - x10 - x11 + x12 + x13 + x14 + x15 - x16 - x17 - x18 - x19 + x20 + x21 + x22 + x23 + x24 + x25 + x26 + x27 - x28 - x29 - x30 - x31 + x32 + x33 + x34 + x35 - x36 - x37 - x38 - x39 - x40 - x41 - x42 - x43 + x44 + x45 + x46 + x47 - x48 - x49 - x50 - x51 + x52 + x53 + x54 + x55 + x56 + x57 + x58 + x59 - x60 - x61 - x62 - x63;
    wire signed [13:0] o29 = x0 - x1 + x2 - x3 - x4 + x5 - x6 + x7 - x8 + x9 - x10 + x11 + x12 - x13 + x14 - x15 - x16 + x17 - x18 + x19 + x20 - x21 + x22 - x23 + x24 - x25 + x26 - x27 - x28 + x29 - x30 + x31 + x32 - x33 + x34 - x35 - x36 + x37 - x38 + x39 - x40 + x41 - x42 + x43 + x44 - x45 + x46 - x47 - x48 + x49 - x50 + x51 + x52 - x53 + x54 - x55 + x56 - x57 + x58 - x59 - x60 + x61 - x62 + x63;
    wire signed [13:0] o30 = x0 + x1 - x2 - x3 - x4 - x5 + x6 + x7 - x8 - x9 + x10 + x11 + x12 + x13 - x14 - x15 - x16 - x17 + x18 + x19 + x20 + x21 - x22 - x23 + x24 + x25 - x26 - x27 - x28 - x29 + x30 + x31 + x32 + x33 - x34 - x35 - x36 - x37 + x38 + x39 - x40 - x41 + x42 + x43 + x44 + x45 - x46 - x47 - x48 - x49 + x50 + x51 + x52 + x53 - x54 - x55 + x56 + x57 - x58 - x59 - x60 - x61 + x62 + x63;
    wire signed [13:0] o31 = x0 - x1 - x2 + x3 - x4 + x5 + x6 - x7 - x8 + x9 + x10 - x11 + x12 - x13 - x14 + x15 - x16 + x17 + x18 - x19 + x20 - x21 - x22 + x23 + x24 - x25 - x26 + x27 - x28 + x29 + x30 - x31 + x32 - x33 - x34 + x35 - x36 + x37 + x38 - x39 - x40 + x41 + x42 - x43 + x44 - x45 - x46 + x47 - x48 + x49 + x50 - x51 + x52 - x53 - x54 + x55 + x56 - x57 - x58 + x59 - x60 + x61 + x62 - x63;
    wire signed [13:0] o32 = x0 + x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8 + x9 + x10 + x11 + x12 + x13 + x14 + x15 + x16 + x17 + x18 + x19 + x20 + x21 + x22 + x23 + x24 + x25 + x26 + x27 + x28 + x29 + x30 + x31 - x32 - x33 - x34 - x35 - x36 - x37 - x38 - x39 - x40 - x41 - x42 - x43 - x44 - x45 - x46 - x47 - x48 - x49 - x50 - x51 - x52 - x53 - x54 - x55 - x56 - x57 - x58 - x59 - x60 - x61 - x62 - x63;
    wire signed [13:0] o33 = x0 - x1 + x2 - x3 + x4 - x5 + x6 - x7 + x8 - x9 + x10 - x11 + x12 - x13 + x14 - x15 + x16 - x17 + x18 - x19 + x20 - x21 + x22 - x23 + x24 - x25 + x26 - x27 + x28 - x29 + x30 - x31 - x32 + x33 - x34 + x35 - x36 + x37 - x38 + x39 - x40 + x41 - x42 + x43 - x44 + x45 - x46 + x47 - x48 + x49 - x50 + x51 - x52 + x53 - x54 + x55 - x56 + x57 - x58 + x59 - x60 + x61 - x62 + x63;
    wire signed [13:0] o34 = x0 + x1 - x2 - x3 + x4 + x5 - x6 - x7 + x8 + x9 - x10 - x11 + x12 + x13 - x14 - x15 + x16 + x17 - x18 - x19 + x20 + x21 - x22 - x23 + x24 + x25 - x26 - x27 + x28 + x29 - x30 - x31 - x32 - x33 + x34 + x35 - x36 - x37 + x38 + x39 - x40 - x41 + x42 + x43 - x44 - x45 + x46 + x47 - x48 - x49 + x50 + x51 - x52 - x53 + x54 + x55 - x56 - x57 + x58 + x59 - x60 - x61 + x62 + x63;
    wire signed [13:0] o35 = x0 - x1 - x2 + x3 + x4 - x5 - x6 + x7 + x8 - x9 - x10 + x11 + x12 - x13 - x14 + x15 + x16 - x17 - x18 + x19 + x20 - x21 - x22 + x23 + x24 - x25 - x26 + x27 + x28 - x29 - x30 + x31 - x32 + x33 + x34 - x35 - x36 + x37 + x38 - x39 - x40 + x41 + x42 - x43 - x44 + x45 + x46 - x47 - x48 + x49 + x50 - x51 - x52 + x53 + x54 - x55 - x56 + x57 + x58 - x59 - x60 + x61 + x62 - x63;
    wire signed [13:0] o36 = x0 + x1 + x2 + x3 - x4 - x5 - x6 - x7 + x8 + x9 + x10 + x11 - x12 - x13 - x14 - x15 + x16 + x17 + x18 + x19 - x20 - x21 - x22 - x23 + x24 + x25 + x26 + x27 - x28 - x29 - x30 - x31 - x32 - x33 - x34 - x35 + x36 + x37 + x38 + x39 - x40 - x41 - x42 - x43 + x44 + x45 + x46 + x47 - x48 - x49 - x50 - x51 + x52 + x53 + x54 + x55 - x56 - x57 - x58 - x59 + x60 + x61 + x62 + x63;
    wire signed [13:0] o37 = x0 - x1 + x2 - x3 - x4 + x5 - x6 + x7 + x8 - x9 + x10 - x11 - x12 + x13 - x14 + x15 + x16 - x17 + x18 - x19 - x20 + x21 - x22 + x23 + x24 - x25 + x26 - x27 - x28 + x29 - x30 + x31 - x32 + x33 - x34 + x35 + x36 - x37 + x38 - x39 - x40 + x41 - x42 + x43 + x44 - x45 + x46 - x47 - x48 + x49 - x50 + x51 + x52 - x53 + x54 - x55 - x56 + x57 - x58 + x59 + x60 - x61 + x62 - x63;
    wire signed [13:0] o38 = x0 + x1 - x2 - x3 - x4 - x5 + x6 + x7 + x8 + x9 - x10 - x11 - x12 - x13 + x14 + x15 + x16 + x17 - x18 - x19 - x20 - x21 + x22 + x23 + x24 + x25 - x26 - x27 - x28 - x29 + x30 + x31 - x32 - x33 + x34 + x35 + x36 + x37 - x38 - x39 - x40 - x41 + x42 + x43 + x44 + x45 - x46 - x47 - x48 - x49 + x50 + x51 + x52 + x53 - x54 - x55 - x56 - x57 + x58 + x59 + x60 + x61 - x62 - x63;
    wire signed [13:0] o39 = x0 - x1 - x2 + x3 - x4 + x5 + x6 - x7 + x8 - x9 - x10 + x11 - x12 + x13 + x14 - x15 + x16 - x17 - x18 + x19 - x20 + x21 + x22 - x23 + x24 - x25 - x26 + x27 - x28 + x29 + x30 - x31 - x32 + x33 + x34 - x35 + x36 - x37 - x38 + x39 - x40 + x41 + x42 - x43 + x44 - x45 - x46 + x47 - x48 + x49 + x50 - x51 + x52 - x53 - x54 + x55 - x56 + x57 + x58 - x59 + x60 - x61 - x62 + x63;
    wire signed [13:0] o40 = x0 + x1 + x2 + x3 + x4 + x5 + x6 + x7 - x8 - x9 - x10 - x11 - x12 - x13 - x14 - x15 + x16 + x17 + x18 + x19 + x20 + x21 + x22 + x23 - x24 - x25 - x26 - x27 - x28 - x29 - x30 - x31 - x32 - x33 - x34 - x35 - x36 - x37 - x38 - x39 + x40 + x41 + x42 + x43 + x44 + x45 + x46 + x47 - x48 - x49 - x50 - x51 - x52 - x53 - x54 - x55 + x56 + x57 + x58 + x59 + x60 + x61 + x62 + x63;
    wire signed [13:0] o41 = x0 - x1 + x2 - x3 + x4 - x5 + x6 - x7 - x8 + x9 - x10 + x11 - x12 + x13 - x14 + x15 + x16 - x17 + x18 - x19 + x20 - x21 + x22 - x23 - x24 + x25 - x26 + x27 - x28 + x29 - x30 + x31 - x32 + x33 - x34 + x35 - x36 + x37 - x38 + x39 + x40 - x41 + x42 - x43 + x44 - x45 + x46 - x47 - x48 + x49 - x50 + x51 - x52 + x53 - x54 + x55 + x56 - x57 + x58 - x59 + x60 - x61 + x62 - x63;
    wire signed [13:0] o42 = x0 + x1 - x2 - x3 + x4 + x5 - x6 - x7 - x8 - x9 + x10 + x11 - x12 - x13 + x14 + x15 + x16 + x17 - x18 - x19 + x20 + x21 - x22 - x23 - x24 - x25 + x26 + x27 - x28 - x29 + x30 + x31 - x32 - x33 + x34 + x35 - x36 - x37 + x38 + x39 + x40 + x41 - x42 - x43 + x44 + x45 - x46 - x47 - x48 - x49 + x50 + x51 - x52 - x53 + x54 + x55 + x56 + x57 - x58 - x59 + x60 + x61 - x62 - x63;
    wire signed [13:0] o43 = x0 - x1 - x2 + x3 + x4 - x5 - x6 + x7 - x8 + x9 + x10 - x11 - x12 + x13 + x14 - x15 + x16 - x17 - x18 + x19 + x20 - x21 - x22 + x23 - x24 + x25 + x26 - x27 - x28 + x29 + x30 - x31 - x32 + x33 + x34 - x35 - x36 + x37 + x38 - x39 + x40 - x41 - x42 + x43 + x44 - x45 - x46 + x47 - x48 + x49 + x50 - x51 - x52 + x53 + x54 - x55 + x56 - x57 - x58 + x59 + x60 - x61 - x62 + x63;
    wire signed [13:0] o44 = x0 + x1 + x2 + x3 - x4 - x5 - x6 - x7 - x8 - x9 - x10 - x11 + x12 + x13 + x14 + x15 + x16 + x17 + x18 + x19 - x20 - x21 - x22 - x23 - x24 - x25 - x26 - x27 + x28 + x29 + x30 + x31 - x32 - x33 - x34 - x35 + x36 + x37 + x38 + x39 + x40 + x41 + x42 + x43 - x44 - x45 - x46 - x47 - x48 - x49 - x50 - x51 + x52 + x53 + x54 + x55 + x56 + x57 + x58 + x59 - x60 - x61 - x62 - x63;
    wire signed [13:0] o45 = x0 - x1 + x2 - x3 - x4 + x5 - x6 + x7 - x8 + x9 - x10 + x11 + x12 - x13 + x14 - x15 + x16 - x17 + x18 - x19 - x20 + x21 - x22 + x23 - x24 + x25 - x26 + x27 + x28 - x29 + x30 - x31 - x32 + x33 - x34 + x35 + x36 - x37 + x38 - x39 + x40 - x41 + x42 - x43 - x44 + x45 - x46 + x47 - x48 + x49 - x50 + x51 + x52 - x53 + x54 - x55 + x56 - x57 + x58 - x59 - x60 + x61 - x62 + x63;
    wire signed [13:0] o46 = x0 + x1 - x2 - x3 - x4 - x5 + x6 + x7 - x8 - x9 + x10 + x11 + x12 + x13 - x14 - x15 + x16 + x17 - x18 - x19 - x20 - x21 + x22 + x23 - x24 - x25 + x26 + x27 + x28 + x29 - x30 - x31 - x32 - x33 + x34 + x35 + x36 + x37 - x38 - x39 + x40 + x41 - x42 - x43 - x44 - x45 + x46 + x47 - x48 - x49 + x50 + x51 + x52 + x53 - x54 - x55 + x56 + x57 - x58 - x59 - x60 - x61 + x62 + x63;
    wire signed [13:0] o47 = x0 - x1 - x2 + x3 - x4 + x5 + x6 - x7 - x8 + x9 + x10 - x11 + x12 - x13 - x14 + x15 + x16 - x17 - x18 + x19 - x20 + x21 + x22 - x23 - x24 + x25 + x26 - x27 + x28 - x29 - x30 + x31 - x32 + x33 + x34 - x35 + x36 - x37 - x38 + x39 + x40 - x41 - x42 + x43 - x44 + x45 + x46 - x47 - x48 + x49 + x50 - x51 + x52 - x53 - x54 + x55 + x56 - x57 - x58 + x59 - x60 + x61 + x62 - x63;
    wire signed [13:0] o48 = x0 + x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8 + x9 + x10 + x11 + x12 + x13 + x14 + x15 - x16 - x17 - x18 - x19 - x20 - x21 - x22 - x23 - x24 - x25 - x26 - x27 - x28 - x29 - x30 - x31 - x32 - x33 - x34 - x35 - x36 - x37 - x38 - x39 - x40 - x41 - x42 - x43 - x44 - x45 - x46 - x47 + x48 + x49 + x50 + x51 + x52 + x53 + x54 + x55 + x56 + x57 + x58 + x59 + x60 + x61 + x62 + x63;
    wire signed [13:0] o49 = x0 - x1 + x2 - x3 + x4 - x5 + x6 - x7 + x8 - x9 + x10 - x11 + x12 - x13 + x14 - x15 - x16 + x17 - x18 + x19 - x20 + x21 - x22 + x23 - x24 + x25 - x26 + x27 - x28 + x29 - x30 + x31 - x32 + x33 - x34 + x35 - x36 + x37 - x38 + x39 - x40 + x41 - x42 + x43 - x44 + x45 - x46 + x47 + x48 - x49 + x50 - x51 + x52 - x53 + x54 - x55 + x56 - x57 + x58 - x59 + x60 - x61 + x62 - x63;
    wire signed [13:0] o50 = x0 + x1 - x2 - x3 + x4 + x5 - x6 - x7 + x8 + x9 - x10 - x11 + x12 + x13 - x14 - x15 - x16 - x17 + x18 + x19 - x20 - x21 + x22 + x23 - x24 - x25 + x26 + x27 - x28 - x29 + x30 + x31 - x32 - x33 + x34 + x35 - x36 - x37 + x38 + x39 - x40 - x41 + x42 + x43 - x44 - x45 + x46 + x47 + x48 + x49 - x50 - x51 + x52 + x53 - x54 - x55 + x56 + x57 - x58 - x59 + x60 + x61 - x62 - x63;
    wire signed [13:0] o51 = x0 - x1 - x2 + x3 + x4 - x5 - x6 + x7 + x8 - x9 - x10 + x11 + x12 - x13 - x14 + x15 - x16 + x17 + x18 - x19 - x20 + x21 + x22 - x23 - x24 + x25 + x26 - x27 - x28 + x29 + x30 - x31 - x32 + x33 + x34 - x35 - x36 + x37 + x38 - x39 - x40 + x41 + x42 - x43 - x44 + x45 + x46 - x47 + x48 - x49 - x50 + x51 + x52 - x53 - x54 + x55 + x56 - x57 - x58 + x59 + x60 - x61 - x62 + x63;
    wire signed [13:0] o52 = x0 + x1 + x2 + x3 - x4 - x5 - x6 - x7 + x8 + x9 + x10 + x11 - x12 - x13 - x14 - x15 - x16 - x17 - x18 - x19 + x20 + x21 + x22 + x23 - x24 - x25 - x26 - x27 + x28 + x29 + x30 + x31 - x32 - x33 - x34 - x35 + x36 + x37 + x38 + x39 - x40 - x41 - x42 - x43 + x44 + x45 + x46 + x47 + x48 + x49 + x50 + x51 - x52 - x53 - x54 - x55 + x56 + x57 + x58 + x59 - x60 - x61 - x62 - x63;
    wire signed [13:0] o53 = x0 - x1 + x2 - x3 - x4 + x5 - x6 + x7 + x8 - x9 + x10 - x11 - x12 + x13 - x14 + x15 - x16 + x17 - x18 + x19 + x20 - x21 + x22 - x23 - x24 + x25 - x26 + x27 + x28 - x29 + x30 - x31 - x32 + x33 - x34 + x35 + x36 - x37 + x38 - x39 - x40 + x41 - x42 + x43 + x44 - x45 + x46 - x47 + x48 - x49 + x50 - x51 - x52 + x53 - x54 + x55 + x56 - x57 + x58 - x59 - x60 + x61 - x62 + x63;
    wire signed [13:0] o54 = x0 + x1 - x2 - x3 - x4 - x5 + x6 + x7 + x8 + x9 - x10 - x11 - x12 - x13 + x14 + x15 - x16 - x17 + x18 + x19 + x20 + x21 - x22 - x23 - x24 - x25 + x26 + x27 + x28 + x29 - x30 - x31 - x32 - x33 + x34 + x35 + x36 + x37 - x38 - x39 - x40 - x41 + x42 + x43 + x44 + x45 - x46 - x47 + x48 + x49 - x50 - x51 - x52 - x53 + x54 + x55 + x56 + x57 - x58 - x59 - x60 - x61 + x62 + x63;
    wire signed [13:0] o55 = x0 - x1 - x2 + x3 - x4 + x5 + x6 - x7 + x8 - x9 - x10 + x11 - x12 + x13 + x14 - x15 - x16 + x17 + x18 - x19 + x20 - x21 - x22 + x23 - x24 + x25 + x26 - x27 + x28 - x29 - x30 + x31 - x32 + x33 + x34 - x35 + x36 - x37 - x38 + x39 - x40 + x41 + x42 - x43 + x44 - x45 - x46 + x47 + x48 - x49 - x50 + x51 - x52 + x53 + x54 - x55 + x56 - x57 - x58 + x59 - x60 + x61 + x62 - x63;
    wire signed [13:0] o56 = x0 + x1 + x2 + x3 + x4 + x5 + x6 + x7 - x8 - x9 - x10 - x11 - x12 - x13 - x14 - x15 - x16 - x17 - x18 - x19 - x20 - x21 - x22 - x23 + x24 + x25 + x26 + x27 + x28 + x29 + x30 + x31 - x32 - x33 - x34 - x35 - x36 - x37 - x38 - x39 + x40 + x41 + x42 + x43 + x44 + x45 + x46 + x47 + x48 + x49 + x50 + x51 + x52 + x53 + x54 + x55 - x56 - x57 - x58 - x59 - x60 - x61 - x62 - x63;
    wire signed [13:0] o57 = x0 - x1 + x2 - x3 + x4 - x5 + x6 - x7 - x8 + x9 - x10 + x11 - x12 + x13 - x14 + x15 - x16 + x17 - x18 + x19 - x20 + x21 - x22 + x23 + x24 - x25 + x26 - x27 + x28 - x29 + x30 - x31 - x32 + x33 - x34 + x35 - x36 + x37 - x38 + x39 + x40 - x41 + x42 - x43 + x44 - x45 + x46 - x47 + x48 - x49 + x50 - x51 + x52 - x53 + x54 - x55 - x56 + x57 - x58 + x59 - x60 + x61 - x62 + x63;
    wire signed [13:0] o58 = x0 + x1 - x2 - x3 + x4 + x5 - x6 - x7 - x8 - x9 + x10 + x11 - x12 - x13 + x14 + x15 - x16 - x17 + x18 + x19 - x20 - x21 + x22 + x23 + x24 + x25 - x26 - x27 + x28 + x29 - x30 - x31 - x32 - x33 + x34 + x35 - x36 - x37 + x38 + x39 + x40 + x41 - x42 - x43 + x44 + x45 - x46 - x47 + x48 + x49 - x50 - x51 + x52 + x53 - x54 - x55 - x56 - x57 + x58 + x59 - x60 - x61 + x62 + x63;
    wire signed [13:0] o59 = x0 - x1 - x2 + x3 + x4 - x5 - x6 + x7 - x8 + x9 + x10 - x11 - x12 + x13 + x14 - x15 - x16 + x17 + x18 - x19 - x20 + x21 + x22 - x23 + x24 - x25 - x26 + x27 + x28 - x29 - x30 + x31 - x32 + x33 + x34 - x35 - x36 + x37 + x38 - x39 + x40 - x41 - x42 + x43 + x44 - x45 - x46 + x47 + x48 - x49 - x50 + x51 + x52 - x53 - x54 + x55 - x56 + x57 + x58 - x59 - x60 + x61 + x62 - x63;
    wire signed [13:0] o60 = x0 + x1 + x2 + x3 - x4 - x5 - x6 - x7 - x8 - x9 - x10 - x11 + x12 + x13 + x14 + x15 - x16 - x17 - x18 - x19 + x20 + x21 + x22 + x23 + x24 + x25 + x26 + x27 - x28 - x29 - x30 - x31 - x32 - x33 - x34 - x35 + x36 + x37 + x38 + x39 + x40 + x41 + x42 + x43 - x44 - x45 - x46 - x47 + x48 + x49 + x50 + x51 - x52 - x53 - x54 - x55 - x56 - x57 - x58 - x59 + x60 + x61 + x62 + x63;
    wire signed [13:0] o61 = x0 - x1 + x2 - x3 - x4 + x5 - x6 + x7 - x8 + x9 - x10 + x11 + x12 - x13 + x14 - x15 - x16 + x17 - x18 + x19 + x20 - x21 + x22 - x23 + x24 - x25 + x26 - x27 - x28 + x29 - x30 + x31 - x32 + x33 - x34 + x35 + x36 - x37 + x38 - x39 + x40 - x41 + x42 - x43 - x44 + x45 - x46 + x47 + x48 - x49 + x50 - x51 - x52 + x53 - x54 + x55 - x56 + x57 - x58 + x59 + x60 - x61 + x62 - x63;
    wire signed [13:0] o62 = x0 + x1 - x2 - x3 - x4 - x5 + x6 + x7 - x8 - x9 + x10 + x11 + x12 + x13 - x14 - x15 - x16 - x17 + x18 + x19 + x20 + x21 - x22 - x23 + x24 + x25 - x26 - x27 - x28 - x29 + x30 + x31 - x32 - x33 + x34 + x35 + x36 + x37 - x38 - x39 + x40 + x41 - x42 - x43 - x44 - x45 + x46 + x47 + x48 + x49 - x50 - x51 - x52 - x53 + x54 + x55 - x56 - x57 + x58 + x59 + x60 + x61 - x62 - x63;
    wire signed [13:0] o63 = x0 - x1 - x2 + x3 - x4 + x5 + x6 - x7 - x8 + x9 + x10 - x11 + x12 - x13 - x14 + x15 - x16 + x17 + x18 - x19 + x20 - x21 - x22 + x23 + x24 - x25 - x26 + x27 - x28 + x29 + x30 - x31 - x32 + x33 + x34 - x35 + x36 - x37 - x38 + x39 + x40 - x41 - x42 + x43 - x44 + x45 + x46 - x47 + x48 - x49 - x50 + x51 - x52 + x53 + x54 - x55 - x56 + x57 + x58 - x59 + x60 - x61 - x62 + x63;
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
    assign out_valid = in_valid;
    wire _unused_clk = clk;
endmodule
`default_nettype wire
