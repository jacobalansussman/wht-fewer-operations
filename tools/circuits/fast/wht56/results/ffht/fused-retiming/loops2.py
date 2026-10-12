import re, subprocess, sys, collections
out = subprocess.run(["objdump", "-d", "--no-show-raw-insn", sys.argv[1]], capture_output=True, text=True).stdout
funcs = {}; cur = None
for line in out.splitlines():
    m = re.match(r"^[0-9a-f]+ <(.+)>:$", line)
    if m: cur = m.group(1); funcs[cur] = []; continue
    m = re.match(r"^\s*([0-9a-f]+):\s+(\S+)\s*(.*)$", line)
    if m and cur: funcs[cur].append((int(m.group(1), 16), m.group(2), m.group(3)))
for name in sys.argv[2:]:
    ins = funcs[name]; loops = []
    for a, mn, ops in ins:
        if mn.startswith("j"):
            m = re.match(r"([0-9a-f]+) <", ops)
            if m and int(m.group(1), 16) < a: loops.append((int(m.group(1), 16), a))
    print("==", name, len(ins), "instructions")
    for t, a in sorted(loops):
        body = [(x, mn, ops) for x, mn, ops in ins if t <= x <= a]
        inner = not any(t < t2 and a2 < a for t2, a2 in loops if (t2, a2) != (t, a))
        if not inner: continue
        c = collections.Counter(mn for _, mn, _ in body)
        grp = collections.Counter()
        for x, mn, ops in body:
            if re.match(r"v(add|sub)p", mn): grp["add/sub"] += 1
            elif re.match(r"vf(n?m)(add|sub)", mn): grp["fused"] += 1
            elif re.match(r"vperm|vshuf|vpshuf", mn): grp["shuffle"] += 1
            elif re.match(r"vxorp|vpsign", mn): grp["sign"] += 1
            elif mn.startswith("vmov"):
                if "rsp" in ops or "rbp" in ops: grp["stack move"] += 1
                elif ops.count("ymm") == 2 or ops.count("xmm") == 2: grp["register copy"] += 1
                elif ops.strip().endswith(")"): grp["store"] += 1
                else: grp["load"] += 1
            elif mn.startswith("vbroadcast"): grp["broadcast"] += 1
            else: grp["other:" + mn] += 1
        memops = sum(1 for x, mn, ops in body if "(" in ops and not mn.startswith(("vmov", "lea", "nop", "j")))
        print("   inner loop %x..%x: %d instructions %s; arithmetic/shuffle instructions that read memory themselves: %d" % (t, a, len(body), dict(grp), memops))
