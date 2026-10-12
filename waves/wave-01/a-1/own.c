// a-1 own.c: independent exhaustive search (not derived from mincirc.c) for a linear circuit over GF(p), scalings free.
// gates = (#targets) + (#intermediates). State = set of projective points. After every addition all targets lying on a line
// through two present points are added (free of the intermediate budget). Intermediates are tried in a canonical order:
// if z2 was already constructible before z1 was added, require z2 > z1 (any valid sequence can be bubble-sorted into this form).
// usage: own p n m < rows     -> prints FOUND / NONE and node counts
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int p, n, m, PN;
static int *normt; static unsigned char *present; static unsigned *stamp[12], *stamp2;
static int pts[128], np, tgt[64], nt; static unsigned char done[64];
static unsigned long long nodes[12]; static unsigned nodeid = 0, id2 = 0;
static int dig(int c, int i){ while(i--) c/=p; return c%p; }
static int lin(int u, int a, int v){ int r=0, b=1; for(int i=0;i<n;i++){ r += ((u%p + a*(v%p))%p)*b; u/=p; v/=p; b*=p; } return r; }
static int nrm(int c){ return normt[c]; }
static int reach(int t){ for(int i=0;i<np;i++) for(int a=1;a<p;a++){ int v = nrm(lin(t,a,pts[i])); if(v && present[v]) return 1; } return 0; }
static int closure(int *added){ int na=0, ch=1; while(ch){ ch=0; for(int i=0;i<nt;i++) if(!done[i] && reach(tgt[i])){ done[i]=1; present[tgt[i]]=1; pts[np++]=tgt[i]; added[na++]=i; ch=1; } } return na; }
static void undo(int *added, int na){ for(int k=na-1;k>=0;k--){ int i=added[k]; done[i]=0; present[tgt[i]]=0; np--; } }
static int rem(void){ int r=0; for(int i=0;i<nt;i++) r+=!done[i]; return r; }
static int dfs(int budget, int depth, int lastz, unsigned parentid){
    int added[64]; int na = closure(added);
    if(rem()==0){ undo(added,na); return 1; }
    if(budget==0){ undo(added,na); return 0; }
    nodes[depth]++;
    unsigned id = ++nodeid; int nc=0; static int *cands[12]; if(!cands[depth]) cands[depth]=malloc(sizeof(int)*20000);
    int *cand = cands[depth];
    for(int i=0;i<np;i++) for(int j=i+1;j<np;j++) for(int a=1;a<p;a++){
        int z = nrm(lin(pts[i],a,pts[j])); if(!z || present[z] || stamp[depth][z]==id) continue; stamp[depth][z]=id; cand[nc++]=z; }
    if(budget==1){   // the last intermediate must put some missing target on a line with a present point
        unsigned t2 = ++id2; int snp = np;
        for(int i=0;i<nt;i++) if(!done[i]) for(int k=0;k<snp;k++) for(int a=1;a<p;a++){
            int z = nrm(lin(tgt[i],a,pts[k])); if(!z || present[z] || stamp[depth][z]!=id || stamp2[z]==t2) continue; stamp2[z]=t2;
            if(depth>0 && stamp[depth-1][z]==parentid && z<lastz) continue;
            present[z]=1; pts[np++]=z; int ad2[64]; int n2=closure(ad2); int ok = rem()==0; undo(ad2,n2); np--; present[z]=0;
            if(ok){ undo(added,na); return 1; } }
        undo(added,na); return 0;
    }
    for(int k=0;k<nc;k++){ int z=cand[k];
        if(depth>0 && stamp[depth-1][z]==parentid && z<lastz) continue;
        present[z]=1; pts[np++]=z; int r=dfs(budget-1, depth+1, z, id); np--; present[z]=0;
        if(r){ undo(added,na); return 1; } }
    undo(added,na); return 0;
}
int main(int argc, char **argv){
    p=atoi(argv[1]); n=atoi(argv[2]); m=atoi(argv[3]); PN=1; for(int i=0;i<n;i++) PN*=p;
    normt=calloc(PN,sizeof(int)); present=calloc(PN,1); stamp2=calloc(PN,sizeof(unsigned));
    for(int d=0;d<12;d++) stamp[d]=calloc(PN,sizeof(unsigned));
    int inv[64]; for(int a=1;a<p;a++) for(int b=1;b<p;b++) if(a*b%p==1) inv[a]=b;
    for(int c=1;c<PN;c++){ int lead=0; for(int i=n-1;i>=0;i--){ int d=dig(c,i); if(d){ lead=d; break; } } normt[c]=lin(0,inv[lead],c); }
    for(int i=0,b=1;i<n;i++,b*=p){ pts[np++]=b; present[b]=1; }
    int v; int row[64]; int k=0, nrows=0;
    while(scanf("%d",&v)==1){ row[k++]=((v%p)+p)%p; if(k==n){ int c=0,b=1; for(int i=0;i<n;i++,b*=p) c+=row[i]*b; c=nrm(c); nrows++;
        if(!c){ printf("zero row mod p\n"); return 2; } int dup=present[c]; for(int i=0;i<nt;i++) dup|=tgt[i]==c; if(!dup) tgt[nt++]=c; k=0; } }
    printf("own: p=%d n=%d rows=%d distinct non-input targets=%d intermediates=%d => gate budget %d\n", p,n,nrows,nt,m,nt+m);
    int r=dfs(m,0,0,0);
    printf("nodes by depth:"); for(int d=0;d<=m;d++) printf(" %llu", nodes[d]); printf("\n");
    printf("RESULT p=%d: %s with %d gates\n", p, r?"a circuit EXISTS":"NO circuit (exhaustive over this field)", nt+m);
    return 0;
}
