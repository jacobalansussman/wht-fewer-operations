import re, subprocess, sys, collections
def funcs(path):
    out = subprocess.run(["objdump", "-d", "--no-show-raw-insn", path], capture_output=True, text=True).stdout
    f = {}; cur = None
    for line in out.splitlines():
        m = re.match(r"^[0-9a-f]+ <(.+)>:$", line)
        if m: cur = m.group(1); f[cur] = []; continue
        m = re.match(r"^\s*([0-9a-f]+):\s+(\S+)\s*(.*)$", line)
        if m and cur: f[cur].append(m.group(2))
    return f
F = funcs(sys.argv[1])
def hist(names): 
    c = collections.Counter()
    for n in names: c.update(F[n])
    return c
for pre, a, b in [("wht_f_", "Tp", "G19p"), ("wht_f_", "Tp", "G19ap"), ("wht_d_", "Tp", "G19p"), ("wht_i_", "Tp", "G19p")]:
    for part in ["_rec", "_pass3", ""]:
        ha, hb = hist([pre + a + part]), hist([pre + b + part])
        d = {k: hb[k] - ha[k] for k in sorted(set(ha) | set(hb)) if hb[k] != ha[k]}
        print("%s%s%s (%d instr) against %s%s%s (%d instr): differences %s" % (pre, b, part, sum(hb.values()), pre, a, part, sum(ha.values()), d))
