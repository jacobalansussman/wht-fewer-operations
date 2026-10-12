#!/usr/bin/env python3
"""tables.py -- turn the raw outputs of bench_size (raw/<machine>-<build>.txt) into the tables of bench.md.

    python3 -B tables.py            writes bench.md = bench-head.md + the tables + bench-tail.md
    python3 -B tables.py --print    prints the tables only

Time of a transform = time of (copy, transform) minus time of (copy): minimum minus minimum, median minus median.
Ratios are quotients of the minima (and, in one column, of the medians).  Below 1: the new kernel took less time.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
VARS = ["copy", "r2", "r8", "new_exact", "new_scaled"]


def parse(path):
    rows, reps, meta = {}, {}, {"checks_int": 0, "checks_real": 0, "ok": False, "lines": []}
    for line in open(path):
        w = line.split()
        if line.startswith("ROW "):
            k, n, v = int(w[1]), int(w[2]), w[3]
            rows.setdefault(k, {})[v] = dict(n=n, reps=int(w[4]), loop=float(w[5]), mn=float(w[6]), med=float(w[7]),
                                             mx=float(w[8]), cpu=float(w[9]))
        elif line.startswith("REP "):
            reps.setdefault(int(w[1][2:]), {})[w[2]] = [float(x) for x in w[3:]]
        elif line.startswith("CHECK k=") and "integer input" in line:
            meta["checks_int"] += 1
        elif line.startswith("CHECK k=") and "real input" in line:
            meta["checks_real"] += 1
        elif line.startswith("CHECK OK"):
            meta["ok"] = True
        elif line.startswith(("machine:", "compiler:", "build ", "start:", "end:", "load:")) or "count:" in line:
            meta["lines"].append(line.strip())
    return rows, reps, meta


def ops(k):
    """count (O) at N = 2^k as the C program does it: (textbook, new exact, new up to scale), in units of N."""
    r, m = k % 3, k // 3
    scaled = r + 2.5 * m
    return k, scaled + (1 if m > 0 else 0), scaled


def commas(n):
    return f"{n:,}"


def table(rows):
    out = []
    out.append("| k | N | array | radix 2 | textbook radix 8 | new, exact | new, up to scale | exact / radix 8 | exact / radix 2 "
               "| scale / radix 8 | scale / radix 2 | exact / radix 8 (medians) | largest spread | shortest loop |")
    out.append("|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|")
    for k in sorted(rows):
        R = rows[k]
        c = R["copy"]
        t = {v: (R[v]["mn"] - c["mn"], R[v]["med"] - c["med"]) for v in VARS[1:]}
        spread = max((R[v]["med"] - R[v]["mn"]) / R[v]["mn"] for v in VARS)
        loop = min(R[v]["loop"] for v in VARS)
        b = 8 << k
        size = f"{b} B" if b < 1024 else (f"{b // 1024} KB" if b < 1 << 20 else f"{b >> 20} MB")
        cell = lambda v: f"{t[v][0]:.3f} / {t[v][1]:.3f}"
        out.append(f"| {k} | {commas(1 << k)} | {size} | {cell('r2')} | {cell('r8')} | {cell('new_exact')} | {cell('new_scaled')} "
                   f"| {t['new_exact'][0] / t['r8'][0]:.3f} | {t['new_exact'][0] / t['r2'][0]:.3f} "
                   f"| {t['new_scaled'][0] / t['r8'][0]:.3f} | {t['new_scaled'][0] / t['r2'][0]:.3f} "
                   f"| {t['new_exact'][1] / t['r8'][1]:.3f} | {100 * spread:.0f}% | {loop:.2f} s |")
    return "\n".join(out)


def ops_table(ks):
    out = ["| k | N | textbook operations | new, exact | new, up to scale | exact / textbook | scale / textbook |",
           "|--:|--:|--:|--:|--:|--:|--:|"]
    for k in ks:
        n = 1 << k
        tb, ex, sc = ops(k)
        out.append(f"| {k} | {commas(n)} | {commas(int(tb * n))} | {commas(int(ex * n))} | {commas(int(sc * n))} "
                   f"| {ex / tb:.3f} | {sc / tb:.3f} |")
    return "\n".join(out)


def ratios(rows, k):
    R = rows[k]
    c = R["copy"]["mn"]
    t = {v: R[v]["mn"] - c for v in VARS[1:]}
    return t["new_exact"] / t["r8"], t["new_scaled"] / t["r8"], t["new_exact"] / t["r2"], t["r8"]


def repeat_table():
    """the second run of everything (raw/<machine>2-<build>.txt) beside the first: do the ratios repeat?"""
    cols, data = [], {}
    for m, mn in (("mac", "Mac"), ("linux", "Linux")):
        for b in ("scalar", "vec"):
            p1 = os.path.join(HERE, "raw", f"{m}-{b}.txt")
            p2 = os.path.join(HERE, "raw", f"{m}2-{b}.txt")
            if not (os.path.exists(p1) and os.path.exists(p2)):
                continue
            r1, _, m1 = parse(p1)
            r2, _, m2 = parse(p2)
            if not (m1["ok"] and m2["ok"]):
                continue
            cols.append(f"{mn} {'scalar' if b == 'scalar' else 'vectorised'}")
            data[cols[-1]] = (r1, r2)
    if not cols:
        return ""
    ks = sorted(next(iter(data.values()))[0])
    out = ["### Table 5. Do the ratios repeat? The first run beside the main run: new exact / textbook radix 8\n",
           "Each cell: the ratio in the first run, the ratio in the main run (from the minima), then in brackets the textbook "
           "radix 8 time of the main run divided by that of the first run (1.00 means the machine gave the same time twice).\n",
           "| k | " + " | ".join(cols) + " |", "|--:|" + "--:|" * len(cols)]
    worst = {c: 0.0 for c in cols}
    for k in ks:
        cells = []
        for c in cols:
            a, b = ratios(data[c][0], k), ratios(data[c][1], k)
            worst[c] = max(worst[c], abs(a[0] - b[0]))
            cells.append(f"{a[0]:.3f}, {b[0]:.3f} [{b[3] / a[3]:.2f}]")
        out.append(f"| {k} | " + " | ".join(cells) + " |")
    out.append("| largest change of the ratio | " + " | ".join(f"{worst[c]:.3f}" for c in cols) + " |")
    out.append("")
    out.append("The same for new, up to scale / textbook radix 8 (first run, main run):\n")
    out += ["| k | " + " | ".join(cols) + " |", "|--:|" + "--:|" * len(cols)]
    for k in ks:
        out.append(f"| {k} | " + " | ".join(f"{ratios(data[c][0], k)[1]:.3f}, {ratios(data[c][1], k)[1]:.3f}" for c in cols) + " |")
    return "\n".join(out) + "\n"


def pass_table(path):
    out = ["| stride | textbook 8-point pass | new pass | new pass with scaled stores | new / textbook | scaled / textbook |",
           "|--:|--:|--:|--:|--:|--:|"]
    ok = False
    info = []
    for line in open(path):
        w = line.split()
        if line.startswith("PASS "):
            out.append(f"| {w[1]} | {float(w[2]):.3f} / {float(w[3]):.3f} | {float(w[4]):.3f} / {float(w[5]):.3f} "
                       f"| {float(w[6]):.3f} / {float(w[7]):.3f} | {w[8]} | {w[9]} |")
        elif line.startswith("CHECK OK"):
            ok = True
        elif line.startswith(("build ", "start:", "load:")):
            info.append(f"- `{line.strip()}`")
    return "\n".join(info) + f"\n- check (new pass = half the textbook pass, exactly): {'passed at every stride' if ok else 'MISSING'}\n\n" + "\n".join(out) + "\n"


def section(title, p):
    if not os.path.exists(p):
        return f"### {title}\n\n(no raw output: {os.path.relpath(p, HERE)})\n", None
    rows, reps, meta = parse(p)
    ks = sorted(rows)
    head = [f"### {title}", "", f"Raw output: `{os.path.relpath(p, HERE)}`", ""]
    head += [f"- `{x}`" for x in meta["lines"]]
    head.append(f"- checks before timing: whole-number input, exact equality, {meta['checks_int']} sizes passed; "
                f"real input, up to rounding, {meta['checks_real']} sizes passed; "
                f"last line of the program: {'CHECK OK' if meta['ok'] else 'MISSING (run not complete)'}")
    head.append(f"- rounds per cell: {len(next(iter(reps[ks[0]].values()))) if ks else 0}")
    head.append("")
    return "\n".join(head) + "\n" + table(rows) + "\n", ks


def main():
    parts = []
    names = {"mac": "Mac mini (Apple M4)", "linux": "rented Linux machine"}
    builds = {"scalar": "scalar build", "vec": "vectorised build"}
    ks = None
    n = 0
    for m in ("mac", "linux"):
        for b in ("scalar", "vec"):
            n += 1
            p = os.path.join(HERE, "raw", f"{m}2-{b}.txt")
            sec, k2 = section(f"Table {n}. {names[m]}, {builds[b]} (main run)", p)
            ks = k2 or ks
            parts.append(sec)
    rep = repeat_table()
    if rep:
        parts.append(rep)
    p = os.path.join(HERE, "raw", "linux-O3novec.txt")
    if os.path.exists(p):
        parts.append(section("Table 6. Control: Linux machine, scalar code at -O3 (the flags of the earlier runs)", p)[0])
    for m in ("mac", "linux"):
        for b in ("scalar", "vec"):
            p = os.path.join(HERE, "raw", f"{m}-pass-{b}.txt")
            if os.path.exists(p):
                parts.append(f"### Control: one 8-point pass by stride, {names[m]}, {builds[b]}\n\n"
                             f"Raw output: `raw/{m}-pass-{b}.txt`. Cells: minimum / median, nanoseconds per point for ONE pass "
                             f"over 2,048 numbers.\n\n" + pass_table(p))
    if ks:
        parts.append("### Table 7. Operation count at the same sizes (count (O): every operation costs one)\n\n"
                     "As the C program does it: k mod 3 textbook layers, then 8-point passes of 20 operations per 8 points, "
                     "then N multiplications for the exact form.\n\n" + ops_table(ks) + "\n")
    body = "\n".join(parts)
    if "--print" in sys.argv:
        print(body)
        return
    head = open(os.path.join(HERE, "bench-head.md")).read() if os.path.exists(os.path.join(HERE, "bench-head.md")) else ""
    tail = open(os.path.join(HERE, "bench-tail.md")).read() if os.path.exists(os.path.join(HERE, "bench-tail.md")) else ""
    open(os.path.join(HERE, "bench.md"), "w").write(head + "\n" + body + "\n" + tail)
    print("wrote bench.md")


if __name__ == "__main__":
    main()
