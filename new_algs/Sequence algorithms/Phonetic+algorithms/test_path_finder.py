import os.path

from unittest import TestCase

from code.cli import DATASETS_DIR
from code.path_finder import *



class PathFinderTestCase(TestCase):
	
	def test_find_dataset(self):
		self.assertEqual(
			find_dataset(DATASETS_DIR, 'abvd'),
			os.path.abspath('data/datasets/abvd.tsv'))
		
		self.assertEqual(
			find_dataset(DATASETS_DIR, 'mayan'),
			os.path.abspath('data/datasets/mayan.tsv'))
	
	def test_find_all_datasets(self):
		paths = find_all_datasets(DATASETS_DIR)
		self.assertEqual(len(paths), 18)
	
	def test_get_dataset_name(self):
		self.assertEqual('mayan',
			get_dataset_name('data/datasets/mayan.tsv'))
		
		self.assertEqual('ob_ugrian',
			get_dataset_name('data/datasets/ob_ugrian.tsv'))
