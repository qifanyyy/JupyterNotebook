"""
@author: David Lei
@since: 22/04/2017
@modified: 

Computational geometry problem: given n points in metric space, find a pair of points with the smallest distance between them.

Input: Array of n points (x, y) coords.
Output: Smallest distance b/w 2 points in the array.

Brute force: O(n^2), compare all elements in points to all others.

Divide and Conquer:
- Smart: O(n*log(n))
- Less smart: O(n*log(n)^2)
"""

def closest_pair_of_points(points):
    middle_point = len(points)//2

    left = points[:middle_point]
    right = points[middle_point:]

    # Recursively find smallest distance in sub arrays.
