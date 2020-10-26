import random, os
import shors

def Extended_euclid(a, b):
	x0, x1, y0, y1 = 0, 1, 1, 0

	while a != 0:
		q, b, a = b//a, a, b%a
		y0, y1 = y1, y0 - q*y1
		x0, x1 = x1, x0 - q*x1

	return b, x0, y0

def Rabin_Miller_Test(n):
	#n-1 = 2^k . m
	#m = (n-1)/(2^k)
	k=0
	temp=0
	while 1:
		k += 1
		m = (n-1)/(pow(2,k))
		if m-int(m) != 0:
			k -= 1
			break
		temp = m
	
	m = int(temp)

	if temp == 0:			#Even Number
		return False

	a = random.randrange(2, n-1)

	b0 = pow(a,m,n)
	if b0 == 1:
		return True
	if b0 == n-1:
		return True
	temp=b0

	for i in range(k-1):
		b = pow(temp,2,n)
		if b == 1:
			return False
		if b == n-1:
			return True
		temp = b
		

def GenerateRandomPrimes():
	p=0
	q=0
	while p==q:
		p = random.randrange(100, 1000)
		q = random.randrange(100, 1000)
	

	while 1:
		if not Rabin_Miller_Test(p):
			p += 1
		if not Rabin_Miller_Test(q):
			q += 1
		if Rabin_Miller_Test(p) and Rabin_Miller_Test(q):
			return p,q
			

def generatePublicKey(totient):
	public_key = random.randrange(3, totient)
	while not Rabin_Miller_Test(public_key):
		public_key += 1
	return public_key


def generatePrivateKey(public_key, totient):

	g, _, private_key = Extended_euclid(totient, public_key)
	if private_key > totient:
		private_key = private_key % totient
	elif private_key < 0:
		private_key += totient


	return private_key



if __name__ == '__main__':

	os.system("clear")
	p, q = GenerateRandomPrimes()
	n = p*q
	totient = (p-1)*(q-1)
	public_key = generatePublicKey(totient)
	private_key = generatePrivateKey(public_key, totient)
	enc_list = []
	decrypted_mess = ""

	printline = "*"*100
	print(printline)
	print("\nRSA Encryption-Decryption\n")
	print(printline)
	print("p - ", p)
	print("q - ", q)
	print("n - ", n)
	print("PHI - ", totient)
	print("Public Key (e, n) - ", "(", public_key, ", ", n, ")")
	print("Private Key (d, n) - ", "(", len(str(private_key))*"x", ", ", n, ")")
	print(printline)
	
	message = input("Enter a message: ")
	for char in message:
		mess = ord(char)
		enc_mess = str(pow(mess, public_key, n))
		enc_list.append(enc_mess)

	print("Encrypted Message - ", "".join(enc_list))
	for enc_mess in enc_list:
		decr = (pow(int(enc_mess), private_key, n))
		decrypted_mess += chr(decr)
		
	print("Decrypted Message - ", decrypted_mess)

	print("-----------------------------------------\n\nDecryption with SHOR\n")
	p, q = shors.shors(n)
	print("Calculating the totient....")
	tot = (p-1) * (q-1)
	print("Generating the private key....")
	prvKey = generatePrivateKey(public_key, tot)
	print("Private key found(You are doomed) : ", prvKey)
	print("Decrypted message is : \n")
	decrmess = ""
	for enc_mess in enc_list:
		decr = (pow(int(enc_mess), prvKey, n))
		decrmess += chr(decr)
	print(decrmess)