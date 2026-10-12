/* bfs16.c [ad-3]  16 points, exact, exhaustive.
   States: the 8008 sets of 6 addresses (a 16-bit mask = where the spectrum is -1).
   EXCHANGE (u, T): T a set that is unchanged by adding u; the permutation y -> y + u for y in T, y -> y elsewhere.
   Class c: T is a union of at most c flats, each unchanged by adding u.  Exchanges that are affine maps
   (T empty, everything, or a hyperplane) are free relabellings and are not counted: start and target classes are closed
   under affine maps, so the least number of counted exchanges is the breadth-first distance with only the counted ones.
   Output: the affine classes of 6-sets, for each its size, D (largest dimension of a flat inside the set or inside its
   complement), least number of flats whose signed sum is the indicator is NOT computed here; and the distance matrices. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define N 16
typedef uint32_t M;
static int popc(M x){return __builtin_popcount(x);}
static M shiftu(M m,int u){ M r=0; for(int y=0;y<N;y++) if(m>>y&1) r|=1u<<(y^u); return r;}
static M flats[400]; static int fdim[400]; static int nfl=0;
static int isflat(M m){ int c=popc(m); if(!c||(c&(c-1))) return 0; int a=__builtin_ctz(m);
  for(int x=0;x<N;x++) if(m>>x&1) for(int y=0;y<N;y++) if(m>>y&1){ if(!((m>>(x^y^a))&1)) return 0;} return 1;}
static M *moves[16]; static int nmoves[16];
static unsigned char seen[65536];
static void build_moves(int c){
  for(int u=1;u<N;u++){
    M L[400]; int nl=0;
    for(int i=0;i<nfl;i++) if(fdim[i]>=1 && fdim[i]<=2 && shiftu(flats[i],u)==flats[i]) L[nl++]=flats[i];
    /* flats of dimension 3 (hyperplanes) and 4 give affine maps; inside a union they can be removed up to an affine map */
    memset(seen,0,sizeof seen); free(moves[u]); moves[u]=malloc(sizeof(M)*70000); nmoves[u]=0;
    for(int i=0;i<nl;i++){ M a=L[i];
      if(!seen[a]){seen[a]=1; moves[u][nmoves[u]++]=a;}
      if(c>=2) for(int j=i+1;j<nl;j++){ M b=a|L[j];
        if(!seen[b]){seen[b]=1; moves[u][nmoves[u]++]=b;}
        if(c>=3) for(int l=j+1;l<nl;l++){ M d=b|L[l]; if(!seen[d]){seen[d]=1; moves[u][nmoves[u]++]=d;} } } }
    /* drop the affine ones */
    int w=0; for(int i=0;i<nmoves[u];i++){ M t=moves[u][i]; int aff = (t==0xFFFF) || (popc(t)==8 && isflat(t)); if(!aff) moves[u][w++]=t; }
    nmoves[u]=w;
  }
}
static M sh[16][65536];
static int dist[65536];
static M queue[9000];
static void bfs(const unsigned char *src){
  int qh=0,qt=0; for(int m=0;m<65536;m++){ dist[m]=-1; if(popc(m)==6 && src[m]){dist[m]=0; queue[qt++]=m;} }
  while(qh<qt){ M m=queue[qh++];
    for(int u=1;u<N;u++) for(int i=0;i<nmoves[u];i++){ M t=moves[u][i]; M r=(m&~t)|sh[u][m&t];
      if(dist[r]<0){dist[r]=dist[m]+1; queue[qt++]=r;} } }
}
static int par[65536];
static int find(int x){ while(par[x]!=x){par[x]=par[par[x]]; x=par[x];} return x;}
static M lin(M m,int i,int j){ /* y_i <- y_i + y_j */ M r=0; for(int y=0;y<N;y++) if(m>>y&1){ int z=y; if(y>>j&1) z^=1<<i; r|=1u<<z;} return r;}
static int isbent(M m){ for(int a=0;a<N;a++){ int s=0; for(int y=0;y<N;y++){ int v=(m>>y&1)^(__builtin_popcount(a&y)&1); s+= v?-1:1;} if(s!=4&&s!=-4) return 0;} return 1;}
static int Dval(M m){ int best=0; M comp=(~m)&0xFFFF; for(int i=0;i<nfl;i++){ if((flats[i]&~m)==0 || (flats[i]&~comp)==0) if(fdim[i]>best) best=fdim[i]; } return best;}
int main(void){
  for(M m=1;m<65536;m++) if(isflat(m)){ flats[nfl]=m; int c=popc(m),d=0; while((1<<d)<c) d++; fdim[nfl]=d; nfl++; }
  printf("flats of the 16-point address space: %d\n",nfl);
  for(int u=1;u<N;u++) for(M m=0;m<65536;m++) sh[u][m]=shiftu(m,u);
  /* affine classes of 6-sets */
  for(int m=0;m<65536;m++) par[m]=m;
  for(M m=0;m<65536;m++) if(popc(m)==6){
    for(int i=0;i<4;i++){ int r=find(sh[1<<i][m]), s=find(m); if(r!=s) par[r]=s; }
    for(int i=0;i<4;i++) for(int j=0;j<4;j++) if(i!=j){ int r=find(lin(m,i,j)), s=find(m); if(r!=s) par[r]=s; } }
  int cls[65536]; int ncls=0; int rep[64], csize[64];
  for(M m=0;m<65536;m++) cls[m]=-1;
  for(M m=0;m<65536;m++) if(popc(m)==6){ int r=find(m); if(cls[r]<0){cls[r]=ncls; rep[ncls]=m; csize[ncls]=0; ncls++;} cls[m]=cls[r]; csize[cls[m]]++; }
  /* start class: hyperplane minus a line inside it */
  int startc=-1, bentc[8], nb=0;
  for(int i=0;i<nfl;i++) if(fdim[i]==3) for(int j=0;j<nfl;j++) if(fdim[j]==1 && (flats[j]&~flats[i])==0){ startc=cls[flats[i]&~flats[j]]; }
  printf("affine classes of 6-sets: %d\n",ncls);
  printf("class  size  representative(points)  D  bent  start\n");
  for(int c=0;c<ncls;c++){ int b=isbent(rep[c]); if(b) bentc[nb++]=c;
    printf("  %2d  %5d  {",c,csize[c]); for(int y=0;y<N;y++) if(rep[c]>>y&1) printf("%d ",y);
    printf("}  D=%d  %s  %s\n",Dval(rep[c]), b?"BENT(quadric)":"", c==startc?"START(hyperplane minus line)":""); }
  for(int c=1;c<=3;c++){
    build_moves(c); long tot=0; for(int u=1;u<N;u++) tot+=nmoves[u];
    printf("\n== class c=%d : %ld counted exchanges (distinct (u,T), T a union of at most %d flats unchanged by u, not affine)\n",c,tot,c);
    { /* the D-lemma on every 6-set and every counted exchange of this class: D falls by at most c */
      static signed char Dt[65536]; long viol=0; int maxdrop=0; long drops[5]={0,0,0,0,0};
      for(M m=0;m<65536;m++) if(popc(m)==6) Dt[m]=Dval(m);
      for(M m=0;m<65536;m++) if(popc(m)==6) for(int u=1;u<N;u++) for(int i=0;i<nmoves[u];i++){ M t=moves[u][i]; M r=(m&~t)|sh[u][m&t];
        int dr=Dt[m]-Dt[r]; if(dr>c) viol++; if(dr>maxdrop) maxdrop=dr; if(dr>=0&&dr<5) drops[dr]++; }
      printf("D-lemma check (D falls by at most c per exchange) on all 8008 sets x all exchanges: violations %ld ; largest fall seen %d ; falls of 0,1,2: %ld %ld %ld\n",viol,maxdrop,drops[0],drops[1],drops[2]); }
    printf("distance matrix between affine classes (rows: from, columns: to):\n     ");
    for(int b=0;b<ncls;b++) printf("%3d",b); printf("\n");
    for(int a=0;a<ncls;a++){ static unsigned char src[65536]; for(int m=0;m<65536;m++) src[m]=(cls[m]==a);
      bfs(src); int row[64]; for(int b=0;b<ncls;b++) row[b]=99;
      for(M m=0;m<65536;m++) if(popc(m)==6 && dist[m]>=0 && dist[m]<row[cls[m]]) row[cls[m]]=dist[m];
      /* consistency: every member of a class has the same distance */
      for(M m=0;m<65536;m++) if(popc(m)==6 && dist[m]!=row[cls[m]]) {printf("INCONSISTENT\n"); return 1;}
      printf("  %2d:",a); for(int b=0;b<ncls;b++) printf("%3d",row[b]); printf("\n");
      if(a==startc){ int best=99; for(int i=0;i<nb;i++) if(row[bentc[i]]<best) best=row[bentc[i]]; printf("     ^ start; j(4,%d) = %d\n",c,best); }
    }
  }
  return 0;
}
