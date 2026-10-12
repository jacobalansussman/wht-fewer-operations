// drain.c -- steepest-drain builder, count (G): a gate is any a*u + b*v, scalings free.
// Exact integer arithmetic throughout (forms are integer vectors taken up to scale).
// d(t) is replaced by an HONEST UPPER BOUND: a greedy "pursuit" writes output t as (a few stored forms) + (a few inputs);
// cost(t) = forms used + inputs left - 1 = gates that finish t alone.  P = sum of cost(t); U = gates + P is always the
// size of a real circuit.  Each step: every pair of stored forms with coefficient ratios from a small set is a candidate;
// cheap screen (one pursuit step) for all, full re-pursuit for the top K; add the candidate with the largest drain.
// usage: drain N seed K coefset maxgates maxsec outfile [target: H|Z] [candidate cap] [stop when the best drain is <= this] [file of gates to preload: lines u v a b; - for none] [1: report at the first free step how many outputs each candidate helps]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#ifdef _OPENMP
#include <omp.h>
#endif
#define MAXN 64
#define MAXM 1200
typedef int32_t v_t;
static int N, M;
static v_t F[MAXM][MAXN];
static int gu[MAXM], gv[MAXM], ga[MAXM], gb[MAXM];
static v_t T[MAXN][MAXN];
typedef struct { v_t r[MAXN]; int nf; int used[MAXN+2]; int cost; } rep_t;
static rep_t Rp[MAXN];
static uint64_t rs=88172645463325252ULL;
static uint64_t rnd(void){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return rs; }
static int gcd_(int a,int b){ a=abs(a); b=abs(b); while(b){int t=a%b;a=b;b=t;} return a; }
static int normalize(v_t*x){ int g=0; for(int i=0;i<N;i++) g=gcd_(g,x[i]); if(!g) return 0; int s=0;
  for(int i=0;i<N;i++){ x[i]/=g; if(!s&&x[i]) s=x[i]>0?1:-1; } if(s<0) for(int i=0;i<N;i++) x[i]=-x[i]; return 1; }
static int wt(const v_t*x){ int w=0; for(int i=0;i<N;i++) w+=(x[i]!=0); return w; }
static inline int mode_gain(const v_t*r,const v_t*f,int64_t*bp,int64_t*bq){
  int64_t Pn[MAXN],Qn[MAXN]; int C[MAXN]; int nd=0, extra=0;
  for(int i=0;i<N;i++){ if(!f[i]) continue; if(!r[i]){extra++;continue;}
    int k; for(k=0;k<nd;k++) if((int64_t)r[i]*Qn[k]==Pn[k]*(int64_t)f[i]){C[k]++;break;}
    if(k==nd){Pn[nd]=r[i];Qn[nd]=f[i];C[nd]=1;nd++;} }
  if(!nd) return -1000;
  int b=0; for(int k=1;k<nd;k++) if(C[k]>C[b]) b=k;
  *bp=Pn[b]; *bq=Qn[b]; return C[b]-extra-1; }
static int apply(v_t*r,const v_t*f,int64_t p,int64_t q){ for(int i=0;i<N;i++){ int64_t z=q*r[i]-p*f[i]; if(z>1000000||z<-1000000) return 0; r[i]=(v_t)z; } normalize(r); return 1; }
static void pursue(rep_t*rp,const v_t*h){
  for(int it=0;it<N;it++){ int best=0,bj=-1; int64_t bp=0,bq=0,p,q;
    for(int j=N;j<M+(h?1:0);j++){ const v_t*f=j<M?F[j]:h; int g=mode_gain(rp->r,f,&p,&q); if(g>best){best=g;bj=j;bp=p;bq=q;} }
    if(bj<0) break;
    if(!apply(rp->r,bj<M?F[bj]:h,bp,bq)) break; rp->used[rp->nf++]=bj; }
  int w=wt(rp->r); rp->cost=rp->nf+w-1; }
