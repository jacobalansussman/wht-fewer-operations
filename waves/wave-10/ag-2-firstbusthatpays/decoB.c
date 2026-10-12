// ag-2: ROOM "the ninth injection", general.  TWO-ELEMENT FIELD, count (G).  Upper circuit C'' = a derivation of a 12-gate
// circuit (12 M2 gates), NINE injections: 9 classes whose reaches have rank 8 (one dependency Dep), or 8 independent classes
// and one version used by no gate (reach 0, "ghost": ad-2's class B).  The offsets are d0 + v on the classes of Dep, v ANY
// form.  Gates 12 + 9 + pure + deliveries: 31 needs pure + deliveries <= 10 (BOUND=10), a tie (32) is BOUND=11.
// One delivery w: census f(Z | w free) + 1 <= BOUND (at BOUND=10 only the lower total passes), w = difference of two
// versions of one wire joined by a tree path of >= 14 - BOUND injections (fewer cannot pay: replace the cancelling gate by
// a chain of pure gates), single-edge test, then the exact joint search over trees.  Pairs of deliveries: NOT covered.
// ag-2: class A of ad-2's decorated cut, ported to C, for EVERY upper circuit C''.  TWO-ELEMENT FIELD, count (G).
// Cut of 16 points; upper circuit C'' = one derivation of one 12-gate circuit for Z on 8 points (list z8_sets.txt);
// 12 M2 gates, exactly 8 injections (extra = 0), groupings of consumer slots into 8 classes with independent reaches,
// forced offsets d = T^-1 Z, at least one wire with >= 3 classes (a bus).  A 31-gate circuit in this class needs a set Dl
// of deliveries (differences of two versions of a bus wire) with |Dl| + pure(Dl free; lower outputs + injected) <= 11.
// NECESSARY conditions tested here, each by the exact search of ad-2's free8 (copied below):
//   census : |Dl| + f(Z | Dl free) <= 11
//   edges  : every wire's versions are connected by differences e with |Dl| + f(Z and e | Dl free) <= 11
// A structure that passes both for some Dl with |Dl| <= MAXD is printed as a SURVIVOR (still only a candidate).
// usage: decoA z8_sets.txt single8.txt pairsdir M r [MAXD]     (derivations with index = r modulo M)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define n 8
#define NP 256
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
static int Zrow[8], zindex[256];
static int XT[64], nXT=0;
static long ncalls=0; static int BOUND=11; static int MINPATH=4;
// least gates given free set W and extra targets XT, if <= bound; else 99
static int mingates_le(const int *W,int nW,int bound){
    ncalls++;
    memset(cnt,0,sizeof cnt); memset(inR,0,sizeof inR); nR=0; nT=0;
    for(int i=0;i<n;i++) add_point(1<<i);
    for(int i=0;i<nW;i++) if(W[i]&&!inR[W[i]]) add_point(W[i]);
    for(int S=1;S<n;S++){ int t=Zrow[S]; if(!inR[t]) T[nT++]=t; }
    for(int i=0;i<nXT;i++){ int t=XT[i], dup=inR[t]; for(int k=0;k<nT;k++) if(T[k]==t) dup=1; if(!dup&&t) T[nT++]=t; }
    int nT0=nT;
    for(int m=0;m<12&&nT0+m<=bound;m++){
        stamp++; if(stamp==0){ memset(seen,0,sizeof seen); stamp=1; }
        int keep=nR; int ad=closure(); nI=0;
        int ok=dfs(m);
        for(int k=0;k<ad;k++) remove_last();
        if(nR!=keep){ fprintf(stderr,"state error\n"); exit(3); }
        if(ok) return nT0+m;
    }
    return 99;
}
// ---------- caches ----------
static unsigned char S1g[256], S2g[256][256];
static unsigned char ok1[256][256];
#define HB 23
static uint64_t *hk; static unsigned char *hv;
static unsigned char *hget(uint64_t key){ uint64_t h=(key*0x9E3779B97F4A7C15ULL)>>(64-HB);
    while(hk[h]&&hk[h]!=key) h=(h+1)&((1u<<HB)-1);
    if(!hk[h]){ hk[h]=key; hv[h]=0; } return &hv[h]; }
