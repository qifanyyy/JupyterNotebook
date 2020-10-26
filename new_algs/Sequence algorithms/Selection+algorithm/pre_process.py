#! /usr/bin/env python

'''
pre_process [OPTIONS] <SCENARIO_PATH>

Computes the SUNNY pre-solving phase and sets the corresponding arguments.

Note that feature selection is performed by using WEKA tool, and in particular 
the supervised attribute filter:

  weka.filters.supervised.attribute.AttributeSelection

which allows various search and evaluation methods to be combined.

Options
=======

--kb-path <PATH>
  PATH of the SUNNY knowledge base for the specified scenario. By default, it is 
  set to <SCENARIO_PATH>
  
--static-schedule 
  Computes a static schedule. If set, computes a static schedule (B, C) where:
    B: is the backup solver of the given scenario.
    C: is min{10, T/(M * 10)}, where T is the timeout and M the number of 
       algorithms of the given scenario.
  By default, this option is unset.
  TODO: Add more options for static scheduling?
  
--filter-portfolio
  Removes from the portfolio the solvers that are never the best solver for any 
  instance of the scenario. Unset by default.  
  
-S "<SEARCH>"
  Sets the search method and its options for WEKA subset evaluators, e.g.:
    -S "weka.attributeSelection.BestFirst -S 8"
  This option is allowed only in conjunction with -E option.
  
-E "<EVALUATOR>"
  Sets the attribute/subset evaluator and its options, e.g.:
    -E "weka.attributeSelection.CfsSubsetEval -L"
  This option is allowed only in conjunction with -S option.
  
--help
  Prints this message.
'''

import os
import csv
import sys
import json
import getopt
import shutil
from subprocess import Popen

in_path = os.path.realpath(__file__).split('/')[:-2]
CLASSPATH = '/'.join(in_path) + '/weka.jar'

def parse_arguments(args):
  '''
  Parse the options specified by the user and returns the corresponding
  arguments properly set.
  '''
  try:
    opts, args = getopt.getopt(
      args, 'S:E:', ['help', 'static-schedule', 'filter-portfolio', 'kb-path=']
    )
  except getopt.GetoptError as msg:
    print >> sys.stderr, msg
    print >> sys.stderr, 'For help use --help'
    sys.exit(2)
  
  if not args:
    if not opts:
      print >> sys.stderr, 'Error! No arguments given.'
      print >> sys.stderr, 'For help use --help'
      sys.exit(2)
    else:
      print __doc__
      sys.exit(0)

  scenario = args[0]
  if scenario[-1] != '/':
    scenario += '/'
  if not os.path.exists(scenario):
    print >> sys.stderr, 'Error: Directory ' + scenario + ' does not exists.'
    print >> sys.stderr, 'For help use --help'
    sys.exit(2)
    
  # Initialize variables with default values.
  feat_algorithm = None
  evaluator = ''
  search = ''
  static_schedule = False
  filter_portfolio = False
  kb_path = scenario
  kb_name = 'kb_' + scenario.split('/')[-2]

  # Options parsing.
  for o, a in opts:
    if o == '--help':
      print __doc__
      sys.exit(0)
    elif o == '-E':
      evaluator = a
    elif o == '-S':
      search = a
    elif o == '--static-schedule':
      static_schedule = True
    elif o == '--filter-portfolio':
      filter_portfolio = True
    elif o == '--kb-path':
      if not os.path.exists(a):
        print >> sys.stderr, 'Error! Directory ' + a + ' not exists.'
        print >> sys.stderr, 'For help use --help'
        sys.exit(2)
      if a[-1] == '/':
        kb_path = a[:-1]
      else:
        kb_path = a
  
  kb_name = kb_path.split('/')[-2]
  args_file = kb_path + '/kb_' + kb_name + '.args'
  info_file = kb_path + '/kb_' + kb_name + '.info'
  return args_file, info_file, scenario, evaluator, search, static_schedule, \
    filter_portfolio

