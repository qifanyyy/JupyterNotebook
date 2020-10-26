import random
import time
import threading
from threading import Thread,Semaphore


globvar = 1
INT_MAX = 1000000000
N=16
DEG=16
P=2
u=0
W = [[0 for x in range(DEG)] for x in range(N)]
W_index = [[0 for x in range(DEG)] for x in range(N)]
D = [0 for x in range(N)]
Q = [0 for x in range(N)]


threads = []

class Barrier:
	def __init__(self, n):
		self.n = n
		self.count = 0
		self.mutex = Semaphore(1)
		self.barrier = Semaphore(0)
	def wait(self):
		self.mutex.acquire()
		self.count = self.count + 1
		self.mutex.release()
		if self.count == self.n: 
			self.barrier.release()
			self.barrier.acquire()
			self.barrier.release()

barrier = Barrier(P)
local_min = [0 for i in range(P)]

def graph():
	print 'Hello, world!'
	global globvar
	global W
	global W_index
	global P
	global INT_MAX
	global D
	global Q
	global u
	global local_min
	for i in range(0,N):
		for j in range(0,DEG):
			W_index[i][j] = i+j
			W[i][j] = i+j#random.randint(1,3)+i
			if W_index[i][j] >= N-1 :
				W_index[i][j] = N-1
				W[i][j] = N-1#random.randint(1, 10) + i
			if i==j:
				W[i][j]=0
			#print W[i][j]
		#print ' '

def array_init():
	for i in range(0,N):
		D[i] = INT_MAX
		Q[i] = 1
	D[0] = 0

def do_work(tid):
	start_time =  time.time()
	local_count=N
	u=0
	
	i_start = tid*DEG/P
	i_stop = (tid+1)*DEG/P
	#print i_start,i_stop,tid

	while local_count!=0:                        #outer loo
		
		
		min1 = INT_MAX
		min_index1 = N-1
		for j in range(i_start,i_stop):                   #local_min
			if(D[j] < min1 and Q[j]):            #inner loop
				min1 = D[j]
				min_index1 = W_index[u][j]
		local_min[tid]=min_index1
		
		#print local_min[tid],tid

		barrier.wait()

		if tid==0 :
			min2=INT_MAX
			min_index2=0
			for k in range(0,P):
				if D[local_min[k]] < min2 and Q[local_min[k]]:
					min2 = D[local_min[k]]
					min_index2 = local_min[k]
			u=N-local_count
			Q[u]=0
			#print u

		barrier.wait()

		for i in range(i_start,i_stop):
			if(D[W_index[u][i]] > D[u] + W[u][i]):
				D[W_index[u][i]] = D[u] + W[u][i]
				#print D[W_index[u][i]]
		
		local_count = local_count - 1
	final_time = time.time() - start_time
	#print final_time
	if tid==0:
		for i in range(0,N):
			print D[i]

def main():
	graph()
	array_init()

	#start_time = time.clock()
	#print start_time

	#do_work(1)
	for i in range(P):
		t = threading.Thread(target=do_work,args=(i,))
		threads.append(t)
		t.start()
	
	#second_time = time.clock()
	#final_time = second_time - start_time
	#print second_time, "seconds"
	#for i in range(0,N):
	#	print D[i]


if __name__ == "__main__":
	#print time.clock()
	main()
	#print time.clock()