static int census(const int *D,int k){
    if(k==1) return S1g[D[0]]<=10;
    if(k==2) return S2g[D[0]][D[1]]<=9;
    uint64_t key=((uint64_t)k<<40); for(int i=0;i<k;i++) key=key*257+D[i]+1; key|=1ULL<<62;
    unsigned char *p=hget(key);
    if(!*p){ nXT=0; *p=(mingates_le(D,k,11-k)<=11-k)?1:2; }
    return *p==1;
}
static int okedge(const int *D,int k,int e){
    if(__builtin_popcount(e)==1) return 1;
    for(int i=0;i<k;i++) if(D[i]==e) return 1;
    unsigned char *p;
    if(k==1) p=&ok1[D[0]][e];
    else { uint64_t key=((uint64_t)k<<40); for(int i=0;i<k;i++) key=key*257+D[i]+1; key=key*257+e+1; key|=1ULL<<61; p=hget(key); }
    if(!*p){ nXT=1; XT[0]=e; *p=(mingates_le(D,k,BOUND-k)<=BOUND-k)?1:2; nXT=0; }
    return *p==1;
}

// ---------- stage 2: exact.  Choose a spanning tree on the versions of every wire (edges = injected pure wires);
// every delivery of D must join two versions of one wire at tree distance >= 3; then |D| + pure(D free; outputs and all
// injected wires) <= BOUND, by the exact search, pruned wire by wire (adding targets never lowers the count).
static int s2_D[4], s2_k, s2_nw, s2_wm[10], s2_wp[10][10];
static int s2_ea[10][16], s2_eb[10][16], s2_ne[10], s2_ch[10][6];
static int Xc[256]; static long st_s2calls=0;
static int feasibleX(void){
    int xs[40], nx=0;
    for(int f=3;f<256;f++) if(Xc[f]>0&&__builtin_popcount(f)>1){ int inD=0; for(int j=0;j<s2_k;j++) if(s2_D[j]==f) inD=1; if(!inD) xs[nx++]=f; }
    uint64_t key=1469598103934665603ULL; for(int j=0;j<s2_k;j++){ key^=(uint64_t)(s2_D[j]+1); key*=1099511628211ULL; }
    key^=0x1000; key*=1099511628211ULL; for(int j=0;j<nx;j++){ key^=(uint64_t)(xs[j]+1); key*=1099511628211ULL; }
    key^=(uint64_t)BOUND<<50; key|=1ULL<<63;
    unsigned char *p=hget(key);
    if(!*p){ nXT=nx; for(int j=0;j<nx;j++) XT[j]=xs[j]; st_s2calls++; *p=(mingates_le(s2_D,s2_k,BOUND-s2_k)<=BOUND-s2_k)?1:2; nXT=0; }
    return *p==1;
}
static int dfs2(int i,int realised){
    if(i==s2_nw) return realised==(1<<s2_k)-1;
    int m=s2_wm[i], ne=s2_ne[i], idx[6];
    if(ne<m) return 0;
    for(int x=0;x<m;x++) idx[x]=x;
    while(1){
        int comp[9], ok=1; for(int x=0;x<=m;x++) comp[x]=x;
        for(int x=0;x<m&&ok;x++){ int a=s2_ea[i][idx[x]], b=s2_eb[i][idx[x]]; if(comp[a]==comp[b]) ok=0; else { int cb=comp[b],ca=comp[a]; for(int z=0;z<=m;z++) if(comp[z]==cb) comp[z]=ca; } }
        if(ok){
            int r=realised;
            if(m>=3){ int dist[7][7]; for(int a=0;a<=m;a++) for(int b=0;b<=m;b++) dist[a][b]=(a==b)?0:99;
                for(int x=0;x<m;x++){ int a=s2_ea[i][idx[x]], b=s2_eb[i][idx[x]]; dist[a][b]=dist[b][a]=1; }
                for(int c=0;c<=m;c++) for(int a=0;a<=m;a++) for(int b=0;b<=m;b++) if(dist[a][c]+dist[c][b]<dist[a][b]) dist[a][b]=dist[a][c]+dist[c][b];
                for(int a=0;a<=m;a++) for(int b=a+1;b<=m;b++) if(dist[a][b]>=MINPATH){ int f=s2_wp[i][a]^s2_wp[i][b]; for(int j=0;j<s2_k;j++) if(s2_D[j]==f) r|=1<<j; } }
            for(int x=0;x<m;x++){ Xc[s2_wp[i][s2_ea[i][idx[x]]]^s2_wp[i][s2_eb[i][idx[x]]]]++; s2_ch[i][x]=idx[x]; }
            int res=feasibleX()&&dfs2(i+1,r);
            for(int x=0;x<m;x++) Xc[s2_wp[i][s2_ea[i][idx[x]]]^s2_wp[i][s2_eb[i][idx[x]]]]--;
            if(res) return 1;
        }
        int x=m-1; while(x>=0&&idx[x]==ne-m+x) x--; if(x<0) break; idx[x]++; for(int y=x+1;y<m;y++) idx[y]=idx[y-1]+1;
    }
    return 0;
}
// ---------- the upper circuit ----------
static int forms[12], optU[12][80], optV[12][80], nopt[12], choice[12];
static long deriv_idx=0, M=1, RR=0; static int MAXD=2;
static int W20[20], nsl[20], sl[20][10], wl[20], capS[21], canbig[21], SYM=0; static long nsets_canon=0;
static int cw[10], ct[10], ncl, basis[8], bmask[8], defect, depm, blk[20][10], WL[64], nWL;
static long st_struct=0, st_cens[8], st_surv[8], st_all=0, st_s2[8], st_found=0, d_found; static long d_struct, d_surv; static int shown=0;
static int gf[12],gu[12],gv[12];
static int reduce(int t){ while(t){ int l=31-__builtin_clz(t); if(!basis[l]) return t; t^=basis[l]; } return 0; }
static void pr(int w){ for(int i=0;i<8;i++) putchar(((w>>i)&1)?'1':'0'); }
static void leaf(void){
    st_struct++; d_struct++;
    int a[8],b[8],d[8];
    for(int S=0;S<8;S++){ int m=0; for(int k=0;k<8;k++) m|=((ct[k]>>S)&1)<<k; a[S]=m; b[S]=Zrow[S]; }
    for(int c=0;c<8;c++){ int piv=c; while(!((a[piv]>>c)&1)) piv++; int t=a[c];a[c]=a[piv];a[piv]=t; t=b[c];b[c]=b[piv];b[piv]=t;
        for(int r=0;r<8;r++) if(r!=c&&((a[r]>>c)&1)){ a[r]^=a[c]; b[r]^=b[c]; } }
    for(int k=0;k<8;k++) d[k]=b[k];
    // wires and their versions
    int ws[8], wm[8], wp[8][9], nw=0;
    for(int k=0;k<8;k++){ if(nw==0||ws[nw-1]!=cw[k]){ ws[nw]=cw[k]; wm[nw]=0; wp[nw][0]=0; nw++; } wm[nw-1]++; wp[nw-1][wm[nw-1]]=d[k]; }
    int Wf[64], nW=0; unsigned char inW[256]; memset(inW,0,sizeof inW);
    for(int i=0;i<nw;i++) if(wm[i]>=3) for(int x=0;x<=wm[i];x++) for(int y=x+1;y<=wm[i];y++){ int f=wp[i][x]^wp[i][y];
        if(__builtin_popcount(f)>1&&!inW[f]){ inW[f]=1; Wf[nW++]=f; } }
    // sort W
    for(int i=1;i<nW;i++){ int v=Wf[i],j=i; while(j>0&&Wf[j-1]>v){Wf[j]=Wf[j-1];j--;} Wf[j]=v; }
    int idx[4], anyfound=0;
    for(int k=1;k<=MAXD&&k<=nW;k++){
        for(int i=0;i<k;i++) idx[i]=i;
        while(1){
            int D[4]; for(int i=0;i<k;i++) D[i]=Wf[idx[i]];
            if(census(D,k)){
                st_cens[k]++;
                int good=1;
                for(int i=0;i<nw&&good;i++){
                    int comp[9]; for(int x=0;x<=wm[i];x++) comp[x]=x;
                    for(int x=0;x<=wm[i];x++) for(int y=x+1;y<=wm[i];y++) if(comp[x]!=comp[y]&&okedge(D,k,wp[i][x]^wp[i][y])){
                        int cy=comp[y],cx=comp[x]; for(int z=0;z<=wm[i];z++) if(comp[z]==cy) comp[z]=cx; }
                    for(int x=1;x<=wm[i];x++) if(comp[x]!=comp[0]) good=0;
                }
                if(good){ st_surv[k]++; d_surv++;
                    s2_k=k; for(int i=0;i<k;i++) s2_D[i]=D[i]; s2_nw=nw;
                    for(int i=0;i<nw;i++){ s2_wm[i]=wm[i]; s2_ne[i]=0; for(int x=0;x<=wm[i];x++) s2_wp[i][x]=wp[i][x];
                        for(int x=0;x<=wm[i];x++) for(int y=x+1;y<=wm[i];y++) if(okedge(D,k,wp[i][x]^wp[i][y])){ s2_ea[i][s2_ne[i]]=x; s2_eb[i][s2_ne[i]]=y; s2_ne[i]++; } }
                    memset(Xc,0,sizeof Xc);
                    if(dfs2(0,0)){ st_s2[k]++; anyfound=1;
                        if(shown<60){ shown++; printf("FOUND (pure + deliveries <= %d) deriv %ld deliveries",BOUND,deriv_idx); for(int i=0;i<k;i++){ putchar(' '); pr(D[i]); }
                        printf(" | injected (per wire: version offsets ; tree edges):"); for(int i=0;i<nw;i++){ printf(" ["); pr(W20[ws[i]]); printf(":"); for(int x=0;x<=wm[i];x++){ putchar(' '); pr(wp[i][x]); } printf(" ;"); for(int x=0;x<wm[i];x++){ putchar(' '); pr(wp[i][s2_ea[i][s2_ch[i][x]]]^wp[i][s2_eb[i][s2_ch[i][x]]]); } printf("]"); }
                        printf(" | classes (wire tau offset):"); for(int c=0;c<8;c++){ putchar(' '); pr(W20[cw[c]]); putchar('/'); pr(ct[c]); putchar('/'); pr(d[c]); }
                        printf(" | C''"); for(int g=0;g<12;g++){ putchar(' '); pr(gf[g]); putchar('='); pr(gu[g]); putchar('+'); pr(gv[g]); } printf("\n"); fflush(stdout); } } }
            }
            int i=k-1; while(i>=0&&idx[i]==nW-k+i) i--; if(i<0) break; idx[i]++; for(int j=i+1;j<k;j++) idx[j]=idx[j-1]+1;
        }
    }
    if(anyfound){ st_found++; d_found++; }
}