def remove_exp(x):
  if 'e-' in x or 'E-' in x:
    return '0'
  else:
    return x

def select_features(args, info_file, scenario, evaluator, search, filter_pf):
  in_path = info_file[:info_file.rfind('/')] + '/feat_in.arff'
  in_file = open(in_path, 'w')
  
  reader = csv.reader(open(info_file), delimiter = '|')
  best = {}
  for row in reader:
    best_solvers = [
      (float(it['time']), s) 
      for s, it in eval(row[2]).items() 
      if it['info'] == 'ok'
    ]
    if not best_solvers:
      continue
    best_solver = min(best_solvers)[1]
    best[row[0]] = best_solver
  
  if filter_pf:
    args['portfolio'] = list(set(best.values()))
  
  reader = csv.reader(open(scenario + 'feature_values.arff'), delimiter = ',')
  pfolio = ','.join(args['portfolio'])
  for row in reader:
    if row:
      if 'instance_id' in row[0] or 'repetition' in row[0]:
	continue
      elif row and row[0].strip().upper() == '@DATA':
	in_file.write('@ATTRIBUTE best_solver {' + pfolio + '}\n\n')
	in_file.write('@DATA\n')
	break
      else:
	in_file.write(','.join(row) + '\n')
  for row in reader:
    if row[0] not in best.keys():
      continue
    label = best[row[0]]
    new_vector = [remove_exp(x) for x in row[2:]] + [label]
    in_file.write(','.join(new_vector) + '\n')
    
  in_file.close()  
  out_path = info_file[:info_file.rfind('/')] + '/feat_out.arff'
  weka_cmd = [
    'java', '-cp', CLASSPATH, 
    'weka.filters.supervised.attribute.AttributeSelection', 
    '-E', evaluator, '-S', search, '-i', in_path, '-o', out_path
  ]
  proc = Popen(weka_cmd)
  proc.communicate()
  
  new_features = []
  reader = csv.reader(open(out_path), delimiter = ' ')
  for row in reader:
    if row:
      if row[0] == '@attribute' and row[1] != 'best_solver':
	new_features.append(row[1])
      elif row[0] == '@data':
	break
  selected_features = dict(
    (feature, index) 
    for (feature, index) in args['selected_features'].items() 
    if feature in new_features
  )
  feature_steps = dict(
    (step, features) 
    for (step, features) in args['feature_steps'].items()
    if set(features).intersection(new_features)
  )
  return selected_features, feature_steps
  

def compute_schedule(args, max_time = 10):	
  solver = args['backup']
  time = args['timeout'] / (10 * len(args['portfolio']))
  return [(solver, min(time, max_time))]

def main(args):
  args_file, info_file, scenario, evaluator, search, static_schedule, \
    filter_portfolio = parse_arguments(args)
  with open(args_file) as infile:
    args = json.load(infile)
  infile.close()
  
  # Feature selection.
  if evaluator and search:
    selected_features, feature_steps = select_features(
      args, info_file, scenario, evaluator, search, filter_portfolio
    )
    args['selected_features'] = selected_features
    args['feature_steps'] = feature_steps
  elif filter_portfolio:
    reader = csv.reader(open(info_file), delimiter = '|')
    portfolio = set([])
    for row in reader:
      best_solvers = [
        (float(it['time']), s) 
        for s, it in eval(row[2]).items() 
        if it['info'] == 'ok'
      ]
      if not best_solvers:
        continue
      portfolio.add(min(best_solvers)[1])
    args['portfolio'] = list(portfolio)
  
  # Static schedule.
  if static_schedule:
    static_schedule = compute_schedule(args)
    args['static_schedule'] = static_schedule
    
  with open(args_file, 'w') as outfile:
    json.dump(args, outfile)
    
if __name__ == '__main__':
  main(sys.argv[1:])