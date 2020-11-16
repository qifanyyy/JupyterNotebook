import csv
import os.path

from code.path_finder import find_all_datasets

from code.prepare.base import load_data
from code.prepare.lexstat import make_lexstat, set_schema
from code.prepare.utils import is_asjp_data

from code.infer.base import infomap_clustering



def infer_lexstat(datasets_dir, output_dir):
	"""
	Finds the datasets in the given dir and runs the _infer_lexstat function on
	each of these, specifying the correct lingpy transcription schema.
	"""
	for dataset_path in find_all_datasets(datasets_dir):
		name = os.path.basename(dataset_path).split('.')[0]
		output_path = os.path.join(output_dir, '{}.lsCC.csv'.format(name))
		
		schema = 'asjp' if is_asjp_data(load_data(dataset_path)) else 'ipa'
		with set_schema(schema):
			_infer_lexstat(dataset_path, output_path)



def _infer_lexstat(dataset_path, output_path, threshold=0.57):
	"""
	Runs the LexStat algorithm on the specified dataset and writes the inferred
	cognate classes to the specified output path.
	
	Assumes that the correct lingpy transcription schema is already set.
	"""
	data = []
	with open(dataset_path) as f:
		reader = csv.DictReader(f, delimiter='\t')
		data = [row for row in reader]
	
	new_data = {}  # the data formatted as LexStat wants it
	new_data[0] = ['doculect', 'concept', 'ipa', 'tokens', 'cogid']
	
	for key, row in enumerate(data, 1):
		new_data[key] = [row['language'], row['gloss'],
			row['transcription'], row['tokens'].split(), row['cognate_class']]
	
	lex = make_lexstat(new_data)
	
	lex.cluster(method='lexstat', threshold=threshold,
		external_function=lambda x, y: infomap_clustering(y, x, revert=True),
		ref='lexstat_infomap')
	
	with open(output_path, 'w', newline='', encoding='utf-8') as f:
		writer = csv.writer(f)
		writer.writerow(['concept', 'doculect', 'counterpart', 'cogid', 'lpID'])
		
		for key in lex:
			doculect = lex[key][lex.header['doculect']]
			concept = lex[key][lex.header['concept']]
			trans = lex[key][lex.header['ipa']]
			cog_class = lex[key][lex.header['cogid']]
			lexstat_infomap = lex[key][lex.header['lexstat_infomap']]
			
			writer.writerow([
				concept, doculect, trans, cog_class, lexstat_infomap])
