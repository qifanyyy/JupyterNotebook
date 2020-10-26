import pdb

print("Karatsuba multiplication -- assuming input is both 4 digits")

n1 = raw_input("Enter n1: ")
n2 = raw_input("Enter n2: ")

a = int(n1[:2])
b = int(n1[2:])

c = int(n2[:2])
d = int(n2[2:])

p1 = a * c
p2 = b * d
p3 = (a + b) * (c + d)

rest = p3 - p2 - p1

f1 = int(str(p1).ljust(len(str(p1)) + 4, '0')) #first product padded with four zeroes
f3 = int(str(rest).ljust(len(str(rest)) + 2, '0')) #third product padded with two zeroes

print(f1 + p2 + f3)

