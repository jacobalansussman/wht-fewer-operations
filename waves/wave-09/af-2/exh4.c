// af-2: own exhaustive check at 16 points. Is g = (-1)^(z1 z2 + z3 z4) a rational combination of 2 or 3 signed flats?
// Whole-number Gram determinants. mode 0: target g. mode 1 (control): a target that IS 3 flats. mode 2 (control): 2 flats.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N 16
static int F[4096][N]; static unsigned S[4096]; static int nf=0; static int isun[4096];
static int par(unsigned x){return __builtin_popcount(x)&1;}
static void addflat(int *v){
  int s=0; for(int z=0;z<N;z++) if(v[z]){s=v[z];break;}
  int w[N]; unsigned m=0; int un=1; for(int z=0;z<N;z++){w[z]=v[z]*s; if(w[z]) m|=1u<<z; if(w[z]<0) un=0;}
  for(int i=0;i<nf;i++) if(S[i]==m && !memcmp(F[i],w,sizeof w)) return;
  memcpy(F[nf],w,sizeof w); S[nf]=m; isun[nf]=un; nf++;
}
static long det3(long a[3][3]){return a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])-a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])+a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]);}
static long det4(long a[4][4]){long d=0; for(int c=0;c<4;c++){long m[3][3]; for(int i=1;i<4;i++){int cc=0; for(int j=0;j<4;j++){ if(j==c) continue; m[i-1][cc++]=a[i][j];}} d+=((c&1)?-1:1)*a[0][c]*det3(m);} return d;}
int main(int argc,char**argv){
  int mode=argc>1?atoi(argv[1]):0; int nsub=0;
  for(unsigned m=1;m<65536;m+=2){ int ok=1;
    for(int a=0;a<N&&ok;a++) if(m>>a&1) for(int b=0;b<N;b++) if((m>>b&1)&&!(m>>(a^b)&1)){ok=0;break;}
    if(!ok) continue; nsub++;
    for(int a=0;a<N;a++) for(int b=0;b<N;b++){ int v[N]; for(int z=0;z<N;z++) v[z]=(m>>(z^a)&1)?(par(b&z)?-1:1):0; addflat(v);} }
  int g[N];
  for(int z=0;z<N;z++){ int z1=z&1,z2=z>>1&1,z3=z>>2&1,z4=z>>3&1;
    if(mode==0) g[z]=((z1&z2)^(z3&z4))?-1:1;
    else if(mode==1) g[z]=1-2*(z1&z2)-2*(z3&z4);
    else g[z]=1-2*(z1&z2&z3&z4); }
  static long G[1100][1100]; long gg=0, Gg[1100];
  for(int i=0;i<nf;i++){ for(int j=0;j<nf;j++){long d=0; for(int z=0;z<N;z++) d+=F[i][z]*F[j][z]; G[i][j]=d;} long d=0; for(int z=0;z<N;z++) d+=F[i][z]*g[z]; Gg[i]=d;}
  for(int z=0;z<N;z++) gg+=g[z]*g[z];
  long single=0,pairs=0,pairhit=0,cov=0,dep=0,hit=0,hitun=0;
  for(int i=0;i<nf;i++){ long d=G[i][i]*gg-Gg[i]*Gg[i]; if(d==0) single++; }
  for(int i=0;i<nf;i++) for(int j=i+1;j<nf;j++){ pairs++; long a[3][3]={{G[i][i],G[i][j],Gg[i]},{G[j][i],G[j][j],Gg[j]},{Gg[i],Gg[j],gg}}; if(det3(a)==0) pairhit++; }
  for(int i=0;i<nf;i++) for(int j=i+1;j<nf;j++){ unsigned u=S[i]|S[j]; for(int l=j+1;l<nf;l++){ if((u|S[l])!=0xFFFFu) continue; cov++;
     long b[3][3]={{G[i][i],G[i][j],G[i][l]},{G[j][i],G[j][j],G[j][l]},{G[l][i],G[l][j],G[l][l]}};
     if(det3(b)==0){dep++; continue;}
     long a[4][4]={{G[i][i],G[i][j],G[i][l],Gg[i]},{G[j][i],G[j][j],G[j][l],Gg[j]},{G[l][i],G[l][j],G[l][l],Gg[l]},{Gg[i],Gg[j],Gg[l],gg}};
     if(det4(a)==0){hit++; if(isun[i]&&isun[j]&&isun[l]) hitun++;} } }
  printf("mode %d: subspaces %d, signed flats up to a factor %d\n",mode,nsub,nf);
  printf("  target a multiple of one flat: %ld ; pairs %ld, pairs spanning the target: %ld\n",single,pairs,pairhit);
  printf("  covering triples %ld (linearly dependent triples among them %ld, covered by the pair test) ; independent triples spanning the target: %ld (unsigned: %ld)\n",cov,dep,hit,hitun);
  return 0; }
