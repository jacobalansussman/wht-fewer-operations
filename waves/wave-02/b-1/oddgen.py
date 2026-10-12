# oddgen.py [b-1] exact (bit operations).  The 'four moves per array' design at every block size m: each odd-weight direction once, W = 2^(m-3).
# Uses only the product forms q(z) = (a.z)(b.z), a.b = 1, a != b (they have q(I) = a.b = 1).  If these alone join every pair of moves,
# the design has a set of 2^(m-1) > W moves pairwise joined by tight forms and is excluded by the clique lemma.
import sys
def dot(a,b): return bin(a&b).count("1")&1
for m in range(4,int(sys.argv[1])+1):
    odd=[z for z in range(1<<m) if bin(z).count("1")&1]; pos={z:i for i,z in enumerate(odd)}; W=1<<(m-3)
    H=[sum(1<<i for i,z in enumerate(odd) if dot(a,z)) for a in range(1<<m)]
    adj=[0]*len(odd); tight=0; minsel=1<<30
    for a in range(1,1<<m):
        for b in range(a+1,1<<m):
            if not dot(a,b): continue
            s=H[a]&H[b]; c=bin(s).count("1"); minsel=min(minsel,c)
            if c==W:
                tight+=1; r=s
                while r:
                    i=(r&-r).bit_length()-1; r&=r-1; adj[i]|=s
    full=(1<<len(odd))-1
    alljoined=all(adj[i]|(1<<i)==full for i in range(len(odd)))
    print("m = %d: %d moves, W = %d (plain %d); product forms: fewest moves selected %d, tight ones %d, every pair of moves joined: %s -> %s"
          %(m,len(odd),W,m*W,minsel,tight,alljoined,"clique %d > W: EXCLUDED"%len(odd) if alljoined else "not decided by product forms"))