// full evaluation of candidate h: new reps into out[] (if not NULL); returns drain
static int full_eval(const v_t*h, rep_t*out){
  int drain=0;
  for(int t=0;t<N;t++){ rep_t best=Rp[t]; int64_t p,q;
    if(Rp[t].cost>0){
      rep_t a=Rp[t]; int g=mode_gain(a.r,h,&p,&q);
      if(g>=1 && apply(a.r,h,p,q)){ a.used[a.nf++]=M; pursue(&a,h); if(a.cost<best.cost) best=a; }
      rep_t b; memcpy(b.r,T[t],sizeof(v_t)*N); b.nf=0; g=mode_gain(b.r,h,&p,&q);
      if(g>=1 && apply(b.r,h,p,q)){ b.used[b.nf++]=M; pursue(&b,h); if(b.cost<best.cost) best=b; }
    }
    drain+=Rp[t].cost-best.cost; if(out) out[t]=best; }
  return drain; }
static inline int cheap_eval(const v_t*h){ int s=0; int64_t p,q;
  for(int t=0;t<N;t++){ if(Rp[t].cost<=0) continue; int g1=mode_gain(Rp[t].r,h,&p,&q); int g2=Rp[t].cost-(N-1)+mode_gain(T[t],h,&p,&q);
    int g=g1>g2?g1:g2; if(g>0) s+=g; } return s; }
