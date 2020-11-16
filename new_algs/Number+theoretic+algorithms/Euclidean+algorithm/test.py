#!/usr/bin/env python3

import unittest

from euclidean import euclideanGCD, extendedEuclidean


class test_euclideanGCD(unittest.TestCase):
    
    def test_0(self):
        
        data = [
            #a  b  r
            (0, 0, 0),
            (0, 1, 1),
            (1, 0, 1),
            (0, 12,12),
            (12,0, 12)
        ]
        
        for a,b,r in data:
            with self.subTest(a=a, b=b, r=r):
                self.assertEqual( euclideanGCD( a, b ), r )
    
    
    def test_1(self):
        
        data = [
            #a  b  r
            (1, 12,1),
            (12,1, 1)
        ]
        
        for a,b,r in data:
            with self.subTest(a=a, b=b, r=r):
                self.assertEqual( euclideanGCD( a, b ), r )
    
    
    def test_big_factors(self):
        
        data = [
            # a             b               r
            (1406700,       164115,         23445),
            (164115,        1406700,        23445),
            (55534,         434334,         2),
            (434334,        55534,          2),
            (30315475,      24440870,       31415),
            (24440870,      30315475,       31415),
            (37279462087332,366983722766,   564958),
            (366983722766,  37279462087332, 564958)
        ]
        
        for a,b,r in data:
            with self.subTest(a=a, b=b, r=r):
                self.assertEqual( euclideanGCD( a, b ), r )
    
    
    def test_big_primes(self):
        
        data = [
            # a          b           r
            (2921802413, 20358439,   1),
            (20358439,   2921802413, 1),
            (85796527,   34775062331,1),
            (34775062331,85796527,   1)
        ]
        
        for a,b,r in data:
            with self.subTest(a=a, b=b, r=r):
                self.assertEqual( euclideanGCD( a, b ), r )



class test_extendedEuclidean(unittest.TestCase):
    
    def test_gcd(self):
        
        data = [
            #a          b           r
            (0,         0,          0),
            (0,         1,          1),
            (1,         12,         1),
            (55534,     434334,     2),
            (30315475,  24440870,   31415),
            (2921802413,20358439,   1)
        ]
        
        for a,b,r in data:
            with self.subTest(a=a, b=b, r=r):
                self.assertEqual( extendedEuclidean( a, b )[0], r )
    
    
    def test_linearcombos(self):
        
        data = [
            # a             b
            (0,             0),
            (0,             1),
            (1,             0),
            (1,             12),
            (12,            1),
            (55534,         434334),
            (434334,        55534),
            (434334,        -55534),
            (-434334,        55534),
            (30315475,      24440870),
            (2921802413,    20358439),
            (20358439,      2921802413),
            (37279462087332,366983722766)
        ]
        
        for a,b in data:
            with self.subTest(a=a, b=b):
                r,s,t = extendedEuclidean( a, b )
                
                self.assertEqual( r, a*s + b*t )
        

if __name__ == '__main__':
    unittest.main()
