"""make_bench.py ISA -> bench_ISA.c : every circuit, plain and port-balanced, as one radix-8/16 pass over a
K x COLS fp32 array in L1 (COLS = 256).  Correctness: exact on random small integers vs a direct H x.
Timing: programs take turns, 9 rounds, each >= 0.2 s, best and median ns per point.  ax-h0, wave 16."""
import sys, re, gen
isa = sys.argv[1]
KS = ['h8_textbook_24', 'h8_G19', 'h8_G22_depth4', 'h8_ar22', 'h16_textbook_64', 'h16_G52_family', 'h16_G56_depth6', 'h16_G60_depth5']
VL = gen.ISA[isa]['VL']
parts, progs = [gen.ISA[isa]['inc'], '#include <stdio.h>', '#include <stdlib.h>', '#include <string.h>', '#include <time.h>',
                '#define S 256', 'static const float KV[] = {1.0f,-1.0f,2.0f,-2.0f,0.5f,-0.5f};'], []
for k in KS:
    for bal in (False, True):
        src = gen.emit(isa, 'circuits/%s.txt' % k, 1, bal)
        src = '\n'.join(l for l in src.splitlines() if 'LLVM-MCA' not in l and not l.startswith('#include') and not l.startswith('#define S') and not l.startswith('const float KV'))
        name = 'k_%s%s' % (k, '_bal' if bal else '')
        # constants are read from k[] in gen's order; give each kernel its own table
        consts = re.findall(r'k\+(\d+)', src)
        src = src.replace('void kern(', 'static void %s(' % name)
        tbl = gen.emit(isa, 'circuits/%s.txt' % k, 1, bal).split('const float KV[] = {')[1].split('}')[0]
        parts.append('static const float KV_%s[] = {%s};' % (name, tbl)); parts.append(src)
        progs.append((name, int(k.split('_')[0][1:])))
parts.append('static double now(void){struct timespec t;clock_gettime(CLOCK_MONOTONIC_RAW,&t);return t.tv_sec+1e-9*t.tv_nsec;}')
parts.append('typedef void (*kf)(float *restrict, const float *restrict, long);')
parts.append('static int sgn(int J,int i){return __builtin_popcount(J&i)&1?-1:1;}')
parts.append('static int check(kf f,const float*kv,int n){ float *a=aligned_alloc(64,n*S*4); float *x=malloc(n*S*4);'
             ' for(int i=0;i<n*S;i++){x[i]=(float)((rand()%201)-100);} memcpy(a,x,n*S*4); f(a,kv,S);'
             ' for(int c=0;c<S;c++) for(int J=0;J<n;J++){ float r=0; for(int i=0;i<n;i++) r+=sgn(J,i)*x[i*S+c];'
             ' if(a[J*S+c]!=r){free(a);free(x);return 0;} } free(a);free(x);return 1;}')
names = ',\n'.join('{"%s",%s,KV_%s,%d}' % (n, n, n, sz) for n, sz in progs)
parts.append('typedef struct{const char*n;kf f;const float*kv;int sz;} P; static P PR[]={%s};' % names)
parts.append(r'''int main(void){ int np=sizeof(PR)/sizeof(PR[0]);
 for(int p=0;p<np;p++){ int ok=check(PR[p].f,PR[p].kv,PR[p].sz); printf("CHECK %-28s %s\n",PR[p].n,ok?"PASS (exact)":"FAIL"); if(!ok) return 1; }
 if(getenv("CHECK_ONLY")) return 0;
 float *a=aligned_alloc(64,16*S*4); memset(a,0,16*S*4);   /* zeros: no overflow, no denormals */
 long calls[64]; double best[64],med[64],rep[64][9];
 for(int p=0;p<np;p++){ long c=1000; for(;;){ double t=now(); for(long i=0;i<c;i++) PR[p].f(a,PR[p].kv,S); if(now()-t>0.2) break; c*=2; } calls[p]=c; }
 for(int r=0;r<9;r++) for(int q=0;q<np;q++){ int p=(q+r)%np; double t=now(); for(long i=0;i<calls[p];i++) PR[p].f(a,PR[p].kv,S); rep[p][r]=(now()-t)*1e9/(calls[p]*(double)PR[p].sz*S); }
 for(int p=0;p<np;p++){ double v[9]; memcpy(v,rep[p],sizeof v); for(int i=0;i<9;i++)for(int j=i+1;j<9;j++) if(v[j]<v[i]){double t=v[i];v[i]=v[j];v[j]=t;}
   printf("RESULT %-28s best %.4f median %.4f ns/point  reps:",PR[p].n,v[0],v[4]); for(int r=0;r<9;r++) printf(" %.4f",rep[p][r]); printf("\n"); }
 return 0; }''')
open('bench_%s.c' % isa, 'w').write('\n'.join(parts) + '\n')
