#!/usr/bin/env python3
"""fpga_measure.py -- the shared FPGA measurement tool of the speed studies of October 2026.
One design through synthesis and place-and-route on one chip, several placement seeds; one JSON line
per seed and one summary line (median, lowest, highest).  Standard library only (python3 3.9 is fine).

    python3 -B fpga_measure.py DESIGN.v [MORE.v ...] --chip ice40-hx8k [--seeds 5 | --seed-list 1,7,9]
        [--top MODULE] [--param NAME=VALUE ...] [--clk clk] [--outreg auto|0|1] [--freq 400]
        [--synth-opts "-dff"] [--no-pnr] [--jobs 2] [--bg] [--keep] [--work DIR] [--tag NAME]
        [--out results.jsonl] [--icetime] [--sv] [--define NAME[=V]] [--incdir DIR]

    python3 -B fpga_measure.py --list-chips

CHIPS (--chip; several separated by commas, or "all")
    ice40-hx8k   Lattice iCE40-HX8K, package ct256. synth_ice40; nextpnr-ice40 --hx8k. P&R.
    ice40-up5k   Lattice iCE40-UP5K, package sg48 (8 SB_MAC16 DSP blocks, 30 SB_RAM40_4K, 4 SPRAM).
                 synth_ice40 -dsp; nextpnr-ice40 --up5k (IO pins placed automatically). P&R.
    ecp5-25k     Lattice ECP5 LFE5U-25F, CABGA381, speed 6. synth_ecp5; nextpnr-ecp5 --25k. P&R.
    ecp5-85k     Lattice ECP5 LFE5U-85F, CABGA381, speed 6. synth_ecp5; nextpnr-ecp5 --85k. P&R.
    nexus-lifcl40  Lattice CrossLink-NX LIFCL-40-9BG400C (Nexus fabric, 28 nm). synth_nexus; nextpnr-nexus,
                 pins fixed by a .pdc file. P&R.
    gowin-gw1n9  Gowin GW1NR-LV9QN88PC6/I5 (the Tang Nano 9K chip), family GW1N-9C. synth_gowin;
                 nextpnr-himbaechel (uarch gowin), pins fixed by a .cst file. P&R.
    xc7          Xilinx 7-series. synth_xilinx -family xc7 -noclkbuf.  SYNTHESIS ONLY (no open P&R).
    cyclonev     Intel Cyclone V. synth_intel_alm -family cyclonev -noiopad -noclkbuf. SYNTHESIS ONLY.

THE DESIGN.  Any Verilog module with a clock port and inputs and outputs of any widths (the clock is
the port named by --clk, default "clk"; a module without one is taken as combinational).  The top
module is --top, else the only module called wht_*, else Yosys' -auto-top.  The ports are read by
Yosys itself (so ANSI or old-style declarations and parameters all work).  The wht41 designs
(clk, in_valid, in_data, out_valid, out_data) are one case of this.

THE HARNESS (the same as wht41/fpga/synth/run.py, generalised).  A design has more input and output
bits than a package has pins, so it sits in a harness:
    top   a serial-in shift register h_sr of NI bits feeds ALL the design's inputs except the clock,
          concatenated in port order (first port in the low bits); a signature register h_acc of NO
          bits takes ALL its outputs, concatenated the same way: acc[0] <= o[0],
          acc[i] <= acc[i-1] XOR o[i]; acc[NO-1] goes to a pin.  Pins: clk, sin, sout.
    dut   the design, plus an OUTPUT REGISTER on every output if --outreg is 1 (auto: 1 when the
          design has no flip-flop or memory of its own, so that the timed path is
          input register -> logic -> output register).  dut has keep_hierarchy during synthesis, so
          nothing of the harness merges with the design; afterwards the netlist is flattened with no
          further optimisation, and nextpnr packs, places and routes the whole.
    For the wht41 ports this is exactly run.py's harness: in_valid is bit 0 of the shift register
    (run.py fed it from its own pin through one flip-flop: the same one cell), out_valid is acc[0].
COUNTING.  After place and route the packed netlist is read (--write); a cell belongs to the design
if its name holds "u_dut." (Yosys' flatten prefixes the instance name) or if it is a cell nextpnr made
itself for a carry chain ($nextpnr_*, chain heads/tails: only the design has carry chains).
Everything else is harness or infrastructure (IO buffers, clock buffers, the constant drivers) and is
reported apart; "harness_ok" checks that the harness took what it should (see FPGA.md).
Synthesis-only chips are counted from Yosys' "stat" of the module dut (hierarchy still kept).

OUTPUT.  One JSON object per seed on stdout (and appended to --out), then one with "summary": true:
    "med", "min", "max" of every numeric field over the seeds.  Field names per chip: see FPGA.md.
Synthesis is done once per (design, chip, options) and cached in the work folder; each seed is one
nextpnr run.

RUNNING (changed 12 October, after the crash).  Every Yosys, nextpnr and icetime call goes through
common/heavy.sh by default: each call holds one of the 3 heavy slots of the whole Mac, so
place-and-route jobs cannot pile up (that night about 20 nextpnr ran at once through bg.sh).  --heavy
is still accepted and is now the default.  --jobs N places up to N seeds at once (at most 3), each in
a slot of its own, so the limit holds for the whole Mac; started inside a heavy slot already
(FARM_HEAVY_SLOT set, e.g. the whole script run with heavy.sh) the tool places one seed at a
time.  --bg runs everything through bg.sh instead: only for tiny designs, still capped by the memory
guard; nextpnr goes back to heavy.sh anyway for ECP5 and Nexus (one run of a tiny design takes 0.35 GB
on the ECP5-85F and 0.7 GB on Nexus: the chip database) and when the synthesised netlist is over
5 MB.  yosys_seconds, pnr_seconds and --timeout count from the moment the tool itself starts, not from
the wait for a slot.
DISK.  The synthesised netlist top.json (1 to 200 MB) is the bulk of a work folder: 2.6 GB of the
3.1 GB that the wave work folders held on 12 October, 1.26 GB of it written to the internal disk
during the six hours before the crash.  When the external SSD is mounted it is written to
$FARM_BIG_DIR/<the work folder's path>/ and the work folder
keeps a symlink top.json to it; logs, reports and statistics stay in the work folder.  Each seed's
packed netlist and routed image go there too and are deleted once counted; probe.json is deleted once
read.  --keep keeps those three.
"""
import argparse
import concurrent.futures as cf
import hashlib
import json
import os
import re
import signal
import statistics
import subprocess
import sys
import time

