// ad-2: subset sums Z on n = 4 or 8 points over the TWO-ELEMENT FIELD, gate count (G) (a gate = u + v).
// For a set W of forms given at no cost: least number of gates.  Same search as ab-5's mincirc_free (sets of m
// intermediate forms, targets added the moment they are a sum of two available forms), done in-process for many W.
// usage: free8 n mode     mode = single | pairs | list (free sets on stdin, one per line, masks in decimal)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int n, NP;
static int cnt[256]; static unsigned char inR[256];
static int R[300], nR; static int T[80], nT;
static unsigned short seen[256][256]; static unsigned short stamp;
static int inter[16], nI;
static void add_point(int w){ for(int i=0;i<nR;i++) cnt[w^R[i]]++; R[nR++]=w; inR[w]=1; }
static void remove_last(void){ int w=R[--nR]; inR[w]=0; for(int i=0;i<nR;i++) cnt[w^R[i]]--; }
static int closure(void){ int added=0,ch=1; while(ch){ ch=0; for(int i=0;i<nT;i++) if(!inR[T[i]]&&cnt[T[i]]>0){ add_point(T[i]); added++; ch=1; } } return added; }
static int all_in(void){ for(int i=0;i<nT;i++) if(!inR[T[i]]) return 0; return 1; }
static int dfs(int j){
    if(all_in()) return 1;
    if(j==0) return 0;
    int base=nR;
    if(j==1){
        for(int i=0;i<nT;i++) if(!inR[T[i]]){
            for(int r=0;r<base;r++){ int w=T[i]^R[r]; if(inR[w]||cnt[w]<=0) continue;
                add_point(w); int ad=closure(); int ok=all_in(); for(int k=0;k<=ad;k++) remove_last(); if(ok) return 1; }
        }
        return 0;
    }
    unsigned char cand[256]; memset(cand,0,sizeof cand);
    for(int w=1;w<NP;w++) if(!inR[w]&&cnt[w]>0) cand[w]=1;
    for(int w=1;w<NP;w++) if(cand[w]){
        inter[nI++]=w;
        if(nI<=2){ int a=inter[0], b=nI>1?inter[1]:0; if(nI>1&&a>b){int t=a;a=b;b=t;} if(nI==1){ b=a; a=0; }
            if(seen[a][b]==stamp){ nI--; continue; } seen[a][b]=stamp; }
        add_point(w); int ad=closure(); int ok=dfs(j-1); for(int k=0;k<=ad;k++) remove_last(); nI--;
        if(ok) return 1;
    }
    return 0;
}
static int zrow(int S){ int r=0; for(int t=0;t<n;t++) if((t&S)==t) r|=1<<t; return r; }
// least gates given free set W (nW masks)
static int XT[64], nXT=0;   // extra targets (ad-2: the injected pure wires)
static int mingates(int *W,int nW){
    memset(cnt,0,sizeof cnt); memset(inR,0,sizeof inR); nR=0; nT=0;
    for(int i=0;i<n;i++) add_point(1<<i);
    for(int i=0;i<nW;i++) if(W[i]&&!inR[W[i]]) add_point(W[i]);
    for(int S=1;S<n;S++){ int t=zrow(S); if(!inR[t]) T[nT++]=t; }
    for(int i=0;i<nXT;i++){ int t=XT[i], dup=inR[t]; for(int k=0;k<nT;k++) if(T[k]==t) dup=1; if(!dup&&t) T[nT++]=t; }
    int nT0=nT;
    for(int m=0;m<12;m++){
        stamp++; if(stamp==0){ memset(seen,0,sizeof seen); stamp=1; }
        // fresh state for each m
        int keep=nR; int ad=closure(); nI=0;
        int ok=dfs(m);
        for(int k=0;k<ad;k++) remove_last();
        if(nR!=keep){ fprintf(stderr,"state error\n"); exit(3); }
        if(ok) return nT0+m;
    }
    return -1;
}
int main(int argc,char**argv){
    n=atoi(argv[1]); NP=1<<n; const char*mode=argv[2];
    int base=mingates(NULL,0);
    printf("# n=%d two-element field, count (G): Z without free forms = %d gates\n",n,base); fflush(stdout);
    if(!strcmp(mode,"single")){
        for(int w=1;w<NP;w++){ if(__builtin_popcount(w)==1) continue; int W[1]={w}; printf("%d %d\n",w,mingates(W,1)); }
    } else if(!strcmp(mode,"pairs")){
        int lo=argc>3?atoi(argv[3]):1, hi=argc>4?atoi(argv[4]):NP;
        for(int a=lo;a<hi;a++){ if(__builtin_popcount(a)==1) continue;
            for(int b=a+1;b<NP;b++){ if(__builtin_popcount(b)==1) continue; int W[2]={a,b}; printf("%d %d %d\n",a,b,mingates(W,2)); }
            fflush(stdout); }
    } else {
        char line[4096];
        while(fgets(line,sizeof line,stdin)){ int W[64],nW=0; char*p=line; int v,off; nXT=0;
            char*tp=strchr(line,'T'); if(tp){ *tp=0; char*q=tp+1; while(sscanf(q,"%d%n",&v,&off)==1){ XT[nXT++]=v; q+=off; } }
            while(sscanf(p,"%d%n",&v,&off)==1){ W[nW++]=v; p+=off; }
            if(nW==0&&nXT==0) continue;
            for(int i=0;i<nW;i++) printf("%d ",W[i]); printf("T "); for(int i=0;i<nXT;i++) printf("%d ",XT[i]); printf(": %d\n",mingates(W,nW)); fflush(stdout); }
    }
    return 0;
}
