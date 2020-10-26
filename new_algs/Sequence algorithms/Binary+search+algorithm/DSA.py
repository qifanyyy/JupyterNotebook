######################################
#               DSA.py               #
#    Helpers for the DSA lecture     #
#  based on the Java Library for the #
#   book Algorithms by Wayne et al.  #
#                                    #
#            Version 1.0             #
#        (c) 2019 Jens Krüger        #
#  this code is in the public domain #
######################################

import array, sys, time, os

class In:
	def __init__(self, filename):
		self.f = open(filename, "r")
		
	def readAllInts(self):
		strData = []
		lines = self.f.readlines()
		for l in lines:
			strData += l.split()
		intData = []
		for s in strData:
			intData += [int(s)]
		return intData

class Stopwatch:
	def __init__(self):
		self.start = time.perf_counter()
	
	def elapsedTime(self):
		return time.perf_counter() - self.start

def objArray(N):
	return [None]*N
	
def intArray(N):
	return array.array("i", [0]*N)
	
def floatArray(N):
	return array.array("d", [0]*N)

def charArray(N):
	return array.array("B", [0]*N)

val = []
l = ""

def __readline__(retval=True):
	global val
	global l
	if val == []:
		l = sys.stdin.readline()
		val = l.split()
	if retval:
		v = val[0]
		del val[0]
		return v

def stdReadLine():
	global val
	global l
	if val == []:
		l = sys.stdin.readline()
	val = []
	return l

def stdReadString():
	return __readline__()
	
def stdReadInt():
	return int(__readline__())
	
def stdReadChar():
	return __readline__()

def stdIsEmpty():
	global val
	__readline__(False)
	return len(val) == 0
	
def stdReadAllStrings():
	a = []
	while not stdIsEmpty():
		a += [stdReadString()]
	return a
	
def readFileNames(p):
	return [f for f in os.listdir(p) if os.path.isfile(os.path.join(p, f))]
	
def exch(a, i, j):
	t = a[i]
	a[i] = a[j]
	a[j] = t