# ---- ax-k1 (wave 16) changes for the Colab kit; everything else is common/fpga_measure.py of 12 October unchanged.
# OSS_CAD_SUITE  the suite folder (default: the Mac's).   OPENXC7  the openXC7 toolchain folder (xc7 P&R chips).
# FARM_DIRECT=1  run every tool directly (no bg.sh / heavy.sh: those exist only on the Mac); FARM_SLOTS = how many
#                tool runs at once (default: the number of cores).  On the Mac leave FARM_DIRECT unset: the house
#                rules (heavy.sh, 3 slots for the whole Mac) then hold exactly as before.
# Every output row carries "platform" (OS, machine, tool versions) so that rows of two machines are never mixed.
SUITE = os.environ.get('OSS_CAD_SUITE', 'oss-cad-suite')
BIN = os.path.join(SUITE, 'bin')
OPENXC7 = os.environ.get('OPENXC7', 'openxc7')
DIRECT = os.environ.get('FARM_DIRECT') == '1'
FARM_COMMON = os.environ.get('FARM_COMMON', 'common')
HERE = os.path.dirname(os.path.abspath(__file__))
BG = os.path.join(FARM_COMMON, 'bg.sh')
HEAVY = os.path.join(FARM_COMMON, 'heavy.sh')
SLOTS = int(os.environ.get('FARM_SLOTS') or os.cpu_count() or 2) if DIRECT else 3   # Mac: heavy.sh's 3 slots
BG_MAX_MB = 5                  # --bg: a bigger synthesised netlist is placed and routed through heavy.sh anyway
BG_FAMILIES = ('ice40', 'gowin')   # --bg: nextpnr of the others takes 0.35 (ECP5-85F) to 0.7 GB (Nexus) for a tiny design
SSD = os.environ.get('FARM_BIG_DIR', '/nonexistent-big-dir')
FARM_ROOT = os.path.dirname(HERE)
BIG = os.path.join(SSD, 'fpga_work')   # bulky files of a work folder, mirrored by its path below FARM_ROOT
# what the memory guard of every bg.sh / heavy.sh command (common/memguard.py) did: 75 is the wrappers'
# own exit code; a tool the guard stopped ends by SIGTERM/SIGKILL after a "MEMGUARD: KILLING" line in its
# log, which sh() turns into 97 or 98 here
GUARD = {75: 'not started: memory or disk short for 5 minutes (memory guard)',
         97: 'killed by the memory guard: over its memory cap (FARM_MEM_CAP_GB=N raises it, at most 8; see heavy.sh)',
         98: 'killed by the memory guard: the Mac was short of memory'}

CHIPS = {
    'ice40-hx8k': dict(family='ice40', synth='synth_ice40 -top top', pnr='nextpnr-ice40',
                       args=['--hx8k', '--package', 'ct256'], cons=('pcf', 'set_io clk J3\nset_io sin B10\nset_io sout B12\n')),
    'ice40-up5k': dict(family='ice40', synth='synth_ice40 -dsp -top top', pnr='nextpnr-ice40',
                       args=['--up5k', '--package', 'sg48'], cons=None),
    'ecp5-25k': dict(family='ecp5', synth='synth_ecp5 -top top', pnr='nextpnr-ecp5',
                     args=['--25k', '--package', 'CABGA381', '--speed', '6'], cons=None),
    'ecp5-85k': dict(family='ecp5', synth='synth_ecp5 -top top', pnr='nextpnr-ecp5',
                     args=['--85k', '--package', 'CABGA381', '--speed', '6'], cons=None),
    'gowin-gw1n9': dict(family='gowin', synth='synth_gowin -noiopads -top top', post=['iopadmap -bits -inpad IBUF O:I -outpad OBUF I:O top', 'clean'],
                        pnr='nextpnr-himbaechel',
                        args=['--device', 'GW1NR-LV9QN88PC6/I5', '--vopt', 'family=GW1N-9C'],
                        cons=('cst', 'IO_LOC "clk" 52;\nIO_LOC "sin" 25;\nIO_LOC "sout" 26;\n')),
    'nexus-lifcl40': dict(family='nexus', synth='synth_nexus -top top', pnr='nextpnr-nexus',
                          args=['--device', 'LIFCL-40-9BG400C'],
                          cons=('pdc', 'ldc_set_location -site {L13} [get_ports clk]\n'
                                       'ldc_set_location -site {E17} [get_ports sin]\n'
                                       'ldc_set_location -site {F18} [get_ports sout]\n')),
    'xc7': dict(family='xc7', synth='synth_xilinx -family xc7 -flatten -noclkbuf -top top', pnr=None),
    # ax-k1: Xilinx 7-series PLACE AND ROUTE with openXC7 (nextpnr-xilinx = nextpnr-himbaechel, uarch xilinx, prjxray
    # database; release cavearr/toolchain-openxc7-releases 2026-10-19).  Synthesis as openXC7's own flow
    # (openXC7.mk: synth_xilinx -flatten -abc9 -arch xc7), with a clock buffer.  Pins: the Arty A7 / Nexys A7 clock pin
    # and two user pins of the csg324 package; Zynq: the PL clock pin of the Zybo/ZedBoard-style clg packages.
    'xc7a100t': dict(family='xc7pnr', synth='synth_xilinx -family xc7 -flatten -abc9 -top top', pnr='nextpnr-xilinx',
                     args=['--device', 'xc7a100tcsg324-1'], cons=('xdc', 'E3 D9 H5')),
    'xc7a200t': dict(family='xc7pnr', synth='synth_xilinx -family xc7 -flatten -abc9 -top top', pnr='nextpnr-xilinx',
                     args=['--device', 'xc7a200tsbg484-1'], cons=('xdc', 'R4 E22 T14')),
    'xc7z020': dict(family='xc7pnr', synth='synth_xilinx -family xc7 -flatten -abc9 -top top', pnr='nextpnr-xilinx',
                    args=['--device', 'xc7z020clg400-1'], cons=('xdc', 'K17 G15 M14')),
    'xc7a100t-abc': dict(family='xc7pnr', synth='synth_xilinx -family xc7 -flatten -top top', pnr='nextpnr-xilinx',
                         args=['--device', 'xc7a100tcsg324-1'], cons=('xdc', 'E3 D9 H5')),
    'cyclonev': dict(family='cyclonev', synth='synth_intel_alm -family cyclonev -noiopad -noclkbuf -top top', pnr=None),
}
CLOCK_NAMES = ('clk', 'clock', 'i_clk', 'aclk', 'clk_i', 'CLK')


def runner(heavy):
    if DIRECT:
        return []          # ax-k1: the Colab has no bg.sh / heavy.sh; the farm limits itself with FARM_SLOTS
    return [HEAVY if heavy else BG]


def tool_versions():
    """ax-k1: the platform stamp put in every row (rows of two machines or two tool builds are never compared)"""
    import platform
    v = {'os': platform.system(), 'machine': platform.machine(), 'direct': DIRECT}
    for k, cmd in (('yosys', [os.path.join(BIN, 'yosys'), '-V']), ('nextpnr', [os.path.join(BIN, 'nextpnr-ecp5'), '--version']),
                   ('openxc7', [os.path.join(OPENXC7, 'bin', 'nextpnr-xilinx'), '--version'])):
        try:
            o = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            v[k] = (o.stdout + o.stderr).strip().splitlines()[0][:120]
        except Exception as e:      # a tool that is not installed
            v[k] = 'missing'
    return v


