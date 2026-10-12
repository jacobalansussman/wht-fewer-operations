/* k6.c [ad-3]  64 points, exact (whole 64-bit masks; a mask = the set of addresses where the spectrum is -1).
   EXCHANGE (u, T): T unchanged by adding u; the permutation y -> y + u on T, identity elsewhere.
   Start A0 = {y : y0 = 0} minus {0,2,4,6}  (a hyperplane minus a subspace of 2 bits), 28 points.
   Target: any bent function of degree 2 with 28 ones (a non-degenerate quadric).
   Stabiliser of A0 has three orbits on directions u: inside W = <e1,e2> (rep 2), inside the hyperplane but not W (rep 8),
   outside the hyperplane (rep 1).  The FIRST exchange may therefore be taken with u in {2, 8, 1}; later ones are free.
   NEAR(g): is g ONE exchange (ANY set T) from a quadric?  Criterion [derived in ad-3.md]: g = Q after the exchange (u,T)
   forces g(y) + g(y+u) = l(y), an affine form (l = Q(y)+Q(y+u)); g = Q where l = 0; on l = 1, Q(y+w) = g(y) + alpha(y)
   for a fixed w with l(w) != l(0) and an affine alpha with alpha(y+u) = alpha(y)+1.  All candidates are tried and every hit
   is replayed by applying the exchange.
   usage: k6 A            c=1: one exchange, then two exchanges (both of class 1), exhaustive
          k6 B c [u1]     first exchange of class c (u in the three reps, or only rep number u1), second exchange ANY set T
          k6 C [u1]       two exchanges of class 1, third exchange ANY set T                                              */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef uint64_t M;
