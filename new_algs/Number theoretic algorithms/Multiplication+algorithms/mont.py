#!/usr/bin/python3

import math, sys, getopt

class Mont(object):

  def __init__(self, mod, wrd_size):
    # Modulus
    if mod < 3 or mod % 2 == 0:
      raise ValueError("Modulus must be an odd number at least 3")
    self.modulus = mod

    # Add wrd_size here so we can avoid final subtraction
    self.reducerbits = 1024 +wrd_size
    self.reducer = 1 << self.reducerbits
    self.mask = self.reducer - 1
    assert self.reducer > mod and math.gcd(self.reducer, mod) == 1

    # Other computed numbers
    self.reciprocal = Mont.reciprocal_mod(self.reducer % mod, mod)
    self.reciprocal_sq = (self.reducer * self.reducer)% mod
    self.factor = (self.reducer * self.reciprocal - 1) // mod
    self.convertedone = self.reducer % mod

  def convert_in(self, x):
    return self.multiply(x, self.reciprocal_sq)

  def convert_out(self, x):
    return self.multiply(x, 1)

  # Inputs and output are in Montgomery form and in the range [0, modulus)
  def multiply(self, x, y):
    mod = self.modulus
    product = x * y
    temp = ((product & self.mask) * self.factor) & self.mask
    reduced = (product + temp * mod) >> self.reducerbits
    result = reduced
    assert 0 <= result < mod
    return result

  def pow(self, x, y):
    assert 0 <= x < self.modulus
    if y < 0:
      raise ValueError("Negative exponent")
    z = self.convertedone
    while y != 0:
      if y & 1 != 0:
        z = self.multiply(z, x)
      x = self.multiply(x, x)
      y >>= 1
    return z

  @staticmethod
  def reciprocal_mod(x, mod):
    # Based on a simplification of the extended Euclidean algorithm
    assert mod > 0 and 0 <= x < mod
    y = x
    x = mod
    a = 0
    b = 1
    while y != 0:
      a, b = b, a - x // y * b
      x, y = y, x % y
    if x == 1:
      return a % mod
    else:
      raise ValueError("Reciprocal does not exist")


try:
   opts, args = getopt.getopt(sys.argv[1:],"hM:w:",           \
                              ["modulus=","wrd_bits="])
except getopt.GetoptError:
   print ('mont.py -M <modulus> -w <word bits>')
   sys.exit(2)

M = 0xb0ad4555c1ee34c8cb0577d7105a475171760330d577a0777ddcb955b302ad0803487d78ca267e8e9f5e3f46e35e10ca641a27e622b2d04bb09f3f5e3ad274b1744f34aeaf90fd45129a02a298dbc430f404f9988c862d10b58c91faba2aa2922f079229b0c8f88d86bfe6def7d026294ed9dee2504b5d30466f7b0488e2666b
WRD_BITS = 16

for opt, arg in opts:
   if opt == '-h':
      print ('mont.py -M <modulus> -w <word bits>')
      sys.exit()
   elif opt in ("-M", "--modulus"):
      M = int(arg)
   elif opt in ("-w", "--wrd_bits"):
      WRD_BITS = int(arg)

print ()
print ('Parameter Values')
print ('---------------------')
print ('WRD_BITS   ', WRD_BITS)
print ('M          ', hex(M))
print ()

mont = Mont(M, WRD_BITS)
print("RECIPROCAL:", hex(mont.reciprocal))
print("RECIPROCAL_SQ:", hex(mont.reciprocal_sq))
print("FACTOR:", hex(mont.factor))


