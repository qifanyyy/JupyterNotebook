from code.prepare.base import load_data, load_targets
from code.prepare.lexstat import set_schema, make_wordlist, make_lexstat
from code.prepare.params import load_params
from code.prepare.pmi import get_asjp_data, get_pairs
from code.prepare.utils import is_asjp_data, ipa_to_asjp, asjp_to_asjp



def check(dataset_path, params_dir):
	"""
	Performs a dry run of the prepare command. Returns a helpful string
	reporting the results of the performed checks.
	
	The last check takes too long to be practical, so it is disabled.
	"""
	params = load_params(params_dir)
	data = load_data(dataset_path)
	
	report = [
		check_asjp_conversion(data, params),
		check_pmi(data, params),
		check_load_targets(data, dataset_path),
		check_lexstat(data, dataset_path)
	]
	
	return '\n\n'.join(report)



def check_asjp_conversion(data, params):
	"""
	Checks whether the transcriptions can be brought in shape for PMI
	algorithms consumption. Returns a helpful string reporting the check.
	"""
	report = ['# ASJP conversion']
	is_ok = True
	
	if is_asjp_data(data):
		func = asjp_to_asjp
	else:
		func = ipa_to_asjp
	
	for lang in data:
		for gloss in data[lang]:
			for trans in data[lang][gloss]:
				try:
					func(trans, params)
				except AssertionError:
					report.append(trans +' collapses to empty string')
					is_ok = False
	
	if is_ok:
		report.append('OK')
	
	return '\n'.join(report)



def check_pmi(data, params):
	"""
	Checks whether the ZeroDivisionError is lurking in the dataset. Returns a
	helpful string reporing the check.
	"""
	report = ['# ZeroDivisionError issue']
	is_ok = True
	
	data = get_asjp_data(data, params)
	lang_pairs = [(a, b) for a in data.keys() for b in data.keys() if a < b]
	
	for lang1, lang2 in lang_pairs:
		syn, _ = get_pairs(lang1, lang2, data)
		try:
			assert len(syn) > 0
		except AssertionError:
			report.append(lang1 +' and '+ lang2 +' share 0 synonymous pairs')
			is_ok = False
	
	if is_ok:
		report.append('OK')
	
	return '\n'.join(report)



def check_load_targets(data, dataset_path):
	"""
	Checks that load_targets will be well-behaved. Returns a helpful string
	reporting the check.
	"""
	report = ['# load_targets issue']
	
	sample_keys = []
	
	lang_pairs = [(a, b) for a in data.keys() for b in data.keys() if a < b]
	for lang1, lang2 in lang_pairs:
		syn, _ = get_pairs(lang1, lang2, data)
		sample_keys.extend(list(syn.keys()))
	
	load_targets(dataset_path, sample_keys, data.keys())
	
	report.append('OK')
	
	return '\n'.join(report)



def check_lexstat(data, dataset_path):
	"""
	Performs a dry run of the LexStat algorithm. Returns a helpful string
	reporting the check.
	"""
	report = ['# LexStat']
	is_ok = True
	
	with set_schema('asjp' if is_asjp_data(data) else 'ipa'):
		wordlist = make_wordlist(data, dataset_path)
		make_lexstat(wordlist, 1)
	
	if is_ok:
		report.append('OK')
	
	return '\n'.join(report)