typedef struct { int u,v,a,b; int cheap; int full; uint64_t key; } cand_t;
static uint64_t hashv(const v_t*x){ uint64_t h=1469598103934665603ULL; for(int i=0;i<N;i++){ h^=(uint64_t)(uint32_t)x[i]; h*=1099511628211ULL; h^=h>>29; } return h; }
static int cmpc(const void*a,const void*b){ const cand_t*x=a,*y=b; if(x->cheap!=y->cheap) return y->cheap-x->cheap; return (x->key<y->key)?-1:(x->key>y->key); }
static int cmpk(const void*a,const void*b){ uint64_t x=*(const uint64_t*)a,y=*(const uint64_t*)b; return x<y?-1:x>y; }
int main(int argc,char**argv){
  if(argc<8){ fprintf(stderr,"usage\n"); return 2; }
  N=atoi(argv[1]); int seed=atoi(argv[2]); int K=atoi(argv[3]); int cs=atoi(argv[4]); int maxg=atoi(argv[5]); double maxsec=atof(argv[6]);
  FILE*fo=fopen(argv[7],"w"); const char*target=argc>8?argv[8]:"H"; long capc=argc>9?atol(argv[9]):400000; int stopdrain=argc>10?atoi(argv[10]):0; const char*prefix=argc>11?argv[11]:NULL; int report=argc>12?atoi(argv[12]):0;
  rs^=(uint64_t)seed*0x9E3779B97F4A7C15ULL; for(int i=0;i<20;i++) rnd();
  for(int x=0;x<N;x++) for(int y=0;y<N;y++){ if(target[0]=='Z') T[x][y]=((x&y)==y); else T[x][y]=(__builtin_popcount(x&y)&1)?-1:1; }
  M=N; memset(F,0,sizeof F); for(int i=0;i<N;i++) F[i][i]=1;
  int CA[10]={1,1,1,1,2,2,1,1,4,4}, CB[10]={1,-1,2,-2,1,-1,4,-4,1,-1}; int nco= cs==1?2: cs==2?6:10;
  for(int t=0;t<N;t++){ memcpy(Rp[t].r,T[t],sizeof(v_t)*N); Rp[t].nf=0; Rp[t].cost=wt(T[t])-1; }
  int P=0; for(int t=0;t<N;t++) P+=Rp[t].cost; int P0=P; int npre=0;
  if(prefix && strcmp(prefix,"-")){ FILE*fp=fopen(prefix,"r"); int u,v,a,b; while(fp && fscanf(fp,"%d %d %d %d",&u,&v,&a,&b)==4){
      for(int k=0;k<N;k++) F[M][k]=a*F[u][k]+b*F[v][k]; normalize(F[M]); gu[M]=u;gv[M]=v;ga[M]=a;gb[M]=b; M++; npre++; }
    if(fp) fclose(fp);
    for(int t=0;t<N;t++){ rep_t b; memcpy(b.r,T[t],sizeof(v_t)*N); b.nf=0; pursue(&b,NULL); Rp[t]=b; }
    P=0; for(int t=0;t<N;t++) P+=Rp[t].cost; }
  time_t t0=time(NULL); int bestU=P, bestg=0; static rep_t bestRp[MAXN]; memcpy(bestRp,Rp,sizeof Rp);
  cand_t*C=malloc(sizeof(cand_t)*(capc+1000)); uint64_t*keys=malloc(sizeof(uint64_t)*MAXM);
  fprintf(fo,"{\"N\":%d,\"seed\":%d,\"K\":%d,\"coefset\":%d,\"target\":\"%s\",\"P0\":%d}\n",N,seed,K,cs,target,P0);
  int g=npre; int nhalf=0, nfull=0; if(npre){ bestU=g+P; bestg=g; memcpy(bestRp,Rp,sizeof Rp); fprintf(fo,"{\"prefix_gates\":%d,\"P\":%d,\"U\":%d}\n",npre,P,g+P); }
  while(P>0 && g<maxg && difftime(time(NULL),t0)<maxsec && M<MAXM-2){
    for(int j=0;j<M;j++) keys[j]=hashv(F[j]); qsort(keys,M,sizeof(uint64_t),cmpk);
    long total=(long)M*(M-1)/2*nco; double keep= total>capc ? (double)capc/total : 1.0; long nc=0;
    for(int u=0;u<M;u++) for(int v=u+1;v<M;v++) for(int c=0;c<nco;c++){
      if(keep<1.0 && (rnd()>>11)*(1.0/9007199254740992.0)>keep) continue;
      if(nc>=capc+900) continue;
      C[nc].u=u;C[nc].v=v;C[nc].a=CA[c];C[nc].b=CB[c];nc++; }
    #pragma omp parallel for schedule(dynamic,256)
    for(long i=0;i<nc;i++){ v_t h[MAXN]; for(int k=0;k<N;k++) h[k]=C[i].a*F[C[i].u][k]+C[i].b*F[C[i].v][k];
      if(!normalize(h)){C[i].cheap=-1;C[i].key=0;continue;} uint64_t key=hashv(h); C[i].key=key;
      if(bsearch(&key,keys,M,sizeof(uint64_t),cmpk)){C[i].cheap=-1;continue;}
      C[i].cheap=cheap_eval(h); C[i].full=-1; }
    qsort(C,nc,sizeof(cand_t),cmpc);
    // dedupe equal keys among the top, take top K distinct
    long top=0; for(long i=0;i<nc && top<K;i++){ if(C[i].cheap<0) break; if(top>0 && C[top-1].key==C[i].key && C[top-1].cheap==C[i].cheap) continue; C[top++]=C[i]; }
    if(top==0) break;
    #pragma omp parallel for schedule(dynamic,8)
    for(long i=0;i<top;i++){ v_t h[MAXN]; for(int k=0;k<N;k++) h[k]=C[i].a*F[C[i].u][k]+C[i].b*F[C[i].v][k]; normalize(h); C[i].full=full_eval(h,NULL); }
    int best=-1; long nb=0; for(long i=0;i<top;i++){ if(C[i].full>best){best=C[i].full;nb=1;} else if(C[i].full==best) nb++; }
    if(report){ report=0; int hist[MAXN+1]; memset(hist,0,sizeof hist); int shown=0;
      for(long i=0;i<top;i++){ if(C[i].full<=0) continue; v_t h[MAXN]; static rep_t nr2[MAXN]; for(int k=0;k<N;k++) h[k]=C[i].a*F[C[i].u][k]+C[i].b*F[C[i].v][k]; normalize(h);
        full_eval(h,nr2); int helped=0; for(int t=0;t<N;t++) if(nr2[t].cost<Rp[t].cost) helped++; hist[helped]++;
        if(4*helped>=3*N && shown<12){ shown++; fprintf(fo,"{\"report\":\"helps %d of %d, drain %d\",\"from\":[%d,%d,%d,%d],\"form\":[",helped,N,C[i].full,C[i].u,C[i].v,C[i].a,C[i].b); for(int k=0;k<N;k++) fprintf(fo,"%s%d",k?",":"",h[k]); fprintf(fo,"]}\n"); } }
      fprintf(fo,"{\"report_hist_outputs_helped\":["); for(int k=0;k<=N;k++) fprintf(fo,"%s%d",k?",":"",hist[k]); fprintf(fo,"]}\n"); }
    if(best<=stopdrain) break;
    long pick=rnd()%nb, bi=-1; for(long i=0;i<top;i++) if(C[i].full==best){ if(pick==0){bi=i;break;} pick--; }
    v_t h[MAXN]; for(int k=0;k<N;k++) h[k]=C[bi].a*F[C[bi].u][k]+C[bi].b*F[C[bi].v][k]; normalize(h);
    static rep_t nr[MAXN]; int dr=full_eval(h,nr); memcpy(F[M],h,sizeof(v_t)*N); gu[M]=C[bi].u; gv[M]=C[bi].v; ga[M]=C[bi].a; gb[M]=C[bi].b; M++;
    memcpy(Rp,nr,sizeof Rp); P-=dr; g++; if(2*dr>=N) nhalf++; if(dr==N) nfull++;
    int hit=0; for(int t=0;t<N;t++) if(Rp[t].cost==0) hit++;
    fprintf(fo,"{\"gate\":%d,\"u\":%d,\"v\":%d,\"a\":%d,\"b\":%d,\"drain\":%d,\"ties\":%ld,\"cands\":%ld,\"P\":%d,\"U\":%d,\"done\":%d,\"wt\":%d,\"sec\":%.0f}\n",g,gu[M-1],gv[M-1],ga[M-1],gb[M-1],dr,nb,nc,P,g+P,hit,wt(h),difftime(time(NULL),t0)); fflush(fo);
    if(g+P<=bestU){ bestU=g+P; bestg=g; memcpy(bestRp,Rp,sizeof Rp); }
  }
  // dump the best state for exact replay
  fprintf(fo,"{\"best\":{\"U\":%d,\"gates\":%d,\"prog\":[",bestU,bestg);
  for(int j=N;j<N+bestg;j++) fprintf(fo,"%s[%d,%d,%d,%d]",j>N?",":"",gu[j],gv[j],ga[j],gb[j]);
  fprintf(fo,"],\"reps\":[");
  for(int t=0;t<N;t++){ fprintf(fo,"%s{\"forms\":[",t?",":""); for(int k=0;k<bestRp[t].nf;k++) fprintf(fo,"%s%d",k?",":"",bestRp[t].used[k]);
    fprintf(fo,"],\"inputs\":["); int f1=1; for(int i=0;i<N;i++) if(bestRp[t].r[i]){ fprintf(fo,"%s%d",f1?"":",",i); f1=0; } fprintf(fo,"],\"cost\":%d}",bestRp[t].cost); }
  fprintf(fo,"]},\"final_gates\":%d,\"final_P\":%d,\"half_drain_gates\":%d,\"full_drain_gates\":%d}\n",g,P,nhalf,nfull); fclose(fo);
  printf("drain N=%d seed=%d K=%d cs=%d target=%s: bestU=%d at gate %d; ended g=%d P=%d; gates draining >=N/2: %d, ==N: %d; %.0fs\n",N,seed,K,cs,target,bestU,bestg,g,P,nhalf,nfull,difftime(time(NULL),t0));
  return 0; }
