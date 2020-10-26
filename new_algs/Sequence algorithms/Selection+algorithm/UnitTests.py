import unittest
import LinearSelection

class Tests(unittest.TestCase):
    def test_slice_in_groups_of_five(self):
        passed_array = [1,2,3,4,5,6,7,8,81,65,41,99,312,32,61,23,654,23,11,58,33,123,34,12]
        result = LinearSelection.slice_in_groups_of_five(passed_array)
        expected_arrays = [[1, 2, 3, 4, 5], [6, 7, 8, 81, 65], [41, 99, 312, 32, 61], [23, 654, 23, 11, 58], [33, 123, 34, 12]]

        self.assertEqual(result, expected_arrays, "Didn't split array successfully")
    
    def test_sort_array_of_arrays(self):
        passed_array = [[1,2,3,4,5], [6,7,8,81,65]]
        result = LinearSelection.sort_array_of_arrays(passed_array)
        expected_arrays = [[1, 2, 3, 4, 5], [6, 7, 8, 65, 81]]

        self.assertEqual(result, expected_arrays, "Didn't order arrays correctly")

    def test_find_median(self):
        passed_array = [1,2,3,4,5]
        result = LinearSelection.find_median(passed_array)
        expected_result = 3

        self.assertEqual(result, expected_result, "Didn't find the median correctly")

    def test_find_medians_array_full(self):
        passed_array = [[1,2,3,4,5], [6,7,8,65,81]]
        result = LinearSelection.find_medians_array(passed_array, 10)
        expected_result = [3,8]

        self.assertEqual(result, expected_result, "Didn't generate the medians array correctly for full arrays")

    def test_find_medians_array_extras(self):
        passed_array = [[1,2,3,4,5], [6,7,8]]
        result = LinearSelection.find_medians_array(passed_array, 8)
        expected_result = [3]

        self.assertEqual(result, expected_result, "Didn't generate the medians array correctly for arrays with extras")

    def test_partition_set(self):
        passed_array = [1,49,92,43,67,5,8,6,81] # [1,5,6,8,43,49,67,81,92] -> median is 43
        lesser, greater = LinearSelection.partition_set(passed_array, 43)
        expected_lesser = [1,5,8,6]
        expected_greater = [49,92,67,81]

        self.assertEqual(lesser, expected_lesser, "Didn't match lesser set correctly")
        self.assertEqual(greater, expected_greater, "Didn't match greater set correctly")

    def test_ultimate_integration(self):
        passed_array = [1,2,3,4,5,6,7,8,81,65,41,99,312,32,61,24,654,23,11,58,33,123,34,12]
                    #   1,2,3,4,5,6,7,8,11,12,23,24,32,33,34,41,58,61,65,81,99,123,312,654
        element = LinearSelection.linear_selection(passed_array, 14)
        expectedElement = 33

        self.assertEqual(element, expectedElement, "Didn't match expected element in ultimate integration test")

unittest.main()