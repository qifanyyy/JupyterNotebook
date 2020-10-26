from django.test import TestCase
from .views import CalculationEuclidiano
# Create your tests here.

class CalculationEuclidianaTest(TestCase):
    def setUp(self):
        self.result_ok = 1.4142
        self.coordinate_one = {
            "coordinate_X": 2,
            "coordinate_Y": 3,
        }
        self.coordinate_two = {
            "coordinate_X": 1,
            "coordinate_Y": 2,
        }

        self.coordinate_one_error_name = {
            "coordin_X": 1,
            "coordinate_Y": 2,
        }
        self.coordinate_two_error_name = {
            "coordinate_X": 1,
            "duck_Y": 2,
        }

    def test_calculation_ok(self):
        
        result = CalculationEuclidiano.calculation(self.coordinate_one, self.coordinate_two)

        self.assertEqual(self.result_ok, result)

    def test_calculation_is_not_ok(self):
        self.assertRaises(KeyError, CalculationEuclidiano.calculation,self.coordinate_one_error_name, self.coordinate_two_error_name)
