#
# This is a toy RSA encryption breaker using Shor's algorithm (params: a = 2, N = 85)
# To use your custom alphabet, please change alphabet var
# 


from qiskit import QuantumProgram
from fractions import gcd
from math import pi


qp = QuantumProgram()
qr = qp.create_quantum_register('qr', 8)
cr = qp.create_classical_register('cr', 4)
qc = qp.create_circuit('Shor',[qr],[cr])

def Oracle():
	qc.cx(qr[2], qr[6])
	qc.cx(qr[3], qr[7])


def findPQ(a, N):

	qc.h(qr[0])
	qc.h(qr[1])
	qc.h(qr[2])
	qc.h(qr[3])

	Oracle()

	qc.h(qr[0])
	qc.cu1(pi/2, qr[0], qr[1])
	qc.h(qr[1])
	qc.cu1(pi/4, qr[0], qr[2])
	qc.cu1(pi/2, qr[1], qr[2])
	qc.h(qr[2])
	qc.cu1(pi/8, qr[0], qr[3])
	qc.cu1(pi/4, qr[1], qr[3])
	qc.cu1(pi/2, qr[2], qr[3])
	qc.h(qr[3])

	qc.measure(qr[0], cr[0])
	qc.measure(qr[1], cr[1])
	qc.measure(qr[2], cr[2])
	qc.measure(qr[3], cr[3])

	result = qp.execute(['Shor'])#, backend='ibmqx_qasm_simulator', shots=1024, wait=5, timeout=1200)
	res = result.get_counts('Shor')

	mult_list = []
	for k in res.keys():
		p = int(k, 2)
		if p % 2 == 0:
			k1 = a**(p/2) - 1
			k2 = a**(p/2) + 1
			mult_list.append((gcd(k1, N), gcd(k2, N)))
		else:
			print("Period is odd, skipping")

	print("mult_list: {}".format(mult_list))
	return mult_list


def decrypt(public_key, message):

	m_list = findPQ(2, public_key[1])

	#alphabet84 = " !(),-./0123456789:?АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюя"
	#alphabet50 = " !(),-.0123456789:?АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

	alphabet = " !(),-./0123456789:?АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюя"

	message = [alphabet.find(i) for i in message]

	for m in m_list: 

		fi = (m[0]-1)*(m[1]-1)

		if(fi == 0):
			print("N = N * 1, skipping")
		else:

			d = 0 
			while True:
				rem = (d*public_key[0]) % fi
				if rem == 1:
					break
				else:
					d = d + 1

			text = ''
			for i in message:
				text += alphabet[i**d % public_key[1]]
			print("The message is: {}".format(text))

if __name__ == '__main__':
	decrypt((11, 85), "Ы97 3хД7УЙ НЖ3 Жл2Ж, Н9ще7 НЖ?32Ж Дхнх9лЖ,д")