static void leaf9(void){
    st_struct++; d_struct++;
    int fr=__builtin_ctz(depm), col[8], nc=0, a[8], b[8], d0[10];
    for(int k=0;k<9;k++) if(k!=fr) col[nc++]=k;
    for(int S=0;S<8;S++){ int m=0; for(int q=0;q<8;q++) m|=((ct[col[q]]>>S)&1)<<q; a[S]=m; b[S]=Zrow[S]; }
    for(int c=0;c<8;c++){ int piv=c; while(piv<8&&!((a[piv]>>c)&1)) piv++; if(piv==8){ fprintf(stderr,"rank error\n"); exit(5); }
        int t=a[c];a[c]=a[piv];a[piv]=t; t=b[c];b[c]=b[piv];b[piv]=t;
        for(int r=0;r<8;r++) if(r!=c&&((a[r]>>c)&1)){ a[r]^=a[c]; b[r]^=b[c]; } }
    d0[fr]=0; for(int q=0;q<8;q++) d0[col[q]]=b[q];
    int ws[10], wm[10], wk[10][7], nw=0;
    for(int k=0;k<9;k++){ if(nw==0||ws[nw-1]!=cw[k]){ ws[nw]=cw[k]; wm[nw]=0; nw++; } wk[nw-1][++wm[nw-1]]=k; }
    // candidate (v, w): w = difference of two versions of a wire with >= MINPATH classes
    static unsigned char mk[64][256]; int any=0, anyfound=0;
    for(int i=0;i<nw;i++) if(wm[i]>=MINPATH) for(int x=0;x<=wm[i];x++) for(int y=x+1;y<=wm[i];y++){
        int base=(x?d0[wk[i][x]]:0)^d0[wk[i][y]], inD=(x?((depm>>wk[i][x])&1):0)^((depm>>wk[i][y])&1);
        for(int q=0;q<nWL;q++){ if(inD){ if(!any){ memset(mk,0,sizeof mk); any=1; } mk[q][WL[q]^base]=1; }
            else if(base==WL[q]){ if(!any){ memset(mk,0,sizeof mk); any=1; } memset(mk[q],1,256); } } }
    if(!any) return;
    for(int q=0;q<nWL;q++) for(int v=0;v<256;v++) if(mk[q][v]){
        int D[1]={WL[q]}, wp[10][10], good=1; st_cens[1]++;
        for(int i=0;i<nw&&good;i++){ wp[i][0]=0; for(int x=1;x<=wm[i];x++){ int k=wk[i][x]; wp[i][x]=d0[k]^(((depm>>k)&1)?v:0); }
            for(int x=0;x<=wm[i]&&good;x++) for(int y=x+1;y<=wm[i];y++) if(wp[i][x]==wp[i][y]){ good=0; break; } }
        for(int i=0;i<nw&&good;i++){ int comp[10]; for(int x=0;x<=wm[i];x++) comp[x]=x;
            for(int x=0;x<=wm[i];x++) for(int y=x+1;y<=wm[i];y++) if(comp[x]!=comp[y]&&okedge(D,1,wp[i][x]^wp[i][y])){
                int cy=comp[y],cx=comp[x]; for(int z=0;z<=wm[i];z++) if(comp[z]==cy) comp[z]=cx; }
            for(int x=1;x<=wm[i];x++) if(comp[x]!=comp[0]) good=0; }
        if(!good) continue;
        st_surv[1]++; d_surv++;
        s2_k=1; s2_D[0]=D[0]; s2_nw=nw;
        for(int i=0;i<nw;i++){ s2_wm[i]=wm[i]; s2_ne[i]=0; for(int x=0;x<=wm[i];x++) s2_wp[i][x]=wp[i][x];
            for(int x=0;x<=wm[i];x++) for(int y=x+1;y<=wm[i];y++) if(okedge(D,1,wp[i][x]^wp[i][y])){ s2_ea[i][s2_ne[i]]=x; s2_eb[i][s2_ne[i]]=y; s2_ne[i]++; } }
        memset(Xc,0,sizeof Xc);
        if(dfs2(0,0)){ st_s2[1]++; anyfound=1;
            if(shown<40){ shown++; printf("FOUND (pure + 1 <= %d, path >= %d) deriv %ld delivered ",BOUND,MINPATH,deriv_idx); pr(D[0]); printf(" free form v = "); pr(v); printf(" dependency mask %d",depm);
                printf(" | per wire (version offsets ; injected):"); for(int i=0;i<nw;i++){ printf(" ["); pr(W20[ws[i]]); printf(":"); for(int x=0;x<=wm[i];x++){ putchar(' '); pr(wp[i][x]); } printf(" ;"); for(int x=0;x<wm[i];x++){ putchar(' '); pr(wp[i][s2_ea[i][s2_ch[i][x]]]^wp[i][s2_eb[i][s2_ch[i][x]]]); } printf("]"); }
                printf(" | classes (wire tau):"); for(int c=0;c<9;c++){ putchar(' '); pr(W20[cw[c]]); putchar('/'); pr(ct[c]); }
                printf(" | C''"); for(int g=0;g<12;g++){ putchar(' '); pr(gf[g]); putchar('='); pr(gu[g]); putchar('+'); pr(gv[g]); } printf("\n"); fflush(stdout); } }
    }
    if(anyfound){ st_found++; d_found++; }
}
static void rec(int i,int big);
static void assign(int i,int j,int nb,int big){
    int w=wl[i], q=nsl[w];
    if(ncl+nb>9) return;
    if(j==q){
        for(int ghost=0;ghost<=1;ghost++){
            if(ghost&&(defect||ncl+nb+1>9)) break;
            int sb[8],sm[8]; memcpy(sb,basis,sizeof sb); memcpy(sm,bmask,sizeof sm); int sn=ncl, sd=defect, sp=depm, ok=1;
            for(int b=1;b<=nb;b++){ int t=0; for(int s=0;s<q;s++) if(blk[i][s]==b) t^=sl[w][s];
                int v=t, m=1<<ncl; while(v){ int l=31-__builtin_clz(v); if(!basis[l]){ basis[l]=v; bmask[l]=m; break; } v^=basis[l]; m^=bmask[l]; }
                if(!v){ if(defect){ ok=0; break; } defect=1; depm=m; }
                cw[ncl]=w; ct[ncl]=t; ncl++; }
            if(ok&&ghost){ if(defect) ok=0; else { defect=1; depm=1<<ncl; cw[ncl]=w; ct[ncl]=0; ncl++; } }
            if(ok) rec(i+1,big||nb+ghost>=MINPATH);
            memcpy(basis,sb,sizeof sb); memcpy(bmask,sm,sizeof sm); ncl=sn; defect=sd; depm=sp;
        }
        return;
    }
    for(int b=0;b<=nb+1;b++){ blk[i][j]=b; assign(i,j+1,b==nb+1?nb+1:nb,big); }
}
static void rec(int i,int big){
    if(ncl==9){ st_all++; if(big&&defect) leaf9(); return; }
    if(i==20||ncl+capS[i]+(defect?0:1)<9) return;
    if(!big&&!canbig[i]) return;   /* no wire left whose slot reaches have rank >= 3 */
    assign(i,0,0,big);
}
static void process(void){
    int pu[12],pv[12]; for(int i=0;i<12;i++){ pu[i]=optU[i][choice[i]]; pv[i]=optV[i][choice[i]]; }
    unsigned char done[256]; memset(done,0,sizeof done); for(int j=0;j<8;j++) done[1<<j]=1;
    int order[12],no=0,ch=1;
    while(ch){ ch=0; for(int i=0;i<12;i++){ int f=forms[i]; if(!done[f]&&done[pu[i]]&&done[pv[i]]){ done[f]=1; order[no++]=i; ch=1; } } }
    if(no!=12) return;
    deriv_idx++;
    if((deriv_idx-1)%M!=RR) return;
    int widx[256]; memset(widx,-1,sizeof widx);
    for(int j=0;j<8;j++){ W20[j]=1<<j; widx[1<<j]=j; }
    for(int k=0;k<12;k++){ gf[k]=forms[order[k]]; gu[k]=pu[order[k]]; gv[k]=pv[order[k]]; W20[8+k]=gf[k]; widx[gf[k]]=8+k; }
    int users[20][12], nu[20]; memset(nu,0,sizeof nu);
    for(int k=0;k<12;k++){ int u=widx[gu[k]], v=widx[gv[k]]; users[u][nu[u]++]=8+k; users[v][nu[v]++]=8+k; }
    int sig[20];
    for(int i=19;i>=0;i--){ int s=0, zi=zindex[W20[i]]; if(zi>=0) s^=1<<zi; for(int x=0;x<nu[i];x++) s^=sig[users[i][x]]; sig[i]=s; }
    for(int i=0;i<20;i++){ nsl[i]=0; for(int x=0;x<nu[i];x++) sl[i][nsl[i]++]=sig[users[i][x]]; int zi=zindex[W20[i]]; if(zi>=0) sl[i][nsl[i]++]=1<<zi;
        if(nsl[i]>9){ fprintf(stderr,"too many slots\n"); exit(4); } }
    for(int i=0;i<20;i++) wl[i]=i;
    for(int i=1;i<20;i++){ int v=wl[i],j=i; while(j>0&&nsl[wl[j-1]]<nsl[v]){ wl[j]=wl[j-1]; j--; } wl[j]=v; }
    capS[20]=0; for(int i=19;i>=0;i--) capS[i]=capS[i+1]+nsl[wl[i]];
    canbig[20]=0; for(int i=19;i>=0;i--){ int w=wl[i]; memset(basis,0,sizeof basis); int rk=0; for(int x=0;x<nsl[w];x++){ int r=reduce(sl[w][x]); if(r){ basis[31-__builtin_clz(r)]=r; rk++; } } canbig[i]=canbig[i+1]||rk>=3; }
    memset(basis,0,sizeof basis); memset(bmask,0,sizeof bmask); defect=0; depm=0; ncl=0; d_struct=0; d_surv=0; d_found=0;
    rec(0,0);
    fprintf(stderr,"deriv %ld structures %ld stage1 %ld FOUND %ld calls %ld\n",deriv_idx,d_struct,d_surv,d_found,ncalls); if(d_found){ printf("deriv %ld : structures %ld, with pure + deliveries <= %d : %ld\n",deriv_idx,d_struct,BOUND,d_found); fflush(stdout); }
}
static void prod(int i){ if(i==12){ process(); return; } for(int c=0;c<nopt[i];c++){ choice[i]=c; prod(i+1); } }
int main(int argc,char**argv){
    if(argc<6){ fprintf(stderr,"usage\n"); return 2; }
    M=atol(argv[4]); RR=atol(argv[5]); if(argc>6) MAXD=atoi(argv[6]);
    long LIM=argc>7?atol(argv[7]):1000000000L; if(getenv("BOUND")) BOUND=atoi(getenv("BOUND")); if(getenv("SYM")) SYM=atoi(getenv("SYM"));
    hk=calloc(1u<<HB,sizeof(uint64_t)); hv=calloc(1u<<HB,1);
    memset(zindex,-1,sizeof zindex);
    for(int S=0;S<8;S++){ int r=0; for(int t=0;t<8;t++) if((t&S)==t) r|=1<<t; Zrow[S]=r; zindex[r]=S; }
    memset(S1g,12,sizeof S1g); memset(S2g,99,sizeof S2g);
    char line[4096]; FILE*f=fopen(argv[2],"r"); if(!f){ perror("single"); return 2; }
    while(fgets(line,sizeof line,f)){ int w,g; if(line[0]!='#'&&sscanf(line,"%d %d",&w,&g)==2) S1g[w]=g; } fclose(f);
    const char*pn[6]={"pA1","pA2","pB1","pB2","pC1","pC2"}; long npairs=0;
    for(int i=0;i<6;i++){ char path[1024]; snprintf(path,sizeof path,"%s/%s.txt",argv[3],pn[i]); f=fopen(path,"r"); if(!f){ perror(path); return 2; }
        while(fgets(line,sizeof line,f)){ int a,b,g; if(line[0]!='#'&&sscanf(line,"%d %d %d",&a,&b,&g)==3){ S2g[a][b]=g; S2g[b][a]=g; npairs++; } } fclose(f); }
    fprintf(stderr,"pairs read %ld\n",npairs);
    MINPATH=14-BOUND; if(MINPATH<3) MINPATH=3; nWL=0; for(int w=3;w<256;w++) if(__builtin_popcount(w)>1&&S1g[w]<=BOUND-1) WL[nWL++]=w;
    fprintf(stderr,"BOUND %d MINPATH %d deliverable forms %d\n",BOUND,MINPATH,nWL);
    f=fopen(argv[1],"r"); if(!f){ perror("sets"); return 2; }
    long nsets=0;
    while(fgets(line,sizeof line,f)){
        if(!strstr(line,"example")) continue;
        char*p=strchr(line,':'); int fs[16],nfm=0;
        for(int S=0;S<8;S++) if(__builtin_popcount(Zrow[S])>1) fs[nfm++]=Zrow[S];
        while((p=strchr(p,'['))){ p++; int m=0; for(int i=0;i<8;i++) if(p[i]=='1') m|=1<<i; int dup=0; for(int i=0;i<nfm;i++) if(fs[i]==m) dup=1; if(!dup) fs[nfm++]=m; }
        if(nfm!=12){ fprintf(stderr,"set with %d forms\n",nfm); continue; }
        for(int i=1;i<12;i++){ int v=fs[i],j=i; while(j>0&&fs[j-1]>v){fs[j]=fs[j-1];j--;} fs[j]=v; }
        if(SYM){ static const int P[6][3]={{0,1,2},{0,2,1},{1,0,2},{1,2,0},{2,0,1},{2,1,0}}; int least=1;
            for(int q=1;q<6&&least;q++){ int im[12];
                for(int i=0;i<12;i++){ int m=0; for(int t=0;t<8;t++) if((fs[i]>>t)&1){ int u=0; for(int c=0;c<3;c++) if((t>>c)&1) u|=1<<P[q][c]; m|=1<<u; } im[i]=m; }
                for(int i=1;i<12;i++){ int v=im[i],j=i; while(j>0&&im[j-1]>v){im[j]=im[j-1];j--;} im[j]=v; }
                for(int i=0;i<12;i++){ if(im[i]<fs[i]){ least=0; break; } if(im[i]>fs[i]) break; } }
            if(!least) continue; nsets_canon++; }
        memcpy(forms,fs,sizeof forms); nsets++;
        int wires[20]; for(int j=0;j<8;j++) wires[j]=1<<j; for(int i=0;i<12;i++) wires[8+i]=forms[i];
        int okset=1;
        for(int i=0;i<12;i++){ nopt[i]=0; for(int x=0;x<20;x++) for(int y=x+1;y<20;y++) if((wires[x]^wires[y])==forms[i]&&wires[x]!=forms[i]&&wires[y]!=forms[i]){ optU[i][nopt[i]]=wires[x]; optV[i][nopt[i]]=wires[y]; nopt[i]++; } if(!nopt[i]) okset=0; }
        if(okset) prod(0);
        if(deriv_idx>=LIM) break;
    }
    printf("TWO-ELEMENT FIELD, count (G). wire sets read %ld, derivations seen %ld, this run: index = %ld modulo %ld, MAXD = %d\n",nsets,deriv_idx,RR,M,MAXD);
    printf("groupings with 8 independent reaches visited (pruned: not all): %ld ; with 9 classes of rank 8 (ghost included) and a wire of >= MINPATH classes: %ld\n",st_all,st_struct);
    for(int k=1;k<=MAXD;k++) printf("delivery sets of size %d: (structure, set) passing the census %ld ; then the single-edge test %ld ; then the exact joint search (pure + deliveries <= %d) %ld\n",k,st_cens[k],st_surv[k],BOUND,st_s2[k]);
    printf("STRUCTURES (9 injections) with one delivery reaching pure + 1 <= %d : %ld   (10 would be a 31-gate candidate; 11 is a tie)\n",BOUND,st_found);
    printf("exact search calls: %ld (joint ones %ld) ; SYM = %d (1: only wire sets that are the least of their 6 images under permutations of the three address bits; such sets met: %ld)\n",ncalls,st_s2calls,SYM,nsets_canon);
    return 0;
}
