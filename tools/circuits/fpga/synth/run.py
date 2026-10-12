#!/usr/bin/env python3
"""run.py -- synthesise, place and route ONE design file for the iCE40-HX8K (package ct256)
and print what was measured, as one JSON object.  Standard library only.

    python3 -B run.py DESIGN.v [--seed 1] [--freq 400] [--retime | --dff] [--extra FILE ...]
                      [--incdir DIR] [--outreg auto|0|1] [--work DIR] [--tag NAME]
                      [--no-pnr] [--keep]

WHAT IS MEASURED
  DESIGN.v holds one module wht_* with the ports of fpga/rtl/v:
      clk, in_valid, in_data[NW-1:0], out_valid, out_data[NO-1:0].
  The design has more inputs and outputs than the package has pins, so it is put in a
  test harness, the same for every design:
      top    a serial-in shift register of NW bits feeds in_data (it is the INPUT REGISTER
             of the measurement); in_valid comes from a pin through one flip-flop;
             a signature register of NO+1 bits takes the outputs: acc[0] <= out_valid,
             acc[i+1] <= acc[i] XOR out_data[i]; acc[NO] goes to a pin.
             Cost of the harness: NW + NO + 2 logic cells, and nextpnr always adds 2 cells
             that hold the constants 0 and 1: NW + NO + 4 (measured with --stub, see below).
      dut    the design under test.  For a combinational design (variant c) dut is the design
             plus an OUTPUT REGISTER on out_data and out_valid, so the path that is timed is
             input register -> adders -> output register.  For a design whose outputs are
             already registered (p, pK, r) dut is the design alone.
  dut is synthesised as its own module (attribute keep_hierarchy), so that nothing of the
  harness can be merged into the design or the other way round (a plain shift register would
  otherwise be merged with the design's own delay registers).  After synthesis the hierarchy
  is flattened without any further optimisation, and nextpnr packs, places and routes it.

  yosys:    synth_ice40 -top top            (--retime and --dff: see the script lines below)
  nextpnr:  --hx8k --package ct256 --seed S --freq F     (defaults otherwise: placer heap,
            router router1)
  icetime:  -d hx8k -P ct256 -t -m  on the routed .asc

  Reported:
    lc_total        logic cells used, whole chip image (nextpnr "ICESTORM_LC")
    lc_harness      logic cells of the harness, counted by name; harness_ok says it is NW + NO + 4
    lc_dut          lc_total - lc_harness: the design (with its output register)
    dut_carry_nolut dut carry cells whose LUT output is not used (carry only)
    dut_chain_extra dut cells that nextpnr added to start or leave a carry chain
    dut_carry       dut logic cells with the carry chain switched on  (adder bits)
    dut_lut_only    dut logic cells: a LUT, no carry, no flip-flop
    dut_lut_ff      dut logic cells: a LUT and a flip-flop, no carry
    dut_ff_only     dut logic cells: only a flip-flop (the LUT is a wire to it)
    dut_ff          dut logic cells that use their flip-flop (any kind)
    yosys_dut       cell counts yosys prints for the module dut (SB_LUT4, SB_CARRY, SB_DFF*)
    fmax_nextpnr    "Max frequency for clock" after routing, MHz
    fmax_icetime    icetime's figure, MHz
    crit            where nextpnr's critical path starts and ends (dut or harness)

  --stub     measures the harness alone: the design is replaced by wires
             (out_data[i] = in_data[i mod NW]).  Needs --nw and --no.
  --lean     the lean harness, for designs that would not fit beside the standard one: the
             outputs are folded 16 to 1 by XOR before the signature register (which is then
             NO/16 + 1 bits long).  Its cost is measured with --stub --lean.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time

SUITE = os.environ.get('OSS_CAD_SUITE', '/opt/oss-cad-suite')      # the unpacked oss-cad-suite
BIN = os.path.join(SUITE, 'bin')
HERE = os.path.dirname(os.path.abspath(__file__))
CHIPDB = os.path.join(SUITE, 'share', 'icebox', 'chipdb-8k.txt')

PCF = """# clock: the board's 12 MHz oscillator ball; the others: free balls of the FTDI serial port
set_io clk  J3
set_io sin  B10
set_io vin  B13
set_io sout B12
"""


def sh(cmd, log, timeout=None):
    t0 = time.time()
    with open(log, 'w') as f:
        p = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, timeout=timeout)
    return p.returncode, time.time() - t0


def parse_design(path):
    src = open(path).read()
    m = re.search(r'module\s+(wht_\w+)\s*\(', src)
    if not m:
        raise SystemExit('no module wht_* in ' + path)
    name = m.group(1)
    body = src[m.end():]
    mi = re.search(r'input\s+wire\s*\[(\d+):0\]\s*in_data', body)
    mo = re.search(r'output\s+wire\s*\[(\d+):0\]\s*out_data', body)
    if not (mi and mo):
        raise SystemExit('ports in_data / out_data not found in ' + path)
    return name, int(mi.group(1)) + 1, int(mo.group(1)) + 1


def stub_src(nw, no):
    name = 'wht_stub_%d_%d' % (nw, no)
    s = ['`default_nettype none',
         'module %s (input wire clk, input wire in_valid, input wire [%d:0] in_data,' % (name, nw - 1),
         '           output wire out_valid, output wire [%d:0] out_data);' % (no - 1),
         '    genvar i;',
         '    generate for (i = 0; i < %d; i = i + 1) begin : g' % no,
         '        assign out_data[i] = in_data[i %% %d];' % nw,
         '    end endgenerate',
         '    assign out_valid = in_valid;',
         'endmodule', '`default_nettype wire', '']
    return name, '\n'.join(s)


def harness_src(mod, nw, no, outreg, lean=False):
    s = []
    s.append('// Test harness written by run.py.  dut = %s%s.' % (mod, ' + output register' if outreg else ''))
    s.append('`default_nettype none')
    s.append('(* keep_hierarchy *)')
    s.append('module dut (input wire clk, input wire in_valid, input wire [%d:0] in_data,' % (nw - 1))
    s.append('            output wire out_valid, output wire [%d:0] out_data);' % (no - 1))
    s.append('    wire ov; wire [%d:0] od;' % (no - 1))
    s.append('    %s core (.clk(clk), .in_valid(in_valid), .in_data(in_data), .out_valid(ov), .out_data(od));' % mod)
    if outreg:
        s.append('    reg [%d:0] q; reg qv = 1\'b0;' % (no - 1))
        s.append('    always @(posedge clk) begin q <= od; qv <= ov; end')
        s.append('    assign out_data = q; assign out_valid = qv;')
    else:
        s.append('    assign out_data = od; assign out_valid = ov;')
    s.append('endmodule')
    s.append('')
    s.append('module top (input wire clk, input wire sin, input wire vin, output wire sout);')
    s.append('    reg [%d:0] sr;' % (nw - 1))
    s.append('    reg v = 1\'b0;')
    s.append('    always @(posedge clk) begin sr <= {sr[%d:0], sin}; v <= vin; end' % (nw - 2))
    s.append('    wire ov; wire [%d:0] od;' % (no - 1))
    s.append('    dut u_dut (.clk(clk), .in_valid(v), .in_data(sr), .out_valid(ov), .out_data(od));')
    if lean:
        # the lean harness (for designs that fill the chip): the outputs are folded 16 to 1 by XOR
        # before the signature register, which is then NO/16 + 1 bits long
        g = -(-no // 16)
        s.append('    wire [%d:0] odp = {%d\'d0, od};' % (g * 16 - 1, g * 16 - no) if g * 16 > no else '    wire [%d:0] odp = od;' % (no - 1))
        s.append('    wire [%d:0] par;' % (g - 1))
        s.append('    genvar gi;')
        s.append('    generate for (gi = 0; gi < %d; gi = gi + 1) begin : fold' % g)
        s.append('        assign par[gi] = ^odp[gi*16 +: 16];')
        s.append('    end endgenerate')
        s.append('    reg [%d:0] acc;' % g)
        s.append('    always @(posedge clk) acc <= {acc[%d:0], ov} ^ {par, 1\'b0};' % (g - 1))
        s.append('    assign sout = acc[%d];' % g)
    else:
        s.append('    reg [%d:0] acc;' % no)
        s.append('    always @(posedge clk) acc <= {acc[%d:0], ov} ^ {od, 1\'b0};' % (no - 1))
        s.append('    assign sout = acc[%d];' % no)
    s.append('endmodule')
    s.append('`default_nettype wire')
    return '\n'.join(s) + '\n'


def yosys_stat(path):
    """per-module cell counts from a 'stat' printout"""
    out, cur = {}, None
    for line in open(path):
        m = re.match(r'\s*===\s*(\S+)\s*===', line)
        if m:
            cur = m.group(1)
            out[cur] = {}
            continue
        m = re.match(r'\s+(\d+)\s+(?:[\d.eE+\-]+\s+)?(\$?[A-Za-z_][\w$]*)\s*$', line)
        if m and cur:
            out[cur][m.group(2)] = int(m.group(1))
            continue
        m = re.match(r'\s+(\$?[A-Za-z_][\w$]*)\s+(\d+)\s*$', line)
        if m and cur:
            out[cur][m.group(1)] = int(m.group(2))
    return out


HARNESS_PREFIXES = ('sr_', 'acc_', 'sout_', 'v_', '$PACKER')   # names of the standard harness's cells


def is_dut(name):
    """a logic cell of the design: its name carries the instance name u_dut, or it is one of the cells
    nextpnr adds to start or leave a carry chain (only the design has carry chains)"""
    return 'u_dut.' in name or name.startswith('$nextpnr_ICESTORM_LC')


def classify(json_path):
    """count the logic cells of the packed netlist by kind.  Harness cells are the shift register
    (sr_), the signature register (acc_, sout_), the valid flip-flop (v_) and nextpnr's two constant
    cells ($PACKER_GND, $PACKER_VCC, present in every image); every other logic cell is the design,
    including the cells nextpnr adds to start or leave a carry chain ($nextpnr_ICESTORM_LC_*)."""
    d = json.load(open(json_path))
    top = d['modules']['top']
    kinds = ('lc', 'carry', 'carry_nolut', 'carry_ff', 'lut_only', 'lut_ff', 'ff_only', 'ff', 'chain_extra')
    res = {'dut': dict.fromkeys(kinds, 0), 'har': dict.fromkeys(kinds, 0)}

    def bit(v):
        if isinstance(v, int):
            return v
        s = str(v).strip()
        return int(s, 2) if s and set(s) <= set('01') else int(s)

    for name, c in top['cells'].items():
        if c['type'] != 'ICESTORM_LC':
            continue
        where = 'dut' if is_dut(name) else 'har'
        p = c['parameters']
        carry = bit(p.get('CARRY_ENABLE', 0)) != 0
        ff = bit(p.get('DFF_ENABLE', 0)) != 0
        init = bit(p.get('LUT_INIT', 0)) & 0xFFFF
        conn = c['connections']
        used = [k for k in ('I0', 'I1', 'I2', 'I3') if conn.get(k)]
        # a flip-flop alone: nextpnr gives the LUT the pass-through of I0 and nothing else
        passthru = (not carry) and ff and len(used) == 1 and init in (2, 0xAAAA)
        r = res[where]
        r['lc'] += 1
        if name.startswith('$nextpnr_ICESTORM_LC'):
            r['chain_extra'] += 1
        if ff:
            r['ff'] += 1
        if carry:
            r['carry'] += 1
            if ff:
                r['carry_ff'] += 1
            if not conn.get('O'):
                r['carry_nolut'] += 1
        elif passthru:
            r['ff_only'] += 1
        elif ff:
            r['lut_ff'] += 1
        else:
            r['lut_only'] += 1
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('design', nargs='?')
    ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--freq', type=float, default=400.0)
    ap.add_argument('--retime', action='store_true', help='add ABC retiming of the design (see the script)')
    ap.add_argument('--dff', action='store_true', help='synth_ice40 -dff (abc9 sequential synthesis)')
    ap.add_argument('--extra', action='append', default=[], help='further Verilog files (an outside core)')
    ap.add_argument('--incdir', action='append', default=[])
    ap.add_argument('--outreg', default='auto', choices=['auto', '0', '1'])
    ap.add_argument('--work', default=os.path.join(HERE, 'work'))
    ap.add_argument('--tag', default=None)
    ap.add_argument('--no-pnr', action='store_true')
    ap.add_argument('--pack-only', action='store_true', help='nextpnr packs and counts the cells, no placement (for designs too big for the chip)')
    ap.add_argument('--stub', action='store_true')
    ap.add_argument('--lean', action='store_true', help='the lean harness: outputs folded 16 to 1 before the signature register')
    ap.add_argument('--nw', type=int)
    ap.add_argument('--no', type=int)
    ap.add_argument('--pnr-timeout', type=int, default=3600)
    a = ap.parse_args()

    env_path = BIN + ':' + os.environ.get('PATH', '')
    os.environ['PATH'] = env_path

    if a.stub:
        mod, src = stub_src(a.nw, a.no)
        nw, no = a.nw, a.no
        tag = a.tag or ('stub_%d_%d' % (nw, no) + ('_lean' if a.lean else ''))
        wd = os.path.join(a.work, tag)
        os.makedirs(wd, exist_ok=True)
        design = os.path.join(wd, 'stub.v')
        open(design, 'w').write(src)
        outreg = 0
    else:
        design = os.path.abspath(a.design)
        mod, nw, no = parse_design(design)
        tag = a.tag or (mod[4:] + ('_retime' if a.retime else '') + ('_dff' if a.dff else '') + ('_lean' if a.lean else ''))
        wd = os.path.join(a.work, tag)
        os.makedirs(wd, exist_ok=True)
        if a.outreg == 'auto':
            outreg = 1 if re.search(r'_c_w\d+$', mod) else 0
        else:
            outreg = int(a.outreg)

    res = {'tag': tag, 'design': design, 'module': mod, 'nw': nw, 'no': no, 'outreg': outreg,
           'retime': bool(a.retime), 'dff': bool(a.dff), 'lean': bool(a.lean), 'seed': a.seed, 'freq_target': a.freq,
           'lc_harness_formula': nw + no + 4}

    # ---- synthesis (once per design and option set) ------------------------------------
    files = [design] + [os.path.abspath(x) for x in a.extra]
    h = hashlib.sha256()
    for f in files:
        h.update(open(f, 'rb').read())
    h.update(repr((outreg, a.retime, a.dff, a.incdir) + (('lean',) if a.lean else ())).encode())
    key = h.hexdigest()[:16]
    jsn = os.path.join(wd, 'top.json')
    keyf = os.path.join(wd, 'synth.key')
    if not (os.path.exists(jsn) and os.path.exists(keyf) and open(keyf).read().strip() == key
            and os.path.exists(os.path.join(wd, 'stat_hier.txt'))):
        open(os.path.join(wd, 'harness.v'), 'w').write(harness_src(mod, nw, no, outreg, a.lean))
        open(os.path.join(wd, 'top.pcf'), 'w').write(PCF)
        inc = ' '.join('-I' + os.path.abspath(d) for d in a.incdir)
        ys = []
        for f in files + [os.path.join(wd, 'harness.v')]:
            ys.append('read_verilog %s %s' % (inc, f))
        if a.retime:
            # yosys 0.69: synth_ice40 has no working -retime (the flag is accepted and does nothing; the
            # help text does not list it).  This is what -retime did in older releases: ABC's sequential
            # script with retiming, on the design only, after the adders were mapped to carry cells.
            ys.append('synth_ice40 -top top -run :map_ffs')
            ys.append('abc -dff -D 1 dut')
            ys.append('ice40_opt')
            ys.append('synth_ice40 -top top -run map_ffs:')
        elif a.dff:
            ys.append('synth_ice40 -top top -dff')
        else:
            ys.append('synth_ice40 -top top')
        ys.append('tee -o %s stat' % os.path.join(wd, 'stat_hier.txt'))
        ys.append('setattr -mod -unset keep_hierarchy dut')
        ys.append('flatten')
        ys.append('clean')
        ys.append('tee -o %s stat' % os.path.join(wd, 'stat_flat.txt'))
        ys.append('write_json %s' % jsn)
        open(os.path.join(wd, 'synth.ys'), 'w').write('\n'.join(ys) + '\n')
        rc, dt = sh(['yosys', '-q', '-l', os.path.join(wd, 'yosys.log'), '-s', os.path.join(wd, 'synth.ys')],
                    os.path.join(wd, 'yosys.out'), timeout=3600)
        res['yosys_seconds'] = round(dt, 1)
        if rc != 0:
            res['error'] = 'yosys failed, see ' + os.path.join(wd, 'yosys.log')
            print(json.dumps(res))
            return 1
        open(keyf, 'w').write(key + '\n')
    st = yosys_stat(os.path.join(wd, 'stat_hier.txt'))
    res['yosys_dut'] = st.get('dut', {})
    res['yosys_top'] = st.get('top', {})
    if a.no_pnr:
        print(json.dumps(res))
        return 0

    if a.pack_only:
        base = os.path.join(wd, 'pack')
        cmd = ['nextpnr-ice40', '--hx8k', '--package', 'ct256', '--json', jsn, '--pcf', os.path.join(wd, 'top.pcf'),
               '--pack-only', '--write', base + '.packed.json', '-q', '-l', base + '.nextpnr.log']
        rc, dt = sh(cmd, base + '.nextpnr.out', timeout=a.pnr_timeout)
        res['pack_only'] = True
        res['nextpnr_seconds'] = round(dt, 1)
        log = open(base + '.nextpnr.log').read() if os.path.exists(base + '.nextpnr.log') else ''
        m = re.search(r'ICESTORM_LC:\s*(\d+)/\s*(\d+)', log)
        if m:
            res['lc_total'] = int(m.group(1))
            res['lc_available'] = int(m.group(2))
        if os.path.exists(base + '.packed.json'):
            cl = classify(base + '.packed.json')
            os.remove(base + '.packed.json')
            res['lc_harness'] = cl['har']['lc']
            res['lc_dut'] = cl['dut']['lc']
            res.setdefault('lc_total', cl['har']['lc'] + cl['dut']['lc'])
            for k in ('carry', 'carry_nolut', 'carry_ff', 'lut_only', 'lut_ff', 'ff_only', 'ff', 'chain_extra'):
                res['dut_' + k] = cl['dut'][k]
            res['harness_ok'] = (cl['har']['lc'] == nw + no + 4) if not a.lean else None
        elif rc != 0:
            res['error'] = 'nextpnr --pack-only failed'
        print(json.dumps(res))
        return 0

    # ---- place and route ---------------------------------------------------------------
    base = os.path.join(wd, 's%d_f%g' % (a.seed, a.freq))
    cmd = ['nextpnr-ice40', '--hx8k', '--package', 'ct256', '--json', jsn, '--pcf', os.path.join(wd, 'top.pcf'),
           '--seed', str(a.seed), '--freq', str(a.freq), '--timing-allow-fail',
           '--asc', base + '.asc', '--report', base + '.report.json', '--write', base + '.packed.json', '-q',
           '-l', base + '.nextpnr.log']
    try:
        rc, dt = sh(cmd, base + '.nextpnr.out', timeout=a.pnr_timeout)
    except subprocess.TimeoutExpired:
        res['error'] = 'nextpnr timed out after %d s' % a.pnr_timeout
        print(json.dumps(res))
        return 1
    res['nextpnr_seconds'] = round(dt, 1)
    if rc != 0:
        tail = open(base + '.nextpnr.log').read()[-600:] if os.path.exists(base + '.nextpnr.log') else ''
        m = re.search(r'ERROR:.*', tail)
        res['error'] = 'nextpnr failed: ' + (m.group(0) if m else 'see log')
        # utilisation, if it got that far
        log = open(base + '.nextpnr.log').read() if os.path.exists(base + '.nextpnr.log') else ''
        m = re.search(r'ICESTORM_LC:\s*(\d+)/\s*(\d+)', log)
        if m:
            res['lc_total'] = int(m.group(1))
        print(json.dumps(res))
        return 1
    rep = json.load(open(base + '.report.json'))
    res['lc_total'] = rep['utilization']['ICESTORM_LC']['used']
    res['lc_available'] = rep['utilization']['ICESTORM_LC']['available']
    fm = rep.get('fmax', {})
    for k, v in fm.items():
        res['fmax_nextpnr'] = round(v['achieved'], 2)
        res['clock_net'] = k
    cp = [p for p in rep.get('critical_paths', []) if p.get('from', '').startswith('posedge') and p.get('to', '').startswith('posedge')]
    if cp:
        segs = cp[0]['path']
        a0 = segs[0]['from']['cell']
        a1 = segs[-1]['to']['cell']
        res['crit'] = ('dut' if is_dut(a0) else 'harness') + '->' + ('dut' if is_dut(a1) else 'harness')
        res['crit_from'] = a0[-60:]
        res['crit_to'] = a1[-60:]
        res['crit_logic_cells'] = sum(1 for s in segs if s.get('type') == 'logic')
    cl = classify(base + '.packed.json')
    os.remove(base + '.packed.json')
    res['lc_harness'] = cl['har']['lc']
    res['lc_dut'] = cl['dut']['lc']
    for k in ('carry', 'carry_nolut', 'carry_ff', 'lut_only', 'lut_ff', 'ff_only', 'ff', 'chain_extra'):
        res['dut_' + k] = cl['dut'][k]
    res['harness_ok'] = (cl['har']['lc'] == nw + no + 4) if not a.lean else None

    # ---- icetime -------------------------------------------------------------------------
    rc, dt = sh(['icetime', '-d', 'hx8k', '-P', 'ct256', '-p', os.path.join(wd, 'top.pcf'), '-t', '-m',
                 '-r', base + '.icetime.rpt', base + '.asc'], base + '.icetime.out', timeout=1800)
    res['icetime_seconds'] = round(dt, 1)
    txt = open(base + '.icetime.out').read() + (open(base + '.icetime.rpt').read() if os.path.exists(base + '.icetime.rpt') else '')
    m = re.search(r'Total path delay:\s*([\d.]+)\s*ns\s*\(([\d.]+)\s*MHz\)', txt)
    if m:
        res['icetime_ns'] = float(m.group(1))
        res['fmax_icetime'] = float(m.group(2))
    os.remove(base + '.asc')
    print(json.dumps(res))
    return 0


if __name__ == '__main__':
    sys.exit(main())
