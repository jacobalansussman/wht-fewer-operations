#!/bin/sh
# The simulations of the self-test, as run on 11 October 2026.  Nothing here touches the board.
#   sh sim.sh short     top level in Icarus Verilog, "seconds" of 4 periods, 13 lines   (about 20 s)
#   sh sim.sh fault     two damaged builds must be reported as failures                  (about 10 s)
#   sh sim.sh chip      the netlist decoded from the packed image, Icarus, first line    (about 1 min)
#   sh sim.sh chip10    the same netlist in Verilator, 10 s of board time, 11 lines      (about 3 min)
#   sh sim.sh real      top level in Icarus at the real settings, 10 s of board time     (about 25 min)
# Each step ends with compare.py, which checks the decoded serial bytes against ../expected.py.
set -eu
SUITE=${OSS_CAD_SUITE:-/opt/oss-cad-suite}      # the unpacked oss-cad-suite
export PATH="$SUITE/bin:$PATH"
cd "$(dirname "$0")"
mkdir -p sim sim/fault
RTL="selftest_top.v rtl/8_textbook_p_w12.v rtl/8_ours_p_w12.v rtl/8_broken_p_w12.v"
case "${1:-short}" in
short)
    iverilog -g2005 -o sim/tb_short.vvp -P tb_top.PPS=4 -I . tb/tb_top.v $RTL
    vvp -n sim/tb_short.vvp +clocks=1700000 +out=sim/short_rtl.bin > sim/short_rtl.log
    tail -1 sim/short_rtl.log
    python3 ../compare.py sim/short_rtl.bin --pps 4 --min-lines 13
    ;;
fault)
    # sim/fault/ours_fault_g5.v: n_g5 = n_g1 + n_g2 instead of -;  sim/fault/textbook_fault.v: last subtraction made an addition
    iverilog -g2005 -o sim/fault/tb_fault_dut.vvp -P tb_top.PPS=4 -I . tb/tb_top.v selftest_top.v rtl/8_textbook_p_w12.v sim/fault/ours_fault_g5.v rtl/8_broken_p_w12.v
    vvp -n sim/fault/tb_fault_dut.vvp +clocks=300000 +out=sim/fault/fault_dut.bin | tail -1
    if python3 ../compare.py sim/fault/fault_dut.bin --pps 4 --min-lines 2; then echo "UNEXPECTED PASS"; exit 1; fi
    iverilog -g2005 -o sim/fault/tb_fault_ref.vvp -P tb_top.PPS=4 -I . tb/tb_top.v selftest_top.v sim/fault/textbook_fault.v rtl/8_ours_p_w12.v rtl/8_broken_p_w12.v
    vvp -n sim/fault/tb_fault_ref.vvp +clocks=300000 +out=sim/fault/fault_ref.bin | tail -1
    if python3 ../compare.py sim/fault/fault_ref.bin --pps 4 --min-lines 2; then echo "UNEXPECTED PASS"; exit 1; fi
    echo "both damaged builds were reported as failures, as they should be"
    ;;
chip)
    icebox_vlog -s -l -d ct256 -p hx8k.pcf -n chip build/selftest_unpacked.asc > build/selftest_chip.v
    python3 chip_header.py build/selftest_chip.v build/selftest_chip_sim.v
    iverilog -g2005 -DCHIP -o sim/tb_chip.vvp tb/tb_top.v build/selftest_chip_sim.v
    vvp -n sim/tb_chip.vvp +clocks=125000 +out=sim/chip_k0.bin > sim/chip_k0.log
    tail -1 sim/chip_k0.log
    python3 ../compare.py sim/chip_k0.bin --min-lines 1
    ;;
chip10)
    verilator --cc tb/chip_wrap.v build/selftest_chip_sim.v --top-module chip_wrap --exe tb/harness.cpp \
        -O3 --build -j 1 -Wno-fatal -Mdir sim/vl_chip \
        -CFLAGS '-DVTOP=Vchip_wrap -DVTOP_H=\"Vchip_wrap.h\" -O2' > sim/vl_chip.build.log 2>&1
    sim/vl_chip/Vchip_wrap 120200000 sim/vl_chip_10s.bin > sim/vl_chip_10s.log
    tail -1 sim/vl_chip_10s.log
    python3 ../compare.py sim/vl_chip_10s.bin --min-lines 11
    ;;
real)
    iverilog -g2005 -o sim/tb_real.vvp -I . tb/tb_top.v $RTL
    vvp -n sim/tb_real.vvp +clocks=120200000 +out=sim/real_10s.bin > sim/real_10s.log
    tail -1 sim/real_10s.log
    python3 ../compare.py sim/real_10s.bin --min-lines 11
    ;;
*)
    echo "usage: sh sim.sh short|fault|chip|chip10|real"; exit 2 ;;
esac
