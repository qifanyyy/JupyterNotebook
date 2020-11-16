import os.path

from unittest import TestCase

from code.cli import PARAMS_DIR, TESTS_DIR

from code.prepare.base import load_data
from code.prepare.lexstat import set_schema
from code.prepare.pmi import *
from code.prepare.params import load_params



FIXTURE_DATASET = os.path.join(TESTS_DIR, 'fixtures/GER.tsv')



class PMITestCase(TestCase):
	
	def setUp(self):
		self.params = load_params(PARAMS_DIR)
		self.data = load_data(FIXTURE_DATASET)
	
	def test_get_pairs(self):
		syn, non_syn = get_pairs('English', 'German', self.data)
		
		self.assertEqual(len(syn), 117)
		self.assertIn('962/English,German/1,1', syn)
		self.assertIn('962/English,German/1,2', syn)
		
		self.assertEqual(len(non_syn), 12763)
		self.assertIn(('ɔːl', 'jaːr'), non_syn)
		self.assertIn(('jɪər', 'al'), non_syn)
	
	def test_get_asjp_data(self):
		data = get_asjp_data(self.data, self.params)
		
		count = sum([len(j) for i in data.values() for j in i.values()])
		self.assertEqual(count, 814)
		
		self.assertEqual(data['English']['98'], ['ol'])
		self.assertEqual(data['Norwegian']['1226'], ['or'])
		self.assertEqual(data['German']['962'], ['frau', 'vaip'])
	
	def test_get_asjp_data_in_lexstat_asjp_mode(self):
		set_schema('asjp')
		
		data = get_asjp_data(self.data, self.params)
		
		count = sum([len(j) for i in data.values() for j in i.values()])
		self.assertEqual(count, 814)
		
		self.assertEqual(data['English']['98'], ['ol'])
		self.assertEqual(data['Norwegian']['1226'], ['or'])
		self.assertEqual(data['German']['962'], ['frau', 'vaip'])
	
	def test_calc_pmi(self):
		self.assertEqual(calc_pmi('ol', 'al', self.params), 2.960483758607)
	
	def test_prepare_lang_pair(self):
		asjp_data = get_asjp_data(self.data, self.params)
		s = prepare_lang_pair('English', 'German', asjp_data, self.params)
		
		self.assertEqual(len(s), 117)
		
		self.assertEqual(s['962/English,German/1,1'][0], -7.005012217116)
		self.assertAlmostEqual(s['962/English,German/1,1'][1], 0.4219680350987151, 1)
		self.assertAlmostEqual(s['962/English,German/1,1'][2], 0.8628257140265899, 1)
		
		self.assertEqual(s['962/English,German/1,2'][0], -7.557346819036999)
		self.assertAlmostEqual(s['962/English,German/1,2'][1], 0.477984957693513, 1)
		self.assertAlmostEqual(s['962/English,German/1,2'][2], 0.7381760162462817, 1)
		
		for sample in s.values():
			self.assertEqual(len(sample), 5)
			self.assertAlmostEqual(sample[3], 3.63223180795, 0)
			self.assertAlmostEqual(sample[4], 1.289847282477176, 1)
