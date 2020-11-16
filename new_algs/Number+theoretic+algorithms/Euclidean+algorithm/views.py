from django.shortcuts import render
from math import sqrt, pow
# Create your views here.
class CalculationEuclidiano():
    
    @staticmethod
    def calculation(coordinate_one, coordinate_two):
        
        keys_one = coordinate_one.keys()
        keys_two = coordinate_two.keys()
        if  not (('coordinate_X'  in keys_one) and ('coordinate_Y' in keys_one )and ('coordinate_X'  in keys_two) and ('coordinate_Y' in keys_two)):
            raise KeyError('A property is not correct')

        cal_x = pow((coordinate_two['coordinate_X'] - coordinate_one['coordinate_X']),2)
        cal_y = pow((coordinate_two['coordinate_Y'] - coordinate_one['coordinate_Y']),2)

        return round(sqrt(cal_x + cal_y), 4)