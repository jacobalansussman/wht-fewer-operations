// p-8-fibonacci/dw.c : exact minimum number of tree rectangles (tau) for the 2^K-point Walsh-Hadamard transform over GF(P),
// for ONE column merge tree and ONE column scaling c', minimised over ALL row merge trees, all row scalings and all numbers.
// Method (see p-8.md section 1): tau = length of the shortest Steiner tree that joins the origin and one point of each line
// {m * h_y} (h_y the rows) in the graph on GF(P)^N whose edges are  v -- v + m * c' * 1_B  (B a node of the column tree).
// Dreyfus-Wagner dynamic programme, exact.  Usage: dw P K [w] < lines "m1 .. m_{N-1}  c0 .. c_{N-1}"   (internal node masks, c')
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define MAXN 8
static int P, K, N, n, NT;
static int ngen; static int *nb;            // nb[g*n+v]
static uint8_t *dp; static uint8_t *sp; static int8_t *pg;
static int gen_node[64], gen_mul[64];
static int pw[MAXN+1];
static int witness;
static void digits(int v, int *d){ for(int i=0;i<N;i++){ d[i]=v%P; v/=P; } }
static int undig(int *d){ int v=0; for(int i=N-1;i>=0;i--) v=v*P+d[i]; return v; }
static void back(int S, int v){
    // print edges of the optimal tree for (S, v)
    while(pg[(size_t)S*n+v] >= 0){
        int g = pg[(size_t)S*n+v];
        // v = u + gen g  ->  u = v - gen g
        int d[MAXN], e[MAXN]; digits(v,d);
        // find u with nb[g][u] == v : subtract
        int u=-1; for(int m=0;m<ngen;m++) if(gen_node[m]==gen_node[g] && nb[(size_t)m*n+v]>=0 && nb[(size_t)g*n+nb[(size_t)m*n+v]]==v){ u=nb[(size_t)m*n+v]; break; }
        digits(u,e);
        printf("  edge  from"); for(int i=0;i<N;i++) printf(" %d",e[i]); printf("  to"); for(int i=0;i<N;i++) printf(" %d",d[i]);
        printf("   node %d  mult %d\n", gen_node[g], gen_mul[g]);
        v = u;
    }
    if(__builtin_popcount(S)==1){ int d[MAXN]; digits(v,d); printf("  terminal row %d at", __builtin_ctz(S)); for(int i=0;i<N;i++) printf(" %d",d[i]); printf("\n"); return; }
    int S1 = sp[(size_t)S*n+v];
    back(S1, v); back(S^S1, v);
}
int main(int argc, char **argv){
    P=atoi(argv[1]); K=atoi(argv[2]); witness = argc>3; N=1<<K; NT=N;
    n=1; for(int i=0;i<N;i++){ pw[i]=n; n*=P; }
    int nnodes = 2*N-1; int MAXE=4; ngen = (nnodes+MAXE)*(P-1); int basegen=nnodes*(P-1);
    nb = malloc(sizeof(int)*(size_t)ngen*n);
    dp = malloc((size_t)(1<<NT)*n);
    if(witness){ sp = malloc((size_t)(1<<NT)*n); pg = malloc((size_t)(1<<NT)*n); }
    uint8_t *tmp = malloc(n); int *dg = malloc(sizeof(int)*(size_t)n*N);
    for(int v=0;v<n;v++) digits(v, dg+(size_t)v*N);
    int masks[2*MAXN], c[MAXN];
    for(;;){
        int ok=1;
        for(int i=0;i<N-1;i++) if(scanf("%d",&masks[N+i])!=1){ ok=0; break; }
        if(!ok) break;
        for(int i=0;i<N;i++) if(scanf("%d",&c[i])!=1) return 1;
        for(int i=0;i<N;i++) masks[i]=1<<i;
        int E=0; if(scanf("%d",&E)!=1) return 1; int ex[4][MAXN]; for(int e=0;e<E;e++) for(int i=0;i<N;i++) if(scanf("%d",&ex[e][i])!=1) return 1;
        ngen=(nnodes+E)*(P-1); (void)basegen;
        int g=0;
        for(int b=0;b<nnodes;b++) for(int m=1;m<P;m++){
            gen_node[g]=masks[b]; gen_mul[g]=m;
            int add[MAXN]; for(int i=0;i<N;i++) add[i] = (masks[b]>>i&1) ? (m*c[i])%P : 0;
            for(int v=0;v<n;v++){ int w=0; int *d=dg+(size_t)v*N; for(int i=N-1;i>=0;i--){ int x=d[i]+add[i]; if(x>=P) x-=P; w=w*P+x; } nb[(size_t)g*n+v]=w; }
            g++;
        }
        for(int e=0;e<E;e++) for(int m=1;m<P;m++){
            gen_node[g]=1000+e; gen_mul[g]=m;
            for(int v=0;v<n;v++){ int w=0; int *d=dg+(size_t)v*N; for(int i=N-1;i>=0;i--){ int x=(d[i]+m*ex[e][i])%P; w=w*P+x; } nb[(size_t)g*n+v]=w; }
            g++;
        }
        for(int S=1;S<(1<<NT);S++){
            uint8_t *D = dp+(size_t)S*n;
            if(__builtin_popcount(S)==1){
                int y=__builtin_ctz(S); memset(tmp,200,n);
                for(int m=1;m<P;m++){ int d[MAXN]; for(int x=0;x<N;x++){ int s=(__builtin_popcount(y&x)&1)? P-1:1; d[x]=(m*s)%P; } tmp[undig(d)]=0; }
                if(witness) memset(sp+(size_t)S*n,0,n);
            } else {
                memset(tmp,200,n); int low = S & -S;
                if(witness) memset(sp+(size_t)S*n,0,n);
                for(int S1=(S-1)&S; S1>0; S1=(S1-1)&S){
                    if(!(S1&low)) continue;
                    uint8_t *A=dp+(size_t)S1*n, *B=dp+(size_t)(S^S1)*n;
                    if(witness){ uint8_t *sq=sp+(size_t)S*n; for(int v=0;v<n;v++){ uint8_t t=A[v]+B[v]; if(t<tmp[v]){ tmp[v]=t; sq[v]=S1; } } }
                    else for(int v=0;v<n;v++){ uint8_t t=A[v]+B[v]; if(t<tmp[v]) tmp[v]=t; }
                }
            }
            memcpy(D,tmp,n);
            if(witness) memset(pg+(size_t)S*n,-1,n);
            int mx=0, mn=255; for(int v=0;v<n;v++){ if(D[v]<mn) mn=D[v]; }
            for(int d=mn; d<200; d++){
                int any=0, more=0;
                for(int v=0;v<n;v++){
                    if(D[v]==d){ any=1;
                        for(int gg=0;gg<ngen;gg++){ int w=nb[(size_t)gg*n+v]; if(D[w]>d+1){ D[w]=d+1; if(witness) pg[(size_t)S*n+w]=gg; } }
                    } else if(D[v]>d) more=1;
                }
                if(!more) break; (void)any; (void)mx;
            }
        }
        int tau = dp[(size_t)((1<<NT)-1)*n + 0];
        printf("%d\n", tau);
        if(witness){ back((1<<NT)-1, 0); }
        fflush(stdout);
    }
    return 0;
}
