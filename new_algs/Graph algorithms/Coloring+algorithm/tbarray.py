from math import ceil, log

class TenseBinArray:

	'''
	Container for storing arrays of 0 and 1 as an array of integers.
	Initial array is divided into blocks of equal size T with the last 
	block being less or equal than T. Each block is transformed to an integer
	from [0,..,2^T-1]. Implemetation includes methods for bitwise operations.
	'''

	def __length_error(func):
		def inner(x, y):
			if x.__l != y.__l:
				raise ValueError("length mismatch")
			return func(x, y)
		return inner
		
	def __blocksize_error(func):
		def inner(x, y):
			if x.__b != y.__b:
				raise ValueError("blocksize mismatch")
			return func(x, y)
		return inner
	
	def __init__(self, array, blocksize):
		
		self.__l = len(array)
		self.__b = blocksize
		self.__x = []
		
		for i in range(0, len(array), blocksize):
			block = array[i:i + blocksize]
			value = sum(q * 2**p for p, q in enumerate(block))
			self.__x.append(value)
			
	@property
	def length(self): 
		return self.__l
	
	@property
	def blocksize(self):
		return self.__b
	
	def __first(self, value):
	
		v = 1 - value
	
		mapobj = map(
			lambda c: ((2**self.__b - c - v) & (c + v)).bit_length() - 1,
			self.__x
		)
			
		block, offset = next(
			(x for x in enumerate(mapobj) if x[1] != -1),
			(None, None)
		)
		
		if offset is None:
			res = -1
		else:
			tmp = block * self.__b + offset
			res = tmp if tmp < self.__l else -1
		
		return res
		
	def first0(self):
		return self.__first(0)
		
	def first1(self): 
		return self.__first(1)
		
	def is_zero(self):
		return all(c == 0 for c in self.__x)
	
	@__length_error
	@__blocksize_error
	def or_update(self, other):		
		for i in range(len(self.__x)):
			self.__x[i] |= other.__x[i]
	
	@__length_error
	@__blocksize_error		
	def and_update(self, other):
		for i in range(len(self.__x)):
			self.__x[i] &= other.__x[i]
			
	def not_update(self):
		k, d = divmod(self.__l, self.__b)
		for i in range(k):
			self.__x[i] = 2**self.__b - self.__x[i] - 1
		if d != 0:
			self.__x[-1] = 2**d - self.__x[-1] - 1
			
	def __str__(self):
		s1 = map(lambda c: bin(c)[2:], self.__x)
		s2 = ''.join(c[::-1] for c in s1)
		s3 = s2 + "0" * (self.__l - len(s2))
		return s3
			
	def __getitem__(self, index):
		idx, pow = divmod(index, self.__b)
		return int(self.__x[idx] & 2**pow != 0)
		
	def __setitem__(self, index, value):
	
		if value != 0 and value != 1:
			raise ValueError("value must be 0 or 1")
			
		idx, pow = divmod(index, self.__b)
		if self[index] != value:
			self.__x[idx] ^= 2**pow
	
	@__length_error
	@__blocksize_error
	def __and__(self, other):
		result = self.__class__([0] * self.__l, self.__b)
		result.or_update(self)
		result.and_update(other)
		return result
		
	@__length_error
	@__blocksize_error
	def __or__(self, other):
		result = self.__class__([0] * self.__l, self.__b)
		result.or_update(self)
		result.or_update(other)
		return result
		
	def __invert__(self):
		result = self.__class__([0] * self.__l, self.__b)
		result.or_update(self)
		result.not_update()
		return result
