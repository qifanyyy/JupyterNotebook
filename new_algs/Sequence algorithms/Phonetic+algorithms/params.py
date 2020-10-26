import os.path

import numpy as np



def load_params(params_dir):
	params = {}
	
	params['sounds'], params['logodds'] = _load_logodds(params_dir)
	params['gap_penalties'] = _load_gap_penalties(params_dir)
	
	return params



def _load_logodds(params_dir):
	"""
	Returns (1) [] of the ASJP sounds; (2) the logodds table ready for
	consumption by calc_pmi_score().
	"""
	file_path = os.path.join(params_dir, 'logodds.csv')
	try:
		assert os.path.exists(file_path)
	except AssertionError:
		raise ValueError('Could not find the PMI logodds file')
	
	# ASJP sound classes
	with open(file_path) as f:
		sounds = np.array([x.strip('\"')
							for x in f.readline().strip().split(',')])
	
	# log odds
	with open(file_path) as f:
		logodds = np.array([x.strip().split(',')[1:]
							for x in f.readlines()[1:]], np.double)
	
	# convert log odds to dictionary
	lodict = dict()
	for i,s1 in enumerate(sounds):
		for j,s2 in enumerate(sounds):
			lodict[s1,s2] = logodds[i,j]
	
	return sounds, lodict



def _load_gap_penalties(params_dir):
	"""
	Returns the (penalty1, penalty2) tuple stored in the params dir.
	"""
	file_path = os.path.join(params_dir, 'gap_penalties.txt')
	
	try:
		assert os.path.exists(file_path)
	except AssertionError:
		raise ValueError('Could not find the PMI gap penalties file')
	
	with open(file_path) as f:
		penalties = tuple([float(x.strip()) for x in f.readlines()])
	
	try:
		assert len(penalties) == 2
	except AssertionError:
		raise ValueError('Could not parse the PMI gap penalties file')
	
	return penalties