PLATFORM = None


LIVE = set()       # pids of the runner processes in flight (taken down with their trees if we are stopped)


def kill_tree(pid):
    """kill a process and every descendant (the tool may run a shell's children; sby starts its engines
    in process groups of their own)"""
    out = subprocess.run(['ps', '-A', '-o', 'pid=,ppid='], capture_output=True, text=True).stdout
    kids = {}
    for line in out.split('\n'):
        f = line.split()
        if len(f) == 2:
            kids.setdefault(int(f[1]), []).append(int(f[0]))
    todo, allp = [pid], []
    while todo:
        q = todo.pop()
        allp.append(q)
        todo += kids.get(q, [])
    for q in reversed(allp):
        try:
            os.kill(q, signal.SIGKILL)
        except OSError:
            pass


def stop(signum, frame):
    """SIGTERM, SIGHUP or ^C: take every running tool down too, so that no nextpnr or solver is left behind"""
    for pid in list(LIVE):
        kill_tree(pid)
    os._exit(128 + signum)


def sh(run, cmd, log, timeout=None, cwd=None):
    """cmd under the runner run (heavy.sh or bg.sh), output to log.  Returns (exit code or 'timeout',
    seconds); 97 or 98 (see GUARD) when the memory guard stopped the tool.  Under heavy.sh a call may
    first wait for a free slot, so the tool touches log.start as it starts, and the seconds and the
    timeout count from then.  A timeout kills the whole process tree."""
    stamp = log + '.start'
    if os.path.exists(stamp):
        os.remove(stamp)
    t0 = time.time()
    said = HEAVY not in run
    with open(log, 'w') as f:
        p = subprocess.Popen(run + ['/bin/sh', '-c', ': > "$0"; exec "$@"', stamp] + cmd,
                             stdout=f, stderr=subprocess.STDOUT, cwd=cwd)
        LIVE.add(p.pid)
        rc = None
        while rc is None:
            try:
                rc = p.wait(timeout=2)
            except subprocess.TimeoutExpired:
                if not os.path.exists(stamp):
                    if not said and time.time() - t0 > 30:
                        print('[%s] waiting for a heavy slot (%d for the whole Mac): %s' % (
                            os.path.basename(sys.argv[0]), SLOTS, os.path.basename(log)), file=sys.stderr, flush=True)
                        said = True
                elif timeout and time.time() - os.path.getmtime(stamp) > timeout:
                    kill_tree(p.pid)
                    p.wait()
                    rc = 'timeout'
        LIVE.discard(p.pid)
    if rc in (-signal.SIGTERM, -signal.SIGKILL):
        rc = guard_kill(log) or rc
    t1 = os.path.getmtime(stamp) if os.path.exists(stamp) else t0
    if os.path.exists(stamp):
        os.remove(stamp)
    return rc, time.time() - t1


def big_dir(wd):
    """where the bulky files of work folder wd go: its mirror on the external SSD when that is mounted
    (and wd is not on it already), else wd itself"""
    real = os.path.realpath(wd)
    if not os.path.ismount(SSD) or real.startswith(SSD + '/'):
        return wd
    rel = os.path.relpath(real, os.path.realpath(FARM_ROOT))
    if rel.startswith('..'):
        rel = os.path.join('_elsewhere', real.lstrip('/'))
    d = os.path.join(BIG, rel)
    try:
        os.makedirs(d, exist_ok=True)
    except OSError:
        return wd
    return d


def big_file(wd, name, link=True):
    """the path to write the bulky file wd/name to: in big_dir(wd), with a symlink wd/name to it (if link).
    An older wd/name (the file this run would have overwritten, or a link) is removed first."""
    p = os.path.join(wd, name)
    drop(p)
    bd = big_dir(wd)
    if bd == wd:
        return p
    t = os.path.join(bd, name)
    if link:
        os.symlink(t, p)
    return t


def guard_kill(log):
    """97 or 98 (see GUARD) if the memory guard's "MEMGUARD: KILLING" line is in log, else None"""
    try:
        with open(log, errors='replace') as f:
            f.seek(max(0, os.fstat(f.fileno()).st_size - 65536))
            lines = [l for l in f.read().splitlines() if l.startswith('MEMGUARD: KILLING')]
    except OSError:
        return None
    if not lines:
        return None
    return 98 if 'short of memory' in lines[-1] else 97


def why(rc):
    """rc, with what it means when the memory guard stopped the job"""
    return '%s, %s' % (rc, GUARD[rc]) if rc in GUARD else str(rc)


def drop(*paths):
    for p in paths:
        if p and os.path.lexists(p):
            os.remove(p)


# ------------------------------------------------------------------------------------------------
# the design's ports, read by yosys
def read_cmds(a, files):
    inc = ' '.join('-I' + os.path.abspath(d) for d in a.incdir)
    dfn = ' '.join('-D' + d for d in a.define)
    sv = '-sv' if a.sv else ''
    return ['read_verilog %s %s %s %s' % (sv, dfn, inc, f) for f in files] + \
           ['read_verilog -overwrite %s %s %s %s' % (sv, dfn, inc, os.path.abspath(f)) for f in getattr(a, 'overwrite', [])]


def probe(a, files, wd):
    """top module name, ports [(name, dir, width)], whether it holds flip-flops/memories"""
    os.makedirs(wd, exist_ok=True)
    keep = getattr(a, 'keep', False)
    pj = big_file(wd, 'probe.json', link=keep)
    ys = read_cmds(a, files)
    top = a.top
    if not top:
        mods = []
        for f in files:
            mods += re.findall(r'^\s*module\s+(\w+)', open(f).read(), re.M)
        w = [m for m in mods if m.startswith('wht_')]
        top = w[0] if len(w) == 1 else (mods[0] if len(mods) == 1 else None)
    chp = ' '.join('-chparam %s %s' % tuple(p.split('=', 1)) for p in a.param)
    ys.append(('hierarchy -top %s %s' % (top, chp)) if top else 'hierarchy -auto-top')
    ys += ['proc', 'flatten', 'opt_clean', 'write_json %s' % pj]
    sf = os.path.join(wd, 'probe.ys')
    open(sf, 'w').write('\n'.join(ys) + '\n')
    # Yosys on the whole design: through heavy.sh unless --bg (a.heavy False)
    rc, _ = sh(runner(getattr(a, 'heavy', True)), [os.path.join(BIN, 'yosys'), '-q', '-l', os.path.join(wd, 'probe.log'), '-s', sf],
               os.path.join(wd, 'probe.out'), 600)
    if rc != 0:
        if not keep:
            drop(pj)
        raise SystemExit('yosys could not read the design (%s): see %s and probe.out' % (why(rc), os.path.join(wd, 'probe.log')))
    d = json.load(open(pj))
    if not keep:
        drop(pj)
    tops = [k for k, v in d['modules'].items() if str(v.get('attributes', {}).get('top', '0')).strip('0') != '']
    name = top or (tops[0] if tops else list(d['modules'])[0])
    if name not in d['modules']:   # parameterised: yosys renames to $paramod...
        cand = [k for k in d['modules'] if name in k]
        name = cand[0]
    m = d['modules'][name]
    ports = [(p, v['direction'], len(v['bits'])) for p, v in m['ports'].items()]
    seq = any(re.search(r'dff|dlatch|\$mem|\$sr\b|\$fsm', c['type'], re.I) for c in m['cells'].values())
    return (top or name), ports, seq


