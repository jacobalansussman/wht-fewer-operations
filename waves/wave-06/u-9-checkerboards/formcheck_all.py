import sys, glob, io, contextlib, traceback
sys.argv = sys.argv[:1]
src = open("formcheck.py").read().split("for fn in sys.argv[1:]:")[0]
exec(src)
I = "waves/wave-06/"
files = []
for pat in ("h-1-staircase3/*.txt", "h-3-orecord/*.txt", "h-6-classhub/*.txt", "g-1-tightwires/*.txt", "e2-0-pieces/*.txt", "p-*/*.txt", "u-*/*.txt", "g-6-twosteps/*.txt", "h-0-onepergate/*.txt", "j-machine/*.txt"):
    files += sorted(glob.glob(I + pat))
seen = 0
for fn in files:
    try:
        N, gates, order, wires = parse(fn)
        if N < 4 or N > 64 or gates < N or gates > 400: continue
        if max(len(t2) for _, t2 in order) > 2: continue
        H = [[(-1) ** bin(y & x).count("1") for x in range(N)] for y in range(N)]
        got = set()
        for name, _ in order:
            v = wires[name]
            if not any(v): continue
            nz = [a for a in v if a]; c = abs(nz[0])
            for y in range(N):
                if all(a == c * b for a, b in zip(v, H[y])) or all(a == -c * b for a, b in zip(v, H[y])): got.add(y)
        if len(got) != N: continue
        k = N.bit_length() - 1
        nonform = []; noncoset = []; sets = set(); spaces = set()
        for name, t2 in order:
            v = wires[name]; nz = [abs(a) for a in v if a]
            if not nz: continue
            if len(set(nz)) != 1: nonform.append(name)
            sup = [x for x in range(N) if v[x]]; sets.add(frozenset(sup))
            ok, sp = is_coset(sup)
            if not ok: noncoset.append(name)
            else: spaces.add(sp)
        laminar = all(a <= b or b <= a or not (a & b) for a in sets for b in sets)
        chain = all(a <= b or b <= a for a in spaces for b in spaces)
        seen += 1
        inclass = (not nonform) and (not noncoset) and laminar and chain
        print(f"{fn[len(I):]}: N={N} gates {gates} floor {N - 1 + k * N // 2} | non-form wires {len(nonform)}, non-coset sets {len(noncoset)}, one tree {laminar}, one flag {chain} | IN THE CLASS: {inclass}{'  ** BELOW THE FLOOR **' if inclass and gates < N - 1 + k * N // 2 else ''}", flush=True)
    except Exception as e:
        pass
print("complete transform circuits parsed:", seen)
