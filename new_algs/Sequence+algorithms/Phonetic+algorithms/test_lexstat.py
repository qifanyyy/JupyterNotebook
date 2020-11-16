import os.path

from unittest import TestCase

from lingpy.basic.wordlist import Wordlist
from lingpy.compare.lexstat import LexStat

from code.cli import TESTS_DIR

from code.prepare.base import load_data
from code.prepare.lexstat import *



FIXTURE_DATASET = os.path.join(TESTS_DIR, 'fixtures/GER.tsv')
FIXTURE_DATASET_ASJP = os.path.join(TESTS_DIR, 'fixtures/Afrasian.tsv')




class LexStatTestCase(TestCase):
	
	def setUp(self):
		self.data = load_data(FIXTURE_DATASET)
		self.data_asjp = load_data(FIXTURE_DATASET_ASJP)
	
	def skip_load_tokens(self):
		pass
	
	def test_make_wordlist(self):
		li = make_wordlist(self.data, FIXTURE_DATASET)
		self.assertTrue(isinstance(li, Wordlist))
		
		self.assertEqual(len(li), 814)
		
		self.assertEqual(li[1], ['Danish', '1035', 'goˀ', 1, 'g oˀ'])
		self.assertEqual(li[len(li)], ['Swedish', '98', 'alː', 1, 'a lː'])
		
		self.assertEqual(
			li.get_list(concept='98', entry='doculect', flat=True),
			['Danish', 'Dutch', 'English', 'German',
			 'Icelandic', 'Norwegian', 'Swedish'])
		self.assertEqual(
			li.get_list(concept='98', entry='ipa', flat=True),
			['æˀl', 'ɑlə', 'ɔːl', 'al', 'at͡lir', 'ɑlə', 'alː'])
	
	def test_make_wordlist_asjp(self):
		with set_schema('asjp'):
			li = make_wordlist(self.data_asjp, FIXTURE_DATASET_ASJP, 'asjp')
			self.assertTrue(isinstance(li, Wordlist))
			
			self.assertEqual(len(li), 829)
			
			self.assertEqual(
				li.get_list(concept='667', entry='doculect', flat=True),
				['AHAGGAR', 'AMHARIC_3', 'ARABIC_LEBANESE', 'ARABIC_QURANIC',
				'BEJA_2', 'BOLEWA', 'DAHALO_2', 'GEEZ', 'GHADAMES_2',
				'HARARI_2', 'HAUSA_3', 'JIBBALI', 'KAFFA', 'MEHRI_2', 'OROMO',
				'QABYLE', 'SOQOTRI_2', 'SYRIAC_2', 'TIGRAI', 'ZENAGA_2'])
			self.assertEqual(
				li.get_list(concept='667', entry='ipa', flat=True),
				['abar3qa', 'm3ng3d', 'darab', 'tX~ariq',
				'lagi', 'gogo', 'le', 'f3not', 'abrid',
				'%uga', 'ha5a', 'orm', 'woreto', 'Xirum', 'kara',
				'abrid', 'orim', 'urX', 'mangadi', 'tir3s'])
	
	def test_filter_wordlist(self):
		wordlist = make_wordlist(self.data, FIXTURE_DATASET)
		li = filter_wordlist(wordlist, 'English', 'German')
		
		self.assertTrue(isinstance(li, Wordlist))
		self.assertEqual(len(li), 115+112)
		
		self.assertEqual(
			li.get_list(concept='98', entry='doculect', flat=True),
			['English', 'German'])
		self.assertEqual(
			li.get_list(concept='98', entry='ipa', flat=True),
			['ɔːl', 'al'])
	
	def test_filter_wordlist_asjp(self):
		with set_schema('asjp'):
			wordlist = make_wordlist(self.data_asjp, FIXTURE_DATASET_ASJP, 'asjp')
			li = filter_wordlist(wordlist, 'AMHARIC_3', 'SOQOTRI_2')
			
			self.assertTrue(isinstance(li, Wordlist))
			self.assertEqual(len(li), 40+39)
			
			self.assertEqual(
				li.get_list(concept='667', entry='doculect', flat=True),
				['AMHARIC_3', 'SOQOTRI_2'])
			self.assertEqual(
				li.get_list(concept='667', entry='ipa', flat=True),
				['m3ng3d', 'orim'])
	
	def test_make_lexstat(self):
		lex = make_lexstat(make_wordlist(self.data, FIXTURE_DATASET), 1)
		self.assertTrue(isinstance(lex, LexStat))
	
	def test_make_lexstat_asjp(self):
		with set_schema('asjp'):
			lex = make_lexstat(make_wordlist(self.data_asjp, FIXTURE_DATASET_ASJP, 'asjp'), 1)
			self.assertTrue(isinstance(lex, LexStat))
	
	def test_get_pairs(self):
		lex = make_lexstat(make_wordlist(self.data, FIXTURE_DATASET), 1)
		pairs = get_pairs('English', 'German', lex)
		self.assertEqual(len(pairs), 117)
		
		for key1, key2 in pairs:
			self.assertEqual(lex[key1][0], 'English')
			self.assertEqual(lex[key2][0], 'German')
			self.assertEqual(lex[key1][1], lex[key2][1])
	
	def test_calc_lexstat(self):
		scores = calc_lexstat('English', 'German', make_wordlist(self.data, FIXTURE_DATASET))
		self.assertEqual(len(scores), 117)
		
		womanFrau = scores['962/English,German/1,1']
		womanWeib = scores['962/English,German/1,2']
		self.assertAlmostEqual(womanFrau[0], womanWeib[0])
