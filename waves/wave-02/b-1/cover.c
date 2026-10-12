// cover.c  [b-1]  exact integer enumeration, no floating point in any decision.
// Old-letter game: a count vector n (how often each nonzero direction z of F_2^m is used as a single move).
// Counting: every quadratic form q without constant term and with q(I)=1 must select at least W moves.
// Clique lemma: tight = selects exactly W; no W+1 moves pairwise selected together by tight forms.
// usage: cover m W T [dualfile]          enumerate ALL count vectors with total <= T that pass counting; clique test on each
//        cover m W 0 design z:n z:n ...  test one given count vector
// The dual file (form index, integer weight) is used only as a pruning bound; its validity is re-checked here in integers.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef uint64_t u64;
static int m, W, T, NZ, NP, NF;
static u64 *mask; static int **formsOf; static int *nFormsOf;
static long long *y; static long long D = 1;
static int *cov; static int n[64];
static long long nodes, leaves, cnt[400], surv[400]; static int cmin[400], cmax[400];
static int printed = 0; static u64 adj[64]; static int bestw;
static int wsum(u64 P){ int s=0; while(P){ int z=__builtin_ctzll(P); P&=P-1; s+=n[z]; } return s; }
static void clq(u64 P, int w){
  if (w > bestw) bestw = w;
  while (P){ if (w + wsum(P) <= bestw) return; int z=__builtin_ctzll(P); P&=P-1; clq(P & adj[z], w + n[z]); }
}
static void pr(void){ for (int z=1;z<=NZ;z++) if(n[z]){ putchar(' '); for(int b=m-1;b>=0;b--) putchar('0'+((z>>b)&1)); printf(":%d", n[z]); } }
static long long ntight; static int npairs;
static void evaluate(int t, int verbose){
  u64 present=0; for(int z=1;z<=NZ;z++) if(n[z]) present |= 1ULL<<z;
  memset(adj,0,sizeof adj); u64 intight=0; ntight=0;
  for(int q=0;q<NF;q++) if(cov[q]==W){ ntight++; u64 s=mask[q]&present; intight|=s; u64 r=s; while(r){int z=__builtin_ctzll(r); r&=r-1; adj[z]|=s;} }
  for(int z=1;z<=NZ;z++) adj[z] &= ~(1ULL<<z);
  bestw=0; clq(intight,0); if(bestw==0 && t>0) bestw=1;
  if (cnt[t]==0){cmin[t]=bestw;cmax[t]=bestw;} if(bestw<cmin[t])cmin[t]=bestw; if(bestw>cmax[t])cmax[t]=bestw;
  cnt[t]++;
  if (bestw<=W){ surv[t]++; if(printed<60){printed++; printf("  SURVIVOR total %d, largest clique %d, tight forms %lld:",t,bestw,ntight); pr(); printf("\n");} }
  if (verbose){ printf("  total %d, tight forms %lld, largest clique %d (W=%d):",t,ntight,bestw,W); pr(); printf("\n"); }
}
static void add(int z,int s){ n[z]+=s; int *f=formsOf[z]; int c=nFormsOf[z]; for(int i=0;i<c;i++) cov[f[i]]+=s; }
static void extend(int t,u64 frozen,int zmin){
  evaluate(t,0); if(t==T) return;
  for(int z=zmin;z<=NZ;z++) if(!((frozen>>z)&1)){ add(z,1); extend(t+1,frozen,z); add(z,-1); }
}
static int PART=0,PARTS=1; static long long splitcnt=0;
static void dfs(int t,u64 frozen){
  if(t==3 && PARTS>1){ if((splitcnt++ % PARTS)!=PART) return; }
  nodes++;
  long long lb=0; int best=-1,bestc=1000,bestd=0,maxdef=0;
  for(int q=0;q<NF;q++){ int d=W-cov[q]; if(d>0){ lb+=y[q]*d; int c=__builtin_popcountll(mask[q]&~frozen); if(c==0) return; if(d>maxdef)maxdef=d; if(c<bestc||(c==bestc&&d>bestd)){best=q;bestc=c;bestd=d;} } }
  if(best<0){ leaves++; extend(t,frozen,1); return; }
  if(t+maxdef>T) return;
  if(lb > D*(long long)(T-t)) return;
  u64 cand=mask[best]&~frozen; u64 fr=frozen;
  while(cand){ int z=__builtin_ctzll(cand); cand&=cand-1; add(z,1); dfs(t+1,fr); add(z,-1); fr|=1ULL<<z; }
}
int main(int argc,char**argv){
  m=atoi(argv[1]); W=atoi(argv[2]); T=atoi(argv[3]); NP=m*(m+1)/2; NZ=(1<<m)-1;
  int pi[64],pj[64],t=0; u64 diag=0; for(int i=0;i<m;i++) for(int j=i;j<m;j++){pi[t]=i;pj[t]=j; if(i==j) diag|=1ULL<<t; t++;}
  u64 zz[64]; for(int z=0;z<=NZ;z++){ zz[z]=0; for(int s=0;s<NP;s++) if(((z>>pi[s])&1)&&((z>>pj[s])&1)) zz[z]|=1ULL<<s; }
  NF=1<<(NP-1); mask=malloc(sizeof(u64)*NF); int *idx=malloc(sizeof(int)*(1<<NP)); int k=0;
  for(u64 Q=0;Q<(1ULL<<NP);Q++){ idx[Q]=-1; if(__builtin_popcountll(Q&diag)&1){ u64 mk=0; for(int z=1;z<=NZ;z++) if(__builtin_popcountll(Q&zz[z])&1) mk|=1ULL<<z; mask[k]=mk; idx[Q]=k; k++; } }
  cov=calloc(NF,sizeof(int)); y=calloc(NF,sizeof(long long));
  if(argc>4 && !strcmp(argv[4],"design")){
    int tot=0; for(int a=5;a<argc;a++){ char*c=strchr(argv[a],':'); int z=(int)strtol(argv[a],NULL,2); int v=atoi(c+1); n[z]+=v; tot+=v; }
    int mn=1<<30; for(int q=0;q<NF;q++){ int c=0; u64 r=mask[q]; while(r){int z=__builtin_ctzll(r); r&=r-1; c+=n[z];} cov[q]=c; if(c<mn)mn=c; }
    printf("m=%d W=%d design with %d moves (plain %d): fewest moves selected by a form with q(I)=1: %d (%s)\n",m,W,tot,m*W,mn,mn>=W?"passes counting":"FAILS counting");
    evaluate(tot,1); printf("  -> %s\n", bestw>W?"EXCLUDED by the clique lemma":"not excluded"); return 0;
  }
  formsOf=malloc(sizeof(int*)*64); nFormsOf=calloc(64,sizeof(int));
  for(int z=1;z<=NZ;z++){ formsOf[z]=malloc(sizeof(int)*(NF/2+1)); for(int q=0;q<NF;q++) if((mask[q]>>z)&1) formsOf[z][nFormsOf[z]++]=q; }
  if(argc>4){ FILE*f=fopen(argv[4],"r"); long long Q,v; while(fscanf(f,"%lld %lld",&Q,&v)==2){ if(idx[Q]>=0 && v>0) y[idx[Q]]=v; } fclose(f);
    D=0; for(int z=1;z<=NZ;z++){ long long s=0; for(int i=0;i<nFormsOf[z];i++) s+=y[formsOf[z][i]]; if(s>D)D=s; } if(D==0)D=1;
    long long tot=0; for(int q=0;q<NF;q++) tot+=y[q]; printf("dual bound re-checked in integers: any covering vector has at least %lld*W/%lld = %.6f moves\n",tot,D,(double)tot*W/D); }
  if(getenv("PARTS")){PARTS=atoi(getenv("PARTS"));PART=atoi(getenv("PART"));}
  dfs(0,0);
  printf("m=%d W=%d: all count vectors with at most %d moves that pass counting (plain = %d). search nodes %lld, minimal leaves %lld, part %d of %d\n",m,W,T,m*W,nodes,leaves,PART,PARTS);
  for(int s=0;s<=T;s++) if(cnt[s]) printf("  %d moves: %lld count vectors pass counting; largest clique between %d and %d; pass the clique test too: %lld\n",s,cnt[s],cmin[s],cmax[s],surv[s]);
  return 0;
}
