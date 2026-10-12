// u-1 corners-theory: ALL optimal pairs of orders for the subset-sum picture at N = 4 or 8 points.  Exact, whole numbers.
// For every input order (cols), cities = the N outputs plus the added zero row (the path must END at the zero row).
// w(S,S') = number of b in 0..N-1 with d[b] != d[b+1], d = row S - row S' along cols, d[N] = 0   (reformulation 1, "two salesmen").
// DP over subsets gives the least corner count for this input order and the NUMBER of output orders reaching it; a DFS lists them.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <algorithm>
int N,k; int cols[16]; int W[17][17]; int f[1<<8][8]; long long cnt[1<<8][8];
int best=999; long long nbest=0, ncols=0; FILE*out;
int wdist(int S,int Sp){ // Sp = -1 means the zero row
  int ch=0, prev=0; // walk from the right end: d[N]=0
  for(int b=N-1;b>=0;b--){ int T=cols[b]; int v=((S&T)==T)-((Sp>=0)&&((Sp&T)==T)); if(v!=prev) ch++; prev=v; }
  return ch; }
int path[16];
void dfs(int mask,int last,int depth,int target){ // reconstruct all optimal: path built from the zero end backwards
  path[depth]=last;
  if(mask==(1<<N)-1){ fprintf(out,"%d |",target); for(int i=N-1;i>=0;i--) fprintf(out," %d",path[i]); fprintf(out," |"); for(int b=0;b<N;b++) fprintf(out," %d",cols[b]); fprintf(out,"\n"); return; }
  for(int nx=0;nx<N;nx++) if(!(mask>>nx&1)){ int m2=mask|1<<nx; // need f[mask][last] consistent: we go forward, check via remaining DP g
    extern int g[1<<8][8]; if(f[mask][last]+W[last][nx]+g[m2][nx]==target) dfs(m2,nx,depth+1,target); } }
int g[1<<8][8]; // g[mask][last] = least cost to finish from (mask,last) to all cities
int main(int argc,char**argv){ k=atoi(argv[1]); N=1<<k; int target=argc>2?atoi(argv[2]):-1; out=argc>3?fopen(argv[3],"w"):NULL;
  for(int i=0;i<N;i++) cols[i]=i; long long hist[200]; memset(hist,0,sizeof hist);
  do{ for(int a=0;a<N;a++){ for(int b=0;b<N;b++) W[a][b]=wdist(a,b); W[a][N]=W[N][a]=wdist(a,-1);} 
    int full=(1<<N)-1;
    for(int m=0;m<=full;m++) for(int l=0;l<N;l++){ f[m][l]=9999; cnt[m][l]=0; }
    for(int l=0;l<N;l++){ f[1<<l][l]=W[N][l]; cnt[1<<l][l]=1; }
    for(int m=1;m<=full;m++) for(int l=0;l<N;l++) if((m>>l&1)&&f[m][l]<9999) for(int nx=0;nx<N;nx++) if(!(m>>nx&1)){ int v=f[m][l]+W[l][nx]; int m2=m|1<<nx; if(v<f[m2][nx]){f[m2][nx]=v;cnt[m2][nx]=cnt[m][l];} else if(v==f[m2][nx]) cnt[m2][nx]+=cnt[m][l]; }
    int mn=9999; long long c=0; for(int l=0;l<N;l++){ if(f[full][l]<mn){mn=f[full][l];c=cnt[full][l];} else if(f[full][l]==mn) c+=cnt[full][l]; }
    hist[mn]++;
    if(mn<best){best=mn;nbest=0;ncols=0;} if(mn==best){nbest+=c;ncols++;}
    if(out && mn==target){ for(int m=full;m>=1;m--) for(int l=0;l<N;l++) if(m>>l&1){ if(m==full){g[m][l]=0;continue;} int bv=9999; for(int nx=0;nx<N;nx++) if(!(m>>nx&1)){ int v=W[l][nx]+g[m|1<<nx][nx]; if(v<bv)bv=v; } g[m][l]=bv; }
      for(int l=0;l<N;l++) if(f[1<<l][l]+g[1<<l][l]==target) dfs(1<<l,l,0,target); }
  } while(std::next_permutation(cols,cols+N));
  printf("N=%d least corners=%d ; optimal pairs=%lld ; input orders that reach it=%lld\n",N,best,nbest,ncols);
  printf("histogram: least corners for a fixed input order -> number of input orders\n"); for(int i=0;i<200;i++) if(hist[i]) printf("  %d: %lld\n",i,hist[i]);
  if(out) fclose(out); return 0; }
