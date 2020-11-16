#
# vectors.py
#
# An overview of how we overcome the lack of a formal vector type
# in Python. We can instead use lists and define arithmetic operations,
# however ideally you should use NumPy arrays for production code.
#

import math


# Vector addition (element-wise addition)
def vector_add(v, w):
    return [vi + wi for vi, wi in zip(v, w)]


# Vector subtraction (element-wise subtraction)
def vector_subtract(v, w):
    return [vi - wi for vi, wi in zip(v, w)]


# Sum multiple vectors (element-wise)
def sum_vectors(vectors):
    return reduce(vector_add, vectors)


# Multiply vector by a scalar (element-wise multiply by constant)
def scalar_multiply(v, c):
    return [c * vi for vi in v]


# Componentwise means of vectors
def vector_mean(vectors):
    return scalar_multiply(sum_vectors(vectors), 1/len(vectors))


# Dot product (sum of componentwise products)
def dot(v, w):
    return sum(vi * wi for vi, wi in zip(v, w))


# Sum of squares
def sum_of_squares(v):
    return dot(v, v)


# Length aka magnitude
def magnitude(v):
    return math.sqrt(sum_of_squares(v))


# Squared distance between 2 vectors
def squared_distance(v, w):
    return sum_of_squares(vector_subtract(v, w))


# Distance between 2 vectors
def distance(v, w):
    return math.sqrt(squared_distance(v, w))
    #return magnitude(vector_subtract(v, w))




def main():

    # We can model any combination of related numbers as a vector
    height_weight_age = [70, 170, 40]


