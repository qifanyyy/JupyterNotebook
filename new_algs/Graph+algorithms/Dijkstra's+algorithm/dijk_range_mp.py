import random
import time
import sys
import multiprocessing
from multiprocessing import Lock,Process,Semaphore,Barrier,Array,Queue

INT_MAX = multiprocessing.Value('i',1000000000)
#N=multiprocessing.Value('i',16384)
#DEG=multiprocessing.Value('i',16)
#P=multiprocessing.Value('i',1)
q = multiprocessing.Queue()

N1=int(sys.argv[2])
DEG1=int(sys.argv[3])
P1=int(sys.argv[1])
W = [[0 for x in range(DEG1)] for x in range(N1)]
W_index = [[0 for x in range(DEG1)] for x in range(N1)]
u = multiprocessing.Array('i',range(P1))
D = multiprocessing.Array('i',range(N1))
Q = multiprocessing.Array('i',range(N1))
range_1 = multiprocessing.Array('i',range(P1))
terminate = multiprocessing.Array('i',range(P1))
lock = multiprocessing.Lock()
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

def do_work(tid,D,Q,N,DEG,P,u,  l,lock,  terminate,range_1):
	start_time =  time.time()
	local_count=N.value
	N=N.value
	DEG=DEG.value
	P=P.value
	INT_MAX2=INT_MAX.value
	u[tid]=0
	uu=0

	i_start = tid*DEG/P
	i_stop = (tid+1)*DEG/P

	barrier.wait()

	while terminate[0]==0:                                           #outer loop
		while u[0]<range_1[0]:

			for i in range(0,DEG):
				l[W_index[uu][i]].acquire()
				if(D[W_index[uu][i]] > D[uu] + W[uu][i]):
					D[W_index[uu][i]] = D[uu] + W[uu][i]                   #relax
				l[W_index[uu][i]].release()
				
			lock.acquire()
			if u[0]<range_1[0]:
				u[0] = u[0] + 1
				uu = u[0]
				if u[0] >= N-1:
					terminate[0] = 1
			lock.release()

		if tid==0:
			range_1[0] = range_1[0]*DEG
			if range_1[0] >= N:
				range_1[0] = N
				
		barrier.wait()
			
	final_time = time.time() - start_time
	print ('TID:',tid,'TIME_SEC',final_time)
	strr0 = "range/range"
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
	print(P11)
	P1 = P11
	N1 = N11
	DEG1 = DEG11
	P = multiprocessing.Value('i',P11)
	N = multiprocessing.Value('i',N11)
	DEG = multiprocessing.Value('i',DEG11)

	range_1[0] = 1
	terminate[0] = 0

	for i in range(1,P1):
		p = Process(target=do_work,args=(i,D,Q,N,DEG,P,u,  l,lock,  terminate,range_1))
		p.start()
	do_work(0,D,Q,N,DEG,P,u,  l,lock, terminate,range_1)

	for i in range(1,P1):
		p.join()

if __name__ == "__main__":
	main()
