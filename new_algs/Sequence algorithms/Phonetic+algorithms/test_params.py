from unittest import TestCase

from code.cli import PARAMS_DIR

from code.prepare.params import load_params



class ParamsTestCase(TestCase):
	
	def test_load_params(self):
		params = load_params(PARAMS_DIR)
		
		self.assertIn('sounds', params)
		self.assertIn('logodds', params)
		self.assertIn('gap_penalties', params)
