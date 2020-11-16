import os
from sys import platform

def clear():
	""" Multi S.O. function to clear the terminal screen """
	if platform == "linux":
		_ = os.system('clear')
	elif platform == "win32":
		_ = os.system('cls')

print('Complete the requested values')
p = int(input('p: '))
q = int(input('q: '))
n = p * q
phi = (p-1)*(q-1)
print('n =',n,'phi =',phi)
e = int(input('e: '))
print('Calculating d...')

posD = [phi, 1]
rem = [phi, e]
quot = []
# ------------------------------- #
#   EXTENDED EUCLIDEAN ALGORITHM  #
# ------------------------------- #
i = 0 														# Initial index
while rem[-1] != 1:											# While remainder is not 1 or 0 keep going
	rem.append(rem[i]%rem[i+1])								# Append to REM the remainder of the division of the last two remainders
	quot.append(rem[i]//rem[i+1])							# Append to QUOT the quotient of the last division
	posD.append((posD[i]-(posD[i+1]*quot[i]))%phi)			# Append to POSD the penultimate posD minus the product between the last posD and the last quotient
	i = i + 1
d = posD[-1]
# For debugging purposes
# print('rem: ',rem)
# print('quot: ',quot)
# print('posD: ',posD)

if rem[-1] != 0:											# If the last remainder is equal to 0 means that some number is not right
	print('d =', d)
else:
	print('Couldn\'t find d, check all introduced parameters.')
	exit()

os.system('echo off')
print('Press a key to continue...')
os.system('pause')
clear()

if input('Decrypt? (s/n): ').lower() == 's':
	listDec = []
	encCad = input('Insert the numbers to decrypt separated by 1 space: ').split(' ')
	for enc in encCad:
		listDec.append(chr((int(enc)**d)%n+97))
	# print(listDec)
	print('Decrypted string: '+' '.join(listDec))	# Show it via terminal
