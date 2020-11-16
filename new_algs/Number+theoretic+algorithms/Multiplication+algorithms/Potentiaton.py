"""
	@author: Brando Sánchez BR7
	@Version: 12/03/19
	INSTITUTO POLITÉCNICO NACIONAL
	ESCUELA SUPERIOR DE CÓMPUTO
	CRYPTOGRAPHY
"""

def main():

	base = 50321
	exp = 60749
	modN = 77851

	result = squareAndMultiply(base, exp, modN)

	print(str(base) + " to " + str(exp) + " mod " + str(modN) + " is " + str(result))

def squareAndMultiply(base, exp, modN):
	
	expBin = str(bin(exp)[2:])
	
	z=1
	for i in range(len(expBin)-1, -1, -1):
		"""
		print(i)
		print(expBin[len(expBin)-1-i])
		"""
		z = z * z % modN
		
		if expBin[len(expBin)-1-i] == '1':
			z = z * base % modN

		"""
		print(z)
		print()
		"""
	return z

