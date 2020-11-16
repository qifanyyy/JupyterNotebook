"""
	@author: Brando Sánchez BR7
	@Version: 28/03/19
	INSTITUTO POLITÉCNICO NACIONAL
	ESCUELA SUPERIOR DE CÓMPUTO
	CRYPTOGRAPHY
"""

import Potentiaton
from random import *


def main():
	
	n = 127

	print(millerRobin(n))

def millerRobin(n):
	
	nAux = int(n-1)
	
	k=0

	while( nAux % 2 == 0 ):
		nAux = nAux // 2
		print(nAux)
		k+=1
	
	"""
	result = 0
	while (result<nAux):
		result = pow(2,i)
		i+=1
	k = i-2  
	"""
	print('n-1 es: ' + str(n-1) )
	print(pow(2,k))
	#m = int((n-1) / pow(2,k))
	m = nAux
	print('m es: ' + str(m))
	print('k es: ' + str(k))
	
	a = randint(2, n)

	print('a es: ' + str(a))

	b = Potentiaton.squareAndMultiply(a, m, n)

	print('b es: ' + str(b))

	if b == 1 % n:
		return True

	for i in range(0, k):
		print('entro')
		print(b)
		print(n-1)
		if b == n-1:
			return True
		else:
			b = Potentiaton.squareAndMultiply(b,2,n)

	return False

	
