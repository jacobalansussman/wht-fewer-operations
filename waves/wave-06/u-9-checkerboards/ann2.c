// u-9 checkerboards: annealer over the two orders of a 0/1 picture, counting ODD second differences only (corners modulo 2).
// mode 0: Z whole-number corners (as u-0's ann.c, for a check against 13, 30, 80)
// mode 1: Z modulo 2 (Sierpinski matrix): odd corners; checkerboards (second difference +-2) are free
// mode 2: B[y][x] = parity of common ones (H = J - 2B): odd corners of B = cells of value 2 of H; value-4 cells free
// mode 3: B2[y][x] = C(common ones, 2) modulo 2 (the second binary digit layer of H)
// cost is a sum over neighbouring rows: number of places where (row a XOR row a+1) changes along the column order, zero appended.
// usage: ann2 mode k iters restarts seed T0 T1
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
#define MAXN 512
static int N,k,mode;
static signed char Zm[MAXN+1][MAXN+1];
static int rows[MAXN+1], cols[MAXN+1], brow[MAXN+1], bcol[MAXN+1];
static uint64_t s[2];
static inline uint64_t rnd(void){uint64_t s1=s[0],s0=s[1];uint64_t r=s0+s1;s[0]=s0;s1^=s1<<23;s[1]=s1^s0^(s1>>17)^(s0>>26);return r;}
static inline double urnd(void){return (rnd()>>11)*(1.0/9007199254740992.0);}
static inline int rcost(int S,int S2){int prev=0,c=0;const signed char*p=Zm[S],*q=Zm[S2];
  if(mode==0){for(int b=N-1;b>=0;b--){int t=cols[b];int d=p[t]-q[t];c+=(d!=prev);prev=d;}}
  else {for(int b=N-1;b>=0;b--){int t=cols[b];int d=p[t]^q[t];c+=(d!=prev);prev=d;}}
  return c;}
static inline int ccost(int T,int T2){int prev=0,c=0;
  if(mode==0){for(int a=N-1;a>=0;a--){const signed char*p=Zm[rows[a]];int d=p[T]-p[T2];c+=(d!=prev);prev=d;}}
  else {for(int a=N-1;a>=0;a--){const signed char*p=Zm[rows[a]];int d=p[T]^p[T2];c+=(d!=prev);prev=d;}}
  return c;}
static inline int jc(int which,int q){ if(q<0) return 0; return which? ccost(cols[q],cols[q+1]) : rcost(rows[q],rows[q+1]); }
static int total(void){int c=0;for(int a=0;a<N;a++)c+=rcost(rows[a],rows[a+1]);return c;}
static int totalc(void){int c=0;for(int b=0;b<N;b++)c+=ccost(cols[b],cols[b+1]);return c;}
static void rev(int*arr,int i,int j){while(i<j){int t=arr[i];arr[i]=arr[j];arr[j]=t;i++;j--;}}
static void rot(int*arr,int i,int m,int p){rev(arr,i,m);rev(arr,m+1,p);rev(arr,i,p);}
int main(int argc,char**argv){
  mode=atoi(argv[1]);k=atoi(argv[2]);N=1<<k;long iters=atol(argv[3]);int restarts=atoi(argv[4]);uint64_t seed=strtoull(argv[5],0,10);
  double T0=atof(argv[6]),T1=atof(argv[7]);
  for(int S=0;S<=N;S++)for(int T=0;T<=N;T++){int v=0;if(S<N&&T<N){int m=__builtin_popcount(S&T);
     if(mode<=1)v=((S&T)==T);else if(mode==2)v=m&1;else v=(m*(m-1)/2)&1;}Zm[S][T]=v;}
  int gbest=1<<30;
  for(int r=0;r<restarts;r++){
    s[0]=seed*0x9E3779B97F4A7C15ULL+r*7919+1;s[1]=(seed+r+1)*0xBF58476D1CE4E5B9ULL+3;for(int i=0;i<20;i++)rnd();
    for(int i=0;i<N;i++){rows[i]=i;cols[i]=i;}
    for(int i=N-1;i>0;i--){int j=rnd()%(i+1);int t=rows[i];rows[i]=rows[j];rows[j]=t;j=rnd()%(i+1);t=cols[i];cols[i]=cols[j];cols[j]=t;}
    rows[N]=N;cols[N]=N;
    int cur=total(),best=cur;memcpy(brow,rows,sizeof(rows));memcpy(bcol,cols,sizeof(cols));
    double lr=log(T1/T0);
    for(long it=0;it<iters;it++){
      double T=T0*exp(lr*(double)it/iters);
      int which=rnd()&1;int*arr=which?cols:rows;int mv=rnd()%3;
      int i=rnd()%N,j=rnd()%N;if(i==j)continue;if(i>j){int t=i;i=j;j=t;}
      int oldc,newc;
      if(mv==0){oldc=jc(which,i-1)+jc(which,j);rev(arr,i,j);newc=jc(which,i-1)+jc(which,j);
        int d=newc-oldc;if(d<=0||urnd()<exp(-d/T)){cur+=d;}else rev(arr,i,j);
      } else if(mv==1){int m=i+rnd()%(j-i);
        oldc=jc(which,i-1)+jc(which,m)+jc(which,j);rot(arr,i,m,j);int nm=i+(j-m)-1;newc=jc(which,i-1)+jc(which,nm)+jc(which,j);
        int d=newc-oldc;if(d<=0||urnd()<exp(-d/T)){cur+=d;}else rot(arr,i,nm,j);
      } else {int q[4]={i-1,i,j-1,j};int nq=4;if(j==i+1){q[2]=j;nq=3;}
        oldc=0;for(int z=0;z<nq;z++)oldc+=jc(which,q[z]);
        int t=arr[i];arr[i]=arr[j];arr[j]=t;
        newc=0;for(int z=0;z<nq;z++)newc+=jc(which,q[z]);
        int d=newc-oldc;if(d<=0||urnd()<exp(-d/T)){cur+=d;}else{t=arr[i];arr[i]=arr[j];arr[j]=t;}
      }
      if(cur<best){best=cur;memcpy(brow,rows,sizeof(rows));memcpy(bcol,cols,sizeof(cols));}
    }
    memcpy(rows,brow,sizeof(rows));memcpy(cols,bcol,sizeof(cols));
    int chk=total(),chk2=totalc();
    // whole-number second differences of the same picture: count +-1, +-2 (checkerboards), others
    int n1=0,n2=0,no=0;for(int a=0;a<N;a++)for(int b=0;b<N;b++){int v=Zm[rows[a]][cols[b]]-Zm[rows[a+1]][cols[b]]-Zm[rows[a]][cols[b+1]]+Zm[rows[a+1]][cols[b+1]];if(v==1||v==-1)n1++;else if(v==2||v==-2)n2++;else if(v)no++;}
    printf("mode=%d N=%d restart=%d best=%d recount rows=%d cols=%d | whole-number: odd cells %d, checkerboards %d, other %d\n",mode,N,r,best,chk,chk2,n1,n2,no);fflush(stdout);
    if(best<gbest){gbest=best;
      printf("BEST %d\nrows ",best);for(int a=0;a<N;a++)printf("%d ",rows[a]);
      printf("\ncols ");for(int b=0;b<N;b++)printf("%d ",cols[b]);printf("\n");fflush(stdout);}
  }
  return 0;
}