static M LO[6];
static inline M swapb(M m,int b){ return ((m&LO[b])<<(1<<b)) | ((m>>(1<<b))&LO[b]); }
static inline M shiftu(M m,int u){ for(int b=0;b<6;b++) if(u>>b&1) m=swapb(m,b); return m; }
static inline int popc(M m){ return __builtin_popcountll(m); }
static M DEG3; static M HYP[64];
static int is_bq(M m, int *deg){
  if(popc(m)!=28) return 0;
  for(int b=0;b<6;b++) if(popc(m^swapb(m,b))!=32) return 0;
  int a[64]; for(int y=0;y<64;y++) a[y]=(m>>y&1)?-1:1;
  for(int h=1;h<64;h<<=1) for(int i=0;i<64;i+=2*h) for(int j=i;j<i+h;j++){ int p=a[j],q=a[j+h]; a[j]=p+q; a[j+h]=p-q; }
  for(int y=0;y<64;y++) if(a[y]!=8&&a[y]!=-8) return 0;
  M anf=m; for(int b=0;b<6;b++) anf^=(anf&LO[b])<<(1<<b);
  int d=0; for(int y=0;y<64;y++) if(anf>>y&1){ int w=__builtin_popcount(y); if(w>d) d=w; }
  if(deg) *deg=d;
  return (anf&DEG3)?2:1;   /* 1 = bent of degree 2 (a quadric); 2 = bent of higher degree */
}
/* flats */
static M sub[3000]; static int subdim[3000]; static int nsub=0;
static M *flat; static int *flatdim; static int nflat=0;
static M *L[64]; static int nL[64];
static int cmpM(const void*a,const void*b){ M x=*(const M*)a,y=*(const M*)b; return x<y?-1:x>y; }
static void build(void){
  for(int b=0;b<6;b++){ M m=0; for(int y=0;y<64;y++) if(!(y>>b&1)) m|=1ULL<<y; LO[b]=m; }
  DEG3=0; for(int y=0;y<64;y++) if(__builtin_popcount(y)>=3) DEG3|=1ULL<<y;
  for(int a=1;a<64;a++){ M m=0; for(int y=0;y<64;y++) if(!(__builtin_popcount(a&y)&1)) m|=1ULL<<y; HYP[a]=m; }
  sub[0]=1; subdim[0]=0; nsub=1;
  for(int i=0;i<nsub;i++) for(int v=1;v<64;v++) if(!(sub[i]>>v&1)){ M s=sub[i]|shiftu(sub[i],v); int f=0;
      for(int j=0;j<nsub;j++) if(sub[j]==s){f=1;break;} if(!f){ sub[nsub]=s; subdim[nsub]=subdim[i]+1; nsub++; } }
  flat=malloc(sizeof(M)*30000); flatdim=malloc(sizeof(int)*30000);
  for(int i=0;i<nsub;i++){ M cov=0; for(int a=0;a<64;a++) if(!(cov>>a&1)){ M f=shiftu(sub[i],a); cov|=f; flat[nflat]=f; flatdim[nflat]=subdim[i]; nflat++; } }
  for(int u=1;u<64;u++){ L[u]=malloc(sizeof(M)*3000); nL[u]=0;
    for(int i=0;i<nflat;i++) if(flatdim[i]>=1&&flatdim[i]<=4&&shiftu(flat[i],u)==flat[i]) L[u][nL[u]++]=flat[i]; }
}
static inline M apply(M g,M gs,M T){ return (g&~T)|(gs&T); }   /* gs = g shifted by u, T unchanged by u */
/* least number (1,2,3, or 9) of flats unchanged by u whose union is t */
static int cover(M t,int u){
  M in[3000]; int n=0; for(int i=0;i<nL[u];i++) if((L[u][i]&~t)==0) in[n++]=L[u][i];
  /* also hyperplane-size and whole flats do not occur inside a set of at most 32 points other than the half itself */
  for(int i=0;i<n;i++) if(in[i]==t) return 1;
  for(int i=0;i<nflat;i++) if(flat[i]==t && shiftu(t,u)==t) return 1;
  for(int i=0;i<n;i++) for(int j=i+1;j<n;j++) if((in[i]|in[j])==t) return 2;
  for(int i=0;i<n;i++) for(int j=i+1;j<n;j++){ M r=t&~(in[i]|in[j]); if(!r) continue; for(int l=j+1;l<n;l++) if((in[l]&r)==r) return 3; }
  return 9;
}
static long near_calls=0, near_hits=0; static int best_cover=99; static M best_g, best_Q, best_t; static int best_u; static long hit_bent_hi=0;
static int cover_hist[10];
/* returns 1 if g is one exchange (any T) from a quadric; records the simplest T found */
static int near(M g){
  near_calls++; int found=0; M gs=g; int u=0;
  for(int i=1;i<64;i++){ int b=__builtin_ctz(i); gs=swapb(gs,b); u^=1<<b;        /* Gray order over u */
    M d=g^gs; if(popc(d)!=32) continue;
    int a=0; for(int x=1;x<64;x++) if(d==HYP[x]||d==~HYP[x]){a=x;break;} if(!a) continue;
    M P1=d, P0=~d; int w=0; for(int b2=0;b2<6;b2++) if(a>>b2&1){w=1<<b2;break;}
    for(int a2=0;a2<64;a2++) if(__builtin_popcount(a2&u)&1) for(int c2=0;c2<2;c2++){
      M AL=a2?(c2?HYP[a2]:~HYP[a2]):0; if(!a2) continue;
      M Q=(g&P0)|shiftu((g^AL)&P0,w);
      int r=is_bq(Q,NULL); if(!r) continue;
      M t=(g^Q)&P1; if(shiftu(t,u)!=t) continue;
      M back=apply(g,gs,t); if(back!=Q) continue;                                   /* replay of the exchange */
      if(r==2){ hit_bent_hi++; continue; }
      found=1; int cv=cover(t,u); cover_hist[cv]++;
      if(cv<best_cover){ best_cover=cv; best_g=g; best_Q=Q; best_t=t; best_u=u; } } }
  if(found) near_hits++;
  return found;
}
static void pm(const char*s,M m){ printf("%s 0x%016llx (%d points)\n",s,(unsigned long long)m,popc(m)); }
int main(int argc,char**argv){
  build();
  printf("subspaces %d, flats %d, flats of dimension 1 to 4 unchanged by a given u: %d\n",nsub,nflat,nL[1]);
  M A0=0; for(int y=0;y<64;y++) if(!(y&1) && y>=8) A0|=1ULL<<y;
  { M Qm=0; for(int y=0;y<64;y++){ int q=((y&1)&(y>>1&1))^((y>>2&1)&(y>>3&1))^((y>>4&1)&(y>>5&1)); if(q) Qm|=1ULL<<y; }
    printf("control: start has %d points, is_bq(start)=%d ; the quadric y0y1+y2y3+y4y5 has %d points, is_bq=%d\n",popc(A0),is_bq(A0,NULL),popc(Qm),is_bq(Qm,NULL)); }
  int reps[3]={2,8,1}; const char*repname[3]={"u in W","u in the hyperplane, not in W","u outside the hyperplane"};
  char mode=argc>1?argv[1][0]:'A';
  if(mode=='A'){
    long h1=0; for(int u=1;u<64;u++){ M gs=shiftu(A0,u); for(int i=0;i<nL[u];i++){ if(is_bq(apply(A0,gs,L[u][i]),NULL)) h1++; } }
    printf("A. class 1, ONE exchange (all 63 directions, %d flats each): quadrics reached %ld\n",nL[1],h1);
    long h2=0,h2hi=0,tried=0; M ex1=0,ex2=0,exg=0,exh=0; int exu1=0,exu2=0;
    for(int r=0;r<3;r++){ int u1=reps[r]; M s0=shiftu(A0,u1); long hr=0;
      for(int i=0;i<nL[u1];i++){ M g=apply(A0,s0,L[u1][i]);
        for(int u2=1;u2<64;u2++){ M gs=shiftu(g,u2); M*Lu=L[u2]; int n=nL[u2];
          for(int j=0;j<n;j++){ M h=apply(g,gs,Lu[j]); tried++;
            if(popc(h^swapb(h,0))!=32) continue;
            int rr=is_bq(h,NULL); if(rr==1){ h2++; hr++; if(!exh){exh=h;exg=g;ex1=L[u1][i];ex2=Lu[j];exu1=u1;exu2=u2;} } else if(rr==2) h2hi++; } } }
      printf("   first exchange with %s: quadrics reached after the second %ld\n",repname[r],hr); }
    printf("A. class 1, TWO exchanges: %ld products tried, quadrics reached %ld, bent of higher degree reached %ld\n",tried,h2,h2hi);
    if(exh){ printf("   example: u1=%d ",exu1); pm("T1",ex1); printf("            u2=%d ",exu2); pm("T2",ex2); pm("            after one",exg); pm("            after two",exh); }
  } else if(mode=='B'){
    int c=atoi(argv[2]); int only=argc>3?atoi(argv[3]):-1; int ilo=argc>4?atoi(argv[4]):0, ihi=argc>5?atoi(argv[5]):1000000;   /* optional: only first flats with index in [ilo, ihi) */
    for(int r=0;r<3;r++){ if(only>=0&&only!=r) continue; int u1=reps[r]; M s0=shiftu(A0,u1); M*Lu=L[u1]; int n=nL[u1]; long cnt=0,hits=0; long before=near_hits;
      for(int i=ilo;i<n&&i<ihi;i++){ M T1=Lu[i];
        if(c==1){ cnt++; hits+=near(apply(A0,s0,T1)); continue; }
        for(int j=i+1;j<n;j++){ M T2=T1|Lu[j];
          if(c==2){ cnt++; hits+=near(apply(A0,s0,T2)); continue; }
          for(int l=j+1;l<n;l++){ cnt++; hits+=near(apply(A0,s0,T2|Lu[l])); } } }
      if(argc>4) printf("   (only first flats with index %d to %d of %d)\n",ilo,ihi<n?ihi:n,n);
      printf("B. first exchange of class %d with %s: %ld sets T tried; of the results, one exchange (ANY T) from a quadric: %ld\n",c,repname[r],cnt,near_hits-before); fflush(stdout); }
    printf("   hits where the quadric side was bent of degree above 2 (not counted): %ld\n",hit_bent_hi);
    printf("   second exchanges found, by least number of flats covering T (1,2,3, 9 = more): %d %d %d %d\n",cover_hist[1],cover_hist[2],cover_hist[3],cover_hist[9]);
    if(best_cover<99){ printf("   simplest second exchange: u=%d, T is a union of %d flat(s)\n",best_u,best_cover); pm("   before it",best_g); pm("   T",best_t); pm("   quadric",best_Q); }
  } else if(mode=='C'){
    int only=argc>2?atoi(argv[2]):-1;
    for(int r=0;r<3;r++){ if(only>=0&&only!=r) continue; int u1=reps[r]; M s0=shiftu(A0,u1); long cnt=0; long before=near_hits;
      for(int i=0;i<nL[u1];i++){ M g=apply(A0,s0,L[u1][i]);
        for(int u2=1;u2<64;u2++){ M gs=shiftu(g,u2); M*Lu=L[u2]; int n=nL[u2];
          for(int j=0;j<n;j++){ cnt++; near(apply(g,gs,Lu[j])); } } }
      printf("C. two exchanges of class 1 (first with %s): %ld products; one exchange (ANY T) from a quadric: %ld\n",repname[r],cnt,near_hits-before); fflush(stdout); }
    printf("   third exchanges found, by least number of flats covering T (1,2,3, 9 = more): %d %d %d %d\n",cover_hist[1],cover_hist[2],cover_hist[3],cover_hist[9]);
    if(best_cover<99){ printf("   simplest third exchange: u=%d, T is a union of %d flat(s)\n",best_u,best_cover); pm("   before it",best_g); pm("   T",best_t); pm("   quadric",best_Q); }
  } else if(mode=='P'){   /* positive controls: plant exchanges on the quadric and ask the tests to find them */
    M Qm=0; for(int y=0;y<64;y++){ int q=((y&1)&(y>>1&1))^((y>>2&1)&(y>>3&1))^((y>>4&1)&(y>>5&1)); if(q) Qm|=1ULL<<y; }
    unsigned long long s=88172645463325252ULL; 
    #define RND (s^=s<<13,s^=s>>7,s^=s<<17,s)
    int ok1=0,ok2=0,tot=200, okc=0;
    for(int it=0;it<tot;it++){ int u=1+RND%63; M T=L[u][RND%nL[u]]; M g=apply(Qm,shiftu(Qm,u),T);
      if(g==Qm||is_bq(g,NULL)==1){ it--; continue; }
      long b=near_hits; best_cover=99; near(g); if(near_hits>b) ok1++; if(best_cover==1) okc++;
      /* arbitrary T unchanged by u: a random set of pairs */
      M R=RND; R|=shiftu(R,u); M g2=apply(Qm,shiftu(Qm,u),R); b=near_hits; near(g2); if(near_hits>b||is_bq(g2,NULL)==1) ok2++; }
    printf("P. control of NEAR: %d of %d planted single-flat exchanges recognised (with a one-flat T recovered: %d); %d of %d planted exchanges on random sets recognised\n",ok1,tot,okc,ok2,tot);
    /* control of the two-step search: plant two single-flat exchanges, then search two steps exhaustively from the planted set */
    int found=0, trials=3;
    for(int it=0;it<trials;it++){ int u1=1+RND%63,u2=1+RND%63; M T1=L[u1][RND%nL[u1]],T2=L[u2][RND%nL[u2]];
      M g1=apply(Qm,shiftu(Qm,u1),T1); M g2=apply(g1,shiftu(g1,u2),T2); int hit=0;
      for(int a=1;a<64&&!hit;a++){ M sa=shiftu(g2,a); for(int i=0;i<nL[a]&&!hit;i++){ M g=apply(g2,sa,L[a][i]);
          for(int b2=1;b2<64&&!hit;b2++){ M gs=shiftu(g,b2); M*Lu=L[b2]; int n=nL[b2];
            for(int j=0;j<n;j++){ M h=apply(g,gs,Lu[j]); if(popc(h^swapb(h,0))!=32) continue; if(is_bq(h,NULL)==1){hit=1;break;} } } } }
      found+=hit; }
    printf("P. control of the two-step search: %d of %d planted two-exchange sets brought back to a quadric\n",found,trials);
  } else if(mode=='S'){   /* UPPER bound for j(6,1): beam search with single-flat exchanges, score = sum over v != 0 of r(v)^2,
                             r(v) = 64 - 2 #{y : g(y) != g(y+v)}  (0 exactly for bent patterns).  A search, not a proof of minimality.
                             The path found is printed and replayed from the start. */
    int Bw=argc>2?atoi(argv[2]):200; int maxd=argc>3?atoi(argv[3]):10; int pw=argc>4?atoi(argv[4]):2;   /* score = sum of |r(v)|^pw, pw = 1, 2 or 4 */
    M *cur=malloc(sizeof(M)*Bw), *nxt=malloc(sizeof(M)*Bw); long *ns=malloc(sizeof(long)*Bw); int ncur=1; cur[0]=A0; int done=0;
    int *par[16],*mu[16],*mi[16]; for(int d=0;d<16;d++){ par[d]=malloc(sizeof(int)*Bw); mu[d]=malloc(sizeof(int)*Bw); mi[d]=malloc(sizeof(int)*Bw); }
    for(int d=1;d<=maxd&&!done;d++){ int nn=0; long worst=-1; int wi=-1;
      for(int c0=0;c0<ncur&&!done;c0++){ M g0=cur[c0];
        for(int u=1;u<64&&!done;u++){ M s0=shiftu(g0,u); M*Lu=L[u]; int n=nL[u];
          for(int i=0;i<n;i++){ M g=apply(g0,s0,Lu[i]); if(g==g0) continue;
            long sc=0; M gs=g; for(int v=1;v<64;v++){ gs=swapb(gs,__builtin_ctz(v)); long r=64-2*popc(g^gs); if(r<0) r=-r; sc+=(pw==1?r:(pw==4?r*r*r*r:r*r)); if(nn==Bw&&sc>=worst) break; }
            if(nn==Bw&&sc>=worst) continue;
            if(sc==0){ int rr=is_bq(g,NULL); if(rr==1){ printf("S. beam %d: a quadric reached after %d single-flat exchanges: ",Bw,d); pm("",g);
                int pu[16]; M pT[16]; pu[d]=u; pT[d]=Lu[i]; int q=c0; for(int e=d-1;e>=1;e--){ pu[e]=mu[e][q]; pT[e]=L[mu[e][q]][mi[e][q]]; q=par[e][q]; }
                M h=A0; for(int e=1;e<=d;e++){ h=apply(h,shiftu(h,pu[e]),pT[e]); printf("     exchange %d: u=%2d on the flat ",e,pu[e]); pm("",pT[e]); pm("        gives",h); }
                printf("     replay from the start ends in the same set: %s ; it is a quadric: %s\n",h==g?"yes":"NO",is_bq(h,NULL)==1?"yes":"NO"); done=1; break; } }
            int dup=0; for(int q=0;q<nn;q++) if(nxt[q]==g){dup=1;break;} if(dup) continue;
            int slot; if(nn<Bw){ slot=nn++; } else slot=wi;
            nxt[slot]=g; ns[slot]=sc; par[d][slot]=c0; mu[d][slot]=u; mi[d][slot]=i;
            if(nn==Bw){ worst=-1; for(int q=0;q<nn;q++) if(ns[q]>worst){worst=ns[q];wi=q;} } } } }
      if(!done){ long best=1L<<60; for(int q=0;q<nn;q++) if(ns[q]<best) best=ns[q]; printf("S. depth %d: beam holds %d sets, least score %ld\n",d,nn,best); fflush(stdout);
        M*t=cur; cur=nxt; nxt=t; ncur=nn; } }
    if(!done) printf("S. beam %d: no quadric within %d exchanges (a search; says nothing about existence)\n",Bw,maxd);
  }
  return 0;
}
