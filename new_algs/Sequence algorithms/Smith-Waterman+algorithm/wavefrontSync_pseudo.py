#Author: Dario Sitnik
#ALGORITHM FOR WAVEFRONT BLOCK SYNCHRONIZATINO. List sync contains lists of block IDs which can run in parallel.  
#NOTE: LARGER SEQUENCE MUST BE ON X-AXIS (Second argument in matrix - N)

def wavefrontSync(M, N):
    i=0
    limit = 1
    decrease = False
    sync = []
    while i<=N*M:
        parallel = []
        if decrease:
            limit -= 1
        for j in range(limit):            
            parallel.append(i+j*N-(j-1))
        if limit<M and (i+1)%N!=0:
            limit += 1
        if (i+1)%N==0 and i!=0:
            i+=N
            decrease = True
        else:
            i+=1
        sync.append(parallel)
    return (sync)

M=5
N=6 #N is always a larger sequence
print(wavefrontSync(5, 7))
