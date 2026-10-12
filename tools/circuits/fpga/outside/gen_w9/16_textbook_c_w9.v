// Written by gen_rtl.py.  Do not edit by hand.
// 16-point Walsh-Hadamard transform, y_J = sum over i of (-1)^popcount(J & i) * x_i.
// Source circuit: tools/circuits/programs/generated/O_textbook_16.txt
// Inputs: 16 signed values of 9 bits.  Outputs: 16 signed values of 13 bits.
// Adders 64, depth 4 adder levels, adder bits 736 (chain bits 736).
// Variant c: combinational.  Latency 0.  clk is not used.
`default_nettype none
module wht_16_textbook_c_w9 (
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
    wire signed [9:0] n_t1 = x0 + x1;   // level 1
    wire signed [9:0] n_t2 = x0 - x1;   // level 1
    wire signed [9:0] n_t3 = x2 + x3;   // level 1
    wire signed [9:0] n_t4 = x2 - x3;   // level 1
    wire signed [9:0] n_t5 = x4 + x5;   // level 1
    wire signed [9:0] n_t6 = x4 - x5;   // level 1
    wire signed [9:0] n_t7 = x6 + x7;   // level 1
    wire signed [9:0] n_t8 = x6 - x7;   // level 1
    wire signed [9:0] n_t9 = x8 + x9;   // level 1
    wire signed [9:0] n_t10 = x8 - x9;   // level 1
    wire signed [9:0] n_t11 = x10 + x11;   // level 1
    wire signed [9:0] n_t12 = x10 - x11;   // level 1
    wire signed [9:0] n_t13 = x12 + x13;   // level 1
    wire signed [9:0] n_t14 = x12 - x13;   // level 1
    wire signed [9:0] n_t15 = x14 + x15;   // level 1
    wire signed [9:0] n_t16 = x14 - x15;   // level 1
    wire signed [10:0] n_t17 = n_t1 + n_t3;   // level 2
    wire signed [10:0] n_t18 = n_t1 - n_t3;   // level 2
    wire signed [10:0] n_t19 = n_t2 + n_t4;   // level 2
    wire signed [10:0] n_t20 = n_t2 - n_t4;   // level 2
    wire signed [10:0] n_t21 = n_t5 + n_t7;   // level 2
    wire signed [10:0] n_t22 = n_t5 - n_t7;   // level 2
    wire signed [10:0] n_t23 = n_t6 + n_t8;   // level 2
    wire signed [10:0] n_t24 = n_t6 - n_t8;   // level 2
    wire signed [10:0] n_t25 = n_t9 + n_t11;   // level 2
    wire signed [10:0] n_t26 = n_t9 - n_t11;   // level 2
    wire signed [10:0] n_t27 = n_t10 + n_t12;   // level 2
    wire signed [10:0] n_t28 = n_t10 - n_t12;   // level 2
    wire signed [10:0] n_t29 = n_t13 + n_t15;   // level 2
    wire signed [10:0] n_t30 = n_t13 - n_t15;   // level 2
    wire signed [10:0] n_t31 = n_t14 + n_t16;   // level 2
    wire signed [10:0] n_t32 = n_t14 - n_t16;   // level 2
    wire signed [11:0] n_t33 = n_t17 + n_t21;   // level 3
    wire signed [11:0] n_t34 = n_t17 - n_t21;   // level 3
    wire signed [11:0] n_t35 = n_t19 + n_t23;   // level 3
    wire signed [11:0] n_t36 = n_t19 - n_t23;   // level 3
    wire signed [11:0] n_t37 = n_t18 + n_t22;   // level 3
    wire signed [11:0] n_t38 = n_t18 - n_t22;   // level 3
    wire signed [11:0] n_t39 = n_t20 + n_t24;   // level 3
    wire signed [11:0] n_t40 = n_t20 - n_t24;   // level 3
    wire signed [11:0] n_t41 = n_t25 + n_t29;   // level 3
    wire signed [11:0] n_t42 = n_t25 - n_t29;   // level 3
    wire signed [11:0] n_t43 = n_t27 + n_t31;   // level 3
    wire signed [11:0] n_t44 = n_t27 - n_t31;   // level 3
    wire signed [11:0] n_t45 = n_t26 + n_t30;   // level 3
    wire signed [11:0] n_t46 = n_t26 - n_t30;   // level 3
    wire signed [11:0] n_t47 = n_t28 + n_t32;   // level 3
    wire signed [11:0] n_t48 = n_t28 - n_t32;   // level 3
    wire signed [12:0] n_t49 = n_t33 + n_t41;   // level 4
    wire signed [12:0] n_t50 = n_t33 - n_t41;   // level 4
    wire signed [12:0] n_t51 = n_t35 + n_t43;   // level 4
    wire signed [12:0] n_t52 = n_t35 - n_t43;   // level 4
    wire signed [12:0] n_t53 = n_t37 + n_t45;   // level 4
    wire signed [12:0] n_t54 = n_t37 - n_t45;   // level 4
    wire signed [12:0] n_t55 = n_t39 + n_t47;   // level 4
    wire signed [12:0] n_t56 = n_t39 - n_t47;   // level 4
    wire signed [12:0] n_t57 = n_t34 + n_t42;   // level 4
    wire signed [12:0] n_t58 = n_t34 - n_t42;   // level 4
    wire signed [12:0] n_t59 = n_t36 + n_t44;   // level 4
    wire signed [12:0] n_t60 = n_t36 - n_t44;   // level 4
    wire signed [12:0] n_t61 = n_t38 + n_t46;   // level 4
    wire signed [12:0] n_t62 = n_t38 - n_t46;   // level 4
    wire signed [12:0] n_t63 = n_t40 + n_t48;   // level 4
    wire signed [12:0] n_t64 = n_t40 - n_t48;   // level 4
    wire signed [12:0] o0 = n_t49;
    wire signed [12:0] o1 = n_t51;
    wire signed [12:0] o2 = n_t53;
    wire signed [12:0] o3 = n_t55;
    wire signed [12:0] o4 = n_t57;
    wire signed [12:0] o5 = n_t59;
    wire signed [12:0] o6 = n_t61;
    wire signed [12:0] o7 = n_t63;
    wire signed [12:0] o8 = n_t50;
    wire signed [12:0] o9 = n_t52;
    wire signed [12:0] o10 = n_t54;
    wire signed [12:0] o11 = n_t56;
    wire signed [12:0] o12 = n_t58;
    wire signed [12:0] o13 = n_t60;
    wire signed [12:0] o14 = n_t62;
    wire signed [12:0] o15 = n_t64;
    assign out_data = {
        o15, o14, o13, o12, o11, o10, o9, o8,
        o7, o6, o5, o4, o3, o2, o1, o0
    };
    assign out_valid = in_valid;
    wire _unused_clk = clk;
endmodule
`default_nettype wire
