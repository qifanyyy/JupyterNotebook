import os.path

from unittest import TestCase

from code.cli import PARAMS_DIR, TESTS_DIR

from code.prepare.base import load_data
from code.prepare.params import load_params
from code.prepare.utils import *



FIXTURE_DATASET = os.path.join(TESTS_DIR, 'fixtures/GER.tsv')
FIXTURE_DATASET_ASJP = os.path.join(TESTS_DIR, 'fixtures/Afrasian.tsv')



class UtilsTestCase(TestCase):
	
	def setUp(self):
		self.params = load_params(PARAMS_DIR)
	
	def test_make_sample_id(self):
		self.assertEqual(
			make_sample_id('98', 'English', 'German', 1, 1),
			'98/English,German/1,1')
	
	def test_ipa_to_asjp(self):
		self.assertEqual(ipa_to_asjp('at͡lir', self.params), 'atir')
		self.assertEqual(ipa_to_asjp('oːɾ', self.params), 'or')
		self.assertEqual(ipa_to_asjp('ɔːl', self.params), 'ol')
		
		self.assertEqual(ipa_to_asjp('ũ', self.params), 'u')
		with self.assertRaises(AssertionError):
			ipa_to_asjp('XXX', self.params)
	
	def test_is_asjp_data(self):
		self.assertFalse(is_asjp_data(load_data(FIXTURE_DATASET)))
		self.assertTrue(is_asjp_data(load_data(FIXTURE_DATASET_ASJP)))
