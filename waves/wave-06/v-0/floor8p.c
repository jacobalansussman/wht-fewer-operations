/* v-0: exact lower bound at 8 points for the PARTNER-FREE relaxation of the class, both tree types.
   gates >= 4 (one wire on each pair node) + |F| (wires held on the two four-nodes) + |W| (full wires),
   |W| >= least number of edges of a tree joining a virtual root and the 8 rows, where
   root--(a,b) is a join of held four-wires a in F_L, b in F_R (either sign), and any full sign vector may be
   flipped on ANY node of the tree (leaf, pair, half) with no partner required.  Dreyfus-Wagner, exact. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define INF 1000
static int d0[128], Dm[129][129], dp[256][129], term[8];
static int nrm(int m){ return ((m&1)?(m^0xFF):m)>>1; }
int main(int argc,char**argv){
  int tw=atoi(argv[1]), maxF=atoi(argv[2]);
  int gens[13],ng=0,i,u,v;
  for(i=0;i<8;i++) gens[ng++]=nrm(1<<i);
  gens[ng++]=nrm(0x03); gens[ng++]=nrm(0x0C);
  if(!tw){gens[ng++]=nrm(0x30);gens[ng++]=nrm(0xC0);} else {gens[ng++]=nrm(0x50);gens[ng++]=nrm(0xA0);}
  gens[ng++]=nrm(0x0F);
  for(i=0;i<128;i++) d0[i]=INF; d0[0]=0;
  { int q[128],h=0,t=0; q[t++]=0; while(h<t){u=q[h++]; for(i=0;i<ng;i++){v=u^gens[i]; if(d0[v]==INF){d0[v]=d0[u]+1;q[t++]=v;}}} }
  for(int y=0;y<8;y++){int m=0; for(int x=0;x<8;x++) if(__builtin_popcount(x&y)&1) m|=1<<x; term[y]=nrm(m);}
  int bestby[17]; long cntby[17]; for(i=0;i<17;i++){bestby[i]=INF;cntby[i]=0;}
  int best=INF; long nbest=0, total=0;
  for(int F=1;F<65536;F++){
    int pc=__builtin_popcount(F); if(pc>maxF) continue; if(!(F&0xFF)||!(F>>8)) continue;
    int r[128]; for(v=0;v<128;v++) r[v]=INF;
    for(int a=0;a<8;a++) if(F>>a&1) for(int b=0;b<8;b++) if(F>>(8+b)&1){
      int la=a<<1, rb=b<<1; int j1=nrm(la|(rb<<4)), j2=nrm(la|((rb^0xF)<<4));
      for(v=0;v<128;v++){ int x=1+d0[v^j1]; if(x<r[v]) r[v]=x; x=1+d0[v^j2]; if(x<r[v]) r[v]=x; } }
    for(u=0;u<128;u++){ for(v=0;v<128;v++){ int x=d0[u^v], y=r[u]+r[v]; Dm[u][v]=x<y?x:y; } Dm[u][128]=Dm[128][u]=r[u]; }
    Dm[128][128]=0;
    for(int mask=1;mask<256;mask++){
      if((mask&(mask-1))==0){ int t=term[__builtin_ctz(mask)]; for(v=0;v<129;v++) dp[mask][v]=Dm[t][v]; continue; }
      int tmp[129]; for(v=0;v<129;v++) tmp[v]=INF;
      for(int sub=(mask-1)&mask; sub>0; sub=(sub-1)&mask){ int o=mask^sub; if(sub<o) continue;
        for(v=0;v<129;v++){ int x=dp[sub][v]+dp[o][v]; if(x<tmp[v]) tmp[v]=x; } }
      for(v=0;v<129;v++){ int m=INF; for(u=0;u<129;u++){ int x=tmp[u]+Dm[u][v]; if(x<m) m=x; } dp[mask][v]=m; }
    }
    int sv=dp[255][128], tot=pc+sv; total++; if(tot<=14) printf("TIGHT F=%d\n",F);
    if(sv<bestby[pc]){bestby[pc]=sv;cntby[pc]=0;} if(sv==bestby[pc]) cntby[pc]++;
    if(tot<best){best=tot;nbest=0;} if(tot==best) nbest++;
  }
  printf("tree=%s  sets of four-wires examined (size<=%d, both sides non-empty): %ld\n", tw?"twisted (left half split along bit 2, right half along bit 1)":"chain (cube tree)", maxF,total);
  for(i=2;i<=maxF;i++) printf("  |F|=%d: least number of full wires = %d (attained by %ld sets)  -> gates >= 4 + %d + %d = %d\n", i,bestby[i],cntby[i],i,bestby[i],4+i+bestby[i]);
  printf("  least |F| + full wires over all sets = %d (%ld sets)  => every circuit of the class on this tree has >= %d gates (partners not charged)\n",best,nbest,4+best);
  printf("  (|F| >= %d gives >= 4 + %d + 8 without computation)\n", maxF+1, maxF+1);
  return 0; }