def harness_src(mod, ports, clk, outreg, params):
    ins = [(p, w) for p, d, w in ports if d == 'input' and p != clk]
    outs = [(p, w) for p, d, w in ports if d == 'output']
    if any(d == 'inout' for _, d, _ in ports):
        raise SystemExit('inout ports are not supported')
    NI = sum(w for _, w in ins)
    NO = sum(w for _, w in outs)
    if NI == 0 or NO == 0:
        raise SystemExit('the design needs at least one input bit and one output bit besides the clock')
    has_clk = any(p == clk for p, _, _ in ports)
    conn, lo = [], 0
    if has_clk:
        conn.append('.%s(clk)' % clk)
    for p, w in ins:
        conn.append('.%s(hin[%d:%d])' % (p, lo + w - 1, lo))
        lo += w
    lo = 0
    for p, w in outs:
        conn.append('.%s(od[%d:%d])' % (p, lo + w - 1, lo))
        lo += w
    par = ''
    if params:
        par = ' #(' + ', '.join('.%s(%s)' % tuple(p.split('=', 1)) for p in params) + ')'
    s = ['// Test harness written by fpga_measure.py.  dut = %s%s.' % (mod, ' + output register' if outreg else ''),
         '`default_nettype none', '(* keep_hierarchy *)',
         'module dut (input wire clk, input wire [%d:0] hin, output wire [%d:0] hout);' % (NI - 1, NO - 1),
         '    wire [%d:0] od;' % (NO - 1),
         '    %s%s core (%s);' % (mod, par, ', '.join(conn))]
    if outreg:
        s += ['    reg [%d:0] q;' % (NO - 1), '    always @(posedge clk) q <= od;', '    assign hout = q;']
    else:
        s += ['    assign hout = od;']
    s += ['endmodule', '',
          'module top (input wire clk, input wire sin, output wire sout);',
          '    reg [%d:0] h_sr;' % (NI - 1),
          ('    always @(posedge clk) h_sr <= {h_sr[%d:0], sin};' % (NI - 2)) if NI > 1 else
          '    always @(posedge clk) h_sr <= sin;',
          '    wire [%d:0] h_o;' % (NO - 1),
          '    dut u_dut (.clk(clk), .hin(h_sr), .hout(h_o));',
          '    reg [%d:0] h_acc;' % (NO - 1),
          ('    always @(posedge clk) h_acc <= {h_acc[%d:0], 1\'b0} ^ h_o;' % (NO - 2)) if NO > 1 else
          '    always @(posedge clk) h_acc <= h_o;',
          '    assign sout = h_acc[%d];' % (NO - 1),
          'endmodule', '`default_nettype wire', '']
    return '\n'.join(s), NI, NO


def yosys_stat(path):
    out, cur = {}, None
    for line in open(path):
        m = re.match(r'\s*===\s*(.+?)\s*===', line)
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


