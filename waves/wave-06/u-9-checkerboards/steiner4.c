// u-9: H modulo 4 as a letter with JUNCTION points.  Rows of the parity matrix B (B[y][x] = parity of common ones) are points of
// F_2^N; a step is "exclusive-or with the indicator of one node of a merge tree T on the inputs" (the whole set is free: an output
// sign).  spanning = cheapest tree that joins 0 and the N rows using only those points; steiner = cheapest network when any
// point of F_2^N may be used as a junction (exact, Dreyfus-Wagner).  Claim to test: spanning >= (N/2) log2 N for EVERY tree T
// [derived], and whether junction points go below it.   usage: steiner4 k ntrees seed
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define MAXN 8
static int k,N,P; static int ch[2*MAXN][2]; static int nn; static unsigned char c[1<<MAXN];
static uint64_t st=88172645463325252ULL; static inline uint64_t rnd(void){st^=st<<13;st^=st>>7;st^=st<<17;return st;}
static int leafof[MAXN];
static void costs(void){ // c[D] = least number of nodes (root free) whose exclusive-or is D
  for(int D=0;D<P;D++){ int f[2*MAXN][2];
    for(int v=0;v<nn;v++){ if(v<N){int lab=(D>>leafof[v])&1;f[v][lab]=0;f[v][1-lab]=100;}
      else for(int g=0;g<2;g++){int s=0;for(int j=0;j<2;j++){int w=ch[v][j];int a=f[w][g],b=f[w][1-g]+1;s+=a<b?a:b;}f[v][g]=s;} }
    c[D]=f[nn-1][0]<f[nn-1][1]?f[nn-1][0]:f[nn-1][1]; } }
static int term[MAXN+1]; static unsigned short dp[1<<MAXN][1<<MAXN];
static int steiner(void){ int t=N; // terminals: term[0]=0 and the N-1 non-zero rows
  int full=(1<<t)-1;
  for(int m=1;m<=full;m++){
    if((m&(m-1))==0){int i=__builtin_ctz(m);for(int v=0;v<P;v++)dp[m][v]=c[term[i]^v];continue;}
    static unsigned short tmp[1<<MAXN];
    for(int v=0;v<P;v++){int best=60000;for(int s=(m-1)&m;s>0;s=(s-1)&m){if(s<(m^s))continue;int val=dp[s][v]+dp[m^s][v];if(val<best)best=val;}tmp[v]=best;}
    for(int v=0;v<P;v++){int best=tmp[v];for(int u=0;u<P;u++){int val=tmp[u]+c[u^v];if(val<best)best=val;}dp[m][v]=best;}
  }
  return dp[full][term[0]]; }
static int spanning(void){ int t=N; int in[MAXN+1]={0},d[MAXN+1];int tot=0;in[0]=1;for(int i=1;i<t;i++)d[i]=c[term[0]^term[i]];
  for(int r=1;r<t;r++){int b=-1;for(int i=1;i<t;i++)if(!in[i]&&(b<0||d[i]<d[b]))b=i;tot+=d[b];in[b]=1;for(int i=1;i<t;i++)if(!in[i]){int x=c[term[b]^term[i]];if(x<d[i])d[i]=x;}}
  return tot; }
static void randtree(void){ int cl[2*MAXN],m=N;for(int i=0;i<N;i++)cl[i]=i;nn=N;
  int perm[MAXN];for(int i=0;i<N;i++)perm[i]=i;for(int i=N-1;i>0;i--){int j=rnd()%(i+1);int x=perm[i];perm[i]=perm[j];perm[j]=x;}
  for(int i=0;i<N;i++)leafof[i]=perm[i];
  while(m>1){int a=rnd()%m,b=rnd()%(m-1);if(b>=a)b++;ch[nn][0]=cl[a];ch[nn][1]=cl[b];int lo=a<b?a:b,hi=a<b?b:a;cl[lo]=nn;cl[hi]=cl[m-1];m--;nn++;} }
static void cubetree(void){ // nodes: sub-cubes fixing the high bits; leaves in address order
  for(int i=0;i<N;i++)leafof[i]=i;nn=N;int cur[MAXN],m=N;for(int i=0;i<N;i++)cur[i]=i;
  while(m>1){for(int i=0;i<m/2;i++){ch[nn][0]=cur[2*i];ch[nn][1]=cur[2*i+1];cur[i]=nn++;}m/=2;} }
static void chaintree(int gray){ for(int i=0;i<N;i++)leafof[i]=gray?(i^(i>>1)):i;nn=N;int cur=0;for(int i=1;i<N;i++){ch[nn][0]=cur;ch[nn][1]=i;cur=nn++;} }
int main(int argc,char**argv){ k=atoi(argv[1]);N=1<<k;P=1<<N;long nt=atol(argv[2]);st^=strtoull(argv[3],0,10)*0x9E3779B97F4A7C15ULL;
  for(int y=0;y<N;y++){int r=0;for(int x=0;x<N;x++)if(__builtin_popcount(y&x)&1)r|=1<<x;term[y]=r;}
  int bound=k*N/2; int minsp=1000,minst=1000; long below=0; long hist[64]={0};
  for(long it=-3;it<nt;it++){ if(it==-3)cubetree();else if(it==-2)chaintree(0);else if(it==-1)chaintree(1);else randtree();
    costs(); int sp=spanning(),stn=steiner();
    if(it<0)printf("%s: spanning %d, with junction points %d\n",it==-3?"cube tree":it==-2?"chain in address order":"chain in Gray order",sp,stn);
    if(sp<minsp)minsp=sp; if(stn<minst){minst=stn;printf("tree %ld: spanning %d, with junction points %d  leaves:",it,sp,stn);for(int i=0;i<N;i++)printf(" %d",leafof[i]);printf("  merges:");for(int v=N;v<nn;v++)printf(" (%d,%d)",ch[v][0],ch[v][1]);printf("\n");fflush(stdout);}
    if(stn<bound)below++; if(stn<64)hist[stn]++; }
  printf("N=%d: (N/2) log2 N = %d; over %ld trees: least spanning %d, least with junction points %d, trees with junction count below (N/2)log2N: %ld\nhistogram of the junction count:",N,bound,nt+3,minsp,minst,below);
  for(int i=0;i<64;i++)if(hist[i])printf(" %d:%ld",i,hist[i]);printf("\n");return 0; }
