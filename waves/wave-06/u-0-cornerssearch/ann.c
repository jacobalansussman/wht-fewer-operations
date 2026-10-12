// u-0 corners-search: simulated annealing over the two orders of the subset-sum picture.
// corners = non-zeros of the second difference M of A[a][b] = [cols[b] subset of rows[a]], zero row/column appended after the last.
// The count is a sum over neighbouring rows (rcost) and also a sum over neighbouring columns (ccost): moves touch 2 or 3 junctions.
// usage: ann k iters restarts seed T0 T1 [seedfile]   (seedfile: line 1 = rows, line 2 = cols)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
#define MAXN 1024
static int N,k;
static unsigned char Zm[MAXN+1][MAXN+1];
static int rows[MAXN+1], cols[MAXN+1], brow[MAXN+1], bcol[MAXN+1], grow[MAXN+1], gcol[MAXN+1];
static uint64_t s[2];
static inline uint64_t rnd(void){uint64_t s1=s[0],s0=s[1];uint64_t r=s0+s1;s[0]=s0;s1^=s1<<23;s[1]=s1^s0^(s1>>17)^(s0>>26);return r;}
static inline double urnd(void){return (rnd()>>11)*(1.0/9007199254740992.0);}
static inline int rcost(int S,int S2){int prev=0,c=0;const unsigned char*p=Zm[S],*q=Zm[S2];for(int b=N-1;b>=0;b--){int t=cols[b];int d=p[t]-q[t];c+=(d!=prev);prev=d;}return c;}
static inline int ccost(int T,int T2){int prev=0,c=0;for(int a=N-1;a>=0;a--){const unsigned char*p=Zm[rows[a]];int d=p[T]-p[T2];c+=(d!=prev);prev=d;}return c;}
static inline int jc(int which,int q){ if(q<0) return 0; return which? ccost(cols[q],cols[q+1]) : rcost(rows[q],rows[q+1]); }
static int total(void){int c=0;for(int a=0;a<N;a++)c+=rcost(rows[a],rows[a+1]);return c;}
static int totalc(void){int c=0;for(int b=0;b<N;b++)c+=ccost(cols[b],cols[b+1]);return c;}
static void rev(int*arr,int i,int j){while(i<j){int t=arr[i];arr[i]=arr[j];arr[j]=t;i++;j--;}}
static void rot(int*arr,int i,int m,int p){rev(arr,i,m);rev(arr,m+1,p);rev(arr,i,p);} // [i..m][m+1..p] -> [m+1..p][i..m]
int main(int argc,char**argv){
  k=atoi(argv[1]);N=1<<k;long iters=atol(argv[2]);int restarts=atoi(argv[3]);uint64_t seed=strtoull(argv[4],0,10);
  double T0=atof(argv[5]),T1=atof(argv[6]);
  for(int S=0;S<=N;S++)for(int T=0;T<=N;T++)Zm[S][T]=(S<N&&T<N&&((S&T)==T))?1:0;
  int have_seed=0;
  if(argc>7){FILE*f=fopen(argv[7],"r");for(int a=0;a<N;a++)if(fscanf(f,"%d",&grow[a])!=1)return 2;for(int b=0;b<N;b++)if(fscanf(f,"%d",&gcol[b])!=1)return 2;fclose(f);have_seed=1;}
  int gbest=1<<30;
  for(int r=0;r<restarts;r++){
    s[0]=seed*0x9E3779B97F4A7C15ULL+r*7919+1;s[1]=(seed+r+1)*0xBF58476D1CE4E5B9ULL+3;for(int i=0;i<20;i++)rnd();
    if(have_seed){memcpy(rows,grow,sizeof(int)*N);memcpy(cols,gcol,sizeof(int)*N);}
    else{for(int i=0;i<N;i++){rows[i]=i;cols[i]=i;}
      for(int i=N-1;i>0;i--){int j=rnd()%(i+1);int t=rows[i];rows[i]=rows[j];rows[j]=t;j=rnd()%(i+1);t=cols[i];cols[i]=cols[j];cols[j]=t;}}
    rows[N]=N;cols[N]=N;
    int cur=total(),best=cur;memcpy(brow,rows,sizeof(rows));memcpy(bcol,cols,sizeof(cols));
    if(r==0) printf("start %d (by columns %d)\n",cur,totalc());
    double lr=log(T1/T0);
    for(long it=0;it<iters;it++){
      double T=T0*exp(lr*(double)it/iters);
      int which=rnd()&1;int*arr=which?cols:rows;int mv=rnd()%3;
      int i=rnd()%N,j=rnd()%N;if(i==j)continue;if(i>j){int t=i;i=j;j=t;}
      int oldc,newc;
      if(mv==0){ // reverse [i..j]
        oldc=jc(which,i-1)+jc(which,j);rev(arr,i,j);newc=jc(which,i-1)+jc(which,j);
        int d=newc-oldc;if(d<=0||urnd()<exp(-d/T)){cur+=d;}else rev(arr,i,j);
      } else if(mv==1){ // rotate [i..m][m+1..j]
        int m=i+rnd()%(j-i);
        oldc=jc(which,i-1)+jc(which,m)+jc(which,j);rot(arr,i,m,j);int nm=i+(j-m)-1;newc=jc(which,i-1)+jc(which,nm)+jc(which,j);
        int d=newc-oldc;if(d<=0||urnd()<exp(-d/T)){cur+=d;}else rot(arr,i,nm,j);
      } else { // swap i,j
        int q[4]={i-1,i,j-1,j};int nq=4;if(j==i+1){q[2]=j;nq=3;}
        oldc=0;for(int z=0;z<nq;z++)oldc+=jc(which,q[z]);
        int t=arr[i];arr[i]=arr[j];arr[j]=t;
        newc=0;for(int z=0;z<nq;z++)newc+=jc(which,q[z]);
        int d=newc-oldc;if(d<=0||urnd()<exp(-d/T)){cur+=d;}else{t=arr[i];arr[i]=arr[j];arr[j]=t;}
      }
      if(cur<best){best=cur;memcpy(brow,rows,sizeof(rows));memcpy(bcol,cols,sizeof(cols));}
    }
    memcpy(rows,brow,sizeof(rows));memcpy(cols,bcol,sizeof(cols));
    int chk=total(),chk2=totalc();
    printf("N=%d restart=%d best=%d recount rows=%d cols=%d final cur=%d\n",N,r,best,chk,chk2,cur);fflush(stdout);
    if(best<gbest){gbest=best;
      printf("BEST %d nnz %d gates %d\nrows [",N,best,N-2+best);for(int a=0;a<N;a++)printf("%d%s",rows[a],a<N-1?", ":"");
      printf("] r []\ncols [");for(int b=0;b<N;b++)printf("%d%s",cols[b],b<N-1?", ":"");printf("] c []\n");fflush(stdout);}
  }
  return 0;
}
