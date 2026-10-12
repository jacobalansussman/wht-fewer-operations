# v-0: close the 16 residual cases on the chain tree.  An 18-gate play needs exactly 4 pair wires (one per pair node), one of the
# 16 sets F of four-wires printed by floor8p, and exactly 10 full wires = the 8 rows + 2 others.  Enumerate all of it in the
# PARTNER-FREE game (a flip on any node is allowed with no partner; a restriction of a held full wire to a half is allowed with no partner).
from itertools import combinations, product
def n8(m): return m^0xFF if m&1 else m
def n4(m): return m^0xF if m&1 else m
gens=[1<<i for i in range(8)]+[0x03,0x0C,0x30,0xC0,0x0F]
g4=[1,2,4,8,0x3,0xC]
rows=[]
for y in range(8):
    m=0
    for x in range(8):
        if bin(x&y).count('1')&1: m|=1<<x
    rows.append(n8(m))
allfull=[m for m in range(256) if not m&1]
others=[m for m in allfull if m not in rows]
Fs=[int(l.split('=')[1]) for l in open('tight.txt')]
passed=0; plays=0; quick=0
for F in Fs:
    FL=[a<<1 for a in range(8) if F>>a&1]; FR=[b<<1 for b in range(8) if F>>(8+b)&1]
    J={n8(a|(b<<4)) for a in FL for b in FR}|{n8(a|((b^0xF)<<4)) for a in FL for b in FR}
    for e in combinations(others,2):
        W=set(rows)|set(e)
        held=W&J; ch=True
        while ch:
            ch=False
            for w in W-held:
                if any(n8(w^g) in held for g in gens): held.add(w); ch=True
        if held!=W: continue
        quick+=1
        # now charge the four-wires: 16 choices of one pair wire per pair node (pattern 0 = ++, 2 = +-)
        for P in product([0,2],repeat=4):
            jl={n4(P[0]|(P[1]<<2)), n4(P[0]|((P[1]^3)<<2))}; jr={n4(P[2]|(P[3]<<2)), n4(P[2]|((P[3]^3)<<2))}
            dl=set(); dr=set(); dw=set(); ch=True
            while ch:
                ch=False
                for a in FL:
                    if a in dl: continue
                    if a in jl or any(n4(a^g) in dl for g in g4) or any((n4(w&0xF)==a) for w in dw): dl.add(a); ch=True
                for b in FR:
                    if b in dr: continue
                    if b in jr or any(n4(b^g) in dr for g in g4) or any((n4(w>>4)==b) for w in dw): dr.add(b); ch=True
                for w in W-dw:
                    a=n4(w&0xF); b=n4(w>>4)
                    if (a in dl and b in dr) or any(n8(w^g) in dw for g in gens): dw.add(w); ch=True
            if set(rows)<=dw: plays+=1; print("PLAY WITH 18 WIRES:",F,P,sorted(W))
print("sets F:",len(Fs),"| (F, two extra full wires) for which the 10 full wires hang together when F is free:",quick,"| of these, legal 18-wire plays once the four-wires must themselves be made (16 choices of pair wires each):",plays)
for F in Fs[:4]:
    print("  example F: left",[format(a<<1,'04b')[::-1] for a in range(8) if F>>a&1],"right",[format(b<<1,'04b')[::-1] for b in range(8) if F>>(8+b)&1],"(1 = minus sign, addresses in order)")
