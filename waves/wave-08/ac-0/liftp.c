// lift3.c (ac-0): the wiring of ab-0's 15-gate circuit, every gate with every coefficient pair in the field with p
// elements up to scaling (u, v, u+c*v for c=1..p-1: p+1 choices per gate, zero coefficients included), exhaustive:
// does any choice produce all 8 rows of the 16-point block (each up to a non-zero factor) somewhere among the 15 gates?
// p = 3: 4^15 = 1,073,741,824 choices. This is a statement in the field with p elements, not over the rationals.
// liftp.c = lift3.c plus a sound cut: only g12,g14,g15,g17,g18,g19,g20,g21,g22 can ever hold a row (supports, replay.out),
// so a branch is dropped when rows so far + candidate gates still to come < 8. "most rows" is then not reported.
// usage: liftp <p>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int p, W[23][2]={{0,0}}; static int vec[23][8]; static int rowid[1<<16]; static unsigned long long leaves, hits, best;
static int T[8][8];
static int key(const int*v){int k=0;for(int j=0;j<8;j++)k=k*p+v[j];return k;}
static int which(const int*v){ // row index if v is a non-zero multiple of a row, else -1
    for(int i=0;i<8;i++){ int c=0,ok=1; for(int j=0;j<8&&ok;j++){ if(T[i][j]){ if(!v[j]) ok=0; else if(!c) c=v[j]; else if(v[j]!=c) ok=0; } else if(v[j]) ok=0; } if(ok) return i; }
    return -1;
}
static int cand[24]={0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,0,1,1,1,1,1,1,0}; static int left[24];
static void rec(int g,int mask){
    if(__builtin_popcount(mask)+left[g]<8) return;
    if(g==23){ leaves++; int n=__builtin_popcount(mask); if((unsigned)n>best) best=n; if(mask==255) hits++; return; }
    int u=W[g][0], v=W[g][1];
    for(int ch=0; ch<p+1; ch++){
        for(int j=0;j<8;j++){ int x; if(ch==0) x=vec[u][j]; else if(ch==1) x=vec[v][j]; else x=(vec[u][j]+(ch-1)*vec[v][j])%p; vec[g][j]=x; }
        int w=which(vec[g]);
        rec(g+1, w>=0? mask|(1<<w) : mask);
    }
}
int main(int argc,char**argv){
    p=atoi(argv[1]);
    int ev[8],od[8],ne=0,no=0; for(int x=0;x<16;x++){ if(__builtin_popcount(x)&1) od[no++]=x; else ev[ne++]=x; }
    for(int i=0;i<8;i++) for(int j=0;j<8;j++) T[i][j]=(__builtin_popcount(od[i]^ev[j])==1);
    int w[15][2]={{1,0},{7,6},{7,5},{10,4},{11,1},{5,3},{13,8},{13,9},{4,2},{16,8},{16,9},{18,12},{19,14},{19,15},{19,17}};
    for(int i=0;i<15;i++){W[8+i][0]=w[i][0];W[8+i][1]=w[i][1];}
    for(int j=0;j<8;j++) for(int i=0;i<8;i++) vec[j][i]=(i==j);
    for(int g=22;g>=0;g--) left[g]=left[g+1]+cand[g];
    rec(8,0);
    printf("p=%d: complete coefficient choices reached %llu ; choices giving all 8 rows: %llu   (with the support cut)\n",p,leaves,hits);
    return 0;
}
