#!/usr/bin/env python
from math import *
from decimal import Decimal
import math
import numpy as np
from itertools import imap

class MyMathHelper:
    """ Provides mathematical functions needed for my recommendation system """

    # These functions are the "standard" mathematical functions
    @staticmethod
    def euclidean_distance(x, y):
        """ return euclidean distance between two lists """

        return sqrt(sum(pow(a - b, 2) for a, b in zip(x, y)))

    @staticmethod
    def manhattan_distance(x, y):
        """ return manhattan distance between two lists """

        return sum(abs(a - b) for a, b in zip(x, y))

    @staticmethod
    def minkowski_distance(x, y, p_value):
        """ return minkowski distance between two lists """

        return MyMathHelper.nth_root(sum(pow(abs(a - b), p_value) for a, b in zip(x, y)),
                                     p_value)

    @staticmethod
    def nth_root(value, n_root):
        """ returns the n_root of an value """
        root_value = 1 / float(n_root)
        return round(Decimal(value) ** Decimal(root_value), 3)

    @staticmethod
    def cosine_similarity(x, y):
        """ return cosine similarity between two lists """

        numerator = sum(a * b for a, b in zip(x, y))
        denominator = MyMathHelper.square_rooted(x) * MyMathHelper.square_rooted(y)
        return round(numerator / float(denominator), 3)

    @staticmethod
    def square_rooted(x):
        """ return 3 rounded square rooted value """

        return round(sqrt(sum([a * a for a in x])), 3)

    @staticmethod
    def jaccard_similarity(x, y):
        """ returns the jaccard similarity between two lists """
        intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
        union_cardinality = len(set.union(*[set(x), set(y)]))
        return intersection_cardinality / float(union_cardinality)

    @staticmethod
    def variance(v):
        return np.var(v)

    @staticmethod
    def common_dimensions(v1, v2):
        """ takes in two vectors and returns a tuple of the vectors with both non zero dimensions
        i.e.
        v1 : [ 1, 2, 3, 0 ]        -->      return [2, 3]
        v2 : [ 0, 4, 5, 6 ]        -->      return [4, 5]  """
        list1, list2 = [], []
        for i in range(0, len(v1)):
            if v1[i] != 0 and v2[i] != 0:
                list1.append(v1[i])
                list2.append(v2[i])
                # print 'INDEX SAME:',i
        return list1, list2

    @staticmethod
    def average(my_list):
        avg = float(sum(my_list)) / float(len(my_list))
        return avg

    @staticmethod
    def net_list(my_list, average):
        """
        Finds the average of the list
        count is used for the denominator for the average equation (# non zero values for list for movie case)
        i.e.
        list : [ 7  8  9]      average = 8     take value - average
        return [ -1 0  1]
        """
        if len(my_list) == 0:  # Empty List
            return []
        net_list = []
        for i in range(0, len(my_list)):
            net_list.append(float(my_list[i]) - average)
        return net_list

    @staticmethod
    def nonzero_count(my_list):
        """
        takes in a list an returns the amount of non zero values in the list
        i.e.
        list [0 0 0 0 1 2 3 ] --> returns 3
        """
        counter = 0
        for value in my_list:
            if value != 0:
                counter += 1
        return counter

    @staticmethod
    def check_equal(my_list):
        return my_list[1:] == my_list[:-1]

    #############################################################################################################
    @staticmethod
    def iuf(number_total_users, number_users_rated_movie):
        try:
            return log10(number_total_users / number_users_rated_movie)
        except Exception, e:
            return 1

    @staticmethod
    def scale_list_by_iuf(my_list, number_total_users, movie_ratings_count_list):
        scaled_list = []
        for i in range(0,len(my_list)):
            iuf_factor = MyMathHelper.iuf(number_total_users, movie_ratings_count_list[i])
            scaled_list.append(my_list[i]*iuf_factor)
        return scaled_list

    # These functions are my custom versions of common mathematical concepts
    @staticmethod
    def custom_rounding(value):
        """
        performs rounding for the scope of this project. Rating scale is integers from 1-5
        """
        value = int(round(value))
        if value > 5:
            return 5
        elif value < 1:
            return 1
        return value

    @staticmethod
    def custom_case_amplification(value):
        """case amplifies value - basically taking an exponential to a constant 2.5"""
        bool_negative = False
        if value < 0:
            bool_negative = True

        result = abs(value) ** 2.5
        if bool_negative:
            result *= -1
        return result

    @staticmethod
    def custom_case_deamplification(value):
        """case amplifies value - basically taking an exponential to a constant 2.5"""
        bool_negative = False
        if value < 0:
            bool_negative = True

        result = abs(value) ** .8
        if bool_negative:
            result *= -1
        return result


    @staticmethod
    def custom_cosine_similarity(v1, v2):
        """
        compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)
        **Note: This cosine similarity only compares the similar dimensions of the two vectors
        """

        if len(v1) == 0:
            print 'Zero Dimension'
            print 'Cos(0D): .001'
            return 0.001
        elif len(v1) == 1:
            print 'One Dimension'
            # smaller_value = min(abs(v1[0]), abs(v2[0]))
            # bigger_value = max(abs(v1[0]), abs(v2[0]))  # todo Check when to return a negative number (for pearson)
            # value = 1.0 - (float(bigger_value) - float(smaller_value)) / 5
            value = 1/(abs(float(v1[0]) - v2[0])+1.15)
            print 'Cos(1D): ', value
            # value_after_scale = value * .12
            # print 'Final Sim:',value_after_scale
            return value
        else:
            print 'Multiple Dimensions'
            sumxx, sumxy, sumyy, value = 0, 0, 0, 0
            for i in range(len(v1)):
                x = v1[i]
                y = v2[i]
                sumxx += x * x
                sumyy += y * y
                sumxy += x * y
            try:
                value = float(sumxy) / math.sqrt(sumxx * sumyy)  # Calculate Cosine Similarity
            except Exception, e:
                print 'Error in custom_cosine_similarity:', e
                value = 0.001  # Edge case when denominator is 0
            print 'Cos(MD):', value
            # value_after_scale = value * math.log(len(v1), 100)
            # print 'Final Sim:',value_after_scale
            return value

    @staticmethod
    def custom_pearson(x, y):
        """calculate pearson coefficient"""
        # Assume len(x) == len(y)
        n = len(x)

        if n == 0:
            return 0
        elif n == 1:
            print 'One Dimension'
            print 'X:', x
            print 'Y:,', y
            smaller_value = min(abs(x[0]), abs(y[0]))
            bigger_value = max(abs(x[0]), abs(y[0]))  # todo Check when to return a negative number (for pearson)
            value = 1.0 - (float(bigger_value) - float(smaller_value)) / 5
            print 'Cos(1D): ', value
            # value_after_scale = value * .12
            # print 'Final Sim:',value_after_scale
            return value
        elif n == 2:
            value = MyMathHelper.custom_cosine_similarity(x,y)
            print 'Cos(MD):', value
            return value
        else:

            sum_x = float(sum(x))
            sum_y = float(sum(y))
            sum_x_sq = sum(map(lambda x: pow(x, 2), x))
            sum_y_sq = sum(map(lambda x: pow(x, 2), y))
            psum = sum(imap(lambda x, y: x * y, x, y))
            num = psum - (sum_x * sum_y/n)
            try:
                den = pow((sum_x_sq - pow(sum_x, 2) / n) * (sum_y_sq - pow(sum_y, 2) / n), 0.5)
                if den == 0: return 0
                value = num / den
                print 'Cos(MD): ', value
                return value
            except Exception, e:
                print "Exception in custom pearson:", e
                if MyMathHelper.check_equal(x):
                    value = x[0]
                elif MyMathHelper.check_equal(y):
                    value = x[0]
                else:
                    print "WTF IS HAPPENING"
                    value = 3
                print 'Pearson(MD): ', value
                return value