import unittest
from Lab_LinearSearch import linearSearch, sortedLinearSearch
from Lab_BinarySearch import binarySearch, sortedbinarySearch

class SearchTestCase(unittest.TestCase):
	# test for linear Search

	def test_linearsearch(self):
		values=[5,3,6,1,2,9,0]
		self.assertEqual(linearSearch(values,5),True) 
		self.assertEqual(linearSearch(values,1),True)
		self.assertEqual(linearSearch(values,7),False)

	def test_sortedLinearSearch(self):
		values=[5,3,6,1,2,9,0]
		values=sorted(values)
		self.assertEqual(linearSearch(values,5),True) 
		self.assertEqual(linearSearch(values,1),True)
		self.assertEqual(linearSearch(values,7),False)

	def test_binarySearch(self):
		values=[5,3,6,1,2,9,0]

		self.assertEqual(linearSearch(values,5),True) 
		self.assertEqual(linearSearch(values,1),True)
		self.assertEqual(linearSearch(values,7),False)

	def test_sortedbinearSearch(self):
		values=[5,3,6,1,2,9,0]
		values=sorted(values)
		self.assertEqual(linearSearch(values,5),True) 
		self.assertEqual(linearSearch(values,1),True)
		self.assertEqual(linearSearch(values,7),False)

if __name__=='__main__':
	unittest.main()





	