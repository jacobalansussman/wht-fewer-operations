// Written by gen_rtl.py.  Do not edit by hand.
// 64-point Walsh-Hadamard transform written from the definition:
// y_J = sum over i of (-1)^popcount(J & i) * x_i, one expression per output, 22 bits.
// A reference for the equivalence proofs; not a design to be measured.
`default_nettype none
module wht_64_def_c_w16 (
    input  wire                 clk,
    input  wire                 in_valid,
    input  wire [1023:0] in_data,
    output wire                 out_valid,
    output wire [1407:0] out_data
);
    wire signed [21:0] x0 = $signed(in_data[15:0]);
    wire signed [21:0] x1 = $signed(in_data[31:16]);
    wire signed [21:0] x2 = $signed(in_data[47:32]);
    wire signed [21:0] x3 = $signed(in_data[63:48]);
    wire signed [21:0] x4 = $signed(in_data[79:64]);
    wire signed [21:0] x5 = $signed(in_data[95:80]);
    wire signed [21:0] x6 = $signed(in_data[111:96]);
    wire signed [21:0] x7 = $signed(in_data[127:112]);
    wire signed [21:0] x8 = $signed(in_data[143:128]);
    wire signed [21:0] x9 = $signed(in_data[159:144]);
    wire signed [21:0] x10 = $signed(in_data[175:160]);
    wire signed [21:0] x11 = $signed(in_data[191:176]);
    wire signed [21:0] x12 = $signed(in_data[207:192]);
    wire signed [21:0] x13 = $signed(in_data[223:208]);
    wire signed [21:0] x14 = $signed(in_data[239:224]);
    wire signed [21:0] x15 = $signed(in_data[255:240]);
    wire signed [21:0] x16 = $signed(in_data[271:256]);
    wire signed [21:0] x17 = $signed(in_data[287:272]);
    wire signed [21:0] x18 = $signed(in_data[303:288]);
    wire signed [21:0] x19 = $signed(in_data[319:304]);
    wire signed [21:0] x20 = $signed(in_data[335:320]);
    wire signed [21:0] x21 = $signed(in_data[351:336]);
    wire signed [21:0] x22 = $signed(in_data[367:352]);
    wire signed [21:0] x23 = $signed(in_data[383:368]);
    wire signed [21:0] x24 = $signed(in_data[399:384]);
    wire signed [21:0] x25 = $signed(in_data[415:400]);
    wire signed [21:0] x26 = $signed(in_data[431:416]);
    wire signed [21:0] x27 = $signed(in_data[447:432]);
    wire signed [21:0] x28 = $signed(in_data[463:448]);
    wire signed [21:0] x29 = $signed(in_data[479:464]);
    wire signed [21:0] x30 = $signed(in_data[495:480]);
    wire signed [21:0] x31 = $signed(in_data[511:496]);
    wire signed [21:0] x32 = $signed(in_data[527:512]);
    wire signed [21:0] x33 = $signed(in_data[543:528]);
    wire signed [21:0] x34 = $signed(in_data[559:544]);
    wire signed [21:0] x35 = $signed(in_data[575:560]);
    wire signed [21:0] x36 = $signed(in_data[591:576]);
    wire signed [21:0] x37 = $signed(in_data[607:592]);
    wire signed [21:0] x38 = $signed(in_data[623:608]);
    wire signed [21:0] x39 = $signed(in_data[639:624]);
    wire signed [21:0] x40 = $signed(in_data[655:640]);
    wire signed [21:0] x41 = $signed(in_data[671:656]);
    wire signed [21:0] x42 = $signed(in_data[687:672]);
    wire signed [21:0] x43 = $signed(in_data[703:688]);
    wire signed [21:0] x44 = $signed(in_data[719:704]);
    wire signed [21:0] x45 = $signed(in_data[735:720]);
    wire signed [21:0] x46 = $signed(in_data[751:736]);
    wire signed [21:0] x47 = $signed(in_data[767:752]);
    wire signed [21:0] x48 = $signed(in_data[783:768]);
    wire signed [21:0] x49 = $signed(in_data[799:784]);
    wire signed [21:0] x50 = $signed(in_data[815:800]);
    wire signed [21:0] x51 = $signed(in_data[831:816]);
    wire signed [21:0] x52 = $signed(in_data[847:832]);
    wire signed [21:0] x53 = $signed(in_data[863:848]);
    wire signed [21:0] x54 = $signed(in_data[879:864]);
    wire signed [21:0] x55 = $signed(in_data[895:880]);
    wire signed [21:0] x56 = $signed(in_data[911:896]);
    wire signed [21:0] x57 = $signed(in_data[927:912]);
    wire signed [21:0] x58 = $signed(in_data[943:928]);
    wire signed [21:0] x59 = $signed(in_data[959:944]);
    wire signed [21:0] x60 = $signed(in_data[975:960]);
    wire signed [21:0] x61 = $signed(in_data[991:976]);
    wire signed [21:0] x62 = $signed(in_data[1007:992]);
    wire signed [21:0] x63 = $signed(in_data[1023:1008]);
    wire signed [21:0] o0 = x0 + x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8 + x9 + x10 + x11 + x12 + x13 + x14 + x15 + x16 + x17 + x18 + x19 + x20 + x21 + x22 + x23 + x24 + x25 + x26 + x27 + x28 + x29 + x30 + x31 + x32 + x33 + x34 + x35 + x36 + x37 + x38 + x39 + x40 + x41 + x42 + x43 + x44 + x45 + x46 + x47 + x48 + x49 + x50 + x51 + x52 + x53 + x54 + x55 + x56 + x57 + x58 + x59 + x60 + x61 + x62 + x63;
    wire signed [21:0] o1 = x0 - x1 + x2 - x3 + x4 - x5 + x6 - x7 + x8 - x9 + x10 - x11 + x12 - x13 + x14 - x15 + x16 - x17 + x18 - x19 + x20 - x21 + x22 - x23 + x24 - x25 + x26 - x27 + x28 - x29 + x30 - x31 + x32 - x33 + x34 - x35 + x36 - x37 + x38 - x39 + x40 - x41 + x42 - x43 + x44 - x45 + x46 - x47 + x48 - x49 + x50 - x51 + x52 - x53 + x54 - x55 + x56 - x57 + x58 - x59 + x60 - x61 + x62 - x63;
    wire signed [21:0] o2 = x0 + x1 - x2 - x3 + x4 + x5 - x6 - x7 + x8 + x9 - x10 - x11 + x12 + x13 - x14 - x15 + x16 + x17 - x18 - x19 + x20 + x21 - x22 - x23 + x24 + x25 - x26 - x27 + x28 + x29 - x30 - x31 + x32 + x33 - x34 - x35 + x36 + x37 - x38 - x39 + x40 + x41 - x42 - x43 + x44 + x45 - x46 - x47 + x48 + x49 - x50 - x51 + x52 + x53 - x54 - x55 + x56 + x57 - x58 - x59 + x60 + x61 - x62 - x63;
    wire signed [21:0] o3 = x0 - x1 - x2 + x3 + x4 - x5 - x6 + x7 + x8 - x9 - x10 + x11 + x12 - x13 - x14 + x15 + x16 - x17 - x18 + x19 + x20 - x21 - x22 + x23 + x24 - x25 - x26 + x27 + x28 - x29 - x30 + x31 + x32 - x33 - x34 + x35 + x36 - x37 - x38 + x39 + x40 - x41 - x42 + x43 + x44 - x45 - x46 + x47 + x48 - x49 - x50 + x51 + x52 - x53 - x54 + x55 + x56 - x57 - x58 + x59 + x60 - x61 - x62 + x63;
    wire signed [21:0] o4 = x0 + x1 + x2 + x3 - x4 - x5 - x6 - x7 + x8 + x9 + x10 + x11 - x12 - x13 - x14 - x15 + x16 + x17 + x18 + x19 - x20 - x21 - x22 - x23 + x24 + x25 + x26 + x27 - x28 - x29 - x30 - x31 + x32 + x33 + x34 + x35 - x36 - x37 - x38 - x39 + x40 + x41 + x42 + x43 - x44 - x45 - x46 - x47 + x48 + x49 + x50 + x51 - x52 - x53 - x54 - x55 + x56 + x57 + x58 + x59 - x60 - x61 - x62 - x63;
    wire signed [21:0] o5 = x0 - x1 + x2 - x3 - x4 + x5 - x6 + x7 + x8 - x9 + x10 - x11 - x12 + x13 - x14 + x15 + x16 - x17 + x18 - x19 - x20 + x21 - x22 + x23 + x24 - x25 + x26 - x27 - x28 + x29 - x30 + x31 + x32 - x33 + x34 - x35 - x36 + x37 - x38 + x39 + x40 - x41 + x42 - x43 - x44 + x45 - x46 + x47 + x48 - x49 + x50 - x51 - x52 + x53 - x54 + x55 + x56 - x57 + x58 - x59 - x60 + x61 - x62 + x63;
    wire signed [21:0] o6 = x0 + x1 - x2 - x3 - x4 - x5 + x6 + x7 + x8 + x9 - x10 - x11 - x12 - x13 + x14 + x15 + x16 + x17 - x18 - x19 - x20 - x21 + x22 + x23 + x24 + x25 - x26 - x27 - x28 - x29 + x30 + x31 + x32 + x33 - x34 - x35 - x36 - x37 + x38 + x39 + x40 + x41 - x42 - x43 - x44 - x45 + x46 + x47 + x48 + x49 - x50 - x51 - x52 - x53 + x54 + x55 + x56 + x57 - x58 - x59 - x60 - x61 + x62 + x63;
    wire signed [21:0] o7 = x0 - x1 - x2 + x3 - x4 + x5 + x6 - x7 + x8 - x9 - x10 + x11 - x12 + x13 + x14 - x15 + x16 - x17 - x18 + x19 - x20 + x21 + x22 - x23 + x24 - x25 - x26 + x27 - x28 + x29 + x30 - x31 + x32 - x33 - x34 + x35 - x36 + x37 + x38 - x39 + x40 - x41 - x42 + x43 - x44 + x45 + x46 - x47 + x48 - x49 - x50 + x51 - x52 + x53 + x54 - x55 + x56 - x57 - x58 + x59 - x60 + x61 + x62 - x63;
    wire signed [21:0] o8 = x0 + x1 + x2 + x3 + x4 + x5 + x6 + x7 - x8 - x9 - x10 - x11 - x12 - x13 - x14 - x15 + x16 + x17 + x18 + x19 + x20 + x21 + x22 + x23 - x24 - x25 - x26 - x27 - x28 - x29 - x30 - x31 + x32 + x33 + x34 + x35 + x36 + x37 + x38 + x39 - x40 - x41 - x42 - x43 - x44 - x45 - x46 - x47 + x48 + x49 + x50 + x51 + x52 + x53 + x54 + x55 - x56 - x57 - x58 - x59 - x60 - x61 - x62 - x63;
    wire signed [21:0] o9 = x0 - x1 + x2 - x3 + x4 - x5 + x6 - x7 - x8 + x9 - x10 + x11 - x12 + x13 - x14 + x15 + x16 - x17 + x18 - x19 + x20 - x21 + x22 - x23 - x24 + x25 - x26 + x27 - x28 + x29 - x30 + x31 + x32 - x33 + x34 - x35 + x36 - x37 + x38 - x39 - x40 + x41 - x42 + x43 - x44 + x45 - x46 + x47 + x48 - x49 + x50 - x51 + x52 - x53 + x54 - x55 - x56 + x57 - x58 + x59 - x60 + x61 - x62 + x63;
    wire signed [21:0] o10 = x0 + x1 - x2 - x3 + x4 + x5 - x6 - x7 - x8 - x9 + x10 + x11 - x12 - x13 + x14 + x15 + x16 + x17 - x18 - x19 + x20 + x21 - x22 - x23 - x24 - x25 + x26 + x27 - x28 - x29 + x30 + x31 + x32 + x33 - x34 - x35 + x36 + x37 - x38 - x39 - x40 - x41 + x42 + x43 - x44 - x45 + x46 + x47 + x48 + x49 - x50 - x51 + x52 + x53 - x54 - x55 - x56 - x57 + x58 + x59 - x60 - x61 + x62 + x63;
    wire signed [21:0] o11 = x0 - x1 - x2 + x3 + x4 - x5 - x6 + x7 - x8 + x9 + x10 - x11 - x12 + x13 + x14 - x15 + x16 - x17 - x18 + x19 + x20 - x21 - x22 + x23 - x24 + x25 + x26 - x27 - x28 + x29 + x30 - x31 + x32 - x33 - x34 + x35 + x36 - x37 - x38 + x39 - x40 + x41 + x42 - x43 - x44 + x45 + x46 - x47 + x48 - x49 - x50 + x51 + x52 - x53 - x54 + x55 - x56 + x57 + x58 - x59 - x60 + x61 + x62 - x63;
    wire signed [21:0] o12 = x0 + x1 + x2 + x3 - x4 - x5 - x6 - x7 - x8 - x9 - x10 - x11 + x12 + x13 + x14 + x15 + x16 + x17 + x18 + x19 - x20 - x21 - x22 - x23 - x24 - x25 - x26 - x27 + x28 + x29 + x30 + x31 + x32 + x33 + x34 + x35 - x36 - x37 - x38 - x39 - x40 - x41 - x42 - x43 + x44 + x45 + x46 + x47 + x48 + x49 + x50 + x51 - x52 - x53 - x54 - x55 - x56 - x57 - x58 - x59 + x60 + x61 + x62 + x63;
    wire signed [21:0] o13 = x0 - x1 + x2 - x3 - x4 + x5 - x6 + x7 - x8 + x9 - x10 + x11 + x12 - x13 + x14 - x15 + x16 - x17 + x18 - x19 - x20 + x21 - x22 + x23 - x24 + x25 - x26 + x27 + x28 - x29 + x30 - x31 + x32 - x33 + x34 - x35 - x36 + x37 - x38 + x39 - x40 + x41 - x42 + x43 + x44 - x45 + x46 - x47 + x48 - x49 + x50 - x51 - x52 + x53 - x54 + x55 - x56 + x57 - x58 + x59 + x60 - x61 + x62 - x63;
    wire signed [21:0] o14 = x0 + x1 - x2 - x3 - x4 - x5 + x6 + x7 - x8 - x9 + x10 + x11 + x12 + x13 - x14 - x15 + x16 + x17 - x18 - x19 - x20 - x21 + x22 + x23 - x24 - x25 + x26 + x27 + x28 + x29 - x30 - x31 + x32 + x33 - x34 - x35 - x36 - x37 + x38 + x39 - x40 - x41 + x42 + x43 + x44 + x45 - x46 - x47 + x48 + x49 - x50 - x51 - x52 - x53 + x54 + x55 - x56 - x57 + x58 + x59 + x60 + x61 - x62 - x63;
    wire signed [21:0] o15 = x0 - x1 - x2 + x3 - x4 + x5 + x6 - x7 - x8 + x9 + x10 - x11 + x12 - x13 - x14 + x15 + x16 - x17 - x18 + x19 - x20 + x21 + x22 - x23 - x24 + x25 + x26 - x27 + x28 - x29 - x30 + x31 + x32 - x33 - x34 + x35 - x36 + x37 + x38 - x39 - x40 + x41 + x42 - x43 + x44 - x45 - x46 + x47 + x48 - x49 - x50 + x51 - x52 + x53 + x54 - x55 - x56 + x57 + x58 - x59 + x60 - x61 - x62 + x63;
    wire signed [21:0] o16 = x0 + x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8 + x9 + x10 + x11 + x12 + x13 + x14 + x15 - x16 - x17 - x18 - x19 - x20 - x21 - x22 - x23 - x24 - x25 - x26 - x27 - x28 - x29 - x30 - x31 + x32 + x33 + x34 + x35 + x36 + x37 + x38 + x39 + x40 + x41 + x42 + x43 + x44 + x45 + x46 + x47 - x48 - x49 - x50 - x51 - x52 - x53 - x54 - x55 - x56 - x57 - x58 - x59 - x60 - x61 - x62 - x63;
    wire signed [21:0] o17 = x0 - x1 + x2 - x3 + x4 - x5 + x6 - x7 + x8 - x9 + x10 - x11 + x12 - x13 + x14 - x15 - x16 + x17 - x18 + x19 - x20 + x21 - x22 + x23 - x24 + x25 - x26 + x27 - x28 + x29 - x30 + x31 + x32 - x33 + x34 - x35 + x36 - x37 + x38 - x39 + x40 - x41 + x42 - x43 + x44 - x45 + x46 - x47 - x48 + x49 - x50 + x51 - x52 + x53 - x54 + x55 - x56 + x57 - x58 + x59 - x60 + x61 - x62 + x63;
    wire signed [21:0] o18 = x0 + x1 - x2 - x3 + x4 + x5 - x6 - x7 + x8 + x9 - x10 - x11 + x12 + x13 - x14 - x15 - x16 - x17 + x18 + x19 - x20 - x21 + x22 + x23 - x24 - x25 + x26 + x27 - x28 - x29 + x30 + x31 + x32 + x33 - x34 - x35 + x36 + x37 - x38 - x39 + x40 + x41 - x42 - x43 + x44 + x45 - x46 - x47 - x48 - x49 + x50 + x51 - x52 - x53 + x54 + x55 - x56 - x57 + x58 + x59 - x60 - x61 + x62 + x63;
    wire signed [21:0] o19 = x0 - x1 - x2 + x3 + x4 - x5 - x6 + x7 + x8 - x9 - x10 + x11 + x12 - x13 - x14 + x15 - x16 + x17 + x18 - x19 - x20 + x21 + x22 - x23 - x24 + x25 + x26 - x27 - x28 + x29 + x30 - x31 + x32 - x33 - x34 + x35 + x36 - x37 - x38 + x39 + x40 - x41 - x42 + x43 + x44 - x45 - x46 + x47 - x48 + x49 + x50 - x51 - x52 + x53 + x54 - x55 - x56 + x57 + x58 - x59 - x60 + x61 + x62 - x63;
    wire signed [21:0] o20 = x0 + x1 + x2 + x3 - x4 - x5 - x6 - x7 + x8 + x9 + x10 + x11 - x12 - x13 - x14 - x15 - x16 - x17 - x18 - x19 + x20 + x21 + x22 + x23 - x24 - x25 - x26 - x27 + x28 + x29 + x30 + x31 + x32 + x33 + x34 + x35 - x36 - x37 - x38 - x39 + x40 + x41 + x42 + x43 - x44 - x45 - x46 - x47 - x48 - x49 - x50 - x51 + x52 + x53 + x54 + x55 - x56 - x57 - x58 - x59 + x60 + x61 + x62 + x63;
    wire signed [21:0] o21 = x0 - x1 + x2 - x3 - x4 + x5 - x6 + x7 + x8 - x9 + x10 - x11 - x12 + x13 - x14 + x15 - x16 + x17 - x18 + x19 + x20 - x21 + x22 - x23 - x24 + x25 - x26 + x27 + x28 - x29 + x30 - x31 + x32 - x33 + x34 - x35 - x36 + x37 - x38 + x39 + x40 - x41 + x42 - x43 - x44 + x45 - x46 + x47 - x48 + x49 - x50 + x51 + x52 - x53 + x54 - x55 - x56 + x57 - x58 + x59 + x60 - x61 + x62 - x63;
    wire signed [21:0] o22 = x0 + x1 - x2 - x3 - x4 - x5 + x6 + x7 + x8 + x9 - x10 - x11 - x12 - x13 + x14 + x15 - x16 - x17 + x18 + x19 + x20 + x21 - x22 - x23 - x24 - x25 + x26 + x27 + x28 + x29 - x30 - x31 + x32 + x33 - x34 - x35 - x36 - x37 + x38 + x39 + x40 + x41 - x42 - x43 - x44 - x45 + x46 + x47 - x48 - x49 + x50 + x51 + x52 + x53 - x54 - x55 - x56 - x57 + x58 + x59 + x60 + x61 - x62 - x63;
    wire signed [21:0] o23 = x0 - x1 - x2 + x3 - x4 + x5 + x6 - x7 + x8 - x9 - x10 + x11 - x12 + x13 + x14 - x15 - x16 + x17 + x18 - x19 + x20 - x21 - x22 + x23 - x24 + x25 + x26 - x27 + x28 - x29 - x30 + x31 + x32 - x33 - x34 + x35 - x36 + x37 + x38 - x39 + x40 - x41 - x42 + x43 - x44 + x45 + x46 - x47 - x48 + x49 + x50 - x51 + x52 - x53 - x54 + x55 - x56 + x57 + x58 - x59 + x60 - x61 - x62 + x63;
    wire signed [21:0] o24 = x0 + x1 + x2 + x3 + x4 + x5 + x6 + x7 - x8 - x9 - x10 - x11 - x12 - x13 - x14 - x15 - x16 - x17 - x18 - x19 - x20 - x21 - x22 - x23 + x24 + x25 + x26 + x27 + x28 + x29 + x30 + x31 + x32 + x33 + x34 + x35 + x36 + x37 + x38 + x39 - x40 - x41 - x42 - x43 - x44 - x45 - x46 - x47 - x48 - x49 - x50 - x51 - x52 - x53 - x54 - x55 + x56 + x57 + x58 + x59 + x60 + x61 + x62 + x63;
    wire signed [21:0] o25 = x0 - x1 + x2 - x3 + x4 - x5 + x6 - x7 - x8 + x9 - x10 + x11 - x12 + x13 - x14 + x15 - x16 + x17 - x18 + x19 - x20 + x21 - x22 + x23 + x24 - x25 + x26 - x27 + x28 - x29 + x30 - x31 + x32 - x33 + x34 - x35 + x36 - x37 + x38 - x39 - x40 + x41 - x42 + x43 - x44 + x45 - x46 + x47 - x48 + x49 - x50 + x51 - x52 + x53 - x54 + x55 + x56 - x57 + x58 - x59 + x60 - x61 + x62 - x63;
    wire signed [21:0] o26 = x0 + x1 - x2 - x3 + x4 + x5 - x6 - x7 - x8 - x9 + x10 + x11 - x12 - x13 + x14 + x15 - x16 - x17 + x18 + x19 - x20 - x21 + x22 + x23 + x24 + x25 - x26 - x27 + x28 + x29 - x30 - x31 + x32 + x33 - x34 - x35 + x36 + x37 - x38 - x39 - x40 - x41 + x42 + x43 - x44 - x45 + x46 + x47 - x48 - x49 + x50 + x51 - x52 - x53 + x54 + x55 + x56 + x57 - x58 - x59 + x60 + x61 - x62 - x63;
    wire signed [21:0] o27 = x0 - x1 - x2 + x3 + x4 - x5 - x6 + x7 - x8 + x9 + x10 - x11 - x12 + x13 + x14 - x15 - x16 + x17 + x18 - x19 - x20 + x21 + x22 - x23 + x24 - x25 - x26 + x27 + x28 - x29 - x30 + x31 + x32 - x33 - x34 + x35 + x36 - x37 - x38 + x39 - x40 + x41 + x42 - x43 - x44 + x45 + x46 - x47 - x48 + x49 + x50 - x51 - x52 + x53 + x54 - x55 + x56 - x57 - x58 + x59 + x60 - x61 - x62 + x63;
    wire signed [21:0] o28 = x0 + x1 + x2 + x3 - x4 - x5 - x6 - x7 - x8 - x9 - x10 - x11 + x12 + x13 + x14 + x15 - x16 - x17 - x18 - x19 + x20 + x21 + x22 + x23 + x24 + x25 + x26 + x27 - x28 - x29 - x30 - x31 + x32 + x33 + x34 + x35 - x36 - x37 - x38 - x39 - x40 - x41 - x42 - x43 + x44 + x45 + x46 + x47 - x48 - x49 - x50 - x51 + x52 + x53 + x54 + x55 + x56 + x57 + x58 + x59 - x60 - x61 - x62 - x63;
    wire signed [21:0] o29 = x0 - x1 + x2 - x3 - x4 + x5 - x6 + x7 - x8 + x9 - x10 + x11 + x12 - x13 + x14 - x15 - x16 + x17 - x18 + x19 + x20 - x21 + x22 - x23 + x24 - x25 + x26 - x27 - x28 + x29 - x30 + x31 + x32 - x33 + x34 - x35 - x36 + x37 - x38 + x39 - x40 + x41 - x42 + x43 + x44 - x45 + x46 - x47 - x48 + x49 - x50 + x51 + x52 - x53 + x54 - x55 + x56 - x57 + x58 - x59 - x60 + x61 - x62 + x63;
    wire signed [21:0] o30 = x0 + x1 - x2 - x3 - x4 - x5 + x6 + x7 - x8 - x9 + x10 + x11 + x12 + x13 - x14 - x15 - x16 - x17 + x18 + x19 + x20 + x21 - x22 - x23 + x24 + x25 - x26 - x27 - x28 - x29 + x30 + x31 + x32 + x33 - x34 - x35 - x36 - x37 + x38 + x39 - x40 - x41 + x42 + x43 + x44 + x45 - x46 - x47 - x48 - x49 + x50 + x51 + x52 + x53 - x54 - x55 + x56 + x57 - x58 - x59 - x60 - x61 + x62 + x63;
    wire signed [21:0] o31 = x0 - x1 - x2 + x3 - x4 + x5 + x6 - x7 - x8 + x9 + x10 - x11 + x12 - x13 - x14 + x15 - x16 + x17 + x18 - x19 + x20 - x21 - x22 + x23 + x24 - x25 - x26 + x27 - x28 + x29 + x30 - x31 + x32 - x33 - x34 + x35 - x36 + x37 + x38 - x39 - x40 + x41 + x42 - x43 + x44 - x45 - x46 + x47 - x48 + x49 + x50 - x51 + x52 - x53 - x54 + x55 + x56 - x57 - x58 + x59 - x60 + x61 + x62 - x63;
    wire signed [21:0] o32 = x0 + x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8 + x9 + x10 + x11 + x12 + x13 + x14 + x15 + x16 + x17 + x18 + x19 + x20 + x21 + x22 + x23 + x24 + x25 + x26 + x27 + x28 + x29 + x30 + x31 - x32 - x33 - x34 - x35 - x36 - x37 - x38 - x39 - x40 - x41 - x42 - x43 - x44 - x45 - x46 - x47 - x48 - x49 - x50 - x51 - x52 - x53 - x54 - x55 - x56 - x57 - x58 - x59 - x60 - x61 - x62 - x63;
    wire signed [21:0] o33 = x0 - x1 + x2 - x3 + x4 - x5 + x6 - x7 + x8 - x9 + x10 - x11 + x12 - x13 + x14 - x15 + x16 - x17 + x18 - x19 + x20 - x21 + x22 - x23 + x24 - x25 + x26 - x27 + x28 - x29 + x30 - x31 - x32 + x33 - x34 + x35 - x36 + x37 - x38 + x39 - x40 + x41 - x42 + x43 - x44 + x45 - x46 + x47 - x48 + x49 - x50 + x51 - x52 + x53 - x54 + x55 - x56 + x57 - x58 + x59 - x60 + x61 - x62 + x63;
    wire signed [21:0] o34 = x0 + x1 - x2 - x3 + x4 + x5 - x6 - x7 + x8 + x9 - x10 - x11 + x12 + x13 - x14 - x15 + x16 + x17 - x18 - x19 + x20 + x21 - x22 - x23 + x24 + x25 - x26 - x27 + x28 + x29 - x30 - x31 - x32 - x33 + x34 + x35 - x36 - x37 + x38 + x39 - x40 - x41 + x42 + x43 - x44 - x45 + x46 + x47 - x48 - x49 + x50 + x51 - x52 - x53 + x54 + x55 - x56 - x57 + x58 + x59 - x60 - x61 + x62 + x63;
    wire signed [21:0] o35 = x0 - x1 - x2 + x3 + x4 - x5 - x6 + x7 + x8 - x9 - x10 + x11 + x12 - x13 - x14 + x15 + x16 - x17 - x18 + x19 + x20 - x21 - x22 + x23 + x24 - x25 - x26 + x27 + x28 - x29 - x30 + x31 - x32 + x33 + x34 - x35 - x36 + x37 + x38 - x39 - x40 + x41 + x42 - x43 - x44 + x45 + x46 - x47 - x48 + x49 + x50 - x51 - x52 + x53 + x54 - x55 - x56 + x57 + x58 - x59 - x60 + x61 + x62 - x63;
    wire signed [21:0] o36 = x0 + x1 + x2 + x3 - x4 - x5 - x6 - x7 + x8 + x9 + x10 + x11 - x12 - x13 - x14 - x15 + x16 + x17 + x18 + x19 - x20 - x21 - x22 - x23 + x24 + x25 + x26 + x27 - x28 - x29 - x30 - x31 - x32 - x33 - x34 - x35 + x36 + x37 + x38 + x39 - x40 - x41 - x42 - x43 + x44 + x45 + x46 + x47 - x48 - x49 - x50 - x51 + x52 + x53 + x54 + x55 - x56 - x57 - x58 - x59 + x60 + x61 + x62 + x63;
    wire signed [21:0] o37 = x0 - x1 + x2 - x3 - x4 + x5 - x6 + x7 + x8 - x9 + x10 - x11 - x12 + x13 - x14 + x15 + x16 - x17 + x18 - x19 - x20 + x21 - x22 + x23 + x24 - x25 + x26 - x27 - x28 + x29 - x30 + x31 - x32 + x33 - x34 + x35 + x36 - x37 + x38 - x39 - x40 + x41 - x42 + x43 + x44 - x45 + x46 - x47 - x48 + x49 - x50 + x51 + x52 - x53 + x54 - x55 - x56 + x57 - x58 + x59 + x60 - x61 + x62 - x63;
    wire signed [21:0] o38 = x0 + x1 - x2 - x3 - x4 - x5 + x6 + x7 + x8 + x9 - x10 - x11 - x12 - x13 + x14 + x15 + x16 + x17 - x18 - x19 - x20 - x21 + x22 + x23 + x24 + x25 - x26 - x27 - x28 - x29 + x30 + x31 - x32 - x33 + x34 + x35 + x36 + x37 - x38 - x39 - x40 - x41 + x42 + x43 + x44 + x45 - x46 - x47 - x48 - x49 + x50 + x51 + x52 + x53 - x54 - x55 - x56 - x57 + x58 + x59 + x60 + x61 - x62 - x63;
    wire signed [21:0] o39 = x0 - x1 - x2 + x3 - x4 + x5 + x6 - x7 + x8 - x9 - x10 + x11 - x12 + x13 + x14 - x15 + x16 - x17 - x18 + x19 - x20 + x21 + x22 - x23 + x24 - x25 - x26 + x27 - x28 + x29 + x30 - x31 - x32 + x33 + x34 - x35 + x36 - x37 - x38 + x39 - x40 + x41 + x42 - x43 + x44 - x45 - x46 + x47 - x48 + x49 + x50 - x51 + x52 - x53 - x54 + x55 - x56 + x57 + x58 - x59 + x60 - x61 - x62 + x63;
    wire signed [21:0] o40 = x0 + x1 + x2 + x3 + x4 + x5 + x6 + x7 - x8 - x9 - x10 - x11 - x12 - x13 - x14 - x15 + x16 + x17 + x18 + x19 + x20 + x21 + x22 + x23 - x24 - x25 - x26 - x27 - x28 - x29 - x30 - x31 - x32 - x33 - x34 - x35 - x36 - x37 - x38 - x39 + x40 + x41 + x42 + x43 + x44 + x45 + x46 + x47 - x48 - x49 - x50 - x51 - x52 - x53 - x54 - x55 + x56 + x57 + x58 + x59 + x60 + x61 + x62 + x63;
    wire signed [21:0] o41 = x0 - x1 + x2 - x3 + x4 - x5 + x6 - x7 - x8 + x9 - x10 + x11 - x12 + x13 - x14 + x15 + x16 - x17 + x18 - x19 + x20 - x21 + x22 - x23 - x24 + x25 - x26 + x27 - x28 + x29 - x30 + x31 - x32 + x33 - x34 + x35 - x36 + x37 - x38 + x39 + x40 - x41 + x42 - x43 + x44 - x45 + x46 - x47 - x48 + x49 - x50 + x51 - x52 + x53 - x54 + x55 + x56 - x57 + x58 - x59 + x60 - x61 + x62 - x63;
    wire signed [21:0] o42 = x0 + x1 - x2 - x3 + x4 + x5 - x6 - x7 - x8 - x9 + x10 + x11 - x12 - x13 + x14 + x15 + x16 + x17 - x18 - x19 + x20 + x21 - x22 - x23 - x24 - x25 + x26 + x27 - x28 - x29 + x30 + x31 - x32 - x33 + x34 + x35 - x36 - x37 + x38 + x39 + x40 + x41 - x42 - x43 + x44 + x45 - x46 - x47 - x48 - x49 + x50 + x51 - x52 - x53 + x54 + x55 + x56 + x57 - x58 - x59 + x60 + x61 - x62 - x63;
    wire signed [21:0] o43 = x0 - x1 - x2 + x3 + x4 - x5 - x6 + x7 - x8 + x9 + x10 - x11 - x12 + x13 + x14 - x15 + x16 - x17 - x18 + x19 + x20 - x21 - x22 + x23 - x24 + x25 + x26 - x27 - x28 + x29 + x30 - x31 - x32 + x33 + x34 - x35 - x36 + x37 + x38 - x39 + x40 - x41 - x42 + x43 + x44 - x45 - x46 + x47 - x48 + x49 + x50 - x51 - x52 + x53 + x54 - x55 + x56 - x57 - x58 + x59 + x60 - x61 - x62 + x63;
    wire signed [21:0] o44 = x0 + x1 + x2 + x3 - x4 - x5 - x6 - x7 - x8 - x9 - x10 - x11 + x12 + x13 + x14 + x15 + x16 + x17 + x18 + x19 - x20 - x21 - x22 - x23 - x24 - x25 - x26 - x27 + x28 + x29 + x30 + x31 - x32 - x33 - x34 - x35 + x36 + x37 + x38 + x39 + x40 + x41 + x42 + x43 - x44 - x45 - x46 - x47 - x48 - x49 - x50 - x51 + x52 + x53 + x54 + x55 + x56 + x57 + x58 + x59 - x60 - x61 - x62 - x63;
    wire signed [21:0] o45 = x0 - x1 + x2 - x3 - x4 + x5 - x6 + x7 - x8 + x9 - x10 + x11 + x12 - x13 + x14 - x15 + x16 - x17 + x18 - x19 - x20 + x21 - x22 + x23 - x24 + x25 - x26 + x27 + x28 - x29 + x30 - x31 - x32 + x33 - x34 + x35 + x36 - x37 + x38 - x39 + x40 - x41 + x42 - x43 - x44 + x45 - x46 + x47 - x48 + x49 - x50 + x51 + x52 - x53 + x54 - x55 + x56 - x57 + x58 - x59 - x60 + x61 - x62 + x63;
    wire signed [21:0] o46 = x0 + x1 - x2 - x3 - x4 - x5 + x6 + x7 - x8 - x9 + x10 + x11 + x12 + x13 - x14 - x15 + x16 + x17 - x18 - x19 - x20 - x21 + x22 + x23 - x24 - x25 + x26 + x27 + x28 + x29 - x30 - x31 - x32 - x33 + x34 + x35 + x36 + x37 - x38 - x39 + x40 + x41 - x42 - x43 - x44 - x45 + x46 + x47 - x48 - x49 + x50 + x51 + x52 + x53 - x54 - x55 + x56 + x57 - x58 - x59 - x60 - x61 + x62 + x63;
    wire signed [21:0] o47 = x0 - x1 - x2 + x3 - x4 + x5 + x6 - x7 - x8 + x9 + x10 - x11 + x12 - x13 - x14 + x15 + x16 - x17 - x18 + x19 - x20 + x21 + x22 - x23 - x24 + x25 + x26 - x27 + x28 - x29 - x30 + x31 - x32 + x33 + x34 - x35 + x36 - x37 - x38 + x39 + x40 - x41 - x42 + x43 - x44 + x45 + x46 - x47 - x48 + x49 + x50 - x51 + x52 - x53 - x54 + x55 + x56 - x57 - x58 + x59 - x60 + x61 + x62 - x63;
    wire signed [21:0] o48 = x0 + x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8 + x9 + x10 + x11 + x12 + x13 + x14 + x15 - x16 - x17 - x18 - x19 - x20 - x21 - x22 - x23 - x24 - x25 - x26 - x27 - x28 - x29 - x30 - x31 - x32 - x33 - x34 - x35 - x36 - x37 - x38 - x39 - x40 - x41 - x42 - x43 - x44 - x45 - x46 - x47 + x48 + x49 + x50 + x51 + x52 + x53 + x54 + x55 + x56 + x57 + x58 + x59 + x60 + x61 + x62 + x63;
    wire signed [21:0] o49 = x0 - x1 + x2 - x3 + x4 - x5 + x6 - x7 + x8 - x9 + x10 - x11 + x12 - x13 + x14 - x15 - x16 + x17 - x18 + x19 - x20 + x21 - x22 + x23 - x24 + x25 - x26 + x27 - x28 + x29 - x30 + x31 - x32 + x33 - x34 + x35 - x36 + x37 - x38 + x39 - x40 + x41 - x42 + x43 - x44 + x45 - x46 + x47 + x48 - x49 + x50 - x51 + x52 - x53 + x54 - x55 + x56 - x57 + x58 - x59 + x60 - x61 + x62 - x63;
    wire signed [21:0] o50 = x0 + x1 - x2 - x3 + x4 + x5 - x6 - x7 + x8 + x9 - x10 - x11 + x12 + x13 - x14 - x15 - x16 - x17 + x18 + x19 - x20 - x21 + x22 + x23 - x24 - x25 + x26 + x27 - x28 - x29 + x30 + x31 - x32 - x33 + x34 + x35 - x36 - x37 + x38 + x39 - x40 - x41 + x42 + x43 - x44 - x45 + x46 + x47 + x48 + x49 - x50 - x51 + x52 + x53 - x54 - x55 + x56 + x57 - x58 - x59 + x60 + x61 - x62 - x63;
    wire signed [21:0] o51 = x0 - x1 - x2 + x3 + x4 - x5 - x6 + x7 + x8 - x9 - x10 + x11 + x12 - x13 - x14 + x15 - x16 + x17 + x18 - x19 - x20 + x21 + x22 - x23 - x24 + x25 + x26 - x27 - x28 + x29 + x30 - x31 - x32 + x33 + x34 - x35 - x36 + x37 + x38 - x39 - x40 + x41 + x42 - x43 - x44 + x45 + x46 - x47 + x48 - x49 - x50 + x51 + x52 - x53 - x54 + x55 + x56 - x57 - x58 + x59 + x60 - x61 - x62 + x63;
    wire signed [21:0] o52 = x0 + x1 + x2 + x3 - x4 - x5 - x6 - x7 + x8 + x9 + x10 + x11 - x12 - x13 - x14 - x15 - x16 - x17 - x18 - x19 + x20 + x21 + x22 + x23 - x24 - x25 - x26 - x27 + x28 + x29 + x30 + x31 - x32 - x33 - x34 - x35 + x36 + x37 + x38 + x39 - x40 - x41 - x42 - x43 + x44 + x45 + x46 + x47 + x48 + x49 + x50 + x51 - x52 - x53 - x54 - x55 + x56 + x57 + x58 + x59 - x60 - x61 - x62 - x63;
    wire signed [21:0] o53 = x0 - x1 + x2 - x3 - x4 + x5 - x6 + x7 + x8 - x9 + x10 - x11 - x12 + x13 - x14 + x15 - x16 + x17 - x18 + x19 + x20 - x21 + x22 - x23 - x24 + x25 - x26 + x27 + x28 - x29 + x30 - x31 - x32 + x33 - x34 + x35 + x36 - x37 + x38 - x39 - x40 + x41 - x42 + x43 + x44 - x45 + x46 - x47 + x48 - x49 + x50 - x51 - x52 + x53 - x54 + x55 + x56 - x57 + x58 - x59 - x60 + x61 - x62 + x63;
    wire signed [21:0] o54 = x0 + x1 - x2 - x3 - x4 - x5 + x6 + x7 + x8 + x9 - x10 - x11 - x12 - x13 + x14 + x15 - x16 - x17 + x18 + x19 + x20 + x21 - x22 - x23 - x24 - x25 + x26 + x27 + x28 + x29 - x30 - x31 - x32 - x33 + x34 + x35 + x36 + x37 - x38 - x39 - x40 - x41 + x42 + x43 + x44 + x45 - x46 - x47 + x48 + x49 - x50 - x51 - x52 - x53 + x54 + x55 + x56 + x57 - x58 - x59 - x60 - x61 + x62 + x63;
    wire signed [21:0] o55 = x0 - x1 - x2 + x3 - x4 + x5 + x6 - x7 + x8 - x9 - x10 + x11 - x12 + x13 + x14 - x15 - x16 + x17 + x18 - x19 + x20 - x21 - x22 + x23 - x24 + x25 + x26 - x27 + x28 - x29 - x30 + x31 - x32 + x33 + x34 - x35 + x36 - x37 - x38 + x39 - x40 + x41 + x42 - x43 + x44 - x45 - x46 + x47 + x48 - x49 - x50 + x51 - x52 + x53 + x54 - x55 + x56 - x57 - x58 + x59 - x60 + x61 + x62 - x63;
    wire signed [21:0] o56 = x0 + x1 + x2 + x3 + x4 + x5 + x6 + x7 - x8 - x9 - x10 - x11 - x12 - x13 - x14 - x15 - x16 - x17 - x18 - x19 - x20 - x21 - x22 - x23 + x24 + x25 + x26 + x27 + x28 + x29 + x30 + x31 - x32 - x33 - x34 - x35 - x36 - x37 - x38 - x39 + x40 + x41 + x42 + x43 + x44 + x45 + x46 + x47 + x48 + x49 + x50 + x51 + x52 + x53 + x54 + x55 - x56 - x57 - x58 - x59 - x60 - x61 - x62 - x63;
    wire signed [21:0] o57 = x0 - x1 + x2 - x3 + x4 - x5 + x6 - x7 - x8 + x9 - x10 + x11 - x12 + x13 - x14 + x15 - x16 + x17 - x18 + x19 - x20 + x21 - x22 + x23 + x24 - x25 + x26 - x27 + x28 - x29 + x30 - x31 - x32 + x33 - x34 + x35 - x36 + x37 - x38 + x39 + x40 - x41 + x42 - x43 + x44 - x45 + x46 - x47 + x48 - x49 + x50 - x51 + x52 - x53 + x54 - x55 - x56 + x57 - x58 + x59 - x60 + x61 - x62 + x63;
    wire signed [21:0] o58 = x0 + x1 - x2 - x3 + x4 + x5 - x6 - x7 - x8 - x9 + x10 + x11 - x12 - x13 + x14 + x15 - x16 - x17 + x18 + x19 - x20 - x21 + x22 + x23 + x24 + x25 - x26 - x27 + x28 + x29 - x30 - x31 - x32 - x33 + x34 + x35 - x36 - x37 + x38 + x39 + x40 + x41 - x42 - x43 + x44 + x45 - x46 - x47 + x48 + x49 - x50 - x51 + x52 + x53 - x54 - x55 - x56 - x57 + x58 + x59 - x60 - x61 + x62 + x63;
    wire signed [21:0] o59 = x0 - x1 - x2 + x3 + x4 - x5 - x6 + x7 - x8 + x9 + x10 - x11 - x12 + x13 + x14 - x15 - x16 + x17 + x18 - x19 - x20 + x21 + x22 - x23 + x24 - x25 - x26 + x27 + x28 - x29 - x30 + x31 - x32 + x33 + x34 - x35 - x36 + x37 + x38 - x39 + x40 - x41 - x42 + x43 + x44 - x45 - x46 + x47 + x48 - x49 - x50 + x51 + x52 - x53 - x54 + x55 - x56 + x57 + x58 - x59 - x60 + x61 + x62 - x63;
    wire signed [21:0] o60 = x0 + x1 + x2 + x3 - x4 - x5 - x6 - x7 - x8 - x9 - x10 - x11 + x12 + x13 + x14 + x15 - x16 - x17 - x18 - x19 + x20 + x21 + x22 + x23 + x24 + x25 + x26 + x27 - x28 - x29 - x30 - x31 - x32 - x33 - x34 - x35 + x36 + x37 + x38 + x39 + x40 + x41 + x42 + x43 - x44 - x45 - x46 - x47 + x48 + x49 + x50 + x51 - x52 - x53 - x54 - x55 - x56 - x57 - x58 - x59 + x60 + x61 + x62 + x63;
    wire signed [21:0] o61 = x0 - x1 + x2 - x3 - x4 + x5 - x6 + x7 - x8 + x9 - x10 + x11 + x12 - x13 + x14 - x15 - x16 + x17 - x18 + x19 + x20 - x21 + x22 - x23 + x24 - x25 + x26 - x27 - x28 + x29 - x30 + x31 - x32 + x33 - x34 + x35 + x36 - x37 + x38 - x39 + x40 - x41 + x42 - x43 - x44 + x45 - x46 + x47 + x48 - x49 + x50 - x51 - x52 + x53 - x54 + x55 - x56 + x57 - x58 + x59 + x60 - x61 + x62 - x63;
    wire signed [21:0] o62 = x0 + x1 - x2 - x3 - x4 - x5 + x6 + x7 - x8 - x9 + x10 + x11 + x12 + x13 - x14 - x15 - x16 - x17 + x18 + x19 + x20 + x21 - x22 - x23 + x24 + x25 - x26 - x27 - x28 - x29 + x30 + x31 - x32 - x33 + x34 + x35 + x36 + x37 - x38 - x39 + x40 + x41 - x42 - x43 - x44 - x45 + x46 + x47 + x48 + x49 - x50 - x51 - x52 - x53 + x54 + x55 - x56 - x57 + x58 + x59 + x60 + x61 - x62 - x63;
    wire signed [21:0] o63 = x0 - x1 - x2 + x3 - x4 + x5 + x6 - x7 - x8 + x9 + x10 - x11 + x12 - x13 - x14 + x15 - x16 + x17 + x18 - x19 + x20 - x21 - x22 + x23 + x24 - x25 - x26 + x27 - x28 + x29 + x30 - x31 - x32 + x33 + x34 - x35 + x36 - x37 - x38 + x39 + x40 - x41 - x42 + x43 - x44 + x45 + x46 - x47 + x48 - x49 - x50 + x51 - x52 + x53 + x54 - x55 - x56 + x57 + x58 - x59 + x60 - x61 - x62 + x63;
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
