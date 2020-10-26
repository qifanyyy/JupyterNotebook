import os.path

from unittest import TestCase, skip

from code.cli import PARAMS_DIR, TESTS_DIR

from code.prepare.base import *
from code.prepare.base import _prepare
from code.prepare.params import load_params
from code.prepare.pmi import get_pairs



FIXTURE_DATASET = os.path.join(TESTS_DIR, 'fixtures/GER.tsv')



class PrepareTestCase(TestCase):
	
	def test_load_data(self):
		data = load_data(FIXTURE_DATASET)
		
		count = sum([len(j) for i in data.values() for j in i.values()])
		self.assertEqual(count, 814)
		
		for lang in [
			'Danish', 'Dutch', 'English', 'German',
			'Icelandic', 'Norwegian', 'Swedish'
		]: self.assertIn(lang, data)
		
		self.assertEqual(data['Norwegian']['1226'], ['oːɾ'])
		self.assertEqual(data['German']['962'], ['frau', 'vaip'])
	
	def test_load_targets(self):
		data = load_data(FIXTURE_DATASET)
		pairs, _ = get_pairs('English', 'German', data)
		t = load_targets(FIXTURE_DATASET, pairs.keys(), data.keys())
		
		self.assertEqual(t['98/English,German/1,1'], True)
		self.assertEqual(t['962/English,German/1,1'], False)
		self.assertEqual(t['962/English,German/1,2'], True)
	
	def test_get_average_gloss_len(self):
		data = load_data(FIXTURE_DATASET)
		gloss_len = get_average_gloss_len(data)
		
		self.assertEqual(gloss_len['98'], 23/7)
		self.assertEqual(gloss_len['1226'], 25/7)
	
	# @skip('for speed')
	def test_prepare(self):
		samples, targets = _prepare(FIXTURE_DATASET, PARAMS_DIR)
		self.assertEqual(len(samples), 2613)
		
		for key, sample in samples.items():
			self.assertEqual(len(sample), 9)
		
		womanFrau = samples['962/English,German/1,1']
		self.assertEqual(womanFrau[0], -7.005012217116)
		self.assertAlmostEqual(womanFrau[1], 0.4219680350987151, 1)
		self.assertAlmostEqual(womanFrau[2], 0.8628257140265899, 1)
		self.assertAlmostEqual(womanFrau[3], 3.63223180795, 0)
		self.assertAlmostEqual(womanFrau[4], 1.289847282477176, 1)
		self.assertEqual(womanFrau[5], 37/8)
		
		womanWeib = samples['962/English,German/1,2']
		self.assertEqual(womanWeib[0], -7.557346819036999)
		self.assertAlmostEqual(womanWeib[1], 0.477984957693513, 1)
		self.assertAlmostEqual(womanWeib[2], 0.7381760162462817, 1)
		self.assertAlmostEqual(womanWeib[3], 3.63223180795, 0)
		self.assertAlmostEqual(womanWeib[4], 1.289847282477176, 1)
		self.assertEqual(womanWeib[5], 37/8)
		
		self.assertEqual(len(targets), len(samples))
		self.assertEqual(targets['98/English,German/1,1'], True)
		self.assertEqual(targets['962/English,German/1,1'], False)
		self.assertEqual(targets['962/English,German/1,2'], True)
