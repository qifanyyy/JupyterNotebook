# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 21:47:58 2019

@author: DSU
"""
"""
To compile the shared library (increased stack size for FibCassini):
g++ -c -fPIC bigint.cpp -o bigint.o -Wl,--stack,1073741824
g++ -shared -Wl,-soname,libbigint.so -o libbigint.so bigint.o
"""

# load libraries and functions
import ctypes
lib = ctypes.cdll.LoadLibrary("../bigint/libbigint.so")

# FibLoop call to cpp
lib.FibLoop.argtypes = [ctypes.c_int]
lib.FibLoop.restype = ctypes.c_char_p
def FibLoop(n: int) -> str:
    assert n >= 0
    return lib.FibLoop(n).decode('utf-8')

# FibMatrix call to cpp
lib.FibMatrix.argtypes = [ctypes.c_int]
lib.FibMatrix.restype = ctypes.c_char_p
def FibMatrix(n: int) -> str:
    assert n >= 0
    return lib.FibMatrix(n).decode('utf-8')

# FibCassini call to cpp
lib.FibCassini.argtypes = [ctypes.c_int]
lib.FibCassini.restype = ctypes.c_char_p
def FibCassini(n: int) -> str:
    assert n >= 0
    return lib.FibCassini(n).decode('utf-8')

algorithms = [FibLoop, FibMatrix, FibCassini]

"""
Driver code verification
Runs up to 50th fib number
"""
if __name__ == '__main__':
    for i in range(50):
        vals = [algo(i) for algo in algorithms]
        assert all(vals[0] == x for x in vals)
