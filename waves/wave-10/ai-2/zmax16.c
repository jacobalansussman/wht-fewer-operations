/* ai-2: EXACT largest minor of the 16-point subset-sum matrix Z (Z[T][x] = 1 if x is a subset of T), every order, every
   row set and column set.  The 24 permutations of the 4 address bits act on rows and columns together and keep Z, so row
   sets are taken up to that symmetry (the smallest of the 24 images).  Determinants by Gaussian elimination in doubles with
   pivoting (entries 0/1, determinants are whole numbers far below 2^40; rounded), the winners re-checked in exact integers. */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
static int perm[24][16];
static long long bareiss(int m, long long A[16][16]){
    long long prev=1; int sign=1;
    for(int i=0;i<m;i++){
        int p=-1; for(int r=i;r<m;r++) if(A[r][i]){p=r;break;}
        if(p<0) return 0;
        if(p!=i){ for(int c=0;c<m;c++){long long t=A[i][c];A[i][c]=A[p][c];A[p][c]=t;} sign=-sign; }
        for(int r=i+1;r<m;r++) for(int c=i+1;c<m;c++) A[r][c]=(A[r][c]*A[i][i]-A[r][i]*A[i][c])/prev;
        prev=A[i][i];
    }
    return sign*A[m-1][m-1];
}
int main(void){
    int bits[4]={0,1,2,3}, np=0;
    for(int a=0;a<4;a++)for(int b=0;b<4;b++)for(int c=0;c<4;c++)for(int d=0;d<4;d++){
        if(a==b||a==c||a==d||b==c||b==d||c==d) continue;
        int pm[4]={a,b,c,d};
        for(int x=0;x<16;x++){int y=0; for(int i=0;i<4;i++) if(x>>i&1) y|=1<<pm[i]; perm[np][x]=y;}
        np++;
    }
    (void)bits;
    long long best[17]={0}; unsigned bestR[17]={0},bestC[17]={0}; unsigned long long count=0, reps=0;
    for(unsigned R=1;R<65536;R++){
        int canon=1;
        for(int p=1;p<24&&canon;p++){unsigned S=0; for(int x=0;x<16;x++) if(R>>x&1) S|=1u<<perm[p][x]; if(S<R) canon=0;}
        if(!canon) continue;
        reps++;
        int m=__builtin_popcount(R); int rows[16],nr=0; for(int x=0;x<16;x++) if(R>>x&1) rows[nr++]=x;
        unsigned C=(1u<<m)-1;
        while(C<65536){
            int cols[16],nc=0; for(int x=0;x<16;x++) if(C>>x&1) cols[nc++]=x;
            double A[16][16];
            for(int i=0;i<m;i++)for(int j=0;j<m;j++) A[i][j]=((cols[j]&rows[i])==cols[j])?1.0:0.0;
            double det=1.0;
            for(int i=0;i<m&&det!=0.0;i++){
                int p=i; double mx=fabs(A[i][i]);
                for(int r=i+1;r<m;r++) if(fabs(A[r][i])>mx){mx=fabs(A[r][i]);p=r;}
                if(mx<1e-9){det=0.0;break;}
                if(p!=i){for(int c=i;c<m;c++){double t=A[i][c];A[i][c]=A[p][c];A[p][c]=t;} det=-det;}
                det*=A[i][i];
                for(int r=i+1;r<m;r++){double f=A[r][i]/A[i][i]; if(f!=0.0) for(int c=i+1;c<m;c++) A[r][c]-=f*A[i][c];}
            }
            long long d=llround(fabs(det)); count++;
            if(d>best[m]){best[m]=d;bestR[m]=R;bestC[m]=C;}
            if(m==16) break;
            unsigned t=C|(C-1); C=(t+1)|(((~t&-~t)-1)>>(__builtin_ctz(C)+1));   /* next set with the same number of bits */
        }
    }
    printf("16 points: %llu row sets up to symmetry, %llu minors examined\n",reps,count);
    long long top=0;
    for(int m=1;m<=16;m++){
        long long A[16][16]; int rows[16],cols[16],nr=0,nc=0;
        for(int x=0;x<16;x++){ if(bestR[m]>>x&1) rows[nr++]=x; if(bestC[m]>>x&1) cols[nc++]=x; }
        for(int i=0;i<m;i++)for(int j=0;j<m;j++) A[i][j]=((cols[j]&rows[i])==cols[j]);
        long long e=bareiss(m,A); if(e<0)e=-e;
        printf("  order %2d: largest |minor| = %lld (exact recheck %lld) rows %04x cols %04x\n",m,best[m],e,bestR[m],bestC[m]);
        if(best[m]>top) top=best[m];
    }
    printf("largest minor of Z at 16 points, all orders: %lld\n",top);
    return 0;
}
