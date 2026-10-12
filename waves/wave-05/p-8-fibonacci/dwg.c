// p-8-fibonacci/dwg.c : generic exact shortest tree (Dreyfus-Wagner) in GF(P)^D with a given list of unit steps.
// Input: P D G T ; G step vectors (D digits) ; T groups: "c  v_1 .. v_c" (the tree must touch one point of each) ; start vector.
// Output: least number of steps of a tree that contains the start and one point of every group.  T <= 8.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
int main(void){
    int P,D,G,T; if(scanf("%d %d %d %d",&P,&D,&G,&T)!=4) return 1;
    int n=1; for(int i=0;i<D;i++) n*=P;
    int *dg=malloc(sizeof(int)*(size_t)n*D); for(int v=0;v<n;v++){ int x=v; for(int i=0;i<D;i++){ dg[(size_t)v*D+i]=x%P; x/=P; } }
    int *nb=malloc(sizeof(int)*(size_t)G*n);
    for(int g=0;g<G;g++){ int a[32]; for(int i=0;i<D;i++) scanf("%d",&a[i]);
        for(int v=0;v<n;v++){ int w=0; int *d=dg+(size_t)v*D; for(int i=D-1;i>=0;i--){ int x=d[i]+a[i]; if(x>=P) x-=P; w=w*P+x; } nb[(size_t)g*n+v]=w; } }
    uint8_t *dp=malloc((size_t)(1<<T)*n), *tmp=malloc(n);
    for(int t=0;t<T;t++){ uint8_t *Dp=dp+(size_t)(1<<t)*n; memset(Dp,200,n); int c; scanf("%d",&c);
        for(int j=0;j<c;j++){ int w=0,a[32]; for(int i=0;i<D;i++) scanf("%d",&a[i]); for(int i=D-1;i>=0;i--) w=w*P+a[i]; Dp[w]=0; } }
    int start=0; { int a[32]; for(int i=0;i<D;i++) scanf("%d",&a[i]); for(int i=D-1;i>=0;i--) start=start*P+a[i]; }
    for(int S=1;S<(1<<T);S++){
        uint8_t *Dp=dp+(size_t)S*n;
        if(__builtin_popcount(S)>1){ memset(tmp,200,n); int low=S&-S;
            for(int S1=(S-1)&S;S1>0;S1=(S1-1)&S){ if(!(S1&low)) continue; uint8_t *A=dp+(size_t)S1*n,*B=dp+(size_t)(S^S1)*n;
                for(int v=0;v<n;v++){ uint8_t t=A[v]+B[v]; if(t<tmp[v]) tmp[v]=t; } }
            memcpy(Dp,tmp,n); }
        int mn=255; for(int v=0;v<n;v++) if(Dp[v]<mn) mn=Dp[v];
        for(int d=mn;d<200;d++){ int more=0;
            for(int v=0;v<n;v++){ if(Dp[v]==d){ for(int g=0;g<G;g++){ int w=nb[(size_t)g*n+v]; if(Dp[w]>d+1) Dp[w]=d+1; } } else if(Dp[v]>d) more=1; }
            if(!more) break; }
    }
    printf("%d\n", dp[(size_t)((1<<T)-1)*n+start]); return 0;
}
