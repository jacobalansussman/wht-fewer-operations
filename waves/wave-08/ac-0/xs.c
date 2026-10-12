// xs.c (ac-0): my own exhaustive search for the least number of gates u+v that compute the 8 rows of one block of
// neighbour sums at 16 points, (a) modulo 2 (XOR gates), (b) "adding only" (no cancellation: supports disjoint,
// every wire a subset of some row). Written from scratch; shares no code with mincirc.
// A circuit = 8 gates that output the 8 rows + m further wires ("intermediates"). State = set of vectors present.
// Closure: any row that is the sum of two present vectors is added at once (its gate must be paid anyway and more
// vectors never hurt). Branch: one new intermediate = sum of two present vectors. A candidate already tried at an
// ancestor is banned below its later siblings (a solution containing it would have been found in its own subtree).
// usage: xs <m> <mode 0=xor 1=adding-only> <stopfirst 0/1>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static int T[8], ist[256], mode, stopfirst; static unsigned long long nodes[16], found;
static int ok_sub[256];
typedef struct { uint64_t w[4]; } bs;
static inline int tst(const bs*b,int x){return (b->w[x>>6]>>(x&63))&1;}
static inline void st(bs*b,int x){b->w[x>>6]|=1ULL<<(x&63);}
static int combine(int u,int v){ if(mode==0) return u^v; if(u&v) return 0; int c=u|v; return ok_sub[c]?c:0; }
static int pts_sol[64], nsol;
static int dfs(int *pts,int n,bs have,bs banned,int budget){
    int loc[64]; memcpy(loc,pts,n*sizeof(int));
    // closure
    int changed=1;
    while(changed){ changed=0;
        for(int i=0;i<n;i++)for(int j=i+1;j<n;j++){int c=combine(loc[i],loc[j]); if(c&&ist[c]&&!tst(&have,c)){st(&have,c);loc[n++]=c;changed=1;}}
    }
    nodes[budget]++;
    int all=1; for(int t=0;t<8;t++) if(!tst(&have,T[t])) {all=0;break;}
    if(all){ found++; if(found==1){nsol=n; memcpy(pts_sol,loc,n*sizeof(int));} return 1; }
    if(budget==0) return 0;
    bs seen; memset(&seen,0,sizeof seen); int any=0;
    for(int i=0;i<n;i++)for(int j=i+1;j<n;j++){
        int c=combine(loc[i],loc[j]); if(!c||tst(&have,c)||tst(&banned,c)||tst(&seen,c)) continue;
        st(&seen,c);
        bs h2=have; st(&h2,c); loc[n]=c;
        if(dfs(loc,n+1,h2,banned,budget-1)){ any=1; if(stopfirst) return 1; }
        st(&banned,c);
    }
    return any;
}
int main(int argc,char**argv){
    int m=atoi(argv[1]); mode=atoi(argv[2]); stopfirst=atoi(argv[3]);
    // build the block myself: inputs = even-weight addresses in increasing order, outputs = odd-weight addresses
    int ev[8],od[8],ne=0,no=0; for(int x=0;x<16;x++){ if(__builtin_popcount(x)&1) od[no++]=x; else ev[ne++]=x; }
    for(int i=0;i<8;i++){ int r=0; for(int j=0;j<8;j++) if(__builtin_popcount(od[i]^ev[j])==1) r|=1<<j; T[i]=r; ist[r]=1; }
    for(int c=1;c<256;c++){ for(int i=0;i<8;i++) if((c&T[i])==c) ok_sub[c]=1; }
    int pts[64]; bs have,banned; memset(&have,0,sizeof have); memset(&banned,0,sizeof banned);
    for(int j=0;j<8;j++){pts[j]=1<<j; st(&have,1<<j);}
    int r=dfs(pts,8,have,banned,m);
    printf("mode=%s m=%d gates=%d : %s", mode?"adding-only":"xor (modulo 2)", m, 8+m, r?"YES":"NO (exhaustive)");
    if(!stopfirst) printf("  number of terminal successes=%llu",found);
    printf("\nnodes by remaining budget:"); for(int b=m;b>=0;b--) printf(" %d:%llu",b,nodes[b]); printf("\n");
    if(r){ printf("first solution, vectors after the inputs (bit j = input j):"); for(int i=8;i<nsol;i++) printf(" %02x%s",pts_sol[i],ist[pts_sol[i]]?"*":""); printf("\n"); }
    return 0;
}
