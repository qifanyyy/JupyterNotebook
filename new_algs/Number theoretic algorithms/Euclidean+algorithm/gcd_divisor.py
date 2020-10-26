# Program: Euclidean Algorithm
# Date:   04/20/17
# Author: John Larkin
# Purpose:
# 	This is solely freelance, but I'm doing this to implement something relatively easy,
# 	learn something new, and take my mind off of getting buried by my E90 and by Theory of Computation.
#	This Euclidaean algorithm is with a little more insight that Euclid imagined, as it uses the modulo
# 	operation, while Euclids original algorithm used subtraction. 

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import signal
import sys
import time

def euclidean_algorithm(num1, num2):
	while num2 != 0:
		t = num2
		num2 = num1 % num2
		num1 = t
	return num1

def main():
    print("Press control + c to quit the program.")
    try:
        while True:
            num1 = int(raw_input('What do you want number 1 to be?: '))
            num2 = int(raw_input('What about number 2?: '))
            print('Computing GCD...')
            gcd_num = euclidean_algorithm(num1,num2)
            print('The answer is: {}'.format(gcd_num))
    except KeyboardInterrupt:
        print()
        print('Quitting gracefully.')
        sys.exit(1)

if __name__ == '__main__':
    main()
