# Program: Euclidean Algorithm
# Date:   04/20/17
# Author: John Larkin
# Purpose:
# 	This is solely freelance, but I'm doing this to implement something relatively easy,
# 	learn something new, and take my mind off of getting buried by my E90 and by Theory of Computation.
#	This Euclidaean algorithm is implemented in the original way Euclid had intended. 
#	It asymptotically is a lot slower as a result. 

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys 

def euclidean_algorithm(num1, num2):
	''' Efficient algorithm for computing the largest number that divides both numbers '''
	while num1 != num2:
		if num1 > num2:
			num1 = num1 - num2
		else:
			num2 = num2 - num1
	return num1

def print_menu():
	print()
	print('Menu:')
	print('-'*30)
	print('q: quit the program')
	print('r: compute a greatest common denominator')
	print('-'*30)
	print()
	

def main():
	print_menu()
	while True:
		ans = raw_input('What would you like to do?: ')
		if ans == 'q':
			sys.exit(0)
		elif ans == 'r':
			try:
				num1 = int(raw_input('What do you want number 1 to be?: '))
				num2 = int(raw_input('What about number 2?: '))
				print('Computing GCD...')
				gcd_num = euclidean_algorithm(num1,num2)
				print('The answer is: {}'.format(gcd_num))
			except ValueError:
				print('That number was not valid!')
		else:
			print('That was not a valid command.')

if __name__ == '__main__':
	main()