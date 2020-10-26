#!/usr/local/bin/python3
"""
pi_sim.py
AUTHOR:     Peter Walker
DATE:       26 November 2015
ABSTRACT:
    A Monte Carlo approximation of the value of pi.
"""

import math
import random
import datetime as dt


def _make_point(maxX=1, maxY=1):
    """Creating a random X,Y point"""
    maxX, maxY = (math.fabs(maxX), math.fabs(maxY))
    return (random.uniform(maxX*-1, maxX), random.uniform(maxY*-1, maxY))
#END DEF


def _in_circle(x, y, r=1):
    """Tests if the given X and Y are in the radius R"""
    return not math.sqrt((x**2)+(y**2))>r
#END DEF


def approx_pi(numpoints=100):
    """
    Using the given number of points, generates an approximation of PI.

    @param      numpoints : Integer, number of points to create for approx
    @return     Float, the approximation of PI
    @return     Float, the percent error to math.pi
    """
    _numin = 0.0
    _total = 0.0
    for _ in range(numpoints):
        _x, _y = _make_point()
        if _in_circle(_x, _y):
            _numin+=1
        _total+=1
    #END FOR

    #We multiply by 4, because our "squares" area is 4
    _pi = 4 * (_numin/_total)
    _error = math.fabs((_pi-math.pi)/math.pi)*100

    return (_pi, _error)
#END DEF


# ---- The MAIN of this script ------------------------------------------------
def main():
    """Script Main"""

    _NUMTESTS = 1000
    _TESTS = [1,2,3,4,5,10,20,30,40,50,100,150,200,250,300,350,400,450,500,
              600,700,800,900,1000,1100,1200,1300,1400,1500,1750,2000,
              2250,2500,2750,3000,3500,4000,5000,6000,8000,10000]

    for points in _TESTS:
        errors = []
        start = dt.datetime.now()
        for _ in range(_NUMTESTS):
            pi, error = approx_pi(points)
            errors.append(error)
        #END FOR
        diff = dt.datetime.now() - start
        print("{0}, {1}%, {2}".format(str(points).ljust(5),
                                      str(sum(errors) / float(len(errors)))[:7],
                                      diff))
    #END FOR
#END DEF


main()

#END OF LINE
