#!/usr/bin/python
from fractions import gcd
import time
import sys

#Finds co-prime number through increasing both x and y values (the two coprime values.)
def coprimes(num):
	for x in range (2, num):
		for y in range (2, num):
			#If the GCD of both x and y values aren't 1 (non prime)
			#and if they aren't the same values, check if their product
			#equals the specified number and return it if true.
			while gcd(x,y) == 1 and x != y:
				if (x * y == num):
					return x, y
				else:
					break

def main(e,n):
	
	start = time.clock()
	#Get the coprimes of n
	p, q = coprimes(n)
	print "The coprimes are p = " + str(p) + " and q = " + str(q)
	#Get the totient
	totient = (p-1)*(q-1)
	print "The totient is " + str(totient)

	i = 1;
	while (i<1000000):
		left = i * e
		a = left - 1
		if(a%totient == 0):
			print "The d value (private key) is " + str(i) +",SUCCESSFUL!"
			break;
		
		i = i + 1



	end = time.clock()
	elapsed = (end - start)
	print "Total time taken to calculate: %f seconds" %elapsed

if __name__ == '__main__':

	e = int(sys.argv[1])
	n = int(sys.argv[2])
	
	main(e,n)
