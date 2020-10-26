import random
import time
import sys
import multiprocessing
from multiprocessing import Lock,Process,Semaphore,Barrier,Array,Queue

INT_MAX = multiprocessing.Value('i',1000000000)
#N=multiprocessing.Value('i',16384)
#DEG=multiprocessing.Value('i',16)
#P=multiprocessing.Value('i',2)
q = multiprocessing.Queue()

N1=int(sys.argv[2])
DEG1=int(sys.argv[3])
P1=int(sys.argv[1])
W = [[0 for x in range(DEG1)] for x in range(N1)]
W_index = [[0 for x in range(DEG1)] for x in range(N1)]
u = multiprocessing.Array('i',range(P1))
D = multiprocessing.Array('i',range(N1))
Q = multiprocessing.Array('i',range(N1))
l = [multiprocessing.Lock() for i in range(0,N1)]
INT_MAX1=1000000000

barrier = Barrier(P1)
local_min = multiprocessing.Array('i',range(P1))

def graph():
	global W
	global W_index
	global P
	global INT_MAX
	global D
	global Q
	global u
	global local_min
	global l

	for i in range(0,N1):
		for j in range(0,DEG1):
			W_index[i][j] = i+j
			W[i][j] = i+j#random.randint(1,3)+i
			if W_index[i][j] >= N1-1 :
				W_index[i][j] = N1-1
				#W[i][j] = N-1 random.randint(1, 10) + i
			if i==i+j:
				W[i][j]=0
			#print (W[i][j], W_index[i][j])
		#print (' ')

def array_init():
	for i in range(0,N1):
		D[i] = INT_MAX1
		Q[i] = 1
	D[0] = 0

def do_work(tid,D,Q,N,DEG,P,u):
	start_time =  time.time()
	local_count=N.value
	N=N.value
	DEG=DEG.value
	P=P.value
	INT_MAX2=INT_MAX.value
	u[tid]=0

	i_start = tid*DEG/P
	i_stop = (tid+1)*DEG/P

	barrier.wait()


	while local_count!=0:                                                  #outer loop
		
		min1 = INT_MAX2
		min_index1 = N-1
		for j in range(int(i_start),int(i_stop)):                            #local_min
			if(D[W_index[u[tid]][j]] < min1 and Q[W_index[u[tid]][j]]==1):     #inner loop
				min1 = D[W_index[u[tid]][j]]
				min_index1 = W_index[u[tid]][j]
		local_min[tid]=min_index1

		barrier.wait()                                                        #barrier

		if tid==0 :
			min2=INT_MAX2
			min_index2=N-1
			for k in range(0,P):
				if D[local_min[k]] < min2 and Q[local_min[k]]==1:
					min2 = D[local_min[k]]
					min_index2 = local_min[k]
			u[tid]=min_index2;
			Q[u[tid]]=0

		barrier.wait()

		if tid!=0:
			u[tid]=u[0]
    
		for i in range(int(i_start),int(i_stop)):
			if(D[W_index[u[tid]][i]] > D[u[tid]] + W[u[tid]][i]):
				D[W_index[u[tid]][i]] = D[u[tid]] + W[u[tid]][i]                   #relax

		local_count = local_count - 1


	final_time = time.time() - start_time
	print ('TID:',tid,'TIME_SEC',final_time)
	strr0 = "inner/inner"
	strr1 = str(P)
	strr11 = str(N)
	strr12 = str(DEG)
	strr2 = ".out"
	strr3 = "-"
	strr_final = strr0 + strr3 + strr1 + strr3 + strr11 + strr3 + strr12 + strr2
	f = open(strr_final,'w')
	f.write(str(final_time))
	f.close
	#if tid==0:
	#	for i in range(0,N):
	#		print (D[i],Q[i])

def main():
	graph()
	array_init()
	P11 = int(sys.argv[1])
	N11 = int(sys.argv[2])
	DEG11 = int(sys.argv[3])
	print (P11)
	P1 = P11
	N1 = N11
	DEG1 = DEG11
	P = multiprocessing.Value('i',P11)
	N = multiprocessing.Value('i',N11)
	DEG = multiprocessing.Value('i',DEG11)

	for i in range(1,P1):
		p = Process(target=do_work,args=(i,D,Q,N,DEG,P,u))
		p.start()
	do_work(0,D,Q,N,DEG,P,u)

	for i in range(1,P1):
		p.join()

if __name__ == "__main__":
	main()
