// Written by gen_rtl.py.  Do not edit by hand.
// 16-point Walsh-Hadamard transform, y_J = sum over i of (-1)^popcount(J & i) * x_i.
// Source circuit: tools/circuits/fpga/rtl/circuits/16_cfl1994.txt
// Coppersmith, Feig, Linzer (1994): eight 4-point circuits of 7 in two layers.  56 adders.
// Inputs: 16 signed values of 16 bits.  Outputs: 16 signed values of 20 bits.
// Adders 56, depth 8 adder levels, adder bits 1056 (chain bits 1032).
// Variant c: combinational.  Latency 0.  clk is not used.
`default_nettype none
module wht_16_cfl1994_c_w16 (
    input  wire                 clk,
    input  wire                 in_valid,
    input  wire [255:0] in_data,
    output wire                 out_valid,
    output wire [319:0] out_data
);
    wire signed [15:0] x0 = in_data[15:0];
    wire signed [15:0] x1 = in_data[31:16];
    wire signed [15:0] x2 = in_data[47:32];
    wire signed [15:0] x3 = in_data[63:48];
    wire signed [15:0] x4 = in_data[79:64];
    wire signed [15:0] x5 = in_data[95:80];
    wire signed [15:0] x6 = in_data[111:96];
    wire signed [15:0] x7 = in_data[127:112];
    wire signed [15:0] x8 = in_data[143:128];
    wire signed [15:0] x9 = in_data[159:144];
    wire signed [15:0] x10 = in_data[175:160];
    wire signed [15:0] x11 = in_data[191:176];
    wire signed [15:0] x12 = in_data[207:192];
    wire signed [15:0] x13 = in_data[223:208];
    wire signed [15:0] x14 = in_data[239:224];
    wire signed [15:0] x15 = in_data[255:240];
    wire signed [16:0] n_t1 = x1 + x2;   // level 1
    wire signed [17:0] n_t2 = n_t1 + x3;   // level 2
    wire signed [17:0] n_t3 = x0 - n_t2;   // level 3
    wire signed [17:0] n_t4 = x0 + n_t2;   // level 3
    wire signed [17:0] n_t5 = n_t3 + (x2 <<< 1);   // level 4
    wire signed [17:0] n_t6 = n_t3 + (x1 <<< 1);   // level 4
    wire signed [17:0] n_t7 = n_t3 + (x3 <<< 1);   // level 4
    wire signed [16:0] n_t8 = x5 + x6;   // level 1
    wire signed [17:0] n_t9 = n_t8 + x7;   // level 2
    wire signed [17:0] n_t10 = x4 - n_t9;   // level 3
    wire signed [17:0] n_t11 = x4 + n_t9;   // level 3
    wire signed [17:0] n_t12 = n_t10 + (x6 <<< 1);   // level 4
    wire signed [17:0] n_t13 = n_t10 + (x5 <<< 1);   // level 4
    wire signed [17:0] n_t14 = n_t10 + (x7 <<< 1);   // level 4
    wire signed [16:0] n_t15 = x9 + x10;   // level 1
    wire signed [17:0] n_t16 = n_t15 + x11;   // level 2
    wire signed [17:0] n_t17 = x8 - n_t16;   // level 3
    wire signed [17:0] n_t18 = x8 + n_t16;   // level 3
    wire signed [17:0] n_t19 = n_t17 + (x10 <<< 1);   // level 4
    wire signed [17:0] n_t20 = n_t17 + (x9 <<< 1);   // level 4
    wire signed [17:0] n_t21 = n_t17 + (x11 <<< 1);   // level 4
    wire signed [16:0] n_t22 = x13 + x14;   // level 1
    wire signed [17:0] n_t23 = n_t22 + x15;   // level 2
    wire signed [17:0] n_t24 = x12 - n_t23;   // level 3
    wire signed [17:0] n_t25 = x12 + n_t23;   // level 3
    wire signed [17:0] n_t26 = n_t24 + (x14 <<< 1);   // level 4
    wire signed [17:0] n_t27 = n_t24 + (x13 <<< 1);   // level 4
    wire signed [17:0] n_t28 = n_t24 + (x15 <<< 1);   // level 4
    wire signed [18:0] n_t29 = n_t11 + n_t18;   // level 4
    wire signed [19:0] n_t30 = n_t29 + n_t25;   // level 5
    wire signed [19:0] n_t31 = n_t4 - n_t30;   // level 6
    wire signed [19:0] n_t32 = n_t4 + n_t30;   // level 6
    wire signed [19:0] n_t33 = n_t31 + (n_t18 <<< 1);   // level 7
    wire signed [19:0] n_t34 = n_t31 + (n_t11 <<< 1);   // level 7
    wire signed [19:0] n_t35 = n_t31 + (n_t25 <<< 1);   // level 7
    wire signed [18:0] n_t36 = n_t12 + n_t19;   // level 5
    wire signed [19:0] n_t37 = n_t36 + n_t26;   // level 6
    wire signed [19:0] n_t38 = n_t5 - n_t37;   // level 7
    wire signed [19:0] n_t39 = n_t5 + n_t37;   // level 7
    wire signed [19:0] n_t40 = n_t38 + (n_t19 <<< 1);   // level 8
    wire signed [19:0] n_t41 = n_t38 + (n_t12 <<< 1);   // level 8
    wire signed [19:0] n_t42 = n_t38 + (n_t26 <<< 1);   // level 8
    wire signed [18:0] n_t43 = n_t13 + n_t20;   // level 5
    wire signed [19:0] n_t44 = n_t43 + n_t27;   // level 6
    wire signed [19:0] n_t45 = n_t6 - n_t44;   // level 7
    wire signed [19:0] n_t46 = n_t6 + n_t44;   // level 7
    wire signed [19:0] n_t47 = n_t45 + (n_t20 <<< 1);   // level 8
    wire signed [19:0] n_t48 = n_t45 + (n_t13 <<< 1);   // level 8
    wire signed [19:0] n_t49 = n_t45 + (n_t27 <<< 1);   // level 8
    wire signed [18:0] n_t50 = n_t14 + n_t21;   // level 5
    wire signed [19:0] n_t51 = n_t50 + n_t28;   // level 6
    wire signed [19:0] n_t52 = n_t7 - n_t51;   // level 7
    wire signed [19:0] n_t53 = n_t7 + n_t51;   // level 7
    wire signed [19:0] n_t54 = n_t52 + (n_t21 <<< 1);   // level 8
    wire signed [19:0] n_t55 = n_t52 + (n_t14 <<< 1);   // level 8
    wire signed [19:0] n_t56 = n_t52 + (n_t28 <<< 1);   // level 8
    wire signed [19:0] o0 = n_t32;
    wire signed [19:0] o1 = n_t39;
    wire signed [19:0] o2 = n_t46;
    wire signed [19:0] o3 = n_t53;
    wire signed [19:0] o4 = n_t33;
    wire signed [19:0] o5 = n_t40;
    wire signed [19:0] o6 = n_t47;
    wire signed [19:0] o7 = n_t54;
    wire signed [19:0] o8 = n_t34;
    wire signed [19:0] o9 = n_t41;
    wire signed [19:0] o10 = n_t48;
    wire signed [19:0] o11 = n_t55;
    wire signed [19:0] o12 = n_t35;
    wire signed [19:0] o13 = n_t42;
    wire signed [19:0] o14 = n_t49;
    wire signed [19:0] o15 = n_t56;
    assign out_data = {
        o15, o14, o13, o12, o11, o10, o9, o8,
        o7, o6, o5, o4, o3, o2, o1, o0
    };
    assign out_valid = in_valid;
    wire _unused_clk = clk;
endmodule
`default_nettype wire
