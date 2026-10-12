// p-8-fibonacci/dws.c : "sign-point model", exact over the integers.  Points are vectors of +1/-1 on N = 2^K columns (bit set = -1).
// Edges: flip one column (a leaf rectangle, number +-2), or flip a whole node B of the column tree when the point equals +c' or -c'
// on all of B (an internal rectangle, number +-2).  Any tree in this graph is an exact decomposition with numbers +-2 (root: 1).
// For a group of rows G: least number of edges of a tree that joins the point c' to one of +h_y, -h_y for every y in G  (Dreyfus-Wagner).
// Usage: dws K [w] < lines "m_1..m_{N-1}  cmask  g  y_1..y_g"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static int K,N,n,witness; static uint8_t *dp,*sp; static int8_t *pg; static int masks[64], nm, cm;
static inline int nbr(int v,int g){ if(g<N) return v^(1<<g); int B=masks[g]; int d=(v^cm)&B; return (d==0||d==B)? v^B : -1; }
static void back(int S,int v){
    while(pg[(size_t)S*n+v]>=0){ int g=pg[(size_t)S*n+v]; int u=v^(g<N?(1<<g):masks[g]); printf("  edge %d -- %d  node %d\n",u,v,g<N?(1<<g):masks[g]); v=u; }
    if(__builtin_popcount(S)==1){ printf("  terminal #%d at %d\n",__builtin_ctz(S),v); return; }
    int S1=sp[(size_t)S*n+v]; back(S1,v); back(S^S1,v);
}
int main(int argc,char**argv){
    K=atoi(argv[1]); witness=argc>2; N=1<<K; n=1<<N; nm=2*N-1;
    uint8_t *tmp=malloc(n); int G,ys[16];
    dp=malloc((size_t)256*n); if(witness){ sp=malloc((size_t)256*n); pg=malloc((size_t)256*n); }
    for(;;){
        int ok=1; for(int i=0;i<N-1;i++) if(scanf("%d",&masks[N+i])!=1){ok=0;break;} if(!ok) break;
        if(scanf("%d %d",&cm,&G)!=2) return 1; for(int i=0;i<G;i++) if(scanf("%d",&ys[i])!=1) return 1;
        for(int S=1;S<(1<<G);S++){
            uint8_t *D=dp+(size_t)S*n; memset(tmp,200,n);
            if(witness){ memset(sp+(size_t)S*n,0,n); memset(pg+(size_t)S*n,-1,n); }
            if(__builtin_popcount(S)==1){ int y=ys[__builtin_ctz(S)]; int h=0; for(int x=0;x<N;x++) if(__builtin_popcount(y&x)&1) h|=1<<x; tmp[h]=0; tmp[h^(n-1)]=0; }
            else { int low=S&-S; for(int S1=(S-1)&S;S1>0;S1=(S1-1)&S){ if(!(S1&low)) continue; uint8_t *A=dp+(size_t)S1*n,*B=dp+(size_t)(S^S1)*n;
                    if(witness){ uint8_t *sq=sp+(size_t)S*n; for(int v=0;v<n;v++){ uint8_t t=A[v]+B[v]; if(t<tmp[v]){tmp[v]=t; sq[v]=S1;} } }
                    else for(int v=0;v<n;v++){ uint8_t t=A[v]+B[v]; if(t<tmp[v]) tmp[v]=t; } } }
            memcpy(D,tmp,n); int mn=255; for(int v=0;v<n;v++) if(D[v]<mn) mn=D[v];
            for(int d=mn;d<200;d++){ int more=0;
                for(int v=0;v<n;v++){ if(D[v]==d){ for(int g=0;g<nm;g++){ int w=nbr(v,g); if(w>=0 && D[w]>d+1){ D[w]=d+1; if(witness) pg[(size_t)S*n+w]=g; } } } else if(D[v]>d) more=1; }
                if(!more) break; }
        }
        printf("%d\n", dp[(size_t)((1<<G)-1)*n+cm]);
        if(witness) back((1<<G)-1,cm);
        fflush(stdout);
    }
    return 0;
}