# ------------------------------------------------------------------------------------------------
# counting, per family
def synth_counts(fam, c):
    """counts from yosys' stat of module dut (cell type -> number)"""
    g = lambda *ks: sum(v for k, v in c.items() if k in ks)
    gp = lambda rx: sum(v for k, v in c.items() if re.match(rx, k))
    if fam == 'ice40':
        return {'y_lut': g('SB_LUT4'), 'y_carry': g('SB_CARRY'), 'y_ff': gp(r'SB_DFF'), 'y_dsp': g('SB_MAC16'),
                'y_bram': gp(r'SB_RAM40'), 'y_spram': g('SB_SPRAM256KA')}
    if fam == 'nexus':
        return {'y_lut4': g('LUT4'), 'y_ccu2': g('CCU2'), 'y_ff': gp(r'FD1P3'), 'y_mux': g('WIDEFN9'),
                'y_dsp': gp(r'MULT|MAC|PREADD|ACC54'), 'y_bram': gp(r'DP16K|PDP16K|SP16K|EBR'), 'y_lram': gp(r'LRAM'),
                'y_lutram': gp(r'DPR16X4'), 'y_lut_equiv': g('LUT4') + 2 * g('CCU2')}
    if fam == 'ecp5':
        return {'y_lut4': g('LUT4'), 'y_ccu2': g('CCU2C'), 'y_ff': g('TRELLIS_FF'), 'y_mux': gp(r'PFUMX|L6MUX21'),
                'y_dsp': gp(r'MULT18X18D|ALU54B'), 'y_bram': g('DP16KD'), 'y_lutram': gp(r'TRELLIS_DPR16X4'),
                'y_lut_equiv': g('LUT4') + 2 * g('CCU2C')}
    if fam == 'gowin':
        return {'y_lut': gp(r'LUT[1-4]$'), 'y_alu': g('ALU'), 'y_ff': gp(r'DFF'), 'y_mux': gp(r'MUX2'),
                'y_dsp': gp(r'MULT|PADD|ALU54'), 'y_bram': gp(r'^(SP|SDP|DP|DPB|SDPB|pROM)X?9?B?$|BSRAM'),
                'y_lutram': gp(r'RAM16')}
    if fam in ('xc7', 'xc7pnr'):
        luts = gp(r'LUT[1-6]$')
        return {'y_lut': luts, 'y_carry4': g('CARRY4'), 'y_ff': gp(r'FD[CPRS]E?(_1)?$'), 'y_srl': gp(r'SRL'),
                'y_muxf': gp(r'MUXF[78]'), 'y_dsp': gp(r'DSP48'), 'y_bram': gp(r'RAMB(18|36)'),
                'y_lutram': gp(r'RAM(32|64|128|256)'), 'y_lut_by_size': {k: v for k, v in c.items() if re.match(r'LUT[1-6]$', k)}}
    if fam == 'cyclonev':
        return {'y_alut_comb': gp(r'MISTRAL_ALUT[2-6]$|MISTRAL_NOT'), 'y_alut_arith': g('MISTRAL_ALUT_ARITH'),
                'y_ff': g('MISTRAL_FF'), 'y_dsp': gp(r'MISTRAL_MUL'), 'y_bram': gp(r'MISTRAL_M10K'),
                'y_lutram': gp(r'MISTRAL_MLAB'),
                'y_alm_estimate': (gp(r'MISTRAL_ALUT[2-6]$|MISTRAL_NOT') + g('MISTRAL_ALUT_ARITH') + 1) // 2}
    return {}


def bit(v):
    if isinstance(v, int):
        return v
    s = str(v).strip()
    if not s:
        return 0
    if set(s) <= set('01xz'):
        return int(s.replace('x', '0').replace('z', '0'), 2)
    try:
        return int(s)
    except ValueError:
        return 0


INFRA = re.compile(r'SB_IO|SB_GB|TRELLIS_IO|DCCA|IOB|IBUF|OBUF|BUFG|GSR|^VCC$|^GND$|OSC|TRELLIS_ECLKBUF')


def classify(fam, pk):
    """count the packed netlist's cells: design (dut), harness (har), infrastructure (io/clock/consts)"""
    d = json.load(open(pk))
    top = d['modules']['top']
    res = {'dut': {}, 'har': {}, 'infra': {}, 'unattributed_names': [], 'slices': {}}

    def add(w, k, n=1):
        res[w][k] = res[w].get(k, 0) + n

    for name, c in top['cells'].items():
        t = c['type']
        if 'u_dut.' in name:
            w = 'dut'
        elif INFRA.search(t) or name.startswith('$PACKER') or 'GND' in name or 'VCC' in name:
            w = 'infra'
        elif name.startswith('$nextpnr'):
            w = 'dut'      # a cell nextpnr made for a carry chain: only the design has carry chains
            res['unattributed_names'].append(name)
        else:
            w = 'har'
        p = c.get('parameters', {})
        conn = c.get('connections', {})
        add(w, 'cell:' + t)
        # the slice (ECP5: 2 LUT4 + 2 FF) or CLS (Gowin: the same) that placement put the cell in
        bel = str(c.get('attributes', {}).get('NEXTPNR_BEL', ''))
        mb = re.match(r'^(X\d+/Y\d+/SLICE[A-D])[._]', bel) or re.match(r'^(X\d+Y\d+)/(?:LUT|DFF|ALU)(\d)$', bel)
        if fam == 'xc7pnr':     # ax-k1: openXC7 BEL -> slice and LUT site (A-D)
            # placed only: "X98Y17/SLICE_X0Y0.D6LUT" (tile-local site); after routing: "SLICE_X35Y142/C6LUT"
            mx = re.match(r'^((?:X\d+Y\d+/)?SLICE_X\d+Y\d+)[./]([A-D]|CARRY4)', bel)
            if mx:
                res['slices'].setdefault(mx.group(1), set()).add(w)
                if t == 'SLICE_LUTX':
                    res.setdefault('lut_sites', {}).setdefault(mx.group(1) + mx.group(2), set()).add(w)
            mb = None
        if mb:
            key = mb.group(1) if fam in ('ecp5', 'nexus') else '%s/CLS%d' % (mb.group(1), int(mb.group(2)) // 2)
            res['slices'].setdefault(key, set()).add(w)
        if fam == 'ice40' and t == 'ICESTORM_LC':
            carry = bit(p.get('CARRY_ENABLE', 0)) != 0
            ff = bit(p.get('DFF_ENABLE', 0)) != 0
            init = bit(p.get('LUT_INIT', 0)) & 0xFFFF
            used = [k for k in ('I0', 'I1', 'I2', 'I3') if conn.get(k)]
            passthru = (not carry) and ff and len(used) == 1 and init in (2, 0xAAAA)
            add(w, 'lc')
            if ff:
                add(w, 'ff')
            if carry:
                add(w, 'carry')
                if not conn.get('O'):
                    add(w, 'carry_nolut')
            elif passthru:
                add(w, 'ff_only')
            elif ff:
                add(w, 'lut_ff')
            else:
                add(w, 'lut_only')
            if name.startswith('$nextpnr'):
                add(w, 'chain_extra')
        elif fam == 'ice40':
            if t in ('ICESTORM_DSP', 'SB_MAC16'):
                add(w, 'dsp')
            elif t in ('ICESTORM_RAM', 'SB_RAM40_4K'):
                add(w, 'bram')
            elif t in ('ICESTORM_SPRAM', 'SB_SPRAM256KA'):
                add(w, 'spram')
        elif fam == 'ecp5':
            if t == 'TRELLIS_COMB':
                mode = str(p.get('MODE', 'LOGIC')).strip()
                add(w, 'comb')
                add(w, 'comb_' + mode.lower())
            elif t == 'TRELLIS_FF':
                add(w, 'ff')
            elif t == 'TRELLIS_RAMW':
                add(w, 'ramw')
            elif t in ('MULT18X18D', 'ALU54B'):
                add(w, 'dsp_' + t.lower())
            elif t == 'DP16KD':
                add(w, 'bram')
            elif t in ('TRELLIS_SLICE',):
                add(w, 'slice')
        elif fam == 'nexus':
            if t == 'OXIDE_COMB':
                add(w, 'comb')
                add(w, 'comb_' + str(p.get('MODE', 'LOGIC')).strip().lower())
            elif t == 'OXIDE_FF':
                add(w, 'ff')
            elif re.match(r'(MULT9|MULT18|PREADD9|REG18|ACC54|MULT18X36|MULT36)_CORE', t):
                add(w, 'dsp_prim')
                if t == 'MULT9_CORE':
                    add(w, 'dsp_mult9')
            elif t in ('OXIDE_EBR', 'DP16K_MODE', 'PDP16K_MODE', 'SP16K_MODE'):
                add(w, 'bram')
            elif t in ('LRAM_CORE',):
                add(w, 'lram')
            elif t == 'RAMW':
                add(w, 'ramw')
        elif fam == 'xc7pnr':     # ax-k1: openXC7 packed cell types
            if t == 'SLICE_LUTX':
                add(w, 'lut')
                if 'PACKED_CARRY4$$' in name:   # a pass-through LUT the packer put on a CARRY4 S or DI input
                    add(w, 'lut_passthrough')
                if conn.get('CLK') or conn.get('WE'):   # a shift register (SRL16E/SRLC32E) or LUT RAM: clocked LUT
                    add(w, 'lut_srl_or_ram')
            elif t == 'SLICE_FFX':
                add(w, 'ff')
            elif t == 'CARRY4':
                add(w, 'carry4')
            elif t.startswith('DSP48'):
                add(w, 'dsp')
            elif t.startswith('RAMB'):
                add(w, 'bram')
            elif t.startswith(('F7MUX', 'F8MUX', 'SELMUX')):
                add(w, 'muxf')
        elif fam == 'gowin':
            if re.match(r'LUT[1-4]$', t):
                add(w, 'lut')
            elif t == 'ALU':
                add(w, 'alu')
            elif 'DFF' in t:
                add(w, 'ff')
            elif t.startswith('MUX2'):
                add(w, 'mux')
            elif re.match(r'MULT|PADD|ALU54', t):
                add(w, 'dsp')
            elif re.match(r'(SP|SDP|DP|SDPB|DPB)X?9?B?$|BSRAM', t):
                add(w, 'bram')
            elif t.startswith('RAM16'):
                add(w, 'lutram')
    return res


def pnr_fields(fam, cl, NI, NO):
    """the reported fields for a placed-and-routed run"""
    D, H = cl['dut'], cl['har']
    r = {}
    if fam == 'ice40':
        for k in ('lc', 'carry', 'carry_nolut', 'lut_only', 'lut_ff', 'ff_only', 'ff', 'chain_extra', 'dsp', 'bram', 'spram'):
            r['dut_' + k] = D.get(k, 0)
        r['har_lc'] = H.get('lc', 0)
        # harness: NI + NO flip-flop cells (each with its XOR or pass-through LUT)
        r['harness_ok'] = H.get('lc', 0) == NI + NO
    elif fam == 'ecp5':
        for k in ('comb', 'comb_logic', 'comb_ccu2', 'comb_dpram', 'comb_ramw', 'ff', 'ramw', 'bram'):
            r['dut_' + k] = D.get(k, 0)
        r['dut_dsp'] = D.get('dsp_mult18x18d', 0) + D.get('dsp_alu54b', 0)
        r['dut_mult18'] = D.get('dsp_mult18x18d', 0)
        r['har_comb'] = H.get('comb', 0)
        r['har_ff'] = H.get('ff', 0)
        r['harness_ok'] = H.get('ff', 0) == NI + NO and H.get('comb', 0) <= NO + 2
    elif fam == 'nexus':
        for k in ('comb', 'comb_logic', 'comb_ccu2', 'comb_dpram', 'ff', 'ramw', 'bram', 'lram', 'dsp_prim', 'dsp_mult9'):
            r['dut_' + k] = D.get(k, 0)
        r['har_comb'] = H.get('comb', 0)
        r['har_ff'] = H.get('ff', 0)
        r['harness_ok'] = H.get('ff', 0) == NI + NO and H.get('comb', 0) <= NO + 2
    elif fam == 'gowin':
        for k in ('lut', 'alu', 'ff', 'mux', 'dsp', 'bram', 'lutram'):
            r['dut_' + k] = D.get(k, 0)
        r['dut_lut_positions'] = D.get('lut', 0) + D.get('alu', 0)
        r['har_lut'] = H.get('lut', 0)
        r['har_ff'] = H.get('ff', 0)
        # nextpnr's gowin packer gives every flip-flop not fed by a LUT a pass-through LUT, so the
        # harness takes NI + NO flip-flops and up to NI + NO LUTs
        r['harness_ok'] = H.get('ff', 0) == NI + NO and H.get('lut', 0) <= NI + NO + 2
    elif fam == 'xc7pnr':     # ax-k1
        for k in ('lut', 'lut_passthrough', 'lut_srl_or_ram', 'ff', 'carry4', 'muxf', 'dsp', 'bram'):
            r['dut_' + k] = D.get(k, 0)
        # the LUT cells of the design itself (Vivado would put a LUT that drives a carry input into the carry's own
        # slice position; this openXC7 packer adds a pass-through LUT there instead: ax-k1, wave 16)
        r['dut_lut_user'] = r['dut_lut'] - r['dut_lut_passthrough']
        ls = cl.get('lut_sites', {})
        r['dut_lut_sites'] = sum(1 for v in ls.values() if 'dut' in v)       # physical 6-input LUT positions used
        r['har_lut'] = H.get('lut', 0)
        r['har_ff'] = H.get('ff', 0)
        r['harness_ok'] = H.get('ff', 0) == NI + NO and H.get('lut', 0) <= NO + 2
        sl = cl['slices']
        r['dut_slices_touched'] = sum(1 for v in sl.values() if 'dut' in v)
        r['dut_slices_shared_with_harness'] = sum(1 for v in sl.values() if 'dut' in v and len(v) > 1)
        # a 7-series slice: 4 LUT6 sites, 8 flip-flops, 1 CARRY4
        r['dut_slices_lower_bound'] = max((r['dut_lut_sites'] + 3) // 4, (r['dut_ff'] + 7) // 8, r['dut_carry4'])
    if fam in ('ecp5', 'gowin', 'nexus'):
        sl = cl['slices']
        r['dut_slices_touched'] = sum(1 for v in sl.values() if 'dut' in v)
        r['dut_slices_shared_with_harness'] = sum(1 for v in sl.values() if 'dut' in v and len(v) > 1)
        lut = r.get('dut_comb', r.get('dut_lut_positions', 0))
        r['dut_slices_lower_bound'] = (max(lut, r.get('dut_ff', 0)) + 1) // 2
    r['dut_cells_by_type'] = {k[5:]: v for k, v in sorted(D.items()) if k.startswith('cell:')}
    if cl['unattributed_names']:
        r['nextpnr_made_cells_counted_as_design'] = len(cl['unattributed_names'])
    return r


# ------------------------------------------------------------------------------------------------
def synthesise(a, chip, files, mod, ports, seq, wd):
    C = CHIPS[chip]
    os.makedirs(wd, exist_ok=True)
    if a.outreg == 'auto':
        outreg = 0 if seq else 1
    else:
        outreg = int(a.outreg)
    hsrc, NI, NO = harness_src(mod, ports, a.clk, outreg, a.param)
    synth = C['synth'] + ((' ' + a.synth_opts) if a.synth_opts else '')
    h = hashlib.sha256()
    for f in list(files) + list(getattr(a, 'overwrite', [])):   # ax-k1: --overwrite files count too (as-7's copy)
        h.update(open(f, 'rb').read())
    h.update(hsrc.encode())
    h.update(repr((synth, a.sv, a.define, a.incdir)).encode())
    key = h.hexdigest()[:16]
    jsn = os.path.join(wd, 'top.json')
    keyf = os.path.join(wd, 'synth.key')
    info = {'outreg': outreg, 'NI': NI, 'NO': NO, 'synth_cmd': synth, 'synth_key': key}
    if (os.path.exists(jsn) and os.path.exists(keyf) and open(keyf).read().strip() == key
            and os.path.exists(os.path.join(wd, 'stat_hier.txt'))):
        info['yosys_seconds'] = json.load(open(os.path.join(wd, 'synth_time.json')))['s'] if os.path.exists(os.path.join(wd, 'synth_time.json')) else None
        info['synth_cached'] = True
        return info, jsn
    open(os.path.join(wd, 'harness.v'), 'w').write(hsrc)
    drop(keyf)
    out = big_file(wd, 'top.json')      # on the SSD when mounted; wd/top.json is then a symlink to it
    if out != jsn:
        print('[fpga_measure] netlist %s (symlink %s)' % (out, jsn), file=sys.stderr, flush=True)
    ys = read_cmds(a, files) + ['read_verilog %s' % os.path.join(wd, 'harness.v'), 'hierarchy -top top', synth] + C.get('post', []) + [
                                'tee -q -o %s stat' % os.path.join(wd, 'stat_hier.txt'),
                                'setattr -mod -unset keep_hierarchy dut', 'flatten', 'clean',
                                'tee -q -o %s stat' % os.path.join(wd, 'stat_flat.txt'),
                                'write_json %s' % out]
    sf = os.path.join(wd, 'synth.ys')
    open(sf, 'w').write('\n'.join(ys) + '\n')
    rc, dt = sh(runner(a.heavy), [os.path.join(BIN, 'yosys'), '-q', '-l', os.path.join(wd, 'yosys.log'), '-s', sf],
                os.path.join(wd, 'yosys.out'), timeout=a.timeout)
    info['yosys_seconds'] = round(dt, 2)
    if rc != 0:
        info['error'] = 'yosys failed (%s), see %s' % (why(rc), os.path.join(wd, 'yosys.log'))
        return info, None
    open(keyf, 'w').write(key + '\n')
    json.dump({'s': round(dt, 2)}, open(os.path.join(wd, 'synth_time.json'), 'w'))
    return info, jsn


def place_route(a, chip, jsn, wd, seed, NI, NO):
    C = CHIPS[chip]
    fam = C['family']
    base = os.path.join(wd, 's%d_f%g' % (seed, a.freq))
    # the packed netlist and the routed image are bulky: written next to the SSD copy of top.json
    pk = big_file(wd, os.path.basename(base) + '.packed.json', link=a.keep)
    asc = big_file(wd, os.path.basename(base) + '.asc', link=a.keep) if fam == 'ice40' and a.icetime else None
    big = os.path.getsize(jsn) > BG_MAX_MB * 1e6
    heavy = a.heavy or big or fam not in BG_FAMILIES
    if heavy and not a.heavy:
        print('[fpga_measure] --bg refused for seed %d: %s, so nextpnr runs through heavy.sh' % (
              seed, 'the netlist is over %g MB' % BG_MAX_MB if big else 'nextpnr takes 0.35 to 0.7 GB on %s even for a tiny design'
              % fam), file=sys.stderr, flush=True)
    pbin = os.path.join(OPENXC7, 'bin') if fam == 'xc7pnr' else BIN
    cmd = [os.path.join(pbin, C['pnr'])] + C['args'] + [
        '--json', jsn, '--seed', str(seed), '--freq', str(a.freq), '--timing-allow-fail',
        '--report', base + '.report.json', '--write', pk, '-q', '-l', base + '.nextpnr.log'] + (a.pnr_opts.split() if a.pnr_opts else [])
    if C.get('cons'):
        kind, txt = C['cons']
        if kind == 'xdc':      # ax-k1: three pins (clk, sin, sout), LVCMOS33
            txt = ''.join('set_property LOC %s [get_ports %s]\nset_property IOSTANDARD LVCMOS33 [get_ports %s]\n' % (pin, port, port)
                          for pin, port in zip(txt.split(), ('clk', 'sin', 'sout')))
        cf_ = os.path.join(wd, 'top.' + kind)
        open(cf_, 'w').write(txt)
        cmd += {'pcf': ['--pcf', cf_], 'cst': ['--vopt', 'cst=' + cf_], 'pdc': ['--pdc', cf_], 'xdc': ['-o', 'xdc=' + cf_]}[kind]
    if asc:
        cmd += ['--asc', asc]
    res = {'seed': seed}
    try:
        rc, dt = sh(runner(heavy), cmd, base + '.nextpnr.out', timeout=a.timeout)
        res['pnr_seconds'] = round(dt, 2)
        if rc != 0:
            log = open(base + '.nextpnr.log').read() if os.path.exists(base + '.nextpnr.log') else ''
            m = re.findall(r'ERROR:.*', log)
            res['error'] = 'nextpnr failed (%s): %s' % (why(rc), m[-1] if m else 'see ' + base + '.nextpnr.log and .out')
            return res
        rep = json.load(open(base + '.report.json'))
        res['chip_used'] = {k: v['used'] for k, v in rep['utilization'].items() if v['used']}
        fm = rep.get('fmax', {})
        if fm:
            res['fmax_mhz'] = round(min(v['achieved'] for v in fm.values()), 2)
            res['clock_nets'] = len(fm)
        cps = [p for p in rep.get('critical_paths', []) if p.get('from', '').startswith('posedge') and p.get('to', '').startswith('posedge')]
        if cps and cps[0].get('path'):
            segs = cps[0]['path']
            a0, a1 = segs[0]['from']['cell'], segs[-1]['to']['cell']
            res['crit'] = ('dut' if 'u_dut.' in a0 else 'harness') + '->' + ('dut' if 'u_dut.' in a1 else 'harness')
            res['crit_logic_steps'] = sum(1 for s in segs if s.get('type') == 'logic')
        cl = classify(fam, pk)
        res.update(pnr_fields(fam, cl, NI, NO))
        if asc and os.path.exists(asc):
            dev = 'hx8k' if '--hx8k' in C['args'] else 'up5k'
            pkg = C['args'][C['args'].index('--package') + 1]
            icmd = [os.path.join(BIN, 'icetime'), '-d', dev, '-P', pkg, '-t', '-m', '-r', base + '.icetime.rpt', asc]
            rc, dt = sh(runner(heavy), icmd, base + '.icetime.out', timeout=a.timeout)
            txt = open(base + '.icetime.out').read()
            m = re.search(r'(?:Timing estimate|Total path delay):\s*([\d.]+)\s*ns\s*\(([\d.]+)\s*MHz\)', txt)
            if m:
                res['fmax_icetime_mhz'] = float(m.group(2))
        return res
    finally:
        if not a.keep:
            drop(pk, asc)


def summarise(rows):
    skip = {'seed', 'NI', 'NO', 'outreg', 'freq_target', 'clock_nets'}
    keys = sorted({k for r in rows for k, v in r.items() if isinstance(v, (int, float)) and not isinstance(v, bool)
                   and k not in skip and not k.startswith('y_')})
    out = {}
    for k in keys:
        vals = [r[k] for r in rows if isinstance(r.get(k), (int, float))]
        if vals:
            out[k] = {'med': statistics.median(vals), 'min': min(vals), 'max': max(vals)}
    return out


def measure_chip(a, chip, files, mod, ports, seq, tag):
    C = CHIPS[chip]
    fam = C['family']
    wd = os.path.join(a.work, tag, chip)
    global PLATFORM
    if PLATFORM is None:
        PLATFORM = tool_versions()
    head = {'tag': tag, 'chip': chip, 'module': mod, 'files': [os.path.basename(f) for f in files], 'freq_target': a.freq,
            'pnr_opts': a.pnr_opts,
            'platform': PLATFORM, 'param': a.param,
            'synth_opts': a.synth_opts, 'pnr': bool(C['pnr']) and not a.no_pnr}
    info, jsn = synthesise(a, chip, files, mod, ports, seq, wd)
    head.update(info)
    st = yosys_stat(os.path.join(wd, 'stat_hier.txt')) if jsn else {}
    dutc = st.get('dut', {})
    head['yosys_dut_cells'] = {k: v for k, v in dutc.items() if not k.startswith('$') and k not in ('cells', 'wires', 'wire_bits', 'public_wires', 'public_wire_bits', 'ports', 'port_bits', 'memories', 'memory_bits', 'processes')}
    head.update(synth_counts(fam, head['yosys_dut_cells']))
    rows = []
    if not jsn or not head['pnr']:
        head['synthesis_only'] = True
        print(json.dumps(head), flush=True)
        if a.out:
            open(a.out, 'a').write(json.dumps(head) + '\n')
        return [head]
    seeds = [int(s) for s in a.seed_list.split(',')] if a.seed_list else list(range(1, a.seeds + 1))
    with cf.ThreadPoolExecutor(max_workers=max(1, a.jobs)) as ex:
        futs = {ex.submit(place_route, a, chip, jsn, wd, s, info['NI'], info['NO']): s for s in seeds}
        for f in cf.as_completed(futs):
            r = dict(head)
            r.update(f.result())
            rows.append(r)
            print(json.dumps(r), flush=True)
            if a.out:
                open(a.out, 'a').write(json.dumps(r) + '\n')
    rows.sort(key=lambda r: r['seed'])
    ok = [r for r in rows if 'error' not in r]
    summ = {'summary': True, 'tag': tag, 'chip': chip, 'module': mod, 'freq_target': a.freq, 'synth_opts': a.synth_opts,
            'seeds': [r['seed'] for r in ok], 'failed_seeds': [r['seed'] for r in rows if 'error' in r],
            'outreg': info.get('outreg'), 'NI': info.get('NI'), 'NO': info.get('NO'),
            'harness_ok_all': all(r.get('harness_ok') for r in ok) if ok else None,
            'stats': summarise(ok)}
    for k in ('y_lut', 'y_carry', 'y_ff', 'y_dsp', 'y_lut4', 'y_ccu2', 'y_alu', 'y_lut_equiv'):
        if k in head:
            summ[k] = head[k]
    print(json.dumps(summ), flush=True)
    if a.out:
        open(a.out, 'a').write(json.dumps(summ) + '\n')
    return rows + [summ]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[1], formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('files', nargs='*')
    ap.add_argument('--chip', default='ice40-hx8k')
    ap.add_argument('--list-chips', action='store_true')
    ap.add_argument('--seeds', type=int, default=5)
    ap.add_argument('--seed-list', default=None)
    ap.add_argument('--top', default=None)
    ap.add_argument('--param', action='append', default=[], help='NAME=VALUE, a parameter of the top module')
    ap.add_argument('--clk', default=None, help='clock port (default: the first of clk, clock, i_clk, aclk, clk_i, CLK)')
    ap.add_argument('--outreg', default='auto', choices=['auto', '0', '1'])
    ap.add_argument('--freq', type=float, default=400.0, help='nextpnr clock target in MHz (timing-driven placement); --timing-allow-fail is always on')
    ap.add_argument('--synth-opts', default='', help='extra options for the synth_* command, e.g. "-dff" or "-nodsp"')
    ap.add_argument('--no-pnr', action='store_true')
    ap.add_argument('--jobs', type=int, default=1, help='seeds placed in parallel (each one nextpnr process in a heavy slot of '
                    'its own; at most %d; 1 when started inside a heavy slot)' % SLOTS)
    ap.add_argument('--heavy', action='store_true', help='(the default now) run yosys/nextpnr/icetime through heavy.sh, '
                    'each call in one of the %d heavy slots of the whole Mac' % SLOTS)
    ap.add_argument('--bg', action='store_true', help='run them through bg.sh instead: only for tiny designs; still capped '
                    'by the memory guard; nextpnr goes to heavy.sh anyway on ECP5 and Nexus and for a netlist over %g MB' % BG_MAX_MB)
    ap.add_argument('--keep', action='store_true', help='keep probe.json and each seed\'s packed netlist and routed image')
    ap.add_argument('--work', default=os.path.join(os.getcwd(), 'fpga_work'),
                    help='work folder (default ./fpga_work); its bulky netlists go to the external SSD (DISK in '
                         'the header of this file)')
    ap.add_argument('--tag', default=None)
    ap.add_argument('--out', default=None, help='append every JSON line to this file')
    ap.add_argument('--icetime', action='store_true', help='iCE40: also run icetime on the routed image')
    ap.add_argument('--sv', action='store_true')
    ap.add_argument('--define', action='append', default=[])
    ap.add_argument('--incdir', action='append', default=[])
    ap.add_argument('--pnr-opts', default='', help='ax-k1: extra nextpnr options, e.g. "--router router2 --threads 4"')
    ap.add_argument('--overwrite', action='append', default=[], help='as-7/av-7: files read after the design files with '
                    'read_verilog -overwrite (replace modules without editing their files)')
    ap.add_argument('--timeout', type=int, default=3600, help='seconds per tool run (the wait for a slot does not count)')
    a = ap.parse_args()
    if a.list_chips:
        for k, v in CHIPS.items():
            print('%-12s %-10s %s' % (k, 'P&R' if v['pnr'] else 'synth only', v['synth']))
        return 0
    if not a.files:
        ap.error('no design file')
    if a.bg and a.heavy:
        ap.error('--bg and --heavy together')
    a.heavy = not a.bg
    if os.environ.get('FARM_HEAVY_SLOT') and a.jobs > 1:
        print('[fpga_measure] inside heavy slot %s already: --jobs %d -> 1, so that one slot holds one place-and-route'
              % (os.environ['FARM_HEAVY_SLOT'], a.jobs), file=sys.stderr, flush=True)
        a.jobs = 1
    if a.jobs > SLOTS:
        print('[fpga_measure] --jobs %d -> %d (%d heavy slots for the whole Mac)' % (a.jobs, SLOTS, SLOTS), file=sys.stderr, flush=True)
        a.jobs = SLOTS
    for s in (signal.SIGTERM, signal.SIGHUP, signal.SIGINT):
        signal.signal(s, stop)
    os.environ['PATH'] = BIN + ':' + os.environ.get('PATH', '')
    files = [os.path.abspath(f) for f in a.files]
    chips = list(CHIPS) if a.chip == 'all' else a.chip.split(',')
    for c in chips:
        if c not in CHIPS:
            ap.error('unknown chip %s; --list-chips' % c)
    tag0 = a.tag or os.path.splitext(os.path.basename(files[0]))[0]
    mod, ports, seq = probe(a, files, os.path.join(a.work, tag0, '_probe'))
    if a.clk is None:
        names = [p for p, d, w in ports if d == 'input' and w == 1]
        a.clk = next((n for n in CLOCK_NAMES if n in names), '__noclock__')
    for c in chips:
        measure_chip(a, c, files, mod, ports, seq, tag0)
    return 0


if __name__ == '__main__':
    sys.exit(main())
