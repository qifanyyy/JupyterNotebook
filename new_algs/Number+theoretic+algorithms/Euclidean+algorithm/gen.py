#!/usr/bin/python
import random
import sys

n = 5

try:
	n = int(sys.argv[1])
except IndexError: pass

print(n)
print(0)
print(n-1)
for i in xrange(n):
	print('%.13f %.13f' % (random.random(),random.random()))