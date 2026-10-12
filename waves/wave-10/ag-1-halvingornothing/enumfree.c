// enumfree.c (ag-1): forms modulo 2 on n = 8 inputs, gate = u + v (count (G) read modulo 2).
// Given target rows (file) and ONE form w given at no cost, list EVERY set of m intermediate forms with which all the
// targets are reached (a target is added the moment it is the sum of two available forms).  Same search as free8.c / enum2.c.
// usage: enumfree rowsfile m w [w ...]      (w = 0: no free form)      prints "SOL w : sorted set" (with repeats) and a count.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int n = 8, NP = 256, m;
static int cnt[256]; static unsigned char inR[256];
static int R[300], nR; static int T[80], nT;
static int inter[16], nI; static int W; static long long nfound, nshort; static long long visited;
static unsigned char seen2[256][256];
static void add_point(int w){ for(int i=0;i<nR;i++) cnt[w^R[i]]++; R[nR++]=w; inR[w]=1; }
static void remove_last(void){ int w=R[--nR]; inR[w]=0; for(int i=0;i<nR;i++) cnt[w^R[i]]--; }
static int closure(void){ int added=0,ch=1; while(ch){ ch=0; for(int i=0;i<nT;i++) if(!inR[T[i]]&&cnt[T[i]]>0){ add_point(T[i]); added++; ch=1; } } return added; }
static int all_in(void){ for(int i=0;i<nT;i++) if(!inR[T[i]]) return 0; return 1; }
static int cmpi(const void*a,const void*b){ return *(const int*)a-*(const int*)b; }
static void emit(int extra){ int s[16],k=0; for(int i=0;i<nI;i++) s[k++]=inter[i]; if(extra) s[k++]=extra; qsort(s,k,sizeof(int),cmpi);
    printf("SOL %d :",W); for(int i=0;i<k;i++) printf(" %d",s[i]); printf("\n"); nfound++; if(k<m) nshort++; }
static void dfs(int j){
    if(all_in()){ emit(0); return; }
    if(j==0) return;
    visited++;
    int base=nR;
    if(j==1){
        unsigned char done[256]; memset(done,0,sizeof done);
        for(int i=0;i<nT;i++) if(!inR[T[i]]) for(int r=0;r<base;r++){ int w=T[i]^R[r]; if(inR[w]||cnt[w]<=0||done[w]) continue; done[w]=1;
            add_point(w); int ad=closure(); if(all_in()) emit(w); for(int k=0;k<=ad;k++) remove_last(); }
        return;
    }
    unsigned char cand[256]; memset(cand,0,sizeof cand);
    for(int w=1;w<NP;w++) if(!inR[w]&&cnt[w]>0) cand[w]=1;
    for(int w=1;w<NP;w++) if(cand[w]){
        inter[nI++]=w;
        if(nI==2){ int a=inter[0],b=inter[1]; if(a>b){int t=a;a=b;b=t;} if(seen2[a][b]){ nI--; continue; } seen2[a][b]=1; }
        add_point(w); int ad=closure(); dfs(j-1); for(int k=0;k<=ad;k++) remove_last(); nI--;
    }
}
int main(int argc,char**argv){
    FILE*f=fopen(argv[1],"r"); m=atoi(argv[2]); int rows[80],nrows=0,v,k=0,code=0;
    while(fscanf(f,"%d",&v)==1){ code=(code<<1)|(v&1); if(++k==n){ rows[nrows++]=code; k=0; code=0; } } fclose(f);
    for(int a=3;a<argc;a++){
        W=atoi(argv[a]); memset(cnt,0,sizeof cnt); memset(inR,0,sizeof inR); memset(seen2,0,sizeof seen2); nR=0; nT=0; nI=0; nfound=0; nshort=0; visited=0;
        for(int i=0;i<n;i++) add_point(1<<i);
        if(W&&!inR[W]) add_point(W);
        for(int i=0;i<nrows;i++){ int t=rows[i],dup=inR[t]; for(int q=0;q<nT;q++) if(T[q]==t) dup=1; if(!dup&&t) T[nT++]=t; }
        int nT0=nT; closure(); dfs(m);
        printf("COUNT w=%d targets_to_make=%d m=%d real_gates=%d : %lld records (with repeats), %lld of them with fewer than m intermediates; nodes %lld\n",W,nT0,m,nT0+m,nfound,nshort,visited);
        fflush(stdout);
    }
    return 0;
}
